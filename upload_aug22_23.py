#!/usr/bin/env python3
"""Custom upload: Aug 22-23 schedule.

Run today (Aug 22): uploads 6 videos (Aug 22 full + Aug 23 shorts)
Run tomorrow (Aug 23): uploads 2 videos (Aug 23 parables)

Usage:
    python3 upload_aug22_23.py          # today's batch (6)
    python3 upload_aug22_23.py --day2   # tomorrow's batch (2)
"""
import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

from dotenv import load_dotenv
load_dotenv()

sys.path.insert(0, str(Path(__file__).parent))
from src.pipeline.youtube_uploader import authenticate, upload_video, resolve_thumbnail, append_schedule

ROOT = Path(__file__).parent
ET = ZoneInfo("America/New_York")


def et(year, month, day, hour, minute):
    return datetime(year, month, day, hour, minute, 0, tzinfo=ET)\
        .astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")


SCHEDULE_DAY1 = [
    # Aug 22
    ("formats/short-motivation/configs/new/short_20260807_210317.yaml",   et(2026, 8, 22,  9,  0)),
    ("formats/parable-classic/configs/new/classic_20260821_071615.yaml",  et(2026, 8, 22, 16, 30)),
    ("formats/parable-animal/configs/new/animal_20260820_231234.yaml",    et(2026, 8, 22, 16, 30)),
    ("formats/short-motivation/configs/new/short_20260807_210349.yaml",   et(2026, 8, 22, 19,  0)),
    # Aug 23 shorts (uploaded today to preserve quota tomorrow)
    ("formats/short-motivation/configs/new/short_20260821_071441.yaml",   et(2026, 8, 23,  9,  0)),
    ("formats/short-motivation/configs/new/short_20260821_071506.yaml",   et(2026, 8, 23, 19,  0)),
]

SCHEDULE_DAY2 = [
    # Aug 23 — shorts missed today + parables
    ("formats/short-motivation/configs/new/short_20260821_071441.yaml",   et(2026, 8, 23,  9,  0)),
    ("formats/parable-classic/configs/new/classic_20260821_071655.yaml",  et(2026, 8, 23, 16, 30)),
    ("formats/parable-animal/configs/new/animal_20260820_231328.yaml",    et(2026, 8, 23, 16, 30)),
    ("formats/short-motivation/configs/new/short_20260821_071506.yaml",   et(2026, 8, 23, 19,  0)),
]

parser = argparse.ArgumentParser()
parser.add_argument("--day2", action="store_true", help="Upload Aug 23 parables (run tomorrow)")
args = parser.parse_args()

schedule = SCHEDULE_DAY2 if args.day2 else SCHEDULE_DAY1

import yaml as yaml_lib
from googleapiclient.discovery import build

creds = authenticate()
youtube = build("youtube", "v3", credentials=creds)

print(f"Uploading {len(schedule)} video(s)...\n")

for rel_path, publish_at in schedule:
    config_path = ROOT / rel_path
    if not config_path.exists():
        print(f"  ✗ Not found: {rel_path}"); continue

    fmt_name = config_path.parent.parent.parent.name
    dt_et = datetime.strptime(publish_at, "%Y-%m-%dT%H:%M:%S.000Z")\
        .replace(tzinfo=timezone.utc).astimezone(ET)
    print(f"▶ {config_path.name}  →  {dt_et.strftime('%b %d %H:%M ET')}")

    try:
        video_id = upload_video(youtube, config_path, publish_at)
        is_short = fmt_name != "long-monologue"
        url = f"https://youtube.com/shorts/{video_id}" if is_short else f"https://youtube.com/watch?v={video_id}"
        print(f"  ✓ {url}")

        # Write video_id and publish_at back into yaml
        config = yaml_lib.safe_load(config_path.read_text())
        config["youtube"]["video_id"] = video_id
        config["youtube"]["publish_at"] = publish_at
        config_path.write_text(yaml_lib.dump(config, allow_unicode=True, sort_keys=False))

        # Append to schedule.md
        meta = config.get("youtube", {})
        append_schedule(config_path, video_id, publish_at, meta.get("title", ""), is_short)

        # Move to archive
        archive_dir = config_path.parent.parent / "archive"
        archive_dir.mkdir(parents=True, exist_ok=True)
        config_path.rename(archive_dir / config_path.name)
        print()

    except Exception as e:
        print(f"  ✗ Failed: {e}\n")

print("Done.")
