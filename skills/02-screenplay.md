# Skill 02 — Screenplay & Narration

The screenplay is the spine: scenes are *built around* narration beats, and every
animation is phased to the narration. Write the screenplay before polishing scenes.

## Pace: comprehension first (hard requirement)
Raw Kokoro "Nova" speaks at ≈ 212 wpm — **too fast for teaching**. Effective
educational pace (3Blue1Brown / Khan territory) is **150–165 words per video-minute**.
The pipeline reaches it with three levers, all defaults in the build template:
1. **ATEMPO 0.95** — gentle global slowdown (below ~0.9 sounds muddy).
2. **Silence engineering** — `[pause]` markers in narration (0.6s each) + 0.5s
   inter-beat gaps. Silence is where understanding happens; budget ~8–12s of
   deliberate silence per video-minute.
3. **Fewer words** — the budget table below already accounts for 1 & 2.

| Target | Words (≈165/video-min) | Beats (scenes) |
|---|---|---|
| 60s short | ~165 (shorts may run ~180) | 5–7 |
| 5 min | ~825 | 12–15 |
| 10 min | ~1,650 | 20–26 |
| 20 min | ~3,300 | 30–36 |

A typical content beat is 70–120 words (25–45s incl. pauses). Dividers 20–30 words.
Different voice? Generate one test segment, measure, re-derive before writing 3,000 words.

**Iterate to target**: build.py prints the real total. Short? First add `[pause]`
breathing room and let visuals carry a beat longer; only then add words with *real
content*. **Never pad with extra terminology to hit a duration** — that trades views
for runtime. Long? Cut hedges and repeated transitions. Delete only changed WAVs.

## Cognitive load rules (violations = the #1 reason viewers drop off)
- **Terminology budget: ≤ 2 new terms per minute.** Every new term follows the
  pattern *name it → one plain-English sentence → use it in a concrete example
  immediately*. Then `[pause]`.
  If a term isn't needed to follow the story (NF4, Ringpop, exact library names),
  move it to an on-screen label and don't say it at all.
- **Sentences ≤ 14 words on average, hard cap 20.** One idea per sentence. If a
  sentence needs a comma splice to work, split it.
- **`[pause]` placement**: after each new-term definition · before each "here's the
  key idea" moment · after a big number or result · at rhetorical questions (let the
  viewer answer). 3–6 per content beat.
- **Say it AND show it**: any number, formula, or name the listener would have to
  hold in memory must be on screen at that moment — the audio then only needs to
  carry the meaning, not the payload.
- **Micro-recaps**: in videos ≥ 8 min, end each PART's last beat with one sentence
  that restates the part in plain words ("So: kernels detect patterns, and stacking
  them detects patterns of patterns.").

## Structure that works
- **Hook first** (after a ≤12s title): open with a concrete puzzle, contrast, or
  surprising fact — not "in this video we will…". Example: "You see a cat. The
  computer sees a grid of numbers."
- **One idea per beat — and keep beats short enough to stay alive.** A single-visual
  scene should carry ≤ ~75–90s of narration (≤ ~200 words). Longer than that and the
  visual tends to finish developing while the audio keeps going, so the frame reads as
  frozen (a shipped defect: a 96s title held still). If a beat's narration runs long,
  SPLIT it into two beats (each with its own developing visual) rather than parking two
  minutes of audio on one diagram. The beat's visual must keep developing to p≈0.85.
- **Long videos (≥8 min)**: number the parts ("Part three. Convolutional neural
  networks.") with divider beats — viewers need the map.
- **Callbacks**: reference earlier beats ("remember the kernel from part two") and,
  where honest, the user's other videos (e.g. transfer learning ↔ LLM fine-tuning).
- **Recap beat** at the end: N one-line items (mirrored on screen as a list) + a
  single closer line + "Thanks for watching."

## Writing for TTS (Kokoro)
- Write **spoken** language: "two fifty five", "seven B", "mAP" → "m A P" if needed.
  Spell out symbols: "Q times K transpose". No markdown, no parentheses-heavy prose.
- Short sentences. Rhetorical questions land well. Contractions are fine.
- Numbers that matter should also appear ON SCREEN (Counter/labels) — say it and show it.
- Each segment must stand alone audio-wise (segments are generated independently);
  don't end a segment mid-thought.

## Narration ↔ scene contract
For every SEGMENTS entry, everything the narration mentions should appear on screen
during that beat, phased to roughly *when* it is said: if "softmax" is said 60% in,
the softmax visual fires around `p(0.55, 0.7)`. Estimate positions by word count
through the segment. This sync is what makes the videos feel authored, not assembled.

**The A/V-lag defect (shipped once — do not repeat).** The killer mistake: narration
*front-loads* — it names all the on-screen items in the first ~30–40% of the beat, then
elaborates — but the reveals were spread evenly to p≈0.85 to "fill the beat." Result: the
visual for an item trailed its mention by **10–30 seconds** ("audio is ahead, the frame
renders late"). Two rules:
- **Phase reveals to the ACTUAL spoken position, not evenly across the beat.** Read your
  own narration: if the four items are all spoken in the first 25s of a 90s beat, all four
  reveals belong in the first ~30% — not dribbled to p0.8. When unsure, measure it: the
  build emits caption cues (audio-timed); compare a still at a cue's timestamp against what
  is revealed there (skills/06 §4b).
- **Do NOT fill the back half with late reveals.** Keep the beat alive after the content
  lands with *continuous motion + a scene-progress bar* (skills/03), NOT by delaying the
  reveals. Filling with motion ≠ delaying the payload.
- Reusable mechanism (see `ITScenes` `REVEAL_SPAN`): a scene-set-local `useP` that
  compresses reveals into the front ~0.6 of the beat, while the progress bar and continuous
  layers use the *uncompressed* `useP` over the full beat. Scenes whose narration genuinely
  tracks a running animation (a sweeping dot, a building tree, a steady list) opt out and
  use the full-beat `useP`. The real cure, though, is **shorter beats** (skills/02 above):
  when a beat is ≤ ~75s the narration and reveals align naturally.
