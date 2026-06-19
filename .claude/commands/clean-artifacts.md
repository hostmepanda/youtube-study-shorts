# Clean Artifacts

Remove leftover video/audio rendering artifacts and caches that pile up across both repos. Safe to run periodically — never touches source texts or configs (yaml/meta.json). Never deletes anything from the actual YouTube channel — only local/iCloud *copies* of videos once they're confirmed live.

## What gets cleaned

| Path | What it is | Why it's safe to delete |
|---|---|---|
| `output/configs/output/` | Orphaned Pexels video cache (created by a path bug — cwd resolved wrong at some point) | Pure cache, re-fetchable from Pexels |
| `output/videos/*.mp4` | Rendered videos | Once a video has been uploaded (moved into `output/uploaded/`) the render in `output/videos/` is a leftover duplicate |
| `output/images/*` | Downloaded Pexels images used for old text-type shorts | `main.py` is supposed to delete these after each run; strays are leftovers from interrupted runs |
| `output/uploaded/*.mp4` | Local copies of videos already pushed to YouTube | Already live on YouTube — local copy is redundant |
| `~/Library/Mobile Documents/com~apple~CloudDocs/Experiments/Youtube-shorts/output/*.mp4` | iCloud copies of videos already pushed to YouTube | Same reasoning — once live on YouTube, the iCloud backup copy has served its purpose and is redundant |
| `wooden-roll/output/audio/*` | Per-render scratch dirs: TTS `full_audio.wav`, `bg_clip_*.mp4`, `subtitles.ass`, timeline JSON | Pure intermediate render output; the final video already lives in `output/videos/` or has been uploaded |

## What never gets touched

- `output/texts/*.json` — parable/text source content
- `output/configs/*.yaml` and `*_meta.json` — configs and metadata sidecars (only the stray nested `output/configs/output/` dir is removed)
- `output/approved/*_meta.json` — metadata sidecars for queued uploads
- The actual videos on the YouTube channel — this skill never calls any YouTube delete API, only cleans local/iCloud file copies

## Steps

1. **Report sizes before cleaning** — run:
   ```bash
   du -sh /Users/panda/Development/private/youtube-study-shorts/output 2>/dev/null
   du -sh /Users/panda/Development/private/wooden-roll/output 2>/dev/null
   du -sh "/Users/panda/Library/Mobile Documents/com~apple~CloudDocs/Experiments/Youtube-shorts/output" 2>/dev/null
   ```

2. **Check for videos in `output/videos/` that are NOT yet in `output/uploaded/` or `output/approved/`** — these may be pending review (just rendered, not yet decided on). List them and ask the user before deleting anything not already archived/uploaded. Only auto-delete videos in `output/videos/` (and their iCloud counterparts) that have an exact filename match already sitting in `output/uploaded/` — that's the signal a video is confirmed live.

3. **Delete the artifacts**:
   ```bash
   rm -rf /Users/panda/Development/private/youtube-study-shorts/output/configs/output
   rm -rf /Users/panda/Development/private/youtube-study-shorts/output/images/*
   rm -rf /Users/panda/Development/private/wooden-roll/output/audio/*
   # Only the videos confirmed in step 2 as already-uploaded duplicates:
   rm -f /Users/panda/Development/private/youtube-study-shorts/output/videos/<matched-files>.mp4
   rm -f /Users/panda/Development/private/youtube-study-shorts/output/uploaded/<matched-files>.mp4
   rm -f "/Users/panda/Library/Mobile Documents/com~apple~CloudDocs/Experiments/Youtube-shorts/output/<matched-files>.mp4"
   ```

4. **Report sizes after** and the total freed.

## Notes

- This is a destructive, irreversible local cleanup (no git tracking on these dirs, and iCloud deletion isn't undoable from here). Always show what's about to be deleted before running `rm`, per standard safety practice.
- If `output/uploaded/` or `output/videos/` contains anything that hasn't been confirmed live on YouTube (no matching filename pattern indicating it went through the uploader), stop and ask the user instead of deleting.
- Accessing the iCloud path from a sandboxed shell may raise "Operation not permitted" — if so, ask the user to grant Full Disk Access to the terminal/tool, or have them delete that specific file manually.
