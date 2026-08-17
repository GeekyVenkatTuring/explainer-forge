#!/usr/bin/env python3
"""aitcore.py — shared TTS + props engine for the "AI Trading, Honestly" course.

Each chapter script (ch0_intro.py … ch7_recap.py) defines SEGMENTS and calls
build(ch_id, SEGMENTS). This:
  • generates one WAV per beat (idempotent — delete a WAV to regenerate it),
  • splits on [pause] and inserts 0.6s silence, then atempo 0.95,
  • concatenates the chapter's beats with 0.5s gaps into
    composer/public/ait/<ch_id>.wav,
  • writes projects/ai-trading-en/artifacts/<ch_id>.json (Explainer cuts, each
    carrying `dur` so scenes phase over the whole beat),
  • prints each beat's duration (⚠ warns > 90s) and the chapter total.

Render a chapter:  (from composer/)
  npx remotion render Explainer ../projects/ai-trading-en/renders/<ch_id>.mp4 \
    --props=../projects/ai-trading-en/artifacts/<ch_id>.json --concurrency=8
Then ffmpeg-concat the chapter MP4s into the master.
"""
import json, os, subprocess, time, urllib.request

BASE = "http://127.0.0.1:17493"
PROFILE = "c488e05c-3407-46a3-874d-1b09b3aff78d"  # TTS Bright (Nova) — af_nova
GAP = 0.5
PAUSE = 0.6
ATEMPO = 0.95
PREFIX = "ait"
ROOT = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(ROOT, "..", ".."))
PUBLIC = os.path.join(REPO, "composer", "public", PREFIX)
RAW = os.path.join(ROOT, "assets", "raw")
FIN = os.path.join(ROOT, "assets")
ART = os.path.join(ROOT, "artifacts")
for d in (PUBLIC, RAW, FIN, ART, os.path.join(ROOT, "renders")):
    os.makedirs(d, exist_ok=True)


def _post(p, b):
    req = urllib.request.Request(BASE + p, data=json.dumps(b).encode(),
                                 headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode())


def _get(p):
    with urllib.request.urlopen(BASE + p, timeout=30) as r:
        return r.read()


def _tts_chunk(path, text):
    gid = _post("/generate", {"profile_id": PROFILE, "text": text, "engine": "kokoro"})["id"]
    for _ in range(300):
        raw = _get(f"/generate/{gid}/status").decode()
        line = [l for l in raw.splitlines() if l.startswith("data:")]
        st = json.loads(line[-1][5:].strip()) if line else None
        if st and st.get("status") == "completed":
            break
        time.sleep(1)
    open(path, "wb").write(_get(f"/audio/{gid}"))


def _dur(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "default=noprint_wrappers=1:nokey=1", path],
                         capture_output=True, text=True, check=True)
    return round(float(out.stdout.strip()), 3)


def _gen_one(seg_id, text):
    fin = os.path.join(FIN, seg_id + ".wav")
    if os.path.exists(fin):
        return fin, _dur(fin)
    chunks = [c.strip() for c in text.split("[pause]") if c.strip()]
    paths = []
    for ci, chunk in enumerate(chunks):
        cp = os.path.join(RAW, f"{seg_id}_c{ci}.wav")
        if not os.path.exists(cp):
            _tts_chunk(cp, chunk)
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
    return fin, _dur(fin)


def build(ch_id, segments, target_min=None):
    """Generate a chapter's audio + props. segments: (seg_id, variant, props, narration)."""
    manifest, words = [], 0
    print(f"\n=== {ch_id} ===", flush=True)
    for sid, variant, props, text in segments:
        path, dur = _gen_one(sid, text)
        words += len(text.replace("[pause]", " ").split())
        manifest.append({"id": sid, "variant": variant, "props": props, "wav": path, "duration": dur})
        warn = "  ⚠ LONG >90s" if dur > 90 else ""
        print(f"  {sid:16s} {dur:6.2f}s{warn}", flush=True)

    silence = os.path.join(FIN, "_sil.wav")
    if not os.path.exists(silence):
        subprocess.run(["ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=24000:cl=mono", "-t", str(GAP), silence],
                       check=True, capture_output=True)
    clist = os.path.join(RAW, f"{ch_id}_master.txt")
    with open(clist, "w") as f:
        for i, m in enumerate(manifest):
            f.write(f"file '{m['wav']}'\n")
            if i < len(manifest) - 1:
                f.write(f"file '{silence}'\n")
    ch_wav = os.path.join(PUBLIC, f"{ch_id}.wav")
    subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", clist, "-c", "copy", ch_wav],
                   check=True, capture_output=True)

    cuts, t = [], 0.0
    for m in manifest:
        start, end = t, t + m["duration"]
        cuts.append({"id": m["id"], "type": m["variant"], "in_seconds": round(start, 3),
                     "out_seconds": round(end, 3),
                     "props": {**m["props"], "dur": round(m["duration"] + GAP, 3)}})
        t = end + GAP
    props = {"cuts": cuts, "audio": {"narration": {"src": f"{PREFIX}/{ch_id}.wav", "volume": 1.0}}}
    json.dump(props, open(os.path.join(ART, f"{ch_id}.json"), "w"), indent=2)
    total = t - GAP
    tstr = f", target ~{target_min}min" if target_min else ""
    print(f"  → {ch_id}: {total:.1f}s ({total/60:.2f} min), {len(cuts)} beats, {words} words{tstr}", flush=True)
    return total
