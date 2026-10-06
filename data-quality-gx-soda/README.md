# data-quality-gx-soda

A small stdlib check runner driven by `checks.json`, two CSV files (good and bad), and the same rules written in SodaCL.

## Goal

Show a quality gate that stops a pipeline: declarative checks (not null, unique, minimum, accepted values, row count) run against a dataset and the process exits with 1 if any fails.

## Run it

```bash
bash verify.sh
python3 run_checks.py orders_bad.csv   # shows FAIL lines, exit code 1
```

Expected: `verify.sh` prints `OK: quality gate passes good data and blocks bad data`. For `orders_bad.csv` the runner prints `PASS` for `row_count_min` and `FAIL` for `not_null`, `unique`, `min` and `accepted_values`. For `orders.csv` all five lines are `PASS`.

## What it proves

- Checks are data in `checks.json`, separate from the runner `run_checks.py`, the same split as Great Expectations suites and Soda check files.
- A failing check changes the exit code, so an orchestrator or CI job stops before bad data is published; `verify.sh` asserts exit 0 for `orders.csv` and exit 1 for `orders_bad.csv`.
- `checks.soda.yml` states the same five rules in SodaCL.

## Trade-offs

- Great Expectations and Soda are heavy installs, so the runnable part is a small runner that mimics the model. The SodaCL file was not executed (it needs soda-core and a data source), and no Great Expectations suite is included.
- Real tools add profiling, data docs, many connectors and result stores; this runner has none of that.
- Checks cover one batch only, not drift over time.

## When not to use it

- In production; use Great Expectations or Soda Core directly. This runner is for understanding the gate pattern.
