# Explainer Forge

A self-contained pipeline for producing narrated, animated explainer videos at the
quality bar of the "fine-tuning LLMs" and "computer vision" gold-reference videos —
designed so any capable coding model (Opus, Sonnet, …) lands at that bar by
following the embedded skills.

**Why this exists:** `REVIEW.md` — an audit of ten earlier scene sets vs the two
gold ones. Short version: earlier videos keyed animation to fixed frame numbers
(everything froze ~2s into each 30s scene), had no always-on motion, illustrated
instead of computed, skipped visual QA, and never calibrated narration length.
This repo turns each fix into a mechanism + a skill.

## Layout
```
CLAUDE.md                 agent contract (hard rules + reading order)
REVIEW.md                 the gap analysis with evidence
skills/01..10             pipeline · screenplay · animation · visuals · TTS · QA · render · cookbook · frame design · vertical (Shorts/Reels)
composer/                 standalone Remotion app (npm installed, tsc-clean)
  src/lib/primitives.tsx  the scene engine (useP, Flow, Wire, PixGrid, …)
  src/scenes/DemoScenes.tsx  annotated reference scene set (demo_*)
  src/Explainer.tsx       timeline player + one-line scene-set registry
projects/_template/       build.py template (screenplay → Voicebox TTS → props JSON)
reference/                gold implementations copied verbatim (FT + CV scene sets)
```

## Quickstart (human or agent)
```bash
# 1. demo video end-to-end (Voicebox.app must be open)
cp -r projects/_template projects/demo && cd projects/demo && python3 build.py
cd ../../composer
npx remotion render Explainer ../projects/demo/renders/final.mp4 \
  --props=../projects/demo/artifacts/edit_decisions.json --concurrency=8

# 2. a real video: follow skills/01-pipeline.md step by step
```

## Requirements
- Node ≥ 18 (`composer/` has its own node_modules), ffmpeg/ffprobe, Python 3
- Voicebox.app open (local TTS, port 17493) — or swap `gen_one()` in build.py
