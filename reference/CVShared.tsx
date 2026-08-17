/**
 * CVShared.tsx — shared visual engine for the Computer Vision explainer (cv_* scenes).
 *
 * Identity: "vision lab" — near-black blue, viewfinder corner brackets, scan-beam
 * sweeps, and a procedural PIXEL engine: sprites are number grids (0..255) and
 * every image operation shown on screen (brightness, contrast, blur, convolution,
 * Sobel edges, max-pool, diffusion noise) is actually computed in JS and rendered
 * as living cells. Duration-aware phases via useP(dur) — see FTScenes.tsx pattern.
 */
import React from "react";
import { AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig } from "remotion";

export const C = {
  bg0: "#04070A",
  bg1: "#081019",
  bg2: "#0E1C28",
  panel: "#122330",
  pix: "#22D3EE", // pixels / data
  classic: "#FBBF24", // classical processing
  neural: "#A78BFA", // deep learning
  green: "#34D399", // detection / ok
  gen: "#F472B6", // generative
  red: "#F87171",
  text: "#EDF6FB",
  muted: "#7E94A4",
  line: "rgba(160,220,255,0.09)",
};
export const MONO = "ui-monospace, 'SF Mono', Menlo, monospace";
export const SANS = "'Space Grotesk', Inter, system-ui, sans-serif";
export const BW = 1920, BH = 1080;
export const CL = { extrapolateLeft: "clamp" as const, extrapolateRight: "clamp" as const };

export function mix(a: string, b: string, t: number) {
  const pa = a.replace("#", "").match(/\w\w/g)!.map((x) => parseInt(x, 16));
  const pb = b.replace("#", "").match(/\w\w/g)!.map((x) => parseInt(x, 16));
  const c = pa.map((v, i) => Math.round(v + (pb[i] - v) * Math.max(0, Math.min(1, t))));
  return `rgb(${c[0]},${c[1]},${c[2]})`;
}

/** Duration-aware phase helper: p(a,b) maps fractions of the whole scene to 0..1. */
export const useP = (dur?: unknown) => {
  const frame = useCurrentFrame();
  const F = Math.max(45, (typeof dur === "number" ? dur : 16) * 30);
  return (a: number, b: number) => interpolate(frame, [a * F, b * F], [0, 1], CL);
};

/** Deterministic hash noise in [0,1) — safe across render threads. */
export const rnd = (i: number, j: number, s = 0) => {
  const x = Math.sin(i * 127.1 + j * 311.7 + s * 74.7) * 43758.5453;
  return x - Math.floor(x);
};

// ---------------------------------------------------------------- image math
export type Grid = number[][];
const clamp255 = (v: number) => Math.max(0, Math.min(255, Math.round(v)));

export const sprite = (rows: string[], map: Record<string, number>): Grid =>
  rows.map((r) => [...r].map((ch) => map[ch] ?? 0));

/** 12×12 cat face (bright fur, dark eyes/nose) — the recurring test image. */
export const CAT12: Grid = sprite(
  [
    "..o......o..",
    ".oxo....oxo.",
    ".oxxo..oxxo.",
    ".xxxxxxxxxx.",
    "oxxxxxxxxxxo",
    "oxx#xxxx#xxo",
    "oxxxxxxxxxxo",
    "oxxxx@@xxxxo",
    ".oxxx@@xxxo.",
    ".oxxxxxxxxo.",
    "..oxxxxxxo..",
    "...oooooo...",
  ],
  { ".": 12, o: 120, x: 205, "#": 30, "@": 70 },
);

/** 8×8 handwritten-style digit 7 — for the convolution walkthrough. */
export const SEVEN8: Grid = sprite(
  [
    "........",
    ".######.",
    "......#.",
    ".....#..",
    "....#...",
    "...##...",
    "...#....",
    "........",
  ],
  { ".": 18, "#": 235 },
);

export const gmap = (g: Grid, f: (v: number) => number): Grid => g.map((r) => r.map((v) => clamp255(f(v))));

export const boxBlur3 = (g: Grid): Grid =>
  g.map((row, r) =>
    row.map((_, c) => {
      let s = 0, n = 0;
      for (let dr = -1; dr <= 1; dr++) for (let dc = -1; dc <= 1; dc++) {
        const rr = r + dr, cc = c + dc;
        if (rr >= 0 && rr < g.length && cc >= 0 && cc < row.length) { s += g[rr][cc]; n++; }
      }
      return clamp255(s / n);
    }),
  );

/** Valid-mode 3×3 convolution (raw, may be negative). */
export const conv3 = (g: Grid, k: number[][]): Grid => {
  const out: Grid = [];
  for (let r = 1; r < g.length - 1; r++) {
    const row: number[] = [];
    for (let c = 1; c < g[0].length - 1; c++) {
      let s = 0;
      for (let dr = -1; dr <= 1; dr++) for (let dc = -1; dc <= 1; dc++) s += g[r + dr][c + dc] * k[dr + 1][dc + 1];
      row.push(s);
    }
    out.push(row);
  }
  return out;
};

export const SOBEL_X = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]];
export const SOBEL_Y = [[-1, -2, -1], [0, 0, 0], [1, 2, 1]];
export const K_BLUR = [[1 / 9, 1 / 9, 1 / 9], [1 / 9, 1 / 9, 1 / 9], [1 / 9, 1 / 9, 1 / 9]];
export const K_SHARP = [[0, -1, 0], [-1, 5, -1], [0, -1, 0]];
export const K_EDGE = [[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]];

export const absNorm = (g: Grid): Grid => {
  const m = Math.max(1, ...g.flat().map((v) => Math.abs(v)));
  return g.map((r) => r.map((v) => clamp255((Math.abs(v) / m) * 255)));
};

export const sobelMag = (g: Grid): Grid => {
  const gx = conv3(g, SOBEL_X), gy = conv3(g, SOBEL_Y);
  return absNorm(gx.map((r, i) => r.map((v, j) => Math.abs(v) + Math.abs(gy[i][j]))));
};

export const maxPool2 = (g: Grid): Grid => {
  const out: Grid = [];
  for (let r = 0; r + 1 < g.length; r += 2) {
    const row: number[] = [];
    for (let c = 0; c + 1 < g[0].length; c += 2) row.push(Math.max(g[r][c], g[r][c + 1], g[r + 1][c], g[r + 1][c + 1]));
    out.push(row);
  }
  return out;
};

// ---------------------------------------------------------------- primitives
/** Number-grid image. reveal: 0..1 scan-order cell reveal. hi: highlighted window. */
export const PixGrid: React.FC<{
  g: Grid; x: number; y: number; cell: number; reveal?: number;
  values?: boolean; tint?: string; gap?: number; label?: string; labelColor?: string;
  hi?: { r: number; c: number; size: number; color?: string } | null; o?: number;
}> = ({ g, x, y, cell, reveal = 1, values, tint, gap = 2, label, labelColor, hi = null, o = 1 }) => {
  const rows = g.length, cols = g[0].length, total = rows * cols;
  return (
    <div style={{ position: "absolute", left: x, top: y, opacity: o }}>
      {label && (
        <div style={{ fontFamily: MONO, fontSize: Math.max(19, cell * 0.5), color: labelColor || C.muted, marginBottom: 8 }}>{label}</div>
      )}
      <div style={{ display: "grid", gridTemplateColumns: `repeat(${cols}, ${cell}px)`, gap }}>
        {g.flat().map((v, i) => {
          const on = i / total <= reveal ? 1 : 0;
          const bgc = tint ? mix(C.bg1, tint, v / 255) : `rgb(${v},${v},${v})`;
          return (
            <div key={i} style={{
              width: cell, height: cell, borderRadius: Math.max(2, cell * 0.12),
              background: bgc, opacity: on, display: "flex", alignItems: "center", justifyContent: "center",
              border: `1px solid rgba(160,220,255,0.06)`,
            }}>
              {values && cell >= 24 && (
                <span style={{ fontFamily: MONO, fontSize: cell * 0.33, color: v > 128 ? "#0B1220" : "#B9D2E2", fontWeight: 700 }}>{v}</span>
              )}
            </div>
          );
        })}
      </div>
      {hi && (
        <div style={{
          position: "absolute", left: (label ? 0 : 0) + hi.c * (cell + gap) - 3, top: (label ? Math.max(19, cell * 0.5) + 8 : 0) + hi.r * (cell + gap) - 3,
          width: hi.size * (cell + gap) - gap + 6, height: hi.size * (cell + gap) - gap + 6,
          border: `3px solid ${hi.color || C.classic}`, borderRadius: 8, boxShadow: `0 0 22px ${hi.color || C.classic}`,
        }} />
      )}
    </div>
  );
};

/** Viewfinder corner brackets with a slow breathing pulse. */
export const Brackets: React.FC<{ x: number; y: number; w: number; h: number; color?: string; o?: number; len?: number }> = ({
  x, y, w, h, color = C.pix, o = 1, len = 34,
}) => {
  const frame = useCurrentFrame();
  const b = Math.sin(frame * 0.05) * 4;
  const s = 4;
  return (
    <div style={{ position: "absolute", left: x - b, top: y - b, width: w + b * 2, height: h + b * 2, opacity: o, pointerEvents: "none" }}>
      {/* four corners drawn with simple bars */}
      {[0, 1, 2, 3].map((i) => {
        const right = i % 2 === 1, bottom = i >= 2;
        return (
          <React.Fragment key={i}>
            <div style={{ position: "absolute", [right ? "right" : "left"]: 0, [bottom ? "bottom" : "top"]: 0, width: s, height: len, background: color, borderRadius: 2 } as React.CSSProperties} />
            <div style={{ position: "absolute", [right ? "right" : "left"]: 0, [bottom ? "bottom" : "top"]: 0, width: len, height: s, background: color, borderRadius: 2 } as React.CSSProperties} />
          </React.Fragment>
        );
      })}
    </div>
  );
};

/** Horizontal scan beam sweeping down a region forever. */
export const ScanBeam: React.FC<{ x: number; y: number; w: number; h: number; color?: string; o?: number; speed?: number }> = ({
  x, y, w, h, color = C.pix, o = 1, speed = 0.55,
}) => {
  const frame = useCurrentFrame();
  const t = ((frame * speed) % (h + 60)) - 30;
  return (
    <div style={{ position: "absolute", left: x, top: y, width: w, height: h, overflow: "hidden", opacity: o, pointerEvents: "none" }}>
      <div style={{ position: "absolute", left: 0, top: t, width: "100%", height: 3, background: color, boxShadow: `0 0 18px ${color}`, opacity: 0.85 }} />
      <div style={{ position: "absolute", left: 0, top: t - 44, width: "100%", height: 44, background: `linear-gradient(180deg, transparent, ${mix(C.bg0, color, 0.45)}44)` }} />
    </div>
  );
};

export const Flow: React.FC<{
  x1: number; y1: number; x2: number; y2: number; curve?: number;
  color?: string; n?: number; speed?: number; size?: number; o?: number;
}> = ({ x1, y1, x2, y2, curve = 0, color = C.pix, n = 7, speed = 0.011, size = 11, o = 1 }) => {
  const frame = useCurrentFrame();
  const mx = (x1 + x2) / 2, my = (y1 + y2) / 2 - curve;
  return (
    <>
      {Array.from({ length: n }).map((_, i) => {
        const tt = (frame * speed + i / n) % 1;
        const u = 1 - tt;
        const px = u * u * x1 + 2 * u * tt * mx + tt * tt * x2;
        const py = u * u * y1 + 2 * u * tt * my + tt * tt * y2;
        const fade = Math.sin(tt * Math.PI);
        return (
          <div key={i} style={{
            position: "absolute", left: px - size / 2, top: py - size / 2, width: size, height: size,
            borderRadius: size, background: color, opacity: o * fade * 0.9, boxShadow: `0 0 ${size}px ${color}`,
          }} />
        );
      })}
    </>
  );
};

export const Wire: React.FC<{
  x1: number; y1: number; x2: number; y2: number; p: number; curve?: number;
  color?: string; w?: number; arrow?: boolean;
}> = ({ x1, y1, x2, y2, p, curve = 0, color = C.muted, w = 3, arrow = true }) => {
  const frame = useCurrentFrame();
  const mx = (x1 + x2) / 2, my = (y1 + y2) / 2 - curve;
  const len = Math.hypot(x2 - x1, y2 - y1) + Math.abs(curve);
  const id = `cv${color.replace(/[^a-z0-9]/gi, "")}${Math.round(curve)}`;
  return (
    <svg style={{ position: "absolute", left: 0, top: 0, overflow: "visible" }} width={BW} height={BH}>
      <defs>
        <marker id={id} markerWidth="10" markerHeight="10" refX="7" refY="3" orient="auto">
          <path d="M0,0 L7,3 L0,6 Z" fill={color} />
        </marker>
      </defs>
      <path d={`M ${x1} ${y1} Q ${mx} ${my} ${x2} ${y2}`} fill="none" stroke={color} strokeWidth={w} opacity={p}
        strokeDasharray={`${len}`} strokeDashoffset={(1 - p) * len}
        markerEnd={arrow && p > 0.95 ? `url(#${id})` : undefined} />
      {p >= 1 - 1e-6 && (
        <path d={`M ${x1} ${y1} Q ${mx} ${my} ${x2} ${y2}`} fill="none" stroke={color} strokeWidth={w} opacity={0.45}
          strokeDasharray="6 18" strokeDashoffset={-frame * 1.6} />
      )}
    </svg>
  );
};

export const Counter: React.FC<{ p: number; to: number; prefix?: string; suffix?: string; color?: string; size?: number; decimals?: number }> = ({
  p, to, prefix = "", suffix = "", color = C.text, size = 44, decimals = 0,
}) => (
  <span style={{ fontFamily: MONO, fontWeight: 800, fontSize: size, color, fontVariantNumeric: "tabular-nums" }}>
    {prefix}{(to * Math.max(0, Math.min(1, p))).toFixed(decimals)}{suffix}
  </span>
);

export const Type: React.FC<{ text: string; p: number; size?: number; color?: string; mono?: boolean }> = ({
  text, p, size = 27, color = C.text, mono,
}) => {
  const frame = useCurrentFrame();
  const n = Math.round(text.length * Math.max(0, Math.min(1, p)));
  const cursor = p > 0 && p < 1 && Math.floor(frame / 8) % 2 === 0;
  return (
    <span style={{ fontFamily: mono ? MONO : SANS, fontSize: size, color, lineHeight: 1.35 }}>
      {text.slice(0, n)}{cursor ? "▌" : ""}
    </span>
  );
};

export const Bg: React.FC<{ accent?: string }> = ({ accent = C.pix }) => {
  const frame = useCurrentFrame();
  const pulse = (Math.sin(frame * 0.02) + 1) / 2;
  const scanY = (frame * 1.15) % (BH + 240) - 120;
  return (
    <AbsoluteFill style={{ background: `radial-gradient(ellipse at 50% 22%, ${C.bg2} 0%, ${C.bg1} 55%, ${C.bg0} 100%)` }}>
      <AbsoluteFill style={{
        backgroundImage: `linear-gradient(${C.line} 1px, transparent 1px), linear-gradient(90deg, ${C.line} 1px, transparent 1px)`,
        backgroundSize: "64px 64px", opacity: 0.5,
        maskImage: "radial-gradient(ellipse at center, black 40%, transparent 92%)",
      }} />
      <AbsoluteFill style={{ background: `radial-gradient(circle at 50% 14%, ${mix(C.bg1, accent, 0.4)} 0%, transparent 46%)`, opacity: 0.28 + pulse * 0.18 }} />
      {/* full-frame slow scanline — the vision-lab heartbeat */}
      <div style={{ position: "absolute", left: 0, top: scanY, width: "100%", height: 2, background: mix(C.bg0, accent, 0.7), opacity: 0.28, boxShadow: `0 0 24px ${mix(C.bg0, accent, 0.6)}` }} />
    </AbsoluteFill>
  );
};

export const Stage: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { width } = useVideoConfig();
  return (
    <AbsoluteFill style={{ alignItems: "center", justifyContent: "center" }}>
      <div style={{ width: BW, height: BH, transform: `scale(${width / BW})`, position: "relative" }}>{children}</div>
    </AbsoluteFill>
  );
};

export const Kicker: React.FC<{ text: string; color?: string; cx?: boolean; o?: number }> = ({ text, color = C.pix, cx, o = 1 }) => (
  <div style={{ display: "flex", alignItems: "center", justifyContent: cx ? "center" : "flex-start", gap: 14, opacity: o }}>
    <div style={{ width: 40, height: 4, borderRadius: 2, background: color }} />
    <div style={{ fontFamily: MONO, letterSpacing: 6, fontSize: 22, color, textTransform: "uppercase", fontWeight: 700 }}>{text}</div>
  </div>
);

export const Head: React.FC<{ kicker: string; title: string; color?: string; o?: number }> = ({ kicker, title, color = C.pix, o = 1 }) => (
  <div style={{ position: "absolute", left: 100, top: 54, right: 100 }}>
    <Kicker text={kicker} color={color} o={o} />
    <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 52, color: C.text, marginTop: 12, letterSpacing: -1.5, opacity: o }}>{title}</div>
  </div>
);

export const Foot: React.FC<{ p: number; children: React.ReactNode }> = ({ p, children }) => (
  <div style={{
    position: "absolute", left: 100, top: 924, right: 100, fontFamily: MONO, fontSize: 23,
    color: C.muted, opacity: p, lineHeight: 1.4, transform: `translateY(${(1 - p) * 14}px)`,
  }}>{children}</div>
);

/** Panel card with tinted border. */
export const Card: React.FC<{
  x: number; y: number; w: number; h?: number; color?: string; o?: number; pad?: string;
  children: React.ReactNode; glow?: boolean;
}> = ({ x, y, w, h, color = C.pix, o = 1, pad = "24px 28px", children, glow }) => {
  const frame = useCurrentFrame();
  return (
    <div style={{
      position: "absolute", left: x, top: y, width: w, height: h, borderRadius: 20,
      background: mix(C.panel, color, 0.09), border: `2.5px solid ${color}`, padding: pad, boxSizing: "border-box",
      opacity: o, transform: `translateY(${(1 - o) * 22}px)`,
      boxShadow: glow ? `0 0 60px ${mix(C.bg0, color, 0.32 + Math.sin(frame * 0.06) * 0.08)}` : "none",
    }}>{children}</div>
  );
};
