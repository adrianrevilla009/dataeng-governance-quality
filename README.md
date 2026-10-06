# dataeng-governance-quality

Six small labs on data governance and quality: a failing quality gate, lineage events, catalog ingestion, PII masking with GDPR erasure, data contracts and master-data matching. All of them use the same tiny Orders and customers data.

## What is inside

| Folder | What it shows | Run |
| --- | --- | --- |
| [`data-quality-gx-soda`](./data-quality-gx-soda) | Declarative checks that return exit code 1 on bad data | `bash verify.sh` |
| [`lineage-openlineage`](./lineage-openlineage) | OpenLineage START/COMPLETE events for Marquez | `python3 verify.py` |
| [`catalog-datahub`](./catalog-datahub) | DataHub ingestion recipe for a Postgres source | `python3 verify.py` |
| [`pii-masking-gdpr`](./pii-masking-gdpr) | Masking, pseudonyms and erasure by deleting the key | `python3 verify.py` |
| [`data-contracts`](./data-contracts) | Versioned JSON contract with schema and SLA checks | `python3 verify.py` |
| [`mdm-golden-record`](./mdm-golden-record) | Matching rules and survivorship into one golden record | `python3 verify.py` |

## Prerequisites

- Python 3.10 or newer (standard library only, no packages to install).
- Docker with Compose, only for the Marquez stack in `lineage-openlineage` and the source database in `catalog-datahub`.
- `acryl-datahub[postgres]==0.14.1` and its quickstart, only if you want to run the DataHub ingestion.

## How to read it

Start with `data-quality-gx-soda`, then `data-contracts`; both are pure Python and run in a second. The Docker-based folders say in their own README which parts were not run end to end.
