
import os
from google import genai

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
client = genai.Client(api_key=GEMINI_API_KEY)

print("\nLEADHUNTER AGENT")
print("------------------")

product = "AI Niche Market Brief Generator"

prompt = f"""
You are a growth strategist.

Product:
{product}

Generate:

1) 10 potential customer types
2) 10 niches that would benefit from this product
3) 10 outreach messages to get them to try it

Format:

CUSTOMERS:
- ...

NICHES:
- ...

MESSAGES:
- ...
"""

response = client.models.generate_content(
    model="gemini-1.5-flash",
    contents=prompt
)

print(response.text)
