# Generate Parables

Generate a batch of 5 parables for YouTube Shorts on language learning. Save them to `output/texts/`.

## What a parable is

A short classic parable — like a Buddhist or Zen story. Concrete situation. Real dialogue. A paradox or reversal at the end. The lesson is never stated — it lives in the last line or last action.

## Reference examples (the gold standard)

**Example 1 — The fisherman:**
A monk sat fishing by the river. A starving beggar asked for food.
The monk said: "If I give you my fish, I go hungry and you eat once.
If I give you my rod, I lose my livelihood.
So I will teach you how to make a rod — and how to fish."

**Example 2 — The woman at the river:**
Two monks crossed a river. A young woman stood afraid to cross.
One monk carried her on his shoulders. The other said nothing — but burned inside.
Hours later, at the monastery, he exploded: "It is forbidden to touch a woman!"
The first monk looked at him and said:
"I left her at the river. You are still carrying her."

## What makes these work

- Concrete situation — visual, specific, immediately clear
- Dialogue carries the meaning, not the narrator
- A twist or paradox at the end
- The last line IS the lesson — no explanation after it
- Short and complete — no emotional journey, just the moment and the punch

## Style rules

- Each screen: 1–2 lines maximum
- Plain language — no literary words, no abstractions
- Characters: monk, student, master, traveler, beggar, wise woman — timeless archetypes
- Setting: river, monastery, road, market, temple — simple and visual
- The story must connect to language learning — fear of speaking, silence vs mistakes, rules vs real use, the gap between knowing and doing
- Never name the lesson. Trust the last line.

## Screen structure

- 1–3: set the scene — who, where, what's happening
- 4–7: the situation unfolds — action and dialogue
- 8–11: tension or contradiction builds
- Last 1–2 screens: the reversal — one line that reframes everything

## What to generate

Write 5 parables yourself — do not call any API or external script.

Each parable: 10–13 screens. Each screen: 1–2 lines.

**ID assignment:** Read all existing `output/texts/parables_*.json` files. Find the highest `parable_XXX` number already used. Start the new batch from `highest + 1`. If none exist, start from `parable_001`.

Save the batch as a single JSON file at:
`output/texts/parables_YYYYMMDD_HHMMSS.json`

Format:
```json
[
  {
    "id": "parable_016",
    "topic": "...",
    "type": "parable",
    "mood": "parable",
    "keywords": ["keyword1", "keyword2"],
    "screens": [
      {"screen": 1, "text": "Line 1\nLine 2"},
      ...
      {"screen": 12, "text": "The last line."}
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
