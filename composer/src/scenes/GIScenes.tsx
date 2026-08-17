/**
 * GIScenes.tsx — "Global IPOs: US vs China this week" (prefix `gi`, English).
 *
 * A SEPARATE international IPO track — NOT the India `sm` set. Read skills/13-intl-ipo.md.
 *
 * Identity (skills/04):
 *   theme accent = blue (Wall Street). Semantic accents:
 *     us    blue   #4F86F7 — United States / Nasdaq / NYSE
 *     cn    red    #F5546B — China / Shanghai / Hong Kong
 *     cash  amber  #FBBF24 — money, deal size, valuation
 *     mkt   cyan   #22D3EE — mechanics / process (filing, book-building, listing)
 *     ok    green  #34D399 — the insight / "good structure"
 *   Recurring motif: a DualTape — two scrolling ticker rows (blue US on top,
 *   red China below) that never stop. Appears in title / dividers / recap.
 *   Every content scene carries a bottom scene-progress bar (rule 2).
 */
import React from "react";
import { AbsoluteFill, interpolate, useCurrentFrame } from "remotion";
import {
  makeTheme, mix, useP, usePop, rnd, MONO, SANS,
  Bg, Stage, Head, Kicker, Flow, Wire, Counter,
  Brackets, ScanBeam,
} from "../lib/primitives";

const T = makeTheme({ accent: "#4F86F7" });
const A = { us: "#4F86F7", cn: "#F5546B", cash: "#FBBF24", mkt: "#22D3EE", ok: "#34D399" };

// ---------------------------------------------------------------- motif: DualTape
// Two scrolling ticker rows. Continuous motion off raw frame.
const US_TAPE = ["ATTO ▲", "BRVE ▲", "VOGX ▲", "OCLT ●", "NASDAQ", "S-1", "NYSE", "SPAC", "BIOTECH", "$200M"];
const CN_TAPE = ["CXMT ▲", "INNOLIGHT ▲", "688xxx", "STAR", "HKEX", "¥57.9B", "CHINEXT", "DRAM", "CHIPS", "HK$55B"];
const Tape: React.FC<{ y: number; items: string[]; color: string; speed: number; o?: number }> = ({
  y, items, color, speed, o = 1,
}) => {
  const frame = useCurrentFrame();
  const step = 340;
  const period = items.length * step;
  const off = (frame * speed) % period;
  return (
    <div style={{ position: "absolute", left: 0, top: y, width: 1920, height: 54, opacity: o, overflow: "hidden", pointerEvents: "none" }}>
      {items.concat(items).map((s, i) => {
        const x = i * step - off;
        if (x < -step || x > 1920) return null;
        return (
          <div key={i} style={{
            position: "absolute", left: x, top: 6, fontFamily: MONO, fontWeight: 700, fontSize: 26,
            color, letterSpacing: 2, opacity: 0.5,
          }}>{s}</div>
        );
      })}
    </div>
  );
};
const DualTape: React.FC<{ o?: number }> = ({ o = 1 }) => (
  <>
    <Tape y={140} items={US_TAPE} color={A.us} speed={1.4} o={o} />
    <Tape y={900} items={CN_TAPE} color={A.cn} speed={-1.2} o={o} />
  </>
);

// scene-progress bar — cheap universal "this is playing" signal (skills/03 rule 2)
const GIProgress: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur);
  return (
    <div style={{ position: "absolute", left: 0, bottom: 0, height: 6, width: `${p(0, 1) * 100}%`,
      background: `linear-gradient(90deg, ${A.us}, ${A.cn})`, opacity: 0.55 }} />
  );
};

// ---------------------------------------------------------------- gi_title
const TitleScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const pop = usePop(dur);
  return (
    <AbsoluteFill style={{ alignItems: "center", justifyContent: "center" }}>
      <DualTape o={p(0.1, 0.28)} />
      {/* orbiting $ / ¥ dots */}
      {Array.from({ length: 12 }).map((_, i) => {
        const ang = frame * 0.009 + (i / 12) * Math.PI * 2;
        const usd = i % 2 === 0;
        return (
          <div key={i} style={{
            position: "absolute", left: 960 + Math.cos(ang) * (620 + i * 9) - 12,
            top: 540 + Math.sin(ang) * (300 + i * 6) - 12,
            fontFamily: MONO, fontWeight: 800, fontSize: 24, color: usd ? A.us : A.cn,
            opacity: 0.14 + rnd(i, 3) * 0.2, textShadow: `0 0 12px ${usd ? A.us : A.cn}`,
          }}>{usd ? "$" : "¥"}</div>
        );
      })}
      <div style={{ textAlign: "center", transform: `scale(${0.92 + pop(0) * 0.08})`, zIndex: 2 }}>
        <div style={{ display: "flex", justifyContent: "center", marginBottom: 26 }}>
          <Kicker theme={T} text="MARKET DEEP-DIVE · THIS WEEK" cx />
        </div>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 116, lineHeight: 1.05, letterSpacing: -3, color: T.text }}>
          <div>Two IPO Markets,</div>
          <div>
            <span style={{ color: A.us, textShadow: `0 0 60px ${mix(T.bg0, A.us, 0.7)}` }}>One</span>{" "}
            <span style={{ color: A.cn, textShadow: `0 0 60px ${mix(T.bg0, A.cn, 0.7)}` }}>Week</span>
          </div>
        </div>
        <div style={{ height: 6, width: interpolate(p(0.18, 0.45), [0, 1], [0, 620]), background: `linear-gradient(90deg, ${A.us}, ${A.cn})`, borderRadius: 3, margin: "30px auto" }} />
        <div style={{ fontFamily: SANS, fontSize: 35, color: T.muted, opacity: p(0.28, 0.5), lineHeight: 1.4 }}>
          Nasdaq biotech &amp; SPACs · Shanghai &amp; Hong Kong mega-chips — same word, different game
        </div>
      </div>
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------- gi_split (bespoke hook)
// Left = US (many small tickets), Right = China (a couple of giants). Contrast IS the point.
const SplitScene: React.FC<{
  dur?: number;
  usItems?: { name: string; tag: string }[];
  cnBig?: { name: string; tag: string; note: string };
  cnSmall?: { name: string; tag: string };
}> = ({
  dur,
  usItems = [
    { name: "Attovia Therapeutics", tag: "BIOTECH" },
    { name: "Braveheart Bio", tag: "BIOTECH" },
    { name: "Vogenx", tag: "BIOTECH" },
    { name: "OceanLight", tag: "SPAC" },
    { name: "…and more small deals", tag: "NASDAQ" },
  ],
  cnBig = { name: "CXMT — ChangXin Memory", tag: "STAR MARKET", note: "memory chips · a record-size listing" },
  cnSmall = { name: "Zhongji Innolight", tag: "HONG KONG" },
}) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const bigHot = 0.9 + Math.sin(frame * 0.06) * 0.1;
  return (
    <Stage>
      <Head theme={T} kicker="THE SAME WEEK · TWO WORLDS" title="One giant. Or a dozen small ones." o={p(0, 0.06)} />
      {/* center divider + downward flow */}
      <div style={{ position: "absolute", left: 958, top: 210, width: 4, height: 690, background: mix(T.line, T.text, 0.15), borderRadius: 2, opacity: p(0.05, 0.14) }} />
      <Flow x1={960} y1={230} x2={960} y2={880} color={mix(A.us, A.cn, 0.5)} n={6} o={p(0.1, 0.2)} />

      {/* LEFT — United States: many small */}
      <div style={{ position: "absolute", left: 110, top: 220, width: 800, opacity: p(0.06, 0.14) }}>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 40, color: A.us }}>🇺🇸 United States</div>
        <div style={{ fontFamily: MONO, fontSize: 24, color: T.muted, marginTop: 4 }}>MANY SMALL DEALS</div>
      </div>
      {usItems.map((it, i) => {
        const at = 0.12 + i * 0.06;
        const o = p(at, at + 0.07);
        return (
          <div key={i} style={{
            position: "absolute", left: 110, top: 320 + i * 104, width: 780, height: 88,
            borderRadius: 14, boxSizing: "border-box", padding: "0 24px",
            display: "flex", alignItems: "center", gap: 16,
            background: mix(T.panel, A.us, o > 0.5 ? 0.09 : 0.02), border: `2px solid ${o > 0.5 ? mix(T.bg2, A.us, 0.6) : T.bg2}`,
            opacity: o, transform: `translateX(${(1 - o) * -24}px)`,
          }}>
            <span style={{ fontSize: 30 }}>{it.tag === "SPAC" ? "📦" : it.tag === "NASDAQ" ? "➕" : "🧬"}</span>
            <span style={{ fontFamily: SANS, fontWeight: 700, fontSize: 28, color: T.text, flex: 1 }}>{it.name}</span>
            <span style={{ fontFamily: MONO, fontWeight: 700, fontSize: 19, color: T.bg0, background: A.us, borderRadius: 999, padding: "5px 14px" }}>{it.tag}</span>
          </div>
        );
      })}

      {/* RIGHT — China: a couple of giants */}
      <div style={{ position: "absolute", left: 1010, top: 220, width: 800, opacity: p(0.1, 0.18) }}>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 40, color: A.cn }}>🇨🇳 China</div>
        <div style={{ fontFamily: MONO, fontSize: 24, color: T.muted, marginTop: 4 }}>A FEW GIANT DEALS</div>
      </div>
      {/* the giant */}
      <div style={{
        position: "absolute", left: 1010, top: 320, width: 800, height: 300, borderRadius: 22, boxSizing: "border-box", padding: "34px 36px",
        background: mix(T.panel, A.cn, 0.13), border: `3px solid ${A.cn}`,
        opacity: p(0.4, 0.56), transform: `scale(${0.96 + p(0.4, 0.56) * 0.04})`,
        boxShadow: p(0.5, 0.6) > 0.5 ? `0 0 ${44 * bigHot}px ${mix(T.bg0, A.cn, 0.4)}` : "none",
      }}>
        <div style={{ display: "flex", alignItems: "center", gap: 18 }}>
          <span style={{ fontSize: 60 }}>🏭</span>
          <span style={{ fontFamily: MONO, fontWeight: 700, fontSize: 20, color: T.bg0, background: A.cn, borderRadius: 999, padding: "6px 16px" }}>{cnBig.tag}</span>
        </div>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 48, color: T.text, marginTop: 18, lineHeight: 1.1 }}>{cnBig.name}</div>
        <div style={{ fontFamily: SANS, fontSize: 27, color: T.muted, marginTop: 14, lineHeight: 1.35 }}>{cnBig.note}</div>
      </div>
      {/* the second */}
      <div style={{
        position: "absolute", left: 1010, top: 648, width: 800, height: 150, borderRadius: 18, boxSizing: "border-box", padding: "0 30px",
        display: "flex", alignItems: "center", gap: 18,
        background: mix(T.panel, A.cn, 0.08), border: `2.5px solid ${p(0.62, 0.72) > 0.5 ? mix(T.bg2, A.cn, 0.7) : T.bg2}`,
        opacity: p(0.62, 0.72),
      }}>
        <span style={{ fontSize: 46 }}>🔦</span>
        <span style={{ fontFamily: SANS, fontWeight: 700, fontSize: 32, color: T.text, flex: 1 }}>{cnSmall.name}</span>
        <span style={{ fontFamily: MONO, fontWeight: 700, fontSize: 19, color: T.bg0, background: A.cn, borderRadius: 999, padding: "5px 14px" }}>{cnSmall.tag}</span>
      </div>

      <GIProgress dur={dur} />
    </Stage>
  );
};

// ---------------------------------------------------------------- gi_steps (generic pipeline)
const StepsScene: React.FC<{
  dur?: number; kicker?: string; title?: string; color?: string; note?: string;
  items?: { emoji: string; label: string; sub: string; c?: string }[];
}> = ({ dur, kicker = "HOW IT WORKS", title = "", color = A.mkt, note = "", items = [] }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const n = items.length;
  const w = n === 3 ? 420 : n === 4 ? 360 : 290;
  const gapX = n === 3 ? 560 : n === 4 ? 425 : 350;
  const x0 = n === 3 ? 190 : n === 4 ? 165 : 170;
  const y = 400;
  return (
    <Stage>
      <Head theme={T} kicker={kicker} title={title} color={color} o={p(0, 0.06)} />
      {items.map((it, i) => {
        const c = it.c || color;
        const at = 0.1 + i * (0.55 / n);
        const o = p(at, at + 0.08);
        const ghost = p(0.03, 0.07);
        const x = x0 + i * gapX;
        const active = Math.floor(frame / 24) % n === i && p(0.7, 0.71) > 0.5;
        return (
          <React.Fragment key={i}>
            {i > 0 && (
              <>
                <Wire x1={x0 + (i - 1) * gapX + w} y1={y + 105} x2={x - 8} y2={y + 105} p={p(at - 0.05, at)} color={c} w={3} />
                <Flow x1={x0 + (i - 1) * gapX + w} y1={y + 105} x2={x - 8} y2={y + 105} color={c} n={4} o={p(at, at + 0.1)} />
              </>
            )}
            <div style={{ position: "absolute", left: x, top: y, width: w, height: 230,
              borderRadius: 18, boxSizing: "border-box", padding: "22px 20px", textAlign: "center",
              background: mix(T.panel, c, o > 0.5 ? (active ? 0.16 : 0.09) : 0.02),
              border: `2.5px solid ${o > 0.5 ? mix(T.bg2, c, active ? 1 : 0.7) : T.bg2}`,
              opacity: Math.max(ghost * 0.22, o), transform: `translateY(${(1 - o) * 20}px) scale(${active ? 1.04 : 1})` }}>
              <div style={{ fontSize: 48 }}>{it.emoji}</div>
              <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 28, color: c, marginTop: 8, lineHeight: 1.2 }}>{it.label}</div>
              <div style={{ fontFamily: SANS, fontSize: 22, color: T.muted, marginTop: 6, lineHeight: 1.35 }}>{it.sub}</div>
            </div>
          </React.Fragment>
        );
      })}
      {note && (
        <div style={{ position: "absolute", left: 150, top: 730, width: 1620, textAlign: "center", opacity: p(0.72, 0.84) }}>
          <span style={{ fontFamily: SANS, fontWeight: 700, fontSize: 31, color: T.text, lineHeight: 1.4 }}>{note}</span>
        </div>
      )}
      <GIProgress dur={dur} />
    </Stage>
  );
};

// ---------------------------------------------------------------- gi_spac (bespoke computed)
// A blank-check lifecycle: raise cash into trust → hunt a target → merge → real company.
// A bright token travels stage→stage on p; trust-account counter fills.
const SpacScene: React.FC<{ dur?: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const stages = [
    { emoji: "📦", label: "IPO an empty shell", sub: "raise cash, no business yet", c: A.cash },
    { emoji: "🔎", label: "Hunt for a target", sub: "usually within ~2 years", c: A.mkt },
    { emoji: "🤝", label: "Merge (de-SPAC)", sub: "combine with a real company", c: A.us },
    { emoji: "🏢", label: "A public company", sub: "the target is now listed", c: A.ok },
  ];
  const n = stages.length, w = 360, gapX = 425, x0 = 165, y = 380;
  const travel = p(0.16, 0.82);            // 0..1 across the 4 stages
  const tokX = x0 + interpolate(travel, [0, 1], [w / 2, (n - 1) * gapX + w / 2]);
  const cur = Math.min(n - 1, Math.floor(travel * n));
  return (
    <Stage>
      <Head theme={T} kicker="THE US ODDITY · SPAC" title="A SPAC: an IPO with no business — yet" color={A.cash} o={p(0, 0.06)} />
      {stages.map((s, i) => {
        const at = 0.1 + i * 0.13;
        const o = p(at, at + 0.08);
        const on = travel * n > i;
        const x = x0 + i * gapX;
        return (
          <React.Fragment key={i}>
            {i > 0 && <Wire x1={x0 + (i - 1) * gapX + w} y1={y + 105} x2={x - 8} y2={y + 105} p={p(at - 0.05, at)} color={s.c} w={3} />}
            <div style={{ position: "absolute", left: x, top: y, width: w, height: 230,
              borderRadius: 18, boxSizing: "border-box", padding: "22px 20px", textAlign: "center",
              background: mix(T.panel, s.c, on ? 0.14 : 0.03), border: `2.5px solid ${on ? s.c : T.bg2}`,
              opacity: Math.max(p(0.02, 0.06) * 0.25, o), transform: `translateY(${(1 - o) * 20}px) scale(${cur === i ? 1.05 : 1})`,
              boxShadow: cur === i ? `0 0 ${34 + Math.sin(frame * 0.1) * 12}px ${mix(T.bg0, s.c, 0.4)}` : "none" }}>
              <div style={{ fontSize: 50 }}>{s.emoji}</div>
              <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 26, color: s.c, marginTop: 8, lineHeight: 1.2 }}>{s.label}</div>
              <div style={{ fontFamily: SANS, fontSize: 21, color: T.muted, marginTop: 6, lineHeight: 1.35 }}>{s.sub}</div>
            </div>
          </React.Fragment>
        );
      })}
      {/* traveling token */}
      <div style={{ position: "absolute", left: tokX - 13, top: y + 105 - 13, width: 26, height: 26, borderRadius: 13,
        background: T.text, boxShadow: `0 0 22px ${T.text}`, opacity: p(0.16, 0.24) }} />
      {/* trust-account meter */}
      <div style={{ position: "absolute", left: 165, top: 690, width: 1590, opacity: p(0.5, 0.6) }}>
        <div style={{ display: "flex", alignItems: "baseline", gap: 16 }}>
          <span style={{ fontFamily: MONO, fontSize: 24, color: T.muted }}>cash held in trust:</span>
          <Counter p={p(0.5, 0.72)} to={100} prefix="≈ $" suffix="M" color={A.cash} size={44} />
          <span style={{ fontFamily: SANS, fontSize: 24, color: T.muted }}>— refunded if no deal is found</span>
        </div>
      </div>
      <div style={{ position: "absolute", left: 150, top: 800, width: 1620, textAlign: "center", opacity: p(0.78, 0.9) }}>
        <span style={{ fontFamily: SANS, fontWeight: 700, fontSize: 30, color: T.text, lineHeight: 1.4 }}>
          You're backing the <span style={{ color: A.cash, fontWeight: 800 }}>sponsor's</span> ability to find a good target — not a business you can see today.
        </span>
      </div>
      <GIProgress dur={dur} />
    </Stage>
  );
};

// ---------------------------------------------------------------- gi_cards (generic iconcards)
const CardsScene: React.FC<{
  dur?: number; kicker?: string; title?: string; color?: string;
  items?: { emoji: string; k: string; v: string; chip?: string }[];
}> = ({ dur, kicker = "", title = "", color = A.us, items = [] }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const cols = items.length > 4 ? 3 : 2;
  const rows = Math.ceil(items.length / cols);
  const w = cols === 2 ? 810 : 533, gap = 24;
  const h = rows === 2 ? 320 : 210;
  const y0 = 210 + (660 - (rows * h + (rows - 1) * gap)) / 2;
  const hot = Math.floor(frame / 32) % items.length;
  return (
    <Stage>
      <Head theme={T} kicker={kicker} title={title} color={color} o={p(0, 0.06)} />
      {items.map((it, i) => {
        const r = Math.floor(i / cols), c = i % cols;
        const at = 0.1 + i * (0.55 / items.length);
        const o = p(at, at + 0.09);
        const ghost = p(0.03, 0.07);
        const active = hot === i && p(0.74, 0.75) > 0.5;
        return (
          <div key={i} style={{
            position: "absolute", left: 130 + c * (w + gap), top: y0 + r * (h + gap), width: w, height: h,
            borderRadius: 20, boxSizing: "border-box", padding: "26px 30px",
            opacity: Math.max(ghost * 0.22, o), transform: `translateY(${(1 - o) * 22}px) scale(${active ? 1.02 : 1})`,
            background: mix(T.panel, color, o > 0.5 ? (active ? 0.15 : 0.08) : 0.02),
            border: `2.5px solid ${o > 0.5 ? mix(T.bg2, color, active ? 1 : 0.65) : T.bg2}`,
          }}>
            <div style={{ display: "flex", alignItems: "center", gap: 20 }}>
              <span style={{ fontSize: h > 250 ? 60 : 46 }}>{it.emoji}</span>
              <span style={{ fontFamily: SANS, fontWeight: 800, fontSize: h > 250 ? 34 : 29, color, lineHeight: 1.22 }}>{it.k}</span>
            </div>
            <div style={{ fontFamily: SANS, fontSize: h > 250 ? 27 : 24, color: T.text, marginTop: 16, lineHeight: 1.4, opacity: 0.55 + o * 0.45 }}>{it.v}</div>
            {it.chip && (
              <div style={{ position: "absolute", right: 24, bottom: 20, fontFamily: MONO, fontWeight: 700, fontSize: 22,
                color: T.bg0, background: color, borderRadius: 999, padding: "8px 18px", opacity: o }}>{it.chip}</div>
            )}
          </div>
        );
      })}
      <GIProgress dur={dur} />
    </Stage>
  );
};

// ---------------------------------------------------------------- gi_stats (generic stat cards)
const StatsScene: React.FC<{
  dur?: number; kicker?: string; title?: string; note?: string; color?: string;
  stats?: { label: string; to: number; prefix?: string; suffix?: string; decimals?: number; color?: string; sub?: string }[];
}> = ({ dur, kicker = "BY THE NUMBERS", title = "", note = "", color = A.cash, stats = [] }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const n = stats.length;
  const w = n === 2 ? 810 : n === 3 ? 533 : 390;
  const y0 = note ? 270 : 320;
  return (
    <Stage>
      <Head theme={T} kicker={kicker} title={title} color={color} o={p(0, 0.06)} />
      {stats.map((s, i) => {
        const at = 0.1 + i * (0.5 / n);
        const o = p(at, at + 0.1);
        const ghost = p(0.03, 0.07);
        const c = s.color || color;
        return (
          <div key={i} style={{
            position: "absolute", left: 130 + i * (w + 24), top: y0, width: w, height: 360,
            borderRadius: 20, boxSizing: "border-box", padding: "34px 26px", textAlign: "center",
            background: mix(T.panel, c, o > 0.5 ? 0.07 : 0.02), border: `2.5px solid ${o > 0.5 ? mix(T.bg2, c, 0.7) : T.bg2}`,
            opacity: Math.max(ghost * 0.22, o), transform: `translateY(${(1 - o) * 22}px)`,
            boxShadow: o > 0.9 ? `0 0 ${34 + Math.sin(frame * 0.07 + i) * 12}px ${mix(T.bg0, c, 0.22)}` : "none",
          }}>
            <div style={{ fontFamily: SANS, fontSize: 26, color: T.muted, lineHeight: 1.35, minHeight: 76 }}>{s.label}</div>
            <div style={{ marginTop: 18 }}>
              <Counter p={p(at + 0.04, at + 0.22)} to={s.to} prefix={s.prefix || ""} suffix={s.suffix || ""} decimals={s.decimals || 0} color={c} size={n === 2 ? 84 : 66} />
            </div>
            {s.sub && <div style={{ fontFamily: SANS, fontSize: 23, color: T.text, marginTop: 18, lineHeight: 1.4, opacity: p(at + 0.12, at + 0.2) }}>{s.sub}</div>}
          </div>
        );
      })}
      {note && (
        <div style={{ position: "absolute", left: 130, top: 700, width: 1660, textAlign: "center", opacity: p(0.68, 0.8) }}>
          <span style={{ fontFamily: SANS, fontWeight: 700, fontSize: 30, color: T.text, lineHeight: 1.4 }}>{note}</span>
        </div>
      )}
      <GIProgress dur={dur} />
    </Stage>
  );
};

// ---------------------------------------------------------------- gi_compare (2 or 3 columns)
const CompareScene: React.FC<{
  dur?: number; kicker?: string; title?: string; color?: string;
  cols?: { name: string; color: string; emoji?: string; hi?: boolean; rows: { k: string; v: string }[] }[];
}> = ({ dur, kicker = "SIDE BY SIDE", title = "", color = A.mkt, cols = [] }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const n = cols.length;
  const w = n === 2 ? 720 : 520;
  const x0 = n === 2 ? 240 : 140;
  const gapX = n === 2 ? 720 : 560;
  return (
    <Stage>
      <Head theme={T} kicker={kicker} title={title} color={color} o={p(0, 0.06)} />
      {cols.map((col, i) => {
        const at = 0.08 + i * 0.14;
        const o = p(at, at + 0.1);
        const ghost = p(0.03, 0.07);
        return (
          <div key={i} style={{
            position: "absolute", left: x0 + i * gapX, top: 230, width: w, height: 640,
            borderRadius: 20, boxSizing: "border-box", padding: "28px 32px",
            opacity: Math.max(ghost * 0.22, o), transform: `translateY(${(1 - o) * 24}px)`,
            background: mix(T.panel, col.color, o > 0.5 ? 0.08 : 0.02),
            border: `2.5px solid ${o > 0.5 ? col.color : T.bg2}`,
          }}>
            <div style={{ textAlign: "center" }}>
              <div style={{ fontSize: 54 }}>{col.emoji}</div>
              <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 34, color: col.color, marginTop: 6, lineHeight: 1.2 }}>{col.name}</div>
            </div>
            <div style={{ marginTop: 24, display: "flex", flexDirection: "column", gap: 18 }}>
              {col.rows.map((r, ri) => (
                <div key={ri} style={{ opacity: p(at + 0.07 + ri * 0.04, at + 0.13 + ri * 0.04) }}>
                  <div style={{ fontFamily: MONO, fontSize: 21, color: T.muted, lineHeight: 1.3 }}>{r.k}</div>
                  <div style={{ fontFamily: SANS, fontWeight: 700, fontSize: 27, color: T.text, marginTop: 3, lineHeight: 1.32 }}>{r.v}</div>
                </div>
              ))}
            </div>
            {col.hi && (
              <div style={{ position: "absolute", left: 0, right: 0, bottom: -1, height: 8, borderRadius: 4, background: col.color, opacity: 0.5 + Math.sin(frame * 0.08) * 0.3 }} />
            )}
          </div>
        );
      })}
      <GIProgress dur={dur} />
    </Stage>
  );
};

// ---------------------------------------------------------------- gi_divider
const TOTAL_PARTS = 3;
const DividerScene: React.FC<{ dur?: number; n?: number; title?: string; sub?: string; color?: string }> = ({
  dur, n = 1, title = "", sub = "", color = A.us,
}) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  return (
    <Stage>
      <DualTape o={p(0.2, 0.34)} />
      <Brackets x={310} y={290} w={1300} h={490} color={color} o={p(0.02, 0.12)} len={54} />
      <ScanBeam theme={T} x={320} y={300} w={1280} h={470} color={color} o={p(0.05, 0.2)} speed={1.6} />
      <div style={{ position: "absolute", left: 0, right: 0, top: 350, textAlign: "center" }}>
        <div style={{ fontFamily: MONO, fontWeight: 800, fontSize: 34, color, letterSpacing: 10, opacity: p(0.05, 0.15) }}>
          PART {"0" + n}
        </div>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 92, color: T.text, letterSpacing: -2, marginTop: 20, opacity: p(0.12, 0.24), transform: `translateY(${(1 - p(0.12, 0.24)) * 30}px)` }}>{title}</div>
        <div style={{ height: 5, width: interpolate(p(0.2, 0.5), [0, 1], [0, 460]), background: color, borderRadius: 3, margin: "26px auto" }} />
        <div style={{ fontFamily: SANS, fontSize: 33, color: T.muted, opacity: p(0.3, 0.45), lineHeight: 1.4 }}>{sub}</div>
      </div>
      <div style={{ position: "absolute", left: 0, right: 0, top: 840, display: "flex", justifyContent: "center", gap: 16, opacity: p(0.3, 0.45) }}>
        {Array.from({ length: TOTAL_PARTS }).map((_, idx) => {
          const i = idx + 1;
          return (
            <div key={i} style={{ width: i === n ? 44 : 14, height: 14, borderRadius: 8,
              background: i <= n ? color : mix(T.panel, color, 0.15), border: `1.5px solid ${i <= n ? color : T.bg2}`,
              opacity: i === n ? 0.7 + Math.sin(frame * 0.1) * 0.3 : 1 }} />
          );
        })}
      </div>
    </Stage>
  );
};

// ---------------------------------------------------------------- gi_recap
const RecapScene: React.FC<{ dur?: number; items?: string[]; closer?: string; title?: string }> = ({
  dur, items = [], closer = "Same word, two different games — know which one you're playing.", title = "This week, in one breath",
}) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  return (
    <AbsoluteFill style={{ padding: "56px 130px", justifyContent: "center" }}>
      <DualTape o={0.3} />
      <div style={{ opacity: p(0, 0.06), textAlign: "center", marginBottom: 24 }}>
        <Kicker theme={T} text="RECAP" cx />
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 58, color: T.text, marginTop: 12, letterSpacing: -1.5 }}>{title}</div>
      </div>
      <div style={{ display: "flex", flexDirection: "column", gap: 12, maxWidth: 1440, margin: "0 auto", width: "100%" }}>
        {items.map((it, i) => {
          const at = 0.06 + i * 0.08;
          const o = p(at, at + 0.07);
          const accent = i % 2 === 0 ? A.us : A.cn;
          return (
            <div key={i} style={{ display: "flex", alignItems: "center", gap: 18,
              opacity: Math.max(p(0.02, 0.06) * 0.25, o), transform: `translateX(${(1 - o) * -26}px)`,
              background: mix(T.panel, accent, 0.05), border: `1.5px solid ${mix(T.bg2, accent, o * 0.5)}`,
              borderLeft: `4px solid ${o > 0.5 ? accent : T.bg2}`, borderRadius: 12, padding: "14px 26px" }}>
              <span style={{ color: accent, fontFamily: MONO, fontWeight: 700, fontSize: 26 }}>{i + 1}</span>
              <span style={{ fontFamily: SANS, fontSize: 29, color: T.text, lineHeight: 1.32 }}>{it}</span>
            </div>
          );
        })}
      </div>
      <div style={{ textAlign: "center", marginTop: 28, opacity: p(0.8, 0.9) }}>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontStyle: "italic", fontSize: 38, color: A.ok, textShadow: `0 0 ${28 + Math.sin(frame * 0.06) * 14}px ${mix(T.bg0, A.ok, 0.7)}` }}>{closer}</div>
      </div>
    </AbsoluteFill>
  );
};

// ===========================================================================
export const GIScene: React.FC<{ variant: string;[key: string]: unknown }> = ({ variant, ...rest }) => {
  let content: React.ReactNode;
  let accent = A.us;
  switch (variant) {
    case "gi_title": content = <TitleScene {...(rest as any)} />; break;
    case "gi_split": content = <SplitScene {...(rest as any)} />; accent = A.cn; break;
    case "gi_steps": content = <StepsScene {...(rest as any)} />; accent = (rest as any).color || A.mkt; break;
    case "gi_spac": content = <SpacScene {...(rest as any)} />; accent = A.cash; break;
    case "gi_cards": content = <CardsScene {...(rest as any)} />; accent = (rest as any).color || A.us; break;
    case "gi_stats": content = <StatsScene {...(rest as any)} />; accent = (rest as any).color || A.cash; break;
    case "gi_compare": content = <CompareScene {...(rest as any)} />; accent = (rest as any).color || A.mkt; break;
    case "gi_divider": content = <DividerScene {...(rest as any)} />; accent = (rest as any).color || A.us; break;
    case "gi_recap": content = <RecapScene {...(rest as any)} />; accent = A.ok; break;
    default: content = <TitleScene {...(rest as any)} />;
  }
  return (
    <AbsoluteFill>
      <Bg theme={T} accent={accent} />
      {content}
    </AbsoluteFill>
  );
};

export default GIScene;
