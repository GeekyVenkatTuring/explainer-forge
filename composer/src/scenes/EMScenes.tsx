/**
 * EMScenes.tsx — "The Engineering Manager Behavioral Interview".
 *
 * How to answer the behavioral questions asked of Manager / Senior EM candidates.
 *
 * IDENTITY
 *   theme accent = amber (leadership / gold)
 *   semantic colors:
 *     SIT  blue   #38BDF8 — situation & context (the setup)
 *     YOU  amber  #F5A524 — YOU: your action, decisions, judgment (the hero color)
 *     RES  green  #34D399 — result / positive signal / strong answer
 *     META violet #A78BFA — the framework, prep, meta
 *     FLAG pink   #FB7185 — traps, red flags, what weak answers do
 *   recurring motif: the STAR-L ribbon (S · T · A · R · L) threads every "how to
 *     answer" scene, and an interviewer "scorecard" of signal bars.
 *
 * Rules (skills/03): every scene takes `dur` and phases with useP(dur); at least
 * one always-on element per frame; determinism via rnd; author on the Stage.
 */
import React from "react";
import { AbsoluteFill, interpolate, useCurrentFrame } from "remotion";
import {
  makeTheme, mix, useP, usePop, rnd, MONO, SANS,
  Bg, Stage, Kicker, Head, Foot, Card, Flow, Wire, Counter, Type, ScanBeam, Brackets,
} from "../lib/primitives";

const T = makeTheme({ accent: "#F5A524" });
const A = {
  sit: "#38BDF8",   // situation / context
  you: "#F5A524",   // YOU — action, judgment
  res: "#34D399",   // result / strong signal
  meta: "#A78BFA",  // framework / prep
  flag: "#FB7185",  // trap / red flag
};

// STAR-L node → color + label (the recurring motif)
const STAR: Record<string, { c: string; label: string }> = {
  S: { c: A.sit, label: "SITUATION" },
  T: { c: A.sit, label: "TASK" },
  A: { c: A.you, label: "ACTION" },
  R: { c: A.res, label: "RESULT" },
  L: { c: A.meta, label: "LEARNING" },
};

// A small STAR-L ribbon used as a recurring header motif on question scenes.
const Ribbon: React.FC<{ p: (a: number, b: number) => number; y?: number; hot?: number }> = ({ p, y = 196, hot }) => {
  const frame = useCurrentFrame();
  const keys = ["S", "T", "A", "R", "L"];
  const x0 = 880, gap = 190;
  return (
    <>
      {keys.map((k, i) => {
        const x = x0 + i * gap;
        const on = hot === i;
        const sc = STAR[k].c;
        return (
          <React.Fragment key={k}>
            {i > 0 && (
              <Wire x1={x0 + (i - 1) * gap + 26} y1={y + 26} x2={x - 26} y2={y + 26}
                p={p(0.02 + i * 0.01, 0.06 + i * 0.01)} color={mix(T.line, sc, 0.6)} w={2.5} arrow={false} />
            )}
            <div style={{
              position: "absolute", left: x - 26, top: y, width: 52, height: 52, borderRadius: 14,
              background: mix(T.panel, sc, on ? 0.35 : 0.14), border: `2.5px solid ${sc}`,
              display: "flex", alignItems: "center", justifyContent: "center",
              fontFamily: MONO, fontWeight: 800, fontSize: 26, color: on ? T.bg0 : sc,
              boxShadow: on ? `0 0 20px ${mix(T.bg0, sc, 0.5)}` : "none",
              transform: `translateY(${on ? -4 : 0}px)`, opacity: p(0.02, 0.1),
            }}>{k}</div>
          </React.Fragment>
        );
      })}
      <div style={{ position: "absolute", left: x0 - 26, top: y + 62, fontFamily: MONO, fontSize: 18, letterSpacing: 4, color: T.muted, opacity: p(0.08, 0.16) }}>
        STAR&nbsp;·&nbsp;+&nbsp;LEARNING&nbsp;→&nbsp;THE ANSWER SPINE
      </div>
    </>
  );
};

// em_title -------------------------------------------------------------------
const TitleScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const pop = usePop(dur);
  // ambient motif: a scorecard of signal bars quietly filling on the right edge
  return (
    <AbsoluteFill style={{ alignItems: "center", justifyContent: "center" }}>
      {/* orbiting judgment dots */}
      {Array.from({ length: 12 }).map((_, i) => {
        const ang = frame * 0.01 + (i / 12) * Math.PI * 2;
        const c = [A.you, A.sit, A.res, A.meta][i % 4];
        return (
          <div key={i} style={{
            position: "absolute", left: 960 + Math.cos(ang) * (620 + i * 10) - 5,
            top: 540 + Math.sin(ang) * (270 + i * 6) - 5, width: 9, height: 9, borderRadius: 9,
            background: c, opacity: 0.22 + rnd(i, 2) * 0.28, boxShadow: `0 0 12px ${c}`,
          }} />
        );
      })}
      <div style={{ textAlign: "center", transform: `scale(${0.93 + pop(0) * 0.07})` }}>
        <div style={{ display: "flex", justifyContent: "center", marginBottom: 26 }}>
          <Kicker theme={T} text="ENGINEERING LEADERSHIP · INTERVIEW PREP" cx />
        </div>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 104, lineHeight: 1.04, letterSpacing: -3, color: T.text }}>
          <div>The Engineering Manager</div>
          <div style={{ color: A.you, textShadow: `0 0 70px ${mix(T.bg0, A.you, 0.7)}` }}>Behavioral Interview</div>
        </div>
        <div style={{ height: 5, width: interpolate(p(0.18, 0.45), [0, 1], [0, 620]), background: `linear-gradient(90deg, ${A.you}, ${A.meta})`, borderRadius: 3, margin: "34px auto" }} />
        <div style={{ fontFamily: SANS, fontSize: 36, color: T.muted, opacity: p(0.28, 0.5) }}>
          the questions they ask · and how to actually answer them · Manager → Senior EM
        </div>
      </div>
    </AbsoluteFill>
  );
};

// em_titlex — parameterized title (for follow-up videos / parts) ------------
const TitleXScene: React.FC<{ dur?: number; kicker?: string; line1?: string; line2?: string; sub?: string }> = ({
  dur, kicker = "", line1 = "", line2 = "", sub = "",
}) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const pop = usePop(dur);
  return (
    <AbsoluteFill style={{ alignItems: "center", justifyContent: "center" }}>
      {Array.from({ length: 12 }).map((_, i) => {
        const ang = frame * 0.01 + (i / 12) * Math.PI * 2;
        const c = [A.you, A.sit, A.res, A.meta][i % 4];
        return (
          <div key={i} style={{
            position: "absolute", left: 960 + Math.cos(ang) * (620 + i * 10) - 5,
            top: 540 + Math.sin(ang) * (270 + i * 6) - 5, width: 9, height: 9, borderRadius: 9,
            background: c, opacity: 0.22 + rnd(i, 2) * 0.28, boxShadow: `0 0 12px ${c}`,
          }} />
        );
      })}
      <div style={{ textAlign: "center", transform: `scale(${0.93 + pop(0) * 0.07})` }}>
        <div style={{ display: "flex", justifyContent: "center", marginBottom: 26 }}>
          <Kicker theme={T} text={kicker} cx />
        </div>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 108, lineHeight: 1.04, letterSpacing: -3, color: T.text }}>
          <div>{line1}</div>
          <div style={{ color: A.you, textShadow: `0 0 70px ${mix(T.bg0, A.you, 0.7)}` }}>{line2}</div>
        </div>
        <div style={{ height: 5, width: interpolate(p(0.18, 0.45), [0, 1], [0, 620]), background: `linear-gradient(90deg, ${A.you}, ${A.meta})`, borderRadius: 3, margin: "34px auto" }} />
        <div style={{ fontFamily: SANS, fontSize: 36, color: T.muted, opacity: p(0.28, 0.5) }}>{sub}</div>
      </div>
    </AbsoluteFill>
  );
};

// em_hook --------------------------------------------------------------------
const HookScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  return (
    <Stage>
      <div style={{ position: "absolute", left: 100, top: 150, right: 100, textAlign: "center", opacity: p(0, 0.06) }}>
        <Kicker theme={T} text="WHY THIS ROUND IS DIFFERENT" cx />
      </div>
      {/* the shift: coding proven → now they test judgment */}
      <div style={{ position: "absolute", left: 130, top: 340, width: 720, textAlign: "center", opacity: p(0.08, 0.18) }}>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 46, color: T.muted, letterSpacing: -1 }}>They already believe</div>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 60, color: A.sit, letterSpacing: -1.5, marginTop: 10, textDecoration: "line-through", textDecorationColor: mix(A.sit, T.bg0, 0.3) }}>you can build it.</div>
      </div>
      <Wire x1={860} y1={430} x2={1060} y2={430} p={p(0.24, 0.34)} color={A.you} w={4} />
      <Flow x1={860} y1={430} x2={1060} y2={430} color={A.you} n={5} o={p(0.3, 0.4)} />
      <div style={{ position: "absolute", left: 1070, top: 330, width: 720, textAlign: "center", opacity: p(0.34, 0.46) }}>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 46, color: T.muted, letterSpacing: -1 }}>Now they're testing</div>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 60, color: A.you, letterSpacing: -1.5, marginTop: 10, textShadow: `0 0 40px ${mix(T.bg0, A.you, 0.5)}` }}>would we hand<br />you a team?</div>
      </div>
      <div style={{
        position: "absolute", left: 360, top: 720, width: 1200, textAlign: "center", opacity: p(0.6, 0.72),
        fontFamily: SANS, fontSize: 34, color: T.text, lineHeight: 1.4,
      }}>
        Every "tell me about a time…" is really one question:{" "}
        <span style={{ color: A.res, fontWeight: 800, textShadow: `0 0 ${20 + Math.sin(frame * 0.07) * 8}px ${mix(T.bg0, A.res, 0.5)}` }}>how do you lead when it's hard?</span>
      </div>
      <Foot theme={T} p={p(0.82, 0.92)}>The stories are the evidence. The structure is the skill. This video gives you both.</Foot>
    </Stage>
  );
};

// em_compass — what they're really testing (orbit hub) -----------------------
const CompassScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const items = [
    { emoji: "👥", label: "People", sub: "grow, coach, retain", c: A.you },
    { emoji: "�caret", label: "Delivery", sub: "ship under pressure", c: A.res },
    { emoji: "⚖️", label: "Judgment", sub: "trade-offs & conflict", c: A.sit },
    { emoji: "🪞", label: "Self-awareness", sub: "own failure, learn", c: A.meta },
  ].map((it) => ({ ...it, emoji: it.emoji === "�caret" ? "🚀" : it.emoji }));
  return (
    <Stage>
      <Head theme={T} kicker="THE FOUR COMPETENCIES" title="What behavioral questions actually measure" o={p(0, 0.06)} />
      {/* center hub */}
      <div style={{
        position: "absolute", left: 960 - 130, top: 560 - 90, width: 260, height: 180, borderRadius: 22,
        background: mix(T.panel, A.you, 0.14), border: `3px solid ${A.you}`, display: "flex", flexDirection: "column",
        alignItems: "center", justifyContent: "center", opacity: p(0.06, 0.16),
        boxShadow: `0 0 ${50 + Math.sin(frame * 0.05) * 16}px ${mix(T.bg0, A.you, 0.3)}`,
      }}>
        <div style={{ fontFamily: MONO, fontSize: 20, letterSpacing: 3, color: A.you }}>THE REAL RUBRIC</div>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 34, color: T.text, marginTop: 8, textAlign: "center", lineHeight: 1.15 }}>Can you<br />lead a team?</div>
      </div>
      {items.map((it, i) => {
        const ang = (i / items.length) * Math.PI * 2 - Math.PI / 2 + Math.sin(frame * 0.008) * 0.05;
        const x = 960 + Math.cos(ang) * 620, y = 560 + Math.sin(ang) * 300;
        const at = 0.14 + i * 0.12;
        const active = Math.floor(frame / 30) % items.length === i;
        return (
          <React.Fragment key={i}>
            <Wire x1={960} y1={560} x2={x} y2={y} p={p(at - 0.06, at)} color={active ? it.c : mix(T.muted, T.bg1, 0.4)} w={active ? 3.5 : 2} arrow={false} />
            <Flow x1={960} y1={560} x2={x} y2={y} color={it.c} n={4} o={active ? p(at, at + 0.06) : 0} />
            <div style={{
              position: "absolute", left: x - 175, top: y - 60, width: 350, height: 120, borderRadius: 18,
              background: mix(T.panel, it.c, active ? 0.2 : 0.08), border: `2.5px solid ${active ? it.c : mix(T.line, it.c, 0.5)}`,
              display: "flex", alignItems: "center", gap: 16, padding: "0 22px", boxSizing: "border-box",
              opacity: p(at, at + 0.08), transform: `scale(${active ? 1.05 : 1})`,
            }}>
              <span style={{ fontSize: 46 }}>{it.emoji}</span>
              <div>
                <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 30, color: T.text }}>{it.label}</div>
                <div style={{ fontFamily: MONO, fontSize: 20, color: it.c, marginTop: 4 }}>{it.sub}</div>
              </div>
            </div>
          </React.Fragment>
        );
      })}
      <Foot theme={T} p={p(0.82, 0.92)}>Every question maps to one of these four. Know which one you're being asked.</Foot>
    </Stage>
  );
};

// em_star — the STAR-L framework (pipeline) ----------------------------------
const StarScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const nodes = [
    { k: "S", desc: "one line of setup", w: 240 },
    { k: "T", desc: "your responsibility", w: 240 },
    { k: "A", desc: "what YOU did — the core", w: 420 },
    { k: "R", desc: "the measurable outcome", w: 260 },
    { k: "L", desc: "what you'd do again", w: 260 },
  ];
  let x = 120;
  const laid = nodes.map((n) => { const o = { ...n, x }; x += n.w + 34; return o; });
  return (
    <Stage>
      <Head theme={T} kicker="THE ANSWER SPINE" title="STAR — plus the letter managers forget" o={p(0, 0.06)} />
      {laid.map((n, i) => {
        const at = 0.08 + i * 0.12;
        const c = STAR[n.k].c;
        const big = n.k === "A";
        return (
          <React.Fragment key={i}>
            {i > 0 && (
              <>
                <Wire x1={laid[i - 1].x + laid[i - 1].w} y1={470} x2={n.x} y2={470} p={p(at - 0.06, at)} color={c} w={3.5} />
                <Flow x1={laid[i - 1].x + laid[i - 1].w} y1={470} x2={n.x} y2={470} color={c} n={4} o={p(at, at + 0.08)} />
              </>
            )}
            <div style={{
              position: "absolute", left: n.x, top: big ? 370 : 400, width: n.w, height: big ? 200 : 140, borderRadius: 18,
              background: mix(T.panel, c, big ? 0.18 : 0.1), border: `${big ? 3 : 2.5}px solid ${c}`,
              padding: "18px 22px", boxSizing: "border-box", opacity: p(at, at + 0.08),
              transform: `translateY(${(1 - p(at, at + 0.08)) * 20}px)`,
              boxShadow: big ? `0 0 ${44 + Math.sin(frame * 0.06) * 14}px ${mix(T.bg0, c, 0.32)}` : "none",
            }}>
              <div style={{ fontFamily: MONO, fontWeight: 800, fontSize: big ? 30 : 24, letterSpacing: 2, color: c }}>{STAR[n.k].label}</div>
              <div style={{ fontFamily: SANS, fontWeight: 700, fontSize: big ? 30 : 24, color: T.text, marginTop: 12, lineHeight: 1.25 }}>{n.desc}</div>
              {big && <div style={{ fontFamily: MONO, fontSize: 20, color: A.you, marginTop: 14, opacity: p(0.5, 0.6) }}>spend most of your airtime here →</div>}
            </div>
          </React.Fragment>
        );
      })}
      <div style={{ position: "absolute", left: 120, top: 660, width: 1680, textAlign: "center", opacity: p(0.7, 0.82) }}>
        <span style={{ fontFamily: SANS, fontSize: 32, color: T.text }}>
          At the management bar, <span style={{ color: A.meta, fontWeight: 800 }}>Learning</span> is what separates a doer from a leader — it proves you grew.
        </span>
      </div>
      <Foot theme={T} p={p(0.84, 0.93)}>Situation and Task are the trailer. Action is the movie. Result and Learning are why it mattered.</Foot>
    </Stage>
  );
};

// em_iwe — the two traps: "we" vs "I", and the 90/20 ratio -------------------
const IWeScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  // ratio bars: weak = 90% context / 10% action ; strong = flipped
  const seg = (label: string, pct: number, c: string) => ({ label, pct, c });
  const weak = [seg("context", 0.72, A.sit), seg("action", 0.14, A.you), seg("result", 0.14, A.res)];
  const strong = [seg("context", 0.22, A.sit), seg("action", 0.56, A.you), seg("result", 0.22, A.res)];
  const barW = 760, x0 = 100, x1 = 1060;
  const drawBars = (segs: ReturnType<typeof seg>[], bx: number, at: number, grown: number) => {
    let acc = 0;
    return segs.map((s, i) => {
      const w = s.pct * barW * grown;
      const left = bx + acc; acc += s.pct * barW * grown;
      return (
        <div key={i} style={{
          position: "absolute", left, top: 0, width: w, height: 64,
          background: mix(T.panel, s.c, 0.5), borderRight: `2px solid ${T.bg0}`,
          display: "flex", alignItems: "center", justifyContent: "center", overflow: "hidden",
        }}>
          <span style={{ fontFamily: MONO, fontSize: 19, color: T.bg0, fontWeight: 700, whiteSpace: "nowrap", opacity: w > 90 ? 1 : 0 }}>{s.label}</span>
        </div>
      );
    });
  };
  const gW = p(0.18, 0.32), gS = p(0.5, 0.66);
  return (
    <Stage>
      <Head theme={T} kicker="THE TWO TRAPS EVERYONE FALLS INTO" title={"Say “I” — and flip the ratio"} color={A.flag} o={p(0, 0.06)} />
      {/* TRAP 1 — we vs I */}
      <div style={{ position: "absolute", left: x0, top: 210, fontFamily: MONO, fontSize: 22, letterSpacing: 3, color: A.flag, opacity: p(0.06, 0.14) }}>TRAP 1 · WHO DID IT?</div>
      <Card theme={T} x={x0} y={250} w={760} h={130} color={A.flag} o={p(0.1, 0.2)}>
        <div style={{ fontFamily: MONO, fontSize: 20, color: A.flag }}>weak</div>
        <div style={{ fontFamily: SANS, fontWeight: 700, fontSize: 30, color: T.text, marginTop: 8 }}>"<span style={{ color: A.flag }}>We</span> aligned the team and <span style={{ color: A.flag }}>we</span> shipped it."</div>
      </Card>
      <Card theme={T} x={x1} y={250} w={760} h={130} color={A.res} o={p(0.24, 0.34)} glow>
        <div style={{ fontFamily: MONO, fontSize: 20, color: A.res }}>strong</div>
        <div style={{ fontFamily: SANS, fontWeight: 700, fontSize: 28, color: T.text, marginTop: 8 }}>"<span style={{ color: A.res }}>I</span> reframed the goal, <span style={{ color: A.res }}>I</span> coached Priya — then <span style={{ color: T.muted }}>we</span> shipped."</div>
      </Card>
      {/* TRAP 2 — the airtime ratio */}
      <div style={{ position: "absolute", left: x0, top: 470, fontFamily: MONO, fontSize: 22, letterSpacing: 3, color: A.flag, opacity: p(0.4, 0.48) }}>TRAP 2 · WHERE DOES YOUR TIME GO?</div>
      <div style={{ position: "absolute", left: x0, top: 520, fontFamily: SANS, fontWeight: 700, fontSize: 26, color: A.flag, opacity: p(0.42, 0.5) }}>most candidates</div>
      <div style={{ position: "absolute", left: x0, top: 560, width: barW, height: 64, borderRadius: 10, overflow: "hidden", border: `2px solid ${T.line}`, opacity: p(0.42, 0.5) }}>{drawBars(weak, 0, 0, gW)}</div>
      <div style={{ position: "absolute", left: x1, top: 520, fontFamily: SANS, fontWeight: 700, fontSize: 26, color: A.res, opacity: p(0.62, 0.7) }}>what to do instead</div>
      <div style={{ position: "absolute", left: x1, top: 560, width: barW, height: 64, borderRadius: 10, overflow: "hidden", border: `2px solid ${mix(T.line, A.res, 0.5)}`, opacity: p(0.62, 0.7) }}>{drawBars(strong, 0, 0, gS)}</div>
      <div style={{ position: "absolute", left: x0, top: 660, width: 1660, textAlign: "center", opacity: p(0.78, 0.88) }}>
        <span style={{ fontFamily: SANS, fontSize: 30, color: T.text }}>
          Ninety seconds of backstory buries your decision. Give context in <span style={{ color: A.res, fontWeight: 800 }}>two sentences</span>, then live in the Action.
        </span>
      </div>
      <Foot theme={T} p={p(0.86, 0.94)}>Own it with "I", spend it on the Action. These two fixes lift almost every answer.</Foot>
    </Stage>
  );
};

// em_divider (parameterized) -------------------------------------------------
const DividerScene: React.FC<{ dur?: number; n?: number; title?: string; sub?: string; color?: string }> = ({
  dur, n = 1, title = "", sub = "", color = A.you,
}) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  return (
    <Stage>
      <Brackets x={360} y={310} w={1200} h={460} color={color} o={p(0.02, 0.14)} len={54} />
      <ScanBeam theme={T} x={370} y={320} w={1180} h={440} color={color} o={p(0.05, 0.2)} speed={1.6} />
      <div style={{ position: "absolute", left: 0, right: 0, top: 380, textAlign: "center" }}>
        <div style={{ fontFamily: MONO, fontWeight: 800, fontSize: 32, color, letterSpacing: 10, opacity: p(0.05, 0.15) }}>PART {"0" + n}</div>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 92, color: T.text, letterSpacing: -2, marginTop: 18, opacity: p(0.12, 0.24), transform: `translateY(${(1 - p(0.12, 0.24)) * 28}px)` }}>{title}</div>
        <div style={{ height: 5, width: interpolate(p(0.2, 0.5), [0, 1], [0, 440]), background: color, borderRadius: 3, margin: "24px auto" }} />
        <div style={{ fontFamily: SANS, fontSize: 33, color: T.muted, opacity: p(0.3, 0.45) }}>{sub}</div>
      </div>
      <div style={{ position: "absolute", left: 0, right: 0, top: 850, display: "flex", justifyContent: "center", gap: 16, opacity: p(0.3, 0.45) }}>
        {[1, 2, 3, 4].map((i) => (
          <div key={i} style={{
            width: i === n ? 46 : 14, height: 14, borderRadius: 8,
            background: i <= n ? color : mix(T.panel, color, 0.15), border: `1.5px solid ${i <= n ? color : T.line}`,
            opacity: i === n ? 0.7 + Math.sin(frame * 0.1) * 0.3 : 1,
          }} />
        ))}
      </div>
    </Stage>
  );
};

// em_q — the WORKHORSE "how to answer this question" scene -------------------
type Move = { node: string; title: string; desc: string };
const QScene: React.FC<{
  dur?: number; cat?: string; title?: string; q?: string; color?: string;
  moves?: Move[]; trap?: string; signal?: string; foot?: string;
}> = ({ dur, cat = "", title = "", q = "", color = A.you, moves = [], trap = "", signal = "", foot = "" }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const hot = Math.floor(frame / 34) % Math.max(1, moves.length);
  const ribbonHot = Math.floor(frame / 40) % 5;
  const cardH = moves.length >= 4 ? 122 : 150;
  const cardGap = 18;
  const yTop = 250;
  return (
    <Stage>
      <Head theme={T} kicker={cat} title={title} color={color} o={p(0, 0.06)} />
      <Ribbon p={p} hot={ribbonHot} />
      {/* LEFT — the question the interviewer asks */}
      <Brackets x={100} y={250} w={700} h={300} color={A.sit} o={p(0.06, 0.16)} len={30} />
      <ScanBeam theme={T} x={104} y={254} w={692} h={292} color={A.sit} o={p(0.1, 0.2)} speed={0.7} />
      <div style={{
        position: "absolute", left: 100, top: 250, width: 700, height: 300, borderRadius: 20,
        background: mix(T.panel, A.sit, 0.08), border: `2.5px solid ${mix(T.line, A.sit, 0.6)}`,
        padding: "26px 30px", boxSizing: "border-box", opacity: p(0.05, 0.14),
      }}>
        <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
          <span style={{ fontSize: 28 }}>🎙️</span>
          <span style={{ fontFamily: MONO, fontSize: 20, letterSpacing: 3, color: A.sit }}>THE INTERVIEWER ASKS</span>
        </div>
        <div style={{ fontFamily: SANS, fontWeight: 700, fontSize: 33, color: T.text, marginTop: 20, lineHeight: 1.34 }}>
          <Type text={q} p={p(0.08, 0.34)} color={T.text} size={33} />
        </div>
      </div>
      {/* trap strip */}
      <div style={{
        position: "absolute", left: 100, top: 578, width: 700, minHeight: 92, borderRadius: 16,
        background: mix(T.panel, A.flag, 0.08), border: `2px solid ${mix(T.line, A.flag, 0.55)}`,
        padding: "16px 22px", boxSizing: "border-box", opacity: p(0.5, 0.6),
      }}>
        <div style={{ fontFamily: MONO, fontSize: 19, letterSpacing: 2, color: A.flag }}>✗ WEAK ANSWER</div>
        <div style={{ fontFamily: SANS, fontSize: 25, color: mix(T.text, A.flag, 0.25), marginTop: 8, lineHeight: 1.32 }}>{trap}</div>
      </div>
      {/* signal chip */}
      <div style={{
        position: "absolute", left: 100, top: 700, width: 700, minHeight: 92, borderRadius: 16,
        background: mix(T.panel, A.res, 0.1), border: `2.5px solid ${A.res}`,
        padding: "16px 22px", boxSizing: "border-box", opacity: p(0.64, 0.74),
        boxShadow: `0 0 ${26 + Math.sin(frame * 0.06) * 10}px ${mix(T.bg0, A.res, 0.25)}`,
      }}>
        <div style={{ fontFamily: MONO, fontSize: 19, letterSpacing: 2, color: A.res }}>✓ WHAT A STRONG ANSWER PROVES</div>
        <div style={{ fontFamily: SANS, fontWeight: 600, fontSize: 25, color: T.text, marginTop: 8, lineHeight: 1.32 }}>{signal}</div>
      </div>
      {/* RIGHT — the key moves */}
      <div style={{ position: "absolute", left: 880, top: 300, fontFamily: MONO, fontSize: 21, letterSpacing: 3, color: color, opacity: p(0.2, 0.3) }}>HOW TO ANSWER →</div>
      {moves.map((m, i) => {
        const at = 0.3 + i * 0.11;
        const y = yTop + 90 + i * (cardH + cardGap);
        const nc = STAR[m.node]?.c || color;
        const on = hot === i;
        const o = p(at, at + 0.08);
        return (
          <div key={i} style={{
            position: "absolute", left: 880, top: y, width: 940, height: cardH, borderRadius: 16,
            background: mix(T.panel, nc, on ? 0.16 : 0.07), border: `2px solid ${on ? nc : mix(T.line, nc, 0.45)}`,
            borderLeft: `6px solid ${nc}`, padding: "14px 24px", boxSizing: "border-box",
            display: "flex", flexDirection: "column", justifyContent: "center",
            opacity: o, transform: `translateX(${(1 - o) * 30}px) scale(${on ? 1.015 : 1})`,
          }}>
            <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
              <span style={{ fontFamily: MONO, fontWeight: 800, fontSize: 18, color: on ? T.bg0 : nc, background: on ? nc : mix(T.panel, nc, 0.2), border: `1.5px solid ${nc}`, borderRadius: 7, padding: "2px 8px" }}>{m.node}</span>
              <span style={{ fontFamily: SANS, fontWeight: 800, fontSize: 28, color: T.text }}>{m.title}</span>
            </div>
            <div style={{ fontFamily: SANS, fontSize: 23, color: T.muted, marginTop: 7, lineHeight: 1.28 }}>{m.desc}</div>
          </div>
        );
      })}
      <Foot theme={T} p={p(0.84, 0.93)}>{foot}</Foot>
    </Stage>
  );
};

// em_story — a full worked STAR-L example answer (~2-3 min) -----------------
type Act = { d: string };
type Met = { v: string; l: string };
const StoryScene: React.FC<{
  dur?: number; cat?: string; title?: string; color?: string;
  situation?: string; task?: string; actions?: Act[]; metrics?: Met[];
  learning?: string; foot?: string;
}> = ({ dur, cat = "", title = "", color = A.you, situation = "", task = "",
  actions = [], metrics = [], learning = "", foot = "" }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const actLanded = p(0.57, 0.63) > 0.5;
  const hot = Math.floor(frame / 34) % Math.max(1, actions.length);
  const rowH = actions.length >= 4 ? 58 : 70;
  return (
    <Stage>
      <Head theme={T} kicker={cat} title={title} color={color} o={p(0, 0.05)} />
      {/* SITUATION */}
      <div style={{
        position: "absolute", left: 100, top: 200, width: 860, height: 158, borderRadius: 16,
        background: mix(T.panel, A.sit, 0.08), border: `2px solid ${mix(T.line, A.sit, 0.55)}`,
        padding: "16px 24px", boxSizing: "border-box", opacity: p(0.03, 0.12),
      }}>
        <div style={{ fontFamily: MONO, fontSize: 19, letterSpacing: 3, color: A.sit }}>① SITUATION</div>
        <div style={{ fontFamily: SANS, fontSize: 25, color: T.text, marginTop: 10, lineHeight: 1.32 }}>{situation}</div>
      </div>
      {/* TASK */}
      <div style={{
        position: "absolute", left: 980, top: 200, width: 840, height: 158, borderRadius: 16,
        background: mix(T.panel, A.sit, 0.05), border: `2px solid ${mix(T.line, A.sit, 0.4)}`,
        padding: "16px 24px", boxSizing: "border-box", opacity: p(0.13, 0.22),
      }}>
        <div style={{ fontFamily: MONO, fontSize: 19, letterSpacing: 3, color: mix(A.sit, T.text, 0.3) }}>② MY MANDATE</div>
        <div style={{ fontFamily: SANS, fontSize: 25, color: T.text, marginTop: 10, lineHeight: 1.32 }}>{task}</div>
      </div>
      <Flow x1={530} y1={362} x2={530} y2={392} color={A.you} n={4} o={p(0.24, 0.32)} />
      {/* ACTION — the hero panel */}
      <Brackets x={96} y={386} w={1728} h={318} color={A.you} o={p(0.24, 0.32)} len={30} />
      <ScanBeam theme={T} x={102} y={392} w={1716} h={306} color={A.you} o={p(0.26, 0.34)} speed={0.8} />
      <div style={{
        position: "absolute", left: 100, top: 390, width: 1720, height: 310, borderRadius: 18,
        background: mix(T.panel, A.you, 0.09), border: `2.5px solid ${A.you}`, padding: "16px 28px",
        boxSizing: "border-box", opacity: p(0.22, 0.30),
        boxShadow: `0 0 ${40 + Math.sin(frame * 0.05) * 12}px ${mix(T.bg0, A.you, 0.22)}`,
      }}>
        <div style={{ fontFamily: MONO, fontSize: 20, letterSpacing: 3, color: A.you }}>③ WHAT I DID  →  <span style={{ color: T.muted }}>(this is where you live)</span></div>
        <div style={{ marginTop: 12 }}>
          {actions.map((a, i) => {
            const at = 0.30 + i * 0.085;
            const o = p(at, at + 0.06);
            const on = actLanded && hot === i;
            return (
              <div key={i} style={{
                display: "flex", alignItems: "center", gap: 14, height: rowH, opacity: o,
                transform: `translateX(${(1 - o) * 24}px)`,
              }}>
                <span style={{
                  fontFamily: MONO, fontWeight: 800, fontSize: 18, color: on ? T.bg0 : A.you,
                  background: on ? A.you : mix(T.panel, A.you, 0.18), border: `1.5px solid ${A.you}`,
                  borderRadius: 7, padding: "3px 9px", flexShrink: 0,
                }}>A{i + 1}</span>
                <span style={{ fontFamily: SANS, fontSize: 25, color: on ? T.text : mix(T.text, T.muted, 0.15), fontWeight: on ? 700 : 500, lineHeight: 1.2 }}>{a.d}</span>
              </div>
            );
          })}
        </div>
      </div>
      {/* RESULT */}
      <div style={{
        position: "absolute", left: 100, top: 728, width: 1030, height: 172, borderRadius: 16,
        background: mix(T.panel, A.res, 0.1), border: `2.5px solid ${A.res}`, padding: "14px 26px",
        boxSizing: "border-box", opacity: p(0.66, 0.74),
        boxShadow: `0 0 ${26 + Math.sin(frame * 0.06) * 10}px ${mix(T.bg0, A.res, 0.22)}`,
      }}>
        <div style={{ fontFamily: MONO, fontSize: 19, letterSpacing: 3, color: A.res }}>④ THE RESULT</div>
        <div style={{ display: "flex", gap: 30, marginTop: 12 }}>
          {metrics.map((m, i) => {
            const at = 0.68 + i * 0.045;
            return (
              <div key={i} style={{ opacity: p(at, at + 0.06), flex: 1 }}>
                <div style={{ fontFamily: MONO, fontWeight: 800, fontSize: 40, color: A.res, textShadow: `0 0 18px ${mix(T.bg0, A.res, 0.4)}`, lineHeight: 1 }}>{m.v}</div>
                <div style={{ fontFamily: SANS, fontSize: 20, color: T.muted, marginTop: 8, lineHeight: 1.2 }}>{m.l}</div>
              </div>
            );
          })}
        </div>
      </div>
      {/* LEARNING */}
      <div style={{
        position: "absolute", left: 1150, top: 728, width: 670, height: 172, borderRadius: 16,
        background: mix(T.panel, A.meta, 0.1), border: `2.5px solid ${A.meta}`, padding: "14px 24px",
        boxSizing: "border-box", opacity: p(0.82, 0.90),
      }}>
        <div style={{ fontFamily: MONO, fontSize: 19, letterSpacing: 3, color: A.meta }}>⑤ WHAT I LEARNED</div>
        <div style={{ fontFamily: SANS, fontSize: 24, fontStyle: "italic", color: T.text, marginTop: 10, lineHeight: 1.3 }}>{learning}</div>
      </div>
      <Foot theme={T} p={p(0.9, 0.97)}>{foot}</Foot>
    </Stage>
  );
};

// em_signals — the interviewer's scorecard (what they actually rate) ---------
const SignalsScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const rows = [
    { label: "Ownership", note: "“I”, not “we” — you drove it", v: 0.95, c: A.you },
    { label: "People judgment", note: "you treated humans as humans", v: 0.9, c: A.res },
    { label: "Structured thinking", note: "STAR — a clear spine", v: 0.85, c: A.sit },
    { label: "Measurable impact", note: "a number, not a vibe", v: 0.8, c: A.meta },
    { label: "Self-awareness", note: "what you'd do differently", v: 0.88, c: A.flag },
  ];
  const x0 = 640, barW = 900, rowH = 108, y0 = 250;
  return (
    <Stage>
      <Head theme={T} kicker="THE HIDDEN SCORECARD" title="What the interviewer is actually rating" o={p(0, 0.06)} />
      {rows.map((r, i) => {
        const at = 0.1 + i * 0.12;
        const grow = p(at, at + 0.16);
        const y = y0 + i * rowH;
        const hot = Math.floor(frame / 32) % rows.length === i;
        return (
          <React.Fragment key={i}>
            <div style={{ position: "absolute", left: 100, top: y + 6, width: 500, opacity: p(at - 0.04, at + 0.04) }}>
              <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 30, color: T.text }}>{r.label}</div>
              <div style={{ fontFamily: MONO, fontSize: 20, color: r.c, marginTop: 4 }}>{r.note}</div>
            </div>
            <div style={{ position: "absolute", left: x0, top: y + 8, width: barW, height: 56, borderRadius: 12, background: mix(T.panel, r.c, 0.05), border: `1.5px solid ${T.line}`, opacity: p(at - 0.04, at + 0.04) }} />
            <div style={{
              position: "absolute", left: x0, top: y + 8, width: barW * r.v * grow, height: 56, borderRadius: 12,
              background: `linear-gradient(90deg, ${mix(T.panel, r.c, 0.5)}, ${r.c})`, border: `2px solid ${r.c}`,
              boxShadow: hot ? `0 0 24px ${mix(T.bg0, r.c, 0.4)}` : "none",
            }} />
            <div style={{ position: "absolute", left: x0 + barW * r.v * grow + 16, top: y + 16, fontFamily: MONO, fontWeight: 800, fontSize: 30, color: r.c, opacity: grow }}>
              <Counter p={grow} to={Math.round(r.v * 10)} color={r.c} size={30} suffix=" / 10" />
            </div>
          </React.Fragment>
        );
      })}
      <Foot theme={T} p={p(0.84, 0.93)}>They aren't grading the story. They're grading these five things through it.</Foot>
    </Stage>
  );
};

// em_redflags — traps that sink candidates -----------------------------------
const RedFlagsScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const flags = [
    { t: "Blaming the team", d: "“They underperformed” — you're the manager; where were you?" },
    { t: "The lone hero", d: "You did everything; you developed no one." },
    { t: "No outcome", d: "The story just… ends. No metric, no result." },
    { t: "All “we”, no “I”", d: "Nothing you personally decided or owned." },
    { t: "No learning", d: "Nothing you'd change — so you didn't grow." },
    { t: "The 5-minute ramble", d: "No structure; the interviewer gets lost." },
  ];
  return (
    <Stage>
      <Head theme={T} kicker="INSTANT CREDIBILITY KILLERS" title="Six red flags that sink strong résumés" color={A.flag} o={p(0, 0.06)} />
      {flags.map((f, i) => {
        const col = i % 2, row = Math.floor(i / 2);
        const x = 100 + col * 870, y = 250 + row * 200;
        const at = 0.08 + i * 0.1;
        const o = p(at, at + 0.08);
        return (
          <div key={i} style={{
            position: "absolute", left: x, top: y, width: 820, height: 172, borderRadius: 18,
            background: mix(T.panel, A.flag, 0.07), border: `2px solid ${mix(T.line, A.flag, 0.5)}`,
            padding: "20px 26px", boxSizing: "border-box", opacity: o, transform: `translateY(${(1 - o) * 20}px)`,
          }}>
            <div style={{ display: "flex", alignItems: "center", gap: 14 }}>
              <span style={{ fontSize: 34, opacity: 0.5 + Math.sin(frame * 0.06 + i) * 0.3 }}>🚩</span>
              <span style={{ fontFamily: SANS, fontWeight: 800, fontSize: 32, color: A.flag, textDecoration: "line-through", textDecorationColor: mix(A.flag, T.bg0, 0.4) }}>{f.t}</span>
            </div>
            <div style={{ fontFamily: SANS, fontSize: 24, color: T.text, marginTop: 12, lineHeight: 1.3 }}>{f.d}</div>
          </div>
        );
      })}
      <Foot theme={T} p={p(0.85, 0.94)}>If your best story contains one of these, pick a different story.</Foot>
    </Stage>
  );
};

// em_matrix — the prep system: one story, many questions ---------------------
const MatrixScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const cols = ["People", "Conflict", "Delivery", "Failure"];
  const colC = [A.you, A.sit, A.res, A.meta];
  const stories = [
    { name: "Turned around an underperformer", hits: [1, 0, 1, 1] },
    { name: "The launch that slipped", hits: [1, 1, 1, 1] },
    { name: "Two staff engineers at war", hits: [1, 1, 0, 0] },
    { name: "Reorg no one asked for", hits: [1, 1, 1, 0] },
    { name: "The outage I owned", hits: [0, 1, 1, 1] },
  ];
  const nx = 760, cw = 250, rh = 92, y0 = 260, lx = 100;
  return (
    <Stage>
      <Head theme={T} kicker="THE PREP SYSTEM" title="One story, tagged for many questions" color={A.meta} o={p(0, 0.06)} />
      {/* column headers */}
      {cols.map((c, j) => (
        <div key={j} style={{ position: "absolute", left: nx + j * cw, top: y0 - 52, width: cw - 16, textAlign: "center", opacity: p(0.06, 0.16) }}>
          <span style={{ fontFamily: MONO, fontWeight: 800, fontSize: 22, letterSpacing: 2, color: colC[j] }}>{c.toUpperCase()}</span>
        </div>
      ))}
      {stories.map((s, i) => {
        const at = 0.12 + i * 0.11;
        const o = p(at, at + 0.08);
        const y = y0 + i * rh;
        return (
          <React.Fragment key={i}>
            <div style={{ position: "absolute", left: lx, top: y + 12, width: 630, opacity: o }}>
              <div style={{ fontFamily: MONO, fontWeight: 700, fontSize: 18, color: A.meta }}>STORY {i + 1}</div>
              <div style={{ fontFamily: SANS, fontWeight: 700, fontSize: 27, color: T.text, marginTop: 2 }}>{s.name}</div>
            </div>
            {s.hits.map((h, j) => {
              const cx = nx + j * cw + (cw - 16) / 2;
              const cyy = y + 30;
              const lit = h === 1;
              const chase = Math.floor(frame / 22) % stories.length === i;
              return (
                <div key={j} style={{
                  position: "absolute", left: cx - 26, top: cyy - 26, width: 52, height: 52, borderRadius: 12,
                  background: lit ? mix(T.panel, colC[j], chase ? 0.4 : 0.24) : "transparent",
                  border: `2px solid ${lit ? colC[j] : mix(T.line, T.muted, 0.2)}`,
                  display: "flex", alignItems: "center", justifyContent: "center", opacity: o,
                  boxShadow: lit && chase ? `0 0 18px ${mix(T.bg0, colC[j], 0.5)}` : "none",
                }}>
                  {lit && <span style={{ fontFamily: MONO, fontWeight: 800, fontSize: 26, color: colC[j] }}>✓</span>}
                </div>
              );
            })}
          </React.Fragment>
        );
      })}
      <div style={{ position: "absolute", left: 100, top: 740, width: 1680, textAlign: "center", opacity: p(0.74, 0.85) }}>
        <span style={{ fontFamily: SANS, fontSize: 30, color: T.text }}>
          You need <span style={{ color: A.meta, fontWeight: 800 }}>12–15 stories</span>, not 50. A good one answers four different questions from four different angles.
        </span>
      </div>
      <Foot theme={T} p={p(0.87, 0.95)}>Build the matrix before the interview. In the room, you're just picking a column.</Foot>
    </Stage>
  );
};

// em_recap (parameterized) ---------------------------------------------------
const RecapScene: React.FC<{ dur?: number; items?: string[]; closer?: string }> = ({
  dur, items = [], closer = "",
}) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  return (
    <AbsoluteFill style={{ padding: "60px 130px", justifyContent: "center" }}>
      <div style={{ opacity: p(0, 0.06), textAlign: "center", marginBottom: 26 }}>
        <Kicker theme={T} text="RECAP · THE WHOLE PLAYBOOK" cx />
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 60, color: T.text, marginTop: 12, letterSpacing: -1.5 }}>The EM interview in one breath</div>
      </div>
      <div style={{ display: "flex", flexDirection: "column", gap: 12, maxWidth: 1400, margin: "0 auto", width: "100%" }}>
        {items.map((it, i) => {
          const at = 0.06 + i * 0.09;
          const o = p(at, at + 0.07);
          const c = [A.you, A.res, A.sit, A.meta, A.flag, A.you, A.res][i % 7];
          return (
            <div key={i} style={{ display: "flex", alignItems: "center", gap: 18, opacity: o, transform: `translateX(${(1 - o) * -26}px)`, background: mix(T.panel, c, 0.06), border: `1.5px solid ${T.line}`, borderLeft: `5px solid ${c}`, borderRadius: 12, padding: "15px 26px" }}>
              <span style={{ color: c, fontFamily: MONO, fontWeight: 800, fontSize: 26 }}>{i + 1}</span>
              <span style={{ fontFamily: SANS, fontSize: 29, color: T.text, lineHeight: 1.25 }}>{it}</span>
            </div>
          );
        })}
      </div>
      <div style={{ textAlign: "center", marginTop: 32, opacity: p(0.82, 0.92) }}>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontStyle: "italic", fontSize: 40, color: A.you, textShadow: `0 0 ${28 + Math.sin(frame * 0.06) * 14}px ${mix(T.bg0, A.you, 0.7)}` }}>{closer}</div>
      </div>
    </AbsoluteFill>
  );
};

// ===========================================================================
export const EMScene: React.FC<{ variant: string;[key: string]: unknown }> = ({ variant, ...rest }) => {
  let content: React.ReactNode;
  let accent = A.you;
  switch (variant) {
    case "em_title": content = <TitleScene {...(rest as any)} />; break;
    case "em_titlex": content = <TitleXScene {...(rest as any)} />; break;
    case "em_hook": content = <HookScene {...(rest as any)} />; break;
    case "em_compass": content = <CompassScene {...(rest as any)} />; break;
    case "em_star": content = <StarScene {...(rest as any)} />; accent = A.meta; break;
    case "em_iwe": content = <IWeScene {...(rest as any)} />; accent = A.flag; break;
    case "em_divider": content = <DividerScene {...(rest as any)} />; accent = (rest as any).color || A.you; break;
    case "em_q": content = <QScene {...(rest as any)} />; accent = (rest as any).color || A.you; break;
    case "em_story": content = <StoryScene {...(rest as any)} />; accent = (rest as any).color || A.you; break;
    case "em_signals": content = <SignalsScene {...(rest as any)} />; accent = A.res; break;
    case "em_redflags": content = <RedFlagsScene {...(rest as any)} />; accent = A.flag; break;
    case "em_matrix": content = <MatrixScene {...(rest as any)} />; accent = A.meta; break;
    case "em_recap": content = <RecapScene {...(rest as any)} />; break;
    default: content = <TitleScene {...(rest as any)} />;
  }
  return (
    <AbsoluteFill>
      <Bg theme={T} accent={accent} />
      {content}
    </AbsoluteFill>
  );
};

export default EMScene;
