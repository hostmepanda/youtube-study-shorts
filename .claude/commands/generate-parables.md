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
- **Keywords: 3–4 per parable, Pexels-friendly.** Use concrete visual scenes that Pexels actually has photos of. Avoid abstract or niche terms. Good: `river mist`, `stone bridge`, `foggy road`, `candle light room`, `old book`, `outdoor market`, `empty bench`, `misty mountain`. Bad: `monastery courtyard`, `monk sitting`, `zen paradox`.

  These pool keywords expand automatically in the fetcher — use them as starting points:
  `monastery`, `monk`, `river`, `bridge`, `market`, `candle`, `fog`, `temple`, `mountain`, `road`, `rain`, `jar`, `silence`, `book`, `well`

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

## Logic review — run twice before saving

After writing all 5 parables, run two review passes. Fix any issues found before saving the file.

### Pass 1 — Internal consistency
For each parable, check screen by screen:
- Does each screen follow logically from the previous one?
- Are there any contradictions between what the narrator shows and what a character later claims?
- Does the final line follow from what actually happened in the story — or does it assume something the reader never saw?
- Are any two screens saying the exact same thing (redundancy)?

Example of a logic gap to catch:
> Screen 3 says students "speak slowly, rarely" — but Screen 8 says they "say nothing."
> These contradict. Fix one or the other before saving.

### Pass 2 — Punch check
For each parable, ask:
- Does the last line land as a surprise or reversal — or does the reader already know it from earlier screens?
- Is the lesson implicit in the action, or is it stated explicitly? (Explicit = rewrite.)
- Could you cut the last screen and still understand the point? (If yes, the second-to-last screen is the real ending — delete the last one.)

Only save the file after both passes are complete and all issues are fixed.

## Output

After saving, print:
- How many parables were written
- The starting ID
- File path
- First line of each parable's screen 1
- One line per parable: what was fixed during review (or "no changes" if clean)
