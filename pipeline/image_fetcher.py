#!/usr/bin/env python3
"""Fetch a portrait photo from Pexels, avoiding duplicates."""

import argparse
import json
import os
import sys
from pathlib import Path
import requests
from dotenv import load_dotenv

load_dotenv()

PEXELS_API = "https://api.pexels.com/v1/search"
USED_PHOTOS = Path(__file__).parent.parent / "data" / "used_photos.json"
IMAGES_DIR = Path(__file__).parent.parent / "output" / "images"

KEYWORD_POOLS = {
    "mistakes": ["learning", "growth", "challenge"],
    "speaking": ["conversation", "communication", "people talking"],
    "progress": ["path", "journey", "sunrise"],
    "language": ["books", "travel", "world map"],
    "study": ["studying", "focus", "desk"],
    "success": ["achievement", "celebration", "winner"],
}


def load_used() -> set:
    if USED_PHOTOS.exists():
        return set(json.loads(USED_PHOTOS.read_text()))
    return set()


def save_used(used: set) -> None:
    USED_PHOTOS.write_text(json.dumps(sorted(used), indent=2))


def expand_keywords(keywords: list[str]) -> list[str]:
    expanded = []
    for kw in keywords:
        expanded.append(kw)
        expanded.extend(KEYWORD_POOLS.get(kw.lower(), []))
    return expanded


def search_pexels(query: str, api_key: str) -> list[dict]:
    resp = requests.get(
        PEXELS_API,
        headers={"Authorization": api_key},
        params={"query": query, "per_page": 15, "orientation": "portrait"},
        timeout=10,
    )
    resp.raise_for_status()
    return resp.json().get("photos", [])


def fetch_image(keywords: list[str]) -> str:
    api_key = os.environ["PEXELS_API_KEY"]
    used = load_used()
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)

    for kw in expand_keywords(keywords):
        photos = search_pexels(kw, api_key)
        for photo in photos:
            photo_id = str(photo["id"])
            if photo_id in used:
                continue

            url = photo["src"].get("portrait") or photo["src"]["large2x"]
            ext = url.split("?")[0].rsplit(".", 1)[-1] or "jpg"
            dest = IMAGES_DIR / f"photo_{photo_id}.{ext}"

            headers = {"User-Agent": "Mozilla/5.0"}
            r = requests.get(url, headers=headers, timeout=30)
            r.raise_for_status()
            dest.write_bytes(r.content)
            used.add(photo_id)
            save_used(used)
            return str(dest)

    sys.exit("No unused photos found for keywords: " + ", ".join(keywords))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--keywords", required=True, help="Comma-separated keywords")
    args = parser.parse_args()

    keywords = [k.strip() for k in args.keywords.split(",")]
    path = fetch_image(keywords)
    print(path)


if __name__ == "__main__":
    main()
