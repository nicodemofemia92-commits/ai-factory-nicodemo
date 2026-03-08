
import os
from google import genai

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
client = genai.Client(api_key=GEMINI_API_KEY)

print("\nSALES ENGINE")
print("------------")

product = "NicheBrief AI"
url = "https://ai-factory-nicodemo.onrender.com"

prompt = f"""
You are a SaaS sales strategist.

Product:
{product}

Website:
{url}

Generate a DAILY SALES PLAN.

Include:

1. 3 niches to target today
2. 3 customer profiles
3. 3 outreach messages
4. 3 content ideas to post
5. 1 offer angle to push today

Format:

NICHES TO TARGET
1.
2.
3.

CUSTOMERS
1.
2.
3.

OUTREACH MESSAGES
1.
2.
3.

CONTENT IDEAS
1.
2.
3.

TODAY OFFER
...
"""

try:
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    print(response.text)

except Exception as e:

    print("""
[DEMO SALES PLAN]

NICHES TO TARGET
1. Real estate agencies
2. Marketing freelancers
3. Local service businesses

CUSTOMERS
1. Solo consultants
2. Agency owners
3. Startup founders

OUTREACH MESSAGES
1. "Hey, I built a tool that generates a niche intelligence brief in seconds. Might help you validate markets faster."
2. "Quick question: how do you usually analyze a new niche before offering services?"
3. "I built an AI that turns any niche into a market research brief."

CONTENT IDEAS
1. Post: "Most founders skip niche research."
2. Post: "How to validate a market before building."
3. Post: "AI for market intelligence."

TODAY OFFER
Get a full niche intelligence brief for €29.

(Gemini quota exhausted fallback)
""")

