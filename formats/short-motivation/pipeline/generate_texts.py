#!/usr/bin/env python3
"""Generate a batch of 5 motivational texts via Premiss LLM.

Usage:
    python3 formats/short-motivation/pipeline/generate_texts.py [--model MODEL]

Models:
    gemma4-26b-a4b-qat  (synopsis-gemma)  — default
    qwen3.5-27b         (synopsis-qwen)   — alternative
    qwen3.6-27b         (synopsis-qwen)   — alternative (32k ctx)
"""
import json, os, sys, re, urllib.request, ssl, time, argparse
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

parser = argparse.ArgumentParser()
parser.add_argument("--model", default="gemma4-26b-a4b-qat",
                    choices=["gemma4-26b-a4b-qat", "qwen3.5-27b", "qwen3.6-27b"])
args = parser.parse_args()

PROVIDER = "synopsis-gemma" if args.model.startswith("gemma") else "synopsis-qwen"
MTP = args.model.startswith("qwen")

FMT_DIR    = Path(__file__).parent.parent
DRAFTS_DIR = FMT_DIR / "drafts"
TOPICS_FILE = FMT_DIR / "topics.md"
USED_FILE  = FMT_DIR / "used.json"
DRAFTS_DIR.mkdir(exist_ok=True)

# Find next text ID
raw = json.loads(USED_FILE.read_text()) if USED_FILE.exists() else []
used_ids = [e["id"] if isinstance(e, dict) else e for e in raw]
draft_ids = []
for f in DRAFTS_DIR.glob("batch_*.json"):
    for t in json.loads(f.read_text()):
        if isinstance(t, dict) and "id" in t:
            draft_ids.append(t["id"])
all_ids = used_ids + draft_ids
nums = [int(i.split("_")[1]) for i in all_ids if i.startswith("text_") and i.split("_")[1].isdigit()]
next_num = max(nums) + 1 if nums else 1

# Read last 20 used final lines for dedup
topics_text = TOPICS_FILE.read_text()
final_lines_raw = re.findall(r'text_\d+: "(.+?)"', topics_text)
recent_finals = final_lines_raw[-20:] if len(final_lines_raw) > 20 else final_lines_raw

ids = [f"text_{next_num + i:03d}" for i in range(5)]
ids_str = ", ".join(ids)

STRUCTURES = """1. Problem→Root cause→Fix
2. Observation→Twist→Call to action
3. Countdown/escalation
4. They vs You contrast
5. Myth→Reality→Action
6. Small truth→Bigger truth→Biggest truth
7. Direct address/confession
8. Story fragment (she/he moved, studied, now fluent)
9. Repetition/rhythm
10. Question→Silence→Answer"""

RECENT = "\n".join(f'- "{l}"' for l in recent_finals)

PROMPT = f"""Write 5 short motivational texts for people learning a foreign language (Spanish, French, Japanese, etc.). Americans learning — NOT people learning English.

Each text:
- 5-7 lines, each line max 8 words, each line on its own screen
- No line ends with a period
- Tone: direct, honest, a drop of warmth — not preachy or fluffy
- Use one of these structures (use all 5 different ones across the batch):
{STRUCTURES}

Avoid final lines similar to these recent ones:
{RECENT}

IDs to use: {ids_str}

Output valid JSON only (no markdown):
[{{"id": "text_066", "lines": ["Line 1", "Line 2", "Last line"], "mood": "motivational", "keywords": ["scene1", "scene2"]}}, ...]"""

print(f"Model: {args.model} ({PROVIDER})")
print(f"IDs: {ids[0]}–{ids[-1]}")
print(f"Prompt: {len(PROMPT)} chars\n")

def api(path, body=None, method=None):
    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(
        f"{BASE_URL}/api/v2{path}",
        data=data,
        headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
        method=method or ("POST" if data else "GET")
    )
    with urllib.request.urlopen(req, context=CTX) as r:
        return json.loads(r.read())

body = {
    "input": f"Generate motivational texts {ids[0]} to {ids[-1]}",
    "steps": [{"name": "llm-v2", "options": {
        "llmProvider": PROVIDER,
        "llmModel": args.model,
        "prompt": PROMPT,
        "llmOutputField": "summary"
    }}],
    "ttl": 1
}
if MTP:
    body["steps"][0]["options"]["llamaFlags"] = {"spec-type": "draft-mtp", "spec-draft-n-max": 2}

def run_task():
    result = api("/tasks", body, "POST")
    if not result.get("success"):
        print("Error:", result); return None
    task_id = result["data"]["id"]
    print(f"Task: {task_id}")
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
                    print("  Empty response — will retry"); return None
                try:
                    return json.loads(raw)
                except json.JSONDecodeError as e:
                    print(f"  JSON parse error: {e}"); return None
            return raw
        elif t["status"] == "failed":
            print("FAILED:", t.get("error")); return None
        time.sleep(15)

texts = None
for attempt in range(1, 4):
    print(f"Attempt {attempt}/3...")
    texts = run_task()
    if texts:
        break
    if attempt < 3:
        time.sleep(10)

if not texts:
    print("All 3 attempts failed"); sys.exit(1)

# Fix IDs if model drifted
for i, t in enumerate(texts):
    if i < len(ids):
        t["id"] = ids[i]

ts = datetime.now().strftime("%Y%m%d_%H%M%S")
out_file = DRAFTS_DIR / f"batch_{ts}_{args.model[:6]}.json"
out_file.write_text(json.dumps(texts, indent=2, ensure_ascii=False))

print(f"\nSaved: {out_file}")
print(f"\n=== TEXTS ({args.model}) ===\n")
for t in texts:
    print(f"[{t['id']}] mood:{t.get('mood','-')} | {' / '.join(t.get('lines',[]))[:80]}")
    print(f"  Final: \"{t['lines'][-1] if t.get('lines') else '?'}\"")
    print()
