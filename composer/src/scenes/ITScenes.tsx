/**
 * ITScenes.tsx — "Information Theory From Scratch" scene set.
 *
 * Identity (skills/04):
 *   theme accent = cyan (bits / signal)
 *   semantic colors: BIT=cyan · SURP=amber(surprise/probability) ·
 *   ENT=violet(entropy/uncertainty) · CODE=green(codes/compression) ·
 *   NOISE=pink(noise/error) · BAD=red
 *   motif: a stream of 0/1 bits flowing through a (noisy) channel.
 *
 * Every scene takes `dur` and phases with useP(dur); continuous motion in every
 * frame (bit streams, Flow, dash-march Wires, scan beams, sine glow). Numeric
 * things are COMPUTED at module scope (entropy curves, Huffman tree, letter
 * entropy, channel capacity, Hamming parity) and indexed by phase — see skills/03,04.
 */
import React from "react";
import { AbsoluteFill, interpolate, useCurrentFrame } from "remotion";
import {
  makeTheme, mix, useP as usePfull, usePop, rnd, MONO, SANS, Theme,
  Bg, Stage, Kicker, Head, Card, Flow, Wire, Counter, Type, Brackets, ScanBeam,
} from "../lib/primitives";

// A/V-SYNC FIX (feedback 2026-07-27): the narration introduces on-screen elements
// EARLY (front-loaded) then elaborates, but reveals spread evenly over a long beat
// trailed the audio by 10–30s. `useP` here compresses reveals into the front
// REVEAL_SPAN of the beat so a visual lands ~when it is spoken; the progress bar and
// continuous motion still run the FULL beat (SceneProgress uses usePfull), so no
// frozen tail. Scenes whose narration tracks a continuous animation (entropy sweep,
// bit-halving, huffman build, letters, redundancy, roadmap, apps, recap, title) opt
// out by calling usePfull directly. See skills/02 §"Narration ↔ scene contract".
const REVEAL_SPAN = 0.62;
const useP = (dur?: unknown) => {
  const p = usePfull(dur);
  return (a: number, b: number) => p(Math.min(1, a * REVEAL_SPAN), Math.min(1, b * REVEAL_SPAN));
};

// Local Foot override: captions are ON for this series and occupy the bottom band,
// so the takeaway strip sits higher (y=856, centered) to clear the caption pill
// (see skills/05 + skills/11 — captions collide with the default Foot at y924).
const Foot: React.FC<{ theme: Theme; p: number; children: React.ReactNode }> = ({ theme, p, children }) => (
  <div style={{
    position: "absolute", left: 100, top: 856, right: 100, fontFamily: MONO, fontSize: 22,
    color: theme.muted, opacity: p, lineHeight: 1.35, transform: `translateY(${(1 - p) * 12}px)`, textAlign: "center",
  }}>{children}</div>
);

// ---------------------------------------------------------------- identity
const T = makeTheme({ accent: "#22D3EE", bg0: "#04060C", bg1: "#080C16", bg2: "#0F1526", panel: "#141A2C" });
const A = {
  bit: "#22D3EE", surp: "#FBBF24", ent: "#A78BFA", code: "#34D399", noise: "#F472B6", bad: "#F87171", ok: "#34D399",
};

// ---------------------------------------------------------------- math (computed once)
const L2 = (x: number) => Math.log(x) / Math.LN2;
const Hbin = (p: number) => (p <= 0 || p >= 1 ? 0 : -p * L2(p) - (1 - p) * L2(1 - p));
const fmt = (x: number, d = 2) => x.toFixed(d);

// binary-entropy curve H(p), 0..1 → 0..1 bit
const ENT_CURVE = Array.from({ length: 101 }, (_, i) => { const p = i / 100; return { p, h: Hbin(p) }; });
// channel capacity of a binary symmetric channel: C = 1 - H(p).
// Only the crossover range p ∈ [0, 0.5] is meaningful, so C falls monotonically 1→0.
const CAP_CURVE = Array.from({ length: 51 }, (_, i) => { const p = i / 100; return { p, c: 1 - Hbin(p) }; });

// English letter frequencies (%), for a REAL entropy computation
const LETTER_FREQ: [string, number][] = [
  ["E", 12.7], ["T", 9.1], ["A", 8.2], ["O", 7.5], ["I", 7.0], ["N", 6.7], ["S", 6.3], ["H", 6.1],
  ["R", 6.0], ["D", 4.3], ["L", 4.0], ["C", 2.8], ["U", 2.8], ["M", 2.4], ["W", 2.4], ["F", 2.2],
  ["G", 2.0], ["Y", 2.0], ["P", 1.9], ["B", 1.5], ["V", 1.0], ["K", 0.8], ["J", 0.15], ["X", 0.15],
  ["Q", 0.10], ["Z", 0.07],
];
const LETTER_H = (() => {
  const tot = LETTER_FREQ.reduce((s, [, f]) => s + f, 0);
  return LETTER_FREQ.reduce((s, [, f]) => { const p = f / tot; return s - p * L2(p); }, 0);
})(); // ≈ 4.18 bits

// ---- Huffman tree over a 6-symbol source (computed at module scope) ----
interface HNode { sym?: string; f: number; l?: HNode; r?: HNode; id: number; x?: number; depth?: number; }
const HUFF_SRC: { s: string; f: number }[] = [
  { s: "E", f: 0.35 }, { s: "T", f: 0.20 }, { s: "A", f: 0.15 }, { s: "O", f: 0.12 }, { s: "I", f: 0.10 }, { s: "N", f: 0.08 },
];
const HUFF = (() => {
  let idc = 0;
  let pq: HNode[] = HUFF_SRC.map((d) => ({ sym: d.s, f: d.f, id: idc++ }));
  const order: HNode[] = [];
  while (pq.length > 1) {
    pq.sort((a, b) => a.f - b.f || a.id - b.id);
    const l = pq.shift()!, r = pq.shift()!;
    const n: HNode = { f: +(l.f + r.f).toFixed(4), l, r, id: idc++ };
    order.push(n); pq.push(n);
  }
  const root = pq[0];
  const codes: Record<string, string> = {};
  (function walk(n: HNode, code: string) {
    if (n.sym !== undefined) { codes[n.sym] = code || "0"; return; }
    walk(n.l!, code + "0"); walk(n.r!, code + "1");
  })(root, "");
  // layout: leaves left→right, internal x = mean of children, y = depth
  let leaf = 0; const nodes: HNode[] = []; const edges: { from: HNode; to: HNode; bit: string }[] = [];
  (function lay(n: HNode, depth: number): number {
    n.depth = depth;
    if (n.sym !== undefined) { n.x = leaf++; nodes.push(n); return n.x; }
    const lx = lay(n.l!, depth + 1), rx = lay(n.r!, depth + 1);
    n.x = (lx + rx) / 2; nodes.push(n);
    edges.push({ from: n, to: n.l!, bit: "0" }); edges.push({ from: n, to: n.r!, bit: "1" });
    return n.x;
  })(root, 0);
  const maxLeaf = leaf - 1;
  const maxDepth = Math.max(...nodes.map((n) => n.depth!));
  const avgLen = HUFF_SRC.reduce((s, d) => s + d.f * codes[d.s].length, 0);
  const entropy = HUFF_SRC.reduce((s, d) => s - d.f * L2(d.f), 0);
  return { root, codes, nodes, edges, maxLeaf, maxDepth, avgLen, entropy };
})();

// ---------------------------------------------------------------- ambient: bit stream
const BitStream: React.FC<{ y: number; color?: string; o?: number; speed?: number; n?: number; seed?: number }> = ({
  y, color = A.bit, o = 0.5, speed = 2.4, n = 26, seed = 0,
}) => {
  const frame = useCurrentFrame();
  return (
    <>
      {Array.from({ length: n }).map((_, i) => {
        const x = ((i * 74 + frame * speed) % (1920 + 80)) - 40;
        const b = rnd(i, Math.floor((frame * speed + i * 74) / (1920 + 80)) + seed) > 0.5 ? "1" : "0";
        const fade = Math.sin((x / 1920) * Math.PI);
        return (
          <span key={i} style={{
            position: "absolute", left: x, top: y, fontFamily: MONO, fontWeight: 700, fontSize: 30,
            color, opacity: o * Math.max(0, fade), textShadow: `0 0 12px ${color}`,
          }}>{b}</span>
        );
      })}
    </>
  );
};

// small reusable stat pill
const Pill: React.FC<{ label: string; value: string; color: string; o?: number }> = ({ label, value, color, o = 1 }) => (
  <div style={{ display: "inline-flex", alignItems: "baseline", gap: 12, opacity: o }}>
    <span style={{ fontFamily: MONO, fontSize: 22, color: T.muted }}>{label}</span>
    <span style={{ fontFamily: MONO, fontWeight: 800, fontSize: 30, color }}>{value}</span>
  </div>
);

// =====================================================================================
// it_title
const TitleScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const p = usePfull(dur);   // narration-tracked: keep full-beat timing
  const pop = usePop(dur);
  return (
    <AbsoluteFill style={{ alignItems: "center", justifyContent: "center" }}>
      <BitStream y={150} color={A.bit} o={0.35} speed={1.8} seed={1} />
      <BitStream y={880} color={A.ent} o={0.3} speed={-1.4} seed={7} />
      {/* orbiting bits */}
      {Array.from({ length: 12 }).map((_, i) => {
        const ang = frame * 0.01 + (i / 12) * Math.PI * 2;
        return (
          <span key={i} style={{
            position: "absolute", left: 960 + Math.cos(ang) * (560 + i * 10) - 6,
            top: 540 + Math.sin(ang) * (250 + i * 6) - 12, fontFamily: MONO, fontWeight: 700, fontSize: 22,
            color: i % 2 ? A.bit : A.surp, opacity: 0.25 + rnd(i, 3) * 0.3, textShadow: `0 0 10px ${A.bit}`,
          }}>{i % 2 ? "1" : "0"}</span>
        );
      })}
      <div style={{ textAlign: "center", transform: `scale(${0.92 + pop(0) * 0.08})` }}>
        <div style={{ display: "flex", justifyContent: "center", marginBottom: 26 }}>
          <Kicker theme={T} text="SURPRISE → BITS · FULL COURSE" cx />
        </div>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 118, lineHeight: 1.0, letterSpacing: -3, color: T.text }}>
          <div>Information</div>
          <div style={{ color: A.bit, textShadow: `0 0 70px ${mix(T.bg0, A.bit, 0.7)}` }}>Theory</div>
        </div>
        <div style={{ height: 5, width: interpolate(p(0.18, 0.45), [0, 1], [0, 540]), background: `linear-gradient(90deg, ${A.bit}, ${A.ent})`, borderRadius: 3, margin: "30px auto" }} />
        <div style={{ fontFamily: SANS, fontSize: 37, color: T.muted, opacity: p(0.28, 0.5) }}>
          surprise · entropy · compression · channels · the limits of communication
        </div>
      </div>
    </AbsoluteFill>
  );
};

// it_hook — which message carries more information?
const HookScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const msgs = [
    { at: 0.12, x: 150, head: "“The sun rose today.”", note: "almost certain", bits: 0.0, c: A.surp, low: true },
    { at: 0.42, x: 1010, head: "“It snowed in the desert.”", note: "very unlikely", bits: 9.0, c: A.bit, low: false },
  ];
  return (
    <Stage>
      <Head theme={T} kicker="THE CENTRAL QUESTION" title="Which message tells you more?" o={p(0, 0.06)} />
      {msgs.map((m, i) => (
        <Card key={i} theme={T} x={m.x} y={250} w={760} h={330} color={m.c} o={p(m.at, m.at + 0.1)} glow>
          <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 44, color: T.text, lineHeight: 1.15 }}>{m.head}</div>
          <div style={{ fontFamily: MONO, fontSize: 26, color: m.c, marginTop: 22 }}>{m.note}</div>
          <div style={{ position: "absolute", left: 32, bottom: 28, display: "flex", alignItems: "center", gap: 14, opacity: p(m.at + 0.12, m.at + 0.2) }}>
            <span style={{ fontFamily: MONO, fontSize: 24, color: T.muted }}>information ≈</span>
            <Counter p={p(m.at + 0.12, m.at + 0.26)} to={m.bits} color={m.c} size={46} decimals={m.low ? 1 : 0} suffix=" bits" />
          </div>
          <BitStream y={0} color={m.c} o={m.low ? 0.12 : 0.45} n={8} speed={m.low ? 0.6 : 3.2} seed={i * 5} />
        </Card>
      ))}
      <div style={{ position: "absolute", left: 0, right: 0, top: 660, textAlign: "center", opacity: p(0.66, 0.78) }}>
        <span style={{ fontFamily: SANS, fontWeight: 800, fontSize: 40, color: T.text }}>
          Information is not about <span style={{ color: T.muted }}>meaning</span> — it is about{" "}
          <span style={{ color: A.surp, textShadow: `0 0 26px ${mix(T.bg0, A.surp, 0.6)}` }}>surprise</span>.
        </span>
      </div>
      <Foot theme={T} p={p(0.84, 0.93)}>
        Claude Shannon, 1948: the more unlikely a message, the more information it carries.
      </Foot>
    </Stage>
  );
};

// it_divider — parameterized part divider
const Divider: React.FC<{ dur?: number; n?: number; title?: string; sub?: string; color?: string }> = ({
  dur, n = 1, title = "", sub = "", color = A.bit,
}) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  return (
    <Stage>
      <BitStream y={210} color={color} o={0.28} speed={1.6} seed={n} />
      <BitStream y={820} color={color} o={0.22} speed={-1.2} seed={n + 4} />
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
          <div key={i} style={{
            width: i === n ? 44 : 14, height: 14, borderRadius: 8,
            background: i <= n ? color : mix(T.panel, color, 0.15), border: `1.5px solid ${i <= n ? color : T.line}`,
            opacity: i === n ? 0.7 + Math.sin(frame * 0.1) * 0.3 : 1,
          }} />
        ))}
      </div>
    </Stage>
  );
};

// it_surprise — probability → surprise (bits), computed I = log2(1/p)
const SurpriseScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur);
    // tight stagger: the narration fires all four events in the first ~30% (extreme
    // front-load), so keep the reveals close together (compressed further by REVEAL_SPAN)
  const events = [
    { at: 0.08, label: "A coin lands heads", frac: "1 / 2", pr: 0.5 },
    { at: 0.20, label: "A die rolls a six", frac: "1 / 6", pr: 1 / 6 },
    { at: 0.32, label: "Snake eyes on two dice", frac: "1 / 36", pr: 1 / 36 },
    { at: 0.44, label: "The ace of spades, first draw", frac: "1 / 52", pr: 1 / 52 },
  ];
  const maxBits = L2(1 / (1 / 52));
  return (
    <Stage>
      <Head theme={T} kicker="SELF-INFORMATION" title="Rarer events carry more bits" color={A.surp} o={p(0, 0.06)} />
      {events.map((e, i) => {
        const bits = L2(1 / e.pr);
        const grow = p(e.at, e.at + 0.12);
        const w = (bits / maxBits) * 900 * grow;
        const y = 250 + i * 130;
        return (
          <React.Fragment key={i}>
            <div style={{ position: "absolute", left: 100, top: y, width: 470, fontFamily: SANS, fontWeight: 700, fontSize: 30, color: T.text, opacity: p(e.at, e.at + 0.06) }}>{e.label}</div>
            <div style={{ position: "absolute", left: 590, top: y - 4, fontFamily: MONO, fontSize: 26, color: T.muted, opacity: p(e.at + 0.02, e.at + 0.08) }}>p = {e.frac}</div>
            <div style={{ position: "absolute", left: 790, top: y - 6, width: w, height: 48, borderRadius: "8px 16px 16px 8px", background: `linear-gradient(90deg, ${mix(A.surp, T.bg1, 0.5)}, ${A.surp})`, border: `2px solid ${A.surp}`, boxShadow: `0 0 20px ${mix(T.bg0, A.surp, 0.35)}` }} />
            <div style={{ position: "absolute", left: 790 + w + 16, top: y, fontFamily: MONO, fontWeight: 800, fontSize: 30, color: A.surp, opacity: grow }}>{fmt(bits, 1)} bits</div>
          </React.Fragment>
        );
      })}
      <div style={{ position: "absolute", left: 100, top: 800, display: "flex", alignItems: "center", gap: 22, opacity: p(0.74, 0.84) }}>
        <span style={{ fontFamily: MONO, fontSize: 30, color: T.muted }}>surprise</span>
        <span style={{ fontFamily: MONO, fontWeight: 800, fontSize: 40, color: A.bit }}>I(x) = log₂(1 / p)</span>
      </div>
      <Foot theme={T} p={p(0.86, 0.94)}>
        Halve the probability, and you add exactly one bit of surprise.
      </Foot>
    </Stage>
  );
};

// it_selfinfo — why the logarithm? additivity of independent events
const SelfInfoScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur);
  return (
    <Stage>
      <Head theme={T} kicker="WHY A LOGARITHM" title="Independent surprises should add up" color={A.bit} o={p(0, 0.06)} />
      {/* two independent coin flips */}
      <Card theme={T} x={150} y={250} w={520} h={230} color={A.surp} o={p(0.1, 0.18)}>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 34, color: T.text }}>Flip 1: heads</div>
        <div style={{ fontFamily: MONO, fontSize: 24, color: T.muted, marginTop: 14 }}>p = 1/2</div>
        <div style={{ fontFamily: MONO, fontWeight: 800, fontSize: 34, color: A.surp, marginTop: 14 }}>1 bit</div>
      </Card>
      <Card theme={T} x={700} y={250} w={520} h={230} color={A.surp} o={p(0.24, 0.32)}>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 34, color: T.text }}>Flip 2: heads</div>
        <div style={{ fontFamily: MONO, fontSize: 24, color: T.muted, marginTop: 14 }}>p = 1/2</div>
        <div style={{ fontFamily: MONO, fontWeight: 800, fontSize: 34, color: A.surp, marginTop: 14 }}>1 bit</div>
      </Card>
      <div style={{ position: "absolute", left: 1250, top: 330, fontFamily: SANS, fontWeight: 800, fontSize: 70, color: T.muted, opacity: p(0.34, 0.42) }}>+</div>
      <Wire x1={410} y1={480} x2={700} y2={620} p={p(0.4, 0.5)} color={A.bit} curve={40} />
      <Wire x1={960} y1={480} x2={700} y2={620} p={p(0.4, 0.5)} color={A.bit} curve={40} />
      <Card theme={T} x={410} y={620} w={600} h={230} color={A.bit} o={p(0.5, 0.6)} glow>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 34, color: T.text }}>Both heads together</div>
        <div style={{ fontFamily: MONO, fontSize: 24, color: T.muted, marginTop: 14 }}>p = 1/2 × 1/2 = 1/4</div>
        <div style={{ fontFamily: MONO, fontWeight: 800, fontSize: 34, color: A.bit, marginTop: 14 }}>log₂(4) = 2 bits</div>
      </Card>
      <Flow x1={410} y1={480} x2={700} y2={620} color={A.bit} n={5} o={p(0.52, 0.6)} curve={40} />
      <Flow x1={960} y1={480} x2={700} y2={620} color={A.bit} n={5} o={p(0.52, 0.6)} curve={40} />
      <div style={{ position: "absolute", left: 1120, top: 690, width: 700, opacity: p(0.66, 0.78) }}>
        <div style={{ fontFamily: SANS, fontWeight: 700, fontSize: 30, color: T.text, lineHeight: 1.4 }}>
          Probabilities <span style={{ color: A.surp }}>multiply</span>. The logarithm turns that into{" "}
          <span style={{ color: A.bit }}>addition</span> — so bits simply stack.
        </div>
      </div>
      <Foot theme={T} p={p(0.86, 0.94)}>
        That single requirement — surprises add — forces the measure to be a logarithm.
      </Foot>
    </Stage>
  );
};

// it_bit — twenty questions / halving the search space (computed)
const BitScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = usePfull(dur);   // narration-tracked halving — keep full-beat timing
  const total = 64;
  const step = Math.min(6, Math.floor(p(0.16, 0.82) * 7));
  const remaining = total >> step; // 64,32,16,8,4,2,1
  return (
    <Stage>
      <Head theme={T} kicker="THE UNIT" title="A bit halves the possibilities" color={A.bit} o={p(0, 0.06)} />
      {/* 8x8 grid of candidates, top `remaining` still lit */}
      <div style={{ position: "absolute", left: 150, top: 250, display: "grid", gridTemplateColumns: "repeat(8, 74px)", gap: 10 }}>
        {Array.from({ length: total }).map((_, i) => {
          const alive = i < remaining;
          return (
            <div key={i} style={{
              width: 74, height: 74, borderRadius: 12,
              background: alive ? mix(T.panel, A.bit, 0.5) : T.panel,
              border: `2px solid ${alive ? A.bit : T.line}`,
              opacity: alive ? 1 : 0.28, boxShadow: alive ? `0 0 14px ${mix(T.bg0, A.bit, 0.4)}` : "none",
              transition: "none",
            }} />
          );
        })}
      </div>
      <div style={{ position: "absolute", left: 830, top: 260, width: 400 }}>
        <div style={{ fontFamily: MONO, fontSize: 26, color: T.muted }}>questions asked</div>
        <div style={{ fontFamily: MONO, fontWeight: 800, fontSize: 92, color: A.bit }}>{step}</div>
        <div style={{ fontFamily: MONO, fontSize: 26, color: T.muted, marginTop: 24 }}>still possible</div>
        <div style={{ fontFamily: MONO, fontWeight: 800, fontSize: 92, color: A.surp }}>{remaining}</div>
        <div style={{ marginTop: 30, fontFamily: SANS, fontWeight: 700, fontSize: 30, color: T.text, lineHeight: 1.4, opacity: p(0.5, 0.6) }}>
          Each yes/no answer cuts the field in half. Six questions pin down one of sixty-four.
        </div>
        <div style={{ marginTop: 22, fontFamily: MONO, fontWeight: 800, fontSize: 34, color: A.code, opacity: p(0.7, 0.8) }}>
          log₂(64) = 6 bits
        </div>
      </div>
      <BitStream y={900} color={A.bit} o={0.3} speed={2.2} />
      <Foot theme={T} p={p(0.86, 0.94)}>
        One bit = one perfect yes/no question. It is the atom of information.
      </Foot>
    </Stage>
  );
};

// it_encode — fixed vs variable-length codes; average length
const ENC_SRC = [
  { s: "A", pr: 0.5, fixed: "00", vari: "0" },
  { s: "B", pr: 0.25, fixed: "01", vari: "10" },
  { s: "C", pr: 0.125, fixed: "10", vari: "110" },
  { s: "D", pr: 0.125, fixed: "11", vari: "111" },
];
const EncodeScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur);
  const avgFixed = 2;
  const avgVari = ENC_SRC.reduce((s, r) => s + r.pr * r.vari.length, 0); // 1.75
  const showVari = p(0.4, 0.42) > 0.5;
  return (
    <Stage>
      <Head theme={T} kicker="ENCODING" title="Spend fewer bits on common symbols" color={A.code} o={p(0, 0.06)} />
      {/* table */}
      <div style={{ position: "absolute", left: 150, top: 240, width: 1000 }}>
        <div style={{ display: "flex", fontFamily: MONO, fontSize: 24, color: T.muted, borderBottom: `2px solid ${T.line}`, paddingBottom: 10 }}>
          <div style={{ width: 180 }}>symbol</div><div style={{ width: 200 }}>probability</div>
          <div style={{ width: 260 }}>fixed code</div><div style={{ width: 260 }}>variable code</div>
        </div>
        {ENC_SRC.map((r, i) => {
          const at = 0.12 + i * 0.07;
          return (
            <div key={i} style={{ display: "flex", alignItems: "center", height: 76, opacity: p(at, at + 0.06), borderBottom: `1px solid ${T.line}` }}>
              <div style={{ width: 180, fontFamily: SANS, fontWeight: 800, fontSize: 40, color: A.bit }}>{r.s}</div>
              <div style={{ width: 200, fontFamily: MONO, fontSize: 30, color: T.text }}>{r.pr}</div>
              <div style={{ width: 260, fontFamily: MONO, fontWeight: 700, fontSize: 32, color: T.muted }}>{r.fixed}</div>
              <div style={{ width: 260, fontFamily: MONO, fontWeight: 800, fontSize: 32, color: showVari ? A.code : "transparent" }}>{r.vari}</div>
            </div>
          );
        })}
      </div>
      {/* averages */}
      <Card theme={T} x={1220} y={300} w={560} h={360} color={A.code} o={p(0.6, 0.7)} glow>
        <div style={{ fontFamily: MONO, fontSize: 24, color: T.muted }}>average bits per symbol</div>
        <div style={{ display: "flex", alignItems: "baseline", gap: 18, marginTop: 18 }}>
          <span style={{ fontFamily: SANS, fontSize: 26, color: T.muted }}>fixed</span>
          <span style={{ fontFamily: MONO, fontWeight: 800, fontSize: 48, color: T.muted }}>{fmt(avgFixed, 2)}</span>
        </div>
        <div style={{ display: "flex", alignItems: "baseline", gap: 18, marginTop: 8 }}>
          <span style={{ fontFamily: SANS, fontSize: 26, color: A.code }}>variable</span>
          <Counter p={p(0.66, 0.8)} to={avgVari} decimals={2} color={A.code} size={48} />
        </div>
        <div style={{ marginTop: 26, fontFamily: SANS, fontWeight: 700, fontSize: 26, color: T.text, lineHeight: 1.35, opacity: p(0.78, 0.88) }}>
          A 12% shorter message — with no loss at all.
        </div>
      </Card>
      <BitStream y={900} color={A.code} o={0.3} speed={2.4} />
      <Foot theme={T} p={p(0.88, 0.95)}>
        But how short can we possibly go? That limit has a name: entropy.
      </Foot>
    </Stage>
  );
};

// it_entropy — binary entropy gauge H(p) curve, live dot
const EntropyScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const p = usePfull(dur);   // narration-tracked dot sweep — keep full-beat timing
  const X0 = 220, Y0 = 780, W = 900, H = 520;
  const cur = p(0.2, 0.85); // sweep probability 0→1
  const dotP = cur;
  const dotH = Hbin(dotP);
  const cp = p(0.14, 0.6);
  const pts = ENT_CURVE.slice(0, Math.max(2, Math.round(101 * cp))).map(({ p: pp, h }) => `${X0 + pp * W},${Y0 - h * H}`).join(" ");
  const dx = X0 + dotP * W, dy = Y0 - dotH * H;
  return (
    <Stage>
      <Head theme={T} kicker="ENTROPY" title="Average surprise of a coin" color={A.ent} o={p(0, 0.06)} />
      <svg style={{ position: "absolute", left: 0, top: 0, overflow: "visible" }} width={1920} height={1080}>
        {/* axes */}
        <line x1={X0} y1={Y0} x2={X0 + W} y2={Y0} stroke={T.line} strokeWidth={2} />
        <line x1={X0} y1={Y0} x2={X0} y2={Y0 - H - 10} stroke={T.line} strokeWidth={2} />
        <polyline points={pts} fill="none" stroke={A.ent} strokeWidth={5} />
        {cp > 0.99 && <circle cx={dx} cy={dy} r={11} fill={A.ent} stroke={T.text} strokeWidth={2} />}
        <line x1={dx} y1={Y0} x2={dx} y2={dy} stroke={mix(A.ent, T.bg1, 0.4)} strokeWidth={2} strokeDasharray="5 7" opacity={cp > 0.99 ? 1 : 0} />
      </svg>
      {/* axis labels */}
      <div style={{ position: "absolute", left: X0 - 10, top: Y0 + 16, fontFamily: MONO, fontSize: 22, color: T.muted }}>p = 0 (always tails)</div>
      <div style={{ position: "absolute", left: X0 + W - 190, top: Y0 + 16, fontFamily: MONO, fontSize: 22, color: T.muted }}>p = 1 (always heads)</div>
      <div style={{ position: "absolute", left: X0 + W / 2 - 90, top: Y0 - H - 66, fontFamily: MONO, fontSize: 24, color: A.ent, opacity: p(0.55, 0.65) }}>max = 1 bit at p = ½</div>
      {/* live readout */}
      <div style={{ position: "absolute", left: 1280, top: 300, width: 520 }}>
        <Pill label="p(heads) =" value={fmt(dotP, 2)} color={A.surp} o={p(0.24, 0.3)} />
        <div style={{ height: 18 }} />
        <Pill label="H(p)     =" value={`${fmt(dotH, 2)} bits`} color={A.ent} o={p(0.24, 0.3)} />
        <div style={{ marginTop: 34, fontFamily: SANS, fontWeight: 700, fontSize: 30, color: T.text, lineHeight: 1.4, opacity: p(0.6, 0.72) }}>
          A fair coin is <span style={{ color: A.ent }}>hardest</span> to predict — one full bit per flip.
          A biased coin is easier, so it carries less.
        </div>
        <div style={{ marginTop: 22, fontFamily: MONO, fontWeight: 800, fontSize: 30, color: A.bit, opacity: p(0.72, 0.82), textShadow: `0 0 ${16 + Math.sin(frame * 0.07) * 8}px ${mix(T.bg0, A.bit, 0.5)}` }}>
          entropy = expected surprise
        </div>
      </div>
      <Foot theme={T} p={p(0.87, 0.95)}>
        Entropy measures how uncertain a source is — before you look.
      </Foot>
    </Stage>
  );
};

// it_entropyformula — worked example: weather
const WEATHER = [
  { s: "sunny", pr: 0.5, c: A.surp }, { s: "cloudy", pr: 0.25, c: A.bit }, { s: "rainy", pr: 0.25, c: A.ent },
];
const EntropyFormulaScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur);
  const H = WEATHER.reduce((s, w) => s - w.pr * L2(w.pr), 0); // 1.5
  return (
    <Stage>
      <Head theme={T} kicker="THE FORMULA" title="H = − Σ p · log₂ p" color={A.ent} o={p(0, 0.06)} />
      <div style={{ position: "absolute", left: 100, right: 100, top: 210, textAlign: "center", fontFamily: MONO, fontSize: 30, color: T.muted, opacity: p(0.06, 0.14) }}>
        weight each symbol's surprise by how often it happens, then add up
      </div>
      {WEATHER.map((w, i) => {
        const at = 0.16 + i * 0.12;
        const term = -w.pr * L2(w.pr);
        const y = 300 + i * 150;
        return (
          <React.Fragment key={i}>
            <div style={{ position: "absolute", left: 140, top: y, width: 260, fontFamily: SANS, fontWeight: 800, fontSize: 40, color: w.c, opacity: p(at, at + 0.06) }}>{w.s}</div>
            <div style={{ position: "absolute", left: 430, top: y + 4, fontFamily: MONO, fontSize: 30, color: T.text, opacity: p(at + 0.02, at + 0.08) }}>
              p = {w.pr}
            </div>
            <div style={{ position: "absolute", left: 690, top: y + 4, fontFamily: MONO, fontSize: 30, color: T.muted, opacity: p(at + 0.04, at + 0.1) }}>
              surprise = {fmt(L2(1 / w.pr), 0)} bits
            </div>
            <div style={{ position: "absolute", left: 1140, top: y + 4, fontFamily: MONO, fontWeight: 800, fontSize: 30, color: w.c, opacity: p(at + 0.06, at + 0.12) }}>
              → {fmt(term, 2)} bits
            </div>
          </React.Fragment>
        );
      })}
      <div style={{ position: "absolute", left: 140, top: 760, right: 140, height: 3, background: T.line, opacity: p(0.6, 0.66) }} />
      <div style={{ position: "absolute", left: 140, top: 790, display: "flex", alignItems: "baseline", gap: 24, opacity: p(0.66, 0.78) }}>
        <span style={{ fontFamily: SANS, fontWeight: 800, fontSize: 40, color: T.text }}>Entropy of the weather =</span>
        <Counter p={p(0.7, 0.84)} to={H} decimals={1} color={A.ent} size={56} suffix=" bits / day" />
      </div>
      <BitStream y={905} color={A.ent} o={0.28} speed={2} />
      <Foot theme={T} p={p(0.88, 0.95)}>
        On average, 1.5 yes/no questions are enough to learn each day's weather.
      </Foot>
    </Stage>
  );
};

// it_maxent — uniform distribution maximizes entropy; compare sources
const MAXENT = [
  { label: "Loaded coin", sub: "p = 0.9 / 0.1", h: Hbin(0.9), max: 1, c: A.surp },
  { label: "Fair coin", sub: "p = 0.5 / 0.5", h: 1, max: 1, c: A.bit },
  { label: "Fair die", sub: "6 equal faces", h: L2(6), max: L2(6), c: A.ent },
];
const MaxEntScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const SCALE = 150; // px per bit
  return (
    <Stage>
      <Head theme={T} kicker="MAXIMUM ENTROPY" title="Uncertainty peaks when all outcomes are equal" color={A.ent} o={p(0, 0.06)} />
      {MAXENT.map((m, i) => {
        const at = 0.14 + i * 0.16;
        const grow = p(at, at + 0.14);
        const h = m.h * SCALE * grow;
        const x = 260 + i * 480;
        const atMax = Math.abs(m.h - m.max) < 1e-6;
        return (
          <React.Fragment key={i}>
            <div style={{ position: "absolute", left: x - 40, top: 760 - h - 56, width: 300, textAlign: "center", fontFamily: MONO, fontWeight: 800, fontSize: 34, color: m.c, opacity: grow }}>
              {fmt(m.h, 2)} bits
            </div>
            <div style={{
              position: "absolute", left: x, top: 760 - h, width: 220, height: h, borderRadius: "14px 14px 0 0",
              background: `linear-gradient(180deg, ${m.c}, ${mix(m.c, T.bg1, 0.5)})`, border: `2.5px solid ${m.c}`, borderBottom: "none",
              boxShadow: atMax ? `0 0 ${26 + Math.sin(frame * 0.08) * 10}px ${mix(T.bg0, m.c, 0.4)}` : "none",
            }} />
            <div style={{ position: "absolute", left: x - 40, top: 776, width: 300, textAlign: "center", fontFamily: SANS, fontWeight: 800, fontSize: 32, color: T.text, opacity: p(at, at + 0.08) }}>{m.label}</div>
            <div style={{ position: "absolute", left: x - 40, top: 820, width: 300, textAlign: "center", fontFamily: MONO, fontSize: 24, color: T.muted, opacity: p(at + 0.04, at + 0.1) }}>{m.sub}</div>
          </React.Fragment>
        );
      })}
      <div style={{ position: "absolute", left: 1240, top: 300, width: 560, opacity: p(0.66, 0.78) }}>
        <div style={{ fontFamily: SANS, fontWeight: 700, fontSize: 32, color: T.text, lineHeight: 1.45 }}>
          Bias always <span style={{ color: A.surp }}>lowers</span> entropy — a predictable source is a
          poorer source. More equally-likely options mean more uncertainty, and more bits.
        </div>
      </div>
      <Foot theme={T} p={p(0.88, 0.95)}>
        For n equally likely outcomes, entropy is exactly log₂ n.
      </Foot>
    </Stage>
  );
};

// it_letters — real entropy of English letters (computed)
const LettersScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const p = usePfull(dur);   // narration-tracked — keep full-beat timing
  const maxF = LETTER_FREQ[0][1];
  const hot = Math.floor(frame / 10) % LETTER_FREQ.length;
  return (
    <Stage>
      <Head theme={T} kicker="A REAL SOURCE" title="How much information is in a letter?" color={A.bit} o={p(0, 0.06)} />
      {/* frequency bars, 26 letters across */}
      {LETTER_FREQ.map(([ch, f], i) => {
        const at = 0.1 + i * 0.014;
        const grow = p(at, at + 0.1);
        const h = (f / maxF) * 340 * grow;
        const x = 130 + i * 63;
        const on = hot === i;
        return (
          <React.Fragment key={i}>
            <div style={{
              position: "absolute", left: x, top: 680 - h, width: 46, height: h, borderRadius: "6px 6px 0 0",
              background: on ? A.surp : `linear-gradient(180deg, ${A.bit}, ${mix(A.bit, T.bg1, 0.55)})`,
              border: `2px solid ${on ? A.surp : A.bit}`, borderBottom: "none",
            }} />
            <div style={{ position: "absolute", left: x, top: 690, width: 46, textAlign: "center", fontFamily: MONO, fontWeight: 700, fontSize: 24, color: on ? A.surp : T.muted, opacity: p(at, at + 0.06) }}>{ch}</div>
          </React.Fragment>
        );
      })}
      <Card theme={T} x={1250} y={220} w={560} h={230} color={A.ent} o={p(0.6, 0.7)} glow>
        <div style={{ fontFamily: MONO, fontSize: 24, color: T.muted }}>entropy of English text</div>
        <Counter p={p(0.64, 0.8)} to={LETTER_H} decimals={2} color={A.ent} size={64} suffix=" bits/letter" />
        <div style={{ fontFamily: MONO, fontSize: 24, color: T.muted, marginTop: 14 }}>vs 26 equal letters: {fmt(L2(26), 2)} bits</div>
      </Card>
      <div style={{ position: "absolute", left: 1250, top: 480, width: 560, fontFamily: SANS, fontWeight: 700, fontSize: 30, color: T.text, lineHeight: 1.4, opacity: p(0.74, 0.86) }}>
        Because some letters are far more common, real text is more predictable — so each letter
        carries about <span style={{ color: A.ent }}>4.2 bits</span>, not 4.7.
      </div>
      <Foot theme={T} p={p(0.88, 0.95)}>
        That gap between actual and maximum entropy is exactly what compression exploits.
      </Foot>
    </Stage>
  );
};

// it_sourcecoding — Shannon's source coding theorem: entropy is the floor
const SourceCodingScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const X0 = 200, Y0 = 760, W = 1100;
  const floorX = X0 + 0.42 * W; // entropy floor position
  const barW = interpolate(p(0.2, 0.6), [0, 1], [W, 0.42 * W]); // compress down toward floor
  return (
    <Stage>
      <Head theme={T} kicker="SOURCE CODING THEOREM" title="Entropy is the compression floor" color={A.code} o={p(0, 0.06)} />
      {/* the message bar shrinking toward the entropy floor */}
      <div style={{ position: "absolute", left: X0, top: Y0 - 240, width: barW, height: 120, borderRadius: 16, background: `linear-gradient(90deg, ${A.code}, ${mix(A.code, T.bg1, 0.5)})`, border: `2.5px solid ${A.code}`, boxShadow: `0 0 24px ${mix(T.bg0, A.code, 0.3)}` }}>
        <BitStream y={44} color={T.bg0} o={0.5} n={12} speed={2.6} />
      </div>
      <div style={{ position: "absolute", left: X0, top: Y0 - 300, fontFamily: MONO, fontSize: 24, color: T.muted, opacity: p(0.24, 0.34) }}>your message, being squeezed…</div>
      {/* the floor line */}
      <div style={{ position: "absolute", left: floorX, top: Y0 - 340, width: 4, height: 380, background: A.bad, opacity: p(0.34, 0.44) }} />
      <div style={{ position: "absolute", left: floorX - 6, top: Y0 + 54, width: 320, fontFamily: MONO, fontWeight: 800, fontSize: 26, color: A.bad, opacity: p(0.4, 0.5) }}>
        the entropy wall
      </div>
      <div style={{ position: "absolute", left: floorX + 20, top: Y0 - 340, width: 520, fontFamily: SANS, fontWeight: 700, fontSize: 30, color: T.text, lineHeight: 1.4, opacity: p(0.56, 0.68), textShadow: Math.sin(frame * 0.06) > 0 ? `0 0 20px ${mix(T.bg0, A.bad, 0.3)}` : "none" }}>
        You cannot compress below <span style={{ color: A.bad }}>H bits</span> per symbol — not with any
        trick, ever — and still recover the message perfectly.
      </div>
      <div style={{ position: "absolute", left: 200, top: 300, width: 1500, textAlign: "left", fontFamily: MONO, fontSize: 30, color: A.code, opacity: p(0.12, 0.22) }}>
        best possible average length  ≥  entropy H
      </div>
      <Foot theme={T} p={p(0.88, 0.95)}>
        Shannon, 1948: entropy is not just a number — it is a hard, provable limit.
      </Foot>
    </Stage>
  );
};

// it_huffman — build the Huffman tree (computed) + code table
const HuffmanScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const p = usePfull(dur);   // narration-tracked tree build — keep full-beat timing
  const X0 = 150, W = 780, Y0 = 250, rowH = 108;
  const px = (n: HNode) => X0 + (n.x! / HUFF.maxLeaf) * W;
  const py = (n: HNode) => Y0 + (n.depth! / HUFF.maxDepth) * (HUFF.maxDepth * rowH);
  return (
    <Stage>
      <Head theme={T} kicker="HUFFMAN CODING" title="A real optimal code, built bottom-up" color={A.code} o={p(0, 0.06)} />
      {/* edges */}
      <svg style={{ position: "absolute", left: 0, top: 0, overflow: "visible" }} width={1920} height={1080}>
        {HUFF.edges.map((e, i) => {
          const at = 0.16 + (e.from.depth! / HUFF.maxDepth) * 0.42;
          const o = p(at, at + 0.08);
          return (
            <line key={i} x1={px(e.from)} y1={py(e.from)} x2={px(e.to)} y2={py(e.to)}
              stroke={e.bit === "0" ? A.bit : A.surp} strokeWidth={3} opacity={o} />
          );
        })}
        {HUFF.edges.map((e, i) => {
          const at = 0.16 + (e.from.depth! / HUFF.maxDepth) * 0.42;
          const mx = (px(e.from) + px(e.to)) / 2, my = (py(e.from) + py(e.to)) / 2;
          return (
            <text key={"t" + i} x={mx + (e.bit === "0" ? -16 : 8)} y={my} fill={e.bit === "0" ? A.bit : A.surp}
              fontFamily="monospace" fontSize={24} fontWeight={800} opacity={p(at + 0.04, at + 0.12)}>{e.bit}</text>
          );
        })}
      </svg>
      {/* nodes */}
      {HUFF.nodes.map((n, i) => {
        const at = 0.16 + (n.depth! / HUFF.maxDepth) * 0.42;
        const o = p(at, at + 0.08);
        const isLeaf = n.sym !== undefined;
        const cx = px(n), cy = py(n);
        return (
          <div key={i} style={{
            position: "absolute", left: cx - (isLeaf ? 34 : 26), top: cy - (isLeaf ? 34 : 26),
            width: isLeaf ? 68 : 52, height: isLeaf ? 68 : 52, borderRadius: isLeaf ? 14 : 30,
            background: isLeaf ? mix(T.panel, A.code, 0.3) : T.panel, border: `2.5px solid ${isLeaf ? A.code : T.muted}`,
            display: "flex", alignItems: "center", justifyContent: "center", opacity: o,
            boxShadow: isLeaf ? `0 0 16px ${mix(T.bg0, A.code, 0.3)}` : "none",
          }}>
            <span style={{ fontFamily: MONO, fontWeight: 800, fontSize: isLeaf ? 30 : 20, color: isLeaf ? A.code : T.muted }}>
              {isLeaf ? n.sym : n.f}
            </span>
          </div>
        );
      })}
      {/* code table */}
      <div style={{ position: "absolute", left: 1120, top: 250, width: 680 }}>
        <div style={{ fontFamily: MONO, fontSize: 24, color: T.muted, marginBottom: 12, opacity: p(0.5, 0.58) }}>resulting prefix code</div>
        {HUFF_SRC.map((d, i) => {
          const at = 0.6 + i * 0.05;
          const hot = Math.floor(frame / 22) % HUFF_SRC.length === i;
          return (
            <div key={i} style={{ display: "flex", alignItems: "center", gap: 22, height: 62, opacity: p(at, at + 0.05) }}>
              <span style={{ width: 60, fontFamily: SANS, fontWeight: 800, fontSize: 36, color: A.code }}>{d.s}</span>
              <span style={{ width: 120, fontFamily: MONO, fontSize: 24, color: T.muted }}>{d.f}</span>
              <span style={{ fontFamily: MONO, fontWeight: 800, fontSize: 34, color: hot ? A.surp : A.bit, background: hot ? mix(T.panel, A.surp, 0.16) : "transparent", padding: "4px 14px", borderRadius: 8 }}>{HUFF.codes[d.s]}</span>
            </div>
          );
        })}
        <div style={{ marginTop: 20, fontFamily: MONO, fontWeight: 800, fontSize: 28, color: A.ent, opacity: p(0.86, 0.94) }}>
          avg {fmt(HUFF.avgLen, 2)} bits  ·  entropy {fmt(HUFF.entropy, 2)} bits
        </div>
      </div>
      <Foot theme={T} p={p(0.9, 0.96)}>
        No codeword is a prefix of another — so the stream decodes with no commas needed.
      </Foot>
    </Stage>
  );
};

// it_crossentropy — cost of using the wrong codebook
const CE_P = [{ s: "A", pt: 0.5 }, { s: "B", pt: 0.25 }, { s: "C", pt: 0.125 }, { s: "D", pt: 0.125 }];
const CE_Q = [0.25, 0.25, 0.25, 0.25]; // model believes uniform
const CrossEntropyScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur);
  const Hp = CE_P.reduce((s, r) => s - r.pt * L2(r.pt), 0); // 1.75
  const Hpq = CE_P.reduce((s, r, i) => s - r.pt * L2(CE_Q[i]), 0); // 2.0
  return (
    <Stage>
      <Head theme={T} kicker="CROSS-ENTROPY" title="The price of a wrong model" color={A.noise} o={p(0, 0.06)} />
      <div style={{ position: "absolute", left: 140, top: 230, width: 800 }}>
        <div style={{ fontFamily: SANS, fontWeight: 700, fontSize: 30, color: T.text, opacity: p(0.08, 0.16), lineHeight: 1.4 }}>
          The world's true frequencies are <span style={{ color: A.bit }}>p</span>. But you built your code
          from a <span style={{ color: A.noise }}>guess q</span>. How many bits does that cost?
        </div>
      </div>
      {CE_P.map((r, i) => {
        const at = 0.24 + i * 0.08;
        const y = 340 + i * 90;
        return (
          <React.Fragment key={i}>
            <div style={{ position: "absolute", left: 160, top: y, fontFamily: SANS, fontWeight: 800, fontSize: 36, color: A.bit, opacity: p(at, at + 0.05) }}>{r.s}</div>
            <div style={{ position: "absolute", left: 260, top: y + 4, fontFamily: MONO, fontSize: 26, color: T.text, opacity: p(at, at + 0.05) }}>true p = {r.pt}</div>
            <div style={{ position: "absolute", left: 540, top: y + 4, fontFamily: MONO, fontSize: 26, color: A.noise, opacity: p(at + 0.02, at + 0.07) }}>model q = {CE_Q[i]}</div>
            <div style={{ position: "absolute", left: 830, top: y + 4, fontFamily: MONO, fontWeight: 700, fontSize: 26, color: T.muted, opacity: p(at + 0.04, at + 0.1) }}>
              code length = {fmt(L2(1 / CE_Q[i]), 0)} bits
            </div>
          </React.Fragment>
        );
      })}
      {/* two totals */}
      <Card theme={T} x={1200} y={320} w={580} h={360} color={A.noise} o={p(0.62, 0.72)} glow>
        <div style={{ display: "flex", alignItems: "baseline", gap: 16 }}>
          <span style={{ fontFamily: SANS, fontSize: 28, color: A.bit }}>ideal H(p)</span>
          <span style={{ fontFamily: MONO, fontWeight: 800, fontSize: 44, color: A.bit }}>{fmt(Hp, 2)}</span>
        </div>
        <div style={{ display: "flex", alignItems: "baseline", gap: 16, marginTop: 14 }}>
          <span style={{ fontFamily: SANS, fontSize: 28, color: A.noise }}>your cost H(p,q)</span>
          <Counter p={p(0.68, 0.82)} to={Hpq} decimals={2} color={A.noise} size={44} />
        </div>
        <div style={{ height: 2, background: T.line, margin: "20px 0" }} />
        <div style={{ display: "flex", alignItems: "baseline", gap: 16 }}>
          <span style={{ fontFamily: SANS, fontWeight: 800, fontSize: 28, color: A.bad }}>wasted</span>
          <Counter p={p(0.78, 0.9)} to={Hpq - Hp} decimals={2} color={A.bad} size={44} suffix=" bits" />
        </div>
        <div style={{ marginTop: 18, fontFamily: SANS, fontWeight: 700, fontSize: 25, color: T.text, opacity: p(0.86, 0.94), lineHeight: 1.35 }}>
          Cross-entropy ≥ entropy, always.
        </div>
      </Card>
      <Foot theme={T} p={p(0.9, 0.96)}>
        This is exactly the loss function that trains modern neural networks.
      </Foot>
    </Stage>
  );
};

// it_kl — KL divergence = the wasted bits, and the ML callback
const KLScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  return (
    <Stage>
      <Head theme={T} kicker="KL DIVERGENCE" title="Distance from truth, measured in bits" color={A.noise} o={p(0, 0.06)} />
      {/* equation build */}
      <div style={{ position: "absolute", left: 0, right: 0, top: 300, textAlign: "center" }}>
        <div style={{ display: "inline-flex", alignItems: "baseline", gap: 24, fontFamily: MONO, fontWeight: 800, fontSize: 56 }}>
          <span style={{ color: A.noise, opacity: p(0.1, 0.2) }}>D(p ‖ q)</span>
          <span style={{ color: T.muted, opacity: p(0.2, 0.3) }}>=</span>
          <span style={{ color: A.noise, opacity: p(0.3, 0.4) }}>H(p, q)</span>
          <span style={{ color: T.muted, opacity: p(0.4, 0.5) }}>−</span>
          <span style={{ color: A.bit, opacity: p(0.5, 0.6) }}>H(p)</span>
        </div>
        <div style={{ marginTop: 30, fontFamily: SANS, fontWeight: 700, fontSize: 34, color: T.text, opacity: p(0.6, 0.7) }}>
          the <span style={{ color: A.bad }}>extra</span> bits you pay for believing q instead of p
        </div>
      </div>
      {/* three properties */}
      {[
        { at: 0.66, t: "Zero only when q = p", c: A.ok },
        { at: 0.74, t: "Never negative", c: A.bit },
        { at: 0.82, t: "Not symmetric: D(p‖q) ≠ D(q‖p)", c: A.surp },
      ].map((r, i) => (
        <div key={i} style={{
          position: "absolute", left: 320 + i * 460, top: 620, width: 420, height: 130,
          borderRadius: 16, background: mix(T.panel, r.c, 0.08), border: `2px solid ${mix(T.line, r.c, 0.6)}`,
          padding: "20px 24px", boxSizing: "border-box", opacity: p(r.at, r.at + 0.06),
          display: "flex", alignItems: "center", fontFamily: SANS, fontWeight: 700, fontSize: 27, color: T.text,
        }}>{r.t}</div>
      ))}
      <div style={{ position: "absolute", left: 0, right: 0, top: 810, textAlign: "center", opacity: p(0.88, 0.96) }}>
        <span style={{ fontFamily: MONO, fontWeight: 800, fontSize: 30, color: A.ent, textShadow: `0 0 ${16 + Math.sin(frame * 0.07) * 8}px ${mix(T.bg0, A.ent, 0.5)}` }}>
          minimizing cross-entropy = minimizing KL = pulling your model toward reality
        </span>
      </div>
    </Stage>
  );
};

// it_mutualinfo — mutual information as overlapping entropy circles
const MutualInfoScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur);
  const cx = 760, cy = 540, r = 250, off = 150;
  return (
    <Stage>
      <Head theme={T} kicker="MUTUAL INFORMATION" title="How much X tells you about Y" color={A.ent} o={p(0, 0.06)} />
      <svg style={{ position: "absolute", left: 0, top: 0, overflow: "visible" }} width={1920} height={1080}>
        <circle cx={cx - off} cy={cy} r={r} fill={mix(T.bg0, A.bit, 0.18)} stroke={A.bit} strokeWidth={3} opacity={p(0.1, 0.2)} />
        <circle cx={cx + off} cy={cy} r={r} fill={mix(T.bg0, A.surp, 0.18)} stroke={A.surp} strokeWidth={3} opacity={p(0.2, 0.3)} />
      </svg>
      <div style={{ position: "absolute", left: cx - off - 210, top: cy - 26, width: 180, textAlign: "center", fontFamily: MONO, fontWeight: 800, fontSize: 30, color: A.bit, opacity: p(0.14, 0.24) }}>H(X)</div>
      <div style={{ position: "absolute", left: cx + off + 30, top: cy - 26, width: 180, textAlign: "center", fontFamily: MONO, fontWeight: 800, fontSize: 30, color: A.surp, opacity: p(0.24, 0.34) }}>H(Y)</div>
      {/* overlap label */}
      <div style={{ position: "absolute", left: cx - 90, top: cy - 30, width: 180, textAlign: "center", fontFamily: MONO, fontWeight: 800, fontSize: 30, color: A.ent, opacity: p(0.4, 0.5), textShadow: `0 0 18px ${mix(T.bg0, A.ent, 0.6)}` }}>I(X;Y)</div>
      <div style={{ position: "absolute", left: cx - off - 130, top: cy - 90, fontFamily: MONO, fontSize: 22, color: T.muted, opacity: p(0.5, 0.6) }}>H(X|Y)</div>
      <div style={{ position: "absolute", left: cx + off + 40, top: cy - 90, fontFamily: MONO, fontSize: 22, color: T.muted, opacity: p(0.5, 0.6) }}>H(Y|X)</div>
      <div style={{ position: "absolute", left: 1300, top: 300, width: 520, opacity: p(0.62, 0.74) }}>
        <div style={{ fontFamily: SANS, fontWeight: 700, fontSize: 30, color: T.text, lineHeight: 1.45 }}>
          Mutual information is the <span style={{ color: A.ent }}>shared</span> uncertainty — how much
          learning Y shrinks your surprise about X.
        </div>
        <div style={{ marginTop: 24, fontFamily: MONO, fontWeight: 800, fontSize: 28, color: A.ent }}>I(X;Y) = H(X) − H(X | Y)</div>
        <div style={{ marginTop: 18, fontFamily: SANS, fontSize: 26, color: T.muted, lineHeight: 1.4 }}>
          Independent variables share nothing: the circles pull apart, and I = 0.
        </div>
      </div>
      <Foot theme={T} p={p(0.88, 0.95)}>
        Mutual information is the backbone of channels, feature selection, and correlation done right.
      </Foot>
    </Stage>
  );
};

// it_channel — binary symmetric channel with noise flips (computed, deterministic)
const ChannelScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const N = 12;
  const flipSeed = Math.floor(frame / 30);
  const bits = Array.from({ length: N }, (_, i) => (rnd(i, 2) > 0.5 ? 1 : 0));
  const flipped = bits.map((b, i) => (rnd(i, flipSeed + 9) < 0.18 ? 1 - b : b));
  return (
    <Stage>
      <Head theme={T} kicker="THE NOISY CHANNEL" title="Every real channel corrupts some bits" color={A.noise} o={p(0, 0.06)} />
      {/* sender */}
      <div style={{ position: "absolute", left: 120, top: 420, fontFamily: SANS, fontWeight: 800, fontSize: 32, color: A.bit, opacity: p(0.06, 0.14) }}>sender</div>
      <div style={{ position: "absolute", left: 120, top: 470, display: "flex", flexDirection: "column", gap: 10, opacity: p(0.1, 0.2) }}>
        {bits.map((b, i) => (
          <span key={i} style={{ fontFamily: MONO, fontWeight: 800, fontSize: 30, color: A.bit }}>{b}</span>
        ))}
      </div>
      {/* channel box */}
      <div style={{ position: "absolute", left: 620, top: 340, width: 680, height: 420, borderRadius: 22, background: mix(T.panel, A.noise, 0.08), border: `2.5px dashed ${A.noise}`, opacity: p(0.16, 0.26) }}>
        <div style={{ position: "absolute", left: 0, right: 0, top: 20, textAlign: "center", fontFamily: MONO, fontSize: 24, color: A.noise }}>binary symmetric channel · flip p ≈ 0.18</div>
      </div>
      <ScanBeam theme={T} x={624} y={344} w={672} h={412} color={A.noise} o={p(0.2, 0.3)} speed={2} />
      <Flow x1={340} y1={560} x2={620} y2={560} color={A.bit} n={7} o={p(0.24, 0.34)} />
      <Flow x1={1300} y1={560} x2={1560} y2={560} color={A.code} n={7} o={p(0.3, 0.4)} />
      {/* noise bolts */}
      {Array.from({ length: 5 }).map((_, i) => (
        <span key={i} style={{ position: "absolute", left: 700 + i * 120, top: 380 + (Math.sin(frame * 0.1 + i) * 20), fontSize: 36, opacity: 0.5 + Math.sin(frame * 0.14 + i * 2) * 0.4 }}>⚡</span>
      ))}
      {/* receiver */}
      <div style={{ position: "absolute", left: 1600, top: 420, fontFamily: SANS, fontWeight: 800, fontSize: 32, color: A.code, opacity: p(0.32, 0.4) }}>receiver</div>
      <div style={{ position: "absolute", left: 1620, top: 470, display: "flex", flexDirection: "column", gap: 10, opacity: p(0.36, 0.46) }}>
        {flipped.map((b, i) => {
          const err = b !== bits[i];
          return (
            <span key={i} style={{ fontFamily: MONO, fontWeight: 800, fontSize: 30, color: err ? A.bad : A.code, textShadow: err ? `0 0 14px ${A.bad}` : "none" }}>
              {b}{err ? " ✗" : ""}
            </span>
          );
        })}
      </div>
      <Foot theme={T} p={p(0.86, 0.94)}>
        Some bits arrive flipped — and the receiver has no way to tell which. Now what?
      </Foot>
    </Stage>
  );
};

// it_capacity — channel capacity C = 1 - H(p) (computed curve)
const CapacityScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const X0 = 220, Y0 = 780, W = 900, H = 520;
  const cp = p(0.16, 0.62);
  // p ranges 0..0.5 across the full plot width, so scale by (pp / 0.5)
  const pts = CAP_CURVE.slice(0, Math.max(2, Math.round(CAP_CURVE.length * cp))).map(({ p: pp, c }) => `${X0 + (pp / 0.5) * W},${Y0 - c * H}`).join(" ");
  const markP = 0.1, markC = 1 - Hbin(0.1);
  const mx = X0 + (markP / 0.5) * W, my = Y0 - markC * H;
  return (
    <Stage>
      <Head theme={T} kicker="CHANNEL CAPACITY" title="The fastest you can ever send" color={A.code} o={p(0, 0.06)} />
      <svg style={{ position: "absolute", left: 0, top: 0, overflow: "visible" }} width={1920} height={1080}>
        <line x1={X0} y1={Y0} x2={X0 + W} y2={Y0} stroke={T.line} strokeWidth={2} />
        <line x1={X0} y1={Y0} x2={X0} y2={Y0 - H - 10} stroke={T.line} strokeWidth={2} />
        <polyline points={pts} fill="none" stroke={A.code} strokeWidth={5} />
        {cp > 0.99 && <>
          <circle cx={mx} cy={my} r={10} fill={A.surp} stroke={T.text} strokeWidth={2} />
          <line x1={mx} y1={Y0} x2={mx} y2={my} stroke={mix(A.surp, T.bg1, 0.4)} strokeWidth={2} strokeDasharray="5 7" />
        </>}
      </svg>
      <div style={{ position: "absolute", left: X0 - 6, top: Y0 + 16, fontFamily: MONO, fontSize: 22, color: T.muted }}>p = 0 (perfect line)</div>
      <div style={{ position: "absolute", left: X0 + W - 150, top: Y0 + 16, fontFamily: MONO, fontSize: 22, color: T.muted }}>p = 0.5 (pure noise)</div>
      <div style={{ position: "absolute", left: X0 - 130, top: Y0 - H - 20, fontFamily: MONO, fontSize: 22, color: A.code, opacity: p(0.3, 0.4) }}>C = 1 bit</div>
      <div style={{ position: "absolute", left: 1260, top: 300, width: 560 }}>
        <div style={{ fontFamily: MONO, fontWeight: 800, fontSize: 40, color: A.code, opacity: p(0.24, 0.34) }}>C = 1 − H(p)</div>
        <div style={{ marginTop: 26, fontFamily: SANS, fontWeight: 700, fontSize: 30, color: T.text, lineHeight: 1.45, opacity: p(0.5, 0.62) }}>
          At an 18% flip rate the channel still carries about{" "}
          <span style={{ color: A.surp }}>{fmt(1 - Hbin(0.18), 2)} bits</span> of real information per use.
        </div>
        <div style={{ marginTop: 24, fontFamily: SANS, fontWeight: 800, fontSize: 32, color: A.bit, opacity: p(0.66, 0.78), textShadow: `0 0 ${16 + Math.sin(frame * 0.06) * 8}px ${mix(T.bg0, A.bit, 0.5)}` }}>
          Below capacity: error can be made vanishingly small.
        </div>
        <div style={{ marginTop: 16, fontFamily: SANS, fontWeight: 800, fontSize: 32, color: A.bad, opacity: p(0.74, 0.86) }}>
          Above capacity: reliable communication is impossible.
        </div>
      </div>
      <Foot theme={T} p={p(0.9, 0.96)}>
        The noisy-channel coding theorem — Shannon's most astonishing result.
      </Foot>
    </Stage>
  );
};

// it_hamming — (7,4) Hamming code as the 3-circle parity Venn (computed)
// data d1..d4 fill the three pairwise/triple regions; p1..p3 make each circle even.
const HAM = (() => {
  const d = [1, 0, 1, 1]; // data nibble
  // circle regions (classic layout):
  //   region A = d1 (top overlap), B = d2, C = d3, center = d4
  //   parity p1 for circle1 = xor of its data bits, etc.
  const d1 = d[0], d2 = d[1], d3 = d[2], d4 = d[3];
  const p1 = d1 ^ d2 ^ d4; // circle 1 covers d1,d2,d4
  const p2 = d1 ^ d3 ^ d4; // circle 2 covers d1,d3,d4
  const p3 = d2 ^ d3 ^ d4; // circle 3 covers d2,d3,d4
  return { d1, d2, d3, d4, p1, p2, p3 };
})();
const HammingScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  // after p(0.55) inject an error in d4 (center); circles 1&2&3 all go odd → locate center
  const errored = p(0.55, 0.57) > 0.5;
  const d4 = errored ? 1 - HAM.d4 : HAM.d4;
  const c1 = (HAM.d1 ^ HAM.d2 ^ d4 ^ HAM.p1);
  const c2 = (HAM.d1 ^ HAM.d3 ^ d4 ^ HAM.p2);
  const c3 = (HAM.d2 ^ HAM.d3 ^ d4 ^ HAM.p3);
  const cx = 640, cy = 540, r = 220;
  const C = [
    { x: cx, y: cy - 130, col: A.bit, bad: c1 }, // circle1 top
    { x: cx - 150, y: cy + 110, col: A.surp, bad: c2 }, // circle2 bottom-left
    { x: cx + 150, y: cy + 110, col: A.ent, bad: c3 }, // circle3 bottom-right
  ];
  const bitDot = (x: number, y: number, v: number, label: string, col: string, o: number, hot = false) => (
    <div style={{ position: "absolute", left: x - 30, top: y - 30, width: 60, height: 60, borderRadius: 12, background: mix(T.panel, col, 0.3), border: `2.5px solid ${hot ? A.bad : col}`, display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", opacity: o, boxShadow: hot ? `0 0 20px ${A.bad}` : "none" }}>
      <span style={{ fontFamily: MONO, fontWeight: 800, fontSize: 28, color: hot ? A.bad : T.text }}>{v}</span>
      <span style={{ fontFamily: MONO, fontSize: 13, color: T.muted, marginTop: -2 }}>{label}</span>
    </div>
  );
  return (
    <Stage>
      <Head theme={T} kicker="ERROR CORRECTION" title="Redundancy that repairs itself" color={A.code} o={p(0, 0.06)} />
      <svg style={{ position: "absolute", left: 0, top: 0, overflow: "visible" }} width={1920} height={1080}>
        {C.map((c, i) => (
          <circle key={i} cx={c.x} cy={c.y} r={r} fill="none"
            stroke={errored && c.bad ? A.bad : c.col} strokeWidth={errored && c.bad ? 5 : 3}
            opacity={p(0.1 + i * 0.05, 0.2 + i * 0.05)} />
        ))}
      </svg>
      {/* data + parity bits placed in regions */}
      {bitDot(cx, cy - 175, HAM.d1, "d1", A.code, p(0.24, 0.32))}
      {bitDot(cx - 110, cy + 40, HAM.d2, "d2", A.code, p(0.28, 0.36))}
      {bitDot(cx + 110, cy + 40, HAM.d3, "d3", A.code, p(0.32, 0.4))}
      {bitDot(cx, cy + 20, d4, "d4", A.code, p(0.36, 0.44), errored)}
      {bitDot(cx, cy - 250, HAM.p1, "p1", A.bit, p(0.44, 0.5))}
      {bitDot(cx - 230, cy + 180, HAM.p2, "p2", A.surp, p(0.46, 0.52))}
      {bitDot(cx + 230, cy + 180, HAM.p3, "p3", A.ent, p(0.48, 0.54))}
      {/* right column explanation */}
      <div style={{ position: "absolute", left: 1080, top: 280, width: 740 }}>
        <div style={{ fontFamily: SANS, fontWeight: 700, fontSize: 29, color: T.text, lineHeight: 1.45, opacity: p(0.14, 0.24) }}>
          Four data bits, three parity bits. Each circle is arranged to hold an{" "}
          <span style={{ color: A.code }}>even</span> number of ones.
        </div>
        <div style={{ marginTop: 26, fontFamily: SANS, fontWeight: 800, fontSize: 30, color: errored ? A.bad : A.code, opacity: p(0.56, 0.66) }}>
          {errored ? "A bit just flipped." : "All parities even — clean."}
        </div>
        <div style={{ marginTop: 16, fontFamily: SANS, fontWeight: 700, fontSize: 28, color: T.text, lineHeight: 1.45, opacity: p(0.62, 0.74) }}>
          {errored ? (
            <>Every circle that now reads <span style={{ color: A.bad }}>odd</span> overlaps at exactly one
              bit — the culprit. The receiver flips it back, with no retransmission.</>
          ) : "Change any single bit and the pattern of broken circles points straight to it."}
        </div>
        <div style={{ marginTop: 22, fontFamily: MONO, fontWeight: 800, fontSize: 26, color: A.ent, opacity: p(0.78, 0.88) }}>
          syndrome: [{c1}{c2}{c3}] → {errored ? "center bit d4" : "no error"}
        </div>
      </div>
      {errored && <Brackets x={cx - 40} y={cy - 20} w={80} h={80} color={A.bad} o={0.6 + Math.sin(frame * 0.12) * 0.4} len={22} />}
      <Foot theme={T} p={p(0.9, 0.96)}>
        This is how QR codes, deep-space probes, and your SSD survive real-world noise.
      </Foot>
    </Stage>
  );
};

// it_apps — where information theory shows up
const AppsScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const p = usePfull(dur);   // narration-tracked list + chase — keep full-beat timing
  const items = [
    { emoji: "🗜️", label: "ZIP · JPEG · MP3", c: A.code },
    { emoji: "🧠", label: "cross-entropy loss", c: A.noise },
    { emoji: "📡", label: "5G · Wi-Fi · deep space", c: A.bit },
    { emoji: "🧬", label: "DNA & the genome", c: A.ok },
    { emoji: "🔐", label: "cryptography", c: A.ent },
    { emoji: "🌡️", label: "thermodynamic entropy", c: A.surp },
  ];
  return (
    <Stage>
      <Head theme={T} kicker="INFORMATION EVERYWHERE" title="One idea, wired through everything" color={A.bit} o={p(0, 0.06)} />
      {items.map((it, i) => {
        const ang = (i / items.length) * Math.PI * 2 - Math.PI / 2 + Math.sin(frame * 0.008) * 0.05;
        const x = 700 + Math.cos(ang) * 520, y = 560 + Math.sin(ang) * 260;
        const at = 0.1 + i * 0.08;
        const active = Math.floor(frame / 28) % items.length === i;
        return (
          <React.Fragment key={i}>
            <Wire x1={700} y1={560} x2={x} y2={y} p={p(at, at + 0.06)} color={active ? it.c : mix(T.muted, T.bg1, 0.4)} w={active ? 3 : 2} arrow={false} />
            <div style={{
              position: "absolute", left: x - 170, top: y - 50, width: 340, height: 100, borderRadius: 18,
              background: mix(T.panel, it.c, active ? 0.2 : 0.08), border: `2.5px solid ${active ? it.c : mix(T.line, it.c, 0.5)}`,
              display: "flex", alignItems: "center", gap: 16, padding: "0 22px", boxSizing: "border-box",
              opacity: p(at, at + 0.08), transform: `scale(${active ? 1.07 : 1})`,
              boxShadow: active ? `0 0 26px ${mix(T.bg0, it.c, 0.35)}` : "none",
            }}>
              <span style={{ fontSize: 44 }}>{it.emoji}</span>
              <span style={{ fontFamily: SANS, fontWeight: 700, fontSize: 26, color: T.text }}>{it.label}</span>
            </div>
          </React.Fragment>
        );
      })}
      {/* hub */}
      <div style={{ position: "absolute", left: 700 - 90, top: 560 - 90, width: 180, height: 180, borderRadius: 90, background: mix(T.panel, A.bit, 0.2), border: `3px solid ${A.bit}`, display: "flex", alignItems: "center", justifyContent: "center", boxShadow: `0 0 ${30 + Math.sin(frame * 0.06) * 12}px ${mix(T.bg0, A.bit, 0.4)}` }}>
        <span style={{ fontFamily: MONO, fontWeight: 800, fontSize: 30, color: A.bit, textAlign: "center", lineHeight: 1.1 }}>the<br />bit</span>
      </div>
      <Foot theme={T} p={p(0.88, 0.95)}>
        From your phone's storage to the edge of the solar system — all the same theory.
      </Foot>
    </Stage>
  );
};

// it_recap — the whole journey
const RecapScene: React.FC<{ dur?: number; items?: string[]; closer?: string }> = ({
  dur, items = [], closer = "Information is surprise you can count — and Shannon taught us how.",
}) => {
  const frame = useCurrentFrame();
  const p = usePfull(dur);   // narration-tracked recap list — keep full-beat timing
  return (
    <AbsoluteFill style={{ padding: "60px 130px", justifyContent: "center" }}>
      <BitStream y={120} color={A.bit} o={0.25} speed={1.6} />
      <BitStream y={940} color={A.ent} o={0.22} speed={-1.3} seed={5} />
      <div style={{ opacity: p(0, 0.06), textAlign: "center", marginBottom: 26 }}>
        <Kicker theme={T} text="RECAP — THE WHOLE MAP" cx />
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 60, color: T.text, marginTop: 12, letterSpacing: -1.5 }}>Information theory in one breath</div>
      </div>
      <div style={{ display: "flex", flexDirection: "column", gap: 11, maxWidth: 1360, margin: "0 auto", width: "100%" }}>
        {items.map((it, i) => {
          const at = 0.05 + i * 0.085;
          const o = p(at, at + 0.06);
          return (
            <div key={i} style={{ display: "flex", alignItems: "center", gap: 18, opacity: o, transform: `translateX(${(1 - o) * -24}px)`, background: mix(T.panel, A.bit, 0.05), border: `1.5px solid ${T.line}`, borderLeft: `4px solid ${A.bit}`, borderRadius: 12, padding: "13px 26px" }}>
              <span style={{ color: A.bit, fontFamily: MONO, fontWeight: 700, fontSize: 25 }}>{i + 1}</span>
              <span style={{ fontFamily: SANS, fontSize: 28, color: T.text, lineHeight: 1.25 }}>{it}</span>
            </div>
          );
        })}
      </div>
      <div style={{ textAlign: "center", marginTop: 30, opacity: p(0.82, 0.92) }}>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontStyle: "italic", fontSize: 40, color: A.bit, textShadow: `0 0 ${28 + Math.sin(frame * 0.06) * 14}px ${mix(T.bg0, A.bit, 0.7)}` }}>{closer}</div>
      </div>
    </AbsoluteFill>
  );
};

// it_conditional — chain rule / info diagram as one decomposed bar
const ConditionalScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur);
  // example numbers (bits): H(X)=1.0, H(Y)=1.5, joint=2.0
  const HxY = 0.5, I = 0.5, HyX = 1.0;           // H(X|Y), I(X;Y), H(Y|X)
  const total = HxY + I + HyX;                     // H(X,Y) = 2.0
  const X0 = 200, W = 1200, y = 470, barH = 96;
  const segs = [
    { at: 0.16, w: HxY, label: "H(X|Y)", c: A.bit, sub: "X's private part" },
    { at: 0.3, w: I, label: "I(X;Y)", c: A.ent, sub: "shared" },
    { at: 0.44, w: HyX, label: "H(Y|X)", c: A.surp, sub: "Y's private part" },
  ];
  let acc = 0;
  return (
    <Stage>
      <Head theme={T} kicker="CONDITIONAL & JOINT ENTROPY" title="Splitting uncertainty into pieces" color={A.ent} o={p(0, 0.06)} />
      <div style={{ position: "absolute", left: 200, top: 250, width: 1200, fontFamily: SANS, fontWeight: 700, fontSize: 30, color: T.text, lineHeight: 1.4, opacity: p(0.06, 0.14) }}>
        The joint entropy H(X,Y) — the total surprise in two variables together — splits cleanly into
        three blocks.
      </div>
      {segs.map((s, i) => {
        const left = X0 + (acc / total) * W;
        const w = (s.w / total) * W * p(s.at, s.at + 0.1);
        acc += s.w;
        return (
          <React.Fragment key={i}>
            <div style={{ position: "absolute", left, top: y, width: w, height: barH, background: `linear-gradient(180deg, ${s.c}, ${mix(s.c, T.bg1, 0.5)})`, borderRight: `3px solid ${T.bg0}`, opacity: 1 }} />
            <div style={{ position: "absolute", left: left + 8, top: y + 18, width: (s.w / total) * W - 16, fontFamily: MONO, fontWeight: 800, fontSize: 26, color: T.bg0, opacity: p(s.at + 0.04, s.at + 0.12) }}>{s.label}</div>
            <div style={{ position: "absolute", left, top: y + barH + 12, width: (s.w / total) * W, textAlign: "center", fontFamily: MONO, fontSize: 21, color: s.c, opacity: p(s.at + 0.06, s.at + 0.14) }}>{s.w} bits · {s.sub}</div>
          </React.Fragment>
        );
      })}
      {/* braces above: H(X) covers first two, H(Y) covers last two */}
      <div style={{ position: "absolute", left: X0, top: y - 54, width: ((HxY + I) / total) * W, height: 30, borderBottom: `3px solid ${A.bit}`, borderLeft: `3px solid ${A.bit}`, borderRight: `3px solid ${A.bit}`, opacity: p(0.58, 0.66) }} />
      <div style={{ position: "absolute", left: X0, top: y - 92, width: ((HxY + I) / total) * W, textAlign: "center", fontFamily: MONO, fontWeight: 800, fontSize: 26, color: A.bit, opacity: p(0.6, 0.68) }}>H(X) = 1.0</div>
      <div style={{ position: "absolute", left: X0 + (HxY / total) * W, top: y + barH + 60, width: ((I + HyX) / total) * W, height: 30, borderTop: `3px solid ${A.surp}`, borderLeft: `3px solid ${A.surp}`, borderRight: `3px solid ${A.surp}`, opacity: p(0.68, 0.76) }} />
      <div style={{ position: "absolute", left: X0 + (HxY / total) * W, top: y + barH + 96, width: ((I + HyX) / total) * W, textAlign: "center", fontFamily: MONO, fontWeight: 800, fontSize: 26, color: A.surp, opacity: p(0.7, 0.78) }}>H(Y) = 1.5</div>
      <div style={{ position: "absolute", left: 200, top: 800, fontFamily: MONO, fontWeight: 800, fontSize: 30, color: A.code, opacity: p(0.82, 0.9) }}>
        chain rule:  H(X,Y) = H(X) + H(Y | X)
      </div>
      <Foot theme={T} p={p(0.9, 0.96)}>
        The shared middle block is the mutual information — the same overlap we drew as two circles.
      </Foot>
    </Stage>
  );
};

// it_redundancy — Shannon's guessing game: predictable text carries ~1 bit/letter
const RedundancyScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const p = usePfull(dur);   // narration-tracked letter reveal — keep full-beat timing
  const sentence = "THE_QUICK_BROWN_FOX";
  const shown = Math.round(sentence.length * p(0.16, 0.62));
  // predictability rises as context grows → bits/letter falls from 4.2 toward ~1
  const bpc = interpolate(p(0.3, 0.82), [0, 1], [4.2, 1.1]);
  return (
    <Stage>
      <Head theme={T} kicker="THE REDUNDANCY OF LANGUAGE" title="You can guess the next letter" color={A.bit} o={p(0, 0.06)} />
      <div style={{ position: "absolute", left: 160, top: 300, width: 1100, opacity: p(0.06, 0.14), fontFamily: SANS, fontWeight: 700, fontSize: 30, color: T.text, lineHeight: 1.4 }}>
        Shannon ran a game: cover the next letter of a sentence and guess it. In English, you win
        astonishingly often.
      </div>
      <div style={{ position: "absolute", left: 160, top: 430, display: "flex", gap: 8 }}>
        {[...sentence].map((ch, i) => {
          const on = i < shown;
          const isNext = i === shown;
          return (
            <div key={i} style={{
              width: 56, height: 76, borderRadius: 10, display: "flex", alignItems: "center", justifyContent: "center",
              background: on ? mix(T.panel, A.bit, 0.25) : T.panel, border: `2px solid ${isNext ? A.surp : on ? A.bit : T.line}`,
              opacity: on || isNext ? 1 : 0.3,
              boxShadow: isNext ? `0 0 16px ${A.surp}` : "none",
            }}>
              <span style={{ fontFamily: MONO, fontWeight: 800, fontSize: 34, color: ch === "_" ? T.muted : on ? T.text : (isNext ? A.surp : T.muted) }}>
                {isNext ? "?" : ch === "_" ? "·" : ch}
              </span>
            </div>
          );
        })}
      </div>
      {/* bits/letter meter */}
      <div style={{ position: "absolute", left: 160, top: 600, width: 900, opacity: p(0.34, 0.44) }}>
        <div style={{ fontFamily: MONO, fontSize: 24, color: T.muted, marginBottom: 10 }}>information actually carried, per letter</div>
        <div style={{ width: 900, height: 40, borderRadius: 10, background: T.panel, border: `2px solid ${T.line}`, overflow: "hidden" }}>
          <div style={{ width: `${(bpc / 4.7) * 100}%`, height: "100%", background: `linear-gradient(90deg, ${A.ent}, ${A.bit})` }} />
        </div>
        <div style={{ display: "flex", justifyContent: "space-between", marginTop: 10, fontFamily: MONO, fontSize: 22, color: T.muted }}>
          <span>≈ 1 bit (with context)</span><span>4.2 bits (letter alone)</span><span>4.7 bits (random)</span>
        </div>
      </div>
      <Card theme={T} x={1180} y={430} w={600} h={210} color={A.bit} o={p(0.66, 0.76)} glow>
        <div style={{ fontFamily: SANS, fontWeight: 700, fontSize: 28, color: T.text, lineHeight: 1.4 }}>
          English is about <span style={{ color: A.surp }}>75% redundant</span>.
        </div>
        <div style={{ fontFamily: MONO, fontSize: 24, color: T.muted, marginTop: 14, textShadow: `0 0 ${10 + Math.sin(frame * 0.08) * 6}px ${mix(T.bg0, A.bit, 0.4)}` }}>
          that redundancy is what lets us read through typos — and what compressors delete.
        </div>
      </Card>
      <Foot theme={T} p={p(0.9, 0.96)}>
        The true entropy of English is barely above one bit per letter.
      </Foot>
    </Stage>
  );
};

// it_arithmetic — arithmetic coding: subdivide the unit interval (computed)
const ARITH = (() => {
  const cum: Record<string, [number, number]> = { A: [0, 0.6], B: [0.6, 1.0] };
  const msg = ["A", "B", "A"];
  let lo = 0, hi = 1;
  const steps: { sym: string; lo: number; hi: number }[] = [{ sym: "", lo, hi }];
  for (const s of msg) {
    const w = hi - lo;
    const [cl, ch] = cum[s];
    hi = lo + w * ch; lo = lo + w * cl;
    steps.push({ sym: s, lo, hi });
  }
  const bits = -L2(hi - lo);
  return { steps, msg, final: (lo + hi) / 2, bits, cum };
})();
const ArithmeticScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur);
  const X0 = 200, W = 1000, rowH = 150;
  return (
    <Stage>
      <Head theme={T} kicker="ARITHMETIC CODING" title="A whole message becomes one number" color={A.code} o={p(0, 0.06)} />
      {ARITH.steps.slice(1).map((st, i) => {
        const at = 0.14 + i * 0.18;
        const prev = ARITH.steps[i];
        const y = 250 + i * rowH;
        // draw the PREVIOUS interval, subdivided into A|B, highlight the chosen sub
        const w = prev.hi - prev.lo;
        const splitX = X0 + ((ARITH.cum.A[1]) ) * W; // relative split at 0.6 of this row's width
        const rowW = W; // each row re-normalises the previous interval to full width
        const chosenA = st.sym === "A";
        return (
          <React.Fragment key={i}>
            <div style={{ position: "absolute", left: X0 - 150, top: y + 8, width: 130, textAlign: "right", fontFamily: MONO, fontSize: 24, color: T.muted, opacity: p(at, at + 0.06) }}>send “{st.sym}”</div>
            {/* A part */}
            <div style={{ position: "absolute", left: X0, top: y, width: 0.6 * rowW, height: 60, borderRadius: "8px 0 0 8px",
              background: chosenA ? A.code : mix(T.panel, A.code, 0.12), border: `2px solid ${A.code}`, opacity: p(at, at + 0.08),
              display: "flex", alignItems: "center", justifyContent: "center" }}>
              <span style={{ fontFamily: MONO, fontWeight: 800, fontSize: 26, color: chosenA ? T.bg0 : A.code }}>A · 0.6</span>
            </div>
            {/* B part */}
            <div style={{ position: "absolute", left: X0 + 0.6 * rowW, top: y, width: 0.4 * rowW, height: 60, borderRadius: "0 8px 8px 0",
              background: !chosenA ? A.surp : mix(T.panel, A.surp, 0.12), border: `2px solid ${A.surp}`, opacity: p(at, at + 0.08),
              display: "flex", alignItems: "center", justifyContent: "center" }}>
              <span style={{ fontFamily: MONO, fontWeight: 800, fontSize: 26, color: !chosenA ? T.bg0 : A.surp }}>B · 0.4</span>
            </div>
            {/* zoom guides to next row */}
            {i < ARITH.steps.length - 2 && (
              <svg style={{ position: "absolute", left: 0, top: 0, overflow: "visible" }} width={1920} height={1080}>
                <line x1={chosenA ? X0 : X0 + 0.6 * rowW} y1={y + 60} x2={X0} y2={y + rowH} stroke={mix(T.muted, T.bg1, 0.3)} strokeWidth={2} strokeDasharray="4 6" opacity={p(at + 0.1, at + 0.16)} />
                <line x1={chosenA ? X0 + 0.6 * rowW : X0 + rowW} y1={y + 60} x2={X0 + rowW} y2={y + rowH} stroke={mix(T.muted, T.bg1, 0.3)} strokeWidth={2} strokeDasharray="4 6" opacity={p(at + 0.1, at + 0.16)} />
              </svg>
            )}
            {/* running interval */}
            <div style={{ position: "absolute", left: X0 + rowW + 40, top: y + 12, fontFamily: MONO, fontSize: 24, color: A.bit, opacity: p(at + 0.06, at + 0.14) }}>
              [{fmt(st.lo, 3)}, {fmt(st.hi, 3)})
            </div>
          </React.Fragment>
        );
      })}
      <div style={{ position: "absolute", left: 200, top: 800, display: "flex", gap: 30, alignItems: "baseline", opacity: p(0.78, 0.88) }}>
        <span style={{ fontFamily: SANS, fontWeight: 800, fontSize: 32, color: T.text }}>“{ARITH.msg.join("")}” → any number like</span>
        <span style={{ fontFamily: MONO, fontWeight: 800, fontSize: 40, color: A.code }}>{fmt(ARITH.final, 3)}</span>
        <span style={{ fontFamily: MONO, fontSize: 26, color: T.muted }}>≈ {fmt(ARITH.bits, 1)} bits</span>
      </div>
      <Foot theme={T} p={p(0.9, 0.96)}>
        Each symbol shrinks the interval by its probability — so likely messages need fewer digits.
      </Foot>
    </Stage>
  );
};

// it_lossy — lossy compression & the rate-distortion trade-off
const LossyScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const X0 = 220, Y0 = 780, W = 760, H = 500;
  const cp = p(0.16, 0.6);
  // R(D): rate falls as allowed distortion rises — convex decreasing
  const pts = Array.from({ length: 61 }, (_, i) => { const t = i / 60; const d = t; const r = 5 * Math.exp(-3 * d); return { d, r }; });
  const line = pts.slice(0, Math.max(2, Math.round(61 * cp))).map(({ d, r }) => `${X0 + d * W},${Y0 - (r / 5) * H}`).join(" ");
  return (
    <Stage>
      <Head theme={T} kicker="LOSSY COMPRESSION" title="Throw away what no one will miss" color={A.code} o={p(0, 0.06)} />
      <svg style={{ position: "absolute", left: 0, top: 0, overflow: "visible" }} width={1920} height={1080}>
        <line x1={X0} y1={Y0} x2={X0 + W} y2={Y0} stroke={T.line} strokeWidth={2} />
        <line x1={X0} y1={Y0} x2={X0} y2={Y0 - H - 10} stroke={T.line} strokeWidth={2} />
        <polyline points={line} fill="none" stroke={A.code} strokeWidth={5} />
      </svg>
      <div style={{ position: "absolute", left: X0 - 80, top: Y0 - H - 20, fontFamily: MONO, fontSize: 22, color: T.muted }}>bits (rate)</div>
      <div style={{ position: "absolute", left: X0 + W - 120, top: Y0 + 16, fontFamily: MONO, fontSize: 22, color: T.muted }}>distortion →</div>
      <div style={{ position: "absolute", left: X0 + 60, top: Y0 - H + 30, fontFamily: MONO, fontSize: 22, color: A.surp, opacity: p(0.5, 0.6) }}>lossless: exact, but big</div>
      <div style={{ position: "absolute", left: X0 + W - 260, top: Y0 - 130, fontFamily: MONO, fontSize: 22, color: A.noise, opacity: p(0.56, 0.66) }}>tiny, but blurry</div>
      {/* coarsening image blocks: fine vs coarse */}
      <div style={{ position: "absolute", left: 1140, top: 260, opacity: p(0.4, 0.5) }}>
        <div style={{ fontFamily: MONO, fontSize: 22, color: T.muted, marginBottom: 8 }}>original</div>
        <div style={{ display: "grid", gridTemplateColumns: "repeat(8, 34px)", gap: 2 }}>
          {Array.from({ length: 64 }).map((_, i) => { const r = Math.floor(i / 8), c = i % 8; const v = Math.round(120 + 120 * Math.sin(r * 0.6) * Math.cos(c * 0.6)); return <div key={i} style={{ width: 34, height: 34, background: `rgb(${v},${Math.round(v * 0.7)},${255 - v})` }} />; })}
        </div>
      </div>
      <div style={{ position: "absolute", left: 1500, top: 260, opacity: p(0.6, 0.7) }}>
        <div style={{ fontFamily: MONO, fontSize: 22, color: T.muted, marginBottom: 8 }}>compressed</div>
        <div style={{ display: "grid", gridTemplateColumns: "repeat(4, 68px)", gap: 2 }}>
          {Array.from({ length: 16 }).map((_, i) => { const r = Math.floor(i / 4) * 2, c = (i % 4) * 2; const v = Math.round(120 + 120 * Math.sin(r * 0.6) * Math.cos(c * 0.6)); return <div key={i} style={{ width: 68, height: 68, background: `rgb(${v},${Math.round(v * 0.7)},${255 - v})` }} />; })}
        </div>
      </div>
      <div style={{ position: "absolute", left: 1140, top: 620, width: 660, fontFamily: SANS, fontWeight: 700, fontSize: 28, color: T.text, lineHeight: 1.4, opacity: p(0.7, 0.82) }}>
        JPEG, MP3 and video codecs slide down this curve — spending bits only where your eyes and ears
        can tell.
      </div>
      <div style={{ position: "absolute", left: 1140, top: 780, fontFamily: MONO, fontWeight: 800, fontSize: 26, color: A.ent, opacity: p(0.84, 0.92), textShadow: `0 0 ${10 + Math.sin(frame * 0.07) * 6}px ${mix(T.bg0, A.ent, 0.4)}` }}>
        rate-distortion theory sets the best trade
      </div>
    </Stage>
  );
};

// it_perplexity — language models, cross-entropy, perplexity (LLM callback)
const PPX = [
  { w: "mat", pr: 0.55, c: A.code }, { w: "floor", pr: 0.20, c: A.bit }, { w: "sofa", pr: 0.12, c: A.ent }, { w: "roof", pr: 0.08, c: A.surp }, { w: "moon", pr: 0.05, c: A.noise },
];
const PerplexityScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur);
  const H = PPX.reduce((s, r) => s - r.pr * L2(r.pr), 0);
  const ppl = Math.pow(2, H);
  return (
    <Stage>
      <Head theme={T} kicker="PERPLEXITY · LANGUAGE MODELS" title="How surprised is the model?" color={A.bit} o={p(0, 0.06)} />
      <div style={{ position: "absolute", left: 140, top: 230, fontFamily: SANS, fontWeight: 800, fontSize: 40, color: T.text, opacity: p(0.06, 0.14) }}>
        “The cat sat on the <span style={{ color: A.surp }}>___</span>”
      </div>
      {PPX.map((r, i) => {
        const at = 0.18 + i * 0.08;
        const grow = p(at, at + 0.1);
        const w = r.pr * 1100 * grow;
        const y = 320 + i * 80;
        return (
          <React.Fragment key={i}>
            <div style={{ position: "absolute", left: 140, top: y, width: 150, fontFamily: MONO, fontWeight: 700, fontSize: 28, color: r.c, opacity: p(at, at + 0.06) }}>{r.w}</div>
            <div style={{ position: "absolute", left: 300, top: y - 2, width: w, height: 42, borderRadius: 8, background: `linear-gradient(90deg, ${mix(r.c, T.bg1, 0.4)}, ${r.c})`, border: `2px solid ${r.c}` }} />
            <div style={{ position: "absolute", left: 300 + w + 14, top: y, fontFamily: MONO, fontWeight: 800, fontSize: 26, color: r.c, opacity: grow }}>{fmt(r.pr * 100, 0)}%</div>
          </React.Fragment>
        );
      })}
      <Card theme={T} x={1240} y={300} w={560} h={300} color={A.bit} o={p(0.64, 0.74)} glow>
        <div style={{ fontFamily: MONO, fontSize: 24, color: T.muted }}>cross-entropy of the guess</div>
        <div style={{ fontFamily: MONO, fontWeight: 800, fontSize: 44, color: A.ent }}>{fmt(H, 2)} bits</div>
        <div style={{ fontFamily: MONO, fontSize: 24, color: T.muted, marginTop: 18 }}>perplexity = 2^H</div>
        <Counter p={p(0.72, 0.86)} to={ppl} decimals={1} color={A.bit} size={52} />
        <div style={{ fontFamily: SANS, fontWeight: 700, fontSize: 23, color: T.text, marginTop: 14, lineHeight: 1.35 }}>
          like choosing between ~{fmt(ppl, 1)} equally-likely words.
        </div>
      </Card>
      <Foot theme={T} p={p(0.9, 0.96)}>
        Training a language model IS minimizing cross-entropy — driving perplexity down toward one.
      </Foot>
    </Stage>
  );
};

// it_bandwidth — Shannon–Hartley: C = B·log2(1 + SNR)
const BandwidthScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const X0 = 220, Y0 = 780, W = 900, H = 520;
  const cp = p(0.16, 0.62);
  const SNRMAX = 31;
  const pts = Array.from({ length: 61 }, (_, i) => { const snr = (i / 60) * SNRMAX; return { snr, c: L2(1 + snr) }; });
  const cmax = L2(1 + SNRMAX);
  const line = pts.slice(0, Math.max(2, Math.round(61 * cp))).map(({ snr, c }) => `${X0 + (snr / SNRMAX) * W},${Y0 - (c / cmax) * H}`).join(" ");
  return (
    <Stage>
      <Head theme={T} kicker="THE SHANNON–HARTLEY LIMIT" title="Real wires: bandwidth meets noise" color={A.bit} o={p(0, 0.06)} />
      <svg style={{ position: "absolute", left: 0, top: 0, overflow: "visible" }} width={1920} height={1080}>
        <line x1={X0} y1={Y0} x2={X0 + W} y2={Y0} stroke={T.line} strokeWidth={2} />
        <line x1={X0} y1={Y0} x2={X0} y2={Y0 - H - 10} stroke={T.line} strokeWidth={2} />
        <polyline points={line} fill="none" stroke={A.bit} strokeWidth={5} />
      </svg>
      <div style={{ position: "absolute", left: X0 + W - 160, top: Y0 + 16, fontFamily: MONO, fontSize: 22, color: T.muted }}>signal-to-noise →</div>
      <div style={{ position: "absolute", left: X0 - 60, top: Y0 - H - 20, fontFamily: MONO, fontSize: 22, color: A.bit }}>capacity</div>
      <div style={{ position: "absolute", left: 1240, top: 300, width: 560 }}>
        <div style={{ fontFamily: MONO, fontWeight: 800, fontSize: 36, color: A.bit, opacity: p(0.24, 0.34) }}>C = B · log₂(1 + S/N)</div>
        <div style={{ marginTop: 26, fontFamily: SANS, fontWeight: 700, fontSize: 30, color: T.text, lineHeight: 1.45, opacity: p(0.48, 0.6) }}>
          Two ways to send more: widen the <span style={{ color: A.ent }}>bandwidth B</span>, or raise the{" "}
          <span style={{ color: A.surp }}>signal-to-noise ratio</span>.
        </div>
        <div style={{ marginTop: 22, fontFamily: SANS, fontWeight: 700, fontSize: 28, color: T.text, lineHeight: 1.45, opacity: p(0.64, 0.76) }}>
          But the logarithm is a tyrant — doubling capacity from noise alone needs the signal power to
          <span style={{ color: A.noise }}> square</span>.
        </div>
        <div style={{ marginTop: 20, fontFamily: MONO, fontWeight: 800, fontSize: 26, color: A.code, opacity: p(0.78, 0.88), textShadow: `0 0 ${10 + Math.sin(frame * 0.07) * 6}px ${mix(T.bg0, A.code, 0.4)}` }}>
          this one formula sizes every modem, cell tower & fibre
        </div>
      </div>
      <Foot theme={T} p={p(0.9, 0.96)}>
        The same capacity idea — now for continuous, analog channels carrying real signals.
      </Foot>
    </Stage>
  );
};

// it_kolmogorov — Kolmogorov complexity: information of a single object
const KOL = [
  { str: "ABABABABABABABABABAB", prog: "print 'AB' × 10", plen: 15, c: A.code, tag: "compressible" },
  { str: "4C1J7A9QZ2XK8B3FW6DL", prog: "print '4C1J7A9QZ2XK8B3FW6DL'", plen: 27, c: A.noise, tag: "random" },
];
const KolmogorovScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const maxP = 30;
  return (
    <Stage>
      <Head theme={T} kicker="KOLMOGOROV COMPLEXITY" title="The information in one single object" color={A.ent} o={p(0, 0.06)} />
      <div style={{ position: "absolute", left: 140, top: 220, width: 1640, fontFamily: SANS, fontWeight: 700, fontSize: 30, color: T.text, lineHeight: 1.4, opacity: p(0.06, 0.14) }}>
        Entropy needs a probability distribution. But what is the information in one fixed string? Its
        complexity is the length of the shortest program that prints it.
      </div>
      {KOL.map((k, i) => {
        const at = 0.2 + i * 0.24;
        const y = 340 + i * 240;
        const barW = (k.plen / maxP) * 900 * p(at + 0.1, at + 0.24);
        return (
          <React.Fragment key={i}>
            <div style={{ position: "absolute", left: 140, top: y, fontFamily: MONO, fontWeight: 800, fontSize: 34, color: T.text, letterSpacing: 4, opacity: p(at, at + 0.06) }}>{k.str}</div>
            <div style={{ position: "absolute", left: 140, top: y + 54, fontFamily: MONO, fontSize: 25, color: k.c, opacity: p(at + 0.06, at + 0.14) }}>shortest program:  {k.prog}</div>
            <div style={{ position: "absolute", left: 140, top: y + 100, width: barW, height: 40, borderRadius: 8, background: `linear-gradient(90deg, ${mix(k.c, T.bg1, 0.4)}, ${k.c})`, border: `2px solid ${k.c}` }} />
            <div style={{ position: "absolute", left: 140 + barW + 16, top: y + 104, fontFamily: MONO, fontWeight: 800, fontSize: 26, color: k.c, opacity: p(at + 0.14, at + 0.24) }}>
              K ≈ {k.plen} · {k.tag}
            </div>
          </React.Fragment>
        );
      })}
      <div style={{ position: "absolute", left: 1120, top: 340, width: 680, fontFamily: SANS, fontWeight: 700, fontSize: 29, color: T.text, lineHeight: 1.45, opacity: p(0.72, 0.84) }}>
        A patterned string hides a short description. A truly random one has none — the shortest
        program is basically the string itself.
        <div style={{ marginTop: 20, fontFamily: MONO, fontWeight: 800, fontSize: 26, color: A.bit, textShadow: `0 0 ${10 + Math.sin(frame * 0.07) * 6}px ${mix(T.bg0, A.bit, 0.4)}` }}>
          random = incompressible = maximally informative
        </div>
      </div>
      <Foot theme={T} p={p(0.9, 0.96)}>
        A profound idea — though the shortest program can never, in general, be computed.
      </Foot>
    </Stage>
  );
};

// it_aep — the typical set / Asymptotic Equipartition Property
const AEP_n = 100, AEP_H = Hbin(0.8), AEP_typ = Math.round(AEP_n * AEP_H); // ≈72
const AepScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const OX = 200, OY = 250, OW = 620, OH = 560; // outer box = all 2^n sequences
  const iw = 250, ih = 220, ix = OX + 60, iy = OY + 260; // inner = typical set
  const hot = Math.floor(frame / 8) % 20;
  return (
    <Stage>
      <Head theme={T} kicker="THE TYPICAL SET" title="Why compression works at all" color={A.ent} o={p(0, 0.06)} />
      {/* outer box */}
      <div style={{ position: "absolute", left: OX, top: OY, width: OW, height: OH, borderRadius: 20, background: mix(T.panel, A.surp, 0.05), border: `2.5px solid ${mix(T.line, A.surp, 0.5)}`, opacity: p(0.1, 0.2) }} />
      <ScanBeam theme={T} x={OX + 3} y={OY + 3} w={OW - 6} h={OH - 6} color={A.surp} o={p(0.14, 0.24)} speed={1.8} />
      <div style={{ position: "absolute", left: OX + 20, top: OY + 18, fontFamily: MONO, fontSize: 24, color: A.surp, opacity: p(0.12, 0.2) }}>ALL sequences of 100 flips</div>
      <div style={{ position: "absolute", left: OX + 20, top: OY + 52, fontFamily: MONO, fontWeight: 800, fontSize: 40, color: A.surp, opacity: p(0.16, 0.26) }}>2¹⁰⁰ of them</div>
      {/* inner typical set */}
      <div style={{ position: "absolute", left: ix, top: iy, width: iw, height: ih, borderRadius: 14, background: mix(T.panel, A.ent, 0.22), border: `3px solid ${A.ent}`, opacity: p(0.36, 0.48), boxShadow: `0 0 30px ${mix(T.bg0, A.ent, 0.3)}` }}>
        {Array.from({ length: 20 }).map((_, i) => (
          <div key={i} style={{ position: "absolute", left: 18 + (i % 5) * 44, top: 24 + Math.floor(i / 5) * 44, width: 26, height: 26, borderRadius: 6, background: hot === i ? A.bit : mix(T.panel, A.ent, 0.5), border: `1.5px solid ${A.ent}` }} />
        ))}
      </div>
      <div style={{ position: "absolute", left: ix, top: iy + ih + 12, width: iw + 120, fontFamily: MONO, fontWeight: 800, fontSize: 26, color: A.ent, opacity: p(0.44, 0.54) }}>the “typical” set: ≈ 2⁷²</div>
      {/* right column */}
      <div style={{ position: "absolute", left: 920, top: 270, width: 880 }}>
        <div style={{ fontFamily: SANS, fontWeight: 700, fontSize: 30, color: T.text, lineHeight: 1.45, opacity: p(0.5, 0.6) }}>
          For a biased coin, almost every long sequence you will ever actually see has about the same
          mix of heads and tails.
        </div>
        <div style={{ marginTop: 22, fontFamily: SANS, fontWeight: 700, fontSize: 30, color: T.text, lineHeight: 1.45, opacity: p(0.62, 0.72) }}>
          These “typical” sequences are a <span style={{ color: A.ent }}>vanishing fraction</span> of all
          possibilities — yet together they hold <span style={{ color: A.code }}>essentially all</span> the
          probability.
        </div>
        <div style={{ marginTop: 26, fontFamily: MONO, fontWeight: 800, fontSize: 30, color: A.bit, opacity: p(0.76, 0.86), textShadow: `0 0 ${14 + Math.sin(frame * 0.07) * 8}px ${mix(T.bg0, A.bit, 0.5)}` }}>
          just number the typical set → ≈ n · H bits
        </div>
      </div>
      <Foot theme={T} p={p(0.9, 0.96)}>
        This is the deep engine under Shannon's source coding theorem — the entropy, made concrete.
      </Foot>
    </Stage>
  );
};

// it_infogain — information gain: pick the question that cuts entropy most (decision trees / 20Q)
const InfoGainScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const N = 12;
  const dot = (x: number, y: number, c: string, o: number) => (
    <div style={{ position: "absolute", left: x, top: y, width: 40, height: 40, borderRadius: 20, background: c, border: `2px solid ${mix(c, "#ffffff", 0.2)}`, opacity: o, boxShadow: `0 0 10px ${c}` }} />
  );
  const hot = Math.floor(frame / 10) % N;
  return (
    <Stage>
      <Head theme={T} kicker="INFORMATION GAIN" title="The best question cuts uncertainty most" color={A.ent} o={p(0, 0.06)} />
      {/* before: mixed set */}
      <div style={{ position: "absolute", left: 150, top: 250, fontFamily: MONO, fontSize: 24, color: T.muted, opacity: p(0.08, 0.16) }}>before the question — 6 cats, 6 dogs, evenly mixed</div>
      {Array.from({ length: N }).map((_, i) => dot(160 + i * 60, 300, i % 2 ? A.bit : A.surp, p(0.1 + i * 0.01, 0.2 + i * 0.01) * (hot === i ? 0.6 : 1)))}
      <div style={{ position: "absolute", left: 900, top: 296, fontFamily: MONO, fontWeight: 800, fontSize: 30, color: A.ent, opacity: p(0.22, 0.3) }}>H = 1.0 bit</div>
      {/* split arrows */}
      <Wire x1={430} y1={360} x2={330} y2={470} p={p(0.34, 0.44)} color={A.code} />
      <Wire x1={520} y1={360} x2={1100} y2={470} p={p(0.34, 0.44)} color={A.code} />
      <div style={{ position: "absolute", left: 430, top: 405, fontFamily: MONO, fontWeight: 700, fontSize: 24, color: A.code, opacity: p(0.36, 0.44) }}>“does it purr?”</div>
      {/* two pure groups */}
      <div style={{ position: "absolute", left: 150, top: 480, width: 420, height: 180, borderRadius: 16, background: mix(T.panel, A.surp, 0.08), border: `2px solid ${A.surp}`, opacity: p(0.46, 0.56) }} />
      {Array.from({ length: 6 }).map((_, i) => dot(180 + (i % 3) * 60, 520 + Math.floor(i / 3) * 60, A.surp, p(0.48 + i * 0.01, 0.58)))}
      <div style={{ position: "absolute", left: 150, top: 668, width: 420, textAlign: "center", fontFamily: MONO, fontWeight: 700, fontSize: 26, color: A.surp, opacity: p(0.56, 0.64) }}>all cats · H = 0</div>
      <div style={{ position: "absolute", left: 690, top: 480, width: 420, height: 180, borderRadius: 16, background: mix(T.panel, A.bit, 0.08), border: `2px solid ${A.bit}`, opacity: p(0.46, 0.56) }} />
      {Array.from({ length: 6 }).map((_, i) => dot(720 + (i % 3) * 60, 520 + Math.floor(i / 3) * 60, A.bit, p(0.48 + i * 0.01, 0.58)))}
      <div style={{ position: "absolute", left: 690, top: 668, width: 420, textAlign: "center", fontFamily: MONO, fontWeight: 700, fontSize: 26, color: A.bit, opacity: p(0.56, 0.64) }}>all dogs · H = 0</div>
      {/* gain */}
      <div style={{ position: "absolute", left: 1200, top: 470, width: 600 }}>
        <div style={{ fontFamily: SANS, fontWeight: 700, fontSize: 30, color: T.text, lineHeight: 1.45, opacity: p(0.6, 0.7) }}>
          The information gain of a question is the entropy before, minus the average entropy after.
        </div>
        <div style={{ marginTop: 22, fontFamily: MONO, fontWeight: 800, fontSize: 34, color: A.code, opacity: p(0.72, 0.82) }}>gain = 1.0 − 0 = 1 bit</div>
        <div style={{ marginTop: 18, fontFamily: SANS, fontWeight: 700, fontSize: 27, color: T.text, lineHeight: 1.4, opacity: p(0.8, 0.9), textShadow: `0 0 ${10 + Math.sin(frame * 0.07) * 6}px ${mix(T.bg0, A.code, 0.3)}` }}>
          It is just the mutual information between the question and the label.
        </div>
      </div>
      <Foot theme={T} p={p(0.92, 0.97)}>
        Every decision tree, and every good game of twenty questions, greedily maximizes this gain.
      </Foot>
    </Stage>
  );
};

// it_dpi — data processing inequality: processing can only lose information
const DpiScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur);
  const stages = [
    { at: 0.12, x: 160, label: "X", sub: "the source", c: A.bit },
    { at: 0.3, x: 760, label: "Y", sub: "noisy copy", c: A.surp },
    { at: 0.5, x: 1360, label: "Z", sub: "processed", c: A.ent },
  ];
  const bars = [{ v: 1.0, x: 460, c: A.bit, label: "I(X;Y)" }, { v: 0.62, x: 1060, c: A.ent, label: "I(X;Z)" }];
  return (
    <Stage>
      <Head theme={T} kicker="DATA PROCESSING INEQUALITY" title="You can't create information by thinking harder" color={A.bit} o={p(0, 0.06)} />
      {stages.map((s, i) => (
        <React.Fragment key={i}>
          {i > 0 && <>
            <Wire x1={stages[i - 1].x + 240} y1={400} x2={s.x - 12} y2={400} p={p(s.at - 0.08, s.at)} color={s.c} w={3.5} />
            <Flow x1={stages[i - 1].x + 240} y1={400} x2={s.x - 12} y2={400} color={s.c} n={6} o={p(s.at + 0.02, s.at + 0.1)} />
          </>}
          <Card theme={T} x={s.x} y={300} w={240} h={200} color={s.c} o={p(s.at, s.at + 0.08)} glow>
            <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 64, color: s.c }}>{s.label}</div>
            <div style={{ fontFamily: MONO, fontSize: 22, color: T.muted, marginTop: 10 }}>{s.sub}</div>
          </Card>
        </React.Fragment>
      ))}
      {/* mutual-info bars shrinking */}
      {bars.map((b, i) => {
        const grow = p(0.6 + i * 0.08, 0.72 + i * 0.08);
        const h = b.v * 220 * grow;
        return (
          <React.Fragment key={i}>
            <div style={{ position: "absolute", left: b.x, top: 780 - h, width: 150, height: h, borderRadius: "10px 10px 0 0", background: `linear-gradient(180deg, ${b.c}, ${mix(b.c, T.bg1, 0.5)})`, border: `2px solid ${b.c}`, borderBottom: "none" }} />
            <div style={{ position: "absolute", left: b.x - 20, top: 790, width: 190, textAlign: "center", fontFamily: MONO, fontWeight: 800, fontSize: 26, color: b.c, opacity: p(0.6 + i * 0.08, 0.7 + i * 0.08) }}>{b.label} = {fmt(b.v, 2)}</div>
          </React.Fragment>
        );
      })}
      <div style={{ position: "absolute", left: 1230, top: 600, width: 560, fontFamily: SANS, fontWeight: 700, fontSize: 29, color: T.text, lineHeight: 1.45, opacity: p(0.78, 0.88) }}>
        Once information about X is lost in Y, no amount of clever processing into Z can bring it back.
        <div style={{ marginTop: 14, fontFamily: MONO, fontWeight: 800, fontSize: 26, color: A.code }}>I(X;Z) ≤ I(X;Y)</div>
      </div>
      <Foot theme={T} p={p(0.92, 0.97)}>
        Processing can reshape information, or destroy it — but it can never manufacture it.
      </Foot>
    </Stage>
  );
};

// it_system — Shannon's 1948 communication model
const SystemScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const y = 430, boxW = 210, boxH = 150;
  const boxes = [
    { at: 0.1, x: 120, label: "Source", sub: "the message", c: A.bit },
    { at: 0.24, x: 470, label: "Encoder", sub: "→ signal", c: A.code },
    { at: 0.4, x: 820, label: "Channel", sub: "carries bits", c: A.surp },
    { at: 0.58, x: 1170, label: "Decoder", sub: "→ message", c: A.code },
    { at: 0.7, x: 1520, label: "Destination", sub: "the receiver", c: A.bit },
  ];
  return (
    <Stage>
      <Head theme={T} kicker="THE COMMUNICATION PROBLEM · 1948" title="Shannon's map of every message ever sent" color={A.bit} o={p(0, 0.06)} />
      {boxes.map((b, i) => (
        <React.Fragment key={i}>
          {i > 0 && <>
            <Wire x1={boxes[i - 1].x + boxW} y1={y + boxH / 2} x2={b.x - 6} y2={y + boxH / 2} p={p(b.at - 0.08, b.at)} color={b.c} w={3.5} />
            <Flow x1={boxes[i - 1].x + boxW} y1={y + boxH / 2} x2={b.x - 6} y2={y + boxH / 2} color={b.c} n={5} o={p(b.at, b.at + 0.1)} />
          </>}
          <Card theme={T} x={b.x} y={y} w={boxW} h={boxH} color={b.c} o={p(b.at, b.at + 0.08)}>
            <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 30, color: b.c }}>{b.label}</div>
            <div style={{ fontFamily: MONO, fontSize: 20, color: T.muted, marginTop: 10 }}>{b.sub}</div>
          </Card>
        </React.Fragment>
      ))}
      {/* noise injecting into the channel */}
      <div style={{ position: "absolute", left: 855, top: 730, width: 140, height: 90, borderRadius: 14, background: mix(T.panel, A.noise, 0.14), border: `2.5px dashed ${A.noise}`, display: "flex", alignItems: "center", justifyContent: "center", opacity: p(0.5, 0.6) }}>
        <span style={{ fontFamily: SANS, fontWeight: 800, fontSize: 26, color: A.noise }}>Noise</span>
      </div>
      <Wire x1={925} y1={730} x2={925} y2={y + boxH + 6} p={p(0.52, 0.6)} color={A.noise} w={3} />
      {Array.from({ length: 3 }).map((_, i) => (
        <span key={i} style={{ position: "absolute", left: 900 + i * 30, top: 690 + Math.sin(frame * 0.12 + i) * 8, fontSize: 26, opacity: 0.4 + Math.sin(frame * 0.14 + i * 2) * 0.4 }}>⚡</span>
      ))}
      <div style={{ position: "absolute", left: 120, top: 250, width: 1680, fontFamily: SANS, fontWeight: 700, fontSize: 29, color: T.text, opacity: p(0.06, 0.14), lineHeight: 1.4 }}>
        Shannon drew one diagram that fits a phone call, a text, a DVD, and a signal from Mars alike:
        a message is encoded, pushed through a noisy channel, and decoded at the far end.
      </div>
      <Foot theme={T} p={p(0.88, 0.95)}>
        Separate the meaning from the medium — and the whole problem becomes mathematics.
      </Foot>
    </Stage>
  );
};

// it_repetition — repetition codes, majority vote, and code rate
const RepetitionScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur);
  const bit = (x: number, y: number, v: string, c: string, o: number, flip = false) => (
    <div style={{ position: "absolute", left: x, top: y, width: 72, height: 72, borderRadius: 12, background: mix(T.panel, c, 0.3), border: `2.5px solid ${flip ? A.bad : c}`, display: "flex", alignItems: "center", justifyContent: "center", opacity: o, boxShadow: flip ? `0 0 16px ${A.bad}` : "none" }}>
      <span style={{ fontFamily: MONO, fontWeight: 800, fontSize: 36, color: flip ? A.bad : T.text }}>{v}</span>
    </div>
  );
  return (
    <Stage>
      <Head theme={T} kicker="REPETITION CODES" title="The simplest defence against noise" color={A.code} o={p(0, 0.06)} />
      <div style={{ position: "absolute", left: 140, top: 250, width: 1000, fontFamily: SANS, fontWeight: 700, fontSize: 30, color: T.text, opacity: p(0.06, 0.14), lineHeight: 1.4 }}>
        Want to send a 1 safely? Just say it three times.
      </div>
      {/* send 111 */}
      <div style={{ position: "absolute", left: 160, top: 340, fontFamily: MONO, fontSize: 24, color: T.muted, opacity: p(0.14, 0.22) }}>you send</div>
      {bit(160, 380, "1", A.bit, p(0.16, 0.24))}
      {bit(244, 380, "1", A.bit, p(0.18, 0.26))}
      {bit(328, 380, "1", A.bit, p(0.2, 0.28))}
      <Wire x1={430} y1={416} x2={600} y2={416} p={p(0.3, 0.38)} color={A.surp} />
      <div style={{ position: "absolute", left: 470, top: 360, fontFamily: MONO, fontSize: 22, color: A.surp, opacity: p(0.32, 0.4) }}>noise</div>
      {/* receive 101 (middle flipped) */}
      <div style={{ position: "absolute", left: 640, top: 340, fontFamily: MONO, fontSize: 24, color: T.muted, opacity: p(0.36, 0.44) }}>you receive</div>
      {bit(640, 380, "1", A.bit, p(0.38, 0.46))}
      {bit(724, 380, "0", A.bit, p(0.4, 0.48), true)}
      {bit(808, 380, "1", A.bit, p(0.42, 0.5))}
      {/* majority vote */}
      <Wire x1={910} y1={416} x2={1080} y2={416} p={p(0.52, 0.6)} color={A.code} />
      <div style={{ position: "absolute", left: 1100, top: 360, fontFamily: SANS, fontWeight: 800, fontSize: 30, color: A.code, opacity: p(0.56, 0.64) }}>majority vote → 1 ✓</div>
      <div style={{ position: "absolute", left: 1100, top: 410, width: 640, fontFamily: SANS, fontSize: 26, color: T.text, opacity: p(0.62, 0.7), lineHeight: 1.35 }}>
        One flip can't outvote two survivors. The error is corrected.
      </div>
      {/* rate tradeoff */}
      <Card theme={T} x={160} y={560} w={1580} h={230} color={A.ent} o={p(0.72, 0.82)}>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 32, color: T.text }}>But you paid dearly for it.</div>
        <div style={{ fontFamily: SANS, fontWeight: 700, fontSize: 28, color: T.text, marginTop: 14, lineHeight: 1.4 }}>
          Three bits sent for every one real bit — a code <span style={{ color: A.ent }}>rate</span> of just one third.
          Repetition works, but it is horribly wasteful. Shannon's promise was reliability
          <span style={{ color: A.code }}> without</span> paying that price — and that needs cleverer codes.
        </div>
      </Card>
      <Foot theme={T} p={p(0.9, 0.96)}>
        Reliability versus rate: the central tension of every error-correcting code.
      </Foot>
    </Stage>
  );
};

// it_separation — source-channel separation theorem
const SeparationScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur);
  const y = 440;
  return (
    <Stage>
      <Head theme={T} kicker="THE SEPARATION THEOREM" title="Compress first, then protect" color={A.code} o={p(0, 0.06)} />
      <Card theme={T} x={140} y={y} w={330} h={170} color={A.bit} o={p(0.1, 0.18)}>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 30, color: A.bit }}>raw data</div>
        <div style={{ fontFamily: MONO, fontSize: 21, color: T.muted, marginTop: 10 }}>full of redundancy</div>
      </Card>
      <Wire x1={470} y1={y + 85} x2={614} y2={y + 85} p={p(0.2, 0.28)} color={A.code} />
      <Card theme={T} x={620} y={y} w={330} h={170} color={A.code} o={p(0.26, 0.34)} glow>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 28, color: A.code }}>source coding</div>
        <div style={{ fontFamily: MONO, fontSize: 21, color: T.muted, marginTop: 10 }}>REMOVE redundancy</div>
        <div style={{ fontFamily: MONO, fontSize: 20, color: A.code, marginTop: 6 }}>→ shrink to entropy</div>
      </Card>
      <Wire x1={950} y1={y + 85} x2={1094} y2={y + 85} p={p(0.4, 0.48)} color={A.noise} />
      <Card theme={T} x={1100} y={y} w={330} h={170} color={A.noise} o={p(0.46, 0.54)} glow>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 28, color: A.noise }}>channel coding</div>
        <div style={{ fontFamily: MONO, fontSize: 21, color: T.muted, marginTop: 10 }}>ADD redundancy</div>
        <div style={{ fontFamily: MONO, fontSize: 20, color: A.noise, marginTop: 6 }}>→ structured, to fight noise</div>
      </Card>
      <Wire x1={1430} y1={y + 85} x2={1574} y2={y + 85} p={p(0.58, 0.66)} color={A.surp} />
      <Card theme={T} x={1580} y={y} w={200} h={170} color={A.surp} o={p(0.62, 0.7)}>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 28, color: A.surp }}>channel</div>
        <div style={{ fontFamily: MONO, fontSize: 20, color: T.muted, marginTop: 10 }}>the noisy wire</div>
      </Card>
      <Flow x1={950} y1={y + 85} x2={1094} y2={y + 85} color={A.noise} n={5} o={p(0.42, 0.52)} />
      <div style={{ position: "absolute", left: 140, top: 690, width: 1640, fontFamily: SANS, fontWeight: 700, fontSize: 30, color: T.text, opacity: p(0.74, 0.84), lineHeight: 1.45 }}>
        It looks absurd — strip out redundancy, then add redundancy right back. But the two jobs use
        totally different redundancy, and Shannon proved you lose nothing by doing them separately.
      </div>
      <Foot theme={T} p={p(0.9, 0.96)}>
        Separation is why compression and error-correction are designed as independent layers.
      </Foot>
    </Stage>
  );
};

// it_landauer — Landauer's principle: the physical cost of erasing a bit
const LandauerScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const erased = p(0.4, 0.42) > 0.5;
  return (
    <Stage>
      <Head theme={T} kicker="LANDAUER'S PRINCIPLE" title="Information is physical" color={A.noise} o={p(0, 0.06)} />
      <div style={{ position: "absolute", left: 140, top: 250, width: 1000, fontFamily: SANS, fontWeight: 700, fontSize: 30, color: T.text, opacity: p(0.06, 0.14), lineHeight: 1.4 }}>
        Is a bit just an abstract idea? Not quite. Erasing one has an unavoidable cost — in the real,
        physical world.
      </div>
      {/* the bit */}
      <div style={{ position: "absolute", left: 300, top: 430, width: 180, height: 180, borderRadius: 20, background: mix(T.panel, erased ? T.muted : A.bit, erased ? 0.06 : 0.28), border: `3px solid ${erased ? T.line : A.bit}`, display: "flex", alignItems: "center", justifyContent: "center", opacity: p(0.16, 0.26) }}>
        <span style={{ fontFamily: MONO, fontWeight: 800, fontSize: 90, color: erased ? T.muted : A.bit }}>{erased ? "·" : "1"}</span>
      </div>
      <div style={{ position: "absolute", left: 300, top: 630, width: 180, textAlign: "center", fontFamily: MONO, fontSize: 24, color: T.muted, opacity: p(0.2, 0.3) }}>{erased ? "erased → 0" : "one bit"}</div>
      {/* heat released on erase */}
      {erased && Array.from({ length: 7 }).map((_, i) => {
        const t = (frame * 0.03 + i / 7) % 1;
        return <span key={i} style={{ position: "absolute", left: 500 + t * 220, top: 500 - Math.sin(t * Math.PI) * 120 - i * 6, fontSize: 30, opacity: (1 - t) * 0.9 }}>♨</span>;
      })}
      {erased && <div style={{ position: "absolute", left: 560, top: 420, fontFamily: SANS, fontWeight: 800, fontSize: 30, color: A.noise, opacity: 0.7 + Math.sin(frame * 0.1) * 0.3 }}>heat released →</div>}
      {/* formula + payoff */}
      <Card theme={T} x={1000} y={400} w={780} h={330} color={A.noise} o={p(0.5, 0.6)} glow>
        <div style={{ fontFamily: MONO, fontWeight: 800, fontSize: 40, color: A.noise }}>E ≥ k·T·ln 2</div>
        <div style={{ fontFamily: SANS, fontWeight: 700, fontSize: 27, color: T.text, marginTop: 18, lineHeight: 1.4 }}>
          Erasing a single bit must dissipate at least this much energy as heat — no exceptions.
        </div>
        <div style={{ fontFamily: SANS, fontWeight: 700, fontSize: 27, color: T.text, marginTop: 14, lineHeight: 1.4, opacity: p(0.72, 0.82) }}>
          Shannon's entropy and thermodynamic entropy are not a metaphor. They are the{" "}
          <span style={{ color: A.bit }}>same quantity</span>.
        </div>
      </Card>
      <Foot theme={T} p={p(0.9, 0.96)}>
        Information isn't abstract — it is written in energy, heat, and the laws of physics.
      </Foot>
    </Stage>
  );
};

// it_roadmap — the course map, building part by part (replaces the long title tail)
const RoadmapScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const p = usePfull(dur);   // narration-tracked part list — keep full-beat timing
  const parts = [
    { n: 1, title: "Measuring Information", sub: "surprise → bits", c: A.surp },
    { n: 2, title: "Entropy", sub: "the average surprise of a source", c: A.ent },
    { n: 3, title: "Compression", sub: "how small can a message get?", c: A.code },
    { n: 4, title: "Comparing Beliefs", sub: "cross-entropy, KL, mutual information", c: A.noise },
    { n: 5, title: "Noisy Channels", sub: "perfect talk through a broken wire", c: A.bit },
    { n: 6, title: "The Big Picture", sub: "one idea, everywhere", c: A.ent },
  ];
  const y0 = 210, rowH = 118;
  const hot = Math.floor(frame / 20) % parts.length;
  const railFill = p(0.08, 0.86);
  return (
    <AbsoluteFill style={{ alignItems: "center", justifyContent: "center" }}>
      <BitStream y={90} color={A.bit} o={0.3} speed={1.8} seed={2} />
      <BitStream y={980} color={A.ent} o={0.24} speed={-1.4} seed={9} />
      <div style={{ position: "absolute", left: 0, right: 0, top: 96, textAlign: "center", opacity: p(0, 0.06) }}>
        <Kicker theme={T} text="THE JOURNEY AHEAD · SIX PARTS" cx />
      </div>
      {/* left rail that fills downward as parts appear */}
      <div style={{ position: "absolute", left: 470, top: y0 + 30, width: 4, height: parts.length * rowH - 60, background: T.line, borderRadius: 2 }} />
      <div style={{ position: "absolute", left: 470, top: y0 + 30, width: 4, height: (parts.length * rowH - 60) * railFill, background: `linear-gradient(180deg, ${A.surp}, ${A.bit})`, borderRadius: 2, boxShadow: `0 0 12px ${A.bit}` }} />
      {parts.map((pt, i) => {
        const at = 0.1 + i * 0.12;
        const o = p(at, at + 0.08);
        const active = hot === i;
        return (
          <div key={i} style={{
            position: "absolute", left: 520, top: y0 + i * rowH, width: 900, height: rowH - 20,
            display: "flex", alignItems: "center", gap: 24, opacity: o, transform: `translateX(${(1 - o) * -30}px)`,
          }}>
            <div style={{
              width: 66, height: 66, borderRadius: 16, flexShrink: 0, background: mix(T.panel, pt.c, active ? 0.35 : 0.18),
              border: `2.5px solid ${pt.c}`, display: "flex", alignItems: "center", justifyContent: "center",
              fontFamily: MONO, fontWeight: 800, fontSize: 32, color: pt.c,
              boxShadow: active ? `0 0 22px ${mix(T.bg0, pt.c, 0.5)}` : "none", transform: `scale(${active ? 1.08 : 1})`,
            }}>{pt.n}</div>
            <div>
              <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 40, color: T.text, letterSpacing: -1 }}>{pt.title}</div>
              <div style={{ fontFamily: MONO, fontSize: 24, color: pt.c, marginTop: 4 }}>{pt.sub}</div>
            </div>
          </div>
        );
      })}
      {/* dot travelling down the rail = continuous motion */}
      <div style={{ position: "absolute", left: 464, top: y0 + 26 + ((frame * 3) % (parts.length * rowH - 52)), width: 16, height: 16, borderRadius: 8, background: A.bit, boxShadow: `0 0 16px ${A.bit}`, opacity: p(0.1, 0.2) }} />
    </AbsoluteFill>
  );
};

// SceneProgress — a thin bar that fills L→R across the whole scene. Guarantees a
// visible "this is playing" signal in EVERY frame so no beat can read as frozen,
// even during narration held on one diagram (feedback fix, 2026-07-26).
const SceneProgress: React.FC<{ accent: string; dur?: number }> = ({ accent, dur }) => {
  const p = usePfull(dur);   // full beat — the bar tracks real time, never compressed
  const w = p(0, 1);
  return (
    <div style={{ position: "absolute", left: 0, bottom: 0, height: 5, width: `${w * 100}%`,
      background: `linear-gradient(90deg, ${mix(accent, "#05060C", 0.35)}, ${accent})`,
      boxShadow: `0 0 12px ${accent}`, opacity: 0.85 }} />
  );
};

// =====================================================================================
export const ITScene: React.FC<{ variant: string;[key: string]: unknown }> = ({ variant, ...rest }) => {
  let content: React.ReactNode;
  let accent = A.bit;
  switch (variant) {
    case "it_title": content = <TitleScene {...(rest as any)} />; break;
    case "it_roadmap": content = <RoadmapScene {...(rest as any)} />; break;
    case "it_hook": content = <HookScene {...(rest as any)} />; accent = A.surp; break;
    case "it_divider": content = <Divider {...(rest as any)} />; accent = (rest as any).color || A.bit; break;
    case "it_surprise": content = <SurpriseScene {...(rest as any)} />; accent = A.surp; break;
    case "it_selfinfo": content = <SelfInfoScene {...(rest as any)} />; break;
    case "it_bit": content = <BitScene {...(rest as any)} />; break;
    case "it_encode": content = <EncodeScene {...(rest as any)} />; accent = A.code; break;
    case "it_entropy": content = <EntropyScene {...(rest as any)} />; accent = A.ent; break;
    case "it_entropyformula": content = <EntropyFormulaScene {...(rest as any)} />; accent = A.ent; break;
    case "it_maxent": content = <MaxEntScene {...(rest as any)} />; accent = A.ent; break;
    case "it_letters": content = <LettersScene {...(rest as any)} />; break;
    case "it_sourcecoding": content = <SourceCodingScene {...(rest as any)} />; accent = A.code; break;
    case "it_huffman": content = <HuffmanScene {...(rest as any)} />; accent = A.code; break;
    case "it_crossentropy": content = <CrossEntropyScene {...(rest as any)} />; accent = A.noise; break;
    case "it_kl": content = <KLScene {...(rest as any)} />; accent = A.noise; break;
    case "it_mutualinfo": content = <MutualInfoScene {...(rest as any)} />; accent = A.ent; break;
    case "it_channel": content = <ChannelScene {...(rest as any)} />; accent = A.noise; break;
    case "it_capacity": content = <CapacityScene {...(rest as any)} />; accent = A.code; break;
    case "it_hamming": content = <HammingScene {...(rest as any)} />; accent = A.code; break;
    case "it_conditional": content = <ConditionalScene {...(rest as any)} />; accent = A.ent; break;
    case "it_redundancy": content = <RedundancyScene {...(rest as any)} />; break;
    case "it_arithmetic": content = <ArithmeticScene {...(rest as any)} />; accent = A.code; break;
    case "it_lossy": content = <LossyScene {...(rest as any)} />; accent = A.code; break;
    case "it_perplexity": content = <PerplexityScene {...(rest as any)} />; break;
    case "it_bandwidth": content = <BandwidthScene {...(rest as any)} />; break;
    case "it_kolmogorov": content = <KolmogorovScene {...(rest as any)} />; accent = A.ent; break;
    case "it_aep": content = <AepScene {...(rest as any)} />; accent = A.ent; break;
    case "it_infogain": content = <InfoGainScene {...(rest as any)} />; accent = A.ent; break;
    case "it_dpi": content = <DpiScene {...(rest as any)} />; break;
    case "it_system": content = <SystemScene {...(rest as any)} />; break;
    case "it_repetition": content = <RepetitionScene {...(rest as any)} />; accent = A.code; break;
    case "it_separation": content = <SeparationScene {...(rest as any)} />; accent = A.code; break;
    case "it_landauer": content = <LandauerScene {...(rest as any)} />; accent = A.noise; break;
    case "it_apps": content = <AppsScene {...(rest as any)} />; break;
    case "it_recap": content = <RecapScene {...(rest as any)} />; break;
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

export default ITScene;
