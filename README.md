# Hydra — Open-Source Authorized Website Test Toolkit

Hydra is a small, open-source toolkit for checking websites you own or have explicit written authorization to test. It separates three different jobs:

1. **Python smoke test** — low-rate HTTP availability and latency check.
2. **Browser compatibility check** — one real browser session to inspect page loading, JavaScript errors, HTTP errors, and failed same-host requests.
3. **Capacity testing** — staged k6 tests, with distributed execution available through the open-source k6 Operator.

Hydra is licensed under MIT. Third-party tools retain their own licenses and terms.

## Safety and scope

- Test only systems you own or have written authorization to test.
- Obtain hosting/CDN provider approval, schedule a test window, arrange monitoring and an emergency stop contact before production load tests.
- The Python smoke tester is capped at 200 requests, 5 workers and 2 requests/second.
- The browser check opens exactly one browser page. It is not a load test.
- Browser checks use stock Chromium, Firefox or WebKit. TLS verification, CORS, same-origin policy and normal browser security remain enabled. No stealth, fingerprint spoofing, proxy rotation, or security bypass is included.
- Browser checks allow only same-host requests. Third-party assets are intentionally blocked and reported; this isolates the target and may cause external fonts, analytics, or CDN assets not to load in this diagnostic.
- The k6 profile supports a configured ceiling of 100,000 VUs. That is not a guarantee that your machine, generators, or target can safely sustain that load. Use properly sized distributed generators.
- Above 5,000 VUs, k6 requires explicit high-scale and provider-approval confirmations. These are operator acknowledgements, not proof that approval exists.
- Stop if the provider requests it, the target becomes unhealthy, error rates rise sharply, or monitoring is unavailable.

## 1. Install the base toolkit (Kali Linux)

Python 3.10+ is recommended.

```bash
chmod +x run_kali.sh
./run_kali.sh --help
```

Or install manually:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

### Run the low-impact HTTP smoke test

```bash
./run_kali.sh --url https://example.com --allow-host example.com --confirm-host example.com --requests 20 --concurrency 2
```

The target hostname must exactly match both confirmation values. Redirects are not followed and TLS verification is enabled.

## 2. Real-browser compatibility check

This is a separate, optional tool using the open-source [Playwright](https://github.com/microsoft/playwright) browser automation framework.

Install its optional dependency and Chromium:

```bash
source .venv/bin/activate
python -m pip install -r requirements-browser.txt
python -m playwright install chromium
```

Run on Kali:

```bash
chmod +x run_kali_browser.sh
./run_kali_browser.sh --url https://example.com --allow-host example.com --confirm-host example.com --browser chromium
```

Supported browser engines: `chromium`, `firefox`, and `webkit`. Install the corresponding engine with `python -m playwright install firefox` or `python -m playwright install webkit`.

The report includes document status, title, JavaScript page errors, console errors, failed requests, HTTP error responses, and blocked third-party requests. The browser test allows only same-host network requests to avoid unintentionally testing unrelated services. It intentionally does not bypass CORS, TLS, bot protections, or browser security policies.

For a visible browser window, add `--headed` (requires a graphical desktop session).

## 3. Open-source k6 capacity testing

Install the open-source [Grafana k6 CLI](https://grafana.com/docs/k6/latest/set-up/install-k6/).

Start with a small test:

```bash
k6 run -e TARGET_URL=https://example.com/ -e ALLOW_HOST=example.com -e CONFIRM_HOST=example.com -e HYDRA_AUTHORIZED=YES -e HYDRA_MAX_VUS=100 load_test_k6.js
```

The script sends ordinary GET requests to one selected URL, ramps through staged VU levels, checks failure/latency/rate-limit thresholds, and ramps down. It does not simulate login, payment, database writes, or complete user journeys.

### Distributed self-hosted k6 (open source)

For larger tests, use [Grafana k6 Operator](https://github.com/grafana/k6-operator) on a Kubernetes cluster:

- [Install the k6 Operator](https://grafana.com/docs/k6/latest/set-up/set-up-distributed-k6/install-k6-operator/)
- [Run distributed tests](https://grafana.com/docs/k6/latest/set-up/set-up-distributed-k6/usage/run-k6-scripts-with-testrun-crd/)
- [Guidance for large tests](https://grafana.com/docs/k6/latest/testing-guides/running-large-tests/)

Benchmark generators individually and increase worker count gradually. CPU, memory, network egress, NAT, connection tracking, DNS, and provider limits can become bottlenecks.

### Optional managed execution

[Grafana Cloud k6](https://grafana.com/products/cloud/k6/) is optional and may require a paid plan. It is not required to use Hydra or its open-source components. Keep API tokens in a secret manager or secure CI secrets; never commit them.

## 4. High-scale profile

Only after written authorization, hosting/CDN approval, a documented test plan, monitoring, emergency stop contact, and a scheduled window:

```bash
k6 run -e TARGET_URL=https://example.com/ -e ALLOW_HOST=example.com -e CONFIRM_HOST=example.com -e HYDRA_AUTHORIZED=YES -e HYDRA_HIGH_SCALE_APPROVED=YES -e HYDRA_PROVIDER_APPROVAL=YES -e HYDRA_MAX_VUS=100000 -e HYDRA_THINK_TIME=10 load_test_k6.js
```

Do not run this example against a live production site until all approvals and generator capacity are confirmed.

## 5. What to monitor

- **k6:** VUs, iteration/request rate, p95/p99 latency, timeouts, failed requests and dropped iterations.
- **CDN/WAF:** 429/5xx, cache hit ratio, origin offload and rate-limit events.
- **Application:** CPU, memory, worker pools, event-loop lag and application errors.
- **Database:** connection count, query latency, pool saturation, locks and CPU.
- **Generators/network:** CPU, memory, bandwidth, open sockets, file descriptors, NAT and connection tracking.

## 6. Local mock server

```bash
python local_test_server.py
python kitty_tester.py --url http://127.0.0.1:8080 --allow-host 127.0.0.1 --confirm-host 127.0.0.1 --requests 10 --concurrency 2
```

## Contributing

Issues and pull requests are welcome. Include reproducible steps and sanitized logs. Never publish credentials, tokens, customer data, or private target details.
