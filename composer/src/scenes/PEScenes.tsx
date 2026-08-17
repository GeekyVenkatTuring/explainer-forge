/**
 * PEScenes.tsx — "Positional Embeddings, From First Principles"
 * ADEPT (VISIBLE rail) + Feynman edition. Prefix `pe`. ~12 min. English (Prabhat).
 *
 * Teaches positional encoding in transformers. The teaching method is ON SCREEN:
 * every teaching scene carries an ADEPT rail (Analogy → Diagram → Example →
 * Plain-English → Technical) that lights up stage by stage, plus a 5-line ledger
 * whose lines reveal in the same stage windows. So the rail + ledger narrate the
 * method while the left-hand diagram builds. Feynman: everyday words, intuition
 * first, jargon last.
 *
 * Identity "Position & Sequence" — dark indigo. Semantic accents (colours mean things):
 *   TOK #A78BFA violet — tokens / embeddings
 *   POS #F6A723 amber  — position
 *   WAV #38BDF8 cyan   — sinusoid / encoding
 *   OK  #43D9A3 green  — attention / "it works"
 *   BAD #F26D6D rose   — the order-blind problem / naive fails
 *   MET #E9D8A6 gold   — the TEACHING METHOD layer (rail + ledger), kept visually
 *                        separate from the content's semantic palette.
 *
 * Compute the real thing (rule 3): the sinusoidal PE matrix, the individual
 * sinusoids, and RoPE's rotation/dot-product are all computed at module scope and
 * indexed by phase — never drawn pictures of numbers.
 */
import React from "react";
import { AbsoluteFill, useCurrentFrame, interpolate } from "remotion";
import {
  makeTheme, mix, MONO, SANS, useP, usePop, rnd,
  Stage, Bg, Kicker, Head, Foot, Wire, Flow, PixGrid,
} from "../lib/primitives";

const T = makeTheme({
  bg0: "#06070F", bg1: "#0B0D1A", bg2: "#141733", panel: "#181B33",
  text: "#EEF0FB", muted: "#8A90B4", line: "rgba(180,190,255,0.09)", accent: "#A78BFA",
});
const TOK = "#A78BFA", POS = "#F6A723", WAV = "#38BDF8", OK = "#43D9A3", BAD = "#F26D6D", MET = "#E9D8A6";
type P = (a: number, b: number) => number;

// ── computed: sinusoidal positional-encoding matrix ─────────────────────────
const DM = 24;    // model dimension (even) — columns of the heatmap
const NPOS = 28;  // positions — rows of the heatmap
const angFreq = (i: number) => 1 / Math.pow(10000, (2 * Math.floor(i / 2)) / DM);
const PE: number[][] = Array.from({ length: NPOS }, (_, pos) =>
  Array.from({ length: DM }, (_, i) => (i % 2 === 0 ? Math.sin(pos * angFreq(i)) : Math.cos(pos * angFreq(i)))));
const PE255: number[][] = PE.map((row) => row.map((v) => Math.round((v + 1) / 2 * 255)));
const WAVE_DIMS = [0, 4, 10, 18]; // fast → slow sinusoids ("clock hands")

// ── computed: RoPE — rotate a 2-D vector by angle ∝ position ────────────────
const ROPE_THETA = 0.42;                          // illustrative angle per position
const ropeAngle = (pos: number) => pos * ROPE_THETA;
const ROPE_M = 6, ROPE_N = 2;                      // two positions to compare
const ROPE_DDOT = Math.cos((ROPE_M - ROPE_N) * ROPE_THETA); // dot depends only on the gap

// ════════════════════════════════════════════ shared motifs
// universal scene-progress bar (rule 2)
const SceneProgress: React.FC<{ dur?: number; color?: string }> = ({ dur, color = WAV }) => {
  const p = useP(dur); const w = p(0, 1);
  return (
    <AbsoluteFill style={{ pointerEvents: "none" }}>
      <div style={{ position: "absolute", left: 0, bottom: 0, height: 5, width: `${w * 100}%`,
        background: `linear-gradient(90deg, ${mix(T.bg1, color, 0.4)}, ${color})`, opacity: 0.75 }} />
    </AbsoluteFill>
  );
};

// THE MOTIF — the visible ADEPT rail. Active stage = which 1/5 of the beat we're in.
const STAGES = [
  { k: "A", w: "ANALOGY", d: "think of it like…" },
  { k: "D", w: "DIAGRAM", d: "picture it" },
  { k: "E", w: "EXAMPLE", d: "work a real case" },
  { k: "P", w: "PLAIN", d: "in plain words" },
  { k: "T", w: "TECHNICAL", d: "the real term" },
];
const TH = [0.2, 0.4, 0.6, 0.8]; // stage boundaries (even fifths)
const AdeptRail: React.FC<{ p: P }> = ({ p }) => {
  const frame = useCurrentFrame();
  const cur = p(0, 1);
  const active = TH.filter((t) => cur >= t).length; // 0..4
  const x0 = 1140, y0 = 66, pw = 108, gap = 20, railW = 5 * pw + 4 * gap;
  return (
    <>
      <div style={{ position: "absolute", left: x0, top: y0 + 26, width: railW, height: 3,
        background: mix(T.panel, MET, 0.3), borderRadius: 2 }} />
      <div style={{ position: "absolute", left: x0, top: y0 + 26, width: Math.min(1, cur) * railW, height: 3,
        background: MET, borderRadius: 2, boxShadow: `0 0 8px ${MET}` }} />
      {STAGES.map((s, i) => {
        const done = i < active, on = i === active;
        return (
          <div key={i} style={{ position: "absolute", left: x0 + i * (pw + gap), top: y0, width: pw, height: 54,
            borderRadius: 12, boxSizing: "border-box",
            background: on ? MET : done ? mix(T.panel, MET, 0.28) : "transparent",
            border: `2px solid ${on || done ? MET : mix(T.line, MET, 0.5)}`,
            display: "flex", alignItems: "center", justifyContent: "center",
            transform: `scale(${on ? 1.08 : 1})`,
            boxShadow: on ? `0 0 ${14 + Math.sin(frame * 0.12) * 5}px ${mix(T.bg0, MET, 0.6)}` : "none" }}>
            <span style={{ fontFamily: MONO, fontWeight: 800, fontSize: 26,
              color: on ? T.bg0 : done ? MET : mix(T.muted, MET, 0.4) }}>{s.k}</span>
          </div>
        );
      })}
      <div style={{ position: "absolute", left: x0, top: y0 + 66, width: railW, textAlign: "center",
        fontFamily: MONO, fontWeight: 700, fontSize: 19, color: MET, letterSpacing: 2 }}>
        {STAGES[active].w} · {STAGES[active].d}
      </div>
    </>
  );
};

// the 5-line content ledger — each stage's takeaway, revealed in its stage window
type Ledg = { k: string; t: string; c: string };
const AdeptLedger: React.FC<{ p: P; x: number; y: number; w: number; lines: Ledg[] }> = ({ p, x, y, w, lines }) => {
  const rowH = 112, gap = 14;
  return (
    <>
      {lines.map((ln, i) => {
        const at = 0.2 * i + 0.02;
        const lo = p(at, at + 0.06);
        return (
          <div key={i} style={{ position: "absolute", left: x, top: y + i * (rowH + gap), width: w, height: rowH,
            borderRadius: 14, background: mix(T.panel, ln.c, 0.07), border: `2px solid ${mix(T.line, ln.c, 0.5)}`,
            display: "flex", alignItems: "center", gap: 18, padding: "0 22px", boxSizing: "border-box",
            opacity: lo, transform: `translateX(${(1 - lo) * 18}px)` }}>
            <div style={{ width: 46, height: 46, borderRadius: 10, flexShrink: 0, background: mix(T.panel, MET, 0.2),
              border: `2px solid ${MET}`, display: "flex", alignItems: "center", justifyContent: "center",
              fontFamily: MONO, fontWeight: 800, fontSize: 24, color: MET }}>{ln.k}</div>
            <span style={{ fontFamily: SANS, fontWeight: 600, fontSize: 23, color: T.text, lineHeight: 1.28 }}>{ln.t}</span>
          </div>
        );
      })}
    </>
  );
};

// a token tile
const Tile: React.FC<{ x: number; y: number; label: string; c: string; o?: number; w?: number; sub?: string }> =
({ x, y, label, c, o = 1, w = 150, sub }) => (
  <div style={{ position: "absolute", left: x, top: y, width: w, height: 74, borderRadius: 12,
    background: mix(T.panel, c, 0.16), border: `2.5px solid ${c}`, display: "flex", flexDirection: "column",
    alignItems: "center", justifyContent: "center", opacity: o, transform: `translateY(${(1 - o) * 14}px)` }}>
    <span style={{ fontFamily: SANS, fontWeight: 800, fontSize: 26, color: T.text }}>{label}</span>
    {sub && <span style={{ fontFamily: MONO, fontSize: 15, color: mix(T.muted, c, 0.5) }}>{sub}</span>}
  </div>
);

// sinusoid line plot (computed) — draws `reveal` fraction of each wave
const WavePlot: React.FC<{ x: number; y: number; w: number; h: number; dims: number[]; reveal: number; colors: string[] }> =
({ x, y, w, h, dims, reveal, colors }) => {
  const N = NPOS * 4;
  const pts = (dim: number) => Array.from({ length: N }, (_, k) => {
    const pos = k / 4; const v = Math.sin(pos * angFreq(dim));
    return `${x + (pos / NPOS) * w},${y + h / 2 - v * (h / 2 - 8)}`;
  }).slice(0, Math.max(2, Math.round(N * reveal))).join(" ");
  return (
    <svg style={{ position: "absolute", left: 0, top: 0, overflow: "visible" }} width={1920} height={1080}>
      <line x1={x} y1={y + h / 2} x2={x + w} y2={y + h / 2} stroke={mix(T.line, T.muted, 0.6)} strokeWidth={1.5} />
      {dims.map((d, i) => (
        <polyline key={i} points={pts(d)} fill="none" stroke={colors[i]} strokeWidth={3.5} opacity={0.92} />
      ))}
    </svg>
  );
};

// ════════════════════════════════════════════ 1. TITLE
const TitleScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur); const frame = useCurrentFrame(); const pop = usePop(dur);
  const tiles = [
    { x: 150, y: 200, l: "the", c: TOK }, { x: 1560, y: 210, l: "cat", c: WAV },
    { x: 120, y: 780, l: "sat", c: POS }, { x: 1580, y: 770, l: "down", c: OK },
  ];
  return (
    <Stage>
      <Bg theme={T} accent={WAV} />
      {tiles.map((m, i) => (
        <div key={i} style={{ position: "absolute", left: m.x, top: m.y,
          opacity: 0.2 + Math.sin(frame * 0.04 + i * 1.3) * 0.1 }}>
          <Tile x={0} y={0} label={m.l} c={m.c} sub={`pos ${i}`} w={130} />
        </div>
      ))}
      <div style={{ position: "absolute", left: 0, right: 0, top: 232, textAlign: "center",
        fontFamily: MONO, fontWeight: 800, fontSize: 22, color: WAV, letterSpacing: 9,
        opacity: p(0.04, 0.14) }}>TRANSFORMERS · FROM FIRST PRINCIPLES · THE ADEPT METHOD</div>
      <div style={{ position: "absolute", left: 0, right: 0, top: 296, textAlign: "center",
        fontFamily: SANS, fontWeight: 800, fontSize: 112, color: T.text, letterSpacing: -3,
        opacity: p(0.10, 0.22), transform: `scale(${0.92 + pop(0.10) * 0.08})` }}>POSITIONAL</div>
      <div style={{ position: "absolute", left: 0, right: 0, top: 424, textAlign: "center",
        fontFamily: SANS, fontWeight: 800, fontSize: 112, letterSpacing: -3,
        color: WAV, textShadow: `0 0 60px ${mix(T.bg0, WAV, 0.7)}`,
        opacity: p(0.18, 0.32), transform: `scale(${0.92 + pop(0.18) * 0.08})` }}>EMBEDDINGS</div>
      <div style={{ position: "absolute", left: 560, right: 560, top: 582, height: 5, borderRadius: 3,
        background: `linear-gradient(90deg, ${mix(T.bg0, WAV, 0.4)}, ${WAV}, ${mix(T.bg0, WAV, 0.4)})`,
        transform: `scaleX(${p(0.24, 0.5)})` }} />
      <div style={{ position: "absolute", left: 300, right: 300, top: 620, textAlign: "center",
        fontFamily: SANS, fontSize: 33, color: T.muted, opacity: p(0.40, 0.56) }}>
        Why order matters · sinusoids &amp; the famous heatmap · RoPE — the modern default
      </div>
      {/* ADEPT rail teaser */}
      <div style={{ position: "absolute", left: 0, right: 0, top: 720, display: "flex", justifyContent: "center",
        gap: 16, opacity: p(0.6, 0.74) }}>
        {STAGES.map((s, i) => (
          <div key={i} style={{ width: 128, borderRadius: 12, border: `2px solid ${MET}`,
            background: mix(T.panel, MET, 0.12), padding: "10px 0", textAlign: "center" }}>
            <div style={{ fontFamily: MONO, fontWeight: 800, fontSize: 22, color: MET }}>{s.k}</div>
            <div style={{ fontFamily: MONO, fontSize: 13, color: mix(T.muted, MET, 0.5), letterSpacing: 1 }}>{s.w}</div>
          </div>
        ))}
      </div>
    </Stage>
  );
};

// ════════════════════════════════════════════ 2. HOOK — order flips meaning
const HookScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur); const frame = useCurrentFrame();
  const rowA = ["Dog", "bites", "man"], rowB = ["Man", "bites", "dog"];
  const cols = [TOK, WAV, POS];
  return (
    <Stage>
      <Bg theme={T} accent={BAD} />
      <Head theme={T} kicker="THE PUZZLE" title="Same Words. Opposite Meaning." color={BAD} />
      {[{ row: rowA, y: 300, tag: "the dog is biting", at: 0.10 },
        { row: rowB, y: 560, tag: "the man is biting", at: 0.34 }].map((r, ri) => (
        <React.Fragment key={ri}>
          {r.row.map((w, i) => (
            <Tile key={i} x={430 + i * 240} y={r.y} label={w} c={cols[i]} w={200}
              o={p(r.at + i * 0.04, r.at + i * 0.04 + 0.06)} sub={`pos ${i}`} />
          ))}
          <div style={{ position: "absolute", left: 1180, top: r.y + 16, width: 620, fontFamily: SANS,
            fontWeight: 700, fontSize: 30, color: ri === 0 ? WAV : POS, opacity: p(r.at + 0.14, r.at + 0.2) }}>
            → {r.tag}
          </div>
        </React.Fragment>
      ))}
      <div style={{ position: "absolute", left: 430, top: 468, fontFamily: MONO, fontWeight: 800, fontSize: 40,
        color: T.muted, opacity: p(0.56, 0.64) }}>same 3 words — just reordered</div>
      <Foot theme={T} p={p(0.78, 0.9)}>
        Word order carries the meaning. Yet a transformer's attention, on its own, can't see order at all. Let's fix that.
      </Foot>
    </Stage>
  );
};

// ════════════════════════════════════════════ 3. DIVIDER (parameterised)
const DividerScene: React.FC<{ dur?: number; n?: number; title?: string; sub?: string; color?: string }> = ({
  dur, n = 1, title = "", sub = "", color = WAV,
}) => {
  const frame = useCurrentFrame(); const p = useP(dur);
  return (
    <Stage>
      <Bg theme={T} accent={color} />
      <div style={{ position: "absolute", left: 0, right: 0, top: 360, textAlign: "center" }}>
        <div style={{ fontFamily: MONO, fontWeight: 800, fontSize: 30, color, letterSpacing: 10,
          opacity: p(0.05, 0.16) }}>PART {String(n).padStart(2, "0")}</div>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 88, color: T.text, letterSpacing: -2,
          marginTop: 16, opacity: p(0.12, 0.26), transform: `translateY(${(1 - p(0.12, 0.26)) * 26}px)` }}>{title}</div>
        <div style={{ height: 5, width: interpolate(p(0.22, 0.52), [0, 1], [0, 460]),
          background: color, borderRadius: 3, margin: "22px auto" }} />
        <div style={{ fontFamily: SANS, fontSize: 31, color: T.muted, opacity: p(0.32, 0.48) }}>{sub}</div>
      </div>
      <div style={{ position: "absolute", left: 0, right: 0, top: 860, display: "flex", justifyContent: "center",
        gap: 14, opacity: p(0.32, 0.48) }}>
        {[1, 2].map((i) => (
          <div key={i} style={{ width: i === n ? 44 : 14, height: 14, borderRadius: 8,
            background: i <= n ? color : mix(T.panel, color, 0.15), border: `1.5px solid ${i <= n ? color : T.line}`,
            opacity: i === n ? 0.7 + Math.sin(frame * 0.1) * 0.3 : 1 }} />
        ))}
      </div>
    </Stage>
  );
};

// shared teaching-scene chrome: Head + rail + ledger + progress
const Teach: React.FC<{
  p: P; kicker: string; title: string; color: string; lines: Ledg[]; children: React.ReactNode; foot: React.ReactNode;
}> = ({ p, kicker, title, color, lines, children, foot }) => (
  <Stage>
    <Bg theme={T} accent={color} />
    <div style={{ position: "absolute", left: 100, top: 54, width: 1000 }}>
      <Kicker theme={T} text={kicker} color={color} o={p(0.03, 0.12)} />
      <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 48, color: T.text, marginTop: 10,
        letterSpacing: -1.2, opacity: p(0.03, 0.12) }}>{title}</div>
    </div>
    <AdeptRail p={p} />
    <AdeptLedger p={p} x={1140} y={222} w={680} lines={lines} />
    {children}
    <Foot theme={T} p={p(0.86, 0.95)}>{foot}</Foot>
  </Stage>
);

// ════════════════════════════════════════════ 4. ORDER-BLIND
const OrderBlindScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur); const frame = useCurrentFrame();
  const words = ["Dog", "bites", "man"];
  const cols = [TOK, WAV, POS];
  // stage E: swap animation — positions of tiles jitter/permute
  const swap = p(0.42, 0.58);
  const order = swap > 0.5 ? [2, 1, 0] : [0, 1, 2];
  return (
    <Teach p={p} kicker="THE PROBLEM" title="Attention Is Order-Blind" color={BAD}
      lines={[
        { k: "A", t: "Like a bag of Scrabble tiles tipped on a table — you see the words, not the order.", c: BAD },
        { k: "D", t: "All tokens enter attention in parallel, not one-by-one like reading.", c: TOK },
        { k: "E", t: "Shuffle the inputs and every attention score is exactly the same.", c: WAV },
        { k: "P", t: "Attention treats the sentence as a SET, not a sequence.", c: OK },
        { k: "T", t: "Self-attention is permutation-equivariant — zero positional info.", c: MET },
      ]}
      foot="No recurrence, no convolution — nothing in plain attention encodes 'which word came first'.">
      {/* bag of tiles / parallel tokens */}
      <div style={{ position: "absolute", left: 120, top: 250, width: 900, height: 240, borderRadius: 18,
        background: mix(T.bg1, BAD, 0.04), border: `2px solid ${mix(T.line, BAD, 0.4)}`, opacity: p(0.06, 0.16) }} />
      {words.map((w, i) => {
        const oi = order[i];
        const x = 180 + oi * 250 + Math.sin(frame * 0.05 + i) * 6;
        return <Tile key={i} x={x} y={330} label={w} c={cols[i]} w={200} o={p(0.06 + i * 0.03, 0.16 + i * 0.03)} />;
      })}
      <div style={{ position: "absolute", left: 120, top: 262, width: 900, textAlign: "center",
        fontFamily: MONO, fontSize: 18, color: T.muted, opacity: p(0.2, 0.3) }}>ALL TOKENS ENTER TOGETHER →</div>
      {/* attention grid (symmetric relationships) */}
      <div style={{ position: "absolute", left: 300, top: 560, fontFamily: MONO, fontWeight: 700, fontSize: 20,
        color: T.muted, opacity: p(0.3, 0.4) }}>pairwise attention</div>
      {[0, 1, 2].map((r) => [0, 1, 2].map((c) => {
        const v = 0.3 + 0.5 * Math.abs(Math.cos((r - c) * 1.2));
        return (
          <div key={`${r}-${c}`} style={{ position: "absolute", left: 300 + c * 90, top: 600 + r * 90, width: 78, height: 78,
            borderRadius: 8, background: mix(T.panel, OK, v * 0.5), border: `1.5px solid ${mix(T.line, OK, 0.4)}`,
            opacity: p(0.32, 0.44) }} />
        );
      }))}
      <div style={{ position: "absolute", left: 610, top: 660, width: 420, fontFamily: SANS, fontSize: 24,
        color: T.text, opacity: swap, lineHeight: 1.4 }}>
        Reorder the words and the <span style={{ color: BAD, fontWeight: 700 }}>same grid</span> comes back — position is invisible.
      </div>
    </Teach>
  );
};

// ════════════════════════════════════════════ 5. THE FIX — POSITION TAGS
const TagScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur);
  const words = ["the", "cat", "sat"];
  return (
    <Teach p={p} kicker="THE FIX" title="Stamp Each Word With Where It Sits" color={POS}
      lines={[
        { k: "A", t: "Like house numbers on a street — every spot gets its own address.", c: POS },
        { k: "D", t: "Make a position vector for each slot: 0, 1, 2, …", c: POS },
        { k: "E", t: "cat's vector + the 'position-1' vector = a position-aware cat.", c: TOK },
        { k: "P", t: "Add a little 'where I am' signal to every word's meaning vector.", c: OK },
        { k: "T", t: "A positional embedding, ADDED to the token embedding.", c: MET },
      ]}
      foot="Same length as the token vector, so it just adds in — no extra slots, no bigger model.">
      {words.map((w, i) => (
        <React.Fragment key={i}>
          <Tile x={150 + i * 300} y={280} label={w} c={TOK} w={200} o={p(0.06 + i * 0.03, 0.14 + i * 0.03)} sub="token" />
          <div style={{ position: "absolute", left: 150 + i * 300, top: 372, width: 200, textAlign: "center",
            fontFamily: MONO, fontWeight: 800, fontSize: 34, color: T.muted, opacity: p(0.24, 0.34) }}>+</div>
          <Tile x={150 + i * 300} y={420} label={`pos ${i}`} c={POS} w={200} o={p(0.24 + i * 0.03, 0.32 + i * 0.03)} sub="position" />
          <div style={{ position: "absolute", left: 150 + i * 300, top: 512, width: 200, textAlign: "center",
            fontFamily: MONO, fontWeight: 800, fontSize: 34, color: T.muted, opacity: p(0.42, 0.52) }}>↓</div>
          <Tile x={150 + i * 300} y={560} label={w} c={OK} w={200} o={p(0.44 + i * 0.03, 0.52 + i * 0.03)} sub={`${w} @ ${i}`} />
        </React.Fragment>
      ))}
      <div style={{ position: "absolute", left: 150, top: 672, width: 900, fontFamily: SANS, fontSize: 24,
        color: T.text, opacity: p(0.6, 0.7), lineHeight: 1.4 }}>
        Now "<span style={{ color: OK, fontWeight: 700 }}>cat at 1</span>" and "cat at 5" are different vectors — attention can finally tell them apart.
      </div>
    </Teach>
  );
};

// ════════════════════════════════════════════ 6. NAIVE ATTEMPTS
const NaiveScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur);
  return (
    <Teach p={p} kicker="TWO TEMPTING SHORTCUTS" title="Why the Obvious Tags Fail" color={BAD}
      lines={[
        { k: "A", t: "Idea 1: number the seats 0,1,2… — like shouting a bigger number each step.", c: BAD },
        { k: "D", t: "By word 500 the tag is 500 — it drowns out the word's meaning.", c: BAD },
        { k: "E", t: "Idea 2: squeeze positions into 0…1 — but the step size then depends on length.", c: POS },
        { k: "P", t: "'Position 5' should mean the same thing in a short OR a long sentence.", c: OK },
        { k: "T", t: "We want tags: bounded, unique, consistent distances, and extrapolating.", c: MET },
      ]}
      foot="Hold these four wishes — the sinusoidal trick grants all of them at once.">
      {/* idea 1: exploding integers */}
      <div style={{ position: "absolute", left: 120, top: 250, width: 900, height: 250, borderRadius: 16,
        background: mix(T.bg1, BAD, 0.05), border: `2px solid ${mix(T.line, BAD, 0.45)}`, opacity: p(0.06, 0.16), padding: 22, boxSizing: "border-box" }}>
        <div style={{ fontFamily: MONO, fontWeight: 800, fontSize: 22, color: BAD }}>IDEA 1 · raw index 0,1,2,3 …</div>
      </div>
      {[0, 1, 2, 500].map((v, i) => (
        <div key={i} style={{ position: "absolute", left: 150 + i * 200, top: 330, width: 170, height: 110, borderRadius: 12,
          background: mix(T.panel, BAD, i === 3 ? 0.22 : 0.08), border: `2px solid ${BAD}`,
          display: "flex", alignItems: "center", justifyContent: "center",
          fontFamily: MONO, fontWeight: 800, fontSize: i === 3 ? 46 : 40, color: i === 3 ? BAD : T.text,
          opacity: p(0.1 + i * 0.04, 0.2 + i * 0.04), transform: `scale(${i === 3 ? 1 + (p(0.24, 0.34)) * 0.12 : 1})` }}>{v}</div>
      ))}
      <div style={{ position: "absolute", left: 150, top: 452, width: 850, fontFamily: SANS, fontSize: 22, color: BAD,
        opacity: p(0.28, 0.38) }}>huge numbers swamp the embedding ✗</div>
      {/* idea 2: 0..1 rescale */}
      <div style={{ position: "absolute", left: 120, top: 540, width: 900, height: 250, borderRadius: 16,
        background: mix(T.bg1, POS, 0.05), border: `2px solid ${mix(T.line, POS, 0.45)}`, opacity: p(0.4, 0.5), padding: 22, boxSizing: "border-box" }}>
        <div style={{ fontFamily: MONO, fontWeight: 800, fontSize: 22, color: POS }}>IDEA 2 · squeeze into 0 … 1</div>
      </div>
      {[{ lbl: "5 words", step: "0.25 / step" }, { lbl: "50 words", step: "0.02 / step" }].map((r, i) => (
        <div key={i} style={{ position: "absolute", left: 150, top: 620 + i * 78, width: 850, height: 62, borderRadius: 10,
          background: mix(T.panel, POS, 0.06), border: `1.5px solid ${mix(T.line, POS, 0.4)}`, display: "flex",
          alignItems: "center", gap: 24, padding: "0 24px", boxSizing: "border-box", opacity: p(0.46 + i * 0.06, 0.56 + i * 0.06) }}>
          <span style={{ fontFamily: MONO, fontWeight: 700, fontSize: 22, color: POS, width: 160 }}>{r.lbl}</span>
          <span style={{ fontFamily: SANS, fontSize: 22, color: T.text }}>step size = {r.step} — "position 1" keeps changing ✗</span>
        </div>
      ))}
    </Teach>
  );
};

// ════════════════════════════════════════════ 7. SINUSOIDS — clock hands
const SinusoidScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur);
  const reveal = p(0.2, 0.62);
  const wcols = [BAD, POS, WAV, TOK];
  return (
    <Teach p={p} kicker="THE SINUSOIDAL IDEA" title="Clock Hands at Different Speeds" color={WAV}
      lines={[
        { k: "A", t: "Like a clock: a fast seconds hand + slow hours hand pin down a unique time.", c: WAV },
        { k: "D", t: "Stack many sine waves, each a different speed (frequency).", c: WAV },
        { k: "E", t: "Fast waves split nearby spots; slow waves separate far-apart ones.", c: POS },
        { k: "P", t: "Together the waves give every position its own smooth fingerprint.", c: OK },
        { k: "T", t: "PE(pos, i) = sin/cos( pos / 10000^(i/d) ) — geometric wavelengths.", c: MET },
      ]}
      foot="Bounded (−1…1), every position unique, distances consistent, and it extrapolates for free.">
      <div style={{ position: "absolute", left: 110, top: 250, width: 940, height: 520, borderRadius: 16,
        background: mix(T.bg1, WAV, 0.03), border: `2px solid ${mix(T.line, WAV, 0.4)}`, opacity: p(0.08, 0.18) }} />
      <WavePlot x={140} y={280} w={880} h={460} dims={WAVE_DIMS} reveal={reveal} colors={wcols} />
      {WAVE_DIMS.map((d, i) => (
        <div key={i} style={{ position: "absolute", left: 150, top: 292 + i * 30, fontFamily: MONO, fontSize: 18,
          color: wcols[i], opacity: p(0.24 + i * 0.05, 0.34 + i * 0.05) }}>
          dim {d} · {i === 0 ? "fastest" : i === WAVE_DIMS.length - 1 ? "slowest" : "faster"}
        </div>
      ))}
      <div style={{ position: "absolute", left: 140, top: 748, width: 880, textAlign: "center", fontFamily: MONO,
        fontSize: 18, color: T.muted, opacity: p(0.3, 0.4) }}>position 0 → {NPOS} →</div>
    </Teach>
  );
};

// ════════════════════════════════════════════ 8. THE HEATMAP (computed matrix)
const HeatmapScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur); const frame = useCurrentFrame();
  const reveal = p(0.2, 0.6);
  const hiPos = 6; // highlight one position's row
  const cell = 20, gx = 150, gy = 238; // 28 rows × (cell+2) must clear the Foot (y924)
  return (
    <Teach p={p} kicker="THE FAMOUS PICTURE" title="Every Position's Fingerprint" color={WAV}
      lines={[
        { k: "A", t: "Like a barcode — each row is one position's unique stripe pattern.", c: WAV },
        { k: "D", t: "Rows = positions (0→top). Columns = the sine/cosine dimensions.", c: TOK },
        { k: "E", t: "Read across one row: that's the exact vector we add to that word.", c: POS },
        { k: "P", t: "Neighbouring rows look similar; far-apart rows look different.", c: OK },
        { k: "T", t: "This is THE sinusoidal positional-encoding matrix.", c: MET },
      ]}
      foot="The model can recover 'how far apart' two tokens are from how similar their fingerprints are.">
      <PixGrid theme={T} g={PE255} x={gx} y={gy} cell={cell} reveal={reveal} tint={WAV} gap={2}
        hi={p(0.4, 0.5) > 0.5 ? { r: hiPos, c: 0, size: 1, color: POS } : null} />
      {/* highlight the whole row for one position */}
      {p(0.42, 0.52) > 0.3 && (
        <div style={{ position: "absolute", left: gx - 4, top: gy + hiPos * (cell + 2) - 4, width: DM * (cell + 2) + 4,
          height: cell + 8, border: `3px solid ${POS}`, borderRadius: 6, opacity: p(0.42, 0.52),
          boxShadow: `0 0 18px ${POS}` }} />
      )}
      <div style={{ position: "absolute", left: gx - 96, top: gy + hiPos * (cell + 2) - 2, fontFamily: MONO,
        fontWeight: 800, fontSize: 20, color: POS, opacity: p(0.44, 0.54) }}>pos {hiPos}</div>
      <div style={{ position: "absolute", left: gx, top: gy + NPOS * (cell + 2) + 12, width: DM * (cell + 2),
        textAlign: "center", fontFamily: MONO, fontSize: 18, color: T.muted, opacity: p(0.3, 0.4) }}>
        dimension 0 → {DM} (fast → slow) →
      </div>
      <div style={{ position: "absolute", left: gx - 132, top: gy, fontFamily: MONO, fontSize: 18, color: T.muted,
        opacity: p(0.3, 0.4), transform: "rotate(-90deg)", transformOrigin: "left top" }}>← position 0 → {NPOS}</div>
    </Teach>
  );
};

// ════════════════════════════════════════════ 9. ADDED → IT WORKS
const AddedScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur);
  const words = ["Dog", "bites", "man"];
  return (
    <Teach p={p} kicker="HOW IT'S USED" title="Add It In, and Order Appears" color={OK}
      lines={[
        { k: "A", t: "Like a timestamp sticker slapped on each word before it's read.", c: POS },
        { k: "D", t: "token vector + position vector → a position-aware input to attention.", c: TOK },
        { k: "E", t: "Now 'Dog bites man' and 'Man bites dog' give DIFFERENT attention.", c: OK },
        { k: "P", t: "The model can finally use order to work out who bit whom.", c: OK },
        { k: "T", t: "PE is added (not concatenated); the network learns to read it.", c: MET },
      ]}
      foot="One cheap addition turns an order-blind set-machine into a sequence model.">
      {/* the addition pipeline */}
      {words.map((w, i) => (
        <React.Fragment key={i}>
          <Tile x={150 + i * 290} y={270} label={w} c={TOK} w={190} o={p(0.06 + i * 0.03, 0.14 + i * 0.03)} sub="token" />
          <div style={{ position: "absolute", left: 150 + i * 290, top: 356, width: 190, textAlign: "center",
            fontFamily: MONO, fontWeight: 800, fontSize: 30, color: POS, opacity: p(0.2, 0.3) }}>＋ pos {i}</div>
          <Tile x={150 + i * 290} y={410} label={`${w}@${i}`} c={OK} w={190} o={p(0.24 + i * 0.03, 0.32 + i * 0.03)} sub="position-aware" />
        </React.Fragment>
      ))}
      {/* two orders → different attention */}
      <div style={{ position: "absolute", left: 150, top: 540, width: 860, fontFamily: MONO, fontWeight: 700,
        fontSize: 20, color: T.muted, opacity: p(0.5, 0.58) }}>WITH position · attention now differs by order</div>
      {[{ lbl: "Dog bites man", v: [0.7, 0.2, 0.1], c: WAV, at: 0.52 },
        { lbl: "Man bites dog", v: [0.1, 0.2, 0.7], c: POS, at: 0.62 }].map((r, ri) => (
        <div key={ri} style={{ position: "absolute", left: 150, top: 584 + ri * 96, width: 860, height: 80, borderRadius: 12,
          background: mix(T.panel, r.c, 0.06), border: `2px solid ${mix(T.line, r.c, 0.45)}`, display: "flex",
          alignItems: "center", gap: 20, padding: "0 22px", boxSizing: "border-box", opacity: p(r.at, r.at + 0.07) }}>
          <span style={{ fontFamily: SANS, fontWeight: 700, fontSize: 24, color: r.c, width: 260 }}>{r.lbl}</span>
          {r.v.map((val, k) => (
            <div key={k} style={{ height: 44, width: 120, borderRadius: 8, background: mix(T.panel, r.c, 0.1),
              border: `1.5px solid ${mix(T.line, r.c, 0.4)}`, position: "relative", overflow: "hidden" }}>
              <div style={{ position: "absolute", left: 0, top: 0, height: "100%", width: `${val * 100}%`,
                background: `linear-gradient(90deg, ${mix(r.c, T.bg1, 0.3)}, ${r.c})` }} />
            </div>
          ))}
        </div>
      ))}
    </Teach>
  );
};

// ════════════════════════════════════════════ 10. LEARNED EMBEDDINGS
const LearnedScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur);
  return (
    <Teach p={p} kicker="A SIMPLER COUSIN" title="Just Let the Model Learn Them" color={TOK}
      lines={[
        { k: "A", t: "Like memorising each seat's label instead of using a formula.", c: TOK },
        { k: "D", t: "A lookup table: one trainable vector per position, 0…max.", c: TOK },
        { k: "E", t: "BERT and GPT do exactly this — positions are parameters.", c: POS },
        { k: "P", t: "Flexible, but it only knows positions it saw in training.", c: BAD },
        { k: "T", t: "Learned absolute PE — no free extrapolation past max length.", c: MET },
      ]}
      foot="Sinusoids are fixed and extend forever; learned tables are flexible but capped. A classic trade-off.">
      {/* lookup table */}
      <div style={{ position: "absolute", left: 130, top: 258, fontFamily: MONO, fontWeight: 700, fontSize: 20,
        color: TOK, opacity: p(0.08, 0.18) }}>learned position table</div>
      {Array.from({ length: 6 }).map((_, r) => (
        <React.Fragment key={r}>
          <div style={{ position: "absolute", left: 130, top: 300 + r * 74, width: 90, height: 60, borderRadius: 8,
            background: mix(T.panel, POS, 0.14), border: `2px solid ${POS}`, display: "flex", alignItems: "center",
            justifyContent: "center", fontFamily: MONO, fontWeight: 800, fontSize: 22, color: POS,
            opacity: p(0.1 + r * 0.03, 0.2 + r * 0.03) }}>{r}</div>
          {Array.from({ length: 8 }).map((_, c) => (
            <div key={c} style={{ position: "absolute", left: 240 + c * 88, top: 300 + r * 74, width: 76, height: 60,
              borderRadius: 8, background: mix(T.panel, TOK, 0.06 + rnd(r, c, 3) * 0.4), border: `1px solid ${mix(T.line, TOK, 0.3)}`,
              opacity: p(0.12 + r * 0.03, 0.22 + r * 0.03) }} />
          ))}
        </React.Fragment>
      ))}
      <div style={{ position: "absolute", left: 130, top: 300 + 6 * 74 + 8, width: 850, fontFamily: SANS, fontSize: 22,
        color: BAD, opacity: p(0.6, 0.7) }}>
        position {"≥"} max_len was never trained → the model has no vector for it ✗
      </div>
    </Teach>
  );
};

// ════════════════════════════════════════════ 11. RELATIVE POSITION
const RelativeScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur);
  const words = ["the", "cat", "sat", "on", "mat"];
  return (
    <Teach p={p} kicker="A BETTER QUESTION" title="Distance, Not Address" color={POS}
      lines={[
        { k: "A", t: "At a table you care 'three seats to my left', not the absolute seat number.", c: POS },
        { k: "D", t: "Encode the GAP between two tokens (i − j), not their absolute spots.", c: TOK },
        { k: "E", t: "'cat' and 'mat' are 3 apart — true wherever the phrase appears.", c: OK },
        { k: "P", t: "The same pattern anywhere in the text is treated the same way.", c: OK },
        { k: "T", t: "Relative position encodings (T5-style) — fed into attention.", c: MET },
      ]}
      foot="This is what we really want — and it sets up the modern favourite: RoPE.">
      {words.map((w, i) => (
        <Tile key={i} x={130 + i * 180} y={300} label={w} c={TOK} w={160} o={p(0.06 + i * 0.03, 0.14 + i * 0.03)} sub={`pos ${i}`} />
      ))}
      {/* distance bracket from cat(1) to mat(4) */}
      {p(0.4, 0.5) > 0.2 && (
        <>
          <div style={{ position: "absolute", left: 130 + 1 * 180 + 80, top: 420, width: 3 * 180, height: 3,
            background: POS, opacity: p(0.4, 0.5) }} />
          <div style={{ position: "absolute", left: 130 + 1 * 180 + 80 + (3 * 180) / 2 - 130, top: 440, width: 260,
            textAlign: "center", fontFamily: MONO, fontWeight: 800, fontSize: 26, color: POS, opacity: p(0.44, 0.54) }}>
            gap = 4 − 1 = 3
          </div>
        </>
      )}
      <div style={{ position: "absolute", left: 130, top: 540, width: 900, fontFamily: SANS, fontSize: 24, color: T.text,
        opacity: p(0.6, 0.7), lineHeight: 1.4 }}>
        Whether the phrase starts at word 1 or word 100, the <span style={{ color: OK, fontWeight: 700 }}>gap of 3</span> is
        what the model should feel.
      </div>
    </Teach>
  );
};

// ════════════════════════════════════════════ 12. RoPE (computed rotation)
const RopeScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur);
  const cx = 400, cy = 520, Rr = 210;
  const reveal = p(0.2, 0.62);
  const nArrows = Math.round(interpolate(reveal, [0, 1], [0, 8]));
  const arrow = (pos: number, color: string, len = Rr, wdt = 3, op = 1) => {
    const a = -ropeAngle(pos); // negative = counter-clockwise up
    const x2 = cx + Math.cos(a) * len, y2 = cy + Math.sin(a) * len;
    return <line x1={cx} y1={cy} x2={x2} y2={y2} stroke={color} strokeWidth={wdt} opacity={op}
      markerEnd={`url(#rah${color.replace(/[^a-z0-9]/gi, "")})`} />;
  };
  return (
    <Teach p={p} kicker="THE MODERN DEFAULT" title="RoPE: Spin, Don't Add" color={WAV}
      lines={[
        { k: "A", t: "Like two dancers spinning — the ANGLE between them tells their gap.", c: WAV },
        { k: "D", t: "Rotate each word's vector by an angle set by its position.", c: TOK },
        { k: "E", t: "Compare two words: their dot product depends only on (m − n).", c: OK },
        { k: "P", t: "Absolute spin cancels; only the relative angle survives.", c: OK },
        { k: "T", t: "Rotary Position Embedding — used in Llama, GPT-NeoX, Qwen.", c: MET },
      ]}
      foot="Relative position, baked straight into the dot product — no vectors added, extends to long contexts.">
      <svg style={{ position: "absolute", left: 0, top: 0, overflow: "visible" }} width={1920} height={1080}>
        <defs>
          {[WAV, POS, T.muted].map((c) => (
            <marker key={c} id={`rah${c.replace(/[^a-z0-9]/gi, "")}`} markerWidth="9" markerHeight="9" refX="6" refY="3" orient="auto">
              <path d="M0,0 L6,3 L0,6 Z" fill={c} />
            </marker>
          ))}
        </defs>
        <circle cx={cx} cy={cy} r={Rr} fill="none" stroke={mix(T.line, WAV, 0.4)} strokeWidth={1.5} opacity={p(0.08, 0.18)} />
        {/* fan of positions */}
        {Array.from({ length: nArrows }).map((_, i) => arrow(i, mix(T.muted, WAV, i / 8), Rr, 2, 0.4))}
        {/* two highlighted vectors m, n */}
        {reveal > 0.5 && arrow(ROPE_N, POS, Rr, 4, 1)}
        {reveal > 0.5 && arrow(ROPE_M, WAV, Rr, 4, 1)}
      </svg>
      <div style={{ position: "absolute", left: cx - 40, top: cy + Rr + 18, fontFamily: MONO, fontSize: 18,
        color: T.muted, opacity: p(0.24, 0.34) }}>angle ∝ position</div>
      <div style={{ position: "absolute", left: cx + Rr + 30, top: cy - 60, fontFamily: MONO, fontWeight: 700,
        fontSize: 20, color: WAV, opacity: reveal > 0.5 ? p(0.5, 0.58) : 0 }}>word m · pos {ROPE_M}</div>
      <div style={{ position: "absolute", left: cx + Rr + 30, top: cy - 20, fontFamily: MONO, fontWeight: 700,
        fontSize: 20, color: POS, opacity: reveal > 0.5 ? p(0.5, 0.58) : 0 }}>word n · pos {ROPE_N}</div>
      {/* the dot-product readout */}
      <div style={{ position: "absolute", left: 720, top: 690, width: 360, height: 120, borderRadius: 14,
        background: mix(T.bg1, OK, 0.06), border: `2.5px solid ${mix(T.line, OK, 0.5)}`, padding: "16px 22px",
        boxSizing: "border-box", opacity: p(0.66, 0.76) }}>
        <div style={{ fontFamily: MONO, fontSize: 18, color: T.muted }}>q · k after rotation</div>
        <div style={{ fontFamily: MONO, fontWeight: 800, fontSize: 26, color: OK, marginTop: 6 }}>
          ∝ cos((m−n)·θ) = {ROPE_DDOT.toFixed(2)}
        </div>
        <div style={{ fontFamily: SANS, fontSize: 18, color: T.text, marginTop: 6 }}>depends only on the gap m−n</div>
      </div>
    </Teach>
  );
};

// ════════════════════════════════════════════ 13. RECAP
const RecapScene: React.FC<{ dur?: number; items?: string[]; closer?: string }> = ({ dur, items = [], closer = "" }) => {
  const p = useP(dur); const frame = useCurrentFrame();
  return (
    <Stage>
      <Bg theme={T} accent={WAV} />
      <div style={{ position: "absolute", left: 0, right: 0, top: 84, textAlign: "center" }}>
        <div style={{ fontFamily: MONO, fontWeight: 800, fontSize: 22, color: WAV, letterSpacing: 8,
          opacity: p(0.03, 0.12) }}>RECAP — THE WHOLE STORY</div>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 56, color: T.text, letterSpacing: -2,
          marginTop: 12, opacity: p(0.10, 0.22) }}>Positional Embeddings in One Breath</div>
      </div>
      <div style={{ position: "absolute", left: 150, top: 214, width: 1620 }}>
        {items.map((item, i) => {
          const at = 0.05 + i * 0.09;
          const lo = p(at, at + 0.06);
          return (
            <div key={i} style={{ display: "flex", alignItems: "center", gap: 18, marginBottom: 18, opacity: lo,
              transform: `translateX(${(1 - lo) * 20}px)` }}>
              <div style={{ width: 5, height: 34, borderRadius: 3, background: WAV, flexShrink: 0 }} />
              <div style={{ fontFamily: MONO, fontWeight: 800, fontSize: 20, color: WAV, width: 44, flexShrink: 0 }}>
                {String(i + 1).padStart(2, "0")}</div>
              <div style={{ fontFamily: SANS, fontSize: 25, color: T.text, lineHeight: 1.3, width: 1500 }}>{item}</div>
            </div>
          );
        })}
      </div>
      {closer && (
        <div style={{ position: "absolute", left: 130, bottom: 84, right: 130, textAlign: "center",
          fontFamily: SANS, fontStyle: "italic", fontSize: 36, color: WAV,
          textShadow: `0 0 40px ${mix(T.bg0, WAV, 0.6)}`, opacity: p(0.80, 0.90), lineHeight: 1.3 }}>{closer}</div>
      )}
      <div style={{ position: "absolute", left: 0, right: 0, top: 726, display: "flex", justifyContent: "center",
        gap: 16, opacity: 0.4 + Math.sin(frame * 0.05) * 0.15 }}>
        {STAGES.map((s, i) => (
          <div key={i} style={{ width: 120, borderRadius: 10, border: `2px solid ${MET}`, background: mix(T.panel, MET, 0.1),
            padding: "8px 0", textAlign: "center", fontFamily: MONO, fontWeight: 800, fontSize: 20, color: MET }}>{s.k}</div>
        ))}
      </div>
    </Stage>
  );
};

// ════════════════════════════════════════════ DISPATCHER
export const PEScene: React.FC<{ variant: string; [key: string]: unknown }> = ({ variant, ...rest }) => {
  const body = (() => {
    switch (variant) {
      case "pe_title":      return <TitleScene {...(rest as any)} />;
      case "pe_hook":       return <HookScene {...(rest as any)} />;
      case "pe_div":        return <DividerScene {...(rest as any)} />;
      case "pe_orderblind": return <OrderBlindScene {...(rest as any)} />;
      case "pe_tag":        return <TagScene {...(rest as any)} />;
      case "pe_naive":      return <NaiveScene {...(rest as any)} />;
      case "pe_sinusoid":   return <SinusoidScene {...(rest as any)} />;
      case "pe_heatmap":    return <HeatmapScene {...(rest as any)} />;
      case "pe_added":      return <AddedScene {...(rest as any)} />;
      case "pe_learned":    return <LearnedScene {...(rest as any)} />;
      case "pe_relative":   return <RelativeScene {...(rest as any)} />;
      case "pe_rope":       return <RopeScene {...(rest as any)} />;
      case "pe_recap":      return <RecapScene {...(rest as any)} />;
      default: return null;
    }
  })();
  if (!body) return null;
  return (<>{body}<SceneProgress dur={rest.dur as number | undefined} /></>);
};
