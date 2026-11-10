```markdown
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

```

An enterprise-grade, high-concurrency asynchronous HTTP benchmark, load testing, and WAF-evasion suite engineered for **AI-generated websites** and **server stress benchmarking**. Designed for seamless execution across **Kali Linux, Ubuntu, and Windows**.

---

## ✨ Features & Architecture

* **High-Throughput Asynchronous Engine**: Powered by Python `asyncio` and `aiohttp` connection pooling, allowing execution of 10,000+ requests with minimal system overhead.
* **WAF & Cloudflare 403 Evasion**:
* Rotating modern user agents across Chrome 131, Firefox 133, Safari 18, Edge, and iOS Mobile.
* Browser client-hint emulation (`Sec-Ch-Ua`, `Sec-Fetch-Dest`, `Sec-Fetch-Mode`, `Sec-Fetch-Site`, `Accept-Language`, `Upgrade-Insecure-Requests`).


* **Multi-Path Route Dispersion**: Spreads requests across multiple routes (`/`, `/index.html`, `/#about`, `/#contact`) instead of hitting a static endpoint repeatedly to mitigate firewall rate-limiting rules.
* **Dual Testing Modes**:
* **Mode 1: Normal Mode** — Balanced multi-path testing with controlled concurrency (200 parallel workers) and keep-alive connection pooling.
* **Mode 2: Intense Mode** — High-concurrency stress burst (500 parallel workers) with dynamic cache-busting query strings (`_kc_cb`) and search/social referer injection (`Google`, `X`, `GitHub`).


* **Telemetry & Percentile Auditing**:
* Real-time terminal progress monitor displaying completion percentage, live RPS, and status counters.
* Computes **P50, P90, P95, and P99** latency percentiles alongside min/max/average timings.
* Exports audit results to a timestamped JSON report (`kitty_enterprise_report_<timestamp>.json`).


* **Cross-Platform Tooling**: Includes ready-to-run integration configurations for **Locust** (`locustfile.py`), **k6** (`load_test_k6.js`), and a standalone mock test server (`local_test_server.py`).

---

## 📁 Repository Structure

```text
├── kitty_tester.py       # Main enterprise load testing engine
├── run_kali.sh           # Automated setup & launcher for Kali Linux / Ubuntu / macOS
├── run_windows.bat       # Automated setup & launcher for Windows
├── local_test_server.py  # Local async mock server ([http://127.0.0.1:8080](http://127.0.0.1:8080))
├── locustfile.py         # Distributed load testing configuration for Locust
├── load_test_k6.js       # Threshold-gated performance script for k6
├── requirements.txt      # Python dependencies (aiohttp, colorama, locust)
└── README.md             # Project documentation

```

---

## 🚀 Quick Start

### 🐉 Kali Linux / Ubuntu / macOS

Make the launch script executable and start the suite:

```bash
git clone https://github.com/psychspy7/hydra.git
cd hydra
chmod +x run_kali.sh
./run_kali.sh

```

*(The script automatically raises file descriptor limits via `ulimit -n 65535`, initializes a virtual environment, installs dependencies, and launches the engine.)*

---

### 🪟 Windows (Command Prompt / PowerShell)

1. Clone or download the repository:
```cmd
git clone https://github.com/psychspy7/hydra.git
cd hydra

```


2. Run the automated Windows launcher:
```cmd
run_windows.bat

```


*(Or execute manually in PowerShell: `python kitty_tester.py` or `py kitty_tester.py`)*

---

## 💻 Manual & CLI Usage

### Direct Script Execution

```bash
# Install dependencies
pip install -r requirements.txt

# Interactive terminal menu (Banner, legal gate, prompts)
python3 kitty_tester.py

# Direct command-line execution (10,000 requests, Intense Mode)
python3 kitty_tester.py --url [https://example.com](https://example.com) --mode 2 --requests 10000

# Custom concurrency override (e.g., 300 concurrent workers)
python3 kitty_tester.py --url [https://example.com](https://example.com) --mode 2 --requests 10000 --concurrency 300

```

### Local Offline Testing

Before running external tests, benchmark the load engine on your local machine using the built-in mock server:

1. Launch the local mock server in terminal 1:
```bash
python3 local_test_server.py

```


2. Run the tester targeting the mock server in terminal 2:
```bash
python3 kitty_tester.py --url [http://127.0.0.1:8080](http://127.0.0.1:8080) --mode 2 --requests 10000

```



### Running with Locust & k6

* **Locust**:
```bash
locust -f locustfile.py --host=[https://example.com](https://example.com)

```


Access the web interface at `http://127.0.0.1:8089`.
* **k6**:
```bash
k6 run load_test_k6.js

```



---

## ⚠️ Disclaimer & Legal Notice

This utility is strictly intended for **educational, research, and authorized capacity benchmarking** purposes on infrastructure you personally own or have explicit written authorization to test. Unauthorized stress testing against third-party infrastructure may violate terms of service and applicable cyber legislation.

**made by kitty corp** | [https://thekittycorp.com/ - support us 🩷](https://thekittycorp.com/)

```

```
