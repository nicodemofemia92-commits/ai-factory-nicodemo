
from pathlib import Path
from datetime import datetime
import csv
import time
import re
import urllib.parse
import requests

BASE = Path.home() / "ai_factory"
TODAY = datetime.now().strftime("%Y-%m-%d")

queries = [
    "marketing agency Milan",
    "digital agency Rome",
    "seo agency Italy",
    "branding studio Milan",
    "real estate agency Milan",
    "marketing agency London",
    "seo consultant UK",
    "branding agency Berlin",
    "digital agency Berlin",
    "startup accelerator Germany",
    "marketing agency New York",
    "seo agency USA",
    "branding agency Toronto",
    "digital agency Toronto",
    "startup accelerator Canada",
    "marketing agency Sydney",
    "seo consultant Australia",
    "branding studio Melbourne",
    "digital agency Dubai",
    "startup accelerator UAE",
]

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

out_dir = BASE / "lead_harvester_x10"
out_dir.mkdir(exist_ok=True)

csv_path = out_dir / f"raw_leads_{TODAY}.csv"

with open(csv_path, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(
        f,
        fieldnames=["query", "company_or_title", "website", "status"]
    )
    w.writeheader()
    w.writerows(rows)

print("raw leads created")
print(csv_path)
print("rows:", len(rows))
