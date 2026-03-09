
from pathlib import Path
from datetime import date
import csv
import re
import time
import urllib.parse
import requests

BASE = Path.home() / "ai_factory"
OUT = BASE / "engine_final"
OUT.mkdir(exist_ok=True)

TODAY = date.today().isoformat()

queries = [
    "marketing agency london",
    "marketing agency new york",
    "marketing agency toronto",
    "marketing agency sydney",
    "marketing agency berlin",
    "marketing agency amsterdam",
    "marketing agency paris",
    "marketing agency madrid",
    "marketing agency dublin",
    "marketing agency singapore",
    "seo agency london",
    "seo agency new york",
    "seo agency toronto",
    "seo agency sydney",
    "seo agency berlin",
    "seo agency amsterdam",
    "seo agency paris",
    "seo agency madrid",
    "seo agency dublin",
    "seo agency singapore",
    "digital agency london",
    "digital agency new york",
    "digital agency toronto",
    "digital agency sydney",
    "digital agency berlin",
    "digital agency amsterdam",
    "digital agency paris",
    "digital agency madrid",
    "digital agency dublin",
    "digital agency singapore",
    "growth agency london",
    "growth agency new york",
    "growth agency toronto",
    "growth agency sydney",
    "growth agency berlin",
    "growth agency amsterdam",
    "branding agency london",
    "branding agency new york",
    "branding agency toronto",
    "branding agency berlin",
    "web agency london",
    "web agency new york",
    "web agency toronto",
    "web agency sydney",
    "web agency berlin",
    "b2b agency london",
    "b2b agency new york",
    "b2b agency toronto",
    "b2b agency berlin",
    "consulting firm london",
    "consulting firm new york",
    "consulting firm toronto",
    "consulting firm berlin",
    "startup accelerator london",
    "startup accelerator new york",
    "startup accelerator toronto",
    "startup accelerator berlin",
    "ai startup london",
    "ai startup new york",
    "ai startup toronto",
    "ai startup berlin",
]

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Content-Type": "application/x-www-form-urlencoded",
    "Accept-Language": "en-US,en;q=0.9",
}

BAD_DOMAIN_PARTS = [
    "duckduckgo.com", "clutch.co", "sortlist.com", "designrush.com", "goodfirms.co",
    "linkedin.com", "facebook.com", "instagram.com", "youtube.com", "wikipedia.org",
    "yelp.com", "agencyspotter.com", "producthunt.com", "medium.com", "semrush.com"
]

BAD_EMAIL_PARTS = [
    ".png", ".jpg", ".jpeg", ".gif", ".svg", "@2x", "@3x", "noreply@", "no-reply@",
    "donotreply@", "example.com", "sentry", "wixpress", "cloudflare"
]

EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")

def ddg_search(query, max_results=10, region="uk-en"):
    url = "https://duckduckgo.com/html/"
    data = {"q": query, "kl": region}
    try:
        r = requests.post(url, headers=HEADERS, data=data, timeout=25)
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

def get_domain(url):
    try:
        p = urllib.parse.urlparse(url)
        d = p.netloc.lower()
        d = re.sub(r"^www\.", "", d)
        return d
    except Exception:
        return ""

def clean_email(e):
    e = (e or "").strip().lower()
    if not e or "@" not in e:
        return ""
    if any(x in e for x in BAD_EMAIL_PARTS):
        return ""
    local, _, domain = e.partition("@")
    if not local or not domain or "." not in domain:
        return ""
    return e

# 1) search -> domains
raw_rows = []
domains = {}
for i, q in enumerate(queries, start=1):
    print(f"[{i}/{len(queries)}] search:", q)
    hits = ddg_search(q, max_results=10)
    for title, href in hits:
        domain = get_domain(href)
        if not domain:
            continue
        if any(x in domain for x in BAD_DOMAIN_PARTS):
            continue
        if domain not in domains:
            domains[domain] = {
                "query": q,
                "company": title,
                "domain": domain,
                "website": f"https://{domain}",
                "status": "new"
            }
        raw_rows.append([q, title, href, domain])
    time.sleep(1.2)

raw_path = OUT / f"raw_results_{TODAY}.csv"
with open(raw_path, "w", newline="", encoding="utf8") as f:
    w = csv.writer(f)
    w.writerow(["query", "title", "url", "domain"])
    w.writerows(raw_rows)

domains_path = OUT / f"domains_{TODAY}.csv"
with open(domains_path, "w", newline="", encoding="utf8") as f:
    w = csv.DictWriter(f, fieldnames=["query","company","domain","website","status"])
    w.writeheader()
    w.writerows(domains.values())

print("unique domains:", len(domains))

# 2) domains -> emails
contacts = []
session = requests.Session()
session.headers.update({"User-Agent": "Mozilla/5.0", "Accept-Language": "en-US,en;q=0.9"})

for i, row in enumerate(domains.values(), start=1):
    website = row["website"]
    email_found = ""
    pages = [website, website + "/contact", website + "/about", website + "/contact-us"]

    for page in pages:
        try:
            r = session.get(page, timeout=10, allow_redirects=True)
            text = r.text
            found = EMAIL_RE.findall(text)
            found = [clean_email(x) for x in found]
            found = [x for x in found if x]
            if found:
                # prefer business-ish emails
                preferred = sorted(found, key=lambda x: (
                    0 if x.startswith(("info@","hello@","contact@","sales@","office@")) else 1,
                    len(x)
                ))
                email_found = preferred[0]
                break
        except Exception:
            continue

    contacts.append({
        "query": row["query"],
        "company": row["company"],
        "domain": row["domain"],
        "website": website,
        "email": email_found,
        "status": "new" if email_found else "no-email"
    })

    if i % 25 == 0:
        print("checked domains:", i)
    time.sleep(0.4)

contacts_path = OUT / f"contacts_{TODAY}.csv"
with open(contacts_path, "w", newline="", encoding="utf8") as f:
    w = csv.DictWriter(f, fieldnames=["query","company","domain","website","email","status"])
    w.writeheader()
    w.writerows(contacts)

valid_contacts = [x for x in contacts if x["email"]]

# 3) outreach queue
outreach_rows = []
for row in valid_contacts:
    company = row["company"].strip() or row["domain"]
    email = row["email"]
    subject = f"free market brief for {company}"
    message = """Hi,

I built a small AI tool that generates a niche market brief for agencies and B2B companies.

Running it on your market reveals:
- competitor angles
- positioning gaps
- monetization opportunities

You can generate the instant version here:
https://buy.stripe.com/test_5kQ8wH3WofTc56Z8vdcs800

It's €9 for now.

Nicodemo
"""
    outreach_rows.append({
        "company": company,
        "email": email,
        "subject": subject,
        "message": message,
        "status": "ready"
    })

outreach_path = OUT / f"outreach_{TODAY}.csv"
with open(outreach_path, "w", newline="", encoding="utf8") as f:
    w = csv.DictWriter(f, fieldnames=["company","email","subject","message","status"])
    w.writeheader()
    w.writerows(outreach_rows)

print("saved raw:", raw_path)
print("saved domains:", domains_path)
print("saved contacts:", contacts_path)
print("saved outreach:", outreach_path)
print("emails found:", len(valid_contacts))
