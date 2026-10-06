# catalog-datahub

A DataHub ingestion recipe (`recipe.yml`), a Postgres source defined by `init.sql` and `compose.yml`, and an offline check of both.

## Goal

Ingest table and column metadata of a Postgres source into the DataHub catalog, with table descriptions and a PII hint on `customers.email`.

## Run it

```bash
python3 verify.py                       # offline recipe/DDL check
cp .env.example .env && docker compose --env-file .env up -d
pip install 'acryl-datahub[postgres]==0.14.1' && datahub docker quickstart
ORDERS_DB_PASSWORD=change-me datahub ingest -c recipe.yml
datahub docker nuke && docker compose down -v   # destroy step
```

Expected: `verify.py` prints `OK: recipe valid, documented tables: ['customers', 'orders']`. A successful ingest would show the `orders` database tables in the DataHub UI.

## What it proves

- A catalog is filled by an ingestion recipe with a source (`postgres`) and a sink (`datahub-rest` on port 8080), not by hand.
- `init.sql` puts `COMMENT ON TABLE` on both tables and `COMMENT ON COLUMN customers.email IS 'PII'`, which are the descriptions the ingestion reads.
- The password is read from `ORDERS_DB_PASSWORD` in the recipe; `verify.py` fails if it is hard-coded.

Not run end to end: the DataHub quickstart is a large multi-container stack and was not started, so the ingestion and the catalog UI were not checked. Only `verify.py` was run.

## Trade-offs

- DataHub is heavy to run locally; lighter catalogs (OpenMetadata, Marquez) exist.
- Ingestion is pull-based and periodic, so metadata can lag the source.
- The PII hint is only a text comment, not a governed tag or classification.

## When not to use it

- For a handful of tables, where a documented schema in git is enough.
