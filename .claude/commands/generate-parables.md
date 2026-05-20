# Generate Parables

Generate a batch of 5 parables for YouTube Shorts on language learning. Save them to `output/texts/`.

## What a parable is

A mini-story in exactly 8 screens. Classic archetypes (traveler, wise man, student, craftsman). Builds tension slowly — the lesson lands on screen 8. More cinematic than motivational quotes.

## Style rules

- Simple, timeless English. No slang, no corporate words.
- Each screen: 2–4 lines
- Never explain the metaphor — let it speak
- Screen 8 is the lesson: 2–3 lines, no fluff
- Screen structure: 1–2 character + problem / 3–4 unexpected response / 5–6 tension builds / 7 the turn / 8 the lesson

## What to generate

Write 5 parables yourself — do not call any API or external script.

**ID assignment:** Read all existing `output/texts/parables_*.json` files. Find the highest `parable_XXX` number already used. Start the new batch from `highest + 1`. If none exist, start from `parable_001`.

Save the batch as a single JSON file at:
`output/texts/parables_YYYYMMDD_HHMMSS.json`

Format:
```json
[
  {
    "id": "parable_006",
    "topic": "...",
    "type": "parable",
    "mood": "calm",
    "keywords": ["keyword1", "keyword2"],
    "screens": [
      {"screen": 1, "text": "Line 1\nLine 2"},
      ...
      {"screen": 8, "text": "The lesson.\n2-3 lines."}
    ]
  }
]
```

## Output

After saving, print:
- How many parables were written
- The starting ID
- File path
- First line of each parable's screen 1
