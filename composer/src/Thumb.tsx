/**
 * Thumb.tsx — 1280×720 YouTube thumbnail composition (id "Thumbnail").
 * Props-driven, rendered as a still: `remotion still Thumbnail out.png --props=...`.
 * Same visual identity as the videos (dark theme, accent glow, big Telugu headline).
 */
import React from "react";
import { AbsoluteFill } from "remotion";
import { makeTheme, mix, MONO, SANS } from "./lib/primitives";

export interface ThumbProps {
  badge?: string;      // series chip, e.g. "స్టాక్ మార్కెట్"
  title?: string;      // big Telugu headline (1–2 lines)
  sub?: string;        // small subtitle under underline
  accent?: string;     // hex accent
  hook?: string;       // big right-side hook (number / % / emoji)
  hookSmall?: string;  // small label under the hook
  ep?: string;         // corner badge, e.g. "PART 05" / "BONUS"
  brand?: string;      // bottom-left brand line
  bg2?: string;        // optional bg tint override
  badgeHi?: boolean;   // render the badge as a filled highlighter pill (dark text on accent)
}

const T = makeTheme({});

export const ThumbCard: React.FC<ThumbProps> = ({
  badge = "", title = "", sub = "", accent = "#34D399", hook = "", hookSmall = "", ep = "", brand = "తెలుగులో · FULL COURSE", badgeHi = false,
}) => {
  const lines = title.split("\n");
  return (
    <AbsoluteFill style={{ background: `radial-gradient(ellipse at 28% 30%, ${mix(T.bg2, accent, 0.18)} 0%, ${T.bg1} 52%, ${T.bg0} 100%)` }}>
      {/* faint grid */}
      <AbsoluteFill style={{
        backgroundImage: `linear-gradient(${T.line} 1px, transparent 1px), linear-gradient(90deg, ${T.line} 1px, transparent 1px)`,
        backgroundSize: "60px 60px", opacity: 0.4,
        maskImage: "radial-gradient(ellipse at center, black 45%, transparent 92%)",
      }} />
      {/* accent glow blob behind hook */}
      <div style={{ position: "absolute", right: -120, top: 120, width: 620, height: 620, borderRadius: "50%",
        background: `radial-gradient(circle, ${mix(T.bg0, accent, 0.55)} 0%, transparent 62%)`, opacity: 0.85 }} />
      {/* left accent bar */}
      <div style={{ position: "absolute", left: 0, top: 0, bottom: 0, width: 16, background: accent }} />

      {/* series badge */}
      {badge && (
        badgeHi ? (
          <div style={{ position: "absolute", left: 72, top: 52, background: accent, borderRadius: 12,
            padding: "12px 26px", boxShadow: `0 0 46px ${mix(T.bg0, accent, 0.8)}` }}>
            <span style={{ fontFamily: MONO, fontWeight: 800, fontSize: 38, letterSpacing: 4, color: T.bg0, textTransform: "uppercase" }}>{badge}</span>
          </div>
        ) : (
          <div style={{ position: "absolute", left: 72, top: 60, display: "flex", alignItems: "center", gap: 14 }}>
            <div style={{ width: 46, height: 6, borderRadius: 3, background: accent }} />
            <span style={{ fontFamily: MONO, fontWeight: 700, fontSize: 30, letterSpacing: 3, color: accent, textTransform: "uppercase" }}>{badge}</span>
          </div>
        )
      )}

      {/* episode / bonus badge (top-right) */}
      {ep && (
        <div style={{ position: "absolute", right: 60, top: 54, background: mix(T.panel, accent, 0.18),
          border: `3px solid ${accent}`, borderRadius: 18, padding: "12px 26px",
          fontFamily: MONO, fontWeight: 800, fontSize: 32, letterSpacing: 2, color: accent }}>{ep}</div>
      )}

      {/* headline */}
      <div style={{ position: "absolute", left: 72, top: 168, width: 820 }}>
        {lines.map((ln, i) => (
          <div key={i} style={{ fontFamily: SANS, fontWeight: 800, fontSize: 104, lineHeight: 1.08, letterSpacing: -1,
            color: i === lines.length - 1 && lines.length > 1 ? accent : T.text,
            textShadow: i === lines.length - 1 && lines.length > 1 ? `0 0 46px ${mix(T.bg0, accent, 0.7)}` : "none" }}>{ln}</div>
        ))}
        <div style={{ height: 9, width: 300, borderRadius: 5, background: `linear-gradient(90deg, ${accent}, ${mix(accent, T.bg0, 0.5)})`, marginTop: 26 }} />
        {sub && <div style={{ fontFamily: SANS, fontWeight: 600, fontSize: 38, color: T.muted, marginTop: 24, maxWidth: 760, lineHeight: 1.25 }}>{sub}</div>}
      </div>

      {/* right hook */}
      {hook && (
        <div style={{ position: "absolute", right: 70, top: 0, bottom: 0, width: 380, display: "flex", flexDirection: "column",
          alignItems: "center", justifyContent: "center", zIndex: 2 }}>
          <div style={{ fontFamily: MONO, fontWeight: 800, fontSize: hook.length > 4 ? 120 : 200, lineHeight: 0.95, color: accent,
            textShadow: `0 0 60px ${mix(T.bg0, accent, 0.85)}`, textAlign: "center" }}>{hook}</div>
          {hookSmall && <div style={{ fontFamily: SANS, fontWeight: 700, fontSize: 34, color: T.text, marginTop: 18, textAlign: "center", maxWidth: 360, lineHeight: 1.2 }}>{hookSmall}</div>}
        </div>
      )}

      {/* brand corner */}
      <div style={{ position: "absolute", left: 72, bottom: 46, fontFamily: MONO, fontWeight: 700, fontSize: 26, color: T.muted, letterSpacing: 2 }}>
        {brand}
      </div>
    </AbsoluteFill>
  );
};
