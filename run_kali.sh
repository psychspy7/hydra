#!/usr/bin/env bash
clear
echo "=========================================================="
echo "         KITTY CORP ADVANCED ENTERPRISE LOAD SUITE          "
echo "                made by kitty corp                        "
echo "        https://thekittycorp.com/ - support us 🩷         "
echo "=========================================================="
ulimit -n 65535 2>/dev/null || true
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
fi
source .venv/bin/activate
pip install --quiet --upgrade pip
pip install --quiet -r requirements.txt
python3 kitty_tester.py "$@"
