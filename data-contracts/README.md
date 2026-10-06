# data-contracts

A versioned JSON contract `orders.contract.json`, a validator `validate.py`, and `verify.py` that checks a good and a bad batch.

## Goal

Express a producer/consumer agreement as a versioned contract (schema, owner, SLA) and enforce it on each batch.

## Run it

```bash
python3 verify.py
python3 validate.py orders.contract.json batch.json   # your own batch file
```

Expected: `verify.py` prints `OK: contract accepts good batch, rejects with 4 violations`. `validate.py` prints `contract satisfied` or one line per violation and exits 1. `batch.json` is not in the repo; the format is `{"loaded_at": "<ISO-8601 with UTC offset>", "rows": [...]}`.

## What it proves

- Schema (types, required fields, no unexpected columns) and SLA (freshness in hours, minimum rows) are checked mechanically.
- The bad batch in `verify.py` yields exactly four violations: wrong type, missing `customer_id`, unexpected column and a stale load (48 h against a 24 h limit).
- The contract is a file with a name, version (1.2.0) and owner (`sales-team`), so changes can be reviewed like code.

A plain JSON format is used instead of the Open Data Contract Standard to stay dependency-free; the fields map onto it.

## Trade-offs

- No compatibility rules between contract versions (breaking against additive) are enforced.
- Semantic guarantees (what a value means) cannot be expressed in this schema.
- Only the types `int`, `float` and `str` are supported.

## When not to use it

- When many teams and warehouses are involved; use ODCS with a tool such as datacontract-cli.
