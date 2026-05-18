# Generate Short

Run the full pipeline to produce one YouTube Short from the next available text.

## Steps

1. **Check texts** — if no `output/texts/batch_*.json` files exist, tell the user to run `/generate-texts` first and stop.

2. **Run pipeline** — execute:
   ```
   python3 main.py
   ```
   `main.py` handles everything: picks the next unused text, fetches images, selects music, builds config, renders video, marks text as used, and cleans up images.

3. **Report** — print:
   - Path to the final `.mp4`
   - YouTube title from the `_meta.json` sidecar
   - Remind the user to move the video to `output/approved/` to queue it for upload
