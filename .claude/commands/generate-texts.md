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

Pick a structure for each text, weighted toward **2 (Observation → Twist → Call to action)**, **4 (They vs You contrast)**, and **8 (Story fragment)** — these have the strongest retention track record (see below) — while still using the full set of 10 across the batch, not just these three.

See `formats/short-motivation/topics.md` for the 10 structures (with examples), the retention-proven pattern, and the running list of used final lines — check it before writing so new texts don't land on the same closing punch as a recent batch.

### Every text should hit these three (regardless of structure)

Retention data shows these three traits separate the 50–70%+ retention texts from the rest:

1. **Hook = the viewer's own thought, verbatim** — `"You feel no progress"`, not `"Language learning takes time"`. Write the first line as something the target viewer would think, not a statement about them.
2. **At least one concrete number or timeline** — an age, a duration, a "first week / second week / third month" progression. Never leave it purely abstract.
3. **A mid-script reversal, around line 3–4 of 5–7** — set up an expected bad outcome, then break it in the next line (`"They won't"`, `"The waiter understood"`). Keep this distinct from the closing line — it's an earlier re-hook, not the final punch.

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
