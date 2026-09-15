#!/usr/bin/env python3
"""Upload 7 animal parables: Sep 23-29, 18:00 ET."""
from src.pipeline.youtube_uploader import authenticate, upload_video, append_schedule
from googleapiclient.discovery import build
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from pathlib import Path
import yaml

ET = ZoneInfo("America/New_York")

SCHEDULE = [
    ("formats/parable-animal/configs/waiting_upload/animal_20260915_072507.yaml", (2026, 9, 23, 18, 0)),  # animal_059
    ("formats/parable-animal/configs/waiting_upload/animal_20260915_072621.yaml", (2026, 9, 24, 18, 0)),  # animal_060
    ("formats/parable-animal/configs/waiting_upload/animal_20260915_072913.yaml", (2026, 9, 25, 18, 0)),  # animal_061
    ("formats/parable-animal/configs/waiting_upload/animal_20260915_073040.yaml", (2026, 9, 26, 18, 0)),  # animal_062
    ("formats/parable-animal/configs/waiting_upload/animal_20260915_073147.yaml", (2026, 9, 27, 18, 0)),  # animal_063
    ("formats/parable-animal/configs/waiting_upload/animal_20260915_073259.yaml", (2026, 9, 28, 18, 0)),  # animal_064
    ("formats/parable-animal/configs/waiting_upload/animal_20260915_073407.yaml", (2026, 9, 29, 18, 0)),  # animal_065
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
