import json, pathlib
from datetime import datetime, timedelta, timezone
from validate import violations

c = json.loads((pathlib.Path(__file__).parent / "orders.contract.json").read_text())
now = datetime.now(timezone.utc)
good = {"loaded_at": (now - timedelta(hours=1)).isoformat(),
        "rows": [{"order_id": 1, "customer_id": 10, "amount": 5.5, "status": "NEW"}]}
assert violations(c, good) == []
bad = {"loaded_at": (now - timedelta(hours=48)).isoformat(),
       "rows": [{"order_id": "x", "amount": 5, "status": "NEW", "extra": 1}]}
v = violations(c, bad)
assert len(v) == 4, v  # wrong type, missing customer_id, unexpected column, stale
print("OK: contract accepts good batch, rejects with", len(v), "violations")
