
import os
from datetime import datetime
from pathlib import Path
from google import genai

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY","")
client = genai.Client(api_key=GEMINI_API_KEY)

today = datetime.now().strftime("%Y-%m-%d")
base = Path.home() / "ai_factory"

prompt = """
Create 20 short market insights that could be used as social posts.

For each insight return:

Niche
Top competitors
Positioning gap
Monetization angle

Keep each insight very short and punchy.
Focus on:
- marketing agencies
- seo consultants
- real estate
- ecommerce
- coaching
- ai startups
"""

try:
    r = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    text = r.text
except Exception as e:
    text = """
[DEMO INSIGHTS]

Niche: AI marketing agencies
Competitors: Jasper, Copy.ai
Gap: AI strategy consulting
Monetization: subscription playbooks

Niche: Real estate Milan
Competitors: Tecnocasa, Remax
Gap: AI valuation
Monetization: SaaS for landlords

Niche: SEO consultants
Competitors: Ahrefs agencies
Gap: AI SEO strategy
Monetization: monthly audits
"""

folder = base / "insight_engine"
folder.mkdir(exist_ok=True)

path = folder / f"insights_{today}.txt"
path.write_text(text)

print("insights generated:", path)
