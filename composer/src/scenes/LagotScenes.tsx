/**
 * LagotScenes.tsx — Lagot / loquat (Eriobotrya japonica) farmer course.
 * Prefix `lag`. English, captions ON, 16:9 1080p30.
 *
 * Identity:
 *   FRUIT #F4A261  ripe fruit, harvest, rupees
 *   LEAF  #7CB518  tree, planting, care
 *   COOL  #4ECDC4  climate, water, cool winters
 *   RISK  #E76F51  lookalikes, perishability, skip-if
 * Motif: falling petals + a filling fruit cluster.
 *
 * Captions occupy the bottom band → Foot at y=856, no default Foot.
 * Reveals compressed into REVEAL_SPAN; progress bar uses full-beat usePfull.
 */
import React from "react";
import { AbsoluteFill, interpolate, useCurrentFrame } from "remotion";
import {
  makeTheme, mix, useP as usePfull, usePop, rnd, MONO, SANS, Theme,
  Bg, Stage, Kicker, Head, Card, Flow, Wire, Counter, Brackets, ScanBeam,
} from "../lib/primitives";

const REVEAL_SPAN = 0.62;
const useP = (dur?: unknown) => {
  const p = usePfull(dur);
  return (a: number, b: number) => p(Math.min(1, a * REVEAL_SPAN), Math.min(1, b * REVEAL_SPAN));
};

const Foot: React.FC<{ theme: Theme; p: number; children: React.ReactNode }> = ({ theme, p, children }) => (
  <div style={{
    position: "absolute", left: 100, top: 856, right: 100, fontFamily: MONO, fontSize: 22,
    color: theme.muted, opacity: p, lineHeight: 1.35, transform: `translateY(${(1 - p) * 12}px)`, textAlign: "center",
  }}>{children}</div>
);

const T = makeTheme({ accent: "#F4A261", bg0: "#07080A", bg1: "#0E120E", bg2: "#161C16", panel: "#1A2218" });
const A = { fruit: "#F4A261", leaf: "#7CB518", cool: "#4ECDC4", risk: "#E76F51", ok: "#8BD450", muted: "#8B9380" };
const col = (c?: string) => (c && (A as Record<string, string>)[c]) || c || A.fruit;

// ---- computed orchard / yield (module scope, deterministic)
const TREES_ACRE = 96;
const YIELD = Array.from({ length: 21 }, (_, y) => {
  if (y < 3) return { y, cons: 0, good: 0 };
  const ramp = Math.min(1, (y - 2) / 13);
  return { y, cons: Math.round(TREES_ACRE * 8 * ramp), good: Math.round(TREES_ACRE * 28 * ramp) };
});
const CASH = (() => {
  const est = 90000, ann = 28000, pCons = 80, pGood = 120;
  let c = -est, g = -est;
  return YIELD.map((row) => {
    if (row.y >= 1) { c -= ann; g -= ann; }
    c += row.cons * pCons;
    g += row.good * pGood;
    return { y: row.y, cons: c, good: g, yCons: row.cons, yGood: row.good };
  });
})();

const Petals: React.FC<{ o?: number; n?: number; color?: string; seed?: number }> = ({
  o = 0.4, n = 18, color = A.fruit, seed = 0,
}) => {
  const frame = useCurrentFrame();
  return (
    <>
      {Array.from({ length: n }).map((_, i) => {
        const x0 = rnd(i, 1, seed) * 1920;
        const span = 1180;
        const t = (frame * 1.8 + i * 73 + rnd(i, 2, seed) * span) % span;
        const sway = Math.sin(frame * 0.04 + i) * 28;
        return (
          <div key={i} style={{
            position: "absolute", left: x0 + sway, top: t - 80, width: 14, height: 9, borderRadius: "70% 30%",
            background: color, opacity: o * Math.max(0, Math.sin((t / 1080) * Math.PI)) * 0.9,
            transform: `rotate(${20 + Math.sin(frame * 0.03 + i) * 40}deg)`,
            boxShadow: `0 0 8px ${color}`,
          }} />
        );
      })}
    </>
  );
};

const Cluster: React.FC<{ x: number; y: number; n?: number; o?: number; ripe?: number }> = ({
  x, y, n = 7, o = 1, ripe = 1,
}) => {
  const frame = useCurrentFrame();
  return (
    <div style={{ position: "absolute", left: x, top: y, opacity: o }}>
      {Array.from({ length: n }).map((_, i) => {
        const ang = -0.9 + (i / Math.max(1, n - 1)) * 1.8;
        const r = 38 + (i % 3) * 8;
        const pulse = 1 + Math.sin(frame * 0.07 + i) * 0.04;
        const on = i / n <= ripe;
        return (
          <div key={i} style={{
            position: "absolute",
            left: Math.sin(ang) * r * pulse, top: Math.cos(ang) * r * 0.7,
            width: 28, height: 34, borderRadius: "50% 50% 50% 50% / 45% 45% 55% 55%",
            background: on ? `linear-gradient(180deg, ${A.fruit}, ${mix(A.fruit, T.bg0, 0.35)})` : mix(T.panel, A.leaf, 0.2),
            border: `2px solid ${on ? A.fruit : A.leaf}`,
            boxShadow: on ? `0 0 12px ${mix(T.bg0, A.fruit, 0.45)}` : "none",
          }} />
        );
      })}
    </div>
  );
};

const SceneProgress: React.FC<{ accent: string; dur?: number }> = ({ accent, dur }) => {
  const p = usePfull(dur);
  const w = p(0, 1);
  return (
    <div style={{
      position: "absolute", left: 0, bottom: 0, height: 5, width: `${w * 100}%`,
      background: `linear-gradient(90deg, ${mix(accent, T.bg0, 0.35)}, ${accent})`,
      boxShadow: `0 0 12px ${accent}`, opacity: 0.85,
    }} />
  );
};

// ============================================================================ TITLE
const TitleScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const p = usePfull(dur);
  const pop = usePop(dur);
  return (
    <AbsoluteFill style={{ alignItems: "center", justifyContent: "center" }}>
      <Petals o={0.5} n={22} />
      <Cluster x={220} y={200} o={0.9} ripe={0.7 + Math.sin(frame * 0.04) * 0.2} />
      <Cluster x={1620} y={720} n={6} o={0.7} ripe={0.9} />
      <div style={{ textAlign: "center", transform: `scale(${0.92 + pop(0) * 0.08})` }}>
        <div style={{ display: "flex", justifyContent: "center", marginBottom: 26 }}>
          <Kicker theme={T} text="LAGOT · LOQUAT · FARMER COURSE" cx />
        </div>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 110, lineHeight: 1.02, letterSpacing: -3, color: T.text }}>
          <div>Lagot Fruit</div>
          <div style={{ color: A.fruit, textShadow: `0 0 70px ${mix(T.bg0, A.fruit, 0.7)}` }}>Before You Plant</div>
        </div>
        <div style={{ height: 5, width: interpolate(p(0.18, 0.45), [0, 1], [0, 540]), background: `linear-gradient(90deg, ${A.leaf}, ${A.fruit})`, borderRadius: 3, margin: "30px auto" }} />
        <div style={{ fontFamily: SANS, fontSize: 34, color: T.muted, opacity: p(0.28, 0.5) }}>
          what it is · how to grow it · whether it pays — in India
        </div>
      </div>
    </AbsoluteFill>
  );
};

const PARTS = [
  { n: 1, title: "What lagot is", sub: "names, lookalikes, the tree", c: A.fruit },
  { n: 2, title: "Eat, kitchen, factory", sub: "food, processing, not medicine", c: A.leaf },
  { n: 3, title: "Climate and India", sub: "where it actually fruits", c: A.cool },
  { n: 4, title: "The farm year", sub: "plant, flower, harvest", c: A.fruit },
  { n: 5, title: "Varieties and plants", sub: "grafts, pollination, nursery", c: A.leaf },
  { n: 6, title: "Planting the orchard", sub: "spacing, pits, intercrop", c: A.cool },
  { n: 7, title: "Years until fruit", sub: "year three, not year one", c: A.fruit },
  { n: 8, title: "Care that decides yield", sub: "water, prune, feed", c: A.leaf },
  { n: 9, title: "Harvest and yield", sub: "clip bunches, real numbers", c: A.fruit },
  { n: 10, title: "Pests and packing", sub: "spoilage is the silent cost", c: A.risk },
  { n: 11, title: "Costs and cash", sub: "establishment to year fifteen", c: A.cool },
  { n: 12, title: "Market and verdict", sub: "who buys, and should you", c: A.fruit },
];

const RoadmapScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const p = usePfull(dur);
  const hot = Math.floor(frame / 22) % PARTS.length;
  return (
    <AbsoluteFill>
      <Petals o={0.28} n={14} />
      <div style={{ position: "absolute", left: 0, right: 0, top: 72, textAlign: "center", opacity: p(0, 0.06) }}>
        <Kicker theme={T} text="TWELVE PARTS · ONE ORCHARD DECISION" cx />
      </div>
      {PARTS.map((pt, i) => {
        const colI = i < 6 ? 0 : 1;
        const row = i % 6;
        const at = 0.06 + i * 0.055;
        const o = p(at, at + 0.07);
        const active = hot === i;
        const x = 100 + colI * 900;
        const y = 168 + row * 108;
        return (
          <div key={i} style={{
            position: "absolute", left: x, top: y, width: 860, height: 96, display: "flex", alignItems: "center", gap: 18,
            opacity: o, transform: `translateX(${(1 - o) * -24}px)`,
            background: mix(T.panel, pt.c, active ? 0.22 : 0.08),
            border: `2px solid ${active ? pt.c : T.line}`, borderRadius: 16, padding: "0 20px", boxSizing: "border-box",
            boxShadow: active ? `0 0 20px ${mix(T.bg0, pt.c, 0.45)}` : "none",
          }}>
            <div style={{
              width: 52, height: 52, borderRadius: 12, flexShrink: 0, background: mix(T.panel, pt.c, 0.3),
              border: `2px solid ${pt.c}`, display: "flex", alignItems: "center", justifyContent: "center",
              fontFamily: MONO, fontWeight: 800, fontSize: 24, color: pt.c,
            }}>{String(pt.n).padStart(2, "0")}</div>
            <div>
              <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 30, color: T.text, letterSpacing: -0.5 }}>{pt.title}</div>
              <div style={{ fontFamily: MONO, fontSize: 20, color: pt.c, marginTop: 2 }}>{pt.sub}</div>
            </div>
          </div>
        );
      })}
    </AbsoluteFill>
  );
};

const Divider: React.FC<{ dur?: number; n?: number; title?: string; sub?: string; color?: string }> = ({
  dur, n = 1, title = "", sub = "", color = A.fruit,
}) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  return (
    <Stage>
      <Petals o={0.32} n={16} color={color} seed={n} />
      <Brackets x={330} y={300} w={1260} h={480} color={color} o={p(0.02, 0.14)} len={54} />
      <ScanBeam theme={T} x={340} y={310} w={1240} h={460} color={color} o={p(0.05, 0.2)} speed={1.6} />
      <div style={{ position: "absolute", left: 0, right: 0, top: 360, textAlign: "center" }}>
        <div style={{ fontFamily: MONO, fontWeight: 800, fontSize: 34, color, letterSpacing: 10, opacity: p(0.05, 0.15) }}>PART {String(n).padStart(2, "0")}</div>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 84, color: T.text, letterSpacing: -2, marginTop: 20, opacity: p(0.12, 0.24), transform: `translateY(${(1 - p(0.12, 0.24)) * 30}px)` }}>{title}</div>
        <div style={{ height: 5, width: interpolate(p(0.2, 0.5), [0, 1], [0, 440]), background: color, borderRadius: 3, margin: "26px auto" }} />
        <div style={{ fontFamily: SANS, fontSize: 32, color: T.muted, opacity: p(0.3, 0.45) }}>{sub}</div>
      </div>
      <div style={{ position: "absolute", left: 0, right: 0, top: 860, display: "flex", justifyContent: "center", gap: 10, opacity: p(0.3, 0.45) }}>
        {Array.from({ length: 12 }).map((_, i) => {
          const k = i + 1;
          return (
            <div key={k} style={{
              width: k === n ? 36 : 12, height: 12, borderRadius: 8,
              background: k <= n ? color : mix(T.panel, color, 0.15),
              border: `1.5px solid ${k <= n ? color : T.line}`,
              opacity: k === n ? 0.7 + Math.sin(frame * 0.1) * 0.3 : 1,
            }} />
          );
        })}
      </div>
    </Stage>
  );
};

type CardItem = { label: string; sub: string; c?: string };
const CardsScene: React.FC<{
  dur?: number; kicker?: string; title?: string; foot?: string; cols?: number; items?: CardItem[];
}> = ({ dur, kicker = "", title = "", foot = "", cols = 3, items = [] }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const n = items.length;
  const cN = cols === 4 ? 4 : cols === 2 ? 2 : 3;
  const w = cN === 4 ? 390 : cN === 2 ? 790 : 520;
  const gap = cN === 4 ? 430 : cN === 2 ? 860 : 560;
  const x0 = cN === 4 ? 130 : cN === 2 ? 130 : 140;
  const rows = Math.ceil(n / cN);
  const h = rows === 1 ? 420 : rows === 2 ? 250 : 190;
  const y0 = 230;
  const hot = Math.floor(frame / 26) % Math.max(1, n);
  return (
    <Stage>
      <Head theme={T} kicker={kicker} title={title} color={A.fruit} o={p(0, 0.06)} />
      <Petals o={0.18} n={10} />
      {items.map((it, i) => {
        const at = 0.08 + i * 0.07;
        const o = p(at, at + 0.08);
        const c = col(it.c);
        const x = x0 + (i % cN) * gap;
        const y = y0 + Math.floor(i / cN) * (h + 22);
        const active = hot === i && p(0.5, 0.51) > 0.4;
        return (
          <Card key={i} theme={T} x={x} y={y} w={w} h={h} color={c} o={o} glow={active}>
            <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 30, color: c, lineHeight: 1.2 }}>{it.label}</div>
            <div style={{ fontFamily: SANS, fontSize: 24, color: T.text, marginTop: 12, lineHeight: 1.35, width: "100%" }}>{it.sub}</div>
          </Card>
        );
      })}
      {foot ? <Foot theme={T} p={p(0.86, 0.94)}>{foot}</Foot> : null}
    </Stage>
  );
};

const CompareScene: React.FC<{
  dur?: number; kicker?: string; title?: string; foot?: string;
  leftTitle?: string; leftBody?: string; rightTitle?: string; rightBody?: string;
  leftC?: string; rightC?: string; vs?: string;
}> = ({
  dur, kicker = "DO NOT CONFUSE THESE", title = "Lagot is not wood apple",
  foot = "", leftTitle = "Lagot / loquat", leftBody = "", rightTitle = "Wood apple", rightBody = "",
  leftC = "fruit", rightC = "risk", vs = "NOT THE SAME TREE",
}) => {
  const p = useP(dur);
  const lc = col(leftC), rc = col(rightC);
  return (
    <Stage>
      <Head theme={T} kicker={kicker} title={title} color={A.risk} o={p(0, 0.06)} />
      <Card theme={T} x={130} y={240} w={760} h={540} color={lc} o={p(0.08, 0.18)} glow>
        <div style={{ fontFamily: MONO, fontSize: 22, color: lc, letterSpacing: 3 }}>THIS COURSE</div>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 40, color: T.text, marginTop: 10 }}>{leftTitle}</div>
        <div style={{ fontFamily: SANS, fontSize: 26, color: T.muted, marginTop: 18, lineHeight: 1.4, width: 680 }}>{leftBody}</div>
        <Cluster x={560} y={320} o={p(0.2, 0.3)} />
      </Card>
      <Card theme={T} x={1030} y={240} w={760} h={540} color={rc} o={p(0.22, 0.32)}>
        <div style={{ fontFamily: MONO, fontSize: 22, color: rc, letterSpacing: 3 }}>LOOKALIKE</div>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 40, color: T.text, marginTop: 10 }}>{rightTitle}</div>
        <div style={{ fontFamily: SANS, fontSize: 26, color: T.muted, marginTop: 18, lineHeight: 1.4, width: 680 }}>{rightBody}</div>
      </Card>
      <div style={{
        position: "absolute", left: 860, top: 460, width: 200, textAlign: "center",
        fontFamily: MONO, fontWeight: 800, fontSize: 22, color: A.risk, opacity: p(0.35, 0.45),
      }}>{vs}</div>
      <Flow x1={890} y1={520} x2={1030} y2={520} color={A.risk} n={5} o={p(0.3, 0.4)} />
      {foot ? <Foot theme={T} p={p(0.86, 0.94)}>{foot}</Foot> : null}
    </Stage>
  );
};

const OrbitScene: React.FC<{
  dur?: number; kicker?: string; title?: string; hub?: string; foot?: string;
  items?: { label: string; c?: string }[];
}> = ({ dur, kicker = "", title = "", hub = "LAGOT", foot = "", items = [] }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const n = Math.max(1, items.length);
  const hot = Math.floor(frame / 26) % n;
  return (
    <Stage>
      <Head theme={T} kicker={kicker} title={title} color={A.fruit} o={p(0, 0.06)} />
      <div style={{
        position: "absolute", left: 810, top: 470, width: 300, height: 160, borderRadius: 24,
        background: mix(T.panel, A.fruit, 0.18), border: `3px solid ${A.fruit}`,
        display: "flex", alignItems: "center", justifyContent: "center",
        fontFamily: SANS, fontWeight: 800, fontSize: 36, color: A.fruit, textAlign: "center",
        boxShadow: `0 0 ${40 + Math.sin(frame * 0.06) * 16}px ${mix(T.bg0, A.fruit, 0.5)}`,
        opacity: p(0.06, 0.14),
      }}>{hub}</div>
      {items.map((it, i) => {
        const ang = (i / n) * Math.PI * 2 - Math.PI / 2 + Math.sin(frame * 0.008) * 0.06;
        const x = 960 + Math.cos(ang) * 560, y = 555 + Math.sin(ang) * 250;
        const at = 0.1 + i * 0.07;
        const active = hot === i && p(0.5, 0.51) > 0.4;
        const c = col(it.c);
        return (
          <React.Fragment key={i}>
            <Wire x1={960} y1={550} x2={x} y2={y} p={p(at, at + 0.06)} color={active ? c : mix(T.muted, T.bg1, 0.4)} w={active ? 3 : 2} arrow={false} />
            <div style={{
              position: "absolute", left: x - 150, top: y - 44, width: 300, height: 88, borderRadius: 16,
              background: mix(T.panel, active ? c : A.fruit, active ? 0.2 : 0.08),
              border: `2.5px solid ${active ? c : mix(T.line, A.fruit, 0.5)}`,
              display: "flex", alignItems: "center", justifyContent: "center",
              fontFamily: SANS, fontWeight: 700, fontSize: 24, color: T.text, textAlign: "center", padding: "0 12px", boxSizing: "border-box",
              opacity: p(at, at + 0.08), transform: `scale(${active ? 1.08 : 1})`,
            }}>{it.label}</div>
          </React.Fragment>
        );
      })}
      {foot ? <Foot theme={T} p={p(0.86, 0.94)}>{foot}</Foot> : null}
    </Stage>
  );
};

const STATES = [
  { k: "Punjab", x: 430, y: 280, on: true },
  { k: "H.P.", x: 560, y: 220, on: true },
  { k: "Delhi", x: 520, y: 340, on: true },
  { k: "U.P.", x: 700, y: 360, on: true },
  { k: "Assam", x: 1180, y: 340, on: true },
  { k: "Maharashtra", x: 560, y: 620, on: true },
  { k: "T.N. hills", x: 680, y: 780, on: false },
  { k: "Karnataka", x: 540, y: 740, on: false },
];

const MapScene: React.FC<{ dur?: number; kicker?: string; title?: string; foot?: string }> = ({
  dur, kicker = "WHERE IT FRUITS", title = "India grows it in cool-winter belts", foot = "",
}) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const hot = Math.floor(frame / 24) % STATES.length;
  return (
    <Stage>
      <Head theme={T} kicker={kicker} title={title} color={A.cool} o={p(0, 0.06)} />
      <div style={{
        position: "absolute", left: 280, top: 200, width: 920, height: 620, borderRadius: 28,
        background: mix(T.panel, A.cool, 0.08), border: `2px solid ${T.line}`, opacity: p(0.06, 0.12),
      }} />
      {STATES.map((s, i) => {
        const at = 0.1 + i * 0.07;
        const o = p(at, at + 0.08);
        const c = s.on ? A.leaf : A.risk;
        const active = hot === i;
        return (
          <div key={s.k} style={{
            position: "absolute", left: s.x, top: s.y, opacity: o,
            padding: "10px 18px", borderRadius: 999,
            background: active ? c : mix(T.panel, c, 0.2),
            border: `2px solid ${c}`,
            fontFamily: MONO, fontWeight: 800, fontSize: 22, color: active ? T.bg0 : c,
            transform: `scale(${active ? 1.08 : 1})`,
          }}>{s.k}{s.on ? "" : " · ornamental"}</div>
        );
      })}
      <Card theme={T} x={1240} y={240} w={540} h={500} color={A.cool} o={p(0.2, 0.3)}>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 32, color: A.cool }}>Fruiting belt</div>
        <div style={{ fontFamily: SANS, fontSize: 26, color: T.text, marginTop: 16, lineHeight: 1.4 }}>
          Punjab, Himachal, Delhi, Uttar Pradesh, Assam, pockets of Maharashtra.
        </div>
        <div style={{ fontFamily: SANS, fontSize: 26, color: A.risk, marginTop: 22, lineHeight: 1.4 }}>
          Warm-winter south: trees live, crop often fails.
        </div>
        <div style={{ fontFamily: MONO, fontSize: 22, color: T.muted, marginTop: 28 }}>
          China is the world crop. India is a niche.
        </div>
      </Card>
      {foot ? <Foot theme={T} p={p(0.86, 0.94)}>{foot}</Foot> : null}
    </Stage>
  );
};

const MONTHS = ["JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC", "JAN", "FEB", "MAR", "APR", "MAY"];
const CalendarScene: React.FC<{
  dur?: number; kicker?: string; title?: string; foot?: string;
  bands?: { label: string; from: number; to: number; c?: string }[];
}> = ({
  dur, kicker = "THE FARM YEAR", title = "One crop, one short harvest",
  foot = "",
  bands = [
    { label: "Plant / graft", from: 0, to: 3, c: "leaf" },
    { label: "Useful flower", from: 4, to: 8, c: "cool" },
    { label: "Harvest", from: 9, to: 10, c: "fruit" },
    { label: "Prune", from: 11, to: 11, c: "risk" },
  ],
}) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const hot = Math.floor(frame / 18) % 12;
  return (
    <Stage>
      <Head theme={T} kicker={kicker} title={title} color={A.fruit} o={p(0, 0.06)} />
      {MONTHS.map((m, i) => (
        <div key={m} style={{
          position: "absolute", left: 110 + i * 141, top: 230, width: 128, height: 70, borderRadius: 12,
          background: hot === i ? A.fruit : mix(T.panel, A.fruit, 0.1),
          border: `2px solid ${A.fruit}`,
          display: "flex", alignItems: "center", justifyContent: "center",
          fontFamily: MONO, fontWeight: 800, fontSize: 22, color: hot === i ? T.bg0 : A.fruit,
          opacity: p(0.06, 0.14),
        }}>{m}</div>
      ))}
      {bands.map((b, i) => {
        const at = 0.18 + i * 0.14;
        const o = p(at, at + 0.1);
        const c = col(b.c);
        const x = 110 + b.from * 141;
        const w = (b.to - b.from + 1) * 141 - 13;
        return (
          <div key={i} style={{
            position: "absolute", left: x, top: 340 + i * 110, width: w, height: 88, borderRadius: 16,
            background: mix(T.panel, c, 0.2), border: `2.5px solid ${c}`, opacity: o,
            display: "flex", alignItems: "center", padding: "0 24px",
            fontFamily: SANS, fontWeight: 800, fontSize: 30, color: T.text,
          }}>{b.label}</div>
        );
      })}
      {foot ? <Foot theme={T} p={p(0.86, 0.94)}>{foot}</Foot> : null}
    </Stage>
  );
};

const TimelineScene: React.FC<{
  dur?: number; kicker?: string; title?: string; foot?: string;
  steps?: { y: string; label: string; sub: string; c?: string }[];
}> = ({ dur, kicker = "", title = "", foot = "", steps = [] }) => {
  const frame = useCurrentFrame();
  const p = usePfull(dur);
  const n = steps.length;
  const fill = p(0.08, 0.85);
  return (
    <Stage>
      <Head theme={T} kicker={kicker} title={title} color={A.leaf} o={p(0, 0.06)} />
      <div style={{ position: "absolute", left: 180, top: 430, width: 1560, height: 6, background: T.line, borderRadius: 3 }} />
      <div style={{ position: "absolute", left: 180, top: 430, width: 1560 * fill, height: 6, background: `linear-gradient(90deg, ${A.leaf}, ${A.fruit})`, borderRadius: 3, boxShadow: `0 0 12px ${A.fruit}` }} />
      {steps.map((s, i) => {
        const at = 0.1 + i * (0.7 / Math.max(1, n));
        const o = p(at, at + 0.08);
        const x = 120 + i * (n <= 1 ? 0 : 350);
        const c = col(s.c);
        const up = i % 2 === 0;
        return (
          <div key={i} style={{ position: "absolute", left: x, top: up ? 250 : 470, width: 260, opacity: o }}>
            <div style={{ fontFamily: MONO, fontWeight: 800, fontSize: 26, color: c }}>{s.y}</div>
            <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 28, color: T.text, marginTop: 6 }}>{s.label}</div>
            <div style={{ fontFamily: SANS, fontSize: 22, color: T.muted, marginTop: 6, lineHeight: 1.3 }}>{s.sub}</div>
            <div style={{
              position: "absolute", left: 8, top: up ? 168 : -28, width: 16, height: 16, borderRadius: 8,
              background: c, boxShadow: `0 0 ${10 + Math.sin(frame * 0.08 + i) * 6}px ${c}`,
            }} />
          </div>
        );
      })}
      {foot ? <Foot theme={T} p={p(0.88, 0.95)}>{foot}</Foot> : null}
    </Stage>
  );
};

const BarsScene: React.FC<{
  dur?: number; kicker?: string; title?: string; foot?: string; unit?: string;
  bars?: { label: string; v: number; c?: string }[];
}> = ({ dur, kicker = "", title = "", foot = "", unit = "", bars = [] }) => {
  const p = useP(dur);
  const max = Math.max(1, ...bars.map((b) => b.v));
  return (
    <Stage>
      <Head theme={T} kicker={kicker} title={title} color={A.fruit} o={p(0, 0.06)} />
      {bars.map((b, i) => {
        const grow = p(0.1 + i * 0.1, 0.22 + i * 0.1);
        const h = (b.v / max) * 420 * grow;
        const c = col(b.c);
        const x = 220 + i * 280;
        return (
          <div key={i}>
            <div style={{
              position: "absolute", left: x, top: 740 - h, width: 160, height: h,
              borderRadius: "12px 12px 0 0",
              background: `linear-gradient(180deg, ${c}, ${mix(c, T.bg1, 0.45)})`,
              border: `2px solid ${c}`, borderBottom: "none",
            }} />
            <div style={{
              position: "absolute", left: x - 20, top: 740 - h - 48, width: 200, textAlign: "center",
              fontFamily: MONO, fontWeight: 800, fontSize: 28, color: c, opacity: grow,
            }}>{b.v}{unit}</div>
            <div style={{
              position: "absolute", left: x - 30, top: 756, width: 220, textAlign: "center",
              fontFamily: SANS, fontSize: 22, color: T.muted, opacity: p(0.12, 0.2),
            }}>{b.label}</div>
          </div>
        );
      })}
      {foot ? <Foot theme={T} p={p(0.86, 0.94)}>{foot}</Foot> : null}
    </Stage>
  );
};

const TableScene: React.FC<{
  dur?: number; kicker?: string; title?: string; foot?: string;
  cols?: string[]; rows?: string[][];
}> = ({ dur, kicker = "", title = "", foot = "", cols = [], rows = [] }) => {
  const p = useP(dur);
  const cw = Math.min(400, Math.floor(1600 / Math.max(1, cols.length)));
  return (
    <Stage>
      <Head theme={T} kicker={kicker} title={title} color={A.leaf} o={p(0, 0.06)} />
      <div style={{ position: "absolute", left: 140, top: 230, display: "flex", gap: 0 }}>
        {cols.map((c, i) => (
          <div key={i} style={{
            width: cw, padding: "16px 18px", fontFamily: MONO, fontWeight: 800, fontSize: 22, color: A.leaf,
            borderBottom: `2px solid ${A.leaf}`, opacity: p(0.06, 0.14),
          }}>{c}</div>
        ))}
      </div>
      {rows.map((row, r) => {
        const at = 0.12 + r * 0.1;
        const o = p(at, at + 0.08);
        return (
          <div key={r} style={{ position: "absolute", left: 140, top: 300 + r * 88, display: "flex", opacity: o }}>
            {row.map((cell, i) => (
              <div key={i} style={{
                width: cw, padding: "18px 18px", fontFamily: SANS, fontSize: 24, color: T.text,
                background: mix(T.panel, A.leaf, r % 2 ? 0.06 : 0.12),
                borderBottom: `1px solid ${T.line}`,
              }}>{cell}</div>
            ))}
          </div>
        );
      })}
      {foot ? <Foot theme={T} p={p(0.86, 0.94)}>{foot}</Foot> : null}
    </Stage>
  );
};

const PipelineScene: React.FC<{
  dur?: number; kicker?: string; title?: string; foot?: string;
  nodes?: { label: string; sub: string; c?: string }[];
}> = ({ dur, kicker = "", title = "", foot = "", nodes = [] }) => {
  const p = useP(dur);
  const n = nodes.length;
  const w = n >= 5 ? 290 : 340;
  const step = n >= 5 ? 350 : 420;
  const x0 = n >= 5 ? 130 : 160;
  return (
    <Stage>
      <Head theme={T} kicker={kicker} title={title} color={A.fruit} o={p(0, 0.06)} />
      {nodes.map((nd, i) => {
        const at = 0.08 + i * 0.12;
        const c = col(nd.c);
        const x = x0 + i * step;
        return (
          <React.Fragment key={i}>
            {i > 0 && (
              <>
                <Wire x1={x0 + (i - 1) * step + w} y1={500} x2={x} y2={500} p={p(at - 0.06, at)} color={c} w={3} />
                <Flow x1={x0 + (i - 1) * step + w} y1={500} x2={x} y2={500} color={c} n={5} o={p(at + 0.02, at + 0.1)} />
              </>
            )}
            <Card theme={T} x={x} y={380} w={w} h={240} color={c} o={p(at, at + 0.09)} glow={i === n - 1}>
              <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 28, color: c }}>{nd.label}</div>
              <div style={{ fontFamily: SANS, fontSize: 22, color: T.muted, marginTop: 12, lineHeight: 1.3 }}>{nd.sub}</div>
            </Card>
          </React.Fragment>
        );
      })}
      {foot ? <Foot theme={T} p={p(0.86, 0.94)}>{foot}</Foot> : null}
    </Stage>
  );
};

const OrchardScene: React.FC<{ dur?: number; kicker?: string; title?: string; foot?: string }> = ({
  dur, kicker = "COMPUTED LAYOUT", title = "Ninety-six trees on one acre", foot = "",
}) => {
  const frame = useCurrentFrame();
  const p = usePfull(dur);
  const cols = 12, rows = 8;
  const year = Math.min(15, Math.floor(p(0.15, 0.8) * 16));
  const wave = (frame * 0.12) % (cols + 4);
  return (
    <Stage>
      <Head theme={T} kicker={kicker} title={title} color={A.leaf} o={p(0, 0.06)} />
      {Array.from({ length: rows * cols }).map((_, i) => {
        const r = Math.floor(i / cols), c = i % cols;
        const bearing = year >= 3;
        const heat = Math.max(0, 1 - Math.abs(c - wave) / 2.4);
        const x = 140 + c * 108, y = 230 + r * 68;
        return (
          <div key={i} style={{
            position: "absolute", left: x, top: y, width: 88, height: 56, borderRadius: 10,
            background: mix(T.panel, bearing ? A.fruit : A.leaf, 0.12 + heat * 0.35),
            border: `1.5px solid ${bearing ? A.fruit : A.leaf}`,
            transform: `scale(${1 + heat * 0.08})`,
            display: "flex", alignItems: "center", justifyContent: "center",
            fontSize: 22,
          }}>{bearing ? "●" : "·"}</div>
        );
      })}
      <div style={{
        position: "absolute", left: 1480, top: 260, width: 300,
        fontFamily: MONO, fontWeight: 800, fontSize: 28, color: A.fruit, opacity: p(0.12, 0.2),
      }}>
        year {year}
        <div style={{ fontFamily: SANS, fontSize: 24, color: T.muted, fontWeight: 400, marginTop: 12 }}>
          {year < 3 ? "green wood only" : year < 7 ? "first crop years" : "commercial bearing"}
        </div>
        <div style={{ fontFamily: MONO, fontSize: 22, color: A.leaf, marginTop: 18 }}>6–7 m grid</div>
        <div style={{ fontFamily: MONO, fontSize: 22, color: A.cool, marginTop: 8 }}>96 trees / acre</div>
      </div>
      {foot ? <Foot theme={T} p={p(0.86, 0.94)}>{foot}</Foot> : null}
    </Stage>
  );
};

const YieldScene: React.FC<{ dur?: number; kicker?: string; title?: string; foot?: string }> = ({
  dur, kicker = "RUN THE YIELD", title = "Two honest acre curves", foot = "",
}) => {
  const p = usePfull(dur);
  const idx = Math.min(YIELD.length - 1, Math.floor(p(0.12, 0.82) * YIELD.length));
  const row = YIELD[idx];
  const ptsC = YIELD.map((r, i) => `${180 + (i / 20) * 1100},${720 - (r.cons / 2700) * 400}`);
  const ptsG = YIELD.map((r, i) => `${180 + (i / 20) * 1100},${720 - (r.good / 2700) * 400}`);
  const cut = Math.max(2, idx + 1);
  return (
    <Stage>
      <Head theme={T} kicker={kicker} title={title} color={A.fruit} o={p(0, 0.06)} />
      <svg style={{ position: "absolute", left: 0, top: 0 }} width={1920} height={1080}>
        <polyline points={ptsC.slice(0, cut).join(" ")} fill="none" stroke={A.risk} strokeWidth={4} />
        <polyline points={ptsG.slice(0, cut).join(" ")} fill="none" stroke={A.leaf} strokeWidth={5} />
      </svg>
      <div style={{ position: "absolute", left: 1360, top: 260, width: 420 }}>
        <div style={{ fontFamily: MONO, fontSize: 22, color: T.muted }}>year {row.y}</div>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 36, color: A.risk, marginTop: 16 }}>
          leaflet {row.cons} kg
        </div>
        <div style={{ fontFamily: SANS, fontSize: 22, color: T.muted }}>8 kg/tree ramp · ~7 qtl at peak</div>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 36, color: A.leaf, marginTop: 28 }}>
          managed {row.good} kg
        </div>
        <div style={{ fontFamily: SANS, fontSize: 22, color: T.muted }}>28 kg/tree ramp · PAU-class trees</div>
      </div>
      {foot ? <Foot theme={T} p={p(0.86, 0.94)}>{foot}</Foot> : null}
    </Stage>
  );
};

const CashScene: React.FC<{ dur?: number; kicker?: string; title?: string; foot?: string }> = ({
  dur, kicker = "COMPUTED CASH", title = "Cumulative rupees, two stories", foot = "",
}) => {
  const p = usePfull(dur);
  const idx = Math.min(CASH.length - 1, Math.max(0, Math.floor(p(0.12, 0.82) * CASH.length)));
  const row = CASH[idx];
  const min = -200000, max = 2500000;
  const ny = (v: number) => 700 - ((v - min) / (max - min)) * 420;
  const ptsC = CASH.map((r, i) => `${200 + (i / 20) * 1000},${ny(r.cons)}`);
  const ptsG = CASH.map((r, i) => `${200 + (i / 20) * 1000},${ny(r.good)}`);
  const cut = Math.max(2, idx + 1);
  const y0 = ny(0);
  return (
    <Stage>
      <Head theme={T} kicker={kicker} title={title} color={A.cool} o={p(0, 0.06)} />
      <svg style={{ position: "absolute", left: 0, top: 0 }} width={1920} height={1080}>
        <line x1={200} y1={y0} x2={1200} y2={y0} stroke={T.line} strokeWidth={2} strokeDasharray="8 8" />
        <polyline points={ptsC.slice(0, cut).join(" ")} fill="none" stroke={A.risk} strokeWidth={4} />
        <polyline points={ptsG.slice(0, cut).join(" ")} fill="none" stroke={A.ok} strokeWidth={5} />
      </svg>
      <div style={{ position: "absolute", left: 1280, top: 250, width: 500 }}>
        <div style={{ fontFamily: MONO, fontSize: 22, color: T.muted }}>end of year {row.y}</div>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 34, color: row.cons >= 0 ? A.ok : A.risk, marginTop: 18 }}>
          conservative {row.cons >= 0 ? "+" : ""}{(row.cons / 1000).toFixed(0)}k
        </div>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 34, color: row.good >= 0 ? A.ok : A.risk, marginTop: 14 }}>
          managed {row.good >= 0 ? "+" : ""}{(row.good / 1000).toFixed(0)}k
        </div>
        <div style={{ fontFamily: SANS, fontSize: 22, color: T.muted, marginTop: 22, lineHeight: 1.35 }}>
          Model: 90k establish, 28k a year, 80 vs 120 rupees a kilo. Not a promise.
        </div>
      </div>
      {foot ? <Foot theme={T} p={p(0.86, 0.94)}>{foot}</Foot> : null}
    </Stage>
  );
};

const TowerScene: React.FC<{
  dur?: number; kicker?: string; title?: string; foot?: string;
  segs?: { label: string; h: number; c?: string }[];
  cap?: string;
}> = ({ dur, kicker = "", title = "", foot = "", segs = [], cap = "" }) => {
  const p = useP(dur);
  return (
    <Stage>
      <Head theme={T} kicker={kicker} title={title} color={A.cool} o={p(0, 0.06)} />
      <div style={{
        position: "absolute", left: 240, top: 230, width: 520, height: 560, borderRadius: 18,
        border: `2.5px solid ${T.line}`, background: T.panel, display: "flex", flexDirection: "column-reverse", overflow: "hidden",
        opacity: p(0.08, 0.16),
      }}>
        {segs.map((s, i) => (
          <div key={i} style={{
            height: s.h * p(0.12 + i * 0.12, 0.24 + i * 0.12),
            background: `linear-gradient(90deg, ${mix(T.panel, col(s.c), 0.75)}, ${mix(T.panel, col(s.c), 0.4)})`,
            borderTop: `2px solid ${col(s.c)}`, display: "flex", alignItems: "center", paddingLeft: 18,
            fontFamily: MONO, fontSize: 22, color: T.text, whiteSpace: "nowrap",
          }}>{s.label}</div>
        ))}
      </div>
      <div style={{
        position: "absolute", left: 840, top: 300, width: 880, fontFamily: SANS, fontSize: 30, color: T.text, lineHeight: 1.4,
        opacity: p(0.3, 0.42),
      }}>{cap}</div>
      {foot ? <Foot theme={T} p={p(0.86, 0.94)}>{foot}</Foot> : null}
    </Stage>
  );
};

const DecideScene: React.FC<{
  dur?: number; kicker?: string; title?: string; foot?: string;
  go?: string[]; no?: string[];
}> = ({ dur, kicker = "THE VERDICT", title = "Plant only if the land fits", foot = "", go = [], no = [] }) => {
  const p = useP(dur);
  return (
    <Stage>
      <Head theme={T} kicker={kicker} title={title} color={A.ok} o={p(0, 0.06)} />
      <Card theme={T} x={130} y={230} w={800} h={560} color={A.ok} o={p(0.08, 0.16)}>
        <div style={{ fontFamily: MONO, fontWeight: 800, fontSize: 26, color: A.ok }}>PLANT IF</div>
        {go.map((g, i) => (
          <div key={i} style={{ fontFamily: SANS, fontSize: 26, color: T.text, marginTop: 16, opacity: p(0.16 + i * 0.08, 0.24 + i * 0.08), lineHeight: 1.3 }}>• {g}</div>
        ))}
      </Card>
      <Card theme={T} x={990} y={230} w={800} h={560} color={A.risk} o={p(0.14, 0.22)}>
        <div style={{ fontFamily: MONO, fontWeight: 800, fontSize: 26, color: A.risk }}>SKIP IF</div>
        {no.map((g, i) => (
          <div key={i} style={{ fontFamily: SANS, fontSize: 26, color: T.text, marginTop: 16, opacity: p(0.22 + i * 0.08, 0.3 + i * 0.08), lineHeight: 1.3 }}>• {g}</div>
        ))}
      </Card>
      {foot ? <Foot theme={T} p={p(0.86, 0.94)}>{foot}</Foot> : null}
    </Stage>
  );
};

const AnatomyScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur);
  const bits = [
    { k: "Skin", d: "thin, eat or peel", x: 1080, y: 260, c: A.fruit },
    { k: "Flesh", d: "sweet-sour, juicy", x: 1080, y: 400, c: A.leaf },
    { k: "Seeds", d: "few large stones", x: 1080, y: 540, c: A.cool },
    { k: "Cluster", d: "pick the whole bunch", x: 1080, y: 680, c: A.risk },
  ];
  return (
    <Stage>
      <Head theme={T} kicker="THE FRUIT" title="What you are actually selling" color={A.fruit} o={p(0, 0.06)} />
      <div style={{
        position: "absolute", left: 280, top: 280, width: 520, height: 480, borderRadius: "50% 50% 48% 48%",
        background: `radial-gradient(circle at 40% 35%, ${mix(A.fruit, "#fff", 0.35)}, ${A.fruit} 55%, ${mix(A.fruit, T.bg0, 0.4)})`,
        border: `4px solid ${A.fruit}`, opacity: p(0.08, 0.16),
        boxShadow: `0 0 50px ${mix(T.bg0, A.fruit, 0.5)}`,
      }} />
      <Cluster x={480} y={420} n={8} o={p(0.1, 0.2)} ripe={p(0.2, 0.7)} />
      {bits.map((b, i) => {
        const at = 0.18 + i * 0.12;
        return (
          <div key={b.k} style={{ position: "absolute", left: b.x, top: b.y, opacity: p(at, at + 0.08) }}>
            <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 34, color: b.c }}>{b.k}</div>
            <div style={{ fontFamily: SANS, fontSize: 24, color: T.muted, marginTop: 6 }}>{b.d}</div>
          </div>
        );
      })}
      <Wire x1={780} y1={480} x2={1060} y2={420} p={p(0.2, 0.28)} color={A.fruit} w={2} />
      <Foot theme={T} p={p(0.86, 0.94)}>Dessert fruit first. Processing second. Medicine last — and unproven as a farm plan.</Foot>
    </Stage>
  );
};

const RecapScene: React.FC<{ dur?: number; items?: string[]; closer?: string }> = ({
  dur, items = [], closer = "Cool winters. Grafted plants. Year three. A short, perishable crop.",
}) => {
  const frame = useCurrentFrame();
  const p = usePfull(dur);
  return (
    <AbsoluteFill style={{ padding: "70px 130px", justifyContent: "center" }}>
      <Petals o={0.25} n={12} />
      <div style={{ opacity: p(0, 0.06), textAlign: "center", marginBottom: 24 }}>
        <Kicker theme={T} text="RECAP — THE WHOLE MAP" cx />
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 56, color: T.text, marginTop: 10, letterSpacing: -1.5 }}>Lagot in one breath</div>
      </div>
      <div style={{ display: "flex", flexDirection: "column", gap: 12, maxWidth: 1400, margin: "0 auto", width: "100%" }}>
        {items.map((it, i) => {
          const at = 0.06 + i * 0.09;
          const o = p(at, at + 0.07);
          return (
            <div key={i} style={{
              display: "flex", alignItems: "center", gap: 18, opacity: o, transform: `translateX(${(1 - o) * -26}px)`,
              background: mix(T.panel, A.fruit, 0.05), border: `1.5px solid ${T.line}`, borderLeft: `4px solid ${A.fruit}`,
              borderRadius: 12, padding: "14px 26px",
            }}>
              <span style={{ color: A.fruit, fontFamily: MONO, fontWeight: 700, fontSize: 24 }}>{i + 1}</span>
              <span style={{ fontFamily: SANS, fontSize: 28, color: T.text, lineHeight: 1.25 }}>{it}</span>
            </div>
          );
        })}
      </div>
      <div style={{ textAlign: "center", marginTop: 28, opacity: p(0.82, 0.92) }}>
        <div style={{
          fontFamily: SANS, fontWeight: 800, fontStyle: "italic", fontSize: 36, color: A.fruit,
          textShadow: `0 0 ${28 + Math.sin(frame * 0.06) * 14}px ${mix(T.bg0, A.fruit, 0.7)}`,
        }}>{closer}</div>
      </div>
    </AbsoluteFill>
  );
};

const ACCENT: Record<string, string> = {
  lag_title: A.fruit, lag_roadmap: A.leaf, lag_divider: A.fruit, lag_cards: A.fruit,
  lag_compare: A.risk, lag_orbit: A.fruit, lag_map: A.cool, lag_cal: A.fruit,
  lag_time: A.leaf, lag_bars: A.fruit, lag_table: A.leaf, lag_pipe: A.fruit,
  lag_orchard: A.leaf, lag_yield: A.fruit, lag_cash: A.cool, lag_tower: A.cool,
  lag_decide: A.ok, lag_anatomy: A.fruit, lag_recap: A.fruit,
};

export const LagScene: React.FC<{ variant: string;[key: string]: unknown }> = ({ variant, ...rest }) => {
  const r = rest as Record<string, unknown>;
  let content: React.ReactNode;
  switch (variant) {
    case "lag_title": content = <TitleScene {...r} />; break;
    case "lag_roadmap": content = <RoadmapScene {...r} />; break;
    case "lag_divider": content = <Divider {...r} />; break;
    case "lag_cards": content = <CardsScene {...r} />; break;
    case "lag_compare": content = <CompareScene {...r} />; break;
    case "lag_orbit": content = <OrbitScene {...r} />; break;
    case "lag_map": content = <MapScene {...r} />; break;
    case "lag_cal": content = <CalendarScene {...r} />; break;
    case "lag_time": content = <TimelineScene {...r} />; break;
    case "lag_bars": content = <BarsScene {...r} />; break;
    case "lag_table": content = <TableScene {...r} />; break;
    case "lag_pipe": content = <PipelineScene {...r} />; break;
    case "lag_orchard": content = <OrchardScene {...r} />; break;
    case "lag_yield": content = <YieldScene {...r} />; break;
    case "lag_cash": content = <CashScene {...r} />; break;
    case "lag_tower": content = <TowerScene {...r} />; break;
    case "lag_decide": content = <DecideScene {...r} />; break;
    case "lag_anatomy": content = <AnatomyScene {...r} />; break;
    case "lag_recap": content = <RecapScene {...r} />; break;
    default: content = <TitleScene {...r} />;
  }
  const accent = (typeof r.color === "string" ? r.color : ACCENT[variant]) || A.fruit;
  return (
    <AbsoluteFill>
      <Bg theme={T} accent={accent} />
      {content}
      <SceneProgress accent={accent} dur={r.dur as number} />
    </AbsoluteFill>
  );
};

export default LagScene;
