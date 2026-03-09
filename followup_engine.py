import csv
import smtplib
from email.message import EmailMessage
from pathlib import Path
import os
from datetime import datetime, timedelta

BASE = Path.home() / "ai_factory"
SEND_LOG = BASE / "send_engine"
REPLIES = BASE / "reply_parser"
LEADS = BASE / "global_leads"

SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT"))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")
FROM_EMAIL = os.getenv("FROM_EMAIL")

now = datetime.now()
followup_after = timedelta(hours=48)

sent = []

for f in SEND_LOG.glob("sent_*.csv"):

    with open(f) as file:
        r = csv.DictReader(file)

        for row in r:

            email = row["email"]
            sent_time = datetime.fromisoformat(row["sent_at"])

            if now - sent_time < followup_after:
                continue

            sent.append(email)

print("followups possible:",len(sent))

server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
server.starttls()
server.login(SMTP_USER, SMTP_PASS)

count = 0

for email in sent[:5]:

    msg = EmailMessage()

    msg["From"] = FROM_EMAIL
    msg["To"] = email
    msg["Subject"] = "Quick follow up"

    msg.set_content(f"""
Hey,

Just wanted to quickly follow up on the idea I sent earlier.

We built a small AI system that generates niche market briefs
for companies in seconds.

Happy to generate one for you if useful.

Best
""")

    try:
        server.send_message(msg)
        print("followup sent:",email)
        count += 1
    except:
        pass

server.quit()

print("followups sent:",count)
