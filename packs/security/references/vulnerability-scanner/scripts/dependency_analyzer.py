#!/usr/bin/env python3
"""Offline dependency hygiene analyzer for common package ecosystems."""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SKIP_DIRS = {"node_modules", ".git", ".agents", ".agent", ".venv", "venv", "dist", "build", ".next", "vendor"}
SEVERITY = {"none": 99, "low": 1, "medium": 2, "high": 3, "critical": 4}


def iter_named_files(root: Path, names: set[str]):
    for path in root.rglob("*"):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.is_file() and path.name in names:
            yield path


def add(findings: list[dict[str, Any]], severity: str, issue: str, path: Path, detail: str) -> None:
    findings.append({"severity": severity, "issue": issue, "file": path.as_posix(), "detail": detail})


def analyze_package_json(path: Path, root: Path, findings: list[dict[str, Any]]) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text("utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        add(findings, "high", "Invalid package.json", path.relative_to(root), str(exc))
        return {"file": path.relative_to(root).as_posix(), "dependencies": 0}

    deps: dict[str, str] = {}
    for section in ("dependencies", "devDependencies", "peerDependencies", "optionalDependencies"):
        values = data.get(section, {})
        if isinstance(values, dict):
            deps.update({str(k): str(v) for k, v in values.items()})

    for name, spec in deps.items():
        normalized = spec.strip().lower()
        if normalized in {"*", "latest", "next"}:
            add(findings, "high", "Unbounded dependency version", path.relative_to(root), f"{name}: {spec}")
        elif normalized.startswith(("http://", "https://", "git://", "git+http://")):
            add(findings, "high", "Dependency fetched from mutable remote", path.relative_to(root), f"{name}: {spec}")
        elif normalized.startswith("github:") and "#" not in normalized:
            add(findings, "medium", "GitHub dependency is not pinned to a ref", path.relative_to(root), f"{name}: {spec}")

    package_dir = path.parent
    locks = [name for name in ("package-lock.json", "npm-shrinkwrap.json", "yarn.lock", "pnpm-lock.yaml", "bun.lock", "bun.lockb") if (package_dir / name).exists()]
    if not locks:
        add(findings, "high", "Missing JavaScript lock file", path.relative_to(root), "Add and commit one package-manager lock file.")
    elif len(locks) > 1:
        add(findings, "medium", "Multiple JavaScript lock files", path.relative_to(root), ", ".join(locks))
    return {"file": path.relative_to(root).as_posix(), "dependencies": len(deps), "lock_files": locks}


def analyze_requirements(path: Path, root: Path, findings: list[dict[str, Any]]) -> dict[str, Any]:
    unpinned = []
    total = 0
    try:
        lines = path.read_text("utf-8").splitlines()
    except OSError as exc:
        add(findings, "high", "Unreadable requirements file", path.relative_to(root), str(exc))
        return {"file": path.relative_to(root).as_posix(), "dependencies": 0}
    for raw in lines:
        line = raw.strip()
        if not line or line.startswith(("#", "-r", "--", "-e")):
            continue
        total += 1
        if " @ " in line or re.search(r"===|==", line):
            continue
        if re.match(r"^[A-Za-z0-9_.-]+(?:\[[^]]+\])?\s*(?:$|[<>!~]=?)", line):
            unpinned.append(line)
    for spec in unpinned[:25]:
        add(findings, "medium", "Python dependency is not exactly pinned", path.relative_to(root), spec)
    return {"file": path.relative_to(root).as_posix(), "dependencies": total, "unpinned": len(unpinned)}


def analyze(root: Path) -> dict[str, Any]:
    findings: list[dict[str, Any]] = []
    manifests: list[dict[str, Any]] = []
    for path in iter_named_files(root, {"package.json"}):
        manifests.append(analyze_package_json(path, root, findings))
    for path in iter_named_files(root, {"requirements.txt", "requirements-dev.txt", "requirements-prod.txt"}):
        manifests.append(analyze_requirements(path, root, findings))

    # Lightweight presence checks for other ecosystems.
    for manifest, locks, ecosystem in (
        ("Cargo.toml", ("Cargo.lock",), "Rust"),
        ("Gemfile", ("Gemfile.lock",), "Ruby"),
        ("go.mod", ("go.sum",), "Go"),
        ("Pipfile", ("Pipfile.lock",), "Python/Pipenv"),
        ("pyproject.toml", ("poetry.lock", "uv.lock", "requirements.txt"), "Python"),
    ):
        for path in iter_named_files(root, {manifest}):
            present = [name for name in locks if (path.parent / name).exists()]
            if not present:
                add(findings, "medium", f"No recognized {ecosystem} lock/resolution file", path.relative_to(root), f"Expected one of: {', '.join(locks)}")

    counts = {severity: sum(f["severity"] == severity for f in findings) for severity in ("critical", "high", "medium", "low")}
    return {
        "project": str(root),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "manifests": manifests,
        "findings": findings,
        "summary": {"total": len(findings), **counts},
    }


def should_fail(report: dict[str, Any], threshold: str) -> bool:
    if threshold == "none":
        return False
    rank = SEVERITY[threshold]
    return any(report["summary"].get(level, 0) and value >= rank for level, value in SEVERITY.items() if level != "none")


def main() -> int:
    parser = argparse.ArgumentParser(description="Analyze dependency pinning and lock-file hygiene without network access")
    parser.add_argument("project", nargs="?", default=".")
    parser.add_argument("--output", choices=["json", "summary"], default="summary")
    parser.add_argument("--fail-on", choices=list(SEVERITY), default="high")
    args = parser.parse_args()
    root = Path(args.project).resolve()
    if not root.is_dir():
        parser.error(f"Project directory does not exist: {root}")
    report = analyze(root)
    if args.output == "json":
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        s = report["summary"]
        print(f"Dependency Analysis: {root}")
        print(f"Findings: {s['total']} (critical={s['critical']}, high={s['high']}, medium={s['medium']}, low={s['low']})")
        for finding in report["findings"][:20]:
            print(f"[{finding['severity'].upper()}] {finding['file']}: {finding['issue']} - {finding['detail']}")
        if not report["findings"]:
            print("[PASS] No dependency hygiene issues detected.")
    return 1 if should_fail(report, args.fail_on) else 0


if __name__ == "__main__":
    raise SystemExit(main())
