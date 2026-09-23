#!/usr/bin/env python3
"""Upload 10 motivational shorts: Oct 3-7, 08:30/14:30 ET."""
from src.pipeline.youtube_uploader import authenticate, upload_video, append_schedule
from googleapiclient.discovery import build
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from pathlib import Path
import yaml

ET = ZoneInfo("America/New_York")

SCHEDULE = [
    ("formats/short-motivation/configs/waiting_upload/short_20260923_065711.yaml", (2026, 10, 3, 8, 30)),
    ("formats/short-motivation/configs/waiting_upload/short_20260923_065734.yaml", (2026, 10, 3, 14, 30)),
    ("formats/short-motivation/configs/waiting_upload/short_20260923_065757.yaml", (2026, 10, 4, 8, 30)),
    ("formats/short-motivation/configs/waiting_upload/short_20260923_065818.yaml", (2026, 10, 4, 14, 30)),
    ("formats/short-motivation/configs/waiting_upload/short_20260923_065840.yaml", (2026, 10, 5, 8, 30)),
    ("formats/short-motivation/configs/waiting_upload/short_20260923_065901.yaml", (2026, 10, 5, 14, 30)),
    ("formats/short-motivation/configs/waiting_upload/short_20260923_065924.yaml", (2026, 10, 6, 8, 30)),
    ("formats/short-motivation/configs/waiting_upload/short_20260923_065949.yaml", (2026, 10, 6, 14, 30)),
    ("formats/short-motivation/configs/waiting_upload/short_20260923_070011.yaml", (2026, 10, 7, 8, 30)),
    ("formats/short-motivation/configs/waiting_upload/short_20260923_070035.yaml", (2026, 10, 7, 14, 30)),
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

    append_schedule(new_path, video_id, publish_at, title, is_short=True)

    dt_et = datetime(yr, mo, dy, hr, mn, 0, tzinfo=ET)
    print(f"  ✅ https://youtube.com/shorts/{video_id}  [{dt_et.strftime('%b %d %H:%M ET')}]")

print("\n=== Done ===")
