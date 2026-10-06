"""Tiny expectation runner (stdlib). Exits 1 when any check fails, so a pipeline stops.
Usage: python3 run_checks.py <data.csv> [checks.json]"""
import csv, json, sys


def evaluate(rows, check):
    t, col = check["type"], check.get("column")
    vals = [r[col] for r in rows] if col else []
    if t == "row_count_min":
        return len(rows) >= check["value"]
    if t == "not_null":
        return all(v != "" for v in vals)
    if t == "unique":
        return len(set(vals)) == len(vals)
    if t == "min":
        return all(float(v) >= check["value"] for v in vals if v != "")
    if t == "accepted_values":
        return all(v in check["values"] for v in vals)
    raise ValueError(f"unknown check {t}")


def main(data, spec_path="checks.json"):
    rows = list(csv.DictReader(open(data)))
    spec = json.load(open(spec_path))
    failed = 0
    for c in spec["checks"]:
        ok = evaluate(rows, c)
        failed += not ok
        print(("PASS " if ok else "FAIL ") + json.dumps(c))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:3]))
