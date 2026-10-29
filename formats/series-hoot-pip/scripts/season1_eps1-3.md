# Season 1, episodes 1–3 — scripts, frames, animation prompts

Speaker tags: **H** Hoot (felix, Premiss) · **P** Pip (bruno, Premiss) · native voices Kokoro. Foreign words are glossed inside the dialogue. Hero positions: Hoot left, Pip right.

---

## Ep. 1 — Spanish — "Pip told the waiter a secret." (engine 1: Pip wins by confidence)

Rendered test: `~/qwen-edit-lab/spain/spain_v4.mp4`. Setting: Spanish plaza café (white wall, orange awning, wicker chairs, marble table). Native: sparrow waiter (apron + bow tie), `em_alex`.

| Shot | Line | Visual |
|---|---|---|
| S1 | P: "Excuse me, waiter! Estoy, embarazado!" | Pip and Hoot at the table, slow zoom in |
| S2 | W: "Congratulations! When is the baby due?" | sparrow waiter, medium wing flap, apron kept |
| S3 | H: "Pip, embarazado means pregnant. You wanted, avergonzado. Embarrassed." | Hoot explains: beak + one wing gesture |
| S4 | P: "Too late. He already brought me a cake." | Pip turns head, cake on the plate |
| S5 | W: "On the house. For the baby." | candle on the cake, calm |
| S6 | card: Embarazado = pregnant / Avergonzado = embarrassed | zoom out, Kokoro es voice reads both words |

Why it works: Pip's mistake is rewarded, both foreign words are translated inside the dialogue, the last two lines are clear and warm.

---

## Ep. 2 — French — "Hoot pulled the baker's leg." (engine 2: Hoot errs by literal translation)

Setting: Paris-style bakery terrace: stone wall, green awning, bistro table, baguettes in a basket. Native: a sparrow baker with a small white apron (no hat — hats get lost in animation). Voice `ff_siwis`.

Idea: the baker jokes in English that the baguette is "made from moonlight". Hoot wants to say "You're pulling my leg!" and translates word for word.

| Shot | Line | Visual |
|---|---|---|
| S1 | Baker: "This baguette? Made from moonlight. Very rare." | baker behind the counter, apron kept, one baguette on a board |
| S2 | H: "You're pulling my leg! Vous tirez, ma jambe!" | Hoot, outraged but proud, wing raised |
| S3 | Baker (gently pulls Hoot's leg with a wing, puzzled): "Ma jambe? Your leg? Like this?" | close shot of baker's wing on Hoot's leg, Pip watching |
| S4 | H: "No! It's an expression! In English, it means joking." | Hoot flustered |
| S5 | Baker: "Ah! In French, we say: vous me faites marcher. You make me walk." Pip, walking in a circle: "Like this? Free baguette?" Baker: "Free baguette. Walk." | Pip walking circles around the table, baguette on the table |
| S6 | card: Vous me faites marcher = you're pulling my leg / Je tire ta jambe = nobody understands you | zoom out, Kokoro French reads the first phrase |

Clarity check: "Vous tirez ma jambe" is glossed by the baker's reaction and Hoot's explanation; "faites marcher" is glossed as "you make me walk". The last two lines are one idea (Pip walks, gets a baguette), instantly clear.

Frame prompts:
- S1: "Keep the owl and the pigeon exactly as in the references. A French bakery terrace with a stone wall, a green awning, a round bistro table and a basket of baguettes. A sparrow wearing a tiny white apron stands behind the counter holding one baguette on a wooden board. There are no humans anywhere in the image, no human body parts, the only living creatures are birds. Vertical 9:16."
- S3: same set, tight on the sparrow baker gently holding the owl's leg with one wing, the pigeon watching, apron kept.
- S5: pigeon in motion on the cobblestones next to the table, baguette on the table.

Animation prompts: S2 "The owl raises one wing proudly and opens its beak as if declaring something. The camera stays still." S3 "The sparrow gently pulls the owl's leg, the owl looks down surprised. Keep the white apron. The camera stays still." S5 "The pigeon walks in a small circle around the table, head bobbing. The camera stays still."

---

## Ep. 3 — Italian — "Hoot asked the way. In a textbook." (engine 4: textbook vs real life)

Setting: Italian train station platform: yellow tiled wall, departure board, bench, warm evening light. Native: a sparrow station clerk in a small blue vest (vest, no hat). Voice `im_nicola`.

| Shot | Line | Visual |
|---|---|---|
| S1 | H, slowly: "Scusi. Dov'è il treno per Roma?" | Hoot at the clerk's window, hopeful |
| S2 | Clerk, very fast: "Binario nove, ma è appena partito, il prossimo tra un'ora, destra poi sinistra poi giù!" | clerk gesturing with both wings; fast audio ~200 wpm |
| S3 | H: "He said so many words. I caught one: treno. Train." P: "We asked about the train." | Hoot dazed, Pip shrugging |
| S4 | Clerk, slow now: "Là. Quel treno. Corri!" H: "Là means there. Corri means run!" | clerk pointing, train on the platform behind |
| S5 | H: "I should have asked: piano, per favore. Slowly, please." | doors closing behind them, both birds laughing, nobody hurt |
| S6 | card: Dov'è = where is / Corri = run / Piano, per favore = slowly, please | zoom out, Kokoro Italian |

Clarity check: the fast line is intentionally unintelligible and the joke is that Hoot caught only "treno" (he says so). "Là" and "Corri" are glossed. Learning payoff: the card teaches "Piano, per favore", the phrase Hoot should have used.

Frame prompts: S1/S4 Italian station platform, yellow tiles, departure board, a small train in the background; a sparrow clerk in a small blue vest, no humans.

Animation: clerk "gestures quickly with both wings and nods while speaking. Keep the blue vest. The camera stays still." Hoot "listens with wide eyes, tilting his head slowly, then blinks."

---

## Checklist before voicing any episode

1. Every foreign word translated by a character inside the dialogue.
2. Last two lines instantly clear, warm, no one humiliated.
3. Native character costume simple (apron, vest, bow tie); no hats or glasses.
4. Premiss queue free before starting animations (one job at a time, ~11–15 min each).
5. Send the user the script first, voice only after OK.

---

# Long-format test (35–40 s, 8 shots) — Ep. 2 and Ep. 3

Test of the longer format: one escalation beat before the correction, and a "say it right" practice scene before the card. Compare retention against Ep. 1 (6 shots, 25 s). Extra cost: 2 more Premiss clips per episode (~25–30 min).

## Ep. 2 (long) — French — "Hoot pulled the baker's leg."

| Shot | Line | Visual |
|---|---|---|
| S1 | Baker: "This baguette? Made from moonlight. Very rare." | baker behind the counter, apron, baguette on a board |
| S2 | H: "You're pulling my leg! Vous tirez, ma jambe!" | Hoot, proud, wing raised slightly |
| S3 | Baker: "Ma jambe? Your leg? Like this?" (gently tugs Hoot's leg) | close shot, wing on Hoot's leg |
| S4 | P: "Two legs. Double joke!" (tugs Hoot's other leg) H: "Stop! It's an expression! It means you're joking!" | Pip and the baker both holding Hoot's legs, Hoot flustered |
| S5 | Baker: "Ah! In French, we say: vous me faites marcher. You make me walk." | baker explains, one wing raised |
| S6 | H, slowly: "Vous me faites marcher." P: "Voo may fet marshay!" Baker: "Close enough!" | three-shot, Pip proud |
| S7 | P (walking in a circle with a baguette): "Is this walking? Free baguette?" Baker: "Free baguette. Walk." | Pip circling the table, baguette |
| S8 | card: Vous me faites marcher = you're pulling my leg | zoom out, Kokoro French |

Clarity: "ma jambe" is glossed by the baker ("Your leg?"), "vous me faites marcher" glossed immediately ("You make me walk"). Pip's catchphrase "Close enough!" comes from the native — a small reversal.

## Ep. 3 (long) — Italian — "Hoot asked the way. In a textbook."

| Shot | Line | Visual |
|---|---|---|
| S1 | H, slowly: "Scusi. Dov'è il treno per Roma?" (Excuse me, where is the train to Rome?) | Hoot at the clerk's window |
| S2 | Clerk, very fast: "Binario nove, ma è appena partito, il prossimo tra un'ora, destra poi sinistra poi giù!" | clerk gesturing with both wings |
| S3 | H: "He said so many words. I caught one: treno. Train." | Hoot dazed |
| S4 | P: "Sì, sì, grazie!" (Yes, yes, thanks!) H: "Pip, you said yes to everything!" Clerk, even faster, with a station announcement over it | Pip nodding, clerk waving more, Hoot overwhelmed |
| S5 | H: "Piano, per favore. Slowly, please." Clerk, slowly: "Ah. Là. Quel treno. Corri!" | Hoot calm for the first time, clerk pointing at the train |
| S6 | H: "Là means there. Corri means run!" | both birds run along the platform |
| S7 | P (on the train, doors closing): "Next time, say piano first." H: "Piano, per favore. I will." | both on the train, doors closing, laughing |
| S8 | card: Dov'è = where is / Corri = run / Piano, per favore = slowly, please | zoom out, Kokoro Italian |

Clarity: every foreign word is glossed inline ("Sì" is glossed by Hoot's reaction, "treno" by Hoot, "piano per favore" by Hoot himself, "là"/"corri" by Hoot). The last two lines state the lesson and land warm.
