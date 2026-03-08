from google import genai

GEMINI_API_KEY = "GEMINI_API_KEY_PLACEHOLDER"

client = genai.Client(api_key=GEMINI_API_KEY)

niche = input("Enter niche: ")
market = input("Enter market/location: ")

prompt = f"""
You are a senior market strategist.

NICHE:
{niche}

MARKET:
{market}

Create a structured niche brief including:

1. Market Overview
2. Customer Profiles
3. Competitor Patterns
4. Marketing Angles
5. Content Opportunities (10 ideas)
6. Growth Opportunities
7. Monetization Models
8. AI Opportunities

Use bullet points.
Keep it concise but strategic.
"""

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt,
)

print("\n\n===== NICHE BRIEF =====\n")
print(response.text)
