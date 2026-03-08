
import subprocess
import os

BASE = os.path.expanduser("~/ai_factory")

steps = [
    ("Scout Agent", f"{BASE}/main.py"),
    ("Bridge Agent", f"{BASE}/bridge.py"),
    ("LeadHunter Agent", f"{BASE}/leadhunter.py"),
    ("AutoContent Agent", f"{BASE}/autocontent.py"),
]

print("\n🚀 AI FACTORY ALL-IN-ONE")
print("=" * 40)

for name, script in steps:
    print(f"\n▶ Running: {name}")
    print("-" * 40)
    subprocess.run(["python3", script])

print("\n✅ Factory cycle completed")
