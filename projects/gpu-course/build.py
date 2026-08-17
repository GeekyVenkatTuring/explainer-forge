#!/usr/bin/env python3
"""GPUs: The Engines of AI — chapter-wise build orchestrator (Remotion).

Each chapter renders to its own MP4; all chapters concat into a master. No captions
(repo default), Nova voice, 16:9 1080p30. Idempotent TTS — delete a segment's
assets/<id>.wav to regenerate just that beat.

Modes:
  tts               generate/cache narration WAVs, concat per chapter, write per-chapter
                    edit_decisions (cuts with dur); print per-chapter durations
  qa   [chid...]    render a mid-animation still for every scene -> qa-stills/
  render [chid...]  final 1080p30 render per chapter (Remotion, --concurrency=8), deliver each
  master            ffmpeg-concat every chapter MP4 -> renders/master.mp4
  deliver           copy chapters + master to ~/Downloads/generated_videos/<slug>/
"""
import argparse, json, os, subprocess, sys, time, urllib.request
from chapters import CHAPTERS

BASE = "http://127.0.0.1:17493"
PROFILE = "c488e05c-3407-46a3-874d-1b09b3aff78d"  # TTS Bright (Nova)
GAP = 0.5           # silence between beats
PAUSE = 0.6         # silence at each [pause]
ATEMPO = 0.95       # gentle global slowdown
PREFIX = "gpu"

ROOT = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(ROOT, "..", ".."))
COMPOSER = os.path.join(REPO, "composer")
PUBLIC = os.path.join(COMPOSER, "public", PREFIX)
RAW = os.path.join(ROOT, "assets", "raw")
FIN = os.path.join(ROOT, "assets")
ART = os.path.join(ROOT, "artifacts")
REND = os.path.join(ROOT, "renders")
QADIR = os.path.join(ROOT, "qa-stills")
SLUG = "gpu-course"
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


# --------------------------------------------------------------------- BUILD
def chapters_arg(names):
    if not names:
        return CHAPTERS
    return [c for c in CHAPTERS if c["id"] in names or f'ch{c["num"]}' in names or str(c["num"]) in names]


def run_tts():
    grand_total, grand_words = 0.0, 0
    for ch in CHAPTERS:
        manifest, cuts, t = [], [], 0.0
        for sid_short, variant, props, narration in ch["segments"]:
            sid = f'{ch["id"]}_{sid_short}'
            path, d = gen_one(sid, narration)
            if d > 90:
                print(f"    ⚠ LONG scene {sid}: {d:.0f}s — ensure it develops to p≈0.85 or split", flush=True)
            manifest.append((sid, path))
            cuts.append({"id": sid, "type": variant,
                         "in_seconds": round(t, 3), "out_seconds": round(t + d, 3),
                         "props": {**props, "dur": round(d + GAP, 3)}})
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
        props = {"cuts": cuts,
                 "audio": {"narration": {"src": f'{PREFIX}/{ch["id"]}.wav', "volume": 1.0}}}
        json.dump(props, open(os.path.join(ART, f'{ch["id"]}.json'), "w"), indent=1)
        words = sum(len(s[3].replace("[pause]", " ").split()) for s in ch["segments"])
        dur = t - GAP
        grand_total += dur; grand_words += words
        print(f'  {ch["id"]:22s} {dur/60:5.2f} min  {len(ch["segments"])} scenes  {words:5d} words'
              f'  ({words/(dur/60):.0f} wpm)', flush=True)
    print(f'\nMASTER total {grand_total/60:.2f} min ({grand_total:.0f}s) · '
          f'{grand_words} words · {sum(len(c["segments"]) for c in CHAPTERS)} scenes · '
          f'{len(CHAPTERS)} chapters · effective {grand_words/(grand_total/60):.0f} wpm')


def run_qa(names):
    for ch in chapters_arg(names):
        props = os.path.join(ART, f'{ch["id"]}.json')
        if not os.path.exists(props):
            sys.exit("run tts first")
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
                            f"--props={props}", "--concurrency=8", "--timeout=120000"],
                           cwd=COMPOSER, capture_output=True, text=True)
        if r.returncode == 0 and os.path.exists(out):
            os.makedirs(DELIVER, exist_ok=True)
            subprocess.run(["cp", out, os.path.join(DELIVER, f'{ch["id"]}.mp4')], check=True)
            return out
        print(f"  render attempt {a}/{attempts} failed for {ch['id']}:\n" + (r.stderr or r.stdout)[-600:], flush=True)
        if os.path.exists(out):
            os.remove(out)
        time.sleep(5)
    print(f"  GAVE UP on {ch['id']} after {attempts} attempts", flush=True)
    return None


def run_render(names):
    for ch in chapters_arg(names):
        out = render_one(ch)
        if out:
            print(f'  rendered {ch["id"]} ({dur_of(out)/60:.2f} min) -> {DELIVER}', flush=True)


def run_master():
    clist = os.path.join(REND, "master_concat.txt")
    with open(clist, "w") as f:
        for ch in CHAPTERS:
            mp4 = os.path.join(REND, f'{ch["id"]}.mp4')
            if not os.path.exists(mp4):
                sys.exit(f"missing {mp4} — render it first")
            f.write(f"file '{mp4}'\n")
    master = os.path.join(REND, "master.mp4")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", clist,
                    "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
                    "-c:a", "aac", "-b:a", "192k", master], check=True)
    print(f"master: {master} ({dur_of(master)/60:.2f} min)")


def run_deliver():
    os.makedirs(DELIVER, exist_ok=True)
    n = 0
    for ch in CHAPTERS:
        src = os.path.join(REND, f'{ch["id"]}.mp4')
        if os.path.exists(src):
            subprocess.run(["cp", src, os.path.join(DELIVER, f'{ch["id"]}.mp4')], check=True); n += 1
    master = os.path.join(REND, "master.mp4")
    if os.path.exists(master):
        subprocess.run(["cp", master, os.path.join(DELIVER, f"{SLUG}-master.mp4")], check=True)
    print(f"delivered {n} chapters + master -> {DELIVER}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["tts", "qa", "render", "master", "deliver"], nargs="?", default="tts")
    ap.add_argument("names", nargs="*")
    a = ap.parse_args()
    {"tts": lambda: run_tts(), "qa": lambda: run_qa(a.names), "render": lambda: run_render(a.names),
     "master": run_master, "deliver": run_deliver}[a.mode]()
