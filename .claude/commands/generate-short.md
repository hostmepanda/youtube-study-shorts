# Generate Short

Generate one complete YouTube Short on language learning.

## Steps

1. **Generate text** — write 3 motivational lines in English. Style: direct, honest, no aggression, a drop of warmth. First two lines: fact or provocation. Third line: call to action or conclusion. Short lines, no fluff. Pick a mood (motivational / calm / uplifting) and 2-3 image keywords.

2. **Save text** — write the result to `output/texts/` as a JSON file named `text_YYYYMMDD_NNN.json` with fields: `id`, `lines` (array of 3), `mood`, `keywords`.

3. **Fetch image** — run `python3 pipeline/image_fetcher.py --keywords "<keywords from step 1>"`. It will save an image to `output/images/` and return the path.

4. **Select music** — run `python3 pipeline/music_selector.py --mood <mood from step 1>`. It will return the path to a random track.

5. **Build config** — run `python3 pipeline/config_builder.py --text-file <path> --image <path> --music <path>`. It generates a wooden-roll YAML in `output/configs/`.

6. **Render video** — run `node ../wooden-roll/src/pipeline.js <config path>`. The output MP4 lands in `output/videos/`.

7. **Report** — print the path to the final video and the metadata (title, description, tags) ready for YouTube upload.
