# Hoot & Pip — recurring-character series (test format)

Scope: a daily serial with three permanent characters, `ep_NNN` IDs, one episode per day at 20:30 ET — a **test format on top of the 4/day floor** (see CLAUDE.md "Minimum daily output").

## Why this exists

Analytics (Oct 2026): 8 subscribers on ~15.7k views (0.5 per 1000 views); every video is standalone, so a viewer from the Shorts feed has no reason to come back. The one video that converted well (4 of 8 subs, 258 views) was an animal parable with an absurd, relatable metaphor. Hypothesis: a named cast + episode numbers + a "next time" teaser gives people something to follow. **Success metric: subscribers gained per 1000 views for this format vs the 0.5 channel baseline** (pull with the Analytics API `subscribersGained` by video). Review after ~14 episodes (around Oct 26).

## Cast (do not change without a reason — continuity is the point)

- **Hoot** (owl) — the Studier. Keeps "the Notebook" (page numbers are a running gag: "page twelve: Train Vocabulary"). Speaks only in sentences he has checked. Warm, anxious, loyal. Catchphrase: "Let me check the notebook."
- **Pip** (pigeon) — the Doer. Knows three words and uses all of them. Never apologizes for a mistake, laughs and tries again. Shares everything (coffee, tickets). Catchphrase: "Close enough!"
- **Moss** (turtle) — the beginner, arrives in Ep. 3. One new word at a time, very slow, very brave. The viewer's stand-in.
- Side characters (use freely, don't build arcs): the sparrow barista at the Meadow Café, the market owl, the baker, the train conductor.
- Setting: the Meadow — Meadow Café, Meadow Market, the train to the lake. They learn "the Other Language" (never named, so any learner relates; keep concrete props: coffee, plum, train tickets, bread).

## The balance rule

Pip is not "right" and Hoot is not "wrong". Early episodes lean toward doing beating studying; the arc must move both ways: Hoot learns to speak before checking (Ep. 5), Pip learns to write one thing down (Ep. 6), and sometimes Hoot's notebook is exactly what saves the day. Don't let it become one joke repeated.

## Episode shape (same as the animal parable skill, plus continuity)

- screen 0: silent hook, ≤8 words, names a character or the situation ("Hoot left the notebook at home.")
- 6–8 story screens, mid-story turn around screen 4–5 (someone expects X, gets Y)
- warm concrete ending image — characters are friends, nobody is humiliated
- **final voiced screen: the teaser**, "Next time: …" (under 10 words), which must be answered by the next episode
- JSON carries `"episode": N` (used in the title: "<hook> | Hoot & Pip Ep. N")
- Narrator is always the `thomas` voice (the pipeline defaults to it for `ep_` IDs).

## Season 1 outline (first seven are written)

1 coffee order · 2 the wrong word (plum/drum) · 3 Moss arrives · 4 the train · 5 Hoot leaves the notebook home · 6 Pip opens a notebook · 7 Moss's sentence at the lake · next: Moss orders for the table, Hoot gets a page wrong in public and survives it, Pip's streak of mistakes ends and he misses it, a visitor who speaks the language natively and is bad at explaining it, etc.

## Episode log (hook → teaser, to keep continuity)

- Ep. 1: "Hoot studied a year. Pip studied a day." → Next time: Hoot tries three words.
- Ep. 2: "Pip said the wrong word. Twice." → Next time: Hoot says one sentence without checking.
- Ep. 3: "A turtle arrived with one word." → Next time: Moss learns word number two.
- Ep. 4: "Hoot checked the notebook. The train left." → Next time: Hoot leaves the notebook at home.
- Ep. 5: "Hoot left the notebook at home." → Next time: Pip opens a notebook.
- Ep. 6: "Pip opened a notebook for the first time." → Next time: the whole meadow goes to the lake.
- Ep. 7: "Moss said a whole sentence at the lake." → Next time: Moss orders for the whole table.
