#!/usr/bin/env bash
# Good data must pass (exit 0); bad data must fail (exit 1).
set -u
cd "$(dirname "$0")"
python3 run_checks.py orders.csv >/dev/null || { echo "good data failed"; exit 1; }
if python3 run_checks.py orders_bad.csv >/dev/null; then echo "bad data passed"; exit 1; fi
echo "OK: quality gate passes good data and blocks bad data"
