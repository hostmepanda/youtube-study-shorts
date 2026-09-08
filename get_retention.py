#!/usr/bin/env python3
"""List videos with audience retention (averageViewPercentage) above a threshold,
using the YouTube Analytics API."""
import re
import json
import sys
from pathlib import Path

from googleapiclient.discovery import build

from src.pipeline.youtube_uploader import authenticate

THRESHOLD = float(sys.argv[1]) if len(sys.argv) > 1 else 50.0

creds = authenticate()
yt = build("youtube", "v3", credentials=creds)
yta = build("youtubeAnalytics", "v2", credentials=creds)

channel_resp = yt.channels().list(part="id", mine=True).execute()
channel_id = channel_resp["items"][0]["id"]
print(f"Channel: {channel_id}")

# Load video metadata (titles/format) from analytics.html's dataset
html = Path("analytics.html").read_text()
m = re.search(r"const VIDEOS = (\[.*?\]);", html, re.S)
videos = {v["id"]: v for v in json.loads(m.group(1))}
public_ids = [vid for vid, v in videos.items() if v["privacy"] == "public"]
print(f"Public videos to check: {len(public_ids)}")

results = []
for i in range(0, len(public_ids), 200):
    batch_ids = public_ids[i:i + 200]
    resp = yta.reports().query(
        ids=f"channel=={channel_id}",
        startDate="2020-01-01",
        endDate="2030-01-01",
        metrics="averageViewPercentage,views",
        dimensions="video",
        filters="video==" + ",".join(batch_ids),
        maxResults=200,
    ).execute()
    for row in resp.get("rows", []):
        vid, avg_pct, views = row
        results.append((vid, avg_pct, views))

print(f"Retention data returned for {len(results)} videos")

results.sort(key=lambda r: r[1], reverse=True)
top = [r for r in results if r[1] >= THRESHOLD]

print(f"\n=== Videos with retention >= {THRESHOLD}% ===")
for vid, pct, views in top:
    v = videos.get(vid, {})
    title = v.get("title", "?")
    fmt = v.get("format", "?")
    print(f"{pct:5.1f}%  {int(views):>5} views  [{fmt}]  {title}  https://youtube.com/watch?v={vid}")

if not top:
    print("(none)")
