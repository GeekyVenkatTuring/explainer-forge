# Skill 01 — The Pipeline (read first)

End-to-end workflow for producing one explainer video. Follow the steps **in order**;
each step's output is the next step's input. Do not skip the QA step — it is where
the quality actually comes from.

## Step 0 — Understand the brief
Extract: topic, target duration, aspect (default 16:9), voice, music (default: none),
captions (default: none). If the user named a duration, treat it as a real target
(±5%), not a vibe — see the word-budget table in skills/02-screenplay.md.
**"Short" / "Reel" / "Instagram" / "TikTok" / "vertical" → 9:16: read
skills/10-vertical.md now; it overrides screenplay structure, frame zones, layout,
and typography for the whole pipeline.**

## Step 1 — Design the video on paper (10 minutes of thinking, in your head or a scratch file)
1. **Beat list**: break the topic into 12–35 beats (scenes). Videos ≥ 8 min get
   numbered PART dividers (a parameterized `*_divider` variant) every 4–6 beats.
2. **Visual identity**: one theme + 2–4 semantic accent colors + one recurring motif
   (knobs for "tuning", viewfinder/scan-beam for "vision"…). See skills/04-visuals.md.
3. **Per-beat visual concept**: for each beat write one line: what is on screen, what
   *develops* over the beat, and what stays in continuous motion. If a beat's concept
   is "a card with text" — redesign it (skills/04-visuals.md has the menu).

## Step 2 — Write the scene set
- Copy `composer/src/scenes/DemoScenes.tsx` as `<Topic>Scenes.tsx`; build every scene
  on `composer/src/lib/primitives.tsx`. Rules in skills/03-animation.md are mandatory.
- Start each scene from the closest recipe in skills/08-cookbook.md (divider, chart,
  orbit hub, chat, gauge, mini-demos, update wave, tracker, morph, recap, title) —
  adapt proven structures instead of inventing new ones.
- Compose every frame per skills/09-frame-design.md: zone layout (Head/content/Foot),
  the fixed typography hierarchy, text-width budgets (§3) so nothing overlaps, and
  the title-card / end-card / divider anatomies. Run its overlap checklist per scene.
- One variant per beat, prefix-named (`cv_conv`, `ft_lora`…). Parameterize recap/divider.
- Register the prefix in `composer/src/Explainer.tsx` REGISTRY (one line).
- `npx tsc --noEmit` (run inside `composer/`) must be clean for YOUR files.

## Step 3 — Write the screenplay + build script
- Copy `projects/_template/` to `projects/<video-slug>/`; fill SEGMENTS with
  (id, variant, props, narration). Craft rules: skills/02-screenplay.md.
- Run `python3 build.py` (TTS instructions: skills/05-tts.md). It prints the real
  total duration — iterate until within ~5% of target (delete only changed WAVs).

## Step 4 — QA stills (MANDATORY — never skip)
Render one mid-animation still per scene and LOOK at every one of them.
Full protocol + bug catalog: skills/06-qa.md. Fix, re-render the fixed stills, verify.

## Step 5 — Final render
`npx remotion render Explainer <out.mp4> --props=<edit_decisions.json> --concurrency=8`
from `composer/`. Details, timing expectations, gotchas: skills/07-render.md.

## Step 6 — Verify + deliver
ffprobe duration & streams; extract 2 spot-check frames from the actual MP4 and look
at them; copy to `~/Downloads/generated_videos/<slug>.mp4`; report honestly (including
what QA caught and fixed).

## Directory convention
```
projects/<video-slug>/
├── build.py            # screenplay + TTS + props builder
├── assets/             # per-segment WAVs (idempotence cache) + raw/
├── artifacts/edit_decisions.json
└── renders/final.mp4
```
Narration audio is staged to `composer/public/<prefix>/narration.wav`
(Remotion can only load from public/ — never use absolute file:// paths).
