/**
 * KGScenes.tsx — "The Living Map: Ontology · Knowledge Graphs · Digital Twins · Agents".
 *
 * Thesis (skills/04 identity): five layers of ONE stack that give machines a world
 * they can understand AND act on, made concrete on a real multi-source Azure/ADO
 * project (six silos: ADO wiki, ADO repo, Azure SQL, Cosmos DB, Blob, AKS logs).
 *
 * Identity:
 *   theme accent = graph indigo (#6366F1)
 *   semantic colors (one per LAYER — the motif):
 *     ONT=amber (meaning) · KG=cyan (memory) · TWIN=violet (mirror) ·
 *     ENG=green (substrate) · AGENT=pink (motion) · BAD=red
 *   motif: the 5-layer stack (title/dividers) + a living node-graph with Flow.
 *
 * Every scene takes `dur` and phases with useP(dur) FRACTIONS; continuous motion in
 * every frame; computed visuals where the topic has a process (entity-resolution
 * merge, what-if cascade, GNN message passing, RCA traversal). Captions are ON, so
 * the takeaway strip sits at y=856 (clear of the caption band) and a SceneProgress
 * bar guarantees a "this is playing" signal. See skills/02,03,04,06,09.
 */
import React from "react";
import { AbsoluteFill, interpolate, useCurrentFrame } from "remotion";
import {
  makeTheme, mix, useP as usePfull, usePop, rnd, MONO, SANS, Theme,
  Bg, Stage, Kicker, Head, Card, Flow, Wire, Counter, Type, Brackets, ScanBeam,
} from "../lib/primitives";

// A/V-sync: narration front-loads names then elaborates. Compress reveals into the
// front REVEAL_SPAN so a visual lands ~when spoken; progress bar + continuous motion
// run the FULL beat (usePfull) so no frozen tail. See skills/02 "A/V-lag defect".
const REVEAL_SPAN = 0.64;
const useP = (dur?: unknown) => {
  const p = usePfull(dur);
  return (a: number, b: number) => p(Math.min(1, a * REVEAL_SPAN), Math.min(1, b * REVEAL_SPAN));
};

// Captions ON → takeaway strip higher (y=856, centered) to clear the caption pill.
const Foot: React.FC<{ theme?: Theme; p: number; children: React.ReactNode }> = ({ p, children }) => (
  <div style={{
    position: "absolute", left: 120, top: 856, right: 120, fontFamily: MONO, fontSize: 22,
    color: T.muted, opacity: p, lineHeight: 1.35, transform: `translateY(${(1 - p) * 12}px)`, textAlign: "center",
  }}>{children}</div>
);

// ---------------------------------------------------------------- identity
const T = makeTheme({ accent: "#6366F1", bg0: "#05060F", bg1: "#0A0C1A", bg2: "#11142A", panel: "#161A32" });
const A = {
  graph: "#818CF8", ont: "#FBBF24", kg: "#22D3EE", twin: "#A78BFA",
  eng: "#34D399", agent: "#F472B6", bad: "#F87171", ok: "#34D399", muted: "#8B93B0",
};

// The 5-layer stack (bottom → top). The recurring motif.
const LAYERS = [
  { key: "ONTOLOGY", role: "MEANING", c: A.ont, tech: "RDF · OWL · SHACL" },
  { key: "KNOWLEDGE GRAPH", role: "MEMORY", c: A.kg, tech: "Neo4j · SPARQL · GraphRAG" },
  { key: "DIGITAL TWIN", role: "MIRROR", c: A.twin, tech: "Azure DT · Ditto · USD" },
  { key: "GRAPH ENGINEERING", role: "SUBSTRATE", c: A.eng, tech: "SHACL · GQL · GNNs" },
  { key: "AGENTIC ENGINEERING", role: "MOTION", c: A.agent, tech: "LangGraph · MCP" },
];

// The six data silos of the running example.
const SOURCES = [
  { emoji: "📘", label: "ADO Wiki", sub: "architecture / design", c: A.ont },
  { emoji: "🗂️", label: "ADO Repo", sub: "report defs · SQL · code", c: A.kg },
  { emoji: "🗄️", label: "Azure SQL", sub: "relational business data", c: A.eng },
  { emoji: "🌐", label: "Cosmos DB", sub: "documents / JSON", c: A.twin },
  { emoji: "🖼️", label: "Blob Storage", sub: "images / assets", c: A.agent },
  { emoji: "📜", label: "AKS Logs", sub: "runtime events", c: A.bad },
];

// ---------------------------------------------------------------- small helpers
const Node: React.FC<{
  x: number; y: number; w?: number; h?: number; label: string; sub?: string; c: string;
  o?: number; emoji?: string; hot?: boolean; big?: boolean;
}> = ({ x, y, w = 232, h = 72, label, sub, c, o = 1, emoji, hot = false, big = false }) => {
  const frame = useCurrentFrame();
  return (
    <div style={{
      position: "absolute", left: x, top: y, width: w, height: h, borderRadius: 15,
      background: mix(T.panel, c, hot ? 0.26 : 0.11), border: `2.5px solid ${hot ? c : mix(T.line, c, 0.6)}`,
      display: "flex", alignItems: "center", gap: 12, padding: "0 16px", boxSizing: "border-box", opacity: o,
      transform: `translateY(${(1 - o) * 16}px) scale(${hot ? 1.05 : 1})`,
      boxShadow: hot ? `0 0 ${26 + Math.sin(frame * 0.1) * 8}px ${mix(T.bg0, c, 0.55)}` : "none",
    }}>
      {emoji && <span style={{ fontSize: big ? 34 : 27 }}>{emoji}</span>}
      <div style={{ minWidth: 0 }}>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: big ? 25 : 22, color: T.text, whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis", letterSpacing: -0.3 }}>{label}</div>
        {sub && <div style={{ fontFamily: MONO, fontSize: 17, color: mix(A.muted, c, 0.45), whiteSpace: "nowrap", marginTop: 2 }}>{sub}</div>}
      </div>
    </div>
  );
};

const Chip: React.FC<{ text: string; c: string; o?: number; hot?: boolean }> = ({ text, c, o = 1, hot }) => (
  <span style={{
    fontFamily: MONO, fontWeight: 700, fontSize: 22, color: hot ? T.bg0 : c,
    background: hot ? c : mix(T.panel, c, 0.14), border: `2px solid ${c}`, borderRadius: 999,
    padding: "9px 20px", opacity: o, whiteSpace: "nowrap",
  }}>{text}</span>
);

// ============================================================================ TITLE
const TitleScene: React.FC<{ dur?: number; title?: string; sub?: string; kicker?: string }> = ({
  dur, title = "The Living Map", sub = "ontology · knowledge graphs · digital twins · agentic engineering",
  kicker = "ENGINEERING A WORLD MACHINES CAN ACT ON",
}) => {
  const frame = useCurrentFrame();
  const p = usePfull(dur);
  const pop = usePop(dur);
  return (
    <AbsoluteFill style={{ alignItems: "center", justifyContent: "center" }}>
      {/* ambient: a slowly rotating ring of the 5 layer colors */}
      {Array.from({ length: 22 }).map((_, i) => {
        const ang = frame * 0.008 + (i / 22) * Math.PI * 2;
        const c = LAYERS[i % 5].c;
        return (
          <div key={i} style={{
            position: "absolute", left: 960 + Math.cos(ang) * (640 + (i % 3) * 26) - 5,
            top: 540 + Math.sin(ang) * (300 + (i % 3) * 14) - 5,
            width: 9, height: 9, borderRadius: 9, background: c,
            opacity: 0.2 + rnd(i, 3) * 0.3, boxShadow: `0 0 12px ${c}`,
          }} />
        );
      })}
      {/* motif: the 5-layer stack, faint, building on the left edge */}
      <div style={{ position: "absolute", left: 150, top: 300, opacity: p(0.3, 0.6) }}>
        {LAYERS.map((L, i) => (
          <div key={i} style={{
            width: 150, height: 66, marginBottom: 10, borderRadius: 10,
            background: mix(T.panel, L.c, 0.14), border: `2px solid ${mix(T.line, L.c, 0.6)}`,
            opacity: p(0.32 + i * 0.05, 0.4 + i * 0.05),
          }} />
        ))}
      </div>
      <div style={{ textAlign: "center", transform: `scale(${0.93 + pop(0) * 0.07})` }}>
        <div style={{ display: "flex", justifyContent: "center", marginBottom: 26 }}>
          <Kicker theme={T} text={kicker} cx />
        </div>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 128, lineHeight: 1.0, letterSpacing: -4, color: T.text }}>
          <div>The Living</div>
          <div style={{ color: A.graph, textShadow: `0 0 70px ${mix(T.bg0, A.graph, 0.7)}` }}>Map</div>
        </div>
        <div style={{ height: 5, width: interpolate(p(0.2, 0.5), [0, 1], [0, 620]), background: `linear-gradient(90deg, ${A.ont}, ${A.kg}, ${A.twin}, ${A.eng}, ${A.agent})`, borderRadius: 3, margin: "30px auto" }} />
        <div style={{ fontFamily: SANS, fontSize: 34, color: T.muted, opacity: p(0.3, 0.55), maxWidth: 1100 }}>{sub}</div>
      </div>
    </AbsoluteFill>
  );
};

// ============================================================================ DIVIDER
const Divider: React.FC<{ dur?: number; n?: number; title?: string; sub?: string; color?: string; layer?: number }> = ({
  dur, n = 1, title = "", sub = "", color = A.graph, layer = -1,
}) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  return (
    <Stage>
      <Brackets x={300} y={280} w={1320} h={520} color={color} o={p(0.02, 0.14)} len={54} />
      <ScanBeam theme={T} x={310} y={290} w={1300} h={500} color={color} o={p(0.05, 0.2)} speed={1.6} />
      {/* motif: the 5-layer stack with the active layer lit */}
      <div style={{ position: "absolute", left: 250, top: 336 }}>
        {LAYERS.slice().reverse().map((L, ri) => {
          const i = 4 - ri; const active = i === layer;
          return (
            <div key={i} style={{
              width: 250, height: 62, marginBottom: 9, borderRadius: 10, display: "flex", alignItems: "center", paddingLeft: 16, boxSizing: "border-box",
              background: mix(T.panel, L.c, active ? 0.28 : 0.08), border: `2px solid ${active ? L.c : mix(T.line, L.c, 0.4)}`,
              opacity: p(0.1 + ri * 0.04, 0.2 + ri * 0.04), transform: `scale(${active ? 1.04 : 1})`,
              boxShadow: active ? `0 0 24px ${mix(T.bg0, L.c, 0.5)}` : "none",
            }}>
              <span style={{ fontFamily: MONO, fontWeight: 700, fontSize: 16, color: active ? L.c : mix(A.muted, L.c, 0.3), letterSpacing: 1 }}>{L.role}</span>
            </div>
          );
        })}
      </div>
      <div style={{ position: "absolute", left: 560, top: 380, right: 240 }}>
        <div style={{ fontFamily: MONO, fontWeight: 800, fontSize: 32, color, letterSpacing: 10, opacity: p(0.06, 0.16) }}>PART {"0" + n}</div>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 84, color: T.text, letterSpacing: -2, marginTop: 16, opacity: p(0.14, 0.26), transform: `translateY(${(1 - p(0.14, 0.26)) * 26}px)` }}>{title}</div>
        <div style={{ height: 5, width: interpolate(p(0.22, 0.52), [0, 1], [0, 460]), background: color, borderRadius: 3, margin: "22px 0" }} />
        <div style={{ fontFamily: SANS, fontSize: 32, color: T.muted, opacity: p(0.32, 0.5), maxWidth: 900 }}>{sub}</div>
      </div>
      <div style={{ position: "absolute", left: 0, right: 0, top: 900, display: "flex", justifyContent: "center", gap: 16, opacity: p(0.34, 0.5) }}>
        {[1, 2, 3, 4, 5, 6].map((i) => (
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

// ============================================================================ STACK / ROADMAP
const StackScene: React.FC<{ dur?: number; foot?: string }> = ({ dur, foot }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const bandW = 1040, bx = 560, h = 106, gap = 16;
  const bottomTop = 812; // top y of the bottom-most band
  return (
    <Stage>
      <Head theme={T} kicker="THE WHOLE STACK · ONE IDEA" title="Five layers that give machines a world to act on" o={p(0, 0.06)} />
      {/* rising Flow through the spine — the same example travels up */}
      <Flow x1={bx - 34} y1={bottomTop + h} x2={bx - 34} y2={bottomTop - 4 * (h + gap)} color={A.graph} n={9} speed={0.012} o={p(0.5, 0.62)} />
      {LAYERS.map((L, i) => {
        const top = bottomTop - i * (h + gap);
        const at = 0.05 + i * 0.1;
        const o = p(at, at + 0.09);
        const hot = Math.floor(frame / 34) % 5 === i;
        return (
          <div key={i}>
            <div style={{
              position: "absolute", left: bx, top, width: bandW, height: h, borderRadius: 16,
              background: mix(T.panel, L.c, hot ? 0.2 : 0.1), border: `2.5px solid ${hot ? L.c : mix(T.line, L.c, 0.6)}`,
              opacity: o, transform: `translateX(${(1 - o) * 40}px)`, display: "flex", alignItems: "center", padding: "0 28px", boxSizing: "border-box",
              boxShadow: hot ? `0 0 34px ${mix(T.bg0, L.c, 0.4)}` : "none",
            }}>
              <div style={{ width: 130, fontFamily: MONO, fontWeight: 800, fontSize: 21, color: L.c, letterSpacing: 1 }}>{L.role}</div>
              <div style={{ flex: 1 }}>
                <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 30, color: T.text }}>{L.key}</div>
                <div style={{ fontFamily: MONO, fontSize: 18, color: A.muted, marginTop: 3 }}>{L.tech}</div>
              </div>
            </div>
            {/* left rail label: MEANING → MOTION arrow ladder */}
            <div style={{ position: "absolute", left: bx - 220, top: top + h / 2 - 15, fontFamily: MONO, fontSize: 20, color: L.c, opacity: p(at + 0.02, at + 0.1), fontWeight: 700 }}>
              {i === 0 ? "grammar" : i === 1 ? "living map" : i === 2 ? "live senses" : i === 3 ? "the body" : "the mind"}
            </div>
          </div>
        );
      })}
      <Foot p={p(0.82, 0.92)}>{foot || "Ontology → graph → twin → engineering → agents: build it bottom-up."}</Foot>
    </Stage>
  );
};

// ============================================================================ SILOS (the problem)
const SilosScene: React.FC<{ dur?: number; foot?: string }> = ({ dur, foot }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  // 3 top, 3 bottom around a central question
  const pos = [
    { x: 150, y: 236 }, { x: 844, y: 210 }, { x: 1538, y: 236 },
    { x: 150, y: 720 }, { x: 844, y: 746 }, { x: 1538, y: 720 },
  ];
  const cx = 960, cy = 500;
  return (
    <Stage>
      <Head theme={T} kicker="THE PROBLEM · ONE PROJECT, SIX SILOS" title="Your knowledge is scattered — and disconnected" color={A.bad} o={p(0, 0.06)} />
      {SOURCES.map((s, i) => {
        const at = 0.06 + i * 0.05;
        const o = p(at, at + 0.07);
        // faint, broken link toward the center (should be connected, isn't)
        const p1 = pos[i];
        return (
          <React.Fragment key={i}>
            <svg style={{ position: "absolute", left: 0, top: 0, overflow: "visible" }} width={1920} height={1080}>
              <line x1={p1.x + 116} y1={p1.y + 36} x2={cx + (p1.x < cx ? -180 : 180)} y2={cy + (p1.y < cy ? -60 : 90)}
                stroke={A.bad} strokeWidth={2} strokeDasharray="4 12" opacity={p(0.5, 0.7) * 0.5} strokeDashoffset={-frame * 1.2} />
            </svg>
            <Node x={p1.x} y={p1.y} w={232} h={78} label={s.label} sub={s.sub} c={s.c} emoji={s.emoji} o={o} big />
          </React.Fragment>
        );
      })}
      {/* central question */}
      <div style={{
        position: "absolute", left: cx - 250, top: cy - 66, width: 500, height: 150, borderRadius: 18,
        background: mix(T.panel, A.bad, 0.12), border: `2.5px solid ${A.bad}`, opacity: p(0.42, 0.54),
        display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center",
        boxShadow: `0 0 ${34 + Math.sin(frame * 0.08) * 12}px ${mix(T.bg0, A.bad, 0.4)}`,
      }}>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 30, color: T.text }}>“Report X is wrong — why?”</div>
        <div style={{ fontFamily: MONO, fontSize: 21, color: A.bad, marginTop: 10 }}>= 6 open tabs + 3 Slack pings</div>
      </div>
      <Foot p={p(0.82, 0.92)}>{foot || "Six systems. No shared meaning. Every answer is a manual scavenger hunt."}</Foot>
    </Stage>
  );
};

// ============================================================================ HOOK (thesis contrast)
const HookScene: React.FC<{ dur?: number; foot?: string }> = ({ dur, foot }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  return (
    <Stage>
      <Head theme={T} kicker="THE HINGE · THE WHOLE IDEA" title="Data answers ‘what’. A graph answers ‘so what’." color={A.graph} o={p(0, 0.06)} />
      {/* left: pile of disconnected rows (data) ; right: connected graph (meaning) */}
      <div style={{ position: "absolute", left: 150, top: 260, width: 700, opacity: p(0.08, 0.18) }}>
        <div style={{ fontFamily: MONO, fontWeight: 700, fontSize: 24, color: A.bad, marginBottom: 16 }}>DISCONNECTED DATA</div>
        {["orders.csv", "wiki/design.md", "pod-7f logs", "assets/9.png", "Q_sales.sql", "cosmos: users"].map((r, i) => (
          <div key={i} style={{ opacity: p(0.1 + i * 0.03, 0.18 + i * 0.03), fontFamily: MONO, fontSize: 23, color: T.muted, background: mix(T.panel, A.bad, 0.05), border: `1.5px solid ${T.line}`, borderRadius: 10, padding: "12px 18px", marginBottom: 10 }}>{r}</div>
        ))}
      </div>
      {/* arrow */}
      <div style={{ position: "absolute", left: 880, top: 470, fontFamily: SANS, fontWeight: 800, fontSize: 60, color: A.graph, opacity: p(0.4, 0.5) }}>→</div>
      {/* right: a tiny connected graph */}
      {(() => {
        const nodes = [
          { x: 1120, y: 300, l: "Report", c: A.agent }, { x: 1420, y: 300, l: "Query", c: A.kg },
          { x: 1580, y: 520, l: "Table", c: A.eng }, { x: 1360, y: 700, l: "Schema Δ", c: A.ont },
          { x: 1080, y: 560, l: "AKS error", c: A.bad },
        ];
        const edges = [[0, 1], [1, 2], [2, 3], [2, 4], [0, 4]];
        return (
          <>
            {edges.map(([a, b], i) => (
              <React.Fragment key={i}>
                <Wire x1={nodes[a].x + 70} y1={nodes[a].y + 26} x2={nodes[b].x + 70} y2={nodes[b].y + 26} p={p(0.3 + i * 0.05, 0.4 + i * 0.05)} color={A.graph} w={2.5} arrow={false} />
                <Flow x1={nodes[a].x + 70} y1={nodes[a].y + 26} x2={nodes[b].x + 70} y2={nodes[b].y + 26} color={A.graph} n={4} o={p(0.5, 0.62)} />
              </React.Fragment>
            ))}
            {nodes.map((n, i) => (
              <div key={i} style={{
                position: "absolute", left: n.x, top: n.y, width: 140, height: 54, borderRadius: 12,
                background: mix(T.panel, n.c, 0.16), border: `2.5px solid ${n.c}`, display: "flex", alignItems: "center", justifyContent: "center",
                opacity: p(0.28 + i * 0.04, 0.38 + i * 0.04), fontFamily: SANS, fontWeight: 800, fontSize: 21, color: T.text,
                boxShadow: Math.floor(frame / 30) % nodes.length === i ? `0 0 24px ${mix(T.bg0, n.c, 0.5)}` : "none",
              }}>{n.l}</div>
            ))}
          </>
        );
      })()}
      <Foot p={p(0.82, 0.92)}>{foot || "Meaning lives in the connections. Model those, and machines can reason — and act."}</Foot>
    </Stage>
  );
};

// ============================================================================ TRIPLE (RDF s-p-o)
const TripleScene: React.FC<{ dur?: number; kicker?: string; title?: string; subj?: string; pred?: string; obj?: string; examples?: string[]; foot?: string }> = ({
  dur, kicker = "THE ATOM OF MEANING", title = "Everything is a triple: subject → predicate → object",
  subj = "Report", pred = "USES", obj = "Query", examples = [], foot,
}) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const box = (x: number, l: string, c: string, o: number, tag: string) => (
    <div style={{ position: "absolute", left: x, top: 380, width: 340, height: 150, borderRadius: 20,
      background: mix(T.panel, c, 0.14), border: `3px solid ${c}`, display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", opacity: o,
      boxShadow: `0 0 30px ${mix(T.bg0, c, 0.3)}` }}>
      <div style={{ fontFamily: MONO, fontSize: 19, color: c, letterSpacing: 2 }}>{tag}</div>
      <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 46, color: T.text, marginTop: 8 }}>{l}</div>
    </div>
  );
  return (
    <Stage>
      <Head theme={T} kicker={kicker} title={title} color={A.ont} o={p(0, 0.06)} />
      {box(200, subj, A.ont, p(0.08, 0.18), "SUBJECT")}
      {box(790, pred, A.kg, p(0.2, 0.3), "PREDICATE")}
      {box(1380, obj, A.eng, p(0.32, 0.42), "OBJECT")}
      <Wire x1={540} y1={455} x2={790} y2={455} p={p(0.22, 0.3)} color={A.graph} w={3} />
      <Wire x1={1130} y1={455} x2={1380} y2={455} p={p(0.34, 0.42)} color={A.graph} w={3} />
      <Flow x1={540} y1={455} x2={1380} y2={455} color={A.graph} n={7} o={p(0.46, 0.58)} />
      {/* concrete examples from the project domain */}
      <div style={{ position: "absolute", left: 0, right: 0, top: 610, display: "flex", justifyContent: "center", gap: 18, flexWrap: "wrap", padding: "0 160px" }}>
        {examples.map((e, i) => (
          <div key={i} style={{ opacity: p(0.5 + i * 0.05, 0.6 + i * 0.05) }}>
            <Chip text={e} c={Math.floor(frame / 28) % Math.max(1, examples.length) === i ? A.graph : A.muted} hot={Math.floor(frame / 28) % Math.max(1, examples.length) === i} />
          </div>
        ))}
      </div>
      <Foot p={p(0.82, 0.92)}>{foot || "Millions of these triples, sharing vocabulary, become a graph of meaning."}</Foot>
    </Stage>
  );
};

// ============================================================================ COMPARE (A vs B)
type Col = { head: string; sub?: string; c: string; rows: string[] };
const CompareScene: React.FC<{ dur?: number; kicker?: string; title?: string; color?: string; left?: Col; right?: Col; foot?: string }> = ({
  dur, kicker = "", title = "", color = A.graph, left, right, foot,
}) => {
  const p = useP(dur);
  const L = left || { head: "A", c: A.kg, rows: [] };
  const R = right || { head: "B", c: A.twin, rows: [] };
  const col = (x: number, C: Col, base: number) => (
    <div style={{ position: "absolute", left: x, top: 250, width: 760 }}>
      <div style={{ opacity: p(base, base + 0.08), borderRadius: 18, background: mix(T.panel, C.c, 0.12), border: `2.5px solid ${C.c}`, padding: "18px 26px", marginBottom: 18 }}>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 34, color: C.c }}>{C.head}</div>
        {C.sub && <div style={{ fontFamily: MONO, fontSize: 20, color: A.muted, marginTop: 6 }}>{C.sub}</div>}
      </div>
      {C.rows.map((r, i) => {
        const at = base + 0.08 + i * 0.06; const o = p(at, at + 0.06);
        return (
          <div key={i} style={{ opacity: o, transform: `translateX(${(1 - o) * (x < 900 ? -24 : 24)}px)`, display: "flex", gap: 14, alignItems: "flex-start", background: mix(T.panel, C.c, 0.04), border: `1.5px solid ${T.line}`, borderLeft: `4px solid ${C.c}`, borderRadius: 12, padding: "14px 20px", marginBottom: 12 }}>
            <span style={{ color: C.c, fontFamily: MONO, fontWeight: 700, fontSize: 22, marginTop: 1 }}>▹</span>
            <span style={{ fontFamily: SANS, fontSize: 25, color: T.text, lineHeight: 1.3 }}>{r}</span>
          </div>
        );
      })}
    </div>
  );
  return (
    <Stage>
      <Head theme={T} kicker={kicker} title={title} color={color} o={p(0, 0.06)} />
      {col(130, L, 0.08)}
      <div style={{ position: "absolute", left: 942, top: 300, bottom: 200, width: 3, background: `linear-gradient(180deg, transparent, ${T.line}, transparent)` }} />
      {col(1030, R, 0.16)}
      {foot && <Foot p={p(0.82, 0.92)}>{foot}</Foot>}
    </Stage>
  );
};

// ============================================================================ CARDS (2-4 grid)
type CardT = { head: string; sub?: string; body?: string; tag?: string; emoji?: string };
const CardsScene: React.FC<{ dur?: number; kicker?: string; title?: string; color?: string; cards?: CardT[]; foot?: string }> = ({
  dur, kicker = "", title = "", color = A.graph, cards = [], foot,
}) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const n = cards.length;
  const cols = n <= 2 ? n : n === 3 ? 3 : 2;
  const rows = Math.ceil(n / cols);
  const cw = cols === 2 ? 790 : 520, gap = 40;
  const totalW = cols * cw + (cols - 1) * gap;
  const x0 = (1920 - totalW) / 2;
  // 2-row (4-card) grids must clear the Foot band at y=856: end by ~y800.
  const ch = rows === 1 ? 420 : 272, gy = rows === 1 ? 34 : 28;
  const y0 = rows === 1 ? 290 : 230;
  return (
    <Stage>
      <Head theme={T} kicker={kicker} title={title} color={color} o={p(0, 0.06)} />
      {cards.map((c, i) => {
        const r = Math.floor(i / cols), cc = i % cols;
        const x = x0 + cc * (cw + gap), y = y0 + r * (ch + gy);
        const at = 0.08 + i * 0.09; const o = p(at, at + 0.08);
        const hot = Math.floor(frame / 30) % n === i;
        return (
          <div key={i} style={{
            position: "absolute", left: x, top: y, width: cw, height: ch, borderRadius: 20,
            background: mix(T.panel, color, hot ? 0.16 : 0.08), border: `2.5px solid ${hot ? color : mix(T.line, color, 0.5)}`,
            opacity: o, transform: `translateY(${(1 - o) * 22}px)`, padding: "24px 30px", boxSizing: "border-box",
            boxShadow: hot ? `0 0 30px ${mix(T.bg0, color, 0.32)}` : "none",
          }}>
            <div style={{ display: "flex", alignItems: "center", gap: 14 }}>
              {c.emoji && <span style={{ fontSize: 40 }}>{c.emoji}</span>}
              <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 34, color: T.text }}>{c.head}</div>
            </div>
            {c.sub && <div style={{ fontFamily: MONO, fontSize: 20, color, marginTop: 8 }}>{c.sub}</div>}
            {c.body && <div style={{ fontFamily: SANS, fontSize: 24, color: T.muted, marginTop: 14, lineHeight: 1.4 }}>{c.body}</div>}
            {c.tag && <div style={{ position: "absolute", left: 30, bottom: 22 }}><Chip text={c.tag} c={color} /></div>}
          </div>
        );
      })}
      {foot && <Foot p={p(0.82, 0.92)}>{foot}</Foot>}
    </Stage>
  );
};

// ============================================================================ ORBIT (hub + items)
const OrbitScene: React.FC<{ dur?: number; kicker?: string; title?: string; color?: string; hub?: string; items?: { emoji?: string; label: string }[]; foot?: string }> = ({
  dur, kicker = "", title = "", color = A.graph, hub = "hub", items = [], foot,
}) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const cx = 960, cy = 560;
  return (
    <Stage>
      <Head theme={T} kicker={kicker} title={title} color={color} o={p(0, 0.06)} />
      {items.map((it, i) => {
        const ang = (i / items.length) * Math.PI * 2 - Math.PI / 2 + Math.sin(frame * 0.008) * 0.05;
        const x = cx + Math.cos(ang) * 600, y = cy + Math.sin(ang) * 268;
        const at = 0.1 + i * 0.06;
        const active = Math.floor(frame / 26) % items.length === i;
        return (
          <React.Fragment key={i}>
            <Wire x1={cx} y1={cy} x2={x} y2={y} p={p(at, at + 0.06)} color={active ? color : mix(A.muted, T.bg1, 0.4)} w={active ? 3 : 2} arrow={false} />
            {active && <Flow x1={cx} y1={cy} x2={x} y2={y} color={color} n={4} o={0.9} />}
            <div style={{
              position: "absolute", left: x - 158, top: y - 44, width: 316, height: 88, borderRadius: 16,
              background: mix(T.panel, active ? color : A.graph, active ? 0.2 : 0.08), border: `2.5px solid ${active ? color : mix(T.line, color, 0.5)}`,
              display: "flex", alignItems: "center", gap: 14, padding: "0 22px", boxSizing: "border-box",
              opacity: p(at, at + 0.08), transform: `scale(${active ? 1.07 : 1})`,
            }}>
              {it.emoji && <span style={{ fontSize: 38 }}>{it.emoji}</span>}
              <span style={{ fontFamily: SANS, fontWeight: 700, fontSize: 25, color: T.text, lineHeight: 1.15 }}>{it.label}</span>
            </div>
          </React.Fragment>
        );
      })}
      {/* hub */}
      <div style={{
        position: "absolute", left: cx - 130, top: cy - 66, width: 260, height: 132, borderRadius: 20,
        background: mix(T.panel, color, 0.2), border: `3px solid ${color}`, display: "flex", alignItems: "center", justifyContent: "center", textAlign: "center", padding: "0 18px", boxSizing: "border-box",
        opacity: p(0.06, 0.16), boxShadow: `0 0 ${40 + Math.sin(frame * 0.06) * 14}px ${mix(T.bg0, color, 0.4)}`,
      }}>
        <span style={{ fontFamily: SANS, fontWeight: 800, fontSize: 28, color: T.text }}>{hub}</span>
      </div>
      {foot && <Foot p={p(0.82, 0.92)}>{foot}</Foot>}
    </Stage>
  );
};

// ============================================================================ CODE / QUERY panel
const CodeScene: React.FC<{ dur?: number; kicker?: string; title?: string; color?: string; lang?: string; lines?: string[]; result?: string[]; caption?: string; foot?: string }> = ({
  dur, kicker = "", title = "", color = A.kg, lang = "cypher", lines = [], result = [], caption, foot,
}) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  return (
    <Stage>
      <Head theme={T} kicker={kicker} title={title} color={color} o={p(0, 0.06)} />
      {/* editor panel */}
      <div style={{ position: "absolute", left: 150, top: 250, width: result.length ? 1040 : 1620, minHeight: 460, borderRadius: 18, background: "#0b0e1c", border: `2.5px solid ${mix(T.line, color, 0.5)}`, padding: "22px 30px", boxSizing: "border-box", opacity: p(0.06, 0.16) }}>
        <div style={{ display: "flex", gap: 10, marginBottom: 18 }}>
          {[A.bad, A.ont, A.ok].map((c, i) => <div key={i} style={{ width: 14, height: 14, borderRadius: 8, background: c, opacity: 0.8 }} />)}
          <div style={{ marginLeft: 14, fontFamily: MONO, fontSize: 18, color: color, letterSpacing: 2 }}>{lang.toUpperCase()}</div>
        </div>
        {lines.map((ln, i) => {
          const at = 0.12 + i * (0.6 / Math.max(1, lines.length));
          const isKw = /^\s*(MATCH|WHERE|RETURN|CREATE|SELECT|PREFIX|CONSTRUCT|WITH|MERGE|sh:|a |@prefix|CALL)/.test(ln);
          return (
            <div key={i} style={{ fontFamily: MONO, fontSize: 24, lineHeight: 1.6, color: isKw ? color : "#c7d2e8", whiteSpace: "pre" }}>
              <Type text={ln} p={p(at, at + 0.5 / Math.max(1, lines.length))} color={isKw ? color : "#c7d2e8"} mono size={24} />
            </div>
          );
        })}
      </div>
      {/* result */}
      {result.length > 0 && (
        <div style={{ position: "absolute", left: 1230, top: 250, width: 540, minHeight: 460, borderRadius: 18, background: mix(T.panel, A.ok, 0.06), border: `2.5px solid ${mix(T.line, A.ok, 0.5)}`, padding: "22px 26px", boxSizing: "border-box", opacity: p(0.62, 0.72) }}>
          <div style={{ fontFamily: MONO, fontSize: 19, color: A.ok, letterSpacing: 2, marginBottom: 16 }}>→ RESULT</div>
          {result.map((r, i) => (
            <div key={i} style={{ opacity: p(0.66 + i * 0.04, 0.74 + i * 0.04), fontFamily: MONO, fontSize: 22, color: T.text, background: mix(T.panel, A.ok, 0.05), borderRadius: 8, padding: "10px 14px", marginBottom: 10 }}>{r}</div>
          ))}
        </div>
      )}
      {caption && <div style={{ position: "absolute", left: 150, top: 786, fontFamily: MONO, fontSize: 22, color: color, opacity: p(0.7, 0.8) }}>{caption}</div>}
      {foot && <Foot p={p(0.84, 0.93)}>{foot}</Foot>}
    </Stage>
  );
};

// ============================================================================ CHART (bars)
const ChartScene: React.FC<{ dur?: number; kicker?: string; title?: string; color?: string; bars?: { label: string; v: number; c: string; suffix?: string }[]; note?: string; foot?: string }> = ({
  dur, kicker = "", title = "", color = A.graph, bars = [], note, foot,
}) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const n = bars.length;
  const maxV = Math.max(...bars.map((b) => b.v), 1);
  const BW2 = 200, GAP = 120, SCALE = 380 / maxV;
  const totalW = n * BW2 + (n - 1) * GAP;
  const X0 = (1920 - totalW) / 2, Y0 = 770;
  return (
    <Stage>
      <Head theme={T} kicker={kicker} title={title} color={color} o={p(0, 0.06)} />
      {/* baseline */}
      <div style={{ position: "absolute", left: X0 - 40, top: Y0, width: totalW + 80, height: 3, background: T.line, opacity: p(0.05, 0.12) }} />
      {bars.map((b, i) => {
        const grow = p(0.12 + i * 0.12, 0.3 + i * 0.12);
        const h = b.v * SCALE * grow;
        const x = X0 + i * (BW2 + GAP);
        return (
          <div key={i}>
            <div style={{ position: "absolute", left: x, top: Y0 - h, width: BW2, height: h, borderRadius: "14px 14px 0 0",
              background: `linear-gradient(180deg, ${b.c}, ${mix(b.c, T.bg1, 0.5)})`, border: `2.5px solid ${b.c}`, borderBottom: "none",
              boxShadow: `0 0 ${20 + Math.sin(frame * 0.08 + i) * 8}px ${mix(T.bg0, b.c, 0.3)}` }} />
            <div style={{ position: "absolute", left: x - 30, top: Y0 - h - 58, width: BW2 + 60, textAlign: "center", opacity: grow }}>
              <Counter p={grow} to={b.v} suffix={b.suffix || "%"} color={b.c} size={48} />
            </div>
            <div style={{ position: "absolute", left: x - 30, top: Y0 + 18, width: BW2 + 60, textAlign: "center", fontFamily: SANS, fontWeight: 700, fontSize: 26, color: T.text, opacity: p(0.1 + i * 0.1, 0.2 + i * 0.1) }}>{b.label}</div>
          </div>
        );
      })}
      {note && <div style={{ position: "absolute", left: 0, right: 0, top: 208, textAlign: "center", fontFamily: SANS, fontSize: 30, color: color, opacity: p(0.5, 0.62) }}>{note}</div>}
      {foot && <Foot p={p(0.82, 0.92)}>{foot}</Foot>}
    </Stage>
  );
};

// ============================================================================ TOWER (maturity levels)
const TowerScene: React.FC<{ dur?: number; kicker?: string; title?: string; color?: string; levels?: { label: string; sub: string }[]; foot?: string }> = ({
  dur, kicker = "", title = "", color = A.twin, levels = [], foot,
}) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const n = levels.length;
  const h = 96, gap = 14, x = 430, w = 1060;
  const bottomTop = 300 + (n - 1) * (h + gap);
  const hot = Math.min(n - 1, Math.floor(p(0.5, 0.98) * n));
  return (
    <Stage>
      <Head theme={T} kicker={kicker} title={title} color={color} o={p(0, 0.06)} />
      {/* climbing arrow */}
      <div style={{ position: "absolute", left: x - 70, top: 300, bottom: 1080 - (bottomTop + h), width: 4, background: `linear-gradient(180deg, ${color}, ${mix(color, T.bg1, 0.6)})`, opacity: p(0.3, 0.42) }} />
      {levels.map((L, i) => {
        const top = bottomTop - i * (h + gap);
        const at = 0.08 + i * 0.11; const o = p(at, at + 0.09);
        const on = i <= hot;
        return (
          <div key={i} style={{
            position: "absolute", left: x, top, width: w, height: h, borderRadius: 14, display: "flex", alignItems: "center", gap: 22, padding: "0 26px", boxSizing: "border-box",
            background: mix(T.panel, color, on ? 0.18 : 0.06), border: `2.5px solid ${on ? color : mix(T.line, color, 0.4)}`,
            opacity: o, transform: `translateX(${(1 - o) * -30}px)`,
            boxShadow: i === hot ? `0 0 30px ${mix(T.bg0, color, 0.4)}` : "none",
          }}>
            <div style={{ fontFamily: MONO, fontWeight: 800, fontSize: 30, color, width: 44 }}>{i + 1}</div>
            <div>
              <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 30, color: T.text }}>{L.label}</div>
              <div style={{ fontFamily: MONO, fontSize: 19, color: A.muted, marginTop: 3 }}>{L.sub}</div>
            </div>
          </div>
        );
      })}
      {foot && <Foot p={p(0.82, 0.92)}>{foot}</Foot>}
    </Stage>
  );
};

// ============================================================================ PIPELINE (horizontal)
const PipelineScene: React.FC<{ dur?: number; kicker?: string; title?: string; color?: string; nodes?: { label: string; sub?: string; c?: string; emoji?: string }[]; foot?: string }> = ({
  dur, kicker = "", title = "", color = A.graph, nodes = [], foot,
}) => {
  const p = useP(dur);
  const n = nodes.length;
  const w = 260, gap = (1620 - n * w) / Math.max(1, n - 1);
  const y = 470;
  return (
    <Stage>
      <Head theme={T} kicker={kicker} title={title} color={color} o={p(0, 0.06)} />
      {nodes.map((nd, i) => {
        const x = 150 + i * (w + gap);
        const c = nd.c || color;
        const at = 0.08 + i * 0.13; const o = p(at, at + 0.09);
        return (
          <React.Fragment key={i}>
            {i > 0 && (
              <>
                <Wire x1={150 + (i - 1) * (w + gap) + w} y1={y + 55} x2={x - 4} y2={y + 55} p={p(at - 0.06, at)} color={c} w={3} />
                <Flow x1={150 + (i - 1) * (w + gap) + w} y1={y + 55} x2={x - 4} y2={y + 55} color={c} n={4} o={p(at + 0.02, at + 0.1)} />
              </>
            )}
            <div style={{ position: "absolute", left: x, top: y, width: w, height: 110, borderRadius: 18,
              background: mix(T.panel, c, 0.12), border: `2.5px solid ${c}`, opacity: o, transform: `translateY(${(1 - o) * 20}px)`,
              display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", padding: "0 14px", boxSizing: "border-box", textAlign: "center" }}>
              {nd.emoji && <span style={{ fontSize: 30, marginBottom: 4 }}>{nd.emoji}</span>}
              <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 25, color: T.text, whiteSpace: "nowrap" }}>{nd.label}</div>
              {nd.sub && <div style={{ fontFamily: MONO, fontSize: 16, color: mix(A.muted, c, 0.4), marginTop: 4, whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis", maxWidth: w - 24 }}>{nd.sub}</div>}
            </div>
          </React.Fragment>
        );
      })}
      {foot && <Foot p={p(0.82, 0.92)}>{foot}</Foot>}
    </Stage>
  );
};

// ============================================================================ INGEST (6 sources → 1 graph)
const IngestScene: React.FC<{ dur?: number; foot?: string }> = ({ dur, foot }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const connectors = ["LLM extract", "repo parse", "R2RML / Ontop", "doc → node", "blob metadata", "log parse"];
  // right-side unified graph
  const g = [
    { x: 1330, y: 250, l: "Project", c: A.graph }, { x: 1590, y: 340, l: "Report", c: A.agent },
    { x: 1290, y: 430, l: "Query", c: A.kg }, { x: 1560, y: 540, l: "Table", c: A.eng },
    { x: 1310, y: 640, l: "Service", c: A.twin }, { x: 1600, y: 720, l: "LogEvent", c: A.bad },
    { x: 1360, y: 810, l: "Asset", c: A.ont },
  ];
  const ge = [[0, 1], [1, 2], [2, 3], [0, 4], [4, 5], [0, 6], [3, 4]];
  return (
    <Stage>
      <Head theme={T} kicker="KNOWLEDGE GRAPH · CONSTRUCTION" title="Six connectors, one unified graph" color={A.kg} o={p(0, 0.06)} />
      {/* left source chips */}
      {SOURCES.map((s, i) => {
        const y = 214 + i * 106; const at = 0.06 + i * 0.05; const o = p(at, at + 0.06);
        return (
          <React.Fragment key={i}>
            <div style={{ position: "absolute", left: 130, top: y, width: 360, height: 84, borderRadius: 14, background: mix(T.panel, s.c, 0.1), border: `2px solid ${mix(T.line, s.c, 0.6)}`, opacity: o, display: "flex", alignItems: "center", gap: 12, padding: "0 16px", boxSizing: "border-box" }}>
              <span style={{ fontSize: 30 }}>{s.emoji}</span>
              <div>
                <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 22, color: T.text }}>{s.label}</div>
                <div style={{ fontFamily: MONO, fontSize: 17, color: s.c }}>{connectors[i]}</div>
              </div>
            </div>
            <Wire x1={490} y1={y + 42} x2={720} y2={512} p={p(at + 0.02, at + 0.1)} color={s.c} w={2} arrow={false} />
            <Flow x1={490} y1={y + 42} x2={720} y2={512} color={s.c} n={3} o={p(0.4, 0.55)} />
          </React.Fragment>
        );
      })}
      {/* builder */}
      <div style={{ position: "absolute", left: 700, top: 440, width: 240, height: 150, borderRadius: 18, background: mix(T.panel, A.kg, 0.18), border: `3px solid ${A.kg}`, display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", textAlign: "center", opacity: p(0.34, 0.44), boxShadow: `0 0 ${34 + Math.sin(frame * 0.07) * 12}px ${mix(T.bg0, A.kg, 0.4)}` }}>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 26, color: T.text }}>Graph Builder</div>
        <div style={{ fontFamily: MONO, fontSize: 18, color: A.kg, marginTop: 8 }}>extract · resolve · load</div>
      </div>
      <Wire x1={940} y1={515} x2={1250} y2={515} p={p(0.46, 0.56)} color={A.kg} w={3.5} />
      <Flow x1={940} y1={515} x2={1250} y2={515} color={A.kg} n={6} o={p(0.5, 0.62)} />
      {/* right graph */}
      {ge.map(([a, b], i) => (
        <React.Fragment key={i}>
          <Wire x1={g[a].x + 66} y1={g[a].y + 24} x2={g[b].x + 66} y2={g[b].y + 24} p={p(0.56 + i * 0.03, 0.64 + i * 0.03)} color={A.graph} w={2} arrow={false} />
          <Flow x1={g[a].x + 66} y1={g[a].y + 24} x2={g[b].x + 66} y2={g[b].y + 24} color={A.graph} n={3} o={p(0.7, 0.82)} />
        </React.Fragment>
      ))}
      {g.map((nd, i) => (
        <div key={i} style={{ position: "absolute", left: nd.x, top: nd.y, width: 132, height: 48, borderRadius: 11, background: mix(T.panel, nd.c, 0.18), border: `2.5px solid ${nd.c}`, display: "flex", alignItems: "center", justifyContent: "center", opacity: p(0.54 + i * 0.03, 0.62 + i * 0.03), fontFamily: SANS, fontWeight: 800, fontSize: 20, color: T.text, boxShadow: Math.floor(frame / 26) % g.length === i ? `0 0 20px ${mix(T.bg0, nd.c, 0.5)}` : "none" }}>{nd.l}</div>
      ))}
      <Foot p={p(0.84, 0.93)}>{foot || "Each silo keeps its home; the graph adds the connective tissue between them."}</Foot>
    </Stage>
  );
};

// ============================================================================ MERGE (entity resolution, computed)
const MergeScene: React.FC<{ dur?: number; foot?: string }> = ({ dur, foot }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const dups = [
    { l: '"orders"', src: "ADO wiki", c: A.ont, y: 280 },
    { l: "ORDERS", src: "Azure SQL", c: A.eng, y: 500 },
    { l: "OrderTbl", src: "ADO repo", c: A.kg, y: 720 },
  ];
  const mp = p(0.28, 0.7); // merge progress
  const tx = 1120, ty = 500; // merged target
  const merged = mp > 0.92;
  return (
    <Stage>
      <Head theme={T} kicker="KNOWLEDGE GRAPH · ENTITY RESOLUTION" title="The same thing, named three ways → one node" color={A.kg} o={p(0, 0.06)} />
      {dups.map((d, i) => {
        const sx = 300, sy = d.y;
        const x = sx + (tx - sx) * mp, y = sy + (ty - sy) * mp;
        const o = p(0.08 + i * 0.06, 0.18 + i * 0.06) * (merged ? 1 - Math.min(1, (mp - 0.92) / 0.08) : 1);
        return (
          <div key={i} style={{ position: "absolute", left: x, top: y, width: 240, height: 92, borderRadius: 14, background: mix(T.panel, d.c, 0.14), border: `2.5px solid ${d.c}`, opacity: o, display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center" }}>
            <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 28, color: T.text }}>{d.l}</div>
            <div style={{ fontFamily: MONO, fontSize: 18, color: d.c, marginTop: 4 }}>{d.src}</div>
          </div>
        );
      })}
      {/* merged node */}
      <div style={{ position: "absolute", left: tx - 20, top: ty - 20, width: 280, height: 132, borderRadius: 18, background: mix(T.panel, A.kg, 0.22), border: `3px solid ${A.kg}`, display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", opacity: merged ? p(0.7, 0.78) : mp * 0.4, boxShadow: `0 0 ${36 + Math.sin(frame * 0.08) * 12}px ${mix(T.bg0, A.kg, 0.45)}` }}>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 34, color: T.text }}>:Table Orders</div>
        <div style={{ fontFamily: MONO, fontSize: 19, color: A.kg, marginTop: 6 }}>{merged ? "1 canonical entity ✓" : "resolving…"}</div>
      </div>
      {/* +34% callout */}
      <div style={{ position: "absolute", left: 0, right: 0, top: 800, textAlign: "center", opacity: p(0.72, 0.82) }}>
        <span style={{ fontFamily: MONO, fontSize: 24, color: A.muted }}>entity resolution → query accuracy </span>
        <Counter p={p(0.74, 0.9)} to={34} prefix="+" suffix="%" color={A.ok} size={40} />
      </div>
      <Foot p={p(0.86, 0.94)}>{foot || "Match keys across sources, collapse duplicates — meaning stays consistent everywhere."}</Foot>
    </Stage>
  );
};

// ============================================================================ TELEMETRY (live twin)
const TelemetryScene: React.FC<{ dur?: number; foot?: string }> = ({ dur, foot }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  // small service graph; health flips over time (computed from frame)
  const nodes = [
    { x: 360, y: 320, l: "api-gateway" }, { x: 760, y: 250, l: "orders-svc" }, { x: 1180, y: 300, l: "reports-svc" },
    { x: 560, y: 560, l: "sql-pool" }, { x: 1000, y: 600, l: "cosmos" }, { x: 1420, y: 540, l: "aks-pod-7f" },
  ];
  const edges = [[0, 1], [1, 3], [1, 4], [2, 4], [0, 2], [2, 5]];
  const health = (i: number) => {
    const s = (Math.sin(frame * 0.03 + i * 1.3) + 1) / 2;
    return s > 0.72 ? A.bad : s > 0.4 ? A.ont : A.ok;
  };
  return (
    <Stage>
      <Head theme={T} kicker="DIGITAL TWIN · LIVE SYNC" title="Telemetry keeps the graph honest, second by second" color={A.twin} o={p(0, 0.06)} />
      {edges.map(([a, b], i) => (
        <React.Fragment key={i}>
          <Wire x1={nodes[a].x + 80} y1={nodes[a].y + 30} x2={nodes[b].x + 80} y2={nodes[b].y + 30} p={p(0.1 + i * 0.03, 0.2 + i * 0.03)} color={A.twin} w={2} arrow={false} />
          <Flow x1={nodes[a].x + 80} y1={nodes[a].y + 30} x2={nodes[b].x + 80} y2={nodes[b].y + 30} color={A.twin} n={4} o={p(0.32, 0.46)} />
        </React.Fragment>
      ))}
      {nodes.map((nd, i) => {
        const c = health(i);
        return (
          <div key={i} style={{ position: "absolute", left: nd.x, top: nd.y, width: 160, height: 60, borderRadius: 13, background: mix(T.panel, c, 0.16), border: `2.5px solid ${c}`, display: "flex", alignItems: "center", justifyContent: "center", gap: 10, opacity: p(0.08 + i * 0.04, 0.18 + i * 0.04), boxShadow: c === A.bad ? `0 0 ${20 + Math.sin(frame * 0.3) * 10}px ${mix(T.bg0, c, 0.5)}` : "none" }}>
            <div style={{ width: 12, height: 12, borderRadius: 8, background: c, boxShadow: `0 0 10px ${c}` }} />
            <span style={{ fontFamily: MONO, fontWeight: 700, fontSize: 21, color: T.text }}>{nd.l}</span>
          </div>
        );
      })}
      {/* live clock chip */}
      <div style={{ position: "absolute", left: 1480, top: 250, fontFamily: MONO, fontSize: 22, color: A.twin, opacity: p(0.5, 0.6) }}>
        ⟳ live · {String(10 + Math.floor(frame / 30) % 50).padStart(2, "0")}s ago
      </div>
      <Foot p={p(0.82, 0.92)}>{foot || "A model that mirrors reality now, not a diagram from last quarter."}</Foot>
    </Stage>
  );
};

// ============================================================================ CASCADE (what-if, computed BFS)
const CascadeScene: React.FC<{ dur?: number; foot?: string }> = ({ dur, foot }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  // dependency DAG: column → table → 2 queries → 3 reports
  const nodes = [
    { id: 0, x: 150, y: 470, l: "orders.region", t: "COLUMN", c: A.ont, depth: 0 },
    { id: 1, x: 520, y: 470, l: ":Table Orders", t: "TABLE", c: A.eng, depth: 1 },
    { id: 2, x: 900, y: 320, l: "Q_sales_by_region", t: "QUERY", c: A.kg, depth: 2 },
    { id: 3, x: 900, y: 620, l: "Q_region_map", t: "QUERY", c: A.kg, depth: 2 },
    { id: 4, x: 1330, y: 250, l: "Regional Sales", t: "REPORT", c: A.agent, depth: 3 },
    { id: 5, x: 1330, y: 430, l: "Exec Dashboard", t: "REPORT", c: A.agent, depth: 3 },
    { id: 6, x: 1330, y: 640, l: "Ops Heatmap", t: "REPORT", c: A.agent, depth: 3 },
  ];
  const edges = [[0, 1], [1, 2], [1, 3], [2, 4], [2, 5], [3, 6]];
  const wave = p(0.35, 0.95) * 3.4; // impact front by depth
  const impacted = (d: number) => wave >= d;
  return (
    <Stage>
      <Head theme={T} kicker="DIGITAL TWIN · SIMULATION" title="“Drop this column — what breaks?”" color={A.twin} o={p(0, 0.06)} />
      {edges.map(([a, b], i) => {
        const on = impacted(nodes[b].depth);
        return (
          <React.Fragment key={i}>
            <Wire x1={nodes[a].x + 150} y1={nodes[a].y + 34} x2={nodes[b].x - 4} y2={nodes[b].y + 34} p={p(0.1 + i * 0.03, 0.2 + i * 0.03)} color={on ? A.bad : mix(A.muted, T.bg1, 0.3)} w={on ? 3 : 2} />
            {on && <Flow x1={nodes[a].x + 150} y1={nodes[a].y + 34} x2={nodes[b].x - 4} y2={nodes[b].y + 34} color={A.bad} n={4} o={0.9} />}
          </React.Fragment>
        );
      })}
      {nodes.map((nd) => {
        const on = impacted(nd.depth);
        const c = on ? A.bad : nd.c;
        return (
          <div key={nd.id} style={{ position: "absolute", left: nd.x, top: nd.y, width: 300, height: 68, borderRadius: 13, background: mix(T.panel, c, on ? 0.2 : 0.09), border: `2.5px solid ${on ? c : mix(T.line, c, 0.6)}`, display: "flex", flexDirection: "column", justifyContent: "center", padding: "0 18px", boxSizing: "border-box", opacity: p(0.06 + nd.depth * 0.05, 0.16 + nd.depth * 0.05), boxShadow: on ? `0 0 ${18 + Math.sin(frame * 0.2) * 8}px ${mix(T.bg0, c, 0.5)}` : "none" }}>
            <div style={{ fontFamily: MONO, fontSize: 15, color: c, letterSpacing: 1 }}>{nd.t}{on ? " · BREAKS" : ""}</div>
            <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 23, color: T.text }}>{nd.l}</div>
          </div>
        );
      })}
      <div style={{ position: "absolute", left: 0, right: 0, top: 800, textAlign: "center", opacity: p(0.72, 0.82), fontFamily: SANS, fontWeight: 800, fontSize: 28, color: A.bad }}>
        3 reports impacted — before you ship the change
      </div>
      <Foot p={p(0.86, 0.94)}>{foot || "Simulate the blast radius on the twin instead of discovering it in production."}</Foot>
    </Stage>
  );
};

// ============================================================================ GNN (message passing, computed)
const GnnScene: React.FC<{ dur?: number; foot?: string }> = ({ dur, foot }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const nodes = [
    { x: 760, y: 280 }, { x: 1060, y: 300 }, { x: 620, y: 500 }, { x: 900, y: 540 },
    { x: 1220, y: 520 }, { x: 760, y: 730 }, { x: 1080, y: 720 },
  ];
  const edges = [[0, 1], [0, 2], [0, 3], [1, 4], [3, 4], [2, 5], [3, 5], [4, 6], [5, 6]];
  const hop = Math.min(3, Math.floor(p(0.3, 0.95) * 4));
  // node "embedding" hue spreads by hop from a seed node 0
  const dist: number[] = nodes.map(() => 9);
  dist[0] = 0;
  for (let k = 0; k < 3; k++) edges.forEach(([a, b]) => { dist[b] = Math.min(dist[b], dist[a] + 1); dist[a] = Math.min(dist[a], dist[b] + 1); });
  return (
    <Stage>
      <Head theme={T} kicker="GRAPH ENGINEERING · GRAPH ML" title="GNNs: a node learns from its neighborhood" color={A.eng} o={p(0, 0.06)} />
      {edges.map(([a, b], i) => (
        <React.Fragment key={i}>
          <Wire x1={nodes[a].x + 30} y1={nodes[a].y + 30} x2={nodes[b].x + 30} y2={nodes[b].y + 30} p={p(0.08 + i * 0.02, 0.16 + i * 0.02)} color={mix(A.eng, T.bg1, 0.3)} w={2} arrow={false} />
          {dist[a] < hop && dist[b] <= hop && <Flow x1={nodes[a].x + 30} y1={nodes[a].y + 30} x2={nodes[b].x + 30} y2={nodes[b].y + 30} color={A.eng} n={3} o={0.85} />}
        </React.Fragment>
      ))}
      {nodes.map((nd, i) => {
        const reached = dist[i] <= hop;
        const c = i === 0 ? A.agent : reached ? A.eng : mix(A.muted, T.bg1, 0.3);
        return (
          <div key={i} style={{ position: "absolute", left: nd.x, top: nd.y, width: 60, height: 60, borderRadius: 40, background: mix(T.panel, c, reached ? 0.4 : 0.1), border: `3px solid ${c}`, opacity: p(0.06, 0.16), transform: `scale(${reached ? 1.15 : 1})`, boxShadow: reached ? `0 0 ${18 + Math.sin(frame * 0.1 + i) * 8}px ${mix(T.bg0, c, 0.5)}` : "none" }} />
        );
      })}
      <div style={{ position: "absolute", left: 1420, top: 300, width: 360, opacity: p(0.5, 0.62) }}>
        <div style={{ fontFamily: MONO, fontSize: 22, color: A.eng, marginBottom: 10 }}>hop = {hop}</div>
        <div style={{ fontFamily: SANS, fontSize: 24, color: T.muted, lineHeight: 1.4 }}>Each layer aggregates one more ring of neighbors — powering link prediction, fraud & recommendations.</div>
      </div>
      <Foot p={p(0.82, 0.92)}>{foot || "Uber ETAs, Pinterest recs, fraud rings — all learned on the graph structure itself."}</Foot>
    </Stage>
  );
};

// ============================================================================ AGENT LOOP
const AgentLoopScene: React.FC<{ dur?: number; foot?: string }> = ({ dur, foot }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const steps = [
    { l: "OBSERVE", sub: "read the graph + twin", c: A.kg, x: 960, y: 250 },
    { l: "REASON", sub: "multi-hop over meaning", c: A.twin, x: 1360, y: 620 },
    { l: "ACT", sub: "typed, governed action", c: A.agent, x: 560, y: 620 },
  ];
  const active = Math.floor(frame / 34) % 3;
  return (
    <Stage>
      <Head theme={T} kicker="AGENTIC ENGINEERING · THE LOOP" title="Observe → reason → act, grounded on the graph" color={A.agent} o={p(0, 0.06)} />
      {/* central graph */}
      <div style={{ position: "absolute", left: 860, top: 470, width: 200, height: 200, borderRadius: 120, background: mix(T.panel, A.graph, 0.14), border: `3px dashed ${A.graph}`, display: "flex", alignItems: "center", justifyContent: "center", opacity: p(0.1, 0.2), transform: `rotate(${frame * 0.3}deg)` }}>
        <span style={{ fontFamily: SANS, fontWeight: 800, fontSize: 26, color: A.graph, transform: `rotate(${-frame * 0.3}deg)` }}>world<br />model</span>
      </div>
      {steps.map((s, i) => {
        const nx = steps[(i + 1) % 3];
        return (
          <React.Fragment key={i}>
            <Wire x1={s.x + 130} y1={s.y + 55} x2={nx.x + 130} y2={nx.y + 55} p={p(0.12 + i * 0.06, 0.22 + i * 0.06)} curve={90} color={active === i ? s.c : mix(A.muted, T.bg1, 0.4)} w={active === i ? 3.5 : 2} />
            <div style={{ position: "absolute", left: s.x, top: s.y, width: 300, height: 116, borderRadius: 18, background: mix(T.panel, s.c, active === i ? 0.22 : 0.1), border: `2.5px solid ${s.c}`, display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", opacity: p(0.08 + i * 0.06, 0.18 + i * 0.06), transform: `scale(${active === i ? 1.06 : 1})`, boxShadow: active === i ? `0 0 34px ${mix(T.bg0, s.c, 0.4)}` : "none" }}>
              <div style={{ fontFamily: MONO, fontWeight: 800, fontSize: 30, color: s.c, letterSpacing: 3 }}>{s.l}</div>
              <div style={{ fontFamily: SANS, fontSize: 22, color: T.muted, marginTop: 6 }}>{s.sub}</div>
            </div>
          </React.Fragment>
        );
      })}
      <Foot p={p(0.82, 0.92)}>{foot || "The graph is the agent's memory, its senses, and its list of safe things to do."}</Foot>
    </Stage>
  );
};

// ============================================================================ TWO-BRAIN (neuro-symbolic)
const TwoBrainScene: React.FC<{ dur?: number; foot?: string }> = ({ dur, foot }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const flip = Math.floor(frame / 40) % 2 === 0;
  return (
    <Stage>
      <Head theme={T} kicker="AGENTIC ENGINEERING · NEURO-SYMBOLIC" title="LLM proposes. The ontology verifies." color={A.agent} o={p(0, 0.06)} />
      {/* left: LLM */}
      <div style={{ position: "absolute", left: 170, top: 300, width: 560, height: 300, borderRadius: 22, background: mix(T.panel, A.agent, 0.12), border: `2.5px solid ${A.agent}`, opacity: p(0.08, 0.18), padding: "26px 30px", boxSizing: "border-box" }}>
        <div style={{ fontFamily: MONO, fontSize: 20, color: A.agent, letterSpacing: 2 }}>🧠 LLM · PROPOSE</div>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 30, color: T.text, marginTop: 14 }}>flexible, fluent, fast</div>
        <div style={{ fontFamily: SANS, fontSize: 23, color: T.muted, marginTop: 14, lineHeight: 1.4 }}>Reads language, spots patterns, drafts a candidate answer or action.</div>
        <div style={{ fontFamily: MONO, fontSize: 20, color: A.bad, marginTop: 18 }}>⚠ can hallucinate</div>
      </div>
      {/* right: symbolic */}
      <div style={{ position: "absolute", left: 1190, top: 300, width: 560, height: 300, borderRadius: 22, background: mix(T.panel, A.eng, 0.12), border: `2.5px solid ${A.eng}`, opacity: p(0.2, 0.3), padding: "26px 30px", boxSizing: "border-box" }}>
        <div style={{ fontFamily: MONO, fontSize: 20, color: A.eng, letterSpacing: 2 }}>⚖ SHACL / REASONER · VERIFY</div>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 30, color: T.text, marginTop: 14 }}>strict, consistent, auditable</div>
        <div style={{ fontFamily: SANS, fontSize: 23, color: T.muted, marginTop: 14, lineHeight: 1.4 }}>Checks the draft against the ontology's rules before it is allowed to act.</div>
        <div style={{ fontFamily: MONO, fontSize: 20, color: A.ok, marginTop: 18 }}>✓ provably valid</div>
      </div>
      {/* candidate flowing across, stamped */}
      <Wire x1={730} y1={450} x2={1190} y2={450} p={p(0.34, 0.46)} color={A.graph} w={3} />
      <Flow x1={730} y1={450} x2={1190} y2={450} color={A.graph} n={5} o={p(0.48, 0.6)} />
      <div style={{ position: "absolute", left: 900, top: 410, fontFamily: MONO, fontSize: 22, color: flip ? A.ont : A.ok, opacity: p(0.5, 0.6) }}>{flip ? "candidate…" : "✓ passes"}</div>
      <Foot p={p(0.82, 0.92)}>{foot || "Creativity from the model, guarantees from the graph — that pairing is trustworthy AI."}</Foot>
    </Stage>
  );
};

// ============================================================================ TRAVERSE (RCA payoff, computed path)
const TraverseScene: React.FC<{ dur?: number; foot?: string }> = ({ dur, foot }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  // ordered root-cause path the agent walks
  const path = [
    { x: 150, y: 250, l: "Report X", sub: "wrong numbers", c: A.agent },
    { x: 470, y: 250, l: "Q_sales.sql", sub: "USES", c: A.kg },
    { x: 790, y: 250, l: ":Table Orders", sub: "READS", c: A.eng },
    { x: 790, y: 470, l: "Schema Δ", sub: "column renamed · 09:14", c: A.ont },
    { x: 470, y: 470, l: "AKS error", sub: "null region · pod-7f", c: A.bad },
    { x: 150, y: 470, l: "ROOT CAUSE", sub: "breaking migration #482", c: A.bad },
    { x: 470, y: 690, l: "ACTION", sub: "opened ADO work item → owner", c: A.ok },
  ];
  const seg = [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 6]];
  const walk = p(0.2, 0.9) * seg.length;
  const litNode = (i: number) => walk >= i - 0.0; // node i lit once walk passes
  return (
    <Stage>
      <Head theme={T} kicker="THE PAYOFF · AUTONOMOUS ROOT-CAUSE" title="One question. The agent walks the graph." color={A.agent} o={p(0, 0.06)} />
      {seg.map(([a, b], i) => {
        const on = walk >= i + 0.5;
        return (
          <React.Fragment key={i}>
            <Wire x1={path[a].x + 130} y1={path[a].y + 45} x2={path[b].x + 130} y2={path[b].y + 45} p={interpolate(walk, [i, i + 1], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" })} color={on ? path[b].c : mix(A.muted, T.bg1, 0.4)} w={3.5} />
            {on && <Flow x1={path[a].x + 130} y1={path[a].y + 45} x2={path[b].x + 130} y2={path[b].y + 45} color={path[b].c} n={4} o={0.9} />}
          </React.Fragment>
        );
      })}
      {path.map((nd, i) => {
        const on = litNode(i);
        return (
          <div key={i} style={{ position: "absolute", left: nd.x, top: nd.y, width: 300, height: 92, borderRadius: 15, background: mix(T.panel, nd.c, on ? 0.2 : 0.07), border: `2.5px solid ${on ? nd.c : mix(T.line, nd.c, 0.4)}`, display: "flex", flexDirection: "column", justifyContent: "center", padding: "0 20px", boxSizing: "border-box", opacity: p(0.06, 0.16), transform: `scale(${Math.abs(walk - (i + 0.2)) < 0.6 ? 1.05 : 1})`, boxShadow: on ? `0 0 ${20 + Math.sin(frame * 0.12 + i) * 8}px ${mix(T.bg0, nd.c, 0.45)}` : "none" }}>
            <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 26, color: T.text }}>{nd.l}</div>
            <div style={{ fontFamily: MONO, fontSize: 18, color: nd.c, marginTop: 3 }}>{nd.sub}</div>
          </div>
        );
      })}
      {/* stat panel */}
      <div style={{ position: "absolute", left: 1150, top: 470, width: 620, height: 300, borderRadius: 20, background: mix(T.panel, A.ok, 0.08), border: `2.5px solid ${mix(T.line, A.ok, 0.5)}`, opacity: p(0.6, 0.72), padding: "26px 32px", boxSizing: "border-box" }}>
        <div style={{ fontFamily: MONO, fontSize: 20, color: A.ok, letterSpacing: 2 }}>WHAT CHANGED</div>
        <div style={{ display: "flex", alignItems: "baseline", gap: 16, marginTop: 16 }}>
          <span style={{ fontFamily: SANS, fontSize: 24, color: T.muted }}>RCA accuracy (F1)</span>
          <span style={{ fontFamily: MONO, fontWeight: 800, fontSize: 40, color: A.muted }}>0.61</span>
          <span style={{ fontFamily: SANS, fontSize: 30, color: A.ok }}>→</span>
          <span style={{ fontFamily: MONO, fontWeight: 800, fontSize: 44, color: A.ok, fontVariantNumeric: "tabular-nums" }}>
            {(0.61 + 0.30 * Math.max(0, Math.min(1, p(0.72, 0.88)))).toFixed(2)}
          </span>
        </div>
        <div style={{ fontFamily: SANS, fontSize: 24, color: T.text, marginTop: 18, lineHeight: 1.4 }}>Six tabs and three Slack pings → <span style={{ color: A.ok, fontWeight: 800 }}>~2 minutes</span>, with an audit trail.</div>
      </div>
      <Foot p={p(0.86, 0.94)}>{foot || "Retrieve on the graph, reason over the path, act through a governed tool. That's the whole video."}</Foot>
    </Stage>
  );
};

// ============================================================================ ARCHITECTURE (capstone)
const ArchitectureScene: React.FC<{ dur?: number; foot?: string }> = ({ dur, foot }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const bandW = 900, bx = 510, h = 92, gap = 12;
  const bottomTop = 780;
  return (
    <Stage>
      <Head theme={T} kicker="THE WHOLE ARCHITECTURE" title="Sources in at the bottom, action out at the top" color={A.graph} o={p(0, 0.06)} />
      {/* six sources feeding the bottom */}
      {SOURCES.map((s, i) => {
        const x = 130 + i * 62;
        return (
          <React.Fragment key={i}>
            <div style={{ position: "absolute", left: 130, top: 300 + i * 90, width: 300, height: 74, borderRadius: 12, background: mix(T.panel, s.c, 0.1), border: `2px solid ${mix(T.line, s.c, 0.6)}`, display: "flex", alignItems: "center", gap: 10, padding: "0 14px", boxSizing: "border-box", opacity: p(0.06 + i * 0.03, 0.16 + i * 0.03) }}>
              <span style={{ fontSize: 26 }}>{s.emoji}</span>
              <span style={{ fontFamily: SANS, fontWeight: 700, fontSize: 21, color: T.text }}>{s.label}</span>
            </div>
            <Wire x1={430} y1={337 + i * 90} x2={bx - 4} y2={bottomTop + 46} p={p(0.2 + i * 0.02, 0.3 + i * 0.02)} color={s.c} w={1.8} arrow={false} />
            <Flow x1={430} y1={337 + i * 90} x2={bx - 4} y2={bottomTop + 46} color={s.c} n={2} o={p(0.34, 0.46)} />
          </React.Fragment>
        );
      })}
      {/* the 5 layer bands */}
      {LAYERS.map((L, i) => {
        const top = bottomTop - i * (h + gap);
        const at = 0.3 + i * 0.08; const o = p(at, at + 0.08);
        return (
          <div key={i} style={{ position: "absolute", left: bx, top, width: bandW, height: h, borderRadius: 14, background: mix(T.panel, L.c, 0.12), border: `2.5px solid ${L.c}`, display: "flex", alignItems: "center", padding: "0 26px", boxSizing: "border-box", opacity: o, transform: `translateX(${(1 - o) * 30}px)` }}>
            <div style={{ width: 300, fontFamily: SANS, fontWeight: 800, fontSize: 26, color: T.text }}>{L.key}</div>
            <div style={{ fontFamily: MONO, fontSize: 18, color: L.c }}>{L.tech}</div>
          </div>
        );
      })}
      <Flow x1={bx + bandW + 40} y1={bottomTop + 46} x2={bx + bandW + 40} y2={bottomTop - 4 * (h + gap) + 46} color={A.graph} n={7} speed={0.014} o={p(0.7, 0.82)} />
      {/* agent + user out the top */}
      <div style={{ position: "absolute", left: 1500, top: 250, width: 300, height: 110, borderRadius: 16, background: mix(T.panel, A.agent, 0.16), border: `2.5px solid ${A.agent}`, display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", opacity: p(0.72, 0.82), boxShadow: `0 0 ${30 + Math.sin(frame * 0.07) * 12}px ${mix(T.bg0, A.agent, 0.4)}` }}>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 26, color: T.text }}>🤖 Agent + You</div>
        <div style={{ fontFamily: MONO, fontSize: 18, color: A.agent, marginTop: 6 }}>ask · decide · act</div>
      </div>
      <Wire x1={1410} y1={bottomTop - 4 * (h + gap) + 46} x2={1500} y2={340} p={p(0.68, 0.78)} color={A.agent} w={3} />
      <Foot p={p(0.86, 0.94)}>{foot || "One coherent stack — every layer earns its place, and the agent sees all of it."}</Foot>
    </Stage>
  );
};

// ============================================================================ TIMELINE (adoption)
const TimelineScene: React.FC<{ dur?: number; kicker?: string; title?: string; color?: string; steps?: { label: string; sub: string }[]; foot?: string }> = ({
  dur, kicker = "START MONDAY · ADOPTION PATH", title = "You don't boil the ocean — you build one layer at a time", color = A.graph, steps = [], foot,
}) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const n = steps.length;
  const y = 520;
  const w = 300, gap = (1620 - n * w) / Math.max(1, n - 1);
  return (
    <Stage>
      <Head theme={T} kicker={kicker} title={title} color={color} o={p(0, 0.06)} />
      <div style={{ position: "absolute", left: 150, top: y + 55, width: 1620, height: 4, background: mix(T.line, color, 0.4), opacity: p(0.1, 0.2) }} />
      {steps.map((s, i) => {
        const x = 150 + i * (w + gap);
        const at = 0.1 + i * 0.14; const o = p(at, at + 0.09);
        const hot = Math.floor(frame / 32) % n === i;
        return (
          <React.Fragment key={i}>
            <div style={{ position: "absolute", left: x + w / 2 - 22, top: y + 34, width: 44, height: 44, borderRadius: 30, background: mix(T.panel, color, 0.2), border: `3px solid ${color}`, display: "flex", alignItems: "center", justifyContent: "center", fontFamily: MONO, fontWeight: 800, fontSize: 24, color: color, opacity: o, boxShadow: hot ? `0 0 22px ${mix(T.bg0, color, 0.5)}` : "none", zIndex: 2 }}>{i + 1}</div>
            <div style={{ position: "absolute", left: x, top: i % 2 === 0 ? y - 150 : y + 110, width: w, borderRadius: 16, background: mix(T.panel, color, hot ? 0.14 : 0.07), border: `2px solid ${hot ? color : mix(T.line, color, 0.5)}`, padding: "18px 22px", boxSizing: "border-box", opacity: o, textAlign: "center" }}>
              <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 26, color: T.text }}>{s.label}</div>
              <div style={{ fontFamily: MONO, fontSize: 18, color: A.muted, marginTop: 8, lineHeight: 1.35 }}>{s.sub}</div>
            </div>
          </React.Fragment>
        );
      })}
      {foot && <Foot p={p(0.82, 0.92)}>{foot}</Foot>}
    </Stage>
  );
};

// ============================================================================ RECAP
const RecapScene: React.FC<{ dur?: number; items?: string[]; closer?: string; kicker?: string; title?: string }> = ({
  dur, items = [], closer = "", kicker = "RECAP · THE WHOLE MAP", title = "The living map in one breath",
}) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const cols = LAYERS.map((L) => L.c);
  return (
    <AbsoluteFill style={{ padding: "60px 130px", justifyContent: "center" }}>
      <div style={{ opacity: p(0, 0.06), textAlign: "center", marginBottom: 26 }}>
        <div style={{ display: "flex", justifyContent: "center" }}><Kicker theme={T} text={kicker} cx /></div>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 60, color: T.text, marginTop: 12, letterSpacing: -1.5 }}>{title}</div>
      </div>
      <div style={{ display: "flex", flexDirection: "column", gap: 12, maxWidth: 1400, margin: "0 auto", width: "100%" }}>
        {items.map((it, i) => {
          const at = 0.06 + i * 0.09; const o = p(at, at + 0.07);
          const c = cols[i % cols.length];
          return (
            <div key={i} style={{ display: "flex", alignItems: "center", gap: 18, opacity: o, transform: `translateX(${(1 - o) * -24}px)`, background: mix(T.panel, c, 0.06), border: `1.5px solid ${T.line}`, borderLeft: `5px solid ${c}`, borderRadius: 12, padding: "15px 26px" }}>
              <span style={{ color: c, fontFamily: MONO, fontWeight: 700, fontSize: 24 }}>{i + 1}</span>
              <span style={{ fontFamily: SANS, fontSize: 28, color: T.text, lineHeight: 1.25 }}>{it}</span>
            </div>
          );
        })}
      </div>
      {closer && (
        <div style={{ textAlign: "center", marginTop: 30, opacity: p(0.82, 0.92) }}>
          <div style={{ fontFamily: SANS, fontWeight: 800, fontStyle: "italic", fontSize: 40, color: A.graph, textShadow: `0 0 ${30 + Math.sin(frame * 0.06) * 14}px ${mix(T.bg0, A.graph, 0.7)}` }}>{closer}</div>
        </div>
      )}
    </AbsoluteFill>
  );
};

// ============================================================================ SceneProgress
const SceneProgress: React.FC<{ accent: string; dur?: number }> = ({ accent, dur }) => {
  const p = usePfull(dur);
  const w = p(0, 1);
  return (
    <div style={{ position: "absolute", left: 0, bottom: 0, height: 5, width: `${w * 100}%`,
      background: `linear-gradient(90deg, ${mix(accent, "#05060F", 0.35)}, ${accent})`, boxShadow: `0 0 12px ${accent}`, opacity: 0.85 }} />
  );
};

// ============================================================================ ROUTER
export const KGScene: React.FC<{ variant: string;[key: string]: unknown }> = ({ variant, ...rest }) => {
  let content: React.ReactNode;
  let accent = A.graph;
  const r = rest as any;
  switch (variant) {
    case "kg_title": content = <TitleScene {...r} />; break;
    case "kg_divider": content = <Divider {...r} />; accent = r.color || A.graph; break;
    case "kg_stack": content = <StackScene {...r} />; break;
    case "kg_silos": content = <SilosScene {...r} />; accent = A.bad; break;
    case "kg_hook": content = <HookScene {...r} />; break;
    case "kg_triple": content = <TripleScene {...r} />; accent = A.ont; break;
    case "kg_compare": content = <CompareScene {...r} />; accent = r.color || A.graph; break;
    case "kg_cards": content = <CardsScene {...r} />; accent = r.color || A.graph; break;
    case "kg_orbit": content = <OrbitScene {...r} />; accent = r.color || A.graph; break;
    case "kg_code": content = <CodeScene {...r} />; accent = r.color || A.kg; break;
    case "kg_chart": content = <ChartScene {...r} />; accent = r.color || A.graph; break;
    case "kg_tower": content = <TowerScene {...r} />; accent = r.color || A.twin; break;
    case "kg_pipeline": content = <PipelineScene {...r} />; accent = r.color || A.graph; break;
    case "kg_ingest": content = <IngestScene {...r} />; accent = A.kg; break;
    case "kg_merge": content = <MergeScene {...r} />; accent = A.kg; break;
    case "kg_telemetry": content = <TelemetryScene {...r} />; accent = A.twin; break;
    case "kg_cascade": content = <CascadeScene {...r} />; accent = A.twin; break;
    case "kg_gnn": content = <GnnScene {...r} />; accent = A.eng; break;
    case "kg_agentloop": content = <AgentLoopScene {...r} />; accent = A.agent; break;
    case "kg_twobrain": content = <TwoBrainScene {...r} />; accent = A.agent; break;
    case "kg_traverse": content = <TraverseScene {...r} />; accent = A.agent; break;
    case "kg_architecture": content = <ArchitectureScene {...r} />; break;
    case "kg_timeline": content = <TimelineScene {...r} />; accent = r.color || A.graph; break;
    case "kg_recap": content = <RecapScene {...r} />; break;
    default: content = <TitleScene {...r} />;
  }
  return (
    <AbsoluteFill>
      <Bg theme={T} accent={accent} />
      {content}
      <SceneProgress accent={accent} dur={r.dur} />
    </AbsoluteFill>
  );
};

export default KGScene;
