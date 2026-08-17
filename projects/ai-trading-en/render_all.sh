#!/bin/zsh
# Render each chapter to its own MP4 (resumable: skips non-empty existing files),
# then concat into the master. Run from anywhere.
set -e
COMPOSER=/Users/appuram/Developer/explainer-forge/composer
PROJ=/Users/appuram/Developer/explainer-forge/projects/ai-trading-en
cd "$COMPOSER"

CHS=(ch0 ch1 ch2 ch3 ch4 ch5 ch6 ch7)
for ch in $CHS; do
  out="$PROJ/renders/$ch.mp4"
  if [[ -s "$out" ]]; then
    echo "== skip $ch (exists) =="
    continue
  fi
  echo "== render $ch =="
  npx remotion render Explainer "$out" \
    --props="$PROJ/artifacts/$ch.json" --concurrency=8 --crf=22 --log=error
  echo "   size: $(du -h "$out" | cut -f1)   disk left: $(df -h "$PROJ" | tail -1 | awk '{print $4}')"
done

echo "== concat -> master.mp4 =="
list="$PROJ/renders/concat.txt"
: > "$list"
for ch in $CHS; do echo "file '$PROJ/renders/$ch.mp4'" >> "$list"; done
ffmpeg -y -f concat -safe 0 -i "$list" -c copy "$PROJ/renders/master.mp4"

echo "== DONE =="
ffprobe -v error -show_entries format=duration,size -of default=noprint_wrappers=1 "$PROJ/renders/master.mp4"
