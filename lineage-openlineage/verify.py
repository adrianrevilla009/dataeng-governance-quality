"""Offline check: emitted events are well formed. Full check needs Docker (see README)."""
from emit_event import event

e = event("COMPLETE", "00000000-0000-0000-0000-000000000001")
assert e["inputs"] and e["outputs"] and e["run"]["runId"] and e["job"]["name"]
assert e["eventType"] in ("START", "COMPLETE") and e["schemaURL"].endswith("OpenLineage.json")
print("OK: OpenLineage event well formed")
