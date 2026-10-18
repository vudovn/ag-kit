#!/usr/bin/env python3
"""Analyze built JavaScript/CSS asset sizes without external dependencies."""
from __future__ import annotations

import argparse
import gzip
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SKIP_DIRS = {"node_modules", ".git", ".agents", ".agent", ".venv", "venv"}
BUILD_ROOTS = (".next/static", "dist", "build/static", "build/assets", "out/_next/static")
SEVERITY = {"none": 99, "low": 1, "medium": 2, "high": 3, "critical": 4}


def human_bytes(value: int) -> str:
    units = ("B", "KiB", "MiB", "GiB")
    size = float(value)
    for unit in units:
        if size < 1024 or unit == units[-1]:
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{value} B"


def analyze(root: Path, file_warn_kib: int, file_fail_kib: int, total_fail_kib: int) -> dict[str, Any]:
    assets: list[dict[str, Any]] = []
    seen: set[Path] = set()
    for relative in BUILD_ROOTS:
        build_root = root / relative
        if not build_root.is_dir():
            continue
        for path in build_root.rglob("*"):
            if not path.is_file() or path.suffix.lower() not in {".js", ".mjs", ".css"}:
                continue
            resolved = path.resolve()
            if resolved in seen:
                continue
            seen.add(resolved)
            try:
                data = path.read_bytes()
            except OSError:
                continue
            assets.append({
                "file": path.relative_to(root).as_posix(),
                "type": path.suffix.lower().lstrip("."),
                "bytes": len(data),
                "gzip_bytes": len(gzip.compress(data, compresslevel=6)),
            })

    findings: list[dict[str, Any]] = []
    for asset in assets:
        kib = asset["bytes"] / 1024
        if kib >= file_fail_kib:
            findings.append({"severity": "high", "issue": "Oversized asset", "file": asset["file"], "size": human_bytes(asset["bytes"])})
        elif kib >= file_warn_kib:
            findings.append({"severity": "medium", "issue": "Large asset", "file": asset["file"], "size": human_bytes(asset["bytes"])})

    js_total = sum(a["bytes"] for a in assets if a["type"] in {"js", "mjs"})
    if js_total / 1024 >= total_fail_kib:
        findings.append({"severity": "high", "issue": "Large total JavaScript payload", "file": "<all JS assets>", "size": human_bytes(js_total)})

    assets.sort(key=lambda item: item["bytes"], reverse=True)
    counts = {severity: sum(f["severity"] == severity for f in findings) for severity in ("critical", "high", "medium", "low")}
    return {
        "project": str(root),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "build_roots_checked": [name for name in BUILD_ROOTS if (root / name).is_dir()],
        "asset_count": len(assets),
        "totals": {
            "bytes": sum(a["bytes"] for a in assets),
            "gzip_bytes": sum(a["gzip_bytes"] for a in assets),
            "javascript_bytes": js_total,
            "css_bytes": sum(a["bytes"] for a in assets if a["type"] == "css"),
        },
        "largest_assets": assets[:30],
        "findings": findings,
        "summary": {"total": len(findings), **counts},
    }


def should_fail(report: dict[str, Any], threshold: str) -> bool:
    if threshold == "none":
        return False
    rank = SEVERITY[threshold]
    return any(report["summary"].get(level, 0) and value >= rank for level, value in SEVERITY.items() if level != "none")


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit generated JavaScript and CSS bundle sizes")
    parser.add_argument("project", nargs="?", default=".")
    parser.add_argument("--output", choices=["json", "summary"], default="summary")
    parser.add_argument("--file-warn-kib", type=int, default=250)
    parser.add_argument("--file-fail-kib", type=int, default=750)
    parser.add_argument("--total-js-fail-kib", type=int, default=2048)
    parser.add_argument("--fail-on", choices=list(SEVERITY), default="high")
    args = parser.parse_args()
    root = Path(args.project).resolve()
    if not root.is_dir():
        parser.error(f"Project directory does not exist: {root}")
    report = analyze(root, args.file_warn_kib, args.file_fail_kib, args.total_js_fail_kib)
    if args.output == "json":
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        totals = report["totals"]
        print(f"Bundle Analysis: {root}")
        if not report["build_roots_checked"]:
            print("[SKIP] No supported build output found. Build the project first for meaningful results.")
        else:
            print(f"Assets: {report['asset_count']} | Raw: {human_bytes(totals['bytes'])} | Gzip: {human_bytes(totals['gzip_bytes'])}")
            for asset in report["largest_assets"][:10]:
                print(f"{human_bytes(asset['bytes']):>10} ({human_bytes(asset['gzip_bytes'])} gzip)  {asset['file']}")
            for finding in report["findings"]:
                print(f"[{finding['severity'].upper()}] {finding['issue']}: {finding['file']} ({finding['size']})")
    return 1 if should_fail(report, args.fail_on) else 0


if __name__ == "__main__":
    raise SystemExit(main())
