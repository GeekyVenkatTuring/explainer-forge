#!/usr/bin/env python3
"""Print mid-scene (60%) frame indices for each cut in a chapter artifact.
Usage: python3 qa/frames.py ch01 [pct]  -> lines: <sceneIdx> <id> <type> <frame>
"""
import json, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ch = sys.argv[1]
pct = float(sys.argv[2]) if len(sys.argv) > 2 else 0.6
data = json.load(open(os.path.join(ROOT, "artifacts", f"{ch}.json")))
for i, c in enumerate(data["cuts"]):
    a, b = c["in_seconds"], c["out_seconds"]
    frame = round((a + (b - a) * pct) * 30)
    print(f"{i}\t{c['id']}\t{c['type']}\t{frame}")
