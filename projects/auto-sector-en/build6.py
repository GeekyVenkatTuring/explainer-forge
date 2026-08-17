#!/usr/bin/env python3
"""Indian Auto Sector — Video 6: ELECTRICALS, LIGHTING, WIRING & AFTERMARKET (English, Nova).
Reuses `au` scene set. Own narration (au/narration6.wav) + edit_decisions6.json.
Data: research/engine-bearings-electricals.md (Screener close 07-Aug-2026). Final part.
Education, not advice. Run: python3 build6.py
"""
import json, os, subprocess, time, urllib.request
BASE="http://127.0.0.1:17493"; PROFILE="c488e05c-3407-46a3-874d-1b09b3aff78d"
GAP,PAUSE,ATEMPO=0.5,0.6,0.95; PREFIX="au"; NARR="narration6.wav"; EDJSON="edit_decisions6.json"
ROOT=os.path.dirname(os.path.abspath(__file__)); REPO=os.path.abspath(os.path.join(ROOT,"..",".."))
PUBLIC=os.path.join(REPO,"composer","public",PREFIX); RAW=os.path.join(ROOT,"assets","raw"); FIN=os.path.join(ROOT,"assets")
for d in (PUBLIC,RAW,os.path.join(ROOT,"artifacts")): os.makedirs(d,exist_ok=True)
BIZC,UP,MOAT,VAL="#38BDF8","#34D399","#A78BFA","#FBBF24"

SEGMENTS=[
 ("v6_title","au_title",
  {"kicker":"AUTO & AUTO-COMPONENTS · PART 6 OF 6","title":"Indian Auto Stocks\nElectricals & the Aftermarket",
   "sub":"23 companies · wiring · lighting · cables · dealers · P/E · moat"},
  "Welcome to the final part. [pause] Part six covers the nervous system and the wardrobe of the "
  "vehicle — the wiring, lighting, switches and cables — and then the dealers and distributors who "
  "sell it all. [pause] This group includes some of the sector's true global champions. [pause] Same "
  "four things for each, one last time. Figures approximate; verify on your terminal. Education, not advice."),

 ("l_d1","au_divider",{"part":"PART ONE","title":"Wiring, Lighting & Electronics","sub":"The vehicle's nervous system","color":BIZC,"pips":3,"at":1},
  "First, wiring, lighting and electronics. [pause] The vehicle's nervous system — and, happily for "
  "these companies, the one part of the car that only grows as vehicles get electric and connected."),

 ("l01_motherson","au_company",
  {"idx":"01 / 23","kicker":"WIRING · LIGHTING","name":"Samvardhana Motherson","ticker":"MOTHERSON","price":"₹168","pe":"38.9×","seg":"Global mega-supplier",
   "biz":["One of the world's largest, most diversified parts groups","Wiring, mirrors, modules and lighting","Operates across dozens of countries"],
   "fin":{"qlabel":"Q1 FY27 · Jun 2026","rev":{"to":35244},"pat":{"to":1076},"note":"A truly global business, expanding beyond autos too."},
   "moat":"A global, diversified mega-supplier with scale and deep OEM integration — one of the sector's widest moats.","moatStrength":"WIDE"},
  "First, Samvardhana Motherson — the global champion. [pause] It's one of the world's largest and "
  "most diversified auto-parts groups, making wiring, mirrors and modules across dozens of countries. "
  "[pause] Revenue was a huge thirty-five thousand crore, profit over a thousand crore. [pause] It "
  "trades near thirty-nine times earnings. [pause] "
  "Its moat is global scale and deep integration into carmakers worldwide — a genuinely wide moat."),

 ("l02_msumi","au_company",
  {"idx":"02 / 23","kicker":"WIRING · LIGHTING","name":"Motherson Sumi Wiring","ticker":"MSUMI","price":"₹41.2","pe":"43.5×","seg":"Wiring harnesses",
   "biz":["India's wiring-harness leader — over 40% share","A Sumitomo and Motherson joint venture","Focused purely on the domestic harness market"],
   "fin":{"qlabel":"Q1 FY27 · Jun 2026","rev":{"to":3407},"pat":{"to":145},"note":"EVs need far more wiring — a direct tailwind."},
   "moat":"India's dominant wiring-harness maker at 40%-plus share — and EVs use much more wiring, not less.","moatStrength":"WIDE"},
  "Second, Motherson Sumi Wiring — the harness king. [pause] Carved out as a pure play, it makes over "
  "forty percent of India's wiring harnesses. [pause] Revenue was about thirty-four hundred crore, "
  "profit a hundred forty-five crore. [pause] It trades near forty-four times earnings. [pause] "
  "Its moat is dominance in a growing market — and here's the twist: electric vehicles need far more "
  "wiring, so the shift helps it."),

 ("l03_unominda","au_company",
  {"idx":"03 / 23","kicker":"WIRING · LIGHTING","name":"UNO Minda","ticker":"UNOMINDA","price":"₹1,285","pe":"60.7×","seg":"Diversified electricals",
   "biz":["Switches, lighting, horns, acoustics and alloy wheels","Sensors and EV components","A diversified tier-1 for every vehicle type"],
   "fin":{"qlabel":"Q1 FY27 · Jun 2026","rev":{"to":5557},"pat":{"to":316},"note":"Rising content per vehicle and a strong EV portfolio."},
   "moat":"A broad, fast-growing electricals platform with rising content per vehicle and real EV products — a wide moat.","moatStrength":"WIDE"},
  "Third, UNO Minda — the compounder. [pause] Formerly Minda Industries, it makes switches, lighting, "
  "horns, alloy wheels and EV parts — a bit of everything electrical. [pause] Revenue was about "
  "fifty-five hundred crore, profit three hundred sixteen crore. [pause] It trades at a rich sixty "
  "times earnings. [pause] "
  "Its moat is breadth and growth — its content in every car keeps rising, and it's well-placed for EVs."),

 ("l04_mindacorp","au_company",
  {"idx":"04 / 23","kicker":"WIRING · LIGHTING","name":"Minda Corporation","ticker":"MINDACORP","price":"₹722","pe":"48.5×","seg":"Security & electricals",
   "biz":["Spark Minda group — security and access systems","Wiring harnesses, clusters and die-casting","For two-wheelers, cars and commercial vehicles"],
   "fin":{"qlabel":"Q1 FY27 · Jun 2026","rev":{"to":1704},"pat":{"to":124},"note":"A distinct Minda group from UNO Minda — don't confuse the two."},
   "moat":"A diversified tier-1 in locks, wiring and clusters — solid, but a step behind UNO Minda in scale and multiple.","moatStrength":"NARROW"},
  "Fourth, Minda Corporation — the other Minda. [pause] Part of the separate Spark Minda group, it "
  "makes locks, wiring and instrument clusters. [pause] Revenue was about seventeen hundred crore, "
  "profit a hundred twenty-four crore. [pause] It trades near forty-eight times earnings. [pause] "
  "Its moat is a solid, diversified base — capable, but it trails its bigger cousin UNO Minda."),

 ("l05_lumaxind","au_company",
  {"idx":"05 / 23","kicker":"WIRING · LIGHTING","name":"Lumax Industries","ticker":"LUMAXIND","price":"₹5,792","pe":"26.9×","seg":"Auto lighting",
   "biz":["A leading maker of automotive lighting","Head lamps, tail lamps and LED lighting","In collaboration with Stanley Electric of Japan"],
   "fin":{"qlabel":"Q1 FY27 · Jun 2026","rev":{"to":1223},"pat":{"to":51,"yoy":"+41%","up":True},"note":"LED lighting is lifting both revenue and margins."},
   "moat":"A lighting leader with Japanese technology (Stanley) — LED and premium lighting keep raising its content.","moatStrength":"WIDE"},
  "Fifth, Lumax Industries — the lighting leader. [pause] With Japanese partner Stanley, it makes "
  "headlamps and LED lighting for cars. [pause] Profit jumped forty-one percent, on revenue of about "
  "twelve hundred crore. [pause] It trades near twenty-seven times earnings. [pause] "
  "Its moat is technology and scale in lighting — and as cars adopt fancier LED lights, its value per car climbs."),

 ("l06_lumaxtech","au_company",
  {"idx":"06 / 23","kicker":"WIRING · LIGHTING","name":"Lumax Auto Technologies","ticker":"LUMAXTECH","price":"₹1,722","pe":"41.4×","seg":"Diversified parts",
   "biz":["Gear-shifters, structural parts and modules","Chassis, seat frames and aftermarket products","Serves two- and four-wheeler OEMs"],
   "fin":{"qlabel":"Latest reported · Q4 FY26 (Mar-26)","rev":{"to":1417},"pat":{"to":98},"note":"The broader parts arm of the Lumax group."},
   "moat":"The diversified parts arm of the Lumax group — a good spread of products, but no single dominant one.","moatStrength":"NARROW"},
  "Sixth, Lumax Auto Technologies — the sister company. [pause] It makes gear-shifters, structural "
  "parts and modules — the broader Lumax parts business. [pause] Revenue was about fourteen hundred "
  "crore, profit ninety-eight crore. [pause] It trades near forty-one times earnings. [pause] "
  "Its moat is diversification within a respected group — steady, but without one product it truly dominates."),

 ("l07_varroc","au_company",
  {"idx":"07 / 23","kicker":"WIRING · LIGHTING","name":"Varroc Engineering","ticker":"VARROC","price":"₹811","pe":"43.4×","seg":"2W electricals",
   "biz":["Automotive lighting, electricals and electronics","Metallic and polymer components","Mainly for two- and three-wheelers"],
   "fin":{"qlabel":"Q1 FY27 · Jun 2026","rev":{"to":2634},"pat":{"to":78},"note":"Revenue up ~30% after a turnaround and de-leveraging."},
   "moat":"A recovering 2W lighting-and-electricals maker — improving, but margins still trail the sector leaders.","moatStrength":"NARROW"},
  "Seventh, Varroc Engineering — the comeback story. [pause] It makes lighting and electricals, "
  "mainly for two-wheelers, and has been cleaning up its balance sheet. [pause] Revenue rose about "
  "thirty percent to twenty-six hundred crore, though profit is still modest at seventy-eight crore. "
  "[pause] It trades near forty-three times earnings. [pause] "
  "Its moat is narrow but improving — a real turnaround, though it's not yet as profitable as the leaders."),

 ("l08_fiem","au_company",
  {"idx":"08 / 23","kicker":"WIRING · LIGHTING","name":"Fiem Industries","ticker":"FIEMIND","price":"₹2,580","pe":"26.7×","seg":"2W LED lighting",
   "biz":["Automotive lighting and signalling","LED lamps and mirrors for two-wheelers","Also LED luminaires for general lighting"],
   "fin":{"qlabel":"Latest reported · Q4 FY26 (Mar-26)","rev":{"to":751},"pat":{"to":71},"note":"A key LED-lighting supplier to Honda and TVS."},
   "moat":"A leading 2W LED-lighting supplier to big OEMs like Honda and TVS — an EV-agnostic, growing niche.","moatStrength":"WIDE"},
  "Eighth, Fiem Industries — the two-wheeler light maker. [pause] It supplies LED lamps and signals "
  "to big two-wheeler makers like Honda and TVS. [pause] Revenue was about seven hundred fifty crore, "
  "profit seventy-one crore. [pause] It trades near twenty-seven times earnings. [pause] "
  "Its moat is being a trusted LED-lighting partner to the biggest two-wheeler brands — and lighting doesn't care if the bike is electric."),

 # ---- PART 2: CABLES, LOCKS & THE RANE GROUP ----
 ("k_d2","au_divider",{"part":"PART TWO","title":"Cables, Locks & Steering","sub":"The mechanical bits — and the Rane group","color":UP,"pips":3,"at":2},
  "Part two — cables, locks and steering, including the well-regarded Rane group. [pause] The "
  "mechanical and safety parts that connect the driver to the machine."),

 ("k09_suprajit","au_company",
  {"idx":"09 / 23","kicker":"CABLES · LOCKS","name":"Suprajit Engineering","ticker":"SUPRAJIT","price":"₹522","pe":"38.1×","seg":"Control cables",
   "biz":["The world's largest maker of automotive control cables","Plus halogen bulbs and speedometers","Supplies OEMs and the aftermarket globally"],
   "fin":{"qlabel":"Q1 FY27 · Jun 2026","rev":{"to":1070},"pat":{"to":52},"note":"Global cable leadership, expanding via acquisitions."},
   "moat":"The world's largest control-cable maker — global scale and cost leadership in a humble but essential part.","moatStrength":"WIDE"},
  "Ninth, Suprajit Engineering — a hidden world-leader. [pause] It's the world's largest maker of the "
  "control cables that connect your throttle, brake and clutch. [pause] Revenue was about a thousand "
  "seventy crore, profit fifty-two crore. [pause] It trades near thirty-eight times earnings. [pause] "
  "Its moat is wide — global scale and cost leadership in a simple, essential part almost every vehicle needs."),

 ("k10_sandhar","au_company",
  {"idx":"10 / 23","kicker":"CABLES · LOCKS","name":"Sandhar Technologies","ticker":"SANDHAR","price":"₹667","pe":"20.0×","seg":"Locks & mirrors",
   "biz":["Locking systems, mirrors and die-cast parts","Sheet-metal components and cabins","Many joint ventures with global partners"],
   "fin":{"qlabel":"Latest reported · Q1 FY26 (Jun-25)","rev":{"to":1090},"pat":{"to":28},"note":"Diversified via JVs, but margins are on the thinner side."},
   "moat":"A diversified locks-and-mirrors maker with many global JVs — broad, but modest margins.","moatStrength":"NARROW"},
  "Tenth, Sandhar Technologies — the lock maker. [pause] It makes locking systems, mirrors and "
  "die-cast parts, often through joint ventures. [pause] Revenue was about eleven hundred crore, but "
  "profit only twenty-eight crore. [pause] It trades near twenty times earnings. [pause] "
  "Its moat is a broad base of products and partners — useful, but the thin margins keep it from being dominant."),

 ("k11_remsons","au_company",
  {"idx":"11 / 23","kicker":"CABLES · LOCKS","name":"Remsons Industries","ticker":"REMSONSIND","price":"₹90.2","pe":"16.9×","seg":"Cables & shifters",
   "biz":["Control cables and gear-shift systems","Mechanical and electronic components","For two-, three- and four-wheelers"],
   "fin":{"qlabel":"Latest reported · Q1 FY26 (Jun-25)","rev":{"to":100},"pat":{"to":5},"note":"A small cable maker competing with the much larger Suprajit."},
   "moat":"A small cables-and-shifters maker — a real niche, but dwarfed by Suprajit and short on scale.","moatStrength":"WEAK"},
  "Eleventh, Remsons Industries — Suprajit's small rival. [pause] It makes control cables and "
  "gear-shift systems too, but at a fraction of the size. [pause] Revenue was about a hundred crore, "
  "profit five crore. [pause] It trades near seventeen times earnings. [pause] "
  "Its moat is weak — the same products as the leader, but without the scale to compete on cost."),

 ("k12_pavna","au_company",
  {"idx":"12 / 23","kicker":"CABLES · LOCKS","name":"Pavna Industries","ticker":"PAVNAIND","price":"₹18.3","pe":"41.9×","seg":"Locks & switches",
   "biz":["Ignition switches, lock kits and handlebars","Switches for two- and three-wheelers","Security and electrical control parts"],
   "fin":{"qlabel":"Q1 FY27 · Jun 2026","rev":{"to":54},"pat":{"to":2},"note":"A micro-cap supplier of locks and switches."},
   "moat":"A micro-cap lock-and-switch maker — a small niche with limited scale or differentiation.","moatStrength":"WEAK"},
  "Twelfth, Pavna Industries — a micro-cap. [pause] It makes ignition switches and lock kits for "
  "two- and three-wheelers. [pause] It's tiny — revenue about fifty-four crore, profit two crore. "
  "[pause] It trades near forty-two times earnings. [pause] "
  "Its moat is weak — a small supplier of simple parts, with little to protect it from competition."),

 ("k13_ppap","au_company",
  {"idx":"13 / 23","kicker":"CABLES · LOCKS","name":"PPAP Automotive","ticker":"PPAP","price":"₹321","pe":"112×","seg":"Sealing & plastics",
   "biz":["Automotive sealing systems and weatherstrips","Injection-moulded interior and exterior plastics","With Japanese technical partners"],
   "fin":{"qlabel":"Q1 FY27 · Jun 2026","rev":{"to":156},"note":"Revenue up ~34%, but barely profitable — hence a huge P/E."},
   "moat":"A sealing-and-plastics maker with Japanese tech — a decent niche, but thin profits and an extreme valuation.","moatStrength":"WEAK"},
  "Thirteenth, PPAP Automotive — pricey for what it earns. [pause] It makes sealing systems and "
  "moulded plastic parts with Japanese partners. [pause] Revenue rose about thirty-four percent to a "
  "hundred fifty-six crore, but it barely made a profit. [pause] So its P E is an eye-watering hundred "
  "and twelve. [pause] "
  "Its moat is a decent niche — but the tiny profit and huge valuation are a warning sign, not a strength."),

 ("k14_ranemadras","au_company",
  {"idx":"14 / 23","kicker":"CABLES · LOCKS","name":"Rane (Madras)","ticker":"RML","price":"₹1,054","pe":"24.1×","seg":"Steering & suspension",
   "biz":["Steering and suspension systems","Ball joints, linkages and die-casting","Just bought Hindustan Composites' friction business"],
   "fin":{"qlabel":"Q1 FY27 · Jun 2026","rev":{"to":1042},"pat":{"to":30},"note":"Buying the friction business we saw in Part 4 expands its range."},
   "moat":"A quality Rane-group steering and suspension maker, now adding friction — a steady, well-run compounder.","moatStrength":"NARROW"},
  "Fourteenth, Rane Madras — quality and steady. [pause] Part of the respected Rane group, it makes "
  "steering and suspension parts — and it just bought the friction business from Hindustan Composites, "
  "which we saw earlier. [pause] Revenue was about a thousand crore, profit thirty crore. [pause] It "
  "trades near twenty-four times earnings. [pause] "
  "Its moat is Rane-group quality and steady execution — a reliable compounder that keeps widening its range."),

 ("k15_raneholdings","au_company",
  {"idx":"15 / 23","kicker":"CABLES · LOCKS","name":"Rane Holdings","ticker":"RANEHOLDIN","price":"₹1,766","pe":"31.9×","seg":"Rane group holdco",
   "biz":["The holding company of the Rane group","Steering, seatbelts, friction and engine valves","Through its listed and JV companies"],
   "fin":{"qlabel":"Latest reported · Q4 FY26 (Mar-26)","rev":{"to":1609},"pat":{"to":88},"note":"A way to own the whole Rane group in one stock."},
   "moat":"The parent that owns a portfolio of solid Rane businesses — quality management, but a holding-company discount.","moatStrength":"NARROW"},
  "Fifteenth, Rane Holdings — the parent. [pause] It's the holding company that owns the various Rane "
  "businesses — steering, seatbelts, valves and friction. [pause] Revenue was about sixteen hundred "
  "crore, profit eighty-eight crore. [pause] It trades near thirty-two times earnings. [pause] "
  "Its moat is owning a whole family of good businesses — though holding companies usually trade at a discount to their parts."),

 # ---- PART 3: DEALERS, DISTRIBUTION & THE REST ----
 ("m_d3","au_divider",{"part":"PART THREE","title":"Dealers & Distribution","sub":"Selling and servicing it all","color":VAL,"pips":3,"at":3},
  "And the final chapter — dealers, distributors and a few odds and ends. [pause] The businesses that "
  "sell, service and distribute everything the rest of the sector makes."),

 ("m16_impal","au_company",
  {"idx":"16 / 23","kicker":"DEALERS · DISTRIBUTION","name":"India Motor Parts (IMPAL)","ticker":"IMPAL","price":"₹1,098","pe":"17.5×","seg":"Parts distribution",
   "biz":["A TVS-group spare-parts distributor","One of India's largest aftermarket networks","Distributes a wide range of components"],
   "fin":{"qlabel":"Q1 FY27 · Jun 2026","rev":{"to":234},"pat":{"to":22},"note":"Cash-rich and cheap — a quiet, steady distributor."},
   "moat":"A large, trusted aftermarket distribution network in the TVS group — cash-rich, steady and cheaply valued.","moatStrength":"NARROW"},
  "Sixteenth, India Motor Parts, or IMPAL — the distributor. [pause] Part of the TVS group, it runs "
  "one of India's largest spare-parts distribution networks. [pause] Revenue was about two hundred "
  "thirty crore, profit twenty-two crore. [pause] It's cheap and cash-rich, near seventeen times "
  "earnings. [pause] "
  "Its moat is a wide, trusted distribution network — unglamorous, but steady and hard to rebuild from scratch."),

 ("m17_landmark","au_company",
  {"idx":"17 / 23","kicker":"DEALERS · DISTRIBUTION","name":"Landmark Cars","ticker":"LANDMARK","price":"₹535","pe":"56.8×","seg":"Luxury dealership",
   "biz":["A leading premium and luxury car dealership","Mercedes, Honda, Jeep, VW, Renault and BYD","New sales, service, spares and pre-owned cars"],
   "fin":{"qlabel":"Latest reported · Q1 FY26 (Jun-25)","rev":{"to":1062},"pat":{"to":7},"note":"Big revenue, but razor-thin dealership margins."},
   "moat":"A leading luxury-car dealer — but dealerships are low-margin, capital-heavy and depend on carmakers.","moatStrength":"NARROW"},
  "Seventeenth, Landmark Cars — the luxury dealer. [pause] It retails premium brands like Mercedes "
  "and Jeep, plus service and pre-owned cars. [pause] Revenue was big, about a thousand crore, but "
  "profit only seven crore — dealerships run on razor-thin margins. [pause] It trades near fifty-seven "
  "times earnings. [pause] "
  "Its moat is narrow — a good retailer, but it doesn't own the brands and margins are structurally thin."),

 ("m18_jma","au_company",
  {"idx":"18 / 23","kicker":"DEALERS · DISTRIBUTION","name":"Jullundur Motor Agency","ticker":"JMA","price":"₹88.4","pe":"6.80×","seg":"Parts trading",
   "biz":["A long-established parts and accessories distributor","Batteries, lubricants and petroleum products","Trading and distribution across India"],
   "fin":{"qlabel":"Latest reported · Q4 FY26 (Mar-26)","rev":{"to":622},"pat":{"to":30},"note":"Very cheap — trades below book value, with lean debt."},
   "moat":"A long-standing parts distributor — thin-margin trading, but strikingly cheap, below book value.","moatStrength":"NARROW"},
  "Eighteenth, Jullundur Motor Agency — deep value. [pause] A long-established distributor of parts, "
  "batteries and lubricants. [pause] Revenue was about six hundred twenty crore, profit thirty crore. "
  "[pause] And it's remarkably cheap — under seven times earnings, below its book value. [pause] "
  "Its moat is narrow — distribution is thin-margin — but the valuation is the striking part of this story."),

 ("m19_kalyanicom","au_company",
  {"idx":"19 / 23","kicker":"DEALERS · DISTRIBUTION","name":"Kalyani Commercials","ticker":"KALYANI","price":"₹138","pe":"5.71×","seg":"Vehicle dealership",
   "biz":["A commercial-vehicle and tractor dealership","Deals in vehicles, spares and services","A small-cap trading and distribution business"],
   "fin":{"qlabel":"Latest reported · FY25","rev":{"to":229},"pat":{"to":2},"note":"Thinly traded, small dealership; data is dated — verify."},
   "moat":"A tiny CV/tractor dealership — low-margin trading with little scale; the cheap P/E reflects the small size.","moatStrength":"WEAK"},
  "Nineteenth, Kalyani Commercials — a tiny dealer. [pause] It's a small commercial-vehicle and "
  "tractor dealership. [pause] Revenue was about two hundred thirty crore, but profit only two crore. "
  "[pause] It's thinly traded, so treat its numbers with care and verify them. [pause] "
  "Its moat is weak — a small, low-margin dealer, which is why it trades so cheaply."),

 ("m20_majestic","au_company",
  {"idx":"20 / 23","kicker":"DEALERS · DISTRIBUTION","name":"Majestic Auto","ticker":"MAJESAUT","price":"₹492","pe":"22.8×","seg":"Investments",
   "biz":["Historically a moped and components maker","Part of the Hero (Munjal) group legacy","Now largely an investment company"],
   "fin":{"qlabel":"Q1 FY27 · Jun 2026","rev":{"to":15},"pat":{"to":14},"note":"Profit exceeds sales — earnings now come from investments, not operations."},
   "moat":"No operating moat — its profit comes from investments, not from making anything. An asset story.","moatStrength":"WEAK"},
  "Twentieth, Majestic Auto — not really a parts maker anymore. [pause] Once a moped and components "
  "company in the Hero group, it now mostly holds investments. [pause] The giveaway: its profit of "
  "fourteen crore is larger than its fifteen crore of sales — the earnings come from investments. [pause] "
  "Its moat is none, operationally — this is an investment holding company wearing an auto-parts name."),

 ("m21_autoline","au_company",
  {"idx":"21 / 23","kicker":"DEALERS · DISTRIBUTION","name":"Autoline Industries","ticker":"AUTOIND","price":"₹93.8","pe":"21.6×","seg":"Sheet metal",
   "biz":["Sheet-metal components and pressed parts","Sub-assemblies and pedal-box assemblies","A tier-1 supplier to CV and PV makers"],
   "fin":{"qlabel":"Latest reported · Q1 FY26 (Jun-25)","rev":{"to":152},"pat":{"to":1},"note":"A small stamper with wafer-thin, volatile profits."},
   "moat":"A small sheet-metal supplier — commoditised pressings with thin, volatile margins and little pricing power.","moatStrength":"WEAK"},
  "Twenty-first, Autoline Industries — a small presser. [pause] It makes sheet-metal parts and pedal "
  "assemblies for carmakers. [pause] Revenue was about a hundred fifty crore, but profit only one "
  "crore. [pause] It trades near twenty-two times earnings. [pause] "
  "Its moat is weak — pressed sheet-metal is commoditised, so its profits are thin and swing around a lot."),

 ("m22_omax","au_company",
  {"idx":"22 / 23","kicker":"DEALERS · DISTRIBUTION","name":"Omax Autos","ticker":"OMAXAUTO","price":"₹183","pe":"N/A","seg":"Sheet metal",
   "biz":["Sheet-metal, tubular and machined components","For two-wheelers and commercial vehicles","Also supplies railways"],
   "fin":{"pending":True,"qlabel":"Recent results modest / near breakeven","note":"A restructured sheet-metal maker that has struggled to earn consistently."},
   "moat":"A restructured sheet-metal supplier that has struggled for years — little in the way of a durable edge.","moatStrength":"WEAK"},
  "Twenty-second, Omax Autos — a long turnaround. [pause] It makes sheet-metal and machined parts for "
  "two-wheelers, commercial vehicles and railways. [pause] But it has struggled to earn consistently "
  "for years, hovering around breakeven. [pause] "
  "Its moat is weak — like the other stampers, it's a commoditised business that's found profitability hard to hold."),

 ("m23_jbm","au_company",
  {"idx":"23 / 23","kicker":"DEALERS · DISTRIBUTION","name":"JBM Auto","ticker":"JBMA","price":"₹649","pe":"66.7×","seg":"Sheet metal + e-buses",
   "biz":["Sheet-metal components, tools and dies","A fast-growing electric-bus business (Ecolife)","E-buses and charging solutions"],
   "fin":{"qlabel":"Q1 FY27 · Jun 2026","rev":{"to":1442},"pat":{"to":44},"note":"An e-bus market leader with 30-35% share — hence the rich P/E."},
   "moat":"A traditional parts maker turned e-bus leader (30-35% share) — real EV momentum, but leveraged and richly priced.","moatStrength":"EMERGING"},
  "And finally, twenty-third, JBM Auto — from panels to e-buses. [pause] It started in sheet metal, "
  "but it's now a leader in electric buses, with roughly a third of the market. [pause] Revenue was "
  "about fourteen hundred crore, profit forty-four crore. [pause] It trades at a rich sixty-seven "
  "times earnings, on those EV-bus hopes. [pause] "
  "Its moat is emerging — genuine leadership in electric buses — but it's carrying debt, and the price already assumes success."),

 ("v6_recap","au_recap",
  {"title":"Electricals & Aftermarket — and the whole sector","color":BIZC,
   "items":[
     "Motherson, UNO Minda, Suprajit: global-scale champions",
     "Wiring & lighting GAIN from EVs — content per vehicle rises",
     "The Rane group: quiet, quality compounders",
     "Dealers & distributors are cheap but thin-margin",
     "Across 125 companies, moats ranged from wide to none",
     "EV-agnostic winners: wiring, lighting, bearings, fasteners",
     "Always match the price you pay to the moat you get",
   ],
   "closer":"Six parts, 125 companies — now you can read the whole Indian auto sector. Thanks for watching."},
  "So, in one breath — and then the whole sector. [pause] Motherson, UNO Minda and Suprajit are "
  "global-scale champions, and here's the key insight: wiring and lighting actually gain from "
  "electric vehicles, because the content per car rises. [pause] The Rane group are quiet quality "
  "compounders, while the dealers and distributors are cheap but thin-margin. [pause] "
  "And stepping back across all one hundred and twenty-five companies we've covered — moats ranged "
  "from wide, like Bosch, Motherson and Royal Enfield, all the way down to none. [pause] The safest "
  "bets on the electric shift are the EV-agnostic parts — wiring, lighting, bearings and fasteners. [pause] "
  "The one lesson that ties it all together: always match the price you pay to the moat you get. [pause] "
  "Six parts, one hundred and twenty-five companies — you can now read the entire Indian auto sector. "
  "Thanks for watching."),
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
cl=os.path.join(ROOT,"concat6.txt")
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
