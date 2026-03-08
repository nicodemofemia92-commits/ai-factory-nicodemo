
import os
from datetime import datetime
from google import genai

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY","")
client = genai.Client(api_key=GEMINI_API_KEY)

today=datetime.now().strftime("%Y-%m-%d")

prompt="""
Create:

1 LinkedIn post
1 X thread
1 SEO article idea

about validating business niches using AI.
"""

try:
    r=client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    text=r.text
except:
    text="""
[DEMO TRAFFIC PACK]

LinkedIn Post:
Most founders waste weeks researching markets.
AI can generate a full niche brief in seconds.

X Thread:
1/ Most startups fail because they pick bad niches
2/ Instead of guessing, generate a market brief
3/ Look at competitors + positioning
4/ Validate before building
"""

folder=base/"traffic_engine"
folder.mkdir(exist_ok=True)

path=folder/f"traffic_{today}.txt"
path.write_text(text)
print("traffic generated:",path)
