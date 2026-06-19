# Generate Animal Parable Short

Generate one surreal animal parable and render it as a YouTube Short with the current production configuration.

## What this skill does

1. Write one animal parable with absurdist elements
2. Save it to `output/texts/`
3. Run the full pipeline (`python3 main.py`) to render the video

---

## What the parable must be

A short classic parable — like a Buddhist or Zen story — but with **animal characters** and **absurdist / surreal elements**. The lesson about language learning is never stated: it lives in the last line or last action.

### What makes animal/absurd parables work

- Animals as characters (bear, horse, fox, crow, turtle, owl, pigeon, cat, goat…)
- The absurdity is **matter-of-fact** — narrated without surprise or comment. The horse opens a bank account. The bear weighs a jar of honey before answering a question. Nobody reacts.
- The surreal element must feel **earned**, not random — it reflects the character's inner logic
- The last line is the lesson — warm, simple, immediately understood. Not a riddle.
- The language learning connection must be **visible in the action**, not stated

### Style rules

- Each screen: 1–2 lines maximum
- Plain language — no literary words, no abstractions
- Mix dialogue and narration — animals talk normally
- The absurd scenes are described deadpan: "He reached into his coat and produced a small set of scales."
- **Never name the lesson.** Trust the last line.
- **Keywords: 3–4 per parable, Pexels-friendly** — concrete visual scenes. Animals are good: `bear forest`, `horse meadow`, `fox path`. Avoid abstract: `wisdom`, `language learning`.
- **video_queries**: one query per 2 screens, based on what actually happens on those screens. Use real animals: `bear walking forest`, `horse running field`, `fox sitting path`. Avoid atmospheric filler.

### Absurd element ideas (pick 1–2 per parable)

- An animal pulls an unrelated object from its coat/trousers (scales, compass, small notebook, jar, umbrella, clock)
- An animal does something completely irrelevant before answering (dances, bows, counts to ten, writes something down)
- A reaction that makes no logical sense but feels emotionally right (a pigeon quits a job, a bear takes notes at the wrong moment)
- A reversal of scale (a very small animal teaches a very large one; a famous creature turns out to be bad at something obvious)

---

## Format

```json
[
  {
    "id": "parable_XXX",
    "topic": "...",
    "type": "parable",
    "mood": "parable",
    "keywords": ["bear", "forest", "fog"],
    "video_queries": [
      "bear walking forest nature",
      "horse running field open",
      "..."
    ],
    "screens": [
      {"screen": 0, "text": "Hook — max 8 words, centered, silent"},
      {"screen": 1, "text": "Line 1\nLine 2"},
      ...
      {"screen": 12, "text": "The last line."}
    ]
  }
]
```

### Screen structure

- **screen 0**: hook — max 8 words, question or provocative claim, specific to the parable's tension. This screen is **silent** (not voiced) and shown centered for 3 seconds.
- screens 1–3: set the scene — who, where, what animal, what absurd detail
- screens 4–7: situation unfolds — dialogue, absurd action, language learning tension
- screens 8–11: contradiction or reversal builds
- last 1–2 screens: the punch — one line that reframes everything

### video_queries rules

- ceil(total_screens / 2) entries
- Each query matches what happens on those 2 screens — not atmospheric
- Use real animals where possible: `bear eating honey`, `horse standing meadow`, `fox sitting stone`
- Good: `"bear sitting grass writing"`, `"two horses talking field"`, `"owl perched branch night"`
- Bad: `"zen atmosphere"`, `"language learning concept"`, `"wisdom"` 

---

## Hook quality check (Pass 0)

For the hook (screen 0):
- Under 8 words? If not, cut.
- Creates a question in the viewer's mind? If not, rewrite.
- Specific to this parable's tension — not generic? If generic, rewrite.
- Would you stop scrolling for this? If not, rewrite.

Examples of good animal/absurd hooks:
- `"She danced. Said three words. He had studied years."` (bear/horse)
- `"He spoke five languages. He belonged to none."`
- `"The owl had read every book. Couldn't order lunch."`
- `"She prepared for three winters. He just tried."`

---

## Logic review (Pass 1 + Pass 2)

### Pass 1 — consistency
- Does each screen follow from the previous one?
- Are there contradictions between what the narrator shows and what a character claims?
- Does the final line follow from what actually happened?
- Redundant screens?

### Pass 2 — punch check
- Does the last line land warm and clear?
- Is the lesson implicit (in the action) — not stated?
- Would someone want to share this?

Only proceed after both passes pass.

---

## ID assignment

Read all `output/texts/parables_*.json` files. Find the highest `parable_XXX` number. New ID = highest + 1.

Save to: `output/texts/parables_YYYYMMDD_HHMMSS.json`

---

## Voice selection — pick before running the pipeline

Three approved voices. Pick the one that fits the parable's tone and main character:

| Voice | Gender | Best for |
|-------|--------|----------|
| diana | female | parables with a female lead, gentle or introspective tone, emotional endings |
| oliver | male | parables with a male lead, classic/timeless tone, wise or calm narrator feel |
| thomas | male | parables with a male lead, warmer or slightly playful tone, absurdist stories |

**How to pick:**
- Look at the parable's main character and emotional register
- Female protagonist or gentle/emotional arc → diana
- Male protagonist, classic serious tone → oliver
- Male protagonist, absurdist or warm humor → thomas
- When unsure → diana (default)

Pass the chosen voice to the pipeline:
```bash
python3 main.py  # uses settings.yaml voice (diana by default)
```

Or override for this run by temporarily editing `config/settings.yaml` → `premiss.voice`.

## After saving the parable — run the pipeline

```bash
python3 main.py
```

`main.py` picks the next unused parable automatically. It will use the current production config:
- Voice: chosen from diana / oliver / thomas based on parable tone
- Hook: silent, centered, 3 seconds, font 180
- Story text: bottom of screen, font 113
- Last screen: centered, font 180
- Outro (one screen): "Didn't motivate? / Drop a message in comments / [subscribe phrase] / @StudyGoTogether"
- Background: video footage from Pexels (from video_queries)
- Music: calm mood

## Output

After the video is rendered, print:
- Parable ID and topic
- Hook text
- Video path (local + iCloud)
- First line of screen 1
