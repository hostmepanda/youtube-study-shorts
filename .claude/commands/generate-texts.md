# Generate Texts

Generate a batch of 10 motivational texts for YouTube Shorts on language learning. Save them to `formats/short-motivation/drafts/`.

## Style rules

- English only
- 5–7 lines per text — each line appears on its own screen
- Tone: direct, honest, no aggression, a drop of warmth and belief in the person
- NOT: fluffy, corporate, preachy, philosophical, childish
- Each line must be short — max 8 words
- Lines can be fragments — punchy is better than complete
- Never end a line with a full stop (.)

## Structures & dedup

Pick a structure **randomly** for each text. Use all 10 across a batch of 10.

See `formats/short-motivation/topics.md` for the 10 structures (with examples) and the running list of used final lines — check it before writing so new texts don't land on the same closing punch as a recent batch.

## What to generate

Write 10 unique texts. For each, assign:
- `mood`: one of `motivational`, `calm`, `uplifting`
- `keywords`: 2–3 words for finding a relevant background photo (concrete nouns/scenes, e.g. "conversation", "open road", "morning light")

## Output format

Save the batch as a single JSON file at:
`formats/short-motivation/drafts/batch_YYYYMMDD_HHMMSS.json`

**ID assignment:** Read `formats/short-motivation/used.json` and all existing `formats/short-motivation/drafts/batch_*.json` files. Find the highest numeric ID already used (e.g. if `text_023` exists, the highest is 23). Start the new batch from `highest + 1`. If no prior IDs exist, start from `text_001`.

Format:
```json
[
  {
    "id": "text_031",
    "lines": ["Line 1", "Line 2", "Line 3"],
    "mood": "motivational",
    "keywords": ["keyword1", "keyword2"]
  }
]
```

After saving, append each text's closing line to the "Used final lines" section of `formats/short-motivation/topics.md`.

After saving, print how many texts were written, the starting ID, and the file path.
