/**
 * EQScenes.tsx — English computed scenes for the Equities/F&O/Commodities course (prefix `eq`).
 * Only the F&O money-scenes that need computed geometry AND English labels live here
 * (payoff diagram, leverage, time-decay). Everything else in the course reuses the
 * parameterized `sm` scenes with English props. Same visual identity as SMScenes.
 */
import React from "react";
import { AbsoluteFill, useCurrentFrame } from "remotion";
import { makeTheme, mix, useP, MONO, SANS, Bg, Stage, Head } from "../lib/primitives";

const T = makeTheme({ accent: "#34D399" });
const A = { up: "#34D399", down: "#FB7185", mkt: "#22D3EE", money: "#FBBF24", deriv: "#A78BFA" };

// eq_payoff — single-leg option payoff (call/put, buy/sell), English labels ---------
const PayoffScene: React.FC<{
  dur?: number; kind?: "call" | "put"; side?: "buy" | "sell"; strike?: number; premium?: number;
  kicker?: string; title?: string; note?: string; cur?: string;
}> = ({ dur, kind = "call", side = "buy", strike = 100, premium = 5, kicker = "OPTIONS", title = "", note = "", cur = "$" }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const X0 = 360, Y0 = 280, W = 1200, H = 480;
  const yMid = Y0 + H / 2;
  const sMin = strike - 30, sMax = strike + 30;
  const payoff = (s: number) => {
    const intrinsic = kind === "call" ? Math.max(0, s - strike) : Math.max(0, strike - s);
    const buyPL = intrinsic - premium;
    return side === "buy" ? buyPL : -buyPL;
  };
  const maxAbs = 26;
  const pts = Array.from({ length: 100 }).map((_, i) => {
    const s = sMin + (i / 99) * (sMax - sMin);
    const v = Math.max(-maxAbs, Math.min(maxAbs, payoff(s)));
    return { x: X0 + (i / 99) * W, y: yMid - (v / maxAbs) * (H / 2 - 20), v };
  });
  const drawN = Math.max(2, Math.round(100 * p(0.3, 0.62)));
  const be = kind === "call" ? strike + premium : strike - premium;
  const beX = X0 + ((be - sMin) / (sMax - sMin)) * W;
  const strikeX = X0 + ((strike - sMin) / (sMax - sMin)) * W;
  const role = `${side === "buy" ? "Long" : "Short"} ${kind === "call" ? "Call" : "Put"}`;
  return (
    <Stage>
      <Head theme={T} kicker={kicker} title={title || `${role} — payoff at expiry`} color={A.deriv} o={p(0, 0.06)} />
      <svg width={1920} height={1080} style={{ position: "absolute", left: 0, top: 0, overflow: "visible" }}>
        <rect x={X0} y={Y0} width={W} height={H / 2} fill={mix(T.bg1, A.up, 0.05)} opacity={p(0.06, 0.12)} />
        <rect x={X0} y={yMid} width={W} height={H / 2} fill={mix(T.bg1, A.down, 0.05)} opacity={p(0.06, 0.12)} />
        <line x1={X0} y1={yMid} x2={X0 + W} y2={yMid} stroke={T.muted} strokeWidth={2} opacity={p(0.08, 0.14)} />
        <line x1={strikeX} y1={Y0} x2={strikeX} y2={Y0 + H} stroke={A.money} strokeWidth={2} strokeDasharray="8 8" opacity={p(0.2, 0.28)} />
        {pts.slice(0, drawN - 1).map((pt, i) => {
          const nx = pts[i + 1];
          return <line key={i} x1={pt.x} y1={pt.y} x2={nx.x} y2={nx.y} stroke={pt.v >= 0 ? A.up : A.down} strokeWidth={6} strokeLinecap="round" />;
        })}
        {p(0.64, 0.66) > 0.5 && <circle cx={beX} cy={yMid} r={10 + Math.sin(frame * 0.12) * 3} fill={A.mkt} opacity={0.9} />}
      </svg>
      <div style={{ position: "absolute", left: X0 - 250, top: Y0 + 30, fontFamily: SANS, fontWeight: 700, fontSize: 26, color: A.up, opacity: p(0.08, 0.16) }}>PROFIT ↑</div>
      <div style={{ position: "absolute", left: X0 - 250, top: Y0 + H - 70, fontFamily: SANS, fontWeight: 700, fontSize: 26, color: A.down, opacity: p(0.08, 0.16) }}>LOSS ↓</div>
      <div style={{ position: "absolute", left: strikeX - 120, top: Y0 + H + 14, width: 240, textAlign: "center", fontFamily: MONO, fontSize: 23, color: A.money, opacity: p(0.22, 0.3) }}>Strike {cur}{strike}</div>
      <div style={{ position: "absolute", left: beX - 150, top: yMid - 56, width: 300, textAlign: "center", fontFamily: SANS, fontWeight: 700, fontSize: 24, color: A.mkt, opacity: p(0.66, 0.74) }}>Break-even {cur}{be}</div>
      <div style={{ position: "absolute", left: X0 + W - 300, top: Y0 + H + 14, fontFamily: MONO, fontSize: 23, color: T.muted, opacity: p(0.1, 0.18) }}>Underlying price at expiry →</div>
      {note && (
        <div style={{ position: "absolute", left: 150, top: 850, width: 1620, textAlign: "center", opacity: p(0.76, 0.88) }}>
          <span style={{ fontFamily: SANS, fontWeight: 700, fontSize: 30, color: T.text, lineHeight: 1.4 }}>{note}</span>
        </div>
      )}
    </Stage>
  );
};

// eq_leverage — margin vs exposure, two outcomes, English ----------------------------
const LeverageScene: React.FC<{
  dur?: number; kicker?: string; title?: string; margin?: number; exposure?: number; movePct?: number; cur?: string;
}> = ({ dur, kicker = "LEVERAGE", title = "Leverage — a double-edged sword", margin = 150000, exposure = 1500000, movePct = 5, cur = "₹" }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const lev = exposure / margin;
  const pl = exposure * (movePct / 100);
  const plPctOnMargin = (pl / margin) * 100;
  const fmt = (v: number) => (v >= 100000 ? `${cur}${(v / 100000).toFixed(v % 100000 === 0 ? 0 : 1)}L` : `${cur}${Math.round(v / 1000)}k`);
  return (
    <Stage>
      <Head theme={T} kicker={kicker} title={title} color={A.deriv} o={p(0, 0.06)} />
      <div style={{ position: "absolute", left: 170, top: 270, width: 640 }}>
        <div style={{ opacity: p(0.08, 0.16) }}>
          <div style={{ fontFamily: SANS, fontWeight: 700, fontSize: 27, color: A.money, marginBottom: 8 }}>Your margin (you pay): {fmt(margin)}</div>
          <div style={{ width: 640 * (margin / exposure) + 60, height: 52, borderRadius: 10, background: `linear-gradient(90deg, ${mix(A.money, T.bg1, 0.3)}, ${A.money})` }} />
        </div>
        <div style={{ marginTop: 36, opacity: p(0.2, 0.3) }}>
          <div style={{ fontFamily: SANS, fontWeight: 700, fontSize: 27, color: A.deriv, marginBottom: 8 }}>Position you control: {fmt(exposure)}</div>
          <div style={{ width: 640 * p(0.22, 0.36), height: 52, borderRadius: 10, background: `linear-gradient(90deg, ${mix(A.deriv, T.bg1, 0.3)}, ${A.deriv})`,
            boxShadow: `0 0 ${18 + Math.sin(frame * 0.08) * 8}px ${mix(T.bg0, A.deriv, 0.35)}` }} />
        </div>
        <div style={{ marginTop: 30, fontFamily: MONO, fontWeight: 800, fontSize: 40, color: A.deriv, opacity: p(0.34, 0.42) }}>= {lev.toFixed(0)}x leverage</div>
      </div>
      {[
        { at: 0.48, c: A.up, dir: "▲", t: `Market +${movePct}%`, v: `+${fmt(pl)}`, s: `+${plPctOnMargin.toFixed(0)}% on your margin` },
        { at: 0.62, c: A.down, dir: "▼", t: `Market −${movePct}%`, v: `−${fmt(pl)}`, s: `half your margin gone!` },
      ].map((r, i) => (
        <div key={i} style={{ position: "absolute", left: 940, top: i === 0 ? 280 : 590, width: 810, height: 280,
          borderRadius: 20, boxSizing: "border-box", padding: "26px 34px",
          background: mix(T.panel, r.c, p(r.at, r.at + 0.08) > 0.5 ? 0.1 : 0.02),
          border: `2.5px solid ${p(r.at, r.at + 0.08) > 0.5 ? r.c : T.bg2}`,
          opacity: Math.max(p(0.04, 0.08) * 0.22, p(r.at, r.at + 0.08)),
          boxShadow: i === 1 && p(r.at + 0.08, r.at + 0.1) > 0.5 ? `0 0 ${30 + Math.sin(frame * 0.1) * 14}px ${mix(T.bg0, A.down, 0.35)}` : "none" }}>
          <div style={{ fontFamily: SANS, fontWeight: 700, fontSize: 30, color: r.c }}>{r.dir} {r.t}</div>
          <div style={{ fontFamily: MONO, fontWeight: 800, fontSize: 64, color: r.c, marginTop: 14 }}>{r.v}</div>
          <div style={{ fontFamily: SANS, fontSize: 26, color: T.text, marginTop: 10, lineHeight: 1.35 }}>{r.s}</div>
        </div>
      ))}
    </Stage>
  );
};

// eq_theta — option time decay, English ---------------------------------------------
const ThetaScene: React.FC<{ dur?: number; kicker?: string; title?: string; note?: string }> = ({
  dur, kicker = "OPTIONS · TIME DECAY", title = "Theta — the melting ice cube", note = "",
}) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const X0 = 260, Y0 = 280, W = 1300, H = 440;
  const pts = Array.from({ length: 90 }).map((_, i) => {
    const t = i / 89;
    const v = Math.sqrt(Math.max(0.0001, 1 - t));
    return `${X0 + t * W},${Y0 + H - v * (H - 30)}`;
  });
  const drawP = p(0.18, 0.55);
  const melt = 1 - p(0.6, 0.85) * 0.75;
  return (
    <Stage>
      <Head theme={T} kicker={kicker} title={title} color={A.down} o={p(0, 0.06)} />
      <svg width={1920} height={1080} style={{ position: "absolute", left: 0, top: 0, overflow: "visible" }}>
        <line x1={X0} y1={Y0 + H} x2={X0 + W} y2={Y0 + H} stroke={T.bg2} strokeWidth={2} />
        <line x1={X0} y1={Y0} x2={X0} y2={Y0 + H} stroke={T.bg2} strokeWidth={2} />
        <polyline points={pts.slice(0, Math.max(2, Math.round(90 * drawP))).join(" ")} fill="none" stroke={A.deriv} strokeWidth={5} opacity={p(0.14, 0.22)} />
      </svg>
      <div style={{ position: "absolute", left: X0, top: 230, fontFamily: MONO, fontSize: 23, color: T.muted, opacity: p(0.08, 0.16) }}>Time value in the premium</div>
      <div style={{ position: "absolute", left: X0 + W - 130, top: Y0 + H + 16, fontFamily: MONO, fontSize: 23, color: A.down, opacity: p(0.2, 0.28) }}>Expiry</div>
      <div style={{ position: "absolute", left: 1600, top: 320, textAlign: "center" }}>
        <div style={{ fontSize: 150 * melt, opacity: p(0.56, 0.64), transform: `translateY(${(1 - melt) * 60}px)` }}>🧊</div>
        <div style={{ fontFamily: SANS, fontWeight: 700, fontSize: 25, color: A.mkt, marginTop: 14, opacity: p(0.6, 0.68), width: 240, marginLeft: -60, lineHeight: 1.35 }}>
          A little value evaporates daily
        </div>
      </div>
      <div style={{ position: "absolute", left: 150, top: 810, width: 1620, textAlign: "center", opacity: p(0.72, 0.84) }}>
        <span style={{ fontFamily: SANS, fontWeight: 700, fontSize: 31, color: T.text, lineHeight: 1.4 }}>
          {note || <>Even if the stock doesn't move, the buyer's premium <span style={{ color: A.down, textShadow: `0 0 ${14 + Math.sin(frame * 0.09) * 8}px ${mix(T.bg0, A.down, 0.6)}` }}>decays every day</span> — time is on the seller's side.</>}
        </span>
      </div>
    </Stage>
  );
};

// ---------------------------------------------------------------- dispatcher
export const EQScene: React.FC<{ variant: string;[key: string]: unknown }> = ({ variant, ...rest }) => {
  let content: React.ReactNode = null;
  let accent = A.deriv;
  switch (variant) {
    case "eq_payoff": content = <PayoffScene {...(rest as any)} />; break;
    case "eq_leverage": content = <LeverageScene {...(rest as any)} />; break;
    case "eq_theta": content = <ThetaScene {...(rest as any)} />; accent = A.down; break;
    default:
      content = (
        <AbsoluteFill style={{ alignItems: "center", justifyContent: "center" }}>
          <div style={{ color: "#f88", fontFamily: MONO, fontSize: 40 }}>unknown eq variant “{variant}”</div>
        </AbsoluteFill>
      );
  }
  return (
    <AbsoluteFill>
      <Bg theme={T} accent={accent} />
      {content}
    </AbsoluteFill>
  );
};
