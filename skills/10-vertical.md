# Skill 10 — Vertical Videos (YouTube Shorts · Instagram Reels · 9:16)

Read this WHENEVER the brief says: short, Shorts, Reel, Instagram, TikTok, vertical,
9:16, or a duration ≤ 3 minutes aimed at social. Vertical is a different medium, not
a rotated 16:9 — different hook economics, different safe areas, different layout
grammar. Skills 01–09 still apply except where this file overrides them.

## 0. Format decision
- Output: **1080×1920, 30fps** → render the `ExplainerVertical` composition.
- Length targets: sweet spot **45–90s** (YouTube Shorts ≤ 60s guarantees Shorts-shelf
  treatment; Reels up to 90s). Never exceed 3 min in vertical.
- **Author vertical-first**: write dedicated scenes on `VStage` (1080×1920 design
  space from lib/primitives). Only reuse a 16:9 set responsively (`useAspect()`)
  when the user explicitly wants a companion short of an existing video — rotated
  layouts always read worse than vertical-first ones.

## 1. Screenplay differences (overrides skill 02)
- **Cold open — the hook IS the title.** No 10s title card. Beat 1 (≤ 4s narration)
  states the payoff as a challenge: "Tokenization, in ninety seconds." or a puzzle
  line. The first VISUAL frame must already be interesting — viewers swipe in ~2s.
- Structure for 60–90s: **HOOK → 3–5 tight idea beats → TAKEAWAY** (5–7 beats total).
  One idea per video. If the outline has two ideas, that's two shorts.
- Word budget (comprehension-adjusted, skill 02): 60s ≈ **165–180 words**, 90s ≈
  250–270. Beats are 20–45 words. Shorts tolerate slightly hotter pace than
  long-form, but still use `[pause]` after the hook and before the takeaway.
- Sentences shorter than long-form; no throat-clearing ("so", "now let's look at").
- Ending: a single takeaway line + optional soft loop (a closer that re-motivates the
  hook makes replays seamless). "Thanks for watching" is optional in shorts — a
  punchy closer line often lands better.
- Gaps: 0.25–0.3s (tighter than long-form's 0.35s).

## 2. Frame anatomy — vertical zones (overrides skill 09 §1)

```
y     0 ──────────────────────────────
        TOP UI ZONE (0–170)            ← YT/IG overlays live here: keep EMPTY
    170   HEADER (kicker + title)      ← y 170–340, centered
    340 ──────────────────────────────
        CONTENT ZONE (340 → 1560)      ← the hero + supports, stacked
   1560 ──────────────────────────────
        BOTTOM UI ZONE (1560–1920)     ← captions/like/share/audio UI: keep EMPTY
x: 70 side margins → usable width 940 (x: 70 → 1010)
   plus: right-edge column x > 950 is half-covered by the action rail on phones —
   never put text or key visuals in the rightmost ~130px of the content zone.
```
These UI zones are non-negotiable: platforms draw handles, captions, and buttons
there and you cannot opt out.

## 3. Layout grammar (vertical-first)
- **Stack, don't column.** The content zone is a vertical flow of 2–4 blocks
  (hero visual ~500–700px tall + 1–2 support blocks). 3-across grids from 16:9 do
  NOT fit — max 2-across (x = 70, 560 · w = 450).
- The **hero sits at the vertical center of the content zone** (~y 700–1000): that's
  where the eye rests on a phone.
- Full-width cards: x=70, w=940. Two stacked cards: heights ≤ 420 each with 30 gap.
- Balance empty space symmetrically: if content is short, pad top and bottom of the
  content zone EQUALLY — a known past bug left all slack at the bottom, making
  frames look top-heavy (the Instagram-short padding-balance gotcha).
- Diagrams: prefer vertical pipelines (top→down flow with Wires) — reading order on
  phones is downward; left→right multi-node pipelines get cramped.

## 4. Typography (overrides skill 09 §2 — everything is BIGGER)
Phone viewing = full-screen but small physical size. Scale up ~25–35%:

| Role | Size (vertical) |
|---|---|
| Hook/title headline | 92–110 (2–3 short lines) |
| Scene heading | 54–60 |
| Body / card text | 32–38 |
| Labels / mono data | 26–30 |
| Minimum anywhere | **24** |

Width math (skill 09 §3) with usable width 940: a 54px heading fits ~34 SANS chars;
body at 34px in a 940px card ≈ 55 chars/line. Keep lines SHORT — 4–7 words punch
harder in vertical.

## 5. Animation & visuals (skills 03/04/08 apply unchanged, plus:)
- Same hard rules: `useP(dur)` phasing + continuous motion every frame. Shorts have
  even less tolerance for frozen frames.
- Pacing is faster: last reveal lands by p ≈ 0.8; entrances snappier (springs with
  stiffness 130–160); chase highlights hop quicker (`frame / 20`).
- One hero visual per beat — vertical frames can't carry 3 supporting groups.
  Computed visuals (skill 04) matter MORE here: a live number grid or running
  algorithm is the scroll-stopper.
- Cookbook adaptations: orbit hub → vertical ellipse (cos×420, sin×620); charts →
  full-width, taller; recap → max 4–5 items at 34px.

## 6. Mechanics
- Scene set: either a dedicated `<topic>-short` set on `VStage`, or the reusable
  vertical pattern — a generic short grammar (hook / analogy / cards / flow /
  compare / takeaway variants) parameterized per topic, which lets one scene file
  serve many shorts (the proven "mls" pattern: new short = new SEGMENTS + accent
  color, zero new components).
- build.py: identical template; set GAP = 0.3. Render:
  ```bash
  npx remotion render ExplainerVertical ../projects/<slug>/renders/final.mp4 \
    --props=../projects/<slug>/artifacts/edit_decisions.json --concurrency=8
  ```
- QA stills (skill 06): same protocol — stills are 1080×1920; additionally verify
  the two UI zones are empty and nothing important sits in the right-rail strip.
  ~2,700 frames for 90s ≈ 8–10 min render; cheap enough to iterate.
- Companion pair: when the user wants both formats, build 16:9 first, then write a
  SEPARATE tightened screenplay (not a trim) reusing the identity + computed cores
  in vertical-first scenes.
