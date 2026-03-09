
from pathlib import Path
import csv
import imaplib
import email
from datetime import datetime
import os

BASE = Path.home() / "ai_factory"
OUTDIR = BASE / "reply_parser"
OUTDIR.mkdir(exist_ok=True)

IMAP_HOST = os.environ.get("IMAP_HOST", "imap.gmail.com")
IMAP_USER = os.environ.get("SMTP_USER", "")
IMAP_PASS = os.environ.get("SMTP_PASS", "")

OUT = OUTDIR / f"replies_{datetime.now().strftime('%Y-%m-%d')}.csv"

skip_from = [
    "accounts.google.com",
    "mailer-daemon",
    "mail delivery subsystem",
    "no-reply",
    "noreply",
]
skip_subject = [
    "delivery status notification",
    "avviso di sicurezza",
    "security alert",
    "failure",
]

mail = imaplib.IMAP4_SSL(IMAP_HOST)
mail.login(IMAP_USER, IMAP_PASS)
mail.select("inbox")

status, messages = mail.search(None, "UNSEEN")
ids = messages[0].split()

rows = []
for num in ids[:100]:
    status, msg_data = mail.fetch(num, "(RFC822)")
    for response_part in msg_data:
        if isinstance(response_part, tuple):
            msg = email.message_from_bytes(response_part[1])
            from_ = (msg.get("From", "") or "").lower()
            subject = (msg.get("Subject", "") or "")
            subject_l = subject.lower()

            if any(x in from_ for x in skip_from):
                continue
            if any(x in subject_l for x in skip_subject):
                continue

            rows.append({
                "from": msg.get("From", ""),
                "subject": msg.get("Subject", ""),
                "status": "new-reply",
                "received_at": datetime.now().isoformat(timespec="seconds")
            })

with open(OUT, "w", newline="", encoding="utf8") as f:
    w = csv.DictWriter(f, fieldnames=["from","subject","status","received_at"])
    w.writeheader()
    w.writerows(rows)

mail.logout()
print("reply_parser completato")
print(OUT)
print("rows:", len(rows))
