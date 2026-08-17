# -*- coding: utf-8 -*-
"""Solar Panels as a Business — screenplay (English, captions ON).

For a complete beginner: the physics of a panel, how systems are installed on
homes and businesses to cut electricity bills, and how the solar business makes
money (channels + margins). Each chapter renders to its own MP4; all concat into
the master.

A chapter is a list of scene segments: {id, variant, props, narration}.
Narration is SPOKEN language (numbers as words), with [pause] markers (0.6s) after
new terms / big numbers / key ideas. Every on-screen element is mentioned in its
beat, phased to roughly when it is said. See skills/02 + skills/09.

Semantic colors (SolarScenes.A): SUN=#FDB813 · CELL=#38BDF8 · GRID=#34D399 ·
BIZ=#A78BFA · HOT=#FB7185. Money figures are illustrative India-2026 ranges
(PM Surya Ghar subsidy slabs, typical costs/margins), flagged on-screen.
"""

SUN, CELL, GRID, BIZ, HOT = "#FDB813", "#38BDF8", "#34D399", "#A78BFA", "#FB7185"


CHAPTERS = [
    # ================================================================= CH 1 — OPPORTUNITY
    {"id": "solar-ch01-opportunity", "title": "Why Solar, Why Now", "segments": [
        {"id": "title", "variant": "sol_title", "props": {}, "narration":
            "Every roof you have ever seen is sitting under a fortune, and doing nothing with it. "
            "[pause] Over the next hour, I am going to take you from knowing nothing about solar "
            "panels, to understanding exactly how they work, how they get installed, and how people "
            "build a real business selling them. [pause] No jargon you can't follow. We build it up, "
            "step by step."},

        {"id": "roadmap", "variant": "sol_roadmap", "props": {}, "narration":
            "Here is the journey. [pause] First, why solar has suddenly become a real opportunity, on "
            "ordinary rooftops. [pause] Then the science — how a flat panel quietly turns sunlight "
            "into electricity, with no moving parts at all. [pause] Then the system around it — "
            "inverters, and how you connect to the grid. [pause] Then the part that pays the bills: "
            "installing on homes, sizing a system, and the government subsidy. [pause] Then serving "
            "businesses, where the numbers get much bigger. [pause] And finally, the business itself "
            "— the different ways to sell, and the margins you can actually earn. Let's begin."},

        {"id": "hook", "variant": "sol_hook", "props": {}, "narration":
            "Start with a problem everyone shares. [pause] Every month, an electricity bill arrives, "
            "and every year it seems to climb a little higher. [pause] That money just leaves, forever. "
            "[pause] Now look at the same house from above. The roof is bare. Sunlight is pouring onto "
            "it, all day, completely free — and it's being wasted. [pause] Solar is simply the "
            "business of catching some of that sunlight and turning it into electricity, so the bill "
            "drops by eighty, ninety, sometimes a hundred percent. [pause] And here is the scale of "
            "it. Enough sunlight strikes the Earth in a single hour to power all of humanity for an "
            "entire year. [pause] The energy is not the problem. Catching it is the opportunity."},

        {"id": "why", "variant": "sol_why", "props": {}, "narration":
            "So why is this a business right now, and not ten years ago? [pause] Four things changed "
            "at once. [pause] First, panels collapsed in price. A solar panel today costs roughly a "
            "tenth of what it did a decade ago. [pause] Second, grid electricity keeps getting more "
            "expensive — so the bill you avoid is bigger every year. [pause] Third, the government is "
            "paying. Under the P M Surya Ghar scheme, a home can get up to seventy-eight thousand "
            "rupees back. [pause] And fourth, the market has barely started. Fewer than five percent "
            "of Indian rooftops have solar. [pause] Cheaper hardware, costlier power, public money, "
            "and a wide-open market. That is why now."},
    ]},

    # ================================================================= CH 2 — THE SCIENCE
    {"id": "solar-ch02-science", "title": "The Science", "segments": [
        {"id": "divider", "variant": "sol_divider", "props": {"n": 2, "title": "The Science", "sub": "how a panel turns light into power", "color": CELL}, "narration":
            "Part two. The science. [pause] To sell something with confidence, you have to understand "
            "it. So let's open up a solar panel and see exactly how light becomes electricity."},

        {"id": "spectrum", "variant": "sol_spectrum", "props": {}, "narration":
            "It starts with the sunlight itself. [pause] Light does not arrive as a smooth stream. It "
            "arrives in tiny packets of energy. Each packet is called a photon. [pause] Think of "
            "sunlight as a constant rain of these energy packets, falling on everything. [pause] On a "
            "bright day, about one thousand watts of sunlight lands on every single square metre of "
            "ground. [pause] That is a lot of free energy, spread thin. A solar panel's whole job is "
            "to stand in that rain and catch it. [pause] So the question becomes — how do you turn a "
            "packet of light into a flow of electricity?"},

        {"id": "cell", "variant": "sol_cell", "props": {}, "narration":
            "This is the heart of everything — the photovoltaic effect. It sounds complex; it really "
            "isn't. [pause] A solar cell is a thin slice of silicon, built in two layers. [pause] The "
            "top layer is treated to have spare electrons, which carry negative charge. The bottom "
            "layer is treated to have empty spaces, called holes, which act positive. [pause] Where "
            "the two layers meet — the junction — nature sets up a built-in, one-way push. [pause] "
            "Now, a photon strikes the silicon and knocks an electron loose. [pause] That freed "
            "electron gets pushed by the junction out through the top. It has nowhere to go but "
            "through your wire — so it travels along, lights the bulb, does real work, and returns to "
            "the bottom. [pause] That steady flow of electrons through the wire is electric current. "
            "[pause] No fuel, no moving parts, no noise. Just light in, and electrons out."},

        {"id": "panel", "variant": "sol_panel", "props": {}, "narration":
            "One cell is tiny. [pause] It makes only about half a volt, and just a few watts — not "
            "enough to do much. [pause] So we wire many cells together. Sixty to a hundred and "
            "forty-four cells, sealed under glass in an aluminium frame, make one panel — the "
            "rectangle you see on roofs. [pause] A single modern panel produces around four to six "
            "hundred watts. [pause] Then we connect many panels together into an array. [pause] And "
            "an array is measured in kilowatts — enough to run a whole home. [pause] So the ladder is "
            "simple: cells make a panel, panels make an array, and the array is sized to match the "
            "electricity bill."},

        {"id": "efficiency", "variant": "sol_efficiency", "props": {}, "narration":
            "Now, a fair question. Of all that sunlight, how much actually becomes electricity? "
            "[pause] Of the one thousand watts landing on a square metre, a good modern panel converts "
            "only about two hundred. [pause] That is an efficiency of roughly twenty-one percent. "
            "[pause] The rest mostly leaves as heat. [pause] And that number is the ceiling, not the "
            "promise. Heat, dust, and even a little shade all pull it down. [pause] This is why a "
            "panel is rated at strong noon sun — real output rises and falls with the weather. [pause] "
            "A useful rule of thumb for India: every one kilowatt of panels makes about four units of "
            "electricity per day. Remember that number — you will use it on every sales call."},

        {"id": "types", "variant": "sol_types", "props": {}, "narration":
            "Walk into the market and you'll meet three kinds of panel. [pause] Monocrystalline — "
            "sleek and black — is the most efficient, around twenty-one percent, and it's today's "
            "default choice. [pause] Polycrystalline — the older blue, speckled panel — is cheaper "
            "but less efficient, around seventeen percent, and it's slowly fading out. [pause] And "
            "thin-film — light and even bendable — is the least efficient, but useful where you have "
            "lots of area and odd shapes. [pause] For a normal rooftop, where space is limited, "
            "monocrystalline almost always wins, because it squeezes the most watts out of every "
            "square foot."},
    ]},

    # ================================================================= CH 3 — THE SYSTEM
    {"id": "solar-ch03-system", "title": "The System", "segments": [
        {"id": "divider", "variant": "sol_divider", "props": {"n": 3, "title": "The System", "sub": "inverters and the grid", "color": GRID}, "narration":
            "Part three. The system. [pause] Panels alone are useless. To power a home, you need a few "
            "more pieces working together. Let's meet them."},

        {"id": "dcac", "variant": "sol_dcac", "props": {}, "narration":
            "Here's a catch nobody expects. [pause] Your panels make direct current — D C — a steady, "
            "one-way flow. [pause] But your home doesn't run on that. Your lights, fans, and fridge "
            "all need alternating current — A C — a wave that flips back and forth fifty times a "
            "second. [pause] So we need a translator. That translator is the inverter. [pause] The "
            "inverter takes the panels' D C and turns it into clean A C the grid can use. [pause] But "
            "it does more. It constantly hunts for the maximum power the panels can give, it handles "
            "safety, and it reports how much you're generating. [pause] It is the brain of the whole "
            "system. And because it works hardest, it's usually the first part to fail — so its "
            "quality matters more than anything else you buy."},

        {"id": "ongrid", "variant": "sol_ongrid", "props": {}, "narration":
            "Now, the clever part — how a home connects to the grid. This is called on-grid, or net "
            "metering, and it's the most common setup. [pause] During the day, your panels often make "
            "more power than you're using. [pause] That surplus doesn't go to waste — it flows out to "
            "the grid, and your meter literally runs backward, banking credit. [pause] At night, when "
            "the panels are asleep, you simply draw that credit back from the grid. [pause] So the "
            "grid acts like a giant, free battery — you deposit power by day and withdraw it by night. "
            "[pause] At the end of the month, you're billed only on the net: units taken, minus units "
            "sent. [pause] No expensive batteries needed. This is exactly why a home solar bill can "
            "land near zero."},

        {"id": "offgrid", "variant": "sol_offgrid", "props": {}, "narration":
            "But sometimes you do want to store the sun, and that means batteries. [pause] There are "
            "two situations. [pause] Off-grid means there's no grid at all — so batteries carry you "
            "through the night. Think of a remote farm, a mobile tower, or a village home far from the "
            "lines. [pause] Hybrid means you keep the grid, but add a battery for backup — so when the "
            "power cuts out, your lights stay on. Very popular where the supply is unreliable. [pause] "
            "But here's the honest trade-off. Batteries add real cost and complexity. [pause] Every "
            "battery you add stretches the payback period. So most homes with a stable grid skip them "
            "entirely, and choose net metering instead."},

        {"id": "components", "variant": "sol_components", "props": {}, "narration":
            "So what actually goes into a system, and where does the money go? [pause] The panels "
            "themselves are the biggest slice — a little over half the cost. [pause] The inverter is "
            "next, around fourteen percent. [pause] Then the mounting structure that holds the panels "
            "to the roof, about twelve percent. [pause] Then the balance of system — the cables, the "
            "meter, the safety gear — another twelve. [pause] And finally the installation and labour, "
            "about ten percent. [pause] Notice this: panels are half the bill of materials. That is "
            "why your profit comes down to two things — how well you source the hardware, and how "
            "cleanly you install it. Not any single magic gadget."},
    ]},

    # ================================================================= CH 4 — HOMES
    {"id": "solar-ch04-homes", "title": "Installing on Homes", "segments": [
        {"id": "divider", "variant": "sol_divider", "props": {"n": 4, "title": "Installing on Homes", "sub": "sizing, savings, subsidy", "color": SUN}, "narration":
            "Part four. Installing on homes. [pause] This is where a customer becomes a project — and "
            "a project becomes money. Let's walk through it exactly the way a good installer does."},

        {"id": "sizing", "variant": "sol_sizing", "props": {}, "narration":
            "The very first thing you do is size the system — and it's just one small sum. [pause] "
            "Take the electricity bill, and read the monthly units. Say this home uses six hundred "
            "units a month. [pause] Now recall our rule: each kilowatt of panels makes about a hundred "
            "and twenty units a month. [pause] So you divide. Six hundred, divided by a hundred and "
            "twenty, is five. [pause] This home needs a five kilowatt system. [pause] Then check the "
            "roof. A system needs roughly a hundred square feet of shade-free space per kilowatt — so "
            "five kilowatts wants about five hundred square feet. [pause] That's it. This one "
            "back-of-envelope calculation is how every single sales conversation begins."},

        {"id": "rooftop", "variant": "sol_rooftop", "props": {}, "narration":
            "But not every roof is a good roof, and knowing the difference saves you from bad "
            "projects. [pause] Four things matter. [pause] One — direction. In India, panels should "
            "face south, to catch the most sun across the day. [pause] Two — tilt. Panels lie at "
            "about fifteen to twenty-five degrees, so they face the sun's average height through the "
            "year. [pause] Three — shade. This one is sneaky. Even a single shadow, from one tree or "
            "one water tank, can drag down a whole connected string of panels. So the roof must stay "
            "clear from about nine in the morning to three in the afternoon. [pause] And four — "
            "strength. The roof has to safely carry the weight for twenty-five years. [pause] Get the "
            "survey right, and everything after it gets easier."},

        {"id": "install", "variant": "sol_install", "props": {}, "narration":
            "So how does the install actually happen? Seven steps. [pause] One, the survey and design. "
            "Two, the application to the electricity company — the DISCOM — for permission. [pause] "
            "Three, fixing the mounting structure to the roof. Four, bolting the panels on. Five, "
            "wiring everything into the inverter. [pause] Six, installing the special net meter and "
            "getting it inspected. And seven, switching on, and claiming the subsidy. [pause] Here's "
            "the surprise for most beginners. The physical work — the part that feels big — is usually "
            "just one to three days. [pause] It's the paperwork, the DISCOM approvals and the meter "
            "inspection, that stretches the whole thing into weeks. Managing that patiently is a real "
            "part of the job."},

        {"id": "savings", "variant": "sol_savings", "props": {}, "narration":
            "Now the moment every customer waits for — the payback. When does this pay for itself? "
            "[pause] Take a three kilowatt home system. After the government subsidy, the net cost is "
            "around one lakh rupees. [pause] That system saves roughly twenty-eight thousand rupees a "
            "year in avoided bills. [pause] So watch the two lines. Your savings pile up, year after "
            "year, until they cross what you paid — at around year three and a half. [pause] That "
            "crossing point is the payback. [pause] And here's the beautiful part. The panels are "
            "warrantied for twenty-five years. So after the payback, you get two more decades of power "
            "that is essentially free. [pause] Pay for about four years, then enjoy twenty for nothing. "
            "That is the pitch."},

        {"id": "subsidy", "variant": "sol_subsidy", "props": {}, "narration":
            "And that subsidy deserves its own moment, because it is your strongest closing argument. "
            "[pause] Under the P M Surya Ghar scheme, the government pays part of a home's system. "
            "[pause] The slab works like this. Thirty thousand rupees per kilowatt for the first two "
            "kilowatts. So one kilowatt gets thirty thousand, and two kilowatts gets sixty thousand. "
            "[pause] For the third kilowatt, you get another eighteen thousand — bringing a three "
            "kilowatt system to seventy-eight thousand rupees. [pause] And that is the cap. Go bigger "
            "— five kilowatts, ten kilowatts — and the subsidy stays at seventy-eight thousand. "
            "[pause] The money lands directly in the customer's bank account after inspection, and "
            "many states add a top-up on top. For a salesperson, that number cuts the price by a "
            "third — and closes the deal."},
    ]},

    # ================================================================= CH 5 — BUSINESSES
    {"id": "solar-ch05-business", "title": "Serving Businesses", "segments": [
        {"id": "divider", "variant": "sol_divider", "props": {"n": 5, "title": "Serving Businesses", "sub": "bigger bills, bigger deals", "color": CELL}, "narration":
            "Part five. Serving businesses. [pause] Homes are a fine start. But the real money in solar "
            "sits on the roofs of shops, offices, and factories. Here's why."},

        {"id": "cni", "variant": "sol_cni", "props": {}, "narration":
            "It comes down to the size of the bill. [pause] A home might pay three to eight thousand "
            "rupees a month, and need a small two-to-five kilowatt system. [pause] A shop or an office "
            "pays twenty to sixty thousand, and needs ten to fifty kilowatts. [pause] But a factory or "
            "a warehouse? It can pay lakhs every month, and need a hundred kilowatts, stretching into "
            "megawatts. [pause] And two things make businesses even better customers. [pause] First, "
            "commercial tariffs are higher than home rates — so every unit you save is worth more. "
            "[pause] Second, factories run during the daytime — exactly when the sun is shining. So "
            "the solar power gets used instantly. [pause] One factory rooftop can equal hundreds of "
            "homes, in size and in revenue."},

        {"id": "models", "variant": "sol_models", "props": {}, "narration":
            "But businesses fund solar in two very different ways, and you must know both. [pause] The "
            "first is CAPEX — the business simply buys the system. [pause] It pays upfront, or with a "
            "loan. In return, it keeps a hundred percent of the savings, gets a tax depreciation "
            "benefit, and after a payback of three to four years, the power is basically free. [pause] "
            "The second is the OPEX, or RESCO model — and this one is clever. [pause] A developer "
            "builds and owns the system on the customer's roof, at zero upfront cost to the business. "
            "[pause] The business just buys the solar power, at a rate lower than the grid, through a "
            "long agreement called a P P A. [pause] The developer earns for fifteen to twenty-five "
            "years. And sixty to seventy percent of commercial deals now use this model — because "
            "that's where the steady, recurring money lives."},

        {"id": "bizcase", "variant": "sol_bizcase", "props": {}, "narration":
            "Let's put real numbers on it, with one example. A factory with a hundred kilowatt "
            "rooftop. [pause] At commercial scale, that system costs around forty-five lakh rupees. "
            "[pause] It generates roughly a hundred and thirty thousand units of electricity a year. "
            "[pause] At a commercial tariff of about nine rupees a unit, that's nearly twelve lakh "
            "rupees saved, every single year. [pause] So it pays for itself in under four years. "
            "[pause] And across a twenty-five year life, it saves close to three crore rupees. [pause] "
            "Add the accelerated depreciation benefit, and the returns look even stronger. [pause] "
            "This is why serious businesses see solar not as a cost, but as one of the safest "
            "investments they can make."},
    ]},

    # ================================================================= CH 6 — THE BUSINESS
    {"id": "solar-ch06-selling", "title": "The Business", "segments": [
        {"id": "divider", "variant": "sol_divider", "props": {"n": 6, "title": "The Business", "sub": "channels, margins, getting started", "color": BIZ}, "narration":
            "Part six. The business itself. [pause] You now understand the product deeply. So let's "
            "answer the question you came for — how do you actually make money selling solar?"},

        {"id": "valuechain", "variant": "sol_valuechain", "props": {}, "narration":
            "Solar has a value chain, and you get to choose your spot on it. [pause] At one end sits "
            "manufacturing — building the panels. That takes enormous capital, a factory, and deep "
            "expertise. Very hard to enter. [pause] Next comes distribution — holding large stock and "
            "supplying dealers. Still high capital. [pause] Then E P C — engineering, procurement, and "
            "construction — the companies that design and install. Medium capital. [pause] Then "
            "selling and dealing — closing customers and arranging the install. Low capital. [pause] "
            "And at the far end, referring and maintenance — tiny capital. [pause] Here's the key "
            "insight. You do not need a factory. Most people start on the right-hand side — referring, "
            "selling, installing — where the capital is small and the demand is huge. The closer you "
            "are to the customer, the less money you need to begin."},

        {"id": "channels", "variant": "sol_channels", "props": {}, "narration":
            "So concretely, here are four doors into the business. [pause] One — referral, or "
            "affiliate. Zero capital. You simply send interested buyers to an installer, and earn "
            "maybe two to five thousand rupees for every closed job. The easiest possible start. "
            "[pause] Two — dealer, or reseller. You hold some stock, sell it, and arrange the install, "
            "for a margin of ten to eighteen percent. [pause] Three — E P C, or turnkey. You design, "
            "supply, and install the whole thing end to end, for fifteen to twenty-five percent. "
            "[pause] Four — a franchise. You ride a known brand — a Tata, a Luminous, a Waaree — and "
            "they hand you leads and trust. [pause] The smart path is to start light with referrals, "
            "build a reputation and real reviews, and then grow into stocking and installing yourself."},

        {"id": "margins", "variant": "sol_margins", "props": {}, "narration":
            "Now the number you really want — the margins. [pause] Selling just the panels, the "
            "hardware, earns a thin eight to twelve percent. [pause] Inverters and batteries do a "
            "little better, twelve to twenty. [pause] But the real money is in the service. Doing the "
            "full E P C — the design and installation — earns fifteen to twenty-five percent. [pause] "
            "And a good dealer, blending hardware and service, can see twenty to thirty-five percent. "
            "[pause] But let me be completely honest with you, because most videos won't be. [pause] "
            "Those headline margins look wonderful, but soft costs quietly eat into them — failed site "
            "visits, redesigns, delays, marketing — often five to ten percent. And competition keeps "
            "squeezing. [pause] The lesson is clear: earn from service and design, not from just "
            "reselling boxes."},

        {"id": "economics", "variant": "sol_economics", "props": {}, "narration":
            "Let's make it painfully concrete, with the profit and loss on one real job — a five "
            "kilowatt home system. [pause] You charge the customer around three lakh, twenty-five "
            "thousand rupees. [pause] Now your costs. The panels run about one lakh sixty. The "
            "inverter, forty-five thousand. The structure and balance of system, forty thousand. And "
            "labour plus soft costs, roughly forty-two thousand. [pause] Add those up, and your gross "
            "profit is around thirty-eight thousand rupees — a little under twelve percent. [pause] "
            "That may sound modest. But do a few of these every month, and add ongoing maintenance "
            "contracts, and the recurring income becomes the real prize. [pause] The whole game is "
            "this: buy well, install cleanly, and kill the soft costs."},

        {"id": "getstarted", "variant": "sol_getstarted", "props": {}, "narration":
            "So how do you actually begin? Here is a simple ninety-day path. [pause] First, learn the "
            "basics — sizing, wiring, and the DISCOM rules. The government's own MNRE site, and honest "
            "videos, cover it for free. [pause] Second, tie up supply — find a distributor for panels "
            "and inverters that are properly approved, on the A L M M and B I S lists. [pause] Third, "
            "register as a vendor, on the national P M Surya Ghar portal, and with your state DISCOM. "
            "[pause] Fourth, start with referrals — close a few jobs, and collect reviews and photos, "
            "because trust is your real product. [pause] And fifth, grow into full E P C — carry "
            "stock, hire an installer, and sign maintenance contracts. Small, steady steps."},

        {"id": "risks", "variant": "sol_risks", "props": {}, "narration":
            "Before we finish, let me show you the risks — the ones nobody advertises. [pause] First, "
            "price wars. Aggressive, cut-throat bidding can compress your margins fast. [pause] "
            "Second, soft-cost leakage — those failed visits, redesigns, and delays that silently eat "
            "your profit. [pause] Third, quality and warranty. A bad inverter or a leaking roof "
            "becomes your liability, for years. [pause] And fourth, policy dependence. Subsidies and "
            "net-metering rules can change with a government notification. [pause] None of these should "
            "scare you off. But they explain who wins. [pause] The winners don't compete on being the "
            "cheapest quote. They compete on trust, and on clean, reliable execution."},

        {"id": "recap", "variant": "sol_recap", "props": {
            "items": [
                "Sunlight arrives as photons; a silicon cell frees electrons — that flow is electricity",
                "Cells make a panel, panels make an array, sized to the customer's bill",
                "The inverter turns DC into AC; net metering makes the grid your free battery",
                "Size a system by dividing monthly units by 120; ~100 sq ft of clear roof per kW",
                "PM Surya Ghar pays up to ₹78,000; home payback is about 3.5 to 5 years",
                "Businesses have the big bills — CAPEX or the zero-upfront OPEX / RESCO model",
                "Enter near the customer: refer, sell, or install — service earns the best margin",
                "Win on trust and clean execution, not on being the cheapest quote",
            ],
            "closer": "Sunlight is free — the business is turning it into savings people gladly pay for.",
        }, "narration":
            "So let's bring the whole map together in one breath. [pause] Sunlight arrives as photons, "
            "and a silicon cell frees electrons — and that flow is your electricity. [pause] Cells "
            "make a panel, panels make an array, sized to the customer's bill. [pause] The inverter "
            "turns D C into A C, and net metering turns the grid into a free battery. [pause] You size "
            "a system by dividing monthly units by a hundred and twenty, and you need about a hundred "
            "square feet of clear roof per kilowatt. [pause] The subsidy pays up to seventy-eight "
            "thousand, and a home pays back in three and a half to five years. [pause] Businesses hold "
            "the big bills, funded by CAPEX, or the zero-upfront OPEX model. [pause] And to earn, you "
            "enter close to the customer — refer, sell, or install — because service earns the best "
            "margin. [pause] You win on trust and clean execution, never on being the cheapest quote. "
            "[pause] Sunlight is free. The business is turning it into savings people gladly pay for. "
            "[pause] Thanks for watching."},
    ]},
]
