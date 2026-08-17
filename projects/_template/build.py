#!/usr/bin/env python3
"""<VIDEO TITLE> — build script (TEMPLATE — copy this folder, then edit).

Pipeline: narration TTS (idempotent) -> concat with gaps -> edit_decisions.json
Every cut gets `dur` = narration length + gap, so scenes phase over the full beat.

Calibration (measured): Kokoro "Nova" ≈ 212 wpm including gaps.
  5-min video ≈ 1,050 words · 10-min ≈ 2,100 · 20-min ≈ 4,200.
After the first full run, the script prints the real total — extend/trim
segments and delete only their WAVs to regenerate just those (idempotent).

TTS backend: Voicebox.app local HTTP API (http://127.0.0.1:17493, app must be
open). Swap gen_one() for any TTS that returns a WAV — the rest is unchanged.
Run:  python3 build.py
"""
import json, os, subprocess, time, urllib.request

BASE = "http://127.0.0.1:17493"
PROFILE = "c488e05c-3407-46a3-874d-1b09b3aff78d"  # "TTS Bright (Nova)" — list via GET /profiles
GAP = 0.5                                         # silence between beats (comprehension breathing room)
PAUSE = 0.6                                       # silence inserted at each [pause] marker inside a beat
ATEMPO = 0.95                                     # gentle slowdown; 1.0 = off, <0.9 sounds muddy
PREFIX = "demo"                                   # scene-set prefix registered in Explainer.tsx
ROOT = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(ROOT, "..", ".."))
PUBLIC = os.path.join(REPO, "composer", "public", PREFIX)   # narration staged under public/
RAW = os.path.join(ROOT, "assets", "raw")
FIN = os.path.join(ROOT, "assets")
for d in (PUBLIC, RAW, os.path.join(ROOT, "artifacts"), os.path.join(ROOT, "renders")):
    os.makedirs(d, exist_ok=True)

# ---------------------------------------------------------------- SCREENPLAY
# (seg_id, variant, scene_props, narration)
# Write narration as SPOKEN language (say "two fifty five", not "255").
# Every on-screen element should be *mentioned* by the narration of its beat.
# Insert [pause] (0.6s silence) after new-term definitions, big numbers, and key
# ideas — see skills/02-screenplay.md cognitive-load rules. 3–6 per content beat.
SEGMENTS = [
 ("s01_title", "demo_title", {},
  "Welcome to the Explainer Forge demo. Four scenes, every core pattern: "
  "duration aware phasing, continuous motion, and computed visuals."),

 ("s02_diagram", "demo_diagram", {},
  "Pattern one, the diagram. Cards land in sync with the narration, wires draw "
  "themselves in and keep marching, and particle flows keep the frame alive long "
  "after the layout has finished building. Notice that nothing here ever freezes."),

 ("s03_data", "demo_data", {},
  "Pattern two, the computed visual. [pause] These bars are being sorted by a real "
  "bubble sort, precomputed deterministically and played back across the whole beat. "
  "[pause] When you can run the actual algorithm instead of drawing a picture of it, "
  "always run it."),

 ("s04_recap", "demo_recap",
  {"items": [
      "Phase everything to fractions of the narration with useP(dur)",
      "Keep something moving in every frame",
      "Compute the real thing whenever the topic allows it",
  ], "closer": "That's the Forge pattern — now build a real one."},
  "And pattern three, the recap. Items slide in one per beat of the summary, and the "
  "closer glows. That's the whole grammar. Thanks for watching."),
]


def post(p, b):
    req = urllib.request.Request(BASE + p, data=json.dumps(b).encode(),
                                 headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode())


def get(p):
    with urllib.request.urlopen(BASE + p, timeout=30) as r:
        return r.read()


def tts_chunk(path, text):
    """One raw Voicebox generation → WAV at `path`."""
    gid = post("/generate", {"profile_id": PROFILE, "text": text, "engine": "kokoro"})["id"]
    for _ in range(300):
        raw = get(f"/generate/{gid}/status").decode()
        line = [l for l in raw.splitlines() if l.startswith("data:")]
        st = json.loads(line[-1][5:].strip()) if line else None
        if st and st.get("status") == "completed":
            break
        time.sleep(1)
    open(path, "wb").write(get(f"/audio/{gid}"))


def gen_one(seg_id, text):
    """Build one beat's WAV: [pause]-split TTS chunks + inserted silence + atempo.
    Skips if assets/<seg_id>.wav exists (delete it to regenerate this beat)."""
    fin = os.path.join(FIN, seg_id + ".wav")
    if os.path.exists(fin):
        out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                              "-of", "default=noprint_wrappers=1:nokey=1", fin],
                             capture_output=True, text=True, check=True)
        return fin, round(float(out.stdout.strip()), 3)
    chunks = [c.strip() for c in text.split("[pause]") if c.strip()]
    paths = []
    for ci, chunk in enumerate(chunks):
        cp = os.path.join(RAW, f"{seg_id}_c{ci}.wav")
        if not os.path.exists(cp):
            tts_chunk(cp, chunk)
        paths.append(cp)
    psil = os.path.join(RAW, "_pause.wav")
    if not os.path.exists(psil):
        subprocess.run(["ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=24000:cl=mono",
                        "-t", str(PAUSE), psil], check=True, capture_output=True)
    clist = os.path.join(RAW, f"{seg_id}_concat.txt")
    with open(clist, "w") as f:
        for i2, p2 in enumerate(paths):
            f.write(f"file '{p2}'\n")
            if i2 < len(paths) - 1:
                f.write(f"file '{psil}'\n")
    af = f"atempo={ATEMPO}" if ATEMPO != 1.0 else "anull"
    subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", clist,
                    "-filter:a", af, fin], check=True, capture_output=True)
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "default=noprint_wrappers=1:nokey=1", fin],
                         capture_output=True, text=True, check=True)
    return fin, round(float(out.stdout.strip()), 3)


manifest = []
for sid, variant, props, text in SEGMENTS:
    path, dur = gen_one(sid, text)
    manifest.append({"id": sid, "variant": variant, "props": props, "wav": path, "duration": dur})
    # A single-visual beat > ~90s tends to finish developing before the audio does,
    # so the frame reads as frozen (skills/02,03,09). Split it, or make its content
    # keep developing to p≈0.85 with a visible progress signal.
    warn = "  ⚠ LONG — split or ensure it develops to p≈0.85 (skills/03)" if dur > 90 else ""
    print(f"  {sid:14s} {dur:6.2f}s{warn}", flush=True)

silence = os.path.join(FIN, "_sil.wav")
subprocess.run(["ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=24000:cl=mono", "-t", str(GAP), silence],
               check=True, capture_output=True)
concat_list = os.path.join(ROOT, "concat.txt")
with open(concat_list, "w") as f:
    for i, m in enumerate(manifest):
        f.write(f"file '{m['wav']}'\n")
        if i < len(manifest) - 1:
            f.write(f"file '{silence}'\n")
subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_list, "-c", "copy",
                os.path.join(PUBLIC, "narration.wav")], check=True, capture_output=True)

cuts, t = [], 0.0
for m in manifest:
    start, end = t, t + m["duration"]
    # `dur` (incl. gap) is what makes scenes duration-aware — do not remove it
    cuts.append({"id": m["id"], "type": m["variant"], "in_seconds": round(start, 3),
                 "out_seconds": round(end, 3),
                 "props": {**m["props"], "dur": round(m["duration"] + GAP, 3)}})
    t = end + GAP
props = {"cuts": cuts,
         "audio": {"narration": {"src": f"{PREFIX}/narration.wav", "volume": 1.0}}}
json.dump(props, open(os.path.join(ROOT, "artifacts", "edit_decisions.json"), "w"), indent=2)
print(f"total {t - GAP:.2f}s ({(t-GAP)/60:.2f} min), {len(cuts)} scenes, NO captions, NO music")
