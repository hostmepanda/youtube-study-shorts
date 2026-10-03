#!/usr/bin/env python3
"""Upload 10 motivational shorts: Oct 8-12, 08:30/14:30 ET."""
from src.pipeline.youtube_uploader import authenticate, upload_video, append_schedule
from googleapiclient.discovery import build
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from pathlib import Path
import yaml

ET = ZoneInfo("America/New_York")

SCHEDULE = [
    ("formats/short-motivation/configs/waiting_upload/short_20260930_073753.yaml", (2026, 10, 8, 8, 30)),
    ("formats/short-motivation/configs/waiting_upload/short_20260930_073815.yaml", (2026, 10, 8, 14, 30)),
    ("formats/short-motivation/configs/waiting_upload/short_20260930_073837.yaml", (2026, 10, 9, 8, 30)),
    ("formats/short-motivation/configs/waiting_upload/short_20260930_073858.yaml", (2026, 10, 9, 14, 30)),
    ("formats/short-motivation/configs/waiting_upload/short_20260930_073919.yaml", (2026, 10, 10, 8, 30)),
    ("formats/short-motivation/configs/waiting_upload/short_20260930_073940.yaml", (2026, 10, 10, 14, 30)),
    ("formats/short-motivation/configs/waiting_upload/short_20260930_074011.yaml", (2026, 10, 11, 8, 30)),
    ("formats/short-motivation/configs/waiting_upload/short_20260930_074044.yaml", (2026, 10, 11, 14, 30)),
    ("formats/short-motivation/configs/waiting_upload/short_20260930_074105.yaml", (2026, 10, 12, 8, 30)),
    ("formats/short-motivation/configs/waiting_upload/short_20260930_074159.yaml", (2026, 10, 12, 14, 30)),
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
