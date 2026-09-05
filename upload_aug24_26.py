#!/usr/bin/env python3
"""Upload Aug 24-26 content (6 videos)."""
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


SCHEDULE = [
    # Aug 24
    ("formats/short-motivation/configs/new/short_20260821_071528.yaml",  et(2026, 8, 24,  9,  0)),
    ("formats/parable-classic/configs/new/classic_20260821_071727.yaml", et(2026, 8, 24, 16, 30)),
    ("formats/parable-animal/configs/new/animal_20260820_231421.yaml",   et(2026, 8, 24, 16, 30)),
    ("formats/short-motivation/configs/new/short_20260821_071550.yaml",  et(2026, 8, 24, 19,  0)),
    # Aug 25
    ("formats/parable-animal/configs/new/animal_20260820_231516.yaml",   et(2026, 8, 25, 16, 30)),
    # Aug 26
    ("formats/parable-animal/configs/new/animal_20260820_231627.yaml",   et(2026, 8, 26, 16, 30)),
]

creds = authenticate()
youtube = build("youtube", "v3", credentials=creds)

print(f"Uploading {len(SCHEDULE)} video(s)...\n")

for rel_path, publish_at in SCHEDULE:
    config_path = ROOT / rel_path
    if not config_path.exists():
        print(f"  Not found: {rel_path}"); continue

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
