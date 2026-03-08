import requests
import json
from google import genai

SUPABASE_URL = "https://zqjkguanvwptqloonety.supabase.co"
SUPABASE_KEY = "SUPABASE_PUBLISHABLE_KEY_PLACEHOLDER"
GEMINI_API_KEY = "GEMINI_API_KEY_PLACEHOLDER"

client = genai.Client(api_key=GEMINI_API_KEY)

def clean_json(text):
    text = text.strip()
    text = text.replace("```json", "").replace("```", "").strip()
    return json.loads(text)

prompt = """
Generate 10 simple online micro business ideas for a mostly-automated AI revenue factory.

For each idea, return:
- idea_name
- niche
- business_model
- monetization
- automation_score (1-10)
- seo_score (1-10)
- overall_score (1-100)
- verdict ("save" or "skip")

Return ONLY valid JSON as an array of objects.
"""

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt,
)

items = clean_json(response.text)

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=representation"
}

for item in items:
    idea_name = item.get("idea_name", "Untitled idea")
    overall_score = int(item.get("overall_score", 50))
    verdict = str(item.get("verdict", "skip")).lower()

    data = {
        "idea_name": idea_name,
        "niche": item.get("niche", "AI tools"),
        "business_model": item.get("business_model", "micro SaaS"),
        "monetization": item.get("monetization", "subscription"),
        "automation_score": int(item.get("automation_score", 5)),
        "seo_score": int(item.get("seo_score", 5)),
        "overall_score": overall_score,
        "status": "new"
    }

    if verdict == "save" and overall_score >= 80:
        resp = requests.post(
            f"{SUPABASE_URL}/rest/v1/ideas",
            headers=headers,
            data=json.dumps(data)
        )
        print("Saved:", idea_name, "| Score:", overall_score, "| Status:", resp.status_code)
    else:
        print("Skipped:", idea_name, "| Score:", overall_score)
