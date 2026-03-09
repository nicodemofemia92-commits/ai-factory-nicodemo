
from pathlib import Path
from datetime import date
import csv
import re
import time
import requests
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from urllib.parse import urlparse

BASE = Path.home() / "ai_factory"
OUT = BASE / "clutch_engine"
OUT.mkdir(exist_ok=True)

TODAY = date.today().isoformat()

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept-Language": "en-US,en;q=0.9",
}

EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")

BAD_EMAIL_BITS = [
    ".png", ".jpg", ".jpeg", ".gif", ".svg", "@2x", "@3x",
    "noreply@", "no-reply@", "donotreply@", "example.com"
]

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

def get_domain(url):
    try:
        d = urlparse(url).netloc.lower()
        if d.startswith("www."):
            d = d[4:]
        return d
    except Exception:
        return ""

def find_site_on_profile(html):
    soup = BeautifulSoup(html, "html.parser")

    # 1) link text "visit website"
    for a in soup.find_all("a", href=True):
        text = a.get_text(" ", strip=True).lower()
        href = a["href"]
        if "visit website" in text and href.startswith("http"):
            return href

    # 2) any external link not clutch
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if href.startswith("http") and "clutch.co" not in href:
            return href

    return ""

def extract_email_from_site(website):
    session = requests.Session()
    session.headers.update(HEADERS)

    pages = [
        website,
        website.rstrip("/") + "/contact",
        website.rstrip("/") + "/about",
        website.rstrip("/") + "/contact-us",
    ]

    for page in pages:
        try:
            r = session.get(page, timeout=12, allow_redirects=True)
            found = EMAIL_RE.findall(r.text)
            found = [clean_email(x) for x in found]
            found = [x for x in found if x]
            if found:
                preferred = sorted(found, key=lambda x: (
                    0 if x.startswith(("info@", "hello@", "contact@", "sales@", "office@")) else 1,
                    len(x)
                ))
                return preferred[0]
        except Exception:
            continue

    return ""

# STEP 1: scrape clutch sitemap profiles
profile_urls = []

# prova 1..20 sitemap profile, abbastanza per avere materiale
for i in range(1, 21):
    sitemap_url = f"https://clutch.co/sitemap-profile-{i}.xml"
    try:
        r = requests.get(sitemap_url, headers=HEADERS, timeout=20)
        if r.status_code != 200 or "<urlset" not in r.text:
            continue

        root = ET.fromstring(r.text)
        for loc in root.iter("{http://www.sitemaps.org/schemas/sitemap/0.9}loc"):
            url = (loc.text or "").strip()
            if "/profile/" in url:
                profile_urls.append(url)

        print("sitemap", i, "profiles:", len(profile_urls))
        time.sleep(0.5)
    except Exception:
        continue

# dedupe
profile_urls = list(dict.fromkeys(profile_urls))
print("total profiles found:", len(profile_urls))

profiles_csv = OUT / f"profiles_{TODAY}.csv"
with open(profiles_csv, "w", newline="", encoding="utf8") as f:
    w = csv.writer(f)
    w.writerow(["profile_url"])
    for u in profile_urls:
        w.writerow([u])

# STEP 2: fetch profiles -> official website
companies = []

for idx, profile_url in enumerate(profile_urls[:300], start=1):
    try:
        r = requests.get(profile_url, headers=HEADERS, timeout=20)
        html = r.text
        site = find_site_on_profile(html)

        company = ""
        soup = BeautifulSoup(html, "html.parser")
        if soup.title:
            company = soup.title.get_text(" ", strip=True).split("|")[0].strip()

        if site:
            companies.append({
                "profile_url": profile_url,
                "company": company or get_domain(site),
                "website": site,
                "domain": get_domain(site)
            })

        if idx % 25 == 0:
            print("profiles checked:", idx, "companies:", len(companies))

        time.sleep(0.4)
    except Exception:
        continue

companies = list({c["domain"]: c for c in companies if c["domain"]}.values())
print("unique company sites:", len(companies))

sites_csv = OUT / f"company_sites_{TODAY}.csv"
with open(sites_csv, "w", newline="", encoding="utf8") as f:
    w = csv.DictWriter(f, fieldnames=["profile_url", "company", "website", "domain"])
    w.writeheader()
    w.writerows(companies)

# STEP 3: site -> email
contacts = []
for idx, c in enumerate(companies, start=1):
    email = extract_email_from_site(c["website"])
    contacts.append({
        "company": c["company"],
        "website": c["website"],
        "domain": c["domain"],
        "email": email,
        "status": "ready" if email else "no-email"
    })

    if idx % 25 == 0:
        print("sites checked for email:", idx)

    time.sleep(0.3)

contacts_csv = OUT / f"contacts_{TODAY}.csv"
with open(contacts_csv, "w", newline="", encoding="utf8") as f:
    w = csv.DictWriter(f, fieldnames=["company", "website", "domain", "email", "status"])
    w.writeheader()
    w.writerows(contacts)

valid = [x for x in contacts if x["email"]]

# STEP 4: outreach queue
stripe = "https://buy.stripe.com/test_5kQ8wH3WofTc56Z8vdcs800"

outreach = []
for row in valid:
    company = row["company"] or row["domain"]
    email = row["email"]

    outreach.append({
        "company": company,
        "email": email,
        "subject": f"free market brief for {company}",
        "message": f"""Hi,

I built a small AI tool that generates a niche market brief for agencies and B2B companies.

Running it on your market reveals:
- competitor angles
- positioning gaps
- monetization opportunities

You can generate the instant version here:
{stripe}

It's €9 for now.

Nicodemo
""",
        "status": "ready"
    })

outreach_csv = OUT / f"outreach_{TODAY}.csv"
with open(outreach_csv, "w", newline="", encoding="utf8") as f:
    w = csv.DictWriter(f, fieldnames=["company", "email", "subject", "message", "status"])
    w.writeheader()
    w.writerows(outreach)

print("saved profiles:", profiles_csv)
print("saved company sites:", sites_csv)
print("saved contacts:", contacts_csv)
print("saved outreach:", outreach_csv)
print("emails found:", len(valid))
