
from pathlib import Path
from datetime import datetime
import csv
import urllib.parse
import re

BASE = Path.home() / "ai_factory"
TODAY = datetime.now().strftime("%Y-%m-%d")

inp = BASE / "global_leads" / f"raw_global_leads_{TODAY}.csv"
out = BASE / "global_leads" / f"global_domains_{TODAY}.csv"

skip = [
    "duckduckgo","clutch","sortlist","designrush","goodfirms",
    "linkedin","medium","wikipedia","facebook","instagram","youtube",
    "yelp","agencyspotter","producthunt"
]

def get_domain(url):
    try:
        if "uddg=" in url:
            url = urllib.parse.unquote(url.split("uddg=")[1])
        p = urllib.parse.urlparse(url)
        d = p.netloc.lower()
        d = re.sub("^www\\.","",d)
        return d
    except:
        return ""

rows = []
seen = set()

with open(inp, encoding="utf8") as f:
    r = csv.DictReader(f)
    for row in r:
        domain = get_domain(row["website"])
        if not domain:
            continue
        if any(x in domain for x in skip):
            continue
        if domain in seen:
            continue
        seen.add(domain)
        rows.append({
            "query": row["query"],
            "company": row["company_or_title"],
            "domain": domain,
            "website": "https://" + domain,
            "status": "new"
        })

with open(out, "w", newline="", encoding="utf8") as f:
    w = csv.DictWriter(f, fieldnames=["query","company","domain","website","status"])
    w.writeheader()
    w.writerows(rows)

print("global domains created")
print(out)
print("rows:", len(rows))
