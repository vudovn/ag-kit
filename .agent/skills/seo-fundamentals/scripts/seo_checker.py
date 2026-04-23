#!/usr/bin/env python3
"""
SEO Checker - Search Engine Optimization Audit
Checks public HTML/JSX/TSX/MDX routes for baseline SEO quality.

PURPOSE:
    - Verify route-level metadata signals
    - Check Open Graph coverage for social sharing
    - Validate heading hierarchy
    - Check image accessibility (alt attributes)

WHAT IT CHECKS:
    - HTML files (actual web pages)
    - Next.js App Router route files (`page.*`, `layout.*`)
    - Next.js Pages Router files under `pages/`
    - Route metadata inheritance from ancestor App Router layouts

Usage:
    python seo_checker.py <project_path>
"""
import json
import re
import sys
from datetime import datetime
from pathlib import Path

# Fix Windows console encoding
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


SKIP_DIRS = {
    "node_modules",
    ".next",
    "dist",
    "build",
    ".git",
    ".github",
    "__pycache__",
    ".vscode",
    ".idea",
    "coverage",
    "test",
    "tests",
    "__tests__",
    "spec",
}

SKIP_PATTERNS = [
    "config",
    "setup",
    "util",
    "helper",
    "hook",
    "context",
    "store",
    "service",
    "api",
    "lib",
    "constant",
    "type",
    "interface",
    "mock",
    ".test.",
    ".spec.",
    "_test.",
    "_spec.",
]

NON_ROUTE_DIRS = {
    "components",
    "hooks",
    "lib",
    "utils",
    "providers",
    "contexts",
    "stores",
    "styles",
    "types",
}

ROUTE_CODE_EXTENSIONS = {".js", ".jsx", ".ts", ".tsx", ".md", ".mdx"}
HTML_EXTENSIONS = {".html", ".htm"}
METADATA_FILE_PREFIXES = (
    "opengraph-image.",
    "twitter-image.",
    "robots.",
    "sitemap.",
    "manifest.",
    "favicon.",
    "icon.",
    "apple-icon.",
)


def lower_parts(path: Path) -> list[str]:
    return [part.lower() for part in path.parts]


def should_skip(file_path: Path) -> bool:
    parts = lower_parts(file_path)
    return any(skip in parts for skip in SKIP_DIRS)


def is_next_metadata_file(file_path: Path) -> bool:
    name = file_path.name.lower()
    return any(name.startswith(prefix) for prefix in METADATA_FILE_PREFIXES)


def is_next_app_route(file_path: Path) -> bool:
    if file_path.suffix.lower() not in ROUTE_CODE_EXTENSIONS:
        return False

    parts = lower_parts(file_path)
    if "app" not in parts or any(part in NON_ROUTE_DIRS for part in parts):
        return False

    if any(skip in file_path.name.lower() for skip in SKIP_PATTERNS):
        return False

    return file_path.stem.lower() in {"page", "layout"}


def is_pages_router_route(file_path: Path) -> bool:
    if file_path.suffix.lower() not in ROUTE_CODE_EXTENSIONS:
        return False

    parts = lower_parts(file_path)
    if "pages" not in parts or any(part in NON_ROUTE_DIRS for part in parts):
        return False

    name = file_path.name.lower()
    stem = file_path.stem.lower()
    if any(skip in name for skip in SKIP_PATTERNS):
        return False

    # Skip framework-only files, but audit real routes such as index/about/contact.
    if stem.startswith("_"):
        return False

    return True


def is_route_file(file_path: Path) -> bool:
    if should_skip(file_path):
        return False

    if file_path.suffix.lower() in HTML_EXTENSIONS:
        return True

    return is_next_app_route(file_path) or is_pages_router_route(file_path)


def find_pages(project_path: Path) -> list[Path]:
    patterns = ["**/*.html", "**/*.htm", "**/*.jsx", "**/*.tsx", "**/*.mdx"]
    files = []

    for pattern in patterns:
        for file_path in project_path.glob(pattern):
            if is_route_file(file_path):
                files.append(file_path)

    unique_files = sorted(set(files))
    return unique_files[:100]


def read_content(file_path: Path) -> str:
    return file_path.read_text(encoding="utf-8", errors="ignore")


def extract_metadata_signals(content: str, file_path: Path | None = None) -> dict[str, bool]:
    lower = content.lower()
    path_name = file_path.name.lower() if file_path else ""

    has_metadata_export = bool(
        re.search(
            r"export\s+(?:const\s+metadata\b|(?:async\s+)?function\s+generateMetadata\b)",
            content,
            re.IGNORECASE,
        )
    )

    head_tag = bool(re.search(r"<head(?:\s|>)", content, re.IGNORECASE))
    title_tag = bool(re.search(r"<title\b", content, re.IGNORECASE))
    description_tag = bool(
        re.search(r"<meta[^>]+name=[\"']description[\"']", content, re.IGNORECASE)
    )
    open_graph_tag = bool(re.search(r"property=[\"']og:", content, re.IGNORECASE))

    title_field = bool(re.search(r"\btitle\s*:", content))
    description_field = bool(re.search(r"\bdescription\s*:", content))
    open_graph_field = bool(re.search(r"\bopenGraph\s*:", content))

    return {
        "title": title_tag or (has_metadata_export and title_field) or (head_tag and title_tag),
        "description": description_tag
        or (has_metadata_export and description_field)
        or description_tag,
        "open_graph": open_graph_tag
        or open_graph_field
        or (file_path is not None and path_name.startswith("opengraph-image.")),
    }


def get_app_root(file_path: Path) -> Path | None:
    for candidate in [file_path.parent, *file_path.parents]:
        if candidate.name.lower() == "app":
            return candidate
    return None


def collect_app_route_context_files(file_path: Path) -> list[Path]:
    app_root = get_app_root(file_path)
    if app_root is None:
        return [file_path]

    route_files = [file_path]
    current = file_path.parent

    while True:
        for sibling in current.iterdir():
            if not sibling.is_file():
                continue

            if sibling == file_path:
                continue

            sibling_name = sibling.name.lower()
            if sibling_name.startswith("layout.") or is_next_metadata_file(sibling):
                route_files.append(sibling)

        if current == app_root:
            break

        current = current.parent

    return route_files


def collect_route_metadata(file_path: Path) -> dict[str, bool]:
    metadata = {"title": False, "description": False, "open_graph": False}

    context_files = (
        collect_app_route_context_files(file_path)
        if is_next_app_route(file_path)
        else [file_path]
    )

    for context_file in context_files:
        if is_next_metadata_file(context_file):
            if context_file.name.lower().startswith("opengraph-image."):
                metadata["open_graph"] = True
            continue

        try:
            content = read_content(context_file)
        except Exception:
            continue

        signals = extract_metadata_signals(content, context_file)
        for key, value in signals.items():
            metadata[key] = metadata[key] or value

    return metadata


def check_page(file_path: Path, project_path: Path) -> dict:
    issues = []

    try:
        content = read_content(file_path)
    except Exception as error:
        return {"file": str(file_path.relative_to(project_path)), "issues": [f"Error: {error}"]}

    metadata = collect_route_metadata(file_path)

    if not metadata["title"]:
        issues.append("Missing title metadata")

    if not metadata["description"]:
        issues.append("Missing meta description")

    if not metadata["open_graph"]:
        issues.append("Missing Open Graph metadata")

    h1_matches = re.findall(r"<h1[^>]*>", content, re.IGNORECASE)
    if len(h1_matches) > 1:
        issues.append(f"Multiple H1 tags ({len(h1_matches)})")

    images = re.findall(r"<img[^>]+>", content, re.IGNORECASE)
    for image in images:
        if "alt=" not in image.lower():
            issues.append("Image missing alt attribute")
            break
        if 'alt=""' in image or "alt=''" in image:
            issues.append("Image has empty alt attribute")
            break

    return {
        "file": str(file_path.relative_to(project_path)),
        "issues": issues,
    }


def main():
    project_path = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()

    print(f"\n{'=' * 60}")
    print("  SEO CHECKER - Search Engine Optimization Audit")
    print(f"{'=' * 60}")
    print(f"Project: {project_path}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 60)

    pages = find_pages(project_path)

    if not pages:
        print("\n[!] No page files found.")
        print("    Looking for: HTML, App Router routes, and Pages Router files")
        output = {"script": "seo_checker", "files_checked": 0, "passed": True}
        print("\n" + json.dumps(output, indent=2))
        sys.exit(0)

    print(f"Found {len(pages)} page files to analyze\n")

    all_issues = []
    for file_path in pages:
        result = check_page(file_path, project_path)
        if result["issues"]:
            all_issues.append(result)

    print("=" * 60)
    print("SEO ANALYSIS RESULTS")
    print("=" * 60)

    if all_issues:
        issue_counts = {}
        for item in all_issues:
            for issue in item["issues"]:
                issue_counts[issue] = issue_counts.get(issue, 0) + 1

        print("\nIssue Summary:")
        for issue, count in sorted(issue_counts.items(), key=lambda item: (-item[1], item[0])):
            print(f"  [{count}] {issue}")

        print(f"\nAffected files ({len(all_issues)}):")
        for item in all_issues[:5]:
            print(f"  - {item['file']}")
        if len(all_issues) > 5:
            print(f"  ... and {len(all_issues) - 5} more")
    else:
        print("\n[OK] No SEO issues found!")

    total_issues = sum(len(item["issues"]) for item in all_issues)
    passed = total_issues == 0

    output = {
        "script": "seo_checker",
        "project": str(project_path),
        "files_checked": len(pages),
        "files_with_issues": len(all_issues),
        "issues_found": total_issues,
        "passed": passed,
    }

    print("\n" + json.dumps(output, indent=2))
    sys.exit(0 if passed else 1)


if __name__ == "__main__":
    main()
