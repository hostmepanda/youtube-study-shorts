# CLAUDE.md

## Publishing schedule — always US Eastern Time

All YouTube uploads (shorts and parables) must be scheduled relative to **US Eastern Time (America/New_York)**, not UTC and not the local machine timezone. This is the audience's timezone.

- `pipeline/youtube_uploader.py` already implements this: `PUBLISH_TZ = ZoneInfo("America/New_York")`, which automatically handles EST/EDT (daylight saving) transitions.
- If scheduling manually (ad-hoc `publishAt` for a custom time request), always convert the requested wall-clock time from US Eastern to UTC before sending it to the YouTube API — do not pass Eastern-time numbers directly as if they were UTC.
- Default schedule: shorts at 09:00 ET, parables at 16:30 ET, one per day starting today, queued in upload order.
