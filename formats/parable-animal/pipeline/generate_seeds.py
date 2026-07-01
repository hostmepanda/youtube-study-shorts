#!/usr/bin/env python3
"""Generate plot seeds for animal parables via Premiss llm-v2.

Usage:
    python3 formats/parable-animal/pipeline/generate_seeds.py [N]

Appends N new seeds to formats/parable-animal/seeds.json.
Default N = 10.
"""
import json, os, sys, urllib.request, ssl, time
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent.parent
ENV  = ROOT / ".env"

for line in ENV.read_text().splitlines():
    line = line.strip()
    if not line or line.startswith("#"): continue
    k, _, v = line.partition("=")
    os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))

API_KEY  = os.environ["PREMISS_API_KEY"]
BASE_URL = os.environ.get("PREMISS_API_URL", "https://core.premiss.ru")
CTX      = ssl.create_default_context()

SEEDS_FILE  = Path(__file__).parent.parent / "seeds.json"
TOPICS_FILE = Path(__file__).parent.parent / "topics.md"

N = int(sys.argv[1]) if len(sys.argv) > 1 else 10

existing_seeds = json.loads(SEEDS_FILE.read_text())
used_combos    = [f"{s['animals']} / {s['absurd']}" for s in existing_seeds]
topics_context = TOPICS_FILE.read_text()

PROMPT = f"""You are helping build a library of animal parable plot seeds for YouTube Shorts about language learning.

## Already used animal + device combinations (do not repeat):
{chr(10).join(f'- {c}' for c in used_combos) if used_combos else '(none yet)'}

## Context from the topics file:
{topics_context}

## Rules for each seed:
- Pick 2 animals from the pool (not the same pair used before)
- One character WANTS something specific from the other
- One clear obstacle (fear, pride, silence, overthinking)
- One absurd element — a surreal object or action, matter-of-fact, nobody reacts
- A hint for the ending — a simple action or plain sentence, no moral stated
- The theme must connect to language learning (fear of speaking, knowing vs. using, waiting to be ready, etc.)
- Vary the themes — not all about fear of speaking

Generate exactly {N} seeds. Output valid JSON array."""

SCHEMA = {
    "type": "array",
    "items": {
        "type": "object",
        "required": ["animals", "want", "obstacle", "absurd", "ending_hint", "theme"],
        "properties": {
            "animals":     {"type": "array", "items": {"type": "string"}, "minItems": 2, "maxItems": 3},
            "want":        {"type": "string"},
            "obstacle":    {"type": "string"},
            "absurd":      {"type": "string"},
            "ending_hint": {"type": "string"},
            "theme":       {"type": "string"}
        }
    }
}

body = json.dumps({
    "input": f"Generate {N} animal parable seeds for language learning YouTube Shorts",
    "steps": [{
        "name": "llm-v2",
        "options": {
            "llmProvider": "synopsis-qwen",
            "llmModel": "qwen3.5-35b-a3b",
            "prompt": PROMPT,
            "llmOutputField": "summary",
            "responseSchema": SCHEMA
        }
    }],
    "ttl": 1
}).encode()

def api(path, data=None, method="GET"):
    req = urllib.request.Request(
        f"{BASE_URL}/api/v2{path}",
        data=data,
        headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
        method=method or ("POST" if data else "GET")
    )
    with urllib.request.urlopen(req, context=CTX) as r:
        return json.loads(r.read())

print(f"Generating {N} seeds...")
result = api("/tasks", body, "POST")
if not result.get("success"):
    print("Error:", result); sys.exit(1)

task_id = result["data"]["id"]
print(f"Task: {task_id}")

while True:
    t = api(f"/tasks/{task_id}")["data"]
    print(f"  {t['status']}", flush=True)
    if t["status"] == "completed":
        seeds = t["output"]["summary"]
        break
    elif t["status"] == "failed":
        print("FAILED:", t.get("error")); sys.exit(1)
    time.sleep(15)

# Assign IDs and status
start = len(existing_seeds) + 1
for i, seed in enumerate(seeds):
    seed["id"] = f"seed_{start + i:03d}"
    seed["status"] = "pending"

existing_seeds.extend(seeds)
SEEDS_FILE.write_text(json.dumps(existing_seeds, indent=2, ensure_ascii=False))

print(f"\nAdded {len(seeds)} seeds to {SEEDS_FILE}")
for s in seeds:
    print(f"  [{s['id']}] {s['animals']} — {s['theme']}")
