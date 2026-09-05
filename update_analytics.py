#!/usr/bin/env python3
"""Refresh analytics.html: merge archived-yaml video IDs with existing dataset,
pull fresh stats from YouTube Data API, rewrite the VIDEOS array in place."""
import glob
import json
import re
from datetime import datetime, timezone
from pathlib import Path

import yaml
from googleapiclient.discovery import build

from src.pipeline.youtube_uploader import authenticate

HTML_PATH = Path("analytics.html")

# 1. Load existing dataset from analytics.html
html = HTML_PATH.read_text()
m = re.search(r"const VIDEOS = (\[.*?\]);", html, re.S)
existing = {v["id"]: v for v in json.loads(m.group(1))}
print(f"Existing dataset: {len(existing)} videos")

# 2. Collect all video_ids from archived yamls (format + publish_date fallback)
archived = {}
for fmt_dir in sorted(glob.glob("formats/*/configs/archive")):
    fmt = fmt_dir.split("/")[1]
    for f in sorted(glob.glob(fmt_dir + "/*.yaml")):
        try:
            d = yaml.safe_load(open(f))
        except Exception as e:
            print("ERR", f, e)
            continue
        yt = d.get("youtube", {})
        vid = yt.get("video_id")
        if not vid:
            continue
        publish_at = yt.get("publish_at", "")
        publish_date = publish_at[:10] if publish_at else None
        archived[vid] = {
            "id": vid,
            "title": yt.get("title", ""),
            "format": fmt,
            "publish_date": publish_date,
        }

new_ids = [vid for vid in archived if vid not in existing]
print(f"New videos found in archives: {len(new_ids)}")

all_ids = list(existing.keys()) + new_ids
print(f"Total to refresh: {len(all_ids)}")

# 3. Fetch stats from YouTube Data API in batches of 50
creds = authenticate()
yt = build("youtube", "v3", credentials=creds)

stats_by_id = {}
for i in range(0, len(all_ids), 50):
    batch = all_ids[i:i + 50]
    resp = yt.videos().list(part="statistics,status,snippet", id=",".join(batch)).execute()
    for item in resp.get("items", []):
        stats_by_id[item["id"]] = item

print(f"Fetched stats for {len(stats_by_id)} / {len(all_ids)} ids")
missing = [vid for vid in all_ids if vid not in stats_by_id]
if missing:
    print(f"Missing (deleted/private-inaccessible?): {missing}")

# 4. Rebuild VIDEOS array
today = datetime.now(timezone.utc).date()
videos = []
for vid in all_ids:
    base = existing.get(vid) or archived.get(vid) or {}
    item = stats_by_id.get(vid)

    title = base.get("title", "")
    fmt = base.get("format", "")
    publish_date = base.get("publish_date")

    if item:
        snippet = item.get("snippet", {})
        status = item.get("status", {})
        statistics = item.get("statistics", {})
        title = snippet.get("title", title)
        privacy = status.get("privacyStatus", base.get("privacy", "public"))
        views = int(statistics.get("viewCount", 0))
        likes = int(statistics.get("likeCount", 0))
        comments = int(statistics.get("commentCount", 0))
        if not publish_date:
            published_at = snippet.get("publishedAt", "")
            publish_date = published_at[:10] if published_at else base.get("publish_date")
    else:
        # video not returned by API (deleted, or scheduled-private not yet public) — keep prior known stats
        privacy = base.get("privacy", "unknown")
        views = base.get("views", 0)
        likes = base.get("likes", 0)
        comments = base.get("comments", 0)

    if not publish_date:
        publish_date = str(today)

    days_live = max((today - datetime.strptime(publish_date, "%Y-%m-%d").date()).days, 0) + 1
    vpd = round(views / days_live, 1) if days_live else views

    videos.append({
        "id": vid,
        "title": title,
        "format": fmt,
        "publish_date": publish_date,
        "days_live": days_live,
        "views": views,
        "likes": likes,
        "comments": comments,
        "privacy": privacy,
        "vpd": vpd,
    })

videos.sort(key=lambda v: v["publish_date"], reverse=True)

# 5. Write back into analytics.html
new_array = json.dumps(videos, separators=(",", ":"))
new_html = html[:m.start(1)] + new_array + html[m.end(1):]

# update the date range text in header (May–Jul 2026 -> actual span)
dates = sorted(v["publish_date"] for v in videos if v["publish_date"])
if dates:
    start = datetime.strptime(dates[0], "%Y-%m-%d")
    end = datetime.strptime(dates[-1], "%Y-%m-%d")
    span = f"{start.strftime('%b')}–{end.strftime('%b %Y')}" if start.month != end.month else start.strftime("%b %Y")
    new_html = new_html.replace(
        '`${VIDEOS.length} videos · May–Jul 2026 · updated ${new Date().toLocaleDateString("en-US",{month:"short",day:"numeric"})}`',
        f'`${{VIDEOS.length}} videos · {span} · updated ${{new Date().toLocaleDateString("en-US",{{month:"short",day:"numeric"}})}}`'
    )

HTML_PATH.write_text(new_html)
print(f"\nWrote {len(videos)} videos to {HTML_PATH}")
print(f"Date span: {dates[0]} .. {dates[-1]}")
total_views = sum(v["views"] for v in videos if v["privacy"] == "public")
print(f"Total views (public): {total_views:,}")
