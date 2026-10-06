from mdm import cluster, golden

recs = [
    {"src": "crm", "name": "Ana  Ruiz", "email": "ana@example.com", "postcode": "28001", "phone": "", "updated": "2024-01-01"},
    {"src": "shop", "name": "ana ruiz", "email": "", "postcode": "28001", "phone": "600111222", "updated": "2024-06-01"},
    {"src": "erp", "name": "A. Ruiz", "email": "ANA@example.com", "postcode": "28002", "phone": "", "updated": "2024-09-01"},
    {"src": "crm", "name": "Bo Lee", "email": "bo@example.com", "postcode": "08001", "phone": "", "updated": "2024-02-01"},
]
groups = cluster(recs)
assert len(groups) == 2, [len(g) for g in groups]
g = golden(next(x for x in groups if len(x) == 3))
assert g["phone"] == "600111222" and g["postcode"] == "28002" and g["email"] == "ANA@example.com"
print("OK: 4 source records -> 2 golden records")
