#!/usr/bin/env python3
"""Upload videos queued in formats/*/configs/waiting_upload/ to YouTube with scheduled publish times.

Each yaml lifecycle file carries its own YouTube metadata under a `youtube:` key
(title/description/tags/category_id/video_path) — no separate meta.json sidecar.
The rendered .mp4 itself lives permanently in output/videos/ and is never moved;
only the yaml travels between configs/{new,waiting_upload,archive}/.
"""

import argparse
import sys
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

ROOT = Path(__file__).parent.parent
FORMATS_DIR = ROOT / "formats"
CREDENTIALS_FILE = ROOT / "credentials.json"
TOKEN_FILE = ROOT / "token.json"

SCOPES = ["https://www.googleapis.com/auth/youtube"]

# All publish times are scheduled relative to US Eastern Time (audience timezone),
# not UTC. ZoneInfo handles EST/EDT (daylight saving) transitions automatically.
PUBLISH_TZ = ZoneInfo("America/New_York")

SHORTS_HOUR = 9       # 09:00 America/New_York
SHORTS_MINUTE = 0
PARABLES_HOUR = 16    # 16:30 America/New_York
PARABLES_MINUTE = 30


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


def upload_video(youtube, config_path: Path, publish_at: str) -> str:
    meta = load_meta(config_path)
    video_path = Path(meta["video_path"])
    if not video_path.exists():
        sys.exit(f"Video not found at {video_path} (referenced by {config_path})")

    print(f"  Title:      {meta['title']}")
    print(f"  Publish at: {publish_at}")

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

    return response["id"]


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

    # short-motivation format gets the shorts schedule; every parable format gets the parables schedule
    shorts = [p for p in queued if p.parent.parent.parent.name == "short-motivation"]
    parables = [p for p in queued if p.parent.parent.parent.name != "short-motivation"]

    youtube = build("youtube", "v3", credentials=creds)
    print(f"Found {len(queued)} video(s) queued ({len(shorts)} shorts, {len(parables)} parables).\n")

    start_date = datetime.now(PUBLISH_TZ)

    schedule = (
        [(p, publish_time(start_date, i, SHORTS_HOUR, SHORTS_MINUTE)) for i, p in enumerate(shorts)] +
        [(p, publish_time(start_date, i, PARABLES_HOUR, PARABLES_MINUTE)) for i, p in enumerate(parables)]
    )

    for config_path, publish_at in schedule:
        print(f"▶ Uploading {config_path.name} ({config_path.parent.parent.parent.name})")
        try:
            video_id = upload_video(youtube, config_path, publish_at)
            print(f"  ✓ Uploaded: https://youtube.com/shorts/{video_id}\n")
            archive_dir = config_path.parent.parent / "archive"
            archive_dir.mkdir(parents=True, exist_ok=True)
            config_path.rename(archive_dir / config_path.name)
        except Exception as e:
            print(f"  ✗ Failed: {e}\n")

    print("Done.")


if __name__ == "__main__":
    main()
