# Hydra — Open-Source Authorized Website Capacity Tester

Hydra is an open-source toolkit for conservative smoke tests and staged capacity tests against systems you own or have explicit written authorization to test.

## What Hydra uses

- **Python smoke tester:** a small, bounded check for basic availability and latency.
- **Grafana k6 (open source):** the load-test engine and JavaScript test scripts.
- **Self-hosted distributed option:** Grafana's open-source k6 Operator can distribute k6 workers across a Kubernetes cluster.
- **Optional managed option:** Grafana Cloud k6 can run tests on Grafana-managed infrastructure. This is a hosted service, may require a paid plan, and is not required to use Hydra.

Hydra itself is public under the MIT License. Third-party tools retain their own licenses and terms; see [LICENSE](LICENSE) and the linked upstream projects.

## Safety first

- Only test systems you own or have explicit written authorization to test.
- Do not run load tests against production without a scheduled window, provider approval, monitoring, and an emergency stop contact.
- The Python smoke tester is capped at 200 requests, 5 workers and 2 requests/second.
- The k6 profile supports up to 100,000 concurrent virtual users, but **100k is a configured ceiling, not a guarantee that one computer or cluster can generate that load**. Size and benchmark load generators independently.
- The k6 script sends ordinary GET traffic to one explicitly selected URL. It does not attempt WAF bypass, cache busting, credential testing, or redirect following.
- Above 5,000 VUs, the script requires explicit high-scale and provider-approval environment confirmations. These flags are operator acknowledgements, not proof of actual provider approval.
- Thresholds abort a run when errors, rate limiting, or latency exceed configured limits. Tune thresholds to your service objectives before a scheduled test.
- Never use Hydra to test third-party services, shared infrastructure, or production systems without authorization.

## Python smoke test setup

Python 3.10+ recommended.

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# Linux/macOS: source .venv/bin/activate
python -m pip install -r requirements.txt
```

Run a small smoke test:

```bash
python kitty_tester.py --url https://example.com --allow-host example.com --confirm-host example.com --requests 20 --concurrency 2
```

## k6: local open-source execution

Install the open-source k6 CLI using the [official installation guide](https://grafana.com/docs/k6/latest/set-up/install-k6/).

Start with a small test and confirm the generator has spare CPU, memory, network capacity, and file descriptors:

```bash
k6 run -e TARGET_URL=https://example.com/ -e ALLOW_HOST=example.com -e CONFIRM_HOST=example.com -e HYDRA_AUTHORIZED=YES -e HYDRA_MAX_VUS=100 load_test_k6.js
```

Replace `example.com` with a hostname you control. The target hostname must exactly match both host confirmation values.

## Distributed self-hosted execution (open source)

For larger tests, Hydra can be used with [Grafana k6 Operator](https://github.com/grafana/k6-operator), an open-source Kubernetes operator that runs distributed k6 tests across a Kubernetes cluster.

Official setup and usage guides:

- [Install the k6 Operator](https://grafana.com/docs/k6/latest/set-up/set-up-distributed-k6/install-k6-operator/)
- [Run k6 scripts with the TestRun resource](https://grafana.com/docs/k6/latest/set-up/set-up-distributed-k6/usage/run-k6-scripts-with-testrun-crd/)
- [Running large tests](https://grafana.com/docs/k6/latest/testing-guides/running-large-tests/)

This option requires a Kubernetes cluster and operational experience. Start with a small worker count, benchmark each generator, and increase parallelism gradually. Do not assume that adding workers linearly increases safe capacity; network egress, NAT, connection tracking, DNS, and the target's own limits can become bottlenecks.

## Optional managed execution: Grafana Cloud k6

Grafana Cloud k6 is optional. It is a managed service, not a prerequisite and not part of Hydra's MIT-licensed code. It can execute tests on managed infrastructure and provide hosted result dashboards.

1. Create a Grafana Cloud account and enable k6.
2. Create an API token and authenticate the CLI:

```bash
k6 cloud login --token YOUR_API_TOKEN --stack YOUR_STACK_URL_OR_SLUG
```

3. Run the same Hydra script in the cloud, passing the same target confirmation variables:

```bash
k6 cloud run -e TARGET_URL=https://example.com/ -e ALLOW_HOST=example.com -e CONFIRM_HOST=example.com -e HYDRA_AUTHORIZED=YES -e HYDRA_MAX_VUS=100 load_test_k6.js
```

Keep tokens out of source control, shell history, screenshots, and issue reports. Use your provider's secret manager or secure CI secrets for automation. Review Grafana's current [cloud CLI documentation](https://grafana.com/docs/grafana-cloud/observe-and-act/testing/k6/get-started/run-cloud-tests-from-the-cli/) and pricing before running tests; cloud execution can incur charges.

## High-scale profile (requires provider approval and distributed generators)

Only after written test authorization, provider approval, a documented test plan, monitoring, an emergency stop contact, and a scheduled window are in place:

```bash
k6 run -e TARGET_URL=https://example.com/ -e ALLOW_HOST=example.com -e CONFIRM_HOST=example.com -e HYDRA_AUTHORIZED=YES -e HYDRA_HIGH_SCALE_APPROVED=YES -e HYDRA_PROVIDER_APPROVAL=YES -e HYDRA_MAX_VUS=100000 -e HYDRA_THINK_TIME=10 load_test_k6.js
```

The profile ramps through capacity stages, holds the selected ceiling for three minutes, then ramps down. A single GET endpoint is only a capacity probe—not a simulation of login, database writes, checkout, or complete browser journeys. For 100k VUs, use distributed generators and agree on a request-rate ceiling with the hosting provider before execution.

## What to monitor

- **k6:** VUs, iteration rate, request rate, p95/p99 latency, timeouts, failed requests, and dropped iterations
- **CDN/WAF:** 429/5xx, origin offload, cache hit ratio, and rate-limit events
- **Application:** CPU, memory, worker/thread pools, event-loop lag, and application errors
- **Database:** connections, query latency, pool saturation, locks, and CPU
- **Infrastructure:** bandwidth, open connections, file descriptors, NAT/connection tracking, and autoscaling events

Stop immediately if the provider asks, the site becomes unhealthy, error rates rise sharply, or monitoring is unavailable. A passing homepage test does not prove that every product workflow supports the same number of users.

## Local validation

Start the local mock server:

```bash
python local_test_server.py
```

Then run:

```bash
python kitty_tester.py --url http://127.0.0.1:8080 --allow-host 127.0.0.1 --confirm-host 127.0.0.1 --requests 10 --concurrency 2
```

## Contributing

Issues and pull requests are welcome. Please include reproducible steps, environment details, and sanitized logs. Never post credentials, tokens, customer data, or private target details in public issues.

