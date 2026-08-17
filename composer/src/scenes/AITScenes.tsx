/**
 * AITScenes.tsx — "AI Trading, Honestly" (~90 min, English, India-first, realist).
 *
 * Identity
 *   theme  : dark quant-terminal (cyan primary)
 *   motif  : the SIGNAL STACK pipeline  Data → Features → Model → Signal → Risk → Order
 *            (recurs as a scene archetype + as ambient) + a live candlestick TAPE that
 *            scrolls under every scene (continuous motion) + a scene-progress bar.
 *   colors : cyan=DATA/inputs · violet=AI/model/agent · green=MONEY/execution ·
 *            red=RISK/reality-check · amber=EDGE/signal/highlight
 *
 * Everything is props-driven parameterized archetypes so a ~60-beat video is authored
 * from build.py, not 60 bespoke components. Rules (skills/03): duration-aware phasing
 * via useP(dur); continuous motion in every frame; determinism via rnd(), never random.
 */
import React from "react";
import { AbsoluteFill, interpolate, useCurrentFrame } from "remotion";
import {
  makeTheme, mix, useP, usePop, rnd, MONO, SANS,
  Bg, Stage, Kicker, Head, Foot, Card, Flow, Wire, Counter, Type, Brackets, ScanBeam,
} from "../lib/primitives";

// ------------------------------------------------------------------ identity
const T = makeTheme({
  bg0: "#04060D", bg1: "#080C18", bg2: "#0F1628", panel: "#141B30",
  text: "#EEF2FC", muted: "#8892AE", line: "rgba(255,255,255,0.08)", accent: "#22D3EE",
});
const A = {
  data: "#22D3EE",  // cyan   — inputs / data
  ai: "#A78BFA",    // violet — AI / model / agent
  money: "#34D399",  // green  — money / execution / go
  risk: "#F87171",  // red    — risk / loss / reality-check
  edge: "#FBBF24",  // amber  — edge / signal / highlight
};
const ACCENT: Record<string, string> = { data: A.data, ai: A.ai, money: A.money, risk: A.risk, edge: A.edge };
const col = (c?: string) => (c && ACCENT[c]) || c || A.data;

// ------------------------------------------------------------------ ambient: candlestick tape
// A deterministic random-walk OHLC series, precomputed once at module scope. A window of
// it scrolls along the bottom of every scene — the "market is live" signal + identity.
const SERIES = (() => {
  const out: { o: number; h: number; l: number; c: number; up: boolean }[] = [];
  let price = 100;
  for (let i = 0; i < 320; i++) {
    const drift = (rnd(i, 7) - 0.47) * 4.2;
    const o = price;
    const c = Math.max(24, price + drift);
    const h = Math.max(o, c) + rnd(i, 3) * 2.6;
    const l = Math.min(o, c) - rnd(i, 9) * 2.6;
    out.push({ o, h, l, c, up: c >= o });
    price = c;
  }
  return out;
})();

const CandleTape: React.FC<{ y?: number; h?: number; o?: number }> = ({ y = 992, h = 74, o = 0.5 }) => {
  const frame = useCurrentFrame();
  const N = 46;
  const start = Math.floor(frame * 0.16) % (SERIES.length - N);
  const win = SERIES.slice(start, start + N);
  let lo = Infinity, hi = -Infinity;
  win.forEach((d) => { lo = Math.min(lo, d.l); hi = Math.max(hi, d.h); });
  const cw = 1920 / N;
  const yFor = (v: number) => y + h - ((v - lo) / (hi - lo || 1)) * h;
  return (
    <div style={{ position: "absolute", left: 0, top: 0, width: 1920, height: 1080, opacity: o, pointerEvents: "none" }}>
      {win.map((d, i) => {
        const cx = i * cw + cw / 2;
        const c = d.up ? A.money : A.risk;
        const bt = yFor(Math.max(d.o, d.c)), bb = yFor(Math.min(d.o, d.c));
        return (
          <React.Fragment key={i}>
            <div style={{ position: "absolute", left: cx - 0.75, top: yFor(d.h), width: 1.5, height: Math.max(1, yFor(d.l) - yFor(d.h)), background: c, opacity: 0.5 }} />
            <div style={{ position: "absolute", left: cx - cw * 0.28, top: bt, width: cw * 0.56, height: Math.max(2, bb - bt), background: c, opacity: 0.6, borderRadius: 1 }} />
          </React.Fragment>
        );
      })}
    </div>
  );
};

/** Universal "this is playing" bar at the very bottom edge, fills L→R over the beat. */
const SceneProgress: React.FC<{ dur?: number; color?: string }> = ({ dur, color = A.data }) => {
  const p = useP(dur);
  return (
    <div style={{ position: "absolute", left: 0, top: 1074, width: 1920, height: 6 }}>
      <div style={{ height: "100%", width: interpolate(p(0, 1), [0, 1], [0, 1920]), background: `linear-gradient(90deg, ${color}, ${mix(color, "#ffffff", 0.25)})`, boxShadow: `0 0 14px ${color}` }} />
    </div>
  );
};

// ------------------------------------------------------------------ small shared bits
const Chip: React.FC<{ c: string; children: React.ReactNode; o?: number; solid?: boolean; size?: number }> = ({ c, children, o = 1, solid, size = 22 }) => (
  <span style={{
    fontFamily: MONO, fontWeight: 700, fontSize: size, letterSpacing: 0.4,
    color: solid ? T.bg0 : c, background: solid ? c : mix(T.panel, c, 0.14),
    border: `2px solid ${c}`, borderRadius: 999, padding: "8px 20px", opacity: o, whiteSpace: "nowrap",
  }}>{children}</span>
);

const Pill: React.FC<{ label: string; c: string; sub?: string; o?: number; x: number; y: number; w: number; h?: number; emoji?: string; glow?: boolean }> = ({ label, c, sub, o = 1, x, y, w, h = 92, emoji, glow }) => {
  const frame = useCurrentFrame();
  return (
    <div style={{
      position: "absolute", left: x, top: y, width: w, height: h, borderRadius: 16,
      background: mix(T.panel, c, 0.1), border: `2.5px solid ${c}`, boxSizing: "border-box",
      display: "flex", flexDirection: "column", justifyContent: "center", padding: "0 22px",
      opacity: o, transform: `translateY(${(1 - o) * 20}px)`,
      boxShadow: glow ? `0 0 34px ${mix(T.bg0, c, 0.3 + Math.sin(frame * 0.06) * 0.08)}` : "none",
    }}>
      <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
        {emoji && <span style={{ fontSize: 34 }}>{emoji}</span>}
        <span style={{ fontFamily: SANS, fontWeight: 800, fontSize: 27, color: T.text }}>{label}</span>
      </div>
      {sub && <div style={{ fontFamily: MONO, fontSize: 19, color: T.muted, marginTop: 5 }}>{sub}</div>}
    </div>
  );
};

// =================================================================== TITLE
const TitleScene: React.FC<any> = ({ dur, kicker = "AI TRADING · HONEST FULL COURSE", line1 = "AI Trading,", line2 = "Honestly", sub = "what it is · how to start · where to do it · how to build it" }) => {
  const frame = useCurrentFrame();
  const p = useP(dur); const pop = usePop(dur);
  const stages = ["DATA", "MODEL", "SIGNAL", "RISK", "ORDER"];
  return (
    <AbsoluteFill style={{ alignItems: "center", justifyContent: "center" }}>
      {/* ambient: orbiting agent nodes */}
      {Array.from({ length: 9 }).map((_, i) => {
        const ang = frame * 0.011 + (i / 9) * Math.PI * 2;
        const c = [A.data, A.ai, A.money, A.edge][i % 4];
        return <div key={i} style={{ position: "absolute", left: 960 + Math.cos(ang) * (600 + i * 12) - 5, top: 540 + Math.sin(ang) * (270 + i * 7) - 5, width: 9, height: 9, borderRadius: 9, background: c, opacity: 0.22 + rnd(i, 1) * 0.28, boxShadow: `0 0 12px ${c}` }} />;
      })}
      <div style={{ textAlign: "center", transform: `scale(${0.93 + pop(0) * 0.07})` }}>
        <div style={{ display: "flex", justifyContent: "center", marginBottom: 26 }}><Kicker theme={T} text={kicker} cx /></div>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 128, lineHeight: 1.0, letterSpacing: -4, color: T.text }}>
          <div>{line1}</div>
          <div style={{ color: A.data, textShadow: `0 0 70px ${mix(T.bg0, A.data, 0.7)}` }}>{line2}</div>
        </div>
        <div style={{ height: 5, width: interpolate(p(0.18, 0.45), [0, 1], [0, 560]), background: `linear-gradient(90deg, ${A.data}, ${A.ai})`, borderRadius: 3, margin: "30px auto" }} />
        <div style={{ fontFamily: SANS, fontSize: 37, color: T.muted, opacity: p(0.26, 0.46) }}>{sub}</div>
        {/* the SIGNAL STACK motif introduced under the title */}
        <div style={{ display: "flex", justifyContent: "center", gap: 12, marginTop: 40, opacity: p(0.5, 0.68) }}>
          {stages.map((s, i) => {
            const c = [A.data, A.ai, A.edge, A.risk, A.money][i];
            const hot = Math.floor(frame / 20) % stages.length === i;
            return (
              <React.Fragment key={i}>
                <span style={{ fontFamily: MONO, fontWeight: 700, fontSize: 20, color: hot ? T.bg0 : c, background: hot ? c : mix(T.panel, c, 0.12), border: `2px solid ${c}`, borderRadius: 8, padding: "8px 16px" }}>{s}</span>
                {i < stages.length - 1 && <span style={{ color: T.muted, fontSize: 22, alignSelf: "center" }}>→</span>}
              </React.Fragment>
            );
          })}
        </div>
      </div>
    </AbsoluteFill>
  );
};

// =================================================================== DIVIDER
const DividerScene: React.FC<any> = ({ dur, n = 1, title = "", sub = "", color = "data", parts = 6 }) => {
  const frame = useCurrentFrame(); const p = useP(dur); const c = col(color);
  return (
    <Stage>
      <Brackets x={330} y={300} w={1260} h={470} color={c} o={p(0.02, 0.14)} len={54} />
      <ScanBeam theme={T} x={340} y={310} w={1240} h={450} color={c} o={p(0.05, 0.2)} speed={1.6} />
      <div style={{ position: "absolute", left: 0, right: 0, top: 358, textAlign: "center" }}>
        <div style={{ fontFamily: MONO, fontWeight: 800, fontSize: 34, color: c, letterSpacing: 10, opacity: p(0.05, 0.15) }}>PART {"0" + n}</div>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 94, color: T.text, letterSpacing: -2, marginTop: 18, opacity: p(0.12, 0.24), transform: `translateY(${(1 - p(0.12, 0.24)) * 28}px)` }}>{title}</div>
        <div style={{ height: 5, width: interpolate(p(0.2, 0.5), [0, 1], [0, 440]), background: c, borderRadius: 3, margin: "24px auto" }} />
        <div style={{ fontFamily: SANS, fontSize: 34, color: T.muted, opacity: p(0.3, 0.45) }}>{sub}</div>
      </div>
      <div style={{ position: "absolute", left: 0, right: 0, top: 858, display: "flex", justifyContent: "center", gap: 16, opacity: p(0.3, 0.45) }}>
        {Array.from({ length: parts }).map((_, i) => {
          const idx = i + 1;
          return <div key={i} style={{ width: idx === n ? 44 : 14, height: 14, borderRadius: 8, background: idx <= n ? c : mix(T.panel, c, 0.15), border: `1.5px solid ${idx <= n ? c : T.line}`, opacity: idx === n ? 0.7 + Math.sin(frame * 0.1) * 0.3 : 1 }} />;
        })}
      </div>
    </Stage>
  );
};

// =================================================================== HOOK (two-sided contrast)
const HookScene: React.FC<any> = ({ dur, kicker = "THE TWO TRUTHS", title = "", left = {}, right = {}, closer = "" }) => {
  const frame = useCurrentFrame(); const p = useP(dur);
  const side = (d: any, x: number, at: number, c: string) => (
    <div style={{ position: "absolute", left: x, top: 300, width: 760, opacity: p(at, at + 0.1), transform: `translateY(${(1 - p(at, at + 0.1)) * 24}px)` }}>
      <div style={{ borderRadius: 22, background: mix(T.panel, c, 0.1), border: `2.5px solid ${c}`, padding: "34px 36px", minHeight: 360, boxShadow: `0 0 44px ${mix(T.bg0, c, 0.16 + Math.sin(frame * 0.05) * 0.05)}` }}>
        <div style={{ fontSize: 56 }}>{d.emoji}</div>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 40, color: c, marginTop: 12 }}>{d.h}</div>
        <div style={{ fontFamily: SANS, fontSize: 29, color: T.text, marginTop: 16, lineHeight: 1.4 }}>{d.body}</div>
      </div>
    </div>
  );
  return (
    <Stage>
      <Head theme={T} kicker={kicker} title={title} o={p(0, 0.06)} />
      {side(left, 100, 0.12, col(left.c) || A.money)}
      <div style={{ position: "absolute", left: 900, top: 520, width: 120, textAlign: "center", opacity: p(0.34, 0.44) }}>
        <span style={{ fontFamily: MONO, fontWeight: 800, fontSize: 40, color: T.muted }}>vs</span>
      </div>
      {side(right, 1060, 0.3, col(right.c) || A.risk)}
      {closer && <Foot theme={T} p={p(0.7, 0.82)}>{closer}</Foot>}
    </Stage>
  );
};

// =================================================================== PIPELINE (the Signal Stack motif)
const PipelineScene: React.FC<any> = ({ dur, kicker = "THE SIGNAL STACK", title = "", stages = [], caption = "", activeIdx = -1 }) => {
  const frame = useCurrentFrame(); const p = useP(dur);
  const n = stages.length; const w = 270, gap = (1720 - n * w) / Math.max(1, n - 1);
  const y = 440, h = 190;
  return (
    <Stage>
      <Head theme={T} kicker={kicker} title={title} o={p(0, 0.06)} />
      {stages.map((s: any, i: number) => {
        const x = 100 + i * (w + gap); const c = col(s.c);
        const at = 0.08 + i * 0.12;
        const hot = activeIdx === i || (activeIdx < 0 && Math.floor(frame / 24) % n === i);
        return (
          <React.Fragment key={i}>
            {i > 0 && <>
              <Wire x1={100 + (i - 1) * (w + gap) + w} y1={y + h / 2} x2={x} y2={y + h / 2} p={p(at - 0.05, at)} color={c} w={3.5} />
              <Flow x1={100 + (i - 1) * (w + gap) + w} y1={y + h / 2} x2={x} y2={y + h / 2} color={c} n={5} o={p(at, at + 0.1)} />
            </>}
            <div style={{ position: "absolute", left: x, top: y, width: w, height: h, borderRadius: 18, background: mix(T.panel, c, hot ? 0.2 : 0.09), border: `2.5px solid ${c}`, boxSizing: "border-box", padding: "20px 20px", opacity: p(at, at + 0.09), transform: `translateY(${(1 - p(at, at + 0.09)) * 22}px) scale(${hot ? 1.04 : 1})`, boxShadow: hot ? `0 0 34px ${mix(T.bg0, c, 0.32)}` : "none" }}>
              <div style={{ fontFamily: MONO, fontWeight: 700, fontSize: 19, color: c, letterSpacing: 1 }}>{"0" + (i + 1)}</div>
              <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 30, color: T.text, marginTop: 8 }}>{s.label}</div>
              <div style={{ fontFamily: SANS, fontSize: 20, color: T.muted, marginTop: 8, lineHeight: 1.32 }}>{s.sub}</div>
            </div>
          </React.Fragment>
        );
      })}
      {caption && <Foot theme={T} p={p(0.78, 0.9)}>{caption}</Foot>}
    </Stage>
  );
};

// =================================================================== CARDS (2/3/4 grid)
const CardsScene: React.FC<any> = ({ dur, kicker = "", title = "", color = "data", cards = [], caption = "" }) => {
  const p = useP(dur);
  const n = cards.length;
  const cols = n <= 2 ? n : n <= 4 ? 2 : 3;
  const rows = Math.ceil(n / cols);
  const gapX = 40, gapY = 34;
  const w = (1720 - (cols - 1) * gapX) / cols;
  const h = rows === 1 ? 480 : 300;
  const y0 = rows === 1 ? 250 : 240;
  return (
    <Stage>
      <Head theme={T} kicker={kicker} title={title} color={col(color)} o={p(0, 0.06)} />
      {cards.map((cd: any, i: number) => {
        const r = Math.floor(i / cols), cc = i % cols;
        const x = 100 + cc * (w + gapX), y = y0 + r * (h + gapY);
        const c = col(cd.c || color); const at = 0.08 + i * 0.11;
        return (
          <Card key={i} theme={T} x={x} y={y} w={w} h={h} color={c} o={p(at, at + 0.09)} glow={i === 0}>
            <div style={{ display: "flex", alignItems: "center", gap: 14 }}>
              {cd.emoji && <span style={{ fontSize: 44 }}>{cd.emoji}</span>}
              <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 32, color: c }}>{cd.title}</div>
            </div>
            <div style={{ fontFamily: SANS, fontSize: 25, color: T.text, marginTop: 16, lineHeight: 1.4 }}>{cd.body}</div>
            {cd.tag && <div style={{ position: "absolute", left: 24, bottom: 20 }}><Chip c={c} size={19}>{cd.tag}</Chip></div>}
          </Card>
        );
      })}
      {caption && <Foot theme={T} p={p(0.8, 0.9)}>{caption}</Foot>}
    </Stage>
  );
};

// =================================================================== SPECTRUM (ladder of levels)
const SpectrumScene: React.FC<any> = ({ dur, kicker = "THE SPECTRUM", title = "", levels = [], caption = "", axis = ["simpler", "more autonomous"] }) => {
  const frame = useCurrentFrame(); const p = useP(dur);
  const n = levels.length; const w = 300, gap = (1720 - n * w) / Math.max(1, n - 1);
  const baseY = 720;
  return (
    <Stage>
      <Head theme={T} kicker={kicker} title={title} color={A.ai} o={p(0, 0.06)} />
      {/* axis arrow */}
      <div style={{ position: "absolute", left: 100, top: baseY + 150, width: 1720, height: 2, background: mix(T.line, A.ai, 0.4), opacity: p(0.04, 0.12) }} />
      <div style={{ position: "absolute", left: 100, top: baseY + 168, fontFamily: MONO, fontSize: 20, color: T.muted, opacity: p(0.06, 0.14) }}>◄ {axis[0]}</div>
      <div style={{ position: "absolute", left: 1520, top: baseY + 168, width: 300, textAlign: "right", fontFamily: MONO, fontSize: 20, color: T.muted, opacity: p(0.06, 0.14) }}>{axis[1]} ►</div>
      {levels.map((lv: any, i: number) => {
        const x = 100 + i * (w + gap); const c = col(lv.c);
        const at = 0.1 + i * 0.14; const barH = 90 + i * 84;
        const hot = Math.floor(frame / 26) % n === i;
        return (
          <React.Fragment key={i}>
            <div style={{ position: "absolute", left: x, top: baseY - barH, width: w, height: barH, borderRadius: "16px 16px 0 0", background: `linear-gradient(180deg, ${mix(T.panel, c, 0.28)}, ${mix(T.panel, c, 0.09)})`, border: `2.5px solid ${c}`, borderBottom: "none", opacity: p(at, at + 0.08), transform: `scale(${hot ? 1.02 : 1})`, transformOrigin: "bottom center", boxShadow: hot ? `0 0 30px ${mix(T.bg0, c, 0.3)}` : "none" }} />
            <div style={{ position: "absolute", left: x, top: baseY - barH - 92, width: w, textAlign: "center", opacity: p(at + 0.02, at + 0.1) }}>
              <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 28, color: c }}>{lv.label}</div>
              <div style={{ fontFamily: SANS, fontSize: 20, color: T.muted, marginTop: 6, lineHeight: 1.3, padding: "0 6px" }}>{lv.sub}</div>
            </div>
            <div style={{ position: "absolute", left: x, top: baseY - 46, width: w, textAlign: "center", fontFamily: MONO, fontWeight: 700, fontSize: 22, color: T.bg0, opacity: p(at + 0.02, at + 0.1) }}>{lv.tag}</div>
          </React.Fragment>
        );
      })}
      {caption && <Foot theme={T} p={p(0.8, 0.9)}>{caption}</Foot>}
    </Stage>
  );
};

// =================================================================== STAT (big numbers)
const StatScene: React.FC<any> = ({ dur, kicker = "BY THE NUMBERS", title = "", color = "risk", stats = [], note = "" }) => {
  const p = useP(dur); const n = stats.length;
  const w = (1720 - (n - 1) * 40) / n;
  return (
    <Stage>
      <Head theme={T} kicker={kicker} title={title} color={col(color)} o={p(0, 0.06)} />
      {stats.map((s: any, i: number) => {
        const x = 100 + i * (w + 40); const c = col(s.c || color); const at = 0.14 + i * 0.16;
        return (
          <div key={i} style={{ position: "absolute", left: x, top: 320, width: w, height: 380, borderRadius: 22, background: mix(T.panel, c, 0.1), border: `2.5px solid ${c}`, boxSizing: "border-box", padding: "34px 28px", display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", textAlign: "center", opacity: p(at, at + 0.08) }}>
            <div style={{ display: "flex", alignItems: "baseline", justifyContent: "center" }}>
              <Counter p={p(at + 0.04, at + 0.24)} to={s.value} prefix={s.prefix || ""} suffix={s.suffix || ""} color={c} size={92} decimals={s.decimals || 0} comma={s.comma} />
            </div>
            <div style={{ fontFamily: SANS, fontWeight: 700, fontSize: 27, color: T.text, marginTop: 20, lineHeight: 1.35 }}>{s.label}</div>
            {s.src && <div style={{ fontFamily: MONO, fontSize: 17, color: T.muted, marginTop: 14 }}>{s.src}</div>}
          </div>
        );
      })}
      {note && <Foot theme={T} p={p(0.78, 0.9)}>{note}</Foot>}
    </Stage>
  );
};

// =================================================================== BARS (chart)
const BarsScene: React.FC<any> = ({ dur, kicker = "", title = "", color = "data", bars = [], unit = "", note = "", max = 100 }) => {
  const frame = useCurrentFrame(); const p = useP(dur);
  const n = bars.length; const bw = Math.min(150, (1560 / n) - 34);
  const step = 1560 / n; const X0 = 200; const Y0 = 800; const SCALE = 470 / max;
  return (
    <Stage>
      <Head theme={T} kicker={kicker} title={title} color={col(color)} o={p(0, 0.06)} />
      {/* baseline */}
      <div style={{ position: "absolute", left: X0 - 40, top: Y0, width: 1600, height: 2, background: T.line, opacity: p(0.02, 0.1) }} />
      {bars.map((b: any, i: number) => {
        const c = col(b.c || color); const grow = p(0.1 + i * 0.1, 0.22 + i * 0.1);
        const h = Math.max(2, b.v * SCALE * grow); const x = X0 + i * step;
        const hot = Math.floor(frame / 28) % n === i;
        return (
          <React.Fragment key={i}>
            <div style={{ position: "absolute", left: x, top: Y0 - h, width: bw, height: h, borderRadius: "12px 12px 0 0", background: `linear-gradient(180deg, ${c}, ${mix(c, T.bg1, 0.5)})`, border: `2px solid ${c}`, borderBottom: "none", boxShadow: hot ? `0 0 26px ${mix(T.bg0, c, 0.4)}` : "none" }} />
            <div style={{ position: "absolute", left: x - 20, top: Y0 - h - 44, width: bw + 40, textAlign: "center", fontFamily: MONO, fontWeight: 800, fontSize: 28, color: c, opacity: grow }}>{b.v}{unit}</div>
            <div style={{ position: "absolute", left: x - 20, top: Y0 + 14, width: bw + 40, textAlign: "center", fontFamily: SANS, fontSize: 22, color: T.muted, opacity: p(0.1 + i * 0.1, 0.2 + i * 0.1), lineHeight: 1.25 }}>{b.label}</div>
          </React.Fragment>
        );
      })}
      {note && <Foot theme={T} p={p(0.8, 0.92)}>{note}</Foot>}
    </Stage>
  );
};

// =================================================================== COMPARE (two columns)
const CompareScene: React.FC<any> = ({ dur, kicker = "", title = "", left = {}, right = {}, caption = "" }) => {
  const p = useP(dur);
  const colBlock = (d: any, x: number, at: number) => {
    const c = col(d.c);
    return (
      <div style={{ position: "absolute", left: x, top: 250, width: 780, opacity: p(at, at + 0.08) }}>
        <div style={{ display: "flex", alignItems: "center", gap: 12, marginBottom: 18 }}>
          {d.emoji && <span style={{ fontSize: 40 }}>{d.emoji}</span>}
          <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 34, color: c }}>{d.title}</div>
        </div>
        {(d.items || []).map((it: string, i: number) => (
          <div key={i} style={{ display: "flex", gap: 14, alignItems: "flex-start", background: mix(T.panel, c, 0.06), border: `1.5px solid ${T.line}`, borderLeft: `4px solid ${c}`, borderRadius: 12, padding: "15px 22px", marginBottom: 12, opacity: p(at + 0.04 + i * 0.05, at + 0.12 + i * 0.05) }}>
            <span style={{ color: c, fontFamily: MONO, fontWeight: 700, fontSize: 22 }}>{d.mark || "•"}</span>
            <span style={{ fontFamily: SANS, fontSize: 25, color: T.text, lineHeight: 1.35 }}>{it}</span>
          </div>
        ))}
      </div>
    );
  };
  return (
    <Stage>
      <Head theme={T} kicker={kicker} title={title} o={p(0, 0.06)} />
      {colBlock(left, 100, 0.1)}
      <div style={{ position: "absolute", left: 933, top: 300, bottom: 200, width: 3, background: `linear-gradient(180deg, transparent, ${T.line}, transparent)`, opacity: p(0.1, 0.2) }} />
      {colBlock(right, 1040, 0.26)}
      {caption && <Foot theme={T} p={p(0.8, 0.9)}>{caption}</Foot>}
    </Stage>
  );
};

// =================================================================== ORBIT (hub + satellites)
const OrbitScene: React.FC<any> = ({ dur, kicker = "", title = "", hub = {}, items = [], caption = "" }) => {
  const frame = useCurrentFrame(); const p = useP(dur); const hc = col(hub.c) || A.ai;
  return (
    <Stage>
      <Head theme={T} kicker={kicker} title={title} color={hc} o={p(0, 0.06)} />
      {items.map((it: any, i: number) => {
        const ang = (i / items.length) * Math.PI * 2 - Math.PI / 2 + Math.sin(frame * 0.008) * 0.05;
        const x = 960 + Math.cos(ang) * 600, y = 560 + Math.sin(ang) * 250;
        const c = col(it.c) || hc; const at = 0.14 + i * 0.08;
        const active = Math.floor(frame / 24) % items.length === i;
        return (
          <React.Fragment key={i}>
            <Wire x1={960} y1={560} x2={x} y2={y} p={p(at - 0.06, at)} color={active ? c : mix(T.muted, T.bg1, 0.4)} w={active ? 3 : 2} arrow={false} />
            {active && <Flow x1={960} y1={560} x2={x} y2={y} color={c} n={4} />}
            <div style={{ position: "absolute", left: x - 165, top: y - 46, width: 330, height: 92, borderRadius: 16, background: mix(T.panel, c, active ? 0.2 : 0.08), border: `2.5px solid ${active ? c : mix(T.line, c, 0.5)}`, display: "flex", alignItems: "center", gap: 14, padding: "0 20px", boxSizing: "border-box", opacity: p(at, at + 0.08), transform: `scale(${active ? 1.06 : 1})` }}>
              {it.emoji && <span style={{ fontSize: 38 }}>{it.emoji}</span>}
              <div>
                <div style={{ fontFamily: SANS, fontWeight: 700, fontSize: 25, color: T.text }}>{it.label}</div>
                {it.sub && <div style={{ fontFamily: MONO, fontSize: 17, color: T.muted, marginTop: 3 }}>{it.sub}</div>}
              </div>
            </div>
          </React.Fragment>
        );
      })}
      <div style={{ position: "absolute", left: 960 - 150, top: 560 - 90, width: 300, height: 180, borderRadius: 22, background: mix(T.panel, hc, 0.22), border: `3px solid ${hc}`, display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", opacity: p(0.06, 0.16), boxShadow: `0 0 50px ${mix(T.bg0, hc, 0.3 + Math.sin(frame * 0.06) * 0.08)}` }}>
        <span style={{ fontSize: 52 }}>{hub.emoji}</span>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 30, color: T.text, marginTop: 8, textAlign: "center", padding: "0 10px" }}>{hub.label}</div>
      </div>
      {caption && <Foot theme={T} p={p(0.82, 0.92)}>{caption}</Foot>}
    </Stage>
  );
};

// =================================================================== CODE panel (real code, line-by-line)
const CodeScene: React.FC<any> = ({ dur, kicker = "FROM SCRATCH", title = "", file = "strategy.py", lines = [], side = null, color = "money", caption = "" }) => {
  const frame = useCurrentFrame(); const p = useP(dur); const c = col(color);
  const n = lines.length;
  const panelW = side ? 1060 : 1720;
  return (
    <Stage>
      <Head theme={T} kicker={kicker} title={title} color={c} o={p(0, 0.06)} />
      <div style={{ position: "absolute", left: 100, top: 240, width: panelW, height: 620, borderRadius: 18, background: "#070B15", border: `2px solid ${mix(T.line, c, 0.5)}`, boxSizing: "border-box", overflow: "hidden", opacity: p(0.04, 0.12) }}>
        {/* title bar */}
        <div style={{ height: 46, background: mix(T.panel, c, 0.14), borderBottom: `1.5px solid ${T.line}`, display: "flex", alignItems: "center", gap: 10, padding: "0 20px" }}>
          <span style={{ width: 12, height: 12, borderRadius: 12, background: A.risk }} />
          <span style={{ width: 12, height: 12, borderRadius: 12, background: A.edge }} />
          <span style={{ width: 12, height: 12, borderRadius: 12, background: A.money }} />
          <span style={{ fontFamily: MONO, fontSize: 19, color: T.muted, marginLeft: 12 }}>{file}</span>
        </div>
        <div style={{ padding: "20px 26px" }}>
          {lines.map((ln: any, i: number) => {
            const txt = typeof ln === "string" ? ln : ln.t;
            const isComment = txt.trimStart().startsWith("#");
            const lc = isComment ? T.muted : (typeof ln === "object" && ln.c ? col(ln.c) : T.text);
            const at = 0.08 + (i / n) * 0.6; const o = p(at, at + 0.05);
            const typing = p(at, at + 0.05) > 0 && p(at, at + 0.05) < 1;
            const indent = (txt.match(/^\s*/)?.[0].length || 0);
            return (
              <div key={i} style={{ display: "flex", gap: 16, opacity: o, minHeight: 30 }}>
                <span style={{ fontFamily: MONO, fontSize: 18, color: mix(T.muted, T.bg1, 0.4), width: 22, textAlign: "right", userSelect: "none" }}>{i + 1}</span>
                <span style={{ fontFamily: MONO, fontSize: 21, color: lc, whiteSpace: "pre", fontWeight: isComment ? 400 : 600, lineHeight: 1.5 }}>
                  {" ".repeat(indent)}{txt.trimStart()}{typing && Math.floor(frame / 8) % 2 === 0 ? "▌" : ""}
                </span>
              </div>
            );
          })}
        </div>
      </div>
      {side && (
        <div style={{ position: "absolute", left: 1200, top: 240, width: 620, opacity: p(0.4, 0.5) }}>
          <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 30, color: c }}>{side.title}</div>
          {(side.points || []).map((pt: string, i: number) => (
            <div key={i} style={{ display: "flex", gap: 12, marginTop: 18, opacity: p(0.45 + i * 0.08, 0.55 + i * 0.08) }}>
              <span style={{ color: c, fontFamily: MONO, fontWeight: 700, fontSize: 21 }}>▸</span>
              <span style={{ fontFamily: SANS, fontSize: 24, color: T.text, lineHeight: 1.4 }}>{pt}</span>
            </div>
          ))}
        </div>
      )}
      {caption && <Foot theme={T} p={p(0.82, 0.92)}>{caption}</Foot>}
    </Stage>
  );
};

// =================================================================== CHECKLIST / red-flags / steps
const ListScene: React.FC<any> = ({ dur, kicker = "", title = "", color = "data", items = [], tone = "neutral", caption = "", numbered = true }) => {
  const frame = useCurrentFrame(); const p = useP(dur);
  const c = tone === "bad" ? A.risk : tone === "ok" ? A.money : col(color);
  const mark = tone === "bad" ? "✕" : tone === "ok" ? "✓" : null;
  return (
    <Stage>
      <Head theme={T} kicker={kicker} title={title} color={c} o={p(0, 0.06)} />
      <div style={{ position: "absolute", left: 150, top: 240, width: 1620 }}>
        {items.map((it: any, i: number) => {
          const at = 0.06 + i * 0.1; const o = p(at, at + 0.07);
          const head = typeof it === "string" ? it : it.h; const sub = typeof it === "object" ? it.sub : null;
          const ic = typeof it === "object" && it.c ? col(it.c) : c;
          return (
            <div key={i} style={{ display: "flex", alignItems: "flex-start", gap: 20, opacity: o, transform: `translateX(${(1 - o) * -24}px)`, background: mix(T.panel, ic, 0.06), border: `1.5px solid ${T.line}`, borderLeft: `5px solid ${ic}`, borderRadius: 14, padding: "16px 26px", marginBottom: 13 }}>
              <span style={{ color: ic, fontFamily: MONO, fontWeight: 800, fontSize: 26, minWidth: 34, textAlign: "center", marginTop: 2 }}>{mark || (numbered ? i + 1 : "•")}</span>
              <div>
                <span style={{ fontFamily: SANS, fontWeight: sub ? 800 : 600, fontSize: 28, color: T.text, lineHeight: 1.3 }}>{head}</span>
                {sub && <div style={{ fontFamily: SANS, fontSize: 23, color: T.muted, marginTop: 6, lineHeight: 1.35 }}>{sub}</div>}
              </div>
            </div>
          );
        })}
      </div>
      {caption && <Foot theme={T} p={p(0.82, 0.92)}>{caption}</Foot>}
    </Stage>
  );
};

// =================================================================== GAUGE / tower (cost drag, risk)
const GaugeScene: React.FC<any> = ({ dur, kicker = "", title = "", color = "risk", segs = [], counter = null, caption = "", limitLabel = "" }) => {
  const frame = useCurrentFrame(); const p = useP(dur); const c = col(color);
  // segs: [{ label, h, c }] stacked bottom-up; total height budget 560
  const totalH = 560; const towerX = 160, towerY = 250, towerW = 420;
  let acc = 0;
  return (
    <Stage>
      <Head theme={T} kicker={kicker} title={title} color={c} o={p(0, 0.06)} />
      <div style={{ position: "absolute", left: towerX, top: towerY, width: towerW, height: totalH, border: `2.5px solid ${T.line}`, borderRadius: 18, background: T.panel, overflow: "hidden", display: "flex", flexDirection: "column-reverse" }}>
        {segs.map((s: any, i: number) => {
          const sc = col(s.c); const at = 0.12 + i * 0.13;
          return (
            <div key={i} style={{ height: s.h * p(at, at + 0.1), background: `linear-gradient(90deg, ${mix(T.panel, sc, 0.7)}, ${mix(T.panel, sc, 0.4)})`, borderTop: `2px solid ${sc}`, display: "flex", alignItems: "center", paddingLeft: 20, boxSizing: "border-box" }}>
              <span style={{ fontFamily: MONO, fontSize: 20, color: T.text, whiteSpace: "nowrap", opacity: p(at + 0.04, at + 0.12) }}>{s.label}</span>
            </div>
          );
        })}
      </div>
      {/* right-side explanation + counter */}
      <div style={{ position: "absolute", left: 720, top: 300, width: 1100 }}>
        {counter && (
          <div style={{ opacity: p(0.4, 0.52) }}>
            <Counter p={p(0.5, 0.74)} to={counter.value} prefix={counter.prefix || ""} suffix={counter.suffix || ""} color={c} size={88} decimals={counter.decimals || 0} comma={counter.comma} />
            <div style={{ fontFamily: SANS, fontWeight: 700, fontSize: 28, color: T.text, marginTop: 10 }}>{counter.label}</div>
          </div>
        )}
        {(segs || []).map((s: any, i: number) => {
          const sc = col(s.c); const at = 0.14 + i * 0.13;
          return s.note ? (
            <div key={i} style={{ display: "flex", gap: 12, marginTop: 20, opacity: p(at + 0.05, at + 0.13) }}>
              <span style={{ width: 16, height: 16, borderRadius: 4, background: sc, marginTop: 6 }} />
              <span style={{ fontFamily: SANS, fontSize: 24, color: T.text, lineHeight: 1.4 }}>{s.note}</span>
            </div>
          ) : null;
        })}
      </div>
      {caption && <Foot theme={T} p={p(0.83, 0.93)}>{caption}</Foot>}
    </Stage>
  );
};

// =================================================================== TIERS (stacked platform tiers)
const TiersScene: React.FC<any> = ({ dur, kicker = "WHERE YOU CAN DO IT", title = "", tiers = [], caption = "" }) => {
  const frame = useCurrentFrame(); const p = useP(dur);
  const n = tiers.length; const rowH = 168; const gap = 22; const y0 = 240;
  return (
    <Stage>
      <Head theme={T} kicker={kicker} title={title} color={A.money} o={p(0, 0.06)} />
      {tiers.map((tr: any, i: number) => {
        const c = col(tr.c); const y = y0 + i * (rowH + gap); const at = 0.1 + i * 0.16;
        const o = p(at, at + 0.09);
        return (
          <div key={i} style={{ position: "absolute", left: 100, top: y, width: 1720, height: rowH, borderRadius: 18, background: mix(T.panel, c, 0.09), border: `2.5px solid ${c}`, boxSizing: "border-box", padding: "18px 28px", display: "flex", alignItems: "center", gap: 28, opacity: o, transform: `translateX(${(1 - o) * -24}px)` }}>
            <div style={{ minWidth: 120, textAlign: "center" }}>
              <div style={{ fontFamily: MONO, fontWeight: 800, fontSize: 44, color: c }}>{tr.level}</div>
              <div style={{ fontFamily: MONO, fontSize: 16, color: T.muted, marginTop: 4 }}>{tr.effort}</div>
            </div>
            <div style={{ width: 2, height: rowH - 44, background: T.line }} />
            <div style={{ flex: 1 }}>
              <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 30, color: T.text }}>{tr.name}</div>
              <div style={{ fontFamily: SANS, fontSize: 22, color: T.muted, marginTop: 6, lineHeight: 1.32 }}>{tr.desc}</div>
            </div>
            <div style={{ display: "flex", flexDirection: "column", gap: 8, alignItems: "flex-end" }}>
              {(tr.tools || []).map((tl: string, j: number) => {
                const hot = Math.floor(frame / 22) % Math.max(1, (tr.tools || []).length) === j;
                return <span key={j} style={{ fontFamily: MONO, fontWeight: 700, fontSize: 19, color: hot ? T.bg0 : c, background: hot ? c : mix(T.panel, c, 0.12), border: `1.5px solid ${c}`, borderRadius: 8, padding: "6px 14px" }}>{tl}</span>;
              })}
            </div>
          </div>
        );
      })}
      {caption && <Foot theme={T} p={p(0.84, 0.93)}>{caption}</Foot>}
    </Stage>
  );
};

// =================================================================== BUILD LOOP (numbered process ring/flow)
const LoopScene: React.FC<any> = ({ dur, kicker = "THE BUILD LOOP", title = "", steps = [], caption = "" }) => {
  const frame = useCurrentFrame(); const p = useP(dur);
  const n = steps.length;
  const cx = 960, cy = 560, rx = 640, ry = 300;
  const active = Math.floor(frame / 30) % n;
  return (
    <Stage>
      <Head theme={T} kicker={kicker} title={title} color={A.edge} o={p(0, 0.06)} />
      {/* connecting ellipse hint */}
      {steps.map((_: any, i: number) => {
        const a1 = (i / n) * Math.PI * 2 - Math.PI / 2;
        const a2 = ((i + 1) / n) * Math.PI * 2 - Math.PI / 2;
        const x1 = cx + Math.cos(a1) * rx, y1 = cy + Math.sin(a1) * ry;
        const x2 = cx + Math.cos(a2) * rx, y2 = cy + Math.sin(a2) * ry;
        return <Wire key={i} x1={x1} y1={y1} x2={x2} y2={y2} p={p(0.1 + i * 0.05, 0.2 + i * 0.05)} color={mix(T.line, A.edge, 0.6)} w={2} arrow />;
      })}
      {steps.map((s: any, i: number) => {
        const a = (i / n) * Math.PI * 2 - Math.PI / 2;
        const x = cx + Math.cos(a) * rx, y = cy + Math.sin(a) * ry;
        const c = col(s.c) || A.edge; const at = 0.1 + i * 0.09; const hot = active === i;
        return (
          <div key={i} style={{ position: "absolute", left: x - 150, top: y - 66, width: 300, height: 132, borderRadius: 16, background: mix(T.panel, c, hot ? 0.2 : 0.09), border: `2.5px solid ${c}`, boxSizing: "border-box", padding: "14px 18px", opacity: p(at, at + 0.08), transform: `scale(${hot ? 1.06 : 1})`, boxShadow: hot ? `0 0 30px ${mix(T.bg0, c, 0.34)}` : "none" }}>
            <div style={{ fontFamily: MONO, fontWeight: 800, fontSize: 20, color: c }}>{"0" + (i + 1)}</div>
            <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 26, color: T.text, marginTop: 4 }}>{s.label}</div>
            <div style={{ fontFamily: SANS, fontSize: 18, color: T.muted, marginTop: 4, lineHeight: 1.28 }}>{s.sub}</div>
          </div>
        );
      })}
      {/* center label */}
      <div style={{ position: "absolute", left: cx - 170, top: cy - 40, width: 340, textAlign: "center", opacity: p(0.3, 0.42) }}>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontStyle: "italic", fontSize: 30, color: A.edge, textShadow: `0 0 24px ${mix(T.bg0, A.edge, 0.6)}` }}>iterate, don't gamble</div>
      </div>
      {caption && <Foot theme={T} p={p(0.84, 0.93)}>{caption}</Foot>}
    </Stage>
  );
};

// =================================================================== CALLOUT (one principle, big)
const CalloutScene: React.FC<any> = ({ dur, kicker = "THE KEY IDEA", color = "edge", text = "", sub = "" }) => {
  const frame = useCurrentFrame(); const p = useP(dur); const pop = usePop(dur); const c = col(color);
  return (
    <AbsoluteFill style={{ alignItems: "center", justifyContent: "center", padding: "0 200px" }}>
      <div style={{ textAlign: "center", transform: `scale(${0.95 + pop(0.05) * 0.05})` }}>
        <div style={{ display: "flex", justifyContent: "center", marginBottom: 30 }}><Kicker theme={T} text={kicker} color={c} cx /></div>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 66, lineHeight: 1.18, letterSpacing: -1.5, color: T.text, opacity: p(0.06, 0.2) }}>
          "{text}"
        </div>
        <div style={{ height: 4, width: interpolate(p(0.3, 0.6), [0, 1], [0, 320]), background: c, borderRadius: 3, margin: "34px auto", boxShadow: `0 0 20px ${c}` }} />
        {sub && <div style={{ fontFamily: SANS, fontSize: 32, color: c, opacity: p(0.5, 0.66), textShadow: `0 0 ${20 + Math.sin(frame * 0.06) * 10}px ${mix(T.bg0, c, 0.6)}` }}>{sub}</div>}
      </div>
    </AbsoluteFill>
  );
};

// =================================================================== RECAP
const RecapScene: React.FC<any> = ({ dur, kicker = "RECAP — THE WHOLE MAP", title = "AI trading in one breath", items = [], closer = "" }) => {
  const frame = useCurrentFrame(); const p = useP(dur);
  return (
    <AbsoluteFill style={{ padding: "56px 130px", justifyContent: "center" }}>
      <div style={{ opacity: p(0, 0.06), textAlign: "center", marginBottom: 26 }}>
        <Kicker theme={T} text={kicker} cx />
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 60, color: T.text, marginTop: 12, letterSpacing: -1.5 }}>{title}</div>
      </div>
      <div style={{ display: "flex", flexDirection: "column", gap: 11, maxWidth: 1400, margin: "0 auto", width: "100%" }}>
        {items.map((it: string, i: number) => {
          const at = 0.05 + i * 0.08; const o = p(at, at + 0.06);
          const c = [A.data, A.ai, A.money, A.risk, A.edge][i % 5];
          return (
            <div key={i} style={{ display: "flex", alignItems: "center", gap: 18, opacity: o, transform: `translateX(${(1 - o) * -24}px)`, background: mix(T.panel, c, 0.05), border: `1.5px solid ${T.line}`, borderLeft: `4px solid ${c}`, borderRadius: 12, padding: "13px 26px" }}>
              <span style={{ color: c, fontFamily: MONO, fontWeight: 700, fontSize: 24 }}>{i + 1}</span>
              <span style={{ fontFamily: SANS, fontSize: 28, color: T.text, lineHeight: 1.25 }}>{it}</span>
            </div>
          );
        })}
      </div>
      <div style={{ textAlign: "center", marginTop: 30, opacity: p(0.8, 0.9) }}>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontStyle: "italic", fontSize: 40, color: A.data, textShadow: `0 0 ${28 + Math.sin(frame * 0.06) * 14}px ${mix(T.bg0, A.data, 0.7)}` }}>{closer}</div>
      </div>
    </AbsoluteFill>
  );
};

// =================================================================== router
const ROUTES: Record<string, { C: React.FC<any>; accent: string }> = {
  ait_title: { C: TitleScene, accent: A.data },
  ait_divider: { C: DividerScene, accent: A.data },
  ait_hook: { C: HookScene, accent: A.edge },
  ait_pipeline: { C: PipelineScene, accent: A.data },
  ait_cards: { C: CardsScene, accent: A.data },
  ait_spectrum: { C: SpectrumScene, accent: A.ai },
  ait_stat: { C: StatScene, accent: A.risk },
  ait_bars: { C: BarsScene, accent: A.data },
  ait_compare: { C: CompareScene, accent: A.ai },
  ait_orbit: { C: OrbitScene, accent: A.ai },
  ait_code: { C: CodeScene, accent: A.money },
  ait_list: { C: ListScene, accent: A.data },
  ait_gauge: { C: GaugeScene, accent: A.risk },
  ait_tiers: { C: TiersScene, accent: A.money },
  ait_loop: { C: LoopScene, accent: A.edge },
  ait_callout: { C: CalloutScene, accent: A.edge },
  ait_recap: { C: RecapScene, accent: A.data },
};

export const AITScene: React.FC<{ variant: string;[key: string]: unknown }> = ({ variant, ...rest }) => {
  const route = ROUTES[variant] || ROUTES.ait_title;
  const { C } = route;
  // accent for Bg tint: prefer an explicit `color` prop when the scene set one
  const accent = col((rest as any).color) || route.accent;
  const isFull = variant === "ait_title" || variant === "ait_recap" || variant === "ait_callout";
  return (
    <AbsoluteFill>
      <Bg theme={T} accent={accent} />
      <Stage><CandleTape o={isFull ? 0.34 : 0.5} /></Stage>
      <C variant={variant} {...(rest as any)} />
      <Stage><SceneProgress dur={(rest as any).dur} color={accent} /></Stage>
    </AbsoluteFill>
  );
};

export default AITScene;
