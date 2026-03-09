
from pathlib import Path
import csv
import io
import re
import requests
from urllib.parse import urlparse

BASE = Path.home() / "ai_factory"
OUT = BASE / "engine_dataset"
OUT.mkdir(exist_ok=True)

CSV_URL = "https://raw.githubusercontent.com/notpeter/crunchbase-data/master/companies.csv"
STRIPE = "https://buy.stripe.com/test_5kQ8wH3WofTc56Z8vdcs800"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept-Language": "en-US,en;q=0.9",
}

EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
BAD_EMAIL_BITS = [".png",".jpg",".jpeg",".gif",".svg","@2x","@3x","noreply@","no-reply@","donotreply@","example.com"]

def clean_email(e):
    e = (e or "").strip().lower()
    if not e or "@" not in e:
        return ""
    if any(x in e for x in BAD_EMAIL_BITS):
        return ""
    local, _, domain = e.partition("@")
    if not local or not domain or "." not in domain:
        return ""
    return e

def norm_url(u):
    u = (u or "").strip()
    if not u:
        return ""
    if not u.startswith(("http://","https://")):
        u = "https://" + u
    return u

def domain_of(u):
    try:
        d = urlparse(u).netloc.lower()
        if d.startswith("www."):
            d = d[4:]
        return d
    except Exception:
        return ""

print("downloading dataset...")
r = requests.get(CSV_URL, headers=HEADERS, timeout=30)
r.raise_for_status()

text = r.content.decode("utf-8", errors="ignore")
reader = csv.DictReader(io.StringIO(text))

wanted_words = [
    "marketing", "advertising", "analytics", "software", "saas", "internet",
    "enterprise", "consulting", "developer", "business", "search"
]
wanted_countries = {"USA","GBR","CAN","AUS","DEU","FRA","ESP","NLD","IRL","SGP","ITA"}

rows = []
seen_domains = set()

for row in reader:
    homepage = norm_url(row.get("homepage_url",""))
    if not homepage:
        continue

    domain = domain_of(homepage)
    if not domain or domain in seen_domains:
        continue

    category = (row.get("category_list","") or "").lower()
    country = (row.get("country_code","") or "").upper()

    if country and country not in wanted_countries:
        continue

    if category and not any(w in category for w in wanted_words):
        continue

    seen_domains.add(domain)
    rows.append({
        "company": row.get("name","").strip() or domain,
        "website": homepage,
        "domain": domain,
        "category": row.get("category_list","").strip(),
        "country": country,
    })

rows = rows[:500]

sites_path = OUT / "company_sites.csv"
with open(sites_path, "w", newline="", encoding="utf8") as f:
    w = csv.DictWriter(f, fieldnames=["company","website","domain","category","country"])
    w.writeheader()
    w.writerows(rows)

print("candidate sites:", len(rows))

contacts = []
session = requests.Session()
session.headers.update(HEADERS)

for i, row in enumerate(rows, start=1):
    email = ""
    try:
        r = session.get(row["website"], timeout=3, allow_redirects=True)
        found = EMAIL_RE.findall(r.text)
        found = [clean_email(x) for x in found]
        found = [x for x in found if x]
        if found:
            preferred = sorted(found, key=lambda x: (
                0 if x.startswith(("info@","hello@","contact@","sales@","office@")) else 1,
                len(x)
            ))
            email = preferred[0]
    except Exception:
        pass

    contacts.append({
        "company": row["company"],
        "website": row["website"],
        "domain": row["domain"],
        "email": email,
        "status": "ready" if email else "no-email"
    })

    if i % 25 == 0:
        print("checked:", i)

contacts_path = OUT / "contacts.csv"
with open(contacts_path, "w", newline="", encoding="utf8") as f:
    w = csv.DictWriter(f, fieldnames=["company","website","domain","email","status"])
    w.writeheader()
    w.writerows(contacts)

valid = [x for x in contacts if x["email"]]

outreach = []
for row in valid:
    outreach.append({
        "company": row["company"],
        "email": row["email"],
        "subject": f"free market brief for {row['company']}",
        "message": f"""Hi,

I built a small AI tool that generates a niche market brief for agencies and B2B companies.

Running it on your market reveals:
- competitor angles
- positioning gaps
- monetization opportunities

You can generate the instant version here:
{STRIPE}

It's €9 for now.

Nicodemo
""",
        "status": "ready"
    })

outreach_path = OUT / "outreach.csv"
with open(outreach_path, "w", newline="", encoding="utf8") as f:
    w = csv.DictWriter(f, fieldnames=["company","email","subject","message","status"])
    w.writeheader()
    w.writerows(outreach)

print("saved sites:", sites_path)
print("saved contacts:", contacts_path)
print("saved outreach:", outreach_path)
print("emails found:", len(valid))
