/**
 * primitives.tsx — the Explainer Video Studio scene engine.
 *
 * Battle-tested primitives distilled from the fine-tuning (FTScenes) and
 * computer-vision (CVScenes) gold-reference videos. Every scene set builds on
 * these. The two non-negotiable rules they encode:
 *
 *   1. DURATION-AWARE PHASES — animations are keyed to fractions of the scene's
 *      full narration length (`useP(dur)`), never to fixed frame numbers, so a
 *      scene keeps developing for its whole beat instead of freezing after 2s.
 *   2. CONTINUOUS MOTION — Flow particles, dash-marching Wires, scan beams and
 *      sine breathing run forever, so no frame of the video is ever static.
 *
 * Determinism: never call Math.random() in render — use rnd(i, j, s).
 * Performance: no CSS filter/backdrop-filter (esp. blur) — gradients + shadows only.
 */
import React from "react";
import { AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";

// ---------------------------------------------------------------- theme
/** Base palette. Scene sets create their own identity via makeTheme(). */
export interface Theme {
  bg0: string; bg1: string; bg2: string; panel: string;
  text: string; muted: string; line: string;
  accent: string; // the video's primary identity color
}

export const makeTheme = (t: Partial<Theme> = {}): Theme => ({
  bg0: "#05060C", bg1: "#0A0D18", bg2: "#12172A", panel: "#181D33",
  text: "#EEF1FB", muted: "#8B93B0", line: "rgba(255,255,255,0.08)",
  accent: "#FFD166",
  ...t,
});

// 'Kohinoor Telugu' (a macOS SYSTEM font — no loading/delayRender, so it can never
// stall a render) is appended so Telugu glyphs fall through to it per-glyph, while
// Latin brand names / ₹ / numbers stay in the Latin face. Web-font loading of Noto
// Sans Telugu proved unreliable under 8-worker renders (delayRender timeouts).
export const MONO = "ui-monospace, 'SF Mono', Menlo, 'Kohinoor Telugu', monospace";
export const SANS = "'Space Grotesk', Inter, 'Kohinoor Telugu', system-ui, sans-serif";
export const BW = 1920, BH = 1080;
export const CL = { extrapolateLeft: "clamp" as const, extrapolateRight: "clamp" as const };

export function mix(a: string, b: string, t: number) {
  const pa = a.replace("#", "").match(/\w\w/g)!.map((x) => parseInt(x, 16));
  const pb = b.replace("#", "").match(/\w\w/g)!.map((x) => parseInt(x, 16));
  const c = pa.map((v, i) => Math.round(v + (pb[i] - v) * Math.max(0, Math.min(1, t))));
  return `rgb(${c[0]},${c[1]},${c[2]})`;
}

// ---------------------------------------------------------------- timing
/**
 * THE core helper. `dur` is the scene's narration length in seconds (the build
 * script injects it into every cut's props). p(a, b) maps fractions [a..b] of
 * the WHOLE scene to 0..1. Example: a reveal at p(0.6, 0.7) fires 60% of the
 * way through the narration — however long the narration is.
 */
export const useP = (dur?: unknown) => {
  const frame = useCurrentFrame();
  const F = Math.max(45, (typeof dur === "number" ? dur : 14) * 30);
  return (a: number, b: number) => interpolate(frame, [a * F, b * F], [0, 1], CL);
};

/** Spring pop that starts at fraction `at` of the scene. */
export const usePop = (dur?: unknown) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const F = Math.max(45, (typeof dur === "number" ? dur : 14) * 30);
  return (at: number) =>
    spring({ frame: frame - Math.round(at * F), fps, config: { damping: 13, stiffness: 110 } });
};

/** Deterministic hash noise in [0,1). Safe across render threads/frames. */
export const rnd = (i: number, j: number, s = 0) => {
  const x = Math.sin(i * 127.1 + j * 311.7 + s * 74.7) * 43758.5453;
  return x - Math.floor(x);
};

// ---------------------------------------------------------------- motion
/** Continuous particle stream along a straight or curved path. Never stops. */
export const Flow: React.FC<{
  x1: number; y1: number; x2: number; y2: number; curve?: number;
  color: string; n?: number; speed?: number; size?: number; o?: number;
}> = ({ x1, y1, x2, y2, curve = 0, color, n = 7, speed = 0.011, size = 11, o = 1 }) => {
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

/** Connector that draws itself in as `p` goes 0→1, then dash-marches forever. */
export const Wire: React.FC<{
  x1: number; y1: number; x2: number; y2: number; p: number; curve?: number;
  color: string; w?: number; arrow?: boolean;
}> = ({ x1, y1, x2, y2, p, curve = 0, color, w = 3, arrow = true }) => {
  const frame = useCurrentFrame();
  const mx = (x1 + x2) / 2, my = (y1 + y2) / 2 - curve;
  const len = Math.hypot(x2 - x1, y2 - y1) + Math.abs(curve);
  const id = `w${color.replace(/[^a-z0-9]/gi, "")}${Math.round(curve)}`;
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

/** Animated numeric counter driven by a phase p. */
export const Counter: React.FC<{
  p: number; to: number; prefix?: string; suffix?: string; color: string; size?: number; decimals?: number; comma?: boolean;
}> = ({ p, to, prefix = "", suffix = "", color, size = 44, decimals = 0, comma = false }) => {
  const v = to * Math.max(0, Math.min(1, p));
  const s = comma
    ? v.toLocaleString("en-US", { minimumFractionDigits: decimals, maximumFractionDigits: decimals })
    : v.toFixed(decimals);
  return (
    <span style={{ fontFamily: MONO, fontWeight: 800, fontSize: size, color, fontVariantNumeric: "tabular-nums" }}>
      {prefix}{s}{suffix}
    </span>
  );
};

/** Typewriter text driven by a phase p, with blinking cursor while typing. */
export const Type: React.FC<{ text: string; p: number; size?: number; color: string; mono?: boolean }> = ({
  text, p, size = 27, color, mono,
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

// ---------------------------------------------------------------- layout
/** Full-bleed animated background: gradient wash + faint grid + drifting light. */
export const Bg: React.FC<{ theme: Theme; accent?: string }> = ({ theme, accent }) => {
  const frame = useCurrentFrame();
  const ac = accent || theme.accent;
  const pulse = (Math.sin(frame * 0.02) + 1) / 2;
  const sweep = ((frame * 2.2) % (BW + 900)) - 450;
  return (
    <AbsoluteFill style={{ background: `radial-gradient(ellipse at 50% 24%, ${theme.bg2} 0%, ${theme.bg1} 55%, ${theme.bg0} 100%)` }}>
      <AbsoluteFill style={{
        backgroundImage: `linear-gradient(${theme.line} 1px, transparent 1px), linear-gradient(90deg, ${theme.line} 1px, transparent 1px)`,
        backgroundSize: "68px 68px", opacity: 0.5,
        maskImage: "radial-gradient(ellipse at center, black 40%, transparent 92%)",
      }} />
      <AbsoluteFill style={{ background: `radial-gradient(circle at 50% 16%, ${mix(theme.bg1, ac, 0.4)} 0%, transparent 46%)`, opacity: 0.3 + pulse * 0.2 }} />
      <div style={{
        position: "absolute", top: -200, left: sweep, width: 340, height: BH + 400, transform: "rotate(14deg)",
        background: `linear-gradient(90deg, transparent, ${mix(theme.bg0, ac, 0.5)}22, transparent)`,
      }} />
    </AbsoluteFill>
  );
};

/** 1920×1080 design stage scaled to output width — author in fixed coordinates. */
export const Stage: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { width } = useVideoConfig();
  return (
    <AbsoluteFill style={{ alignItems: "center", justifyContent: "center" }}>
      <div style={{ width: BW, height: BH, transform: `scale(${width / BW})`, position: "relative" }}>{children}</div>
    </AbsoluteFill>
  );
};

// Vertical (9:16 Shorts/Reels) design space — see skills/10-vertical.md
export const VW = 1080, VH = 1920;

/** 1080×1920 design stage for vertical-first scenes — author in fixed coordinates. */
export const VStage: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { width } = useVideoConfig();
  return (
    <AbsoluteFill style={{ alignItems: "center", justifyContent: "center" }}>
      <div style={{ width: VW, height: VH, transform: `scale(${width / VW})`, position: "relative" }}>{children}</div>
    </AbsoluteFill>
  );
};

/** "landscape" | "portrait" — for the rare responsive scene shared across formats. */
export const useAspect = () => {
  const { width, height } = useVideoConfig();
  return height > width ? ("portrait" as const) : ("landscape" as const);
};

export const Kicker: React.FC<{ theme: Theme; text: string; color?: string; cx?: boolean; o?: number }> = ({
  theme, text, color, cx, o = 1,
}) => (
  <div style={{ display: "flex", alignItems: "center", justifyContent: cx ? "center" : "flex-start", gap: 14, opacity: o }}>
    <div style={{ width: 40, height: 4, borderRadius: 2, background: color || theme.accent }} />
    <div style={{ fontFamily: MONO, letterSpacing: 6, fontSize: 22, color: color || theme.accent, textTransform: "uppercase", fontWeight: 700 }}>{text}</div>
  </div>
);

export const Head: React.FC<{ theme: Theme; kicker: string; title: string; color?: string; o?: number }> = ({
  theme, kicker, title, color, o = 1,
}) => (
  <div style={{ position: "absolute", left: 100, top: 54, right: 100 }}>
    <Kicker theme={theme} text={kicker} color={color} o={o} />
    <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 52, color: theme.text, marginTop: 12, letterSpacing: -1.5, opacity: o }}>{title}</div>
  </div>
);

/** Footnote strip pinned to the bottom of the Stage — reinforces the narration. */
export const Foot: React.FC<{ theme: Theme; p: number; children: React.ReactNode }> = ({ theme, p, children }) => (
  <div style={{
    position: "absolute", left: 100, top: 924, right: 100, fontFamily: MONO, fontSize: 23,
    color: theme.muted, opacity: p, lineHeight: 1.4, transform: `translateY(${(1 - p) * 14}px)`,
  }}>{children}</div>
);

/** Tinted panel card with slide-up reveal and optional breathing glow. */
export const Card: React.FC<{
  theme: Theme; x: number; y: number; w: number; h?: number; color: string; o?: number; pad?: string;
  children: React.ReactNode; glow?: boolean;
}> = ({ theme, x, y, w, h, color, o = 1, pad = "24px 28px", children, glow }) => {
  const frame = useCurrentFrame();
  return (
    <div style={{
      position: "absolute", left: x, top: y, width: w, height: h, borderRadius: 20,
      background: mix(theme.panel, color, 0.09), border: `2.5px solid ${color}`, padding: pad, boxSizing: "border-box",
      opacity: o, transform: `translateY(${(1 - o) * 22}px)`,
      boxShadow: glow ? `0 0 60px ${mix(theme.bg0, color, 0.32 + Math.sin(frame * 0.06) * 0.08)}` : "none",
    }}>{children}</div>
  );
};

// ---------------------------------------------------------------- data viz
export type Grid = number[][];

/** Build a value grid from character rows — for pixel-art / heatmap scenes. */
export const gridFromRows = (rows: string[], map: Record<string, number>): Grid =>
  rows.map((r) => [...r].map((ch) => map[ch] ?? 0));

/** Number-grid heatmap with scan-order reveal and an optional highlight window. */
export const PixGrid: React.FC<{
  theme: Theme; g: Grid; x: number; y: number; cell: number; reveal?: number;
  values?: boolean; tint?: string; gap?: number; label?: string; labelColor?: string;
  hi?: { r: number; c: number; size: number; color: string } | null; o?: number;
}> = ({ theme, g, x, y, cell, reveal = 1, values, tint, gap = 2, label, labelColor, hi = null, o = 1 }) => {
  const rows = g.length, cols = g[0].length, total = rows * cols;
  const labelH = label ? Math.max(19, cell * 0.5) + 8 : 0;
  return (
    <div style={{ position: "absolute", left: x, top: y, opacity: o }}>
      {label && (
        <div style={{ fontFamily: MONO, fontSize: Math.max(19, cell * 0.5), color: labelColor || theme.muted, marginBottom: 8 }}>{label}</div>
      )}
      <div style={{ display: "grid", gridTemplateColumns: `repeat(${cols}, ${cell}px)`, gap }}>
        {g.flat().map((v, i) => {
          const on = i / total <= reveal ? 1 : 0;
          const bgc = tint ? mix(theme.bg1, tint, v / 255) : `rgb(${v},${v},${v})`;
          return (
            <div key={i} style={{
              width: cell, height: cell, borderRadius: Math.max(2, cell * 0.12),
              background: bgc, opacity: on, display: "flex", alignItems: "center", justifyContent: "center",
              border: `1px solid rgba(200,220,255,0.06)`,
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
          position: "absolute", left: hi.c * (cell + gap) - 3, top: labelH + hi.r * (cell + gap) - 3,
          width: hi.size * (cell + gap) - gap + 6, height: hi.size * (cell + gap) - gap + 6,
          border: `3px solid ${hi.color}`, borderRadius: 8, boxShadow: `0 0 22px ${hi.color}`,
        }} />
      )}
    </div>
  );
};

/** Viewfinder corner brackets with a slow breathing pulse. */
export const Brackets: React.FC<{ x: number; y: number; w: number; h: number; color: string; o?: number; len?: number }> = ({
  x, y, w, h, color, o = 1, len = 34,
}) => {
  const frame = useCurrentFrame();
  const b = Math.sin(frame * 0.05) * 4;
  const s = 4;
  return (
    <div style={{ position: "absolute", left: x - b, top: y - b, width: w + b * 2, height: h + b * 2, opacity: o, pointerEvents: "none" }}>
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

/** Scan beam sweeping down a region forever. */
export const ScanBeam: React.FC<{ theme: Theme; x: number; y: number; w: number; h: number; color: string; o?: number; speed?: number }> = ({
  theme, x, y, w, h, color, o = 1, speed = 0.55,
}) => {
  const frame = useCurrentFrame();
  const t = ((frame * speed) % (h + 60)) - 30;
  return (
    <div style={{ position: "absolute", left: x, top: y, width: w, height: h, overflow: "hidden", opacity: o, pointerEvents: "none" }}>
      <div style={{ position: "absolute", left: 0, top: t, width: "100%", height: 3, background: color, boxShadow: `0 0 18px ${color}`, opacity: 0.85 }} />
      <div style={{ position: "absolute", left: 0, top: t - 44, width: "100%", height: 44, background: `linear-gradient(180deg, transparent, ${mix(theme.bg0, color, 0.45)}44)` }} />
    </div>
  );
};
