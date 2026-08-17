/**
 * FTScenes.tsx — a bespoke "model tuning workshop" visual system for a
 * **Fine-Tuning LLMs, explained end-to-end** explainer.
 *
 * Narrative beats (ft_* variants): title, hook (generalist→specialist doctor),
 * scale (pretraining vs fine-tuning firehose), when (prompt→RAG→fine-tune ladder),
 * family (CPT / SFT / preference tree), full (full fine-tune weight wave + VRAM),
 * lora (frozen W + A·B bypass), qlora (4-bit squeeze onto one GPU), sft (chat
 * data typewriter), rlhf (preference loop + DPO shortcut), data (quality scale),
 * pitfalls (forgetting bars + overfit curves), workflow (5-step pipeline), recap.
 *
 * Identity: warm charcoal workshop + faint grid; frozen base=cyan, tuning=amber,
 * adapters=violet, ok=green, danger=red. Every scene is DURATION-AWARE: the
 * build script passes `dur` (seconds) in cut.ft, and phases are fractions of the
 * full narration, so scenes keep developing instead of freezing after entry.
 * Continuous motion (particle flows, sweeps, draws, counters) runs throughout.
 * Dispatched via cut.type === "ft_*" -> <FTScene variant .. {...cut.ft} />.
 */
import React from "react";
import {
  AbsoluteFill,
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";

const C = {
  bg0: "#070609",
  bg1: "#0D0B12",
  bg2: "#16121D",
  panel: "#1C1826",
  base: "#38BDF8", // frozen base model
  tune: "#FFB020", // fine-tuning / heat
  adapt: "#A78BFA", // LoRA adapters
  green: "#34D399",
  red: "#F87171",
  text: "#F4F1FA",
  muted: "#9A93AE",
  line: "rgba(255,255,255,0.07)",
};
const MONO = "ui-monospace, 'SF Mono', Menlo, monospace";
const SANS = "'Space Grotesk', Inter, system-ui, sans-serif";
const BW = 1920, BH = 1080;
const CL = { extrapolateLeft: "clamp" as const, extrapolateRight: "clamp" as const };

function mix(a: string, b: string, t: number) {
  const pa = a.replace("#", "").match(/\w\w/g)!.map((x) => parseInt(x, 16));
  const pb = b.replace("#", "").match(/\w\w/g)!.map((x) => parseInt(x, 16));
  const c = pa.map((v, i) => Math.round(v + (pb[i] - v) * t));
  return `rgb(${c[0]},${c[1]},${c[2]})`;
}

/** Duration-aware phase: p(a,b) maps fractions [a..b] of the WHOLE scene to 0..1. */
const useP = (dur?: unknown) => {
  const frame = useCurrentFrame();
  const F = Math.max(45, (typeof dur === "number" ? dur : 14) * 30);
  return (a: number, b: number) => interpolate(frame, [a * F, b * F], [0, 1], CL);
};

/** Spring pop that starts at fraction `at` of the scene. */
const usePop = (dur?: unknown) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const F = Math.max(45, (typeof dur === "number" ? dur : 14) * 30);
  return (at: number) =>
    spring({ frame: frame - Math.round(at * F), fps, config: { damping: 13, stiffness: 110 } });
};

// Quadratic bezier point
const qp = (t: number, x1: number, y1: number, cx: number, cy: number, x2: number, y2: number) => {
  const u = 1 - t;
  return { x: u * u * x1 + 2 * u * t * cx + t * t * x2, y: u * u * y1 + 2 * u * t * cy + t * t * y2 };
};

/** Continuous particle stream along a (possibly curved) path. Cheap divs, no filters. */
const Flow: React.FC<{
  x1: number; y1: number; x2: number; y2: number; curve?: number;
  color?: string; n?: number; speed?: number; size?: number; o?: number;
}> = ({ x1, y1, x2, y2, curve = 0, color = C.tune, n = 7, speed = 0.011, size = 11, o = 1 }) => {
  const frame = useCurrentFrame();
  const mx = (x1 + x2) / 2, my = (y1 + y2) / 2 - curve;
  return (
    <>
      {Array.from({ length: n }).map((_, i) => {
        const tt = (frame * speed + i / n) % 1;
        const pos = qp(tt, x1, y1, mx, my, x2, y2);
        const fade = Math.sin(tt * Math.PI);
        return (
          <div key={i} style={{
            position: "absolute", left: pos.x - size / 2, top: pos.y - size / 2,
            width: size, height: size, borderRadius: size,
            background: color, opacity: o * fade * 0.9,
            boxShadow: `0 0 ${size}px ${color}`,
          }} />
        );
      })}
    </>
  );
};

/** SVG connector that draws itself in as `p` goes 0→1, then marches its dashes forever. */
const Wire: React.FC<{
  x1: number; y1: number; x2: number; y2: number; p: number; curve?: number;
  color?: string; w?: number; arrow?: boolean;
}> = ({ x1, y1, x2, y2, p, curve = 0, color = C.muted, w = 3, arrow = true }) => {
  const frame = useCurrentFrame();
  const mx = (x1 + x2) / 2, my = (y1 + y2) / 2 - curve;
  const len = Math.hypot(x2 - x1, y2 - y1) + Math.abs(curve);
  const id = `ft${color.replace(/[^a-z0-9]/gi, "")}${Math.round(curve)}`;
  return (
    <svg style={{ position: "absolute", left: 0, top: 0, overflow: "visible" }} width={BW} height={BH}>
      <defs>
        <marker id={id} markerWidth="10" markerHeight="10" refX="7" refY="3" orient="auto">
          <path d="M0,0 L7,3 L0,6 Z" fill={color} />
        </marker>
      </defs>
      <path
        d={`M ${x1} ${y1} Q ${mx} ${my} ${x2} ${y2}`} fill="none"
        stroke={color} strokeWidth={w} opacity={p}
        strokeDasharray={`${len}`} strokeDashoffset={(1 - p) * len}
        markerEnd={arrow && p > 0.95 ? `url(#${id})` : undefined}
      />
      {p >= 1 - 1e-6 && (
        <path
          d={`M ${x1} ${y1} Q ${mx} ${my} ${x2} ${y2}`} fill="none"
          stroke={color} strokeWidth={w} opacity={0.5}
          strokeDasharray="6 18" strokeDashoffset={-frame * 1.6}
        />
      )}
    </svg>
  );
};

/** Animated numeric counter. */
const Counter: React.FC<{ p: number; to: number; prefix?: string; suffix?: string; color?: string; size?: number; decimals?: number }> = ({
  p, to, prefix = "", suffix = "", color = C.text, size = 44, decimals = 0,
}) => {
  const v = (to * interpolate(p, [0, 1], [0, 1], CL)).toFixed(decimals);
  return (
    <span style={{ fontFamily: MONO, fontWeight: 800, fontSize: size, color, fontVariantNumeric: "tabular-nums" }}>
      {prefix}{v}{suffix}
    </span>
  );
};

/** Rotating tuning knob — the identity motif. */
const Knob: React.FC<{ x: number; y: number; r: number; speed?: number; color?: string; o?: number }> = ({
  x, y, r, speed = 0.6, color = C.tune, o = 1,
}) => {
  const frame = useCurrentFrame();
  const ang = frame * speed;
  return (
    <div style={{
      position: "absolute", left: x - r, top: y - r, width: r * 2, height: r * 2, borderRadius: r * 2,
      border: `${Math.max(2, r * 0.09)}px solid ${mix(C.panel, color, 0.55)}`,
      background: `radial-gradient(circle at 38% 32%, ${mix(C.panel, color, 0.22)}, ${C.panel})`,
      opacity: o, transform: `rotate(${ang}deg)`,
      boxShadow: `0 0 ${r * 0.8}px ${mix(C.bg0, color, 0.35)}`,
    }}>
      <div style={{ position: "absolute", left: "50%", top: r * 0.12, width: Math.max(3, r * 0.1), height: r * 0.42, marginLeft: -Math.max(3, r * 0.1) / 2, borderRadius: 4, background: color }} />
    </div>
  );
};

const Bg: React.FC<{ accent?: string }> = ({ accent = C.tune }) => {
  const frame = useCurrentFrame();
  const pulse = (Math.sin(frame * 0.02) + 1) / 2;
  const sweep = ((frame * 2.2) % (BW + 900)) - 450;
  return (
    <AbsoluteFill style={{ background: `radial-gradient(ellipse at 50% 24%, ${C.bg2} 0%, ${C.bg1} 55%, ${C.bg0} 100%)` }}>
      <AbsoluteFill style={{
        backgroundImage: `linear-gradient(${C.line} 1px, transparent 1px), linear-gradient(90deg, ${C.line} 1px, transparent 1px)`,
        backgroundSize: "72px 72px", opacity: 0.5,
        maskImage: "radial-gradient(ellipse at center, black 40%, transparent 92%)",
      }} />
      <AbsoluteFill style={{ background: `radial-gradient(circle at 50% 16%, ${mix(C.bg1, accent, 0.4)} 0%, transparent 46%)`, opacity: 0.3 + pulse * 0.2 }} />
      {/* slow diagonal light sweep — keeps every scene alive */}
      <div style={{
        position: "absolute", top: -200, left: sweep, width: 340, height: BH + 400,
        transform: "rotate(14deg)",
        background: `linear-gradient(90deg, transparent, ${mix(C.bg0, accent, 0.5)}22, transparent)`,
      }} />
    </AbsoluteFill>
  );
};

const Stage: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { width } = useVideoConfig();
  return (
    <AbsoluteFill style={{ alignItems: "center", justifyContent: "center" }}>
      <div style={{ width: BW, height: BH, transform: `scale(${width / BW})`, position: "relative" }}>{children}</div>
    </AbsoluteFill>
  );
};

const Kicker: React.FC<{ text: string; color?: string; cx?: boolean; o?: number }> = ({ text, color = C.tune, cx, o = 1 }) => (
  <div style={{ display: "flex", alignItems: "center", justifyContent: cx ? "center" : "flex-start", gap: 14, opacity: o }}>
    <div style={{ width: 40, height: 4, borderRadius: 2, background: color }} />
    <div style={{ fontFamily: MONO, letterSpacing: 6, fontSize: 22, color, textTransform: "uppercase", fontWeight: 700 }}>{text}</div>
  </div>
);

const Head: React.FC<{ kicker: string; title: string; color?: string; o?: number }> = ({ kicker, title, color = C.tune, o = 1 }) => (
  <div style={{ position: "absolute", left: 100, top: 56, right: 100 }}>
    <Kicker text={kicker} color={color} o={o} />
    <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 54, color: C.text, marginTop: 12, letterSpacing: -1.5, opacity: o }}>{title}</div>
  </div>
);

const Foot: React.FC<{ p: number; children: React.ReactNode }> = ({ p, children }) => (
  <div style={{
    position: "absolute", left: 100, top: 920, right: 100, fontFamily: MONO, fontSize: 23,
    color: C.muted, opacity: p, lineHeight: 1.4, transform: `translateY(${(1 - p) * 14}px)`,
  }}>{children}</div>
);

// ft_title --------------------------------------------------------------------
const TitleScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const p = useP(dur);
  const pop = spring({ frame, fps, config: { damping: 14, stiffness: 90 } });
  const bars = 24;
  return (
    <AbsoluteFill style={{ alignItems: "center", justifyContent: "center" }}>
      {/* equalizer floor — continuously dancing */}
      <div style={{ position: "absolute", bottom: 0, left: 0, right: 0, height: 300, display: "flex", alignItems: "flex-end", justifyContent: "center", gap: 18, opacity: 0.5 }}>
        {Array.from({ length: bars }).map((_, i) => {
          const h = 40 + (Math.sin(frame * 0.09 + i * 0.9) + 1) * 70 + (Math.sin(frame * 0.041 + i * 2.3) + 1) * 34;
          return <div key={i} style={{ width: 30, height: h, borderRadius: "8px 8px 0 0", background: `linear-gradient(180deg, ${mix(C.tune, C.adapt, i / bars)}, transparent)`, opacity: 0.7 }} />;
        })}
      </div>
      <Knob x={260} y={250} r={86} speed={0.5} color={C.adapt} o={0.85 * p(0.02, 0.12)} />
      <Knob x={1690} y={780} r={110} speed={-0.35} color={C.tune} o={0.85 * p(0.05, 0.15)} />
      <Knob x={1590} y={220} r={56} speed={0.8} color={C.base} o={0.8 * p(0.08, 0.18)} />
      <div style={{ textAlign: "center", transform: `scale(${0.9 + pop * 0.1})`, zIndex: 2 }}>
        <div style={{ display: "flex", justifyContent: "center", marginBottom: 28 }}>
          <Kicker text="LLM TRAINING · SPECIALIZATION" cx />
        </div>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 128, lineHeight: 1.02, letterSpacing: -3, color: C.text }}>
          <div>Fine-Tuning</div>
          <div style={{ color: C.tune, textShadow: `0 0 70px ${mix(C.bg0, C.tune, 0.7)}` }}>LLMs</div>
        </div>
        <div style={{ height: 5, width: interpolate(p(0.15, 0.45), [0, 1], [0, 520]), background: `linear-gradient(90deg, ${C.base}, ${C.tune}, ${C.adapt})`, borderRadius: 3, margin: "34px auto" }} />
        <div style={{ fontFamily: SANS, fontSize: 38, color: C.muted, opacity: p(0.25, 0.5), maxWidth: 1200 }}>
          Full fine-tuning · LoRA · QLoRA · SFT · RLHF &amp; DPO — end to end
        </div>
      </div>
    </AbsoluteFill>
  );
};

// ft_hook — generalist → specialist ------------------------------------------
const HookScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const orbit = [
    { e: "📚", ph: 0 }, { e: "⚖️", ph: 1 }, { e: "🧬", ph: 2 },
    { e: "💻", ph: 3 }, { e: "🎨", ph: 4 }, { e: "🌍", ph: 5 },
  ];
  const converge = p(0.45, 0.75); // orbit tightens as fine-tuning kicks in
  const cx0 = 560, cy0 = 560;
  return (
    <Stage>
      <Head kicker="THE ONE-LINE INTUITION" title="A generalist becomes a specialist" o={p(0, 0.08)} />
      {/* generalist model with orbiting knowledge */}
      <div style={{ position: "absolute", left: cx0 - 130, top: cy0 - 130, width: 260, height: 260, borderRadius: 260, background: mix(C.panel, C.base, 0.2), border: `4px solid ${C.base}`, display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", opacity: p(0.04, 0.14), boxShadow: `0 0 90px ${mix(C.bg0, C.base, 0.4)}` }}>
        <div style={{ fontSize: 84 }}>🧠</div>
        <div style={{ fontFamily: MONO, fontSize: 24, color: C.base, fontWeight: 700 }}>base model</div>
      </div>
      {orbit.map((o, i) => {
        const ang = frame * 0.024 + (i / orbit.length) * Math.PI * 2;
        const r = interpolate(converge, [0, 1], [300, 130]);
        const fade = interpolate(converge, [0.5, 1], [1, 0.12], CL);
        return (
          <div key={i} style={{
            position: "absolute",
            left: cx0 + Math.cos(ang) * r - 38, top: cy0 + Math.sin(ang) * r * 0.72 - 38,
            fontSize: 62, opacity: p(0.08 + i * 0.03, 0.18 + i * 0.03) * fade,
          }}>{o.e}</div>
        );
      })}
      {/* fine-tune beam */}
      <Wire x1={720} y1={560} x2={1170} y2={560} p={p(0.42, 0.58)} color={C.tune} w={5} />
      <div style={{ position: "absolute", left: 770, top: 470, fontFamily: MONO, fontSize: 25, color: C.tune, opacity: p(0.46, 0.58) }}>
        fine-tuning →
      </div>
      <Flow x1={720} y1={560} x2={1170} y2={560} color={C.tune} n={6} o={p(0.5, 0.6)} />
      {/* specialist */}
      <div style={{ position: "absolute", left: 1190, top: 400, width: 340, height: 320, borderRadius: 28, background: mix(C.panel, C.tune, 0.14), border: `4px solid ${C.tune}`, display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", gap: 8, opacity: p(0.55, 0.68), transform: `scale(${0.85 + p(0.55, 0.72) * 0.15})`, boxShadow: `0 0 90px ${mix(C.bg0, C.tune, 0.45 + Math.sin(frame * 0.06) * 0.1)}` }}>
        <div style={{ fontSize: 92 }}>🩺</div>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 40, color: C.tune }}>specialist</div>
        <div style={{ fontFamily: MONO, fontSize: 23, color: C.muted }}>your domain expert</div>
      </div>
      {/* med-school → residency strip */}
      <div style={{ position: "absolute", left: 240, top: 828, right: 240, opacity: p(0.2, 0.32) }}>
        <div style={{ display: "flex", justifyContent: "space-between", fontFamily: MONO, fontSize: 24, color: C.muted, marginBottom: 10 }}>
          <span>🎓 medical school = <b style={{ color: C.base }}>pretraining</b></span>
          <span>🏥 residency = <b style={{ color: C.tune }}>fine-tuning</b></span>
        </div>
        <div style={{ height: 16, borderRadius: 10, background: C.panel, border: `1.5px solid ${C.line}`, overflow: "hidden" }}>
          <div style={{ width: `${p(0.25, 0.9) * 100}%`, height: "100%", background: `linear-gradient(90deg, ${C.base}, ${C.tune})` }} />
        </div>
      </div>
    </Stage>
  );
};

// ft_scale — pretraining vs fine-tuning --------------------------------------
const Rain: React.FC<{ x: number; w: number; color: string; n: number; speed: number; o: number; size?: number }> = ({ x, w, color, n, speed, o, size = 10 }) => {
  const frame = useCurrentFrame();
  return (
    <>
      {Array.from({ length: n }).map((_, i) => {
        const seed = (i * 733) % 100 / 100;
        const tt = (frame * speed + seed) % 1;
        const y = 250 + tt * 420;
        const fade = Math.sin(tt * Math.PI);
        return (
          <div key={i} style={{
            position: "absolute", left: x + ((i * 379) % w), top: y,
            width: size, height: size, borderRadius: 3, background: color,
            opacity: o * fade * 0.85, boxShadow: `0 0 8px ${color}`,
          }} />
        );
      })}
    </>
  );
};

const ScaleScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur);
  const rows = (side: "l" | "r") => side === "l"
    ? [["tokens", "15 trillion+", C.base], ["compute", "1000s of GPUs", C.base], ["time", "months", C.base], ["cost", "$ millions", C.base]] as const
    : [["examples", "~10 thousand", C.tune], ["compute", "1 GPU", C.tune], ["time", "hours", C.tune], ["cost", "< $100", C.tune]] as const;
  return (
    <Stage>
      <Head kicker="TWO PHASES, WILDLY DIFFERENT SCALE" title="Pretraining builds the brain — fine-tuning teaches it a job" color={C.base} o={p(0, 0.08)} />
      {/* left: firehose */}
      <div style={{ position: "absolute", left: 130, top: 210, width: 760, opacity: p(0.05, 0.14) }}>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 42, color: C.base }}>PRETRAINING</div>
        <div style={{ fontFamily: MONO, fontSize: 24, color: C.muted }}>the whole internet, once</div>
      </div>
      <Rain x={180} w={620} color={C.base} n={54} speed={0.012} o={p(0.08, 0.16)} />
      <div style={{ position: "absolute", left: 220, top: 680, width: 560, height: 120, borderRadius: 20, background: mix(C.panel, C.base, 0.16), border: `3px solid ${C.base}`, display: "flex", alignItems: "center", justifyContent: "center", opacity: p(0.08, 0.16) }}>
        <span style={{ fontFamily: SANS, fontWeight: 800, fontSize: 38, color: C.text }}>🧠 base model</span>
      </div>
      {/* right: trickle */}
      <div style={{ position: "absolute", left: 1040, top: 210, width: 760, opacity: p(0.42, 0.52) }}>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 42, color: C.tune }}>FINE-TUNING</div>
        <div style={{ fontFamily: MONO, fontSize: 24, color: C.muted }}>a curated drip, targeted</div>
      </div>
      <Rain x={1300} w={200} color={C.tune} n={8} speed={0.007} o={p(0.46, 0.56)} size={13} />
      <div style={{ position: "absolute", left: 1130, top: 680, width: 560, height: 120, borderRadius: 20, background: mix(C.panel, C.tune, 0.16), border: `3px solid ${C.tune}`, display: "flex", alignItems: "center", justifyContent: "center", opacity: p(0.46, 0.56) }}>
        <span style={{ fontFamily: SANS, fontWeight: 800, fontSize: 38, color: C.text }}>🩺 specialist</span>
      </div>
      {/* stat counters */}
      {(["l", "r"] as const).map((side) =>
        rows(side).map(([label, value, color], i) => {
          const start = side === "l" ? 0.14 : 0.54;
          const px = side === "l" ? 560 : 1470;
          const o = p(start + i * 0.04, start + 0.1 + i * 0.04);
          return (
            <div key={side + i} style={{ position: "absolute", left: px, top: 300 + i * 92, width: 340, display: "flex", flexDirection: "column", opacity: o, transform: `translateX(${(1 - o) * (side === "l" ? -22 : 22)}px)` }}>
              <span style={{ fontFamily: MONO, fontSize: 21, color: C.muted }}>{label}</span>
              <span style={{ fontFamily: MONO, fontWeight: 800, fontSize: 38, color: color as string }}>{value}</span>
            </div>
          );
        })
      )}
      <div style={{ position: "absolute", left: 0, right: 0, top: 500, textAlign: "center", opacity: p(0.36, 0.46) }}>
        <div style={{ display: "inline-block", fontFamily: SANS, fontWeight: 800, fontSize: 44, color: C.muted, background: C.panel, borderRadius: 999, border: `2px solid ${C.line}`, padding: "12px 34px" }}>vs</div>
      </div>
      <Foot p={p(0.82, 0.92)}>Pretraining: trillions of tokens, months, millions of dollars. Fine-tuning: thousands of examples, hours, often under $100.</Foot>
    </Stage>
  );
};

// ft_when — decision ladder ---------------------------------------------------
const WhenScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const steps = [
    { at: 0.08, icon: "💬", name: "1 · PROMPT", when: "Try a better prompt + few-shot examples first", cost: "free · instant", c: C.green },
    { at: 0.32, icon: "📚", name: "2 · RAG", when: "Model needs your private / fresh knowledge", cost: "adds facts at runtime", c: C.base },
    { at: 0.56, icon: "🎛️", name: "3 · FINE-TUNE", when: "Change behavior: style, format, domain skill", cost: "bakes skills into weights", c: C.tune },
  ];
  return (
    <Stage>
      <Head kicker="DON'T FINE-TUNE FIRST" title="The decision ladder" color={C.green} o={p(0, 0.08)} />
      {steps.map((s, i) => {
        const on = p(s.at, s.at + 0.1);
        const active = p(s.at, s.at + 0.14) > 0.5 && (i === 2 || p(steps[Math.min(i + 1, 2)].at, steps[Math.min(i + 1, 2)].at + 0.01) < 1);
        const glow = active ? 0.35 + Math.sin(frame * 0.08) * 0.15 : 0.12;
        const x = 170 + i * 560, y = 620 - i * 170;
        return (
          <React.Fragment key={i}>
            {i > 0 && <Wire x1={x - 90} y1={y + 40} x2={x + 30} y2={y + 90} p={p(s.at - 0.06, s.at)} color={s.c} w={3.5} />}
            <div style={{ position: "absolute", left: x, top: y, width: 470, borderRadius: 22, background: mix(C.panel, s.c, 0.1), border: `3px solid ${s.c}`, padding: "26px 30px", boxSizing: "border-box", opacity: on, transform: `translateY(${(1 - on) * 26}px)`, boxShadow: `0 0 60px ${mix(C.bg0, s.c, glow)}` }}>
              <div style={{ display: "flex", alignItems: "center", gap: 16 }}>
                <span style={{ fontSize: 52 }}>{s.icon}</span>
                <span style={{ fontFamily: SANS, fontWeight: 800, fontSize: 38, color: s.c }}>{s.name}</span>
              </div>
              <div style={{ fontFamily: SANS, fontSize: 28, color: C.text, marginTop: 14, lineHeight: 1.3 }}>{s.when}</div>
              <div style={{ fontFamily: MONO, fontSize: 22, color: C.muted, marginTop: 10 }}>{s.cost}</div>
            </div>
          </React.Fragment>
        );
      })}
      {/* rule of thumb */}
      <div style={{ position: "absolute", left: 0, right: 0, top: 866, textAlign: "center", opacity: p(0.8, 0.9) }}>
        <div style={{ display: "inline-block", fontFamily: SANS, fontWeight: 700, fontSize: 34, color: C.text, background: C.panel, border: `2px solid ${C.line}`, borderRadius: 16, padding: "16px 36px" }}>
          <b style={{ color: C.base }}>RAG adds knowledge</b> · <b style={{ color: C.tune }}>fine-tuning adds skills</b>
        </div>
      </div>
    </Stage>
  );
};

// ft_family — three flavors ---------------------------------------------------
const FamilyScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const leaves = [
    { at: 0.12, x: 140, icon: "📄", name: "Continued pretraining", body: "Raw domain text — absorb the vocabulary", ex: "medical papers · legal contracts", c: C.base },
    { at: 0.36, x: 725, icon: "💬", name: "Supervised fine-tuning (SFT)", body: "Prompt → response pairs — follow instructions", ex: "Q&A · style · formats", c: C.tune },
    { at: 0.6, x: 1310, icon: "⚖️", name: "Preference tuning", body: "Learn which answer humans prefer", ex: "RLHF · DPO", c: C.adapt },
  ];
  return (
    <Stage>
      <Head kicker="THE FINE-TUNING FAMILY" title="Three flavors — most pipelines stack all three" color={C.adapt} o={p(0, 0.08)} />
      <div style={{ position: "absolute", left: 760, top: 218, width: 400, height: 110, borderRadius: 20, background: mix(C.panel, C.tune, 0.14), border: `3px solid ${C.tune}`, display: "flex", alignItems: "center", justifyContent: "center", opacity: p(0.03, 0.1), boxShadow: `0 0 50px ${mix(C.bg0, C.tune, 0.3)}` }}>
        <span style={{ fontFamily: SANS, fontWeight: 800, fontSize: 38, color: C.text }}>🎛️ FINE-TUNING</span>
      </div>
      {leaves.map((l, i) => (
        <React.Fragment key={i}>
          <Wire x1={960} y1={330} x2={l.x + 235} y2={430} p={p(l.at - 0.05, l.at + 0.02)} color={l.c} w={3.5} curve={-40} />
          <div style={{ position: "absolute", left: l.x, top: 440, width: 470, height: 330, borderRadius: 24, background: mix(C.panel, l.c, 0.1), border: `3px solid ${l.c}`, padding: "30px 32px", boxSizing: "border-box", opacity: p(l.at, l.at + 0.1), transform: `translateY(${(1 - p(l.at, l.at + 0.1)) * 24}px)` }}>
            <div style={{ fontSize: 62 }}>{l.icon}</div>
            <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 33, color: l.c, marginTop: 10 }}>{l.name}</div>
            <div style={{ fontFamily: SANS, fontSize: 27, color: C.text, marginTop: 14, lineHeight: 1.32 }}>{l.body}</div>
            <div style={{ fontFamily: MONO, fontSize: 22, color: C.muted, marginTop: 12 }}>{l.ex}</div>
          </div>
        </React.Fragment>
      ))}
      {/* stacked order chase */}
      <div style={{ position: "absolute", left: 0, right: 0, top: 850, display: "flex", justifyContent: "center", gap: 24, opacity: p(0.82, 0.92) }}>
        {["domain text", "SFT", "preferences"].map((s, i) => {
          const hot = Math.floor(frame / 24) % 3 === i;
          const cols = [C.base, C.tune, C.adapt];
          return (
            <React.Fragment key={i}>
              {i > 0 && <span style={{ fontFamily: MONO, fontSize: 30, color: C.muted, alignSelf: "center" }}>→</span>}
              <div style={{ fontFamily: MONO, fontWeight: 700, fontSize: 27, color: hot ? C.bg0 : cols[i], background: hot ? cols[i] : mix(C.panel, cols[i], 0.12), border: `2px solid ${cols[i]}`, borderRadius: 999, padding: "10px 28px" }}>{i + 1} · {s}</div>
            </React.Fragment>
          );
        })}
      </div>
    </Stage>
  );
};

// ft_full — full fine-tuning --------------------------------------------------
const FullScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const cols = 14, rowsN = 8;
  const wave = (frame * 1.6) % (cols + 6) - 3;
  const segs = [
    { at: 0.34, h: 90, label: "weights · 14 GB", c: C.base },
    { at: 0.46, h: 90, label: "gradients · 14 GB", c: C.tune },
    { at: 0.58, h: 200, label: "optimizer states · 56+ GB", c: C.red },
    { at: 0.68, h: 70, label: "activations · 20+ GB", c: C.adapt },
  ];
  return (
    <Stage>
      <Head kicker="OPTION A — THE CLASSIC" title="Full fine-tuning: update every weight" color={C.tune} o={p(0, 0.08)} />
      {/* weight grid with continuous update wave */}
      <div style={{ position: "absolute", left: 140, top: 240, opacity: p(0.04, 0.14) }}>
        <div style={{ fontFamily: MONO, fontSize: 24, color: C.muted, marginBottom: 14 }}>7,000,000,000 parameters — <b style={{ color: C.tune }}>all trainable</b></div>
        {Array.from({ length: rowsN }).map((_, r) => (
          <div key={r} style={{ display: "flex", gap: 10, marginBottom: 10 }}>
            {Array.from({ length: cols }).map((_, c) => {
              const d = Math.abs(c - wave + Math.sin(r * 1.7) * 1.4);
              const heat = Math.max(0, 1 - d / 2.6);
              return (
                <div key={c} style={{
                  width: 48, height: 48, borderRadius: 9,
                  background: mix(C.panel, C.tune, 0.08 + heat * 0.75),
                  border: `1.5px solid ${mix(C.line, C.tune, heat)}`,
                  transform: `scale(${1 + heat * 0.14})`,
                  boxShadow: heat > 0.4 ? `0 0 16px ${mix(C.bg0, C.tune, heat)}` : "none",
                }} />
              );
            })}
          </div>
        ))}
      </div>
      {/* VRAM tower */}
      <div style={{ position: "absolute", left: 1120, top: 240, width: 640, opacity: p(0.28, 0.38) }}>
        <div style={{ fontFamily: MONO, fontSize: 24, color: C.muted, marginBottom: 12 }}>GPU memory needed (7B model)</div>
        <div style={{ position: "relative", width: 380, height: 480, border: `2.5px solid ${C.line}`, borderRadius: 18, background: C.panel, display: "flex", flexDirection: "column-reverse", overflow: "hidden" }}>
          {segs.map((s, i) => (
            <div key={i} style={{ height: s.h * p(s.at, s.at + 0.1), background: `linear-gradient(90deg, ${mix(C.panel, s.c, 0.75)}, ${mix(C.panel, s.c, 0.45)})`, borderTop: `2px solid ${s.c}`, display: "flex", alignItems: "center", paddingLeft: 18 }}>
              <span style={{ fontFamily: MONO, fontSize: 21, color: C.text, whiteSpace: "nowrap", opacity: p(s.at + 0.04, s.at + 0.12) }}>{s.label}</span>
            </div>
          ))}
          {/* 24GB consumer line */}
          <div style={{ position: "absolute", bottom: 110, left: 0, right: 0, borderTop: `3px dashed ${C.green}`, opacity: p(0.4, 0.5) }}>
            <span style={{ position: "absolute", right: 8, top: 4, fontFamily: MONO, fontSize: 19, color: C.green }}>consumer GPU · 24 GB</span>
          </div>
        </div>
        <div style={{ marginTop: 18, opacity: p(0.66, 0.76) }}>
          <Counter p={p(0.66, 0.82)} to={112} prefix="≈ " suffix=" GB total" color={C.red} size={52} />
          <span style={{ fontFamily: MONO, fontSize: 25, color: C.red, marginLeft: 16, opacity: 0.6 + Math.sin(frame * 0.12) * 0.4 }}>⚠ won't fit</span>
        </div>
      </div>
      <Foot p={p(0.84, 0.94)}>Training needs weights + gradients + optimizer states — roughly 16× the model size. Best quality, brutal cost. There has to be a smarter way…</Foot>
    </Stage>
  );
};

// ft_lora ----------------------------------------------------------------------
const LoraScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const cart = ["⚖️ legal", "🩺 medical", "🎧 support"];
  return (
    <Stage>
      <Head kicker="OPTION B — THE ELEGANT TRICK" title="LoRA: freeze the base, train tiny adapters" color={C.adapt} o={p(0, 0.08)} />
      {/* frozen W */}
      <div style={{ position: "absolute", left: 200, top: 260, width: 420, height: 420, borderRadius: 26, background: mix(C.panel, C.base, 0.12), border: `4px solid ${C.base}`, opacity: p(0.05, 0.14), display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", gap: 6 }}>
        <div style={{ fontSize: 66, opacity: 0.85 + Math.sin(frame * 0.05) * 0.15 }}>❄️</div>
        <div style={{ fontFamily: MONO, fontWeight: 800, fontSize: 62, color: C.base }}>W</div>
        <div style={{ fontFamily: MONO, fontSize: 24, color: C.muted }}>base weights</div>
        <div style={{ fontFamily: MONO, fontSize: 24, color: C.base, border: `2px solid ${C.base}`, borderRadius: 999, padding: "4px 18px", marginTop: 8 }}>🔒 FROZEN</div>
      </div>
      {/* main path x -> W -> + -> out */}
      <Wire x1={80} y1={470} x2={196} y2={470} p={p(0.08, 0.14)} color={C.muted} w={3} />
      <Wire x1={622} y1={470} x2={1060} y2={470} p={p(0.1, 0.18)} color={C.muted} w={3} />
      {/* bypass: A and B */}
      <Wire x1={110} y1={470} x2={330} y2={790} p={p(0.24, 0.32)} color={C.adapt} w={3.5} curve={-120} />
      <div style={{ position: "absolute", left: 330, top: 730, width: 120, height: 190, borderRadius: 16, background: mix(C.panel, C.adapt, 0.2), border: `3px solid ${C.adapt}`, display: "flex", alignItems: "center", justifyContent: "center", opacity: p(0.28, 0.36), transform: `scale(${0.8 + p(0.28, 0.38) * 0.2})` }}>
        <span style={{ fontFamily: MONO, fontWeight: 800, fontSize: 52, color: C.adapt }}>A</span>
      </div>
      <Wire x1={455} y1={820} x2={600} y2={820} p={p(0.34, 0.4)} color={C.adapt} w={3.5} />
      <div style={{ position: "absolute", left: 605, top: 770, width: 240, height: 100, borderRadius: 16, background: mix(C.panel, C.adapt, 0.2), border: `3px solid ${C.adapt}`, display: "flex", alignItems: "center", justifyContent: "center", opacity: p(0.36, 0.44), transform: `scale(${0.8 + p(0.36, 0.46) * 0.2})` }}>
        <span style={{ fontFamily: MONO, fontWeight: 800, fontSize: 52, color: C.adapt }}>B</span>
      </div>
      <Wire x1={850} y1={820} x2={1075} y2={500} p={p(0.42, 0.5)} color={C.adapt} w={3.5} curve={120} />
      <Flow x1={110} y1={470} x2={330} y2={790} curve={-120} color={C.adapt} n={5} o={p(0.44, 0.52)} />
      <Flow x1={455} y1={820} x2={600} y2={820} color={C.adapt} n={3} o={p(0.44, 0.52)} />
      <Flow x1={850} y1={820} x2={1075} y2={500} curve={120} color={C.adapt} n={5} o={p(0.44, 0.52)} />
      <div style={{ position: "absolute", left: 400, top: 940, fontFamily: MONO, fontSize: 24, color: C.adapt, opacity: p(0.3, 0.4) }}>
        tiny trainable bypass — the “adapter”
      </div>
      {/* plus node */}
      <div style={{ position: "absolute", left: 1060, top: 430, width: 84, height: 84, borderRadius: 84, background: mix(C.panel, C.tune, 0.2), border: `3px solid ${C.tune}`, display: "flex", alignItems: "center", justifyContent: "center", opacity: p(0.44, 0.52) }}>
        <span style={{ fontFamily: MONO, fontWeight: 800, fontSize: 48, color: C.tune }}>+</span>
      </div>
      {/* stats */}
      <div style={{ position: "absolute", left: 1240, top: 270, width: 560, display: "flex", flexDirection: "column", gap: 20 }}>
        <div style={{ background: mix(C.panel, C.adapt, 0.1), border: `2.5px solid ${C.adapt}`, borderRadius: 18, padding: "22px 28px", opacity: p(0.52, 0.62) }}>
          <div style={{ fontFamily: MONO, fontSize: 22, color: C.muted }}>trainable parameters</div>
          <Counter p={p(0.52, 0.7)} to={0.6} prefix="< " suffix=" %" color={C.adapt} size={56} decimals={1} />
        </div>
        <div style={{ background: mix(C.panel, C.green, 0.08), border: `2.5px solid ${C.green}`, borderRadius: 18, padding: "22px 28px", opacity: p(0.6, 0.7) }}>
          <div style={{ fontFamily: MONO, fontSize: 22, color: C.muted }}>quality vs full fine-tune</div>
          <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 44, color: C.green }}>≈ comparable</div>
        </div>
        <div style={{ opacity: p(0.72, 0.82) }}>
          <div style={{ fontFamily: MONO, fontSize: 22, color: C.muted, marginBottom: 10 }}>adapters swap like cartridges (MBs each)</div>
          <div style={{ display: "flex", gap: 14 }}>
            {cart.map((s, i) => {
              const hot = Math.floor(frame / 26) % 3 === i;
              return <div key={i} style={{ fontFamily: MONO, fontSize: 24, fontWeight: 700, color: hot ? C.bg0 : C.adapt, background: hot ? C.adapt : mix(C.panel, C.adapt, 0.14), border: `2px solid ${C.adapt}`, borderRadius: 12, padding: "10px 18px", transform: `translateY(${hot ? -6 : 0}px)` }}>{s}</div>;
            })}
          </div>
        </div>
      </div>
      <Foot p={p(0.84, 0.94)}>The change a fine-tune needs is low-rank — two skinny matrices capture it. Train &lt;1% of parameters, keep the base untouched.</Foot>
    </Stage>
  );
};

// ft_qlora ----------------------------------------------------------------------
const QloraScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const squeeze = p(0.14, 0.42);
  const nB = 12;
  return (
    <Stage>
      <Head kicker="OPTION C — FINE-TUNING FOR EVERYONE" title="QLoRA: quantize the base to 4-bit, LoRA on top" color={C.green} o={p(0, 0.08)} />
      {/* bit blocks squeezing */}
      <div style={{ position: "absolute", left: 150, top: 270, width: 760 }}>
        <div style={{ fontFamily: MONO, fontSize: 24, color: C.muted, marginBottom: 16, opacity: p(0.05, 0.12) }}>
          each frozen weight: <b style={{ color: C.base }}>16-bit</b> → <b style={{ color: C.green }}>4-bit (NF4)</b>
        </div>
        <div style={{ display: "flex", alignItems: "flex-end", gap: 14 }}>
          {Array.from({ length: nB }).map((_, i) => {
            const h = interpolate(squeeze, [i / nB * 0.7, i / nB * 0.7 + 0.3], [200, 58], CL);
            const done = h < 70;
            return (
              <div key={i} style={{
                width: 44, height: h, borderRadius: 10,
                background: mix(C.panel, done ? C.green : C.base, 0.5),
                border: `2px solid ${done ? C.green : C.base}`,
                opacity: p(0.05 + i * 0.008, 0.12 + i * 0.008),
                boxShadow: done ? `0 0 14px ${mix(C.bg0, C.green, 0.6)}` : "none",
              }} />
            );
          })}
        </div>
        {/* memory bar */}
        <div style={{ marginTop: 46, opacity: p(0.4, 0.5) }}>
          <div style={{ fontFamily: MONO, fontSize: 23, color: C.muted, marginBottom: 10 }}>7B base model in memory</div>
          <div style={{ width: 700, height: 46, background: C.panel, border: `2px solid ${C.line}`, borderRadius: 12, overflow: "hidden" }}>
            <div style={{ width: `${interpolate(p(0.42, 0.62), [0, 1], [100, 28])}%`, height: "100%", background: `linear-gradient(90deg, ${C.green}, ${mix(C.green, C.base, 0.5)})`, transition: "none" }} />
          </div>
          <div style={{ display: "flex", gap: 30, marginTop: 12 }}>
            <span style={{ fontFamily: MONO, fontSize: 30, color: C.muted, textDecoration: p(0.5, 0.58) > 0.5 ? "line-through" : "none" }}>14 GB</span>
            <Counter p={p(0.46, 0.62)} to={4} prefix="→ ≈ " suffix=" GB" color={C.green} size={38} />
          </div>
        </div>
      </div>
      {/* GPU card it fits into */}
      <div style={{ position: "absolute", left: 1080, top: 280, width: 700, height: 420, borderRadius: 26, border: `3.5px solid ${p(0.62, 0.7) > 0.5 ? C.green : C.line}`, background: C.panel, opacity: p(0.3, 0.4), padding: 28, boxSizing: "border-box", boxShadow: p(0.62, 0.7) > 0.5 ? `0 0 70px ${mix(C.bg0, C.green, 0.4)}` : "none" }}>
        <div style={{ fontFamily: MONO, fontSize: 24, color: C.muted }}>🖥️ one consumer GPU · 24 GB</div>
        <div style={{
          marginTop: 26, marginLeft: interpolate(p(0.55, 0.7), [0, 1], [640, 0]),
          width: 300, height: 150, borderRadius: 18, background: mix(C.panel, C.green, 0.2), border: `3px solid ${C.green}`,
          display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", opacity: p(0.5, 0.6),
        }}>
          <span style={{ fontFamily: SANS, fontWeight: 800, fontSize: 34, color: C.green }}>4-bit base</span>
          <span style={{ fontFamily: MONO, fontSize: 22, color: C.muted }}>frozen ❄️</span>
        </div>
        <div style={{ display: "flex", gap: 14, marginTop: 20, opacity: p(0.68, 0.78) }}>
          {["A", "B"].map((m, i) => (
            <div key={i} style={{ width: 90, height: 64, borderRadius: 12, background: mix(C.panel, C.adapt, 0.24), border: `2.5px solid ${C.adapt}`, display: "flex", alignItems: "center", justifyContent: "center", transform: `translateY(${Math.sin(frame * 0.07 + i) * 4}px)` }}>
              <span style={{ fontFamily: MONO, fontWeight: 800, fontSize: 34, color: C.adapt }}>{m}</span>
            </div>
          ))}
          <span style={{ fontFamily: MONO, fontSize: 22, color: C.adapt, alignSelf: "center" }}>LoRA adapters — full precision</span>
        </div>
        <div style={{ position: "absolute", right: 26, top: 22, fontSize: 54, opacity: p(0.72, 0.8), transform: `scale(${0.7 + p(0.72, 0.82) * 0.3})` }}>✅</div>
      </div>
      <Foot p={p(0.84, 0.94)}>Frozen weights barely mind 4-bit compression. 14 GB → ~4 GB, so a model that needed a cluster now fine-tunes on one GPU. This made fine-tuning mainstream.</Foot>
    </Stage>
  );
};

// ft_sft — training data typewriter --------------------------------------------
const Type: React.FC<{ text: string; p: number; size?: number; color?: string; mono?: boolean }> = ({ text, p, size = 27, color = C.text, mono }) => {
  const frame = useCurrentFrame();
  const n = Math.round(text.length * p);
  const cursor = p > 0 && p < 1 && Math.floor(frame / 8) % 2 === 0;
  return (
    <span style={{ fontFamily: mono ? MONO : SANS, fontSize: size, color, lineHeight: 1.35 }}>
      {text.slice(0, n)}{cursor ? "▌" : ""}
    </span>
  );
};

const SftScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const bubbles = [
    { role: "system", c: C.muted, text: "You are a concise support agent for Acme Bank.", at: 0.08 },
    { role: "user", c: C.base, text: "I was double-charged for my card fee this month.", at: 0.22 },
    { role: "assistant ★", c: C.tune, text: "Sorry about that! I can see the duplicate ₹499 fee on May 3rd. I've raised reversal #8127 — it will be credited within 2 business days.", at: 0.38 },
  ];
  const toks = ["Sorry", "about", "that!", "I", "can", "see", "the", "duplicate", "fee…"];
  const hot = Math.floor(frame / 14) % toks.length;
  return (
    <Stage>
      <Head kicker="WHAT THE DATA LOOKS LIKE" title="SFT: teach by example — prompt → ideal response" color={C.tune} o={p(0, 0.08)} />
      {/* chat card */}
      <div style={{ position: "absolute", left: 140, top: 240, width: 900, borderRadius: 24, background: C.panel, border: `2.5px solid ${C.line}`, padding: "28px 34px", boxSizing: "border-box", opacity: p(0.04, 0.12) }}>
        <div style={{ fontFamily: MONO, fontSize: 21, color: C.muted, marginBottom: 18 }}>training_example_0421.json</div>
        {bubbles.map((b, i) => (
          <div key={i} style={{ marginBottom: 18, opacity: p(b.at, b.at + 0.05) }}>
            <div style={{ fontFamily: MONO, fontSize: 21, color: b.c, fontWeight: 700, marginBottom: 6 }}>{b.role}</div>
            <div style={{ background: mix(C.panel, b.c, 0.1), border: `2px solid ${mix(C.line, b.c, 0.55)}`, borderRadius: 14, padding: "14px 20px" }}>
              <Type text={b.text} p={p(b.at, b.at + 0.22)} />
            </div>
          </div>
        ))}
      </div>
      {/* next-token panel */}
      <div style={{ position: "absolute", left: 1110, top: 240, width: 670, borderRadius: 24, background: C.panel, border: `2.5px solid ${C.line}`, padding: "28px 32px", boxSizing: "border-box", opacity: p(0.55, 0.65) }}>
        <div style={{ fontFamily: MONO, fontSize: 22, color: C.muted, marginBottom: 18 }}>model predicts the response, token by token</div>
        <div style={{ display: "flex", flexWrap: "wrap", gap: 10 }}>
          {toks.map((tk, i) => (
            <span key={i} style={{
              fontFamily: MONO, fontSize: 25, padding: "8px 14px", borderRadius: 10,
              color: i === hot ? C.bg0 : C.text,
              background: i === hot ? C.tune : mix(C.panel, C.tune, 0.1),
              border: `1.5px solid ${i === hot ? C.tune : C.line}`,
            }}>{tk}</span>
          ))}
        </div>
        <div style={{ marginTop: 26, display: "flex", alignItems: "center", gap: 16 }}>
          <span style={{ fontFamily: MONO, fontSize: 22, color: C.muted }}>each miss nudges the weights</span>
          <span style={{ fontFamily: MONO, fontWeight: 800, fontSize: 30, color: C.tune, transform: `rotate(${Math.sin(frame * 0.1) * 10}deg)` }}>🎛️</span>
        </div>
        <div style={{ marginTop: 22, fontFamily: SANS, fontSize: 26, color: C.text, lineHeight: 1.35, opacity: p(0.72, 0.82) }}>
          A few thousand examples of <b style={{ color: C.tune }}>your tone, format &amp; edge cases</b> → baked into the weights.
        </div>
      </div>
      <Foot p={p(0.86, 0.95)}>After SFT there's no mega-prompt at runtime — the model just is that assistant.</Foot>
    </Stage>
  );
};

// ft_rlhf ------------------------------------------------------------------------
const RlhfScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const dpo = p(0.62, 0.74);
  return (
    <Stage>
      <Head kicker="ALIGNMENT — WHAT HUMANS PREFER" title="RLHF … and the DPO shortcut" color={C.adapt} o={p(0, 0.08)} />
      {/* model */}
      <div style={{ position: "absolute", left: 150, top: 400, width: 260, height: 200, borderRadius: 24, background: mix(C.panel, C.base, 0.14), border: `3px solid ${C.base}`, display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", opacity: p(0.04, 0.12) }}>
        <span style={{ fontSize: 60 }}>🧠</span>
        <span style={{ fontFamily: MONO, fontSize: 24, color: C.base, fontWeight: 700 }}>LLM</span>
      </div>
      {/* two answers */}
      {["A", "B"].map((label, i) => {
        const chosen = i === 1;
        const at = 0.12 + i * 0.06;
        return (
          <React.Fragment key={i}>
            <Wire x1={415} y1={500} x2={585} y2={i === 0 ? 350 : 650} p={p(at, at + 0.06)} color={C.muted} w={3} curve={i === 0 ? 40 : -40} />
            <div style={{ position: "absolute", left: 590, top: i === 0 ? 270 : 570, width: 430, height: 170, borderRadius: 20, background: mix(C.panel, chosen ? C.green : C.red, p(0.3, 0.4) * (chosen ? 0.16 : 0.07) + 0.04), border: `3px solid ${p(0.3, 0.4) > 0.5 ? (chosen ? C.green : C.red) : C.line}`, padding: "18px 24px", boxSizing: "border-box", opacity: p(at + 0.04, at + 0.12) }}>
              <div style={{ fontFamily: MONO, fontSize: 22, color: C.muted }}>answer {label}</div>
              <div style={{ fontFamily: SANS, fontSize: 26, color: C.text, marginTop: 8 }}>{chosen ? "Clear, honest, helpful ✓" : "Rambling, evasive ✗"}</div>
              {chosen && (
                <div style={{ position: "absolute", right: -26, top: -30, fontSize: 64, opacity: p(0.3, 0.38), transform: `scale(${0.6 + p(0.3, 0.4) * 0.4}) rotate(-12deg)` }}>👍</div>
              )}
            </div>
          </React.Fragment>
        );
      })}
      {/* human */}
      <div style={{ position: "absolute", left: 1090, top: 430, fontSize: 82, opacity: p(0.24, 0.32) }}>🧑‍⚖️</div>
      {/* reward model path */}
      <Wire x1={1180} y1={470} x2={1400} y2={470} p={p(0.4, 0.48)} color={dpo > 0.5 ? mix(C.muted, C.bg1, 0.5) : C.adapt} w={3} />
      <div style={{ position: "absolute", left: 1410, top: 400, width: 300, height: 150, borderRadius: 20, background: mix(C.panel, C.adapt, dpo > 0.5 ? 0.04 : 0.14), border: `3px ${dpo > 0.5 ? "dashed" : "solid"} ${dpo > 0.5 ? mix(C.adapt, C.bg1, 0.5) : C.adapt}`, display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", opacity: p(0.44, 0.52) * (dpo > 0.5 ? 0.45 : 1) }}>
        <span style={{ fontFamily: SANS, fontWeight: 800, fontSize: 32, color: C.adapt }}>reward model</span>
        <span style={{ fontFamily: MONO, fontSize: 21, color: C.muted }}>scores answers</span>
      </div>
      {/* RL feedback particles looping back */}
      <Flow x1={1420} y1={560} x2={300} y2={620} curve={-260} color={dpo > 0.5 ? C.green : C.adapt} n={8} o={p(0.5, 0.58)} speed={0.008} />
      <div style={{ position: "absolute", left: 700, top: 856, fontFamily: MONO, fontSize: 23, color: dpo > 0.5 ? C.green : C.adapt, opacity: p(0.52, 0.6) }}>
        {dpo > 0.5 ? "DPO: learn straight from chosen vs rejected pairs" : "RL: nudge the LLM toward higher reward"}
      </div>
      {/* DPO shortcut */}
      <Wire x1={1090} y1={560} x2={340} y2={600} p={dpo} color={C.green} w={5} curve={-160} />
      <div style={{ position: "absolute", left: 1140, top: 620, opacity: dpo, transform: `scale(${0.8 + dpo * 0.2})` }}>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 40, color: C.green, background: mix(C.panel, C.green, 0.12), border: `3px solid ${C.green}`, borderRadius: 16, padding: "12px 28px" }}>
          DPO — skip the reward model
        </div>
      </div>
      <Foot p={p(0.86, 0.95)}>This preference step is what turned raw GPT into ChatGPT. DPO won because it's simpler and stabler than the full RLHF loop.</Foot>
    </Stage>
  );
};

// ft_data — quality beats quantity ------------------------------------------------
const DataScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  // curated (left) side outweighs → sinks; positive tilt drops the gem pan
  const tilt = interpolate(p(0.3, 0.55), [0, 1], [0, 9]) + Math.sin(frame * 0.04) * 0.8;
  return (
    <Stage>
      <Head kicker="THE PART EVERYONE UNDERESTIMATES" title="Data: quality crushes quantity" color={C.green} o={p(0, 0.08)} />
      {/* scale */}
      <div style={{ position: "absolute", left: 660, top: 330, width: 600, height: 420, opacity: p(0.06, 0.16) }}>
        <div style={{ position: "absolute", left: 288, top: 60, width: 24, height: 330, background: mix(C.panel, C.muted, 0.5), borderRadius: 8 }} />
        <div style={{ position: "absolute", left: 150, top: 388, width: 300, height: 26, background: mix(C.panel, C.muted, 0.5), borderRadius: 10 }} />
        {/* beam */}
        <div style={{ position: "absolute", left: 0, top: 46, width: 600, height: 18, background: `linear-gradient(90deg, ${C.green}, ${C.muted}, ${C.red})`, borderRadius: 10, transform: `rotate(${-tilt}deg)`, transformOrigin: "50% 50%" }} />
        {/* pans */}
        {[0, 1].map((s) => {
          const px = s === 0 ? 10 : 530;
          const dy = (s === 0 ? 1 : -1) * tilt * 5.2;
          return (
            <div key={s} style={{ position: "absolute", left: px, top: 90 + dy, width: 120 }}>
              <div style={{ width: 3, height: 70, background: C.muted, margin: "0 auto" }} />
              <div style={{ width: 120, height: 46, borderRadius: "0 0 60px 60px", background: mix(C.panel, s === 0 ? C.green : C.red, 0.3), border: `2.5px solid ${s === 0 ? C.green : C.red}`, display: "flex", alignItems: "center", justifyContent: "center" }}>
                <span style={{ fontSize: 30 }}>{s === 0 ? "💎" : "🗑️"}</span>
              </div>
            </div>
          );
        })}
      </div>
      {/* left: curated */}
      <div style={{ position: "absolute", left: 130, top: 340, width: 470, borderRadius: 22, background: mix(C.panel, C.green, 0.1), border: `3px solid ${C.green}`, padding: "28px 32px", boxSizing: "border-box", opacity: p(0.16, 0.26) }}>
        <Counter p={p(0.18, 0.34)} to={1000} suffix="" color={C.green} size={64} />
        <div style={{ fontFamily: SANS, fontWeight: 700, fontSize: 32, color: C.text, marginTop: 6 }}>curated examples</div>
        <div style={{ fontFamily: MONO, fontSize: 23, color: C.muted, marginTop: 12, lineHeight: 1.4 }}>clean · diverse · consistent<br />LIMA matched huge runs with 1k</div>
        <div style={{ position: "absolute", right: 20, top: 20, fontSize: 34, opacity: 0.5 + Math.sin(frame * 0.09) * 0.5 }}>✨</div>
      </div>
      {/* right: noisy */}
      <div style={{ position: "absolute", left: 1320, top: 340, width: 470, borderRadius: 22, background: mix(C.panel, C.red, 0.07), border: `3px solid ${C.red}`, padding: "28px 32px", boxSizing: "border-box", opacity: p(0.24, 0.34) }}>
        <Counter p={p(0.26, 0.42)} to={100000} suffix="" color={C.red} size={64} />
        <div style={{ fontFamily: SANS, fontWeight: 700, fontSize: 32, color: C.text, marginTop: 6 }}>noisy scraped ones</div>
        <div style={{ fontFamily: MONO, fontSize: 23, color: C.muted, marginTop: 12, lineHeight: 1.4 }}>duplicates · errors · contradictions<br />the model learns your mistakes too</div>
      </div>
      {/* stamp */}
      <div style={{ position: "absolute", left: 0, right: 0, top: 830, textAlign: "center", opacity: p(0.6, 0.7), transform: `scale(${0.9 + p(0.6, 0.72) * 0.1}) rotate(-2deg)` }}>
        <span style={{ fontFamily: SANS, fontWeight: 800, fontSize: 46, color: C.red, border: `4px solid ${C.red}`, borderRadius: 14, padding: "10px 34px", background: mix(C.bg1, C.red, 0.08) }}>
          garbage in → garbage baked in
        </span>
      </div>
      <Foot p={p(0.82, 0.92)}>Curate, deduplicate, cover edge cases — the highest-leverage hour in the whole pipeline.</Foot>
    </Stage>
  );
};

// ft_pitfalls ----------------------------------------------------------------------
const PitfallsScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const drain = p(0.12, 0.42);
  const skills = [
    { name: "your task", from: 0.35, to: 0.96, c: C.tune },
    { name: "reasoning", from: 0.85, to: 0.38, c: C.base },
    { name: "coding", from: 0.8, to: 0.34, c: C.base },
    { name: "languages", from: 0.75, to: 0.3, c: C.base },
  ];
  // overfit curves
  const cp = p(0.5, 0.95);
  const N = 60;
  const pts = (which: "train" | "val") =>
    Array.from({ length: N }).map((_, i) => {
      const t = i / (N - 1);
      const x = 1080 + t * 660;
      const yTrain = 800 - 300 * (1 - Math.exp(-t * 3.4));
      const yVal = 800 - 300 * (1 - Math.exp(-t * 3.4)) + (t > 0.45 ? (t - 0.45) * 520 : 0);
      return `${x},${which === "train" ? yTrain : Math.min(yVal, 810)}`;
    }).join(" ");
  const visN = Math.max(2, Math.round(N * cp));
  return (
    <Stage>
      <Head kicker="TWO WAYS IT GOES WRONG" title="Catastrophic forgetting · overfitting" color={C.red} o={p(0, 0.08)} />
      {/* forgetting bars */}
      <div style={{ position: "absolute", left: 140, top: 250, width: 800, opacity: p(0.06, 0.14) }}>
        <div style={{ fontFamily: SANS, fontWeight: 700, fontSize: 32, color: C.red }}>1 · catastrophic forgetting</div>
        {skills.map((s, i) => {
          const v = interpolate(drain, [0, 1], [s.from, s.to]) + Math.sin(frame * 0.06 + i * 2) * 0.012;
          const bad = s.c === C.base && drain > 0.6;
          return (
            <div key={i} style={{ marginTop: 26 }}>
              <div style={{ display: "flex", justifyContent: "space-between", fontFamily: MONO, fontSize: 22, color: bad ? C.red : C.muted }}>
                <span>{s.name}</span><span>{Math.round(v * 100)}%</span>
              </div>
              <div style={{ height: 30, background: C.panel, border: `1.5px solid ${C.line}`, borderRadius: 9, overflow: "hidden", marginTop: 6 }}>
                <div style={{ width: `${v * 100}%`, height: "100%", background: bad ? `linear-gradient(90deg, ${s.c}, ${C.red})` : s.c, opacity: 0.85 }} />
              </div>
            </div>
          );
        })}
        <div style={{ fontFamily: MONO, fontSize: 22, color: C.muted, marginTop: 18, opacity: p(0.34, 0.44) }}>one metric climbs — everything else quietly decays</div>
      </div>
      {/* overfitting chart */}
      <div style={{ position: "absolute", left: 1040, top: 250, width: 760, opacity: p(0.46, 0.54) }}>
        <div style={{ fontFamily: SANS, fontWeight: 700, fontSize: 32, color: C.red }}>2 · overfitting</div>
      </div>
      <svg style={{ position: "absolute", left: 0, top: 0, overflow: "visible" }} width={BW} height={BH}>
        <line x1={1080} y1={810} x2={1760} y2={810} stroke={C.line} strokeWidth={2} opacity={p(0.48, 0.56)} />
        <line x1={1080} y1={430} x2={1080} y2={810} stroke={C.line} strokeWidth={2} opacity={p(0.48, 0.56)} />
        <polyline points={pts("train").split(" ").slice(0, visN).join(" ")} fill="none" stroke={C.green} strokeWidth={5} />
        <polyline points={pts("val").split(" ").slice(0, visN).join(" ")} fill="none" stroke={C.red} strokeWidth={5} strokeDasharray="10 7" />
        {cp > 0.55 && (
          <circle cx={1080 + 0.5 * 660} cy={800 - 300 * (1 - Math.exp(-0.5 * 3.4))} r={12 + Math.sin(frame * 0.15) * 4} fill="none" stroke={C.red} strokeWidth={3} />
        )}
      </svg>
      <div style={{ position: "absolute", left: 1100, top: 460, fontFamily: MONO, fontSize: 22, color: C.green, opacity: p(0.56, 0.64) }}>train loss ↓</div>
      <div style={{ position: "absolute", left: 1520, top: 560, fontFamily: MONO, fontSize: 22, color: C.red, opacity: p(0.62, 0.7) }}>validation loss ↗ = memorizing</div>
      {/* fixes */}
      <div style={{ position: "absolute", left: 0, right: 0, top: 900, display: "flex", justifyContent: "center", gap: 18, opacity: p(0.78, 0.88) }}>
        {["low learning rate", "1–3 epochs", "held-out eval set", "LoRA: frozen weights can't forget"].map((f, i) => (
          <div key={i} style={{ fontFamily: MONO, fontSize: 23, fontWeight: 700, color: C.green, background: mix(C.panel, C.green, 0.1), border: `2px solid ${C.green}`, borderRadius: 999, padding: "10px 24px", transform: `translateY(${(1 - p(0.78 + i * 0.03, 0.88 + i * 0.03)) * 18}px)` }}>✓ {f}</div>
        ))}
      </div>
    </Stage>
  );
};

// ft_workflow ------------------------------------------------------------------------
const WorkflowScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const steps = [
    { at: 0.08, icon: "🧠", name: "Base model", sub: "Llama · Mistral · Qwen (instruct)" },
    { at: 0.24, icon: "🗂️", name: "Dataset", sub: "curate pairs · split eval" },
    { at: 0.42, icon: "🎛️", name: "Train", sub: "LoRA/QLoRA · PEFT · Axolotl · Unsloth" },
    { at: 0.6, icon: "📊", name: "Evaluate", sub: "benchmarks · side-by-side vs base" },
    { at: 0.74, icon: "🚀", name: "Deploy", sub: "merge adapter or hot-swap" },
  ];
  const xs = steps.map((_, i) => 170 + i * 350);
  return (
    <Stage>
      <Head kicker="THE WHOLE RECIPE" title="Fine-tuning, end to end" color={C.tune} o={p(0, 0.08)} />
      {steps.map((s, i) => {
        const on = p(s.at, s.at + 0.09);
        const done = p(s.at + 0.1, s.at + 0.14);
        return (
          <React.Fragment key={i}>
            {i > 0 && <Wire x1={xs[i - 1] + 290} y1={520} x2={xs[i]} y2={520} p={p(s.at - 0.05, s.at)} color={C.tune} w={3.5} />}
            <div style={{ position: "absolute", left: xs[i], top: 400, width: 290, height: 240, borderRadius: 22, background: mix(C.panel, C.tune, 0.08 + on * 0.06), border: `3px solid ${on > 0.5 ? C.tune : C.line}`, padding: "22px 24px", boxSizing: "border-box", opacity: on, transform: `translateY(${(1 - on) * 26}px) scale(${0.94 + on * 0.06})`, boxShadow: on > 0.5 ? `0 0 44px ${mix(C.bg0, C.tune, 0.25 + Math.sin(frame * 0.07 + i) * 0.08)}` : "none" }}>
              <div style={{ fontSize: 52 }}>{s.icon}</div>
              <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 30, color: C.text, marginTop: 8 }}>{i + 1} · {s.name}</div>
              <div style={{ fontFamily: MONO, fontSize: 20, color: C.muted, marginTop: 8, lineHeight: 1.35 }}>{s.sub}</div>
              <div style={{ position: "absolute", right: 16, top: 14, fontSize: 34, color: C.green, opacity: done, transform: `scale(${0.5 + done * 0.5})` }}>✓</div>
            </div>
          </React.Fragment>
        );
      })}
      {/* iterate loop back */}
      <Wire x1={xs[4] + 145} y1={650} x2={xs[1] + 145} y2={655} p={p(0.82, 0.92)} color={C.adapt} w={3.5} curve={-210} />
      <div style={{ position: "absolute", left: 0, right: 0, top: 830, textAlign: "center", opacity: p(0.86, 0.94) }}>
        <span style={{ fontFamily: MONO, fontWeight: 700, fontSize: 27, color: C.adapt, background: mix(C.panel, C.adapt, 0.1), border: `2px solid ${C.adapt}`, borderRadius: 999, padding: "10px 30px" }}>↻ iterate — a solid specialist in days, not months</span>
      </div>
    </Stage>
  );
};

// ft_recap -----------------------------------------------------------------------
const RecapScene: React.FC<{ dur?: number; items?: string[]; closer?: string }> = ({
  dur, items = [], closer = "Fine-tuning: the craft of turning a generalist into your specialist.",
}) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  return (
    <AbsoluteFill style={{ padding: "70px 130px", justifyContent: "center" }}>
      <Knob x={120} y={140} r={52} speed={0.5} color={C.tune} o={0.5} />
      <Knob x={1800} y={950} r={68} speed={-0.4} color={C.adapt} o={0.5} />
      <div style={{ opacity: p(0, 0.06), textAlign: "center", marginBottom: 30 }}>
        <Kicker text="RECAP — THE WHOLE MAP" cx />
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 62, color: C.text, marginTop: 12, letterSpacing: -1.5 }}>Fine-tuning in one breath</div>
      </div>
      <div style={{ display: "flex", flexDirection: "column", gap: 13, maxWidth: 1340, margin: "0 auto", width: "100%" }}>
        {items.map((it, i) => {
          const at = 0.06 + i * 0.09;
          const o = p(at, at + 0.07);
          return (
            <div key={i} style={{ display: "flex", alignItems: "center", gap: 18, opacity: o, transform: `translateX(${(1 - o) * -26}px)`, background: mix(C.panel, C.tune, 0.05), border: `1.5px solid ${C.line}`, borderLeft: `4px solid ${C.tune}`, borderRadius: 12, padding: "15px 26px" }}>
              <span style={{ color: C.tune, fontFamily: MONO, fontWeight: 700, fontSize: 26 }}>{i + 1}</span>
              <span style={{ fontFamily: SANS, fontSize: 30, color: C.text, lineHeight: 1.25 }}>{it}</span>
            </div>
          );
        })}
      </div>
      <div style={{ textAlign: "center", marginTop: 34, opacity: p(0.8, 0.9) }}>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontStyle: "italic", fontSize: 42, color: C.tune, textShadow: `0 0 ${30 + Math.sin(frame * 0.06) * 14}px ${mix(C.bg0, C.tune, 0.7)}` }}>{closer}</div>
      </div>
    </AbsoluteFill>
  );
};

// ===========================================================================
export interface FTSceneProps { variant: string;[key: string]: unknown; }

export const FTScene: React.FC<FTSceneProps> = ({ variant, ...rest }) => {
  let content: React.ReactNode = null;
  let accent = C.tune;
  switch (variant) {
    case "ft_title": content = <TitleScene {...(rest as any)} />; break;
    case "ft_hook": content = <HookScene {...(rest as any)} />; break;
    case "ft_scale": content = <ScaleScene {...(rest as any)} />; accent = C.base; break;
    case "ft_when": content = <WhenScene {...(rest as any)} />; accent = C.green; break;
    case "ft_family": content = <FamilyScene {...(rest as any)} />; accent = C.adapt; break;
    case "ft_full": content = <FullScene {...(rest as any)} />; break;
    case "ft_lora": content = <LoraScene {...(rest as any)} />; accent = C.adapt; break;
    case "ft_qlora": content = <QloraScene {...(rest as any)} />; accent = C.green; break;
    case "ft_sft": content = <SftScene {...(rest as any)} />; break;
    case "ft_rlhf": content = <RlhfScene {...(rest as any)} />; accent = C.adapt; break;
    case "ft_data": content = <DataScene {...(rest as any)} />; accent = C.green; break;
    case "ft_pitfalls": content = <PitfallsScene {...(rest as any)} />; accent = C.red; break;
    case "ft_workflow": content = <WorkflowScene {...(rest as any)} />; break;
    case "ft_recap": content = <RecapScene {...(rest as any)} />; break;
    default: content = <TitleScene {...(rest as any)} />;
  }
  return (
    <AbsoluteFill>
      <Bg accent={accent} />
      {content}
    </AbsoluteFill>
  );
};

export default FTScene;
