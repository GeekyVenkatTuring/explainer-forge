#!/usr/bin/env python3
"""Indian Auto Sector — Video 2: TYRES, RUBBER & BATTERIES (English, Nova).

Reuses the `au` scene set. Own narration file (au/narration2.wav) + own
edit_decisions (edit_decisions2.json) so it never collides with Video 1.
Data: research/tyres-rubber-batteries.md. Price/PE = Screener close 07-Aug-2026.
Q = Q1 FY27 (Jun-26). Amara Raja Q1 pending (~11-Aug) -> latest reported shown.
Education, not advice. Run: python3 build2.py  (Voicebox open).
"""
import json, os, subprocess, time, urllib.request

BASE = "http://127.0.0.1:17493"
PROFILE = "c488e05c-3407-46a3-874d-1b09b3aff78d"  # Nova
GAP, PAUSE, ATEMPO = 0.5, 0.6, 0.95
PREFIX = "au"
NARR = "narration2.wav"          # per-video audio file under public/au/
EDJSON = "edit_decisions2.json"
ROOT = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(ROOT, "..", ".."))
PUBLIC = os.path.join(REPO, "composer", "public", PREFIX)
RAW = os.path.join(ROOT, "assets", "raw")
FIN = os.path.join(ROOT, "assets")
for d in (PUBLIC, RAW, os.path.join(ROOT, "artifacts")):
    os.makedirs(d, exist_ok=True)

BIZC, UP, MOAT, VAL = "#38BDF8", "#34D399", "#A78BFA", "#FBBF24"

SEGMENTS = [
 ("v2_title", "au_title",
  {"kicker": "AUTO & AUTO-COMPONENTS · PART 2 OF 6", "title": "Indian Auto Stocks\nTyres, Rubber & Batteries",
   "sub": "14 companies · what they do · latest quarter · P/E · their moat"},
  "Welcome back to our tour of India's automobile sector. [pause] "
  "Part two: the companies that keep vehicles rolling and running — tyre makers, rubber "
  "and recycling firms, and the battery giants. [pause] For each, the same four things: "
  "what they do, their latest quarter, their P E, and their moat. [pause] "
  "One theme to watch this time — a spike in rubber and crude prices hammered tyre margins "
  "this quarter. [pause] Figures are approximate; verify on your terminal. Education, not advice."),

 # ---- TYRE MAKERS ----
 ("t_d1", "au_divider",
  {"part": "PART ONE", "title": "The Tyre Makers", "sub": "Where a rubber-price shock just bit hard",
   "color": BIZC, "pips": 3, "at": 1},
  "First, the tyre makers. [pause] Seven listed names — and a quarter where surging raw-material "
  "costs separated the strong franchises from the price-takers."),

 ("t01_mrf", "au_company",
  {"idx": "01 / 14", "kicker": "TYRE MAKERS", "name": "MRF", "ticker": "MRF",
   "price": "₹1,34,190", "pe": "23.0×", "seg": "All-category tyres",
   "biz": ["India's largest tyre maker — and its priciest listed share",
           "Tyres for everything from two-wheelers to aircraft",
           "Also paints, conveyor belts and toys"],
   "fin": {"qlabel": "Q1 FY27 · Jun 2026",
           "rev": {"to": 7676, "yoy": "+9%", "up": True},
           "pat": {"to": 500, "yoy": "−9%", "up": False},
           "note": "Margins held up better than peers despite the cost spike."},
   "moat": "The strongest brand in Indian tyres — scale, disciplined pricing and leadership in premium replacement.",
   "moatStrength": "WIDE"},
  "First, MRF — the giant. [pause] It's India's largest tyre maker and famously the "
  "highest-priced share on the exchange, above one lakh rupees. [pause] It makes tyres for "
  "everything, right up to aircraft. [pause] Last quarter, revenue was about seventy-six "
  "hundred crore and profit around five hundred crore — margins held up better than most. [pause] "
  "It trades near twenty-three times earnings. [pause] "
  "Its moat is brand and scale — and the pricing discipline that protects those fat margins."),

 ("t02_apollo", "au_company",
  {"idx": "02 / 14", "kicker": "TYRE MAKERS", "name": "Apollo Tyres", "ticker": "APOLLOTYRE",
   "price": "₹445", "pe": "13.2×", "seg": "India + Europe tyres",
   "biz": ["Cars, trucks, two-wheelers and farm tyres",
           "Apollo brand in India, premium Vredestein in Europe",
           "Plants across India and Europe"],
   "fin": {"qlabel": "Q1 FY27 · Jun 2026",
           "rev": {"to": 7398, "yoy": "+13%", "up": True},
           "pat": {"to": 349, "yoy": "multi-fold", "up": True},
           "note": "Profit jumped off a weak base; a new CFO takes over."},
   "moat": "A strong Indian brand plus European premium tyres (Vredestein) — the cheapest valuation of the majors.",
   "moatStrength": "WIDE"},
  "Second, Apollo Tyres — the global one. [pause] It sells the Apollo brand in India and the "
  "premium Vredestein brand in Europe, with plants on both continents. [pause] "
  "Revenue rose thirteen percent to about seventy-four hundred crore, and profit jumped "
  "many times over — though partly off a weak year-ago base. [pause] "
  "Strikingly, it's the cheapest of the majors, near thirteen times earnings. [pause] "
  "Its moat is that twin brand — mass-market India plus premium Europe."),

 ("t03_bkt", "au_company",
  {"idx": "03 / 14", "kicker": "TYRE MAKERS", "name": "Balkrishna Industries (BKT)", "ticker": "BALKRISIND",
   "price": "₹2,466", "pe": "33.9×", "seg": "Off-highway tyres",
   "biz": ["Specialist in off-highway tyres — agriculture, mining, construction",
           "Sells largely into export replacement markets abroad",
           "A niche exporter, not an on-road tyre maker"],
   "fin": {"qlabel": "Q1 FY27 · Jun 2026",
           "rev": {"to": 3455, "yoy": "+25%", "up": True},
           "pat": {"to": 451, "yoy": "+56%", "up": True},
           "note": "EBITDA margin a fat 21.5% — the star of the quarter."},
   "moat": "A low-cost specialist in a niche global market — roughly 6% of world off-highway tyres, with rich margins.",
   "moatStrength": "WIDE"},
  "Third, Balkrishna Industries — better known as B-K-T. [pause] It doesn't make road tyres; "
  "it makes giant off-highway tyres for tractors, mines and construction, sold mostly as "
  "exports. [pause] It was the star of the quarter — revenue up twenty-five percent, profit "
  "up fifty-six percent, and margins above twenty-one percent. [pause] "
  "It trades near thirty-four times earnings. [pause] "
  "Its moat is being the low-cost specialist in a niche — around six percent of the world's off-highway tyres."),

 ("t04_ceat", "au_company",
  {"idx": "04 / 14", "kicker": "TYRE MAKERS", "name": "CEAT", "ticker": "CEATLTD",
   "price": "₹3,723", "pe": "23.7×", "seg": "2W + truck-bus tyres",
   "biz": ["RPG-group tyre maker",
           "Strong in two-wheeler and truck-bus tyres",
           "OEM, replacement and exports"],
   "fin": {"qlabel": "Q1 FY27 · Jun 2026",
           "rev": {"to": 4318, "yoy": "+22%", "up": True},
           "pat": {"to": 4, "yoy": "−96%", "up": False},
           "note": "Profit crashed 96% as rubber and crude costs spiked."},
   "moat": "A solid two-wheeler and truck-bus replacement brand — but a price-taker on rubber, so margins swing hard.",
   "moatStrength": "NARROW"},
  "Fourth, CEAT — and the cost shock made visible. [pause] The RPG-group maker is strong in "
  "two-wheeler and truck tyres. [pause] Revenue actually rose twenty-two percent — but profit "
  "collapsed ninety-six percent, to just four crore, as rubber and crude prices spiked. [pause] "
  "That is the whole tyre story this quarter in one number. [pause] It trades near twenty-four "
  "times earnings. [pause] Its moat is a decent brand — but it can't set raw-material prices, so margins whip around."),

 ("t05_jk", "au_company",
  {"idx": "05 / 14", "kicker": "TYRE MAKERS", "name": "JK Tyre & Industries", "ticker": "JKTYRE",
   "price": "₹395", "pe": "15.8×", "seg": "Truck & car tyres",
   "biz": ["A pioneer of radial tyres in India",
           "Trucks, buses, cars and off-highway",
           "Plants in India and Mexico"],
   "fin": {"qlabel": "Q1 FY27 · Jun 2026",
           "rev": {"to": 3946, "yoy": "~flat", "up": False},
           "pat": {"to": 44, "yoy": "−73%", "up": False},
           "note": "Same cost squeeze — but domestic volumes still rose 25%."},
   "moat": "Strength in truck radials plus scale — but leveraged and cyclical, so profits swing with input costs.",
   "moatStrength": "NARROW"},
  "Fifth, JK Tyre — the truck-radial specialist. [pause] A radial pioneer, it's strong in "
  "truck and bus tyres, with plants in India and Mexico. [pause] Same story as CEAT: revenue "
  "roughly flat, but profit down seventy-three percent to forty-four crore. [pause] "
  "The bright spot — domestic volumes still grew twenty-five percent. [pause] "
  "It trades near sixteen times earnings. [pause] "
  "Its moat is truck-radial strength and scale — but it's leveraged, so cost spikes hurt more."),

 ("t06_goodyear", "au_company",
  {"idx": "06 / 14", "kicker": "TYRE MAKERS", "name": "Goodyear India", "ticker": "GOODYEAR",
   "price": "₹803", "pe": "24.3×", "seg": "Farm & car tyres",
   "biz": ["The Indian arm of America's Goodyear",
           "Mainly farm/tractor and passenger-car tyres",
           "OEM and replacement markets"],
   "fin": {"qlabel": "Q1 FY27 · Jun 2026",
           "rev": {"to": 616, "yoy": "+2%", "up": True},
           "pat": {"to": 10, "yoy": "−", "up": False},
           "note": "A small, steady player focused on the tractor-tyre niche."},
   "moat": "A global brand and a farm-tyre niche — but small, and licensing-linked to its US parent.",
   "moatStrength": "NARROW"},
  "Sixth, Goodyear India — the farm-tyre name. [pause] It's the Indian arm of America's "
  "Goodyear, focused on tractor and car tyres. [pause] It's small: revenue around six hundred "
  "crore, profit about ten crore. [pause] It trades near twenty-four times earnings. [pause] "
  "Its moat is the global brand and its farm-tyre niche — but it's a small, licensing-linked business."),

 ("t07_tvssri", "au_company",
  {"idx": "07 / 14", "kicker": "TYRE MAKERS", "name": "TVS Srichakra", "ticker": "TVSSRICHAK",
   "price": "₹3,965", "pe": "43.5×", "seg": "Two-wheeler tyres",
   "biz": ["TVS-group maker of two- and three-wheeler tyres",
           "Sold under the TVS Eurogrip brand",
           "Plus off-highway and specialty tyres"],
   "fin": {"qlabel": "Q1 FY27 · Jun 2026",
           "rev": {"to": 819, "yoy": "+8%", "up": True},
           "pat": {"to": 13, "yoy": "−", "up": False},
           "note": "Thin margins — the rubber cost spike bites small makers too."},
   "moat": "A focused two-wheeler-tyre brand inside the TVS ecosystem — but margin-sensitive to rubber prices.",
   "moatStrength": "NARROW"},
  "Seventh, TVS Srichakra — the two-wheeler-tyre specialist. [pause] Part of the TVS group, it "
  "makes scooter and bike tyres under the Eurogrip brand. [pause] Revenue was about eight "
  "hundred crore, but profit only thirteen crore — the cost squeeze hits small makers too. [pause] "
  "Yet it trades at a rich forty-four times earnings. [pause] "
  "Its moat is a focused brand within the TVS family — but it, too, is at the mercy of rubber prices."),

 # ---- RUBBER, RECYCLING & LEGACY ----
 ("r_d2", "au_divider",
  {"part": "PART TWO", "title": "Rubber & Recycling", "sub": "Retreading, crumb rubber and old names",
   "color": UP, "pips": 3, "at": 2},
  "Part two — rubber, recycling and a couple of legacy names. [pause] Smaller companies around "
  "the edges of the tyre world: retreading, recycling old tyres, and brands whose best days have passed."),

 ("r08_tinna", "au_company",
  {"idx": "08 / 14", "kicker": "RUBBER & RECYCLING", "name": "Tinna Rubber & Infrastructure", "ticker": "TINNARUBR",
   "price": "₹1,108", "pe": "32.4×", "seg": "Tyre recycling",
   "biz": ["Recycles end-of-life tyres into crumb rubber",
           "Makes crumb-rubber-modified bitumen for roads",
           "A play on sustainability and the circular economy"],
   "fin": {"qlabel": "Q1 FY27 · Jun 2026",
           "rev": {"to": 156, "yoy": "+20%", "up": True},
           "pat": {"to": 21, "yoy": "+15%", "up": True},
           "note": "Small but profitable, riding an ESG and road-building tailwind."},
   "moat": "A first-mover leader in the growing tyre-recycling niche — scale plus a sustainability tailwind.",
   "moatStrength": "EMERGING"},
  "Eighth, Tinna Rubber — the recycler. [pause] It turns old, end-of-life tyres into crumb "
  "rubber, and modified bitumen for roads. [pause] It's small but nicely profitable — revenue "
  "up twenty percent to about a hundred fifty crore, profit around twenty crore. [pause] "
  "It trades near thirty-two times earnings. [pause] "
  "Its moat is emerging — a first-mover in tyre recycling, with a real sustainability tailwind behind it."),

 ("r09_elgi", "au_company",
  {"idx": "09 / 14", "kicker": "RUBBER & RECYCLING", "name": "Elgi Rubber", "ticker": "ELGIRUBCO",
   "price": "₹63.0", "pe": "N/A", "seg": "Retreading materials",
   "biz": ["Tyre-retreading materials and rubber machinery",
           "Reclaimed rubber and rubber products",
           "Operates across the global retreading chain"],
   "fin": {"qlabel": "Latest reported · Jun 2025",
           "rev": {"to": 86, "up": False},
           "pat": {"to": 2, "up": False, "loss": True, "label": "Net loss"},
           "note": "Sub-scale and periodically loss-making."},
   "moat": "A niche in retreading and rubber recycling — but sub-scale and often unprofitable.",
   "moatStrength": "WEAK"},
  "Ninth, Elgi Rubber — a niche within a niche. [pause] It makes retreading materials and "
  "rubber machinery — the business of giving worn tyres a second life. [pause] But it's "
  "sub-scale, with revenue under a hundred crore and small losses. [pause] "
  "There's no meaningful P E. [pause] "
  "Its moat is weak — a genuine niche, but too small and too cyclical to earn steadily."),

 ("r10_tolins", "au_company",
  {"idx": "10 / 14", "kicker": "RUBBER & RECYCLING", "name": "Tolins Tyres", "ticker": "TOLINS",
   "price": "₹102", "pe": "26.8×", "seg": "Tyres & retread rubber",
   "biz": ["A Kerala-based maker of tyres and tubes",
           "Plus precured tread rubber and compounds",
           "Sells in domestic and export markets"],
   "fin": {"qlabel": "Latest reported · Mar 2026",
           "rev": {"to": 46, "yoy": "", "up": True},
           "pat": {"to": 3, "yoy": "", "up": True},
           "note": "A small, recently-listed regional player."},
   "moat": "A small regional maker across the tyre and retread chain — limited scale, limited edge.",
   "moatStrength": "WEAK"},
  "Tenth, Tolins Tyres — a small newcomer. [pause] This Kerala company makes tyres, tubes and "
  "retreading rubber. [pause] It's tiny — revenue around forty-five crore, profit under three "
  "crore. [pause] It trades near twenty-seven times earnings. [pause] "
  "Its moat is limited — a small regional player without the scale of the majors."),

 ("r11_modi", "au_company",
  {"idx": "11 / 14", "kicker": "RUBBER & RECYCLING", "name": "Modi Rubber", "ticker": "MODIRUBBER",
   "price": "₹126", "pe": "n.m.", "seg": "Legacy tyre brand",
   "biz": ["Once a well-known tyre brand under the Modi group",
           "Core tyre operations have shrunk sharply",
           "Now largely investment and asset interests"],
   "fin": {"qlabel": "Latest reported · Mar 2026",
           "rev": {"to": 12, "up": False},
           "pat": {"to": 14, "up": False, "loss": True, "label": "Net loss"},
           "note": "The tyre business is a shadow of its past; recent quarter in the red."},
   "moat": "None operationally — whatever value exists is in legacy assets and investments, not tyres.",
   "moatStrength": "NONE"},
  "Eleventh, Modi Rubber — a name from tyre history. [pause] Once a well-known brand, its tyre "
  "business has all but faded, and it now sits on investments and assets. [pause] "
  "Revenue is just twelve crore, and it's loss-making. [pause] The P E isn't meaningful. [pause] "
  "Its moat is gone — this is an asset story, not a tyre business."),

 ("r12_ptl", "au_company",
  {"idx": "12 / 14", "kicker": "RUBBER & RECYCLING", "name": "PTL Enterprises", "ticker": "PTL",
   "price": "₹39.8", "pe": "11.6×", "seg": "Lease income + health",
   "biz": ["Owns the Kerala tyre plant leased to Apollo Tyres",
           "Earns steady lease income from it",
           "Also has healthcare interests via Artemis"],
   "fin": {"qlabel": "Q1 FY27 · Jun 2026",
           "pat": {"to": 9, "yoy": "", "up": True, "label": "Net profit"},
           "note": ""},
   "moat": "Stable, annuity-style lease income — low risk, but a holding-type entity tied to the Apollo promoter group.",
   "moatStrength": "NARROW"},
  "Twelfth, PTL Enterprises — the quiet landlord. [pause] It owns a tyre plant that it leases "
  "to Apollo Tyres, earning steady rent, and it has healthcare interests through Artemis. [pause] "
  "Its June-quarter profit was about nine crore. [pause] It trades cheaply, near twelve times "
  "earnings. [pause] "
  "Its moat is that annuity-like lease income — safe and predictable, but it's really a holding company."),

 # ---- BATTERIES ----
 ("b_d3", "au_divider",
  {"part": "PART THREE", "title": "The Battery Duopoly", "sub": "Exide vs Amara Raja — and the lithium bet",
   "color": VAL, "pips": 3, "at": 3},
  "And part three — the batteries. [pause] Two companies split almost the entire market between "
  "them. Both are now racing to build lithium cells for the electric age."),

 ("b13_exide", "au_company",
  {"idx": "13 / 14", "kicker": "BATTERIES", "name": "Exide Industries", "ticker": "EXIDEIND",
   "price": "₹490", "pe": "44.4×", "seg": "Batteries + lithium",
   "biz": ["India's largest lead-acid battery maker",
           "Car, two-wheeler, inverter and industrial batteries",
           "Building a lithium-ion cell gigafactory for EVs"],
   "fin": {"qlabel": "Q1 FY27 · Jun 2026 (consolidated)",
           "rev": {"to": 5528, "yoy": "+18%", "up": True},
           "pat": {"to": 351, "yoy": "+28%", "up": True},
           "note": "A solid quarter; margins expanding as it invests in lithium."},
   "moat": "Number one in a battery duopoly — brand, nationwide distribution and steady replacement demand, plus a lithium bet.",
   "moatStrength": "WIDE"},
  "Thirteenth, Exide Industries — the battery leader. [pause] It's India's largest maker of "
  "lead-acid batteries, for cars, inverters and industry, and it's building a lithium-cell "
  "gigafactory for the EV era. [pause] A solid quarter — revenue up eighteen percent to about "
  "fifty-five hundred crore, profit up twenty-eight percent. [pause] It trades near forty-four "
  "times earnings. [pause] "
  "Its moat is wide — one of just two players, with brand, distribution and steady replacement demand."),

 ("b14_amararaja", "au_company",
  {"idx": "14 / 14", "kicker": "BATTERIES", "name": "Amara Raja Energy & Mobility", "ticker": "ARE&M",
   "price": "₹932", "pe": "26.6×", "seg": "Batteries + new energy",
   "biz": ["The Amaron and PowerZone battery maker",
           "The number two in the lead-acid duopoly",
           "Pushing into lithium cells, chargers and EV packs"],
   "fin": {"pending": True, "qlabel": "Latest reported · Q4 FY26 (Mar-26)",
           "rev": {"to": 3460, "yoy": "+6%", "up": True},
           "pat": {"to": 322, "yoy": "+93%", "up": True},
           "note": "Q1 FY27 lands around 11-Aug; figures shown are the prior quarter."},
   "moat": "The strong number two in the battery duopoly — Amaron brand and distribution, plus a new-energy push.",
   "moatStrength": "WIDE"},
  "And fourteenth, Amara Raja Energy and Mobility — the challenger. [pause] Maker of the Amaron "
  "batteries you see everywhere, it's the clear number two, and it's investing in lithium cells "
  "and EV packs. [pause] Its new quarter is due around the eleventh of August, so I'm showing the "
  "last one — about thirty-four hundred crore of revenue. [pause] It trades near twenty-seven times "
  "earnings, cheaper than Exide. [pause] "
  "Its moat is being the strong second in a two-player market, with a trusted brand and its own new-energy bet."),

 # ---- RECAP ----
 ("v2_recap", "au_recap",
  {"title": "Tyres, Rubber & Batteries — in one breath", "color": BIZC,
   "items": [
     "A rubber & crude cost spike crushed tyre profits this quarter",
     "CEAT −96% and JK Tyre −73% — margins are the whole story",
     "MRF and Apollo, the strongest brands, held up best",
     "Balkrishna (BKT) shone — a niche off-highway export moat",
     "Tinna recycles tyres; the legacy names have faded",
     "Exide & Amara Raja: a two-player battery market, now betting on lithium",
     "Watch input costs — they decide tyre earnings quarter to quarter",
   ],
   "closer": "In tyres, brand and cost control are everything — and in batteries, it's a cosy club of two."},
  "So, in one breath. [pause] A spike in rubber and crude costs crushed tyre profits — CEAT down "
  "ninety-six percent, JK Tyre down seventy-three. Margins were the whole story. [pause] "
  "The strongest brands, MRF and Apollo, held up best, and Balkrishna shone with its niche "
  "off-highway export moat. [pause] Around the edges, Tinna recycles old tyres, while the legacy "
  "names have faded. [pause] And in batteries, Exide and Amara Raja quietly split the market — now "
  "both betting on lithium. [pause] "
  "The lesson: in tyres, brand and cost control are everything — and batteries are a cosy club of two. [pause] "
  "Next time, the engine and powertrain makers. Thanks for watching."),
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
    print(f"  {sid:14s} {dur:6.2f}s", flush=True)

silence = os.path.join(FIN, "_sil.wav")
subprocess.run(["ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=24000:cl=mono", "-t", str(GAP), silence],
               check=True, capture_output=True)
concat_list = os.path.join(ROOT, "concat2.txt")
with open(concat_list, "w") as f:
    for i, m in enumerate(manifest):
        f.write(f"file '{m['wav']}'\n")
        if i < len(manifest) - 1:
            f.write(f"file '{silence}'\n")
subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_list, "-c", "copy",
                os.path.join(PUBLIC, NARR)], check=True, capture_output=True)

cuts, t = [], 0.0
for m in manifest:
    start, end = t, t + m["duration"]
    cuts.append({"id": m["id"], "type": m["variant"], "in_seconds": round(start, 3),
                 "out_seconds": round(end, 3),
                 "props": {**m["props"], "dur": round(m["duration"] + GAP, 3)}})
    t = end + GAP
props = {"cuts": cuts, "audio": {"narration": {"src": f"{PREFIX}/{NARR}", "volume": 1.0}}}
json.dump(props, open(os.path.join(ROOT, "artifacts", EDJSON), "w"), indent=2)
print(f"total {t - GAP:.2f}s ({(t-GAP)/60:.2f} min), {len(cuts)} scenes")
