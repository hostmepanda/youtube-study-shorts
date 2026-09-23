# Insights Journal

A running log of data-driven findings, the conclusions drawn from them, and the concrete skill/pipeline changes made in response. Newest entries at the top.

Purpose: separate a *finding* (what the data showed) from the *decision* (what we changed because of it) so future sessions can trace why a skill or slot looks the way it does — and re-evaluate if the underlying data changes.

---

## 2026-09-23 — Zero comments across the entire channel; low like rate; 8 subscribers at 13k+ views

**Finding:** Pulled channel-level stats (`channels().list`) and aggregated likes/comments/views from `analytics.html` across 254 public videos: **0 comments, on any video, ever.** Total 45 likes on 13,173 views (0.34% like rate overall). By format: parable-animal has the best like rate (0.63%, n=43), then legacy parable (0.63%, n=31), short-motivation the weakest (0.21%, n=132) despite carrying the most views. Channel sits at 8 subscribers with 261 public videos and 13,362 total channel views.

**Conclusion:** Retention (what we've been optimizing) and *engagement* (likes/comments/subs) are separate problems — a video can retain viewers fine and still generate zero interaction. Zero comments across 254 videos strongly suggests the current outro CTA ("Didn't motivate? Drop a message in comments / Subscribe to stay on track / @StudyGoTogether") isn't actually prompting anyone to act — it's generic and not tied to the specific video's content, so there's no concrete thing to reply to. The animal-parable like-rate edge (0.63% vs 0.21% for shorts) hints that humor/absurdity may drive "like" reactions even when it doesn't drive completion — a different lever than the retention structure work.

**Decision / how to apply:** Not yet implemented — flagging for follow-up. Ideas worth testing (see conversation 2026-09-23 for full discussion):
1. Replace the generic outro CTA with a content-specific question (e.g. "What's your version of [the parable's specific mistake]? Say it below") so there's something concrete to reply to.
2. Seed the first comment on new uploads via the API with a genuine question, since a comment section starting at zero rarely self-starts.
3. Lean into the animal-parable humor angle more deliberately (already the best-liked format) as a distinct axis from the retention-structure work — these may need different tuning, not the same playbook.
4. Treat subscriber growth as a separate metric to watch once engagement moves — 8 subs at 13k+ views is expected at this stage and not itself concerning without an engagement funnel already producing comments/likes to convert.

**Update (same day):** implemented idea #1 for animal parables specifically (user's suggestion): `generate-animal-parable.md` now requires a final **voiced comment-question** screen, specific to that parable's animal/device (e.g. "Why do you think the crow couldn't say it?"), which becomes the actual last screen (inherits the big centered treatment, gets read by the TTS since it's a normal screen entry — no pipeline change needed for that part). `config_builder.py`'s `build_parable_config` now gives animal parables a shorter outro ("Answer below" + subscribe) instead of the old generic "Drop a message in comments" line, so the two don't say the same thing back to back. Classic parables are untouched — this is scoped to animal only, as an experiment, per the user's framing ("для животных"). Not yet applied retroactively to already-rendered animal parables (animal_001–072) — only new batches from here get it.

Still open: ideas #2 (seed first comments via API), #3 (lean further into humor for likes), and #4 (subscriber funnel) from above — plus revisiting this once a batch of comment-question videos accumulates data to see if it actually moved the needle.

---

## 2026-09-16 — Line count and mood affect short-motivation retention; voice is an untested lever

**Finding:** Joined short-motivation drafts (lines/mood) to YouTube Analytics retention data for 78 videos with ≥15 views. Line count: 5 lines → 53.2% avg retention (n=33), 4 lines → 45.2% (n=10), 6 lines → 45.1% (n=31), 7 lines → 33.4% (n=3, small). Mood: uplifting → 50.1% (n=22), motivational → 48.8% (n=39), calm → 43.9% (n=17). Separately checked voice: every short rendered so far uses the `elder` Premiss voice at speed 1.0 (inherited from the global `settings.yaml` default meant for parable-classic) — including both the best- and worst-performing shorts — so there's zero variance to test voice as a factor yet.

**Conclusion:** 5 lines is a real sweet spot, not just "shorter is better" (7 lines underperforms, but so does 4). Uplifting/motivational mood modestly outperforms calm. Sample sizes here (10–39 per bucket) are smaller than the ~200-video retention-structure analysis from Sep 8, so treat these as real but softer signals, not settled facts to over-index on. Voice couldn't be evaluated at all — the whole catalog has been a single, untested choice that was never deliberately selected for this format's tone (contemplative parable voice vs. a punchier motivational tone).

**Decision / how to apply:**
- `generate-texts.md`: made 5 lines the explicit default (was "5–7"); weight `mood` toward uplifting/motivational over calm.
- `formats/short-motivation/topics.md`: added a "Length and mood" section with the numbers above, plus a note flagging voice as untested.
- Not yet done: an actual voice experiment (render a batch with a non-`elder` voice and compare retention after it accumulates data). Flagged in both files — pick this up next time a short batch is queued and there's appetite for an experiment.

---

## 2026-09-15 — Viral outlier is algorithm variance, not a repeatable content formula

**Finding:** "Quiet pond. A hedgehog, a duck." (parable-animal, animal_0xx era) hit 827 views — ~3x the next-highest video — with only middling 40.9% retention. Investigated with the YouTube Analytics API:
- Traffic source: 805/827 views (97.4%) came from the **Shorts feed** (`SHORTS` traffic type), not search or channel.
- Daily breakdown: 407 + 301 + 117 = 825 views landed in the **first 3 days** after publish (Aug 25–27). From Aug 28 through Sep 15 (19 days), it got a total of **2** views.
- Engagement: 4 likes, 0 comments on 827 views (~0.5%) — typical of passive feed-swipe traffic, not resonance.

**Conclusion:** This is a one-time algorithmic test-push burst (YouTube trials a Short with a small sample, and expands distribution for a few days if early signals look decent), not sustained organic growth or evidence the specific content ("moon... pancakes?" joke) was exceptional. The video's actual retention was unremarkable for a parable. Raw view counts and views/day averaged over a long window can look like a lasting hit when in fact 99%+ of it happened in a 72-hour window right after publish.

**Decision / how to apply:** Don't chase or try to reverse-engineer a specific "viral" video's content as if it were a formula — it's largely algorithm variance in the initial test-distribution size, not a signal about content-market fit. When evaluating whether something worked, prefer **retention** (intrinsic to the content) over raw views or views/day (dominated by algorithmic distribution luck), and if citing views, check the daily breakdown before treating a total as "sustained" performance. See [[project_retention_analysis_sep2026]] for the retention-side findings that *are* being used to steer content decisions.

---

## 2026-09-08 — Retention analysis: shorts retain ~2x parables

**Finding:** YouTube Analytics (`averageViewPercentage`) across ~200 public videos: short-motivation averages ~48% retention vs ~22–26% for parables (classic/animal). The gap tracked length/structure, not topic quality — background media type (static photo vs Pexels video clip) and music track showed no meaningful independent effect once format was controlled for. Top-performing shorts (reliable samples, 50+ views) consistently combined: (1) a hook that mirrors the viewer's own thought verbatim, (2) a concrete number/timeline, (3) a mid-script reversal of an expected bad outcome, distinct from the closing line.

**Decision:**
- `generate-parables.md`: classic parables shortened 10–13 → 7–9 screens; added a required mid-story turn (~screen 5–6) distinct from the closing reversal; added a Pass 1.5 review step to check for it.
- `generate-animal-parable.md`: same mid-story-turn requirement added on top of its existing 8–9 screen limit.
- `generate-texts.md` / `formats/short-motivation/topics.md`: codified the 3-part pattern above; weighted structures 2/4/8 higher in the rotation.
- Full detail in memory: [[project_retention_analysis_sep2026]].

---

## 2026-09-08 — Minimum daily output floor + fixed upload slots

**Finding/decision (user-driven, not data-driven):** User set a strict requirement: the queue must never drop below 4 videos/day — 2 shorts + 1 classic parable + 1 animal parable — with fixed slots 08:30 / 12:00 / 14:30 / 18:00 ET.

**Bug found while implementing:** `pipeline/youtube_uploader.py`'s default scheduling lumped `parable-classic` and `parable-animal` into one shared "parables" bucket scheduled at a single slot — meaning classic and animal parables alternated by batch (e.g. classic ran Sep 2–8, then animal ran Sep 9–15) instead of both running every day. Fixed: they now route to separate buckets with their own slots (`PARABLES_HOUR`/`ANIMAL_HOUR`). Also caught and fixed: custom ad-hoc upload scripts weren't writing `video_id`/`publish_at` back into archived yamls (see CLAUDE.md "Analytics dashboard" gotcha), which silently dropped those videos from `analytics.html`.

**Full detail:** `CLAUDE.md` → "Minimum daily output" (durable source of truth); memory: [[feedback_minimum_daily_output]].

---

## Template for new entries

```
## YYYY-MM-DD — Short title of the finding

**Finding:** What the data showed. Cite the metric, sample size, and how it was pulled (API, script name).

**Conclusion:** What this means — and what it does NOT mean (call out obvious over-generalizations).

**Decision / how to apply:** What changed as a result — which file, which skill, which memory. If nothing changed (e.g. sample too small to act on), say that explicitly rather than omitting the entry.
```
