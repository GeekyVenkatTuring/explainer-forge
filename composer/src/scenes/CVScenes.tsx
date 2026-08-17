/**
 * CVScenes.tsx — Computer Vision explainer: parts 4–6 scenes (core tasks,
 * transformer era, in practice) + the CVScene dispatcher for all cv_* variants.
 * Parts 1–3 live in CVScenesA.tsx; shared pixel engine in CVShared.tsx.
 * Every scene is duration-aware (cut.ft-style `dur` prop) with continuous motion.
 */
import React from "react";
import { AbsoluteFill, interpolate, useCurrentFrame } from "remotion";
import {
  C, MONO, SANS, BW, BH, mix, useP, rnd, CAT12, SEVEN8, Bg,
  conv3, absNorm, boxBlur3, K_SHARP, K_EDGE,
  PixGrid, Brackets, ScanBeam, Flow, Wire, Counter, Type, Stage, Kicker, Head, Foot, Card,
} from "./CVShared";

// precomputed kernel results (module scope = deterministic, once per worker)
const clampG = (g: number[][]) => g.map((r) => r.map((v) => Math.max(0, Math.min(255, Math.round(v)))));
const K_BLUR_G = boxBlur3(CAT12);
const K_SHARP_G = clampG(conv3(CAT12, K_SHARP));
const K_EDGE_G = absNorm(conv3(CAT12, K_EDGE));
import {
  CvTitle, CvHook, CvDivider, CvPixels, CvTasks, CvApps,
  CvFilters, CvConv, CvEdges, CvClassic, CvWhyCnn, CvCnn, CvPool, CvHier, CvImagenet, CvTrain,
} from "./CVScenesA";

// cv_classify -------------------------------------------------------------------
const CvClassify: React.FC<{ dur?: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const probs = [
    { nm: "cat", v: 91, c: C.green }, { nm: "dog", v: 6, c: C.muted },
    { nm: "fox", v: 2, c: C.muted }, { nm: "rabbit", v: 1, c: C.muted },
  ];
  return (
    <Stage>
      <Head kicker="CORE TASK 1" title="Classification: one image, one answer" color={C.green} o={p(0, 0.06)} />
      <div style={{ position: "absolute", left: 170, top: 300, width: 380, height: 380, borderRadius: 24, background: C.bg1, border: `2.5px solid ${C.line}`, display: "flex", alignItems: "center", justifyContent: "center", fontSize: 200, opacity: p(0.05, 0.13) }}>🐱</div>
      <Brackets x={156} y={286} w={408} h={408} color={C.pix} o={p(0.08, 0.16)} />
      <ScanBeam x={172} y={302} w={376} h={376} color={C.pix} o={p(0.1, 0.2)} />
      <Flow x1={570} y1={490} x2={730} y2={490} color={C.neural} n={5} o={p(0.16, 0.24)} />
      <Card x={740} y={400} w={280} h={180} color={C.neural} o={p(0.18, 0.26)} glow>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 38, color: C.neural, textAlign: "center", marginTop: 18 }}>CNN / ViT</div>
        <div style={{ fontFamily: MONO, fontSize: 21, color: C.muted, textAlign: "center", marginTop: 6 }}>backbone</div>
      </Card>
      <Flow x1={1020} y1={490} x2={1170} y2={490} color={C.green} n={5} o={p(0.26, 0.34)} />
      <div style={{ position: "absolute", left: 1190, top: 330, width: 600 }}>
        <div style={{ fontFamily: MONO, fontSize: 23, color: C.muted, marginBottom: 14, opacity: p(0.3, 0.38) }}>softmax → % over classes</div>
        {probs.map((pr, i) => {
          const grow = p(0.32 + i * 0.05, 0.5 + i * 0.05);
          const wig = pr.nm === "cat" ? Math.sin(frame * 0.06) * 1.5 : 0;
          return (
            <div key={i} style={{ display: "flex", alignItems: "center", gap: 16, marginBottom: 16, opacity: p(0.3 + i * 0.05, 0.38 + i * 0.05) }}>
              <span style={{ fontFamily: MONO, fontSize: 27, color: C.text, width: 110 }}>{pr.nm}</span>
              <div style={{ flex: 1, height: 44, background: C.panel, borderRadius: 10, overflow: "hidden", border: `1.5px solid ${C.line}` }}>
                <div style={{ width: `${(pr.v + wig) * grow}%`, height: "100%", background: `linear-gradient(90deg, ${pr.c}, ${mix(pr.c, C.bg1, 0.3)})`, borderRadius: 10 }} />
              </div>
              <span style={{ fontFamily: MONO, fontWeight: 800, fontSize: 28, color: pr.c, width: 90 }}>{Math.round((pr.v + wig) * grow)}%</span>
            </div>
          );
        })}
        <div style={{ marginTop: 18, opacity: p(0.56, 0.64) }}>
          <span style={{ fontFamily: SANS, fontWeight: 800, fontSize: 32, color: C.green, background: mix(C.panel, C.green, 0.12), border: `2.5px solid ${C.green}`, borderRadius: 14, padding: "10px 26px" }}>top-1: “cat” ✓</span>
        </div>
      </div>
      <div style={{ position: "absolute", left: 170, top: 780, right: 170, display: "flex", gap: 18, opacity: p(0.7, 0.78) }}>
        {["quality control", "content moderation", "medical triage", "the backbone inside every other task"].map((u, i) => (
          <div key={i} style={{ fontFamily: MONO, fontSize: 22, color: C.pix, background: mix(C.panel, C.pix, 0.08), border: `1.5px solid ${mix(C.line, C.pix, 0.6)}`, borderRadius: 999, padding: "10px 22px", opacity: p(0.7 + i * 0.03, 0.78 + i * 0.03) }}>{u}</div>
        ))}
      </div>
      <Foot p={p(0.84, 0.93)}>The engine in its purest form: image in, probability per class out.</Foot>
    </Stage>
  );
};

// cv_detect — YOLO grid + NMS + live tracking ------------------------------------
const CvDetect: React.FC<{ dur?: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const SX = 150, SY = 260, SW = 1100, SH = 520;
  // moving car — its box tracks it live
  const carX = SX + 90 + ((frame * 1.5) % (SW - 260));
  const objs = [
    { e: "🚶", x: SX + 700, y: SY + 200, w: 110, h: 140, nm: "person .88", c: C.green },
    { e: "🐕", x: SX + 200, y: SY + 160, w: 120, h: 100, nm: "dog .83", c: C.classic },
    { e: "🚦", x: SX + 460, y: SY + 40, w: 90, h: 150, nm: "light .95", c: C.pix },
  ];
  const gridOn = p(0.14, 0.22);
  const cand = p(0.26, 0.34);
  const nms = p(0.42, 0.52);
  const finalB = p(0.5, 0.58);
  return (
    <Stage>
      <Head kicker="CORE TASK 2" title="Detection: what AND where — in one pass" color={C.green} o={p(0, 0.06)} />
      {/* scene */}
      <div style={{ position: "absolute", left: SX, top: SY, width: SW, height: SH, borderRadius: 22, background: `linear-gradient(180deg, ${C.bg2}, ${C.bg1})`, border: `2.5px solid ${C.line}`, overflow: "hidden", opacity: p(0.04, 0.12) }}>
        {/* road */}
        <div style={{ position: "absolute", left: 0, bottom: 60, width: "100%", height: 4, background: C.line }} />
        {objs.map((o, i) => (
          <span key={i} style={{ position: "absolute", left: o.x - SX, top: o.y - SY, fontSize: o.h * 0.8 }}>{o.e}</span>
        ))}
        <span style={{ position: "absolute", left: carX - SX, top: 378, fontSize: 110 }}>🚗</span>
        {/* YOLO grid */}
        <div style={{
          position: "absolute", inset: 0, opacity: gridOn * 0.5,
          backgroundImage: `linear-gradient(${mix(C.green, C.bg1, 0.35)} 1.5px, transparent 1.5px), linear-gradient(90deg, ${mix(C.green, C.bg1, 0.35)} 1.5px, transparent 1.5px)`,
          backgroundSize: `${SW / 8}px ${SH / 5}px`,
        }} />
        {/* candidate boxes (duplicates) fade under NMS */}
        {Array.from({ length: 14 }).map((_, i) => {
          const bx = 60 + rnd(i, 1) * (SW - 260), by = 40 + rnd(i, 2) * (SH - 220);
          return (
            <div key={i} style={{
              position: "absolute", left: bx, top: by, width: 120 + rnd(i, 3) * 120, height: 90 + rnd(i, 4) * 100,
              border: `2px solid ${mix(C.green, C.bg1, 0.25)}`, borderRadius: 8,
              opacity: cand * (1 - nms) * (0.35 + rnd(i, 5) * 0.4),
            }} />
          );
        })}
      </div>
      <Brackets x={SX - 14} y={SY - 14} w={SW + 28} h={SH + 28} color={C.green} o={p(0.06, 0.14)} />
      {/* final boxes */}
      {objs.map((o, i) => (
        <React.Fragment key={i}>
          <div style={{ position: "absolute", left: o.x - 12, top: o.y - 10, width: o.w, height: o.h, border: `3.5px solid ${o.c}`, borderRadius: 10, opacity: finalB, boxShadow: `0 0 24px ${mix(C.bg0, o.c, 0.5)}` }} />
          <div style={{ position: "absolute", left: o.x - 12, top: o.y - 46, fontFamily: MONO, fontWeight: 700, fontSize: 22, color: C.bg0, background: o.c, borderRadius: 6, padding: "2px 12px", opacity: finalB }}>{o.nm}</div>
        </React.Fragment>
      ))}
      {/* tracking box on the moving car */}
      <div style={{ position: "absolute", left: carX - 10, top: SY + 370, width: 132, height: 116, border: `3.5px solid ${C.gen}`, borderRadius: 10, opacity: finalB, boxShadow: `0 0 24px ${mix(C.bg0, C.gen, 0.5)}` }} />
      <div style={{ position: "absolute", left: carX - 10, top: SY + 328, fontFamily: MONO, fontWeight: 700, fontSize: 22, color: C.bg0, background: C.gen, borderRadius: 6, padding: "2px 12px", opacity: finalB }}>car .97 · id 4</div>
      {/* side panel */}
      <div style={{ position: "absolute", left: 1310, top: 280, width: 490 }}>
        {[
          { at: 0.14, t: "grid the image — each cell predicts boxes + class + confidence (YOLO)", c: C.green },
          { at: 0.3, t: "thousands of candidates come out…", c: C.muted },
          { at: 0.44, t: "NMS: delete overlapping duplicates", c: C.classic },
          { at: 0.56, t: "clean boxes — in ONE forward pass", c: C.green },
        ].map((s, i) => (
          <div key={i} style={{ fontFamily: SANS, fontSize: 27, color: C.text, background: mix(C.panel, s.c, 0.08), border: `2px solid ${mix(C.line, s.c, 0.7)}`, borderLeft: `5px solid ${s.c}`, borderRadius: 12, padding: "14px 20px", marginBottom: 14, opacity: p(s.at, s.at + 0.08), transform: `translateX(${(1 - p(s.at, s.at + 0.08)) * 24}px)` }}>{s.t}</div>
        ))}
        <div style={{ display: "flex", alignItems: "baseline", gap: 12, marginTop: 8, opacity: p(0.66, 0.74) }}>
          <Counter p={p(0.66, 0.8)} to={100} suffix="+" color={C.green} size={54} />
          <span style={{ fontFamily: MONO, fontSize: 25, color: C.muted }}>frames / second — real time</span>
        </div>
      </div>
      <Foot p={p(0.84, 0.93)}>The workhorse of self-driving, CCTV and sports. (The R-CNN family trades speed for accuracy when you can afford it.)</Foot>
    </Stage>
  );
};

// cv_segment -----------------------------------------------------------------------
const CvSegment: React.FC<{ dur?: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const SX = 140, SY = 270, SW = 760, SH = 470;
  const sem = p(0.12, 0.3);
  const inst = p(0.4, 0.5);
  const sam = p(0.78, 0.86);
  const blobs = [
    { x: 90, y: 240, w: 200, h: 190, c: C.green, nm: "person", ic: "🧍" },
    { x: 320, y: 250, w: 200, h: 180, c: C.green, nm: "person", ic: "🧍" },
    { x: 560, y: 300, w: 160, h: 130, c: C.classic, nm: "dog", ic: "🐕" },
  ];
  return (
    <Stage>
      <Head kicker="CORE TASK 3" title="Segmentation: decide every single pixel" color={C.neural} o={p(0, 0.06)} />
      <div style={{ position: "absolute", left: SX, top: SY, width: SW, height: SH, borderRadius: 22, background: `linear-gradient(180deg, ${C.bg2}, ${C.bg1})`, border: `2.5px solid ${C.line}`, overflow: "hidden", opacity: p(0.04, 0.12) }}>
        {/* sky/ground semantic wash */}
        <div style={{ position: "absolute", inset: 0, background: `linear-gradient(180deg, ${mix(C.pix, C.bg1, 0.75)} 0%, transparent 55%)`, opacity: sem * 0.7 }} />
        <div style={{ position: "absolute", left: 0, bottom: 0, width: "100%", height: 110, background: mix(C.neural, C.bg1, 0.7), opacity: sem * 0.7 }} />
        {blobs.map((b, i) => (
          <React.Fragment key={i}>
            <span style={{ position: "absolute", left: b.x + 40, top: b.y + 20, fontSize: 110 }}>{b.ic}</span>
            {/* mask grows like a paint fill */}
            <div style={{
              position: "absolute", left: b.x + b.w / 2 - (b.w / 2) * sem, top: b.y + b.h / 2 - (b.h / 2) * sem,
              width: b.w * sem, height: b.h * sem, borderRadius: 34,
              background: inst > 0.5 ? [C.green, C.pix, C.classic][i] : b.c,
              opacity: 0.4, border: `2.5px solid ${inst > 0.5 ? [C.green, C.pix, C.classic][i] : b.c}`,
            }} />
            {inst > 0.5 && (
              <div style={{ position: "absolute", left: b.x + 8, top: b.y - 6, fontFamily: MONO, fontWeight: 700, fontSize: 20, color: C.bg0, background: [C.green, C.pix, C.classic][i], borderRadius: 6, padding: "2px 10px", opacity: inst }}>
                {b.nm} #{i + 1}
              </div>
            )}
          </React.Fragment>
        ))}
        {/* SAM click ripple */}
        <div style={{ position: "absolute", left: 168, top: 320, opacity: sam }}>
          <div style={{ width: 20, height: 20, borderRadius: 20, background: C.gen, boxShadow: `0 0 20px ${C.gen}` }} />
          <div style={{ position: "absolute", left: 10 - ((frame * 1.4) % 60), top: 10 - ((frame * 1.4) % 60), width: ((frame * 1.4) % 60) * 2, height: ((frame * 1.4) % 60) * 2, borderRadius: 999, border: `2.5px solid ${C.gen}`, opacity: 1 - ((frame * 1.4) % 60) / 60 }} />
          <span style={{ position: "absolute", left: 30, top: -6, fontFamily: MONO, fontSize: 21, color: C.gen, whiteSpace: "nowrap" }}>SAM: click → mask anything</span>
        </div>
      </div>
      {/* semantic vs instance labels */}
      <div style={{ position: "absolute", left: SX, top: SY + SH + 22, display: "flex", gap: 20 }}>
        <span style={{ fontFamily: MONO, fontSize: 24, color: C.green, opacity: sem, textDecoration: inst > 0.5 ? "line-through" : "none" }}>semantic: all people = one class</span>
        <span style={{ fontFamily: MONO, fontSize: 24, color: C.pix, opacity: inst }}>instance: person #1 ≠ person #2 (Mask R-CNN)</span>
      </div>
      {/* U-Net mini diagram */}
      <div style={{ position: "absolute", left: 1000, top: 290, width: 800, opacity: p(0.56, 0.64) }}>
        <div style={{ fontFamily: MONO, fontSize: 23, color: C.muted, marginBottom: 16 }}>the U-Net shape — down to understand, up to paint</div>
        <svg width={760} height={360}>
          {[0, 1, 2].map((i) => (
            <rect key={`d${i}`} x={40 + i * 110} y={30 + i * 90} width={70 - i * 14} height={90 - i * 18} rx={10}
              fill={mix(C.panel, C.neural, 0.3)} stroke={C.neural} strokeWidth={2.5} opacity={p(0.58 + i * 0.04, 0.66 + i * 0.04)} />
          ))}
          {[2, 1, 0].map((i, k) => (
            <rect key={`u${i}`} x={420 + k * 110} y={30 + i * 90} width={70 - i * 14} height={90 - i * 18} rx={10}
              fill={mix(C.panel, C.green, 0.3)} stroke={C.green} strokeWidth={2.5} opacity={p(0.66 + k * 0.04, 0.74 + k * 0.04)} />
          ))}
          {/* skip connections */}
          {[0, 1, 2].map((i) => (
            <line key={`s${i}`} x1={112 + i * 110 - i * 14} y1={70 + i * 90} x2={418 + (2 - i) * 110} y2={70 + i * 90}
              stroke={C.pix} strokeWidth={2.5} strokeDasharray="8 8" strokeDashoffset={-frame * 0.8}
              opacity={p(0.72, 0.8) * 0.8} />
          ))}
          <text x={40} y={350} fontFamily={MONO} fontSize={21} fill={C.muted} opacity={p(0.74, 0.82)}>skip connections keep the fine detail — medical imaging's favorite</text>
        </svg>
      </div>
      <Foot p={p(0.86, 0.94)}>Detection draws a box; segmentation traces the exact outline — per-pixel classification.</Foot>
    </Stage>
  );
};

// cv_face ------------------------------------------------------------------------------
const CvFace: React.FC<{ dur?: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const emb = (seed: number) => Array.from({ length: 14 }).map((_, i) => rnd(i, seed));
  const e1 = emb(1), e2 = emb(1.02), e3 = emb(7);
  const VecBar: React.FC<{ e: number[]; x: number; y: number; c: string; o: number; label: string }> = ({ e, x, y, c, o, label }) => (
    <div style={{ position: "absolute", left: x, top: y, opacity: o }}>
      <div style={{ display: "flex", gap: 3 }}>
        {e.map((v, i) => <div key={i} style={{ width: 22, height: 52, borderRadius: 5, background: mix(C.bg1, c, 0.25 + v * 0.65) }} />)}
      </div>
      <div style={{ fontFamily: MONO, fontSize: 20, color: C.muted, marginTop: 6 }}>{label}</div>
    </div>
  );
  const d12 = p(0.5, 0.62), d13 = p(0.68, 0.8);
  return (
    <Stage>
      <Head kicker="CORE TASK 4" title="Face recognition: a fingerprint made of numbers" color={C.pix} o={p(0, 0.06)} />
      {/* pipeline on face 1 */}
      <div style={{ position: "absolute", left: 160, top: 290, width: 300, height: 300, borderRadius: 22, background: C.bg1, border: `2.5px solid ${C.line}`, display: "flex", alignItems: "center", justifyContent: "center", fontSize: 170, opacity: p(0.04, 0.12) }}>🙂</div>
      <div style={{ position: "absolute", left: 186, top: 316, width: 248, height: 248, border: `3px solid ${C.green}`, borderRadius: 14, opacity: p(0.1, 0.17) }} />
      {/* landmarks */}
      {[[248, 402], [332, 402], [290, 452], [258, 500], [322, 500]].map(([x, y], i) => (
        <div key={i} style={{ position: "absolute", left: x, top: y, width: 14, height: 14, borderRadius: 8, background: C.classic, boxShadow: `0 0 12px ${C.classic}`, opacity: p(0.16 + i * 0.02, 0.22 + i * 0.02), transform: `scale(${0.8 + Math.sin(frame * 0.1 + i) * 0.15})` }} />
      ))}
      <div style={{ position: "absolute", left: 160, top: 620, fontFamily: MONO, fontSize: 21, color: C.muted, opacity: p(0.18, 0.26) }}>1 detect → 2 landmarks → 3 align</div>
      <Flow x1={470} y1={440} x2={620} y2={440} color={C.neural} n={4} o={p(0.26, 0.34)} />
      <Card x={630} y={380} w={250} h={130} color={C.neural} o={p(0.28, 0.36)}>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 30, color: C.neural, textAlign: "center", marginTop: 8 }}>embedding<br />network</div>
      </Card>
      <Flow x1={880} y1={440} x2={1010} y2={440} color={C.pix} n={4} o={p(0.34, 0.42)} />
      <VecBar e={e1} x={1030} y={410} c={C.pix} o={p(0.36, 0.44)} label="512-number vector — the face's fingerprint" />
      {/* comparisons */}
      <div style={{ position: "absolute", left: 160, top: 700, fontSize: 84, opacity: p(0.46, 0.54) }}>😊</div>
      <VecBar e={e2} x={300} y={716} c={C.green} o={p(0.48, 0.56)} label="same person, new photo" />
      <div style={{ position: "absolute", left: 720, top: 700, width: 380, opacity: d12 }}>
        <div style={{ fontFamily: MONO, fontSize: 22, color: C.muted }}>distance</div>
        <div style={{ height: 22, background: C.panel, borderRadius: 8, overflow: "hidden", border: `1.5px solid ${C.line}`, marginTop: 6 }}>
          <div style={{ width: `${18 * d12}%`, height: "100%", background: C.green }} />
        </div>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 32, color: C.green, marginTop: 10 }}>0.18 → MATCH ✓</div>
      </div>
      <div style={{ position: "absolute", left: 1180, top: 700, fontSize: 84, opacity: p(0.64, 0.72) }}>🧔</div>
      <VecBar e={e3} x={1310} y={716} c={C.red} o={p(0.66, 0.74)} label="different person" />
      <div style={{ position: "absolute", left: 1310, top: 820, width: 420, opacity: d13 }}>
        <div style={{ height: 22, background: C.panel, borderRadius: 8, overflow: "hidden", border: `1.5px solid ${C.line}` }}>
          <div style={{ width: `${88 * d13}%`, height: "100%", background: C.red }} />
        </div>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 32, color: C.red, marginTop: 8 }}>0.88 → NO MATCH ✗</div>
      </div>
      <Foot p={p(0.86, 0.94)}>Enroll with ONE photo — no retraining per person. (Phone unlock adds depth + liveness so a printout can't fool it.)</Foot>
    </Stage>
  );
};

// cv_vit --------------------------------------------------------------------------------
const CvVit: React.FC<{ dur?: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const split = p(0.1, 0.26);
  const toRow = p(0.3, 0.46);
  const attn = p(0.52, 0.66);
  const IMG = 390, PN = 3, PS = IMG / PN;
  const rowY = 700, rowX = 330;
  return (
    <Stage>
      <Head kicker="THE TRANSFORMER ERA" title="ViT: treat an image like a sentence" color={C.gen} o={p(0, 0.06)} />
      {/* image splitting into patches */}
      {Array.from({ length: 9 }).map((_, i) => {
        const r = Math.floor(i / 3), c = i % 3;
        const gapPx = split * 26;
        const startX = 220 + c * PS, startY = 260 + r * PS;
        const sx = 220 + c * (PS + gapPx) - gapPx, sy = 260 + r * (PS + gapPx) - gapPx;
        const tx = rowX + i * 145, ty = rowY;
        const x = sx + (tx - sx) * toRow, y = sy + (ty - sy) * toRow;
        const size = PS - 8 - toRow * 40;
        return (
          <div key={i} style={{
            position: "absolute", left: x, top: y, width: size, height: size,
            borderRadius: 14, overflow: "hidden", border: `2.5px solid ${toRow > 0.6 ? C.gen : C.pix}`,
            background: C.bg1, opacity: p(0.04 + i * 0.01, 0.12 + i * 0.01),
            boxShadow: toRow > 0.6 ? `0 0 18px ${mix(C.bg0, C.gen, 0.4)}` : "none",
          }}>
            <span style={{ position: "absolute", left: -c * (size + 4) - 8, top: -r * (size + 4) - 14, fontSize: size * 3.1 }}>🐯</span>
            {toRow > 0.6 && <div style={{ position: "absolute", right: 4, bottom: 0, fontFamily: MONO, fontSize: 17, color: C.gen }}>{i}</div>}
          </div>
        );
      })}
      <Brackets x={206} y={246} w={IMG + 26} h={IMG + 26} color={C.pix} o={p(0.03, 0.1) * (1 - toRow)} />
      <div style={{ position: "absolute", left: 240, top: 262 + IMG + 30, fontFamily: MONO, fontSize: 23, color: C.pix, opacity: p(0.12, 0.2) * (1 - toRow) }}>16×16 patches → tokens</div>
      {/* token row label */}
      <div style={{ position: "absolute", left: rowX, top: rowY + 120, fontFamily: MONO, fontSize: 23, color: C.gen, opacity: toRow }}>a sentence of patches — fed to a standard transformer</div>
      {/* attention arcs between tokens */}
      {attn > 0.02 && [[0, 4], [4, 8], [1, 7], [2, 4], [0, 8], [3, 5]].map(([a, b], i) => (
        <Wire key={i} x1={rowX + a * 145 + 45} y1={rowY} x2={rowX + b * 145 + 45} y2={rowY}
          p={interpolate(attn, [i * 0.12, i * 0.12 + 0.3], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" })}
          color={i % 2 ? C.neural : C.gen} w={2.5 + (i % 3)} curve={90 + (b - a) * 22} arrow={false} />
      ))}
      <div style={{ position: "absolute", left: rowX + 200, top: rowY - 170, fontFamily: SANS, fontSize: 27, color: C.text, opacity: p(0.6, 0.68) }}>
        <b style={{ color: C.gen }}>self-attention:</b> every patch sees every other patch — global context from layer one
      </div>
      {/* right panel */}
      <div style={{ position: "absolute", left: 1380, top: 280, width: 420 }}>
        {[
          { at: 0.2, t: "patch = token, image = sentence", c: C.gen },
          { at: 0.44, t: "same Q · K · V attention as an LLM", c: C.neural },
          { at: 0.68, t: "CNN: local → global slowly. ViT: global instantly (needs more data)", c: C.pix },
        ].map((s, i) => (
          <div key={i} style={{ fontFamily: SANS, fontSize: 27, color: C.text, background: mix(C.panel, s.c, 0.08), border: `2px solid ${mix(C.line, s.c, 0.7)}`, borderLeft: `5px solid ${s.c}`, borderRadius: 12, padding: "16px 22px", marginBottom: 16, opacity: p(s.at, s.at + 0.08), transform: `translateX(${(1 - p(s.at, s.at + 0.08)) * 24}px)`, lineHeight: 1.35 }}>{s.t}</div>
        ))}
      </div>
      <Foot p={p(0.84, 0.93)}>If you know attention from language models, you already know ViT — the tokens are just patches instead of words.</Foot>
    </Stage>
  );
};

// cv_clip -------------------------------------------------------------------------------
const CvClip: React.FC<{ dur?: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const pull = p(0.26, 0.46);
  const zs = p(0.6, 0.72);
  const PX = 1080, PY = 300, PW = 700, PH = 520; // embedding plane
  const pairs = [
    { img: "🐱", txt: "“a photo of a cat”", ix: 200, iy: 120, tx: 560, ty: 380, hx: 320, hy: 200, c: C.pix },
    { img: "🚗", txt: "“a red car”", ix: 120, iy: 380, tx: 500, ty: 90, hx: 250, hy: 300, c: C.classic },
    { img: "🌊", txt: "“waves on a beach”", ix: 540, iy: 300, tx: 150, ty: 240, hx: 420, hy: 400, c: C.green },
  ];
  return (
    <Stage>
      <Head kicker="VISION MEETS LANGUAGE" title="CLIP: images and text in one meaning space" color={C.gen} o={p(0, 0.06)} />
      {/* encoders */}
      <Card x={140} y={300} w={330} h={170} color={C.pix} o={p(0.05, 0.13)}>
        <div style={{ fontSize: 44 }}>🖼️</div>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 30, color: C.pix }}>image encoder</div>
        <div style={{ fontFamily: MONO, fontSize: 21, color: C.muted, marginTop: 4 }}>image → vector</div>
      </Card>
      <Card x={140} y={520} w={330} h={170} color={C.classic} o={p(0.1, 0.18)}>
        <div style={{ fontSize: 44 }}>💬</div>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 30, color: C.classic }}>text encoder</div>
        <div style={{ fontFamily: MONO, fontSize: 21, color: C.muted, marginTop: 4 }}>caption → vector</div>
      </Card>
      <div style={{ position: "absolute", left: 150, top: 740, width: 700, fontFamily: MONO, fontSize: 23, color: C.muted, opacity: p(0.18, 0.26) }}>
        trained on <b style={{ color: C.gen }}>400,000,000</b> image–caption pairs: pull matches together, push mismatches apart
      </div>
      <Flow x1={470} y1={390} x2={PX + 60} y2={PY + 120} curve={-60} color={C.pix} n={5} o={p(0.14, 0.22)} />
      <Flow x1={470} y1={610} x2={PX + 60} y2={PY + 380} curve={60} color={C.classic} n={5} o={p(0.18, 0.26)} />
      {/* embedding plane */}
      <div style={{ position: "absolute", left: PX, top: PY, width: PW, height: PH, borderRadius: 24, border: `2.5px solid ${mix(C.line, C.gen, 0.6)}`, background: `radial-gradient(circle at 50% 50%, ${mix(C.bg2, C.gen, 0.08)}, ${C.bg1})`, opacity: p(0.12, 0.2) }}>
        <div style={{ position: "absolute", left: 20, top: 14, fontFamily: MONO, fontSize: 21, color: C.gen }}>shared embedding space</div>
        {pairs.map((pr, i) => {
          const ix = pr.ix + (pr.hx - pr.ix) * pull, iy = pr.iy + (pr.hy - pr.iy) * pull;
          const tx = pr.tx + (pr.hx + 26 - pr.tx) * pull, ty = pr.ty + (pr.hy + 20 - pr.ty) * pull;
          return (
            <React.Fragment key={i}>
              <div style={{ position: "absolute", left: ix, top: iy, fontSize: 46, opacity: p(0.2 + i * 0.03, 0.28 + i * 0.03), filter: `drop-shadow(0 0 12px ${pr.c})` }}>{pr.img}</div>
              <div style={{ position: "absolute", left: tx, top: ty, fontFamily: MONO, fontSize: 20, color: pr.c, opacity: p(0.22 + i * 0.03, 0.3 + i * 0.03), background: mix(C.panel, pr.c, 0.14), border: `1.5px solid ${pr.c}`, borderRadius: 8, padding: "4px 10px" }}>{pr.txt}</div>
              {pull > 0.9 && <div style={{ position: "absolute", left: ix - 16, top: iy - 14, width: 210, height: 92, borderRadius: 18, border: `2px dashed ${pr.c}`, opacity: 0.5 + Math.sin(frame * 0.07 + i) * 0.2 }} />}
            </React.Fragment>
          );
        })}
      </div>
      {/* zero-shot */}
      <div style={{ position: "absolute", left: 570, top: 300, width: 430, opacity: zs }}>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 32, color: C.gen }}>zero-shot classification</div>
        <div style={{ fontFamily: SANS, fontSize: 26, color: C.text, marginTop: 10, lineHeight: 1.4 }}>
          embed the <b style={{ color: C.classic }}>labels as sentences</b>, embed the image, pick the nearest — classify things it was never explicitly taught.
        </div>
        <div style={{ fontFamily: MONO, fontSize: 21, color: C.muted, marginTop: 12 }}>also: image search, and the “eyes” of image generators</div>
      </div>
      <Foot p={p(0.84, 0.93)}>One shared space for pictures and words — the bridge every multimodal model walks across.</Foot>
    </Stage>
  );
};

// cv_gen — diffusion ---------------------------------------------------------------------
const CvGen: React.FC<{ dur?: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const steps = [1.0, 0.75, 0.5, 0.25, 0.0];
  const denoise = p(0.1, 0.62);
  return (
    <Stage>
      <Head kicker="VISION IN REVERSE" title="Diffusion: sculpt an image out of noise" color={C.gen} o={p(0, 0.06)} />
      {/* prompt chip */}
      <div style={{ position: "absolute", left: 150, top: 250, opacity: p(0.05, 0.13) }}>
        <span style={{ fontFamily: MONO, fontSize: 26, color: C.gen, background: mix(C.panel, C.gen, 0.12), border: `2px solid ${C.gen}`, borderRadius: 999, padding: "12px 30px" }}>
          prompt: “a cat” <span style={{ color: C.muted }}>→ text embedding steers every step</span>
        </span>
      </div>
      {steps.map((amp, i) => {
        const active = denoise * (steps.length - 1) >= i;
        const localAmp = Math.max(amp, amp === 0 ? 0 : 0);
        const g = CAT12.map((row, r) => row.map((v, c) => {
          const nz = rnd(r, c, Math.floor(frame / 5) + i * 99) * 255;
          return Math.round(v * (1 - localAmp) + nz * localAmp);
        }));
        return (
          <div key={i} style={{ opacity: active ? 1 : 0.18 }}>
            <PixGrid g={g} x={150 + i * 340} y={360} cell={24} tint={amp === 0 ? undefined : C.gen} o={p(0.08 + i * 0.02, 0.16 + i * 0.02)} />
            <div style={{ position: "absolute", left: 150 + i * 340, top: 682, fontFamily: MONO, fontSize: 22, color: active ? C.gen : C.muted }}>
              {amp === 1 ? "pure noise" : amp === 0 ? "image ✓" : `t = ${Math.round(amp * 1000)}`}
            </div>
            {i < 4 && <Wire x1={150 + i * 340 + 300} y1={505} x2={150 + (i + 1) * 340 - 14} y2={505} p={active ? 1 : 0} color={C.gen} w={3} />}
          </div>
        );
      })}
      <div style={{ position: "absolute", left: 150, top: 750, right: 150, display: "flex", gap: 24, opacity: p(0.68, 0.76) }}>
        <div style={{ flex: 1, fontFamily: SANS, fontSize: 27, color: C.text, background: mix(C.panel, C.gen, 0.08), border: `2px solid ${C.gen}`, borderRadius: 14, padding: "18px 26px", lineHeight: 1.4 }}>
          <b style={{ color: C.gen }}>training:</b> add noise to real images, learn to remove it — one denoising step at a time
        </div>
        <div style={{ flex: 1, fontFamily: SANS, fontSize: 27, color: C.text, background: mix(C.panel, C.pix, 0.08), border: `2px solid ${C.pix}`, borderRadius: 14, padding: "18px 26px", lineHeight: 1.4 }}>
          <b style={{ color: C.pix }}>same trick:</b> inpainting, style transfer, upscaling — Stable Diffusion, Midjourney, DALL·E
        </div>
      </div>
      <Foot p={p(0.85, 0.93)}>Recognition climbs from pixels to meaning; generation walks back down — meaning to pixels.</Foot>
    </Stage>
  );
};

// cv_vlm ----------------------------------------------------------------------------------
const CvVlm: React.FC<{ dur?: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  return (
    <Stage>
      <Head kicker="WHERE IT ALL LANDED" title="VLMs: vision plugged into language models" color={C.gen} o={p(0, 0.06)} />
      {/* architecture strip */}
      <div style={{ position: "absolute", left: 150, top: 260 }}>
        <PixGrid g={CAT12} x={0} y={0} cell={13} o={p(0.05, 0.12)} />
      </div>
      <Flow x1={320} y1={340} x2={430} y2={340} color={C.pix} n={4} o={p(0.1, 0.18)} />
      <Card x={440} y={280} w={300} h={130} color={C.pix} o={p(0.12, 0.2)}>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 27, color: C.pix, textAlign: "center", marginTop: 6 }}>vision encoder</div>
        <div style={{ fontFamily: MONO, fontSize: 20, color: C.muted, textAlign: "center", marginTop: 4 }}>image → tokens</div>
      </Card>
      {/* vision tokens joining text tokens */}
      <div style={{ position: "absolute", left: 790, top: 300, display: "flex", gap: 8, opacity: p(0.2, 0.28) }}>
        {["▦", "▦", "▦", "“what", "broke", "here?”"].map((t, i) => (
          <div key={i} style={{ fontFamily: MONO, fontSize: 22, color: i < 3 ? C.pix : C.classic, background: mix(C.panel, i < 3 ? C.pix : C.classic, 0.14), border: `1.5px solid ${i < 3 ? C.pix : C.classic}`, borderRadius: 9, padding: "8px 12px", transform: `translateY(${Math.sin(frame * 0.06 + i) * 3}px)` }}>{t}</div>
        ))}
      </div>
      <Flow x1={1240} y1={340} x2={1330} y2={340} color={C.neural} n={4} o={p(0.26, 0.34)} />
      <Card x={1340} y={270} w={330} h={150} color={C.neural} o={p(0.28, 0.36)} glow>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 34, color: C.neural, textAlign: "center", marginTop: 14 }}>LLM</div>
        <div style={{ fontFamily: MONO, fontSize: 20, color: C.muted, textAlign: "center", marginTop: 4 }}>reads both, answers in words</div>
      </Card>
      <div style={{ position: "absolute", left: 800, top: 245, fontFamily: MONO, fontSize: 20, color: C.muted, opacity: p(0.22, 0.3) }}>image tokens + text tokens, one sequence</div>
      {/* chat demo */}
      <div style={{ position: "absolute", left: 300, top: 470, width: 1320, borderRadius: 24, background: C.panel, border: `2.5px solid ${C.line}`, padding: "26px 34px", boxSizing: "border-box", opacity: p(0.36, 0.44) }}>
        <div style={{ fontFamily: MONO, fontSize: 21, color: C.muted, marginBottom: 14 }}>GPT-4V · Gemini · Claude</div>
        <div style={{ display: "flex", gap: 16, marginBottom: 16, opacity: p(0.4, 0.46) }}>
          <div style={{ width: 92, height: 92, borderRadius: 12, background: C.bg1, border: `2px solid ${C.pix}`, display: "flex", alignItems: "center", justifyContent: "center", fontSize: 52 }}>🐱</div>
          <div style={{ background: mix(C.panel, C.classic, 0.1), border: `2px solid ${mix(C.line, C.classic, 0.6)}`, borderRadius: 14, padding: "14px 20px", alignSelf: "center" }}>
            <Type text="What happened on my desk?" p={p(0.42, 0.52)} size={27} />
          </div>
        </div>
        <div style={{ background: mix(C.panel, C.gen, 0.09), border: `2px solid ${mix(C.line, C.gen, 0.6)}`, borderRadius: 14, padding: "16px 22px" }}>
          <Type text="Your cat knocked the coffee onto the laptop — and, judging by the posture, feels no remorse. I'd power it off and dry the keyboard first." p={p(0.52, 0.8)} size={28} />
        </div>
      </div>
      <Foot p={p(0.86, 0.94)}>Classification said “cat.” A VLM describes, reasons, and acts. Vision stopped being a separate field — it became perception for general AI.</Foot>
    </Stage>
  );
};

// cv_stack -----------------------------------------------------------------------------------
const CvStack: React.FC<{ dur?: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const tools = [
    { nm: "OpenCV", sub: "classical ops · video IO", c: C.classic },
    { nm: "PyTorch + torchvision", sub: "models & training", c: C.neural },
    { nm: "Ultralytics YOLO", sub: "detection in 5 lines", c: C.green },
    { nm: "Hugging Face", sub: "ViT · CLIP · SAM checkpoints", c: C.gen },
    { nm: "Roboflow / CVAT", sub: "labeling & datasets", c: C.pix },
    { nm: "ONNX / TensorRT", sub: "deploy · quantize · edge", c: C.classic },
  ];
  const steps = ["collect", "label", "pretrained start", "fine-tune + augment", "evaluate (mAP · IoU)", "optimize & deploy"];
  const hotTool = Math.floor(frame / 26) % tools.length;
  return (
    <Stage>
      <Head kicker="IN PRACTICE" title="The working stack — you rarely train from scratch" color={C.green} o={p(0, 0.06)} />
      {tools.map((t, i) => {
        const col = i % 3, row = Math.floor(i / 3);
        const at = 0.06 + i * 0.05;
        const active = hotTool === i && p(0.4, 0.41) > 0.5;
        return (
          <div key={i} style={{
            position: "absolute", left: 140 + col * 560, top: 260 + row * 200, width: 520, height: 170, borderRadius: 20,
            background: mix(C.panel, t.c, active ? 0.16 : 0.08), border: `2.5px solid ${active ? t.c : mix(C.line, t.c, 0.55)}`,
            padding: "24px 30px", boxSizing: "border-box", opacity: p(at, at + 0.08),
            transform: `translateY(${(1 - p(at, at + 0.08)) * 22 + (active ? -6 : 0)}px)`,
            boxShadow: active ? `0 0 44px ${mix(C.bg0, t.c, 0.4)}` : "none",
          }}>
            <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 34, color: t.c }}>{t.nm}</div>
            <div style={{ fontFamily: MONO, fontSize: 23, color: C.muted, marginTop: 10 }}>{t.sub}</div>
          </div>
        );
      })}
      {/* workflow pipeline */}
      <div style={{ position: "absolute", left: 140, top: 700, right: 140, opacity: p(0.5, 0.58) }}>
        <div style={{ fontFamily: MONO, fontSize: 23, color: C.muted, marginBottom: 16 }}>the workflow:</div>
        <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
          {steps.map((s, i) => {
            const at = 0.52 + i * 0.055;
            const on = p(at, at + 0.05);
            return (
              <React.Fragment key={i}>
                {i > 0 && <div style={{ fontFamily: MONO, fontSize: 26, color: C.green, opacity: p(at - 0.02, at) }}>→</div>}
                <div style={{ fontFamily: MONO, fontWeight: 700, fontSize: 23, color: on > 0.5 ? C.bg0 : C.green, background: on > 0.5 ? C.green : mix(C.panel, C.green, 0.1), border: `2px solid ${C.green}`, borderRadius: 999, padding: "12px 22px", opacity: p(at - 0.02, at + 0.03), transform: `scale(${0.94 + on * 0.06})` }}>
                  {i + 1} {s}
                </div>
              </React.Fragment>
            );
          })}
        </div>
      </div>
      <Foot p={p(0.87, 0.95)}>Modern CV is assembly, not alchemy: pretrained backbone + your labeled data + an afternoon of fine-tuning.</Foot>
    </Stage>
  );
};

// cv_hard -------------------------------------------------------------------------------------
const CvHard: React.FC<{ dur?: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const cards = [
    { t: "Lighting & weather", sub: "night, rain, glare, blur", icon: "🌧️", c: C.pix, demo: "dim" },
    { t: "Occlusion", sub: "objects hide behind objects", icon: "🫣", c: C.classic, demo: "occl" },
    { t: "Long tail", sub: "rare classes, few examples", icon: "📉", c: C.neural, demo: "tail" },
    { t: "Domain shift", sub: "trained here, deployed there", icon: "🌍", c: C.green, demo: "shift" },
    { t: "Adversarial", sub: "patterns that fool the model", icon: "🎭", c: C.red, demo: "adv" },
    { t: "Bias & fairness", sub: "uneven accuracy across people", icon: "⚖️", c: C.gen, demo: "bias" },
  ];
  const hot = Math.floor(frame / 28) % cards.length;
  return (
    <Stage>
      <Head kicker="STILL HARD" title="Not solved — engineerable" color={C.red} o={p(0, 0.06)} />
      {cards.map((cd, i) => {
        const col = i % 3, row = Math.floor(i / 3);
        const at = 0.07 + i * 0.09;
        const o = p(at, at + 0.09);
        const active = hot === i && p(0.6, 0.61) > 0.5;
        return (
          <div key={i} style={{
            position: "absolute", left: 140 + col * 560, top: 260 + row * 280, width: 520, height: 250, borderRadius: 20,
            background: mix(C.panel, cd.c, active ? 0.15 : 0.07), border: `2.5px solid ${active ? cd.c : mix(C.line, cd.c, 0.55)}`,
            padding: "24px 28px", boxSizing: "border-box", opacity: o, transform: `translateY(${(1 - o) * 24 + (active ? -7 : 0)}px)`,
            boxShadow: active ? `0 0 46px ${mix(C.bg0, cd.c, 0.4)}` : "none",
          }}>
            <div style={{ display: "flex", alignItems: "center", gap: 14 }}>
              <span style={{ fontSize: 42 }}>{cd.icon}</span>
              <span style={{ fontFamily: SANS, fontWeight: 800, fontSize: 31, color: cd.c }}>{cd.t}</span>
            </div>
            <div style={{ fontFamily: MONO, fontSize: 23, color: C.muted, marginTop: 10 }}>{cd.sub}</div>
            <div style={{ position: "relative", height: 106, marginTop: 14, borderRadius: 12, background: C.bg1, border: `1.5px solid ${C.line}`, overflow: "hidden" }}>
              <HardDemo kind={cd.demo} color={cd.c} on={o > 0.9} />
            </div>
          </div>
        );
      })}
      <div style={{ position: "absolute", left: 140, top: 830, right: 140, textAlign: "center", opacity: p(0.78, 0.86) }}>
        <span style={{ fontFamily: MONO, fontSize: 24, color: C.green, background: mix(C.panel, C.green, 0.1), border: `2px solid ${C.green}`, borderRadius: 999, padding: "12px 30px" }}>
          + the edge constraint: 30 fps on a few watts — quantize, prune, distill
        </span>
      </div>
    </Stage>
  );
};

const HardDemo: React.FC<{ kind: string; color: string; on: boolean }> = ({ kind, color, on }) => {
  const frame = useCurrentFrame();
  if (!on) return null;
  const t = (frame % 100) / 100;
  switch (kind) {
    case "dim": {
      const dim = 0.25 + (Math.sin(frame * 0.05) + 1) * 0.3;
      return (<><span style={{ position: "absolute", left: 40, top: 18, fontSize: 56, opacity: dim }}>🚶</span><span style={{ position: "absolute", left: 200, top: 30, fontFamily: MONO, fontSize: 22, color, opacity: 1 - dim }}>conf {Math.round(30 + dim * 60)}%</span></>);
    }
    case "occl":
      return (<><span style={{ position: "absolute", left: 44, top: 18, fontSize: 56 }}>🐕</span><div style={{ position: "absolute", left: 20 + Math.sin(frame * 0.04) * 30 + 30, top: 0, width: 90, height: 106, background: mix(C.bg1, color, 0.5), borderRadius: 8, opacity: 0.9 }} /><span style={{ position: "absolute", left: 210, top: 34, fontFamily: MONO, fontSize: 22, color }}>dog? 41%</span></>);
    case "tail": {
      return (<svg width={480} height={106}>{Array.from({ length: 18 }).map((_, i) => { const h = 88 * Math.exp(-i * 0.32); return <rect key={i} x={16 + i * 25} y={98 - h} width={18} height={h} rx={4} fill={i < 3 ? color : mix(color, C.bg1, 0.6)} />; })}<text x={300} y={40} fontFamily={MONO} fontSize={20} fill={color}>most classes: barely any data</text></svg>);
    }
    case "shift":
      return (<><span style={{ position: "absolute", left: 30, top: 20, fontSize: 50, filter: "saturate(1)" }}>☀️</span><span style={{ position: "absolute", left: 110, top: 34, fontFamily: MONO, fontSize: 24, color: C.green }}>98%</span><span style={{ position: "absolute", left: 230, top: 20, fontSize: 50 }}>🌫️</span><span style={{ position: "absolute", left: 310, top: 34, fontFamily: MONO, fontSize: 24, color }}>71% ↓</span></>);
    case "adv": {
      const cells = Array.from({ length: 24 }).map((_, i) => <div key={i} style={{ position: "absolute", left: 40 + (i % 6) * 13, top: 22 + Math.floor(i / 6) * 13, width: 11, height: 11, background: mix(C.bg1, color, rnd(i, 9, Math.floor(frame / 4))), borderRadius: 2 }} />);
      return (<>{cells}<span style={{ position: "absolute", left: 150, top: 34, fontFamily: MONO, fontSize: 22, color: C.text }}>+ sticker → <b style={{ color }}>“toaster”</b></span></>);
    }
    case "bias": {
      const groups = [92, 88, 71, 64];
      return (<svg width={480} height={106}>{groups.map((v, i) => (<g key={i}><rect x={30 + i * 90} y={98 - v * 0.8} width={52} height={v * 0.8} rx={6} fill={i < 2 ? C.green : color} opacity={0.85} /><text x={36 + i * 90} y={92 - v * 0.8} fontFamily={MONO} fontSize={19} fill={i < 2 ? C.green : color}>{v}%</text></g>))}<text x={310} y={40} fontFamily={MONO} fontSize={19} fill={color}>must audit</text></svg>);
    }
    default: return null;
  }
};

// cv_recap -------------------------------------------------------------------------------------
const CvRecap: React.FC<{ dur?: number; items?: string[]; closer?: string }> = ({
  dur, items = [], closer = "Computer vision — from pixels to perception.",
}) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  return (
    <AbsoluteFill style={{ padding: "64px 130px", justifyContent: "center" }}>
      <div style={{ position: "absolute", left: 60, top: 60, opacity: 0.5 }}>
        <PixGrid g={CAT12} x={0} y={0} cell={10} tint={C.pix} o={0.6} />
      </div>
      <Brackets x={40} y={40} w={BW - 80} h={BH - 80} color={mix(C.pix, C.bg1, 0.4)} o={p(0.02, 0.1)} len={60} />
      <div style={{ opacity: p(0, 0.06), textAlign: "center", marginBottom: 26 }}>
        <Kicker text="RECAP — THE WHOLE MAP" cx />
        <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 60, color: C.text, marginTop: 12, letterSpacing: -1.5 }}>Computer vision in one breath</div>
      </div>
      <div style={{ display: "flex", flexDirection: "column", gap: 12, maxWidth: 1380, margin: "0 auto", width: "100%" }}>
        {items.map((it, i) => {
          const at = 0.05 + i * 0.085;
          const o = p(at, at + 0.065);
          return (
            <div key={i} style={{ display: "flex", alignItems: "center", gap: 18, opacity: o, transform: `translateX(${(1 - o) * -26}px)`, background: mix(C.panel, C.pix, 0.05), border: `1.5px solid ${C.line}`, borderLeft: `4px solid ${C.pix}`, borderRadius: 12, padding: "14px 26px" }}>
              <span style={{ color: C.pix, fontFamily: MONO, fontWeight: 700, fontSize: 25 }}>{i + 1}</span>
              <span style={{ fontFamily: SANS, fontSize: 29, color: C.text, lineHeight: 1.25 }}>{it}</span>
            </div>
          );
        })}
      </div>
      <div style={{ textAlign: "center", marginTop: 30, opacity: p(0.82, 0.9) }}>
        <div style={{ fontFamily: SANS, fontWeight: 800, fontStyle: "italic", fontSize: 42, color: C.pix, textShadow: `0 0 ${30 + Math.sin(frame * 0.06) * 14}px ${mix(C.bg0, C.pix, 0.7)}` }}>{closer}</div>
      </div>
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------- code engine
type Ln = { t: string; c?: string };
const kw = C.gen, str = C.green, com = C.muted, num = C.classic, fn = C.pix;

/** Line-numbered code panel: reveals lines over `reveal` (0..1), blinking cursor
 *  on the newest line, and a marching highlight band for continuous motion. */
const CodeBlock: React.FC<{
  lines: Ln[]; x: number; y: number; w: number; reveal: number;
  title?: string; accent?: string; size?: number;
}> = ({ lines, x, y, w, reveal, title, accent = C.neural, size = 25 }) => {
  const frame = useCurrentFrame();
  const shown = Math.round(lines.length * Math.max(0, Math.min(1, reveal)));
  const rowH = Math.round(size * 1.52);
  const hot = shown > 0 ? Math.floor(frame / 32) % shown : -1;
  return (
    <div style={{
      position: "absolute", left: x, top: y, width: w, borderRadius: 18,
      background: `linear-gradient(180deg, ${mix(C.panel, accent, 0.06)}, ${C.bg1})`,
      border: `2.5px solid ${mix(C.line, accent, 0.5)}`, padding: "18px 24px 22px", boxSizing: "border-box",
      boxShadow: `0 0 44px ${mix(C.bg0, accent, 0.18)}`,
    }}>
      {title && (
        <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 14 }}>
          <span style={{ width: 12, height: 12, borderRadius: 8, background: C.red }} />
          <span style={{ width: 12, height: 12, borderRadius: 8, background: C.classic }} />
          <span style={{ width: 12, height: 12, borderRadius: 8, background: C.green }} />
          <span style={{ fontFamily: MONO, fontSize: 20, color: accent, marginLeft: 8, letterSpacing: 1 }}>{title}</span>
        </div>
      )}
      {lines.map((ln, i) => {
        const vis = i < shown;
        const isHot = i === hot && vis;
        return (
          <div key={i} style={{
            display: "flex", gap: 16, alignItems: "baseline", height: rowH,
            opacity: vis ? 1 : 0, background: isHot ? mix(C.panel, accent, 0.16) : "transparent",
            borderRadius: 6, marginLeft: -8, paddingLeft: 8,
          }}>
            <span style={{ fontFamily: MONO, fontSize: Math.round(size * 0.72), color: mix(C.muted, C.bg1, 0.35), width: 26, textAlign: "right", flexShrink: 0 }}>{i + 1}</span>
            <span style={{ fontFamily: MONO, fontSize: size, color: ln.c || C.text, whiteSpace: "pre" }}>
              {ln.t}{i === shown - 1 && Math.floor(frame / 8) % 2 === 0 ? <span style={{ color: accent }}>▌</span> : ""}
            </span>
          </div>
        );
      })}
    </div>
  );
};

/** Small labelled tensor-shape chip used in the code chapter's right column. */
const ShapeChip: React.FC<{ label: string; shape: string; c: string; o: number }> = ({ label, shape, c, o }) => (
  <div style={{ opacity: o, transform: `translateY(${(1 - o) * 16}px)` }}>
    <div style={{ fontFamily: MONO, fontSize: 20, color: C.muted, marginBottom: 4 }}>{label}</div>
    <div style={{ fontFamily: MONO, fontWeight: 800, fontSize: 30, color: c, background: mix(C.panel, c, 0.12), border: `2px solid ${c}`, borderRadius: 12, padding: "10px 20px", display: "inline-block" }}>{shape}</div>
  </div>
);

// cv_code_setup — data & transforms -----------------------------------------------
const CvCodeSetup: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur);
  const lines: Ln[] = [
    { t: "import torch", c: kw },
    { t: "from torchvision import datasets, transforms", c: kw },
    { t: "" },
    { t: "tf = transforms.Compose([", c: C.text },
    { t: "    transforms.ToTensor(),", c: fn },
    { t: "    transforms.Normalize((0.5,), (0.5,)),", c: fn },
    { t: "])", c: C.text },
    { t: "" },
    { t: "train = datasets.CIFAR10(\"./data\", train=True,", c: C.text },
    { t: "                         download=True, transform=tf)", c: C.text },
    { t: "loader = torch.utils.data.DataLoader(", c: C.text },
    { t: "    train, batch_size=64, shuffle=True)", c: C.text },
  ];
  return (
    <Stage>
      <Head kicker="CODE · PYTORCH — STEP 1" title="Load the images as tensors" color={C.neural} o={p(0, 0.06)} />
      <CodeBlock lines={lines} x={120} y={230} w={1040} reveal={p(0.06, 0.74)} title="data.py" accent={C.neural} />
      <ScanBeam x={120} y={230} w={1040} h={520} color={C.neural} o={p(0.1, 0.2) * 0.5} speed={0.7} />
      {/* right: one image tensor becomes a batch */}
      <div style={{ position: "absolute", left: 1250, top: 300 }}>
        <PixGrid g={CAT12} x={0} y={0} cell={20} o={p(0.2, 0.3)} label="one 32×32 image" />
      </div>
      <Flow x1={1360} y1={560} x2={1360} y2={628} curve={0} color={C.pix} n={4} o={p(0.42, 0.5)} />
      <div style={{ position: "absolute", left: 1230, top: 640, display: "flex", flexDirection: "column", gap: 22 }}>
        <ShapeChip label="image → tensor" shape="[3, 32, 32]" c={C.pix} o={p(0.34, 0.44)} />
        <ShapeChip label="a batch of 64" shape="[64, 3, 32, 32]" c={C.green} o={p(0.56, 0.66)} />
      </div>
      <Foot p={p(0.82, 0.9)}>ToTensor scales 0–255 pixels to 0–1 floats; the DataLoader serves shuffled batches of 64.</Foot>
    </Stage>
  );
};

// cv_code_model — the nn.Module -----------------------------------------------------
const CvCodeModel: React.FC<{ dur?: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const lines: Ln[] = [
    { t: "class SmallCNN(nn.Module):", c: kw },
    { t: "    def __init__(self):", c: kw },
    { t: "        super().__init__()", c: C.text },
    { t: "        self.conv1 = nn.Conv2d(3, 32, 3, padding=1)", c: fn },
    { t: "        self.conv2 = nn.Conv2d(32, 64, 3, padding=1)", c: fn },
    { t: "        self.pool  = nn.MaxPool2d(2)", c: fn },
    { t: "        self.fc    = nn.Linear(64*8*8, 10)", c: fn },
    { t: "" },
    { t: "    def forward(self, x):", c: kw },
    { t: "        x = self.pool(F.relu(self.conv1(x)))", c: C.text },
    { t: "        x = self.pool(F.relu(self.conv2(x)))", c: C.text },
    { t: "        x = x.flatten(1)", c: C.text },
    { t: "        return self.fc(x)", c: kw },
  ];
  const flow = [
    { s: "3×32×32", c: C.pix, at: 0.34 },
    { s: "32×16×16", c: C.classic, at: 0.44 },
    { s: "64×8×8", c: C.neural, at: 0.54 },
    { s: "10 logits", c: C.green, at: 0.64 },
  ];
  return (
    <Stage>
      <Head kicker="CODE · PYTORCH — STEP 2" title="Define the network" color={C.neural} o={p(0, 0.06)} />
      <CodeBlock lines={lines} x={110} y={210} w={1080} reveal={p(0.06, 0.72)} title="model.py" accent={C.neural} size={24} />
      {/* right: shape flow through the layers */}
      <div style={{ position: "absolute", left: 1290, top: 250, fontFamily: MONO, fontSize: 22, color: C.muted, opacity: p(0.3, 0.38) }}>tensor shape, layer by layer</div>
      {flow.map((f, i) => {
        const o = p(f.at, f.at + 0.08);
        const yy = 300 + i * 150;
        return (
          <React.Fragment key={i}>
            <div style={{ position: "absolute", left: 1290, top: yy, width: 360, height: 96, borderRadius: 16, background: mix(C.panel, f.c, 0.1), border: `2.5px solid ${f.c}`, display: "flex", alignItems: "center", justifyContent: "center", opacity: o, transform: `translateY(${(1 - o) * 18}px)`, boxShadow: i === 3 ? `0 0 34px ${mix(C.bg0, f.c, 0.4 + Math.sin(frame * 0.06) * 0.1)}` : "none" }}>
              <span style={{ fontFamily: MONO, fontWeight: 800, fontSize: 34, color: f.c }}>{f.s}</span>
            </div>
            {i < 3 && <Flow x1={1470} y1={yy + 96} x2={1470} y2={yy + 150} color={f.c} n={3} o={p(f.at + 0.04, f.at + 0.12)} />}
          </React.Fragment>
        );
      })}
      <Foot p={p(0.8, 0.88)}>Two conv+pool blocks halve the map each time, then a linear layer turns 4096 features into 10 class scores.</Foot>
    </Stage>
  );
};

// cv_code_train — the training loop -------------------------------------------------
const CvCodeTrain: React.FC<{ dur?: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const lines: Ln[] = [
    { t: "model = SmallCNN().to(device)", c: C.text },
    { t: "opt = torch.optim.Adam(model.parameters(), lr=1e-3)", c: fn },
    { t: "loss_fn = nn.CrossEntropyLoss()", c: fn },
    { t: "" },
    { t: "for epoch in range(10):", c: kw },
    { t: "    for x, y in loader:", c: kw },
    { t: "        x, y = x.to(device), y.to(device)", c: C.text },
    { t: "        opt.zero_grad()", c: C.text },
    { t: "        out  = model(x)", c: C.text },
    { t: "        loss = loss_fn(out, y)", c: C.text },
    { t: "        loss.backward()", c: str },
    { t: "        opt.step()", c: str },
  ];
  // live loss curve — a real exponential decay drawn + a counter
  const prog = p(0.5, 0.95);
  const N = 60;
  const X0 = 1280, Y0 = 640, W = 480, H = 300;
  const pts = Array.from({ length: N }).map((_, i) => {
    const t = i / (N - 1);
    const v = 2.3 * Math.exp(-t * 2.6) + 0.28 + Math.sin(i * 1.3) * 0.03 * Math.exp(-t * 2);
    return { x: X0 + t * W, y: Y0 - ((v - 0.28) / 2.3) * H }; // high loss = top, falls to the right
  });
  const nShow = Math.max(2, Math.round(N * prog));
  const curLoss = 2.3 * Math.exp(-prog * 2.6) + 0.28;
  return (
    <Stage>
      <Head kicker="CODE · PYTORCH — STEP 3" title="Train: predict, measure, correct" color={C.neural} o={p(0, 0.06)} />
      <CodeBlock lines={lines} x={110} y={210} w={1080} reveal={p(0.06, 0.66)} title="train.py" accent={C.neural} size={24} />
      {/* right: live loss curve */}
      <div style={{ position: "absolute", left: X0, top: 300, fontFamily: MONO, fontSize: 22, color: C.muted, opacity: p(0.44, 0.52) }}>training loss</div>
      <div style={{ position: "absolute", left: X0, top: 336, display: "flex", alignItems: "baseline", gap: 10, opacity: p(0.46, 0.54) }}>
        <span style={{ fontFamily: MONO, fontWeight: 800, fontSize: 58, color: C.green, fontVariantNumeric: "tabular-nums" }}>{curLoss.toFixed(2)}</span>
        <span style={{ fontFamily: MONO, fontSize: 24, color: C.muted }}>↓ falling</span>
      </div>
      <svg style={{ position: "absolute", left: 0, top: 0, overflow: "visible" }} width={BW} height={BH}>
        <line x1={X0} y1={Y0} x2={X0 + W} y2={Y0} stroke={C.line} strokeWidth={2} />
        <line x1={X0} y1={Y0 - H} x2={X0} y2={Y0} stroke={C.line} strokeWidth={2} />
        <polyline points={pts.slice(0, nShow).map((q) => `${q.x},${q.y}`).join(" ")} fill="none" stroke={C.green} strokeWidth={4} opacity={p(0.5, 0.58)} />
        {nShow > 2 && <circle cx={pts[nShow - 1].x} cy={pts[nShow - 1].y} r={7} fill={C.green} opacity={0.7 + Math.sin(frame * 0.12) * 0.3} />}
      </svg>
      <Foot p={p(0.82, 0.9)}>Four lines are the whole loop: zero the gradients, forward, backward, step — repeated until the loss flattens.</Foot>
    </Stage>
  );
};

// cv_code_infer — inference ---------------------------------------------------------
const CvCodeInfer: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur);
  const lines: Ln[] = [
    { t: "model.eval()", c: fn },
    { t: "with torch.no_grad():", c: kw },
    { t: "    logits = model(image.unsqueeze(0))", c: C.text },
    { t: "    probs  = logits.softmax(1)", c: C.text },
    { t: "    pred   = probs.argmax(1)", c: C.text },
    { t: "" },
    { t: "print(classes[pred])   # -> 'cat'", c: com },
  ];
  const probs = [
    { nm: "cat", v: 92, c: C.green }, { nm: "dog", v: 5, c: C.muted },
    { nm: "deer", v: 2, c: C.muted }, { nm: "ship", v: 1, c: C.muted },
  ];
  return (
    <Stage>
      <Head kicker="CODE · PYTORCH — STEP 4" title="Predict on a new image" color={C.neural} o={p(0, 0.06)} />
      <CodeBlock lines={lines} x={120} y={250} w={980} reveal={p(0.06, 0.6)} title="infer.py" accent={C.neural} />
      <div style={{ position: "absolute", left: 150, top: 690, fontFamily: MONO, fontSize: 22, color: C.muted, opacity: p(0.62, 0.7) }}>eval() + no_grad() = faster, no training bookkeeping</div>
      {/* right: image → softmax bars → label */}
      <div style={{ position: "absolute", left: 1180, top: 250, width: 360, height: 250, borderRadius: 18, background: C.bg1, border: `2.5px solid ${C.line}`, display: "flex", alignItems: "center", justifyContent: "center", fontSize: 150, opacity: p(0.16, 0.24) }}>🐱</div>
      <Brackets x={1166} y={236} w={388} h={278} color={C.pix} o={p(0.2, 0.28)} />
      <div style={{ position: "absolute", left: 1180, top: 540, width: 620 }}>
        {probs.map((pr, i) => {
          const grow = p(0.5 + i * 0.05, 0.66 + i * 0.05);
          return (
            <div key={i} style={{ display: "flex", alignItems: "center", gap: 14, marginBottom: 12, opacity: p(0.48 + i * 0.05, 0.56 + i * 0.05) }}>
              <span style={{ fontFamily: MONO, fontSize: 25, color: C.text, width: 78 }}>{pr.nm}</span>
              <div style={{ flex: 1, height: 34, background: C.panel, borderRadius: 8, overflow: "hidden", border: `1.5px solid ${C.line}` }}>
                <div style={{ width: `${pr.v * grow}%`, height: "100%", background: `linear-gradient(90deg, ${pr.c}, ${mix(pr.c, C.bg1, 0.3)})` }} />
              </div>
              <span style={{ fontFamily: MONO, fontWeight: 800, fontSize: 26, color: pr.c, width: 70 }}>{Math.round(pr.v * grow)}%</span>
            </div>
          );
        })}
        <div style={{ marginTop: 14, opacity: p(0.78, 0.86) }}>
          <span style={{ fontFamily: SANS, fontWeight: 800, fontSize: 32, color: C.green, background: mix(C.panel, C.green, 0.12), border: `2.5px solid ${C.green}`, borderRadius: 14, padding: "10px 26px" }}>argmax → “cat” ✓</span>
        </div>
      </div>
      <Foot p={p(0.86, 0.94)}>That is a full computer-vision model — from raw pixels to a named prediction — in well under a hundred lines.</Foot>
    </Stage>
  );
};

// cv_sam — Segment Anything / foundation models -------------------------------------
const CvSam: React.FC<{ dur?: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const SX = 150, SY = 270, SW = 900, SH = 500;
  const objs = [
    { e: "🐈", x: 120, y: 250, w: 210, h: 180, c: C.green, at: 0.34 },
    { e: "🪴", x: 430, y: 150, w: 150, h: 240, c: C.pix, at: 0.44 },
    { e: "☕", x: 620, y: 320, w: 150, h: 150, c: C.classic, at: 0.54 },
  ];
  const ripple = (frame * 1.4) % 60;
  return (
    <Stage>
      <Head kicker="FOUNDATION MODELS" title="Segment Anything: one click, any object" color={C.gen} o={p(0, 0.06)} />
      <div style={{ position: "absolute", left: SX, top: SY, width: SW, height: SH, borderRadius: 22, background: `linear-gradient(180deg, ${C.bg2}, ${C.bg1})`, border: `2.5px solid ${C.line}`, overflow: "hidden", opacity: p(0.05, 0.13) }}>
        {objs.map((o, i) => (
          <React.Fragment key={i}>
            <span style={{ position: "absolute", left: o.x + 20, top: o.y + 10, fontSize: o.h * 0.7 }}>{o.e}</span>
            {/* prompt point */}
            <div style={{ position: "absolute", left: o.x + o.w / 2, top: o.y + o.h / 2, width: 16, height: 16, borderRadius: 10, background: C.gen, boxShadow: `0 0 16px ${C.gen}`, opacity: p(o.at - 0.06, o.at) }} />
            {/* mask fills out from the point */}
            <div style={{ position: "absolute", left: o.x + o.w / 2 - (o.w / 2) * p(o.at, o.at + 0.1), top: o.y + o.h / 2 - (o.h / 2) * p(o.at, o.at + 0.1), width: o.w * p(o.at, o.at + 0.1), height: o.h * p(o.at, o.at + 0.1), borderRadius: 26, background: mix(C.bg1, o.c, 0.5), opacity: 0.42, border: `2.5px solid ${o.c}` }} />
          </React.Fragment>
        ))}
        {/* live cursor ripple over the last object */}
        <div style={{ position: "absolute", left: 695, top: 395, width: 16, height: 16, borderRadius: 10, background: C.gen, boxShadow: `0 0 16px ${C.gen}`, opacity: p(0.56, 0.62) }} />
        <div style={{ position: "absolute", left: 703 - ripple, top: 403 - ripple, width: ripple * 2, height: ripple * 2, borderRadius: 999, border: `2px solid ${C.gen}`, opacity: (1 - ripple / 60) * p(0.56, 0.62) }} />
      </div>
      <Brackets x={SX - 14} y={SY - 14} w={SW + 28} h={SH + 28} color={C.gen} o={p(0.08, 0.16)} />
      {/* right panel */}
      <div style={{ position: "absolute", left: 1110, top: 280, width: 700 }}>
        {[
          { at: 0.2, t: "prompt with a point, a box, or a rough mask", c: C.gen },
          { at: 0.4, t: "returns a clean mask — for objects it never saw in training", c: C.green },
          { at: 0.6, t: "pretrained on 1,000,000,000+ masks → zero-shot", c: C.pix },
          { at: 0.74, t: "SAM 2 tracks the same object across a whole video", c: C.classic },
        ].map((s, i) => (
          <div key={i} style={{ fontFamily: SANS, fontSize: 28, color: C.text, background: mix(C.panel, s.c, 0.08), border: `2px solid ${mix(C.line, s.c, 0.7)}`, borderLeft: `5px solid ${s.c}`, borderRadius: 12, padding: "16px 22px", marginBottom: 16, opacity: p(s.at, s.at + 0.08), transform: `translateX(${(1 - p(s.at, s.at + 0.08)) * 24}px)`, lineHeight: 1.35 }}>{s.t}</div>
        ))}
      </div>
      <Foot p={p(0.85, 0.93)}>Foundation models flipped segmentation from “train per dataset” to “prompt one giant pretrained model.”</Foot>
    </Stage>
  );
};

// cv_selfsup — self-supervised learning ---------------------------------------------
const CvSelfsup: React.FC<{ dur?: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  // masked-autoencoder demo: hide ~40% of patches, reconstruct them
  const reveal = p(0.16, 0.32);
  const recon = p(0.5, 0.72);
  const PN = 6, PS = 60, GX = 170, GY = 300;
  const masked = (i: number) => rnd(i % PN, Math.floor(i / PN), 3) < 0.42;
  return (
    <Stage>
      <Head kicker="LEARNING WITHOUT LABELS" title="Self-supervised: hide, then predict" color={C.neural} o={p(0, 0.06)} />
      {/* patch grid with masked squares */}
      <div style={{ position: "absolute", left: GX - 16, top: GY - 44, fontFamily: MONO, fontSize: 22, color: C.muted, opacity: p(0.1, 0.18) }}>hide 40% of the patches…</div>
      {Array.from({ length: PN * PN }).map((_, i) => {
        const r = Math.floor(i / PN), c = i % PN;
        const isMask = masked(i);
        const filled = !isMask ? 1 : recon; // reconstructed patches fade back in
        const v = 60 + rnd(r, c, 1) * 150;
        return (
          <div key={i} style={{
            position: "absolute", left: GX + c * (PS + 4), top: GY + r * (PS + 4), width: PS, height: PS, borderRadius: 8,
            background: isMask && recon < 0.5 ? C.bg2 : mix(C.bg1, C.neural, 0.2 + (v / 210) * 0.6),
            border: `1.5px solid ${isMask ? mix(C.line, C.neural, 0.6) : C.line}`,
            opacity: (i / (PN * PN) <= reveal ? 1 : 0),
            transform: `scale(${isMask && recon > 0.5 ? 0.9 + filled * 0.1 : 1})`,
            boxShadow: isMask && recon > 0.5 && recon < 0.9 ? `0 0 14px ${mix(C.bg0, C.neural, 0.5)}` : "none",
          }} />
        );
      })}
      <div style={{ position: "absolute", left: GX, top: GY + PN * (PS + 4) + 14, fontFamily: MONO, fontSize: 22, color: C.neural, opacity: recon }}>…reconstruct them → the model must learn how the world looks</div>
      <Flow x1={GX + PN * (PS + 4) + 20} y1={GY + 190} x2={GX + PN * (PS + 4) + 120} y2={GY + 190} color={C.neural} n={4} o={p(0.4, 0.48)} />
      {/* right panel */}
      <div style={{ position: "absolute", left: 1120, top: 285, width: 700 }}>
        {[
          { at: 0.22, t: "labels are expensive; raw images are almost free", c: C.pix },
          { at: 0.42, t: "invent a pretext task — mask & reconstruct (MAE), or match two crops (DINO)", c: C.neural },
          { at: 0.64, t: "no human labels, yet it learns rich, general features", c: C.green },
          { at: 0.78, t: "then fine-tune on a tiny labeled set", c: C.classic },
        ].map((s, i) => (
          <div key={i} style={{ fontFamily: SANS, fontSize: 27, color: C.text, background: mix(C.panel, s.c, 0.08), border: `2px solid ${mix(C.line, s.c, 0.7)}`, borderLeft: `5px solid ${s.c}`, borderRadius: 12, padding: "16px 22px", marginBottom: 16, opacity: p(s.at, s.at + 0.08), transform: `translateX(${(1 - p(s.at, s.at + 0.08)) * 24}px)`, lineHeight: 1.35 }}>{s.t}</div>
        ))}
      </div>
      <Foot p={p(0.85, 0.93)}>The same idea that powers language models — predict the hidden part — now pretrains vision backbones.</Foot>
    </Stage>
  );
};

// cv_3d — depth, flow, and 3D vision ------------------------------------------------
const Cv3d: React.FC<{ dur?: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  // depth map: nearer = brighter, computed as a radial gradient over a grid
  const DN = 10, DS = 42, DX = 150, DY = 320;
  const depthReveal = p(0.16, 0.34);
  // optical-flow arrows sweeping
  const flowOn = p(0.44, 0.56);
  return (
    <Stage>
      <Head kicker="BEYOND THE FLAT IMAGE" title="Depth, motion, and 3D" color={C.pix} o={p(0, 0.06)} />
      {/* depth map */}
      <div style={{ position: "absolute", left: DX, top: DY - 44, fontFamily: MONO, fontSize: 22, color: C.muted, opacity: p(0.1, 0.18) }}>monocular depth — one photo → distance per pixel</div>
      {Array.from({ length: DN * DN }).map((_, i) => {
        const r = Math.floor(i / DN), c = i % DN;
        const dx = (c - DN / 2) / DN, dy = (r - DN / 2) / DN;
        const d = 1 - Math.min(1, Math.sqrt(dx * dx + dy * dy) * 1.5); // nearer at centre
        return (
          <div key={i} style={{
            position: "absolute", left: DX + c * (DS + 3), top: DY + r * (DS + 3), width: DS, height: DS, borderRadius: 6,
            background: mix(C.bg1, C.pix, 0.1 + d * 0.8), opacity: i / (DN * DN) <= depthReveal ? 1 : 0,
          }} />
        );
      })}
      <div style={{ position: "absolute", left: DX, top: DY + DN * (DS + 3) + 12, fontFamily: MONO, fontSize: 21, color: C.pix, opacity: depthReveal }}>bright = near · dark = far (Depth Anything)</div>
      {/* optical flow panel */}
      <div style={{ position: "absolute", left: 780, top: DY - 44, fontFamily: MONO, fontSize: 22, color: C.muted, opacity: p(0.4, 0.48) }}>optical flow — how each pixel moved</div>
      <div style={{ position: "absolute", left: 780, top: DY, width: 470, height: DN * (DS + 3) - 3, borderRadius: 16, background: C.bg1, border: `2px solid ${C.line}`, overflow: "hidden", opacity: p(0.42, 0.5) }}>
        {Array.from({ length: 36 }).map((_, i) => {
          const gx = 40 + (i % 6) * 72, gy = 40 + Math.floor(i / 6) * 62;
          const ph = (frame * 0.05 + i) % (Math.PI * 2);
          const len = 22 + Math.sin(ph) * 8;
          return (
            <svg key={i} style={{ position: "absolute", left: gx, top: gy, overflow: "visible" }} width={1} height={1}>
              <line x1={0} y1={0} x2={len} y2={6} stroke={C.green} strokeWidth={3} opacity={flowOn * 0.9} markerEnd="" />
              <circle cx={len} cy={6} r={3} fill={C.green} opacity={flowOn} />
            </svg>
          );
        })}
      </div>
      {/* NeRF / novel view */}
      <div style={{ position: "absolute", left: 1300, top: DY - 44, fontFamily: MONO, fontSize: 22, color: C.muted, opacity: p(0.6, 0.68) }}>NeRF / Gaussian splats — new views</div>
      <div style={{ position: "absolute", left: 1300, top: DY, width: 470, height: DN * (DS + 3) - 3, borderRadius: 16, background: `radial-gradient(circle at ${50 + Math.sin(frame * 0.03) * 20}% 50%, ${mix(C.bg2, C.gen, 0.25)}, ${C.bg1})`, border: `2px solid ${mix(C.line, C.gen, 0.5)}`, opacity: p(0.62, 0.7), display: "flex", alignItems: "center", justifyContent: "center", fontSize: 120, transform: `perspective(600px) rotateY(${Math.sin(frame * 0.03) * 18}deg)` }}>🏛️</div>
      <div style={{ position: "absolute", left: 1300, top: DY + DN * (DS + 3) + 12, fontFamily: MONO, fontSize: 21, color: C.gen, opacity: p(0.68, 0.76) }}>photos in → fly the camera anywhere</div>
      <Foot p={p(0.84, 0.92)}>Robots, AR and self-driving need the third dimension — reconstructed from ordinary 2D frames.</Foot>
    </Stage>
  );
};

// cv_kernels — the kernel zoo (same slide, different numbers) -----------------------
const CvKernels: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur);
  const panels = [
    { g: K_BLUR_G, k: [[1, 1, 1], [1, 1, 1], [1, 1, 1]], nm: "blur", note: "average → smooth", c: C.pix, at: 0.24 },
    { g: K_SHARP_G, k: [[0, -1, 0], [-1, 5, -1], [0, -1, 0]], nm: "sharpen", note: "boost the centre", c: C.classic, at: 0.42 },
    { g: K_EDGE_G, k: [[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]], nm: "edges", note: "difference → outline", c: C.green, at: 0.6 },
  ];
  return (
    <Stage>
      <Head kicker="CLASSICAL VISION" title="The kernel zoo — one slide, many detectors" color={C.classic} o={p(0, 0.06)} />
      {/* source */}
      <div style={{ position: "absolute", left: 150, top: 320 }}>
        <PixGrid g={CAT12} x={0} y={0} cell={26} o={p(0.05, 0.13)} label="source image" />
      </div>
      <ScanBeam x={150} y={356} w={312} h={312} color={C.classic} o={p(0.1, 0.2) * 0.5} speed={0.7} />
      {panels.map((pn, i) => {
        const o = p(pn.at, pn.at + 0.12);
        const x = 620 + i * 420;
        return (
          <React.Fragment key={i}>
            <Flow x1={480} y1={480} x2={x - 20} y2={480} color={pn.c} n={3} o={p(pn.at - 0.06, pn.at + 0.02)} />
            {/* kernel numbers */}
            <div style={{ position: "absolute", left: x, top: 300, opacity: o }}>
              <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 34px)", gap: 3 }}>
                {pn.k.flat().map((v, j) => (
                  <div key={j} style={{ width: 34, height: 34, borderRadius: 5, background: mix(C.panel, pn.c, 0.12), border: `1.5px solid ${mix(C.line, pn.c, 0.6)}`, display: "flex", alignItems: "center", justifyContent: "center", fontFamily: MONO, fontSize: 17, color: pn.c, fontWeight: 700 }}>{v}</div>
                ))}
              </div>
            </div>
            <PixGrid g={pn.g} x={x} y={420} cell={22} o={o} />
            <div style={{ position: "absolute", left: x, top: 420 + pn.g.length * 24 + 10, fontFamily: MONO, fontSize: 21, color: pn.c, opacity: o, fontWeight: 700 }}>{pn.nm}</div>
            <div style={{ position: "absolute", left: x, top: 420 + pn.g.length * 24 + 40, fontFamily: MONO, fontSize: 18, color: C.muted, opacity: o }}>{pn.note}</div>
          </React.Fragment>
        );
      })}
      <Foot p={p(0.82, 0.9)}>Nothing changed but the nine numbers in the window — and the detector changed completely.</Foot>
    </Stage>
  );
};

// cv_receptive — the receptive field grows with depth -------------------------------
const CvReceptive: React.FC<{ dur?: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const GX = 150, GY = 320, N = 11, CELL = 30;
  const depth = p(0.16, 0.82); // 0..1 → receptive field size
  const rf = Math.round(1 + depth * (N - 1)); // window side in cells
  const center = Math.floor(N / 2);
  const half = Math.floor(rf / 2);
  const layers = [
    { at: 0.2, nm: "layer 1", sub: "sees a 3×3 patch", c: C.pix },
    { at: 0.42, nm: "layer 2", sub: "sees ~7×7", c: C.classic },
    { at: 0.62, nm: "layer 3", sub: "sees ~15×15", c: C.neural },
    { at: 0.78, nm: "deep layer", sub: "sees (almost) everything", c: C.green },
  ];
  const activeLayer = Math.min(3, Math.floor(depth * 4));
  return (
    <Stage>
      <Head kicker="DEEP LEARNING" title="Depth = context: the receptive field grows" color={C.neural} o={p(0, 0.06)} />
      {/* input grid */}
      {Array.from({ length: N * N }).map((_, i) => {
        const r = Math.floor(i / N), c = i % N;
        const inRF = Math.abs(r - center) <= half && Math.abs(c - center) <= half;
        return (
          <div key={i} style={{
            position: "absolute", left: GX + c * (CELL + 3), top: GY + r * (CELL + 3), width: CELL, height: CELL, borderRadius: 5,
            background: inRF ? mix(C.bg1, layers[activeLayer].c, 0.55) : C.bg1,
            border: `1px solid ${inRF ? layers[activeLayer].c : C.line}`,
            opacity: p(0.05, 0.14),
            boxShadow: inRF ? `0 0 8px ${mix(C.bg0, layers[activeLayer].c, 0.4)}` : "none",
          }} />
        );
      })}
      <div style={{ position: "absolute", left: GX + center * (CELL + 3) + 4, top: GY + center * (CELL + 3) + 4, width: CELL - 8, height: CELL - 8, borderRadius: 4, background: C.text, opacity: 0.5 + Math.sin(frame * 0.1) * 0.3 }} />
      <div style={{ position: "absolute", left: GX, top: GY + N * (CELL + 3) + 14, fontFamily: MONO, fontSize: 21, color: C.muted, opacity: p(0.12, 0.2) }}>one deep neuron's view of the input</div>
      {/* layer stack on the right */}
      <div style={{ position: "absolute", left: 900, top: 300, width: 780 }}>
        {layers.map((l, i) => {
          const o = p(l.at, l.at + 0.1);
          const active = activeLayer === i;
          return (
            <div key={i} style={{ display: "flex", alignItems: "center", gap: 18, marginBottom: 20, opacity: o, transform: `translateX(${(1 - o) * 22}px)` }}>
              <div style={{ width: 60, height: 60, borderRadius: 12, background: mix(C.panel, l.c, active ? 0.25 : 0.1), border: `2.5px solid ${l.c}`, display: "flex", alignItems: "center", justifyContent: "center", fontFamily: MONO, fontWeight: 800, fontSize: 26, color: l.c, boxShadow: active ? `0 0 26px ${mix(C.bg0, l.c, 0.5)}` : "none" }}>{i + 1}</div>
              <div>
                <div style={{ fontFamily: SANS, fontWeight: 800, fontSize: 32, color: l.c }}>{l.nm}</div>
                <div style={{ fontFamily: MONO, fontSize: 23, color: C.muted, marginTop: 4 }}>{l.sub}</div>
              </div>
            </div>
          );
        })}
      </div>
      <Foot p={p(0.85, 0.93)}>Small local filters, stacked — so a deep neuron ends up influenced by the whole image.</Foot>
    </Stage>
  );
};

// cv_augment — data augmentation gallery --------------------------------------------
const CvAugment: React.FC<{ dur?: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const tiles = [
    { nm: "original", tf: "none", at: 0.14 },
    { nm: "flip", tf: "scaleX(-1)", at: 0.26 },
    { nm: "rotate", tf: "rotate(14deg)", at: 0.38 },
    { nm: "crop + zoom", tf: "scale(1.4) translate(-8%, 6%)", at: 0.5 },
    { nm: "brightness", tf: "none", dim: true, at: 0.62 },
    { nm: "color jitter", tf: "none", hue: true, at: 0.72 },
  ];
  const hot = Math.floor(frame / 30) % tiles.length;
  return (
    <Stage>
      <Head kicker="TRAINING" title="Data augmentation: one image, many views" color={C.neural} o={p(0, 0.06)} />
      {tiles.map((t, i) => {
        const col = i % 3, row = Math.floor(i / 3);
        const o = p(t.at, t.at + 0.1);
        const active = hot === i && p(0.5, 0.51) > 0.5;
        const x = 220 + col * 500, y = 280 + row * 300;
        return (
          <div key={i} style={{ position: "absolute", left: x, top: y, opacity: o, transform: `translateY(${(1 - o) * 20 + (active ? -6 : 0)}px)` }}>
            <div style={{ width: 260, height: 220, borderRadius: 18, background: t.hue ? mix(C.bg1, C.gen, 0.25) : C.bg1, border: `2.5px solid ${active ? C.neural : C.line}`, overflow: "hidden", display: "flex", alignItems: "center", justifyContent: "center", boxShadow: active ? `0 0 34px ${mix(C.bg0, C.neural, 0.4)}` : "none" }}>
              <span style={{ fontSize: 150, transform: t.tf, opacity: t.dim ? 0.45 : 1, filter: t.hue ? "hue-rotate(90deg)" : "none" }}>🐱</span>
            </div>
            <div style={{ fontFamily: MONO, fontSize: 22, color: active ? C.neural : C.muted, marginTop: 10 }}>{t.nm}</div>
          </div>
        );
      })}
      <Foot p={p(0.84, 0.92)}>Same label, endless variety — the model must generalize instead of memorizing.</Foot>
    </Stage>
  );
};

// cv_transfer — transfer learning ---------------------------------------------------
const CvTransfer: React.FC<{ dur?: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const layers = ["edges", "textures", "parts", "objects"];
  return (
    <Stage>
      <Head kicker="TRAINING" title="Transfer learning: don't start from zero" color={C.neural} o={p(0, 0.06)} />
      {/* frozen backbone */}
      <div style={{ position: "absolute", left: 150, top: 300, width: 820, height: 420, borderRadius: 24, background: mix(C.panel, C.pix, 0.06), border: `2.5px solid ${C.pix}`, opacity: p(0.05, 0.14) }}>
        <div style={{ position: "absolute", left: 26, top: 20, display: "flex", alignItems: "center", gap: 12 }}>
          <span style={{ fontSize: 34 }}>🔒</span>
          <span style={{ fontFamily: SANS, fontWeight: 800, fontSize: 32, color: C.pix }}>pretrained backbone — frozen</span>
        </div>
        <div style={{ position: "absolute", left: 26, top: 70, fontFamily: MONO, fontSize: 21, color: C.muted }}>trained once on ImageNet · reused forever</div>
        {layers.map((l, i) => (
          <div key={i} style={{ position: "absolute", left: 40 + i * 195, top: 150, width: 170, height: 210, borderRadius: 14, background: mix(C.bg1, C.pix, 0.08 + i * 0.05), border: `2px solid ${mix(C.line, C.pix, 0.5)}`, display: "flex", alignItems: "flex-end", justifyContent: "center", paddingBottom: 16, opacity: p(0.12 + i * 0.05, 0.2 + i * 0.05) }}>
            <span style={{ fontFamily: MONO, fontSize: 21, color: C.pix }}>{l}</span>
          </div>
        ))}
      </div>
      <Flow x1={970} y1={510} x2={1120} y2={510} color={C.green} n={5} o={p(0.4, 0.48)} />
      {/* new trainable head */}
      <div style={{ position: "absolute", left: 1130, top: 380, width: 560, height: 260, borderRadius: 24, background: mix(C.panel, C.green, 0.1), border: `2.5px solid ${C.green}`, opacity: p(0.44, 0.54), boxShadow: `0 0 44px ${mix(C.bg0, C.green, 0.24 + Math.sin(frame * 0.06) * 0.08)}` }}>
        <div style={{ position: "absolute", left: 26, top: 22, fontFamily: SANS, fontWeight: 800, fontSize: 32, color: C.green }}>new head</div>
        <div style={{ position: "absolute", left: 26, top: 68, fontFamily: MONO, fontSize: 21, color: C.muted }}>YOUR classes · trained fresh</div>
        <div style={{ position: "absolute", left: 26, top: 120, right: 26, display: "flex", flexWrap: "wrap", gap: 10 }}>
          {["healthy", "diseased", "unknown"].map((c, i) => (
            <span key={i} style={{ fontFamily: MONO, fontSize: 21, color: C.bg0, background: C.green, borderRadius: 999, padding: "8px 18px", opacity: p(0.56 + i * 0.03, 0.64 + i * 0.03) }}>{c}</span>
          ))}
        </div>
      </div>
      <div style={{ position: "absolute", left: 1130, top: 670, width: 560, fontFamily: SANS, fontSize: 25, color: C.text, opacity: p(0.7, 0.78), lineHeight: 1.4 }}>
        freeze the backbone, train only the head — learns from a few <b style={{ color: C.green }}>hundred</b> images, not millions
      </div>
      <Foot p={p(0.85, 0.93)}>The same idea as fine-tuning a language model: reuse general knowledge, specialize cheaply.</Foot>
    </Stage>
  );
};

// cv_metrics — how we measure vision models -----------------------------------------
const CvMetrics: React.FC<{ dur?: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  // IoU: prediction box slowly drifts toward ground truth so IoU rises visibly
  const drift = (Math.sin(frame * 0.03) + 1) / 2; // 0..1
  const gtX = 220, gtY = 340, BW2 = 200, BH2 = 180;
  const prX = gtX + 90 - drift * 70, prY = gtY + 60 - drift * 40;
  const ix = Math.max(gtX, prX), iy = Math.max(gtY, prY);
  const ix2 = Math.min(gtX + BW2, prX + BW2), iy2 = Math.min(gtY + BH2, prY + BH2);
  const inter = Math.max(0, ix2 - ix) * Math.max(0, iy2 - iy);
  const uni = 2 * BW2 * BH2 - inter;
  const iou = inter / uni;
  const aps = [{ nm: "cat", v: 0.91 }, { nm: "dog", v: 0.86 }, { nm: "car", v: 0.78 }, { nm: "sign", v: 0.64 }];
  const mAP = aps.reduce((s, a) => s + a.v, 0) / aps.length;
  return (
    <Stage>
      <Head kicker="IN PRACTICE" title="Measuring a model: IoU, precision, mAP" color={C.green} o={p(0, 0.06)} />
      {/* IoU panel */}
      <div style={{ position: "absolute", left: 150, top: 280, fontFamily: MONO, fontSize: 22, color: C.muted, opacity: p(0.08, 0.16) }}>1 · overlap = IoU (intersection / union)</div>
      <div style={{ position: "absolute", left: gtX, top: gtY, width: BW2, height: BH2, border: `3px solid ${C.green}`, borderRadius: 8, opacity: p(0.12, 0.2) }} />
      <div style={{ position: "absolute", left: gtX + 6, top: gtY - 30, fontFamily: MONO, fontSize: 19, color: C.green, opacity: p(0.14, 0.22) }}>ground truth</div>
      <div style={{ position: "absolute", left: prX, top: prY, width: BW2, height: BH2, border: `3px dashed ${C.classic}`, borderRadius: 8, opacity: p(0.18, 0.26) }} />
      <div style={{ position: "absolute", left: prX + 6, top: prY + BH2 + 6, fontFamily: MONO, fontSize: 19, color: C.classic, opacity: p(0.2, 0.28) }}>prediction</div>
      {inter > 0 && <div style={{ position: "absolute", left: ix, top: iy, width: ix2 - ix, height: iy2 - iy, background: mix(C.bg1, C.pix, 0.4), opacity: p(0.28, 0.36) }} />}
      <div style={{ position: "absolute", left: 150, top: 560, display: "flex", alignItems: "baseline", gap: 10, opacity: p(0.34, 0.42) }}>
        <span style={{ fontFamily: MONO, fontSize: 24, color: C.muted }}>IoU =</span>
        <Counter p={1} to={iou} decimals={2} color={iou > 0.5 ? C.green : C.classic} size={52} />
        <span style={{ fontFamily: MONO, fontSize: 22, color: C.muted }}>{iou > 0.5 ? "→ a hit ✓" : "→ too loose"}</span>
      </div>
      {/* precision / recall */}
      <div style={{ position: "absolute", left: 730, top: 300, width: 380, opacity: p(0.44, 0.52) }}>
        <div style={{ fontFamily: MONO, fontSize: 22, color: C.muted, marginBottom: 12 }}>2 · precision vs recall</div>
        <div style={{ fontFamily: SANS, fontSize: 25, color: C.text, lineHeight: 1.5 }}>
          <b style={{ color: C.pix }}>precision:</b> of what you flagged, how much was right?<br />
          <b style={{ color: C.classic }}>recall:</b> of what was there, how much did you find?
        </div>
        <div style={{ fontFamily: MONO, fontSize: 21, color: C.muted, marginTop: 12 }}>a threshold trades one for the other</div>
      </div>
      {/* mAP bars */}
      <div style={{ position: "absolute", left: 1200, top: 300, width: 520, opacity: p(0.6, 0.68) }}>
        <div style={{ fontFamily: MONO, fontSize: 22, color: C.muted, marginBottom: 14 }}>3 · average precision per class → mean</div>
        {aps.map((a, i) => {
          const grow = p(0.62 + i * 0.04, 0.74 + i * 0.04);
          return (
            <div key={i} style={{ display: "flex", alignItems: "center", gap: 12, marginBottom: 12 }}>
              <span style={{ fontFamily: MONO, fontSize: 22, color: C.text, width: 60 }}>{a.nm}</span>
              <div style={{ flex: 1, height: 30, background: C.panel, borderRadius: 8, overflow: "hidden", border: `1.5px solid ${C.line}` }}>
                <div style={{ width: `${a.v * 100 * grow}%`, height: "100%", background: C.green }} />
              </div>
              <span style={{ fontFamily: MONO, fontWeight: 700, fontSize: 22, color: C.green, width: 60 }}>{(a.v * grow).toFixed(2)}</span>
            </div>
          );
        })}
        <div style={{ display: "flex", alignItems: "baseline", gap: 10, marginTop: 10, opacity: p(0.78, 0.86) }}>
          <span style={{ fontFamily: MONO, fontSize: 24, color: C.muted }}>mAP =</span>
          <Counter p={p(0.78, 0.9)} to={mAP} decimals={2} color={C.green} size={44} />
        </div>
      </div>
      <Foot p={p(0.88, 0.95)}>“It works” is not a number. IoU, precision, recall and mAP are how the field keeps score.</Foot>
    </Stage>
  );
};

// cv_track — multi-object tracking --------------------------------------------------
const CvTrack: React.FC<{ dur?: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const p = useP(dur);
  const SX = 150, SY = 280, SW = 1080, SH = 500;
  const actors = [
    { e: "🚶", id: 1, c: C.green, y: SY + 180, speed: 1.3, x0: 60 },
    { e: "🚴", id: 2, c: C.classic, y: SY + 300, speed: 2.1, x0: 40 },
    { e: "🚗", id: 3, c: C.gen, y: SY + 360, speed: 3.0, x0: 20 },
  ];
  return (
    <Stage>
      <Head kicker="CORE TASK" title="Tracking: keep the same ID across frames" color={C.green} o={p(0, 0.06)} />
      <div style={{ position: "absolute", left: SX, top: SY, width: SW, height: SH, borderRadius: 22, background: `linear-gradient(180deg, ${C.bg2}, ${C.bg1})`, border: `2.5px solid ${C.line}`, overflow: "hidden", opacity: p(0.05, 0.13) }}>
        {actors.map((a, i) => {
          const x = a.x0 + ((frame * a.speed) % (SW + 160)) - 80;
          const on = p(0.14 + i * 0.06, 0.24 + i * 0.06);
          return (
            <React.Fragment key={i}>
              {/* trail */}
              {[1, 2, 3].map((k) => (
                <div key={k} style={{ position: "absolute", left: x - k * 26, top: a.y - SY + 40, width: 8, height: 8, borderRadius: 8, background: a.c, opacity: on * (0.3 - k * 0.07) }} />
              ))}
              <span style={{ position: "absolute", left: x, top: a.y - SY, fontSize: 74 }}>{a.e}</span>
              <div style={{ position: "absolute", left: x - 6, top: a.y - SY - 8, width: 92, height: 92, border: `3px solid ${a.c}`, borderRadius: 10, opacity: on }} />
              <div style={{ position: "absolute", left: x - 6, top: a.y - SY - 40, fontFamily: MONO, fontWeight: 700, fontSize: 20, color: C.bg0, background: a.c, borderRadius: 6, padding: "2px 10px", opacity: on }}>id {a.id}</div>
            </React.Fragment>
          );
        })}
      </div>
      <Brackets x={SX - 14} y={SY - 14} w={SW + 28} h={SH + 28} color={C.green} o={p(0.08, 0.16)} />
      <div style={{ position: "absolute", left: SX, top: SY + SH + 24, right: 150, display: "flex", gap: 22, opacity: p(0.5, 0.6) }}>
        {[
          { t: "detect every frame", c: C.pix },
          { t: "match this frame's boxes to last frame's IDs", c: C.classic },
          { t: "re-ID recovers an object after it's hidden", c: C.gen },
        ].map((s, i) => (
          <div key={i} style={{ flex: 1, fontFamily: SANS, fontSize: 25, color: C.text, background: mix(C.panel, s.c, 0.08), border: `2px solid ${mix(C.line, s.c, 0.6)}`, borderLeft: `5px solid ${s.c}`, borderRadius: 12, padding: "14px 20px", opacity: p(0.5 + i * 0.06, 0.6 + i * 0.06), lineHeight: 1.35 }}>{s.t}</div>
        ))}
      </div>
      <Foot p={p(0.86, 0.94)}>Detection finds objects; tracking gives each one a lasting identity — the basis of traffic and sports analytics.</Foot>
    </Stage>
  );
};

// cv_ocr — text detection + recognition ---------------------------------------------
const CvOcr: React.FC<{ dur?: number }> = ({ dur }) => {
  const p = useP(dur);
  const boxes = [
    { txt: "STOP", x: 240, y: 340, w: 300, h: 110, at: 0.2, read: 0.42 },
    { txt: "EXIT 24", x: 240, y: 500, w: 420, h: 100, at: 0.3, read: 0.56 },
    { txt: "OPEN 24/7", x: 240, y: 650, w: 520, h: 100, at: 0.4, read: 0.68 },
  ];
  return (
    <Stage>
      <Head kicker="CORE TASK" title="OCR: turn pixels of text into characters" color={C.pix} o={p(0, 0.06)} />
      {/* scene */}
      <div style={{ position: "absolute", left: 150, top: 300, width: 760, height: 520, borderRadius: 22, background: `linear-gradient(180deg, ${C.bg2}, ${C.bg1})`, border: `2.5px solid ${C.line}`, overflow: "hidden", opacity: p(0.05, 0.13) }} />
      <ScanBeam x={150} y={300} w={760} h={520} color={C.pix} o={p(0.1, 0.2)} speed={0.9} />
      {boxes.map((b, i) => (
        <React.Fragment key={i}>
          {/* faint "printed" text */}
          <div style={{ position: "absolute", left: b.x + 20, top: b.y + 18, fontFamily: SANS, fontWeight: 800, fontSize: 60, color: mix(C.bg1, C.text, 0.5), opacity: p(0.06, 0.14) }}>{b.txt}</div>
          {/* detection box */}
          <div style={{ position: "absolute", left: b.x, top: b.y, width: b.w, height: b.h, border: `3px solid ${C.green}`, borderRadius: 8, opacity: p(b.at, b.at + 0.08) }} />
        </React.Fragment>
      ))}
      <div style={{ position: "absolute", left: 240, top: 780, fontFamily: MONO, fontSize: 21, color: C.green, opacity: p(0.2, 0.28) }}>step 1 · detect where the text is</div>
      {/* recognized output */}
      <div style={{ position: "absolute", left: 1010, top: 320, width: 720 }}>
        <div style={{ fontFamily: MONO, fontSize: 22, color: C.muted, marginBottom: 18, opacity: p(0.34, 0.42) }}>step 2 · recognize what it says</div>
        {boxes.map((b, i) => (
          <div key={i} style={{ display: "flex", alignItems: "center", gap: 16, marginBottom: 22, opacity: p(b.read - 0.06, b.read) }}>
            <span style={{ fontFamily: MONO, fontSize: 22, color: C.pix, width: 30 }}>{i + 1}</span>
            <div style={{ background: mix(C.panel, C.pix, 0.1), border: `2px solid ${mix(C.line, C.pix, 0.6)}`, borderRadius: 12, padding: "12px 24px", minWidth: 320 }}>
              <span style={{ fontFamily: MONO, fontWeight: 800, fontSize: 34, color: C.text }}>
                <Type text={`"${b.txt}"`} p={p(b.read, b.read + 0.12)} size={34} mono />
              </span>
            </div>
          </div>
        ))}
        <div style={{ fontFamily: SANS, fontSize: 24, color: C.text, marginTop: 10, opacity: p(0.8, 0.88), lineHeight: 1.4 }}>
          documents, license plates, receipts, live translation — text is everywhere in images
        </div>
      </div>
      <Foot p={p(0.88, 0.95)}>Two stages, both computer vision: find the text, then read it — the same detect-then-classify pattern.</Foot>
    </Stage>
  );
};

// ===========================================================================
export interface CVSceneProps { variant: string;[key: string]: unknown; }

export const CVScene: React.FC<CVSceneProps> = ({ variant, ...rest }) => {
  let content: React.ReactNode = null;
  let accent = C.pix;
  switch (variant) {
    case "cv_title": content = <CvTitle {...(rest as any)} />; break;
    case "cv_hook": content = <CvHook {...(rest as any)} />; break;
    case "cv_divider": content = <CvDivider {...(rest as any)} />; accent = (rest as any).color || C.pix; break;
    case "cv_pixels": content = <CvPixels {...(rest as any)} />; break;
    case "cv_tasks": content = <CvTasks {...(rest as any)} />; break;
    case "cv_apps": content = <CvApps {...(rest as any)} />; accent = C.green; break;
    case "cv_filters": content = <CvFilters {...(rest as any)} />; accent = C.classic; break;
    case "cv_conv": content = <CvConv {...(rest as any)} />; accent = C.classic; break;
    case "cv_edges": content = <CvEdges {...(rest as any)} />; accent = C.classic; break;
    case "cv_classic": content = <CvClassic {...(rest as any)} />; accent = C.classic; break;
    case "cv_whycnn": content = <CvWhyCnn {...(rest as any)} />; accent = C.neural; break;
    case "cv_cnn": content = <CvCnn {...(rest as any)} />; accent = C.neural; break;
    case "cv_pool": content = <CvPool {...(rest as any)} />; break;
    case "cv_hier": content = <CvHier {...(rest as any)} />; accent = C.neural; break;
    case "cv_imagenet": content = <CvImagenet {...(rest as any)} />; accent = C.neural; break;
    case "cv_train": content = <CvTrain {...(rest as any)} />; accent = C.neural; break;
    case "cv_classify": content = <CvClassify {...(rest as any)} />; accent = C.green; break;
    case "cv_detect": content = <CvDetect {...(rest as any)} />; accent = C.green; break;
    case "cv_segment": content = <CvSegment {...(rest as any)} />; accent = C.neural; break;
    case "cv_face": content = <CvFace {...(rest as any)} />; break;
    case "cv_vit": content = <CvVit {...(rest as any)} />; accent = C.gen; break;
    case "cv_clip": content = <CvClip {...(rest as any)} />; accent = C.gen; break;
    case "cv_gen": content = <CvGen {...(rest as any)} />; accent = C.gen; break;
    case "cv_vlm": content = <CvVlm {...(rest as any)} />; accent = C.gen; break;
    case "cv_stack": content = <CvStack {...(rest as any)} />; accent = C.green; break;
    case "cv_hard": content = <CvHard {...(rest as any)} />; accent = C.red; break;
    case "cv_sam": content = <CvSam {...(rest as any)} />; accent = C.gen; break;
    case "cv_selfsup": content = <CvSelfsup {...(rest as any)} />; accent = C.neural; break;
    case "cv_3d": content = <Cv3d {...(rest as any)} />; accent = C.pix; break;
    case "cv_code_setup": content = <CvCodeSetup {...(rest as any)} />; accent = C.neural; break;
    case "cv_code_model": content = <CvCodeModel {...(rest as any)} />; accent = C.neural; break;
    case "cv_code_train": content = <CvCodeTrain {...(rest as any)} />; accent = C.neural; break;
    case "cv_code_infer": content = <CvCodeInfer {...(rest as any)} />; accent = C.neural; break;
    case "cv_kernels": content = <CvKernels {...(rest as any)} />; accent = C.classic; break;
    case "cv_receptive": content = <CvReceptive {...(rest as any)} />; accent = C.neural; break;
    case "cv_augment": content = <CvAugment {...(rest as any)} />; accent = C.neural; break;
    case "cv_transfer": content = <CvTransfer {...(rest as any)} />; accent = C.neural; break;
    case "cv_metrics": content = <CvMetrics {...(rest as any)} />; accent = C.green; break;
    case "cv_track": content = <CvTrack {...(rest as any)} />; accent = C.green; break;
    case "cv_ocr": content = <CvOcr {...(rest as any)} />; accent = C.pix; break;
    case "cv_recap": content = <CvRecap {...(rest as any)} />; break;
    default: content = <CvTitle {...(rest as any)} />;
  }
  return (
    <AbsoluteFill>
      <Bg accent={accent} />
      {content}
    </AbsoluteFill>
  );
};

export default CVScene;
