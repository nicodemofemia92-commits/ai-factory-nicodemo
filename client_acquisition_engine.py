
import os
from datetime import datetime
from google import genai

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
client = genai.Client(api_key=GEMINI_API_KEY)

today = datetime.now().strftime("%Y-%m-%d")

product = "NicheBrief AI"
offer = "Custom niche brief for €29"
upsell = "Extended growth plan"
website = "https://ai-factory-nicodemo.onrender.com"

prompt = f"""
You are a startup client acquisition strategist.

Product:
{product}

Offer:
{offer}

Upsell:
{upsell}

Website:
{website}

Create a practical CLIENT ACQUISITION ENGINE output.

Return:

1. 10 best target buyer profiles
2. 10 niches with highest buying intent
3. 10 reasons they would buy
4. 5 first outreach messages
5. 5 follow-up messages
6. 5 CTA offers
7. 1 acquisition workflow from lead to €29 sale
8. 1 upsell workflow from €29 to higher-ticket offer
9. 1 daily KPI checklist

Keep it practical, concise, sales-oriented, and ethical.
Focus on public outreach and human-reviewed sales steps.
"""

try:
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    output = response.text

except Exception as e:
    output = f"""
[DEMO CLIENT ACQUISITION ENGINE]

BEST TARGET BUYER PROFILES
1. Small marketing agency owners
2. Freelance SEO consultants
3. Solo growth marketers
4. Startup founders validating a niche
5. Business consultants
6. Boutique branding studios
7. Real estate agency owners
8. Local lead generation agencies
9. Web design freelancers
10. Small B2B service firms

NICHES WITH HIGHEST BUYING INTENT
1. Marketing agencies
2. SEO consultants
3. Real estate agencies
4. Coaches
5. Dentists
6. Lawyers
7. Local service businesses
8. Ecommerce founders
9. SaaS founders
10. Business consultants

REASONS THEY WOULD BUY
1. Faster market validation
2. Better competitor clarity
3. Better offer positioning
4. Saves manual research time
5. Useful for client pitches
6. Helps package services
7. Helps niche expansion
8. Helps pricing decisions
9. Gives usable strategy angles
10. Low-ticket easy test purchase

FIRST OUTREACH MESSAGES
1. Hey, I built a tool that turns any niche into a structured market brief. Want me to generate one for your market?
2. Quick question: how do you validate a niche before building an offer?
3. I’m testing an AI market brief generator for founders and agencies. Happy to send an example.
4. Built something that gives competitor + positioning + monetization angles for any niche. Might be useful for your work.
5. If you explore new markets often, this could save hours of manual research.

FOLLOW-UP MESSAGES
1. Just bumping this in case niche validation is still manual for you.
2. Happy to send a sample brief if useful.
3. I can generate one example for your niche today.
4. Curious if this would help your team or your clients more.
5. No rush — just thought it might save some research time.

CTA OFFERS
1. Want a custom niche brief for €29?
2. I can generate a full version for your market today.
3. Try the live tool here: {website}
4. Want a sample brief first?
5. Stop guessing your niche.

ACQUISITION WORKFLOW
1. Pick one niche
2. Find 10 prospects
3. Send 3 first messages
4. Generate 1 sample brief
5. Offer full brief for €29
6. Deliver within 24h
7. Ask for feedback and upsell

UPSELL WORKFLOW
1. Deliver the €29 brief
2. Highlight 2-3 strategic opportunities
3. Offer extended growth plan
4. Offer competitor deep dive
5. Offer ongoing niche research support

DAILY KPI CHECKLIST
- 3 prospects contacted
- 1 follow-up sent
- 1 content post published
- 1 sample brief generated
- 1 CTA pushed
- 1 paid customer target

(Gemini fallback)
Error: {str(e)}
"""

print(output)

folder = os.path.expanduser("~/ai_factory/client_acquisition")
os.makedirs(folder, exist_ok=True)
path = os.path.join(folder, f"client_acquisition_{today}.txt")

with open(path, "w") as f:
    f.write(output)

print("\nSaved to:", path)
