
from pathlib import Path
from datetime import datetime
import csv
import requests
import re

BASE = Path.home() / "ai_factory"
TODAY = datetime.now().strftime("%Y-%m-%d")

inp = BASE / "global_leads" / f"global_domains_{TODAY}.csv"
out = BASE / "global_leads" / f"global_contacts_{TODAY}.csv"

email_regex = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"
rows = []

with open(inp, encoding="utf8") as f:
    r = csv.DictReader(f)
    for row in r:
        website = row["website"]
        email = ""

        try:
            html = requests.get(
                website,
                timeout=5,
                headers={"User-Agent":"Mozilla/5.0"}
            ).text
            found = re.findall(email_regex, html)
            if found:
                email = found[0]
        except Exception:
            pass

        row["email"] = email
        rows.append(row)

with open(out, "w", newline="", encoding="utf8") as f:
    w = csv.DictWriter(
        f,
        fieldnames=["query","company","domain","website","email","status"]
    )
    w.writeheader()
    w.writerows(rows)

print("global contacts created")
print(out)
print("rows:", len(rows))
