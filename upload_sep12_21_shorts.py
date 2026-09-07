#!/usr/bin/env python3
"""Upload 10 motivational shorts: Sep 12–21, 09:00 ET."""
from src.pipeline.youtube_uploader import authenticate, upload_video, append_schedule
from googleapiclient.discovery import build
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from pathlib import Path
import yaml

ET = ZoneInfo("America/New_York")

SCHEDULE = [
    ("formats/short-motivation/configs/waiting_upload/short_20260907_072441.yaml", (2026, 9, 12, 9, 0)),
    ("formats/short-motivation/configs/waiting_upload/short_20260907_072506.yaml", (2026, 9, 13, 9, 0)),
    ("formats/short-motivation/configs/waiting_upload/short_20260907_072528.yaml", (2026, 9, 14, 9, 0)),
    ("formats/short-motivation/configs/waiting_upload/short_20260907_072548.yaml", (2026, 9, 15, 9, 0)),
    ("formats/short-motivation/configs/waiting_upload/short_20260907_072609.yaml", (2026, 9, 16, 9, 0)),
    ("formats/short-motivation/configs/waiting_upload/short_20260907_072632.yaml", (2026, 9, 17, 9, 0)),
    ("formats/short-motivation/configs/waiting_upload/short_20260907_072653.yaml", (2026, 9, 18, 9, 0)),
    ("formats/short-motivation/configs/waiting_upload/short_20260907_072711.yaml", (2026, 9, 19, 9, 0)),
    ("formats/short-motivation/configs/waiting_upload/short_20260907_072732.yaml", (2026, 9, 20, 9, 0)),
    ("formats/short-motivation/configs/waiting_upload/short_20260907_072852.yaml", (2026, 9, 21, 9, 0)),
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
