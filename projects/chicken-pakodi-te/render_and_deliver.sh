#!/usr/bin/env bash
# Render chapters one at a time. Each completed chapter is verified and copied to
# the user's output directory before the next chapter starts; only then build master.
set -euo pipefail

repo="/Users/appuram/Developer/explainer-forge"
project="$repo/projects/chicken-pakodi-te"
renders="$project/renders"
deliver="/Users/appuram/Downloads/generated_videos"

mkdir -p "$renders" "$deliver"

deliver_chapter() {
  local chapter="$1"
  local source="$renders/${chapter}.mp4"
  local destination="$deliver/chicken-pakodi-te-${chapter}.mp4"

  ffprobe -v error -show_entries format=duration,size -of default=noprint_wrappers=1 "$source"
  cp -p "$source" "$destination"
  echo "DELIVERED $chapter -> $destination"
}

for chapter in ch01 ch02 ch03 ch04 ch05 ch06 ch07; do
  if [[ ! -f "$renders/${chapter}.mp4" ]]; then
    (
      cd "$repo/composer"
      npx remotion render Explainer "$renders/${chapter}.mp4" \
        --props="$project/artifacts/${chapter}.json" --concurrency=8
    )
  fi
  deliver_chapter "$chapter"
done

(
  cd "$project"
  python3 build.py master
)
ffprobe -v error -show_entries format=duration,size -of default=noprint_wrappers=1 "$renders/master.mp4"
cp -p "$renders/master.mp4" "$deliver/chicken-pakodi-te-master.mp4"
echo "DELIVERED MASTER -> $deliver/chicken-pakodi-te-master.mp4"
