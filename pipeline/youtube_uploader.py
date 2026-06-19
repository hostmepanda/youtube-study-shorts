#!/usr/bin/env python3
"""Upload approved shorts to YouTube with scheduled publish times."""

import argparse
import json
import os
import shutil
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

from dotenv import load_dotenv
from google.auth.exceptions import RefreshError
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

load_dotenv()

ROOT = Path(__file__).parent.parent
APPROVED_DIR = ROOT / "output" / "approved"
UPLOADED_DIR = ROOT / "output" / "uploaded"
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


def load_metadata(video_path: Path) -> dict:
    # Check approved/ first (may have updated meta), then configs/
    meta_path = APPROVED_DIR / (video_path.stem + "_meta.json")
    if not meta_path.exists():
        meta_path = ROOT / "output" / "configs" / (video_path.stem + "_meta.json")
    if meta_path.exists():
        return json.loads(meta_path.read_text())

    # Try to extract title from the YAML config
    yaml_path = ROOT / "output" / "configs" / (video_path.stem + ".yaml")
    first_line = None
    if yaml_path.exists():
        try:
            import yaml
            config = yaml.safe_load(yaml_path.read_text())
            for step in config.get("steps", []):
                if step.get("type") == "audio" and step.get("text"):
                    lines = [l.strip() for l in step["text"].splitlines() if l.strip()]
                    if lines:
                        first_line = lines[0]
                        break
        except Exception:
            pass

    is_parable = video_path.stem.startswith("parable_")
    tag = "parable" if is_parable else "motivation"
    title = f"{first_line} #{tag}" if first_line else f"{video_path.stem} #languagelearning #{tag}"
    return {
        "title": f"{title} #languagelearning",
        "description": first_line or "Start speaking. Stop waiting.",
        "tags": ["languagelearning", tag, "motivation", "shorts"],
        "category_id": "27",
    }


def upload_video(youtube, video_path: Path, publish_at: str) -> str:
    meta = load_metadata(video_path)
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

    UPLOADED_DIR.mkdir(parents=True, exist_ok=True)

    videos = sorted(APPROVED_DIR.glob("*.mp4"))
    if not videos:
        print("No videos in output/approved/ — nothing to upload.")
        return

    shorts = [v for v in videos if v.name.startswith("short_")]
    parables = [v for v in videos if v.name.startswith("parable_")]
    other = [v for v in videos if not v.name.startswith("short_") and not v.name.startswith("parable_")]

    youtube = build("youtube", "v3", credentials=creds)
    print(f"Found {len(videos)} video(s) to upload ({len(shorts)} shorts, {len(parables)} parables).\n")

    start_date = datetime.now(PUBLISH_TZ)

    queue = (
        [(v, publish_time(start_date, i, SHORTS_HOUR, SHORTS_MINUTE)) for i, v in enumerate(shorts)] +
        [(v, publish_time(start_date, i, PARABLES_HOUR, PARABLES_MINUTE)) for i, v in enumerate(parables)] +
        [(v, publish_time(datetime.now(PUBLISH_TZ), i, SHORTS_HOUR, SHORTS_MINUTE)) for i, v in enumerate(other)]
    )

    for video_path, publish_at in queue:
        print(f"▶ Uploading {video_path.name}")
        try:
            video_id = upload_video(youtube, video_path, publish_at)
            print(f"  ✓ Uploaded: https://youtube.com/shorts/{video_id}\n")
            dest = UPLOADED_DIR / video_path.name
            shutil.move(str(video_path), str(dest))
        except Exception as e:
            print(f"  ✗ Failed: {e}\n")

    print("Done.")


if __name__ == "__main__":
    main()
