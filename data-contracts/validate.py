"""Validate a batch and its metadata against a data contract (stdlib).
Usage: python3 validate.py <contract.json> <batch.json>
batch.json: {"loaded_at": ISO-8601 with UTC offset, "rows": [...]}. Exit 1 on violation."""
import json, sys
from datetime import datetime, timezone

TYPES = {"int": int, "float": (int, float), "str": str}


def violations(contract, batch, now=None):
    now = now or datetime.now(timezone.utc)
    out = []
    for i, row in enumerate(batch["rows"]):
        for col, spec in contract["schema"].items():
            if row.get(col) is None:
                if spec["required"]:
                    out.append(f"row {i}: {col} missing")
            elif not isinstance(row[col], TYPES[spec["type"]]):
                out.append(f"row {i}: {col} not {spec['type']}")
        for extra in set(row) - set(contract["schema"]):
            out.append(f"row {i}: unexpected column {extra}")
    sla = contract["sla"]
    age = (now - datetime.fromisoformat(batch["loaded_at"])).total_seconds() / 3600
    if age > sla["freshness_hours"]:
        out.append(f"stale: {age:.0f}h > {sla['freshness_hours']}h")
    if len(batch["rows"]) < sla["min_rows"]:
        out.append("too few rows")
    return out


if __name__ == "__main__":
    v = violations(json.load(open(sys.argv[1])), json.load(open(sys.argv[2])))
    print("\n".join(v) or "contract satisfied")
    sys.exit(1 if v else 0)
