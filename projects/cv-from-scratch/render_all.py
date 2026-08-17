#!/usr/bin/env python3
"""Render every chapter as soon as its narration JSON is ready, in order.

Renders sequentially at --concurrency=8 (via build.render_one, which also copies
each finished MP4 to the delivery folder). Picks up new chapters produced by an
in-flight TTS pass, so it can run concurrently with build.py tts. Captions are
disabled at the Explainer level, so these renders have no burned-in captions.
"""
import os, time
import build
from chapters import CHAPTERS

done = set()
while len(done) < len(CHAPTERS):
    progressed = False
    for ch in CHAPTERS:
        if ch["id"] in done:
            continue
        mp = os.path.join(build.REND, ch["id"] + ".mp4")
        jp = os.path.join(build.ART, ch["id"] + ".json")
        if os.path.exists(mp):
            done.add(ch["id"]); continue
        if os.path.exists(jp):
            build.render_one(ch)
            print(f"rendered {ch['id']} ({build.dur_of(mp)/60:.2f} min)  [{len(done)+1}/{len(CHAPTERS)}]", flush=True)
            done.add(ch["id"]); progressed = True
    if len(done) < len(CHAPTERS) and not progressed:
        time.sleep(20)
print(f"ALL {len(done)} CHAPTERS RENDERED", flush=True)
