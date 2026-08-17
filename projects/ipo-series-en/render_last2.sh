#!/bin/bash
set -e
PROJ=/Users/appuram/Developer/explainer-forge/projects/ipo-series-en
cd /Users/appuram/Developer/explainer-forge/composer
for ch in shamfoam pramodini; do
  echo "=== RENDER $ch $(date +%H:%M:%S) ==="
  npx remotion render Explainer "$PROJ/renders/$ch.mp4" --props="$PROJ/artifacts/$ch.json" --concurrency=3 --timeout=90000
  echo "=== DONE $ch $(date +%H:%M:%S) ==="
done
echo "LAST2 COMPLETE"
