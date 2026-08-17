# Skill 09 — Frame Design: anatomy, typography, and overlap-proof layout

You are composing frames blind — you only SEE them at QA. This skill makes frames
correct by construction so QA finds polish issues, not layout disasters. All numbers
are for the 1920×1080 `Stage` (author at this size always; vertical 9:16 is a
separate adaptation).

## 1. The frame zones (every content scene)

```
y    0 ─────────────────────────────────────────────
      54   HEADER ZONE (Head: kicker + title)       ← always via <Head>
     ~170 ──────────────────────────────────────────
     200   CONTENT ZONE (~200 → 900)                ← everything lives here
     900 ──────────────────────────────────────────
     924   FOOTER ZONE (Foot: one-line takeaway)    ← optional but recommended
    1000   hard bottom safe line
x:  100 left/right margins → usable width 1720 (x: 100 → 1820)
```

- One `Head` per scene (kicker ≤ 40 chars, title ≤ 55 chars — see width math below).
- Content NEVER enters the header zone (y < 190) or crosses y > 900 unless it is the
  Foot. If content needs more room, drop the Foot — never squeeze into it.
- Full-bleed scenes (title, divider, recap) skip Head/Foot and center on the canvas.

## 2. Typography hierarchy (fixed — don't invent sizes)

| Role | Font | Weight | Size | Notes |
|---|---|---|---|---|
| Title-card headline | SANS | 800 | 110–128 | 1–2 lines, letterSpacing −3 |
| Scene title (Head) | SANS | 800 | 52 | one line only |
| Section/card heading | SANS | 800 | 30–40 | |
| Body / explanation | SANS | 400–700 | 26–30 | lineHeight 1.3–1.45 |
| Kicker / labels / data | MONO | 700 | 21–26 | caps + letterSpacing for kickers |
| Footnote (Foot) | MONO | 400 | 23 | |
| Chip/badge text | MONO | 700 | 22–27 | |
| Minimum anywhere | — | — | **19** | below this is illegible at 1080p |

Hierarchy rule: each frame has exactly ONE largest element (the thing the beat is
about). If two elements compete at the same size, demote one.

## 3. Text width math (this is how you prevent overlap while blind)

Approximate rendered width:
- `SANS` ≈ **0.50 × fontSize** per char (800-weight ≈ 0.53)
- `MONO` ≈ **0.60 × fontSize** per char

So before placing text, budget it:
- Head title at 52px: 55 chars ≈ 55 × 27.6 ≈ 1520px ✓ (fits 1720). 65 chars ✗.
- A 520px-wide card, 28px body → 520/14 ≈ 37 chars/line; 3 lines ≈ 110 chars max.
- A MONO label at 24px next to a 700px bar: label 20 chars ≈ 288px → bar + gap +
  label = 700+14+288 = 1002px; place at x ≤ 818.

Hard rules:
- EVERY text block gets an explicit width (`width` or `right`) — never unbounded
  absolute text; long content wraps (`lineHeight`) inside its box instead of
  colliding with neighbors.
- Count characters of your longest REAL string (not the placeholder) against the
  budget. Recap items ≤ 78 chars at 29–30px in a 1340px list. Card bodies: trim the
  copy until it fits — don't shrink below the size table.
- Numbers that animate (Counter) grow: budget for the FINAL value + suffix.

## 4. Spacing & alignment system

- Spacing scale: 8 / 14 / 22 / 30 / 60. Related items 8–14 apart, siblings 22–30,
  groups 60+. Card padding: "24px 28px".
- **Column grids** (memorize, reuse):
  - 2-col: x = 130, 990 · w = 790
  - 3-col: x = 140 + i×560 · w = 520
  - 4-col: x = 130 + i×430 · w = 390
  - Pipeline rows: 5 nodes → x = 170 + i×350, w = 290; wires at the vertical center.
- Vertical stacking arithmetic: nextY = y + ownHeight + gap. Compute it — do not
  eyeball. A 4-row list at rowH 92 starting y=300 ends at 668; anything below starts ≥ 700.
- Alignment: pick ONE content top edge (usually y=250–300) and ONE baseline grid per
  scene. Center full-bleed scenes with flexbox, not manual x math.

## 5. Element budget & z-order

- Per frame: 1 hero element + ≤ 3 supporting groups + 1–3 continuous-motion layers.
  If a scene needs more, it is two beats — split it in the screenplay.
- z-order (DOM order): Bg → stage decorations (Brackets/ScanBeam) → wires/flows →
  panels/cards → text → highlight overlays. Wires under cards: draw Wire before the
  Cards it connects so line ends tuck under the card borders.
- Anything that MOVES owns its full path as a keep-out lane (skill 08 §9).

## 6. Title card (the video's first ~10–12s)

Anatomy (see DemoScenes TitleScene + cookbook §12):
1. Kicker chip centered: `CATEGORY · PROMISE` (e.g. "PIXELS → PERCEPTION · FULL COURSE")
2. Headline: 1–2 lines, 110–128px, second line in the accent with a glow
   text-shadow; spring pop on entry.
3. Underline: 5px gradient bar drawing to 420–560px via `p(0.18, 0.45)`.
4. Subtitle: 36–40px muted, ≤ 90 chars — the contents promise ("X · Y · Z — end to end").
5. Identity ambience: the video's motif animating (knobs, pixel grid resolving from
   noise, equalizer, orbiting dots) — placed in corners/edges, NEVER behind the
   headline text block (past bug: decoration overlapped the subtitle).
Nothing else. No Head/Foot. The narration over it is the hook promise (≤ 45 words).

**Keep the title SHORT — ≤ ~20–25s of narration (~45–55 words).** A title card's
headline is static by nature, so a long intro narration parked on it makes the frame
read as frozen (a real shipped defect: a 96s title held still for ~46s). If the intro
runs long, split it: a short title card, then a *developing* roadmap/overview scene
that builds the course's parts one by one across its whole duration (see the
`it_roadmap` pattern — numbered part chips revealed on a filling rail). The rest of the
intro belongs on scenes whose content changes, not on the title.

## 7. End card / recap (the video's last beat)

Anatomy (cookbook §11): centered kicker "RECAP — THE WHOLE MAP" → 60–64px title
("<Topic> in one breath") → N numbered items (5–8, one line each ≤ 78 chars, phased
`at = 0.05 + i×0.09`) → glowing italic closer (40–42px, ONE sentence, the video's
thesis). Narration ends "…Thanks for watching." Keep motif decorations at ≤ 0.5
opacity in corners. If the video is long (≥ 8 items), cap at 8 — the recap is a
souvenir, not a table of contents.

## 8. Divider cards (long videos)

Fixed anatomy (cookbook §1): PART NN mono kicker → 96px title (≤ 24 chars) → color
underline → one-line sub (≤ 60 chars) → progress pips. Divider color = the accent of
the upcoming part. Duration 7–10s of narration. Same layout every time — dividers
are wayfinding, not creativity slots.

## 9. Overlap prevention checklist (run mentally per scene, then verify at QA)

- [ ] Every absolute text block has a width; longest real string fits its budget (§3)
- [ ] Stacked y-positions computed, incl. margins/labels above grids (PixGrid label
      adds ~cell×0.5+8 to the top)
- [ ] Rightmost element: x + w ≤ 1820; bottom: y + h ≤ 900 (content) / 1000 (Foot)
- [ ] Animated growth (bars, counters, typewriter lines) checked at FINAL size
- [ ] Moving elements' full path is clear of static elements and their labels
- [ ] Labels attached to phased elements appear WITH or AFTER their element, never
      floating alone before it
- [ ] Two things revealed at the same phase never occupy the same region
