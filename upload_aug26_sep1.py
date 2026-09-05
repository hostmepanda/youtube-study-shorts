#!/usr/bin/env python3
"""Upload Aug 26 – Sep 1 content (revised after broken mp4 cleanup).

Already uploaded:
  Day1 (6): Aug 26 full + Aug 27 partial (09:00 short, classic, animal)
  Day2 partial (2): Aug 27 19:00 short, Aug 28 09:00 short

Remaining 15 uploads — split by quota day:
  --resume  (4): Aug 28 16:30 classic+animal, 19:00 short, Aug 29 09:00 short
  --day3    (6): Aug 29 16:30 classic, 19:00 short, Aug 30 09:00+16:30+19:00, Aug 31 09:00
  --day4    (5): Aug 31 16:30+19:00, Sep 1 09:00+16:30+19:00

Usage:
    python3 upload_aug26_sep1.py --resume   # run now (4 uploads)
    python3 upload_aug26_sep1.py --day3     # tomorrow after quota reset
    python3 upload_aug26_sep1.py --day4     # day after
"""
import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

from dotenv import load_dotenv
load_dotenv()

sys.path.insert(0, str(Path(__file__).parent))
from src.pipeline.youtube_uploader import authenticate, upload_video, append_schedule

ROOT = Path(__file__).parent
ET = ZoneInfo("America/New_York")

import yaml as yaml_lib
from googleapiclient.discovery import build


def et(year, month, day, hour, minute):
    return datetime(year, month, day, hour, minute, 0, tzinfo=ET)\
        .astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")


# Good files (all mp4s verified to exist)
C = [
    "formats/parable-classic/configs/new/classic_20260825_232615.yaml",  # C[0] → Aug 28
    "formats/parable-classic/configs/new/classic_20260825_232649.yaml",  # C[1] → Aug 29
    "formats/parable-classic/configs/new/classic_20260825_232829.yaml",  # C[2] → Aug 30
    "formats/parable-classic/configs/new/classic_20260825_232908.yaml",  # C[3] → Aug 31
    "formats/parable-classic/configs/new/classic_20260825_232944.yaml",  # C[4] → Sep 1
]

A = [
    "formats/parable-animal/configs/new/animal_20260825_233146.yaml",    # A[0] → Aug 28
]

S = [
    "formats/short-motivation/configs/new/short_20260825_232042.yaml",   # S[0] → Aug 28 19:00
    "formats/short-motivation/configs/new/short_20260825_232104.yaml",   # S[1] → Aug 29 09:00
    "formats/short-motivation/configs/new/short_20260825_232126.yaml",   # S[2] → Aug 29 19:00
    "formats/short-motivation/configs/new/short_20260825_232156.yaml",   # S[3] → Aug 30 09:00
    "formats/short-motivation/configs/new/short_20260825_232220.yaml",   # S[4] → Aug 30 19:00
    "formats/short-motivation/configs/new/short_20260825_232243.yaml",   # S[5] → Aug 31 09:00
    "formats/short-motivation/configs/new/short_20260825_232305.yaml",   # S[6] → Aug 31 19:00
    "formats/short-motivation/configs/new/short_20260825_232327.yaml",   # S[7] → Sep 1 09:00
    "formats/short-motivation/configs/new/short_20260825_232402.yaml",   # S[8] → Sep 1 19:00
]

SCHEDULE_RESUME = [
    # Aug 28 remaining
    (C[0],  et(2026, 8, 28, 16, 30)),   # classic
    (A[0],  et(2026, 8, 28, 16, 30)),   # animal
    (S[0],  et(2026, 8, 28, 19,  0)),   # short
    # Aug 29 partial
    (S[1],  et(2026, 8, 29,  9,  0)),   # short
]

SCHEDULE_DAY3 = [
    # Aug 29 remaining
    (C[1],  et(2026, 8, 29, 16, 30)),   # classic
    (S[2],  et(2026, 8, 29, 19,  0)),   # short
    # Aug 30 (3)
    (S[3],  et(2026, 8, 30,  9,  0)),   # short
    (C[2],  et(2026, 8, 30, 16, 30)),   # classic
    (S[4],  et(2026, 8, 30, 19,  0)),   # short
    # Aug 31 partial
    (S[5],  et(2026, 8, 31,  9,  0)),   # short
]

SCHEDULE_DAY4 = [
    # Aug 31 remaining
    (C[3],  et(2026, 8, 31, 16, 30)),   # classic
    (S[6],  et(2026, 8, 31, 19,  0)),   # short
    # Sep 1 (3)
    (S[7],  et(2026, 9,  1,  9,  0)),   # short
    (C[4],  et(2026, 9,  1, 16, 30)),   # classic
    (S[8],  et(2026, 9,  1, 19,  0)),   # short
]

parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group()
group.add_argument("--resume", action="store_true", help="4 remaining videos (run now)")
group.add_argument("--day3", action="store_true", help="6 videos (tomorrow after quota reset)")
group.add_argument("--day4", action="store_true", help="5 videos (day after)")
args = parser.parse_args()

if args.day3:
    schedule = SCHEDULE_DAY3
    label = "Day 3 (6 videos)"
elif args.day4:
    schedule = SCHEDULE_DAY4
    label = "Day 4 (5 videos)"
else:
    schedule = SCHEDULE_RESUME
    label = "Resume (4 videos: Aug 28 + Aug 29 morning)"

creds = authenticate()
youtube = build("youtube", "v3", credentials=creds)

print(f"=== {label} ===\n")

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

        config = yaml_lib.safe_load(config_path.read_text())
        config["youtube"]["video_id"] = video_id
        config["youtube"]["publish_at"] = publish_at
        config_path.write_text(yaml_lib.dump(config, allow_unicode=True, sort_keys=False))

        meta = config.get("youtube", {})
        append_schedule(config_path, video_id, publish_at, meta.get("title", ""), is_short)

        archive_dir = config_path.parent.parent / "archive"
        archive_dir.mkdir(parents=True, exist_ok=True)
        config_path.rename(archive_dir / config_path.name)
        print()

    except Exception as e:
        print(f"  ✗ Failed: {e}\n")

print("Done.")
