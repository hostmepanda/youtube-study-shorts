#!/usr/bin/env python3
"""Upload 7 animal parables: Oct 7-13, 18:00 ET."""
from src.pipeline.youtube_uploader import authenticate, upload_video, append_schedule
from googleapiclient.discovery import build
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from pathlib import Path
import yaml

ET = ZoneInfo("America/New_York")

SCHEDULE = [
    ("formats/parable-animal/configs/waiting_upload/animal_20260925_121029.yaml", (2026, 10, 7, 18, 0)),   # animal_073
    ("formats/parable-animal/configs/waiting_upload/animal_20260925_121151.yaml", (2026, 10, 8, 18, 0)),   # animal_074
    ("formats/parable-animal/configs/waiting_upload/animal_20260925_121308.yaml", (2026, 10, 9, 18, 0)),   # animal_075
    ("formats/parable-animal/configs/waiting_upload/animal_20260925_121413.yaml", (2026, 10, 10, 18, 0)),  # animal_076
    ("formats/parable-animal/configs/waiting_upload/animal_20260925_121522.yaml", (2026, 10, 11, 18, 0)),  # animal_077
    ("formats/parable-animal/configs/waiting_upload/animal_20260925_121636.yaml", (2026, 10, 12, 18, 0)),  # animal_078
    ("formats/parable-animal/configs/waiting_upload/animal_20260925_121832.yaml", (2026, 10, 13, 18, 0)),  # animal_079
]

creds = authenticate()
yt = build("youtube", "v3", credentials=creds)

for config_path_str, (yr, mo, dy, hr, mn) in SCHEDULE:
    config_path = Path(config_path_str).resolve()
    if not config_path.exists():
        print(f"  SKIP (not found): {config_path.name}")
        continue

    publish_at = (datetime(yr, mo, dy, hr, mn, 0, tzinfo=ET)
                  .astimezone(timezone.utc)
                  .strftime("%Y-%m-%dT%H:%M:%S.000Z"))

    print(f"\n→ {config_path.name}")
    print(f"  publish: {yr}-{mo:02d}-{dy:02d} {hr:02d}:{mn:02d} ET")

    video_id = upload_video(yt, config_path, publish_at)

    archive_dir = config_path.parent.parent / "archive"
    archive_dir.mkdir(exist_ok=True)
    new_path = archive_dir / config_path.name
    config_path.rename(new_path)

    meta = yaml.safe_load(new_path.read_text())
    title = meta["youtube"]["title"]
    meta["youtube"]["video_id"] = video_id
    meta["youtube"]["publish_at"] = publish_at
    new_path.write_text(yaml.safe_dump(meta, sort_keys=False, allow_unicode=True))

    append_schedule(new_path, video_id, publish_at, title, is_short=False)

    dt_et = datetime(yr, mo, dy, hr, mn, 0, tzinfo=ET)
    print(f"  ✅ https://youtube.com/watch?v={video_id}  [{dt_et.strftime('%b %d %H:%M ET')}]")

print("\n=== Done ===")
