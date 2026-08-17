#!/usr/bin/env python3
"""Computer Vision From Scratch — chapter-wise build orchestrator (Remotion).

Mirrors the LLM-from-scratch series: each chapter renders to its own MP4 and all
chapters concat into a >1h master. Burned-in captions (skills default is none; the
user asked for captions). Nova voice, 16:9 1080p30, no vertical.

Modes:
  tts               generate/cache narration WAVs, concat per chapter, write
                    per-chapter edit_decisions (cuts + caption cues); print durations
  qa   [chid...]    render a mid-animation still for every scene → qa-stills/
  render [chid...]  final 1080p30 render per chapter (Remotion, --concurrency=8)
  master            ffmpeg-concat every chapter MP4 → renders/master.mp4
  deliver           copy chapters + master to ~/Downloads/generated_videos/<slug>/

TTS: Voicebox local API (http://127.0.0.1:17493, app must be open). Idempotent —
delete a segment's assets/<id>.wav to regenerate just that beat.
"""
import argparse, json, os, subprocess, sys, time, urllib.request
from concurrent.futures import ThreadPoolExecutor
from chapters import CHAPTERS

BASE = "http://127.0.0.1:17493"
PROFILE = "c488e05c-3407-46a3-874d-1b09b3aff78d"  # TTS Bright (Nova)
GAP = 0.5           # silence between beats
PAUSE = 0.6         # silence at each [pause]
ATEMPO = 0.95       # gentle global slowdown
PREFIX = "cv"
CAP_MAXWORDS = 8
CAP_WRAP = 42       # wrap width (chars) per caption line

ROOT = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(ROOT, "..", ".."))
COMPOSER = os.path.join(REPO, "composer")
PUBLIC = os.path.join(COMPOSER, "public", PREFIX)
RAW = os.path.join(ROOT, "assets", "raw")
FIN = os.path.join(ROOT, "assets")
ART = os.path.join(ROOT, "artifacts")
REND = os.path.join(ROOT, "renders")
QADIR = os.path.join(ROOT, "qa-stills")
SLUG = "computer-vision-from-scratch"
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
    """Caption cues [start,end,text] for one beat, offset by t0 seconds."""
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
def chapters_arg(names):
    if not names:
        return CHAPTERS
    return [c for c in CHAPTERS if c["id"] in names or c["id"].replace("cv-", "") in names]


def run_tts():
    grand_total, grand_words = 0.0, 0
    for ch in CHAPTERS:
        manifest, cues, cuts, t = [], [], [], 0.0
        for seg in ch["segments"]:
            sid = f'{ch["id"]}_{seg["id"]}'
            path, d = gen_one(sid, seg["narration"])
            manifest.append((sid, path))
            cues.extend(beat_cues(seg["narration"], d, t))
            cuts.append({"id": sid, "type": seg["variant"],
                         "in_seconds": round(t, 3), "out_seconds": round(t + d, 3),
                         "props": {**seg.get("props", {}), "dur": round(d + GAP, 3)}})
            t = round(t + d + GAP, 3)
        # concat this chapter's narration with gaps
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
        props = {"cuts": cuts, "captions": cues,
                 "audio": {"narration": {"src": f'{PREFIX}/{ch["id"]}.wav', "volume": 1.0}}}
        json.dump(props, open(os.path.join(ART, f'{ch["id"]}.json'), "w"), indent=1)
        words = sum(len(s["narration"].replace("[pause]", " ").split()) for s in ch["segments"])
        dur = t - GAP
        grand_total += dur; grand_words += words
        print(f'  {ch["id"]:26s} {dur/60:5.2f} min  {len(ch["segments"])} scenes  {words:5d} words', flush=True)
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


def render_one(ch):
    props = os.path.join(ART, f'{ch["id"]}.json')
    out = os.path.join(REND, f'{ch["id"]}.mp4')
    r = subprocess.run(["npx", "remotion", "render", "Explainer", out,
                        f"--props={props}", "--concurrency=8"],
                       cwd=COMPOSER, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stdout[-1200:], r.stderr[-1200:]); sys.exit(f"render failed {ch['id']}")
    # copy to the delivery folder immediately, so chapters appear as they finish
    os.makedirs(DELIVER, exist_ok=True)
    subprocess.run(["cp", out, os.path.join(DELIVER, f'{ch["id"]}.mp4')], check=True)
    return out


def run_render(names):
    for ch in chapters_arg(names):
        out = render_one(ch)
        print(f'  rendered {ch["id"]} ({dur_of(out)/60:.2f} min)', flush=True)


def run_master():
    clist = os.path.join(REND, "master_concat.txt")
    with open(clist, "w") as f:
        for ch in CHAPTERS:
            mp4 = os.path.join(REND, f'{ch["id"]}.mp4')
            if not os.path.exists(mp4):
                sys.exit(f"missing {mp4} — render it first")
            f.write(f"file '{mp4}'\n")
    master = os.path.join(REND, "master.mp4")
    # re-encode on concat to guarantee uniform streams
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", clist,
                    "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
                    "-c:a", "aac", "-b:a", "192k", master], check=True)
    print(f"master: {master} ({dur_of(master)/60:.2f} min)")


def run_deliver():
    os.makedirs(DELIVER, exist_ok=True)
    n = 0
    for i, ch in enumerate(CHAPTERS, 1):
        src = os.path.join(REND, f'{ch["id"]}.mp4')
        if os.path.exists(src):
            dst = os.path.join(DELIVER, f'{ch["id"]}.mp4')
            subprocess.run(["cp", src, dst], check=True); n += 1
    master = os.path.join(REND, "master.mp4")
    if os.path.exists(master):
        subprocess.run(["cp", master, os.path.join(DELIVER, f"{SLUG}-master.mp4")], check=True)
    print(f"delivered {n} chapters + master → {DELIVER}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["tts", "qa", "render", "master", "deliver"], nargs="?", default="tts")
    ap.add_argument("names", nargs="*")
    a = ap.parse_args()
    if a.mode == "tts":
        run_tts()
    elif a.mode == "qa":
        run_qa(a.names)
    elif a.mode == "render":
        run_render(a.names)
    elif a.mode == "master":
        run_master()
    elif a.mode == "deliver":
        run_deliver()
