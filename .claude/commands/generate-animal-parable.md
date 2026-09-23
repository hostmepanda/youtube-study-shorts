# Generate Animal Parable Short

Generate one surreal animal parable and render it as a YouTube Short with the current production configuration.

## What this skill does

1. Write one animal parable with absurdist elements
2. Save it to `formats/parable-animal/drafts/`
3. Run the full pipeline (`python3 main.py`) to render the video

---

## What the parable must be

A SHORT, VIVID, PROVOCATIVE animal parable — 8–9 story screens maximum, plus one final voiced comment-question (see "Comment-question screen" below). Simple enough to understand in one watch. Memorable enough to repost.

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

### Comment-question screen (new, 2026-09-23 — engagement experiment)

**Add one extra screen after the punch line: a voiced question, addressed to the viewer, specific to this parable's animal and situation.** This is a deliberate engagement experiment — analytics showed 0 comments across 254 videos on the channel, and the generic silent outro CTA ("Drop a message in comments") clearly isn't prompting anyone. A specific, voiced question about *this* story is the test for whether that changes.

- It becomes the actual last entry in `screens` — so it inherits the big, centered "last screen" treatment and gets voiced by the TTS along with everything else (no separate pipeline step needed).
- Ask about the animal's specific choice or the specific absurd device, not a generic "what did you learn" — e.g. `"Why do you think the crow couldn't say it?"`, `"Would you have kept tapping the gavel?"`, `"What's your version of the stopwatch?"`
- Keep it under 10 words, genuinely curious in tone — not rhetorical, not leading to an obvious one-word answer.
- The silent text-only outro screen after this (handled automatically by the pipeline) now just says "Answer below" + the subscribe line — don't duplicate the question there.

Example:
```
{"screen": 7, "text": "Sheep put the stamp away mid-air, unused, for the rest of the day."},
{"screen": 8, "text": "Would you have kept stamping?"}
```

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
      {"screen": 8, "text": "The punch line."},
      {"screen": 9, "text": "Voiced comment-question — see below"}
    ]
  }
]
```

### Screen structure (8–9 story screens + hook + comment-question)

- **screen 0**: hook — max 8 words, question or provocative claim, specific to the parable's tension. This screen is **silent** (not voiced) and shown centered for 3 seconds.
- screens 1–2: set the scene — who, where, what animal, what absurd detail
- screens 3–4: situation unfolds — dialogue, absurd action, language learning tension
- **screen ~5 (mid-story turn): something the viewer expects doesn't happen.** Retention data shows viewers drop off long before the final line if the story saves 100% of its surprise for the end — a smaller, earlier reversal re-hooks them. Pattern: the animal braces for one outcome (correction, rejection, ridicule) and gets the opposite ("The sparrow didn't laugh." / "Nobody noticed the wrong word."). Keep this distinct from the ending — don't let it become the same beat.
- next 2–3 screens: the punch — one line that reframes everything (the character who does LESS gets the SAME result)
- **final screen: the voiced comment-question** (see "Comment-question screen" above) — this is now the true last screen and gets the big centered treatment

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

## Logic review (Pass 1 + Pass 1.5 + Pass 2)

### Pass 1 — consistency
- Does each screen follow from the previous one?
- Are there contradictions between what the narrator shows and what a character claims?
- Does the final line follow from what actually happened?
- Redundant screens?

### Pass 1.5 — mid-story turn check
- Is there a clear reversal around screen 5, distinct from the ending?
- Does it break an expectation set up in the 1–2 screens just before it — not just add new information?
- If it feels identical to the ending beat, add a real setup-and-break moment earlier.

### Pass 2 — punch check
- Does the punch line (second-to-last screen) land warm and clear?
- Is the lesson implicit (in the action) — not stated?
- Would someone want to share this?

### Pass 3 — comment-question check
- Is the question specific to this animal/device, not generic ("What did you learn?")?
- Under 10 words?
- Does it invite a real, personal answer rather than yes/no?

Only proceed after all three passes pass.

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
- Last screen (the comment-question): centered, font 180, voiced
- Outro (one silent screen, automatic): "Answer below / [subscribe phrase] / @StudyGoTogether"
- Background: video footage from Pexels (from video_queries)
- Music: calm mood

## Output

After the video is rendered:
- Append the animal/device combo + topic to `formats/parable-animal/topics.md` under "Used animals + absurd devices"
- Print parable ID and topic
- Hook text
- Video path (local + iCloud)
- First line of screen 1
