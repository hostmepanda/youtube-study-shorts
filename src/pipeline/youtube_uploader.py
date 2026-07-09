#!/usr/bin/env python3
"""Upload videos queued in formats/*/configs/waiting_upload/ to YouTube with scheduled publish times.

Each yaml lifecycle file carries its own YouTube metadata under a `youtube:` key
(title/description/tags/category_id/video_path) — no separate meta.json sidecar.
The rendered .mp4 itself lives permanently in output/videos/ and is never moved;
only the yaml travels between configs/{new,waiting_upload,archive}/.
"""

import argparse
import re
import sys
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

import yaml as yaml_lib
from dotenv import load_dotenv
from google.auth.exceptions import RefreshError
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

load_dotenv()

ROOT = Path(__file__).parent.parent.parent
FORMATS_DIR = ROOT / "formats"
CREDENTIALS_FILE = ROOT / "credentials.json"
TOKEN_FILE = ROOT / "token.json"

SCOPES = ["https://www.googleapis.com/auth/youtube"]

# All publish times are scheduled relative to US Eastern Time (audience timezone),
# not UTC. ZoneInfo handles EST/EDT (daylight saving) transitions automatically.
PUBLISH_TZ = ZoneInfo("America/New_York")

SHORTS_HOUR = 9       # 09:00 America/New_York — slot 1
SHORTS_MINUTE = 0
SHORTS_HOUR2 = 19     # 19:00 America/New_York — slot 2 (when queue has >1/day)
PARABLES_HOUR = 16    # 16:30 America/New_York
PARABLES_MINUTE = 30
LONG_HOUR = 12        # 12:00 America/New_York
LONG_MINUTE = 0


def authenticate() -> Credentials:
    creds = None
    if TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except RefreshError:
                creds = None
        if not creds or not creds.valid:
            if not CREDENTIALS_FILE.exists():
                sys.exit("credentials.json not found. See README for setup instructions.")
            flow = InstalledAppFlow.from_client_secrets_file(str(CREDENTIALS_FILE), SCOPES)
            creds = flow.run_local_server(port=0)
        TOKEN_FILE.write_text(creds.to_json())

    return creds


def publish_time(start_date: datetime, offset_days: int, hour: int, minute: int) -> str:
    """Return RFC 3339 UTC datetime for given hour/minute US Eastern Time, offset_days from start_date."""
    target = start_date.replace(hour=hour, minute=minute, second=0, microsecond=0)
    target += timedelta(days=offset_days)
    return target.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")


def find_queued() -> list[Path]:
    """All yaml lifecycle files sitting in formats/*/configs/waiting_upload/, oldest first."""
    if not FORMATS_DIR.exists():
        return []
    queued = []
    for fmt_dir in sorted(FORMATS_DIR.iterdir()):
        waiting_dir = fmt_dir / "configs" / "waiting_upload"
        if waiting_dir.exists():
            queued += sorted(waiting_dir.glob("*.yaml"))
    return queued


def load_meta(config_path: Path) -> dict:
    config = yaml_lib.safe_load(config_path.read_text())
    meta = config.get("youtube")
    if not meta:
        sys.exit(f"{config_path} has no youtube: metadata — was it built before the meta-merge restructure?")
    return meta


def resolve_thumbnail(meta: dict, config_path: Path) -> Path | None:
    """Return thumbnail path: explicit in meta > auto-generated from hook > format-level default."""
    if meta.get("thumbnail"):
        p = Path(meta["thumbnail"])
        return p if p.exists() else None

    # Auto-generate from hook lines if present
    hook_lines = meta.get("hook")
    if hook_lines:
        try:
            from src.pipeline.thumbnail_generator import generate
        except ImportError:
            from thumbnail_generator import generate
        lines = hook_lines if isinstance(hook_lines, list) else [hook_lines]
        stem  = config_path.stem
        out   = config_path.parent / f"{stem}_thumbnail.jpg"
        if not out.exists():
            print(f"  Generating thumbnail from hook…")
            generate(lines, out)
        return out

    # Format-level static fallback: formats/<format>/thumbnail.jpg
    fmt_dir = config_path.parent.parent.parent
    for name in ("thumbnail.jpg", "thumbnail.png"):
        p = fmt_dir / name
        if p.exists():
            return p

    return None


FORMAT_TYPE = {
    "short-motivation": "motivational short",
    "long-monologue":   "long monologue",
    "parable-classic":  "classic parable",
    "parable-animal":   "animal parable",
    "legacy":           "classic parable",
}

HEL_TZ = ZoneInfo("Europe/Helsinki")


def append_schedule(config_path: Path, video_id: str, publish_at: str, title: str, is_short: bool) -> None:
    """Append one row to schedule.md in the project root."""
    schedule_file = ROOT / "schedule.md"
    if not schedule_file.exists():
        return

    fmt_name  = config_path.parent.parent.parent.name
    video_type = FORMAT_TYPE.get(fmt_name, fmt_name)
    yaml_rel  = config_path.relative_to(ROOT)

    dt_utc = datetime.strptime(publish_at, "%Y-%m-%dT%H:%M:%S.000Z").replace(tzinfo=timezone.utc)
    dt_et  = dt_utc.astimezone(ZoneInfo("America/New_York"))
    dt_hel = dt_utc.astimezone(HEL_TZ)

    date_str = dt_et.strftime("%Y-%m-%d")
    et_str   = dt_et.strftime("%H:%M")
    hel_str  = dt_hel.strftime("%H:%M")

    url = f"https://youtube.com/shorts/{video_id}" if is_short else f"https://youtube.com/watch?v={video_id}"
    short_title = title[:55] + ("…" if len(title) > 55 else "")
    row = f"| {date_str} | {et_str} | {hel_str} | {video_type} | {short_title} | [link]({url}) | [{yaml_rel.name}]({yaml_rel}) |"

    text  = schedule_file.read_text()
    # Insert before the Notes section or at end of table
    if "## Notes" in text:
        text = text.replace("## Notes", row + "\n## Notes")
    else:
        text = text.rstrip() + "\n" + row + "\n"
    schedule_file.write_text(text)


def upload_video(youtube, config_path: Path, publish_at: str) -> str:
    meta = load_meta(config_path)
    video_path = Path(meta["video_path"])
    if not video_path.exists():
        sys.exit(f"Video not found at {video_path} (referenced by {config_path})")

    thumbnail_path = resolve_thumbnail(meta, config_path)

    print(f"  Title:      {meta['title']}")
    print(f"  Publish at: {publish_at}")
    print(f"  Thumbnail:  {thumbnail_path or '(auto)'}")

    body = {
        "snippet": {
            "title": meta["title"],
            "description": meta.get("description", ""),
            "tags": meta.get("tags", []),
            "categoryId": meta.get("category_id", "27"),
        },
        "status": {
            "privacyStatus": "private",
            "publishAt": publish_at,
            "selfDeclaredMadeForKids": False,
        },
    }

    media = MediaFileUpload(str(video_path), mimetype="video/mp4", resumable=True)
    request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)

    response = None
    while response is None:
        _, response = request.next_chunk()

    video_id = response["id"]

    # Thumbnail upload disabled — requires verified YouTube account (youtube.com/verify)
    # if thumbnail_path:
    #     mimetype = "image/png" if thumbnail_path.suffix.lower() == ".png" else "image/jpeg"
    #     youtube.thumbnails().set(
    #         videoId=video_id,
    #         media_body=MediaFileUpload(str(thumbnail_path), mimetype=mimetype),
    #     ).execute()
    #     print(f"  ✓ Thumbnail uploaded")

    return video_id


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--auth", action="store_true", help="Run OAuth flow and exit")
    args = parser.parse_args()

    creds = authenticate()
    if args.auth:
        print("✓ Authentication successful. token.json saved.")
        return

    queued = find_queued()
    if not queued:
        print("Nothing in formats/*/configs/waiting_upload/ — nothing to upload.")
        return

    # Route by format name to the correct publish slot
    shorts   = [p for p in queued if p.parent.parent.parent.name == "short-motivation"]
    longs    = [p for p in queued if p.parent.parent.parent.name == "long-monologue"]
    parables = [p for p in queued if p.parent.parent.parent.name not in ("short-motivation", "long-monologue")]

    youtube = build("youtube", "v3", credentials=creds)
    print(f"Found {len(queued)} video(s) queued ({len(shorts)} shorts, {len(parables)} parables, {len(longs)} long).\n")

    start_date = datetime.now(PUBLISH_TZ)

    # Shorts: 2 per day — slot 1 = 09:00 ET, slot 2 = 19:00 ET
    shorts_schedule = [
        (p, publish_time(start_date, i // 2, SHORTS_HOUR if i % 2 == 0 else SHORTS_HOUR2, SHORTS_MINUTE))
        for i, p in enumerate(shorts)
    ]

    schedule = (
        shorts_schedule +
        [(p, publish_time(start_date, i, PARABLES_HOUR, PARABLES_MINUTE)) for i, p in enumerate(parables)] +
        [(p, publish_time(start_date, i, LONG_HOUR,     LONG_MINUTE))     for i, p in enumerate(longs)]
    )

    for config_path, publish_at in schedule:
        fmt_name = config_path.parent.parent.parent.name
        print(f"▶ Uploading {config_path.name} ({fmt_name})")
        try:
            video_id = upload_video(youtube, config_path, publish_at)
            is_short = fmt_name in ("short-motivation", "parable-classic", "parable-animal", "legacy")
            url = f"https://youtube.com/shorts/{video_id}" if is_short else f"https://youtube.com/watch?v={video_id}"
            print(f"  ✓ Uploaded: {url}\n")

            # Write video_id and publish_at back into the yaml before archiving
            config = yaml_lib.safe_load(config_path.read_text())
            config["youtube"]["video_id"] = video_id
            config["youtube"]["publish_at"] = publish_at
            config_path.write_text(yaml_lib.dump(config, allow_unicode=True, sort_keys=False))

            # Append row to schedule.md
            meta = config.get("youtube", {})
            append_schedule(config_path, video_id, publish_at, meta.get("title", ""), fmt_name != "long-monologue")

            archive_dir = config_path.parent.parent / "archive"
            archive_dir.mkdir(parents=True, exist_ok=True)
            config_path.rename(archive_dir / config_path.name)
        except Exception as e:
            print(f"  ✗ Failed: {e}\n")

    print("Done.")


if __name__ == "__main__":
    main()
