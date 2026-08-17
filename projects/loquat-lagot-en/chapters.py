# -*- coding: utf-8 -*-
"""Lagot / loquat (Eriobotrya japonica) — long farmer course, English, captions ON.

Target: well over 30 minutes (~50–70 after TTS). Spoken language, [pause] after
new terms and numbers. Figures are planning bands, not a mandi quote.
"""

FRUIT, LEAF, COOL, RISK = "#F4A261", "#7CB518", "#4ECDC4", "#E76F51"


def S(sid, variant, narration, **props):
    return {"id": sid, "variant": variant, "props": props, "narration": narration}


CHAPTERS = [
    # ============================================================ CH 01
    {"id": "lag-ch01-identity", "title": "What lagot is", "segments": [
        S("title", "lag_title",
          "This is not a ten minute fruit tour. [pause] "
          "It is the briefing you want before you put lagot on farmland. [pause] "
          "What it is. How it grows. What it costs. Whether it is worth it."),

        S("roadmap", "lag_roadmap",
          "Twelve parts. [pause] First, what lagot actually is, and the trees people confuse with it. [pause] "
          "Then food uses, not miracle medicine. [pause] Then climate, and which Indian states really crop it. [pause] "
          "Then the farm year, varieties, planting, and the wait until year three. [pause] "
          "Then care, harvest, pests, costs, and the market verdict. [pause] "
          "Stay for the numbers. They are why most people should not plant this as their only crop."),

        S("hook", "lag_compare",
          "People search lagot and get wood apple. Those are not the same plant. [pause] "
          "Lagot is loquat. In India you also hear lukat, and lugath. [pause] "
          "The scientific name is Eriobotrya japonica. It is in the rose family, with apple and pear. [pause] "
          "Wood apple is kaitha. Hard shell. Brown pulp. A totally different tree. [pause] "
          "If you plant the wrong nursery label, you wait years for the wrong fruit.",
          kicker="HOOK · WRONG TREE, WRONG LIFE",
          title="Lagot is loquat, not wood apple",
          leftTitle="Lagot / loquat / lukat",
          leftBody="Evergreen subtropical tree. Soft yellow-orange fruit in clusters. Native to China. Eaten fresh in March and April.",
          rightTitle="Wood apple / kaitha",
          rightBody="Hard woody shell. Brown aromatic pulp. Different genus. Different season. Different market.",
          vs="NOT THE SAME TREE",
          leftC="fruit", rightC="risk",
          foot="Confirm the Latin name before you pay for plants."),

        S("names", "lag_cards",
          "Say the names out loud so a nursery cannot bluff you. [pause] "
          "English: loquat, sometimes Japanese medlar. [pause] "
          "North India: lukat, lugath, lagot. [pause] "
          "Japan calls the fruit biwa. China is still the world's main producer. [pause] "
          "In much of South India the same tree is planted as an ornamental, because warm winters do not set a crop. [pause] "
          "Your first job is not marketing. It is matching the name to the species.",
          kicker="NAMES ON THE TAG",
          title="If the Latin name is wrong, stop",
          cols=3, foot="Ask for Eriobotrya japonica, grafted.",
          items=[
              {"label": "Loquat", "sub": "English trade name. Soft clustered fruit.", "c": "fruit"},
              {"label": "Lukat / lugath", "sub": "Common North Indian names for the same tree.", "c": "leaf"},
              {"label": "Biwa", "sub": "Japanese name. Leaves used as tea there.", "c": "cool"},
              {"label": "Not kaitha", "sub": "Wood apple. Hard shell. Different crop.", "c": "risk"},
              {"label": "Not bael", "sub": "Aegle marmelos. Another lookalike in search.", "c": "risk"},
              {"label": "Not chikoo", "sub": "Sapota. Tropical. Fruits most of the year.", "c": "cool"},
          ]),

        S("tree", "lag_cards",
          "Picture the tree you will live with for twenty years. [pause] "
          "Evergreen. Spreading. Usually five to six metres tall in Indian orchards. [pause] "
          "Large leathery leaves. White flower clusters in the cool months. [pause] "
          "Fruit hangs in bunches, not as single mango-like units. [pause] "
          "That bunch habit decides harvest: you clip the cluster, you do not yank one fruit. [pause] "
          "If your land cannot host a spreading evergreen of that size, this is the wrong crop.",
          kicker="THE TREE",
          title="A spreading evergreen, not a bush",
          cols=2, foot="Plan canopy room now, not in year eight.",
          items=[
              {"label": "Height 5–6 m", "sub": "Spreading crown. Needs a real grid, not a fence line of leftovers.", "c": "leaf"},
              {"label": "Evergreen", "sub": "Shade all year. Intercrops only work while the trees are young.", "c": "cool"},
              {"label": "Cluster fruit", "sub": "One clip per bunch. Pulling fruit bruises and rots the lot.", "c": "fruit"},
              {"label": "Long life", "sub": "Peak yield around year fifteen. This is an orchard, not an annual.", "c": "fruit"},
          ]),
    ]},

    # ============================================================ CH 02
    {"id": "lag-ch02-uses", "title": "Eat, kitchen, factory", "segments": [
        S("div", "lag_divider",
          "Part two. What the fruit is for. [pause] "
          "You can eat it. You can cook it. You can process it. [pause] "
          "You should not plant it as a medicine factory.",
          n=2, title="Eat, kitchen, factory", sub="food first — claims last", color=LEAF),

        S("anatomy", "lag_anatomy",
          "What you sell is a small yellow to orange fruit. [pause] "
          "Thin skin. Juicy sweet-sour flesh. A few large seeds. [pause] "
          "It ripens on the tree. Half-ripe fruit does not finish like a banana. [pause] "
          "That is why harvest timing is everything. Pick too early, flavour never arrives. [pause] "
          "Pick too late, and the bunch collapses in the crate. [pause] "
          "Dessert fruit first. Jam and squash second. Leaf tea is a side story, not a farm plan."),

        S("eat", "lag_orbit",
          "Yes, you eat it. Fresh, out of hand, is the main Indian use. [pause] "
          "The window is late March into April, when few other local fruits are cheap. [pause] "
          "That scarcity is the price story. It is also the logistics story. [pause] "
          "The fruit is perishable. It does not sit like apple in cold store for months. [pause] "
          "If you cannot reach a buyer in days, you need a processing plan before you plant. [pause] "
          "Eating it is easy. Selling a truck of ripe loquat is the hard part.",
          kicker="CAN WE EAT IT",
          title="Yes — as a short-season dessert fruit",
          hub="FRESH",
          foot="Edible. Perishable. Seasonal. That triad is the business.",
          items=[
              {"label": "Eat fresh", "c": "fruit"},
              {"label": "Jam and jelly", "c": "leaf"},
              {"label": "Squash / nectar", "c": "cool"},
              {"label": "Chutney", "c": "fruit"},
              {"label": "Leaf tea (Asia)", "c": "cool"},
              {"label": "Not a drug crop", "c": "risk"},
          ]),

        S("kitchen", "lag_cards",
          "Kitchen uses are real and they add a second buyer. [pause] "
          "Jam and jelly take fruit that is too soft for the fresh stall. [pause] "
          "Squash and nectar take pulp. Chutney takes the sweet-sour edge. [pause] "
          "Canning exists in countries with a bigger crop. India barely has that industry for loquat. [pause] "
          "So do not assume a factory will appear because you planted twenty acres. [pause] "
          "If processing is your plan, talk to a pulp unit before the pits are dug.",
          kicker="COMMERCIAL USES",
          title="Processing is a buffer, not a given",
          cols=2, foot="A buyer on paper beats a recipe in your head.",
          items=[
              {"label": "Fresh mandi", "sub": "Highest price if fruit is uniform, ripe, and in the city this week.", "c": "fruit"},
              {"label": "Jam / jelly", "sub": "Saves soft fruit. Needs sugar, jars, FSSAI sense, and a brand or a contract.", "c": "leaf"},
              {"label": "Squash", "sub": "Pulp plus acid plus sugar. Works when fresh glut hits.", "c": "cool"},
              {"label": "Leaf tea", "sub": "Popular in East Asia. Not a listed Indian commodity you can scale blindly.", "c": "risk"},
          ]),

        S("medicine", "lag_cards",
          "You will see health videos. Treat them as noise. [pause] "
          "The fruit has carotenoids, potassium, vitamin C, polyphenols. That is food. [pause] "
          "Leaves are used in Chinese and Japanese herbal teas for cough and inflammation in those traditions. [pause] "
          "Tradition is not a licence, and it is not a purchase order. [pause] "
          "Do not tell a banker this orchard is an Ayurvedic A P I farm. [pause] "
          "Plant it to sell fruit. Anything else is a bonus you cannot bank.",
          kicker="MEDICINE CLAIMS",
          title="Nutrients yes. A clinic crop no.",
          cols=3, foot="This video is not medical advice.",
          items=[
              {"label": "Food value", "sub": "Vitamin A carotenoids, potassium, vitamin C. Eat as fruit.", "c": "leaf"},
              {"label": "Leaf tradition", "sub": "East Asian teas. Not your Indian mandi ticket.", "c": "cool"},
              {"label": "Do not claim cures", "sub": "Inflammation, tumours, liver — those papers are not a farm model.", "c": "risk"},
          ]),
    ]},

    # ============================================================ CH 03
    {"id": "lag-ch03-climate", "title": "Climate and India", "segments": [
        S("div", "lag_divider",
          "Part three. Climate, and the map. [pause] "
          "Loquat will grow as a pretty tree in many places. [pause] "
          "It will fruit as a crop only where winters are cool enough.",
          n=3, title="Climate and India", sub="pretty tree versus paying crop", color=COOL),

        S("climate", "lag_cards",
          "This is a subtropical fruit. [pause] "
          "It wants an average year above about fifteen degrees, and a long frost-free stretch. [pause] "
          "It also wants a cool, relatively wet winter so flower and fruit can develop. [pause] "
          "April to June heat above thirty-five degrees on ripening fruit is a quality killer. [pause] "
          "Warm winters mean flowers drop or never come. That is why Chennai is not Punjab for this crop. [pause] "
          "Match the climate first. Variety shopping comes second.",
          kicker="CLIMATE GATE",
          title="Cool winters make fruit. Heat makes leaves.",
          cols=2, foot="If your winter is warm, plant something else.",
          items=[
              {"label": "Cool winter", "sub": "Needed for a real crop. Warm winters → ornamental tree.", "c": "cool"},
              {"label": "Frost window", "sub": "It handles some frost, but bloom and young fruit do not.", "c": "risk"},
              {"label": "Heat at harvest", "sub": "Over 35°C in April–June cooks quality on the tree.", "c": "fruit"},
              {"label": "Drainage", "sub": "Sandy loam, organic matter, never a wet foot for weeks.", "c": "leaf"},
          ]),

        S("map", "lag_map",
          "Where does India actually grow it? [pause] "
          "Punjab: Rupnagar, Hoshiarpur, Gurdaspur, Patiala. Semi-hilly, drained land. [pause] "
          "Himachal, especially the Kangra belt. Delhi orchards and home gardens. [pause] "
          "Uttar Pradesh. Assam in small pockets. Maharashtra in places with a cooler winter. [pause] "
          "Tamil Nadu hills and Mysore: often ornamental, fruit quality poor. [pause] "
          "China grows the world's crop. Spain and others follow. India is a niche, not a sea of orchards.",
          kicker="INDIAN GEOGRAPHY",
          title="Fruiting states are few, and northern",
          foot="A neighbour with fruit in April is better proof than a YouTube map."),

        S("punjab", "lag_cards",
          "Punjab is the Indian reference because P A U actually tested cultivars there. [pause] "
          "Tanaka showed heavier fruit and better acceptance than some older local types. [pause] "
          "Golden Yellow and Pale Yellow are older releases from the late nineteen sixties. [pause] "
          "California Advance is a late type, into the fourth week of April. [pause] "
          "Use that research as a starting list, then ask your K V K what survives locally. [pause] "
          "A variety that wins in Ludhiana can sulk one valley over.",
          kicker="PUNJAB AS THE REFERENCE",
          title="P A U names you can actually ask for",
          cols=2, foot="Local trial beats a catalogue photo.",
          items=[
              {"label": "Golden Yellow", "sub": "1967. Medium fruit, yellow flesh, about third week of March.", "c": "fruit"},
              {"label": "Pale Yellow", "sub": "1967. Larger fruit, white flesh, about second week of April.", "c": "leaf"},
              {"label": "California Advance", "sub": "1970. Later. Cream flesh. Fourth week of April.", "c": "cool"},
              {"label": "Tanaka", "sub": "Promising under Punjab trials: size, cluster, taste scores.", "c": "fruit"},
          ]),

        S("world", "lag_bars",
          "Scale check, so you do not dream of export on day one. [pause] "
          "China produces far more loquat than anyone else. [pause] "
          "Spain is a distant second in the trade conversation. Pakistan and Turkey also crop it. [pause] "
          "India does not publish this as a major horticulture statistic the way it does mango. [pause] "
          "That means two things. One: you will not fight a national glut. [pause] "
          "Two: you also will not find a ready cold-chain and a futures price. You are making a market by hand.",
          kicker="WORLD SCALE",
          title="India is a footnote, not the crop",
          unit="",
          foot="Niche can mean premium. It can also mean no buyer.",
          bars=[
              {"label": "China", "v": 100, "c": "fruit"},
              {"label": "Spain", "v": 18, "c": "cool"},
              {"label": "Others", "v": 12, "c": "leaf"},
              {"label": "India niche", "v": 4, "c": "risk"},
          ]),
    ]},

    # ============================================================ CH 04
    {"id": "lag-ch04-year", "title": "The farm year", "segments": [
        S("div", "lag_divider",
          "Part four. The calendar. [pause] "
          "Loquat is not a year-round fruit like sapota in the tropics. [pause] "
          "You get one main harvest, and it is short.",
          n=4, title="The farm year", sub="one crop, one short window", color=FRUIT),

        S("cal", "lag_cal",
          "Plant and graft in the monsoon, June to September. [pause] "
          "Flowering can run from July thoughts through January, but the useful flush is later. [pause] "
          "The first flush often sheds. The third is weak. The second flush, around October to February, is the crop. [pause] "
          "Fruit needs about two months on the tree after set, and about ninety days from bloom to ripe in many climates. [pause] "
          "Harvest: end of March into April. Then a May prune. [pause] "
          "Miss that rhythm and you are decorating land.",
          kicker="TWELVE MONTHS",
          title="Monsoon plant. Spring harvest. May prune.",
          foot="The money weeks are few. Everything else is setup.",
          bands=[
              {"label": "Plant / graft  June–September", "from": 0, "to": 3, "c": "leaf"},
              {"label": "Useful flowering  Oct–Feb", "from": 4, "to": 8, "c": "cool"},
              {"label": "Harvest  late March–April", "from": 9, "to": 10, "c": "fruit"},
              {"label": "Light prune  end of May", "from": 11, "to": 11, "c": "risk"},
          ]),

        S("plantwin", "lag_cards",
          "Why monsoon planting? [pause] "
          "Young grafts need water without you living on the pump in week one. [pause] "
          "June to September is the usual window in North Indian guides. [pause] "
          "Pits should be ready before the rains, not scraped during a downpour. [pause] "
          "Keep the graft union well above soil so it does not rot or root from the scion. [pause] "
          "Stake every plant. A spreading loquat in wind is a snapped union waiting to happen.",
          kicker="PLANTING WINDOW",
          title="June to September, pits already open",
          cols=3, foot="Rain helps. Waterlogging kills.",
          items=[
              {"label": "Pits first", "sub": "Metre-class pits, filled with topsoil and F Y M, then plant.", "c": "leaf"},
              {"label": "Union high", "sub": "Graft joint stays above ground. Always.", "c": "risk"},
              {"label": "Stake", "sub": "Two stakes, not a hopeful bamboo. Wind is real.", "c": "cool"},
          ]),

        S("flower", "lag_cards",
          "Flowering is the part farmers misread. [pause] "
          "You will see blooms in more than one flush. Most of the early ones drop. [pause] "
          "Protect the October to February flush with water and nutrition, not with hope. [pause] "
          "Bees help. Mixing varieties helps when a type is a shy pollinator. [pause] "
          "Frost on open flowers is a silent yield cut. Low spots collect cold air. [pause] "
          "If your block is a frost pocket, loquat flowers will teach you that once.",
          kicker="FLOWER FLUSHES",
          title="The second flush is the crop",
          cols=2, foot="Count clusters in winter, not leaves in August.",
          items=[
              {"label": "Flush one", "sub": "Often sheds. Do not celebrate it as harvest.", "c": "risk"},
              {"label": "Flush two", "sub": "October to February. This is the money bloom.", "c": "fruit"},
              {"label": "Flush three", "sub": "Usually poor. Do not delay prune for it.", "c": "cool"},
              {"label": "Pollination", "sub": "Mix cultivars. Bees. Do not plant a lonely clone block.", "c": "leaf"},
          ]),

        S("harvestwin", "lag_cards",
          "Harvest is late March to April in the North Indian belt. [pause] "
          "Early types like Golden Yellow come first. Late types stretch the stall into late April. [pause] "
          "That is why a mixed orchard is not decoration. It is a two to three week longer sales window. [pause] "
          "Fruit must colour and flavour on the tree. [pause] "
          "Once clipped, the clock is days, not months. [pause] "
          "Plan labour for bunches, crates, and a truck the same week, not 'sometime in summer'.",
          kicker="HARVEST WINDOW",
          title="Three to five weeks, then it is gone",
          cols=2, foot="Labour in April is part of the crop, not an afterthought.",
          items=[
              {"label": "Early", "sub": "Golden Yellow class. Third week of March in Punjab guides.", "c": "fruit"},
              {"label": "Mid", "sub": "Fire Ball, Safeda, and similar lists in extension notes.", "c": "leaf"},
              {"label": "Late", "sub": "California Advance, Tanaka. Stretch into late April.", "c": "cool"},
              {"label": "Clock", "sub": "Ripe to buyer in days. No mango-style holding fantasy.", "c": "risk"},
          ]),
    ]},

    # ============================================================ CH 05
    {"id": "lag-ch05-plants", "title": "Varieties and plants", "segments": [
        S("div", "lag_divider",
          "Part five. What you put in the ground. [pause] "
          "Seedlings are a trap. True-to-type plants are scarce. [pause] "
          "This is the bottleneck Indian papers actually name.",
          n=5, title="Varieties and plants", sub="grafts, not seeds", color=LEAF),

        S("seed", "lag_compare",
          "Do not raise a commercial orchard from seed. [pause] "
          "Seedlings grow slow, fruit late, and do not copy the mother tree. [pause] "
          "You wanted Golden Yellow. You get a lottery. [pause] "
          "Buy grafted or budded plants. Air-layering is used, but success is often lower than a good graft. [pause] "
          "Inarching is timed in July and August in some guides. [pause] "
          "The constraint in India is not Wikipedia. It is finding a nursery that sells true plants.",
          kicker="PROPAGATION",
          title="Grafted plants, or do not plant",
          leftTitle="Graft / bud",
          leftBody="True to type. Earlier bearing, often year three. This is the commercial path.",
          rightTitle="Seedling",
          rightBody="Slow. Off-type. Late to fruit. Fine for a curiosity tree, fatal for an acre plan.",
          vs="YEAR THREE VS NEVER QUITE",
          leftC="leaf", rightC="risk",
          foot="Papers flag missing true-type nursery plants as the adoption brake."),

        S("vars", "lag_table",
          "Build a mix, not a monoculture of one pretty name. [pause] "
          "Early, mid, and late types spread harvest and pollination. [pause] "
          "Golden Yellow and Pale Yellow are the old Punjab pair. [pause] "
          "Improved Golden Yellow and Thames Pride show up on early lists. [pause] "
          "Mid lists include Fire Ball, Safeda, Matchless, Large Agra. [pause] "
          "Late: California Advance and Tanaka. Ask P A U or your university which are still in their plots.",
          kicker="CULTIVAR MIX",
          title="Early, mid, late — on purpose",
          cols=["Slot", "Examples", "Why mix"],
          rows=[
              ["Early", "Golden Yellow, Pale Yellow", "First rupees in March"],
              ["Mid", "Fire Ball, Safeda, Matchless", "Fill the stall"],
              ["Late", "California Advance, Tanaka", "April buyers still hungry"],
              ["Pollinizer", "Plant two or three types", "Shy types need neighbours"],
          ],
          foot="One clone across ten acres is a pollination and price-risk bet."),

        S("nursery", "lag_cards",
          "How do you buy plants without getting cheated? [pause] "
          "Go to a university farm, a registered horticulture nursery, or a K V K demo. [pause] "
          "Ask for the rootstock, the scion name, and the graft date. [pause] "
          "Reject plants with a buried union, scale, or a bent graft. [pause] "
          "Expect on the order of ninety-five plants per acre at six to seven metre spacing. [pause] "
          "Price the plant last. A cheap off-type is the most expensive tree you will ever own.",
          kicker="NURSERY DISCIPLINE",
          title="True-to-type or walk away",
          cols=2, foot="Count plants for the grid you designed, not a denser fantasy.",
          items=[
              {"label": "~96 / acre", "sub": "Six to seven metre spacing. Do not crowd for 'more trees'.", "c": "leaf"},
              {"label": "Named scion", "sub": "Write Golden Yellow, not 'desi loquat'.", "c": "fruit"},
              {"label": "Union visible", "sub": "If you cannot see the graft, you cannot trust the tree.", "c": "risk"},
              {"label": "K V K / univ.", "sub": "Start there. Random roadside plants are how orchards fail.", "c": "cool"},
          ]),

        S("poll", "lag_orbit",
          "Pollination is easy to skip on paper and expensive in year five. [pause] "
          "Some cultivars are self fertile. Some are only weakly so. [pause] "
          "Extension advice: mix California Advance with Golden Yellow and Pale Yellow. [pause] "
          "Keep bees if you can. Do not spray insecticides in open bloom. [pause] "
          "Wind and insects both move pollen, but a solid block of one shy type still under-sets. [pause] "
          "Design the mix on the map before the tractor arrives.",
          kicker="POLLINATION",
          title="Mix types so flowers become fruit",
          hub="POLLEN",
          foot="A pretty monoculture can be a barren one.",
          items=[
              {"label": "Golden Yellow", "c": "fruit"},
              {"label": "Pale Yellow", "c": "leaf"},
              {"label": "Cal. Advance", "c": "cool"},
              {"label": "Tanaka", "c": "fruit"},
              {"label": "Bees", "c": "leaf"},
              {"label": "No bloom spray", "c": "risk"},
          ]),
    ]},

    # ============================================================ CH 06
    {"id": "lag-ch06-plant", "title": "Planting the orchard", "segments": [
        S("div", "lag_divider",
          "Part six. Layout. [pause] "
          "This is the last cheap moment to get spacing right. [pause] "
          "After year five, a crowded orchard is a saw problem.",
          n=6, title="Planting the orchard", sub="six to seven metres, or regret", color=COOL),

        S("space", "lag_orchard",
          "Here is the acre, computed. [pause] "
          "Twelve by eight is ninety-six stations at a six to seven metre grid. [pause] "
          "That matches the ninety-five to ninety-six plants per acre in Punjab leaflets. [pause] "
          "Watch the grid as years pass. Until year three the dots stay green wood. [pause] "
          "Then they switch to bearing. The layout does not magically tighten. [pause] "
          "If you plant at four metres because plants were cheap, you will prune for light forever."),

        S("pits", "lag_pipe",
          "Land work is boring and it decides roots. [pause] "
          "Level. Two or three deep ploughings. Then pits, about a metre class, not a dibble hole. [pause] "
          "Mix topsoil with farmyard manure in the fill. Plant on a slight mound if drainage is shy. [pause] "
          "Water in. Mulch. Stake. [pause] "
          "Do not bury the union. Do not leave an air pocket under the root ball. [pause] "
          "The first month is establishment. Miss water then, and you replant in year two.",
          kicker="ESTABLISHMENT PIPE",
          title="Plough, pit, plant, stake, water",
          foot="A metre pit is cheaper than a dead graft.",
          nodes=[
              {"label": "Plough", "sub": "Fine tilth, level", "c": "leaf"},
              {"label": "Pit 1 m", "sub": "FYM + topsoil", "c": "cool"},
              {"label": "Plant", "sub": "Union above soil", "c": "fruit"},
              {"label": "Stake", "sub": "Wind insurance", "c": "risk"},
              {"label": "Water", "sub": "Then mulch", "c": "cool"},
          ]),

        S("soil", "lag_cards",
          "Soil: sandy loam, organic matter, drainage. [pause] "
          "Loquat hates wet feet. A pretty monsoon clay pan is a grave. [pause] "
          "pH in a comfortable horticultural range matters less than oxygen at the root. [pause] "
          "Hill benches and light alluvium in the Punjab-Himachal story work because water leaves. [pause] "
          "If your field ponds for a week after rain, fix drainage or pick another fruit. [pause] "
          "Organic matter is the other half: young trees want a living topsoil, not a crust.",
          kicker="SOIL",
          title="Drainage first, texture second",
          cols=3, foot="Waterlogged loquat is a short story.",
          items=[
              {"label": "Sandy loam", "sub": "The textbook home. Roots breathe.", "c": "leaf"},
              {"label": "Never stagnant", "sub": "Raise beds or skip the crop.", "c": "risk"},
              {"label": "FYM every year", "sub": "Especially once bearing starts. Leaves and fruit both demand it.", "c": "fruit"},
          ]),

        S("inter", "lag_cards",
          "Years one and two, the alley is cash. [pause] "
          "Intercrop short vegetables or pulses that do not swamp the graft. [pause] "
          "Do not plant another tree in the row. Do not run sugarcane that owns the water. [pause] "
          "Keep a clean basin around each loquat. [pause] "
          "The intercrop pays labour while you wait for year three. [pause] "
          "When the canopy closes, the alley ends. Plan that grief now.",
          kicker="YEARS ONE AND TWO CASH",
          title="Intercrop the alley — not another orchard",
          cols=2, foot="The tree is the business. The alley is a bridge.",
          items=[
              {"label": "Veg / pulse", "sub": "Short, shallow, and out of the basin.", "c": "leaf"},
              {"label": "Not a second tree", "sub": "No mango filler in the same grid. You will regret the shade.", "c": "risk"},
              {"label": "Clean basin", "sub": "Weeds at the trunk steal water from a baby graft.", "c": "cool"},
              {"label": "Stop when shade", "sub": "Closed canopy means the intercrop idea is over.", "c": "fruit"},
          ]),
    ]},

    # ============================================================ CH 07
    {"id": "lag-ch07-years", "title": "Years until fruit", "segments": [
        S("div", "lag_divider",
          "Part seven. Time. [pause] "
          "The question everyone asks: one year, two, or three? [pause] "
          "For grafted plants, plan on year three. Not year one.",
          n=7, title="Years until fruit", sub="year three — peak near fifteen", color=FRUIT),

        S("time", "lag_time",
          "Here is the honest timeline. [pause] "
          "Year zero: plant in monsoon. Survive. [pause] "
          "Year one and two: wood, training, intercrop. Maybe a stray fruit. Ignore it. [pause] "
          "Year three: first real crop on grafted trees, if you did not starve them. [pause] "
          "Some guides say four years to a proper bloom. Believe the slower number when you budget. [pause] "
          "Year seven to ten: commercial volume. Year fifteen: typical maximum in the leaflets. Then a long plateau if you keep feeding the tree.",
          kicker="TIME TO MONEY",
          title="Not one year. Not two. Plan three.",
          foot="Seedlings can add years. That is another reason not to use them.",
          steps=[
              {"y": "Y0", "label": "Plant", "sub": "Monsoon grafts", "c": "leaf"},
              {"y": "Y1–2", "label": "Wood", "sub": "Train + intercrop", "c": "cool"},
              {"y": "Y3", "label": "First crop", "sub": "Grafted trees", "c": "fruit"},
              {"y": "Y7–10", "label": "Commercial", "sub": "Volume arrives", "c": "leaf"},
              {"y": "Y15", "label": "Peak", "sub": "Leaflet maximum", "c": "fruit"},
          ]),

        S("y12", "lag_cards",
          "What you actually do in year one and two. [pause] "
          "Water through dry spells. A young loquat is not a cactus in June. [pause] "
          "Train a central leader or an open centre. Remove low shoots up to about sixty centimetres to a metre. [pause] "
          "Fertilize lightly. Punjab-style tables start around ten to twenty kilos F Y M per tree, plus small urea, S S P, and M O P. [pause] "
          "Do not chase fruit. Chase a framework you can pick from in year eight. [pause] "
          "If a tree flowers in year two, thin most of it. Let wood win.",
          kicker="YEARS ONE AND TWO",
          title="Build the skeleton, steal no fruit",
          cols=2, foot="A bent year-two tree is a bent year-twelve tree.",
          items=[
              {"label": "Train", "sub": "Leader or open centre. Low branches off. Stakes still on.", "c": "leaf"},
              {"label": "Light feed", "sub": "FYM plus modest N P K. Not a mango dose on a baby.", "c": "cool"},
              {"label": "Water", "sub": "Establishment irrigations beat a dramatic drip later.", "c": "cool"},
              {"label": "Thin flowers", "sub": "If they appear early, take them off. Wood first.", "c": "risk"},
          ]),

        S("y3", "lag_cards",
          "Year three is not a lottery ticket. It is a small crop if the tree is ready. [pause] "
          "Expect kilograms, not quintals, per tree. [pause] "
          "This is when you learn your harvest crew, crates, and buyer. [pause] "
          "Better a small sold crop than a dumped experiment. [pause] "
          "If year three is zero, do not panic once. Check union, water, frost, and whether you actually planted loquat. [pause] "
          "If year five is still zero, the climate or the plant type is wrong. Cut losses.",
          kicker="YEAR THREE",
          title="First fruit is a rehearsal, not retirement",
          cols=3, foot="Use year three to test the market path.",
          items=[
              {"label": "Small crop", "sub": "Learn clip, grade, and the mandi clock.", "c": "fruit"},
              {"label": "Still train", "sub": "Do not let fruit bend the leader forever.", "c": "leaf"},
              {"label": "Zero crop?", "sub": "Once: diagnose. Year five still zero: exit.", "c": "risk"},
          ]),

        S("feed", "lag_table",
          "Feeding, as leaflets state it, scales with age. [pause] "
          "Years one and two: ten to twenty kilos F Y M, and a few hundred grams of fertiliser each. [pause] "
          "Years three to six: twenty-five to forty kilos F Y M, and the N P K jumps. [pause] "
          "Older trees: around fifty kilos F Y M, plus about a kilo of urea and larger S S P and M O P. [pause] "
          "Put F Y M, phosphorus, and potash in September. Split urea: October, then January or February after fruit set. [pause] "
          "Those grams are per tree in the Punjab table, not per acre. Do not  multiply wrong.",
          kicker="FERTILISER BY AGE",
          title="September organics. Split urea.",
          cols=["Age", "FYM / tree", "Urea band"],
          rows=[
              ["1–2 years", "10–20 kg", "150–500 g"],
              ["3–6 years", "25–40 kg", "600–750 g"],
              ["7–10 years", "40–50 kg", "800–1000 g"],
              ["10+ years", "about 50 kg", "about 1000 g"],
          ],
          foot="Confirm current K V K rates. Leaflets age. Your soil test does not."),
    ]},

    # ============================================================ CH 08
    {"id": "lag-ch08-care", "title": "Care that decides yield", "segments": [
        S("div", "lag_divider",
          "Part eight. The work that changes yield. [pause] "
          "Water at fruit set. A May prune. A trained frame. [pause] "
          "Skip these and year fifteen still looks like year four.",
          n=8, title="Care that decides yield", sub="water, wood, and a clip", color=LEAF),

        S("water", "lag_cards",
          "Loquat can look drought-tough and still fail you at fruit size. [pause] "
          "Guides call for three to four irrigations from fruit set to maturity. [pause] "
          "That is the yield irrigation, not the survival irrigation. [pause] "
          "Drip makes those pulses cheap. Flood on heavy soil invites root rot. [pause] "
          "Mulch the basin. Weeds in March steal the water you just paid for. [pause] "
          "If you cannot water in the sixty days before harvest, do not plant a dessert fruit.",
          kicker="IRRIGATION",
          title="Three to four pulses while fruit swells",
          cols=2, foot="Survival drought-tolerance is not a sizing strategy.",
          items=[
              {"label": "Fruit-set water", "sub": "This is when size is decided. Miss it, sell small fruit.", "c": "cool"},
              {"label": "Drip if you can", "sub": "Pulses without a wet pan. Better on loam too.", "c": "leaf"},
              {"label": "Mulch", "sub": "Keeps April heat off shallow roots.", "c": "fruit"},
              {"label": "No flood clay", "sub": "Wet feet plus heat is how trees fade.", "c": "risk"},
          ]),

        S("prune", "lag_cards",
          "Prune for a frame, then stop showing off. [pause] "
          "After harvest, around the end of May, snip about five centimetres below the shoot tips. [pause] "
          "That light heading sets next season's wood. [pause] "
          "Heavy pruning makes leaves, not fruit. [pause] "
          "Open the centre enough that a cluster can colour. [pause] "
          "Take out dead wood and watersprouts whenever you see them, not in a once-a-decade rage.",
          kicker="PRUNING",
          title="May tip-prune. Do not butcher.",
          cols=3, foot="Wood you cut in May is next April's money.",
          items=[
              {"label": "End of May", "sub": "After harvest. Light heading, not topping.", "c": "fruit"},
              {"label": "Open light", "sub": "Colour needs sun on the bunch.", "c": "leaf"},
              {"label": "Heavy = leaves", "sub": "A savage prune delays bearing. Again.", "c": "risk"},
          ]),

        S("thin", "lag_cards",
          "Clusters overbear. That is normal. [pause] "
          "If you want mandi size, thin fruit in the cluster while they are small. [pause] "
          "If you want jam pulp, you can leave more on, and accept small fruit. [pause] "
          "Decide that before bloom, not at the crate. [pause] "
          "Birds and bats will thin for you in a bad way. Netting is a cost in some sites. [pause] "
          "Hand thinning is skilled, slow, and worth it on the fresh market path.",
          kicker="CROP LOAD",
          title="Thin for size, or leave for pulp",
          cols=2, foot="Every fruit on a cluster is not a victory.",
          items=[
              {"label": "Fresh path", "sub": "Fewer, larger fruit. Buyers pay for size and colour.", "c": "fruit"},
              {"label": "Pulp path", "sub": "More fruit, smaller, processed the same week.", "c": "leaf"},
              {"label": "Birds", "sub": "Net or lose the coloured ones first.", "c": "risk"},
              {"label": "Labour", "sub": "Thinning is a line item. Budget it.", "c": "cool"},
          ]),

        S("weed", "lag_cards",
          "Weeds: hand hoe the basin. [pause] "
          "Old leaflets mention glyphosate in the alley at a labelled rate, off the crop. [pause] "
          "Rules and products change. Read the current label. Keep spray off green loquat wood. [pause] "
          "A weedy March basin is a water thief. [pause] "
          "A herbicide scar on a young graft is a dead tree. [pause] "
          "If labour can hoe, hoe. Chemical shortcuts belong in the alley, never on the trunk.",
          kicker="WEEDS",
          title="Clean basin. Careful alley.",
          cols=3, foot="Current label beats a 2015 PDF.",
          items=[
              {"label": "Hoe the basin", "sub": "Safe. Always legal. Always useful.", "c": "leaf"},
              {"label": "Alley only", "sub": "If you use herbicide, it is for weeds, not the tree.", "c": "risk"},
              {"label": "Mulch helps", "sub": "Less germination, cooler soil, fewer hoes.", "c": "cool"},
          ]),
    ]},

    # ============================================================ CH 09
    {"id": "lag-ch09-harvest", "title": "Harvest and yield", "segments": [
        S("div", "lag_divider",
          "Part nine. Picking, and the numbers. [pause] "
          "We will run two yield curves, not one fantasy number.",
          n=9, title="Harvest and yield", sub="clip bunches — believe two curves", color=FRUIT),

        S("pick", "lag_pipe",
          "How to pick. [pause] "
          "Wait until the bunch is uniformly ripe enough. Colour and flavour do not improve in the crate. [pause] "
          "Do not pull fruit. You tear skin and start rot. [pause] "
          "Use a clipper. Take the whole cluster. [pause] "
          "Shade immediately. Grade by size. [pause] "
          "Then move. This pipeline is the difference between a premium crate and vinegar.",
          kicker="HARVEST PIPE",
          title="Ripe on the tree. Clip. Shade. Grade. Move.",
          foot="Hand-pulling is how a good orchard looks like a bad one.",
          nodes=[
              {"label": "Ripe", "sub": "On-tree colour", "c": "fruit"},
              {"label": "Clip", "sub": "Whole bunch", "c": "leaf"},
              {"label": "Shade", "sub": "Field heat off", "c": "cool"},
              {"label": "Grade", "sub": "Size, scars", "c": "fruit"},
              {"label": "Ship", "sub": "Days, not weeks", "c": "risk"},
          ]),

        S("yield", "lag_yield",
          "Now the computed curves on one acre of ninety-six trees. [pause] "
          "The red line is a conservative leaflet world: about eight kilos per mature tree, ramping from year three to fifteen. [pause] "
          "That lands near six to eight quintals an acre at peak — the number many Punjab notes print. [pause] "
          "The green line is a managed trial world: about twenty-eight kilos a tree, in the P A U ballpark for good cultivars. [pause] "
          "That is twenty-plus quintals if everything works. [pause] "
          "Do not put the green line in a bank file unless you have seen your own trees do it."),

        S("kg", "lag_bars",
          "P A U compared cultivars under Punjab conditions. [pause] "
          "Tanaka sat near thirty-four kilos per plant in that study window. [pause] "
          "Pale Yellow and Pathankot were in the low thirties. Golden Yellow a little under thirty. [pause] "
          "Those are research trees, not a neglected backyard. [pause] "
          "Fruit weight sat around eighteen to twenty-four grams. Not a mango. A premium small fruit. [pause] "
          "Cluster counts matter: Tanaka held more fruit per cluster in that trial.",
          kicker="TRIAL YIELD PER TREE",
          title="Kilos on research trees, not promises",
          unit=" kg",
          foot="Your acre will undershoot until water, mix, and age catch up.",
          bars=[
              {"label": "Imp. G.Y.", "v": 24, "c": "risk"},
              {"label": "Golden Y.", "v": 29, "c": "fruit"},
              {"label": "Pathankot", "v": 31, "c": "cool"},
              {"label": "Pale Y.", "v": 31, "c": "leaf"},
              {"label": "Tanaka", "v": 34, "c": "fruit"},
          ]),

        S("grade", "lag_cards",
          "Grading is how you capture the upper price. [pause] "
          "Large, unblemished, uniform colour in a ventilated crate. [pause] "
          "Seconds go to pulp the same day if you have a kettle or a buyer. [pause] "
          "Do not mix bird-pecked fruit into the top layer. Buyers remember. [pause] "
          "Count seeds and acid only if you are breeding. The stall cares about look and taste. [pause] "
          "A cheap crate that crushes clusters destroys the week's work.",
          kicker="GRADE OR GIVE AWAY MARGIN",
          title="Top fruit and pulp fruit are different products",
          cols=2, foot="One rotten fruit in a bunch teaches the rest to rot.",
          items=[
              {"label": "A grade", "sub": "Size, colour, no scars. City retail and hotels.", "c": "fruit"},
              {"label": "B grade", "sub": "Smaller, still sound. Local mandi.", "c": "leaf"},
              {"label": "Process", "sub": "Soft, split, surplus. Jam the same week.", "c": "cool"},
              {"label": "Dump", "sub": "Rot and bird wrecks. Do not hide them.", "c": "risk"},
          ]),
    ]},

    # ============================================================ CH 10
    {"id": "lag-ch10-protect", "title": "Pests and packing", "segments": [
        S("div", "lag_divider",
          "Part ten. What eats your margin. [pause] "
          "Insects, fungus, birds, and the crate. [pause] "
          "Perishability is the silent cost.",
          n=10, title="Pests and packing", sub="the week after ripe is the risk", color=RISK),

        S("pests", "lag_cards",
          "Leaf roller ties leaves and chews. [pause] "
          "Aphids suck new growth, curl leaves, and grow sooty mould on honeydew. [pause] "
          "Old notes name specific insecticides. Those labels change. Ask K V K for today's list. [pause] "
          "Do not spray in open bloom. You kill the crop's pollinators. [pause] "
          "Scout weekly in flush periods, not once when the tree looks sad. [pause] "
          "A clean, fed tree still needs eyes. Loquat is not 'no pest'.",
          kicker="INSECTS",
          title="Leaf roller and aphids, then ask K V K",
          cols=2, foot="Bloom sprays are how you buy a pretty barren tree.",
          items=[
              {"label": "Leaf roller", "sub": "Rolled leaves, chewed flush. Scout the new growth.", "c": "risk"},
              {"label": "Aphids", "sub": "Curl, honeydew, black mould. Worse on lush nitrogen.", "c": "cool"},
              {"label": "No bloom spray", "sub": "Protect bees or you protect nothing.", "c": "leaf"},
              {"label": "Current label", "sub": "This course will not recite banned chemistry.", "c": "fruit"},
          ]),

        S("disease", "lag_cards",
          "Black spot is the fungus leaflets keep repeating. [pause] "
          "Sunken dark spots on leaves, and sometimes fruit blemish that kills grade. [pause] "
          "Wet springs favour it. Open canopies and sanitation help. [pause] "
          "Fungicide names in old PDFs may still be legal, or not. Check. [pause] "
          "Remove badly infected wood. Do not compost obvious disease in the basin. [pause] "
          "Fruit with spots is process fruit at best, dump at worst.",
          kicker="DISEASE",
          title="Black spot steals grade, then price",
          cols=3, foot="Blemish is a market disease even when the tree lives.",
          items=[
              {"label": "Black spot", "sub": "Fungus. Leaves and fruit. Wet weather friend.", "c": "risk"},
              {"label": "Air flow", "sub": "May prune and spacing are the first spray.", "c": "leaf"},
              {"label": "Sanitation", "sub": "Get sick wood off the orchard floor.", "c": "cool"},
          ]),

        S("post", "lag_cards",
          "After the clip, physics owns you. [pause] "
          "Field heat. Compression in a deep crate. One split fruit. [pause] "
          "There is no national cold-chain built for Indian loquat. You improvise. [pause] "
          "Shade nets, morning harvest, shallow layers, fast truck. [pause] "
          "Hotels and retail want this week. Processors wanted a call last month. [pause] "
          "If the mandi is four hours of bad road, pack for bruises, not for Instagram.",
          kicker="POSTHARVEST",
          title="Days to a buyer, or days to a loss",
          cols=2, foot="Perishability is a line on the P and L.",
          items=[
              {"label": "Morning pick", "sub": "Cooler fruit, longer fuse.", "c": "cool"},
              {"label": "Shallow crates", "sub": "Clusters crush. Depth is a decision.", "c": "fruit"},
              {"label": "Same-week sale", "sub": "No apple fantasy. Move or process.", "c": "leaf"},
              {"label": "Bad road", "sub": "Distance is a quality tax.", "c": "risk"},
          ]),

        S("pack", "lag_pipe",
          "A simple pack line you can actually run. [pause] "
          "Clip in the cool hours. [pause] "
          "Sort in shade: A crate, B crate, kettle. [pause] "
          "Weigh. Ticket. [pause] "
          "Truck or tempo to mandi, kirana aggregator, or the jam bench. [pause] "
          "If that line has no owner on your farm, the fruit will find the compost by itself.",
          kicker="PACK LINE",
          title="Someone must own the hours after clip",
          foot="Harvest without a pack owner is a hobby.",
          nodes=[
              {"label": "Clip", "sub": "Cool hours", "c": "fruit"},
              {"label": "Sort", "sub": "A / B / kettle", "c": "leaf"},
              {"label": "Weigh", "sub": "Ticket it", "c": "cool"},
              {"label": "Move", "sub": "Mandi or pan", "c": "fruit"},
          ]),
    ]},

    # ============================================================ CH 11
    {"id": "lag-ch11-costs", "title": "Costs and cash", "segments": [
        S("div", "lag_divider",
          "Part eleven. Money out, money in. [pause] "
          "These are planning bands. Your district will disagree. [pause] "
          "That disagreement is why you call K V K before you borrow.",
          n=11, title="Costs and cash", sub="bands, not a promise", color=COOL),

        S("est", "lag_tower",
          "Establishment is the year-zero cheque. [pause] "
          "Land preparation and pits. [pause] "
          "Ninety-six grafted plants — price varies wildly by nursery honesty. [pause] "
          "FYM, stakes, basin shaping. [pause] "
          "Irrigation if you do not already have it. That line dominates. [pause] "
          "Fencing if nilgai or people will browse. A planning band around one lakh an acre is a starting conversation, not a quote. Drip and fence can double it.",
          kicker="YEAR ZERO",
          title="What you spend before a single fruit",
          cap="Illustrative stack: plants and pits are not the expensive part. Water and fence are. Get three local quotes. Reject any YouTube 'lakhs a month from year one' clip.",
          foot="Year zero has no loquat revenue. Intercrop is the only cash.",
          segs=[
              {"label": "Land + pits", "h": 90, "c": "leaf"},
              {"label": "Grafts ~96", "h": 110, "c": "fruit"},
              {"label": "FYM + stakes", "h": 70, "c": "cool"},
              {"label": "Irrigation share", "h": 160, "c": "cool"},
              {"label": "Fence / risk", "h": 80, "c": "risk"},
          ]),

        S("ann", "lag_cards",
          "Every year after: manure, fertiliser, irrigation energy, pruning labour, harvest labour, crates, spray if needed. [pause] "
          "Harvest labour is bunched into three to five weeks. That spike surprises people. [pause] "
          "A planning band of twenty-five to forty thousand rupees an acre a year, excluding family labour, is a conservative talk number. [pause] "
          "It will be wrong on your farm. Use it to see that this is not a zero-cost jungle tree. [pause] "
          "The expensive years are the silent ones — one and two — when costs run and fruit does not. [pause] "
          "Budget a cash bridge. Intercrop. Another crop. Off-farm. Not hope.",
          kicker="ANNUAL COSTS",
          title="Quiet years still spend money",
          cols=2, foot="Family labour is a cost even when nobody invoices it.",
          items=[
              {"label": "Feed + water", "sub": "FYM, fertiliser, pump hours. Every year.", "c": "cool"},
              {"label": "April labour", "sub": "Clip and pack. You cannot postpone ripening.", "c": "fruit"},
              {"label": "Y1–Y2 hole", "sub": "Costs without fruit. Design the bridge.", "c": "risk"},
              {"label": "Crates / net", "sub": "Pack and bird net are easy to forget on paper.", "c": "leaf"},
          ]),

        S("cash", "lag_cash",
          "Here is a computed cumulative cash story. It is a model. [pause] "
          "Ninety thousand to establish. Twenty-eight thousand a year. [pause] "
          "Conservative line: leaflet yield times eighty rupees a kilo. [pause] "
          "Managed line: trial-like yield times one hundred twenty rupees a kilo. [pause] "
          "Watch when each line crosses zero. That is the patience the crop demands. [pause] "
          "If your mandi is fifty rupees, or your yield is the red line, the crossing moves right. Maybe off the chart."),

        S("price", "lag_cards",
          "Price honesty. [pause] "
          "Loquat is not onion. There is no clean all-India mandi series I will pretend to quote as gospel. [pause] "
          "Retail in metros in season is often talked about from about fifty rupees a kilo up through a couple of hundred for fancy packed fruit. [pause] "
          "Farm-gate is lower. Always. [pause] "
          "A seven kilo gift box at a high city price is not your acre average. [pause] "
          "Call your nearest fruit mandi next March and write the number you hear. That number beats this video.",
          kicker="PRICE BANDS",
          title="No national MSP. Ask March mandi.",
          cols=2, foot="Premium packed fruit is not the same as bulk farm-gate.",
          items=[
              {"label": "Farm-gate", "sub": "Lowest. Distance and glut hit you first.", "c": "risk"},
              {"label": "Local mandi", "sub": "The default path. Commission and wastage apply.", "c": "cool"},
              {"label": "City retail", "sub": "Higher sticker. You are not that sticker.", "c": "fruit"},
              {"label": "Process", "sub": "Lower rupees, higher volume, less panic.", "c": "leaf"},
          ]),
    ]},

    # ============================================================ CH 12
    {"id": "lag-ch12-verdict", "title": "Market and verdict", "segments": [
        S("div", "lag_divider",
          "Part twelve. Who buys, and whether you should plant. [pause] "
          "This is the decision chapter. [pause] "
          "If your land fails the climate test, you already have the answer.",
          n=12, title="Market and verdict", sub="who buys — and should you", color=FRUIT),

        S("who", "lag_orbit",
          "Where can you sell. [pause] "
          "The fruit mandi in a city that already knows lukat: Chandigarh, Delhi, Lucknow, parts of Punjab. [pause] "
          "Street vendors in those weeks. [pause] "
          "Hotels and juice counters if you can grade. [pause] "
          "A jam maker if you signed them before harvest. [pause] "
          "Direct boxes to consumers in a four week window if you already have a list. [pause] "
          "Export is not plan A for a new Indian orchard. You have no volume and no protocol.",
          kicker="BUYERS",
          title="Local mandi first. Export last, if ever.",
          hub="SELL",
          foot="A named buyer in February is worth more than a May hope.",
          items=[
              {"label": "Fruit mandi", "c": "fruit"},
              {"label": "Vendors", "c": "leaf"},
              {"label": "Hotels", "c": "cool"},
              {"label": "Jam unit", "c": "leaf"},
              {"label": "Direct boxes", "c": "fruit"},
              {"label": "Not export-first", "c": "risk"},
          ]),

        S("model", "lag_cards",
          "Business models that are not fantasy. [pause] "
          "One: a few acres as diversification on a cool-winter farm that already has water and a city road. [pause] "
          "Two: a homestead block for home use plus a crate to neighbours. Fine. Not a loan crop. [pause] "
          "Three: fresh plus a small kettle brand, if you can do FSSAI and sales. [pause] "
          "Four: contract pulp — only with a signature. [pause] "
          "What is not a model: ten acres of seedlings, no buyer, tropical plains, year-one income slides.",
          kicker="MODELS",
          title="Diversify. Do not bet the farm.",
          cols=2, foot="Loquat is a side orchard until you have years of data.",
          items=[
              {"label": "Diversify", "sub": "Best use. Other crops pay the quiet years.", "c": "leaf"},
              {"label": "Homestead", "sub": "Honest. Do not borrow against it.", "c": "cool"},
              {"label": "Fresh + jam", "sub": "Needs a kitchen that is a real micro-enterprise.", "c": "fruit"},
              {"label": "Contract pulp", "sub": "Paper first. Fruit second.", "c": "risk"},
          ]),

        S("decide", "lag_decide",
          "So is it worth it? [pause] "
          "Plant if your winters are cool, your soil drains, you can buy grafted named plants, you can water at fruit set, and a city mandi is close enough that fruit arrives alive. [pause] "
          "Plant if you can wait three years, and fifteen for peak. [pause] "
          "Skip if you need income next season from this tree. [pause] "
          "Skip if your winter is warm. Skip if the nursery cannot name the scion. Skip if April labour will not show up. [pause] "
          "Worth it as a niche on the right land. Not worth it as a miracle, a medicine farm, or a tropical gamble.",
          kicker="GO OR NO",
          title="Worth it only on the right land",
          foot="Not financial advice. Confirm with K V K and last March's mandi.",
          go=[
              "Cool winters, drained soil, irrigation",
              "Grafted, named plants and a cultivar mix",
              "A nearby fruit mandi or a signed processor",
              "Cash to survive years one and two",
              "Willingness to clip bunches in April",
          ],
          no=[
              "Warm-winter plains expecting a crop",
              "Seedlings and unknown roadside plants",
              "Need for year-one loan repayment from loquat",
              "No labour in the harvest weeks",
              "Medicine or export as the main story",
          ]),

        S("check", "lag_cards",
          "A last field checklist. [pause] "
          "Walk a neighbour's tree in April if one exists. Taste. Time the harvest. [pause] "
          "Stand in your field in January. Is it actually cold at night? [pause] "
          "Stand there after a heavy rain. Does water leave? [pause] "
          "Get a plant quote with a variety name. Get a mandi commission number. [pause] "
          "Then decide. Lagot is a real fruit, a real food, a real niche business — and a real way to waste five years on the wrong climate.",
          kicker="BEFORE YOU DIG",
          title="Five checks that beat a video",
          cols=2, foot="The orchard is decided in January and in a nursery yard.",
          items=[
              {"label": "Taste April fruit", "sub": "If nobody nearby has it, your market may be thin too.", "c": "fruit"},
              {"label": "January night", "sub": "Cool enough to flower, not a frost bowl.", "c": "cool"},
              {"label": "Rain drainage", "sub": "Puddles are a veto.", "c": "risk"},
              {"label": "Named grafts", "sub": "No Latin name, no sale.", "c": "leaf"},
          ]),

        S("recap", "lag_recap",
          "In one breath. [pause] "
          "Lagot is loquat, not wood apple. You eat it. You can jam it. You do not farm it as a drug. [pause] "
          "Cool-winter India: Punjab, Himachal, Delhi, U P, Assam, some Maharashtra. [pause] "
          "Plant monsoon. Harvest March and April. Grafted trees fruit around year three. Peak near fifteen. [pause] "
          "Ninety-six trees an acre. Clip bunches. Yield is a band, not a boast. [pause] "
          "Sell near a city. Price is local. Worth it only if the land and the wait both fit. [pause] "
          "Thanks for watching.",
          items=[
              "Lagot = loquat (Eriobotrya japonica), not kaitha",
              "Eat fresh; process as backup; skip medicine-as-business",
              "Cool winters required; South often ornamental only",
              "Grafted plants; mix varieties; ~96 trees per acre",
              "First fruit ~year 3; peak ~year 15; harvest Mar–Apr",
              "Clip clusters; perishable in days; grade or lose price",
              "Costs run before fruit; intercrop years 1–2",
              "Worth it as a niche on the right land — not a miracle",
          ],
          closer="Cool winters. Grafted plants. Year three. A short, perishable crop."),
    ]},
]


def _insert(chid, segs, before_last=False):
    for c in CHAPTERS:
        if c["id"] == chid:
            if before_last:
                c["segments"] = c["segments"][:-1] + segs + c["segments"][-1:]
            else:
                c["segments"].extend(segs)
            return
    raise KeyError(chid)


# Extra depth so the course clears 30 minutes and teaches like a farm briefing.
_insert("lag-ch01-identity", [
    S("origin", "lag_cards",
      "Where did this tree come from? [pause] "
      "Central eastern China. Japan made it famous as biwa. [pause] "
      "It travelled as an ornamental and a fruit tree, not as a British plantation staple like tea. [pause] "
      "That history matters. There is no colonial playbook for Indian loquat acres. [pause] "
      "You are closer to a homestead fruit that found a few serious districts. [pause] "
      "Treat it like a specialist orchard, not like a wheat package.",
      kicker="ORIGIN",
      title="Chinese fruit. Indian niche. No package.",
      cols=3, foot="No MSP, no national mission, no default buyer.",
      items=[
          {"label": "China", "sub": "Still the world's orchard. Breeding and volume live there.", "c": "fruit"},
          {"label": "Japan", "sub": "Culture and leaf tea. Not your mandi.", "c": "cool"},
          {"label": "India", "sub": "Scattered belts. You must build the market by hand.", "c": "leaf"},
      ]),
    S("family", "lag_cards",
      "The rose family is a clue for care. [pause] "
      "Apple and pear people already know fire blight anxiety and fruit thinning. [pause] "
      "Loquat is evergreen, so it does not take a hard winter rest like apple. [pause] "
      "But it still wants thinning, a frame, and respect at bloom. [pause] "
      "Do not copy mango spray calendars onto this tree. [pause] "
      "Copy the idea of a trained fruit tree, not a jungle.",
      kicker="BOTANY CLUE",
      title="Rose family. Evergreen. Not mango.",
      cols=2, foot="Wrong spray calendar is how you burn bees and fruit.",
      items=[
          {"label": "Like apple", "sub": "Thinning, frame, bloom care, fruit in clusters.", "c": "leaf"},
          {"label": "Unlike apple", "sub": "Evergreen. Subtropical. Spring harvest in India.", "c": "cool"},
          {"label": "Unlike mango", "sub": "Different pests, different season, different pack.", "c": "fruit"},
          {"label": "Unlike kaitha", "sub": "Soft fruit. No crowbar. No brown pulp.", "c": "risk"},
      ]),
    S("idleaf", "lag_cards",
      "Identify a tree in a nursery yard. [pause] "
      "Leaves are large, thick, dark green above, often rusty-felted below. [pause] "
      "The leaf looks tropical. The fruit looks like a small apricot cluster. [pause] "
      "Wood apple leaves do not look like that. Bael leaves are trifoliate. [pause] "
      "Take a photo of the leaf underside before you pay. [pause] "
      "If the seller hates that, walk.",
      kicker="FIELD ID",
      title="Leaf first, fruit story second",
      cols=3, foot="A felted leaf underside is a loquat tell.",
      items=[
          {"label": "Thick leaf", "sub": "Leathery. Not a thin citrus leaf.", "c": "leaf"},
          {"label": "Felt below", "sub": "Rusty hairs on the underside are common.", "c": "fruit"},
          {"label": "Not trifoliate", "sub": "If you see bael’s three leaflets, you are in the wrong queue.", "c": "risk"},
      ]),
])

_insert("lag-ch02-uses", [
    S("howeat", "lag_cards",
      "How people actually eat it. [pause] "
      "Wash. Eat skin and all, or peel if it bothers you. [pause] "
      "Spit the large seeds. Do not crush them for a snack. [pause] "
      "Chill briefly if you can. Warm fruit tastes flatter. [pause] "
      "A ripe fruit yields to a gentle press and smells floral-sweet. [pause] "
      "Green-hard fruit is sour and never becomes a banana on the kitchen counter.",
      kicker="HOW TO EAT",
      title="Ripe, gentle, spit the stones",
      cols=2, foot="Seeds are waste, not a second product, on a small farm.",
      items=[
          {"label": "Skin on", "sub": "Thin. Many eat it. Wash dust and spray residue.", "c": "fruit"},
          {"label": "Spit seeds", "sub": "Large stones. Not almond culture.", "c": "leaf"},
          {"label": "Slight give", "sub": "Ripe test. Hard-green stays disappointing.", "c": "cool"},
          {"label": "No counter-ripe", "sub": "It is not banana. Tree-ripe or not at all.", "c": "risk"},
      ]),
    S("nutri", "lag_cards",
      "Nutrition, without a sermon. [pause] "
      "You get carotenoids, which the body can use as vitamin A activity. [pause] "
      "Potassium is in the pulp — think banana-class mineral, not a pill. [pause] "
      "Vitamin C and polyphenols ride along. Water is most of the fruit. [pause] "
      "That is a good dessert. It is not a prescription. [pause] "
      "If a seller says it cures blood pressure, you are not in a nursery. You are in a pitch.",
      kicker="NUTRITION",
      title="A fruit. Not a pharmacy.",
      cols=3, foot="Sell flavour and season. Not diagnoses.",
      items=[
          {"label": "Carotenoids", "sub": "The orange colour is not just pretty.", "c": "fruit"},
          {"label": "Potassium", "sub": "Food mineral. Still a fruit serving.", "c": "cool"},
          {"label": "No cure card", "sub": "Refuse medical marketing on the crate.", "c": "risk"},
      ]),
    S("valueadd", "lag_pipe",
      "If you add value, keep the line short. [pause] "
      "Wash. Sort. Cook with sugar and acid. Fill hot. Label. [pause] "
      "Jam is the realistic Indian micro-product. Wine and leather and cosmetics are hobbies. [pause] "
      "FSSAI registration is not optional if you sell beyond friends. [pause] "
      "A pretty jar without a buyer is inventory with a shelf life. [pause] "
      "Start with one SKU. One flavour. One city kirana list.",
      kicker="VALUE ADD",
      title="Jam is the grown-up side path",
      foot="Process the seconds. Do not process your A grade unless the mandi failed.",
      nodes=[
          {"label": "Sort", "sub": "Seconds only", "c": "leaf"},
          {"label": "Cook", "sub": "Sugar + acid", "c": "fruit"},
          {"label": "Fill", "sub": "Hot, clean", "c": "cool"},
          {"label": "Label", "sub": "FSSAI", "c": "risk"},
          {"label": "Sell", "sub": "One SKU", "c": "fruit"},
      ]),
])

_insert("lag-ch03-climate", [
    S("micro", "lag_cards",
      "Microclimate will humble a district average. [pause] "
      "A frost hollow fifty metres below the road can strip flowers while the ridge crops. [pause] "
      "A west wall that bakes in April can sunburn fruit. [pause] "
      "Wind on a ridge snaps unions. [pause] "
      "Walk your field at dawn in January and at two in the afternoon in April. [pause] "
      "Those two walks are cheaper than a wrong ten-acre plant.",
      kicker="MICROCLIMATE",
      title="The field is not the district map",
      cols=2, foot="Ridge versus hollow is a yield decision.",
      items=[
          {"label": "Dawn January", "sub": "Where does cold air pool? Flowers die there.", "c": "cool"},
          {"label": "April 2 p.m.", "sub": "Where does heat sit? Fruit quality dies there.", "c": "fruit"},
          {"label": "Wind line", "sub": "Stake and maybe a break. Unions snap.", "c": "risk"},
          {"label": "Shade of forest", "sub": "Loquat wants light on the cluster. Deep shade is ornamental.", "c": "leaf"},
      ]),
    S("elev", "lag_cards",
      "Elevation. [pause] "
      "Guides say it can grow toward two thousand metres, but fruit quality often falls. [pause] "
      "Too high: cold and short seasons. Too low and tropical: no crop. [pause] "
      "The sweet belt in India is foothill and north subtropical plain with a real winter. [pause] "
      "If you are in coastal Konkan humidity without a cool winter, look at sapota instead. [pause] "
      "Right fruit, right altitude.",
      kicker="ALTITUDE",
      title="Foothills yes. High Himalaya, poor fruit.",
      cols=3, foot="Two thousand metres is survival, not a quality slogan.",
      items=[
          {"label": "Foothill", "sub": "Himachal-Punjab story. Drainage plus winter.", "c": "leaf"},
          {"label": "North plain", "sub": "If winter is real and water leaves.", "c": "cool"},
          {"label": "High / coastal", "sub": "Pretty tree. Weak business.", "c": "risk"},
      ]),
    S("china", "lag_cards",
      "Why China dwarfs everyone. [pause] "
      "Centuries of cultivars. Hills that match the crop. A public that already wants biwa-class fruit. [pause] "
      "India has the opposite: few cultivars in trade, few eaters outside a belt, few nurseries. [pause] "
      "That is not a reason to quit. It is a reason to stay small until demand is proven. [pause] "
      "Copying a Chinese mountain documentary onto a Tamil Nadu plot is how money dies. [pause] "
      "Copy the discipline: right hill, right variety, right harvest week.",
      kicker="WHY CHINA WINS",
      title="Culture plus climate plus cultivars",
      cols=2, foot="You cannot import a market by importing a YouTube clip.",
      items=[
          {"label": "Cultivars", "sub": "They have many. We have a short list in real nurseries.", "c": "fruit"},
          {"label": "Eaters", "sub": "They know the fruit. Many Indians do not.", "c": "cool"},
          {"label": "Hills", "sub": "Matched sites. Not wishful tropical acres.", "c": "leaf"},
          {"label": "Your move", "sub": "Start small. Prove April sales. Then expand.", "c": "risk"},
      ]),
])

_insert("lag-ch04-year", [
    S("flushwhy", "lag_cards",
      "Why the first flush sheds. [pause] "
      "Heat, incomplete chill, and a tree still pushing leaves. [pause] "
      "You cannot bully that flush into a crop with urea. [pause] "
      "You can make the second flush worse by starving water in autumn. [pause] "
      "Think like a fruit grower: protect the flush that history says pays. [pause] "
      "Write October to February on the pump shed wall.",
      kicker="WHY FLUSHES FAIL",
      title="Do not worship the first blossom",
      cols=3, foot="The paying bloom is the one you water in winter.",
      items=[
          {"label": "Early shed", "sub": "Normal. Not a tragedy.", "c": "risk"},
          {"label": "Autumn water", "sub": "Sets the useful bloom.", "c": "cool"},
          {"label": "No urea panic", "sub": "Nitrogen in the wrong month is leaves.", "c": "leaf"},
      ]),
    S("labourcal", "lag_cal",
      "Labour peaks twice. [pause] "
      "Monsoon: pits, planting, staking. [pause] "
      "April: clip, grade, pack, every day for a few weeks. [pause] "
      "May prune is a smaller crew. Winter thinning is skilled and slow. [pause] "
      "If your family is away in April for a wedding season, you will watch fruit rot. [pause] "
      "Put April on the calendar like a harvest festival that cannot move.",
      kicker="LABOUR CALENDAR",
      title="April is not optional overtime",
      foot="Hire before colour, not after the first crate collapses.",
      bands=[
          {"label": "Plant labour  Jun–Sep", "from": 0, "to": 3, "c": "leaf"},
          {"label": "Winter thin / watch  Nov–Feb", "from": 5, "to": 8, "c": "cool"},
          {"label": "Harvest crew  Mar–Apr", "from": 9, "to": 10, "c": "fruit"},
          {"label": "May prune crew", "from": 11, "to": 11, "c": "risk"},
      ]),
    S("irrigcal", "lag_cards",
      "Irrigation calendar, plain. [pause] "
      "After planting: keep the basin moist until roots bite. [pause] "
      "Winter: do not let the useful bloom sit in dust. [pause] "
      "Fruit swell: three to four real irrigations, more on sand. [pause] "
      "Monsoon: often none, except drainage. [pause] "
      "A moisture metre is nicer than a fight. A finger in the basin is free.",
      kicker="WATER CALENDAR",
      title="Wet at plant. Wet at swell. Dry feet in flood.",
      cols=2, foot="The dangerous week is fruit swell on sand in a dry April.",
      items=[
          {"label": "Establish", "sub": "Frequent small drinks. Mulch.", "c": "leaf"},
          {"label": "Bloom winter", "sub": "Do not drought the paying flush.", "c": "cool"},
          {"label": "Swell", "sub": "Three to four pulses. Size lives here.", "c": "fruit"},
          {"label": "Monsoon", "sub": "Drain. Do not add a flood.", "c": "risk"},
      ]),
])

_insert("lag-ch05-plants", [
    S("graft", "lag_pipe",
      "Grafting, at the level you need to brief a nursery. [pause] "
      "A rootstock seedling or a strong plant. A named scion stick. A union that heals. [pause] "
      "Inarching in July-August appears in Indian notes. Budding and grafting are preferred for early bearing. [pause] "
      "Air-layers root, but many growers still see more failures. [pause] "
      "You do not need to be the grafter. You need to inspect unions. [pause] "
      "A tape mummy with no callus is a stick, not a tree.",
      kicker="GRAFT BRIEF",
      title="Union, scion name, date — or no deal",
      foot="Pay for a healed union, not for soil in a bag.",
      nodes=[
          {"label": "Rootstock", "sub": "Healthy base", "c": "leaf"},
          {"label": "Named scion", "sub": "Written", "c": "fruit"},
          {"label": "Union", "sub": "Callused", "c": "cool"},
          {"label": "Harden", "sub": "Then sell", "c": "leaf"},
          {"label": "Your check", "sub": "See it", "c": "risk"},
      ]),
    S("tanaka", "lag_cards",
      "Tanaka, in that Punjab comparison, carried more fruit weight and a better eating score. [pause] "
      "That does not mean Tanaka is legal magic in your tehsil. [pause] "
      "It means you should ask whether anyone nearby has Tanaka fruit you can taste in April. [pause] "
      "If they do, prefer it in the mix. [pause] "
      "If they do not, Golden Yellow plus Pale Yellow is still a documented pair. [pause] "
      "Never plant a name you have not seen as fruit.",
      kicker="TANAKA NOTE",
      title="Trial winner. Still taste it locally.",
      cols=3, foot="A paper is not a tree in your soil.",
      items=[
          {"label": "Size", "sub": "Heavier fruit in the Punjab study window.", "c": "fruit"},
          {"label": "Cluster", "sub": "More fruit per bunch in that trial.", "c": "leaf"},
          {"label": "Taste score", "sub": "Higher acceptance. Confirm with your mouth.", "c": "cool"},
      ]),
    S("mixmap", "lag_orchard",
      "On the same ninety-six station grid, mix types. [pause] "
      "Do not put all Golden Yellow on the west hot edge. [pause] "
      "Scatter pollinizers every few trees, like a chessboard, not a ghetto block. [pause] "
      "Mark them with paint on the stake the day you plant. You will forget. [pause] "
      "A map in a notebook beats memory in year six. [pause] "
      "When you replant a dead station, write the name again."),
])

_insert("lag-ch06-plant", [
    S("rowdir", "lag_cards",
      "Row direction. [pause] "
      "North-south rows often share light more evenly on a flat field. [pause] "
      "On a slope, contour wins, because erosion and drainage win. [pause] "
      "Leave a road down the middle you can drive a tempo in April. [pause] "
      "If a crate cannot leave the row without a circus, you designed a museum. [pause] "
      "Tractor width plus cluster overhang is wider than you think.",
      kicker="ROWS AND ROADS",
      title="Light, contour, and a harvest road",
      cols=2, foot="Design the April tempo path on day zero.",
      items=[
          {"label": "N–S on flat", "sub": "Even light on both sides of the tree.", "c": "leaf"},
          {"label": "Contour on slope", "sub": "Soil stays. Water leaves slowly, not as a cut.", "c": "cool"},
          {"label": "Harvest road", "sub": "Centre lane. No dead ends of mud.", "c": "fruit"},
          {"label": "Overhang", "sub": "Clusters occupy the aisle. Measure real trees.", "c": "risk"},
      ]),
    S("fence", "lag_cards",
      "Animals. [pause] "
      "Nilgai, goats, and stray cattle will browse a young graft like salad. [pause] "
      "A fruit year invites theft in peri-urban belts. [pause] "
      "Fence is ugly and it is often the difference between an orchard and a story. [pause] "
      "Guard in April if the block is visible from a road. [pause] "
      "Budget pride last. Budget wire first.",
      kicker="FENCE AND THEFT",
      title="A crop you cannot protect is not a crop",
      cols=3, foot="Year-three fruit is a beacon. Plan for that.",
      items=[
          {"label": "Browse", "sub": "Young grafts disappear into goats.", "c": "risk"},
          {"label": "Fence", "sub": "Ugly. Effective. Price it in year zero.", "c": "leaf"},
          {"label": "April watch", "sub": "Visible fruit is a magnet.", "c": "fruit"},
      ]),
    S("replant", "lag_cards",
      "Some plants will die. [pause] "
      "Replant in the next monsoon with the same named scion. [pause] "
      "Do not fill gaps with random seedlings 'just to occupy'. [pause] "
      "A gap is better than a genetic hole that never matches the row. [pause] "
      "Keep five spare grafts in a corner nursery if you can. [pause] "
      "The grid you saw computed only works if the stations stay true.",
      kicker="REPLANT",
      title="Same name in the gap, or leave it",
      cols=2, foot="A seedling gap-fill is how orchards become chaos.",
      items=[
          {"label": "Expect deaths", "sub": "Unions fail. Floods happen. Plan spares.", "c": "risk"},
          {"label": "Next monsoon", "sub": "Replant named. Same grid point.", "c": "leaf"},
          {"label": "Corner nursery", "sub": "Five extra grafts save a year of hunting.", "c": "cool"},
          {"label": "No random fill", "sub": "Off-type trees steal space forever.", "c": "fruit"},
      ]),
])

_insert("lag-ch07-years", [
    S("y47", "lag_time",
      "Between first fruit and peak there is a long middle. [pause] "
      "Year four to six: crop grows if water and feed stay honest. [pause] "
      "Year seven to ten: this is when a well-run acre starts to look like a business. [pause] "
      "Do not raise household spend in year four because one good crate happened. [pause] "
      "Biennial hints can appear if you overbear and underfeed. [pause] "
      "Steady beats heroic.",
      kicker="THE MIDDLE YEARS",
      title="Year seven is when it starts to look real",
      foot="Lifestyle creep in year four is how orchards get sold.",
      steps=[
          {"y": "Y3", "label": "Rehearsal", "sub": "Small crop", "c": "cool"},
          {"y": "Y4–6", "label": "Build", "sub": "If you keep feeding", "c": "leaf"},
          {"y": "Y7–10", "label": "Business", "sub": "Volume + skill", "c": "fruit"},
          {"y": "Y11–14", "label": "Climb", "sub": "Toward peak", "c": "leaf"},
          {"y": "Y15+", "label": "Plateau", "sub": "Maintain, don’t neglect", "c": "fruit"},
      ]),
    S("train2", "lag_cards",
      "Training systems, in practice. [pause] "
      "Central leader: one trunk, tiers of branches, good for a grid. [pause] "
      "Open centre: a vase, light into the middle, easy picking. [pause] "
      "Pick one in year one. Switching in year eight is a wood tax. [pause] "
      "Remove forks that rub. Remove branches that shoot straight up after a savage cut. [pause] "
      "The goal is a person with a clipper who can reach clusters without a death ladder.",
      kicker="FRAME",
      title="Leader or vase — pick once",
      cols=2, foot="Picking safety is a yield practice.",
      items=[
          {"label": "Central leader", "sub": "Orderly grid. Needs consistent heading.", "c": "leaf"},
          {"label": "Open centre", "sub": "Light in the vase. Watch for split crotches.", "c": "cool"},
          {"label": "Reach", "sub": "If you need a tall ladder for every bunch, the frame failed.", "c": "fruit"},
          {"label": "Rubbing wood", "sub": "Wounds are disease doors. Cut them.", "c": "risk"},
      ]),
    S("record", "lag_cards",
      "Write things down. [pause] "
      "Plant date. Scion. Dead stations. First bloom date. First crate weight. Mandi price that week. [pause] "
      "Without notes, year six you will argue with yourself. [pause] "
      "A cheap notebook beats a myth about 'the trees that used to bear'. [pause] "
      "Photo the union on day one. [pause] "
      "Future you is a different farmer. Leave them evidence.",
      kicker="RECORDS",
      title="A notebook is part of the orchard",
      cols=3, foot="Memory is not agronomy.",
      items=[
          {"label": "Plant log", "sub": "Date, name, source nursery.", "c": "leaf"},
          {"label": "Harvest log", "sub": "Kilos, grade, price, wastage.", "c": "fruit"},
          {"label": "Photo union", "sub": "Day one. Disputes end.", "c": "cool"},
      ]),
])

_insert("lag-ch08-care", [
    S("microfeed", "lag_cards",
      "Micronutrients. [pause] "
      "If leaves yellow in a pattern, do not dump more urea blindly. [pause] "
      "Iron, zinc, and manganese issues show up on some calcareous soils. [pause] "
      "Leaflets say foliar correction when symptoms are clear. [pause] "
      "A soil test every few years is cheaper than a yellow mystery. [pause] "
      "Green leaves are not vanity. They are next year’s clusters.",
      kicker="MICRONUTRIENTS",
      title="Yellow is a question, not more urea",
      cols=3, foot="Match the symptom to a test, not to a shopkeeper’s bag.",
      items=[
          {"label": "Soil test", "sub": "Every few years. Especially if leaves misbehave.", "c": "cool"},
          {"label": "Foliar fix", "sub": "When a named deficiency is diagnosed.", "c": "leaf"},
          {"label": "Urea dump", "sub": "The usual wrong answer.", "c": "risk"},
      ]),
    S("drip", "lag_cards",
      "Drip design, briefly. [pause] "
      "Two laterals per row once canopies widen, or a ring of points in the basin. [pause] "
      "Keep emitters off the trunk. Wet trunk plus fungus is a classic own-goal. [pause] "
      "Filter the water. Loquat drip fails as plumbing more than as agronomy. [pause] "
      "Flush lines. [pause] "
      "If power is erratic, a small tank and gravity still beats a cracked flood basin.",
      kicker="DRIP",
      title="Wet the roots. Not the trunk.",
      cols=2, foot="Clogged emitters in April are a yield event.",
      items=[
          {"label": "Basin ring", "sub": "Where the feeder roots actually are.", "c": "cool"},
          {"label": "Off trunk", "sub": "Dry collar. Wet soil.", "c": "leaf"},
          {"label": "Filter + flush", "sub": "Plumbing is plant care.", "c": "fruit"},
          {"label": "Power gaps", "sub": "Tank buffer. Fruit swell will not wait.", "c": "risk"},
      ]),
    S("thinhow", "lag_cards",
      "How to thin, practically. [pause] "
      "When fruit is marble size, remove the smallest and the damaged. [pause] "
      "Leave a cluster that can colour without a pile of touching skins. [pause] "
      "Touching skins in a tight bunch rot together in the crate. [pause] "
      "Work from the outside of the tree in. [pause] "
      "Stop when your hands say the remaining fruit can grow. Greed is a small-fruit machine.",
      kicker="THINNING HOW",
      title="Marble size. Small ones off. Air in the bunch.",
      cols=3, foot="A crowded bunch is a rot bunch.",
      items=[
          {"label": "Marble stage", "sub": "Early enough that remaining fruit swell.", "c": "fruit"},
          {"label": "Damaged first", "sub": "Scars and insect hits never become A grade.", "c": "risk"},
          {"label": "Air", "sub": "Skins that do not kiss survive the crate.", "c": "cool"},
      ]),
])

_insert("lag-ch09-harvest", [
    S("ripe", "lag_cards",
      "Ripe signs, in words you can use at dawn. [pause] "
      "Background colour leaves green. Yellow-orange takes over. [pause] "
      "A light floral smell. A slight give. The cluster looks even. [pause] "
      "If three fruits are green and four are collapsing, you waited on the wrong story. Pick the ready ones as a bunch only when the bunch is ready. [pause] "
      "Some orchards pick in two waves a week apart. [pause] "
      "Two waves need two labour days. Budget them.",
      kicker="RIPENESS",
      title="Colour, smell, give — then clip",
      cols=2, foot="A mixed-ripe bunch is a packing problem.",
      items=[
          {"label": "Colour shift", "sub": "Green ground colour gone.", "c": "fruit"},
          {"label": "Smell", "sub": "Floral-sweet. Not grassy.", "c": "leaf"},
          {"label": "Give", "sub": "Gentle press. Not mush.", "c": "cool"},
          {"label": "Two waves", "sub": "Possible. Costs a second crew day.", "c": "risk"},
      ]),
    S("tools", "lag_cards",
      "Tools. [pause] "
      "Sharp clippers. Harvest bags or shallow crates. A shaded trolley. [pause] "
      "Gloves if sap bothers skin. A stone for the clipper at lunch. [pause] "
      "No fertilizer sack as a crate. It sweats and crushes. [pause] "
      "No throwing clusters into a trailer from six feet. [pause] "
      "Treat them like eggs that stain.",
      kicker="KIT",
      title="Clippers, shallow crates, shade",
      cols=3, foot="The tool list is short. Skipping it is expensive.",
      items=[
          {"label": "Clippers", "sub": "Sharp. Disinfect if disease is in the block.", "c": "leaf"},
          {"label": "Shallow crate", "sub": "Clusters hate depth.", "c": "fruit"},
          {"label": "Shade", "sub": "Trolley or net. Field heat is the enemy.", "c": "cool"},
      ]),
    S("waste", "lag_bars",
      "Wastage is a yield number too. [pause] "
      "A model: ten percent lost to birds, five to crush, five to rot if you are sloppy. [pause] "
      "That is not a lab result. It is a warning. [pause] "
      "Netting and shallow crates and morning picks cut that curve. [pause] "
      "If you count only tree kilos, you will hate the mandi. [pause] "
      "Count kilos that a buyer paid for.",
      kicker="WASTAGE",
      title="Tree kilos are not sold kilos",
      unit="%",
      foot="Design against birds and crush before you brag yield.",
      bars=[
          {"label": "Sold", "v": 80, "c": "leaf"},
          {"label": "Birds", "v": 10, "c": "risk"},
          {"label": "Crush", "v": 5, "c": "fruit"},
          {"label": "Rot", "v": 5, "c": "cool"},
      ]),
])

_insert("lag-ch10-protect", [
    S("birds", "lag_cards",
      "Birds love coloured fruit at the edge of the canopy. [pause] "
      "They teach you which clusters were ready. Then they eat them. [pause] "
      "Netting a few trees is possible. Netting ten acres is a project. [pause] "
      "Reflective tape is a maybe. Dogs are not a bird plan. [pause] "
      "Harvest a little earlier on the outer colour if theft by beak is severe — flavour tradeoff. [pause] "
      "Watch one dawn. Count pecks. Then spend.",
      kicker="BIRDS",
      title="They harvest the best fruit first",
      cols=2, foot="A dawn count beats a late netting regret.",
      items=[
          {"label": "Edges first", "sub": "Colour plus access. That is bird logic.", "c": "risk"},
          {"label": "Net a block", "sub": "Works small. Plan labour to drape and undrape.", "c": "leaf"},
          {"label": "Tape / scare", "sub": "Partial. Birds get bored of your cleverness.", "c": "cool"},
          {"label": "Earlier clip", "sub": "Last resort. Flavour pays the tax.", "c": "fruit"},
      ]),
    S("spray", "lag_cards",
      "A spray philosophy that will not age as badly as a product name. [pause] "
      "Scout. Identify. Then choose a legal product with the K V K. [pause] "
      "Cover the underside of leaves for aphids. [pause] "
      "Rotate modes of action if you spray more than once. [pause] "
      "Record the date. Respect pre-harvest interval so April fruit is not a residue story. [pause] "
      "Hotels will not take a mystery chemical smell.",
      kicker="SPRAY RULES",
      title="Scout. Legal. Interval. Record.",
      cols=2, foot="Residue is a market pest.",
      items=[
          {"label": "Scout first", "sub": "No calendar dump 'because mango does'.", "c": "leaf"},
          {"label": "P H I", "sub": "Pre-harvest interval is part of ripening.", "c": "fruit"},
          {"label": "Under leaf", "sub": "Aphids live there. Spray the sky and you miss.", "c": "cool"},
          {"label": "Write it", "sub": "Date, product, reason. Future you needs this.", "c": "risk"},
      ]),
    S("cold", "lag_cards",
      "Cold. [pause] "
      "A household fridge is not a packhouse. A few crates overnight, maybe. [pause] "
      "Do not freeze loquat. Texture dies. [pause] "
      "If you ever get a cold room, keep it gentle and do not mix with onion. [pause] "
      "Most Indian growers will not have this. Design for ambient shade and speed instead. [pause] "
      "Fantasy cold-chain is how people skip the tempo booking.",
      kicker="COLD REALITY",
      title="Shade and speed beat a fictional packhouse",
      cols=3, foot="Book the vehicle before the clip.",
      items=[
          {"label": "No freeze", "sub": "Ice crystals wreck dessert fruit.", "c": "risk"},
          {"label": "Brief chill", "sub": "A few crates, maybe. Not a season.", "c": "cool"},
          {"label": "Speed", "sub": "The real cold chain is a fast road.", "c": "fruit"},
      ]),
])

_insert("lag-ch11-costs", [
    S("scenarios", "lag_cards",
      "Three money stories, spoken. [pause] "
      "Homestead: twenty trees. You eat and gift. Costs are pride and water. Fine. [pause] "
      "One to three acres, diversified: the model this course respects. [pause] "
      "Ten acres as the only crop: you need a buyer letter, a crew, and a stomach for April. Most people should not. [pause] "
      "Credit: do not hypothecate the house for a niche fruit you have never harvested. [pause] "
      "Scale is not a virtue here. Fit is.",
      kicker="SCALE STORIES",
      title="Twenty trees. Three acres. Not ten as only crop.",
      cols=3, foot="Borrow against a crop you have already sold once, if ever.",
      items=[
          {"label": "Homestead", "sub": "Joy plus a crate. Not a D P R.", "c": "leaf"},
          {"label": "1–3 acres", "sub": "Diversified. The serious path.", "c": "fruit"},
          {"label": "Ten acres solo", "sub": "Rarely wise on a first loquat attempt.", "c": "risk"},
      ]),
    S("rev", "lag_cards",
      "Revenue arithmetic you can redo with a pencil. [pause] "
      "Kilos sold times rupees per kilo. That is it. [pause] "
      "Conservative peak: seven quintals times eighty rupees is about fifty-six thousand an acre. [pause] "
      "Managed peak: twenty quintals times one hundred twenty is about two lakh forty thousand. [pause] "
      "Subtract wastage, commission, crates, and the year you miss bloom. [pause] "
      "If the lower number cannot live beside your other crops, do not plant for money.",
      kicker="PENCIL MATH",
      title="Sold kilos times farm-gate rupees",
      cols=2, foot="Commission and rot are not rounding errors.",
      items=[
          {"label": "Low story", "sub": "~7 qtl × ₹80 ≈ ₹56,000 at peak acre.", "c": "risk"},
          {"label": "High story", "sub": "~20 qtl × ₹120 ≈ ₹2.4 lakh if you are excellent.", "c": "leaf"},
          {"label": "Minus", "sub": "Mandi cut, crates, bird tax, a bad frost year.", "c": "cool"},
          {"label": "Beside other crops", "sub": "If loquat must carry the farm, stop.", "c": "fruit"},
      ]),
    S("subsidy", "lag_cards",
      "Schemes. [pause] "
      "There is no famous national loquat mission with a poster. [pause] "
      "You may still stack drip subsidy, farm pond, or general horticulture planting support if your state allows the species. [pause] "
      "Ask horticulture department, not a WhatsApp forward. [pause] "
      "Never plant because a subsidy exists. Plant because April fruit has a buyer. [pause] "
      "Subsidy is a discount on a good idea, or a lure into a bad one.",
      kicker="SUBSIDY",
      title="No loquat mission. Maybe drip help.",
      cols=3, foot="Paperwork after agronomy, never before.",
      items=[
          {"label": "Ask the dept", "sub": "Species lists change. Get it in writing.", "c": "cool"},
          {"label": "Drip / pond", "sub": "Often the real lever, crop-agnostic.", "c": "leaf"},
          {"label": "Not a reason", "sub": "Subsidy without a mandi is a trap.", "c": "risk"},
      ]),
])

_insert("lag-ch12-verdict", [
    S("fpo", "lag_cards",
      "Collectives. [pause] "
      "An F P O that already sells fruit can add a four-week loquat crate if several members plant. [pause] "
      "A lone farmer with two acres inventing a brand in Delhi is swimming in glue. [pause] "
      "Share a tempo. Share a mandi agent relationship. Share a jam kettle maybe. [pause] "
      "Do not share a spray pump that just did a restricted chemical. [pause] "
      "Cooperation is logistics. It is not a substitute for cool winters.",
      kicker="COLLECTIVES",
      title="Share the tempo, not the climate requirement",
      cols=2, foot="An F P O cannot make a tropical plot fruit.",
      items=[
          {"label": "Shared truck", "sub": "The unglamorous win.", "c": "fruit"},
          {"label": "Shared agent", "sub": "Someone who already sells lukat weeks.", "c": "leaf"},
          {"label": "Shared kettle", "sub": "Only with hygiene rules.", "c": "cool"},
          {"label": "Not climate", "sub": "No group can vote a winter into existence.", "c": "risk"},
      ]),
    S("mistakes", "lag_cards",
      "The usual ways this fails. [pause] "
      "Wrong species from a roadside plant. [pause] "
      "Warm winter. [pause] "
      "Seedlings. Tight spacing. No April crew. [pause] "
      "Believing a lakh-a-month thumbnail. [pause] "
      "If you avoid those, you still might not get rich. You might get fruit. That is the honest prize.",
      kicker="FAILURE MODES",
      title="The five ways people waste years",
      cols=2, foot="Avoiding failure is the first profit.",
      items=[
          {"label": "Wrong tree", "sub": "Kaitha, bael, unnamed 'lagot'.", "c": "risk"},
          {"label": "Warm winter", "sub": "Leaves without a crop.", "c": "cool"},
          {"label": "Seed / crowd", "sub": "Late fruit, dark fruit, fights.", "c": "leaf"},
          {"label": "No April people", "sub": "Ripe fruit with no hands.", "c": "fruit"},
      ]),
    S("next", "lag_pipe",
      "If you still want to plant, the next thirty days. [pause] "
      "Call K V K. Visit a bearing tree in season — wait until April if you must. [pause] "
      "Get three nursery quotes with names. Walk the field at dawn. [pause] "
      "Price a fence and drip. Talk to a mandi commission agent about lukat weeks. [pause] "
      "Then plant a test line, not the whole farm. [pause] "
      "Expand only after you have sold a crate you grew.",
      kicker="NEXT THIRTY DAYS",
      title="Test line first. Whole farm later.",
      foot="A test row is agronomy. A ten-acre leap is a speech.",
      nodes=[
          {"label": "K V K", "sub": "Ask", "c": "leaf"},
          {"label": "Taste", "sub": "April tree", "c": "fruit"},
          {"label": "Quotes", "sub": "Named grafts", "c": "cool"},
          {"label": "Mandi", "sub": "Talk", "c": "fruit"},
          {"label": "Test row", "sub": "Then wait", "c": "risk"},
      ]),
], before_last=True)
