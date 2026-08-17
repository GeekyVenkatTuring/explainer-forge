/**
 * CVScenesA.tsx — Computer Vision explainer scenes, parts 1–3:
 * images-as-numbers, classical image processing, and CNNs.
 * All image operations are computed live from CVShared's pixel engine.
 */
import React from "react";
import { AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import {
  C, MONO, SANS, BW, BH, CL, mix, useP, rnd,
  CAT12, SEVEN8, gmap, boxBlur3, conv3, absNorm, sobelMag, maxPool2,
  SOBEL_X, SOBEL_Y, K_BLUR, K_SHARP, K_EDGE,
  PixGrid, Brackets, ScanBeam, Flow, Wire, Counter, Stage, Kicker, Head, Foot, Card,
} from "./CVShared";

// Precomputed image ops (static — module scope)
const CAT_BRIGHT = gmap(CAT12, (v) => v + 60);
const CAT_CONTRAST = gmap(CAT12, (v) => (v - 128) * 1.8 + 128);
const CAT_BLUR = boxBlur3(boxBlur3(CAT12));
const CAT_EDGES = sobelMag(CAT12);
const CAT_GX = absNorm(conv3(CAT12, SOBEL_X));
const CAT_GY = absNorm(conv3(CAT12, SOBEL_Y));
const SEVEN_EDGE = absNorm(conv3(SEVEN8, K_EDGE));
const SEVEN_BLUR = absNorm(conv3(SEVEN8, K_BLUR));
const SEVEN_SHARP = absNorm(conv3(SEVEN8, K_SHARP));

// cv_title ---------------------------------------------------------------------
export const CvTitle: React.FC<{ dur?: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const p = useP(dur);
  const pop = spring({ frame, fps, config: { damping: 14, stiffness: 90 } });
  // noise → cat resolve, forever breathing
  const resolve = p(0.1, 0.55);
  const g = CAT12.map((row, i) => row.map((v, j) => {
    const nz = rnd(i, j, Math.floor(frame / 4)) * 255;
    const a = 1 - resolve;
    return Math.round(v * (1 - a) + nz * a);
  }));
  return (
    <AbsoluteFill style={{ alignItems: "center", justifyContent: "center" }}>
      <PixGrid g={g} x={1330} y={300} cell={38} tint={C.pix} o={0.9 * p(0.02, 0.12)} />
      <Brackets x={1316} y={286} w={12 * 40 + 20} h={12 * 40 + 20} color={C.pix} o={p(0.05, 0.15)} />
      <ScanBeam x={1330} y={300} w={12 * 40 - 4} h={12 * 40 - 4} color={C.pix} o={p(0.1, 0.2)} />
      <PixGrid g={CAT_EDGES} x={130} y={800} cell={18} tint={C.classic} o={0.35 * p(0.15, 0.3)} />
      <div style={{ textAlign: "left", transform: `scale(${0.92 + pop * 0.08})`, position: "absolute", left: 150, top: 250, width: 1050 }}>
        <Kicker text="PIXELS → PERCEPTION · FULL COURSE" />
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 124, lineHeight: 1.02, letterSpacing: -3, color: C.text, marginTop: 24 }}>
          <div>Computer</div>
          <div style={{ color: C.pix, textShadow: `0 0 70px ${mix(C.bg0, C.pix, 0.7)}` }}>Vision</div>
        </div>
        <div style={{ height: 5, width: interpolate(p(0.18, 0.45), [0, 1], [0, 560]), background: `linear-gradient(90deg, ${C.pix}, ${C.classic}, ${C.neural}, ${C.gen})`, borderRadius: 3, margin: "30px 0" }} />
        <div style={{ fontFamily: SANS, fontSize: 38, color: C.muted, opacity: p(0.28, 0.5), maxWidth: 950 }}>
          Pixels · filters · CNNs · detection · segmentation · ViT · CLIP · diffusion — end to end
        </div>
      </div>
    </AbsoluteFill>
  );
};

// cv_hook — semantic gap ---------------------------------------------------------
export const CvHook: React.FC<{ dur?: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  return (
    <Stage>
      <Head kicker="THE PROBLEM" title="You see a cat. The computer sees numbers." o={p(0, 0.06)} />
      {/* human side */}
      <Card x={130} y={250} w={560} h={560} color={C.green} o={p(0.05, 0.13)}>
        <div style={{ fontFamily: MONO, fontSize: 23, color: C.muted }}>WHAT YOU SEE</div>
        <div style={{ fontSize: 210, textAlign: "center", marginTop: 40, transform: `scale(${1 + Math.sin(frame * 0.03) * 0.02})` }}>🐱</div>
        <div style={{ textAlign: "center", marginTop: 34, opacity: p(0.12, 0.2) }}>
          <span style={{ fontFamily: SANS, fontWeight: 800, fontSize: 44, color: C.green }}>“cat”</span>
          <span style={{ fontFamily: MONO, fontSize: 25, color: C.muted, marginLeft: 18 }}>~0.1 s, effortless</span>
        </div>
      </Card>
      {/* the gap */}
      <div style={{ position: "absolute", left: 730, top: 430, width: 300, textAlign: "center", opacity: p(0.42, 0.52) }}>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 40, color: C.red }}>the semantic gap</div>
        <div style={{ fontFamily: MONO, fontSize: 23, color: C.muted, marginTop: 12, lineHeight: 1.4 }}>numbers ↔ meaning<br />crossing it = this whole field</div>
        <div style={{ marginTop: 18, fontSize: 44, transform: `translateY(${Math.sin(frame * 0.07) * 6}px)` }}>⚡</div>
      </div>
      {/* machine side */}
      <Card x={1070} y={250} w={720} h={560} color={C.pix} o={p(0.2, 0.3)}>
        <div style={{ fontFamily: MONO, fontSize: 23, color: C.muted }}>WHAT THE COMPUTER SEES</div>
        <div style={{ position: "relative", marginTop: 22 }}>
          <PixGrid g={CAT12} x={20} y={0} cell={40} values reveal={p(0.24, 0.6)} />
        </div>
      </Card>
      <ScanBeam x={1090} y={320} w={680} h={470} color={C.pix} o={p(0.3, 0.4)} />
      <Foot p={p(0.75, 0.85)}>A phone photo is ~12,000,000 of these numbers. Every technique in this video is a way to climb from that grid to “cat.”</Foot>
    </Stage>
  );
};

// cv_divider ----------------------------------------------------------------------
export const CvDivider: React.FC<{ dur?: number; n?: number; title?: string; sub?: string; color?: string }> = ({
  dur, n = 1, title = "SECTION", sub = "", color = C.pix,
}) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  return (
    <Stage>
      <Brackets x={330} y={300} w={1260} h={480} color={color} o={p(0.02, 0.14)} len={54} />
      <ScanBeam x={340} y={310} w={1240} h={460} color={color} o={p(0.05, 0.2)} speed={1.6} />
      <div style={{ position: "absolute", left: 0, right: 0, top: 360, textAlign: "center" }}>
        <div style={{ fontFamily: MONO, fontWeight: 800, fontSize: 34, color, letterSpacing: 10, opacity: p(0.05, 0.15) }}>
          PART {"0" + n}
        </div>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 96, color: C.text, letterSpacing: -2, marginTop: 20, opacity: p(0.12, 0.24), transform: `translateY(${(1 - p(0.12, 0.24)) * 30}px)` }}>
          {title}
        </div>
        <div style={{ height: 5, width: interpolate(p(0.2, 0.5), [0, 1], [0, 420]), background: color, borderRadius: 3, margin: "26px auto" }} />
        <div style={{ fontFamily: SANS, fontSize: 34, color: C.muted, opacity: p(0.3, 0.45) }}>{sub}</div>
      </div>
      {/* progress pips */}
      <div style={{ position: "absolute", left: 0, right: 0, top: 860, display: "flex", justifyContent: "center", gap: 16, opacity: p(0.3, 0.45) }}>
        {[1, 2, 3, 4, 5, 6].map((i) => (
          <div key={i} style={{ width: i === n ? 44 : 14, height: 14, borderRadius: 8, background: i <= n ? color : mix(C.panel, color, 0.15), border: `1.5px solid ${i <= n ? color : C.line}`, transition: "none", opacity: i === n ? 0.7 + Math.sin(frame * 0.1) * 0.3 : 1 }} />
        ))}
      </div>
    </Stage>
  );
};

// cv_pixels ------------------------------------------------------------------------
export const CvPixels: React.FC<{ dur?: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  // magnifier orbits over the grid picking cells
  const mi = Math.floor((frame / 22) % 12), mj = Math.floor((frame / 7) % 12);
  const val = CAT12[mi][mj];
  const chans: [string, string][] = [["R", "#F87171"], ["G", "#34D399"], ["B", "#60A5FA"]];
  return (
    <Stage>
      <Head kicker="THE RAW MATERIAL" title="An image is a block of numbers" o={p(0, 0.06)} />
      {/* grayscale with live probe */}
      <PixGrid g={CAT12} x={150} y={260} cell={42} values reveal={p(0.05, 0.3)} label="grayscale · one number per pixel (0–255)" />
      <PixGrid g={CAT12} x={150} y={260} cell={42} o={0} />
      <div style={{ position: "absolute", left: 150 + mj * 44, top: 260 + 36 + mi * 44 - 3, width: 46, height: 46, border: `3px solid ${C.classic}`, borderRadius: 8, boxShadow: `0 0 20px ${C.classic}`, opacity: p(0.3, 0.38) }} />
      <div style={{ position: "absolute", left: 165, top: 830, fontFamily: MONO, fontSize: 26, color: C.classic, opacity: p(0.3, 0.38) }}>
        pixel[{mi}][{mj}] = <b style={{ fontSize: 32 }}>{val}</b> · {val < 60 ? "dark" : val < 160 ? "mid" : "bright"}
      </div>
      {/* 0..255 ramp */}
      <div style={{ position: "absolute", left: 150, top: 890, width: 530, height: 26, borderRadius: 8, background: "linear-gradient(90deg, #000, #fff)", border: `1.5px solid ${C.line}`, opacity: p(0.1, 0.2) }}>
        <div style={{ position: "absolute", left: `${(val / 255) * 100}%`, top: -9, width: 4, height: 44, background: C.classic, borderRadius: 2, opacity: p(0.3, 0.38) }} />
      </div>
      {/* RGB stack */}
      <div style={{ position: "absolute", left: 900, top: 250, fontFamily: MONO, fontSize: 24, color: C.muted, opacity: p(0.45, 0.55) }}>color = 3 stacked channels</div>
      {chans.map(([nm, col], i) => {
        const o = p(0.48 + i * 0.07, 0.58 + i * 0.07);
        const gg = gmap(CAT12, (v) => (i === 0 ? v : i === 1 ? v * 0.92 : v * 0.8));
        return (
          <div key={nm} style={{ opacity: o }}>
            <PixGrid g={gg} x={900 + i * 130} y={300 + i * 105} cell={22} tint={col} o={o} />
            <div style={{ position: "absolute", left: 900 + i * 130 - 46, top: 300 + i * 105 + 100, fontFamily: MONO, fontWeight: 800, fontSize: 34, color: col, opacity: o }}>{nm}</div>
          </div>
        );
      })}
      <Card x={1470} y={330} w={330} color={C.pix} o={p(0.72, 0.82)} glow>
        <div style={{ fontFamily: MONO, fontSize: 22, color: C.muted }}>a phone photo</div>
        <Counter p={p(0.72, 0.9)} to={12} suffix=" M" color={C.pix} size={54} />
        <div style={{ fontFamily: MONO, fontSize: 22, color: C.muted }}>pixels × 3 channels</div>
        <div style={{ fontFamily: SANS, fontSize: 25, color: C.text, marginTop: 12 }}>height × width × 3<br />= one tensor</div>
      </Card>
      <Foot p={p(0.84, 0.93)}>Every vision algorithm ever built — from Photoshop blur to GPT-4V — is math on this block of numbers.</Foot>
    </Stage>
  );
};

// cv_tasks — the task zoo ------------------------------------------------------------
export const CvTasks: React.FC<{ dur?: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const tasks = [
    { name: "Classification", q: "what is it?", icon: "🏷️", c: C.pix, demo: "label" },
    { name: "Detection", q: "what is where?", icon: "📦", c: C.green, demo: "box" },
    { name: "Segmentation", q: "which pixels?", icon: "🎨", c: C.neural, demo: "mask" },
    { name: "Tracking", q: "where did it go?", icon: "🎯", c: C.classic, demo: "track" },
    { name: "Pose", q: "how is it standing?", icon: "🕺", c: C.gen, demo: "pose" },
    { name: "OCR", q: "what does it say?", icon: "🔤", c: C.pix, demo: "ocr" },
    { name: "Generation", q: "make me an image", icon: "✨", c: C.gen, demo: "gen" },
  ];
  const hot = Math.floor(frame / 30) % tasks.length;
  return (
    <Stage>
      <Head kicker="THE TASK ZOO" title="One field, many questions" o={p(0, 0.06)} />
      {tasks.map((t, i) => {
        const col = i % 4, row = Math.floor(i / 4);
        const at = 0.06 + i * 0.075;
        const o = p(at, at + 0.08);
        const active = hot === i && p(0.62, 0.63) > 0.5;
        const x = 130 + col * 430, y = 250 + row * 320;
        return (
          <div key={i} style={{
            position: "absolute", left: x, top: y, width: 390, height: 285, borderRadius: 20,
            background: mix(C.panel, t.c, active ? 0.16 : 0.08), border: `2.5px solid ${active ? t.c : mix(C.line, t.c, 0.5)}`,
            padding: "22px 26px", boxSizing: "border-box", opacity: o,
            transform: `translateY(${(1 - o) * 24 + (active ? -8 : 0)}px)`,
            boxShadow: active ? `0 0 50px ${mix(C.bg0, t.c, 0.4)}` : "none",
          }}>
            <div style={{ display: "flex", alignItems: "center", gap: 14 }}>
              <span style={{ fontSize: 46 }}>{t.icon}</span>
              <span style={{ fontFamily: SANS, fontWeight: 800, fontSize: 32, color: t.c }}>{t.name}</span>
            </div>
            <div style={{ fontFamily: MONO, fontSize: 24, color: C.muted, marginTop: 10 }}>“{t.q}”</div>
            {/* mini live demo */}
            <div style={{ position: "relative", marginTop: 16, height: 110, borderRadius: 12, background: C.bg1, border: `1.5px solid ${C.line}`, overflow: "hidden" }}>
              <MiniDemo kind={t.demo} color={t.c} on={o > 0.9} />
            </div>
          </div>
        );
      })}
    </Stage>
  );
};

const MiniDemo: React.FC<{ kind: string; color: string; on: boolean }> = ({ kind, color, on }) => {
  const frame = useCurrentFrame();
  if (!on) return null;
  const t = (frame % 90) / 90;
  const cat = <span style={{ position: "absolute", left: 34, top: 22, fontSize: 56 }}>🐈</span>;
  switch (kind) {
    case "label":
      return (<>{cat}<span style={{ position: "absolute", right: 16, top: 36, fontFamily: MONO, fontWeight: 800, fontSize: 26, color, opacity: t > 0.3 ? 1 : t / 0.3 }}>“cat” 0.94</span></>);
    case "box":
      return (<>{cat}<div style={{ position: "absolute", left: 26, top: 14, width: 84 * Math.min(1, t * 2), height: 76 * Math.min(1, t * 2), border: `3px solid ${color}`, borderRadius: 8 }} /><span style={{ position: "absolute", left: 120, top: 12, fontFamily: MONO, fontSize: 20, color }}>cat .91</span></>);
    case "mask":
      return (<>{cat}<div style={{ position: "absolute", left: 24, top: 12, width: 86, height: 82, borderRadius: 18, background: color, opacity: 0.35 * Math.min(1, t * 2) }} /></>);
    case "track": {
      const x = 20 + t * 220;
      return (<><span style={{ position: "absolute", left: x, top: 26, fontSize: 48 }}>🐈</span><div style={{ position: "absolute", left: x - 6, top: 20, width: 66, height: 62, border: `2.5px dashed ${color}`, borderRadius: 8 }} /></>);
    }
    case "pose": {
      const joints = [[60, 20], [60, 44], [40, 60], [80, 60], [48, 92], [74, 92]];
      return (<svg width={340} height={110}>{joints.map(([x, y], i) => <circle key={i} cx={x + 60} cy={y} r={6} fill={color} opacity={t * 3 - i * 0.3 > 0 ? 1 : 0} />)}
        <path d={`M120,20 L120,44 L100,60 M120,44 L140,60 M120,44 L108,92 M120,44 L134,92`} stroke={color} strokeWidth={3} fill="none" opacity={Math.min(1, t * 2)} /></svg>);
    }
    case "ocr":
      return (<><span style={{ position: "absolute", left: 20, top: 30, fontFamily: MONO, fontSize: 30, color: C.text }}>STOP</span><div style={{ position: "absolute", left: 16, top: 26, width: 104, height: 44, border: `2.5px solid ${color}`, borderRadius: 6, opacity: Math.min(1, t * 2) }} /><span style={{ position: "absolute", left: 140, top: 34, fontFamily: MONO, fontSize: 24, color }}>→ “STOP”</span></>);
    case "gen": {
      const g = [[0, 1], [1, 2], [2, 0], [1, 1]].map(([i, j], k) => <div key={k} style={{ position: "absolute", left: 30 + j * 30 + rnd(k, 1, Math.floor(frame / 6)) * 8, top: 20 + i * 26, width: 22, height: 22, borderRadius: 6, background: mix(C.bg1, color, 0.4 + rnd(k, 2, Math.floor(frame / 6)) * 0.6) }} />);
      return (<>{g}<span style={{ position: "absolute", left: 160, top: 36, fontFamily: MONO, fontSize: 22, color }}>“a cat” → 🐈</span></>);
    }
    default: return cat;
  }
};

// cv_apps -----------------------------------------------------------------------------
export const CvApps: React.FC<{ dur?: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const apps = [
    { e: "📱", t: "Face unlock" }, { e: "🏥", t: "Medical imaging" }, { e: "🚗", t: "Self-driving" },
    { e: "🏭", t: "Defect inspection" }, { e: "🌾", t: "Crop monitoring" }, { e: "🛒", t: "Retail checkout" },
    { e: "⚽", t: "Sports analytics" }, { e: "📄", t: "Document AI" },
  ];
  const hot = Math.floor(frame / 26) % apps.length;
  return (
    <Stage>
      <Head kicker="WHERE IT RUNS" title="Cameras that understand" color={C.green} o={p(0, 0.06)} />
      {/* center camera */}
      <div style={{ position: "absolute", left: 875, top: 470, width: 170, height: 170, borderRadius: 170, background: mix(C.panel, C.pix, 0.16), border: `4px solid ${C.pix}`, display: "flex", alignItems: "center", justifyContent: "center", fontSize: 84, opacity: p(0.04, 0.12), boxShadow: `0 0 80px ${mix(C.bg0, C.pix, 0.4)}` }}>📷</div>
      {apps.map((a, i) => {
        const ang = (i / apps.length) * Math.PI * 2 - Math.PI / 2 + Math.sin(frame * 0.008) * 0.06;
        const R = 360;
        const x = 960 + Math.cos(ang) * R * 1.55, y = 555 + Math.sin(ang) * R * 0.78;
        const at = 0.08 + i * 0.06;
        const active = hot === i && p(0.55, 0.56) > 0.5;
        return (
          <React.Fragment key={i}>
            <Wire x1={960} y1={555} x2={x} y2={y} p={p(at, at + 0.06)} color={active ? C.green : mix(C.muted, C.bg1, 0.4)} w={active ? 3 : 2} arrow={false} />
            <div style={{
              position: "absolute", left: x - 150, top: y - 44, width: 300, height: 88, borderRadius: 16,
              background: mix(C.panel, active ? C.green : C.pix, active ? 0.18 : 0.08),
              border: `2.5px solid ${active ? C.green : mix(C.line, C.pix, 0.5)}`,
              display: "flex", alignItems: "center", gap: 14, padding: "0 20px", boxSizing: "border-box",
              opacity: p(at, at + 0.08), transform: `scale(${active ? 1.08 : 1})`,
              boxShadow: active ? `0 0 40px ${mix(C.bg0, C.green, 0.45)}` : "none",
            }}>
              <span style={{ fontSize: 40 }}>{a.e}</span>
              <span style={{ fontFamily: SANS, fontWeight: 700, fontSize: 26, color: C.text }}>{a.t}</span>
            </div>
          </React.Fragment>
        );
      })}
      <Foot p={p(0.8, 0.9)}>Dozens of detections per second in a car; microscopic defects on a production line; one camera, any industry.</Foot>
    </Stage>
  );
};

// cv_filters — point ops & blur, values changing live ---------------------------------
export const CvFilters: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur);
  const stages: { at: number; g: typeof CAT12; label: string; sub: string; c: string }[] = [
    { at: 0.06, g: CAT12, label: "original", sub: "v", c: C.muted },
    { at: 0.2, g: CAT_BRIGHT, label: "brighter", sub: "v + 60", c: C.classic },
    { at: 0.42, g: CAT_CONTRAST, label: "more contrast", sub: "(v−128)×1.8+128", c: C.classic },
    { at: 0.62, g: CAT_BLUR, label: "blurred", sub: "avg of 3×3 neighbors", c: C.pix },
  ];
  return (
    <Stage>
      <Head kicker="CLASSICAL PROCESSING · STEP 1" title="Filters: change the numbers, change the image" color={C.classic} o={p(0, 0.06)} />
      {stages.map((s, i) => {
        const o = p(s.at, s.at + 0.09);
        const mrph = p(s.at, s.at + 0.16);
        // morph values from original to target for a live "processing" feel
        const g = CAT12.map((row, r) => row.map((v, c) => Math.round(v + (s.g[r][c] - v) * mrph)));
        return (
          <div key={i} style={{ opacity: o }}>
            <PixGrid g={g} x={140 + i * 430} y={300} cell={30} values={false} o={o} label={s.label} labelColor={s.c} />
            <div style={{ position: "absolute", left: 140 + i * 430, top: 740, fontFamily: MONO, fontSize: 23, color: s.c, opacity: o }}>{s.sub}</div>
            {i > 0 && <Wire x1={140 + (i - 1) * 430 + 380} y1={490} x2={140 + i * 430 - 16} y2={490} p={p(s.at - 0.04, s.at)} color={s.c} w={3} />}
          </div>
        );
      })}
      <div style={{ position: "absolute", left: 140, top: 806, right: 140, display: "flex", gap: 30, opacity: p(0.78, 0.88) }}>
        <div style={{ flex: 1, fontFamily: SANS, fontSize: 28, color: C.text, background: mix(C.panel, C.classic, 0.08), border: `2px solid ${C.classic}`, borderRadius: 14, padding: "16px 24px" }}>
          <b style={{ color: C.classic }}>point ops</b> — each pixel changed alone (brightness, contrast)
        </div>
        <div style={{ flex: 1, fontFamily: SANS, fontSize: 28, color: C.text, background: mix(C.panel, C.pix, 0.08), border: `2px solid ${C.pix}`, borderRadius: 14, padding: "16px 24px" }}>
          <b style={{ color: C.pix }}>neighborhood ops</b> — each pixel looks around → leads to convolution
        </div>
      </div>
    </Stage>
  );
};

// cv_conv — THE convolution walkthrough ------------------------------------------------
export const CvConv: React.FC<{ dur?: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const IN = SEVEN8, N = IN.length; // 8
  const OUTN = N - 2; // 6
  const kernels: { k: number[][]; out: typeof IN; name: string; c: string }[] = [
    { k: K_EDGE, out: SEVEN_EDGE, name: "edge detect", c: C.classic },
    { k: K_BLUR.map((r) => r.map(() => 0.11)), out: SEVEN_BLUR, name: "blur", c: C.pix },
    { k: K_SHARP, out: SEVEN_SHARP, name: "sharpen", c: C.gen },
  ];
  // main slide phase covers 0.08..0.62 for kernel 0; then quick swaps
  const slide = p(0.1, 0.58);
  const pos = Math.min(OUTN * OUTN - 1, Math.floor(slide * OUTN * OUTN));
  const kr = Math.floor(pos / OUTN), kc = pos % OUTN;
  const kSel = p(0.66, 0.67) < 0.5 ? 0 : p(0.8, 0.81) < 0.5 ? 1 : 2;
  const K = kernels[kSel];
  const cell = 52, gx = 150, gy = 280;
  const ox = 1310, oy = 300;
  const raw = conv3(IN, K.k);
  const outNorm = absNorm(raw);
  const shown = kSel === 0 ? pos : OUTN * OUTN - 1;
  return (
    <Stage>
      <Head kicker="THE ONE OPERATION TO UNDERSTAND" title="Convolution: slide · multiply · sum" color={C.classic} o={p(0, 0.06)} />
      {/* input */}
      <PixGrid g={IN} x={gx} y={gy} cell={cell} values reveal={p(0.04, 0.12)} label="input image (8×8)" hi={p(0.1, 0.11) > 0.5 ? { r: kr, c: kc, size: 3, color: K.c } : null} />
      {/* kernel */}
      <div style={{ position: "absolute", left: 700, top: 330, opacity: p(0.06, 0.14) }}>
        <div style={{ fontFamily: MONO, fontSize: 24, color: K.c, marginBottom: 10 }}>kernel · {K.name}</div>
        <div style={{ display: "grid", gridTemplateColumns: `repeat(3, 88px)`, gap: 4 }}>
          {K.k.flat().map((v, i) => (
            <div key={i} style={{ width: 88, height: 66, borderRadius: 10, background: mix(C.panel, K.c, Math.abs(v) > 2 ? 0.3 : 0.12), border: `2px solid ${K.c}`, display: "flex", alignItems: "center", justifyContent: "center", fontFamily: MONO, fontWeight: 800, fontSize: 27, color: C.text }}>
              {Number.isInteger(v) ? v : v.toFixed(2)}
            </div>
          ))}
        </div>
        <div style={{ fontFamily: MONO, fontSize: 23, color: C.muted, marginTop: 20, opacity: p(0.16, 0.24) }}>
          Σ (pixel × weight)
        </div>
        <div style={{ fontFamily: MONO, fontWeight: 800, fontSize: 40, color: K.c, marginTop: 8, opacity: p(0.16, 0.24) }}>
          = {raw[kr][kc] > 0 ? "+" : ""}{Math.round(raw[kr][kc])}
        </div>
      </div>
      <Flow x1={640} y1={480} x2={700} y2={480} color={K.c} n={3} o={p(0.14, 0.2)} />
      <Flow x1={1080} y1={480} x2={1290} y2={480} color={K.c} n={4} o={p(0.14, 0.2)} />
      {/* output */}
      <PixGrid g={outNorm} x={ox} y={oy} cell={62} reveal={(shown + 1) / (OUTN * OUTN)} label={`output · feature map (6×6)`} tint={K.c} />
      {/* kernel selector chips */}
      <div style={{ position: "absolute", left: 700, top: 760, display: "flex", gap: 16, opacity: p(0.62, 0.7) }}>
        {kernels.map((kk, i) => (
          <div key={i} style={{ fontFamily: MONO, fontWeight: 700, fontSize: 24, color: kSel === i ? C.bg0 : kk.c, background: kSel === i ? kk.c : mix(C.panel, kk.c, 0.12), border: `2px solid ${kk.c}`, borderRadius: 999, padding: "10px 24px" }}>{kk.name}</div>
        ))}
      </div>
      <div style={{ position: "absolute", left: 700, top: 840, fontFamily: SANS, fontSize: 29, color: C.text, width: 1000, opacity: p(0.7, 0.8), lineHeight: 1.35 }}>
        same slide-multiply-sum — <b style={{ color: C.classic }}>different weights, completely different result.</b> A kernel is a pattern detector.
      </div>
      <Foot p={p(0.86, 0.94)}>Output is high where the image matches the kernel's pattern. Hold onto that — it's the seed of everything deep.</Foot>
    </Stage>
  );
};

// cv_edges ------------------------------------------------------------------------------
export const CvEdges: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur);
  const panels = [
    { at: 0.05, g: CAT12, label: "input", c: C.muted, k: null as null | number[][] },
    { at: 0.22, g: CAT_GX, label: "vertical edges · Sobel-X", c: C.classic, k: SOBEL_X },
    { at: 0.45, g: CAT_GY, label: "horizontal edges · Sobel-Y", c: C.classic, k: SOBEL_Y },
    { at: 0.66, g: CAT_EDGES, label: "|Gx| + |Gy| → edge map", c: C.pix, k: null },
  ];
  return (
    <Stage>
      <Head kicker="CLASSICAL PROCESSING · STEP 2" title="Edge detection: find where the numbers jump" color={C.classic} o={p(0, 0.06)} />
      {panels.map((pn, i) => {
        const o = p(pn.at, pn.at + 0.1);
        return (
          <div key={i} style={{ opacity: o }}>
            <PixGrid g={pn.g} x={130 + i * 440} y={300} cell={i === 0 ? 30 : 32} tint={i === 0 ? undefined : pn.c} o={o} label={pn.label} labelColor={pn.c} reveal={p(pn.at, pn.at + 0.18)} />
            {pn.k && (
              <div style={{ position: "absolute", left: 130 + i * 440, top: 740, display: "grid", gridTemplateColumns: "repeat(3, 52px)", gap: 3, opacity: o }}>
                {pn.k.flat().map((v, j) => (
                  <div key={j} style={{ width: 52, height: 40, borderRadius: 7, background: v > 0 ? mix(C.panel, C.green, 0.3) : v < 0 ? mix(C.panel, C.red, 0.3) : C.panel, border: `1.5px solid ${C.line}`, display: "flex", alignItems: "center", justifyContent: "center", fontFamily: MONO, fontSize: 21, color: C.text }}>{v}</div>
                ))}
              </div>
            )}
            {i > 0 && <Wire x1={130 + (i - 1) * 440 + 390} y1={500} x2={130 + i * 440 - 14} y2={500} p={p(pn.at - 0.04, pn.at)} color={pn.c} w={3} />}
          </div>
        );
      })}
      <ScanBeam x={1450} y={330} w={390} h={400} color={C.pix} o={p(0.72, 0.8)} />
      <Foot p={p(0.84, 0.93)}>Flat regions → zero. Boundaries → strong response. Edges are where the information lives: shape, without lighting.</Foot>
    </Stage>
  );
};

// cv_classic — handcrafted era & its ceiling ----------------------------------------------
export const CvClassic: React.FC<{ dur?: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  // HOG-ish oriented gradients on cat
  const cells: { x: number; y: number; a: number; m: number }[] = [];
  for (let r = 1; r < 11; r += 2) for (let c = 1; c < 11; c += 2) {
    const gx = CAT12[r][Math.min(11, c + 1)] - CAT12[r][Math.max(0, c - 1)];
    const gy = CAT12[Math.min(11, r + 1)][c] - CAT12[Math.max(0, r - 1)][c];
    const m = Math.hypot(gx, gy);
    if (m > 25) cells.push({ x: c, y: r, a: Math.atan2(gy, gx), m });
  }
  const years = [
    { y: "1999", t: "SIFT keypoints" }, { y: "2001", t: "Viola-Jones faces" },
    { y: "2005", t: "HOG pedestrians" }, { y: "2006", t: "SURF" },
  ];
  return (
    <Stage>
      <Head kicker="THE HANDCRAFTED ERA" title="Fifty years of features designed by hand" color={C.classic} o={p(0, 0.06)} />
      {/* HOG arrows over cat */}
      <PixGrid g={CAT12} x={150} y={280} cell={38} o={p(0.05, 0.13)} label="gradient orientations (HOG idea)" labelColor={C.classic} />
      <svg style={{ position: "absolute", left: 150, top: 316, overflow: "visible" }} width={480} height={480}>
        {cells.map((cl, i) => {
          const o = p(0.12 + (i / cells.length) * 0.16, 0.18 + (i / cells.length) * 0.16);
          const cx = cl.x * 40 + 20, cy = cl.y * 40 + 20;
          const L = 16 + (cl.m / 255) * 12;
          const wob = Math.sin(frame * 0.06 + i) * 0.06;
          return (
            <line key={i} x1={cx - Math.cos(cl.a + wob) * L} y1={cy - Math.sin(cl.a + wob) * L}
              x2={cx + Math.cos(cl.a + wob) * L} y2={cy + Math.sin(cl.a + wob) * L}
              stroke={C.classic} strokeWidth={4} opacity={o * 0.95} strokeLinecap="round" />
          );
        })}
      </svg>
      {/* timeline */}
      <div style={{ position: "absolute", left: 760, top: 290, width: 460 }}>
        {years.map((yr, i) => (
          <div key={i} style={{ display: "flex", gap: 18, alignItems: "center", marginBottom: 22, opacity: p(0.2 + i * 0.06, 0.28 + i * 0.06) }}>
            <span style={{ fontFamily: MONO, fontWeight: 800, fontSize: 27, color: C.classic, width: 90 }}>{yr.y}</span>
            <span style={{ fontFamily: SANS, fontSize: 29, color: C.text }}>{yr.t}</span>
          </div>
        ))}
        <div style={{ fontFamily: MONO, fontSize: 23, color: C.muted, marginTop: 8, opacity: p(0.44, 0.52) }}>
          recipe: handcrafted features + simple classifier
        </div>
      </div>
      {/* the ceiling */}
      <div style={{ position: "absolute", left: 1290, top: 300, width: 500, opacity: p(0.52, 0.6) }}>
        <div style={{ fontFamily: MONO, fontSize: 23, color: C.muted, marginBottom: 12 }}>accuracy over the 2000s</div>
        <svg width={480} height={330}>
          <line x1={30} y1={300} x2={460} y2={300} stroke={C.line} strokeWidth={2} />
          <polyline
            points={Array.from({ length: 40 }).map((_, i) => {
              const t = i / 39;
              const v = 60 + 90 * (1 - Math.exp(-t * 3)) + Math.sin(t * 20) * 4;
              return `${30 + t * 420 * p(0.55, 0.85)},${300 - v * p(0.55, 0.85)}`;
            }).join(" ")}
            fill="none" stroke={C.classic} strokeWidth={5} />
          <line x1={30} y1={140} x2={460} y2={140} stroke={C.red} strokeWidth={3} strokeDasharray="10 8" opacity={p(0.72, 0.8)} />
          <text x={40} y={126} fontFamily={MONO} fontSize={22} fill={C.red} opacity={p(0.72, 0.8)}>the ceiling — real world is too messy</text>
        </svg>
      </div>
      <Foot p={p(0.84, 0.93)}>Lighting, angle, occlusion, deformation — every hand-written rule broke somewhere. Lesson: stop designing features. Learn them.</Foot>
    </Stage>
  );
};

// cv_whycnn ---------------------------------------------------------------------------------
export const CvWhyCnn: React.FC<{ dur?: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const shift = p(0.62, 0.72);
  return (
    <Stage>
      <Head kicker="WHY CONVOLUTION + LEARNING" title="Why not a plain neural net on pixels?" color={C.neural} o={p(0, 0.06)} />
      {/* left: MLP mess */}
      <Card x={130} y={250} w={790} h={430} color={C.red} o={p(0.05, 0.13)}>
        <div style={{ fontFamily: SANS, fontWeight: 700, fontSize: 30, color: C.red }}>fully-connected on pixels</div>
        <svg width={720} height={260} style={{ marginTop: 14 }}>
          {Array.from({ length: 14 }).map((_, i) => (
            Array.from({ length: 8 }).map((_, j) => (
              <line key={`${i}-${j}`} x1={40} y1={20 + i * 17} x2={640} y2={40 + j * 26}
                stroke={mix(C.red, C.bg1, 0.55)} strokeWidth={1}
                opacity={p(0.08 + ((i * 8 + j) / 112) * 0.14, 0.14 + ((i * 8 + j) / 112) * 0.14) * (0.35 + rnd(i, j) * 0.4)} />
            ))
          ))}
          {Array.from({ length: 14 }).map((_, i) => <circle key={i} cx={40} cy={20 + i * 17} r={5} fill={C.pix} opacity={p(0.07, 0.14)} />)}
          {Array.from({ length: 8 }).map((_, j) => <circle key={j} cx={640} cy={40 + j * 26} r={7} fill={C.red} opacity={p(0.07, 0.14)} />)}
        </svg>
        <div style={{ display: "flex", gap: 26, alignItems: "baseline", opacity: p(0.2, 0.3) }}>
          <span style={{ fontFamily: MONO, fontSize: 23, color: C.muted }}>1M pixels × 1000 neurons =</span>
          <Counter p={p(0.2, 0.36)} to={1} prefix="" suffix=" BILLION weights" color={C.red} size={34} />
        </div>
      </Card>
      {/* right: conv reuse */}
      <Card x={990} y={250} w={800} h={430} color={C.green} o={p(0.36, 0.44)}>
        <div style={{ fontFamily: SANS, fontWeight: 700, fontSize: 30, color: C.green }}>convolution: 9 weights, reused everywhere</div>
        <div style={{ position: "relative", marginTop: 18, height: 250 }}>
          <PixGrid g={CAT12} x={30} y={0} cell={20} o={p(0.38, 0.46)} />
          {(() => {
            const t = (frame * 0.9) % 100 / 100;
            const posi = Math.floor(t * 100);
            const rr = Math.floor(posi / 10), cc = posi % 10;
            return <div style={{ position: "absolute", left: 30 + cc * 22 - 2, top: rr * 22 - 2, width: 3 * 22 + 2, height: 3 * 22 + 2, border: `3px solid ${C.green}`, borderRadius: 6, boxShadow: `0 0 16px ${C.green}`, opacity: p(0.4, 0.48) }} />;
          })()}
          <div style={{ position: "absolute", left: 360, top: 40, fontFamily: MONO, fontSize: 24, color: C.text, opacity: p(0.44, 0.52), lineHeight: 1.6 }}>
            same <b style={{ color: C.green }}>9 numbers</b> stamped<br />across the whole image<br />
            <span style={{ color: C.muted }}>→ few weights</span><br />
            <span style={{ color: C.muted }}>→ works at any position</span>
          </div>
        </div>
      </Card>
      {/* shift demo */}
      <div style={{ position: "absolute", left: 130, top: 740, right: 130, display: "flex", gap: 40, alignItems: "center", opacity: p(0.6, 0.68) }}>
        <div style={{ position: "relative", width: 320, height: 130, borderRadius: 16, background: C.bg1, border: `2px solid ${C.line}`, overflow: "hidden" }}>
          <span style={{ position: "absolute", left: 30 + shift * 120, top: 28, fontSize: 62 }}>🐈</span>
        </div>
        <div style={{ fontFamily: SANS, fontSize: 30, color: C.text, lineHeight: 1.45 }}>
          shift the cat one step → <b style={{ color: C.red }}>MLP: brand-new input</b> · <b style={{ color: C.green }}>CNN: same kernels still fire</b>
        </div>
      </div>
      <Foot p={p(0.84, 0.93)}>So: make the network's layers convolutions — and let backpropagation learn the kernel weights.</Foot>
    </Stage>
  );
};

// cv_cnn — the architecture ---------------------------------------------------------------
export const CvCnn: React.FC<{ dur?: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const blocks = [
    { at: 0.06, w: 150, maps: 1, cellN: 10, label: "input", c: C.pix },
    { at: 0.16, w: 170, maps: 3, cellN: 10, label: "conv+ReLU", c: C.neural },
    { at: 0.28, w: 150, maps: 3, cellN: 7, label: "pool", c: C.pix },
    { at: 0.38, w: 170, maps: 5, cellN: 7, label: "conv+ReLU", c: C.neural },
    { at: 0.48, w: 150, maps: 5, cellN: 4, label: "pool", c: C.pix },
    { at: 0.56, w: 170, maps: 8, cellN: 3, label: "conv+ReLU", c: C.neural },
  ];
  let bx = 120;
  const xs: number[] = blocks.map((b) => { const v = bx; bx += b.w + 60; return v; });
  const probs = [["cat", 0.91, C.green], ["dog", 0.06, C.muted], ["fox", 0.02, C.muted], ["car", 0.01, C.muted]] as const;
  return (
    <Stage>
      <Head kicker="THE ARCHITECTURE" title="CNN: stack conv → ReLU → pool, repeat" color={C.neural} o={p(0, 0.06)} />
      {blocks.map((b, i) => {
        const o = p(b.at, b.at + 0.09);
        return (
          <React.Fragment key={i}>
            {i > 0 && <Flow x1={xs[i - 1] + b.w - 10} y1={490} x2={xs[i]} y2={490} color={blocks[i].c} n={4} o={o} speed={0.014} />}
            <div style={{ position: "absolute", left: xs[i], top: 350, opacity: o, transform: `translateY(${(1 - o) * 20}px)` }}>
              {Array.from({ length: b.maps }).map((_, m) => {
                const sz = b.cellN * (b.cellN > 6 ? 13 : 22);
                return (
                  <div key={m} style={{
                    position: "absolute", left: m * 12, top: 60 - m * 12, width: sz, height: sz,
                    borderRadius: 10, background: mix(C.panel, b.c, 0.16 + (m / b.maps) * 0.2),
                    border: `2px solid ${mix(C.line, b.c, 0.7)}`,
                    backgroundImage: `linear-gradient(${C.line} 1px, transparent 1px), linear-gradient(90deg, ${C.line} 1px, transparent 1px)`,
                    backgroundSize: `${sz / b.cellN}px ${sz / b.cellN}px`,
                    boxShadow: m === b.maps - 1 ? `0 0 22px ${mix(C.bg0, b.c, 0.25 + Math.sin(frame * 0.06 + i) * 0.1)}` : "none",
                  }} />
                );
              })}
              <div style={{ position: "absolute", left: 0, top: 260, fontFamily: MONO, fontSize: 21, color: b.c, whiteSpace: "nowrap" }}>{b.label}</div>
              <div style={{ position: "absolute", left: 0, top: 292, fontFamily: MONO, fontSize: 19, color: C.muted, whiteSpace: "nowrap" }}>{b.cellN}×{b.cellN} · {b.maps} ch</div>
            </div>
          </React.Fragment>
        );
      })}
      {/* flatten → vector → softmax */}
      <Flow x1={1290} y1={490} x2={1400} y2={490} color={C.classic} n={4} o={p(0.62, 0.7)} />
      <div style={{ position: "absolute", left: 1400, top: 380, opacity: p(0.64, 0.72) }}>
        <div style={{ fontFamily: MONO, fontSize: 21, color: C.classic, marginBottom: 8 }}>flatten → vector</div>
        {Array.from({ length: 12 }).map((_, i) => (
          <div key={i} style={{ display: "inline-block", width: 26, height: 46, marginRight: 4, borderRadius: 6, background: mix(C.panel, C.classic, 0.2 + rnd(i, 3) * 0.5), border: `1.5px solid ${C.line}` }} />
        ))}
      </div>
      <div style={{ position: "absolute", left: 1400, top: 540, width: 400, opacity: p(0.72, 0.8) }}>
        <div style={{ fontFamily: MONO, fontSize: 21, color: C.green, marginBottom: 10 }}>classifier head → softmax</div>
        {probs.map(([nm, v, col], i) => (
          <div key={nm} style={{ display: "flex", alignItems: "center", gap: 12, marginBottom: 8 }}>
            <span style={{ fontFamily: MONO, fontSize: 22, color: C.text, width: 60 }}>{nm}</span>
            <div style={{ flex: 1, height: 26, background: C.panel, borderRadius: 7, overflow: "hidden", border: `1px solid ${C.line}` }}>
              <div style={{ width: `${v * 100 * p(0.74 + i * 0.02, 0.9)}%`, height: "100%", background: col }} />
            </div>
            <span style={{ fontFamily: MONO, fontSize: 21, color: col, width: 66 }}>{Math.round(v * 100 * p(0.74 + i * 0.02, 0.9))}%</span>
          </div>
        ))}
      </div>
      <div style={{ position: "absolute", left: 120, top: 760, right: 120, textAlign: "center", opacity: p(0.8, 0.88) }}>
        <span style={{ fontFamily: SANS, fontSize: 30, color: C.text, background: C.panel, border: `2px solid ${C.line}`, borderRadius: 14, padding: "14px 30px" }}>
          resolution <b style={{ color: C.pix }}>shrinks</b> → channels <b style={{ color: C.neural }}>grow</b> → pixels become <b style={{ color: C.classic }}>concepts</b>
        </span>
      </div>
      <Foot p={p(0.87, 0.95)}>Millions of kernel weights — every one learned from data, none designed by hand.</Foot>
    </Stage>
  );
};

// cv_pool -----------------------------------------------------------------------------------
export const CvPool: React.FC<{ dur?: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const IN = [
    [12, 200, 30, 45, 80, 21],
    [8, 190, 60, 210, 15, 22],
    [90, 35, 240, 70, 55, 130],
    [20, 28, 66, 90, 200, 40],
    [140, 30, 22, 80, 60, 70],
    [25, 210, 45, 35, 20, 190],
  ];
  const OUT = maxPool2(IN);
  const slide = p(0.14, 0.5);
  const pos = Math.min(8, Math.floor(slide * 9));
  const wr = Math.floor(pos / 3), wc = pos % 3;
  const rf = p(0.62, 0.8);
  return (
    <Stage>
      <Head kicker="THE SHRINK STEP" title="Max pooling: keep the strongest signal" color={C.pix} o={p(0, 0.06)} />
      <PixGrid g={IN} x={170} y={290} cell={72} values label="feature map (6×6)" hi={p(0.12, 0.13) > 0.5 ? { r: wr * 2, c: wc * 2, size: 2, color: C.green } : null} reveal={p(0.04, 0.12)} tint={C.neural} />
      <div style={{ position: "absolute", left: 700, top: 480, fontFamily: MONO, fontSize: 25, color: C.green, opacity: p(0.14, 0.2), textAlign: "center", width: 240 }}>
        take the <b>max</b> of each 2×2 window →
      </div>
      <PixGrid g={OUT} x={980} y={330} cell={92} values reveal={(pos + 1) / 9} label="pooled (3×3) — half the size" tint={C.green} />
      {/* receptive field */}
      <div style={{ position: "absolute", left: 1420, top: 300, width: 380, opacity: p(0.6, 0.68) }}>
        <div style={{ fontFamily: MONO, fontSize: 23, color: C.muted, marginBottom: 14 }}>stack a few blocks…</div>
        <div style={{ position: "relative", width: 340, height: 340 }}>
          {[1, 0.66, 0.38, 0.16].map((s, i) => (
            <div key={i} style={{
              position: "absolute", left: 170 - 170 * s * rf, top: 170 - 170 * s * rf,
              width: 340 * s * rf, height: 340 * s * rf, borderRadius: 14,
              border: `2.5px solid ${mix(C.pix, C.neural, i / 3)}`, opacity: 0.85,
              boxShadow: i === 0 ? `0 0 30px ${mix(C.bg0, C.pix, 0.3 + Math.sin(frame * 0.07) * 0.1)}` : "none",
            }} />
          ))}
          <div style={{ position: "absolute", left: 118, top: 152, fontFamily: MONO, fontSize: 21, color: C.text, opacity: rf }}>receptive field</div>
        </div>
        <div style={{ fontFamily: SANS, fontSize: 26, color: C.text, marginTop: 10, lineHeight: 1.4, opacity: p(0.7, 0.78) }}>
          each deeper layer sees a <b style={{ color: C.pix }}>wider window</b> of the original image
        </div>
      </div>
      <Foot p={p(0.84, 0.93)}>Bonus: small shifts stop mattering, and compute drops 4× per block. That's how tiny 3×3 kernels end up seeing whole objects.</Foot>
    </Stage>
  );
};

// cv_hier — learned feature hierarchy ----------------------------------------------------------
export const CvHier: React.FC<{ dur?: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const layers = [
    { at: 0.08, name: "layer 1", sub: "edges & colors", c: C.pix, kind: "edges" },
    { at: 0.28, name: "layer 2", sub: "textures & corners", c: C.classic, kind: "tex" },
    { at: 0.48, name: "layer 3", sub: "parts", c: C.neural, kind: "parts" },
    { at: 0.68, name: "layer 4+", sub: "objects", c: C.green, kind: "obj" },
  ];
  return (
    <Stage>
      <Head kicker="WHAT TRAINING DISCOVERS" title="A hierarchy nobody programmed" color={C.neural} o={p(0, 0.06)} />
      {layers.map((L, i) => {
        const o = p(L.at, L.at + 0.1);
        const x = 130 + i * 450;
        return (
          <React.Fragment key={i}>
            {i > 0 && <Wire x1={x - 76} y1={520} x2={x - 6} y2={520} p={p(L.at - 0.05, L.at)} color={L.c} w={4} />}
            <Card x={x} y={290} w={380} h={460} color={L.c} o={o} glow={o > 0.9}>
              <div style={{ fontFamily: MONO, fontWeight: 800, fontSize: 26, color: L.c }}>{L.name}</div>
              <div style={{ fontFamily: SANS, fontSize: 27, color: C.text, marginTop: 4 }}>{L.sub}</div>
              <div style={{ position: "relative", marginTop: 20, height: 290 }}>
                <HierGlyphs kind={L.kind} color={L.c} on={o > 0.85} />
              </div>
            </Card>
          </React.Fragment>
        );
      })}
      <Foot p={p(0.84, 0.93)}>Layer-1 kernels literally rediscover Sobel-style edges. The visual cortex shows the same rough progression — striking.</Foot>
    </Stage>
  );
};

const HierGlyphs: React.FC<{ kind: string; color: string; on: boolean }> = ({ kind, color, on }) => {
  const frame = useCurrentFrame();
  if (!on) return null;
  if (kind === "edges") {
    return (
      <svg width={320} height={280}>
        {Array.from({ length: 9 }).map((_, i) => {
          const a = (i / 9) * Math.PI + Math.sin(frame * 0.03) * 0.05;
          const cx = 55 + (i % 3) * 105, cy = 50 + Math.floor(i / 3) * 92;
          return (
            <g key={i}>
              <rect x={cx - 42} y={cy - 38} width={84} height={76} rx={10} fill="none" stroke={color} strokeWidth={1.5} opacity={0.4} />
              <line x1={cx - Math.cos(a) * 30} y1={cy - Math.sin(a) * 30} x2={cx + Math.cos(a) * 30} y2={cy + Math.sin(a) * 30} stroke={color} strokeWidth={6} strokeLinecap="round" />
            </g>
          );
        })}
      </svg>
    );
  }
  if (kind === "tex") {
    return (
      <svg width={320} height={280}>
        {Array.from({ length: 6 }).map((_, i) => {
          const cx = 55 + (i % 3) * 105, cy = 66 + Math.floor(i / 3) * 130;
          return (
            <g key={i}>
              <rect x={cx - 44} y={cy - 52} width={88} height={104} rx={10} fill="none" stroke={color} strokeWidth={1.5} opacity={0.4} />
              {Array.from({ length: 5 }).map((_, j) => (
                i % 2 === 0
                  ? <path key={j} d={`M ${cx - 34} ${cy - 40 + j * 18} q 17 ${10 + Math.sin(frame * 0.05 + j) * 4} 34 0 q 17 -10 34 0`} transform={`translate(-17 0)`} fill="none" stroke={color} strokeWidth={3.5} />
                  : <circle key={j} cx={cx - 22 + (j % 3) * 22} cy={cy - 26 + Math.floor(j / 3) * 26} r={7} fill={color} opacity={0.8} />
              ))}
            </g>
          );
        })}
      </svg>
    );
  }
  if (kind === "parts") {
    const parts = ["👁️", "👂", "🐾", "🛞", "🚪", "🪟"];
    return (
      <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: 14 }}>
        {parts.map((e, i) => (
          <div key={i} style={{ height: 120, borderRadius: 12, border: `1.5px solid ${color}55`, display: "flex", alignItems: "center", justifyContent: "center", fontSize: 52, transform: `translateY(${Math.sin(frame * 0.05 + i) * 4}px)` }}>{e}</div>
        ))}
      </div>
    );
  }
  const objs = ["🐱", "🚗"];
  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>
      {objs.map((e, i) => (
        <div key={i} style={{ height: 128, borderRadius: 14, border: `2px solid ${color}88`, display: "flex", alignItems: "center", justifyContent: "center", fontSize: 76, boxShadow: `0 0 ${26 + Math.sin(frame * 0.06 + i * 2) * 10}px ${color}44` }}>{e}</div>
      ))}
    </div>
  );
};

// cv_imagenet ------------------------------------------------------------------------------------
export const CvImagenet: React.FC<{ dur?: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const bars = [
    { y: "2010", v: 28.2, c: C.classic, tag: "classical" },
    { y: "2011", v: 25.8, c: C.classic, tag: "classical" },
    { y: "2012", v: 16.4, c: C.neural, tag: "AlexNet — deep CNN" },
    { y: "2013", v: 11.7, c: C.neural, tag: "all CNNs" },
    { y: "2014", v: 6.7, c: C.neural, tag: "GoogLeNet" },
    { y: "2015", v: 3.6, c: C.green, tag: "ResNet · 152 layers" },
  ];
  const X0 = 240, W = 200, H = 560, Y0 = 830;
  return (
    <Stage>
      <Head kicker="THE BREAKTHROUGH HAD A DATE" title="ImageNet: error rate, 1.2M images, 1000 classes" color={C.neural} o={p(0, 0.06)} />
      <svg style={{ position: "absolute", left: 0, top: 0 }} width={BW} height={BH}>
        <line x1={X0 - 60} y1={Y0} x2={X0 + 6 * W + 40} y2={Y0} stroke={C.line} strokeWidth={2} />
        {/* human line */}
        <line x1={X0 - 60} y1={Y0 - 5.1 * 19} x2={X0 + 6 * W + 40} y2={Y0 - 5.1 * 19} stroke={C.pix} strokeWidth={3} strokeDasharray="12 9" opacity={p(0.7, 0.78)} />
        <text x={X0 + 6 * W - 260} y={Y0 - 5.1 * 19 - 12} fontFamily={MONO} fontSize={23} fill={C.pix} opacity={p(0.7, 0.78)}>human · 5.1%</text>
      </svg>
      {bars.map((b, i) => {
        const at = 0.08 + i * 0.1;
        const grow = p(at, at + 0.1);
        const h = b.v * 19 * grow;
        const isAlex = i === 2;
        return (
          <div key={i}>
            <div style={{
              position: "absolute", left: X0 + i * W, top: Y0 - h, width: 130, height: h,
              borderRadius: "12px 12px 0 0", background: `linear-gradient(180deg, ${b.c}, ${mix(b.c, C.bg1, 0.45)})`,
              border: `2px solid ${b.c}`, borderBottom: "none",
              boxShadow: isAlex && grow > 0.9 ? `0 0 50px ${mix(C.bg0, C.neural, 0.5 + Math.sin(frame * 0.09) * 0.15)}` : "none",
            }} />
            <div style={{ position: "absolute", left: X0 + i * W - 20, top: Y0 - h - 46, width: 170, textAlign: "center", fontFamily: MONO, fontWeight: 800, fontSize: 30, color: b.c, opacity: grow }}>
              {b.v}%
            </div>
            <div style={{ position: "absolute", left: X0 + i * W - 20, top: Y0 + 14, width: 170, textAlign: "center", fontFamily: MONO, fontSize: 24, color: C.text, opacity: p(at, at + 0.08) }}>{b.y}</div>
            <div style={{ position: "absolute", left: X0 + i * W - 45, top: Y0 + 50, width: 220, textAlign: "center", fontFamily: MONO, fontSize: 19, color: C.muted, opacity: p(at + 0.03, at + 0.1) }}>{b.tag}</div>
            {isAlex && (
              <div style={{ position: "absolute", left: X0 + i * W - 60, top: Y0 - h - 130, width: 250, textAlign: "center", opacity: p(0.3, 0.38), transform: `translateY(${Math.sin(frame * 0.06) * 5}px)` }}>
                <span style={{ fontFamily: SANS, fontWeight: 800, fontSize: 30, color: C.neural, background: mix(C.panel, C.neural, 0.15), border: `2.5px solid ${C.neural}`, borderRadius: 12, padding: "8px 18px" }}>−10 pts overnight</span>
              </div>
            )}
          </div>
        );
      })}
      <Foot p={p(0.84, 0.93)}>2012: AlexNet, a deep CNN trained on two gaming GPUs. Three years later machines passed the human benchmark. The deep-learning era detonated here.</Foot>
    </Stage>
  );
};

// cv_train ------------------------------------------------------------------------------------------
export const CvTrain: React.FC<{ dur?: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const augs = [
    { t: "flip", g: CAT12.map((r) => [...r].reverse()) },
    { t: "crop", g: CAT12.map((r, i) => r.map((v, j) => (i > 1 && j > 1 ? CAT12[Math.min(11, i + 1)][Math.min(11, j + 1)] : v))) },
    { t: "jitter", g: gmap(CAT12, (v) => v * 0.8 + 30) },
  ];
  return (
    <Stage>
      <Head kicker="HOW IT LEARNS" title="Label → loss → blame → nudge · millions of times" color={C.neural} o={p(0, 0.06)} />
      {/* loop */}
      <PixGrid g={CAT12} x={150} y={300} cell={17} o={p(0.05, 0.12)} label="labeled: “cat”" labelColor={C.green} />
      <Wire x1={390} y1={400} x2={520} y2={400} p={p(0.1, 0.16)} color={C.neural} w={3.5} />
      <Card x={530} y={330} w={250} h={150} color={C.neural} o={p(0.12, 0.19)}>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 34, color: C.neural, textAlign: "center", marginTop: 12 }}>CNN</div>
        <div style={{ fontFamily: MONO, fontSize: 20, color: C.muted, textAlign: "center" }}>forward pass</div>
      </Card>
      <Wire x1={780} y1={400} x2={910} y2={400} p={p(0.18, 0.24)} color={C.neural} w={3.5} />
      <Card x={920} y={315} w={310} h={180} color={C.red} o={p(0.2, 0.27)}>
        <div style={{ fontFamily: MONO, fontSize: 22, color: C.muted }}>prediction</div>
        <div style={{ fontFamily: MONO, fontWeight: 800, fontSize: 32, color: C.red, marginTop: 6 }}>“dog” ✗</div>
        <div style={{ fontFamily: MONO, fontSize: 22, color: C.text, marginTop: 8 }}>truth: “cat” → loss = <b style={{ color: C.red }}>{(2.1 - 1.9 * p(0.26, 0.85)).toFixed(2)}</b></div>
      </Card>
      {/* backprop particles flowing backwards */}
      <Flow x1={920} y1={520} x2={560} y2={520} curve={-80} color={C.classic} n={8} o={p(0.3, 0.38)} speed={0.009} />
      <div style={{ position: "absolute", left: 600, top: 560, fontFamily: MONO, fontSize: 23, color: C.classic, opacity: p(0.32, 0.4) }}>
        backprop: every kernel weight gets its share of blame, then a nudge
      </div>
      {/* kernels shimmering */}
      <div style={{ position: "absolute", left: 540, top: 630, display: "flex", gap: 12, opacity: p(0.36, 0.44) }}>
        {Array.from({ length: 6 }).map((_, i) => (
          <div key={i} style={{ display: "grid", gridTemplateColumns: "repeat(3, 18px)", gap: 2 }}>
            {Array.from({ length: 9 }).map((_, j) => (
              <div key={j} style={{ width: 18, height: 18, borderRadius: 4, background: mix(C.panel, C.neural, 0.25 + rnd(i, j, Math.floor(frame / 8)) * 0.55) }} />
            ))}
          </div>
        ))}
      </div>
      {/* augmentation strip */}
      <div style={{ position: "absolute", left: 1330, top: 290, width: 470, opacity: p(0.5, 0.58) }}>
        <div style={{ fontFamily: MONO, fontSize: 23, color: C.muted, marginBottom: 12 }}>data hunger? augment:</div>
        <div style={{ display: "flex", gap: 20 }}>
          {augs.map((a, i) => (
            <div key={i} style={{ opacity: p(0.52 + i * 0.05, 0.6 + i * 0.05) }}>
              <PixGrid g={a.g} x={0} y={0} cell={10} o={1} />
              <div style={{ position: "relative", fontFamily: MONO, fontSize: 20, color: C.pix, textAlign: "center", marginTop: 128 }}>{a.t}</div>
            </div>
          ))}
        </div>
      </div>
      {/* transfer learning */}
      <Card x={1330} y={620} w={470} h={210} color={C.green} o={p(0.68, 0.76)} glow>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 30, color: C.green }}>the shortcut: transfer learning</div>
        <div style={{ fontFamily: SANS, fontSize: 26, color: C.text, marginTop: 10, lineHeight: 1.4 }}>
          start from ImageNet-pretrained weights, fine-tune on <b>thousands</b>, not millions.
        </div>
        <div style={{ fontFamily: MONO, fontSize: 21, color: C.muted, marginTop: 8 }}>same specialist story as LLM fine-tuning</div>
      </Card>
      <Foot p={p(0.84, 0.93)}>Loss measures wrongness; backprop assigns blame; millions of tiny nudges carve pattern detectors out of random noise.</Foot>
    </Stage>
  );
};
