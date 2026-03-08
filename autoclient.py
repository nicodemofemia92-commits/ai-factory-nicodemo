
import os
from google import genai

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
client = genai.Client(api_key=GEMINI_API_KEY)

print("\nAUTOCLIENT AGENT")
print("----------------")

product = "NicheBrief AI"
offer = "Custom niche intelligence brief for €29"
website = "https://ai-factory-nicodemo.onrender.com"

prompt = f"""
You are a B2B outbound strategist.

Product:
{product}

Offer:
{offer}

Website:
{website}

Generate a practical target acquisition plan.

Include:

1. 10 target company types
2. 10 example target business categories
3. Best public channels to find them
4. Best public contact entry points to look for
5. 5 outreach messages
6. 5 follow-up messages
7. 5 lead magnets or hooks

Rules:
- Focus on agencies, freelancers, founders, consultants, local business operators
- Do not suggest scraping private emails or violating platform rules
- Prefer public websites, contact pages, LinkedIn company pages, directories, and public business listings
- Keep it practical and concise

Format:

TARGET COMPANY TYPES
1.
2.

TARGET BUSINESS CATEGORIES
1.
2.

PUBLIC CHANNELS
1.
2.

CONTACT ENTRY POINTS
1.
2.

OUTREACH MESSAGES
1.
2.

FOLLOW-UPS
1.
2.

HOOKS
1.
2.
"""

try:
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    print(response.text)

except Exception as e:
    print("""
[DEMO AUTOCLIENT PLAN]

TARGET COMPANY TYPES
1. Small marketing agencies
2. Freelance growth marketers
3. Boutique branding studios
4. SEO consultants
5. Solo business consultants
6. Real estate agencies
7. Web design studios
8. Local lead generation agencies
9. Startup advisors
10. Small B2B service firms

TARGET BUSINESS CATEGORIES
1. Real estate
2. Dentists
3. Lawyers
4. Gyms
5. Spas
6. Restaurants
7. Accountants
8. Ecommerce brands
9. Coaches
10. Architects

PUBLIC CHANNELS
1. LinkedIn company pages
2. Company websites
3. Contact pages
4. Local directories
5. Agency showcases
6. Clutch
7. Google Maps business listings
8. Founder communities
9. X/Twitter
10. Instagram business pages

CONTACT ENTRY POINTS
1. Contact form
2. Public business email
3. LinkedIn company inbox
4. Founder/owner contact page
5. Booking/demo page

OUTREACH MESSAGES
1. Hey, I built a tool that turns any niche into a strategic market brief in seconds. Thought it might be useful if you pitch or sell into new verticals.
2. Quick question: how do you currently validate a market before building an offer for it?
3. I’m testing a niche intelligence tool for agencies and consultants. Want me to generate one brief for your market?
4. I built an AI market brief generator for founders and agencies. It helps with positioning, competitors and monetization.
5. If you enter new niches often, this might save you hours of manual research.

FOLLOW-UPS
1. Just bumping this in case niche research is something you do manually today.
2. Happy to send a sample brief if useful.
3. I can generate one example for your niche and market.
4. Curious if this would be more useful for your team or your clients.
5. No rush — just thought it could save time if you explore new verticals often.

HOOKS
1. Free sample niche brief
2. 3 competitor angles in 30 seconds
3. AI market scan for your next offer
4. Stop guessing your niche
5. Validate before building

(Gemini quota exhausted fallback)
""")
