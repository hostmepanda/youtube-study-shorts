# Generate Parables

Generate a batch of 5 classic Zen/Buddhist-style parables for YouTube Shorts on language learning. Save them to `formats/parable-classic/drafts/`.

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
- The last line must be simple, clear, and uplifting — like a small breath of air. Not a riddle, not a stated moral, but an image or a short line that lands warm and obvious. The viewer should feel it instantly, not puzzle over it.
- Think of "I left her at the river. You are still carrying her." — concrete, simple, immediately understood, and slightly poetic. That is the target tone for every ending.
- **Keywords: 3–4 per parable, Pexels-friendly.** Use concrete visual scenes that Pexels actually has photos of. Avoid abstract or niche terms. Good: `river mist`, `stone bridge`, `foggy road`, `candle light room`, `old book`, `outdoor market`, `empty bench`, `misty mountain`. Bad: `monastery courtyard`, `monk sitting`, `zen paradox`.

  These pool keywords expand automatically in the fetcher — use them as starting points:
  `monastery`, `monk`, `river`, `bridge`, `market`, `candle`, `fog`, `temple`, `mountain`, `road`, `rain`, `jar`, `silence`, `book`, `well`

## Screen structure

- 1–3: set the scene — who, where, what's happening
- 4–7: the situation unfolds — action and dialogue
- 8–11: tension or contradiction builds
- Last 1–2 screens: the reversal — one line that reframes everything

## Topic pool & dedup

See `formats/parable-classic/topics.md` for the full T01–T20 topic pool (with core tension + what to avoid per topic) and the running list of final lessons already used — check it before writing so the new batch doesn't repeat a recent lesson or category.

Pick 5 topics from the pool — one from each of 5 different categories. Record which topic ID you used in the `topic` field.

## What to generate

Write 5 parables yourself — do not call any API or external script.

Each parable: 10–13 screens. Each screen: 1–2 lines.

**ID assignment:** Read `formats/parable-classic/used.json` and all existing `formats/parable-classic/drafts/parables_*.json` files. Find the highest `classic_XXX` number already used. Start the new batch from `highest + 1`. If none exist, start from `classic_001`.

Save the batch as a single JSON file at:
`formats/parable-classic/drafts/parables_YYYYMMDD_HHMMSS.json`

Format:
```json
[
  {
    "id": "classic_001",
    "topic": "...",
    "type": "parable",
    "mood": "parable",
    "keywords": ["keyword1", "keyword2"],
    "video_queries": ["query for screens 0-1", "query for screens 2-3", "..."],
    "screens": [
      {"screen": 0, "text": "Hook line"},
      {"screen": 1, "text": "Line 1\nLine 2"},
      ...
      {"screen": 12, "text": "The last line."}
    ]
  }
]
```

**`video_queries`** — one Pexels video search query per every 2 screens (ceil(total_screens / 2) entries).
Each query must match what actually happens in those screens — not atmospheric filler.
- screens 0-1 → hook + opening scene → query matches opening visual
- screens 2-3 → query matches what character does in those screens
- etc.

Good queries: `"market vendor throwing vegetable"`, `"person walking into shop"`, `"old woman reading book"`, `"foggy mountain path"`, `"two people arguing street"`
Bad queries: `"zen atmosphere"`, `"spiritual journey"`, `"language learning"`

Note: `"mood": "parable"` — this routes to calm background music.

## Hook generation — do this after writing all 5 parables, before the logic review

Generate a `screen_0` hook for each parable. Insert it as the first screen in the `screens` array.

**Rules:**
- One line only. Max 8 words.
- Must be a question OR a provocative incomplete statement.
- Must connect to the parable's core tension — not a generic "language learning" line.
- Must work as a standalone sentence on a black screen with no context.
- No character names. No "A man..." or "A student..." — that's the story starting, not a hook.
- Use "you" or make it feel personal where possible.

**Hook types that work:**
- Direct question: `"Why do most learners go silent right before they improve?"`
- Provocative claim: `"Knowing a language and speaking it are not the same thing."`
- Incomplete tension: `"He spoke five languages. He belonged to none."`
- Reframe: `"Your accent is not a mistake. It's a signature."`

**Hook types to avoid:**
- Generic: `"Language learning is hard."` — no tension
- Story openers: `"A monk once met a student..."` — that's screen 1
- Commands: `"Stop waiting and speak."` — that's the old lesson pattern

**Example mappings:**
| Topic | Hook |
|-------|------|
| T20 — speaks five languages, belongs to none | `"He spoke five languages. He belonged to none."` |
| T05 — the plateau | `"What do you do when progress just... stops?"` |
| T16 — shame of an accent | `"Your accent is not a mistake."` |
| T14 — learning at 70 | `"Is there an age when it's too late?"` |
| T03 — first dream in foreign language | `"The night it stopped feeling foreign."` |

**Updated format with screen_0:**
```json
{
  "screens": [
    {"screen": 0, "text": "Why do most learners go silent right before they improve?"},
    {"screen": 1, "text": "A boy came to an old well.\nHe had heard that if you spoke into it, the well would answer."},
    ...
  ]
}
```

### Pass 0 — Hook quality check (run before Pass 1 and Pass 2)

For each hook:
- Is it under 8 words? If not, cut it.
- Does it create a question in the viewer's mind? If not, rewrite.
- Does it match the parable's actual tension — not generic? If generic, rewrite.
- Would you stop scrolling for this? If not, rewrite.

Only proceed to Pass 1 after all hooks pass this check.

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
- Does the last line feel warm and clear — or does it leave the viewer confused?
- Is it inspiring? Would someone want to share it?
- It can be poetic, but it must be immediately understood — no puzzles, no ambiguity.
- It should feel like a small revelation, not a clever trick.

Only save the file after both passes are complete and all issues are fixed.

## Voice selection — note in output

See `formats/parable-classic/topics.md` for the voice table (elder/abbot/thomas/oliver). Default: elder. Override in `config/settings.yaml` → `premiss.voice` or via `--voice` flag.

## Output

After saving:
- Append each parable's topic ID + final lesson line to `formats/parable-classic/topics.md` under "Used final lessons"
- Print how many parables were written
- The starting ID
- File path
- First line of each parable's screen 1
- One line per parable: what was fixed during review (or "no changes" if clean)
- Hook for each parable: `- classic_001: "Why do most learners go silent right before they improve?"`
