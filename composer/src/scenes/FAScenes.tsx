/**
 * FAScenes.tsx — "Reading a Business by the Numbers" — Fundamental Analysis course.
 *
 * A 7-chapter English course teaching every core fundamental-analysis term (P&L,
 * margins, returns, valuation multiples, leverage, growth/quality) with the ADEPT
 * method (Analogy → Diagram → Example → Plain-English → Technical). One running
 * real example: three Indian lead-recycling companies — Ardee, Gravita, Pondy.
 *
 * Identity:
 *   theme  — near-black "financial slate", teal primary (clarity / analysis).
 *   accents (semantic, consistent across ALL chapters):
 *     A.rev    sky      = revenue / top line / money coming IN
 *     A.cost   coral    = costs / anything subtracted / risk
 *     A.profit emerald  = profit / returns / what survives / "good"
 *     A.val    violet   = valuation / price / the market's opinion
 *     A.debt   amber    = debt / leverage / interest
 *     company hues: A.ardee teal · A.grav indigo · A.pondy orange
 *   motif  — a "ledger tape": faint rows of figures with a marching scan highlight,
 *            echoed in title / dividers / backgrounds (LedgerMotif). The P&L
 *            waterfall is the recurring hero diagram.
 *
 * Rules (skills/03): every scene phases with useP(dur) (no fixed frames); a
 * SceneProgress bar + Bg wrap every scene so no frame reads frozen; continuous
 * motion in every frame; randomness only via rnd(); no CSS filter/blur.
 * Captions ON → NO Foot (bottom band is the caption lane); takeaways live ≤ y880.
 */
import React from "react";
import { AbsoluteFill, interpolate, useCurrentFrame } from "remotion";
import {
  makeTheme, mix, useP, usePop, rnd, MONO, SANS,
  Bg, Stage, Kicker, Head, Card, Flow, Wire, Counter, Brackets, ScanBeam,
} from "../lib/primitives";

// ---------------------------------------------------------------- identity
const T = makeTheme({ accent: "#2DD4BF", bg0: "#05070C", bg1: "#0A0E18", bg2: "#111726", panel: "#151B2C" });
const A = {
  rev: "#38BDF8",     // revenue / top line (sky)
  cost: "#F87171",    // costs / subtractions / risk (coral)
  profit: "#34D399",  // profit / returns / good (emerald)
  val: "#A78BFA",     // valuation / price / market (violet)
  debt: "#FBBF24",    // debt / leverage / interest (amber)
  teal: "#2DD4BF",    // primary
  gray: "#8B93B0",
  ardee: "#2DD4BF",   // company: Ardee (teal)
  grav: "#818CF8",    // company: Gravita (indigo)
  pondy: "#FB923C",   // company: Pondy (orange)
};

// Reveals compressed into the front ~0.62 of the beat (narration front-loads names),
// while the progress bar + continuous motion use the FULL beat (skills/02 A/V-lag).
const SPAN = 0.62;
const useReveal = (dur?: unknown) => {
  const p = useP(dur);
  return (a: number, b: number) => p(Math.min(1, a * SPAN), Math.min(1, b * SPAN));
};

// ---------------------------------------------------------------- number fmt
const fmt = (v: number, d = 0) =>
  v.toLocaleString("en-IN", { minimumFractionDigits: d, maximumFractionDigits: d });

// ---------------------------------------------------------------- motif
/** Ledger tape: faint rows of figures with a marching bright lane. Continuous. */
const LedgerMotif: React.FC<{ x: number; y: number; cols: number; rows: number; cell?: number; color?: string; o?: number; seed?: number }> = ({
  x, y, cols, rows, cell = 26, color = A.teal, o = 1, seed = 0,
}) => {
  const frame = useCurrentFrame();
  const wave = (frame * 0.85) % (rows + 5) - 2.5;
  return (
    <div style={{ position: "absolute", left: x, top: y, display: "grid", gridTemplateColumns: `repeat(${cols}, ${cell * 1.7}px)`, gridAutoRows: `${cell}px`, gap: 6, opacity: o }}>
      {Array.from({ length: cols * rows }).map((_, i) => {
        const c = i % cols, r = Math.floor(i / cols);
        const heat = Math.max(0, 1 - Math.abs(r - wave + Math.sin(c * 1.3 + seed) * 1.1) / 2.3);
        const digit = Math.floor(rnd(c, r, seed) * 10);
        return (
          <div key={i} style={{
            fontFamily: MONO, fontSize: cell * 0.72, fontWeight: 700, textAlign: "right",
            color: mix(T.line, color, 0.25 + heat * 0.75),
            textShadow: heat > 0.5 ? `0 0 10px ${mix(T.bg0, color, heat)}` : "none",
          }}>{rnd(c, r, seed + 9) > 0.82 ? "." : digit}</div>
        );
      })}
    </div>
  );
};

/** Universal "this is playing" bar filling L→R across the whole beat, frame edge. */
const SceneProgress: React.FC<{ dur?: unknown; color?: string }> = ({ dur, color = A.teal }) => {
  const p = useP(dur);
  return (
    <div style={{ position: "absolute", left: 0, bottom: 0, width: 1920, height: 5, background: "rgba(255,255,255,0.05)" }}>
      <div style={{ height: "100%", width: `${p(0, 1) * 1920}px`, background: `linear-gradient(90deg, ${A.rev}, ${color}, ${A.profit})`, boxShadow: `0 0 12px ${color}` }} />
    </div>
  );
};

/** Wrap that gives every content scene the Bg + progress bar (never a frozen frame). */
const Frame: React.FC<{ dur?: unknown; color?: string; children: React.ReactNode }> = ({ dur, color, children }) => (
  <>
    <Bg theme={T} accent={color || A.teal} />
    <Stage>{children}</Stage>
    <SceneProgress dur={dur} color={color} />
  </>
);

// ================================================================ TITLE
const TitleScene: React.FC<{
  dur?: number; kicker?: string; line1?: string; line2?: string; sub?: string; color?: string;
}> = ({ dur, kicker = "FUNDAMENTAL ANALYSIS · FROM SCRATCH", line1 = "Reading a Business", line2 = "by the Numbers", sub = "P&L · margins · returns · valuation · leverage", color = A.teal }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const pop = usePop(dur);
  return (
    <>
      <Bg theme={T} accent={color} />
      <AbsoluteFill style={{ alignItems: "center", justifyContent: "center" }}>
        <Stage>
          <LedgerMotif x={90} y={120} cols={5} rows={11} cell={30} color={color} o={0.42} />
          <LedgerMotif x={1470} y={560} cols={5} rows={11} cell={30} color={A.val} o={0.36} seed={4} />
          {Array.from({ length: 9 }).map((_, i) => {
            const ang = frame * 0.009 + (i / 9) * Math.PI * 2;
            return <div key={i} style={{
              position: "absolute", left: 960 + Math.cos(ang) * (560 + i * 11) - 5, top: 540 + Math.sin(ang) * (250 + i * 7) - 5,
              width: 9, height: 9, borderRadius: 9, background: i % 2 ? color : A.profit, opacity: 0.18 + rnd(i, 3) * 0.3, boxShadow: `0 0 12px ${color}`,
            }} />;
          })}
          <div style={{ position: "absolute", left: 0, right: 0, top: 300, textAlign: "center", transform: `scale(${0.93 + pop(0) * 0.07})`, zIndex: 2 }}>
            <div style={{ display: "flex", justifyContent: "center", marginBottom: 26 }}>
              <Kicker theme={T} text={kicker} color={color} cx />
            </div>
            <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 118, lineHeight: 1.02, letterSpacing: -3, color: T.text }}>
              <div>{line1}</div>
              <div style={{ color, textShadow: `0 0 70px ${mix(T.bg0, color, 0.7)}` }}>{line2}</div>
            </div>
            <div style={{ height: 6, width: interpolate(p(0.18, 0.45), [0, 1], [0, 560]), background: `linear-gradient(90deg, ${A.rev}, ${color}, ${A.profit})`, borderRadius: 3, margin: "32px auto" }} />
            <div style={{ fontFamily: SANS, fontSize: 37, color: T.muted, opacity: p(0.28, 0.5) }}>{sub}</div>
          </div>
        </Stage>
      </AbsoluteFill>
    </>
  );
};

// ================================================================ DIVIDER
const DividerScene: React.FC<{ dur?: number; n?: number; title?: string; sub?: string; color?: string; total?: number }> = ({
  dur, n = 1, title = "", sub = "", color = A.teal, total = 7,
}) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  return (
    <>
      <Bg theme={T} accent={color} />
      <Stage>
        <LedgerMotif x={110} y={300} cols={4} rows={9} cell={28} color={color} o={0.3} />
        <LedgerMotif x={1560} y={380} cols={4} rows={9} cell={28} color={color} o={0.28} seed={6} />
        <Brackets x={430} y={330} w={1060} h={430} color={color} o={p(0.02, 0.14)} len={52} />
        <ScanBeam theme={T} x={440} y={340} w={1040} h={410} color={color} o={p(0.05, 0.2)} speed={1.5} />
        <div style={{ position: "absolute", left: 0, right: 0, top: 388, textAlign: "center" }}>
          <div style={{ fontFamily: MONO, fontWeight: 800, fontSize: 32, color, letterSpacing: 10, opacity: p(0.05, 0.15) }}>CHAPTER {("0" + n).slice(-2)}</div>
          <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 92, color: T.text, letterSpacing: -2, marginTop: 18, opacity: p(0.12, 0.24), transform: `translateY(${(1 - p(0.12, 0.24)) * 28}px)` }}>{title}</div>
          <div style={{ height: 5, width: interpolate(p(0.2, 0.5), [0, 1], [0, 440]), background: color, borderRadius: 3, margin: "24px auto" }} />
          <div style={{ fontFamily: SANS, fontSize: 34, color: T.muted, opacity: p(0.3, 0.45) }}>{sub}</div>
        </div>
        <div style={{ position: "absolute", left: 0, right: 0, top: 860, display: "flex", justifyContent: "center", gap: 14, opacity: p(0.3, 0.45) }}>
          {Array.from({ length: total }).map((_, i) => {
            const k = i + 1;
            return <div key={k} style={{ width: k === n ? 42 : 13, height: 13, borderRadius: 8,
              background: k <= n ? color : mix(T.panel, color, 0.15), border: `1.5px solid ${k <= n ? color : T.line}`,
              opacity: k === n ? 0.7 + Math.sin(frame * 0.1) * 0.3 : 1 }} />;
          })}
        </div>
      </Stage>
    </>
  );
};

// ================================================================ ROADMAP
type Part = { n: number; title: string; sub: string; c: string };
const RoadmapScene: React.FC<{ dur?: number; kicker?: string; parts?: Part[] }> = ({
  dur, kicker = "THE COURSE · SEVEN CHAPTERS",
  parts = [
    { n: 1, title: "The Statements", sub: "revenue → profit, line by line", c: A.rev },
    { n: 2, title: "Margins", sub: "how much of each rupee is kept", c: A.profit },
    { n: 3, title: "Returns", sub: "ROE · ROCE · ROIC · DuPont", c: A.teal },
    { n: 4, title: "Valuation", sub: "market cap · EV · P/E · EV/EBITDA", c: A.val },
    { n: 5, title: "Leverage", sub: "debt · coverage · solvency", c: A.debt },
    { n: 6, title: "Growth & Quality", sub: "CAGR · free cash flow · working capital", c: A.rev },
    { n: 7, title: "Putting It Together", sub: "reading a company end to end", c: A.profit },
  ],
}) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const y0 = 236, rowH = 92, railX = 250;
  const hot = Math.floor(frame / 22) % parts.length;
  const railFill = p(0.06, 0.84);
  return (
    <Frame dur={dur}>
      <div style={{ position: "absolute", left: 0, right: 0, top: 96, textAlign: "center", opacity: p(0, 0.06) }}>
        <Kicker theme={T} text={kicker} cx />
      </div>
      <div style={{ position: "absolute", left: railX, top: y0 + 18, width: 4, height: parts.length * rowH - 40, background: T.line, borderRadius: 2 }} />
      <div style={{ position: "absolute", left: railX, top: y0 + 18, width: 4, height: (parts.length * rowH - 40) * railFill, background: `linear-gradient(180deg, ${A.rev}, ${A.profit})`, borderRadius: 2, boxShadow: `0 0 12px ${A.teal}` }} />
      {parts.map((pt, i) => {
        const at = 0.08 + i * 0.1;
        const o = p(at, at + 0.09);
        const active = hot === i;
        const y = y0 + i * rowH;
        return (
          <React.Fragment key={pt.n}>
            <div style={{ position: "absolute", left: railX - 15, top: y + 6, width: 34, height: 34, borderRadius: 20, background: mix(T.bg0, pt.c, 0.5 + (active ? 0.3 : 0)), border: `3px solid ${pt.c}`, opacity: o, boxShadow: active ? `0 0 18px ${pt.c}` : "none" }} />
            <div style={{ position: "absolute", left: railX + 46, top: y, width: 1200, opacity: o, transform: `translateX(${(1 - o) * 16}px)` }}>
              <div style={{ display: "flex", alignItems: "baseline", gap: 18 }}>
                <span style={{ fontFamily: MONO, fontWeight: 800, fontSize: 22, color: pt.c }}>{("0" + pt.n).slice(-2)}</span>
                <span style={{ fontFamily: SANS, fontWeight: 800, fontSize: 38, color: active ? T.text : mix(T.text, T.bg1, 0.15), letterSpacing: -0.8 }}>{pt.title}</span>
                <span style={{ fontFamily: SANS, fontSize: 25, color: T.muted }}>— {pt.sub}</span>
              </div>
            </div>
          </React.Fragment>
        );
      })}
    </Frame>
  );
};

// ================================================================ ANALOGY (ADEPT · A)
type Side = { emoji?: string; label?: string; cap?: string; c?: string };
const AnalogyScene: React.FC<{ dur?: number; kicker?: string; title?: string; left?: Side; right?: Side; note?: string; color?: string }> = ({
  dur, kicker = "ANALOGY", title = "", left = {}, right = {}, note = "", color = A.teal,
}) => {
  const rp = useReveal(dur);
  const L: Required<Side> = { emoji: "🏠", label: "Everyday idea", cap: "", c: A.gray, ...left };
  const R: Required<Side> = { emoji: "📊", label: "The finance term", cap: "", c: color, ...right };
  const cardY = 300, cardW = 660, cardH = 420;
  const box = (s: Required<Side>, x: number, at: number) => (
    <Card theme={T} x={x} y={cardY} w={cardW} h={cardH} color={s.c} o={rp(at, at + 0.12)} pad="34px 38px" glow>
      <div style={{ fontFamily: MONO, fontSize: 22, color: s.c, fontWeight: 700, letterSpacing: 2, textTransform: "uppercase" }}>{s.label}</div>
      <div style={{ fontSize: 128, textAlign: "center", margin: "26px 0" }}>{s.emoji}</div>
      <div style={{ fontFamily: SANS, fontWeight: 400, fontSize: 28, color: T.text, lineHeight: 1.4, textAlign: "center" }}>{s.cap}</div>
    </Card>
  );
  return (
    <Frame dur={dur} color={color}>
      <Head theme={T} kicker={kicker} title={title} color={color} o={rp(0, 0.08)} />
      {box(L, 130, 0.16)}
      {box(R, 1130, 0.34)}
      {/* the "≈" bridge */}
      <div style={{ position: "absolute", left: 790, top: cardY + cardH / 2 - 60, width: 340, textAlign: "center", opacity: rp(0.5, 0.62) }}>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 96, color: A.profit, textShadow: `0 0 30px ${mix(T.bg0, A.profit, 0.6)}` }}>≈</div>
      </div>
      <Flow x1={790} y1={cardY + cardH / 2} x2={1130} y2={cardY + cardH / 2} color={A.profit} n={6} />
      {note && (
        <div style={{ position: "absolute", left: 130, top: 790, width: 1660, textAlign: "center", fontFamily: SANS, fontSize: 30, color: T.text, opacity: rp(0.66, 0.8), lineHeight: 1.4 }}>{note}</div>
      )}
    </Frame>
  );
};

// ================================================================ WATERFALL (P&L)
// segs: ordered. subtotal=true → bar from baseline to running (a "total"); else a
// floating delta bar (delta usually negative = a cost). Running total tracked.
type WSeg = { label: string; delta?: number; value?: number; c: string; subtotal?: boolean };
const WaterfallScene: React.FC<{ dur?: number; kicker?: string; title?: string; unit?: string; segs?: WSeg[]; note?: string; color?: string; decimals?: number }> = ({
  dur, kicker = "THE P&L WATERFALL", title = "From Revenue to Profit", unit = "₹ Cr", color = A.rev,
  decimals = 0,
  segs = [
    { label: "Revenue", value: 1168, c: A.rev, subtotal: true },
    { label: "− Operating costs", delta: -1021, c: A.cost },
    { label: "EBITDA", value: 147, c: A.profit, subtotal: true },
    { label: "− Depreciation", delta: -20, c: A.cost },
    { label: "− Interest", delta: -18, c: A.debt },
    { label: "− Tax", delta: -24, c: A.cost },
    { label: "Net profit (PAT)", value: 85, c: A.profit, subtotal: true },
  ],
  note = "Ardee FY26 (approx). Every ratio ahead is built from these lines.",
}) => {
  const rp = useReveal(dur);
  // compute running + bar geometry
  const runs: { seg: WSeg; from: number; to: number }[] = [];
  let run = 0;
  for (const s of segs) {
    if (s.subtotal) { runs.push({ seg: s, from: 0, to: s.value ?? run }); run = s.value ?? run; }
    else { const to = run + (s.delta ?? 0); runs.push({ seg: s, from: run, to }); run = to; }
  }
  const maxV = Math.max(...runs.map((r) => Math.max(r.from, r.to)));
  const baseY = 820, topY = 300, H = baseY - topY;
  const SCALE = H / maxV;
  const n = segs.length;
  const x0 = 150, colW = 1620 / n, barW = Math.min(150, colW - 40);
  return (
    <Frame dur={dur} color={color}>
      <Head theme={T} kicker={kicker} title={title} color={color} o={rp(0, 0.08)} />
      {/* baseline */}
      <div style={{ position: "absolute", left: x0, top: baseY, width: 1620, height: 2, background: T.line }} />
      {runs.map((r, i) => {
        const at = 0.08 + i * 0.11;
        const o = rp(at, at + 0.09);
        const hi = Math.max(r.from, r.to), lo = Math.min(r.from, r.to);
        const barTop = baseY - hi * SCALE;
        const barH = (hi - lo) * SCALE * o;
        const cx = x0 + i * colW + (colW - barW) / 2;
        const isSub = r.seg.subtotal;
        const shown = r.seg.value ?? r.seg.delta ?? 0;
        return (
          <React.Fragment key={i}>
            {/* connector step line from previous top */}
            {i > 0 && (
              <div style={{ position: "absolute", left: x0 + (i - 1) * colW + (colW + barW) / 2, top: baseY - runs[i - 1].to * SCALE, width: colW - barW, height: 2, background: mix(T.line, r.seg.c, 0.4), opacity: o, borderTop: `2px dashed ${mix(T.line, r.seg.c, 0.5)}` }} />
            )}
            <div style={{
              position: "absolute", left: cx, top: barTop + (hi - Math.max(r.from, r.to)) * SCALE, width: barW, height: barH,
              borderRadius: isSub ? "10px 10px 0 0" : 8,
              background: isSub ? `linear-gradient(180deg, ${r.seg.c}, ${mix(r.seg.c, T.bg1, 0.5)})` : mix(T.panel, r.seg.c, 0.5),
              border: `2.5px solid ${r.seg.c}`, boxShadow: isSub ? `0 0 26px ${mix(T.bg0, r.seg.c, 0.4)}` : "none",
            }} />
            {/* value label above bar */}
            <div style={{ position: "absolute", left: cx - 30, top: barTop - 42, width: barW + 60, textAlign: "center", fontFamily: MONO, fontWeight: 800, fontSize: 27, color: r.seg.c, opacity: o }}>
              {shown < 0 ? "−" : ""}{fmt(Math.abs(shown), decimals)}
            </div>
            {/* line label under baseline */}
            <div style={{ position: "absolute", left: cx - 34, top: baseY + 14, width: barW + 68, textAlign: "center", fontFamily: SANS, fontWeight: isSub ? 800 : 600, fontSize: 20, color: isSub ? T.text : T.muted, opacity: o, lineHeight: 1.2 }}>{r.seg.label}</div>
          </React.Fragment>
        );
      })}
      <div style={{ position: "absolute", left: 150, top: 214, fontFamily: MONO, fontSize: 21, color: T.muted, opacity: rp(0.1, 0.2) }}>all figures in {unit}</div>
      {note && (
        <div style={{ position: "absolute", left: 150, top: 872, width: 1620, textAlign: "center", fontFamily: MONO, fontSize: 21, color: T.muted, opacity: rp(0.7, 0.82) }}>{note}</div>
      )}
    </Frame>
  );
};

// ================================================================ FORMULA CALCULATOR (ADEPT · E + T)
// Shows name = (num) / (den), then plugs numbers, then a live-counting result.
type Term = { label: string; val: number; c: string };
const FormulaScene: React.FC<{
  dur?: number; kicker?: string; title?: string; name?: string;
  num?: Term[]; den?: Term[]; op?: "÷" | "×" | "−";
  result?: { label: string; val: number; unit?: string; decimals?: number; c?: string; suffix?: string };
  note?: string; color?: string;
}> = ({
  dur, kicker = "THE FORMULA", title = "", name = "Ratio",
  num = [{ label: "Numerator", val: 100, c: A.profit }], den = [{ label: "Denominator", val: 50, c: A.rev }], op = "÷",
  result = { label: "Result", val: 2, unit: "×", decimals: 1, c: A.teal }, note = "", color = A.teal,
}) => {
  const rp = useReveal(dur);
  const rc = result.c || color;
  const cx = 960, topY = 300;
  const termRow = (terms: Term[], y: number, at: number) => (
    <div style={{ position: "absolute", left: cx - 620, top: y, width: 1240, display: "flex", justifyContent: "center", gap: 18, opacity: rp(at, at + 0.1) }}>
      {terms.map((t, i) => (
        <React.Fragment key={i}>
          {i > 0 && <span style={{ fontFamily: SANS, fontWeight: 800, fontSize: 40, color: T.muted, alignSelf: "center" }}>+</span>}
          <div style={{ background: mix(T.panel, t.c, 0.12), border: `2.5px solid ${t.c}`, borderRadius: 14, padding: "14px 26px", textAlign: "center" }}>
            <div style={{ fontFamily: MONO, fontSize: 19, color: t.c, fontWeight: 700 }}>{t.label}</div>
            <div style={{ fontFamily: MONO, fontWeight: 800, fontSize: 38, color: T.text }}>{fmt(t.val, Number.isInteger(t.val) ? 0 : 2)}</div>
          </div>
        </React.Fragment>
      ))}
    </div>
  );
  return (
    <Frame dur={dur} color={color}>
      <Head theme={T} kicker={kicker} title={title} color={color} o={rp(0, 0.08)} />
      {/* name of the ratio */}
      <div style={{ position: "absolute", left: 0, right: 0, top: 220, textAlign: "center", opacity: rp(0.04, 0.14) }}>
        <span style={{ fontFamily: SANS, fontWeight: 800, fontSize: 44, color: rc, letterSpacing: -0.5 }}>{name}</span>
      </div>
      {termRow(num, topY, 0.16)}
      {/* divider between the two rows: a fraction bar for ÷, else the operator glyph */}
      {op === "÷" ? (
        <div style={{ position: "absolute", left: cx - 300, top: topY + 120, width: 600, height: 4, background: T.text, borderRadius: 2, opacity: rp(0.3, 0.4) }} />
      ) : (
        <div style={{ position: "absolute", left: 0, right: 0, top: topY + 98, textAlign: "center", fontFamily: SANS, fontWeight: 800, fontSize: 44, color: op === "−" ? A.cost : T.muted, opacity: rp(0.3, 0.4) }}>{op}</div>
      )}
      {termRow(den, topY + 150, 0.42)}
      {/* equals + result */}
      <div style={{ position: "absolute", left: 0, right: 0, top: topY + 330, textAlign: "center", opacity: rp(0.6, 0.72) }}>
        <span style={{ fontFamily: SANS, fontWeight: 800, fontSize: 48, color: T.muted }}>=&nbsp;&nbsp;</span>
        <span style={{ display: "inline-block", background: mix(T.panel, rc, 0.16), border: `3px solid ${rc}`, borderRadius: 18, padding: "16px 40px", boxShadow: `0 0 40px ${mix(T.bg0, rc, 0.3)}` }}>
          <Counter p={rp(0.62, 0.82)} to={result.val} decimals={result.decimals ?? 1} suffix={(result.suffix ?? "") + (result.unit ? " " + result.unit : "")} color={rc} size={64} comma />
        </span>
      </div>
      <div style={{ position: "absolute", left: 0, right: 0, top: topY + 452, textAlign: "center", fontFamily: SANS, fontSize: 26, color: T.text, opacity: rp(0.72, 0.84) }}>{result.label}</div>
      {note && (
        <div style={{ position: "absolute", left: 150, top: 878, width: 1620, textAlign: "center", fontFamily: MONO, fontSize: 21, color: T.muted, opacity: rp(0.78, 0.9) }}>{note}</div>
      )}
    </Frame>
  );
};

// ================================================================ COMPARISON BARS
type Bar = { label: string; val: number; c: string; note?: string };
const BarsScene: React.FC<{ dur?: number; kicker?: string; title?: string; unit?: string; bars?: Bar[]; decimals?: number; baseline?: { val: number; label: string }; note?: string; color?: string }> = ({
  dur, kicker = "COMPARE", title = "", unit = "", bars = [], decimals = 1, baseline, note = "", color = A.teal,
}) => {
  const rp = useReveal(dur);
  const maxV = Math.max(...bars.map((b) => b.val), baseline?.val ?? 0) * 1.15 || 1;
  const baseY = 800, topY = 300, H = baseY - topY;
  const n = bars.length;
  const x0 = 220, colW = Math.min(360, 1500 / n), barW = Math.min(200, colW - 70);
  return (
    <Frame dur={dur} color={color}>
      <Head theme={T} kicker={kicker} title={title} color={color} o={rp(0, 0.08)} />
      <div style={{ position: "absolute", left: x0 - 60, top: baseY, width: 1620, height: 2, background: T.line }} />
      {baseline && (
        <>
          <div style={{ position: "absolute", left: x0 - 60, top: baseY - baseline.val / maxV * H, width: n * colW + 40, height: 0, borderTop: `3px dashed ${A.gray}`, opacity: rp(0.5, 0.6) }} />
          <div style={{ position: "absolute", left: x0 - 60 + n * colW - 20, top: baseY - baseline.val / maxV * H - 30, fontFamily: MONO, fontSize: 20, color: A.gray, opacity: rp(0.52, 0.62) }}>{baseline.label}</div>
        </>
      )}
      {bars.map((b, i) => {
        const at = 0.1 + i * 0.13;
        const grow = rp(at, at + 0.14);
        const h = b.val / maxV * H * grow;
        const cx = x0 + i * colW + (colW - barW) / 2;
        return (
          <React.Fragment key={i}>
            <div style={{ position: "absolute", left: cx, top: baseY - h, width: barW, height: h, borderRadius: "12px 12px 0 0", background: `linear-gradient(180deg, ${b.c}, ${mix(b.c, T.bg1, 0.5)})`, border: `2.5px solid ${b.c}`, borderBottom: "none", boxShadow: `0 0 26px ${mix(T.bg0, b.c, 0.3)}` }} />
            <div style={{ position: "absolute", left: cx - 40, top: baseY - h - 48, width: barW + 80, textAlign: "center", fontFamily: MONO, fontWeight: 800, fontSize: 34, color: b.c, opacity: grow }}>{fmt(b.val, decimals)}{unit}</div>
            <div style={{ position: "absolute", left: cx - 50, top: baseY + 16, width: barW + 100, textAlign: "center", fontFamily: SANS, fontWeight: 700, fontSize: 25, color: T.text, opacity: grow }}>{b.label}</div>
            {b.note && <div style={{ position: "absolute", left: cx - 50, top: baseY + 52, width: barW + 100, textAlign: "center", fontFamily: MONO, fontSize: 19, color: T.muted, opacity: grow }}>{b.note}</div>}
          </React.Fragment>
        );
      })}
      {note && <div style={{ position: "absolute", left: 150, top: 872, width: 1620, textAlign: "center", fontFamily: MONO, fontSize: 21, color: T.muted, opacity: rp(0.74, 0.86) }}>{note}</div>}
    </Frame>
  );
};

// ================================================================ GAUGE / METER
type Zone = { to: number; c: string; label?: string };
const GaugeScene: React.FC<{ dur?: number; kicker?: string; title?: string; value?: number; min?: number; max?: number; unit?: string; zones?: Zone[]; caption?: string; note?: string; color?: string }> = ({
  dur, kicker = "THE METER", title = "", value = 50, min = 0, max = 100, unit = "%", zones = [{ to: 33, c: A.cost, label: "weak" }, { to: 66, c: A.debt, label: "ok" }, { to: 100, c: A.profit, label: "strong" }], caption = "", note = "", color = A.teal,
}) => {
  const rp = useReveal(dur);
  const cx = 960, cy = 620, R = 300;
  const a0 = Math.PI, a1 = 0; // 180°→0°
  const frac = Math.max(0, Math.min(1, (value - min) / (max - min)));
  const needleA = a0 + (a1 - a0) * frac * rp(0.35, 0.72);
  const arc = (f0: number, f1: number, col: string, w: number) => {
    const s = a0 + (a1 - a0) * f0, e = a0 + (a1 - a0) * f1;
    const x1 = cx + Math.cos(s) * R, y1 = cy - Math.sin(s) * R;
    const x2 = cx + Math.cos(e) * R, y2 = cy - Math.sin(e) * R;
    return <path d={`M ${x1} ${y1} A ${R} ${R} 0 0 1 ${x2} ${y2}`} fill="none" stroke={col} strokeWidth={w} strokeLinecap="round" />;
  };
  let prev = 0;
  return (
    <Frame dur={dur} color={color}>
      <Head theme={T} kicker={kicker} title={title} color={color} o={rp(0, 0.08)} />
      <svg style={{ position: "absolute", left: 0, top: 0, overflow: "visible" }} width={1920} height={1080}>
        {arc(0, 1, T.line, 40)}
        {zones.map((z, i) => {
          const f0 = prev, f1 = (z.to - min) / (max - min); prev = f1;
          return <g key={i} opacity={rp(0.12 + i * 0.08, 0.24 + i * 0.08)}>{arc(f0, f1, z.c, 40)}</g>;
        })}
        {/* needle */}
        <line x1={cx} y1={cy} x2={cx + Math.cos(needleA) * (R - 24)} y2={cy - Math.sin(needleA) * (R - 24)} stroke={T.text} strokeWidth={7} strokeLinecap="round" />
        <circle cx={cx} cy={cy} r={16} fill={color} />
      </svg>
      {/* zone labels */}
      {zones.map((z, i) => {
        const f0 = i === 0 ? 0 : (zones[i - 1].to - min) / (max - min);
        const f1 = (z.to - min) / (max - min); const fm = (f0 + f1) / 2;
        const a = a0 + (a1 - a0) * fm;
        return z.label ? <div key={i} style={{ position: "absolute", left: cx + Math.cos(a) * (R + 46) - 50, top: cy - Math.sin(a) * (R + 46) - 16, width: 100, textAlign: "center", fontFamily: MONO, fontSize: 20, color: z.c, opacity: rp(0.3, 0.42) }}>{z.label}</div> : null;
      })}
      {/* value readout */}
      <div style={{ position: "absolute", left: 0, right: 0, top: cy + 40, textAlign: "center", opacity: rp(0.4, 0.55) }}>
        <Counter p={rp(0.4, 0.72)} to={value} decimals={Number.isInteger(value) ? 0 : 2} suffix={unit} color={color} size={92} />
      </div>
      {caption && <div style={{ position: "absolute", left: 0, right: 0, top: cy + 150, textAlign: "center", fontFamily: SANS, fontSize: 28, color: T.text, opacity: rp(0.6, 0.74) }}>{caption}</div>}
      {note && <div style={{ position: "absolute", left: 150, top: 878, width: 1620, textAlign: "center", fontFamily: MONO, fontSize: 21, color: T.muted, opacity: rp(0.76, 0.88) }}>{note}</div>}
    </Frame>
  );
};

// ================================================================ LEDGER (statement rows)
type Row = { label: string; val?: string; c?: string; indent?: number; bold?: boolean; rule?: boolean };
const LedgerScene: React.FC<{ dur?: number; kicker?: string; title?: string; rows?: Row[]; caption?: string; color?: string }> = ({
  dur, kicker = "THE STATEMENT", title = "", rows = [], caption = "", color = A.teal,
}) => {
  const rp = useReveal(dur);
  const x0 = 360, w = 1200, y0 = 250, rowH = Math.min(74, (640) / Math.max(1, rows.length));
  return (
    <Frame dur={dur} color={color}>
      <Head theme={T} kicker={kicker} title={title} color={color} o={rp(0, 0.08)} />
      <Card theme={T} x={x0 - 30} y={y0 - 30} w={w + 60} h={rows.length * rowH + 60} color={color} o={rp(0.04, 0.14)} pad="0">
        <span />
      </Card>
      {rows.map((r, i) => {
        const at = 0.1 + i * (0.62 / Math.max(1, rows.length));
        const o = rp(at, at + 0.1);
        const rc = r.c || (r.bold ? color : T.text);
        const y = y0 + i * rowH;
        return (
          <React.Fragment key={i}>
            <div style={{ position: "absolute", left: x0 + (r.indent ?? 0) * 34, top: y, width: w - (r.indent ?? 0) * 34, opacity: o, display: "flex", justifyContent: "space-between", alignItems: "baseline", borderTop: r.rule ? `2px solid ${mix(T.line, color, 0.5)}` : "none", paddingTop: r.rule ? 10 : 0 }}>
              <span style={{ fontFamily: SANS, fontWeight: r.bold ? 800 : 500, fontSize: r.bold ? 30 : 26, color: r.bold ? rc : T.text }}>{r.label}</span>
              {r.val !== undefined && <span style={{ fontFamily: MONO, fontWeight: r.bold ? 800 : 600, fontSize: r.bold ? 30 : 26, color: rc }}>{r.val}</span>}
            </div>
          </React.Fragment>
        );
      })}
      {caption && <div style={{ position: "absolute", left: 150, top: 872, width: 1620, textAlign: "center", fontFamily: MONO, fontSize: 21, color: T.muted, opacity: rp(0.76, 0.88) }}>{caption}</div>}
    </Frame>
  );
};

// ================================================================ STACK (EV build-up / capital stack)
type StackSeg = { label: string; val: number; c: string; op?: "+" | "−" | "=" };
const StackScene: React.FC<{ dur?: number; kicker?: string; title?: string; unit?: string; segs?: StackSeg[]; result?: { label: string; val: number; c: string }; note?: string; color?: string; decimals?: number }> = ({
  dur, kicker = "BUILD IT UP", title = "", unit = "₹ Cr", segs = [], result, note = "", color = A.val, decimals = 0,
}) => {
  const rp = useReveal(dur);
  const x0 = 220, y0 = 280, rowH = 96, w = 760;
  const maxV = Math.max(...segs.map((s) => Math.abs(s.val)), result ? Math.abs(result.val) : 0) || 1;
  return (
    <Frame dur={dur} color={color}>
      <Head theme={T} kicker={kicker} title={title} color={color} o={rp(0, 0.08)} />
      {segs.map((s, i) => {
        const at = 0.1 + i * 0.14;
        const o = rp(at, at + 0.12);
        const y = y0 + i * rowH;
        const bw = Math.max(6, Math.abs(s.val) / maxV * 900 * o);   // magnitude cue (under the label)
        return (
          <React.Fragment key={i}>
            {s.op && <div style={{ position: "absolute", left: x0 - 74, top: y + 2, fontFamily: SANS, fontWeight: 800, fontSize: 48, color: s.op === "−" ? A.cost : s.op === "=" ? A.profit : T.muted, opacity: o }}>{s.op}</div>}
            {/* label in LIGHT text at a fixed position — never dark-on-dark */}
            <div style={{ position: "absolute", left: x0, top: y, fontFamily: SANS, fontWeight: 700, fontSize: 28, color: T.text, opacity: o, whiteSpace: "nowrap" }}>{s.label}</div>
            {/* proportional magnitude bar UNDER the label */}
            <div style={{ position: "absolute", left: x0, top: y + 44, width: bw, height: 10, borderRadius: 6, background: `linear-gradient(90deg, ${s.c}, ${mix(s.c, T.bg1, 0.4)})`, boxShadow: `0 0 14px ${mix(T.bg0, s.c, 0.5)}`, opacity: o }} />
            <div style={{ position: "absolute", left: x0 + 980, top: y + 6, width: 340, textAlign: "right", fontFamily: MONO, fontWeight: 800, fontSize: 34, color: s.c, opacity: o }}>{s.val < 0 ? "−" : ""}{fmt(Math.abs(s.val), decimals)} {unit}</div>
          </React.Fragment>
        );
      })}
      {result && (
        <div style={{ position: "absolute", left: x0, top: y0 + segs.length * rowH + 18, width: 1320, opacity: rp(0.66, 0.8), display: "flex", alignItems: "center", gap: 24, borderTop: `3px solid ${result.c}`, paddingTop: 22 }}>
          <span style={{ fontFamily: SANS, fontWeight: 800, fontSize: 38, color: T.text }}>{result.label}</span>
          <span style={{ fontFamily: MONO, fontWeight: 800, fontSize: 46, color: result.c, marginLeft: "auto" }}>{fmt(result.val, decimals)} {unit}</span>
        </div>
      )}
      {note && <div style={{ position: "absolute", left: 150, top: 878, width: 1620, textAlign: "center", fontFamily: MONO, fontSize: 21, color: T.muted, opacity: rp(0.78, 0.9) }}>{note}</div>}
    </Frame>
  );
};

// ================================================================ DUPONT (product chain)
type Factor = { name: string; val: number; unit?: string; c: string; decimals?: number };
const DupontScene: React.FC<{ dur?: number; kicker?: string; title?: string; factors?: Factor[]; result?: { name: string; val: number; unit?: string; c?: string; decimals?: number }; note?: string; color?: string }> = ({
  dur, kicker = "DECOMPOSE IT", title = "", factors = [], result, note = "", color = A.teal,
}) => {
  const rp = useReveal(dur);
  const n = factors.length;
  const y = 420, x0 = 150, gap = 60;
  const boxW = Math.min(360, (1620 - (n - 1) * gap) / n);
  return (
    <Frame dur={dur} color={color}>
      <Head theme={T} kicker={kicker} title={title} color={color} o={rp(0, 0.08)} />
      {factors.map((f, i) => {
        const at = 0.12 + i * 0.14;
        const o = rp(at, at + 0.1);
        const x = x0 + i * (boxW + gap);
        return (
          <React.Fragment key={i}>
            {i > 0 && <div style={{ position: "absolute", left: x - gap, top: y + 70, width: gap, textAlign: "center", fontFamily: SANS, fontWeight: 800, fontSize: 46, color: T.muted, opacity: o }}>×</div>}
            <Card theme={T} x={x} y={y} w={boxW} h={190} color={f.c} o={o} pad="22px 20px" glow>
              <div style={{ fontFamily: MONO, fontSize: 19, color: f.c, fontWeight: 700, textAlign: "center", minHeight: 46 }}>{f.name}</div>
              <div style={{ textAlign: "center", marginTop: 14 }}>
                <Counter p={rp(at + 0.02, at + 0.14)} to={f.val} decimals={f.decimals ?? (Number.isInteger(f.val) ? 0 : 2)} suffix={f.unit ? " " + f.unit : ""} color={T.text} size={48} />
              </div>
            </Card>
          </React.Fragment>
        );
      })}
      {result && (
        <div style={{ position: "absolute", left: 0, right: 0, top: y + 260, textAlign: "center", opacity: rp(0.64, 0.78) }}>
          <span style={{ fontFamily: SANS, fontWeight: 800, fontSize: 44, color: T.muted }}>=&nbsp;&nbsp;</span>
          <span style={{ display: "inline-block", background: mix(T.panel, result.c || color, 0.16), border: `3px solid ${result.c || color}`, borderRadius: 18, padding: "14px 40px" }}>
            <Counter p={rp(0.66, 0.82)} to={result.val} decimals={result.decimals ?? 1} suffix={result.unit ? " " + result.unit : ""} color={result.c || color} size={58} />
          </span>
          <div style={{ fontFamily: SANS, fontWeight: 700, fontSize: 30, color: T.text, marginTop: 20 }}>{result.name}</div>
        </div>
      )}
      {note && <div style={{ position: "absolute", left: 150, top: 878, width: 1620, textAlign: "center", fontFamily: MONO, fontSize: 21, color: T.muted, opacity: rp(0.8, 0.92) }}>{note}</div>}
    </Frame>
  );
};

// ================================================================ QUADRANT (2×2)
type Pt = { x: number; y: number; label: string; c: string };
const QuadrantScene: React.FC<{ dur?: number; kicker?: string; title?: string; xlab?: string; ylab?: string; xlo?: string; xhi?: string; ylo?: string; yhi?: string; points?: Pt[]; note?: string; color?: string }> = ({
  dur, kicker = "THE MAP", title = "", xlab = "X", ylab = "Y", xlo = "", xhi = "", ylo = "", yhi = "", points = [], note = "", color = A.teal,
}) => {
  const rp = useReveal(dur);
  const cx0 = 560, cy0 = 236, PW = 900, PH = 470; // plot box
  return (
    <Frame dur={dur} color={color}>
      <Head theme={T} kicker={kicker} title={title} color={color} o={rp(0, 0.08)} />
      {/* axes */}
      <div style={{ position: "absolute", left: cx0, top: cy0 + PH / 2, width: PW, height: 2, background: T.line, opacity: rp(0.06, 0.16) }} />
      <div style={{ position: "absolute", left: cx0 + PW / 2, top: cy0, width: 2, height: PH, background: T.line, opacity: rp(0.06, 0.16) }} />
      {/* axis labels */}
      <div style={{ position: "absolute", left: cx0 + PW / 2 - 60, top: cy0 + PH + 16, fontFamily: MONO, fontSize: 22, color: color, opacity: rp(0.1, 0.2) }}>→ {xhi}</div>
      <div style={{ position: "absolute", left: cx0 - 40, top: cy0 - 44, fontFamily: MONO, fontSize: 22, color: color, opacity: rp(0.1, 0.2) }}>↑ {ylab}</div>
      <div style={{ position: "absolute", left: cx0 - 4, top: cy0 + PH + 16, fontFamily: MONO, fontSize: 18, color: T.muted, opacity: rp(0.12, 0.22) }}>{xlo}</div>
      {points.map((pt, i) => {
        const at = 0.2 + i * 0.14;
        const o = rp(at, at + 0.12);
        const px = cx0 + pt.x * PW, py = cy0 + (1 - pt.y) * PH;
        return (
          <React.Fragment key={i}>
            <div style={{ position: "absolute", left: px - 16, top: py - 16, width: 32, height: 32, borderRadius: 20, background: pt.c, border: `3px solid ${T.text}`, opacity: o, boxShadow: `0 0 20px ${pt.c}` }} />
            <div style={{ position: "absolute", left: px + 24, top: py - 20, width: 320, fontFamily: SANS, fontWeight: 700, fontSize: 25, color: pt.c, opacity: o }}>{pt.label}</div>
          </React.Fragment>
        );
      })}
      {note && <div style={{ position: "absolute", left: 150, top: 878, width: 1620, textAlign: "center", fontFamily: MONO, fontSize: 21, color: T.muted, opacity: rp(0.78, 0.9) }}>{note}</div>}
    </Frame>
  );
};

// ================================================================ COMPARE (company cards)
type Co = { name: string; c: string; tag?: string; stats: { k: string; v: string; hot?: boolean }[] };
const CompareScene: React.FC<{ dur?: number; kicker?: string; title?: string; cos?: Co[]; note?: string; color?: string }> = ({
  dur, kicker = "SIDE BY SIDE", title = "", cos = [], note = "", color = A.teal,
}) => {
  const rp = useReveal(dur);
  const n = cos.length;
  const x0 = 150, gap = 40, cardW = Math.min(520, (1620 - (n - 1) * gap) / n), cardY = 250, cardH = 560;
  return (
    <Frame dur={dur} color={color}>
      <Head theme={T} kicker={kicker} title={title} color={color} o={rp(0, 0.08)} />
      {cos.map((co, i) => {
        const at = 0.12 + i * 0.14;
        const o = rp(at, at + 0.12);
        const x = x0 + i * (cardW + gap);
        return (
          <Card key={i} theme={T} x={x} y={cardY} w={cardW} h={cardH} color={co.c} o={o} pad="26px 30px" glow>
            <div style={{ display: "flex", alignItems: "baseline", justifyContent: "space-between" }}>
              <span style={{ fontFamily: SANS, fontWeight: 800, fontSize: 34, color: co.c }}>{co.name}</span>
              {co.tag && <span style={{ fontFamily: MONO, fontSize: 18, color: T.muted }}>{co.tag}</span>}
            </div>
            <div style={{ height: 3, background: mix(T.line, co.c, 0.6), margin: "16px 0 8px" }} />
            {co.stats.map((s, j) => (
              <div key={j} style={{ display: "flex", justifyContent: "space-between", alignItems: "baseline", padding: "13px 0", borderBottom: `1px solid ${T.line}`, opacity: rp(at + 0.04 + j * 0.02, at + 0.14 + j * 0.02) }}>
                <span style={{ fontFamily: SANS, fontSize: 24, color: T.muted }}>{s.k}</span>
                <span style={{ fontFamily: MONO, fontWeight: 800, fontSize: 27, color: s.hot ? co.c : T.text }}>{s.v}</span>
              </div>
            ))}
          </Card>
        );
      })}
      {note && <div style={{ position: "absolute", left: 150, top: 838, width: 1620, textAlign: "center", fontFamily: MONO, fontSize: 21, color: T.muted, opacity: rp(0.76, 0.88) }}>{note}</div>}
    </Frame>
  );
};

// ================================================================ KEY IDEA (ADEPT · Plain English)
const KeyIdeaScene: React.FC<{ dur?: number; kicker?: string; big?: string; sub?: string; color?: string }> = ({
  dur, kicker = "IN PLAIN ENGLISH", big = "", sub = "", color = A.profit,
}) => {
  const frame = useCurrentFrame();
  const rp = useReveal(dur);
  return (
    <Frame dur={dur} color={color}>
      <Brackets x={230} y={330} w={1460} h={430} color={color} o={rp(0.04, 0.16)} len={54} />
      <div style={{ position: "absolute", left: 0, right: 0, top: 300, textAlign: "center", opacity: rp(0, 0.1) }}>
        <Kicker theme={T} text={kicker} color={color} cx />
      </div>
      <div style={{ position: "absolute", left: 230, right: 230, top: 400, textAlign: "center", fontFamily: SANS, fontWeight: 800, fontSize: 60, lineHeight: 1.24, letterSpacing: -1.2, color: T.text, opacity: rp(0.12, 0.32), transform: `translateY(${(1 - rp(0.12, 0.32)) * 18}px)` }}>{big}</div>
      {sub && <div style={{ position: "absolute", left: 300, right: 300, top: 690, textAlign: "center", fontFamily: SANS, fontSize: 32, color: mix(T.text, color, 0.4), fontStyle: "italic", opacity: rp(0.4, 0.6) }}>{sub}</div>}
      <div style={{ position: "absolute", left: 0, right: 0, top: 800, textAlign: "center", opacity: 0.5 + Math.sin(frame * 0.05) * 0.3 }}>
        <div style={{ display: "inline-block", width: 90, height: 4, background: color, borderRadius: 2 }} />
      </div>
    </Frame>
  );
};

// ================================================================ RECAP
const RecapScene: React.FC<{ dur?: number; kicker?: string; title?: string; items?: string[]; closer?: string; color?: string }> = ({
  dur, kicker = "RECAP — THE WHOLE MAP", title = "The chapter in one breath", items = [], closer = "", color = A.teal,
}) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const y0 = 300, rowH = Math.min(84, 520 / Math.max(1, items.length));
  return (
    <Frame dur={dur} color={color}>
      <div style={{ position: "absolute", left: 0, right: 0, top: 120, textAlign: "center", opacity: p(0, 0.06) }}>
        <Kicker theme={T} text={kicker} color={color} cx />
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 56, color: T.text, letterSpacing: -1.4, marginTop: 16, opacity: p(0.04, 0.14) }}>{title}</div>
      </div>
      {items.map((it, i) => {
        const at = 0.1 + i * 0.1;
        const o = p(at, at + 0.09);
        const y = y0 + i * rowH;
        return (
          <div key={i} style={{ position: "absolute", left: 300, top: y, width: 1320, opacity: o, transform: `translateX(${(1 - o) * 16}px)`, display: "flex", alignItems: "center", gap: 22 }}>
            <div style={{ width: 6, height: rowH - 24, background: color, borderRadius: 3 }} />
            <span style={{ fontFamily: MONO, fontWeight: 800, fontSize: 22, color, minWidth: 34 }}>{("0" + (i + 1)).slice(-2)}</span>
            <span style={{ fontFamily: SANS, fontWeight: 500, fontSize: 29, color: T.text }}>{it}</span>
          </div>
        );
      })}
      {closer && (
        <div style={{ position: "absolute", left: 260, right: 260, top: y0 + items.length * rowH + 30, textAlign: "center", fontFamily: SANS, fontWeight: 700, fontStyle: "italic", fontSize: 34, color: mix(T.text, color, 0.4), opacity: p(0.78, 0.9), textShadow: `0 0 30px ${mix(T.bg0, color, 0.4 + Math.sin(frame * 0.05) * 0.1)}` }}>{closer}</div>
      )}
    </Frame>
  );
};

// ================================================================ ROUTER
export const FAScene: React.FC<{ variant: string; [k: string]: unknown }> = ({ variant, ...props }) => {
  const v = variant.replace(/^fa_/, "");
  switch (v) {
    case "title": return <TitleScene {...props} />;
    case "divider": return <DividerScene {...props} />;
    case "roadmap": return <RoadmapScene {...props} />;
    case "analogy": return <AnalogyScene {...props} />;
    case "waterfall": return <WaterfallScene {...props} />;
    case "formula": return <FormulaScene {...props} />;
    case "bars": return <BarsScene {...props} />;
    case "gauge": return <GaugeScene {...props} />;
    case "ledger": return <LedgerScene {...props} />;
    case "stack": return <StackScene {...props} />;
    case "dupont": return <DupontScene {...props} />;
    case "quadrant": return <QuadrantScene {...props} />;
    case "compare": return <CompareScene {...props} />;
    case "keyidea": return <KeyIdeaScene {...props} />;
    case "recap": return <RecapScene {...props} />;
    default: return <TitleScene {...props} />;
  }
};

export default FAScene;
