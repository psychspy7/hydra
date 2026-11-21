# Hydra — Kitty Corp Authorized Website Smoke Tester

Hydra is a **low-impact, controlled smoke/performance test utility** for websites you own or have explicit authorization to test. It is intended for pre-launch checks, not denial-of-service testing or WAF evasion.

## Safety limits
- Maximum 200 requests per run
- Maximum 5 concurrent workers
- Global pacing of 2 requests/second
- TLS certificate verification enabled
- Redirects disabled (to avoid following requests outside the selected target)
- Exact hostname must match both authorization arguments and a typed confirmation
- No cache-busting, proxy rotation, user-agent rotation, or WAF-bypass behavior

## Setup
Python 3.10+ recommended.

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Run
```bash
python kitty_tester.py --url https://example.com --allow-host example.com --confirm-host example.com --requests 20 --concurrency 2
```
Replace `example.com` with a hostname you own or have written authorization to test. The tool asks you to type the hostname again before starting.

## Output
A timestamped JSON report includes elapsed time, observed request rate, success/failure counts, HTTP status distribution, network exception counts, and latency min/average/P50/P90/P95/max.

## Local validation
Start the local mock server in one terminal:
```bash
python local_test_server.py
```
In another terminal:
```bash
python kitty_tester.py --url http://127.0.0.1:8080 --allow-host 127.0.0.1 --confirm-host 127.0.0.1 --requests 10 --concurrency 2
```

## Other integrations
The repository retains example Locust and k6 files. Review their configured targets and test profile before running; do not run them against production or third-party systems without authorization and an approved test window.

**Use responsibly:** even small tests can affect services. Coordinate with your hosting provider and monitor application, database, CDN, and error logs.
