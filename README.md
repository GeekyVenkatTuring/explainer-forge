# Explainer Video Studio

A Remotion pipeline and skill set for **coding agents** (and humans) to produce
narrated, animated explainer videos that stay in lockstep with the voiceover —
not narrated slides.

Default output is **16:9, 1080p, 30 fps**, no music, no captions, Nova TTS, unless
the brief says otherwise. Vertical (9:16 Shorts/Reels) is a first-class path with
its own skill.

This GitHub repository is source only. Renders, TTS audio, `node_modules`, and
QA stills are gitignored.

**https://github.com/GeekyVenkatTuring/explainer-video-studio**

## What it is

Each video is three things that must stay consistent:

1. **A scene set** — React/Remotion components in `composer/src/scenes/`, built on
   the shared engine in `composer/src/lib/primitives.tsx`.
2. **A screenplay** — beats in `projects/<slug>/build.py`: variant id, scene props,
   and spoken narration.
3. **A props JSON** — `artifacts/edit_decisions.json` produced by `build.py`. Every
   cut carries `dur` (beat length in seconds) so animation is phased as fractions of
   the *actual* narration, not hardcoded frame numbers.

The player (`composer/src/Explainer.tsx`) is a thin timeline: it reads `cuts` +
narration audio, routes `type` (`<prefix>_<variant>`) through a one-line
`REGISTRY`, and plays sequences. Adding a video is one scene file + one registry
line + one `projects/<slug>/` folder.

The quality bar is not taste. It is the two gold-reference implementations in
`reference/` (fine-tuning **FTScenes**, computer vision **CVScenes** /
**CVScenesA** / **CVShared**). Agents are required to read the skills before
doing the corresponding step. The contract is `AGENTS.md` / `CLAUDE.md`.

## Why it exists

`REVIEW.md` audits ten earlier scene sets against those gold videos. The earlier
sets looked like slideshows with a voiceover. The defects, and the mechanisms this
repo encodes:

| Defect | What happened | Mechanism here |
|---|---|---|
| **Freeze** | Animation keyed to fixed frames (`t(40,56)`). At 30 fps all motion finished in ~2s; the rest of a 20–40s beat sat still. | Every scene takes `dur` from cut props and phases reveals with `useP(dur)` fractions. |
| **Nothing breathes** | Entrance-only fades, then a still frame. | Always-on motion (Flow, Wire dash-march, ScanBeam, sine glow, chase, orbit) plus a scene-progress bar. |
| **Illustrated, not computed** | Static cards *about* an algorithm. | When the topic is a process, **run it** (precompute deterministic states, index by phase). |
| **No visual QA** | Straight to a full MP4. Layout collisions, wrong metaphors, overlapping type shipped unseen. | Mid-animation still of **every** scene, reviewed as images, then re-checked. |
| **No length calibration** | “20 minutes” meant whatever the script happened to be. | Word budget from target minutes × measured TTS rate; iterate until ±5%. |
| **Non-determinism / slow filters** | `Math.random()` flickered across workers; CSS `blur()` made renders take hours. | `rnd(i, j, seed)` from primitives; no CSS `filter` / `backdrop-filter`. |

Two shipped bugs the contract now forbids: a 96s title held static for ~46s, and
reveals lagging narration by up to 30s because phases were spread evenly to
“fill the beat” instead of tracking when the subject is spoken.

## Architecture

```
brief
  → beat list + visual identity
  → scene set (composer/src/scenes/<X>Scenes.tsx)
  → screenplay + TTS (projects/<slug>/build.py)
  → QA stills (look at every scene)
  → final Remotion render
  → ffprobe + spot-check frames
  → deliver
```

**Composer** (`composer/`) is a standalone Remotion 4 app (React 18, TypeScript).
Run `npx remotion` from this directory only. Scenes author at 1920×1080 on
`Stage` (or 1080×1920 on `VStage` for vertical). The scene engine exports
`useP`, `usePop`, `Flow`, `Wire`, `Counter`, `Type`, `Card`, `Head`/`Foot`/`Kicker`,
`Bg`, `PixGrid`, `Brackets`, `ScanBeam`, `rnd`, `makeTheme`, and vertical helpers.

**Projects** (`projects/<slug>/`) own the screenplay and generated media:

```
projects/<slug>/
├── build.py                 # SEGMENTS + TTS + edit_decisions.json
├── assets/                  # per-segment WAVs (idempotent cache)  [not in git]
├── artifacts/               # edit_decisions.json (+ logs, thumbs)
├── qa-stills/               # mid-beat PNGs                         [not in git]
└── renders/                 # final.mp4                             [not in git]
```

Narration WAVs are also staged under `composer/public/<prefix>/` because Remotion
loads from `public/` only (never `file://` absolute paths). That folder is
gitignored.

**Skills** (`skills/01`–`13`) are the operating manual. If you have not read a
skill, do not perform its step. Cookbook recipes (`08`) and frame-design math
(`09`) exist so agents adapt proven layouts instead of inventing overlapping
frames while composing blind.

**Reference** (`reference/`) is the gold scene code copied verbatim. When a scene
feels thin, match those files—not a card grid.

## Hard rules (violations = defects)

1. **Reveals track narration.** `useP(dur)` only. `interpolate(frame, [40, 56], …)`
   for a reveal is a defect. Narration is usually front-loaded (names items, then
   elaborates), so reveals are too. Do not delay reveals to p≈0.85 to “fill time.”
   Keep the back half alive with continuous motion and a progress bar. Cap a
   single-visual beat at ~75s; split long intros.
2. **Continuous motion in every frame.** 1–3 always-on elements that are clearly
   visible, plus an edge progress bar over `p(0,1)`.
3. **Compute the real thing** when the topic is an algorithm or numeric process.
4. **Deterministic rendering.** `rnd()` from primitives; no CSS filters.
5. **QA stills before the final render.** Never ship an unseen scene.
6. **Calibrated length.** Budget from the screenplay skill; after TTS, print the
   real total and iterate (delete only changed WAVs) until within ~5%.
7. **One visual identity per video:** theme + 2–4 semantic accent colors + one
   recurring motif. Colors mean things.
8. **Defaults:** 16:9 1080p 30fps, no music, no captions, Nova, ~0.35–0.5s gaps —
   unless the brief overrides.

Honesty: report what QA caught, what you fixed, and what is still weak. Do not
hide a missed duration target or a thin scene.

## Pipeline (summary)

Detail lives in `skills/01-pipeline.md`. Order is mandatory.

0. **Brief** — topic, duration (±5% is real), aspect, voice, captions/music.
   Short / Reel / TikTok / Instagram / vertical / 9:16 → read skill 10 *before*
   designing. Telugu or Indic script → skill 11. Markets / IPOs / investing →
   skill 12 (India) or 13 (US/China) *before* any web research.
1. **Paper design** — 12–35 beats; videos ≥ 8 min get numbered part dividers.
   Identity: theme, semantic accents, motif. One line per beat: what is on
   screen, what *develops*, what never stops moving. “A card with text” is not
   a concept.
2. **Scene set** — copy `DemoScenes.tsx`; start from cookbook recipes; compose
   with skill 09 zones and text-width math; register the prefix in `Explainer.tsx`;
   `npx tsc --noEmit` clean inside `composer/`.
3. **Screenplay + TTS** — copy `projects/_template/`; fill `SEGMENTS`; run
   `python3 build.py`; iterate duration.
4. **QA stills** — one mid-animation frame per variant; look; fix; re-render
   the fixed stills (skill 06).
5. **Final render** from `composer/` (skill 07).
6. **Verify** — ffprobe; extract 2 frames from the real MP4 and look at them;
   copy to `~/Downloads/generated_videos/`; report honestly.

## Skills index

Read before the matching step. Do not skim the contract and skip these.

| Skill | File | When |
|---|---|---|
| 01 Pipeline | `skills/01-pipeline.md` | First. End-to-end order. |
| 02 Screenplay | `skills/02-screenplay.md` | Beats, word budget, `[pause]`, narration↔scene contract. Educational pace is ~150–165 words per video-minute (Nova is ~212 wpm raw; slowdown + silence bring it down). |
| 03 Animation | `skills/03-animation.md` | `useP(dur)`, continuous motion, progress bar. |
| 04 Visuals | `skills/04-visuals.md` | Identity, computed visuals, what not to draw. |
| 05 TTS | `skills/05-tts.md` | Voicebox / Kokoro, profiles, idempotent WAV cache. |
| 06 QA | `skills/06-qa.md` | Still protocol and bug catalog. **Before first render.** |
| 07 Render | `skills/07-render.md` | Remotion commands, concurrency, gotchas. |
| 08 Cookbook | `skills/08-cookbook.md` | Copy-paste archetypes: divider, chart, orbit hub, chat, gauge, recap, title, … |
| 09 Frame design | `skills/09-frame-design.md` | Head/content/foot zones, type hierarchy, text-width math, title/end-card anatomy. |
| 10 Vertical | `skills/10-vertical.md` | 9:16. Overrides parts of 02 and 09. `VStage`, `ExplainerVertical`. |
| 11 Indic / Telugu | `skills/11-indic-telugu.md` | Letter-spacing, caption band, fonts, edge-tts notes. |
| 12 Market research | `skills/12-market-research.md` | India markets/IPOs. Exact figures, triangulation, disclaimer. |
| 13 Intl IPO | `skills/13-intl-ipo.md` | US + China IPO education; do not reuse India sources or the `sm` set. |

## Repository layout

```
AGENTS.md / CLAUDE.md     agent contract (hard rules + reading order)
REVIEW.md                 why earlier videos failed vs gold
README.md                 this file
skills/                   pipeline manual (01–13)
composer/                 Remotion app
  src/lib/primitives.tsx  scene engine
  src/scenes/             one file per video (DemoScenes.tsx is the annotated starter)
  src/Explainer.tsx       timeline + REGISTRY
  public/                 staged narration (gitignored)
projects/_template/       build.py template
projects/<slug>/          one folder per video
reference/                gold FT + CV scene sets
videos/                   small extra experiments (not the main pipeline)
```

Scene-set prefixes already registered include `demo`, `cv`, `llm`, and many
production sets (`sm`, `eq`, `sol`, `lag`, …). Keep those folder names and
prefixes; do not rename them to match this document’s product name.

## What is not in git

Working trees on a production machine are large (renders + WAV + `node_modules`).
This remote tracks source. Ignored:

- `node_modules/`
- `*.mp4`, `renders/`
- `qa-stills/`
- `__pycache__/`
- audio (`*.wav`, `*.mp3`, …) and `composer/public/`

Clone, `npm install` in `composer/`, run TTS locally, then render. Do not commit
masters or Voicebox output.

## Requirements

- **Node ≥ 18** and npm (install inside `composer/`)
- **Python 3** (stdlib only for the template `build.py`)
- **ffmpeg / ffprobe**
- **Voicebox.app** open for default TTS (`http://127.0.0.1:17493`). Swap
  `gen_one()` in `build.py` for another engine that writes WAVs if needed.
- A coding agent (or a human) that will follow the skills in order

## Quickstart

```bash
# Composer dependencies (once per clone)
cd composer && npm install && cd ..

# Demo video end-to-end (Voicebox.app must be open)
cp -r projects/_template projects/demo
cd projects/demo && python3 build.py && cd ../..

cd composer
npx remotion render Explainer ../projects/demo/renders/final.mp4 \
  --props=../projects/demo/artifacts/edit_decisions.json --concurrency=8
```

Studio preview: `cd composer && npm run studio`.

A real video: follow `skills/01-pipeline.md` step by step. Do not skip QA stills.

## Word budget (Nova, after pace levers)

Use skill 02 as source of truth. Rough targets:

| Target | Words | Beats |
|---|---|---|
| ~60s short | ~165 | 5–7 |
| 5 min | ~825 | 12–15 |
| 10 min | ~1,650 | 20–26 |
| 20 min | ~3,300 | 30–36 |

A typical content beat is 70–120 words (25–45s including pauses). After `build.py`,
compare printed duration to the brief and iterate.

## License and status

Personal production pipeline published as source. No warranty that a clone will
match a previously delivered MP4 without regenerating audio and renders.
