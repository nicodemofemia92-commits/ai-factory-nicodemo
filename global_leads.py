import csv
from pathlib import Path
from datetime import date

BASE = Path.home() / "ai_factory"
OUT = BASE / "global_leads"

OUT.mkdir(exist_ok=True)

queries = [
"marketing agency london",
"marketing agency new york",
"seo agency berlin",
"seo agency toronto",
"digital agency milan",
"digital agency paris",
"growth agency san francisco",
"growth agency amsterdam",
"startup accelerator europe",
"startup accelerator usa",
"ai startup london",
"ai startup berlin",
"b2b saas startup usa",
"b2b saas startup europe",
"consulting firm london",
"consulting firm new york",
"consulting firm berlin",
"consulting firm singapore",
"startup founders berlin",
"startup founders london",
]

out = OUT / f"global_queries_{date.today()}.csv"

with open(out,"w",newline="") as f:
    w = csv.writer(f)
    w.writerow(["query"])
    for q in queries:
        w.writerow([q])

print("GLOBAL LEAD ENGINE seeds created")
print(out)
