#!/usr/bin/env python3
"""GPUs: The Engines of AI — chapter-wise screenplay (4 standalone chapters + master).

Each CHAPTER: id, num, title, and a list of segments (id, variant, props, narration).
Variants route to the `gpu` scene set (composer/src/scenes/GPUScenes.tsx). `dur` is
injected by build.py from measured TTS length, so scenes phase over the whole beat.

Narration rules (skills/02): spoken language, ≤~14-word sentences, [pause] after new
terms / big numbers / key ideas, on-screen numbers mirrored in the audio. All GPU
specs verified 2026-08; serving numbers (tokens/sec, users, racks) are transparently
derived order-of-magnitude estimates, always framed as "about / roughly / ≈".
"""

C = dict(comp="#FBBF24", mem="#22D3EE", ai="#A78BFA", ok="#34D399", nv="#76B900")

CHAPTERS = [
 # ============================================================ CHAPTER 1
 {"id": "ch1-what-are-gpus", "num": 1, "title": "What a GPU Is", "segments": [
   ("s01_title", "gpu_title",
    {"kicker": "A DEEP-DIVE COURSE · CHAPTER 1", "line1": "GPUs:", "line2": "The Engines of AI",
     "sub": "what they are · how they run models · which exist · how many you need", "color": C["mem"]},
    "Nearly every A-I model you have ever used runs on a G-P-U. [pause] Not a mysterious "
    "brain — just a very particular kind of computer chip. [pause] In this course we open "
    "it up, end to end. What a G-P-U actually is. How it runs an A-I model. Which ones the "
    "big companies build. And how many it takes to serve the whole world. [pause] Chapter "
    "one: what is this thing?"),

   ("s02_roadmap", "gpu_roadmap", {},
    "Here is the map. Four chapters. [pause] First, what a G-P-U really is — thousands of "
    "tiny cores acting as one. [pause] Second, how those cores run an A-I model — matrix "
    "math, tensor cores, and tokens. [pause] Third, the landscape — NVIDIA, A-M-D, Google, "
    "Amazon, and the challengers. [pause] And fourth, the question everyone asks — how many "
    "G-P-Us it takes to serve real users, at real speed. [pause] We will build every answer "
    "from the ground up, using only numbers we can check."),

   ("s03_cpuvsgpu", "gpu_cpuvsgpu", {},
    "Start with the chip you already own. [pause] The C-P-U in your laptop has a handful of "
    "big, powerful cores. It is brilliant at doing one complicated thing after another, very "
    "fast. Open a file, run a spreadsheet, load a page — that is a C-P-U. [pause] A G-P-U "
    "makes the opposite bet. Instead of a few strong cores, it packs in thousands of small, "
    "simple ones. [pause] Say you have twenty-four numbers to square. The C-P-U works through "
    "them a few at a time, in order. [pause] The G-P-U hands one number to each core and "
    "squares all twenty-four at once. [pause] Same total work — but finished in a single "
    "step. The C-P-U is a sprinter. The G-P-U is ten thousand runners crossing the line "
    "together."),

   ("s04_parallel", "gpu_parallel", {},
    "That trick has a name — S-I-M-D. Single instruction, multiple data. [pause] One "
    "instruction, broadcast to a whole flood of numbers. [pause] Here the instruction is "
    "simple: take each value, and square it. [pause] On a C-P-U you would loop through the "
    "list, one after another. On a G-P-U, every lane loads its own number, and on the very "
    "same clock tick, all of them multiply together. [pause] Sixteen lanes here, so you can "
    "see them — but a real G-P-U runs tens of thousands of lanes side by side. [pause] This "
    "is the whole idea. Do not make one calculation faster. Do a mountain of them at the "
    "same time. Any job that looks like the same math repeated over huge amounts of data is "
    "a job a G-P-U will devour."),

   ("s05_anatomy", "gpu_anatomy", {},
    "So what is physically on the chip? [pause] In the middle sits a sea of compute — those "
    "thousands of cores, plus special units we will meet in the next chapter called Tensor "
    "Cores. That single slab of silicon holds tens, even hundreds, of billions of "
    "transistors. [pause] Ringing it is memory: tall stacks called H-B-M — high bandwidth "
    "memory — sitting right up against the die. [pause] And wide buses connect the two, "
    "shuttling numbers back and forth constantly. [pause] Here is the sentence to remember "
    "from this whole chapter. The cores are useless if you cannot feed them. [pause] Keeping "
    "that memory full and flowing into the cores is the entire game — and it is where most "
    "of the difficulty, and most of the cost, actually lives."),

   ("s06_bandwidth", "gpu_bandwidth", {},
    "Which brings us to the single most important number on a G-P-U: memory bandwidth. "
    "[pause] It is how fast the chip can read its own memory — measured in bytes per second. "
    "[pause] Your laptop's memory moves maybe eighty gigabytes a second. [pause] An older "
    "A100 data-center G-P-U moves two terabytes a second. An H100, three point three. An "
    "H200, nearly five. [pause] And a Blackwell B200 moves eight terabytes every single "
    "second — roughly a hundred times your laptop. [pause] Hold on to that one word: "
    "bandwidth. In Chapter four it turns out to decide almost everything about how fast, and "
    "how cheaply, A-I can answer you."),

   ("s07_recap", "gpu_recap",
    {"kicker": "CHAPTER 1 · RECAP", "title": "What a GPU is, in one breath", "color": C["comp"],
     "items": [
       "A CPU has a few big cores; a GPU has thousands of small ones",
       "SIMD: one instruction runs across a flood of numbers at once",
       "On the die: a sea of cores, ringed by fast HBM memory",
       "Memory bandwidth — bytes read per second — is the number that matters",
     ], "closer": "A GPU is a machine for doing enormous piles of simple math, all at once."},
    "So, Chapter one in one breath. [pause] A C-P-U has a few big cores; a G-P-U has "
    "thousands of small ones. It runs one instruction across a whole flood of numbers at "
    "once. On the die, a sea of cores wrapped in fast memory. And bandwidth is king. [pause] "
    "That is the machine. Next, we put it to work — and watch it run an actual A-I model."),
 ]},

 # ============================================================ CHAPTER 2
 {"id": "ch2-run-ai-models", "num": 2, "title": "Running AI Models", "segments": [
   ("s01_title", "gpu_title",
    {"kicker": "A DEEP-DIVE COURSE · CHAPTER 2", "line1": "How GPUs", "line2": "Run AI Models",
     "sub": "matrix math · tensor cores · tokens · the memory wall", "color": C["ai"]},
    "You have seen what a G-P-U is. [pause] Now the real question: how does all that parallel "
    "math turn into a chatbot writing you a poem? [pause] The answer is simpler, and "
    "stranger, than you might think. [pause] Underneath the magic, a language model is almost "
    "entirely one single operation — done, over and over, billions of times."),

   ("s02_matmul", "gpu_matmul", {},
    "That one operation is matrix multiply. [pause] A matrix is just a grid of numbers. "
    "Multiply two of them together, and every cell in the answer is one row from the first, "
    "times one column from the second, added up. [pause] Watch a single output cell. Take "
    "this row. Take that column. Multiply them pair by pair, and sum the results. That is "
    "the whole operation. [pause] A model does billions of these tiny multiply-and-add steps "
    "for every single word it produces. [pause] And now remember Chapter one — multiplying "
    "and adding across a grid is exactly what thousands of parallel cores were built to do. "
    "[pause] The model and the chip were made for each other."),

   ("s03_tensorcore", "gpu_tensorcore", {},
    "Ordinary cores multiply two numbers at a time. [pause] But NVIDIA noticed that the "
    "whole job is matrices — so they built a unit that swallows a small matrix in one bite. "
    "That is a Tensor Core. [pause] Feed it a tile of numbers from here, and a tile from "
    "there. In a single fused step it multiplies them and adds the result onto a running "
    "total. D equals A times B, plus C. [pause] Stack thousands of those operations, and you "
    "have computed an entire layer of the network. [pause] On an H100 that is close to a "
    "thousand trillion of these operations every second. [pause] This is why a modern G-P-U "
    "is really an A-I machine — most of its silicon is now dedicated Tensor Cores, not "
    "general-purpose math."),

   ("s04_transformer", "gpu_transformer", {},
    "Now zoom out to the whole model — a transformer. [pause] Your words come in as tokens, "
    "little chunks of text. [pause] First comes attention: every word looks at the other "
    "words to gather context — who did what, to whom. [pause] Then a feed-forward block — "
    "those giant matrix multiplies we just saw — mixes all that information together. "
    "[pause] And out the far end comes exactly one thing: a prediction for the next token. "
    "Here, the word 'on'. [pause] Then the model loops. That brand-new word joins the input, "
    "and the entire stack runs again to produce the word after it. [pause] One full pass "
    "through the network buys you one token. Just one."),

   ("s05_prefill", "gpu_prefill", {},
    "That loop actually hides two very different phases. [pause] Phase one is prefill: the "
    "model reads your entire prompt at once. Every token in parallel, all the cores lit up "
    "and busy. We call that compute-bound — limited by raw math. [pause] Phase two is "
    "decode: now it writes the reply, one token at a time. [pause] And here is the catch. "
    "For every single new word, the G-P-U must read every weight in the model back out of "
    "memory. [pause] So decode is not limited by math at all. It is limited by memory "
    "bandwidth — that word again. [pause] Prefill is a sprint the cores love. Decode is a "
    "slow drip, and the memory bus sets the pace."),

   ("s06_precision", "gpu_precision", {},
    "There is one more lever, and it is a big one — precision. [pause] Every weight in the "
    "model is a number, and you get to choose how many bits to spend storing it. [pause] Old "
    "training used thirty-two bits per number — that is four gigabytes for every billion "
    "parameters. [pause] Then sixteen bits became the workhorse: two gigabytes. [pause] The "
    "H100 generation went down to eight bits — one gigabyte, and twice the speed. [pause] "
    "And Blackwell added four-bit numbers — half a gigabyte per billion, and twice as fast "
    "again. [pause] Fewer bits means less memory to move, and more math per second. Given "
    "everything in Chapter one, you can already feel why that matters so much."),

   ("s07_membound", "gpu_membound", {},
    "Let us make that memory wall completely concrete. [pause] Take a model with seventy "
    "billion parameters, stored in eight-bit. That is seventy gigabytes of weights. [pause] "
    "And decode has to read all seventy of them — once — for every token it writes. [pause] "
    "So the speed limit is just a division: bandwidth, divided by seventy gigabytes. [pause] "
    "On an H100, three point three terabytes a second, over seventy, gives about forty-eight "
    "tokens a second. On an H200, nearly seventy. On a B200, over a hundred. [pause] And that "
    "is for one user, one stream — while the chip is barely breaking a sweat. [pause] Turning "
    "that bored G-P-U into a busy one is the whole subject of Chapter four."),

   ("s08_recap", "gpu_recap",
    {"kicker": "CHAPTER 2 · RECAP", "title": "How a model runs, in one breath", "color": C["ai"],
     "items": [
       "A model is mostly one operation: matrix multiply",
       "Tensor Cores multiply whole tiles in a single fused step",
       "A transformer loops the stack once per token generated",
       "Prefill is compute-bound; decode is memory-bound",
       "Lower precision — FP16 to FP8 to FP4 — means less memory and more speed",
     ], "closer": "Writing one token means re-reading the whole model — the wall everything hits."},
    "Chapter two, in one breath. [pause] A model is mostly matrix multiply. Tensor Cores do "
    "it a tile at a time. A transformer runs the whole stack once per token, in two phases — "
    "a compute-heavy prefill, and a memory-hungry decode. And lower precision buys speed. "
    "[pause] Now we know exactly what the work is. Let us go meet the machines built to do "
    "it."),
 ]},

 # ============================================================ CHAPTER 3
 {"id": "ch3-the-landscape", "num": 3, "title": "The GPU Landscape", "segments": [
   ("s01_title", "gpu_title",
    {"kicker": "A DEEP-DIVE COURSE · CHAPTER 3", "line1": "The GPU", "line2": "Landscape",
     "sub": "NVIDIA · AMD · Google · Amazon · the challengers", "color": C["nv"]},
    "We know what the work is. So who actually makes the hardware to do it? [pause] One "
    "company towers over this entire market — but it is no longer alone. [pause] Let us walk "
    "the landscape, from the chips training today's frontier models, to the challengers "
    "snapping at NVIDIA's heels."),

   ("s02_nvidia", "gpu_nvidia", {},
    "Start with the king: NVIDIA. [pause] Their data-center line marches through three "
    "architectures. [pause] The A100, from twenty-twenty — eighty gigabytes of memory, two "
    "terabytes a second. It trained the first wave of large language models. [pause] The "
    "H100, code-named Hopper, from twenty-twenty-two — same memory, but far faster, and the "
    "chip that powered the ChatG-P-T boom. [pause] The H200 then pushed memory up to a "
    "hundred and forty-one gigabytes. [pause] And the B200, Blackwell — a hundred and "
    "ninety-two gigabytes, eight terabytes a second, built from over two hundred billion "
    "transistors. [pause] Each generation roughly doubles what matters. And still, every "
    "chip is spoken for long before it is even made."),

   ("s03_gb200", "gpu_gb200", {},
    "But the real unit of A-I compute is not one chip any more. It is a rack. [pause] "
    "NVIDIA's G-B-200 N-V-L seventy-two wires seventy-two Blackwell G-P-Us together with "
    "thirty-six Grace C-P-Us, all sharing memory over a fabric called N-V-Link. [pause] To "
    "the model running on it, the whole thing looks like one enormous G-P-U. [pause] The "
    "numbers are staggering. Thirteen terabytes of fast memory. A hundred and thirty "
    "terabytes a second of internal bandwidth. One point four exaFLOPS of A-I compute. "
    "[pause] All in a single cabinet — drawing a hundred and twenty kilowatts, enough to "
    "power dozens of homes. [pause] And data centers now buy these racks by the thousand."),

   ("s04_speccompare", "gpu_speccompare", {},
    "NVIDIA is not the only game, though — especially on memory. [pause] Put the flagships "
    "side by side. [pause] NVIDIA's H100 holds eighty gigabytes; the B200, a hundred and "
    "ninety-two. [pause] A-M-D's Instinct MI300X matched that hundred and ninety-two early. "
    "And their newest, the MI355X, pushes all the way to two hundred and eighty-eight "
    "gigabytes — more memory than anything NVIDIA ships. [pause] Google's T-P-U, their own "
    "custom chip, sits right in the mix. [pause] More memory means you can fit a bigger "
    "model onto fewer chips. So why does NVIDIA still win most of the sales? [pause] Two "
    "words we will come straight back to: software, and networking."),

   ("s05_others", "gpu_others", {},
    "Zoom out to the whole field. [pause] NVIDIA G-P-Us are the default — largely because of "
    "CUDA, the software layer that nearly everyone already builds on. [pause] A-M-D's "
    "Instinct chips lead on raw memory and are catching up fast. [pause] Google skips the "
    "open market entirely and builds T-P-Us for its own data centers, at massive scale. "
    "[pause] Amazon does the same thing with its Trainium chips. [pause] And then the "
    "radicals. Cerebras prints a single chip the size of a dinner plate — an entire wafer, "
    "uncut. And Groq designed a chip that does almost nothing but spit out tokens, at record "
    "speed. [pause] Different bets on the same problem. But CUDA's long head start is why "
    "NVIDIA still sets the pace."),

   ("s06_recap", "gpu_recap",
    {"kicker": "CHAPTER 3 · RECAP", "title": "The landscape, in one breath", "color": C["nv"],
     "items": [
       "NVIDIA leads: A100 to H100 to H200 to B200, doubling each generation",
       "The GB200 NVL72 rack acts as one giant 72-GPU accelerator",
       "AMD leads on memory — the MI355X reaches 288GB",
       "Google TPU and AWS Trainium serve their own clouds at scale",
       "Cerebras and Groq chase radically different chip designs",
     ], "closer": "The hardware race is fierce — but CUDA keeps NVIDIA's lead intact, for now."},
    "Chapter three, in one breath. [pause] NVIDIA leads, roughly doubling each generation, "
    "and now sells compute by the rack. A-M-D leads on memory. Google and Amazon build their "
    "own. And the radicals — Cerebras, Groq — rethink the chip entirely. [pause] Which "
    "leaves the one question everyone actually asks. How many of these do you need?"),
 ]},

 # ============================================================ CHAPTER 4
 {"id": "ch4-sizing-compute", "num": 4, "title": "Sizing the Compute", "segments": [
   ("s01_title", "gpu_title",
    {"kicker": "A DEEP-DIVE COURSE · CHAPTER 4", "line1": "Sizing the", "line2": "Compute",
     "sub": "tokens/sec · throughput · latency · users · racks", "color": C["ok"]},
    "Final chapter — the one everyone really wants answered. [pause] How many G-P-Us does it "
    "take to serve real users? How many tokens a second can they generate? How many people "
    "at once? [pause] And what do throughput and latency actually mean? [pause] We will build "
    "the whole answer from the ground up, using only numbers we have already met. No "
    "hand-waving."),

   ("s02_batching", "gpu_batching", {},
    "Remember the wall from Chapter two. One user, on an H100, got about forty-eight tokens "
    "a second — and the chip was bored stiff. [pause] Here is the fix. It is called "
    "batching. [pause] The G-P-U reads the model's weights once per step. Whether there is "
    "one prompt riding along, or a hundred, it is the exact same read. [pause] So you stack "
    "the prompts together. [pause] With a batch of eight, you get roughly three hundred and "
    "sixty tokens a second. Batch of thirty-two, about twelve hundred. Batch of a hundred "
    "and twenty-eight, over two thousand five hundred — all from that same single chip. "
    "[pause] Same weights, same bandwidth. We just stopped wasting them. This is why real "
    "serving systems always batch."),

   ("s03_tradeoff", "gpu_tradeoff", {},
    "But batching is not free — and this is the trade-off at the very heart of A-I serving. "
    "[pause] Two numbers pull against each other. [pause] Throughput: the total tokens per "
    "second, across everybody. Make the batch bigger, and it climbs — then flattens out as "
    "the chip fills up. [pause] Latency: how long any one user waits between words. Make the "
    "batch bigger, and each person's turn comes around a little slower. [pause] So total "
    "throughput goes up, while individual responsiveness goes down. [pause] There is no free "
    "lunch here — only a dial. Want cheap tokens? Use big batches. Want a snappy, instant "
    "chatbot? Smaller ones. [pause] Every A-I company is quietly choosing its own point on "
    "this curve."),

   ("s04_users", "gpu_users", {},
    "So how many people is that, really? [pause] It is simple division. [pause] Say a "
    "well-batched G-P-U puts out around two thousand six hundred tokens a second. [pause] A "
    "person reads comfortably at maybe ten to fifteen tokens a second — so let us give each "
    "active user twenty, a little faster than they can read. [pause] Two thousand six "
    "hundred, divided by twenty, is about a hundred and thirty people — all chatting live, "
    "on one chip. [pause] And here is the kicker: most of the time, users are reading, not "
    "typing. So in practice, one G-P-U quietly serves many times that number by sharing all "
    "those idle moments."),

   ("s05_cluster", "gpu_cluster", {},
    "Now let us scale it up to a real product. [pause] Suppose you want to serve one million "
    "people, all at the same moment. [pause] Divide by roughly a hundred and thirty live "
    "streams per G-P-U, and you need about seven thousand seven hundred G-P-Us — just for "
    "inference, before any backup capacity. [pause] Package those into G-B-200 racks, "
    "seventy-two G-P-Us each, and that is around a hundred and seven racks. [pause] Just one "
    "row of a large data center. [pause] And now you understand the headlines. Why A-I labs "
    "raise billions of dollars. Why power and cooling are the real bottleneck. And why "
    "NVIDIA sells every single chip it can make."),

   ("s06_recap", "gpu_recap",
    {"kicker": "CHAPTER 4 · RECAP", "title": "Sizing the compute, in one breath", "color": C["ok"],
     "items": [
       "One stream is memory-bound: about 48 tok/s for a 70B model on an H100",
       "Batching amortizes weight reads — one GPU reaches ~2,600 tok/s",
       "Throughput versus latency is a dial you tune, not a free win",
       "At ~20 tok/s per active user, that is ~130 live users per GPU",
       "A million concurrent users is roughly 7,700 GPUs — about 107 racks",
     ], "closer": "AI runs on arithmetic you can now do yourself: bandwidth, batching, and a lot of racks."},
    "Chapter four, in one breath. [pause] One user barely troubles a G-P-U. Batching fills "
    "it — thousands of tokens a second. Throughput versus latency is a dial you choose. That "
    "is about a hundred and thirty live users per chip, so a million users needs roughly a "
    "hundred racks. [pause] And that is the whole course. [pause] G-P-Us are parallel math "
    "engines — and A-I is simply one very large pile of parallel math. [pause] Thanks for "
    "watching."),
 ]},
]
