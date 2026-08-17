# -*- coding: utf-8 -*-
"""Computer Vision From Scratch — screenplay.

Each chapter renders to its own MP4; all chapters concat into the master.
A chapter is a list of scene segments: {id, variant, props, narration}.
Narration is SPOKEN language (numbers as words), with [pause] markers (0.6s) after
new terms / big numbers / key ideas. Every on-screen element is mentioned in its
beat. Colors (dividers) = accent of the upcoming part. See skills/02 + skills/09.

Semantic colors reused from CVShared.C:
  pix=#22D3EE (pixels/data) · classic=#FBBF24 (classical) · neural=#A78BFA (deep) ·
  green=#34D399 (tasks/ok) · gen=#F472B6 (generative/frontier) · red=#F87171
"""

PIX, CLASSIC, NEURAL, GREEN, GEN, RED = "#22D3EE", "#FBBF24", "#A78BFA", "#34D399", "#F472B6", "#F87171"


CHAPTERS = [
    # ============================================================ PART 1 — SEEING
    {"id": "cv-ch01-big-picture", "title": "The Big Picture", "segments": [
        {"id": "title", "variant": "cv_title", "props": {}, "narration":
            "You open your eyes, and you just... see. A cat. A street. A friend's face. "
            "[pause] It feels effortless. You don't compute anything. You just know. [pause] "
            "But for a computer, seeing is one of the hardest problems we have ever tried to "
            "solve. [pause] This is computer vision — the field that teaches machines to turn "
            "raw light into understanding. [pause] It is the technology behind self-driving "
            "cars, medical scanners, face unlock, and the image generators taking over the "
            "internet. [pause] Over this course, we are going to build that understanding from "
            "the ground up. [pause] We will start with a single pixel. Then convolution — the "
            "one idea at the heart of it all. [pause] Then deep networks, the tasks they solve, "
            "and the transformers and foundation models running today. [pause] We will even "
            "open a code editor and write a working vision model together. [pause] There is no "
            "magic here. Just a handful of clear ideas, stacked one on top of another, until a "
            "machine can look at the world and understand it. Let's begin."},
        {"id": "hook", "variant": "cv_hook", "props": {}, "narration":
            "Let me show you the whole problem in one picture. [pause] You see a cat. [pause] "
            "The computer sees this — a grid of numbers. [pause] That is it. There is no cat in "
            "there. No fur, no ears, no whiskers. Only brightness values, row after row. [pause] "
            "This distance, between the raw numbers at the bottom and the meaning at the top, "
            "has a name. The semantic gap. [pause] And it is enormous. [pause] Move the cat a "
            "little to the left, and every single number changes. [pause] Dim the lights, and "
            "they all change again. Yet your brain still says, instantly, cat. [pause] The same "
            "object can produce a billion different grids of numbers. [pause] That is what makes "
            "vision so hard. We are not matching pictures. We are trying to find meaning that "
            "survives across endless variation. [pause] The entire history of this field is one "
            "long campaign to cross this gap. [pause] For decades, we tried to cross it by hand, "
            "writing rules ourselves. It barely worked. [pause] Then we discovered how to let "
            "the machine cross it on its own — and everything changed. That is the story we are "
            "about to tell, step by step."},
    ]},

    {"id": "cv-ch02-pixels", "title": "Images Are Numbers", "segments": [
        {"id": "pixels", "variant": "cv_pixels", "props": {}, "narration":
            "So let's start at the very bottom, with the raw material. What actually is a "
            "digital image? [pause] It is a grid of tiny squares called pixels, and every "
            "pixel is just a number. [pause] For a black-and-white image, that number is a "
            "brightness. It runs from zero, which is pure black, to two fifty five, which is "
            "pure white. [pause] Everything in between is a shade of gray. Look at the values "
            "on the grid — that is the actual data the computer stores. Nothing more. [pause] "
            "Now, why does it stop at two fifty five? [pause] Because each pixel is stored in "
            "eight bits of memory, and eight bits can count exactly two hundred and fifty six "
            "different levels, from zero up to two fifty five. [pause] A color image is just "
            "three of these grids stacked on top of each other. [pause] One grid for red, one "
            "for green, one for blue. We call them channels. [pause] Mix those three brightness "
            "values in different amounts, and you can make any color on your screen. [pause] So "
            "a color image is really a block of numbers — height, times width, times three. "
            "[pause] The number of pixels is the resolution. More pixels means more detail, but "
            "also more numbers to process. That trade-off will follow us the whole course. "
            "[pause] And a video? A video is nothing more than a stack of these images, "
            "flipping past at maybe thirty per second. So everything we learn about one frame "
            "applies to video too — just many times a second. "
            "[pause] Let's feel the scale of that. A single twelve-megapixel phone photo holds "
            "over thirty-six million numbers. [pause] And there, in one sentence, is the whole "
            "challenge of this course. [pause] Somewhere inside that wall of thirty-six million "
            "numbers is a cat. [pause] Every technique we learn, from here to the end, is a "
            "smarter and smarter way to read this grid."},
    ]},

    {"id": "cv-ch03-tasks", "title": "What Vision Can Do", "segments": [
        {"id": "tasks", "variant": "cv_tasks", "props": {}, "narration":
            "Before we build anything, let's map out where we are going. [pause] Computer "
            "vision is not one task. It is a whole family of them, and they get harder as we "
            "go. [pause] The simplest is classification. One image goes in, one label comes "
            "out. Is this a cat, or a dog? [pause] That is it — a single answer for the whole "
            "picture. [pause] Next is detection. Now we are not happy with one label. We want "
            "to know what is in the image and where. [pause] Detection draws a box around every "
            "object and names each one. Two people, a dog, a car. [pause] Then comes "
            "segmentation, which is stricter still. [pause] Here we label every single pixel. "
            "This pixel is road. This one is car. This one is sky. [pause] It traces the exact "
            "outline of everything, not just a rough box. [pause] And the family keeps growing. "
            "We can track an object as it moves across a video. [pause] We can estimate pose — "
            "the skeleton and joints of a body. We can even rebuild a scene in three dimensions. "
            "[pause] Notice the pattern. Each task asks for more detail than the one before, "
            "and each one is built on the same foundation underneath. [pause] Keep this map in "
            "your head. As we go, we will unlock these tasks one at a time. [pause] And here is "
            "the punchline you will see again and again — by the end, they will all run on the "
            "same core engine."},
        {"id": "apps", "variant": "cv_apps", "props": {}, "narration":
            "And this is not just an academic exercise on a whiteboard. Vision is already woven "
            "through your daily life. [pause] It is the camera in your phone, finding faces and "
            "locking focus before you even press the shutter. [pause] It is the self-driving "
            "car, reading lanes, signs, and pedestrians many times a second. [pause] It is the "
            "doctor's assistant, quietly flagging a suspicious spot on an X-ray or a "
            "retina scan — sometimes catching what a tired human eye would miss. [pause] It is "
            "the warehouse robot navigating the aisles, the farm drone counting healthy crops "
            "from the air, the factory camera spotting a cracked part as it flies down the "
            "line. [pause] It is how your photo app lets you search your own pictures for the "
            "word beach, and instantly finds them. [pause] Here is the remarkable thing. The "
            "same small handful of ideas powers every one of these. [pause] They are not "
            "separate inventions. They are the same core, pointed at different problems. [pause] "
            "That is exactly what makes this worth learning deeply. [pause] Understand the "
            "engine once, and you understand a technology that is reshaping medicine, transport, "
            "farming, and science all at the same time. [pause] So now let's earn that "
            "understanding — starting with the oldest trick in the book."},
    ]},

    # ============================================================ PART 2 — CLASSICAL
    {"id": "cv-ch04-filters", "title": "Filters", "segments": [
        {"id": "div", "variant": "cv_divider",
         "props": {"n": 2, "title": "Classical Vision", "sub": "hand-built filters — before the networks", "color": CLASSIC},
         "narration":
            "Part two. Classical vision. [pause] Long before neural networks existed, engineers "
            "crossed the semantic gap by hand — with clever mathematical filters. [pause] These "
            "old ideas are not obsolete. They are the bedrock that everything modern is built "
            "on. [pause] So let's roll up our sleeves and see how they actually work."},
        {"id": "filters", "variant": "cv_filters", "props": {}, "narration":
            "The most basic operation in all of vision is the filter. [pause] A filter takes an "
            "image and transforms its numbers to reveal something useful. [pause] Some filters "
            "are simple and work one pixel at a time. [pause] To make an image brighter, just "
            "add a fixed value to every pixel. Watch the numbers on the grid climb together. "
            "[pause] To increase contrast, push the bright pixels brighter and the dark pixels "
            "darker, pulling them apart. [pause] But the truly interesting filters do something "
            "different. They look at a pixel's neighborhood, not just the pixel itself. [pause] "
            "Take blur. [pause] To blur a pixel, you replace it with the average of the pixels "
            "immediately around it. [pause] Do that for every pixel, and sharp edges soften. "
            "[pause] Now, why would anyone want a blurry image? [pause] Because blur removes "
            "noise — those tiny random speckles a camera sensor adds in low light. [pause] "
            "Averaging a neighborhood cancels the random flecks while keeping the real shapes. "
            "[pause] And here is the insight that this whole course turns on. [pause] This one "
            "little move — slide a small window across the image, and combine each neighborhood "
            "into a new value — is the single most important idea in computer vision. [pause] "
            "It has a formal name. Convolution. [pause] And it is so important that it deserves "
            "a chapter entirely to itself."},
    ]},

    {"id": "cv-ch05-convolution", "title": "Convolution", "segments": [
        {"id": "conv", "variant": "cv_conv", "props": {}, "narration":
            "Convolution. If you remember only one idea from this entire course, make it this "
            "one. Everything else is built on top of it. [pause] Let's go slowly. [pause] We "
            "start with a small grid of numbers called a kernel. Here it is just three pixels "
            "by three pixels — a tiny window of nine numbers. [pause] We place that kernel over "
            "the top-left corner of the image. [pause] Now, at this position, we do two things. "
            "[pause] First, we multiply each kernel number by the pixel sitting underneath it. "
            "[pause] Then we add up all nine of those products into a single number. [pause] "
            "That one number is the output for this spot. [pause] Then we slide the kernel one "
            "step to the right, and do it all again. Multiply, sum, write one number. [pause] "
            "Watch it march across the image. Left to right, top to bottom, covering every "
            "position. [pause] When it finishes, we have a brand-new grid of numbers. We call "
            "it a feature map. [pause] Now here is the beautiful part — the part that changes "
            "everything. [pause] The nine numbers inside the kernel decide what it detects. "
            "[pause] Fill the kernel one way, and it lights up on vertical lines. [pause] Fill "
            "it another way, and it responds to horizontal lines. Another, and it finds a "
            "corner, or a spot of a certain color. [pause] The exact same sliding operation, "
            "with different numbers inside, becomes a completely different detector. [pause] "
            "For thirty years, human engineers chose those numbers carefully, by hand. [pause] "
            "And the entire deep learning revolution — the whole thing — comes down to one "
            "move. [pause] Stop choosing the numbers ourselves. Let the machine learn them. "
            "Hold on to that thought. We will come back to it."},
        {"id": "kernels", "variant": "cv_kernels", "props": {}, "narration":
            "Let's really drive home why convolution is so powerful, by trying a few kernels "
            "side by side. [pause] On the left is our source image. Now watch what different "
            "kernels do to it. [pause] The first kernel is all ones. [pause] It just averages "
            "each neighborhood, and the result is a smooth, blurred image. Good for killing "
            "noise. [pause] The second kernel has a big positive number in the center and "
            "negative numbers around it. [pause] It boosts the middle pixel relative to its "
            "neighbors, and the result is a sharpened image — edges pop. [pause] The third "
            "kernel is the difference kernel. [pause] It subtracts the neighbors from the "
            "center. In a flat region, that cancels to zero and comes out dark. But at an "
            "edge, it fires — and we get a clean outline. [pause] Look at what just happened "
            "here, because it is the whole idea in one picture. [pause] The operation never "
            "changed. It was the same slide, the same multiply, the same sum, every time. "
            "[pause] The only thing that changed was the nine numbers inside the little window. "
            "[pause] Blur, sharpen, edges — three completely different results, from one "
            "operation. [pause] So imagine having not three kernels, but hundreds of them. And "
            "instead of choosing their numbers yourself, you let the network discover exactly "
            "the kernels it needs. [pause] That is a convolutional neural network. And that is "
            "where we are heading."},
    ]},

    {"id": "cv-ch06-edges", "title": "Edge Detection", "segments": [
        {"id": "edges", "variant": "cv_edges", "props": {}, "narration":
            "Let's make convolution concrete with its most famous job — finding edges. [pause] "
            "First, what is an edge? [pause] An edge is simply a place where brightness changes "
            "sharply. It is the border where an object stops and the background begins. [pause] "
            "The fur of the cat is bright. The background behind it is dark. Where they meet, "
            "the numbers jump. That jump is the edge. [pause] There is a classic pair of "
            "kernels built to catch exactly this, called the Sobel filters. [pause] One of them "
            "responds to horizontal changes in brightness. The other responds to vertical "
            "changes. [pause] Now watch what happens as we slide them across the cat. [pause] "
            "In a flat region — say, the middle of a patch of fur — neighboring pixels are all "
            "about the same. The filter multiplies and sums, and the result comes out near "
            "zero. Dark. Nothing here. [pause] But right at the outline, where dark meets "
            "bright, the filter fires hard, and the output glows bright. [pause] The final "
            "picture is an outline drawing of the cat — its whole silhouette pulled out of the "
            "image by nothing but multiply and add. [pause] And there is more hiding in here. "
            "[pause] Combine the horizontal and vertical filters, and you get two things at "
            "once. The strength of the edge — how sharp the change is. [pause] And its "
            "direction — which way the edge points. [pause] Classic detectors like Canny use "
            "exactly this to trace thin, clean contours. [pause] Here is a deeper reason edges "
            "matter so much. The flat regions of an image are, in a sense, boring and "
            "predictable. [pause] The information — the structure — lives at the edges. That is "
            "why so many vision methods start by finding them. [pause] Stop and appreciate what just "
            "happened. [pause] We took raw, meaningless brightness, and produced something with "
            "structure. Edges. [pause] Edges are the very first rung on the ladder that climbs "
            "from pixels up to perception. [pause] And the way we climb the rest of that ladder "
            "is by stacking these operations, one on top of another."},
    ]},

    {"id": "cv-ch07-handcrafted", "title": "The Handcrafted Era", "segments": [
        {"id": "classic", "variant": "cv_classic", "props": {}, "narration":
            "So for decades, this was the master plan. Chain clever filters together, by hand, "
            "into a pipeline. [pause] First find the edges. [pause] Then group nearby edges "
            "into corners and blobs. [pause] Then describe the pattern of those corners around "
            "each interesting point, and turn it into a compact signature. [pause] Famous, "
            "brilliant methods did exactly this. You may hear their names — SIFT, and HOG. "
            "[pause] They were carefully engineered features, designed by very smart people "
            "over many years. [pause] And for a while, they genuinely worked. [pause] They gave "
            "us panorama stitching on our cameras. The first face detectors in point-and-shoot "
            "cameras. Early object recognition. [pause] SIFT, for instance, was genuinely "
            "clever — it found keypoints that survived zooming and rotation, so you could match "
            "the same object across different photos. [pause] People even built early image "
            "search this way, by collecting an image's features into a bag of visual words. "
            "[pause] But this whole approach slammed into a "
            "hard ceiling. [pause] A feature hand-tuned to recognize a cat in bright daylight "
            "would simply fail at night. [pause] Change the camera angle. Change the lighting. "
            "Add a cluttered background, or a partly hidden object. And the careful pipeline "
            "would crumble. [pause] The problem was fundamental. The real world has far too "
            "much variety to ever cover with hand-written rules. [pause] Engineers would spend "
            "years crafting features for one narrow problem, and end up with something brittle "
            "that broke the moment conditions shifted. [pause] It was clear the field needed a "
            "completely different idea. [pause] Not humans painstakingly designing features. "
            "[pause] But a system that could learn the right features by itself, directly from "
            "examples. [pause] That idea is the deep learning revolution — and it begins right "
            "now."},
    ]},

    # ============================================================ PART 3 — DEEP LEARNING
    {"id": "cv-ch08-why-cnn", "title": "Why CNNs", "segments": [
        {"id": "div", "variant": "cv_divider",
         "props": {"n": 3, "title": "Deep Learning", "sub": "networks that learn their own filters", "color": NEURAL},
         "narration":
            "Part three. Deep learning. [pause] This is the turning point. Here the machine "
            "stops using the filters we hand it, and starts inventing its own — learned from "
            "data, not designed by us. [pause] This single shift is what changed computer "
            "vision forever. Let's understand exactly why it works."},
        {"id": "whycnn", "variant": "cv_whycnn", "props": {}, "narration":
            "You might reasonably ask — why invent a special kind of network for images? "
            "[pause] Why not just take that grid of pixels, flatten it into one long list, and "
            "feed it into an ordinary neural network? Connect every pixel to every neuron, and "
            "let it figure everything out. [pause] There are two problems, and they are both "
            "serious. [pause] The first problem is size. [pause] A modest image has hundreds of "
            "thousands of pixels. If you connect every one of them to every neuron in the next "
            "layer, you get billions of connections in a single layer. [pause] That is far too "
            "many numbers to store or train. It would be hopeless. [pause] The second problem "
            "is that this approach throws away two obvious truths about images. [pause] Truth "
            "number one — meaning is local. [pause] To find an eye, you only need to look at a "
            "small patch of the picture. You do not need the opposite corner. [pause] Truth "
            "number two — a pattern means the same thing wherever it appears. [pause] An edge "
            "in the top-left corner looks exactly like an edge in the bottom-right corner. "
            "[pause] So why on earth would we learn to detect it twice, in two separate places? "
            "[pause] The convolutional neural network is designed to respect both truths. "
            "[pause] It uses small filters that only look at little local patches. That handles "
            "locality. [pause] And it slides the very same filter across the entire image, "
            "reusing it everywhere. That handles repetition. [pause] The payoff is huge. Far "
            "fewer numbers to learn, and every detector automatically works no matter where the "
            "pattern shows up. [pause] That is the trick that finally made vision learnable at "
            "scale."},
    ]},

    {"id": "cv-ch09-cnn-anatomy", "title": "Anatomy of a CNN", "segments": [
        {"id": "cnn", "variant": "cv_cnn", "props": {}, "narration":
            "So let's look at the shape of a full convolutional network — a C N N. [pause] It "
            "is a stack of layers, and the image flows through them, left to right, "
            "transforming as it goes. [pause] The first layer is a set of learned convolution "
            "filters. [pause] Each filter slides across the image, exactly as we saw, and "
            "produces its own feature map. Many filters, so many feature maps side by side. "
            "[pause] The early filters tend to learn simple things — edges, and patches of "
            "color. The raw alphabet of vision. [pause] Now, after every convolution, each "
            "number passes through an activation function. [pause] The most common one is "
            "called ReLU, and it could not be simpler. If a number is positive, keep it. If it "
            "is negative, replace it with zero. [pause] That tiny bend is doing something "
            "essential. [pause] Without it, stacking layers would just be adding straight lines "
            "to straight lines, and the whole network could only ever learn simple, straight "
            "relationships. [pause] That little kink is what lets the network bend and curve "
            "and learn genuinely complex shapes. [pause] Then we stack another convolution "
            "layer on top of the first. [pause] This second layer combines the simple features "
            "below it into richer ones — edges into corners, corners into textures. [pause] "
            "Layer after layer, the picture gets smaller in size, but deeper in meaning. [pause] "
            "And at the very end, an ordinary fully connected layer reads the final, rich "
            "features and produces the answer — the class scores. [pause] Convolve, activate, "
            "repeat. That is the engine. [pause] Now let's zoom in on the step that shrinks the "
            "image along the way."},
        {"id": "pool", "variant": "cv_pool", "props": {}, "narration":
            "In between convolution layers, we almost always add a step called pooling. [pause] "
            "Pooling shrinks the feature map, and its whole job is to summarize. [pause] The "
            "most common form is max pooling. [pause] You take a small window — let's say two "
            "pixels by two pixels — and from those four numbers, you keep only the largest one. "
            "[pause] Watch it. Four numbers go in. The single strongest one survives. The other "
            "three are thrown away. [pause] Slide that window across the whole map, and the map "
            "shrinks to half the width and half the height. That is four times fewer numbers to "
            "carry forward. [pause] But why keep the maximum, of all things? [pause] Because "
            "the maximum answers a genuinely useful question. Was this feature present anywhere "
            "in this little region? [pause] A high value means yes, strongly, somewhere in "
            "here. [pause] And keeping only that fact gives us something precious — a little "
            "tolerance to position. [pause] If the cat's ear shifts a few pixels to the side, "
            "the pooled summary barely changes at all. [pause] The network stops caring about "
            "the exact pixel, and starts caring about the presence of the pattern. [pause] So "
            "pooling makes the network cheaper to run and more robust at the same time. [pause] "
            "Convolution finds the patterns. Pooling zooms out. [pause] Alternate them again "
            "and again, and you build a pyramid — from fine local detail at the bottom, up to "
            "the big picture at the top."},
    ]},

    {"id": "cv-ch10-hierarchy", "title": "Feature Hierarchies", "segments": [
        {"id": "hier", "variant": "cv_hier", "props": {}, "narration":
            "Now here is the single most beautiful idea in all of deep vision. If you take one "
            "insight home, let it be this one. [pause] When you stack these layers deep, "
            "something extraordinary emerges on its own — a hierarchy of understanding. [pause] "
            "And we do not have to take this on faith. We can actually peek inside a trained "
            "network and see what each layer has learned to respond to. [pause] So let's climb "
            "it, layer by layer. [pause] The very first layer learns edges and simple colors. "
            "The raw vocabulary of seeing — little strokes and gradients. [pause] The next "
            "layer up takes those edges and combines them into textures and corners. Simple "
            "shapes made from simpler ones. [pause] Go one layer deeper, and it assembles those "
            "shapes into object parts. [pause] An eye. A wheel. A petal. A patch of skin. "
            "[pause] Deeper still, and whole objects light up. A complete face. A car. A cat. "
            "[pause] Now, read this next sentence slowly, because it is the whole point. [pause] "
            "Nobody programmed the concept of an edge. Nobody defined an eye, or a face. [pause] "
            "The network discovered all of it, entirely on its own, just by trying over and "
            "over to get the final answer right. [pause] It built its own ladder, from raw "
            "pixels all the way up to meaning. [pause] This is precisely the thing we could "
            "never do by hand, no matter how clever we were. [pause] And it is the reason deep "
            "learning did not just improve computer vision — it completely swept the field. "
            "[pause] Simple parts, combined layer by layer, into understanding."},
        {"id": "receptive", "variant": "cv_receptive", "props": {}, "narration":
            "Here is a question that puzzles a lot of people. [pause] If every convolution "
            "filter only ever looks at a tiny three-by-three patch, how can the network "
            "possibly recognize a whole cat, which fills the entire image? [pause] The answer "
            "is one of the most elegant ideas in deep learning, and it is called the receptive "
            "field. [pause] Follow one neuron, deep in the network, and ask — how much of the "
            "original image does it actually depend on? [pause] A neuron in the very first "
            "layer sees just a three-by-three patch. Truly local. [pause] But a neuron in the "
            "second layer looks at a patch of first-layer neurons — and each of those already "
            "saw a patch of their own. [pause] So the second-layer neuron indirectly sees "
            "roughly a seven-by-seven region. [pause] Go to the third layer, and the "
            "highlighted region on the input grows again, to around fifteen by fifteen. [pause] "
            "Keep stacking, and a deep neuron ends up influenced by almost the entire image. "
            "[pause] Watch the highlighted window expand as we go deeper. [pause] This is the "
            "resolution of our puzzle. [pause] Early layers see fine local detail. Deep layers "
            "see broad global context. [pause] The network never needed a giant filter. It "
            "just needed depth. Small windows, stacked, quietly add up to the whole picture."},
    ]},

    {"id": "cv-ch11-imagenet", "title": "ImageNet & Classic Networks", "segments": [
        {"id": "imagenet", "variant": "cv_imagenet", "props": {}, "narration":
            "Big ideas need a proving ground — a place to test who is really best. For computer "
            "vision, that place was ImageNet. [pause] ImageNet is a giant dataset. Over "
            "fourteen million images, each one labeled by hand, spread across a thousand "
            "different categories. [pause] A thousand kinds of dog, mushroom, vehicle, and "
            "everything else. [pause] Every year, research teams competed to classify these "
            "images, and the error rate on that competition became the official scoreboard for "
            "the whole field. [pause] Lower error was better. [pause] For years, the "
            "hand-crafted methods from part two crawled along, stuck at roughly twenty-five "
            "percent error. One in four wrong. Progress was slow and grinding. [pause] Then, in "
            "twenty twelve, everything changed in a single afternoon. [pause] A deep "
            "convolutional network, called AlexNet, entered the competition — and the error "
            "rate collapsed. [pause] It was not a modest improvement. It was a landslide, and "
            "it converted the entire research community almost overnight. [pause] What followed "
            "was a furious race to go deeper. [pause] A network called VGG showed the power of "
            "stacking many small three-by-three filters. [pause] But let's pause on why twenty "
            "twelve, of all years, was the moment. [pause] Three things finally lined up at "
            "once. [pause] The core ideas were actually decades old. What was new was data — "
            "ImageNet finally gave them millions of labeled examples to learn from. [pause] And "
            "hardware — researchers found that graphics cards, G P Us, built for video games, "
            "could train these networks tens of times faster. [pause] Ideas, data, and compute, "
            "arriving together. That is the combination that set off the explosion. [pause] "
            "Then ResNet solved a stubborn "
            "problem. Very deep networks had become almost impossible to train. [pause] ResNet "
            "added a clever shortcut — a skip connection that lets the signal jump straight "
            "past a group of layers. [pause] That one trick made it possible to train networks "
            "over a hundred layers deep, without them falling apart. [pause] And with that, "
            "accuracy on ImageNet passed the human benchmark. [pause] In just a few short "
            "years, machines went from clumsy to genuinely superhuman at naming what is in a "
            "picture. [pause] So next, the natural question — how do we actually train one of "
            "these?"},
    ]},

    {"id": "cv-ch12-training", "title": "Training a Vision Model", "segments": [
        {"id": "train", "variant": "cv_train", "props": {}, "narration":
            "So how does a network actually learn those millions of filter numbers? [pause] "
            "Through a loop. And it is essentially the same loop for nearly every model in deep "
            "learning. [pause] It begins knowing absolutely nothing. Every filter is set to "
            "random numbers. [pause] We show it a training image, and it makes a guess. Early "
            "on, that guess is basically a coin flip. It says dog when the answer is cat. "
            "[pause] Now we measure exactly how wrong it was, with a single number called the "
            "loss. [pause] A high loss means a badly wrong guess. A low loss means it was "
            "close. Our entire goal is to push that number down. [pause] Then comes the truly "
            "clever step — backpropagation. [pause] Backpropagation works backward through the "
            "network and figures out, for every single weight, how it nudged the loss up or "
            "down. [pause] Then we adjust every weight a tiny amount in the direction that would "
            "have made the loss smaller. [pause] One image barely moves anything. But do this "
            "millions of times, over millions of images, and watch the loss curve slide "
            "downward. The guesses get better, and better, and better. [pause] Two more tricks "
            "make this practical in the real world. [pause] The first is data augmentation. "
            "[pause] Flip, rotate, crop, and recolor your training images, so the model sees "
            "endless variety and cannot simply memorize. It has to actually generalize. [pause] "
            "The second trick is enormous, and you will use it constantly. It is called "
            "transfer learning. [pause] Do not start from random numbers at all. [pause] Take a "
            "network already trained on ImageNet — one that already knows edges, textures, and "
            "shapes — and simply fine-tune it on your specific problem. [pause] Because it "
            "starts with real visual knowledge, it can learn your task from just a few hundred "
            "examples, instead of millions. [pause] Alright. Enough theory. Let's open a code "
            "editor and build one for real."},
        {"id": "augment", "variant": "cv_augment", "props": {}, "narration":
            "Let's slow down on that first trick, augmentation, because it matters more than "
            "people expect. [pause] A deep network is greedy. Give it a small dataset, and it "
            "will happily memorize every image instead of learning the real pattern. [pause] "
            "We call that overfitting, and augmentation is our main defense. [pause] The idea "
            "is simple. Take each training image, and make many altered copies of it — all "
            "still clearly the same thing. [pause] Flip it left to right. A cat is still a cat. "
            "[pause] Rotate it a little. Still a cat. [pause] Crop in and zoom. Still a cat. "
            "[pause] Change the brightness, as if the lighting were different. Still a cat. "
            "[pause] Shift the colors slightly. Still a cat. [pause] From one photo, we have "
            "manufactured half a dozen. [pause] And crucially, the label never changes. [pause] "
            "The network now sees the cat from many angles, in many lights, and it can no "
            "longer cheat by memorizing exact pixels. [pause] It is forced to learn what "
            "actually makes a cat a cat. [pause] Best of all, augmentation is nearly free — it "
            "is just a few cheap transforms on data you already have. [pause] It is one of the "
            "highest-value habits in all of practical computer vision."},
        {"id": "transfer", "variant": "cv_transfer", "props": {}, "narration":
            "And now the second trick, transfer learning — which is honestly how almost all "
            "real vision work gets done today. [pause] Think about what a network trained on "
            "ImageNet already knows. [pause] Its early layers learned edges. Deeper ones "
            "learned textures, then object parts, then whole objects. [pause] That knowledge is "
            "general. Edges and textures are useful for almost any image task, not just the one "
            "it was trained on. [pause] So why throw it away? [pause] Here is the move. Take "
            "that pretrained network and freeze its backbone — lock those learned filters in "
            "place, so training does not touch them. [pause] Then bolt a small new head onto "
            "the end — a fresh layer for your specific classes. [pause] Maybe healthy versus "
            "diseased leaves. Maybe your company's products. [pause] And you train only that "
            "little head. [pause] Because the hard part, understanding images in general, is "
            "already done, you can learn your task from just a few hundred labeled examples, in "
            "minutes, on a single computer. [pause] Notice this is the exact same idea as "
            "fine-tuning a large language model. [pause] Reuse enormous general knowledge, and "
            "specialize it cheaply. [pause] That is why you almost never start from scratch."},
    ]},

    # ============================================================ PART 4 — CODE
    {"id": "cv-ch13-code-pytorch", "title": "Code: A CNN in PyTorch", "segments": [
        {"id": "div", "variant": "cv_divider",
         "props": {"n": 4, "title": "Let's Write It", "sub": "a working CNN in PyTorch, end to end", "color": NEURAL},
         "narration":
            "Part four. Let's write it. [pause] Everything we have learned so far, now in real, "
            "running code. [pause] We are going to build a small convolutional network in "
            "PyTorch — the most popular framework for this — and take it all the way. [pause] "
            "Load the data. Define the model. Train it. And make a real prediction. [pause] "
            "Four short files. Don't worry about memorizing the syntax. Just follow the shape of "
            "it, and watch our theory turn into code."},
        {"id": "setup", "variant": "cv_code_setup", "props": {}, "narration":
            "Step one. Get the images into the model. [pause] At the top, we import PyTorch, "
            "and its dedicated vision toolkit called torchvision. [pause] Next, we build "
            "something called a transform. Think of it as a small assembly line that every "
            "image passes through. [pause] The first stage, ToTensor, converts the picture into "
            "a tensor — a grid of numbers PyTorch can work with — and scales the pixels from "
            "the zero to two fifty five range down into a clean zero to one range. [pause] The "
            "second stage, Normalize, re-centers those values around zero, which helps training "
            "run smoothly and quickly. [pause] Now we load an actual dataset. We use C I F A R "
            "ten — a classic collection of sixty thousand small color photos, sorted into ten "
            "classes like cat, dog, ship, and truck. [pause] Look at the shape on the right. "
            "One image becomes a tensor of three by thirty-two by thirty-two. [pause] That is "
            "three color channels, each thirty-two pixels wide and thirty-two tall. [pause] "
            "Finally, the DataLoader. Its job is to hand us the images in shuffled batches of "
            "sixty-four at a time. [pause] Why batches? Because updating the model on sixty-four "
            "images at once is far faster and steadier than one at a time. [pause] So each step "
            "of training, the model receives a stack shaped sixty-four, by three, by "
            "thirty-two, by thirty-two. The data is ready to flow."},
        {"id": "model", "variant": "cv_code_model", "props": {}, "narration":
            "Step two. Define the network itself. [pause] In PyTorch, a model is a class, and "
            "we will call ours SmallCNN. [pause] It has two parts. First, in the setup method, "
            "we simply list the layers we are going to use. [pause] We create two convolution "
            "layers. Conv one takes the three color channels coming in, and produces "
            "thirty-two feature maps. [pause] Conv two takes those thirty-two maps and produces "
            "sixty-four richer ones. [pause] We add a max-pool layer to shrink things down, and "
            "one final linear layer that will output ten numbers — one score for each of our "
            "ten classes. [pause] The second part is the forward method, and this is where the "
            "data actually flows. It reads top to bottom. [pause] Apply conv one, then the "
            "ReLU activation, then pooling. [pause] Follow the shapes on the right. The image "
            "goes from three by thirty-two by thirty-two, down to thirty-two channels at "
            "sixteen by sixteen. [pause] We run the same trio again with conv two, and land at "
            "sixty-four channels at eight by eight. [pause] Then we flatten that block into one "
            "long vector, feed it through the linear layer, and out come our ten class scores. "
            "[pause] And that is the whole architecture. Every idea from part three — "
            "convolution, activation, pooling, a final classifier — sitting in about a dozen "
            "lines of code."},
        {"id": "train", "variant": "cv_code_train", "props": {}, "narration":
            "Step three. Train it. This is where the loop from the last chapter becomes real. "
            "[pause] First we set up three things. We create the model, an optimizer, and a "
            "loss function. [pause] The optimizer here is called Adam. It is the machinery that "
            "actually adjusts the weights. The learning rate — one times ten to the minus three "
            "— controls how big each adjustment is. [pause] The loss function is cross-entropy "
            "loss, the standard choice for classification. It measures how wrong each "
            "prediction was. [pause] Now the loop itself. For each batch of images and their "
            "true labels, we run four lines. These four lines are the beating heart of all deep "
            "learning. [pause] One. Zero out the old gradients from the last step. [pause] Two. "
            "Run the images forward through the model to get predictions. [pause] Three. "
            "Compute the loss — how wrong those predictions are. [pause] Four. Call loss dot "
            "backward. This is backpropagation, and it fills in how every single weight affected "
            "the error. [pause] Then optimizer step nudges all those weights in the better "
            "direction. [pause] Now watch the loss curve on the right as the loop runs. See it "
            "falling. [pause] That falling line is not a decoration. It is the network actually "
            "learning, in real time. [pause] Repeat over the whole dataset several times, and "
            "our model is trained."},
        {"id": "infer", "variant": "cv_code_infer", "props": {}, "narration":
            "Step four. The payoff — actually using the model on a new image. [pause] First we "
            "switch the model into eval mode, and wrap everything in no-grad. [pause] Together, "
            "these tell PyTorch we are only making predictions now, not learning. It can skip "
            "all the training bookkeeping, which makes it faster and lighter. [pause] We pass in "
            "a fresh image. The little unsqueeze adds the batch dimension the model expects, "
            "turning one image into a batch of one. [pause] Out come ten raw numbers, called "
            "logits. [pause] They are hard to read directly, so we run softmax, which turns "
            "those ten numbers into clean probabilities that add up to one hundred percent. "
            "[pause] Then argmax simply picks the index of the biggest probability. [pause] "
            "Look at the bars on the right. Cat, ninety-two percent. Everything else, tiny. "
            "[pause] We look up that index in our list of class names, print it, and the "
            "program says — cat. [pause] Take a second to appreciate this. [pause] That is a "
            "complete, working computer vision model. From raw pixels, all the way to a named "
            "answer, in well under a hundred lines of code. [pause] Everything that comes after "
            "this in the course is just making this same idea bigger, and smarter, and more "
            "capable."},
    ]},

    # ============================================================ PART 5 — CORE TASKS
    {"id": "cv-ch14-classification", "title": "Classification", "segments": [
        {"id": "div", "variant": "cv_divider",
         "props": {"n": 5, "title": "The Core Tasks", "sub": "classify · detect · segment · recognize", "color": GREEN},
         "narration":
            "Part five. The core tasks. [pause] We have built an engine — a network that turns "
            "pixels into meaning. Now let's point it at the real jobs of computer vision. "
            "[pause] Finding what is in an image, and exactly where. It all begins with the "
            "simplest task of them all."},
        {"id": "classify", "variant": "cv_classify", "props": {}, "narration":
            "Classification. One image in, one answer out. It is the task we already solved in "
            "code, so let's look at what is really happening. [pause] The picture flows into the "
            "backbone — the C N N, or a transformer — the very engine we just built together. "
            "[pause] The backbone's job is to turn raw pixels into a compact, rich set of "
            "features that capture what the image contains. [pause] Then a final step, called "
            "softmax, converts those features into a probability for every possible class. "
            "[pause] Look at the bars on the right. Cat, ninety-one percent. Dog, six. Fox, "
            "two. Rabbit, one. [pause] Notice they always add up to one hundred percent. [pause] "
            "The model is not certain — it is spreading its confidence across the options, and "
            "here it is putting almost all of it on cat. [pause] We take the top one, and that "
            "is our prediction. [pause] Now, a subtle but important point about how we grade "
            "this. [pause] Sometimes we use top-one accuracy — was the single best guess "
            "exactly right? [pause] But often we use top-five accuracy — was the correct answer "
            "anywhere in the model's top five guesses? [pause] Why be so lenient? Because "
            "ImageNet has a thousand classes, including a hundred breeds of dog that even a "
            "human would struggle to tell apart. [pause] Top-five is a fairer test of whether "
            "the model basically understood the image. [pause] And that spread of confidence "
            "across classes is genuinely useful — a model that says fifty-one percent should be "
            "trusted very differently from one that says ninety-nine. [pause] This looks humble, "
            "but do not underestimate it. It is "
            "the foundation for everything else. [pause] Quality control on a factory line is "
            "classification. Content moderation is classification. Sorting medical images for "
            "triage is classification. [pause] And most importantly of all — that same backbone "
            "lives inside every harder task we are about to meet. [pause] Master "
            "classification, and you have mastered the engine that drives the whole field."},
    ]},

    {"id": "cv-ch15-detection", "title": "Object Detection", "segments": [
        {"id": "detect", "variant": "cv_detect", "props": {}, "narration":
            "Classification tells you what is in a picture. Detection tells you what, and "
            "exactly where. [pause] Now we want a tight box around every object, each one with "
            "a label and a confidence score. [pause] The most famous approach has a great name "
            "— YOLO. It stands for you only look once. [pause] Here is the idea. YOLO lays a "
            "grid over the whole image. [pause] And every single cell in that grid predicts a "
            "few things at once — candidate boxes, a class, and how confident it is — all in "
            "one single pass through the network. [pause] But that produces a flood. Thousands "
            "of overlapping boxes, many of them guessing at the same object. Look at all that "
            "clutter. [pause] So we clean it up with a step called non-max suppression. [pause] "
            "For each cluster of boxes piled on the same object, we keep only the most "
            "confident one, and delete all the rest. [pause] Watch the duplicates vanish, "
            "leaving just the clean, final boxes — person, dog, traffic light, car. [pause] And "
            "here is the headline that makes YOLO special. [pause] All of this happens in a "
            "single forward pass, at well over a hundred frames per second. [pause] That is "
            "fast enough to run live, on streaming video, in real time. [pause] And that speed "
            "is exactly why detection is the workhorse behind self-driving cars, security "
            "cameras, and automated sports analysis. [pause] When you need to know where, "
            "instantly, this is the tool you reach for. [pause] There is also a slower, more "
            "careful family of detectors, called R-CNN, for when you can trade speed for a "
            "little extra accuracy."},
        {"id": "track", "variant": "cv_track", "props": {}, "narration":
            "Detection works on a single frame. But the world moves, and video is just a "
            "stream of frames. [pause] So how do we follow a specific object through time? That "
            "task is called tracking. [pause] The naive approach is to run detection on every "
            "frame, one at a time. [pause] But that gives you fresh, anonymous boxes each "
            "frame. It has no memory. It cannot tell you that the car in this frame is the same "
            "car as the last one. [pause] Tracking adds that memory. [pause] Step one, still "
            "detect every frame. [pause] Step two, match this frame's boxes to the previous "
            "frame's objects, usually by which ones are closest and look the most alike. [pause] "
            "And with a good match, each object keeps a stable identity — an I D — as it moves. "
            "[pause] Watch the walker, the cyclist, and the car. Each keeps its own numbered "
            "box and leaves a little trail as it crosses the scene. [pause] There is a third "
            "piece, called re-identification, or re-I D. [pause] When an object is briefly "
            "hidden behind something and reappears, re-I D recognizes it and restores the same "
            "identity, instead of inventing a new one. [pause] This is the engine behind "
            "traffic monitoring, sports analytics that follow every player, and any system that "
            "needs to count or follow things over time."},
        {"id": "metrics", "variant": "cv_metrics", "props": {}, "narration":
            "Before we move on, one honest question. How do we even know if a detector is any "
            "good? [pause] Saying it works is not a number. So the field built precise ways to "
            "keep score. [pause] Start with a single box. How do we grade a predicted box "
            "against the true one? [pause] We use a measure called I O U — intersection over "
            "union. [pause] Take the area where the two boxes overlap, and divide it by the "
            "total area they cover together. [pause] Watch the number. A perfect overlap gives "
            "one. No overlap gives zero. [pause] We usually count it as a correct hit if the I "
            "O U is above one half. [pause] Next, two words you must not confuse — precision "
            "and recall. [pause] Precision asks — of everything the model flagged, how much was "
            "actually right? [pause] Recall asks — of everything that was really there, how "
            "much did the model find? [pause] There is always a trade-off between them, set by "
            "how cautious you make the model. [pause] Finally, we roll it all into one headline "
            "number — mean average precision, or m A P. [pause] It scores the model on every "
            "class, then averages. Look at the bars — a strong score on cats and dogs, weaker "
            "on rare signs, and the mean at the bottom. [pause] When you read that a detector "
            "scores, say, zero point five m A P, this is exactly what that means."},
    ]},

    {"id": "cv-ch16-segmentation", "title": "Segmentation & Segment Anything", "segments": [
        {"id": "segment", "variant": "cv_segment", "props": {}, "narration":
            "A box is useful, but it is rough. It always includes background in the corners. "
            "Sometimes you need the exact shape of a thing. [pause] That is segmentation — "
            "labeling every single pixel in the image. [pause] And it comes in two flavors, so "
            "let's be precise about the difference. [pause] The first is semantic segmentation. "
            "It paints every pixel with its class. All the pixels of people get one color. The "
            "road gets another. The sky gets another. [pause] But notice its limit — it does "
            "not separate individuals. Two people standing together blur into one single blob "
            "of the person color. [pause] The second flavor fixes exactly that. Instance "
            "segmentation. [pause] Now person number one and person number two each get their "
            "own separate mask, even though they are the same class. A method called Mask R-CNN "
            "does this. [pause] So how does a network paint a clean mask in the first place? "
            "[pause] Very often, with a U-shaped design called U-Net. [pause] It first shrinks "
            "the image down, step by step, to understand what is in it. Then it grows it back "
            "up to full resolution, to paint the answer pixel by pixel. [pause] The clever part "
            "is the skip connections — those shortcuts across the U. [pause] They carry the "
            "fine, sharp detail from the early layers straight over to the end, so the final "
            "outline stays crisp instead of blurry. [pause] This is the absolute favorite tool "
            "of medical imaging — outlining an organ, or the precise boundary of a tumor, one "
            "pixel at a time. [pause] Remember the difference. Detection draws the box. "
            "Segmentation traces the outline."},
        {"id": "sam", "variant": "cv_sam", "props": {}, "narration":
            "Recently, segmentation took a giant leap forward — and it came from a foundation "
            "model. [pause] Meet Segment Anything, usually just called SAM. [pause] Here is the "
            "shift in thinking. Instead of training a fresh, specialized model for every new "
            "dataset, we train one single, enormous model — on a truly colossal scale. [pause] "
            "SAM was trained on over one billion masks. [pause] And once you have a model like "
            "that, you do not retrain it. You simply prompt it, like you would prompt a "
            "chatbot. [pause] Click a single point on an object. Or drag a rough box around it. "
            "Or sketch a crude shape. [pause] And SAM instantly returns a clean, precise mask — "
            "even for objects it never explicitly saw during training. [pause] That ability, to "
            "handle brand-new things with no extra training, is called zero-shot. [pause] Click "
            "the cat, and get the cat. Click the plant, and get the plant. Watch it work. "
            "[pause] Its successor, SAM two, does the very same thing across an entire video — "
            "you select an object once, and it tracks and masks it, frame after frame. [pause] "
            "And this is the single biggest shift happening across all of computer vision right "
            "now. [pause] From training a small, narrow model for every task, to prompting one "
            "giant, pretrained model for almost any task. [pause] Hold on to that idea. It is "
            "going to return again and again for the rest of this course."},
    ]},

    {"id": "cv-ch17-faces", "title": "Faces, Embeddings & Reading Text", "segments": [
        {"id": "face", "variant": "cv_face", "props": {}, "narration":
            "Now a task that feels like pure magic, but rests entirely on one simple, powerful "
            "idea — face recognition. [pause] Let's think about why the obvious approach fails. "
            "[pause] The naive plan would be to train a classifier on every person in the "
            "world. But there are billions of people, and new ones you have never seen. It is "
            "completely impossible. [pause] So we do something much cleverer. [pause] First, a "
            "pipeline finds the face in the image, marks its landmarks — the corners of the "
            "eyes, the nose, the mouth — and rotates it to a standard, straight-on position. "
            "[pause] Then comes the key part. An embedding network turns that aligned face into "
            "a list of numbers. [pause] A vector. Think of it as a fingerprint made of, say, "
            "five hundred and twelve numbers. [pause] And here is the trick that makes it all "
            "work. [pause] The network is trained so that photos of the same person always land "
            "at nearby vectors, and photos of different people land far apart. [pause] So now, "
            "to check whether two faces match, we do not classify anything. [pause] We just "
            "measure the distance between their two vectors. [pause] Same person, in a "
            "completely new photo? The vectors sit close together. The distance is small. It is "
            "a match. [pause] A different person entirely? The vectors are far apart. The "
            "distance is large. No match. [pause] And the real beauty is this — you can enroll "
            "a brand-new person with a single photo, and never retrain the model. Their photo "
            "just becomes one more vector to compare against. [pause] This idea, of turning "
            "things into comparable vectors, is one of the most powerful ideas in all of "
            "machine learning, and it will come back when we reach language models in a few "
            "chapters."},
        {"id": "ocr", "variant": "cv_ocr", "props": {}, "narration":
            "Here is another everyday task that is secretly two vision problems stacked "
            "together — reading text from an image. We call it O C R, optical character "
            "recognition. [pause] Think about all the text that lives in the visual world. "
            "Street signs. License plates. Receipts. Whole pages of a scanned book. [pause] "
            "None of it arrives as neat digital characters. It arrives as pixels. [pause] So we "
            "solve it in two stages. [pause] Stage one is detection — exactly the idea we just "
            "learned. Find where the text is, and draw a box around each word or line. [pause] "
            "Watch the boxes snap onto the stop sign, the exit sign, the shop hours. [pause] "
            "Stage two is recognition. Take each box, and turn those pixels into actual "
            "characters. [pause] Read the letters out — S, T, O, P — and produce the word "
            "stop. [pause] Notice the shape of this. It is detect, then classify — the same "
            "one-two pattern that runs through so much of computer vision. [pause] And it is "
            "everywhere in the real world. It digitizes old documents, reads plates at parking "
            "gates, scans receipts into your expense app, and powers the live camera "
            "translation that rewrites a foreign menu right in front of your eyes."},
    ]},

    # ============================================================ PART 6 — MODERN & FRONTIER
    {"id": "cv-ch18-vit", "title": "Vision Transformers", "segments": [
        {"id": "div", "variant": "cv_divider",
         "props": {"n": 6, "title": "The Modern Era", "sub": "transformers, multimodal, generative, frontier", "color": GEN},
         "narration":
            "Part six. The modern era. [pause] For nearly a decade, convolution was the "
            "undisputed king of vision. Then an idea, born over in the world of language "
            "models, crossed over — and shook everything up all over again. [pause] That idea "
            "is attention. Let's watch how it learned to see."},
        {"id": "vit", "variant": "cv_vit", "props": {}, "narration":
            "This is the Vision Transformer, usually shortened to ViT. And its core idea is "
            "delightfully strange. [pause] Treat an image exactly like a sentence. [pause] "
            "Let's see how. First, we cut the image up into a grid of small square patches — "
            "say, sixteen pixels by sixteen pixels each. [pause] Watch the patches lift off the "
            "image and line up in a single row. [pause] Each patch now becomes a token — the "
            "very same concept as a word in a sentence. So an image becomes a sentence of "
            "patches. [pause] Then we feed that row of tokens into a standard transformer — "
            "the exact same architecture that powers large language models like the one you may "
            "have chatted with. [pause] The transformer's key mechanism is self-attention. "
            "[pause] Here is what it does. Every patch looks at every other patch, and decides "
            "which ones are relevant to it. [pause] Look at the arcs connecting the patches — a "
            "patch of ear reaching across to a patch of eye, linking distant parts of the image "
            "in a single step. [pause] And this is the crucial difference from a C N N. [pause] "
            "A convolution only ever sees a small local window, and has to build up a global "
            "view slowly, layer by layer. [pause] A transformer sees the entire image at once, "
            "from its very first layer. [pause] There is a catch, and it is worth knowing. ViT "
            "is hungry. It needs a lot of data to learn well, more than a C N N does. [pause] "
            "But give it that data, and it matches or beats convolution outright. [pause] And "
            "the best part — if you already understand attention from language models, then you "
            "already understand ViT. The tokens are just patches instead of words."},
    ]},

    {"id": "cv-ch19-clip-vlm", "title": "CLIP & Vision-Language Models", "segments": [
        {"id": "clip", "variant": "cv_clip", "props": {}, "narration":
            "This is where vision and language finally meet, in a landmark model called CLIP. "
            "[pause] CLIP has two encoders working side by side. [pause] One is an image "
            "encoder — it turns a picture into a vector. [pause] The other is a text encoder — "
            "it turns a sentence into a vector. [pause] Now here is the magic. Both encoders "
            "are trained to write into the same shared space. [pause] A picture of a cat, and "
            "the words a photo of a cat, are pushed to land in nearly the same spot. [pause] "
            "How? CLIP was trained on four hundred million image and caption pairs, scraped "
            "from across the internet. [pause] Its goal, on every pair, was simple. Pull the "
            "matching image and caption close together, and push mismatched ones apart. [pause] "
            "Watch the pictures and their captions drift together in that shared space. [pause] "
            "And once you have this, you unlock a genuine superpower — zero-shot classification. "
            "[pause] Suppose you want to know if an image is a cat. [pause] You do not train a "
            "cat detector. You simply write the sentence a photo of a cat, embed it, embed the "
            "image, and check whether they land close. [pause] With this, you can classify "
            "things the model was never explicitly taught to recognize, just by describing them "
            "in words. [pause] This shared space also powers text-based image search, and it "
            "acts as the eyes inside modern image generators. [pause] One space for pictures "
            "and words together — it is the bridge that every multimodal model walks across."},
        {"id": "vlm", "variant": "cv_vlm", "props": {}, "narration":
            "And that bridge leads directly to where vision has arrived today — vision-language "
            "models, or V L Ms. [pause] The recipe is surprisingly elegant, and it reuses "
            "everything we have built. [pause] Take a vision encoder, the kind CLIP gave us, "
            "and use it to turn an image into a small handful of tokens. [pause] Then feed those "
            "image tokens straight into a large language model, right alongside the words of "
            "your question. [pause] The model now reads one single sequence — part picture, "
            "part text, mixed together. [pause] The language model processes both at once, and "
            "answers back in fluent, natural words. [pause] This is exactly what happens when "
            "you show a photo to GPT-4V, or Gemini, or Claude. [pause] Ask it, what happened on "
            "my desk? And it does not just say cat. [pause] It describes the whole scene, "
            "reasons about the coffee spilled on the laptop, and even suggests what you should "
            "do about it. [pause] Now, step back and look at how far we have traveled. [pause] "
            "We started this course with a grid of numbers that meant absolutely nothing. "
            "[pause] And we have arrived at a model that can look at the world, understand it, "
            "and talk about it in plain language. [pause] Vision stopped being a separate, "
            "walled-off field. [pause] It quietly became something bigger — perception for "
            "general intelligence."},
    ]},

    {"id": "cv-ch20-generative", "title": "Generative Vision", "segments": [
        {"id": "gen", "variant": "cv_gen", "props": {}, "narration":
            "So far, every single model we have built has read images — taken pixels in, and "
            "given meaning out. [pause] Now let's flip the arrow completely, and build a model "
            "that writes images. [pause] This is generative vision. [pause] The first approach "
            "to really work was called a G A N — a generative adversarial network. [pause] The "
            "idea is a duel between two networks. [pause] One, the generator, tries to paint "
            "fake images. The other, the discriminator, tries to tell real from fake. [pause] "
            "They train against each other, and as the critic gets sharper, the forger is "
            "forced to get better, until the fakes look startlingly real. [pause] G A Ns gave "
            "us the first convincing fake faces. But they were fiddly and unstable to train. "
            "[pause] So today's leading approach is something steadier, called diffusion. "
            "[pause] The idea sounds backwards at first, and that is "
            "exactly what makes it so clever. [pause] Start with a real, clean image. Now slowly "
            "add random noise to it, a little at each step, over and over, until the picture is "
            "nothing but pure static. Total snow. [pause] Now — train a network to undo just one "
            "of those steps. To take a slightly noisy image and remove a little bit of the "
            "noise. [pause] That is a much easier task to learn than creating a whole image from "
            "thin air. [pause] But here is the payoff. Once the network can reliably remove a "
            "little noise, you can run the whole process in reverse. [pause] Begin with a canvas "
            "of pure random noise. Then denoise, step by step by step, and watch an image slowly "
            "emerge out of the static. [pause] See it happen on screen — chaos, sharpening into "
            "a cat. [pause] And we can steer the whole thing. [pause] Feed in a text prompt — a "
            "photo of a cat — and that prompt guides every single denoising step, pulling the "
            "result toward the picture you actually asked for. [pause] The very same trick also "
            "powers inpainting, style transfer, and upscaling. [pause] It is the engine humming "
            "inside Stable Diffusion, Midjourney, and DALL-E. [pause] And notice the lovely "
            "symmetry. Recognition climbs up the ladder, from pixels to meaning. Generation "
            "walks that same ladder back down — from meaning, all the way to pixels."},
    ]},

    {"id": "cv-ch21-frontier", "title": "Self-Supervised & 3D", "segments": [
        {"id": "selfsup", "variant": "cv_selfsup", "props": {}, "narration":
            "Let's touch two frontiers that are actively shaping what comes next. [pause] First "
            "— learning without labels. [pause] Every model we have trained so far needed "
            "labeled images. Someone, somewhere, had to sit down and tag them. Cat. Dog. Car. "
            "[pause] And labels are slow, and expensive, and there are never enough of them. "
            "[pause] But raw, unlabeled images? Those are almost free. There are billions upon "
            "billions of them, all over the internet. [pause] Self-supervised learning finds a "
            "way to turn those unlabeled images into their own teacher. [pause] Here is one "
            "beautiful example. Take an image, and hide forty percent of its patches, at "
            "random. [pause] Now ask the network to reconstruct the missing parts, from the "
            "parts it can still see. [pause] To fill in those gaps convincingly, the network is "
            "forced to genuinely learn how objects and the world actually look. [pause] There "
            "was no human label anywhere in that process. Yet the network comes out having "
            "learned rich, general-purpose features. [pause] This is the idea behind methods "
            "like masked autoencoders, and DINO. [pause] Then, once it has that head start, you "
            "fine-tune it on a tiny labeled set for your specific task. [pause] And here is the "
            "connection worth savoring. This is the exact same principle behind large language "
            "models — predict the hidden part. [pause] The same deep idea, now quietly "
            "pretraining the vision backbones of the future."},
        {"id": "3d", "variant": "cv_3d", "props": {}, "narration":
            "The second frontier — escaping the flat image entirely. [pause] The world is three "
            "dimensional, but a photograph is stubbornly flat. It has thrown the depth away. So "
            "how do we get it back? [pause] Modern models can estimate depth from just a single "
            "picture. [pause] Look at the depth map on the left. Bright means near, dark means "
            "far. The model has guessed a distance for every single pixel, from one flat image. "
            "[pause] Methods like Depth Anything do this astonishingly well. [pause] Next, "
            "motion. Optical flow measures how each pixel moved between two frames of a video. "
            "[pause] See the little arrows in the middle — each one shows the direction and "
            "speed that part of the scene is traveling. [pause] That is how models understand "
            "action, and follow objects as they move. [pause] And finally, full three "
            "dimensional reconstruction. [pause] Techniques called NeRF, and Gaussian "
            "splatting, take just a handful of ordinary photos and build a complete 3D scene. "
            "[pause] Then you can fly a virtual camera through it, to brand-new viewpoints the "
            "camera never actually visited. [pause] Robots, augmented reality headsets, and "
            "self-driving cars all depend on this third dimension. [pause] All of it, rebuilt "
            "from nothing but flat, two dimensional frames."},
    ]},

    {"id": "cv-ch22-stack-recap", "title": "The Stack, The Limits & Recap", "segments": [
        {"id": "stack", "variant": "cv_stack", "props": {}, "narration":
            "Before we wrap up, let's get practical for a moment. How do you actually build "
            "vision systems in the real world, today? [pause] Here is the good news. You almost "
            "never start from scratch. [pause] You reach for a well-worn stack of tools. [pause] "
            "There is OpenCV, for classic image operations and reading video. [pause] There is "
            "PyTorch and torchvision, for building and training models — the tools we used in "
            "part four. [pause] A library called Ultralytics gives you full YOLO detection in "
            "about five lines of code. [pause] Hugging Face hosts thousands of pretrained "
            "checkpoints — ViT, CLIP, SAM — all ready to download and use. [pause] Tools like "
            "Roboflow and CVAT help you label your data. [pause] And ONNX and TensorRT optimize "
            "your finished model to run fast on real hardware — a phone, a car, a camera. "
            "[pause] The workflow itself is a pipeline. Collect your data. Label it. Start from "
            "a pretrained model, never from random. [pause] Fine-tune it, using augmentation. "
            "Evaluate it with proper metrics, like mean average precision. Then optimize it and "
            "deploy. [pause] So here is the honest truth about modern computer vision. It is "
            "assembly, far more than it is alchemy. [pause] A pretrained backbone, plus your "
            "own labeled data, plus an afternoon of careful fine-tuning. That is the real job."},
        {"id": "hard", "variant": "cv_hard", "props": {}, "narration":
            "But let's be honest with ourselves. Vision is not a solved problem. [pause] It is "
            "powerful, yes, but it is fragile in ways that are genuinely important to "
            "understand before you deploy it. [pause] Bad lighting, rain, and glare can wreck "
            "accuracy in an instant. [pause] Occlusion — when one object is partly hidden "
            "behind another — confuses models badly, because they never saw the whole thing. "
            "[pause] Then there is the long tail. Models are excellent on common objects they "
            "saw a million times, and starved of data on the rare ones that still matter. "
            "[pause] There is domain shift — a model trained on data from one place, or one "
            "camera, quietly failing when you deploy it somewhere new. [pause] There are "
            "adversarial patterns — a small, carefully crafted sticker, nearly invisible to "
            "you, that can make a model confidently call a banana a toaster. [pause] And most "
            "important of all, there is bias. [pause] If the training data is skewed, the "
            "model's accuracy can be badly uneven across different groups of people. [pause] "
            "That is not a minor bug. It must be measured, and audited, and taken seriously. "
            "[pause] Now, none of these are reasons to despair. [pause] They are the real "
            "engineering frontier — the actual work of putting vision safely into the world. "
            "[pause] Not solved. But, more and more every year, engineerable."},
        {"id": "recap", "variant": "cv_recap", "props": {
            "items": [
                "An image is just a grid of numbers — the semantic gap is the whole problem",
                "Convolution slides small filters to build feature maps",
                "CNNs learn their own filters; depth builds a hierarchy from edges to objects",
                "Train by guessing, measuring loss, and backpropagating — fine-tune, don't start over",
                "Classify, detect, segment, recognize — one backbone, many tasks",
                "Transformers, CLIP and VLMs fused vision with language",
                "Diffusion runs vision in reverse — meaning back to pixels",
            ],
            "closer": "Computer vision — from pixels to perception.",
        }, "narration":
            "So let's pull the whole journey together, in one breath. [pause] An image is just "
            "a grid of numbers, and crossing the gap from those numbers to meaning is the whole "
            "game. [pause] Convolution slides small filters across the image to build feature "
            "maps. That is the core operation underneath everything. [pause] Convolutional "
            "networks learn those filters for themselves, and stacking them deep builds a "
            "hierarchy — from edges, to parts, to whole objects. [pause] We train them by "
            "guessing, measuring the loss, and backpropagating the error — and we fine-tune a "
            "pretrained model instead of ever starting over. [pause] One backbone then powers "
            "many tasks — classify, detect, segment, and recognize. [pause] Transformers, CLIP, "
            "and vision-language models fused vision together with language, giving us machines "
            "that can both look and talk. [pause] And diffusion runs the whole thing in "
            "reverse, turning meaning back into fresh pixels. [pause] You now hold the real map "
            "of this entire field — from a meaningless wall of numbers, all the way up to "
            "perception. [pause] The ideas are simple. The combinations are endless. [pause] So "
            "go build something that sees. [pause] Thanks for watching."},
    ]},
]
