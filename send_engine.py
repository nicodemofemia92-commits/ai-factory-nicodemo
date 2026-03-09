
from pathlib import Path
import csv
import os
import smtplib
from email.message import EmailMessage

BASE = Path.home() / "ai_factory"
LEADS = BASE / "global_leads" / "global_outreach_queue_clean.csv"

SMTP_HOST = os.environ.get("SMTP_HOST")
SMTP_PORT = int(os.environ.get("SMTP_PORT", "587"))
SMTP_USER = os.environ.get("SMTP_USER")
SMTP_PASS = os.environ.get("SMTP_PASS")
FROM_EMAIL = os.environ.get("FROM_EMAIL")
SEND_BATCH_SIZE = int(os.environ.get("SEND_BATCH_SIZE", "5"))

print("Starting send engine...")

if not LEADS.exists():
    print("Leads file not found:", LEADS)
    exit()

rows = []
with open(LEADS, encoding="utf8") as f:
    r = csv.DictReader(f)
    for row in r:
        if row.get("email"):
            rows.append(row)

print("Emails found:", len(rows))

server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
server.starttls()
server.login(SMTP_USER, SMTP_PASS)

sent = 0

for row in rows[:5]:
    msg = EmailMessage()
    msg["From"] = FROM_EMAIL
    msg["To"] = row["email"]
    msg["Subject"] = "Quick question about your marketing"

    msg.set_content(f'''
Hi {row["company"]},

I built a tool that generates a quick market intelligence brief for companies in your niche.

Would you like me to send you one for free?

Best,
Nicodemo
''')

    try:
        server.send_message(msg)
        print("sent:", row["email"])
        sent += 1
    except Exception as e:
        print("failed:", row["email"], e)

server.quit()

print("Done. Sent:", sent)
