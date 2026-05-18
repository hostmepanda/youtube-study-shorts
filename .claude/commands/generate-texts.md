# Generate Texts

Generate a batch of 10 motivational texts for YouTube Shorts on language learning. Save them to `output/texts/`.

## Style rules

- English only
- 5–7 lines per text — each line appears on its own screen
- Tone: direct, honest, no aggression, a drop of warmth and belief in the person
- NOT: fluffy, corporate, preachy, philosophical, childish
- Each line must be short — max 8 words
- Lines can be fragments — punchy is better than complete
- Never end a line with a full stop (.)

## Structures

Pick a structure **randomly** for each text. Use all 10 across a batch of 10.

**1. Problem → Root cause → Fix**
> You're not bad at languages. / You're bad at discomfort. / Get comfortable being uncomfortable.

**2. Observation → Twist → Call to action**
> Everyone wants to be fluent. / Nobody wants to sound stupid first. / That's the only way through.

**3. Countdown / escalation**
> One year ago you started. / Six months ago you promised yourself. / Last week you opened the app. / Today you're still not speaking. / Tomorrow is not the plan.

**4. They vs You contrast**
> Kids don't study before they speak. / They just speak. / You know more than any child. / So what's stopping you?

**5. Myth → Reality → Action**
> You think fluency takes years. / It takes conversations. / Go have one.

**6. Small truth → Bigger truth → Biggest truth**
> Speaking badly is embarrassing. / Staying silent is worse. / Being understood is everything.

**7. Direct address / confession**
> You know exactly what you need to do. / You've known for months. / You're just waiting for a sign. / This is it.

**8. Story fragment**
> She moved to a new country. / Didn't speak the language. / Made every mistake possible. / Now she runs meetings in it. / The mistakes were the method.

**9. Repetition / rhythm**
> Not ready. / Still not ready. / Never ready. / Go anyway.

**10. Question → Silence → Answer**
> What's holding you back? / Really. / It's not the grammar. / It's not the vocabulary. / It's the first word. / Say it.

## What to generate

Write 10 unique texts. For each, assign:
- `mood`: one of `motivational`, `calm`, `uplifting`
- `keywords`: 2–3 words for finding a relevant background photo (concrete nouns/scenes, e.g. "conversation", "open road", "morning light")

## Output format

Save the batch as a single JSON file at:
`output/texts/batch_YYYYMMDD_HHMMSS.json`

Format:
```json
[
  {
    "id": "text_001",
    "lines": ["Line 1", "Line 2", "Line 3"],
    "mood": "motivational",
    "keywords": ["keyword1", "keyword2"]
  }
]
```

After saving, print how many texts were written and the file path.
