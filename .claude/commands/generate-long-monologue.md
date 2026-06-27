# Generate Long Monologue

Write a script for a long-form motivational video (5–8 min) and render it via the wooden-roll pipeline.

---

## Target audience

**Americans learning a foreign language** — Spanish, French, Japanese, etc. They are NOT learning English; English is their native language. They already study but struggle with consistency, fear of speaking, or self-doubt.

Content should speak to the **emotional experience of learning** — the fear of sounding stupid, the plateau, the moment something clicks. Avoid tips/tricks content; this is story and reflection, not a tutorial.

---

## What a long-monologue is

A voiced essay (no on-screen text) over cinematic footage. The narrator tells a true story — a real person who faced a language barrier and pushed through it — and draws a quiet, universal lesson for the listener.

Structure:
1. **Opening** (30–60s) — a quiet, relatable moment the listener has experienced
2. **Story** (3–5 min) — one real person, specific details, no fluff. The language struggle is central
3. **Turn** (30–60s) — what the person understood or did that changed everything
4. **Close** (30–60s) — bring it back to the listener, warm and direct

Tone: calm, intimate, like a podcast. No hype. No "you got this!" energy. Trust the story.

---

## Script rules

- Spoken paragraphs separated by blank lines (each becomes a TTS phrase)
- Plain conversational English — no literary flourishes
- Specific details: names, places, years, exact quotes where possible
- Never state the lesson directly — let the last paragraph carry it
- Length: 700–1000 words (≈ 5–7 min at 0.95 speed)

---

## YouTube metadata

### Tags — base set (use for every long-monologue video)

```yaml
tags:
  - language learning
  - how to learn a language
  - language learning tips
  - become fluent in a language
  - language immersion
  - fear of speaking a new language
  - motivation to learn a language
  - motivational story
  - self improvement
  - personal growth
  - StudyGoTogether
```

Add 2–3 video-specific tags based on the story subject (person's name, country, language, relevant topic).

### Description hashtags

Always end description with: `#languagelearning #motivation #languagelearningtips #StudyGoTogether`

### Hook for thumbnail

3 lines, last line in gold. Should create intrigue without giving away the story.
Example: `"He was in prison." / "He chose to learn" / "their language."`

---

## Config yaml structure

Save script as the `text:` value inside `steps[0]` (premiss-audio step). ID format: `longmono_YYYYMMDD_HHMMSS`.

Key render settings:
- `voice: diana`, `speed: 0.95`, `phraseGap: 0.85`
- `width: 1920`, `height: 1080` (landscape)
- `hideText: true` (no on-screen captions — voice only)
- `musicVolume: 0.10`
- 30–35 `backgroundVideos` queries (cinematic, landscape footage)
- `outroText`: warm sign-off + Subscribe + @StudyGoTogether

The `youtube:` block at the end of the yaml must include `hook:` (3 lines) for auto-thumbnail generation.

---

## Render command

```bash
node /Users/panda/Development/private/youtube-study-shorts/wooden-roll/src/pipeline.js \
  formats/long-monologue/configs/new/<id>.yaml
```

---

## After render

Move yaml to `waiting_upload/` and run `/publish` to schedule at **12:00 ET**.
