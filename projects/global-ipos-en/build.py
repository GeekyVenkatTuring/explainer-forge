#!/usr/bin/env python3
"""Global IPOs: US vs China — THIS WEEK (English, Nova). Prefix `gi`, scene set GIScenes.tsx.

A combined, concept/education video contrasting the two IPO markets in one week
(early August 2026). Read skills/13-intl-ipo.md. This is NOT the India `sm` track.

DATA HONESTY (skill 13 §4/§6) — figures are kept qualitative / clearly labelled because
the market-data web tools in this harness have returned fabricated-looking numbers before.
Real, well-reported ANCHORS used (names + what the companies do are stable facts):

  UNITED STATES — this week's Nasdaq slate (StockAnalysis / Yahoo IPO calendars, 3-4 Aug 2026;
    "IPO dates are estimated and may change"):
      Attovia Therapeutics (ATTO)  — immunology biotech, ~$200M range, NASDAQ
      Braveheart Bio (BRVE)        — biotech, ~$300M range, NASDAQ
      Vogenx (VOGX)                — biotech, ~$75M range, NASDAQ
      OceanLight Acquisition (OCLT)— a SPAC / blank-check, ~$100M, NASDAQ
    Profile: MANY small, market-driven deals; biotech-heavy; plus a SPAC.
  CHINA — around this week (Caixin Global / Reuters / KPMG-Deloitte reviews, late Jul-Aug 2026):
      CXMT · ChangXin Memory Technologies — DRAM memory-chip maker; listed on the Shanghai
        STAR Market; reported ~¥57.9B (≈ $8.6B) — the largest IPO in the STAR board's history.
      Zhongji Innolight — optical-module maker; multi-billion-dollar Hong Kong (HKEX) listing.
    Profile: A FEW giant, strategic (chip/hard-tech) deals; policy-aligned.

  All dollar/yuan figures are prefixed "≈/around/reportedly" and the currency + exchange is
  named every time. No listing-gain prediction. VIE / dual-class / lock-up flagged as risks.
  Education only — not investment advice (disclaimer in narration AND description).

Voice: Kokoro "Nova" (Voicebox, English). Usage: python3 build.py
"""
import json, os, subprocess, time, urllib.request

BASE = "http://127.0.0.1:17493"
PROFILE = "c488e05c-3407-46a3-874d-1b09b3aff78d"  # "TTS Bright (Nova)"
GAP = 0.5
PAUSE = 0.6
ATEMPO = 0.95
PREFIX = "gi"
ROOT = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(ROOT, "..", ".."))
PUBLIC = os.path.join(REPO, "composer", "public", PREFIX)
RAW = os.path.join(ROOT, "assets", "raw")
FIN = os.path.join(ROOT, "assets")
for d in (PUBLIC, RAW, os.path.join(ROOT, "artifacts"), os.path.join(ROOT, "renders")):
    os.makedirs(d, exist_ok=True)

US, CN, CASH, MKT, OK = "#4F86F7", "#F5546B", "#FBBF24", "#22D3EE", "#34D399"

DISCLAIMER = ("One last thing, and it matters. [pause] This video is education, not investment "
    "advice. It is not a recommendation to buy or sell anything, and nothing here predicts how "
    "any of these shares will trade. I-P-O dates and sizes are estimates that can change. Always "
    "read the official prospectus, and talk to a licensed advisor before you invest. Thanks for watching.")

# ---------------------------------------------------------------- SCREENPLAY
SEGMENTS = [

 ("gi01_title", "gi_title", {},
  "This week, dozens of companies go public. [pause] In America, a cluster of small deals. "
  "In China, one or two absolute giants. [pause] Same word — I-P-O — completely different game. "
  "Let's walk through both. This is education, not investment advice."),

 ("gi02_split", "gi_split", {
    "usItems": [
      {"name": "Attovia Therapeutics", "tag": "BIOTECH"},
      {"name": "Braveheart Bio", "tag": "BIOTECH"},
      {"name": "Vogenx", "tag": "BIOTECH"},
      {"name": "OceanLight", "tag": "SPAC"},
      {"name": "…and more small deals", "tag": "NASDAQ"},
    ],
    "cnBig": {"name": "CXMT · ChangXin Memory", "tag": "SHANGHAI · STAR", "note": "memory chips · reportedly a record-size STAR listing"},
    "cnSmall": {"name": "Zhongji Innolight", "tag": "HONG KONG"},
  },
  "Look at the same week through two windows. [pause] On the American side — a handful of small "
  "companies on the Nasdaq, mostly tiny biotechs, plus one blank-cheque deal. Each one raising "
  "a few hundred million dollars at most. [pause] On the Chinese side — far fewer names, but "
  "enormous. One memory-chip maker alone reportedly raised around eight and a half billion "
  "dollars — the biggest listing in its exchange's history. [pause] Many small versus a few "
  "giant. That single contrast tells you almost everything."),

 ("gi03_ipoflow", "gi_steps", {
    "kicker": "I-P-O IN ONE BREATH", "title": "What 'going public' actually means", "color": MKT,
    "items": [
      {"emoji": "🏢", "label": "A private company", "sub": "owned by founders & backers", "c": MKT},
      {"emoji": "📄", "label": "Files a prospectus", "sub": "opens its books to regulators", "c": MKT},
      {"emoji": "🏷️", "label": "Sets a price", "sub": "and sells new shares", "c": CASH},
      {"emoji": "🔔", "label": "Shares start trading", "sub": "anyone can now buy", "c": OK},
    ],
    "note": "An IPO simply turns a private company into one whose shares you can buy on an exchange.",
  },
  "First, the basics — quickly. [pause] A company starts out private, owned by its founders and "
  "early backers. [pause] To go public, it files a detailed document — a prospectus — that opens "
  "its books to regulators and investors. [pause] Then it sets a price and sells shares. On listing "
  "day, those shares start trading, and now anyone can buy a slice. [pause] That's the whole idea. "
  "The interesting part is how differently America and China run each of these steps."),

 ("gi04_div1", "gi_divider", {"n": 1, "title": "The American Way", "sub": "Many small deals, driven by the market", "color": US},
  "Part one. The American way. [pause] Many small deals — and it's the market, not the state, that decides them."),

 ("gi05_usslate", "gi_cards", {
    "kicker": "THIS WEEK ON THE NASDAQ", "title": "America's slate: small and biotech-heavy", "color": US,
    "items": [
      {"emoji": "🧬", "k": "Attovia Therapeutics", "v": "An immunology biotech — one of several small drug developers pricing this week", "chip": "≈ $200M"},
      {"emoji": "🧬", "k": "Braveheart Bio", "v": "Another clinical-stage biotech tapping public markets for research cash", "chip": "≈ $300M"},
      {"emoji": "🧪", "k": "Vogenx", "v": "A smaller biotech deal — the long tail of tiny US listings", "chip": "≈ $75M"},
      {"emoji": "📦", "k": "OceanLight", "v": "Not a real business yet — a SPAC, a blank-cheque shell raising cash to merge later", "chip": "SPAC"},
    ],
  },
  "Here's America's actual slate this week, on the Nasdaq. [pause] Attovia Therapeutics — an "
  "immunology biotech. Braveheart Bio — another drug developer. Vogenx — a smaller one still. "
  "[pause] Notice the pattern? Biotech, biotech, biotech. American markets fund a huge number of "
  "small, early companies — especially in drug research — each raising a few hundred million at "
  "most. [pause] And then there's OceanLight, which isn't a normal company at all. It's a SPAC. "
  "Hold that thought — we'll come back to it."),

 ("gi06_usmech", "gi_steps", {
    "kicker": "HOW A US I-P-O WORKS", "title": "File, review, sell — the book-build", "color": US,
    "items": [
      {"emoji": "📝", "label": "File an S-1", "sub": "the SEC prospectus", "c": US},
      {"emoji": "🔍", "label": "SEC review", "sub": "disclosure, back-and-forth", "c": MKT},
      {"emoji": "📣", "label": "Roadshow", "sub": "book-build a price range", "c": CASH},
      {"emoji": "🔔", "label": "List & trade", "sub": "opens at a market price", "c": OK},
    ],
    "note": "You see a price RANGE before the deal; the final price is set the night before it lists.",
  },
  "So how does an American I-P-O actually work? [pause] The company files a document called an "
  "S-one with the securities regulator, the S-E-C. The regulator reviews the disclosures, but it "
  "does not judge whether the company is a good investment. [pause] Then bankers run a roadshow — "
  "they take orders from big investors across a price range, say fifteen to seventeen dollars. "
  "That's called building the book. [pause] The final price is set the night before listing. And "
  "here's a key point for you — regular investors usually buy at the open, which can be well above "
  "that I-P-O price."),

 ("gi07_spac", "gi_spac", {},
  "Now, that blank-cheque deal — the SPAC. It's worth understanding, because they're almost uniquely "
  "American. [pause] A SPAC goes public as an empty shell. No products, no revenue — just a pile of "
  "cash and a promise. [pause] The sponsors then have around two years to find a real company and "
  "merge with it. If they succeed, that company becomes public through the back door. If they fail, "
  "the cash is returned. [pause] So when you buy a SPAC, you're not backing a business you can see. "
  "You're betting on the sponsor's ability to find one. That's a very different risk."),

 ("gi08_ustake", "gi_cards", {
    "kicker": "WHAT THE US SLATE SAYS", "title": "The American signature", "color": US,
    "items": [
      {"emoji": "🐜", "k": "Volume over size", "v": "Hundreds of small IPOs a year — the market funds lots of tiny bets", "chip": "MANY SMALL"},
      {"emoji": "🧬", "k": "Innovation-led", "v": "Biotech and tech dominate — high-risk, high-reward science", "chip": "BIOTECH"},
      {"emoji": "🕰️", "k": "Market timing", "v": "Deals cluster when appetite is high; they stall when it isn't", "chip": "MARKET-DRIVEN"},
      {"emoji": "🛒", "k": "Open access", "v": "Any brokerage account can buy once shares trade — but at the open price", "chip": "RETAIL-EASY"},
    ],
  },
  "Step back, and America's signature is clear. [pause] Volume over size — hundreds of small listings "
  "a year, the market happily funding lots of little bets. [pause] It's innovation-led, dominated by "
  "biotech and tech — high risk, high reward. [pause] And it's market-driven — deals flood in when "
  "appetite is high and dry up when it isn't. [pause] The upside for you? Access is easy. Any "
  "brokerage account can buy once a stock trades. So: many small, market-timed, easy to reach. "
  "Now let's cross the Pacific."),

 ("gi09_div2", "gi_divider", {"n": 2, "title": "The Chinese Way", "sub": "A few giant deals, aligned with the state", "color": CN},
  "Part two. The Chinese way. [pause] Fewer deals — but far bigger, and often aligned with national priorities."),

 ("gi10_cnslate", "gi_cards", {
    "kicker": "THIS WEEK IN CHINA", "title": "China's slate: fewer, but enormous", "color": CN,
    "items": [
      {"emoji": "🏭", "k": "CXMT — ChangXin Memory", "v": "A DRAM memory-chip maker; listed in Shanghai, reportedly the STAR board's largest-ever IPO", "chip": "≈ $8.6B"},
      {"emoji": "🔦", "k": "Zhongji Innolight", "v": "An optical-module giant doing a multi-billion-dollar Hong Kong listing", "chip": "HONG KONG"},
      {"emoji": "⭐", "k": "The STAR Market", "v": "Shanghai's Nasdaq-style board for hard-tech — tickers starting 688", "chip": "688xxx"},
      {"emoji": "🎯", "k": "Why so big?", "v": "These are strategic industries — chips China wants to build at home", "chip": "STRATEGIC"},
    ],
  },
  "Here's China's slate around the same week — and the scale is jarring. [pause] The headline is "
  "C-X-M-T, ChangXin Memory — a maker of D-RAM, the memory chips inside every phone and laptop. It "
  "listed in Shanghai and reportedly raised around eight and a half billion dollars — the largest "
  "I-P-O in that board's history. [pause] Alongside it, Zhongji Innolight, an optical-module maker, "
  "did a multi-billion-dollar listing in Hong Kong. [pause] Two names. Both huge. Both in chips. And "
  "that is not a coincidence — these are exactly the strategic industries China is racing to build "
  "at home."),

 ("gi11_cnvenues", "gi_compare", {
    "kicker": "WHERE CHINA LISTS", "title": "Three very different doors", "color": MKT,
    "cols": [
      {"name": "STAR Market", "color": CN, "emoji": "⭐", "hi": True, "rows": [
        {"k": "WHERE", "v": "Shanghai · tickers 688"},
        {"k": "FOR", "v": "Hard-tech: chips, biotech"},
        {"k": "FIRST 5 DAYS", "v": "No daily price limit"},
        {"k": "FOREIGNERS", "v": "Gated — via Stock Connect"},
      ]},
      {"name": "ChiNext", "color": US, "emoji": "🌱", "rows": [
        {"k": "WHERE", "v": "Shenzhen · growth firms"},
        {"k": "FOR", "v": "Younger, innovative names"},
        {"k": "FIRST 5 DAYS", "v": "No daily price limit"},
        {"k": "THEN", "v": "±20% daily band"},
      ]},
      {"name": "Hong Kong", "color": CASH, "emoji": "🇭🇰", "rows": [
        {"k": "WHERE", "v": "HKEX · global gateway"},
        {"k": "FOR", "v": "Big dual-listings"},
        {"k": "LIMITS", "v": "No daily price cap"},
        {"k": "FOREIGNERS", "v": "Open to global money"},
      ]},
    ],
  },
  "But where exactly does a Chinese company list? There are three very different doors. [pause] "
  "The STAR Market in Shanghai — think of it as China's Nasdaq for deep technology, chips and "
  "biotech, with tickers that start six-eight-eight. [pause] ChiNext in Shenzhen, aimed at younger "
  "growth companies. [pause] And Hong Kong — the global gateway, where the biggest names dual-list "
  "to reach international money. [pause] One quirk worth knowing — on the mainland boards, a new "
  "stock has no daily price limit for its first five days, so those debuts can swing violently."),

 ("gi12_cnmech", "gi_steps", {
    "kicker": "HOW A CHINA I-P-O DIFFERS", "title": "More hands on the wheel", "color": CN,
    "items": [
      {"emoji": "📄", "label": "File & register", "sub": "with the exchange", "c": CN},
      {"emoji": "🏛️", "label": "Regulator sign-off", "sub": "the CSRC's blessing", "c": MKT},
      {"emoji": "🤝", "label": "Strategic placement", "sub": "big anchors take chunks", "c": US},
      {"emoji": "🔔", "label": "List", "sub": "no price cap, first 5 days", "c": OK},
    ],
    "note": "The state and strategic investors shape the deal far more than in the US.",
  },
  "The mechanics differ too. [pause] A Chinese company files and registers with its exchange, and "
  "the national securities regulator has to sign off. Pricing comes with more guidance from above "
  "than in America. [pause] A big slice often goes to strategic investors — state-linked funds and "
  "partners who take large anchor stakes. [pause] Then it lists, with those wild, uncapped first "
  "five days on the mainland. [pause] The theme running through all of it — in China, the state and "
  "strategic players shape an I-P-O far more than the free market alone. That's the core difference."),

 ("gi13_div3", "gi_divider", {"n": 3, "title": "Same Word, Different Game", "sub": "What the contrast means for you", "color": OK},
  "Part three. Same word, different game. [pause] Let's put the two side by side — and see what it means for you."),

 ("gi14_bigcompare", "gi_compare", {
    "kicker": "US vs CHINA · THIS WEEK", "title": "The contrast in one frame", "color": OK,
    "cols": [
      {"name": "United States", "color": US, "emoji": "🇺🇸", "rows": [
        {"k": "THIS WEEK", "v": "A cluster of small deals"},
        {"k": "TYPICAL SIZE", "v": "Tens to a few hundred $M"},
        {"k": "SECTORS", "v": "Biotech, tech, a SPAC"},
        {"k": "WHAT DRIVES IT", "v": "Market appetite"},
        {"k": "WHO CAN BUY", "v": "Any broker, at the open"},
      ]},
      {"name": "China", "color": CN, "emoji": "🇨🇳", "rows": [
        {"k": "THIS WEEK", "v": "One or two giants"},
        {"k": "TYPICAL SIZE", "v": "Billions of dollars"},
        {"k": "SECTORS", "v": "Chips & hard-tech"},
        {"k": "WHAT DRIVES IT", "v": "National priorities"},
        {"k": "WHO CAN BUY", "v": "Gated; HK & ADRs open"},
      ]},
    ],
  },
  "Here's the whole story in one frame. [pause] This week, America brought a cluster of small deals; "
  "China brought one or two giants. [pause] American listings run from tens to a few hundred million "
  "dollars; Chinese ones this week were measured in billions. [pause] America's were biotech, tech, "
  "and a SPAC; China's were chips and hard-tech. [pause] America's are driven by market appetite; "
  "China's, heavily, by national priorities. [pause] And you can buy the American ones through any "
  "broker — while mainland China stays gated, reachable mainly through Hong Kong or American "
  "depositary receipts."),

 ("gi15_investor", "gi_cards", {
    "kicker": "WHAT IT MEANS FOR YOU", "title": "Reading any IPO like a pro", "color": CASH,
    "items": [
      {"emoji": "🌐", "k": "Access the giants carefully", "v": "Reach Chinese names via Hong Kong shares or US-listed ADRs — not the mainland directly", "chip": "ADRs / HK"},
      {"emoji": "⚠️", "k": "Read the structure", "v": "Watch for VIEs, dual-class voting and lock-up expiries — they change who really controls what", "chip": "RISKS"},
      {"emoji": "🔎", "k": "Go to the source", "v": "SEC EDGAR for US filings, HKEXnews for Hong Kong, and reputable outlets for the rest", "chip": "SOURCES"},
      {"emoji": "🧭", "k": "An IPO is a start", "v": "Going public is a fundraising event, not a promise of gains — judge the business, not the buzz", "chip": "MINDSET"},
    ],
  },
  "So what should you actually do with all this? [pause] If a Chinese giant tempts you, reach it the "
  "safe way — through Hong Kong shares or an American depositary receipt, an A-D-R, not the mainland "
  "directly. [pause] Always read the structure. Watch for V-I-E arrangements, super-voting founder "
  "shares, and lock-up expiries — they decide who really controls the company. [pause] Go to the "
  "source: the S-E-C's Edgar system for American filings, the Hong Kong exchange's site for its own. "
  "[pause] And remember — an I-P-O is a fundraising event, not a promise. Judge the business, never "
  "the hype."),

 ("gi16_recap", "gi_recap", {
    "title": "This week, in one breath",
    "items": [
      "US: many small IPOs — biotech-heavy, plus a SPAC",
      "China: one or two giants — chips & hard-tech",
      "US deals are market-driven; China's align with the state",
      "STAR & ChiNext have no price limit for 5 days",
      "Reach Chinese names via Hong Kong or ADRs",
      "Watch VIEs, dual-class shares & lock-ups",
    ],
    "closer": "Same word, two different games — know which one you're playing.",
  },
  "Let's bring it together. [pause] This week, America ran many small I-P-Os, heavy on biotech, plus "
  "a SPAC. China ran one or two giants, in chips and hard-tech. [pause] American deals are driven by "
  "the market; Chinese ones lean on the state. [pause] Remember the quirks — no price limit for the "
  "first five days on China's tech boards, and you reach those names through Hong Kong or A-D-Rs. "
  "[pause] And always read the structure — the V-I-Es, the voting shares, the lock-ups. " + DISCLAIMER),
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
    warn = "  ⚠ LONG — split or ensure it develops to p≈0.85" if dur > 90 else ""
    print(f"  {sid:16s} {dur:6.2f}s{warn}", flush=True)

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
