/**
 * LBRScenes.tsx — "Lead-Acid Battery Recycling business" Telugu course (prefix `lbr`).
 *
 * Identity (skills/04):
 *   theme accent = molten amber (#FB923C). Semantic accents:
 *     heat   orange #FB923C — furnace / smelting / the core hot process
 *     lead   steel  #9FB3C8 — lead metal, ingots, the material itself
 *     money  amber  #FBBF24 — rupees, capex, unit economics
 *     green  emeral #34D399 — recycling loop, EPR, profit, compliance-good
 *     risk   rose   #FB7185 — hazard, lead poisoning, pollution, non-compliance
 *   Recurring motif: a live circular recycling loop (LoopMotif) — title, dividers,
 *   chapter titles. A closed loop = the circular-economy idea of the whole business.
 *
 * Telugu long-form rules (skills/11): NO letterSpacing on Telugu (kickers are LATIN),
 * first skeleton visible by p≈0.06, content fills the vertical band, Telugu ≥ 23px,
 * lineHeight ≥ 1.35, mix() gets HEX only. Brands/₹/numbers stay Latin on screen.
 */
import React from "react";
import { AbsoluteFill, interpolate, useCurrentFrame } from "remotion";
import {
  makeTheme, mix, useP, usePop, rnd, MONO, SANS,
  Bg, Stage, Kicker, Card, Flow, Wire, Counter, Brackets, ScanBeam,
} from "../lib/primitives";

const T = makeTheme({ accent: "#FB923C", bg0: "#0B0A08", bg1: "#12100C", bg2: "#241D14", panel: "#1C1810" });
const A = { heat: "#FB923C", lead: "#9FB3C8", money: "#FBBF24", green: "#34D399", risk: "#FB7185" };

// LBRHead — Telugu-safe header: Latin kicker (tracked), Telugu title untracked.
const LBRHead: React.FC<{ kicker: string; title: string; color?: string; o?: number }> = ({
  kicker, title, color, o = 1,
}) => (
  <div style={{ position: "absolute", left: 100, top: 54, right: 100 }}>
    <Kicker theme={T} text={kicker} color={color} o={o} />
    <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 52, color: T.text, marginTop: 12, letterSpacing: 0, opacity: o }}>{title}</div>
  </div>
);

// ---------------------------------------------------------------- motif
/** The motif: a rotating recycling loop with orbiting battery→ingot markers. */
const LoopMotif: React.FC<{ x: number; y: number; r: number; o?: number; dim?: boolean }> = ({
  x, y, r, o = 1, dim,
}) => {
  const frame = useCurrentFrame();
  const rot = frame * 0.7;
  const marks = ["🔋", "🔥", "🧱", "♻️"];
  return (
    <div style={{ position: "absolute", left: 0, top: 0, opacity: o * (dim ? 0.4 : 1), pointerEvents: "none" }}>
      <svg width={1920} height={1080} style={{ position: "absolute", left: 0, top: 0, overflow: "visible" }}>
        {/* two chasing arc arrows forming a loop */}
        {[0, 1].map((k) => (
          <circle key={k} cx={x} cy={y} r={r} fill="none" stroke={k ? A.green : A.heat} strokeWidth={5}
            strokeLinecap="round" strokeDasharray={`${Math.PI * r * 0.42} ${Math.PI * r * 0.58}`}
            strokeDashoffset={-(rot * (k ? -1 : 1))} transform={`rotate(${k * 180} ${x} ${y})`} opacity={0.75} />
        ))}
        <circle cx={x} cy={y} r={r * 0.62} fill="none" stroke={mix(T.bg2, A.heat, 0.4)} strokeWidth={2} />
      </svg>
      {marks.map((m, i) => {
        const ang = (rot * 0.017) + (i / marks.length) * Math.PI * 2;
        return (
          <div key={i} style={{ position: "absolute", left: x + Math.cos(ang) * r - 20, top: y + Math.sin(ang) * r - 22, fontSize: 38 }}>{m}</div>
        );
      })}
      <div style={{ position: "absolute", left: x - 34, top: y - 40, fontSize: 66, opacity: 0.9 }}>♻️</div>
    </div>
  );
};

// ---------------------------------------------------------------- lbr_title
const TitleScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const pop = usePop(dur);
  return (
    <AbsoluteFill style={{ alignItems: "center", justifyContent: "center" }}>
      <LoopMotif x={320} y={760} r={150} o={p(0.08, 0.22)} dim />
      <LoopMotif x={1600} y={250} r={120} o={p(0.14, 0.28)} dim />
      {/* rising heat embers */}
      {Array.from({ length: 12 }).map((_, i) => {
        const t = ((frame * (0.6 + rnd(i, 2) * 0.6) + i * 90) % 700) / 700;
        return (
          <div key={i} style={{ position: "absolute", left: 200 + rnd(i, 5) * 1520,
            top: 900 - t * 780, fontFamily: MONO, fontWeight: 800, fontSize: 18,
            color: i % 2 ? A.heat : A.money, opacity: (1 - t) * 0.35, textShadow: `0 0 12px ${i % 2 ? A.heat : A.money}` }}>▲</div>
        );
      })}
      <div style={{ textAlign: "center", transform: `scale(${0.92 + pop(0) * 0.08})`, zIndex: 2 }}>
        <div style={{ display: "flex", justifyContent: "center", marginBottom: 26 }}>
          <Kicker theme={T} text="BUSINESS COURSE · 2026" cx />
        </div>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 104, lineHeight: 1.08, letterSpacing: 0, color: T.text }}>
          <div>లెడ్ బ్యాటరీ రీసైక్లింగ్</div>
          <div style={{ color: A.heat, textShadow: `0 0 70px ${mix(T.bg0, A.heat, 0.7)}` }}>వ్యాపారం — A to Z</div>
        </div>
        <div style={{ height: 6, width: interpolate(p(0.18, 0.45), [0, 1], [0, 620]), background: `linear-gradient(90deg, ${A.heat}, ${A.green})`, borderRadius: 3, margin: "30px auto" }} />
        <div style={{ fontFamily: SANS, fontSize: 34, color: T.muted, opacity: p(0.28, 0.5), lineHeight: 1.4 }}>
          ప్రాసెస్ · మెషినరీ · పెట్టుబడి · లైసెన్సులు — పూర్తి ఫండమెంటల్స్
        </div>
      </div>
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------- lbr_ptitle
const PTitleScene: React.FC<{ dur?: number; title?: string; sub?: string; kicker?: string }> = ({
  dur, title = "", sub = "", kicker = "CHAPTER",
}) => {
  const p = useP(dur);
  const pop = usePop(dur);
  return (
    <AbsoluteFill style={{ alignItems: "center", justifyContent: "center" }}>
      <LoopMotif x={960} y={560} r={330} o={p(0.1, 0.3)} dim />
      <div style={{ textAlign: "center", transform: `scale(${0.94 + pop(0) * 0.06})`, zIndex: 2 }}>
        <div style={{ display: "flex", justifyContent: "center", marginBottom: 24 }}>
          <Kicker theme={T} text={kicker} cx />
        </div>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 88, lineHeight: 1.12, letterSpacing: 0, color: T.text, maxWidth: 1560 }}>{title}</div>
        <div style={{ height: 6, width: interpolate(p(0.18, 0.45), [0, 1], [0, 480]), background: `linear-gradient(90deg, ${A.heat}, ${A.green})`, borderRadius: 3, margin: "28px auto" }} />
        <div style={{ fontFamily: SANS, fontSize: 34, color: T.muted, opacity: p(0.28, 0.5), lineHeight: 1.4 }}>{sub}</div>
      </div>
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------- lbr_divider
const TOTAL_PARTS = 4;
const DividerScene: React.FC<{ dur?: number; n?: number; title?: string; sub?: string; color?: string }> = ({
  dur, n = 1, title = "", sub = "", color = A.heat,
}) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  return (
    <Stage>
      <Brackets x={310} y={290} w={1300} h={490} color={color} o={p(0.02, 0.12)} len={54} />
      <ScanBeam theme={T} x={320} y={300} w={1280} h={470} color={color} o={p(0.05, 0.2)} speed={1.6} />
      <LoopMotif x={1470} y={410} r={95} o={p(0.2, 0.34)} dim />
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

// ---------------------------------------------------------------- lbr_recap
const RecapScene: React.FC<{ dur?: number; items?: string[]; closer?: string; title?: string }> = ({
  dur, items = [], closer = "ముందు నేర్చుకో — తర్వాత పెట్టుబడి పెట్టు.", title = "ఒక్క చూపులో గుర్తుంచుకోండి",
}) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  return (
    <AbsoluteFill style={{ padding: "60px 130px", justifyContent: "center" }}>
      <LoopMotif x={1600} y={190} r={100} o={0.4} dim />
      <div style={{ opacity: p(0, 0.06), textAlign: "center", marginBottom: 26 }}>
        <Kicker theme={T} text="RECAP" cx />
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 58, color: T.text, marginTop: 12, letterSpacing: 0 }}>{title}</div>
      </div>
      <div style={{ display: "flex", flexDirection: "column", gap: 12, maxWidth: 1480, margin: "0 auto", width: "100%" }}>
        {items.map((it, i) => {
          const at = 0.06 + i * 0.08;
          const o = p(at, at + 0.07);
          const ghost = p(0.02, 0.06);
          return (
            <div key={i} style={{ display: "flex", alignItems: "center", gap: 18,
              opacity: Math.max(ghost * 0.25, o), transform: `translateX(${(1 - o) * -26}px)`,
              background: mix(T.panel, A.heat, 0.04 + o * 0.04), border: `1.5px solid ${mix(T.bg2, A.heat, o * 0.5)}`,
              borderLeft: `4px solid ${o > 0.5 ? A.heat : T.bg2}`, borderRadius: 12, padding: "14px 26px" }}>
              <span style={{ color: A.heat, fontFamily: MONO, fontWeight: 700, fontSize: 26 }}>{i + 1}</span>
              <span style={{ fontFamily: SANS, fontSize: 28, color: T.text, lineHeight: 1.35 }}>{it}</span>
            </div>
          );
        })}
      </div>
      <div style={{ textAlign: "center", marginTop: 30, opacity: p(0.8, 0.9) }}>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontStyle: "italic", fontSize: 38, color: A.heat, textShadow: `0 0 ${28 + Math.sin(frame * 0.06) * 14}px ${mix(T.bg0, A.heat, 0.7)}` }}>{closer}</div>
      </div>
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------- lbr_steps
// Horizontal n-node pipeline with flows; 3–5 nodes. x = 170 + i*340 for 5 (skills/11).
const StepsScene: React.FC<{
  dur?: number; kicker?: string; title?: string; color?: string; note?: string;
  items?: { emoji: string; label: string; sub: string; c?: string }[];
}> = ({ dur, kicker = "FLOW", title = "", color = A.heat, note = "", items = [] }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const n = items.length;
  const w = n === 3 ? 420 : n === 4 ? 360 : 290;
  const gapX = n === 3 ? 560 : n === 4 ? 425 : 340;
  const x0 = n === 3 ? 190 : n === 4 ? 165 : 170;
  const y = 400;
  return (
    <Stage>
      <LBRHead kicker={kicker} title={title} color={color} o={p(0, 0.06)} />
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
              <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 29, color: c, marginTop: 8, lineHeight: 1.25 }}>{it.label}</div>
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

// ---------------------------------------------------------------- lbr_iconcards
const IconCardsScene: React.FC<{
  dur?: number; kicker?: string; title?: string; color?: string;
  items?: { emoji: string; k: string; v: string; chip?: string }[];
}> = ({ dur, kicker = "CONCEPTS", title = "", color = A.lead, items = [] }) => {
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
      <LBRHead kicker={kicker} title={title} color={color} o={p(0, 0.06)} />
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
              <span style={{ fontFamily: SANS, fontWeight: 800, fontSize: h > 250 ? 34 : 29, color, lineHeight: 1.25 }}>{it.k}</span>
            </div>
            <div style={{ fontFamily: SANS, fontSize: h > 250 ? 27 : 24, color: T.text, marginTop: 14, lineHeight: 1.4, opacity: 0.6 + o * 0.4 }}>{it.v}</div>
            {it.chip && (
              <div style={{ position: "absolute", right: 22, bottom: 18, fontFamily: MONO, fontWeight: 700, fontSize: 23,
                color: T.bg0, background: color, borderRadius: 999, padding: "8px 18px", opacity: o }}>{it.chip}</div>
            )}
          </div>
        );
      })}
    </Stage>
  );
};

// ---------------------------------------------------------------- lbr_compare3
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
      <LBRHead kicker={kicker} title={title} o={p(0, 0.06)} />
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
              <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 33, color: col.color, marginTop: 6, lineHeight: 1.25 }}>{col.name}</div>
            </div>
            <div style={{ marginTop: 22, display: "flex", flexDirection: "column", gap: 16 }}>
              {col.rows.map((r, ri) => (
                <div key={ri} style={{ opacity: p(at + 0.07 + ri * 0.03, at + 0.13 + ri * 0.03) }}>
                  <div style={{ fontFamily: MONO, fontSize: 22, color: T.muted, lineHeight: 1.35 }}>{r.k}</div>
                  <div style={{ fontFamily: SANS, fontWeight: 700, fontSize: 27, color: T.text, marginTop: 3, lineHeight: 1.35 }}>{r.v}</div>
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

// ---------------------------------------------------------------- lbr_checklist
const ChecklistScene: React.FC<{ dur?: number; kicker?: string; title?: string; color?: string; items?: string[]; icon?: string }> = ({
  dur, kicker = "CHECKLIST", title = "", color = A.green, items = [], icon = "✅",
}) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const n = items.length;
  const rowH = Math.min(112, Math.floor(600 / n) - 10);
  const totalH = n * (rowH + 14);
  const y0 = 210 + Math.max(0, (660 - totalH) / 2);
  const hot = Math.floor(frame / 30) % n;
  return (
    <Stage>
      <LBRHead kicker={kicker} title={title} color={color} o={p(0, 0.06)} />
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
            <span style={{ fontFamily: SANS, fontWeight: 700, fontSize: 30, color: T.text, lineHeight: 1.35 }}>{it}</span>
          </div>
        );
      })}
    </Stage>
  );
};

// ---------------------------------------------------------------- lbr_stats
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
      <LBRHead kicker={kicker} title={title} color={A.money} o={p(0, 0.06)} />
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
            <div style={{ fontFamily: SANS, fontSize: 27, color: T.muted, lineHeight: 1.35, minHeight: 76 }}>{s.label}</div>
            <div style={{ marginTop: 18 }}>
              <Counter p={p(at + 0.04, at + 0.22)} to={s.to} prefix={s.prefix || ""} suffix={s.suffix || ""} decimals={s.decimals || 0} color={c} size={n === 2 ? 84 : 64} />
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

// ---------------------------------------------------------------- lbr_stairs
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
      <LBRHead kicker={kicker} title={title} color={A.green} o={p(0, 0.06)} />
      {steps.map((s, i) => {
        const c = s.c || A.green;
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

// ================================================================ DOMAIN SCENES

// ---------------------------------------------------------------- lbr_loop
// The circular value chain: 5 stations around an ellipse, wired in a closed loop
// with Flow particles + a chase highlight. Closed loop = circular economy.
const LoopScene: React.FC<{
  dur?: number; kicker?: string; title?: string;
  stations?: { emoji: string; label: string; c?: string }[];
}> = ({ dur, kicker = "THE VALUE CHAIN", title = "వ్యాపార చక్రం", stations = [] }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const n = stations.length;
  const cx = 960, cy = 530, rx = 620, ry = 268;  // ry keeps bottom stations ≤ y880
  const pos = (i: number) => {
    const ang = (i / n) * Math.PI * 2 - Math.PI / 2;
    return { x: cx + Math.cos(ang) * rx, y: cy + Math.sin(ang) * ry };
  };
  const hot = Math.floor(frame / 26) % n;
  return (
    <Stage>
      <LBRHead kicker={kicker} title={title} color={A.heat} o={p(0, 0.06)} />
      <div style={{ position: "absolute", left: cx - 60, top: cy - 78, fontSize: 92, opacity: p(0.5, 0.62),
        textShadow: `0 0 ${30 + Math.sin(frame * 0.06) * 14}px ${mix(T.bg0, A.green, 0.6)}` }}>♻️</div>
      <div style={{ position: "absolute", left: cx - 220, top: cy + 20, width: 440, textAlign: "center", fontFamily: SANS, fontWeight: 800, fontSize: 30, color: A.green, opacity: p(0.55, 0.66) }}>
        క్లోజ్డ్ లూప్ — వ్యర్థం తిరిగి ముడిసరుకు
      </div>
      {stations.map((s, i) => {
        const c = s.c || A.heat;
        const a = pos(i), b = pos((i + 1) % n);
        const at = 0.08 + i * (0.5 / n);
        const o = p(at, at + 0.08);
        const ghost = p(0.03, 0.07);
        const active = hot === i && p(0.7, 0.71) > 0.5;
        return (
          <React.Fragment key={i}>
            <Wire x1={a.x} y1={a.y} x2={b.x} y2={b.y} p={p(at + 0.02, at + 0.1)} color={mix(c, A.green, 0.3)} w={3} arrow />
            <Flow x1={a.x} y1={a.y} x2={b.x} y2={b.y} color={mix(c, A.green, 0.3)} n={4} o={p(at + 0.05, at + 0.15)} />
            <div style={{ position: "absolute", left: a.x - 130, top: a.y - 62, width: 260, height: 124,
              borderRadius: 18, boxSizing: "border-box", padding: "14px 12px", textAlign: "center",
              background: mix(T.panel, c, o > 0.5 ? (active ? 0.18 : 0.1) : 0.02),
              border: `2.5px solid ${o > 0.5 ? mix(T.bg2, c, active ? 1 : 0.7) : T.bg2}`,
              opacity: Math.max(ghost * 0.22, o), transform: `scale(${active ? 1.06 : 1})`, zIndex: 2 }}>
              <div style={{ fontSize: 42 }}>{s.emoji}</div>
              <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 25, color: c, marginTop: 4, lineHeight: 1.2 }}>{s.label}</div>
              <div style={{ position: "absolute", top: -30, left: 10, fontFamily: MONO, fontWeight: 800, fontSize: 22, color: c, opacity: o }}>{i + 1}</div>
            </div>
          </React.Fragment>
        );
      })}
    </Stage>
  );
};

// ---------------------------------------------------------------- lbr_furnace
// Live smelting: scrap flows in → rotary furnace (rotating, glowing) → molten pour
// into ingot mould → ingots stack. Temperature counter. Continuous heat.
const FurnaceScene: React.FC<{ dur?: number; kicker?: string; title?: string; temp?: number; note?: string }> = ({
  dur, kicker = "PROCESS · SMELTING", title = "కొలిమిలో ఏం జరుగుతుంది?", temp = 1150, note = "",
}) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const fx = 820, fy = 360;                       // furnace box
  const pourOn = p(0.5, 0.58);
  const drip = (frame % 40) / 40;                  // molten drip cycle
  return (
    <Stage>
      <LBRHead kicker={kicker} title={title} color={A.heat} o={p(0, 0.06)} />
      {/* scrap feed in (left) */}
      <div style={{ position: "absolute", left: 150, top: 380, width: 240, textAlign: "center", opacity: p(0.08, 0.16) }}>
        <div style={{ fontSize: 74 }}>🔋</div>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 27, color: A.lead, marginTop: 6, lineHeight: 1.25 }}>లెడ్ స్క్రాప్ + పేస్ట్</div>
        <div style={{ fontFamily: SANS, fontSize: 23, color: T.muted, marginTop: 4 }}>+ కోక్, ఫ్లక్స్</div>
      </div>
      <Wire x1={400} y1={470} x2={fx - 8} y2={470} p={p(0.16, 0.24)} color={A.lead} w={4} />
      <Flow x1={400} y1={470} x2={fx - 8} y2={470} color={A.lead} n={5} o={p(0.2, 0.3)} />
      {/* rotary furnace */}
      <div style={{ position: "absolute", left: fx, top: fy, width: 300, height: 240, borderRadius: 26,
        background: `radial-gradient(circle at 50% 60%, ${mix(T.panel, A.heat, 0.5)}, ${mix(T.panel, A.heat, 0.12)})`,
        border: `3px solid ${A.heat}`, boxSizing: "border-box", overflow: "hidden",
        opacity: p(0.24, 0.34), boxShadow: `0 0 ${44 + Math.sin(frame * 0.12) * 20}px ${mix(T.bg0, A.heat, 0.5)}` }}>
        {/* rotating drum ribs */}
        <svg width={300} height={240} style={{ position: "absolute", left: 0, top: 0 }}>
          {Array.from({ length: 7 }).map((_, i) => {
            const a = frame * 0.06 + (i / 7) * Math.PI * 2;
            return <line key={i} x1={150} y1={150} x2={150 + Math.cos(a) * 96} y2={150 + Math.sin(a) * 70}
              stroke={mix(A.heat, T.text, 0.3)} strokeWidth={3} opacity={0.5} />;
          })}
          <circle cx={150} cy={150} r={12} fill={A.money} opacity={0.9} />
        </svg>
        <div style={{ position: "absolute", left: 0, right: 0, top: 12, textAlign: "center", fontFamily: MONO, fontWeight: 800, fontSize: 22, color: T.bg0, background: A.heat, padding: "4px 0" }}>ROTARY FURNACE</div>
      </div>
      <div style={{ position: "absolute", left: fx - 10, top: fy + 250, width: 320, textAlign: "center", opacity: p(0.3, 0.4) }}>
        <Counter p={p(0.34, 0.5)} to={temp} suffix=" °C" color={A.heat} size={48} />
        <div style={{ fontFamily: SANS, fontSize: 23, color: T.muted, marginTop: 2 }}>ఘనం → కరిగిన లోహం</div>
      </div>
      {/* molten pour → ingot mould (right) */}
      {pourOn > 0.3 && (
        <svg width={1920} height={1080} style={{ position: "absolute", left: 0, top: 0, overflow: "visible" }}>
          <line x1={fx + 300} y1={fy + 150} x2={1360} y2={fy + 150} stroke={A.heat} strokeWidth={5} opacity={pourOn} />
          <circle cx={fx + 300 + drip * 240} cy={fy + 150} r={7} fill={A.money} opacity={pourOn} />
        </svg>
      )}
      <div style={{ position: "absolute", left: 1360, top: 380, width: 300, textAlign: "center", opacity: p(0.56, 0.66) }}>
        <div style={{ fontSize: 74 }}>🧱</div>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 28, color: A.money, marginTop: 6, lineHeight: 1.25 }}>లెడ్ ఇంగోట్‌లు</div>
        <div style={{ fontFamily: SANS, fontSize: 23, color: T.muted, marginTop: 4 }}>ముడి / క్రూడ్ లెడ్</div>
      </div>
      {/* slag/dross note */}
      <div style={{ position: "absolute", left: fx - 30, top: fy - 74, fontFamily: MONO, fontSize: 21, color: A.risk, opacity: p(0.62, 0.72) }}>↑ పొగ → బ్యాగ్‌ఫిల్టర్ · స్లాగ్/డ్రాస్ వ్యర్థం</div>
      {note && (
        <div style={{ position: "absolute", left: 150, top: 780, width: 1620, textAlign: "center", opacity: p(0.76, 0.88) }}>
          <span style={{ fontFamily: SANS, fontWeight: 700, fontSize: 30, color: T.text, lineHeight: 1.4 }}>{note}</span>
        </div>
      )}
    </Stage>
  );
};

// ---------------------------------------------------------------- lbr_capex
// Capex breakdown: horizontal bars summing to a total (Counter). Values in ₹ lakh.
const CapexScene: React.FC<{
  dur?: number; kicker?: string; title?: string; unit?: string; total?: number; totalLabel?: string;
  items?: { label: string; v: number; color?: string }[]; note?: string;
}> = ({ dur, kicker = "INVESTMENT", title = "", unit = " లక్షలు", total = 0, totalLabel = "మొత్తం పెట్టుబడి",
  items = [], note = "" }) => {
  const p = useP(dur);
  const n = items.length;
  const maxV = Math.max(...items.map((i) => i.v), 1);
  const X0 = 620, BW = 900, rowH = Math.min(78, Math.floor(520 / n));
  const y0 = 250;
  return (
    <Stage>
      <LBRHead kicker={kicker} title={title} color={A.money} o={p(0, 0.06)} />
      {items.map((it, i) => {
        const c = it.color || A.money;
        const at = 0.1 + i * (0.55 / n);
        const grow = p(at, at + 0.12);
        const o = p(at - 0.02, at + 0.04);
        const y = y0 + i * (rowH + 16);
        return (
          <React.Fragment key={i}>
            <div style={{ position: "absolute", left: 130, top: y + rowH / 2 - 18, width: 470, textAlign: "right",
              fontFamily: SANS, fontWeight: 700, fontSize: 25, color: T.text, opacity: o, lineHeight: 1.25 }}>{it.label}</div>
            <div style={{ position: "absolute", left: X0, top: y, width: BW, height: rowH, borderRadius: 10,
              background: mix(T.panel, c, 0.05), border: `1.5px solid ${T.bg2}`, opacity: o, overflow: "hidden" }}>
              <div style={{ width: `${(it.v / maxV) * 100 * grow}%`, height: "100%",
                background: `linear-gradient(90deg, ${mix(c, T.bg1, 0.35)}, ${c})` }} />
            </div>
            <div style={{ position: "absolute", left: X0 + BW + 16, top: y + rowH / 2 - 18, width: 260,
              fontFamily: MONO, fontWeight: 800, fontSize: 27, color: c, opacity: grow }}>₹{it.v}{unit}</div>
          </React.Fragment>
        );
      })}
      <div style={{ position: "absolute", left: 620, top: y0 + n * (rowH + 16) + 20, width: 900, textAlign: "center", opacity: p(0.66, 0.78) }}>
        <div style={{ fontFamily: SANS, fontSize: 25, color: T.muted }}>{totalLabel}</div>
        <Counter p={p(0.7, 0.9)} to={total} prefix="≈ ₹" suffix={unit} color={A.heat} size={58} />
      </div>
      {note && (
        <div style={{ position: "absolute", left: 130, top: 852, width: 1660, textAlign: "center", opacity: p(0.8, 0.92) }}>
          <span style={{ fontFamily: SANS, fontSize: 24, color: T.muted, lineHeight: 1.35 }}>{note}</span>
        </div>
      )}
    </Stage>
  );
};

// ---------------------------------------------------------------- lbr_pnl
// Per-kg unit economics, HONEST mass balance: you buy 1 kg used battery but only
// recover ~0.6 kg lead, so net is NOT (leadPrice − scrapPrice). Two same-scaled
// bars (cost vs revenue per kg of INPUT) with legends below → tiny margin is visible.
const PnlScene: React.FC<{
  dur?: number; kicker?: string; title?: string;
  scrap?: number; processing?: number; leadOut?: number; ppOut?: number; epr?: number; net?: number; note?: string;
}> = ({ dur, kicker = "UNIT ECONOMICS · ₹/kg", title = "కిలోకు లెక్క (సుమారు)", scrap = 75, processing = 29,
  leadOut = 102, ppOut = 4, epr = 6, net = 8, note = "" }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const cost = [{ label: "స్క్రాప్ కొనుగోలు", v: scrap, c: A.lead }, { label: "నడిపే ఖర్చు (ఇంధనం, కూలీ, వడ్డీ)", v: processing, c: A.risk }];
  const rev = [{ label: "లెడ్ ఇంగోట్", v: leadOut, c: A.money }, { label: "ప్లాస్టిక్ PP", v: ppOut, c: A.lead }, { label: "EPR సర్టిఫికెట్", v: epr, c: A.green }];
  const costTot = scrap + processing, revTot = leadOut + ppOut + epr;
  const maxV = Math.max(costTot, revTot, 1);
  const X0 = 250, BW = 1250, SCALE = BW / maxV;
  const barH = 92;
  const Bar = (items: { label: string; v: number; c: string }[], y: number, at0: number, tot: number, cap: string, capColor: string) => {
    let acc = 0;
    return (
      <React.Fragment>
        <div style={{ position: "absolute", left: 130, top: y - 34, fontFamily: SANS, fontWeight: 800, fontSize: 25, color: capColor, opacity: p(at0 - 0.02, at0 + 0.04) }}>{cap}</div>
        {items.map((it, i) => {
          const at = at0 + i * 0.06;
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
        {/* total ₹ at bar end */}
        <div style={{ position: "absolute", left: X0 + tot * SCALE + 18, top: y + barH / 2 - 20, width: 200,
          fontFamily: MONO, fontWeight: 800, fontSize: 30, color: capColor, opacity: p(at0 + 0.12, at0 + 0.2) }}>₹{tot}</div>
        {/* legend below */}
        <div style={{ position: "absolute", left: X0, top: y + barH + 12, width: BW, display: "flex", gap: 26, flexWrap: "wrap" }}>
          {items.map((it, i) => (
            <div key={i} style={{ display: "flex", alignItems: "center", gap: 9, opacity: p(at0 + i * 0.06 + 0.04, at0 + i * 0.06 + 0.12) }}>
              <span style={{ width: 18, height: 18, borderRadius: 5, background: it.c, display: "inline-block" }} />
              <span style={{ fontFamily: MONO, fontWeight: 700, fontSize: 22, color: T.text }}>{it.label} · ₹{it.v}</span>
            </div>
          ))}
        </div>
      </React.Fragment>
    );
  };
  return (
    <Stage>
      <LBRHead kicker={kicker} title={title} color={A.money} o={p(0, 0.06)} />
      {Bar(cost, 268, 0.1, costTot, "1 kg బ్యాటరీకి ఖర్చు", A.risk)}
      {Bar(rev, 468, 0.36, revTot, "అదే కిలో నుండి రాబడి", A.green)}
      {/* net margin callout */}
      <div style={{ position: "absolute", left: 250, top: 664, width: 1250, height: 96, borderRadius: 16,
        background: mix(T.panel, A.green, 0.12), border: `2.5px solid ${A.green}`, boxSizing: "border-box",
        display: "flex", alignItems: "center", justifyContent: "space-between", padding: "0 40px",
        opacity: p(0.66, 0.76), boxShadow: `0 0 ${26 + Math.sin(frame * 0.07) * 12}px ${mix(T.bg0, A.green, 0.3)}` }}>
        <span style={{ fontFamily: SANS, fontWeight: 800, fontSize: 32, color: A.green }}>నికర మార్జిన్ (నెట్)</span>
        <Counter p={p(0.72, 0.88)} to={net} prefix="≈ ₹" suffix=" / kg" color={A.green} size={52} />
      </div>
      <div style={{ position: "absolute", left: 130, top: 782, width: 1660, textAlign: "center", opacity: p(0.8, 0.9) }}>
        <span style={{ fontFamily: SANS, fontSize: 24, color: T.muted, lineHeight: 1.35 }}>
          {note || "గమనిక: 1 kg బ్యాటరీ నుండి ~0.6 kg లెడ్ మాత్రమే వస్తుంది — అందుకే మార్జిన్ సన్నగా ఉంటుంది."}
        </span>
      </div>
    </Stage>
  );
};

// ---------------------------------------------------------------- dispatcher
export const LBRScene: React.FC<{ variant: string;[key: string]: unknown }> = ({ variant, ...rest }) => {
  let content: React.ReactNode = null;
  let accent = T.accent;
  switch (variant) {
    case "lbr_title": content = <TitleScene {...(rest as any)} />; break;
    case "lbr_ptitle": content = <PTitleScene {...(rest as any)} />; break;
    case "lbr_divider": content = <DividerScene {...(rest as any)} />; accent = ((rest as any).color as string) || A.heat; break;
    case "lbr_recap": content = <RecapScene {...(rest as any)} />; break;
    case "lbr_steps": content = <StepsScene {...(rest as any)} />; accent = ((rest as any).color as string) || A.heat; break;
    case "lbr_iconcards": content = <IconCardsScene {...(rest as any)} />; accent = ((rest as any).color as string) || A.lead; break;
    case "lbr_compare3": content = <Compare3Scene {...(rest as any)} />; break;
    case "lbr_checklist": content = <ChecklistScene {...(rest as any)} />; accent = ((rest as any).color as string) || A.green; break;
    case "lbr_stats": content = <StatsScene {...(rest as any)} />; accent = A.money; break;
    case "lbr_stairs": content = <StairsScene {...(rest as any)} />; accent = A.green; break;
    case "lbr_loop": content = <LoopScene {...(rest as any)} />; accent = A.heat; break;
    case "lbr_furnace": content = <FurnaceScene {...(rest as any)} />; accent = A.heat; break;
    case "lbr_capex": content = <CapexScene {...(rest as any)} />; accent = A.money; break;
    case "lbr_pnl": content = <PnlScene {...(rest as any)} />; accent = A.green; break;
    default:
      content = (
        <AbsoluteFill style={{ alignItems: "center", justifyContent: "center" }}>
          <div style={{ color: "#f88", fontFamily: MONO, fontSize: 40 }}>unknown lbr variant “{variant}”</div>
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
