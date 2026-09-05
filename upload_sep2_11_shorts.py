#!/usr/bin/env python3
"""Upload 10 motivational shorts: Sep 2–11, 09:00 ET."""
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from pathlib import Path
from src.pipeline.youtube_uploader import authenticate, upload_video, append_schedule
from googleapiclient.discovery import build

ET = ZoneInfo("America/New_York")

def et(year, month, day, hour, minute):
    return datetime(year, month, day, hour, minute, 0, tzinfo=ET)\
        .astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")

SCHEDULE = [
    # short_20260901_080209 already uploaded → Dald64MkU84
    ("formats/short-motivation/configs/new/short_20260901_080243.yaml", et(2026, 9, 3,  9, 0)),
    ("formats/short-motivation/configs/new/short_20260901_080305.yaml", et(2026, 9, 4,  9, 0)),
    ("formats/short-motivation/configs/new/short_20260901_080327.yaml", et(2026, 9, 5,  9, 0)),
    ("formats/short-motivation/configs/new/short_20260901_080349.yaml", et(2026, 9, 6,  9, 0)),
    ("formats/short-motivation/configs/new/short_20260901_080410.yaml", et(2026, 9, 7,  9, 0)),
    ("formats/short-motivation/configs/new/short_20260901_080432.yaml", et(2026, 9, 8,  9, 0)),
    ("formats/short-motivation/configs/new/short_20260901_080452.yaml", et(2026, 9, 9,  9, 0)),
    ("formats/short-motivation/configs/new/short_20260901_080514.yaml", et(2026, 9, 10, 9, 0)),
    ("formats/short-motivation/configs/new/short_20260901_080536.yaml", et(2026, 9, 11, 9, 0)),
]

creds = authenticate()
youtube = build("youtube", "v3", credentials=creds)

for config_path_str, publish_at in SCHEDULE:
    config_path = Path(config_path_str).resolve()

    print(f"\n→ {config_path.name}")
    print(f"  publish: {publish_at}")

    video_id = upload_video(youtube, config_path, publish_at)

    archive_dir = config_path.parent.parent / "archive"
    archive_dir.mkdir(exist_ok=True)
    new_path = archive_dir / config_path.name
    config_path.rename(new_path)

    append_schedule(new_path, video_id, publish_at,
                    title=__import__('yaml').safe_load(new_path.read_text())["youtube"]["title"],
                    is_short=True)

    dt_et = datetime.fromisoformat(publish_at.replace("Z", "+00:00")).astimezone(ET)
    print(f"  ✅ https://youtube.com/shorts/{video_id}  [{dt_et.strftime('%b %d %H:%M ET')}]")

print("\n=== Done ===")
