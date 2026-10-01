#!/usr/bin/env python3
"""AG Kit security scanner.

Performs lightweight, local checks for dependency hygiene, hard-coded secrets,
dangerous code patterns, and common security misconfiguration.

The scanner is intentionally dependency-free. It is a guardrail, not a
replacement for a full SAST/SCA product.
"""
from __future__ import annotations

import argparse
import io
import json
import os
import re
import subprocess
import sys
import tokenize
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except AttributeError:
    pass

SECRET_PATTERNS: tuple[tuple[str, str, str], ...] = (
    (r"api[_-]?key\s*[=:]\s*[\"'][^\"']{10,}[\"']", "API Key", "high"),
    (r"token\s*[=:]\s*[\"'][^\"']{10,}[\"']", "Token", "high"),
    (r"bearer\s+[a-zA-Z0-9\-_.]{16,}", "Bearer Token", "critical"),
    (r"AKIA[0-9A-Z]{16}", "AWS Access Key", "critical"),
    (r"aws[_-]?secret[_-]?access[_-]?key\s*[=:]\s*[\"'][^\"']+[\"']", "AWS Secret", "critical"),
    (r"AZURE[_-]?[A-Z_]+\s*[=:]\s*[\"'][^\"']+[\"']", "Azure Credential", "critical"),
    (r"GOOGLE[_-]?[A-Z_]+\s*[=:]\s*[\"'][^\"']+[\"']", "GCP Credential", "critical"),
    (r"password\s*[=:]\s*[\"'][^\"']{6,}[\"']", "Password", "high"),
    (r"(?:mongodb|postgres(?:ql)?|mysql|redis):\/\/[^\s\"']+", "Database Connection String", "critical"),
    (r"-----BEGIN\s+(?:RSA|PRIVATE|EC|OPENSSH)\s+KEY-----", "Private Key", "critical"),
    (r"ssh-rsa\s+[A-Za-z0-9+/]{80,}", "SSH Key", "critical"),
    (r"eyJ[A-Za-z0-9_-]+\.eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+", "JWT Token", "high"),
)

DANGEROUS_PATTERNS: tuple[tuple[str, str, str, str], ...] = (
    (r"\beval\s*\(", "eval() usage", "critical", "Code injection risk"),
    (r"\bexec\s*\(", "exec() usage", "critical", "Code injection risk"),
    (r"new\s+Function\s*\(", "Function constructor", "high", "Code injection risk"),
    (r"child_process\.exec\s*\(", "child_process.exec", "high", "Command injection risk"),
    (r"subprocess\.(?:call|run|Popen)\s*\([^\n]*shell\s*=\s*True", "subprocess shell=True", "high", "Command injection risk"),
    (r"dangerouslySetInnerHTML", "dangerouslySetInnerHTML", "high", "XSS risk"),
    (r"\.innerHTML\s*=", "innerHTML assignment", "medium", "XSS risk"),
    (r"document\.write\s*\(", "document.write", "medium", "XSS risk"),
    (r"[\"'][^\"']*\+\s*[a-zA-Z_]\w*\s*\+\s*[\"'][^\n]*(?:SELECT|INSERT|UPDATE|DELETE)", "SQL string concatenation", "critical", "SQL injection risk"),
    (r"f[\"'][^\"']*(?:SELECT|INSERT|UPDATE|DELETE)[^\"']*\{", "SQL f-string", "critical", "SQL injection risk"),
    (r"verify\s*=\s*False", "SSL verification disabled", "high", "MITM risk"),
    (r"--insecure\b", "Insecure flag", "medium", "Security disabled"),
    (r"disable[_-]?ssl", "SSL disabled", "high", "MITM risk"),
    (r"pickle\.loads?\s*\(", "pickle usage", "high", "Unsafe deserialization risk"),
    (r"yaml\.load\s*\(", "yaml.load usage", "high", "Unsafe deserialization risk"),
)

SEVERITY_RANK = {"none": 99, "low": 1, "medium": 2, "high": 3, "critical": 4}
SKIP_DIRS = {
    "node_modules", ".git", "dist", "build", "__pycache__", ".venv", "venv",
    ".next", ".agents", ".agent", ".tox", ".mypy_cache", ".pytest_cache",
    "coverage", ".coverage", "vendor",
}
CODE_EXTENSIONS = {".js", ".mjs", ".cjs", ".ts", ".tsx", ".jsx", ".py", ".go", ".java", ".rb", ".php"}
CONFIG_EXTENSIONS = {".json", ".yaml", ".yml", ".toml", ".env", ".ini", ".conf"}
PLACEHOLDER_MARKERS = (
    "YOUR_", "EXAMPLE", "CHANGEME", "CHANGE_ME", "REPLACE_ME", "PLACEHOLDER",
    "DUMMY", "SAMPLE", "FAKE_", "TEST_TOKEN", "TEST_KEY",
)
SELF_PATH = Path(__file__).resolve()


def _new_result(tool: str, status: str) -> dict[str, Any]:
    return {"tool": tool, "findings": [], "status": status, "scanned_files": 0}


def _iter_files(project: Path, extensions: set[str]):
    for root, dirs, files in os.walk(project):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for filename in files:
            path = Path(root) / filename
            if path.resolve() == SELF_PATH:
                continue
            if path.suffix.lower() in extensions or filename.startswith(".env"):
                yield path


def _relative(path: Path, project: Path) -> str:
    try:
        return path.relative_to(project).as_posix()
    except ValueError:
        return path.as_posix()


def _is_placeholder(value: str) -> bool:
    upper = value.upper()
    return any(marker in upper for marker in PLACEHOLDER_MARKERS)


def _redact(value: str) -> str:
    value = value.strip().replace("\n", " ")
    if len(value) <= 12:
        return "<redacted>"
    return f"{value[:4]}…{value[-4:]}"


def _python_code_without_strings(text: str) -> list[str]:
    lines = [list(line) for line in text.splitlines(keepends=True)]
    try:
        tokens = tokenize.generate_tokens(io.StringIO(text).readline)
        for tok in tokens:
            if tok.type not in {tokenize.STRING, tokenize.COMMENT}:
                continue
            (srow, scol), (erow, ecol) = tok.start, tok.end
            for row in range(srow, erow + 1):
                if not (1 <= row <= len(lines)):
                    continue
                start = scol if row == srow else 0
                end = ecol if row == erow else len(lines[row - 1])
                for col in range(start, min(end, len(lines[row - 1]))):
                    if lines[row - 1][col] not in "\r\n":
                        lines[row - 1][col] = " "
    except (tokenize.TokenError, IndentationError):
        pass
    return ["".join(line) for line in lines]


def _generic_code_without_strings(text: str) -> list[str]:
    cleaned = re.sub(r"/\*.*?\*/", lambda m: "\n" * m.group(0).count("\n"), text, flags=re.DOTALL)
    output: list[str] = []
    string_re = re.compile(r"(?:\"(?:\\.|[^\"\\])*\"|'(?:\\.|[^'\\])*'|`(?:\\.|[^`\\])*`)")
    for line in cleaned.splitlines(keepends=True):
        no_comment = re.sub(r"//.*$", "", line)
        output.append(string_re.sub("", no_comment))
    return output


def scan_dependencies(project_path: str) -> dict[str, Any]:
    project = Path(project_path)
    result = _new_result("dependency_scanner", "[OK] Supply chain checks passed")

    ecosystems = {
        "node": (["package.json"], ["package-lock.json", "npm-shrinkwrap.json", "yarn.lock", "pnpm-lock.yaml", "bun.lock", "bun.lockb"]),
        "python": (["pyproject.toml", "setup.py", "setup.cfg", "requirements.in"], ["poetry.lock", "Pipfile.lock", "uv.lock", "requirements.txt"]),
        "ruby": (["Gemfile"], ["Gemfile.lock"]),
        "rust": (["Cargo.toml"], ["Cargo.lock"]),
        "go": (["go.mod"], ["go.sum"]),
    }
    for name, (manifests, locks) in ecosystems.items():
        if any((project / f).exists() for f in manifests) and not any((project / f).exists() for f in locks):
            result["findings"].append({
                "type": "Missing lock file",
                "severity": "high",
                "ecosystem": name,
                "message": f"{name}: manifest found but no supported lock file is present.",
            })

    if (project / "package.json").exists():
        try:
            proc = subprocess.run(
                ["npm", "audit", "--json"], cwd=project, capture_output=True,
                text=True, timeout=90, check=False,
            )
            raw = proc.stdout.strip() or proc.stderr.strip()
            if raw:
                data = json.loads(raw)
                metadata = data.get("metadata", {}).get("vulnerabilities", {})
                counts = {key: int(metadata.get(key, 0) or 0) for key in ("critical", "high", "moderate", "low")}
                result["npm_audit"] = counts
                for severity in ("critical", "high"):
                    if counts[severity]:
                        result["findings"].append({
                            "type": "npm audit", "severity": severity,
                            "message": f"{counts[severity]} {severity} dependency vulnerabilities.",
                        })
        except FileNotFoundError:
            result["notes"] = ["npm is unavailable; npm audit was skipped."]
        except subprocess.TimeoutExpired:
            result["notes"] = ["npm audit timed out."]
        except (json.JSONDecodeError, OSError) as exc:
            result["notes"] = [f"npm audit output could not be parsed: {exc}"]

    if result["findings"]:
        result["status"] = "[!] Dependency risks found"
    return result


def scan_secrets(project_path: str) -> dict[str, Any]:
    project = Path(project_path).resolve()
    result = _new_result("secret_scanner", "[OK] No secrets detected")
    counts = {"critical": 0, "high": 0, "medium": 0, "low": 0}

    for path in _iter_files(project, CODE_EXTENSIONS | CONFIG_EXTENSIONS):
        result["scanned_files"] += 1
        try:
            content = path.read_text("utf-8", errors="ignore")
        except OSError:
            continue
        for pattern, secret_type, severity in SECRET_PATTERNS:
            for match in re.finditer(pattern, content, re.IGNORECASE):
                matched = match.group(0)
                line = content.count("\n", 0, match.start()) + 1
                source_line = content.splitlines()[line - 1] if content.splitlines() else ""
                if _is_placeholder(matched) or "agkit: allow-secret" in source_line.lower() or "# nosec" in source_line.lower():
                    continue
                result["findings"].append({
                    "file": _relative(path, project), "line": line, "type": secret_type,
                    "severity": severity, "preview": _redact(matched),
                })
                counts[severity] += 1

    result["by_severity"] = counts
    if counts["critical"]:
        result["status"] = "[!!] CRITICAL: Potential secrets exposed"
    elif counts["high"]:
        result["status"] = "[!] HIGH: Potential secrets found"
    elif sum(counts.values()):
        result["status"] = "[?] Potential secrets need review"
    return result


def scan_code_patterns(project_path: str) -> dict[str, Any]:
    project = Path(project_path).resolve()
    result = _new_result("pattern_scanner", "[OK] No dangerous patterns")
    by_category: dict[str, int] = {}

    for path in _iter_files(project, CODE_EXTENSIONS):
        result["scanned_files"] += 1
        try:
            text = path.read_text("utf-8", errors="ignore")
        except OSError:
            continue
        lines = _python_code_without_strings(text) if path.suffix.lower() == ".py" else _generic_code_without_strings(text)
        original = text.splitlines()
        for line_number, code_line in enumerate(lines, 1):
            for pattern, name, severity, category in DANGEROUS_PATTERNS:
                if re.search(pattern, code_line, re.IGNORECASE):
                    snippet = original[line_number - 1].strip()[:120] if line_number <= len(original) else ""
                    result["findings"].append({
                        "file": _relative(path, project), "line": line_number,
                        "pattern": name, "severity": severity, "category": category,
                        "snippet": snippet,
                    })
                    by_category[category] = by_category.get(category, 0) + 1
    result["by_category"] = by_category
    critical = sum(f["severity"] == "critical" for f in result["findings"])
    high = sum(f["severity"] == "high" for f in result["findings"])
    if critical:
        result["status"] = f"[!!] CRITICAL: {critical} dangerous pattern(s)"
    elif high:
        result["status"] = f"[!] HIGH: {high} risky pattern(s)"
    elif result["findings"]:
        result["status"] = "[?] Patterns need review"
    return result


def _looks_like_web_project(project: Path) -> bool:
    indicators = (
        "package.json", "next.config.js", "next.config.mjs", "vite.config.ts",
        "vite.config.js", "nuxt.config.ts", "angular.json", "nginx.conf",
    )
    return any((project / name).exists() for name in indicators)


def scan_configuration(project_path: str) -> dict[str, Any]:
    project = Path(project_path).resolve()
    result = _new_result("config_scanner", "[OK] Configuration checks passed")
    checks: dict[str, Any] = {}
    patterns = (
        (r'"DEBUG"\s*:\s*true', "Debug mode enabled", "high"),
        (r"\bdebug\s*=\s*True", "Debug mode enabled", "high"),
        (r'"CORS_ALLOW_ALL"\s*:\s*true', "CORS allows every origin", "high"),
        (r'Access-Control-Allow-Origin[^\n]*[\"\']\*[\"\']', "CORS wildcard", "high"),
        (r"allowCredentials[^\n]*true[^\n]*origin[^\n]*\*", "Credentials with wildcard CORS", "critical"),
    )

    extra_names = {"next.config.js", "next.config.mjs", "next.config.ts", "webpack.config.js", ".eslintrc.js", "nginx.conf"}
    header_files = {"next.config.js", "next.config.mjs", "next.config.ts", "middleware.ts", "middleware.js", "nginx.conf", "vercel.json"}
    header_pattern = re.compile(
        r"Content-Security-Policy|Strict-Transport-Security|X-Frame-Options|frame-ancestors|Referrer-Policy",
        re.IGNORECASE,
    )
    has_security_headers = False
    for root, dirs, files in os.walk(project):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for filename in files:
            path = Path(root) / filename
            if path.resolve() == SELF_PATH:
                continue
            if path.suffix.lower() not in CONFIG_EXTENSIONS and filename not in extra_names and not filename.startswith(".env"):
                continue
            result["scanned_files"] += 1
            try:
                content = path.read_text("utf-8", errors="ignore")
            except OSError:
                continue
            if filename in header_files and header_pattern.search(content):
                has_security_headers = True
            for pattern, issue, severity in patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    result["findings"].append({"file": _relative(path, project), "issue": issue, "severity": severity})

    if _looks_like_web_project(project):
        checks["security_headers_config"] = has_security_headers
        if not checks["security_headers_config"]:
            result["findings"].append({
                "issue": "No obvious security-header configuration found",
                "severity": "medium",
                "recommendation": "Configure CSP, HSTS, frame-ancestors/X-Frame-Options, and Referrer-Policy as appropriate.",
            })
    else:
        checks["security_headers_config"] = "not_applicable"
    result["checks"] = checks

    if any(f["severity"] == "critical" for f in result["findings"]):
        result["status"] = "[!!] CRITICAL: Configuration issues"
    elif any(f["severity"] == "high" for f in result["findings"]):
        result["status"] = "[!] HIGH: Configuration review needed"
    elif result["findings"]:
        result["status"] = "[?] Configuration review recommended"
    return result


def run_full_scan(project_path: str, scan_type: str = "all") -> dict[str, Any]:
    project = str(Path(project_path).resolve())
    report: dict[str, Any] = {
        "project": project,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "scan_type": scan_type,
        "scans": {},
        "summary": {"total_findings": 0, "critical": 0, "high": 0, "medium": 0, "low": 0, "overall_status": "[OK] SECURE"},
    }
    scanners: dict[str, tuple[str, Callable[[str], dict[str, Any]]]] = {
        "deps": ("dependencies", scan_dependencies),
        "secrets": ("secrets", scan_secrets),
        "patterns": ("code_patterns", scan_code_patterns),
        "config": ("configuration", scan_configuration),
    }
    for key, (name, scanner) in scanners.items():
        if scan_type not in {"all", key}:
            continue
        scan_result = scanner(project)
        report["scans"][name] = scan_result
        findings = scan_result.get("findings", [])
        report["summary"]["total_findings"] += len(findings)
        for finding in findings:
            severity = finding.get("severity", "low")
            if severity in {"critical", "high", "medium", "low"}:
                report["summary"][severity] += 1

    summary = report["summary"]
    if summary["critical"]:
        summary["overall_status"] = "[!!] CRITICAL ISSUES FOUND"
    elif summary["high"]:
        summary["overall_status"] = "[!] HIGH RISK ISSUES"
    elif summary["total_findings"]:
        summary["overall_status"] = "[?] REVIEW RECOMMENDED"
    return report


def _should_fail(report: dict[str, Any], threshold: str) -> bool:
    if threshold == "none":
        return False
    required_rank = SEVERITY_RANK[threshold]
    return any(
        report["summary"].get(severity, 0) > 0 and rank >= required_rank
        for severity, rank in SEVERITY_RANK.items()
        if severity != "none"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Run lightweight AG Kit security checks")
    parser.add_argument("project_path", nargs="?", default=".", help="Project directory to scan")
    parser.add_argument("--scan-type", choices=["all", "deps", "secrets", "patterns", "config"], default="all")
    parser.add_argument("--output", choices=["json", "summary"], default="json")
    parser.add_argument(
        "--fail-on", choices=["none", "low", "medium", "high", "critical"], default="high",
        help="Return exit code 1 when a finding at or above this severity exists (default: high)",
    )
    args = parser.parse_args()
    project = Path(args.project_path).resolve()
    if not project.is_dir():
        print(json.dumps({"error": f"Directory not found: {project}"}))
        return 2

    report = run_full_scan(str(project), args.scan_type)
    if args.output == "summary":
        summary = report["summary"]
        print(f"\n{'=' * 60}\nSecurity Scan: {report['project']}\n{'=' * 60}")
        print(f"Status: {summary['overall_status']}")
        print(f"Total Findings: {summary['total_findings']}")
        print(f"  Critical: {summary['critical']}\n  High: {summary['high']}\n  Medium: {summary['medium']}\n  Low: {summary['low']}")
        print("=" * 60)
        for name, scan in report["scans"].items():
            print(f"\n{name.upper()}: {scan['status']}")
            for finding in scan.get("findings", [])[:10]:
                print(f"  - {finding}")
    else:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    return 1 if _should_fail(report, args.fail_on) else 0


if __name__ == "__main__":
    raise SystemExit(main())
