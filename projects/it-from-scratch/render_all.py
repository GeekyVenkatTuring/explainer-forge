#!/usr/bin/env python3
"""Render every chapter as soon as its narration JSON is ready, in order, then
build + deliver the master automatically.

Renders sequentially at --concurrency=8 (via build.render_one, which also copies
each finished MP4 to the delivery folder immediately). Burned-in captions are ON
(each chapter's props JSON carries caption cues). When all chapters are done, it
concats the master and copies chapters + master to the delivery folder.
Idempotent: already-rendered chapter MP4s are skipped, so it is safe to re-run.
"""
import os
import build
from chapters import CHAPTERS

# Render each chapter (idempotent: skip ones already on disk). render_one retries
# transient headless-browser crashes internally; if a chapter still fails we record it,
# finish the rest, then do one more pass over the failures before deciding on the master.
def render_pass():
    for ch in CHAPTERS:
        mp = os.path.join(build.REND, ch["id"] + ".mp4")
        if os.path.exists(mp):
            continue
        if os.path.exists(os.path.join(build.ART, ch["id"] + ".json")):
            out = build.render_one(ch)
            if out:
                print(f"rendered {ch['id']} ({build.dur_of(out)/60:.2f} min)", flush=True)

render_pass()
missing = [c["id"] for c in CHAPTERS if not os.path.exists(os.path.join(build.REND, c["id"] + ".mp4"))]
if missing:
    print(f"retrying {len(missing)} unrendered chapter(s): {missing}", flush=True)
    render_pass()
    missing = [c["id"] for c in CHAPTERS if not os.path.exists(os.path.join(build.REND, c["id"] + ".mp4"))]

if missing:
    print(f"STILL MISSING after retries: {missing} — fix and re-run; NOT building master.", flush=True)
else:
    print(f"ALL {len(CHAPTERS)} CHAPTERS RENDERED", flush=True)
    print("building master…", flush=True)
    build.run_master()
    build.run_deliver()
    print("MASTER BUILT + DELIVERED", flush=True)
