import subprocess
import os

BASE = os.path.expanduser("~/ai_factory")

print("🚀 Starting AI Factory")

print("\n1️⃣ Running Scout Agent (idea generation)")
subprocess.run(["python3", f"{BASE}/main.py"])

print("\n2️⃣ Running Bridge Agent (select best idea + create brief)")
subprocess.run(["python3", f"{BASE}/bridge.py"])

print("\n✅ Factory cycle completed")
