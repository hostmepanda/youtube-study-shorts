# Generate Short

Run the full pipeline to produce one YouTube Short from the next available text.

## Steps

1. **Pick text** — find the oldest unused JSON file in `output/texts/`. If none exist, tell the user to run `/generate-texts` first and stop.

2. **Fetch image** — run:
   ```
   python3 pipeline/image_fetcher.py --keywords "<comma-separated keywords from text file>"
   ```

3. **Select music** — run:
   ```
   python3 pipeline/music_selector.py --mood <mood from text file>
   ```

4. **Build config** — run:
   ```
   python3 pipeline/config_builder.py --text-file <path> --image <path> --music <path>
   ```

5. **Render video** — run:
   ```
   python3 main.py <config path from step 4>
   ```

6. **Report** — print:
   - Path to the final `.mp4`
   - YouTube title, description, and tags from the `_meta.json` sidecar
