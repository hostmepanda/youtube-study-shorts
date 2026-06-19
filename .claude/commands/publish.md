# Publish

Upload a rendered video (short or parable) to YouTube as a scheduled, private-until-publish upload.

## Timezone rule — IMPORTANT

**All publish times are scheduled relative to US Eastern Time (America/New_York)**, the audience's timezone — never raw UTC, never the local machine's timezone. `pipeline/youtube_uploader.py` handles this automatically via `ZoneInfo("America/New_York")`, which accounts for EST/EDT daylight-saving transitions.

If the user gives a custom time (e.g. "publish at 7pm today" or "today and tomorrow at 12/15/18"), treat it as Eastern Time unless they explicitly say otherwise, and convert to UTC before calling the YouTube API.

## Steps

1. **Stage the video** — copy the rendered `.mp4` and its `_meta.json` sidecar into `output/approved/`:
   ```bash
   cp output/videos/<name>.mp4 output/approved/
   cp output/configs/<name>_meta.json output/approved/
   ```
   If the parable/text was edited after the meta.json was first written (e.g. rewritten text, new title), make sure the copy in `output/approved/` reflects the latest version — `load_metadata()` in `youtube_uploader.py` prefers `output/approved/` over `output/configs/`.

2. **Default schedule (no custom time requested)** — just run:
   ```bash
   python3 pipeline/youtube_uploader.py
   ```
   This uploads everything in `output/approved/`, scheduling shorts at 09:00 ET and parables at 16:30 ET, one per day in filename order, starting today. Uploaded files are moved to `output/uploaded/`.

3. **Custom schedule requested** — when the user specifies particular times/dates (e.g. "2 today 3 hours apart, 3 tomorrow at 12/15/18"), write a one-off script that:
   - Authenticates via `from pipeline.youtube_uploader import authenticate, load_metadata`
   - Builds each `publishAt` by interpreting the requested times as **US Eastern**, converting to UTC (e.g. via `datetime(..., tzinfo=ZoneInfo("America/New_York")).astimezone(timezone.utc)`)
   - Uploads with `privacyStatus: "private"` + `publishAt` set (same body shape as `upload_video()` in `youtube_uploader.py`)
   - Moves each uploaded file from `output/approved/` to `output/uploaded/`

4. **Report** — for each upload, print the title, the publish time (state it in ET so the user can sanity-check, e.g. "today 19:00 ET"), and the `https://youtube.com/shorts/<id>` link.

## Notes

- Uploads always go in as `privacyStatus: private` with `publishAt` set — YouTube auto-publishes at that time. If `publishAt` is in the past, YouTube publishes immediately.
- To replace a wrong/outdated upload: delete the old video via `youtube.videos().delete(id=...)`, then upload the corrected version with the same publish time.
- To update only title/description/tags on a live or scheduled video without re-uploading: `youtube.videos().update(part="snippet", body={...})` — requires the `youtube` (not `youtube.upload`) OAuth scope, already set in `SCOPES`.
