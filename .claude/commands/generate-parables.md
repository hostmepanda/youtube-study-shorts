# Generate Parables

Generate a batch of 5 parables for YouTube Shorts on language learning. Save them to `output/texts/`.

## What a parable is

A mini-story in 10–15 screens. Classic archetypes (traveler, wise man, student, craftsman, child, exile, stranger). Hooks immediately — screen 1 grabs attention like a short. Builds emotional tension slowly. The lesson lands on the last screen. More cinematic than motivational quotes.

## Style rules

- Simple, timeless English. No slang, no corporate words.
- Each screen: 2–4 lines
- Never explain the metaphor — let it speak
- Start with a hook — screen 1 should make the viewer want to know what happens next
- Lean into emotion: longing, fear of being left behind, quiet pride, small victories
- Always end on something positive or hopeful — the lesson is empowering, not bleak
- The last screen is the lesson: 2–3 lines, no fluff
- Screen structure:
  - 1–2: hook — character + a sharp problem or surprising situation
  - 3–5: unexpected response or first attempt (failure, confusion, or small courage)
  - 6–8: tension builds — something at stake, the character is tested
  - 9–11: things shift — a small turning point, a moment of connection or insight
  - 12–14: the change lands — show don't tell
  - Last screen: the lesson

## What to generate

Write 5 parables yourself — do not call any API or external script.

Each parable must have between 10 and 15 screens. Vary the length across the batch.

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
    "mood": "parable",
    "keywords": ["keyword1", "keyword2"],
    "screens": [
      {"screen": 1, "text": "Line 1\nLine 2"},
      ...
      {"screen": 12, "text": "The lesson.\n2-3 lines."}
    ]
  }
]
```

Note: `"mood": "parable"` — this routes to calm background music.

## Output

After saving, print:
- How many parables were written
- The starting ID
- File path
- First line of each parable's screen 1
