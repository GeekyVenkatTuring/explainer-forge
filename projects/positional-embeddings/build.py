#!/usr/bin/env python3
"""Positional Embeddings, From First Principles — ADEPT (visible rail) + Feynman.
~12 min, 13 scenes, prefix `pe`, Prabhat Neural voice (en-IN-PrabhatNeural).

The teaching method is ON SCREEN: every teaching beat's narration walks the five
ADEPT stages in order — Analogy → Diagram → Example → Plain-English → Technical —
so the on-screen A-D-E-P-T rail and the 5-line ledger light up in sync. The [pause]
markers sit at the stage boundaries. Feynman: everyday words, intuition first,
jargon last. Usage: python3 build.py

Budget: Prabhat +6% ≈ 129 wpm effective (with [pause] + gaps) → ~1,550 words ≈ 12 min.
build.py prints the real total — iterate to ±5%.

Content is standard ML (no market/finance figures); the technical claims are the
textbook facts of positional encoding: sinusoidal PE (Vaswani et al. 2017), learned
absolute PE (BERT/GPT), relative PE (Shaw/T5), and RoPE (Su et al.; used in Llama,
GPT-NeoX, Qwen). All visuals compute the real thing in PEScenes.tsx.
"""
import json, os, subprocess, time

VOICE = "en-IN-PrabhatNeural"; RATE = "+6%"; GAP = 0.5; PAUSE = 0.55; PREFIX = "pe"
ROOT = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(ROOT, "..", ".."))
PUBLIC = os.path.join(REPO, "composer", "public", PREFIX)
RAW = os.path.join(ROOT, "assets", "raw")
FIN = os.path.join(ROOT, "assets")
QA_DIR = os.path.join(ROOT, "renders", "qa")
for d in (PUBLIC, RAW, os.path.join(ROOT, "artifacts"), os.path.join(ROOT, "renders"), QA_DIR):
    os.makedirs(d, exist_ok=True)

WAV = "#38BDF8"; TOK = "#A78BFA"  # divider colours (match PEScenes accents)

SEGMENTS = [

 ("s01_title", "pe_title", {},
  "A promise before we start. Every idea here, I'll explain with something you already know, "
  "using a method called ADEPT — analogy, diagram, example, plain words, then the technical term. [pause] "
  "Today's topic: positional embeddings. How a transformer knows the ORDER of your words. [pause] "
  "We'll build it from scratch — the problem, the classic sinusoid trick, and RoPE, the modern default."),

 ("s02_hook", "pe_hook", {},
  "Here's a puzzle. Dog bites man. Now flip it: man bites dog. [pause] "
  "Same three words. Completely different meaning — and in one case, a much worse day. [pause] "
  "Word order carries the meaning. [pause] "
  "But here's the strange part. A transformer's attention, all by itself, cannot see order at all. "
  "To it, both sentences look identical. [pause] "
  "Older networks, like RNNs, read one word at a time, so the order came for free. "
  "Transformers threw that away for speed — they look at every word at once — and lost order with it. [pause] "
  "So how do we teach a model where each word sits, without giving up that speed? "
  "That's what positional embeddings do. Let's build the idea, step by step."),

 ("s03_div1", "pe_div",
  {"n": 1, "title": "Why Order Matters", "sub": "Attention is blind to it — and the classic fix", "color": WAV},
  "Part one. Why attention is blind to order — and the classic fix that quietly powers the original Transformer."),

 ("s04_orderblind", "pe_orderblind", {},
  "First, why is attention order-blind? [pause] "
  "Think of a bag of Scrabble tiles tipped onto a table. You can see every letter, "
  "but nothing tells you the order they came in. [pause] "
  "Here's the picture. Unlike reading left to right, a transformer looks at all the words "
  "at the same time, in parallel. That parallelism is why transformers are so fast to train. [pause] "
  "So try shuffling the words on the table. Every attention score you compute comes out exactly the same. "
  "The math only asks how much each word relates to each other word — never where they sit. [pause] "
  "In plain terms, attention treats your sentence as a set, not a sequence. Order simply isn't in the math. [pause] "
  "The technical name for this is permutation-equivariance — self-attention, on its own, carries zero positional information."),

 ("s05_tag", "pe_tag", {},
  "So we need to add position ourselves. [pause] "
  "Think of house numbers on a street. Every spot gets its own address, so you always know where you are. [pause] "
  "The plan: build a position vector for each slot — zero, one, two, and so on. [pause] "
  "Take the word cat at position one. We add cat's meaning vector to the position-one vector, "
  "and get a position-aware cat. The same word in a different slot becomes a slightly different vector. [pause] "
  "In plain words, we stamp a little where-I-am signal onto every word before attention ever sees it. [pause] "
  "That stamp is the positional embedding. And crucially, it's added to the token embedding, not glued on beside it — "
  "same size, no extra slots, and the model learns to pull meaning and position back apart when it needs to."),

 ("s06_naive", "pe_naive", {},
  "But what should that position vector be? Two obvious ideas — and both break. [pause] "
  "Idea one: just number the words, zero, one, two. It's like shouting a bigger number at each step. [pause] "
  "By word five hundred, the tag IS five hundred — a giant value that drowns out the word's actual meaning. [pause] "
  "Idea two: squeeze positions into zero to one. But then the step size depends on length — "
  "a five-word sentence steps by a quarter, a fifty-word one by a fiftieth. Position five keeps shifting. [pause] "
  "We really want position five to mean the same thing in a short sentence or a long one. "
  "And we'd like nearby positions to feel similar, so the model can sense small shifts. [pause] "
  "So our wish list has four items: the values stay bounded, every position is unique, "
  "the distance between positions is consistent, and it should extrapolate to lengths never seen in training."),

 ("s07_sinusoid", "pe_sinusoid", {},
  "Here's the clever fix — sine waves. [pause] "
  "Think of a clock. A fast seconds hand plus a slow hours hand together pin down one unique moment. [pause] "
  "We do the same with position. Stack many sine waves, each running at a different speed — "
  "a different frequency. [pause] "
  "The fast waves tell nearby positions apart; the slow waves separate the far-apart ones. [pause] "
  "Put together, these waves give every position its own smooth fingerprint. "
  "And here's the elegant part: each dimension comes as a sine and cosine pair, "
  "so moving forward by a few steps is just a small rotation — which means the model can express "
  "relative positions as a simple, linear operation. [pause] "
  "The formula: position over ten-thousand to the power i-over-d, fed through sine and cosine — "
  "wavelengths that grow geometrically from short to very long. And notice: it's bounded, unique, consistent, and extends forever."),

 ("s08_heatmap", "pe_heatmap", {},
  "Let's look at all those fingerprints at once. This is the famous picture — think of a sheet of barcodes. [pause] "
  "Each row is one position; each column is one sine or cosine dimension. [pause] "
  "Read straight across a single row — that's the exact vector we add to the word in that slot. [pause] "
  "Look at the columns on the left: they flip quickly, position to position. "
  "The columns on the right barely change — those are the slow hands. "
  "And neighbouring rows look alike, while far-apart rows look clearly different. [pause] "
  "This is the sinusoidal positional-encoding matrix — and from it, the model can recover "
  "how far apart any two words are, just by comparing their stripes."),

 ("s09_added", "pe_added", {},
  "So how is it actually used? Think of slapping a timestamp sticker on each word before the model reads it. [pause] "
  "For every word, we take its token vector and add its position vector — "
  "giving a position-aware input to attention. [pause] "
  "Now run our puzzle again. Dog bites man, and man bites dog, finally produce different attention, "
  "because 'dog at position zero' and 'dog at position two' are now different inputs. [pause] "
  "In plain words, the model can now use order to work out who bit whom. [pause] "
  "And that's the whole trick — the encoding is added once at the input, and the network learns to read it. "
  "Funnily enough, the fixed sinusoid and a fully learned table end up performing about the same."),

 ("s10_div2", "pe_div",
  {"n": 2, "title": "Modern Upgrades", "sub": "Learned · Relative · RoPE", "color": TOK},
  "Part two. Three modern upgrades — learned embeddings, relative position, "
  "and the one most new models actually use."),

 ("s11_learned", "pe_learned", {},
  "The sinusoid is a formula. But there's an even simpler cousin. [pause] "
  "Instead of a formula, just memorise each seat's label. [pause] "
  "You keep a lookup table: one trainable vector per position, from zero up to some maximum. [pause] "
  "This is exactly what BERT and the original GPT do — positions are just parameters the model learns, "
  "one row for each slot up to the context length, say five hundred and twelve. [pause] "
  "It's flexible, and it can shape itself to the data — but it only knows the positions it saw during training. "
  "Feed it a longer input than it ever trained on, and there's simply no row to look up. [pause] "
  "This is learned absolute positional embedding. The catch: no free extrapolation past the maximum "
  "length. Sinusoids stretch forever; learned tables are capped."),

 ("s12_relative", "pe_relative", {},
  "Now a better question. At a dinner table, you don't care about your absolute seat number. "
  "You care that someone is three seats to your left. [pause] "
  "So instead of absolute spots, encode the gap between two words — position i minus position j. [pause] "
  "Cat and mat are three apart. That stays true whether the phrase starts at word one or word one hundred. [pause] "
  "The same pattern, anywhere in the sentence, gets treated the same way — which helps the model "
  "generalise to sentences longer than it trained on. [pause] "
  "These are relative position encodings, first used in models like T5 — and they set up the modern favourite, RoPE."),

 ("s13_rope", "pe_rope", {},
  "RoPE does something beautiful. Think of two dancers spinning — what matters is the angle between them. [pause] "
  "For each word, we take its query and key vectors, split them into pairs of numbers, "
  "and rotate each pair by an angle set by the position — using those same many frequencies as before. "
  "Word two turns a little; word six turns more. [pause] "
  "Now compare two words. When you take their dot product, the absolute spin cancels out — "
  "what's left depends only on the gap, m minus n. Relative position falls out of the math, for free. [pause] "
  "In plain words, each word spins by where it sits, but only their relative angle survives the comparison. [pause] "
  "This is Rotary Position Embedding — RoPE — used in Llama, GPT-NeoX, and Qwen. "
  "It gives relative position, baked right into attention, and it stretches gracefully to very long contexts."),

 ("s14_recap", "pe_recap",
  {"items": [
   "Attention is order-blind — on its own it sees a SET of tokens, not a sequence",
   "Fix: add a position vector onto each token embedding (same size, no extra slots)",
   "Naive tags fail — a raw index explodes; 0…1 rescaling changes with length",
   "Sinusoids = clock hands at many speeds → a unique, bounded fingerprint per position",
   "The striped heatmap IS that matrix; similar rows mean nearby positions",
   "Added in, 'dog bites man' finally differs from 'man bites dog'",
   "Learned PE: simple but capped. Relative PE: encodes the gap i − j",
   "RoPE rotates q and k so only the relative angle survives — the modern default (Llama)",
  ],
   "closer": "Position isn't in attention by default — putting it back is what lets transformers read language at all."},
  "Let's put the whole story in one breath. [pause] "
  "Attention is order-blind — on its own it sees a bag of tiles, not a sequence. [pause] "
  "So we stamp each word with its position, added right onto the token vector. [pause] "
  "Numbering the words, or squeezing them into zero-to-one, both break — so we use sine waves at many "
  "speeds, like clock hands, giving every position a unique fingerprint. "
  "That's the sinusoidal encoding, and its famous striped heatmap. [pause] "
  "Add it in, and dog bites man finally differs from man bites dog. [pause] "
  "Learned tables are simpler but can't extrapolate. Relative encodings track the gap between words. "
  "And RoPE rotates each vector so only the relative angle matters — the modern default. [pause] "
  "Position isn't in attention by default. Everything good about transformers on language depends on "
  "putting it back. Thanks for watching."),
]

# ──────────────────────────── TTS engine (edge-tts)
def ffdur(path):
    out = subprocess.run(
        ["ffprobe","-v","error","-show_entries","format=duration",
         "-of","default=noprint_wrappers=1:nokey=1",path],
        capture_output=True, text=True, check=True)
    return round(float(out.stdout.strip()), 3)

def tts_chunk(path, text):
    mp3 = path[:-4] + ".mp3"
    for attempt in range(6):
        r = subprocess.run(
            ["edge-tts","--voice",VOICE,f"--rate={RATE}","--text",text,"--write-media",mp3],
            capture_output=True)
        if r.returncode == 0 and os.path.exists(mp3) and os.path.getsize(mp3) > 0:
            break
        time.sleep(3 + attempt * 4)
    else:
        raise RuntimeError(f"tts failed after 6 attempts: {path}")
    subprocess.run(["ffmpeg","-y","-i",mp3,"-ar","24000","-ac","1",path],
                   check=True, capture_output=True)
    os.remove(mp3)

def gen_one(seg_id, text):
    fin = os.path.join(FIN, seg_id + ".wav")
    if os.path.exists(fin):
        return fin, ffdur(fin)
    chunks = [c.strip() for c in text.split("[pause]") if c.strip()]
    paths = []
    for ci, chunk in enumerate(chunks):
        cp = os.path.join(RAW, f"{seg_id}_c{ci}.wav")
        if not os.path.exists(cp):
            tts_chunk(cp, chunk)
        paths.append(cp)
    psil = os.path.join(RAW, "_pause.wav")
    if not os.path.exists(psil):
        subprocess.run(["ffmpeg","-y","-f","lavfi","-i","anullsrc=r=24000:cl=mono",
                        "-t",str(PAUSE), psil], check=True, capture_output=True)
    clist = os.path.join(RAW, f"{seg_id}_concat.txt")
    with open(clist, "w") as f:
        for i2, p2 in enumerate(paths):
            f.write(f"file '{p2}'\n")
            if i2 < len(paths) - 1:
                f.write(f"file '{psil}'\n")
    subprocess.run(["ffmpeg","-y","-f","concat","-safe","0","-i",clist,"-c","copy",fin],
                   check=True, capture_output=True)
    return fin, ffdur(fin)

# ──────────────────────────── main build
manifest = []
for sid, variant, props, text in SEGMENTS:
    path, dur = gen_one(sid, text)
    manifest.append({"id": sid, "variant": variant, "props": props, "wav": path, "duration": dur})
    print(f"  {sid:18s} {dur:6.2f}s", flush=True)

silence = os.path.join(FIN, "_sil.wav")
subprocess.run(["ffmpeg","-y","-f","lavfi","-i","anullsrc=r=24000:cl=mono","-t",str(GAP),silence],
               check=True, capture_output=True)

concat_list = os.path.join(ROOT, "concat_pe.txt")
with open(concat_list, "w") as f:
    for i, m in enumerate(manifest):
        f.write(f"file '{m['wav']}'\n")
        if i < len(manifest) - 1:
            f.write(f"file '{silence}'\n")

subprocess.run(["ffmpeg","-y","-f","concat","-safe","0","-i",concat_list,"-c","copy",
                os.path.join(PUBLIC, "narration.wav")], check=True, capture_output=True)

cuts, t = [], 0.0
for m in manifest:
    start, end = t, t + m["duration"]
    cuts.append({
        "id": m["id"], "type": m["variant"],
        "in_seconds": round(start, 3), "out_seconds": round(end, 3),
        "props": {**m["props"], "dur": round(m["duration"] + GAP, 3)},
    })
    t = end + GAP

props_out = {
    "cuts": cuts,
    "audio": {"narration": {"src": f"{PREFIX}/narration.wav", "volume": 1.0}},
}
json.dump(props_out, open(os.path.join(ROOT, "artifacts", "edit_decisions.json"), "w"), indent=2)
total = t - GAP
words = sum(len(text.replace("[pause]", " ").split()) for _, _, _, text in SEGMENTS)
print(f"\ntotal {total:.2f}s ({total/60:.2f} min) · {len(cuts)} scenes · {words} words · NO captions · NO music")
print("Next: QA stills for every scene, LOOK at each, fix, then final render.")
