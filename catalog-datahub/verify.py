"""Offline check: the recipe has source+sink, and every table in init.sql is documented."""
import re, pathlib

here = pathlib.Path(__file__).parent
recipe = (here / "recipe.yml").read_text()
assert re.search(r"^source:", recipe, re.M) and re.search(r"^sink:", recipe, re.M)
assert "${ORDERS_DB_PASSWORD}" in recipe, "password must come from env"
sql = (here / "init.sql").read_text()
tables = re.findall(r"CREATE TABLE (\w+)", sql)
missing = [t for t in tables if f"COMMENT ON TABLE {t} " not in sql]
assert not missing, f"undocumented tables: {missing}"
print("OK: recipe valid, documented tables:", tables)
