#!/usr/bin/env python3
"""
GEO Checker - Generative Engine Optimization Audit
Checks PUBLIC WEB CONTENT for AI citation readiness.

PURPOSE:
    - Analyze pages that will be INDEXED by AI engines (ChatGPT, Perplexity, etc.)
    - Check for structured data, author info, dates, FAQ sections
    - Help content rank in AI-generated answers

WHAT IT CHECKS:
    - HTML files (actual web pages)
    - JSX/TSX files (React page components)
    - NOT markdown files (those are developer docs, not public content)

Usage:
    python geo_checker.py <project_path>
"""
from __future__ import annotations
import sys
import re
import json
from pathlib import Path

# Fix Windows console encoding
try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')
except AttributeError:
    pass


# Directories that never represent public source content.
SKIP_DIRS = {
    "node_modules", ".next", "dist", "build", ".git", ".github",
    ".agents", "__pycache__", ".vscode", ".idea", "coverage",
    "test", "tests", "__tests__", "spec", "public", "components",
}

PAGE_SUFFIXES = {".html", ".htm", ".jsx", ".tsx"}
ARTICLE_SEGMENTS = {"blog", "blogs", "article", "articles", "post", "posts", "news"}


def _lower_parts(file_path: Path) -> list[str]:
    return [part.lower() for part in file_path.parts]


def is_page_file(file_path: Path) -> bool:
    """Return True only for route entry points, not layouts or components."""
    if file_path.suffix.lower() not in PAGE_SUFFIXES:
        return False
    parts = _lower_parts(file_path)
    if any(part in SKIP_DIRS for part in parts):
        return False
    if file_path.suffix.lower() in {".html", ".htm"}:
        return True

    name = file_path.stem.lower()
    if name.endswith((".test", ".spec")) or name.startswith(("test_", "spec_")):
        return False

    # Next.js App Router: only page.tsx/page.jsx is a public route entry.
    if "app" in parts:
        return name == "page"

    # Next.js Pages Router: each source file is a route except framework/API files.
    if "pages" in parts:
        pages_index = parts.index("pages")
        route_parts = parts[pages_index + 1 :]
        if "api" in route_parts or name.startswith("_"):
            return False
        return True

    # Other routers commonly use explicit page/index route entries.
    return "routes" in parts and name in {"page", "index"}


def find_web_pages(project_path: Path) -> list[Path]:
    """Find public-facing route source files deterministically."""
    files = []
    for suffix in PAGE_SUFFIXES:
        for file_path in project_path.rglob(f"*{suffix}"):
            if is_page_file(file_path):
                files.append(file_path)
    return sorted(set(files), key=lambda item: item.as_posix())[:100]


def _read_route_content(file_path: Path) -> str:
    """Read a route and its directly imported local content modules.

    Next.js route entries often delegate all visible markup to content.tsx or
    localized MDX files. Static analysis must follow those imports or it scores
    a thin wrapper instead of the page users and crawlers receive.
    """
    content = file_path.read_text(encoding="utf-8", errors="ignore")
    import_paths = re.findall(r"(?:import|from)\s+(?:[^'\"]+?\s+from\s+)?['\"](\.{1,2}/[^'\"]+)['\"]", content)
    extensions = ("", ".tsx", ".ts", ".jsx", ".js", ".mdx", ".md")
    seen = {file_path.resolve()}
    resolved_imports = []
    for import_path in import_paths:
        base = (file_path.parent / import_path).resolve()
        candidates = [Path(f"{base}{extension}") for extension in extensions]
        candidates.extend(base / f"index{extension}" for extension in extensions[1:])
        for candidate in candidates:
            if not candidate.is_file() or candidate.resolve() in seen:
                continue
            seen.add(candidate.resolve())
            resolved_imports.append(candidate)
            break

    # A localized wrapper renders one locale at a time. Analyze the canonical
    # English source rather than concatenating four mutually exclusive H1s.
    canonical_locale = [item for item in resolved_imports if ".en." in item.name.lower()]
    selected = canonical_locale or resolved_imports
    chunks = [content]
    chunks.extend(item.read_text(encoding="utf-8", errors="ignore") for item in selected)
    return "\n".join(chunks)


def check_page(file_path: Path, project_path: Path | None = None) -> dict:
    """Score a route source file without requiring article metadata on product docs."""
    try:
        content = _read_route_content(file_path)
    except Exception as exc:
        return {"file": str(file_path), "passed": [], "issues": [f"Error: {exc}"], "score": 0}

    issues = []
    passed = []
    optional_points = 0
    lower_content = content.lower()
    parts = set(_lower_parts(file_path))
    is_article = bool(parts & ARTICLE_SEGMENTS)
    is_root_landing = file_path.parent.name.lower() == "app"

    heading_content = re.sub(r"```.*?```", "", content, flags=re.S)
    heading_content = re.sub(r"`(?:\.|[^`])*`", "", heading_content, flags=re.S)
    h1_count = len(re.findall(r"<h1[^>]*>", heading_content, re.I))
    h1_count += len(re.findall(r"^#\s+\S", heading_content, re.M))
    h2_count = len(re.findall(r"<h2[^>]*>", heading_content, re.I))
    h2_count += len(re.findall(r"^##\s+\S", heading_content, re.M))
    required_total = 1 if is_root_landing else 2
    required_passed = 0

    if h1_count == 1:
        passed.append("Single H1 heading (clear topic)")
        required_passed += 1
    elif h1_count == 0:
        issues.append("No H1 heading - page topic unclear")
    else:
        issues.append(f"Multiple H1 headings ({h1_count}) - confusing for AI")

    if not is_root_landing:
        repeated_heading = h2_count >= 1 and ".map(" in content
        if h2_count >= 2 or repeated_heading:
            detail = "dynamic repeated" if repeated_heading and h2_count < 2 else str(h2_count)
            passed.append(f"{detail} H2 subheadings (good structure)")
            required_passed += 1
        else:
            issues.append("Add at least two H2 subheadings for scannable content")

    if "application/ld+json" in lower_content:
        passed.append("JSON-LD structured data found")
        optional_points += 10
    if re.search(r'"@type"\s*:\s*"(Organization|Person|Brand|Article|FAQPage)"', content, re.I):
        passed.append("Recognizable schema entity found")
        optional_points += 5

    author_patterns = ("author", "byline", "written-by", "contributor", 'rel="author"')
    has_author = any(pattern in lower_content for pattern in author_patterns)
    date_patterns = ("datepublished", "datemodified", "datetime=", "pubdate", "article:published")
    has_date = any(pattern in lower_content for pattern in date_patterns)
    if is_article:
        required_total += 2
        if has_author:
            passed.append("Author attribution found")
            required_passed += 1
        else:
            issues.append("Article has no author attribution")
        if has_date:
            passed.append("Publication date found")
            required_passed += 1
        else:
            issues.append("Article has no publication date")
    else:
        optional_points += 3 if has_author else 0
        optional_points += 3 if has_date else 0

    optional_checks = (
        (r"<details|faq|frequently.?asked|\"FAQPage\"", "FAQ section detected", 5),
        (r"<(ul|ol)[^>]*>", "Structured list content found", 5),
        (r"<table[^>]*>", "Comparison table found", 5),
        (r"\d+%|according to|data\s+(shows|reveals)|\d+x\s+(faster|better|more)", "Data-backed claims found", 5),
        (r"is defined as|refers to|means that|in short,|simply put,|<dfn", "Direct-answer phrasing found", 5),
    )
    for pattern, label, points in optional_checks:
        if re.search(pattern, content, re.I):
            passed.append(label)
            optional_points += points

    base_score = (required_passed / required_total * 70) if required_total else 70
    score = min(100, round(base_score + min(optional_points, 30)))
    display = file_path.relative_to(project_path).as_posix() if project_path else file_path.as_posix()
    return {"file": display, "passed": passed, "issues": issues, "score": score}


def main():
    target = sys.argv[1] if len(sys.argv) > 1 else "."
    target_path = Path(target).resolve()
    
    print("\n" + "=" * 60)
    print("  GEO CHECKER - AI Citation Readiness Audit")
    print("=" * 60)
    print(f"Project: {target_path}")
    print("-" * 60)
    
    # Find web pages only
    pages = find_web_pages(target_path)
    
    if not pages:
        print("\n[!] No public web pages found.")
        print("    Looking for: HTML, JSX, TSX files in pages/app directories")
        print("    Skipping: docs, tests, config files, node_modules")
        output = {"script": "geo_checker", "pages_found": 0, "passed": True}
        print("\n" + json.dumps(output, indent=2))
        sys.exit(0)
    
    print(f"Found {len(pages)} public pages to analyze\n")
    
    # Check each page
    results = []
    for page in pages:
        result = check_page(page, target_path)
        results.append(result)
    
    # Print results
    for result in results:
        status = "[OK]" if result['score'] >= 60 else "[!]"
        print(f"{status} {result['file']}: {result['score']}%")
        if result['issues'] and result['score'] < 60:
            for issue in result['issues'][:2]:  # Show max 2 issues
                print(f"    - {issue}")
    
    # Average score
    avg_score = sum(r['score'] for r in results) / len(results) if results else 0
    
    print("\n" + "=" * 60)
    print(f"AVERAGE GEO SCORE: {avg_score:.0f}%")
    print("=" * 60)
    
    if avg_score >= 80:
        print("[OK] Excellent - Content well-optimized for AI citations")
    elif avg_score >= 60:
        print("[OK] Good - Some improvements recommended")
    elif avg_score >= 40:
        print("[!] Needs work - Add structured elements")
    else:
        print("[X] Poor - Content needs GEO optimization")
    
    # JSON output
    output = {
        "script": "geo_checker",
        "project": str(target_path),
        "pages_checked": len(results),
        "average_score": round(avg_score),
        "passed": avg_score >= 60
    }
    print("\n" + json.dumps(output, indent=2))
    
    sys.exit(0 if avg_score >= 60 else 1)


if __name__ == "__main__":
    main()
