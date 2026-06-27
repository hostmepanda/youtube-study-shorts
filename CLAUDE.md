# CLAUDE.md

## Publishing schedule — always US Eastern Time

All YouTube uploads (shorts and parables) must be scheduled relative to **US Eastern Time (America/New_York)**, not UTC and not the local machine timezone. This is the audience's timezone.

- `pipeline/youtube_uploader.py` already implements this: `PUBLISH_TZ = ZoneInfo("America/New_York")`, which automatically handles EST/EDT (daylight saving) transitions.
- If scheduling manually (ad-hoc `publishAt` for a custom time request), always convert the requested wall-clock time from US Eastern to UTC before sending it to the YouTube API — do not pass Eastern-time numbers directly as if they were UTC.
- Default schedule: shorts at 09:00 ET, long-monologue at 12:00 ET, parables at 16:30 ET, one per day starting today, queued in upload order.

## Render/publish lifecycle

- `output/videos/<id>.mp4` is the **permanent** home for every rendered video. Nothing in this codebase moves or deletes it — not `/clean-artifacts`, not the uploader, nothing.
- Each render also produces exactly one yaml at `formats/<format>/configs/new/<id>.yaml`, with YouTube metadata (title/description/tags) embedded under a `youtube:` key — there is no separate `_meta.json` sidecar anymore. That yaml is the thing that moves: `new/` → `waiting_upload/` (queue for upload — see `/publish`) → `archive/` (after a successful upload).
- `main.py` auto-deletes render scratch (wooden-roll's per-render audio/video cache, downloaded Pexels images) immediately after every successful render. Don't add a separate manual cleanup step for this — it already happens.
- New content IDs use per-format prefixes: `text_` (short-motivation), `classic_` (parable-classic), `animal_` (parable-animal), `longmono_` (long-monologue). Pre-restructure content kept its original `parable_NNN`/`short_NNN` ids and lives under `formats/legacy/` for lifecycle purposes — don't try to renumber or move it.

## Thumbnails (long-monologue)

Long-form videos need a custom thumbnail. `pipeline/thumbnail_generator.py` generates a branded 1280×720 JPEG — navy gradient background, gold accent bar, hook text (last line in gold), channel avatar in the bottom-right corner.

- Add `youtube.hook` to the yaml as a list of 2–3 lines; the uploader auto-generates the thumbnail before upload.
- To preview manually: `python3 pipeline/thumbnail_generator.py --lines "Line 1." "Line 2" "gold line." --output thumb.jpg`
- Channel avatar must exist at `channel-ava.png` in the project root.
- Format-level static fallback: `formats/long-monologue/thumbnail.jpg` (used if no `hook` is set in the yaml).
