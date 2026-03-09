
import requests
import csv
import time
from pathlib import Path

BASE = Path.home() / "ai_factory"
OUT = BASE / "lead_harvester"

OUT.mkdir(exist_ok=True)

queries = [
"marketing agency milan",
"digital agency milan",
"seo agency milan",
"real estate agency milan",
"startup accelerator italy"
]

def search_duckduckgo(q):
    url="https://duckduckgo.com/html/?q="+q.replace(" ","+")
    r=requests.get(url,headers={"User-Agent":"Mozilla/5.0"})
    html=r.text

    links=[]
    parts=html.split('result__a')

    for p in parts[1:]:
        try:
            url=p.split('href="')[1].split('"')[0]
            title=p.split(">")[1].split("<")[0]
            links.append((title,url))
        except:
            pass

    return links[:10]

rows=[]

for q in queries:

    results=search_duckduckgo(q)

    for title,url in results:

        if any(x in url for x in [
        "clutch","sortlist","designrush","goodfirms",
        "linkedin.com","medium.com","wikipedia"
        ]):
            continue

        rows.append({
        "query":q,
        "company":title,
        "website":url,
        "status":"new"
        })

    time.sleep(1)

csv_path=OUT/"company_leads.csv"

with open(csv_path,"w",newline="",encoding="utf8") as f:

    w=csv.DictWriter(f,fieldnames=["query","company","website","status"])
    w.writeheader()
    w.writerows(rows)

print("company leads created")
print(csv_path)
