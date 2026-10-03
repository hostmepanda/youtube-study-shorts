#!/usr/bin/env python3
"""Upload everything in formats/<format>/configs/waiting_upload/ into the fixed daily ET slots.

Usage: python3 upload_queue.py <short-motivation|parable-classic|parable-animal> <YYYY-MM-DD> [slot_index]
Start day and slot (0-based, default 0) of the first queued video; videos go in sorted-filename order.
Safe to re-run after a quota error: uploaded yamls move to archive/, the rest stay queued,
so pass the day/slot of the first still-queued video.
"""
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

import yaml
from googleapiclient.discovery import build

from src.pipeline.youtube_uploader import authenticate, append_schedule, upload_video

ET = ZoneInfo("America/New_York")
SLOTS = {
    "short-motivation": [(8, 30), (14, 30)],
    "parable-classic": [(12, 0)],
    "parable-animal": [(18, 0)],
}

if len(sys.argv) not in (3, 4) or sys.argv[1] not in SLOTS:
    sys.exit(__doc__)

fmt = sys.argv[1]
day = date.fromisoformat(sys.argv[2])
slots = SLOTS[fmt]
first_slot = int(sys.argv[3]) if len(sys.argv) == 4 else 0
queued = sorted(Path(f"formats/{fmt}/configs/waiting_upload").glob("*.yaml"))
if not queued:
    sys.exit("Nothing queued.")

yt = build("youtube", "v3", credentials=authenticate())

for i, config_path in enumerate(queued):
    n = first_slot + i
    d = day + timedelta(days=n // len(slots))
    hh, mm = slots[n % len(slots)]
    publish_at = (datetime(d.year, d.month, d.day, hh, mm, tzinfo=ET)
                  .astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z"))
    print(f"\n→ {config_path.name}\n  publish: {d} {hh:02d}:{mm:02d} ET")

    video_id = upload_video(yt, config_path.resolve(), publish_at)

    new_path = config_path.resolve().parent.parent / "archive" / config_path.name
    new_path.parent.mkdir(exist_ok=True)
    config_path.rename(new_path)
    meta = yaml.safe_load(new_path.read_text())
    meta["youtube"]["video_id"] = video_id
    meta["youtube"]["publish_at"] = publish_at
    new_path.write_text(yaml.safe_dump(meta, sort_keys=False, allow_unicode=True))
    append_schedule(new_path, video_id, publish_at, meta["youtube"]["title"], is_short=(fmt == "short-motivation"))

    base = "shorts" if fmt == "short-motivation" else "watch?v="
    url = f"https://youtube.com/shorts/{video_id}" if base == "shorts" else f"https://youtube.com/watch?v={video_id}"
    print(f"  ✅ {url}")

print("\n=== Done ===")
