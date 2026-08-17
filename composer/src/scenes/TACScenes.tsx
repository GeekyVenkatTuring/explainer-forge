/**
 * TACScenes.tsx — "Technical Analysis: Reading the Market's Own Language"
 * Full course, prefix `tac`. ~20 min / 32 scenes.
 *
 * Identity: night-sky dark + CANDLESTICK MOTIF.
 * Semantic accents (consistent throughout):
 *   C  #22D3EE  cyan   — chart structure / price / axis
 *   G  #34D399  green  — bullish / support / confirmation
 *   R  #FB7185  rose   — bearish / resistance / caution
 *   Y  #FBBF24  amber  — indicators (MA, RSI, MACD, Volume, BB)
 *   V  #A78BFA  violet — named pattern labels / theory
 */
import React from "react";
import { useCurrentFrame, interpolate } from "remotion";
import {
  makeTheme, mix, MONO, SANS, useP, usePop, rnd,
  Stage, Bg, Head, Foot, Wire, Flow, Counter, Type, ScanBeam, Brackets,
} from "../lib/primitives";

const T = makeTheme({});
const C = "#22D3EE", G = "#34D399", R = "#FB7185", Y = "#FBBF24", V = "#A78BFA";
type OHLC = { o: number; c: number; h: number; l: number };

// ──────────────── data helpers (module-scope, deterministic)
function makeOHLC(n: number, seed: number, drift: number, vol: number, start = 300): OHLC[] {
  let px = start;
  return Array.from({ length: n }, (_, i) => {
    const d = drift + (rnd(i, 1, seed) - 0.5) * vol;
    const o = px, c2 = px + d; px = c2;
    return { o, c: c2, h: Math.max(o, c2) + rnd(i, 2, seed) * vol * 0.28, l: Math.min(o, c2) - rnd(i, 3, seed) * vol * 0.28 };
  });
}
function fromClose(closes: number[], seed: number, wf = 0.18): OHLC[] {
  return closes.map((c2, i) => {
    const o = i === 0 ? c2 * 0.999 : closes[i - 1];
    const rng = Math.abs(c2 - o) + 1;
    return { o, c: c2, h: Math.max(o, c2) + rng * wf * rnd(i, 1, seed), l: Math.min(o, c2) - rng * wf * rnd(i, 2, seed) };
  });
}
function smaArr(d: OHLC[], w: number): number[] {
  return d.map((_, i) => { const s = d.slice(Math.max(0, i - w + 1), i + 1); return s.reduce((a, k) => a + k.c, 0) / s.length; });
}
function emaOHLC(d: OHLC[], w: number): number[] {
  const k = 2 / (w + 1); const out: number[] = [];
  d.forEach((x, i) => out.push(i === 0 ? x.c : x.c * k + out[i - 1] * (1 - k)));
  return out;
}
function emaVals(vals: number[], w: number): number[] {
  const k = 2 / (w + 1); const out: number[] = [];
  vals.forEach((v, i) => out.push(i === 0 ? v : v * k + out[i - 1] * (1 - k)));
  return out;
}

// ──────────────── precomputed series
const TREND_UP = makeOHLC(36, 1, 2.6, 12, 280);
const TF_1H   = makeOHLC(40, 20, 0.3,  4, 300);
const TF_DAY  = makeOHLC(25, 21, 2.0, 10, 300);
const TF_WEEK = makeOHLC(12, 22, 8.0, 14, 300);

// SR scene — explicit closes with 3 clear SR levels
const SR_CLOSES = [280,291,299,307,303,297,301,308,302,298,302,309,314,308,301,305,311,318,325,332,326,320,326,333,340,334,329,335,341,347,341,335,340,347,353,345];
const SR_SERIES = fromClose(SR_CLOSES, 15, 0.12);
const SR_SUP1 = 299, SR_SUP2 = 312, SR_RES = 353;

// H&S
const HS_CLOSES = [100,104,108,105,103,106,112,118,115,109,103,106,109,107,103,99,94,89];
const HS_SERIES = fromClose(HS_CLOSES, 7, 0.16);
const HS_NECK = 103, HS_HEAD_PEAK = 118;

// Double Top
const DT_CLOSES = [100,106,113,119,121,117,112,109,112,117,121,118,113,108,102,96];
const DT_SERIES = fromClose(DT_CLOSES, 8, 0.14);

// Bull Flag
const FLAG_CLOSES = [100,109,119,129,140,150,158,154,149,145,141,144,150,158,167,175];
const FLAG_SERIES = fromClose(FLAG_CLOSES, 9, 0.11);

// Ascending Triangle
const TRI_CLOSES = [104,113,120,116,112,115,120,118,115,118,120,119,118,119,120,122,129,136];
const TRI_SERIES = fromClose(TRI_CLOSES, 10, 0.10);

// MA cross: down → base → up (SMA-10 crosses SMA-30 near index 42)
const MA_CLOSES: number[] = [];
for (let i = 0; i < 60; i++) {
  if (i < 18) MA_CLOSES.push(252 - i * 2.5 + (rnd(i, 0, 5) - 0.5) * 7);
  else if (i < 38) MA_CLOSES.push(207 + (rnd(i, 0, 5) - 0.5) * 9);
  else MA_CLOSES.push(207 + (i - 38) * 2.7 + (rnd(i, 0, 5) - 0.5) * 7);
}
const MA_SERIES = fromClose(MA_CLOSES, 5, 0.14);
const MA_SMA10 = smaArr(MA_SERIES, 10);
const MA_SMA30 = smaArr(MA_SERIES, 30);

// RSI
const RSI_BASE = makeOHLC(46, 11, 1.2, 18, 240);
const RSI_VALS = RSI_BASE.map((_, i) => {
  const w = RSI_BASE.slice(Math.max(0, i - 9), i + 1);
  let up = 0, dn = 0;
  w.forEach((k) => { const d = k.c - k.o; if (d > 0) up += d; else dn -= d; });
  return dn === 0 ? 83 : 100 - 100 / (1 + up / dn);
});

// MACD
const MACD_BASE = makeOHLC(52, 12, 1.0, 15, 235);
const MACD_EMA12 = emaOHLC(MACD_BASE, 12);
const MACD_EMA26 = emaOHLC(MACD_BASE, 26);
const MACD_LINE = MACD_EMA12.map((v, i) => v - MACD_EMA26[i]);
const MACD_SIGNAL = emaVals(MACD_LINE, 9);
const MACD_HIST = MACD_LINE.map((v, i) => v - MACD_SIGNAL[i]);

// Bollinger Bands
const BB_BASE = makeOHLC(40, 13, 0.4, 20, 255);
const BB_SMA = smaArr(BB_BASE, 10);
const BB_UPPER = BB_BASE.map((_, i) => {
  const sl = BB_BASE.slice(Math.max(0, i - 9), i + 1).map((k) => k.c);
  const avg = sl.reduce((a, v) => a + v, 0) / sl.length;
  const std = Math.sqrt(sl.reduce((a, v) => a + (v - avg) ** 2, 0) / sl.length);
  return BB_SMA[i] + 2 * std;
});
const BB_LOWER = BB_BASE.map((_, i) => {
  const sl = BB_BASE.slice(Math.max(0, i - 9), i + 1).map((k) => k.c);
  const avg = sl.reduce((a, v) => a + v, 0) / sl.length;
  const std = Math.sqrt(sl.reduce((a, v) => a + (v - avg) ** 2, 0) / sl.length);
  return BB_SMA[i] - 2 * std;
});

// Volume data
const VOL_DATA = TREND_UP.map((k, i) => ({ v: 22 + rnd(i, 5, 3) * 70, up: k.c >= k.o }));

// Doji exact specs
const DOJI_SPECS = [
  { o: 100, c: 100.3, h: 113, l: 87,  name: "Standard Doji",  sub: "Equal bulls & bears" },
  { o: 100, c: 100.3, h: 101, l: 74,  name: "Dragonfly Doji", sub: "Demand found at lows" },
  { o: 100, c: 100.3, h: 127, l: 99.8,name: "Gravestone Doji",sub: "Supply found at highs" },
  { o: 100, c: 100.3, h: 126, l: 74,  name: "Long-Legged",    sub: "Maximum uncertainty" },
];
const DOJI_PMIN = 72, DOJI_PMAX = 130;

// ──────────────── shared Browser chrome
const Browser: React.FC<{
  url: string; color: string; o: number;
  x?: number; y?: number; w?: number; h?: number; children?: React.ReactNode;
}> = ({ url, color, o, x = 210, y = 205, w = 1500, h = 680, children }) => {
  const frame = useCurrentFrame();
  return (
    <div style={{ position: "absolute", left: x, top: y, width: w, height: h, borderRadius: 20,
      background: mix(T.bg1, color, 0.04), border: `2.5px solid ${mix(T.line, color, 0.5)}`,
      boxShadow: `0 0 ${34 + Math.sin(frame * 0.05) * 10}px ${mix(T.bg0, color, 0.3)}`,
      opacity: o, transform: `translateY(${(1 - o) * 24}px)`, overflow: "hidden" }}>
      <div style={{ height: 54, background: mix(T.bg0, color, 0.08), borderBottom: `2px solid ${mix(T.line, color, 0.35)}`,
        display: "flex", alignItems: "center", gap: 10, padding: "0 22px" }}>
        {[R, Y, G].map((cc, i) => <div key={i} style={{ width: 13, height: 13, borderRadius: 7, background: mix(cc, T.bg0, 0.3) }} />)}
        <div style={{ marginLeft: 16, height: 30, borderRadius: 999, background: mix(T.bg0, color, 0.14),
          border: `1.5px solid ${mix(T.line, color, 0.45)}`, display: "flex", alignItems: "center",
          padding: "0 16px", minWidth: 340 }}>
          <span style={{ fontFamily: MONO, fontSize: 19, color: mix(T.muted, color, 0.45), letterSpacing: 0.3 }}>{url}</span>
        </div>
        <div style={{ marginLeft: "auto", fontFamily: MONO, fontWeight: 700, fontSize: 18, color: T.bg0,
          background: mix(color, T.bg0, 0.12), borderRadius: 8, padding: "3px 11px", letterSpacing: 2 }}>DEMO DATA</div>
      </div>
      <div style={{ position: "relative", height: h - 54 }}>{children}</div>
    </div>
  );
};

// ──────────────── CandleChart (renders N candles in a bounding box on Stage coords)
const CandleChart: React.FC<{
  data: OHLC[]; nC: number;
  bx: number; by: number; bw: number; bh: number;
  upC?: string; dnC?: string; glowLast?: boolean;
}> = ({ data, nC, bx, by, bw, bh, upC = G, dnC = R, glowLast = true }) => {
  const n = data.length;
  const pmin = Math.min(...data.map((k) => k.l));
  const pmax = Math.max(...data.map((k) => k.h));
  const cx = (i: number) => bx + (i + 0.5) * (bw / n);
  const py = (v: number) => by + ((pmax - v) / (pmax - pmin)) * bh;
  const cw = Math.max(5, (bw / n) * 0.62);
  return (
    <>
      {data.slice(0, nC).map((k, i) => {
        const up = k.c >= k.o;
        const col = up ? upC : dnC;
        const bt = py(Math.max(k.o, k.c));
        const bHt = Math.max(2, py(Math.min(k.o, k.c)) - bt);
        return (
          <React.Fragment key={i}>
            <div style={{ position: "absolute", left: cx(i) - 1.5, top: py(k.h), width: 3,
              height: Math.max(2, py(k.l) - py(k.h)), background: col, opacity: 0.8 }} />
            <div style={{ position: "absolute", left: cx(i) - cw / 2, top: bt, width: cw, height: bHt,
              borderRadius: 2, background: col,
              boxShadow: glowLast && i === nC - 1 ? `0 0 10px ${col}` : "none" }} />
          </React.Fragment>
        );
      })}
    </>
  );
};

// helper: price→pixel Y inside a bounded chart area
function makePY(data: OHLC[], by: number, bh: number) {
  const pmin = Math.min(...data.map((k) => k.l));
  const pmax = Math.max(...data.map((k) => k.h));
  return (v: number) => by + ((pmax - v) / (pmax - pmin)) * bh;
}
function makeCX(n: number, bx: number, bw: number) {
  return (i: number) => bx + (i + 0.5) * (bw / n);
}

// ════════════════════════════════════════════ 1. TITLE
const TitleScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur); const frame = useCurrentFrame(); const pop = usePop(dur);
  // decorative floating candles (motif) — 6 mini body+wick shapes at edges
  const candleMotif = [
    { x: 120, y: 140, h: 120, bh: 48, c: G }, { x: 1720, y: 200, h: 100, bh: 38, c: C },
    { x: 80,  y: 760, h: 90,  bh: 36, c: R }, { x: 1760, y: 700, h: 110, bh: 44, c: Y },
    { x: 450, y: 960, h: 80,  bh: 30, c: V }, { x: 1400, y: 940, h: 85,  bh: 34, c: C },
  ];
  return (
    <Stage>
      <Bg theme={T} accent={C} />
      {/* motif candles — continuous breathing glow */}
      {candleMotif.map((m, i) => (
        <div key={i} style={{ position: "absolute", left: m.x, top: m.y,
          opacity: 0.18 + Math.sin(frame * 0.04 + i * 1.3) * 0.08 }}>
          <div style={{ width: 3, height: (m.h - m.bh) / 2, background: m.c, margin: "0 auto" }} />
          <div style={{ width: 18, height: m.bh, borderRadius: 3, background: m.c }} />
          <div style={{ width: 3, height: (m.h - m.bh) / 2, background: m.c, margin: "0 auto" }} />
        </div>
      ))}
      {/* kicker */}
      <div style={{ position: "absolute", left: 0, right: 0, top: 270, textAlign: "center",
        fontFamily: MONO, fontWeight: 800, fontSize: 22, color: C, letterSpacing: 10,
        opacity: p(0.04, 0.14), transform: `translateY(${(1 - p(0.04, 0.14)) * 20}px)` }}>
        TRADING EDUCATION · FULL COURSE
      </div>
      {/* headline */}
      <div style={{ position: "absolute", left: 0, right: 0, top: 322, textAlign: "center",
        fontFamily: SANS, fontWeight: 800, fontSize: 110, color: T.text, letterSpacing: -3,
        opacity: p(0.10, 0.22), transform: `scale(${0.92 + pop(0.10) * 0.08})` }}>
        TECHNICAL
      </div>
      <div style={{ position: "absolute", left: 0, right: 0, top: 444, textAlign: "center",
        fontFamily: SANS, fontWeight: 800, fontSize: 128, letterSpacing: -4,
        color: C, textShadow: `0 0 60px ${mix(T.bg0, C, 0.7)}`,
        opacity: p(0.18, 0.32), transform: `scale(${0.92 + pop(0.18) * 0.08})` }}>
        ANALYSIS
      </div>
      {/* underline */}
      <div style={{ position: "absolute", left: "50%", top: 590,
        width: interpolate(p(0.28, 0.52), [0, 1], [0, 520]), height: 5,
        background: `linear-gradient(90deg, ${C}, ${mix(C, V, 0.5)})`,
        borderRadius: 3, transform: "translateX(-50%)" }} />
      {/* subtitle */}
      <div style={{ position: "absolute", left: 300, right: 300, top: 618, textAlign: "center",
        fontFamily: SANS, fontSize: 36, color: T.muted, letterSpacing: 0.5,
        opacity: p(0.36, 0.54) }}>
        Charts · Candlesticks · Patterns · Indicators — End to End
      </div>
      {/* disclaimer tag */}
      <div style={{ position: "absolute", left: 0, right: 0, top: 686, textAlign: "center",
        fontFamily: MONO, fontSize: 21, color: R, opacity: p(0.55, 0.70) }}>
        ⚠ Education only — not investment advice — consult a SEBI-registered advisor
      </div>
    </Stage>
  );
};

// ════════════════════════════════════════════ 2. DIVIDER (parameterised)
const DividerScene: React.FC<{ dur?: number; n?: number; title?: string; sub?: string; color?: string }> = ({
  dur, n = 1, title = "", sub = "", color = C,
}) => {
  const frame = useCurrentFrame(); const p = useP(dur);
  return (
    <Stage>
      <Bg theme={T} accent={color} />
      <Brackets x={330} y={290} w={1260} h={500} color={color} o={p(0.02, 0.14)} len={54} />
      <ScanBeam theme={T} x={340} y={300} w={1240} h={480} color={color} o={p(0.05, 0.18)} speed={1.5} />
      <div style={{ position: "absolute", left: 0, right: 0, top: 350, textAlign: "center" }}>
        <div style={{ fontFamily: MONO, fontWeight: 800, fontSize: 30, color, letterSpacing: 10,
          opacity: p(0.05, 0.16) }}>PART {String(n).padStart(2, "0")}</div>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 96, color: T.text, letterSpacing: -2,
          marginTop: 16, opacity: p(0.12, 0.26), transform: `translateY(${(1 - p(0.12, 0.26)) * 28}px)` }}>{title}</div>
        <div style={{ height: 5, width: interpolate(p(0.22, 0.52), [0, 1], [0, 460]),
          background: color, borderRadius: 3, margin: "22px auto" }} />
        <div style={{ fontFamily: SANS, fontSize: 32, color: T.muted, opacity: p(0.32, 0.48) }}>{sub}</div>
      </div>
      <div style={{ position: "absolute", left: 0, right: 0, top: 856,
        display: "flex", justifyContent: "center", gap: 14, opacity: p(0.32, 0.48) }}>
        {[1, 2, 3, 4, 5, 6].map((i) => (
          <div key={i} style={{ width: i === n ? 44 : 14, height: 14, borderRadius: 8,
            background: i <= n ? color : mix(T.panel, color, 0.15),
            border: `1.5px solid ${i <= n ? color : T.line}`,
            opacity: i === n ? 0.7 + Math.sin(frame * 0.1) * 0.3 : 1 }} />
        ))}
      </div>
    </Stage>
  );
};

// ════════════════════════════════════════════ 3. WHY TA
const WhyTAScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur); const frame = useCurrentFrame();
  const headlines = ["📰 Analysts say BUY — target 25,000", "🔑 Fundamentals strong", "💼 FII bullish on sector"];
  const tick = (frame * 1.2) % (headlines.length * 480);
  // mini downward chart data for left panel
  const DOWN_MINI = makeOHLC(18, 30, -1.8, 8, 120);
  const dPmin = Math.min(...DOWN_MINI.map((k) => k.l));
  const dPmax = Math.max(...DOWN_MINI.map((k) => k.h));
  const dY = (v: number) => 80 + ((dPmax - v) / (dPmax - dPmin)) * 120;
  const dX = (i: number) => 20 + (i + 0.5) * (500 / 18);
  const nDMini = Math.round(interpolate(p(0.14, 0.34), [0, 1], [0, DOWN_MINI.length]));
  return (
    <Stage>
      <Bg theme={T} accent={C} />
      <Head theme={T} kicker="WHY CHARTS? THE CASE FOR PRICE" title="The Market Knew Before the Headlines Did" color={C} />
      {/* Left: analyst opinion panel */}
      <div style={{ position: "absolute", left: 130, top: 220, width: 740, height: 600, borderRadius: 20,
        background: mix(T.bg1, Y, 0.04), border: `2.5px solid ${mix(T.line, Y, 0.5)}`, overflow: "hidden",
        opacity: p(0.04, 0.13) }}>
        <div style={{ fontFamily: MONO, fontWeight: 800, fontSize: 22, color: Y, letterSpacing: 2,
          padding: "18px 24px 10px" }}>💬 WHAT THE PUNDITS SAID</div>
        {/* scrolling headlines */}
        {headlines.map((h, i) => (
          <div key={i} style={{ position: "absolute", left: 740 - ((tick + i * 480) % (headlines.length * 480)) + 80,
            top: 70 + (i % 2) * 70, whiteSpace: "nowrap", fontFamily: SANS, fontWeight: 600, fontSize: 24,
            color: T.text, background: mix(T.panel, Y, 0.12), border: `1.5px solid ${mix(T.line, Y, 0.5)}`,
            borderRadius: 999, padding: "10px 22px", opacity: p(0.08, 0.18) }}>{h}</div>
        ))}
        {/* mini down chart — "actual price" */}
        <div style={{ position: "absolute", left: 20, top: 220, width: 700, height: 340,
          background: mix(T.bg0, R, 0.03), borderRadius: 12, border: `1.5px solid ${mix(T.line, R, 0.4)}`,
          opacity: p(0.22, 0.34) }}>
          <div style={{ fontFamily: MONO, fontSize: 20, color: R, padding: "10px 16px" }}>ACTUAL PRICE — SAME PERIOD</div>
          {DOWN_MINI.slice(0, nDMini).map((k, i) => {
            const up = k.c >= k.o; const col = up ? G : R;
            const bt = dY(Math.max(k.o, k.c));
            return (
              <React.Fragment key={i}>
                <div style={{ position: "absolute", left: dX(i) - 1.5, top: dY(k.h) + 40, width: 3,
                  height: Math.max(2, dY(k.l) - dY(k.h)), background: col, opacity: 0.8 }} />
                <div style={{ position: "absolute", left: dX(i) - 12, top: bt + 40, width: 24,
                  height: Math.max(2, dY(Math.min(k.o, k.c)) - bt), borderRadius: 2, background: col }} />
              </React.Fragment>
            );
          })}
        </div>
      </div>
      {/* Right: explanation */}
      <div style={{ position: "absolute", left: 1010, top: 220, width: 780, height: 600, borderRadius: 20,
        background: mix(T.bg1, C, 0.04), border: `2.5px solid ${mix(T.line, C, 0.5)}`,
        padding: "32px 36px", boxSizing: "border-box", opacity: p(0.36, 0.46) }}>
        <div style={{ fontFamily: MONO, fontWeight: 800, fontSize: 22, color: C, letterSpacing: 2, marginBottom: 28 }}>WHAT PRICE WAS SAYING</div>
        {[
          { emoji: "📉", line: "Price already below all key MAs", at: 0.40 },
          { emoji: "📊", line: "Volume expanding on red days", at: 0.50 },
          { emoji: "⚠", line: "RSI divergence: lower highs on indicator", at: 0.60 },
          { emoji: "🔻", line: "Support zone broken — no recovery", at: 0.70 },
        ].map((it, i) => (
          <div key={i} style={{ display: "flex", gap: 18, alignItems: "flex-start", marginBottom: 28,
            opacity: p(it.at, it.at + 0.07), transform: `translateX(${(1 - p(it.at, it.at + 0.07)) * 20}px)` }}>
            <span style={{ fontSize: 30 }}>{it.emoji}</span>
            <span style={{ fontFamily: SANS, fontWeight: 600, fontSize: 27, color: T.text, lineHeight: 1.35, width: 620 }}>{it.line}</span>
          </div>
        ))}
        <div style={{ fontFamily: MONO, fontWeight: 800, fontSize: 24, color: C, marginTop: 14,
          opacity: 0.55 + Math.sin(frame * 0.08) * 0.4 }}>
          Price already knew. The chart is the fastest signal.
        </div>
      </div>
      <Wire x1={870} y1={520} x2={1010} y2={520} p={p(0.52, 0.62)} color={C} w={3} />
      <Flow x1={870} y1={520} x2={1010} y2={520} color={C} n={6} o={p(0.64, 0.70)} />
      <Foot theme={T} p={p(0.85, 0.94)}>Technicals + Fundamentals together = better decisions. Never use charts in isolation.</Foot>
    </Stage>
  );
};

// ════════════════════════════════════════════ 4. TIMEFRAMES
const TimeframesScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur); const frame = useCurrentFrame();
  const panels = [
    { label: "1 HOUR", sub: "40 candles · lots of noise", data: TF_1H,   color: Y, x: 130, nAt: [0.05, 0.35] },
    { label: "DAILY",  sub: "25 candles · trend clearer",  data: TF_DAY,  color: C, x: 680, nAt: [0.28, 0.60] },
    { label: "WEEKLY", sub: "12 candles · big picture",    data: TF_WEEK, color: G, x: 1230,nAt: [0.54, 0.82] },
  ];
  const hot = Math.floor(frame / 50) % 3;
  return (
    <Stage>
      <Bg theme={T} accent={C} />
      <Head theme={T} kicker="TIMEFRAMES — CHOOSING YOUR LENS" title="Zoom Out to Find the Real Story" color={C} />
      {panels.map((pn, pi) => {
        const panelO = p(pn.nAt[0] - 0.02, pn.nAt[0] + 0.07);
        const nC = Math.round(interpolate(p(pn.nAt[0], pn.nAt[1]), [0, 1], [0, pn.data.length]));
        const isHot = hot === pi && p(0.60, 0.61) > 0.5;
        return (
          <div key={pi} style={{ position: "absolute", left: pn.x, top: 225, width: 510, height: 620,
            borderRadius: 18, background: mix(T.bg1, pn.color, 0.04),
            border: `2.5px solid ${mix(T.line, pn.color, isHot ? 0.9 : 0.45)}`,
            boxShadow: isHot ? `0 0 30px ${mix(T.bg0, pn.color, 0.5)}` : "none",
            opacity: panelO, transform: `translateY(${(1 - panelO) * 20}px)` }}>
            <div style={{ fontFamily: MONO, fontWeight: 800, fontSize: 22, color: pn.color,
              letterSpacing: 3, padding: "18px 22px 4px" }}>{pn.label}</div>
            <div style={{ fontFamily: SANS, fontSize: 20, color: T.muted, paddingLeft: 22, marginBottom: 8 }}>{pn.sub}</div>
            {/* candles inside panel — relative to panel top-left */}
            <CandleChart data={pn.data} nC={nC} bx={20} by={80} bw={470} bh={480} />
          </div>
        );
      })}
      <Foot theme={T} p={p(0.85, 0.94)}>Weekly for bias · Daily for setup · Intraday for entry. Always trade in the direction of the larger frame.</Foot>
    </Stage>
  );
};

// ════════════════════════════════════════════ 5. CANDLE ANATOMY
// Single large candle with labeled parts
const ANAT_CANDLE: OHLC = { o: 96, c: 119, h: 127, l: 87 };
const ANAT_PMIN = 82, ANAT_PMAX = 132;
const anatPY = (v: number) => 215 + ((ANAT_PMAX - v) / (ANAT_PMAX - ANAT_PMIN)) * 600;
// Key pixel positions
const A_HI  = anatPY(ANAT_CANDLE.h); // ~125
const A_CL  = anatPY(ANAT_CANDLE.c); // ~245
const A_MID = (A_CL + anatPY(ANAT_CANDLE.o)) / 2; // mid-body
const A_OP  = anatPY(ANAT_CANDLE.o); // ~533
const A_LO  = anatPY(ANAT_CANDLE.l); // ~740
const ANAT_CX = 560; // candle center x

const CandleAnatomyScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur); const frame = useCurrentFrame();
  const candleO = p(0.04, 0.14);
  const labels: { text: string; y: number; color: string; at: number; desc: string }[] = [
    { text: "HIGH", y: A_HI,  color: C, at: 0.15, desc: "Highest price reached this period" },
    { text: "UPPER WICK", y: (A_HI + A_CL) / 2, color: T.muted, at: 0.22, desc: "Sellers pushed it up but couldn't hold" },
    { text: "CLOSE",      y: A_CL, color: G, at: 0.30, desc: "Where price settled at period end" },
    { text: "BODY",       y: A_MID,color: G, at: 0.40, desc: "Range between Open and Close" },
    { text: "OPEN",       y: A_OP, color: Y, at: 0.52, desc: "Where price started this period" },
    { text: "LOWER WICK", y: (A_OP + A_LO) / 2, color: T.muted, at: 0.62, desc: "Bears pushed it down but buyers stepped in" },
    { text: "LOW",        y: A_LO, color: R, at: 0.72, desc: "Lowest price reached this period" },
  ];
  return (
    <Stage>
      <Bg theme={T} accent={G} />
      <Head theme={T} kicker="CANDLESTICK ANATOMY — THE BASICS" title="Every Candle Is a Complete Battle Report" color={G} />
      {/* big candle */}
      {candleO > 0.05 && (
        <>
          {/* upper wick */}
          <div style={{ position: "absolute", left: ANAT_CX - 2, top: A_HI, width: 4,
            height: A_CL - A_HI, background: G, opacity: candleO * 0.85 }} />
          {/* body */}
          <div style={{ position: "absolute", left: ANAT_CX - 52, top: A_CL, width: 104,
            height: A_OP - A_CL, borderRadius: 6,
            background: `linear-gradient(180deg, ${mix(G, T.bg0, 0.1)}, ${mix(G, T.bg1, 0.3)})`,
            border: `2px solid ${G}`, opacity: candleO,
            boxShadow: `0 0 ${22 + Math.sin(frame * 0.06) * 8}px ${mix(T.bg0, G, 0.5)}` }} />
          {/* lower wick */}
          <div style={{ position: "absolute", left: ANAT_CX - 2, top: A_OP, width: 4,
            height: A_LO - A_OP, background: G, opacity: candleO * 0.85 }} />
        </>
      )}
      {/* dashed tick lines + labels */}
      {labels.map((lb, i) => {
        const lo = p(lb.at, lb.at + 0.06);
        return (
          <React.Fragment key={i}>
            {/* horizontal tick line to label area */}
            <div style={{ position: "absolute", left: ANAT_CX + 58, top: lb.y, width: 170,
              borderTop: `1.5px dashed ${mix(T.line, lb.color, 0.6)}`, opacity: lo }} />
            {/* label name */}
            <div style={{ position: "absolute", left: 740, top: lb.y - 14, width: 200,
              fontFamily: MONO, fontWeight: 800, fontSize: 22, color: lb.color, opacity: lo }}>{lb.text}</div>
            {/* description */}
            <div style={{ position: "absolute", left: 950, top: lb.y - 14, width: 760,
              fontFamily: SANS, fontSize: 23, color: T.muted, opacity: lo, lineHeight: 1.3 }}>{lb.desc}</div>
          </React.Fragment>
        );
      })}
      {/* "GREEN = bullish" tag */}
      <div style={{ position: "absolute", left: 370, top: A_HI - 50, fontFamily: MONO, fontWeight: 800,
        fontSize: 21, color: G, opacity: p(0.82, 0.90),
        background: mix(T.panel, G, 0.12), border: `1.5px solid ${G}`, borderRadius: 8, padding: "4px 14px" }}>
        GREEN = Close &gt; Open = Bullish candle
      </div>
      <Foot theme={T} p={p(0.86, 0.94)}>A red candle = Open above Close. Same four points — O, H, L, C — different story.</Foot>
    </Stage>
  );
};

// ════════════════════════════════════════════ 6. DOJI TYPES
const DojiScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur); const frame = useCurrentFrame();
  const COL_CX = [270, 610, 950, 1290]; // candle centers
  const dY = (v: number) => 265 + ((DOJI_PMAX - v) / (DOJI_PMAX - DOJI_PMIN)) * 380;
  const hot = Math.floor(frame / 38) % 4;
  return (
    <Stage>
      <Bg theme={T} accent={V} />
      <Head theme={T} kicker="SINGLE CANDLE — DOJI FAMILY" title="Four Shapes, One Message: The Market Is Deciding" color={V} />
      {DOJI_SPECS.map((d, i) => {
        const at = 0.08 + i * 0.14;
        const lo = p(at, at + 0.08);
        const isHot = hot === i && p(0.65, 0.66) > 0.5;
        const bodyTop = dY(Math.max(d.o, d.c));
        const bodyH = Math.max(3, dY(Math.min(d.o, d.c)) - bodyTop);
        return (
          <React.Fragment key={i}>
            {/* column bg */}
            <div style={{ position: "absolute", left: COL_CX[i] - 150, top: 240, width: 300, height: 600,
              borderRadius: 16, background: mix(T.panel, V, isHot ? 0.15 : 0.06),
              border: `2px solid ${mix(T.line, V, isHot ? 0.9 : 0.4)}`,
              opacity: lo, transform: `translateY(${(1 - lo) * 18}px)` }} />
            {/* wick */}
            <div style={{ position: "absolute", left: COL_CX[i] - 1.5, top: dY(d.h), width: 3,
              height: Math.max(2, dY(d.l) - dY(d.h)), background: C, opacity: lo * 0.85 }} />
            {/* tiny body */}
            <div style={{ position: "absolute", left: COL_CX[i] - 18, top: bodyTop, width: 36,
              height: bodyH, borderRadius: 2, background: C, opacity: lo,
              boxShadow: isHot ? `0 0 18px ${C}` : "none" }} />
            {/* name */}
            <div style={{ position: "absolute", left: COL_CX[i] - 140, top: 716, width: 280,
              textAlign: "center", fontFamily: MONO, fontWeight: 800, fontSize: 22,
              color: isHot ? V : T.text, opacity: lo }}>{d.name}</div>
            {/* sub */}
            <div style={{ position: "absolute", left: COL_CX[i] - 140, top: 752, width: 280,
              textAlign: "center", fontFamily: SANS, fontSize: 21, color: T.muted, opacity: lo * 0.8 }}>{d.sub}</div>
          </React.Fragment>
        );
      })}
      <Foot theme={T} p={p(0.86, 0.94)}>Doji = indecision. Always look LEFT — a doji after a long trend carries more weight.</Foot>
    </Stage>
  );
};

// ════════════════════════════════════════════ 7. HAMMER & HANGING MAN
// Context candles + pattern candle
const CTX_DOWN: OHLC[] = fromClose([130, 123, 116, 110, 105], 40, 0.1);
const CTX_UP:   OHLC[] = fromClose([90,  97,  104, 111, 116], 41, 0.1);
const HAMMER:   OHLC = { o: 106, c: 111, h: 112, l: 89 };
const HANG_MAN: OHLC = { o: 114, c: 118, h: 119, l: 100 };

const HammerScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur); const frame = useCurrentFrame();
  // Left side: downtrend + Hammer
  const LX = 170, LY_TOP = 260, LY_BOT = 740, LW = 580;
  const allL = [...CTX_DOWN, HAMMER];
  const lpmin = Math.min(...allL.map((k) => k.l));
  const lpmax = Math.max(...allL.map((k) => k.h));
  const lpY = (v: number) => LY_TOP + ((lpmax - v) / (lpmax - lpmin)) * (LY_BOT - LY_TOP);
  const lpX = (i: number) => LX + (i + 0.5) * (LW / allL.length);
  // Right side: uptrend + Hanging Man
  const RX = 1150, RY_TOP = 260, RY_BOT = 740, RW = 580;
  const allR = [...CTX_UP, HANG_MAN];
  const rpmin = Math.min(...allR.map((k) => k.l));
  const rpmax = Math.max(...allR.map((k) => k.h));
  const rpY = (v: number) => RY_TOP + ((rpmax - v) / (rpmax - rpmin)) * (RY_BOT - RY_TOP);
  const rpX = (i: number) => RX + (i + 0.5) * (RW / allR.length);
  const nLeft  = Math.round(interpolate(p(0.06, 0.36), [0, 1], [0, allL.length]));
  const nRight = Math.round(interpolate(p(0.44, 0.72), [0, 1], [0, allR.length]));
  return (
    <Stage>
      <Bg theme={T} accent={Y} />
      <Head theme={T} kicker="SINGLE CANDLE — HAMMER & HANGING MAN" title="Same Body, Opposite Meaning — Context Decides" color={Y} />
      {/* Left panel */}
      <div style={{ position: "absolute", left: 130, top: 220, width: 700, height: 620, borderRadius: 18,
        background: mix(T.bg1, G, 0.04), border: `2.5px solid ${mix(T.line, G, 0.5)}`,
        opacity: p(0.04, 0.12) }}>
        <div style={{ fontFamily: MONO, fontWeight: 800, fontSize: 22, color: G, letterSpacing: 2,
          padding: "16px 22px 4px" }}>🔨 HAMMER — in a downtrend</div>
        <div style={{ fontFamily: SANS, fontSize: 22, color: T.muted, paddingLeft: 22, marginBottom: 4 }}>Long lower wick · small body at top</div>
      </div>
      {allL.slice(0, nLeft).map((k, i) => {
        const isHammer = i === allL.length - 1;
        const col = isHammer ? Y : (k.c >= k.o ? G : R);
        const bw = isHammer ? 42 : 28;
        const bt = lpY(Math.max(k.o, k.c));
        return (
          <React.Fragment key={i}>
            <div style={{ position: "absolute", left: lpX(i) - 1.5, top: lpY(k.h), width: 3,
              height: Math.max(2, lpY(k.l) - lpY(k.h)), background: col, opacity: 0.85 }} />
            <div style={{ position: "absolute", left: lpX(i) - bw / 2, top: bt, width: bw,
              height: Math.max(2, lpY(Math.min(k.o, k.c)) - bt), borderRadius: 3, background: col,
              boxShadow: isHammer ? `0 0 22px ${Y}` : "none" }} />
          </React.Fragment>
        );
      })}
      {nLeft >= allL.length && (
        <div style={{ position: "absolute", left: 240, top: 748, fontFamily: MONO, fontWeight: 800,
          fontSize: 22, color: G, opacity: p(0.38, 0.48) }}>
          ↑ Potential bullish reversal — confirm with next candle
        </div>
      )}
      {/* Right panel */}
      <div style={{ position: "absolute", left: 1090, top: 220, width: 700, height: 620, borderRadius: 18,
        background: mix(T.bg1, R, 0.04), border: `2.5px solid ${mix(T.line, R, 0.5)}`,
        opacity: p(0.40, 0.50) }}>
        <div style={{ fontFamily: MONO, fontWeight: 800, fontSize: 22, color: R, letterSpacing: 2,
          padding: "16px 22px 4px" }}>HANGING MAN — in an uptrend</div>
        <div style={{ fontFamily: SANS, fontSize: 22, color: T.muted, paddingLeft: 22, marginBottom: 4 }}>Same shape — BEARISH potential</div>
      </div>
      {allR.slice(0, nRight).map((k, i) => {
        const isHang = i === allR.length - 1;
        const col = isHang ? Y : (k.c >= k.o ? G : R);
        const bw = isHang ? 42 : 28;
        const bt = rpY(Math.max(k.o, k.c));
        return (
          <React.Fragment key={i}>
            <div style={{ position: "absolute", left: rpX(i) - 1.5, top: rpY(k.h), width: 3,
              height: Math.max(2, rpY(k.l) - rpY(k.h)), background: col, opacity: 0.85 }} />
            <div style={{ position: "absolute", left: rpX(i) - bw / 2, top: bt, width: bw,
              height: Math.max(2, rpY(Math.min(k.o, k.c)) - bt), borderRadius: 3, background: col,
              boxShadow: isHang ? `0 0 22px ${Y}` : "none" }} />
          </React.Fragment>
        );
      })}
      {nRight >= allR.length && (
        <div style={{ position: "absolute", left: 1160, top: 748, fontFamily: MONO, fontWeight: 800,
          fontSize: 22, color: R, opacity: p(0.74, 0.84) }}>
          ↓ Potential bearish reversal — wait for confirmation
        </div>
      )}
      <Foot theme={T} p={p(0.86, 0.94)}>A pattern without context is noise. Trend first, candle second.</Foot>
    </Stage>
  );
};

// ════════════════════════════════════════════ 8. MARUBOZU
const MarubozuScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur); const frame = useCurrentFrame();
  const MY = 265, MB = 765, MCX_L = 480, MCX_R = 1440, MBW = 110;
  const mPmin = 90, mPmax = 135;
  const mPY = (v: number) => MY + ((mPmax - v) / (mPmax - mPmin)) * (MB - MY);
  // Bullish: o=95, c=130, h=130, l=95 (no wicks)
  const bBullTop = mPY(130), bBullBot = mPY(95);
  // Bearish: o=130, c=95, h=130, l=95
  const bBearTop = mPY(130), bBearBot = mPY(95);
  const bullO = p(0.04, 0.16), bearO = p(0.44, 0.56);
  return (
    <Stage>
      <Bg theme={T} accent={G} />
      <Head theme={T} kicker="SINGLE CANDLE — MARUBOZU" title="No Wicks = Total Conviction, No Hesitation" color={G} />
      {/* Bullish Marubozu */}
      <div style={{ position: "absolute", left: 130, top: 235, width: 700, height: 590, borderRadius: 18,
        background: mix(T.bg1, G, 0.05), border: `2.5px solid ${mix(T.line, G, 0.6)}`, opacity: bullO }}>
        <div style={{ fontFamily: MONO, fontWeight: 800, fontSize: 24, color: G, letterSpacing: 2, padding: "18px 24px" }}>
          BULLISH MARUBOZU
        </div>
      </div>
      {bullO > 0.05 && (
        <div style={{ position: "absolute", left: MCX_L - MBW / 2, top: bBullTop, width: MBW,
          height: bBullBot - bBullTop, borderRadius: 8,
          background: `linear-gradient(180deg, ${G}, ${mix(G, T.bg0, 0.35)})`,
          border: `2px solid ${G}`, opacity: bullO,
          boxShadow: `0 0 ${30 + Math.sin(frame * 0.06) * 10}px ${mix(T.bg0, G, 0.55)}` }} />
      )}
      {[{ text: "Open = Low", y: mPY(95) + 10, c: G }, { text: "Close = High", y: mPY(130) - 30, c: G }].map((lb, i) => (
        <div key={i} style={{ position: "absolute", left: 280, top: lb.y, fontFamily: MONO, fontWeight: 800,
          fontSize: 22, color: lb.c, opacity: p(0.20 + i * 0.08, 0.30 + i * 0.08) }}>{lb.text}</div>
      ))}
      <div style={{ position: "absolute", left: 150, top: 786, width: 650, fontFamily: SANS, fontSize: 25,
        color: T.muted, opacity: p(0.34, 0.46), lineHeight: 1.4 }}>
        Bulls controlled the ENTIRE session. From first tick to last, no seller could push it back.
      </div>
      {/* Bearish Marubozu */}
      <div style={{ position: "absolute", left: 1090, top: 235, width: 700, height: 590, borderRadius: 18,
        background: mix(T.bg1, R, 0.05), border: `2.5px solid ${mix(T.line, R, 0.6)}`, opacity: bearO }}>
        <div style={{ fontFamily: MONO, fontWeight: 800, fontSize: 24, color: R, letterSpacing: 2, padding: "18px 24px" }}>
          BEARISH MARUBOZU
        </div>
      </div>
      {bearO > 0.05 && (
        <div style={{ position: "absolute", left: MCX_R - MBW / 2, top: bBearTop, width: MBW,
          height: bBearBot - bBearTop, borderRadius: 8,
          background: `linear-gradient(180deg, ${mix(R, T.bg0, 0.1)}, ${R})`,
          border: `2px solid ${R}`, opacity: bearO,
          boxShadow: `0 0 ${30 + Math.sin(frame * 0.06) * 10}px ${mix(T.bg0, R, 0.55)}` }} />
      )}
      {[{ text: "Open = High", y: mPY(130) - 30, c: R }, { text: "Close = Low", y: mPY(95) + 10, c: R }].map((lb, i) => (
        <div key={i} style={{ position: "absolute", left: 1570, top: lb.y, fontFamily: MONO, fontWeight: 800,
          fontSize: 22, color: lb.c, opacity: p(0.58 + i * 0.08, 0.68 + i * 0.08) }}>{lb.text}</div>
      ))}
      <div style={{ position: "absolute", left: 1110, top: 786, width: 650, fontFamily: SANS, fontSize: 25,
        color: T.muted, opacity: p(0.72, 0.84), lineHeight: 1.4 }}>
        Bears owned this session. No counter-rally. Strong conviction — treat it with respect.
      </div>
      <Foot theme={T} p={p(0.87, 0.95)}>A Marubozu at a breakout point or after a long trend is one of the cleanest signals.</Foot>
    </Stage>
  );
};

// ════════════════════════════════════════════ 9. ENGULFING
const EngulfingScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur); const frame = useCurrentFrame();
  const EY_TOP = 260, EY_BOT = 760, EBW = 80;
  const ePmin = 88, ePmax = 122;
  const ePY = (v: number) => EY_TOP + ((ePmax - v) / (ePmax - ePmin)) * (EY_BOT - EY_TOP);
  // Bullish engulfing (left): small red C1, big green C2
  const BE_C1: OHLC = { o: 110, c: 104, h: 112, l: 102 };
  const BE_C2: OHLC = { o: 100, c: 118, h: 120, l: 98 };
  const LC1X = 440, LC2X = 600;
  // Bearish engulfing (right): small green C1, big red C2
  const BE2_C1: OHLC = { o: 100, c: 106, h: 108, l: 98 };
  const BE2_C2: OHLC = { o: 110, c: 92, h: 112, l: 90 };
  const RC1X = 1300, RC2X = 1460;
  const growL = p(0.36, 0.52), growR = p(0.68, 0.84);
  const drawCandle = (k: OHLC, cx: number, col: string, bw: number, grow = 1) => {
    const bt = ePY(Math.max(k.o, k.c));
    const fullH = Math.max(3, ePY(Math.min(k.o, k.c)) - bt);
    return (
      <>
        <div style={{ position: "absolute", left: cx - 1.5, top: ePY(k.h), width: 3,
          height: Math.max(2, ePY(k.l) - ePY(k.h)), background: col, opacity: 0.85 }} />
        <div style={{ position: "absolute", left: cx - bw / 2, top: bt, width: bw,
          height: fullH * grow, borderRadius: 3, background: col,
          boxShadow: `0 0 ${14 + Math.sin(frame * 0.08) * 5}px ${col}` }} />
      </>
    );
  };
  return (
    <Stage>
      <Bg theme={T} accent={G} />
      <Head theme={T} kicker="TWO-CANDLE PATTERN — ENGULFING" title="The Second Candle Swallows the First" color={G} />
      {/* Left: Bullish Engulfing */}
      <div style={{ position: "absolute", left: 130, top: 230, width: 730, height: 560, borderRadius: 18,
        background: mix(T.bg1, G, 0.04), border: `2.5px solid ${mix(T.line, G, 0.5)}`,
        opacity: p(0.04, 0.12) }}>
        <div style={{ fontFamily: MONO, fontWeight: 800, fontSize: 23, color: G, letterSpacing: 2,
          padding: "16px 22px" }}>BULLISH ENGULFING — reversal ↑</div>
      </div>
      {p(0.06, 0.07) > 0 && drawCandle(BE_C1, LC1X, R, EBW)}
      {growL > 0 && drawCandle(BE_C2, LC2X, G, EBW, Math.min(1, growL))}
      <div style={{ position: "absolute", left: 175, top: 752, width: 680, fontFamily: SANS, fontSize: 24,
        color: T.muted, opacity: p(0.56, 0.68) }}>
        Green body fully engulfs the red body — bulls overwhelmed sellers
      </div>
      {/* Right: Bearish Engulfing */}
      <div style={{ position: "absolute", left: 1060, top: 230, width: 730, height: 560, borderRadius: 18,
        background: mix(T.bg1, R, 0.04), border: `2.5px solid ${mix(T.line, R, 0.5)}`,
        opacity: p(0.52, 0.62) }}>
        <div style={{ fontFamily: MONO, fontWeight: 800, fontSize: 23, color: R, letterSpacing: 2,
          padding: "16px 22px" }}>BEARISH ENGULFING — reversal ↓</div>
      </div>
      {p(0.54, 0.55) > 0 && drawCandle(BE2_C1, RC1X, G, EBW)}
      {growR > 0 && drawCandle(BE2_C2, RC2X, R, EBW, Math.min(1, growR))}
      <div style={{ position: "absolute", left: 1090, top: 752, width: 680, fontFamily: SANS, fontSize: 24,
        color: T.muted, opacity: p(0.86, 0.94) }}>
        Red body fully engulfs the green body — sellers overwhelmed buyers
      </div>
      <Foot theme={T} p={p(0.87, 0.95)}>Engulfing is stronger when it appears after an extended trend, with above-average volume.</Foot>
    </Stage>
  );
};

// ════════════════════════════════════════════ 10. HARAMI
const HaramiScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur); const frame = useCurrentFrame();
  const HY_TOP = 265, HY_BOT = 775;
  const hPmin = 88, hPmax = 128;
  const hPY = (v: number) => HY_TOP + ((hPmax - v) / (hPmax - hPmin)) * (HY_BOT - HY_TOP);
  const BULL_H_C1: OHLC = { o: 118, c: 97, h: 121, l: 94 };  // large bearish mother
  const BULL_H_C2: OHLC = { o: 102, c: 109, h: 112, l: 100 }; // small bullish baby (inside)
  const BEAR_H_C1: OHLC = { o: 96, c: 117, h: 120, l: 93 };   // large bullish mother
  const BEAR_H_C2: OHLC = { o: 112, c: 105, h: 114, l: 103 }; // small bearish baby (inside)
  const drawH = (k: OHLC, cx: number, bw: number, col: string, lo: number) => {
    const bt = hPY(Math.max(k.o, k.c));
    return (
      <>
        <div style={{ position: "absolute", left: cx - 1.5, top: hPY(k.h), width: 3,
          height: Math.max(2, hPY(k.l) - hPY(k.h)), background: col, opacity: lo * 0.85 }} />
        <div style={{ position: "absolute", left: cx - bw / 2, top: bt, width: bw,
          height: Math.max(2, hPY(Math.min(k.o, k.c)) - bt), borderRadius: 3, background: col, opacity: lo,
          boxShadow: `0 0 12px ${col}` }} />
      </>
    );
  };
  return (
    <Stage>
      <Bg theme={T} accent={V} />
      <Head theme={T} kicker="TWO-CANDLE — HARAMI (INSIDE BAR)" title="A Small Baby Inside a Big Mother" color={V} />
      {/* Bullish Harami */}
      <div style={{ position: "absolute", left: 130, top: 235, width: 720, height: 580, borderRadius: 18,
        background: mix(T.bg1, G, 0.04), border: `2.5px solid ${mix(T.line, G, 0.5)}`, opacity: p(0.04, 0.12) }}>
        <div style={{ fontFamily: MONO, fontWeight: 800, fontSize: 22, color: G, letterSpacing: 2, padding: "16px 22px" }}>BULLISH HARAMI</div>
        <div style={{ fontFamily: SANS, fontSize: 22, color: T.muted, paddingLeft: 22 }}>after downtrend → indecision</div>
      </div>
      {drawH(BULL_H_C1, 380, 90, R, p(0.06, 0.18))}
      {drawH(BULL_H_C2, 540, 42, G, p(0.24, 0.36))}
      {p(0.36, 0.37) > 0 && (
        <div style={{ position: "absolute", left: 210, top: 776, width: 680, fontFamily: SANS, fontSize: 24,
          color: T.muted, opacity: p(0.36, 0.48) }}>
          Selling pressure contained — bulls holding ground inside the red body
        </div>
      )}
      {/* Bearish Harami */}
      <div style={{ position: "absolute", left: 1070, top: 235, width: 720, height: 580, borderRadius: 18,
        background: mix(T.bg1, R, 0.04), border: `2.5px solid ${mix(T.line, R, 0.5)}`, opacity: p(0.50, 0.60) }}>
        <div style={{ fontFamily: MONO, fontWeight: 800, fontSize: 22, color: R, letterSpacing: 2, padding: "16px 22px" }}>BEARISH HARAMI</div>
        <div style={{ fontFamily: SANS, fontSize: 22, color: T.muted, paddingLeft: 22 }}>after uptrend → caution</div>
      </div>
      {drawH(BEAR_H_C1, 1300, 90, G, p(0.52, 0.64))}
      {drawH(BEAR_H_C2, 1460, 42, R, p(0.68, 0.80))}
      {p(0.80, 0.81) > 0 && (
        <div style={{ position: "absolute", left: 1100, top: 776, width: 680, fontFamily: SANS, fontSize: 24,
          color: T.muted, opacity: p(0.80, 0.90) }}>
          Buying momentum stalling — sellers fitting inside the green candle's range
        </div>
      )}
      <Foot theme={T} p={p(0.87, 0.95)}>Harami alone = caution, not action. Confirm with next-day price behavior.</Foot>
    </Stage>
  );
};

// ════════════════════════════════════════════ 11. MORNING STAR
const MorningStarScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur); const frame = useCurrentFrame();
  const MSY_TOP = 255, MSY_BOT = 775;
  const msPmin = 88, msPmax = 122;
  const msPY = (v: number) => MSY_TOP + ((msPmax - v) / (msPmax - msPmin)) * (MSY_BOT - MSY_TOP);
  const MS_C1: OHLC = { o: 117, c: 99, h: 120, l: 97 };   // bearish
  const MS_C2: OHLC = { o: 98,  c: 98.4, h: 103, l: 92 }; // doji / indecision
  const MS_C3: OHLC = { o: 99,  c: 117, h: 120, l: 97 };  // bullish
  const EVE_C1: OHLC = { o: 97, c: 115, h: 118, l: 95 };  // bullish
  const EVE_C2: OHLC = { o: 116, c: 116.4, h: 121, l: 111 }; // doji
  const EVE_C3: OHLC = { o: 115, c: 99, h: 117, l: 97 };  // bearish
  const candles3 = (arr: OHLC[], startX: number, colors: string[], phase: number[]) => arr.map((k, i) => {
    const lo = p(phase[i], phase[i] + 0.08);
    const col = colors[i]; const cx = startX + i * 200;
    const bt = msPY(Math.max(k.o, k.c));
    return (
      <React.Fragment key={i}>
        <div style={{ position: "absolute", left: cx - 1.5, top: msPY(k.h), width: 3,
          height: Math.max(2, msPY(k.l) - msPY(k.h)), background: col, opacity: lo * 0.85 }} />
        <div style={{ position: "absolute", left: cx - 46, top: bt, width: 92,
          height: Math.max(3, msPY(Math.min(k.o, k.c)) - bt), borderRadius: 4, background: col,
          opacity: lo, boxShadow: `0 0 ${14 + Math.sin(frame * 0.07 + i) * 5}px ${col}` }} />
      </React.Fragment>
    );
  });
  return (
    <Stage>
      <Bg theme={T} accent={G} />
      <Head theme={T} kicker="THREE-CANDLE — MORNING & EVENING STAR" title="Three Candles That Signal a Trend Change" color={G} />
      {/* Morning Star */}
      <div style={{ position: "absolute", left: 130, top: 230, width: 720, height: 560, borderRadius: 18,
        background: mix(T.bg1, G, 0.04), border: `2.5px solid ${mix(T.line, G, 0.5)}`, opacity: p(0.04, 0.12) }}>
        <div style={{ fontFamily: MONO, fontWeight: 800, fontSize: 22, color: G, letterSpacing: 2, padding: "16px 22px" }}>⭐ MORNING STAR — bullish reversal</div>
      </div>
      {candles3([MS_C1, MS_C2, MS_C3], 290, [R, Y, G], [0.10, 0.26, 0.42])}
      {[["Red: strong selling","0.14"],["Doji: sellers exhaust","0.30"],["Green: bulls take over","0.48"]].map(([lb, at], i) => (
        <div key={i} style={{ position: "absolute", left: 186 + i * 200, top: 774, width: 180,
          textAlign: "center", fontFamily: MONO, fontSize: 19, color: T.muted,
          opacity: p(parseFloat(at), parseFloat(at) + 0.1) }}>{lb}</div>
      ))}
      {/* Evening Star */}
      <div style={{ position: "absolute", left: 1070, top: 230, width: 720, height: 560, borderRadius: 18,
        background: mix(T.bg1, R, 0.04), border: `2.5px solid ${mix(T.line, R, 0.5)}`, opacity: p(0.52, 0.62) }}>
        <div style={{ fontFamily: MONO, fontWeight: 800, fontSize: 22, color: R, letterSpacing: 2, padding: "16px 22px" }}>🌙 EVENING STAR — bearish reversal</div>
      </div>
      {candles3([EVE_C1, EVE_C2, EVE_C3], 1230, [G, Y, R], [0.58, 0.68, 0.78])}
      {[["Green: strong rally","0.62"],["Doji: buyers pause","0.72"],["Red: bears arrive","0.82"]].map(([lb, at], i) => (
        <div key={i} style={{ position: "absolute", left: 1128 + i * 200, top: 774, width: 180,
          textAlign: "center", fontFamily: MONO, fontSize: 19, color: T.muted,
          opacity: p(parseFloat(at), parseFloat(at) + 0.08) }}>{lb}</div>
      ))}
      <Foot theme={T} p={p(0.87, 0.95)}>Star patterns need confirmation — a strong close on the third candle is the key signal.</Foot>
    </Stage>
  );
};

// ════════════════════════════════════════════ 12b. THREE WHITE SOLDIERS / BLACK CROWS
const ThreeWhiteScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur); const frame = useCurrentFrame();
  const TWY_TOP = 255, TWY_BOT = 775;
  const twPmin = 88, twPmax = 138;
  const twPY = (v: number) => TWY_TOP + ((twPmax - v) / (twPmax - twPmin)) * (TWY_BOT - TWY_TOP);
  // Three White Soldiers
  const SOLDIERS: OHLC[] = [
    { o: 95, c: 108, h: 110, l: 93 },
    { o: 105, c: 118, h: 120, l: 103 },
    { o: 115, c: 129, h: 131, l: 113 },
  ];
  // Three Black Crows
  const CROWS: OHLC[] = [
    { o: 130, c: 117, h: 132, l: 115 },
    { o: 120, c: 107, h: 122, l: 105 },
    { o: 110, c: 97, h: 112, l: 95 },
  ];
  const drawSet = (arr: OHLC[], startX: number, col: string, baseAt: number) => arr.map((k, i) => {
    const lo = p(baseAt + i * 0.12, baseAt + i * 0.12 + 0.09);
    const cx = startX + i * 190;
    const bt = twPY(Math.max(k.o, k.c));
    return (
      <React.Fragment key={i}>
        <div style={{ position: "absolute", left: cx - 1.5, top: twPY(k.h), width: 3,
          height: Math.max(2, twPY(k.l) - twPY(k.h)), background: col, opacity: lo * 0.85 }} />
        <div style={{ position: "absolute", left: cx - 52, top: bt, width: 104,
          height: Math.max(3, twPY(Math.min(k.o, k.c)) - bt), borderRadius: 4, background: col,
          opacity: lo, boxShadow: `0 0 ${16 + Math.sin(frame * 0.06 + i) * 6}px ${col}` }} />
      </React.Fragment>
    );
  });
  return (
    <Stage>
      <Bg theme={T} accent={G} />
      <Head theme={T} kicker="THREE-CANDLE PATTERN — SOLDIERS & CROWS" title="Three Consecutive Candles Signal Strong Momentum" color={G} />
      <div style={{ position: "absolute", left: 130, top: 230, width: 720, height: 560, borderRadius: 18,
        background: mix(T.bg1, G, 0.04), border: `2.5px solid ${mix(T.line, G, 0.5)}`, opacity: p(0.04, 0.12) }}>
        <div style={{ fontFamily: MONO, fontWeight: 800, fontSize: 22, color: G, letterSpacing: 2, padding: "16px 22px" }}>THREE WHITE SOLDIERS 🪖🪖🪖</div>
        <div style={{ fontFamily: SANS, fontSize: 22, color: T.muted, paddingLeft: 22 }}>Each opens inside previous body · closes near its high</div>
      </div>
      {drawSet(SOLDIERS, 250, G, 0.10)}
      <div style={{ position: "absolute", left: 140, top: 774, fontFamily: SANS, fontSize: 24, color: T.muted, opacity: p(0.44, 0.56) }}>
        Strong, persistent buying across three sessions. Bulls in control.
      </div>
      <div style={{ position: "absolute", left: 1070, top: 230, width: 720, height: 560, borderRadius: 18,
        background: mix(T.bg1, R, 0.04), border: `2.5px solid ${mix(T.line, R, 0.5)}`, opacity: p(0.52, 0.62) }}>
        <div style={{ fontFamily: MONO, fontWeight: 800, fontSize: 22, color: R, letterSpacing: 2, padding: "16px 22px" }}>THREE BLACK CROWS 🐦🐦🐦</div>
        <div style={{ fontFamily: SANS, fontSize: 22, color: T.muted, paddingLeft: 22 }}>Each opens inside previous body · closes near its low</div>
      </div>
      {drawSet(CROWS, 1200, R, 0.58)}
      <div style={{ position: "absolute", left: 1080, top: 774, fontFamily: SANS, fontSize: 24, color: T.muted, opacity: p(0.84, 0.94) }}>
        Persistent selling. Bears in full control for three sessions.
      </div>
      <Foot theme={T} p={p(0.87, 0.95)}>After a long run-up, Three Black Crows is one of the most reliable reversal signals.</Foot>
    </Stage>
  );
};

// ════════════════════════════════════════════ 13. SUPPORT & RESISTANCE
const SRScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur); const frame = useCurrentFrame();
  const BX = 60, BY = 60, BW = 1380, BH = 430; // inside Browser content
  const N = SR_SERIES.length;
  const pmin = Math.min(...SR_SERIES.map((k) => k.l)) - 4;
  const pmax = Math.max(...SR_SERIES.map((k) => k.h)) + 4;
  const pY = (v: number) => BY + ((pmax - v) / (pmax - pmin)) * BH;
  const cX = (i: number) => BX + (i + 0.5) * (BW / N);
  const cw = Math.max(5, (BW / N) * 0.62);
  const nC = Math.round(interpolate(p(0.04, 0.42), [0, 1], [0, N]));
  const srO1 = p(0.44, 0.52), srO2 = p(0.55, 0.63), srO3 = p(0.66, 0.74);
  const cross = 60 + ((frame * 2.0) % 1380);
  return (
    <Stage>
      <Bg theme={T} accent={C} />
      <Head theme={T} kicker="CHART PATTERN — SUPPORT & RESISTANCE" title="The Floor and the Ceiling Every Market Remembers" color={C} />
      <Browser url="price-chart · DEMO · NSE" color={C} o={p(0.02, 0.08)}>
        {/* candles */}
        {SR_SERIES.slice(0, nC).map((k, i) => {
          const up = k.c >= k.o; const col = up ? G : R;
          const bt = pY(Math.max(k.o, k.c));
          return (
            <React.Fragment key={i}>
              <div style={{ position: "absolute", left: cX(i) - 1.5, top: pY(k.h), width: 3,
                height: Math.max(2, pY(k.l) - pY(k.h)), background: col, opacity: 0.82 }} />
              <div style={{ position: "absolute", left: cX(i) - cw / 2, top: bt, width: cw,
                height: Math.max(2, pY(Math.min(k.o, k.c)) - bt), borderRadius: 2, background: col,
                boxShadow: i === nC - 1 ? `0 0 10px ${col}` : "none" }} />
            </React.Fragment>
          );
        })}
        {/* crosshair */}
        {cross < 1440 && <svg style={{ position: "absolute", left: 0, top: 0, overflow: "visible" }} width={1500} height={626}>
          <line x1={cross} y1={BY} x2={cross} y2={BY + BH} stroke={mix(T.muted, C, 0.35)} strokeWidth={1.5} strokeDasharray="5 7" opacity={0.5} />
        </svg>}
        {/* SR horizontal lines — labels right-anchored INSIDE chart at BX+BW-16 */}
        <svg style={{ position: "absolute", left: 0, top: 0, overflow: "visible" }} width={1500} height={626}>
          <line x1={BX} y1={pY(SR_SUP1)} x2={BX + BW} y2={pY(SR_SUP1)} stroke={G} strokeWidth={2.5} strokeDasharray="10 8" opacity={srO1} />
          <text x={BX + BW - 16} y={pY(SR_SUP1) - 8} textAnchor="end" fill={G} fontFamily={MONO} fontSize={20} opacity={srO1}>SUPPORT {SR_SUP1}</text>
          <line x1={BX} y1={pY(SR_SUP2)} x2={BX + BW} y2={pY(SR_SUP2)} stroke={G} strokeWidth={2.5} strokeDasharray="10 8" opacity={srO2} />
          <text x={BX + BW - 16} y={pY(SR_SUP2) - 8} textAnchor="end" fill={G} fontFamily={MONO} fontSize={20} opacity={srO2}>SUP/RES {SR_SUP2}</text>
          <line x1={BX} y1={pY(SR_RES)} x2={BX + BW} y2={pY(SR_RES)} stroke={R} strokeWidth={2.5} strokeDasharray="10 8" opacity={srO3} />
          <text x={BX + BW - 16} y={pY(SR_RES) - 8} textAnchor="end" fill={R} fontFamily={MONO} fontSize={20} opacity={srO3}>RESISTANCE {SR_RES}</text>
        </svg>
        {/* bounce / rejection labels */}
        {srO1 > 0 && (
          <div style={{ position: "absolute", left: cX(8) - 60, top: pY(SR_SUP1) - 44, width: 120,
            textAlign: "center", fontFamily: MONO, fontSize: 19, color: G, opacity: srO1 }}>↑ bounce</div>
        )}
        {srO3 > 0 && (
          <div style={{ position: "absolute", left: cX(33) - 70, top: pY(SR_RES) + 12, width: 140,
            textAlign: "center", fontFamily: MONO, fontSize: 19, color: R, opacity: srO3 }}>↓ rejection</div>
        )}
        {/* education strip */}
        <div style={{ position: "absolute", left: 60, top: 506, width: 1380, fontFamily: SANS, fontSize: 23,
          color: T.muted, opacity: p(0.74, 0.84) }}>
          Price has memory — the more times a level holds, the stronger it becomes as a future signal.
        </div>
      </Browser>
      <Foot theme={T} p={p(0.86, 0.94)}>Former resistance becomes support on a clean breakout. Watch for retests.</Foot>
    </Stage>
  );
};

// ════════════════════════════════════════════ 14. TRENDLINES
const TrendlineScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur); const frame = useCurrentFrame();
  const BX = 60, BY = 64, BW = 1380, BH = 420;
  const N = TREND_UP.length;
  const pmin = Math.min(...TREND_UP.map((k) => k.l)) - 3;
  const pmax = Math.max(...TREND_UP.map((k) => k.h)) + 3;
  const pY = (v: number) => BY + ((pmax - v) / (pmax - pmin)) * BH;
  const cX = (i: number) => BX + (i + 0.5) * (BW / N);
  const cw = Math.max(5, (BW / N) * 0.62);
  const nC = Math.round(interpolate(p(0.04, 0.40), [0, 1], [0, N]));
  const tlO = p(0.44, 0.58);   // uptrend support line
  const hhO = p(0.62, 0.74);   // higher-high annotations
  const cross = 60 + ((frame * 1.8) % 1380);
  // Trendline: connect low of candle 1 to low of candle 28 (estimated)
  const tl_i1 = 1, tl_i2 = 28;
  const tl_x1 = cX(tl_i1), tl_y1 = pY(TREND_UP[tl_i1].l);
  const tl_x2 = cX(tl_i2), tl_y2 = pY(TREND_UP[tl_i2].l);
  return (
    <Stage>
      <Bg theme={T} accent={C} />
      <Head theme={T} kicker="CHART PATTERN — TRENDLINES" title="Connect the Lows: That Line Is Your Edge" color={C} />
      <Browser url="price-chart · DEMO · UPTREND" color={C} o={p(0.02, 0.08)}>
        {TREND_UP.slice(0, nC).map((k, i) => {
          const up = k.c >= k.o; const col = up ? G : R;
          const bt = pY(Math.max(k.o, k.c));
          return (
            <React.Fragment key={i}>
              <div style={{ position: "absolute", left: cX(i) - 1.5, top: pY(k.h), width: 3,
                height: Math.max(2, pY(k.l) - pY(k.h)), background: col, opacity: 0.82 }} />
              <div style={{ position: "absolute", left: cX(i) - cw / 2, top: bt, width: cw,
                height: Math.max(2, pY(Math.min(k.o, k.c)) - bt), borderRadius: 2, background: col,
                boxShadow: i === nC - 1 ? `0 0 10px ${col}` : "none" }} />
            </React.Fragment>
          );
        })}
        <svg style={{ position: "absolute", left: 0, top: 0, overflow: "visible" }} width={1500} height={626}>
          {cross < 1440 && <line x1={cross} y1={BY} x2={cross} y2={BY + BH} stroke={mix(T.muted, C, 0.35)} strokeWidth={1.5} strokeDasharray="5 7" opacity={0.45} />}
          {/* uptrend support line */}
          {tlO > 0 && <line x1={tl_x1} y1={tl_y1} x2={tl_x1 + (tl_x2 - tl_x1) * tlO} y2={tl_y1 + (tl_y2 - tl_y1) * tlO}
            stroke={G} strokeWidth={3} strokeDasharray="none" opacity={tlO} />}
          {/* higher-high indicators */}
          {hhO > 0 && [4, 12, 22, 30].map((idx) => (
            <React.Fragment key={idx}>
              <circle cx={cX(idx)} cy={pY(TREND_UP[idx].h)} r={7} fill="none" stroke={Y} strokeWidth={2.5} opacity={hhO} />
              <text x={cX(idx) - 8} y={pY(TREND_UP[idx].h) - 16} fill={Y} fontFamily={MONO} fontSize={18} opacity={hhO}>HH</text>
            </React.Fragment>
          ))}
        </svg>
        <div style={{ position: "absolute", left: tl_x2 + 24, top: tl_y2 - 14,
          fontFamily: MONO, fontWeight: 800, fontSize: 21, color: G, opacity: tlO }}>
          UPTREND LINE — buy dips to this line
        </div>
        <div style={{ position: "absolute", left: 60, top: 510, width: 1380, fontFamily: SANS, fontSize: 23,
          color: T.muted, opacity: p(0.76, 0.86) }}>
          Higher Highs + Higher Lows = uptrend intact. A close BELOW the trendline is the first warning.
        </div>
      </Browser>
      <Foot theme={T} p={p(0.86, 0.94)}>Need at least 2 points to draw a trendline. Three touches makes it significant.</Foot>
    </Stage>
  );
};

// ════════════════════════════════════════════ 15. HEAD & SHOULDERS
const HeadShouldersScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur); const frame = useCurrentFrame();
  const BX = 60, BY = 64, BW = 1280, BH = 420;
  const N = HS_SERIES.length;
  const pmin = Math.min(...HS_SERIES.map((k) => k.l)) - 3;
  const pmax = Math.max(...HS_SERIES.map((k) => k.h)) + 4;
  const pY = (v: number) => BY + ((pmax - v) / (pmax - pmin)) * BH;
  const cX = (i: number) => BX + (i + 0.5) * (BW / N);
  const cw = Math.max(8, (BW / N) * 0.62);
  const nC = Math.round(interpolate(p(0.04, 0.44), [0, 1], [0, N]));
  const neckO = p(0.46, 0.58);
  const labelO = p(0.56, 0.70);
  const targetO = p(0.72, 0.84);
  const targetPY = pY(HS_NECK - (HS_HEAD_PEAK - HS_NECK));
  const neckPY = pY(HS_NECK);
  return (
    <Stage>
      <Bg theme={T} accent={V} />
      <Head theme={T} kicker="CHART PATTERN — HEAD & SHOULDERS" title="The Most Reliable Reversal Pattern in Charts" color={V} />
      <Browser url="price-chart · DEMO · H&S REVERSAL" color={V} o={p(0.02, 0.08)}>
        {HS_SERIES.slice(0, nC).map((k, i) => {
          const up = k.c >= k.o; const col = up ? G : R;
          const bt = pY(Math.max(k.o, k.c));
          return (
            <React.Fragment key={i}>
              <div style={{ position: "absolute", left: cX(i) - 1.5, top: pY(k.h), width: 3,
                height: Math.max(2, pY(k.l) - pY(k.h)), background: col, opacity: 0.82 }} />
              <div style={{ position: "absolute", left: cX(i) - cw / 2, top: bt, width: cw,
                height: Math.max(2, pY(Math.min(k.o, k.c)) - bt), borderRadius: 2, background: col,
                boxShadow: i === nC - 1 ? `0 0 10px ${col}` : "none" }} />
            </React.Fragment>
          );
        })}
        <svg style={{ position: "absolute", left: 0, top: 0, overflow: "visible" }} width={1500} height={626}>
          {/* neckline */}
          {neckO > 0 && <line x1={BX} y1={neckPY} x2={BX + BW} y2={neckPY} stroke={Y} strokeWidth={2.5} strokeDasharray="10 8" opacity={neckO} />}
          {/* target arrow */}
          {targetO > 0 && <>
            <line x1={cX(N - 2)} y1={neckPY} x2={cX(N - 2)} y2={targetPY} stroke={R} strokeWidth={2.5} strokeDasharray="8 8" opacity={targetO} />
            <polygon points={`${cX(N - 2) - 8},${targetPY + 12} ${cX(N - 2) + 8},${targetPY + 12} ${cX(N - 2)},${targetPY}`} fill={R} opacity={targetO} />
          </>}
        </svg>
        {/* Labels */}
        {labelO > 0 && <>
          <div style={{ position: "absolute", left: cX(2) - 55, top: pY(HS_SERIES[2].h) - 38, width: 110,
            textAlign: "center", fontFamily: MONO, fontWeight: 800, fontSize: 20, color: V, opacity: labelO }}>LEFT SHOULDER</div>
          <div style={{ position: "absolute", left: cX(7) - 40, top: pY(HS_SERIES[7].h) - 38, width: 80,
            textAlign: "center", fontFamily: MONO, fontWeight: 800, fontSize: 20, color: Y, opacity: labelO }}>HEAD</div>
          <div style={{ position: "absolute", left: cX(12) - 55, top: pY(HS_SERIES[12].h) - 38, width: 110,
            textAlign: "center", fontFamily: MONO, fontWeight: 800, fontSize: 20, color: V, opacity: labelO }}>RIGHT SHOULDER</div>
          <div style={{ position: "absolute", left: BX + BW + 14, top: neckPY - 12, fontFamily: MONO, fontWeight: 800,
            fontSize: 20, color: Y, opacity: neckO }}>NECKLINE {HS_NECK}</div>
        </>}
        {targetO > 0 && (
          <div style={{ position: "absolute", left: cX(N - 2) + 18, top: (neckPY + targetPY) / 2 - 14,
            fontFamily: MONO, fontWeight: 800, fontSize: 21, color: R, opacity: targetO }}>
            TARGET {HS_NECK - (HS_HEAD_PEAK - HS_NECK)}
          </div>
        )}
        <div style={{ position: "absolute", left: 60, top: 510, width: 1280, fontFamily: SANS, fontSize: 23,
          color: T.muted, opacity: p(0.84, 0.94) }}>
          Measured move: neckline − (head − neckline) = the minimum expected fall after breakdown.
        </div>
      </Browser>
      <Foot theme={T} p={p(0.86, 0.94)}>Volume should confirm: heavy on the left, lighter on right shoulder — confirms distribution.</Foot>
    </Stage>
  );
};

// ════════════════════════════════════════════ 16. DOUBLE TOP
const DoubleTopScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur); const frame = useCurrentFrame();
  const BX = 60, BY = 64, BW = 1380, BH = 430;
  const N = DT_SERIES.length;
  const pmin = Math.min(...DT_SERIES.map((k) => k.l)) - 3;
  const pmax = Math.max(...DT_SERIES.map((k) => k.h)) + 4;
  const pY = (v: number) => BY + ((pmax - v) / (pmax - pmin)) * BH;
  const cX = (i: number) => BX + (i + 0.5) * (BW / N);
  const cw = Math.max(8, (BW / N) * 0.62);
  const nC = Math.round(interpolate(p(0.04, 0.42), [0, 1], [0, N]));
  const neckY = pY(109); // double top neckline approx
  const neckO = p(0.46, 0.58), labO = p(0.56, 0.70), targO = p(0.70, 0.82);
  return (
    <Stage>
      <Bg theme={T} accent={R} />
      <Head theme={T} kicker="CHART PATTERN — DOUBLE TOP & BOTTOM" title="The 'M' and 'W' Patterns That Signal Reversals" color={R} />
      <Browser url="price-chart · DEMO · DOUBLE TOP" color={R} o={p(0.02, 0.08)}>
        {DT_SERIES.slice(0, nC).map((k, i) => {
          const up = k.c >= k.o; const col = up ? G : R;
          const bt = pY(Math.max(k.o, k.c));
          return (
            <React.Fragment key={i}>
              <div style={{ position: "absolute", left: cX(i) - 1.5, top: pY(k.h), width: 3,
                height: Math.max(2, pY(k.l) - pY(k.h)), background: col, opacity: 0.82 }} />
              <div style={{ position: "absolute", left: cX(i) - cw / 2, top: bt, width: cw,
                height: Math.max(2, pY(Math.min(k.o, k.c)) - bt), borderRadius: 2, background: col,
                boxShadow: i === nC - 1 ? `0 0 10px ${col}` : "none" }} />
            </React.Fragment>
          );
        })}
        <svg style={{ position: "absolute", left: 0, top: 0, overflow: "visible" }} width={1500} height={626}>
          {neckO > 0 && <line x1={BX} y1={neckY} x2={BX + BW} y2={neckY} stroke={Y} strokeWidth={2.5} strokeDasharray="10 8" opacity={neckO} />}
        </svg>
        {labO > 0 && <>
          <div style={{ position: "absolute", left: cX(3) - 55, top: pY(DT_SERIES[4].h) - 38, width: 110,
            textAlign: "center", fontFamily: MONO, fontWeight: 800, fontSize: 20, color: R, opacity: labO }}>TOP 1</div>
          <div style={{ position: "absolute", left: cX(10) - 55, top: pY(DT_SERIES[10].h) - 38, width: 110,
            textAlign: "center", fontFamily: MONO, fontWeight: 800, fontSize: 20, color: R, opacity: labO }}>TOP 2</div>
          <div style={{ position: "absolute", left: BX + BW + 14, top: neckY - 12,
            fontFamily: MONO, fontWeight: 800, fontSize: 20, color: Y, opacity: neckO }}>NECKLINE</div>
        </>}
        {targO > 0 && (
          <div style={{ position: "absolute", left: cX(13) + 14, top: pY(97) - 16,
            fontFamily: MONO, fontWeight: 800, fontSize: 21, color: R, opacity: targO }}>↓ Target = 2× height below neck</div>
        )}
        <div style={{ position: "absolute", left: 60, top: 510, width: 1380, fontFamily: SANS, fontSize: 23,
          color: T.muted, opacity: p(0.82, 0.92) }}>
          The "M" shape — two equal peaks, breakdown below the neckline confirms the reversal.
        </div>
      </Browser>
      <Foot theme={T} p={p(0.86, 0.94)}>Double Bottom = the "W" pattern → bullish. Same measured-move math, flipped.</Foot>
    </Stage>
  );
};

// ════════════════════════════════════════════ 17. FLAG
const FlagScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur); const frame = useCurrentFrame();
  const BX = 60, BY = 64, BW = 1380, BH = 430;
  const N = FLAG_SERIES.length;
  const pmin = Math.min(...FLAG_SERIES.map((k) => k.l)) - 3;
  const pmax = Math.max(...FLAG_SERIES.map((k) => k.h)) + 4;
  const pY = (v: number) => BY + ((pmax - v) / (pmax - pmin)) * BH;
  const cX = (i: number) => BX + (i + 0.5) * (BW / N);
  const cw = Math.max(8, (BW / N) * 0.62);
  const nC = Math.round(interpolate(p(0.04, 0.42), [0, 1], [0, N]));
  const annO = p(0.46, 0.60), boO = p(0.66, 0.80);
  // Flag channel lines (indices 7-12 = consolidation)
  const fc_top = pY(156), fc_bot = pY(139);
  const fc_x1 = cX(7), fc_x2 = cX(12);
  return (
    <Stage>
      <Bg theme={T} accent={G} />
      <Head theme={T} kicker="CHART PATTERN — FLAG & PENNANT" title="Pause After a Strong Move, Then Continue" color={G} />
      <Browser url="price-chart · DEMO · BULL FLAG" color={G} o={p(0.02, 0.08)}>
        {FLAG_SERIES.slice(0, nC).map((k, i) => {
          const up = k.c >= k.o; const col = up ? G : R;
          const bt = pY(Math.max(k.o, k.c));
          return (
            <React.Fragment key={i}>
              <div style={{ position: "absolute", left: cX(i) - 1.5, top: pY(k.h), width: 3,
                height: Math.max(2, pY(k.l) - pY(k.h)), background: col, opacity: 0.82 }} />
              <div style={{ position: "absolute", left: cX(i) - cw / 2, top: bt, width: cw,
                height: Math.max(2, pY(Math.min(k.o, k.c)) - bt), borderRadius: 2, background: col,
                boxShadow: i === nC - 1 ? `0 0 10px ${col}` : "none" }} />
            </React.Fragment>
          );
        })}
        <svg style={{ position: "absolute", left: 0, top: 0, overflow: "visible" }} width={1500} height={626}>
          {annO > 0 && <>
            <line x1={fc_x1} y1={fc_top} x2={fc_x2} y2={fc_top} stroke={Y} strokeWidth={2} strokeDasharray="8 6" opacity={annO} />
            <line x1={fc_x1} y1={fc_bot} x2={fc_x2} y2={fc_bot} stroke={Y} strokeWidth={2} strokeDasharray="8 6" opacity={annO} />
          </>}
        </svg>
        {annO > 0 && <>
          <div style={{ position: "absolute", left: cX(3) - 60, top: pY(140) - 38, width: 120,
            textAlign: "center", fontFamily: MONO, fontWeight: 800, fontSize: 20, color: G, opacity: annO }}>FLAGPOLE</div>
          <div style={{ position: "absolute", left: cX(9) - 45, top: fc_top - 36, width: 90,
            textAlign: "center", fontFamily: MONO, fontWeight: 800, fontSize: 20, color: Y, opacity: annO }}>FLAG</div>
        </>}
        {boO > 0 && (
          <div style={{ position: "absolute", left: cX(13) - 60, top: pY(175) - 36, width: 120,
            textAlign: "center", fontFamily: MONO, fontWeight: 800, fontSize: 20, color: G, opacity: boO }}>BREAKOUT ↑</div>
        )}
        <div style={{ position: "absolute", left: 60, top: 510, width: 1380, fontFamily: SANS, fontSize: 23,
          color: T.muted, opacity: p(0.82, 0.92) }}>
          Bull flag: strong pole (momentum) → shallow pullback in a channel → breakout = continuation trade.
        </div>
      </Browser>
      <Foot theme={T} p={p(0.86, 0.94)}>Volume should dry up during the flag and SURGE on the breakout — that's the signal.</Foot>
    </Stage>
  );
};

// ════════════════════════════════════════════ 18. TRIANGLE
const TriangleScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur); const frame = useCurrentFrame();
  const BX = 60, BY = 64, BW = 1380, BH = 430;
  const N = TRI_SERIES.length;
  const pmin = Math.min(...TRI_SERIES.map((k) => k.l)) - 3;
  const pmax = Math.max(...TRI_SERIES.map((k) => k.h)) + 4;
  const pY = (v: number) => BY + ((pmax - v) / (pmax - pmin)) * BH;
  const cX = (i: number) => BX + (i + 0.5) * (BW / N);
  const cw = Math.max(8, (BW / N) * 0.62);
  const nC = Math.round(interpolate(p(0.04, 0.42), [0, 1], [0, N]));
  const lineO = p(0.46, 0.62), boO = p(0.70, 0.84);
  // Resistance flat line (~120) and rising support
  const res_y = pY(120);
  const sup_x1 = cX(1), sup_y1 = pY(TRI_SERIES[1].l);
  const sup_x2 = cX(12), sup_y2 = pY(TRI_SERIES[12].l);
  return (
    <Stage>
      <Bg theme={T} accent={C} />
      <Head theme={T} kicker="CHART PATTERN — ASCENDING TRIANGLE" title="Flat Resistance + Rising Lows = Coiling Energy" color={C} />
      <Browser url="price-chart · DEMO · ASCENDING TRIANGLE" color={C} o={p(0.02, 0.08)}>
        {TRI_SERIES.slice(0, nC).map((k, i) => {
          const up = k.c >= k.o; const col = up ? G : R;
          const bt = pY(Math.max(k.o, k.c));
          return (
            <React.Fragment key={i}>
              <div style={{ position: "absolute", left: cX(i) - 1.5, top: pY(k.h), width: 3,
                height: Math.max(2, pY(k.l) - pY(k.h)), background: col, opacity: 0.82 }} />
              <div style={{ position: "absolute", left: cX(i) - cw / 2, top: bt, width: cw,
                height: Math.max(2, pY(Math.min(k.o, k.c)) - bt), borderRadius: 2, background: col,
                boxShadow: i === nC - 1 ? `0 0 10px ${col}` : "none" }} />
            </React.Fragment>
          );
        })}
        <svg style={{ position: "absolute", left: 0, top: 0, overflow: "visible" }} width={1500} height={626}>
          {lineO > 0 && <>
            <line x1={BX} y1={res_y} x2={BX + BW * 0.75} y2={res_y} stroke={R} strokeWidth={2.5} strokeDasharray="10 8" opacity={lineO} />
            <line x1={sup_x1} y1={sup_y1} x2={sup_x2} y2={sup_y2} stroke={G} strokeWidth={2.5} opacity={lineO} />
          </>}
        </svg>
        {lineO > 0 && <>
          <div style={{ position: "absolute", left: BX + BW * 0.76 + 10, top: res_y - 14,
            fontFamily: MONO, fontWeight: 800, fontSize: 20, color: R, opacity: lineO }}>RESISTANCE 120</div>
          <div style={{ position: "absolute", left: sup_x1, top: sup_y2 + 14,
            fontFamily: MONO, fontWeight: 800, fontSize: 20, color: G, opacity: lineO }}>RISING SUPPORT</div>
        </>}
        {boO > 0 && (
          <div style={{ position: "absolute", left: cX(15) - 60, top: pY(132) - 36, width: 150,
            textAlign: "center", fontFamily: MONO, fontWeight: 800, fontSize: 21, color: G, opacity: boO }}>BREAKOUT ↑</div>
        )}
        <div style={{ position: "absolute", left: 60, top: 510, width: 1380, fontFamily: SANS, fontSize: 23,
          color: T.muted, opacity: p(0.82, 0.92) }}>
          Buyers making higher lows while sellers hold the same ceiling — eventually buyers win.
        </div>
      </Browser>
      <Foot theme={T} p={p(0.86, 0.94)}>Descending triangle: flat support + falling highs → usually resolves downward.</Foot>
    </Stage>
  );
};

// ════════════════════════════════════════════ 19. VOLUME
const VolumeScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur); const frame = useCurrentFrame();
  const BX = 60, BY = 52, BW = 1380, BH = 310; // chart area
  const VY_TOP = 390, VH = 170; // volume area inside browser
  const N = TREND_UP.length;
  const pmin = Math.min(...TREND_UP.map((k) => k.l)) - 3;
  const pmax = Math.max(...TREND_UP.map((k) => k.h)) + 3;
  const pY = (v: number) => BY + ((pmax - v) / (pmax - pmin)) * BH;
  const cX = (i: number) => BX + (i + 0.5) * (BW / N);
  const cw = Math.max(5, (BW / N) * 0.62);
  const nC = Math.round(interpolate(p(0.04, 0.42), [0, 1], [0, N]));
  const volO = p(0.44, 0.56);
  const maxV = Math.max(...VOL_DATA.map((v) => v.v));
  return (
    <Stage>
      <Bg theme={T} accent={Y} />
      <Head theme={T} kicker="INDICATOR — VOLUME" title="Price Moves Mean More When Volume Confirms" color={Y} />
      <Browser url="price-chart + volume · DEMO" color={Y} o={p(0.02, 0.08)}>
        {/* price candles */}
        {TREND_UP.slice(0, nC).map((k, i) => {
          const up = k.c >= k.o; const col = up ? G : R;
          const bt = pY(Math.max(k.o, k.c));
          return (
            <React.Fragment key={i}>
              <div style={{ position: "absolute", left: cX(i) - 1.5, top: pY(k.h), width: 3,
                height: Math.max(2, pY(k.l) - pY(k.h)), background: col, opacity: 0.82 }} />
              <div style={{ position: "absolute", left: cX(i) - cw / 2, top: bt, width: cw,
                height: Math.max(2, pY(Math.min(k.o, k.c)) - bt), borderRadius: 2, background: col,
                boxShadow: i === nC - 1 ? `0 0 10px ${col}` : "none" }} />
            </React.Fragment>
          );
        })}
        {/* divider */}
        <div style={{ position: "absolute", left: BX, top: VY_TOP - 12, width: BW, height: 2,
          background: mix(T.line, Y, 0.4), opacity: volO }} />
        <div style={{ position: "absolute", left: BX, top: VY_TOP - 10, fontFamily: MONO, fontSize: 20,
          color: Y, opacity: volO }}>VOLUME</div>
        {/* volume bars */}
        {VOL_DATA.slice(0, nC).map((vd, i) => {
          const barH = (vd.v / maxV) * VH * p(0.44 + i * 0.002, 0.56);
          return (
            <div key={i} style={{ position: "absolute", left: cX(i) - cw / 2,
              top: VY_TOP + VH - barH, width: cw, height: Math.max(2, barH),
              background: vd.up ? mix(G, T.panel, 0.4) : mix(R, T.panel, 0.4),
              borderRadius: "2px 2px 0 0" }} />
          );
        })}
        {/* annotation */}
        <div style={{ position: "absolute", left: 60, top: 572, width: 1380, fontFamily: SANS, fontSize: 23,
          color: T.muted, opacity: p(0.72, 0.84) }}>
          Heavy green volume on up days = accumulation. Heavy red volume on down days = distribution.
        </div>
      </Browser>
      <Foot theme={T} p={p(0.86, 0.94)}>No volume data on the candle alone? Check the OBV line — it integrates volume direction over time.</Foot>
    </Stage>
  );
};

// ════════════════════════════════════════════ 20. MOVING AVERAGES
const MAScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur); const frame = useCurrentFrame();
  const BX = 60, BY = 64, BW = 1380, BH = 430;
  const N = 50; // show first 50 of 60
  const slice = MA_SERIES.slice(0, N);
  const pmin = Math.min(...slice.map((k) => k.l)) - 4;
  const pmax = Math.max(...slice.map((k) => k.h)) + 4;
  const pY = (v: number) => BY + ((pmax - v) / (pmax - pmin)) * BH;
  const cX = (i: number) => BX + (i + 0.5) * (BW / N);
  const cw = Math.max(5, (BW / N) * 0.62);
  const nC = Math.round(interpolate(p(0.04, 0.40), [0, 1], [0, N]));
  const smaO = p(0.42, 0.56), emaO = p(0.58, 0.70), gcO = p(0.74, 0.86);
  // find golden cross index (SMA10 crosses above SMA30)
  let gcIdx = 38;
  for (let i = 10; i < N; i++) {
    if (MA_SMA10[i] > MA_SMA30[i] && MA_SMA10[i - 1] <= MA_SMA30[i - 1]) { gcIdx = i; break; }
  }
  return (
    <Stage>
      <Bg theme={T} accent={Y} />
      <Head theme={T} kicker="INDICATOR — MOVING AVERAGES" title="SMA and EMA: Smoothing Out the Noise" color={Y} />
      <Browser url="price-chart · SMA10 · SMA30 · DEMO" color={Y} o={p(0.02, 0.08)}>
        {slice.slice(0, nC).map((k, i) => {
          const up = k.c >= k.o; const col = up ? G : R;
          const bt = pY(Math.max(k.o, k.c));
          return (
            <React.Fragment key={i}>
              <div style={{ position: "absolute", left: cX(i) - 1.5, top: pY(k.h), width: 3,
                height: Math.max(2, pY(k.l) - pY(k.h)), background: col, opacity: 0.65 }} />
              <div style={{ position: "absolute", left: cX(i) - cw / 2, top: bt, width: cw,
                height: Math.max(2, pY(Math.min(k.o, k.c)) - bt), borderRadius: 2, background: col, opacity: 0.75 }} />
            </React.Fragment>
          );
        })}
        <svg style={{ position: "absolute", left: 0, top: 0, overflow: "visible" }} width={1500} height={626}>
          {/* SMA-10 line */}
          {nC >= 10 && smaO > 0 && (
            <polyline points={MA_SMA10.slice(0, nC).map((v, i) => `${cX(i)},${pY(v)}`).join(" ")}
              fill="none" stroke={Y} strokeWidth={3.5} strokeLinecap="round" opacity={smaO} />
          )}
          {/* SMA-30 line */}
          {nC >= 30 && emaO > 0 && (
            <polyline points={MA_SMA30.slice(0, nC).map((v, i) => `${cX(i)},${pY(v)}`).join(" ")}
              fill="none" stroke={V} strokeWidth={3} strokeLinecap="round" opacity={emaO} strokeDasharray="none" />
          )}
          {/* Golden cross circle */}
          {gcO > 0 && nC > gcIdx && (
            <circle cx={cX(gcIdx)} cy={pY(MA_SMA10[gcIdx])} r={16}
              fill="none" stroke={G} strokeWidth={3} opacity={gcO} />
          )}
        </svg>
        {/* legend */}
        <div style={{ position: "absolute", left: 1100, top: 28, display: "flex", flexDirection: "column", gap: 8 }}>
          <div style={{ display: "flex", alignItems: "center", gap: 10, opacity: smaO }}>
            <div style={{ width: 34, height: 4, background: Y, borderRadius: 2 }} />
            <span style={{ fontFamily: MONO, fontSize: 21, color: Y }}>SMA 10 (fast)</span>
          </div>
          <div style={{ display: "flex", alignItems: "center", gap: 10, opacity: emaO }}>
            <div style={{ width: 34, height: 4, background: V, borderRadius: 2 }} />
            <span style={{ fontFamily: MONO, fontSize: 21, color: V }}>SMA 30 (slow)</span>
          </div>
        </div>
        {gcO > 0 && nC > gcIdx && (
          <div style={{ position: "absolute", left: cX(gcIdx) - 60, top: pY(MA_SMA10[gcIdx]) - 52, width: 200,
            fontFamily: MONO, fontWeight: 800, fontSize: 20, color: G, opacity: gcO }}>
            GOLDEN CROSS ↑
          </div>
        )}
        <div style={{ position: "absolute", left: 60, top: 510, width: 1380, fontFamily: SANS, fontSize: 23,
          color: T.muted, opacity: p(0.84, 0.94) }}>
          Golden Cross: fast MA above slow MA = bullish. Death Cross: fast below slow = bearish bias.
        </div>
      </Browser>
      <Foot theme={T} p={p(0.86, 0.94)}>MAs lag — they confirm trends, not predict them. Use with price action, not instead of it.</Foot>
    </Stage>
  );
};

// ════════════════════════════════════════════ 21. RSI
const RSIScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur); const frame = useCurrentFrame();
  const BX = 60, BY = 48, BW = 1380, BH = 280; // chart
  const RY = 362, RH = 180; // RSI pane
  const N = RSI_BASE.length;
  const pmin = Math.min(...RSI_BASE.map((k) => k.l)) - 3;
  const pmax = Math.max(...RSI_BASE.map((k) => k.h)) + 3;
  const pY = (v: number) => BY + ((pmax - v) / (pmax - pmin)) * BH;
  const cX = (i: number) => BX + (i + 0.5) * (BW / N);
  const cw = Math.max(4, (BW / N) * 0.62);
  const nC = Math.round(interpolate(p(0.04, 0.40), [0, 1], [0, N]));
  const rsiO = p(0.44, 0.58), zonesO = p(0.58, 0.70);
  const rsiY = (v: number) => RY + ((100 - v) / 100) * RH;
  const cross = 60 + ((frame * 1.8) % 1380);
  return (
    <Stage>
      <Bg theme={T} accent={Y} />
      <Head theme={T} kicker="INDICATOR — RSI (RELATIVE STRENGTH INDEX)" title="Measuring Momentum: Is the Market Overstretched?" color={Y} />
      <Browser url="price-chart + RSI(10) · DEMO" color={Y} o={p(0.02, 0.08)}>
        {RSI_BASE.slice(0, nC).map((k, i) => {
          const up = k.c >= k.o; const col = up ? G : R;
          const bt = pY(Math.max(k.o, k.c));
          return (
            <React.Fragment key={i}>
              <div style={{ position: "absolute", left: cX(i) - 1.5, top: pY(k.h), width: 3,
                height: Math.max(2, pY(k.l) - pY(k.h)), background: col, opacity: 0.75 }} />
              <div style={{ position: "absolute", left: cX(i) - cw / 2, top: bt, width: cw,
                height: Math.max(2, pY(Math.min(k.o, k.c)) - bt), borderRadius: 2, background: col }} />
            </React.Fragment>
          );
        })}
        {/* RSI pane divider */}
        <div style={{ position: "absolute", left: BX, top: RY - 12, width: BW, height: 2,
          background: mix(T.line, Y, 0.4), opacity: rsiO }} />
        <div style={{ position: "absolute", left: BX, top: RY - 10, fontFamily: MONO, fontSize: 19,
          color: Y, opacity: rsiO }}>RSI (10)</div>
        <svg style={{ position: "absolute", left: 0, top: 0, overflow: "visible" }} width={1500} height={626}>
          {/* overbought / oversold zones */}
          {zonesO > 0 && <>
            <rect x={BX} y={rsiY(70)} width={BW} height={rsiY(30) - rsiY(70)} fill={mix(T.panel, R, 0.06)} opacity={zonesO * 0.6} />
            <line x1={BX} y1={rsiY(70)} x2={BX + BW} y2={rsiY(70)} stroke={R} strokeWidth={1.5} strokeDasharray="6 8" opacity={zonesO} />
            <text x={BX + BW + 8} y={rsiY(70) + 5} fill={R} fontFamily={MONO} fontSize={18} opacity={zonesO}>70</text>
            <line x1={BX} y1={rsiY(30)} x2={BX + BW} y2={rsiY(30)} stroke={G} strokeWidth={1.5} strokeDasharray="6 8" opacity={zonesO} />
            <text x={BX + BW + 8} y={rsiY(30) + 5} fill={G} fontFamily={MONO} fontSize={18} opacity={zonesO}>30</text>
          </>}
          {/* RSI line */}
          {rsiO > 0 && nC >= 2 && (
            <polyline points={RSI_VALS.slice(0, nC).map((v, i) => `${cX(i)},${rsiY(v)}`).join(" ")}
              fill="none" stroke={Y} strokeWidth={3} strokeLinecap="round" opacity={rsiO} />
          )}
          {/* crosshair */}
          {cross < 1440 && <line x1={cross} y1={BY} x2={cross} y2={RY + RH} stroke={mix(T.muted, Y, 0.3)} strokeWidth={1.5} strokeDasharray="5 7" opacity={0.45} />}
        </svg>
        <div style={{ position: "absolute", left: 60, top: 558, width: 1380, fontFamily: SANS, fontSize: 22,
          color: T.muted, opacity: p(0.74, 0.86) }}>
          RSI &gt;70 = overbought — but in a strong trend it can STAY overbought for weeks. Context matters.
        </div>
      </Browser>
      <Foot theme={T} p={p(0.86, 0.94)}>RSI divergence is more powerful than level alone — lower RSI highs while price makes higher highs = warning.</Foot>
    </Stage>
  );
};

// ════════════════════════════════════════════ 22. MACD
const MACDScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur); const frame = useCurrentFrame();
  const BX = 60, BY = 48, BW = 1380, BH = 280;
  const MY = 358, MH = 190; // MACD pane
  const N = MACD_BASE.length;
  const pmin = Math.min(...MACD_BASE.map((k) => k.l)) - 3;
  const pmax = Math.max(...MACD_BASE.map((k) => k.h)) + 3;
  const pY = (v: number) => BY + ((pmax - v) / (pmax - pmin)) * BH;
  const cX = (i: number) => BX + (i + 0.5) * (BW / N);
  const cw = Math.max(4, (BW / N) * 0.62);
  const nC = Math.round(interpolate(p(0.04, 0.40), [0, 1], [0, N]));
  const macdO = p(0.44, 0.58), histO = p(0.60, 0.74), crossO = p(0.76, 0.88);
  const mMin = Math.min(...MACD_HIST), mMax = Math.max(...MACD_HIST);
  const mRange = Math.max(Math.abs(mMin), Math.abs(mMax));
  const mZero = MY + MH / 2;
  const mY = (v: number) => mZero - (v / mRange) * (MH / 2);
  // find bullish crossover
  let crossIdx = 30;
  for (let i = 5; i < N; i++) {
    if (MACD_LINE[i] > MACD_SIGNAL[i] && MACD_LINE[i - 1] <= MACD_SIGNAL[i - 1]) { crossIdx = i; break; }
  }
  return (
    <Stage>
      <Bg theme={T} accent={Y} />
      <Head theme={T} kicker="INDICATOR — MACD" title="Signal Line Crossovers and Momentum Shifts" color={Y} />
      <Browser url="price-chart + MACD(12,26,9) · DEMO" color={Y} o={p(0.02, 0.08)}>
        {MACD_BASE.slice(0, nC).map((k, i) => {
          const up = k.c >= k.o; const col = up ? G : R;
          const bt = pY(Math.max(k.o, k.c));
          return (
            <React.Fragment key={i}>
              <div style={{ position: "absolute", left: cX(i) - 1.5, top: pY(k.h), width: 3,
                height: Math.max(2, pY(k.l) - pY(k.h)), background: col, opacity: 0.72 }} />
              <div style={{ position: "absolute", left: cX(i) - cw / 2, top: bt, width: cw,
                height: Math.max(2, pY(Math.min(k.o, k.c)) - bt), borderRadius: 2, background: col }} />
            </React.Fragment>
          );
        })}
        <div style={{ position: "absolute", left: BX, top: MY - 14, width: BW, height: 2,
          background: mix(T.line, Y, 0.4), opacity: macdO }} />
        <div style={{ position: "absolute", left: BX, top: MY - 12, fontFamily: MONO, fontSize: 19, color: Y, opacity: macdO }}>MACD</div>
        <svg style={{ position: "absolute", left: 0, top: 0, overflow: "visible" }} width={1500} height={626}>
          {/* zero line */}
          {macdO > 0 && <line x1={BX} y1={mZero} x2={BX + BW} y2={mZero} stroke={mix(T.line, Y, 0.5)} strokeWidth={1.5} opacity={macdO} />}
          {/* histogram */}
          {histO > 0 && MACD_HIST.slice(0, nC).map((v, i) => (
            <rect key={i} x={cX(i) - cw / 2} y={v >= 0 ? mY(v) : mZero} width={cw}
              height={Math.max(2, Math.abs(mY(v) - mZero))}
              fill={v >= 0 ? mix(G, T.panel, 0.3) : mix(R, T.panel, 0.3)} opacity={histO} />
          ))}
          {/* MACD line */}
          {macdO > 0 && nC >= 13 && (
            <polyline points={MACD_LINE.slice(0, nC).map((v, i) => `${cX(i)},${mY(v)}`).join(" ")}
              fill="none" stroke={C} strokeWidth={2.5} strokeLinecap="round" opacity={macdO} />
          )}
          {/* Signal line */}
          {macdO > 0 && nC >= 22 && (
            <polyline points={MACD_SIGNAL.slice(0, nC).map((v, i) => `${cX(i)},${mY(v)}`).join(" ")}
              fill="none" stroke={Y} strokeWidth={2} strokeLinecap="round" strokeDasharray="8 6" opacity={macdO} />
          )}
          {/* crossover circle */}
          {crossO > 0 && nC > crossIdx && (
            <circle cx={cX(crossIdx)} cy={mY(MACD_LINE[crossIdx])} r={14}
              fill="none" stroke={G} strokeWidth={3} opacity={crossO} />
          )}
        </svg>
        {crossO > 0 && nC > crossIdx && (
          <div style={{ position: "absolute", left: cX(crossIdx) - 80, top: mY(MACD_LINE[crossIdx]) - 38, width: 220,
            textAlign: "center", fontFamily: MONO, fontWeight: 800, fontSize: 20, color: G, opacity: crossO }}>
            BULLISH CROSS ↑
          </div>
        )}
        <div style={{ position: "absolute", left: 60, top: 560, width: 1380, fontFamily: SANS, fontSize: 22,
          color: T.muted, opacity: p(0.80, 0.92) }}>
          MACD line crosses above signal = bullish momentum. Histogram turning positive is the early signal.
        </div>
      </Browser>
      <Foot theme={T} p={p(0.86, 0.94)}>MACD is a lagging indicator — it confirms trends. Best used with SR or candlestick signals.</Foot>
    </Stage>
  );
};

// ════════════════════════════════════════════ 23. BOLLINGER BANDS
const BBScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur); const frame = useCurrentFrame();
  const BX = 60, BY = 64, BW = 1380, BH = 430;
  const N = BB_BASE.length;
  const allPrices = BB_BASE.map((k) => k.h).concat(BB_UPPER, BB_LOWER);
  const pmin = Math.min(...allPrices) - 4;
  const pmax = Math.max(...allPrices) + 4;
  const pY = (v: number) => BY + ((pmax - v) / (pmax - pmin)) * BH;
  const cX = (i: number) => BX + (i + 0.5) * (BW / N);
  const cw = Math.max(5, (BW / N) * 0.62);
  const nC = Math.round(interpolate(p(0.04, 0.42), [0, 1], [0, N]));
  const bandO = p(0.46, 0.60), sqO = p(0.64, 0.78);
  // Find squeeze zone (bands closest together) — around index 10-16 roughly
  const bandWidths = BB_UPPER.map((u, i) => u - BB_LOWER[i]);
  const minBW = Math.min(...bandWidths.slice(5, 30));
  const squeezeIdx = bandWidths.indexOf(minBW);
  return (
    <Stage>
      <Bg theme={T} accent={Y} />
      <Head theme={T} kicker="INDICATOR — BOLLINGER BANDS" title="Volatility Breathing: Squeeze Then Expansion" color={Y} />
      <Browser url="price-chart + Bollinger Bands · DEMO" color={Y} o={p(0.02, 0.08)}>
        {BB_BASE.slice(0, nC).map((k, i) => {
          const up = k.c >= k.o; const col = up ? G : R;
          const bt = pY(Math.max(k.o, k.c));
          return (
            <React.Fragment key={i}>
              <div style={{ position: "absolute", left: cX(i) - 1.5, top: pY(k.h), width: 3,
                height: Math.max(2, pY(k.l) - pY(k.h)), background: col, opacity: 0.72 }} />
              <div style={{ position: "absolute", left: cX(i) - cw / 2, top: bt, width: cw,
                height: Math.max(2, pY(Math.min(k.o, k.c)) - bt), borderRadius: 2, background: col }} />
            </React.Fragment>
          );
        })}
        <svg style={{ position: "absolute", left: 0, top: 0, overflow: "visible" }} width={1500} height={626}>
          {/* BB fill region */}
          {bandO > 0 && nC >= 10 && (
            <polygon points={
              BB_UPPER.slice(0, nC).map((v, i) => `${cX(i)},${pY(v)}`).join(" ") + " " +
              [...BB_LOWER.slice(0, nC)].reverse().map((v, i) => `${cX(nC - 1 - i)},${pY(v)}`).join(" ")
            } fill={mix(T.panel, Y, 0.12)} opacity={bandO * 0.7} />
          )}
          {/* Upper band */}
          {bandO > 0 && nC >= 10 && (
            <polyline points={BB_UPPER.slice(0, nC).map((v, i) => `${cX(i)},${pY(v)}`).join(" ")}
              fill="none" stroke={Y} strokeWidth={2} strokeDasharray="7 5" opacity={bandO} />
          )}
          {/* Middle band (SMA) */}
          {bandO > 0 && nC >= 10 && (
            <polyline points={BB_SMA.slice(0, nC).map((v, i) => `${cX(i)},${pY(v)}`).join(" ")}
              fill="none" stroke={mix(T.muted, Y, 0.4)} strokeWidth={1.5} opacity={bandO} />
          )}
          {/* Lower band */}
          {bandO > 0 && nC >= 10 && (
            <polyline points={BB_LOWER.slice(0, nC).map((v, i) => `${cX(i)},${pY(v)}`).join(" ")}
              fill="none" stroke={Y} strokeWidth={2} strokeDasharray="7 5" opacity={bandO} />
          )}
          {/* squeeze indicator */}
          {sqO > 0 && nC > squeezeIdx && (
            <rect x={cX(Math.max(0, squeezeIdx - 3))} y={BY}
              width={cX(squeezeIdx + 3) - cX(squeezeIdx - 3)} height={BH}
              fill={mix(T.panel, V, 0.18)} opacity={sqO * 0.7} rx={4} />
          )}
        </svg>
        {sqO > 0 && nC > squeezeIdx && (
          <div style={{ position: "absolute", left: cX(squeezeIdx) - 70, top: BY - 36, width: 200,
            textAlign: "center", fontFamily: MONO, fontWeight: 800, fontSize: 20, color: V, opacity: sqO }}>
            SQUEEZE → EXPANSION
          </div>
        )}
        <div style={{ position: "absolute", left: 60, top: 510, width: 1380, fontFamily: SANS, fontSize: 22,
          color: T.muted, opacity: p(0.80, 0.92) }}>
          Bands narrow (squeeze) → low volatility → expect a BIG move. Direction not guaranteed.
        </div>
      </Browser>
      <Foot theme={T} p={p(0.86, 0.94)}>Touching the band ≠ reversal. In strong trends price "walks the band" — use with RSI or candles.</Foot>
    </Stage>
  );
};

// ════════════════════════════════════════════ 24. CONFLUENCE
const ConfluenceScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur); const frame = useCurrentFrame();
  const items = [
    { emoji: "📊", label: "Support Zone", sub: "Price bounced here 3×", color: G },
    { emoji: "🕯️", label: "Bullish Doji",  sub: "Indecision at support",  color: C },
    { emoji: "📉", label: "RSI Oversold", sub: "RSI < 30 for first time", color: Y },
    { emoji: "📈", label: "Volume Spike",  sub: "2× avg — big buyer",      color: V },
    { emoji: "📏", label: "SMA Touch",     sub: "Price at SMA-200",        color: Y },
  ];
  return (
    <Stage>
      <Bg theme={T} accent={G} />
      <Head theme={T} kicker="PUTTING IT TOGETHER — CONFLUENCE" title="When Multiple Signals Agree, Probability Rises" color={G} />
      {/* center hub */}
      <div style={{ position: "absolute", left: 760, top: 410, width: 400, height: 160,
        borderRadius: 24, background: mix(T.panel, G, 0.18), border: `3px solid ${G}`,
        display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center",
        boxShadow: `0 0 ${36 + Math.sin(frame * 0.05) * 12}px ${mix(T.bg0, G, 0.55)}`,
        opacity: p(0.04, 0.16) }}>
        <div style={{ fontFamily: MONO, fontWeight: 800, fontSize: 22, color: G }}>HIGH-PROBABILITY</div>
        <div style={{ fontFamily: MONO, fontWeight: 800, fontSize: 22, color: G }}>SETUP ZONE</div>
      </div>
      {/* orbit items */}
      {items.map((it, i) => {
        const ang = (i / items.length) * Math.PI * 2 - Math.PI / 2 + Math.sin(frame * 0.007) * 0.05;
        const ox = 960 + Math.cos(ang) * 550, oy = 540 + Math.sin(ang) * 260;
        const at = 0.12 + i * 0.10;
        const active = Math.floor(frame / 30) % items.length === i && p(0.65, 0.66) > 0.5;
        return (
          <React.Fragment key={i}>
            <Wire x1={960} y1={540} x2={ox} y2={oy} p={p(at, at + 0.07)}
              color={active ? it.color : mix(T.muted, it.color, 0.5)} w={active ? 3 : 2} arrow={false} />
            <div style={{ position: "absolute", left: ox - 175, top: oy - 50, width: 350, height: 100,
              borderRadius: 16, background: mix(T.panel, active ? it.color : T.line, active ? 0.2 : 0.08),
              border: `2.5px solid ${active ? it.color : mix(T.line, it.color, 0.5)}`,
              display: "flex", alignItems: "center", gap: 14, padding: "0 20px", boxSizing: "border-box",
              opacity: p(at, at + 0.09), transform: `scale(${active ? 1.06 : 1})` }}>
              <span style={{ fontSize: 34 }}>{it.emoji}</span>
              <div>
                <div style={{ fontFamily: SANS, fontWeight: 700, fontSize: 24, color: T.text }}>{it.label}</div>
                <div style={{ fontFamily: MONO, fontSize: 20, color: T.muted }}>{it.sub}</div>
              </div>
            </div>
          </React.Fragment>
        );
      })}
      <Foot theme={T} p={p(0.82, 0.92)}>No single signal is reliable alone. Stack 3–4 signals pointing the same way — that's your edge.</Foot>
    </Stage>
  );
};

// ════════════════════════════════════════════ 25. RISK MANAGEMENT
const RISK_ENTRY = 100, RISK_SL = 96, RISK_TGT = 108;
const RiskScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur); const frame = useCurrentFrame(); const pop = usePop(dur);
  // Diagram occupies left half; right panel occupies x 1070–1780
  const RX = 130, RY_TOP = 270, RY_BOT = 840, RW = 840;
  const rPmin = 90, rPmax = 115;
  const rPY = (v: number) => RY_TOP + ((rPmax - v) / (rPmax - rPmin)) * (RY_BOT - RY_TOP);
  const entryY = rPY(RISK_ENTRY), slY = rPY(RISK_SL), tgtY = rPY(RISK_TGT);
  const riskR = RISK_ENTRY - RISK_SL; // 4
  const rewardR = RISK_TGT - RISK_ENTRY; // 8
  const rrRatio = rewardR / riskR; // 2
  const entryO = p(0.04, 0.16), slO = p(0.20, 0.34), tgtO = p(0.40, 0.52);
  const posO = p(0.30, 0.42);  // position-size card — appears alongside stop zone
  const statO = p(0.48, 0.60); // trade stats — visible well before 60% frame
  return (
    <Stage>
      <Bg theme={T} accent={G} />
      <Head theme={T} kicker="PUTTING IT TOGETHER — RISK MANAGEMENT" title="Know Your Max Loss BEFORE You Enter" color={G} />
      {/* ── LEFT: zone diagram ── */}
      {entryO > 0 && <>
        <div style={{ position: "absolute", left: RX, top: entryY, width: RW, height: 3, background: Y, opacity: entryO }} />
        <div style={{ position: "absolute", left: RX + RW + 12, top: entryY - 14,
          fontFamily: MONO, fontWeight: 800, fontSize: 21, color: Y, opacity: entryO }}>ENTRY {RISK_ENTRY}</div>
      </>}
      {slO > 0 && <>
        <div style={{ position: "absolute", left: RX, top: entryY, width: RW, height: slY - entryY,
          background: mix(T.panel, R, 0.18), opacity: slO }} />
        <div style={{ position: "absolute", left: RX, top: slY, width: RW, height: 3, background: R, opacity: slO }} />
        <div style={{ position: "absolute", left: RX + RW + 12, top: slY - 14,
          fontFamily: MONO, fontWeight: 800, fontSize: 21, color: R, opacity: slO }}>STOP {RISK_SL} (−{riskR} = 1R)</div>
        <div style={{ position: "absolute", left: RX + RW / 2 - 80, top: entryY + 12,
          fontFamily: MONO, fontSize: 21, color: R, opacity: slO }}>MAX LOSS = 1R</div>
      </>}
      {tgtO > 0 && <>
        <div style={{ position: "absolute", left: RX, top: tgtY, width: RW, height: entryY - tgtY,
          background: mix(T.panel, G, 0.18), opacity: tgtO }} />
        <div style={{ position: "absolute", left: RX, top: tgtY, width: RW, height: 3, background: G, opacity: tgtO }} />
        <div style={{ position: "absolute", left: RX + RW + 12, top: tgtY - 14,
          fontFamily: MONO, fontWeight: 800, fontSize: 21, color: G, opacity: tgtO }}>TARGET {RISK_TGT} (+{rewardR} = 2R)</div>
        <div style={{ position: "absolute", left: RX + RW / 2 - 80, top: tgtY + 12,
          fontFamily: MONO, fontSize: 21, color: G, opacity: tgtO }}>REWARD = 2R</div>
      </>}
      {/* ── RIGHT: position sizing + trade stats ── */}
      {/* Position size card — appears with stop zone */}
      <div style={{ position: "absolute", left: 1070, top: 270, width: 660, borderRadius: 18,
        background: mix(T.panel, Y, 0.09), border: `2px solid ${mix(T.line, Y, 0.55)}`,
        padding: "26px 30px", boxSizing: "border-box",
        opacity: posO, transform: `translateY(${(1 - posO) * 18}px)` }}>
        <div style={{ fontFamily: MONO, fontWeight: 800, fontSize: 22, color: Y, marginBottom: 20 }}>POSITION SIZING</div>
        {[
          { l: "Account capital", v: "₹1,00,000", c: T.text },
          { l: "Max risk per trade", v: "2% = ₹2,000", c: Y },
          { l: "Stop distance", v: `${riskR} pts / share`, c: R },
          { l: "Shares to buy", v: `₹2,000 ÷ ₹${riskR} = 500`, c: G },
        ].map((row, i) => (
          <div key={i} style={{ display: "flex", justifyContent: "space-between", marginBottom: 14,
            opacity: p(0.32 + i * 0.04, 0.42 + i * 0.04) }}>
            <span style={{ fontFamily: MONO, fontSize: 21, color: T.muted }}>{row.l}</span>
            <span style={{ fontFamily: MONO, fontWeight: 800, fontSize: 21, color: row.c }}>{row.v}</span>
          </div>
        ))}
      </div>
      {/* Trade stats card */}
      <div style={{ position: "absolute", left: 1070, top: 584, width: 660, borderRadius: 18,
        background: mix(T.panel, G, 0.12), border: `2.5px solid ${G}`,
        padding: "26px 30px", boxSizing: "border-box",
        opacity: statO, transform: `scale(${pop(0.48)})` }}>
        <div style={{ fontFamily: MONO, fontWeight: 800, fontSize: 22, color: G, marginBottom: 18 }}>TRADE STATS</div>
        {[
          { l: "RISK (1R)",       v: `₹${riskR * 100}`,    c: R },
          { l: "REWARD (2R)",     v: `₹${rewardR * 100}`,  c: G },
          { l: "R:R RATIO",       v: `${rrRatio}:1`,        c: Y },
          { l: "WIN RATE NEEDED", v: "34%",                 c: C },
        ].map((st, i) => (
          <div key={i} style={{ display: "flex", justifyContent: "space-between", marginBottom: 12,
            opacity: p(0.50 + i * 0.04, 0.60 + i * 0.04) }}>
            <span style={{ fontFamily: MONO, fontSize: 21, color: T.muted }}>{st.l}</span>
            <span style={{ fontFamily: MONO, fontWeight: 800, fontSize: 21, color: st.c }}>{st.v}</span>
          </div>
        ))}
        <div style={{ fontFamily: MONO, fontSize: 20, color: mix(T.muted, G, 0.5), marginTop: 6,
          opacity: p(0.66, 0.76), fontStyle: "italic" }}>
          Lose 2 of 3 — still profitable if winners are 2× losses
        </div>
      </div>
      <Foot theme={T} p={p(0.84, 0.93)}>At 2:1 R:R you only need to be right 34% of the time to be profitable long-term.</Foot>
    </Stage>
  );
};

// ════════════════════════════════════════════ 26. CHECKLIST
const ChecklistScene: React.FC<{ dur?: number; items?: string[] }> = ({ dur, items = [] }) => {
  const p = useP(dur); const frame = useCurrentFrame();
  const hot = Math.floor(frame / 32) % Math.max(1, items.length);
  return (
    <Stage>
      <Bg theme={T} accent={C} />
      <Head theme={T} kicker="THE PRE-TRADE RITUAL" title="8 Questions Before Every Trade" color={C} />
      <div style={{ position: "absolute", left: 130, top: 210, width: 1660, display: "flex", flexWrap: "wrap", gap: 22 }}>
        {items.map((item, i) => {
          const at = 0.06 + i * 0.08;
          const lo = p(at, at + 0.07);
          const isHot = hot === i && p(0.74, 0.75) > 0.5;
          return (
            <div key={i} style={{ width: 780, display: "flex", alignItems: "flex-start", gap: 18,
              opacity: lo, transform: `translateX(${(1 - lo) * 22}px)` }}>
              <div style={{ width: 5, height: 54, borderRadius: 3, background: C, flexShrink: 0, marginTop: 4 }} />
              <div style={{ width: 48, height: 48, borderRadius: 10, flexShrink: 0,
                background: isHot ? C : mix(T.panel, C, 0.2), border: `2px solid ${C}`,
                display: "flex", alignItems: "center", justifyContent: "center",
                fontFamily: MONO, fontWeight: 800, fontSize: 22, color: isHot ? T.bg0 : C }}>
                {String(i + 1).padStart(2, "0")}
              </div>
              <div style={{ fontFamily: SANS, fontSize: 26, color: T.text, lineHeight: 1.35, width: 700 }}>{item}</div>
            </div>
          );
        })}
      </div>
      <Foot theme={T} p={p(0.82, 0.92)}>If you can't answer all 8, the setup isn't ready. Wait for the next one.</Foot>
    </Stage>
  );
};

// ════════════════════════════════════════════ 27. RECAP
const RecapScene: React.FC<{ dur?: number; items?: string[]; closer?: string }> = ({ dur, items = [], closer = "" }) => {
  const p = useP(dur); const frame = useCurrentFrame();
  return (
    <Stage>
      <Bg theme={T} accent={C} />
      <div style={{ position: "absolute", left: 0, right: 0, top: 96, textAlign: "center" }}>
        <div style={{ fontFamily: MONO, fontWeight: 800, fontSize: 22, color: C, letterSpacing: 8,
          opacity: p(0.03, 0.12) }}>RECAP — THE WHOLE MAP</div>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 60, color: T.text, letterSpacing: -2,
          marginTop: 14, opacity: p(0.10, 0.22) }}>Technical Analysis in One Breath</div>
      </div>
      <div style={{ position: "absolute", left: 130, top: 240, width: 1660 }}>
        {items.map((item, i) => {
          const at = 0.05 + i * 0.08;
          const lo = p(at, at + 0.06);
          return (
            <div key={i} style={{ display: "flex", alignItems: "center", gap: 18, marginBottom: 20, opacity: lo,
              transform: `translateX(${(1 - lo) * 20}px)` }}>
              <div style={{ width: 5, height: 36, borderRadius: 3, background: C, flexShrink: 0 }} />
              <div style={{ fontFamily: MONO, fontWeight: 800, fontSize: 21, color: C, width: 44, flexShrink: 0 }}>
                {String(i + 1).padStart(2, "0")}
              </div>
              <div style={{ fontFamily: SANS, fontSize: 26, color: T.text, lineHeight: 1.3, width: 1560 }}>{item}</div>
            </div>
          );
        })}
      </div>
      {closer && (
        <div style={{ position: "absolute", left: 130, bottom: 110, right: 130, textAlign: "center",
          fontFamily: SANS, fontStyle: "italic", fontSize: 38, color: C,
          textShadow: `0 0 40px ${mix(T.bg0, C, 0.6)}`,
          opacity: p(0.78, 0.90), lineHeight: 1.3 }}>{closer}</div>
      )}
      {/* disclaimer */}
      <div style={{ position: "absolute", left: 130, top: 984, right: 130, textAlign: "center",
        fontFamily: MONO, fontSize: 20, color: R,
        opacity: 0.5 + Math.sin(frame * 0.06) * 0.3 }}>
        ⚠ Education only · Not investment advice · Consult a SEBI-registered advisor before investing
      </div>
    </Stage>
  );
};

// ════════════════════════════════════════════ DISPATCHER
export const TACScene: React.FC<{ variant: string; [key: string]: unknown }> = ({ variant, ...rest }) => {
  switch (variant) {
    case "tac_title":      return <TitleScene {...(rest as any)} />;
    case "tac_div":        return <DividerScene {...(rest as any)} />;
    case "tac_whyta":      return <WhyTAScene {...(rest as any)} />;
    case "tac_timeframes": return <TimeframesScene {...(rest as any)} />;
    case "tac_anatomy":    return <CandleAnatomyScene {...(rest as any)} />;
    case "tac_doji":       return <DojiScene {...(rest as any)} />;
    case "tac_hammer":     return <HammerScene {...(rest as any)} />;
    case "tac_marubozu":   return <MarubozuScene {...(rest as any)} />;
    case "tac_engulfing":  return <EngulfingScene {...(rest as any)} />;
    case "tac_harami":     return <HaramiScene {...(rest as any)} />;
    case "tac_morningstar":return <MorningStarScene {...(rest as any)} />;
    case "tac_threewhite": return <ThreeWhiteScene {...(rest as any)} />;
    case "tac_sr":         return <SRScene {...(rest as any)} />;
    case "tac_trendlines": return <TrendlineScene {...(rest as any)} />;
    case "tac_hs":         return <HeadShouldersScene {...(rest as any)} />;
    case "tac_doubletop":  return <DoubleTopScene {...(rest as any)} />;
    case "tac_flag":       return <FlagScene {...(rest as any)} />;
    case "tac_triangle":   return <TriangleScene {...(rest as any)} />;
    case "tac_volume":     return <VolumeScene {...(rest as any)} />;
    case "tac_ma":         return <MAScene {...(rest as any)} />;
    case "tac_rsi":        return <RSIScene {...(rest as any)} />;
    case "tac_macd":       return <MACDScene {...(rest as any)} />;
    case "tac_bb":         return <BBScene {...(rest as any)} />;
    case "tac_confluence": return <ConfluenceScene {...(rest as any)} />;
    case "tac_risk":       return <RiskScene {...(rest as any)} />;
    case "tac_checklist":  return <ChecklistScene {...(rest as any)} />;
    case "tac_recap":      return <RecapScene {...(rest as any)} />;
    default: return null;
  }
};
