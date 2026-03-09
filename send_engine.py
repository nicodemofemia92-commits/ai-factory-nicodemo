
from pathlib import Path
import csv
import os
import smtplib
from email.message import EmailMessage
from datetime import datetime
import re

BASE = Path.home() / "ai_factory"
LEADS = BASE / "engine_dataset" / "outreach.csv"
LOGDIR = BASE / "send_engine"
LOGDIR.mkdir(exist_ok=True)

SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")
FROM_EMAIL = os.getenv("FROM_EMAIL")
SEND_BATCH_SIZE = int(os.getenv("SEND_BATCH_SIZE", "40"))

BAD_BITS = [
    ".png", ".jpg", ".jpeg", ".gif", ".svg",
    "@2x", "@3x", "postmaster@", "sentry.io",
    "noreply@", "no-reply@", "donotreply@"
]

def valid_email(email: str) -> bool:
    e = (email or "").strip().lower()
    if not e or "@" not in e:
        return False
    if any(x in e for x in BAD_BITS):
        return False
    return True

print("Starting send engine...")
print("Using leads file:", LEADS)

already_sent = set()
for f in LOGDIR.glob("sent_*.csv"):
    try:
        with open(f, encoding="utf8") as fh:
            r = csv.DictReader(fh)
            for row in r:
                em = (row.get("email") or "").strip().lower()
                if em:
                    already_sent.add(em)
    except Exception:
        pass

rows = []
seen = set()

with open(LEADS, encoding="utf8") as f:
    r = csv.DictReader(f)
    for row in r:
        email = (row.get("email") or "").strip().lower()
        subject = (row.get("subject") or "Quick idea").strip()
        message = (row.get("message") or "").strip()

        if not valid_email(email):
            continue
        if not message:
            continue
        if email in seen:
            continue
        if email in already_sent:
            continue

        seen.add(email)
        rows.append({
            "email": email,
            "subject": subject,
            "message": message
        })

print("Emails available:", len(rows))

to_send = rows[:SEND_BATCH_SIZE]
print("Sending batch:", len(to_send))

server = smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=20)
server.ehlo()
server.starttls()
server.ehlo()
server.login(SMTP_USER, SMTP_PASS)

today = datetime.now().strftime("%Y-%m-%d")
logfile = LOGDIR / f"sent_{today}.csv"

sent_rows = []
for row in to_send:
    msg = EmailMessage()
    msg["From"] = FROM_EMAIL
    msg["To"] = row["email"]
    msg["Subject"] = row["subject"]
    msg.set_content(row["message"])

    try:
        server.send_message(msg)
        print("sent:", row["email"])
        sent_rows.append({
            "email": row["email"],
            "subject": row["subject"],
            "sent_at": datetime.now().isoformat(timespec="seconds")
        })
    except Exception as e:
        print("failed:", row["email"], e)

server.quit()

if sent_rows:
    write_header = not logfile.exists()
    with open(logfile, "a", newline="", encoding="utf8") as f:
        w = csv.DictWriter(f, fieldnames=["email","subject","sent_at"])
        if write_header:
            w.writeheader()
        w.writerows(sent_rows)

print("Done. Sent:", len(sent_rows))
print("Log:", logfile)
