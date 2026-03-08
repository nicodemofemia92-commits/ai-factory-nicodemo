
import os
from datetime import datetime
from google import genai
from pathlib import Path

GEMINI_API_KEY=os.environ.get("GEMINI_API_KEY","")
client=genai.Client(api_key=GEMINI_API_KEY)

today=datetime.now().strftime("%Y-%m-%d")
base=Path.home()/ "ai_factory"

prompt="""
Write 3 outreach messages selling a niche intelligence brief for 29€.
Target: marketing agencies.
"""

try:
    r=client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    text=r.text
except:
    text="""
[DEMO OUTREACH]

Hey,
I built a tool that generates a structured niche brief for any market.
Would you like one for your agency niche?

Price is 29€.
"""

folder=base/"lead_reactor"
folder.mkdir(exist_ok=True)

path=folder/f"reactor_{today}.txt"
path.write_text(text)

print("lead reactor generated:",path)
