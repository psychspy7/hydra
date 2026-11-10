#!/usr/bin/env python3
"""
Kitty Corp Enterprise-Grade Advanced Website Load, Stress & WAF Bypass Suite
Cross-Platform (Kali Linux, Ubuntu, Windows)
https://thekittycorp.com/ - support us 🩷
"""

import asyncio
import sys
import os
import time
import random
import statistics
import json
import argparse
from datetime import datetime
from urllib.parse import urlparse, urljoin

if os.name == 'nt':
    os.system('')

try:
    import aiohttp
except ImportError:
    aiohttp = None

RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"
WHITE = "\033[97m"
BOLD = "\033[1m"
RESET = "\033[0m"

BROWSER_USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_7_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64; rv:133.0) Gecko/20100101 Firefox/133.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:133.0) Gecko/20100101 Firefox/133.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.2903.86",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 18_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Mobile/15E148 Safari/604.1"
]

ACCEPT_LANGUAGES = ["en-US,en;q=0.9", "en-GB,en;q=0.8,es;q=0.7", "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7"]

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    clear_screen()
    print(RED + BOLD + "    =========================================================================" + RESET)
    print(GREEN + BOLD + "                         /\\_/\\           /\\_/\\   " + RESET)
    print(GREEN + BOLD + "                        ( " + RED + "o.o" + GREEN + " )         ( " + RED + "^.^" + GREEN + " )  " + RESET)
    print(GREEN + BOLD + "                         > " + RED + "^" + GREEN + " <           > " + RED + "w" + GREEN + " <   " + RESET)
    print(GREEN + BOLD + "                       /|     |\\       /|     |\\ " + RESET)
    print(GREEN + BOLD + "                      (_|     |_)     (_|     |_)" + RESET)
    print(RED + BOLD + "          _  _____ _____ _______   __   ____ ___  ____  ____  " + RESET)
    print(RED + BOLD + "         | |/ /_ _|_   _|_   _\\ \\ / /  / ___/ _ \\|  _ \\|  _ \\ " + RESET)
    print(RED + BOLD + "         | ' / | |  | |   | |  \\ V /  | |  | | | | |_) | |_) |" + RESET)
    print(RED + BOLD + "         | . \\ | |  | |   | |   | |   | |__| |_| |  _ <|  __/ " + RESET)
    print(RED + BOLD + "         |_|\\_\\___| |_|   |_|   |_|    \\____\\___/|_|\\_\\_|    " + RESET)
    print("\n" + GREEN + BOLD + "                        [ made by kitty corp ]" + RESET)
    print(RED + BOLD + "               https://thekittycorp.com/ - support us 🩷" + RESET)
    print(GREEN + "      Advanced Enterprise Load Testing & WAF Bypass Suite | Kali & Windows" + RESET)
    print(RED + BOLD + "    =========================================================================\n" + RESET)

def ask_permission():
    print(RED + BOLD + "[!] LEGAL DISCLAIMER & AUTHORIZATION GATE [!]" + RESET)
    print(YELLOW + "-------------------------------------------------------------------------" + RESET)
    print(WHITE + "This tool is strictly for " + GREEN + BOLD + "educational and research purposes" + RESET + WHITE + " and for")
    print("benchmarking websites you own or have explicit written permission to test.")
    print(RED + BOLD + "You are solely responsible for every action performed with this tool." + RESET)
    print(YELLOW + "-------------------------------------------------------------------------\n" + RESET)
    
    try:
        consent = input(GREEN + BOLD + "[?] Do you agree that this is for educational/research purposes and accept full responsibility? (yes/no): " + RESET).strip().lower()
    except (KeyboardInterrupt, EOFError):
        print("\n" + RED + "[!] Aborted by user." + RESET)
        sys.exit(0)

    if consent not in ['yes', 'y']:
        print("\n" + RED + BOLD + "[X] Permission denied. Exiting Kitty Corp Testing Engine." + RESET)
        sys.exit(0)
    print("\n" + GREEN + "[+] Authorization confirmed. Initializing enterprise engine...\n" + RESET)

def validate_url(url: str) -> str:
    url = url.strip()
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    parsed = urlparse(url)
    if not parsed.netloc:
        raise ValueError("Invalid target URL format.")
    return url

async def send_request_advanced(session, base_url, mode, req_id, semaphore, stats, paths):
    native_path = random.choice(paths) if paths else "/"
    target_url = urljoin(base_url, native_path)

    async with semaphore:
        ua = random.choice(BROWSER_USER_AGENTS)
        headers = {
            "User-Agent": ua,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": random.choice(ACCEPT_LANGUAGES),
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Sec-Ch-Ua": '"Not A(Brand";v="99", "Google Chrome";v="131", "Chromium";v="131"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"Windows"',
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "cross-site",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1"
        }

        if mode == 2:
            sep = "&" if "?" in target_url else "?"
            target_url = f"{target_url}{sep}_kc_cb={req_id}_{random.randint(100000, 999999)}"
            headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
            headers["Pragma"] = "no-cache"
            headers["Referer"] = random.choice([
                "https://www.google.com/search?q=thekittycorp",
                "https://github.com/explore",
                "https://x.com/kittycorp",
                base_url
            ])

        start_t = time.perf_counter()
        try:
            async with session.get(target_url, headers=headers, allow_redirects=True, ssl=False) as response:
                await response.read()
                elapsed = (time.perf_counter() - start_t) * 1000.0
                code = response.status
                stats["completed"] += 1
                stats["latencies"].append(elapsed)
                stats["status_codes"][code] = stats["status_codes"].get(code, 0) + 1
                if 200 <= code < 400:
                    stats["success"] += 1
                else:
                    stats["failed"] += 1
        except Exception as e:
            elapsed = (time.perf_counter() - start_t) * 1000.0
            stats["completed"] += 1
            stats["failed"] += 1
            err_name = type(e).__name__
            stats["errors"][err_name] = stats["errors"].get(err_name, 0) + 1
            stats["latencies"].append(elapsed)

        if mode == 1:
            await asyncio.sleep(0.002)

async def progress_monitor(total_requests, stats, start_time):
    while stats["completed"] < total_requests:
        done = stats["completed"]
        elapsed = max(time.perf_counter() - start_time, 0.001)
        rps = done / elapsed
        pct = (done / total_requests) * 100
        bar_len = 30
        filled = int(bar_len * done // total_requests)
        bar = f"{GREEN}{'█' * filled}{RED}{'░' * (bar_len - filled)}{RESET}"
        sys.stdout.write(
            f"\r{BOLD}[{bar}] {pct:5.1f}% | Sent: {done}/{total_requests} | "
            f"{GREEN}OK: {stats['success']}{RESET} | {RED}ERR: {stats['failed']}{RESET} | "
            f"{CYAN}{rps:6.1f} req/s{RESET}"
        )
        sys.stdout.flush()
        await asyncio.sleep(0.1)

    done = stats["completed"]
    elapsed = max(time.perf_counter() - start_time, 0.001)
    rps = done / elapsed
    bar = f"{GREEN}{'█' * 30}{RESET}"
    sys.stdout.write(
        f"\r{BOLD}[{bar}] 100.0% | Sent: {done}/{total_requests} | "
        f"{GREEN}OK: {stats['success']}{RESET} | {RED}ERR: {stats['failed']}{RESET} | "
        f"{CYAN}{rps:6.1f} req/s{RESET}\n"
    )
    sys.stdout.flush()

async def run_load_test(url: str, mode: int, total_requests: int = 10000, custom_concurrency: int = None):
    if aiohttp is None:
        print(RED + "[!] 'aiohttp' is not installed. Please run: pip install -r requirements.txt" + RESET)
        sys.exit(1)

    concurrency = custom_concurrency if custom_concurrency else (200 if mode == 1 else 500)
    mode_name = "MODE 1: NORMAL (Balanced Multi-Path WAF-Safe Load)" if mode == 1 else "MODE 2: INTENSE (High-Throughput Stress Burst)"
    timeout_sec = 15 if mode == 1 else 10

    test_paths = ["/", "/index.html", "/#about", "/#contact", "/?ref=ai_tester_v4"]

    print(f"\n{GREEN}{BOLD}================ ENTERPRISE TEST CONFIGURATION ================{RESET}")
    print(f" {WHITE}Target URL       :{RESET} {CYAN}{url}{RESET}")
    print(f" {WHITE}Selected Mode    :{RESET} {RED if mode == 2 else GREEN}{BOLD}{mode_name}{RESET}")
    print(f" {WHITE}Total Requests   :{RESET} {BOLD}{total_requests}{RESET}")
    print(f" {WHITE}Concurrency Pool :{RESET} {BOLD}{concurrency} parallel workers{RESET}")
    print(f" {WHITE}Platform OS      :{RESET} {BOLD}{sys.platform} ({os.name}){RESET}")
    print(f"{GREEN}{BOLD}================================================================{RESET}\n")

    stats = {
        "completed": 0,
        "success": 0,
        "failed": 0,
        "latencies": [],
        "status_codes": {},
        "errors": {}
    }

    semaphore = asyncio.Semaphore(concurrency)
    connector = aiohttp.TCPConnector(limit=concurrency, ttl_dns_cache=300, ssl=False, force_close=False)
    timeout = aiohttp.ClientTimeout(total=timeout_sec)

    start_time = time.perf_counter()

    async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
        monitor_task = asyncio.create_task(progress_monitor(total_requests, stats, start_time))
        tasks = [
            asyncio.create_task(send_request_advanced(session, url, mode, i, semaphore, stats, test_paths))
            for i in range(1, total_requests + 1)
        ]
        await asyncio.gather(*tasks)
        await monitor_task

    total_duration = time.perf_counter() - start_time
    print_report(url, mode_name, total_requests, concurrency, total_duration, stats)

def print_report(url, mode_name, total_requests, concurrency, total_duration, stats):
    latencies = sorted(stats["latencies"])
    avg_lat = statistics.mean(latencies) if latencies else 0
    min_lat = latencies[0] if latencies else 0
    max_lat = latencies[-1] if latencies else 0
    p50 = latencies[int(len(latencies) * 0.50)] if latencies else 0
    p90 = latencies[int(len(latencies) * 0.90)] if latencies else 0
    p95 = latencies[int(len(latencies) * 0.95)] if latencies else 0
    p99 = latencies[int(len(latencies) * 0.99)] if latencies else 0
    rps = total_requests / max(total_duration, 0.001)

    print(f"\n{RED}{BOLD}================ KITTY CORP ENTERPRISE AUDIT REPORT ================{RESET}")
    print(f" {WHITE}Target Website     :{RESET} {url}")
    print(f" {WHITE}Engine Mode        :{RESET} {mode_name}")
    print(f" {WHITE}Total Time Taken   :{RESET} {total_duration:.2f} seconds")
    print(f" {WHITE}Average Throughput :{RESET} {GREEN}{BOLD}{rps:.2f} requests/sec{RESET}")
    print(f" {WHITE}Total Requests     :{RESET} {total_requests}")
    print(f" {WHITE}Successful (2xx/3xx):{RESET} {GREEN}{stats['success']}{RESET}")
    print(f" {WHITE}Failed / Errors    :{RESET} {RED}{stats['failed']}{RESET}")
    print(f"{GREEN}--------------------------------------------------------------------{RESET}")
    print(f" {BOLD}LATENCY PERCENTILES (Milliseconds):{RESET}")
    print(f"   Min: {min_lat:.2f} ms | Avg: {avg_lat:.2f} ms | Max: {max_lat:.2f} ms")
    print(f"   P50: {p50:.2f} ms | P90: {p90:.2f} ms | P95: {p95:.2f} ms | P99: {p99:.2f} ms")
    
    if stats["status_codes"]:
        print(f"{GREEN}--------------------------------------------------------------------{RESET}")
        print(f" {BOLD}HTTP STATUS CODE BREAKDOWN:{RESET}")
        for code, count in sorted(stats["status_codes"].items()):
            color = GREEN if 200 <= code < 400 else RED
            print(f"   {color}HTTP {code}{RESET} : {count} responses")

    if stats["errors"]:
        print(f"{GREEN}--------------------------------------------------------------------{RESET}")
        print(f" {BOLD}NETWORK / TIMEOUT ERRORS:{RESET}")
        for err, count in sorted(stats["errors"].items(), key=lambda x: x[1], reverse=True):
            print(f"   {RED}{err}{RESET} : {count}")

    report_data = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "generator": "Kitty Corp Enterprise Advanced Load Tester (https://thekittycorp.com/)",
        "target": url,
        "mode": mode_name,
        "total_requests": total_requests,
        "concurrency": concurrency,
        "duration_seconds": round(total_duration, 3),
        "requests_per_second": round(rps, 2),
        "success_count": stats["success"],
        "failed_count": stats["failed"],
        "latency_ms": {
            "min": round(min_lat, 2),
            "avg": round(avg_lat, 2),
            "max": round(max_lat, 2),
            "p50": round(p50, 2),
            "p90": round(p90, 2),
            "p95": round(p95, 2),
            "p99": round(p99, 2),
        },
        "status_codes": stats["status_codes"],
        "errors": stats["errors"]
    }

    report_file = f"kitty_enterprise_report_{int(time.time())}.json"
    with open(report_file, "w", encoding="utf-8") as f:
        json.dump(report_data, f, indent=4)

    print(f"{GREEN}--------------------------------------------------------------------{RESET}")
    print(f" {GREEN}[+] Detailed JSON audit report saved to: {BOLD}{report_file}{RESET}")
    print(f" {RED}{BOLD}made by kitty corp | https://thekittycorp.com/ - support us 🩷{RESET}")
    print(f"{RED}{BOLD}===================================================================={RESET}\n")

def interactive_menu():
    print_banner()
    ask_permission()

    try:
        raw_url = input(GREEN + BOLD + "[1] Enter Target Website URL (e.g., https://example.com): " + RESET)
        target_url = validate_url(raw_url)
    except Exception as e:
        print(RED + f"[X] Error: {e}" + RESET)
        sys.exit(1)

    print(f"\n{CYAN}{BOLD}Select Enterprise Load Testing Mode (Default: 10,000 Requests):{RESET}")
    print(f"  {GREEN}{BOLD}[1] Normal Mode{RESET}  - 10,000 requests | Multi-path balanced load | WAF friendly")
    print(f"  {RED}{BOLD}[2] Intense Mode{RESET} - 10,000 requests | High concurrency burst | Cache-bypass & Anti-bot rotation")

    try:
        mode_choice = input(f"\n{GREEN}{BOLD}[2] Choose Mode (1 or 2): {RESET}").strip()
        mode = 2 if mode_choice == "2" else 1
        
        req_input = input(f"{GREEN}{BOLD}[3] Number of Requests [Press Enter for 10000]: {RESET}").strip()
        total_requests = int(req_input) if req_input else 10000
    except (ValueError, KeyboardInterrupt, EOFError):
        print(f"\n{RED}[!] Invalid input or cancelled. Exiting.{RESET}")
        sys.exit(1)

    if sys.platform.startswith("win"):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    try:
        asyncio.run(run_load_test(target_url, mode, total_requests))
    except KeyboardInterrupt:
        print(f"\n\n{RED}{BOLD}[!] Test interrupted by user.{RESET}")

def main():
    parser = argparse.ArgumentParser(description="Kitty Corp Enterprise Advanced Load Tester")
    parser.add_argument("-u", "--url", help="Target Website URL")
    parser.add_argument("-m", "--mode", type=int, choices=[1, 2], help="1 = Normal Mode, 2 = Intense Mode")
    parser.add_argument("-n", "--requests", type=int, default=10000, help="Total requests (default: 10000)")
    parser.add_argument("-c", "--concurrency", type=int, help="Override concurrency workers")
    args = parser.parse_args()

    if args.url and args.mode:
        print_banner()
        ask_permission()
        target_url = validate_url(args.url)
        if sys.platform.startswith("win"):
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        try:
            asyncio.run(run_load_test(target_url, args.mode, args.requests, args.concurrency))
        except KeyboardInterrupt:
            print(f"\n\n{RED}{BOLD}[!] Test interrupted by user.{RESET}")
    else:
        interactive_menu()

if __name__ == "__main__":
    main()
