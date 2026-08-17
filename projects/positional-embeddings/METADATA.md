# Positional Embeddings, From First Principles — YouTube metadata

## Title
Positional Embeddings Explained From First Principles (Sinusoids → RoPE, the ADEPT way)

## Description
Transformers read every word at once — which makes them fast, but blind to word order.
"Dog bites man" and "man bites dog" look identical to self-attention. Positional
embeddings are how we put order back. This video builds the whole idea from scratch.

It's taught with the ADEPT method — shown right on screen — where every concept moves
through Analogy → Diagram → Example → Plain-English → Technical term, plus the Feynman
technique (everyday words first, jargon last):

• Attention is order-blind — a bag of Scrabble tiles on a table (permutation-equivariance)
• The fix — stamp each word with its position, ADDED onto the token vector (house numbers)
• Why naive tags fail — raw index explodes; 0…1 rescaling changes with sentence length
• Sinusoidal encoding — clock hands at many speeds give every position a unique fingerprint
• The famous heatmap — the real sinusoidal PE matrix (rows = positions, cols = sin/cos dims)
• Add it in — "dog bites man" finally differs from "man bites dog"
• Learned positional embeddings (BERT/GPT) — flexible but capped at the trained length
• Relative position — encode the gap between words (i − j), not the absolute seat
• RoPE (Rotary) — rotate each vector by its position so only the relative angle survives;
  the modern default in Llama, GPT-NeoX and Qwen

Every visual computes the real thing: the sinusoidal matrix, the individual sinusoids,
and RoPE's rotation + dot product are all computed, not drawn.

## Tags
positional embeddings, positional encoding, transformers, attention, self-attention,
sinusoidal encoding, RoPE, rotary position embedding, LLM, deep learning, machine learning,
BERT, GPT, Llama, ADEPT method, Feynman technique, AI explained, neural networks

## Notes (production)
- Voice: en-IN-PrabhatNeural (+6%). Identity "Position & Sequence" (indigo/tech).
- VISIBLE ADEPT rail motif (`AdeptRail`) + 5-line stage ledger on every teaching scene;
  universal `SceneProgress` bar. Prefix `pe`, scenes in `composer/src/scenes/PEScenes.tsx`.
- Runtime ~11.7 min, 14 scenes, 1530 words. Computed: sinusoidal PE matrix (PixGrid heatmap),
  sinusoids, RoPE rotation/dot-product.
