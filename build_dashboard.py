from pathlib import Path

base = Path.home() / "ai_factory"

def latest(folder, pattern):
    p = base / folder
    if not p.exists():
        return "", ""
    files = sorted(p.glob(pattern), reverse=True)
    if not files:
        return "", ""
    f = files[0]
    try:
        return str(f), f.read_text()[:2500]
    except Exception:
        return str(f), ""

daily_path, daily_text = latest("daily_packs", "daily_pack_*.txt")
client_path, client_text = latest("client_hunter", "client_hunter_*.txt")
sales_path, sales_text = latest("sales_queue", "sales_queue_*.txt")
lead_path, lead_text = latest("leads", "lead_machine_*.txt")
acq_path, acq_text = latest("client_acquisition", "client_acquisition_*.txt")
acf_path, acf_text = latest("auto_client_finder", "auto_client_finder_*.txt")
aop_path, aop_text = latest("auto_outreach", "auto_outreach_*.txt")
dsr_path, dsr_text = latest("daily_sales", "daily_sales_*.txt")
harv_path, harv_text = latest("harvester", "harvester_*.txt")
ins_path, ins_text = latest("insight_engine", "insights_*.txt")

today_niche = "Marketing Agencies"
if daily_text:
    for line in daily_text.splitlines():
        line = line.strip()
        if line and not line.startswith("[DEMO"):
            today_niche = line
            break

today_offer = "Custom niche brief for €29"

html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>AI Factory Dashboard</title>

<style>
body {{
font-family: Arial, sans-serif;
background:#f6f7fb;
margin:0;
padding:40px;
color:#111;
}}

.container {{
max-width:1200px;
margin:auto;
}}

h1 {{
font-size:40px;
margin-bottom:10px;
}}

p {{
color:#555;
}}

.section {{
margin-top:40px;
}}

.grid {{
display:grid;
grid-template-columns: repeat(auto-fit, minmax(260px,1fr));
gap:20px;
}}

.card {{
background:white;
padding:20px;
border-radius:12px;
margin-top:15px;
box-shadow:0 8px 18px rgba(0,0,0,0.05);
}}

.badge {{
display:inline-block;
padding:6px 10px;
border-radius:999px;
font-size:12px;
font-weight:bold;
background:#e8f0fe;
color:#1a73e8;
margin-bottom:12px;
}}

.button {{
display:inline-block;
padding:12px 16px;
background:#111;
color:white;
text-decoration:none;
border-radius:8px;
margin-right:10px;
margin-top:10px;
}}

pre {{
white-space:pre-wrap;
font-size:14px;
line-height:1.5;
}}

ul {{
padding-left:18px;
}}
</style>
</head>

<body>

<div class="container">

<h1>AI Factory Dashboard</h1>
<p>Operational control room for your AI startup machine.</p>

<div class="section">
<h2>Execution Cockpit</h2>

<div class="grid">

<div class="card">
<div class="badge">TODAY NICHE</div>
<h3>{today_niche}</h3>
<p>Primary niche to attack today.</p>
</div>

<div class="card">
<div class="badge">TODAY OFFER</div>
<h3>{today_offer}</h3>
<p>Push this offer in outreach and content.</p>
</div>

<div class="card">
<div class="badge">TODAY ACTIONS</div>
<ul>
<li>Contact 3 prospects</li>
<li>Generate 1 sample brief</li>
<li>Publish 1 post with CTA</li>
</ul>
</div>

<div class="card">
<div class="badge">LINKS</div>
<a class="button" href="https://ai-factory-nicodemo.onrender.com" target="_blank">Open SaaS</a>
<a class="button" href="https://getnichebriefai.netlify.app/" target="_blank">Open Landing</a>
</div>

</div>
</div>

<div class="section">
<h2>Daily Pack</h2>
<div class="card">
<a class="button" href="file://{daily_path}" target="_blank">Open File</a>
<pre>{daily_text or "No daily pack yet"}</pre>
</div>
</div>

<div class="section">
<h2>Daily Sales Routine</h2>
<div class="card">
<a class="button" href="file://{dsr_path}" target="_blank">Open File</a>
<pre>{dsr_text or "No daily sales routine yet"}</pre>
</div>
</div>

<div class="section">
<h2>Client Hunter</h2>
<div class="card">
<a class="button" href="file://{client_path}" target="_blank">Open File</a>
<pre>{client_text or "No client hunter yet"}</pre>
</div>
</div>

<div class="section">
<h2>Sales Queue</h2>
<div class="card">
<a class="button" href="file://{sales_path}" target="_blank">Open File</a>
<pre>{sales_text or "No sales queue yet"}</pre>
</div>
</div>

<div class="section">
<h2>Lead Machine</h2>
<div class="card">
<a class="button" href="file://{lead_path}" target="_blank">Open File</a>
<pre>{lead_text or "No lead machine yet"}</pre>
</div>
</div>

<div class="section">
<h2>Client Acquisition Engine</h2>
<div class="card">
<a class="button" href="file://{acq_path}" target="_blank">Open File</a>
<pre>{acq_text or "No client acquisition output yet"}</pre>
</div>
</div>

<div class="section">
<h2>Auto Client Finder</h2>
<div class="card">
<a class="button" href="file://{acf_path}" target="_blank">Open File</a>
<pre>{acf_text or "No auto client finder output yet"}</pre>
</div>
</div>


<div class="section">
<h2>Auto Outreach Engine</h2>
<div class="card">
<a class="button" href="file://{aop_path}" target="_blank">Open File</a>
<pre>{aop_text or "No auto outreach output yet"}</pre>
</div>
</div>


<div class="section">
<h2>Harvester Queue</h2>
<div class="card">
<a class="button" href="file://{harv_path}" target="_blank">Open File</a>
<pre>{harv_text or "No harvester queue yet"}</pre>
</div>
</div>


<div class="section">
<h2>Insight Engine</h2>
<div class="card">
<a class="button" href="file://{ins_path}" target="_blank">Open File</a>
<pre>{ins_text or "No insights yet"}</pre>
</div>
</div>

</div>

</body>
</html>
"""

(base / "dashboard.html").write_text(html)
print("dashboard rebuilt with execution cockpit")
