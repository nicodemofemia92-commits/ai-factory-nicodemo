import requests
from google import genai

GEMINI_API_KEY = "GEMINI_API_KEY_PLACEHOLDER"
SUPABASE_URL = "https://zqjkguanvwptqloonety.supabase.co"
SUPABASE_KEY = "SUPABASE_PUBLISHABLE_KEY_PLACEHOLDER"

client = genai.Client(api_key=GEMINI_API_KEY)

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=representation"
}

resp = requests.get(
    f"{SUPABASE_URL}/rest/v1/ideas?select=idea_name,overall_score&order=overall_score.desc&limit=1",
    headers=headers
)

ideas = resp.json()
print("Supabase response:", ideas)

if not isinstance(ideas, list) or len(ideas) == 0:
    print("Nessuna idea trovata.")
    raise SystemExit

idea_name = ideas[0]["idea_name"]
print("Idea scelta:", idea_name)

prompt = f"""
Create a short validation brief for this AI startup idea:

IDEA:
{idea_name}

Return bullet points for:
- what the product is
- target users
- key problem solved
- positioning
- monetization
- risks
"""

try:
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )
    report = response.text
except Exception as e:
    report = f"""[DEMO MODE]

- Product: lightweight AI startup idea
- Target users: freelancers, agencies, SMBs
- Problem solved: faster research and positioning
- Monetization: subscription / pay-per-use
- Risks: crowded AI space, API limits

Gemini fallback:
{str(e)}
"""

data = {
    "niche": idea_name,
    "market": "AI validation",
    "report": report
}

save_resp = requests.post(
    f"{SUPABASE_URL}/rest/v1/briefs",
    headers=headers,
    json=data
)

print("Brief status:", save_resp.status_code)
print("Bridge completato.")
