# Skill 08 — Scene Cookbook (copy-paste recipes)

Concrete, tested snippets for every recurring archetype in the gold videos. Adapt
coordinates/colors; keep the timing structure. All assume:
`const p = useP(dur);` · theme `T` · accents `A` · imports from `../lib/primitives`.

---

## 1. Section divider with progress pips (videos ≥ 8 min)
Parameterized once, reused for every part: `{n, title, sub, color}` via cut props.
```tsx
const Divider: React.FC<{ dur?: number; n?: number; title?: string; sub?: string; color?: string }> =
({ dur, n = 1, title = "", sub = "", color = T.accent }) => {
  const frame = useCurrentFrame(); const p = useP(dur);
  return (
    <Stage>
      <Brackets x={330} y={300} w={1260} h={480} color={color} o={p(0.02, 0.14)} len={54} />
      <ScanBeam theme={T} x={340} y={310} w={1240} h={460} color={color} o={p(0.05, 0.2)} speed={1.6} />
      <div style={{ position: "absolute", left: 0, right: 0, top: 360, textAlign: "center" }}>
        <div style={{ fontFamily: MONO, fontWeight: 800, fontSize: 34, color, letterSpacing: 10, opacity: p(0.05, 0.15) }}>PART {"0" + n}</div>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 96, color: T.text, letterSpacing: -2, marginTop: 20, opacity: p(0.12, 0.24), transform: `translateY(${(1 - p(0.12, 0.24)) * 30}px)` }}>{title}</div>
        <div style={{ height: 5, width: interpolate(p(0.2, 0.5), [0, 1], [0, 420]), background: color, borderRadius: 3, margin: "26px auto" }} />
        <div style={{ fontFamily: SANS, fontSize: 34, color: T.muted, opacity: p(0.3, 0.45) }}>{sub}</div>
      </div>
      <div style={{ position: "absolute", left: 0, right: 0, top: 860, display: "flex", justifyContent: "center", gap: 16, opacity: p(0.3, 0.45) }}>
        {[1, 2, 3, 4, 5, 6].map((i) => (
          <div key={i} style={{ width: i === n ? 44 : 14, height: 14, borderRadius: 8,
            background: i <= n ? color : mix(T.panel, color, 0.15), border: `1.5px solid ${i <= n ? color : T.line}`,
            opacity: i === n ? 0.7 + Math.sin(frame * 0.1) * 0.3 : 1 }} />
        ))}
      </div>
    </Stage>
  );
};
```

## 2. Progressive chart draw (bar or line)
Bars grow one-per-phase; lines are polylines sliced by a phase. Draw axes early,
curves across the middle, annotations near the end.
```tsx
// BAR (per-bar phased growth + counter label)
{bars.map((b, i) => {
  const grow = p(0.08 + i * 0.1, 0.18 + i * 0.1);
  const h = b.v * SCALE * grow;
  return (<div key={i}>
    <div style={{ position: "absolute", left: X0 + i * W, top: Y0 - h, width: 130, height: h,
      borderRadius: "12px 12px 0 0", background: `linear-gradient(180deg, ${b.c}, ${mix(b.c, T.bg1, 0.45)})`,
      border: `2px solid ${b.c}`, borderBottom: "none" }} />
    <div style={{ position: "absolute", left: X0 + i * W - 20, top: Y0 - h - 46, width: 170, textAlign: "center",
      fontFamily: MONO, fontWeight: 800, fontSize: 30, color: b.c, opacity: grow }}>{b.v}%</div>
  </div>);
})}

// LINE (slice a precomputed point list by phase; dashed = second series)
const cp = p(0.5, 0.95);
const pts = Array.from({ length: 60 }).map((_, i) => { const t = i / 59;
  return `${X0 + t * 660},${Y0 - 300 * (1 - Math.exp(-t * 3.4))}`; });
<polyline points={pts.slice(0, Math.max(2, Math.round(60 * cp))).join(" ")}
  fill="none" stroke={A.ok} strokeWidth={5} />
// reference line (human baseline, budget…): dashed horizontal + label, phased in late
```

## 3. Orbit hub (items around a center)
```tsx
{items.map((it, i) => {
  const ang = (i / items.length) * Math.PI * 2 - Math.PI / 2 + Math.sin(frame * 0.008) * 0.06; // slow sway
  const x = 960 + Math.cos(ang) * 560, y = 555 + Math.sin(ang) * 280;   // ellipse, not circle (16:9)
  const at = 0.08 + i * 0.06;
  const active = Math.floor(frame / 26) % items.length === i && p(0.55, 0.56) > 0.5; // chase
  return (<React.Fragment key={i}>
    <Wire x1={960} y1={555} x2={x} y2={y} p={p(at, at + 0.06)} color={active ? A.ok : mix(T.muted, T.bg1, 0.4)} w={active ? 3 : 2} arrow={false} />
    <div style={{ position: "absolute", left: x - 150, top: y - 44, width: 300, height: 88, borderRadius: 16,
      background: mix(T.panel, active ? A.ok : A.main, active ? 0.18 : 0.08),
      border: `2.5px solid ${active ? A.ok : mix(T.line, A.main, 0.5)}`,
      display: "flex", alignItems: "center", gap: 14, padding: "0 20px", boxSizing: "border-box",
      opacity: p(at, at + 0.08), transform: `scale(${active ? 1.08 : 1})` }}>
      <span style={{ fontSize: 40 }}>{it.emoji}</span>
      <span style={{ fontFamily: SANS, fontWeight: 700, fontSize: 26, color: T.text }}>{it.label}</span>
    </div>
  </React.Fragment>);
})}
```

## 4. Chase highlight (cycling emphasis after elements land)
Keeps a finished row/grid alive for the rest of the beat.
```tsx
const hot = Math.floor(frame / 26) % chips.length;           // 26 frames per hop
{chips.map((c, i) => (
  <div key={i} style={{ fontFamily: MONO, fontWeight: 700, fontSize: 24,
    color: hot === i ? T.bg0 : A.main,
    background: hot === i ? A.main : mix(T.panel, A.main, 0.12),
    border: `2px solid ${A.main}`, borderRadius: 999, padding: "10px 24px",
    transform: `translateY(${hot === i ? -6 : 0}px)` }}>{c}</div>
))}
```

## 5. Typewriter chat / code panel
```tsx
const bubbles = [
  { role: "user",      c: A.main, text: "…", at: 0.22 },
  { role: "assistant", c: A.warm, text: "…", at: 0.38 },  // stagger `at` down the thread
];
{bubbles.map((b, i) => (
  <div key={i} style={{ marginBottom: 18, opacity: p(b.at, b.at + 0.05) }}>
    <div style={{ fontFamily: MONO, fontSize: 21, color: b.c, fontWeight: 700, marginBottom: 6 }}>{b.role}</div>
    <div style={{ background: mix(T.panel, b.c, 0.1), border: `2px solid ${mix(T.line, b.c, 0.55)}`, borderRadius: 14, padding: "14px 20px" }}>
      <Type text={b.text} p={p(b.at, b.at + 0.22)} color={T.text} />   {/* types over ~1/5 of the beat */}
    </div>
  </div>
))}
```

## 6. Stacked gauge / budget tower (memory, cost, quota)
Segments stack bottom-up, each phased; overflow past a dashed limit line = red + pulse.
```tsx
<div style={{ position: "relative", width: 380, height: 480, border: `2.5px solid ${T.line}`, borderRadius: 18,
  background: T.panel, display: "flex", flexDirection: "column-reverse", overflow: "hidden" }}>
  {segs.map((s, i) => (   // segs: { at, h, label, c }
    <div key={i} style={{ height: s.h * p(s.at, s.at + 0.1), background: `linear-gradient(90deg, ${mix(T.panel, s.c, 0.75)}, ${mix(T.panel, s.c, 0.45)})`,
      borderTop: `2px solid ${s.c}`, display: "flex", alignItems: "center", paddingLeft: 18 }}>
      <span style={{ fontFamily: MONO, fontSize: 21, color: T.text, whiteSpace: "nowrap", opacity: p(s.at + 0.04, s.at + 0.12) }}>{s.label}</span>
    </div>
  ))}
  <div style={{ position: "absolute", bottom: LIMIT_Y, left: 0, right: 0, borderTop: `3px dashed ${A.ok}`, opacity: p(0.4, 0.5) }} />
</div>
// + <Counter p={p(0.66, 0.82)} to={112} prefix="≈ " suffix=" GB" color={A.bad} size={52} />
// + warning text with opacity 0.6 + Math.sin(frame * 0.12) * 0.4
```

## 7. Mini live demo inside a card (task-zoo pattern)
A small stage (~100×340px) per card with its own looping animation, switched on
once the card has landed (`on = o > 0.9`). Loop off raw frame: `const t = (frame % 90) / 90;`
Examples worth copying from `reference/CVScenes*.tsx`: box drawing around an emoji,
mask fill, dot following a path, typed OCR result, per-demo `switch(kind)`.

## 8. Update wave over a grid ("everything is changing")
```tsx
const wave = (frame * 1.6) % (cols + 6) - 3;               // sweeps forever
{cells.map(({ r, c }, i) => {
  const heat = Math.max(0, 1 - Math.abs(c - wave + Math.sin(r * 1.7) * 1.4) / 2.6);
  return <div key={i} style={{ width: 48, height: 48, borderRadius: 9,
    background: mix(T.panel, A.warm, 0.08 + heat * 0.75),
    border: `1.5px solid ${mix(T.line, A.warm, heat)}`,
    transform: `scale(${1 + heat * 0.14})`,
    boxShadow: heat > 0.4 ? `0 0 16px ${mix(T.bg0, A.warm, heat)}` : "none" }} />;
})}
```

## 9. Element that MOVES with a tracking annotation
Anything that travels: derive position from frame, attach labels/boxes to the SAME
variable, and clear its whole lane of other elements (QA catches collisions).
```tsx
const carX = X0 + 90 + ((frame * 1.5) % (W - 260));
<span style={{ position: "absolute", left: carX, top: LANE_Y, fontSize: 110 }}>🚗</span>
<div style={{ position: "absolute", left: carX - 10, top: LANE_Y - 8, width: 132, height: 116,
  border: `3.5px solid ${A.gen}`, borderRadius: 10, opacity: p(0.5, 0.58) }} />
```

## 10. Morph between computed states (filters, compression, denoise)
Interpolate VALUES between precomputed grids/arrays so the audience sees the change happen.
```tsx
const m = p(0.2, 0.36);
const g = SRC.map((row, r) => row.map((v, c) => Math.round(v + (DST[r][c] - v) * m)));
<PixGrid theme={T} g={g} x={140} y={300} cell={30} />
// noise version (diffusion): v*(1-amp) + rnd(r, c, Math.floor(frame/5)) * 255 * amp
```

## 11. Recap scene (every video ends with one)
See `DemoScenes.tsx` RecapScene — phased list items (`at = 0.06 + i * 0.09`),
left-accent bars, numbered mono badges, glowing italic closer at p(0.8, 0.9).
Items come from cut props so build.py owns the copy.

## 12. Title scene ingredients
Spring pop on the block (`usePop(0)`), two-line title with the second line in the
accent + text-shadow glow, phased underline draw (`interpolate(p(0.18,0.45),[0,1],[0,520])`),
kicker chip, subtitle at p(0.28, 0.5), and 1–2 ambient identity elements (orbiting
dots, equalizer bars, the video's motif) running off raw frame.
