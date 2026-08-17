/**
 * LLMScenes.tsx — "LLM Training Strategies Explained" YouTube Short (8 beats)
 *
 * Visual identity:
 *   Theme : dark bg (makeTheme) with violet accent
 *   Accents (semantic):
 *     main  #8B5CF6  violet  → AI/neural theme
 *     cool  #06B6D4  cyan    → pretraining, base model
 *     warm  #F59E0B  amber   → fine-tuning, LoRA
 *     ok    #10B981  emerald → alignment, good outcomes
 *   Motif : orbiting neural nodes + flow particles between them
 *
 * Platform: YouTube Short / Instagram Reel — 1080×1920 portrait
 * Rules followed (skills/03-animation.md):
 *   • useP(dur) fractions — no fixed frame numbers
 *   • Continuous motion: Flow, breathing glow, orbiting nodes
 *   • No Math.random() — only rnd(i,j,s); no CSS filter/backdrop-filter
 */
import React from "react";
import { AbsoluteFill, interpolate, useCurrentFrame } from "remotion";
import {
  makeTheme, mix, useP, usePop, rnd, MONO, SANS,
  Bg, Kicker, Foot, Card, Flow, Wire, Type, Counter,
} from "../lib/primitives";

// ── Identity ────────────────────────────────────────────────────────────────
const T = makeTheme({ accent: "#8B5CF6" });
const A = {
  main: "#8B5CF6",  cool: "#06B6D4",  warm: "#F59E0B",
  ok:   "#10B981",  bad: "#EF4444",
};

// ── Vertical layout constants (1080×1920 portrait) ──────────────────────────
const VW = 1080, VH = 1920;
const CX = 540;
const CW = 920;
const SX = 80;

function ambientNodes(frame: number, o: number, n = 8) {
  return Array.from({ length: n }).map((_, i) => {
    const ang = frame * (0.007 + rnd(i, 0) * 0.005) + (i / n) * Math.PI * 2;
    return (
      <div key={i} style={{
        position: "absolute",
        left: CX + Math.cos(ang) * (360 + rnd(i, 1) * 100) - 6,
        top: 960 + Math.sin(ang) * (640 + rnd(i, 2) * 160) - 6,
        width: 12, height: 12, borderRadius: 12,
        background: A.main,
        opacity: o * (0.12 + rnd(i, 3) * 0.2),
        boxShadow: `0 0 ${10 + rnd(i, 4) * 8}px ${A.main}`,
      }} />
    );
  });
}

function GoalChip({ o, label, color }: { o: number; label: string; color: string }) {
  return (
    <div style={{
      position: "absolute", left: SX, top: 1550, width: CW, opacity: o as number,
    }}>
      <div style={{
        display: "inline-flex", alignItems: "center", gap: 14,
        background: mix(T.panel, color, 0.1),
        border: `2px solid ${mix(T.line, color, 0.5)}`,
        borderRadius: 999, padding: "16px 36px",
      }}>
        <div style={{ fontFamily: MONO, fontSize: 22, color, fontWeight: 700, letterSpacing: 2 }}>
          GOAL
        </div>
        <div style={{ width: 2, height: 24, background: color, opacity: 0.5 }} />
        <div style={{ fontFamily: SANS, fontSize: 32, color: T.text, fontWeight: 600 }}>{label}</div>
      </div>
    </div>
  );
}

// ── llm_title ────────────────────────────────────────────────────────────────
const TitleScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const pop = usePop(dur);

  return (
    <AbsoluteFill>
      {ambientNodes(frame, p(0.03, 0.15))}
      <div style={{ position: "absolute", left: 0, right: 0, top: 420, textAlign: "center" }}>
        <div style={{ opacity: p(0.02, 0.12), marginBottom: 28 }}>
          <Kicker theme={T} text="ARTIFICIAL INTELLIGENCE" cx />
        </div>
        <div style={{
          fontFamily: SANS, fontWeight: 800, fontSize: 108, lineHeight: 1.05,
          letterSpacing: -3, color: T.text,
          transform: `scale(${0.92 + pop(0) * 0.08})`,
          opacity: p(0.04, 0.18),
        }}>
          LLM Training
        </div>
        <div style={{
          fontFamily: SANS, fontWeight: 800, fontSize: 108, lineHeight: 1.1,
          letterSpacing: -3, color: A.main,
          textShadow: `0 0 80px ${mix(T.bg0, A.main, 0.65)}`,
          opacity: p(0.08, 0.22),
        }}>
          Strategies
        </div>
        <div style={{
          height: 5, margin: "32px auto",
          width: interpolate(p(0.14, 0.36), [0, 1], [0, 480]),
          background: `linear-gradient(90deg, ${A.main}, ${A.cool})`,
          borderRadius: 3,
        }} />
        <div style={{
          fontFamily: SANS, fontSize: 38, color: T.muted, marginTop: 8,
          opacity: p(0.24, 0.42),
        }}>
          Five techniques that power modern AI assistants
        </div>
      </div>
      <div style={{
        position: "absolute", left: CX - 160, top: 1280, width: 320,
        textAlign: "center", fontFamily: MONO, fontSize: 28, color: T.muted,
        opacity: p(0.50, 0.70),
      }}>
        2 min · 5 strategies
      </div>
      {Array.from({ length: 3 }).map((_, i) => (
        <Flow key={i}
          x1={80 + i * 360} y1={1380 + rnd(i, 0) * 180}
          x2={200 + i * 360} y2={1680 + rnd(i, 1) * 180}
          color={A.main} n={3} speed={0.008 + rnd(i, 2) * 0.004}
          o={0.25} size={7}
        />
      ))}
    </AbsoluteFill>
  );
};

// ── llm_hook ─────────────────────────────────────────────────────────────────
const HookScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);

  const icons = [
    { emoji: "🌐", label: "Raw Model", at: 0.08, x: CX - 310, color: T.muted },
    { emoji: "⚡", label: "Training",  at: 0.28, x: CX,       color: A.main },
    { emoji: "🤖", label: "Assistant", at: 0.50, x: CX + 310, color: A.ok },
  ];

  return (
    <AbsoluteFill>
      {ambientNodes(frame, p(0, 0.12), 6)}
      <div style={{
        position: "absolute", left: 0, right: 0, top: 100,
        textAlign: "center", opacity: p(0, 0.08),
      }}>
        <Kicker theme={T} text="THE QUESTION" cx />
      </div>
      <div style={{
        position: "absolute", left: SX, top: 380, width: CW,
        fontFamily: SANS, fontWeight: 800, fontSize: 64, lineHeight: 1.15,
        color: T.text, textAlign: "center",
        opacity: p(0.04, 0.16),
      }}>
        How does a raw language model become a<br />
        <span style={{ color: A.main }}>helpful AI assistant</span>?
      </div>
      {/* Transformation journey */}
      <div style={{ position: "absolute", left: 0, top: 740, width: VW, height: 520 }}>
        {icons.map((ic, i) => (
          <React.Fragment key={i}>
            {i > 0 && (
              <>
                <Wire
                  x1={icons[i - 1].x + 75} y1={180}
                  x2={ic.x - 75} y2={180}
                  p={p(ic.at - 0.08, ic.at)}
                  color={ic.color} w={4}
                />
                <Flow
                  x1={icons[i - 1].x + 75} y1={180}
                  x2={ic.x - 75} y2={180}
                  color={ic.color} n={5}
                  o={p(ic.at, ic.at + 0.08) * 0.6}
                  speed={0.012}
                />
              </>
            )}
            <div style={{
              position: "absolute",
              left: ic.x - 130, top: 80,
              width: 260, textAlign: "center",
              opacity: p(ic.at, ic.at + 0.08),
              transform: `translateY(${(1 - p(ic.at, ic.at + 0.06)) * 20}px)`,
            }}>
              <div style={{ fontSize: 80, marginBottom: 12 }}>{ic.emoji}</div>
              <div style={{
                fontFamily: MONO, fontSize: 28, color: ic.color,
                fontWeight: 700,
                background: mix(T.panel, ic.color, 0.08),
                borderRadius: 999, padding: "10px 24px",
                display: "inline-block",
              }}>{ic.label}</div>
            </div>
          </React.Fragment>
        ))}
      </div>
      <div style={{
        position: "absolute", left: SX, top: 1580, width: CW,
        fontFamily: SANS, fontSize: 32, color: T.muted,
        textAlign: "center", opacity: p(0.64, 0.78),
      }}>
        Five stages. Each one builds on the last.
      </div>
    </AbsoluteFill>
  );
};

// ── llm_pretrain ─────────────────────────────────────────────────────────────
const PretrainScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);

  const sources = [
    { emoji: "📚", label: "Books", at: 0.06 },
    { emoji: "🌐", label: "Web", at: 0.14 },
  ];

  return (
    <AbsoluteFill>
      {ambientNodes(frame, p(0, 0.08), 5)}
      <div style={{
        position: "absolute", left: 0, right: 0, top: 130,
        textAlign: "center", opacity: p(0, 0.08),
      }}>
        <Kicker theme={T} text="STAGE 1 · PRETRAINING" cx />
        <div style={{
          fontFamily: SANS, fontWeight: 800, fontSize: 48, color: A.cool,
          marginTop: 10, letterSpacing: -1.5,
        }}>
          Learn language from massive data
        </div>
      </div>
      {/* Data sources — two big cards side by side */}
      <div style={{ position: "absolute", left: SX, top: 410, width: CW, display: "flex", gap: 20 }}>
        {sources.map((src, i) => (
          <div key={i} style={{
            flex: 1, textAlign: "center", padding: "40px 0",
            background: mix(T.panel, A.cool, 0.06),
            border: `2px solid ${mix(T.line, A.cool, 0.3)}`,
            borderRadius: 20,
            opacity: p(src.at, src.at + 0.07),
            transform: `translateY(${(1 - p(src.at, src.at + 0.06)) * 20}px)`,
          }}>
            <div style={{ fontSize: 64 }}>{src.emoji}</div>
            <div style={{ fontFamily: MONO, fontSize: 28, color: T.text, fontWeight: 700, marginTop: 12 }}>
              {src.label}
            </div>
          </div>
        ))}
      </div>
      {/* Flow — data moving to model */}
      <div style={{ position: "absolute", left: 0, top: 670, width: VW }}>
        <div style={{ textAlign: "center", opacity: p(0.20, 0.30) }}>
          <div style={{
            fontFamily: MONO, fontSize: 26, color: A.cool,
            marginBottom: 10,
          }}>
            trillions of tokens →
          </div>
        </div>
        <Flow x1={SX + 120} y1={0} x2={CX + 120} y2={0} color={A.cool} n={8} o={p(0.22, 0.32)} speed={0.015} size={8} />
        <Wire x1={SX + 120} y1={0} x2={CX + 120} y2={0} p={p(0.18, 0.26)} color={A.cool} w={4} />
      </div>
      {/* Model brain card — centered */}
      <Card theme={T} x={CX - 200} y={770} w={400} h={280} color={A.cool} o={p(0.22, 0.32)} glow>
        <div style={{ textAlign: "center" }}>
          <div style={{ fontSize: 80 }}>🧠</div>
          <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 38, color: A.cool, marginTop: 12 }}>
            Foundation Model
          </div>
          <div style={{ fontFamily: MONO, fontSize: 24, color: T.muted, marginTop: 8 }}>
            grammar · facts · reasoning
          </div>
        </div>
      </Card>
      {/* Stats strip */}
      <div style={{
        position: "absolute", left: CX - 160, top: 1150, width: 320, height: 100,
        background: mix(T.panel, A.main, 0.08),
        border: `2px solid ${mix(T.line, A.main, 0.35)}`,
        borderRadius: 16, textAlign: "center",
        opacity: p(0.38, 0.48),
      }}>
        <div style={{ fontFamily: MONO, fontSize: 22, color: T.muted, marginTop: 14 }}>data consumed</div>
        <Counter p={Math.min(1, p(0.42, 0.56))} to={10} suffix=" TB+" color={A.main} size={52} />
      </div>
      {/* Scan beam on model */}
      <div style={{
        position: "absolute", left: CX - 200, top: 770, width: 400, height: 280,
        overflow: "hidden", borderRadius: 20, pointerEvents: "none",
        opacity: p(0.34, 0.48) * 0.35,
      }}>
        <div style={{
          position: "absolute", left: 0, top: ((frame * 0.5) % 340) - 30, width: "100%", height: 3,
          background: A.cool, boxShadow: `0 0 18px ${A.cool}`, opacity: 0.6,
        }} />
      </div>
      <GoalChip o={p(0.56, 0.68)} label="Build a strong foundation" color={A.cool} />
    </AbsoluteFill>
  );
};

// ── llm_sft ──────────────────────────────────────────────────────────────────
const SFTScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);

  const bubbles = [
    { role: "Human", text: "What is the capital of France?", at: 0.10, color: A.main, emoji: "❓" },
    { role: "Assistant", text: "The capital of France is Paris.", at: 0.30, color: A.ok, emoji: "💬" },
  ];

  return (
    <AbsoluteFill>
      {ambientNodes(frame, p(0, 0.08), 5)}
      <div style={{
        position: "absolute", left: 0, right: 0, top: 130,
        textAlign: "center", opacity: p(0, 0.08),
      }}>
        <Kicker theme={T} text="STAGE 2 · SUPERVISED FINE-TUNING" cx />
        <div style={{
          fontFamily: SANS, fontWeight: 800, fontSize: 48, color: A.warm,
          marginTop: 10, letterSpacing: -1.5,
        }}>
          Learn to follow instructions
        </div>
      </div>
      {/* Chat panel — centered, fewer bigger bubbles */}
      <div style={{
        position: "absolute", left: SX, top: 390, width: CW,
        background: mix(T.panel, A.warm, 0.04),
        border: `2px solid ${mix(T.line, A.warm, 0.25)}`,
        borderRadius: 24, padding: "28px 32px",
        opacity: p(0.04, 0.14),
      }}>
        <div style={{
          display: "flex", alignItems: "center", gap: 10, marginBottom: 24,
          borderBottom: `1px solid ${T.line}`, paddingBottom: 16,
        }}>
          <div style={{ width: 14, height: 14, borderRadius: 14, background: "#EF4444" }} />
          <div style={{ width: 14, height: 14, borderRadius: 14, background: "#F59E0B" }} />
          <div style={{ width: 14, height: 14, borderRadius: 14, background: "#10B981" }} />
          <div style={{ fontFamily: MONO, fontSize: 24, color: T.muted, marginLeft: 10 }}>
            fine-tuning — Q&A
          </div>
        </div>
        {bubbles.map((b, i) => (
          <div key={i} style={{
            marginBottom: 24, opacity: p(b.at, b.at + 0.06),
            transform: `translateY(${(1 - p(b.at, b.at + 0.06)) * 16}px)`,
          }}>
            <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 8 }}>
              <span style={{ fontSize: 28 }}>{b.emoji}</span>
              <span style={{ fontFamily: MONO, fontSize: 22, fontWeight: 700, color: b.color }}>{b.role}</span>
            </div>
            <div style={{
              background: mix(T.panel, b.color, 0.08),
              border: `1.5px solid ${mix(T.line, b.color, 0.4)}`,
              borderRadius: 16, padding: "16px 22px",
            }}>
              <Type text={b.text} p={i % 2 === 0 ? 1 : Math.min(1, p(b.at + 0.04, b.at + 0.18))} color={T.text} size={30} />
            </div>
          </div>
        ))}
        {/* Third bubble typing — "Explain quantum computing..." */}
        <div style={{
          opacity: p(0.52, 0.62),
          transform: `translateY(${(1 - p(0.52, 0.62)) * 16}px)`,
        }}>
          <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 8 }}>
            <span style={{ fontSize: 28 }}>❓</span>
            <span style={{ fontFamily: MONO, fontSize: 22, fontWeight: 700, color: A.main }}>Human</span>
          </div>
          <div style={{
            background: mix(T.panel, A.main, 0.08),
            border: `1.5px solid ${mix(T.line, A.main, 0.4)}`,
            borderRadius: 16, padding: "16px 22px",
          }}>
            <Type text="Explain quantum computing simply." p={Math.min(1, p(0.54, 0.72))} color={T.text} size={30} />
          </div>
        </div>
      </div>
      {/* Scan beam */}
      <div style={{
        position: "absolute", left: SX, top: 340, width: CW, height: 500,
        overflow: "hidden", borderRadius: 24, pointerEvents: "none",
        opacity: p(0.40, 0.52) * 0.25,
      }}>
        <div style={{
          position: "absolute", left: 0, top: ((frame * 0.4) % 560) - 30, width: "100%", height: 3,
          background: A.warm, boxShadow: `0 0 18px ${A.warm}`, opacity: 0.5,
        }} />
      </div>
      <GoalChip o={p(0.72, 0.84)} label="Teach the model to follow instructions" color={A.warm} />
    </AbsoluteFill>
  );
};

// ── llm_lora ─────────────────────────────────────────────────────────────────
const LORAScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);

  return (
    <AbsoluteFill>
      {ambientNodes(frame, p(0, 0.08), 5)}
      <div style={{
        position: "absolute", left: 0, right: 0, top: 130,
        textAlign: "center", opacity: p(0, 0.08),
      }}>
        <Kicker theme={T} text="STAGE 3 · LORA" cx />
        <div style={{
          fontFamily: SANS, fontWeight: 800, fontSize: 48, color: A.warm,
          marginTop: 10, letterSpacing: -1.5,
        }}>
          Efficient fine-tuning
        </div>
      </div>
      {/* Frozen model (large matrix) */}
      <div style={{ position: "absolute", left: CX - 320, top: 350, opacity: p(0.04, 0.14) }}>
        <div style={{ fontFamily: MONO, fontSize: 24, color: T.muted, marginBottom: 10, textAlign: "center" }}>
          FROZEN BASE MODEL
        </div>
        <div style={{
          width: 640, height: 360,
          background: `linear-gradient(135deg, ${mix(T.bg2, A.cool, 0.15)}, ${mix(T.bg2, A.cool, 0.05)})`,
          border: `2px solid ${mix(T.line, A.cool, 0.3)}`,
          borderRadius: 16,
          display: "grid", gridTemplateColumns: "repeat(8, 1fr)", gap: 6, padding: 14,
        }}>
          {Array.from({ length: 64 }).map((_, i) => (
            <div key={i} style={{
              background: mix(T.bg1, A.cool, 0.04 + rnd(i, 0) * 0.08),
              borderRadius: 4, border: `1px solid ${T.line}`,
            }} />
          ))}
        </div>
      </div>
      {/* LoRA adapters — below the model, no overlap */}
      <div style={{
        position: "absolute", left: CX - 280, top: 810, width: 560,
        opacity: p(0.18, 0.28),
      }}>
        <div style={{ fontFamily: MONO, fontSize: 24, color: A.warm, fontWeight: 700, marginBottom: 14, textAlign: "center" }}>
          + LORA ADAPTERS (trainable)
        </div>
        <div style={{ display: "flex", justifyContent: "center", gap: 30 }}>
          {[
            { label: "A", c: A.warm },
            { label: "B", c: A.main },
            { label: "C", c: A.ok },
          ].map((ad, i) => (
            <div key={i} style={{
              width: 140, height: 80, borderRadius: 12,
              background: mix(T.panel, ad.c, 0.2),
              border: `3px solid ${ad.c}`,
              display: "flex", alignItems: "center", justifyContent: "center",
              fontFamily: MONO, fontSize: 24, fontWeight: 700, color: ad.c,
              transform: `translateY(${(1 - p(0.22 + i * 0.06, 0.30 + i * 0.06)) * 20}px)`,
              boxShadow: `0 0 ${14 + Math.sin(frame * 0.08 + i) * 6}px ${mix(T.bg0, ad.c, 0.4)}`,
              opacity: p(0.22 + i * 0.06, 0.30 + i * 0.06),
            }}>{ad.label}</div>
          ))}
        </div>
      </div>
      {/* "only these update" moved to avoid overlap with model grid */}
      <div style={{
        position: "absolute", left: CX + 90, top: 620,
        opacity: p(0.34, 0.46),
      }}>
        <div style={{
          fontFamily: MONO, fontSize: 26, color: A.warm,
          background: mix(T.panel, A.warm, 0.12),
          border: `2px solid ${mix(T.line, A.warm, 0.5)}`,
          borderRadius: 999, padding: "10px 24px",
        }}>
          ← only these update
        </div>
      </div>
      {/* Efficiency stats */}
      <Card theme={T} x={SX} y={1110} w={CW} h={160} color={A.warm} o={p(0.44, 0.56)}>
        <div style={{ display: "flex", justifyContent: "space-around", alignItems: "center", height: "100%" }}>
          <div style={{ textAlign: "center" }}>
            <div style={{ fontFamily: MONO, fontSize: 24, color: T.muted }}>Memory Savings</div>
            <div style={{ fontFamily: MONO, fontWeight: 800, fontSize: 44, color: A.ok }}>
              <Counter p={Math.min(1, p(0.50, 0.68))} to={90} suffix="%" color={A.ok} size={44} />
            </div>
          </div>
          <div style={{ width: 2, height: 80, background: T.line }} />
          <div style={{ textAlign: "center" }}>
            <div style={{ fontFamily: MONO, fontSize: 24, color: T.muted }}>Params Updated</div>
            <div style={{ fontFamily: MONO, fontWeight: 800, fontSize: 44, color: A.warm }}>
              &lt; 1%
            </div>
          </div>
        </div>
      </Card>
      <GoalChip o={p(0.66, 0.78)} label="Efficient fine-tuning" color={A.warm} />
    </AbsoluteFill>
  );
};

// ── llm_qlora ────────────────────────────────────────────────────────────────
const QLORAScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);

  return (
    <AbsoluteFill>
      {ambientNodes(frame, p(0, 0.08), 5)}
      <div style={{
        position: "absolute", left: 0, right: 0, top: 130,
        textAlign: "center", opacity: p(0, 0.08),
      }}>
        <Kicker theme={T} text="STAGE 4 · QLORA" cx />
        <div style={{
          fontFamily: SANS, fontWeight: 800, fontSize: 48, color: A.main,
          marginTop: 10, letterSpacing: -1.5,
        }}>
          Compress + fine-tune
        </div>
      </div>
      {/* Memory comparison — centered */}
      <div style={{ position: "absolute", left: CX - 360, top: 410, width: 720 }}>
        {/* Before */}
        <div style={{
          opacity: p(0.06, 0.16),
          marginBottom: 50,
        }}>
          <div style={{ fontFamily: MONO, fontSize: 24, color: T.muted, marginBottom: 10 }}>
            STANDARD (16-bit)
          </div>
          <div style={{
            height: 80, width: 640, borderRadius: 16,
            background: `linear-gradient(90deg, ${mix(T.bg2, A.bad, 0.2)}, ${mix(T.bg2, A.bad, 0.05)})`,
            border: `2px solid ${mix(T.line, A.bad, 0.3)}`,
            position: "relative",
          }}>
            <div style={{
              position: "absolute", left: 0, top: 0, width: "100%", height: "100%",
              background: `linear-gradient(90deg, ${mix(A.bad, T.bg0, 0.2)}33, transparent 80%)`,
            }} />
            <div style={{
              position: "absolute", right: 24, top: 22,
              fontFamily: MONO, fontWeight: 700, fontSize: 30, color: A.bad,
            }}>
              16-bit
            </div>
          </div>
        </div>
        {/* After */}
        <div style={{
          opacity: p(0.20, 0.32),
        }}>
          <div style={{ fontFamily: MONO, fontSize: 24, color: T.muted, marginBottom: 10 }}>
            QUANTIZED (4-bit)
          </div>
          <div style={{
            height: 80, width: 260, borderRadius: 16,
            background: `linear-gradient(90deg, ${mix(T.bg2, A.ok, 0.25)}, ${mix(T.bg2, A.ok, 0.05)})`,
            border: `2px solid ${mix(T.line, A.ok, 0.4)}`,
            position: "relative",
          }}>
            <div style={{
              position: "absolute", right: 20, top: 22,
              fontFamily: MONO, fontWeight: 700, fontSize: 30, color: A.ok,
            }}>
              4-bit
            </div>
          </div>
        </div>
        {/* 4x badge */}
        <div style={{
          position: "absolute", left: 680, top: 160,
          opacity: p(0.26, 0.38),
        }}>
          <div style={{
            fontFamily: MONO, fontWeight: 800, fontSize: 56, color: A.ok,
            background: mix(T.panel, A.ok, 0.12),
            border: `3px solid ${A.ok}`,
            borderRadius: 20, padding: "16px 28px",
            textAlign: "center",
          }}>
            4×
            <div style={{ fontFamily: MONO, fontSize: 22, color: T.muted, fontWeight: 400 }}>
              less memory
            </div>
          </div>
        </div>
      </div>
      {/* Flow — compression effect */}
      <div style={{
        position: "absolute", left: CX - 100, top: 730, width: 200, height: 40,
        opacity: p(0.16, 0.28),
      }}>
        <Flow x1={0} y1={20} x2={200} y2={20} color={A.main} n={6} speed={0.014} o={0.6} size={8} />
      </div>
      {/* LoRA on compressed */}
      <div style={{
        position: "absolute", left: CX - 250, top: 850, width: 500,
        textAlign: "center", opacity: p(0.34, 0.46),
      }}>
        <div style={{ fontFamily: MONO, fontSize: 24, color: A.main, fontWeight: 700, marginBottom: 18 }}>
          + LoRA adapters on compressed base
        </div>
        <div style={{ display: "flex", justifyContent: "center", gap: 50 }}>
          <div style={{
            padding: "16px 28px", borderRadius: 14,
            background: mix(T.panel, A.main, 0.1),
            border: `2px solid ${mix(T.line, A.main, 0.4)}`,
            fontFamily: MONO, fontSize: 22, color: A.main, fontWeight: 700,
          }}>
            🧊 4-bit Base
          </div>
          <div style={{
            padding: "16px 28px", borderRadius: 14,
            background: mix(T.panel, A.warm, 0.15),
            border: `2px solid ${A.warm}`,
            fontFamily: MONO, fontSize: 22, color: A.warm, fontWeight: 700,
            boxShadow: `0 0 ${14 + Math.sin(frame * 0.1) * 6}px ${mix(T.bg0, A.warm, 0.4)}`,
          }}>
            ⚡ LoRA
          </div>
        </div>
      </div>
      <GoalChip o={p(0.58, 0.70)} label="Fine-tune large models with less memory" color={A.main} />
    </AbsoluteFill>
  );
};

// ── llm_rlhf ─────────────────────────────────────────────────────────────────
const RLHFScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);

  return (
    <AbsoluteFill>
      {ambientNodes(frame, p(0, 0.08), 5)}
      <div style={{
        position: "absolute", left: 0, right: 0, top: 130,
        textAlign: "center", opacity: p(0, 0.08),
      }}>
        <Kicker theme={T} text="STAGE 5 · RLHF" cx />
        <div style={{
          fontFamily: SANS, fontWeight: 800, fontSize: 48, color: A.ok,
          marginTop: 10, letterSpacing: -1.5,
        }}>
          Learn from human preferences
        </div>
      </div>
      {/* Two response cards — positioned explicitly (Card uses position:absolute so flex won't work) */}
        <Card theme={T} x={SX} y={390} w={452} h={380} color={A.ok} o={p(0.06, 0.16)}>
          <div style={{
            fontFamily: MONO, fontSize: 22, color: A.ok, fontWeight: 700,
            marginBottom: 14, display: "flex", alignItems: "center", gap: 10,
          }}>
            ✅ Response A
          </div>
          <div style={{
            fontFamily: SANS, fontSize: 28, color: T.text, lineHeight: 1.35,
          }}>
            "I don't have enough information to answer that accurately. Let me explain what I do know..."
          </div>
        </Card>
        <Card theme={T} x={SX + 468} y={390} w={452} h={380} color={A.bad} o={p(0.06, 0.16)}>
          <div style={{
            fontFamily: MONO, fontSize: 22, color: A.bad, fontWeight: 700,
            marginBottom: 14, display: "flex", alignItems: "center", gap: 10,
          }}>
            ❌ Response B
          </div>
          <div style={{
            fontFamily: SANS, fontSize: 28, color: T.text, lineHeight: 1.35,
          }}>
            "Here's a made-up answer with false facts and no sources."
          </div>
        </Card>
      {/* Human evaluator */}
      <div style={{
        position: "absolute", left: CX - 180, top: 850, width: 360,
        textAlign: "center", opacity: p(0.20, 0.32),
      }}>
        <div style={{ fontSize: 60, marginBottom: 8 }}>🧑‍⚖️</div>
        <div style={{
          fontFamily: MONO, fontSize: 24, fontWeight: 700, color: A.ok,
          background: mix(T.panel, A.ok, 0.1),
          border: `2px solid ${mix(T.line, A.ok, 0.4)}`,
          borderRadius: 999, padding: "10px 28px",
          display: "inline-block",
        }}>
          Human prefers A → Reward
        </div>
      </div>
      {/* Feedback loop */}
      <div style={{ position: "absolute", left: 0, top: 1110, width: VW, height: 130 }}>
        <div style={{ fontFamily: MONO, fontSize: 26, color: A.ok, textAlign: "center", opacity: p(0.32, 0.44) }}>
          Model learns from preferences
        </div>
        <Flow
          x1={CX + 120} y1={50} x2={CX - 120} y2={50}
          color={A.ok} n={7} speed={0.018}
          o={p(0.36, 0.48) * 0.7} size={9}
        />
        <Wire
          x1={CX + 120} y1={50} x2={CX - 120} y2={50}
          p={p(0.32, 0.42)} color={A.ok} w={4} arrow
        />
        <div style={{
          position: "absolute", left: CX - 100, top: 66,
          fontFamily: MONO, fontSize: 22, color: A.ok,
          fontWeight: 700, opacity: p(0.38, 0.50),
        }}>
          ← preference feedback
        </div>
      </div>
      {/* Alignment qualities */}
      <div style={{
        position: "absolute", left: SX, top: 1310, width: CW,
        display: "flex", justifyContent: "center", gap: 30,
        opacity: p(0.44, 0.56),
      }}>
        {[
          { label: "Helpful", c: A.ok },
          { label: "Accurate", c: A.cool },
          { label: "Harmless", c: A.main },
        ].map((q, i) => (
          <div key={i} style={{
            fontFamily: MONO, fontWeight: 700, fontSize: 24,
            color: q.c,
            background: mix(T.panel, q.c, 0.1),
            border: `2px solid ${mix(T.line, q.c, 0.4)}`,
            borderRadius: 999, padding: "10px 24px",
          }}>{q.label}</div>
        ))}
      </div>
      {/* Breathing glow */}
      <div style={{
        position: "absolute", left: CX - 80, top: 1200, width: 160, height: 50,
        borderRadius: 25, background: A.ok,
        opacity: 0.08 + Math.sin(frame * 0.08) * 0.06,
        boxShadow: `0 0 60px ${A.ok}`,
      }} />
      <GoalChip o={p(0.62, 0.74)} label="Align AI with human values" color={A.ok} />
    </AbsoluteFill>
  );
};

// ── llm_recap ────────────────────────────────────────────────────────────────
const RECAP_COLORS = [A.cool, A.warm, A.warm, A.main, A.ok];
const RecapScene: React.FC<{
  dur?: number;
  items?: string[];
  closer?: string;
}> = ({
  dur,
  items = [
    "Pretraining — build a strong foundation",
    "SFT — teach instruction following",
    "LoRA — efficient fine-tuning",
    "QLoRA — fine-tune with less memory",
    "RLHF — align with human values",
  ],
  closer = "Five strategies. One intelligent assistant.",
}) => {
  const frame = useCurrentFrame();
  const p = useP(dur);

  return (
    <AbsoluteFill>
      {ambientNodes(frame, p(0, 0.10), 6)}
      <div style={{
        position: "absolute", left: 0, right: 0, top: 180,
        textAlign: "center", opacity: p(0, 0.08),
      }}>
        <Kicker theme={T} text="THE LEARNING JOURNEY" cx />
        <div style={{
          fontFamily: SANS, fontWeight: 800, fontSize: 52,
          color: T.text, marginTop: 12, letterSpacing: -1.5,
        }}>
          Everything you just saw
        </div>
      </div>
      <div style={{
        position: "absolute", left: SX + 20, top: 380, width: CW - 40,
        display: "flex", flexDirection: "column", gap: 16,
      }}>
        {items.map((label, i) => {
          const c = RECAP_COLORS[i % RECAP_COLORS.length];
          const at = 0.06 + i * 0.10;
          const o = p(at, at + 0.07);
          return (
            <div key={i} style={{
              display: "flex", alignItems: "center", gap: 18,
              opacity: o as number,
              transform: `translateX(${(1 - o) * -24}px)`,
              background: mix(T.panel, c, 0.05),
              border: `1.5px solid ${T.line}`,
              borderLeft: `5px solid ${c}`,
              borderRadius: 14, padding: "18px 28px",
            }}>
              <span style={{
                fontFamily: MONO, fontWeight: 700, fontSize: 28,
                color: c, minWidth: 34,
              }}>
                {i + 1}
              </span>
              <span style={{
                fontFamily: SANS, fontSize: 32, color: T.text,
                lineHeight: 1.25, fontWeight: 500,
              }}>
                {label}
              </span>
            </div>
          );
        })}
      </div>
      <div style={{
        position: "absolute", left: 0, right: 0, top: 1400,
        textAlign: "center", opacity: p(0.74, 0.86),
      }}>
        <div style={{
          fontFamily: SANS, fontWeight: 800, fontStyle: "italic",
          fontSize: 48, color: A.main,
          textShadow: `0 0 ${30 + Math.sin(frame * 0.06) * 14}px ${mix(T.bg0, A.main, 0.68)}`,
        }}>{closer}</div>
      </div>
      <div style={{
        position: "absolute", left: CX - 220, top: 1400, width: 440, height: 70,
        borderRadius: 35, background: A.main,
        opacity: 0.04 + Math.sin(frame * 0.07) * 0.03,
        boxShadow: `0 0 80px ${A.main}`,
      }} />
    </AbsoluteFill>
  );
};

// ── Dispatch ─────────────────────────────────────────────────────────────────
export const LLMScene: React.FC<{ variant: string; [key: string]: unknown }> = ({ variant, ...rest }) => {
  let content: React.ReactNode;
  let accent = A.main;
  switch (variant) {
    case "llm_title":   content = <TitleScene    {...(rest as any)} />; break;
    case "llm_hook":    content = <HookScene     {...(rest as any)} />; accent = A.cool; break;
    case "llm_pretrain": content = <PretrainScene {...(rest as any)} />; accent = A.cool; break;
    case "llm_sft":     content = <SFTScene      {...(rest as any)} />; accent = A.warm; break;
    case "llm_lora":    content = <LORAScene     {...(rest as any)} />; accent = A.warm; break;
    case "llm_qlora":   content = <QLORAScene    {...(rest as any)} />; break;
    case "llm_rlhf":    content = <RLHFScene     {...(rest as any)} />; accent = A.ok; break;
    case "llm_recap":   content = <RecapScene    {...(rest as any)} />; break;
    default:            content = <TitleScene    {...(rest as any)} />;
  }
  return (
    <AbsoluteFill>
      <Bg theme={T} accent={accent} />
      {content}
    </AbsoluteFill>
  );
};

export default LLMScene;
