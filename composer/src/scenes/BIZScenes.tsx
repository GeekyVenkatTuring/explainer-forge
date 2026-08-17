/**
 * BIZScenes.tsx — "Business ideas under ₹25 lakh" Telugu course (prefix `biz`).
 *
 * Identity (skills/04):
 *   theme accent = growth emerald (#22C55E). Semantic accents (colors MEAN things):
 *     invest  sky    #38BDF8 — पेट्टుबడి / capex / capital going IN
 *     money   gold   #FBBF24 — revenue, ₹ per unit, fees, sales
 *     grow    emeral #34D399 — profit / margin / payback / the good outcome
 *     risk    rose   #FB7185 — risk, competition, thin margins, the warning
 *     idea    violet #A78BFA — the idea / concept / people / service
 *   Recurring motif: a rising growth staircase + orbiting ₹/🌱/📈 (GrowMotif) — a small
 *   business compounding upward. Appears in title, chapter titles, dividers, recap.
 *
 * Telugu long-form rules (skills/11): NO letterSpacing on Telugu (kickers are LATIN),
 * first skeleton visible by p≈0.06, content fills the vertical band (captions ON → design
 * to y≈880, no Foot), Telugu ≥ 23px, lineHeight ≥ 1.35, mix() gets HEX only.
 * Brands / ₹ amounts / %/ numbers stay Latin on screen. Educational — not financial advice.
 */
import React from "react";
import { AbsoluteFill, interpolate, useCurrentFrame } from "remotion";
import {
  makeTheme, mix, useP, usePop, rnd, MONO, SANS,
  Bg, Stage, Kicker, Card, Flow, Wire, Counter, Brackets, ScanBeam,
} from "../lib/primitives";

const T = makeTheme({ accent: "#22C55E", bg0: "#080B09", bg1: "#0C120E", bg2: "#16241C", panel: "#101B14" });
const A = { invest: "#38BDF8", money: "#FBBF24", grow: "#34D399", risk: "#FB7185", idea: "#A78BFA" };

// BIZHead — Telugu-safe header: Latin kicker (tracked), Telugu title untracked.
const BIZHead: React.FC<{ kicker: string; title: string; color?: string; o?: number }> = ({
  kicker, title, color, o = 1,
}) => (
  <div style={{ position: "absolute", left: 100, top: 54, right: 100 }}>
    <Kicker theme={T} text={kicker} color={color} o={o} />
    <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 52, color: T.text, marginTop: 12, letterSpacing: 0, opacity: o }}>{title}</div>
  </div>
);

// ---------------------------------------------------------------- motif
/** GrowMotif: a small rising staircase of bars with orbiting ₹ / 🌱 / 📈 markers. */
const GrowMotif: React.FC<{ x: number; y: number; r: number; o?: number; dim?: boolean }> = ({
  x, y, r, o = 1, dim,
}) => {
  const frame = useCurrentFrame();
  const rot = frame * 0.6;
  const marks = ["₹", "🌱", "📈", "🪙"];
  const bars = [0.4, 0.6, 0.8, 1.0];
  return (
    <div style={{ position: "absolute", left: 0, top: 0, opacity: o * (dim ? 0.4 : 1), pointerEvents: "none" }}>
      <svg width={1920} height={1080} style={{ position: "absolute", left: 0, top: 0, overflow: "visible" }}>
        <circle cx={x} cy={y} r={r} fill="none" stroke={mix(T.bg2, A.grow, 0.5)} strokeWidth={2}
          strokeDasharray={`${Math.PI * r * 0.5} ${Math.PI * r * 0.5}`} strokeDashoffset={-rot} opacity={0.6} />
        {/* rising bars inside */}
        {bars.map((h, i) => (
          <rect key={i} x={x - 46 + i * 26} y={y + 30 - h * 60} width={18} height={h * 60}
            rx={3} fill={i === bars.length - 1 ? A.grow : mix(A.invest, A.grow, i / 3)} opacity={0.8} />
        ))}
      </svg>
      {marks.map((m, i) => {
        const ang = (rot * 0.017) + (i / marks.length) * Math.PI * 2;
        return (
          <div key={i} style={{ position: "absolute", left: x + Math.cos(ang) * r - 16, top: y + Math.sin(ang) * r - 20,
            fontFamily: SANS, fontWeight: 800, fontSize: 34, color: A.money }}>{m}</div>
        );
      })}
    </div>
  );
};

// ---------------------------------------------------------------- biz_title
const TitleScene: React.FC<{ dur?: number; k?: string; l1?: string; l2?: string; sub?: string }> = ({
  dur,
  k = "SMALL-BUSINESS COURSE · 2026",
  l1 = "₹25 లక్షల లోపు వ్యాపారాలు",
  l2 = "10 ఆలోచనలు — A to Z",
  sub = "పెట్టుబడి · మార్జిన్ · లైసెన్సులు · రిస్క్ — పూర్తి వివరాలతో",
}) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const pop = usePop(dur);
  return (
    <AbsoluteFill style={{ alignItems: "center", justifyContent: "center" }}>
      <GrowMotif x={320} y={770} r={150} o={p(0.08, 0.22)} dim />
      <GrowMotif x={1600} y={250} r={120} o={p(0.14, 0.28)} dim />
      {/* rising ₹ sparks */}
      {Array.from({ length: 12 }).map((_, i) => {
        const t = ((frame * (0.6 + rnd(i, 2) * 0.6) + i * 90) % 700) / 700;
        return (
          <div key={i} style={{ position: "absolute", left: 200 + rnd(i, 5) * 1520,
            top: 900 - t * 780, fontFamily: MONO, fontWeight: 800, fontSize: 18,
            color: i % 2 ? A.grow : A.money, opacity: (1 - t) * 0.35, textShadow: `0 0 12px ${i % 2 ? A.grow : A.money}` }}>▲</div>
        );
      })}
      <div style={{ textAlign: "center", transform: `scale(${0.92 + pop(0) * 0.08})`, zIndex: 2 }}>
        <div style={{ display: "flex", justifyContent: "center", marginBottom: 26 }}>
          <Kicker theme={T} text={k} cx />
        </div>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 100, lineHeight: 1.08, letterSpacing: 0, color: T.text }}>
          <div>{l1}</div>
          <div style={{ color: A.grow, textShadow: `0 0 70px ${mix(T.bg0, A.grow, 0.7)}` }}>{l2}</div>
        </div>
        <div style={{ height: 6, width: interpolate(p(0.18, 0.45), [0, 1], [0, 640]), background: `linear-gradient(90deg, ${A.invest}, ${A.grow})`, borderRadius: 3, margin: "30px auto" }} />
        <div style={{ fontFamily: SANS, fontSize: 34, color: T.muted, opacity: p(0.28, 0.5), lineHeight: 1.4 }}>
          {sub}
        </div>
      </div>
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------- biz_ptitle
const PTitleScene: React.FC<{ dur?: number; title?: string; sub?: string; kicker?: string; emoji?: string }> = ({
  dur, title = "", sub = "", kicker = "CHAPTER", emoji = "",
}) => {
  const p = useP(dur);
  const pop = usePop(dur);
  return (
    <AbsoluteFill style={{ alignItems: "center", justifyContent: "center" }}>
      {/* motifs kept off-center so the orbit/bars never cross the centered title text */}
      <GrowMotif x={300} y={790} r={150} o={p(0.1, 0.3)} dim />
      <GrowMotif x={1620} y={250} r={120} o={p(0.16, 0.34)} dim />
      <div style={{ textAlign: "center", transform: `scale(${0.94 + pop(0) * 0.06})`, zIndex: 2 }}>
        {emoji && <div style={{ fontSize: 90, marginBottom: 8, opacity: p(0.05, 0.2) }}>{emoji}</div>}
        <div style={{ display: "flex", justifyContent: "center", marginBottom: 24 }}>
          <Kicker theme={T} text={kicker} cx />
        </div>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 86, lineHeight: 1.12, letterSpacing: 0, color: T.text, maxWidth: 1560 }}>{title}</div>
        <div style={{ height: 6, width: interpolate(p(0.18, 0.45), [0, 1], [0, 480]), background: `linear-gradient(90deg, ${A.invest}, ${A.grow})`, borderRadius: 3, margin: "28px auto" }} />
        <div style={{ fontFamily: SANS, fontSize: 34, color: T.muted, opacity: p(0.28, 0.5), lineHeight: 1.4 }}>{sub}</div>
      </div>
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------- biz_divider
const DividerScene: React.FC<{ dur?: number; n?: number; title?: string; sub?: string; color?: string; parts?: number }> = ({
  dur, n = 1, title = "", sub = "", color = A.grow, parts = 3,
}) => {
  const TOTAL_PARTS = parts;
  const frame = useCurrentFrame();
  const p = useP(dur);
  return (
    <Stage>
      <Brackets x={310} y={290} w={1300} h={490} color={color} o={p(0.02, 0.12)} len={54} />
      <ScanBeam theme={T} x={320} y={300} w={1280} h={470} color={color} o={p(0.05, 0.2)} speed={1.6} />
      <GrowMotif x={1470} y={410} r={95} o={p(0.2, 0.34)} dim />
      <div style={{ position: "absolute", left: 0, right: 0, top: 350, textAlign: "center" }}>
        <div style={{ fontFamily: MONO, fontWeight: 800, fontSize: 34, color, letterSpacing: 10, opacity: p(0.05, 0.15) }}>
          PART {n < 10 ? "0" + n : n}
        </div>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 82, color: T.text, letterSpacing: 0, marginTop: 20, opacity: p(0.12, 0.24), transform: `translateY(${(1 - p(0.12, 0.24)) * 30}px)` }}>{title}</div>
        <div style={{ height: 5, width: interpolate(p(0.2, 0.5), [0, 1], [0, 420]), background: color, borderRadius: 3, margin: "26px auto" }} />
        <div style={{ fontFamily: SANS, fontSize: 32, color: T.muted, opacity: p(0.3, 0.45), lineHeight: 1.4 }}>{sub}</div>
      </div>
      <div style={{ position: "absolute", left: 0, right: 0, top: 850, display: "flex", justifyContent: "center", gap: 16, opacity: p(0.3, 0.45) }}>
        {Array.from({ length: TOTAL_PARTS }).map((_, idx) => {
          const i = idx + 1;
          return (
            <div key={i} style={{ width: i === n ? 44 : 14, height: 14, borderRadius: 8,
              background: i <= n ? color : mix(T.panel, color, 0.15), border: `1.5px solid ${i <= n ? color : T.bg2}`,
              opacity: i === n ? 0.7 + Math.sin(frame * 0.1) * 0.3 : 1 }} />
          );
        })}
      </div>
    </Stage>
  );
};

// ---------------------------------------------------------------- biz_recap
const RecapScene: React.FC<{ dur?: number; items?: string[]; closer?: string; title?: string }> = ({
  dur, items = [], closer = "చిన్నగా మొదలుపెట్టు — లెక్క నిరూపించు — తర్వాత పెంచు.", title = "ఒక్క చూపులో గుర్తుంచుకోండి",
}) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  return (
    <AbsoluteFill style={{ padding: "50px 130px", justifyContent: "center" }}>
      <GrowMotif x={1610} y={185} r={95} o={0.4} dim />
      <div style={{ opacity: p(0, 0.06), textAlign: "center", marginBottom: 22 }}>
        <Kicker theme={T} text="RECAP" cx />
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 56, color: T.text, marginTop: 12, letterSpacing: 0 }}>{title}</div>
      </div>
      <div style={{ display: "flex", flexDirection: "column", gap: 11, maxWidth: 1500, margin: "0 auto", width: "100%" }}>
        {items.map((it, i) => {
          const at = 0.06 + i * 0.08;
          const o = p(at, at + 0.07);
          const ghost = p(0.02, 0.06);
          return (
            <div key={i} style={{ display: "flex", alignItems: "center", gap: 18,
              opacity: Math.max(ghost * 0.25, o), transform: `translateX(${(1 - o) * -26}px)`,
              background: mix(T.panel, A.grow, 0.04 + o * 0.04), border: `1.5px solid ${mix(T.bg2, A.grow, o * 0.5)}`,
              borderLeft: `4px solid ${o > 0.5 ? A.grow : T.bg2}`, borderRadius: 12, padding: "13px 26px" }}>
              <span style={{ color: A.grow, fontFamily: MONO, fontWeight: 700, fontSize: 26 }}>{i + 1}</span>
              <span style={{ fontFamily: SANS, fontSize: 27, color: T.text, lineHeight: 1.35 }}>{it}</span>
            </div>
          );
        })}
      </div>
      <div style={{ textAlign: "center", marginTop: 26, opacity: p(0.8, 0.9) }}>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontStyle: "italic", fontSize: 37, color: A.grow, textShadow: `0 0 ${28 + Math.sin(frame * 0.06) * 14}px ${mix(T.bg0, A.grow, 0.7)}` }}>{closer}</div>
      </div>
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------- biz_steps
// Horizontal n-node pipeline with flows; 3–5 nodes.
const StepsScene: React.FC<{
  dur?: number; kicker?: string; title?: string; color?: string; note?: string;
  items?: { emoji: string; label: string; sub: string; c?: string }[];
}> = ({ dur, kicker = "FLOW", title = "", color = A.invest, note = "", items = [] }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const n = items.length;
  const w = n <= 3 ? 420 : n === 4 ? 360 : 290;
  const gapX = n <= 3 ? 560 : n === 4 ? 425 : 340;
  const x0 = n <= 3 ? 190 : n === 4 ? 165 : 170;
  const y = 400;
  return (
    <Stage>
      <BIZHead kicker={kicker} title={title} color={color} o={p(0, 0.06)} />
      {items.map((it, i) => {
        const c = it.c || color;
        const at = 0.1 + i * (0.55 / n);
        const o = p(at, at + 0.08);
        const ghost = p(0.03, 0.07);
        const x = x0 + i * gapX;
        const active = Math.floor(frame / 24) % n === i && p(0.75, 0.76) > 0.5;
        return (
          <React.Fragment key={i}>
            {i > 0 && (
              <>
                <Wire x1={x0 + (i - 1) * gapX + w} y1={y + 105} x2={x - 8} y2={y + 105} p={p(at - 0.05, at)} color={c} w={3} />
                <Flow x1={x0 + (i - 1) * gapX + w} y1={y + 105} x2={x - 8} y2={y + 105} color={c} n={4} o={p(at, at + 0.1)} />
              </>
            )}
            <div style={{ position: "absolute", left: x, top: y, width: w, height: 230,
              borderRadius: 18, boxSizing: "border-box", padding: "22px 20px", textAlign: "center",
              background: mix(T.panel, c, o > 0.5 ? (active ? 0.16 : 0.09) : 0.02),
              border: `2.5px solid ${o > 0.5 ? mix(T.bg2, c, active ? 1 : 0.7) : T.bg2}`,
              opacity: Math.max(ghost * 0.22, o), transform: `translateY(${(1 - o) * 20}px) scale(${active ? 1.04 : 1})` }}>
              <div style={{ fontSize: 48 }}>{it.emoji}</div>
              <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 28, color: c, marginTop: 8, lineHeight: 1.25 }}>{it.label}</div>
              <div style={{ fontFamily: SANS, fontSize: 23, color: T.muted, marginTop: 6, lineHeight: 1.35 }}>{it.sub}</div>
            </div>
          </React.Fragment>
        );
      })}
      {note && (
        <div style={{ position: "absolute", left: 150, top: 730, width: 1620, textAlign: "center", opacity: p(0.72, 0.84) }}>
          <span style={{ fontFamily: SANS, fontWeight: 700, fontSize: 31, color: T.text, lineHeight: 1.4 }}>{note}</span>
        </div>
      )}
    </Stage>
  );
};

// ---------------------------------------------------------------- biz_iconcards
const IconCardsScene: React.FC<{
  dur?: number; kicker?: string; title?: string; color?: string;
  items?: { emoji: string; k: string; v: string; chip?: string }[];
}> = ({ dur, kicker = "CONCEPTS", title = "", color = A.idea, items = [] }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const cols = items.length > 4 ? 3 : 2;
  const rows = Math.ceil(items.length / cols);
  const w = cols === 2 ? 810 : 533, gap = 24;
  const h = rows === 2 ? 320 : rows === 3 ? 210 : 320;
  const y0 = 210 + (660 - (rows * h + (rows - 1) * gap)) / 2;
  const hot = Math.floor(frame / 32) % items.length;
  return (
    <Stage>
      <BIZHead kicker={kicker} title={title} color={color} o={p(0, 0.06)} />
      {items.map((it, i) => {
        const r = Math.floor(i / cols), c = i % cols;
        const at = 0.1 + i * (0.55 / items.length);
        const o = p(at, at + 0.09);
        const ghost = p(0.03, 0.07);
        const active = hot === i && p(0.78, 0.79) > 0.5;
        return (
          <div key={i} style={{
            position: "absolute", left: 130 + c * (w + gap), top: y0 + r * (h + gap), width: w, height: h,
            borderRadius: 20, boxSizing: "border-box", padding: "24px 30px",
            opacity: Math.max(ghost * 0.22, o), transform: `translateY(${(1 - o) * 22}px) scale(${active ? 1.02 : 1})`,
            background: mix(T.panel, color, o > 0.5 ? (active ? 0.15 : 0.08) : 0.02),
            border: `2.5px solid ${o > 0.5 ? mix(T.bg2, color, active ? 1 : 0.65) : T.bg2}`,
          }}>
            <div style={{ display: "flex", alignItems: "center", gap: 18 }}>
              <span style={{ fontSize: h > 250 ? 58 : 44 }}>{it.emoji}</span>
              <span style={{ fontFamily: SANS, fontWeight: 800, fontSize: h > 250 ? 33 : 28, color, lineHeight: 1.25 }}>{it.k}</span>
            </div>
            <div style={{ fontFamily: SANS, fontSize: h > 250 ? 27 : 24, color: T.text, marginTop: 14, lineHeight: 1.4, opacity: 0.62 + o * 0.38 }}>{it.v}</div>
            {it.chip && (
              <div style={{ position: "absolute", right: 22, bottom: 18, fontFamily: MONO, fontWeight: 700, fontSize: 22,
                color: T.bg0, background: color, borderRadius: 999, padding: "8px 18px", opacity: o }}>{it.chip}</div>
            )}
          </div>
        );
      })}
    </Stage>
  );
};

// ---------------------------------------------------------------- biz_compare3
const Compare3Scene: React.FC<{
  dur?: number; kicker?: string; title?: string;
  cols?: { name: string; color: string; emoji?: string; hi?: boolean; rows: { k: string; v: string }[] }[];
}> = ({ dur, kicker = "COMPARE", title = "", cols = [] }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const n = cols.length;
  const cw = n === 2 ? 800 : 520;
  const gapX = n === 2 ? 60 : 40;
  const x0 = n === 2 ? 130 : 140;
  return (
    <Stage>
      <BIZHead kicker={kicker} title={title} o={p(0, 0.06)} />
      {cols.map((col, i) => {
        const at = 0.08 + i * 0.16;
        const o = p(at, at + 0.1);
        const ghost = p(0.03, 0.07);
        return (
          <div key={i} style={{
            position: "absolute", left: x0 + i * (cw + gapX), top: 230, width: cw, height: 640,
            borderRadius: 20, boxSizing: "border-box", padding: "28px 30px",
            opacity: Math.max(ghost * 0.22, o), transform: `translateY(${(1 - o) * 24}px)`,
            background: mix(T.panel, col.color, o > 0.5 ? 0.08 : 0.02),
            border: `2.5px solid ${o > 0.5 ? col.color : T.bg2}`,
          }}>
            <div style={{ textAlign: "center" }}>
              <div style={{ fontSize: 54 }}>{col.emoji}</div>
              <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 32, color: col.color, marginTop: 6, lineHeight: 1.25 }}>{col.name}</div>
            </div>
            <div style={{ marginTop: 22, display: "flex", flexDirection: "column", gap: 16 }}>
              {col.rows.map((r, ri) => (
                <div key={ri} style={{ opacity: p(at + 0.07 + ri * 0.03, at + 0.13 + ri * 0.03) }}>
                  <div style={{ fontFamily: MONO, fontSize: 22, color: T.muted, lineHeight: 1.35 }}>{r.k}</div>
                  <div style={{ fontFamily: SANS, fontWeight: 700, fontSize: 26, color: T.text, marginTop: 3, lineHeight: 1.35 }}>{r.v}</div>
                </div>
              ))}
            </div>
            {col.hi && (
              <div style={{ position: "absolute", left: 0, right: 0, bottom: -1, height: 8, borderRadius: 4, background: col.color, opacity: 0.5 + Math.sin(frame * 0.08) * 0.3 }} />
            )}
          </div>
        );
      })}
    </Stage>
  );
};

// ---------------------------------------------------------------- biz_checklist
const ChecklistScene: React.FC<{ dur?: number; kicker?: string; title?: string; color?: string; items?: string[]; icon?: string }> = ({
  dur, kicker = "CHECKLIST", title = "", color = A.grow, items = [], icon = "✅",
}) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const n = items.length;
  const rowH = Math.min(108, Math.floor(620 / n) - 10);
  const totalH = n * (rowH + 14);
  const y0 = 210 + Math.max(0, (660 - totalH) / 2);
  const hot = Math.floor(frame / 30) % n;
  return (
    <Stage>
      <BIZHead kicker={kicker} title={title} color={color} o={p(0, 0.06)} />
      {items.map((it, i) => {
        const at = 0.08 + (i * 0.7) / n;
        const o = p(at, at + 0.08);
        const ghost = p(0.03, 0.07);
        const active = hot === i && p(0.8, 0.81) > 0.5;
        return (
          <div key={i} style={{
            position: "absolute", left: 130, top: y0 + i * (rowH + 14), width: 1660, height: rowH,
            display: "flex", alignItems: "center", gap: 24, padding: "0 34px", boxSizing: "border-box",
            borderRadius: 16, opacity: Math.max(ghost * 0.22, o),
            background: mix(T.panel, color, o > 0.5 ? (active ? 0.16 : 0.09) : 0.02),
            border: `2px solid ${o > 0.5 ? mix(T.bg2, color, active ? 1 : 0.6) : T.bg2}`,
            transform: `translateX(${(1 - o) * -30}px) scale(${active ? 1.015 : 1})`,
          }}>
            <div style={{ width: 52, height: 52, borderRadius: 12, background: mix(T.panel, color, 0.2), border: `2px solid ${color}`,
              display: "flex", alignItems: "center", justifyContent: "center", fontSize: 28, opacity: o }}>{icon}</div>
            <span style={{ fontFamily: MONO, fontWeight: 800, fontSize: 27, color, opacity: o }}>{i + 1}</span>
            <span style={{ fontFamily: SANS, fontWeight: 700, fontSize: 29, color: T.text, lineHeight: 1.35 }}>{it}</span>
          </div>
        );
      })}
    </Stage>
  );
};

// ---------------------------------------------------------------- biz_stats
const StatsScene: React.FC<{
  dur?: number; kicker?: string; title?: string; note?: string;
  stats?: { label: string; to: number; prefix?: string; suffix?: string; decimals?: number; color?: string; sub?: string }[];
}> = ({ dur, kicker = "DATA", title = "", note = "", stats = [] }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const n = stats.length;
  const w = n === 2 ? 810 : n === 3 ? 533 : 390;
  const y0 = note ? 270 : 320;
  return (
    <Stage>
      <BIZHead kicker={kicker} title={title} color={A.money} o={p(0, 0.06)} />
      {stats.map((s, i) => {
        const at = 0.1 + i * (0.5 / n);
        const o = p(at, at + 0.1);
        const ghost = p(0.03, 0.07);
        const c = s.color || A.money;
        return (
          <div key={i} style={{
            position: "absolute", left: 130 + i * (w + 24), top: y0, width: w, height: 360,
            borderRadius: 20, boxSizing: "border-box", padding: "34px 26px", textAlign: "center",
            background: mix(T.panel, c, o > 0.5 ? 0.07 : 0.02), border: `2.5px solid ${o > 0.5 ? mix(T.bg2, c, 0.7) : T.bg2}`,
            opacity: Math.max(ghost * 0.22, o), transform: `translateY(${(1 - o) * 22}px)`,
            boxShadow: o > 0.9 ? `0 0 ${34 + Math.sin(frame * 0.07 + i) * 12}px ${mix(T.bg0, c, 0.22)}` : "none",
          }}>
            <div style={{ fontFamily: SANS, fontSize: 26, color: T.muted, lineHeight: 1.35, minHeight: 76 }}>{s.label}</div>
            <div style={{ marginTop: 18 }}>
              <Counter p={p(at + 0.04, at + 0.22)} to={s.to} prefix={s.prefix || ""} suffix={s.suffix || ""} decimals={s.decimals || 0} color={c} size={n === 2 ? 82 : 62} />
            </div>
            {s.sub && <div style={{ fontFamily: SANS, fontSize: 24, color: T.text, marginTop: 18, lineHeight: 1.4, opacity: p(at + 0.12, at + 0.2) }}>{s.sub}</div>}
          </div>
        );
      })}
      {note && (
        <div style={{ position: "absolute", left: 130, top: 700, width: 1660, textAlign: "center", opacity: p(0.68, 0.8) }}>
          <span style={{ fontFamily: SANS, fontWeight: 700, fontSize: 31, color: T.text, lineHeight: 1.4 }}>{note}</span>
        </div>
      )}
    </Stage>
  );
};

// ---------------------------------------------------------------- biz_stairs
// Roadmap staircase: numbered steps rising L→R with a walker.
const StairsScene: React.FC<{
  dur?: number; kicker?: string; title?: string;
  steps?: { emoji: string; label: string; sub?: string; c?: string }[]; note?: string;
}> = ({ dur, kicker = "ROADMAP", title = "", steps = [], note = "" }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const n = steps.length;
  const w = Math.min(300, Math.floor(1620 / n) - 16);
  const baseY = 670, riser = Math.min(90, Math.floor(400 / n));  // bottom ≤ y880 for caption clearance
  const walker = Math.min(n - 1, Math.floor(p(0.7, 0.95) * n));
  return (
    <Stage>
      <BIZHead kicker={kicker} title={title} color={A.grow} o={p(0, 0.06)} />
      {steps.map((s, i) => {
        const c = s.c || A.grow;
        const at = 0.08 + i * (0.55 / n);
        const o = p(at, at + 0.08);
        const x = 150 + i * (w + 16);
        const y = baseY - i * riser;
        const active = walker === i;
        return (
          <div key={i} style={{ position: "absolute", left: x, top: y, width: w, height: 200 + i * riser,
            borderRadius: "16px 16px 0 0", boxSizing: "border-box", padding: "18px 18px",
            background: `linear-gradient(180deg, ${mix(T.panel, c, o > 0.5 ? 0.14 : 0.03)}, ${mix(T.panel, c, 0.03)})`,
            borderTop: `4px solid ${o > 0.5 ? c : T.bg2}`, borderLeft: `2px solid ${o > 0.5 ? mix(T.bg2, c, 0.5) : T.bg2}`,
            borderRight: `2px solid ${o > 0.5 ? mix(T.bg2, c, 0.5) : T.bg2}`,
            opacity: Math.max(p(0.03, 0.07) * 0.25, o),
            boxShadow: active ? `0 0 ${26 + Math.sin(frame * 0.09) * 10}px ${mix(T.bg0, c, 0.3)}` : "none" }}>
            <div style={{ fontSize: 40 }}>{s.emoji}</div>
            <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 25, color: c, marginTop: 8, lineHeight: 1.3 }}>{s.label}</div>
            {s.sub && <div style={{ fontFamily: SANS, fontSize: 22, color: T.muted, marginTop: 6, lineHeight: 1.35 }}>{s.sub}</div>}
            <div style={{ position: "absolute", top: -46, left: 12, fontFamily: MONO, fontWeight: 800, fontSize: 26, color: c, opacity: o }}>{i + 1}</div>
          </div>
        );
      })}
      <div style={{ position: "absolute", left: 150 + walker * (w + 16) + w / 2 - 24, top: baseY - walker * riser - 64,
        fontSize: 48, opacity: p(0.68, 0.76), transform: `translateY(${Math.sin(frame * 0.12) * 4}px)` }}>🚶</div>
      {note && (
        <div style={{ position: "absolute", left: 150, top: 205, width: 1620, opacity: p(0.1, 0.2) }}>
          <span style={{ fontFamily: SANS, fontSize: 28, color: T.muted, lineHeight: 1.4 }}>{note}</span>
        </div>
      )}
    </Stage>
  );
};

// ---------------------------------------------------------------- biz_capex
// Investment breakdown: horizontal bars summing to a total (Counter). Values in ₹ lakh.
const CapexScene: React.FC<{
  dur?: number; kicker?: string; title?: string; unit?: string; total?: number; totalLabel?: string;
  items?: { label: string; v: number; color?: string }[]; note?: string;
}> = ({ dur, kicker = "INVESTMENT", title = "", unit = " లక్షలు", total = 0, totalLabel = "మొత్తం పెట్టుబడి",
  items = [], note = "" }) => {
  const p = useP(dur);
  const n = items.length;
  const maxV = Math.max(...items.map((i) => i.v), 1);
  const X0 = 620, BW = 900, rowH = Math.min(74, Math.floor(520 / n));
  const y0 = 250;
  return (
    <Stage>
      <BIZHead kicker={kicker} title={title} color={A.invest} o={p(0, 0.06)} />
      {items.map((it, i) => {
        const c = it.color || A.invest;
        const at = 0.1 + i * (0.55 / n);
        const grow = p(at, at + 0.12);
        const o = p(at - 0.02, at + 0.04);
        const y = y0 + i * (rowH + 16);
        return (
          <React.Fragment key={i}>
            <div style={{ position: "absolute", left: 130, top: y + rowH / 2 - 18, width: 470, textAlign: "right",
              fontFamily: SANS, fontWeight: 700, fontSize: 24, color: T.text, opacity: o, lineHeight: 1.25 }}>{it.label}</div>
            <div style={{ position: "absolute", left: X0, top: y, width: BW, height: rowH, borderRadius: 10,
              background: mix(T.panel, c, 0.05), border: `1.5px solid ${T.bg2}`, opacity: o, overflow: "hidden" }}>
              <div style={{ width: `${(it.v / maxV) * 100 * grow}%`, height: "100%",
                background: `linear-gradient(90deg, ${mix(c, T.bg1, 0.35)}, ${c})` }} />
            </div>
            <div style={{ position: "absolute", left: X0 + BW + 16, top: y + rowH / 2 - 18, width: 260,
              fontFamily: MONO, fontWeight: 800, fontSize: 26, color: c, opacity: grow }}>₹{it.v}{unit}</div>
          </React.Fragment>
        );
      })}
      <div style={{ position: "absolute", left: 620, top: y0 + n * (rowH + 16) + 20, width: 900, textAlign: "center", opacity: p(0.66, 0.78) }}>
        <div style={{ fontFamily: SANS, fontSize: 25, color: T.muted }}>{totalLabel}</div>
        <Counter p={p(0.7, 0.9)} to={total} prefix="≈ ₹" suffix={unit} color={A.grow} size={56} />
      </div>
      {note && (
        <div style={{ position: "absolute", left: 130, top: 852, width: 1660, textAlign: "center", opacity: p(0.8, 0.92) }}>
          <span style={{ fontFamily: SANS, fontSize: 24, color: T.muted, lineHeight: 1.35 }}>{note}</span>
        </div>
      )}
    </Stage>
  );
};

// ---------------------------------------------------------------- biz_econ
// Generic unit economics: a COST bar vs a REVENUE bar (same scale) with legends, and a
// net-profit callout. Labels come from props (generalizes the lead-recycling pnl scene).
const EconScene: React.FC<{
  dur?: number; kicker?: string; title?: string; unit?: string;
  costLabel?: string; revLabel?: string; netLabel?: string;
  costs?: { label: string; v: number; c: string }[];
  revenue?: { label: string; v: number; c: string }[];
  net?: number; netColor?: string; note?: string;
}> = ({ dur, kicker = "UNIT ECONOMICS", title = "", unit = " / order",
  costLabel = "ఖర్చు (ఒక యూనిట్‌కు)", revLabel = "రాబడి (అదే యూనిట్)", netLabel = "నికర లాభం (నెట్)",
  costs = [], revenue = [], net = 0, netColor = A.grow, note = "" }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const costTot = costs.reduce((s, x) => s + x.v, 0);
  const revTot = revenue.reduce((s, x) => s + x.v, 0);
  const maxV = Math.max(costTot, revTot, 1);
  const X0 = 250, BW = 1250, SCALE = BW / maxV;
  const barH = 92;
  const Bar = (items: { label: string; v: number; c: string }[], y: number, at0: number, tot: number, cap: string, capColor: string) => {
    let acc = 0;
    return (
      <React.Fragment>
        <div style={{ position: "absolute", left: 130, top: y - 34, fontFamily: SANS, fontWeight: 800, fontSize: 24, color: capColor, opacity: p(at0 - 0.02, at0 + 0.04) }}>{cap}</div>
        {items.map((it, i) => {
          const at = at0 + i * 0.05;
          const grow = p(at, at + 0.1);
          const x = X0 + acc * SCALE;
          const wpx = it.v * SCALE * grow;
          acc += it.v;
          return (
            <div key={i} style={{ position: "absolute", left: x, top: y, width: Math.max(0, wpx), height: barH,
              background: `linear-gradient(90deg, ${mix(it.c, T.bg1, 0.3)}, ${it.c})`, borderRight: `2px solid ${T.bg0}`,
              borderRadius: i === 0 ? "10px 0 0 10px" : 0 }} />
          );
        })}
        <div style={{ position: "absolute", left: X0 + tot * SCALE + 18, top: y + barH / 2 - 20, width: 220,
          fontFamily: MONO, fontWeight: 800, fontSize: 30, color: capColor, opacity: p(at0 + 0.12, at0 + 0.2) }}>₹{tot}</div>
        <div style={{ position: "absolute", left: X0, top: y + barH + 12, width: BW, display: "flex", gap: 24, flexWrap: "wrap" }}>
          {items.map((it, i) => (
            <div key={i} style={{ display: "flex", alignItems: "center", gap: 9, opacity: p(at0 + i * 0.05 + 0.04, at0 + i * 0.05 + 0.12) }}>
              <span style={{ width: 18, height: 18, borderRadius: 5, background: it.c, display: "inline-block" }} />
              <span style={{ fontFamily: MONO, fontWeight: 700, fontSize: 21, color: T.text }}>{it.label} · ₹{it.v}</span>
            </div>
          ))}
        </div>
      </React.Fragment>
    );
  };
  return (
    <Stage>
      <BIZHead kicker={kicker} title={title} color={A.money} o={p(0, 0.06)} />
      {Bar(costs, 268, 0.1, costTot, costLabel, A.risk)}
      {Bar(revenue, 468, 0.36, revTot, revLabel, A.grow)}
      <div style={{ position: "absolute", left: 250, top: 664, width: 1250, height: 96, borderRadius: 16,
        background: mix(T.panel, netColor, 0.12), border: `2.5px solid ${netColor}`, boxSizing: "border-box",
        display: "flex", alignItems: "center", justifyContent: "space-between", padding: "0 40px",
        opacity: p(0.66, 0.76), boxShadow: `0 0 ${26 + Math.sin(frame * 0.07) * 12}px ${mix(T.bg0, netColor, 0.3)}` }}>
        <span style={{ fontFamily: SANS, fontWeight: 800, fontSize: 31, color: netColor }}>{netLabel}</span>
        <Counter p={p(0.72, 0.88)} to={net} prefix="≈ ₹" suffix={unit} color={netColor} size={50} />
      </div>
      {note && (
        <div style={{ position: "absolute", left: 130, top: 782, width: 1660, textAlign: "center", opacity: p(0.8, 0.9) }}>
          <span style={{ fontFamily: SANS, fontSize: 24, color: T.muted, lineHeight: 1.35 }}>{note}</span>
        </div>
      )}
    </Stage>
  );
};

// ---------------------------------------------------------------- biz_matrix
// A compact comparison table: first column = idea (emoji + name), then k data cells,
// each a chip toned good/med/bad. Header row + phased data rows. Up to ~6 rows.
const TONE: Record<string, string> = { good: A.grow, med: A.money, bad: A.risk, plain: A.invest };
const MatrixScene: React.FC<{
  dur?: number; kicker?: string; title?: string; headers?: string[];
  rows?: { name: string; emoji?: string; cells: { t: string; tone?: string }[] }[]; note?: string;
}> = ({ dur, kicker = "COMPARE", title = "", headers = [], rows = [], note = "" }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const n = rows.length;
  const nameW = 470, cellGap = 14;
  const k = headers.length;
  const cellW = Math.floor((1660 - nameW - cellGap) / k) - cellGap;
  const rowH = Math.min(96, Math.floor(560 / (n + 1)) - 12);
  const y0 = 220;
  const hot = Math.floor(frame / 30) % n;
  const x0 = 130;
  const cellX = (ci: number) => x0 + nameW + cellGap + ci * (cellW + cellGap);
  return (
    <Stage>
      <BIZHead kicker={kicker} title={title} color={A.idea} o={p(0, 0.06)} />
      {/* header row */}
      <div style={{ position: "absolute", left: x0 + nameW + cellGap, top: y0, opacity: p(0.05, 0.12) }}>
        {headers.map((h, ci) => (
          <div key={ci} style={{ position: "absolute", left: ci * (cellW + cellGap), top: 0, width: cellW, height: rowH,
            display: "flex", alignItems: "center", justifyContent: "center",
            fontFamily: MONO, fontWeight: 700, fontSize: 22, color: T.muted, textAlign: "center", lineHeight: 1.2 }}>{h}</div>
        ))}
      </div>
      {rows.map((row, ri) => {
        const at = 0.1 + ri * (0.6 / n);
        const o = p(at, at + 0.08);
        const ghost = p(0.03, 0.07);
        const active = hot === ri && p(0.78, 0.79) > 0.5;
        const y = y0 + (ri + 1) * (rowH + 12);
        return (
          <React.Fragment key={ri}>
            <div style={{ position: "absolute", left: x0, top: y, width: nameW, height: rowH,
              display: "flex", alignItems: "center", gap: 14, padding: "0 20px", boxSizing: "border-box",
              borderRadius: 12, opacity: Math.max(ghost * 0.22, o),
              background: mix(T.panel, A.idea, o > 0.5 ? (active ? 0.16 : 0.08) : 0.02),
              border: `2px solid ${o > 0.5 ? mix(T.bg2, A.idea, active ? 1 : 0.6) : T.bg2}`,
              transform: `translateX(${(1 - o) * -24}px)` }}>
              {row.emoji && <span style={{ fontSize: 34 }}>{row.emoji}</span>}
              <span style={{ fontFamily: SANS, fontWeight: 700, fontSize: 25, color: T.text, lineHeight: 1.2 }}>{row.name}</span>
            </div>
            {row.cells.map((cell, ci) => {
              const c = TONE[cell.tone || "plain"];
              return (
                <div key={ci} style={{ position: "absolute", left: cellX(ci), top: y, width: cellW, height: rowH,
                  display: "flex", alignItems: "center", justifyContent: "center", textAlign: "center",
                  borderRadius: 12, opacity: o, boxSizing: "border-box", padding: "0 8px",
                  background: mix(T.panel, c, 0.13), border: `1.5px solid ${mix(T.bg2, c, 0.7)}`,
                  fontFamily: MONO, fontWeight: 700, fontSize: 22, color: c, lineHeight: 1.2 }}>{cell.t}</div>
              );
            })}
          </React.Fragment>
        );
      })}
      {note && (
        <div style={{ position: "absolute", left: 130, top: 838, width: 1660, textAlign: "center", opacity: p(0.72, 0.84) }}>
          <span style={{ fontFamily: SANS, fontSize: 24, color: T.muted, lineHeight: 1.35 }}>{note}</span>
        </div>
      )}
    </Stage>
  );
};

// ---------------------------------------------------------------- dispatcher
export const BIZScene: React.FC<{ variant: string;[key: string]: unknown }> = ({ variant, ...rest }) => {
  let content: React.ReactNode = null;
  let accent = T.accent;
  switch (variant) {
    case "biz_title": content = <TitleScene {...(rest as any)} />; break;
    case "biz_ptitle": content = <PTitleScene {...(rest as any)} />; break;
    case "biz_divider": content = <DividerScene {...(rest as any)} />; accent = ((rest as any).color as string) || A.grow; break;
    case "biz_recap": content = <RecapScene {...(rest as any)} />; break;
    case "biz_steps": content = <StepsScene {...(rest as any)} />; accent = ((rest as any).color as string) || A.invest; break;
    case "biz_iconcards": content = <IconCardsScene {...(rest as any)} />; accent = ((rest as any).color as string) || A.idea; break;
    case "biz_compare3": content = <Compare3Scene {...(rest as any)} />; break;
    case "biz_checklist": content = <ChecklistScene {...(rest as any)} />; accent = ((rest as any).color as string) || A.grow; break;
    case "biz_stats": content = <StatsScene {...(rest as any)} />; accent = A.money; break;
    case "biz_stairs": content = <StairsScene {...(rest as any)} />; accent = A.grow; break;
    case "biz_capex": content = <CapexScene {...(rest as any)} />; accent = A.invest; break;
    case "biz_econ": content = <EconScene {...(rest as any)} />; accent = A.money; break;
    case "biz_matrix": content = <MatrixScene {...(rest as any)} />; accent = A.idea; break;
    default:
      content = (
        <AbsoluteFill style={{ alignItems: "center", justifyContent: "center" }}>
          <div style={{ color: "#f88", fontFamily: MONO, fontSize: 40 }}>unknown biz variant “{variant}”</div>
        </AbsoluteFill>
      );
  }
  return (
    <AbsoluteFill>
      <Bg theme={T} accent={accent} />
      {content}
    </AbsoluteFill>
  );
};
