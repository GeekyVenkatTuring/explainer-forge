# Skill 07 — Rendering

## Commands (always run from `composer/` — cwd matters)
```bash
cd ~/Developer/explainer-forge/composer

# stills (QA)
npx remotion still Explainer /tmp/stills/s3.png --props=... --frame=3240

# final render
npx remotion render Explainer ../projects/<slug>/renders/final.mp4 \
  --props=../projects/<slug>/artifacts/edit_decisions.json --concurrency=8
```
Running `npx remotion` from the wrong directory fails with npm's cryptic
"could not determine executable to run" — `cd` to `composer/` first. Note the shell's
cwd drifts between commands in this harness; use absolute `cd` in each command.

## Expectations & behavior
- Throughput ≈ **5–6 fps at 1080p, concurrency 8** on this machine (measured):
  5-min video (~9k frames) ≈ 30 min · 20-min video (~36k frames) ≈ 1h50m.
- Remotion v4 streams frames internally and writes the MP4 **only at the very end** —
  an empty `renders/` directory during the run is normal, not a failure. Check
  liveness via `ps aux | grep chrome-headless` (workers at high CPU = rendering).
- Run renders in the background. If you pipe output through `tail`, progress is
  buffered until completion — that's cosmetic.
- Long renders: launch, then do other work; verify on the completion notification.

## Performance rules (set at authoring time, enforced here)
- No CSS `filter`/`backdrop-filter` anywhere (a past full-frame blur(40px) turned a
  40k-frame render into 1h40m). Grep before rendering long videos:
  `grep -rn "filter:" src/scenes/<YourScenes>.tsx`
- Prefer divs/SVG/gradients; avoid thousands-of-nodes scenes (cap particle counts
  ~10–20 per Flow; grids ≤ ~20×20 with values, larger without).

## Verify the deliverable
```bash
ffprobe -v error -show_entries format=duration,size -of default=noprint_wrappers=1 final.mp4
ffprobe -v error -show_entries stream=codec_type,codec_name -of csv=p=0 final.mp4  # expect h264 + aac
ffmpeg -y -v error -ss <mid> -i final.mp4 -frames:v 1 /tmp/check.png               # and LOOK at it
```
Deliver to `~/Downloads/generated_videos/<slug>.mp4` (user's convention) and report:
duration, size, scene count, what QA caught/fixed, and honest caveats.
