"""PII masking, pseudonymisation and GDPR erasure via crypto-shredding (stdlib).
Each subject has its own key in a key store. Pseudonym = HMAC(subject key, email).
Erasure deletes the key: pseudonyms in analytics tables can no longer be linked back."""
import hashlib, hmac, secrets

KEYS = {}  # subject_id -> key; stands in for a KMS / vault


def mask_email(email):
    user, domain = email.split("@")
    return user[0] + "***@" + domain


def _digest(key, email):
    return hmac.new(key, email.encode(), hashlib.sha256).hexdigest()[:16]


def pseudonym(subject_id, email):
    key = KEYS.setdefault(subject_id, secrets.token_bytes(32))
    return _digest(key, email)


def can_relink(subject_id, email, pseud):
    key = KEYS.get(subject_id)
    return key is not None and hmac.compare_digest(_digest(key, email), pseud)


def erase(subject_id, table):
    KEYS.pop(subject_id, None)  # crypto-shred the pseudonym key
    return [r for r in table if r["subject_id"] != subject_id]  # delete raw rows
