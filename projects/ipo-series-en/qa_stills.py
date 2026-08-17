#!/usr/bin/env python3
"""Render a mid-animation still of EVERY scene in the given chapters (QA gate, hard rule 5).
Usage: python3 qa_stills.py horizon lalithaa ...
Writes renders/qa/<ch>__<sceneid>.png. For sm_stats/sm_financials the counters finish late, so we
sample at ~82% of each scene (per QA note in memory) rather than the exact midpoint."""
import json, os, subprocess, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
COMPOSER = os.path.abspath(os.path.join(ROOT, "..", "..", "composer"))
ART = os.path.join(ROOT, "artifacts")
QA = os.path.join(ROOT, "renders", "qa"); os.makedirs(QA, exist_ok=True)
FPS = 30
LATE = {"sm_stats", "sm_financials", "sm_peers"}  # counters/bars finish late → sample at 82%

for ch in (sys.argv[1:] or ["horizon"]):
    data = json.load(open(os.path.join(ART, f"{ch}.json")))
    for c in data["cuts"]:
        a, b = c["in_seconds"], c["out_seconds"]
        frac = 0.82 if c["type"] in LATE else 0.5
        frame = int((a + (b - a) * frac) * FPS)
        out = os.path.join(QA, f"{ch}__{c['id']}.png")
        print(f"{ch} {c['id']:24s} {c['type']:16s} frame={frame}", flush=True)
        subprocess.run(["npx", "remotion", "still", "Explainer", out,
                        f"--props={os.path.join(ART, ch + '.json')}", f"--frame={frame}"],
                       cwd=COMPOSER, check=True, capture_output=True)
    print(f"{ch}: stills done -> {QA}")
print("QA stills complete")
