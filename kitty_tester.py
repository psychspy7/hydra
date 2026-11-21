#!/usr/bin/env python3
"""Hydra: low-impact, authorized website smoke/performance tester.

Limits are intentionally conservative: 200 requests, 5 concurrent workers,
and 2 requests/second. Redirects are not followed, TLS verification is enabled,
and the requested hostname must be explicitly allow-listed and confirmed.
"""
import argparse
import asyncio
import json
import os
import statistics
import time
from datetime import datetime, timezone
from urllib.parse import urlparse

try:
    import aiohttp
except ImportError:
    aiohttp = None

MAX_REQUESTS = 200
MAX_CONCURRENCY = 5
MAX_RPS = 2.0
TIMEOUT_SECONDS = 10

def normalize_url(value):
    value = value.strip()
    if not value.startswith(("http://", "https://")):
        value = "https://" + value
    parsed = urlparse(value)
    if parsed.scheme not in ("http", "https") or not parsed.hostname:
        raise ValueError("Enter a valid HTTP(S) URL.")
    return value

def percentile(values, p):
    if not values:
        return 0.0
    ordered = sorted(values)
    index = min(len(ordered)-1, max(0, round((len(ordered)-1)*p)))
    return ordered[index]

async def run_test(url, count, concurrency):
    if aiohttp is None:
        raise RuntimeError("aiohttp missing. Install with: pip install -r requirements.txt")
    parsed = urlparse(url)
    host = parsed.hostname.lower()
    stats = {"completed": 0, "success": 0, "failed": 0, "status_codes": {}, "errors": {}}
    latencies = []
    sem = asyncio.Semaphore(concurrency)
    start = time.perf_counter()
    timeout = aiohttp.ClientTimeout(total=TIMEOUT_SECONDS)
    connector = aiohttp.TCPConnector(limit=concurrency, ssl=True)

    async def worker(i):
        # Global pacing: one request every 0.5 seconds, staggered across workers.
        await asyncio.sleep(i / MAX_RPS)
        async with sem:
            t0 = time.perf_counter()
            try:
                async with session.get(url, allow_redirects=False, headers={"User-Agent": "Hydra-Authorized-SmokeTest/1.0"}) as resp:
                    await resp.read()
                    elapsed = (time.perf_counter()-t0)*1000
                    latencies.append(elapsed)
                    stats["status_codes"][str(resp.status)] = stats["status_codes"].get(str(resp.status),0)+1
                    if 200 <= resp.status < 400:
                        stats["success"] += 1
                    else:
                        stats["failed"] += 1
            except Exception as exc:
                elapsed = (time.perf_counter()-t0)*1000
                latencies.append(elapsed)
                name = type(exc).__name__
                stats["errors"][name] = stats["errors"].get(name,0)+1
                stats["failed"] += 1
            stats["completed"] += 1
            print(f"Progress: {stats['completed']}/{count} | OK: {stats['success']} | Failed: {stats['failed']}")

    async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
        await asyncio.gather(*(worker(i) for i in range(count)))

    duration = time.perf_counter()-start
    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "tool": "Hydra Safe Smoke Test",
        "target": url,
        "target_host": host,
        "limits": {"requests": count, "concurrency": concurrency, "max_rate_rps": MAX_RPS, "timeout_seconds": TIMEOUT_SECONDS},
        "duration_seconds": round(duration,3),
        "requests_per_second": round(stats["completed"]/duration,3) if duration else 0,
        "success_count": stats["success"],
        "failed_count": stats["failed"],
        "status_codes": stats["status_codes"],
        "errors": stats["errors"],
        "latency_ms": {
            "min": round(min(latencies),2) if latencies else 0,
            "avg": round(statistics.mean(latencies),2) if latencies else 0,
            "p50": round(percentile(latencies,.50),2),
            "p90": round(percentile(latencies,.90),2),
            "p95": round(percentile(latencies,.95),2),
            "max": round(max(latencies),2) if latencies else 0
        }
    }
    filename = f"hydra_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename,"w",encoding="utf-8") as f:
        json.dump(report,f,indent=2)
    print("\n=== HYDRA TEST REPORT ===")
    print(json.dumps(report,indent=2))
    print(f"Saved: {filename}")

def main():
    parser = argparse.ArgumentParser(description="Hydra low-impact authorized website smoke test")
    parser.add_argument("--url", required=True, help="Target URL")
    parser.add_argument("--allow-host", required=True, help="Exact hostname you are authorized to test")
    parser.add_argument("--confirm-host", required=True, help="Repeat hostname to confirm target")
    parser.add_argument("--requests", type=int, default=20, help=f"Requests (1-{MAX_REQUESTS}, default 20)")
    parser.add_argument("--concurrency", type=int, default=2, help=f"Workers (1-{MAX_CONCURRENCY}, default 2)")
    args = parser.parse_args()
    url = normalize_url(args.url)
    host = urlparse(url).hostname.lower()
    allow = args.allow_host.strip().lower()
    confirm = args.confirm_host.strip().lower()
    if host != allow or host != confirm:
        parser.error("Target hostname must exactly match both --allow-host and --confirm-host.")
    if not 1 <= args.requests <= MAX_REQUESTS:
        parser.error(f"--requests must be between 1 and {MAX_REQUESTS}.")
    if not 1 <= args.concurrency <= MAX_CONCURRENCY:
        parser.error(f"--concurrency must be between 1 and {MAX_CONCURRENCY}.")
    print("Hydra low-impact test")
    print(f"Target: {url}\nRequests: {args.requests}\nConcurrency: {args.concurrency}\nRate cap: {MAX_RPS} req/s")
    print("Redirects disabled; TLS verification enabled.")
    consent = input(f"Type the exact hostname '{host}' to start: ").strip().lower()
    if consent != host:
        print("Confirmation mismatch. Aborted.")
        return
    asyncio.run(run_test(url,args.requests,args.concurrency))

if __name__ == "__main__":
    main()
