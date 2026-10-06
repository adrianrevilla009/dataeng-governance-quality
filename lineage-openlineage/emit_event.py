"""Emit an OpenLineage START/COMPLETE pair for the job orders_etl: raw_orders -> clean_orders.
Usage: python3 emit_event.py [--url http://localhost:5000] | --dry-run"""
import json, sys, uuid, urllib.request
from datetime import datetime, timezone

PRODUCER = "https://github.com/example/dataeng-governance-quality"
SCHEMA = "https://openlineage.io/spec/2-0-2/OpenLineage.json"


def event(kind, run_id):
    return {
        "eventType": kind,
        "eventTime": datetime.now(timezone.utc).isoformat(),
        "run": {"runId": run_id},
        "job": {"namespace": "orders", "name": "orders_etl"},
        "inputs": [{"namespace": "orders", "name": "raw_orders"}],
        "outputs": [{"namespace": "orders", "name": "clean_orders"}],
        "producer": PRODUCER,
        "schemaURL": SCHEMA,
    }


def main(argv):
    run_id = str(uuid.uuid4())
    events = [event("START", run_id), event("COMPLETE", run_id)]
    if "--dry-run" in argv:
        print(json.dumps(events[1], indent=2))
        return 0
    base = argv[argv.index("--url") + 1] if "--url" in argv else "http://localhost:5000"
    for e in events:
        req = urllib.request.Request(base + "/api/v1/lineage", json.dumps(e).encode(),
                                     {"Content-Type": "application/json"})
        print(e["eventType"], urllib.request.urlopen(req).status)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
