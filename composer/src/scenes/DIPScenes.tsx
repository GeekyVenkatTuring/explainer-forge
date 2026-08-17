/**
 * DIPScenes.tsx — "The Macro-Dip Playbook: Buying Quality When the Market Falls"
 * Internal research / education. Prefix `dip`. ~11 min / 17 scenes. English (Neerja).
 *
 * A METHODOLOGY video, built deliberately WITHOUT specific per-stock buy calls or
 * unverified figures — because live per-stock data could not be reliably verified.
 * It teaches: last week's macro setup (qualitative, indicative), how each macro
 * factor transmits to sectors, how to tell a macro DIP from company DAMAGE, the
 * quality + valuation filters, the exact screen to run, and how to enter with risk
 * control. Any market number on screen is indicative context, not a precision claim.
 *
 * Identity: finance night-sky + candlestick + a DIP curve motif (fall → base).
 * Semantic accents (shared with TAC/IN videos):
 *   C #22D3EE cyan — price / structure / neutral data
 *   G #34D399 green — opportunity / quality / "buy zone"
 *   R #FB7185 rose — risk / trap / the falling move / "avoid"
 *   Y #FBBF24 amber — macro factors / caution
 *   V #A78BFA violet — method / concept labels
 */
import React from "react";
import { useCurrentFrame, interpolate } from "remotion";
import {
  makeTheme, mix, MONO, SANS, useP, usePop, rnd,
  Stage, Bg, Head, Foot, Wire, Flow, Type, ScanBeam, Brackets,
} from "../lib/primitives";

const T = makeTheme({});
const C = "#22D3EE", G = "#34D399", R = "#FB7185", Y = "#FBBF24", V = "#A78BFA";
type OHLC = { o: number; c: number; h: number; l: number };

function fromClose(closes: number[], seed: number, wf = 0.16): OHLC[] {
  return closes.map((c2, i) => {
    const o = i === 0 ? c2 * 0.999 : closes[i - 1];
    const rng = Math.abs(c2 - o) + 1;
    return { o, c: c2, h: Math.max(o, c2) + rng * wf * rnd(i, 1, seed), l: Math.min(o, c2) - rng * wf * rnd(i, 2, seed) };
  });
}
function makePY(data: OHLC[], by: number, bh: number, pminF?: number, pmaxF?: number) {
  const pmin = pminF ?? Math.min(...data.map((k) => k.l));
  const pmax = pmaxF ?? Math.max(...data.map((k) => k.h));
  return (v: number) => by + ((pmax - v) / (pmax - pmin)) * bh;
}
function makeCX(n: number, bx: number, bw: number) { return (i: number) => bx + (i + 0.5) * (bw / n); }

const CandleChart: React.FC<{
  data: OHLC[]; nC: number; bx: number; by: number; bw: number; bh: number;
  upC?: string; dnC?: string; pminF?: number; pmaxF?: number;
}> = ({ data, nC, bx, by, bw, bh, upC = G, dnC = R, pminF, pmaxF }) => {
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
              borderRadius: 2, background: col }} />
          </React.Fragment>
        );
      })}
    </>
  );
};

// Falling-then-basing index series (the "dip" — used as case-study + motif)
const DIP_CLOSES = [252, 250, 246, 243, 241, 240, 240.5, 241, 240.5, 241.5];
const DIP_SERIES = fromClose(DIP_CLOSES, 31, 0.14);

// ── Transmission map: one macro hub → sector chips (hurt = rose, help = green)
const Transmission: React.FC<{
  dur: number; hub: string; hubSub: string; hubColor: string;
  hurt: string[]; help?: string[];
}> = ({ dur, hub, hubSub, hubColor, hurt, help = [] }) => {
  const p = useP(dur); const frame = useCurrentFrame();
  const hubX = 430, hubY = 520;
  const rows = [...hurt.map((l) => ({ l, kind: "hurt" as const })), ...help.map((l) => ({ l, kind: "help" as const }))];
  const n = rows.length;
  const listX = 1060, top = 250, rowH = Math.min(96, (760 - top) / n), chipH = rowH - 16;
  const hot = Math.floor(frame / 30) % n;
  return (
    <>
      {/* hub */}
      <div style={{ position: "absolute", left: hubX - 250, top: hubY - 120, width: 500, height: 240, borderRadius: 22,
        background: mix(T.bg1, hubColor, 0.08), border: `3px solid ${hubColor}`, padding: "28px 30px", boxSizing: "border-box",
        opacity: p(0.04, 0.14), boxShadow: `0 0 ${34 + Math.sin(frame * 0.06) * 12}px ${mix(T.bg0, hubColor, 0.4)}`,
        display: "flex", flexDirection: "column", justifyContent: "center" }}>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 44, color: hubColor, letterSpacing: -1 }}>{hub}</div>
        <div style={{ fontFamily: SANS, fontSize: 25, color: T.muted, marginTop: 12, lineHeight: 1.35 }}>{hubSub}</div>
      </div>
      {rows.map((r, i) => {
        const y = top + i * rowH + rowH / 2;
        const col = r.kind === "hurt" ? R : G;
        const at = 0.16 + i * 0.07;
        const isHot = hot === i && p(0.6, 0.61) > 0.5;
        return (
          <React.Fragment key={i}>
            <Wire x1={hubX + 250} y1={hubY} x2={listX} y2={y} p={p(at, at + 0.06)} color={mix(col, T.bg1, 0.3)} w={2} arrow={false} />
            {p(at + 0.05, at + 0.1) > 0.2 && <Flow x1={hubX + 250} y1={hubY} x2={listX} y2={y} color={col} n={4} o={p(at + 0.05, at + 0.12)} speed={0.014} />}
            <div style={{ position: "absolute", left: listX, top: y - chipH / 2, width: 720, height: chipH, borderRadius: 12,
              background: mix(T.panel, col, isHot ? 0.16 : 0.07), border: `2px solid ${mix(T.line, col, isHot ? 0.9 : 0.5)}`,
              display: "flex", alignItems: "center", gap: 16, padding: "0 22px", boxSizing: "border-box",
              opacity: p(at, at + 0.07), transform: `translateX(${(1 - p(at, at + 0.07)) * 22}px)` }}>
              <span style={{ fontFamily: MONO, fontWeight: 800, fontSize: 22, color: col }}>{r.kind === "hurt" ? "▼" : "▲"}</span>
              <span style={{ fontFamily: SANS, fontWeight: 600, fontSize: 25, color: T.text }}>{r.l}</span>
              <span style={{ marginLeft: "auto", fontFamily: MONO, fontSize: 19, color: col, letterSpacing: 1 }}>
                {r.kind === "hurt" ? "PRESSURED" : "BENEFITS"}</span>
            </div>
          </React.Fragment>
        );
      })}
    </>
  );
};

// ════════════════════════════════════════════ 1. TITLE
const TitleScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur); const frame = useCurrentFrame(); const pop = usePop(dur);
  // dip curve motif behind title
  const pts = Array.from({ length: 60 }).map((_, i) => {
    const t = i / 59;
    const y = 560 + (1 - Math.exp(-t * 3)) * 180 - Math.max(0, t - 0.6) * 220;
    return `${180 + t * 1560},${y}`;
  });
  const nDraw = Math.round(interpolate(p(0.1, 0.6), [0, 1], [0, 60]));
  return (
    <Stage>
      <Bg theme={T} accent={G} />
      <svg style={{ position: "absolute", left: 0, top: 0, overflow: "visible", opacity: 0.5 }} width={1920} height={1080}>
        <polyline points={pts.slice(0, nDraw).join(" ")} fill="none" stroke={mix(T.bg1, R, 0.6)} strokeWidth={4} />
      </svg>
      <div style={{ position: "absolute", left: 0, right: 0, top: 250, textAlign: "center",
        fontFamily: MONO, fontWeight: 800, fontSize: 22, color: G, letterSpacing: 10,
        opacity: p(0.04, 0.14) }}>INTERNAL RESEARCH · MARKET EDUCATION</div>
      <div style={{ position: "absolute", left: 0, right: 0, top: 300, textAlign: "center",
        fontFamily: SANS, fontWeight: 800, fontSize: 108, color: T.text, letterSpacing: -3,
        opacity: p(0.10, 0.22), transform: `scale(${0.92 + pop(0.10) * 0.08})` }}>THE MACRO-DIP</div>
      <div style={{ position: "absolute", left: 0, right: 0, top: 420, textAlign: "center",
        fontFamily: SANS, fontWeight: 800, fontSize: 128, letterSpacing: -4, color: G,
        textShadow: `0 0 60px ${mix(T.bg0, G, 0.7)}`,
        opacity: p(0.18, 0.32), transform: `scale(${0.92 + pop(0.18) * 0.08})` }}>PLAYBOOK</div>
      <div style={{ position: "absolute", left: "50%", top: 586, width: interpolate(p(0.28, 0.52), [0, 1], [0, 560]),
        height: 5, background: `linear-gradient(90deg, ${G}, ${mix(G, C, 0.5)})`, borderRadius: 3, transform: "translateX(-50%)" }} />
      <div style={{ position: "absolute", left: 260, right: 260, top: 616, textAlign: "center",
        fontFamily: SANS, fontSize: 35, color: T.muted, opacity: p(0.36, 0.54) }}>
        Telling a market-wide bargain from a value trap — when quality gets sold off
      </div>
      <div style={{ position: "absolute", left: 0, right: 0, top: 690, textAlign: "center",
        fontFamily: MONO, fontSize: 21, color: R, opacity: p(0.56, 0.70) }}>
        ⚠ Education only — not investment advice — market figures are indicative
      </div>
    </Stage>
  );
};

// ════════════════════════════════════════════ 2. DIVIDER
const DividerScene: React.FC<{ dur?: number; n?: number; title?: string; sub?: string; color?: string }> = ({
  dur, n = 1, title = "", sub = "", color = G,
}) => {
  const frame = useCurrentFrame(); const p = useP(dur);
  return (
    <Stage>
      <Bg theme={T} accent={color} />
      <Brackets x={330} y={290} w={1260} h={500} color={color} o={p(0.02, 0.14)} len={54} />
      <ScanBeam theme={T} x={340} y={300} w={1240} h={480} color={color} o={p(0.05, 0.18)} speed={1.5} />
      <div style={{ position: "absolute", left: 0, right: 0, top: 356, textAlign: "center" }}>
        <div style={{ fontFamily: MONO, fontWeight: 800, fontSize: 30, color, letterSpacing: 10, opacity: p(0.05, 0.16) }}>PART {String(n).padStart(2, "0")}</div>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 88, color: T.text, letterSpacing: -2,
          marginTop: 16, opacity: p(0.12, 0.26), transform: `translateY(${(1 - p(0.12, 0.26)) * 28}px)` }}>{title}</div>
        <div style={{ height: 5, width: interpolate(p(0.22, 0.52), [0, 1], [0, 460]), background: color, borderRadius: 3, margin: "22px auto" }} />
        <div style={{ fontFamily: SANS, fontSize: 32, color: T.muted, opacity: p(0.32, 0.48) }}>{sub}</div>
      </div>
      <div style={{ position: "absolute", left: 0, right: 0, top: 858, display: "flex", justifyContent: "center", gap: 14, opacity: p(0.32, 0.48) }}>
        {[1, 2].map((i) => (
          <div key={i} style={{ width: i === n ? 44 : 14, height: 14, borderRadius: 8,
            background: i <= n ? color : mix(T.panel, color, 0.15), border: `1.5px solid ${i <= n ? color : T.line}`,
            opacity: i === n ? 0.7 + Math.sin(frame * 0.1) * 0.3 : 1 }} />
        ))}
      </div>
    </Stage>
  );
};

// ════════════════════════════════════════════ 3. THESIS (hook)
const ThesisScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur); const frame = useCurrentFrame();
  const bx = 130, by = 250, bw = 760, bh = 470;
  const nC = Math.round(interpolate(p(0.12, 0.5), [0, 1], [0, DIP_SERIES.length]));
  return (
    <Stage>
      <Bg theme={T} accent={G} />
      <Head theme={T} kicker="THE IDEA" title="When the Tide Goes Out, Good Boats Sink Too" color={G} />
      {/* left: the whole market dips */}
      <div style={{ position: "absolute", left: bx, top: by, width: bw, height: bh, borderRadius: 14,
        background: mix(T.bg1, C, 0.03), border: `2px solid ${mix(T.line, C, 0.4)}`, opacity: p(0.04, 0.12) }} />
      <CandleChart data={DIP_SERIES} nC={nC} bx={bx} by={by} bw={bw} bh={bh} pminF={236} pmaxF={254} />
      <div style={{ position: "absolute", left: bx, top: by + bh + 16, width: bw, fontFamily: MONO, fontSize: 21,
        color: R, opacity: p(0.42, 0.5) }}>A market-wide sell-off drags EVERYTHING down together</div>
      {/* right: two outcomes */}
      {[
        { c: G, tag: "MACRO DIP", sub: "Quality fell for reasons that have nothing to do with the business.", label: "OPPORTUNITY", at: 0.52 },
        { c: R, tag: "COMPANY DAMAGE", sub: "It fell because something is genuinely wrong with the company.", label: "VALUE TRAP", at: 0.68 },
      ].map((o, i) => (
        <div key={i} style={{ position: "absolute", left: 960, top: 258 + i * 236, width: 820, height: 208, borderRadius: 18,
          background: mix(T.bg1, o.c, 0.06), border: `2.5px solid ${o.c}`, padding: "24px 30px", boxSizing: "border-box",
          opacity: p(o.at, o.at + 0.1), boxShadow: `0 0 ${20 + Math.sin(frame * 0.06) * 8}px ${mix(T.bg0, o.c, 0.25)}` }}>
          <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between" }}>
            <span style={{ fontFamily: MONO, fontWeight: 800, fontSize: 26, color: o.c, letterSpacing: 2 }}>{o.tag}</span>
            <span style={{ fontFamily: MONO, fontWeight: 800, fontSize: 22, color: T.bg0, background: o.c, borderRadius: 8, padding: "4px 14px" }}>{o.label}</span>
          </div>
          <div style={{ fontFamily: SANS, fontSize: 27, color: T.text, marginTop: 18, lineHeight: 1.4 }}>{o.sub}</div>
        </div>
      ))}
      <Foot theme={T} p={p(0.85, 0.94)}>The whole game is telling these two apart. Buy the first. Never buy the second just because it's cheap.</Foot>
    </Stage>
  );
};

// ════════════════════════════════════════════ 4. LAST WEEK'S SETUP
const SetupScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur); const frame = useCurrentFrame();
  const bx = 130, by = 250, bw = 820, bh = 480;
  const nC = Math.round(interpolate(p(0.1, 0.5), [0, 1], [0, DIP_SERIES.length]));
  const factors = [
    { e: "🛢️", t: "Crude near $100", at: 0.30 },
    { e: "₹", t: "Rupee past ~96/$", at: 0.40 },
    { e: "📤", t: "FIIs net sellers", at: 0.50 },
    { e: "⚔️", t: "War / geopolitics", at: 0.60 },
    { e: "🇺🇸", t: "US curbs on IT", at: 0.70 },
  ];
  return (
    <Stage>
      <Bg theme={T} accent={Y} />
      <Head theme={T} kicker="THE CASE STUDY — LAST WEEK" title="Five Macro Forces Hit at Once" color={Y} />
      <div style={{ position: "absolute", left: bx, top: by, width: bw, height: bh, borderRadius: 14,
        background: mix(T.bg1, C, 0.03), border: `2px solid ${mix(T.line, C, 0.4)}`, opacity: p(0.04, 0.12) }} />
      <CandleChart data={DIP_SERIES} nC={nC} bx={bx} by={by} bw={bw} bh={bh} pminF={236} pmaxF={254} />
      <div style={{ position: "absolute", left: bx, top: by + bh + 14, width: bw, fontFamily: MONO, fontSize: 21,
        color: R, opacity: p(0.2, 0.3) }}>~2–3% over five sessions · worst week in months (indicative)</div>
      {factors.map((f, i) => {
        const lo = p(f.at, f.at + 0.08);
        return (
          <div key={i} style={{ position: "absolute", left: 1010, top: 258 + i * 96, width: 780, height: 80, borderRadius: 14,
            background: mix(T.panel, Y, 0.06), border: `2px solid ${mix(T.line, Y, 0.5)}`, display: "flex", alignItems: "center",
            gap: 20, padding: "0 26px", boxSizing: "border-box", opacity: lo, transform: `translateX(${(1 - lo) * 22}px)` }}>
            <span style={{ fontSize: 36 }}>{f.e}</span>
            <span style={{ fontFamily: SANS, fontWeight: 700, fontSize: 28, color: T.text }}>{f.t}</span>
          </div>
        );
      })}
      <Foot theme={T} p={p(0.85, 0.94)}>None of these is about any single company. That's the tell — a macro-wide sell-off, not a business problem.</Foot>
    </Stage>
  );
};

// ════════════════════════════════════════════ 5-9. TRANSMISSION SCENES
const CrudeScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur);
  return (
    <Stage>
      <Bg theme={T} accent={Y} />
      <Head theme={T} kicker="FACTOR 1 — CRUDE NEAR $100" title="Expensive Oil Squeezes the Importers" color={Y} />
      <Transmission dur={dur ?? 30} hub="Brent ≈ $100 ▲" hubSub="A costlier barrel raises input & fuel bills across the economy."
        hubColor={Y}
        hurt={["Oil marketing — BPCL, HPCL, IOC", "Paints & tyres (crude derivatives)", "Aviation & logistics (fuel)"]}
        help={["Upstream producers — ONGC, Oil India"]} />
      <Foot theme={T} p={p(0.85, 0.94)}>Ask: is the crude spike temporary (geopolitical) or structural? Temporary spikes are where quality importers get mispriced.</Foot>
    </Stage>
  );
};
const RupeeScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur);
  return (
    <Stage>
      <Bg theme={T} accent={Y} />
      <Head theme={T} kicker="FACTOR 2 — A WEAKER RUPEE" title="A Falling Rupee Cuts Both Ways" color={Y} />
      <Transmission dur={dur ?? 30} hub="USD/INR past ~96 ▲" hubSub="Imports cost more; export earnings convert to more rupees."
        hubColor={Y}
        hurt={["Importers — oil, capital goods", "Companies with dollar debt"]}
        help={["Exporters — IT services", "Pharma & specialty chemicals"]} />
      <Foot theme={T} p={p(0.85, 0.94)}>A weak rupee is a TAILWIND for IT — yet IT still fell. That contradiction is the clue we chase in Factor 5.</Foot>
    </Stage>
  );
};
const FiiScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur);
  return (
    <Stage>
      <Bg theme={T} accent={R} />
      <Head theme={T} kicker="FACTOR 3 — FII SELLING" title="Foreign Selling Is Indiscriminate" color={R} />
      <Transmission dur={dur ?? 30} hub="FIIs net sellers ▼" hubSub="They sell what they OWN and what's liquid — not what's overvalued."
        hubColor={R}
        hurt={["Index heavyweights & high-FII names", "Private banks & financials", "Large-cap leaders in every sector"]}
        help={["DIIs often absorb the selling"]} />
      <Foot theme={T} p={p(0.85, 0.94)}>This is the richest hunting ground: FIIs sell great businesses simply because they're big and liquid — fundamentals intact.</Foot>
    </Stage>
  );
};
const WarScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur);
  return (
    <Stage>
      <Bg theme={T} accent={R} />
      <Head theme={T} kicker="FACTOR 4 — WAR & GEOPOLITICS" title="Fear Is Loud, but Usually Temporary" color={R} />
      <Transmission dur={dur ?? 30} hub="Geopolitical risk ▲" hubSub="Uncertainty triggers risk-off selling and a volatility spike."
        hubColor={R}
        hurt={["Broad risk-off — most sectors dip", "High-beta & cyclical names"]}
        help={["Defence & defensives", "Gold and safe-havens"]} />
      <Foot theme={T} p={p(0.85, 0.94)}>Markets price fear fast and forgive it slowly. If the conflict doesn't hit a company's actual earnings, the dip tends to mean-revert.</Foot>
    </Stage>
  );
};
const UsItScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur); const frame = useCurrentFrame();
  return (
    <Stage>
      <Bg theme={T} accent={V} />
      <Head theme={T} kicker="FACTOR 5 — US CURBS ON IT" title="Is It a Dip… or a Re-Rating?" color={V} />
      {/* two interpretations side by side — the critical nuance */}
      {[
        { c: G, tag: "IF TEMPORARY", pts: ["A one-off cost / policy scare", "Earnings power intact", "→ a genuine macro DIP to buy"], at: 0.14 },
        { c: R, tag: "IF STRUCTURAL", pts: ["The business model is impaired", "Lower growth for years", "→ a re-rating, NOT a dip"], at: 0.34 },
      ].map((b, i) => {
        const lo = p(b.at, b.at + 0.1);
        return (
          <div key={i} style={{ position: "absolute", left: 130 + i * 850, top: 258, width: 790, height: 420, borderRadius: 20,
            background: mix(T.bg1, b.c, 0.05), border: `2.5px solid ${b.c}`, padding: "30px 34px", boxSizing: "border-box",
            opacity: lo, transform: `translateY(${(1 - lo) * 20}px)` }}>
            <div style={{ fontFamily: MONO, fontWeight: 800, fontSize: 26, color: b.c, letterSpacing: 2 }}>{b.tag}</div>
            <div style={{ height: 2, background: mix(T.line, b.c, 0.5), margin: "20px 0" }} />
            {b.pts.map((pt, j) => (
              <div key={j} style={{ display: "flex", gap: 14, marginBottom: 22, opacity: p(b.at + 0.06 + j * 0.05, b.at + 0.12 + j * 0.05) }}>
                <span style={{ fontFamily: MONO, fontWeight: 800, color: b.c, fontSize: 26 }}>•</span>
                <span style={{ fontFamily: SANS, fontSize: 27, color: T.text, lineHeight: 1.35 }}>{pt}</span>
              </div>
            ))}
          </div>
        );
      })}
      <div style={{ position: "absolute", left: 130, top: 706, width: 1660, textAlign: "center", fontFamily: MONO, fontWeight: 800,
        fontSize: 26, color: V, opacity: 0.6 + Math.sin(frame * 0.08) * 0.35 }}>
        The whole art of dip-buying lives in this one distinction.
      </div>
      <Foot theme={T} p={p(0.86, 0.94)}>US IT curbs may be structural — so treat IT with caution. A cheap price doesn't help if earnings power is permanently lower.</Foot>
    </Stage>
  );
};

// ════════════════════════════════════════════ 10. DIP vs DAMAGE (hero)
const DipVsTrapScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur); const frame = useCurrentFrame();
  const dip = ["The whole sector / market fell together", "No company-specific bad news", "Earnings & guidance intact", "Trigger is external & likely temporary", "Balance sheet unchanged"];
  const dmg = ["Only THIS stock fell hard", "Earnings miss or guidance cut", "Governance / accounting red flags", "A permanent shift in the business", "Rising debt or cash-flow stress"];
  return (
    <Stage>
      <Bg theme={T} accent={G} />
      <Head theme={T} kicker="THE ONE DISTINCTION THAT MATTERS" title="Macro Dip vs Company Damage" color={G} />
      {[
        { c: G, title: "✓ MACRO DIP — a candidate", items: dip, x: 130 },
        { c: R, title: "✗ COMPANY DAMAGE — avoid", items: dmg, x: 990 },
      ].map((col, ci) => (
        <div key={ci} style={{ position: "absolute", left: col.x, top: 236, width: 800, height: 560, borderRadius: 20,
          background: mix(T.bg1, col.c, 0.05), border: `2.5px solid ${col.c}`, padding: "26px 30px", boxSizing: "border-box",
          opacity: p(0.04 + ci * 0.06, 0.14 + ci * 0.06) }}>
          <div style={{ fontFamily: MONO, fontWeight: 800, fontSize: 26, color: col.c, letterSpacing: 1, marginBottom: 12 }}>{col.title}</div>
          {col.items.map((it, i) => {
            const at = 0.16 + ci * 0.04 + i * 0.07;
            return (
              <div key={i} style={{ display: "flex", gap: 14, alignItems: "flex-start", marginTop: 20,
                opacity: p(at, at + 0.06), transform: `translateX(${(1 - p(at, at + 0.06)) * 18}px)` }}>
                <span style={{ fontFamily: MONO, fontWeight: 800, fontSize: 24, color: col.c }}>{ci === 0 ? "✓" : "✗"}</span>
                <span style={{ fontFamily: SANS, fontSize: 26, color: T.text, lineHeight: 1.35, width: 660 }}>{it}</span>
              </div>
            );
          })}
        </div>
      ))}
      <Foot theme={T} p={p(0.86, 0.94)}>One quick test: did the peers fall too? If the whole sector dropped together, it's macro. If only this name cratered, dig deeper.</Foot>
    </Stage>
  );
};

// ════════════════════════════════════════════ 11. QUALITY FILTER
const QualityScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur); const frame = useCurrentFrame();
  const items = [
    { e: "📈", t: "ROE above ~15% — efficient use of capital", at: 0.14 },
    { e: "🧱", t: "Low debt — Debt-to-Equity under ~0.5", at: 0.28 },
    { e: "💰", t: "Consistent profit growth over 3–5 years", at: 0.42 },
    { e: "💵", t: "Positive free cash flow — real, not just paper profit", at: 0.56 },
    { e: "🛡️", t: "A durable moat — leader in its space", at: 0.70 },
  ];
  return (
    <Stage>
      <Bg theme={T} accent={G} />
      <Head theme={T} kicker="FILTER 1 — IS IT ACTUALLY GOOD?" title="Define 'Fundamentally Strong'" color={G} />
      {items.map((it, i) => {
        const lo = p(it.at, it.at + 0.09);
        return (
          <div key={i} style={{ position: "absolute", left: 260, top: 250 + i * 108, width: 1400, height: 92, borderRadius: 16,
            background: mix(T.bg1, G, 0.05), border: `2px solid ${mix(T.line, G, 0.5)}`, display: "flex", alignItems: "center",
            gap: 24, padding: "0 30px", boxSizing: "border-box", opacity: lo, transform: `translateX(${(1 - lo) * 22}px)` }}>
            <span style={{ fontSize: 40 }}>{it.e}</span>
            <span style={{ fontFamily: SANS, fontWeight: 600, fontSize: 30, color: T.text }}>{it.t}</span>
          </div>
        );
      })}
      <Foot theme={T} p={p(0.85, 0.94)}>These numbers don't move because of a war or a crude spike. If they're intact, the business is fine — only the price changed.</Foot>
    </Stage>
  );
};

// ════════════════════════════════════════════ 12. VALUATION FILTER
const ValueScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur); const frame = useCurrentFrame();
  // illustrative PE-vs-industry bar (clearly labelled illustrative)
  const stockPE = 18, indPE = 26, scale = 14;
  return (
    <Stage>
      <Bg theme={T} accent={C} />
      <Head theme={T} kicker="FILTER 2 — IS IT ACTUALLY CHEAP?" title="Discounted vs Peers — Not Just 'Fallen'" color={C} />
      {/* left: checklist */}
      <div style={{ position: "absolute", left: 130, top: 250 }}>
        {[
          { t: "PE below the industry / peer median", at: 0.16 },
          { t: "PEG reasonable — cheap relative to its growth", at: 0.30 },
          { t: "P/B below its own 5-year average", at: 0.44 },
          { t: "Trading well below its 52-week high", at: 0.58 },
        ].map((it, i) => {
          const lo = p(it.at, it.at + 0.08);
          return (
            <div key={i} style={{ display: "flex", gap: 16, alignItems: "center", marginBottom: 30, width: 820, opacity: lo,
              transform: `translateX(${(1 - lo) * 20}px)` }}>
              <span style={{ width: 40, height: 40, borderRadius: 10, border: `2.5px solid ${C}`, background: mix(T.panel, C, 0.14),
                color: C, display: "flex", alignItems: "center", justifyContent: "center", fontFamily: MONO, fontWeight: 800, fontSize: 24, flexShrink: 0 }}>✓</span>
              <span style={{ fontFamily: SANS, fontSize: 28, color: T.text, lineHeight: 1.3 }}>{it.t}</span>
            </div>
          );
        })}
      </div>
      {/* right: illustrative PE bars */}
      <div style={{ position: "absolute", left: 1020, top: 262, width: 760, height: 470, borderRadius: 18,
        background: mix(T.bg1, C, 0.04), border: `2px solid ${mix(T.line, C, 0.4)}`, padding: "26px 30px", boxSizing: "border-box",
        opacity: p(0.5, 0.6) }}>
        <div style={{ fontFamily: MONO, fontWeight: 800, fontSize: 22, color: C, letterSpacing: 1 }}>PE vs INDUSTRY (illustrative)</div>
        {[{ l: "This stock", v: stockPE, c: G }, { l: "Industry median", v: indPE, c: T.muted }].map((b, i) => (
          <div key={i} style={{ marginTop: 44 }}>
            <div style={{ fontFamily: SANS, fontSize: 24, color: T.text, marginBottom: 10 }}>{b.l}</div>
            <div style={{ display: "flex", alignItems: "center", gap: 16 }}>
              <div style={{ height: 48, width: interpolate(p(0.56 + i * 0.06, 0.7 + i * 0.06), [0, 1], [0, b.v * scale]),
                borderRadius: 10, background: `linear-gradient(90deg, ${mix(String(b.c), T.bg1, 0.35)}, ${b.c})` }} />
              <span style={{ fontFamily: MONO, fontWeight: 800, fontSize: 30, color: b.c }}>{b.v}×</span>
            </div>
          </div>
        ))}
        <div style={{ fontFamily: SANS, fontSize: 23, color: T.muted, marginTop: 40, lineHeight: 1.4 }}>
          Same quality, a lower multiple than peers — <span style={{ color: G }}>that's</span> a discount. A stock can fall and still be expensive.
        </div>
      </div>
      <Foot theme={T} p={p(0.86, 0.94)}>"It fell 5%" is not a reason to buy. "It's a leader trading below its peers and its own history" is.</Foot>
    </Stage>
  );
};

// ════════════════════════════════════════════ 13. THE SCREEN
const ScreenScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur); const frame = useCurrentFrame();
  const lines = [
    "Market Capitalization > 20000 AND",
    "Return on equity > 15 AND",
    "Debt to equity < 0.5 AND",
    "Profit growth > 10 AND",
    "Price to Earning < Industry PE",
  ];
  return (
    <Stage>
      <Bg theme={T} accent={V} />
      <Head theme={T} kicker="RUN IT YOURSELF — THE SCREEN" title="Turn the Filters into a Query" color={V} />
      {/* screener panel */}
      <div style={{ position: "absolute", left: 130, top: 244, width: 1050, height: 540, borderRadius: 18,
        background: mix(T.bg0, C, 0.05), border: `2.5px solid ${mix(T.line, C, 0.5)}`, overflow: "hidden", opacity: p(0.04, 0.14) }}>
        <div style={{ height: 50, background: mix(T.bg0, C, 0.1), borderBottom: `2px solid ${mix(T.line, C, 0.4)}`,
          display: "flex", alignItems: "center", gap: 10, padding: "0 20px" }}>
          {[R, Y, G].map((cc, i) => <div key={i} style={{ width: 12, height: 12, borderRadius: 6, background: cc }} />)}
          <span style={{ marginLeft: 14, fontFamily: MONO, fontSize: 19, color: T.muted }}>screener.in — custom query</span>
        </div>
        <div style={{ padding: "28px 34px" }}>
          {lines.map((ln, i) => {
            const at = 0.16 + i * 0.1;
            return (
              <div key={i} style={{ fontFamily: MONO, fontSize: 27, color: i === lines.length - 1 ? G : T.text,
                lineHeight: 1.9, opacity: p(at, at + 0.05) }}>
                <span style={{ color: V, marginRight: 14 }}>{String(i + 1).padStart(2, "0")}</span>{ln}
              </div>
            );
          })}
          <div style={{ marginTop: 22, fontFamily: MONO, fontSize: 20, color: T.muted, opacity: p(0.74, 0.82) }}>
            <span style={{ color: G }}>{"// "}</span>large-caps · strong · low-debt · growing · cheaper than peers
          </div>
        </div>
      </div>
      {/* right: step to intersect with weekly losers */}
      <div style={{ position: "absolute", left: 1230, top: 244, width: 560, height: 540, borderRadius: 18,
        background: mix(T.bg1, Y, 0.05), border: `2.5px solid ${mix(T.line, Y, 0.5)}`, padding: "28px 30px", boxSizing: "border-box",
        opacity: p(0.5, 0.6) }}>
        <div style={{ fontFamily: MONO, fontWeight: 800, fontSize: 22, color: Y, letterSpacing: 1 }}>THEN INTERSECT WITH</div>
        <div style={{ fontFamily: SANS, fontWeight: 700, fontSize: 30, color: T.text, marginTop: 16, lineHeight: 1.35 }}>
          Last week's top losers
        </div>
        <div style={{ fontFamily: SANS, fontSize: 24, color: T.muted, marginTop: 14, lineHeight: 1.45 }}>
          Trendlyne → Top Losers → Week → Nifty 200.
          <br /><br />Keep only the names that appear in <span style={{ color: G }}>both</span> lists — strong, cheap, AND freshly dipped.
        </div>
        <div style={{ marginTop: 26, fontFamily: MONO, fontSize: 21, color: V, opacity: 0.6 + Math.sin(frame * 0.08) * 0.35 }}>
          Screen → shortlist → verify each name.
        </div>
      </div>
      <Foot theme={T} p={p(0.86, 0.94)}>The screen only produces a SHORTLIST. It never produces a buy. Every name still has to pass the checks by hand.</Foot>
    </Stage>
  );
};

// ════════════════════════════════════════════ 14. CONFIRM BEFORE BUYING
const ConfirmScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur); const frame = useCurrentFrame();
  const steps = [
    { n: "1", t: "Confirm WHY it fell", d: "Read the news. Macro / sector-wide? Good. Company-specific? Stop.", c: C },
    { n: "2", t: "Wait for it to stabilise", d: "Don't catch a falling knife. Let price base out before entering.", c: Y },
    { n: "3", t: "Enter in tranches", d: "Buy in parts, not all at once. You can't pick the exact bottom.", c: G },
    { n: "4", t: "Write the thesis & the exit", d: "Why you bought, and what would prove you wrong.", c: V },
  ];
  return (
    <Stage>
      <Bg theme={T} accent={C} />
      <Head theme={T} kicker="BEFORE YOU BUY THE DIP" title="Confirm, Then Enter Slowly" color={C} />
      {steps.map((s, i) => {
        const lo = p(0.12 + i * 0.14, 0.2 + i * 0.14);
        const x = 130 + (i % 2) * 850, y = 256 + Math.floor(i / 2) * 262;
        return (
          <div key={i} style={{ position: "absolute", left: x, top: y, width: 790, height: 226, borderRadius: 18,
            background: mix(T.bg1, s.c, 0.05), border: `2.5px solid ${s.c}`, padding: "26px 30px", boxSizing: "border-box",
            opacity: lo, transform: `translateY(${(1 - lo) * 18}px)` }}>
            <div style={{ display: "flex", alignItems: "center", gap: 18 }}>
              <div style={{ width: 54, height: 54, borderRadius: 12, background: s.c, color: T.bg0, display: "flex",
                alignItems: "center", justifyContent: "center", fontFamily: MONO, fontWeight: 800, fontSize: 30 }}>{s.n}</div>
              <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 32, color: T.text }}>{s.t}</div>
            </div>
            <div style={{ fontFamily: SANS, fontSize: 26, color: T.muted, marginTop: 18, lineHeight: 1.4 }}>{s.d}</div>
          </div>
        );
      })}
      <Foot theme={T} p={p(0.86, 0.94)}>A cheap price is an invitation, not a signal. Confirmation and patience turn a dip into a position.</Foot>
    </Stage>
  );
};

// ════════════════════════════════════════════ 15. RISK MANAGEMENT
const RiskScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur); const frame = useCurrentFrame();
  const items = [
    { e: "📊", t: "Size each position — no single name too large", at: 0.16 },
    { e: "🧩", t: "Spread across the shortlist, not one bet", at: 0.30 },
    { e: "⏳", t: "Give the thesis time — dips reward patience", at: 0.44 },
    { e: "🚪", t: "Exit if the thesis breaks, not if price wobbles", at: 0.58 },
  ];
  return (
    <Stage>
      <Bg theme={T} accent={R} />
      <Head theme={T} kicker="STAY IN THE GAME" title="Risk Management Turns Dips into Returns" color={R} />
      {items.map((it, i) => {
        const lo = p(it.at, it.at + 0.09);
        return (
          <div key={i} style={{ position: "absolute", left: 260, top: 268 + i * 128, width: 1400, height: 108, borderRadius: 16,
            background: mix(T.bg1, R, 0.05), border: `2px solid ${mix(T.line, R, 0.5)}`, display: "flex", alignItems: "center",
            gap: 24, padding: "0 30px", boxSizing: "border-box", opacity: lo, transform: `translateX(${(1 - lo) * 22}px)` }}>
            <span style={{ fontSize: 42 }}>{it.e}</span>
            <span style={{ fontFamily: SANS, fontWeight: 600, fontSize: 30, color: T.text }}>{it.t}</span>
          </div>
        );
      })}
      <Foot theme={T} p={p(0.85, 0.94)}>Even a perfect shortlist fails sometimes. Sizing and diversification are what let you be wrong and still come out ahead.</Foot>
    </Stage>
  );
};

// ════════════════════════════════════════════ 16. RECAP
const RecapScene: React.FC<{ dur?: number; items?: string[]; closer?: string }> = ({ dur, items = [], closer = "" }) => {
  const p = useP(dur); const frame = useCurrentFrame();
  return (
    <Stage>
      <Bg theme={T} accent={G} />
      <div style={{ position: "absolute", left: 0, right: 0, top: 90, textAlign: "center" }}>
        <div style={{ fontFamily: MONO, fontWeight: 800, fontSize: 22, color: G, letterSpacing: 8, opacity: p(0.03, 0.12) }}>RECAP — THE PLAYBOOK</div>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 58, color: T.text, letterSpacing: -2, marginTop: 12, opacity: p(0.10, 0.22) }}>
          Buying the Dip, Intelligently</div>
      </div>
      <div style={{ position: "absolute", left: 150, top: 222, width: 1620 }}>
        {items.map((item, i) => {
          const at = 0.05 + i * 0.09;
          const lo = p(at, at + 0.06);
          return (
            <div key={i} style={{ display: "flex", alignItems: "center", gap: 18, marginBottom: 18, opacity: lo,
              transform: `translateX(${(1 - lo) * 20}px)` }}>
              <div style={{ width: 5, height: 34, borderRadius: 3, background: G, flexShrink: 0 }} />
              <div style={{ fontFamily: MONO, fontWeight: 800, fontSize: 20, color: G, width: 44, flexShrink: 0 }}>{String(i + 1).padStart(2, "0")}</div>
              <div style={{ fontFamily: SANS, fontSize: 26, color: T.text, lineHeight: 1.3, width: 1490 }}>{item}</div>
            </div>
          );
        })}
      </div>
      {closer && (
        <div style={{ position: "absolute", left: 130, bottom: 92, right: 130, textAlign: "center",
          fontFamily: SANS, fontStyle: "italic", fontSize: 36, color: G, textShadow: `0 0 40px ${mix(T.bg0, G, 0.6)}`,
          opacity: p(0.80, 0.90), lineHeight: 1.3 }}>{closer}</div>
      )}
      <div style={{ position: "absolute", left: 130, top: 986, right: 130, textAlign: "center", fontFamily: MONO, fontSize: 20,
        color: R, opacity: 0.5 + Math.sin(frame * 0.06) * 0.3 }}>
        ⚠ Internal education only · Not investment advice · Verify all data & consult a SEBI-registered advisor
      </div>
    </Stage>
  );
};

// ════════════════════════════════════════════ DISPATCHER
export const DIPScene: React.FC<{ variant: string; [key: string]: unknown }> = ({ variant, ...rest }) => {
  switch (variant) {
    case "dip_title":     return <TitleScene {...(rest as any)} />;
    case "dip_div":       return <DividerScene {...(rest as any)} />;
    case "dip_thesis":    return <ThesisScene {...(rest as any)} />;
    case "dip_setup":     return <SetupScene {...(rest as any)} />;
    case "dip_crude":     return <CrudeScene {...(rest as any)} />;
    case "dip_rupee":     return <RupeeScene {...(rest as any)} />;
    case "dip_fii":       return <FiiScene {...(rest as any)} />;
    case "dip_war":       return <WarScene {...(rest as any)} />;
    case "dip_usit":      return <UsItScene {...(rest as any)} />;
    case "dip_dipvstrap": return <DipVsTrapScene {...(rest as any)} />;
    case "dip_quality":   return <QualityScene {...(rest as any)} />;
    case "dip_value":     return <ValueScene {...(rest as any)} />;
    case "dip_screen":    return <ScreenScene {...(rest as any)} />;
    case "dip_confirm":   return <ConfirmScene {...(rest as any)} />;
    case "dip_risk":      return <RiskScene {...(rest as any)} />;
    case "dip_recap":     return <RecapScene {...(rest as any)} />;
    default: return null;
  }
};
