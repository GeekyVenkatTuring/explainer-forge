/**
 * DPScenes.tsx — "Design Patterns, felt before named" scene set (prefix `dp`).
 *
 * ONE scene set drives all 23 Gang-of-Four videos. Every pattern follows the exact
 * same 10-section teaching arc (scenario → naive code → pain → what varies vs fixed
 * → analogy → refactor → payoff → NAME it (UML) → tradeoffs → recap+challenge), so
 * each section is authored ONCE as a data-driven archetype variant and every pattern
 * is just narration + props in patterns.py. The pattern's NAME and UML are withheld
 * from the visuals until the reveal scene — that is the whole pedagogy.
 *
 * Identity (skills/04):
 *   theme accent = violet (structure / the pattern language) · motif = a fixed
 *   bracket with a hot-swappable module ("isolate what varies behind a stable slot").
 *   Semantic colors: FIXED=cyan (stable abstraction/interface) · VARY=amber (the
 *   family of behaviors that changes) · PAIN=red (rigid naive code, smells, edits to
 *   working code) · PAT=green (the clean pattern, the payoff, a new class added).
 *
 * Rules (skills/03): every scene takes `dur` and phases with useP(dur); continuous
 * motion in every frame (scan beams, Flow, dash-march wires, sine glow, a top
 * scene-progress bar); determinism via rnd(); no CSS filter. Captions are ON for this
 * series, so the bottom band is reserved for subtitles — content stays within y≈200–890
 * and Foot is avoided (skills/05).
 */
import React from "react";
import { AbsoluteFill, interpolate, useCurrentFrame } from "remotion";
import {
  makeTheme, mix, useP as usePfull, usePop, rnd, MONO, SANS, Theme,
  Bg, Stage, Kicker, Head, Card, Flow, Wire, Brackets, ScanBeam,
} from "../lib/primitives";

// A/V-SYNC: narration front-loads (names on-screen items early, then elaborates), so
// reveals are compressed into the front REVEAL_SPAN of the beat; the progress bar and
// continuous motion still run the FULL beat (usePfull), so no frozen tail. See
// skills/02 §"A/V-lag defect".
const REVEAL_SPAN = 0.6;
const useP = (dur?: unknown) => {
  const p = usePfull(dur);
  return (a: number, b: number) => p(Math.min(1, a * REVEAL_SPAN), Math.min(1, b * REVEAL_SPAN));
};

// ---------------------------------------------------------------- identity
const T = makeTheme({ accent: "#A78BFA", bg0: "#05060E", bg1: "#0A0C18", bg2: "#111528", panel: "#151A30" });
const A = {
  vio: "#A78BFA",   // structure / the pattern language (primary)
  fix: "#22D3EE",   // FIXED — the stable abstraction / interface
  var: "#FBBF24",   // VARY  — the family of behaviors that changes
  pain: "#F87171",  // PAIN  — rigid code, smells, edits to working code
  pat: "#34D399",   // PATTERN / payoff / clean extension
  muted: "#8B93B0",
};

// syntax palette for the Java code panels (muted, IDE-like)
const C = {
  kw: "#C792EA", type: "#7FD1F0", str: "#ECC48D", num: "#F78C6C",
  com: "#5C6a86", anno: "#82AAFF", txt: "#D7DCEC", punct: "#9AA3BE",
};
const KW = new Set(
  ("class interface enum record public private protected static final void return new if else for while switch " +
   "case break default implements extends abstract import package this null true false throws throw try catch " +
   "instanceof super do continue var boolean int double long char").split(" ")
);

// ---------------------------------------------------------------- code rendering
type Ln = { t: string; s?: "hi" | "dim" | "add" | "del" | "ghost" };

// deterministic per-line Java tokenizer → colored spans (no regex randomness)
function hlLine(line: string): React.ReactNode[] {
  let code = line, comment = "";
  const ci = line.indexOf("//");
  if (ci >= 0) { code = line.slice(0, ci); comment = line.slice(ci); }
  const toks = code.split(/(\s+|"[^"]*"|[A-Za-z_@][A-Za-z0-9_]*|[0-9]+)/).filter((t) => t !== "");
  const out: React.ReactNode[] = toks.map((t, i) => {
    if (/^\s+$/.test(t)) return <span key={i}>{t}</span>;
    let color = C.txt;
    if (/^"/.test(t)) color = C.str;
    else if (/^@/.test(t)) color = C.anno;
    else if (KW.has(t)) color = C.kw;
    else if (/^[0-9]/.test(t)) color = C.num;
    else if (/^[A-Z]/.test(t)) color = C.type;
    else if (/^[A-Za-z_]/.test(t)) color = C.txt;
    else color = C.punct;
    return <span key={i} style={{ color }}>{t}</span>;
  });
  if (comment) out.push(<span key="c" style={{ color: C.com, fontStyle: "italic" }}>{comment}</span>);
  return out;
}

/** A titled code panel; lines cascade in over `p`, per-line emphasis via `s`. */
const Code: React.FC<{
  lines: Ln[]; p: number; x: number; y: number; w: number; file?: string;
  size?: number; accent?: string; scan?: boolean;
}> = ({ lines, p, x, y, w, file, size = 25, accent = A.vio, scan = true }) => {
  const frame = useCurrentFrame();
  const lh = size * 1.62;
  const bodyH = lines.length * lh + 26;
  const total = 46 + bodyH;
  return (
    <div style={{
      position: "absolute", left: x, top: y, width: w, borderRadius: 16, overflow: "hidden",
      background: "rgba(6,9,18,0.92)", border: `2px solid ${mix(T.line, accent, 0.4)}`,
      boxShadow: `0 24px 70px rgba(0,0,0,0.5)`,
    }}>
      {/* title bar */}
      <div style={{
        height: 46, display: "flex", alignItems: "center", gap: 9, padding: "0 18px",
        background: mix(T.panel, accent, 0.1), borderBottom: `1.5px solid ${mix(T.line, accent, 0.4)}`,
      }}>
        <span style={{ width: 12, height: 12, borderRadius: 12, background: "#FF5F56", display: "inline-block" }} />
        <span style={{ width: 12, height: 12, borderRadius: 12, background: "#FFBD2E", display: "inline-block" }} />
        <span style={{ width: 12, height: 12, borderRadius: 12, background: "#27C93F", display: "inline-block" }} />
        <span style={{ fontFamily: MONO, fontSize: 20, color: T.muted, marginLeft: 12 }}>{file || "Main.java"}</span>
      </div>
      <div style={{ position: "relative", padding: "13px 0", overflow: "hidden" }}>
        {scan && (
          <div style={{
            position: "absolute", left: 0, right: 0, height: 40, opacity: 0.5,
            top: ((frame * 1.7) % (bodyH + 40)) - 40,
            background: `linear-gradient(180deg, transparent, ${mix(T.bg0, accent, 0.4)}22)`,
          }} />
        )}
        {lines.map((ln, i) => {
          const rv = Math.max(0, Math.min(1, p * lines.length - i));
          const emph = ln.s;
          const bg = emph === "hi" ? mix("#06090F", accent, 0.16)
            : emph === "add" ? mix("#06090F", A.pat, 0.14)
            : emph === "del" ? mix("#06090F", A.pain, 0.14) : "transparent";
          const bar = emph === "hi" ? accent : emph === "add" ? A.pat : emph === "del" ? A.pain : "transparent";
          const op = (emph === "dim" ? 0.4 : emph === "ghost" ? 0.22 : 1) * rv;
          return (
            <div key={i} style={{
              display: "flex", alignItems: "center", minHeight: lh, padding: "0 20px 0 16px",
              background: bg, borderLeft: `3px solid ${bar}`, opacity: op,
              transform: `translateX(${(1 - rv) * 10}px)`,
            }}>
              <span style={{
                fontFamily: MONO, fontSize: size, lineHeight: 1.5, whiteSpace: "pre",
                textDecoration: emph === "del" ? "line-through" : "none",
                textDecorationColor: A.pain,
              }}>
                {ln.t === "" ? " " : (emph === "ghost" ? <span style={{ color: mix(T.muted, accent, 0.4) }}>{ln.t}</span> : hlLine(ln.t))}
              </span>
            </div>
          );
        })}
      </div>
    </div>
  );
};

// convenience: build Ln[] from a list of [text, state?] tuples
const L = (rows: (string | [string, Ln["s"]])[]): Ln[] =>
  rows.map((r) => (typeof r === "string" ? { t: r } : { t: r[0], s: r[1] }));

// ---------------------------------------------------------------- motif: swap-slot
/** A fixed bracket with a module that swaps — the soul of the pattern language. */
const SwapSlot: React.FC<{ x: number; y: number; s?: number; o?: number; labels?: string[] }> = ({
  x, y, s = 1, o = 1, labels = ["A", "B", "C"],
}) => {
  const frame = useCurrentFrame();
  const idx = Math.floor(frame / 40) % labels.length;
  const rise = (Math.sin(frame * 0.12) + 1) / 2;
  return (
    <div style={{ position: "absolute", left: x, top: y, opacity: o, transform: `scale(${s})`, transformOrigin: "top left" }}>
      {/* fixed frame (cyan) */}
      <div style={{ position: "absolute", left: 0, top: 0, width: 190, height: 150, borderRadius: 16, border: `2.5px dashed ${A.fix}`, background: mix(T.panel, A.fix, 0.05) }} />
      <div style={{ position: "absolute", left: 0, top: -30, fontFamily: MONO, fontSize: 18, color: A.fix, letterSpacing: 2 }}>FIXED SLOT</div>
      {/* swappable module (amber) sitting in the slot */}
      <div style={{
        position: "absolute", left: 24, top: 24 - rise * 6, width: 142, height: 102, borderRadius: 12,
        background: mix(T.panel, A.var, 0.22), border: `2.5px solid ${A.var}`,
        display: "flex", alignItems: "center", justifyContent: "center",
        boxShadow: `0 0 ${18 + rise * 16}px ${mix(T.bg0, A.var, 0.5)}`,
      }}>
        <span style={{ fontFamily: SANS, fontWeight: 800, fontSize: 46, color: A.var }}>{labels[idx]}</span>
      </div>
    </div>
  );
};

// scene-progress bar (universal "this is playing" signal) — uses the FULL-beat clock
const SceneProgress: React.FC<{ dur?: unknown; color?: string }> = ({ dur, color = A.vio }) => {
  const pf = usePfull(dur);
  return (
    <div style={{ position: "absolute", left: 0, top: 0, height: 5, width: `${interpolate(pf(0, 1), [0, 1], [0, 100])}%`, background: `linear-gradient(90deg, ${color}, ${mix(color, "#ffffff", 0.3)})`, opacity: 0.8 }} />
  );
};

// small labeled chip
const Chip: React.FC<{ text: string; color: string; o?: number; big?: boolean }> = ({ text, color, o = 1, big }) => (
  <span style={{
    fontFamily: MONO, fontWeight: 700, fontSize: big ? 25 : 21, color: T.bg0, background: color,
    borderRadius: 999, padding: big ? "9px 22px" : "6px 16px", opacity: o, whiteSpace: "nowrap",
  }}>{text}</span>
);

// =====================================================================================
// ARCHETYPE VARIANTS (each = one section of the fixed 10-part arc, driven by props)
// =====================================================================================

// dp_title — §hook cold open. Teases the PROBLEM; never names the pattern. -----------
const TitleScene: React.FC<{ dur?: number; ep?: string; kicker?: string; line1?: string; line2?: string; sub?: string }> =
({ dur, ep = "EPISODE", kicker = "DESIGN PATTERNS", line1 = "The code that", line2 = "fights every change", sub = "" }) => {
  const frame = useCurrentFrame();
  const p = useP(dur); const pop = usePop(dur);
  return (
    <AbsoluteFill style={{ alignItems: "center", justifyContent: "center" }}>
      <SwapSlot x={1500} y={200} s={1.1} o={0.5 + p(0.3, 0.6) * 0.4} />
      <SwapSlot x={210} y={720} s={0.9} o={0.4 + p(0.4, 0.7) * 0.4} labels={["if", "el", "sw"]} />
      {Array.from({ length: 9 }).map((_, i) => {
        const ang = frame * 0.01 + (i / 9) * Math.PI * 2;
        return <div key={i} style={{ position: "absolute", left: 960 + Math.cos(ang) * (560 + i * 12) - 5, top: 540 + Math.sin(ang) * (250 + i * 7) - 5, width: 8, height: 8, borderRadius: 8, background: A.vio, opacity: 0.2 + rnd(i, 3) * 0.25, boxShadow: `0 0 12px ${A.vio}` }} />;
      })}
      <div style={{ textAlign: "center", transform: `scale(${0.93 + pop(0) * 0.07})`, maxWidth: 1400 }}>
        <div style={{ display: "flex", justifyContent: "center", marginBottom: 24 }}>
          <Kicker theme={T} text={`${kicker} · ${ep}`} cx />
        </div>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 104, lineHeight: 1.03, letterSpacing: -3, color: T.text }}>
          <div>{line1}</div>
          <div style={{ color: A.vio, textShadow: `0 0 70px ${mix(T.bg0, A.vio, 0.7)}` }}>{line2}</div>
        </div>
        <div style={{ height: 5, width: interpolate(p(0.2, 0.5), [0, 1], [0, 560]), background: `linear-gradient(90deg, ${A.pain}, ${A.pat})`, borderRadius: 3, margin: "30px auto" }} />
        <div style={{ fontFamily: SANS, fontSize: 36, color: T.muted, opacity: p(0.32, 0.55) }}>{sub}</div>
      </div>
    </AbsoluteFill>
  );
};

// dp_scenario — §1 concrete scenario / the decision -----------------------------------
const ScenarioScene: React.FC<{ dur?: number; kicker?: string; title?: string; situation?: string; actors?: { emoji: string; label: string }[]; ask?: string }> =
({ dur, kicker = "THE SCENARIO", title = "", situation = "", actors = [], ask = "" }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const n = actors.length;
  const gap = n > 0 ? 1520 / n : 0;
  return (
    <Stage>
      <Head theme={T} kicker={kicker} title={title} color={A.fix} o={p(0, 0.06)} />
      <Card theme={T} x={200} y={230} w={1520} color={A.fix} o={p(0.06, 0.16)} glow>
        <div style={{ fontFamily: SANS, fontSize: 33, color: T.text, lineHeight: 1.4 }}>{situation}</div>
      </Card>
      {actors.map((ac, i) => {
        const x = 200 + i * gap + gap / 2 - 130;
        const at = 0.22 + i * 0.08;
        const hot = Math.floor(frame / 30) % Math.max(1, n) === i;
        return (
          <div key={i} style={{ position: "absolute", left: x, top: 470, width: 260, textAlign: "center", opacity: p(at, at + 0.09), transform: `translateY(${(1 - p(at, at + 0.09)) * 20}px)` }}>
            <div style={{ width: 200, height: 200, margin: "0 auto", borderRadius: 24, background: mix(T.panel, hot ? A.var : A.vio, hot ? 0.16 : 0.07), border: `2.5px solid ${hot ? A.var : mix(T.line, A.vio, 0.5)}`, display: "flex", alignItems: "center", justifyContent: "center", boxShadow: hot ? `0 0 30px ${mix(T.bg0, A.var, 0.4)}` : "none" }}>
              <span style={{ fontSize: 96 }}>{ac.emoji}</span>
            </div>
            <div style={{ fontFamily: MONO, fontSize: 24, color: hot ? A.var : T.muted, marginTop: 16 }}>{ac.label}</div>
          </div>
        );
      })}
      <div style={{ position: "absolute", left: 260, top: 748, right: 260, textAlign: "center", opacity: p(0.6, 0.74) }}>
        <span style={{ fontFamily: SANS, fontWeight: 800, fontStyle: "italic", fontSize: 40, color: A.var, textShadow: `0 0 ${26 + Math.sin(frame * 0.06) * 12}px ${mix(T.bg0, A.var, 0.6)}` }}>{ask}</span>
      </div>
    </Stage>
  );
};

// dp_code — §2 naive solution & general code states ----------------------------------
const CodeScene: React.FC<{ dur?: number; kicker?: string; title?: string; color?: string; file?: string; lines?: Ln[]; note?: string; size?: number }> =
({ dur, kicker = "FIRST ATTEMPT", title = "", color = A.vio, file, lines = [], note = "", size = 25 }) => {
  const p = useP(dur);
  const w = 1360;
  return (
    <Stage>
      <Head theme={T} kicker={kicker} title={title} color={color} o={p(0, 0.06)} />
      <Code lines={lines} p={p(0.08, 0.9)} x={(1920 - w) / 2} y={210} w={w} file={file} accent={color} size={size} />
      {note && <div style={{ position: "absolute", left: 200, right: 200, top: 866, textAlign: "center", fontFamily: MONO, fontSize: 23, color: T.muted, opacity: p(0.7, 0.82) }}>{note}</div>}
    </Stage>
  );
};

// dp_pain — §3 make the pain visible (emotional peak) ---------------------------------
const PainScene: React.FC<{ dur?: number; kicker?: string; title?: string; file?: string; lines?: Ln[]; smell?: string; touched?: string[]; size?: number }> =
({ dur, kicker = "ADD ONE REQUIREMENT", title = "", file, lines = [], smell = "", touched = [], size = 24 }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const w = 1180;
  const pulse = 0.6 + Math.sin(frame * 0.12) * 0.4;
  return (
    <Stage>
      <Head theme={T} kicker={kicker} title={title} color={A.pain} o={p(0, 0.06)} />
      <Code lines={lines} p={p(0.06, 0.7)} x={110} y={210} w={w} file={file} accent={A.pain} size={size} />
      {/* right rail: the smell + everywhere you must touch */}
      <div style={{ position: "absolute", left: 1330, top: 220, width: 480 }}>
        <div style={{ opacity: p(0.5, 0.62), background: mix(T.panel, A.pain, 0.14), border: `2.5px solid ${A.pain}`, borderRadius: 16, padding: "18px 22px", boxShadow: `0 0 ${20 + pulse * 20}px ${mix(T.bg0, A.pain, 0.4)}` }}>
          <div style={{ fontFamily: MONO, fontSize: 19, color: A.pain, letterSpacing: 2 }}>CODE SMELL</div>
          <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 34, color: T.text, marginTop: 8, lineHeight: 1.15 }}>{smell}</div>
        </div>
        <div style={{ marginTop: 26, opacity: p(0.62, 0.74) }}>
          <div style={{ fontFamily: MONO, fontSize: 19, color: T.muted, letterSpacing: 2, marginBottom: 12 }}>YOU HAD TO EDIT WORKING CODE:</div>
          {touched.map((tt, i) => {
            const at = 0.66 + i * 0.05;
            return (
              <div key={i} style={{ display: "flex", alignItems: "center", gap: 12, marginBottom: 12, opacity: p(at, at + 0.06) }}>
                <span style={{ color: A.pain, fontSize: 26 }}>✎</span>
                <span style={{ fontFamily: MONO, fontSize: 23, color: T.text }}>{tt}</span>
              </div>
            );
          })}
        </div>
      </div>
    </Stage>
  );
};

// dp_insight — §4 what varies vs what stays fixed -------------------------------------
const InsightScene: React.FC<{ dur?: number; kicker?: string; title?: string; fixed?: string[]; varies?: string[]; principle?: string }> =
({ dur, kicker = "STEP BACK", title = "What changes, what stays", fixed = [], varies = [], principle = "" }) => {
  const p = useP(dur);
  const col = (items: string[], label: string, color: string, x: number, atBase: number) => (
    <div style={{ position: "absolute", left: x, top: 250, width: 620 }}>
      <div style={{ fontFamily: MONO, fontSize: 22, color, letterSpacing: 3, marginBottom: 14, opacity: p(atBase, atBase + 0.06) }}>{label}</div>
      {items.map((it, i) => {
        const at = atBase + 0.08 + i * 0.07;
        return (
          <div key={i} style={{ display: "flex", alignItems: "center", gap: 14, marginBottom: 14, background: mix(T.panel, color, 0.08), border: `2px solid ${mix(T.line, color, 0.6)}`, borderRadius: 12, padding: "16px 20px", opacity: p(at, at + 0.07), transform: `translateY(${(1 - p(at, at + 0.07)) * 16}px)` }}>
            <span style={{ width: 10, height: 10, borderRadius: 10, background: color, flexShrink: 0 }} />
            <span style={{ fontFamily: SANS, fontSize: 27, color: T.text, lineHeight: 1.25 }}>{it}</span>
          </div>
        );
      })}
    </div>
  );
  return (
    <Stage>
      <Head theme={T} kicker={kicker} title={title} color={A.vio} o={p(0, 0.06)} />
      {col(fixed, "STAYS FIXED", A.fix, 120, 0.1)}
      <SwapSlot x={862} y={430} s={1.0} o={p(0.34, 0.5)} />
      {col(varies, "THIS VARIES", A.var, 1180, 0.22)}
      <div style={{ position: "absolute", left: 200, right: 200, top: 878, textAlign: "center", opacity: p(0.66, 0.8) }}>
        <span style={{ fontFamily: SANS, fontWeight: 700, fontSize: 30, color: A.pat }}>{principle}</span>
      </div>
    </Stage>
  );
};

// dp_analogy — §5 analogy + where it breaks ------------------------------------------
const AnalogyScene: React.FC<{ dur?: number; kicker?: string; title?: string; emoji?: string; analogy?: string; map?: { from: string; to: string }[]; breaks?: string }> =
({ dur, kicker = "AN ANALOGY", title = "", emoji = "🔌", analogy = "", map = [], breaks = "" }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  return (
    <Stage>
      <Head theme={T} kicker={kicker} title={title} color={A.var} o={p(0, 0.06)} />
      <div style={{ position: "absolute", left: 120, top: 250, width: 640, textAlign: "center", opacity: p(0.08, 0.2) }}>
        <div style={{ fontSize: 190, transform: `translateY(${Math.sin(frame * 0.05) * 6}px)` }}>{emoji}</div>
        <div style={{ fontFamily: SANS, fontWeight: 700, fontSize: 30, color: T.text, marginTop: 10, lineHeight: 1.35 }}>{analogy}</div>
      </div>
      <div style={{ position: "absolute", left: 820, top: 250, width: 1000 }}>
        <div style={{ fontFamily: MONO, fontSize: 20, color: T.muted, letterSpacing: 2, marginBottom: 14, opacity: p(0.24, 0.32) }}>MAPS ONTO THE CODE</div>
        {map.map((m, i) => {
          const at = 0.3 + i * 0.08;
          return (
            <div key={i} style={{ display: "flex", alignItems: "center", gap: 16, marginBottom: 14, opacity: p(at, at + 0.07) }}>
              <span style={{ fontFamily: SANS, fontSize: 26, color: A.var, width: 380 }}>{m.from}</span>
              <span style={{ color: A.vio, fontSize: 26 }}>→</span>
              <span style={{ fontFamily: MONO, fontSize: 25, color: A.fix }}>{m.to}</span>
            </div>
          );
        })}
        {breaks && (
          <div style={{ marginTop: 22, background: mix(T.panel, A.pain, 0.12), border: `2px solid ${A.pain}`, borderRadius: 14, padding: "16px 22px", opacity: p(0.72, 0.84) }}>
            <span style={{ fontFamily: MONO, fontSize: 20, color: A.pain, letterSpacing: 2 }}>WHERE THE ANALOGY BREAKS  </span>
            <span style={{ fontFamily: SANS, fontSize: 25, color: T.text, lineHeight: 1.35 }}>{breaks}</span>
          </div>
        )}
      </div>
    </Stage>
  );
};

// dp_refactor — §6 one refactor move (before dim/strike → after add) ------------------
const RefactorScene: React.FC<{ dur?: number; step?: number; of?: number; move?: string; file?: string; lines?: Ln[]; note?: string; size?: number }> =
({ dur, step = 1, of = 3, move = "", file, lines = [], note = "", size = 24 }) => {
  const p = useP(dur);
  const w = 1360;
  return (
    <Stage>
      <div style={{ position: "absolute", left: 100, top: 54, right: 100, display: "flex", alignItems: "center", gap: 18, opacity: p(0, 0.06) }}>
        <Chip text={`MOVE ${step} / ${of}`} color={A.pat} big />
        <span style={{ fontFamily: SANS, fontWeight: 800, fontSize: 46, color: T.text, letterSpacing: -1 }}>{move}</span>
      </div>
      <Code lines={lines} p={p(0.1, 0.82)} x={(1920 - w) / 2} y={200} w={w} file={file} accent={A.pat} size={size} />
      {note && <div style={{ position: "absolute", left: 200, right: 200, top: 866, textAlign: "center", fontFamily: MONO, fontSize: 23, color: T.muted, opacity: p(0.72, 0.84) }}>{note}</div>}
    </Stage>
  );
};

// dp_try — §6 fading / retrieval "pause here and try it yourself" ---------------------
const TryScene: React.FC<{ dur?: number; title?: string; file?: string; lines?: Ln[]; prompt?: string; hint?: string; size?: number }> =
({ dur, title = "Your turn", file, lines = [], prompt = "", hint = "", size = 24 }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const w = 1160;
  const pulse = 0.55 + Math.sin(frame * 0.09) * 0.45;
  return (
    <Stage>
      <div style={{ position: "absolute", left: 100, top: 54, right: 100, display: "flex", alignItems: "center", gap: 18, opacity: p(0, 0.06) }}>
        <Chip text="PAUSE & TRY" color={A.var} big />
        <span style={{ fontFamily: SANS, fontWeight: 800, fontSize: 46, color: T.text, letterSpacing: -1 }}>{title}</span>
      </div>
      <Code lines={lines} p={p(0.08, 0.55)} x={110} y={200} w={w} file={file} accent={A.var} size={size} />
      <div style={{ position: "absolute", left: 1330, top: 210, width: 480 }}>
        <div style={{ opacity: p(0.4, 0.55), background: mix(T.panel, A.var, 0.14), border: `2.5px solid ${A.var}`, borderRadius: 16, padding: "20px 24px", boxShadow: `0 0 ${18 + pulse * 22}px ${mix(T.bg0, A.var, 0.4)}` }}>
          <div style={{ fontSize: 60, textAlign: "center" }}>⏸️</div>
          <div style={{ fontFamily: SANS, fontWeight: 700, fontSize: 29, color: T.text, marginTop: 12, lineHeight: 1.35 }}>{prompt}</div>
        </div>
        {hint && (
          <div style={{ marginTop: 22, opacity: p(0.6, 0.72), fontFamily: MONO, fontSize: 22, color: A.fix, lineHeight: 1.4 }}>
            <span style={{ color: T.muted }}>hint · </span>{hint}
          </div>
        )}
      </div>
    </Stage>
  );
};

// dp_payoff — §7 same requirement, now trivial (naive vs pattern, side by side) -------
const PayoffScene: React.FC<{ dur?: number; kicker?: string; requirement?: string; naiveLabel?: string; naiveCost?: string; naiveSteps?: string[]; patLabel?: string; patCost?: string; patLines?: Ln[]; patFile?: string }> =
({ dur, kicker = "SAME REQUIREMENT, AGAIN", requirement = "", naiveLabel = "Before", naiveCost = "", naiveSteps = ["reopen a working file", "edit + recompile the core", "re-test everything"], patLabel = "Now", patCost = "", patLines = [], patFile = "NewThing.java" }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  return (
    <Stage>
      <Head theme={T} kicker={kicker} title={requirement} color={A.pat} o={p(0, 0.06)} />
      {/* left: the old cost (red) */}
      <div style={{ position: "absolute", left: 120, top: 240, width: 600, height: 560, borderRadius: 18, background: mix(T.panel, A.pain, 0.08), border: `2.5px solid ${A.pain}`, opacity: p(0.1, 0.22), padding: "26px 30px", boxSizing: "border-box" }}>
        <Chip text={naiveLabel} color={A.pain} />
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 40, color: A.pain, marginTop: 24, lineHeight: 1.2 }}>{naiveCost}</div>
        <div style={{ position: "absolute", left: 30, bottom: 30, right: 30 }}>
          {naiveSteps.slice(0, 3).map((s, i) => (
            <div key={i} style={{ display: "flex", gap: 10, alignItems: "center", marginBottom: 10, opacity: p(0.3 + i * 0.05, 0.4 + i * 0.05) }}>
              <span style={{ color: A.pain, fontSize: 22 }}>✎</span>
              <span style={{ fontFamily: MONO, fontSize: 22, color: T.muted }}>{s}</span>
            </div>
          ))}
        </div>
      </div>
      <div style={{ position: "absolute", left: 748, top: 480, fontSize: 60, color: A.vio, opacity: p(0.4, 0.5) }}>➜</div>
      {/* right: the new cost (green) — add one class, touch nothing */}
      <div style={{ position: "absolute", left: 900, top: 240, width: 900, height: 560, borderRadius: 18, background: mix(T.panel, A.pat, 0.08), border: `2.5px solid ${A.pat}`, opacity: p(0.24, 0.38), padding: "26px 30px", boxSizing: "border-box", boxShadow: `0 0 ${24 + Math.sin(frame * 0.06) * 12}px ${mix(T.bg0, A.pat, 0.3)}` }}>
        <Chip text={patLabel} color={A.pat} />
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 34, color: A.pat, margin: "16px 0 14px", lineHeight: 1.2 }}>{patCost}</div>
        <Code lines={patLines} p={p(0.4, 0.82)} x={0} y={130} w={840} file={patFile} accent={A.pat} size={22} scan={false} />
      </div>
    </Stage>
  );
};

// dp_reveal — §8 NOW name it: the pattern name + UML structure ------------------------
type UmlNode = { id: string; title: string; stereo?: string; members?: string[]; x: number; y: number; w: number; h?: number; color?: string };
type UmlEdge = { from: string; to: string; kind?: "impl" | "assoc" | "has"; label?: string };
const RevealScene: React.FC<{ dur?: number; name?: string; nodes?: UmlNode[]; edges?: UmlEdge[]; plain?: string }> =
({ dur, name = "The Pattern", nodes = [], edges = [], plain = "" }) => {
  const frame = useCurrentFrame();
  const p = useP(dur); const pop = usePop(dur);
  const byId = (id: string) => nodes.find((n) => n.id === id)!;
  const hh = (n: UmlNode) => n.h || (46 + (n.stereo ? 24 : 0) + (n.members?.length || 0) * 30 + 20);
  return (
    <Stage>
      <div style={{ position: "absolute", left: 100, top: 46, right: 100, textAlign: "center", opacity: p(0, 0.08), transform: `scale(${0.9 + pop(0) * 0.1})` }}>
        <div style={{ fontFamily: MONO, fontSize: 22, color: A.vio, letterSpacing: 8 }}>IT HAS A NAME</div>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 76, color: A.vio, letterSpacing: -2, textShadow: `0 0 ${40 + Math.sin(frame * 0.05) * 16}px ${mix(T.bg0, A.vio, 0.7)}` }}>{name}</div>
      </div>
      {/* UML edges (draw under nodes). impl = child top → parent bottom-center
          (converging tree); has/assoc = right-of-source → left-of-target (horizontal). */}
      {edges.map((e, i) => {
        const a = byId(e.from), b = byId(e.to);
        const at = 0.3 + i * 0.05;
        if (e.kind === "impl") {
          const x1 = a.x + a.w / 2, y1 = a.y, x2 = b.x + b.w / 2, y2 = b.y + hh(b) + 14;
          return <Wire key={i} x1={x1} y1={y1} x2={x2} y2={y2} p={p(at, at + 0.08)} color={A.fix} w={2.5} arrow={false} />;
        }
        // association: connect on the sides that face each other (orient by x)
        const aLeft = a.x + a.w / 2 <= b.x + b.w / 2;
        const sx = aLeft ? a.x + a.w : a.x, tx = aLeft ? b.x : b.x + b.w;
        const sy = a.y + hh(a) / 2, ty = b.y + hh(b) / 2;
        return <Wire key={i} x1={sx} y1={sy} x2={tx} y2={ty} p={p(at, at + 0.08)} color={A.var} w={2.5} arrow />;
      })}
      {/* one shared hollow generalization triangle per parent interface */}
      {Array.from(new Set(edges.filter((e) => e.kind === "impl").map((e) => e.to))).map((tid, i) => {
        const b = byId(tid);
        return <div key={"t" + i} style={{ position: "absolute", left: b.x + b.w / 2 - 11, top: b.y + hh(b), width: 0, height: 0, borderLeft: "11px solid transparent", borderRight: "11px solid transparent", borderBottom: `15px solid ${A.fix}`, opacity: p(0.34, 0.46) }} />;
      })}
      {nodes.map((n, i) => {
        const at = 0.18 + i * 0.07;
        const color = n.color || A.vio;
        return (
          <div key={n.id} style={{ position: "absolute", left: n.x, top: n.y, width: n.w, borderRadius: 12, overflow: "hidden", background: mix(T.panel, color, 0.1), border: `2.5px solid ${color}`, opacity: p(at, at + 0.08), transform: `translateY(${(1 - p(at, at + 0.08)) * 16}px)` }}>
            <div style={{ padding: "10px 0", textAlign: "center", borderBottom: `1.5px solid ${mix(T.line, color, 0.5)}`, background: mix(T.panel, color, 0.06) }}>
              {n.stereo && <div style={{ fontFamily: MONO, fontSize: 18, color: T.muted }}>«{n.stereo}»</div>}
              <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 27, color }}>{n.title}</div>
            </div>
            {(n.members || []).map((m, j) => (
              <div key={j} style={{ fontFamily: MONO, fontSize: 20, color: T.text, padding: "5px 16px", borderBottom: j < (n.members!.length - 1) ? `1px solid ${T.line}` : "none" }}>{m}</div>
            ))}
          </div>
        );
      })}
      <div style={{ position: "absolute", left: 200, right: 200, top: 866, textAlign: "center", opacity: p(0.72, 0.84) }}>
        <span style={{ fontFamily: SANS, fontStyle: "italic", fontSize: 28, color: T.text }}>{plain}</span>
      </div>
    </Stage>
  );
};

// dp_map — §8 participants mapped to classes you wrote + definitions ------------------
const MapScene: React.FC<{ dur?: number; kicker?: string; title?: string; participants?: { role: string; your: string }[]; plain?: string; gof?: string }> =
({ dur, kicker = "THE PARTICIPANTS", title = "Names, mapped to your code", participants = [], plain = "", gof = "" }) => {
  const p = useP(dur);
  return (
    <Stage>
      <Head theme={T} kicker={kicker} title={title} color={A.vio} o={p(0, 0.06)} />
      <div style={{ position: "absolute", left: 120, top: 240, width: 900 }}>
        <div style={{ display: "flex", gap: 20, marginBottom: 14, opacity: p(0.08, 0.16) }}>
          <span style={{ fontFamily: MONO, fontSize: 19, color: A.vio, letterSpacing: 2, width: 360 }}>GoF ROLE</span>
          <span style={{ fontFamily: MONO, fontSize: 19, color: A.fix, letterSpacing: 2 }}>THE CLASS YOU WROTE</span>
        </div>
        {participants.map((pt, i) => {
          const at = 0.14 + i * 0.08;
          return (
            <div key={i} style={{ display: "flex", alignItems: "center", gap: 20, marginBottom: 12, background: mix(T.panel, A.vio, 0.05), border: `1.5px solid ${T.line}`, borderLeft: `4px solid ${A.vio}`, borderRadius: 12, padding: "14px 22px", opacity: p(at, at + 0.07), transform: `translateX(${(1 - p(at, at + 0.07)) * -20}px)` }}>
              <span style={{ fontFamily: SANS, fontWeight: 700, fontSize: 26, color: A.vio, width: 340 }}>{pt.role}</span>
              <span style={{ color: T.muted }}>→</span>
              <span style={{ fontFamily: MONO, fontSize: 24, color: A.fix }}>{pt.your}</span>
            </div>
          );
        })}
      </div>
      <div style={{ position: "absolute", left: 1080, top: 250, width: 740 }}>
        <div style={{ background: mix(T.panel, A.pat, 0.08), border: `2px solid ${mix(T.line, A.pat, 0.6)}`, borderRadius: 14, padding: "20px 24px", opacity: p(0.5, 0.62) }}>
          <div style={{ fontFamily: MONO, fontSize: 19, color: A.pat, letterSpacing: 2, marginBottom: 10 }}>IN PLAIN ENGLISH</div>
          <div style={{ fontFamily: SANS, fontSize: 27, color: T.text, lineHeight: 1.4 }}>{plain}</div>
        </div>
        <div style={{ marginTop: 22, background: mix(T.panel, A.vio, 0.08), border: `2px solid ${mix(T.line, A.vio, 0.6)}`, borderRadius: 14, padding: "20px 24px", opacity: p(0.64, 0.78) }}>
          <div style={{ fontFamily: MONO, fontSize: 19, color: A.vio, letterSpacing: 2, marginBottom: 10 }}>GANG OF FOUR</div>
          <div style={{ fontFamily: SANS, fontStyle: "italic", fontSize: 24, color: T.muted, lineHeight: 1.42 }}>{gof}</div>
        </div>
      </div>
    </Stage>
  );
};

// dp_tradeoffs — §9 costs + when NOT to use + the one signal ---------------------------
const TradeoffScene: React.FC<{ dur?: number; kicker?: string; title?: string; costs?: string[]; dont?: string[]; signal?: string }> =
({ dur, kicker = "THE HONEST COST", title = "When NOT to reach for it", costs = [], dont = [], signal = "" }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const list = (items: string[], label: string, color: string, icon: string, x: number, atBase: number) => (
    <div style={{ position: "absolute", left: x, top: 250, width: 800 }}>
      <div style={{ fontFamily: MONO, fontSize: 21, color, letterSpacing: 3, marginBottom: 14, opacity: p(atBase, atBase + 0.06) }}>{label}</div>
      {items.map((it, i) => {
        const at = atBase + 0.08 + i * 0.06;
        return (
          <div key={i} style={{ display: "flex", alignItems: "flex-start", gap: 14, marginBottom: 13, opacity: p(at, at + 0.06) }}>
            <span style={{ color, fontSize: 24, marginTop: 2 }}>{icon}</span>
            <span style={{ fontFamily: SANS, fontSize: 26, color: T.text, lineHeight: 1.3 }}>{it}</span>
          </div>
        );
      })}
    </div>
  );
  return (
    <Stage>
      <Head theme={T} kicker={kicker} title={title} color={A.pain} o={p(0, 0.06)} />
      {list(costs, "IT COSTS YOU", A.pain, "▲", 120, 0.1)}
      {list(dont, "SKIP IT WHEN", A.muted, "—", 980, 0.28)}
      <div style={{ position: "absolute", left: 120, top: 792, width: 1680, background: mix(T.panel, A.pat, 0.1), border: `2.5px solid ${A.pat}`, borderRadius: 16, padding: "20px 28px", opacity: p(0.62, 0.76), boxShadow: `0 0 ${20 + Math.sin(frame * 0.06) * 12}px ${mix(T.bg0, A.pat, 0.3)}` }}>
        <span style={{ fontFamily: MONO, fontSize: 20, color: A.pat, letterSpacing: 2 }}>REACH FOR IT WHEN  </span>
        <span style={{ fontFamily: SANS, fontWeight: 700, fontSize: 30, color: T.text }}>{signal}</span>
      </div>
    </Stage>
  );
};

// dp_recap — §10 three-bullet recap + a "pause and predict" challenge (ends here) -----
const RecapScene: React.FC<{ dur?: number; kicker?: string; title?: string; items?: string[]; challenge?: string; question?: string }> =
({ dur, kicker = "THE JOURNEY", title = "Problem → insight → pattern", items = [], challenge = "", question = "" }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const cols = [A.pain, A.var, A.pat];
  const labs = ["PROBLEM", "INSIGHT", "PATTERN"];
  return (
    <Stage>
      <div style={{ position: "absolute", left: 100, top: 60, right: 100, textAlign: "center", opacity: p(0, 0.06) }}>
        <Kicker theme={T} text={kicker} cx />
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 54, color: T.text, marginTop: 10, letterSpacing: -1 }}>{title}</div>
      </div>
      {items.slice(0, 3).map((it, i) => {
        const at = 0.1 + i * 0.09;
        const x = 120 + i * 570;
        return (
          <div key={i} style={{ position: "absolute", left: x, top: 220, width: 520, height: 250, background: mix(T.panel, cols[i], 0.08), border: `2.5px solid ${cols[i]}`, borderRadius: 18, padding: "22px 26px", opacity: p(at, at + 0.08), transform: `translateY(${(1 - p(at, at + 0.08)) * 20}px)` }}>
            <div style={{ fontFamily: MONO, fontSize: 20, color: cols[i], letterSpacing: 3 }}>{labs[i]}</div>
            <div style={{ fontFamily: SANS, fontSize: 28, color: T.text, marginTop: 14, lineHeight: 1.34 }}>{it}</div>
          </div>
        );
      })}
      {/* the retrieval challenge — the video ENDS on this */}
      <div style={{ position: "absolute", left: 160, top: 520, width: 1600, background: mix(T.panel, A.vio, 0.1), border: `2.5px solid ${A.vio}`, borderRadius: 20, padding: "26px 34px", opacity: p(0.4, 0.55), boxShadow: `0 0 ${26 + Math.sin(frame * 0.05) * 14}px ${mix(T.bg0, A.vio, 0.35)}` }}>
        <div style={{ display: "flex", alignItems: "center", gap: 14 }}>
          <Chip text="PAUSE & PREDICT" color={A.vio} big />
          <span style={{ fontFamily: MONO, fontSize: 21, color: T.muted }}>before the next episode</span>
        </div>
        <div style={{ fontFamily: SANS, fontSize: 31, color: T.text, marginTop: 18, lineHeight: 1.4 }}>{challenge}</div>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontStyle: "italic", fontSize: 34, color: A.vio, marginTop: 16, opacity: p(0.62, 0.76) }}>{question}</div>
      </div>
    </Stage>
  );
};

// =====================================================================================
const ACCENT: Record<string, string> = {
  dp_title: A.vio, dp_scenario: A.fix, dp_code: A.vio, dp_pain: A.pain, dp_insight: A.vio,
  dp_analogy: A.var, dp_refactor: A.pat, dp_try: A.var, dp_payoff: A.pat, dp_reveal: A.vio,
  dp_map: A.vio, dp_tradeoffs: A.pain, dp_recap: A.vio,
};

export const DPScene: React.FC<{ variant: string; [key: string]: unknown }> = ({ variant, ...rest }) => {
  let content: React.ReactNode;
  switch (variant) {
    case "dp_title": content = <TitleScene {...(rest as any)} />; break;
    case "dp_scenario": content = <ScenarioScene {...(rest as any)} />; break;
    case "dp_code": content = <CodeScene {...(rest as any)} />; break;
    case "dp_pain": content = <PainScene {...(rest as any)} />; break;
    case "dp_insight": content = <InsightScene {...(rest as any)} />; break;
    case "dp_analogy": content = <AnalogyScene {...(rest as any)} />; break;
    case "dp_refactor": content = <RefactorScene {...(rest as any)} />; break;
    case "dp_try": content = <TryScene {...(rest as any)} />; break;
    case "dp_payoff": content = <PayoffScene {...(rest as any)} />; break;
    case "dp_reveal": content = <RevealScene {...(rest as any)} />; break;
    case "dp_map": content = <MapScene {...(rest as any)} />; break;
    case "dp_tradeoffs": content = <TradeoffScene {...(rest as any)} />; break;
    case "dp_recap": content = <RecapScene {...(rest as any)} />; break;
    default: content = <TitleScene {...(rest as any)} />;
  }
  const accent = ACCENT[variant] || A.vio;
  return (
    <AbsoluteFill>
      <Bg theme={T} accent={accent} />
      {content}
      <SceneProgress dur={(rest as any).dur} color={accent} />
    </AbsoluteFill>
  );
};

export default DPScene;
