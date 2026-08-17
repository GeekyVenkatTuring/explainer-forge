#!/usr/bin/env python3
"""LLM Training Strategies — YouTube Short build script.

2-minute explainer: 5 LLM training strategies in 8 scenes.
Voice: TTS Bright (Nova) via Voicebox.app local API.
Calibration: Nova ≈ 212 wpm including gaps.
"""
import json, os, subprocess, time, urllib.request

BASE = "http://127.0.0.1:17493"
PROFILE = "c488e05c-3407-46a3-874d-1b09b3aff78d"  # "TTS Bright (Nova)"
GAP = 0.35
PREFIX = "llm"
ROOT = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(ROOT, "..", ".."))
PUBLIC = os.path.join(REPO, "composer", "public", PREFIX)
RAW = os.path.join(ROOT, "assets", "raw")
FIN = os.path.join(ROOT, "assets")
for d in (PUBLIC, RAW, os.path.join(ROOT, "artifacts"), os.path.join(ROOT, "renders")):
    os.makedirs(d, exist_ok=True)

# ---------------------------------------------------------------- SCREENPLAY
# (seg_id, variant, scene_props, narration)
# Written for TTS: spoken language, ~212 wpm
SEGMENTS = [
 ("s01_title", "llm_title", {},
  "LLM training strategies. Five distinct techniques that transform a raw "
  "neural network into a capable AI assistant."),

 ("s02_hook", "llm_hook", {},
  "It is not just one single training run. There are five training strategies "
  "used in sequence, and together they turn a basic language model into "
  "something truly intelligent and useful."),

 ("s03_pretrain", "llm_pretrain", {},
  "Stage one, pretraining. The model reads enormous amounts of text. Books, "
  "articles, websites, code repositories. Billions of words, trillions of "
  "tokens. It learns grammar, factual knowledge, reasoning patterns, and how "
  "language works at a deep statistical level. This builds the foundation for "
  "everything that comes next."),

 ("s04_sft", "llm_sft", {},
  "Stage two, supervised fine-tuning. Now we train the model on high quality "
  "examples: human written questions paired with ideal answers. The model "
  "learns to follow instructions, stay on topic, and respond helpfully instead "
  "of just predicting the next word. It transforms from a text completer into "
  "an assistant."),

 ("s05_lora", "llm_lora", {},
  "Stage three, LoRA. Retraining every parameter is expensive. LoRA freezes "
  "the original model and inserts small trainable adapter matrices. Only these "
  "lightweight modules are updated. Fine-tuning becomes fast, cheap, and "
  "practical. A fraction of the usual memory and compute."),

 ("s06_qlora", "llm_qlora", {},
  "Stage four, QLoRA. This compresses the frozen base model down to four bit "
  "precision before adding LoRA adapters. Memory drops by up to four times, "
  "while the model retains most of its original quality. Now large models can "
  "be fine tuned on a single consumer GPU."),

 ("s07_rlhf", "llm_rlhf", {},
  "Stage five, RLHF. Reinforcement learning from human feedback. Human "
  "evaluators compare generated responses and choose the better one. The model "
  "trains on these preferences, learning to be more accurate, less harmful, "
  "and better aligned with what people actually want. This is what makes AI "
  "assistants safe and helpful."),

 ("s08_recap", "llm_recap",
  {"items": [
      "Pretraining — build a strong foundation",
      "SFT — teach instruction following",
      "LoRA — efficient fine-tuning",
      "QLoRA — fine-tune with less memory",
      "RLHF — align with human values",
  ], "closer": "Five strategies. One intelligent assistant."},
  "Pretraining builds the foundation. SFT teaches instruction following. LoRA "
  "makes tuning efficient. QLoRA cuts memory costs. RLHF aligns with human "
  "values. Five strategies, working together, to create the AI assistants we "
  "rely on every day."),
]


def post(p, b):
    req = urllib.request.Request(BASE + p, data=json.dumps(b).encode(),
                                 headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode())


def get(p):
    with urllib.request.urlopen(BASE + p, timeout=30) as r:
        return r.read()


def gen_one(seg_id, text):
    """Generate one narration WAV via Voicebox (skips if it already exists)."""
    fin = os.path.join(FIN, seg_id + ".wav")
    if os.path.exists(fin):
        out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                              "-of", "default=noprint_wrappers=1:nokey=1", fin],
                             capture_output=True, text=True, check=True)
        return fin, round(float(out.stdout.strip()), 3)
    gid = post("/generate", {"profile_id": PROFILE, "text": text, "engine": "kokoro"})["id"]
    for _ in range(300):
        raw = get(f"/generate/{gid}/status").decode()
        line = [l for l in raw.splitlines() if l.startswith("data:")]
        st = json.loads(line[-1][5:].strip()) if line else None
        if st and st.get("status") == "completed":
            break
        time.sleep(1)
    open(os.path.join(RAW, seg_id + ".wav"), "wb").write(get(f"/audio/{gid}"))
    subprocess.run(["ffmpeg", "-y", "-i", os.path.join(RAW, seg_id + ".wav"), fin],
                   check=True, capture_output=True)
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "default=noprint_wrappers=1:nokey=1", fin],
                         capture_output=True, text=True, check=True)
    return fin, round(float(out.stdout.strip()), 3)


manifest = []
for sid, variant, props, text in SEGMENTS:
    path, dur = gen_one(sid, text)
    manifest.append({"id": sid, "variant": variant, "props": props, "wav": path, "duration": dur})
    print(f"  {sid:14s} {dur:6.2f}s", flush=True)

silence = os.path.join(FIN, "_sil.wav")
subprocess.run(["ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=24000:cl=mono", "-t", str(GAP), silence],
               check=True, capture_output=True)
concat_list = os.path.join(ROOT, "concat.txt")
with open(concat_list, "w") as f:
    for i, m in enumerate(manifest):
        f.write(f"file '{m['wav']}'\n")
        if i < len(manifest) - 1:
            f.write(f"file '{silence}'\n")
subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_list, "-c", "copy",
                os.path.join(PUBLIC, "narration.wav")], check=True, capture_output=True)

cuts, t = [], 0.0
for m in manifest:
    start, end = t, t + m["duration"]
    cuts.append({"id": m["id"], "type": m["variant"], "in_seconds": round(start, 3),
                 "out_seconds": round(end, 3),
                 "props": {**m["props"], "dur": round(m["duration"] + GAP, 3)}})
    t = end + GAP
props = {"cuts": cuts,
         "audio": {"narration": {"src": f"{PREFIX}/narration.wav", "volume": 1.0}}}
json.dump(props, open(os.path.join(ROOT, "artifacts", "edit_decisions.json"), "w"), indent=2)
total_narration = sum(m["duration"] for m in manifest)
print(f"total {total_narration:.2f}s narration + {len(SEGMENTS)-1}×{GAP}s gaps = {t:.2f}s ({(t)/60:.2f} min), "
      f"{len(cuts)} scenes, NO captions, NO music")
