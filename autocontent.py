
import os
from google import genai

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
client = genai.Client(api_key=GEMINI_API_KEY)

print("\nAUTOCONTENT AGENT")
print("------------------")

product = "NicheBrief AI"
url = "https://ai-factory-nicodemo.onrender.com"

prompt = f"""
You are a SaaS growth copywriter.

Product:
{product}

Website:
{url}

Generate:

1) 5 LinkedIn posts to promote the product
2) 5 short X/Twitter hooks
3) 5 SEO article titles
4) 5 CTA lines

Rules:
- Make them practical
- Focus on founders, freelancers, agencies, consultants
- Emphasize market research, niche intelligence, positioning, and monetization
- Include the website URL when useful

Format clearly with sections:

LINKEDIN POSTS
1.
2.

X HOOKS
1.
2.

SEO TITLES
1.
2.

CTA
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
[DEMO MODE]

LINKEDIN POSTS
1. I built an AI tool that generates niche market briefs in seconds. It helps founders and agencies understand competitors, positioning and monetization faster.
2. Most people build before understanding the market. NicheBrief AI flips that: niche first, product second.
3. If you had to validate a niche in 30 seconds, what would you want to know first? Competitors? Positioning? Pricing? That's what NicheBrief AI does.
4. I turned market research into a simple AI workflow: niche in, strategic brief out.
5. Founders waste weeks on messy research. A structured niche brief can cut that down to minutes.

X HOOKS
1. Most startups fail before understanding the niche.
2. I built an AI that turns any niche into a market brief.
3. Want competitor + positioning + monetization in seconds?
4. Market research is broken. This fixes it.
5. Niche clarity > building faster.

SEO TITLES
1. How to Analyze Any Niche in Minutes with AI
2. Best AI Tool for Market Research and Niche Validation
3. How Founders Can Validate a Market Before Building
4. AI Market Brief Generator for Agencies and Freelancers
5. How to Find Positioning and Monetization Opportunities Fast

CTA
1. Try NicheBrief AI
2. Generate your niche brief
3. Get your market intelligence report
4. Stop guessing your market
5. Validate your niche faster

Temporary fallback because Gemini quota is exhausted.
Error:
""" + str(e))
