# Skill 03 — Animation Standards (the core of the quality bar)

Two rules separate the gold-reference videos from narrated slides. They are **hard
requirements**, verified at QA. Everything else in this file is technique.

## Rule 1 — Duration-aware phasing (no fixed frame numbers, ever)

The #1 defect in earlier videos: animations keyed to fixed frames (`t(40,56)`) finish
in the first ~2 seconds, then the scene freezes for 20–40s of narration.

Every scene receives `dur` (its narration length in seconds — build.py injects it).
Phase EVERYTHING as fractions of the beat:

```tsx
const p = useP(dur);              // from lib/primitives
<Card o={p(0.30, 0.40)} … />      // lands 30–40% through the narration
<Wire p={p(0.55, 0.62)} … />      // draws just before its subject is spoken
<Foot p={p(0.84, 0.93)} … />      // footnote near the end
```

Plan each scene as a **timeline of 4–8 phases** spread over the full 0..1 range,
matching the narration order (see skill 02's sync contract). The last reveal should
land at p ≈ 0.75–0.9 — if your final phase is at 0.3, the scene will feel frozen for
its back half. `usePop(at)` gives a spring keyed the same way.

Writing `interpolate(frame, [40, 56], …)` or a fixed-frame helper is a defect. The
only legitimate uses of raw `frame` are continuous loops (Rule 2).

**Reveals must SPAN the whole scene, not cluster early (the "frozen title" defect).**
A real bug shipped once: a 96-second title card whose reveals all landed by p≈0.5, so
its main visual sat static for ~46s while narration played — "just audio, the frame is
held still." Two hard consequences:
- **Cap narration per single-visual scene.** A beat that lives on ONE diagram should run
  ≤ ~75–90s. If a scene carries more narration than that, either its main content must
  keep developing to p≈0.85 (new sub-reveals across the whole span), or the beat must be
  SPLIT into two scenes (a long intro → short title + a developing roadmap/overview scene;
  see skills/09 §6 and skills/02). Title/divider/recap cards especially must stay short.
- **Give every scene an unmistakable "this is playing" signal.** Tiny orbiting dots are
  not enough on a 2-minute beat. Add a always-on element that is clearly visible AND, for
  long single-visual scenes, a scene-progress bar that fills L→R over `p(0,1)` at the
  frame edge (`ITScenes.SceneProgress`) so no beat can ever read as frozen while the audio
  runs. This is cheap, universal (add it once in the scene-set router), and collision-free.

## Rule 2 — Continuous motion in every frame

After all reveals land, the scene must still breathe. Layer at least 1–2 of these
(they run off raw `frame` and never stop):

| Element | Primitive / pattern | Use for |
|---|---|---|
| Particle flow along a path | `Flow` | data moving between nodes; keeps diagrams alive |
| Dash-marching connector | `Wire` (auto after draw-in) | any edge/arrow |
| Scan beam sweep | `ScanBeam` | "analysis" feel over images/panels |
| Breathing glow | `Math.sin(frame * 0.06)` on boxShadow/opacity | the scene's hero element |
| Orbiting satellites | `cos/sin(frame * k + i * 2π/n)` | items around a hub |
| Chase highlight | `Math.floor(frame / 26) % n` | cycling emphasis across finished cards/chips |
| Sliding update wave | `(frame * k) % span` over a grid | "every weight updating", heatmaps |
| Typewriter + blinking cursor | `Type` | chat/code/data examples |
| Animated counter | `Counter` driven by a phase | any number that matters |
| Ambient background | `Bg` (built-in sweep + pulse) | free — always on |

Budget per scene: ~3–6 phased reveals + 1–3 continuous layers. More is noise.

## Choreography patterns (from the gold sets)

- **Build left→right / top→bottom** in narration order; wire draws *just before* its
  target card lands, then Flow particles start on it.
- **Transform, don't swap**: morph values/positions (interpolate between states) so
  the eye tracks the change — e.g. filter panels morph pixel values, ViT patches fly
  from grid positions to a token row, compression bars shrink in place.
- **Progressive draws** for charts: slice a polyline's points by a phase; draw axes
  first, curves over the beat's middle, annotations near the end.
- **Multi-state scenes**: for A-then-B stories (RLHF→DPO, semantic→instance), flip a
  phase-derived boolean and *dim/strike* the superseded part rather than removing it.
- **Entrances**: opacity + small translateY (20–26px) + occasional spring scale.
  Exits are unnecessary — cuts handle scene changes.

## Engineering rules (defects if violated)

- **Determinism**: never `Math.random()` in render — frames are rendered by parallel
  workers and will flicker. Use `rnd(i, j, seed)`; animate noise with
  `seed = Math.floor(frame / 4)`.
- **Performance**: no CSS `filter`/`backdrop-filter` (blur cost made a past 40k-frame
  render take 1h40m). Use gradients, boxShadow, and color mixing. Hundreds of divs
  per frame are fine; full-screen filters are not.
- **Author on the Stage**: use `Stage` (1920×1080 design space, scales to output) with
  absolute positioning; safe margins ~100px; `Foot` sits at y=924.
- Springs: `spring({ damping: 13, stiffness: 110 })` for pops; don't overshoot text.
