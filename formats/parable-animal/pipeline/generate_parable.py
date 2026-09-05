#!/usr/bin/env python3
"""Generate one animal parable from the next pending seed via Premiss llm-v2.

Usage:
    python3 formats/parable-animal/pipeline/generate_parable.py [seed_id]

If seed_id is omitted, picks the first pending seed from seeds.json.
Saves the result to formats/parable-animal/drafts/parables_YYYYMMDD_HHMMSS.json.
"""
import json, os, sys, urllib.request, ssl, time
from pathlib import Path
from datetime import datetime

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

FMT_DIR    = Path(__file__).parent.parent
SEEDS_FILE = FMT_DIR / "seeds.json"
USED_FILE  = FMT_DIR / "used.json"
DRAFTS_DIR = FMT_DIR / "drafts"
DRAFTS_DIR.mkdir(exist_ok=True)

# Pick seed
seeds = json.loads(SEEDS_FILE.read_text())
if len(sys.argv) > 1:
    seed = next((s for s in seeds if s["id"] == sys.argv[1]), None)
    if not seed:
        print(f"Seed {sys.argv[1]} not found"); sys.exit(1)
else:
    seed = next((s for s in seeds if s["status"] == "pending"), None)
    if not seed:
        print("No pending seeds. Run generate_seeds.py first."); sys.exit(1)

print(f"Using seed: {seed['id']}")
print(f"  Animals:  {seed['animals']}")
print(f"  Want:     {seed['want']}")
print(f"  Obstacle: {seed['obstacle']}")
print(f"  Absurd:   {seed['absurd']}")
print(f"  Ending:   {seed['ending_hint']}")
print(f"  Theme:    {seed['theme']}")

# Find next animal_NNN id
raw = json.loads(USED_FILE.read_text()) if USED_FILE.exists() else []
used_ids = [e["id"] if isinstance(e, dict) else e for e in raw]
draft_ids = []
for f in DRAFTS_DIR.glob("parables_*.json"):
    for p in json.loads(f.read_text()):
        if isinstance(p, dict) and "id" in p:
            draft_ids.append(p["id"])
all_ids = used_ids + draft_ids
nums = [int(i.split("_")[1]) for i in all_ids if i.startswith("animal_") and i.split("_")[1].isdigit()]
next_num = max(nums) + 1 if nums else 1
next_id = f"animal_{next_num:03d}"

dialogue_block = ""
if seed.get("style") == "dialogue":
    dialogue_block = (
        "\n## Dialogue requirement\n"
        "This parable must include natural spoken dialogue between the characters.\n"
        "Use em dash for speech (like classic parables): — Like this, said the horse.\n"
        "At least 4 screens should be direct speech.\n"
        "Dialogue should carry the turning point, not narration."
    )

animals_str = " and ".join(seed["animals"])
PROMPT = f"""Write a short animal parable as JSON. Animals: {animals_str}.
{seed["want"]}. Obstacle: {seed["obstacle"]}.
Absurd (deadpan, nobody reacts): {seed["absurd"]}.
Ending: {seed["ending_hint"]}.
{dialogue_block}8-10 screens. Screen 0: hook max 10 words, two plain facts. Final screen: 3-6 words, absurd prop reappears.

Output valid JSON only (no markdown):
{{"id": "{next_id}", "topic": "...", "type": "parable", "mood": "parable", "keywords": ["crow branch", "turtle grass"], "video_queries": ["crow sitting branch", "turtle walking meadow"], "screens": [{{"screen": 0, "text": "hook"}}, {{"screen": 1, "text": "..."}}, {{"screen": 9, "text": "last line."}}]}}"""

SCHEMA = {
    "type": "object",
    "required": ["id", "topic", "type", "mood", "keywords", "video_queries", "screens"],
    "properties": {
        "id": {"type": "string"},
        "topic": {"type": "string"},
        "type": {"type": "string", "enum": ["parable"]},
        "mood": {"type": "string", "enum": ["parable"]},
        "keywords": {"type": "array", "items": {"type": "string"}, "minItems": 2, "maxItems": 4},
        "video_queries": {"type": "array", "items": {"type": "string"}, "minItems": 5, "maxItems": 8},
        "screens": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["screen", "text"],
                "properties": {
                    "screen": {"type": "integer"},
                    "text": {"type": "string"}
                }
            }
        }
    }
}

body = json.dumps({
    "input": f"Write an animal parable: {seed['want']}",
    "steps": [{
        "name": "llm-v2",
        "options": {
            "llmProvider": "synopsis-gemma",
            "llmModel": "gemma4-26b-a4b-qat",
            "prompt": PROMPT,
            "llmOutputField": "summary"
        }
    }],
    "ttl": 1
}).encode()

def api(path, data=None, method=None):
    req = urllib.request.Request(
        f"{BASE_URL}/api/v2{path}",
        data=data,
        headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
        method=method or ("POST" if data else "GET")
    )
    with urllib.request.urlopen(req, context=CTX) as r:
        return json.loads(r.read())

def run_task():
    result = api("/tasks", body, "POST")
    if not result.get("success"):
        print("Error:", result); return None
    task_id = result["data"]["id"]
    print(f"Task: {task_id}\nPolling...")
    while True:
        t = api(f"/tasks/{task_id}")["data"]
        print(f"  {t['status']}", flush=True)
        if t["status"] == "completed":
            raw = t["output"]["summary"]
            if isinstance(raw, str):
                if "```" in raw:
                    raw = raw.split("```")[1]
                    if raw.startswith("json"): raw = raw[4:]
                raw = raw.strip()
                if not raw:
                    print("  Empty response — will retry")
                    return None
                try:
                    return json.loads(raw)
                except json.JSONDecodeError:
                    last_complete = raw.rfind('{"screen":')
                    if last_complete != -1:
                        prev_close = raw.rfind('}', 0, last_complete)
                        if prev_close != -1:
                            try:
                                p = json.loads(raw[:prev_close + 1] + "]}")
                                print(f"  (recovered truncated JSON, {len(p.get('screens',[]))} screens)")
                                return p
                            except json.JSONDecodeError:
                                pass
                    print("  Truncated JSON unrecoverable — will retry")
                    return None
            return raw
        elif t["status"] == "failed":
            print("FAILED:", t.get("error")); return None
        time.sleep(15)

parable = None
for attempt in range(1, 4):
    print(f"\nAttempt {attempt}/3...")
    parable = run_task()
    if parable:
        break
    if attempt < 3:
        print("  Waiting 10s before retry...")
        time.sleep(10)

if not parable:
    print("All 3 attempts failed"); sys.exit(1)

# Enforce correct fixed fields regardless of what the LLM returned
parable["type"] = "parable"
parable["mood"] = "parable"

# Save draft
ts = datetime.now().strftime("%Y%m%d_%H%M%S")
out_file = DRAFTS_DIR / f"parables_{ts}.json"
out_file.write_text(json.dumps([parable], indent=2, ensure_ascii=False))

# Mark seed as used
seed["status"] = "used"
SEEDS_FILE.write_text(json.dumps(seeds, indent=2, ensure_ascii=False))

print(f"\nSaved: {out_file}")
print(f"Seed {seed['id']} marked as used\n")
print("=== TEXT ===")
for s in parable["screens"]:
    print(s["text"])
