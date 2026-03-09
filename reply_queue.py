import csv
from pathlib import Path
from datetime import date

BASE = Path.home() / "ai_factory"
REPLIES = BASE / "reply_parser" / f"replies_{date.today()}.csv"
OUT = BASE / "reply_parser" / f"reply_queue_{date.today()}.csv"

rows = []

with open(REPLIES) as f:
    r = csv.DictReader(f)
    for row in r:

        email = row["from"]
        subject = row["subject"]

        rows.append({
            "company":"",
            "email":email,
            "subject":subject,
            "status":"new_lead",
            "next_action":"review"
        })

with open(OUT,"w",newline="") as f:
    w = csv.DictWriter(f,fieldnames=[
        "company",
        "email",
        "subject",
        "status",
        "next_action"
    ])
    w.writeheader()
    w.writerows(rows)

print("reply queue created")
print(OUT)
print("rows:",len(rows))
