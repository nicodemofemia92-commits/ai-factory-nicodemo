
from pathlib import Path
import csv
import requests
from datetime import datetime

BASE = Path.home() / "ai_factory"
OUTDIR = BASE / "global_leads"
OUTDIR.mkdir(exist_ok=True)

queries = [
"seo agency italy",
"seo agency uk",
"digital marketing agency usa",
"marketing agency canada",
"marketing agency australia",
"seo agency germany",
"seo agency netherlands",
"seo agency spain",
"real estate agency italy",
"real estate agency uk",
"saas startups usa",
"saas companies europe",
"consulting firms london",
"consulting firms new york"
]

rows = []

for q in queries:
    rows.append({
        "query": q,
        "status": "seed"
    })

outfile = OUTDIR / f"global_queries_{datetime.now().strftime('%Y-%m-%d')}.csv"

with open(outfile,"w",newline="",encoding="utf8") as f:
    w = csv.DictWriter(f,fieldnames=["query","status"])
    w.writeheader()
    w.writerows(rows)

print("GLOBAL LEAD ENGINE seeds created")
print(outfile)
