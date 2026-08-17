/**
 * GPUScenes.tsx — "GPUs: The Engines of AI" deep-dive course (4 chapters).
 *
 * Identity:
 *   theme  — near-black "silicon" family, cyan primary (memory/bandwidth is the
 *            through-line of AI serving).
 *   accents (semantic, consistent across all chapters):
 *     A.comp  amber  = compute / cores / FLOPS
 *     A.mem   cyan   = memory / bandwidth / HBM
 *     A.ai    violet = the AI model / precision / tokens
 *     A.ok    green  = the result / serving / "it works"
 *     vendor brand colors (Ch3 only): A.nv A.amd A.goog A.gray
 *   motif  — a chip-die grid with a marching data lane (DieMotif), echoed in the
 *            title, dividers and backgrounds.
 *
 * Rules (skills/03): every scene phases with useP(dur) fractions (no fixed frames),
 * something moves in every frame, randomness only via rnd(), no CSS filter/blur.
 * A SceneProgress bar + Bg wrap every scene so no frame reads as frozen.
 */
import React from "react";
import { AbsoluteFill, interpolate, useCurrentFrame } from "remotion";
import {
  makeTheme, mix, useP, usePop, rnd, MONO, SANS,
  Bg, Stage, Kicker, Head, Foot, Card, Flow, Wire, Counter, Brackets, ScanBeam,
} from "../lib/primitives";

// ---------------------------------------------------------------- identity
const T = makeTheme({ accent: "#22D3EE", bg0: "#04060C", bg1: "#080C16", bg2: "#0F1526", panel: "#141A2C" });
const A = {
  comp: "#FBBF24",  // compute / cores / FLOPS (amber)
  mem: "#22D3EE",   // memory / bandwidth / HBM (cyan)
  ai: "#A78BFA",    // model / precision / tokens (violet)
  ok: "#34D399",    // result / serving (green)
  warn: "#F87171",  // limits / bottleneck (red)
  nv: "#76B900",    // NVIDIA brand green
  amd: "#ED1C24",   // AMD brand red
  goog: "#4285F4",  // Google brand blue
  gray: "#94A3B8",
};

// reveals compressed into the front ~0.66 of the beat (front-loaded narration),
// while progress bar + continuous motion use the FULL beat. See skills/02 A/V-lag.
const SPAN = 0.66;
const useReveal = (dur?: unknown) => {
  const p = useP(dur);
  return (a: number, b: number) => p(Math.min(1, a * SPAN), Math.min(1, b * SPAN));
};

// ---------------------------------------------------------------- motif
/** A chip die: grid of cells with a marching bright lane. Continuous, cheap. */
const DieMotif: React.FC<{ x: number; y: number; cols: number; rows: number; cell?: number; color?: string; o?: number; seed?: number }> = ({
  x, y, cols, rows, cell = 26, color = A.mem, o = 1, seed = 0,
}) => {
  const frame = useCurrentFrame();
  const wave = (frame * 0.9) % (cols + 5) - 2.5;
  return (
    <div style={{ position: "absolute", left: x, top: y, display: "grid", gridTemplateColumns: `repeat(${cols}, ${cell}px)`, gap: 3, opacity: o }}>
      {Array.from({ length: cols * rows }).map((_, i) => {
        const c = i % cols, r = Math.floor(i / cols);
        const heat = Math.max(0, 1 - Math.abs(c - wave + Math.sin(r * 1.3 + seed) * 1.2) / 2.4);
        const lit = rnd(c, r, seed) > 0.72;
        return (
          <div key={i} style={{
            width: cell, height: cell, borderRadius: cell * 0.18,
            background: mix(T.bg2, color, (lit ? 0.14 : 0.05) + heat * 0.7),
            border: `1px solid ${mix(T.line, color, 0.2 + heat * 0.6)}`,
            boxShadow: heat > 0.5 ? `0 0 12px ${mix(T.bg0, color, heat)}` : "none",
          }} />
        );
      })}
    </div>
  );
};

// ---------------------------------------------------------------- title
const TitleScene: React.FC<{
  dur?: number; kicker?: string; line1?: string; line2?: string; sub?: string; color?: string;
}> = ({ dur, kicker = "GPUS · THE ENGINES OF AI", line1 = "How GPUs", line2 = "Power AI", sub = "silicon · parallelism · tokens per second", color = A.mem }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const pop = usePop(dur);
  return (
    <AbsoluteFill style={{ alignItems: "center", justifyContent: "center" }}>
      <DieMotif x={120} y={120} cols={10} rows={7} cell={30} color={color} o={0.5} />
      <DieMotif x={1360} y={640} cols={11} rows={7} cell={30} color={A.ai} o={0.4} seed={3} />
      {Array.from({ length: 8 }).map((_, i) => {
        const ang = frame * 0.01 + (i / 8) * Math.PI * 2;
        return <div key={i} style={{
          position: "absolute", left: 960 + Math.cos(ang) * (540 + i * 12) - 5, top: 540 + Math.sin(ang) * (250 + i * 7) - 5,
          width: 9, height: 9, borderRadius: 9, background: color, opacity: 0.2 + rnd(i, 2) * 0.3, boxShadow: `0 0 12px ${color}`,
        }} />;
      })}
      <div style={{ textAlign: "center", transform: `scale(${0.92 + pop(0) * 0.08})`, zIndex: 2 }}>
        <div style={{ display: "flex", justifyContent: "center", marginBottom: 26 }}>
          <Kicker theme={T} text={kicker} color={color} cx />
        </div>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 122, lineHeight: 1.02, letterSpacing: -3, color: T.text }}>
          <div>{line1}</div>
          <div style={{ color, textShadow: `0 0 70px ${mix(T.bg0, color, 0.7)}` }}>{line2}</div>
        </div>
        <div style={{ height: 6, width: interpolate(p(0.18, 0.45), [0, 1], [0, 560]), background: `linear-gradient(90deg, ${color}, ${A.ai})`, borderRadius: 3, margin: "34px auto" }} />
        <div style={{ fontFamily: SANS, fontSize: 38, color: T.muted, opacity: p(0.28, 0.5) }}>{sub}</div>
      </div>
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------- roadmap (Ch1)
const RoadmapScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const parts = [
    { n: 1, title: "What a GPU Is", sub: "thousands of cores, one job", c: A.comp },
    { n: 2, title: "Running AI Models", sub: "matrix math, tensor cores, tokens", c: A.ai },
    { n: 3, title: "The GPU Landscape", sub: "NVIDIA · AMD · Google · others", c: A.nv },
    { n: 4, title: "Sizing the Compute", sub: "tokens/sec, users, throughput, latency", c: A.ok },
  ];
  const y0 = 250, rowH = 148;
  const hot = Math.floor(frame / 22) % parts.length;
  const railFill = p(0.08, 0.82);
  return (
    <AbsoluteFill style={{ alignItems: "center", justifyContent: "center" }}>
      <DieMotif x={70} y={330} cols={6} rows={9} cell={24} color={A.mem} o={0.3} />
      <div style={{ position: "absolute", left: 0, right: 0, top: 110, textAlign: "center", opacity: p(0, 0.06) }}>
        <Kicker theme={T} text="THE COURSE · FOUR CHAPTERS" cx />
      </div>
      <div style={{ position: "absolute", left: 520, top: y0 + 30, width: 4, height: parts.length * rowH - 90, background: T.line, borderRadius: 2 }} />
      <div style={{ position: "absolute", left: 520, top: y0 + 30, width: 4, height: (parts.length * rowH - 90) * railFill, background: `linear-gradient(180deg, ${A.comp}, ${A.ok})`, borderRadius: 2, boxShadow: `0 0 12px ${A.mem}` }} />
      {parts.map((pt, i) => {
        const at = 0.1 + i * 0.15;
        const o = p(at, at + 0.09);
        const active = hot === i;
        return (
          <div key={i} style={{ position: "absolute", left: 570, top: y0 + i * rowH, width: 940, height: rowH - 26, display: "flex", alignItems: "center", gap: 26, opacity: o, transform: `translateX(${(1 - o) * -30}px)` }}>
            <div style={{ width: 74, height: 74, borderRadius: 18, flexShrink: 0, background: mix(T.panel, pt.c, active ? 0.35 : 0.16), border: `2.5px solid ${pt.c}`, display: "flex", alignItems: "center", justifyContent: "center", fontFamily: MONO, fontWeight: 800, fontSize: 34, color: pt.c, boxShadow: active ? `0 0 22px ${mix(T.bg0, pt.c, 0.5)}` : "none", transform: `scale(${active ? 1.08 : 1})` }}>{pt.n}</div>
            <div>
              <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 44, color: T.text, letterSpacing: -1 }}>{pt.title}</div>
              <div style={{ fontFamily: MONO, fontSize: 25, color: pt.c, marginTop: 4 }}>{pt.sub}</div>
            </div>
          </div>
        );
      })}
      <div style={{ position: "absolute", left: 514, top: y0 + 26 + ((frame * 3) % (parts.length * rowH - 80)), width: 16, height: 16, borderRadius: 8, background: A.mem, boxShadow: `0 0 16px ${A.mem}`, opacity: p(0.1, 0.2) }} />
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------- divider
const Divider: React.FC<{ dur?: number; n?: number; title?: string; sub?: string; color?: string }> = ({
  dur, n = 1, title = "", sub = "", color = A.mem,
}) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  return (
    <Stage>
      <DieMotif x={140} y={150} cols={7} rows={4} cell={26} color={color} o={0.3} seed={n} />
      <DieMotif x={1470} y={780} cols={7} rows={4} cell={26} color={color} o={0.28} seed={n + 5} />
      <Brackets x={330} y={300} w={1260} h={480} color={color} o={p(0.02, 0.14)} len={54} />
      <ScanBeam theme={T} x={340} y={310} w={1240} h={460} color={color} o={p(0.05, 0.2)} speed={1.6} />
      <div style={{ position: "absolute", left: 0, right: 0, top: 360, textAlign: "center" }}>
        <div style={{ fontFamily: MONO, fontWeight: 800, fontSize: 34, color, letterSpacing: 10, opacity: p(0.05, 0.15) }}>CHAPTER {n}</div>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 92, color: T.text, letterSpacing: -2, marginTop: 20, opacity: p(0.12, 0.24), transform: `translateY(${(1 - p(0.12, 0.24)) * 30}px)` }}>{title}</div>
        <div style={{ height: 5, width: interpolate(p(0.2, 0.5), [0, 1], [0, 460]), background: color, borderRadius: 3, margin: "26px auto" }} />
        <div style={{ fontFamily: SANS, fontSize: 33, color: T.muted, opacity: p(0.3, 0.45) }}>{sub}</div>
      </div>
      <div style={{ position: "absolute", left: 0, right: 0, top: 860, display: "flex", justifyContent: "center", gap: 16, opacity: p(0.3, 0.45) }}>
        {[1, 2, 3, 4].map((i) => (
          <div key={i} style={{ width: i === n ? 46 : 14, height: 14, borderRadius: 8, background: i <= n ? color : mix(T.panel, color, 0.15), border: `1.5px solid ${i <= n ? color : T.line}`, opacity: i === n ? 0.7 + Math.sin(frame * 0.1) * 0.3 : 1 }} />
        ))}
      </div>
    </Stage>
  );
};

// ================================================================ CHAPTER 1
// gpu_cpuvsgpu — few big cores vs thousands of small cores, both doing a task
const CpuVsGpuScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const r = useReveal(dur);
  // CPU: 6 cores sweep through 24 items sequentially. GPU: 24 lanes, all at once.
  const N = 24;
  const cpuCores = 6;
  const cpuStep = Math.floor(p(0.42, 0.9) * (N / cpuCores + 1)); // which "round" the CPU is on
  const gpuOn = r(0.5, 0.62);
  return (
    <Stage>
      <Head theme={T} kicker="CH1 · TWO KINDS OF CHIP" title="A few fast cores, or thousands of small ones" o={p(0, 0.06)} />
      {/* CPU panel */}
      <Card theme={T} x={110} y={230} w={780} h={620} color={A.warn} o={r(0.06, 0.14)}>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 40, color: A.warn }}>CPU</div>
        <div style={{ fontFamily: MONO, fontSize: 24, color: T.muted, marginTop: 4 }}>a few big cores · runs steps in order</div>
        <div style={{ display: "grid", gridTemplateColumns: `repeat(3, 200px)`, gap: 18, marginTop: 34 }}>
          {Array.from({ length: cpuCores }).map((_, i) => {
            const active = i === (Math.floor(frame / 8) % cpuCores) && p(0.42, 0.44) > 0;
            return <div key={i} style={{ height: 108, borderRadius: 14, background: mix(T.panel, A.warn, active ? 0.32 : 0.1), border: `2.5px solid ${A.warn}`, display: "flex", alignItems: "center", justifyContent: "center", fontFamily: MONO, fontWeight: 700, fontSize: 26, color: T.text, boxShadow: active ? `0 0 20px ${mix(T.bg0, A.warn, 0.5)}` : "none" }}>core {i + 1}</div>;
          })}
        </div>
        <div style={{ fontFamily: MONO, fontSize: 23, color: A.warn, marginTop: 30, opacity: r(0.42, 0.5) }}>24 numbers → {Math.min(N, cpuStep * cpuCores)} done, one round at a time</div>
      </Card>
      {/* GPU panel */}
      <Card theme={T} x={1030} y={230} w={780} h={620} color={A.comp} o={r(0.2, 0.28)} glow>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 40, color: A.comp }}>GPU</div>
        <div style={{ fontFamily: MONO, fontSize: 24, color: T.muted, marginTop: 4 }}>thousands of small cores · all at once</div>
        <div style={{ display: "grid", gridTemplateColumns: `repeat(6, 108px)`, gap: 10, marginTop: 34 }}>
          {Array.from({ length: N }).map((_, i) => {
            const glow = gpuOn > 0 && 0.5 + Math.sin(frame * 0.15 + i * 0.5) * 0.5;
            return <div key={i} style={{ height: 74, borderRadius: 11, background: mix(T.panel, A.comp, gpuOn > 0 ? 0.22 + (glow as number) * 0.25 : 0.08), border: `2px solid ${A.comp}`, opacity: r(0.2 + i * 0.005, 0.3 + i * 0.005) }} />;
          })}
        </div>
        <div style={{ fontFamily: MONO, fontSize: 23, color: A.comp, marginTop: 30, opacity: r(0.5, 0.58) }}>24 numbers → all 24 done in one shot</div>
      </Card>
      <Foot theme={T} p={p(0.84, 0.92)}>
        Same total work. The CPU is a sprinter; the GPU is ten thousand runners crossing the line together.
      </Foot>
    </Stage>
  );
};

// gpu_parallel — SIMD: one instruction, many data. Computed elementwise square.
const SRC_VEC = Array.from({ length: 16 }, (_, i) => Math.round(2 + rnd(i, 7) * 7));
const ParallelScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const r = useReveal(dur);
  const applied = r(0.4, 0.72);
  return (
    <Stage>
      <Head theme={T} kicker="CH1 · SIMD" title="One instruction, applied to a flood of numbers" color={A.comp} o={p(0, 0.06)} />
      <div style={{ position: "absolute", left: 0, right: 0, top: 250, textAlign: "center", opacity: r(0.1, 0.2) }}>
        <span style={{ fontFamily: MONO, fontWeight: 800, fontSize: 40, color: A.comp, background: mix(T.panel, A.comp, 0.12), border: `2.5px solid ${A.comp}`, borderRadius: 14, padding: "12px 30px" }}>instruction:  y = x × x</span>
      </div>
      {/* input row */}
      {SRC_VEC.map((v, i) => {
        const x = 150 + i * 105, y = 420;
        const out = Math.round(v + (v * v - v) * applied);
        const lane = r(0.24 + i * 0.008, 0.34 + i * 0.008);
        return (
          <React.Fragment key={i}>
            <div style={{ position: "absolute", left: x, top: y, width: 88, height: 78, borderRadius: 12, background: mix(T.panel, A.mem, 0.14), border: `2px solid ${A.mem}`, display: "flex", alignItems: "center", justifyContent: "center", fontFamily: MONO, fontWeight: 800, fontSize: 34, color: T.text, opacity: lane }}>{v}</div>
            <Wire x1={x + 44} y1={y + 84} x2={x + 44} y2={y + 176} p={r(0.34 + i * 0.006, 0.42 + i * 0.006)} color={A.comp} w={2.5} arrow={false} />
            <div style={{ position: "absolute", left: x, top: y + 190, width: 88, height: 78, borderRadius: 12, background: mix(T.panel, A.comp, 0.12 + applied * 0.16), border: `2px solid ${A.comp}`, display: "flex", alignItems: "center", justifyContent: "center", fontFamily: MONO, fontWeight: 800, fontSize: 32, color: A.comp, opacity: r(0.4, 0.5), boxShadow: applied > 0.9 ? `0 0 14px ${mix(T.bg0, A.comp, 0.4 + Math.sin(frame * 0.1 + i) * 0.2)}` : "none" }}>{out}</div>
          </React.Fragment>
        );
      })}
      <div style={{ position: "absolute", left: 150, top: 388, fontFamily: MONO, fontSize: 22, color: A.mem, opacity: r(0.2, 0.28) }}>x  (the input numbers)</div>
      <div style={{ position: "absolute", left: 150, top: 706, fontFamily: MONO, fontSize: 22, color: A.comp, opacity: r(0.4, 0.48) }}>y = x²  ·  all sixteen lanes fire on the same clock</div>
      <Foot theme={T} p={p(0.84, 0.92)}>
        This is the GPU's whole trick: broadcast one instruction across a vast array of tiny arithmetic units.
      </Foot>
    </Stage>
  );
};

// gpu_anatomy — inside the die: SMs, tensor cores, HBM stacks, memory bus
const AnatomyScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur);
  const r = useReveal(dur);
  return (
    <Stage>
      <Head theme={T} kicker="CH1 · INSIDE THE DIE" title="What is actually on the silicon" color={A.mem} o={p(0, 0.06)} />
      {/* central die */}
      <div style={{ position: "absolute", left: 610, top: 250, width: 700, height: 560, borderRadius: 22, background: mix(T.panel, A.mem, 0.06), border: `2.5px solid ${mix(T.line, A.mem, 0.5)}`, opacity: r(0.05, 0.14) }}>
        <div style={{ fontFamily: MONO, fontSize: 22, color: T.muted, padding: "14px 20px" }}>GPU DIE · ~80–208 billion transistors</div>
        <DieMotif x={40} y={70} cols={16} rows={10} cell={30} color={A.comp} o={r(0.16, 0.28)} />
      </div>
      {/* HBM stacks left & right */}
      {[0, 1, 2, 3].map((i) => {
        const left = i < 2;
        const x = left ? 360 : 1330; const y = 250 + (i % 2) * 290;
        return <Card key={i} theme={T} x={x} y={y} w={220} h={250} color={A.mem} o={r(0.28 + i * 0.04, 0.36 + i * 0.04)}>
          <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 30, color: A.mem }}>HBM</div>
          <div style={{ fontFamily: MONO, fontSize: 21, color: T.muted, marginTop: 6 }}>stacked memory</div>
          <div style={{ marginTop: 14 }}>{[0, 1, 2, 3, 4].map((k) => <div key={k} style={{ height: 26, marginBottom: 6, borderRadius: 5, background: mix(T.panel, A.mem, 0.2 + k * 0.05), border: `1.5px solid ${mix(T.line, A.mem, 0.5)}` }} />)}</div>
        </Card>;
      })}
      {/* buses die<->HBM with flow */}
      {[0, 1, 2, 3].map((i) => {
        const left = i < 2; const y = 375 + (i % 2) * 290;
        const x1 = left ? 580 : 1330; const x2 = left ? 610 : 1310;
        return <React.Fragment key={i}>
          <Wire x1={x1} y1={y} x2={x2} y2={y} p={r(0.4, 0.5)} color={A.mem} w={4} arrow={false} />
          <Flow x1={left ? 580 : 1310} y1={y} x2={left ? 610 : 1330} y2={y} color={A.mem} n={4} o={r(0.5, 0.6)} />
        </React.Fragment>;
      })}
      <div style={{ position: "absolute", left: 610, top: 690, width: 700, textAlign: "center", fontFamily: MONO, fontSize: 24, color: A.comp, opacity: r(0.2, 0.3) }}>
        thousands of cores · Tensor Cores · L2 cache
      </div>
      <Foot theme={T} p={p(0.84, 0.92)}>
        A sea of compute in the middle, ringed by ultra-fast memory — feeding the cores is the whole game.
      </Foot>
    </Stage>
  );
};

// gpu_bandwidth — bandwidth is the headline number. Computed bytes/s bars.
const BandwidthScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur);
  const r = useReveal(dur);
  // GB/s across memory tiers (illustrative, order-of-magnitude, on screen)
  const tiers = [
    { label: "Your laptop's RAM (DDR5)", v: 80, disp: "80 GB/s", c: A.gray },
    { label: "A100 (HBM2e)", v: 2039, disp: "2.0 TB/s", c: A.ai },
    { label: "H100 (HBM3)", v: 3350, disp: "3.35 TB/s", c: A.comp },
    { label: "H200 (HBM3e)", v: 4800, disp: "4.8 TB/s", c: A.mem },
    { label: "B200 (HBM3e)", v: 8000, disp: "8.0 TB/s", c: A.ok },
  ];
  const max = 8000, X0 = 640, W = 1080;
  return (
    <Stage>
      <Head theme={T} kicker="CH1 · BANDWIDTH" title="How fast the chip can read its own memory" color={A.mem} o={p(0, 0.06)} />
      {tiers.map((t, i) => {
        const y = 250 + i * 118;
        const grow = r(0.1 + i * 0.09, 0.24 + i * 0.09);
        const w = (t.v / max) * W * grow;
        return (
          <React.Fragment key={i}>
            <div style={{ position: "absolute", left: 100, top: y + 8, width: 510, fontFamily: SANS, fontWeight: 700, fontSize: 28, color: T.text, opacity: r(0.08 + i * 0.09, 0.16 + i * 0.09) }}>{t.label}</div>
            <div style={{ position: "absolute", left: X0, top: y, width: w, height: 60, borderRadius: "10px 16px 16px 10px", background: `linear-gradient(90deg, ${mix(t.c, T.bg1, 0.5)}, ${t.c})`, border: `2px solid ${t.c}`, boxShadow: `0 0 20px ${mix(T.bg0, t.c, 0.3)}` }} />
            <div style={{ position: "absolute", left: X0 + w + 16, top: y + 12, fontFamily: MONO, fontWeight: 800, fontSize: 32, color: t.c, opacity: grow }}>{t.disp}</div>
          </React.Fragment>
        );
      })}
      <Foot theme={T} p={p(0.84, 0.92)}>
        A B200 moves 8 terabytes every second — about 100× your laptop. In AI, bandwidth is destiny.
      </Foot>
    </Stage>
  );
};

// ================================================================ CHAPTER 2
// gpu_matmul — a REAL small matrix multiply, computed & animated
const MM_A = [[1, 2, 3], [4, 0, 1], [2, 5, 1], [0, 3, 2]]; // 4x3
const MM_B = [[1, 0, 2], [0, 1, 1], [2, 1, 0]];            // 3x3
const MM_C = MM_A.map((row) => MM_B[0].map((_, j) => row.reduce((s, a, k) => s + a * MM_B[k][j], 0)));
const MatmulScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur);
  const r = useReveal(dur);
  const cell = 74, gap = 8;
  const total = MM_C.length * MM_C[0].length;
  const filled = Math.floor(r(0.34, 0.92) * (total + 1));
  const grid = (g: number[][], x: number, y: number, color: string, reveal: number, hi?: { r?: number; c?: number }) =>
    g.map((row, ri) => row.map((v, ci) => {
      const on = reveal > (ri * row.length + ci) / (g.length * row.length);
      const isHiR = hi?.r === ri, isHiC = hi?.c === ci;
      const active = isHiR || isHiC;
      return <div key={`${ri}-${ci}`} style={{ position: "absolute", left: x + ci * (cell + gap), top: y + ri * (cell + gap), width: cell, height: cell, borderRadius: 10, background: mix(T.panel, color, active ? 0.34 : 0.12), border: `2px solid ${active ? color : mix(T.line, color, 0.5)}`, display: "flex", alignItems: "center", justifyContent: "center", fontFamily: MONO, fontWeight: 800, fontSize: 32, color: on ? T.text : "transparent", opacity: on ? 1 : 0.15 }}>{v}</div>;
    }));
  const outIdx = Math.min(total - 1, filled);
  const hr = Math.floor(outIdx / MM_C[0].length), hc = outIdx % MM_C[0].length;
  return (
    <Stage>
      <Head theme={T} kicker="CH2 · THE CORE OPERATION" title="An AI model is mostly one thing: matrix multiply" color={A.ai} o={p(0, 0.06)} />
      {grid(MM_A, 150, 320, A.mem, r(0.08, 0.2), { r: hr })}
      <div style={{ position: "absolute", left: 470, top: 430, fontFamily: MONO, fontSize: 46, color: T.muted, opacity: r(0.1, 0.18) }}>×</div>
      {grid(MM_B, 540, 320, A.comp, r(0.14, 0.26), { c: hc })}
      <div style={{ position: "absolute", left: 820, top: 430, fontFamily: MONO, fontSize: 46, color: T.muted, opacity: r(0.2, 0.28) }}>=</div>
      {grid(MM_C, 900, 320, A.ai, filled / total, { r: hr, c: hc })}
      {/* running dot-product readout for the active output cell */}
      <div style={{ position: "absolute", left: 150, top: 720, width: 1500, fontFamily: MONO, fontSize: 27, color: A.ai, opacity: r(0.4, 0.5) }}>
        each output = row · column, summed — {filled} of {total} cells computed
      </div>
      <Foot theme={T} p={p(0.84, 0.92)}>
        Billions of these multiply-adds per token. GPUs exist to do exactly this, massively in parallel.
      </Foot>
    </Stage>
  );
};

// gpu_tensorcore — a Tensor Core swallows a whole tile per op
const TensorCoreScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const r = useReveal(dur);
  const pulse = 0.5 + Math.sin(frame * 0.12) * 0.5;
  return (
    <Stage>
      <Head theme={T} kicker="CH2 · TENSOR CORES" title="Specialized units that eat whole tiles at once" color={A.comp} o={p(0, 0.06)} />
      {/* tile A and B feeding a core, producing accumulate */}
      <Card theme={T} x={120} y={280} w={340} h={340} color={A.mem} o={r(0.06, 0.16)}>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 30, color: A.mem }}>tile A</div>
        <DieMotif x={20} y={70} cols={6} rows={6} cell={40} color={A.mem} o={r(0.14, 0.24)} />
      </Card>
      <Card theme={T} x={490} y={280} w={340} h={340} color={A.comp} o={r(0.12, 0.22)}>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 30, color: A.comp }}>tile B</div>
        <DieMotif x={20} y={70} cols={6} rows={6} cell={40} color={A.comp} o={r(0.2, 0.3)} />
      </Card>
      <Wire x1={460} y1={450} x2={900} y2={450} p={r(0.26, 0.36)} color={A.comp} w={4} />
      <Flow x1={460} y1={450} x2={900} y2={450} color={A.comp} n={6} o={r(0.34, 0.44)} />
      {/* the tensor core */}
      <div style={{ position: "absolute", left: 910, top: 320, width: 280, height: 260, borderRadius: 20, background: mix(T.panel, A.ai, 0.2), border: `3px solid ${A.ai}`, display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", opacity: r(0.3, 0.4), boxShadow: `0 0 ${30 + pulse * 30}px ${mix(T.bg0, A.ai, 0.5)}` }}>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 30, color: A.ai }}>Tensor Core</div>
        <div style={{ fontFamily: MONO, fontSize: 40, color: T.text, marginTop: 10 }}>D = A·B + C</div>
        <div style={{ fontFamily: MONO, fontSize: 20, color: T.muted, marginTop: 8 }}>one fused op</div>
      </div>
      <Wire x1={1190} y1={450} x2={1420} y2={450} p={r(0.42, 0.52)} color={A.ai} w={4} />
      <Card theme={T} x={1430} y={310} w={330} h={280} color={A.ok} o={r(0.5, 0.6)} glow>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 30, color: A.ok }}>accumulate</div>
        <div style={{ fontFamily: MONO, fontSize: 22, color: T.muted, marginTop: 8, lineHeight: 1.4 }}>results pile up across thousands of tiles → a full layer</div>
        <Counter p={r(0.56, 0.72)} to={989} suffix=" TFLOPS" color={A.ok} size={34} />
      </Card>
      <Foot theme={T} p={p(0.84, 0.92)}>
        Regular cores multiply numbers; Tensor Cores multiply small matrices — the reason modern GPUs are AI machines.
      </Foot>
    </Stage>
  );
};

// gpu_transformer — token → attention → FFN → next token, as a pipeline
const TransformerScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur);
  const r = useReveal(dur);
  const stages = [
    { at: 0.08, x: 120, label: "tokens", sub: '"The cat sat"', c: A.mem },
    { at: 0.22, x: 560, label: "attention", sub: "words look at words", c: A.ai },
    { at: 0.4, x: 1000, label: "feed-forward", sub: "big matrix multiplies", c: A.comp },
    { at: 0.56, x: 1440, label: "next token", sub: '"on"', c: A.ok },
  ];
  return (
    <Stage>
      <Head theme={T} kicker="CH2 · THE TRANSFORMER" title="How the words flow through the model" color={A.ai} o={p(0, 0.06)} />
      {stages.map((s, i) => (
        <React.Fragment key={i}>
          {i > 0 && (
            <>
              <Wire x1={stages[i - 1].x + 360} y1={470} x2={s.x - 12} y2={470} p={r(s.at - 0.08, s.at)} color={s.c} w={3.5} />
              <Flow x1={stages[i - 1].x + 360} y1={470} x2={s.x - 12} y2={470} color={s.c} n={5} o={r(s.at + 0.02, s.at + 0.1)} />
            </>
          )}
          <Card theme={T} x={s.x} y={360} w={360} h={230} color={s.c} o={r(s.at, s.at + 0.09)} glow={i === 3}>
            <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 36, color: s.c }}>{s.label}</div>
            <div style={{ fontFamily: MONO, fontSize: 25, color: T.muted, marginTop: 14 }}>{s.sub}</div>
          </Card>
        </React.Fragment>
      ))}
      {/* the loop-back arrow: output feeds back as input */}
      <Wire x1={1620} y1={590} x2={300} y2={700} p={r(0.66, 0.78)} color={A.gray} w={2.5} curve={-120} />
      <div style={{ position: "absolute", left: 760, top: 720, width: 400, textAlign: "center", fontFamily: MONO, fontSize: 24, color: A.gray, opacity: r(0.72, 0.82) }}>…then loop: the new word becomes input for the next</div>
      <Foot theme={T} p={p(0.84, 0.92)}>
        Every single word out is one full pass through the stack — repeated, token after token.
      </Foot>
    </Stage>
  );
};

// gpu_prefill_decode — the two phases: prefill (parallel) vs decode (one at a time)
const PrefillDecodeScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const r = useReveal(dur);
  const decodeStep = Math.floor(p(0.5, 0.92) * 7) % 7;
  return (
    <Stage>
      <Head theme={T} kicker="CH2 · TWO PHASES" title="Reading the prompt vs. writing the answer" color={A.ai} o={p(0, 0.06)} />
      {/* PREFILL */}
      <Card theme={T} x={110} y={240} w={800} h={560} color={A.comp} o={r(0.06, 0.16)}>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 38, color: A.comp }}>1 · Prefill</div>
        <div style={{ fontFamily: MONO, fontSize: 24, color: T.muted, marginTop: 6 }}>read the whole prompt — all at once</div>
        <div style={{ display: "flex", flexWrap: "wrap", gap: 10, marginTop: 30 }}>
          {"The cat sat on the warm mat by".split(" ").map((w, i) => (
            <div key={i} style={{ padding: "12px 18px", borderRadius: 10, background: mix(T.panel, A.comp, 0.2), border: `2px solid ${A.comp}`, fontFamily: MONO, fontSize: 26, color: T.text, opacity: r(0.16 + i * 0.01, 0.26 + i * 0.01) }}>{w}</div>
          ))}
        </div>
        <div style={{ fontFamily: SANS, fontWeight: 700, fontSize: 26, color: A.comp, marginTop: 36, opacity: r(0.34, 0.44) }}>compute-bound — the cores are busy</div>
      </Card>
      {/* DECODE */}
      <Card theme={T} x={1010} y={240} w={800} h={560} color={A.mem} o={r(0.2, 0.3)} glow>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 38, color: A.mem }}>2 · Decode</div>
        <div style={{ fontFamily: MONO, fontSize: 24, color: T.muted, marginTop: 6 }}>write the answer — one token at a time</div>
        <div style={{ display: "flex", gap: 12, marginTop: 40, alignItems: "center" }}>
          {["the", "fire", "place", "…"].map((w, i) => (
            <div key={i} style={{ padding: "14px 20px", borderRadius: 10, background: mix(T.panel, A.mem, i <= decodeStep ? 0.28 : 0.06), border: `2px solid ${i <= decodeStep ? A.mem : T.line}`, fontFamily: MONO, fontSize: 28, color: i <= decodeStep ? T.text : T.muted, opacity: r(0.3, 0.4) }}>{w}</div>
          ))}
          <div style={{ width: 16, height: 44, background: A.mem, opacity: Math.floor(frame / 8) % 2 ? 0.9 : 0.2, borderRadius: 3 }} />
        </div>
        <div style={{ fontFamily: SANS, fontWeight: 700, fontSize: 26, color: A.mem, marginTop: 60, opacity: r(0.44, 0.54) }}>memory-bound — re-read every weight, per token</div>
        <div style={{ position: "absolute", left: 30, bottom: 24, fontFamily: MONO, fontSize: 22, color: T.muted }}>this is the slow part — and Chapter 4's bottleneck</div>
      </Card>
      <Foot theme={T} p={p(0.84, 0.92)}>
        Prefill is a sprint the cores love; decode is a slow drip the memory bus controls.
      </Foot>
    </Stage>
  );
};

// gpu_precision — number formats: fewer bits = more speed + less memory
const PrecisionScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur);
  const r = useReveal(dur);
  const fmts = [
    { name: "FP32", bits: 32, gb: 4.0, c: A.gray, note: "full precision · training's old default" },
    { name: "FP16 / BF16", bits: 16, gb: 2.0, c: A.ai, note: "the workhorse for years" },
    { name: "FP8", bits: 8, gb: 1.0, c: A.comp, note: "H100 era — 2× faster" },
    { name: "FP4", bits: 4, gb: 0.5, c: A.ok, note: "Blackwell — 2× again" },
  ];
  return (
    <Stage>
      <Head theme={T} kicker="CH2 · PRECISION" title="Shrink the numbers, and everything gets faster" color={A.ai} o={p(0, 0.06)} />
      {fmts.map((f, i) => {
        const y = 250 + i * 138;
        const rr = r(0.08 + i * 0.1, 0.2 + i * 0.1);
        return (
          <React.Fragment key={i}>
            <div style={{ position: "absolute", left: 100, top: y + 18, width: 260, fontFamily: SANS, fontWeight: 800, fontSize: 34, color: f.c, opacity: rr }}>{f.name}</div>
            {/* bit boxes */}
            <div style={{ position: "absolute", left: 380, top: y + 16, display: "flex", gap: 4 }}>
              {Array.from({ length: f.bits }).map((_, b) => (
                <div key={b} style={{ width: 18, height: 42, borderRadius: 4, background: mix(T.panel, f.c, 0.35), border: `1.5px solid ${f.c}`, opacity: r(0.1 + i * 0.1 + b * 0.004, 0.22 + i * 0.1 + b * 0.004) }} />
              ))}
            </div>
            <div style={{ position: "absolute", left: 1230, top: y + 20, fontFamily: MONO, fontWeight: 800, fontSize: 30, color: f.c, opacity: rr }}>{f.gb} GB / 1B params</div>
            <div style={{ position: "absolute", left: 380, top: y + 74, width: 800, fontFamily: MONO, fontSize: 22, color: T.muted, opacity: r(0.16 + i * 0.1, 0.26 + i * 0.1) }}>{f.note}</div>
          </React.Fragment>
        );
      })}
      <Foot theme={T} p={p(0.84, 0.92)}>
        FP4 stores a billion parameters in half a gigabyte — the trick behind today's throughput gains.
      </Foot>
    </Stage>
  );
};

// gpu_membound — roofline: decode reads all weights per token → memory-bound
const MemBoundScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur);
  const r = useReveal(dur);
  // 70B model, FP8 = 70 GB read per token. tok/s = BW / 70.
  const cards = [
    { gpu: "H100", bw: 3.35, c: A.comp },
    { gpu: "H200", bw: 4.8, c: A.mem },
    { gpu: "B200", bw: 8.0, c: A.ok },
  ];
  return (
    <Stage>
      <Head theme={T} kicker="CH2 · THE ROOFLINE" title="Why one token costs one full memory sweep" color={A.mem} o={p(0, 0.06)} />
      <div style={{ position: "absolute", left: 100, top: 230, width: 1720, textAlign: "center", fontFamily: MONO, fontSize: 28, color: T.text, opacity: r(0.06, 0.16) }}>
        70-billion-parameter model in FP8 = <span style={{ color: A.ai, fontWeight: 800 }}>70 GB of weights</span> — read once for every single token
      </div>
      <div style={{ position: "absolute", left: 100, top: 300, width: 1720, textAlign: "center", fontFamily: MONO, fontWeight: 800, fontSize: 34, color: A.mem, opacity: r(0.16, 0.26) }}>
        tokens per second  =  bandwidth  /  70 GB
      </div>
      {cards.map((c, i) => {
        const x = 250 + i * 500;
        const toks = Math.round((c.bw * 1000) / 70);
        return (
          <Card key={i} theme={T} x={x} y={410} w={420} h={320} color={c.c} o={r(0.28 + i * 0.08, 0.38 + i * 0.08)} glow={i === 2}>
            <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 40, color: c.c }}>{c.gpu}</div>
            <div style={{ fontFamily: MONO, fontSize: 24, color: T.muted, marginTop: 8 }}>{c.bw} TB/s / 70 GB</div>
            <div style={{ marginTop: 40 }}>
              <Counter p={r(0.4 + i * 0.08, 0.6 + i * 0.08)} to={toks} color={c.c} size={72} />
              <span style={{ fontFamily: MONO, fontSize: 30, color: c.c }}> tok/s</span>
            </div>
            <div style={{ fontFamily: MONO, fontSize: 21, color: T.muted, marginTop: 14 }}>single stream, one user</div>
          </Card>
        );
      })}
      <Foot theme={T} p={p(0.84, 0.92)}>
        One user, one stream — the GPU is barely warm. The fix is serving many users at once. (Chapter 4.)
      </Foot>
    </Stage>
  );
};

// ================================================================ CHAPTER 3
// gpu_nvidia_line — the NVIDIA lineage as a growing timeline
const NvidiaLineScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur);
  const r = useReveal(dur);
  const gens = [
    { name: "A100", year: "2020", mem: 80, bw: 2.0, c: A.gray },
    { name: "H100", year: "2022", mem: 80, bw: 3.35, c: A.ai },
    { name: "H200", year: "2024", mem: 141, bw: 4.8, c: A.comp },
    { name: "B200", year: "2024", mem: 192, bw: 8.0, c: A.ok },
  ];
  const X0 = 200, W = 400;
  return (
    <Stage>
      <Head theme={T} kicker="CH3 · NVIDIA" title="Ampere → Hopper → Blackwell" color={A.nv} o={p(0, 0.06)} />
      {/* baseline */}
      <div style={{ position: "absolute", left: 140, top: 760, width: 1640, height: 3, background: T.line }} />
      {gens.map((g, i) => {
        const x = X0 + i * W;
        const hMem = g.mem * 2.2 * r(0.1 + i * 0.09, 0.24 + i * 0.09);
        const hBw = g.bw * 55 * r(0.14 + i * 0.09, 0.28 + i * 0.09);
        return (
          <React.Fragment key={i}>
            {i > 0 && <Wire x1={X0 + (i - 1) * W + 260} y1={720} x2={x + 40} y2={720} p={r(0.08 + i * 0.09, 0.16 + i * 0.09)} color={A.nv} w={2.5} />}
            {/* memory bar */}
            <div style={{ position: "absolute", left: x, top: 760 - hMem, width: 120, height: hMem, borderRadius: "10px 10px 0 0", background: `linear-gradient(180deg, ${A.mem}, ${mix(A.mem, T.bg1, 0.5)})`, border: `2px solid ${A.mem}` }} />
            {/* bandwidth bar */}
            <div style={{ position: "absolute", left: x + 130, top: 760 - hBw, width: 120, height: hBw, borderRadius: "10px 10px 0 0", background: `linear-gradient(180deg, ${A.comp}, ${mix(A.comp, T.bg1, 0.5)})`, border: `2px solid ${A.comp}` }} />
            <div style={{ position: "absolute", left: x, top: 780, width: 250, textAlign: "center", fontFamily: SANS, fontWeight: 800, fontSize: 34, color: g.c, opacity: r(0.1 + i * 0.09, 0.2 + i * 0.09) }}>{g.name}</div>
            <div style={{ position: "absolute", left: x, top: 824, width: 250, textAlign: "center", fontFamily: MONO, fontSize: 22, color: T.muted, opacity: r(0.14 + i * 0.09, 0.24 + i * 0.09) }}>{g.year} · {g.mem}GB · {g.bw}TB/s</div>
          </React.Fragment>
        );
      })}
      <div style={{ position: "absolute", left: 1440, top: 250, display: "flex", flexDirection: "column", gap: 14, opacity: r(0.5, 0.6) }}>
        <div style={{ fontFamily: MONO, fontSize: 24, color: A.mem }}>▮ memory (GB)</div>
        <div style={{ fontFamily: MONO, fontSize: 24, color: A.comp }}>▮ bandwidth (TB/s)</div>
      </div>
      <Foot theme={T} p={p(0.84, 0.92)}>
        Every generation roughly doubles what matters — and demand still outruns supply.
      </Foot>
    </Stage>
  );
};

// gpu_gb200 — rack scale: 72 GPUs act as one
const Gb200Scene: React.FC<{ dur?: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const r = useReveal(dur);
  return (
    <Stage>
      <Head theme={T} kicker="CH3 · RACK SCALE" title="GB200 NVL72 — 72 GPUs wired into one brain" color={A.nv} o={p(0, 0.06)} />
      {/* the rack: 72 cells */}
      <div style={{ position: "absolute", left: 130, top: 250, width: 760, padding: 24, borderRadius: 20, background: mix(T.panel, A.nv, 0.06), border: `2.5px solid ${mix(T.line, A.nv, 0.5)}`, opacity: r(0.05, 0.14) }}>
        <div style={{ fontFamily: MONO, fontSize: 22, color: T.muted, marginBottom: 14 }}>72 × Blackwell GPU · one NVLink domain</div>
        <div style={{ display: "grid", gridTemplateColumns: `repeat(9, 1fr)`, gap: 8 }}>
          {Array.from({ length: 72 }).map((_, i) => {
            const lit = (Math.floor(frame / 2) % 72) === i || rnd(i, 3, Math.floor(frame / 30)) > 0.8;
            return <div key={i} style={{ height: 54, borderRadius: 7, background: mix(T.panel, A.nv, lit ? 0.5 : 0.18), border: `1.5px solid ${A.nv}`, opacity: r(0.1 + i * 0.004, 0.2 + i * 0.004), boxShadow: lit ? `0 0 10px ${mix(T.bg0, A.nv, 0.6)}` : "none" }} />;
          })}
        </div>
      </div>
      {/* aggregate stats */}
      {[
        { at: 0.3, label: "HBM3e memory", to: 13.4, suf: " TB", dec: 1, c: A.mem },
        { at: 0.4, label: "NVLink bandwidth", to: 130, suf: " TB/s", dec: 0, c: A.comp },
        { at: 0.5, label: "FP4 compute", to: 1.4, suf: " exaFLOPS", dec: 1, c: A.ok },
        { at: 0.6, label: "power draw", to: 120, suf: " kW / rack", dec: 0, c: A.warn },
      ].map((s, i) => (
        <div key={i} style={{ position: "absolute", left: 980, top: 270 + i * 130, opacity: r(s.at, s.at + 0.08) }}>
          <div style={{ fontFamily: MONO, fontSize: 25, color: T.muted }}>{s.label}</div>
          <Counter p={r(s.at + 0.04, s.at + 0.16)} to={s.to} suffix={s.suf} decimals={s.dec} color={s.c} size={58} />
        </div>
      ))}
      <Foot theme={T} p={p(0.84, 0.92)}>
        One rack, the compute of a small supercomputer — and this is the unit AI data centers now buy by the thousand.
      </Foot>
    </Stage>
  );
};

// gpu_speccompare — vendors head to head (bars for memory + bandwidth)
const SpecCompareScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur);
  const r = useReveal(dur);
  const rows = [
    { name: "NVIDIA H100", mem: 80, bw: 3.35, c: A.nv },
    { name: "NVIDIA B200", mem: 192, bw: 8.0, c: A.nv },
    { name: "AMD MI300X", mem: 192, bw: 5.3, c: A.amd },
    { name: "AMD MI355X", mem: 288, bw: 8.0, c: A.amd },
    { name: "Google TPU v7", mem: 192, bw: 7.4, c: A.goog },
  ];
  const memMax = 288, bwMax = 8, X0 = 560, WM = 520, WB = 480;
  return (
    <Stage>
      <Head theme={T} kicker="CH3 · HEAD TO HEAD" title="Memory and bandwidth, across the vendors" color={A.mem} o={p(0, 0.06)} />
      <div style={{ position: "absolute", left: X0, top: 210, fontFamily: MONO, fontSize: 22, color: A.mem, opacity: r(0.05, 0.12) }}>memory (GB)</div>
      <div style={{ position: "absolute", left: X0 + WM + 90, top: 210, fontFamily: MONO, fontSize: 22, color: A.comp, opacity: r(0.05, 0.12) }}>bandwidth (TB/s)</div>
      {rows.map((row, i) => {
        const y = 268 + i * 108;
        const rr = r(0.08 + i * 0.09, 0.18 + i * 0.09);
        const wm = (row.mem / memMax) * WM * rr;
        const wb = (row.bw / bwMax) * WB * rr;
        return (
          <React.Fragment key={i}>
            <div style={{ position: "absolute", left: 100, top: y + 8, width: 440, fontFamily: SANS, fontWeight: 700, fontSize: 28, color: row.c, opacity: rr }}>{row.name}</div>
            <div style={{ position: "absolute", left: X0, top: y, width: wm, height: 56, borderRadius: 8, background: `linear-gradient(90deg, ${mix(A.mem, T.bg1, 0.5)}, ${A.mem})`, border: `2px solid ${A.mem}` }} />
            <div style={{ position: "absolute", left: X0 + wm + 10, top: y + 14, fontFamily: MONO, fontWeight: 800, fontSize: 26, color: A.mem, opacity: rr }}>{row.mem}</div>
            <div style={{ position: "absolute", left: X0 + WM + 90, top: y, width: wb, height: 56, borderRadius: 8, background: `linear-gradient(90deg, ${mix(A.comp, T.bg1, 0.5)}, ${A.comp})`, border: `2px solid ${A.comp}` }} />
            <div style={{ position: "absolute", left: X0 + WM + 90 + wb + 10, top: y + 14, fontFamily: MONO, fontWeight: 800, fontSize: 26, color: A.comp, opacity: rr }}>{row.bw}</div>
          </React.Fragment>
        );
      })}
      <Foot theme={T} p={p(0.84, 0.92)}>
        AMD leads on raw memory; NVIDIA leads on software and networking. That gap is the whole competition.
      </Foot>
    </Stage>
  );
};

// gpu_others — the wider ecosystem, orbit hub
const OthersScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const r = useReveal(dur);
  const items = [
    { emoji: "🟩", label: "NVIDIA GPU", sub: "the default", c: A.nv },
    { emoji: "🟥", label: "AMD Instinct", sub: "memory leader", c: A.amd },
    { emoji: "🟦", label: "Google TPU", sub: "in-house, at scale", c: A.goog },
    { emoji: "🟧", label: "AWS Trainium", sub: "cloud-native", c: A.comp },
    { emoji: "🟪", label: "Cerebras", sub: "wafer-scale chip", c: A.ai },
    { emoji: "⬜", label: "Groq LPU", sub: "fastest tokens", c: A.gray },
  ];
  return (
    <Stage>
      <Head theme={T} kicker="CH3 · THE FIELD" title="It isn't only NVIDIA any more" color={A.mem} o={p(0, 0.06)} />
      {/* hub */}
      <div style={{ position: "absolute", left: 860, top: 470, width: 200, height: 160, borderRadius: 22, background: mix(T.panel, A.mem, 0.16), border: `3px solid ${A.mem}`, display: "flex", alignItems: "center", justifyContent: "center", textAlign: "center", opacity: r(0.05, 0.14), boxShadow: `0 0 ${30 + Math.sin(frame * 0.06) * 14}px ${mix(T.bg0, A.mem, 0.4)}` }}>
        <span style={{ fontFamily: SANS, fontWeight: 800, fontSize: 30, color: T.text }}>AI accelerators</span>
      </div>
      {items.map((it, i) => {
        const ang = (i / items.length) * Math.PI * 2 - Math.PI / 2 + Math.sin(frame * 0.008) * 0.05;
        const x = 960 + Math.cos(ang) * 620, y = 550 + Math.sin(ang) * 300;
        const at = 0.1 + i * 0.08;
        const active = Math.floor(frame / 26) % items.length === i;
        return (
          <React.Fragment key={i}>
            <Wire x1={960} y1={550} x2={x} y2={y} p={r(at, at + 0.06)} color={active ? it.c : mix(T.muted, T.bg1, 0.4)} w={active ? 3 : 2} arrow={false} />
            <div style={{ position: "absolute", left: x - 165, top: y - 52, width: 330, height: 104, borderRadius: 16, background: mix(T.panel, it.c, active ? 0.2 : 0.08), border: `2.5px solid ${active ? it.c : mix(T.line, it.c, 0.5)}`, display: "flex", alignItems: "center", gap: 16, padding: "0 22px", boxSizing: "border-box", opacity: r(at, at + 0.08), transform: `scale(${active ? 1.06 : 1})` }}>
              <span style={{ fontSize: 40 }}>{it.emoji}</span>
              <div>
                <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 27, color: T.text }}>{it.label}</div>
                <div style={{ fontFamily: MONO, fontSize: 20, color: it.c, marginTop: 2 }}>{it.sub}</div>
              </div>
            </div>
          </React.Fragment>
        );
      })}
      <Foot theme={T} p={p(0.84, 0.92)}>
        Different bets on the same problem — but NVIDIA's software moat, CUDA, still sets the pace.
      </Foot>
    </Stage>
  );
};

// ================================================================ CHAPTER 4
// gpu_batching — batching amortizes weight reads → throughput scales
const BatchingScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur);
  const r = useReveal(dur);
  // single-stream ~48 tok/s on H100 (70B FP8). Aggregate ≈ batch × single (until roofs).
  const bats = [
    { b: 1, agg: 48, c: A.gray },
    { b: 8, agg: 360, c: A.ai },
    { b: 32, agg: 1200, c: A.comp },
    { b: 128, agg: 2600, c: A.ok },
  ];
  const max = 2600, X0 = 260, W = 340, Y0 = 740;
  return (
    <Stage>
      <Head theme={T} kicker="CH4 · BATCHING" title="Serve many users, read the weights once" color={A.ok} o={p(0, 0.06)} />
      <div style={{ position: "absolute", left: 100, top: 220, width: 1720, fontFamily: MONO, fontSize: 26, color: T.text, opacity: r(0.06, 0.16) }}>
        The weights get read once per step no matter how many prompts ride along — so stack the prompts.
      </div>
      {bats.map((bt, i) => {
        const x = X0 + i * W;
        const h = (bt.agg / max) * 440 * r(0.14 + i * 0.1, 0.3 + i * 0.1);
        return (
          <React.Fragment key={i}>
            <div style={{ position: "absolute", left: x, top: Y0 - h, width: 200, height: h, borderRadius: "12px 12px 0 0", background: `linear-gradient(180deg, ${bt.c}, ${mix(bt.c, T.bg1, 0.5)})`, border: `2px solid ${bt.c}` }} />
            <div style={{ position: "absolute", left: x - 20, top: Y0 - h - 52, width: 240, textAlign: "center", fontFamily: MONO, fontWeight: 800, fontSize: 32, color: bt.c, opacity: r(0.2 + i * 0.1, 0.32 + i * 0.1) }}>{bt.agg} tok/s</div>
            <div style={{ position: "absolute", left: x - 20, top: Y0 + 14, width: 240, textAlign: "center", fontFamily: SANS, fontWeight: 700, fontSize: 27, color: T.text, opacity: r(0.16 + i * 0.1, 0.26 + i * 0.1) }}>batch {bt.b}</div>
          </React.Fragment>
        );
      })}
      <div style={{ position: "absolute", left: 140, top: Y0, width: 1500, height: 3, background: T.line }} />
      <Foot theme={T} p={p(0.84, 0.92)}>
        One H100 goes from ~50 to a couple thousand tokens a second — same chip, just kept busy.
      </Foot>
    </Stage>
  );
};

// gpu_tradeoff — throughput vs latency curve
const TradeoffScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur);
  const r = useReveal(dur);
  const X0 = 260, Y0 = 760, W = 1200, H = 480;
  // throughput rises then plateaus; per-user latency rises steadily. draw both.
  const tp = Array.from({ length: 60 }, (_, i) => { const t = i / 59; return `${X0 + t * W},${Y0 - H * (1 - Math.exp(-t * 3.2))}`; });
  const lat = Array.from({ length: 60 }, (_, i) => { const t = i / 59; return `${X0 + t * W},${Y0 - H * (0.15 + t * 0.8)}`; });
  const cp = r(0.16, 0.6), cl = r(0.34, 0.78);
  return (
    <Stage>
      <Head theme={T} kicker="CH4 · THE TRADE-OFF" title="Throughput and latency pull against each other" color={A.ok} o={p(0, 0.06)} />
      <svg style={{ position: "absolute", left: 0, top: 0 }} width={1920} height={1080}>
        <line x1={X0} y1={Y0} x2={X0 + W} y2={Y0} stroke={T.line} strokeWidth={2} />
        <line x1={X0} y1={Y0} x2={X0} y2={Y0 - H} stroke={T.line} strokeWidth={2} />
        <polyline points={tp.slice(0, Math.max(2, Math.round(60 * cp))).join(" ")} fill="none" stroke={A.ok} strokeWidth={5} />
        <polyline points={lat.slice(0, Math.max(2, Math.round(60 * cl))).join(" ")} fill="none" stroke={A.warn} strokeWidth={5} strokeDasharray="10 8" />
      </svg>
      <div style={{ position: "absolute", left: X0 + W - 340, top: Y0 - H + 6, fontFamily: MONO, fontWeight: 800, fontSize: 28, color: A.ok, opacity: r(0.4, 0.5) }}>total throughput ↑</div>
      <div style={{ position: "absolute", left: X0 + W - 360, top: Y0 - 130, fontFamily: MONO, fontWeight: 800, fontSize: 28, color: A.warn, opacity: r(0.55, 0.65) }}>per-user latency ↑</div>
      <div style={{ position: "absolute", left: X0, top: Y0 + 20, fontFamily: MONO, fontSize: 24, color: T.muted, opacity: r(0.1, 0.2) }}>bigger batch  →</div>
      <div style={{ position: "absolute", left: 300, top: 250, width: 470, fontFamily: SANS, fontWeight: 700, fontSize: 26, color: T.text, opacity: r(0.66, 0.76), textAlign: "left", lineHeight: 1.4 }}>
        Push the batch too far, and every user waits longer between words. Serving is just choosing a point on this curve.
      </div>
      <Foot theme={T} p={p(0.84, 0.92)}>
        Cheap tokens or snappy replies — you tune the batch size to buy one with the other.
      </Foot>
    </Stage>
  );
};

// gpu_users — users per GPU, computed
const UsersScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur);
  const r = useReveal(dur);
  return (
    <Stage>
      <Head theme={T} kicker="CH4 · USERS PER GPU" title="From tokens per second to people served" color={A.ok} o={p(0, 0.06)} />
      {/* equation blocks */}
      <Card theme={T} x={120} y={280} w={470} h={280} color={A.comp} o={r(0.08, 0.18)}>
        <div style={{ fontFamily: MONO, fontSize: 25, color: T.muted }}>one GPU delivers</div>
        <div style={{ marginTop: 20 }}><Counter p={r(0.14, 0.3)} to={2600} color={A.comp} size={66} /><span style={{ fontFamily: MONO, fontSize: 28, color: A.comp }}> tok/s</span></div>
        <div style={{ fontFamily: MONO, fontSize: 22, color: T.muted, marginTop: 16 }}>aggregate, well-batched</div>
      </Card>
      <div style={{ position: "absolute", left: 624, top: 396, fontFamily: MONO, fontSize: 58, color: T.muted, opacity: r(0.24, 0.32) }}>/</div>
      <Card theme={T} x={720} y={280} w={470} h={280} color={A.ai} o={r(0.24, 0.34)}>
        <div style={{ fontFamily: MONO, fontSize: 25, color: T.muted }}>each reader needs</div>
        <div style={{ marginTop: 20 }}><Counter p={r(0.3, 0.44)} to={20} color={A.ai} size={66} /><span style={{ fontFamily: MONO, fontSize: 28, color: A.ai }}> tok/s</span></div>
        <div style={{ fontFamily: MONO, fontSize: 22, color: T.muted, marginTop: 16 }}>faster than you can read</div>
      </Card>
      <div style={{ position: "absolute", left: 1230, top: 400, fontFamily: MONO, fontSize: 54, color: T.muted, opacity: r(0.4, 0.48) }}>=</div>
      <Card theme={T} x={1320} y={280} w={470} h={280} color={A.ok} o={r(0.44, 0.54)} glow>
        <div style={{ fontFamily: MONO, fontSize: 25, color: T.muted }}>concurrent users</div>
        <div style={{ marginTop: 20 }}><span style={{ fontFamily: MONO, fontSize: 28, color: A.ok }}>≈ </span><Counter p={r(0.5, 0.66)} to={130} color={A.ok} size={72} /></div>
        <div style={{ fontFamily: MONO, fontSize: 22, color: T.muted, marginTop: 16 }}>per single GPU, chatting live</div>
      </Card>
      <div style={{ position: "absolute", left: 120, top: 640, width: 1670, fontFamily: MONO, fontSize: 24, color: T.muted, opacity: r(0.62, 0.72), textAlign: "center" }}>
        …but they don't all type at once — real systems serve many times this by sharing idle moments.
      </div>
      <Foot theme={T} p={p(0.84, 0.92)}>
        A single accelerator can hold a live conversation with roughly a hundred people at once.
      </Foot>
    </Stage>
  );
};

// gpu_cluster — sizing a real deployment
const ClusterScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const r = useReveal(dur);
  const steps = [
    { at: 0.1, label: "target", val: "1,000,000", sub: "concurrent users", c: A.ai },
    { at: 0.26, label: "/ users per GPU", val: "≈ 130", sub: "live streams each", c: A.comp },
    { at: 0.42, label: "= GPUs needed", val: "≈ 7,700", sub: "just for serving", c: A.mem },
    { at: 0.58, label: "= NVL72 racks", val: "≈ 107", sub: "at 72 GPUs / rack", c: A.ok },
  ];
  return (
    <Stage>
      <Head theme={T} kicker="CH4 · SIZING IT" title="How big a fleet does a million users need?" color={A.ok} o={p(0, 0.06)} />
      {steps.map((s, i) => {
        const y = 250 + i * 145;
        return (
          <React.Fragment key={i}>
            {i > 0 && <Wire x1={430} y1={y - 30} x2={430} y2={y} p={r(s.at - 0.06, s.at)} color={s.c} w={3} arrow={false} />}
            <div style={{ position: "absolute", left: 120, top: y + 12, width: 560, fontFamily: SANS, fontWeight: 700, fontSize: 30, color: T.muted, opacity: r(s.at, s.at + 0.08) }}>{s.label}</div>
            <div style={{ position: "absolute", left: 720, top: y, fontFamily: MONO, fontWeight: 800, fontSize: 62, color: s.c, opacity: r(s.at + 0.02, s.at + 0.1) }}>{s.val}</div>
            <div style={{ position: "absolute", left: 1120, top: y + 22, width: 640, fontFamily: MONO, fontSize: 24, color: T.muted, opacity: r(s.at + 0.04, s.at + 0.12) }}>{s.sub}</div>
          </React.Fragment>
        );
      })}
      {/* a few glowing racks as motif */}
      <div style={{ position: "absolute", left: 120, top: 840, display: "flex", gap: 8, opacity: r(0.6, 0.7) }}>
        {Array.from({ length: 24 }).map((_, i) => <div key={i} style={{ width: 22, height: 40, borderRadius: 4, background: mix(T.panel, A.ok, 0.2 + (Math.floor(frame / 3) % 24 === i ? 0.5 : 0)), border: `1.5px solid ${A.ok}` }} />)}
        <span style={{ fontFamily: MONO, fontSize: 22, color: T.muted, alignSelf: "center", marginLeft: 10 }}>…× 107 racks</span>
      </div>
      <Foot theme={T} p={p(0.84, 0.92)}>
        This is why AI labs raise billions — and why NVIDIA sells every chip it can make.
      </Foot>
    </Stage>
  );
};

// ---------------------------------------------------------------- recap
const RecapScene: React.FC<{ dur?: number; items?: string[]; closer?: string; kicker?: string; title?: string; color?: string }> = ({
  dur, items = [], closer = "GPUs are parallel math engines — and AI is one very big pile of parallel math.", kicker = "RECAP", title = "The whole story in one breath", color = A.mem,
}) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  return (
    <AbsoluteFill style={{ padding: "60px 130px", justifyContent: "center" }}>
      <DieMotif x={70} y={60} cols={8} rows={3} cell={22} color={color} o={0.22} />
      <div style={{ opacity: p(0, 0.06), textAlign: "center", marginBottom: 28 }}>
        <Kicker theme={T} text={kicker} color={color} cx />
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 60, color: T.text, marginTop: 12, letterSpacing: -1.5 }}>{title}</div>
      </div>
      <div style={{ display: "flex", flexDirection: "column", gap: 13, maxWidth: 1360, margin: "0 auto", width: "100%" }}>
        {items.map((it, i) => {
          const at = 0.08 + i * 0.1;
          const o = p(at, at + 0.07);
          return (
            <div key={i} style={{ display: "flex", alignItems: "center", gap: 18, opacity: o, transform: `translateX(${(1 - o) * -26}px)`, background: mix(T.panel, color, 0.05), border: `1.5px solid ${T.line}`, borderLeft: `4px solid ${color}`, borderRadius: 12, padding: "15px 26px" }}>
              <span style={{ color, fontFamily: MONO, fontWeight: 700, fontSize: 26 }}>{i + 1}</span>
              <span style={{ fontFamily: SANS, fontSize: 29, color: T.text, lineHeight: 1.25 }}>{it}</span>
            </div>
          );
        })}
      </div>
      <div style={{ textAlign: "center", marginTop: 32, opacity: p(0.8, 0.9) }}>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontStyle: "italic", fontSize: 40, color, textShadow: `0 0 ${30 + Math.sin(frame * 0.06) * 14}px ${mix(T.bg0, color, 0.7)}` }}>{closer}</div>
      </div>
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------- SceneProgress
const SceneProgress: React.FC<{ accent: string; dur?: number }> = ({ accent, dur }) => {
  const p = useP(dur);
  const w = p(0, 1);
  return (
    <div style={{ position: "absolute", left: 0, bottom: 0, height: 5, width: `${w * 100}%`, background: `linear-gradient(90deg, ${mix(accent, "#04060C", 0.35)}, ${accent})`, boxShadow: `0 0 12px ${accent}`, opacity: 0.85 }} />
  );
};

// ================================================================ router
export const GPUScene: React.FC<{ variant: string;[key: string]: unknown }> = ({ variant, ...rest }) => {
  let content: React.ReactNode;
  let accent = A.mem;
  switch (variant) {
    case "gpu_title": content = <TitleScene {...(rest as any)} />; accent = (rest as any).color || A.mem; break;
    case "gpu_roadmap": content = <RoadmapScene {...(rest as any)} />; break;
    case "gpu_divider": content = <Divider {...(rest as any)} />; accent = (rest as any).color || A.mem; break;
    // ch1
    case "gpu_cpuvsgpu": content = <CpuVsGpuScene {...(rest as any)} />; accent = A.comp; break;
    case "gpu_parallel": content = <ParallelScene {...(rest as any)} />; accent = A.comp; break;
    case "gpu_anatomy": content = <AnatomyScene {...(rest as any)} />; accent = A.mem; break;
    case "gpu_bandwidth": content = <BandwidthScene {...(rest as any)} />; accent = A.mem; break;
    // ch2
    case "gpu_matmul": content = <MatmulScene {...(rest as any)} />; accent = A.ai; break;
    case "gpu_tensorcore": content = <TensorCoreScene {...(rest as any)} />; accent = A.comp; break;
    case "gpu_transformer": content = <TransformerScene {...(rest as any)} />; accent = A.ai; break;
    case "gpu_prefill": content = <PrefillDecodeScene {...(rest as any)} />; accent = A.ai; break;
    case "gpu_precision": content = <PrecisionScene {...(rest as any)} />; accent = A.ai; break;
    case "gpu_membound": content = <MemBoundScene {...(rest as any)} />; accent = A.mem; break;
    // ch3
    case "gpu_nvidia": content = <NvidiaLineScene {...(rest as any)} />; accent = A.nv; break;
    case "gpu_gb200": content = <Gb200Scene {...(rest as any)} />; accent = A.nv; break;
    case "gpu_speccompare": content = <SpecCompareScene {...(rest as any)} />; accent = A.mem; break;
    case "gpu_others": content = <OthersScene {...(rest as any)} />; accent = A.mem; break;
    // ch4
    case "gpu_batching": content = <BatchingScene {...(rest as any)} />; accent = A.ok; break;
    case "gpu_tradeoff": content = <TradeoffScene {...(rest as any)} />; accent = A.ok; break;
    case "gpu_users": content = <UsersScene {...(rest as any)} />; accent = A.ok; break;
    case "gpu_cluster": content = <ClusterScene {...(rest as any)} />; accent = A.ok; break;
    case "gpu_recap": content = <RecapScene {...(rest as any)} />; accent = (rest as any).color || A.mem; break;
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

export default GPUScene;
