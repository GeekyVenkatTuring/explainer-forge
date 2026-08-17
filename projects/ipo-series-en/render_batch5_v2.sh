#!/bin/bash
# Rebuild (adds 'clients' beat narration) + re-render all 8 BATCH-5 videos at 10 beats, concurrency 4.
set -e
PROJ=/Users/appuram/Developer/explainer-forge/projects/ipo-series-en
CHS="dhoot molbio milkymist shiprocket beharilal fascinate shamfoam pramodini"
cd "$PROJ"
echo "=== BUILD (TTS + artifacts) $(date +%H:%M:%S) ==="
python3 build.py $CHS
cd /Users/appuram/Developer/explainer-forge/composer
for ch in $CHS; do
  echo "=== RENDER $ch $(date +%H:%M:%S) ==="
  npx remotion render Explainer "$PROJ/renders/$ch.mp4" --props="$PROJ/artifacts/$ch.json" --concurrency=4
  echo "=== DONE $ch $(date +%H:%M:%S) ==="
done
echo "V2 ALL COMPLETE"
