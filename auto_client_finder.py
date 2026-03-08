
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
You are a B2B client finding strategist.

Product:
{product}

Offer:
{offer}

Website:
{website}

Create an AUTO CLIENT FINDER output.

Return:

1. 15 target business types
2. 20 Google search queries to find them
3. 15 LinkedIn search queries
4. 10 public contact entry points
5. 10 public directories/platforms
6. 10 example company names by niche
7. 5 outreach messages
8. 1 suggested client-finding workflow

Rules:
- Focus on public channels only
- No scraping private emails
- Focus on agencies, consultants, founders, local businesses, real estate agencies
- Keep it practical and concise
- Make it directly usable

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
[DEMO AUTO CLIENT FINDER]

TARGET BUSINESS TYPES
1. Marketing agencies
2. SEO consultants
3. Growth consultants
4. Branding studios
5. Real estate agencies
6. Web design agencies
7. Local business consultants
8. Startup advisors
9. Lead generation agencies
10. Business coaches
11. Dentists
12. Lawyers
13. Ecommerce consultants
14. SaaS founders
15. Architects

GOOGLE SEARCH QUERIES
1. marketing agency Milan
2. seo consultant Italy
3. real estate agency Milan
4. branding studio Milan
5. web design agency Rome
6. startup advisor Italy
7. growth consultant London
8. digital agency Italy
9. business consultant Milan
10. local lead generation agency
11. dentist clinic Milan
12. lawyer firm Milan
13. architect studio Milan
14. ecommerce consultant Italy
15. founder LinkedIn Italy
16. SaaS founder Italy
17. branding agency Rome
18. marketing consultant Milan
19. real estate consultant Milan
20. digital growth consultant

LINKEDIN SEARCH QUERIES
1. marketing agency owner
2. seo consultant
3. growth consultant
4. startup founder
5. freelance marketer
6. real estate agency owner
7. branding consultant
8. digital agency founder
9. web design agency owner
10. business consultant
11. lead generation agency
12. ecommerce consultant
13. startup advisor
14. freelance seo specialist
15. local marketing consultant

PUBLIC CONTACT ENTRY POINTS
1. Contact page
2. Public business email
3. LinkedIn company page
4. Founder profile
5. Demo booking page
6. Contact form
7. Instagram bio link
8. X/Twitter bio
9. Agency directory listing
10. Google Maps profile

PUBLIC DIRECTORIES / PLATFORMS
1. LinkedIn
2. Clutch
3. Sortlist
4. GoodFirms
5. Agency Spotter
6. Google Maps
7. Yelp
8. Product Hunt
9. AngelList
10. Crunchbase

EXAMPLE COMPANY NAMES
1. GrowthLab Agency
2. Prime SEO Studio
3. Digital Boost Agency
4. BrandForge Studio
5. Realty Milano
6. Scale Marketing
7. Local Lead Labs
8. Startup Sprint Advisory
9. WebNest Studio
10. MarketPilot Agency

OUTREACH MESSAGES
1. Hey, I built a tool that generates a niche intelligence brief in seconds. Want me to generate one for your market?
2. Quick question: how do you currently validate a niche before building an offer?
3. I’m testing an AI market brief generator for agencies and consultants. Happy to send an example.
4. Built something that gives competitor + positioning + monetization angles for any niche. Might be useful for your work.
5. If you explore new markets often, this could save hours of manual research.

CLIENT-FINDING WORKFLOW
1. Pick one niche
2. Use 3 search queries
3. Collect 10 company names
4. Save website + contact page
5. Send 3 outreach messages
6. Offer €29 brief
7. Upsell later

(Gemini fallback)
Error: {str(e)}
"""

print(output)

folder = os.path.expanduser("~/ai_factory/auto_client_finder")
os.makedirs(folder, exist_ok=True)
path = os.path.join(folder, f"auto_client_finder_{today}.txt")

with open(path, "w") as f:
    f.write(output)

print("\nSaved to:", path)
