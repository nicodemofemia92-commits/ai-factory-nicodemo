
import os
from datetime import datetime
from google import genai

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
client = genai.Client(api_key=GEMINI_API_KEY)

today = datetime.now().strftime("%Y-%m-%d")
product = "NicheBrief AI"
offer = "Custom niche brief for €29"
website = "https://ai-factory-nicodemo.onrender.com"

print("\nSALES QUEUE")
print("-----------")
print("Date:", today)

prompt = f"""
You are a startup sales operator.

Product:
{product}

Offer:
{offer}

Website:
{website}

Create a SALES QUEUE for today.

Return:

1. 10 target prospects or prospect types
2. 10 search queries to find them
3. 5 first outreach messages
4. 5 follow-up messages
5. 5 CTA variations
6. 1 simple action queue for today

Keep it concise, practical and ready to use.
Use public channels only.
"""

try:
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    output = response.text

except Exception as e:
    output = f"""
[DEMO SALES QUEUE]

TARGET PROSPECTS
1. Small marketing agency owners
2. Freelance SEO consultants
3. Solo growth marketers
4. Startup founders validating niches
5. Boutique branding studios
6. Real estate agency owners
7. Web design freelancers
8. Local business consultants
9. Lead generation agencies
10. Small B2B service firms

SEARCH QUERIES
1. marketing agency Milan
2. seo consultant Milan
3. startup founder LinkedIn Italy
4. freelance marketer Italy
5. real estate agency Milan
6. web design agency Rome
7. branding studio London
8. local business consultant Italy
9. agency owner LinkedIn
10. clutch marketing agencies Italy

FIRST OUTREACH
1. Hey, I built a tool that generates a niche intelligence brief in seconds. Want me to create one for your market?
2. Quick question: how do you currently validate a niche before building an offer?
3. I’m testing an AI market brief generator for agencies and consultants. Happy to send an example.
4. Built something that gives competitor + positioning + monetization angles for any niche. Might be useful for your work.
5. If you explore new markets often, this could save hours of research.

FOLLOW-UP
1. Just bumping this in case market validation is still manual for you.
2. Happy to send a sample brief if useful.
3. I can generate one example for your market today.
4. Curious whether this is more useful for your team or your clients.
5. No rush — just thought it might save you research time.

CTA VARIATIONS
1. Want a custom niche brief for your market?
2. I can generate a full version for €29.
3. Try the live tool here: {website}
4. Want a sample for your niche?
5. Stop guessing your market.

ACTION QUEUE
1. Pick 1 niche
2. Search 10 prospects
3. Contact 3 today
4. Publish 1 post
5. Generate 1 sample brief
6. Push the €29 offer

(Gemini fallback)
Error: {str(e)}
"""

print(output)

folder = os.path.expanduser("~/ai_factory/sales_queue")
os.makedirs(folder, exist_ok=True)
path = os.path.join(folder, f"sales_queue_{today}.txt")
with open(path, "w") as f:
    f.write(output)

print("\nSaved to:", path)
