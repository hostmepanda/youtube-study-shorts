# Experiment: Language-Specific Targeting

**Started:** 2026-07-11  
**Status:** running

## Hypothesis

Naming a specific language (Spanish, French, Japanese) in the hook drives higher views/day than a generic equivalent — because YouTube's algorithm surfaces the video to audiences already searching for that language, and the emotional recognition is stronger ("that's me").

## Evidence that prompted this

Spanish experiment (Jul 9–10, batch `batch_20260709_spanish.json`):
- `text_014` "She was terrified to speak Spanish" → **222 vpd** (day 1)
- `text_015` "Everyone wants to speak Spanish fluently" → 48 vpd
- Generic equivalent `text_015`-style "Everyone wants to speak fluently" (Jun 12) → 0.4 vpd

That's a 50–500× difference. Could be algorithm timing (July vs May), could be the language specificity, could be the hook structure.

## What we're testing

Two hooks × three languages, compared against existing Spanish baselines:

| Hook | Spanish (baseline) | French | Japanese |
|------|--------------------|--------|----------|
| "Terrified → now thinks in it" | text_014 · 222 vpd | text_016 | text_017 |
| "Wrong order, still understood" | text_018 | text_019 | text_020 |
| "Everyone wants fluency → go badly" | text_015 · 48 vpd | text_021 | — |

## What would confirm the hypothesis

- French and Japanese hooks land at comparable vpd to Spanish equivalents (within 2×)
- All language-specific texts outperform generic equivalents published in the same week

## What would refute it

- French/Japanese significantly underperform Spanish (→ Spanish audience is just bigger on this channel, not a language-targeting effect)
- Generic texts published in July perform as well (→ it's the algorithm timing, not the language name)

## Check-in date

**2026-07-25** — 2 weeks post-publish, enough data on all 6 videos.

## Results

*(fill in after check-in)*
