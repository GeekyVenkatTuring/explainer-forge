/**
 * GWScenes.tsx — "How to invest in international (US) stock markets from India" (prefix `gw`, English).
 *
 * India-context investor education (LRS / RBI / TCS / taxes) — read skills/12-market-research.md §5.
 *
 * Identity (skills/04):
 *   theme accent = saffron (India / the rupee). Semantic accents:
 *     inr   saffron #F59E0B — India, the rupee, your money at home
 *     usd   blue    #4F86F7 — US / world markets, the dollar
 *     cost  rose    #FB7185 — costs, fees, money leaving
 *     tax   violet  #A78BFA — tax, rules, compliance
 *     ok    green   #34D399 — growth, your money working, the good path
 *   Recurring motif: a globe with a ₹ and $ orbiting it (GlobeOrbit) — title,
 *   dividers, recap. Every content scene carries a bottom scene-progress bar.
 *   Two bespoke COMPUTED heroes: the LRS money-pipe (gw_pipe) and the cost
 *   waterfall (gw_fees).
 */
import React from "react";
import { AbsoluteFill, interpolate, useCurrentFrame } from "remotion";
import {
  makeTheme, mix, useP, usePop, rnd, MONO, SANS,
  Bg, Stage, Head, Kicker, Flow, Wire, Counter, Brackets, ScanBeam,
} from "../lib/primitives";

const T = makeTheme({ accent: "#F59E0B" });
const A = { inr: "#F59E0B", usd: "#4F86F7", cost: "#FB7185", tax: "#A78BFA", ok: "#34D399" };

// ---------------------------------------------------------------- motif: GlobeOrbit
const GlobeOrbit: React.FC<{ cx?: number; cy?: number; o?: number; scale?: number }> = ({
  cx = 960, cy = 540, o = 1, scale = 1,
}) => {
  const frame = useCurrentFrame();
  return (
    <div style={{ position: "absolute", left: 0, top: 0, width: 1920, height: 1080, opacity: o, pointerEvents: "none" }}>
      {Array.from({ length: 14 }).map((_, i) => {
        const ang = frame * 0.008 + (i / 14) * Math.PI * 2;
        const rupee = i % 2 === 0;
        const rx = (560 + i * 8) * scale, ry = (270 + i * 5) * scale;
        return (
          <div key={i} style={{
            position: "absolute", left: cx + Math.cos(ang) * rx - 12, top: cy + Math.sin(ang) * ry - 12,
            fontFamily: MONO, fontWeight: 800, fontSize: 24, color: rupee ? A.inr : A.usd,
            opacity: 0.12 + rnd(i, 3) * 0.2, textShadow: `0 0 12px ${rupee ? A.inr : A.usd}`,
          }}>{rupee ? "₹" : "$"}</div>
        );
      })}
    </div>
  );
};

const GWProgress: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur);
  return (
    <div style={{ position: "absolute", left: 0, bottom: 0, height: 6, width: `${p(0, 1) * 100}%`,
      background: `linear-gradient(90deg, ${A.inr}, ${A.usd})`, opacity: 0.55 }} />
  );
};

// ---------------------------------------------------------------- gw_title
const TitleScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur);
  const pop = usePop(dur);
  return (
    <AbsoluteFill style={{ alignItems: "center", justifyContent: "center" }}>
      <GlobeOrbit o={p(0.08, 0.24)} />
      <div style={{ textAlign: "center", transform: `scale(${0.92 + pop(0) * 0.08})`, zIndex: 2 }}>
        <div style={{ display: "flex", justifyContent: "center", marginBottom: 26 }}>
          <Kicker theme={T} text="INVESTING FROM INDIA · FULL GUIDE" cx />
        </div>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 108, lineHeight: 1.06, letterSpacing: -3, color: T.text }}>
          <div>Invest in the <span style={{ color: A.usd, textShadow: `0 0 60px ${mix(T.bg0, A.usd, 0.7)}` }}>US Market</span></div>
          <div>from <span style={{ color: A.inr, textShadow: `0 0 60px ${mix(T.bg0, A.inr, 0.7)}` }}>India</span></div>
        </div>
        <div style={{ height: 6, width: interpolate(p(0.18, 0.45), [0, 1], [0, 640]), background: `linear-gradient(90deg, ${A.inr}, ${A.usd})`, borderRadius: 3, margin: "30px auto" }} />
        <div style={{ fontFamily: SANS, fontSize: 35, color: T.muted, opacity: p(0.28, 0.5), lineHeight: 1.4 }}>
          Is it legal? · Which platforms? · Every cost &amp; tax — end to end
        </div>
      </div>
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------- gw_routes (2-panel overview)
const RoutesScene: React.FC<{
  dur?: number; kicker?: string; title?: string;
  left?: { label: string; sub: string; items: string[] };
  right?: { label: string; sub: string; items: string[] };
}> = ({
  dur, kicker = "TWO DOORS", title = "Two ways in",
  left = { label: "Direct", sub: "you own the actual US shares", items: ["Send rupees abroad under LRS", "Buy real US stocks — even fractions", "Apps: INDmoney, Vested, Groww, IBKR"] },
  right = { label: "Indirect", sub: "invest in rupees, on Indian exchanges", items: ["No LRS, no dollar transfer", "India-listed ETFs & mutual funds", "They hold the US stocks for you"] },
}) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const cols = [{ ...left, color: A.usd, emoji: "🎯" }, { ...right, color: A.ok, emoji: "🧺" }];
  return (
    <Stage>
      <Head theme={T} kicker={kicker} title={title} color={A.inr} o={p(0, 0.06)} />
      {cols.map((col, i) => {
        const at = 0.1 + i * 0.16;
        const o = p(at, at + 0.1);
        return (
          <div key={i} style={{
            position: "absolute", left: 240 + i * 720, top: 235, width: 720, height: 630,
            borderRadius: 22, boxSizing: "border-box", padding: "30px 36px",
            opacity: o, transform: `translateY(${(1 - o) * 24}px)`,
            background: mix(T.panel, col.color, o > 0.5 ? 0.09 : 0.02), border: `2.5px solid ${o > 0.5 ? col.color : T.bg2}`,
          }}>
            <div style={{ display: "flex", alignItems: "center", gap: 16 }}>
              <span style={{ fontSize: 56 }}>{col.emoji}</span>
              <div>
                <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 40, color: col.color, lineHeight: 1.1 }}>{col.label}</div>
                <div style={{ fontFamily: SANS, fontSize: 24, color: T.muted, marginTop: 4 }}>{col.sub}</div>
              </div>
            </div>
            <div style={{ marginTop: 26, display: "flex", flexDirection: "column", gap: 18 }}>
              {col.items.map((it, ri) => {
                const io = p(at + 0.08 + ri * 0.05, at + 0.16 + ri * 0.05);
                return (
                  <div key={ri} style={{ display: "flex", alignItems: "flex-start", gap: 14, opacity: io }}>
                    <span style={{ color: col.color, fontFamily: MONO, fontWeight: 800, fontSize: 26, marginTop: 2 }}>›</span>
                    <span style={{ fontFamily: SANS, fontWeight: 600, fontSize: 28, color: T.text, lineHeight: 1.35 }}>{it}</span>
                  </div>
                );
              })}
            </div>
            <div style={{ position: "absolute", left: 0, right: 0, bottom: -1, height: 8, borderRadius: 4, background: col.color, opacity: (0.4 + Math.sin(frame * 0.08 + i) * 0.25) * (o > 0.6 ? 1 : 0) }} />
          </div>
        );
      })}
      <GWProgress dur={dur} />
    </Stage>
  );
};

// ---------------------------------------------------------------- gw_pipe (bespoke: the LRS money route)
const PipeScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const nodes = [
    { emoji: "🧑‍💻", label: "You, in India", sub: "with rupees (₹)", c: A.inr },
    { emoji: "🏦", label: "Your bank", sub: "starts the transfer", c: A.inr },
    { emoji: "🛂", label: "LRS gateway", sub: "up to $250,000 / year", c: A.tax },
    { emoji: "🌎", label: "US broker a/c", sub: "held in your name", c: A.usd },
    { emoji: "📈", label: "US stocks", sub: "Apple, Nvidia, S&P 500…", c: A.ok },
  ];
  const n = 5, w = 280, gapX = 360, x0 = 100, y = 360;
  return (
    <Stage>
      <Head theme={T} kicker="IS IT EVEN LEGAL? · YES" title="How your money actually reaches Wall Street" color={A.usd} o={p(0, 0.06)} />
      {nodes.map((it, i) => {
        const at = 0.08 + i * 0.1;
        const o = p(at, at + 0.08);
        const x = x0 + i * gapX;
        const gate = i === 2;
        const active = Math.floor(frame / 22) % n === i && p(0.72, 0.73) > 0.5;
        return (
          <React.Fragment key={i}>
            {i > 0 && (
              <>
                <Wire x1={x0 + (i - 1) * gapX + w} y1={y + 105} x2={x - 8} y2={y + 105} p={p(at - 0.05, at)} color={it.c} w={3} />
                <Flow x1={x0 + (i - 1) * gapX + w} y1={y + 105} x2={x - 8} y2={y + 105} color={i <= 2 ? A.inr : A.usd} n={5} o={p(at, at + 0.1)} />
              </>
            )}
            <div style={{ position: "absolute", left: x, top: y, width: w, height: 230,
              borderRadius: 18, boxSizing: "border-box", padding: "22px 18px", textAlign: "center",
              background: mix(T.panel, it.c, o > 0.5 ? (gate || active ? 0.16 : 0.09) : 0.02),
              border: `${gate ? 3 : 2.5}px solid ${o > 0.5 ? mix(T.bg2, it.c, gate || active ? 1 : 0.7) : T.bg2}`,
              opacity: o, transform: `translateY(${(1 - o) * 20}px) scale(${active ? 1.04 : 1})`,
              boxShadow: gate && o > 0.6 ? `0 0 ${34 + Math.sin(frame * 0.08) * 12}px ${mix(T.bg0, A.tax, 0.4)}` : "none" }}>
              <div style={{ fontSize: 50 }}>{it.emoji}</div>
              <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 27, color: it.c, marginTop: 8, lineHeight: 1.2 }}>{it.label}</div>
              <div style={{ fontFamily: SANS, fontSize: 22, color: T.muted, marginTop: 6, lineHeight: 1.3 }}>{it.sub}</div>
            </div>
          </React.Fragment>
        );
      })}
      {/* the ₹ → $ conversion label under the gate */}
      <div style={{ position: "absolute", left: x0 + 2 * gapX - 40, top: y + 250, width: 360, textAlign: "center", opacity: p(0.5, 0.6) }}>
        <span style={{ fontFamily: MONO, fontWeight: 800, fontSize: 30, color: A.inr }}>₹</span>
        <span style={{ fontFamily: MONO, fontSize: 26, color: T.muted }}> → </span>
        <span style={{ fontFamily: MONO, fontWeight: 800, fontSize: 30, color: A.usd }}>$</span>
        <div style={{ fontFamily: MONO, fontSize: 20, color: T.muted, marginTop: 2 }}>rupees converted here</div>
      </div>
      <div style={{ position: "absolute", left: 150, top: 800, width: 1620, textAlign: "center", opacity: p(0.78, 0.9) }}>
        <span style={{ fontFamily: SANS, fontWeight: 700, fontSize: 31, color: T.text, lineHeight: 1.4 }}>
          It's fully legal under the RBI's <span style={{ color: A.tax, fontWeight: 800 }}>Liberalised Remittance Scheme</span> — the account abroad is yours.
        </span>
      </div>
      <GWProgress dur={dur} />
    </Stage>
  );
};

// ---------------------------------------------------------------- gw_fees (bespoke: cost waterfall)
const FeeStackScene: React.FC<{
  dur?: number; kicker?: string; title?: string; gross?: number;
  steps?: { label: string; delta: number; c: string; note?: string }[]; note?: string;
}> = ({
  dur, kicker = "WHAT IT COSTS", title = "Put in ₹1,00,000 — what actually gets invested?", gross = 100000,
  steps = [
    { label: "Forex markup (~1%)", delta: -1000, c: A.cost, note: "₹→$ conversion spread" },
    { label: "TCS (20% > ₹10L/yr)", delta: 0, c: A.tax, note: "₹0 here — below ₹10L; and refundable" },
    { label: "Brokerage", delta: 0, c: A.cost, note: "₹0 on many apps" },
  ],
  note = "Under ₹10 lakh a year, TCS is zero — and even above it, TCS is refundable against your income tax.",
}) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  // running balance after each deduction (computed)
  let bal = gross;
  const bars = [{ label: "You send", val: gross, c: A.inr, delta: gross, note: "gross amount" } as { label: string; val: number; c: string; delta: number; note?: string }];
  steps.forEach((s) => { bal += s.delta; bars.push({ label: s.label, val: bal, c: s.c, delta: s.delta, note: s.note }); });
  const net = bal;
  const maxV = gross;
  const X0 = 150, W = 1620, top = 300, H = 300, baseY = top + H;
  const bw = W / bars.length - 40;
  return (
    <Stage>
      <Head theme={T} kicker={kicker} title={title} color={A.cost} o={p(0, 0.06)} />
      {bars.map((b, i) => {
        const at = 0.12 + i * (0.5 / bars.length);
        const o = p(at, at + 0.09);
        const h = (b.val / maxV) * H * o;
        const x = X0 + i * (W / bars.length) + 20;
        const isNet = i === bars.length - 1;
        return (
          <React.Fragment key={i}>
            <div style={{ position: "absolute", left: x, top: baseY - h, width: bw, height: h,
              borderRadius: "12px 12px 0 0",
              background: `linear-gradient(180deg, ${isNet ? A.ok : b.c}, ${mix(isNet ? A.ok : b.c, T.bg1, 0.5)})`,
              border: `2.5px solid ${isNet ? A.ok : b.c}`, borderBottom: "none", opacity: 0.35 + o * 0.65,
              boxShadow: isNet && o > 0.8 ? `0 0 ${30 + Math.sin(frame * 0.08) * 12}px ${mix(T.bg0, A.ok, 0.4)}` : "none" }} />
            {/* value on top */}
            <div style={{ position: "absolute", left: x - 10, top: baseY - h - 46, width: bw + 20, textAlign: "center", opacity: o }}>
              <Counter p={p(at + 0.02, at + 0.14)} to={b.val} prefix="₹" color={isNet ? A.ok : b.c} size={30} />
            </div>
            {/* label + note under axis */}
            <div style={{ position: "absolute", left: x - 10, top: baseY + 16, width: bw + 20, textAlign: "center", opacity: o }}>
              <div style={{ fontFamily: SANS, fontWeight: 700, fontSize: 23, color: isNet ? A.ok : T.text, lineHeight: 1.25 }}>{b.label}</div>
              {b.note && <div style={{ fontFamily: MONO, fontSize: 18, color: T.muted, marginTop: 5, lineHeight: 1.3 }}>{b.note}</div>}
              {i > 0 && !isNet && b.delta !== 0 && (
                <div style={{ fontFamily: MONO, fontWeight: 700, fontSize: 20, color: A.cost, marginTop: 3 }}>−₹{Math.abs(b.delta)}</div>
              )}
            </div>
          </React.Fragment>
        );
      })}
      <svg width={1920} height={1080} style={{ position: "absolute", left: 0, top: 0 }}>
        <line x1={X0} y1={baseY} x2={X0 + W} y2={baseY} stroke={T.bg2} strokeWidth={2} />
      </svg>
      <div style={{ position: "absolute", left: 150, top: 800, width: 1620, textAlign: "center", opacity: p(0.72, 0.84) }}>
        <span style={{ fontFamily: SANS, fontWeight: 700, fontSize: 29, color: T.text, lineHeight: 1.4 }}>{note}</span>
      </div>
      <GWProgress dur={dur} />
    </Stage>
  );
};

// ---------------------------------------------------------------- gw_steps (generic pipeline)
const StepsScene: React.FC<{
  dur?: number; kicker?: string; title?: string; color?: string; note?: string;
  items?: { emoji: string; label: string; sub: string; c?: string }[];
}> = ({ dur, kicker = "HOW IT WORKS", title = "", color = A.usd, note = "", items = [] }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const n = items.length;
  const cfg = n === 3 ? { w: 420, gapX: 560, x0: 190 } : n === 4 ? { w: 360, gapX: 425, x0: 165 } : { w: 280, gapX: 360, x0: 100 };
  const { w, gapX, x0 } = cfg;
  const y = 400;
  return (
    <Stage>
      <Head theme={T} kicker={kicker} title={title} color={color} o={p(0, 0.06)} />
      {items.map((it, i) => {
        const c = it.c || color;
        const at = 0.1 + i * (0.55 / n);
        const o = p(at, at + 0.08);
        const x = x0 + i * gapX;
        const active = Math.floor(frame / 24) % n === i && p(0.7, 0.71) > 0.5;
        return (
          <React.Fragment key={i}>
            {i > 0 && (
              <>
                <Wire x1={x0 + (i - 1) * gapX + w} y1={y + 105} x2={x - 8} y2={y + 105} p={p(at - 0.05, at)} color={c} w={3} />
                <Flow x1={x0 + (i - 1) * gapX + w} y1={y + 105} x2={x - 8} y2={y + 105} color={c} n={4} o={p(at, at + 0.1)} />
              </>
            )}
            <div style={{ position: "absolute", left: x, top: y, width: w, height: 230,
              borderRadius: 18, boxSizing: "border-box", padding: "22px 18px", textAlign: "center",
              background: mix(T.panel, c, o > 0.5 ? (active ? 0.16 : 0.09) : 0.02),
              border: `2.5px solid ${o > 0.5 ? mix(T.bg2, c, active ? 1 : 0.7) : T.bg2}`,
              opacity: Math.max(p(0.03, 0.07) * 0.22, o), transform: `translateY(${(1 - o) * 20}px) scale(${active ? 1.04 : 1})` }}>
              <div style={{ fontSize: 46 }}>{it.emoji}</div>
              <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: n >= 5 ? 25 : 28, color: c, marginTop: 8, lineHeight: 1.2 }}>{it.label}</div>
              <div style={{ fontFamily: SANS, fontSize: n >= 5 ? 20 : 22, color: T.muted, marginTop: 6, lineHeight: 1.32 }}>{it.sub}</div>
            </div>
          </React.Fragment>
        );
      })}
      {note && (
        <div style={{ position: "absolute", left: 150, top: 730, width: 1620, textAlign: "center", opacity: p(0.72, 0.84) }}>
          <span style={{ fontFamily: SANS, fontWeight: 700, fontSize: 31, color: T.text, lineHeight: 1.4 }}>{note}</span>
        </div>
      )}
      <GWProgress dur={dur} />
    </Stage>
  );
};

// ---------------------------------------------------------------- gw_cards (generic iconcards)
const CardsScene: React.FC<{
  dur?: number; kicker?: string; title?: string; color?: string;
  items?: { emoji: string; k: string; v: string; chip?: string }[];
}> = ({ dur, kicker = "", title = "", color = A.usd, items = [] }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const cols = items.length > 4 ? 3 : 2;
  const rows = Math.ceil(items.length / cols);
  const w = cols === 2 ? 810 : 533, gap = 24;
  const h = rows === 2 ? 320 : 210;
  const y0 = 210 + (660 - (rows * h + (rows - 1) * gap)) / 2;
  const hot = Math.floor(frame / 32) % items.length;
  return (
    <Stage>
      <Head theme={T} kicker={kicker} title={title} color={color} o={p(0, 0.06)} />
      {items.map((it, i) => {
        const r = Math.floor(i / cols), c = i % cols;
        const at = 0.1 + i * (0.55 / items.length);
        const o = p(at, at + 0.09);
        const ghost = p(0.03, 0.07);
        const active = hot === i && p(0.74, 0.75) > 0.5;
        return (
          <div key={i} style={{
            position: "absolute", left: 130 + c * (w + gap), top: y0 + r * (h + gap), width: w, height: h,
            borderRadius: 20, boxSizing: "border-box", padding: "26px 30px",
            opacity: Math.max(ghost * 0.22, o), transform: `translateY(${(1 - o) * 22}px) scale(${active ? 1.02 : 1})`,
            background: mix(T.panel, color, o > 0.5 ? (active ? 0.15 : 0.08) : 0.02),
            border: `2.5px solid ${o > 0.5 ? mix(T.bg2, color, active ? 1 : 0.65) : T.bg2}`,
          }}>
            <div style={{ display: "flex", alignItems: "center", gap: 20 }}>
              <span style={{ fontSize: h > 250 ? 60 : 46 }}>{it.emoji}</span>
              <span style={{ fontFamily: SANS, fontWeight: 800, fontSize: h > 250 ? 34 : 29, color, lineHeight: 1.22 }}>{it.k}</span>
            </div>
            <div style={{ fontFamily: SANS, fontSize: h > 250 ? 27 : 24, color: T.text, marginTop: 16, lineHeight: 1.4, opacity: 0.55 + o * 0.45 }}>{it.v}</div>
            {it.chip && (
              <div style={{ position: "absolute", right: 24, bottom: 20, fontFamily: MONO, fontWeight: 700, fontSize: 22,
                color: T.bg0, background: color, borderRadius: 999, padding: "8px 18px", opacity: o }}>{it.chip}</div>
            )}
          </div>
        );
      })}
      <GWProgress dur={dur} />
    </Stage>
  );
};

// ---------------------------------------------------------------- gw_stats (generic stat cards)
const StatsScene: React.FC<{
  dur?: number; kicker?: string; title?: string; note?: string; color?: string;
  stats?: { label: string; to: number; prefix?: string; suffix?: string; decimals?: number; color?: string; sub?: string }[];
}> = ({ dur, kicker = "BY THE NUMBERS", title = "", note = "", color = A.inr, stats = [] }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const n = stats.length;
  const w = n === 2 ? 810 : n === 3 ? 533 : 390;
  const y0 = note ? 270 : 320;
  return (
    <Stage>
      <Head theme={T} kicker={kicker} title={title} color={color} o={p(0, 0.06)} />
      {stats.map((s, i) => {
        const at = 0.1 + i * (0.5 / n);
        const o = p(at, at + 0.1);
        const ghost = p(0.03, 0.07);
        const c = s.color || color;
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
              <Counter p={p(at + 0.04, at + 0.22)} to={s.to} prefix={s.prefix || ""} suffix={s.suffix || ""} decimals={s.decimals || 0} color={c} size={n === 2 ? 80 : 62} />
            </div>
            {s.sub && <div style={{ fontFamily: SANS, fontSize: 23, color: T.text, marginTop: 18, lineHeight: 1.4, opacity: p(at + 0.12, at + 0.2) }}>{s.sub}</div>}
          </div>
        );
      })}
      {note && (
        <div style={{ position: "absolute", left: 130, top: 700, width: 1660, textAlign: "center", opacity: p(0.68, 0.8) }}>
          <span style={{ fontFamily: SANS, fontWeight: 700, fontSize: 30, color: T.text, lineHeight: 1.4 }}>{note}</span>
        </div>
      )}
      <GWProgress dur={dur} />
    </Stage>
  );
};

// ---------------------------------------------------------------- gw_compare (2 or 3 columns)
const CompareScene: React.FC<{
  dur?: number; kicker?: string; title?: string; color?: string;
  cols?: { name: string; color: string; emoji?: string; hi?: boolean; rows: { k: string; v: string }[] }[];
}> = ({ dur, kicker = "SIDE BY SIDE", title = "", color = A.usd, cols = [] }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const n = cols.length;
  const w = n === 2 ? 720 : 520;
  const x0 = n === 2 ? 240 : 140;
  const gapX = n === 2 ? 720 : 560;
  return (
    <Stage>
      <Head theme={T} kicker={kicker} title={title} color={color} o={p(0, 0.06)} />
      {cols.map((col, i) => {
        const at = 0.08 + i * 0.14;
        const o = p(at, at + 0.1);
        const ghost = p(0.03, 0.07);
        return (
          <div key={i} style={{
            position: "absolute", left: x0 + i * gapX, top: 230, width: w, height: 640,
            borderRadius: 20, boxSizing: "border-box", padding: "26px 30px",
            opacity: Math.max(ghost * 0.22, o), transform: `translateY(${(1 - o) * 24}px)`,
            background: mix(T.panel, col.color, o > 0.5 ? 0.08 : 0.02),
            border: `2.5px solid ${o > 0.5 ? col.color : T.bg2}`,
          }}>
            <div style={{ textAlign: "center" }}>
              <div style={{ fontSize: 52 }}>{col.emoji}</div>
              <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 32, color: col.color, marginTop: 6, lineHeight: 1.2 }}>{col.name}</div>
            </div>
            <div style={{ marginTop: 22, display: "flex", flexDirection: "column", gap: 15 }}>
              {col.rows.map((r, ri) => (
                <div key={ri} style={{ opacity: p(at + 0.07 + ri * 0.035, at + 0.13 + ri * 0.035) }}>
                  <div style={{ fontFamily: MONO, fontSize: 20, color: T.muted, lineHeight: 1.3 }}>{r.k}</div>
                  <div style={{ fontFamily: SANS, fontWeight: 700, fontSize: 26, color: T.text, marginTop: 3, lineHeight: 1.3 }}>{r.v}</div>
                </div>
              ))}
            </div>
            {col.hi && (
              <div style={{ position: "absolute", left: 0, right: 0, bottom: -1, height: 8, borderRadius: 4, background: col.color, opacity: 0.5 + Math.sin(frame * 0.08) * 0.3 }} />
            )}
          </div>
        );
      })}
      <GWProgress dur={dur} />
    </Stage>
  );
};

// ---------------------------------------------------------------- gw_divider
const TOTAL_PARTS = 5;
const DividerScene: React.FC<{ dur?: number; n?: number; title?: string; sub?: string; color?: string }> = ({
  dur, n = 1, title = "", sub = "", color = A.inr,
}) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  return (
    <Stage>
      <GlobeOrbit o={p(0.2, 0.34) * 0.7} scale={1.15} />
      <Brackets x={310} y={290} w={1300} h={490} color={color} o={p(0.02, 0.12)} len={54} />
      <ScanBeam theme={T} x={320} y={300} w={1280} h={470} color={color} o={p(0.05, 0.2)} speed={1.6} />
      <div style={{ position: "absolute", left: 0, right: 0, top: 350, textAlign: "center" }}>
        <div style={{ fontFamily: MONO, fontWeight: 800, fontSize: 34, color, letterSpacing: 10, opacity: p(0.05, 0.15) }}>
          PART {"0" + n}
        </div>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 84, color: T.text, letterSpacing: -2, marginTop: 20, opacity: p(0.12, 0.24), transform: `translateY(${(1 - p(0.12, 0.24)) * 30}px)` }}>{title}</div>
        <div style={{ height: 5, width: interpolate(p(0.2, 0.5), [0, 1], [0, 460]), background: color, borderRadius: 3, margin: "26px auto" }} />
        <div style={{ fontFamily: SANS, fontSize: 32, color: T.muted, opacity: p(0.3, 0.45), lineHeight: 1.4 }}>{sub}</div>
      </div>
      <div style={{ position: "absolute", left: 0, right: 0, top: 850, display: "flex", justifyContent: "center", gap: 14, opacity: p(0.3, 0.45) }}>
        {Array.from({ length: TOTAL_PARTS }).map((_, idx) => {
          const i = idx + 1;
          return (
            <div key={i} style={{ width: i === n ? 42 : 13, height: 13, borderRadius: 8,
              background: i <= n ? color : mix(T.panel, color, 0.15), border: `1.5px solid ${i <= n ? color : T.bg2}`,
              opacity: i === n ? 0.7 + Math.sin(frame * 0.1) * 0.3 : 1 }} />
          );
        })}
      </div>
    </Stage>
  );
};

// ---------------------------------------------------------------- gw_recap
const RecapScene: React.FC<{ dur?: number; items?: string[]; closer?: string; title?: string }> = ({
  dur, items = [], closer = "The world is investable from India — go in with eyes open.", title = "The whole guide in one breath",
}) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  return (
    <AbsoluteFill style={{ padding: "54px 130px", justifyContent: "center" }}>
      <GlobeOrbit o={0.22} scale={1.2} />
      <div style={{ opacity: p(0, 0.06), textAlign: "center", marginBottom: 22, zIndex: 2 }}>
        <Kicker theme={T} text="RECAP" cx />
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 56, color: T.text, marginTop: 12, letterSpacing: -1.5 }}>{title}</div>
      </div>
      <div style={{ display: "flex", flexDirection: "column", gap: 11, maxWidth: 1460, margin: "0 auto", width: "100%", zIndex: 2 }}>
        {items.map((it, i) => {
          const at = 0.06 + i * 0.07;
          const o = p(at, at + 0.07);
          const accent = [A.usd, A.inr, A.cost, A.tax, A.ok][i % 5];
          return (
            <div key={i} style={{ display: "flex", alignItems: "center", gap: 18,
              opacity: Math.max(p(0.02, 0.06) * 0.25, o), transform: `translateX(${(1 - o) * -26}px)`,
              background: mix(T.panel, accent, 0.06), border: `1.5px solid ${mix(T.bg2, accent, o * 0.5)}`,
              borderLeft: `4px solid ${o > 0.5 ? accent : T.bg2}`, borderRadius: 12, padding: "13px 26px" }}>
              <span style={{ color: accent, fontFamily: MONO, fontWeight: 700, fontSize: 25 }}>{i + 1}</span>
              <span style={{ fontFamily: SANS, fontSize: 28, color: T.text, lineHeight: 1.3 }}>{it}</span>
            </div>
          );
        })}
      </div>
      <div style={{ textAlign: "center", marginTop: 26, opacity: p(0.8, 0.9), zIndex: 2 }}>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontStyle: "italic", fontSize: 37, color: A.ok, textShadow: `0 0 ${28 + Math.sin(frame * 0.06) * 14}px ${mix(T.bg0, A.ok, 0.7)}` }}>{closer}</div>
      </div>
    </AbsoluteFill>
  );
};

// ===========================================================================
export const GWScene: React.FC<{ variant: string;[key: string]: unknown }> = ({ variant, ...rest }) => {
  let content: React.ReactNode;
  let accent = A.inr;
  switch (variant) {
    case "gw_title": content = <TitleScene {...(rest as any)} />; break;
    case "gw_routes": content = <RoutesScene {...(rest as any)} />; accent = A.usd; break;
    case "gw_pipe": content = <PipeScene {...(rest as any)} />; accent = A.usd; break;
    case "gw_fees": content = <FeeStackScene {...(rest as any)} />; accent = A.cost; break;
    case "gw_steps": content = <StepsScene {...(rest as any)} />; accent = (rest as any).color || A.usd; break;
    case "gw_cards": content = <CardsScene {...(rest as any)} />; accent = (rest as any).color || A.usd; break;
    case "gw_stats": content = <StatsScene {...(rest as any)} />; accent = (rest as any).color || A.inr; break;
    case "gw_compare": content = <CompareScene {...(rest as any)} />; accent = (rest as any).color || A.usd; break;
    case "gw_divider": content = <DividerScene {...(rest as any)} />; accent = (rest as any).color || A.inr; break;
    case "gw_recap": content = <RecapScene {...(rest as any)} />; accent = A.ok; break;
    default: content = <TitleScene {...(rest as any)} />;
  }
  return (
    <AbsoluteFill>
      <Bg theme={T} accent={accent} />
      {content}
    </AbsoluteFill>
  );
};

export default GWScene;
