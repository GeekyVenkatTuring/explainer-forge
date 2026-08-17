# -*- coding: utf-8 -*-
"""Information Theory From Scratch — screenplay.

Each chapter renders to its own MP4; all chapters concat into the master.
A chapter is a list of scene segments: {id, variant, props, narration}.
Narration is SPOKEN language (numbers as words), with [pause] markers (0.6s) after
new terms / big numbers / key ideas. Every on-screen element is mentioned in its
beat, phased to roughly when it is said. See skills/02 + skills/09.

Semantic colors (ITScenes.A):
  BIT=#22D3EE (bits/signal) · SURP=#FBBF24 (surprise/probability) ·
  ENT=#A78BFA (entropy/uncertainty) · CODE=#34D399 (codes/compression) ·
  NOISE=#F472B6 (noise/error)

~21 chapters · 6 parts · target ~68-72 min at ~145-155 effective wpm.
"""

BIT, SURP, ENT, CODE, NOISE = "#22D3EE", "#FBBF24", "#A78BFA", "#34D399", "#F472B6"


CHAPTERS = [
    # ================================================================= INTRO
    {"id": "it-ch01-big-picture", "title": "The Big Picture", "segments": [
        {"id": "title", "variant": "it_title", "props": {}, "narration":
            "Here is a question that sounds impossible to answer. [pause] How do you measure "
            "information? [pause] Not whether a message is true. Not what it means. Just how "
            "much information is in it — as an honest number, the way we measure length or weight. "
            "[pause] In nineteen forty-eight, a quiet engineer named Claude Shannon answered that "
            "question, in a single paper — and in doing so, he invented the digital world. [pause] "
            "Over this course, we are going to rebuild his answer from nothing."},
        {"id": "roadmap", "variant": "it_roadmap", "props": {}, "narration":
            "So here is the journey ahead of us. [pause] We will start at the very bottom, with a "
            "single surprising event, and turn it into a precise number of bits. [pause] From "
            "there, entropy — the true, irreducible size of a message. [pause] Then compression, "
            "and the hard wall on how small things can ever shrink. [pause] Then we will learn to "
            "compare beliefs — cross-entropy, divergence, and mutual information, the tools that "
            "now train artificial intelligence. [pause] Then the noisy channel, and Shannon's "
            "almost unbelievable promise: perfect communication through an imperfect, crackling "
            "wire. [pause] And finally, the big picture — how this one idea reaches from your "
            "phone, to your genes, to the edge of physics itself. [pause] There is no mathematics "
            "here we will not build together, brick by brick. So let's begin, at the very "
            "beginning — with surprise."},
        {"id": "hook", "variant": "it_hook", "props": {}, "narration":
            "Let me show you the entire idea in just two sentences. [pause] Here is the first "
            "one. The sun rose this morning. [pause] Is that informative? Not really. You already "
            "knew it would. It was practically certain — so hearing it tells you almost nothing "
            "new. [pause] Now the second sentence. It snowed, today, in the Sahara desert. "
            "[pause] That one stops you cold. It is rare. It is unexpected. It is surprising — and "
            "suddenly you have learned a great deal. [pause] Look at the two. Same length. Same "
            "grammar. Both perfectly ordinary English. Yet they carry wildly different amounts of "
            "information. [pause] So what is the difference? It is not the words. It is not the "
            "meaning. It is how likely each message was. [pause] And here is Shannon's great "
            "reversal, the hinge the whole field swings on. [pause] Information is not about "
            "meaning at all. It is about surprise. [pause] The less likely a message, the more "
            "information it delivers. The more predictable, the less. A message you could have "
            "guessed carries nothing. [pause] That single flip — measuring surprise instead of "
            "meaning — is the seed of everything ahead. [pause] So our very first job is to take "
            "that soft, fuzzy word, surprise, and forge it into a hard number. And, remarkably, "
            "there turns out to be only one sensible way to do it."},
        {"id": "system", "variant": "it_system", "props": {}, "narration":
            "So how did Shannon actually attack a problem this slippery? He did what every great "
            "scientist does — he drew a picture. [pause] And this one diagram, from his nineteen "
            "forty-eight paper, quietly organizes the entire digital world. [pause] On the far "
            "left sits the source — whatever is producing a message. Your voice. A file. A photo. "
            "A sensor reading. [pause] The message enters an encoder — sometimes called the "
            "transmitter — which turns it into a signal, a stream of bits ready to travel. "
            "[pause] That signal crosses the channel — the wire, the air, the fibre, the "
            "magnetic disk. Anything that carries information across space, or across time. "
            "[pause] At the far end, a decoder reads the incoming signal and reconstructs the "
            "message. And finally it arrives at the destination — the person, or machine, that "
            "needed it. [pause] Source, encoder, channel, decoder, destination. Five boxes. "
            "[pause] But there is a sixth thing, and it is the villain of our whole story. Noise. "
            "[pause] Noise creeps into the channel from the side — static, interference, a "
            "scratch, a stray cosmic ray — corrupting the signal in transit. [pause] Here is the "
            "genius of the diagram. It deliberately throws the meaning away. Shannon does not "
            "care whether you are sending a love letter or a stock price. [pause] By separating "
            "the meaning from the medium, he turned a vague human problem — communication — into "
            "something sharp and mathematical. [pause] Every idea in this course lives somewhere "
            "on this map. Compression makes the encoder lean. Error-correcting codes fight the "
            "noise. Capacity measures what the channel can bear. [pause] And notice something "
            "subtle. The same diagram describes storage as well as transmission. Saving a file to "
            "a disk today, and reading it back tomorrow, is just sending a message through time "
            "instead of space — with the same noise, and the same defences. [pause] Keep this "
            "picture in the back of your mind. Everything we build from here plugs into one of "
            "these boxes."},
    ]},

    # ================================================= PART 1 — MEASURING INFORMATION
    {"id": "it-ch02-surprise", "title": "Information Is Surprise", "segments": [
        {"id": "div", "variant": "it_divider",
         "props": {"n": 1, "title": "Measuring Information", "sub": "turning surprise into a number of bits", "color": SURP},
         "narration":
            "Part one. Measuring information. [pause] Before entropy, before compression, before "
            "channels, we need the atom of the whole theory — the information carried by a single "
            "event. Let's build that atom, from the ground up."},
        {"id": "surprise", "variant": "it_surprise", "props": {}, "narration":
            "Let's line up a few events by how surprising they are, and look for a pattern. "
            "[pause] A coin lands heads. The probability is one in two. Barely a surprise at all. "
            "[pause] A single die rolls a six. One chance in six. A little more surprising. "
            "[pause] Now snake eyes — two ones on a pair of dice at once. One chance in "
            "thirty-six. Rarer still, and more surprising. [pause] And the ace of spades, drawn "
            "first from a freshly shuffled deck. One in fifty-two. [pause] Watch the bars grow. "
            "As the probability shrinks, the surprise climbs. So whatever information is, it must "
            "be some function of one over p — of how rare the event was. [pause] But which "
            "function, exactly? Here is the clean, and it turns out only, choice. We measure the "
            "surprise as the logarithm, base two, of one over p. [pause] Why base two? Because it "
            "measures the answer in bits — in yes-or-no questions, as we will see in a moment. "
            "[pause] Let's sanity-check it. An event with probability one half gives the log of "
            "two, which is exactly one bit. One in four gives two bits. One in eight, three bits. "
            "[pause] Notice the rhythm. Every time the odds get twice as long, the surprise goes "
            "up by exactly one bit. Halve the probability, add a bit. [pause] That simple, "
            "steady rule — surprise equals log of one over p — is the single foundation the "
            "entire field is built on. Everything else grows from it."},
    ]},

    {"id": "it-ch03-self-information", "title": "Why a Logarithm", "segments": [
        {"id": "selfinfo", "variant": "it_selfinfo", "props": {}, "narration":
            "But hold on — why the logarithm, exactly? Why not just use one over p directly as "
            "our measure of surprise? [pause] The reason is genuinely beautiful, and it comes "
            "from one simple thing we demand of information. [pause] Flip a fair coin and it lands "
            "heads. That is one bit of surprise. [pause] Now flip it again, completely "
            "independently, and it lands heads once more. Another one bit. [pause] Here is the "
            "question. How surprising is it to get both heads together, as a single joint event? "
            "[pause] Your intuition is firm about this. It should be two bits. One plus one. The "
            "surprises of independent events ought to simply add up. That feels non-negotiable. "
            "[pause] But now look at the probabilities. Each flip has probability one half, and "
            "independent probabilities do not add — they multiply. One half times one half is one "
            "quarter. [pause] So we are asking for a function with a very specific magic property. "
            "When the inputs multiply, the outputs must add. [pause] And there is exactly one "
            "family of functions on Earth that turns multiplication into addition. The logarithm. "
            "[pause] Check it. The probability of both heads is one quarter. The log, base two, "
            "of one over one quarter, is the log of four, which is two. Two bits. It adds up, "
            "perfectly. [pause] So the logarithm is not a clever choice we reached for. It is "
            "forced on us. We insisted that independent surprises add together — and that one "
            "demand leaves the logarithm as the only possibility. [pause] This is a theme you "
            "will see again and again in Shannon's work. He does not pick formulas. He states "
            "what a good measure must do, and the mathematics hands him the only answer."},
    ]},

    {"id": "it-ch04-the-bit", "title": "The Bit", "segments": [
        {"id": "bit", "variant": "it_bit", "props": {}, "narration":
            "We keep saying the word bit. Let's pin down what a bit actually is. [pause] Forget "
            "transistors and hardware for a minute. At its core, a bit is one perfect yes-or-no "
            "question — the answer that splits your uncertainty exactly in half. [pause] Let me "
            "show you with a game. I am thinking of a number from one to sixty-four, and you have "
            "to find it. [pause] You could guess one at a time. Is it one? Is it two? Slow, and up "
            "to sixty-four tries in the worst case. [pause] Or you could be clever. Ask: is it in "
            "the top half — thirty-three or above? Whatever I answer, you have just eliminated "
            "half of all the possibilities in a single question. [pause] Ask again, about the "
            "half that remains. Sixty-four candidates become thirty-two. [pause] Then sixteen. "
            "Then eight, four, two, and finally one. Watch the field of squares collapse each "
            "time. [pause] Now count the questions it took. Just six of them pinned down one "
            "option out of sixty-four. [pause] And six is precisely the logarithm, base two, of "
            "sixty-four. There is that log again. [pause] So this is what a bit really is. It is "
            "the information in one ideal question — the answer that cuts your uncertainty cleanly "
            "in half. [pause] And it ties straight back to surprise. An outcome with probability "
            "one in sixty-four carries six bits of surprise, and it takes six perfect questions "
            "to resolve. The two ideas are the same idea. [pause] Everything digital — every file, "
            "every message, every image — is, at bottom, a pile of these halving answers stacked "
            "on top of one another."},
        {"id": "encode", "variant": "it_encode", "props": {}, "narration":
            "Now let's put bits to work and actually encode something, because this is where the "
            "theory starts paying off. [pause] Suppose our messages are built from just four "
            "symbols — A, B, C, and D. [pause] The obvious scheme gives each symbol its own "
            "two-bit codeword. A is zero-zero. B is zero-one. C is one-zero. D is one-one. Four "
            "symbols, two bits each, always. Simple and clear. [pause] But now suppose the symbols "
            "are not equally common. Suppose A shows up half the time, B a quarter of the time, "
            "and C and D just one-eighth each. [pause] Then spending two whole bits on A, the most "
            "frequent symbol, starts to feel wasteful. We pay the same for the common and the "
            "rare. [pause] So let's be smarter about it. Give the common A a single short bit — "
            "just zero. And give the rarer symbols longer codes to make up for it. [pause] Now "
            "compute the average length across a typical message. Half the time we send one bit. "
            "A quarter of the time, two bits. And the last quarter, three bits. [pause] Add it up, "
            "weighted by frequency, and it comes to one point seven five bits per symbol — instead "
            "of a flat two. [pause] Same messages. Same information. Twelve percent shorter, with "
            "absolutely nothing lost. [pause] And there is the golden rule of coding in one line: "
            "spend few bits on common things, and more bits on rare things. [pause] But this opens "
            "the real question — the one that drives the middle of this course. How short can we "
            "possibly go? Is there a hard limit? [pause] There is. And its name is entropy."},
    ]},

    # ================================================================= PART 2 — ENTROPY
    {"id": "it-ch05-entropy", "title": "Entropy", "segments": [
        {"id": "div", "variant": "it_divider",
         "props": {"n": 2, "title": "Entropy", "sub": "the average surprise of a source", "color": ENT},
         "narration":
            "Part two. Entropy. [pause] We now know how to measure the surprise of one single "
            "event. But real sources — a language, a sensor, a coin flipped forever — produce "
            "event after event. So we ask the deeper question: how uncertain is a whole source, "
            "on average? [pause] That average has a name, and it will run the rest of this course."},
        {"id": "entropy", "variant": "it_entropy", "props": {}, "narration":
            "Meet entropy — the single most important quantity in all of information theory. "
            "[pause] The definition is simpler than its fearsome reputation. Entropy is just the "
            "average surprise of a source. If you watched it produce outcomes forever, how many "
            "bits would each one cost you, on average? [pause] Let's build the intuition with a "
            "coin whose bias we can dial. On this curve, the horizontal axis is the probability "
            "of heads, and the height of the curve is the entropy, in bits. [pause] Start at the "
            "far left. A coin that always lands tails. There is no surprise here at all — you knew "
            "the result before you flipped. Entropy: zero bits. [pause] Same story at the far "
            "right. A coin that always lands heads. Utterly predictable. Also zero. [pause] Now "
            "slide toward the middle, watch the dot climb, and reach a perfectly fair, "
            "fifty-fifty coin. Here the entropy peaks — at exactly one full bit. [pause] And "
            "there is the core intuition of the whole idea. Uncertainty is highest when the "
            "outcomes are balanced, and it falls away the moment the source becomes lopsided and "
            "predictable. [pause] Notice what entropy is really about. It is not about any single "
            "flip. It is the expected surprise, a property baked into the source itself, before "
            "you ever look at an outcome. [pause] Entropy measures your ignorance about what the "
            "source will do next — measured, precisely, in bits."},
        {"id": "formula", "variant": "it_entropyformula", "props": {}, "narration":
            "Let's make that average precise, because the famous formula is much friendlier than "
            "it looks. [pause] To get an average surprise, we do the natural thing. We take each "
            "possible outcome's surprise, and weight it by how often that outcome actually "
            "happens. Then we add all those weighted pieces together. [pause] Let's try it on a "
            "tiny weather source. In some town, it is sunny half the days, cloudy a quarter of "
            "them, and rainy the other quarter. [pause] Sunny has probability one half, so its "
            "surprise is one bit. Cloudy and rainy are one quarter each, so two bits apiece. "
            "[pause] Now weight and sum. Half, times one bit. Plus a quarter, times two bits. "
            "Plus another quarter, times two bits. [pause] Work it through, and the total comes "
            "to one point five bits per day. [pause] That number is the entropy of the weather in "
            "that town. [pause] And written in full, this is Shannon's celebrated formula. H "
            "equals minus the sum, over all outcomes, of p times the log of p. [pause] Do not let "
            "that minus sign intimidate you. It is only there for bookkeeping — the log of a "
            "probability is a negative number, and we want surprise to come out positive. The "
            "minus just flips the sign. [pause] So what does one point five bits actually mean, "
            "on the ground? It means that, on an average day, one and a half well-chosen yes-or-no "
            "questions are enough to nail down the weather. [pause] That, right there, is the true "
            "information content of the source — no more, and no less."},
    ]},

    {"id": "it-ch06-uncertainty", "title": "The Shape of Uncertainty", "segments": [
        {"id": "maxent", "variant": "it_maxent", "props": {}, "narration":
            "Entropy has a definite personality, and it is worth getting to know. [pause] Let's "
            "put three sources side by side and compare their entropies directly. [pause] First, "
            "a loaded coin — ninety percent heads, ten percent tails. Because it is so easy to "
            "predict, its entropy is low: under half a bit. You are rarely surprised by it. "
            "[pause] Second, a fair coin. Perfectly balanced, maximally unpredictable for two "
            "outcomes — a full one bit. [pause] Third, a fair six-sided die. Now there are six "
            "equally likely faces, and the entropy jumps to the logarithm of six, about two point "
            "five eight bits. [pause] Two big lessons fall out of this picture. [pause] Lesson "
            "one. Bias always lowers entropy. The more lopsided a source, the more predictable it "
            "is, and the less information each outcome carries. In the information sense, a "
            "predictable source is a poorer source. [pause] Lesson two. For a fixed number of "
            "possible outcomes, entropy is largest exactly when every outcome is equally likely. "
            "[pause] In fact, for n equally likely options, the entropy is precisely the logarithm "
            "of n. Maximum uncertainty is perfect balance. [pause] This second lesson has a name "
            "and a life of its own — the principle of maximum entropy. [pause] It says: when you "
            "genuinely know nothing else about a situation, the flattest, most balanced "
            "distribution is the most honest one you can assume, because it commits to the least. "
            "[pause] It is the mathematics of not fooling yourself — of refusing to pretend you "
            "know more than you do."},
        {"id": "letters", "variant": "it_letters", "props": {}, "narration":
            "Let's leave the toy coins behind and measure something real — the letters of written "
            "English. [pause] Imagine, first, that all twenty-six letters were equally likely. "
            "Then each one would carry the logarithm of twenty-six, which is about four point "
            "seven bits. That is the ceiling — the entropy of pure, random letters. [pause] But "
            "English is nowhere near equal. Look at the real frequencies. The letter E is "
            "absolutely everywhere. T, A, O, and I are common visitors too. [pause] Meanwhile J, "
            "Q, X, and Z are rare — you can go whole sentences without seeing one. [pause] Because "
            "the distribution is so uneven, real text is far more predictable than random letters "
            "would be. And more predictable means lower entropy. [pause] So let's feed these true "
            "frequencies into Shannon's formula and actually compute it. The answer comes out "
            "around four point two bits per letter. [pause] Noticeably below the four point seven "
            "of pure randomness. [pause] Now, that gap — between the real entropy and the maximum "
            "possible — might look small. But it is not a curiosity. It is real, unused space. "
            "[pause] It is precisely the room that a compression algorithm moves into and "
            "reclaims. [pause] Here is the principle to carry forward. Every predictable pattern in "
            "your data is entropy you are not using — bits left sitting on the table. [pause] And "
            "as we are about to see, someone can always come along and squeeze them out."},
    ]},

    {"id": "it-ch07-conditional", "title": "Conditional and Joint Entropy", "segments": [
        {"id": "conditional", "variant": "it_conditional", "props": {}, "narration":
            "So far we have measured the uncertainty of one source at a time. But the world comes "
            "in pairs. Clouds and rain. A symptom and a disease. A word and the word before it. "
            "[pause] So let's learn to slice uncertainty apart when two variables, X and Y, are "
            "tangled together. [pause] Start with the joint entropy, written H of X and Y. It is "
            "just the total surprise in the pair, considered together — everything you do not know "
            "about both at once. [pause] The beautiful fact is that this total splits cleanly into "
            "three blocks. Watch the bar. [pause] On the left, the part of X that Y tells you "
            "nothing about — X's private uncertainty. We call it the conditional entropy, H of X "
            "given Y. [pause] On the right, the mirror image — Y's private uncertainty, H of Y "
            "given X. [pause] And in the middle, the piece the two variables share. Hold onto "
            "that middle block; it is about to become a star. [pause] Now here is the single most "
            "useful identity in the subject, and the bar makes it obvious. The chain rule. [pause] "
            "The joint entropy H of X and Y equals the entropy of X, plus the entropy of Y given "
            "that you already know X. [pause] In plain words: the total surprise in the pair is "
            "the surprise of the first, plus whatever surprise is left in the second once the "
            "first is known. [pause] Learn one variable, and it can only shrink your uncertainty "
            "about the other — never grow it. [pause] Knowing something never hurts. And that "
            "shared middle block, the amount one variable reveals about the other, is important "
            "enough that it deserves a beat all its own."},
    ]},

    {"id": "it-ch08-redundancy", "title": "The Redundancy of Language", "segments": [
        {"id": "redundancy", "variant": "it_redundancy", "props": {}, "narration":
            "Let's use these ideas to catch something surprising about your own language. [pause] "
            "Shannon ran a famous little experiment, and you can run it in your head right now. "
            "[pause] Take an ordinary English sentence, cover up the next letter, and try to guess "
            "it before you look. [pause] The quick brown f... You already know it is an o, then an "
            "x. You barely had to think. [pause] That is the game, and in English you win it "
            "astonishingly often. After a q, you know a u is coming. At the end of many words, "
            "you can feel the letters before you read them. [pause] Now connect that to entropy. "
            "A letter looked at completely alone carries about four point two bits, as we just "
            "computed. [pause] But a letter seen in the context of everything before it? Once you "
            "have the sentence so far, the next letter is often nearly certain — so it carries far "
            "less new information. [pause] Watch the meter fall as context builds — from four "
            "point two bits, down toward roughly one bit per letter, and by some estimates even "
            "less. [pause] Which leads to a striking headline. Written English is about seventy-"
            "five percent redundant. [pause] Three out of every four letters, in a sense, you "
            "could have guessed from the rest. [pause] And that redundancy is not a flaw. It is a "
            "feature, working two jobs at once. [pause] It is exactly what lets you read straight "
            "through typos and autocorrect disasters without slowing down. [pause] And it is "
            "exactly what a compression program hunts down and deletes. Redundancy is predictable "
            "structure — and predictable structure is entropy you are not using."},
    ]},

    {"id": "it-ch08b-info-gain", "title": "Information Gain", "segments": [
        {"id": "infogain", "variant": "it_infogain", "props": {}, "narration":
            "Let's turn entropy into a tool for making decisions. [pause] Think back to twenty "
            "questions. A good question halves the possibilities — but what actually makes one "
            "question better than another? Entropy gives us the exact answer. [pause] Suppose you "
            "are sorting a mixed group — six cats and six dogs, all jumbled together. Before you "
            "ask anything, the label is a perfect coin flip. The entropy is one full bit. [pause] "
            "Now you ask a question. Does it purr? [pause] Watch what happens. The cats fall into "
            "one group, the dogs into the other. Each group is now pure — all one kind. And a "
            "pure group has zero entropy. There is nothing left to be uncertain about. [pause] So "
            "your uncertainty just dropped from one full bit, all the way to zero. [pause] That "
            "drop has a name — the information gain of the question. It is simply the entropy "
            "before, minus the average entropy afterward. [pause] Here, one bit minus zero — a "
            "gain of one whole bit. A perfect question. [pause] A weak question — say, is it "
            "sitting down — barely separates the animals, leaves both groups still mixed, and "
            "yields almost no gain. [pause] And here is the beautiful connection. Information gain "
            "is exactly the mutual information between the question and the label. It measures how "
            "much the answer tells you about the thing you care about. [pause] This one idea is "
            "the engine inside a whole family of machine-learning models. [pause] Every time a "
            "decision tree grows a branch, it examines every possible question and greedily picks "
            "the one with the highest information gain — the one that cuts entropy the most. "
            "[pause] It is twenty questions, played by a machine, with Shannon keeping score."},
    ]},

    # ============================================================= PART 3 — COMPRESSION
    {"id": "it-ch09-limit", "title": "The Compression Limit", "segments": [
        {"id": "div", "variant": "it_divider",
         "props": {"n": 3, "title": "Compression", "sub": "how small can a message get?", "color": CODE},
         "narration":
            "Part three. Compression. [pause] We have felt, again and again, the gap between "
            "predictable data and its true information content. Now we cash that intuition in. "
            "Shannon will tell us exactly how far a message can be squeezed — and draw a wall we "
            "can never cross."},
        {"id": "sourcecoding", "variant": "it_sourcecoding", "props": {}, "narration":
            "So, concretely — how small can we squeeze a message and still get it back perfectly? "
            "[pause] Picture taking your data and beginning to compress. You find the repeated "
            "patterns. You spend short codes on the common symbols and long ones on the rare. The "
            "file shrinks. [pause] And it shrinks, and shrinks — and then, no matter how clever "
            "you get, it stops. It hits a wall. [pause] Here is the profound part. The position of "
            "that wall is not an accident of your particular algorithm. It is fixed by the source "
            "itself. It sits exactly at the entropy. [pause] This is Shannon's source coding "
            "theorem, one of the great results of the twentieth century. [pause] It says the best "
            "possible average code length is at least the entropy — H bits per symbol. [pause] "
            "Not with a smarter trick. Not with a faster computer. Not with a thousand years of "
            "engineering. The floor is the floor, forever. [pause] If you try to push below H and "
            "still recover every message perfectly, you are guaranteed to lose information — the "
            "way a perpetual motion machine is guaranteed to fail. It is not hard. It is "
            "impossible. [pause] So entropy quietly reveals its second face. It is not only a "
            "measure of uncertainty. It is a hard, provable limit on compression. [pause] The two "
            "meanings are one. The average surprise of a source is exactly the smallest number of "
            "bits you need to describe it. [pause] That is why entropy beats at the heart of every "
            "zip file, every photo, every stream — telling each one precisely how far it may go, "
            "and not one bit further."},
    ]},

    {"id": "it-ch09b-typical-set", "title": "The Typical Set", "segments": [
        {"id": "aep", "variant": "it_aep", "props": {}, "narration":
            "Let's answer a question we have been circling. Why is the entropy the compression "
            "limit? What is really going on underneath? [pause] The answer is one of the most "
            "beautiful ideas in the whole theory — the typical set. [pause] Imagine flipping a "
            "biased coin — eighty percent heads — one hundred times in a row. [pause] How many "
            "different sequences could you possibly get? Two, raised to the hundredth power. An "
            "astronomical number — far more than the atoms in your body. [pause] But here is the "
            "thing. You will almost never see the vast majority of them. A run of a hundred "
            "straight tails is technically possible, but you would wait longer than the age of "
            "the universe to witness it. [pause] The sequences you actually get all look, in a "
            "sense, alike. They have roughly eighty heads and twenty tails, in some order. "
            "[pause] These are called the typical sequences. And there is a stunning fact about "
            "them. [pause] The number of typical sequences is not two to the hundred. It is "
            "roughly two, raised to the power of n times the entropy — here, about two to the "
            "seventy-second. [pause] That is a vanishingly tiny fraction of all the possibilities. "
            "[pause] And yet — this is the magic — those few typical sequences together hold "
            "essentially all of the probability. Almost every sequence reality will ever hand you "
            "lives inside that small set. [pause] This is the asymptotic equipartition property, "
            "and it delivers compression on a plate. [pause] We do not need codes for all "
            "two-to-the-hundred sequences. We can simply ignore the atypical ones — they "
            "practically never happen. [pause] We just number the typical set. And labelling "
            "two-to-the-n-times-H items takes exactly n times H bits. [pause] There it is. The "
            "entropy, made concrete. Shannon's compression limit is really a statement about "
            "which sequences the world actually bothers to produce. [pause] And this is why "
            "compression only truly pays off over long messages. For a single flip, there is "
            "nothing to exploit. But stretch to thousands of symbols, and the typical set "
            "sharpens, the atypical fades away, and real files collapse toward their entropy — "
            "reliably, every time. The law of large numbers, quietly doing the work."},
    ]},

    {"id": "it-ch10-huffman", "title": "Huffman Coding", "segments": [
        {"id": "huffman", "variant": "it_huffman", "props": {}, "narration":
            "Knowing the limit exists is one thing. Actually building a code that reaches it is "
            "another. So let's construct one, by hand — the Huffman code, still in daily use "
            "seventy years on. [pause] Here is our source: six symbols with different frequencies. "
            "E is the most common; N the rarest. We want short codes for the frequent ones. "
            "[pause] Huffman's insight is to build the code backwards — not from the top down, but "
            "from the bottom up, starting with the least likely symbols. [pause] Here is the move. "
            "Find the two least likely items and merge them into a small pair. Their combined "
            "probability becomes a brand-new node that stands in for both. [pause] Then simply "
            "repeat. Again, reach for the two least likely items — whether they are original "
            "symbols or merged nodes — and join them under a new parent. [pause] Watch the pieces "
            "combine, step by step, the rarest ones binding together first, until everything hangs "
            "from a single root at the top. A whole tree, grown from the bottom. [pause] Now, to "
            "read off each symbol's codeword, you just walk down from the root. Every time you go "
            "left, write a zero. Every time you go right, write a one. [pause] Look where the "
            "symbols landed. The common E sits high, with a short code. The rare N sits deep, with "
            "a long one — exactly the trade we wanted. [pause] And here is the property that makes "
            "it all work. No codeword is the beginning of any other codeword. It is a prefix-free "
            "code. [pause] So a receiver reading the raw stream of bits never gets confused about "
            "where one symbol ends and the next begins — no commas, no separators needed. [pause] "
            "Best of all, the average length lands right down at the entropy. Huffman does not "
            "just compress. It compresses provably about as well as anything ever could."},
    ]},

    {"id": "it-ch11-arithmetic", "title": "Arithmetic Coding", "segments": [
        {"id": "arithmetic", "variant": "it_arithmetic", "props": {}, "narration":
            "Huffman is elegant, but it has one stubborn weakness. It must spend a whole number "
            "of bits on every symbol — one bit, or two, never one-and-a-half. [pause] When a "
            "symbol's ideal length is fractional, that rounding quietly wastes space. So how do we "
            "reclaim those fractions of a bit? [pause] The answer is a gorgeous idea called "
            "arithmetic coding, and its trick is to encode an entire message as a single number "
            "between zero and one. [pause] Watch how. We start with the full interval, from zero "
            "to one, and we carve it up by probability. In our source, A has probability zero "
            "point six, so A claims the first sixty percent of the line. B takes the rest. [pause] "
            "To encode the first symbol, A, we simply throw away everything else and zoom in on "
            "A's slice — from zero to zero point six. [pause] Now the magic: we subdivide that "
            "smaller interval in exactly the same proportions. To encode the next symbol, B, we "
            "zoom into B's portion of what remains. [pause] The live interval on the right keeps "
            "narrowing — zero to zero point six, then zero point three-six to zero point six, and "
            "on it goes. [pause] Encode a third symbol, A, and we zoom in one more time, to an "
            "even tinier sliver. [pause] When the message ends, we are left with one final, "
            "narrow interval. And any number that falls inside it — say, zero point four — encodes "
            "the whole message, unambiguously. [pause] Here is the beautiful part. Each symbol "
            "shrinks the interval by its own probability, so a likely message ends up in a "
            "relatively wide interval that needs very few digits to pin down. [pause] Rare "
            "messages get tiny intervals and cost more. Which is exactly, to the fraction of a "
            "bit, what the entropy demanded all along. Arithmetic coding kisses the Shannon limit."},
    ]},

    {"id": "it-ch12-lossy", "title": "Lossy Compression", "segments": [
        {"id": "lossy", "variant": "it_lossy", "props": {}, "narration":
            "Everything so far has been lossless. Every bit recovered, perfectly, down to the "
            "last one. That is what you need for a text file or a bank statement. [pause] But "
            "think about a photograph, or a song, or a movie. Do you truly need every bit back, "
            "exactly? Or just something your eyes and ears cannot tell apart from the original? "
            "[pause] The moment you are willing to accept a little error, a whole new door opens — "
            "lossy compression. And with it comes a fundamental trade-off. [pause] Look at this "
            "curve. Along the bottom is distortion — how much error you will tolerate. Up the "
            "side is the rate — how many bits you must spend. [pause] At the top left, you insist "
            "on near-perfect fidelity, and you pay for it with a big, heavy file. [pause] Slide "
            "down and to the right, and you accept more blur, more noise — and the file shrinks "
            "dramatically. [pause] This curve is not a guess or a rule of thumb. Its exact shape "
            "is fixed by a branch of the theory that Shannon founded, called rate-distortion "
            "theory. For a given amount of acceptable error, it names the smallest possible number "
            "of bits. [pause] And this is the theory living inside your daily life. JPEG for "
            "images. MP3 for music. Every video codec that streams to your screen. [pause] They "
            "all do the same clever thing. They spend precious bits only where your perception can "
            "actually notice — the sharp edges, the loud notes — and they quietly throw away the "
            "fine detail you were never going to miss. [pause] Lossless compression removes what "
            "is redundant. Lossy compression removes what is imperceptible. Both are just "
            "information theory, deciding what truly matters."},
    ]},

    # ================================================== PART 4 — COMPARING DISTRIBUTIONS
    {"id": "it-ch13-cross-entropy", "title": "Cross-Entropy and KL", "segments": [
        {"id": "div", "variant": "it_divider",
         "props": {"n": 4, "title": "Comparing Beliefs", "sub": "the bit-cost of being wrong", "color": NOISE},
         "narration":
            "Part four. Comparing beliefs. [pause] Until now, we have quietly assumed we know the "
            "true probabilities of our source. But in the real world we almost never do. We work "
            "from a model — a guess about how the world behaves. [pause] So what happens when that "
            "guess is wrong? Remarkably, information theory can measure the cost of being wrong — "
            "and it measures it in bits."},
        {"id": "crossentropy", "variant": "it_crossentropy", "props": {}, "narration":
            "Every optimal code is tailored to one specific set of probabilities. So here is the "
            "sharp question: what does it cost you when your probabilities are wrong? [pause] Let "
            "the true frequencies of our four symbols be the distribution p. A is one half, B a "
            "quarter, C and D an eighth each. The perfect code for p costs its entropy — one point "
            "seven five bits per symbol, as we found before. [pause] But suppose you did not know "
            "that truth. You assumed, instead, that all four symbols were equally likely — a "
            "model we will call q — and you built your code from that wrong belief. [pause] Your "
            "code, tuned for q, gives every symbol a flat two bits. [pause] Now run the real "
            "world through it. Send data that actually follows p, encoded with the code built for "
            "q. What is the average cost? [pause] It comes out to two full bits per symbol — more "
            "than the one point seven five that the data truly required. [pause] That quantity — "
            "the average bits you spend encoding the real distribution p using a code designed "
            "for the wrong distribution q — is called the cross-entropy. [pause] And it obeys an "
            "iron law. Cross-entropy is always greater than or equal to the true entropy. Always. "
            "[pause] A wrong model can only ever cost you extra bits. It can never, ever beat the "
            "code built for the truth. [pause] Now, if measuring how well a guessed distribution q "
            "matches a true distribution p reminds you of machine learning — hold that thought "
            "tight. [pause] Because cross-entropy is not just an analogy for training modern "
            "neural networks. It is, quite literally, the loss function they minimize."},
        {"id": "kl", "variant": "it_kl", "props": {}, "narration":
            "Let's isolate the waste itself — the pure penalty for being wrong. [pause] We just "
            "held two numbers side by side. The true entropy, H of p — the bits you would spend "
            "with a perfect model. And the cross-entropy, H of p and q — the bits you actually "
            "spend with your imperfect one. [pause] Subtract the first from the second. Whatever "
            "is left over is the cost of your error, and nothing else. [pause] That leftover has a "
            "name: the Kullback-Leibler divergence — usually just called K-L divergence, or "
            "relative entropy. [pause] It is the number of extra bits you pay, per symbol, for "
            "believing q when reality is actually p. [pause] It has three properties worth "
            "burning into memory. [pause] First, it is zero — and only zero — when your model "
            "exactly matches reality. Perfect belief, zero penalty. [pause] Second, it is never "
            "negative. You can never do better than the truth; the best you can hope for is to "
            "match it. [pause] Third, and this one surprises people, it is not symmetric. The cost "
            "of mistaking p for q is generally not the same as mistaking q for p. Direction "
            "matters. It is a divergence, not a true distance. [pause] And now the payoff that "
            "ties this whole part together. [pause] When you train a model by minimizing its "
            "cross-entropy, you are — provably, exactly — shrinking the K-L divergence between "
            "your model and reality. [pause] Learning, in the language of information theory, is "
            "just this: dragging your beliefs toward the truth, one bit at a time."},
    ]},

    {"id": "it-ch14-mutual-information", "title": "Mutual Information", "segments": [
        {"id": "mutualinfo", "variant": "it_mutualinfo", "props": {}, "narration":
            "Let's return to that shared middle block from the chain rule and give it the "
            "spotlight it deserves. [pause] Here is the question it answers. If I tell you the "
            "value of X, how much does that shrink your uncertainty about Y? [pause] Picture two "
            "circles. The left circle is the entropy of X — the total uncertainty you have about "
            "it. The right circle is the entropy of Y. [pause] Now, if X and Y are related in any "
            "way, the two circles overlap. And that overlap is the whole point of this beat. "
            "[pause] It is called the mutual information between X and Y — the uncertainty the two "
            "variables share. [pause] Put as plainly as possible: it is the number of bits you "
            "learn about X, for free, just by observing Y. [pause] Written as an equation, the "
            "mutual information equals the entropy of X, minus the entropy of X once you already "
            "know Y. It is your uncertainty before, minus your uncertainty after. Whatever the "
            "observation removed, that is the information it gave you. [pause] The left crescent — "
            "the part of X that the overlap does not cover — is what stays uncertain even after "
            "you have seen Y. [pause] And what about two variables that have nothing to do with "
            "each other? Watch. The circles drift apart, the overlap vanishes, and the mutual "
            "information drops to zero. [pause] Independence means knowing one tells you exactly "
            "nothing about the other. [pause] This single number is quietly everywhere in modern "
            "science. It measures how much a feature reveals about a label in machine learning. "
            "How strongly two genes are linked. How well two signals correlate — capturing curved "
            "relationships that ordinary correlation completely misses. [pause] And, as we are "
            "about to see, it measures exactly how much of your message survives a noisy channel."},
    ]},

    {"id": "it-ch14b-data-processing", "title": "Information Can Only Be Lost", "segments": [
        {"id": "dpi", "variant": "it_dpi", "props": {}, "narration":
            "Here is a rule that sounds almost obvious once you hear it — but it has real teeth. "
            "[pause] Information can only be lost, never created, by processing. [pause] Picture "
            "a chain. A source, X, is sent through a noisy channel, producing a corrupted copy, "
            "Y. Then you take Y and run it through any processing you like — a filter, a formula, "
            "a fancy algorithm — to produce a new result, Z. [pause] Now compare two quantities. "
            "The mutual information between X and Y — how much the noisy copy tells you about the "
            "original. And the mutual information between X and Z — how much your processed "
            "version tells you. [pause] The data processing inequality states, flatly, that the "
            "information between X and Z can never exceed the information between X and Y. [pause] "
            "Watch the bars. Whatever information about X survived into Y, your processing can "
            "preserve it, or lose some of it — but it can never increase it. [pause] Once "
            "information about the source is gone from Y, no amount of clever computation can "
            "conjure it back. [pause] This is deeply counterintuitive in the age of artificial "
            "intelligence. It means no algorithm, however powerful, can pull out more information "
            "about the original than the data it was handed actually contains. [pause] You cannot "
            "truly enhance a blurry photo into detail that was never captured — no matter what "
            "the movies show you. The information simply is not there to recover. [pause] "
            "Processing can reorganize information. It can make it easier to use. It can throw it "
            "away. [pause] But it can never manufacture information out of nothing. [pause] "
            "There is a hopeful flip side, though. If the information you need did survive into "
            "the data, then good processing can bring it to the surface — which is exactly what a "
            "well-trained model does. It cannot invent signal, but it can rescue the signal that "
            "is truly there, buried under noise. [pause] Garbage in, garbage out — it turns out — "
            "is a theorem."},
    ]},

    {"id": "it-ch15-perplexity", "title": "Perplexity and Language Models", "segments": [
        {"id": "perplexity", "variant": "it_perplexity", "props": {}, "narration":
            "Let's bring these ideas crashing into the present day — into the large language "
            "models behind today's A-I. Because at their core, they run on exactly the "
            "information theory we have built. [pause] A language model does one deceptively simple "
            "thing. It looks at some text and predicts the next word, as a probability over every "
            "possible word. [pause] Take the sentence: the cat sat on the — blank. [pause] A good "
            "model puts most of its probability on mat, a decent chunk on floor, a little on sofa, "
            "and only a sliver on something like moon. [pause] Now, how do we score that "
            "prediction? With cross-entropy, our exact tool for the cost of an imperfect model. "
            "[pause] When the true next word arrives, we measure the surprise the model felt — the "
            "log of one over the probability it assigned. Low probability on the right answer "
            "means high surprise, means a big penalty. [pause] Averaged over an entire corpus, "
            "that is the cross-entropy loss, and driving it down is the whole of training. [pause] "
            "But researchers love to report a friendlier cousin of this number, called perplexity. "
            "It is simply two raised to the power of the cross-entropy. [pause] And it has a "
            "wonderfully concrete meaning. Perplexity is the effective number of words the model "
            "is choosing between at each step. [pause] A perplexity of two means the model is as "
            "confused as if it were flipping a fair coin between two options. A perplexity of a "
            "hundred means it is floundering among a hundred. [pause] So the entire race to build "
            "better language models is, underneath the marketing, a race to lower perplexity — to "
            "make the machine less surprised by human language. [pause] Every A-I you have ever "
            "used is, at heart, an entropy-minimizing machine. Shannon's fingerprints are all over "
            "it."},
    ]},

    # ========================================================= PART 5 — THE NOISY CHANNEL
    {"id": "it-ch16-noisy-channel", "title": "The Noisy Channel", "segments": [
        {"id": "div", "variant": "it_divider",
         "props": {"n": 5, "title": "Noisy Channels", "sub": "talking clearly through a broken wire", "color": BIT},
         "narration":
            "Part five. Noisy channels. [pause] Everything so far assumed our bits arrive exactly "
            "as they were sent. But the real world is not so tidy. Wires crackle. Signals fade. "
            "Bits flip in transit. [pause] This is where Shannon reached his most astonishing "
            "result of all — and rewrote what engineers believed was possible."},
        {"id": "channel", "variant": "it_channel", "props": {}, "narration":
            "Every real communication channel is noisy. A radio link, a phone line, a scratch on "
            "a DVD, a fading signal from a spacecraft. [pause] To reason about all of them at once, "
            "we strip the idea down to its bones — the simplest model of noise there is, the "
            "binary symmetric channel. [pause] Here is how it works. You send a single bit in. "
            "Most of the time, it comes out the other side unchanged. But with some fixed "
            "probability, the noise flips it. A zero arrives as a one. A one arrives as a zero. "
            "[pause] Watch the stream. On the left, the sender pushes clean, deliberate bits into "
            "the channel. [pause] Inside, noise strikes at random, sparking here and there with no "
            "pattern you can predict. [pause] And on the right, the receiver reads out whatever "
            "survived. A few of those bits are now wrong — flipped — marked in red. [pause] Now "
            "here is the genuinely cruel part, the thing that makes this hard. The receiver has no "
            "way of knowing which bits flipped. [pause] A received one looks utterly identical "
            "whether it was sent as a one, or sent as a zero and corrupted along the way. The "
            "damage is invisible. [pause] So it looks completely hopeless. If any bit can silently "
            "betray you, and you can never tell which, how could you ever communicate reliably at "
            "all? [pause] For years, the smartest engineers believed you simply couldn't. They "
            "were convinced that noise imposed a permanent ceiling — that to cut errors, you had "
            "to slow down toward a crawl, and even then a little noise always leaked through. "
            "[pause] Shannon proved every one of them wrong. And the way he did it is the most "
            "beautiful surprise in the whole subject."},
    ]},

    {"id": "it-ch17-capacity", "title": "Channel Capacity", "segments": [
        {"id": "capacity", "variant": "it_capacity", "props": {}, "narration":
            "So how much real, trustworthy information can a noisy channel actually carry? [pause] "
            "Shannon gave the answer both a name and an exact formula. The name is the channel "
            "capacity. [pause] For our binary symmetric channel, the capacity C equals one, minus "
            "the entropy of the noise itself. One minus H of p. [pause] Look at the curve, and "
            "read off its two ends. [pause] When the flip probability is zero, the wire is "
            "flawless, the noise has zero entropy, and the capacity is a full one bit per use. You "
            "get out everything you put in. [pause] Now slide the noise up toward one half. The "
            "capacity falls, and falls, until — at a flip probability of one half — it hits zero. "
            "[pause] And that makes perfect sense. A channel that flips every bit with a coin toss "
            "is pure randomness. Its output has nothing to do with its input. It carries no "
            "information whatsoever. [pause] But between those extremes lies the wonderful part. "
            "Even a genuinely noisy channel — say one that corrupts eighteen percent of its bits — "
            "still carries a solid third of a bit of real information on every single use. [pause] "
            "And now the theorem that stunned the world of engineering. Shannon's noisy-channel "
            "coding theorem. [pause] As long as you transmit at a rate below the capacity, you can "
            "drive your probability of error as close to zero as you desire. Not smaller — "
            "arbitrarily, vanishingly close to zero — with clever enough coding. [pause] Read that "
            "again. Perfect, reliable communication, straight through an imperfect, noisy channel. "
            "The ceiling everyone believed in simply does not exist. [pause] But there is a hard "
            "edge. Try to transmit above the capacity, and reliable communication becomes flatly, "
            "provably impossible. [pause] Capacity is the true speed limit of every wire, every "
            "antenna, every fibre on Earth. Below it lies paradise. Above it, a wall."},
    ]},

    {"id": "it-ch18-bandwidth", "title": "Bandwidth and the Shannon Limit", "segments": [
        {"id": "bandwidth", "variant": "it_bandwidth", "props": {}, "narration":
            "Our coin-flipping channel sent clean, discrete bits. But a real radio wave or copper "
            "wire is analog — a continuous, wobbling voltage, smeared by continuous noise. Does "
            "capacity still have something to say? [pause] It does, and the result is one of the "
            "most famous equations in all of engineering — the Shannon-Hartley theorem. [pause] It "
            "says the capacity C equals the bandwidth B, times the logarithm of one plus the "
            "signal-to-noise ratio. [pause] Let's unpack the two knobs it hands you. [pause] The "
            "first is bandwidth — the width of the band of frequencies you are allowed to use. "
            "Widen the pipe, and capacity rises in direct proportion. This is why fifth-generation "
            "cellular reaches for ever-higher frequency bands: more bandwidth, more capacity. "
            "[pause] The second knob is the signal-to-noise ratio — how loud your signal is "
            "compared to the noise floor. Turn up the power, and capacity rises too. [pause] But "
            "look carefully at the curve, because here the logarithm plays the tyrant. [pause] "
            "Because capacity grows only with the log of the signal power, you face brutally "
            "diminishing returns. To merely double the capacity through power alone, you must "
            "roughly square the signal strength. [pause] Bandwidth is cheap and linear. Power is "
            "expensive and logarithmic. That single asymmetry quietly shapes the entire design of "
            "modern communication. [pause] This one formula sizes your home wi-fi, the modem in "
            "your wall, every cell tower on the skyline, and the fibre threads carrying the "
            "internet under the oceans. [pause] It is the same capacity idea as before — a hard, "
            "unbreakable limit on communication — now translated into the messy, continuous, analog "
            "world where our signals actually live."},
    ]},

    {"id": "it-ch18b-repetition", "title": "Repetition and Redundancy", "segments": [
        {"id": "repetition", "variant": "it_repetition", "props": {}, "narration":
            "We know reliable communication through noise is possible. Let's start with the "
            "crudest possible way to do it, just to feel the problem in our hands. [pause] The "
            "repetition code. [pause] You want to send a single one, and you are worried the "
            "channel might flip it. So you do the obvious thing. You send it three times. One, "
            "one, one. [pause] Now the noise strikes, and flips the middle bit. The receiver sees "
            "one, zero, one. [pause] But the fix is easy. Just take a majority vote. Two ones "
            "against a single zero — the ones win. The receiver correctly decides you meant a "
            "one. [pause] The error has been detected and corrected, automatically, with no need "
            "to ask you to send it again. [pause] And you can make it as safe as you like. Send "
            "five copies, or seven, and you can survive two or three flips. The more copies, the "
            "more errors you can outvote. [pause] So repetition works. But look at the price you "
            "paid. [pause] To send one real bit of information, you transmitted three. Your code "
            "rate — useful bits divided by total bits — is just one third. [pause] Two out of "
            "every three bits were pure overhead. And to get safer still, the rate gets even "
            "worse, crawling toward zero. [pause] This is the trap everyone assumed was "
            "inescapable — that you could only buy reliability by throwing away speed. [pause] "
            "And this is exactly the ceiling Shannon shattered. His theorem promised you could "
            "drive the error rate to nearly zero while keeping the rate high — right up near the "
            "channel capacity. [pause] Repetition is the sledgehammer. What we really need are "
            "the surgical tools — codes that add just a little, cleverly shaped redundancy, and "
            "get far more protection in return."},
    ]},

    {"id": "it-ch19-error-correction", "title": "Error-Correcting Codes", "segments": [
        {"id": "hamming", "variant": "it_hamming", "props": {}, "narration":
            "Shannon promised that near-perfect communication through noise was possible. But his "
            "proof was famously non-constructive — it swore the codes existed without telling us "
            "how to build one. So let's actually build one. [pause] The core idea is to add "
            "redundancy — but cleverly, with structure, not by blindly repeating everything. "
            "[pause] Here is a classic that does exactly that: the Hamming code, drawn as three "
            "overlapping circles. [pause] Into the regions where the circles cross, we drop our "
            "four data bits — the actual message we care about protecting. [pause] Then we add "
            "three parity bits, one guarding each circle. Each parity bit is set so that its own "
            "circle contains an even number of ones. Three tidy, even circles. [pause] Now we send "
            "all seven bits — four of data, three of parity — out across the noisy channel. And we "
            "let the noise do its worst: it flips one of them. [pause] Watch what happens. Every "
            "circle that contained the damaged bit now holds an odd number of ones. Its parity is "
            "broken. Its ring flashes red. [pause] And here is the fingerprint. The exact pattern "
            "of which circles broke, and which stayed even, points to one and only one bit — the "
            "single bit that must have flipped. [pause] The receiver reads that pattern, called "
            "the syndrome, locates the guilty bit, and simply flips it back. [pause] No asking the "
            "sender to repeat. No slowing down. The message quietly repairs itself, in flight. "
            "[pause] This is the invisible magic protecting nearly everything digital you touch. "
            "The QR code that still scans with a coffee stain across it. The space probe "
            "whispering across billions of miles. The memory chip in the very device you are "
            "watching this on. [pause] Redundancy, shaped with the precision of information theory, "
            "turns the terror of noise into something we can simply, calmly undo."},
    ]},

    {"id": "it-ch19b-separation", "title": "The Separation Theorem", "segments": [
        {"id": "separation", "variant": "it_separation", "props": {}, "narration":
            "Now watch two halves of this course click together into a single machine. [pause] We "
            "have learned two opposite skills. [pause] Source coding — compression — whose whole "
            "job is to remove redundancy and shrink a message down toward its entropy. [pause] "
            "And channel coding — error correction — whose whole job is to add redundancy, to "
            "protect a message against noise. [pause] Put them in a line, and it looks completely "
            "insane. First you painstakingly strip out every redundant bit. Then, immediately, "
            "you add redundant bits right back in. Why not just leave them there? [pause] Because "
            "the two kinds of redundancy are utterly different. [pause] The redundancy in raw "
            "data is accidental and messy — the lopsided letter frequencies, the repeated "
            "patterns. It does nothing to protect you against noise. [pause] The redundancy that "
            "channel coding adds is deliberate and precisely structured — engineered so that any "
            "error lights up and points to itself. [pause] And here is Shannon's remarkable "
            "separation theorem. [pause] You lose absolutely nothing by doing these two jobs "
            "separately, one after the other. [pause] The best possible system can always be "
            "built as a compressor, followed by an independent error-correcting code. You never "
            "need to tangle them together. [pause] And this is not just a theoretical nicety. It "
            "is why the entire engineering world is built in clean layers. [pause] The team "
            "designing a compression format, like JPEG or ZIP, never has to think about wi-fi "
            "static. The team designing the error-correction for that wi-fi never has to know "
            "what is being sent. [pause] Compress first. Then protect. Two clean, independent "
            "layers — blessed by a theorem — and the whole tower of modern communication rests on "
            "that promise. [pause] One honest caveat. The theorem assumes unlimited time and "
            "arbitrarily long codes. In the real world, with tight delays, engineers sometimes do "
            "blend the two layers for a little extra performance. But as a guiding principle, "
            "separation is why the internet can be built by thousands of teams who never have to "
            "talk to one another."},
    ]},

    # ============================================================= PART 6 — THE BIG PICTURE
    {"id": "it-ch20-deepest", "title": "The Deepest Idea", "segments": [
        {"id": "div", "variant": "it_divider",
         "props": {"n": 6, "title": "The Big Picture", "sub": "one idea, wired through everything", "color": BIT},
         "narration":
            "Part six. The big picture. [pause] We have built the whole theory from a single "
            "surprising event. Before we gather it all together, let's push the very idea of "
            "information to its philosophical limit — and then watch it echo across all of "
            "science."},
        {"id": "kolmogorov", "variant": "it_kolmogorov", "props": {}, "narration":
            "Shannon's entropy is powerful, but it has one quiet requirement. It needs a "
            "probability distribution — a source that emits symbols with known odds. [pause] But "
            "here is a haunting question. What is the information content of one single, fixed "
            "object? Not a source. Just... this one specific string of characters, sitting on the "
            "page. There are no probabilities in sight. [pause] The answer is one of the deepest "
            "ideas in computer science — Kolmogorov complexity. [pause] It defines the information "
            "in an object as the length of the shortest computer program that can reproduce it. "
            "[pause] Look at the first string. A-B repeated ten times over. It looks long, but you "
            "can describe it in a tiny breath: print A-B, ten times. A short program. So its "
            "complexity is low. It is deeply compressible. [pause] Now look at the second string — "
            "a jumble of random letters and digits with no pattern at all. [pause] What is the "
            "shortest program that prints it? There is no clever shortcut, no rule to exploit. The "
            "shortest program is essentially: print, and then the entire string, character by "
            "character. [pause] So a truly random object is incompressible. Its shortest "
            "description is just itself. And that gives us a stunning, precise definition of "
            "randomness. [pause] Random means incompressible. Random means maximally informative — "
            "there is simply no shorter story to tell. [pause] It connects straight back to "
            "entropy: both say that information is the length of the shortest faithful "
            "description. [pause] There is one last twist, and it is a beautiful one. In general, "
            "the shortest program can never be computed. No algorithm can reliably find it, for "
            "every input. [pause] The ultimate measure of information turns out to be perfectly "
            "well-defined — and forever beyond our full reach."},
    ]},

    {"id": "it-ch20b-landauer", "title": "The Physical Cost of a Bit", "segments": [
        {"id": "landauer", "variant": "it_landauer", "props": {}, "narration":
            "We are going to end this part somewhere you would never expect information theory to "
            "reach — inside physics itself. [pause] All along, we have treated a bit as something "
            "abstract. A yes or a no. A pure idea, floating free of the world. But is it, really? "
            "[pause] In nineteen sixty-one, a physicist named Rolf Landauer asked a startling "
            "question. What does it cost, in the physical world, to erase a single bit of "
            "information? [pause] And he found there is a hard, unavoidable answer. [pause] To "
            "erase one bit, you must dissipate at least a tiny, specific amount of energy, as "
            "heat. The amount is k, times the temperature T, times the natural logarithm of two. "
            "[pause] It is a minuscule number at room temperature — but it is not zero, and it can "
            "never be zero. Erasing information warms the world, by law. [pause] Watch the bit "
            "vanish, and the heat pour out. [pause] Why does this happen? Because erasing is "
            "irreversible. Two possibilities — a one or a zero — collapse into one certain "
            "outcome. And in thermodynamics, destroying possibilities like that always releases "
            "heat. [pause] And now the punchline that should give you chills. [pause] The entropy "
            "in Shannon's formula — the one we built from surprise and coin flips — is not merely "
            "similar to the entropy of thermodynamics, the entropy of heat and disorder and the "
            "arrow of time. [pause] They are, mathematically, the very same quantity. Shannon even "
            "borrowed the name entropy from physics, on von Neumann's advice. [pause] Your hard "
            "drive and a steam engine are governed by the same equation. [pause] Information is "
            "not floating in some abstract realm. It is physical. It is written in energy and "
            "heat, and it obeys the deepest laws we know. [pause] It even reaches into one of "
            "physics' great puzzles. When something falls into a black hole, its information "
            "seems to vanish — and whether the universe truly allows that is still fiercely "
            "debated, in the language of entropy Shannon gave us. [pause] From a coin flip, to "
            "your hard drive, to the edge of a black hole — the same idea, all the way down."},
    ]},

    {"id": "it-ch21-everywhere", "title": "Information Everywhere", "segments": [
        {"id": "apps", "variant": "it_apps", "props": {}, "narration":
            "Step back now, and look at how far a single idea has traveled. It is genuinely hard "
            "to overstate. [pause] At the center of it all sits the bit — surprise, made "
            "countable. And from that one small atom, look at everything that grows. [pause] "
            "Compression. Every ZIP archive, every JPEG photo, every MP3 song lives right up "
            "against the entropy limit we drew — squeezing out redundancy, and no further. [pause] "
            "Machine learning. The cross-entropy loss that trains almost every neural network is, "
            "precisely, our bit-cost of a wrong model. Perplexity is its scoreboard. [pause] "
            "Communication. Five-G, wi-fi, satellite links, and the faint signals from deep-space "
            "probes all ride on channel capacity and error-correcting codes. [pause] Biology. The "
            "genome is a code written in four letters, and we measure the information in DNA with "
            "these very same tools. [pause] Cryptography. A perfect cipher is defined as one whose "
            "output has maximum entropy — pure, patternless surprise, giving an eavesdropper "
            "nothing to grip. [pause] And physics, most astonishing of all. Shannon's entropy "
            "turned out to be, mathematically, the very same entropy that governs heat, disorder, "
            "and the arrow of time in thermodynamics. The universe and your hard drive keep the "
            "same books. [pause] One definition of a single bit — and it reappears in your pocket, "
            "inside your cells, and at the trembling edge of the solar system. [pause] That is the "
            "reach of information theory."},
        {"id": "recap", "variant": "it_recap",
         "props": {"items": [
             "Information is surprise: rare events carry more bits — I(x) = log₂(1/p)",
             "A bit is one perfect yes/no question; log₂ counts how many you need",
             "Entropy H = −Σ p·log p is a source's average surprise",
             "Source coding theorem: entropy is the hard floor on compression",
             "Huffman & arithmetic codes reach that floor; lossy codes trade fidelity for size",
             "Cross-entropy & KL divergence price a wrong model in bits — the loss that trains AI",
             "Mutual information is the uncertainty two variables share",
             "Channel capacity C = 1 − H(p) is the speed limit; codes beat the noise",
         ], "closer": "Information is surprise you can count — and Shannon taught us how."},
         "narration":
            "Let's gather the whole journey into one breath. [pause] Information is surprise. Rare "
            "events carry more bits — given by the log of one over p. [pause] A bit is one perfect "
            "yes-or-no question, and the logarithm counts how many of them you need. [pause] "
            "Entropy is a source's average surprise — minus the sum of p times log p — and it is "
            "the beating heart of the theory. [pause] The source coding theorem makes that entropy "
            "a hard floor on compression. Huffman and arithmetic codes press right up against it, "
            "while lossy codes trade a little fidelity for a lot of size. [pause] Cross-entropy "
            "and K-L divergence measure the cost of a wrong model, in bits — the very loss that "
            "trains modern artificial intelligence. [pause] Mutual information is the uncertainty "
            "that two variables share. [pause] And channel capacity, one minus the entropy of the "
            "noise, is the speed limit of every wire — a limit that clever error-correcting codes "
            "let us approach without fear. [pause] From a single flipped coin, to the foundations "
            "of the entire digital age, it is all, in the end, one idea. [pause] Information is "
            "surprise you can count — and Claude Shannon taught us how to count it. [pause] Thanks "
            "for watching."},
    ]},
]
