#!/usr/bin/env python3
"""Upload 7 animal parables: Sep 9–15, 16:30 ET (parable slot — classics already occupy Sep 2–8)."""
from src.pipeline.youtube_uploader import authenticate, upload_video, append_schedule
from googleapiclient.discovery import build
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from pathlib import Path
import yaml

ET = ZoneInfo("America/New_York")

SCHEDULE = [
    ("formats/parable-animal/configs/waiting_upload/animal_20260902_115650.yaml", (2026, 9, 9,  16, 30)),
    ("formats/parable-animal/configs/waiting_upload/animal_20260902_115759.yaml", (2026, 9, 10, 16, 30)),
    ("formats/parable-animal/configs/waiting_upload/animal_20260902_115908.yaml", (2026, 9, 11, 16, 30)),
    ("formats/parable-animal/configs/waiting_upload/animal_20260902_120012.yaml", (2026, 9, 12, 16, 30)),
    ("formats/parable-animal/configs/waiting_upload/animal_20260902_120210.yaml", (2026, 9, 13, 16, 30)),
    ("formats/parable-animal/configs/waiting_upload/animal_20260902_120326.yaml", (2026, 9, 14, 16, 30)),
    ("formats/parable-animal/configs/waiting_upload/animal_20260902_120527.yaml", (2026, 9, 15, 16, 30)),
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
    append_schedule(new_path, video_id, publish_at, title, is_short=False)

    dt_et = datetime(yr, mo, dy, hr, mn, 0, tzinfo=ET)
    print(f"  ✅ https://youtube.com/watch?v={video_id}  [{dt_et.strftime('%b %d %H:%M ET')}]")

print("\n=== Done ===")
