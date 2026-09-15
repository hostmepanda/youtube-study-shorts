#!/usr/bin/env python3
"""Upload 7 animal parables: Sep 16-22, 18:00 ET (new animal-parable slot)."""
from src.pipeline.youtube_uploader import authenticate, upload_video, append_schedule
from googleapiclient.discovery import build
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from pathlib import Path
import yaml

ET = ZoneInfo("America/New_York")

SCHEDULE = [
    ("formats/parable-animal/configs/waiting_upload/animal_20260912_011021.yaml", (2026, 9, 16, 18, 0)),  # animal_052
    ("formats/parable-animal/configs/waiting_upload/animal_20260912_011205.yaml", (2026, 9, 17, 18, 0)),  # animal_053
    ("formats/parable-animal/configs/waiting_upload/animal_20260912_011314.yaml", (2026, 9, 18, 18, 0)),  # animal_054
    ("formats/parable-animal/configs/waiting_upload/animal_20260912_011419.yaml", (2026, 9, 19, 18, 0)),  # animal_055
    ("formats/parable-animal/configs/waiting_upload/animal_20260912_011613.yaml", (2026, 9, 20, 18, 0)),  # animal_056
    ("formats/parable-animal/configs/waiting_upload/animal_20260912_011709.yaml", (2026, 9, 21, 18, 0)),  # animal_057
    ("formats/parable-animal/configs/waiting_upload/animal_20260912_011815.yaml", (2026, 9, 22, 18, 0)),  # animal_058
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
