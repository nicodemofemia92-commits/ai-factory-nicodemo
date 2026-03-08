
import os
from datetime import datetime
from google import genai

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
client = genai.Client(api_key=GEMINI_API_KEY)

today = datetime.now().strftime("%Y-%m-%d")
product = "NicheBrief AI"
offer = "Custom niche brief for €29"
website = "https://ai-factory-nicodemo.onrender.com"

prompt = f"""
You are an outbound sales copywriter.

Product:
{product}

Offer:
{offer}

Website:
{website}

Create a DAILY OUTREACH PACK.

Return:

1. 3 target prospect types
2. 3 first outreach messages
3. 3 follow-up messages
4. 3 CTA lines
5. 1 short LinkedIn post to support outreach
6. 1 action checklist for today

Keep it short, practical and directly usable.
"""

try:
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    output = response.text

except Exception as e:
    output = f"""
[DEMO AUTO OUTREACH PACK]

TARGET PROSPECT TYPES
1. Small marketing agency owners
2. Freelance SEO consultants
3. Startup founders validating a niche

FIRST OUTREACH MESSAGES
1. Hey, I built a tool that generates a structured niche market brief in seconds. Want me to run one for your market?
2. Quick question: how do you validate a niche before building an offer?
3. I’m testing an AI market brief generator for agencies and consultants. Happy to send a sample.

FOLLOW-UP MESSAGES
1. Just bumping this in case niche validation is still manual for you.
2. Happy to generate one sample brief if useful.
3. I can send an example for your market today.

CTA LINES
1. Want a custom niche brief for €29?
2. I can generate a full version for your market today.
3. Try the live tool here: {website}

LINKEDIN POST
Most founders and agencies waste time on messy research.
I built a tool that turns any niche into a structured market brief in seconds:
competitors, positioning, monetization.
Live here: {website}

ACTION CHECKLIST
- Send 3 first outreach messages
- Send 1 follow-up
- Publish the LinkedIn post
- Generate 1 sample brief
- Push the €29 offer

(Gemini fallback)
Error: {str(e)}
"""

print(output)

folder = os.path.expanduser("~/ai_factory/auto_outreach")
os.makedirs(folder, exist_ok=True)
path = os.path.join(folder, f"auto_outreach_{today}.txt")

with open(path, "w") as f:
    f.write(output)

print("\nSaved to:", path)
