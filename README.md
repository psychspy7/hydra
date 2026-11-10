```Markdown
# Kitty Corp Enterprise Load & WAF Bypass Suite 🐾

```text
    =========================================================================
                         /\_/\           /\_/\   
                        ( o.o )         ( ^.^ )  
                         > ^ <           > w <   
                       /|     |\       /|     |\ 
                      (_|     |_)     (_|     |_)
          _  _____ _____ _______   __   ____ ___  ____  ____  
         | |/ /_ _|_   _|_   _\ \ / /  / ___/ _ \|  _ \|  _ \ 
         | ' / | |  | |   | |  \ V /  | |  | | | | |_) | |_) |
         | . \ | |  | |   | |   | |   | |__| |_| |  _ <|  __/ 
         |_|\_\___| |_|   |_|   |_|    \____\___/|_| \_\_|    

                        [ made by kitty corp ]
               [https://thekittycorp.com/](https://thekittycorp.com/) - support us 🩷
    =========================================================================
An enterprise-grade, high-concurrency asynchronous HTTP benchmark, stress-testing, and WAF-evasion utility engineered for AI-generated websites and infrastructure resilience audits. Built for native execution across Windows, Kali Linux, and Ubuntu.

⚡ Quick Start: One-Click Execution
🪟 Windows Setup & Execution
Option A: Windows PowerShell (Requires .\)
PowerShell
git clone [https://github.com/psychspy7/hydra.git](https://github.com/psychspy7/hydra.git)
cd hydra
.\run_windows.bat
Note for PowerShell users: Windows PowerShell does not execute local scripts without the relative path prefix. Always use .\run_windows.bat instead of just run_windows.bat.

Option B: Windows Command Prompt (CMD)
DOS
git clone [https://github.com/psychspy7/hydra.git](https://github.com/psychspy7/hydra.git)
cd hydra
run_windows.bat
Option C: Direct Python Execution (Windows)
If running manually without the batch launcher:

PowerShell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python kitty_tester.py
🐉 Linux Setup & Execution (Kali Linux / Ubuntu / Debian)
Bash
git clone [https://github.com/psychspy7/hydra.git](https://github.com/psychspy7/hydra.git)
cd hydra
chmod +x run_kali.sh
./run_kali.sh
Direct Python Execution (Linux)
Bash
ulimit -n 65535
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 kitty_tester.py
🛠️ How It Works & Architecture
The testing suite uses Python's asynchronous I/O engine (asyncio and aiohttp) with a custom TCP connection pool to generate controlled high-volume web traffic without exhausting local memory or CPU.

1. WAF & Bot-Mitigation Evasion
Many modern hosting platforms and web application firewalls (Cloudflare, AWS WAF, Akamai) drop benchmark traffic with HTTP 403 Forbidden if basic scripted request patterns are detected. The engine mitigates this via:

Rotating Modern User-Agents: Rotates desktop and mobile signatures across Chrome 131, Firefox 133, Safari 18, and Edge.

Client Hints & Realistic Headers: Emulates real browser navigation by including Sec-Ch-Ua, Sec-Fetch-Dest, Sec-Fetch-Mode, Sec-Fetch-Site, Accept-Language, and Upgrade-Insecure-Requests.

Multi-Path Crawl Distribution: Spreads traffic across common functional site paths (/, /index.html, /#about, /#contact) instead of repeatedly hitting a single static path.

2. Dual Testing Modes
Mode 1: Normal Mode

Target: 10,000 requests.

Concurrency: 200 concurrent worker tasks.

Behavior: Persistent HTTP keep-alive pooling with gentle pacing to evaluate sustained normal user traffic.

Mode 2: Intense Mode

Target: 10,000 requests.

Concurrency: 500 concurrent worker tasks.

Behavior: Zero artificial delay combined with dynamic cache-busting query tokens (_kc_cb) and randomized search/social referers (Google, X, GitHub) to force origin server processing and evaluate DDoS resilience.

💻 CLI Commands & Local Testing
Direct Command-Line Arguments
Bypass interactive prompts by passing arguments directly:

Bash
# Windows (PowerShell)
python kitty_tester.py --url [https://your-website.com](https://your-website.com) --mode 1 --requests 5000

# Linux
python3 kitty_tester.py --url [https://your-website.com](https://your-website.com) --mode 2 --requests 10000 --concurrency 400
Local Mock Server Testing (Safe Sandbox)
To benchmark your local network adapter or verify script execution before targeting external servers:

Start the local mock server:

Bash
python local_test_server.py
(Runs on http://127.0.0.1:8080)

In a second terminal, launch the load tester against the mock server:

Bash
python kitty_tester.py --url [http://127.0.0.1:8080](http://127.0.0.1:8080) --mode 2 --requests 10000
Third-Party Tool Integrations
Locust: Run distributed user load tests via the web interface:

Bash
locust -f locustfile.py --host=[https://your-website.com](https://your-website.com)
(Dashboard runs at http://127.0.0.1:8089)

k6: Run threshold-gated performance tests:

Bash
k6 run load_test_k6.js
📊 Telemetry & Audit Reports
During runtime, the console displays a live dynamic progress bar with completed request tallies, real-time requests-per-second (RPS), and error counters.

Upon test completion, the engine calculates:

Throughput: Total execution duration and average requests/sec.

Latency Percentiles: Min, Average, Max, P50 (median), P90, P95, and P99 response times in milliseconds.

Status Code Breakdown: Aggregated HTTP response codes (2xx, 3xx, 4xx, 5xx).

JSON Export: Automatically writes full telemetry to kitty_enterprise_report_<timestamp>.json for CI/CD integration.

📁 Repository Structure
Plaintext
├── kitty_tester.py       # Asynchronous load testing engine & WAF evasion logic
├── run_windows.bat       # Windows launcher (initializes .venv, installs deps, runs suite)
├── run_kali.sh           # Linux launcher (sets ulimit, configures environment, runs suite)
├── local_test_server.py  # Standalone local async mock server for safe benchmarking
├── locustfile.py         # Locust scenario configuration
├── load_test_k6.js       # k6 performance script with latency threshold checks
├── requirements.txt      # Python dependencies (aiohttp, colorama, locust)
└── README.md             # Project documentation
⚠️ Disclaimer
This utility is developed strictly for educational, research, and authorized capacity benchmarking purposes on systems you own or have explicit written permission to test. Unauthorized load testing against third-party web services may violate terms of service and relevant cybersecurity regulations.

made by kitty corp | https://thekittycorp.com/ - support us 🩷
