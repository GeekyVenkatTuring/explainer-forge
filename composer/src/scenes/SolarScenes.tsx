/**
 * SolarScenes.tsx — "Solar Panels: The Business" scene set (prefix `sol`).
 *
 * A complete-beginner course: how a solar panel works, how systems are installed
 * on homes and businesses to cut electricity bills, and how the solar business
 * makes money (channels + margins). English, captions ON, 16:9 1080p30.
 *
 * Identity (skills/04):
 *   theme accent = SUN gold (sunlight / energy source)
 *   semantic colors:
 *     SUN  #FDB813  sunlight, photons, energy, generation
 *     CELL #38BDF8  silicon, panels, DC electrons, hardware
 *     GRID #34D399  savings, money, AC power, the grid, "good"
 *     BIZ  #A78BFA  business, margins, sales, channels
 *     HOT  #FB7185  cost, loss, warning, the rising bill
 *   motif: photons raining onto a panel → electrons → rupees (sun → savings).
 *
 * Every scene takes `dur` and phases with useP(dur); continuous motion in every
 * frame (photon rain, sun rays, Flow, dash-march Wires, sine glow, chase). Numeric
 * things (sizing, payback lines, subsidy slabs, margins, P&L) are COMPUTED and
 * indexed by phase — see skills/03,04. Money figures are illustrative India 2026
 * ranges (PM Surya Ghar subsidy, typical costs/margins), flagged on-screen.
 */
import React from "react";
import { AbsoluteFill, interpolate, useCurrentFrame } from "remotion";
import {
  makeTheme, mix, useP as usePfull, usePop, rnd, MONO, SANS, Theme,
  Bg, Stage, Kicker, Head, Card, Flow, Wire, Counter, Brackets, ScanBeam,
} from "../lib/primitives";

// A/V-SYNC: narration front-loads names then elaborates; compress reveals into the
// front REVEAL_SPAN so a visual lands ~when spoken. Progress bar + continuous motion
// use usePfull over the FULL beat (no frozen tail). Scenes that track a continuous
// animation (sizing counters, savings line, meter, install chase, roadmap, recap,
// title) opt out via usePfull. See skills/02 §"Narration ↔ scene contract".
const REVEAL_SPAN = 0.62;
const useP = (dur?: unknown) => {
  const p = usePfull(dur);
  return (a: number, b: number) => p(Math.min(1, a * REVEAL_SPAN), Math.min(1, b * REVEAL_SPAN));
};

// Captions ON → the takeaway strip sits higher (y=856, centered) to clear the
// caption pill (skills/05: captions collide with the default Foot at y924).
const Foot: React.FC<{ theme: Theme; p: number; children: React.ReactNode }> = ({ theme, p, children }) => (
  <div style={{
    position: "absolute", left: 100, top: 856, right: 100, fontFamily: MONO, fontSize: 22,
    color: theme.muted, opacity: p, lineHeight: 1.35, transform: `translateY(${(1 - p) * 12}px)`, textAlign: "center",
  }}>{children}</div>
);

// ---------------------------------------------------------------- identity
const T = makeTheme({ accent: "#FDB813", bg0: "#07060A", bg1: "#0D0B14", bg2: "#16131F", panel: "#1B1826" });
const A = {
  sun: "#FDB813", cell: "#38BDF8", grid: "#34D399", biz: "#A78BFA", hot: "#FB7185", ok: "#34D399", muted: "#8B8598",
};
const fmt = (x: number, d = 0) => x.toFixed(d);

// ---------------------------------------------------------------- ambient motifs
/** Photons raining diagonally — the video's signature "sunlight" layer. Never stops. */
const PhotonRain: React.FC<{ o?: number; color?: string; n?: number; speed?: number; seed?: number }> = ({
  o = 0.4, color = A.sun, n = 22, speed = 1, seed = 0,
}) => {
  const frame = useCurrentFrame();
  return (
    <>
      {Array.from({ length: n }).map((_, i) => {
        const x0 = rnd(i, 1, seed) * 2000 - 120;
        const span = 1260;
        const t = ((frame * speed * 2.4 + i * 90 + rnd(i, 2, seed) * span) % span);
        const x = x0 + t * 0.42;
        const y = t - 140;
        const fade = Math.sin((y / 1080) * Math.PI);
        return (
          <div key={i} style={{
            position: "absolute", left: x, top: y, width: 3, height: 18, borderRadius: 2,
            background: color, opacity: o * Math.max(0, fade) * 0.85, transform: "rotate(20deg)",
            boxShadow: `0 0 9px ${color}`,
          }} />
        );
      })}
    </>
  );
};

/** Glowing sun with slowly rotating rays — title/divider hero motif. */
const SunCore: React.FC<{ cx: number; cy: number; r: number; o?: number; color?: string; rays?: number }> = ({
  cx, cy, r, o = 1, color = A.sun, rays = 14,
}) => {
  const frame = useCurrentFrame();
  const pulse = (Math.sin(frame * 0.05) + 1) / 2;
  return (
    <div style={{ position: "absolute", left: cx, top: cy, opacity: o }}>
      {Array.from({ length: rays }).map((_, i) => {
        const ang = frame * 0.006 + (i / rays) * Math.PI * 2;
        const inner = r + 14, outer = r + 40 + Math.sin(frame * 0.08 + i) * 10;
        return (
          <div key={i} style={{
            position: "absolute",
            left: Math.cos(ang) * inner, top: Math.sin(ang) * inner,
            width: outer - inner, height: 4, borderRadius: 2, transformOrigin: "left center",
            transform: `rotate(${ang}rad)`, background: color, opacity: 0.45,
            boxShadow: `0 0 10px ${color}`,
          }} />
        );
      })}
      <div style={{
        position: "absolute", left: -r, top: -r, width: r * 2, height: r * 2, borderRadius: r * 2,
        background: `radial-gradient(circle, ${color} 0%, ${mix(color, T.bg0, 0.4)} 55%, transparent 75%)`,
        boxShadow: `0 0 ${60 + pulse * 40}px ${color}`,
      }} />
    </div>
  );
};

/** Small reusable stat pill. */
const Pill: React.FC<{ label: string; value: string; color: string; o?: number }> = ({ label, value, color, o = 1 }) => (
  <div style={{ display: "inline-flex", alignItems: "baseline", gap: 12, opacity: o }}>
    <span style={{ fontFamily: MONO, fontSize: 22, color: T.muted }}>{label}</span>
    <span style={{ fontFamily: MONO, fontWeight: 800, fontSize: 30, color }}>{value}</span>
  </div>
);

/** A drawn solar panel (grid of cells) at (x,y). */
const PanelIcon: React.FC<{ x: number; y: number; w: number; h: number; cols?: number; rows?: number; color?: string; o?: number; live?: boolean }> = ({
  x, y, w, h, cols = 6, rows = 4, color = A.cell, o = 1, live = false,
}) => {
  const frame = useCurrentFrame();
  const cw = (w - (cols + 1) * 4) / cols, ch = (h - (rows + 1) * 4) / rows;
  const hot = Math.floor(frame / 6) % (cols * rows);
  return (
    <div style={{
      position: "absolute", left: x, top: y, width: w, height: h, borderRadius: 8, opacity: o,
      background: mix(T.panel, color, 0.12), border: `3px solid ${mix(color, T.text, 0.1)}`,
      padding: 4, boxSizing: "border-box", transform: "perspective(900px) rotateX(6deg)",
    }}>
      <div style={{ display: "grid", gridTemplateColumns: `repeat(${cols}, ${cw}px)`, gridTemplateRows: `repeat(${rows}, ${ch}px)`, gap: 4, width: "100%", height: "100%" }}>
        {Array.from({ length: cols * rows }).map((_, i) => (
          <div key={i} style={{
            background: `linear-gradient(135deg, ${mix(color, T.bg0, 0.35)}, ${mix(color, T.bg0, 0.6)})`,
            borderRadius: 3, border: `1px solid ${mix(color, T.text, 0.2)}`,
            boxShadow: live && hot === i ? `inset 0 0 10px ${color}` : "none",
          }} />
        ))}
      </div>
    </div>
  );
};

// ============================================================================ TITLE
const TitleScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const p = usePfull(dur);
  const pop = usePop(dur);
  return (
    <AbsoluteFill style={{ alignItems: "center", justifyContent: "center" }}>
      <PhotonRain o={0.45} n={26} />
      <SunCore cx={300} cy={230} r={70} o={0.9} />
      <SunCore cx={1650} cy={880} r={46} o={0.6} color={A.grid} rays={10} />
      <div style={{ textAlign: "center", transform: `scale(${0.92 + pop(0) * 0.08})` }}>
        <div style={{ display: "flex", justifyContent: "center", marginBottom: 26 }}>
          <Kicker theme={T} text="SUNLIGHT → SAVINGS → BUSINESS · FULL COURSE" cx />
        </div>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 118, lineHeight: 1.0, letterSpacing: -3, color: T.text }}>
          <div>Solar Panels</div>
          <div style={{ color: A.sun, textShadow: `0 0 70px ${mix(T.bg0, A.sun, 0.7)}` }}>as a Business</div>
        </div>
        <div style={{ height: 5, width: interpolate(p(0.18, 0.45), [0, 1], [0, 560]), background: `linear-gradient(90deg, ${A.sun}, ${A.grid})`, borderRadius: 3, margin: "30px auto" }} />
        <div style={{ fontFamily: SANS, fontSize: 36, color: T.muted, opacity: p(0.28, 0.5) }}>
          the physics · installing on homes · cutting bills · selling · margins — from zero
        </div>
      </div>
    </AbsoluteFill>
  );
};

// ============================================================================ ROADMAP
const RoadmapScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const p = usePfull(dur);
  const parts = [
    { n: 1, title: "Why Solar, Why Now", sub: "the opportunity on every roof", c: A.sun },
    { n: 2, title: "The Science", sub: "how a panel turns light into power", c: A.cell },
    { n: 3, title: "The System", sub: "DC, inverters, and the grid", c: A.grid },
    { n: 4, title: "Installing on Homes", sub: "sizing, savings, subsidy", c: A.sun },
    { n: 5, title: "Serving Businesses", sub: "bigger bills, CAPEX vs OPEX", c: A.cell },
    { n: 6, title: "The Business", sub: "channels, margins, getting started", c: A.biz },
  ];
  const y0 = 200, rowH = 116;
  const hot = Math.floor(frame / 20) % parts.length;
  const railFill = p(0.08, 0.86);
  return (
    <AbsoluteFill style={{ alignItems: "center", justifyContent: "center" }}>
      <PhotonRain o={0.3} n={16} />
      <div style={{ position: "absolute", left: 0, right: 0, top: 88, textAlign: "center", opacity: p(0, 0.06) }}>
        <Kicker theme={T} text="THE JOURNEY AHEAD · SIX PARTS" cx />
      </div>
      <div style={{ position: "absolute", left: 470, top: y0 + 30, width: 4, height: parts.length * rowH - 60, background: T.line, borderRadius: 2 }} />
      <div style={{ position: "absolute", left: 470, top: y0 + 30, width: 4, height: (parts.length * rowH - 60) * railFill, background: `linear-gradient(180deg, ${A.sun}, ${A.biz})`, borderRadius: 2, boxShadow: `0 0 12px ${A.sun}` }} />
      {parts.map((pt, i) => {
        const at = 0.1 + i * 0.12;
        const o = p(at, at + 0.08);
        const active = hot === i;
        return (
          <div key={i} style={{ position: "absolute", left: 520, top: y0 + i * rowH, width: 940, height: rowH - 20, display: "flex", alignItems: "center", gap: 24, opacity: o, transform: `translateX(${(1 - o) * -30}px)` }}>
            <div style={{ width: 66, height: 66, borderRadius: 16, flexShrink: 0, background: mix(T.panel, pt.c, active ? 0.35 : 0.18), border: `2.5px solid ${pt.c}`, display: "flex", alignItems: "center", justifyContent: "center", fontFamily: MONO, fontWeight: 800, fontSize: 32, color: pt.c, boxShadow: active ? `0 0 22px ${mix(T.bg0, pt.c, 0.5)}` : "none", transform: `scale(${active ? 1.08 : 1})` }}>{pt.n}</div>
            <div>
              <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 40, color: T.text, letterSpacing: -1 }}>{pt.title}</div>
              <div style={{ fontFamily: MONO, fontSize: 23, color: pt.c, marginTop: 4 }}>{pt.sub}</div>
            </div>
          </div>
        );
      })}
      <div style={{ position: "absolute", left: 464, top: y0 + 26 + ((frame * 3) % (parts.length * rowH - 52)), width: 16, height: 16, borderRadius: 8, background: A.sun, boxShadow: `0 0 16px ${A.sun}`, opacity: p(0.1, 0.2) }} />
    </AbsoluteFill>
  );
};

// ============================================================================ HOOK
const HookScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const billH = interpolate(p(0.16, 0.5), [0, 1], [40, 300]); // the bill climbs
  return (
    <Stage>
      <Head theme={T} kicker="THE OPPORTUNITY" title="Your roof is doing nothing" color={A.sun} o={p(0, 0.06)} />
      <PhotonRain o={0.35} n={16} />
      {/* left: the rising electricity bill */}
      <Card theme={T} x={130} y={250} w={740} h={520} color={A.hot} o={p(0.1, 0.18)}>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 36, color: T.text }}>Every month, the same bill</div>
        <div style={{ fontFamily: MONO, fontSize: 24, color: A.hot, marginTop: 10 }}>and it keeps climbing ▲</div>
        <div style={{ position: "absolute", left: 40, bottom: 40, display: "flex", alignItems: "flex-end", gap: 20 }}>
          {[0, 1, 2, 3, 4].map((i) => {
            const h = billH * (0.6 + i * 0.1);
            return <div key={i} style={{ width: 84, height: h, borderRadius: "8px 8px 0 0", background: `linear-gradient(180deg, ${A.hot}, ${mix(A.hot, T.bg1, 0.5)})`, border: `2px solid ${A.hot}`, borderBottom: "none" }} />;
          })}
        </div>
        <div style={{ position: "absolute", right: 34, top: 120, fontFamily: MONO, fontWeight: 800, fontSize: 40, color: A.hot, opacity: p(0.32, 0.42) }}>₹ ₹ ₹</div>
      </Card>
      {/* right: the same roof, now working */}
      <Card theme={T} x={1050} y={250} w={740} h={520} color={A.grid} o={p(0.4, 0.5)} glow>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 36, color: T.text }}>The same roof, now working</div>
        <div style={{ fontFamily: MONO, fontSize: 24, color: A.grid, marginTop: 10 }}>free fuel falling from the sky ▼</div>
        <PanelIcon x={40} y={150} w={560} h={230} cols={7} rows={4} color={A.grid} live o={p(0.5, 0.6)} />
        <div style={{ position: "absolute", left: 40, bottom: 32, fontFamily: SANS, fontWeight: 800, fontSize: 30, color: A.grid, opacity: p(0.58, 0.68) }}>
          bills drop 80–100% ▼
        </div>
      </Card>
      <Flow x1={870} y1={510} x2={1050} y2={510} color={A.sun} n={6} o={p(0.5, 0.6)} />
      <div style={{ position: "absolute", left: 0, right: 0, top: 792, textAlign: "center", opacity: p(0.7, 0.82) }}>
        <span style={{ fontFamily: SANS, fontWeight: 800, fontSize: 38, color: T.text }}>
          Enough sunlight hits the Earth in <span style={{ color: A.sun, textShadow: `0 0 26px ${mix(T.bg0, A.sun, 0.6)}` }}>one hour</span> to power humanity for a <span style={{ color: A.sun }}>year</span>.
        </span>
      </div>
      <Foot theme={T} p={p(0.86, 0.94)}>
        Solar is the business of catching a little of that — and selling the savings.
      </Foot>
    </Stage>
  );
};

// ============================================================================ WHY NOW
const WhyScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur);
  const cards = [
    { at: 0.1, c: A.grid, big: "−90%", label: "panel prices, last decade", note: "a panel today costs a tenth of what it did" },
    { at: 0.24, c: A.hot, big: "▲", label: "grid tariffs keep rising", note: "the bill you avoid gets bigger every year" },
    { at: 0.38, c: A.sun, big: "₹78k", label: "government subsidy per home", note: "PM Surya Ghar pays part of the cost" },
    { at: 0.52, c: A.cell, big: "<5%", label: "of Indian rooftops are solar", note: "the market has barely started" },
  ];
  return (
    <Stage>
      <Head theme={T} kicker="WHY NOW" title="Four forces made solar a business" color={A.sun} o={p(0, 0.06)} />
      {cards.map((cd, i) => {
        const x = 130 + (i % 2) * 860;
        const y = 250 + Math.floor(i / 2) * 300;
        return (
          <Card key={i} theme={T} x={x} y={y} w={790} h={260} color={cd.c} o={p(cd.at, cd.at + 0.1)}>
            <div style={{ display: "flex", alignItems: "baseline", gap: 22 }}>
              <div style={{ fontFamily: MONO, fontWeight: 800, fontSize: 76, color: cd.c }}>{cd.big}</div>
              <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 30, color: T.text, lineHeight: 1.2 }}>{cd.label}</div>
            </div>
            <div style={{ fontFamily: MONO, fontSize: 23, color: T.muted, marginTop: 20, lineHeight: 1.35 }}>{cd.note}</div>
          </Card>
        );
      })}
      <Foot theme={T} p={p(0.86, 0.94)}>
        Cheaper hardware, costlier grid power, public money, and a wide-open market.
      </Foot>
    </Stage>
  );
};

// ============================================================================ DIVIDER
const Divider: React.FC<{ dur?: number; n?: number; title?: string; sub?: string; color?: string }> = ({
  dur, n = 1, title = "", sub = "", color = A.sun,
}) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  return (
    <Stage>
      <PhotonRain o={0.3} n={16} color={color} seed={n} />
      <Brackets x={330} y={300} w={1260} h={480} color={color} o={p(0.02, 0.14)} len={54} />
      <ScanBeam theme={T} x={340} y={310} w={1240} h={460} color={color} o={p(0.05, 0.2)} speed={1.6} />
      <div style={{ position: "absolute", left: 0, right: 0, top: 360, textAlign: "center" }}>
        <div style={{ fontFamily: MONO, fontWeight: 800, fontSize: 34, color, letterSpacing: 10, opacity: p(0.05, 0.15) }}>PART {"0" + n}</div>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 92, color: T.text, letterSpacing: -2, marginTop: 20, opacity: p(0.12, 0.24), transform: `translateY(${(1 - p(0.12, 0.24)) * 30}px)` }}>{title}</div>
        <div style={{ height: 5, width: interpolate(p(0.2, 0.5), [0, 1], [0, 440]), background: color, borderRadius: 3, margin: "26px auto" }} />
        <div style={{ fontFamily: SANS, fontSize: 33, color: T.muted, opacity: p(0.3, 0.45) }}>{sub}</div>
      </div>
      <div style={{ position: "absolute", left: 0, right: 0, top: 860, display: "flex", justifyContent: "center", gap: 16, opacity: p(0.3, 0.45) }}>
        {[1, 2, 3, 4, 5, 6].map((i) => (
          <div key={i} style={{ width: i === n ? 44 : 14, height: 14, borderRadius: 8, background: i <= n ? color : mix(T.panel, color, 0.15), border: `1.5px solid ${i <= n ? color : T.line}`, opacity: i === n ? 0.7 + Math.sin(frame * 0.1) * 0.3 : 1 }} />
        ))}
      </div>
    </Stage>
  );
};

// ============================================================================ SPECTRUM (photons)
const SpectrumScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  return (
    <Stage>
      <Head theme={T} kicker="STEP ONE — THE FUEL" title="Sunlight arrives in tiny packets" color={A.sun} o={p(0, 0.06)} />
      <SunCore cx={330} cy={520} r={90} o={p(0.08, 0.18)} />
      {/* photon stream from sun to panel */}
      <Flow x1={430} y1={520} x2={1180} y2={520} color={A.sun} n={12} o={p(0.2, 0.3)} speed={0.02} size={13} />
      <div style={{ position: "absolute", left: 560, top: 360, fontFamily: MONO, fontSize: 24, color: A.sun, opacity: p(0.3, 0.4) }}>photons — packets of energy</div>
      <PanelIcon x={1200} y={400} w={420} h={240} cols={6} rows={4} color={A.cell} live o={p(0.42, 0.52)} />
      <div style={{ position: "absolute", left: 1200, top: 660, width: 420, textAlign: "center", fontFamily: SANS, fontWeight: 700, fontSize: 26, color: T.text, opacity: p(0.5, 0.6) }}>the panel catches them</div>
      {/* solar constant stat */}
      <Card theme={T} x={600} y={636} w={520} h={190} color={A.sun} o={p(0.62, 0.72)}>
        <div style={{ fontFamily: MONO, fontSize: 22, color: T.muted }}>sunlight on 1 square metre</div>
        <div style={{ marginTop: 10 }}>
          <Counter p={p(0.66, 0.8)} to={1000} comma color={A.sun} size={56} suffix=" W" />
        </div>
        <div style={{ fontFamily: MONO, fontSize: 22, color: T.muted, marginTop: 8 }}>≈ a bright noon</div>
      </Card>
      <Foot theme={T} p={p(0.86, 0.94)}>
        A packet of light is a photon. Catch its energy, and you have electricity.
      </Foot>
    </Stage>
  );
};

// ============================================================================ CELL (photovoltaic effect)
const CellScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const p = usePfull(dur); // continuous electron loop tracks the whole beat
  // cross-section geometry
  const CX = 250, CY = 300, CW = 900, topH = 120, botH = 200;
  const junctionY = CY + topH;
  return (
    <Stage>
      <Head theme={T} kicker="THE PHOTOVOLTAIC EFFECT" title="How light knocks an electron loose" color={A.cell} o={p(0, 0.06)} />
      {/* n-type top layer */}
      <div style={{ position: "absolute", left: CX, top: CY, width: CW, height: topH, background: mix(T.panel, A.cell, 0.28), border: `2px solid ${A.cell}`, borderRadius: "10px 10px 0 0", opacity: p(0.08, 0.16), display: "flex", alignItems: "center", paddingLeft: 24 }}>
        <span style={{ fontFamily: MONO, fontSize: 24, color: A.cell }}>n-type silicon — spare electrons (−)</span>
      </div>
      {/* p-type bottom layer */}
      <div style={{ position: "absolute", left: CX, top: junctionY, width: CW, height: botH, background: mix(T.panel, A.hot, 0.18), border: `2px solid ${A.hot}`, borderTop: "none", borderRadius: "0 0 10px 10px", opacity: p(0.12, 0.2), display: "flex", alignItems: "flex-end", paddingLeft: 24, paddingBottom: 16 }}>
        <span style={{ fontFamily: MONO, fontSize: 24, color: A.hot }}>p-type silicon — holes, waiting (+)</span>
      </div>
      {/* junction line */}
      <div style={{ position: "absolute", left: CX, top: junctionY - 2, width: CW, height: 4, background: A.grid, opacity: p(0.2, 0.28), boxShadow: `0 0 12px ${A.grid}` }} />
      <div style={{ position: "absolute", left: CX + CW + 14, top: junctionY - 14, width: 260, fontFamily: MONO, fontSize: 21, color: A.grid, opacity: p(0.24, 0.34) }}>the junction: a built-in one-way push</div>
      {/* incoming photon (starts below the header zone, y>190) */}
      <Flow x1={CX + 200} y1={205} x2={CX + 200} y2={CY + 40} color={A.sun} n={4} o={p(0.3, 0.4)} speed={0.03} size={12} />
      <div style={{ position: "absolute", left: CX + 230, top: 210, fontFamily: MONO, fontSize: 22, color: A.sun, opacity: p(0.32, 0.42) }}>photon in</div>
      {/* external circuit: top contact → load → bottom contact, electrons flow forever */}
      <svg style={{ position: "absolute", left: 0, top: 0, overflow: "visible" }} width={1920} height={1080}>
        <path d={`M ${CX} ${CY + 10} L ${CX - 120} ${CY + 10} L ${CX - 120} ${junctionY + 120} L ${CX} ${junctionY + 120}`} fill="none" stroke={A.cell} strokeWidth={4} opacity={p(0.4, 0.5)} />
      </svg>
      {/* moving electrons in the wire */}
      {p(0.42, 0.44) > 0.5 && Array.from({ length: 7 }).map((_, i) => {
        const t = (frame * 0.006 + i / 7) % 1;
        // path length param along the 3-segment wire (down-left, down, right)
        let x = CX, y = CY + 10;
        if (t < 0.33) { x = CX - 120 * (t / 0.33); y = CY + 10; }
        else if (t < 0.66) { x = CX - 120; y = (CY + 10) + (junctionY + 110 - CY) * ((t - 0.33) / 0.33); }
        else { x = CX - 120 + 120 * ((t - 0.66) / 0.34); y = junctionY + 120; }
        return <div key={i} style={{ position: "absolute", left: x - 6, top: y - 6, width: 12, height: 12, borderRadius: 6, background: A.cell, boxShadow: `0 0 10px ${A.cell}` }} />;
      })}
      {/* the load (a bulb) sitting on the external wire */}
      <div style={{ position: "absolute", left: CX - 205, top: junctionY - 14, width: 150, textAlign: "center", opacity: p(0.44, 0.54) }}>
        <div style={{ fontSize: 60 }}>💡</div>
        <div style={{ fontFamily: MONO, fontSize: 20, color: A.grid }}>does work</div>
      </div>
      <div style={{ position: "absolute", left: 1360, top: 300, width: 460, opacity: p(0.56, 0.68) }}>
        <div style={{ fontFamily: SANS, fontWeight: 700, fontSize: 29, color: T.text, lineHeight: 1.4 }}>
          A photon frees an <span style={{ color: A.cell }}>electron</span>. The junction pushes it
          out one side — so it flows through your wire, powers the bulb, and returns.
        </div>
        <div style={{ marginTop: 22, fontFamily: MONO, fontWeight: 800, fontSize: 28, color: A.sun, textShadow: `0 0 ${14 + Math.sin(frame * 0.07) * 8}px ${mix(T.bg0, A.sun, 0.5)}` }}>
          that flow = electric current
        </div>
      </div>
      <Foot theme={T} p={p(0.87, 0.95)}>
        No moving parts, no fuel, no noise — just light in, electrons out.
      </Foot>
    </Stage>
  );
};

// ============================================================================ PANEL (cell → module → array)
const PanelScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur);
  const steps = [
    { at: 0.1, label: "1 cell", val: "≈ 0.5 volt · a few watts", c: A.cell },
    { at: 0.28, label: "≈ 60–144 cells = 1 panel", val: "≈ 400–600 watts", c: A.cell },
    { at: 0.46, label: "many panels = 1 array", val: "kilowatts — a whole roof", c: A.grid },
  ];
  return (
    <Stage>
      <Head theme={T} kicker="FROM CELL TO ROOF" title="Small cells add up to real power" color={A.cell} o={p(0, 0.06)} />
      {/* single cell */}
      <div style={{ position: "absolute", left: 150, top: 320, width: 130, height: 130, borderRadius: 10, background: `linear-gradient(135deg, ${mix(A.cell, T.bg0, 0.35)}, ${mix(A.cell, T.bg0, 0.6)})`, border: `2.5px solid ${A.cell}`, opacity: p(0.1, 0.18) }} />
      <Wire x1={290} y1={385} x2={430} y2={385} p={p(0.24, 0.32)} color={A.cell} />
      {/* one panel */}
      <PanelIcon x={440} y={300} w={300} h={170} cols={6} rows={4} color={A.cell} live o={p(0.28, 0.38)} />
      <Wire x1={750} y1={385} x2={890} y2={385} p={p(0.42, 0.5)} color={A.grid} />
      {/* array of panels */}
      <div style={{ position: "absolute", left: 900, top: 250, width: 620, height: 300, opacity: p(0.46, 0.56) }}>
        {Array.from({ length: 6 }).map((_, i) => (
          <PanelIcon key={i} x={(i % 3) * 210} y={Math.floor(i / 3) * 160} w={190} h={140} cols={5} rows={3} color={A.grid} live />
        ))}
      </div>
      {steps.map((s, i) => (
        <div key={i} style={{ position: "absolute", left: 150 + i * 470, top: 620, width: 430, opacity: p(s.at + 0.06, s.at + 0.14) }}>
          <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 30, color: s.c }}>{s.label}</div>
          <div style={{ fontFamily: MONO, fontSize: 23, color: T.muted, marginTop: 8 }}>{s.val}</div>
        </div>
      ))}
      <Foot theme={T} p={p(0.86, 0.94)}>
        Wire cells into a panel, panels into an array — and you size it to the bill.
      </Foot>
    </Stage>
  );
};

// ============================================================================ IV CURVE / EFFICIENCY
const EfficiencyScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const inW = 1000, outW = 210; // ~21% of 1000 W/m²
  const barTop = 300, barLeft = 200, fullH = 420, maxW = 900;
  const inLen = interpolate(p(0.14, 0.34), [0, 1], [0, maxW]);
  const outLen = interpolate(p(0.44, 0.64), [0, 1], [0, maxW * (outW / inW)]);
  return (
    <Stage>
      <Head theme={T} kicker="HOW MUCH POWER" title="A panel keeps about a fifth of the light" color={A.sun} o={p(0, 0.06)} />
      {/* input bar */}
      <div style={{ position: "absolute", left: barLeft, top: barTop, fontFamily: MONO, fontSize: 24, color: A.sun, opacity: p(0.1, 0.18) }}>sunlight in</div>
      <div style={{ position: "absolute", left: barLeft, top: barTop + 36, width: inLen, height: 96, borderRadius: 12, background: `linear-gradient(90deg, ${A.sun}, ${mix(A.sun, T.bg1, 0.4)})`, border: `2.5px solid ${A.sun}` }} />
      <div style={{ position: "absolute", left: barLeft + inLen + 18, top: barTop + 50, fontFamily: MONO, fontWeight: 800, fontSize: 40, color: A.sun, opacity: p(0.3, 0.4) }}>{fmt(inW)} W</div>
      {/* output bar */}
      <div style={{ position: "absolute", left: barLeft, top: barTop + 190, fontFamily: MONO, fontSize: 24, color: A.grid, opacity: p(0.4, 0.48) }}>electricity out</div>
      <div style={{ position: "absolute", left: barLeft, top: barTop + 226, width: outLen, height: 96, borderRadius: 12, background: `linear-gradient(90deg, ${A.grid}, ${mix(A.grid, T.bg1, 0.4)})`, border: `2.5px solid ${A.grid}`, boxShadow: `0 0 20px ${mix(T.bg0, A.grid, 0.3)}` }} />
      <div style={{ position: "absolute", left: barLeft + outLen + 18, top: barTop + 240, fontFamily: MONO, fontWeight: 800, fontSize: 40, color: A.grid, opacity: p(0.6, 0.7) }}>{fmt(outW)} W</div>
      {/* efficiency callout */}
      <Card theme={T} x={1360} y={330} w={460} h={260} color={A.sun} o={p(0.62, 0.72)} glow>
        <div style={{ fontFamily: MONO, fontSize: 22, color: T.muted }}>modern panel efficiency</div>
        <Counter p={p(0.66, 0.8)} to={21} color={A.sun} size={80} suffix=" %" />
        <div style={{ fontFamily: SANS, fontWeight: 700, fontSize: 24, color: T.text, marginTop: 10, lineHeight: 1.35 }}>
          The rest leaves as heat — and heat, dust, and shade lower it further.
        </div>
      </Card>
      <div style={{ position: "absolute", left: barLeft, top: 800, fontFamily: SANS, fontWeight: 700, fontSize: 27, color: T.text, opacity: p(0.78, 0.88) }}>
        So a “<span style={{ color: A.cell }}>1 kilowatt</span>” system is rated at strong noon sun — real output rides the weather.
      </div>
      <Foot theme={T} p={p(0.88, 0.95)}>
        Rule of thumb in India: 1 kW makes about 4 units of electricity a day.
      </Foot>
    </Stage>
  );
};

// ============================================================================ TYPES (mono/poly/thin-film)
const TypesScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur);
  const kinds = [
    { at: 0.1, name: "Monocrystalline", eff: 21, c: A.cell, look: "sleek black", note: "most efficient · premium · today's default" },
    { at: 0.26, name: "Polycrystalline", eff: 17, c: A.biz, look: "blue, speckled", note: "cheaper · older tech · fading out" },
    { at: 0.42, name: "Thin-film", eff: 12, c: A.grid, look: "flexible sheet", note: "light & bendy · needs more area" },
  ];
  const maxEff = 24;
  return (
    <Stage>
      <Head theme={T} kicker="CHOOSING PANELS" title="Three kinds — mostly one wins today" color={A.cell} o={p(0, 0.06)} />
      {kinds.map((k, i) => {
        const x = 140 + i * 560;
        const barH = (k.eff / maxEff) * 300 * p(k.at + 0.06, k.at + 0.2);
        return (
          <React.Fragment key={i}>
            <Card theme={T} x={x} y={230} w={520} h={520} color={k.c} o={p(k.at, k.at + 0.1)}>
              <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 34, color: k.c }}>{k.name}</div>
              <div style={{ fontFamily: MONO, fontSize: 22, color: T.muted, marginTop: 6 }}>{k.look}</div>
              {/* efficiency bar */}
              <div style={{ position: "absolute", left: 40, bottom: 150, display: "flex", alignItems: "flex-end", gap: 16 }}>
                <div style={{ width: 90, height: barH, borderRadius: "8px 8px 0 0", background: `linear-gradient(180deg, ${k.c}, ${mix(k.c, T.bg1, 0.5)})`, border: `2px solid ${k.c}`, borderBottom: "none" }} />
                <div style={{ fontFamily: MONO, fontWeight: 800, fontSize: 44, color: k.c, opacity: p(k.at + 0.1, k.at + 0.2) }}>~{k.eff}%</div>
              </div>
              <div style={{ position: "absolute", left: 36, bottom: 34, width: 448, fontFamily: SANS, fontWeight: 600, fontSize: 24, color: T.text, lineHeight: 1.35 }}>{k.note}</div>
            </Card>
          </React.Fragment>
        );
      })}
      <Foot theme={T} p={p(0.86, 0.94)}>
        For rooftops, mono panels almost always win: more watts from the same area.
      </Foot>
    </Stage>
  );
};

// ============================================================================ DC → AC (inverter)
const DcAcScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const p = usePfull(dur); // sine wave + flows run the whole beat
  const rev = useP(dur);
  // AC sine points after inverter
  const sineX0 = 1180, sineW = 560, sineY = 470, amp = 70;
  const pts = Array.from({ length: 90 }).map((_, i) => {
    const t = i / 89;
    const x = sineX0 + t * sineW;
    const y = sineY + Math.sin(t * Math.PI * 5 - frame * 0.15) * amp;
    return `${x},${y}`;
  }).join(" ");
  return (
    <Stage>
      <Head theme={T} kicker="THE BRAIN OF THE SYSTEM" title="The inverter turns DC into usable AC" color={A.grid} o={rev(0, 0.06)} />
      {/* panel (DC) */}
      <PanelIcon x={130} y={370} w={280} h={200} cols={5} rows={4} color={A.cell} live o={rev(0.08, 0.18)} />
      <div style={{ position: "absolute", left: 130, top: 590, width: 280, textAlign: "center", fontFamily: MONO, fontSize: 23, color: A.cell, opacity: rev(0.12, 0.22) }}>panels make DC — one-way</div>
      <Flow x1={410} y1={470} x2={700} y2={470} color={A.cell} n={7} o={rev(0.2, 0.3)} />
      {/* inverter box */}
      <Card theme={T} x={700} y={360} w={340} h={220} color={A.grid} o={rev(0.28, 0.38)} glow>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 34, color: A.grid }}>Inverter</div>
        <div style={{ fontFamily: MONO, fontSize: 21, color: T.muted, marginTop: 12, lineHeight: 1.5 }}>
          • DC → AC<br />• finds max power (MPPT)<br />• safety + monitoring
        </div>
      </Card>
      {/* AC sine out */}
      <svg style={{ position: "absolute", left: 0, top: 0, overflow: "visible" }} width={1920} height={1080}>
        <polyline points={pts} fill="none" stroke={A.grid} strokeWidth={4} opacity={rev(0.44, 0.54)} />
      </svg>
      <div style={{ position: "absolute", left: sineX0, top: 300, fontFamily: MONO, fontSize: 23, color: A.grid, opacity: rev(0.46, 0.56) }}>AC — the wave your home runs on</div>
      {/* appliances */}
      <div style={{ position: "absolute", left: 1500, top: 590, display: "flex", gap: 22, opacity: rev(0.58, 0.68), fontSize: 56 }}>
        <span>💡</span><span>🌀</span><span>❄️</span>
      </div>
      <div style={{ position: "absolute", left: 130, top: 720, width: 1600, fontFamily: SANS, fontWeight: 700, fontSize: 28, color: T.text, opacity: rev(0.7, 0.8) }}>
        Your lights, fans and fridge all need <span style={{ color: A.grid }}>alternating current</span>. The inverter is what makes rooftop DC usable — it is the piece that fails first, so its quality matters most.
      </div>
      <Foot theme={T} p={rev(0.87, 0.95)}>
        Panels are the muscle; the inverter is the brain.
      </Foot>
    </Stage>
  );
};

// ============================================================================ ON-GRID (net metering)
const OnGridScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const p = usePfull(dur);
  const rev = useP(dur);
  const spin = (frame * 4) % 360;
  return (
    <Stage>
      <Head theme={T} kicker="ON-GRID · NET METERING" title="The grid becomes your free battery" color={A.grid} o={rev(0, 0.06)} />
      {/* house with panels */}
      <div style={{ position: "absolute", left: 160, top: 300, opacity: rev(0.08, 0.16) }}>
        <PanelIcon x={0} y={0} w={300} h={150} cols={6} rows={3} color={A.cell} live />
        <div style={{ position: "absolute", left: 40, top: 160, fontSize: 120 }}>🏠</div>
      </div>
      {/* meter in the middle */}
      <div style={{ position: "absolute", left: 780, top: 360, width: 200, height: 200, borderRadius: 20, background: T.panel, border: `3px solid ${A.grid}`, opacity: rev(0.24, 0.34), display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center" }}>
        <div style={{ width: 90, height: 90, borderRadius: 90, border: `4px solid ${A.grid}`, position: "relative" }}>
          <div style={{ position: "absolute", left: 41, top: 8, width: 4, height: 40, background: A.sun, transformOrigin: "bottom center", transform: `rotate(${spin}deg)` }} />
        </div>
        <div style={{ fontFamily: MONO, fontSize: 20, color: A.grid, marginTop: 10 }}>net meter</div>
      </div>
      {/* grid */}
      <div style={{ position: "absolute", left: 1520, top: 340, textAlign: "center", opacity: rev(0.16, 0.26) }}>
        <div style={{ fontSize: 130 }}>🗼</div>
        <div style={{ fontFamily: MONO, fontSize: 23, color: T.muted }}>the grid</div>
      </div>
      {/* day: export to grid (meter runs back) */}
      <Flow x1={980} y1={430} x2={1480} y2={430} color={A.grid} n={7} o={rev(0.36, 0.46)} />
      <div style={{ position: "absolute", left: 1010, top: 384, fontFamily: MONO, fontSize: 22, color: A.grid, opacity: rev(0.38, 0.48) }}>daytime surplus → sold to the grid</div>
      {/* night: import */}
      <Flow x1={1480} y1={520} x2={980} y2={520} color={A.sun} n={5} o={rev(0.52, 0.62)} />
      <div style={{ position: "absolute", left: 1010, top: 540, fontFamily: MONO, fontSize: 22, color: A.sun, opacity: rev(0.54, 0.64) }}>at night → you draw it back</div>
      <div style={{ position: "absolute", left: 160, top: 720, width: 1600, fontFamily: SANS, fontWeight: 700, fontSize: 28, color: T.text, opacity: rev(0.68, 0.78) }}>
        You are billed only on the <span style={{ color: A.grid }}>net</span> — units drawn minus units sent. No batteries needed. This is the cheapest, most common home setup.
      </div>
      <Foot theme={T} p={rev(0.87, 0.95)}>
        Net metering is why a home solar bill can land near zero.
      </Foot>
    </Stage>
  );
};

// ============================================================================ OFF-GRID / HYBRID (batteries)
const OffGridScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const p = usePfull(dur);
  const rev = useP(dur);
  const charge = (Math.sin(frame * 0.03) + 1) / 2; // battery fills/drains
  return (
    <Stage>
      <Head theme={T} kicker="OFF-GRID & HYBRID" title="When you need to store the sun" color={A.cell} o={rev(0, 0.06)} />
      {/* the battery */}
      <div style={{ position: "absolute", left: 250, top: 300, width: 240, height: 400, borderRadius: 20, border: `4px solid ${A.cell}`, background: T.panel, overflow: "hidden", opacity: rev(0.1, 0.2) }}>
        <div style={{ position: "absolute", bottom: 0, left: 0, right: 0, height: `${charge * 100}%`, background: `linear-gradient(180deg, ${A.grid}, ${mix(A.grid, T.bg1, 0.4)})`, boxShadow: `0 0 26px ${A.grid}` }} />
        <div style={{ position: "absolute", top: 16, left: 0, right: 0, textAlign: "center", fontFamily: MONO, fontWeight: 800, fontSize: 30, color: T.text }}>{Math.round(charge * 100)}%</div>
      </div>
      <div style={{ position: "absolute", left: 250, top: 250, width: 240, textAlign: "center", fontFamily: MONO, fontSize: 24, color: A.cell, opacity: rev(0.12, 0.22) }}>battery</div>
      {/* two modes */}
      <Card theme={T} x={620} y={280} w={560} h={200} color={A.cell} o={rev(0.3, 0.4)}>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 32, color: A.cell }}>Off-grid</div>
        <div style={{ fontFamily: SANS, fontSize: 25, color: T.text, marginTop: 12, lineHeight: 1.4 }}>No grid at all. Batteries carry you through the night. For farms, towers, remote homes.</div>
      </Card>
      <Card theme={T} x={620} y={510} w={560} h={200} color={A.grid} o={rev(0.46, 0.56)}>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 32, color: A.grid }}>Hybrid</div>
        <div style={{ fontFamily: SANS, fontSize: 25, color: T.text, marginTop: 12, lineHeight: 1.4 }}>Grid + battery backup. Keeps lights on during cuts. Popular where power is unreliable.</div>
      </Card>
      <div style={{ position: "absolute", left: 1240, top: 300, width: 560, opacity: rev(0.62, 0.72) }}>
        <div style={{ fontFamily: SANS, fontWeight: 700, fontSize: 29, color: T.text, lineHeight: 1.45 }}>
          Batteries add <span style={{ color: A.hot }}>cost and complexity</span>. Most homes with a stable grid skip them and choose net metering instead.
        </div>
      </div>
      <Foot theme={T} p={rev(0.87, 0.95)}>
        Store the sun only when you must — every battery you add stretches the payback.
      </Foot>
    </Stage>
  );
};

// ============================================================================ COMPONENTS (BOM + cost share)
const ComponentsScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur);
  const parts = [
    { at: 0.1, name: "Solar panels", share: 52, c: A.cell },
    { at: 0.2, name: "Inverter", share: 14, c: A.grid },
    { at: 0.3, name: "Mounting structure", share: 12, c: A.biz },
    { at: 0.4, name: "Cables, meter, safety (BOS)", share: 12, c: A.sun },
    { at: 0.5, name: "Installation & labour", share: 10, c: A.hot },
  ];
  const X0 = 200, W = 820, rowH = 96, Y0 = 250;
  return (
    <Stage>
      <Head theme={T} kicker="WHAT'S IN A SYSTEM" title="Where the money goes" color={A.sun} o={p(0, 0.06)} />
      {parts.map((pt, i) => {
        const y = Y0 + i * rowH;
        const w = (pt.share / 52) * W * p(pt.at + 0.04, pt.at + 0.16);
        return (
          <React.Fragment key={i}>
            <div style={{ position: "absolute", left: X0, top: y, width: 360, fontFamily: SANS, fontWeight: 700, fontSize: 28, color: T.text, opacity: p(pt.at, pt.at + 0.06) }}>{pt.name}</div>
            <div style={{ position: "absolute", left: X0 + 380, top: y - 6, width: w, height: 52, borderRadius: "8px 14px 14px 8px", background: `linear-gradient(90deg, ${mix(pt.c, T.bg1, 0.45)}, ${pt.c})`, border: `2px solid ${pt.c}` }} />
            <div style={{ position: "absolute", left: X0 + 380 + w + 14, top: y, fontFamily: MONO, fontWeight: 800, fontSize: 30, color: pt.c, opacity: p(pt.at + 0.06, pt.at + 0.16) }}>~{pt.share}%</div>
          </React.Fragment>
        );
      })}
      <Card theme={T} x={1240} y={548} w={580} h={280} color={A.cell} o={p(0.6, 0.7)} glow>
        <div style={{ fontFamily: SANS, fontWeight: 700, fontSize: 27, color: T.text, lineHeight: 1.4 }}>
          Panels are half the bill of materials. That's why <span style={{ color: A.cell }}>sourcing</span> and <span style={{ color: A.grid }}>install quality</span> decide your margin — not any single gadget.
        </div>
      </Card>
      <Foot theme={T} p={p(0.86, 0.94)}>
        Illustrative split for a typical Indian rooftop system — it shifts with battery and brand.
      </Foot>
    </Stage>
  );
};

// ============================================================================ SIZING (computed)
const SizingScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = usePfull(dur); // counters track the beat
  const units = 600;         // monthly units
  const perKwMonth = 120;    // 1 kW ≈ 4 units/day ≈ 120/month
  const kw = units / perKwMonth; // 5 kW
  const area = kw * 100;     // ~100 sqft/kW
  return (
    <Stage>
      <Head theme={T} kicker="SIZING A SYSTEM" title="Read the bill, size the roof" color={A.grid} o={p(0, 0.06)} />
      {/* step 1: the bill */}
      <Card theme={T} x={130} y={260} w={520} h={230} color={A.hot} o={p(0.08, 0.18)}>
        <div style={{ fontFamily: MONO, fontSize: 23, color: T.muted }}>from the electricity bill</div>
        <div style={{ display: "flex", alignItems: "baseline", gap: 12, marginTop: 14 }}>
          <Counter p={p(0.12, 0.26)} to={units} comma color={A.hot} size={72} />
          <span style={{ fontFamily: SANS, fontWeight: 700, fontSize: 30, color: T.text }}>units / month</span>
        </div>
      </Card>
      <div style={{ position: "absolute", left: 690, top: 340, fontFamily: SANS, fontWeight: 800, fontSize: 60, color: T.muted, opacity: p(0.28, 0.36) }}>÷</div>
      <Card theme={T} x={780} y={260} w={430} h={230} color={A.cell} o={p(0.3, 0.4)}>
        <div style={{ fontFamily: MONO, fontSize: 23, color: T.muted }}>each kW makes / month</div>
        <div style={{ display: "flex", alignItems: "baseline", gap: 12, marginTop: 14 }}>
          <span style={{ fontFamily: MONO, fontWeight: 800, fontSize: 72, color: A.cell }}>~120</span>
          <span style={{ fontFamily: SANS, fontWeight: 700, fontSize: 26, color: T.text }}>units</span>
        </div>
      </Card>
      <div style={{ position: "absolute", left: 1250, top: 340, fontFamily: SANS, fontWeight: 800, fontSize: 60, color: T.muted, opacity: p(0.44, 0.52) }}>=</div>
      <Card theme={T} x={1340} y={260} w={460} h={230} color={A.grid} o={p(0.46, 0.56)} glow>
        <div style={{ fontFamily: MONO, fontSize: 23, color: T.muted }}>system you need</div>
        <div style={{ display: "flex", alignItems: "baseline", gap: 12, marginTop: 14 }}>
          <Counter p={p(0.46, 0.6)} to={kw} decimals={0} color={A.grid} size={80} suffix=" kW" />
        </div>
      </Card>
      {/* step 2: area */}
      <div style={{ position: "absolute", left: 130, top: 560, width: 1670, opacity: p(0.66, 0.76) }}>
        <div style={{ fontFamily: SANS, fontWeight: 700, fontSize: 30, color: T.text }}>
          A rooftop needs about <span style={{ color: A.sun }}>100 sq ft per kW</span> of shade-free space —
        </div>
        <div style={{ display: "flex", alignItems: "baseline", gap: 14, marginTop: 16 }}>
          <span style={{ fontFamily: SANS, fontWeight: 700, fontSize: 30, color: T.text }}>so this home wants roughly</span>
          <Counter p={p(0.72, 0.84)} to={area} comma color={A.sun} size={56} suffix=" sq ft" />
        </div>
      </div>
      <Foot theme={T} p={p(0.88, 0.95)}>
        This one back-of-envelope sum is the first thing you do on every sales call.
      </Foot>
    </Stage>
  );
};

// ============================================================================ ROOFTOP (survey)
const RooftopScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const checks = [
    { at: 0.12, t: "Faces south (in India)", c: A.sun },
    { at: 0.24, t: "Tilted ~15–25° for the year", c: A.cell },
    { at: 0.36, t: "Shade-free 9am–3pm", c: A.grid },
    { at: 0.48, t: "Roof can bear the weight", c: A.biz },
  ];
  const sunX = 300 + ((frame * 1.2) % 900);
  return (
    <Stage>
      <Head theme={T} kicker="THE ROOF SURVEY" title="Not every roof is a good roof" color={A.cell} o={p(0, 0.06)} />
      {/* sun arc + roof */}
      <div style={{ position: "absolute", left: sunX, top: 220 + Math.sin(((sunX - 300) / 900) * Math.PI) * -60 + 60, fontSize: 48, opacity: p(0.1, 0.2) }}>☀️</div>
      <div style={{ position: "absolute", left: 250, top: 430, width: 620, height: 30, background: mix(T.panel, A.cell, 0.3), border: `2px solid ${A.cell}`, borderRadius: 6, transform: "rotate(-14deg)", opacity: p(0.14, 0.24) }} />
      <div style={{ position: "absolute", left: 300, top: 470, fontSize: 90, opacity: p(0.14, 0.24) }}>🏠</div>
      {/* shadow hazard */}
      <div style={{ position: "absolute", left: 700, top: 520, fontSize: 60, opacity: p(0.3, 0.4) }}>🌳</div>
      <div style={{ position: "absolute", left: 660, top: 610, fontFamily: MONO, fontSize: 20, color: A.hot, opacity: p(0.32, 0.42) }}>even one shadow hurts a whole string</div>
      {/* checklist */}
      <div style={{ position: "absolute", left: 1050, top: 260, width: 760 }}>
        {checks.map((c, i) => (
          <div key={i} style={{ display: "flex", alignItems: "center", gap: 18, height: 92, opacity: p(c.at, c.at + 0.08) }}>
            <div style={{ width: 46, height: 46, borderRadius: 12, background: mix(T.panel, c.c, 0.25), border: `2.5px solid ${c.c}`, display: "flex", alignItems: "center", justifyContent: "center", fontFamily: MONO, fontWeight: 800, color: c.c, fontSize: 26 }}>✓</div>
            <span style={{ fontFamily: SANS, fontWeight: 700, fontSize: 32, color: T.text }}>{c.t}</span>
          </div>
        ))}
      </div>
      <Foot theme={T} p={p(0.86, 0.94)}>
        Orientation, tilt, shade, strength — the survey decides how much power the roof will really give.
      </Foot>
    </Stage>
  );
};

// ============================================================================ INSTALL (steps)
const InstallScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const p = usePfull(dur);
  const steps = [
    "Survey & design", "DISCOM application", "Mount the structure",
    "Fix the panels", "Wire the inverter", "Net meter + inspection", "Switch on + subsidy",
  ];
  const hot = Math.floor(frame / 24) % steps.length;
  const railFill = p(0.1, 0.86);
  const X0 = 160, W = 1600, y = 470;
  return (
    <Stage>
      <Head theme={T} kicker="THE INSTALL" title="From survey to switch-on" color={A.sun} o={usePfull(dur)(0, 0.06)} />
      {/* rail */}
      <div style={{ position: "absolute", left: X0, top: y, width: W, height: 5, background: T.line, borderRadius: 3 }} />
      <div style={{ position: "absolute", left: X0, top: y, width: W * railFill, height: 5, background: `linear-gradient(90deg, ${A.sun}, ${A.grid})`, borderRadius: 3, boxShadow: `0 0 12px ${A.sun}` }} />
      {steps.map((s, i) => {
        const x = X0 + (i / (steps.length - 1)) * W;
        const at = 0.08 + i * 0.1;
        const on = p(at, at + 0.06) > 0.4;
        const active = hot === i;
        return (
          <React.Fragment key={i}>
            <div style={{ position: "absolute", left: x - 30, top: y - 27, width: 60, height: 60, borderRadius: 30, background: on ? mix(T.panel, active ? A.sun : A.grid, 0.4) : T.panel, border: `3px solid ${on ? (active ? A.sun : A.grid) : T.line}`, display: "flex", alignItems: "center", justifyContent: "center", fontFamily: MONO, fontWeight: 800, fontSize: 26, color: on ? (active ? A.sun : A.grid) : T.muted, boxShadow: active ? `0 0 22px ${A.sun}` : "none", transform: `scale(${active ? 1.12 : 1})` }}>{i + 1}</div>
            <div style={{ position: "absolute", left: x - 100, top: i % 2 === 0 ? y - 130 : y + 50, width: 200, textAlign: "center", fontFamily: SANS, fontWeight: 700, fontSize: 24, color: active ? A.sun : T.text, opacity: on ? 1 : 0.3 }}>{s}</div>
          </React.Fragment>
        );
      })}
      <div style={{ position: "absolute", left: X0, top: 700, width: W, textAlign: "center", fontFamily: SANS, fontWeight: 700, fontSize: 28, color: T.text, opacity: p(0.7, 0.8) }}>
        A home install is usually <span style={{ color: A.grid }}>1–3 days of work</span> — but paperwork with the DISCOM is what stretches the timeline to weeks.
      </div>
      <Foot theme={T} p={p(0.87, 0.95)}>
        The technical part is fast; approvals and net-meter inspection are the slow part.
      </Foot>
    </Stage>
  );
};

// ============================================================================ SAVINGS (payback line, computed)
const SavingsScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const p = usePfull(dur);
  // 3 kW system: net cost ~₹1.0L after subsidy; savings ~₹28k/yr
  const netCost = 102000;
  const perYear = 28000;
  const years = 12;
  const X0 = 240, Y0 = 760, W = 1000, H = 480;
  const maxRs = 336000; // 12 yr savings
  const sweep = p(0.16, 0.85);
  const nShown = Math.max(1, Math.round(years * sweep));
  const pts = Array.from({ length: nShown + 1 }).map((_, i) => {
    const x = X0 + (i / years) * W;
    const yv = Y0 - (perYear * i / maxRs) * H;
    return `${x},${yv}`;
  }).join(" ");
  const costY = Y0 - (netCost / maxRs) * H;
  const paybackYr = netCost / perYear; // ~3.6
  const paybackX = X0 + (paybackYr / years) * W;
  return (
    <Stage>
      <Head theme={T} kicker="THE PAYBACK" title="A few years to free — then decades of it" color={A.grid} o={useP(dur)(0, 0.06)} />
      <svg style={{ position: "absolute", left: 0, top: 0, overflow: "visible" }} width={1920} height={1080}>
        <line x1={X0} y1={Y0} x2={X0 + W} y2={Y0} stroke={T.line} strokeWidth={2} />
        <line x1={X0} y1={Y0} x2={X0} y2={Y0 - H - 10} stroke={T.line} strokeWidth={2} />
        {/* cost line (what you paid) */}
        <line x1={X0} y1={costY} x2={X0 + W} y2={costY} stroke={A.hot} strokeWidth={3} strokeDasharray="8 8" opacity={useP(dur)(0.24, 0.34)} />
        {/* cumulative savings */}
        <polyline points={pts} fill="none" stroke={A.grid} strokeWidth={5} />
        {sweep > paybackYr / years && <circle cx={paybackX} cy={costY} r={12} fill={A.sun} stroke={T.text} strokeWidth={2} />}
      </svg>
      <div style={{ position: "absolute", left: X0 + W - 260, top: costY - 40, fontFamily: MONO, fontWeight: 800, fontSize: 26, color: A.hot, opacity: useP(dur)(0.26, 0.36) }}>what you paid ≈ ₹1.0 L</div>
      <div style={{ position: "absolute", left: paybackX - 60, top: costY - 90, width: 260, textAlign: "center", fontFamily: MONO, fontWeight: 800, fontSize: 26, color: A.sun, opacity: sweep > paybackYr / years ? 1 : 0 }}>paid back<br />~year 3.6</div>
      <div style={{ position: "absolute", left: X0 + 40, top: Y0 + 16, fontFamily: MONO, fontSize: 22, color: T.muted }}>year 0</div>
      <div style={{ position: "absolute", left: X0 + W - 40, top: Y0 + 16, fontFamily: MONO, fontSize: 22, color: T.muted }}>year 12</div>
      {/* readouts */}
      <div style={{ position: "absolute", left: 1320, top: 250, width: 520 }}>
        <Pill label="system" value="3 kW rooftop" color={A.cell} o={useP(dur)(0.4, 0.5)} />
        <div style={{ height: 16 }} />
        <Pill label="net cost" value="≈ ₹1.0 lakh" color={A.hot} o={useP(dur)(0.44, 0.54)} />
        <div style={{ height: 16 }} />
        <Pill label="saves/yr" value="≈ ₹28,000" color={A.grid} o={useP(dur)(0.48, 0.58)} />
        <div style={{ marginTop: 26, fontFamily: SANS, fontWeight: 700, fontSize: 29, color: T.text, lineHeight: 1.4, opacity: useP(dur)(0.62, 0.74) }}>
          Panels are warrantied for <span style={{ color: A.sun }}>25 years</span>. After payback, the power is
          essentially <span style={{ color: A.grid }}>free</span> for two more decades.
        </div>
      </div>
      <Foot theme={T} p={useP(dur)(0.88, 0.95)}>
        Illustrative: exact payback depends on your tariff, usage, and shade — usually 3.5 to 5 years.
      </Foot>
    </Stage>
  );
};

// ============================================================================ SUBSIDY (PM Surya Ghar, computed)
const SubsidyScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur);
  // slabs: 30k/kW first 2, 18k for 3rd, cap 78k
  const sizes = [
    { at: 0.14, kw: "1 kW", sub: 30000 },
    { at: 0.26, kw: "2 kW", sub: 60000 },
    { at: 0.38, kw: "3 kW", sub: 78000 },
    { at: 0.5, kw: "5 kW", sub: 78000, capped: true },
  ];
  const maxSub = 90000, X0 = 200, W = 760, Y0 = 250, rowH = 116;
  return (
    <Stage>
      <Head theme={T} kicker="PM SURYA GHAR — THE SUBSIDY" title="The government pays part of the roof" color={A.sun} o={p(0, 0.06)} />
      {sizes.map((s, i) => {
        const y = Y0 + i * rowH;
        const w = (s.sub / maxSub) * W * p(s.at + 0.04, s.at + 0.16);
        return (
          <React.Fragment key={i}>
            <div style={{ position: "absolute", left: X0, top: y + 6, width: 130, fontFamily: SANS, fontWeight: 800, fontSize: 34, color: A.cell, opacity: p(s.at, s.at + 0.06) }}>{s.kw}</div>
            <div style={{ position: "absolute", left: X0 + 150, top: y, width: w, height: 62, borderRadius: "8px 16px 16px 8px", background: `linear-gradient(90deg, ${mix(A.sun, T.bg1, 0.45)}, ${A.sun})`, border: `2px solid ${A.sun}` }} />
            <div style={{ position: "absolute", left: X0 + 150 + w + 16, top: y + 8, fontFamily: MONO, fontWeight: 800, fontSize: 34, color: A.sun, opacity: p(s.at + 0.06, s.at + 0.16) }}>
              ₹{s.sub.toLocaleString("en-IN")}{s.capped ? "  (capped)" : ""}
            </div>
          </React.Fragment>
        );
      })}
      <Card theme={T} x={1240} y={250} w={580} h={340} color={A.sun} o={p(0.62, 0.72)} glow>
        <div style={{ fontFamily: MONO, fontSize: 22, color: T.muted }}>the slab</div>
        <div style={{ fontFamily: SANS, fontWeight: 700, fontSize: 27, color: T.text, marginTop: 12, lineHeight: 1.45 }}>
          <span style={{ color: A.sun }}>₹30,000</span> per kW for the first 2 kW, <span style={{ color: A.sun }}>₹18,000</span> for the 3rd — capped at <span style={{ color: A.sun }}>₹78,000</span>.
        </div>
        <div style={{ fontFamily: MONO, fontSize: 21, color: A.grid, marginTop: 18, lineHeight: 1.4 }}>
          Paid to the bank account after inspection. Many states add a top-up.
        </div>
      </Card>
      <Foot theme={T} p={p(0.86, 0.94)}>
        For a salesperson, the subsidy is the closing argument — it cuts the price a third or more.
      </Foot>
    </Stage>
  );
};

// ============================================================================ C&I (why businesses)
const CniScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur);
  const rows = [
    { at: 0.12, label: "Home", bill: "₹3–8k / month", kw: "2–5 kW", c: A.grid, h: 90 },
    { at: 0.3, label: "Shop / office", bill: "₹20–60k / month", kw: "10–50 kW", c: A.cell, h: 200 },
    { at: 0.48, label: "Factory / warehouse", bill: "₹2–20 lakh / month", kw: "100 kW – MWs", c: A.biz, h: 340 },
  ];
  return (
    <Stage>
      <Head theme={T} kicker="THE COMMERCIAL PRIZE" title="Businesses have the big bills" color={A.biz} o={p(0, 0.06)} />
      {rows.map((r, i) => {
        const x = 200 + i * 520;
        return (
          <React.Fragment key={i}>
            <div style={{ position: "absolute", left: x, top: 720 - r.h, width: 300, height: r.h, borderRadius: "14px 14px 0 0", background: `linear-gradient(180deg, ${r.c}, ${mix(r.c, T.bg1, 0.5)})`, border: `2.5px solid ${r.c}`, borderBottom: "none", opacity: p(r.at, r.at + 0.12) }} />
            <div style={{ position: "absolute", left: x, top: 736, width: 300, textAlign: "center", fontFamily: SANS, fontWeight: 800, fontSize: 30, color: T.text, opacity: p(r.at, r.at + 0.08) }}>{r.label}</div>
            <div style={{ position: "absolute", left: x, top: 776, width: 300, textAlign: "center", fontFamily: MONO, fontSize: 22, color: r.c, opacity: p(r.at + 0.04, r.at + 0.12) }}>{r.bill}</div>
            <div style={{ position: "absolute", left: x, top: 690 - r.h, width: 300, textAlign: "center", fontFamily: MONO, fontWeight: 800, fontSize: 26, color: r.c, opacity: p(r.at + 0.06, r.at + 0.16) }}>{r.kw}</div>
          </React.Fragment>
        );
      })}
      <div style={{ position: "absolute", left: 130, top: 250, width: 980, opacity: p(0.64, 0.76) }}>
        <div style={{ fontFamily: SANS, fontWeight: 700, fontSize: 30, color: T.text, lineHeight: 1.45 }}>
          Commercial tariffs are <span style={{ color: A.hot }}>higher</span> than home rates, and factories run in the
          <span style={{ color: A.sun }}> daytime</span> — exactly when the sun shines. So each panel saves more.
        </div>
      </div>
      <Foot theme={T} p={p(0.86, 0.94)}>
        One factory rooftop can equal hundreds of homes in size — and in revenue.
      </Foot>
    </Stage>
  );
};

// ============================================================================ MODELS (CAPEX vs OPEX)
const ModelsScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur);
  return (
    <Stage>
      <Head theme={T} kicker="HOW BUSINESSES PAY" title="Two ways to fund a commercial system" color={A.biz} o={p(0, 0.06)} />
      <Card theme={T} x={130} y={240} w={800} h={520} color={A.cell} o={p(0.1, 0.2)}>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 40, color: A.cell }}>CAPEX — they own it</div>
        <div style={{ fontFamily: MONO, fontSize: 23, color: T.muted, marginTop: 8 }}>the business buys the system</div>
        <div style={{ marginTop: 26, fontFamily: SANS, fontSize: 27, color: T.text, lineHeight: 1.7 }}>
          • Pays upfront (or loan)<br />
          • Keeps 100% of the savings<br />
          • Gets tax depreciation benefit<br />
          • Payback in <span style={{ color: A.grid }}>3–4 years</span>, then free
        </div>
      </Card>
      <Card theme={T} x={990} y={240} w={800} h={520} color={A.grid} o={p(0.32, 0.42)} glow>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 40, color: A.grid }}>OPEX / RESCO — you own it</div>
        <div style={{ fontFamily: MONO, fontSize: 23, color: T.muted, marginTop: 8 }}>a developer builds it on their roof</div>
        <div style={{ marginTop: 26, fontFamily: SANS, fontSize: 27, color: T.text, lineHeight: 1.7 }}>
          • Business pays <span style={{ color: A.sun }}>zero upfront</span><br />
          • Buys the power at a discount (a PPA)<br />
          • You earn for 15–25 years<br />
          • <span style={{ color: A.biz }}>60–70%</span> of commercial deals use this
        </div>
      </Card>
      <Foot theme={T} p={p(0.7, 0.82)}>
        CAPEX suits cash-rich firms; OPEX wins everyone else — and it's where the recurring money is.
      </Foot>
    </Stage>
  );
};

// ============================================================================ BIZ CASE (commercial ROI, computed)
const BizCaseScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const p = usePfull(dur);
  const kw = 100, costPerKw = 45000;
  const cost = kw * costPerKw;              // ₹45 L
  const unitsYr = kw * 4 * 330;             // ~132,000 units/yr
  const tariff = 9;
  const saveYr = unitsYr * tariff;          // ₹11.88 L
  const payback = cost / saveYr;            // ~3.8 yr
  const life = 25;
  const lifeSave = saveYr * life;           // ~₹2.97 Cr
  return (
    <Stage>
      <Head theme={T} kicker="A COMMERCIAL EXAMPLE" title="A 100 kW factory rooftop" color={A.biz} o={useP(dur)(0, 0.06)} />
      {[
        { at: 0.1, label: "system cost", to: cost, c: A.hot, pre: "₹", suf: "" },
        { at: 0.26, label: "units / year", to: unitsYr, c: A.cell, pre: "", suf: " kWh" },
        { at: 0.42, label: "saved / year", to: saveYr, c: A.grid, pre: "₹", suf: "" },
      ].map((r, i) => (
        <Card key={i} theme={T} x={130 + i * 560} y={250} w={520} h={220} color={r.c} o={useP(dur)(r.at, r.at + 0.1)}>
          <div style={{ fontFamily: MONO, fontSize: 23, color: T.muted }}>{r.label}</div>
          <div style={{ marginTop: 16 }}>
            <Counter p={p(r.at + 0.02, r.at + 0.18)} to={r.to} comma color={r.c} size={56} prefix={r.pre} suffix={r.suf} />
          </div>
        </Card>
      ))}
      <div style={{ position: "absolute", left: 130, top: 540, display: "flex", gap: 40, alignItems: "center", opacity: useP(dur)(0.6, 0.72) }}>
        <div>
          <div style={{ fontFamily: MONO, fontSize: 24, color: T.muted }}>pays for itself in</div>
          <Counter p={p(0.54, 0.68)} to={payback} decimals={1} color={A.sun} size={80} suffix=" years" />
        </div>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 60, color: T.muted }}>→</div>
        <div>
          <div style={{ fontFamily: MONO, fontSize: 24, color: T.muted }}>saved over 25 years</div>
          <div style={{ fontFamily: MONO, fontWeight: 800, fontSize: 80, color: A.grid }}>≈ ₹3 crore</div>
        </div>
      </div>
      <Foot theme={T} p={useP(dur)(0.88, 0.95)}>
        Illustrative at ₹9/unit. Add accelerated depreciation and the returns look even better.
      </Foot>
    </Stage>
  );
};

// ============================================================================ VALUE CHAIN
const ValueChainScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const nodes = [
    { at: 0.1, name: "Manufacture", cap: "very high", c: A.hot, hard: true },
    { at: 0.2, name: "Distribute", cap: "high", c: A.biz, hard: true },
    { at: 0.3, name: "EPC / Install", cap: "medium", c: A.cell, hard: false },
    { at: 0.4, name: "Sell / Dealer", cap: "low", c: A.grid, hard: false },
    { at: 0.5, name: "Refer / O&M", cap: "tiny", c: A.sun, hard: false },
  ];
  const X0 = 140, gap = 350, y = 400;
  const hot = Math.floor(frame / 22) % nodes.length;
  return (
    <Stage>
      <Head theme={T} kicker="WHERE YOU CAN PLAY" title="Pick your spot in the chain" color={A.biz} o={p(0, 0.06)} />
      {nodes.map((n, i) => {
        const x = X0 + i * gap;
        const active = hot === i;
        return (
          <React.Fragment key={i}>
            {i < nodes.length - 1 && <Wire x1={x + 250} y1={y + 70} x2={x + gap} y2={y + 70} p={p(n.at + 0.04, n.at + 0.12)} color={T.muted} />}
            <div style={{ position: "absolute", left: x, top: y, width: 250, height: 140, borderRadius: 18, background: mix(T.panel, n.c, active ? 0.28 : 0.12), border: `3px solid ${n.c}`, opacity: p(n.at, n.at + 0.08), display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", boxShadow: active ? `0 0 24px ${mix(T.bg0, n.c, 0.5)}` : "none", transform: `scale(${active ? 1.05 : 1})` }}>
              <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 30, color: T.text }}>{n.name}</div>
              <div style={{ fontFamily: MONO, fontSize: 21, color: n.c, marginTop: 8 }}>capital: {n.cap}</div>
            </div>
            <div style={{ position: "absolute", left: x, top: y + 156, width: 250, textAlign: "center", fontFamily: MONO, fontSize: 21, color: n.hard ? A.hot : A.grid, opacity: p(n.at + 0.06, n.at + 0.16) }}>
              {n.hard ? "hard to enter" : "start here ✓"}
            </div>
          </React.Fragment>
        );
      })}
      <div style={{ position: "absolute", left: 140, top: 650, width: 1670, textAlign: "center", fontFamily: SANS, fontWeight: 700, fontSize: 29, color: T.text, opacity: p(0.66, 0.78) }}>
        You do <span style={{ color: A.hot }}>not</span> need a factory. Most people enter on the right — referring, selling, or installing — where capital is small and demand is huge.
      </div>
      <Foot theme={T} p={p(0.86, 0.94)}>
        The closer you are to the customer, the less money you need to start.
      </Foot>
    </Stage>
  );
};

// ============================================================================ CHANNELS (ways to sell)
const ChannelsScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur);
  const ch = [
    { at: 0.1, name: "Referral / affiliate", cap: "₹0", margin: "₹2–5k per lead", c: A.sun, note: "send buyers to an installer; get paid per closed job" },
    { at: 0.24, name: "Dealer / reseller", cap: "₹1–5 L stock", margin: "10–18%", c: A.grid, note: "buy hardware, sell + arrange install" },
    { at: 0.38, name: "EPC / turnkey", cap: "₹5–20 L", margin: "15–25%", c: A.cell, note: "design, supply and install end-to-end" },
    { at: 0.52, name: "Franchise", cap: "₹3–10 L", margin: "brand + leads", c: A.biz, note: "ride a known name (Tata, Luminous, Waaree…)" },
  ];
  return (
    <Stage>
      <Head theme={T} kicker="WAYS TO SELL SOLAR" title="Four doors into the business" color={A.biz} o={p(0, 0.06)} />
      {ch.map((c, i) => {
        const x = 130 + (i % 2) * 880;
        const y = 240 + Math.floor(i / 2) * 280;
        return (
          <Card key={i} theme={T} x={x} y={y} w={810} h={250} color={c.c} o={p(c.at, c.at + 0.1)}>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "baseline" }}>
              <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 34, color: c.c }}>{c.name}</div>
              <div style={{ fontFamily: MONO, fontWeight: 800, fontSize: 30, color: A.grid }}>{c.margin}</div>
            </div>
            <div style={{ fontFamily: MONO, fontSize: 22, color: T.muted, marginTop: 12 }}>capital to start: <span style={{ color: c.c }}>{c.cap}</span></div>
            <div style={{ fontFamily: SANS, fontSize: 25, color: T.text, marginTop: 16, lineHeight: 1.4 }}>{c.note}</div>
          </Card>
        );
      })}
      <Foot theme={T} p={p(0.84, 0.92)}>
        Start light with referrals, build trust and reviews, then grow into stocking and installing.
      </Foot>
    </Stage>
  );
};

// ============================================================================ MARGINS (computed comparison)
const MarginsScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur);
  const rows = [
    { at: 0.12, label: "Panels (hardware)", lo: 8, hi: 12, c: A.cell },
    { at: 0.24, label: "Inverter & battery", lo: 12, hi: 20, c: A.grid },
    { at: 0.36, label: "EPC / installation", lo: 15, hi: 25, c: A.sun },
    { at: 0.48, label: "Dealer (blended)", lo: 20, hi: 35, c: A.biz },
  ];
  const X0 = 200, W = 900, Y0 = 250, rowH = 116, maxPct = 40;
  return (
    <Stage>
      <Head theme={T} kicker="WHAT YOU KEEP" title="Margins, layer by layer" color={A.biz} o={p(0, 0.06)} />
      {rows.map((r, i) => {
        const y = Y0 + i * rowH;
        const grow = p(r.at + 0.04, r.at + 0.18);
        const loW = (r.lo / maxPct) * W;
        const hiW = (r.hi / maxPct) * W * grow;
        return (
          <React.Fragment key={i}>
            <div style={{ position: "absolute", left: X0, top: y + 6, width: 380, fontFamily: SANS, fontWeight: 700, fontSize: 28, color: T.text, opacity: p(r.at, r.at + 0.06) }}>{r.label}</div>
            <div style={{ position: "absolute", left: X0 + 400, top: y, width: hiW, height: 56, borderRadius: "8px 14px 14px 8px", background: `linear-gradient(90deg, ${mix(r.c, T.bg1, 0.5)}, ${r.c})`, border: `2px solid ${r.c}` }} />
            <div style={{ position: "absolute", left: X0 + 400 + loW - 2, top: y - 6, width: 3, height: 68, background: T.text, opacity: grow * 0.5 }} />
            <div style={{ position: "absolute", left: X0 + 400 + hiW + 14, top: y + 6, fontFamily: MONO, fontWeight: 800, fontSize: 30, color: r.c, opacity: grow }}>{r.lo}–{r.hi}%</div>
          </React.Fragment>
        );
      })}
      <Card theme={T} x={1360} y={250} w={460} h={340} color={A.hot} o={p(0.62, 0.72)}>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 30, color: A.hot }}>The honest catch</div>
        <div style={{ fontFamily: SANS, fontSize: 25, color: T.text, marginTop: 16, lineHeight: 1.45 }}>
          Headline margins look great, but <span style={{ color: A.hot }}>soft costs</span> — failed site visits, redesigns, delays, marketing — quietly eat <span style={{ color: A.hot }}>5–10%</span>. Competition keeps squeezing.
        </div>
      </Card>
      <Foot theme={T} p={p(0.86, 0.94)}>
        Illustrative India ranges. Service and design earn more than reselling boxes.
      </Foot>
    </Stage>
  );
};

// ============================================================================ ECONOMICS (per-project P&L, computed)
const EconomicsScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur);
  // 5 kW residential job
  const revenue = 325000;
  const items = [
    { at: 0.16, label: "Panels", v: 160000, c: A.cell },
    { at: 0.26, label: "Inverter", v: 45000, c: A.grid },
    { at: 0.36, label: "Structure + BOS", v: 40000, c: A.biz },
    { at: 0.46, label: "Labour + soft costs", v: 42000, c: A.hot },
  ];
  const cogs = items.reduce((s, it) => s + it.v, 0); // 287000
  const profit = revenue - cogs; // 38000
  const X0 = 200, W = 1000, Y0 = 300, barTop = 300;
  const scale = W / revenue;
  return (
    <Stage>
      <Head theme={T} kicker="ONE PROJECT'S P&L" title="A 5 kW home job, rupee by rupee" color={A.grid} o={p(0, 0.06)} />
      {/* revenue bar */}
      <div style={{ position: "absolute", left: X0, top: barTop, fontFamily: MONO, fontSize: 23, color: A.grid, opacity: p(0.08, 0.16) }}>you charge the customer</div>
      <div style={{ position: "absolute", left: X0, top: barTop + 34, width: revenue * scale * p(0.1, 0.24), height: 66, borderRadius: 12, background: `linear-gradient(90deg, ${A.grid}, ${mix(A.grid, T.bg1, 0.4)})`, border: `2.5px solid ${A.grid}` }} />
      <div style={{ position: "absolute", left: X0 + revenue * scale + 16, top: barTop + 46, fontFamily: MONO, fontWeight: 800, fontSize: 34, color: A.grid, opacity: p(0.16, 0.26) }}>₹3.25 L</div>
      {/* cost segments stacked */}
      <div style={{ position: "absolute", left: X0, top: barTop + 150, fontFamily: MONO, fontSize: 23, color: A.hot, opacity: p(0.14, 0.22) }}>your costs</div>
      {(() => { let acc = 0; return items.map((it, i) => {
        const left = X0 + acc * scale;
        const w = it.v * scale * p(it.at, it.at + 0.1);
        acc += it.v;
        return (
          <React.Fragment key={i}>
            <div style={{ position: "absolute", left, top: barTop + 184, width: w, height: 66, background: `linear-gradient(180deg, ${it.c}, ${mix(it.c, T.bg1, 0.5)})`, borderRight: `3px solid ${T.bg0}` }} />
            <div style={{ position: "absolute", left: left + 4, top: barTop + 256, width: it.v * scale, fontFamily: MONO, fontSize: 19, color: it.c, opacity: p(it.at + 0.04, it.at + 0.12), textAlign: "center" }}>{it.label}<br />₹{(it.v / 1000).toFixed(0)}k</div>
          </React.Fragment>
        );
      }); })()}
      {/* profit */}
      <div style={{ position: "absolute", left: X0, top: 720, display: "flex", alignItems: "baseline", gap: 24, opacity: p(0.66, 0.78) }}>
        <span style={{ fontFamily: SANS, fontWeight: 800, fontSize: 36, color: T.text }}>Gross profit ≈</span>
        <Counter p={p(0.7, 0.84)} to={profit} comma prefix="₹" color={A.sun} size={64} />
        <span style={{ fontFamily: MONO, fontSize: 30, color: A.sun }}>(~12%)</span>
      </div>
      <div style={{ position: "absolute", left: 1360, top: 320, width: 460, fontFamily: SANS, fontWeight: 700, fontSize: 27, color: T.text, opacity: p(0.6, 0.72), lineHeight: 1.45 }}>
        Do a few of these a month, add <span style={{ color: A.biz }}>maintenance contracts</span>, and the recurring income is the real prize.
      </div>
      <Foot theme={T} p={p(0.88, 0.95)}>
        Illustrative. Buy better, install cleanly, and cut soft costs — that's the whole game.
      </Foot>
    </Stage>
  );
};

// ============================================================================ GET STARTED
const GetStartedScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const p = usePfull(dur);
  const steps = [
    { n: 1, t: "Learn the basics", d: "sizing, wiring, DISCOM rules — free MNRE + YouTube", c: A.sun },
    { n: 2, t: "Tie up supply", d: "a distributor for ALMM/BIS-approved panels & inverters", c: A.cell },
    { n: 3, t: "Register as a vendor", d: "on the national portal + your state DISCOM", c: A.grid },
    { n: 4, t: "Start with referrals", d: "close a few jobs, collect reviews and photos", c: A.biz },
    { n: 5, t: "Grow into EPC", d: "stock, hire an installer, add AMC contracts", c: A.hot },
  ];
  const hot = Math.floor(frame / 22) % steps.length;
  const railFill = usePfull(dur)(0.1, 0.86);
  const y0 = 220, rowH = 118;
  return (
    <AbsoluteFill style={{ alignItems: "center", justifyContent: "center" }}>
      <PhotonRain o={0.28} n={14} />
      <div style={{ position: "absolute", left: 0, right: 0, top: 96, textAlign: "center", opacity: usePfull(dur)(0, 0.06) }}>
        <Kicker theme={T} text="YOUR FIRST 90 DAYS" cx />
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 56, color: T.text, marginTop: 10, letterSpacing: -1.5 }}>How to actually start</div>
      </div>
      <div style={{ position: "absolute", left: 480, top: y0 + 30, width: 4, height: steps.length * rowH - 60, background: T.line }} />
      <div style={{ position: "absolute", left: 480, top: y0 + 30, width: 4, height: (steps.length * rowH - 60) * railFill, background: `linear-gradient(180deg, ${A.sun}, ${A.hot})`, boxShadow: `0 0 12px ${A.sun}` }} />
      {steps.map((s, i) => {
        const at = 0.1 + i * 0.12;
        const o = usePfull(dur)(at, at + 0.08);
        const active = hot === i;
        return (
          <div key={i} style={{ position: "absolute", left: 530, top: y0 + i * rowH, width: 940, height: rowH - 20, display: "flex", alignItems: "center", gap: 24, opacity: o, transform: `translateX(${(1 - o) * -30}px)` }}>
            <div style={{ width: 62, height: 62, borderRadius: 16, flexShrink: 0, background: mix(T.panel, s.c, active ? 0.35 : 0.18), border: `2.5px solid ${s.c}`, display: "flex", alignItems: "center", justifyContent: "center", fontFamily: MONO, fontWeight: 800, fontSize: 30, color: s.c, boxShadow: active ? `0 0 22px ${mix(T.bg0, s.c, 0.5)}` : "none" }}>{s.n}</div>
            <div>
              <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 36, color: T.text }}>{s.t}</div>
              <div style={{ fontFamily: MONO, fontSize: 23, color: s.c, marginTop: 4 }}>{s.d}</div>
            </div>
          </div>
        );
      })}
    </AbsoluteFill>
  );
};

// ============================================================================ RISKS
const RisksScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur);
  const risks = [
    { at: 0.1, t: "Price wars", d: "aggressive bidding compresses margins fast", c: A.hot },
    { at: 0.22, t: "Soft-cost leakage", d: "failed visits, redesigns and delays eat profit", c: A.biz },
    { at: 0.34, t: "Quality & warranty", d: "a bad inverter or leak is your liability for years", c: A.cell },
    { at: 0.46, t: "Policy dependence", d: "subsidies and net-metering rules can change", c: A.sun },
  ];
  return (
    <Stage>
      <Head theme={T} kicker="EYES OPEN" title="The risks nobody advertises" color={A.hot} o={p(0, 0.06)} />
      {risks.map((r, i) => {
        const x = 130 + (i % 2) * 880;
        const y = 250 + Math.floor(i / 2) * 270;
        return (
          <Card key={i} theme={T} x={x} y={y} w={810} h={230} color={r.c} o={p(r.at, r.at + 0.1)}>
            <div style={{ display: "flex", alignItems: "center", gap: 16 }}>
              <span style={{ fontSize: 40 }}>⚠️</span>
              <span style={{ fontFamily: SANS, fontWeight: 800, fontSize: 34, color: r.c }}>{r.t}</span>
            </div>
            <div style={{ fontFamily: SANS, fontSize: 26, color: T.text, marginTop: 18, lineHeight: 1.4 }}>{r.d}</div>
          </Card>
        );
      })}
      <Foot theme={T} p={p(0.84, 0.92)}>
        The winners compete on trust and clean execution — not on being the cheapest quote.
      </Foot>
    </Stage>
  );
};

// ============================================================================ RECAP
const RecapScene: React.FC<{ dur?: number; items?: string[]; closer?: string }> = ({
  dur, items = [], closer = "Sunlight is free — the business is turning it into savings people gladly pay for.",
}) => {
  const frame = useCurrentFrame();
  const p = usePfull(dur);
  return (
    <AbsoluteFill style={{ padding: "60px 130px", justifyContent: "center" }}>
      <PhotonRain o={0.3} n={16} />
      <div style={{ opacity: p(0, 0.06), textAlign: "center", marginBottom: 26 }}>
        <Kicker theme={T} text="RECAP — THE WHOLE MAP" cx />
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 60, color: T.text, marginTop: 12, letterSpacing: -1.5 }}>Solar, from panel to profit</div>
      </div>
      <div style={{ display: "flex", flexDirection: "column", gap: 11, maxWidth: 1400, margin: "0 auto", width: "100%" }}>
        {items.map((it, i) => {
          const at = 0.05 + i * 0.085;
          const o = p(at, at + 0.06);
          return (
            <div key={i} style={{ display: "flex", alignItems: "center", gap: 18, opacity: o, transform: `translateX(${(1 - o) * -24}px)`, background: mix(T.panel, A.sun, 0.05), border: `1.5px solid ${T.line}`, borderLeft: `4px solid ${A.sun}`, borderRadius: 12, padding: "13px 26px" }}>
              <span style={{ color: A.sun, fontFamily: MONO, fontWeight: 700, fontSize: 25 }}>{i + 1}</span>
              <span style={{ fontFamily: SANS, fontSize: 28, color: T.text, lineHeight: 1.25 }}>{it}</span>
            </div>
          );
        })}
      </div>
      <div style={{ textAlign: "center", marginTop: 30, opacity: p(0.82, 0.92) }}>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontStyle: "italic", fontSize: 38, color: A.sun, textShadow: `0 0 ${28 + Math.sin(frame * 0.06) * 14}px ${mix(T.bg0, A.sun, 0.7)}` }}>{closer}</div>
      </div>
    </AbsoluteFill>
  );
};

// SceneProgress — thin bar, fills L→R over the full beat; guarantees a "playing" signal.
const SceneProgress: React.FC<{ accent: string; dur?: number }> = ({ accent, dur }) => {
  const p = usePfull(dur);
  const w = p(0, 1);
  return (
    <div style={{ position: "absolute", left: 0, bottom: 0, height: 5, width: `${w * 100}%`,
      background: `linear-gradient(90deg, ${mix(accent, "#07060A", 0.35)}, ${accent})`,
      boxShadow: `0 0 12px ${accent}`, opacity: 0.85 }} />
  );
};

// =====================================================================================
export const SolScene: React.FC<{ variant: string;[key: string]: unknown }> = ({ variant, ...rest }) => {
  let content: React.ReactNode;
  let accent = A.sun;
  switch (variant) {
    case "sol_title": content = <TitleScene {...(rest as any)} />; break;
    case "sol_roadmap": content = <RoadmapScene {...(rest as any)} />; break;
    case "sol_hook": content = <HookScene {...(rest as any)} />; break;
    case "sol_why": content = <WhyScene {...(rest as any)} />; break;
    case "sol_divider": content = <Divider {...(rest as any)} />; accent = (rest as any).color || A.sun; break;
    case "sol_spectrum": content = <SpectrumScene {...(rest as any)} />; break;
    case "sol_cell": content = <CellScene {...(rest as any)} />; accent = A.cell; break;
    case "sol_panel": content = <PanelScene {...(rest as any)} />; accent = A.cell; break;
    case "sol_efficiency": content = <EfficiencyScene {...(rest as any)} />; break;
    case "sol_types": content = <TypesScene {...(rest as any)} />; accent = A.cell; break;
    case "sol_dcac": content = <DcAcScene {...(rest as any)} />; accent = A.grid; break;
    case "sol_ongrid": content = <OnGridScene {...(rest as any)} />; accent = A.grid; break;
    case "sol_offgrid": content = <OffGridScene {...(rest as any)} />; accent = A.cell; break;
    case "sol_components": content = <ComponentsScene {...(rest as any)} />; break;
    case "sol_sizing": content = <SizingScene {...(rest as any)} />; accent = A.grid; break;
    case "sol_rooftop": content = <RooftopScene {...(rest as any)} />; accent = A.cell; break;
    case "sol_install": content = <InstallScene {...(rest as any)} />; break;
    case "sol_savings": content = <SavingsScene {...(rest as any)} />; accent = A.grid; break;
    case "sol_subsidy": content = <SubsidyScene {...(rest as any)} />; break;
    case "sol_cni": content = <CniScene {...(rest as any)} />; accent = A.biz; break;
    case "sol_models": content = <ModelsScene {...(rest as any)} />; accent = A.biz; break;
    case "sol_bizcase": content = <BizCaseScene {...(rest as any)} />; accent = A.biz; break;
    case "sol_valuechain": content = <ValueChainScene {...(rest as any)} />; accent = A.biz; break;
    case "sol_channels": content = <ChannelsScene {...(rest as any)} />; accent = A.biz; break;
    case "sol_margins": content = <MarginsScene {...(rest as any)} />; accent = A.biz; break;
    case "sol_economics": content = <EconomicsScene {...(rest as any)} />; accent = A.grid; break;
    case "sol_getstarted": content = <GetStartedScene {...(rest as any)} />; break;
    case "sol_risks": content = <RisksScene {...(rest as any)} />; accent = A.hot; break;
    case "sol_recap": content = <RecapScene {...(rest as any)} />; break;
    default: content = <TitleScene {...(rest as any)} />;
  }
  return (
    <AbsoluteFill>
      <Bg theme={T} accent={accent} />
      {content}
      <SceneProgress accent={accent} dur={(rest as any).dur} />
    </AbsoluteFill>
  );
};

export default SolScene;
