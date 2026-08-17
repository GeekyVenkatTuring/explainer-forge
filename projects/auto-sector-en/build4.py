#!/usr/bin/env python3
"""Indian Auto Sector — Video 4: CHASSIS, BRAKING, SUSPENSION & BODY (English, Nova).
Reuses `au` scene set. Own narration (au/narration4.wav) + edit_decisions4.json.
Data: research/chassis-braking-suspension.md (Screener close 07-Aug-2026; Q1 FY27/Jun-26
where available). Education, not advice. Run: python3 build4.py
"""
import json, os, subprocess, time, urllib.request
BASE="http://127.0.0.1:17493"; PROFILE="c488e05c-3407-46a3-874d-1b09b3aff78d"
GAP,PAUSE,ATEMPO=0.5,0.6,0.95; PREFIX="au"; NARR="narration4.wav"; EDJSON="edit_decisions4.json"
ROOT=os.path.dirname(os.path.abspath(__file__)); REPO=os.path.abspath(os.path.join(ROOT,"..",".."))
PUBLIC=os.path.join(REPO,"composer","public",PREFIX); RAW=os.path.join(ROOT,"assets","raw"); FIN=os.path.join(ROOT,"assets")
for d in (PUBLIC,RAW,os.path.join(ROOT,"artifacts")): os.makedirs(d,exist_ok=True)
BIZC,UP,MOAT,VAL="#38BDF8","#34D399","#A78BFA","#FBBF24"

SEGMENTS=[
 ("v4_title","au_title",
  {"kicker":"AUTO & AUTO-COMPONENTS · PART 4 OF 6","title":"Indian Auto Stocks\nChassis, Braking & Body",
   "sub":"24 companies · suspension · brakes · wheels · seats · glass · P/E · moat"},
  "Welcome back. [pause] Part four is about everything that holds a vehicle up, stops it, and "
  "wraps around you — suspension, brakes, wheels, seats and glass. [pause] Some are quiet monopolies "
  "with huge market shares; a few are in real trouble. [pause] Same four things for each: what they "
  "do, the latest quarter, the P E, and the moat. [pause] Figures approximate; verify on your terminal. "
  "Education, not advice."),

 ("a_d1","au_divider",{"part":"PART ONE","title":"Ride & Suspension","sub":"Shock absorbers, springs and wheels","color":BIZC,"pips":3,"at":1},
  "First, ride and suspension. [pause] The parts that soak up the bumps and carry the load — and here, "
  "a couple of companies own staggering market shares."),

 ("a01_endurance","au_company",
  {"idx":"01 / 24","kicker":"RIDE & SUSPENSION","name":"Endurance Technologies","ticker":"ENDURANCE","price":"₹2,904","pe":"43.8×","seg":"2W components",
   "biz":["India's largest two-wheeler component maker","Aluminium castings, suspension, braking and clutches","Operations across India and Europe"],
   "fin":{"qlabel":"Q1 FY27 · Jun 2026","rev":{"to":4086},"pat":{"to":276},"note":"Broad, diversified and steadily scaling across products and geographies."},
   "moat":"India's biggest 2W component supplier — diversified across products and Europe, and hard for OEMs to replace.","moatStrength":"WIDE"},
  "First, Endurance Technologies — the two-wheeler backbone. [pause] It's India's largest maker of "
  "two-wheeler parts — castings, suspension, brakes and clutches — with plants in India and Europe. "
  "[pause] Revenue was about four thousand crore, profit two hundred seventy-six crore. [pause] "
  "It trades near forty-four times earnings. [pause] "
  "Its moat is breadth and scale — so many parts, so deeply embedded, that carmakers can't easily switch."),

 ("a02_gabriel","au_company",
  {"idx":"02 / 24","kicker":"RIDE & SUSPENSION","name":"Gabriel India","ticker":"GABRIEL","price":"₹1,500","pe":"59.8×","seg":"Ride control",
   "biz":["Shock absorbers, struts and front forks","Around 88% share of commercial-vehicle dampers","Serves every vehicle segment, plus railways"],
   "fin":{"qlabel":"Q1 FY27 · Jun 2026","rev":{"to":1426},"pat":{"to":108},"note":"An Anand-group restructuring widened its product base."},
   "moat":"A near-monopoly — roughly 88% of CV dampers — and the ride-control leader across segments.","moatStrength":"WIDE"},
  "Second, Gabriel India — the shock-absorber king. [pause] Part of the Anand group, it makes "
  "ride-control parts, and it holds an astonishing eighty-eight percent share of commercial-vehicle "
  "dampers. [pause] Revenue was about fourteen hundred crore, profit a hundred eight crore. [pause] "
  "It trades near sixty times earnings. [pause] "
  "Its moat is that dominance — when nearly nine of ten trucks use your dampers, you set the terms."),

 ("a03_munjalshowa","au_company",
  {"idx":"03 / 24","kicker":"RIDE & SUSPENSION","name":"Munjal Showa","ticker":"MUNJALSHOW","price":"₹134","pe":"20.3×","seg":"Shock absorbers",
   "biz":["A Hero-group and Showa-of-Japan joint venture","Shock absorbers, struts and front forks","Mainly for two-wheelers"],
   "fin":{"qlabel":"Q1 FY27 · Jun 2026","rev":{"to":348},"pat":{"to":11},"note":"Reliant on a few big customers like Hero and Honda."},
   "moat":"Solid ride-control tech via a Japanese JV — but heavily dependent on a couple of two-wheeler customers.","moatStrength":"NARROW"},
  "Third, Munjal Showa — Gabriel's rival. [pause] A joint venture of the Hero group and Japan's "
  "Showa, it makes shock absorbers, mostly for two-wheelers. [pause] Revenue was about three hundred "
  "fifty crore, profit eleven crore. [pause] It trades near twenty times earnings. [pause] "
  "Its moat is narrow — good technology, but it leans on a handful of big customers like Hero and Honda."),

 ("a04_jamna","au_company",
  {"idx":"04 / 24","kicker":"RIDE & SUSPENSION","name":"Jamna Auto Industries","ticker":"JAMNAAUTO","price":"₹145","pe":"23.9×","seg":"Leaf springs",
   "biz":["India's largest maker of leaf and parabolic springs","Suspension systems for commercial vehicles","Among the world's top spring makers"],
   "fin":{"qlabel":"Q1 FY27 · Jun 2026","rev":{"to":611},"pat":{"to":49},"note":"A dominant domestic share in CV suspension springs."},
   "moat":"A dominant share of India's CV suspension springs — scale, OEM ties and a global top-three position.","moatStrength":"WIDE"},
  "Fourth, Jamna Auto — the spring specialist. [pause] It's India's largest, and one of the world's "
  "largest, makers of the leaf springs that suspend trucks. [pause] Revenue was about six hundred "
  "crore, profit forty-nine crore. [pause] It trades near twenty-four times earnings. [pause] "
  "Its moat is dominance in a focused niche — most Indian trucks ride on Jamna's springs."),

 ("a05_belrise","au_company",
  {"idx":"05 / 24","kicker":"RIDE & SUSPENSION","name":"Belrise Industries","ticker":"BELRISE","price":"₹248","pe":"48.0×","seg":"Chassis & metal parts",
   "biz":["Metal chassis, body and suspension parts","For two-wheelers and four-wheelers","A large, diversified tier-1 supplier"],
   "fin":{"qlabel":"FY26 · full year","rev":{"to":9509},"pat":{"to":497},"note":"Newly listed in 2025; quarterly revenue runs around ₹2,400 cr."},
   "moat":"A big, diversified metal-parts tier-1 with scale — but relatively low margins and a fresh listing to prove out.","moatStrength":"NARROW"},
  "Fifth, Belrise Industries — the new giant. [pause] A Pune-based maker of metal chassis and body "
  "parts, it listed only in twenty twenty-five. [pause] Over the full year it did about ninety-five "
  "hundred crore of revenue and five hundred crore of profit. [pause] It trades near forty-eight "
  "times earnings. [pause] "
  "Its moat is scale and diversification — but margins are thin, and as a new listing it still has to prove itself."),

 ("a06_ssw","au_company",
  {"idx":"06 / 24","kicker":"RIDE & SUSPENSION","name":"Steel Strips Wheels","ticker":"SSWL","price":"₹308","pe":"22.8×","seg":"Wheel rims",
   "biz":["India's largest maker of steel and alloy wheel rims","Supplies every vehicle segment","Exports wheels and is growing alloy & EV rims"],
   "fin":{"qlabel":"Q1 FY27 · Jun 2026","rev":{"to":1510},"pat":{"to":69},"note":"Record monthly turnover in July; alloy and EV wheels are the growth."},
   "moat":"India's largest wheel-rim maker across every segment — scale plus a growing alloy/EV wheel mix.","moatStrength":"WIDE"},
  "Sixth, Steel Strips Wheels — the wheel maker. [pause] It's India's largest maker of steel and "
  "alloy wheel rims, for everything from bikes to trucks. [pause] Revenue was about fifteen hundred "
  "crore, profit sixty-nine crore. [pause] It trades near twenty-three times earnings. [pause] "
  "Its moat is scale across every segment — and a shift toward pricier alloy and EV wheels."),

 ("a07_wheels","au_company",
  {"idx":"07 / 24","kicker":"RIDE & SUSPENSION","name":"Wheels India","ticker":"WHEELS","price":"₹1,387","pe":"20.7×","seg":"Wheels & suspension",
   "biz":["TVS-group maker of steel wheels","For cars, trucks, tractors and construction","Plus air-suspension and hydraulic parts"],
   "fin":{"qlabel":"Q1 FY27 · Jun 2026","rev":{"to":1491},"pat":{"to":39},"note":"Large revenue, but thin margins typical of wheels."},
   "moat":"A TVS-group wheel leader broadening into air-suspension — but wheels are low-margin and CV-cyclical.","moatStrength":"NARROW"},
  "Seventh, Wheels India — the other wheel maker. [pause] Part of the TVS group, it makes steel "
  "wheels for cars and trucks, and is moving into air suspension. [pause] Revenue was about fifteen "
  "hundred crore, but profit only thirty-nine crore — wheels are a thin-margin business. [pause] "
  "It trades near twenty-one times earnings. [pause] "
  "Its moat is narrow — scale and a good group, but a commoditised product tied to the truck cycle."),

 ("a08_uniparts","au_company",
  {"idx":"08 / 24","kicker":"RIDE & SUSPENSION","name":"Uniparts India","ticker":"UNIPARTS","price":"₹815","pe":"20.1×","seg":"Off-highway parts",
   "biz":["Three-point-linkage parts and hydraulic cylinders","For off-highway farm and construction equipment","Largely for export"],
   "fin":{"qlabel":"Q1 FY27 · Jun 2026","rev":{"to":347},"pat":{"to":57},"note":"High margins from a specialised global export niche."},
   "moat":"A global leader in three-point-linkage off-highway parts — a high-margin export niche with sticky customers.","moatStrength":"NARROW"},
  "Eighth, Uniparts India — the export niche. [pause] It makes three-point-linkage parts — the arms "
  "that attach tools to a tractor — and hydraulic cylinders, mostly for export. [pause] On revenue "
  "of three hundred forty-seven crore it made fifty-seven crore in profit — fat margins. [pause] "
  "It trades near twenty times earnings. [pause] "
  "Its moat is being a global leader in a small, specialised export niche few rivals bother with."),

 # ---- PART 2: BRAKES, EMISSIONS & THERMAL ----
 ("b_d2","au_divider",{"part":"PART TWO","title":"Brakes, Emissions & Heat","sub":"Stopping, cleaning and cooling","color":UP,"pips":3,"at":2},
  "Part two — braking, emissions and thermal parts. [pause] The systems that stop the vehicle, clean "
  "its exhaust, and keep it cool. Here the EV shift is both a threat and an opportunity."),

 ("b09_ask","au_company",
  {"idx":"09 / 24","kicker":"BRAKES · EMISSIONS","name":"ASK Automotive","ticker":"ASKAUTOLTD","price":"₹635","pe":"39.6×","seg":"2W braking",
   "biz":["India's largest maker of 2-wheeler braking systems","Around 50% market share","Also aluminium lightweighting and EV drivetrain parts"],
   "fin":{"qlabel":"Q1 FY27 · Jun 2026","rev":{"to":1358},"pat":{"to":85},"note":"EV drivetrain parts open a new growth lane."},
   "moat":"Roughly half of India's 2-wheeler brakes — a dominant share, with EV-drivetrain optionality on top.","moatStrength":"WIDE"},
  "Ninth, ASK Automotive — the brake leader. [pause] It makes about half of all the braking systems "
  "on India's two-wheelers, and it's moving into EV drivetrain parts. [pause] Revenue was about "
  "thirteen hundred fifty crore, profit eighty-five crore. [pause] It trades near forty times "
  "earnings. [pause] "
  "Its moat is that fifty-percent share — plus an EV angle that turns the electric threat into an opportunity."),

 ("b10_sharda","au_company",
  {"idx":"10 / 24","kicker":"BRAKES · EMISSIONS","name":"Sharda Motor Industries","ticker":"SHARDAMOTR","price":"₹941","pe":"16.3×","seg":"Exhaust & emissions",
   "biz":["Exhaust systems and emission-control products","Catalytic converters and after-treatment","Plus suspension and roof systems"],
   "fin":{"qlabel":"Latest reported · Q1 FY26 (Jun-25)","rev":{"to":756},"pat":{"to":100},"note":"Cheap and cash-rich — but EVs don't need exhausts."},
   "moat":"A strong, cheap emission-control specialist — but its core product fades if EVs win big.","moatStrength":"NARROW"},
  "Tenth, Sharda Motor — cheap, with a question mark. [pause] It makes exhaust and emission-control "
  "systems, which every combustion engine needs. [pause] It's cash-rich and cheap, near sixteen times "
  "earnings, on revenue of about seven hundred fifty crore. [pause] "
  "But here's the catch. [pause] Its moat is real today — yet electric vehicles don't have exhausts, "
  "so the long-term question is what replaces that business."),

 ("b11_tenneco","au_company",
  {"idx":"11 / 24","kicker":"BRAKES · EMISSIONS","name":"Tenneco Clean Air India","ticker":"TENNIND","price":"₹563","pe":"36.6×","seg":"Clean-air systems",
   "biz":["Part of the global Tenneco group","Exhaust, catalytic converters, after-treatment","Emission-control for auto OEMs"],
   "fin":{"qlabel":"Q1 FY27 · Jun 2026","rev":{"to":1545},"pat":{"to":165},"note":"Global technology, but the same EV-transition question."},
   "moat":"A global-tech emission-control specialist with strong OEM ties — facing the same long-term EV headwind.","moatStrength":"NARROW"},
  "Eleventh, Tenneco Clean Air — the global cousin. [pause] Part of the worldwide Tenneco group, it "
  "makes emission-control systems for carmakers. [pause] Revenue was about fifteen hundred crore, "
  "profit a hundred sixty-five crore. [pause] It trades near thirty-seven times earnings. [pause] "
  "Its moat is global technology and OEM relationships — but it too must answer the electric question."),

 ("b12_sundrmbrak","au_company",
  {"idx":"12 / 24","kicker":"BRAKES · EMISSIONS","name":"Sundaram Brake Linings","ticker":"SUNDRMBRAK","price":"₹787","pe":"86.2×","seg":"Friction",
   "biz":["TVS-group maker of brake linings and pads","Clutch facings and friction materials","For CVs, cars and railways"],
   "fin":{"qlabel":"Q1 FY27 · Jun 2026","rev":{"to":91},"note":"Barely profitable — under ₹1 crore of profit, on a very high P/E."},
   "moat":"A niche friction-materials maker in the TVS group — but tiny profits make the high valuation hard to justify.","moatStrength":"WEAK"},
  "Twelfth, Sundaram Brake Linings — small and pricey. [pause] Part of the TVS group, it makes brake "
  "linings and friction materials. [pause] But it's small — revenue about ninety crore — and it "
  "barely turned a profit, under one crore. [pause] Yet it trades at eighty-six times earnings. [pause] "
  "Its moat is weak — a real niche, but the numbers don't support that lofty price."),

 ("b13_hindcomp","au_company",
  {"idx":"13 / 24","kicker":"BRAKES · EMISSIONS","name":"Hindustan Composites","ticker":"HINDCOMPOS","price":"₹424","pe":"35.8×","seg":"Friction (exiting)",
   "biz":["Historically a friction-materials maker","Just sold its friction business to Rane (Madras)","Now largely an investment company"],
   "fin":{"qlabel":"Q1 FY27 · Jun 2026","rev":{"to":20},"pat":{"to":9},"note":"Friction business sold to Rane for ₹370 cr; profit now comes mostly from investments."},
   "moat":"Its operating moat is gone — it has sold its friction business and is becoming an investment holding company.","moatStrength":"WEAK"},
  "Thirteenth, Hindustan Composites — a business in transition. [pause] It used to make brake linings, "
  "but it just sold that friction business to Rane Madras for three hundred seventy crore. [pause] "
  "So its sales have collapsed to twenty crore, and its profit now comes mostly from investments. [pause] "
  "It trades near thirty-six times earnings. [pause] "
  "Its operating moat is essentially gone — this is turning into an investment holding company."),

 ("b14_setco","au_company",
  {"idx":"14 / 24","kicker":"BRAKES · EMISSIONS","name":"Setco Automotive","ticker":"SETCO","price":"₹17.8","pe":"N/A","seg":"CV clutches",
   "biz":["A leading maker of clutches for heavy trucks","Sold under the Lipe brand","Supplies OEMs and the aftermarket"],
   "fin":{"qlabel":"Latest reported · Q3 FY26 (Dec-25)","rev":{"to":197},"pat":{"to":57,"loss":True,"label":"Net loss"},"note":"Deeply loss-making — trailing losses of about ₹163 crore."},
   "moat":"A leading truck-clutch brand on paper — but deep, persistent losses make it a distressed situation.","moatStrength":"WEAK"},
  "Fourteenth, Setco Automotive — a cautionary case. [pause] It's a leading maker of truck clutches "
  "under the Lipe brand. [pause] But it's deeply loss-making — a recent quarter lost fifty-seven "
  "crore, and trailing losses are around a hundred sixty-three crore. [pause] There's no P E. [pause] "
  "Its moat, whatever the brand once meant, can't offset a balance sheet under this much strain. A distressed situation."),

 ("b15_banco","au_company",
  {"idx":"15 / 24","kicker":"BRAKES · EMISSIONS","name":"Banco Products","ticker":"BANCOINDIA","price":"₹687","pe":"20.4×","seg":"Cooling systems",
   "biz":["Engine-cooling systems — radiators and oil coolers","Sealing gaskets for auto and industrial use","Europe via its NRF subsidiary"],
   "fin":{"qlabel":"Q1 FY27 · Jun 2026","rev":{"to":1184},"pat":{"to":122},"note":"Healthy margins and a solid European business."},
   "moat":"A cooling-systems specialist with a European arm (NRF) and healthy margins — a durable, unglamorous niche.","moatStrength":"NARROW"},
  "Fifteenth, Banco Products — the cooling specialist. [pause] It makes radiators and cooling systems "
  "for engines, in India and, through its NRF arm, across Europe. [pause] Revenue was about twelve "
  "hundred crore, profit a healthy hundred twenty-two crore. [pause] It trades near twenty times "
  "earnings. [pause] "
  "Its moat is a solid, profitable niche — cooling is needed in combustion and electric vehicles alike."),

 ("b16_talbros","au_company",
  {"idx":"16 / 24","kicker":"BRAKES · EMISSIONS","name":"Talbros Automotive","ticker":"TALBROAUTO","price":"₹439","pe":"26.0×","seg":"Gaskets & chassis",
   "biz":["Gaskets, heat shields and chassis systems","Forgings and anti-vibration rubber parts","Through its own plants and several JVs"],
   "fin":{"qlabel":"Q1 FY27 · Jun 2026","rev":{"to":207},"pat":{"to":22},"note":"A diversified small tier-1 spread across sealing and chassis."},
   "moat":"A diversified small tier-1 across gaskets, chassis and rubber — steady, but no single dominant product.","moatStrength":"NARROW"},
  "Sixteenth, Talbros Automotive — the diversifier. [pause] It makes gaskets, heat shields and "
  "chassis parts, often through joint ventures. [pause] Revenue was about two hundred crore, profit "
  "twenty-two crore. [pause] It trades near twenty-six times earnings. [pause] "
  "Its moat is spread thin — a capable, diversified supplier, but without one product it dominates."),

 # ---- PART 3: BODY, SEATING & GLASS ----
 ("c_d3","au_divider",{"part":"PART THREE","title":"Body, Seats & Glass","sub":"The parts you see and touch","color":VAL,"pips":3,"at":3},
  "And part three — body, seats and glass. [pause] The parts you actually see and touch. From "
  "sheet-metal to seats to the world's largest helmet maker."),

 ("c17_bharatseats","au_company",
  {"idx":"17 / 24","kicker":"BODY · SEATS · GLASS","name":"Bharat Seats","ticker":"BHARATSE","price":"₹241","pe":"32.0×","seg":"Seating",
   "biz":["Complete seating systems and interiors","A Suzuki–Maruti joint venture","Works closely with the Maruti supply chain"],
   "fin":{"qlabel":"Q1 FY27 · Jun 2026","rev":{"to":578},"pat":{"to":13},"note":"Captive to Maruti — steady volumes, but thin margins."},
   "moat":"A captive Maruti-Suzuki seating supplier — reliable volumes, but low margins and one dominant customer.","moatStrength":"NARROW"},
  "Seventeenth, Bharat Seats — the Maruti seat maker. [pause] A Suzuki-Maruti joint venture, it makes "
  "seats and interiors, closely tied to Maruti. [pause] Revenue was about five hundred seventy-eight "
  "crore, but profit only thirteen crore. [pause] It trades near thirty-two times earnings. [pause] "
  "Its moat is that captive Maruti link — steady, but with thin margins and heavy dependence on one customer."),

 ("c18_ndr","au_company",
  {"idx":"18 / 24","kicker":"BODY · SEATS · GLASS","name":"NDR Auto Components","ticker":"NDRAUTO","price":"₹829","pe":"31.5×","seg":"Seating",
   "biz":["Seating systems, frames and interior trim","Carved out of the Bharat Seats/NDR group","A tier-1 interior and seating supplier"],
   "fin":{"qlabel":"Latest reported · Q1 FY26 (Jun-25)","rev":{"to":185},"pat":{"to":14},"note":"A small, focused seating and interiors maker."},
   "moat":"A small seating specialist spun out of the NDR group — focused, but sub-scale next to global seat majors.","moatStrength":"NARROW"},
  "Eighteenth, NDR Auto Components — Bharat Seats' sibling. [pause] Carved out of the same group, it "
  "makes seating and interior trim. [pause] It's small — revenue about a hundred eighty-five crore, "
  "profit fourteen crore. [pause] It trades near thirty-two times earnings. [pause] "
  "Its moat is a focused seating niche — but it's tiny beside the global seat giants."),

 ("c19_jbm","au_company",
  {"idx":"19 / 24","kicker":"BODY · SEATS · GLASS","name":"Jay Bharat Maruti","ticker":"JAYBARMARU","price":"₹139","pe":"10.9×","seg":"Sheet metal",
   "biz":["Sheet-metal parts, welded assemblies and exhausts","A joint venture with Maruti Suzuki","A dedicated tier-1 to the Maruti ecosystem"],
   "fin":{"qlabel":"Q1 FY27 · Jun 2026","rev":{"to":627},"pat":{"to":22},"note":"Cheap at 11× — but its fortunes track Maruti's volumes."},
   "moat":"A captive Maruti sheet-metal supplier — cheap and steady, but entirely tied to one customer's volumes.","moatStrength":"NARROW"},
  "Nineteenth, Jay Bharat Maruti — captive and cheap. [pause] A Maruti joint venture, it stamps "
  "sheet-metal parts almost entirely for Maruti cars. [pause] Revenue was about six hundred "
  "twenty-seven crore, profit twenty-two crore. [pause] It's cheap, near eleven times earnings. [pause] "
  "Its moat is the guaranteed Maruti work — but that's also the risk: as Maruti goes, so goes Jay Bharat."),

 ("c20_asal","au_company",
  {"idx":"20 / 24","kicker":"BODY · SEATS · GLASS","name":"Automotive Stampings","ticker":"ASAL","price":"₹506","pe":"N/A","seg":"Stampings",
   "biz":["Sheet-metal stampings and welded assemblies","Body-in-white and structural pressed parts","A tier-1 supplier to vehicle OEMs"],
   "fin":{"pending":True,"qlabel":"Q1 FY27 · figures thin","note":"A small stamping supplier in the JBM / Tata AutoComp orbit; results are modest."},
   "moat":"A small structural-stampings supplier — commoditised pressed parts with little pricing power.","moatStrength":"WEAK"},
  "Twentieth, Automotive Stampings — a small presser. [pause] It stamps and welds body panels and "
  "structural parts for carmakers. [pause] It's a modest tier-1, historically tied to the JBM and "
  "Tata AutoComp ecosystems. [pause] "
  "Its moat is weak — pressed sheet-metal is a commoditised business where the carmaker holds the power."),

 ("c21_munjalauto","au_company",
  {"idx":"21 / 24","kicker":"BODY · SEATS · GLASS","name":"Munjal Auto Industries","ticker":"MUNJALAU","price":"₹102","pe":"29.0×","seg":"Exhausts & rims",
   "biz":["Exhaust systems, wheel rims and fuel tanks","Sheet-metal parts, mainly for two-wheelers","A Hero-group tier-1 supplier"],
   "fin":{"qlabel":"Latest reported · Q4 FY26 (Mar-26)","rev":{"to":614},"note":"Slipped to a small loss last quarter; heavily reliant on Hero."},
   "moat":"A Hero-linked two-wheeler parts maker — but customer-concentrated and recently unprofitable.","moatStrength":"WEAK"},
  "Twenty-first, Munjal Auto — Hero's parts arm. [pause] It makes exhausts, rims and fuel tanks, "
  "mostly for Hero two-wheelers. [pause] Revenue was about six hundred crore, but it slipped into a "
  "small loss last quarter. [pause] It trades near twenty-nine times earnings. [pause] "
  "Its moat is weak — closely tied to Hero, with thin, sometimes negative, margins."),

 ("c22_asahi","au_company",
  {"idx":"22 / 24","kicker":"BODY · SEATS · GLASS","name":"Asahi India Glass","ticker":"ASAHIINDIA","price":"₹899","pe":"51.3×","seg":"Auto glass",
   "biz":["India's largest automotive glass maker","Windshields and windows for most carmakers","Also architectural glass for buildings"],
   "fin":{"qlabel":"Q1 FY27 · Jun 2026","rev":{"to":1413},"pat":{"to":149},"note":"A near-monopoly in OEM auto glass, part-owned by Asahi and Maruti."},
   "moat":"A near-monopoly in Indian auto glass — high entry barriers, OEM lock-in, plus an architectural-glass arm.","moatStrength":"WIDE"},
  "Twenty-second, Asahi India Glass — the glassmaker. [pause] It makes most of the windshields and "
  "windows in Indian cars, and also architectural glass. [pause] Revenue was about fourteen hundred "
  "crore, profit a hundred forty-nine crore. [pause] It trades near fifty-one times earnings. [pause] "
  "Its moat is wide — auto glass is capital-intensive and OEM-approved, so a near-monopoly is hard to challenge."),

 ("c23_studds","au_company",
  {"idx":"23 / 24","kicker":"BODY · SEATS · GLASS","name":"Studds Accessories","ticker":"STUDDS","price":"₹439","pe":"23.1×","seg":"Helmets",
   "biz":["The world's largest maker of two-wheeler helmets","Sold under the Studds and SMK brands","Market leader in India, with exports"],
   "fin":{"qlabel":"Q1 FY27 · Jun 2026","rev":{"to":170},"pat":{"to":12},"note":"Revenue up ~14%, but profit dipped this quarter."},
   "moat":"The world's largest helmet maker — a trusted safety brand, scale, and tightening helmet rules as a tailwind.","moatStrength":"WIDE"},
  "Twenty-third, Studds Accessories — a global number one. [pause] It's the world's largest maker of "
  "two-wheeler helmets, under the Studds and S-M-K brands. [pause] Revenue rose about fourteen "
  "percent to a hundred seventy crore, though profit dipped. [pause] It trades near twenty-three "
  "times earnings. [pause] "
  "Its moat is wide — a trusted safety brand at global scale, helped by ever-tighter helmet laws."),

 ("c24_sjs","au_company",
  {"idx":"24 / 24","kicker":"BODY · SEATS · GLASS","name":"SJS Enterprises","ticker":"SJS","price":"₹2,446","pe":"41.1×","seg":"Aesthetics",
   "biz":["Decorative and functional aesthetic parts","Logos, dials, overlays, chrome and in-mould parts","For two-wheelers, cars and appliances"],
   "fin":{"qlabel":"Q1 FY27 · Jun 2026","rev":{"to":261},"pat":{"to":74},"note":"Remarkable margins for a parts maker — design commands a premium."},
   "moat":"A design-led aesthetics specialist with premium margins — content-per-vehicle keeps rising as cars get fancier.","moatStrength":"NARROW"},
  "And twenty-fourth, SJS Enterprises — the design house. [pause] It makes the logos, dials and "
  "decorative trim that make a vehicle look premium. [pause] Look at the margins — seventy-four crore "
  "of profit on just two hundred sixty crore of revenue. [pause] It trades near forty-one times "
  "earnings. [pause] "
  "Its moat is design and aesthetics — and as vehicles get fancier, the value of that decorative content keeps rising."),

 ("v4_recap","au_recap",
  {"title":"Chassis, Braking & Body — in one breath","color":BIZC,
   "items":[
     "Gabriel (~88% CV dampers) and Jamna own their niches",
     "ASK Automotive: ~50% of India's 2-wheeler brakes",
     "Asahi Glass & Studds: near-monopoly and world #1 helmets",
     "Exhaust makers (Sharda, Tenneco) face the EV question",
     "Setco is distressed; Hindustan Composites exited friction",
     "Captive Maruti suppliers are cheap but customer-tied",
     "Aesthetics (SJS) and cooling (Banco) are quiet high-margin niches",
   ],
   "closer":"Dominant share is the real moat here — and the EV shift is quietly re-drawing the map."},
  "So, in one breath. [pause] The winners here own their niches — Gabriel with nearly ninety percent "
  "of truck dampers, Jamna in springs, ASK in two-wheeler brakes, Asahi in glass, and Studds, the "
  "world's number-one helmet maker. [pause] The exhaust makers, Sharda and Tenneco, are cheap but "
  "face the electric question. [pause] Setco is distressed, and Hindustan Composites has walked away "
  "from friction entirely. [pause] The captive Maruti suppliers are cheap, but tied to one customer. [pause] "
  "The lesson: dominant market share is the real moat here — and the EV shift is quietly re-drawing the map. [pause] "
  "Next time, the electricals, electronics and steering makers. Thanks for watching."),
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
cl=os.path.join(ROOT,"concat4.txt")
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
