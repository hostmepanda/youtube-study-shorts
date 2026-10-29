# Hoot & Pip — production guide (dialogue format)

Everything here was learned while building the Spain test episode (Oct 2026). Working dir for experiments: `~/qwen-edit-lab/` (outside the repo); renderer: `~/Development/private/wooden-roll`. Never print or commit the Premiss API key (`.env`, and the wooden-roll yamls contain it in plain text — gitignored).

## Pipeline per episode

1. **Script** (`scripts/ep_NNN.md`): 6 shots, lines, speaker, language, gloss.
2. **Frames** — Premiss `image-edit` (Qwen-Image-Edit-2511) from reference images `owl.png`, `pigeon.png` (+ `sparrow.png` or a new native character ref). 1–3 refs per call, one frame per shot, same seed across the episode.
3. **Animation** — Premiss `text-to-video` (Wan2.2 5B), image → 4 s clip, 704x1280, ~11–15 min per clip, one job at a time. Animate every shot except the zoom shots (S1, S6 in Spain).
4. **Voices** — Premiss TTS for Hoot (`felix`) and Pip (`bruno`), local Kokoro for native characters and the foreign "Say it right" card. Stitch per line, level to −20 LUFS, 0.45 s gaps.
5. **Background bake** — one `bg_<tag>.mp4` from the clips, cuts at the midpoints of the gaps between phrases, 0.5 s crossfades; zoom shots via OpenCV Ken Burns.
6. **Render** via wooden-roll `premiss-audio` with `skipIfExists` (pre-baked `full_audio.wav` + `timeline.json`); per-speaker subtitle colors with ASS tags (Pip blue `{\c&HFFB85B&}`, Hoot gold `{\c&H32C8FF&}`, others white).
7. Output → `output/videos/ep_NNN.mp4` and a yaml in `configs/new/` with the `youtube:` block, same as the other formats.

## Frame prompts (image-edit)

Always: "Keep the owl and the pigeon exactly as in the reference images." + scene + "There are no humans anywhere in the image, no human body parts, the only living creatures are birds." + "Vertical 9:16."

- **Never write the noun "waiter" / "baker" / "clerk" for a bird** — the model draws a human. Write "a sparrow wearing a tiny white waiter apron and a small black bow tie". Costume = the role. Name props explicitly ("a baguette on a wooden board", "a cake with a strawberry on a plate").
- One scene style per episode (Spanish plaza café: white wall, orange awning, wicker chairs, marble table). Keep the light consistent.
- Generate every shot with the same seed, compose the pair in the same relative positions (Hoot left, Pip right) so cuts feel continuous.
- Check each frame for: no human, correct species, costume present, both heroes recognizable. Regenerate with another seed when they fail.

## Animation prompts (text-to-video)

- Start from the frame. Prompt = one simple action + "The camera stays still." Add "Keep the <costume items>." for costumed characters.
- **Calm prompts keep identity; strong motion strips accessories.** Costumed bird + big motion → the apron and bow tie vanish after ~1 s. Medium motion with "keep the apron" works.
- Clothing-free bird + head turn / nod = safe; one wing gesture = ok but the wing blurs at its peak → say "slowly raises one wing a little and lowers it again, the wing stays solid".
- Wing flaps at full speed give a translucent, ghost-like wing. Prefer head, beak, blink, small hops.
- Clips are 4 s and the model has no lip-sync: open-beak motion is just generic. Don't promise exact matching; hold the shot for the line and let it be.
- If a shot fails: re-roll with another seed or simplify the prompt; do not chase it with stronger motion.

## Voices

- Premiss TTS = F5-TTS voice cloning with **no language parameter**: foreign words are read with English phonetics, which is acceptable and funny when Hoot or Pip says them ("avergonzado" in an English accent).
- Hoot = `felix`, speed 0.85 with commas. Pip = `bruno`, speed 0.85. (Never use `diana` or `violet` in this repo.)
- Short phrases (1–3 words) get swallowed by F5: lengthen ("Excuse me, waiter! Estoy, embarazado!"), use commas to force pauses. Each phrase gets leading silence → trim with threshold 0.002 + 0.12 s pad (not stricter, or soft onsets are cut).
- Native characters: Kokoro-82M (MLX, local `wooden-roll/.venv`) preset voices per language: Spanish `em_alex`/`ef_dora`, French `ff_siwis`, Italian `im_nicola`/`if_sara`, others in the HF cache (`jf_*`, `zf_*`, …). `KokoroPipeline(lang_code=...)` per language ('e' es, 'f' fr, 'i' it, 'j' ja, 'z' zh, 'a' US, 'b' UK). English lines of a native character are read with the native voice → accent for free.
- Level every line to −20 LUFS (ffmpeg `ebur128`), not RMS. Pip came out −12, waiter −28, Hoot −18 before leveling.
- Mandarin/Thai/Vietnamese (tonal): don't until TTS can do tones.

## Subtitle / card rules

- Hook font 150, last-line font 95, subtitles per speaker color; Pip's blue is low-contrast on light backgrounds → keep a thick outline or use a brighter blue.
- Outro text goes in the lower half over the hero: `{\an5\pos(540,1450)}…` (PlayRes 1080x1920). No dark plate behind it.
- The "Say it right" card: `Phrase = meaning`, one per line, correct form first.

## System notes

- Homebrew ffmpeg 9.0.2_1 has no libass → all renders fail with "Unknown filter 'ass'". Use `ffmpeg-full`: either `brew unlink ffmpeg && brew link --force ffmpeg-full`, or prefix `PATH=/opt/homebrew/opt/ffmpeg-full/bin:$PATH`.
- Background shells: `python3` may be an alias, use `/opt/homebrew/opt/python@3.11/bin/python3.11`.
- Background-launcher "completed" notifications are unreliable; check logs/`pgrep` for the real state.

## Retro Ep. 1–2 (Oct 2026): what cost us iterations, and the rule that prevents it

Ep. 2 took ~5 rounds of frames, 4 rounds of voices, 1 re-animation. Every item below was a wasted round. Follow the rules and an episode should take 1 frame round, 1 voice round, 0 re-animations.

### Frames
- **Max 2 characters per image-edit call (2 refs).** With 3 refs the model swaps species, grows extra owls, merges two pigeons into one body, moves the apron to the wrong bird. Plan shots as pairs: owl+native, owl+pigeon, pigeon+native. A 3-bird shot is allowed only if calm, and must be checked bird by bird. A speaker may be off-screen (the native's line over a shot of Hoot and Pip).
- **No spread or raised wings in the frame.** Wings spread in a still turn into ghost / extra / foreign wings once animated, and they were the reason S7 was redone. Ask for "wings folded against its body, each bird has exactly two wings". If a ghost wing remains, a targeted edit works: one ref (the frame itself) + "remove the extra transparent wing ... keep everything else exactly the same", 3 seeds.
- **Birds "stand in the air"** when the counter is a small box in the corner. Use "a wide wooden counter that fills the bottom of the frame, all feet touch the wood, nobody is flying or jumping".
- **Backdrop = recognizable landmark:** "exactly one Eiffel Tower" (otherwise 2–3 towers). Check the corners for a human silhouette in the background and reject those seeds.
- Always generate 3–4 seeds and **look at them yourself before showing the user** (one grid was sent unseen and all 3 variants were broken).
- Native bird must differ from the heroes and be recognizable for the country (France: Gallic rooster in a white apron). Italy: peacock in a blue vest (proposal, not confirmed).
- Pip in blue on a light backdrop is low-contrast for subtitles; keep the outline thick.

### Animation
- Calm prompts worked first try for 5 of 6 clips ("speaks calmly, beak slightly open, keeps the apron, the camera stays still"). When a clip fails, fix the **frame**, not the prompt.
- One job at a time, ~11–15 min per clip: queue all clips in ONE background script (`tools/anim.py`, skips existing files) and start voices at the same time.
- Clips are 4 s, shots are 5–7 s: extend by ping-pong (forward + reversed) instead of freezing (`tools/build2.py`).
- Check clips by frames at 0.3 / 1.5 / 3.7 s in a contact sheet before showing; look for the head turning away (S4) and extra limbs.

### Voices
- **Premiss voices leak the tail of their reference recording at the start of a line.** felix: "…hint of derision" (≈0.8–1.1 s); bruno leaks at speed 0.7 ("of the two parties"). Always transcribe each Premiss line with whisper.cpp word timestamps and cut just before the first intended word (`CUT` dict in `tools/stitch.py`, cut ≈0.05 s earlier than the word start; if "-sion" survives, cut later). Re-check after every re-generation: the junk length changes with text and speed.
  - Setup: `whisper-cli -m ggml-base.en.bin -f x.wav -ml 1 -sow -oj -of out` (model: huggingface.co/ggerganov/whisper.cpp `ggml-base.en.bin`, 148 MB; delete after use).
- Foreign words in the F5 voices come out as garbage. Respell phonetically in the TTS text ("voo tee-ray, mah zhahmb") and keep the correct spelling in the subtitles; the native bird says the real phrase correctly later.
- Speeds: Hoot felix 0.8, Pip bruno 0.8 (0.7 leaks, and Pip still sounds fast on short lines; give him commas).
- **Kokoro has only ONE French voice and it is female (`ff_siwis`)**. For a male native use a male voice (`am_michael`) and render per segment: English segments with lang `a`, foreign phrases with the foreign lang code (`f`, `e`, `i`…). Reading English through the foreign phonemizer is garbled. Native voice has some background noise; acceptable.
- **The card:** the voice reads the foreign phrase AND the English meaning ("It means, you're pulling my leg"), then the text stays 2 s after the voice (`HOLD` in `tools/stitch.py`), otherwise the text vanishes before it can be read.
- Gap between lines 0.6 s; level −20 LUFS; trim threshold 0.002 pad 0.12 (as before).

### Length budget
- Ep. 2 came out at 50 s (voice 40 s + 5 s outro + hook), the target was 35–40 s. Budget: ≤ 30 s of voice, no line over ~3.5 s (the longest native line was 7 s), card ≤ 5 s with hold. Cut words in the script, not speed.

### Process
- Script → user OK → frames (pairs, 3–4 seeds, self-check) → lineup to user → OK → animation + voices in parallel → `tools/` scripts → rough cut → user OK → metadata → upload.
- Send previews as CRF 24 copies: SendUserFile limit is 30 MiB (a 35 MiB render was refused).
- Lab dir `~/qwen-edit-lab/epN/` is scratch: after upload keep only finals (`final/`, `anim/`, `vo/`, scripts, the master mp4) and delete variants, grids, seg/bg files and `wooden-roll/output/audio/<tag>`.

### Reusable scripts: `formats/series-hoot-pip/tools/`
`lines.py` (script lines: shot, voice, speed, TTS text, subtitle text) → `vo_premiss.py` (Hoot/Pip) + `vo_kokoro.py` (native bird, per-language segments) → `stitch.py` (trim, CUT, level, hold) → `build2.py <tag>` (background bake with ping-pong + xfades, ASS colors, wooden-roll yaml) → `node src/pipeline.js <yaml>` in wooden-roll with ffmpeg-full. `anim.py` and `frames_j.py` are the animation / image-edit templates. They use paths under `~/qwen-edit-lab/ep2/`; copy and adapt per episode.
