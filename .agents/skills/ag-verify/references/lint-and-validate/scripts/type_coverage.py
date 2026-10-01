#!/usr/bin/env python3
"""Pragmatic TypeScript and Python type-safety checker.

The checker prefers real compiler output when a local TypeScript compiler is
available. Its source fallback focuses on explicit escape hatches such as
``any`` and ``@ts-ignore``; inferred TypeScript return types are not treated as
coverage failures.
"""
from __future__ import annotations

import ast
import json
import math
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

SKIP_DIRS = {
    ".git",
    ".next",
    ".venv",
    "build",
    "coverage",
    "dist",
    "node_modules",
    "out",
    "venv",
    "__pycache__",
}


def _source_files(project: Path, suffixes: set[str]) -> list[Path]:
    files: list[Path] = []
    for path in project.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in suffixes:
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.name.endswith(".d.ts"):
            continue
        files.append(path)
    return sorted(files)


def _local_tsc(tsconfig: Path) -> Path | None:
    executable = "tsc.cmd" if sys.platform == "win32" else "tsc"
    for parent in (tsconfig.parent, *tsconfig.parents):
        candidate = parent / "node_modules" / ".bin" / executable
        if candidate.is_file():
            return candidate
    return None


def _run_typescript_compilers(project: Path) -> list[dict[str, Any]]:
    runs: list[dict[str, Any]] = []
    tsconfigs = [
        path
        for path in project.rglob("tsconfig.json")
        if not any(part in SKIP_DIRS for part in path.parts)
    ]
    for tsconfig in sorted(tsconfigs):
        compiler = _local_tsc(tsconfig)
        if compiler is None:
            runs.append({"config": str(tsconfig), "status": "skipped", "reason": "local tsc not installed"})
            continue
        proc = subprocess.run(
            [str(compiler), "--noEmit", "--pretty", "false", "-p", str(tsconfig)],
            cwd=tsconfig.parent,
            capture_output=True,
            text=True,
            check=False,
            timeout=180,
        )
        runs.append(
            {
                "config": str(tsconfig),
                "status": "passed" if proc.returncode == 0 else "failed",
                "returncode": proc.returncode,
                "output": "\n".join(part.strip() for part in (proc.stdout, proc.stderr) if part.strip())[-4000:],
            }
        )
    return runs


def check_typescript_coverage(project_path: Path) -> dict[str, Any]:
    issues: list[str] = []
    passed: list[str] = []
    files = _source_files(project_path, {".ts", ".tsx"})
    stats: dict[str, Any] = {
        "any_count": 0,
        "suppression_count": 0,
        "files_with_any": 0,
        "compiler_runs": [],
    }

    if not files:
        return {"type": "typescript", "files": 0, "passed": [], "issues": ["[!] No TypeScript files found"], "stats": stats}

    any_pattern = re.compile(r"(?::\s*any\b|\bas\s+any\b|<any>)")
    suppression_pattern = re.compile(r"@ts-(?:ignore|nocheck)")
    for file_path in files:
        content = file_path.read_text("utf-8", errors="ignore")
        any_count = len(any_pattern.findall(content))
        stats["any_count"] += any_count
        stats["files_with_any"] += int(any_count > 0)
        stats["suppression_count"] += len(suppression_pattern.findall(content))

    any_fail_threshold = max(10, math.ceil(len(files) * 0.25))
    suppression_fail_threshold = max(3, math.ceil(len(files) * 0.05))

    if stats["any_count"] == 0:
        passed.append("[OK] No explicit 'any' escape hatches found")
    elif stats["any_count"] > any_fail_threshold:
        issues.append(
            f"[X] {stats['any_count']} explicit 'any' usages exceed the project threshold of {any_fail_threshold}"
        )
    else:
        issues.append(
            f"[!] {stats['any_count']} explicit 'any' usages across {stats['files_with_any']} file(s)"
        )

    if stats["suppression_count"] > suppression_fail_threshold:
        issues.append(
            f"[X] {stats['suppression_count']} TypeScript suppression comments exceed the threshold of {suppression_fail_threshold}"
        )
    elif stats["suppression_count"]:
        issues.append(f"[!] {stats['suppression_count']} TypeScript suppression comment(s) found")
    else:
        passed.append("[OK] No @ts-ignore or @ts-nocheck suppressions found")

    stats["compiler_runs"] = _run_typescript_compilers(project_path)
    failed_runs = [run for run in stats["compiler_runs"] if run["status"] == "failed"]
    completed_runs = [run for run in stats["compiler_runs"] if run["status"] == "passed"]
    if failed_runs:
        issues.append(f"[X] TypeScript compiler failed for {len(failed_runs)} project(s)")
    elif completed_runs:
        passed.append(f"[OK] TypeScript compiler passed for {len(completed_runs)} project(s)")
    elif stats["compiler_runs"]:
        passed.append("[OK] Compiler check skipped because project-local tsc is not installed")

    passed.append(f"[OK] Analyzed {len(files)} TypeScript files")
    return {"type": "typescript", "files": len(files), "passed": passed, "issues": issues, "stats": stats}


def _annotation_complete(node: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    positional = [*node.args.posonlyargs, *node.args.args, *node.args.kwonlyargs]
    relevant = [arg for arg in positional if arg.arg not in {"self", "cls"}]
    args_typed = all(arg.annotation is not None for arg in relevant)
    varargs_typed = node.args.vararg is None or node.args.vararg.annotation is not None
    kwargs_typed = node.args.kwarg is None or node.args.kwarg.annotation is not None
    return args_typed and varargs_typed and kwargs_typed and node.returns is not None


def check_python_coverage(project_path: Path) -> dict[str, Any]:
    issues: list[str] = []
    passed: list[str] = []
    files = _source_files(project_path, {".py"})
    stats = {"typed_functions": 0, "untyped_functions": 0, "any_count": 0, "parse_errors": 0}

    if not files:
        return {"type": "python", "files": 0, "passed": [], "issues": ["[!] No Python files found"], "stats": stats}

    for file_path in files:
        try:
            tree = ast.parse(file_path.read_text("utf-8", errors="ignore"), filename=str(file_path))
        except SyntaxError:
            stats["parse_errors"] += 1
            continue
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                key = "typed_functions" if _annotation_complete(node) else "untyped_functions"
                stats[key] += 1
            elif isinstance(node, ast.Name) and node.id == "Any":
                stats["any_count"] += 1

    total = stats["typed_functions"] + stats["untyped_functions"]
    typed_ratio = (stats["typed_functions"] / total * 100) if total else 100.0
    stats["typed_ratio"] = round(typed_ratio, 2)

    if stats["parse_errors"]:
        issues.append(f"[X] {stats['parse_errors']} Python file(s) could not be parsed")
    if typed_ratio >= 65:
        passed.append(f"[OK] Fully annotated Python functions: {typed_ratio:.0f}%")
    elif typed_ratio >= 40:
        issues.append(f"[!] Fully annotated Python functions: {typed_ratio:.0f}%")
    else:
        issues.append(f"[X] Fully annotated Python functions: {typed_ratio:.0f}%")

    any_fail_threshold = max(50, len(files) * 3)
    if stats["any_count"] == 0:
        passed.append("[OK] No Python Any references found")
    elif stats["any_count"] > any_fail_threshold:
        issues.append(
            f"[X] {stats['any_count']} Python Any references exceed the project threshold of {any_fail_threshold}"
        )
    else:
        issues.append(f"[!] {stats['any_count']} Python Any reference(s) found")

    passed.append(f"[OK] Analyzed {len(files)} Python files")
    return {"type": "python", "files": len(files), "passed": passed, "issues": issues, "stats": stats}


def main() -> int:
    project_path = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    if not project_path.is_dir():
        print(json.dumps({"error": f"Directory not found: {project_path}"}))
        return 2

    print("\n" + "=" * 60)
    print("  TYPE SAFETY CHECKER")
    print("=" * 60 + "\n")

    results = [
        result
        for result in (
            check_typescript_coverage(project_path),
            check_python_coverage(project_path),
        )
        if result["files"] > 0
    ]
    if not results:
        print("[!] No TypeScript or Python files found.")
        return 0

    critical_issues = 0
    for result in results:
        print(f"\n[{result['type'].upper()}]\n" + "-" * 40)
        for item in result["passed"]:
            print(f"  {item}")
        for item in result["issues"]:
            print(f"  {item}")
            critical_issues += int(item.startswith("[X]"))

    print("\n" + "=" * 60)
    if critical_issues:
        print(f"[X] TYPE SAFETY: {critical_issues} blocking issue(s)")
        return 1
    print("[OK] TYPE SAFETY: ACCEPTABLE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
