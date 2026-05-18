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

# 2. Check there are unused texts available
UNUSED=$($PYTHON - << 'EOF'
import json
from pathlib import Path
root = Path(".")
used = set(json.loads((root / "output/texts/used_texts.json").read_text())) if (root / "output/texts/used_texts.json").exists() else set()
total = sum(len(json.loads(f.read_text())) for f in (root / "output/texts").glob("batch_*.json"))
print(total - len(used))
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
