
import os
from datetime import datetime
from google import genai

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
client = genai.Client(api_key=GEMINI_API_KEY)

today = datetime.now().strftime("%Y-%m-%d")
product = "NicheBrief AI"
offer = "Custom niche brief for €29"
website = "https://ai-factory-nicodemo.onrender.com"

print("\nDAILY PACK")
print("----------")
print("Date:", today)

prompt = f"""
You are a startup growth operator.

Create a DAILY EXECUTION PACK for this product:

Product:
{product}

Offer:
{offer}

Website:
{website}

Return:

1. 3 niches to target today
2. 3 target customer types
3. 3 outreach messages
4. 3 content posts
5. 1 offer angle for today
6. 1 CTA line
7. 1 daily action checklist

Keep it practical and concise.
Format clearly with sections.
"""

try:
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    output = response.text
except Exception as e:
    output = f"""
[DEMO DAILY PACK]

NICHES TO TARGET
1. Real estate agencies
2. Marketing freelancers
3. Local service businesses

TARGET CUSTOMERS
1. Agency owners
2. Solo consultants
3. Startup founders

OUTREACH MESSAGES
1. Hey, I built a tool that generates a niche intelligence brief in seconds. Want me to create one for your market?
2. Quick question: how do you validate a niche before building an offer for it?
3. I’m testing an AI market brief generator for founders and agencies. Happy to send an example.

CONTENT POSTS
1. Most founders build before understanding the niche. That’s backward.
2. A structured market brief can save weeks of random validation.
3. I turned niche research into a simple AI workflow: niche in, strategic brief out.

TODAY OFFER
Get a custom niche brief for €29.

CTA
Generate your market brief now: {website}

DAILY ACTION CHECKLIST
- Contact 3 target prospects
- Publish 1 LinkedIn post
- Share 1 CTA
- Generate 1 sample brief
- Ask for 1 paid test customer

(Gemini fallback)
Error: {str(e)}
"""

print(output)

# salva anche su file
folder = os.path.expanduser("~/ai_factory/daily_packs")
os.makedirs(folder, exist_ok=True)
path = os.path.join(folder, f"daily_pack_{today}.txt")
with open(path, "w") as f:
    f.write(output)

print("\nSaved to:", path)
