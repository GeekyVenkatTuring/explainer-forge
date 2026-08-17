/**
 * Captions.tsx — burned-in subtitle overlay for the Explainer timeline.
 *
 * Driven by `cues`: an array of [startSeconds, endSeconds, text] entries in
 * composition-local time (build.py emits them per chapter). The active cue is
 * shown in the bottom UI-safe band as a matte pill + sans text (≤2 lines).
 * Deterministic (time-derived only), no CSS filter/backdrop-filter — safe for
 * parallel-worker rendering per the project contract.
 */
import React from "react";
import { AbsoluteFill, useCurrentFrame, useVideoConfig } from "remotion";

// Telugu-capable stack: Latin stays in Space Grotesk, Telugu falls through to the
// macOS system font Kohinoor Telugu (no web-font loading — can't stall a render).
const SANS = "'Space Grotesk', Inter, 'Kohinoor Telugu', system-ui, sans-serif";

export type Cue = [number, number, string];

export const Captions: React.FC<{ cues?: Cue[] }> = ({ cues = [] }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = frame / fps;

  // active cue: last one whose window contains t (cues are ordered)
  let active: Cue | null = null;
  for (const c of cues) {
    if (t >= c[0] && t < c[1]) active = c;
  }
  if (!active) return null;

  const [start, end, text] = active;
  // quick fade in/out at the cue edges (120ms), clamped
  const fadeIn = Math.min(1, (t - start) / 0.12);
  const fadeOut = Math.min(1, (end - t) / 0.12);
  const o = Math.max(0, Math.min(1, Math.min(fadeIn, fadeOut)));

  return (
    <AbsoluteFill style={{ justifyContent: "flex-end", alignItems: "center", pointerEvents: "none" }}>
      <div
        style={{
          maxWidth: 1500,
          margin: "0 auto 30px",
          padding: "12px 32px",
          borderRadius: 14,
          background: "rgba(4,7,10,0.84)",
          border: "1.5px solid rgba(160,220,255,0.16)",
          boxShadow: "0 8px 40px rgba(0,0,0,0.55)",
          opacity: o,
          textAlign: "center",
        }}
      >
        <div
          style={{
            fontFamily: SANS,
            fontWeight: 600,
            fontSize: 33,
            lineHeight: 1.26,
            color: "#F4FAFF",
            letterSpacing: -0.3,
            whiteSpace: "pre-line",
            textShadow: "0 2px 10px rgba(0,0,0,0.7)",
          }}
        >
          {text}
        </div>
      </div>
    </AbsoluteFill>
  );
};

export default Captions;
