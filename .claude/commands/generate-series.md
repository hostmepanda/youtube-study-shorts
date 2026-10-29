# Generate Series Episodes (Hoot & Pip — dialogue format)

Write the next episode scripts for the Hoot & Pip dialogue comedy series. Read `formats/series-hoot-pip/topics.md` first (cast, clarity rule, humor engines, season plan), then `formats/series-hoot-pip/production.md` (prompt and voice rules) and `formats/series-hoot-pip/scripts/season1_eps1-3.md` (the shape of finished scripts).

## Rules

- One episode = one language situation, one humor engine, one native character (a bird, never a human). Rotate languages and engines; never the same language or engine twice in a row.
- **Clarity rule:** every foreign word must be understood inside the dialogue (a character translates it, or the situation shows it). The last two lines must be instantly clear and warm. No in-jokes. Test the script as someone who knows zero of the language.
- Six shots: S1 setup → S2 reaction → S3 correction → S4 payoff → S5 landing → S6 "Say it right" card. 4–6 lines, ≤ ~15 words each. Foreign words in Hoot's and Pip's English lines are fine (English-accented TTS is part of the joke).
- Hoot and Pip keep their roles (Hoot studies, Pip does); sometimes Pip wins, sometimes Hoot errs, rarely a role reversal. Nobody is humiliated.
- Episodes are standalone: no teaser, no arcs, no permanent third character.
- For each episode also write: frame prompts (image-edit), animation prompts (text-to-video), voice/Kokoro assignments, and the card text — following production.md (never the noun "waiter"/"baker" for the bird, simple costumes, calm animation).
- Before writing frame prompts read the "Retro Ep. 1–2" section of production.md (max 2 characters per frame, no spread wings, voice leak cuts, script budget ≤ 30 s of voice) and reuse `formats/series-hoot-pip/tools/`.
- Show the script to the user and wait for OK **before** generating frames or voices (animation costs ~11–15 min of Premiss per clip).
- IDs `ep_NNN` (N = highest used + 1). Append the episode to the season plan table in topics.md.
- Rendering (not `main.py`): follow the pipeline in production.md (wooden-roll `premiss-audio` with pre-baked audio). Use `PATH=/opt/homebrew/opt/ffmpeg-full/bin:$PATH` until ffmpeg-full is linked. Upload only when the user asks: `python3 upload_queue.py series-hoot-pip <first-date>` (slot 20:30 ET).
- The legacy narrator-format episodes in `configs/waiting_upload/` are obsolete; don't generate more of that style and don't upload them unless the user asks.
