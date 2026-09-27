#!/usr/bin/env python3
"""Lightweight static accessibility audit for HTML, JSX, and TSX.

This checker intentionally limits itself to findings that can be inferred from
source. Component names such as ``<Button>`` and ``<InputGroup>`` are not
mistaken for native HTML elements.
"""
from __future__ import annotations

import json
import re
import sys
from datetime import datetime
from pathlib import Path

SKIP_DIRS = {"node_modules", ".next", "dist", "build", ".git", "coverage", "out"}


def find_html_files(project_path: Path) -> list[Path]:
    files = [
        path
        for path in project_path.rglob("*")
        if path.is_file()
        and path.suffix.lower() in {".html", ".jsx", ".tsx"}
        and not any(part in SKIP_DIRS for part in path.parts)
    ]
    return sorted(files)


def _opening_tags(content: str, tag: str) -> list[str]:
    return re.findall(rf"<{tag}\b[^>]*>", content, re.DOTALL)


def check_accessibility(file_path: Path) -> list[str]:
    issues: list[str] = []
    content = file_path.read_text("utf-8", errors="ignore")
    lowered = content.lower()

    for input_tag in _opening_tags(content, "input"):
        normalized = input_tag.lower()
        if re.search(r'type\s*=\s*["\']hidden["\']', normalized):
            continue
        accessible = any(
            token in normalized
            for token in ("aria-label=", "aria-labelledby=", "id=", "{...", "name=")
        )
        if not accessible:
            issues.append("Native input without id, name, aria-label, or aria-labelledby")
            break

    for match in re.finditer(r"<button\b([^>]*)>(.*?)</button\s*>", content, re.DOTALL):
        attributes, body = match.groups()
        if "aria-label=" in attributes.lower() or "aria-labelledby=" in attributes.lower():
            continue
        text = re.sub(r"<[^>]+>|\{[^}]+\}", "", body).strip()
        has_child_content = bool(re.search(r"<[A-Za-z]", body) or re.search(r"\{[^}]+\}", body))
        if not text and not has_child_content:
            issues.append("Native button without accessible text or label")
            break

    html_tags = _opening_tags(content, "html")
    if html_tags and not any(re.search(r"\blang\s*=", tag, re.IGNORECASE) for tag in html_tags):
        issues.append("Missing lang attribute on <html>")

    if _opening_tags(content, "body"):
        has_skip_link = bool(
            re.search(r"href\s*=\s*[\"']#(?:main|main-content)[\"']", content, re.IGNORECASE)
        )
        if not has_skip_link:
            issues.append("Document body is missing a skip-to-main-content link")

    non_interactive_click = re.finditer(
        r"<(div|span|li|section|article)\b([^>]*)\bonClick\s*=([^>]*)>",
        content,
        re.DOTALL,
    )
    for _, before, after in non_interactive_click:
        attributes = f"{before} {after}".lower()
        keyboard_enabled = "onkeydown=" in attributes or "onkeyup=" in attributes
        semantic_button = 'role="button"' in attributes or "role='button'" in attributes
        focusable = "tabindex=" in attributes
        if not (keyboard_enabled and semantic_button and focusable):
            issues.append("Non-interactive element with onClick lacks role, tabIndex, or keyboard handler")
            break

    positive_tabindex = re.findall(r"tabIndex\s*=\s*[\"']([1-9]\d*)[\"']", content, re.IGNORECASE)
    if positive_tabindex:
        issues.append("Avoid positive tabIndex values")

    for media_tag in re.findall(r"<(?:audio|video)\b[^>]*>", content, re.DOTALL):
        if "autoplay" in media_tag.lower() and "muted" not in media_tag.lower():
            issues.append("Autoplay media should be muted")
            break

    for div_tag in re.findall(r"<div\b[^>]*role\s*=\s*[\"']button[\"'][^>]*>", content, re.DOTALL):
        lowered_tag = div_tag.lower()
        if "tabindex=" not in lowered_tag or ("onkeydown=" not in lowered_tag and "onkeyup=" not in lowered_tag):
            issues.append("role='button' requires tabIndex and a keyboard handler")
            break

    return issues


def main() -> int:
    project_path = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    if not project_path.is_dir():
        print(json.dumps({"error": f"Directory not found: {project_path}"}))
        return 2

    print(f"\n{'=' * 60}\n[ACCESSIBILITY CHECKER] WCAG Static Audit\n{'=' * 60}")
    print(f"Project: {project_path}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n" + "-" * 60)

    files = find_html_files(project_path)
    print(f"Found {len(files)} HTML/JSX/TSX files")
    all_issues = []
    for file_path in files:
        issues = check_accessibility(file_path)
        if issues:
            all_issues.append({"file": str(file_path.relative_to(project_path)), "issues": issues})

    print("\n" + "=" * 60 + "\nACCESSIBILITY ISSUES\n" + "=" * 60)
    if all_issues:
        for item in all_issues[:20]:
            print(f"\n{item['file']}:")
            for issue in item["issues"]:
                print(f"  - {issue}")
    else:
        print("No statically detectable accessibility issues found.")

    total_issues = sum(len(item["issues"]) for item in all_issues)
    output = {
        "script": "accessibility_checker",
        "project": str(project_path),
        "files_checked": len(files),
        "files_with_issues": len(all_issues),
        "issues_found": total_issues,
        "passed": total_issues == 0,
    }
    print("\n" + json.dumps(output, indent=2))
    return 0 if output["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
