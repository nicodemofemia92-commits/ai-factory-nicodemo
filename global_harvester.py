
from pathlib import Path
from datetime import datetime
import csv
import time
import re
import urllib.parse
import requests

BASE = Path.home() / "ai_factory"
TODAY = datetime.now().strftime("%Y-%m-%d")

seed_file = BASE / "global_leads" / f"global_queries_{TODAY}.csv"
out_dir = BASE / "global_leads"
out_dir.mkdir(exist_ok=True)

queries = []
with open(seed_file, encoding="utf8") as f:
    r = csv.DictReader(f)
    for row in r:
        q = (row.get("query") or "").strip()
        if q:
            queries.append(q)

def ddg_search(query, max_results=12):
    url = "https://html.duckduckgo.com/html/"
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {"q": query}
    try:
        r = requests.post(url, headers=headers, data=data, timeout=20)
        html = r.text
    except Exception:
        return []

    results = []
    pattern = re.compile(
        r'<a[^>]+class="[^"]*result__a[^"]*"[^>]+href="([^"]+)"[^>]*>(.*?)</a>',
        re.I | re.S
    )

    for m in pattern.finditer(html):
        href = m.group(1)
        title = re.sub(r"<.*?>", "", m.group(2))
        title = re.sub(r"\s+", " ", title).strip()

        if "duckduckgo.com/l/?" in href:
            parsed = urllib.parse.urlparse(href)
            qs = urllib.parse.parse_qs(parsed.query)
            if "uddg" in qs:
                href = urllib.parse.unquote(qs["uddg"][0])

        if href.startswith("http"):
            results.append((title, href))
        if len(results) >= max_results:
            break

    return results

rows = []
for query in queries:
    results = ddg_search(query, max_results=12)
    for title, url in results:
        rows.append({
            "query": query,
            "company_or_title": title,
            "website": url,
            "status": "to-review"
        })
    time.sleep(1)

csv_path = out_dir / f"raw_global_leads_{TODAY}.csv"

with open(csv_path, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(
        f,
        fieldnames=["query", "company_or_title", "website", "status"]
    )
    w.writeheader()
    w.writerows(rows)

print("raw global leads created")
print(csv_path)
print("rows:", len(rows))
