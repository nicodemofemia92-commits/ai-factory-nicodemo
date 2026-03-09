
from pathlib import Path

base = Path.home() / "ai_factory"

def read_file(path):
    try:
        return Path(path).read_text()[:4000]
    except:
        return "no data"

lead_queue = read_file(base / "lead_harvester_x10" / "top_ready_queue_x10.csv")
outreach_queue = read_file(base / "lead_harvester_x10" / "top_ready_outreach_x10.csv")

html = f"""
<html>
<head>
<title>AI Factory Dashboard</title>
<style>
body{{font-family:Arial;background:#0f172a;color:white;padding:40px}}
.section{{margin-bottom:40px}}
.card{{background:#1e293b;padding:20px;border-radius:10px}}
pre{{white-space:pre-wrap;font-size:12px}}
</style>
</head>

<body>

<h1>AI Factory Control Room</h1>

<div class="section">
<h2>Global Lead Queue</h2>
<div class="card">
<pre>{lead_queue}</pre>
</div>
</div>

<div class="section">
<h2>Global Outreach Queue</h2>
<div class="card">
<pre>{outreach_queue}</pre>
</div>
</div>

</body>
</html>
"""

out = base / "dashboard.html"
out.write_text(html)

print("dashboard rebuilt")
print(out)
