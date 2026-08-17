/**
 * VShort.tsx — 9:16 vertical Short/Reel (id "Short"), continuing the LLM-From-Scratch /
 * Math-for-ML style: a CH/PART badge, a big glowing chapter title + subtitle, an animated
 * list of highlights, a keyword tag, and a brand line. NO captions. Plays a short hook audio.
 */
import React from "react";
import { AbsoluteFill, Audio, staticFile, useCurrentFrame, interpolate } from "remotion";
import { makeTheme, mix, useP, usePop, rnd, MONO, SANS } from "./lib/primitives";

export interface ShortProps {
  badge?: string;        // "CH 09" / "PART 03" / "SECTOR"
  title?: string;        // big chapter title (1–2 lines via \n)
  sub?: string;          // subtitle under title
  keyword?: string;      // bottom keyword tag
  accent?: string;       // hex accent
  brand?: string;        // bottom brand line
  highlights?: string[]; // 3–4 short points
  audioSrc?: string;     // path under public/ (e.g. "short/x.wav")
  durationSec?: number;
}

const T = makeTheme({});
const VW = 1080, VH = 1920;

export const VShort: React.FC<ShortProps> = ({
  badge = "", title = "", sub = "", keyword = "", accent = "#34D399", brand = "",
  highlights = [], audioSrc, durationSec = 20,
}) => {
  const frame = useCurrentFrame();
  const p = useP(durationSec);
  const pop = usePop(durationSec);
  const lines = title.split("\n");
  return (
    <AbsoluteFill style={{ background: `radial-gradient(ellipse at 50% 26%, ${mix(T.bg2, accent, 0.16)} 0%, ${T.bg1} 55%, ${T.bg0} 100%)` }}>
      {/* faint grid */}
      <AbsoluteFill style={{
        backgroundImage: `linear-gradient(${T.line} 1px, transparent 1px), linear-gradient(90deg, ${T.line} 1px, transparent 1px)`,
        backgroundSize: "72px 72px", opacity: 0.35,
        maskImage: "radial-gradient(ellipse at center, black 45%, transparent 92%)",
      }} />
      {/* drifting particles */}
      {Array.from({ length: 16 }).map((_, i) => {
        const a = frame * 0.008 + (i / 16) * Math.PI * 2;
        return <div key={i} style={{
          position: "absolute", left: 540 + Math.cos(a) * (360 + i * 14) - 5,
          top: 960 + Math.sin(a) * (720 + i * 8) - 5, width: 10, height: 10, borderRadius: 10,
          background: accent, opacity: 0.06 + rnd(i, 3) * 0.12, boxShadow: `0 0 12px ${accent}`,
        }} />;
      })}

      {/* badge */}
      <div style={{ position: "absolute", top: 210, left: 0, right: 0, display: "flex", justifyContent: "center", opacity: p(0.0, 0.08), transform: `scale(${0.9 + pop(0) * 0.1})` }}>
        <div style={{ background: mix(T.panel, accent, 0.22), border: `3px solid ${accent}`, borderRadius: 999,
          padding: "14px 40px", fontFamily: MONO, fontWeight: 800, fontSize: 40, letterSpacing: 4, color: accent }}>{badge}</div>
      </div>

      {/* title block */}
      <div style={{ position: "absolute", top: 330, left: 70, right: 70, textAlign: "center" }}>
        {lines.map((ln, i) => (
          <div key={i} style={{ fontFamily: SANS, fontWeight: 800, fontSize: 82, lineHeight: 1.08, letterSpacing: -1.5,
            color: accent, textShadow: `0 0 54px ${mix(T.bg0, accent, 0.7)}`,
            opacity: p(0.06 + i * 0.05, 0.18 + i * 0.05), transform: `translateY(${(1 - p(0.06 + i * 0.05, 0.18 + i * 0.05)) * 26}px)` }}>{ln}</div>
        ))}
        <div style={{ height: 7, width: interpolate(p(0.2, 0.42), [0, 1], [0, 360]), background: `linear-gradient(90deg, ${accent}, ${mix(accent, T.bg0, 0.5)})`, borderRadius: 4, margin: "34px auto" }} />
        {sub && <div style={{ fontFamily: SANS, fontWeight: 600, fontSize: 44, color: T.text, opacity: p(0.28, 0.42), lineHeight: 1.3 }}>{sub}</div>}
      </div>

      {/* highlights — revealed progressively across the whole minute, with an active glow */}
      <div style={{ position: "absolute", top: 800, left: 84, right: 84, display: "flex", flexDirection: "column", gap: 24 }}>
        {highlights.slice(0, 6).map((h, i) => {
          const n = Math.max(1, Math.min(6, highlights.length));
          const at = 0.14 + i * (0.66 / n);
          const o = p(at, at + 0.06);
          const active = frame >= at * (durationSec * 30) && frame < (0.14 + (i + 1) * (0.66 / n)) * (durationSec * 30);
          return (
            <div key={i} style={{ display: "flex", alignItems: "center", gap: 24, opacity: o, transform: `translateX(${(1 - o) * -28}px) scale(${active ? 1.02 : 1})`,
              background: mix(T.panel, accent, active ? 0.16 : 0.08), border: `2.5px solid ${mix(T.bg2, accent, active ? 1 : 0.5)}`, borderLeft: `8px solid ${accent}`,
              borderRadius: 18, padding: "22px 30px",
              boxShadow: active ? `0 0 30px ${mix(T.bg0, accent, 0.35)}` : "none" }}>
              <span style={{ fontFamily: MONO, fontWeight: 800, fontSize: 36, color: accent }}>{i + 1}</span>
              <span style={{ fontFamily: SANS, fontWeight: 700, fontSize: 38, color: T.text, lineHeight: 1.28 }}>{h}</span>
            </div>
          );
        })}
      </div>

      {/* playback progress bar (bottom) */}
      <div style={{ position: "absolute", bottom: 44, left: 84, right: 84, height: 8, borderRadius: 4, background: mix(T.panel, accent, 0.1), overflow: "hidden" }}>
        <div style={{ height: "100%", width: `${Math.min(100, (frame / (durationSec * 30)) * 100)}%`, background: `linear-gradient(90deg, ${accent}, ${mix(accent, T.bg0, 0.4)})` }} />
      </div>

      {/* keyword tag */}
      {keyword && (
        <div style={{ position: "absolute", top: 1600, left: 0, right: 0, display: "flex", alignItems: "center", justifyContent: "center", gap: 18, opacity: p(0.55, 0.7) }}>
          <div style={{ width: 60, height: 6, borderRadius: 3, background: accent }} />
          <span style={{ fontFamily: MONO, fontWeight: 800, fontSize: 40, letterSpacing: 2, color: accent, textTransform: "uppercase" }}>{keyword}</span>
        </div>
      )}

      {/* brand + swipe cue */}
      <div style={{ position: "absolute", top: 1730, left: 0, right: 0, textAlign: "center", fontFamily: MONO, fontWeight: 700, fontSize: 32, letterSpacing: 3, color: T.muted, opacity: p(0.6, 0.75) }}>{brand}</div>
      <div style={{ position: "absolute", top: 1800, left: 0, right: 0, textAlign: "center", fontFamily: SANS, fontWeight: 700, fontSize: 34, color: accent, opacity: 0.55 + Math.sin(frame * 0.12) * 0.35 }}>▲ full video on the channel</div>

      {audioSrc && <Audio src={staticFile(audioSrc)} />}
    </AbsoluteFill>
  );
};
