
import os
from datetime import datetime
from google import genai

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
client = genai.Client(api_key=GEMINI_API_KEY)

today = datetime.now().strftime("%Y-%m-%d")

prompt = """
You are a startup sales operator.

Create a DAILY SALES ROUTINE to sell NicheBrief AI.

Return:

1. ONE niche to attack today
2. FIVE example prospects
3. THREE outreach messages
4. ONE follow-up message
5. ONE daily revenue task
6. ONE micro growth tactic

Keep it short and practical.
"""

try:

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    output = response.text

except Exception as e:

    output = f"""
[DEMO DAILY SALES ROUTINE]

NICHE TODAY
Marketing Agencies

PROSPECTS
GrowthLab Agency
Prime SEO Studio
Digital Boost Agency
Scale Marketing
BrandForge Studio

OUTREACH
Hey — quick question.

How do you usually validate a niche before building a service offer?

I built a tool that generates a structured niche market brief.

FOLLOW UP
Just checking if niche validation is something you do often.

DAILY TASK
Generate one sample brief for a marketing agency niche.

MICRO GROWTH
Post a LinkedIn thread:
"How I analyze a niche in 3 minutes with AI".
"""

print(output)

folder = os.path.expanduser("~/ai_factory/daily_sales")
os.makedirs(folder, exist_ok=True)

path = os.path.join(folder, f"daily_sales_{today}.txt")

with open(path,"w") as f:
    f.write(output)

print("\nSaved to:",path)
