from pii import mask_email, pseudonym, can_relink, erase, KEYS

assert mask_email("ana@example.com") == "a***@example.com"
p1, p2 = pseudonym("c1", "ana@example.com"), pseudonym("c2", "bo@example.com")
assert p1 == pseudonym("c1", "ana@example.com") and p1 != p2, "stable per subject, distinct across subjects"
assert can_relink("c1", "ana@example.com", p1)
raw = [{"subject_id": "c1", "email": "ana@example.com"}, {"subject_id": "c2", "email": "bo@example.com"}]
raw = erase("c1", raw)
assert [r["subject_id"] for r in raw] == ["c2"] and "c1" not in KEYS
assert not can_relink("c1", "ana@example.com", p1), "erased subject must not be relinkable"
print("OK: masking, stable pseudonyms, GDPR erase flow")
