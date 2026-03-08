from flask import Flask, request, render_template_string
import os
from google import genai

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")

client = genai.Client(api_key=GEMINI_API_KEY)
app = Flask(__name__)

HTML = """
<!doctype html>
<html>
<head>
    <title>NicheBrief AI</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 900px;
            margin: 40px auto;
            padding: 20px;
            line-height: 1.5;
            background: #f6f7fb;
            color: #111;
        }
        h1 {
            font-size: 42px;
            margin-bottom: 10px;
        }
        p {
            color: #444;
        }
        input, button {
            width: 100%;
            padding: 12px;
            margin: 8px 0 16px 0;
            font-size: 16px;
            box-sizing: border-box;
        }
        button {
            cursor: pointer;
            background: #111;
            color: white;
            border: none;
            border-radius: 8px;
        }
        .card {
            background: white;
            padding: 24px;
            border-radius: 12px;
            box-shadow: 0 10px 20px rgba(0,0,0,0.05);
            margin-top: 24px;
        }
        .report {
            white-space: pre-wrap;
        }
    </style>
</head>
<body>
    <h1>NicheBrief AI</h1>
    <p>Generate instant market intelligence for any niche.</p>

    <div class="card">
        <form method="POST">
            <label>Niche</label>
            <input type="text" name="niche" placeholder="e.g. real estate agents" value="real estate agents" required>

            <label>Market / Location</label>
            <input type="text" name="market" placeholder="e.g. Milan" value="Milan" required>

            <button type="submit">Generate Brief</button>
        </form>
    </div>

    {% if report %}
    <div class="card">
        <h2>Brief</h2>
        <div class="report">{{ report }}</div>
    </div>
    {% endif %}

<hr style="margin-top:40px">
<div style="background:#111;padding:30px;border-radius:10px;color:white;margin-top:30px">
<h2>Want the full niche intelligence report?</h2>
<p>This preview is only a short market scan.</p>

<ul>
<li>Full competitor analysis</li>
<li>Lead generation strategies</li>
<li>Pricing opportunities</li>
<li>SEO keyword map</li>
</ul>

<a href="mailto:nicodemofemia92@gmail.com?subject=NicheBrief%20Request&body=Hi,%20I%20want%20a%20custom%20niche%20brief"
style="display:inline-block;margin-top:15px;padding:14px 22px;background:#4f46e5;color:white;text-decoration:none;border-radius:6px;font-weight:bold">
Get Full Brief – €29
</a>

</div>

</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    report = ""

    if request.method == "POST":
        niche = request.form["niche"]
        market = request.form["market"]

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

        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
            )
            report = response.text
        except Exception as e:
            report = f"""[DEMO MODE]

### 1. Market Overview
- Strong niche potential with room for differentiated positioning.
- Market research is usually slow and fragmented.
- Buyers value speed, clarity and relevance.

### 2. Customer Profiles
- Agencies
- Freelancers
- Founders
- Consultants

### 3. Competitor Patterns
- Generic messaging
- Weak specialization
- Manual research workflows

### 4. Marketing Angles
- Faster niche understanding
- Better strategic clarity
- Decision-ready market intelligence
- Specialized vertical insights
- AI-powered research assistant

### 5. Content Opportunities
- niche analysis posts
- competitor teardowns
- trend summaries
- location-based market snapshots
- positioning ideas

### 6. Growth Opportunities
- agency partnerships
- SEO landing pages
- founder communities
- outbound demos
- white-label reports

### 7. Monetization Models
- monthly subscription
- pay-per-brief
- agency plan
- custom reports

### 8. AI Opportunities
- automate niche research
- generate market briefs instantly
- scale content and strategy creation

Temporary fallback due to Gemini issue:
{str(e)}
"""

    return render_template_string(HTML, report=report)

if __name__ == "__main__":
    app.run(debug=True)
