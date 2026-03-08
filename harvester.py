
from pathlib import Path
from datetime import datetime
import re

base = Path.home() / "ai_factory"
today = datetime.now().strftime("%Y-%m-%d")

def latest_text(folder, pattern):
    p = base / folder
    if not p.exists():
        return ""
    files = sorted(p.glob(pattern), reverse=True)
    if not files:
        return ""
    try:
        return files[0].read_text()
    except Exception:
        return ""

lead_machine = latest_text("leads", "lead_machine_*.txt")
client_hunter = latest_text("client_hunter", "client_hunter_*.txt")
sales_queue = latest_text("sales_queue", "sales_queue_*.txt")
reactor = latest_text("lead_reactor", "reactor_*.txt")
auto_outreach = latest_text("auto_outreach", "auto_outreach_*.txt")

def pick_queries(text, limit=12):
    lines = []
    for line in text.splitlines():
        s = line.strip()
        if not s:
            continue
        if s.startswith("[DEMO"):
            continue
        if any(k in s.lower() for k in [
            "marketing agency", "seo consultant", "real estate", "branding",
            "web design", "growth consultant", "digital agency", "startup founder",
            "business consultant", "lead generation"
        ]):
            lines.append(s.lstrip("-•1234567890. ").strip())
    # dedupe
    out = []
    seen = set()
    for x in lines:
        if x.lower() not in seen:
            seen.add(x.lower())
            out.append(x)
    return out[:limit]

queries = []
for source in [lead_machine, client_hunter, sales_queue]:
    queries.extend(pick_queries(source, limit=20))

# dedupe queries
clean_queries = []
seen = set()
for q in queries:
    key = q.lower()
    if key not in seen:
        seen.add(key)
        clean_queries.append(q)

if not clean_queries:
    clean_queries = [
        "marketing agency Milan",
        "seo consultant Italy",
        "branding studio Milan",
        "real estate agency Milan",
        "digital agency Rome",
        "startup founder LinkedIn Italy",
    ]

message_source = reactor or auto_outreach
messages = []
for line in message_source.splitlines():
    s = line.strip()
    if not s:
        continue
    if s.startswith("[DEMO"):
        continue
    if len(s) > 20:
        messages.append(s)
messages = messages[:5]

if not messages:
    messages = [
        "Hey, I built a tool that generates a structured niche market brief in seconds. Want me to run one for your market?",
        "Quick question: how do you validate a niche before building an offer?",
        "I’m testing an AI market brief generator for agencies and consultants. Happy to send a sample.",
    ]

rows = []
for i, q in enumerate(clean_queries[:10], start=1):
    rows.append(
        f"{i}. QUERY: {q}\n"
        f"   COMPANY: \n"
        f"   WEBSITE: \n"
        f"   CONTACT PAGE: \n"
        f"   LINKEDIN: \n"
        f"   STATUS: to-research\n"
    )

text = f"""HARVESTER QUEUE
Date: {today}

HOW TO USE
1. Pick 3 queries below
2. Search them on Google / LinkedIn / Clutch / Maps
3. Fill company + website + contact page
4. Use one outreach message
5. Update STATUS to contacted

SEARCH QUERIES
{chr(10).join(rows)}

OUTREACH MESSAGES
""" + "\n".join([f"- {m}" for m in messages]) + """

PUBLIC SOURCES TO USE
- Google Search
- LinkedIn company pages
- Clutch
- Sortlist
- Google Maps
- company websites
- public contact pages

DAILY TARGET
- research 5 companies
- contact 3
- generate 1 sample brief
- push €29 offer
"""

folder = base / "harvester"
folder.mkdir(exist_ok=True)
path = folder / f"harvester_{today}.txt"
path.write_text(text)

print("harvester generated:", path)
