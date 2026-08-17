/**
 * AUScenes.tsx — "Indian Auto & Auto-Components — company by company" (prefix `au`).
 *
 * A stock-market EDUCATION series built from the sector PDF: each company gets one
 * profile beat — what it does, its latest quarter, its valuation (P/E), and its moat.
 *
 * Identity (skills/04):
 *   theme accent = electric cyan (mobility / tech). Semantic accents:
 *     biz   cyan   #38BDF8 — the business / what they do
 *     up    green  #34D399 — growth, revenue up, profit
 *     down  rose   #FB7185 — decline, loss, risk
 *     val   amber  #FBBF24 — price / valuation / P/E
 *     moat  violet #A78BFA — competitive moat / durable edge
 *   Recurring motif: a tachometer gauge with a sweeping needle (GaugeMotif) — on
 *   title, dividers, every company card, recap. Continuous motion everywhere:
 *   gauge needle, road-dash march, Bg sweep, and a scene-progress bar (SceneProgress).
 *
 * Numbers are best-effort from public sources (Screener.in close 07-Aug-2026 for
 * price/PE; results-day coverage for revenue/PAT). On-screen disclaimer on title +
 * every card: "approx · verify on your terminal". Education only, not advice.
 */
import React from "react";
import { AbsoluteFill, useCurrentFrame } from "remotion";
import {
  makeTheme, mix, useP, usePop, rnd, MONO, SANS,
  Bg, Stage, Kicker, Counter,
} from "../lib/primitives";

const T = makeTheme({ accent: "#38BDF8" });
const A = { biz: "#38BDF8", up: "#34D399", down: "#FB7185", val: "#FBBF24", moat: "#A78BFA" };
const DISC = "Figures approx · verify on your terminal · educational, not investment advice";

// ---------------------------------------------------------------- motif
/** Tachometer gauge with a sweeping needle. The series' recurring identity mark. */
const GaugeMotif: React.FC<{ x: number; y: number; r: number; color?: string; o?: number }> = ({
  x, y, r, color = A.biz, o = 1,
}) => {
  const frame = useCurrentFrame();
  // needle sweeps 0..1 of a 240° arc, back and forth (revving)
  const t = (Math.sin(frame * 0.045) + 1) / 2;
  const a0 = Math.PI * 0.86, a1 = Math.PI * 2.14; // 155°..385°
  const na = a0 + (a1 - a0) * t;
  const cx = x + r, cy = y + r;
  const ticks = 11;
  return (
    <svg style={{ position: "absolute", left: x, top: y, overflow: "visible", opacity: o }} width={r * 2} height={r * 2}>
      {Array.from({ length: ticks }).map((_, i) => {
        const ta = a0 + (a1 - a0) * (i / (ticks - 1));
        const hot = i / (ticks - 1) > 0.72;
        const rr = r - 4, ri = r - (i % 2 === 0 ? 18 : 12);
        return (
          <line key={i} x1={cx + Math.cos(ta) * ri} y1={cy + Math.sin(ta) * ri}
            x2={cx + Math.cos(ta) * rr} y2={cy + Math.sin(ta) * rr}
            stroke={hot ? A.down : mix(T.bg2, color, 0.7)} strokeWidth={i % 2 === 0 ? 3 : 2} opacity={0.9} />
        );
      })}
      <circle cx={cx} cy={cy} r={r} fill="none" stroke={mix(T.bg2, color, 0.35)} strokeWidth={2} opacity={0.5} />
      <line x1={cx} y1={cy} x2={cx + Math.cos(na) * (r - 10)} y2={cy + Math.sin(na) * (r - 10)}
        stroke={color} strokeWidth={3.5} strokeLinecap="round" />
      <circle cx={cx} cy={cy} r={5} fill={color} />
    </svg>
  );
};

/** Continuous marching road dashes along the bottom — motion floor. */
const RoadDashes: React.FC<{ color?: string; o?: number }> = ({ color = A.biz, o = 0.5 }) => {
  const frame = useCurrentFrame();
  const y = 1012, seg = 120, n = 18;
  return (
    <div style={{ position: "absolute", left: 0, top: y, width: 1920, height: 8, opacity: o }}>
      {Array.from({ length: n }).map((_, i) => {
        const x = ((i * seg - frame * 6) % (n * seg) + n * seg) % (n * seg) - seg;
        return <div key={i} style={{ position: "absolute", left: x, top: 0, width: 64, height: 6, borderRadius: 4,
          background: mix(T.bg1, color, 0.55) }} />;
      })}
    </div>
  );
};

/** Bottom-edge scene-progress bar — the universal "this is playing" signal. */
const SceneProgress: React.FC<{ p: (a: number, b: number) => number; color?: string }> = ({ p, color = A.biz }) => (
  <div style={{ position: "absolute", left: 0, top: 1073, width: 1920, height: 7, background: "rgba(255,255,255,0.05)" }}>
    <div style={{ width: `${p(0, 1) * 100}%`, height: "100%",
      background: `linear-gradient(90deg, ${mix(color, T.bg1, 0.3)}, ${color})`, boxShadow: `0 0 12px ${color}` }} />
  </div>
);

// ---------------------------------------------------------------- shared bits
const Chip: React.FC<{ label: string; value: string; color: string; o?: number; big?: boolean }> = ({
  label, value, color, o = 1, big,
}) => (
  <div style={{ display: "flex", flexDirection: "column", gap: 3, opacity: o, padding: "8px 18px", borderRadius: 12,
    background: mix(T.panel, color, 0.1), border: `2px solid ${mix(T.bg2, color, 0.7)}` }}>
    <div style={{ fontFamily: MONO, fontSize: 15, letterSpacing: 2, color: T.muted, textTransform: "uppercase" }}>{label}</div>
    <div style={{ fontFamily: MONO, fontWeight: 800, fontSize: big ? 32 : 26, color }}>{value}</div>
  </div>
);

const YoY: React.FC<{ text: string; up: boolean; o?: number }> = ({ text, up, o = 1 }) => {
  const c = up ? A.up : A.down;
  return (
    <span style={{ display: "inline-flex", alignItems: "center", gap: 6, opacity: o, padding: "4px 12px", borderRadius: 20,
      background: mix(T.panel, c, 0.16), border: `1.5px solid ${c}`, fontFamily: MONO, fontWeight: 800, fontSize: 21, color: c }}>
      {up ? "▲" : "▼"} {text} <span style={{ color: T.muted, fontWeight: 600, fontSize: 16 }}>YoY</span>
    </span>
  );
};

// ---------------------------------------------------------------- title
const TitleScene: React.FC<{ dur?: number; title?: string; sub?: string; kicker?: string }> = ({
  dur, title = "", sub = "", kicker = "",
}) => {
  const p = useP(dur); const pop = usePop(dur);
  return (
    <Stage>
      <GaugeMotif x={1560} y={120} r={90} o={p(0.1, 0.4)} />
      <div style={{ position: "absolute", left: 120, top: 300, right: 120 }}>
        <div style={{ opacity: p(0.02, 0.12) }}><Kicker theme={T} text={kicker} color={A.val} /></div>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 118, letterSpacing: -3, color: T.text,
          marginTop: 22, lineHeight: 1.02, transform: `scale(${0.9 + pop(0.1) * 0.1})`, transformOrigin: "left" }}>
          {title.split("\n").map((l, i) => (
            <div key={i} style={i === 1 ? { color: A.biz, textShadow: `0 0 40px ${A.biz}66` } : undefined}>{l}</div>
          ))}
        </div>
        <div style={{ height: 6, borderRadius: 3, marginTop: 24, width: p(0.2, 0.5) * 560,
          background: `linear-gradient(90deg, ${A.biz}, ${A.moat})` }} />
        <div style={{ fontFamily: SANS, fontWeight: 500, fontSize: 37, color: T.muted, marginTop: 26, opacity: p(0.4, 0.6) }}>{sub}</div>
      </div>
      <div style={{ position: "absolute", left: 120, top: 968, fontFamily: MONO, fontSize: 21, color: T.muted, opacity: p(0.6, 0.75) }}>
        ⚠ {DISC}
      </div>
      <RoadDashes o={p(0.3, 0.6) * 0.6} />
      <SceneProgress p={p} color={A.val} />
    </Stage>
  );
};

// ---------------------------------------------------------------- divider
const DividerScene: React.FC<{ dur?: number; part?: string; title?: string; sub?: string; color?: string; pips?: number; at?: number }> = ({
  dur, part = "", title = "", sub = "", color = A.biz, pips = 5, at = 1,
}) => {
  const p = useP(dur); const pop = usePop(dur);
  return (
    <Stage>
      <GaugeMotif x={1580} y={130} r={86} color={color} o={p(0.1, 0.4)} />
      <div style={{ position: "absolute", left: 0, right: 0, top: 360, textAlign: "center" }}>
        <div style={{ fontFamily: MONO, fontWeight: 700, letterSpacing: 8, fontSize: 26, color, opacity: p(0.05, 0.2) }}>{part}</div>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 92, letterSpacing: -2, color: T.text, marginTop: 16,
          transform: `scale(${0.92 + pop(0.12) * 0.08})` }}>{title}</div>
        <div style={{ height: 6, width: p(0.25, 0.55) * 420, background: color, borderRadius: 3, margin: "22px auto 0" }} />
        <div style={{ fontFamily: SANS, fontSize: 32, color: T.muted, marginTop: 24, opacity: p(0.4, 0.62) }}>{sub}</div>
        <div style={{ display: "flex", gap: 14, justifyContent: "center", marginTop: 40, opacity: p(0.5, 0.7) }}>
          {Array.from({ length: pips }).map((_, i) => (
            <div key={i} style={{ width: i + 1 === at ? 46 : 14, height: 14, borderRadius: 8,
              background: i + 1 === at ? color : mix(T.bg2, color, 0.3) }} />
          ))}
        </div>
      </div>
      <RoadDashes color={color} o={p(0.3, 0.6) * 0.6} />
      <SceneProgress p={p} color={color} />
    </Stage>
  );
};

// ---------------------------------------------------------------- company profile (the core scene)
type Fin = {
  qlabel: string; pending?: boolean;
  rev?: { to: number; yoy?: string; up?: boolean };
  pat?: { to: number; yoy?: string; up?: boolean; loss?: boolean; label?: string };
  note?: string;
};
const MOAT_C: Record<string, string> = { WIDE: A.up, DEEP: A.up, NARROW: A.val, EMERGING: A.biz, WEAK: A.down, NONE: A.down };

const CompanyScene: React.FC<{
  dur?: number; idx?: string; name?: string; ticker?: string; price?: string; pe?: string;
  seg?: string; biz?: string[]; fin?: Fin; moat?: string; moatStrength?: string; kicker?: string;
}> = ({ dur, idx = "", name = "", ticker = "", price = "", pe = "", seg = "",
  biz = [], fin, moat = "", moatStrength = "NARROW", kicker = "VEHICLE MAKERS" }) => {
  const p = useP(dur);
  const frame = useCurrentFrame();
  const mc = MOAT_C[moatStrength] || A.moat;

  return (
    <Stage>
      {/* header */}
      <div style={{ position: "absolute", left: 100, top: 50, right: 100, opacity: p(0, 0.05) }}>
        <Kicker theme={T} text={`${kicker} · ${idx}`} color={A.biz} />
      </div>
      <div style={{ position: "absolute", left: 100, top: 88, fontFamily: SANS, fontWeight: 800, fontSize: 52,
        letterSpacing: -1.5, color: T.text, opacity: p(0.01, 0.07) }}>{name}</div>
      <GaugeMotif x={1716} y={44} r={58} o={p(0.05, 0.2)} />

      {/* valuation strip */}
      <div style={{ position: "absolute", left: 100, top: 196, display: "flex", gap: 16, alignItems: "center" }}>
        <div style={{ opacity: p(0.03, 0.1) }}><Chip label="NSE" value={ticker} color={A.biz} /></div>
        <div style={{ opacity: p(0.06, 0.13) }}><Chip label="Price · 07-Aug" value={price} color={A.val} big /></div>
        <div style={{ opacity: p(0.09, 0.16) }}><Chip label="P/E" value={pe} color={A.val} big /></div>
        <div style={{ opacity: p(0.12, 0.19), padding: "10px 20px", borderRadius: 12, background: mix(T.panel, A.biz, 0.08),
          border: `2px solid ${mix(T.bg2, A.biz, 0.5)}`, fontFamily: SANS, fontWeight: 700, fontSize: 24, color: A.biz }}>
          {seg}
        </div>
      </div>

      {/* LEFT — the business */}
      <div style={{ position: "absolute", left: 100, top: 300, width: 800, opacity: p(0.1, 0.2) }}>
        <div style={{ fontFamily: MONO, fontSize: 20, letterSpacing: 3, color: A.biz, textTransform: "uppercase" }}>▸ What they do</div>
      </div>
      {biz.map((b, i) => {
        const at = 0.12 + i * 0.07;
        return (
          <div key={i} style={{ position: "absolute", left: 100, top: 344 + i * 112, width: 800, minHeight: 84,
            display: "flex", gap: 16, alignItems: "flex-start", opacity: p(at, at + 0.08),
            transform: `translateX(${(1 - p(at, at + 0.08)) * -18}px)`, padding: "14px 20px", borderRadius: 14,
            background: mix(T.panel, A.biz, 0.05), border: `1.5px solid ${mix(T.bg2, A.biz, 0.35)}` }}>
            <div style={{ width: 10, height: 10, borderRadius: 6, background: A.biz, marginTop: 8, flexShrink: 0,
              boxShadow: `0 0 12px ${A.biz}` }} />
            <div style={{ fontFamily: SANS, fontWeight: 500, fontSize: 27, color: T.text, lineHeight: 1.32 }}>{b}</div>
          </div>
        );
      })}

      {/* RIGHT — latest quarter */}
      <div style={{ position: "absolute", left: 952, top: 300, width: 868, opacity: p(0.3, 0.4) }}>
        <div style={{ fontFamily: MONO, fontSize: 20, letterSpacing: 3, color: A.up, textTransform: "uppercase" }}>
          ▸ Latest quarter{fin?.pending ? "  ·  results due" : ""}
        </div>
        <div style={{ fontFamily: MONO, fontSize: 20, color: T.muted, marginTop: 6 }}>{fin?.qlabel || ""}</div>
      </div>
      {fin?.rev && (
        <div style={{ position: "absolute", left: 952, top: 372, width: 868, opacity: p(0.34, 0.44),
          padding: "18px 26px", borderRadius: 16, background: mix(T.panel, A.up, 0.07), border: `2px solid ${mix(T.bg2, A.up, 0.5)}` }}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
            <div style={{ fontFamily: SANS, fontWeight: 700, fontSize: 24, color: T.muted }}>Revenue</div>
            {fin.rev.yoy && <YoY text={fin.rev.yoy} up={fin.rev.up ?? true} o={p(0.44, 0.52)} />}
          </div>
          <div style={{ marginTop: 4 }}>
            <Counter p={p(0.36, 0.56)} to={fin.rev.to} prefix="₹" suffix=" cr" color={A.up} size={52} comma />
          </div>
        </div>
      )}
      {fin?.pat && (
        <div style={{ position: "absolute", left: 952, top: fin?.rev ? 512 : 372, width: 868, opacity: p(0.42, 0.52),
          padding: "18px 26px", borderRadius: 16, background: mix(T.panel, fin.pat.loss ? A.down : A.up, 0.07),
          border: `2px solid ${mix(T.bg2, fin.pat.loss ? A.down : A.up, 0.5)}` }}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
            <div style={{ fontFamily: SANS, fontWeight: 700, fontSize: 24, color: T.muted }}>{fin.pat.label || "Net profit"}</div>
            {fin.pat.yoy && <YoY text={fin.pat.yoy} up={fin.pat.up ?? true} o={p(0.52, 0.6)} />}
          </div>
          <div style={{ marginTop: 4 }}>
            <Counter p={p(0.44, 0.64)} to={fin.pat.to} prefix="₹" suffix=" cr" color={fin.pat.loss ? A.down : A.up} size={52} comma />
          </div>
        </div>
      )}
      {/* pending / results-due placeholder — fills the financial column when no numbers yet */}
      {fin && !fin.rev && !fin.pat && (
        <div style={{ position: "absolute", left: 952, top: 372, width: 868, opacity: p(0.32, 0.44),
          padding: "22px 28px", borderRadius: 16, background: mix(T.panel, A.val, 0.06),
          border: `2px dashed ${mix(T.bg2, A.val, 0.65)}` }}>
          <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
            <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 30, color: A.val }}>⏳ Results awaited</div>
          </div>
          {fin.note && (
            <div style={{ fontFamily: SANS, fontSize: 25, color: T.text, lineHeight: 1.4, marginTop: 12, opacity: p(0.4, 0.5) }}>
              {fin.note}
            </div>
          )}
        </div>
      )}
      {fin?.note && fin?.rev && (
        <div style={{ position: "absolute", left: 952, top: fin?.pat ? 680 : 540, width: 868,
          fontFamily: SANS, fontSize: 22, color: T.muted, lineHeight: 1.35, opacity: p(0.6, 0.7) }}>{fin.note}</div>
      )}

      {/* MOAT — full-width bottom */}
      <div style={{ position: "absolute", left: 100, top: 754, width: 1720, minHeight: 150, opacity: p(0.6, 0.7),
        padding: "20px 28px", borderRadius: 18, background: mix(T.panel, mc, 0.12), border: `2.5px solid ${mc}`,
        boxShadow: p(0.7, 0.85) > 0.5 ? `0 0 ${26 + Math.sin(frame * 0.07) * 12}px ${mix(T.bg0, mc, 0.3)}` : "none" }}>
        <div style={{ display: "flex", alignItems: "center", gap: 16 }}>
          <div style={{ fontFamily: MONO, fontSize: 20, letterSpacing: 3, color: mc, textTransform: "uppercase" }}>🛡 Moat</div>
          <div style={{ padding: "3px 14px", borderRadius: 20, background: mix(T.panel, mc, 0.2), border: `1.5px solid ${mc}`,
            fontFamily: MONO, fontWeight: 800, fontSize: 18, color: mc }}>{moatStrength}</div>
        </div>
        <div style={{ fontFamily: SANS, fontWeight: 600, fontSize: 28, color: T.text, lineHeight: 1.34, marginTop: 12 }}>{moat}</div>
      </div>

      <div style={{ position: "absolute", left: 100, top: 966, fontFamily: MONO, fontSize: 17, color: T.muted, opacity: p(0.5, 0.65) }}>
        ⚠ {DISC}
      </div>
      <RoadDashes o={0.5} />
      <SceneProgress p={p} />
    </Stage>
  );
};

// ---------------------------------------------------------------- recap
const RecapScene: React.FC<{ dur?: number; title?: string; items?: string[]; closer?: string; color?: string }> = ({
  dur, title = "", items = [], closer = "", color = A.biz,
}) => {
  const p = useP(dur);
  return (
    <Stage>
      <GaugeMotif x={1600} y={90} r={78} color={color} o={p(0.1, 0.4) * 0.7} />
      <div style={{ position: "absolute", left: 0, right: 0, top: 96, textAlign: "center", opacity: p(0.02, 0.12) }}>
        <Kicker theme={T} text="RECAP · THE LINE-UP" color={color} cx />
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 60, letterSpacing: -1.5, color: T.text, marginTop: 14 }}>{title}</div>
      </div>
      <div style={{ position: "absolute", left: 260, top: 250, width: 1400 }}>
        {items.map((it, i) => {
          const at = 0.12 + i * 0.08;
          return (
            <div key={i} style={{ display: "flex", gap: 18, alignItems: "center", marginBottom: 16, opacity: p(at, at + 0.08),
              transform: `translateX(${(1 - p(at, at + 0.08)) * -20}px)` }}>
              <div style={{ width: 40, height: 40, borderRadius: 10, flexShrink: 0, background: mix(T.panel, color, 0.18),
                border: `2px solid ${color}`, fontFamily: MONO, fontWeight: 800, fontSize: 20, color,
                display: "flex", alignItems: "center", justifyContent: "center" }}>{i + 1}</div>
              <div style={{ fontFamily: SANS, fontWeight: 500, fontSize: 29, color: T.text, lineHeight: 1.3 }}>{it}</div>
            </div>
          );
        })}
      </div>
      {closer && (
        <div style={{ position: "absolute", left: 160, right: 160, top: 936, textAlign: "center", opacity: p(0.78, 0.9) }}>
          <span style={{ fontFamily: SANS, fontStyle: "italic", fontWeight: 700, fontSize: 34, color,
            textShadow: `0 0 30px ${color}55` }}>{closer}</span>
        </div>
      )}
      <RoadDashes color={color} o={0.5} />
      <SceneProgress p={p} color={color} />
    </Stage>
  );
};

// ---------------------------------------------------------------- dispatcher
export const AUScene: React.FC<{ variant: string;[key: string]: unknown }> = ({ variant, ...rest }) => {
  let content: React.ReactNode = null;
  let accent = A.biz;
  switch (variant) {
    case "au_title": content = <TitleScene {...(rest as any)} />; accent = A.val; break;
    case "au_divider": content = <DividerScene {...(rest as any)} />; accent = ((rest as any).color as string) || A.biz; break;
    case "au_company": content = <CompanyScene {...(rest as any)} />; break;
    case "au_recap": content = <RecapScene {...(rest as any)} />; accent = ((rest as any).color as string) || A.biz; break;
    default:
      content = (
        <AbsoluteFill style={{ alignItems: "center", justifyContent: "center" }}>
          <div style={{ color: "#f88", fontFamily: MONO, fontSize: 40 }}>unknown au variant "{variant}"</div>
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
