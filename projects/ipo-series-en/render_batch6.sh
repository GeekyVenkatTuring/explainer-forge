#!/bin/bash
# Render BATCH 6 videos + thumbnails. Run from composer/. concurrency=3 + timeout (8 crashes this machine).
set -e
cd /Users/appuram/Developer/explainer-forge/composer
PROJ=/Users/appuram/Developer/explainer-forge/projects/ipo-series-en
CHS="${*:-horizon lalithaa shankesh sunshine gaja}"
mkdir -p "$PROJ/renders"
for ch in $CHS; do
  echo "=== THUMB $ch ==="
  npx remotion still Thumbnail "$PROJ/renders/$ch.thumb.png" --props="$PROJ/artifacts/$ch.thumb.json" --frame=0
  echo "=== RENDER $ch ==="
  npx remotion render Explainer "$PROJ/renders/$ch.mp4" --props="$PROJ/artifacts/$ch.json" --concurrency=3 --timeout=90000
  echo "=== DONE $ch ==="
done
echo "ALL BATCH-6 RENDERS COMPLETE"
