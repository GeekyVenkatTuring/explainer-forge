#!/usr/bin/env python3
"""Disk-safe chunked renderer. Renders each chapter in frame-range slices (low peak
temp), stream-concats the slices, delivers, and deletes slices between chapters so a
near-full disk can't cause ENOSPC. Then builds the master. Usage: render_chunked.py ch03 ch04 ch05"""
import json, os, subprocess, sys, math, time
ROOT = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(ROOT, "..", ".."))
COMPOSER = os.path.join(REPO, "composer")
ART = os.path.join(ROOT, "artifacts")
REND = os.path.join(ROOT, "renders")
DELIVER = os.path.expanduser("~/Downloads/generated_videos/nifty-beaters")
CHUNK = 2500
os.makedirs(DELIVER, exist_ok=True)

def ffdur(p):
    try:
        o = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                            "-of", "default=noprint_wrappers=1:nokey=1", p], capture_output=True, text=True)
        return round(float(o.stdout.strip()), 3)
    except Exception:
        return 0.0

def total_frames(props):
    d = json.load(open(props))
    mx = max(c["out_seconds"] for c in d["cuts"])
    return math.ceil((mx + 1) * 30)

def render_chapter(chid):
    props = os.path.join(ART, f"{chid}.json")
    N = total_frames(props)
    cdir = os.path.join(REND, "chunks", chid)
    os.makedirs(cdir, exist_ok=True)
    starts = list(range(0, N, CHUNK))
    parts = []
    print(f"[{time.strftime('%H:%M')}] {chid}: {N} frames -> {len(starts)} chunks", flush=True)
    for i, start in enumerate(starts):
        end = min(start + CHUNK - 1, N - 1)
        out = os.path.join(cdir, f"{i:03d}.mp4")
        if os.path.exists(out) and ffdur(out) > 0:
            parts.append(out); continue
        for att in range(1, 4):
            r = subprocess.run(["npx", "remotion", "render", "Explainer", out, f"--props={props}",
                                f"--frames={start}-{end}", "--concurrency=2", "--timeout=600000"],
                               cwd=COMPOSER, capture_output=True, text=True)
            if r.returncode == 0 and os.path.exists(out):
                break
            if os.path.exists(out):
                os.remove(out)
            print(f"  {chid} chunk {i} [{start}-{end}] attempt {att} FAILED: " + (r.stderr or r.stdout)[-260:], flush=True)
            time.sleep(4)
        else:
            print(f"  GAVE UP on {chid} chunk {i}", flush=True); return None
        parts.append(out)
        print(f"  [{time.strftime('%H:%M')}] {chid} chunk {i+1}/{len(starts)} ok", flush=True)
    lst = os.path.join(cdir, "concat.txt")
    with open(lst, "w") as f:
        for p in parts:
            f.write(f"file '{p}'\n")
    final = os.path.join(REND, f"{chid}.mp4")
    subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", final],
                   check=True, capture_output=True)
    subprocess.run(["cp", final, os.path.join(DELIVER, f"nifty-beaters-{chid}.mp4")], check=True)
    for p in parts:  # reclaim slice space immediately
        os.remove(p)
    print(f"  [{time.strftime('%H:%M')}] {chid} DONE {ffdur(final)/60:.2f} min -> delivered", flush=True)
    return final

def build_master():
    from chapters import CHAPTERS
    files = [os.path.join(REND, f'{c["id"]}.mp4') for c in CHAPTERS]
    files = [f for f in files if os.path.exists(f)]
    if len(files) < len(CHAPTERS):
        print(f"  master: only {len(files)}/{len(CHAPTERS)} chapters present; skipping"); return
    lst = os.path.join(ART, "master_concat.txt")
    with open(lst, "w") as f:
        for p in files:
            f.write(f"file '{p}'\n")
    out = os.path.join(REND, "master.mp4")
    subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", out], check=True)
    subprocess.run(["cp", out, os.path.join(DELIVER, "nifty-beaters-master.mp4")], check=True)
    print(f"  [{time.strftime('%H:%M')}] master {ffdur(out)/60:.2f} min -> delivered", flush=True)

if __name__ == "__main__":
    chapters = sys.argv[1:] or ["ch03", "ch04", "ch05"]
    for ch in chapters:
        if not render_chapter(ch):
            print(f"STOP: {ch} failed"); sys.exit(1)
    build_master()
    print(f"[{time.strftime('%H:%M')}] ALL DONE")
