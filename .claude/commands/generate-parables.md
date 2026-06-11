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

## Topic pool — use these seeds (do not repeat lessons from existing parables)

Pick topics from this list. Rotate across categories — no two consecutive parables from the same category.

**Do not repeat these final lessons (parable_001–005 already covered):**
- A language lived in is never perfect. A language studied in is never alive.
- He had forgotten most of the maps. But he knew every road by heart.
- Stop adding. Start removing the fear.
- Fluency is not the absence of mistakes. It is the decision to speak before you are ready.
- The language only teaches you when you speak into it. Silence has no echo.

All five = "act before you're ready." New parables must land somewhere different.

**The lesson must be a reframe, not a command** — "you are not just learning words" not "go speak now."
**Specific detail over abstraction** — "she had friends in four countries" not "she succeeded."
**Screen 8 is the earliest the lesson can appear** — never before.
**Leave some things unresolved** — especially T12, T19, T20. Not every parable needs a happy ending.

### Identity & Change
| ID | Topic | Core tension | Avoid |
|----|-------|-------------|-------|
| T01 | Language changes personality — you become a different person in a new language | Who is the "real" you? | Don't moralize. Let the character decide. |
| T02 | Losing your accent as losing yourself — when fluency costs too much | Belonging vs. achievement | Don't resolve it neatly. Leave it open. |
| T03 | The moment you first dream in a foreign language | Surprise, not effort | Don't make it about hard work. It just happened. |
| T04 | A bilingual child who switches between two versions of themselves | Duality as strength | Don't make it a problem to solve. |

### The Middle of the Road
| ID | Topic | Core tension | Avoid |
|----|-------|-------------|-------|
| T05 | The plateau — progress stops and it feels like nothing is working | Persistence without reward | Don't promise it gets better. Sit in it. |
| T06 | A person who has studied for 10 years and still calls themselves a beginner | Self-perception vs. reality | Don't tell them they're wrong. Ask why. |
| T07 | The day motivation disappeared — and what happened next | Discipline vs. feeling | Don't replace motivation with discipline speech. |
| T08 | Exhaustion from the language — wanting to quit but being too far in | Sunk cost, not failure | Don't make quitting wrong. Make continuing honest. |

### Connection & People
| ID | Topic | Core tension | Avoid |
|----|-------|-------------|-------|
| T09 | A word that cannot be translated — and what it reveals about the people who use it | Language as worldview | Don't explain the word. Let it stay mysterious. |
| T10 | Speaking to a grandparent in their language for the first time | Regret and arrival | Don't sentimentalize. Keep it spare. |
| T11 | A person who learned a language for one specific person | Love as motivation | Don't judge the reason. Honor it. |
| T12 | Losing your native language after years abroad | Grief, not failure | Don't offer a solution. This is a real loss. |

### Time & Patience
| ID | Topic | Core tension | Avoid |
|----|-------|-------------|-------|
| T13 | A tree that grows slowly — on long journeys with no visible results | Faith without proof | Don't rush to the payoff. The slowness is the point. |
| T14 | An old person who starts learning a language at 70 — and why | It's never too late, but reframed | Don't make it inspirational. Make it quiet and true. |
| T15 | A person who quit and came back 5 years later | Return without shame | Don't make quitting a mistake. Make returning a choice. |

### Fear & Shame
| ID | Topic | Core tension | Avoid |
|----|-------|-------------|-------|
| T16 | The shame of an accent — and why an accent is not an error | Identity in sound | Don't fix the shame. Reframe what it means. |
| T17 | A person who stayed silent for a year before speaking a word aloud | Fear as information | Don't rush them. The silence means something. |
| T18 | Being laughed at for a mistake — who laughs and why it doesn't matter | Embarrassment vs. growth | Don't minimize the laugh. Redirect its meaning. |

### Provocation
| ID | Topic | Core tension | Avoid |
|----|-------|-------------|-------|
| T19 | The language you don't need to learn — on choice and honesty with yourself | Permission to stop | Don't make this negative. Make it liberating. |
| T20 | A person who speaks five languages and feels at home in none | Mastery without belonging | Don't resolve this. End in the question. |

## What to generate

Write 5 parables yourself — do not call any API or external script.

Pick 5 topics from the pool above — one from each of 5 different categories. Record which topic ID you used in the `topic` field.

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

## Output

After saving, print:
- How many parables were written
- The starting ID
- File path
- First line of each parable's screen 1
- One line per parable: what was fixed during review (or "no changes" if clean)
- Hook for each parable: `- parable_016: "Why do most learners go silent right before they improve?"`
