/**
 * DemoScenes.tsx — the REFERENCE scene set. Copy this file to start a new video.
 *
 * It demonstrates, in ~4 scenes, every pattern the gold-reference videos
 * (FTScenes, CVScenes in reference/) use at scale:
 *
 *   demo_title    — identity, spring pop, animated underline, ambient motion
 *   demo_diagram  — Cards + Wires + Flow particles, phased left→right build
 *   demo_data     — computed visual (live sorting bars), Counter, chase pill
 *   demo_recap    — phased list + glowing closer
 *
 * THE RULES (see skills/03-animation.md — they are not optional):
 *   • every scene receives `dur` (seconds) and phases with p(a, b) FRACTIONS
 *   • something must be moving in every frame (Flow, dash-march, sin breathing)
 *   • randomness only via rnd(i, j, s) — never Math.random()
 *   • no CSS filter/blur; author on the 1920×1080 Stage
 */
import React from "react";
import { AbsoluteFill, interpolate, useCurrentFrame } from "remotion";
import {
  makeTheme, mix, useP, usePop, rnd, MONO, SANS,
  Bg, Stage, VStage, Kicker, Head, Foot, Card, Flow, Wire, Counter,
} from "../lib/primitives";

// 1) Every video defines its own IDENTITY: a theme + 2-4 semantic accent colors.
const T = makeTheme({ accent: "#5EEAD4" });
const A = { main: "#5EEAD4", warm: "#FBBF24", deep: "#A78BFA", ok: "#34D399" };

// demo_title -----------------------------------------------------------------
const TitleScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const pop = usePop(dur);
  return (
    <AbsoluteFill style={{ alignItems: "center", justifyContent: "center" }}>
      {/* ambient: orbiting dots — cheap, runs forever */}
      {Array.from({ length: 10 }).map((_, i) => {
        const ang = frame * 0.012 + (i / 10) * Math.PI * 2;
        return (
          <div key={i} style={{
            position: "absolute", left: 960 + Math.cos(ang) * (560 + i * 14) - 5,
            top: 540 + Math.sin(ang) * (250 + i * 8) - 5,
            width: 10, height: 10, borderRadius: 10, background: A.main,
            opacity: 0.25 + rnd(i, 1) * 0.3, boxShadow: `0 0 12px ${A.main}`,
          }} />
        );
      })}
      <div style={{ textAlign: "center", transform: `scale(${0.92 + pop(0) * 0.08})` }}>
        <div style={{ display: "flex", justifyContent: "center", marginBottom: 26 }}>
          <Kicker theme={T} text="EXPLAINER FORGE · REFERENCE" cx />
        </div>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 120, lineHeight: 1.02, letterSpacing: -3, color: T.text }}>
          <div>Demo</div>
          <div style={{ color: A.main, textShadow: `0 0 70px ${mix(T.bg0, A.main, 0.7)}` }}>Scene Set</div>
        </div>
        {/* underline draw is phased over the narration, not a fixed 12 frames */}
        <div style={{ height: 5, width: interpolate(p(0.18, 0.45), [0, 1], [0, 520]), background: `linear-gradient(90deg, ${A.main}, ${A.deep})`, borderRadius: 3, margin: "32px auto" }} />
        <div style={{ fontFamily: SANS, fontSize: 38, color: T.muted, opacity: p(0.28, 0.5) }}>
          duration-aware phases · continuous motion · computed visuals
        </div>
      </div>
    </AbsoluteFill>
  );
};

// demo_diagram ------------------------------------------------------------------
const DiagramScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur);
  const nodes = [
    { at: 0.08, x: 150, label: "input", sub: "raw data", c: A.main },
    { at: 0.3, x: 760, label: "process", sub: "the interesting part", c: A.deep },
    { at: 0.55, x: 1380, label: "output", sub: "the payoff", c: A.ok },
  ];
  return (
    <Stage>
      <Head theme={T} kicker="PATTERN 1 · DIAGRAM" title="Cards, wires, and particle flows" o={p(0, 0.06)} />
      {nodes.map((n, i) => (
        <React.Fragment key={i}>
          {/* wires draw in just before their target card lands */}
          {i > 0 && (
            <>
              <Wire x1={nodes[i - 1].x + 390} y1={520} x2={n.x - 12} y2={520} p={p(n.at - 0.06, n.at)} color={n.c} w={3.5} />
              <Flow x1={nodes[i - 1].x + 390} y1={520} x2={n.x - 12} y2={520} color={n.c} n={5} o={p(n.at + 0.04, n.at + 0.12)} />
            </>
          )}
          <Card theme={T} x={n.x} y={400} w={390} h={240} color={n.c} o={p(n.at, n.at + 0.09)} glow>
            <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 40, color: n.c }}>{n.label}</div>
            <div style={{ fontFamily: MONO, fontSize: 24, color: T.muted, marginTop: 12 }}>{n.sub}</div>
          </Card>
        </React.Fragment>
      ))}
      <Foot theme={T} p={p(0.8, 0.9)}>
        The build lands at 55% of the narration; the Flow particles keep every later second alive.
      </Foot>
    </Stage>
  );
};

// demo_data — a COMPUTED visual: bubble sort, animated live -----------------------
const N = 12;
const sortSteps = (() => {
  // precompute (deterministic) bubble-sort snapshots at module scope
  const arr = Array.from({ length: N }, (_, i) => Math.round(20 + rnd(i, 5) * 220));
  const steps: number[][] = [arr.slice()];
  const a = arr.slice();
  for (let i = 0; i < N; i++) for (let j = 0; j < N - 1 - i; j++) {
    if (a[j] > a[j + 1]) { [a[j], a[j + 1]] = [a[j + 1], a[j]]; steps.push(a.slice()); }
  }
  return steps;
})();

const DataScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  // the algorithm actually RUNS across the scene — this is "compute the real thing"
  const step = Math.min(sortSteps.length - 1, Math.floor(p(0.15, 0.75) * sortSteps.length));
  const bars = sortSteps[step];
  const done = step === sortSteps.length - 1;
  return (
    <Stage>
      <Head theme={T} kicker="PATTERN 2 · COMPUTED VISUAL" title="Don't illustrate the idea — run it" color={A.warm} o={p(0, 0.06)} />
      {bars.map((v, i) => (
        <div key={i} style={{
          position: "absolute", left: 260 + i * 120, top: 760 - v * 1.7, width: 92, height: v * 1.7,
          borderRadius: "10px 10px 0 0",
          background: `linear-gradient(180deg, ${done ? A.ok : A.warm}, ${mix(done ? A.ok : A.warm, T.bg1, 0.5)})`,
          border: `2px solid ${done ? A.ok : A.warm}`, opacity: p(0.05 + i * 0.01, 0.13 + i * 0.01),
          boxShadow: done ? `0 0 26px ${mix(T.bg0, A.ok, 0.3 + Math.sin(frame * 0.08 + i) * 0.1)}` : "none",
        }}>
          <div style={{ fontFamily: MONO, fontSize: 21, color: T.text, textAlign: "center", marginTop: -34 }}>{v}</div>
        </div>
      ))}
      <div style={{ position: "absolute", left: 260, top: 812, display: "flex", gap: 24, alignItems: "baseline", opacity: p(0.16, 0.24) }}>
        <span style={{ fontFamily: MONO, fontSize: 24, color: T.muted }}>swaps:</span>
        <Counter p={step / (sortSteps.length - 1)} to={sortSteps.length - 1} color={A.warm} size={40} />
        {done && <span style={{ fontFamily: SANS, fontWeight: 800, fontSize: 32, color: A.ok, opacity: p(0.76, 0.84) }}>sorted ✓</span>}
      </div>
      <Foot theme={T} p={p(0.84, 0.93)}>
        The bars are real bubble-sort states computed at module scope — precise, cheap, and impossible to fake wrong.
      </Foot>
    </Stage>
  );
};

// demo_recap -----------------------------------------------------------------------
const RecapScene: React.FC<{ dur?: number; items?: string[]; closer?: string }> = ({
  dur, items = [], closer = "Phased to the narration, moving in every frame.",
}) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  return (
    <AbsoluteFill style={{ padding: "70px 130px", justifyContent: "center" }}>
      <div style={{ opacity: p(0, 0.06), textAlign: "center", marginBottom: 30 }}>
        <Kicker theme={T} text="PATTERN 3 · RECAP" cx />
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 62, color: T.text, marginTop: 12, letterSpacing: -1.5 }}>The whole set in one breath</div>
      </div>
      <div style={{ display: "flex", flexDirection: "column", gap: 13, maxWidth: 1340, margin: "0 auto", width: "100%" }}>
        {items.map((it, i) => {
          const at = 0.06 + i * 0.1;
          const o = p(at, at + 0.07);
          return (
            <div key={i} style={{ display: "flex", alignItems: "center", gap: 18, opacity: o, transform: `translateX(${(1 - o) * -26}px)`, background: mix(T.panel, A.main, 0.05), border: `1.5px solid ${T.line}`, borderLeft: `4px solid ${A.main}`, borderRadius: 12, padding: "15px 26px" }}>
              <span style={{ color: A.main, fontFamily: MONO, fontWeight: 700, fontSize: 26 }}>{i + 1}</span>
              <span style={{ fontFamily: SANS, fontSize: 30, color: T.text, lineHeight: 1.25 }}>{it}</span>
            </div>
          );
        })}
      </div>
      <div style={{ textAlign: "center", marginTop: 34, opacity: p(0.8, 0.9) }}>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontStyle: "italic", fontSize: 42, color: A.main, textShadow: `0 0 ${30 + Math.sin(frame * 0.06) * 14}px ${mix(T.bg0, A.main, 0.7)}` }}>{closer}</div>
      </div>
    </AbsoluteFill>
  );
};

// demo_vhook — VERTICAL (9:16) reference scene. Render via ExplainerVertical.
// Shows the vertical grammar from skills/10-vertical.md: UI-safe zones kept empty
// (top 170 / bottom 1560+ / right rail), stacked layout, hero at vertical center,
// bigger type. Author on VStage (1080×1920).
const VHookScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  return (
    <VStage>
      {/* HEADER zone (y 170–340): the hook IS the title */}
      <div style={{ position: "absolute", left: 70, right: 70, top: 190, textAlign: "center" }}>
        <div style={{ display: "flex", justifyContent: "center", opacity: p(0, 0.08) }}>
          <Kicker theme={T} text="IN 60 SECONDS" cx />
        </div>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 96, lineHeight: 1.04, letterSpacing: -2, color: T.text, marginTop: 18, opacity: p(0.02, 0.1) }}>
          The Forge,<br /><span style={{ color: A.main, textShadow: `0 0 60px ${mix(T.bg0, A.main, 0.7)}` }}>vertical</span>
        </div>
      </div>
      {/* HERO at the content-zone center (~y 700–1250): a computed visual */}
      <div style={{ position: "absolute", left: 70, top: 700, width: 940, height: 560, borderRadius: 26, background: mix(T.panel, A.main, 0.06), border: `2.5px solid ${mix(T.line, A.main, 0.5)}`, opacity: p(0.1, 0.2) }}>
        {sortSteps[Math.min(sortSteps.length - 1, Math.floor(p(0.18, 0.75) * sortSteps.length))].map((v, i) => (
          <div key={i} style={{
            position: "absolute", left: 50 + i * 72, bottom: 60, width: 52, height: v * 1.6,
            borderRadius: "8px 8px 0 0", background: `linear-gradient(180deg, ${A.warm}, ${mix(A.warm, T.bg1, 0.5)})`,
            border: `2px solid ${A.warm}`, opacity: p(0.14 + i * 0.01, 0.22 + i * 0.01),
          }} />
        ))}
        <div style={{ position: "absolute", left: 50, top: 34, fontFamily: MONO, fontSize: 28, color: T.muted }}>same engine · stacked layout</div>
      </div>
      <Flow x1={540} y1={620} x2={540} y2={700} color={A.main} n={4} o={p(0.12, 0.2)} />
      {/* one support block below the hero — takeaway chip */}
      <div style={{ position: "absolute", left: 70, right: 70, top: 1330, textAlign: "center", opacity: p(0.6, 0.72) }}>
        <span style={{ fontFamily: SANS, fontWeight: 800, fontSize: 40, color: A.ok, background: mix(T.panel, A.ok, 0.1), border: `2.5px solid ${A.ok}`, borderRadius: 18, padding: "16px 34px", boxShadow: `0 0 ${34 + Math.sin(frame * 0.07) * 12}px ${mix(T.bg0, A.ok, 0.4)}` }}>
          hook → 3 beats → takeaway
        </span>
      </div>
      {/* top 0–170 and bottom 1560–1920 intentionally EMPTY (platform UI zones) */}
    </VStage>
  );
};

// ===========================================================================
export const DemoScene: React.FC<{ variant: string;[key: string]: unknown }> = ({ variant, ...rest }) => {
  let content: React.ReactNode;
  let accent = A.main;
  switch (variant) {
    case "demo_title": content = <TitleScene {...(rest as any)} />; break;
    case "demo_diagram": content = <DiagramScene {...(rest as any)} />; accent = A.deep; break;
    case "demo_data": content = <DataScene {...(rest as any)} />; accent = A.warm; break;
    case "demo_vhook": content = <VHookScene {...(rest as any)} />; break;
    case "demo_recap": content = <RecapScene {...(rest as any)} />; break;
    default: content = <TitleScene {...(rest as any)} />;
  }
  return (
    <AbsoluteFill>
      <Bg theme={T} accent={accent} />
      {content}
    </AbsoluteFill>
  );
};

export default DemoScene;
