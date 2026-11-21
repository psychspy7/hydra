#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

echo "Hydra — authorized smoke test"
echo "This launcher does not run a high-concurrency test."
echo

if ! command -v python3 >/dev/null 2>&1; then
  echo "Python 3 is required." >&2
  exit 1
fi

if [ ! -d ".venv" ]; then
  python3 -m venv .venv
fi
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

exec python3 kitty_tester.py "$@"
