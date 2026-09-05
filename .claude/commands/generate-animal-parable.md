# Generate Animal Parable Short

Generate one surreal animal parable and render it as a YouTube Short with the current production configuration.

## What this skill does

1. Write one animal parable with absurdist elements
2. Save it to `formats/parable-animal/drafts/`
3. Run the full pipeline (`python3 main.py`) to render the video

---

## What the parable must be

A SHORT, VIVID, PROVOCATIVE animal parable — 8–9 screens maximum. Simple enough to understand in one watch. Memorable enough to repost.

### What makes animal parables work

- **Short**: 8–9 screens, not 12. Every screen must earn its place.
- **Vivid**: one concrete detail that makes the world feel real ("In the mirror. Alone." / "She had arrived last Tuesday.")
- **Provocative ending**: the character who does LESS gets the SAME result. The last line is slightly uncomfortable for anyone who over-prepares. Not a riddle — a fact.
- Animals as characters — see `formats/parable-animal/topics.md` for the pool and used combos
- The absurd element is **matter-of-fact** — narrated without comment. Nobody reacts.
- The language learning connection lives in the action, never stated

### Style rules

- **8–9 screens total. Never more.**
- Screen 0 (hook): max 8 words, a **paradox** — not a description. Creates immediate tension.
- Each screen: 1–2 lines. Plain everyday English. No metaphors. No literary words.
- Last line: a **concrete fact or image** — undeniable, slightly uncomfortable.
  GOOD: "It tasted the same." / "She got the job." / "He was still at the door."
  BAD: "He kept the card in his pocket." / "She smiled." / symbolic gestures.
- The absurd element appears deadpan — described as normal fact.
- **Never name the lesson.** The discomfort IS the lesson.
- **Keywords: 3–4, Pexels-friendly** — concrete animals/scenes. No abstractions.
- **video_queries**: one per 2 screens, matching what literally happens. Real animals only.

### Absurd element ideas & animal pool

See `formats/parable-animal/topics.md` — pick 1–2 absurd-element ideas, and check the "used animals + devices" table before picking your animal/device combo so it doesn't repeat a recent parable.

---

## Format

```json
[
  {
    "id": "animal_XXX",
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
- No people in any query
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

Read `formats/parable-animal/used.json` and all existing `formats/parable-animal/drafts/parables_*.json` files. Find the highest `animal_XXX` number. New ID = highest + 1. If none exist, start from `animal_001`.

Save to: `formats/parable-animal/drafts/parables_YYYYMMDD_HHMMSS.json`

---

## Voice selection — pick before running the pipeline

See `formats/parable-animal/topics.md` for the voice table (linda/arina/oliver/thomas).

**How to pick:**
- Look at the parable's main character and emotional register
- Female protagonist or gentle/emotional arc → linda
- Female protagonist, alternative warm tone → arina
- Male protagonist, classic serious tone → oliver
- Male protagonist, absurdist or warm humor → thomas
- When unsure → linda (default)

Pass the chosen voice to the pipeline:
```bash
python3 main.py  # uses settings.yaml voice
```

Or override for this run by temporarily editing `config/settings.yaml` → `premiss.voice`.

## After saving the parable — run the pipeline

```bash
python3 main.py
```

`main.py` picks the next unused parable automatically. It will use the current production config:
- Voice: chosen from linda / arina / oliver / thomas based on parable tone
- Hook: silent, centered, 3 seconds, font 180
- Story text: bottom of screen, font 113
- Last screen: centered, font 180
- Outro (one screen): "Didn't motivate? / Drop a message in comments / [subscribe phrase] / @StudyGoTogether"
- Background: video footage from Pexels (from video_queries)
- Music: calm mood

## Output

After the video is rendered:
- Append the animal/device combo + topic to `formats/parable-animal/topics.md` under "Used animals + absurd devices"
- Print parable ID and topic
- Hook text
- Video path (local + iCloud)
- First line of screen 1
