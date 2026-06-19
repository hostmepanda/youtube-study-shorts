# Publish

Upload a rendered video (short or parable) to YouTube as a scheduled, private-until-publish upload.

## How the lifecycle works

Every render produces one yaml file under `formats/<format>/configs/new/<short_id>.yaml`. That file carries its own `youtube:` block (title, description, tags, category_id, video_path) — there is no separate meta.json sidecar.

The yaml travels through three folders inside its format's `configs/` dir:
```
new/  →  waiting_upload/  →  archive/
```
**The rendered `.mp4` itself never moves** — it lives permanently in `output/videos/<short_id>.mp4`. Only the yaml (a few KB of text) travels between lifecycle folders, so "what's been published" is always answered by "which folder is the yaml sitting in," not by hunting for files across `approved/`/`uploaded/`.

## Timezone rule — IMPORTANT

**All publish times are scheduled relative to US Eastern Time (America/New_York)**, the audience's timezone — never raw UTC, never the local machine's timezone. `pipeline/youtube_uploader.py` handles this automatically via `ZoneInfo("America/New_York")`, which accounts for EST/EDT daylight-saving transitions.

If the user gives a custom time (e.g. "publish at 7pm today" or "today and tomorrow at 12/15/18"), treat it as Eastern Time unless they explicitly say otherwise, and convert to UTC before calling the YouTube API.

## Steps

1. **Review what's in `new/`** across all formats:
   ```bash
   find formats/*/configs/new -name "*.yaml"
   ```
   For each candidate, you can check its embedded metadata without uploading:
   ```bash
   python3 -c "from pipeline.youtube_uploader import load_meta; from pathlib import Path; print(load_meta(Path('formats/<format>/configs/new/<id>.yaml')))"
   ```

2. **Queue for upload** — move the chosen yaml(s) from `new/` to `waiting_upload/` within the same format dir:
   ```bash
   mv formats/<format>/configs/new/<id>.yaml formats/<format>/configs/waiting_upload/
   ```
   If the underlying text/parable was edited after rendering (e.g. rewritten ending, new title), re-render first so the yaml's embedded `youtube:` block reflects the latest version — don't hand-edit metadata in a stale yaml.

3. **Default schedule (no custom time requested)** — just run:
   ```bash
   python3 pipeline/youtube_uploader.py
   ```
   This uploads everything sitting in any `formats/*/configs/waiting_upload/`, scheduling `short-motivation` items at 09:00 ET and everything else (parable-classic, parable-animal, legacy) at 16:30 ET, one per day in queue order, starting today. On success, each yaml is moved from `waiting_upload/` to `archive/` — the mp4 is untouched.

4. **Custom schedule requested** — when the user specifies particular times/dates (e.g. "2 today 3 hours apart, 3 tomorrow at 12/15/18"), write a one-off script that:
   - Authenticates via `from pipeline.youtube_uploader import authenticate, load_meta`
   - For each queued yaml, builds `publishAt` by interpreting the requested times as **US Eastern**, converting to UTC (e.g. via `datetime(..., tzinfo=ZoneInfo("America/New_York")).astimezone(timezone.utc)`)
   - Uploads with `privacyStatus: "private"` + `publishAt` set (same body shape as `upload_video()` in `youtube_uploader.py`)
   - On success, moves the yaml from `waiting_upload/` to `archive/` (`config_path.rename(archive_dir / config_path.name)`) — never touches the mp4

5. **Report** — for each upload, print the title, the publish time (state it in ET so the user can sanity-check, e.g. "today 19:00 ET"), and the `https://youtube.com/shorts/<id>` link.

## Notes

- Uploads always go in as `privacyStatus: private` with `publishAt` set — YouTube auto-publishes at that time. If `publishAt` is in the past, YouTube publishes immediately.
- To replace a wrong/outdated upload: delete the old video via `youtube.videos().delete(id=...)`, then move the corrected yaml from `new/` to `waiting_upload/` and re-upload.
- To update only title/description/tags on a live or scheduled video without re-uploading: `youtube.videos().update(part="snippet", body={...})` — requires the `youtube` (not `youtube.upload`) OAuth scope, already set in `SCOPES`.
- Legacy videos rendered before this lifecycle existed may still have loose `_meta.json` files under `output/configs/` or `output/approved/` — those are historical leftovers, not part of the current flow.
