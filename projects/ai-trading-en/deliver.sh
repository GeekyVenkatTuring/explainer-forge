#!/bin/zsh
# Idempotently deliver fully-written chapters (and the master) to the output folder.
# A chapter is "safe to copy" only once the NEXT chapter's render has started (Remotion
# writes the mp4 at the very end), or the concat/DONE step has run.
R=/Users/appuram/Developer/explainer-forge/projects/ai-trading-en/renders
OUT=~/Downloads/generated_videos/ai-trading-honestly
LOG=/private/tmp/claude-501/-Users-appuram-Developer-explainer-forge/079d19f2-977b-4876-b5b1-92d8e0609bf0/tasks/b3avtyzp2.output
mkdir -p "$OUT"
names=(00-intro 01-what-ai-trading-is 02-the-reality-check 03-before-you-start 04-where-to-do-it 05-build-your-own 06-your-plan 07-recap)
done_all=0
grep -q "RENDER+STITCH DONE\|== DONE ==\|== concat" "$LOG" 2>/dev/null && done_all=1
for k in {0..7}; do
  src="$R/ch$k.mp4"; dst="$OUT/${names[$((k+1))]}.mp4"   # zsh arrays are 1-indexed
  [[ -s "$src" ]] || continue
  next=$((k+1))
  if [[ $done_all -eq 1 ]] || grep -q "render ch$next " "$LOG" 2>/dev/null; then
    if [[ ! -s "$dst" || "$src" -nt "$dst" ]]; then cp -f "$src" "$dst"; echo "delivered ${names[$((k+1))]}.mp4"; fi
  fi
done
if [[ -s "$R/master.mp4" ]]; then
  cp -f "$R/master.mp4" "$OUT/ai-trading-honestly-FULL.mp4"; echo "delivered ai-trading-honestly-FULL.mp4"
fi
echo "--- output folder ---"; ls -1 "$OUT"