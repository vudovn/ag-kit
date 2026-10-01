#!/usr/bin/env python3
"""Audit locale completeness and likely user-facing hard-coded strings."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

SKIP_DIRS = {"node_modules", ".git", ".agents", ".agent", "dist", "build", "__pycache__", ".venv", "venv", ".next", "tests", "test", "spec", "specs"}
CODE_TYPES = {".tsx": "jsx", ".jsx": "jsx", ".ts": "jsx", ".js": "jsx", ".vue": "vue", ".py": "python"}
I18N_PATTERNS = (
    re.compile(r"\buseTranslation\s*\("),
    re.compile(r"\buseTranslations\s*\("),
    re.compile(r"(?<![\w$])t\s*\(\s*[\"']"),
    re.compile(r"\$t\s*\("),
    re.compile(r"\bgettext\s*\("),
    re.compile(r"(?<!\w)_\s*\(\s*[\"']"),
    re.compile(r"\bFormattedMessage\b"),
    re.compile(r"\bi18n\."),
)
HARDCODED_PATTERNS = {
    "jsx": (
        re.compile(r">\s*([A-Z][A-Za-z][A-Za-z\s!?.,'-]{2,80})\s*</"),
        re.compile(r"(?:title|placeholder|label|alt|aria-label)=[\"']([A-Z][A-Za-z\s!?.,'-]{2,80})[\"']"),
    ),
    "vue": (
        re.compile(r">\s*([A-Z][A-Za-z][A-Za-z\s!?.,'-]{2,80})\s*</"),
        re.compile(r"(?:title|placeholder|label|alt|aria-label)=[\"']([A-Z][A-Za-z\s!?.,'-]{2,80})[\"']"),
    ),
    "python": (
        re.compile(r"\bflash\s*\(\s*[\"']([A-Z][^\"']{4,100})[\"']"),
    ),
}


def is_skipped(path: Path, root: Path) -> bool:
    try:
        rel = path.relative_to(root)
    except ValueError:
        rel = path
    return any(part in SKIP_DIRS for part in rel.parts)


def find_locale_files(root: Path) -> list[Path]:
    patterns = (
        "**/locales/**/*.json", "**/translations/**/*.json", "**/lang/**/*.json",
        "**/i18n/**/*.json", "**/messages/*.json", "**/*.po",
    )
    found: set[Path] = set()
    for pattern in patterns:
        for path in root.glob(pattern):
            if path.is_file() and not is_skipped(path, root):
                found.add(path)
    return sorted(found)


def flatten_keys(value: Any, prefix: str = "") -> set[str]:
    keys: set[str] = set()
    if not isinstance(value, dict):
        return keys
    for key, child in value.items():
        name = f"{prefix}.{key}" if prefix else str(key)
        if isinstance(child, dict):
            keys.update(flatten_keys(child, name))
        else:
            keys.add(name)
    return keys


def check_locale_completeness(locale_files: list[Path], root: Path) -> dict[str, Any]:
    if not locale_files:
        return {"status": "not_applicable", "files": 0, "languages": [], "issues": [], "notes": ["No locale files found."]}

    locales: dict[str, dict[str, set[str]]] = {}
    issues: list[dict[str, str]] = []
    for path in locale_files:
        if path.suffix == ".po":
            continue
        try:
            content = json.loads(path.read_text("utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            issues.append({"severity": "high", "file": path.relative_to(root).as_posix(), "issue": f"Invalid locale JSON: {exc}"})
            continue
        language = path.parent.name
        locales.setdefault(language, {})[path.stem] = flatten_keys(content)

    languages = sorted(locales)
    if len(languages) >= 2:
        base = languages[0]
        namespaces = set().union(*(set(locales[lang]) for lang in languages))
        for namespace in sorted(namespaces):
            base_keys = locales[base].get(namespace, set())
            for language in languages[1:]:
                keys = locales[language].get(namespace, set())
                missing = sorted(base_keys - keys)
                extra = sorted(keys - base_keys)
                if missing:
                    issues.append({"severity": "high", "file": f"{language}/{namespace}", "issue": f"Missing {len(missing)} key(s): {', '.join(missing[:8])}"})
                if extra:
                    issues.append({"severity": "medium", "file": f"{language}/{namespace}", "issue": f"Has {len(extra)} extra key(s)"})

    return {"status": "checked", "files": len(locale_files), "languages": languages, "issues": issues, "notes": []}


def iter_code_files(root: Path):
    for path in root.rglob("*"):
        if path.is_file() and path.suffix.lower() in CODE_TYPES and not is_skipped(path, root):
            yield path


def project_uses_i18n(root: Path, code_files: list[Path], locale_files: list[Path]) -> bool:
    if locale_files:
        return True
    package = root / "package.json"
    if package.is_file():
        try:
            text = package.read_text("utf-8").lower()
            if any(name in text for name in ("i18next", "next-intl", "react-intl", "vue-i18n", "@lingui")):
                return True
        except OSError:
            pass
    for path in code_files[:200]:
        try:
            content = path.read_text("utf-8", errors="ignore")
        except OSError:
            continue
        if any(pattern.search(content) for pattern in I18N_PATTERNS):
            return True
    return False


def check_hardcoded_strings(root: Path, code_files: list[Path], enforce: bool) -> dict[str, Any]:
    if not enforce:
        return {"status": "not_applicable", "files_checked": 0, "files_using_i18n": 0, "issues": [], "notes": ["No i18n framework or locale files detected."]}

    issues: list[dict[str, Any]] = []
    files_using_i18n = 0
    checked = 0
    for path in code_files[:500]:
        try:
            content = path.read_text("utf-8", errors="ignore")
        except OSError:
            continue
        checked += 1
        has_i18n = any(pattern.search(content) for pattern in I18N_PATTERNS)
        if has_i18n:
            files_using_i18n += 1
        if has_i18n:
            continue
        file_type = CODE_TYPES[path.suffix.lower()]
        for pattern in HARDCODED_PATTERNS[file_type]:
            for match in pattern.finditer(content):
                value = match.group(1).strip()
                if value.lower().startswith(("http", "error", "warning")):
                    continue
                line = content.count("\n", 0, match.start()) + 1
                issues.append({
                    "severity": "medium",
                    "file": path.relative_to(root).as_posix(),
                    "line": line,
                    "issue": "Likely user-facing hard-coded string",
                    "text": value[:100],
                })
                if len(issues) >= 100:
                    break
            if len(issues) >= 100:
                break
        if len(issues) >= 100:
            break
    return {"status": "checked", "files_checked": checked, "files_using_i18n": files_using_i18n, "issues": issues, "notes": []}


def audit(root: Path, strict: bool = False) -> dict[str, Any]:
    locale_files = find_locale_files(root)
    code_files = list(iter_code_files(root))
    enforce = strict or project_uses_i18n(root, code_files, locale_files)
    locale = check_locale_completeness(locale_files, root)
    code = check_hardcoded_strings(root, code_files, enforce)
    findings = locale["issues"] + code["issues"]
    high = sum(item["severity"] == "high" for item in findings)
    medium = sum(item["severity"] == "medium" for item in findings)
    return {
        "project": str(root),
        "applicable": enforce,
        "locale_check": locale,
        "code_check": code,
        "summary": {"total": len(findings), "high": high, "medium": medium, "passed": high == 0},
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Check locale completeness and likely hard-coded UI strings")
    parser.add_argument("project", nargs="?", default=".")
    parser.add_argument("--strict", action="store_true", help="Scan hard-coded strings even when no i18n setup is detected")
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()
    root = Path(args.project).resolve()
    if not root.is_dir():
        parser.error(f"Project directory does not exist: {root}")
    report = audit(root, args.strict)
    if args.as_json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(f"i18n Audit: {root}")
        if not report["applicable"]:
            print("[SKIP] No i18n framework or locale files detected.")
        else:
            locale = report["locale_check"]
            code = report["code_check"]
            print(f"Locale files: {locale['files']} | Languages: {', '.join(locale['languages']) or 'unknown'}")
            print(f"Code files checked: {code['files_checked']} | Files using i18n: {code['files_using_i18n']}")
            for item in (locale["issues"] + code["issues"])[:30]:
                line = f":{item['line']}" if "line" in item else ""
                print(f"[{item['severity'].upper()}] {item['file']}{line} - {item['issue']}")
            print("[PASS] No blocking i18n issues." if report["summary"]["passed"] else "[FAIL] Blocking i18n issues found.")
    return 0 if report["summary"]["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
