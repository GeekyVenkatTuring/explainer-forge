#!/usr/bin/env python3
"""Design Patterns, Java — one video PER PATTERN (Gang of Four, 23 total).

Each pattern is an independent MP4 (the user asked for separate videos, rendered as
each is finished — no batching). Burned-in captions ON. Nova voice, 16:9 1080p30.
Every pattern follows the identical 10-section teaching arc; the shared scene set is
composer/src/scenes/DPScenes.tsx (prefix `dp`). Screenplay lives in patterns.py.

Modes (mirrors it-from-scratch):
  tts   [id...]     generate/cache narration WAVs, concat per pattern, write per-pattern
                    edit_decisions (cuts + audio-timed caption cues); print durations
  qa    [id...]     render a mid-animation still for every scene → qa-stills/
  render[id...]     final 1080p30 render per pattern (Remotion), deliver each MP4 immediately
  deliver           copy any rendered pattern MP4s to ~/Downloads/generated_videos/<slug>/

TTS: Voicebox local API (http://127.0.0.1:17493, app must be open). Idempotent —
delete a segment's assets/<id>.wav to regenerate just that beat.
Run one pattern end to end:  python3 build.py tts strategy && python3 build.py qa strategy && python3 build.py render strategy
"""
import argparse, json, os, subprocess, sys, time, urllib.request
from patterns import PATTERNS

BASE = "http://127.0.0.1:17493"
PROFILE = "c488e05c-3407-46a3-874d-1b09b3aff78d"  # TTS Bright (Nova)
GAP = 0.5           # silence between beats
PAUSE = 0.6         # silence at each [pause]
ATEMPO = 0.95       # gentle global slowdown
PREFIX = "dp"
CAP_MAXWORDS = 8
CAP_WRAP = 50

ROOT = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(ROOT, "..", ".."))
COMPOSER = os.path.join(REPO, "composer")
PUBLIC = os.path.join(COMPOSER, "public", PREFIX)
RAW = os.path.join(ROOT, "assets", "raw")
FIN = os.path.join(ROOT, "assets")
ART = os.path.join(ROOT, "artifacts")
REND = os.path.join(ROOT, "renders")
QADIR = os.path.join(ROOT, "qa-stills")
SLUG = "design-patterns-java"
DELIVER = os.path.expanduser(f"~/Downloads/generated_videos/{SLUG}")
for d in (PUBLIC, RAW, FIN, ART, REND, QADIR):
    os.makedirs(d, exist_ok=True)


# --------------------------------------------------------------------- TTS
def post(p, b):
    req = urllib.request.Request(BASE + p, data=json.dumps(b).encode(),
                                 headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode())


def get(p):
    with urllib.request.urlopen(BASE + p, timeout=30) as r:
        return r.read()


def tts_chunk(path, text):
    gid = post("/generate", {"profile_id": PROFILE, "text": text, "engine": "kokoro"})["id"]
    for _ in range(300):
        raw = get(f"/generate/{gid}/status").decode()
        line = [l for l in raw.splitlines() if l.startswith("data:")]
        st = json.loads(line[-1][5:].strip()) if line else None
        if st and st.get("status") == "completed":
            break
        time.sleep(1)
    open(path, "wb").write(get(f"/audio/{gid}"))


def dur_of(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "default=noprint_wrappers=1:nokey=1", path],
                         capture_output=True, text=True, check=True)
    return round(float(out.stdout.strip()), 3)


def gen_one(seg_id, text):
    fin = os.path.join(FIN, seg_id + ".wav")
    if os.path.exists(fin):
        return fin, dur_of(fin)
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
        for i, p in enumerate(paths):
            f.write(f"file '{p}'\n")
            if i < len(paths) - 1:
                f.write(f"file '{psil}'\n")
    subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", clist,
                    "-filter:a", f"atempo={ATEMPO}", fin], check=True, capture_output=True)
    return fin, dur_of(fin)


# --------------------------------------------------------------------- CAPTIONS
def _wrap(text):
    lines, cur = [], ""
    for w in text.split():
        if cur and len(cur) + 1 + len(w) > CAP_WRAP:
            lines.append(cur); cur = w
        else:
            cur = (cur + " " + w).strip()
    if cur:
        lines.append(cur)
    return "\n".join(lines)


def beat_cues(text, dur, t0):
    """Audio-timed caption cues [start,end,text] for one beat, offset by t0."""
    parts = text.split("[pause]")
    ppause = PAUSE / ATEMPO
    n_pause = len(parts) - 1
    all_words = sum(len(p.split()) for p in parts) or 1
    word_time = max(0.0, dur - n_pause * ppause) / all_words
    cues, ct = [], 0.0
    for pi, part in enumerate(parts):
        words = part.split()
        i = 0
        while i < len(words):
            j = min(i + CAP_MAXWORDS, len(words))
            for k in range(i + 1, j):
                if words[k - 1][-1:] in ".?!,;:":
                    j = k; break
            chunk = words[i:j]
            d = word_time * len(chunk)
            cues.append([round(t0 + ct, 3), round(t0 + ct + d, 3), _wrap(" ".join(chunk))])
            ct += d
            i = j
        if pi < len(parts) - 1:
            ct += ppause
    return cues


# --------------------------------------------------------------------- BUILD
def pick(names):
    if not names:
        return PATTERNS
    out = []
    for p in PATTERNS:
        short = p["id"].split("-", 1)[-1]  # "dp01-strategy" -> "strategy"
        if p["id"] in names or short in names:
            out.append(p)
    if not out:
        sys.exit(f"no pattern matched {names}; known: {[p['id'] for p in PATTERNS]}")
    return out


def run_tts(names):
    for pat in pick(names):
        manifest, cues, cuts, t = [], [], [], 0.0
        for seg in pat["segments"]:
            sid = f'{pat["id"]}_{seg["id"]}'
            path, d = gen_one(sid, seg["narration"])
            if d > 90:
                print(f"    ⚠ LONG scene {sid}: {d:.0f}s — ensure it develops to p≈0.85 or split", flush=True)
            manifest.append((sid, path))
            cues.extend(beat_cues(seg["narration"], d, t))
            cuts.append({"id": sid, "type": seg["variant"],
                         "in_seconds": round(t, 3), "out_seconds": round(t + d, 3),
                         "props": {**seg.get("props", {}), "dur": round(d + GAP, 3)}})
            t = round(t + d + GAP, 3)
        sil = os.path.join(FIN, "_gap.wav")
        if not os.path.exists(sil):
            subprocess.run(["ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=24000:cl=mono",
                            "-t", str(GAP), sil], check=True, capture_output=True)
        clist = os.path.join(ART, f'{pat["id"]}_audio.txt')
        with open(clist, "w") as f:
            for i, (sid, path) in enumerate(manifest):
                f.write(f"file '{path}'\n")
                if i < len(manifest) - 1:
                    f.write(f"file '{sil}'\n")
        wav_out = os.path.join(PUBLIC, f'{pat["id"]}.wav')
        subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", clist, "-c", "copy",
                        wav_out], check=True, capture_output=True)
        props = {"cuts": cuts, "captions": cues,
                 "audio": {"narration": {"src": f'{PREFIX}/{pat["id"]}.wav', "volume": 1.0}}}
        json.dump(props, open(os.path.join(ART, f'{pat["id"]}.json'), "w"), indent=1)
        words = sum(len(s["narration"].replace("[pause]", " ").split()) for s in pat["segments"])
        dur = t - GAP
        print(f'  {pat["id"]:22s} {dur/60:5.2f} min  {len(pat["segments"])} scenes  {words:5d} words  '
              f'{words/(dur/60):.0f} wpm', flush=True)


def run_qa(names):
    for pat in pick(names):
        props = os.path.join(ART, f'{pat["id"]}.json')
        if not os.path.exists(props):
            sys.exit(f"run tts first for {pat['id']}")
        data = json.load(open(props))
        for cut in data["cuts"]:
            mid = (cut["in_seconds"] + cut["out_seconds"]) / 2
            frame = round(mid * 30)
            out = os.path.join(QADIR, f'{cut["id"]}.png')
            r = subprocess.run(["npx", "remotion", "still", "Explainer", out,
                                f"--props={props}", f"--frame={frame}"],
                               cwd=COMPOSER, capture_output=True, text=True)
            if r.returncode != 0:
                print(r.stdout[-800:], r.stderr[-800:]); sys.exit(f"still failed {cut['id']}")
            print(f'  QA {cut["id"]} @f{frame}', flush=True)
    print(f"\nLOOK at every png in {QADIR}/ (skills/06 checklist) before render")


def render_one(pat, attempts=3):
    props = os.path.join(ART, f'{pat["id"]}.json')
    out = os.path.join(REND, f'{pat["id"]}.mp4')
    for a in range(1, attempts + 1):
        r = subprocess.run(["npx", "remotion", "render", "Explainer", out,
                            f"--props={props}", "--concurrency=8", "--timeout=120000"],
                           cwd=COMPOSER, capture_output=True, text=True)
        if r.returncode == 0 and os.path.exists(out):
            os.makedirs(DELIVER, exist_ok=True)
            subprocess.run(["cp", out, os.path.join(DELIVER, f'{pat["id"]}.mp4')], check=True)
            return out
        print(f"  render attempt {a}/{attempts} failed for {pat['id']}:\n" + (r.stderr or r.stdout)[-600:], flush=True)
        if os.path.exists(out):
            os.remove(out)
        time.sleep(5)
    print(f"  GAVE UP on {pat['id']} after {attempts} attempts", flush=True)
    return None


def run_render(names):
    for pat in pick(names):
        out = render_one(pat)
        if out:
            print(f'  rendered + delivered {pat["id"]} ({dur_of(out)/60:.2f} min) → {DELIVER}', flush=True)


def run_deliver(names):
    os.makedirs(DELIVER, exist_ok=True)
    n = 0
    for pat in pick(names):
        src = os.path.join(REND, f'{pat["id"]}.mp4')
        if os.path.exists(src):
            subprocess.run(["cp", src, os.path.join(DELIVER, f'{pat["id"]}.mp4')], check=True); n += 1
    print(f"delivered {n} pattern videos → {DELIVER}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["tts", "qa", "render", "deliver"], nargs="?", default="tts")
    ap.add_argument("names", nargs="*")
    a = ap.parse_args()
    {"tts": run_tts, "qa": run_qa, "render": run_render, "deliver": run_deliver}[a.mode](a.names)
