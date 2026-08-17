# Skill 04 — Visual Design & Computed Visuals

## One identity per video
Before writing any scene, fix the identity (5 minutes, huge payoff):

1. **Theme**: `makeTheme({...})` — near-black background family, one primary accent.
   Keep backgrounds dark and desaturated; accents saturated.
2. **Semantic accent colors (2–4)**: colors MEAN something consistently across all
   scenes. Examples from the gold sets: fine-tuning used cyan=frozen-base,
   amber=tuning, violet=adapters; CV used cyan=pixels, amber=classical,
   violet=neural, green=detection, pink=generative. Never decorate randomly.
3. **A recurring motif**: one visual signature that appears in the title, dividers,
   and backgrounds — rotating knobs (tuning), viewfinder brackets + scan beam
   (vision), a budget meter (context), a map grid (dispatch). This is what makes the
   video feel like ONE authored piece.
4. **Typography**: `SANS` (Space Grotesk stack) for headlines/body, `MONO` for
   data/labels/kickers. Headline 800 weight, negative letter-spacing. Kicker strips
   (small mono caps + colored dash) top every diagram scene via `Head`.

## The doctrine: compute the real thing
The single biggest visual upgrade: when the topic has an algorithm, **run it** —
don't draw a picture of it.

- CV video: convolution, Sobel edges, blur, max-pooling and diffusion noise are
  actually computed over pixel grids in JS (`reference/CVShared.tsx`) and the number
  grids animate. The demo set runs a real bubble sort.
- The pattern: precompute at **module scope** (deterministic, once per worker), then
  index the precomputed states by a phase: `steps[Math.floor(p(0.15, 0.75) * steps.length)]`.
- `PixGrid` renders any `number[][]` as a heatmap/pixel image with scan-order reveal,
  optional value labels, and a highlight window. Define sprites with `gridFromRows`.
- Works for: sorting, graph traversal, gradient descent steps, attention weights,
  cellular automata, tokenization, compression, queues/caches — most CS topics.

## Visual menu (never "a card with text")
Every beat needs a visual that *develops*. Pick from (all proven in the gold sets):
pipeline of Cards + Wires + Flow · number-grid transformations (PixGrid) · animated
bar/line charts drawn progressively (SVG polyline slicing) · before/after morphs ·
balance scale / gauge / meter metaphors · typed chat or code (Type) · orbit/hub
diagrams · stacked-segment towers (memory budgets) · emoji actors with boxes/masks
drawn over them (detection/segmentation style) · matrix/token rows with attention
arcs · mini live demos inside cards (a 100×340px stage per card).

Emoji are legitimate, render-perfectly, and need no assets — use them as actors
(🐱🚗🧑‍⚖️), with your drawn geometry (boxes, masks, skeletons) on top.

## Layout rules (QA catches violations)
- 1920×1080 Stage; keep 100px side margins; `Head` at top; `Foot` at y=924.
- Check width arithmetic: `x + w ≤ 1820`. A 3-column grid: x = 140 + i*560, w=520.
- Nothing overlaps unless intentional; moving elements need a cleared lane — check
  the FULL path of anything that travels (a past bug: a driving car crossed three
  static objects' boxes).
- Metaphor direction matters: heavier side of a scale goes DOWN; growth goes UP;
  time flows LEFT→RIGHT. State the metaphor in a comment and double-check the sign
  (a past bug: the "winning" side of a balance scale rose).
- Text on colored chips: dark text (`theme.bg0`) on saturated fills; muted mono for
  captions; values ≥ 21px font at 1080p.
- Footnote (`Foot`) reinforces the beat's takeaway in one line — appears near the end.
