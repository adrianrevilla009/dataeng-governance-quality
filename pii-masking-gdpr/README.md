# pii-masking-gdpr

`pii.py` with email masking, per-subject pseudonyms and an erasure function, plus `verify.py` that exercises them.

## Goal

Show masking, pseudonymisation and a GDPR right-to-erasure flow on a tiny customer table.

## Run it

```bash
python3 verify.py
```

Expected: `OK: masking, stable pseudonyms, GDPR erase flow`.

## What it proves

- Masking turns `ana@example.com` into `a***@example.com`; it is for display only.
- A pseudonym is an HMAC-SHA256 of the email under a per-subject key, so it is stable for one subject and differs between subjects, which keeps joins possible in analytics.
- `erase()` deletes the subject's raw rows and the subject's key (crypto-shredding); after that `can_relink()` returns false for the old pseudonym.

The keys live in the in-memory dict `KEYS`, standing in for a KMS. No real credentials are used.

## Trade-offs

- Pseudonymised data is still personal data under GDPR while the key exists.
- Backups, logs and copies must be covered by the same key scheme to make erasure real.
- The pseudonym is truncated to 16 hex characters, which is fine for a demo but short for large datasets.

## When not to use it

- In production with the in-memory key store; use a KMS or vault, and get legal review for retention rules.
