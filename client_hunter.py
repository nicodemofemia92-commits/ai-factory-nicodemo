
import os
from datetime import datetime
from google import genai

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
client = genai.Client(api_key=GEMINI_API_KEY)

today = datetime.now().strftime("%Y-%m-%d")
product = "NicheBrief AI"
offer1 = "Custom niche brief for €29"
offer2 = "Extended growth plan upsell"
website = "https://ai-factory-nicodemo.onrender.com"

print("\nCLIENT HUNTER AGENT")
print("-------------------")
print("Date:", today)

prompt = f"""
You are a B2B growth operator.

Product:
{product}

Primary offer:
{offer1}

Upsell:
{offer2}

Website:
{website}

Create a practical client hunting plan.

Return:

1. 10 target customer types
2. 15 search queries to find potential clients
3. 10 business categories to target first
4. 10 public places where to find them
5. 5 short outreach messages
6. 5 follow-up messages
7. 5 lead magnet hooks
8. 1 simple client acquisition workflow

Rules:
- Focus on founders, freelancers, agencies, consultants, local businesses
- Prefer public channels only
- No scraping private emails
- Keep everything practical and concise

Format with clear sections.
"""

try:
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    output = response.text

except Exception as e:
    output = f"""
[DEMO CLIENT HUNTER PLAN]

TARGET CUSTOMER TYPES
1. Small marketing agency owners
2. Freelance SEO consultants
3. Solo growth marketers
4. Startup founders validating ideas
5. Local lead generation agencies
6. Business consultants
7. Real estate agency owners
8. Boutique branding studios
9. Web design freelancers
10. Small B2B service firms

SEARCH QUERIES
1. marketing agency Milan
2. seo consultant Milan
3. startup studio Italy
4. freelance marketer Italy
5. real estate agency Milan
6. growth consultant London
7. branding agency Berlin
8. local business consultant Italy
9. SaaS founder LinkedIn
10. agency owner LinkedIn
11. Clutch marketing agencies Italy
12. web design agency Milan
13. small digital agency Rome
14. consultant niche strategy
15. local lead gen agency

BUSINESS CATEGORIES
1. Agencies
2. Consultants
3. Founders
4. Real estate
5. Local services
6. Coaches
7. Dentists
8. Lawyers
9. Ecommerce brands
10. Architects

PUBLIC PLACES TO FIND THEM
1. LinkedIn company pages
2. LinkedIn founder profiles
3. Company websites
4. Contact pages
5. Clutch
6. Google Maps listings
7. Agency directories
8. Founder communities
9. X/Twitter bios
10. Instagram business profiles

OUTREACH MESSAGES
1. Hey, I built a tool that turns any niche into a strategic market brief in seconds. Want me to generate one for your market?
2. Quick question: how do you currently validate a niche before building an offer?
3. I’m testing an AI market brief generator for agencies and consultants. Happy to send an example.
4. Built something that gives competitor + positioning + monetization angles for any niche. Might be useful for your work.
5. If you explore new markets often, this could save hours of manual research.

FOLLOW-UP MESSAGES
1. Just bumping this in case niche validation is still a manual process for you.
2. Happy to send a sample brief if useful.
3. I can run one niche report for your market and send it over.
4. Curious if this would help more with your offers or with your clients.
5. No rush — just thought it could save some research time.

LEAD MAGNET HOOKS
1. Free sample niche brief
2. 3 competitor angles for your market
3. AI market scan in 30 seconds
4. Stop guessing your niche
5. Validate before building

CLIENT ACQUISITION WORKFLOW
1. Pick 1 niche today
2. Search 10 companies with the queries above
3. Save company name + website + contact page
4. Send 3 outreach messages
5. Generate 1 sample brief
6. Offer full brief for €29
7. Upsell growth plan later

(Gemini fallback)
Error: {str(e)}
"""

print(output)

folder = os.path.expanduser("~/ai_factory/client_hunter")
os.makedirs(folder, exist_ok=True)
path = os.path.join(folder, f"client_hunter_{today}.txt")
with open(path, "w") as f:
    f.write(output)

print("\nSaved to:", path)
