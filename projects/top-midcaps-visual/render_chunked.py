#!/usr/bin/env python3
"""Disk-safe Chapter 1 renderer for the visual Top Midcaps series."""
import json
import math
import os
import subprocess
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
COMPOSER = ROOT.parents[1] / "composer"
PROPS = ROOT / "artifacts" / "ch01.json"
CHUNKS = ROOT / "renders" / "chunks" / "ch01"
FINAL = ROOT / "renders" / "chapter-01.mp4"
DELIVERED = Path.home() / "Downloads" / "generated_videos" / "top-midcaps-visual" / "top-midcaps-visual-chapter-01.mp4"
CHUNK_FRAMES = 2500


def duration(path: Path) -> float:
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
        capture_output=True, text=True,
    )
    try:
        return float(result.stdout.strip())
    except ValueError:
        return 0.0


data = json.loads(PROPS.read_text())
frames = math.ceil((max(c["out_seconds"] for c in data["cuts"]) + 1) * 30)
CHUNKS.mkdir(parents=True, exist_ok=True)
DELIVERED.parent.mkdir(parents=True, exist_ok=True)
parts = []

for index, start in enumerate(range(0, frames, CHUNK_FRAMES)):
    end = min(start + CHUNK_FRAMES - 1, frames - 1)
    output = CHUNKS / f"{index:03d}.mp4"
    if output.exists() and duration(output) > 0:
        parts.append(output)
        continue
    for attempt in range(1, 4):
        result = subprocess.run(
            ["npx", "remotion", "render", "Explainer", str(output), f"--props={PROPS}",
             f"--frames={start}-{end}", "--concurrency=8", "--timeout=600000"],
            cwd=COMPOSER, capture_output=True, text=True,
        )
        if result.returncode == 0 and duration(output) > 0:
            break
        if output.exists():
            output.rename(output.with_suffix(f".failed-{attempt}.mp4"))
        print((result.stderr or result.stdout)[-500:], flush=True)
        time.sleep(2)
    else:
        raise SystemExit(f"Chunk {index + 1} failed")
    parts.append(output)
    print(f"[{time.strftime('%H:%M:%S')}] chunk {index + 1}/{math.ceil(frames / CHUNK_FRAMES)} complete", flush=True)

concat = CHUNKS / "concat.txt"
concat.write_text("".join(f"file '{p}'\n" for p in parts))
subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(concat), "-c", "copy", str(FINAL)], check=True)
subprocess.run(["cp", str(FINAL), str(DELIVERED)], check=True)
print(f"DONE: {duration(DELIVERED) / 60:.2f} minutes -> {DELIVERED}")
