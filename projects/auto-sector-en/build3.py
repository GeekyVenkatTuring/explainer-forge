#!/usr/bin/env python3
"""Indian Auto Sector — Video 3: FORGED, CAST & MACHINED (English, Nova).
Reuses `au` scene set. Own narration (au/narration3.wav) + edit_decisions3.json.
Data: research/forged-cast-machined.md (Screener close 07-Aug-2026; Q1 FY27 / Jun-26
where available). YoY shown only where sourced. Education, not advice.
Run: python3 build3.py
"""
import json, os, subprocess, time, urllib.request

BASE = "http://127.0.0.1:17493"; PROFILE = "c488e05c-3407-46a3-874d-1b09b3aff78d"
GAP, PAUSE, ATEMPO = 0.5, 0.6, 0.95
PREFIX = "au"; NARR = "narration3.wav"; EDJSON = "edit_decisions3.json"
ROOT = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(ROOT, "..", ".."))
PUBLIC = os.path.join(REPO, "composer", "public", PREFIX); RAW = os.path.join(ROOT, "assets", "raw"); FIN = os.path.join(ROOT, "assets")
for d in (PUBLIC, RAW, os.path.join(ROOT, "artifacts")): os.makedirs(d, exist_ok=True)
BIZC, UP, MOAT, VAL = "#38BDF8", "#34D399", "#A78BFA", "#FBBF24"

SEGMENTS = [
 ("v3_title", "au_title",
  {"kicker": "AUTO & AUTO-COMPONENTS · PART 3 OF 6", "title": "Indian Auto Stocks\nForged, Cast & Machined",
   "sub": "23 companies · the metal backbone · what they do · P/E · moat"},
  "Welcome back. [pause] Part three goes under the skin of the car — to the metal backbone. "
  "The forging, casting and machining companies that make the crankshafts, axles, gears and "
  "fasteners every vehicle is built from. [pause] They're unglamorous, but some are world-class "
  "exporters. [pause] Watch how wildly their valuations differ — from eleven times earnings to over "
  "a hundred and sixty. [pause] Figures are approximate; verify on your terminal. Education, not advice."),

 ("f_d1", "au_divider",
  {"part": "PART ONE", "title": "Forging & Machining", "sub": "Crankshafts, beams and complex precision parts",
   "color": BIZC, "pips": 3, "at": 1},
  "First, the forging and machining names. [pause] They pound and cut steel and aluminium into "
  "the strongest parts of a vehicle — and the best of them export to the world."),

 ("f01_bhforge", "au_company",
  {"idx": "01 / 23", "kicker": "FORGING & MACHINING", "name": "Bharat Forge", "ticker": "BHARATFORG",
   "price": "₹2,265", "pe": "96.0×", "seg": "Forgings",
   "biz": ["The Kalyani group's flagship — a global forging leader",
           "Crankshafts, axles and structural forgings",
           "Also defence, aerospace, oil & gas and industrial"],
   "fin": {"pending": True, "qlabel": "Q1 FY27 due 10-Aug (not out)",
           "note": "One of the world's largest forging companies; defence is a fast-growing new leg."},
   "moat": "A global forging leader with deep engineering and a fast-growing defence arm — but cyclical, and richly valued.",
   "moatStrength": "WIDE"},
  "First, Bharat Forge — the giant of the group. [pause] The flagship of the Kalyani group, it's "
  "one of the world's largest forging companies, making crankshafts and axles for trucks, and "
  "increasingly parts for defence and aerospace. [pause] Its June-quarter results are due on the "
  "tenth of August. [pause] It trades at a steep ninety-six times earnings. [pause] "
  "Its moat is world-class scale and engineering — plus a promising defence business. But forging is cyclical."),

 ("f02_rkforge", "au_company",
  {"idx": "02 / 23", "kicker": "FORGING & MACHINING", "name": "Ramkrishna Forgings", "ticker": "RKFORGE",
   "price": "₹727", "pe": "115×", "seg": "Forgings",
   "biz": ["India's second-largest forging company",
           "Crankshafts, axle beams and gears, mainly for trucks",
           "Expanding into railways and defence"],
   "fin": {"qlabel": "Q1 FY27 · Jun 2026", "rev": {"to": 1217}, "pat": {"to": 47},
           "note": "Exports and railways are diversifying it beyond the truck cycle."},
   "moat": "India's number-two forger, diversifying into railways and exports — but leveraged, and priced at a very rich P/E.",
   "moatStrength": "NARROW"},
  "Second, Ramkrishna Forgings — the challenger. [pause] India's second-largest forger, it makes "
  "truck crankshafts and axle beams, and is pushing into railways and defence. [pause] "
  "Revenue was about twelve hundred crore, profit forty-seven crore. [pause] But the stock is "
  "expensive — a hundred and fifteen times earnings. [pause] "
  "Its moat is scale and diversification — though it carries debt, and the valuation leaves little room for error."),

 ("f03_mmfl", "au_company",
  {"idx": "03 / 23", "kicker": "FORGING & MACHINING", "name": "MM Forgings", "ticker": "MMFL",
   "price": "₹629", "pe": "31.0×", "seg": "Forgings",
   "biz": ["A Chennai-based steel-forging maker",
           "Crankshafts, front axle beams and castings",
           "A significant exporter of forged components"],
   "fin": {"qlabel": "Latest reported · Jun 2025", "rev": {"to": 362}, "pat": {"to": 19},
           "note": "A mid-size exporter, sensitive to the global truck cycle."},
   "moat": "A capable mid-size forging exporter — but small and cyclical, with no dominant edge.",
   "moatStrength": "NARROW"},
  "Third, MM Forgings — the exporter. [pause] This Chennai company forges crankshafts and axle "
  "beams, selling a lot overseas. [pause] It's mid-sized — revenue around three hundred sixty "
  "crore. [pause] It trades near thirty-one times earnings. [pause] "
  "Its moat is modest — a solid export business, but small and tied to the global truck cycle."),

 ("f04_sansera", "au_company",
  {"idx": "04 / 23", "kicker": "FORGING & MACHINING", "name": "Sansera Engineering", "ticker": "SANSERA",
   "price": "₹3,864", "pe": "71.7×", "seg": "Precision parts",
   "biz": ["Precision forging and machining of complex parts",
           "Connecting rods, rocker arms, crankshafts, gear-shift forks",
           "Diversifying into aerospace and EV-neutral parts"],
   "fin": {"qlabel": "Q1 FY27 · Jun 2026", "rev": {"to": 999, "yoy": "+28%", "up": True}, "pat": {"to": 62},
           "note": "Profit before tax nearly doubled — a strong quarter."},
   "moat": "An engineering moat in complex precision parts, spreading into aerospace and EV-agnostic products.",
   "moatStrength": "NARROW"},
  "Fourth, Sansera Engineering — the precision specialist. [pause] It makes complex forged and "
  "machined parts, and is smartly diversifying into aerospace and parts that don't care whether a "
  "car is petrol or electric. [pause] A strong quarter — revenue up twenty-eight percent to about "
  "a thousand crore. [pause] It trades near seventy-two times earnings. [pause] "
  "Its moat is engineering — the ability to make hard, critical parts, for cars and beyond."),

 ("f05_craftsman", "au_company",
  {"idx": "05 / 23", "kicker": "FORGING & MACHINING", "name": "Craftsman Automation", "ticker": "CRAFTSMAN",
   "price": "₹10,483", "pe": "58.5×", "seg": "Machining",
   "biz": ["Precision machining of powertrain and engine parts",
           "Aluminium die-cast products",
           "Plus an industrial and storage-solutions arm"],
   "fin": {"qlabel": "Q1 FY27 · Jun 2026", "rev": {"to": 2432}, "pat": {"to": 151},
           "note": "A key machining supplier to commercial-vehicle and off-highway makers."},
   "moat": "A leading precision-machining partner for CV and off-highway makers — capital-heavy, and richly valued.",
   "moatStrength": "NARROW"},
  "Fifth, Craftsman Automation — the machinist. [pause] It precision-machines engine and "
  "powertrain parts, makes aluminium castings, and runs an industrial arm. [pause] "
  "Revenue was about twenty-four hundred crore, profit a hundred fifty-one crore. [pause] "
  "It trades near fifty-nine times earnings. [pause] "
  "Its moat is being a trusted, hard-to-replace machining partner — though the business eats a lot of capital."),

 ("f06_cie", "au_company",
  {"idx": "06 / 23", "kicker": "FORGING & MACHINING", "name": "CIE Automotive India", "ticker": "CIEINDIA",
   "price": "₹410", "pe": "17.4×", "seg": "Multi-tech parts",
   "biz": ["Formerly Mahindra CIE — a diversified parts maker",
           "Forgings, castings, stampings, gears and magnetics",
           "Owned by Spain's CIE Automotive group"],
   "fin": {"qlabel": "Q2 CY26 · Jun 2026", "rev": {"to": 2621}, "pat": {"to": 236},
           "note": "Almost debt-free and EV-agnostic — and one of the cheapest here."},
   "moat": "A diversified, multi-technology parts platform with a global parent — cheap, debt-free and EV-neutral.",
   "moatStrength": "NARROW"},
  "Sixth, CIE Automotive India — the diversifier. [pause] Once Mahindra CIE, it now makes a bit of "
  "everything — forgings, castings, gears — under a Spanish parent. [pause] Revenue was about "
  "twenty-six hundred crore, profit two hundred thirty-six crore. [pause] "
  "Notably, it's cheap, near seventeen times earnings, and almost debt-free. [pause] "
  "Its moat is breadth — many technologies, many customers, and a business that doesn't fear the EV shift."),

 ("f07_kalyanifrg", "au_company",
  {"idx": "07 / 23", "kicker": "FORGING & MACHINING", "name": "Kalyani Forge", "ticker": "KALYANIFRG",
   "price": "₹635", "pe": "24.8×", "seg": "Precision forgings",
   "biz": ["A smaller Kalyani-family forging company",
           "Connecting rods, rocker arms, hubs and gears",
           "Supplies auto OEMs and engineering customers"],
   "fin": {"pending": True, "qlabel": "Q1 FY27 due 11-Aug (not out)",
           "note": "A niche precision forger — small next to the flagship Bharat Forge."},
   "moat": "A small niche forger in the Kalyani family — capable, but sub-scale against far bigger rivals.",
   "moatStrength": "WEAK"},
  "Seventh, Kalyani Forge — the small cousin. [pause] Part of the wider Kalyani family, it makes "
  "precision forged parts like connecting rods and hubs. [pause] Its results are due on the "
  "eleventh of August. [pause] It trades near twenty-five times earnings. [pause] "
  "Its moat is weak — it's a capable niche forger, but tiny beside giants like Bharat Forge."),

 # ---- CASTINGS & AXLES ----
 ("c_d2", "au_divider",
  {"part": "PART TWO", "title": "Castings & Axles", "sub": "Iron, aluminium and the parts that carry the load",
   "color": UP, "pips": 3, "at": 2},
  "Part two — castings and axles. [pause] The companies that pour metal into shape, and build the "
  "axles that literally carry the vehicle's weight. Many are quiet export specialists."),

 ("c08_alicon", "au_company",
  {"idx": "08 / 23", "kicker": "CASTINGS & AXLES", "name": "Alicon Castalloy", "ticker": "ALICON",
   "price": "₹743", "pe": "31.1×", "seg": "Aluminium castings",
   "biz": ["India's largest integrated aluminium-casting maker",
           "Cylinder heads, manifolds and structural parts",
           "Expanding into EV and defence castings"],
   "fin": {"qlabel": "Latest reported · Q4 FY26 (Mar-26)", "rev": {"to": 495}, "pat": {"to": 8},
           "note": "Lightweighting and EV parts are the growth story; margins are thin."},
   "moat": "India's largest aluminium caster, with lightweighting and EV/defence optionality — but wafer-thin margins.",
   "moatStrength": "NARROW"},
  "Eighth, Alicon Castalloy — the aluminium specialist. [pause] It's India's largest integrated "
  "aluminium-casting maker, and aluminium is exactly what carmakers want more of, to cut weight. "
  "[pause] Revenue was about five hundred crore, but profit only eight crore — margins are thin. "
  "[pause] It trades near thirty-one times earnings. [pause] "
  "Its moat is scale in aluminium casting, plus EV and defence optionality — if it can widen those margins."),

 ("c09_nelcast", "au_company",
  {"idx": "09 / 23", "kicker": "CASTINGS & AXLES", "name": "Nelcast", "ticker": "NELCAST",
   "price": "₹126", "pe": "26.6×", "seg": "Iron castings",
   "biz": ["One of India's largest iron-castings foundries",
           "Axle housings, brackets, differential cases, hubs",
           "For commercial vehicles, tractors and off-highway"],
   "fin": {"qlabel": "Q1 FY27 · Jun 2026", "rev": {"to": 341}, "pat": {"to": 5},
           "note": "High volumes, but low-margin jobbing-foundry economics."},
   "moat": "A large jobbing foundry with scale — but low-margin, commoditised, and tied to the CV cycle.",
   "moatStrength": "WEAK"},
  "Ninth, Nelcast — the iron founder. [pause] It's one of India's largest iron-castings foundries, "
  "making axle housings and hubs for trucks and tractors. [pause] Revenue was around three hundred "
  "forty crore, but profit just five crore. [pause] It trades near twenty-seven times earnings. [pause] "
  "Its moat is weak — casting iron is a scale game with thin, commoditised margins."),

 ("c10_pritika", "au_company",
  {"idx": "10 / 23", "kicker": "CASTINGS & AXLES", "name": "Pritika Auto Industries", "ticker": "PRITIKAUTO",
   "price": "₹18.2", "pe": "13.9×", "seg": "Tractor castings",
   "biz": ["Machined castings for tractors and vehicles",
           "Transmission housings, axle and hydraulic parts",
           "A tier-1 casting and machining supplier"],
   "fin": {"qlabel": "Q1 FY27 · Jun 2026", "rev": {"to": 145}, "pat": {"to": 7},
           "note": "A small penny-stock supplier to the tractor industry."},
   "moat": "A small tractor-parts caster — low-margin and sub-scale, with limited pricing power.",
   "moatStrength": "WEAK"},
  "Tenth, Pritika Auto — a tractor-parts minnow. [pause] It makes machined castings — housings and "
  "axle parts — mainly for tractors. [pause] It's tiny, a penny stock, with revenue around a "
  "hundred forty-five crore. [pause] It trades near fourteen times earnings. [pause] "
  "Its moat is limited — a small supplier with little pricing power in a competitive field."),

 ("c11_rolex", "au_company",
  {"idx": "11 / 23", "kicker": "CASTINGS & AXLES", "name": "Rolex Rings", "ticker": "ROLEXRINGS",
   "price": "₹157", "pe": "21.2×", "seg": "Bearing rings",
   "biz": ["A top-five forged bearing-ring maker",
           "Supplies global bearing companies and auto OEMs",
           "A large share of revenue is exports"],
   "fin": {"qlabel": "Q1 FY27 · Jun 2026", "rev": {"to": 304}, "pat": {"to": 60},
           "note": "Healthy margins for a forger — bearing rings are a specialised niche."},
   "moat": "A top-five forged bearing-ring maker with a big export share to global bearing giants — a real niche.",
   "moatStrength": "NARROW"},
  "Eleventh, Rolex Rings — no, not the watches. [pause] This Rajkot company forges bearing rings, "
  "selling to the world's big bearing makers. [pause] It's nicely profitable — revenue three hundred "
  "crore, profit sixty crore. [pause] It trades near twenty-one times earnings. [pause] "
  "Its moat is that specialised niche — being a trusted ring supplier to global bearing giants, mostly for export."),

 ("c12_gna", "au_company",
  {"idx": "12 / 23", "kicker": "CASTINGS & AXLES", "name": "GNA Axles", "ticker": "GNA",
   "price": "₹527", "pe": "17.1×", "seg": "Axle shafts",
   "biz": ["Makes rear axle shafts and driveline parts",
           "For commercial vehicles, tractors and off-highway",
           "A significant exporter to global OEMs"],
   "fin": {"qlabel": "Q1 FY27 · Jun 2026", "rev": {"to": 470}, "pat": {"to": 38},
           "note": "Strong export franchise keeps margins healthy."},
   "moat": "A focused axle-shaft exporter to global CV and tractor makers — a durable niche, reasonably priced.",
   "moatStrength": "NARROW"},
  "Twelfth, GNA Axles — the shaft specialist. [pause] It makes rear axle shafts for trucks and "
  "tractors, and exports a lot of them. [pause] Revenue was about four hundred seventy crore, "
  "profit thirty-eight crore. [pause] It trades near seventeen times earnings. [pause] "
  "Its moat is that export niche — a trusted supplier of a critical part to global drivetrain makers."),

 ("c13_autoaxles", "au_company",
  {"idx": "13 / 23", "kicker": "CASTINGS & AXLES", "name": "Automotive Axles", "ticker": "AUTOAXLES",
   "price": "₹1,828", "pe": "15.1×", "seg": "CV axles & brakes",
   "biz": ["A Kalyani–Meritor joint venture",
           "Drive and non-drive axles, plus brakes",
           "Mainly for truck and bus makers"],
   "fin": {"qlabel": "Q1 FY27 · Jun 2026", "rev": {"to": 517}, "pat": {"to": 46},
           "note": "Its fortunes ride the commercial-vehicle cycle closely."},
   "moat": "A leading CV axle maker via a strong JV — but its earnings rise and fall with the truck cycle.",
   "moatStrength": "NARROW"},
  "Thirteenth, Automotive Axles — the truck-axle leader. [pause] A joint venture between the "
  "Kalyani group and America's Meritor, it makes axles and brakes for trucks and buses. [pause] "
  "Revenue was about five hundred seventeen crore, profit forty-six crore. [pause] "
  "It trades near fifteen times earnings. [pause] "
  "Its moat is a leading position through a strong JV — but it lives and dies by the commercial-vehicle cycle."),

 ("c14_carraro", "au_company",
  {"idx": "14 / 23", "kicker": "CASTINGS & AXLES", "name": "Carraro India", "ticker": "CARRARO",
   "price": "₹502", "pe": "20.4×", "seg": "Axles & transmissions",
   "biz": ["Indian arm of Italy's Carraro group",
           "Axles, transmissions and driveline systems",
           "For tractors and construction equipment"],
   "fin": {"qlabel": "Q1 FY27 · Jun 2026", "rev": {"to": 545}, "pat": {"to": 31},
           "note": "Off-highway focused; recently listed, sensitive to farm-equipment demand."},
   "moat": "A driveline specialist for tractors and construction gear, backed by an Italian parent — but off-highway cyclical.",
   "moatStrength": "NARROW"},
  "Fourteenth, Carraro India — the off-highway driveline maker. [pause] The Indian arm of Italy's "
  "Carraro, it makes axles and transmissions for tractors and construction machines. [pause] "
  "Revenue was about five hundred forty-five crore, profit thirty-one crore. [pause] "
  "It trades near twenty times earnings. [pause] "
  "Its moat is specialised driveline know-how with a global parent — though demand swings with farming and construction."),

 ("c15_kross", "au_company",
  {"idx": "15 / 23", "kicker": "CASTINGS & AXLES", "name": "Kross", "ticker": "KROSS",
   "price": "₹203", "pe": "22.6×", "seg": "Trailer axles",
   "biz": ["Forged and machined parts, plus trailer axles",
           "Suspension products for heavy commercial vehicles",
           "A tier-1 maker of safety-critical driveline parts"],
   "fin": {"qlabel": "Q1 FY27 · Jun 2026", "rev": {"to": 184}, "pat": {"to": 13},
           "note": "A recently-listed, fast-growing CV-parts specialist."},
   "moat": "A newer specialist in safety-critical trailer axles and suspension for heavy trucks — an emerging niche.",
   "moatStrength": "EMERGING"},
  "Fifteenth, Kross — the newcomer. [pause] This Jamshedpur company makes trailer axles and "
  "suspension for heavy trucks — safety-critical parts. [pause] It's small and recently listed, "
  "with revenue around a hundred eighty-four crore. [pause] It trades near twenty-three times "
  "earnings. [pause] "
  "Its moat is emerging — a focused, fast-growing specialist in parts that trucks simply can't fail on."),

 # ---- FASTENERS, GEARS & TRANSMISSION ----
 ("g_d3", "au_divider",
  {"part": "PART THREE", "title": "Fasteners, Gears & Belts", "sub": "The small parts that hold it all together",
   "color": VAL, "pips": 3, "at": 3},
  "And part three — fasteners, gears and belts. [pause] The small, precise parts that literally "
  "hold a vehicle together and transmit its power. This is where a few quiet quality-champions hide."),

 ("g16_sundram", "au_company",
  {"idx": "16 / 23", "kicker": "FASTENERS · GEARS", "name": "Sundram Fasteners", "ticker": "SUNDRMFAST",
   "price": "₹1,091", "pe": "36.9×", "seg": "Fasteners",
   "biz": ["TVS-group maker of high-tensile fasteners",
           "Plus powder-metal parts, pumps, gears and hubs",
           "A major exporter, expanding into EV parts"],
   "fin": {"qlabel": "Q1 FY27 · Jun 2026", "rev": {"to": 1846}, "pat": {"to": 169},
           "note": "High-quality, export-heavy and EV-agnostic — a franchise business."},
   "moat": "A quality-and-relationships moat — a trusted global fastener supplier, EV-agnostic, with strong margins.",
   "moatStrength": "WIDE"},
  "Sixteenth, Sundram Fasteners — a quiet quality-champion. [pause] Part of the TVS group, it makes "
  "high-tensile fasteners and precision parts, and exports to the world's top carmakers. [pause] "
  "Revenue was about eighteen hundred crore, profit a hundred sixty-nine crore. [pause] "
  "It trades near thirty-seven times earnings. [pause] "
  "Its moat is wide — decades of quality and trust with global OEMs, on parts every vehicle needs, electric or not."),

 ("g17_sterling", "au_company",
  {"idx": "17 / 23", "kicker": "FASTENERS · GEARS", "name": "Sterling Tools", "ticker": "STERTOOLS",
   "price": "₹244", "pe": "46.1×", "seg": "Fasteners",
   "biz": ["A leading cold-forged fastener maker",
           "Supplies most major auto OEMs",
           "Building EV components through joint ventures"],
   "fin": {"qlabel": "Q1 FY27 · Jun 2026", "rev": {"to": 214}, "pat": {"to": 6},
           "note": "The number-two fastener maker, betting on EV parts for growth."},
   "moat": "A solid number-two in fasteners with OEM relationships and an EV-parts push — but a step below the leader.",
   "moatStrength": "NARROW"},
  "Seventeenth, Sterling Tools — the challenger fastener maker. [pause] It supplies bolts and "
  "fasteners to most big carmakers, and is building EV parts through joint ventures. [pause] "
  "Revenue was about two hundred fourteen crore, profit only six crore. [pause] "
  "Yet it trades near forty-six times earnings, on EV hopes. [pause] "
  "Its moat is decent OEM relationships — but it's the number two, chasing the leader."),

 ("g18_sintercom", "au_company",
  {"idx": "18 / 23", "kicker": "FASTENERS · GEARS", "name": "Sintercom India", "ticker": "SINTERCOM",
   "price": "₹83.7", "pe": "161×", "seg": "Sintered parts",
   "biz": ["Makes sintered, powder-metallurgy parts",
           "Net-shape components for engines and transmissions",
           "Lightweight parts for OEMs and tier-1s"],
   "fin": {"qlabel": "Latest reported · Q4 FY26 (Mar-26)", "rev": {"to": 101}, "pat": {"to": 1},
           "note": "Tiny earnings and an extreme valuation — priced for perfection."},
   "moat": "A niche in sintered net-shape parts — but tiny, with barely any profit and an extreme P/E.",
   "moatStrength": "WEAK"},
  "Eighteenth, Sintercom India — and a valuation warning. [pause] It makes sintered powder-metal "
  "parts — a clever, lightweight process. [pause] But it's tiny: revenue around a hundred crore, "
  "profit barely one crore. [pause] And yet the stock trades at a hundred sixty-one times "
  "earnings. [pause] "
  "Its moat is a genuine niche technology — but the price assumes flawless execution for years. Tread carefully."),

 ("g19_hitech", "au_company",
  {"idx": "19 / 23", "kicker": "FASTENERS · GEARS", "name": "The Hi-Tech Gears", "ticker": "HITECHGEAR",
   "price": "₹560", "pe": "53.4×", "seg": "Gears",
   "biz": ["Makes precision gears, shafts and transmission parts",
           "For two-wheelers, off-highway and commercial vehicles",
           "Supplies OEMs in India and abroad"],
   "fin": {"qlabel": "Q1 FY27 · Jun 2026", "rev": {"to": 238}, "pat": {"to": 5},
           "note": "A capable gear specialist, but small and modestly profitable."},
   "moat": "A tier-1 gear specialist with global customers — but small, with thin current profits.",
   "moatStrength": "NARROW"},
  "Nineteenth, Hi-Tech Gears — the gear cutter. [pause] It makes precision gears and transmission "
  "parts for two-wheelers and off-highway machines. [pause] Revenue was about two hundred thirty-eight "
  "crore, profit five crore. [pause] It trades near fifty-three times earnings. [pause] "
  "Its moat is precision-gear know-how and global customers — but it's small, and profits are thin for now."),

 ("g20_racl", "au_company",
  {"idx": "20 / 23", "kicker": "FASTENERS · GEARS", "name": "RACL Geartech", "ticker": "RACLGEAR",
   "price": "₹1,483", "pe": "35.1×", "seg": "Precision gears",
   "biz": ["Makes high-precision automotive gears",
           "Exports to premium European OEMs like BMW and KTM",
           "A niche precision-gear specialist"],
   "fin": {"qlabel": "Q1 FY27 · Jun 2026", "rev": {"to": 132}, "pat": {"to": 9},
           "note": "Small but premium — its customers are top European names."},
   "moat": "A precision-and-trust moat — a small Indian firm that supplies gears to demanding premium European brands.",
   "moatStrength": "EMERGING"},
  "Twentieth, RACL Geartech — the premium exporter. [pause] It's small, but it makes gears precise "
  "enough for BMW Motorrad and KTM in Europe. [pause] Revenue was about a hundred thirty-two crore, "
  "profit nine crore. [pause] It trades near thirty-five times earnings. [pause] "
  "Its moat is emerging but real — few Indian firms clear the quality bar of premium European OEMs. That's a hard-won edge."),

 ("g21_bhgear", "au_company",
  {"idx": "21 / 23", "kicker": "FASTENERS · GEARS", "name": "Bharat Gears", "ticker": "BHARATGEAR",
   "price": "₹106", "pe": "10.9×", "seg": "Ring gears",
   "biz": ["One of India's largest makers of ring gears",
           "Crown wheels and pinions for CVs and tractors",
           "Also runs a heat-treatment business"],
   "fin": {"qlabel": "Q1 FY27 · Jun 2026", "rev": {"to": 216},
           "note": "Revenue is fine, but it barely broke even — net profit just ₹0.15 crore."},
   "moat": "A long-standing gear maker with scale — but wafer-thin profits keep it a value trap risk, despite a cheap P/E.",
   "moatStrength": "WEAK"},
  "Twenty-first, Bharat Gears — cheap for a reason. [pause] It's a large maker of ring gears for "
  "trucks and tractors. [pause] Revenue was healthy, over two hundred crore — but it barely broke "
  "even, with profit of just fifteen lakh. [pause] That's why it looks cheap, near eleven times "
  "earnings. [pause] "
  "Its moat is weak — real scale, but no pricing power, so the profits just aren't there. A classic value trap risk."),

 ("g22_lgb", "au_company",
  {"idx": "22 / 23", "kicker": "FASTENERS · GEARS", "name": "LG Balakrishnan (Rolon)", "ticker": "LGBBROSLTD",
   "price": "₹1,524", "pe": "15.2×", "seg": "Chains & sprockets",
   "biz": ["The dominant maker of two-wheeler chains and sprockets",
           "Sold under the Rolon brand",
           "OEM, aftermarket and exports"],
   "fin": {"qlabel": "Q1 FY27 · Jun 2026", "rev": {"to": 799}, "pat": {"to": 67},
           "note": "A strong franchise trading at a surprisingly cheap valuation."},
   "moat": "A dominant, trusted brand in two-wheeler chains (Rolon) — a wide franchise, and cheap at 15× earnings.",
   "moatStrength": "WIDE"},
  "Twenty-second, LG Balakrishnan — the chain king. [pause] Under the Rolon brand, it dominates "
  "two-wheeler chains and sprockets, in both new bikes and the aftermarket. [pause] Revenue was "
  "about eight hundred crore, profit sixty-seven crore. [pause] And it's cheap — near fifteen times "
  "earnings. [pause] "
  "Its moat is wide — a trusted, dominant brand in a part every bike needs, at a value price. One to remember."),

 ("g23_pix", "au_company",
  {"idx": "23 / 23", "kicker": "FASTENERS · GEARS", "name": "Pix Transmissions", "ticker": "PIXTRANS",
   "price": "₹1,717", "pe": "17.8×", "seg": "Power-transmission belts",
   "biz": ["A leading maker of V-belts and timing belts",
           "For automotive, agricultural and industrial use",
           "A big exporter across the world"],
   "fin": {"qlabel": "Q1 FY27 · Jun 2026", "rev": {"to": 149}, "pat": {"to": 53},
           "note": "Remarkable margins — over a third of revenue drops to profit."},
   "moat": "A high-margin, export-heavy belt specialist — a focused niche with pricing power few components makers enjoy.",
   "moatStrength": "NARROW"},
  "And twenty-third, Pix Transmissions — the belt maker. [pause] It makes power-transmission belts "
  "for engines and machinery, exported worldwide. [pause] Look at the margins — on revenue of about "
  "a hundred fifty crore, it made fifty-three crore in profit. [pause] It trades near eighteen times "
  "earnings. [pause] "
  "Its moat is a focused, high-margin niche with real pricing power — rare for a components company."),

 ("v3_recap", "au_recap",
  {"title": "The Metal Backbone — in one breath", "color": BIZC,
   "items": [
     "Forging & machining: Bharat Forge, Sansera, Craftsman lead",
     "Export niches shine — GNA, Rolex Rings, RACL, Pix",
     "Sundram Fasteners & LG Balakrishnan: quiet quality franchises",
     "Castings are low-margin; axles ride the truck cycle",
     "Valuations are all over — from 11× to 161× earnings",
     "Cheap isn't always good — Bharat Gears barely earns",
     "EV-agnostic parts makers are the safest bet on the shift",
   ],
   "closer": "The backbone is unglamorous — but quality, niches and exports quietly compound."},
  "So, in one breath. [pause] Forging and machining is led by Bharat Forge, Sansera and Craftsman — "
  "big, capable, but cyclical. [pause] The real gems are the export niches: GNA, Rolex Rings, RACL "
  "and Pix, each dominating a tiny corner of the world. [pause] Sundram Fasteners and LG Balakrishnan "
  "are quiet quality franchises worth remembering. [pause] Castings stay low-margin, and axle makers "
  "ride the truck cycle. [pause] And notice the valuations — from eleven times to a hundred sixty-one. "
  "Cheap isn't always good; Bharat Gears barely earns a rupee. [pause] "
  "The lesson: this backbone is unglamorous, but quality, niches and exports quietly compound. [pause] "
  "Next time, the chassis, braking and suspension makers. Thanks for watching."),
]


def post(p, b):
    req = urllib.request.Request(BASE + p, data=json.dumps(b).encode(), headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(req, timeout=30) as r: return json.loads(r.read().decode())
def get(p):
    with urllib.request.urlopen(BASE + p, timeout=30) as r: return r.read()
def tts_chunk(path, text):
    gid = post("/generate", {"profile_id": PROFILE, "text": text, "engine": "kokoro"})["id"]
    for _ in range(300):
        raw = get(f"/generate/{gid}/status").decode()
        line = [l for l in raw.splitlines() if l.startswith("data:")]
        st = json.loads(line[-1][5:].strip()) if line else None
        if st and st.get("status") == "completed": break
        time.sleep(1)
    open(path, "wb").write(get(f"/audio/{gid}"))
def gen_one(seg_id, text):
    fin = os.path.join(FIN, seg_id + ".wav")
    if os.path.exists(fin):
        out = subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","default=noprint_wrappers=1:nokey=1",fin], capture_output=True, text=True, check=True)
        return fin, round(float(out.stdout.strip()), 3)
    chunks = [c.strip() for c in text.split("[pause]") if c.strip()]; paths = []
    for ci, chunk in enumerate(chunks):
        cp = os.path.join(RAW, f"{seg_id}_c{ci}.wav")
        if not os.path.exists(cp): tts_chunk(cp, chunk)
        paths.append(cp)
    psil = os.path.join(RAW, "_pause.wav")
    if not os.path.exists(psil):
        subprocess.run(["ffmpeg","-y","-f","lavfi","-i","anullsrc=r=24000:cl=mono","-t",str(PAUSE),psil], check=True, capture_output=True)
    clist = os.path.join(RAW, f"{seg_id}_concat.txt")
    with open(clist, "w") as f:
        for i2, p2 in enumerate(paths):
            f.write(f"file '{p2}'\n")
            if i2 < len(paths) - 1: f.write(f"file '{psil}'\n")
    af = f"atempo={ATEMPO}" if ATEMPO != 1.0 else "anull"
    subprocess.run(["ffmpeg","-y","-f","concat","-safe","0","-i",clist,"-filter:a",af,fin], check=True, capture_output=True)
    out = subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","default=noprint_wrappers=1:nokey=1",fin], capture_output=True, text=True, check=True)
    return fin, round(float(out.stdout.strip()), 3)

manifest = []
for sid, variant, props, text in SEGMENTS:
    path, dur = gen_one(sid, text)
    manifest.append({"id": sid, "variant": variant, "props": props, "wav": path, "duration": dur})
    print(f"  {sid:14s} {dur:6.2f}s", flush=True)
silence = os.path.join(FIN, "_sil.wav")
subprocess.run(["ffmpeg","-y","-f","lavfi","-i","anullsrc=r=24000:cl=mono","-t",str(GAP),silence], check=True, capture_output=True)
concat_list = os.path.join(ROOT, "concat3.txt")
with open(concat_list, "w") as f:
    for i, m in enumerate(manifest):
        f.write(f"file '{m['wav']}'\n")
        if i < len(manifest) - 1: f.write(f"file '{silence}'\n")
subprocess.run(["ffmpeg","-y","-f","concat","-safe","0","-i",concat_list,"-c","copy",os.path.join(PUBLIC, NARR)], check=True, capture_output=True)
cuts, t = [], 0.0
for m in manifest:
    start, end = t, t + m["duration"]
    cuts.append({"id": m["id"], "type": m["variant"], "in_seconds": round(start,3), "out_seconds": round(end,3), "props": {**m["props"], "dur": round(m["duration"]+GAP,3)}})
    t = end + GAP
json.dump({"cuts": cuts, "audio": {"narration": {"src": f"{PREFIX}/{NARR}", "volume": 1.0}}}, open(os.path.join(ROOT, "artifacts", EDJSON), "w"), indent=2)
print(f"total {t-GAP:.2f}s ({(t-GAP)/60:.2f} min), {len(cuts)} scenes")
