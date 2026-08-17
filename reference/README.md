# Gold references (read-only)

Verbatim copies of the two gold-standard scene sets from OpenMontage. They are NOT
compiled here (they import OpenMontage's Explainer types) — they are for READING:

- `FTScenes.tsx` — fine-tuning video (6.3 min, 14 scenes). The first duration-aware
  set; study TitleScene→RecapScene for phase choreography and the Knob/Flow/Wire use.
- `CVShared.tsx` — the pixel engine: sprites, conv3/sobel/blur/maxPool math, PixGrid.
  The canonical "compute the real thing" implementation.
- `CVScenesA.tsx` / `CVScenes.tsx` — computer-vision video (20 min, 32 scenes, 6 parts):
  dividers with progress pips, mini live demos inside cards (MiniDemo/HardDemo),
  moving tracked objects, ViT patch-flight, diffusion denoise.

When unsure how detailed or animated a scene should be — open one of these and match it.
