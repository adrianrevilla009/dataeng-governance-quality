"""Master-data matching and golden record (stdlib).
Match rule: same normalised email (exact) OR same normalised name + same postcode.
Survivorship: most recently updated non-empty value wins per field."""
import re


def norm(s):
    return re.sub(r"[^a-z0-9]", "", (s or "").lower())


def is_match(a, b):
    if norm(a["email"]) and norm(a["email"]) == norm(b["email"]):
        return True
    return bool(norm(a["name"])) and norm(a["name"]) == norm(b["name"]) and norm(a["postcode"]) == norm(b["postcode"])


def cluster(records):
    groups = []
    for r in records:
        hits = [g for g in groups if any(is_match(r, m) for m in g)]
        merged = [r] + [m for g in hits for m in g]
        groups = [g for g in groups if g not in hits] + [merged]
    return groups


def golden(group):
    out = {}
    for r in sorted(group, key=lambda r: r["updated"]):  # oldest first, newer overwrites
        for k, v in r.items():
            if v:
                out[k] = v
    return out
