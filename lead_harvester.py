from pathlib import Path

import csv
import os
import re
import time
import urllib.parse
from datetime import datetime

import requests

BASE = Path.home() / "ai_factory"
TODAY = datetime.now().strftime("%Y-%m-%d")

def latest_text(folder, pattern):
    p = BASE / folder
    if not p.exists():
        return ""
    files = sorted(p.glob(pattern), reverse=True)
    if not files:
        return ""
    try:
        return files[0].read_text()
    except Exception:
        return ""

def extract_queries(text, limit=25):
    out = []
    for line in text.splitlines():
        s = line.strip()
        if not s:
            continue
        s = re.sub(r'^[\-\•\d\.\)\s]+', '', s).strip()
        if len(s) < 6:
            continue
        if any(k in s.lower() for k in [
            "marketing agency", "seo consultant", "branding", "digital agency",
            "real estate", "web design", "growth consultant", "startup founder",
            "business consultant", "lead generation", "agency", "consultant"
        ]):
            out.append(s)
    # dedupe
    seen = set()
    clean = []
    for q in out:
        k = q.lower()
        if k not in seen:
            seen.add(k)
            clean.append(q)
    if not clean:
        clean = [
            "marketing agency Milan",
            "seo consultant Italy",
            "branding studio Milan",
            "real estate agency Milan",
            "digital agency Rome",
        ]
    return clean[:limit]

def ddg_search(query, max_results=8):
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

    # very simple extraction of result links/titles
    results = []
    pattern = re.compile(
        r'<a[^>]+class="[^"]*result__a[^"]*"[^>]+href="([^"]+)"[^>]*>(.*?)</a>',
        re.I | re.S
    )
    for m in pattern.finditer(html):
        href = m.group(1)
        title = re.sub(r"<.*?>", "", m.group(2))
        title = re.sub(r"\s+", " ", title).strip()

        # decode duckduckgo redirect
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

lead_machine = latest_text("leads", "lead_machine_*.txt")
client_hunter = latest_text("client_hunter", "client_hunter_*.txt")
harvester = latest_text("harvester", "harvester_*.txt")

queries = []
for source in [lead_machine, client_hunter, harvester]:
    queries.extend(extract_queries(source, limit=30))

# dedupe again
seen = set()
queries_clean = []
for q in queries:
    if q.lower() not in seen:
        seen.add(q.lower())
        queries_clean.append(q)

rows = []
for query in queries_clean[:20]:
    results = ddg_search(query, max_results=8)
    for title, url in results:
        rows.append({
            "query": query,
            "company_or_title": title,
            "website": url,
            "contact_page": "",
            "linkedin": "",
            "status": "to-review",
            "notes": "",
        })
    time.sleep(1)

out_dir = BASE / "lead_harvester"
out_dir.mkdir(exist_ok=True)

csv_path = out_dir / f"lead_harvester_{TODAY}.csv"
txt_path = out_dir / f"lead_harvester_{TODAY}.txt"

with open(csv_path, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(
        f,
        fieldnames=["query", "company_or_title", "website", "contact_page", "linkedin", "status", "notes"]
    )
    w.writeheader()
    w.writerows(rows)

summary = [
    f"LEAD HARVESTER",
    f"Date: {TODAY}",
    f"",
    f"Queries used: {len(queries_clean[:20])}",
    f"Rows found: {len(rows)}",
    f"",
    f"CSV:",
    str(csv_path),
    f"",
    f"How to use:",
    f"1. Open the CSV",
    f"2. Keep only real companies",
    f"3. Fill contact_page / linkedin",
    f"4. Status -> ready / contacted / ignored",
]
txt_path.write_text("\n".join(summary), encoding="utf-8")

print("lead_harvester creato")
print("CSV:", csv_path)
print("TXT:", txt_path)
print("Rows:", len(rows))
