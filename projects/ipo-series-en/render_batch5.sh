#!/bin/bash
# Render BATCH 5 videos + thumbnails. Run from composer/ (cwd matters for npx remotion).
set -e
cd /Users/appuram/Developer/explainer-forge/composer
PROJ=/Users/appuram/Developer/explainer-forge/projects/ipo-series-en
CHS="dhoot molbio milkymist shiprocket beharilal fascinate shamfoam pramodini"
mkdir -p "$PROJ/renders"
for ch in $CHS; do
  echo "=== THUMB $ch ==="
  npx remotion still Thumbnail "$PROJ/renders/$ch.thumb.png" --props="$PROJ/artifacts/$ch.thumb.json" --frame=0
  echo "=== RENDER $ch ==="
  npx remotion render Explainer "$PROJ/renders/$ch.mp4" --props="$PROJ/artifacts/$ch.json" --concurrency=8
  echo "=== DONE $ch ==="
done
echo "ALL RENDERS COMPLETE"
