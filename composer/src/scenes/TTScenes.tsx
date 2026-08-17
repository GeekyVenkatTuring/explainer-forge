/**
 * TTScenes.tsx — "The Trader's Toolkit" custom scenes (prefix `tt`).
 * Identity: dark theme + browser-window motif (chrome bar + URL pill + scan beam).
 * Semantic accents: G green=fundamentals · C cyan=charting · V violet=options ·
 * Y amber=backtesting · R rose=warnings/learning.
 * Doctrine: compute the real thing — the screener FILTERS a dataset, the payoff
 * graph is REAL option math, candles/SMA/RSI and the equity curve are computed
 * deterministically at module scope. Demo panels carry a "DEMO DATA" chip.
 */
import React from "react";
import { useCurrentFrame, interpolate } from "remotion";
import {
  makeTheme, mix, MONO, SANS, useP, usePop, rnd,
  Stage, Bg, Head, Foot, Wire, Flow, Counter, Type, ScanBeam, Brackets,
} from "../lib/primitives";

const T = makeTheme({});
const G = "#34D399", C = "#22D3EE", V = "#A78BFA", Y = "#FBBF24", R = "#FB7185";

// ---------------------------------------------------------------- shared: browser frame
const Browser: React.FC<{
  url: string; color: string; o: number; x?: number; y?: number; w?: number; h?: number;
  demo?: boolean; children?: React.ReactNode;
}> = ({ url, color, o, x = 210, y = 205, w = 1500, h = 680, demo = true, children }) => {
  const frame = useCurrentFrame();
  return (
    <div style={{ position: "absolute", left: x, top: y, width: w, height: h, borderRadius: 20,
      background: mix(T.bg1, color, 0.04), border: `2.5px solid ${mix(T.line, color, 0.5)}`,
      boxShadow: `0 0 ${34 + Math.sin(frame * 0.05) * 10}px ${mix(T.bg0, color, 0.35)}`,
      opacity: o, transform: `translateY(${(1 - o) * 24}px)`, overflow: "hidden" }}>
      {/* chrome bar */}
      <div style={{ height: 54, background: mix(T.bg0, color, 0.08), borderBottom: `2px solid ${mix(T.line, color, 0.4)}`,
        display: "flex", alignItems: "center", gap: 10, padding: "0 22px" }}>
        {[R, Y, G].map((c, i) => (
          <div key={i} style={{ width: 14, height: 14, borderRadius: 7, background: mix(c, T.bg0, 0.25) }} />
        ))}
        <div style={{ marginLeft: 16, flex: 1, maxWidth: 640, height: 32, borderRadius: 999,
          background: mix(T.bg0, color, 0.14), border: `1.5px solid ${mix(T.line, color, 0.45)}`,
          display: "flex", alignItems: "center", gap: 10, padding: "0 16px" }}>
          <span style={{ fontSize: 15, color }}>🔒</span>
          <span style={{ fontFamily: MONO, fontSize: 20, color: mix(T.muted, color, 0.45), letterSpacing: 0.5 }}>{url}</span>
        </div>
        {demo && (
          <div style={{ marginLeft: "auto", fontFamily: MONO, fontWeight: 700, fontSize: 19, color: T.bg0,
            background: mix(color, T.bg0, 0.12), borderRadius: 8, padding: "4px 12px", letterSpacing: 2 }}>DEMO DATA</div>
        )}
      </div>
      <div style={{ position: "relative", height: h - 54 }}>{children}</div>
    </div>
  );
};

// ================================================================ 1. SCREENER — query filters a real dataset
type Stk = { n: string; roce: number; de: number; g: number };
const STOCKS: Stk[] = [
  { n: "Astra Polymers", roce: 31, de: 0.1, g: 18 }, { n: "Deccan Textiles", roce: 9, de: 1.4, g: 4 },
  { n: "Kaveri Pharma", roce: 27, de: 0.2, g: 22 }, { n: "Northline Infra", roce: 11, de: 2.1, g: 9 },
  { n: "Suvarna Foods", roce: 24, de: 0.0, g: 15 }, { n: "Metro Retail Co", roce: 14, de: 0.8, g: 12 },
  { n: "Bharat Precision", roce: 29, de: 0.3, g: 20 }, { n: "Coastal Power", roce: 8, de: 1.9, g: 3 },
  { n: "Zenith Chemicals", roce: 22, de: 0.1, g: 16 }, { n: "Grand Hotels Ltd", roce: 12, de: 1.1, g: 7 },
];
const PASS = STOCKS.map((s) => s.roce > 20 && s.de < 0.3); // the query, actually computed

const ScreenerScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur); const frame = useCurrentFrame();
  const typed = p(0.10, 0.30);                       // query typing
  const run = p(0.34, 0.38);                         // filter fires
  const nPass = PASS.filter(Boolean).length;
  const hot = Math.floor(frame / 30) % nPass;        // chase over the survivors
  let hi = -1, seen = -1;
  PASS.forEach((ok, i) => { if (ok) { seen += 1; if (seen === hot) hi = i; } });
  return (
    <Stage>
      <Bg theme={T} accent={G} />
      <Head theme={T} kicker="SCREENER.IN — LIVE DEMO" title="One Query, Five Thousand Stocks Filtered" color={G} />
      <Browser url="screener.in/screens/new" color={G} o={p(0.02, 0.1)}>
        {/* query box */}
        <div style={{ position: "absolute", left: 40, top: 26, width: 900, height: 92, borderRadius: 14,
          background: mix(T.bg0, G, 0.05), border: `2px solid ${mix(T.line, G, run > 0 ? 0.9 : 0.5)}`, padding: "14px 20px" }}>
          <Type mono text={"ROCE > 20 AND Debt to equity < 0.3"} p={typed} size={30} color={G} />
        </div>
        <div style={{ position: "absolute", left: 970, top: 26, width: 190, height: 92, borderRadius: 14,
          background: run > 0 ? G : mix(T.panel, G, 0.2), border: `2px solid ${G}`,
          display: "flex", alignItems: "center", justifyContent: "center",
          fontFamily: MONO, fontWeight: 800, fontSize: 27, color: run > 0 ? T.bg0 : G,
          transform: `scale(${1 + (run > 0 && run < 1 ? 0.08 : 0)})` }}>RUN ▶</div>
        {/* matches counter */}
        <div style={{ position: "absolute", left: 1195, top: 34, width: 240, textAlign: "center", opacity: p(0.36, 0.44) }}>
          <Counter p={p(0.36, 0.52)} to={23} color={G} size={54} suffix="" />
          <div style={{ fontFamily: MONO, fontSize: 20, color: T.muted, marginTop: 2 }}>matches of 5,000</div>
        </div>
        {/* results table — failing rows dim & strike as the filter runs */}
        {STOCKS.map((s, i) => {
          const at = 0.12 + i * 0.016;
          const killed = !PASS[i] && run > 0;
          const rowO = p(at, at + 0.05);
          const y = 140 + i * 46;
          return (
            <div key={i} style={{ position: "absolute", left: 40, top: y, width: 1420, height: 40,
              display: "flex", alignItems: "center", gap: 0, opacity: rowO * (killed ? interpolate(run, [0, 1], [1, 0.22]) : 1),
              background: hi === i && p(0.55, 0.56) > 0.5 ? mix(T.panel, G, 0.16) : i % 2 ? mix(T.bg1, G, 0.02) : "transparent",
              borderRadius: 8, border: hi === i && p(0.55, 0.56) > 0.5 ? `1.5px solid ${mix(T.line, G, 0.7)}` : `1.5px solid transparent` }}>
              <span style={{ fontFamily: SANS, fontWeight: 700, fontSize: 24, color: killed ? T.muted : T.text, width: 420, paddingLeft: 16,
                textDecoration: killed && run > 0.6 ? "line-through" : "none" }}>{s.n}</span>
              <span style={{ fontFamily: MONO, fontSize: 23, color: s.roce > 20 ? G : R, width: 300 }}>ROCE {s.roce}%</span>
              <span style={{ fontFamily: MONO, fontSize: 23, color: s.de < 0.3 ? G : R, width: 300 }}>D/E {s.de.toFixed(1)}</span>
              <span style={{ fontFamily: MONO, fontSize: 23, color: killed ? T.muted : mix(T.muted, G, 0.6), width: 260 }}>5-yr growth {s.g}%</span>
              <span style={{ fontFamily: MONO, fontWeight: 800, fontSize: 21, color: PASS[i] ? T.bg0 : "transparent",
                background: PASS[i] && run > 0.8 ? G : "transparent", borderRadius: 6, padding: "2px 10px" }}>PASS</span>
            </div>
          );
        })}
      </Browser>
      <Foot theme={T} p={p(0.84, 0.92)}>Free plan covers this · Premium ₹4,999/yr (as of Jul 2026) adds alerts & exports</Foot>
    </Stage>
  );
};

// ================================================================ 2. MODERN SCREENERS TRIO — DVM donuts · MMI gauge · mobile scans
const Donut: React.FC<{ cx: number; cy: number; rr: number; val: number; p: number; color: string; label: string }> =
({ cx, cy, rr, val, p, color, label }) => {
  const sweep = p * (val / 100) * Math.PI * 2;
  const pts = Array.from({ length: 40 }, (_, i) => {
    const a = -Math.PI / 2 + (i / 39) * sweep;
    return `${cx + Math.cos(a) * rr},${cy + Math.sin(a) * rr}`;
  });
  return (
    <>
      <svg style={{ position: "absolute", left: 0, top: 0, overflow: "visible" }} width={1920} height={1080}>
        <circle cx={cx} cy={cy} r={rr} fill="none" stroke={mix(T.line, color, 0.25)} strokeWidth={12} />
        {p > 0.02 && <polyline points={pts.join(" ")} fill="none" stroke={color} strokeWidth={12} strokeLinecap="round" />}
      </svg>
      <div style={{ position: "absolute", left: cx - 70, top: cy - 34, width: 140, textAlign: "center" }}>
        <Counter p={p} to={val} color={color} size={44} />
        <div style={{ fontFamily: MONO, fontSize: 20, color: T.muted, marginTop: 0 }}>{label}</div>
      </div>
    </>
  );
};

const TrioScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur); const frame = useCurrentFrame();
  const needle = interpolate(p(0.42, 0.62), [0, 1], [-80, 34]); // MMI → 62 "greed" zone
  const scanRows = ["⚡ 52-week high break", "📈 Volume 3× average", "🏦 FII holding up 2 qtrs", "🎯 Sector momentum #1"];
  return (
    <Stage>
      <Bg theme={T} accent={G} />
      <Head theme={T} kicker="TRENDLYNE · TICKERTAPE · STOCKEDGE" title="Scores, Sentiment & Scans at a Glance" color={G} />
      {/* Trendlyne DVM donuts */}
      <div style={{ position: "absolute", left: 130, top: 230, width: 540, height: 620, borderRadius: 20,
        background: mix(T.bg1, G, 0.04), border: `2.5px solid ${mix(T.line, G, 0.5)}`, opacity: p(0.04, 0.12) }}>
        <div style={{ fontFamily: MONO, fontWeight: 800, fontSize: 24, color: G, letterSpacing: 2, padding: "22px 0 0 28px" }}>TRENDLYNE · DVM SCORE</div>
        <div style={{ fontFamily: SANS, fontSize: 23, color: T.muted, padding: "6px 28px" }}>One number each for quality, price & trend</div>
      </div>
      <Donut cx={268} cy={470} rr={78} val={72} p={p(0.10, 0.24)} color={G} label="Durability" />
      <Donut cx={468} cy={470} rr={78} val={58} p={p(0.16, 0.30)} color={Y} label="Value" />
      <Donut cx={368} cy={690} rr={78} val={81} p={p(0.22, 0.36)} color={C} label="Momentum" />
      {/* Tickertape MMI gauge */}
      <div style={{ position: "absolute", left: 700, top: 230, width: 540, height: 620, borderRadius: 20,
        background: mix(T.bg1, C, 0.04), border: `2.5px solid ${mix(T.line, C, 0.5)}`, opacity: p(0.30, 0.38) }}>
        <div style={{ fontFamily: MONO, fontWeight: 800, fontSize: 24, color: C, letterSpacing: 2, padding: "22px 0 0 28px" }}>TICKERTAPE · MOOD INDEX</div>
        <div style={{ fontFamily: SANS, fontSize: 23, color: T.muted, padding: "6px 28px" }}>Is the MARKET fearful or greedy?</div>
      </div>
      <svg style={{ position: "absolute", left: 0, top: 0, overflow: "visible" }} width={1920} height={1080}>
        {Array.from({ length: 36 }, (_, i) => {
          const a = Math.PI + (i / 35) * Math.PI;
          const zone = i < 12 ? G : i < 24 ? Y : R;
          return <line key={i} x1={970 + Math.cos(a) * 150} y1={620 + Math.sin(a) * 150}
            x2={970 + Math.cos(a) * 178} y2={620 + Math.sin(a) * 178}
            stroke={mix(zone, T.bg0, 0.15)} strokeWidth={7} opacity={p(0.34, 0.46)} strokeLinecap="round" />;
        })}
        <line x1={970} y1={620} x2={970 + Math.cos(((needle - 90) * Math.PI) / 180) * 132}
          y2={620 + Math.sin(((needle - 90) * Math.PI) / 180) * 132}
          stroke={T.text} strokeWidth={6} strokeLinecap="round" opacity={p(0.4, 0.48)} />
        <circle cx={970} cy={620} r={14} fill={C} opacity={p(0.4, 0.48)} />
      </svg>
      <div style={{ position: "absolute", left: 850, top: 668, width: 240, textAlign: "center", opacity: p(0.5, 0.6) }}>
        <Counter p={p(0.5, 0.64)} to={62} color={Y} size={50} />
        <div style={{ fontFamily: MONO, fontWeight: 700, fontSize: 22, color: Y }}>GREED ZONE</div>
        <div style={{ fontFamily: SANS, fontSize: 21, color: T.muted, marginTop: 6 }}>fear 0 ←→ 100 greed</div>
      </div>
      {/* StockEdge phone */}
      <div style={{ position: "absolute", left: 1290, top: 230, width: 500, height: 620, borderRadius: 20,
        background: mix(T.bg1, V, 0.04), border: `2.5px solid ${mix(T.line, V, 0.5)}`, opacity: p(0.56, 0.64) }}>
        <div style={{ fontFamily: MONO, fontWeight: 800, fontSize: 24, color: V, letterSpacing: 2, padding: "22px 0 0 28px" }}>STOCKEDGE · DAILY SCANS</div>
        <div style={{ position: "absolute", left: 120, top: 90, width: 260, height: 490, borderRadius: 30,
          background: T.bg0, border: `3px solid ${mix(T.line, V, 0.7)}` }}>
          <div style={{ width: 90, height: 8, borderRadius: 5, background: mix(T.line, V, 0.5), margin: "12px auto" }} />
          {scanRows.map((s2, i) => {
            const at = 0.62 + i * 0.05;
            const glow = Math.floor(frame / 24) % scanRows.length === i;
            return (
              <div key={i} style={{ margin: "12px 14px", padding: "12px 12px", borderRadius: 12,
                background: mix(T.panel, V, glow ? 0.22 : 0.08), border: `1.5px solid ${mix(T.line, V, glow ? 0.9 : 0.4)}`,
                fontFamily: SANS, fontWeight: 600, fontSize: 19.5, color: T.text, opacity: p(at, at + 0.05) }}>{s2}</div>
            );
          })}
        </div>
      </div>
      <Foot theme={T} p={p(0.86, 0.94)}>Trendlyne from ~₹119/mo · Tickertape from ~₹249/mo (as of Jul 2026 — check sites)</Foot>
    </Stage>
  );
};

// ================================================================ 3. TRADINGVIEW — computed candles + SMA + RSI + crosshair
const CANDLES = (() => {
  let px = 400; const out: { o: number; c: number; h: number; l: number }[] = [];
  for (let i = 0; i < 34; i++) {
    const drift = Math.sin(i * 0.34) * 5 + 1.4 + (rnd(i, 3, 7) - 0.5) * 16;
    const o = px, c2 = px + drift;
    out.push({ o, c: c2, h: Math.max(o, c2) + rnd(i, 4, 7) * 7, l: Math.min(o, c2) - rnd(i, 5, 7) * 7 });
    px = c2;
  }
  return out;
})();
const SMA = CANDLES.map((_, i) => {
  const w = CANDLES.slice(Math.max(0, i - 7), i + 1);
  return w.reduce((a, k) => a + k.c, 0) / w.length;
});
const RSI = CANDLES.map((_, i) => {
  const w = CANDLES.slice(Math.max(0, i - 7), i + 1);
  let up = 0, dn = 0;
  w.forEach((k) => { const d = k.c - k.o; if (d > 0) up += d; else dn -= d; });
  return dn === 0 ? 88 : 100 - 100 / (1 + up / dn);
});
const PMIN = Math.min(...CANDLES.map((k) => k.l)), PMAX = Math.max(...CANDLES.map((k) => k.h));
const py = (v: number) => 30 + ((PMAX - v) / (PMAX - PMIN)) * 330;

const TVScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur); const frame = useCurrentFrame();
  const nC = Math.round(interpolate(p(0.08, 0.42), [0, 1], [0, CANDLES.length]));
  const nS = Math.round(interpolate(p(0.42, 0.58), [0, 1], [0, CANDLES.length]));
  const nR = Math.round(interpolate(p(0.62, 0.78), [0, 1], [0, CANDLES.length]));
  const cross = 120 + ((frame * 2.2) % 1200);
  const X = (i: number) => 60 + i * 41;
  return (
    <Stage>
      <Bg theme={T} accent={C} />
      <Head theme={T} kicker="TRADINGVIEW — LIVE DEMO" title="The Chart Draws, The Story Appears" color={C} />
      <Browser url="tradingview.com/chart · NIFTY · 1D" color={C} o={p(0.02, 0.08)}>
        {/* toolbar */}
        <div style={{ position: "absolute", left: 0, top: 0, bottom: 0, width: 52, borderRight: `1.5px solid ${mix(T.line, C, 0.4)}`,
          display: "flex", flexDirection: "column", alignItems: "center", gap: 18, paddingTop: 18, opacity: p(0.04, 0.1) }}>
          {["✏️", "📏", "🎯", "🧲", "🔤"].map((e, i) => (
            <span key={i} style={{ fontSize: 22, opacity: Math.floor(frame / 26) % 5 === i ? 1 : 0.45 }}>{e}</span>
          ))}
        </div>
        {/* candles */}
        {CANDLES.slice(0, nC).map((k, i) => {
          const up = k.c >= k.o;
          return (
            <React.Fragment key={i}>
              <div style={{ position: "absolute", left: X(i) + 12, top: py(k.h), width: 3, height: py(k.l) - py(k.h),
                background: up ? G : R, opacity: 0.85 }} />
              <div style={{ position: "absolute", left: X(i) + 3, top: py(Math.max(k.o, k.c)), width: 21,
                height: Math.max(4, Math.abs(py(k.o) - py(k.c))), borderRadius: 3,
                background: up ? G : R, boxShadow: i === nC - 1 ? `0 0 14px ${up ? G : R}` : "none" }} />
            </React.Fragment>
          );
        })}
        {/* SMA-8 overlay */}
        <svg style={{ position: "absolute", left: 0, top: 0, overflow: "visible" }} width={1500} height={640}>
          {nS > 2 && <polyline points={SMA.slice(0, nS).map((v, i) => `${X(i) + 13},${py(v)}`).join(" ")}
            fill="none" stroke={Y} strokeWidth={4} strokeLinecap="round" opacity={0.95} />}
          {/* trendline snapping on */}
          {p(0.5, 0.6) > 0 && <line x1={X(6)} y1={py(CANDLES[6].l) + 10} x2={X(6) + (X(30) - X(6)) * p(0.5, 0.6)}
            y2={py(CANDLES[6].l) + 10 - (py(CANDLES[6].l) - py(CANDLES[30].l) - 4) * p(0.5, 0.6)}
            stroke={C} strokeWidth={3.5} strokeDasharray="10 8" opacity={0.9} />}
          {/* crosshair */}
          {cross < 1440 && <line x1={cross} y1={0} x2={cross} y2={420} stroke={mix(T.muted, C, 0.4)} strokeWidth={1.5} strokeDasharray="5 7" opacity={0.6} />}
        </svg>
        <div style={{ position: "absolute", left: 1200, top: 30, fontFamily: MONO, fontSize: 21, color: Y, opacity: p(0.46, 0.54) }}>— SMA 8 · trend filter</div>
        <div style={{ position: "absolute", left: 1200, top: 64, fontFamily: MONO, fontSize: 21, color: C, opacity: p(0.56, 0.64) }}>-- trendline · support</div>
        {/* RSI pane */}
        <div style={{ position: "absolute", left: 52, top: 428, width: 1448, height: 198, borderTop: `2px solid ${mix(T.line, C, 0.5)}`,
          background: mix(T.bg0, C, 0.03), opacity: p(0.6, 0.68) }}>
          <div style={{ fontFamily: MONO, fontSize: 20, color: V, padding: "8px 0 0 16px" }}>RSI (8) — overbought ›70 · oversold ‹30</div>
          <svg style={{ position: "absolute", left: 0, top: 0 }} width={1448} height={198}>
            <line x1={10} y1={62} x2={1400} y2={62} stroke={mix(T.line, R, 0.5)} strokeWidth={1.5} strokeDasharray="6 8" />
            <line x1={10} y1={150} x2={1400} y2={150} stroke={mix(T.line, G, 0.5)} strokeWidth={1.5} strokeDasharray="6 8" />
            {nR > 2 && <polyline points={RSI.slice(0, nR).map((v, i) => `${8 + i * 41},${170 - (v / 100) * 130}`).join(" ")}
              fill="none" stroke={V} strokeWidth={3.5} strokeLinecap="round" />}
          </svg>
        </div>
      </Browser>
      <Foot theme={T} p={p(0.84, 0.92)}>Free tier is fully usable — learn charts before paying anyone for "special indicators"</Foot>
    </Stage>
  );
};

// ================================================================ 4. CHARTINK — scan conditions + populating results
const SCAN_HITS = [
  { n: "Bharat Precision", pct: 3.2 }, { n: "Kaveri Pharma", pct: 2.7 },
  { n: "Zenith Chemicals", pct: 2.1 }, { n: "Astra Polymers", pct: 1.8 }, { n: "Suvarna Foods", pct: 1.4 },
];
const ChartinkScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur); const frame = useCurrentFrame();
  const run = p(0.4, 0.44);
  return (
    <Stage>
      <Bg theme={T} accent={C} />
      <Head theme={T} kicker="CHARTINK — LIVE DEMO" title="Build a Scan From Dropdowns, No Code" color={C} />
      <Browser url="chartink.com/screener" color={C} o={p(0.02, 0.09)}>
        {/* condition rows */}
        {[
          { txt: "Latest RSI(14)  crossed above  60", at: 0.10 },
          { txt: "Latest Close  greater than  SMA(Close, 200)", at: 0.20 },
          { txt: "Latest Volume  greater than  2 × Avg Volume(20)", at: 0.30 },
        ].map((cnd, i) => (
          <div key={i} style={{ position: "absolute", left: 40, top: 28 + i * 74, width: 950, height: 60, borderRadius: 12,
            background: mix(T.bg0, C, 0.05), border: `2px solid ${mix(T.line, C, 0.55)}`,
            display: "flex", alignItems: "center", gap: 14, padding: "0 20px", opacity: p(cnd.at, cnd.at + 0.07),
            transform: `translateX(${(1 - p(cnd.at, cnd.at + 0.07)) * -30}px)` }}>
            <span style={{ fontFamily: MONO, fontWeight: 800, fontSize: 21, color: T.bg0, background: C, borderRadius: 6, padding: "2px 10px" }}>{i + 1}</span>
            <span style={{ fontFamily: MONO, fontSize: 24, color: T.text }}>{cnd.txt}</span>
            <span style={{ marginLeft: "auto", fontFamily: MONO, fontSize: 20, color: T.muted }}>▾</span>
          </div>
        ))}
        <div style={{ position: "absolute", left: 1020, top: 100, width: 220, height: 64, borderRadius: 14,
          background: run > 0 ? C : mix(T.panel, C, 0.2), border: `2.5px solid ${C}`,
          display: "flex", alignItems: "center", justifyContent: "center", fontFamily: MONO, fontWeight: 800,
          fontSize: 26, color: run > 0 ? T.bg0 : C, opacity: p(0.32, 0.4),
          boxShadow: run > 0 ? `0 0 26px ${mix(T.bg0, C, 0.7)}` : "none" }}>RUN SCAN</div>
        {/* results populate */}
        <div style={{ position: "absolute", left: 40, top: 268, width: 1420, borderTop: `2px solid ${mix(T.line, C, 0.5)}`, opacity: p(0.42, 0.5) }}>
          <div style={{ fontFamily: MONO, fontSize: 21, color: T.muted, padding: "10px 4px" }}>
            SCAN RESULTS — <span style={{ color: C, fontWeight: 800 }}>{Math.round(interpolate(p(0.44, 0.6), [0, 1], [0, 5]))} stocks</span> pass all 3 conditions
          </div>
          {SCAN_HITS.map((h2, i) => {
            const at = 0.46 + i * 0.07;
            const hot = Math.floor(frame / 28) % SCAN_HITS.length === i && p(0.8, 0.81) > 0.5;
            return (
              <div key={i} style={{ display: "flex", alignItems: "center", height: 54, borderRadius: 10, margin: "4px 0",
                background: hot ? mix(T.panel, C, 0.16) : i % 2 ? mix(T.bg1, C, 0.03) : "transparent",
                opacity: p(at, at + 0.06), transform: `translateY(${(1 - p(at, at + 0.06)) * 14}px)` }}>
                <span style={{ fontFamily: SANS, fontWeight: 700, fontSize: 25, color: T.text, width: 520, paddingLeft: 16 }}>{h2.n}</span>
                <div style={{ width: 340, height: 20, borderRadius: 999, background: mix(T.bg0, C, 0.08), overflow: "hidden" }}>
                  <div style={{ width: `${(h2.pct / 3.5) * 100 * p(at + 0.02, at + 0.1)}%`, height: "100%",
                    background: `linear-gradient(90deg, ${mix(C, T.bg0, 0.3)}, ${C})` }} />
                </div>
                <span style={{ fontFamily: MONO, fontWeight: 800, fontSize: 24, color: G, marginLeft: 22 }}>+{h2.pct}%</span>
                <span style={{ marginLeft: "auto", fontFamily: MONO, fontSize: 20, color: T.muted, paddingRight: 18 }}>today</span>
              </div>
            );
          })}
        </div>
      </Browser>
      <Foot theme={T} p={p(0.86, 0.94)}>Core screener free for a decade — thousands of community scans to copy</Foot>
    </Stage>
  );
};

// ================================================================ 5. SENSIBULL — real bull-call-spread payoff math
const LEGS = [{ k: 23800, prem: 150, sign: +1 }, { k: 24000, prem: -60, sign: -1 }]; // buy CE / sell CE
const payoff = (s: number) => LEGS.reduce((a, l) => a + l.sign * Math.max(0, s - l.k) - l.prem, 0) * 1; // net premium folded in prem signs
const NET = LEGS.reduce((a, l) => a + l.prem, 0);          // 90 debit
const MAXP = 24000 - 23800 - NET, MAXL = NET, BE = 23800 + NET;
const SGRID = Array.from({ length: 81 }, (_, i) => 23500 + i * 10);
const PAYS = SGRID.map((s) => LEGS.reduce((a, l) => a + l.sign * Math.max(0, s - l.k), 0) - NET);

const SensibullScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur); const frame = useCurrentFrame();
  const gx = (s: number) => 90 + ((s - 23500) / 800) * 1290;
  const gy = (v: number) => 330 - (v / 130) * 150;
  const nPts = Math.round(interpolate(p(0.42, 0.62), [0, 1], [0, SGRID.length]));
  const pop = usePop(dur);
  return (
    <Stage>
      <Bg theme={T} accent={V} />
      <Head theme={T} kicker="SENSIBULL — LIVE DEMO" title="See the Payoff BEFORE You Trade" color={V} />
      <Browser url="web.sensibull.com/strategy-builder" color={V} o={p(0.02, 0.08)}>
        {/* view chips */}
        <div style={{ position: "absolute", left: 40, top: 22, display: "flex", gap: 16, opacity: p(0.06, 0.14) }}>
          {["📈 Bullish", "📉 Bearish", "↔️ Sideways"].map((v2, i) => {
            const sel = i === 0 && p(0.14, 0.18) > 0.5;
            return <div key={i} style={{ fontFamily: MONO, fontWeight: 700, fontSize: 23, borderRadius: 999, padding: "10px 26px",
              color: sel ? T.bg0 : mix(T.muted, V, 0.4), background: sel ? V : mix(T.panel, V, 0.1),
              border: `2px solid ${sel ? V : mix(T.line, V, 0.45)}`,
              boxShadow: sel ? `0 0 22px ${mix(T.bg0, V, 0.7)}` : "none" }}>{v2}</div>;
          })}
          <div style={{ fontFamily: SANS, fontSize: 23, color: T.muted, alignSelf: "center", marginLeft: 10, opacity: p(0.18, 0.24) }}>→ suggests: <b style={{ color: V }}>Bull Call Spread</b></div>
        </div>
        {/* legs */}
        {LEGS.map((l, i) => {
          const at = 0.2 + i * 0.09;
          return (
            <div key={i} style={{ position: "absolute", left: 40 + i * 480, top: 88, width: 450, height: 62, borderRadius: 12,
              background: mix(T.bg0, l.sign > 0 ? G : R, 0.06), border: `2px solid ${mix(T.line, l.sign > 0 ? G : R, 0.7)}`,
              display: "flex", alignItems: "center", gap: 14, padding: "0 18px", opacity: p(at, at + 0.07) }}>
              <span style={{ fontFamily: MONO, fontWeight: 800, fontSize: 21, color: T.bg0, borderRadius: 6, padding: "3px 10px",
                background: l.sign > 0 ? G : R }}>{l.sign > 0 ? "BUY" : "SELL"}</span>
              <span style={{ fontFamily: MONO, fontSize: 24, color: T.text }}>{l.k} CE</span>
              <span style={{ marginLeft: "auto", fontFamily: MONO, fontSize: 23, color: l.sign > 0 ? R : G }}>
                {l.sign > 0 ? `− ₹${l.prem}` : `+ ₹${-l.prem}`}</span>
            </div>
          );
        })}
        <div style={{ position: "absolute", left: 1010, top: 96, fontFamily: MONO, fontSize: 22, color: T.muted, opacity: p(0.34, 0.4) }}>
          net cost: <span style={{ color: Y, fontWeight: 800 }}>₹{NET}</span>
        </div>
        {/* payoff graph */}
        <svg style={{ position: "absolute", left: 0, top: 0, overflow: "visible" }} width={1500} height={640}>
          {/* profit / loss fill regions */}
          {nPts > 2 && (
            <polygon points={`${gx(SGRID[0])},${gy(0)} ` + PAYS.slice(0, nPts).map((v, i) => `${gx(SGRID[i])},${gy(v)}`).join(" ") + ` ${gx(SGRID[nPts - 1])},${gy(0)}`}
              fill={mix(T.bg0, G, 0.18)} opacity={0.5} />
          )}
          <line x1={80} y1={gy(0)} x2={1420} y2={gy(0)} stroke={mix(T.line, V, 0.6)} strokeWidth={2} opacity={p(0.38, 0.44)} />
          {[23600, 23800, 24000, 24200].map((s3) => (
            <text key={s3} x={gx(s3) - 30} y={gy(0) + 30} fill={T.muted} fontFamily={MONO} fontSize={20} opacity={p(0.38, 0.44)}>{s3}</text>
          ))}
          {nPts > 2 && <polyline points={PAYS.slice(0, nPts).map((v, i) => `${gx(SGRID[i])},${gy(v)}`).join(" ")}
            fill="none" stroke={V} strokeWidth={5} strokeLinecap="round" />}
          {/* breakeven marker */}
          {p(0.66, 0.72) > 0 && <line x1={gx(BE)} y1={gy(-120)} x2={gx(BE)} y2={gy(120)} stroke={Y} strokeWidth={3}
            strokeDasharray="8 8" opacity={p(0.66, 0.72)} />}
        </svg>
        {/* labels with real numbers */}
        <div style={{ position: "absolute", left: 1080, top: 200, opacity: p(0.72, 0.8), transform: `scale(${pop(0.72)})` }}>
          <div style={{ fontFamily: MONO, fontSize: 22, color: G }}>MAX PROFIT</div>
          <Counter p={p(0.72, 0.82)} to={MAXP} prefix="+₹" color={G} size={46} />
        </div>
        <div style={{ position: "absolute", left: 120, top: 420, opacity: p(0.76, 0.84) }}>
          <div style={{ fontFamily: MONO, fontSize: 22, color: R }}>MAX LOSS</div>
          <Counter p={p(0.76, 0.86)} to={MAXL} prefix="−₹" color={R} size={46} />
        </div>
        <div style={{ position: "absolute", left: gx(BE) - 96, top: 152, fontFamily: MONO, fontSize: 22, color: Y, opacity: p(0.68, 0.76) }}>
          breakeven {BE}
        </div>
        <div style={{ position: "absolute", left: 40, top: 560, fontFamily: SANS, fontSize: 23, color: T.muted, opacity: p(0.8, 0.88) }}>
          Both risk numbers known <b style={{ color: T.text }}>before</b> the order —{" "}
          <span style={{ opacity: 0.6 + Math.sin(frame * 0.09) * 0.4, color: V }}>never trade an option you can't draw</span>
        </div>
      </Browser>
      <Foot theme={T} p={p(0.88, 0.95)}>Pro free for Zerodha users · paid on other brokers (as of Jul 2026 — check site)</Foot>
    </Stage>
  );
};

// ================================================================ 6. BACKTEST — rule → computed equity curve + honest drawdown
const TRADES = Array.from({ length: 60 }, (_, i) => (rnd(i, 11, 21) > 0.42 ? 2 : -1)); // +2R win / −1R loss
const EQUITY = TRADES.reduce<number[]>((acc, r2) => { acc.push((acc[acc.length - 1] || 0) + r2); return acc; }, []);
const PEAKS = EQUITY.map((_, i) => Math.max(...EQUITY.slice(0, i + 1)));
const DDI = EQUITY.reduce((worst, v, i) => (PEAKS[i] - v > PEAKS[worst] - EQUITY[worst] ? i : worst), 0);
const WINPCT = Math.round((TRADES.filter((t) => t > 0).length / TRADES.length) * 100);
const EMAX = Math.max(...EQUITY), EMIN = Math.min(...EQUITY, 0);

const BacktestScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur); const frame = useCurrentFrame();
  const ex = (i: number) => 60 + (i / (EQUITY.length - 1)) * 1380;
  const ey = (v: number) => 500 - ((v - EMIN) / (EMAX - EMIN)) * 330;
  const nPts = Math.round(interpolate(p(0.34, 0.66), [0, 1], [0, EQUITY.length]));
  return (
    <Stage>
      <Bg theme={T} accent={Y} />
      <Head theme={T} kicker="STREAK / ALGOTEST — LIVE DEMO" title="Ten Years of 'What If' in Ten Seconds" color={Y} />
      <Browser url="streak.tech/create · backtest" color={Y} o={p(0.02, 0.08)}>
        {/* rule, typed in plain English */}
        <div style={{ position: "absolute", left: 40, top: 24, width: 1180, height: 64, borderRadius: 12,
          background: mix(T.bg0, Y, 0.05), border: `2px solid ${mix(T.line, Y, 0.6)}`, padding: "14px 20px" }}>
          <Type mono text={"BUY when Close crosses above 20-day high · SL 1% · Target 2%"} p={p(0.08, 0.28)} size={26} color={Y} />
        </div>
        <div style={{ position: "absolute", left: 1250, top: 24, width: 210, height: 64, borderRadius: 12,
          background: p(0.3, 0.32) > 0 ? Y : mix(T.panel, Y, 0.2), border: `2.5px solid ${Y}`, display: "flex",
          alignItems: "center", justifyContent: "center", fontFamily: MONO, fontWeight: 800, fontSize: 24,
          color: p(0.3, 0.32) > 0 ? T.bg0 : Y, opacity: p(0.26, 0.32) }}>BACKTEST ⚡</div>
        {/* equity curve */}
        <svg style={{ position: "absolute", left: 0, top: 0, overflow: "visible" }} width={1500} height={640}>
          <line x1={50} y1={ey(0)} x2={1450} y2={ey(0)} stroke={mix(T.line, Y, 0.45)} strokeWidth={1.5} strokeDasharray="6 9" opacity={p(0.32, 0.38)} />
          {/* drawdown valley shading, revealed once curve passes it */}
          {nPts > DDI && (
            <rect x={ex(DDI - 7)} y={ey(PEAKS[DDI])} width={ex(DDI + 4) - ex(DDI - 7)} height={ey(EQUITY[DDI]) - ey(PEAKS[DDI])}
              fill={mix(T.bg0, R, 0.25)} opacity={0.55} rx={8} />
          )}
          {nPts > 2 && <polyline points={EQUITY.slice(0, nPts).map((v, i) => `${ex(i)},${ey(v)}`).join(" ")}
            fill="none" stroke={Y} strokeWidth={4.5} strokeLinecap="round" />}
          {nPts > 1 && <circle cx={ex(nPts - 1)} cy={ey(EQUITY[nPts - 1])} r={8} fill={Y}
            opacity={0.6 + Math.sin(frame * 0.2) * 0.4} />}
        </svg>
        {nPts > DDI && (
          <div style={{ position: "absolute", left: ex(DDI) - 120, top: ey(EQUITY[DDI]) + 14, fontFamily: MONO, fontSize: 21, color: R }}>
            the max drawdown · could YOU sit through this?
          </div>
        )}
        {/* stats strip */}
        <div style={{ position: "absolute", left: 40, top: 540, display: "flex", gap: 40, opacity: p(0.7, 0.78) }}>
          {[
            { l: "TRADES", v: TRADES.length, c: T.text, sfx: "" },
            { l: "WIN RATE", v: WINPCT, c: G, sfx: "%" },
            { l: "AVG WIN : LOSS", v: 2, c: C, sfx: " : 1" },
            { l: "NET RESULT", v: EQUITY[EQUITY.length - 1], c: Y, sfx: "R" },
          ].map((s4, i) => (
            <div key={i} style={{ textAlign: "center" }}>
              <div style={{ fontFamily: MONO, fontSize: 20, color: T.muted, marginBottom: 4 }}>{s4.l}</div>
              <Counter p={p(0.72 + i * 0.04, 0.82 + i * 0.04)} to={s4.v} suffix={s4.sfx} color={s4.c} size={42} />
            </div>
          ))}
        </div>
      </Browser>
      <Foot theme={T} p={p(0.88, 0.95)}>Streak (Zerodha) no-code · AlgoTest free F&O backtests · always include costs & slippage</Foot>
    </Stage>
  );
};

// ================================================================ 7. INFO WALL — 4 live mini-panels
const InfoWallScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur); const frame = useCurrentFrame();
  const heads = ["Q1 results: IT beats street estimates…", "RBI holds rates; stance neutral…", "FII flows turn positive in July…", "Crude eases; OMCs rally…"];
  const tick = (frame * 1.4) % (heads.length * 560);
  const subs = [{ l: "QIB", x: 2.8 }, { l: "NII", x: 4.2 }, { l: "RETAIL", x: 1.6 }];
  return (
    <Stage>
      <Bg theme={T} accent={G} />
      <Head theme={T} kicker="THE INFORMATION LAYER" title="Facts First: News · Funds · IPOs · Official" color={G} />
      {/* Moneycontrol ticker */}
      <div style={{ position: "absolute", left: 130, top: 226, width: 790, height: 300, borderRadius: 18, overflow: "hidden",
        background: mix(T.bg1, C, 0.04), border: `2.5px solid ${mix(T.line, C, 0.5)}`, opacity: p(0.04, 0.12) }}>
        <div style={{ fontFamily: MONO, fontWeight: 800, fontSize: 23, color: C, letterSpacing: 2, padding: "18px 24px 8px" }}>📰 MONEYCONTROL — the news pulse</div>
        {heads.map((h3, i) => (
          <div key={i} style={{ position: "absolute", left: 790 - ((tick + i * 560) % (heads.length * 560)) + 100, top: 90 + (i % 2) * 90,
            whiteSpace: "nowrap", fontFamily: SANS, fontWeight: 600, fontSize: 25, color: T.text,
            background: mix(T.panel, C, 0.1), border: `1.5px solid ${mix(T.line, C, 0.5)}`, borderRadius: 999, padding: "12px 26px" }}>{h3}</div>
        ))}
        <div style={{ position: "absolute", bottom: 14, left: 24, fontFamily: MONO, fontSize: 20, color: T.muted }}>news · results · portfolio tracker</div>
      </div>
      {/* Value Research stars */}
      <div style={{ position: "absolute", left: 1000, top: 226, width: 790, height: 300, borderRadius: 18,
        background: mix(T.bg1, G, 0.04), border: `2.5px solid ${mix(T.line, G, 0.5)}`, opacity: p(0.16, 0.24) }}>
        <div style={{ fontFamily: MONO, fontWeight: 800, fontSize: 23, color: G, letterSpacing: 2, padding: "18px 24px 8px" }}>🏦 VALUE RESEARCH — fund ratings</div>
        {[{ n: "Flexi Cap Fund A", s: 5 }, { n: "Midcap Fund B", s: 4 }].map((f2, i) => (
          <div key={i} style={{ display: "flex", alignItems: "center", gap: 18, padding: "14px 26px" }}>
            <span style={{ fontFamily: SANS, fontWeight: 700, fontSize: 25, color: T.text, width: 300 }}>{f2.n}</span>
            {Array.from({ length: 5 }, (_, si) => (
              <span key={si} style={{ fontSize: 30, opacity: p(0.2 + i * 0.08 + si * 0.025, 0.24 + i * 0.08 + si * 0.025),
                filter: "none", color: si < f2.s ? Y : T.line }}>{si < f2.s ? "★" : "☆"}</span>
            ))}
          </div>
        ))}
        <div style={{ position: "absolute", bottom: 14, left: 24, fontFamily: MONO, fontSize: 20, color: T.muted }}>independent MF ratings · portfolio X-ray</div>
      </div>
      {/* Chittorgarh IPO subscriptions */}
      <div style={{ position: "absolute", left: 130, top: 556, width: 790, height: 300, borderRadius: 18,
        background: mix(T.bg1, V, 0.04), border: `2.5px solid ${mix(T.line, V, 0.5)}`, opacity: p(0.34, 0.42) }}>
        <div style={{ fontFamily: MONO, fontWeight: 800, fontSize: 23, color: V, letterSpacing: 2, padding: "18px 24px 10px" }}>📋 CHITTORGARH — IPO subscriptions (sample)</div>
        {subs.map((s5, i) => (
          <div key={i} style={{ display: "flex", alignItems: "center", gap: 16, padding: "8px 26px" }}>
            <span style={{ fontFamily: MONO, fontSize: 22, color: T.muted, width: 110 }}>{s5.l}</span>
            <div style={{ width: 470, height: 24, borderRadius: 999, background: mix(T.bg0, V, 0.08), overflow: "hidden" }}>
              <div style={{ width: `${(s5.x / 5) * 100 * p(0.4 + i * 0.06, 0.52 + i * 0.06)}%`, height: "100%",
                background: `linear-gradient(90deg, ${mix(V, T.bg0, 0.35)}, ${V})` }} />
            </div>
            <Counter p={p(0.4 + i * 0.06, 0.52 + i * 0.06)} to={s5.x} suffix="×" decimals={1} color={V} size={28} />
          </div>
        ))}
        <div style={{ position: "absolute", bottom: 12, left: 24, fontFamily: MONO, fontSize: 20, color: R }}>⚠ GMP there = UNOFFICIAL grey-market data</div>
      </div>
      {/* NSE official */}
      <div style={{ position: "absolute", left: 1000, top: 556, width: 790, height: 300, borderRadius: 18,
        background: mix(T.bg1, G, 0.05), border: `2.5px solid ${mix(T.line, G, 0.6)}`, opacity: p(0.52, 0.6) }}>
        <div style={{ fontFamily: MONO, fontWeight: 800, fontSize: 23, color: G, letterSpacing: 2, padding: "18px 24px 8px" }}>🏛️ NSE / BSE — the official source</div>
        {["Corporate announcements", "FII/DII provisional (same evening)", "Circulars: lot sizes · margins · expiry"].map((r3, i) => (
          <div key={i} style={{ display: "flex", gap: 14, alignItems: "center", padding: "9px 26px", opacity: p(0.58 + i * 0.05, 0.64 + i * 0.05) }}>
            <span style={{ color: G, fontSize: 22 }}>✓</span>
            <span style={{ fontFamily: SANS, fontSize: 25, color: T.text }}>{r3}</span>
          </div>
        ))}
        <div style={{ position: "absolute", bottom: 14, left: 24, fontFamily: MONO, fontWeight: 700, fontSize: 21,
          color: G, opacity: 0.6 + Math.sin(frame * 0.07) * 0.4 }}>when two sites disagree — the exchange wins</div>
      </div>
      <Foot theme={T} p={p(0.86, 0.94)}>Bookmark all four — opinions are optional, facts are not</Foot>
    </Stage>
  );
};

// ================================================================ 8. SMALLCASE — tiles fly into a basket → your demat
const HOLD = [
  { n: "INFY", w: 22, e: "💻" }, { n: "HDFCBANK", w: 24, e: "🏦" }, { n: "TITAN", w: 18, e: "⌚" },
  { n: "LT", w: 20, e: "🏗️" }, { n: "SUNPHARMA", w: 16, e: "💊" },
];
const SmallcaseScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur); const frame = useCurrentFrame();
  return (
    <Stage>
      <Bg theme={T} accent={G} />
      <Head theme={T} kicker="SMALLCASE" title="A Basket You Own, Stock by Stock" color={G} />
      {/* basket */}
      <div style={{ position: "absolute", left: 620, top: 300, width: 680, height: 420, borderRadius: "26px 26px 110px 110px",
        background: mix(T.bg1, G, 0.05), border: `3px solid ${mix(T.line, G, 0.7)}`, opacity: p(0.04, 0.12),
        boxShadow: `0 0 ${30 + Math.sin(frame * 0.06) * 12}px ${mix(T.bg0, G, 0.4)}` }}>
        <div style={{ textAlign: "center", fontFamily: MONO, fontWeight: 800, fontSize: 24, color: G, letterSpacing: 3, marginTop: 18 }}>
          🧺 QUALITY-5 SMALLCASE (SAMPLE)
        </div>
      </div>
      {/* tiles fly in from top, land in 2 rows inside the basket */}
      {HOLD.map((h4, i) => {
        const at = 0.14 + i * 0.09;
        const t2 = p(at, at + 0.1);
        const tx = 660 + (i % 3) * 210, ty = i < 3 ? 396 : 520;
        const sx = 240 + i * 340, sy = 180;
        return (
          <div key={i} style={{ position: "absolute", left: sx + (tx - sx) * t2, top: sy + (ty - sy) * t2,
            width: 190, height: 104, borderRadius: 16, background: mix(T.panel, G, 0.1),
            border: `2.5px solid ${mix(T.line, G, 0.8)}`, opacity: Math.max(0.001, p(at - 0.02, at)),
            display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center",
            transform: `rotate(${(1 - t2) * (i % 2 ? 10 : -10)}deg)` }}>
            <div style={{ fontSize: 26 }}>{h4.e} <span style={{ fontFamily: MONO, fontWeight: 800, fontSize: 23, color: T.text }}>{h4.n}</span></div>
            <Counter p={p(at + 0.06, at + 0.14)} to={h4.w} suffix="%" color={G} size={27} />
          </div>
        );
      })}
      {/* weights total + demat */}
      <div style={{ position: "absolute", left: 220, top: 420, width: 300, textAlign: "center", opacity: p(0.62, 0.7) }}>
        <div style={{ fontFamily: MONO, fontSize: 22, color: T.muted }}>WEIGHTS TOTAL</div>
        <Counter p={p(0.62, 0.74)} to={100} suffix="%" color={G} size={56} />
        <div style={{ fontFamily: SANS, fontSize: 23, color: T.muted, marginTop: 6 }}>rebalanced periodically by a SEBI-registered manager</div>
      </div>
      <Wire x1={1300} y1={520} x2={1560} y2={520} p={p(0.7, 0.78)} color={G} w={3.5} />
      <Flow x1={1300} y1={520} x2={1560} y2={520} color={G} n={6} o={p(0.76, 0.8)} />
      <div style={{ position: "absolute", left: 1560, top: 440, width: 250, height: 160, borderRadius: 18,
        background: mix(T.panel, G, 0.1), border: `2.5px solid ${G}`, textAlign: "center", opacity: p(0.72, 0.8) }}>
        <div style={{ fontSize: 44, marginTop: 18 }}>🔐</div>
        <div style={{ fontFamily: MONO, fontWeight: 800, fontSize: 23, color: G }}>YOUR DEMAT</div>
        <div style={{ fontFamily: SANS, fontSize: 21, color: T.muted }}>you own the stocks</div>
      </div>
      <Foot theme={T} p={p(0.86, 0.94)}>Free & fee-based smallcases exist — structure yes, understanding still required</Foot>
    </Stage>
  );
};

// ================================================================ 9. LEARN — Varsity bookshelf + red-flag panel
const MODS = [
  { n: "Intro to Markets", c: G }, { n: "Technical Analysis", c: C }, { n: "Fundamental Analysis", c: G },
  { n: "Futures", c: V }, { n: "Options Theory", c: V }, { n: "Taxation", c: Y },
];
const LearnScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur); const frame = useCurrentFrame();
  return (
    <Stage>
      <Bg theme={T} accent={R} />
      <Head theme={T} kicker="LEARNING — THE LAYER UNDER EVERYTHING" title="Varsity: a Free Degree in Markets" color={R} />
      {/* shelf */}
      <div style={{ position: "absolute", left: 130, top: 700, width: 1000, height: 10, borderRadius: 6, background: mix(T.line, R, 0.5), opacity: p(0.05, 0.12) }} />
      {MODS.map((m, i) => {
        const at = 0.08 + i * 0.07;
        const o = p(at, at + 0.08);
        const prog = p(at + 0.28, at + 0.5);
        const hot = Math.floor(frame / 30) % MODS.length === i;
        return (
          <div key={i} style={{ position: "absolute", left: 150 + i * 160, top: 700 - 320 * o, width: 140, height: 320 * o,
            borderRadius: "10px 10px 0 0", background: `linear-gradient(180deg, ${mix(T.panel, m.c, hot ? 0.3 : 0.16)}, ${mix(T.bg1, m.c, 0.06)})`,
            border: `2.5px solid ${mix(T.line, m.c, hot ? 1 : 0.6)}`, overflow: "hidden" }}>
            <div style={{ position: "absolute", left: 0, right: 0, bottom: 0, height: `${prog * 100}%`,
              background: mix(T.bg0, m.c, 0.25), borderTop: `2px solid ${m.c}` }} />
            <div style={{ position: "absolute", left: 8, top: 14, width: 124, fontFamily: SANS, fontWeight: 700, fontSize: 21,
              lineHeight: 1.2, color: T.text, textAlign: "center" }}>{m.n}</div>
            <div style={{ position: "absolute", left: 0, right: 0, bottom: 8, textAlign: "center", fontFamily: MONO,
              fontWeight: 800, fontSize: 20, color: m.c }}>{Math.round(prog * 100)}%</div>
          </div>
        );
      })}
      <div style={{ position: "absolute", left: 150, top: 740, fontFamily: MONO, fontSize: 22, color: T.muted, opacity: p(0.5, 0.58) }}>
        ZERODHA VARSITY — every module FREE · progress at your pace · also on mobile
      </div>
      {/* red flag panel */}
      <div style={{ position: "absolute", left: 1240, top: 280, width: 550, height: 420, borderRadius: 20,
        background: mix(T.bg1, R, 0.06), border: `3px solid ${mix(T.line, R, 0.5 + Math.sin(frame * 0.1) * 0.3)}`,
        opacity: p(0.58, 0.66), padding: "26px 30px", boxSizing: "border-box" }}>
        <div style={{ fontFamily: MONO, fontWeight: 800, fontSize: 26, color: R, letterSpacing: 2 }}>🚩 RED FLAGS</div>
        {["'Guaranteed' returns", "Sure-shot paid tips", "Unregistered advisors", "Screenshot P&L bragging"].map((r4, i) => (
          <div key={i} style={{ display: "flex", gap: 14, alignItems: "center", marginTop: 22, opacity: p(0.64 + i * 0.05, 0.7 + i * 0.05) }}>
            <span style={{ color: R, fontSize: 26 }}>✕</span>
            <span style={{ fontFamily: SANS, fontWeight: 600, fontSize: 27, color: T.text }}>{r4}</span>
          </div>
        ))}
        <div style={{ fontFamily: MONO, fontSize: 21, color: R, marginTop: 26, opacity: p(0.84, 0.9) }}>
          if returns are "guaranteed" → walk away
        </div>
      </div>
      <ScanBeam theme={T} x={140} y={370} w={1000} h={330} color={R} o={p(0.5, 0.6)} speed={1.2} />
      <Foot theme={T} p={p(0.87, 0.94)}>SEBI investor education + TradingQnA forum — all free, all legitimate</Foot>
    </Stage>
  );
};

// ================================================================ dispatcher
export const TTScene: React.FC<{ variant: string;[key: string]: unknown }> = ({ variant, ...rest }) => {
  switch (variant) {
    case "tt_screener": return <ScreenerScene {...(rest as any)} />;
    case "tt_trio": return <TrioScene {...(rest as any)} />;
    case "tt_tv": return <TVScene {...(rest as any)} />;
    case "tt_chartink": return <ChartinkScene {...(rest as any)} />;
    case "tt_sensibull": return <SensibullScene {...(rest as any)} />;
    case "tt_backtest": return <BacktestScene {...(rest as any)} />;
    case "tt_infowall": return <InfoWallScene {...(rest as any)} />;
    case "tt_smallcase": return <SmallcaseScene {...(rest as any)} />;
    case "tt_learn": return <LearnScene {...(rest as any)} />;
    default: return null;
  }
};
