#!/bin/zsh
# Render the remaining pieces (ch5 split into ch5a+ch5b, plus ch6, ch7), recombine
# Part 5, then concat the master. Resumable: skips any non-empty existing output.
# Each render self-cleans its temp on success (disk was exhausted by the killed big-ch5
# renders; halves keep the temp footprint ~1.5GB each with plenty of headroom).
set -e
COMPOSER=/Users/appuram/Developer/explainer-forge/composer
PROJ=/Users/appuram/Developer/explainer-forge/projects/ai-trading-en
cd "$COMPOSER"

render() {  # $1 = chapter id
  local out="$PROJ/renders/$1.mp4"
  if [[ -s "$out" ]]; then echo "== skip $1 (exists) =="; return; fi
  echo "== render $1 =="
  npx remotion render Explainer "$out" \
    --props="$PROJ/artifacts/$1.json" --concurrency=6 --crf=22 --log=error
  echo "   $1 size: $(du -h "$out" | cut -f1)   disk left: $(df -h "$PROJ" | tail -1 | awk '{print $4}')"
}

render ch5a
render ch5b
render ch6
render ch7

# recombine Part 5 into a single file for clean delivery
echo "== combine ch5a+ch5b -> ch5.mp4 =="
c5="$PROJ/renders/ch5_concat.txt"; : > "$c5"
echo "file '$PROJ/renders/ch5a.mp4'" >> "$c5"
echo "file '$PROJ/renders/ch5b.mp4'" >> "$c5"
ffmpeg -y -f concat -safe 0 -i "$c5" -c copy "$PROJ/renders/ch5.mp4"

# master = all parts in order
echo "== concat master =="
list="$PROJ/renders/concat.txt"; : > "$list"
for ch in ch0 ch1 ch2 ch3 ch4 ch5a ch5b ch6 ch7; do
  echo "file '$PROJ/renders/$ch.mp4'" >> "$list"
done
ffmpeg -y -f concat -safe 0 -i "$list" -c copy "$PROJ/renders/master.mp4"

echo "== ALL DONE =="
ffprobe -v error -show_entries format=duration,size -of default=noprint_wrappers=1 "$PROJ/renders/master.mp4"
