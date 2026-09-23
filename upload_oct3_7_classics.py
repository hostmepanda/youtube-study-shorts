#!/usr/bin/env python3
"""Upload 5 classic parables: Oct 3-7, 12:00 ET."""
from src.pipeline.youtube_uploader import authenticate, upload_video, append_schedule
from googleapiclient.discovery import build
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from pathlib import Path
import yaml

ET = ZoneInfo("America/New_York")

SCHEDULE = [
    ("formats/parable-classic/configs/waiting_upload/classic_20260923_070106.yaml", (2026, 10, 3, 12, 0)),  # classic_057
    ("formats/parable-classic/configs/waiting_upload/classic_20260923_070206.yaml", (2026, 10, 4, 12, 0)),  # classic_058
    ("formats/parable-classic/configs/waiting_upload/classic_20260923_070317.yaml", (2026, 10, 5, 12, 0)),  # classic_059
    ("formats/parable-classic/configs/waiting_upload/classic_20260923_070453.yaml", (2026, 10, 6, 12, 0)),  # classic_060
    ("formats/parable-classic/configs/waiting_upload/classic_20260923_070552.yaml", (2026, 10, 7, 12, 0)),  # classic_061
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
