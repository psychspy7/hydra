#!/usr/bin/env python3
"""One-session, allow-listed browser smoke check using stock Playwright browsers.

This is a compatibility diagnostic, not a load generator or stealth browser.
TLS validation and browser security controls remain enabled.
"""
import argparse
import asyncio
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse, urlunparse

from playwright.async_api import async_playwright


def safe_url(value):
    value = value.strip()
    if not value.startswith(("http://", "https://")):
        value = "https://" + value
    parsed = urlparse(value)
    if parsed.scheme not in ("http", "https") or not parsed.hostname:
        raise ValueError("Provide a valid HTTP(S) URL.")
    if parsed.username or parsed.password:
        raise ValueError("Credentials in URLs are not allowed.")
    return parsed


async def run(args):
    parsed = safe_url(args.url)
    host = parsed.hostname.lower()
    if host != args.allow_host.lower() or host != args.confirm_host.lower():
        raise ValueError("Target hostname must exactly match --allow-host and --confirm-host.")
    if host not in ("localhost", "127.0.0.1", "::1") and parsed.scheme != "https":
        raise ValueError("Use HTTPS for non-local targets.")
    if not 1000 <= args.timeout_ms <= 60000:
        raise ValueError("--timeout-ms must be between 1000 and 60000.")

    target = urlunparse(parsed._replace(query="", fragment=""))
    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "tool": "Hydra Browser Compatibility Smoke Check",
        "browser": args.browser,
        "target": target,
        "target_host": host,
        "checks": {},
        "console_errors": [],
        "page_errors": [],
        "failed_requests": [],
        "blocked_external_requests": [],
    }

    async with async_playwright() as playwright:
        browser_type = getattr(playwright, args.browser)
        browser = await browser_type.launch(headless=not args.headed)
        context = await browser.new_context(ignore_https_errors=False)
        page = await context.new_page()
        page.set_default_timeout(args.timeout_ms)

        async def guard_route(route):
            request_host = (urlparse(route.request.url).hostname or "").lower()
            if request_host != host:
                report["blocked_external_requests"].append(route.request.url[:300])
                await route.abort()
                return
            await route.continue_()

        await page.route("**/*", guard_route)
        page.on("console", lambda msg: report["console_errors"].append(msg.text[:500]) if msg.type == "error" else None)
        page.on("pageerror", lambda exc: report["page_errors"].append(str(exc)[:500]))
        page.on("requestfailed", lambda req: report["failed_requests"].append({
            "url": req.url[:300], "failure": (req.failure or "request failed")[:300]
        }))
        page.on("response", lambda response: report["checks"].setdefault("http_error_responses", []).append({
            "status": response.status, "url": response.url[:300]
        }) if response.status >= 400 else None)

        try:
            response = await page.goto(args.url, wait_until="domcontentloaded", timeout=args.timeout_ms)
            report["checks"]["navigation_status"] = response.status if response else None
            report["checks"]["final_url"] = page.url.split("?", 1)[0][:500]
            report["checks"]["title"] = (await page.title())[:300]
            report["checks"]["document_ready"] = await page.evaluate("document.readyState")
            report["checks"]["main_document_ok"] = bool(response and response.status < 400)
        except Exception as exc:
            report["checks"]["navigation_error"] = str(exc)[:700]
            report["checks"]["main_document_ok"] = False
        finally:
            await context.close()
            await browser.close()

    report["passed"] = bool(report["checks"].get("main_document_ok")) and not report["page_errors"]
    report["notes"] = [
        "Single browser session only; this is not a concurrency or capacity test.",
        "Only same-host requests are allowed; third-party assets are intentionally blocked and listed.",
        "Stock browser security, same-origin policy, CORS, and TLS verification remain enabled.",
        "No stealth, fingerprint spoofing, proxy rotation, or browser-security bypass is used.",
    ]
    filename = f"hydra_browser_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    Path(filename).write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    print(f"Saved: {filename}")
    return 0 if report["passed"] else 1


def main():
    parser = argparse.ArgumentParser(description="Hydra one-session browser compatibility check")
    parser.add_argument("--url", required=True)
    parser.add_argument("--allow-host", required=True)
    parser.add_argument("--confirm-host", required=True)
    parser.add_argument("--browser", choices=("chromium", "firefox", "webkit"), default="chromium")
    parser.add_argument("--timeout-ms", type=int, default=15000)
    parser.add_argument("--headed", action="store_true", help="Show the browser window")
    args = parser.parse_args()
    host = (urlparse(safe_url(args.url).geturl()).hostname or "").lower()
    print(f"Browser check target: {host} | browser: {args.browser}")
    if input(f"Type the exact hostname '{host}' to continue: ").strip().lower() != host:
        print("Confirmation mismatch. Aborted.")
        raise SystemExit(2)
    raise SystemExit(asyncio.run(run(args)))


if __name__ == "__main__":
    main()
