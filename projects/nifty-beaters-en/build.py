#!/usr/bin/env python3
"""Reading a Business by the Numbers — Fundamental Analysis, from scratch (English).

Seven chapter videos (each a standalone MP4) + a stitched master, teaching every core
fundamental-analysis term with the ADEPT method. Running real example: three Indian
lead-recycling companies — Ardee, Gravita, Pondy. Shared scene set FAScenes.tsx (`fa`).
Burned-in captions ON. Neerja Neural (en-IN) voice, 16:9 1080p30.

Modes (mirrors design-patterns/build.py):
  tts    [ch...]   generate/cache narration WAVs (edge-tts), concat per chapter, write
                   per-chapter edit_decisions (cuts + audio-timed caption cues); print durations
  qa     [ch...]   render a mid-animation still for every scene → qa-stills/
  render [ch...]   final 1080p30 render per chapter (Remotion), deliver each MP4
  master           concat all rendered chapter MP4s into one master file + deliver
  deliver          copy rendered chapter MP4s to ~/Downloads/generated_videos/<slug>/
Run one chapter end to end:
  python3 build.py tts ch01 && python3 build.py qa ch01 && python3 build.py render ch01

═══════════════════════════════════════════════════════════════════════════════
NUMBERS — teaching figures (skill-12 gate). All company figures are APPROXIMATE,
rounded from FY26 public sources (Screener/company results/aggregators, Aug 2026)
and used ILLUSTRATIVELY to teach the ratios. Intermediate P&L splits (depreciation,
interest, tax) are illustrative and chosen to reconcile Revenue → EBITDA → PAT.
On-screen notes and the narration say "approx". This is EDUCATION, not advice; the
disclaimer is spoken (title + recap) and belongs in every description.

  Ardee Industries (FY26 approx):
    Revenue 1,168 Cr · EBITDA 147 Cr (12.6%) · PAT 85 Cr · Mcap ~2,116 Cr
    ~30 Cr shares · EPS ~2.8 · price ~70 · P/E ~25x · EV/EBITDA ~15x
    D/E 1.25x (pre-IPO, falling) · ROCE ~44%
    illustrative waterfall: Rev 1168 − OpCost 1021 = EBITDA 147 − Dep 20 = EBIT 127
                            − Interest 18 = PBT 109 − Tax 24 = PAT 85
  Gravita India (FY26 approx):
    Revenue 4,265 Cr · EBITDA 452 Cr (10.6%) · PAT 378 Cr · Mcap ~13,550 Cr
    P/E ~31x · EV/EBITDA ~26x · D/E ~0.14x (net cash)
  Pondy Oxides (FY26 approx):
    Revenue 2,939 Cr · EBITDA 218 Cr (7.4%) · PAT 132 Cr · Mcap ~5,700 Cr
    P/E ~40x · D/E ~0.17x (near debt-free)
═══════════════════════════════════════════════════════════════════════════════
"""
import argparse, json, os, subprocess, sys, time
from chapters import CHAPTERS

VOICE = "en-IN-PrabhatNeural"
RATE = "+2%"          # confident thesis pace
GAP = 0.5             # silence between beats
PAUSE = 0.55          # silence at each [pause]
PREFIX = "nb"
CAP_MAXWORDS = 8
CAP_WRAP = 52
SLUG = "nifty-beaters"

ROOT = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(ROOT, "..", ".."))
COMPOSER = os.path.join(REPO, "composer")
PUBLIC = os.path.join(COMPOSER, "public", PREFIX)
RAW = os.path.join(ROOT, "assets", "raw")
FIN = os.path.join(ROOT, "assets")
ART = os.path.join(ROOT, "artifacts")
REND = os.path.join(ROOT, "renders")
QADIR = os.path.join(ROOT, "qa-stills")
DELIVER = os.path.expanduser(f"~/Downloads/generated_videos/{SLUG}")
for d in (PUBLIC, RAW, FIN, ART, REND, QADIR):
    os.makedirs(d, exist_ok=True)


# --------------------------------------------------------------------- TTS (edge-tts)
def ffdur(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "default=noprint_wrappers=1:nokey=1", path],
                         capture_output=True, text=True, check=True)
    return round(float(out.stdout.strip()), 3)


def tts_chunk(path, text):
    mp3 = path[:-4] + ".mp3"
    for attempt in range(8):
        try:
            # HARD timeout: edge-tts can hang indefinitely on a stuck network socket
            # (observed 30+ min freezes). Kill + retry rather than block forever.
            r = subprocess.run(["edge-tts", "--voice", VOICE, f"--rate={RATE}", "--text", text,
                                "--write-media", mp3], capture_output=True, timeout=45)
        except subprocess.TimeoutExpired:
            if os.path.exists(mp3):
                os.remove(mp3)
            time.sleep(2 + attempt * 3)
            continue
        if r.returncode == 0 and os.path.exists(mp3) and os.path.getsize(mp3) > 0:
            break
        time.sleep(2 + attempt * 3)
    else:
        raise RuntimeError(f"tts failed after 8 attempts: {path}")
    subprocess.run(["ffmpeg", "-y", "-i", mp3, "-ar", "24000", "-ac", "1", path],
                   check=True, capture_output=True)
    os.remove(mp3)


def gen_one(seg_id, text):
    fin = os.path.join(FIN, seg_id + ".wav")
    if os.path.exists(fin):
        return fin, ffdur(fin)
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
    subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", clist, "-c", "copy", fin],
                   check=True, capture_output=True)
    return fin, ffdur(fin)


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
    parts = text.split("[pause]")
    ppause = PAUSE
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
        return CHAPTERS
    out = [c for c in CHAPTERS if c["id"] in names or c["id"].replace("ch", "") in names]
    if not out:
        sys.exit(f"no chapter matched {names}; known: {[c['id'] for c in CHAPTERS]}")
    return out


def run_tts(names):
    for ch in pick(names):
        manifest, cues, cuts, t = [], [], [], 0.0
        for seg in ch["segments"]:
            sid = f'{ch["id"]}_{seg[0]}'
            path, d = gen_one(sid, seg[3])
            warn = "  ⚠ LONG >90s" if d > 90 else ""
            manifest.append((sid, path))
            cues.extend(beat_cues(seg[3], d, t))
            cuts.append({"id": sid, "type": seg[1],
                         "in_seconds": round(t, 3), "out_seconds": round(t + d, 3),
                         "props": {**seg[2], "dur": round(d + GAP, 3)}})
            print(f"    {sid:22s} {d:6.2f}s{warn}", flush=True)
            t = round(t + d + GAP, 3)
        sil = os.path.join(FIN, "_gap.wav")
        if not os.path.exists(sil):
            subprocess.run(["ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=24000:cl=mono",
                            "-t", str(GAP), sil], check=True, capture_output=True)
        clist = os.path.join(ART, f'{ch["id"]}_audio.txt')
        with open(clist, "w") as f:
            for i, (sid, path) in enumerate(manifest):
                f.write(f"file '{path}'\n")
                if i < len(manifest) - 1:
                    f.write(f"file '{sil}'\n")
        wav_out = os.path.join(PUBLIC, f'{ch["id"]}.wav')
        subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", clist, "-c", "copy",
                        wav_out], check=True, capture_output=True)
        props = {"cuts": cuts, "captions": [],  # no captions (default)
                 "audio": {"narration": {"src": f'{PREFIX}/{ch["id"]}.wav', "volume": 1.0}}}
        json.dump(props, open(os.path.join(ART, f'{ch["id"]}.json'), "w"), indent=1)
        words = sum(len(s[3].replace("[pause]", " ").split()) for s in ch["segments"])
        dur = t - GAP
        print(f'  {ch["id"]}: {dur/60:5.2f} min  {len(ch["segments"])} scenes  {words:5d} words  '
              f'{words/(dur/60):.0f} wpm', flush=True)


def run_qa(names):
    for ch in pick(names):
        props = os.path.join(ART, f'{ch["id"]}.json')
        if not os.path.exists(props):
            sys.exit(f"run tts first for {ch['id']}")
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


def render_one(ch, attempts=3):
    props = os.path.join(ART, f'{ch["id"]}.json')
    out = os.path.join(REND, f'{ch["id"]}.mp4')
    for a in range(1, attempts + 1):
        r = subprocess.run(["npx", "remotion", "render", "Explainer", out,
                            f"--props={props}", "--concurrency=2", "--timeout=600000"],
                           cwd=COMPOSER, capture_output=True, text=True)
        if r.returncode == 0 and os.path.exists(out):
            os.makedirs(DELIVER, exist_ok=True)
            subprocess.run(["cp", out, os.path.join(DELIVER, f'{SLUG}-{ch["id"]}.mp4')], check=True)
            return out
        print(f"  render attempt {a}/{attempts} failed for {ch['id']}:\n" + (r.stderr or r.stdout)[-700:], flush=True)
        if os.path.exists(out):
            os.remove(out)
        time.sleep(5)
    print(f"  GAVE UP on {ch['id']} after {attempts} attempts", flush=True)
    return None


def run_render(names):
    for ch in pick(names):
        out = render_one(ch)
        if out:
            print(f'  rendered + delivered {ch["id"]} ({ffdur(out)/60:.2f} min) → {DELIVER}', flush=True)


def run_master(names):
    """Concat all rendered chapter MP4s into one master (re-encode for safe concat)."""
    files = [os.path.join(REND, f'{ch["id"]}.mp4') for ch in CHAPTERS]
    files = [f for f in files if os.path.exists(f)]
    if not files:
        sys.exit("no chapter MP4s rendered yet")
    lst = os.path.join(ART, "master_concat.txt")
    with open(lst, "w") as f:
        for p in files:
            f.write(f"file '{p}'\n")
    out = os.path.join(REND, "master.mp4")
    subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", lst,
                    "-c:v", "libx264", "-preset", "medium", "-crf", "18",
                    "-c:a", "aac", "-b:a", "192k", out], check=True)
    os.makedirs(DELIVER, exist_ok=True)
    subprocess.run(["cp", out, os.path.join(DELIVER, f"{SLUG}-master.mp4")], check=True)
    print(f"master: {len(files)} chapters → {ffdur(out)/60:.2f} min → {DELIVER}")


def run_deliver(names):
    os.makedirs(DELIVER, exist_ok=True)
    n = 0
    for ch in pick(names):
        src = os.path.join(REND, f'{ch["id"]}.mp4')
        if os.path.exists(src):
            subprocess.run(["cp", src, os.path.join(DELIVER, f'{SLUG}-{ch["id"]}.mp4')], check=True); n += 1
    print(f"delivered {n} chapter videos → {DELIVER}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["tts", "qa", "render", "master", "deliver"], nargs="?", default="tts")
    ap.add_argument("names", nargs="*")
    a = ap.parse_args()
    {"tts": run_tts, "qa": run_qa, "render": run_render, "master": run_master, "deliver": run_deliver}[a.mode](a.names)
