
import os,requests
from datetime import datetime
from pathlib import Path

today=datetime.now().strftime("%Y-%m-%d")
base=Path.home()/ "ai_factory"

queries=[
"marketing agency milan",
"seo consultant italy",
"digital agency rome"
]

results=[]

for q in queries:
    results.append(f"Search Google: {q}")

folder=base/"lead_scraper"
folder.mkdir(exist_ok=True)

path=folder/f"leads_{today}.txt"
path.write_text("\n".join(results))

print("lead scraper generated:",path)
