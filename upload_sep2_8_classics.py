#!/usr/bin/env python3
"""Upload 7 classic parables: Sep 2–8, 16:30 ET. Run after 10:00 FI / 03:00 ET."""
from src.pipeline.youtube_uploader import authenticate, upload_video, append_schedule
from googleapiclient.discovery import build
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from pathlib import Path
import yaml

ET = ZoneInfo("America/New_York")

SCHEDULE = [
    ("formats/parable-classic/configs/waiting_upload/classic_20260901_105246.yaml", (2026, 9, 2,  16, 30)),
    ("formats/parable-classic/configs/waiting_upload/classic_20260901_105323.yaml", (2026, 9, 3,  16, 30)),
    ("formats/parable-classic/configs/waiting_upload/classic_20260901_105357.yaml", (2026, 9, 4,  16, 30)),
    ("formats/parable-classic/configs/waiting_upload/classic_20260901_105428.yaml", (2026, 9, 5,  16, 30)),
    ("formats/parable-classic/configs/waiting_upload/classic_20260901_105500.yaml", (2026, 9, 6,  16, 30)),
    ("formats/parable-classic/configs/waiting_upload/classic_20260901_105534.yaml", (2026, 9, 7,  16, 30)),
    ("formats/parable-classic/configs/waiting_upload/classic_20260901_105606.yaml", (2026, 9, 8,  16, 30)),
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
