# Hoot & Pip — dialogue comedy series (test format)

Scope: a daily serial, `ep_NNN` IDs, slot 20:30 ET — a **test format on top of the 4/day floor** (see CLAUDE.md "Minimum daily output"). It never counts toward the floor.

**Redesigned 2026-10-25.** The first version (narrator + stock footage + Moss the turtle, Ep. 1–7, still in `configs/waiting_upload/`) is obsolete: it was "animal parables with constant animals". The new version is a **dialogue comedy**: two consistent characters, one foreign-language situation per episode, a joke the viewer gets without knowing the language. Old episodes are not uploaded; the experiment clock restarts from the first new upload (no review date set yet).

## Why this exists

Analytics (Oct 2026): 8 subscribers on ~15.7k views (0.5 per 1000 views); every video is standalone, so nothing gives a viewer a reason to come back. Hypothesis: two named, visually identical characters + a recognizable episode shape ("they land in a new language") + a joke people share gives something to follow. **Success metric: subscribers gained per 1000 views vs the 0.5 channel baseline** (Analytics API `subscribersGained` by video).

## The hook of the series (the "изюминка")

Hoot and Pip travel through the world's languages. Every episode: a real place, a real native speaker, one real foreign phrase, one misunderstanding — and at the end a **"Say it right" card** with the correct phrase (a mini language lesson hidden inside a joke, so it fits a channel for people learning languages). The channel is not tied to one language: Spanish, French, Italian, German, Japanese, Portuguese, Korean… rotate, never two in a row.

## Cast (do not change without a reason)

- **Hoot** (owl) — the Studier. Knows rules, textbook phrases, grammar. Anxious, precise, good-hearted. Over-translates literally. Catchphrase: "Let me check the notebook." (use sparingly, not every episode)
- **Pip** (pigeon) — the Doer. Knows three words and uses all of them with total confidence. Never apologizes. Wins by confidence, loses by not understanding what he said. Catchphrase: "Close enough!" (sparingly)
- **Natives** — one new local character per episode (sparrow waiter, baker, station clerk, grandma on a bench…). Always a bird, no humans. Speaks real local language in a local voice, plus the English line that carries the joke.
- No permanent third character. No arcs between episodes; **no "next time" teaser required**. Episodes are standalone, so any one can be a viewer's first.

## The clarity rule (most important)

Every foreign word must be understood by a non-speaker **inside the dialogue**, never only from the card. Either a character translates it ("embarazado means pregnant"), or the situation makes it obvious (the baker grabs Hoot's leg). No in-jokes, no references to "page 12", no unexplained words. Test: read the script as someone with zero knowledge of the language — if any line is a puzzle, rewrite it. The last two lines of an episode are the punch and the warm landing; both must be instantly clear.

## Humor engines (rotate; don't repeat one twice in a row)

1. **Pip wins by confidence** — he says the wrong thing with total certainty and the mistake is rewarded (Spain: "Estoy embarazado" → free cake).
2. **Hoot errs by literal translation** — he translates an English idiom word for word ("You're pulling my leg" → "Je tire ta jambe"). The native acts it out.
3. **Both err in opposite ways and combine** — postponed: needs tonal languages (Mandarin) and our TTS can't do tones yet.
4. **Textbook vs real life** — Hoot's slow textbook sentence meets fast native speech (Italian station). He catches one word out of twenty.
5. **Role reversal (rare)** — Hoot is the one who improvises and wins, Pip is the one who checked. Max one in six episodes.

## Episode shape (≈25 s)

- Hook text on screen (≤8 words, names the situation): "Pip told the waiter a secret."
- 6 shots, one per beat, **S1 setup → S2 reaction → S3 correction/explanation → S4 payoff → S5 landing → S6 "Say it right" card**.
- 4–6 spoken lines, each ≤ ~15 words. Hoot and Pip speak English with foreign words inserted; natives speak the foreign language and, where needed, English.
- Ending: warm, nobody humiliated, the last line is the punch. Then the outro card: "Hoot & Pip / New episode every day / Subscribe to follow them / @StudyGoTogether".
- Title format: "<hook> | Hoot & Pip (<Language>)".

## Season 1 plan

| Ep | Language | Engine | Situation | Status |
|----|----------|--------|-----------|--------|
| 1 | Spanish | 1 Pip wins | Café: Pip says "embarazado" (pregnant) instead of "avergonzado" (embarrassed); waiter brings a free cake | uploaded 2026-10-26 (`ep_001`, `hTpBxpBjWCQ`) |
| 2 | French | 2 Hoot literal | Bakery stall: "Vous tirez ma jambe" (you pull my leg); native = Gallic rooster, Eiffel Tower backdrop | uploaded 2026-10-29 (`ep_002`, `RPNB4va7S_s`), long format 50 s |
| 3 | Italian | 4 textbook vs real | Train station: slow textbook question, answer at 200 wpm | script in `scripts/` |
| 4 | German | 1 or 5 | long compound word / "Ich bin voll" (restaurant) | idea |
| 5 | Portuguese | 2 | "saudade" explained literally | idea |
| 6 | Japanese | 4 | polite vs casual, vending machine / bow | idea |

## Production guide (what to prompt and what to watch)

Full technical notes live in `formats/series-hoot-pip/production.md`.

## Legacy (narrator-format) episode log — obsolete, kept for reference

Ep. 1 coffee order · 2 the wrong word (plum/drum) · 3 Moss arrives · 4 the train · 5 Hoot leaves the notebook home · 6 Pip opens a notebook · 7 Moss's sentence at the lake. Seven rendered mp4s with yamls in `configs/waiting_upload/`; superseded by this bible, do not upload unless the user asks.
