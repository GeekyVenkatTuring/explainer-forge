#!/usr/bin/env python3
"""Print `npx remotion still` commands at ~60% into chosen cuts (QA), from the
real edit_decisions.json. Usage: python3 qa_stills.py [cut_id ...]  (default = a
representative set covering every layout branch)."""
import json, os, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
ed = json.load(open(os.path.join(ROOT, "artifacts", "edit_decisions.json")))
cuts = {c["id"]: c for c in ed["cuts"]}
want = sys.argv[1:] or [
    "s00_title", "d1", "c01_maruti", "c03_tmpv", "c04_mm", "c11_ather",
    "c12_ola", "c13_olectra", "c14_mercury", "c16_vst", "c17_tube", "c18_atlas", "s99_recap",
]
outdir = "/private/tmp/claude-501/-Users-appuram-Developer-explainer-forge/5fd2e11f-6315-4557-a9a9-b78d05cc9949/scratchpad/qa"
os.makedirs(outdir, exist_ok=True)
for cid in want:
    c = cuts.get(cid)
    if not c:
        print(f"# MISSING {cid}"); continue
    f = int((c["in_seconds"] + 0.6 * (c["out_seconds"] - c["in_seconds"])) * 30)
    print(f'npx remotion still Explainer {outdir}/{cid}.png --props={ROOT}/artifacts/edit_decisions.json --frame={f}')
