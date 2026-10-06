# lineage-openlineage

A script that builds OpenLineage START and COMPLETE events for the job `orders_etl`, a Marquez compose file, and an offline check of the event shape.

## Goal

Emit OpenLineage run events for a job with one input (`raw_orders`) and one output (`clean_orders`) and see the lineage graph in Marquez.

## Run it

```bash
python3 verify.py                       # offline: event shape only
python3 emit_event.py --dry-run         # prints the COMPLETE event as JSON
docker compose -f compose.yml up -d     # Marquez UI on http://localhost:3000
python3 emit_event.py                   # posts START and COMPLETE to :5000
docker compose -f compose.yml down -v   # destroy step
```

Expected: `verify.py` prints `OK: OpenLineage event well formed`. `emit_event.py` prints one line per event (`START`, `COMPLETE`) with the HTTP status returned by Marquez.

## What it proves

- Lineage is just events: `emit_event.py` sets event type, run id, job, inputs, outputs and producer, and nothing else.
- Both events share one run id, so the backend can tie START to COMPLETE.
- Marquez, pinned to 0.49.0 with Postgres 14.13 in `compose.yml`, is the backend that should draw `raw_orders -> orders_etl -> clean_orders`.

Not run end to end: the Marquez stack was not started, so posting events and the graph in the UI were not checked. Only `verify.py` and the dry run were run.

## Trade-offs

- Hand-written events show the model; real pipelines use the Spark, Airflow or dbt integrations.
- No dataset facets (schema, column lineage) are sent.
- The compose file uses a throwaway database password and is meant for local use only.

## When not to use it

- In production, where events should come from the OpenLineage integration of your orchestrator, not from a hand-written script.
