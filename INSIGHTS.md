# Insights Journal

A running log of data-driven findings, the conclusions drawn from them, and the concrete skill/pipeline changes made in response. Newest entries at the top.

Purpose: separate a *finding* (what the data showed) from the *decision* (what we changed because of it) so future sessions can trace why a skill or slot looks the way it does — and re-evaluate if the underlying data changes.

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
