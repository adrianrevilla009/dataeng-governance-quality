# mdm-golden-record

`mdm.py` with matching, clustering and survivorship functions, and `verify.py` that merges four customer records from three sources.

## Goal

Merge duplicate customer records from several sources into one golden record using explicit matching and survivorship rules.

## Run it

```bash
python3 verify.py
```

Expected: `OK: 4 source records -> 2 golden records`.

## What it proves

- Matching: two records match if the normalised email is equal and not empty, or the normalised name and postcode are both equal. Clusters grow transitively: in `verify.py` the ERP record joins the CRM record through its email, and the shop record joins through name and postcode.
- Survivorship: per field, the most recently updated non-empty value wins, so the golden record gets the phone from the shop, the postcode `28002` from the ERP and the email `ANA@example.com`.
- Bo Lee stays a separate record, giving two golden records from four inputs.

## Trade-offs

- Exact rules are explainable but miss typos; probabilistic matching (Splink, Zingg) trades explainability for recall.
- Last-write-wins ignores source trust; real MDM ranks sources per field.
- Pairwise comparison is O(n^2); real systems use blocking.

## When not to use it

- For large volumes or fuzzy matching; use a dedicated MDM or record-linkage library.
