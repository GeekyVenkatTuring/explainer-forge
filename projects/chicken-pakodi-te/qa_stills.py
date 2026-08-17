#!/usr/bin/env python3
"""Render a mid-scene still per cut for QA. Usage: python3 qa_stills.py [ch01 ch02 ...]"""
import json, os, subprocess, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(ROOT, "..", ".."))
COMPOSER = os.path.join(REPO, "composer")
QA = os.path.join(ROOT, "qa")
os.makedirs(QA, exist_ok=True)
FPS = 30
chs = sys.argv[1:] or [f"ch0{i}" for i in range(1, 8)]
for ch in chs:
    j = os.path.join(ROOT, "artifacts", f"{ch}.json")
    if not os.path.exists(j):
        print("skip", ch); continue
    data = json.load(open(j))
    for cut in data["cuts"]:
        mid = (cut["in_seconds"] + cut["out_seconds"]) / 2
        frame = round(mid * FPS)
        out = os.path.join(QA, f"{ch}_{cut['id']}.png")
        print(f"{ch} {cut['id']:14s} frame {frame}", flush=True)
        subprocess.run(["npx", "remotion", "still", "Explainer", out,
                        f"--props={j}", f"--frame={frame}"],
                       cwd=COMPOSER, check=True, capture_output=True)
print("done")
