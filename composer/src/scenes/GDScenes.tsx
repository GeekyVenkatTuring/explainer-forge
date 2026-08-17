/**
 * GDScenes.tsx — "How Gradient Descent Works" explainer (5 beats)
 *
 * Visual identity:
 *   Theme : default dark bg (makeTheme)
 *   Accents (semantic):
 *     main  #F97316  amber-orange  → loss / gradient / heat
 *     cool  #60A5FA  blue          → weight position (w)
 *     ok    #34D399  green         → convergence / good LR
 *     bad   #F43F5E  rose          → divergence / bad LR
 *   Motif : parabola loss curve + descending dot — appears in every scene.
 *
 * Rules followed:
 *   • Every scene phases via useP(dur) fractions — no fixed frame numbers.
 *   • Continuous motion every frame: sin-breathing glows, ScanBeam, Flow.
 *   • Real GD steps precomputed at module scope (deterministic).
 *   • No Math.random() — only rnd(i,j,s); no CSS filter/backdrop-filter.
 */
import React from "react";
import { AbsoluteFill, interpolate, useCurrentFrame } from "remotion";
import {
  makeTheme, mix, useP, usePop, rnd, MONO, SANS,
  Bg, Stage, Kicker, Head, Foot, Card, Flow, ScanBeam,
} from "../lib/primitives";

// ── Identity ────────────────────────────────────────────────────────────────
const T = makeTheme({ accent: "#F97316" });
const A = { main: "#F97316", cool: "#60A5FA", ok: "#34D399", bad: "#F43F5E" };

// ── Precomputed GD runs (module scope — deterministic, one-time) ─────────────
const LR_GOOD = 0.18;
const W0 = -2.2;
const LOSS_FN = (w: number) => (w - 3) * (w - 3);
const GRAD_FN = (w: number) => 2 * (w - 3);

function runGD(lr: number, steps: number, w0 = W0): number[] {
  const ws: number[] = [w0];
  let w = w0;
  for (let i = 0; i < steps; i++) {
    w = w - lr * GRAD_FN(w);
    ws.push(w);
  }
  return ws;
}

const STEPS_GOOD = runGD(LR_GOOD, 18);   // gd_step hero + "just right" column
const STEPS_SLOW = runGD(0.02, 18);       // crawls
const STEPS_FAST = runGD(0.95, 18);       // heavy oscillation

// ── Chart coordinate helpers ─────────────────────────────────────────────────
const W_MIN = -3.5, W_MAX = 8.5;
const L_MAX = 42;

function wx(w: number, x0: number, x1: number) {
  return x0 + ((w - W_MIN) / (W_MAX - W_MIN)) * (x1 - x0);
}
function ly(loss: number, y0: number, y1: number) {
  // y0 = chart top (small y), y1 = baseline (large y)
  return y1 - (Math.min(loss, L_MAX) / L_MAX) * (y1 - y0);
}

// 80-sample parabola SVG point string for given chart bounds
function parabola(x0: number, y0: number, x1: number, y1: number, n = 80): string {
  return Array.from({ length: n })
    .map((_, i) => {
      const w = W_MIN + (i / (n - 1)) * (W_MAX - W_MIN);
      return `${wx(w, x0, x1).toFixed(1)},${ly(LOSS_FN(w), y0, y1).toFixed(1)}`;
    })
    .join(" ");
}

// ── gd_title ─────────────────────────────────────────────────────────────────
const TitleScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const pop = usePop(dur);

  // Ambient parabola behind title (always visible)
  const allPts = parabola(240, 240, 1680, 900);

  // Descending dot along the parabola — continuous motion
  const tDot = ((frame * 0.007) % 1);
  const dotW = W_MIN + tDot * (W_MAX - W_MIN);
  const dotX = wx(dotW, 240, 1680);
  const dotY = ly(LOSS_FN(dotW), 240, 900);

  // Orbiting accent dots for ambient motion (deterministic positions)
  const orbits = Array.from({ length: 8 }).map((_, i) => {
    const ang = frame * 0.009 + (i / 8) * Math.PI * 2;
    return {
      x: 960 + Math.cos(ang) * (500 + rnd(i, 0) * 120) - 6,
      y: 540 + Math.sin(ang) * (210 + rnd(i, 1) * 70) - 6,
      o: 0.18 + rnd(i, 2) * 0.22,
    };
  });

  return (
    <Stage>
      {/* Ambient parabola motif */}
      <svg style={{ position: "absolute", left: 0, top: 0 }} width={1920} height={1080}>
        <polyline
          points={allPts}
          fill="none"
          stroke={mix(T.bg2, A.main, 0.32)}
          strokeWidth={3}
          opacity={p(0.03, 0.18)}
        />
      </svg>

      {/* Descending dot */}
      <div style={{
        position: "absolute",
        left: dotX - 10, top: dotY - 10,
        width: 20, height: 20, borderRadius: 20,
        background: A.main,
        boxShadow: `0 0 22px ${A.main}`,
        opacity: p(0.08, 0.28) * (0.5 + Math.sin(frame * 0.09) * 0.3),
      }} />

      {/* Orbiting dots */}
      {orbits.map((d, i) => (
        <div key={i} style={{
          position: "absolute", left: d.x, top: d.y,
          width: 12, height: 12, borderRadius: 12,
          background: A.cool, opacity: d.o * p(0.04, 0.2),
          boxShadow: `0 0 10px ${A.cool}`,
        }} />
      ))}

      {/* Title block */}
      <div style={{
        position: "absolute", left: 0, right: 0, top: 268,
        textAlign: "center",
        transform: `scale(${0.92 + pop(0) * 0.08})`,
      }}>
        <div style={{ display: "flex", justifyContent: "center", marginBottom: 30, opacity: p(0.02, 0.14) }}>
          <Kicker theme={T} text="MACHINE LEARNING · FUNDAMENTALS" cx />
        </div>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 116, lineHeight: 1.0, letterSpacing: -3, color: T.text, opacity: p(0.06, 0.20) }}>
          Gradient
        </div>
        <div style={{
          fontFamily: SANS, fontWeight: 800, fontSize: 116, lineHeight: 1.05, letterSpacing: -3,
          color: A.main,
          textShadow: `0 0 80px ${mix(T.bg0, A.main, 0.65)}`,
          opacity: p(0.10, 0.24),
        }}>
          Descent
        </div>
        {/* Underline draw — phased */}
        <div style={{
          height: 5, margin: "30px auto",
          width: interpolate(p(0.22, 0.50), [0, 1], [0, 510]),
          background: `linear-gradient(90deg, ${A.main}, ${A.cool})`,
          borderRadius: 3,
        }} />
        <div style={{ fontFamily: SANS, fontSize: 36, color: T.muted, opacity: p(0.34, 0.54) }}>
          how models learn to reduce their mistakes
        </div>
      </div>

      {/* Update rule chip */}
      <div style={{
        position: "absolute", left: 0, right: 0, top: 790,
        textAlign: "center",
        opacity: p(0.56, 0.74),
      }}>
        <div style={{
          display: "inline-block",
          fontFamily: MONO, fontWeight: 800, fontSize: 44, letterSpacing: 2,
          color: A.cool,
          background: mix(T.panel, A.cool, 0.10),
          border: `2px solid ${mix(T.line, A.cool, 0.55)}`,
          borderRadius: 14, padding: "14px 44px",
        }}>
          w := w − lr · ∇L
        </div>
      </div>

      <Foot theme={T} p={p(0.82, 0.92)}>
        Gradient descent is the engine behind almost every model trained today.
      </Foot>
    </Stage>
  );
};

// ── gd_hook ───────────────────────────────────────────────────────────────────
const HookScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);

  // Hiker 🧗 descends the parabola over 12%→82% of the beat
  const hikerPhase = p(0.12, 0.82);
  const hikerW = W_MIN + hikerPhase * (3 - W_MIN) * 0.92;
  const hikerX = wx(hikerW, 200, 1500);
  const hikerY = ly(LOSS_FN(hikerW), 220, 840);

  // Minimum marker position
  const minX = wx(3, 200, 1500);
  const minY = ly(0, 220, 840);

  // Curve reveal 6%→28%
  const nReveal = Math.max(2, Math.round(80 * Math.min(p(0.06, 0.28), 1)));

  // Fog breathing
  const fogO = 0.20 + Math.sin(frame * 0.022) * 0.07;

  // Current loss for the card
  const lossNow = LOSS_FN(hikerW);

  return (
    <Stage>
      <Head theme={T} kicker="THE INTUITION · FOGGY VALLEY" title="You are a hiker lost in fog" color={A.cool} o={p(0, 0.08)} />

      {/* SVG: axes + parabola + update arrow */}
      <svg style={{ position: "absolute", left: 0, top: 0 }} width={1920} height={1080}>
        {/* Axes */}
        <line x1={200} y1={840} x2={1530} y2={840} stroke={T.muted} strokeWidth={2} opacity={p(0.04, 0.14)} />
        <line x1={200} y1={840} x2={200} y2={200} stroke={T.muted} strokeWidth={2} opacity={p(0.04, 0.14)} />

        {/* Parabola — draws in progressively */}
        <polyline
          points={Array.from({ length: nReveal }).map((_, i) => {
            const w = W_MIN + (i / 79) * (W_MAX - W_MIN);
            return `${wx(w, 200, 1500).toFixed(1)},${ly(LOSS_FN(w), 220, 840).toFixed(1)}`;
          }).join(" ")}
          fill="none" stroke={A.main} strokeWidth={4.5}
        />

        {/* Downhill arrow at hiker position */}
        {p(0.46, 0.56) > 0.05 && (
          <line
            x1={hikerX} y1={hikerY + 10}
            x2={hikerX + (3 - hikerW) * 22}
            y2={hikerY + 10 + 65 * p(0.46, 0.56)}
            stroke={A.ok} strokeWidth={3.5}
            opacity={p(0.46, 0.56) * 0.9}
          />
        )}

        {/* Minimum star/dot */}
        <circle cx={minX} cy={minY} r={10} fill={A.ok}
          opacity={p(0.28, 0.40)}
          style={{ filter: "none" }}
        />
      </svg>

      {/* Fog overlay — breathing */}
      <div style={{
        position: "absolute", left: 0, right: 0, top: 200, height: 700,
        background: `linear-gradient(180deg, ${mix(T.bg1, A.cool, 0.07)} 0%, transparent 55%)`,
        opacity: fogO,
      }} />

      {/* Hiker emoji */}
      <div style={{
        position: "absolute",
        left: hikerX - 42, top: hikerY - 72,
        fontSize: 68,
        opacity: p(0.10, 0.24),
      }}>🧗</div>

      {/* Axis labels */}
      <div style={{ position: "absolute", left: 820, top: 858, fontFamily: MONO, fontSize: 24, color: T.muted, opacity: p(0.06, 0.18) }}>weight  w</div>
      <div style={{ position: "absolute", left: 118, top: 500, fontFamily: MONO, fontSize: 24, color: T.muted, opacity: p(0.06, 0.18), transform: "rotate(-90deg)" }}>loss L(w)</div>

      {/* Minimum label */}
      <div style={{ position: "absolute", left: minX + 18, top: minY - 20, fontFamily: MONO, fontSize: 22, color: A.ok, opacity: p(0.30, 0.42) }}>minimum</div>

      {/* Live loss card */}
      <Card theme={T} x={1560} y={370} w={300} h={180} color={A.main} o={p(0.40, 0.52)} glow>
        <div style={{ fontFamily: MONO, fontSize: 20, color: T.muted, marginBottom: 8 }}>current loss</div>
        <div style={{ fontFamily: MONO, fontWeight: 800, fontSize: 54, color: A.main }}>
          {lossNow.toFixed(1)}
        </div>
      </Card>

      {/* Flow particles from hiker toward minimum */}
      <Flow
        x1={hikerX} y1={hikerY}
        x2={minX} y2={minY}
        color={A.ok} n={4}
        o={p(0.52, 0.66) * 0.65}
        speed={0.009}
      />

      <Foot theme={T} p={p(0.84, 0.93)}>
        The hiker can't see the whole valley — but can always feel the slope. That slope is the gradient.
      </Foot>
    </Stage>
  );
};

// ── gd_step ───────────────────────────────────────────────────────────────────
// Main chart bounds
const SX0 = 160, SX1 = 1080, SY0 = 185, SY1 = 880;

const StepScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);

  // Step index tracks 12%→82% of the beat
  const stepPhase = Math.max(0, Math.min(1, p(0.12, 0.82)));
  const stepIdx = Math.min(STEPS_GOOD.length - 1, Math.floor(stepPhase * STEPS_GOOD.length));
  const wCur = STEPS_GOOD[stepIdx];
  const wNext = stepIdx < STEPS_GOOD.length - 1 ? STEPS_GOOD[stepIdx + 1] : wCur;
  const lossCur = LOSS_FN(wCur);
  const gradCur = GRAD_FN(wCur);

  const dotX = wx(wCur, SX0, SX1);
  const dotY = ly(lossCur, SY0, SY1);
  const dotXn = wx(Math.min(W_MAX, Math.max(W_MIN, wNext)), SX0, SX1);
  const dotYn = ly(Math.min(L_MAX, LOSS_FN(wNext)), SY0, SY1);

  // Curve fully in by 14%
  const nReveal = Math.max(2, Math.round(80 * Math.min(p(0.02, 0.14), 1)));

  // Equation panel fade-in
  const eqO = p(0.18, 0.30);

  // Chase highlight: blink the formula box
  const blinkO = 0.8 + Math.sin(frame * 0.12) * 0.2;

  return (
    <Stage>
      <Head
        theme={T}
        kicker={`THE ALGORITHM · STEP ${stepIdx + 1} OF ${STEPS_GOOD.length}`}
        title="Real gradient descent — step by step"
        color={A.main}
        o={p(0, 0.08)}
      />

      {/* SVG: axes + parabola + update arrow + trail */}
      <svg style={{ position: "absolute", left: 0, top: 0 }} width={1920} height={1080}>
        {/* Axes */}
        <line x1={SX0} y1={SY1} x2={SX1 + 40} y2={SY1} stroke={T.muted} strokeWidth={2} opacity={0.45} />
        <line x1={SX0} y1={SY1} x2={SX0} y2={SY0 - 20} stroke={T.muted} strokeWidth={2} opacity={0.45} />
        <text x={SX1 + 50} y={SY1 + 8} fontSize={24} fill={T.muted} fontFamily={MONO}>w</text>
        <text x={SX0 - 12} y={SY0 - 32} fontSize={24} fill={T.muted} fontFamily={MONO}>L</text>

        {/* Parabola */}
        <polyline
          points={Array.from({ length: nReveal }).map((_, i) => {
            const w = W_MIN + (i / 79) * (W_MAX - W_MIN);
            return `${wx(w, SX0, SX1).toFixed(1)},${ly(LOSS_FN(w), SY0, SY1).toFixed(1)}`;
          }).join(" ")}
          fill="none" stroke={A.main} strokeWidth={4}
        />

        {/* Tangent slope at current position (dashed) */}
        {eqO > 0.05 && (() => {
          const scaleY = (SY1 - SY0) / L_MAX;
          const tlen = 160;
          // Normalized direction along the tangent
          const dx = 1, dy = -gradCur * scaleY;
          const mag = Math.sqrt(dx * dx + dy * dy);
          const ux = (dx / mag) * tlen, uy = (dy / mag) * tlen;
          return (
            <line
              x1={dotX - ux * 0.5} y1={dotY - uy * 0.5}
              x2={dotX + ux * 0.5} y2={dotY + uy * 0.5}
              stroke={A.cool} strokeWidth={2.5} strokeDasharray="10 6"
              opacity={eqO * 0.7}
            />
          );
        })()}

        {/* Update arrow: current → next step */}
        {stepIdx < STEPS_GOOD.length - 1 && (
          <line
            x1={dotX} y1={dotY} x2={dotXn} y2={dotYn}
            stroke={A.ok} strokeWidth={3} markerEnd="url(#arrowGD)"
            opacity={p(0.14, 0.26) * 0.85}
          />
        )}
        <defs>
          <marker id="arrowGD" markerWidth="10" markerHeight="10" refX="7" refY="3" orient="auto">
            <path d="M0,0 L7,3 L0,6 Z" fill={A.ok} />
          </marker>
        </defs>

        {/* Trail: past step dots */}
        {STEPS_GOOD.slice(0, stepIdx + 1).map((ww, i) => {
          const cx = wx(ww, SX0, SX1);
          const cy = ly(LOSS_FN(ww), SY0, SY1);
          const isCur = i === stepIdx;
          return (
            <circle key={i}
              cx={cx} cy={cy}
              r={isCur ? 13 : 5}
              fill={isCur ? A.cool : mix(A.cool, T.bg1, 0.5)}
              opacity={isCur ? 1 : 0.52}
            />
          );
        })}

        {/* Minimum marker */}
        <circle cx={wx(3, SX0, SX1)} cy={ly(0, SY0, SY1)} r={9} fill={A.ok} opacity={0.9} />
      </svg>

      {/* Breathing glow on current dot */}
      <div style={{
        position: "absolute",
        left: dotX - 20, top: dotY - 20,
        width: 40, height: 40, borderRadius: 40,
        background: A.cool,
        boxShadow: `0 0 ${22 + Math.sin(frame * 0.1) * 10}px ${A.cool}`,
        opacity: 0.32 + Math.sin(frame * 0.1) * 0.14,
      }} />

      {/* Equation panel */}
      <Card theme={T} x={1130} y={190} w={670} h={640} color={A.main} o={eqO} glow>
        <div style={{ fontFamily: MONO, fontWeight: 700, fontSize: 26, color: T.muted, marginBottom: 20 }}>
          ITERATION {stepIdx + 1}
        </div>
        <div style={{ display: "flex", flexDirection: "column", gap: 18 }}>

          {/* w */}
          <div style={{ display: "flex", alignItems: "baseline", gap: 10 }}>
            <span style={{ fontFamily: MONO, fontSize: 24, color: T.muted, minWidth: 80 }}>w =</span>
            <span style={{ fontFamily: MONO, fontWeight: 800, fontSize: 38, color: A.cool }}>
              {wCur.toFixed(3)}
            </span>
          </div>

          {/* L(w) */}
          <div style={{ display: "flex", alignItems: "baseline", gap: 10 }}>
            <span style={{ fontFamily: MONO, fontSize: 24, color: T.muted, minWidth: 80 }}>L(w) =</span>
            <span style={{ fontFamily: MONO, fontWeight: 800, fontSize: 38, color: A.main }}>
              {lossCur.toFixed(3)}
            </span>
          </div>

          {/* ∇L */}
          <div style={{ display: "flex", alignItems: "baseline", gap: 10 }}>
            <span style={{ fontFamily: MONO, fontSize: 24, color: T.muted, minWidth: 80 }}>∇L =</span>
            <span style={{ fontFamily: MONO, fontWeight: 800, fontSize: 38, color: A.bad }}>
              {gradCur.toFixed(3)}
            </span>
          </div>

          {/* Update rule box */}
          <div style={{
            marginTop: 10, padding: "16px 20px",
            background: mix(T.bg0, A.ok, 0.08),
            borderRadius: 12, border: `1.5px solid ${mix(T.line, A.ok, 0.48)}`,
            opacity: blinkO,
          }}>
            <div style={{ fontFamily: MONO, fontSize: 20, color: T.muted, marginBottom: 6 }}>update rule</div>
            <div style={{ fontFamily: MONO, fontWeight: 800, fontSize: 30, color: A.ok }}>
              w ← w − {LR_GOOD} · ∇L
            </div>
            <div style={{ fontFamily: MONO, fontSize: 28, color: A.cool, marginTop: 8 }}>
              = {wNext.toFixed(3)}
            </div>
          </div>
        </div>
      </Card>

      {/* ScanBeam over equation panel */}
      <ScanBeam theme={T} x={1130} y={190} w={670} h={640} color={A.main} o={p(0.32, 0.46) * 0.35} speed={0.42} />

      <Foot theme={T} p={p(0.85, 0.94)}>
        Each step nudges w toward the minimum. Repeat until the loss stops falling.
      </Foot>
    </Stage>
  );
};

// ── gd_lr ─────────────────────────────────────────────────────────────────────
const LR_COLS = [
  { steps: STEPS_SLOW, label: "Too Small",  sub: "lr = 0.02",        color: A.cool, verdict: "crawls" },
  { steps: STEPS_FAST, label: "Too Large",  sub: "lr = 0.95",        color: A.bad,  verdict: "diverges" },
  { steps: STEPS_GOOD, label: "Just Right", sub: `lr = ${LR_GOOD}`,  color: A.ok,   verdict: "converges ✓" },
];

// Column chart bounds (3 columns, each 510px wide with 20px gap)
const LC_X0 = [130, 700, 1270];
const LC_X1 = [640, 1210, 1780];
const LC_Y0 = 265;
const LC_Y1 = 830;

const LRScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);

  // Animate all columns together 15%→82% of the beat
  const stepPhase = Math.max(0, Math.min(1, p(0.15, 0.82)));
  const stepIdx = Math.min(17, Math.floor(stepPhase * 18));

  return (
    <Stage>
      <Head theme={T} kicker="LEARNING RATE · THREE SCENARIOS" title="Learning rate controls the step size" color={A.main} o={p(0, 0.08)} />

      {/* Vertical dividers */}
      {[1, 2].map(ci => (
        <div key={ci} style={{
          position: "absolute", left: LC_X0[ci] - 16, top: 155, width: 2, height: 730,
          background: T.line, opacity: p(0.05, 0.16),
        }} />
      ))}

      {/* Column headers */}
      {LR_COLS.map((col, ci) => (
        <div key={ci} style={{
          position: "absolute", left: LC_X0[ci], top: 168,
          width: LC_X1[ci] - LC_X0[ci], textAlign: "center",
          opacity: p(0.08, 0.22),
        }}>
          <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 34, color: col.color }}>{col.label}</div>
          <div style={{ fontFamily: MONO, fontSize: 22, color: T.muted, marginTop: 4 }}>{col.sub}</div>
        </div>
      ))}

      {/* SVG: parabolas + trails per column */}
      <svg style={{ position: "absolute", left: 0, top: 0 }} width={1920} height={1080}>
        {LR_COLS.map((col, ci) => {
          const x0 = LC_X0[ci], x1 = LC_X1[ci];
          const trail = col.steps.slice(0, stepIdx + 1);
          const trailPts = trail
            .map(ww => {
              const cx = wx(Math.max(W_MIN, Math.min(W_MAX, ww)), x0, x1);
              const cy = ly(Math.min(L_MAX, LOSS_FN(ww)), LC_Y0, LC_Y1);
              return `${cx.toFixed(1)},${cy.toFixed(1)}`;
            })
            .join(" ");

          return (
            <React.Fragment key={ci}>
              {/* Axis */}
              <line x1={x0} y1={LC_Y1} x2={x1} y2={LC_Y1} stroke={T.muted} strokeWidth={1.5} opacity={0.32} />

              {/* Parabola */}
              <polyline
                points={Array.from({ length: 60 }).map((_, i) => {
                  const w = W_MIN + (i / 59) * (W_MAX - W_MIN);
                  return `${wx(w, x0, x1).toFixed(1)},${ly(LOSS_FN(w), LC_Y0, LC_Y1).toFixed(1)}`;
                }).join(" ")}
                fill="none"
                stroke={mix(col.color, T.bg1, 0.38)}
                strokeWidth={2.5}
                opacity={p(0.08, 0.22)}
              />

              {/* Trail connector */}
              {stepIdx >= 1 && (
                <polyline
                  points={trailPts}
                  fill="none" stroke={col.color} strokeWidth={2.5} opacity={0.55}
                />
              )}

              {/* Trail dots */}
              {trail.map((ww, si) => {
                const cx = wx(Math.max(W_MIN, Math.min(W_MAX, ww)), x0, x1);
                const cy = ly(Math.min(L_MAX, LOSS_FN(ww)), LC_Y0, LC_Y1);
                const isCur = si === stepIdx;
                return (
                  <circle key={si}
                    cx={cx} cy={cy}
                    r={isCur ? 9 : 4}
                    fill={isCur ? col.color : mix(col.color, T.bg1, 0.45)}
                    opacity={isCur ? 1 : 0.5}
                  />
                );
              })}

              {/* Minimum marker */}
              <circle
                cx={wx(3, x0, x1)} cy={ly(0, LC_Y0, LC_Y1)}
                r={6} fill={A.ok} opacity={p(0.10, 0.22)}
              />
            </React.Fragment>
          );
        })}
      </svg>

      {/* Breathing glow on each column's current dot */}
      {LR_COLS.map((col, ci) => {
        const ww = col.steps[stepIdx];
        const cx = wx(Math.max(W_MIN, Math.min(W_MAX, ww)), LC_X0[ci], LC_X1[ci]);
        const cy = ly(Math.min(L_MAX, LOSS_FN(ww)), LC_Y0, LC_Y1);
        return (
          <div key={ci} style={{
            position: "absolute",
            left: cx - 17, top: cy - 17, width: 34, height: 34, borderRadius: 34,
            background: col.color,
            opacity: 0.28 + Math.sin(frame * 0.10 + ci * 1.2) * 0.14,
            boxShadow: `0 0 ${18 + Math.sin(frame * 0.10 + ci * 1.2) * 8}px ${col.color}`,
          }} />
        );
      })}

      {/* Verdict chips */}
      {LR_COLS.map((col, ci) => (
        <div key={ci} style={{
          position: "absolute",
          left: LC_X0[ci], top: 860,
          width: LC_X1[ci] - LC_X0[ci],
          display: "flex", justifyContent: "center",
          opacity: p(0.56, 0.70),
        }}>
          <div style={{
            fontFamily: MONO, fontWeight: 800, fontSize: 26, color: col.color,
            background: mix(T.panel, col.color, 0.12),
            border: `2px solid ${col.color}`,
            borderRadius: 999, padding: "10px 28px",
          }}>{col.verdict}</div>
        </div>
      ))}

      {/* Step counter */}
      <div style={{
        position: "absolute", left: 830, top: 930,
        fontFamily: MONO, fontSize: 26, color: T.muted,
        opacity: p(0.18, 0.30),
      }}>
        step{" "}
        <span style={{ color: A.main, fontWeight: 800 }}>{stepIdx + 1}</span>
        {" "}/ 18
      </div>

      <Foot theme={T} p={p(0.84, 0.93)}>
        Same algorithm. Same starting point. The learning rate alone decides whether you converge.
      </Foot>
    </Stage>
  );
};

// ── gd_recap ──────────────────────────────────────────────────────────────────
const RecapScene: React.FC<{
  dur?: number;
  items?: string[];
  closer?: string;
}> = ({
  dur,
  items = [
    "The loss surface is a landscape — gradient descent follows the slope downhill.",
    "Each step: w := w − lr · ∇L  (weight minus learning-rate × gradient).",
    "The gradient ∇L is exact calculus — computed, not approximated.",
    "Learning rate is the knob: too small crawls, too large diverges, just right converges.",
    "Repeat until the loss flattens — that is a trained model.",
  ],
  closer = "One rule. A million applications.",
}) => {
  const frame = useCurrentFrame();
  const p = useP(dur);

  return (
    <AbsoluteFill style={{ padding: "68px 130px", justifyContent: "center" }}>
      <div style={{ opacity: p(0, 0.08), textAlign: "center", marginBottom: 26 }}>
        <Kicker theme={T} text="GRADIENT DESCENT · RECAP" cx />
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 62, color: T.text, marginTop: 12, letterSpacing: -1.5 }}>
          Everything you just saw
        </div>
      </div>

      <div style={{ display: "flex", flexDirection: "column", gap: 13, maxWidth: 1380, margin: "0 auto", width: "100%" }}>
        {items.map((it, i) => {
          const at = 0.06 + i * 0.10;
          const o = p(at, at + 0.07);
          return (
            <div key={i} style={{
              display: "flex", alignItems: "center", gap: 18, opacity: o,
              transform: `translateX(${(1 - o) * -26}px)`,
              background: mix(T.panel, A.main, 0.05),
              border: `1.5px solid ${T.line}`,
              borderLeft: `4px solid ${A.main}`,
              borderRadius: 12, padding: "14px 26px",
            }}>
              <span style={{ color: A.main, fontFamily: MONO, fontWeight: 700, fontSize: 26, minWidth: 28 }}>{i + 1}</span>
              <span style={{ fontFamily: SANS, fontSize: 27, color: T.text, lineHeight: 1.3 }}>{it}</span>
            </div>
          );
        })}
      </div>

      <div style={{ textAlign: "center", marginTop: 28, opacity: p(0.76, 0.88) }}>
        <div style={{
          fontFamily: SANS, fontWeight: 800, fontStyle: "italic", fontSize: 44,
          color: A.main,
          textShadow: `0 0 ${26 + Math.sin(frame * 0.06) * 12}px ${mix(T.bg0, A.main, 0.68)}`,
        }}>{closer}</div>
      </div>
    </AbsoluteFill>
  );
};

// ── Dispatch ──────────────────────────────────────────────────────────────────
export const GDScene: React.FC<{ variant: string; [key: string]: unknown }> = ({ variant, ...rest }) => {
  let content: React.ReactNode;
  let accent = A.main;
  switch (variant) {
    case "gd_title": content = <TitleScene  {...(rest as any)} />; break;
    case "gd_hook":  content = <HookScene   {...(rest as any)} />; accent = A.cool; break;
    case "gd_step":  content = <StepScene   {...(rest as any)} />; break;
    case "gd_lr":    content = <LRScene     {...(rest as any)} />; break;
    case "gd_recap": content = <RecapScene  {...(rest as any)} />; break;
    default:         content = <TitleScene  {...(rest as any)} />;
  }
  return (
    <AbsoluteFill>
      <Bg theme={T} accent={accent} />
      {content}
    </AbsoluteFill>
  );
};

export default GDScene;
