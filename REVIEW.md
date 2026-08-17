# Why earlier explainer videos fell short — and what the gold-reference videos did differently

Audit of `~/Developer/OpenMontage/remotion-composer/src/components/` (July 2026), comparing
the two gold-reference videos — **FTScenes** (fine-tuning, 6.3 min) and **CVScenes/CVScenesA/CVShared**
(computer vision, 20 min) — against the ten scene sets built in earlier sessions
(AwsScenes, CEScenes, EmbeddingScenes, ObsScenes, STTScenes, NetflixScenes, IGScenes,
UberScenes, AttnExplainScenes, MLShortScenes).

## The numbers

Static-analysis counts per file (grep, July 2026):

| Scene set | Fixed-frame `t(a,b)` calls | Duration-aware refs (`dur`) | Continuous motion (`Math.sin(frame`) |
|---|---|---|---|
| NetflixScenes | 71 | 0 | 0 |
| AwsScenes | 54 | 0 | 1 |
| ObsScenes | 54 | 0 | 0 |
| EmbeddingScenes | 35 (raw interpolate) | 0 | — |
| AttnExplainScenes | 29 | 0 | 1 |
| **FTScenes (gold)** | **0** | **16** | **14** |
| **CVScenesA (gold)** | **0** | **17** | **13** |

AwsScenes and NetflixScenes additionally use CSS `blur()` — the AWS video's full-frame
per-frame `blur(40px)` made a 40k-frame render take ~1h40m (documented gotcha).

## Root cause #1 — the freeze (the big one)

Older sets key every animation to **fixed frame numbers**: `t(0,12)`, `t(40,56)`, i.e.
frames 0–56 of a scene. At 30 fps that means *all motion completes in the first ~2
seconds*, then the scene sits frozen for the remaining 20–40 seconds of narration.
The video feels like narrated slides.

The fix (gold pattern): the build script measures each beat's narration length and
injects `dur` into the cut's props; scenes call `useP(dur)` and phase everything as
**fractions of the whole beat** — `p(0.55, 0.65)` fires 55% of the way through the
narration, whatever its length. Reveals stay in lockstep with the voiceover, and the
scene develops for its entire duration.

## Root cause #2 — nothing breathes

Even where older scenes animate, motion is entrance-only (fade/slide in, then stop).
The gold sets layer **always-on motion** that costs nothing and never stops: particle
`Flow`s along paths, `Wire`s that draw in then dash-march forever, scan beams, orbiting
icons, sine "breathing" glows, chase highlights cycling through finished elements, and
an ambient background sweep. Zero frames of the video are static.

## Root cause #3 — illustrated, not computed

Older sets *draw pictures of* concepts (static cards with labels). The gold sets
**run the real thing** whenever the topic allows: the CV video computes actual
convolution, Sobel edges, box blur, max-pooling and noise-interpolation on pixel
grids in JS and animates the number grids; the demo set runs a real bubble sort.
Computed visuals are precise, always self-consistent, cheap to render, and far more
convincing than clip-art.

## Root cause #4 — no QA loop

Earlier videos went straight from code to a full render. The gold workflow renders a
**mid-animation still of every scene** before the final render, reviews them as
images, and fixes what it sees. That loop caught (real examples): a balance-scale
tipping the *wrong way* for its metaphor, stat text rendering as "1000$", title text
overlapping a decoration, RGB channel stacks hiding each other, and detection boxes
colliding with a moving object's lane. None of these are visible in code.

## Root cause #5 — no narration calibration

Older scripts guessed at length. Measured: Kokoro "Nova" ≈ **212 wpm** including
0.35s gaps — so 20 min needs ~4,200 words. The CV video's first pass hit 16.8 min and
was extended segment-by-segment (idempotent regen: delete only the changed WAVs) to
land at 20:04. Without the calibration + iterate loop, a "20-minute video" brief
lands wherever it lands.

## Root cause #6 — engineering hygiene

- `Math.random()` in render code makes frames non-deterministic across render worker
  threads (flicker/tearing). Gold sets use a hash `rnd(i, j, seed)`.
- CSS `filter: blur()` on large surfaces multiplies render time (see AwsScenes).
- Emoji + SVG + gradients render crisply and cheaply; no external image assets needed,
  which also removes the image-provider dependency entirely.

## What the pipeline in this repo does about it

Every root cause maps to a mechanism here:

1. Freeze → `useP(dur)` in `composer/src/lib/primitives.tsx` + `dur` injection in
   `projects/_template/build.py` (skills/03-animation.md).
2. Nothing breathes → continuous-motion primitives (Flow/Wire/ScanBeam/Brackets) +
   the "motion inventory" checklist (skills/03-animation.md).
3. Illustrated → "compute the real thing" doctrine + PixGrid/grid math examples
   (skills/04-visuals.md, reference/CVShared.tsx).
4. No QA → the mandatory still-review protocol with a catalog of the actual bugs it
   has caught (skills/06-qa.md).
5. Length → the 212-wpm budget table + measure-and-extend loop (skills/02-screenplay.md).
6. Hygiene → determinism & perf rules baked into primitives and CLAUDE.md hard rules.
