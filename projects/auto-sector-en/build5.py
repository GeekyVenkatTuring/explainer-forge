#!/usr/bin/env python3
"""Indian Auto Sector — Video 5: ENGINE, BEARINGS & DRIVETRAIN (English, Nova).
Reuses `au` scene set. Own narration (au/narration5.wav) + edit_decisions5.json.
Data: research/engine-bearings-electricals.md (Screener close 07-Aug-2026). Education, not advice.
Run: python3 build5.py
"""
import json, os, subprocess, time, urllib.request
BASE="http://127.0.0.1:17493"; PROFILE="c488e05c-3407-46a3-874d-1b09b3aff78d"
GAP,PAUSE,ATEMPO=0.5,0.6,0.95; PREFIX="au"; NARR="narration5.wav"; EDJSON="edit_decisions5.json"
ROOT=os.path.dirname(os.path.abspath(__file__)); REPO=os.path.abspath(os.path.join(ROOT,"..",".."))
PUBLIC=os.path.join(REPO,"composer","public",PREFIX); RAW=os.path.join(ROOT,"assets","raw"); FIN=os.path.join(ROOT,"assets")
for d in (PUBLIC,RAW,os.path.join(ROOT,"artifacts")): os.makedirs(d,exist_ok=True)
BIZC,UP,MOAT,VAL="#38BDF8","#34D399","#A78BFA","#FBBF24"

SEGMENTS=[
 ("v5_title","au_title",
  {"kicker":"AUTO & AUTO-COMPONENTS · PART 5 OF 6","title":"Indian Auto Stocks\nEngine, Bearings & Drivetrain",
   "sub":"23 companies · pistons · bearings · gears · steering · P/E · moat"},
  "Welcome back. [pause] Part five is the heart of the machine — the engine internals, bearings and "
  "drivetrain. [pause] Pistons, camshafts, bearings, differentials and steering. [pause] This is where "
  "the big global names live — Bosch, Schaeffler, S-K-F — alongside the company leading India into "
  "electric drivetrains. [pause] Same four things for each. Figures approximate; verify on your terminal. "
  "Education, not advice."),

 ("e_d1","au_divider",{"part":"PART ONE","title":"Engine & Fuel Internals","sub":"Pistons, rings, camshafts and castings","color":BIZC,"pips":3,"at":1},
  "First, the engine internals. [pause] Pistons, rings, camshafts — the parts that take the heat and "
  "pressure inside a combustion engine. A group facing the long EV question, but earning well today."),

 ("e01_bosch","au_company",
  {"idx":"01 / 23","kicker":"ENGINE INTERNALS","name":"Bosch","ticker":"BOSCHLTD","price":"₹42,950","pe":"60.7×","seg":"Fuel & electronics",
   "biz":["India's largest auto-components company","Fuel-injection systems, electronics, starters","Plus industrial and building technology"],
   "fin":{"qlabel":"Latest reported · Q4 FY26 (Mar-26)","rev":{"to":5566},"pat":{"to":570},"note":"The German giant's India arm — deep tech and a huge aftermarket."},
   "moat":"India's biggest components maker with world-class technology and an unrivalled aftermarket — a wide, durable moat.","moatStrength":"WIDE"},
  "First, Bosch — the German giant. [pause] It's India's largest auto-components company, famous for "
  "fuel-injection and vehicle electronics, plus a vast aftermarket. [pause] Revenue was about "
  "fifty-five hundred crore, profit five hundred seventy crore. [pause] It trades near sixty-one times "
  "earnings, and above forty-two thousand rupees a share. [pause] "
  "Its moat is wide — world-class technology, scale, and a service network that spans the country."),

 ("e02_fmgoetze","au_company",
  {"idx":"02 / 23","kicker":"ENGINE INTERNALS","name":"Federal-Mogul Goetze","ticker":"FMGOETZE","price":"₹492","pe":"15.0×","seg":"Pistons & rings",
   "biz":["Pistons, piston rings and cylinder liners","Part of the global Tenneco / Federal-Mogul group","For engines and the aftermarket"],
   "fin":{"qlabel":"Latest reported · Q1 FY26 (Jun-25)","rev":{"to":484},"pat":{"to":45},"note":"Cheap for the sector — but its products are tied to combustion engines."},
   "moat":"A leading piston-and-ring maker with global backing — but ICE-tied, which caps the multiple.","moatStrength":"NARROW"},
  "Second, Federal-Mogul Goetze — the piston maker. [pause] Part of the global Tenneco group, it makes "
  "pistons and rings for engines. [pause] Revenue was about four hundred eighty crore, profit "
  "forty-five crore. [pause] It's cheap, near fifteen times earnings. [pause] "
  "Its moat is global technology and brand — but its core parts belong to the combustion engine, which is why it's cheap."),

 ("e03_spr","au_company",
  {"idx":"03 / 23","kicker":"ENGINE INTERNALS","name":"SPR Auto (Shriram Pistons)","ticker":"SHRIPISTON","price":"₹4,393","pe":"33.2×","seg":"Engine parts",
   "biz":["Pistons, rings and engine valves","Brands like SPR, Kolben and USHA","Diversifying into EV motors and controllers"],
   "fin":{"qlabel":"Q1 FY27 · Jun 2026","rev":{"to":1474},"pat":{"to":148},"note":"Using engine-parts cash to build an EV-components arm."},
   "moat":"A leading engine-parts maker funding an EV pivot — a smart hedge, but the transition is still young.","moatStrength":"NARROW"},
  "Third, SPR Auto — formerly Shriram Pistons. [pause] It makes pistons, rings and valves, and is "
  "using that cash to build EV motors and controllers. [pause] Revenue was about fifteen hundred "
  "crore, profit a hundred forty-eight crore. [pause] It trades near thirty-three times earnings. [pause] "
  "Its moat is a strong engine-parts business — and a sensible bet to reinvent itself for the electric age."),

 ("e04_menonpis","au_company",
  {"idx":"04 / 23","kicker":"ENGINE INTERNALS","name":"Menon Pistons","ticker":"MENNPIS","price":"₹74","pe":"14.4×","seg":"Diesel pistons",
   "biz":["Pistons and piston pins for diesel engines","For trucks, tractors, gensets and industry","A Kolhapur-based supplier"],
   "fin":{"qlabel":"Q1 FY27 · Jun 2026","rev":{"to":83},"pat":{"to":8},"note":"Small, steady and among the cheapest in the sector."},
   "moat":"A small, focused diesel-piston maker — steady and cheap, but with limited scale and pricing power.","moatStrength":"NARROW"},
  "Fourth, Menon Pistons — small and cheap. [pause] This Kolhapur company makes pistons for diesel "
  "engines in trucks and tractors. [pause] Revenue was about eighty crore, profit eight crore. [pause] "
  "It's among the cheapest here, near fourteen times earnings. [pause] "
  "Its moat is narrow — a focused, steady supplier, but too small to command real pricing power."),

 ("e05_precam","au_company",
  {"idx":"05 / 23","kicker":"ENGINE INTERNALS","name":"Precision Camshafts","ticker":"PRECAM","price":"₹143","pe":"55.2×","seg":"Camshafts",
   "biz":["A leading global maker of cast camshafts","For passenger cars, tractors and industry","Diversifying into non-camshaft and EV-neutral parts"],
   "fin":{"qlabel":"Q1 FY27 · Jun 2026","rev":{"to":195},"pat":{"to":19},"note":"A global camshaft leader hedging against the EV shift."},
   "moat":"A global leader in cast camshafts — a real niche, now diversifying so the EV shift doesn't strand it.","moatStrength":"NARROW"},
  "Fifth, Precision Camshafts — the camshaft king. [pause] From Solapur, it's a leading global maker "
  "of cast camshafts, and it's diversifying into parts that don't depend on the engine. [pause] "
  "Revenue was about a hundred ninety-five crore, profit nineteen crore. [pause] It trades near "
  "fifty-five times earnings. [pause] "
  "Its moat is a genuine global niche in camshafts — with a sensible move to hedge the electric future."),

 ("e06_rico","au_company",
  {"idx":"06 / 23","kicker":"ENGINE INTERNALS","name":"Rico Auto Industries","ticker":"RICOAUTO","price":"₹152","pe":"36.2×","seg":"Machined parts",
   "biz":["Aluminium and ferrous machined components","Engine, transmission and braking parts","Casting, machining and assembly in one"],
   "fin":{"qlabel":"Latest reported · Q1 FY26 (Jun-25)","rev":{"to":543},"pat":{"to":17},"note":"Integrated casting-to-assembly, but thin margins."},
   "moat":"An integrated caster-machiner-assembler — convenient for OEMs, but low-margin and competitive.","moatStrength":"NARROW"},
  "Sixth, Rico Auto — the integrator. [pause] It casts, machines and assembles aluminium and iron "
  "parts under one roof. [pause] Revenue was about five hundred forty crore, but profit only "
  "seventeen crore. [pause] It trades near thirty-six times earnings. [pause] "
  "Its moat is convenience — doing the whole job for a carmaker — but the margins tell you it's a competitive space."),

 ("e07_ucal","au_company",
  {"idx":"07 / 23","kicker":"ENGINE INTERNALS","name":"UCAL","ticker":"UCAL","price":"₹118","pe":"N/A","seg":"Fuel systems",
   "biz":["Fuel-management and precision machined parts","Carburettors, throttle bodies and pumps","Supplies OEMs in India and abroad"],
   "fin":{"qlabel":"Latest reported · Q1 FY26 (Jun-25)","rev":{"to":195},"pat":{"to":6,"loss":True,"label":"Net loss"},"note":"Slipped into losses as demand and mix turned against it."},
   "moat":"A fuel-systems supplier under pressure — carburettor-era products and recent losses make its moat weak.","moatStrength":"WEAK"},
  "Seventh, UCAL — under pressure. [pause] It makes fuel-management parts like throttle bodies and "
  "pumps. [pause] But it's been slipping into losses, on revenue of about a hundred ninety-five "
  "crore. [pause] There's no P E right now. [pause] "
  "Its moat is weak — its heritage is fuel systems, and it's struggling to stay profitable through the transition."),

 ("e08_sunclay","au_company",
  {"idx":"08 / 23","kicker":"ENGINE INTERNALS","name":"Sundaram Clayton","ticker":"SUNCLAY","price":"₹1,242","pe":"N/A","seg":"Die-castings",
   "biz":["A TVS-group aluminium die-casting maker","Castings for two-wheelers and commercial vehicles","Plus non-automotive industrial castings"],
   "fin":{"qlabel":"Q1 FY27 · Jun 2026","rev":{"to":592},"pat":{"to":59,"loss":True,"label":"Net loss"},"note":"Loss-making, with a weak return on equity over recent years."},
   "moat":"A TVS-group caster with pedigree — but currently loss-making, so its moat isn't showing in the numbers.","moatStrength":"WEAK"},
  "Eighth, Sundaram Clayton — a struggling name. [pause] Part of the TVS group, it makes aluminium "
  "die-castings. [pause] But it lost about fifty-nine crore last quarter, on revenue of five hundred "
  "ninety-two crore. [pause] There's no meaningful P E. [pause] "
  "Its moat, on paper, is TVS-group pedigree in casting — but the losses say the business is under real strain."),

 # ---- PART 2: BEARINGS ----
 ("g_d2","au_divider",{"part":"PART TWO","title":"The Bearings Club","sub":"Where global brands quietly compound","color":UP,"pips":3,"at":2},
  "Part two — bearings. [pause] The humble parts that let everything spin. It's a club of global "
  "brands with strong margins, that quietly compound through both auto and industrial cycles."),

 ("g09_schaeffler","au_company",
  {"idx":"09 / 23","kicker":"BEARINGS","name":"Schaeffler India","ticker":"SCHAEFFLER","price":"₹4,035","pe":"50.3×","seg":"Bearings",
   "biz":["Bearings, engine, transmission and chassis parts","Brands like INA, LuK and FAG","Serves auto OEMs and a broad industrial base"],
   "fin":{"qlabel":"Q1 FY27 · Jun 2026","rev":{"to":2761},"pat":{"to":326},"note":"Auto plus industrial breadth smooths the cycle."},
   "moat":"A global bearings and precision leader spanning auto and industry — brand, breadth and pricing power.","moatStrength":"WIDE"},
  "Ninth, Schaeffler India — the precision leader. [pause] It makes bearings and engine parts under "
  "brands like L-u-K and F-A-G, for both cars and industry. [pause] Revenue was about twenty-seven "
  "hundred crore, profit three hundred twenty-six crore. [pause] It trades near fifty times "
  "earnings. [pause] "
  "Its moat is wide — a trusted global brand, spread across auto and industrial markets so no single cycle can sink it."),

 ("g10_skf","au_company",
  {"idx":"10 / 23","kicker":"BEARINGS","name":"SKF India","ticker":"SKFINDIA","price":"₹1,534","pe":"26.0×","seg":"Bearings",
   "biz":["The Indian arm of Sweden's SKF","Bearings, seals and lubrication systems","Auto, aftermarket and industrial"],
   "fin":{"qlabel":"Latest reported · Q1 FY26 (Jun-25)","rev":{"to":1283},"pat":{"to":118},"note":"A century-old bearings brand with a strong aftermarket."},
   "moat":"A century-old global bearings brand with a deep aftermarket — a durable, cash-generative franchise.","moatStrength":"WIDE"},
  "Tenth, SKF India — the Swedish name. [pause] It's the Indian arm of SKF, one of the world's oldest "
  "bearing makers, also selling seals and lubrication. [pause] Revenue was about thirteen hundred "
  "crore, profit a hundred eighteen crore. [pause] It trades near twenty-six times earnings. [pause] "
  "Its moat is wide — a trusted, century-old brand with a big, sticky aftermarket business."),

 ("g11_nrb","au_company",
  {"idx":"11 / 23","kicker":"BEARINGS","name":"NRB Bearings","ticker":"NRBBEARING","price":"₹462","pe":"29.9×","seg":"Needle bearings",
   "biz":["A leader in needle roller bearings","For transmissions, engines and steering","Supplies OEMs and exports"],
   "fin":{"qlabel":"Q1 FY27 · Jun 2026","rev":{"to":370},"pat":{"to":38},"note":"India's needle-bearing specialist, with a growing export book."},
   "moat":"India's leader in needle roller bearings — a focused, technical niche with OEM lock-in and exports.","moatStrength":"NARROW"},
  "Eleventh, NRB Bearings — the needle specialist. [pause] It's India's leader in needle roller "
  "bearings, used in gearboxes and engines. [pause] Revenue was about three hundred seventy crore, "
  "profit thirty-eight crore. [pause] It trades near thirty times earnings. [pause] "
  "Its moat is a focused technical niche — once your bearing is designed into a gearbox, you're hard to replace."),

 ("g12_bimetal","au_company",
  {"idx":"12 / 23","kicker":"BEARINGS","name":"Bimetal Bearings","ticker":"BIMETAL","price":"₹665","pe":"22.1×","seg":"Engine bearings",
   "biz":["Engine bearings, bushings and thrust washers","For automotive, locomotive and industrial engines","Part of the Amalgamations group"],
   "fin":{"qlabel":"Latest reported · Q1 FY26 (Jun-25)","rev":{"to":72},"pat":{"to":4},"note":"Small and specialised, within a large industrial group."},
   "moat":"A small engine-bearing specialist backed by the Amalgamations group — a stable niche, but sub-scale.","moatStrength":"NARROW"},
  "Twelfth, Bimetal Bearings — small and specialised. [pause] Part of the Amalgamations group, it "
  "makes engine bearings and bushings. [pause] It's tiny — revenue about seventy crore, profit four "
  "crore. [pause] It trades near twenty-two times earnings. [pause] "
  "Its moat is a stable niche inside a big industrial house — reliable, but too small to move the needle."),

 ("g13_menonbe","au_company",
  {"idx":"13 / 23","kicker":"BEARINGS","name":"Menon Bearings","ticker":"MENONBE","price":"₹237","pe":"30.3×","seg":"Bearings & castings",
   "biz":["Bimetal bearings, bushings and thrust washers","Plus aluminium die-cast components","For automotive, tractor and industrial engines"],
   "fin":{"qlabel":"Q1 FY27 · Jun 2026","rev":{"to":92},"pat":{"to":14},"note":"Small but consistently profitable, with healthy margins."},
   "moat":"A small, well-run bearings-and-castings maker — good margins, but limited scale.","moatStrength":"NARROW"},
  "Thirteenth, Menon Bearings — the other Menon. [pause] From Kolhapur too, it makes bearings and "
  "aluminium castings. [pause] It's small — revenue about ninety crore — but nicely profitable, with "
  "fourteen crore of profit. [pause] It trades near thirty times earnings. [pause] "
  "Its moat is narrow but real — a well-run niche supplier with healthy margins, just short on scale."),

 # ---- PART 3: DRIVETRAIN, STEERING & CONTROLS ----
 ("d_d3","au_divider",{"part":"PART THREE","title":"Drivetrain & Controls","sub":"Gears, motors, steering and the EV leader","color":VAL,"pips":3,"at":3},
  "And part three — drivetrain, steering and electronic controls. [pause] Gears, motors and the "
  "brains of the vehicle — including the one company best positioned for the electric future."),

 ("d14_sona","au_company",
  {"idx":"14 / 23","kicker":"DRIVETRAIN · CONTROLS","name":"Sona BLW (Comstar)","ticker":"SONACOMS","price":"₹818","pe":"70.2×","seg":"EV driveline",
   "biz":["Differential gears, assemblies and starter motors","Increasingly, EV traction motors and systems","A large and rising share from electric vehicles"],
   "fin":{"qlabel":"Q1 FY27 · Jun 2026","rev":{"to":1301},"pat":{"to":179},"note":"A high and growing share of revenue comes from EV programs."},
   "moat":"The best-positioned Indian driveline maker for EVs — a fast-growing electric order book and global customers.","moatStrength":"WIDE"},
  "Fourteenth, Sona Comstar — the EV winner. [pause] It makes differential gears and, increasingly, "
  "the traction motors that drive electric cars. [pause] A big and rising share of its revenue is "
  "already electric. [pause] Revenue was about thirteen hundred crore, profit a hundred seventy-nine "
  "crore. [pause] It trades at a premium seventy times earnings. [pause] "
  "Its moat is the best EV position in this whole series — global electric programs designing Sona in for years."),

 ("d15_divgi","au_company",
  {"idx":"15 / 23","kicker":"DRIVETRAIN · CONTROLS","name":"Divgi TorqTransfer","ticker":"DIVGIITTS","price":"₹1,047","pe":"68.2×","seg":"4WD & EV driveline",
   "biz":["Transfer cases and torque couplers","Four-wheel-drive and driveline systems","Increasingly, EV powertrain components"],
   "fin":{"qlabel":"Latest reported · Q1 FY26 (Jun-25)","rev":{"to":72},"pat":{"to":9},"note":"Small, but with a genuine EV-driveline growth story."},
   "moat":"A niche leader in 4WD driveline tech, extending into EV powertrains — small, but technically differentiated.","moatStrength":"NARROW"},
  "Fifteenth, Divgi TorqTransfer — the four-wheel-drive specialist. [pause] It makes transfer cases "
  "and torque couplers, and is moving into EV powertrains. [pause] It's small — revenue about seventy "
  "crore. [pause] It trades at a rich sixty-eight times earnings. [pause] "
  "Its moat is niche driveline technology — differentiated, with a real EV angle, but still tiny."),

 ("d16_shivam","au_company",
  {"idx":"16 / 23","kicker":"DRIVETRAIN · CONTROLS","name":"Shivam Autotech","ticker":"SHIVAMAUTO","price":"₹17.7","pe":"N/A","seg":"Forged gears",
   "biz":["Near-net-shape forged and machined parts","Gears, shafts and transmission components","A Dayanand Munjal (Hero) group company"],
   "fin":{"pending":True,"qlabel":"Q1 FY27 due 13-Aug (not out)","note":"A small penny-stock, closely tied to the Hero two-wheeler ecosystem."},
   "moat":"A small Hero-linked forger of gears and shafts — customer-concentrated and sub-scale.","moatStrength":"WEAK"},
  "Sixteenth, Shivam Autotech — a penny-stock supplier. [pause] Part of a Munjal-family group, it "
  "forges gears and shafts, mostly for Hero two-wheelers. [pause] Its results are due on the "
  "thirteenth of August. [pause] "
  "Its moat is weak — a small forger tied closely to one customer, with little to set it apart."),

 ("d17_igarashi","au_company",
  {"idx":"17 / 23","kicker":"DRIVETRAIN · CONTROLS","name":"Igarashi Motors","ticker":"IGARASHI","price":"₹465","pe":"N/A","seg":"Micro-motors",
   "biz":["Permanent-magnet DC micro-motors","Used in power seats, mirrors, HVAC and braking","A specialist supplier to global OEMs"],
   "fin":{"qlabel":"Q1 FY27 · Jun 2026","pat":{"to":7,"label":"Net profit"},"note":"A niche micro-motor exporter; profit improved this quarter."},
   "moat":"A specialist micro-motor exporter to global OEMs — a real niche, but small and customer-concentrated.","moatStrength":"NARROW"},
  "Seventeenth, Igarashi Motors — the micro-motor maker. [pause] It makes the tiny motors that move "
  "your power seats and mirrors, exporting to global carmakers. [pause] Its June-quarter profit was "
  "about seven crore, and improving. [pause] "
  "Its moat is a technical export niche — useful and specialised, but small and reliant on a few big customers."),

 ("d18_sedemac","au_company",
  {"idx":"18 / 23","kicker":"DRIVETRAIN · CONTROLS","name":"SEDEMAC Mechatronics","ticker":"SEDEMAC","price":"₹2,810","pe":"High","seg":"ECUs & controls",
   "biz":["Engine-control and motion-control systems","ECUs, starter-generators and embedded tech","For two-wheelers, small engines and off-road"],
   "fin":{"qlabel":"Q1 FY27 · Jun 2026","rev":{"to":310},"pat":{"to":33},"note":"A recently-listed, fast-growing controls-technology company."},
   "moat":"A technology-led maker of engine and motion controls — an emerging, high-growth franchise in embedded systems.","moatStrength":"EMERGING"},
  "Eighteenth, SEDEMAC Mechatronics — the brains supplier. [pause] It builds the electronic control "
  "units and embedded systems that manage engines and motors. [pause] Recently listed, it's growing "
  "fast — revenue about three hundred ten crore, profit thirty-three crore. [pause] "
  "Its moat is emerging technology — control electronics that get more valuable as vehicles get smarter and electric."),

 ("d19_indnippon","au_company",
  {"idx":"19 / 23","kicker":"DRIVETRAIN · CONTROLS","name":"India Nippon Electricals","ticker":"INDNIPPON","price":"₹1,166","pe":"28.9×","seg":"Ignition & ECUs",
   "biz":["Electronic ignition systems and ECUs","Engine-management for two- and three-wheelers","Part of the TVS group"],
   "fin":{"qlabel":"Q1 FY27 · Jun 2026","rev":{"to":299},"pat":{"to":40},"note":"Solid margins from engine-management electronics."},
   "moat":"A focused engine-management electronics maker in the TVS group — good margins, evolving toward EV controls.","moatStrength":"NARROW"},
  "Nineteenth, India Nippon Electricals — the ignition maker. [pause] Part of the TVS group, it makes "
  "the electronic ignition and control units for two- and three-wheelers. [pause] Revenue was about "
  "three hundred crore, profit forty crore. [pause] It trades near twenty-nine times earnings. [pause] "
  "Its moat is focused electronics with good margins — and it's evolving those skills toward electric controls."),

 ("d20_pricol","au_company",
  {"idx":"20 / 23","kicker":"DRIVETRAIN · CONTROLS","name":"Pricol","ticker":"PRICOLLTD","price":"₹738","pe":"33.6×","seg":"Instrument clusters",
   "biz":["Driver-information systems and instrument clusters","Sensors, telematics and pumps","A leading supplier of clusters and controls"],
   "fin":{"qlabel":"Q1 FY27 · Jun 2026","rev":{"to":1105},"pat":{"to":67},"note":"Digital clusters and connectivity are a real growth engine."},
   "moat":"A leader in instrument clusters and driver-information — content-per-vehicle rising as dashboards go digital.","moatStrength":"WIDE"},
  "Twentieth, Pricol — the dashboard company. [pause] It makes the instrument clusters and sensors "
  "behind your steering wheel, and as dashboards go digital, its content per vehicle keeps rising. "
  "[pause] Revenue was about eleven hundred crore, profit sixty-seven crore. [pause] It trades near "
  "thirty-four times earnings. [pause] "
  "Its moat is leadership in a growing category — smarter, connected dashboards that every new vehicle now wants."),

 ("d21_jtekt","au_company",
  {"idx":"21 / 23","kicker":"DRIVETRAIN · CONTROLS","name":"JTEKT India","ticker":"JTEKTINDIA","price":"₹140","pe":"49.4×","seg":"Steering",
   "biz":["Steering systems and columns","Manual, hydraulic and electric power steering","Formerly Sona Koyo; part of Japan's JTEKT"],
   "fin":{"qlabel":"Latest reported","rev":{"to":584},"pat":{"to":30},"note":"A Japanese-parent steering specialist; electric steering is the growth."},
   "moat":"A steering specialist with Japanese-parent technology — electric power steering is a structural tailwind.","moatStrength":"NARROW"},
  "Twenty-first, JTEKT India — the steering maker. [pause] Once Sona Koyo, now part of Japan's JTEKT, "
  "it makes steering systems, increasingly electric ones. [pause] Revenue was about five hundred "
  "eighty crore, profit thirty crore. [pause] It trades near forty-nine times earnings. [pause] "
  "Its moat is steering technology with a global parent — and the shift to electric power steering plays to its strengths."),

 ("d22_zfcv","au_company",
  {"idx":"22 / 23","kicker":"DRIVETRAIN · CONTROLS","name":"ZF Commercial (WABCO)","ticker":"ZFCVINDIA","price":"₹2,637","pe":"59.4×","seg":"CV braking & ADAS",
   "biz":["Air brakes, ABS and vehicle-control electronics","Advanced driver-assistance for commercial vehicles","Formerly WABCO India; part of Germany's ZF"],
   "fin":{"qlabel":"Q1 FY27 · Jun 2026","rev":{"to":1066},"pat":{"to":104},"note":"Safety mandates keep raising the electronics per truck."},
   "moat":"The leader in commercial-vehicle braking and safety electronics — regulation keeps expanding its content per truck.","moatStrength":"WIDE"},
  "Twenty-second, ZF Commercial — formerly WABCO. [pause] Part of Germany's ZF, it's the leader in "
  "truck braking, A-B-S and driver-assistance electronics. [pause] Revenue was about a thousand "
  "crore, profit a hundred four crore. [pause] It trades near fifty-nine times earnings. [pause] "
  "Its moat is wide — as safety rules tighten, every truck needs more of exactly what ZF sells."),

 ("d23_zfsteer","au_company",
  {"idx":"23 / 23","kicker":"DRIVETRAIN · CONTROLS","name":"ZF Steering Gear","ticker":"ZFSTEERING","price":"₹658","pe":"29.6×","seg":"CV steering",
   "biz":["Steering gears and hydraulic pumps","For commercial vehicles, tractors and utility vehicles","In association with ZF group technology"],
   "fin":{"qlabel":"Q1 FY27 · Jun 2026","rev":{"to":143},"pat":{"to":11},"note":"A smaller, separate ZF-linked steering maker."},
   "moat":"A smaller CV-and-tractor steering maker with ZF-linked technology — a solid niche, but modest in scale.","moatStrength":"NARROW"},
  "And twenty-third, ZF Steering Gear — the tractor-steering maker. [pause] A separate ZF-linked "
  "company, it makes steering for trucks and tractors. [pause] Revenue was about a hundred forty-three "
  "crore, profit eleven crore. [pause] It trades near thirty times earnings. [pause] "
  "Its moat is a solid steering niche with global technology — just at a much smaller scale than its cousins."),

 ("v5_recap","au_recap",
  {"title":"Engine, Bearings & Drivetrain — in one breath","color":BIZC,
   "items":[
     "Bosch, Schaeffler, SKF: global brands quietly compounding",
     "Engine-internal makers are cheap — but face the EV question",
     "Sona Comstar is the clear EV-driveline winner (at a premium)",
     "ZF Commercial gains as truck-safety rules tighten",
     "Pricol & SEDEMAC ride smarter, digital vehicles",
     "UCAL and Sundaram Clayton are loss-making, under strain",
     "Bearings are the sector's quiet, durable compounders",
   ],
   "closer":"The engine era is fading — the winners already sell into whatever comes next."},
  "So, in one breath. [pause] The global bearing and components brands — Bosch, Schaeffler, S-K-F — "
  "quietly compound through every cycle. [pause] The pure engine-internal makers look cheap, but they "
  "all face the same electric question. [pause] The clear winner is Sona Comstar, already deep into "
  "EV drivetrains — though you pay up for it. [pause] ZF Commercial gains as truck-safety rules "
  "tighten, and Pricol and SEDEMAC ride the move to smarter, digital vehicles. [pause] A few, like "
  "UCAL and Sundaram Clayton, are simply struggling. [pause] "
  "The lesson: the engine era is fading — and the winners already sell into whatever comes next. [pause] "
  "One part to go — the electricals, lighting and the aftermarket. Thanks for watching."),
]

def post(p,b):
    req=urllib.request.Request(BASE+p,data=json.dumps(b).encode(),headers={"Content-Type":"application/json"},method="POST")
    with urllib.request.urlopen(req,timeout=30) as r: return json.loads(r.read().decode())
def get(p):
    with urllib.request.urlopen(BASE+p,timeout=30) as r: return r.read()
def tts_chunk(path,text):
    gid=post("/generate",{"profile_id":PROFILE,"text":text,"engine":"kokoro"})["id"]
    for _ in range(300):
        raw=get(f"/generate/{gid}/status").decode(); line=[l for l in raw.splitlines() if l.startswith("data:")]
        st=json.loads(line[-1][5:].strip()) if line else None
        if st and st.get("status")=="completed": break
        time.sleep(1)
    open(path,"wb").write(get(f"/audio/{gid}"))
def gen_one(seg_id,text):
    fin=os.path.join(FIN,seg_id+".wav")
    if os.path.exists(fin):
        out=subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","default=noprint_wrappers=1:nokey=1",fin],capture_output=True,text=True,check=True)
        return fin,round(float(out.stdout.strip()),3)
    chunks=[c.strip() for c in text.split("[pause]") if c.strip()]; paths=[]
    for ci,chunk in enumerate(chunks):
        cp=os.path.join(RAW,f"{seg_id}_c{ci}.wav")
        if not os.path.exists(cp): tts_chunk(cp,chunk)
        paths.append(cp)
    psil=os.path.join(RAW,"_pause.wav")
    if not os.path.exists(psil): subprocess.run(["ffmpeg","-y","-f","lavfi","-i","anullsrc=r=24000:cl=mono","-t",str(PAUSE),psil],check=True,capture_output=True)
    clist=os.path.join(RAW,f"{seg_id}_concat.txt")
    with open(clist,"w") as f:
        for i2,p2 in enumerate(paths):
            f.write(f"file '{p2}'\n")
            if i2<len(paths)-1: f.write(f"file '{psil}'\n")
    af=f"atempo={ATEMPO}" if ATEMPO!=1.0 else "anull"
    subprocess.run(["ffmpeg","-y","-f","concat","-safe","0","-i",clist,"-filter:a",af,fin],check=True,capture_output=True)
    out=subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","default=noprint_wrappers=1:nokey=1",fin],capture_output=True,text=True,check=True)
    return fin,round(float(out.stdout.strip()),3)
manifest=[]
for sid,variant,props,text in SEGMENTS:
    path,dur=gen_one(sid,text); manifest.append({"id":sid,"variant":variant,"props":props,"wav":path,"duration":dur})
    print(f"  {sid:14s} {dur:6.2f}s",flush=True)
silence=os.path.join(FIN,"_sil.wav"); subprocess.run(["ffmpeg","-y","-f","lavfi","-i","anullsrc=r=24000:cl=mono","-t",str(GAP),silence],check=True,capture_output=True)
cl=os.path.join(ROOT,"concat5.txt")
with open(cl,"w") as f:
    for i,m in enumerate(manifest):
        f.write(f"file '{m['wav']}'\n")
        if i<len(manifest)-1: f.write(f"file '{silence}'\n")
subprocess.run(["ffmpeg","-y","-f","concat","-safe","0","-i",cl,"-c","copy",os.path.join(PUBLIC,NARR)],check=True,capture_output=True)
cuts,t=[],0.0
for m in manifest:
    s,e=t,t+m["duration"]; cuts.append({"id":m["id"],"type":m["variant"],"in_seconds":round(s,3),"out_seconds":round(e,3),"props":{**m["props"],"dur":round(m["duration"]+GAP,3)}}); t=e+GAP
json.dump({"cuts":cuts,"audio":{"narration":{"src":f"{PREFIX}/{NARR}","volume":1.0}}},open(os.path.join(ROOT,"artifacts",EDJSON),"w"),indent=2)
print(f"total {t-GAP:.2f}s ({(t-GAP)/60:.2f} min), {len(cuts)} scenes")
