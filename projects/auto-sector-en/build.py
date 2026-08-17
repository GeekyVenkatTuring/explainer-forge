#!/usr/bin/env python3
"""Indian Auto Sector — Video 1: VEHICLE MAKERS (English, Nova).

Company-by-company tour built from the sector PDF (125 companies, this video = 18
vehicle makers / OEMs). Each beat: what they do · latest quarter · P/E · moat.

Data: price + P/E from Screener.in (NSE close 07-Aug-2026, matches source PDF).
Revenue/PAT from Q1 FY27 (Apr-Jun 2026) results-day coverage (Business Standard /
Equitybulls / company PR), triangulated where sources disagreed. Several names report
~13-17 Aug 2026 (not out at build time) -> shown as "results due" / latest reported.
ALL numbers approximate; on-screen disclaimer on every card. Education, not advice.
Research log: research/vehicle-makers.md.

Usage: python3 build.py            (Voicebox.app must be open for Nova TTS)
"""
import json, os, subprocess, time, urllib.request

BASE = "http://127.0.0.1:17493"
PROFILE = "c488e05c-3407-46a3-874d-1b09b3aff78d"  # "TTS Bright (Nova)"
GAP = 0.5
PAUSE = 0.6
ATEMPO = 0.95
PREFIX = "au"
ROOT = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(ROOT, "..", ".."))
PUBLIC = os.path.join(REPO, "composer", "public", PREFIX)
RAW = os.path.join(ROOT, "assets", "raw")
FIN = os.path.join(ROOT, "assets")
for d in (PUBLIC, RAW, os.path.join(ROOT, "artifacts"), os.path.join(ROOT, "renders")):
    os.makedirs(d, exist_ok=True)

BIZC, UP, MOAT, VAL = "#38BDF8", "#34D399", "#A78BFA", "#FBBF24"

# ---------------------------------------------------------------- SCREENPLAY
# (seg_id, variant, props, narration)
SEGMENTS = [
 ("s00_title", "au_title",
  {"kicker": "AUTO & AUTO-COMPONENTS · PART 1 OF 6", "title": "Indian Auto Stocks\nThe Vehicle Makers",
   "sub": "18 companies · what they do · latest quarter · P/E · their moat"},
  "Welcome to a company-by-company tour of India's automobile sector. [pause] "
  "This first part covers the vehicle makers — the brands that actually build the cars, "
  "bikes, buses and tractors. [pause] For each one, we cover four things: what they do, "
  "their latest quarter, their P E, and their moat — the edge that protects them. [pause] "
  "One note. These figures are approximate — always verify on your own terminal. "
  "This is education, not investment advice."),

 # ---- PART 1: FOUR-WHEELERS ----
 ("d1", "au_divider",
  {"part": "PART ONE", "title": "The Four-Wheelers", "sub": "Cars, SUVs, vans — and the electric shift",
   "color": BIZC, "pips": 4, "at": 1},
  "Part one — the four-wheelers. [pause] The car and utility-vehicle makers, where scale, "
  "distribution, and the move to electric decide the winners."),

 ("c01_maruti", "au_company",
  {"idx": "01 / 18", "kicker": "FOUR-WHEELERS", "name": "Maruti Suzuki", "ticker": "MARUTI",
   "price": "₹14,037", "pe": "30.8×", "seg": "Passenger cars",
   "biz": ["India's number-one carmaker — Suzuki small cars to SUVs like Swift, Brezza and Grand Vitara",
           "The widest sales and service network in the country",
           "A leading exporter of cars made in India"],
   "fin": {"qlabel": "Q1 FY27 · Apr–Jun 2026 (standalone)",
           "rev": {"to": 52456, "yoy": "+37%", "up": True},
           "pat": {"to": 3352, "yoy": "−11%", "up": False},
           "note": "Volumes up ~29%, but margins squeezed by raw-material costs and model mix."},
   "moat": "Unmatched distribution — around 4,000 outlets, scale-driven low costs and resale value nobody can match.",
   "moatStrength": "WIDE"},
  "First, Maruti Suzuki — India's number-one carmaker. [pause] It builds everything from the Swift "
  "to the Grand Vitara, sold through the widest service network in the country. [pause] "
  "Last quarter, revenue jumped thirty-seven percent to about fifty-two thousand crore. "
  "But net profit slipped eleven percent, to roughly thirty-three hundred crore, as costs and mix "
  "hit margins. [pause] The stock trades near thirty-one times earnings. [pause] "
  "Its moat is that distribution — thousands of outlets, low costs, and unbeatable resale value."),

 ("c02_hyundai", "au_company",
  {"idx": "02 / 18", "kicker": "FOUR-WHEELERS", "name": "Hyundai Motor India", "ticker": "HYUNDAI",
   "price": "₹2,200", "pe": "36.1×", "seg": "Passenger cars",
   "biz": ["India's number-two carmaker — SUV-led, with Creta, Venue, i20 and Verna",
           "Builds locally and exports across dozens of markets",
           "The India arm of Korea's Hyundai Motor"],
   "fin": {"qlabel": "Q1 FY27 (consolidated)",
           "rev": {"to": 16335, "yoy": "−0.5%", "up": False},
           "pat": {"to": 889, "yoy": "−35%", "up": False},
           "note": "Hit by a plant fire and West-Asia export disruption; rural mix at an all-time high."},
   "moat": "Brand pull and SUV-design leadership, plus a large export base that softens India's ups and downs.",
   "moatStrength": "NARROW"},
  "Next, Hyundai Motor India — the country's number-two carmaker. [pause] It's SUV-heavy, "
  "with the Creta and Venue, and it exports cars to dozens of markets. [pause] "
  "This quarter was tough: profit fell thirty-five percent to under nine hundred crore, "
  "hurt by a plant fire and disruption to Middle-East exports. Revenue was roughly flat. [pause] "
  "It trades near thirty-six times earnings. [pause] "
  "Its edge is brand and design in SUVs, plus a big export base that steadies the India cycle."),

 ("c03_tmpv", "au_company",
  {"idx": "03 / 18", "kicker": "FOUR-WHEELERS", "name": "Tata Motors Passenger Vehicles", "ticker": "TMPV",
   "price": "₹347", "pe": "n.m.", "seg": "PV · EV · JLR",
   "biz": ["Tata's demerged passenger-vehicle and EV business",
           "Home to Nexon, Punch and Harrier — and India's best-selling electric cars",
           "Also owns Jaguar Land Rover, the global luxury brands"],
   "fin": {"pending": True, "qlabel": "Q1 FY27 due 13-Aug (not out)",
           "note": "Q1 India PV sales up 46%, EV volumes up 112%. Earnings swing with Jaguar Land Rover."},
   "moat": "India's EV-car first-mover with a charging ecosystem, plus JLR's global brands — offset by JLR's cyclicality.",
   "moatStrength": "NARROW"},
  "Third, Tata Motors Passenger Vehicles — the demerged Tata car business. [pause] "
  "It owns the Nexon and Punch, India's best-selling electric cars, and also Jaguar Land Rover. [pause] "
  "Its first-quarter results land on the thirteenth of August, so they aren't out yet. But India car "
  "sales rose forty-six percent, and electric volumes more than doubled. [pause] "
  "Because of the recent demerger, its printed P E isn't meaningful — check it carefully. [pause] "
  "Its moat is EV leadership at home, plus J L R's luxury brands abroad — though Land Rover's cycle cuts both ways."),

 ("c04_mm", "au_company",
  {"idx": "04 / 18", "kicker": "FOUR-WHEELERS", "name": "Mahindra & Mahindra", "ticker": "M&M",
   "price": "₹3,502", "pe": "22.7×", "seg": "SUVs + tractors",
   "biz": ["India's SUV powerhouse — Thar, Scorpio, XUV and BE electric SUVs",
           "The country's number-one tractor maker, by a wide margin",
           "Plus finance, IT and mobility arms"],
   "fin": {"qlabel": "Q1 FY27 (consolidated)",
           "rev": {"to": 57533, "yoy": "+27%", "up": True},
           "pat": {"to": 5455, "yoy": "+34%", "up": True},
           "note": "Broad-based: autos, farm equipment and services all grew."},
   "moat": "Tractor-market leadership plus a red-hot SUV franchise — deep rural distribution few rivals can match.",
   "moatStrength": "WIDE"},
  "Fourth, Mahindra and Mahindra — a rare two-engine company. [pause] It's an SUV powerhouse, "
  "with the Thar and Scorpio, and it's also India's biggest tractor maker. [pause] "
  "A stellar quarter: profit rose thirty-four percent to about fifty-four hundred crore, on revenue "
  "up twenty-seven percent. Autos, farm and services all grew. [pause] "
  "It trades near twenty-three times earnings — reasonable for the growth. [pause] "
  "Its moat is that combination: SUV heat plus the tractor throne, and rural reach nobody else has."),

 ("c05_force", "au_company",
  {"idx": "05 / 18", "kicker": "FOUR-WHEELERS", "name": "Force Motors", "ticker": "FORCEMOT",
   "price": "₹18,500", "pe": "22.2×", "seg": "Vans · UVs · engines",
   "biz": ["Makes the Traveller vans, plus Urbania and Gurkha utility vehicles",
           "Assembles engines and axles for BMW and Mercedes-Benz in India",
           "Also builds tractors and small commercial vehicles"],
   "fin": {"qlabel": "Q1 FY27 (consolidated)",
           "rev": {"to": 2440, "yoy": "+6%", "up": True},
           "pat": {"to": 217, "yoy": "+23%", "up": True},
           "note": "Profit grew strongly on a modest revenue rise."},
   "moat": "Near-monopoly in shared-mobility vans, plus sticky, high-trust engine-assembly contracts with BMW and Mercedes.",
   "moatStrength": "NARROW"},
  "Fifth, Force Motors — a quiet niche champion. [pause] It makes the Traveller vans you see as "
  "shared taxis, and it assembles engines and axles for BMW and Mercedes in India. [pause] "
  "Profit rose twenty-three percent to about two hundred seventeen crore, though revenue grew just six percent. [pause] "
  "It trades near twenty-two times earnings. [pause] "
  "Its moat is dominance in vans, plus those trusted engine contracts with the German luxury makers."),

 # ---- PART 2: TWO & THREE-WHEELERS ----
 ("d2", "au_divider",
  {"part": "PART TWO", "title": "Two & Three-Wheelers", "sub": "India's bikes, scooters and autorickshaws",
   "color": UP, "pips": 4, "at": 2},
  "Part two — two and three-wheelers. [pause] This is India's heartland: the bikes, scooters "
  "and autorickshaws that move the country, made by some of the world's largest players."),

 ("c06_hero", "au_company",
  {"idx": "06 / 18", "kicker": "TWO & THREE-WHEELERS", "name": "Hero MotoCorp", "ticker": "HEROMOTOCO",
   "price": "₹5,725", "pe": "20.7×", "seg": "Two-wheelers",
   "biz": ["The world's largest two-wheeler maker by volume",
           "Commuter king — Splendor and HF Deluxe dominate the mass market",
           "Now pushing scooters, premium bikes and Vida electric"],
   "fin": {"qlabel": "Q1 FY27 (consolidated)",
           "rev": {"to": 13126, "yoy": "+35%", "up": True},
           "pat": {"to": 1418, "yoy": "−17%", "up": False},
           "note": "Profit dip is a high base — last year had a one-off gain."},
   "moat": "Unrivalled scale and the deepest rural dealer network — the lowest cost per bike. Watch the EV transition.",
   "moatStrength": "WIDE"},
  "Sixth, Hero MotoCorp — the world's largest two-wheeler maker. [pause] Its commuter bikes, "
  "the Splendor and H-F Deluxe, are everywhere in small-town India. [pause] "
  "Revenue rose thirty-five percent, but profit fell seventeen percent to about fourteen hundred crore — "
  "that drop is a high base, since last year had a one-time gain. [pause] "
  "It trades near twenty-one times earnings. [pause] "
  "Its moat is sheer scale and rural reach — the lowest cost per bike. The question is the electric shift."),

 ("c07_bajaj", "au_company",
  {"idx": "07 / 18", "kicker": "TWO & THREE-WHEELERS", "name": "Bajaj Auto", "ticker": "BAJAJ-AUTO",
   "price": "₹11,662", "pe": "27.2×", "seg": "2W · 3W · exports",
   "biz": ["Pulsar and Dominar bikes, plus Chetak electric scooters",
           "Dominates three-wheelers and exports heavily",
           "Owns stakes in KTM and Husqvarna"],
   "fin": {"qlabel": "Q1 FY27 (standalone)",
           "rev": {"to": 17244, "yoy": "+37%", "up": True},
           "pat": {"to": 2983, "yoy": "+42%", "up": True},
           "note": "Consolidated numbers jump further after folding in its KTM holding."},
   "moat": "A world-class export franchise, near-duopoly in three-wheelers, and premium bikes powered by KTM tech.",
   "moatStrength": "WIDE"},
  "Seventh, Bajaj Auto — the great exporter. [pause] It makes Pulsar bikes and Chetak electric "
  "scooters, dominates autorickshaws, and ships huge volumes overseas. [pause] "
  "A strong quarter: profit up forty-two percent to about three thousand crore, on revenue up "
  "thirty-seven percent. [pause] It trades near twenty-seven times earnings. [pause] "
  "Its moat is that export machine, a near-duopoly in three-wheelers, and premium motorcycles built with KTM."),

 ("c08_tvs", "au_company",
  {"idx": "08 / 18", "kicker": "TWO & THREE-WHEELERS", "name": "TVS Motor", "ticker": "TVSMOTOR",
   "price": "₹4,441", "pe": "61.0×", "seg": "Two & three-wheelers",
   "biz": ["Apache bikes, Jupiter scooters and the iQube electric",
           "Strong exports, and owns the Norton brand",
           "A relentless premiumisation push"],
   "fin": {"qlabel": "Q1 FY27 (consolidated)",
           "rev": {"to": 16296, "yoy": "+34%", "up": True},
           "pat": {"to": 1058, "yoy": "+65%", "up": True},
           "note": "Electric two-wheeler sales nearly doubled."},
   "moat": "Design and premiumisation, plus fast-growing iQube EV leadership — a rich P/E prices this optimism in.",
   "moatStrength": "NARROW"},
  "Eighth, TVS Motor — the momentum stock. [pause] It makes Apache bikes, Jupiter scooters, "
  "and the iQube electric, and it owns Norton. [pause] "
  "A record quarter: profit surged sixty-five percent to about a thousand crore, and its electric "
  "scooter sales nearly doubled. [pause] But the stock is expensive, near sixty-one times earnings. [pause] "
  "Its moat is design and premiumisation, plus fast-growing electric — though the price already assumes a lot."),

 ("c09_eicher", "au_company",
  {"idx": "09 / 18", "kicker": "TWO & THREE-WHEELERS", "name": "Eicher Motors", "ticker": "EICHERMOT",
   "price": "₹8,020", "pe": "37.8×", "seg": "Royal Enfield + trucks",
   "biz": ["Owns Royal Enfield — India's iconic mid-size motorcycle brand",
           "A near-monopoly from 250 to 750cc",
           "Half-owns the VECV truck and bus joint venture with Volvo"],
   "fin": {"qlabel": "Q1 FY27 (consolidated)",
           "rev": {"to": 6632, "yoy": "+32%", "up": True},
           "pat": {"to": 1463, "yoy": "+21%", "up": True},
           "note": "Royal Enfield sold a record 332,940 motorcycles."},
   "moat": "One of Indian autos' strongest brand moats — cult loyalty and pricing power around Royal Enfield.",
   "moatStrength": "WIDE"},
  "Ninth, Eicher Motors — the brand story. [pause] It owns Royal Enfield, the cult motorcycle "
  "brand that all but owns the mid-size segment, and half of a truck venture with Volvo. [pause] "
  "Profit rose twenty-one percent to about fourteen hundred crore, on record Enfield sales. [pause] "
  "It trades near thirty-eight times earnings. [pause] "
  "Its moat is that brand — loyalty and pricing power few products in India can match."),

 ("c10_atul", "au_company",
  {"idx": "10 / 18", "kicker": "TWO & THREE-WHEELERS", "name": "Atul Auto", "ticker": "ATULAUTO",
   "price": "₹577", "pe": "33.2×", "seg": "Three-wheelers",
   "biz": ["Gujarat maker of Atul Gem and Shakti three-wheelers",
           "Diesel, CNG, petrol and electric last-mile autos",
           "A small player trying to turn the corner"],
   "fin": {"qlabel": "Q1 FY27",
           "rev": {"to": 215, "yoy": "+42%", "up": True},
           "pat": {"to": 8, "yoy": "+169%", "up": True},
           "note": "Fast growth — but off a small base; profit is only about ₹8 crore."},
   "moat": "Modest — a regional three-wheeler brand chasing an EV turnaround, not a structural edge.",
   "moatStrength": "WEAK"},
  "Tenth, Atul Auto — the small challenger. [pause] This Gujarat company makes three-wheelers "
  "for last-mile transport, in diesel, C-N-G and electric. [pause] "
  "Revenue rose forty-two percent and profit jumped, but off a tiny base — it's just eight crore. [pause] "
  "The stock still trades near thirty-three times earnings. [pause] "
  "Honestly, its moat is weak — it's a regional brand chasing a turnaround, up against much bigger rivals."),

 # ---- PART 3: ELECTRIC UPSTARTS ----
 ("d3", "au_divider",
  {"part": "PART THREE", "title": "The Electric Upstarts", "sub": "EV scooters, buses and hopefuls",
   "color": MOAT, "pips": 4, "at": 3},
  "Part three — the electric upstarts. [pause] The pure-play E-V makers. Big growth, big ambition — "
  "and, for most of them, big losses that they're racing to close."),

 ("c11_ather", "au_company",
  {"idx": "11 / 18", "kicker": "ELECTRIC", "name": "Ather Energy", "ticker": "ATHERENERG",
   "price": "₹1,482", "pe": "N/A", "seg": "Electric scooters",
   "biz": ["Premium 450-series electric scooters",
           "In-house Atherstack software and the Ather Grid charging network",
           "Designs its own vehicles and batteries"],
   "fin": {"qlabel": "Q1 FY27",
           "rev": {"to": 1217, "yoy": "+89%", "up": True},
           "pat": {"to": 51, "yoy": "71% narrower", "up": True, "loss": True, "label": "Net loss"},
           "note": "Loss narrowed sharply and — importantly — EBITDA turned positive."},
   "moat": "An emerging tech moat — its own software and fast-charging network — but it's still loss-making.",
   "moatStrength": "EMERGING"},
  "Eleventh, Ather Energy — the tech-led one. [pause] It makes premium 450 electric scooters, "
  "with its own software and its own fast-charging network. [pause] "
  "Revenue nearly doubled, up eighty-nine percent, and the net loss narrowed to just fifty-one crore — "
  "with operating profit finally turning positive. [pause] It's loss-making, so there's no P E yet. [pause] "
  "Its moat is emerging — software and charging that lock customers in — but the profits still have to come."),

 ("c12_ola", "au_company",
  {"idx": "12 / 18", "kicker": "ELECTRIC", "name": "Ola Electric", "ticker": "OLAELEC",
   "price": "₹41", "pe": "N/A", "seg": "Electric scooters",
   "biz": ["S1-series electric scooters — once the clear market leader",
           "Vertically integrated, with its own battery-cell gigafactory plan",
           "Now entering electric motorcycles"],
   "fin": {"qlabel": "Q1 FY27",
           "rev": {"to": 455, "yoy": "−45%", "up": False},
           "pat": {"to": 336, "yoy": "22% narrower", "up": True, "loss": True, "label": "Net loss"},
           "note": "Revenue slid and share slipped; it raised ₹780 crore to keep funding operations."},
   "moat": "Contested and weak — scale on paper, but falling share, heavy cash burn and trust issues.",
   "moatStrength": "WEAK"},
  "Twelfth, Ola Electric — the cautionary tale. [pause] It builds S-one scooters and wants to make "
  "its own battery cells, and it's now entering electric motorcycles. [pause] "
  "But revenue fell forty-five percent as sales slid, and it's still losing money — a loss of "
  "three hundred thirty-six crore, even though that's narrower than before. [pause] "
  "It had to raise seven hundred eighty crore. [pause] "
  "Its moat is weak and contested — scale in theory, but shrinking share and heavy cash burn."),

 ("c13_olectra", "au_company",
  {"idx": "13 / 18", "kicker": "ELECTRIC", "name": "Olectra Greentech", "ticker": "OLECTRA",
   "price": "₹1,385", "pe": "64.0×", "seg": "Electric buses",
   "biz": ["India's largest electric-bus maker",
           "Built on a BYD technology tie-up",
           "Also makes composite insulators for the power grid"],
   "fin": {"pending": True, "qlabel": "Latest reported · Q1 FY26 (Jun-2025)",
           "rev": {"to": 347, "yoy": "+11%", "up": True},
           "pat": {"to": 26, "yoy": "+8%", "up": True},
           "note": "Fresh Q1 FY27 results land 13-Aug; figures shown are the prior June quarter."},
   "moat": "First-mover leadership in e-buses, with BYD tech and its MEIL parent's order access — but working-capital heavy.",
   "moatStrength": "EMERGING"},
  "Thirteenth, Olectra Greentech — the bus play. [pause] It's India's largest electric-bus maker, "
  "built on technology from China's B-Y-D, and it also makes power-grid insulators. [pause] "
  "Its new quarter is due on the thirteenth of August, so I'm showing the last reported one — about "
  "three hundred fifty crore of revenue and twenty-six crore of profit. [pause] "
  "It trades near sixty-four times earnings, on hopes for a big order book. [pause] "
  "Its moat is first-mover e-bus leadership — real, but the business ties up a lot of cash."),

 ("c14_mercury", "au_company",
  {"idx": "14 / 18", "kicker": "ELECTRIC", "name": "Mercury EV-Tech", "ticker": "MERCURYEV",
   "price": "₹35", "pe": "159×", "seg": "EV micro-cap",
   "biz": ["A micro-cap in electric two- and three-wheelers",
           "Makes e-rickshaws, EV parts and battery tech",
           "Very small scale and weak returns"],
   "fin": {"pending": True, "qlabel": "Latest reported · Q4 FY26",
           "rev": {"to": 25, "up": False},
           "note": "Q1 FY27 due 13-Aug; sales are trending down toward ₹20 crore. Return on equity ~1.5%."},
   "moat": "Effectively none — sub-scale, low returns, and earnings that lean on other income. Speculative.",
   "moatStrength": "NONE"},
  "Fourteenth, Mercury E-V Tech — and a word of caution. [pause] It's a tiny micro-cap making "
  "electric rickshaws and E-V parts. [pause] Sales are small, around twenty-five crore and falling, "
  "and its return on equity is barely one and a half percent. [pause] "
  "Yet the stock trades at a hundred and fifty-nine times earnings. [pause] "
  "Its moat is, frankly, none — it's sub-scale and speculative. I'm including it only for completeness."),

 # ---- PART 4: TRACTORS & LEGACY ----
 ("d4", "au_divider",
  {"part": "PART FOUR", "title": "Tractors & Legacy", "sub": "Farm power, engines and old names",
   "color": VAL, "pips": 4, "at": 4},
  "Part four — tractors and legacy names. [pause] Quiet, cash-rich farm-power niches, "
  "and a couple of old brands whose stories have moved on."),

 ("c15_swaraj", "au_company",
  {"idx": "15 / 18", "kicker": "TRACTORS & LEGACY", "name": "Swaraj Engines", "ticker": "SWARAJENG",
   "price": "₹3,600", "pe": "21.4×", "seg": "Tractor engines",
   "biz": ["Makes diesel engines for Swaraj-brand tractors",
           "The sole engine supplier to Mahindra's Swaraj line",
           "Just crossed 2 million engines made"],
   "fin": {"qlabel": "Q1 FY27 (standalone)",
           "rev": {"to": 588, "yoy": "+22%", "up": True},
           "pat": {"to": 56, "yoy": "+11%", "up": True},
           "note": "Record engine volumes; the business is cash-rich and high-return."},
   "moat": "A deep captive moat — the sole, sticky engine supplier to Mahindra's Swaraj tractors. That's also its dependency.",
   "moatStrength": "DEEP"},
  "Fifteenth, Swaraj Engines — a quiet compounder. [pause] It makes the diesel engines for "
  "Mahindra's Swaraj tractors, and it's the only supplier of them. [pause] "
  "Revenue rose twenty-two percent and profit eleven percent, on record engine volumes. It's "
  "cash-rich and highly profitable. [pause] It trades near twenty-one times earnings. [pause] "
  "Its moat is deep but narrow — a locked-in supplier to Mahindra. That relationship is its strength, and its risk."),

 ("c16_vst", "au_company",
  {"idx": "16 / 18", "kicker": "TRACTORS & LEGACY", "name": "VST Tillers Tractors", "ticker": "VSTTILLERS",
   "price": "₹4,487", "pe": "37.1×", "seg": "Power tillers & tractors",
   "biz": ["India's leading power-tiller maker",
           "Also small tractors, weeders and farm machinery",
           "Serves small-farm mechanisation"],
   "fin": {"pending": True, "qlabel": "Q1 FY27 due 13-Aug (not out)",
           "note": "Q1 volumes rose about 22%. Full results and the earnings call are on 13-Aug."},
   "moat": "Category leadership in power tillers — dominant share and dealer reach across the small-farm belt.",
   "moatStrength": "NARROW"},
  "Sixteenth, V-S-T Tillers Tractors — the small-farm specialist. [pause] It's India's leading maker "
  "of power tillers, the little machines that mechanise small farms, plus compact tractors. [pause] "
  "Its results are due on the thirteenth of August, but quarterly volumes rose about twenty-two percent. [pause] "
  "It trades near thirty-seven times earnings. [pause] "
  "Its moat is category leadership in tillers — dominant share and dealer reach where big tractor makers don't focus."),

 ("c17_tube", "au_company",
  {"idx": "17 / 18", "kicker": "TRACTORS & LEGACY", "name": "Tube Investments", "ticker": "TIINDIA",
   "price": "₹2,772", "pe": "81.2×", "seg": "Diversified engineering",
   "biz": ["Murugappa-group engineering — precision steel tubes and chains",
           "Bicycles — Hercules and BSA",
           "Building an EV arm: TI Clean Mobility, with e-3Ws, tractors and trucks"],
   "fin": {"pending": True, "qlabel": "Q1 FY27 due 14-Aug (not out)",
           "note": "Diversified: tubes, chains, cycles — plus a fast-scaling clean-mobility EV business."},
   "moat": "Murugappa's disciplined capital allocation and a diversified engineering platform, with real EV optionality.",
   "moatStrength": "NARROW"},
  "Seventeenth, Tube Investments of India — the diversifier. [pause] Part of the respected Murugappa "
  "group, it makes precision steel tubes, chains, and Hercules bicycles — and it's building an "
  "electric-vehicle arm. [pause] Its results are due on the fourteenth of August. [pause] "
  "It trades at a rich eighty-one times earnings, pricing in that growth. [pause] "
  "Its moat is quality capital allocation and a broad engineering base, with an EV option on top."),

 ("c18_atlas", "au_company",
  {"idx": "18 / 18", "kicker": "TRACTORS & LEGACY", "name": "Atlas Cycles (Haryana)", "ticker": "ATLASCYCLE",
   "price": "₹99.7", "pe": "N/A", "seg": "Legacy bicycles",
   "biz": ["Once India's largest bicycle brand",
           "Cycle operations are now largely dormant",
           "The story today is legacy real-estate assets"],
   "fin": {"qlabel": "FY26 (annual)",
           "rev": {"to": 7, "up": False},
           "pat": {"to": 8, "up": False, "loss": True, "label": "Net loss"},
           "note": "Sales collapsed to about ₹7 crore; the stock trades well below its book value."},
   "moat": "None operationally — the value case is legacy land, not the business.",
   "moatStrength": "NONE"},
  "And eighteenth, Atlas Cycles — a name from the past. [pause] Once India's biggest bicycle brand, "
  "its cycle business is now nearly dormant. [pause] Sales have collapsed to about seven crore, and "
  "it's making losses. [pause] There's no meaningful P E; the stock trades below its book value. [pause] "
  "Its moat is gone — whatever value remains is in old land and assets, not in making cycles."),

 # ---- RECAP ----
 ("s99_recap", "au_recap",
  {"title": "Vehicle Makers — in one breath", "color": BIZC,
   "items": [
     "Maruti & Hyundai: scale, service and SUVs rule the car market",
     "M&M: SUV heat plus India's tractor throne — a wide moat",
     "Hero, Bajaj, TVS: two-wheeler giants, each with its own edge",
     "Eicher: Royal Enfield — the strongest brand moat here",
     "Ather, Ola, Olectra: the electric bet — still mostly loss-making",
     "Swaraj & VST: quiet, cash-rich farm-power niches",
     "Valuations range wildly — from ~20× to over 80× earnings",
   ],
   "closer": "Moats last longer than momentum — and the price you pay still matters."},
  "So, in one breath. [pause] Maruti and Hyundai win the car market on scale and service. "
  "Mahindra pairs hot SUVs with the tractor throne. [pause] Hero, Bajaj and TVS are two-wheeler "
  "giants, each with a different edge — and Eicher's Royal Enfield is the strongest brand here. [pause] "
  "The electric names — Ather, Ola, Olectra — are growing fast but still mostly losing money. "
  "And Swaraj and V-S-T are quiet, cash-rich farm niches. [pause] "
  "Notice how far valuations range — from about twenty times earnings to over eighty. [pause] "
  "The lesson: moats last longer than momentum, and the price you pay still matters. [pause] "
  "Next time, we tackle the tyre, rubber and battery makers. Thanks for watching."),
]


def post(p, b):
    req = urllib.request.Request(BASE + p, data=json.dumps(b).encode(),
                                 headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode())


def get(p):
    with urllib.request.urlopen(BASE + p, timeout=30) as r:
        return r.read()


def tts_chunk(path, text):
    gid = post("/generate", {"profile_id": PROFILE, "text": text, "engine": "kokoro"})["id"]
    for _ in range(300):
        raw = get(f"/generate/{gid}/status").decode()
        line = [l for l in raw.splitlines() if l.startswith("data:")]
        st = json.loads(line[-1][5:].strip()) if line else None
        if st and st.get("status") == "completed":
            break
        time.sleep(1)
    open(path, "wb").write(get(f"/audio/{gid}"))


def gen_one(seg_id, text):
    fin = os.path.join(FIN, seg_id + ".wav")
    if os.path.exists(fin):
        out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                              "-of", "default=noprint_wrappers=1:nokey=1", fin],
                             capture_output=True, text=True, check=True)
        return fin, round(float(out.stdout.strip()), 3)
    chunks = [c.strip() for c in text.split("[pause]") if c.strip()]
    paths = []
    for ci, chunk in enumerate(chunks):
        cp = os.path.join(RAW, f"{seg_id}_c{ci}.wav")
        if not os.path.exists(cp):
            tts_chunk(cp, chunk)
        paths.append(cp)
    psil = os.path.join(RAW, "_pause.wav")
    if not os.path.exists(psil):
        subprocess.run(["ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=24000:cl=mono",
                        "-t", str(PAUSE), psil], check=True, capture_output=True)
    clist = os.path.join(RAW, f"{seg_id}_concat.txt")
    with open(clist, "w") as f:
        for i2, p2 in enumerate(paths):
            f.write(f"file '{p2}'\n")
            if i2 < len(paths) - 1:
                f.write(f"file '{psil}'\n")
    af = f"atempo={ATEMPO}" if ATEMPO != 1.0 else "anull"
    subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", clist,
                    "-filter:a", af, fin], check=True, capture_output=True)
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "default=noprint_wrappers=1:nokey=1", fin],
                         capture_output=True, text=True, check=True)
    return fin, round(float(out.stdout.strip()), 3)


manifest = []
for sid, variant, props, text in SEGMENTS:
    path, dur = gen_one(sid, text)
    manifest.append({"id": sid, "variant": variant, "props": props, "wav": path, "duration": dur})
    warn = "  ⚠ LONG — split (skills/03)" if dur > 90 else ""
    print(f"  {sid:14s} {dur:6.2f}s{warn}", flush=True)

silence = os.path.join(FIN, "_sil.wav")
subprocess.run(["ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=24000:cl=mono", "-t", str(GAP), silence],
               check=True, capture_output=True)
concat_list = os.path.join(ROOT, "concat.txt")
with open(concat_list, "w") as f:
    for i, m in enumerate(manifest):
        f.write(f"file '{m['wav']}'\n")
        if i < len(manifest) - 1:
            f.write(f"file '{silence}'\n")
subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_list, "-c", "copy",
                os.path.join(PUBLIC, "narration.wav")], check=True, capture_output=True)

cuts, t = [], 0.0
for m in manifest:
    start, end = t, t + m["duration"]
    cuts.append({"id": m["id"], "type": m["variant"], "in_seconds": round(start, 3),
                 "out_seconds": round(end, 3),
                 "props": {**m["props"], "dur": round(m["duration"] + GAP, 3)}})
    t = end + GAP
props = {"cuts": cuts,
         "audio": {"narration": {"src": f"{PREFIX}/narration.wav", "volume": 1.0}}}
json.dump(props, open(os.path.join(ROOT, "artifacts", "edit_decisions.json"), "w"), indent=2)
print(f"total {t - GAP:.2f}s ({(t-GAP)/60:.2f} min), {len(cuts)} scenes, NO captions, NO music")
