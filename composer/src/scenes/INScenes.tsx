/**
 * INScenes.tsx — "Intraday Trading: A Framework You Can Actually Follow"
 * Full course, prefix `in`. ~15-16 min / 26 scenes. English (Neerja).
 *
 * Companion to TACScenes (Technical Analysis). Reuses the candlestick identity.
 * Identity: night-sky dark + CANDLESTICK + a SESSION-CLOCK motif (9:15 → 3:30).
 * Semantic accents (consistent throughout, same as TAC):
 *   C  #22D3EE  cyan   — price / chart / structure / VWAP
 *   G  #34D399  green  — profit / bullish / go / target
 *   R  #FB7185  rose   — loss / risk / stop / caution
 *   Y  #FBBF24  amber  — time / the session / setup / rules
 *   V  #A78BFA  violet — strategy / concept labels
 *
 * Every numeric example is COMPUTED at module scope (leverage, trading costs,
 * VWAP, position sizing, R:R win-rate) — never a drawn picture of a number.
 */
import React from "react";
import { useCurrentFrame, interpolate } from "remotion";
import {
  makeTheme, mix, MONO, SANS, useP, usePop, rnd,
  Stage, Bg, Head, Foot, Wire, Flow, Counter, ScanBeam, Brackets,
} from "../lib/primitives";

const T = makeTheme({});
const C = "#22D3EE", G = "#34D399", R = "#FB7185", Y = "#FBBF24", V = "#A78BFA";
type OHLC = { o: number; c: number; h: number; l: number };

// ──────────────── data helpers (module-scope, deterministic)
function fromClose(closes: number[], seed: number, wf = 0.18): OHLC[] {
  return closes.map((c2, i) => {
    const o = i === 0 ? c2 * 0.999 : closes[i - 1];
    const rng = Math.abs(c2 - o) + 1;
    return { o, c: c2, h: Math.max(o, c2) + rng * wf * rnd(i, 1, seed), l: Math.min(o, c2) - rng * wf * rnd(i, 2, seed) };
  });
}
const money = (n: number) => "₹" + Math.round(n).toLocaleString("en-IN");

// ── COMPUTED: trading costs for ONE intraday round-trip (Zerodha-style, ₹1L/side)
// buy ₹1,00,000 + sell ₹1,00,000 → turnover ₹2,00,000
const COST_TURN = 100000;
const COST_BROK = Math.min(20, COST_TURN * 0.0003) * 2;      // ₹20 or 0.03%, per order ×2 = 40
const COST_STT = COST_TURN * 0.00025;                        // 0.025% sell side = 25
const COST_TXN = COST_TURN * 2 * 0.0000297;                  // NSE ~0.00297% on turnover ≈ 5.94
const COST_SEBI = COST_TURN * 2 * 0.000001;                  // ₹10/crore ≈ 0.20
const COST_STAMP = COST_TURN * 0.00003;                      // 0.003% buy side = 3
const COST_GST = (COST_BROK + COST_TXN + COST_SEBI) * 0.18;  // 18% on brok+txn+sebi
const COST_TOTAL = COST_BROK + COST_STT + COST_TXN + COST_SEBI + COST_STAMP + COST_GST; // ≈ 82.45
const COST_PER_YEAR = COST_TOTAL * 5 * 20 * 12;              // 5 trades/day · 20 days · 12 months

// ── COMPUTED: leverage example — ₹50,000 capital, 5x
const LEV_CAP = 50000, LEV_X = 5, LEV_POS = LEV_CAP * LEV_X;  // ₹2,50,000
const LEV_MOVE = 0.02;                                        // 2% move
const LEV_PNL = LEV_POS * LEV_MOVE;                           // ₹5,000
const LEV_PCT = (LEV_PNL / LEV_CAP) * 100;                    // 10% of capital

// ── COMPUTED: position sizing (1% rule) — ₹1,00,000 capital
const PS_CAP = 100000, PS_RISKPCT = 0.01;
const PS_RISK = PS_CAP * PS_RISKPCT;                          // ₹1,000
const PS_ENTRY = 200, PS_STOP = 196, PS_PERSHARE = PS_ENTRY - PS_STOP; // ₹4
const PS_QTY = Math.floor(PS_RISK / PS_PERSHARE);            // 250
const PS_POS = PS_QTY * PS_ENTRY;                            // ₹50,000

// ── COMPUTED: R:R win-rate breakeven table (breakeven win% = 1/(1+RR))
const RR_ROWS = [
  { rr: "1 : 1", be: 100 / (1 + 1) },
  { rr: "1 : 2", be: 100 / (1 + 2) },
  { rr: "1 : 3", be: 100 / (1 + 3) },
];

// ── COMPUTED: VWAP series (typical price × volume, cumulative)
const VW_CLOSES = [100, 102, 101, 103, 104, 103, 102, 101.5, 102.5, 103.5, 104.5, 105, 104, 103.5, 104.5, 105.5, 106, 105.5, 106.5, 107];
const VW_VOL = [95, 88, 70, 62, 55, 50, 44, 40, 42, 45, 41, 56, 48, 44, 52, 62, 74, 66, 82, 96];
const VW_SERIES = fromClose(VW_CLOSES, 61, 0.16);
const VW_VWAP: number[] = (() => {
  let cpv = 0, cv = 0; const out: number[] = [];
  VW_SERIES.forEach((k, i) => { const tp = (k.h + k.l + k.c) / 3; cpv += tp * VW_VOL[i]; cv += VW_VOL[i]; out.push(cpv / cv); });
  return out;
})();

// ── ORB series (opening range from first 6 candles, then breakout up)
const ORB_CLOSES = [100, 101, 99.5, 100.5, 101, 100, 102.5, 104, 106, 105, 107, 109, 108, 110, 112];
const ORB_SERIES = fromClose(ORB_CLOSES, 62, 0.14);
const ORB_N = 6;
const ORB_HI = Math.max(...ORB_SERIES.slice(0, ORB_N).map((k) => k.h));
const ORB_LO = Math.min(...ORB_SERIES.slice(0, ORB_N).map((k) => k.l));

// ── Levels series (clear intraday structure)
const LV_CLOSES = [312, 318, 322, 316, 309, 305, 308, 314, 320, 324, 319, 313, 308, 311, 317, 323, 328, 331, 326, 321];
const LV_SERIES = fromClose(LV_CLOSES, 63, 0.14);
const LV_PDH = 331, LV_PDL = 305, LV_ORH = 322, LV_ORL = 309;

// ── Walkthrough series (consolidation → breakout → run → exit)
const WT_CLOSES = [200, 201, 199.5, 200.5, 201, 200, 199.5, 200.5, 201.5, 204, 206, 208, 207, 210, 212, 211, 213, 215, 214, 216];
const WT_SERIES = fromClose(WT_CLOSES, 64, 0.13);
const WT_ENTRY = 202, WT_STOP = 198, WT_TARGET = 210; // risk 4, reward 8 = 1:2

// ── Volume-confirmation series
const VOLC_CLOSES = [100, 101, 100.5, 101.5, 102, 101.5, 102.5, 105, 107, 106, 108, 110];
const VOLC_SERIES = fromClose(VOLC_CLOSES, 65, 0.14);
const VOLC_VOL = VOLC_SERIES.map((k, i) => ({ v: (i === 7 ? 96 : 30 + rnd(i, 4, 7) * 40), up: k.c >= k.o }));

// ──────────────── CandleChart (renders N candles in a bounding box on Stage coords)
const CandleChart: React.FC<{
  data: OHLC[]; nC: number; bx: number; by: number; bw: number; bh: number;
  upC?: string; dnC?: string; glowLast?: boolean; pminF?: number; pmaxF?: number;
}> = ({ data, nC, bx, by, bw, bh, upC = G, dnC = R, glowLast = true, pminF, pmaxF }) => {
  const n = data.length;
  const pmin = pminF ?? Math.min(...data.map((k) => k.l));
  const pmax = pmaxF ?? Math.max(...data.map((k) => k.h));
  const cx = (i: number) => bx + (i + 0.5) * (bw / n);
  const py = (v: number) => by + ((pmax - v) / (pmax - pmin)) * bh;
  const cw = Math.max(5, (bw / n) * 0.62);
  return (
    <>
      {data.slice(0, nC).map((k, i) => {
        const up = k.c >= k.o; const col = up ? upC : dnC;
        const bt = py(Math.max(k.o, k.c));
        const bHt = Math.max(2, py(Math.min(k.o, k.c)) - bt);
        return (
          <React.Fragment key={i}>
            <div style={{ position: "absolute", left: cx(i) - 1.5, top: py(k.h), width: 3,
              height: Math.max(2, py(k.l) - py(k.h)), background: col, opacity: 0.8 }} />
            <div style={{ position: "absolute", left: cx(i) - cw / 2, top: bt, width: cw, height: bHt,
              borderRadius: 2, background: col, boxShadow: glowLast && i === nC - 1 ? `0 0 10px ${col}` : "none" }} />
          </React.Fragment>
        );
      })}
    </>
  );
};

// ──────────────── SessionBar motif (9:15 → 3:30 trading day timeline)
const TICKS = [
  { t: 0, label: "9:15" }, { t: 0.12, label: "10:00" }, { t: 0.44, label: "12:00" },
  { t: 0.68, label: "1:30" }, { t: 0.92, label: "3:15" }, { t: 1, label: "3:30" },
];
const SessionBar: React.FC<{
  x: number; y: number; w: number; color?: string; o?: number; prog?: number;
  live?: boolean; zones?: { a: number; b: number; c: string }[]; h?: number;
}> = ({ x, y, w, color = Y, o = 1, prog, live = true, zones, h = 16 }) => {
  const frame = useCurrentFrame();
  const mp = prog ?? ((frame * 0.0016) % 1); // auto-sweep when no explicit prog
  return (
    <div style={{ position: "absolute", left: x, top: y, width: w, opacity: o }}>
      {/* track */}
      <div style={{ position: "relative", width: w, height: h, borderRadius: h,
        background: mix(T.panel, color, 0.12), border: `1.5px solid ${mix(T.line, color, 0.4)}`, overflow: "hidden" }}>
        {zones && zones.map((z, i) => (
          <div key={i} style={{ position: "absolute", left: z.a * w, top: 0, width: (z.b - z.a) * w, height: "100%",
            background: mix(T.panel, z.c, 0.4) }} />
        ))}
        {!zones && (
          <div style={{ position: "absolute", left: 0, top: 0, width: mp * w, height: "100%",
            background: `linear-gradient(90deg, ${mix(color, T.bg1, 0.3)}, ${color})` }} />
        )}
      </div>
      {/* live marker */}
      {live && (
        <div style={{ position: "absolute", left: mp * w - 2, top: -6, width: 4, height: h + 12, borderRadius: 3,
          background: color, boxShadow: `0 0 ${10 + Math.sin(frame * 0.12) * 5}px ${color}` }} />
      )}
      {/* ticks */}
      {TICKS.map((tk, i) => (
        <div key={i} style={{ position: "absolute", left: tk.t * w - 20, top: h + 8, width: 40, textAlign: "center",
          fontFamily: MONO, fontSize: 17, color: mix(T.muted, color, 0.4) }}>{tk.label}</div>
      ))}
    </div>
  );
};

// helper: price→pixel Y inside a bounded chart area
function makePY(data: OHLC[], by: number, bh: number, pminF?: number, pmaxF?: number) {
  const pmin = pminF ?? Math.min(...data.map((k) => k.l));
  const pmax = pmaxF ?? Math.max(...data.map((k) => k.h));
  return (v: number) => by + ((pmax - v) / (pmax - pmin)) * bh;
}
function makeCX(n: number, bx: number, bw: number) { return (i: number) => bx + (i + 0.5) * (bw / n); }

// ════════════════════════════════════════════ 1. TITLE
const TitleScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur); const frame = useCurrentFrame(); const pop = usePop(dur);
  const candleMotif = [
    { x: 120, y: 150, h: 120, bh: 48, c: G }, { x: 1730, y: 210, h: 100, bh: 38, c: C },
    { x: 90, y: 770, h: 90, bh: 36, c: R }, { x: 1760, y: 690, h: 110, bh: 44, c: Y },
    { x: 430, y: 940, h: 80, bh: 30, c: V }, { x: 1420, y: 930, h: 85, bh: 34, c: C },
  ];
  return (
    <Stage>
      <Bg theme={T} accent={Y} />
      {candleMotif.map((m, i) => (
        <div key={i} style={{ position: "absolute", left: m.x, top: m.y,
          opacity: 0.16 + Math.sin(frame * 0.04 + i * 1.3) * 0.08 }}>
          <div style={{ width: 3, height: (m.h - m.bh) / 2, background: m.c, margin: "0 auto" }} />
          <div style={{ width: 18, height: m.bh, borderRadius: 3, background: m.c }} />
          <div style={{ width: 3, height: (m.h - m.bh) / 2, background: m.c, margin: "0 auto" }} />
        </div>
      ))}
      <div style={{ position: "absolute", left: 0, right: 0, top: 250, textAlign: "center",
        fontFamily: MONO, fontWeight: 800, fontSize: 22, color: Y, letterSpacing: 10,
        opacity: p(0.04, 0.14), transform: `translateY(${(1 - p(0.04, 0.14)) * 20}px)` }}>
        TRADING EDUCATION · A FRAMEWORK, NOT A TIP-SHEET
      </div>
      <div style={{ position: "absolute", left: 0, right: 0, top: 302, textAlign: "center",
        fontFamily: SANS, fontWeight: 800, fontSize: 112, color: T.text, letterSpacing: -3,
        opacity: p(0.10, 0.22), transform: `scale(${0.92 + pop(0.10) * 0.08})` }}>
        INTRADAY
      </div>
      <div style={{ position: "absolute", left: 0, right: 0, top: 428, textAlign: "center",
        fontFamily: SANS, fontWeight: 800, fontSize: 122, letterSpacing: -4,
        color: Y, textShadow: `0 0 60px ${mix(T.bg0, Y, 0.7)}`,
        opacity: p(0.18, 0.32), transform: `scale(${0.92 + pop(0.18) * 0.08})` }}>
        TRADING
      </div>
      <SessionBar x={560} y={608} w={800} color={Y} o={p(0.30, 0.46)} />
      <div style={{ position: "absolute", left: 300, right: 300, top: 672, textAlign: "center",
        fontFamily: SANS, fontSize: 34, color: T.muted, letterSpacing: 0.5, opacity: p(0.40, 0.56) }}>
        What it really is · Costs &amp; leverage · A repeatable setup &amp; risk plan
      </div>
      <div style={{ position: "absolute", left: 0, right: 0, top: 742, textAlign: "center",
        fontFamily: MONO, fontSize: 21, color: R, opacity: p(0.58, 0.72) }}>
        ⚠ Education only — not investment advice — consult a SEBI-registered advisor
      </div>
    </Stage>
  );
};

// ════════════════════════════════════════════ 2. DIVIDER (parameterised)
const DividerScene: React.FC<{ dur?: number; n?: number; title?: string; sub?: string; color?: string }> = ({
  dur, n = 1, title = "", sub = "", color = Y,
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
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 92, color: T.text, letterSpacing: -2,
          marginTop: 16, opacity: p(0.12, 0.26), transform: `translateY(${(1 - p(0.12, 0.26)) * 28}px)` }}>{title}</div>
        <div style={{ height: 5, width: interpolate(p(0.22, 0.52), [0, 1], [0, 460]),
          background: color, borderRadius: 3, margin: "22px auto" }} />
        <div style={{ fontFamily: SANS, fontSize: 32, color: T.muted, opacity: p(0.32, 0.48) }}>{sub}</div>
      </div>
      <div style={{ position: "absolute", left: 0, right: 0, top: 856,
        display: "flex", justifyContent: "center", gap: 14, opacity: p(0.32, 0.48) }}>
        {[1, 2, 3].map((i) => (
          <div key={i} style={{ width: i === n ? 44 : 14, height: 14, borderRadius: 8,
            background: i <= n ? color : mix(T.panel, color, 0.15),
            border: `1.5px solid ${i <= n ? color : T.line}`,
            opacity: i === n ? 0.7 + Math.sin(frame * 0.1) * 0.3 : 1 }} />
        ))}
      </div>
    </Stage>
  );
};

// ════════════════════════════════════════════ 3. HOOK — the honest number
const HookScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur); const frame = useCurrentFrame();
  const stats = [
    { label: "Very frequent traders (500+ trades/yr)", v: 80, at: 0.46 },
    { label: "Traders under age 30", v: 76, at: 0.56 },
    { label: "All individual intraday traders", v: 71, at: 0.66 },
  ];
  return (
    <Stage>
      <Bg theme={T} accent={R} />
      <Head theme={T} kicker="THE HONEST STARTING POINT" title="Most Intraday Traders Lose Money" color={R} />
      {/* hero stat */}
      <div style={{ position: "absolute", left: 130, top: 250, width: 720, height: 560, borderRadius: 22,
        background: mix(T.bg1, R, 0.05), border: `2.5px solid ${mix(T.line, R, 0.6)}`,
        display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center",
        opacity: p(0.06, 0.16), boxShadow: `0 0 ${40 + Math.sin(frame * 0.05) * 12}px ${mix(T.bg0, R, 0.3)}` }}>
        <div style={{ fontFamily: MONO, fontSize: 24, color: T.muted, letterSpacing: 2, marginBottom: 6 }}>SEBI STUDY · FY23</div>
        <div style={{ display: "flex", alignItems: "baseline" }}>
          <Counter p={p(0.14, 0.40)} to={71} suffix="%" color={R} size={180} />
        </div>
        <div style={{ fontFamily: SANS, fontWeight: 700, fontSize: 30, color: T.text, marginTop: 4 }}>made a net LOSS</div>
        <div style={{ fontFamily: SANS, fontSize: 23, color: T.muted, marginTop: 18, width: 560, textAlign: "center", lineHeight: 1.4 }}>
          7 out of 10 individual intraday traders in the equity cash segment — after costs.
        </div>
      </div>
      {/* breakdown bars */}
      <div style={{ position: "absolute", left: 910, top: 258, fontFamily: MONO, fontWeight: 800, fontSize: 22,
        color: R, letterSpacing: 2, opacity: p(0.40, 0.50) }}>IT GETS WORSE THE MORE YOU TRADE</div>
      {stats.map((s, i) => {
        const lo = p(s.at, s.at + 0.08);
        const bw = interpolate(lo, [0, 1], [0, 720]);
        return (
          <div key={i} style={{ position: "absolute", left: 910, top: 320 + i * 130, width: 780, opacity: lo }}>
            <div style={{ fontFamily: SANS, fontSize: 24, color: T.text, marginBottom: 10 }}>{s.label}</div>
            <div style={{ position: "relative", height: 46, borderRadius: 10, background: mix(T.panel, R, 0.08),
              border: `1.5px solid ${mix(T.line, R, 0.4)}`, overflow: "hidden" }}>
              <div style={{ position: "absolute", left: 0, top: 0, height: "100%", width: (s.v / 100) * 780,
                background: `linear-gradient(90deg, ${mix(R, T.bg1, 0.35)}, ${R})` }} />
              <div style={{ position: "absolute", left: 16, top: 8, fontFamily: MONO, fontWeight: 800,
                fontSize: 26, color: T.bg0 }}>{s.v}% lose</div>
            </div>
          </div>
        );
      })}
      <Foot theme={T} p={p(0.84, 0.93)}>This is not to scare you off — it's the reason a real framework matters. The other 29% follow rules.</Foot>
    </Stage>
  );
};

// ════════════════════════════════════════════ 4. WHAT IS INTRADAY
const WhatIsScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur); const frame = useCurrentFrame();
  // intraday squiggle across the session
  const pts = Array.from({ length: 60 }).map((_, i) => {
    const t = i / 59;
    const y = 470 - Math.sin(t * Math.PI * 1.6) * 120 - t * 30 + Math.sin(t * 22) * 10;
    return { x: 260 + t * 1200, y };
  });
  const buyI = 8, sellI = 46;
  const nDraw = Math.round(interpolate(p(0.18, 0.62), [0, 1], [0, pts.length]));
  const line = pts.slice(0, nDraw).map((q) => `${q.x},${q.y}`).join(" ");
  return (
    <Stage>
      <Bg theme={T} accent={C} />
      <Head theme={T} kicker="DEFINITION — THE ONE-DAY RULE" title="Buy and Sell Within the Same Session" color={C} />
      {/* chart frame */}
      <div style={{ position: "absolute", left: 210, top: 250, width: 1300, height: 380, borderRadius: 16,
        background: mix(T.bg1, C, 0.03), border: `2px solid ${mix(T.line, C, 0.4)}`, opacity: p(0.06, 0.16) }} />
      <svg style={{ position: "absolute", left: 0, top: 0, overflow: "visible" }} width={1920} height={1080}>
        <polyline points={line} fill="none" stroke={C} strokeWidth={4} opacity={0.9} />
      </svg>
      {/* buy / sell markers */}
      {nDraw > buyI && (
        <div style={{ position: "absolute", left: pts[buyI].x - 60, top: pts[buyI].y + 20, opacity: p(0.30, 0.38) }}>
          <div style={{ fontFamily: MONO, fontWeight: 800, fontSize: 24, color: G,
            background: mix(T.panel, G, 0.16), border: `2px solid ${G}`, borderRadius: 8, padding: "5px 14px" }}>BUY ▲</div>
        </div>
      )}
      {nDraw > sellI && (
        <div style={{ position: "absolute", left: pts[sellI].x - 30, top: pts[sellI].y - 66, opacity: p(0.56, 0.64) }}>
          <div style={{ fontFamily: MONO, fontWeight: 800, fontSize: 24, color: R,
            background: mix(T.panel, R, 0.16), border: `2px solid ${R}`, borderRadius: 8, padding: "5px 14px" }}>SELL ▼</div>
        </div>
      )}
      {/* live dot */}
      {nDraw > 1 && nDraw <= pts.length && (
        <div style={{ position: "absolute", left: pts[Math.min(nDraw - 1, pts.length - 1)].x - 7,
          top: pts[Math.min(nDraw - 1, pts.length - 1)].y - 7, width: 14, height: 14, borderRadius: 14,
          background: C, boxShadow: `0 0 ${12 + Math.sin(frame * 0.2) * 6}px ${C}` }} />
      )}
      <SessionBar x={260} y={668} w={1200} color={Y} o={p(0.20, 0.30)} prog={(frame * 0.004) % 1} />
      {/* three defining facts */}
      {[
        { t: "Positions OPEN and CLOSE the same day — nothing is held overnight.", c: C, at: 0.66 },
        { t: "Unclosed trades are auto squared-off near 3:15–3:20 PM by your broker.", c: Y, at: 0.74 },
        { t: "You profit from the day's PRICE MOVE — not from owning the company.", c: G, at: 0.82 },
      ].map((it, i) => (
        <div key={i} style={{ position: "absolute", left: 210, top: 748 + i * 58, width: 1500,
          fontFamily: SANS, fontSize: 26, color: T.text, opacity: p(it.at, it.at + 0.06),
          display: "flex", alignItems: "center", gap: 14 }}>
          <span style={{ width: 12, height: 12, borderRadius: 12, background: it.c, flexShrink: 0 }} />
          {it.t}
        </div>
      ))}
    </Stage>
  );
};

// ════════════════════════════════════════════ 5. INTRADAY vs DELIVERY
const VsDeliveryScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur); const frame = useCurrentFrame();
  const rows = [
    { k: "Holding period", intra: "Same day — square off by 3:30", del: "Days to years", at: 0.20 },
    { k: "What you pay for", intra: "Margin only (part of value)", del: "Full value of shares", at: 0.30 },
    { k: "Overnight risk", intra: "None — you're flat by close", del: "Yes — gaps & news", at: 0.40 },
    { k: "STT (tax)", intra: "0.025% — sell side only", del: "0.10% — both sides", at: 0.50 },
    { k: "Pace & pressure", intra: "Fast, minute-by-minute", del: "Slow, patient", at: 0.60 },
  ];
  return (
    <Stage>
      <Bg theme={T} accent={C} />
      <Head theme={T} kicker="INTRADAY vs DELIVERY" title="Same Market, Very Different Game" color={C} />
      {/* headers */}
      <div style={{ position: "absolute", left: 720, top: 232, width: 500, textAlign: "center",
        fontFamily: MONO, fontWeight: 800, fontSize: 26, color: Y,
        background: mix(T.panel, Y, 0.14), border: `2px solid ${Y}`, borderRadius: 12, padding: "10px 0",
        opacity: p(0.08, 0.16) }}>INTRADAY</div>
      <div style={{ position: "absolute", left: 1260, top: 232, width: 500, textAlign: "center",
        fontFamily: MONO, fontWeight: 800, fontSize: 26, color: C,
        background: mix(T.panel, C, 0.12), border: `2px solid ${C}`, borderRadius: 12, padding: "10px 0",
        opacity: p(0.12, 0.20) }}>DELIVERY</div>
      {rows.map((row, i) => {
        const lo = p(row.at, row.at + 0.07);
        const y = 316 + i * 106;
        const hot = Math.floor(frame / 40) % rows.length === i;
        return (
          <React.Fragment key={i}>
            <div style={{ position: "absolute", left: 130, top: y + 14, width: 560, fontFamily: SANS, fontWeight: 700,
              fontSize: 26, color: T.text, opacity: lo }}>{row.k}</div>
            <div style={{ position: "absolute", left: 720, top: y, width: 500, height: 88, borderRadius: 12,
              background: mix(T.panel, Y, hot ? 0.14 : 0.06), border: `1.5px solid ${mix(T.line, Y, hot ? 0.8 : 0.35)}`,
              display: "flex", alignItems: "center", justifyContent: "center", padding: "0 18px", boxSizing: "border-box",
              textAlign: "center", fontFamily: SANS, fontSize: 22, color: T.text, opacity: lo }}>{row.intra}</div>
            <div style={{ position: "absolute", left: 1260, top: y, width: 500, height: 88, borderRadius: 12,
              background: mix(T.panel, C, hot ? 0.12 : 0.05), border: `1.5px solid ${mix(T.line, C, hot ? 0.7 : 0.3)}`,
              display: "flex", alignItems: "center", justifyContent: "center", padding: "0 18px", boxSizing: "border-box",
              textAlign: "center", fontFamily: SANS, fontSize: 22, color: T.text, opacity: lo }}>{row.del}</div>
          </React.Fragment>
        );
      })}
      <Foot theme={T} p={p(0.86, 0.94)}>Intraday isn't "better" — it's faster, cheaper per trade, but far less forgiving. Speed cuts both ways.</Foot>
    </Stage>
  );
};

// ════════════════════════════════════════════ 6. THE SESSION CLOCK
const SessionScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur); const frame = useCurrentFrame();
  const phases = [
    { name: "OPENING DRIVE", time: "9:15 – 10:00", desc: "Highest volume & volatility. Big moves — and traps. Trend often set here.", c: G, at: 0.24, a: 0.0, b: 0.12 },
    { name: "MID-DAY CHOP", time: "11:00 – 2:00", desc: "Volume dries up. Choppy, range-bound. Most false signals happen now.", c: R, at: 0.46, a: 0.30, b: 0.68 },
    { name: "CLOSING MOVE", time: "2:30 – 3:30", desc: "Volume returns. Trends resume or reverse as positions are squared off.", c: Y, at: 0.66, a: 0.80, b: 1.0 },
  ];
  const zones = phases.map((ph) => ({ a: ph.a, b: ph.b, c: ph.c }));
  return (
    <Stage>
      <Bg theme={T} accent={Y} />
      <Head theme={T} kicker="THE TRADING DAY — 9:15 TO 3:30" title="The Session Has a Rhythm. Learn It." color={Y} />
      <SessionBar x={160} y={300} w={1600} color={Y} o={p(0.06, 0.16)} zones={zones} h={40} live prog={(frame * 0.0016) % 1} />
      {phases.map((ph, i) => {
        const lo = p(ph.at, ph.at + 0.08);
        const x = 160 + i * 540;
        return (
          <div key={i} style={{ position: "absolute", left: x, top: 420, width: 500, height: 360, borderRadius: 18,
            background: mix(T.bg1, ph.c, 0.05), border: `2.5px solid ${mix(T.line, ph.c, 0.55)}`, padding: "26px 28px",
            boxSizing: "border-box", opacity: lo, transform: `translateY(${(1 - lo) * 20}px)` }}>
            <div style={{ fontFamily: MONO, fontWeight: 800, fontSize: 24, color: ph.c, letterSpacing: 2 }}>{ph.name}</div>
            <div style={{ fontFamily: MONO, fontSize: 22, color: T.muted, marginTop: 6 }}>{ph.time}</div>
            <div style={{ height: 2, background: mix(T.line, ph.c, 0.5), margin: "18px 0" }} />
            <div style={{ fontFamily: SANS, fontSize: 25, color: T.text, lineHeight: 1.45 }}>{ph.desc}</div>
          </div>
        );
      })}
      <Foot theme={T} p={p(0.85, 0.94)}>Rule of thumb: trade the open and the close. Respect the mid-day chop — it eats accounts quietly.</Foot>
    </Stage>
  );
};

// ════════════════════════════════════════════ 7. LEVERAGE (computed)
const LeverageScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur); const frame = useCurrentFrame();
  return (
    <Stage>
      <Bg theme={T} accent={Y} />
      <Head theme={T} kicker="MARGIN & LEVERAGE — THE DOUBLE EDGE" title="Leverage Multiplies Both Sides" color={Y} />
      {/* capital → position flow */}
      <div style={{ position: "absolute", left: 130, top: 270, width: 340, height: 190, borderRadius: 16,
        background: mix(T.bg1, C, 0.05), border: `2.5px solid ${C}`, padding: "22px 24px", boxSizing: "border-box",
        opacity: p(0.06, 0.16) }}>
        <div style={{ fontFamily: MONO, fontSize: 20, color: T.muted }}>YOUR CAPITAL</div>
        <div style={{ fontFamily: MONO, fontWeight: 800, fontSize: 46, color: C, marginTop: 10 }}>{money(LEV_CAP)}</div>
      </div>
      <Wire x1={470} y1={365} x2={620} y2={365} p={p(0.18, 0.26)} color={Y} w={3} />
      <div style={{ position: "absolute", left: 470, top: 300, width: 150, textAlign: "center",
        fontFamily: MONO, fontWeight: 800, fontSize: 30, color: Y, opacity: p(0.20, 0.28) }}>× {LEV_X}</div>
      <div style={{ position: "absolute", left: 630, top: 270, width: 380, height: 190, borderRadius: 16,
        background: mix(T.bg1, Y, 0.06), border: `2.5px solid ${Y}`, padding: "22px 24px", boxSizing: "border-box",
        opacity: p(0.24, 0.34), boxShadow: `0 0 ${26 + Math.sin(frame * 0.06) * 8}px ${mix(T.bg0, Y, 0.3)}` }}>
        <div style={{ fontFamily: MONO, fontSize: 20, color: T.muted }}>BUYING POWER (MIS)</div>
        <div style={{ fontFamily: MONO, fontWeight: 800, fontSize: 46, color: Y, marginTop: 10 }}>{money(LEV_POS)}</div>
      </div>
      <Flow x1={470} y1={365} x2={620} y2={365} color={Y} n={5} o={p(0.28, 0.34)} />
      {/* two outcomes of a 2% move */}
      {[
        { c: G, sign: "+", label: "Price moves +2% in your favour", at: 0.44 },
        { c: R, sign: "−", label: "Price moves −2% against you", at: 0.60 },
      ].map((br, i) => {
        const lo = p(br.at, br.at + 0.1);
        return (
          <div key={i} style={{ position: "absolute", left: 1080, top: 268 + i * 130, width: 700, height: 110, borderRadius: 16,
            background: mix(T.bg1, br.c, 0.06), border: `2.5px solid ${br.c}`, padding: "0 26px", boxSizing: "border-box",
            display: "flex", alignItems: "center", gap: 22, opacity: lo }}>
            <div style={{ fontFamily: MONO, fontWeight: 800, fontSize: 44, color: br.c }}>{br.sign}{money(LEV_PNL)}</div>
            <div>
              <div style={{ fontFamily: SANS, fontSize: 23, color: T.text }}>{br.label}</div>
              <div style={{ fontFamily: MONO, fontWeight: 800, fontSize: 24, color: br.c, marginTop: 4 }}>
                = {br.sign}{LEV_PCT.toFixed(0)}% of your capital
              </div>
            </div>
          </div>
        );
      })}
      {/* key line */}
      <div style={{ position: "absolute", left: 130, top: 620, width: 890, height: 150, borderRadius: 16,
        background: mix(T.bg1, R, 0.05), border: `2px dashed ${mix(T.line, R, 0.6)}`, padding: "22px 26px", boxSizing: "border-box",
        opacity: p(0.74, 0.84) }}>
        <div style={{ fontFamily: SANS, fontWeight: 700, fontSize: 27, color: T.text, lineHeight: 1.4 }}>
          A tiny 2% move = a 10% swing on your money. SEBI now caps intraday leverage near <span style={{ color: Y }}>5×</span> —
          because bigger leverage wiped out beginners.
        </div>
      </div>
      <Foot theme={T} p={p(0.86, 0.94)}>Leverage is a tool, not free money. Size positions by RISK (coming up) — never by the maximum margin offered.</Foot>
    </Stage>
  );
};

// ════════════════════════════════════════════ 8. COSTS (computed)
const CostsScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur); const frame = useCurrentFrame();
  const items = [
    { k: "Brokerage (₹20 / order × 2)", v: COST_BROK, at: 0.22 },
    { k: "STT (0.025% sell side)", v: COST_STT, at: 0.30 },
    { k: "Exchange txn charges", v: COST_TXN, at: 0.38 },
    { k: "Stamp duty (0.003% buy)", v: COST_STAMP, at: 0.46 },
    { k: "GST (18%) + SEBI fee", v: COST_GST + COST_SEBI, at: 0.54 },
  ];
  const maxV = Math.max(...items.map((it) => it.v));
  return (
    <Stage>
      <Bg theme={T} accent={R} />
      <Head theme={T} kicker="THE COST OF CHURNING" title="Every Trade Starts in a Small Hole" color={R} />
      <div style={{ position: "absolute", left: 130, top: 244, width: 620, fontFamily: SANS, fontSize: 24,
        color: T.muted, opacity: p(0.08, 0.16), lineHeight: 1.4 }}>
        One round-trip on <span style={{ color: C }}>{money(COST_TURN)}</span> turnover:
      </div>
      {items.map((it, i) => {
        const lo = p(it.at, it.at + 0.07);
        const bw = interpolate(lo, [0, 1], [0, (it.v / maxV) * 380]);
        return (
          <div key={i} style={{ position: "absolute", left: 130, top: 300 + i * 82, width: 900, opacity: lo }}>
            <div style={{ position: "absolute", left: 0, top: 6, width: 400, fontFamily: SANS, fontSize: 23, color: T.text }}>{it.k}</div>
            <div style={{ position: "absolute", left: 430, top: 0, height: 40, width: bw, borderRadius: 8,
              background: `linear-gradient(90deg, ${mix(R, T.bg1, 0.35)}, ${R})` }} />
            <div style={{ position: "absolute", left: 440 + bw, top: 6, fontFamily: MONO, fontWeight: 800,
              fontSize: 24, color: R }}>{money(it.v)}</div>
          </div>
        );
      })}
      {/* total + annualized */}
      <div style={{ position: "absolute", left: 1120, top: 300, width: 660, height: 220, borderRadius: 18,
        background: mix(T.bg1, R, 0.06), border: `2.5px solid ${R}`, padding: "26px 30px", boxSizing: "border-box",
        opacity: p(0.60, 0.70), boxShadow: `0 0 ${30 + Math.sin(frame * 0.06) * 10}px ${mix(T.bg0, R, 0.3)}` }}>
        <div style={{ fontFamily: MONO, fontSize: 22, color: T.muted }}>COST OF ONE ROUND-TRIP</div>
        <div style={{ fontFamily: MONO, fontWeight: 800, fontSize: 62, color: R, marginTop: 8 }}>≈ {money(COST_TOTAL)}</div>
        <div style={{ fontFamily: SANS, fontSize: 22, color: T.text, marginTop: 10, lineHeight: 1.4 }}>
          Price must move this much just to break even — before you make a single rupee.
        </div>
      </div>
      <div style={{ position: "absolute", left: 1120, top: 548, width: 660, height: 180, borderRadius: 18,
        background: mix(T.bg1, Y, 0.05), border: `2px dashed ${mix(T.line, Y, 0.6)}`, padding: "22px 30px", boxSizing: "border-box",
        opacity: p(0.76, 0.86) }}>
        <div style={{ fontFamily: SANS, fontSize: 24, color: T.text, lineHeight: 1.4 }}>
          At just 5 trades a day, that's roughly
          <span style={{ fontFamily: MONO, fontWeight: 800, color: Y, fontSize: 30 }}> {money(COST_PER_YEAR)}</span> a year in costs alone.
        </div>
      </div>
      <Foot theme={T} p={p(0.88, 0.95)}>Overtrading is expensive twice: costs bleed you, and forced trades are bad trades. Fewer, better setups win.</Foot>
    </Stage>
  );
};

// ════════════════════════════════════════════ 9. EDGE — why most lose / part recap
const EdgeScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur); const frame = useCurrentFrame();
  const causes = [
    { emoji: "🎯", t: "No edge — trading on tips, news & gut feeling", at: 0.16 },
    { emoji: "🛑", t: "No stop-loss — small losses become account-enders", at: 0.28 },
    { emoji: "📈", t: "Over-leverage — one bad trade does outsized damage", at: 0.40 },
    { emoji: "🔁", t: "Overtrading & revenge — costs and emotion compound", at: 0.52 },
  ];
  return (
    <Stage>
      <Bg theme={T} accent={V} />
      <Head theme={T} kicker="SO WHY DO MOST LOSE?" title="It's Rarely the Market — It's the Method" color={V} />
      {causes.map((cs, i) => {
        const lo = p(cs.at, cs.at + 0.08);
        return (
          <div key={i} style={{ position: "absolute", left: 130, top: 262 + i * 116, width: 900, height: 96, borderRadius: 14,
            background: mix(T.panel, R, 0.06), border: `2px solid ${mix(T.line, R, 0.45)}`, display: "flex",
            alignItems: "center", gap: 22, padding: "0 26px", boxSizing: "border-box", opacity: lo,
            transform: `translateX(${(1 - lo) * 22}px)` }}>
            <span style={{ fontSize: 40 }}>{cs.emoji}</span>
            <span style={{ fontFamily: SANS, fontWeight: 600, fontSize: 26, color: T.text }}>{cs.t}</span>
          </div>
        );
      })}
      {/* the reframe */}
      <div style={{ position: "absolute", left: 1080, top: 262, width: 700, height: 448, borderRadius: 20,
        background: mix(T.bg1, G, 0.05), border: `2.5px solid ${mix(T.line, G, 0.6)}`, padding: "34px 36px",
        boxSizing: "border-box", opacity: p(0.60, 0.70) }}>
        <div style={{ fontFamily: MONO, fontWeight: 800, fontSize: 24, color: G, letterSpacing: 2 }}>THE GOOD NEWS</div>
        <div style={{ fontFamily: SANS, fontSize: 30, color: T.text, marginTop: 22, lineHeight: 1.5 }}>
          Every one of these is a <span style={{ color: G }}>rules problem</span>, not a talent problem.
          <br /><br />
          The rest of this video is one repeatable framework: a <span style={{ color: Y }}>bias</span>,
          a <span style={{ color: C }}>level</span>, a <span style={{ color: V }}>trigger</span>,
          a <span style={{ color: R }}>stop</span>, and a <span style={{ color: G }}>size</span>.
        </div>
        <div style={{ fontFamily: MONO, fontWeight: 800, fontSize: 22, color: G, marginTop: 26,
          opacity: 0.55 + Math.sin(frame * 0.08) * 0.4 }}>
          Discipline is the edge.
        </div>
      </div>
      <Foot theme={T} p={p(0.86, 0.94)}>The market moves money from the impatient to the patient. Your job is to be on the rules side of that trade.</Foot>
    </Stage>
  );
};

// ════════════════════════════════════════════ 10. TIP 1 — TREND / BIAS
const BiasScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur); const frame = useCurrentFrame();
  const panels = [
    { label: "DAILY — the bias", sub: "Which way is the stock trending?", data: fromClose([280, 288, 296, 292, 301, 310, 318, 326, 334, 343], 71, 0.14), color: C, at: 0.16 },
    { label: "15-MIN — the setup", sub: "Where is today's structure?", data: fromClose([334, 338, 336, 340, 344, 341, 345, 349, 347, 352], 72, 0.14), color: Y, at: 0.40 },
    { label: "5-MIN — the entry", sub: "Trigger, in the SAME direction", data: fromClose([347, 349, 348, 350, 352, 351, 353, 355, 354, 357], 73, 0.14), color: G, at: 0.62 },
  ];
  const hot = Math.floor(frame / 46) % 3;
  return (
    <Stage>
      <Bg theme={T} accent={C} />
      <Head theme={T} kicker="TIP 1 — TRADE WITH THE TREND" title="Top-Down: Bias First, Entry Last" color={C} />
      {panels.map((pn, i) => {
        const lo = p(pn.at, pn.at + 0.08);
        const nC = Math.round(interpolate(p(pn.at, pn.at + 0.22), [0, 1], [0, pn.data.length]));
        const isHot = hot === i && p(0.70, 0.71) > 0.5;
        return (
          <div key={i} style={{ position: "absolute", left: 130 + i * 540, top: 250, width: 500, height: 480, borderRadius: 18,
            background: mix(T.bg1, pn.color, 0.04), border: `2.5px solid ${mix(T.line, pn.color, isHot ? 0.9 : 0.45)}`,
            boxShadow: isHot ? `0 0 30px ${mix(T.bg0, pn.color, 0.5)}` : "none",
            opacity: lo, transform: `translateY(${(1 - lo) * 20}px)` }}>
            <div style={{ fontFamily: MONO, fontWeight: 800, fontSize: 22, color: pn.color, letterSpacing: 2, padding: "18px 22px 2px" }}>{pn.label}</div>
            <div style={{ fontFamily: SANS, fontSize: 20, color: T.muted, paddingLeft: 22, marginBottom: 6 }}>{pn.sub}</div>
            <CandleChart data={pn.data} nC={nC} bx={20} by={90} bw={460} bh={330} />
            {i < 2 && <div style={{ position: "absolute", right: -46, top: 240, fontFamily: MONO, fontWeight: 800, fontSize: 40, color: T.muted, opacity: lo }}>→</div>}
          </div>
        );
      })}
      <Foot theme={T} p={p(0.85, 0.94)}>From our TA course: never fight the higher timeframe. Longs in an uptrend, shorts in a downtrend — not the reverse.</Foot>
    </Stage>
  );
};

// ════════════════════════════════════════════ 11. TIP 2 — MARK YOUR LEVELS
const LevelsScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur); const frame = useCurrentFrame();
  const bx = 200, by = 250, bw = 1180, bh = 520;
  const py = makePY(LV_SERIES, by, bh, 298, 340);
  const nC = Math.round(interpolate(p(0.10, 0.50), [0, 1], [0, LV_SERIES.length]));
  const lines = [
    { v: LV_PDH, label: "PDH · prev day high", c: R, at: 0.54 },
    { v: LV_ORH, label: "OR high · first 15-min", c: Y, at: 0.66 },
    { v: LV_ORL, label: "OR low · first 15-min", c: Y, at: 0.72 },
    { v: LV_PDL, label: "PDL · prev day low", c: G, at: 0.60 },
  ];
  return (
    <Stage>
      <Bg theme={T} accent={Y} />
      <Head theme={T} kicker="TIP 2 — MARK YOUR LEVELS BEFORE 9:15" title="Decide Where You Care — In Advance" color={Y} />
      <div style={{ position: "absolute", left: bx, top: by, width: bw, height: bh, borderRadius: 14,
        background: mix(T.bg1, C, 0.03), border: `2px solid ${mix(T.line, C, 0.4)}`, opacity: p(0.04, 0.12) }} />
      <CandleChart data={LV_SERIES} nC={nC} bx={bx} by={by} bw={bw} bh={bh} pminF={298} pmaxF={340} />
      {lines.map((ln, i) => {
        const lo = p(ln.at, ln.at + 0.06);
        const y = py(ln.v);
        return (
          <React.Fragment key={i}>
            <div style={{ position: "absolute", left: bx, top: y, width: bw, borderTop: `2px dashed ${ln.c}`, opacity: lo }} />
            <div style={{ position: "absolute", left: bx + bw + 10, top: y - 16, width: 320, fontFamily: MONO,
              fontWeight: 700, fontSize: 21, color: ln.c, opacity: lo }}>{ln.label}</div>
          </React.Fragment>
        );
      })}
      {/* live price dot on last candle */}
      {nC > 0 && (
        <div style={{ position: "absolute", left: makeCX(LV_SERIES.length, bx, bw)(Math.min(nC, LV_SERIES.length) - 1) - 6,
          top: py(LV_SERIES[Math.min(nC, LV_SERIES.length) - 1].c) - 6, width: 12, height: 12, borderRadius: 12,
          background: C, boxShadow: `0 0 ${10 + Math.sin(frame * 0.2) * 5}px ${C}`, opacity: p(0.5, 0.55) }} />
      )}
      <Foot theme={T} p={p(0.85, 0.94)}>Prev-day high/low + the first-15-min opening range = your map. Trades happen AT levels, not in empty space.</Foot>
    </Stage>
  );
};

// ════════════════════════════════════════════ 12. TIP 3 — VWAP (computed)
const VwapScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur); const frame = useCurrentFrame();
  const bx = 200, by = 250, bw = 1180, bh = 480;
  const allV = [...VW_SERIES.map((k) => k.l), ...VW_VWAP];
  const allH = [...VW_SERIES.map((k) => k.h), ...VW_VWAP];
  const pmin = Math.min(...allV) - 0.5, pmax = Math.max(...allH) + 0.5;
  const py = (v: number) => by + ((pmax - v) / (pmax - pmin)) * bh;
  const cx = makeCX(VW_SERIES.length, bx, bw);
  const nC = Math.round(interpolate(p(0.10, 0.46), [0, 1], [0, VW_SERIES.length]));
  const vwLine = VW_VWAP.slice(0, nC).map((v, i) => `${cx(i)},${py(v)}`).join(" ");
  return (
    <Stage>
      <Bg theme={T} accent={C} />
      <Head theme={T} kicker="TIP 3 — VWAP, THE INTRADAY ANCHOR" title="The Line the Big Players Watch" color={C} />
      <div style={{ position: "absolute", left: bx, top: by, width: bw, height: bh, borderRadius: 14,
        background: mix(T.bg1, C, 0.03), border: `2px solid ${mix(T.line, C, 0.4)}`, opacity: p(0.04, 0.12) }} />
      <CandleChart data={VW_SERIES} nC={nC} bx={bx} by={by} bw={bw} bh={bh} pminF={pmin} pmaxF={pmax} />
      <svg style={{ position: "absolute", left: 0, top: 0, overflow: "visible" }} width={1920} height={1080}>
        <polyline points={vwLine} fill="none" stroke={V} strokeWidth={4} opacity={p(0.14, 0.24)}
          strokeDasharray="2 0" />
      </svg>
      {nC > 2 && (
        <div style={{ position: "absolute", left: cx(nC - 1) + 14, top: py(VW_VWAP[nC - 1]) - 14,
          fontFamily: MONO, fontWeight: 800, fontSize: 22, color: V, opacity: p(0.30, 0.40) }}>VWAP</div>
      )}
      {/* rule cards */}
      {[
        { t: "Price ABOVE VWAP → intraday bias is UP. Favour longs.", c: G, at: 0.56 },
        { t: "Price BELOW VWAP → bias is DOWN. Favour shorts.", c: R, at: 0.66 },
        { t: "VWAP often acts as support/resistance — great for entries on a pullback to it.", c: V, at: 0.76 },
      ].map((it, i) => (
        <div key={i} style={{ position: "absolute", left: 200, top: 762 + i * 52, width: 1500, fontFamily: SANS,
          fontSize: 25, color: T.text, opacity: p(it.at, it.at + 0.06), display: "flex", alignItems: "center", gap: 14 }}>
          <span style={{ width: 12, height: 12, borderRadius: 12, background: it.c, flexShrink: 0 }} />{it.t}
        </div>
      ))}
    </Stage>
  );
};

// ════════════════════════════════════════════ 13. TIP 4 — ORB SETUP (computed)
const OrbScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur); const frame = useCurrentFrame();
  const bx = 200, by = 250, bw = 1180, bh = 480;
  const py = makePY(ORB_SERIES, by, bh, 96, 114);
  const cx = makeCX(ORB_SERIES.length, bx, bw);
  const nC = Math.round(interpolate(p(0.10, 0.56), [0, 1], [0, ORB_SERIES.length]));
  const boxShow = p(0.30, 0.40);
  const orY1 = py(ORB_HI), orY2 = py(ORB_LO);
  const orX = cx(0) - 20, orW = cx(ORB_N - 1) - cx(0) + 40;
  const breakoutShow = nC > ORB_N + 1;
  return (
    <Stage>
      <Bg theme={T} accent={G} />
      <Head theme={T} kicker="TIP 4 — WAIT FOR A SETUP (ORB)" title="Opening Range Breakout" color={G} />
      <div style={{ position: "absolute", left: bx, top: by, width: bw, height: bh, borderRadius: 14,
        background: mix(T.bg1, C, 0.03), border: `2px solid ${mix(T.line, C, 0.4)}`, opacity: p(0.04, 0.12) }} />
      {/* opening range box */}
      {boxShow > 0.05 && (
        <div style={{ position: "absolute", left: orX, top: orY1, width: orW, height: orY2 - orY1,
          background: mix(T.panel, Y, 0.12), border: `2px solid ${Y}`, borderRadius: 6, opacity: boxShow }} />
      )}
      {boxShow > 0.5 && (
        <div style={{ position: "absolute", left: orX, top: orY1 - 34, fontFamily: MONO, fontWeight: 800,
          fontSize: 20, color: Y, opacity: boxShow }}>OPENING RANGE · first 15 min</div>
      )}
      {/* breakout level line + arrow */}
      {breakoutShow && (
        <>
          <div style={{ position: "absolute", left: orX + orW, top: orY1, width: bx + bw - (orX + orW),
            borderTop: `2px dashed ${G}`, opacity: p(0.58, 0.66) }} />
          <div style={{ position: "absolute", left: cx(ORB_N + 1), top: py(ORB_SERIES[ORB_N + 1].h) - 70,
            fontFamily: MONO, fontWeight: 800, fontSize: 22, color: G, opacity: p(0.62, 0.70),
            background: mix(T.panel, G, 0.16), border: `2px solid ${G}`, borderRadius: 8, padding: "5px 12px" }}>
            ENTRY on breakout ▲
          </div>
        </>
      )}
      <CandleChart data={ORB_SERIES} nC={nC} bx={bx} by={by} bw={bw} bh={bh} pminF={96} pmaxF={114} />
      {/* live dot */}
      {nC > 0 && (
        <div style={{ position: "absolute", left: cx(Math.min(nC, ORB_SERIES.length) - 1) - 6,
          top: py(ORB_SERIES[Math.min(nC, ORB_SERIES.length) - 1].c) - 6, width: 12, height: 12, borderRadius: 12,
          background: C, boxShadow: `0 0 ${10 + Math.sin(frame * 0.2) * 5}px ${C}` }} />
      )}
      <Foot theme={T} p={p(0.84, 0.93)}>Let the first 15 minutes set the range. Enter only when price breaks it WITH volume — don't guess the direction early.</Foot>
    </Stage>
  );
};

// ════════════════════════════════════════════ 14. TIP 5 — DON'T CHASE (pullback)
const PullbackScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur); const frame = useCurrentFrame();
  const mk = (closes: number[], seed: number) => fromClose(closes, seed, 0.13);
  const CHASE = mk([100, 101, 102, 106, 109, 112, 108, 104, 101, 99], 81);   // buy the spike, then it fades
  const PULL = mk([100, 101, 102, 106, 109, 107, 106, 108, 111, 114], 82);   // breakout, pullback, then go
  const panels = [
    { title: "CHASING THE MOVE", sub: "Buy the vertical spike", data: CHASE, color: R, at: 0.14, buyI: 5, tag: "Bought here → gave it all back", tagC: R },
    { title: "WAITING FOR PULLBACK", sub: "Buy the retest, stop below", data: PULL, color: G, at: 0.44, buyI: 6, tag: "Entry on the dip → clean run", tagC: G },
  ];
  return (
    <Stage>
      <Bg theme={T} accent={G} />
      <Head theme={T} kicker="TIP 5 — DON'T CHASE. WAIT FOR THE RETEST" title="The Best Entries Feel Boring" color={G} />
      {panels.map((pn, pi) => {
        const lo = p(pn.at, pn.at + 0.08);
        const bx = 130 + pi * 850, by = 250, bw = 760, bh = 440;
        const py = makePY(pn.data, by, bh);
        const cx = makeCX(pn.data.length, bx, bw);
        const nC = Math.round(interpolate(p(pn.at, pn.at + 0.24), [0, 1], [0, pn.data.length]));
        return (
          <React.Fragment key={pi}>
            <div style={{ position: "absolute", left: bx - 20, top: by - 62, width: bw + 40, height: bh + 130, borderRadius: 18,
              background: mix(T.bg1, pn.color, 0.04), border: `2.5px solid ${mix(T.line, pn.color, 0.5)}`, opacity: lo }} />
            <div style={{ position: "absolute", left: bx, top: by - 52, fontFamily: MONO, fontWeight: 800,
              fontSize: 23, color: pn.color, letterSpacing: 1, opacity: lo }}>{pn.title}</div>
            <div style={{ position: "absolute", left: bx, top: by - 22, fontFamily: SANS, fontSize: 20, color: T.muted, opacity: lo }}>{pn.sub}</div>
            <CandleChart data={pn.data} nC={nC} bx={bx} by={by} bw={bw} bh={bh} />
            {nC > pn.buyI && (
              <div style={{ position: "absolute", left: cx(pn.buyI) - 14, top: py(pn.data[pn.buyI].l) + 14,
                fontFamily: MONO, fontWeight: 800, fontSize: 22, color: pn.color, opacity: p(pn.at + 0.2, pn.at + 0.26) }}>▲</div>
            )}
            <div style={{ position: "absolute", left: bx, top: by + bh + 22, width: bw, fontFamily: SANS,
              fontSize: 23, color: pn.tagC, opacity: p(pn.at + 0.22, pn.at + 0.3) }}>{pn.tag}</div>
          </React.Fragment>
        );
      })}
      <Foot theme={T} p={p(0.86, 0.94)}>A breakout you missed is not a trade you must take. Wait for the retest — it gives you a tight stop and a better price.</Foot>
    </Stage>
  );
};

// ════════════════════════════════════════════ 15. TIP 6 — VOLUME CONFIRMS
const VolumeScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur); const frame = useCurrentFrame();
  const bx = 200, by = 240, bw = 1180, bh = 360;
  const py = makePY(VOLC_SERIES, by, bh);
  const cx = makeCX(VOLC_SERIES.length, bx, bw);
  const nC = Math.round(interpolate(p(0.10, 0.48), [0, 1], [0, VOLC_SERIES.length]));
  const volTop = by + bh + 40, volH = 150, maxVol = Math.max(...VOLC_VOL.map((v) => v.v));
  const breakoutI = 7;
  return (
    <Stage>
      <Bg theme={T} accent={Y} />
      <Head theme={T} kicker="TIP 6 — MAKE VOLUME CONFIRM" title="No Volume, No Conviction" color={Y} />
      <div style={{ position: "absolute", left: bx, top: by, width: bw, height: bh, borderRadius: 14,
        background: mix(T.bg1, C, 0.03), border: `2px solid ${mix(T.line, C, 0.4)}`, opacity: p(0.04, 0.12) }} />
      <CandleChart data={VOLC_SERIES} nC={nC} bx={bx} by={by} bw={bw} bh={bh} />
      {/* volume bars */}
      {VOLC_VOL.slice(0, nC).map((vb, i) => {
        const h = (vb.v / maxVol) * volH;
        const isBreak = i === breakoutI;
        return (
          <div key={i} style={{ position: "absolute", left: cx(i) - 14, top: volTop + (volH - h), width: 28, height: h,
            borderRadius: 3, background: isBreak ? Y : mix(vb.up ? G : R, T.bg1, 0.35),
            boxShadow: isBreak ? `0 0 16px ${Y}` : "none" }} />
        );
      })}
      {nC > breakoutI && (
        <div style={{ position: "absolute", left: cx(breakoutI) - 90, top: volTop - 40, width: 200, textAlign: "center",
          fontFamily: MONO, fontWeight: 800, fontSize: 20, color: Y, opacity: p(0.52, 0.60) }}>volume SPIKE ↑</div>
      )}
      <div style={{ position: "absolute", left: bx, top: volTop + volH + 14, width: bw, fontFamily: SANS, fontSize: 25,
        color: T.text, opacity: p(0.64, 0.72), lineHeight: 1.4 }}>
        The breakout candle rides a <span style={{ color: Y }}>surge in volume</span> — real buyers showed up.
        A breakout on thin volume is the classic trap.
      </div>
      <Foot theme={T} p={p(0.85, 0.94)}>Volume is the one thing that can't be faked. Big move + big volume = trust it. Big move + no volume = fade risk.</Foot>
    </Stage>
  );
};

// ════════════════════════════════════════════ 16. TIP 7 — STOP-LOSS (computed)
const StopScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur); const frame = useCurrentFrame();
  const mk = (closes: number[], seed: number) => fromClose(closes, seed, 0.12);
  const SERIES = mk([200, 201, 202, 200, 198, 196, 193, 189, 184, 178], 91); // trade goes wrong
  const bx = 130, by = 250, bw = 760, bh = 470;
  const py = makePY(SERIES, by, bh, 174, 205);
  const cx = makeCX(SERIES.length, bx, bw);
  const entry = 202, stop = 199;
  return (
    <Stage>
      <Bg theme={T} accent={R} />
      <Head theme={T} kicker="TIP 7 — THE STOP IS NON-NEGOTIABLE" title="Decide Your Exit Before You Enter" color={R} />
      <div style={{ position: "absolute", left: bx, top: by, width: bw, height: bh, borderRadius: 14,
        background: mix(T.bg1, C, 0.03), border: `2px solid ${mix(T.line, C, 0.4)}`, opacity: p(0.06, 0.14) }} />
      <CandleChart data={SERIES} nC={Math.round(interpolate(p(0.12, 0.55), [0, 1], [0, SERIES.length]))} bx={bx} by={by} bw={bw} bh={bh} pminF={174} pmaxF={205} />
      {/* entry + stop lines */}
      <div style={{ position: "absolute", left: bx, top: py(entry), width: bw, borderTop: `2px solid ${C}`, opacity: p(0.24, 0.32) }} />
      <div style={{ position: "absolute", left: bx + bw + 8, top: py(entry) - 14, fontFamily: MONO, fontWeight: 700, fontSize: 20, color: C, opacity: p(0.24, 0.32) }}>ENTRY ₹202</div>
      <div style={{ position: "absolute", left: bx, top: py(stop), width: bw, borderTop: `2px dashed ${R}`, opacity: p(0.34, 0.42) }} />
      <div style={{ position: "absolute", left: bx + bw + 8, top: py(stop) - 14, fontFamily: MONO, fontWeight: 700, fontSize: 20, color: R, opacity: p(0.34, 0.42) }}>STOP ₹199</div>
      {/* two outcomes */}
      <div style={{ position: "absolute", left: 1000, top: 262, width: 790, height: 210, borderRadius: 18,
        background: mix(T.bg1, G, 0.05), border: `2.5px solid ${mix(T.line, G, 0.55)}`, padding: "24px 28px", boxSizing: "border-box",
        opacity: p(0.58, 0.68) }}>
        <div style={{ fontFamily: MONO, fontWeight: 800, fontSize: 22, color: G, letterSpacing: 1 }}>✓ WITH A STOP</div>
        <div style={{ fontFamily: SANS, fontSize: 26, color: T.text, marginTop: 14, lineHeight: 1.45 }}>
          Exit at ₹199. Loss is <span style={{ color: R, fontFamily: MONO, fontWeight: 800 }}>₹3/share</span> — small, planned, survivable.
          You live to trade the next setup.
        </div>
      </div>
      <div style={{ position: "absolute", left: 1000, top: 500, width: 790, height: 210, borderRadius: 18,
        background: mix(T.bg1, R, 0.06), border: `2.5px solid ${R}`, padding: "24px 28px", boxSizing: "border-box",
        opacity: p(0.74, 0.84), boxShadow: `0 0 ${24 + Math.sin(frame * 0.06) * 8}px ${mix(T.bg0, R, 0.3)}` }}>
        <div style={{ fontFamily: MONO, fontWeight: 800, fontSize: 22, color: R, letterSpacing: 1 }}>✗ "IT'LL COME BACK"</div>
        <div style={{ fontFamily: SANS, fontSize: 26, color: T.text, marginTop: 14, lineHeight: 1.45 }}>
          No stop → hope takes over. ₹202 → ₹178 is a <span style={{ color: R, fontFamily: MONO, fontWeight: 800 }}>₹24/share</span> loss.
          One trade undoes ten good ones.
        </div>
      </div>
      <Foot theme={T} p={p(0.87, 0.95)}>A stop-loss is the price at which your reason for the trade is proven wrong. Place it there — then honour it.</Foot>
    </Stage>
  );
};

// ════════════════════════════════════════════ 17. TIP 8 — RISK : REWARD (computed)
const RrScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur); const frame = useCurrentFrame();
  const by = 250, bh = 470, bx = 130, bw = 720;
  const pmin = 494, pmax = 514;
  const py = (v: number) => by + ((pmax - v) / (pmax - pmin)) * bh;
  const entry = 500, stop = 496, target = 508; // 1R = 4, 2R = 8
  return (
    <Stage>
      <Bg theme={T} accent={G} />
      <Head theme={T} kicker="TIP 8 — RISK-TO-REWARD ≥ 1:2" title="Win Small-Often, Lose Small — Still Win" color={G} />
      {/* R:R ladder */}
      <div style={{ position: "absolute", left: bx, top: by, width: bw, height: bh, borderRadius: 14,
        background: mix(T.bg1, C, 0.03), border: `2px solid ${mix(T.line, C, 0.4)}`, opacity: p(0.06, 0.14) }} />
      {/* reward zone */}
      <div style={{ position: "absolute", left: bx, top: py(target), width: bw, height: py(entry) - py(target),
        background: mix(T.panel, G, 0.14), opacity: p(0.30, 0.40) }} />
      {/* risk zone */}
      <div style={{ position: "absolute", left: bx, top: py(entry), width: bw, height: py(stop) - py(entry),
        background: mix(T.panel, R, 0.14), opacity: p(0.20, 0.30) }} />
      {[
        { v: target, label: "TARGET ₹508  ·  +2R", c: G, at: 0.34 },
        { v: entry, label: "ENTRY ₹500", c: C, at: 0.16 },
        { v: stop, label: "STOP ₹496  ·  −1R", c: R, at: 0.24 },
      ].map((ln, i) => (
        <React.Fragment key={i}>
          <div style={{ position: "absolute", left: bx, top: py(ln.v), width: bw,
            borderTop: `2px ${ln.c === C ? "solid" : "dashed"} ${ln.c}`, opacity: p(ln.at, ln.at + 0.06) }} />
          <div style={{ position: "absolute", left: bx + 14, top: py(ln.v) - 30, fontFamily: MONO, fontWeight: 800,
            fontSize: 21, color: ln.c, opacity: p(ln.at, ln.at + 0.06) }}>{ln.label}</div>
        </React.Fragment>
      ))}
      {/* win-rate table */}
      <div style={{ position: "absolute", left: 950, top: 262, width: 840, fontFamily: MONO, fontWeight: 800,
        fontSize: 22, color: G, letterSpacing: 1, opacity: p(0.46, 0.54) }}>BREAK-EVEN WIN RATE</div>
      {RR_ROWS.map((row, i) => {
        const lo = p(0.52 + i * 0.08, 0.60 + i * 0.08);
        const best = row.rr === "1 : 2";
        return (
          <div key={i} style={{ position: "absolute", left: 950, top: 320 + i * 104, width: 840, height: 88, borderRadius: 14,
            background: mix(T.panel, best ? G : C, best ? 0.14 : 0.05), border: `2px solid ${best ? G : mix(T.line, C, 0.4)}`,
            display: "flex", alignItems: "center", padding: "0 30px", boxSizing: "border-box", gap: 30, opacity: lo }}>
            <div style={{ fontFamily: MONO, fontWeight: 800, fontSize: 34, color: best ? G : T.text, width: 130 }}>{row.rr}</div>
            <div style={{ fontFamily: SANS, fontSize: 23, color: T.muted, flex: 1 }}>need only</div>
            <div style={{ fontFamily: MONO, fontWeight: 800, fontSize: 34, color: best ? G : C }}>{row.be.toFixed(0)}% wins</div>
          </div>
        );
      })}
      <Foot theme={T} p={p(0.86, 0.94)}>At 1:2, you can be WRONG two out of three times and still make money. Refuse setups that don't offer at least 2R.</Foot>
    </Stage>
  );
};

// ════════════════════════════════════════════ 18. TIP 9 — POSITION SIZING (computed)
const SizingScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur); const frame = useCurrentFrame();
  const steps = [
    { label: "Total capital", val: money(PS_CAP), c: C, at: 0.14 },
    { label: "Risk 1% per trade", val: money(PS_RISK), c: Y, at: 0.28 },
    { label: "Stop distance / share", val: money(PS_PERSHARE) + "  (₹200 → ₹196)", c: R, at: 0.42 },
    { label: "Shares = risk ÷ stop", val: PS_QTY + " shares", c: G, at: 0.58 },
  ];
  return (
    <Stage>
      <Bg theme={T} accent={G} />
      <Head theme={T} kicker="TIP 9 — SIZE BY RISK, NOT BY GREED" title="The 1% Rule Decides Your Quantity" color={G} />
      {steps.map((st, i) => {
        const lo = p(st.at, st.at + 0.1);
        return (
          <React.Fragment key={i}>
            <div style={{ position: "absolute", left: 130, top: 268 + i * 132, width: 900, height: 108, borderRadius: 16,
              background: mix(T.bg1, st.c, 0.05), border: `2.5px solid ${mix(T.line, st.c, 0.55)}`,
              display: "flex", alignItems: "center", justifyContent: "space-between", padding: "0 34px", boxSizing: "border-box",
              opacity: lo, transform: `translateY(${(1 - lo) * 18}px)` }}>
              <span style={{ fontFamily: SANS, fontWeight: 700, fontSize: 27, color: T.text }}>{st.label}</span>
              <span style={{ fontFamily: MONO, fontWeight: 800, fontSize: 34, color: st.c }}>{st.val}</span>
            </div>
            {i < steps.length - 1 && (
              <div style={{ position: "absolute", left: 560, top: 376 + i * 132, fontFamily: MONO, fontWeight: 800,
                fontSize: 26, color: T.muted, opacity: lo }}>↓</div>
            )}
          </React.Fragment>
        );
      })}
      {/* result */}
      <div style={{ position: "absolute", left: 1090, top: 300, width: 700, height: 400, borderRadius: 20,
        background: mix(T.bg1, G, 0.05), border: `2.5px solid ${G}`, padding: "34px 36px", boxSizing: "border-box",
        opacity: p(0.66, 0.76), boxShadow: `0 0 ${30 + Math.sin(frame * 0.06) * 10}px ${mix(T.bg0, G, 0.3)}` }}>
        <div style={{ fontFamily: MONO, fontWeight: 800, fontSize: 24, color: G, letterSpacing: 2 }}>THE POSITION</div>
        <div style={{ fontFamily: MONO, fontWeight: 800, fontSize: 40, color: T.text, marginTop: 20 }}>{PS_QTY} shares × ₹200</div>
        <div style={{ fontFamily: MONO, fontWeight: 800, fontSize: 30, color: C, marginTop: 6 }}>= {money(PS_POS)} position</div>
        <div style={{ fontFamily: SANS, fontSize: 25, color: T.text, marginTop: 22, lineHeight: 1.5 }}>
          If the stop hits, you lose exactly <span style={{ color: R, fontFamily: MONO, fontWeight: 800 }}>{money(PS_RISK)}</span> — 1% of capital.
          <br /><br />Your <span style={{ color: G }}>stop</span> decides your <span style={{ color: G }}>size</span> — never the other way around.
        </div>
      </div>
      <Foot theme={T} p={p(0.87, 0.95)}>At 1% risk, it takes 100 straight losses to blow up — which no rules-based trader ever does. This is how you survive.</Foot>
    </Stage>
  );
};

// ════════════════════════════════════════════ 19. TIP 10 — TIME OF DAY
const TimeOfDayScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur); const frame = useCurrentFrame();
  const zones = [
    { a: 0.0, b: 0.12, c: G }, { a: 0.12, b: 0.30, c: Y }, { a: 0.30, b: 0.68, c: R }, { a: 0.68, b: 0.80, c: Y }, { a: 0.80, b: 1.0, c: G },
  ];
  const rows = [
    { c: G, band: "9:15 – 10:00 & 2:30 – 3:30", note: "PRIME — volume, momentum, cleaner moves", at: 0.34 },
    { c: Y, band: "10:00 – 11:00 & after 2:00", note: "OK — trends can develop; be selective", at: 0.48 },
    { c: R, band: "11:00 – 2:00 (mid-day)", note: "AVOID — low volume, choppy, whipsaws", at: 0.62 },
  ];
  return (
    <Stage>
      <Bg theme={T} accent={Y} />
      <Head theme={T} kicker="TIP 10 — TRADE THE RIGHT HOURS" title="When You Trade Matters as Much as What" color={Y} />
      <SessionBar x={160} y={300} w={1600} color={Y} o={p(0.06, 0.16)} zones={zones} h={44} live prog={(frame * 0.0016) % 1} />
      {rows.map((r, i) => {
        const lo = p(r.at, r.at + 0.08);
        return (
          <div key={i} style={{ position: "absolute", left: 160, top: 430 + i * 130, width: 1600, height: 108, borderRadius: 16,
            background: mix(T.bg1, r.c, 0.05), border: `2.5px solid ${mix(T.line, r.c, 0.55)}`, display: "flex",
            alignItems: "center", gap: 26, padding: "0 32px", boxSizing: "border-box", opacity: lo,
            transform: `translateX(${(1 - lo) * 20}px)` }}>
            <div style={{ width: 20, height: 60, borderRadius: 6, background: r.c, flexShrink: 0 }} />
            <div style={{ fontFamily: MONO, fontWeight: 800, fontSize: 26, color: r.c, width: 560 }}>{r.band}</div>
            <div style={{ fontFamily: SANS, fontSize: 26, color: T.text }}>{r.note}</div>
          </div>
        );
      })}
      <Foot theme={T} p={p(0.85, 0.94)}>New traders should avoid the first 5 minutes too — the opening auction is wild. Let a little structure form first.</Foot>
    </Stage>
  );
};

// ════════════════════════════════════════════ 20. TIP 11 — PSYCHOLOGY
const PsychScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur); const frame = useCurrentFrame();
  const cards = [
    { emoji: "😤", bad: "Revenge trading", good: "Lost a trade? Step away. Don't 'win it back'.", at: 0.16 },
    { emoji: "🐂", bad: "FOMO entries", good: "Missed it? There's always another setup. Wait.", at: 0.30 },
    { emoji: "🔁", bad: "Overtrading", good: "3 good trades beat 30 forced ones. Quality > activity.", at: 0.44 },
    { emoji: "📓", bad: "No review", good: "Journal every trade. Your mistakes are your syllabus.", at: 0.58 },
  ];
  return (
    <Stage>
      <Bg theme={T} accent={V} />
      <Head theme={T} kicker="TIP 11 — MASTER YOURSELF" title="Your Biggest Opponent Is in the Mirror" color={V} />
      {cards.map((cd, i) => {
        const lo = p(cd.at, cd.at + 0.08);
        const x = 130 + (i % 2) * 850, y = 258 + Math.floor(i / 2) * 260;
        return (
          <div key={i} style={{ position: "absolute", left: x, top: y, width: 790, height: 224, borderRadius: 18,
            background: mix(T.bg1, V, 0.05), border: `2.5px solid ${mix(T.line, V, 0.5)}`, padding: "24px 28px",
            boxSizing: "border-box", opacity: lo, transform: `translateY(${(1 - lo) * 18}px)` }}>
            <div style={{ display: "flex", alignItems: "center", gap: 16 }}>
              <span style={{ fontSize: 40 }}>{cd.emoji}</span>
              <span style={{ fontFamily: MONO, fontWeight: 800, fontSize: 26, color: R }}>✗ {cd.bad}</span>
            </div>
            <div style={{ height: 2, background: mix(T.line, V, 0.5), margin: "16px 0" }} />
            <div style={{ fontFamily: SANS, fontSize: 26, color: T.text, lineHeight: 1.4 }}>
              <span style={{ color: G, fontWeight: 700 }}>✓ </span>{cd.good}
            </div>
          </div>
        );
      })}
      <Foot theme={T} p={p(0.85, 0.94)}>Rules only work if you follow them on a bad day. Discipline under pressure is the whole game.</Foot>
    </Stage>
  );
};

// ════════════════════════════════════════════ 21. COMMON MISTAKES
const MistakesScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur); const frame = useCurrentFrame();
  const items = [
    { emoji: "📉", t: "Averaging into a losing position", at: 0.14 },
    { emoji: "🚫", t: "Moving or removing your stop-loss", at: 0.24 },
    { emoji: "📰", t: "Trading on tips & TV noise", at: 0.34 },
    { emoji: "💸", t: "Using maximum leverage on every trade", at: 0.44 },
    { emoji: "🎰", t: "No plan — entering on a hunch", at: 0.54 },
    { emoji: "🕕", t: "Trading all day, every day", at: 0.64 },
  ];
  const hot = Math.floor(frame / 30) % items.length;
  return (
    <Stage>
      <Bg theme={T} accent={R} />
      <Head theme={T} kicker="THE FAST WAY TO LOSE" title="Six Habits That Empty Accounts" color={R} />
      {items.map((it, i) => {
        const lo = p(it.at, it.at + 0.08);
        const x = 130 + (i % 2) * 850, y = 258 + Math.floor(i / 2) * 172;
        const isHot = hot === i && p(0.7, 0.71) > 0.5;
        return (
          <div key={i} style={{ position: "absolute", left: x, top: y, width: 790, height: 140, borderRadius: 16,
            background: mix(T.bg1, R, isHot ? 0.12 : 0.05), border: `2.5px solid ${mix(T.line, R, isHot ? 0.9 : 0.45)}`,
            display: "flex", alignItems: "center", gap: 22, padding: "0 30px", boxSizing: "border-box", opacity: lo,
            boxShadow: isHot ? `0 0 26px ${mix(T.bg0, R, 0.4)}` : "none" }}>
            <span style={{ fontSize: 46 }}>{it.emoji}</span>
            <span style={{ fontFamily: SANS, fontWeight: 700, fontSize: 28, color: T.text }}>{it.t}</span>
            <span style={{ marginLeft: "auto", fontFamily: MONO, fontWeight: 800, fontSize: 34, color: R }}>✗</span>
          </div>
        );
      })}
      <Foot theme={T} p={p(0.85, 0.94)}>Notice the pattern: every one of these is breaking a rule you already know. Losing is usually self-inflicted.</Foot>
    </Stage>
  );
};

// ════════════════════════════════════════════ 22. FULL WALK-THROUGH (computed)
const WalkthroughScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur); const frame = useCurrentFrame();
  const bx = 130, by = 240, bw = 1180, bh = 540;
  const py = makePY(WT_SERIES, by, bh, 196, 218);
  const cx = makeCX(WT_SERIES.length, bx, bw);
  const nC = Math.round(interpolate(p(0.08, 0.60), [0, 1], [0, WT_SERIES.length]));
  const steps = [
    { t: "1 · Bias UP + price above VWAP", c: C, at: 0.16 },
    { t: "2 · Range breaks with volume → ENTER ₹202", c: G, at: 0.40 },
    { t: "3 · STOP ₹198 (below range) · 1R = ₹4", c: R, at: 0.54 },
    { t: "4 · TARGET ₹210 (2R) → booked", c: G, at: 0.70 },
  ];
  return (
    <Stage>
      <Bg theme={T} accent={G} />
      <Head theme={T} kicker="PUTTING IT TOGETHER — ONE CLEAN TRADE" title="Bias → Level → Trigger → Stop → Target" color={G} />
      <div style={{ position: "absolute", left: bx, top: by, width: bw, height: bh, borderRadius: 14,
        background: mix(T.bg1, C, 0.03), border: `2px solid ${mix(T.line, C, 0.4)}`, opacity: p(0.04, 0.1) }} />
      {/* zones */}
      <div style={{ position: "absolute", left: bx, top: py(WT_TARGET), width: bw, height: py(WT_ENTRY) - py(WT_TARGET),
        background: mix(T.panel, G, 0.1), opacity: p(0.5, 0.58) }} />
      <div style={{ position: "absolute", left: bx, top: py(WT_ENTRY), width: bw, height: py(WT_STOP) - py(WT_ENTRY),
        background: mix(T.panel, R, 0.1), opacity: p(0.44, 0.52) }} />
      <CandleChart data={WT_SERIES} nC={nC} bx={bx} by={by} bw={bw} bh={bh} pminF={196} pmaxF={218} />
      {[
        { v: WT_TARGET, label: "TARGET ₹210", c: G, at: 0.66 },
        { v: WT_ENTRY, label: "ENTRY ₹202", c: C, at: 0.38 },
        { v: WT_STOP, label: "STOP ₹198", c: R, at: 0.50 },
      ].map((ln, i) => (
        <React.Fragment key={i}>
          <div style={{ position: "absolute", left: bx, top: py(ln.v), width: bw,
            borderTop: `2px ${ln.c === C ? "solid" : "dashed"} ${ln.c}`, opacity: p(ln.at, ln.at + 0.05) }} />
          <div style={{ position: "absolute", left: bx + bw + 8, top: py(ln.v) - 14, fontFamily: MONO, fontWeight: 800,
            fontSize: 20, color: ln.c, opacity: p(ln.at, ln.at + 0.05) }}>{ln.label}</div>
        </React.Fragment>
      ))}
      {/* live dot */}
      {nC > 0 && (
        <div style={{ position: "absolute", left: cx(Math.min(nC, WT_SERIES.length) - 1) - 6,
          top: py(WT_SERIES[Math.min(nC, WT_SERIES.length) - 1].c) - 6, width: 12, height: 12, borderRadius: 12,
          background: C, boxShadow: `0 0 ${10 + Math.sin(frame * 0.2) * 6}px ${C}` }} />
      )}
      {/* step chips */}
      <div style={{ position: "absolute", left: bx, top: by + bh + 24, width: bw, display: "flex", gap: 16, flexWrap: "wrap" }}>
        {steps.map((s, i) => (
          <div key={i} style={{ fontFamily: MONO, fontWeight: 700, fontSize: 21, color: T.bg0,
            background: s.c, borderRadius: 999, padding: "8px 18px", opacity: p(s.at, s.at + 0.05) }}>{s.t}</div>
        ))}
      </div>
      <Foot theme={T} p={p(0.86, 0.94)}>Risked ₹4 to make ₹8 — a 1:2 trade, planned before entry. Repeatable. Boring. That's the point.</Foot>
    </Stage>
  );
};

// ════════════════════════════════════════════ 23. THE PRE-TRADE CHECKLIST
const ChecklistScene: React.FC<{ dur?: number; items?: string[] }> = ({ dur, items = [] }) => {
  const p = useP(dur); const frame = useCurrentFrame();
  return (
    <Stage>
      <Bg theme={T} accent={G} />
      <Head theme={T} kicker="BEFORE YOU CLICK BUY" title="The 60-Second Pre-Trade Checklist" color={G} />
      <div style={{ position: "absolute", left: 200, top: 232, width: 1520 }}>
        {items.map((item, i) => {
          const at = 0.08 + i * 0.1;
          const lo = p(at, at + 0.06);
          return (
            <div key={i} style={{ display: "flex", alignItems: "center", gap: 22, marginBottom: 20, opacity: lo,
              transform: `translateX(${(1 - lo) * 20}px)` }}>
              <div style={{ width: 44, height: 44, borderRadius: 10, flexShrink: 0,
                border: `2.5px solid ${G}`, background: mix(T.panel, G, 0.14), color: G,
                display: "flex", alignItems: "center", justifyContent: "center",
                fontFamily: MONO, fontWeight: 800, fontSize: 26 }}>✓</div>
              <div style={{ fontFamily: SANS, fontSize: 28, color: T.text, lineHeight: 1.3, width: 1420 }}>{item}</div>
            </div>
          );
        })}
      </div>
      <Foot theme={T} p={p(0.84, 0.92)}>Can't tick every box? It's not a trade — it's a gamble. The best traders skip more setups than they take.</Foot>
    </Stage>
  );
};

// ════════════════════════════════════════════ 24. RECAP
const RecapScene: React.FC<{ dur?: number; items?: string[]; closer?: string }> = ({ dur, items = [], closer = "" }) => {
  const p = useP(dur); const frame = useCurrentFrame();
  return (
    <Stage>
      <Bg theme={T} accent={Y} />
      <div style={{ position: "absolute", left: 0, right: 0, top: 84, textAlign: "center" }}>
        <div style={{ fontFamily: MONO, fontWeight: 800, fontSize: 22, color: Y, letterSpacing: 8,
          opacity: p(0.03, 0.12) }}>RECAP — THE WHOLE FRAMEWORK</div>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 58, color: T.text, letterSpacing: -2,
          marginTop: 12, opacity: p(0.10, 0.22) }}>Intraday Trading in One Breath</div>
      </div>
      <div style={{ position: "absolute", left: 130, top: 218, width: 1660 }}>
        {items.map((item, i) => {
          const at = 0.05 + i * 0.08;
          const lo = p(at, at + 0.06);
          return (
            <div key={i} style={{ display: "flex", alignItems: "center", gap: 18, marginBottom: 17, opacity: lo,
              transform: `translateX(${(1 - lo) * 20}px)` }}>
              <div style={{ width: 5, height: 34, borderRadius: 3, background: Y, flexShrink: 0 }} />
              <div style={{ fontFamily: MONO, fontWeight: 800, fontSize: 20, color: Y, width: 44, flexShrink: 0 }}>
                {String(i + 1).padStart(2, "0")}</div>
              <div style={{ fontFamily: SANS, fontSize: 25, color: T.text, lineHeight: 1.3, width: 1540 }}>{item}</div>
            </div>
          );
        })}
      </div>
      {closer && (
        <div style={{ position: "absolute", left: 130, bottom: 96, right: 130, textAlign: "center",
          fontFamily: SANS, fontStyle: "italic", fontSize: 36, color: Y,
          textShadow: `0 0 40px ${mix(T.bg0, Y, 0.6)}`, opacity: p(0.80, 0.90), lineHeight: 1.3 }}>{closer}</div>
      )}
      <div style={{ position: "absolute", left: 130, top: 986, right: 130, textAlign: "center",
        fontFamily: MONO, fontSize: 20, color: R, opacity: 0.5 + Math.sin(frame * 0.06) * 0.3 }}>
        ⚠ Education only · Not investment advice · Consult a SEBI-registered advisor before trading
      </div>
    </Stage>
  );
};

// ════════════════════════════════════════════ THUMBNAIL (1920×1080, static — for YouTube)
const ThumbScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  // full breakout chart, right side
  const bx = 1120, by = 250, bw = 700, bh = 560;
  const py = makePY(WT_SERIES, by, bh, 196, 218);
  const cx = makeCX(WT_SERIES.length, bx, bw);
  const glow = 30 + Math.sin(frame * 0.06) * 10;
  // decorative floating candles
  const motif = [
    { x: 90, y: 120, h: 110, bh: 44, c: G }, { x: 1850, y: 150, h: 90, bh: 34, c: C },
    { x: 70, y: 900, h: 90, bh: 34, c: R }, { x: 1860, y: 880, h: 100, bh: 40, c: Y },
  ];
  return (
    <Stage>
      <Bg theme={T} accent={R} />
      {motif.map((m, i) => (
        <div key={i} style={{ position: "absolute", left: m.x, top: m.y, opacity: 0.22 }}>
          <div style={{ width: 4, height: (m.h - m.bh) / 2, background: m.c, margin: "0 auto" }} />
          <div style={{ width: 22, height: m.bh, borderRadius: 4, background: m.c }} />
          <div style={{ width: 4, height: (m.h - m.bh) / 2, background: m.c, margin: "0 auto" }} />
        </div>
      ))}
      {/* LEFT — the hook */}
      <div style={{ position: "absolute", left: 90, top: 150, width: 1000 }}>
        <div style={{ display: "inline-flex", alignItems: "center", gap: 14, background: mix(T.panel, Y, 0.16),
          border: `2px solid ${Y}`, borderRadius: 999, padding: "10px 24px" }}>
          <span style={{ width: 12, height: 12, borderRadius: 12, background: Y }} />
          <span style={{ fontFamily: MONO, fontWeight: 800, fontSize: 32, color: Y, letterSpacing: 4 }}>INTRADAY TRADING</span>
        </div>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 300, color: R, letterSpacing: -8, lineHeight: 0.9,
          marginTop: 26, textShadow: `0 0 ${glow * 2}px ${mix(T.bg0, R, 0.8)}` }}>71%</div>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 104, color: T.text, letterSpacing: -3, marginTop: -6 }}>LOSE MONEY</div>
        <div style={{ marginTop: 34, display: "inline-flex", alignItems: "center", gap: 16, background: mix(T.panel, G, 0.14),
          border: `2.5px solid ${G}`, borderRadius: 16, padding: "18px 30px" }}>
          <span style={{ fontFamily: SANS, fontWeight: 800, fontSize: 46, color: G }}>The framework the other 29% use →</span>
        </div>
      </div>
      {/* RIGHT — breakout chart with entry/stop/target */}
      <div style={{ position: "absolute", left: bx - 24, top: by - 30, width: bw + 60, height: bh + 70, borderRadius: 24,
        background: mix(T.bg1, C, 0.05), border: `2.5px solid ${mix(T.line, C, 0.5)}`,
        boxShadow: `0 0 ${glow}px ${mix(T.bg0, G, 0.35)}` }} />
      {/* zones */}
      <div style={{ position: "absolute", left: bx, top: py(WT_TARGET), width: bw, height: py(WT_ENTRY) - py(WT_TARGET),
        background: mix(T.panel, G, 0.16) }} />
      <div style={{ position: "absolute", left: bx, top: py(WT_ENTRY), width: bw, height: py(WT_STOP) - py(WT_ENTRY),
        background: mix(T.panel, R, 0.16) }} />
      <CandleChart data={WT_SERIES} nC={WT_SERIES.length} bx={bx} by={by} bw={bw} bh={bh} pminF={196} pmaxF={218} />
      {[
        { v: WT_TARGET, label: "TARGET", c: G }, { v: WT_ENTRY, label: "ENTRY", c: C }, { v: WT_STOP, label: "STOP", c: R },
      ].map((ln, i) => (
        <React.Fragment key={i}>
          <div style={{ position: "absolute", left: bx, top: py(ln.v), width: bw,
            borderTop: `3px ${ln.c === C ? "solid" : "dashed"} ${ln.c}` }} />
          <div style={{ position: "absolute", left: bx + 12, top: py(ln.v) - 34, fontFamily: MONO, fontWeight: 800,
            fontSize: 26, color: ln.c, background: mix(T.bg0, ln.c, 0.1), padding: "2px 10px", borderRadius: 6 }}>{ln.label}</div>
        </React.Fragment>
      ))}
      {/* big up arrow */}
      <div style={{ position: "absolute", left: bx + bw - 96, top: by + 40, fontFamily: SANS, fontWeight: 800,
        fontSize: 130, color: G, textShadow: `0 0 ${glow}px ${mix(T.bg0, G, 0.8)}` }}>▲</div>
    </Stage>
  );
};

// ════════════════════════════════════════════ DISPATCHER
export const INScene: React.FC<{ variant: string; [key: string]: unknown }> = ({ variant, ...rest }) => {
  switch (variant) {
    case "in_thumb":       return <ThumbScene {...(rest as any)} />;
    case "in_title":       return <TitleScene {...(rest as any)} />;
    case "in_div":         return <DividerScene {...(rest as any)} />;
    case "in_hook":        return <HookScene {...(rest as any)} />;
    case "in_whatis":      return <WhatIsScene {...(rest as any)} />;
    case "in_vsdelivery":  return <VsDeliveryScene {...(rest as any)} />;
    case "in_session":     return <SessionScene {...(rest as any)} />;
    case "in_leverage":    return <LeverageScene {...(rest as any)} />;
    case "in_costs":       return <CostsScene {...(rest as any)} />;
    case "in_edge":        return <EdgeScene {...(rest as any)} />;
    case "in_bias":        return <BiasScene {...(rest as any)} />;
    case "in_levels":      return <LevelsScene {...(rest as any)} />;
    case "in_vwap":        return <VwapScene {...(rest as any)} />;
    case "in_orb":         return <OrbScene {...(rest as any)} />;
    case "in_pullback":    return <PullbackScene {...(rest as any)} />;
    case "in_volume":      return <VolumeScene {...(rest as any)} />;
    case "in_stop":        return <StopScene {...(rest as any)} />;
    case "in_rr":          return <RrScene {...(rest as any)} />;
    case "in_sizing":      return <SizingScene {...(rest as any)} />;
    case "in_timeofday":   return <TimeOfDayScene {...(rest as any)} />;
    case "in_psych":       return <PsychScene {...(rest as any)} />;
    case "in_mistakes":    return <MistakesScene {...(rest as any)} />;
    case "in_walkthrough": return <WalkthroughScene {...(rest as any)} />;
    case "in_checklist":   return <ChecklistScene {...(rest as any)} />;
    case "in_recap":       return <RecapScene {...(rest as any)} />;
    default: return null;
  }
};
