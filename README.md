# Hydra — Kitty Corp Authorized Website Capacity Tester

Hydra provides conservative smoke testing and a staged k6 capacity-test profile for websites you own or have explicit written authorization to test.

## Safety first
- Do not run load tests against a production site without a scheduled test window and approval from your hosting/CDN provider.
- The Python smoke tester is capped at 200 requests, 5 workers and 2 requests/second.
- The k6 profile supports up to 100,000 concurrent virtual users, but **100k is a target ceiling, not a promise that one computer can generate that load**. Use properly sized distributed load generators and validate generator CPU, memory, network and connection limits.
- The k6 script sends ordinary GET requests to one explicitly selected URL. It does not attempt WAF bypass, cache busting, credential testing, or redirect following.
- Above 5,000 VUs, the script requires explicit high-scale and provider-approval environment confirmations.
- Thresholds abort the run when errors, rate limiting, or latency exceed the configured limits. Tune thresholds to your actual service-level objectives before a scheduled test.

## Python smoke test setup
Python 3.10+ recommended.

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
python -m pip install -r requirements.txt
```

Run a small smoke test:
```bash
python kitty_tester.py --url https://thekittycorp.com --allow-host thekittycorp.com --confirm-host thekittycorp.com --requests 20 --concurrency 2
```

## k6 staged capacity test
Install k6 on the load-generator host(s). First run a small test (100–1,000 VUs), confirm the generator is not saturated, and review origin/CDN/application/database metrics.

Example for a small test:
```bash
k6 run -e TARGET_URL=https://thekittycorp.com/ -e ALLOW_HOST=thekittycorp.com -e CONFIRM_HOST=thekittycorp.com -e HYDRA_AUTHORIZED=YES -e HYDRA_MAX_VUS=100 load_test_k6.js
```

### High-scale profile (requires provider approval and distributed generators)
Only after a written test plan, provider approval, monitoring, an emergency stop contact, and a scheduled window are in place:

```bash
k6 run -e TARGET_URL=https://thekittycorp.com/ -e ALLOW_HOST=thekittycorp.com -e CONFIRM_HOST=thekittycorp.com -e HYDRA_AUTHORIZED=YES -e HYDRA_HIGH_SCALE_APPROVED=YES -e HYDRA_PROVIDER_APPROVAL=YES -e HYDRA_MAX_VUS=100000 -e HYDRA_THINK_TIME=10 load_test_k6.js
```

The profile ramps in two-minute stages through the capacity ladder, holds the selected ceiling for three minutes, then ramps down. Default think time is 5 seconds; use a realistic value for your expected user journey. A single GET endpoint is only a capacity probe, not a complete simulation of logins, database writes, checkout, or real browsing sessions.

## What to monitor during a run
- k6: VUs, iteration rate, request rate, p95/p99 latency, timeouts and failed requests
- CDN/WAF: 429/5xx, origin offload, cache hit ratio and rate-limit events
- Application: CPU, memory, worker/thread pools, event-loop lag and application errors
- Database: connections, query latency, pool saturation, locks and CPU
- Infrastructure: bandwidth, open connections, file descriptors and autoscaling events

Stop immediately if the provider asks, the site becomes unhealthy, error rates rise sharply, or monitoring is unavailable. Do not treat a passing test of the homepage as proof that every product workflow supports the same number of users.

## Local validation
Start the local mock server:
```bash
python local_test_server.py
```
Then run:
```bash
python kitty_tester.py --url http://127.0.0.1:8080 --allow-host 127.0.0.1 --confirm-host 127.0.0.1 --requests 10 --concurrency 2
```

Use only targets you own or are authorized to test. Even a legitimate load test can disrupt shared hosting and other tenants.
