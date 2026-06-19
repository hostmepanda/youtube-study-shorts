# Clean Artifacts

Remove leftover render scratch/cache that piles up across both repos. Safe to run periodically.

**Policy change:** `output/videos/*.mp4` is now the permanent home for every rendered video — it is never deleted by this skill (or by anything else). Only the yaml lifecycle file moves between `new/` → `waiting_upload/` → `archive/`; the video itself stays put forever. This skill no longer touches `.mp4` files anywhere, local or iCloud.

Most of what this skill used to clean by hand now happens automatically: `main.py` deletes the wooden-roll scratch dir and downloaded images/footage right after every successful render (see `cleanup_render_scratch()` in `main.py`). This skill is now a safety net for **leftovers from interrupted or failed runs**, plus pre-existing orphaned debris from before the yaml-lifecycle restructure.

## What gets cleaned

| Path | What it is | Why it's safe to delete |
|---|---|---|
| `output/configs/output/` | Orphaned Pexels video cache (pre-restructure path bug) | Pure cache, re-fetchable from Pexels |
| `output/images/*` | Downloaded Pexels images | `main.py` deletes these after every successful run now; strays mean an interrupted run |
| `wooden-roll/output/audio/<id>/` dirs with no matching `output/videos/<id>.mp4` | Scratch dirs from a render that failed or was interrupted before producing a final video | The render never completed, so there's nothing downstream depending on this scratch data |
| `output/approved/*_meta.json`, `output/uploaded/` contents | Debris from the pre-restructure approve/upload flow (retired — see `/publish`) | No longer read by any code path; the yaml-lifecycle replaced this entirely |

## What never gets touched

- Any `.mp4` in `output/videos/` — permanent, by design, regardless of publish status
- Any `.mp4` in iCloud (`~/Library/Mobile Documents/com~apple~CloudDocs/Experiments/Youtube-shorts/output/`) — also left alone now; only the policy on local video deletion changed today, but to keep this simple, iCloud copies aren't touched by this skill either
- `output/texts/*.json`, `formats/*/drafts/*.json` — source content
- `formats/*/configs/{new,waiting_upload,archive}/*.yaml` — the lifecycle files themselves, and `formats/*/used.json`, `formats/*/topics.md`
- `wooden-roll/output/audio/<id>/` dirs that DO have a matching `output/videos/<id>.mp4` — if a video exists, don't assume the scratch dir is safe to remove without checking it isn't from an in-progress run

## Steps

1. **Report sizes before cleaning**:
   ```bash
   du -sh /Users/panda/Development/private/youtube-study-shorts/output 2>/dev/null
   du -sh /Users/panda/Development/private/wooden-roll/output 2>/dev/null
   ```

2. **Find orphaned scratch dirs** — for each `wooden-roll/output/audio/<id>/`, check whether `output/videos/<id>.mp4` exists. If it doesn't, the render never finished and the scratch dir is dead weight.

3. **Delete**:
   ```bash
   rm -rf /Users/panda/Development/private/youtube-study-shorts/output/configs/output
   rm -rf /Users/panda/Development/private/youtube-study-shorts/output/images/*
   rm -rf /Users/panda/Development/private/youtube-study-shorts/output/approved
   rm -rf /Users/panda/Development/private/youtube-study-shorts/output/uploaded
   # Only scratch dirs confirmed orphaned in step 2:
   rm -rf "/Users/panda/Development/private/wooden-roll/output/audio/<orphaned-id>"
   ```

4. **Report sizes after** and the total freed.

## Notes

- This is irreversible for the paths it touches, but none of them hold anything not reproducible (cache) or already-dead (debris from a retired flow). Still, show what's about to be deleted before running `rm`.
- If you're unsure whether a `wooden-roll/output/audio/<id>/` dir belongs to an in-progress render (not yet failed, just slow), check whether `main.py` is currently running before deleting it.
