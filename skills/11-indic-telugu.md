# Skill 11 — Indic-language (Telugu) long-form videos

Read this BEFORE designing any Telugu / Indic-script video. It encodes a frame-by-frame
QA review (2026-07-20) of the credit-cards-te chapters plus the pipeline facts proven
in that build. Everything here was either seen broken in delivered video or learned
the hard way; do not re-derive it.

## A. Defects found in delivered video — fix by construction

1. **NEVER apply `letterSpacing` to Telugu text.** Kickers styled with
   `letterSpacing: 8–10` shredded words into spaced syllable clusters on screen:
   "పాఠం" rendered as "పా ఠం", "నిర్మాణం" as "ని ర్మా ణం" — every Head kicker in
   ch01–ch06 shipped like this. Rules:
   - Telugu strings: `letterSpacing: 0` (max 1). No caps-tracking treatment.
   - If a kicker needs the spaced-caps look, write that kicker in LATIN
     ("PART 02", "CIBIL MASTERCLASS") — Latin tracking is fine and looked correct
     in the dividers.
   - This applies to Kicker, chips, mono labels — anywhere a style adds tracking.

2. **No dead-air frames.** Multiple sampled frames showed header + caption and an
   EMPTY content zone many seconds into a beat (worst: ch10 rewards t=120s —
   nothing on screen at all; ch10 t=40s — one card, 70% of frame empty). Cause:
   list/card scenes phased item i at `0.15 + i*0.12` across 35–45s beats. Rules:
   - Something substantial (hero element or the scene's skeleton) must be visible
     by **p = 0.06 or ~2.5s, whichever is sooner**.
   - For beats > 30s with N reveals: show the full structure early as dimmed/ghost
     placeholders (opacity ~0.2, gray border) and LIGHT EACH UP when narration
     reaches it. The viewer should always see the map, never a blank screen.
   - Continuous-motion layers (Flow/ScanBeam/glow) must be attached to CONTENT,
     not just the Bg grid — an empty frame with an animated background still reads
     as frozen/broken.

3. **Fill the vertical band — captions replace Foot, so design to y≈880.**
   Scenes were top-aligned: content typically ended at y≈700, leaving a ~200px
   dead band above the caption box. Rules:
   - With captions ON there is no `Foot`; the content zone is y190→880. Vertically
     CENTER the content block in that band, or size rows/cards to fill it.
   - Checklists/lists: rows were only ~900–1100px wide with the right half of the
     frame empty. Use full 1720px width, or 2 columns, or add a right-side
     illustration/motif panel.
   - Icon-card grids: cards were large but ~60% empty inside (one heading + one
     small line). Either enrich (bigger emoji ≥ 56px, a value chip, a mini-demo)
     or shrink the cards and center the grid.

4. **Telugu typography minimums (Telugu glyphs are denser than Latin):**
   - Minimum readable size **23px** (Latin minimum is 19). Card body ≥ 25px.
   - `lineHeight ≥ 1.35` everywhere Telugu wraps — conjunct stacks (డ్డ, ర్మా, క్ష్మ)
     descend far below the Latin baseline and clip at tight line heights.
   - Width budget: Kohinoor Telugu SANS ≈ **0.58 × fontSize per character**
     (Latin ≈ 0.50). Telugu strings are also simply longer — count the real string,
     add ~15% over the Latin budget, and prefer wrapping inside a fixed-width box.

5. **Caption band = y935–1018.** Nothing (including bottom chip rows) below y≈880.
   The ch08 gauge scene's score-band chips at y≈870 were one line-wrap away from
   collision. Two-line captions are common in Telugu — budget for them.

## B. Pipeline facts (proven in credit-cards-te — reuse, don't rediscover)

- **TTS**: `edge-tts --voice te-IN-ShrutiNeural` (f) / `te-IN-MohanNeural` (m).
  Pass rate as ONE token: `f"--rate={RATE}"` (e.g. `--rate=-4%`); two tokens → argparse
  exit 2. edge-tts → mp3 → ffmpeg 24kHz mono WAV. Shruti ≈ **110 Telugu words/min**
  at -4% — budget ≈ 110 × target-minutes words, then iterate.
- **Fonts**: use the macOS SYSTEM font **'Kohinoor Telugu'** appended to the SANS/MONO
  stacks in `lib/primitives.tsx` (Latin faces first so brands/₹/numbers stay Latin).
  NO web fonts, NO `delayRender`, NO `staticFile()` font loading — both variants
  caused intermittent delayRender timeouts that killed FULL renders at random frames
  even though single-frame QA stills passed.
- **QA stills pass ≠ render passes**: always do at least one FULL chapter render
  before assuming the pipeline is healthy.
- Brand names, ₹ amounts, numbers, % stay **Latin** on screen; explanatory labels Telugu.
- `mix()` in primitives parses HEX only — passing `rgba(...)` (like `T.line`) breaks;
  use `T.bg2`/`T.panel`.
- 5-node pipeline rows: use `x = 170 + i*340` (skill 09's i*350 overflows 1820 with
  node width 290).
- Chapter-based `build.py` (CHAPTERS dict, `python3 build.py chNN`) is the right
  shape for multi-hour courses: each chapter renders and delivers independently.
- Renders: ~5–6 fps at 1080p `--concurrency=8`; a 15-min chapter ≈ 80–90 min. Run in
  background; MP4 appears only at the very end.

## C. Review checklist additions for Telugu QA stills

On top of skill 06's checklist, verify per still:
- [ ] No Telugu string is letter-spaced (look for gaps INSIDE words)
- [ ] Frame at ~15% of the beat: is anything substantial on screen yet?
- [ ] Content reaches down toward y≈880 or is vertically centered (no dead band
      above the captions)
- [ ] All Telugu ≥ 23px; conjuncts not clipped by tight lineHeight
- [ ] Nothing below y≈880 (two-line caption clearance)
- [ ] Kickers either Latin-tracked or Telugu-untracked
