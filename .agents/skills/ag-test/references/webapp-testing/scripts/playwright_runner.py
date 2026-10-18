#!/usr/bin/env python3
"""Run a Playwright smoke or lightweight accessibility test against a URL."""
from __future__ import annotations

import argparse
import json
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    sync_playwright = None


def valid_url(value: str) -> str:
    parsed = urlparse(value)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise argparse.ArgumentTypeError("URL must start with http:// or https://")
    return value


def run_test(url: str, screenshot: bool, accessibility_only: bool, timeout_ms: int) -> dict:
    if sync_playwright is None:
        return {"url": url, "status": "error", "error": "Playwright is not installed", "fix": "pip install playwright && playwright install chromium"}

    result = {"url": url, "timestamp": datetime.now(timezone.utc).isoformat(), "status": "pending"}
    try:
        with sync_playwright() as runtime:
            browser = runtime.chromium.launch(headless=True)
            context = browser.new_context(viewport={"width": 1280, "height": 720})
            page = context.new_page()
            console_errors: list[str] = []
            page_errors: list[str] = []
            page.on("console", lambda message: console_errors.append(message.text) if message.type == "error" else None)
            page.on("pageerror", lambda error: page_errors.append(str(error)))

            response = page.goto(url, wait_until="networkidle", timeout=timeout_ms)
            status_code = response.status if response else None
            title = page.title()

            accessibility = page.evaluate(
                """() => {
                    const text = (el) => (el.innerText || el.textContent || '').trim();
                    const interactive = [...document.querySelectorAll('button, a[href], input, select, textarea')];
                    return {
                        images_total: document.querySelectorAll('img').length,
                        images_without_alt: document.querySelectorAll('img:not([alt])').length,
                        buttons_without_name: [...document.querySelectorAll('button')].filter(el => !text(el) && !el.getAttribute('aria-label') && !el.getAttribute('title')).length,
                        links_without_name: [...document.querySelectorAll('a[href]')].filter(el => !text(el) && !el.getAttribute('aria-label') && !el.getAttribute('title')).length,
                        inputs_without_label: [...document.querySelectorAll('input:not([type=hidden]), select, textarea')].filter(el => {
                            const id = el.id;
                            return !el.getAttribute('aria-label') && !el.getAttribute('aria-labelledby') && !(id && document.querySelector(`label[for="${CSS.escape(id)}"]`)) && !el.closest('label');
                        }).length,
                        h1_count: document.querySelectorAll('h1').length,
                        interactive_count: interactive.length,
                    };
                }"""
            )

            result.update({
                "page": {"title": title, "final_url": page.url, "status_code": status_code},
                "accessibility": accessibility,
                "console_errors": console_errors[:20],
                "page_errors": page_errors[:20],
            })

            if not accessibility_only:
                navigation = page.evaluate(
                    """() => {
                        const entry = performance.getEntriesByType('navigation')[0];
                        if (!entry) return {};
                        return {
                            dom_content_loaded_ms: Math.round(entry.domContentLoadedEventEnd),
                            load_complete_ms: Math.round(entry.loadEventEnd),
                            response_ms: Math.round(entry.responseEnd),
                        };
                    }"""
                )
                result["performance"] = navigation
                result["elements"] = {
                    "links": page.locator("a").count(),
                    "buttons": page.locator("button").count(),
                    "inputs": page.locator("input").count(),
                    "images": page.locator("img").count(),
                    "forms": page.locator("form").count(),
                }

            if screenshot:
                screenshot_dir = Path(tempfile.gettempdir()) / "agkit_screenshots"
                screenshot_dir.mkdir(parents=True, exist_ok=True)
                screenshot_path = screenshot_dir / f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}.png"
                page.screenshot(path=str(screenshot_path), full_page=True)
                result["screenshot"] = str(screenshot_path)

            context.close()
            browser.close()

            blocking_a11y = sum(accessibility[key] for key in ("images_without_alt", "buttons_without_name", "links_without_name", "inputs_without_label"))
            loaded = status_code is not None and status_code < 400
            result["passed"] = bool(loaded and title and not page_errors and blocking_a11y == 0)
            result["status"] = "success" if result["passed"] else "failed"
    except Exception as exc:
        result.update({"status": "error", "passed": False, "error": str(exc)})
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Run a Playwright smoke test")
    parser.add_argument("url", type=valid_url)
    parser.add_argument("--screenshot", action="store_true")
    parser.add_argument("--a11y", action="store_true", help="Run only lightweight accessibility checks")
    parser.add_argument("--timeout-ms", type=int, default=30000)
    args = parser.parse_args()
    result = run_test(args.url, args.screenshot, args.a11y, args.timeout_ms)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result.get("passed") else 1


if __name__ == "__main__":
    raise SystemExit(main())
