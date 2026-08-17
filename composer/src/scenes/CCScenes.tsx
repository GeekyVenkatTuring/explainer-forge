/**
 * CCScenes.tsx — "Credit Cards in India" Telugu master video (prefix `cc`).
 *
 * Identity (skills/04):
 *   theme accent = cyan (the card / mechanics). Semantic accents:
 *     card  cyan   #22D3EE — the card itself, neutral mechanics
 *     good  green  #34D399 — benefits, rewards, paying in full, healthy score
 *     bad   rose   #FB7185 — debt, interest, the trap, wrong usage
 *     money amber  #FBBF24 — rupees, credit limit, the bank's money, fees
 *     fin   violet #A78BFA — CIBIL score, fintech/startup cards
 *   Recurring motif: a drawn credit card (CardMotif) — title, dividers, backgrounds.
 *
 * On-screen text is Telugu (Noto Sans Telugu via the SANS/MONO fallback stacks);
 * brand names, ₹ amounts, numbers and % stay in Latin. Rules: duration-aware phases
 * (useP), continuous motion every frame, deterministic (rnd), author on Stage.
 */
import React from "react";
import { AbsoluteFill, interpolate, useCurrentFrame } from "remotion";
import {
  makeTheme, mix, useP, usePop, rnd, MONO, SANS,
  Bg, Stage, Kicker, Head, Card, Flow, Wire, Counter, Brackets, ScanBeam,
} from "../lib/primitives";

const T = makeTheme({ accent: "#22D3EE" });
const A = { card: "#22D3EE", good: "#34D399", bad: "#FB7185", money: "#FBBF24", fin: "#A78BFA" };

// --- recurring motif: a drawn credit card with chip, stripe, and a live shimmer ---
const CardMotif: React.FC<{
  x: number; y: number; w: number; color?: string; o?: number; brand?: string; label?: string;
}> = ({ x, y, w, color = A.card, o = 1, brand = "RuPay", label }) => {
  const frame = useCurrentFrame();
  const h = w * 0.63; // ISO card ratio ≈ 1.586
  const shimmer = ((frame * 3) % (w + 240)) - 120; // continuous sheen sweep
  return (
    <div style={{
      position: "absolute", left: x, top: y, width: w, height: h, borderRadius: w * 0.06,
      background: `linear-gradient(135deg, ${mix(T.panel, color, 0.35)}, ${mix(T.bg1, color, 0.12)})`,
      border: `2px solid ${mix(color, "#ffffff", 0.15)}`, opacity: o, overflow: "hidden",
      boxShadow: `0 24px 70px ${mix(T.bg0, color, 0.18)}`, transform: `translateY(${(1 - o) * 24}px)`,
    }}>
      {/* sheen */}
      <div style={{ position: "absolute", top: -20, left: shimmer, width: 90, height: h + 40, transform: "rotate(16deg)",
        background: `linear-gradient(90deg, transparent, ${mix(T.bg0, "#ffffff", 0.22)}, transparent)` }} />
      {/* chip */}
      <div style={{ position: "absolute", left: w * 0.09, top: h * 0.30, width: w * 0.14, height: w * 0.11,
        borderRadius: w * 0.02, background: `linear-gradient(135deg, ${A.money}, ${mix(A.money, T.bg0, 0.4)})`,
        border: `1.5px solid ${mix(A.money, "#000", 0.2)}` }} />
      {/* contactless waves */}
      <div style={{ position: "absolute", left: w * 0.26, top: h * 0.31, fontSize: w * 0.09, color: mix(color, "#fff", 0.3), opacity: 0.8 }}>›))</div>
      {/* number */}
      <div style={{ position: "absolute", left: w * 0.09, top: h * 0.56, fontFamily: MONO, fontWeight: 700,
        fontSize: w * 0.058, letterSpacing: 2, color: mix(T.text, color, 0.2) }}>
        4829  ••••  ••••  7310
      </div>
      {/* label + brand */}
      <div style={{ position: "absolute", left: w * 0.09, top: h * 0.76, fontFamily: SANS, fontWeight: 700, fontSize: w * 0.05, color: T.text }}>
        {label || "MY CARD"}
      </div>
      <div style={{ position: "absolute", right: w * 0.08, bottom: h * 0.09, fontFamily: SANS, fontWeight: 800, fontSize: w * 0.075, color: mix(color, "#fff", 0.25) }}>
        {brand}
      </div>
    </div>
  );
};

// cc_title -------------------------------------------------------------------
const TitleScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const pop = usePop(dur);
  return (
    <AbsoluteFill style={{ alignItems: "center", justifyContent: "center" }}>
      {/* ambient: orbiting ₹ money dots — continuous */}
      {Array.from({ length: 12 }).map((_, i) => {
        const ang = frame * 0.01 + (i / 12) * Math.PI * 2;
        return (
          <div key={i} style={{
            position: "absolute", left: 960 + Math.cos(ang) * (600 + i * 12) - 12,
            top: 540 + Math.sin(ang) * (270 + i * 7) - 12, width: 24, height: 24,
            fontFamily: MONO, fontWeight: 800, fontSize: 22, textAlign: "center",
            color: i % 2 ? A.good : A.money, opacity: 0.18 + rnd(i, 3) * 0.25,
            textShadow: `0 0 12px ${i % 2 ? A.good : A.money}`,
          }}>₹</div>
        );
      })}
      <CardMotif x={1230} y={250} w={470} color={A.card} o={p(0.1, 0.24)} label="CREDIT" brand="RuPay" />
      <div style={{ textAlign: "center", transform: `scale(${0.92 + pop(0) * 0.08})`, zIndex: 2 }}>
        <div style={{ display: "flex", justifyContent: "center", marginBottom: 26 }}>
          <Kicker theme={T} text="పూర్తి కోర్సు · భారతదేశం 2026" cx />
        </div>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 118, lineHeight: 1.05, letterSpacing: -2, color: T.text }}>
          <div>క్రెడిట్ కార్డ్</div>
          <div style={{ color: A.card, textShadow: `0 0 70px ${mix(T.bg0, A.card, 0.7)}` }}>పూర్తి గైడ్</div>
        </div>
        <div style={{ height: 6, width: interpolate(p(0.18, 0.45), [0, 1], [0, 560]), background: `linear-gradient(90deg, ${A.card}, ${A.fin})`, borderRadius: 3, margin: "30px auto" }} />
        <div style={{ fontFamily: SANS, fontSize: 36, color: T.muted, opacity: p(0.28, 0.5) }}>
          అర్థం · ఉపయోగం · లాభాలు · తప్పులు — అన్నీ ఒకే చోట
        </div>
      </div>
    </AbsoluteFill>
  );
};

// cc_hook — India's card boom: powerful tool OR debt trap ---------------------
const HookScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  return (
    <Stage>
      <Head theme={T} kicker="ఎందుకు ఇది ముఖ్యం" title="భారతదేశంలో క్రెడిట్ కార్డ్ విప్లవం" o={p(0, 0.06)} />
      {/* two big stats */}
      <div style={{ position: "absolute", left: 130, top: 250, width: 790, textAlign: "center", opacity: p(0.1, 0.2) }}>
        <div style={{ fontFamily: MONO, fontSize: 26, color: T.muted, marginBottom: 10 }}>చెలామణిలో ఉన్న కార్డులు</div>
        <div><Counter p={p(0.16, 0.5)} to={11.49} decimals={2} suffix=" కోట్లు" color={A.card} size={96} /></div>
      </div>
      <div style={{ position: "absolute", left: 990, top: 250, width: 790, textAlign: "center", opacity: p(0.24, 0.34) }}>
        <div style={{ fontFamily: MONO, fontSize: 26, color: T.muted, marginBottom: 10 }}>మొత్తం బాకీ (Aug 2025)</div>
        <div style={{ fontFamily: MONO, fontWeight: 800, fontSize: 96, color: A.money }}>
          ₹{(2.88 * Math.max(0, Math.min(1, p(0.3, 0.6)))).toFixed(2)}<span style={{ fontSize: 46 }}> లక్షల కోట్లు</span>
        </div>
      </div>
      {/* the contrast: tool vs trap */}
      <div style={{ position: "absolute", left: 130, top: 520, width: 790, height: 250, borderRadius: 20, background: mix(T.panel, A.good, 0.08), border: `2.5px solid ${A.good}`, padding: "26px 30px", boxSizing: "border-box", opacity: p(0.5, 0.6) }}>
        <div style={{ fontSize: 46, marginBottom: 10 }}>✅</div>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 40, color: A.good }}>శక్తివంతమైన సాధనం</div>
        <div style={{ fontFamily: SANS, fontSize: 27, color: T.text, marginTop: 8, lineHeight: 1.35 }}>సరిగ్గా వాడితే — రివార్డ్స్, భద్రత, మంచి క్రెడిట్ స్కోర్.</div>
      </div>
      <div style={{ position: "absolute", left: 990, top: 520, width: 790, height: 250, borderRadius: 20, background: mix(T.panel, A.bad, 0.08), border: `2.5px solid ${A.bad}`, padding: "26px 30px", boxSizing: "border-box", opacity: p(0.62, 0.72), boxShadow: `0 0 ${30 + Math.sin(frame * 0.08) * 12}px ${mix(T.bg0, A.bad, 0.3)}` }}>
        <div style={{ fontSize: 46, marginBottom: 10 }}>⚠️</div>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 40, color: A.bad }}>లేదా అప్పు ఉచ్చు</div>
        <div style={{ fontFamily: SANS, fontSize: 27, color: T.text, marginTop: 8, lineHeight: 1.35 }}>తప్పుగా వాడితే — 45% వరకు వడ్డీతో ఎప్పటికీ తీరని అప్పు.</div>
      </div>
    </Stage>
  );
};

// cc_whatis — borrow now, pay later; the bank's money; the limit --------------
const WhatIsScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur);
  const bankX = 150, youX = 780, shopX = 1410, y = 470;
  return (
    <Stage>
      <Head theme={T} kicker="పాఠం 1 · ప్రాథమికాంశం" title="క్రెడిట్ కార్డ్ అంటే ఏమిటి?" o={p(0, 0.06)} />
      {/* bank -> you (credit line) -> shop (spend) */}
      <Wire x1={bankX + 300} y1={y + 80} x2={youX - 12} y2={y + 80} p={p(0.24, 0.32)} color={A.money} w={4} />
      <Flow x1={bankX + 300} y1={y + 80} x2={youX - 12} y2={y + 80} color={A.money} n={6} o={p(0.3, 0.4)} />
      <Wire x1={youX + 300} y1={y + 80} x2={shopX - 12} y2={y + 80} p={p(0.5, 0.58)} color={A.card} w={4} />
      <Flow x1={youX + 300} y1={y + 80} x2={shopX - 12} y2={y + 80} color={A.card} n={6} o={p(0.56, 0.64)} />

      <Card theme={T} x={bankX} y={y} w={300} h={200} color={A.money} o={p(0.1, 0.2)} glow>
        <div style={{ fontSize: 46 }}>🏦</div>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 34, color: A.money, marginTop: 8 }}>బ్యాంకు</div>
        <div style={{ fontFamily: SANS, fontSize: 23, color: T.muted, marginTop: 4 }}>డబ్బు దీని నుండే</div>
      </Card>
      <Card theme={T} x={youX} y={y} w={300} h={200} color={A.card} o={p(0.36, 0.46)} glow>
        <div style={{ fontSize: 46 }}>💳</div>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 34, color: A.card, marginTop: 8 }}>మీరు + కార్డ్</div>
        <div style={{ fontFamily: SANS, fontSize: 23, color: T.muted, marginTop: 4 }}>ఇప్పుడు కొనండి</div>
      </Card>
      <Card theme={T} x={shopX} y={y} w={300} h={200} color={A.good} o={p(0.62, 0.72)} glow>
        <div style={{ fontSize: 46 }}>🛍️</div>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 34, color: A.good, marginTop: 8 }}>వర్తకుడు</div>
        <div style={{ fontFamily: SANS, fontSize: 23, color: T.muted, marginTop: 4 }}>వెంటనే చెల్లింపు</div>
      </Card>
      <div style={{ position: "absolute", left: 150, top: 730, width: 1560, textAlign: "center", opacity: p(0.74, 0.84) }}>
        <span style={{ fontFamily: SANS, fontWeight: 700, fontSize: 32, color: T.text }}>
          కార్డ్ = బ్యాంకు ఇచ్చే <span style={{ color: A.money }}>ముందస్తు అప్పు</span>. మీరు <span style={{ color: A.card }}>ఇప్పుడు</span> కొంటారు, డబ్బు <span style={{ color: A.bad }}>తర్వాత</span> కడతారు.
        </span>
      </div>
    </Stage>
  );
};

// cc_vs — credit vs debit vs UPI ---------------------------------------------
const VsScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const cols = [
    { at: 0.12, x: 140, c: A.card, emoji: "💳", name: "క్రెడిట్ కార్డ్", whose: "బ్యాంకు డబ్బు", when: "నెల తర్వాత", score: "అవును ✓" },
    { at: 0.3, x: 700, c: A.money, emoji: "🏧", name: "డెబిట్ కార్డ్", whose: "మీ డబ్బు", when: "వెంటనే", score: "లేదు ✗" },
    { at: 0.48, x: 1260, c: A.fin, emoji: "📱", name: "UPI", whose: "మీ డబ్బు", when: "వెంటనే", score: "లేదు ✗" },
  ];
  const rows = [
    { k: "ఎవరి డబ్బు?", get: (c: any) => c.whose },
    { k: "ఎప్పుడు చెల్లిస్తారు?", get: (c: any) => c.when },
    { k: "క్రెడిట్ స్కోర్ పెరుగుతుందా?", get: (c: any) => c.score },
  ];
  return (
    <Stage>
      <Head theme={T} kicker="పాఠం 1 · పోలిక" title="క్రెడిట్ vs డెబిట్ vs UPI" o={p(0, 0.06)} />
      {cols.map((col, i) => (
        <Card key={i} theme={T} x={col.x} y={250} w={520} h={560} color={col.c} o={p(col.at, col.at + 0.1)} glow={i === 0}>
          <div style={{ textAlign: "center" }}>
            <div style={{ fontSize: 56 }}>{col.emoji}</div>
            <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 34, color: col.c, marginTop: 6 }}>{col.name}</div>
          </div>
          <div style={{ marginTop: 24, display: "flex", flexDirection: "column", gap: 18 }}>
            {rows.map((r, ri) => (
              <div key={ri} style={{ opacity: p(col.at + 0.06 + ri * 0.04, col.at + 0.12 + ri * 0.04) }}>
                <div style={{ fontFamily: MONO, fontSize: 21, color: T.muted }}>{r.k}</div>
                <div style={{ fontFamily: SANS, fontWeight: 700, fontSize: 30, color: T.text, marginTop: 2 }}>{r.get(col)}</div>
              </div>
            ))}
          </div>
          {i === 0 && (
            <div style={{ position: "absolute", left: 0, right: 0, bottom: -1, height: 8, borderRadius: 4, background: col.c, opacity: 0.5 + Math.sin(frame * 0.08) * 0.3 }} />
          )}
        </Card>
      ))}
    </Stage>
  );
};

// cc_anatomy — the parts of the card -----------------------------------------
const AnatomyScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur);
  const cardX = 250, cardY = 330, cardW = 640;
  const cardH = cardW * 0.63;
  const parts = [
    { at: 0.18, label: "చిప్ (EMV) — సురక్షితం", lx: 920, ly: 430, tx: cardX + cardW * 0.16, ty: cardY + cardH * 0.36 },
    { at: 0.34, label: "16-అంకెల నంబర్", lx: 920, ly: 540, tx: cardX + cardW * 0.35, ty: cardY + cardH * 0.62 },
    { at: 0.5, label: "పేరు · గడువు తేదీ", lx: 920, ly: 650, tx: cardX + cardW * 0.3, ty: cardY + cardH * 0.82 },
    { at: 0.66, label: "నెట్‌వర్క్ — Visa / RuPay / Mastercard", lx: 920, ly: 760, tx: cardX + cardW * 0.82, ty: cardY + cardH * 0.9 },
  ];
  return (
    <Stage>
      <Head theme={T} kicker="పాఠం 1 · కార్డ్ నిర్మాణం" title="కార్డ్‌పై ఏముంటుంది?" o={p(0, 0.06)} />
      <Brackets x={cardX - 26} y={cardY - 26} w={cardW + 52} h={cardH + 52} color={A.card} o={p(0.08, 0.16)} />
      <CardMotif x={cardX} y={cardY} w={cardW} color={A.card} o={p(0.06, 0.16)} label="RAHUL K" brand="VISA" />
      {parts.map((pt, i) => (
        <React.Fragment key={i}>
          <Wire x1={pt.tx} y1={pt.ty} x2={pt.lx - 12} y2={pt.ly + 16} p={p(pt.at, pt.at + 0.07)} color={A.fin} w={2.5} arrow={false} />
          <div style={{ position: "absolute", left: pt.lx, top: pt.ly, width: 720, opacity: p(pt.at + 0.04, pt.at + 0.12) }}>
            <span style={{ fontFamily: SANS, fontWeight: 700, fontSize: 30, color: T.text, background: mix(T.panel, A.fin, 0.12), border: `2px solid ${mix(T.line, A.fin, 0.5)}`, borderRadius: 12, padding: "10px 20px" }}>{pt.label}</span>
          </div>
        </React.Fragment>
      ))}
    </Stage>
  );
};

// cc_swipe — what happens behind a swipe (5-node flow) ------------------------
const SwipeScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const nodes = [
    { at: 0.1, emoji: "🧑", label: "మీరు", sub: "స్వైప్", c: A.card },
    { at: 0.24, emoji: "🏪", label: "వర్తకుడు", sub: "మెషిన్", c: A.good },
    { at: 0.38, emoji: "🔗", label: "అక్వైరర్", sub: "మర్చంట్ బ్యాంకు", c: A.money },
    { at: 0.52, emoji: "🌐", label: "నెట్‌వర్క్", sub: "Visa / RuPay", c: A.fin },
    { at: 0.66, emoji: "🏦", label: "ఇష్యూయర్", sub: "మీ బ్యాంకు", c: A.bad },
  ];
  const y = 430;
  return (
    <Stage>
      <Head theme={T} kicker="పాఠం 1 · లావాదేవీ" title="ఒక స్వైప్ వెనుక ఏం జరుగుతుంది?" o={p(0, 0.06)} />
      {nodes.map((n, i) => {
        const x = 170 + i * 340;
        const active = Math.floor(frame / 20) % nodes.length === i;
        return (
          <React.Fragment key={i}>
            {i > 0 && (
              <>
                <Wire x1={170 + (i - 1) * 340 + 290} y1={y + 90} x2={x - 8} y2={y + 90} p={p(n.at - 0.06, n.at)} color={n.c} w={3} />
                <Flow x1={170 + (i - 1) * 340 + 290} y1={y + 90} x2={x - 8} y2={y + 90} color={n.c} n={4} o={p(n.at, n.at + 0.1)} />
              </>
            )}
            <Card theme={T} x={x} y={y} w={290} h={200} color={n.c} o={p(n.at, n.at + 0.08)}>
              <div style={{ textAlign: "center", transform: `scale(${active && p(0.7, 0.72) > 0.5 ? 1.06 : 1})` }}>
                <div style={{ fontSize: 50 }}>{n.emoji}</div>
                <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 30, color: n.c, marginTop: 6 }}>{n.label}</div>
                <div style={{ fontFamily: MONO, fontSize: 20, color: T.muted, marginTop: 4 }}>{n.sub}</div>
              </div>
            </Card>
          </React.Fragment>
        );
      })}
      <div style={{ position: "absolute", left: 170, top: 700, width: 1580, textAlign: "center", opacity: p(0.76, 0.86) }}>
        <span style={{ fontFamily: SANS, fontSize: 30, color: T.text }}>ఇదంతా <span style={{ color: A.good, fontWeight: 700 }}>2 సెకన్లలో</span> జరుగుతుంది — ఆమోదం తిరిగి వచ్చి, కొనుగోలు పూర్తవుతుంది.</span>
      </div>
    </Stage>
  );
};

// cc_divider — reusable section divider (parameterized) ----------------------
const DividerScene: React.FC<{ dur?: number; n?: number; title?: string; sub?: string; color?: string }> = ({
  dur, n = 1, title = "", sub = "", color = A.card,
}) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  return (
    <Stage>
      <Brackets x={330} y={300} w={1260} h={480} color={color} o={p(0.02, 0.14)} len={54} />
      <ScanBeam theme={T} x={340} y={310} w={1240} h={460} color={color} o={p(0.05, 0.2)} speed={1.6} />
      <CardMotif x={1360} y={330} w={220} color={color} o={p(0.2, 0.34)} label={`PART ${n}`} brand="" />
      <div style={{ position: "absolute", left: 0, right: 0, top: 360, textAlign: "center" }}>
        <div style={{ fontFamily: MONO, fontWeight: 800, fontSize: 34, color, letterSpacing: 10, opacity: p(0.05, 0.15) }}>PART {"0" + n}</div>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 88, color: T.text, letterSpacing: -2, marginTop: 20, opacity: p(0.12, 0.24), transform: `translateY(${(1 - p(0.12, 0.24)) * 30}px)` }}>{title}</div>
        <div style={{ height: 5, width: interpolate(p(0.2, 0.5), [0, 1], [0, 420]), background: color, borderRadius: 3, margin: "26px auto" }} />
        <div style={{ fontFamily: SANS, fontSize: 32, color: T.muted, opacity: p(0.3, 0.45) }}>{sub}</div>
      </div>
      <div style={{ position: "absolute", left: 0, right: 0, top: 860, display: "flex", justifyContent: "center", gap: 16, opacity: p(0.3, 0.45) }}>
        {[1, 2, 3, 4, 5, 6].map((i) => (
          <div key={i} style={{ width: i === n ? 44 : 14, height: 14, borderRadius: 8,
            background: i <= n ? color : mix(T.panel, color, 0.15), border: `1.5px solid ${i <= n ? color : T.line}`,
            opacity: i === n ? 0.7 + Math.sin(frame * 0.1) * 0.3 : 1 }} />
        ))}
      </div>
    </Stage>
  );
};

// cc_recap — reusable recap / end card ---------------------------------------
const RecapScene: React.FC<{ dur?: number; items?: string[]; closer?: string; title?: string }> = ({
  dur, items = [], closer = "క్రెడిట్ కార్డ్ — తెలివిగా వాడితే మిత్రుడు.", title = "ఒక్క చూపులో గుర్తుంచుకోండి",
}) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  return (
    <AbsoluteFill style={{ padding: "60px 130px", justifyContent: "center" }}>
      <div style={{ opacity: p(0, 0.06), textAlign: "center", marginBottom: 26 }}>
        <Kicker theme={T} text="రీక్యాప్ · మొత్తం చిత్రం" cx />
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 60, color: T.text, marginTop: 12, letterSpacing: -1.5 }}>{title}</div>
      </div>
      <div style={{ display: "flex", flexDirection: "column", gap: 12, maxWidth: 1360, margin: "0 auto", width: "100%" }}>
        {items.map((it, i) => {
          const at = 0.06 + i * 0.09;
          const o = p(at, at + 0.07);
          return (
            <div key={i} style={{ display: "flex", alignItems: "center", gap: 18, opacity: o, transform: `translateX(${(1 - o) * -26}px)`, background: mix(T.panel, A.card, 0.05), border: `1.5px solid ${T.line}`, borderLeft: `4px solid ${A.card}`, borderRadius: 12, padding: "14px 26px" }}>
              <span style={{ color: A.card, fontFamily: MONO, fontWeight: 700, fontSize: 26 }}>{i + 1}</span>
              <span style={{ fontFamily: SANS, fontSize: 29, color: T.text, lineHeight: 1.25 }}>{it}</span>
            </div>
          );
        })}
      </div>
      <div style={{ textAlign: "center", marginTop: 30, opacity: p(0.8, 0.9) }}>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontStyle: "italic", fontSize: 40, color: A.card, textShadow: `0 0 ${28 + Math.sin(frame * 0.06) * 14}px ${mix(T.bg0, A.card, 0.7)}` }}>{closer}</div>
      </div>
    </AbsoluteFill>
  );
};

// cc_billing — the billing-cycle RING (motif) + explanation panel ------------
const BillingScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const cx = 600, cy = 540, R = 205;
  const C = 2 * Math.PI * R;
  const ringDraw = p(0.16, 0.4);
  const graceFrac = 0.62;
  const graceDraw = p(0.5, 0.72);
  const ang = -Math.PI / 2 + ((frame * 0.02) % (Math.PI * 2)); // orbiting "today"
  const mx = cx + Math.cos(ang) * R, my = cy + Math.sin(ang) * R;
  const dueAng = -Math.PI / 2 + graceFrac * Math.PI * 2;
  const dux = cx + Math.cos(dueAng) * R, duy = cy + Math.sin(dueAng) * R;
  return (
    <Stage>
      <Head theme={T} kicker="పాఠం 2 · మెకానిక్స్" title="బిల్లింగ్ సైకిల్ ఎలా పనిచేస్తుంది?" o={p(0, 0.06)} />
      <svg width={1920} height={1080} style={{ position: "absolute", left: 0, top: 0, overflow: "visible" }}>
        <circle cx={cx} cy={cy} r={R} fill="none" stroke={mix(T.bg2, A.card, 0.55)} strokeWidth={14}
          strokeDasharray={C} strokeDashoffset={(1 - ringDraw) * C}
          transform={`rotate(-90 ${cx} ${cy})`} strokeLinecap="round" />
        <circle cx={cx} cy={cy} r={R} fill="none" stroke={A.good} strokeWidth={16}
          strokeDasharray={`${graceFrac * C * graceDraw} ${C * 2}`}
          transform={`rotate(-90 ${cx} ${cy})`} strokeLinecap="round" opacity={0.9} />
      </svg>
      <div style={{ position: "absolute", left: cx - 160, top: cy - 48, width: 320, textAlign: "center", opacity: p(0.22, 0.32) }}>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 46, color: T.text }}>≈30 రోజులు</div>
        <div style={{ fontFamily: MONO, fontSize: 22, color: T.muted, marginTop: 4 }}>1 బిల్లింగ్ సైకిల్</div>
      </div>
      <div style={{ position: "absolute", left: cx - 12, top: cy - R - 12, width: 24, height: 24, borderRadius: 12, background: A.card, boxShadow: `0 0 16px ${A.card}`, opacity: p(0.3, 0.4) }} />
      <div style={{ position: "absolute", left: cx - 140, top: cy - R - 66, width: 280, textAlign: "center", fontFamily: SANS, fontWeight: 700, fontSize: 25, color: A.card, opacity: p(0.32, 0.42) }}>స్టేట్‌మెంట్ తేదీ</div>
      <div style={{ position: "absolute", left: dux - 14, top: duy - 14, width: 28, height: 28, borderRadius: 14, background: A.bad, boxShadow: `0 0 16px ${A.bad}`, opacity: p(0.56, 0.66) }} />
      <div style={{ position: "absolute", left: dux - 150, top: duy + 24, width: 150, textAlign: "right", fontFamily: SANS, fontWeight: 700, fontSize: 24, color: A.bad, opacity: p(0.58, 0.68) }}>గడువు తేదీ</div>
      <div style={{ position: "absolute", left: mx - 9, top: my - 9, width: 18, height: 18, borderRadius: 9, background: T.text, boxShadow: `0 0 14px ${T.text}`, opacity: p(0.4, 0.5) }} />
      <div style={{ position: "absolute", left: 1030, top: 300, width: 760 }}>
        {[
          { at: 0.3, c: A.card, k: "స్టేట్‌మెంట్ తేదీ", v: "నెల ఖర్చులన్నీ కలిపి బిల్లు తయారవుతుంది" },
          { at: 0.5, c: A.bad, k: "గడువు తేదీ · Due Date", v: "18–21 రోజుల తర్వాత — కట్టాల్సిన చివరి రోజు" },
          { at: 0.66, c: A.good, k: "గ్రేస్ పీరియడ్", v: "ఈ మధ్యలో వడ్డీ ఉండదు (పూర్తిగా కడితే)" },
        ].map((r, i) => {
          const o = p(r.at, r.at + 0.1);
          return (
            <div key={i} style={{ marginBottom: 22, opacity: o, transform: `translateX(${(1 - o) * 24}px)`, background: mix(T.panel, r.c, 0.08), borderLeft: `5px solid ${r.c}`, borderRadius: 12, padding: "18px 24px" }}>
              <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 30, color: r.c }}>{r.k}</div>
              <div style={{ fontFamily: SANS, fontSize: 25, color: T.text, marginTop: 6, lineHeight: 1.35 }}>{r.v}</div>
            </div>
          );
        })}
      </div>
    </Stage>
  );
};

// cc_grace — interest-free window timeline + the purchase-timing trick --------
const GraceScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const X0 = 180, W = 1560, y = 360;
  const greenW = W * 0.82 * p(0.28, 0.52);
  return (
    <Stage>
      <Head theme={T} kicker="పాఠం 2 · మెకానిక్స్" title="వడ్డీ లేని గ్రేస్ పీరియడ్" color={A.good} o={p(0, 0.06)} />
      <div style={{ position: "absolute", left: X0, top: y, width: W, height: 6, background: mix(T.line, A.card, 0.4), borderRadius: 3, opacity: p(0.1, 0.2) }} />
      <div style={{ position: "absolute", left: X0, top: y - 9, width: greenW, height: 24, borderRadius: 12, background: `linear-gradient(90deg, ${A.good}, ${mix(A.good, T.bg1, 0.4)})`, boxShadow: `0 0 24px ${mix(T.bg0, A.good, 0.4)}`, opacity: p(0.28, 0.38) }} />
      <div style={{ position: "absolute", left: X0, top: y - 58, fontFamily: SANS, fontWeight: 700, fontSize: 24, color: A.card, opacity: p(0.3, 0.4) }}>కొనుగోలు</div>
      <div style={{ position: "absolute", left: X0 + W * 0.82 - 90, top: y - 58, width: 180, textAlign: "center", fontFamily: SANS, fontWeight: 700, fontSize: 24, color: A.bad, opacity: p(0.44, 0.54) }}>గడువు తేదీ</div>
      <div style={{ position: "absolute", left: X0, top: y + 34, width: W * 0.82, textAlign: "center", fontFamily: SANS, fontWeight: 800, fontSize: 34, color: A.good, opacity: p(0.5, 0.6) }}>50 రోజుల వరకు వడ్డీ లేదు</div>
      {/* timing trick: two examples */}
      {[
        { at: 0.6, c: A.good, k: "స్టేట్‌మెంట్ మరుసటి రోజు కొంటే", v: "≈ 48 రోజులు ఉచిత సమయం", emoji: "👍" },
        { at: 0.72, c: A.money, k: "స్టేట్‌మెంట్ ముందు రోజు కొంటే", v: "≈ 19 రోజులు మాత్రమే", emoji: "⏳" },
      ].map((r, i) => {
        const o = p(r.at, r.at + 0.1);
        return (
          <Card key={i} theme={T} x={180 + i * 800} y={560} w={760} h={220} color={r.c} o={o}>
            <div style={{ fontSize: 44 }}>{r.emoji}</div>
            <div style={{ fontFamily: SANS, fontWeight: 700, fontSize: 28, color: T.text, marginTop: 8 }}>{r.k}</div>
            <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 34, color: r.c, marginTop: 6 }}>{r.v}</div>
          </Card>
        );
      })}
      <div style={{ position: "absolute", left: 180, top: 810, width: 1560, textAlign: "center", opacity: p(0.82, 0.9) }}>
        <span style={{ fontFamily: SANS, fontWeight: 700, fontSize: 28, color: A.bad }}>గుర్తుంచుకోండి: బిల్లు పూర్తిగా కడితేనే ఈ గ్రేస్ పీరియడ్ వర్తిస్తుంది.</span>
      </div>
    </Stage>
  );
};

// cc_mindue — the minimum-due amount and why it's a trap ----------------------
const MinDueScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur);
  return (
    <Stage>
      <Head theme={T} kicker="పాఠం 2 · మెకానిక్స్" title="కనీస మొత్తం — మినిమం డ్యూ" color={A.bad} o={p(0, 0.06)} />
      {/* the bill */}
      <Card theme={T} x={140} y={250} w={620} h={520} color={A.card} o={p(0.1, 0.2)} glow>
        <div style={{ fontFamily: MONO, fontSize: 24, color: T.muted }}>మీ బిల్లు</div>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "baseline", marginTop: 20 }}>
          <span style={{ fontFamily: SANS, fontSize: 30, color: T.text }}>టోటల్ డ్యూ</span>
          <span style={{ fontFamily: MONO, fontWeight: 800, fontSize: 44, color: A.card }}>₹50,000</span>
        </div>
        <div style={{ height: 2, background: T.line, margin: "26px 0" }} />
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "baseline", opacity: p(0.24, 0.34) }}>
          <span style={{ fontFamily: SANS, fontSize: 30, color: A.bad }}>మినిమం డ్యూ (5%)</span>
          <span style={{ fontFamily: MONO, fontWeight: 800, fontSize: 44, color: A.bad }}>₹2,500</span>
        </div>
        <div style={{ marginTop: 30, fontFamily: SANS, fontSize: 25, color: T.muted, lineHeight: 1.4, opacity: p(0.34, 0.44) }}>
          చాలామంది ఈ ₹2,500 కడితే సరిపోతుందని అనుకుంటారు.
        </div>
      </Card>
      {/* two outcomes */}
      <Card theme={T} x={820} y={250} w={960} h={240} color={A.good} o={p(0.46, 0.56)}>
        <div style={{ display: "flex", alignItems: "center", gap: 16 }}>
          <div style={{ fontSize: 48 }}>✅</div>
          <div>
            <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 34, color: A.good }}>పూర్తిగా ₹50,000 కడితే</div>
            <div style={{ fontFamily: SANS, fontSize: 27, color: T.text, marginTop: 6 }}>వడ్డీ = ₹0. క్రెడిట్ స్కోర్ మెరుగవుతుంది.</div>
          </div>
        </div>
      </Card>
      <Card theme={T} x={820} y={530} w={960} h={240} color={A.bad} o={p(0.64, 0.74)} glow>
        <div style={{ display: "flex", alignItems: "center", gap: 16 }}>
          <div style={{ fontSize: 48 }}>⚠️</div>
          <div>
            <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 34, color: A.bad }}>మినిమం ₹2,500 మాత్రమే కడితే</div>
            <div style={{ fontFamily: SANS, fontSize: 27, color: T.text, marginTop: 6 }}>మిగిలిన ₹47,500 పై భారీ వడ్డీ మొదలు.</div>
          </div>
        </div>
      </Card>
    </Stage>
  );
};

// cc_interest — COMPUTED: minimum-due amortization on ₹50,000 at 3.5%/mo ------
const AMORT = (() => {
  let bal = 50000; const rate = 0.035; const bals: number[] = []; let interest = 0;
  for (let m = 0; m < 24; m++) {
    bals.push(bal);
    const intr = bal * rate; interest += intr;
    const pay = Math.max(bal * 0.05, 200);
    bal = Math.max(0, bal + intr - pay);
  }
  return { bals, interest: Math.round(interest), maxBal: 50000 };
})();

const InterestScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const X0 = 200, Yb = 720, BW = 54, GAPX = 63, HMAX = 380;
  const reveal = p(0.2, 0.75);
  const shown = Math.round(AMORT.bals.length * reveal);
  return (
    <Stage>
      <Head theme={T} kicker="పాఠం 2 · నిజం" title="మినిమం డ్యూ కడితే ఏమవుతుంది? (₹50,000)" color={A.bad} o={p(0, 0.06)} />
      {/* baseline */}
      <div style={{ position: "absolute", left: X0 - 10, top: Yb, width: AMORT.bals.length * GAPX + 20, height: 3, background: T.line }} />
      {AMORT.bals.map((b, i) => {
        const on = i < shown;
        const h = (b / AMORT.maxBal) * HMAX;
        return (
          <div key={i} style={{ position: "absolute", left: X0 + i * GAPX, top: Yb - h, width: BW, height: h,
            borderRadius: "6px 6px 0 0", background: `linear-gradient(180deg, ${A.bad}, ${mix(A.bad, T.bg1, 0.5)})`,
            border: `1.5px solid ${A.bad}`, opacity: on ? 1 : 0 }} />
        );
      })}
      {/* x labels */}
      <div style={{ position: "absolute", left: X0, top: Yb + 14, fontFamily: MONO, fontSize: 22, color: T.muted, opacity: p(0.22, 0.3) }}>నెల 1</div>
      <div style={{ position: "absolute", left: X0 + 23 * GAPX - 30, top: Yb + 14, fontFamily: MONO, fontSize: 22, color: T.muted, opacity: p(0.5, 0.58) }}>నెల 24</div>
      {/* remaining balance callout */}
      <div style={{ position: "absolute", left: 200, top: 250, width: 1520, display: "flex", gap: 60, opacity: p(0.62, 0.72) }}>
        <div>
          <div style={{ fontFamily: MONO, fontSize: 24, color: T.muted }}>24 నెలల తర్వాత మిగిలిన అప్పు</div>
          <div style={{ fontFamily: MONO, fontWeight: 800, fontSize: 52, color: A.bad }}>≈ ₹{Math.round(AMORT.bals[23]).toLocaleString("en-IN")}</div>
        </div>
        <div>
          <div style={{ fontFamily: MONO, fontSize: 24, color: T.muted }}>ఈ 2 ఏళ్లలో కట్టిన వడ్డీ</div>
          <div style={{ fontFamily: MONO, fontWeight: 800, fontSize: 52, color: A.money }}>
            ≈ ₹<Counter p={p(0.5, 0.8)} to={AMORT.interest} color={A.money} size={52} />
          </div>
        </div>
      </div>
      <div style={{ position: "absolute", left: 200, top: 800, width: 1520, textAlign: "center", opacity: p(0.84, 0.92) }}>
        <span style={{ fontFamily: SANS, fontWeight: 700, fontSize: 28, color: T.text }}>అసలు దాదాపు తగ్గలేదు — <span style={{ color: A.bad }}>వడ్డీ మాత్రం పేరుకుపోతోంది.</span></span>
      </div>
    </Stage>
  );
};

// cc_fees — the fees you must know (grid + chase highlight) -------------------
const FeesScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const fees = [
    { emoji: "📅", k: "వార్షిక ఫీజు", v: "₹0 – ₹10,000", c: A.money },
    { emoji: "⏰", k: "లేట్ పేమెంట్", v: "₹100 – ₹1,300", c: A.bad },
    { emoji: "✈️", k: "ఫారెక్స్ మార్కప్", v: "2% – 3.5%", c: A.fin },
    { emoji: "🏧", k: "క్యాష్ అడ్వాన్స్", v: "2.5% + వడ్డీ", c: A.bad },
    { emoji: "🧾", k: "GST", v: "18%", c: A.card },
    { emoji: "🚫", k: "ఓవర్-లిమిట్", v: "₹500+", c: A.money },
  ];
  const hot = Math.floor(frame / 24) % fees.length;
  return (
    <Stage>
      <Head theme={T} kicker="పాఠం 2 · ఫీజులు" title="తెలుసుకోవాల్సిన ఫీజులు" color={A.money} o={p(0, 0.06)} />
      {fees.map((f, i) => {
        const col = i % 3, row = Math.floor(i / 3);
        const x = 140 + col * 560, y = 250 + row * 290;
        const o = p(0.1 + i * 0.07, 0.18 + i * 0.07);
        const active = hot === i && p(0.72, 0.74) > 0.5;
        return (
          <div key={i} style={{ position: "absolute", left: x, top: y, width: 520, height: 250, borderRadius: 18,
            background: mix(T.panel, f.c, active ? 0.2 : 0.08), border: `2.5px solid ${active ? f.c : mix(T.line, f.c, 0.5)}`,
            padding: "26px 30px", boxSizing: "border-box", opacity: o, transform: `translateY(${(1 - o) * 22}px) scale(${active ? 1.03 : 1})`,
            boxShadow: active ? `0 0 40px ${mix(T.bg0, f.c, 0.4)}` : "none" }}>
            <div style={{ fontSize: 46 }}>{f.emoji}</div>
            <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 32, color: T.text, marginTop: 10 }}>{f.k}</div>
            <div style={{ fontFamily: MONO, fontWeight: 800, fontSize: 34, color: f.c, marginTop: 8 }}>{f.v}</div>
          </div>
        );
      })}
    </Stage>
  );
};

// cc_cibil — CIBIL score gauge (300–900 speedometer) -------------------------
const CibilScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur);
  const cx = 960, cy = 640, R = 300, N = 44;
  const targetFrac = (780 - 300) / 600; // 0.8
  const needleFrac = targetFrac * p(0.3, 0.66);
  const zoneColor = (f: number) => (f < 0.417 ? A.bad : f < 0.583 ? A.money : f < 0.75 ? A.card : A.good);
  const nAng = Math.PI - needleFrac * Math.PI;
  const nx = cx + Math.cos(nAng) * (R - 40), ny = cy - Math.sin(nAng) * (R - 40);
  return (
    <Stage>
      <Head theme={T} kicker="పాఠం 3 · క్రెడిట్ స్కోర్" title="CIBIL స్కోర్ అంటే ఏమిటి?" color={A.fin} o={p(0, 0.06)} />
      {Array.from({ length: N + 1 }).map((_, i) => {
        const f = i / N;
        const ang = Math.PI - f * Math.PI;
        const on = p(0.12, 0.4) > f * 0.9;
        const x1 = cx + Math.cos(ang) * (R - 22), y1 = cy - Math.sin(ang) * (R - 22);
        const x2 = cx + Math.cos(ang) * R, y2 = cy - Math.sin(ang) * R;
        return <svg key={i} width={1920} height={1080} style={{ position: "absolute", left: 0, top: 0 }}>
          <line x1={x1} y1={y1} x2={x2} y2={y2} stroke={zoneColor(f)} strokeWidth={7} opacity={on ? 0.9 : 0.12} strokeLinecap="round" />
        </svg>;
      })}
      {/* needle */}
      <svg width={1920} height={1080} style={{ position: "absolute", left: 0, top: 0 }}>
        <line x1={cx} y1={cy} x2={nx} y2={ny} stroke={T.text} strokeWidth={6} strokeLinecap="round" />
        <circle cx={cx} cy={cy} r={14} fill={T.text} />
      </svg>
      {/* center readout */}
      <div style={{ position: "absolute", left: cx - 260, top: cy + 40, width: 520, textAlign: "center", opacity: p(0.34, 0.44) }}>
        <div><Counter p={p(0.3, 0.66)} to={780} color={A.good} size={92} /></div>
        <div style={{ fontFamily: MONO, fontSize: 24, color: T.muted, marginTop: 4 }}>300 – 900 · TransUnion CIBIL</div>
      </div>
      {/* legend */}
      <div style={{ position: "absolute", left: 0, right: 0, top: 858, display: "flex", justifyContent: "center", gap: 22, opacity: p(0.6, 0.72) }}>
        {[{ k: "పేలవం", c: A.bad }, { k: "సాధారణం", c: A.money }, { k: "మంచిది", c: A.card }, { k: "750+ అద్భుతం", c: A.good }].map((z, i) => (
          <span key={i} style={{ fontFamily: SANS, fontWeight: 700, fontSize: 26, color: z.c, background: mix(T.panel, z.c, 0.12), border: `2px solid ${z.c}`, borderRadius: 999, padding: "8px 22px" }}>{z.k}</span>
        ))}
      </div>
    </Stage>
  );
};

// cc_util — credit utilization meter (keep < 30%) ----------------------------
const UtilScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const X0 = 300, W = 1320, y = 430, H = 66;
  const fill = W * 0.25 * p(0.28, 0.5); // spent 25% of limit
  const thr = X0 + W * 0.3;
  return (
    <Stage>
      <Head theme={T} kicker="పాఠం 3 · క్రెడిట్ స్కోర్" title="క్రెడిట్ యుటిలైజేషన్ — 30% నియమం" color={A.fin} o={p(0, 0.06)} />
      <div style={{ position: "absolute", left: X0, top: 288, fontFamily: MONO, fontSize: 24, color: T.muted, opacity: p(0.12, 0.2) }}>లిమిట్ ₹1,00,000 · వాడింది ₹25,000</div>
      <div style={{ position: "absolute", left: X0, top: y, width: W, height: H, borderRadius: 14, background: mix(T.panel, A.card, 0.06), border: `2px solid ${T.line}`, opacity: p(0.12, 0.2) }} />
      <div style={{ position: "absolute", left: X0, top: y, width: fill, height: H, borderRadius: 14, background: `linear-gradient(90deg, ${A.good}, ${mix(A.good, T.bg1, 0.4)})`, opacity: p(0.28, 0.36) }} />
      {/* 30% threshold */}
      <div style={{ position: "absolute", left: thr, top: y - 26, width: 3, height: H + 52, background: A.bad, opacity: p(0.36, 0.46) }} />
      <div style={{ position: "absolute", left: thr - 70, top: y - 60, width: 140, textAlign: "center", fontFamily: MONO, fontWeight: 700, fontSize: 24, color: A.bad, opacity: p(0.38, 0.48) }}>30% పరిమితి</div>
      {/* counter */}
      <div style={{ position: "absolute", left: X0, top: 540, opacity: p(0.44, 0.54) }}>
        <Counter p={p(0.3, 0.52)} to={25} suffix="%" color={A.good} size={64} />
        <span style={{ fontFamily: SANS, fontWeight: 800, fontSize: 40, color: A.good, marginLeft: 20 }}>ఆరోగ్యకరం ✓</span>
      </div>
      <Card theme={T} x={300} y={650} w={620} h={200} color={A.good} o={p(0.56, 0.66)}>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 30, color: A.good }}>నియమం</div>
        <div style={{ fontFamily: SANS, fontSize: 27, color: T.text, marginTop: 10, lineHeight: 1.35 }}>వాడకాన్ని ఎప్పుడూ లిమిట్‌లో 30% కంటే తక్కువగా ఉంచండి.</div>
      </Card>
      <Card theme={T} x={1000} y={650} w={620} h={200} color={A.bad} o={p(0.7, 0.8)} glow>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 30, color: A.bad }}>₹70,000 వాడితే → 70%</div>
        <div style={{ fontFamily: SANS, fontSize: 27, color: T.text, marginTop: 10, lineHeight: 1.35 }}>స్కోర్ దెబ్బతింటుంది — మీరు డబ్బు కోసం ఇబ్బందిలో ఉన్నారని సంకేతం.</div>
      </Card>
    </Stage>
  );
};

// cc_factors — what moves your CIBIL score (weighted bars) --------------------
const FactorsScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur);
  const factors = [
    { k: "చెల్లింపు చరిత్ర", w: 35, c: A.good },
    { k: "క్రెడిట్ యుటిలైజేషన్", w: 30, c: A.card },
    { k: "క్రెడిట్ వయస్సు", w: 15, c: A.money },
    { k: "క్రెడిట్ మిక్స్", w: 10, c: A.fin },
    { k: "కొత్త ఎంక్వైరీలు", w: 10, c: A.bad },
  ];
  return (
    <Stage>
      <Head theme={T} kicker="పాఠం 3 · క్రెడిట్ స్కోర్" title="స్కోర్‌ను ఏవి నిర్ణయిస్తాయి? (సుమారుగా)" color={A.fin} o={p(0, 0.06)} />
      {factors.map((f, i) => {
        const y = 250 + i * 116;
        const grow = p(0.12 + i * 0.08, 0.26 + i * 0.08);
        const bw = f.w * 26 * grow;
        return (
          <React.Fragment key={i}>
            <div style={{ position: "absolute", left: 140, top: y + 8, width: 380, fontFamily: SANS, fontWeight: 700, fontSize: 30, color: T.text, opacity: p(0.1 + i * 0.08, 0.2 + i * 0.08) }}>{f.k}</div>
            <div style={{ position: "absolute", left: 540, top: y, width: bw, height: 62, borderRadius: 12, background: `linear-gradient(90deg, ${f.c}, ${mix(f.c, T.bg1, 0.45)})`, border: `2px solid ${f.c}` }} />
            <div style={{ position: "absolute", left: 540 + bw + 16, top: y + 8, fontFamily: MONO, fontWeight: 800, fontSize: 30, color: f.c, opacity: grow }}>{f.w}%</div>
          </React.Fragment>
        );
      })}
      <div style={{ position: "absolute", left: 140, top: 850, width: 1640, textAlign: "center", opacity: p(0.82, 0.9) }}>
        <span style={{ fontFamily: SANS, fontWeight: 700, fontSize: 28, color: T.text }}>సకాలంలో బిల్లు కట్టడం, తక్కువ యుటిలైజేషన్ — ఇవే అతి ముఖ్యం.</span>
      </div>
    </Stage>
  );
};

// cc_firstcard — how to get your first card ----------------------------------
const FirstCardScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur);
  const opts = [
    { emoji: "💼", k: "జీతం ఆధారంగా", v: "క్రమమైన ఆదాయం ఉంటే బ్యాంకు కార్డ్ ఇస్తుంది", c: A.card },
    { emoji: "🔒", k: "సెక్యూర్డ్ కార్డ్", v: "FD పెట్టి కార్డ్ — క్రెడిట్ చరిత్ర లేనివారికి", c: A.good },
    { emoji: "👨‍👩‍👦", k: "యాడ్-ఆన్ కార్డ్", v: "కుటుంబ సభ్యుడి కార్డ్‌పై అదనపు కార్డ్", c: A.money },
    { emoji: "🎓", k: "ఎంట్రీ కార్డులు", v: "మొదటి కార్డ్‌కు lifetime-free ఎంపికలు", c: A.fin },
  ];
  return (
    <Stage>
      <Head theme={T} kicker="పాఠం 3 · మొదటి అడుగు" title="మొదటి కార్డ్ ఎలా పొందాలి?" color={A.fin} o={p(0, 0.06)} />
      {opts.map((o, i) => {
        const col = i % 2, row = Math.floor(i / 2);
        const x = 160 + col * 850, y = 250 + row * 290;
        const op = p(0.12 + i * 0.1, 0.24 + i * 0.1);
        return (
          <Card key={i} theme={T} x={x} y={y} w={780} h={250} color={o.c} o={op}>
            <div style={{ display: "flex", alignItems: "center", gap: 20 }}>
              <div style={{ fontSize: 60 }}>{o.emoji}</div>
              <div>
                <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 34, color: o.c }}>{o.k}</div>
                <div style={{ fontFamily: SANS, fontSize: 26, color: T.text, marginTop: 8, lineHeight: 1.35 }}>{o.v}</div>
              </div>
            </div>
          </Card>
        );
      })}
    </Stage>
  );
};

// cc_rewards — rewards & cashback + real card examples -----------------------
const RewardsScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur);
  const cards = [
    { name: "Cashback SBI Card", rate: "5%", note: "ఆన్‌లైన్ ఖర్చులపై", c: A.good },
    { name: "Amazon Pay ICICI", rate: "5%", note: "Prime · lifetime-free", c: A.card },
    { name: "Axis ACE", rate: "5%", note: "బిల్ పేమెంట్‌లపై (GPay)", c: A.money },
  ];
  return (
    <Stage>
      <Head theme={T} kicker="పాఠం 4 · లాభాలు" title="రివార్డ్స్ & క్యాష్‌బ్యాక్" color={A.good} o={p(0, 0.06)} />
      <div style={{ position: "absolute", left: 140, top: 240, width: 1640, textAlign: "center", opacity: p(0.1, 0.2) }}>
        <span style={{ fontFamily: SANS, fontWeight: 700, fontSize: 32, color: T.text }}>
          ప్రతి ఖర్చుకూ కొంత <span style={{ color: A.good }}>తిరిగి వస్తుంది</span> — పాయింట్లు లేదా నేరుగా క్యాష్‌బ్యాక్‌గా.
        </span>
      </div>
      {cards.map((c, i) => {
        const x = 140 + i * 560;
        const o = p(0.24 + i * 0.1, 0.36 + i * 0.1);
        return (
          <Card key={i} theme={T} x={x} y={360} w={520} h={360} color={c.c} o={o} glow={i === 0}>
            <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 30, color: c.c }}>{c.name}</div>
            <div style={{ fontFamily: MONO, fontWeight: 800, fontSize: 92, color: T.text, marginTop: 26 }}>{c.rate}</div>
            <div style={{ fontFamily: SANS, fontSize: 26, color: T.muted, marginTop: 6 }}>క్యాష్‌బ్యాక్</div>
            <div style={{ fontFamily: SANS, fontSize: 26, color: T.text, marginTop: 22, lineHeight: 1.35 }}>{c.note}</div>
          </Card>
        );
      })}
      <div style={{ position: "absolute", left: 140, top: 770, width: 1640, textAlign: "center", opacity: p(0.78, 0.88) }}>
        <span style={{ fontFamily: SANS, fontSize: 27, color: T.muted }}>పాయింట్లను స్టేట్‌మెంట్ క్రెడిట్, వోచర్లు లేదా ప్రయాణంగా మార్చుకోవచ్చు.</span>
      </div>
    </Stage>
  );
};

// cc_nocostemi — the hidden cost of "no cost" EMI (receipt breakdown) ---------
const NoCostEmiScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const lines = [
    { k: "వస్తువు ధర (మీరు అనుకునేది)", v: "₹30,000", c: T.text, at: 0.16 },
    { k: "+ వడ్డీపై 18% GST", v: "₹810", c: A.bad, at: 0.36 },
    { k: "+ ప్రాసెసింగ్ ఫీజు", v: "₹99 – ₹500", c: A.bad, at: 0.5 },
    { k: "+ క్యాష్‌బ్యాక్ రద్దు", v: "నష్టం", c: A.bad, at: 0.62 },
  ];
  return (
    <Stage>
      <Head theme={T} kicker="పాఠం 4 · జాగ్రత్త" title="నో-కాస్ట్ EMI నిజంగా ఉచితమా?" color={A.money} o={p(0, 0.06)} />
      <div style={{ position: "absolute", left: 460, top: 250, width: 1000, borderRadius: 20, background: mix(T.panel, A.money, 0.06), border: `2.5px solid ${mix(T.line, A.money, 0.5)}`, padding: "30px 40px", boxSizing: "border-box" }}>
        {lines.map((l, i) => (
          <div key={i} style={{ display: "flex", justifyContent: "space-between", alignItems: "baseline", padding: "16px 0", borderBottom: `1px solid ${T.line}`, opacity: p(l.at, l.at + 0.08) }}>
            <span style={{ fontFamily: SANS, fontSize: 30, color: T.text }}>{l.k}</span>
            <span style={{ fontFamily: MONO, fontWeight: 800, fontSize: 36, color: l.c }}>{l.v}</span>
          </div>
        ))}
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "baseline", paddingTop: 22, opacity: p(0.74, 0.84) }}>
          <span style={{ fontFamily: SANS, fontWeight: 800, fontSize: 36, color: A.bad }}>= అసలు ఖర్చు</span>
          <span style={{ fontFamily: MONO, fontWeight: 800, fontSize: 52, color: A.bad, textShadow: `0 0 ${20 + Math.sin(frame * 0.08) * 10}px ${mix(T.bg0, A.bad, 0.5)}` }}>₹30,810+</span>
        </div>
      </div>
      <div style={{ position: "absolute", left: 460, top: 800, width: 1000, textAlign: "center", opacity: p(0.86, 0.94) }}>
        <span style={{ fontFamily: SANS, fontWeight: 700, fontSize: 28, color: T.text }}>"నో-కాస్ట్" అనే పేరే — నిజంగా ఉచితం కాదు.</span>
      </div>
    </Stage>
  );
};

// cc_perks — travel / lounge / forex / insurance perks (grid) ----------------
const PerksScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const perks = [
    { emoji: "🛋️", k: "ఎయిర్‌పోర్ట్ లాంజ్", c: A.card },
    { emoji: "⛽", k: "ఫ్యూయల్ సర్‌ఛార్జ్ మినహాయింపు", c: A.money },
    { emoji: "🛡️", k: "ట్రావెల్ ఇన్సూరెన్స్", c: A.good },
    { emoji: "🌐", k: "జీరో-ఫారెక్స్ కార్డులు", c: A.fin },
    { emoji: "⚡", k: "రివార్డ్ యాక్సిలరేటర్లు", c: A.good },
    { emoji: "🛍️", k: "కొనుగోలు రక్షణ", c: A.card },
  ];
  const hot = Math.floor(frame / 24) % perks.length;
  return (
    <Stage>
      <Head theme={T} kicker="పాఠం 4 · లాభాలు" title="వాడుకోవాల్సిన పెర్క్‌లు" color={A.good} o={p(0, 0.06)} />
      {perks.map((f, i) => {
        const col = i % 3, row = Math.floor(i / 3);
        const x = 140 + col * 560, y = 250 + row * 290;
        const o = p(0.1 + i * 0.07, 0.18 + i * 0.07);
        const active = hot === i && p(0.7, 0.72) > 0.5;
        return (
          <div key={i} style={{ position: "absolute", left: x, top: y, width: 520, height: 250, borderRadius: 18,
            background: mix(T.panel, f.c, active ? 0.2 : 0.08), border: `2.5px solid ${active ? f.c : mix(T.line, f.c, 0.5)}`,
            padding: "30px", boxSizing: "border-box", opacity: o, transform: `translateY(${(1 - o) * 22}px) scale(${active ? 1.03 : 1})`,
            display: "flex", flexDirection: "column", justifyContent: "center",
            boxShadow: active ? `0 0 40px ${mix(T.bg0, f.c, 0.4)}` : "none" }}>
            <div style={{ fontSize: 54 }}>{f.emoji}</div>
            <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 32, color: T.text, marginTop: 14, lineHeight: 1.2 }}>{f.k}</div>
          </div>
        );
      })}
    </Stage>
  );
};

// cc_habits — smart-usage checklist ------------------------------------------
const HabitsScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur);
  const habits = [
    "ఆటోపే సెటప్ చేయండి — గడువు తేదీ ఎప్పుడూ మిస్ కాదు",
    "ప్రతి నెలా టోటల్ డ్యూ పూర్తిగా కట్టండి",
    "ప్రతి ఖర్చును యాప్‌లో ట్రాక్ చేయండి",
    "యుటిలైజేషన్ ఎప్పుడూ 30% లోపు ఉంచండి",
    "అనవసర కార్డులు వద్దు — క్రమశిక్షణతో వాడండి",
  ];
  return (
    <Stage>
      <Head theme={T} kicker="పాఠం 4 · అలవాట్లు" title="తెలివైన 5 అలవాట్లు" color={A.good} o={p(0, 0.06)} />
      <div style={{ position: "absolute", left: 300, top: 250, width: 1320, display: "flex", flexDirection: "column", gap: 18 }}>
        {habits.map((h, i) => {
          const at = 0.08 + i * 0.12;
          const o = p(at, at + 0.08);
          return (
            <div key={i} style={{ display: "flex", alignItems: "center", gap: 22, opacity: o, transform: `translateX(${(1 - o) * -26}px)`, background: mix(T.panel, A.good, 0.06), border: `1.5px solid ${T.line}`, borderLeft: `5px solid ${A.good}`, borderRadius: 14, padding: "20px 28px" }}>
              <span style={{ fontSize: 40 }}>✅</span>
              <span style={{ fontFamily: SANS, fontWeight: 600, fontSize: 32, color: T.text }}>{h}</span>
            </div>
          );
        })}
      </div>
    </Stage>
  );
};

// cc_spiral — the debt trap as a vicious cycle (loop of nodes) ---------------
const SpiralScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const nodes = [
    { k: "ఎక్కువ ఖర్చు", emoji: "💸" },
    { k: "పెద్ద బిల్లు", emoji: "🧾" },
    { k: "మినిమం కట్టడం", emoji: "🪙" },
    { k: "వడ్డీ చేరుతుంది", emoji: "📈" },
    { k: "అప్పు పెరుగుతుంది", emoji: "⛓️" },
  ];
  const cx = 960, cy = 540, rx = 430, ry = 265;
  const pos = (i: number) => {
    const ang = -Math.PI / 2 + (i / nodes.length) * Math.PI * 2;
    return { x: cx + Math.cos(ang) * rx, y: cy + Math.sin(ang) * ry };
  };
  const hot = Math.floor(frame / 24) % nodes.length;
  return (
    <Stage>
      <Head theme={T} kicker="పాఠం 5 · తప్పుడు వినియోగం" title="అప్పు ఉచ్చు — వికృత చక్రం" color={A.bad} o={p(0, 0.06)} />
      {nodes.map((n, i) => {
        const a = pos(i), b = pos((i + 1) % nodes.length);
        return <Flow key={"f" + i} x1={a.x} y1={a.y} x2={b.x} y2={b.y} color={A.bad} n={4} o={p(0.4 + i * 0.02, 0.5 + i * 0.02)} />;
      })}
      {nodes.map((n, i) => {
        const a = pos(i), b = pos((i + 1) % nodes.length);
        return <Wire key={"w" + i} x1={a.x} y1={a.y} x2={b.x} y2={b.y} p={p(0.2 + i * 0.06, 0.3 + i * 0.06)} color={mix(A.bad, T.bg1, 0.3)} w={2.5} arrow />;
      })}
      {/* center */}
      <div style={{ position: "absolute", left: cx - 160, top: cy - 60, width: 320, textAlign: "center", opacity: p(0.3, 0.42) }}>
        <div style={{ fontSize: 54 }}>🌀</div>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 40, color: A.bad, textShadow: `0 0 ${24 + Math.sin(frame * 0.09) * 12}px ${mix(T.bg0, A.bad, 0.6)}` }}>అప్పు ఉచ్చు</div>
      </div>
      {nodes.map((n, i) => {
        const a = pos(i);
        const o = p(0.14 + i * 0.06, 0.24 + i * 0.06);
        const active = hot === i && p(0.6, 0.62) > 0.5;
        return (
          <div key={"n" + i} style={{ position: "absolute", left: a.x - 125, top: a.y - 58, width: 250, height: 116, borderRadius: 16,
            background: mix(T.panel, A.bad, active ? 0.2 : 0.1), border: `2.5px solid ${active ? A.bad : mix(T.line, A.bad, 0.5)}`,
            display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", opacity: o, transform: `scale(${active ? 1.06 : 1})` }}>
            <div style={{ fontSize: 34 }}>{n.emoji}</div>
            <div style={{ fontFamily: SANS, fontWeight: 700, fontSize: 25, color: T.text, marginTop: 4 }}>{n.k}</div>
          </div>
        );
      })}
    </Stage>
  );
};

// cc_mintrap — COMPUTED full payoff paying only the minimum on ₹50,000 --------
const TRAP = (() => {
  let bal = 50000, rate = 0.035, months = 0, interest = 0, paid = 0;
  const curve: number[] = [];
  while (bal > 1 && months < 600) {
    if (months % 6 === 0) curve.push(bal);
    const i = bal * rate; interest += i;
    let pay = Math.max(bal * 0.05, 200); if (pay > bal + i) pay = bal + i;
    paid += pay; bal = bal + i - pay; months++;
  }
  return { years: +(months / 12).toFixed(0), paid: Math.round(paid), interest: Math.round(interest), curve };
})();

const MinTrapScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  return (
    <Stage>
      <Head theme={T} kicker="పాఠం 5 · నిజం" title="మినిమం మాత్రమే కడితే? (₹50,000 అప్పు)" color={A.bad} o={p(0, 0.06)} />
      {/* three big stats */}
      {[
        { at: 0.16, k: "అప్పు తీర్చడానికి సమయం", val: TRAP.years, suf: " ఏళ్లు", c: A.bad, big: true },
        { at: 0.4, k: "మొత్తం మీరు కట్టేది", val: TRAP.paid, pre: "₹", c: A.money },
        { at: 0.62, k: "అందులో వడ్డీ మాత్రమే", val: TRAP.interest, pre: "₹", c: A.bad },
      ].map((s, i) => (
        <div key={i} style={{ position: "absolute", left: 140 + i * 560, top: 300, width: 520, textAlign: "center", opacity: p(s.at, s.at + 0.12) }}>
          <div style={{ fontFamily: MONO, fontSize: 25, color: T.muted, marginBottom: 14 }}>{s.k}</div>
          <div style={{ fontFamily: MONO, fontWeight: 800, fontSize: 74, color: s.c }}>
            {s.pre || ""}<Counter p={p(s.at + 0.02, s.at + 0.2)} to={s.val} color={s.c} size={74} />{s.suf || ""}
          </div>
        </div>
      ))}
      <div style={{ position: "absolute", left: 140, top: 560, width: 1640, textAlign: "center", opacity: p(0.72, 0.82) }}>
        <span style={{ fontFamily: SANS, fontWeight: 800, fontSize: 40, color: T.text }}>
          ₹50,000 అప్పు → మీరు కట్టేది <span style={{ color: A.bad }}>₹{TRAP.paid.toLocaleString("en-IN")}</span>
        </span>
      </div>
      <div style={{ position: "absolute", left: 140, top: 680, width: 1640, textAlign: "center", opacity: p(0.82, 0.9) }}>
        <span style={{ fontFamily: SANS, fontSize: 30, color: A.bad, fontWeight: 700, textShadow: `0 0 ${18 + Math.sin(frame * 0.08) * 10}px ${mix(T.bg0, A.bad, 0.5)}` }}>వడ్డీ, అసలు కంటే రెండు రెట్లు ఎక్కువ!</span>
      </div>
    </Stage>
  );
};

// cc_mistakes — cash withdrawal & other costly mistakes ----------------------
const MistakesScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur);
  const items = [
    { emoji: "🏧", k: "నగదు ఉపసంహరణ", v: "గ్రేస్ పీరియడ్ ఉండదు — మొదటి రోజు నుండే వడ్డీ + ఫీజు", c: A.bad },
    { emoji: "🛒", k: "అతిగా ఖర్చు", v: "కార్డ్ డబ్బు 'ఉచితం' అనిపిస్తుంది — అవసరం లేనివీ కొంటారు", c: A.money },
    { emoji: "🪙", k: "మినిమం అలవాటు", v: "ప్రతినెలా మినిమం కడితే = శాశ్వత అప్పు", c: A.bad },
    { emoji: "⏰", k: "లేట్ పేమెంట్", v: "ఫీజు + క్రెడిట్ స్కోర్‌కు దెబ్బ", c: A.money },
  ];
  return (
    <Stage>
      <Head theme={T} kicker="పాఠం 5 · తప్పులు" title="ఖరీదైన తప్పులు" color={A.bad} o={p(0, 0.06)} />
      {items.map((it, i) => {
        const col = i % 2, row = Math.floor(i / 2);
        const x = 160 + col * 850, y = 250 + row * 290;
        const o = p(0.12 + i * 0.1, 0.24 + i * 0.1);
        return (
          <Card key={i} theme={T} x={x} y={y} w={780} h={250} color={it.c} o={o} glow={i === 0}>
            <div style={{ display: "flex", alignItems: "center", gap: 20 }}>
              <div style={{ fontSize: 58 }}>{it.emoji}</div>
              <div>
                <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 34, color: it.c }}>{it.k}</div>
                <div style={{ fontFamily: SANS, fontSize: 26, color: T.text, marginTop: 8, lineHeight: 1.35 }}>{it.v}</div>
              </div>
            </div>
          </Card>
        );
      })}
    </Stage>
  );
};

// cc_escape — escaping debt: rate comparison + steps -------------------------
const EscapeScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur);
  const rates = [
    { k: "క్రెడిట్ కార్డ్ రివాల్వింగ్", v: 42, c: A.bad },
    { k: "EMIగా మార్చడం", v: 16, c: A.money },
    { k: "పర్సనల్ లోన్", v: 13, c: A.good },
  ];
  const steps = [
    "బాకీని EMIగా మార్చండి (12–18%)",
    "పర్సనల్ లోన్‌తో కన్సాలిడేట్ చేయండి",
    "కొత్త ఖర్చులకు కార్డ్ వాడటం ఆపండి",
    "వీలైనంత త్వరగా పూర్తిగా కట్టండి",
  ];
  return (
    <Stage>
      <Head theme={T} kicker="పాఠం 5 · పరిష్కారం" title="అప్పు నుండి ఎలా బయటపడాలి?" color={A.good} o={p(0, 0.06)} />
      {/* comparison bars (left) */}
      {rates.map((r, i) => {
        const y = 280 + i * 150;
        const grow = p(0.14 + i * 0.1, 0.3 + i * 0.1);
        const bw = r.v * 17 * grow;
        return (
          <React.Fragment key={i}>
            <div style={{ position: "absolute", left: 140, top: y - 40, width: 720, fontFamily: SANS, fontWeight: 700, fontSize: 28, color: T.text, opacity: p(0.1 + i * 0.1, 0.2 + i * 0.1) }}>{r.k}</div>
            <div style={{ position: "absolute", left: 140, top: y, width: bw, height: 56, borderRadius: 12, background: `linear-gradient(90deg, ${r.c}, ${mix(r.c, T.bg1, 0.45)})`, border: `2px solid ${r.c}` }} />
            <div style={{ position: "absolute", left: 140 + bw + 16, top: y + 6, fontFamily: MONO, fontWeight: 800, fontSize: 34, color: r.c, opacity: grow }}>{r.v}%</div>
          </React.Fragment>
        );
      })}
      {/* steps (right) */}
      <div style={{ position: "absolute", left: 1010, top: 260, width: 780 }}>
        {steps.map((s, i) => {
          const o = p(0.4 + i * 0.1, 0.5 + i * 0.1);
          return (
            <div key={i} style={{ display: "flex", alignItems: "center", gap: 16, marginBottom: 16, opacity: o, transform: `translateX(${(1 - o) * 24}px)`, background: mix(T.panel, A.good, 0.06), borderLeft: `4px solid ${A.good}`, borderRadius: 12, padding: "16px 22px" }}>
              <span style={{ color: A.good, fontFamily: MONO, fontWeight: 800, fontSize: 26 }}>{i + 1}</span>
              <span style={{ fontFamily: SANS, fontSize: 27, color: T.text }}>{s}</span>
            </div>
          );
        })}
      </div>
    </Stage>
  );
};

// cc_bankcards — the major bank issuers & flagship cards ---------------------
const BankCardsScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur);
  const banks = [
    { name: "SBI Card", c: A.card, cards: ["Cashback — 5% ఆన్‌లైన్", "SimplyCLICK", "SBI Card ELITE"] },
    { name: "HDFC Bank", c: A.good, cards: ["Millennia — 5% ఈ-కామర్స్", "Regalia Gold", "Infinia (invite)"] },
    { name: "ICICI Bank", c: A.money, cards: ["Amazon Pay — LTF", "Coral", "MakeMyTrip"] },
    { name: "Axis Bank", c: A.fin, cards: ["ACE — 5% బిల్ పే", "Flipkart Axis", "Magnus"] },
  ];
  return (
    <Stage>
      <Head theme={T} kicker="పాఠం 6 · భారత మార్కెట్" title="పెద్ద బ్యాంకు కార్డులు" o={p(0, 0.06)} />
      {banks.map((b, i) => {
        const x = 130 + i * 440;
        const o = p(0.1 + i * 0.09, 0.22 + i * 0.09);
        return (
          <Card key={i} theme={T} x={x} y={250} w={390} h={560} color={b.c} o={o} glow={i === 0}>
            <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 32, color: b.c }}>{b.name}</div>
            <div style={{ height: 2, background: mix(T.line, b.c, 0.4), margin: "18px 0" }} />
            {b.cards.map((cd, j) => (
              <div key={j} style={{ display: "flex", gap: 10, marginBottom: 20, opacity: p(0.16 + i * 0.09 + j * 0.03, 0.28 + i * 0.09 + j * 0.03) }}>
                <span style={{ color: b.c, fontSize: 22 }}>▸</span>
                <span style={{ fontFamily: SANS, fontSize: 24, color: T.text, lineHeight: 1.3 }}>{cd}</span>
              </div>
            ))}
          </Card>
        );
      })}
    </Stage>
  );
};

// cc_fintech — OneCard & the Uni cautionary tale -----------------------------
const FintechScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur);
  const one = ["మెటల్ కార్డ్ · lifetime-free (₹0)", "5x రివార్డ్స్ — నెల టాప్-2 కేటగిరీలపై", "1% ఫారెక్స్ మార్కప్", "5-నిమిషాల డిజిటల్ ఆన్‌బోర్డింగ్", "IDFC FIRST / BOB / Federal భాగస్వామ్యంతో"];
  const uni = ["Uni Pay 1/3rd — బిల్లును 3 భాగాలుగా", "2022: RBI నిబంధనలతో సేవలు నిలిపివేత", "ఇప్పుడు GoldX — గోల్డ్ రివార్డ్స్ కార్డ్", "పాఠం: స్టార్టప్ + రెగ్యులేషన్ రిస్క్"];
  return (
    <Stage>
      <Head theme={T} kicker="పాఠం 6 · ఫిన్‌టెక్ కార్డులు" title="OneCard & Uni — కొత్త తరం" color={A.fin} o={p(0, 0.06)} />
      <Card theme={T} x={140} y={240} w={820} h={600} color={A.card} o={p(0.1, 0.2)} glow>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 40, color: A.card }}>OneCard</div>
        <div style={{ fontFamily: MONO, fontSize: 23, color: T.muted, marginTop: 6 }}>మెటల్ · యాప్-ఫస్ట్</div>
        <div style={{ marginTop: 22 }}>
          {one.map((t, i) => (
            <div key={i} style={{ display: "flex", gap: 12, marginBottom: 18, opacity: p(0.24 + i * 0.05, 0.34 + i * 0.05) }}>
              <span style={{ color: A.card, fontSize: 24 }}>▸</span>
              <span style={{ fontFamily: SANS, fontSize: 27, color: T.text, lineHeight: 1.3 }}>{t}</span>
            </div>
          ))}
        </div>
      </Card>
      <Card theme={T} x={1000} y={240} w={780} h={600} color={A.money} o={p(0.16, 0.26)}>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 40, color: A.money }}>Uni</div>
        <div style={{ fontFamily: MONO, fontSize: 23, color: T.muted, marginTop: 6 }}>ఒక హెచ్చరిక కథ</div>
        <div style={{ marginTop: 22 }}>
          {uni.map((t, i) => (
            <div key={i} style={{ display: "flex", gap: 12, marginBottom: 22, opacity: p(0.34 + i * 0.06, 0.44 + i * 0.06) }}>
              <span style={{ color: A.money, fontFamily: MONO, fontWeight: 800, fontSize: 22 }}>{i + 1}</span>
              <span style={{ fontFamily: SANS, fontSize: 27, color: T.text, lineHeight: 1.3 }}>{t}</span>
            </div>
          ))}
        </div>
      </Card>
    </Stage>
  );
};

// cc_choose — match your spending profile to a card type ---------------------
const ChooseScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur);
  const rows = [
    { profile: "ఆన్‌లైన్ షాపింగ్ ఎక్కువ", card: "క్యాష్‌బ్యాక్ కార్డ్", c: A.good, emoji: "🛒" },
    { profile: "తరచూ ప్రయాణం", card: "ట్రావెల్ / లాంజ్ కార్డ్", c: A.card, emoji: "✈️" },
    { profile: "ఇదే మొదటి కార్డ్", card: "lifetime-free ఎంట్రీ కార్డ్", c: A.fin, emoji: "🎓" },
    { profile: "విదేశీ ఖర్చులు ఎక్కువ", card: "జీరో-ఫారెక్స్ కార్డ్", c: A.money, emoji: "🌐" },
  ];
  return (
    <Stage>
      <Head theme={T} kicker="పాఠం 6 · ఎంపిక" title="మీకు ఏ కార్డ్ సరైనది?" o={p(0, 0.06)} />
      {rows.map((r, i) => {
        const y = 260 + i * 150;
        const o = p(0.12 + i * 0.12, 0.24 + i * 0.12);
        return (
          <React.Fragment key={i}>
            <div style={{ position: "absolute", left: 140, top: y, width: 640, height: 110, borderRadius: 16, background: mix(T.panel, r.c, 0.06), border: `2px solid ${mix(T.line, r.c, 0.5)}`, display: "flex", alignItems: "center", gap: 18, padding: "0 26px", boxSizing: "border-box", opacity: o }}>
              <span style={{ fontSize: 44 }}>{r.emoji}</span>
              <span style={{ fontFamily: SANS, fontWeight: 700, fontSize: 30, color: T.text }}>{r.profile}</span>
            </div>
            <Wire x1={790} y1={y + 55} x2={988} y2={y + 55} p={p(0.16 + i * 0.12, 0.24 + i * 0.12)} color={r.c} w={3} />
            <div style={{ position: "absolute", left: 1000, top: y, width: 780, height: 110, borderRadius: 16, background: mix(T.panel, r.c, 0.14), border: `2.5px solid ${r.c}`, display: "flex", alignItems: "center", padding: "0 30px", boxSizing: "border-box", opacity: p(0.2 + i * 0.12, 0.3 + i * 0.12) }}>
              <span style={{ fontFamily: SANS, fontWeight: 800, fontSize: 34, color: r.c }}>{r.card}</span>
            </div>
          </React.Fragment>
        );
      })}
    </Stage>
  );
};

// cc_ptitle — parameterized title for standalone videos ---------------------
const PTitleScene: React.FC<{ dur?: number; title?: string; sub?: string; kicker?: string }> = ({
  dur, title = "", sub = "", kicker = "క్రెడిట్ కార్డ్ · తెలుగు",
}) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const pop = usePop(dur);
  return (
    <AbsoluteFill style={{ alignItems: "center", justifyContent: "center" }}>
      {Array.from({ length: 12 }).map((_, i) => {
        const ang = frame * 0.01 + (i / 12) * Math.PI * 2;
        return <div key={i} style={{ position: "absolute", left: 960 + Math.cos(ang) * (600 + i * 12) - 12, top: 540 + Math.sin(ang) * (270 + i * 7) - 12, fontFamily: MONO, fontWeight: 800, fontSize: 22, color: i % 2 ? A.good : A.money, opacity: 0.16 + rnd(i, 3) * 0.22, textShadow: `0 0 12px ${i % 2 ? A.good : A.money}` }}>₹</div>;
      })}
      <CardMotif x={1240} y={250} w={450} color={A.card} o={p(0.1, 0.24)} label="CARD" brand="RuPay" />
      <div style={{ textAlign: "center", transform: `scale(${0.92 + pop(0) * 0.08})`, zIndex: 2, maxWidth: 1400 }}>
        <div style={{ display: "flex", justifyContent: "center", marginBottom: 24 }}><Kicker theme={T} text={kicker} cx /></div>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 96, lineHeight: 1.06, letterSpacing: -2, color: T.text }}>{title}</div>
        <div style={{ height: 6, width: interpolate(p(0.18, 0.45), [0, 1], [0, 520]), background: `linear-gradient(90deg, ${A.card}, ${A.fin})`, borderRadius: 3, margin: "28px auto" }} />
        <div style={{ fontFamily: SANS, fontSize: 34, color: T.muted, opacity: p(0.28, 0.5) }}>{sub}</div>
      </div>
    </AbsoluteFill>
  );
};

// cc_cardreview — parameterized single-card review ---------------------------
const CardReviewScene: React.FC<{ dur?: number; name?: string; brand?: string; tagline?: string; color?: string; specs?: { k: string; v: string }[]; forWho?: string }> = ({
  dur, name = "", brand = "", tagline = "", color = A.card, specs = [], forWho = "",
}) => {
  const p = useP(dur);
  const c = color;
  return (
    <Stage>
      <Head theme={T} kicker="కార్డ్ రివ్యూ" title={name} color={c} o={p(0, 0.06)} />
      <CardMotif x={140} y={300} w={620} color={c} o={p(0.08, 0.2)} label={name} brand={brand} />
      <div style={{ position: "absolute", left: 140, top: 720, width: 620, fontFamily: SANS, fontSize: 28, color: T.muted, opacity: p(0.24, 0.34), lineHeight: 1.35 }}>{tagline}</div>
      <div style={{ position: "absolute", left: 860, top: 270, width: 920 }}>
        {specs.map((s, i) => {
          const o = p(0.24 + i * 0.09, 0.34 + i * 0.09);
          return (
            <div key={i} style={{ display: "flex", justifyContent: "space-between", alignItems: "baseline", padding: "18px 0", borderBottom: `1px solid ${T.line}`, opacity: o }}>
              <span style={{ fontFamily: SANS, fontSize: 28, color: T.muted }}>{s.k}</span>
              <span style={{ fontFamily: SANS, fontWeight: 800, fontSize: 32, color: T.text, textAlign: "right", maxWidth: 560 }}>{s.v}</span>
            </div>
          );
        })}
      </div>
      <Card theme={T} x={860} y={660} w={920} h={170} color={c} o={p(0.66, 0.76)} glow>
        <div style={{ fontFamily: MONO, fontSize: 23, color: c }}>ఎవరికి సరైనది</div>
        <div style={{ fontFamily: SANS, fontWeight: 700, fontSize: 30, color: T.text, marginTop: 8, lineHeight: 1.3 }}>{forWho}</div>
      </Card>
    </Stage>
  );
};

// cc_cardcompare — comparison table of the 4 cards ---------------------------
const CardCompareScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur);
  const cols = [
    { name: "OneCard", c: A.card }, { name: "Amazon Pay ICICI", c: A.money },
    { name: "Cashback SBI", c: A.good }, { name: "Axis ACE", c: A.fin },
  ];
  const rows = [
    { k: "వార్షిక ఫీజు", v: ["₹0", "₹0", "₹999*", "₹499"] },
    { k: "రివార్డ్స్", v: ["5x టాప్-2", "5% Amazon", "5% ఆన్‌లైన్", "5% బిల్ పే"] },
    { k: "ఫారెక్స్", v: ["1%", "3.5%", "3.5%", "3.5%"] },
    { k: "బెస్ట్ ఫర్", v: ["ఫారెక్స్ + యాప్", "Amazon షాపింగ్", "ఆన్‌లైన్ ఖర్చు", "బిల్ పేమెంట్"] },
  ];
  const LX = 120, CW = 330, RH = 116, Y0 = 250;
  return (
    <Stage>
      <Head theme={T} kicker="పోలిక" title="4 కార్డులు — పక్కపక్కన" o={p(0, 0.06)} />
      {/* header row */}
      {cols.map((c, j) => (
        <div key={j} style={{ position: "absolute", left: LX + 340 + j * CW, top: Y0, width: CW - 16, height: 84, borderRadius: 12, background: mix(T.panel, c.c, 0.16), border: `2px solid ${c.c}`, display: "flex", alignItems: "center", justifyContent: "center", opacity: p(0.06 + j * 0.04, 0.16 + j * 0.04) }}>
          <span style={{ fontFamily: SANS, fontWeight: 800, fontSize: 26, color: c.c, textAlign: "center" }}>{c.name}</span>
        </div>
      ))}
      {rows.map((r, i) => {
        const y = Y0 + 104 + i * RH;
        return (
          <React.Fragment key={i}>
            <div style={{ position: "absolute", left: LX, top: y, width: 330, height: RH - 14, display: "flex", alignItems: "center", opacity: p(0.14 + i * 0.06, 0.24 + i * 0.06) }}>
              <span style={{ fontFamily: SANS, fontWeight: 700, fontSize: 28, color: T.muted }}>{r.k}</span>
            </div>
            {r.v.map((val, j) => (
              <div key={j} style={{ position: "absolute", left: LX + 340 + j * CW, top: y, width: CW - 16, height: RH - 14, borderRadius: 10, background: mix(T.panel, cols[j].c, 0.05), border: `1px solid ${T.line}`, display: "flex", alignItems: "center", justifyContent: "center", opacity: p(0.16 + i * 0.06 + j * 0.02, 0.26 + i * 0.06 + j * 0.02) }}>
                <span style={{ fontFamily: SANS, fontWeight: 700, fontSize: 26, color: T.text, textAlign: "center" }}>{val}</span>
              </div>
            ))}
          </React.Fragment>
        );
      })}
      <div style={{ position: "absolute", left: 150, top: 850, fontFamily: MONO, fontSize: 20, color: T.muted, opacity: p(0.8, 0.88) }}>* ఫీజు ఖర్చు మైలురాళ్లతో తిరిగి రావచ్చు · వివరాలు మారవచ్చు</div>
    </Stage>
  );
};

// cc_scorebands — the 4 CIBIL score bands and what each means ----------------
const ScoreBandsScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur);
  const bands = [
    { range: "300–549", k: "పేలవం", v: "రుణం రాదు / చాలా ఎక్కువ వడ్డీ", c: A.bad, frac: 0.30 },
    { range: "550–649", k: "సాధారణం", v: "కొన్ని రుణాలు, ఎక్కువ వడ్డీతో", c: A.money, frac: 0.20 },
    { range: "650–749", k: "మంచిది", v: "చాలా రుణాలు ఆమోదం", c: A.card, frac: 0.20 },
    { range: "750–900", k: "అద్భుతం", v: "సులభ ఆమోదం, తక్కువ వడ్డీ", c: A.good, frac: 0.30 },
  ];
  const X0 = 140, W = 1640, barY = 340;
  let acc = 0;
  return (
    <Stage>
      <Head theme={T} kicker="CIBIL మాస్టర్‌క్లాస్" title="స్కోర్ బ్యాండ్‌లు — ఏది ఏమి చెబుతుంది" color={A.fin} o={p(0, 0.06)} />
      {bands.map((b, i) => {
        const segX = X0 + acc * W;
        const segW = b.frac * W;
        acc += b.frac;
        const o = p(0.12 + i * 0.08, 0.24 + i * 0.08);
        return (
          <React.Fragment key={i}>
            <div style={{ position: "absolute", left: segX, top: barY, width: segW - 8, height: 74, background: `linear-gradient(180deg, ${b.c}, ${mix(b.c, T.bg1, 0.4)})`, borderRadius: 10, opacity: o }} />
            <div style={{ position: "absolute", left: segX, top: barY - 44, width: segW, textAlign: "center", fontFamily: MONO, fontWeight: 700, fontSize: 26, color: b.c, opacity: o }}>{b.range}</div>
            <div style={{ position: "absolute", left: segX, top: barY + 100, width: segW - 8, opacity: p(0.2 + i * 0.08, 0.32 + i * 0.08) }}>
              <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 30, color: b.c, textAlign: "center" }}>{b.k}</div>
              <div style={{ fontFamily: SANS, fontSize: 23, color: T.text, marginTop: 8, textAlign: "center", lineHeight: 1.3, padding: "0 12px" }}>{b.v}</div>
            </div>
          </React.Fragment>
        );
      })}
      <div style={{ position: "absolute", left: 140, top: 700, width: 1640, textAlign: "center", opacity: p(0.8, 0.9) }}>
        <span style={{ fontFamily: SANS, fontWeight: 800, fontSize: 38, color: A.good }}>లక్ష్యం: 750+ స్కోర్</span>
      </div>
    </Stage>
  );
};

// cc_checklist — reusable checklist (title + items via props) ----------------
const ChecklistScene: React.FC<{ dur?: number; kicker?: string; title?: string; color?: string; items?: string[] }> = ({
  dur, kicker = "", title = "", color = A.good, items = [],
}) => {
  const p = useP(dur);
  return (
    <Stage>
      <Head theme={T} kicker={kicker} title={title} color={color} o={p(0, 0.06)} />
      <div style={{ position: "absolute", left: 260, top: 240, width: 1400, display: "flex", flexDirection: "column", gap: 16 }}>
        {items.map((h, i) => {
          const at = 0.08 + i * 0.11;
          const o = p(at, at + 0.08);
          return (
            <div key={i} style={{ display: "flex", alignItems: "center", gap: 22, opacity: o, transform: `translateX(${(1 - o) * -26}px)`, background: mix(T.panel, color, 0.06), border: `1.5px solid ${T.line}`, borderLeft: `5px solid ${color}`, borderRadius: 14, padding: "20px 28px" }}>
              <span style={{ fontSize: 38 }}>✅</span>
              <span style={{ fontFamily: SANS, fontWeight: 600, fontSize: 31, color: T.text }}>{h}</span>
            </div>
          );
        })}
      </div>
    </Stage>
  );
};

// cc_myths — myth vs fact rows (via props) -----------------------------------
const MythsScene: React.FC<{ dur?: number; kicker?: string; title?: string; pairs?: { m: string; f: string }[] }> = ({
  dur, kicker = "", title = "", pairs = [],
}) => {
  const p = useP(dur);
  return (
    <Stage>
      <Head theme={T} kicker={kicker} title={title} color={A.bad} o={p(0, 0.06)} />
      {pairs.map((pr, i) => {
        const y = 250 + i * 200;
        const o = p(0.12 + i * 0.12, 0.24 + i * 0.12);
        return (
          <React.Fragment key={i}>
            <div style={{ position: "absolute", left: 140, top: y, width: 780, height: 168, borderRadius: 16, background: mix(T.panel, A.bad, 0.08), border: `2px solid ${mix(T.line, A.bad, 0.5)}`, padding: "22px 28px", boxSizing: "border-box", opacity: o }}>
              <div style={{ fontFamily: MONO, fontSize: 22, color: A.bad }}>❌ అపోహ</div>
              <div style={{ fontFamily: SANS, fontWeight: 700, fontSize: 29, color: T.text, marginTop: 8, lineHeight: 1.3 }}>{pr.m}</div>
            </div>
            <Wire x1={922} y1={y + 84} x2={998} y2={y + 84} p={p(0.16 + i * 0.12, 0.24 + i * 0.12)} color={A.good} w={3} />
            <div style={{ position: "absolute", left: 1000, top: y, width: 780, height: 168, borderRadius: 16, background: mix(T.panel, A.good, 0.1), border: `2.5px solid ${A.good}`, padding: "22px 28px", boxSizing: "border-box", opacity: p(0.2 + i * 0.12, 0.32 + i * 0.12) }}>
              <div style={{ fontFamily: MONO, fontSize: 22, color: A.good }}>✅ నిజం</div>
              <div style={{ fontFamily: SANS, fontWeight: 700, fontSize: 29, color: T.text, marginTop: 8, lineHeight: 1.3 }}>{pr.f}</div>
            </div>
          </React.Fragment>
        );
      })}
    </Stage>
  );
};

// cc_iconcards — reusable 2x2 icon+text cards (via props) --------------------
const IconCardsScene: React.FC<{ dur?: number; kicker?: string; title?: string; color?: string; items?: { emoji: string; k: string; v: string }[] }> = ({
  dur, kicker = "", title = "", color = A.card, items = [],
}) => {
  const p = useP(dur);
  return (
    <Stage>
      <Head theme={T} kicker={kicker} title={title} color={color} o={p(0, 0.06)} />
      {items.map((it, i) => {
        const col = i % 2, row = Math.floor(i / 2);
        const x = 160 + col * 850, y = 250 + row * 290;
        const o = p(0.12 + i * 0.1, 0.24 + i * 0.1);
        return (
          <Card key={i} theme={T} x={x} y={y} w={780} h={250} color={color} o={o}>
            <div style={{ display: "flex", alignItems: "center", gap: 20 }}>
              <div style={{ fontSize: 58 }}>{it.emoji}</div>
              <div>
                <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 34, color }}>{it.k}</div>
                <div style={{ fontFamily: SANS, fontSize: 26, color: T.text, marginTop: 8, lineHeight: 1.35 }}>{it.v}</div>
              </div>
            </div>
          </Card>
        );
      })}
    </Stage>
  );
};

// cc_payoff — COMPUTED: how much faster you clear ₹50,000 by paying more -----
const PAYOFF = (() => {
  const sim = (monthly: number | "min") => {
    let bal = 50000, rate = 0.035, m = 0, intr = 0;
    while (bal > 1 && m < 600) {
      const i = bal * rate; intr += i;
      let pay = monthly === "min" ? Math.max(bal * 0.05, 200) : monthly;
      if (pay > bal + i) pay = bal + i;
      bal = bal + i - pay; m++;
    }
    return { months: m, interest: Math.round(intr) };
  };
  return [
    { k: "మినిమం మాత్రమే", ...sim("min"), c: A.bad },
    { k: "నెలకు ₹5,000", ...sim(5000), c: A.money },
    { k: "నెలకు ₹10,000", ...sim(10000), c: A.good },
  ];
})();

const PayoffScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur);
  const maxM = PAYOFF[0].months;
  return (
    <Stage>
      <Head theme={T} kicker="డెట్-ఫ్రీ · నిజం" title="కొంచెం ఎక్కువ కడితే — భారీ ఆదా (₹50,000)" color={A.good} o={p(0, 0.06)} />
      {PAYOFF.map((r, i) => {
        const y = 280 + i * 165;
        const grow = p(0.16 + i * 0.12, 0.34 + i * 0.12);
        const bw = Math.max(14, (r.months / maxM) * 1180 * grow);
        const yrs = (r.months / 12).toFixed(r.months < 24 ? 0 : 1);
        return (
          <React.Fragment key={i}>
            <div style={{ position: "absolute", left: 140, top: y - 44, fontFamily: SANS, fontWeight: 800, fontSize: 32, color: r.c, opacity: p(0.12 + i * 0.12, 0.24 + i * 0.12) }}>{r.k}</div>
            <div style={{ position: "absolute", left: 140, top: y, width: bw, height: 66, borderRadius: 12, background: `linear-gradient(90deg, ${r.c}, ${mix(r.c, T.bg1, 0.45)})`, border: `2px solid ${r.c}` }} />
            <div style={{ position: "absolute", left: 140 + bw + 20, top: y + 4, fontFamily: MONO, fontWeight: 800, fontSize: 30, color: r.c, opacity: grow, whiteSpace: "nowrap" }}>
              {r.months < 24 ? `${r.months} నెలలు` : `${yrs} ఏళ్లు`} · వడ్డీ ₹{r.interest.toLocaleString("en-IN")}
            </div>
          </React.Fragment>
        );
      })}
      <div style={{ position: "absolute", left: 140, top: 810, width: 1640, textAlign: "center", opacity: p(0.82, 0.9) }}>
        <span style={{ fontFamily: SANS, fontWeight: 700, fontSize: 30, color: T.text }}>నెలకు కొన్ని వేలు ఎక్కువ కడితే — <span style={{ color: A.good }}>17 ఏళ్లు → 1 ఏడాదికి తగ్గుతుంది.</span></span>
      </div>
    </Stage>
  );
};

// cc_rewardmath — COMPUTED: annual cashback from category-matched spending ----
const RMATH = (() => {
  const cats = [
    { k: "ఆన్‌లైన్ షాపింగ్", spend: 10000, rate: 5, c: A.good },
    { k: "బిల్లులు (GPay)", spend: 8000, rate: 5, c: A.card },
    { k: "ఫుడ్ · ప్రయాణం", spend: 6000, rate: 4, c: A.money },
    { k: "ఇతర ఖర్చులు", spend: 12000, rate: 1.5, c: A.fin },
  ].map((c) => ({ ...c, back: Math.round(c.spend * c.rate / 100) }));
  const monthly = cats.reduce((s, c) => s + c.back, 0);
  return { cats, monthly, annual: monthly * 12 };
})();

const RewardMathScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur);
  return (
    <Stage>
      <Head theme={T} kicker="రివార్డ్స్ మాస్టర్‌క్లాస్" title="ఏడాదికి ఎంత తిరిగి వస్తుంది?" color={A.good} o={p(0, 0.06)} />
      <div style={{ position: "absolute", left: 130, top: 250, width: 1050 }}>
        {RMATH.cats.map((c, i) => {
          const o = p(0.14 + i * 0.1, 0.26 + i * 0.1);
          return (
            <div key={i} style={{ display: "flex", justifyContent: "space-between", alignItems: "center", padding: "20px 24px", marginBottom: 14, borderRadius: 12, background: mix(T.panel, c.c, 0.07), borderLeft: `5px solid ${c.c}`, opacity: o }}>
              <span style={{ fontFamily: SANS, fontWeight: 700, fontSize: 28, color: T.text, width: 360 }}>{c.k}</span>
              <span style={{ fontFamily: MONO, fontSize: 26, color: T.muted }}>₹{c.spend.toLocaleString("en-IN")} × {c.rate}%</span>
              <span style={{ fontFamily: MONO, fontWeight: 800, fontSize: 30, color: c.c }}>₹{c.back}</span>
            </div>
          );
        })}
      </div>
      <Card theme={T} x={1230} y={280} w={550} h={430} color={A.good} o={p(0.6, 0.72)} glow>
        <div style={{ textAlign: "center", height: "100%", display: "flex", flexDirection: "column", justifyContent: "center" }}>
          <div style={{ fontFamily: MONO, fontSize: 25, color: T.muted }}>నెలకు తిరిగి</div>
          <div style={{ fontFamily: MONO, fontWeight: 800, fontSize: 54, color: T.text, marginTop: 6 }}>₹<Counter p={p(0.6, 0.76)} to={RMATH.monthly} color={T.text} size={54} /></div>
          <div style={{ height: 2, background: mix(T.line, A.good, 0.4), margin: "24px 40px" }} />
          <div style={{ fontFamily: MONO, fontSize: 25, color: A.good }}>సంవత్సరానికి</div>
          <div style={{ fontFamily: MONO, fontWeight: 800, fontSize: 72, color: A.good, marginTop: 6 }}>₹<Counter p={p(0.68, 0.86)} to={RMATH.annual} color={A.good} size={72} /></div>
        </div>
      </Card>
      <div style={{ position: "absolute", left: 130, top: 780, width: 1050, textAlign: "center", opacity: p(0.84, 0.92) }}>
        <span style={{ fontFamily: SANS, fontWeight: 700, fontSize: 27, color: T.text }}>సరైన కేటగిరీకి సరైన కార్డ్ వాడితేనే ఇది సాధ్యం.</span>
      </div>
    </Stage>
  );
};

// cc_compare3 — generic 3-column comparison (via props) ----------------------
const Compare3Scene: React.FC<{ dur?: number; kicker?: string; title?: string; cols?: { name: string; color: string; emoji?: string; rows: { k: string; v: string }[] }[] }> = ({
  dur, kicker = "", title = "", cols = [],
}) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  return (
    <Stage>
      <Head theme={T} kicker={kicker} title={title} o={p(0, 0.06)} />
      {cols.map((col, i) => {
        const x = 140 + i * 560;
        const at = 0.12 + i * 0.14;
        return (
          <Card key={i} theme={T} x={x} y={230} w={520} h={600} color={col.color} o={p(at, at + 0.1)} glow={i === 0}>
            <div style={{ textAlign: "center" }}>
              {col.emoji && <div style={{ fontSize: 50 }}>{col.emoji}</div>}
              <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 30, color: col.color, marginTop: 4 }}>{col.name}</div>
            </div>
            <div style={{ marginTop: 20, display: "flex", flexDirection: "column", gap: 16 }}>
              {col.rows.map((r, ri) => (
                <div key={ri} style={{ opacity: p(at + 0.06 + ri * 0.03, at + 0.14 + ri * 0.03) }}>
                  <div style={{ fontFamily: MONO, fontSize: 20, color: T.muted }}>{r.k}</div>
                  <div style={{ fontFamily: SANS, fontWeight: 700, fontSize: 27, color: T.text, marginTop: 2, lineHeight: 1.25 }}>{r.v}</div>
                </div>
              ))}
            </div>
            {i === 0 && <div style={{ position: "absolute", left: 0, right: 0, bottom: -1, height: 8, borderRadius: 4, background: col.color, opacity: 0.5 + Math.sin(frame * 0.08) * 0.3 }} />}
          </Card>
        );
      })}
    </Stage>
  );
};

// ===========================================================================
export const CCScene: React.FC<{ variant: string;[key: string]: unknown }> = ({ variant, ...rest }) => {
  let content: React.ReactNode;
  let accent = A.card;
  switch (variant) {
    case "cc_title": content = <TitleScene {...(rest as any)} />; break;
    case "cc_hook": content = <HookScene {...(rest as any)} />; break;
    case "cc_whatis": content = <WhatIsScene {...(rest as any)} />; accent = A.money; break;
    case "cc_vs": content = <VsScene {...(rest as any)} />; accent = A.fin; break;
    case "cc_anatomy": content = <AnatomyScene {...(rest as any)} />; break;
    case "cc_swipe": content = <SwipeScene {...(rest as any)} />; accent = A.good; break;
    case "cc_billing": content = <BillingScene {...(rest as any)} />; break;
    case "cc_grace": content = <GraceScene {...(rest as any)} />; accent = A.good; break;
    case "cc_mindue": content = <MinDueScene {...(rest as any)} />; accent = A.bad; break;
    case "cc_interest": content = <InterestScene {...(rest as any)} />; accent = A.bad; break;
    case "cc_fees": content = <FeesScene {...(rest as any)} />; accent = A.money; break;
    case "cc_cibil": content = <CibilScene {...(rest as any)} />; accent = A.fin; break;
    case "cc_util": content = <UtilScene {...(rest as any)} />; accent = A.fin; break;
    case "cc_factors": content = <FactorsScene {...(rest as any)} />; accent = A.fin; break;
    case "cc_firstcard": content = <FirstCardScene {...(rest as any)} />; accent = A.fin; break;
    case "cc_rewards": content = <RewardsScene {...(rest as any)} />; accent = A.good; break;
    case "cc_nocostemi": content = <NoCostEmiScene {...(rest as any)} />; accent = A.money; break;
    case "cc_perks": content = <PerksScene {...(rest as any)} />; accent = A.good; break;
    case "cc_habits": content = <HabitsScene {...(rest as any)} />; accent = A.good; break;
    case "cc_spiral": content = <SpiralScene {...(rest as any)} />; accent = A.bad; break;
    case "cc_mintrap": content = <MinTrapScene {...(rest as any)} />; accent = A.bad; break;
    case "cc_mistakes": content = <MistakesScene {...(rest as any)} />; accent = A.bad; break;
    case "cc_escape": content = <EscapeScene {...(rest as any)} />; accent = A.good; break;
    case "cc_bankcards": content = <BankCardsScene {...(rest as any)} />; accent = A.card; break;
    case "cc_fintech": content = <FintechScene {...(rest as any)} />; accent = A.fin; break;
    case "cc_choose": content = <ChooseScene {...(rest as any)} />; accent = A.card; break;
    case "cc_ptitle": content = <PTitleScene {...(rest as any)} />; break;
    case "cc_cardreview": content = <CardReviewScene {...(rest as any)} />; accent = ((rest as any).color as string) || A.card; break;
    case "cc_cardcompare": content = <CardCompareScene {...(rest as any)} />; break;
    case "cc_scorebands": content = <ScoreBandsScene {...(rest as any)} />; accent = A.fin; break;
    case "cc_checklist": content = <ChecklistScene {...(rest as any)} />; accent = ((rest as any).color as string) || A.good; break;
    case "cc_myths": content = <MythsScene {...(rest as any)} />; accent = A.bad; break;
    case "cc_iconcards": content = <IconCardsScene {...(rest as any)} />; accent = ((rest as any).color as string) || A.card; break;
    case "cc_payoff": content = <PayoffScene {...(rest as any)} />; accent = A.good; break;
    case "cc_rewardmath": content = <RewardMathScene {...(rest as any)} />; accent = A.good; break;
    case "cc_compare3": content = <Compare3Scene {...(rest as any)} />; break;
    case "cc_divider": content = <DividerScene {...(rest as any)} />; accent = (rest as any).color || A.card; break;
    case "cc_recap": content = <RecapScene {...(rest as any)} />; break;
    default: content = <TitleScene {...(rest as any)} />;
  }
  return (
    <AbsoluteFill>
      <Bg theme={T} accent={accent} />
      {content}
    </AbsoluteFill>
  );
};

export default CCScene;
