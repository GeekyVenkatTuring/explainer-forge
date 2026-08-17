#!/bin/bash
# Re-render remaining BATCH 5 videos at lower concurrency (browser crashed at conc 8).
set -e
cd /Users/appuram/Developer/explainer-forge/composer
PROJ=/Users/appuram/Developer/explainer-forge/projects/ipo-series-en
CHS="molbio milkymist shiprocket beharilal fascinate shamfoam pramodini"
for ch in $CHS; do
  echo "=== THUMB $ch ==="
  npx remotion still Thumbnail "$PROJ/renders/$ch.thumb.png" --props="$PROJ/artifacts/$ch.thumb.json" --frame=0
  echo "=== RENDER $ch $(date +%H:%M:%S) ==="
  npx remotion render Explainer "$PROJ/renders/$ch.mp4" --props="$PROJ/artifacts/$ch.json" --concurrency=4
  echo "=== DONE $ch $(date +%H:%M:%S) ==="
done
echo "REST RENDERS COMPLETE"
