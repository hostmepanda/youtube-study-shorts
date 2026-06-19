#!/bin/bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
LOG="$ROOT/logs/daily.log"
PYTHON=/opt/homebrew/opt/python@3.11/bin/python3.11

cd "$ROOT"

echo "======================================" >> "$LOG"
echo "$(date '+%Y-%m-%d %H:%M:%S') — Daily run started" >> "$LOG"
echo "======================================" >> "$LOG"

# 1. Upload any approved videos from yesterday's review
echo "" >> "$LOG"
echo "▶ Uploading approved videos..." >> "$LOG"
$PYTHON pipeline/youtube_uploader.py >> "$LOG" 2>&1 || echo "  Upload step failed or nothing to upload" >> "$LOG"

# 2. Check there are unused texts available — across legacy output/texts/ AND all formats/*/drafts/
UNUSED=$($PYTHON - << 'EOF'
import json
from pathlib import Path
root = Path(".")

def count_unused(batch_files, used_file):
    used = set(json.loads(used_file.read_text())) if used_file.exists() else set()
    total = sum(len(json.loads(f.read_text())) for f in batch_files)
    return total - len(used)

legacy_dir = root / "output" / "texts"
unused = 0
if legacy_dir.exists():
    legacy_files = list(legacy_dir.glob("batch_*.json")) + list(legacy_dir.glob("parables_*.json"))
    unused = count_unused(legacy_files, legacy_dir / "used_texts.json")

formats_dir = root / "formats"
if formats_dir.exists():
    for fmt_dir in formats_dir.iterdir():
        drafts_dir = fmt_dir / "drafts"
        if drafts_dir.exists():
            unused += count_unused(list(drafts_dir.glob("*.json")), fmt_dir / "used.json")

print(unused)
EOF
)

echo "" >> "$LOG"
echo "▶ Unused texts available: $UNUSED" >> "$LOG"

if [ "$UNUSED" -lt 10 ]; then
  echo "  ⚠️  Less than 10 texts left — run /generate-texts in Claude Code to refill" >> "$LOG"
fi

# 3. Generate 10 shorts
echo "" >> "$LOG"
echo "▶ Generating 10 shorts..." >> "$LOG"

SUCCESS=0
FAIL=0

for i in $(seq 1 10); do
  echo "" >> "$LOG"
  echo "  [Short $i/10]" >> "$LOG"
  if $PYTHON main.py >> "$LOG" 2>&1; then
    SUCCESS=$((SUCCESS + 1))
  else
    FAIL=$((FAIL + 1))
    echo "  ✗ Short $i failed" >> "$LOG"
  fi
done

echo "" >> "$LOG"
echo "✓ Done — $SUCCESS generated, $FAIL failed" >> "$LOG"
echo "$(date '+%Y-%m-%d %H:%M:%S') — Run complete" >> "$LOG"
