# Generate Series Episodes (Hoot & Pip)

Write the next batch of episodes for the recurring-character test series. Read `formats/series-hoot-pip/topics.md` first: it has the cast bible, the balance rule, the success metric and the **episode log** (hook → teaser of every episode so far).

## Rules

- Continuity is the product. Every episode must answer the previous episode's teaser, and its own last screen must be a new "Next time: …" teaser (under 10 words, voiced) that the next episode answers.
- Use only the cast in topics.md (Hoot, Pip, Moss + side characters). Keep their catchphrases and running gags (the Notebook's page numbers, Pip's "Close enough!").
- Follow the balance rule: don't let it become "doing always beats studying". Alternate who gets the win; sometimes both.
- Structure: screen 0 silent hook (≤8 words) · 6–8 story screens, mid-story turn around screen 4–5 (someone expects X, gets Y) · warm, concrete ending image · final teaser screen. Plain words, 1–2 lines per screen, nobody humiliated.
- JSON: same as animal parables plus `"episode": N` and `"series": "Hoot & Pip"`; `video_queries` real animals only, ceil(screens/2) entries; ID `ep_NNN`, N = highest used + 1 (check `used.json` and existing drafts).
- Save to `formats/series-hoot-pip/drafts/episodes_YYYYMMDD_HHMMSS.json`; append "Ep. N: hook → teaser" to the episode log in topics.md.
- Render with `python3 main.py` (the narrator voice defaults to `thomas` for `ep_` IDs — don't rotate voices in this format). Upload with `python3 upload_queue.py series-hoot-pip <first-date>` (slot 20:30 ET).
- Stock footage can't keep the characters visually identical between episodes; continuity lives in names, text and voice. Don't promise visual consistency.
