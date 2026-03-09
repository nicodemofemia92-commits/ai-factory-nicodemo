
from pathlib import Path
import csv
import re

base = Path.home() / "ai_factory" / "lead_harvester_x10"
inp = base / "company_contacts_"  # prefix only

files = sorted(base.glob("company_contacts_*.csv"), reverse=True)
if not files:
    raise SystemExit("Nessun company_contacts_*.csv trovato")

inp = files[0]
out = base / "company_contacts_clean.csv"

bad_patterns = [
    r"\.jpg$", r"\.jpeg$", r"\.png$", r"\.gif$", r"\.webp$",
    r"post-@", r"noreply@", r"no-reply@", r"donotreply@", r"example\.com"
]

def is_good_email(email: str) -> bool:
    e = (email or "").strip().lower()
    if not e or "@" not in e:
        return False
    if any(re.search(p, e) for p in bad_patterns):
        return False
    local, _, domain = e.partition("@")
    if not local or not domain or "." not in domain:
        return False
    return True

rows = []
with open(inp, encoding="utf8") as f:
    r = csv.DictReader(f)
    for row in r:
        email = (row.get("email") or "").strip()
        if is_good_email(email):
            row["email"] = email
            rows.append(row)

with open(out, "w", newline="", encoding="utf8") as f:
    w = csv.DictWriter(f, fieldnames=["query","company","domain","website","email","status"])
    w.writeheader()
    w.writerows(rows)

print("company_contacts_clean.csv creato")
print(out)
print("rows:", len(rows))
