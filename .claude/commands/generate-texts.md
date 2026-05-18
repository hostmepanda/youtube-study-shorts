# Generate Texts

Generate a batch of 10 motivational texts for YouTube Shorts on language learning. Save them to `output/texts/`.

## Style rules

- English only
- 5–7 lines per text — each line appears on its own screen
- Structure: build tension across the first 3–5 lines, resolve with a call to action in the last 1–2
- Tone: direct, honest, no aggression, a drop of warmth and belief in the person
- NOT: fluffy, corporate, preachy, philosophical, childish
- Each line must be short — max 8 words
- Lines can be fragments — punchy is better than complete

## Reference example (match this level)

```
You've been studying for two years.
You know the grammar.
You know the words.
But you still don't speak.
That's not a study problem.
That's a courage problem.
Fix it today.
```

## What to generate

Write 10 unique texts. For each, assign:
- `mood`: one of `motivational`, `calm`, `uplifting`
- `keywords`: 2–3 words for finding a relevant background photo (concrete nouns/scenes, e.g. "conversation", "open road", "morning light")

## Output format

Save the batch as a single JSON file at:
`output/texts/batch_YYYYMMDD_HHMMSS.json`

Format:
```json
[
  {
    "id": "text_001",
    "lines": ["Line 1", "Line 2", "Line 3"],
    "mood": "motivational",
    "keywords": ["keyword1", "keyword2"]
  }
]
```

After saving, print how many texts were written and the file path.
