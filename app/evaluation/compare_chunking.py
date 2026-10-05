import asyncio
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import subprocess

STRATEGIES = ["fixed", "sentence", "semantic"]

def update_env_strategy(strategy):
    with open("../.env" if os.path.basename(os.getcwd()) == "evaluation" else ".env", "r") as f:
        lines = f.readlines()
    with open("../.env" if os.path.basename(os.getcwd()) == "evaluation" else ".env", "w") as f:
        for line in lines:
            if line.startswith("CHUNKING_STRATEGY"):
                f.write(f"CHUNKING_STRATEGY={strategy}\n")
            else:
                f.write(line)

print("This script requires manual steps between strategies — see instructions printed below.")
for strategy in STRATEGIES:
    print(f"\n{'='*50}\nSTRATEGY: {strategy}\n{'='*50}")
    print(f"1. Set CHUNKING_STRATEGY={strategy} in .env")
    print(f"2. Run: docker exec -it ai-platform-db psql -U aiuser -d ai_platform -c \"DELETE FROM chunks; DELETE FROM documents;\"")
    print(f"3. Re-upload your PDF via curl")
    print(f"4. Run: python evaluation/run_eval.py")
    print(f"5. Record the average recall score")