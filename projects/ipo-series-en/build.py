#!/usr/bin/env python3
"""IPO Analysis series (ENGLISH). Reuses `sm` scene set. One chapter = one video.
Data from DRHP/RHP-based public reporting (Business Standard, Business Today, Outlook Money,
IPO Watch, Chittorgarh, InvestorGain, Groww, IPOJi, tradebrains, autocarpro). GMP is UNOFFICIAL.

BATCH 1 (23 Jul 2026): indomim | lohia | xtranet | cube
BATCH 2 (30 Jul 2026 — 4 mainboard issues open this week; figures triangulated 30 Jul 2026):
  manipal   — Manipal Health, ₹9,275 Cr, 29-31 Jul. FY26 rev ₹10,520.52 Cr / PAT ₹916.52 Cr
              [BusinessToday, Medical Buyer]. Fresh ₹8,000 Cr + OFS 2.16 Cr sh (~₹1,275 Cr) = ₹9,275 Cr.
              Use: ₹5,378 Cr repay Manipal Hospitals debt + ₹574 Cr Sahyadri minority stake + GCP.
              Lot 25 / min ₹14,750 / band ₹560-590 / ~₹77,600 Cr val (~85x) / GMP ~₹6 (~1%, modest).
  juniper   — Juniper Green Energy, ₹1,800 Cr, 30 Jul-3 Aug. 100% FRESH. FY26 rev ₹804.93 Cr
              (₹424.45→₹569.78→₹804.93 FY24-26) / PAT ₹40.46 Cr (+11%, from ₹36.48) / net worth ₹122.89 Cr
              [Outlook Money, IPOJi]. Use: ₹683.24 Cr repay own borrowings + ₹728.69 Cr subsidiary debt
              (~₹1,412 Cr / 78% to debt) + GCP. Lot 66 / min ₹14,850 / band ₹214-225 / GMP ₹17 (~7.6%).
  mvelectro — MV Electrosystems, ₹290 Cr, 30 Jul-3 Aug. 100% FRESH. FY26 rev ₹49.79 Cr (fell from
              ₹64.64 Cr) / NET LOSS ₹12.63 Cr (from ₹1.40 Cr profit) [tradebrains, IPOJi]. Order book
              ₹921.64 Cr executable; Indian Railways = 76.72% of FY26 rev. Use: ~₹180 Cr WC + ~₹21 Cr
              R&D + GCP. Lot 34 / min ₹14,450 / band ₹400-425.
  ardee     — Ardee Industries, ₹425.87 Cr, 5-7 Aug. Fresh ₹320 Cr + OFS ₹105.87 Cr (75/25). FY26
              rev ₹1,167.65 Cr (+57%) / PAT ₹84.68 Cr (+155%, from ₹33.3) [HDFCSky, Business Standard,
              IPOJi]. Use: ₹220 Cr WC + ₹20 Cr debt + GCP. Lot 281 / min ₹14,893 / band ₹50-53 / GMP ₹13 (~24.5%).
BATCH 3 (4 Aug 2026 — 2 new mainboard issues opening 7 Aug, not yet covered; figures per RHP-based reporting
  Business Standard / BusinessToday / IPOJi / Chittorgarh, dated 3-4 Aug 2026):
  technocraft — Technocraft Ventures, ₹251.88 Cr, 7-11 Aug (lists 14 Aug). Govt EPC (water/waste-water, roads,
              urban infra, power distribution, trenchless) for UP/Uttarakhand/Rajasthan/Delhi; founded 1998.
              Revenue FY24-26: ₹227.30 → ₹281.00 → ₹347.00 Cr; PAT ₹19.05 → ₹28.20 → ₹43.32 Cr (+53.6% FY26).
              Borrowings low ~₹89.76 Cr. Order book ₹1,320.70 Cr (15 Jul 2026, ~3.8x rev). Post-issue P/E 19.38.
              Fresh ₹201.51 Cr (95,05,000 sh) + OFS ₹50.37 Cr (23,76,000 sh) = ₹251.88 Cr -> ~80% FRESH / 20% OFS.
              Promoter Kartikey Constructions (Tyagi family). Use: working capital + GCP. Band ₹200-212 / lot 70 /
              min ₹14,840 / GMP ~₹16.50 (~7.78% over ₹212, UNOFFICIAL, as of 3 Aug).
  leap        — LEAP India, ₹2,480 Cr, 7-11 Aug (anchor 6 Aug, lists 14 Aug). Supply-chain asset pooling (rents
              pallets/crates/containers to FMCG/logistics/e-comm/industrial); India's largest on-demand pooling co;
              KKR majority since 2023. Revenue FY24-26: ₹371.94 → ₹485.03 → ₹747.36 Cr; PAT ₹37.17 → ₹37.56 →
              ₹62.34 Cr. Net worth ₹714.18 -> ₹1,006.33 Cr. Borrowings DOUBLED ₹513.07 -> ₹1,017.73 Cr. P/B 6.48,
              mcap ~₹7,000 Cr => ~112x FY26 PAT (COMPUTED estimate; label as est). Fresh ₹480 Cr + OFS ₹2,000 Cr =
              ₹2,480 Cr -> only 19% FRESH / 81% OFS (to sellers incl KKR). Use: ₹360 Cr debt repay + GCP.
              Band ₹151-159 / lot 94 / min ₹14,946. No official GMP cited. Watch-outs: mostly-OFS, high debt, rich value.
BATCH 4 — SME IPOs opening this week (4 Aug 2026; figures per Chittorgarh/IPO Watch/IPOJi/Groww/Business
  Standard/Whalesbook RHP-based reporting, dated 3-4 Aug 2026). SME = separate NSE Emerge / BSE SME platform,
  LARGE minimum bid (~₹1-2.5 lakh), thin liquidity, lighter disclosure. GMP UNOFFICIAL.
  anawil     — Anawil Wire & Engineering (NSE SME), ₹177.81 Cr, 3-5 Aug. Transmission/telecom TOWER mfg &
               fabrication (~99.95% of FY25 rev = towers). Rev FY24-26 ₹54.07 → ₹78.59 → ₹143.27 Cr; PAT
               ₹4.39 → ₹12.30 → ₹36.63 Cr (+82% rev, +198% PAT FY26). Fresh ₹142.69 Cr (~80%) + OFS ₹35.12 Cr.
               Band ₹257-270 / lot 400 (~₹1.08 L). Use: repay debt + GCP. GMP ~21%.
  aegeus     — Aegeus Technologies (BSE SME), ₹23.71 Cr, 4-6 Aug. Solar-panel CLEANING ROBOTS (Unicorn ground-
               mount, Shreem rooftop); FY26 product 55% / maintenance 45%. Total income FY25→26 ₹21.90 → ₹41.22 Cr
               (+88%); PAT ₹1.39 → ₹4.02 Cr (~3x). 100% FRESH. Band ₹100-105 / lot 1,200 / min 2 lots ₹2,52,000.
               Use: product dev + new plant capex + WC + GCP.
  lapl       — LAPL Automotive (BSE SME), ₹32.40 Cr, 6-10 Aug. Auto components — lighting & mirrors; ODM 78% /
               OBM 22% (FY26). Rev FY25→26 ₹66.00 → ₹93.30 Cr (+41.3%); PAT ₹5.03 → ₹8.60 Cr (+71.4%). 100% FRESH
               (34.46 L sh; ₹2 Cr market-maker reserved). Band ₹88-94 / lot 1,200 / min 2 lots ₹2,25,600. Use:
               ₹19.56 Cr new plant + ₹4.8 Cr debt + GCP. GMP ~18%.
  optimystix — Optimystix Entertainment (NSE SME), ₹107.88 Cr, 7-11 Aug. TV/content producer (Comedy Circus,
               Crime Patrol; 150+ shows, 7,500+ hrs); promoters Vipul D. Shah & Rajesh Bahl; first IPO. Rev FY25→26
               ₹125.07 → ₹135.89 Cr (+8.6%); PAT ₹17.24 → ₹24.04 Cr (+39%). Fresh 50 L sh (~₹87 Cr, ~81%) + OFS
               12 L sh (~₹20.88 Cr). Post value ~₹405 Cr => ~16.8x P/E (COMPUTED est). Band ₹165-174 / lot TBA
               (~₹1 L+). Use: ₹55.88 Cr working capital + GCP. GMP not started at open.
  NOTE: SME per-stock closes/mins triangulated across aggregators; where a lot/min was unconfirmed (Optimystix
  lot) it is framed qualitatively (~₹1 L+). Optimystix P/E is COMPUTED (label as est).

Each video: title -> what the company does -> financials -> issue structure (FRESH vs OFS: is the
money going INTO the company or to selling promoters?) -> use of proceeds -> should-you-subscribe
(strengths vs watch-outs) -> Retail vs HNI + how much money + where to check subscription -> recap.
Education, NOT investment advice.

Usage: python3 build.py                 (all chapters)
       python3 build.py manipal juniper mvelectro ardee   (batch 2 only)
"""
import json, os, re, subprocess, sys, time

VOICE = "en-IN-NeerjaNeural"; RATE = "-4%"; GAP = 0.5; PAUSE = 0.55; PREFIX = "sm"
ROOT = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(ROOT, "..", ".."))
PUBLIC = os.path.join(REPO, "composer", "public", PREFIX); RAW = os.path.join(ROOT, "assets", "raw"); FIN = os.path.join(ROOT, "assets")
for d in (PUBLIC, RAW, os.path.join(ROOT, "artifacts"), os.path.join(ROOT, "renders")):
    os.makedirs(d, exist_ok=True)

# ---- shared education blurbs (per-IPO min amount injected) --------------------------------------
def retail_hni_items(retail_min, hni_extra=""):
    return [
        {"emoji": "🧑", "k": "Retail (RII) — up to ₹2 lakh", "v": "35% quota. If oversubscribed, shares are allotted by LOTTERY — a bigger cheque does NOT get you more", "chip": "LOTTERY"},
        {"emoji": "💼", "k": "HNI (NII) — above ₹2 lakh", "v": "15% quota. Split into S-HNI (₹2–10 L) and B-HNI (over ₹10 L); allotment is proportionate", "chip": "> ₹2 LAKH"},
        {"emoji": "💰", "k": "Money you need", "v": f"Minimum 1 lot = {retail_min} as a retail bid. {hni_extra}To apply as an HNI you need more than ₹2 lakh", "chip": "MIN BID"},
        {"emoji": "🔎", "k": "Check subscription LIVE", "v": "NSE & BSE IPO pages, Chittorgarh, Moneycontrol, or your broker app (Zerodha / Groww / Angel One)", "chip": "SOURCES"},
    ]

DISCLAIMER = ("This video explains the IPO for education only — it is not investment advice, not a "
    "buy or sell recommendation, and not a prediction of listing gains. Grey-market premium is unofficial "
    "and changes hourly. Always read the RHP and check the live subscription before you apply. Thanks for watching.")

# ---- per-IPO configuration ---------------------------------------------------------------------
IPOS = {
"indomim": {
  "accent": "#22D3EE", "name": "Indo-MIM IPO", "kicker": "IPO ANALYSIS · MAINBOARD",
  "sub": "Precision metal parts · ₹3,811 Cr · Opens 23–27 Jul 2026",
  "n_title": ("Let's break down the Indo-MIM I-P-O — one of the biggest of this season, at three thousand "
    "eight hundred and eleven crore rupees. [pause] By the end of this video you'll understand what the company "
    "does, its financials, where the money is actually going, and how much you'd need to apply — as a retail or "
    "an H-N-I investor. [pause] Quick note — this is education, not investment advice, and not a tip to buy."),
  "biz": {"kicker":"WHAT THE COMPANY DOES","title":"Inside Indo-MIM","color":"#22D3EE","items":[
    {"emoji":"⚙️","k":"Metal Injection Molding (MIM)","v":"A world leader in tiny, complex, high-precision metal parts made at scale — founded back in 1996","chip":"GLOBAL LEADER"},
    {"emoji":"🚗","k":"Who buys from them","v":"Automotive, defence, medical, aerospace and consumer companies — diversified, sticky customers","chip":"5 SECTORS"},
    {"emoji":"🖨️","k":"Beyond MIM","v":"Also does investment casting, precision machining and even 3D metal printing — a full-stack parts maker","chip":"TECH EDGE"},
  ]},
  "n_biz": ("So what does Indo-MIM actually do? [pause] It's a world leader in something called Metal Injection Molding, "
    "or M-I-M — a way of mass-producing very small, very complex metal parts to extremely fine tolerances. Think of parts "
    "you'd find inside a car, a medical device, or a defence system. [pause] Its customers span five sectors — automotive, "
    "defence, medical, aerospace and consumer — so it isn't dependent on any single industry. [pause] And beyond M-I-M it also "
    "does investment casting, precision machining, and 3D metal printing. In short, a diversified, technology-led parts maker."),
  "fin": {"kicker":"FY26 FINANCIALS","title":"The Numbers","stats":[
    {"label":"Revenue FY26","to":4193,"prefix":"₹","suffix":" Cr","color":"#34D399","sub":"+26% YoY — strong growth"},
    {"label":"Net Profit FY26","to":534,"prefix":"₹","suffix":" Cr","color":"#34D399","sub":"+26% YoY — highly profitable"},
    {"label":"Grey-mkt premium","to":39,"prefix":"~","suffix":"%","color":"#FBBF24","sub":"unofficial · over ₹485 cap"}],
    "note":"A genuinely profitable, growing business — revenue and profit both up 26%. The grey market is signalling a strong listing, but GMP is unofficial and drifts daily."},
  "n_fin": ("Now the financials — and they're strong. [pause] In the year ended March twenty twenty-six, Indo-MIM did "
    "four thousand one hundred and ninety-three crore in revenue, up twenty-six percent. Net profit was five hundred and "
    "thirty-four crore, also up twenty-six percent. [pause] So this is a real, profitable, fast-growing company — not a loss-maker "
    "chasing a listing. The grey market premium is around thirty-nine percent, hinting at a strong debut — but remember, that number "
    "is unofficial and changes every day."),
  "issue": {"kicker":"WHERE THE MONEY GOES","title":"Fresh Issue vs Offer-for-Sale","stats":[
    {"label":"Total issue","to":3811,"prefix":"₹","suffix":" Cr","color":"#22D3EE","sub":"price band ₹461–485"},
    {"label":"Fresh (into company)","to":500,"prefix":"₹","suffix":" Cr","color":"#34D399","sub":"just 13% of the issue"},
    {"label":"OFS (to sellers)","to":3312,"prefix":"₹","suffix":" Cr","color":"#F87171","sub":"87% — existing owners exit"}],
    "note":"KEY POINT: 87% is an Offer-for-Sale — that money goes to existing shareholders cashing out (incl. Green Meadows and IIT Madras), NOT into the business."},
  "n_issue": ("Here's the most important part for any I-P-O — where does your money actually go? [pause] Of the three thousand "
    "eight hundred and eleven crore, only five hundred crore is a fresh issue — new money that goes into the company. That's just "
    "thirteen percent. [pause] The other three thousand three hundred and twelve crore — eighty-seven percent — is an Offer for Sale. "
    "That means existing shareholders, including a big investor called Green Meadows and even I-I-T Madras, are selling their stakes and "
    "pocketing that cash. [pause] So when you apply, most of your money is buying out people who are exiting — not funding the company's growth."),
  "proceeds": {"kicker":"USE OF THE FRESH MONEY","title":"What the ₹500 Cr Funds","color":"#22D3EE","items":[
    {"emoji":"🏦","k":"₹400 Cr — repay debt","v":"The bulk of the fresh money simply pays down existing borrowings — it strengthens the balance sheet, but doesn't build new capacity","chip":"DEBT"},
    {"emoji":"🧰","k":"Balance — general corporate","v":"The rest goes to general corporate purposes, the standard catch-all bucket","chip":"GCP"},
  ]},
  "n_proceeds": ("And that small fresh-issue slice — the five hundred crore — what does it fund? [pause] Four hundred crore of it "
    "just repays existing debt. That's not a bad thing — it cuts interest costs and de-risks the balance sheet — but it does not add "
    "new factories or capacity. [pause] The remainder goes to general corporate purposes, the usual catch-all. So the fresh money "
    "cleans up the balance sheet rather than fuelling expansion."),
  "verdict": {"kicker":"SHOULD YOU SUBSCRIBE?","title":"Strengths vs Watch-outs","mythLabel":"⚠️ WATCH-OUTS","factLabel":"✅ STRENGTHS","pairs":[
    {"m":"87% is OFS — mostly a promoter/investor exit","f":"Profitable, 26% revenue & profit growth"},
    {"m":"Fresh money repays debt, not growth capex","f":"Global leader in a niche, sticky business"},
    {"m":"Premium valuation; GMP can fade by listing","f":"~39% grey-market premium — strong demand"}],
  },
  "n_verdict": ("So — should you subscribe? Let's weigh it honestly. [pause] On the strengths side — it's a genuinely profitable "
    "business growing at twenty-six percent, a global leader in a niche with sticky customers, and the grey market is pricing a strong "
    "listing near thirty-nine percent. [pause] On the watch-out side — eighty-seven percent of the issue is existing owners cashing out, "
    "the fresh money only repays debt rather than funding growth, and the valuation is rich, so that grey-market premium can shrink by "
    "listing day. [pause] The takeaway — a high-quality company, but go in understanding you're mostly buying shares from sellers, not "
    "funding expansion."),
  "retail_min":"₹14,550", "hni_extra":"Retail can bid up to 13 lots, about ₹1.9 lakh. ",
  "n_retail": ("Finally — how do you actually apply, and how much do you need? [pause] As a retail investor you can put in up to "
    "two lakh rupees, and you get thirty-five percent of the issue. But if it's oversubscribed, shares are given out by lottery — so a "
    "bigger cheque does not get you more. [pause] H-N-Is bid above two lakh and share a fifteen percent quota. [pause] For Indo-MIM, one "
    "lot is thirty shares — about fourteen thousand five hundred and fifty rupees — and that's your minimum. [pause] To watch the "
    "subscription build up live, use the N-S-E and B-S-E I-P-O pages, Chittorgarh, Moneycontrol, or your broker app."),
  "recap": {"title":"Indo-MIM IPO — at a Glance","items":[
    "Business: global metal-injection-molding parts leader","FY26: revenue ₹4,193 Cr, profit ₹534 Cr (both +26%)",
    "₹3,811 Cr issue — but 87% is OFS (owners exiting)","Fresh ₹500 Cr mainly repays debt","Retail min ~₹14,550 · GMP ~39% (unofficial)"],
    "closer":"A quality company at a full price — mostly a sell-down. Read the RHP; decide for yourself."},
  "n_recap_pre": ("Let's recap Indo-MIM. [pause] A world-leading metal-parts maker, genuinely profitable with revenue and profit both "
    "up twenty-six percent. [pause] The issue is big at three thousand eight hundred crore — but eighty-seven percent is existing owners "
    "selling, and the fresh money mostly repays debt. [pause] Retail minimum is about fourteen thousand five hundred and fifty rupees, "
    "and the grey market premium is near thirty-nine percent, though that's unofficial. [pause] "),
},

"lohia": {
  "accent": "#FBBF24", "name": "Lohia Corp IPO", "kicker": "IPO ANALYSIS · MAINBOARD",
  "sub": "Industrial machinery · ₹1,102 Cr · 100% OFS · 23–27 Jul 2026",
  "n_title": ("Let's analyse the Lohia Corp I-P-O — a one thousand one hundred and two crore issue from an industrial "
    "machinery maker. [pause] There's one feature of this I-P-O that every investor must understand before applying, and we'll get "
    "to it. We'll cover the business, the financials, where the money goes, and how much you need to apply. [pause] This is education, "
    "not investment advice."),
  "biz": {"kicker":"WHAT THE COMPANY DOES","title":"Inside Lohia Corp","color":"#FBBF24","items":[
    {"emoji":"🏭","k":"Industrial machinery maker","v":"Builds the heavy machines that produce woven plastics and flexible packaging — an engineering business","chip":"MACHINERY"},
    {"emoji":"🌍","k":"Global supplier","v":"Sells its technical-textile and packaging machinery to manufacturers around the world","chip":"EXPORTS"},
    {"emoji":"🔧","k":"Niche & specialised","v":"A leader in its narrow segment — high engineering barriers keep competition limited","chip":"NICHE LEADER"},
  ]},
  "n_biz": ("So what does Lohia Corp do? [pause] It's an industrial machinery company — it builds the large, specialised machines "
    "that other factories use to make woven plastics, flexible packaging and technical textiles. [pause] It's a global supplier, "
    "exporting this equipment to manufacturers worldwide. [pause] It operates in a narrow, highly-engineered niche where the technical "
    "barriers are high, so it faces limited competition. A quiet, specialised, business-to-business leader."),
  "fin": {"kicker":"FY26 FINANCIALS","title":"The Numbers","stats":[
    {"label":"Revenue FY26","to":1717,"prefix":"₹","suffix":" Cr","color":"#34D399","sub":"+25% YoY"},
    {"label":"Net Profit FY26","to":193,"prefix":"₹","suffix":" Cr","color":"#34D399","sub":"+64% YoY — sharp jump"},
    {"label":"Valuation","to":4500,"prefix":"~₹","suffix":" Cr","color":"#FBBF24","sub":"at the ₹425 upper band"}],
    "note":"Financially strong — revenue up 25% and profit up a sharp 64%. The company is valued near ₹4,500 crore at the top of the band."},
  "n_fin": ("The financials are strong. [pause] Revenue for the year ended March twenty twenty-six was one thousand seven hundred "
    "and seventeen crore, up twenty-five percent. And net profit jumped sixty-four percent to one hundred and ninety-three crore — a "
    "sharp rise. [pause] At the top of the price band, the company is valued at around four and a half thousand crore. So on the numbers "
    "alone, this is a healthy, growing business."),
  "issue": {"kicker":"WHERE THE MONEY GOES","title":"Fresh Issue vs Offer-for-Sale","stats":[
    {"label":"Total issue","to":1102,"prefix":"₹","suffix":" Cr","color":"#FBBF24","sub":"price band ₹404–425"},
    {"label":"Fresh (into company)","to":0,"prefix":"₹","suffix":" Cr","color":"#F87171","sub":"ZERO — no fresh issue"},
    {"label":"OFS (to sellers)","to":1102,"prefix":"₹","suffix":" Cr","color":"#F87171","sub":"100% — promoters cash out"}],
    "note":"CRITICAL: this is a 100% Offer-for-Sale. The company receives NOTHING. Every rupee goes to the promoters selling their shares."},
  "n_issue": ("Now, the single most important feature of this I-P-O — the one I promised. [pause] This is a one hundred percent "
    "Offer for Sale. There is zero fresh issue. [pause] That means the company itself receives absolutely nothing from this I-P-O. "
    "Every single rupee you invest goes straight to the promoters who are selling their shares. [pause] The business gets no new money "
    "for factories, no debt repayment, no working capital — nothing. You are simply buying the promoters' stake from them at the "
    "I-P-O price."),
  "proceeds": {"kicker":"USE OF PROCEEDS","title":"What the Money Funds","color":"#FBBF24","items":[
    {"emoji":"🚫","k":"Nothing for the company","v":"Because there's no fresh issue, none of the money funds capacity, R&D, debt repayment or working capital","chip":"₹0 TO FIRM"},
    {"emoji":"👤","k":"100% to selling promoters","v":"The entire ₹1,102 Cr goes to existing shareholders monetising part of their holding","chip":"PROMOTER EXIT"},
  ]},
  "n_proceeds": ("So where do the proceeds go? [pause] Because there's no fresh issue, none of the money funds the company — not "
    "capacity, not research, not debt, not working capital. [pause] The full one thousand one hundred crore goes to the selling "
    "promoters, who are converting part of their ownership into cash. [pause] Now, a pure O-F-S isn't automatically bad — it can simply "
    "mean early backers want liquidity — but you should know the growth of the business won't be funded by your money."),
  "verdict": {"kicker":"SHOULD YOU SUBSCRIBE?","title":"Strengths vs Watch-outs","mythLabel":"⚠️ WATCH-OUTS","factLabel":"✅ STRENGTHS","pairs":[
    {"m":"100% OFS — company gets nothing","f":"Profit up a strong 64% in FY26"},
    {"m":"No growth capital from the issue","f":"Niche global machinery leader"},
    {"m":"Machinery demand is capex-cycle sensitive","f":"Healthy 25% revenue growth"}],
  },
  "n_verdict": ("Should you subscribe? [pause] The strengths are real — profit up sixty-four percent, revenue up twenty-five, and a "
    "defensible global niche in specialised machinery. [pause] But the watch-outs are equally real — it's a hundred-percent sell-down, "
    "so none of your money strengthens the company; there's no growth capital in the deal; and machinery demand rises and falls with the "
    "broader capital-expenditure cycle. [pause] The bottom line — judge it purely as buying into a good business at this price, because "
    "the I-P-O itself adds nothing to that business."),
  "retail_min":"₹14,875", "hni_extra":"",
  "n_retail": ("How do you apply, and how much do you need? [pause] Retail investors bid up to two lakh rupees for a thirty-five "
    "percent quota — and if it's oversubscribed, allotment is by lottery, so a larger bid doesn't help. [pause] H-N-Is invest above two "
    "lakh for a fifteen percent quota. [pause] For Lohia Corp, one lot is thirty-five shares — about fourteen thousand eight hundred and "
    "seventy-five rupees — your minimum bid. [pause] Track the live subscription on the N-S-E and B-S-E I-P-O pages, Chittorgarh, "
    "Moneycontrol, or your broker app."),
  "recap": {"title":"Lohia Corp IPO — at a Glance","items":[
    "Business: global industrial-machinery maker","FY26: revenue ₹1,717 Cr (+25%), profit ₹193 Cr (+64%)",
    "₹1,102 Cr issue — 100% OFS, company gets ₹0","Every rupee goes to selling promoters","Retail min ~₹14,875"],
    "closer":"Strong business, but a pure cash-out. The IPO funds the owners, not the company."},
  "n_recap_pre": ("Let's recap Lohia Corp. [pause] A global maker of specialised industrial machinery, with profit up a sharp "
    "sixty-four percent. [pause] But the defining feature — this is a one hundred percent Offer for Sale. The company receives nothing; "
    "every rupee goes to the promoters cashing out. [pause] The retail minimum is about fourteen thousand eight hundred and seventy-five "
    "rupees. [pause] "),
},

"xtranet": {
  "accent": "#34D399", "name": "Xtranet Technologies IPO", "kicker": "IPO ANALYSIS · MAINBOARD",
  "sub": "Enterprise IT & data centres · ₹167 Cr · 100% Fresh · 23–27 Jul 2026",
  "n_title": ("Let's look at the Xtranet Technologies I-P-O — a smaller issue at one hundred and sixty-seven crore, but with a "
    "structure that's the opposite of the big names this week. [pause] We'll cover what it does, its financials, exactly where the "
    "money goes, and how much you'd need to apply. [pause] This is education, not investment advice."),
  "biz": {"kicker":"WHAT THE COMPANY DOES","title":"Inside Xtranet","color":"#34D399","items":[
    {"emoji":"🖥️","k":"Enterprise IT & data centres","v":"Builds and manages IT infrastructure, data-centre solutions and managed services for businesses and government","chip":"IT INFRA"},
    {"emoji":"☁️","k":"Software & integration","v":"ERP, system integration, cloud, analytics — plus digital-signature and PKI security platforms","chip":"SaaS + INTEGRATION"},
    {"emoji":"📈","k":"Riding a hot theme","v":"Data centres and digital transformation are among the fastest-growing IT spends in India","chip":"TAILWIND"},
  ]},
  "n_biz": ("So what does Xtranet do? [pause] It's an enterprise I-T company. It builds and manages I-T infrastructure, data-centre "
    "solutions, and managed services for businesses and government departments. [pause] On top of that it does software work — E-R-P, "
    "system integration, cloud, analytics — and it has security platforms for digital signatures and public-key infrastructure. [pause] "
    "Importantly, it sits on a hot theme — data centres and digital transformation are among the fastest-growing areas of I-T spending "
    "in India right now."),
  "fin": {"kicker":"FY26 FINANCIALS","title":"The Numbers","stats":[
    {"label":"Revenue FY26","to":366,"prefix":"₹","suffix":" Cr","color":"#34D399","sub":"+32% YoY"},
    {"label":"Net Profit FY26","to":41,"prefix":"₹","suffix":" Cr","color":"#34D399","sub":"+36% YoY (₹30 Cr → ₹41 Cr)"},
    {"label":"Issue size","to":167,"prefix":"₹","suffix":" Cr","color":"#22D3EE","sub":"price band ₹120–127"}],
    "note":"Small but fast-growing — revenue up 32% and profit up 36%. This is a genuinely profitable small-cap, not a story stock."},
  "n_fin": ("The financials are small but growing fast. [pause] Revenue for FY twenty twenty-six was three hundred and sixty-six "
    "crore, up thirty-two percent. Net profit rose thirty-six percent, from thirty crore to about forty-one crore. [pause] So this is a "
    "profitable small-cap that's genuinely scaling — not a loss-making story stock. Just remember, small companies are naturally more "
    "volatile than the big blue-chips."),
  "issue": {"kicker":"WHERE THE MONEY GOES","title":"Fresh Issue vs Offer-for-Sale","stats":[
    {"label":"Total issue","to":167,"prefix":"₹","suffix":" Cr","color":"#34D399","sub":"price band ₹120–127"},
    {"label":"Fresh (into company)","to":167,"prefix":"₹","suffix":" Cr","color":"#34D399","sub":"100% — all into the firm"},
    {"label":"OFS (to sellers)","to":0,"prefix":"₹","suffix":" Cr","color":"#34D399","sub":"ZERO — no promoter exit"}],
    "note":"THE GOOD KIND: this is a 100% fresh issue. Every rupee goes INTO the company to fund growth — no promoters are cashing out."},
  "n_issue": ("Now the key point — where does the money go? And here Xtranet is the mirror image of Lohia and Indo-MIM. [pause] "
    "This is a one hundred percent fresh issue. Every single rupee — all one hundred and sixty-seven crore — goes into the company "
    "itself. [pause] No promoters are selling, no one is cashing out. This is what people mean by the good kind of I-P-O — you're "
    "funding the business's growth, not buying someone's exit. [pause] Of course, that also means the promoters keep their full stake, "
    "which many investors like to see."),
  "proceeds": {"kicker":"USE OF PROCEEDS","title":"What the ₹167 Cr Funds","color":"#34D399","items":[
    {"emoji":"🔄","k":"~₹102 Cr — working capital","v":"The bulk funds day-to-day working capital, which an IT-services business needs to take on bigger contracts","chip":"GROWTH"},
    {"emoji":"🏦","k":"~₹22 Cr — repay debt","v":"Cuts borrowings and interest cost, strengthening the balance sheet","chip":"DEBT"},
    {"emoji":"🖧","k":"~₹7 Cr — capex","v":"New systems and hardware; the rest is general corporate purposes","chip":"CAPEX"},
  ]},
  "n_proceeds": ("Where does that fresh money go? [pause] The bulk — about one hundred and two crore — funds working capital. That "
    "matters, because an I-T services firm needs cash on hand to take on bigger contracts. [pause] Around twenty-two crore repays debt, "
    "cutting interest costs, and about seven crore goes to new systems and hardware, with the rest for general purposes. [pause] But note "
    "the flip side — a working-capital-hungry model means the business constantly needs cash to grow, which is a real risk to watch."),
  "verdict": {"kicker":"SHOULD YOU SUBSCRIBE?","title":"Strengths vs Watch-outs","mythLabel":"⚠️ WATCH-OUTS","factLabel":"✅ STRENGTHS","pairs":[
    {"m":"Small-cap — more volatile, less proven","f":"100% fresh issue — money funds growth"},
    {"m":"Working-capital heavy — always needs cash","f":"Profitable & fast-growing (rev +32%, PAT +36%)"},
    {"m":"Crowded, competitive IT-services market","f":"On the hot data-centre / digital theme"}],
  },
  "n_verdict": ("Should you subscribe? [pause] The strengths are attractive — it's a hundred-percent fresh issue, so your money "
    "actually funds growth; it's profitable and growing fast; and it rides the data-centre and digital-transformation wave. [pause] But "
    "the watch-outs are just as important — it's a small-cap, so it's more volatile and less proven; its model is working-capital hungry, "
    "meaning it constantly needs cash; and I-T services is a crowded, competitive market. [pause] The takeaway — the cleanest structure of "
    "the four, but a higher-risk, higher-reward small-cap. Size any bet accordingly."),
  "retail_min":"₹13,970", "hni_extra":"",
  "n_retail": ("How much do you need, and how do you apply? [pause] Retail investors bid up to two lakh for a thirty-five percent "
    "quota, with allotment by lottery if it's oversubscribed. [pause] H-N-Is go above two lakh for a fifteen percent quota. [pause] For "
    "Xtranet, one lot is one hundred and ten shares — about thirteen thousand nine hundred and seventy rupees — your minimum. [pause] "
    "Watch the live subscription on the N-S-E and B-S-E I-P-O pages, Chittorgarh, Moneycontrol, or your broker app."),
  "recap": {"title":"Xtranet Technologies IPO — at a Glance","items":[
    "Business: enterprise IT, data centres & managed services","FY26: revenue ₹366 Cr (+32%), profit ₹41 Cr (+36%)",
    "₹167 Cr issue — 100% FRESH, all into the company","Money funds working capital, debt & capex","Retail min ~₹13,970 · small-cap risk"],
    "closer":"The cleanest structure of the four — but a small, working-capital-hungry bet. Read the RHP."},
  "n_recap_pre": ("Let's recap Xtranet. [pause] An enterprise I-T and data-centre company, profitable and growing over thirty "
    "percent. [pause] Its stand-out feature — a one hundred percent fresh issue, so every rupee funds the business, mainly working "
    "capital. [pause] It's a small-cap though, and working-capital hungry, so it carries more risk. The retail minimum is about "
    "thirteen thousand nine hundred and seventy rupees. [pause] "),
},

"cube": {
  "accent": "#A78BFA", "name": "Cube Highways Trust", "kicker": "IPO ANALYSIS · InvIT (NOT A STOCK)",
  "sub": "Toll-road income trust · ₹5,000 Cr · ~9% yield · 22–24 Jul 2026",
  "n_title": ("Let's decode Cube Highways Trust — a five thousand crore issue that is NOT a normal I-P-O and NOT a stock. [pause] "
    "It's an InvIT — an Infrastructure Investment Trust — and it behaves very differently from a company share. Understanding that "
    "difference is the whole point of this video. [pause] This is education, not investment advice."),
  "biz": {"kicker":"WHAT IS AN InvIT?","title":"A Toll-Road Income Trust","color":"#A78BFA","items":[
    {"emoji":"🛣️","k":"It owns highways","v":"A trust that owns operating toll roads and passes the toll income to you as regular payouts — like a REIT, but for roads","chip":"NOT A STOCK"},
    {"emoji":"🗺️","k":"The portfolio","v":"27 highway assets · 8,754 lane-kilometres · across 12 states and 1 UT — large and diversified","chip":"27 ROADS"},
    {"emoji":"💵","k":"You buy income, not growth","v":"You're buying a stream of distributions, not betting on a share price multiplying","chip":"INCOME"},
  ]},
  "n_biz": ("So what exactly is this? [pause] Cube Highways is an InvIT — an Infrastructure Investment Trust. Think of it as a "
    "landlord for toll roads. The trust owns operating highways, collects the toll money, and passes most of that income to you as "
    "regular payouts. It works much like a R-E-I-T does for real estate. [pause] Its portfolio is large and diversified — twenty-seven "
    "highway assets, over eight thousand seven hundred lane-kilometres, spread across twelve states and one union territory. [pause] The "
    "mindset is completely different from a stock — you're buying a steady stream of income, not betting on a share price multiplying."),
  "fin": {"kicker":"THE INCOME MATH","title":"Yield & Terms","stats":[
    {"label":"Distribution yield","to":9,"prefix":"~","suffix":"%","color":"#34D399","sub":"FY26 payout ₹13.77 per unit"},
    {"label":"Price per unit","to":152,"prefix":"₹","suffix":"","color":"#A78BFA","sub":"band ₹151–152"},
    {"label":"Issue size","to":5000,"prefix":"₹","suffix":" Cr","color":"#22D3EE","sub":"32.89 Cr units"}],
    "note":"The headline is the ~9% yield — well above a bank FD. But a yield is not a guaranteed return; toll traffic and interest rates can move it."},
  "n_fin": ("Now the number that matters for an InvIT — the yield. [pause] Based on last year's payout of thirteen rupees "
    "seventy-seven per unit, at the price of one hundred and fifty-two, the distribution yield works out to roughly nine percent. That's "
    "meaningfully higher than a bank fixed deposit. [pause] The issue is large — five thousand crore, nearly thirty-three crore units. "
    "[pause] But a word of caution — a yield is not a guaranteed return. If toll traffic dips or interest rates change, both the payout "
    "and the unit price can move."),
  "issue": {"kicker":"WHERE THE MONEY GOES","title":"It's a 100% Offer-for-Sale","stats":[
    {"label":"Total issue","to":5000,"prefix":"₹","suffix":" Cr","color":"#A78BFA","sub":"price ₹151–152 per unit"},
    {"label":"Fresh (into trust)","to":0,"prefix":"₹","suffix":" Cr","color":"#F87171","sub":"no fresh units issued"},
    {"label":"OFS (to sellers)","to":5000,"prefix":"₹","suffix":" Cr","color":"#F87171","sub":"existing unitholders sell"}],
    "note":"This is a 100% OFS — existing unitholders are selling down. For an InvIT that's normal, but the trust isn't raising new money here."},
  "n_issue": ("Where does the money go? [pause] Like Lohia, this is a hundred-percent Offer for Sale — existing unitholders are "
    "selling part of their holding, and the trust itself isn't raising fresh money in this issue. [pause] For an InvIT, a sell-down like "
    "this is fairly normal — early sponsors monetising their stake. [pause] Interestingly, ahead of the public issue, five strategic "
    "investors already bought around one thousand two hundred and fifty crore worth of units — a vote of confidence, though not a "
    "guarantee of anything."),
  "proceeds": {"kicker":"WHO SHOULD LOOK AT THIS?","title":"Right Fit vs Wrong Fit","color":"#A78BFA","items":[
    {"emoji":"✅","k":"Good fit — income seekers","v":"If you want regular, FD-plus payouts and can hold long-term, a ~9% yielding road portfolio can suit you","chip":"INCOME"},
    {"emoji":"❌","k":"Wrong fit — quick gains","v":"If you're chasing a fast listing pop or a multibagger, an InvIT is NOT that — it's a slow, steady instrument","chip":"NOT A PUNT"},
    {"emoji":"⚖️","k":"Key risks","v":"Toll-traffic dips, interest-rate rises (which hurt yield instruments), and it's a long-dated hold","chip":"RISKS"},
  ]},
  "n_proceeds": ("So who is this actually for? [pause] It's a good fit if you want regular income — payouts a notch above a fixed "
    "deposit — and you can hold for the long term. A diversified toll-road portfolio yielding around nine percent can suit that goal. "
    "[pause] It's the wrong fit if you're chasing a quick listing pop or a multibagger — an InvIT is a slow, steady income instrument, "
    "not a punt. [pause] And the key risks — toll traffic can dip in a slowdown, rising interest rates tend to pull down yield "
    "instruments, and your capital is committed for the long haul."),
  "verdict": {"kicker":"SHOULD YOU SUBSCRIBE?","title":"Strengths vs Watch-outs","mythLabel":"⚠️ WATCH-OUTS","factLabel":"✅ STRENGTHS","pairs":[
    {"m":"It's a yield product, not a multibagger","f":"~9% distribution yield — beats an FD"},
    {"m":"Traffic & interest-rate sensitive","f":"Diversified 27-road, 12-state portfolio"},
    {"m":"100% OFS; long-dated commitment","f":"Stable, regulated, real-asset cash flows"}],
  },
  "n_verdict": ("Should you subscribe? [pause] The strengths — a roughly nine-percent yield that comfortably beats a fixed deposit, "
    "a large diversified portfolio of twenty-seven roads across twelve states, and stable, regulated cash flows from real assets. [pause] "
    "The watch-outs — it's an income product, not a multibagger; its payout is sensitive to toll traffic and interest rates; and it's a "
    "hundred-percent sell-down that you hold for the long term. [pause] The takeaway — judge it like a bond or an F-D alternative, not "
    "like a growth stock. Right tool, but only for the right goal."),
  "retail_min":"₹14,440", "hni_extra":"",
  "n_retail": ("How do you apply, and how much? [pause] For an InvIT the categories work a little differently, but broadly — retail "
    "investors apply in the smaller bucket, and larger investors above the retail limit sit in the institutional and non-institutional "
    "categories, which dominate InvIT demand. [pause] For Cube Highways, one lot is ninety-five units — about fourteen thousand four "
    "hundred and forty rupees — your minimum. [pause] And check the live subscription on the N-S-E and B-S-E I-P-O pages, Chittorgarh, "
    "Moneycontrol, or your broker app."),
  "recap": {"title":"Cube Highways InvIT — at a Glance","items":[
    "An InvIT — a toll-road income trust, NOT a stock","27 roads · 8,754 lane-km · 12 states + 1 UT",
    "~9% distribution yield (FY26 ₹13.77/unit)","₹5,000 Cr issue — 100% OFS, price ₹151–152","Min ~₹14,440 · for income, not quick gains"],
    "closer":"An FD-plus income instrument, not a growth punt. Match it to your goal, read the offer document."},
  "n_recap_pre": ("Let's recap Cube Highways. [pause] It's an InvIT — a toll-road income trust, not a stock — owning twenty-seven "
    "highways across twelve states. [pause] Its appeal is a roughly nine-percent yield, well above a fixed deposit. [pause] It's a hundred-"
    "percent Offer for Sale, priced near one hundred and fifty-two per unit, with a minimum of about fourteen thousand four hundred and "
    "forty rupees. Treat it as income, not a quick gain. [pause] "),
},

"manipal": {
  "accent": "#FB7185", "name": "Manipal Health IPO", "kicker": "IPO ANALYSIS · MAINBOARD",
  "sub": "India's biggest hospital IPO · ₹9,275 Cr · 29–31 Jul 2026",
  "n_title": ("Let's break down the Manipal Health I-P-O — at nine thousand two hundred and seventy-five crore rupees, it is the "
    "biggest healthcare I-P-O India has ever seen. [pause] By the end you'll understand what the company does, its financials, where "
    "your money actually goes, and how much you'd need to apply as a retail or an H-N-I investor. [pause] Quick note — this is "
    "education, not investment advice, and not a tip to buy."),
  "biz": {"kicker":"WHAT THE COMPANY DOES","title":"Inside Manipal Health","color":"#FB7185","items":[
    {"emoji":"🏥","k":"A large hospital network","v":"One of India's largest multispeciality hospital chains, running a network of hospitals across the country","chip":"HOSPITALS"},
    {"emoji":"🩺","k":"Full-service healthcare","v":"From complex quaternary care to diagnostics and pharmacies — a strong, trusted brand, especially in South and West India","chip":"FULL-STACK"},
    {"emoji":"🏦","k":"Marquee ownership","v":"Backed by big global investors — Temasek is the promoter, with TPG and Novo Holdings among the shareholders","chip":"BIG BACKERS"},
  ]},
  "n_biz": ("So what is Manipal Health? [pause] It's one of India's largest multispeciality hospital chains — a network of hospitals "
    "spread across the country. [pause] It offers the full range of care, from complex quaternary treatment to diagnostics and pharmacies, "
    "and it's a trusted brand, particularly in South and West India. [pause] It also has serious backers — Temasek is the promoter, and "
    "investors like T-P-G and Novo Holdings are on the cap table. A big, established, professionally-run healthcare business."),
  "fin": {"kicker":"FY26 FINANCIALS","title":"The Numbers","stats":[
    {"label":"Revenue FY26","to":10521,"prefix":"₹","suffix":" Cr","color":"#34D399","sub":"≈ ₹10,520.52 Cr"},
    {"label":"Net Profit FY26","to":917,"prefix":"₹","suffix":" Cr","color":"#34D399","sub":"≈ ₹916.52 Cr — solidly profitable"},
    {"label":"Valuation","to":77600,"prefix":"~₹","suffix":" Cr","color":"#FB7185","sub":"at the ₹590 upper band"}],
    "note":"A large, genuinely profitable hospital chain. But at roughly ₹77,600 crore, it's valued near 85 times its earnings — a rich, premium price."},
  "n_fin": ("Now the financials — and they're solid. [pause] In the year ended March twenty twenty-six, Manipal did about ten thousand "
    "five hundred and twenty crore in revenue and a net profit of roughly nine hundred and seventeen crore. So this is a large, genuinely "
    "profitable business, not a loss-maker. [pause] But here's the catch — at the top of the band the company is valued near seventy-seven "
    "thousand six hundred crore. That's roughly eighty-five times its earnings — a rich, premium valuation you're paying up for."),
  "issue": {"kicker":"WHERE THE MONEY GOES","title":"Fresh Issue vs Offer-for-Sale","stats":[
    {"label":"Total issue","to":9275,"prefix":"₹","suffix":" Cr","color":"#FB7185","sub":"price band ₹560–590"},
    {"label":"Fresh (into company)","to":8000,"prefix":"₹","suffix":" Cr","color":"#34D399","sub":"86% — into the company"},
    {"label":"OFS (to sellers)","to":1275,"prefix":"₹","suffix":" Cr","color":"#F87171","sub":"~14% — TPG, Novo & others exit"}],
    "note":"Mostly a FRESH issue — the better structure. But watch where that fresh money goes: the bulk simply repays debt, not new hospitals."},
  "n_issue": ("Here's the most important part of any I-P-O — where does your money go? [pause] The good news — eight thousand crore of "
    "the nine-thousand-crore issue is a fresh issue, money going into the company. That's about eighty-six percent. [pause] The remaining "
    "one thousand two hundred and seventy-five crore is an Offer for Sale — existing investors like T-P-G and Novo Holdings selling part of "
    "their stakes and pocketing that cash. [pause] So structurally this is mostly a fresh issue, which is the healthier kind. But — and it's "
    "a big but — what the company DOES with that fresh money is the real story."),
  "proceeds": {"kicker":"USE OF THE FRESH MONEY","title":"What the ₹8,000 Cr Funds","color":"#FB7185","items":[
    {"emoji":"🏦","k":"₹5,378 Cr — repay debt","v":"The bulk of the fresh money simply pays down borrowings at its subsidiary, Manipal Hospitals — it de-risks the balance sheet, but doesn't add new capacity","chip":"DEBT"},
    {"emoji":"🏥","k":"₹574 Cr — buy out Sahyadri minority","v":"Acquires the remaining minority stake in Sahyadri Hospitals, tightening its ownership of an acquired chain","chip":"CONSOLIDATE"},
    {"emoji":"🧰","k":"Balance — general corporate","v":"The rest goes to general corporate purposes, the standard catch-all bucket","chip":"GCP"},
  ]},
  "n_proceeds": ("So what does that eight thousand crore of fresh money actually fund? [pause] The bulk — five thousand three hundred and "
    "seventy-eight crore — simply repays debt at its main subsidiary, Manipal Hospitals. That's not bad; it cuts interest costs and "
    "strengthens the balance sheet — but it does not build new hospitals or add beds. [pause] Another five hundred and seventy-four crore buys "
    "out the minority holders in Sahyadri Hospitals, a chain it acquired. [pause] So most of the fresh money cleans up the balance sheet and "
    "consolidates ownership, rather than funding brand-new expansion."),
  "verdict": {"kicker":"SHOULD YOU SUBSCRIBE?","title":"Strengths vs Watch-outs","mythLabel":"⚠️ WATCH-OUTS","factLabel":"✅ STRENGTHS","pairs":[
    {"m":"₹5,378 Cr of fresh money repays debt, not new capacity","f":"Large, profitable, trusted hospital brand"},
    {"m":"Rich valuation — roughly 85x earnings","f":"86% is a fresh issue — mostly funds the company"},
    {"m":"GMP is modest (~1%) — a muted listing signal","f":"Marquee backers; ~₹4,167 Cr anchor book"}],
  },
  "n_verdict": ("So — should you subscribe? Let's weigh it honestly. [pause] On the strengths side — it's a large, profitable, well-known "
    "hospital brand; the deal is mostly a fresh issue, which is the healthier structure; and it pulled in a big anchor book of over four "
    "thousand crore, a vote of confidence from institutions. [pause] On the watch-out side — the bulk of the fresh money repays debt rather "
    "than building new capacity, the valuation is rich at around eighty-five times earnings, and the grey-market premium is modest, near one "
    "percent, hinting at a muted debut. [pause] The takeaway — a high-quality hospital chain, but you're paying a premium price for it."),
  "retail_min":"₹14,750", "hni_extra":"",
  "n_retail": ("Finally — how do you apply, and how much do you need? [pause] As a retail investor you can put in up to two lakh rupees, "
    "for a thirty-five percent quota. But if it's oversubscribed, shares are given out by lottery — so a bigger cheque does not get you more. "
    "[pause] H-N-Is bid above two lakh and share a fifteen percent quota. [pause] For Manipal, one lot is twenty-five shares — about fourteen "
    "thousand seven hundred and fifty rupees — and that's your minimum. [pause] To watch the subscription build up live, use the N-S-E and "
    "B-S-E I-P-O pages, Chittorgarh, Moneycontrol, or your broker app."),
  "recap": {"title":"Manipal Health IPO — at a Glance","items":[
    "Business: one of India's largest hospital chains","FY26: revenue ₹10,520.52 Cr, profit ₹916.52 Cr",
    "₹9,275 Cr issue — India's biggest healthcare IPO, 86% fresh","But ₹5,378 Cr of fresh money repays debt, not new hospitals","Retail min ~₹14,750 · ~85x earnings · GMP ~1% (unofficial)"],
    "closer":"A quality hospital chain at a premium price — mostly deleveraging, not expansion. Read the RHP; decide for yourself."},
  "n_recap_pre": ("Let's recap Manipal Health. [pause] One of India's largest hospital chains, genuinely profitable, doing over ten "
    "thousand crore in revenue. [pause] At nine thousand two hundred crore it's the biggest healthcare I-P-O in India — and it's mostly a "
    "fresh issue. But the bulk of that fresh money, over five thousand crore, repays debt rather than building new hospitals, and the "
    "valuation is rich at around eighty-five times earnings. [pause] Retail minimum is about fourteen thousand seven hundred and fifty "
    "rupees, and the grey-market premium is modest, near one percent — though that's unofficial. [pause] "),
},

"juniper": {
  "accent": "#34D399", "name": "Juniper Green Energy IPO", "kicker": "IPO ANALYSIS · MAINBOARD",
  "sub": "Renewable power · ₹1,800 Cr · 100% Fresh · 30 Jul–3 Aug 2026",
  "n_title": ("Let's analyse the Juniper Green Energy I-P-O — an eighteen hundred crore issue from a renewable-power company. [pause] "
    "It's a one hundred percent fresh issue, which usually sounds great — but there's a twist in where that money goes that every investor "
    "should understand. We'll cover the business, the financials, the money trail, and how much you need to apply. [pause] This is "
    "education, not investment advice."),
  "biz": {"kicker":"WHAT THE COMPANY DOES","title":"Inside Juniper Green Energy","color":"#34D399","items":[
    {"emoji":"⚡","k":"Renewable power producer","v":"Develops, owns and operates solar and wind power projects — an independent power producer, or I-P-P","chip":"SOLAR + WIND"},
    {"emoji":"🔌","k":"Sells power on long contracts","v":"Supplies electricity under long-term purchase agreements, giving it contracted, recurring cash flows","chip":"LONG-TERM PPAs"},
    {"emoji":"🌱","k":"Rides the clean-energy push","v":"Sits on India's fast-growing renewable theme — but it's a capital-hungry, heavily-financed business","chip":"GROWTH THEME"},
  ]},
  "n_biz": ("So what does Juniper Green Energy do? [pause] It's a renewable-power company — an independent power producer that develops, "
    "owns and operates solar and wind projects. [pause] It sells that electricity under long-term power-purchase agreements, which gives it "
    "steady, contracted cash flows year after year. [pause] It's riding India's fast-growing clean-energy theme — but keep one thing in mind: "
    "building power plants is enormously capital-hungry, so these businesses carry a lot of debt."),
  "fin": {"kicker":"FY26 FINANCIALS","title":"The Numbers","stats":[
    {"label":"Revenue FY26","to":805,"prefix":"₹","suffix":" Cr","color":"#34D399","sub":"₹424 → ₹570 → ₹805 Cr (FY24-26)"},
    {"label":"Net Profit FY26","to":40,"prefix":"₹","suffix":" Cr","color":"#FBBF24","sub":"just +11% YoY (₹36.48 → ₹40.46 Cr)"},
    {"label":"Net worth","to":123,"prefix":"₹","suffix":" Cr","color":"#F87171","sub":"tiny vs an ₹1,800 Cr raise"}],
    "note":"Revenue nearly doubled in two years — impressive. But profit barely grew, and net worth is just ₹123 crore against an ₹1,800 crore raise, which tells you how leveraged this is."},
  "n_fin": ("Now the financials. [pause] Revenue has grown fast — from four hundred and twenty-four crore two years ago, to five hundred "
    "and seventy, to eight hundred and five crore in FY twenty twenty-six. That's nearly doubling in two years. [pause] But profit tells a "
    "quieter story — net profit was only about forty crore, up just eleven percent. [pause] And here's the number that matters most — the "
    "company's net worth is only around one hundred and twenty-three crore, against an eighteen hundred crore raise. That gap tells you this "
    "is a heavily-leveraged, debt-laden business."),
  "issue": {"kicker":"WHERE THE MONEY GOES","title":"Fresh Issue vs Offer-for-Sale","stats":[
    {"label":"Total issue","to":1800,"prefix":"₹","suffix":" Cr","color":"#34D399","sub":"price band ₹214–225"},
    {"label":"Fresh (into company)","to":1800,"prefix":"₹","suffix":" Cr","color":"#34D399","sub":"100% — all new money"},
    {"label":"OFS (to sellers)","to":0,"prefix":"₹","suffix":" Cr","color":"#34D399","sub":"ZERO — no promoter exit"}],
    "note":"Structurally, this is the good kind — a 100% fresh issue, no promoters cashing out. But the twist is what the fresh money is USED for — see next."},
  "n_issue": ("So where does the money go? [pause] On the surface, this is the good kind of I-P-O — a one hundred percent fresh issue. "
    "There's no offer for sale, so no promoter is cashing out. Every rupee — all eighteen hundred crore — goes into the company. [pause] "
    "But hold on, because this is exactly where you have to read the fine print. A fresh issue funds the company, yes — but funds it to do "
    "WHAT? [pause] For many I-P-Os that means new factories or capacity. For Juniper, as you'll see next, most of it does something very "
    "different."),
  "proceeds": {"kicker":"USE OF THE FRESH MONEY","title":"What the ₹1,800 Cr Funds","color":"#34D399","items":[
    {"emoji":"🏦","k":"₹683 Cr — repay own debt","v":"The company uses a big chunk to pay down its own borrowings","chip":"DEBT"},
    {"emoji":"🏭","k":"₹729 Cr — fund subsidiaries' debt","v":"More money goes into subsidiaries so THEY can repay their borrowings too","chip":"MORE DEBT"},
    {"emoji":"🧰","k":"Balance — general corporate","v":"Only the remainder is flexible, for general corporate purposes","chip":"GCP"},
  ]},
  "n_proceeds": ("Here's the twist. [pause] Of the eighteen hundred crore of fresh money, about six hundred and eighty-three crore repays "
    "the company's own borrowings, and another seven hundred and twenty-nine crore is pushed into its subsidiaries so THEY can repay their "
    "debt. [pause] Add those up — that's roughly fourteen hundred crore, about seventy-eight percent of the entire issue, going to repay "
    "debt. [pause] So while it's technically a fresh issue, it's not really funding new solar farms — it's deleveraging a debt-heavy balance "
    "sheet. That's a very different thing from funding growth."),
  "verdict": {"kicker":"SHOULD YOU SUBSCRIBE?","title":"Strengths vs Watch-outs","mythLabel":"⚠️ WATCH-OUTS","factLabel":"✅ STRENGTHS","pairs":[
    {"m":"~78% of fresh money repays debt, not new capacity","f":"100% fresh issue — no promoter cash-out"},
    {"m":"Heavily leveraged; profit up just 11%","f":"Revenue nearly doubled in two years"},
    {"m":"Capital-intensive; execution & tariff risk","f":"On India's clean-energy tailwind"}],
  },
  "n_verdict": ("Should you subscribe? [pause] The strengths — it's a hundred-percent fresh issue with no promoter selling; revenue has "
    "nearly doubled in two years; and it rides India's powerful clean-energy tailwind. [pause] The watch-outs — around seventy-eight percent "
    "of the fresh money repays debt rather than building new capacity; the balance sheet is heavily leveraged and profit grew only eleven "
    "percent; and power generation is capital-intensive with real execution and tariff risks. [pause] The takeaway — a fresh issue on paper, "
    "but mostly a deleveraging exercise. Judge it as a debt clean-up, not a growth-capital raise."),
  "retail_min":"₹14,850", "hni_extra":"",
  "n_retail": ("How do you apply, and how much do you need? [pause] Retail investors bid up to two lakh rupees for a thirty-five percent "
    "quota — and if it's oversubscribed, allotment is by lottery, so a bigger bid doesn't help. [pause] H-N-Is invest above two lakh for a "
    "fifteen percent quota. [pause] For Juniper, one lot is sixty-six shares — about fourteen thousand eight hundred and fifty rupees — your "
    "minimum bid. [pause] Track the live subscription on the N-S-E and B-S-E I-P-O pages, Chittorgarh, Moneycontrol, or your broker app."),
  "recap": {"title":"Juniper Green Energy IPO — at a Glance","items":[
    "Business: renewable solar & wind power producer","FY26: revenue ₹804.93 Cr, profit ₹40.46 Cr (+11%)",
    "₹1,800 Cr issue — 100% fresh, no promoter exit","But ~₹1,412 Cr (78%) repays debt, not new capacity","Retail min ~₹14,850 · GMP ~7.6% (unofficial)"],
    "closer":"A fresh issue that mostly repays debt — deleveraging, not growth. Read the RHP; decide for yourself."},
  "n_recap_pre": ("Let's recap Juniper Green Energy. [pause] A renewable-power producer whose revenue nearly doubled in two years, though "
    "profit grew just eleven percent. [pause] The I-P-O is a one hundred percent fresh issue — the good structure — but here's the catch: "
    "about seventy-eight percent of that fresh money repays debt rather than building new capacity. The balance sheet is heavily leveraged. "
    "[pause] Retail minimum is about fourteen thousand eight hundred and fifty rupees, and the grey-market premium is near seven and a half "
    "percent, though that's unofficial. [pause] "),
},

"mvelectro": {
  "accent": "#38BDF8", "name": "MV Electrosystems IPO", "kicker": "IPO ANALYSIS · MAINBOARD",
  "sub": "Railway power-electronics · ₹290 Cr · 100% Fresh · 30 Jul–3 Aug 2026",
  "n_title": ("Let's look at the MV Electrosystems I-P-O — a two hundred and ninety crore issue from a railway power-electronics maker. "
    "[pause] This one has a fascinating tension inside it — a clean, hundred-percent fresh structure and a huge order book on one side, and "
    "a tiny, loss-making set of financials on the other. We'll unpack all of it, and how much you'd need to apply. [pause] This is "
    "education, not investment advice."),
  "biz": {"kicker":"WHAT THE COMPANY DOES","title":"Inside MV Electrosystems","color":"#38BDF8","items":[
    {"emoji":"🚆","k":"Railway propulsion systems","v":"Builds I-G-B-T based 3-phase drive propulsion equipment — the systems that actually move electric locomotives","chip":"PROPULSION"},
    {"emoji":"🔧","k":"Coach & EMU electricals","v":"Also makes switchgear panels, cable management and electrical sub-systems for railway coaches and E-M-Us","chip":"RAIL GEAR"},
    {"emoji":"🇮🇳","k":"A Make-in-India rail play","v":"A decade-long Indian Railways supplier with in-house research and development","chip":"IN-HOUSE R&D"},
  ]},
  "n_biz": ("So what does MV Electrosystems do? [pause] It's a railway power-electronics company. Its flagship product is I-G-B-T based "
    "three-phase drive propulsion equipment — essentially the systems that move electric locomotives down the track. [pause] It also makes "
    "switchgear panels, cable-management products and electrical sub-systems for railway coaches and E-M-Us. [pause] It's very much a "
    "Make-in-India rail play — a supplier to Indian Railways for about a decade, with its own in-house research and development. A "
    "specialised, engineering-led niche."),
  "fin": {"kicker":"FY26 FINANCIALS","title":"The Numbers","stats":[
    {"label":"Revenue FY26","to":49.79,"decimals":2,"prefix":"₹","suffix":" Cr","color":"#F87171","sub":"FELL from ₹64.64 Cr in FY25"},
    {"label":"Net result FY26","to":12.63,"decimals":2,"prefix":"−₹","suffix":" Cr","color":"#F87171","sub":"swung to a LOSS (from ₹1.40 Cr profit)"},
    {"label":"Executable order book","to":921.64,"decimals":2,"prefix":"₹","suffix":" Cr","color":"#38BDF8","sub":"~18x FY26 revenue"}],
    "note":"The whole tension of this IPO: revenue is tiny and just turned loss-making — yet the order book is ₹921.64 crore, nearly 18 times last year's sales."},
  "n_fin": ("Now the financials — and this is where it gets interesting. [pause] Revenue in FY twenty twenty-six was tiny — just under "
    "fifty crore — and it actually FELL from about sixty-five crore the year before. Worse, the company swung to a loss of about twelve and "
    "a half crore, after a small profit the previous year. [pause] So on the face of it, this looks weak. [pause] But here's the other side "
    "— its executable order book is nine hundred and twenty-one crore. That is nearly eighteen times last year's revenue. The whole bet is "
    "whether it can convert that order book into profitable sales."),
  "issue": {"kicker":"WHERE THE MONEY GOES","title":"Fresh Issue vs Offer-for-Sale","stats":[
    {"label":"Total issue","to":290,"prefix":"₹","suffix":" Cr","color":"#38BDF8","sub":"price band ₹400–425"},
    {"label":"Fresh (into company)","to":290,"prefix":"₹","suffix":" Cr","color":"#34D399","sub":"100% — all into the firm"},
    {"label":"OFS (to sellers)","to":0,"prefix":"₹","suffix":" Cr","color":"#34D399","sub":"ZERO — no promoter exit"}],
    "note":"Structurally clean: a 100% fresh issue. Every rupee goes into the company — mostly working capital to deliver that huge order book."},
  "n_issue": ("Where does the money go? [pause] Here the structure is clean — this is a one hundred percent fresh issue. There's no offer "
    "for sale, so no promoter is cashing out. All two hundred and ninety crore goes straight into the company. [pause] And that actually "
    "matters a lot here, because a company sitting on a nine-hundred-crore order book but tiny revenue has one obvious problem — it needs "
    "cash to buy raw materials and build all those orders. [pause] So the fresh money is going exactly where this business needs it — into "
    "working capital."),
  "proceeds": {"kicker":"USE OF THE FRESH MONEY","title":"What the ₹290 Cr Funds","color":"#38BDF8","items":[
    {"emoji":"🔄","k":"~₹180 Cr — working capital","v":"The bulk funds long-term working capital — buying raw materials and scaling output to deliver the large order book","chip":"GROWTH"},
    {"emoji":"🔬","k":"~₹21 Cr — R&D","v":"Invests in research and development of next-generation power-electronics equipment","chip":"R&D"},
    {"emoji":"🧰","k":"Balance — general corporate","v":"The remainder goes to general corporate purposes","chip":"GCP"},
  ]},
  "n_proceeds": ("So what does the fresh money fund? [pause] The bulk — around one hundred and eighty crore — goes into long-term working "
    "capital. That's the fuel it needs to buy raw materials and ramp up production, reportedly from around twenty propulsion sets a month "
    "toward fifty. [pause] About twenty-one crore goes into research and development of next-generation power electronics, and the rest to "
    "general purposes. [pause] But note the flip side — a working-capital-hungry model that's already loss-making means the business "
    "constantly needs cash to grow. Execution is everything here."),
  "verdict": {"kicker":"SHOULD YOU SUBSCRIBE?","title":"Strengths vs Watch-outs","mythLabel":"⚠️ WATCH-OUTS","factLabel":"✅ STRENGTHS","pairs":[
    {"m":"Tiny & just turned loss-making (−₹12.63 Cr)","f":"100% fresh issue — money funds delivery"},
    {"m":"76.72% of revenue from Indian Railways alone","f":"₹921.64 Cr executable order book"},
    {"m":"Negative returns at this valuation","f":"Make-in-India rail theme; in-house R&D"}],
  },
  "n_verdict": ("Should you subscribe? [pause] The strengths — it's a hundred-percent fresh issue, so your money funds delivery of that "
    "order book; the order book itself is huge at over nine hundred crore; and it rides the Make-in-India railway theme with its own R&D. "
    "[pause] The watch-outs are serious though — the company is tiny and just turned loss-making; more than seventy-six percent of its "
    "revenue comes from a single customer, Indian Railways; and its returns on capital are currently negative at this valuation. [pause] The "
    "takeaway — this is a high-risk, order-book-driven bet. It works only if it executes and turns that backlog into profit. Size any "
    "position accordingly."),
  "retail_min":"₹14,450", "hni_extra":"",
  "n_retail": ("How much do you need, and how do you apply? [pause] Retail investors bid up to two lakh for a thirty-five percent quota, "
    "with allotment by lottery if it's oversubscribed. [pause] H-N-Is go above two lakh for a fifteen percent quota. [pause] For MV "
    "Electrosystems, one lot is thirty-four shares — about fourteen thousand four hundred and fifty rupees — your minimum. [pause] Watch the "
    "live subscription on the N-S-E and B-S-E I-P-O pages, Chittorgarh, Moneycontrol, or your broker app."),
  "recap": {"title":"MV Electrosystems IPO — at a Glance","items":[
    "Business: railway propulsion & coach electricals","FY26: revenue ₹49.79 Cr (fell), NET LOSS ₹12.63 Cr",
    "₹290 Cr issue — 100% fresh, all into the company","Order book ₹921.64 Cr, but 76.72% from Railways","Retail min ~₹14,450 · high-risk small-cap"],
    "closer":"A clean structure and a huge order book — but tiny, loss-making and single-customer heavy. A pure execution bet. Read the RHP."},
  "n_recap_pre": ("Let's recap MV Electrosystems. [pause] A railway power-electronics maker with a clean, hundred-percent fresh issue — "
    "money that funds working capital to deliver its orders. [pause] The tension — its revenue is tiny and just turned to a loss, and over "
    "seventy-six percent of sales come from Indian Railways alone. Yet its order book is over nine hundred crore, nearly eighteen times "
    "revenue. [pause] It's a high-risk execution bet, with a retail minimum of about fourteen thousand four hundred and fifty rupees. "
    "[pause] "),
},

"ardee": {
  "accent": "#FACC15", "name": "Ardee Industries IPO", "kicker": "IPO ANALYSIS · MAINBOARD",
  "sub": "Battery & lead recycling · ₹425.87 Cr · 75% Fresh · 5–7 Aug 2026",
  "n_title": ("Let's break down the Ardee Industries I-P-O — a four hundred and twenty-six crore issue from a battery-recycling company, "
    "and the fastest-growing business of this whole batch. [pause] We'll cover what it does, its financials, where the money goes, and how "
    "much you'd need to apply as a retail or an H-N-I investor. [pause] This is education, not investment advice."),
  "biz": {"kicker":"WHAT THE COMPANY DOES","title":"Inside Ardee Industries","color":"#FACC15","items":[
    {"emoji":"♻️","k":"Recycles old batteries","v":"Recovers lead and non-ferrous metals from end-of-life batteries and energy-storage products","chip":"RECYCLING"},
    {"emoji":"🔋","k":"Makes high-purity lead","v":"Turns that recovered material into high-purity lead and specialised alloys for industry","chip":"PURE LEAD"},
    {"emoji":"🌍","k":"A circular-economy / EV play","v":"Serves battery, e-mobility, automotive and chemical customers; based in Tirupati, Andhra Pradesh","chip":"EV THEME"},
  ]},
  "n_biz": ("So what does Ardee Industries do? [pause] It's a recycling company. It takes end-of-life batteries and other energy-storage "
    "products and recovers the lead and non-ferrous metals inside them. [pause] It then refines that into high-purity lead and specialised "
    "alloys, which it sells to battery makers, the e-mobility and automotive industries, and chemical companies. [pause] It's based in "
    "Tirupati, Andhra Pradesh, and it sits on a genuinely interesting theme — the circular economy. As batteries and E-Vs grow, so does the "
    "need to recycle them."),
  "fin": {"kicker":"FY26 FINANCIALS","title":"The Numbers","stats":[
    {"label":"Revenue FY26","to":1168,"prefix":"₹","suffix":" Cr","color":"#34D399","sub":"+57% YoY (₹742.7 → ₹1,167.65 Cr)"},
    {"label":"Net Profit FY26","to":85,"prefix":"₹","suffix":" Cr","color":"#34D399","sub":"+155% YoY (₹33.3 → ₹84.68 Cr)"},
    {"label":"Grey-mkt premium","to":24.5,"decimals":1,"prefix":"~","suffix":"%","color":"#FACC15","sub":"unofficial · ₹13 over ₹53 cap"}],
    "note":"The fastest grower of the batch — revenue up 57% and profit up a striking 155%. The grey market is pricing a strong debut, but GMP is unofficial."},
  "n_fin": ("Now the financials — and they're the strongest growth story of this batch. [pause] Revenue jumped fifty-seven percent, from "
    "about seven hundred and forty-three crore to over eleven hundred and sixty-seven crore in FY twenty twenty-six. And net profit "
    "exploded a hundred and fifty-five percent, from thirty-three crore to nearly eighty-five crore. [pause] That's genuinely rapid growth. "
    "[pause] The grey market has taken notice too, pricing a premium of around twenty-four percent — but remember, that number is unofficial "
    "and drifts every day."),
  "issue": {"kicker":"WHERE THE MONEY GOES","title":"Fresh Issue vs Offer-for-Sale","stats":[
    {"label":"Total issue","to":426,"prefix":"₹","suffix":" Cr","color":"#FACC15","sub":"₹425.87 Cr · band ₹50–53"},
    {"label":"Fresh (into company)","to":320,"prefix":"₹","suffix":" Cr","color":"#34D399","sub":"75% — funds the business"},
    {"label":"OFS (to sellers)","to":106,"prefix":"₹","suffix":" Cr","color":"#F87171","sub":"₹105.87 Cr — promoters part-sell"}],
    "note":"A healthy mix: 75% is a fresh issue funding the business; 25% is the promoters, Sandeep and Nikunj Aggarwal, selling part of their stake."},
  "n_issue": ("Where does your money go? [pause] Here Ardee strikes a healthy balance. Of the four hundred and twenty-six crore issue, "
    "three hundred and twenty crore — about seventy-five percent — is a fresh issue, money going into the company. [pause] The remaining "
    "one hundred and six crore is an offer for sale, where the promoters, Sandeep and Nikunj Aggarwal, sell part of their stake and take "
    "some cash off the table. [pause] So this isn't a pure sell-down like some I-P-Os, nor entirely fresh — three-quarters funds the "
    "business, one-quarter rewards the founders. A reasonable, common structure."),
  "proceeds": {"kicker":"USE OF THE FRESH MONEY","title":"What the ₹320 Cr Funds","color":"#FACC15","items":[
    {"emoji":"🔄","k":"₹220 Cr — working capital","v":"The bulk funds working capital — a recycling and metals business ties up heavy cash in inventory and raw material","chip":"GROWTH"},
    {"emoji":"🏦","k":"₹20 Cr — repay debt","v":"A slice repays borrowings, trimming interest costs","chip":"DEBT"},
    {"emoji":"🧰","k":"Balance — general corporate","v":"The rest goes to general corporate purposes","chip":"GCP"},
  ]},
  "n_proceeds": ("What does the fresh money fund? [pause] The large majority — about two hundred and twenty crore — goes into working "
    "capital. That makes sense: a recycling and metals business ties up a lot of cash in inventory and raw material, so growth needs "
    "funding. [pause] Around twenty crore repays debt, cutting interest costs, and the rest is for general purposes. [pause] The flip side "
    "to watch — a working-capital-heavy, commodity-linked model means both cash needs and profits can swing with lead prices."),
  "verdict": {"kicker":"SHOULD YOU SUBSCRIBE?","title":"Strengths vs Watch-outs","mythLabel":"⚠️ WATCH-OUTS","factLabel":"✅ STRENGTHS","pairs":[
    {"m":"Lead & commodity price swings hit margins","f":"Explosive growth — revenue +57%, profit +155%"},
    {"m":"Working-capital heavy — always needs cash","f":"75% fresh — mostly funds the business"},
    {"m":"25% OFS — promoters partly cash out","f":"On the EV / battery-recycling theme; GMP ~24.5%"}],
  },
  "n_verdict": ("Should you subscribe? [pause] The strengths are attractive — it's growing explosively, with revenue up fifty-seven "
    "percent and profit up a hundred and fifty-five; three-quarters of the issue is fresh money funding the business; and it rides the "
    "E-V and battery-recycling theme, which the grey market clearly likes. [pause] The watch-outs — its profits are tied to volatile lead "
    "and commodity prices; the model is working-capital hungry, so it always needs cash; and a quarter of the issue is the promoters "
    "cashing out. [pause] The takeaway — the best growth and structure of this batch, but a commodity-linked business. Understand the lead-"
    "price risk before you decide."),
  "retail_min":"₹14,893", "hni_extra":"",
  "n_retail": ("Finally — how do you apply, and how much do you need? [pause] Retail investors can bid up to two lakh rupees for a "
    "thirty-five percent quota, with allotment by lottery if it's oversubscribed — so a bigger cheque doesn't help. [pause] H-N-Is bid "
    "above two lakh for a fifteen percent quota. [pause] For Ardee, one lot is two hundred and eighty-one shares — about fourteen thousand "
    "eight hundred and ninety-three rupees — your minimum. [pause] Track the live subscription on the N-S-E and B-S-E I-P-O pages, "
    "Chittorgarh, Moneycontrol, or your broker app."),
  "recap": {"title":"Ardee Industries IPO — at a Glance","items":[
    "Business: battery & lead recycling (circular economy)","FY26: revenue ₹1,167.65 Cr (+57%), profit ₹84.68 Cr (+155%)",
    "₹425.87 Cr issue — 75% fresh, 25% promoter OFS","Fresh money mainly funds working capital","Retail min ~₹14,893 · GMP ~24.5% (unofficial)"],
    "closer":"The best growth and structure of the batch — but a commodity-linked, lead-price-sensitive business. Read the RHP; decide for yourself."},
  "n_recap_pre": ("Let's recap Ardee Industries. [pause] A battery and lead-recycling business on the circular-economy theme, and the "
    "fastest grower of this batch — revenue up fifty-seven percent, profit up a hundred and fifty-five. [pause] The issue is a healthy mix: "
    "seventy-five percent fresh money funding the company, twenty-five percent a promoter sell-down, with the fresh money mainly funding "
    "working capital. [pause] Retail minimum is about fourteen thousand eight hundred and ninety-three rupees, and the grey-market premium "
    "is around twenty-four percent, though that's unofficial. [pause] "),
},
"technocraft": {
  "accent": "#22D3EE", "name": "Technocraft Ventures IPO", "kicker": "IPO ANALYSIS · MAINBOARD",
  "sub": "Government EPC & water infra · ₹251.88 Cr · 80% Fresh · 7–11 Aug 2026",
  "n_title": ("Let's break down the Technocraft Ventures I-P-O — a two hundred and fifty-two crore issue from a government "
    "infrastructure builder. [pause] We'll cover what the company does, its financials, where the money actually goes, and how "
    "much you'd need to apply as a retail or an H-N-I investor. [pause] This is education, not investment advice."),
  "biz": {"kicker":"WHAT THE COMPANY DOES","title":"Inside Technocraft Ventures","color":"#22D3EE","items":[
    {"emoji":"🏗️","k":"A turnkey EPC builder","v":"Engineering, procurement and construction — builds infrastructure end-to-end, founded back in 1998","chip":"EPC"},
    {"emoji":"💧","k":"Water, roads & urban infra","v":"Water and waste-water systems, roads, urban infrastructure, power distribution and trenchless pipelines","chip":"5 SEGMENTS"},
    {"emoji":"🏛️","k":"Government client base","v":"Mostly state-government projects in UP, Uttarakhand, Rajasthan & Delhi; order book over ₹1,320 Cr","chip":"GOVT ORDERS"},
  ]},
  "n_biz": ("So what does Technocraft Ventures do? [pause] It's an E-P-C contractor — that stands for engineering, procurement and "
    "construction. In plain terms, it builds infrastructure on a turnkey basis. [pause] Its projects span water and waste-water systems, "
    "roads and highways, urban infrastructure, power distribution, and trenchless pipelines — mostly for state governments in Uttar "
    "Pradesh, Uttarakhand, Rajasthan and Delhi. [pause] Founded in nineteen ninety-eight, it rides a strong theme — India's heavy "
    "government spending on water and urban infrastructure. And it carries an order book of over thirteen hundred crore, which gives it "
    "good revenue visibility."),
  "fin": {"kicker":"FY26 FINANCIALS","title":"The Numbers","stats":[
    {"label":"Revenue FY26","to":347,"prefix":"₹","suffix":" Cr","color":"#34D399","sub":"+23% YoY (₹281.00 → ₹347.00 Cr)"},
    {"label":"Net Profit FY26","to":43,"prefix":"₹","suffix":" Cr","color":"#34D399","sub":"+53.6% YoY (₹28.20 → ₹43.32 Cr)"},
    {"label":"Order book","to":1321,"prefix":"₹","suffix":" Cr","color":"#22D3EE","sub":"₹1,320.70 Cr · ~3.8× revenue"}],
    "note":"Solid growth and strong visibility. Valued at ~19× earnings (P/E 19.38) — reasonable for a growing EPC. GMP ~7.78% (unofficial, ₹16.50 over ₹212)."},
  "n_fin": ("Now the financials — and they're solid and improving. [pause] Revenue rose about twenty-three percent, to three hundred and "
    "forty-seven crore in FY twenty twenty-six. But the profit is the standout — net profit jumped fifty-three point six percent, from "
    "twenty-eight point two zero crore to forty-three point three two crore. [pause] Its order book stands at over thirteen hundred and "
    "twenty crore — nearly four times its annual revenue — so a large pipeline of work is already booked. [pause] At the issue price the "
    "stock is valued at about nineteen times earnings, which is reasonable for a growing E-P-C company. The grey-market premium is around "
    "seven point seven eight percent — but remember, that's unofficial and drifts daily."),
  "issue": {"kicker":"WHERE THE MONEY GOES","title":"Fresh Issue vs Offer-for-Sale","stats":[
    {"label":"Total issue","to":252,"prefix":"₹","suffix":" Cr","color":"#22D3EE","sub":"₹251.88 Cr · band ₹200–212"},
    {"label":"Fresh (into company)","to":202,"prefix":"₹","suffix":" Cr","color":"#34D399","sub":"₹201.51 Cr · 80% funds the business"},
    {"label":"OFS (to promoter)","to":50,"prefix":"₹","suffix":" Cr","color":"#F87171","sub":"₹50.37 Cr — promoter part-sells"}],
    "note":"A healthy structure: about 80% is a fresh issue funding the business; only 20% is the promoter, Kartikey Constructions, selling part of its stake."},
  "n_issue": ("Where does your money go? This is the most important question in any I-P-O. [pause] Of the two hundred and fifty-two crore "
    "issue, about two hundred and one and a half crore — roughly eighty percent — is a fresh issue. That's money going into the company. "
    "[pause] The remaining fifty crore is an offer for sale, where the promoter sells a small part of its stake. [pause] So this is a "
    "mostly-fresh issue — four-fifths funds the business, and only a fifth is a promoter cash-out. That's a genuinely healthy structure, "
    "and a good sign."),
  "proceeds": {"kicker":"USE OF THE FRESH MONEY","title":"What the ₹201.5 Cr Funds","color":"#22D3EE","items":[
    {"emoji":"🔄","k":"Bulk — working capital","v":"Most of the fresh money funds working capital — an EPC builder ties up heavy cash in materials and machinery before it gets paid","chip":"GROWTH"},
    {"emoji":"🧰","k":"Balance — general corporate","v":"The remainder goes to general corporate purposes","chip":"GCP"},
    {"emoji":"⏳","k":"Why so much working capital","v":"Government projects pay in stages, so cash gets locked up for months — funding it is what lets the company grow","chip":"WC-HEAVY"},
  ]},
  "n_proceeds": ("What does the fresh money fund? [pause] Almost all of it goes into working capital. [pause] That makes sense for an "
    "E-P-C builder — these projects tie up huge amounts of cash in materials, machinery and payments, long before the government pays the "
    "bills. So growth needs funding. [pause] The rest is for general corporate purposes. [pause] The flip side to watch — a working-"
    "capital-heavy model that depends on government payments means cash can get stuck, and payment delays hurt."),
  "verdict": {"kicker":"SHOULD YOU SUBSCRIBE?","title":"Strengths vs Watch-outs","mythLabel":"⚠️ WATCH-OUTS","factLabel":"✅ STRENGTHS","pairs":[
    {"m":"Depends heavily on government spending","f":"Profit up 53.6%; ~19× earnings — reasonable value"},
    {"m":"Wins work by tendering — can be lumpy","f":"80% fresh — mostly funds the business; low debt"},
    {"m":"Working-capital heavy; payment delays hurt","f":"Order book over ₹1,320 Cr — strong visibility"}],
  },
  "n_verdict": ("Should you subscribe? [pause] The strengths are real — profit grew over fifty-three percent; eighty percent of the "
    "issue is fresh money funding the business; debt is low; the order book of over thirteen hundred crore gives strong visibility; and "
    "at nineteen times earnings the valuation is reasonable. [pause] The watch-outs — it depends heavily on government infrastructure "
    "spending, it wins work through competitive tendering which can be lumpy, and it's a working-capital-hungry business exposed to "
    "payment delays. [pause] The takeaway — a small, clean, mostly-fresh issue with a healthy order book, but a government-dependent "
    "E-P-C model. Understand that dependence before you decide."),
  "retail_min":"₹14,840", "hni_extra":"",
  "n_retail": ("Finally — how do you apply, and how much do you need? [pause] Retail investors can bid up to two lakh rupees for a "
    "thirty-five percent quota, with allotment by lottery if it's oversubscribed — so a bigger cheque doesn't help. [pause] H-N-Is bid "
    "above two lakh for a fifteen percent quota. [pause] For Technocraft, one lot is seventy shares — about fourteen thousand eight "
    "hundred and forty rupees — your minimum. [pause] Track the live subscription on the N-S-E and B-S-E I-P-O pages, Chittorgarh, "
    "Moneycontrol, or your broker app."),
  "recap": {"title":"Technocraft Ventures IPO — at a Glance","items":[
    "Business: government EPC — water, roads, urban infra","FY26: revenue ₹347.00 Cr (+23%), profit ₹43.32 Cr (+53.6%)",
    "₹251.88 Cr issue — 80% fresh, into the company","Order book ₹1,320.70 Cr · P/E ~19; fresh money funds working capital",
    "Retail min ~₹14,840 · GMP ~7.78% (unofficial)"],
    "closer":"Small, clean and mostly-fresh, with a healthy order book — but a government-dependent, working-capital-heavy EPC play. Read the RHP; decide for yourself."},
  "n_recap_pre": ("Let's recap Technocraft Ventures. [pause] A government-focused E-P-C builder — water systems, roads and urban "
    "infrastructure — with a strong order book of over thirteen hundred crore. [pause] In FY twenty twenty-six, revenue rose about "
    "twenty-three percent and profit jumped over fifty-three percent. [pause] The issue is a healthy, mostly-fresh structure — eighty "
    "percent goes into the company, funding working capital, and only twenty percent is a promoter sell-down. [pause] Retail minimum is "
    "about fourteen thousand eight hundred and forty rupees, and the grey-market premium is around eight percent, though that's "
    "unofficial. [pause] "),
},
"leap": {
  "accent": "#A78BFA", "name": "LEAP India IPO", "kicker": "IPO ANALYSIS · MAINBOARD",
  "sub": "Supply-chain asset pooling (KKR-backed) · ₹2,480 Cr · 81% OFS · 7–11 Aug 2026",
  "n_title": ("Let's break down the LEAP India I-P-O — the biggest of this batch, a two thousand four hundred and eighty crore issue "
    "from a K-K-R-backed logistics company. [pause] We'll cover what the company does, its financials, where the money actually goes — "
    "and this one has a very important twist there — and how much you'd need to apply. [pause] This is education, not investment advice."),
  "biz": {"kicker":"WHAT THE COMPANY DOES","title":"Inside LEAP India","color":"#A78BFA","items":[
    {"emoji":"📦","k":"Supply-chain asset pooling","v":"Owns a huge pool of pallets, crates and containers and RENTS them out — customers pay only for what they use","chip":"POOLING"},
    {"emoji":"🔁","k":"A shared, reusable fleet","v":"Asset-light for customers: a circulating fleet of logistics equipment instead of each firm buying its own","chip":"ASSET-LIGHT"},
    {"emoji":"🏢","k":"Market leader, KKR-backed","v":"Calls itself India's largest on-demand pooling company; global investor KKR took a majority stake in 2023","chip":"KKR 2023"},
  ]},
  "n_biz": ("So what does LEAP India do? [pause] It runs a business called supply-chain asset pooling. Instead of a company buying its "
    "own pallets, crates and containers, LEAP owns a huge pool of them and rents them out — pay only for what you use, when you use it. "
    "[pause] Think of it as a shared, circulating fleet of reusable logistics equipment. Its customers are F-M-C-G, logistics, e-commerce "
    "and industrial companies. [pause] It calls itself India's largest on-demand asset-pooling company, and the global investment giant "
    "K-K-R took a majority stake back in twenty twenty-three."),
  "fin": {"kicker":"FY26 FINANCIALS","title":"The Numbers","stats":[
    {"label":"Revenue FY26","to":747,"prefix":"₹","suffix":" Cr","color":"#34D399","sub":"nearly doubled: ₹371.94 → ₹747.36 Cr"},
    {"label":"Net Profit FY26","to":62,"prefix":"₹","suffix":" Cr","color":"#34D399","sub":"+66% YoY (₹37.56 → ₹62.34 Cr)"},
    {"label":"Total borrowings","to":1018,"prefix":"₹","suffix":" Cr","color":"#F87171","sub":"DOUBLED: ₹513.07 → ₹1,017.73 Cr"}],
    "note":"Fast growth — but debt has doubled in two years, and the stock looks richly valued: price-to-book 6.48, and well over 100× earnings."},
  "n_fin": ("Now the financials. [pause] The growth is strong — revenue has nearly doubled in two years, reaching seven hundred and "
    "forty-seven point three six crore in FY twenty twenty-six, up about fifty-four percent in the last year alone. Net profit rose to "
    "sixty-two point three four crore. [pause] But here's the number to watch — borrowings. Debt has doubled, from about five hundred and "
    "thirteen crore to over one thousand and seventeen crore in two years. [pause] And the valuation is rich — a price-to-book of six "
    "point four eight, and, on our estimate from its roughly seven thousand crore value, well over a hundred times earnings. This is "
    "priced for a lot of future growth."),
  "issue": {"kicker":"WHERE THE MONEY GOES","title":"Fresh Issue vs Offer-for-Sale","stats":[
    {"label":"Total issue","to":2480,"prefix":"₹","suffix":" Cr","color":"#A78BFA","sub":"₹2,480 Cr · band ₹151–159"},
    {"label":"Fresh (into company)","to":480,"prefix":"₹","suffix":" Cr","color":"#34D399","sub":"only 19% — into the business"},
    {"label":"OFS (to sellers)","to":2000,"prefix":"₹","suffix":" Cr","color":"#F87171","sub":"81% — to owners incl. KKR"}],
    "note":"The key point: over four-fifths of this ₹2,480 crore issue goes to existing shareholders cashing out — NOT into the business."},
  "n_issue": ("Now, where does your money go? And for this I-P-O, this is the single most important slide. [pause] Of the two thousand "
    "four hundred and eighty crore issue, only four hundred and eighty crore — about nineteen percent — is a fresh issue going into the "
    "company. [pause] The other two thousand crore — a full eighty-one percent — is an offer for sale. That money goes to existing "
    "shareholders selling their stake, including K-K-R, not to the business. [pause] So be very clear-eyed here — this issue is mostly a "
    "cash-out for early investors. Only about a fifth actually strengthens the company."),
  "proceeds": {"kicker":"USE OF THE FRESH MONEY","title":"What the ₹480 Cr Funds","color":"#A78BFA","items":[
    {"emoji":"🏦","k":"₹360 Cr — repay debt","v":"Most of the fresh money repays borrowings — genuinely needed, given debt has doubled to over ₹1,000 Cr","chip":"DEBT"},
    {"emoji":"🧰","k":"Balance — general corporate","v":"The remainder goes to general corporate purposes","chip":"GCP"},
    {"emoji":"⚠️","k":"But most cash exits","v":"Remember: ₹2,000 Cr of the ₹2,480 Cr is OFS — it goes to sellers, and builds nothing new","chip":"OFS 81%"},
  ]},
  "n_proceeds": ("What does that small fresh portion fund? [pause] Of the four hundred and eighty crore of fresh money, three hundred "
    "and sixty crore repays debt — which, given borrowings have doubled, is genuinely needed. [pause] The rest is for general corporate "
    "purposes. [pause] But keep the big picture in view — repaying debt is sensible, yet the overwhelming majority of this issue, that "
    "two thousand crore, simply moves ownership from existing investors to you. It does not build a single new warehouse or add one pallet."),
  "verdict": {"kicker":"SHOULD YOU SUBSCRIBE?","title":"Strengths vs Watch-outs","mythLabel":"⚠️ WATCH-OUTS","factLabel":"✅ STRENGTHS","pairs":[
    {"m":"81% is OFS — mostly a cash-out for owners","f":"Market leader in supply-chain asset pooling"},
    {"m":"Debt has doubled to over ₹1,000 Cr","f":"Revenue nearly doubled in two years"},
    {"m":"Richly valued — P/B 6.48, ~112× earnings","f":"KKR-backed; asset-light model for customers"}],
  },
  "n_verdict": ("Should you subscribe? [pause] The strengths are genuine — LEAP is the market leader in a fast-growing niche, its revenue "
    "has nearly doubled in two years, the pooling model is attractive and asset-light for its customers, and it has the backing and "
    "governance of K-K-R. [pause] The watch-outs are equally real — eighty-one percent of the issue is an offer for sale, so most of your "
    "money goes to sellers, not the company; debt has doubled to over a thousand crore; and the valuation is rich, at more than a hundred "
    "times earnings. [pause] The takeaway — a high-quality, high-growth leader, but an expensive, mostly-cash-out issue. Weigh the quality "
    "against the price and the structure."),
  "retail_min":"₹14,946", "hni_extra":"",
  "n_retail": ("Finally — how do you apply, and how much do you need? [pause] Retail investors can bid up to two lakh rupees for a "
    "thirty-five percent quota, allotted by lottery if it's oversubscribed — so a bigger cheque doesn't help. [pause] H-N-Is bid above "
    "two lakh for a fifteen percent quota. [pause] For LEAP India, one lot is ninety-four shares — about fourteen thousand nine hundred "
    "and forty-six rupees — your minimum. [pause] Track the live subscription on the N-S-E and B-S-E I-P-O pages, Chittorgarh, "
    "Moneycontrol, or your broker app."),
  "recap": {"title":"LEAP India IPO — at a Glance","items":[
    "Business: supply-chain asset pooling — pallets & crates (KKR-backed)","FY26: revenue ₹747.36 Cr, profit ₹62.34 Cr",
    "₹2,480 Cr issue — but 81% is OFS (₹2,000 Cr to sellers)","Fresh ₹480 Cr mainly repays debt",
    "Retail min ~₹14,946 · richly valued (P/B 6.48)"],
    "closer":"A high-growth market leader — but this issue is mostly a promoter and KKR cash-out, at a rich price. Read the RHP; decide for yourself."},
  "n_recap_pre": ("Let's recap LEAP India. [pause] A K-K-R-backed market leader in supply-chain asset pooling — renting out pallets and "
    "crates rather than selling them. [pause] Growth is strong: revenue nearly doubled in two years to seven hundred and forty-seven "
    "crore, with profit of sixty-two crore. [pause] But the structure is the key story — of the two thousand four hundred and eighty "
    "crore issue, eighty-one percent is an offer for sale going to existing owners; only about a fifth is fresh money, and most of that "
    "repays debt. [pause] The minimum retail bid is about fourteen thousand nine hundred and forty-six rupees, and the stock looks richly "
    "valued. [pause] "),
},

# ===== BATCH 5 (8 Aug 2026 — IPOs opening next week, 10–14 Aug 2026) ============================
# Figures per RHP-based reporting (BusinessToday, Business Standard, Outlook Money, IPO Watch,
# InvestorGain, IPOJi, Groww, tradebrains, Whalesbook, IPO Central), triangulated 8 Aug 2026.
# GMP is UNOFFICIAL (IPO Watch, 8 Aug). Peer P/E from each RHP "Basis for Offer Price" peer table
# where one exists; where the RHP says "no listed peer" (Molbio, Behari Lal) or the company is
# loss-making (Shiprocket) the peers scene explains that instead of inventing a P/E.
"dhoot": {
  "accent":"#38BDF8","name":"Dhoot Transmission IPO","kicker":"IPO ANALYSIS · MAINBOARD",
  "sub":"Auto wiring & EV connectors · ₹3,067 Cr · 10–12 Aug 2026",
  "n_title":("Let's break down the Dhoot Transmission I-P-O — one of the largest issues opening next week, at three thousand and "
    "sixty-seven crore rupees. [pause] We'll cover what the company does, its financials, where the money actually goes, how it's priced "
    "against its rivals, and how much you'd need to apply. [pause] Quick note — this is education, not investment advice, and not a tip to buy."),
  "biz":{"kicker":"WHAT THE COMPANY DOES","title":"Inside Dhoot Transmission","color":"#38BDF8","items":[
    {"emoji":"🔌","k":"Auto wiring harnesses","v":"Makes the wiring harnesses and connectors — the electrical nervous system of a vehicle — for two-wheelers, cars and commercial vehicles","chip":"WIRING"},
    {"emoji":"🔋","k":"An EV & premiumisation play","v":"Modern and electric vehicles pack in far more wiring and electronics, so the value of parts per vehicle keeps rising","chip":"EV TAILWIND"},
    {"emoji":"🌍","k":"Scale & exports","v":"Supplies large vehicle makers in India and abroad — a diversified customer base across segments","chip":"OEM SUPPLIER"},
  ]},
  "n_biz":("So what does Dhoot Transmission do? [pause] It makes wiring harnesses and connectors — think of them as the electrical nervous "
    "system of a vehicle, carrying power and signals to every part. It supplies these to makers of two-wheelers, cars and commercial "
    "vehicles. [pause] It's riding a strong theme: modern and electric vehicles use far more wiring and electronics than older ones, so the "
    "value of components per vehicle keeps climbing. [pause] And it sells to large vehicle makers both in India and overseas — a diversified, "
    "sticky customer base."),
  "fin":{"kicker":"FY26 FINANCIALS","title":"The Numbers","stats":[
    {"label":"Revenue FY26","to":4564,"prefix":"₹","suffix":" Cr","color":"#34D399","sub":"+31.33% YoY (≈ ₹4,563.70 Cr)"},
    {"label":"Net Profit FY26","to":397,"prefix":"₹","suffix":" Cr","color":"#34D399","sub":"+12.14% YoY (≈ ₹396.84 Cr)"},
    {"label":"Grey-mkt premium","to":28,"prefix":"~","suffix":"%","color":"#FBBF24","sub":"unofficial · ~₹247 over ₹871"}],
    "note":"Strong growth — revenue up over 31%. Note profit grew slower, up 12%, so margins are under some pressure as it scales."},
  "n_fin":("Now the financials — and they're solid. [pause] Revenue for the year ended March twenty twenty-six was about four thousand five "
    "hundred and sixty-four crore, up a strong thirty-one point three three percent. Net profit was three hundred and ninety-seven crore, "
    "up twelve point one four percent. [pause] Notice profit grew slower than revenue — a sign of some margin pressure as the company scales. "
    "The grey market is pricing a premium near twenty-eight percent, but that's unofficial and drifts daily."),
  "issue":{"kicker":"WHERE THE MONEY GOES","title":"Fresh Issue vs Offer-for-Sale","stats":[
    {"label":"Total issue","to":3067,"prefix":"₹","suffix":" Cr","color":"#38BDF8","sub":"₹3,066.89 Cr · band ₹829–871"},
    {"label":"Fresh (into company)","to":1400,"prefix":"₹","suffix":" Cr","color":"#34D399","sub":"~46% funds the business"},
    {"label":"OFS (to sellers)","to":1667,"prefix":"₹","suffix":" Cr","color":"#F87171","sub":"~54% — existing owners exit"}],
    "note":"A roughly even split — a little over half is an Offer-for-Sale going to existing shareholders; the rest is fresh money."},
  "n_issue":("Here's the most important part of any I-P-O — where does your money go? [pause] Of the three thousand and sixty-seven crore, "
    "about fourteen hundred crore — some forty-six percent — is a fresh issue that goes into the company. [pause] The larger part, about "
    "one thousand six hundred and sixty-seven crore, is an Offer for Sale — existing shareholders selling and pocketing that cash. [pause] "
    "So it's a fairly even split: a little over half is a sell-down, and the rest funds the business."),
  "proceeds":{"kicker":"USE OF THE FRESH MONEY","title":"What the Fresh Money Funds","color":"#38BDF8","items":[
    {"emoji":"🏦","k":"Repay borrowings","v":"A large part of the fresh issue pays down debt — cutting interest costs and strengthening the balance sheet","chip":"DEBT"},
    {"emoji":"🏭","k":"Capacity & growth","v":"The balance supports capital spending and working capital to serve rising EV and premium-vehicle demand","chip":"GROWTH"},
    {"emoji":"🧰","k":"General corporate","v":"A portion is kept for general corporate purposes, the standard catch-all bucket","chip":"GCP"},
  ]},
  "n_proceeds":("What does the fresh money fund? [pause] A large part goes to repaying borrowings, which cuts interest costs and strengthens "
    "the balance sheet. [pause] The rest supports capital spending and working capital, so the company can serve rising demand from electric "
    "and premium vehicles. [pause] And a portion is kept for general corporate purposes. So the fresh money both de-risks the balance sheet "
    "and funds some growth."),
  "peers":{"variant":"sm_peers","props":{"kicker":"COMPETITORS · VALUATION","title":"Cheaper Than Its Auto-Parts Rivals","color":"#38BDF8",
    "peLabel":"P/E (×) · lower = cheaper","rows":[
      {"name":"Dhoot Transmission (this IPO)","pe":44.9,"hi":True,"note":"₹4,564 Cr rev · ROE 16.3%"},
      {"name":"Sona BLW Precision Forgings","pe":74.6,"note":"EV driveline · ~₹4,475 Cr rev · priciest"},
      {"name":"Uno Minda","pe":56.9,"note":"diversified parts · ~₹19,658 Cr rev"},
      {"name":"Motherson Sumi Wiring","pe":43.2,"note":"harness pure-play · ~₹11,478 Cr rev"}],
    "verdict":"Dhoot's ~45× sits below the ~57× peer average — and it earns a higher return on equity (16.3% vs ~11.8%). On the numbers, a cheaper, higher-quality name."},
    "narr":("So how is it priced against its rivals? [pause] At about forty-five times earnings, Dhoot is asking LESS than the peer average "
      "of roughly fifty-seven times. Sona B-L-W trades near seventy-five, Uno Minda around fifty-seven, and Motherson Sumi Wiring about "
      "forty-three. [pause] So Dhoot sits at the cheaper end of the pack — and it earns a higher return on equity, above sixteen percent "
      "versus around twelve for the group. On the numbers, it looks like the better-value, higher-quality name — though remember, these peer "
      "multiples move with the market every day.")},
  "verdict":{"kicker":"SHOULD YOU SUBSCRIBE?","title":"Strengths vs Watch-outs","mythLabel":"⚠️ WATCH-OUTS","factLabel":"✅ STRENGTHS","pairs":[
    {"m":"~54% is OFS — over half is a sell-down","f":"Revenue +31%; priced below the peer average"},
    {"m":"Profit grew slower than sales — margin squeeze","f":"Higher ROE (~16.3%) than its rivals"},
    {"m":"Auto demand is cyclical","f":"EV & premiumisation lift parts per vehicle; GMP ~28%"}],
  },
  "n_verdict":("So — should you subscribe? Let's weigh it honestly. [pause] On the strengths side — revenue is up thirty-one percent, it's "
    "priced below the peer average, and it earns a higher return on equity than its rivals. [pause] On the watch-out side — over half the "
    "issue is a sell-down, profit grew slower than revenue so margins are under pressure, and auto demand is cyclical. [pause] The takeaway "
    "— a cyclical business, but a cheaply-priced, higher-quality one. Go in understanding half your money buys out sellers."),
  "retail_min":"₹14,807", "hni_extra":"",
  "n_retail":("Finally — how do you apply, and how much do you need? [pause] As a retail investor you can bid up to two lakh rupees for a "
    "thirty-five percent quota. If it's oversubscribed, shares are given out by lottery, so a bigger cheque does not get you more. [pause] "
    "H-N-Is bid above two lakh for a fifteen percent quota. [pause] For Dhoot, one lot is seventeen shares — about fourteen thousand eight "
    "hundred and seven rupees — your minimum. [pause] Track the live subscription on the N-S-E and B-S-E I-P-O pages, Chittorgarh, "
    "Moneycontrol, or your broker app."),
  "recap":{"title":"Dhoot Transmission IPO — at a Glance","items":[
    "Business: auto wiring harnesses & EV connectors","FY26: revenue ₹4,563.70 Cr (+31.33%), profit ₹396.84 Cr (+12.14%)",
    "₹3,066.89 Cr issue — ~46% fresh, ~54% OFS","Priced ~44.9× vs ~57× peers — cheaper, higher ROE","Retail min ~₹14,807 · GMP ~28% (unofficial)"],
    "closer":"A cyclical but cheaply-priced, higher-quality auto-parts play. Read the RHP; decide for yourself."},
  "n_recap_pre":("Let's recap Dhoot Transmission. [pause] An auto wiring-harness maker riding the E-V and premiumisation theme, with revenue "
    "up thirty-one percent. [pause] The issue is a roughly even split — forty-six percent fresh, the rest a sell-down. [pause] Crucially, "
    "it's priced around forty-five times earnings, below the fifty-seven times peer average, and with a higher return on equity — cheaper "
    "and better-quality than its rivals. The retail minimum is about fourteen thousand eight hundred rupees, and the grey-market premium is "
    "near twenty-eight percent, though that's unofficial. [pause] "),
},

"molbio": {
  "accent":"#2DD4BF","name":"Molbio Diagnostics IPO","kicker":"IPO ANALYSIS · MAINBOARD",
  "sub":"Point-of-care molecular testing · ₹940 Cr · 10–12 Aug 2026",
  "n_title":("Let's break down the Molbio Diagnostics I-P-O — a nine hundred and forty crore issue from a company with a genuinely unique "
    "product, and an unusual twist when it comes to valuation. [pause] We'll cover what it does, its financials, where the money goes, why "
    "it has no listed peer, and how much you'd need to apply. [pause] This is education, not investment advice."),
  "biz":{"kicker":"WHAT THE COMPANY DOES","title":"Inside Molbio Diagnostics","color":"#2DD4BF","items":[
    {"emoji":"🧬","k":"Truenat molecular testing","v":"Makes 'Truenat' — a portable, PCR-style device that gives lab-grade molecular diagnosis in about an hour, even in remote clinics","chip":"POINT-OF-CARE"},
    {"emoji":"🦠","k":"TB and much more","v":"Widely used for tuberculosis and dozens of other infectious and non-communicable diseases — a made-in-India platform used globally","chip":"MULTI-DISEASE"},
    {"emoji":"🔁","k":"Device + test kits","v":"Sells the machines AND the recurring test cartridges — a razor-and-blade model with a recurring-revenue tail","chip":"RECURRING"},
  ]},
  "n_biz":("So what does Molbio do? [pause] It makes a device called Truenat — a portable, lab-grade molecular testing machine that can "
    "diagnose disease in about an hour, right at the point of care, even in a remote village clinic. [pause] It's best known for "
    "tuberculosis testing, but it runs dozens of other infectious and non-communicable disease tests too. It's a made-in-India platform "
    "used around the world. [pause] And it has a smart model — it sells the machines, and then the recurring test cartridges that go with "
    "them. Razor and blade — a recurring-revenue tail."),
  "fin":{"kicker":"FY26 FINANCIALS","title":"The Numbers","stats":[
    {"label":"Revenue FY26","to":1446,"prefix":"₹","suffix":" Cr","color":"#34D399","sub":"+41.7% YoY (≈ ₹1,445.70 Cr)"},
    {"label":"Net Profit FY26","to":167,"prefix":"₹","suffix":" Cr","color":"#34D399","sub":"+14.8% YoY (≈ ₹166.60 Cr)"},
    {"label":"Grey-mkt premium","to":22,"prefix":"~","suffix":"%","color":"#FBBF24","sub":"unofficial · ~₹180 over ₹807"}],
    "note":"Fast-growing and solidly profitable — revenue up nearly 42%. Profit grew slower as it invests in R&D and capacity."},
  "n_fin":("The financials are strong. [pause] Revenue for FY twenty twenty-six was about one thousand four hundred and forty-six crore, up "
    "nearly forty-two percent. Net profit was around one hundred and sixty-seven crore, up fifteen percent. [pause] So this is a genuinely "
    "profitable, fast-growing business — the profit grew slower than revenue because it's investing in research and capacity. The grey "
    "market premium is near twenty-two percent, but as always, that's unofficial."),
  "issue":{"kicker":"WHERE THE MONEY GOES","title":"Fresh Issue vs Offer-for-Sale","stats":[
    {"label":"Total issue","to":940,"prefix":"₹","suffix":" Cr","color":"#2DD4BF","sub":"₹939.70 Cr · band ₹768–807"},
    {"label":"Fresh (into company)","to":200,"prefix":"₹","suffix":" Cr","color":"#34D399","sub":"~21% funds the business"},
    {"label":"OFS (to sellers)","to":740,"prefix":"₹","suffix":" Cr","color":"#F87171","sub":"~79% — existing investors exit"}],
    "note":"KEY POINT: nearly four-fifths is an Offer-for-Sale — that money goes to selling shareholders, not into the company."},
  "n_issue":("Now — where does your money go? And here's the catch. [pause] Of the nine hundred and forty crore issue, only two hundred "
    "crore — about twenty-one percent — is a fresh issue that goes into the company. [pause] The other seven hundred and forty crore, nearly "
    "eighty percent, is an Offer for Sale — existing investors selling their stakes and cashing out. [pause] So when you apply, most of your "
    "money is buying out people who are exiting, not funding the company's growth."),
  "proceeds":{"kicker":"USE OF THE FRESH MONEY","title":"What the ₹200 Cr Funds","color":"#2DD4BF","items":[
    {"emoji":"🔬","k":"₹105.5 Cr — R&D & centre of excellence","v":"Builds an R&D facility and centre of excellence through subsidiary Bigtec, plus office infrastructure","chip":"R&D"},
    {"emoji":"🏭","k":"₹72.2 Cr — plant & machinery","v":"New equipment for its manufacturing facilities in Goa and Visakhapatnam","chip":"CAPEX"},
    {"emoji":"🧰","k":"Balance — general corporate","v":"The remainder funds general corporate purposes","chip":"GCP"},
  ]},
  "n_proceeds":("That small fresh-issue slice — the two hundred crore — what does it fund? [pause] About a hundred and five crore builds an "
    "R and D facility and a centre of excellence through its subsidiary Bigtec, plus office space. [pause] Another seventy-two crore buys "
    "plant and machinery for its factories in Goa and Visakhapatnam. [pause] The rest is general corporate purposes. So the fresh money is "
    "well spent on research and capacity — there just isn't very much of it, because most of the issue is a sell-down."),
  "peers":{"variant":"sm_iconcards","props":{"kicker":"COMPETITORS · VALUATION","title":"No Listed Twin — Judge With Care","color":"#2DD4BF","items":[
    {"emoji":"🧬","k":"No listed peer (per RHP)","v":"Molbio's own offer document states there is NO comparable listed company — its point-of-care molecular platform is unique on the exchange","chip":"NO PEER"},
    {"emoji":"🏥","k":"The lab chains aren't peers","v":"Dr Lal PathLabs, Metropolis and Thyrocare RUN tests as service chains; Molbio MAKES the testing devices — a different business, not a true peer","chip":"DIFFERENT MODEL"},
    {"emoji":"⚖️","k":"What that means for pricing","v":"With no peer to anchor a P/E, there's no yardstick — so weigh it on growth (+42%) and margins, and be wary of an unchallenged price","chip":"WATCH PRICE"},
  ]},
    "narr":("Now — the competitors, and here Molbio is unusual. [pause] Its own offer document says it has NO listed peer to compare with. "
      "There simply isn't another company like it on the exchange. [pause] People often name Dr Lal PathLabs, Metropolis or Thyrocare — but "
      "those are lab-SERVICE chains that run tests; Molbio MAKES the testing devices. Different business, not a real peer. [pause] The catch: "
      "with no peer, there's no P-E yardstick to tell you whether it's cheap or expensive. So judge it on its growth — revenue up over forty "
      "percent — and its margins, and be a little wary of a price that no rival is keeping honest.")},
  "verdict":{"kicker":"SHOULD YOU SUBSCRIBE?","title":"Strengths vs Watch-outs","mythLabel":"⚠️ WATCH-OUTS","factLabel":"✅ STRENGTHS","pairs":[
    {"m":"~79% is OFS — mostly investors exiting","f":"Fast growth (+42%) & solidly profitable"},
    {"m":"No listed peer — hard to value","f":"Unique made-in-India platform, used globally"},
    {"m":"Priced richly, with no benchmark","f":"Razor-and-blade recurring test-kit revenue; GMP ~22%"}],
  },
  "n_verdict":("Should you subscribe? [pause] The strengths are real — it's a unique, made-in-India platform used globally, it's fast-growing "
    "and profitable, and it has a lovely recurring stream from test kits. [pause] The watch-outs — nearly eighty percent of the issue is "
    "investors cashing out, there's no listed peer so it's hard to value, and it's priced richly with no benchmark to check it against. "
    "[pause] The takeaway — a genuinely impressive company, but mostly a sell-down at a price no peer anchors. Size any bet with that in mind."),
  "retail_min":"₹14,526", "hni_extra":"",
  "n_retail":("How do you apply, and how much do you need? [pause] Retail investors bid up to two lakh for a thirty-five percent quota, with "
    "allotment by lottery if oversubscribed. [pause] H-N-Is go above two lakh for a fifteen percent quota. [pause] For Molbio, one lot is "
    "eighteen shares — about fourteen thousand five hundred and twenty-six rupees — your minimum. [pause] Track the live subscription on the "
    "N-S-E and B-S-E I-P-O pages, Chittorgarh, Moneycontrol, or your broker app."),
  "recap":{"title":"Molbio Diagnostics IPO — at a Glance","items":[
    "Business: Truenat point-of-care molecular diagnostics","FY26: revenue ~₹1,446 Cr (+41.7%), profit ~₹167 Cr (+14.8%)",
    "₹939.70 Cr issue — only ~21% fresh, ~79% OFS","No listed peer per RHP — no P/E benchmark","Retail min ~₹14,526 · GMP ~22% (unofficial)"],
    "closer":"A unique, fast-growing diagnostics innovator — but mostly a sell-down at a price no peer anchors. Read the RHP; decide for yourself."},
  "n_recap_pre":("Let's recap Molbio Diagnostics. [pause] A unique, made-in-India point-of-care testing company behind the Truenat platform, "
    "fast-growing and profitable, with revenue up over forty percent. [pause] But nearly eighty percent of the issue is a sell-down, and it "
    "has no listed peer — so there's no P-E to tell you if the price is fair. [pause] The retail minimum is about fourteen thousand five "
    "hundred and twenty-six rupees, and the grey-market premium is near twenty-two percent, though unofficial. [pause] "),
},

"milkymist": {
  "accent":"#FBBF24","name":"Milky Mist IPO","kicker":"IPO ANALYSIS · MAINBOARD",
  "sub":"Value-added dairy · ₹1,553 Cr · 11–13 Aug 2026",
  "n_title":("Let's break down the Milky Mist I-P-O — a one thousand five hundred and fifty-three crore issue from a well-known dairy brand. "
    "[pause] It has a clean, mostly-fresh structure that sounds great — but wait until you see how it's priced against its rivals. We'll "
    "cover the business, the financials, the money trail, the valuation, and how to apply. [pause] This is education, not investment advice."),
  "biz":{"kicker":"WHAT THE COMPANY DOES","title":"Inside Milky Mist","color":"#FBBF24","items":[
    {"emoji":"🧀","k":"Value-added dairy brand","v":"Best known for paneer, cheese, curd, ghee and yogurt — higher-margin branded products, not just plain milk","chip":"BRANDED"},
    {"emoji":"🐄","k":"Farm-to-fork chain","v":"Procures from farmers and runs its own processing and cold-chain — control over quality and supply","chip":"COLD CHAIN"},
    {"emoji":"🏆","k":"Temasek-backed","v":"Singapore's Temasek is an investor; a strong, trusted brand especially across South India","chip":"BIG BACKER"},
  ]},
  "n_biz":("So what is Milky Mist? [pause] It's a value-added dairy company — best known for paneer, cheese, curd, ghee and yogurt. That "
    "matters, because these branded products earn higher margins than plain milk. [pause] It runs a farm-to-fork chain: it procures from "
    "farmers and operates its own processing and cold-chain, giving it control over quality and supply. [pause] And it has a marquee backer "
    "— Singapore's Temasek is an investor — with a strong, trusted brand especially across South India."),
  "fin":{"kicker":"FY26 FINANCIALS","title":"The Numbers","stats":[
    {"label":"Total income FY26","to":3145,"prefix":"₹","suffix":" Cr","color":"#34D399","sub":"≈ ₹3,145.01 Cr"},
    {"label":"Net Profit FY26","to":127,"prefix":"₹","suffix":" Cr","color":"#34D399","sub":"+142% YoY (≈ ₹127.01 Cr)"},
    {"label":"EBITDA FY26","to":435,"prefix":"₹","suffix":" Cr","color":"#FBBF24","sub":"up from ₹310 Cr in FY25"}],
    "note":"Profit more than DOUBLED in a year — genuinely impressive. But hold that thought; the pricing is rich, as we'll see next."},
  "n_fin":("The financials are strong. [pause] Total income for FY twenty twenty-six was about three thousand one hundred and forty-five "
    "crore, and net profit was a hundred and twenty-seven crore — up a remarkable one hundred and forty-two percent. Operating profit, or "
    "EBITDA, rose to four hundred and thirty-five crore. [pause] So profit more than doubled in a single year — genuinely impressive. But "
    "hold that thought, because how it's priced is the real story, and we'll get to it in a moment."),
  "issue":{"kicker":"WHERE THE MONEY GOES","title":"Fresh Issue vs Offer-for-Sale","stats":[
    {"label":"Total issue","to":1553,"prefix":"₹","suffix":" Cr","color":"#FBBF24","sub":"band ₹133–140"},
    {"label":"Fresh (into company)","to":1428,"prefix":"₹","suffix":" Cr","color":"#34D399","sub":"~92% — funds the business"},
    {"label":"OFS (to sellers)","to":125,"prefix":"₹","suffix":" Cr","color":"#F87171","sub":"~8% — a small sell-down"}],
    "note":"THE GOOD KIND: over 92% is a fresh issue — the money goes INTO the company, not to exiting owners."},
  "n_issue":("Now — where does your money go? And here Milky Mist looks great. [pause] Of the one thousand five hundred and fifty-three crore "
    "issue, about one thousand four hundred and twenty-eight crore — over ninety-two percent — is a fresh issue that goes into the company. "
    "[pause] Only about a hundred and twenty-five crore is an Offer for Sale — a small sell-down. [pause] So this is the good kind of I-P-O "
    "in structure: your money is funding the business's growth, not buying out people who are leaving."),
  "proceeds":{"kicker":"USE OF THE FRESH MONEY","title":"What the ₹1,428 Cr Funds","color":"#FBBF24","items":[
    {"emoji":"🏦","k":"₹496.8 Cr — repay borrowings","v":"The largest single use pays down debt, cutting interest costs and strengthening the balance sheet","chip":"DEBT"},
    {"emoji":"🏭","k":"Capex — Perundurai plant","v":"Expansion and modernisation of its Perundurai manufacturing facility to grow capacity","chip":"CAPACITY"},
    {"emoji":"🧰","k":"Working capital + GCP","v":"The rest funds working capital and general corporate purposes","chip":"WC"},
  ]},
  "n_proceeds":("So what does the fresh money fund? [pause] The largest single use — about four hundred and ninety-seven crore — repays debt, "
    "cutting interest costs and strengthening the balance sheet. [pause] A chunk goes to expanding and modernising its Perundurai "
    "manufacturing facility, adding real capacity. [pause] And the rest funds working capital and general corporate purposes. So unlike a "
    "pure sell-down, this money genuinely goes to work inside the business."),
  "peers":{"variant":"sm_peers","props":{"kicker":"COMPETITORS · VALUATION","title":"Priced Above the Entire Dairy Pack","color":"#FBBF24",
    "peLabel":"P/E (×) · higher = pricier","rows":[
      {"name":"Milky Mist (this IPO)","pe":84.9,"hi":True,"note":"~₹10,778 Cr mcap ÷ ₹127 Cr PAT"},
      {"name":"Hatsun Agro","pe":58.2,"note":"leader · ~₹20,283 Cr mcap"},
      {"name":"Dodla Dairy","pe":24.3,"note":"South-India dairy · branded"},
      {"name":"Parag Milk Foods","pe":21.3,"note":"cheese & value-added · cheapest"}],
    "verdict":"At ~85× earnings, Milky Mist is asking MORE than every listed dairy peer — pricier even than market-leader Hatsun (~58×). A steep premium for its growth."},
    "narr":("So how is it priced against rivals? This is the number to sit with. [pause] At the top of the band, Milky Mist is valued near "
      "ten thousand eight hundred crore — about eighty-five times its earnings. [pause] Compare that with listed dairy peers: Hatsun Agro, "
      "the market leader, trades near fifty-eight times; Dodla Dairy around twenty-four; and Parag Milk Foods about twenty-one. [pause] In "
      "other words, Milky Mist is asking MORE than every one of them — pricier even than the leader. The growth is real, with profit more "
      "than doubling — but you're paying a full, premium price for it, so the margin for error is thin.")},
  "verdict":{"kicker":"SHOULD YOU SUBSCRIBE?","title":"Strengths vs Watch-outs","mythLabel":"⚠️ WATCH-OUTS","factLabel":"✅ STRENGTHS","pairs":[
    {"m":"Priced ~85× — above EVERY listed peer","f":"Profit more than doubled (+142%)"},
    {"m":"Dairy is milk-cost sensitive; margins swing","f":"~92% fresh — money funds the business"},
    {"m":"Listed dairy peers are all down in 2026","f":"Strong brand; Temasek-backed; cold-chain moat"}],
  },
  "n_verdict":("So — should you subscribe? [pause] The strengths are attractive — profit more than doubled, over ninety percent is fresh "
    "money funding the company, and it's a trusted, Temasek-backed brand with a real cold-chain moat. [pause] The watch-outs are just as "
    "important — it's priced above every single listed dairy peer, dairy margins swing with milk costs, and the listed peers are all down "
    "this year. [pause] The takeaway — a lovely, cleanly-structured business, but you're paying a premium price above the whole pack. Only "
    "you can decide if the growth justifies it."),
  "retail_min":"₹14,980", "hni_extra":"",
  "n_retail":("Finally — how do you apply, and how much? [pause] Retail investors bid up to two lakh for a thirty-five percent quota, with "
    "allotment by lottery if oversubscribed. [pause] H-N-Is bid above two lakh for a fifteen percent quota. [pause] For Milky Mist, one lot "
    "is a hundred and seven shares — about fourteen thousand nine hundred and eighty rupees — your minimum. [pause] Track the live "
    "subscription on the N-S-E and B-S-E I-P-O pages, Chittorgarh, Moneycontrol, or your broker app."),
  "recap":{"title":"Milky Mist IPO — at a Glance","items":[
    "Business: value-added dairy — paneer, cheese, curd, ghee","FY26: income ₹3,145.01 Cr, profit ₹127.01 Cr (+142%)",
    "₹1,553 Cr issue — ~92% FRESH (the good kind)","But priced ~85× — above every listed dairy peer","Retail min ~₹14,980 · GMP ~19% (unofficial)"],
    "closer":"A fast-growing, cleanly-structured dairy brand — at a premium price above all its peers. Read the RHP; decide for yourself."},
  "n_recap_pre":("Let's recap Milky Mist. [pause] A well-known value-added dairy brand — paneer, cheese, ghee — that's Temasek-backed, with "
    "profit more than doubling. [pause] The structure is clean: over ninety percent is fresh money funding the company. [pause] But the "
    "catch is the price — about eighty-five times earnings, above every listed dairy peer, even the market leader. The retail minimum is "
    "about fourteen thousand nine hundred and eighty rupees, and the grey-market premium is near nineteen percent, though unofficial. [pause] "),
},

"shiprocket": {
  "accent":"#A78BFA","name":"Shiprocket IPO","kicker":"IPO ANALYSIS · MAINBOARD",
  "sub":"E-commerce logistics platform · ₹1,617 Cr · 12–14 Aug 2026",
  "n_title":("Let's break down the Shiprocket I-P-O — a one thousand six hundred and seventeen crore issue from a well-known e-commerce "
    "logistics platform. [pause] There's one thing that makes valuing this company different from the others this week — it doesn't yet make "
    "a profit. We'll cover the business, the financials, the money trail, how it compares to rivals, and how to apply. [pause] This is "
    "education, not investment advice."),
  "biz":{"kicker":"WHAT THE COMPANY DOES","title":"Inside Shiprocket","color":"#A78BFA","items":[
    {"emoji":"📦","k":"E-commerce shipping platform","v":"A software layer that lets online sellers ship through 17+ courier partners from one dashboard — it owns no trucks itself","chip":"ASSET-LIGHT"},
    {"emoji":"🛒","k":"Full seller toolkit","v":"Shipping, checkout, returns, packaging and financing for D2C brands and small online sellers","chip":"SELLER SUITE"},
    {"emoji":"📈","k":"Rides D2C growth","v":"Grows with India's small online sellers — a picks-and-shovels play on e-commerce, not a single store","chip":"E-COM TAILWIND"},
  ]},
  "n_biz":("So what does Shiprocket do? [pause] It's a software platform that helps online sellers ship their orders. From one dashboard, a "
    "seller can pick from more than seventeen courier partners — but Shiprocket itself owns no trucks or warehouses. It's asset-light. "
    "[pause] Around that, it offers a full toolkit — checkout, returns, packaging, even financing — for small online sellers and D2C brands. "
    "[pause] So it's a picks-and-shovels play on India's e-commerce boom: it grows as the number of small online sellers grows, rather than "
    "betting on any single store."),
  "fin":{"kicker":"FY26 FINANCIALS","title":"The Numbers","stats":[
    {"label":"Revenue FY26","to":2024,"prefix":"₹","suffix":" Cr","color":"#34D399","sub":"+24% YoY (≈ ₹2,024.1 Cr)"},
    {"label":"Net loss FY26","to":79,"prefix":"−₹","suffix":" Cr","color":"#F87171","sub":"was −₹595 Cr in FY24"},
    {"label":"Grey-mkt premium","to":14,"prefix":"~","suffix":"%","color":"#FBBF24","sub":"unofficial · ~₹14 over ₹97"}],
    "note":"Revenue up 24% and losses cut dramatically — from ₹595 Cr in FY24 to ₹79 Cr. But it is still NOT profitable."},
  "n_fin":("Now the financials, and this is the key part. [pause] Revenue for FY twenty twenty-six was about two thousand and twenty-four "
    "crore, up twenty-four percent. [pause] But the company is still loss-making — it lost about seventy-nine crore. The good news is how "
    "sharply that loss has shrunk: from a huge five hundred and ninety-five crore loss two years ago, to seventy-nine crore now. [pause] So "
    "the trend is strongly in the right direction — but remember, it does not yet make a profit, and that changes how you value it."),
  "issue":{"kicker":"WHERE THE MONEY GOES","title":"Fresh Issue vs Offer-for-Sale","stats":[
    {"label":"Total issue","to":1617,"prefix":"₹","suffix":" Cr","color":"#A78BFA","sub":"₹1,617.5 Cr · band ₹92–97"},
    {"label":"Fresh (into company)","to":886,"prefix":"₹","suffix":" Cr","color":"#34D399","sub":"~55% funds the business"},
    {"label":"OFS (to sellers)","to":732,"prefix":"₹","suffix":" Cr","color":"#F87171","sub":"~45% — early investors exit"}],
    "note":"A fairly balanced split — a little over half is fresh money; the rest lets early backers sell down."},
  "n_issue":("Where does your money go? [pause] Of the one thousand six hundred and seventeen crore issue, about eight hundred and eighty-six "
    "crore — some fifty-five percent — is a fresh issue that goes into the company. [pause] The remaining seven hundred and thirty-two crore "
    "is an Offer for Sale, where early investors sell part of their stake. [pause] So it's a fairly balanced split — a little over half is "
    "fresh money for the business, and the rest lets early backers take some money off the table."),
  "proceeds":{"kicker":"USE OF THE FRESH MONEY","title":"What the Fresh Money Funds","color":"#A78BFA","items":[
    {"emoji":"📣","k":"Marketing & technology","v":"Fresh money funds marketing and technology across its core and emerging businesses to keep growing","chip":"GROWTH"},
    {"emoji":"🤝","k":"Acquisitions & debt","v":"Part is kept for potential acquisitions and to repay some borrowings","chip":"M&A / DEBT"},
    {"emoji":"🧰","k":"General corporate","v":"The remainder is for general corporate purposes","chip":"GCP"},
  ]},
  "n_proceeds":("What does the fresh money fund? [pause] The main use is marketing and technology, across both its core shipping business and "
    "newer lines — the fuel it needs to keep growing and, hopefully, reach profit. [pause] Part is set aside for potential acquisitions and "
    "to repay some borrowings. [pause] And the rest is general corporate purposes. So the money is aimed squarely at growth — which is what a "
    "company still chasing profitability needs."),
  "peers":{"variant":"sm_iconcards","props":{"kicker":"COMPETITORS · VALUATION","title":"Loss-Making — Judged on Sales, Not P/E","color":"#A78BFA","items":[
    {"emoji":"🚚","k":"Delhivery — the listed benchmark","v":"India's largest logistics firm (~₹25,000 Cr+). But it OWNS trucks, hubs and warehouses; Shiprocket is asset-light, aggregating 17 couriers","chip":"ASSET-HEAVY"},
    {"emoji":"🧩","k":"A crowded field","v":"Unicommerce (listed e-commerce enablement) plus unlisted Xpressbees, Shadowfax and others chase the same sellers","chip":"CROWDED"},
    {"emoji":"📉","k":"No P/E — it loses money","v":"With a net loss, there's no P/E. It's valued on price-to-SALES — about ₹7,000 Cr ÷ ₹2,024 Cr, near 3.5× — and on its shrinking losses","chip":"~3.5× SALES"},
  ]},
    "narr":("Now the competitors — and here the maths is different, because Shiprocket loses money, so there's no P-E to quote. [pause] Its "
      "main listed benchmark is Delhivery, India's largest logistics company, worth over twenty-five thousand crore. But Delhivery OWNS the "
      "trucks, hubs and warehouses; Shiprocket is asset-light — it just aggregates seventeen courier partners under one dashboard. [pause] "
      "It also competes with the listed enabler Unicommerce, and unlisted names like Xpressbees and Shadowfax — a crowded field. [pause] "
      "Because it's loss-making, investors value it on price-to-SALES — roughly three and a half times revenue at its seven-thousand-crore "
      "price — and on how fast those losses are shrinking, from nearly six hundred crore down to under eighty.")},
  "verdict":{"kicker":"SHOULD YOU SUBSCRIBE?","title":"Strengths vs Watch-outs","mythLabel":"⚠️ WATCH-OUTS","factLabel":"✅ STRENGTHS","pairs":[
    {"m":"Still loss-making (−₹79 Cr) — no P/E","f":"Revenue +24%; losses cut ~88% since FY24"},
    {"m":"Crowded, competitive market","f":"Asset-light, scalable software model"},
    {"m":"~45% is OFS; valued on sales, not profit","f":"Picks-and-shovels play on D2C; ~55% fresh"}],
  },
  "n_verdict":("Should you subscribe? [pause] The strengths — revenue up twenty-four percent, losses cut by nearly ninety percent in two "
    "years, and an asset-light, scalable model that rides the whole D2C wave. [pause] The watch-outs — it's still loss-making, so there's no "
    "P-E; the market is crowded and competitive; and about forty-five percent is a sell-down, with the company valued on sales rather than "
    "profit. [pause] The takeaway — a fast-improving, asset-light platform with a real path to profit, but not there yet. Judge it as a "
    "growth bet, not a value one."),
  "retail_min":"₹14,938", "hni_extra":"",
  "n_retail":("How do you apply, and how much do you need? [pause] Retail investors bid up to two lakh for a thirty-five percent quota, with "
    "allotment by lottery if oversubscribed. [pause] H-N-Is go above two lakh for a fifteen percent quota. [pause] For Shiprocket, one lot is "
    "a hundred and fifty-four shares — about fourteen thousand nine hundred and thirty-eight rupees — your minimum. [pause] Track the live "
    "subscription on the N-S-E and B-S-E I-P-O pages, Chittorgarh, Moneycontrol, or your broker app."),
  "recap":{"title":"Shiprocket IPO — at a Glance","items":[
    "Business: asset-light e-commerce shipping platform","FY26: revenue ₹2,024.1 Cr (+24%), net loss −₹79.2 Cr",
    "₹1,617.5 Cr issue — ~55% fresh, ~45% OFS","Loss-making → valued on ~3.5× sales, not P/E","Retail min ~₹14,938 · GMP ~14% (unofficial)"],
    "closer":"A fast-scaling, asset-light platform with narrowing losses — but not yet profitable, priced on sales. Read the RHP; decide for yourself."},
  "n_recap_pre":("Let's recap Shiprocket. [pause] An asset-light e-commerce shipping platform — a picks-and-shovels play on D2C, with revenue "
    "up twenty-four percent and losses cut sharply. [pause] The issue is about fifty-five percent fresh, the rest a sell-down. [pause] The "
    "key point — it's still loss-making, so there's no P-E; it's valued on sales, near three and a half times revenue, and against listed "
    "Delhivery. The retail minimum is about fourteen thousand nine hundred and thirty-eight rupees, and the grey-market premium is near "
    "fourteen percent, though unofficial. [pause] "),
},

"beharilal": {
  "accent":"#F97316","name":"Behari Lal Engineering IPO","kicker":"IPO ANALYSIS · MAINBOARD",
  "sub":"Metal rolls manufacturer · ₹302 Cr · 12–14 Aug 2026",
  "n_title":("Let's break down the Behari Lal Engineering I-P-O — the smallest mainboard issue of next week, at about three hundred and two "
    "crore, from a niche engineering company. [pause] It has an unusual feature — no listed peer — but a surprisingly modest price. We'll "
    "cover the business, the financials, the money trail, the valuation, and how to apply. [pause] This is education, not investment advice."),
  "biz":{"kicker":"WHAT THE COMPANY DOES","title":"Inside Behari Lal Engineering","color":"#F97316","items":[
    {"emoji":"🛠️","k":"Makes metal & steel rolls","v":"One of India's largest makers of metal rolls — the heavy rollers used inside steel and metal-processing mills","chip":"METAL ROLLS"},
    {"emoji":"🏗️","k":"Custom engineering","v":"Customised, engineered products for industrial customers — a niche capital-goods business, founded back in 1995","chip":"NICHE"},
    {"emoji":"📊","k":"Sizeable share","v":"Estimated to serve around 10 to 11 percent of domestic metal-roll demand in FY26","chip":"~10–11% SHARE"},
  ]},
  "n_biz":("So what does Behari Lal do? [pause] It's one of India's largest makers of metal rolls — the big, heavy rollers used inside steel "
    "and metal-processing mills to shape metal. [pause] It's a customised, engineered business, making products to order for industrial "
    "customers, and it's been around since nineteen ninety-five. [pause] It's a genuine niche leader — estimated to serve about ten to "
    "eleven percent of domestic metal-roll demand. But keep in mind, its fortunes are tied to the industrial and steel capital-expenditure "
    "cycle."),
  "fin":{"kicker":"FY26 FINANCIALS","title":"The Numbers","stats":[
    {"label":"Revenue FY26","to":547,"prefix":"₹","suffix":" Cr","color":"#34D399","sub":"≈ ₹546.52 Cr (+5.9%)"},
    {"label":"Net Profit FY26","to":65,"prefix":"₹","suffix":" Cr","color":"#34D399","sub":"≈ ₹64.64 Cr (+22%)"},
    {"label":"Grey-mkt premium","to":11,"prefix":"~","suffix":"%","color":"#FBBF24","sub":"unofficial · ~₹30 over ₹285"}],
    "note":"Revenue growth is modest at ~6%, but profit jumped 22% — margins are improving. A steady, profitable niche maker."},
  "n_fin":("The financials are steady. [pause] Revenue for FY twenty twenty-six was about five hundred and forty-seven crore, up a modest "
    "six percent. But net profit jumped twenty-two percent to around sixty-five crore — so margins are improving nicely. [pause] It's a "
    "profitable, well-run niche business rather than a fast grower. The grey market premium is near ten to eleven percent, the most modest "
    "of the mainboard names this week — and of course, unofficial."),
  "issue":{"kicker":"WHERE THE MONEY GOES","title":"Fresh Issue vs Offer-for-Sale","stats":[
    {"label":"Total issue","to":302,"prefix":"₹","suffix":" Cr","color":"#F97316","sub":"₹301.62 Cr · band ₹271–285"},
    {"label":"Fresh (into company)","to":93,"prefix":"₹","suffix":" Cr","color":"#34D399","sub":"~31% funds the business"},
    {"label":"OFS (to sellers)","to":209,"prefix":"₹","suffix":" Cr","color":"#F87171","sub":"~69% — promoters part-exit"}],
    "note":"Mostly an Offer-for-Sale — about seven-tenths goes to selling promoters, not into the company."},
  "n_issue":("Where does your money go? [pause] Of the roughly three hundred and two crore issue, only about ninety-three crore — thirty-one "
    "percent — is a fresh issue going into the company. [pause] The larger part, about two hundred and nine crore, is an Offer for Sale — the "
    "promoters selling part of their stake and pocketing that cash. [pause] So it's mostly a sell-down: around seven-tenths of your money "
    "buys out existing owners, rather than funding the business."),
  "proceeds":{"kicker":"USE OF THE FRESH MONEY","title":"What the Fresh Money Funds","color":"#F97316","items":[
    {"emoji":"🏭","k":"Capacity & equipment","v":"The fresh money largely funds capital expenditure and capacity for its manufacturing operations","chip":"CAPEX"},
    {"emoji":"🔄","k":"Working capital","v":"Supports working capital, which a heavy, made-to-order engineering business ties up","chip":"WC"},
    {"emoji":"🧰","k":"General corporate","v":"The balance is for general corporate purposes","chip":"GCP"},
  ]},
  "n_proceeds":("What does the fresh slice fund? [pause] Largely capital expenditure and capacity for its manufacturing operations. [pause] "
    "It also supports working capital — a made-to-order engineering business ties up a lot of cash in orders and inventory. [pause] And the "
    "balance is general corporate purposes. So the fresh money is put to sensible, growth-oriented use — there just isn't much of it, since "
    "most of the issue is a promoter sell-down."),
  "peers":{"variant":"sm_iconcards","props":{"kicker":"COMPETITORS · VALUATION","title":"No Listed Peer — But Priced Modestly","color":"#F97316","items":[
    {"emoji":"🛠️","k":"No listed peer (per RHP)","v":"The offer document lists no directly comparable company — metal-roll makers are a niche with few pure-play listed names","chip":"NO PEER"},
    {"emoji":"⚖️","k":"No clean P/E comparison","v":"Broader steel-products and engineering firms exist, but none matches its rolls focus, so a like-for-like P/E isn't available","chip":"NICHE"},
    {"emoji":"💰","k":"But the price looks modest","v":"At the ₹285 upper band it's asking about 17× FY26 earnings — modest versus many recent IPOs, though the lack of a peer makes benchmarking harder","chip":"~17× P/E"},
  ]},
    "narr":("Now — the competitors. Like Molbio, Behari Lal says in its offer document that it has no directly comparable listed company. "
      "[pause] Metal rolls are a narrow niche; there are broader steel-products and engineering firms, but none is a true like-for-like peer, "
      "so there's no clean P-E to compare against. [pause] The good news is the price itself looks modest — at the top of the band it's asking "
      "only about seventeen times its earnings, which is cheap next to many recent I-P-Os. [pause] Just remember, without a peer, that word "
      "'cheap' has nothing solid to be measured against — so lean on the business quality and the modest multiple, not a comparison.")},
  "verdict":{"kicker":"SHOULD YOU SUBSCRIBE?","title":"Strengths vs Watch-outs","mythLabel":"⚠️ WATCH-OUTS","factLabel":"✅ STRENGTHS","pairs":[
    {"m":"~69% is OFS — mostly a promoter exit","f":"Profit +22%; margins improving"},
    {"m":"No listed peer — hard to benchmark","f":"Modest ~17× valuation"},
    {"m":"Slow revenue growth (~6%); cyclical demand","f":"Niche leader (~10–11% share); profitable since 1995"}],
  },
  "n_verdict":("Should you subscribe? [pause] The strengths — it's a profitable niche leader with improving margins, it's been around since "
    "the nineties, and it's modestly priced at about seventeen times earnings. [pause] The watch-outs — about seventy percent is a promoter "
    "sell-down, there's no listed peer to benchmark against, and revenue growth is slow in a cyclical industry. [pause] The takeaway — a "
    "solid, cheaply-priced niche business, but mostly a cash-out with no peer to check the price. Judge it on the business, not a comparison."),
  "retail_min":"₹14,820", "hni_extra":"",
  "n_retail":("How do you apply, and how much do you need? [pause] Retail investors bid up to two lakh for a thirty-five percent quota, with "
    "allotment by lottery if oversubscribed. [pause] H-N-Is go above two lakh for a fifteen percent quota. [pause] For Behari Lal, one lot is "
    "fifty-two shares — about fourteen thousand eight hundred and twenty rupees — your minimum. [pause] Track the live subscription on the "
    "N-S-E and B-S-E I-P-O pages, Chittorgarh, Moneycontrol, or your broker app."),
  "recap":{"title":"Behari Lal Engineering IPO — at a Glance","items":[
    "Business: one of India's largest metal-roll makers","FY26: revenue ₹546.52 Cr (+5.9%), profit ₹64.64 Cr (+22%)",
    "₹301.62 Cr issue — only ~31% fresh, ~69% OFS","No listed peer per RHP — but a modest ~17× price","Retail min ~₹14,820 · GMP ~10.5% (unofficial)"],
    "closer":"A profitable niche leader at a modest price — but mostly a promoter sell-down with no peer to benchmark. Read the RHP; decide for yourself."},
  "n_recap_pre":("Let's recap Behari Lal Engineering. [pause] One of India's largest metal-roll makers — a profitable niche leader with "
    "improving margins, though slow revenue growth. [pause] The issue is mostly a promoter sell-down, only about a third fresh. [pause] It "
    "has no listed peer, but it's modestly priced at around seventeen times earnings — cheap by recent standards. The retail minimum is "
    "about fourteen thousand eight hundred and twenty rupees, and the grey-market premium is near ten percent, though unofficial. [pause] "),
},
# ============================================================================================
# BATCH 6 — mainboard IPOs opening the week of 17–23 Aug 2026 (figures triangulated 14 Aug 2026
# across IPO Watch, businessoutreach, indiaipo, ipocentral, ipoplatform, BusinessToday, Business
# Standard, Outlook Business, Free Press Journal, Upstox, Groww, Chittorgarh summaries). GMP is
# UNOFFICIAL. New: full THREE-STATEMENT beat (sm_financials). Public IPO summaries publish the
# income statement + balance sheet but NOT the full cash-flow statement — that column shows the
# known financing flows (fresh raise + primary use) and marks operating CFO "Not disclosed" (honest).
#
#  horizon  — Horizon Industrial Parks, ₹2,600 Cr, 17–19 Aug (list 24 Aug). Blackstone ~89%,
#             Radhakishan-Damani-linked. Industrial/logistics real estate: 45 assets, 10 cities,
#             58.01 msf. 100% FRESH, no OFS. Band ₹57–60. Total income FY24→26 ₹245.52 → (FY25 rev
#             ₹390.30) → ₹691.38 Cr (rev ops FY26; total income FY26 ₹767.84 Cr, +77.1%). NET LOSS
#             FY24→26 ₹162.21 → ₹178.70 → ₹203.65 Cr (widening). Total borrowings ₹6,884 Cr (Mar-26).
#             Use: ₹2,250 Cr repay borrowings + GCP. Post-issue mcap ~₹17,298 Cr. Loss-making → P/E n/a
#             (~25× sales — rich). No comparable listed operating peer (Embassy/Nexus/Mindspace are REITs).
#  lalithaa — Lalithaa Jewellery Mart, ₹1,700 Cr = FRESH ₹1,200 Cr (5,97,32,655 sh) + OFS ₹500 Cr
#             (2,48,75,621 sh), 17–19 Aug (list 24 Aug). Band ₹190–201, lot 74, min ₹14,874. South-India
#             jeweller, 56 stores/46 cities. TotIncome FY24/25/26 ₹16,788.05 / ₹16,897.32 / ₹25,023.93 Cr;
#             PAT ₹359.83 / ₹364.73 / ₹1,009.82 Cr; Net worth ₹1,667.78 / ₹2,028.80 / ₹3,033.14 Cr; Total
#             assets ₹5,182.26 / ₹6,929.68 / ₹10,945.14 Cr; Borrowings ₹824.18 / ₹949.26 / ₹1,604.14 Cr.
#             ROE 41.60%, ROCE 42.60%, D/E 0.53, PAT margin 4.04%. Post-issue P/E ~11.1× (ipoplatform) vs
#             peer avg 44.2× — Kalyan 46.85×, Thangamayil 46.26×, PN Gadgil 22.18×, Senco 11.5×, PC Jeweller
#             9.26×, Manoj Vaibhav 7.12×. GMP ~₹25 (~12.44%, unofficial). Promoter 97.72%→82.85%.
#  shankesh — Shankesh Jewellers, ₹367.18 Cr = FRESH ₹274.18 Cr (2,94,82,000 sh) + OFS ₹93.00 Cr
#             (1,00,00,000 sh, promoters Kantilal & Manoj Jain), 18–20 Aug (list 25 Aug). Band ₹88–93.
#             Mumbai B2B ASSET-LIGHT handcrafted 22/18k gold jewellery; no in-house mfg, 72 jobworkers.
#             TotIncome FY24/25/26 ₹1,061.91 / ₹1,403.94 / ₹1,630.93 Cr; PAT ₹12.82 / ₹40.31 / ₹106.68 Cr
#             (+164.6% FY26); margin 6.54%, ROE 50.94%, ROCE 41.57%. Borrowings ₹167.30 Cr (FY26; ₹242.57
#             Cr by Dec-25). Use: ₹158 Cr repay borrowings + ₹38 Cr WC. No directly comparable listed peer
#             (B2B/asset-light) → competitor landscape, no fabricated peer P/E. GMP ~unofficial.
#  sunshine — Sunshine Pictures, ₹282.14 Cr = FRESH ~₹172.80 Cr (48,00,000 sh) + OFS ~₹109.33 Cr
#             (30,37,000 sh, promoters Vipul Amrutlal Shah & Shefali Shah), 18–20 Aug (anchor 17, list 25).
#             Band ₹342–360. Mumbai film/TV/web production (VFX, DI colour, Dolby Atmos). FY26 TotIncome
#             ₹76.27 Cr (DOWN from FY25 ₹105.80 Cr — lumpy/project-dependent), PAT ₹40.02 Cr (FY25 ₹34.46
#             Cr), EBITDA FY25 ₹50.76 Cr; net worth ₹145.13 Cr, borrowings ₹9.09 Cr, D/E 0.06. Of fresh:
#             ₹112.50 Cr → long-term WC + GCP. Post-issue mcap ~₹1,121 Cr → P/E ~32.55× (demanding on
#             lumpy earnings). Scarce clean listed production peer → competitor landscape.
#  gaja     — Gaja Alternative Asset Management (Gaja Capital), ₹550 Cr = FRESH ₹450 Cr (2.81 cr sh) +
#             OFS ₹100 Cr (0.63 cr sh), 19–21 Aug (list 26 Aug). Band ₹152–160. India's FIRST home-grown
#             PE/AIF manager to list; founded 1999, Mumbai; Cat I & II AIFs + offshore advisory. FY26 total
#             income ₹157.80 Cr (+28%, FY25 ₹123.28 Cr), PAT ₹79.60 Cr (+33.8%, FY25 ₹59.50 Cr), margin
#             ~51.94%. Borrowings ₹41.56 Cr (FY25 ₹4.00 Cr), D/E 0.07; sponsor commitments ~₹274 Cr. Use:
#             ₹372 Cr sponsor commitments to funds + bridge-loan repay. Post-issue mcap ~₹2,256 Cr → P/E
#             ~28×. No listed pure-PE-AMC peer (MF AMCs HDFC/Nippon are a different model) → competitor beat.
#  Note: operating cash-flow (CFO) line items are NOT in the public IPO summaries used here → shown as
#  "Not disclosed" in the cash-flow column, with the known financing flows filled in. Lot/min for the four
#  non-Lalithaa issues stated as "about ₹15,000" (SEBI retail-min design) rather than a fabricated exact lot.
# ============================================================================================
"horizon": {
  "accent":"#38BDF8","name":"Horizon Industrial Parks IPO","kicker":"IPO ANALYSIS · MAINBOARD",
  "sub":"Warehousing & industrial parks · ₹2,600 Cr · 100% Fresh · 17–19 Aug 2026",
  "n_title":("Let's break down the Horizon Industrial Parks I-P-O — a two thousand six hundred crore mainboard issue, and one of the "
    "biggest of this week. [pause] It's a Blackstone-backed warehousing and industrial real-estate company. [pause] We'll cover what it "
    "does, its full financials — income statement, balance sheet and cash flow — where the money goes, how it's valued, and whether it "
    "fits you. [pause] This is education, not investment advice."),
  "biz":{"kicker":"WHAT THE COMPANY DOES","title":"Inside Horizon Industrial Parks","color":"#38BDF8","items":[
    {"emoji":"🏭","k":"Owns warehousing & industrial parks","v":"A platform of grade-A logistics and industrial assets it leases to e-commerce, manufacturing and 3PL tenants","chip":"REAL ESTATE"},
    {"emoji":"📦","k":"45 assets · 10 cities · 58 msf","v":"Around fifty-eight million sq ft of leasable space across ten major Indian cities — a large, national footprint","chip":"SCALE"},
    {"emoji":"🏦","k":"Blackstone-backed (~89%)","v":"Controlled by global giant Blackstone; rides India's warehousing and supply-chain boom","chip":"SPONSOR"},
  ]},
  "n_biz":("So what does Horizon do? [pause] It owns and leases warehousing and industrial parks — the grade-A sheds and logistics "
    "buildings that e-commerce, manufacturers and third-party logistics firms rent. [pause] It's large: about forty-five assets across "
    "ten cities, roughly fifty-eight million square feet of leasable space. [pause] And it's controlled by Blackstone, the global real-"
    "estate giant, with about an eighty-nine percent stake. It rides India's warehousing and supply-chain boom — but note, it's still "
    "loss-making, as we'll see."),
  "fin":{"kicker":"FINANCIALS","title":"The Headline Numbers","stats":[
    {"label":"Revenue FY26","to":691,"prefix":"₹","suffix":" Cr","color":"#34D399","sub":"+77.1% YoY (₹390.30 → ₹691.38 Cr)"},
    {"label":"Net loss FY26","to":204,"prefix":"−₹","suffix":" Cr","color":"#F87171","sub":"loss WIDENED from ₹178.70 Cr"},
    {"label":"Total borrowings","to":6884,"prefix":"₹","suffix":" Cr","color":"#FBBF24","sub":"as of Mar 2026 — heavily leveraged"}],
    "note":"Fast-growing rentals — but still deep in the red, and carrying nearly ₹6,884 Cr of debt. Growth story with a leverage problem."},
  "n_fin":("Now the financials — and here's the tension. [pause] Revenue grew fast — up seventy-seven percent, to about six hundred and "
    "ninety-one crore. [pause] But the company is loss-making: a net loss of about two hundred and four crore in FY twenty twenty-six, "
    "and that loss actually widened from a hundred and seventy-nine crore the year before. [pause] And it's heavily leveraged — total "
    "borrowings near six thousand eight hundred and eighty-four crore. So: strong top-line growth, but red ink and a lot of debt."),
  "threestmt":{"kicker":"FINANCIALS · 3 STATEMENTS","title":"Income, Balance Sheet & Cash Flow","color":"#38BDF8","cols":[
    {"name":"Income Statement","icon":"📊","accent":"#34D399","rows":[
      {"label":"Revenue (ops) FY26","val":"₹691.38 Cr","sub":"FY25 ₹390.30 Cr · +77.1%"},
      {"label":"Total income FY26","val":"₹767.84 Cr"},
      {"label":"Net loss FY26","val":"−₹203.65 Cr","hi":True,"sub":"FY25 −₹178.70 Cr — widening"}]},
    {"name":"Balance Sheet","icon":"🏦","accent":"#FBBF24","rows":[
      {"label":"Total borrowings","val":"₹6,884 Cr","hi":True,"sub":"Mar 2026 — heavily geared"},
      {"label":"Portfolio","val":"58.01 msf","sub":"45 assets · 10 cities"},
      {"label":"Blackstone stake","val":"~89%"}]},
    {"name":"Cash Flow","icon":"💵","accent":"#38BDF8","rows":[
      {"label":"Fresh issue inflow","val":"₹2,600 Cr","sub":"100% fresh — into company"},
      {"label":"→ Repay borrowings","val":"₹2,250 Cr","hi":True,"sub":"~87% of proceeds"},
      {"label":"Operating cash flow","val":"Not disclosed","sub":"rent-led per RHP; read RHP"}]}],
    "note":"Public summaries give the income statement & balance sheet — for the full cash-flow statement, read the RHP."},
  "n_threestmt":("Let's put all three statements together. [pause] The income statement shows revenue near six hundred and ninety-one "
    "crore, but a net loss of about two hundred and four crore that's widening. [pause] The balance sheet is the worry — nearly six "
    "thousand nine hundred crore of borrowings against fifty-eight million square feet of assets. [pause] On the cash-flow side, the "
    "I-P-O brings in two thousand six hundred crore fresh, and about two thousand two hundred and fifty crore of that repays debt. [pause] "
    "The public summaries don't publish the full operating cash-flow line — for that, you read the R-H-P."),
  "issue":{"kicker":"WHERE THE MONEY GOES","title":"Fresh Issue vs Offer-for-Sale","stats":[
    {"label":"Total issue","to":2600,"prefix":"₹","suffix":" Cr","color":"#38BDF8","sub":"band ₹57–60"},
    {"label":"Fresh (into company)","to":2600,"prefix":"₹","suffix":" Cr","color":"#34D399","sub":"100% — every rupee funds the company"},
    {"label":"OFS (to sellers)","to":0,"prefix":"₹","suffix":" Cr","color":"#F87171","sub":"NONE — Blackstone isn't cashing out"}],
    "note":"THE GOOD KIND of structure: 100% fresh — the entire ₹2,600 Cr goes INTO the company, mostly to cut its heavy debt."},
  "n_issue":("Where does your money go? [pause] And on structure, Horizon scores well. [pause] The entire two thousand six hundred crore "
    "is a fresh issue — one hundred percent. There is no Offer for Sale, which means Blackstone and the other owners are not cashing "
    "out; every rupee goes into the company. [pause] That's the good kind of structure. [pause] The catch, of course, is what the money "
    "is for — mostly paying down that big pile of debt."),
  "proceeds":{"kicker":"USE OF THE FRESH MONEY","title":"What the ₹2,600 Cr Funds","color":"#38BDF8","items":[
    {"emoji":"🏦","k":"₹2,250 Cr — repay borrowings","v":"The overwhelming bulk repays debt, cutting interest costs on a heavily-leveraged balance sheet","chip":"DEBT"},
    {"emoji":"⚖️","k":"Deleveraging, not expansion","v":"Even after this, sizeable debt remains — the IPO fixes the balance sheet more than it funds new growth","chip":"CLEAN-UP"},
    {"emoji":"🧰","k":"Balance — general corporate","v":"The remainder goes to general corporate purposes","chip":"GCP"},
  ]},
  "n_proceeds":("What does the fresh money fund? [pause] Overwhelmingly, debt repayment — about two thousand two hundred and fifty crore, "
    "the lion's share, repays borrowings. [pause] So this is primarily a balance-sheet clean-up, not an expansion war-chest. It cuts "
    "interest costs — genuinely helpful — but even afterwards, sizeable debt remains. [pause] The small remainder goes to general "
    "corporate purposes."),
  "peers":{"variant":"sm_iconcards","props":{"kicker":"COMPETITORS · VALUATION","title":"How Is It Priced? No Clean Listed Peer","color":"#38BDF8","items":[
    {"emoji":"🚫","k":"P/E can't be used — it's loss-making","v":"With a net loss, there are no earnings to divide by; the P/E ratio simply doesn't apply here","chip":"P/E n/a"},
    {"emoji":"📐","k":"~25× sales at ₹17,298 Cr value","v":"At the top band the company is valued near ₹17,298 Cr — about 25 times its FY26 revenue. That is a rich price","chip":"PRICEY"},
    {"emoji":"🏢","k":"REIT peers aren't comparable","v":"Embassy, Nexus and Mindspace are REITs — yield instruments that pay out rent; Horizon is a loss-making operating company","chip":"NOT A REIT"},
  ]},
    "narr":("So how is it priced against rivals? [pause] This is where you must be careful. Because it's loss-making, the P/E ratio can't "
      "be used — there are no earnings to divide by. [pause] So look at sales: at the top of the band, Horizon is valued near seventeen "
      "thousand three hundred crore — about twenty-five times its revenue. That is a rich price for a company still in the red. [pause] And "
      "don't confuse it with the listed warehousing REITs like Embassy, Nexus or Mindspace — those are yield instruments that pay out rent. "
      "Horizon is an operating company that isn't yet profitable.")},
  "verdict":{"kicker":"SHOULD YOU SUBSCRIBE?","title":"Strengths vs Watch-outs","mythLabel":"⚠️ WATCH-OUTS","factLabel":"✅ STRENGTHS","pairs":[
    {"m":"Loss-making — and the loss is widening","f":"100% fresh — every rupee funds the company"},
    {"m":"~₹6,884 Cr debt; even post-IPO it's high","f":"Blackstone-backed; large 58-msf national platform"},
    {"m":"~25× sales — a rich price for red ink","f":"Rides India's structural warehousing boom; +77% revenue"}],
  },
  "n_verdict":("So — should you subscribe? [pause] The strengths are real — the whole issue is fresh money, it's backed by Blackstone, it "
    "owns a large fifty-eight-million-square-foot platform, and revenue is growing over seventy-seven percent on a genuine warehousing "
    "boom. [pause] But the watch-outs are serious — the company is loss-making, and the loss is widening; it carries nearly six thousand "
    "nine hundred crore of debt, still high even after the I-P-O; and it's priced at about twenty-five times sales for that red ink. "
    "[pause] The takeaway — a marquee-backed growth platform, but a loss-making, debt-heavy one at a full price. Only you can decide if "
    "the story is worth the risk."),
  "retail_min":"about ₹15,000", "hni_extra":"",
  "n_retail":("Finally — how do you apply, and how much? [pause] Retail investors bid up to two lakh for a thirty-five percent quota, with "
    "allotment by lottery if oversubscribed. [pause] H-N-Is bid above two lakh for a fifteen percent quota. [pause] For Horizon, at a "
    "fifty-seven to sixty rupee band, one lot works out to about fifteen thousand rupees — your minimum. [pause] Track the live "
    "subscription on the N-S-E and B-S-E I-P-O pages, Chittorgarh, Moneycontrol, or your broker app."),
  "recap":{"title":"Horizon Industrial Parks IPO — at a Glance","items":[
    "Business: Blackstone-backed warehousing & industrial parks (45 assets, 58 msf)","FY26: revenue ₹691.38 Cr (+77%), NET LOSS ₹203.65 Cr (widening)",
    "₹2,600 Cr issue — 100% FRESH; mostly repays ₹6,884 Cr debt","Loss-making → P/E n/a; ~25× sales at ~₹17,298 Cr value","Retail min ~₹15,000 · lists 24 Aug"],
    "closer":"A large, marquee-backed warehousing platform on a real boom — but loss-making, debt-heavy and richly priced. Read the RHP; decide for yourself."},
  "n_recap_pre":("Let's recap Horizon Industrial Parks. [pause] A Blackstone-backed warehousing and industrial-parks company — large, "
    "national, and growing revenue over seventy-seven percent. [pause] The issue is one hundred percent fresh, which is good — but the "
    "money mostly repays a heavy debt load near six thousand nine hundred crore. [pause] It's still loss-making, so the P/E doesn't "
    "apply, and at about twenty-five times sales it's richly priced. The retail minimum is about fifteen thousand rupees. [pause] "),
},
"lalithaa": {
  "accent":"#FBBF24","name":"Lalithaa Jewellery Mart IPO","kicker":"IPO ANALYSIS · MAINBOARD",
  "sub":"South-India jewellery chain · ₹1,700 Cr · 17–19 Aug 2026",
  "n_title":("Let's break down the Lalithaa Jewellery Mart I-P-O — a one thousand seven hundred crore mainboard issue from a big South-"
    "India jewellery chain. [pause] And it has one of the most interesting valuation stories of the week. [pause] We'll cover what it "
    "does, its full financials, where the money goes, how it's priced against rivals, and whether it fits you. [pause] This is education, "
    "not investment advice."),
  "biz":{"kicker":"WHAT THE COMPANY DOES","title":"Inside Lalithaa Jewellery Mart","color":"#FBBF24","items":[
    {"emoji":"💍","k":"South-India jewellery retailer","v":"Sells gold, silver and diamond jewellery through large-format stores — a trusted regional brand","chip":"RETAIL"},
    {"emoji":"🏬","k":"56 stores across 46 cities","v":"Spread over Tamil Nadu, Andhra, Telangana, Karnataka and Puducherry — strong in Tier-2 and Tier-3 towns","chip":"56 STORES"},
    {"emoji":"🏆","k":"Best-in-class store economics","v":"Claims the highest operating revenue and EBITDA per store among major organised Indian jewellers","chip":"EFFICIENCY"},
  ]},
  "n_biz":("So what does Lalithaa do? [pause] It's a South-India jewellery retailer — gold, silver and diamond jewellery sold through "
    "large-format showrooms, and a genuinely trusted regional brand. [pause] It has fifty-six stores across forty-six cities, spread "
    "over Tamil Nadu, Andhra, Telangana, Karnataka and Puducherry, with real strength in smaller Tier-2 and Tier-3 towns. [pause] And "
    "its store economics stand out — it claims the highest revenue and profit per store among the major organised jewellers. That "
    "efficiency is the heart of its story."),
  "fin":{"kicker":"FINANCIALS","title":"The Headline Numbers","stats":[
    {"label":"Total income FY26","to":25024,"prefix":"₹","suffix":" Cr","color":"#34D399","sub":"₹25,023.93 Cr (FY25 ₹16,897.32 Cr)"},
    {"label":"Net profit FY26","to":1010,"prefix":"₹","suffix":" Cr","color":"#34D399","sub":"₹1,009.82 Cr · +176.9% YoY"},
    {"label":"Return on equity","to":41.6,"prefix":"","suffix":"%","decimals":1,"color":"#FBBF24","sub":"vs ~21.7% peer average"}],
    "note":"A big jump: income up ~48% and profit nearly tripling to ₹1,009.82 Cr — with a best-in-class 41.60% return on equity."},
  "n_fin":("Now the financials — and they're strong. [pause] Total income jumped to about twenty-five thousand crore in FY twenty twenty-"
    "six, up from around sixteen thousand nine hundred crore. [pause] And net profit nearly tripled — up about a hundred and seventy-"
    "seven percent — to one thousand and ten crore. [pause] Most striking is the return on equity — forty-one point six zero percent, "
    "roughly double the peer average of about twenty-two percent. This is a highly profitable, efficient retailer."),
  "threestmt":{"kicker":"FINANCIALS · 3 STATEMENTS","title":"Income, Balance Sheet & Cash Flow","color":"#FBBF24","cols":[
    {"name":"Income Statement","icon":"📊","accent":"#34D399","rows":[
      {"label":"Total income FY26","val":"₹25,023.93 Cr","sub":"FY25 ₹16,897.32 Cr"},
      {"label":"Net profit FY26","val":"₹1,009.82 Cr","hi":True,"sub":"FY25 ₹364.73 Cr · +176.9%"},
      {"label":"PAT margin","val":"4.04%","sub":"thin, as jewellery is"}]},
    {"name":"Balance Sheet","icon":"🏦","accent":"#FBBF24","rows":[
      {"label":"Net worth FY26","val":"₹3,033.14 Cr","sub":"FY25 ₹2,028.80 Cr"},
      {"label":"Total assets","val":"₹10,945.14 Cr","sub":"inventory-heavy"},
      {"label":"Total borrowings","val":"₹1,604.14 Cr","hi":True,"sub":"D/E 0.53 — moderate"}]},
    {"name":"Cash Flow","icon":"💵","accent":"#38BDF8","rows":[
      {"label":"Fresh issue inflow","val":"₹1,200 Cr","sub":"into the company"},
      {"label":"→ New stores, WC, debt","val":"expansion","hi":True,"sub":"stores + inventory + repay"},
      {"label":"Operating cash flow","val":"Not disclosed","sub":"summary omits it; read RHP"}]}],
    "note":"Income statement & balance sheet look strong; the full cash-flow statement isn't in public summaries — read the RHP."},
  "n_threestmt":("Let's put all three statements together. [pause] The income statement is excellent — twenty-five thousand crore of "
    "income and a thousand crore of profit. [pause] The balance sheet is solid too — net worth of about three thousand crore, total "
    "assets near eleven thousand crore, and moderate borrowings of sixteen hundred crore, a debt-to-equity of just zero point five three. "
    "[pause] On cash flow, the fresh money will fund new stores, working capital for inventory, and some debt repayment. The public "
    "summaries don't print the full operating cash-flow line — for that, read the R-H-P."),
  "issue":{"kicker":"WHERE THE MONEY GOES","title":"Fresh Issue vs Offer-for-Sale","stats":[
    {"label":"Total issue","to":1700,"prefix":"₹","suffix":" Cr","color":"#FBBF24","sub":"band ₹190–201"},
    {"label":"Fresh (into company)","to":1200,"prefix":"₹","suffix":" Cr","color":"#34D399","sub":"~71% — funds growth & debt"},
    {"label":"OFS (to promoters)","to":500,"prefix":"₹","suffix":" Cr","color":"#F87171","sub":"~29% — promoters part-sell"}],
    "note":"A healthy mix: about 71% is fresh money funding the business; ~29% is a promoter sell-down (holding 97.72% → 82.85%)."},
  "n_issue":("Where does your money go? [pause] Of the one thousand seven hundred crore issue, about one thousand two hundred crore — "
    "roughly seventy-one percent — is a fresh issue that goes into the company. [pause] The remaining five hundred crore is an Offer for "
    "Sale, where the promoters sell part of their stake, trimming their holding from about ninety-eight percent to eighty-three percent. "
    "[pause] So it's a healthy, mostly-fresh structure — most of your money funds the business."),
  "proceeds":{"kicker":"USE OF THE FRESH MONEY","title":"What the ₹1,200 Cr Funds","color":"#FBBF24","items":[
    {"emoji":"🏬","k":"New retail stores","v":"Expanding the showroom network — the core growth engine for a store-led jewellery retailer","chip":"EXPANSION"},
    {"emoji":"🏦","k":"Repay borrowings","v":"Cutting debt lowers interest costs and strengthens an already-solid balance sheet","chip":"DEBT"},
    {"emoji":"💎","k":"Working capital + GCP","v":"Funding inventory — gold stock is a jeweller's biggest working-capital need — and general purposes","chip":"INVENTORY"},
  ]},
  "n_proceeds":("What does the fresh money fund? [pause] Three things. First, new retail stores — the core growth engine for a store-led "
    "jeweller. [pause] Second, repaying borrowings, which cuts interest costs. [pause] And third, working capital — because gold "
    "inventory is a jeweller's single biggest working-capital need — plus general corporate purposes. So the money genuinely goes to "
    "work funding growth."),
  "peers":{"variant":"sm_peers","props":{"kicker":"COMPETITORS · VALUATION","title":"Priced Well Below the Big Jewellers","color":"#FBBF24",
    "peLabel":"P/E (×) · higher = pricier","rows":[
      {"name":"Kalyan Jewellers","pe":46.9,"note":"national organised leader"},
      {"name":"Thangamayil","pe":46.3,"note":"Tamil Nadu jeweller"},
      {"name":"PN Gadgil","pe":22.2,"note":"western India · recent IPO"},
      {"name":"Senco Gold","pe":11.5,"note":"east India · value-priced"},
      {"name":"Lalithaa (this IPO)","pe":11.1,"hi":True,"note":"~11× · best ROE in the pack"}],
    "verdict":"At ~11× earnings, Lalithaa is priced far below the peer average of ~44× — cheaper than Kalyan or Thangamayil — despite the highest ROE. A genuine value angle."},
    "narr":("So how is it priced against rivals? [pause] This is the number to sit with. [pause] At the top of the band, Lalithaa is "
      "valued at about eleven times its earnings. Compare that with listed peers: Kalyan Jewellers near forty-seven times, Thangamayil "
      "about forty-six, P-N Gadgil around twenty-two, and Senco Gold about eleven and a half. [pause] The peer average is roughly forty-"
      "four times. [pause] In other words, Lalithaa is asking far LESS than most of the pack — cheaper than Kalyan or Thangamayil — even "
      "though it has the best return on equity of the lot. That's a genuine value angle, and it's rare in a hot IPO market.")},
  "verdict":{"kicker":"SHOULD YOU SUBSCRIBE?","title":"Strengths vs Watch-outs","mythLabel":"⚠️ WATCH-OUTS","factLabel":"✅ STRENGTHS","pairs":[
    {"m":"Concentrated in South India — regional risk","f":"Priced ~11× — well BELOW peer average of ~44×"},
    {"m":"Thin 4% margins; gold-price swings hurt","f":"Profit nearly tripled; best-in-class 41.6% ROE"},
    {"m":"Inventory-heavy; needs constant working capital","f":"~71% fresh; strong per-store economics"}],
  },
  "n_verdict":("So — should you subscribe? [pause] The strengths are compelling — it's priced at about eleven times earnings, well below "
    "the peer average of forty-four; profit nearly tripled; it has the best return on equity in the group; and most of the issue is "
    "fresh money. [pause] The watch-outs matter too — it's concentrated in South India, so there's regional risk; margins are thin at "
    "about four percent and swing with gold prices; and like every jeweller, it's inventory-heavy and hungry for working capital. "
    "[pause] The takeaway — a profitable, efficient retailer at a genuinely modest price, with regional concentration as the main "
    "caveat. Only you can decide."),
  "retail_min":"₹14,874", "hni_extra":"",
  "n_retail":("Finally — how do you apply, and how much? [pause] Retail investors bid up to two lakh for a thirty-five percent quota, with "
    "allotment by lottery if oversubscribed. [pause] H-N-Is bid above two lakh for a fifteen percent quota. [pause] For Lalithaa, one lot "
    "is seventy-four shares — about fourteen thousand eight hundred and seventy-four rupees — your minimum. [pause] Track the live "
    "subscription on the N-S-E and B-S-E I-P-O pages, Chittorgarh, Moneycontrol, or your broker app."),
  "recap":{"title":"Lalithaa Jewellery Mart IPO — at a Glance","items":[
    "Business: South-India jewellery chain (56 stores, best per-store economics)","FY26: income ₹25,023.93 Cr, profit ₹1,009.82 Cr (+177%), ROE 41.6%",
    "₹1,700 Cr issue — ~71% fresh; funds new stores, WC, debt","Priced ~11× vs peer avg ~44× — a real value angle","Retail min ₹14,874 · GMP ~12.44% (unofficial)"],
    "closer":"A highly profitable regional jeweller priced well below its listed peers — with South-India concentration as the main risk. Read the RHP; decide for yourself."},
  "n_recap_pre":("Let's recap Lalithaa Jewellery Mart. [pause] A trusted South-India jewellery chain with the best per-store economics in "
    "the organised pack — profit nearly tripled, and a forty-one percent return on equity. [pause] The issue is about seventy-one percent "
    "fresh, funding new stores, inventory and some debt repayment. [pause] And the headline is valuation — about eleven times earnings, "
    "far below the peer average of forty-four. The main caveat is its concentration in South India. The retail minimum is fourteen "
    "thousand eight hundred and seventy-four rupees. [pause] "),
},
"shankesh": {
  "accent":"#FB923C","name":"Shankesh Jewellers IPO","kicker":"IPO ANALYSIS · MAINBOARD",
  "sub":"B2B handcrafted gold jewellery · ₹367.18 Cr · 18–20 Aug 2026",
  "n_title":("Let's break down the Shankesh Jewellers I-P-O — a three hundred and sixty-seven crore mainboard issue with an unusual, "
    "asset-light business model and explosive recent profit growth. [pause] We'll cover what it does, its full financials, where the "
    "money goes, how to think about its valuation, and whether it fits you. [pause] This is education, not investment advice."),
  "biz":{"kicker":"WHAT THE COMPANY DOES","title":"Inside Shankesh Jewellers","color":"#FB923C","items":[
    {"emoji":"💛","k":"B2B handcrafted gold jewellery","v":"Designs, sources and supplies customised, handcrafted 22- and 18-karat gold jewellery — mainly to other businesses","chip":"WHOLESALE"},
    {"emoji":"🪶","k":"Asset-light — no in-house factory","v":"Doesn't manufacture itself; works through a network of 72 skilled karigars/jobworkers while controlling design & quality","chip":"ASSET-LIGHT"},
    {"emoji":"🏙️","k":"Mumbai-based, since 2005","v":"Retains control over design, sourcing, quality checks, finishing and delivery — a design-and-supply model","chip":"MUMBAI"},
  ]},
  "n_biz":("So what does Shankesh do? [pause] It designs, sources and supplies customised, handcrafted twenty-two and eighteen-karat gold "
    "jewellery — largely a business-to-business, wholesale model. [pause] And here's the unusual part: it's asset-light. It does not run "
    "its own factory. Instead it works through a network of about seventy-two skilled karigars, or jobworkers, while keeping control of "
    "design, sourcing, quality and finishing. [pause] It's Mumbai-based, founded in two thousand five. So think of it as a design-and-"
    "supply house, not a factory."),
  "fin":{"kicker":"FINANCIALS","title":"The Headline Numbers","stats":[
    {"label":"Total income FY26","to":1631,"prefix":"₹","suffix":" Cr","color":"#34D399","sub":"₹1,630.93 Cr (FY25 ₹1,403.94 Cr)"},
    {"label":"Net profit FY26","to":107,"prefix":"₹","suffix":" Cr","color":"#34D399","sub":"₹106.68 Cr · +164.6% YoY"},
    {"label":"Return on equity","to":50.9,"prefix":"","suffix":"%","decimals":1,"color":"#FB923C","sub":"exceptional · ROCE 41.57%"}],
    "note":"Profit exploded — up 164.6% to ₹106.68 Cr — with a striking 50.94% ROE, helped by the asset-light model."},
  "n_fin":("Now the financials — and the profit growth is striking. [pause] Total income rose to about one thousand six hundred and thirty-"
    "one crore in FY twenty twenty-six. [pause] But look at profit: it surged over a hundred and sixty-four percent — from about forty "
    "crore to a hundred and seven crore. [pause] And the returns are exceptional — a return on equity near fifty-one percent, and return "
    "on capital around forty-two percent. That's the asset-light model at work — high returns because it doesn't tie up money in "
    "factories."),
  "threestmt":{"kicker":"FINANCIALS · 3 STATEMENTS","title":"Income, Balance Sheet & Cash Flow","color":"#FB923C","cols":[
    {"name":"Income Statement","icon":"📊","accent":"#34D399","rows":[
      {"label":"Total income FY26","val":"₹1,630.93 Cr","sub":"FY24→26 ₹1,061.91 → ₹1,630.93"},
      {"label":"Net profit FY26","val":"₹106.68 Cr","hi":True,"sub":"FY25 ₹40.31 Cr · +164.6%"},
      {"label":"PAT margin","val":"6.54%","sub":"better than most jewellers"}]},
    {"name":"Balance Sheet","icon":"🏦","accent":"#FB923C","rows":[
      {"label":"ROE / ROCE","val":"50.9% / 41.6%","hi":True,"sub":"asset-light → high returns"},
      {"label":"Total borrowings","val":"₹167.30 Cr","sub":"₹242.57 Cr by Dec-25"},
      {"label":"Model","val":"Asset-light","sub":"no in-house factory"}]},
    {"name":"Cash Flow","icon":"💵","accent":"#38BDF8","rows":[
      {"label":"Fresh issue inflow","val":"₹274.18 Cr","sub":"into the company"},
      {"label":"→ Repay borrowings","val":"₹158 Cr","hi":True,"sub":"cuts interest cost"},
      {"label":"→ Working capital","val":"₹38 Cr","sub":"CFO not disclosed; read RHP"}]}],
    "note":"Strong income statement & high returns; the full cash-flow statement isn't in public summaries — read the RHP."},
  "n_threestmt":("Let's put all three statements together. [pause] The income statement shows income of about sixteen hundred crore and "
    "profit of a hundred and seven crore, on a healthy six and a half percent margin. [pause] The balance sheet is where the model shines "
    "— return on equity near fifty-one percent, because it carries little more than about a hundred and sixty-seven crore of debt and no "
    "big factory. [pause] On cash flow, the fresh money — about a hundred and fifty-eight crore — repays debt, and thirty-eight crore "
    "funds working capital. The full operating cash-flow line isn't published in the summaries — read the R-H-P."),
  "issue":{"kicker":"WHERE THE MONEY GOES","title":"Fresh Issue vs Offer-for-Sale","stats":[
    {"label":"Total issue","to":367,"prefix":"₹","suffix":" Cr","color":"#FB923C","sub":"₹367.18 Cr · band ₹88–93"},
    {"label":"Fresh (into company)","to":274,"prefix":"₹","suffix":" Cr","color":"#34D399","sub":"₹274.18 Cr · ~75% funds the business"},
    {"label":"OFS (to promoters)","to":93,"prefix":"₹","suffix":" Cr","color":"#F87171","sub":"₹93 Cr — Jain promoters part-sell"}],
    "note":"A healthy mix: about 75% is fresh money that funds the company; ~25% is a promoter sell-down."},
  "n_issue":("Where does your money go? [pause] Of the three hundred and sixty-seven crore issue, about two hundred and seventy-four crore "
    "— roughly seventy-five percent — is a fresh issue, money going into the company. [pause] The remaining ninety-three crore is an "
    "Offer for Sale, where the Jain promoters sell part of their stake. [pause] So it's a mostly-fresh issue — three-quarters funds the "
    "business. That's a healthy structure."),
  "proceeds":{"kicker":"USE OF THE FRESH MONEY","title":"What the ₹274 Cr Funds","color":"#FB923C","items":[
    {"emoji":"🏦","k":"₹158 Cr — repay borrowings","v":"The largest use cuts debt, lowering finance costs and de-risking a fast-growing business","chip":"DEBT"},
    {"emoji":"💎","k":"₹38 Cr — working capital","v":"Funds gold inventory and order flow — the lifeblood of a design-and-supply jeweller","chip":"WC"},
    {"emoji":"🧰","k":"Balance — general corporate","v":"The remainder goes to general corporate purposes","chip":"GCP"},
  ]},
  "n_proceeds":("What does the fresh money fund? [pause] The largest use — about a hundred and fifty-eight crore — repays borrowings, "
    "cutting finance costs and de-risking a fast-growing business. [pause] Another thirty-eight crore funds working capital — gold "
    "inventory and order flow, the lifeblood of a design-and-supply jeweller. [pause] And the rest goes to general corporate purposes. A "
    "sensible, deleveraging use of the money."),
  "peers":{"variant":"sm_iconcards","props":{"kicker":"COMPETITORS · VALUATION","title":"How Is It Priced? A Wholesale Niche","color":"#FB923C","items":[
    {"emoji":"⚖️","k":"No clean listed twin","v":"Listed jewellers like Kalyan or Titan are consumer RETAIL brands; Shankesh is B2B, asset-light wholesale — a different model","chip":"NO PEER"},
    {"emoji":"📈","k":"Growth & returns justify some premium","v":"+164.6% profit and a ~51% ROE are far above sector norms — but such explosive growth can be hard to repeat","chip":"HOT GROWTH"},
    {"emoji":"🔎","k":"Judge on margin & durability","v":"Ask whether a wholesale, jobworker-based model can sustain these margins as it scales — that's the real question","chip":"DURABILITY"},
  ]},
    "narr":("So how is it priced against rivals? [pause] Here's the honest complication: there's no clean listed twin. Big names like "
      "Kalyan or Titan are consumer retail brands with their own stores; Shankesh is a business-to-business, asset-light wholesaler — a "
      "genuinely different model, so a simple P/E comparison can mislead. [pause] What you can say is that its growth and returns — profit "
      "up a hundred and sixty-four percent, a fifty-one percent return on equity — are far above sector norms, which justifies some "
      "premium. [pause] But explosive growth like that is hard to repeat. The real question is whether a wholesale, jobworker-based model "
      "can sustain these margins as it grows. Judge it on that.")},
  "verdict":{"kicker":"SHOULD YOU SUBSCRIBE?","title":"Strengths vs Watch-outs","mythLabel":"⚠️ WATCH-OUTS","factLabel":"✅ STRENGTHS","pairs":[
    {"m":"No clean listed peer to benchmark against","f":"Profit exploded +164.6%; ROE ~51%"},
    {"m":"B2B/wholesale — lower margins, key-customer risk","f":"~75% fresh; asset-light, capital-efficient"},
    {"m":"Can such fast growth be sustained?","f":"Fresh money cuts debt; ROCE ~42%"}],
  },
  "n_verdict":("So — should you subscribe? [pause] The strengths are eye-catching — profit up a hundred and sixty-four percent, a fifty-"
    "one percent return on equity, an asset-light and capital-efficient model, and three-quarters of the issue is fresh money that also "
    "cuts debt. [pause] The watch-outs are just as important — there's no clean listed peer to benchmark the price against; it's a "
    "business-to-business wholesaler, which brings thinner margins and key-customer risk; and you have to ask whether such explosive "
    "growth can be sustained. [pause] The takeaway — a fast-growing, efficient niche business at a fair-looking price, but one that's "
    "harder to value and to predict. Only you can decide."),
  "retail_min":"about ₹15,000", "hni_extra":"",
  "n_retail":("Finally — how do you apply, and how much? [pause] Retail investors bid up to two lakh for a thirty-five percent quota, with "
    "allotment by lottery if oversubscribed. [pause] H-N-Is bid above two lakh for a fifteen percent quota. [pause] For Shankesh, at an "
    "eighty-eight to ninety-three rupee band, one lot works out to about fifteen thousand rupees — your minimum. [pause] Track the live "
    "subscription on the N-S-E and B-S-E I-P-O pages, Chittorgarh, Moneycontrol, or your broker app."),
  "recap":{"title":"Shankesh Jewellers IPO — at a Glance","items":[
    "Business: B2B, asset-light handcrafted gold jewellery (Mumbai)","FY26: income ₹1,630.93 Cr, profit ₹106.68 Cr (+164.6%), ROE ~51%",
    "₹367.18 Cr issue — ~75% fresh; mainly repays debt","No clean listed peer — judge on margin durability","Retail min ~₹15,000 · lists 25 Aug"],
    "closer":"A capital-efficient, fast-growing wholesale jeweller — but with no clean peer and a model whose margins must prove durable. Read the RHP; decide for yourself."},
  "n_recap_pre":("Let's recap Shankesh Jewellers. [pause] An asset-light, business-to-business handcrafted-gold-jewellery house from "
    "Mumbai — profit exploded a hundred and sixty-four percent, with a fifty-one percent return on equity. [pause] The issue is about "
    "seventy-five percent fresh, mainly repaying debt. [pause] The catch is valuation and durability — there's no clean listed peer, and "
    "you must ask whether a wholesale model can sustain these margins. The retail minimum is about fifteen thousand rupees. [pause] "),
},
"sunshine": {
  "accent":"#A78BFA","name":"Sunshine Pictures IPO","kicker":"IPO ANALYSIS · MAINBOARD",
  "sub":"Film & content production · ₹282.14 Cr · 18–20 Aug 2026",
  "n_title":("Let's break down the Sunshine Pictures I-P-O — a two hundred and eighty-two crore mainboard issue from film-maker Vipul "
    "Shah's production house. [pause] It's a rare listed play on movies and content — but with the lumpy earnings that come with the "
    "business. [pause] We'll cover what it does, its full financials, where the money goes, how it's priced, and whether it fits you. "
    "[pause] This is education, not investment advice."),
  "biz":{"kicker":"WHAT THE COMPANY DOES","title":"Inside Sunshine Pictures","color":"#A78BFA","items":[
    {"emoji":"🎬","k":"Produces films, TV & web series","v":"A Mumbai content house that produces and distributes movies, television serials and web series","chip":"CONTENT"},
    {"emoji":"🎞️","k":"In-house VFX, colour & sound","v":"Uses digital-intermediate colour grading, Dolby Atmos mixing and dedicated VFX pipelines — a full production stack","chip":"POST-PROD"},
    {"emoji":"🌐","k":"Theatrical, satellite, digital, music","v":"Monetises across theatres, satellite/TV, streaming platforms and music — in India and overseas","chip":"MULTI-WINDOW"},
  ]},
  "n_biz":("So what does Sunshine do? [pause] It's a Mumbai content house — it produces and distributes films, television serials and web "
    "series, led by the film-maker Vipul Shah. [pause] It runs a full production stack in-house: digital colour grading, Dolby Atmos "
    "sound, and dedicated visual-effects pipelines. [pause] And it monetises across every window — theatres, satellite and TV, streaming "
    "platforms, and music, both in India and overseas. [pause] But keep one thing in mind throughout: a production business is project-"
    "dependent, so its earnings are lumpy — big in a hit year, thin in a quiet one."),
  "fin":{"kicker":"FINANCIALS","title":"The Headline Numbers","stats":[
    {"label":"Total income FY26","to":76,"prefix":"₹","suffix":" Cr","color":"#FBBF24","sub":"₹76.27 Cr — DOWN from FY25 ₹105.80 Cr"},
    {"label":"Net profit FY26","to":40,"prefix":"₹","suffix":" Cr","color":"#34D399","sub":"₹40.02 Cr (FY25 ₹34.46 Cr)"},
    {"label":"Debt-to-equity","to":0.06,"prefix":"","suffix":"","decimals":2,"color":"#A78BFA","sub":"near debt-free · borrowings ₹9.09 Cr"}],
    "note":"Note the lumpiness: FY26 income FELL versus FY25, yet profit rose — classic project-dependent content economics."},
  "n_fin":("Now the financials — and here you must read carefully. [pause] Total income in FY twenty twenty-six was about seventy-six "
    "crore — and notice, that's actually DOWN from about a hundred and six crore the year before. [pause] Yet net profit ROSE, to about "
    "forty crore. [pause] That mismatch — falling revenue, rising profit — is classic content economics: it depends on which projects "
    "landed in which year. [pause] On the plus side, the balance sheet is clean — near debt-free, with a debt-to-equity of just zero "
    "point zero six."),
  "threestmt":{"kicker":"FINANCIALS · 3 STATEMENTS","title":"Income, Balance Sheet & Cash Flow","color":"#A78BFA","cols":[
    {"name":"Income Statement","icon":"📊","accent":"#FBBF24","rows":[
      {"label":"Total income FY26","val":"₹76.27 Cr","hi":True,"sub":"FY25 ₹105.80 Cr — DOWN (lumpy)"},
      {"label":"Net profit FY26","val":"₹40.02 Cr","sub":"FY25 ₹34.46 Cr"},
      {"label":"EBITDA (FY25)","val":"₹50.76 Cr","sub":"strong margins in a hit year"}]},
    {"name":"Balance Sheet","icon":"🏦","accent":"#34D399","rows":[
      {"label":"Net worth","val":"₹145.13 Cr","sub":"healthy equity base"},
      {"label":"Total borrowings","val":"₹9.09 Cr","hi":True,"sub":"D/E 0.06 — near debt-free"},
      {"label":"Balance sheet","val":"Clean","sub":"low leverage"}]},
    {"name":"Cash Flow","icon":"💵","accent":"#38BDF8","rows":[
      {"label":"Fresh issue inflow","val":"~₹172.80 Cr","sub":"48L fresh shares @ ₹360"},
      {"label":"→ Long-term WC","val":"₹112.50 Cr","hi":True,"sub":"fund content pipeline"},
      {"label":"Operating cash flow","val":"Not disclosed","sub":"lumpy; read RHP"}]}],
    "note":"Clean balance sheet; but income is project-dependent — and the full cash-flow statement isn't in public summaries. Read the RHP."},
  "n_threestmt":("Let's put all three statements together. [pause] The income statement carries that lumpiness — seventy-six crore of "
    "income in FY twenty-six, down from a hundred and six, but forty crore of profit. [pause] The balance sheet is a genuine strength — "
    "net worth of about a hundred and forty-five crore and almost no debt, just nine crore. [pause] On cash flow, the fresh issue brings "
    "in about a hundred and seventy-three crore, of which a hundred and twelve and a half crore funds long-term working capital for the "
    "content pipeline. The operating cash-flow line isn't published in the summaries — read the R-H-P."),
  "issue":{"kicker":"WHERE THE MONEY GOES","title":"Fresh Issue vs Offer-for-Sale","stats":[
    {"label":"Total issue","to":282,"prefix":"₹","suffix":" Cr","color":"#A78BFA","sub":"₹282.14 Cr · band ₹342–360"},
    {"label":"Fresh (into company)","to":173,"prefix":"₹","suffix":" Cr","color":"#34D399","sub":"~₹172.8 Cr · ~61% funds the business"},
    {"label":"OFS (to promoters)","to":109,"prefix":"₹","suffix":" Cr","color":"#F87171","sub":"~₹109 Cr — Vipul & Shefali Shah sell"}],
    "note":"About 61% is fresh money for the content pipeline; ~39% is the promoter family (Vipul & Shefali Shah) partly cashing out."},
  "n_issue":("Where does your money go? [pause] Of the two hundred and eighty-two crore issue, about a hundred and seventy-three crore — "
    "roughly sixty-one percent — is a fresh issue that goes into the company. [pause] The remaining hundred and nine crore is an Offer "
    "for Sale, where the promoter family, Vipul and Shefali Shah, partly cash out. [pause] So it's a majority-fresh issue — most of your "
    "money funds the content pipeline."),
  "proceeds":{"kicker":"USE OF THE FRESH MONEY","title":"What the Fresh Money Funds","color":"#A78BFA","items":[
    {"emoji":"🎥","k":"₹112.50 Cr — long-term working capital","v":"Funds the content pipeline — developing and producing the next slate of films and series","chip":"PIPELINE"},
    {"emoji":"🧰","k":"General corporate purposes","v":"The balance supports general corporate needs as the company scales its output","chip":"GCP"},
    {"emoji":"⚠️","k":"Growth needs fresh content bets","v":"More content means more upfront spend before revenue lands — the working-capital ask reflects that","chip":"UPFRONT"},
  ]},
  "n_proceeds":("What does the fresh money fund? [pause] The main use — about a hundred and twelve and a half crore — is long-term working "
    "capital: funding the content pipeline, developing and producing the next slate of films and series. [pause] The rest goes to general "
    "corporate purposes. [pause] It makes sense for the business — more content means more upfront spend before the revenue lands — but "
    "it also means growth depends on making the right content bets."),
  "peers":{"variant":"sm_iconcards","props":{"kicker":"COMPETITORS · VALUATION","title":"How Is It Priced? ~32.5× on Lumpy Earnings","color":"#A78BFA","items":[
    {"emoji":"🔢","k":"~32.55× post-issue P/E","v":"At ₹360, the company is valued near ₹1,121 Cr — about 32.5 times FY26 earnings. That's a demanding multiple","chip":"~32.5×"},
    {"emoji":"🎲","k":"Earnings are project-dependent","v":"A P/E built on one year's profit is fragile when the next year's profit rides on which films land","chip":"LUMPY"},
    {"emoji":"🎬","k":"Few clean listed twins","v":"Pure film-production peers are scarce and messy on the exchanges — so the P/E is hard to anchor to a peer set","chip":"NO PEER"},
  ]},
    "narr":("So how is it priced? [pause] At the top of the band, Sunshine is valued near one thousand one hundred and twenty-one crore — "
      "about thirty-two and a half times its FY twenty-six earnings. That is a demanding multiple. [pause] And here's the catch: because "
      "earnings are project-dependent, a P/E built on a single year's profit is fragile — next year's number rides on which films land. "
      "[pause] There also aren't clean listed twins — pure film-production companies are scarce and messy on the exchanges — so you can't "
      "easily anchor that thirty-two times to a peer group. Treat the valuation with caution.")},
  "verdict":{"kicker":"SHOULD YOU SUBSCRIBE?","title":"Strengths vs Watch-outs","mythLabel":"⚠️ WATCH-OUTS","factLabel":"✅ STRENGTHS","pairs":[
    {"m":"Lumpy, project-dependent earnings","f":"Near debt-free balance sheet (D/E 0.06)"},
    {"m":"~32.5× P/E is demanding on one year","f":"Experienced promoter; full in-house production stack"},
    {"m":"FY26 revenue fell vs FY25","f":"Rare listed play on films & content; profitable"}],
  },
  "n_verdict":("So — should you subscribe? [pause] The strengths are real — a near debt-free balance sheet, an experienced film-maker at "
    "the helm, a full in-house production stack, and it's a rare, profitable, listed way to play movies and content. [pause] The watch-"
    "outs are equally real — earnings are lumpy and project-dependent, FY twenty-six revenue actually fell versus the year before, and at "
    "about thirty-two times earnings the price is demanding on a single year's profit. [pause] The takeaway — an interesting, clean-"
    "balance-sheet content play, but a volatile, hard-to-value one at a full price. Only you can decide."),
  "retail_min":"about ₹15,000", "hni_extra":"",
  "n_retail":("Finally — how do you apply, and how much? [pause] Retail investors bid up to two lakh for a thirty-five percent quota, with "
    "allotment by lottery if oversubscribed. [pause] H-N-Is bid above two lakh for a fifteen percent quota. [pause] For Sunshine, at a "
    "three hundred and forty-two to three hundred and sixty rupee band, one lot works out to about fifteen thousand rupees — your "
    "minimum. [pause] Track the live subscription on the N-S-E and B-S-E I-P-O pages, Chittorgarh, Moneycontrol, or your broker app."),
  "recap":{"title":"Sunshine Pictures IPO — at a Glance","items":[
    "Business: Vipul Shah's film, TV & web content house (Mumbai)","FY26: income ₹76.27 Cr (down YoY), profit ₹40.02 Cr; near debt-free",
    "₹282.14 Cr issue — ~61% fresh; funds content pipeline","~32.5× P/E on lumpy, project-dependent earnings","Retail min ~₹15,000 · lists 25 Aug"],
    "closer":"A rare, profitable, clean-balance-sheet listed content play — but with lumpy earnings and a demanding price. Read the RHP; decide for yourself."},
  "n_recap_pre":("Let's recap Sunshine Pictures. [pause] Film-maker Vipul Shah's content house — producing movies, TV and web series with "
    "a full in-house production stack and a near debt-free balance sheet. [pause] The issue is about sixty-one percent fresh, funding the "
    "content pipeline. [pause] But remember the two big caveats — earnings are lumpy and project-dependent, FY twenty-six revenue fell, "
    "and it's priced at a demanding thirty-two times earnings. The retail minimum is about fifteen thousand rupees. [pause] "),
},
"gaja": {
  "accent":"#34D399","name":"Gaja Alternative Asset Management IPO","kicker":"IPO ANALYSIS · MAINBOARD",
  "sub":"India's first PE/AIF manager to list · ₹550 Cr · 19–21 Aug 2026",
  "n_title":("Let's break down the Gaja Alternative Asset Management I-P-O — a five hundred and fifty crore issue that's a genuine first: "
    "India's own home-grown private-equity firm coming to the public market. [pause] We'll cover what it does, its full financials, where "
    "the money goes, how to value a business like this, and whether it fits you. [pause] This is education, not investment advice."),
  "biz":{"kicker":"WHAT THE COMPANY DOES","title":"Inside Gaja Capital","color":"#34D399","items":[
    {"emoji":"🏛️","k":"A private-equity / AIF manager","v":"Manages India-focused alternative investment funds — Category I and II AIFs — and advises offshore funds","chip":"PRIVATE EQUITY"},
    {"emoji":"🇮🇳","k":"India's first home-grown PE to list","v":"Founded 1999 in Mumbai; a mid-market PE firm — the first independent Indian alternative-asset manager to seek a listing","chip":"A FIRST"},
    {"emoji":"💸","k":"Earns fees on assets managed","v":"Makes money from management & performance fees on the capital it runs — a high-margin, fee-based model","chip":"FEE MODEL"},
  ]},
  "n_biz":("So what does Gaja do? [pause] It's an alternative-asset manager — in plain terms, a private-equity firm. It runs India-focused "
    "funds, the Category one and two alternative investment funds, and advises offshore funds that invest in Indian companies. [pause] "
    "It was founded in nineteen ninety-nine in Mumbai, and here's why this I-P-O matters: it's the first independent, home-grown Indian "
    "private-equity firm to seek a public listing. [pause] It earns management and performance fees on the capital it manages — a high-"
    "margin, fee-based model."),
  "fin":{"kicker":"FINANCIALS","title":"The Headline Numbers","stats":[
    {"label":"Total income FY26","to":158,"prefix":"₹","suffix":" Cr","color":"#34D399","sub":"₹157.80 Cr · +28% YoY"},
    {"label":"Net profit FY26","to":80,"prefix":"₹","suffix":" Cr","color":"#34D399","sub":"₹79.60 Cr · +33.8% YoY"},
    {"label":"PAT margin","to":51.9,"prefix":"","suffix":"%","decimals":1,"color":"#FBBF24","sub":"exceptional — fee-based model"}],
    "note":"A high-margin compounder: income up 28% and profit up ~34% to ₹79.60 Cr, on an outstanding ~52% net margin."},
  "n_fin":("Now the financials — and they show why fee-based businesses are prized. [pause] Total income rose about twenty-eight percent, "
    "to roughly a hundred and fifty-eight crore. [pause] Net profit grew about thirty-four percent, to around eighty crore. [pause] But "
    "the number that stands out is the margin — a net profit margin near fifty-two percent. [pause] That's the beauty of an asset-light, "
    "fee-based model: once the funds are running, a very large share of each rupee of fees drops to profit."),
  "threestmt":{"kicker":"FINANCIALS · 3 STATEMENTS","title":"Income, Balance Sheet & Cash Flow","color":"#34D399","cols":[
    {"name":"Income Statement","icon":"📊","accent":"#34D399","rows":[
      {"label":"Total income FY26","val":"₹157.80 Cr","sub":"FY25 ₹123.28 Cr · +28%"},
      {"label":"Net profit FY26","val":"₹79.60 Cr","hi":True,"sub":"FY25 ₹59.50 Cr · +33.8%"},
      {"label":"PAT margin","val":"~51.94%","sub":"fee-based, high margin"}]},
    {"name":"Balance Sheet","icon":"🏦","accent":"#FBBF24","rows":[
      {"label":"Total borrowings","val":"₹41.56 Cr","hi":True,"sub":"FY25 ₹4.00 Cr · D/E 0.07"},
      {"label":"Sponsor commitments","val":"~₹274 Cr","sub":"6.4% of fund corpus"},
      {"label":"Model","val":"Asset-light","sub":"fee income on AUM"}]},
    {"name":"Cash Flow","icon":"💵","accent":"#38BDF8","rows":[
      {"label":"Fresh issue inflow","val":"₹450 Cr","sub":"into the company"},
      {"label":"→ Fund commitments","val":"₹372 Cr","hi":True,"sub":"sponsor commits + bridge repay"},
      {"label":"Operating cash flow","val":"Not disclosed","sub":"summary omits it; read RHP"}]}],
    "note":"High-margin income statement & a light balance sheet; the full cash-flow statement isn't in public summaries — read the RHP."},
  "n_threestmt":("Let's put all three statements together. [pause] The income statement is the highlight — a hundred and fifty-eight crore "
    "of income, eighty crore of profit, and a fifty-two percent margin. [pause] The balance sheet is light — modest borrowings of about "
    "forty-two crore, and about two hundred and seventy-four crore of the firm's own money committed alongside investors in its funds. "
    "[pause] On cash flow, the fresh issue brings in four hundred and fifty crore, of which about three hundred and seventy-two crore "
    "goes to fund commitments and repay a bridge loan. The operating cash-flow line isn't published in the summaries — read the R-H-P."),
  "issue":{"kicker":"WHERE THE MONEY GOES","title":"Fresh Issue vs Offer-for-Sale","stats":[
    {"label":"Total issue","to":550,"prefix":"₹","suffix":" Cr","color":"#34D399","sub":"band ₹152–160"},
    {"label":"Fresh (into company)","to":450,"prefix":"₹","suffix":" Cr","color":"#34D399","sub":"~82% funds the business"},
    {"label":"OFS (to promoters)","to":100,"prefix":"₹","suffix":" Cr","color":"#F87171","sub":"~18% — a small sell-down"}],
    "note":"A strong mix: about 82% is fresh money; only ~18% is a promoter sell-down. Promoters hold ~71% pre-issue."},
  "n_issue":("Where does your money go? [pause] Of the five hundred and fifty crore issue, about four hundred and fifty crore — some "
    "eighty-two percent — is a fresh issue, money going into the company. [pause] Only about a hundred crore is an Offer for Sale, a "
    "small promoter sell-down. [pause] So this is a strongly fresh-led issue — most of your money funds the business, and the promoters, "
    "who hold about seventy-one percent, are keeping the vast majority of their stake."),
  "proceeds":{"kicker":"USE OF THE FRESH MONEY","title":"What the ₹450 Cr Funds","color":"#34D399","items":[
    {"emoji":"🤝","k":"₹372 Cr — sponsor commitments","v":"Puts the firm's OWN money into its funds alongside investors — 'skin in the game' that aligns interests","chip":"ALIGNMENT"},
    {"emoji":"🏦","k":"Repay a bridge loan","v":"Part of the same allocation repays a bridge loan, tidying the balance sheet","chip":"DEBT"},
    {"emoji":"🧰","k":"Balance — general corporate","v":"The remainder supports general corporate purposes as the platform grows","chip":"GCP"},
  ]},
  "n_proceeds":("What does the fresh money fund? [pause] The main use — about three hundred and seventy-two crore — goes to sponsor "
    "commitments: the firm putting its OWN money into its funds, alongside outside investors. [pause] That 'skin in the game' is actually "
    "a good sign — it aligns the manager's interests with yours. [pause] Part of that allocation also repays a bridge loan, and the rest "
    "goes to general corporate purposes."),
  "peers":{"variant":"sm_iconcards","props":{"kicker":"COMPETITORS · VALUATION","title":"How Is It Priced? A One-of-a-Kind Listing","color":"#34D399","items":[
    {"emoji":"🔢","k":"~28× P/E at ₹2,256 Cr value","v":"At ₹160 the firm is valued near ₹2,256 Cr — about 28 times FY26 earnings. Punchy, but its margins are exceptional","chip":"~28×"},
    {"emoji":"🆚","k":"Listed AMCs aren't the same model","v":"HDFC AMC and Nippon are MUTUAL-FUND managers with huge, steady AUM; Gaja is a PE firm with lumpier, performance-linked fees","chip":"DIFFERENT"},
    {"emoji":"📊","k":"Judge on AUM growth & fund returns","v":"For a PE manager, what matters is raising bigger funds and delivering returns — that drives future fees, not this year's P/E","chip":"AUM ENGINE"},
  ]},
    "narr":("So how is it priced? [pause] At the top of the band, Gaja is valued near two thousand two hundred and fifty-six crore — about "
      "twenty-eight times its FY twenty-six earnings. That's punchy, though its fifty-two percent margins soften it. [pause] Now, be "
      "careful with peers: the listed names people reach for — H-D-F-C A-M-C, Nippon — are mutual-fund managers with huge, steady assets "
      "and stable fees. Gaja is a private-equity firm, with lumpier, performance-linked fees. Different animal. [pause] For a manager like "
      "this, what really matters is whether it can raise bigger funds and deliver strong returns — that's the engine of future fees, far "
      "more than this year's P/E.")},
  "verdict":{"kicker":"SHOULD YOU SUBSCRIBE?","title":"Strengths vs Watch-outs","mythLabel":"⚠️ WATCH-OUTS","factLabel":"✅ STRENGTHS","pairs":[
    {"m":"~28× P/E; PE fees can be lumpy","f":"Exceptional ~52% net margin; +34% profit"},
    {"m":"No listed pure-PE peer to benchmark","f":"~82% fresh; promoters keep most of their stake"},
    {"m":"Success rides on future fundraising","f":"India's first home-grown PE listing; skin-in-the-game"}],
  },
  "n_verdict":("So — should you subscribe? [pause] The strengths are attractive — an exceptional fifty-two percent net margin, profit up "
    "about thirty-four percent, most of the issue is fresh money, the promoters keep the bulk of their stake, and the firm is putting its "
    "own capital into its funds. [pause] The watch-outs matter — at twenty-eight times earnings it isn't cheap; private-equity fees can "
    "be lumpy and performance-linked; there's no listed pure-PE peer to benchmark against; and future success rides on the firm raising "
    "bigger funds. [pause] The takeaway — a high-quality, high-margin first-of-its-kind business, but one whose earnings and value are "
    "harder to pin down than a mutual-fund AMC. Only you can decide."),
  "retail_min":"about ₹15,000", "hni_extra":"",
  "n_retail":("Finally — how do you apply, and how much? [pause] Retail investors bid up to two lakh for a thirty-five percent quota, with "
    "allotment by lottery if oversubscribed. [pause] H-N-Is bid above two lakh for a fifteen percent quota. [pause] For Gaja, at a "
    "hundred and fifty-two to a hundred and sixty rupee band, one lot works out to about fifteen thousand rupees — your minimum. [pause] "
    "Track the live subscription on the N-S-E and B-S-E I-P-O pages, Chittorgarh, Moneycontrol, or your broker app."),
  "recap":{"title":"Gaja Alternative Asset Management IPO — at a Glance","items":[
    "Business: India's first home-grown PE / AIF manager to list","FY26: income ₹157.80 Cr, profit ₹79.60 Cr (+34%), ~52% margin",
    "₹550 Cr issue — ~82% fresh; funds sponsor commitments","~28× P/E; no listed pure-PE peer — judge on fundraising","Retail min ~₹15,000 · lists 26 Aug"],
    "closer":"A high-margin, one-of-a-kind PE listing with the founders keeping most of their stake — but with lumpy fees and no clean peer. Read the RHP; decide for yourself."},
  "n_recap_pre":("Let's recap Gaja Alternative Asset Management. [pause] India's first home-grown private-equity firm to list — a high-"
    "margin, fee-based business with a fifty-two percent net margin and profit up about thirty-four percent. [pause] The issue is about "
    "eighty-two percent fresh, funding the firm's own commitments into its funds. [pause] The caveats — it's priced near twenty-eight "
    "times earnings, PE fees are lumpy, and there's no listed pure-PE peer, so success rides on future fundraising. The retail minimum is "
    "about fifteen thousand rupees. [pause] "),
},
}

# ---- scene assembly ----------------------------------------------------------------------------
def make_ipo(cid, c):
    a = c["accent"]
    def sc(sid, variant, props, narr): return (f"{cid}_{sid}", variant, props, narr)
    return [
      sc("title","sm_ptitle",{"title":c["name"],"sub":c["sub"],"kicker":c["kicker"]}, c["n_title"]),
      sc("biz","sm_iconcards",c["biz"], c["n_biz"]),
      *([sc("clients",c["clients"]["variant"],c["clients"]["props"], c["clients"]["narr"])] if "clients" in c else []),
      sc("fin","sm_stats",c["fin"], c["n_fin"]),
      *([sc("threestmt","sm_financials",c["threestmt"], c["n_threestmt"])] if "threestmt" in c else []),
      sc("issue","sm_stats",c["issue"], c["n_issue"]),
      sc("proceeds","sm_iconcards",c["proceeds"], c["n_proceeds"]),
      *([sc("peers",c["peers"]["variant"],c["peers"]["props"], c["peers"]["narr"])] if "peers" in c else []),
      sc("verdict","sm_myths",c["verdict"], c["n_verdict"]),
      sc("retail","sm_iconcards",{"kicker":"HOW TO APPLY · RETAIL vs HNI","title":"Categories & Money Needed","color":a,
          "items":retail_hni_items(c["retail_min"], c.get("hni_extra",""))}, c["n_retail"]),
      sc("recap","sm_recap",c["recap"], c["n_recap_pre"] + DISCLAIMER),
    ]

# ---- SME chapters ------------------------------------------------------------------------------
# SME IPOs differ from mainboard: separate NSE Emerge / BSE SME platform, a LARGE minimum bid
# (~₹1 lakh+, often 2 lots), thinner liquidity and lighter disclosure. The "apply" scene reflects that.
def sme_apply_items(exchange, lot_txt, min_txt):
    return [
        {"emoji":"🏢","k":f"Lists on {exchange}","v":"A separate platform for small companies — NOT the mainboard. Lot sizes, liquidity and risk all differ","chip":"SME"},
        {"emoji":"💰","k":"A large minimum bid","v":f"One lot is {lot_txt}. The minimum you need is {min_txt} — far above a mainboard IPO's ~₹15,000","chip":"MIN BID"},
        {"emoji":"⚠️","k":"Higher risk, thin liquidity","v":"SME stocks are volatile and lightly traded, with lighter disclosure — invest only money you can afford to lock up","chip":"RISK"},
        {"emoji":"🔎","k":"Check subscription LIVE","v":"NSE/BSE SME IPO pages, Chittorgarh or your broker app; allotment is by lottery if oversubscribed","chip":"SOURCES"},
    ]

def make_sme_ipo(cid, c):
    a = c["accent"]
    def sc(sid, variant, props, narr): return (f"{cid}_{sid}", variant, props, narr)
    return [
      sc("title","sm_ptitle",{"title":c["name"],"sub":c["sub"],"kicker":c["kicker"]}, c["n_title"]),
      sc("biz","sm_iconcards",c["biz"], c["n_biz"]),
      *([sc("clients",c["clients"]["variant"],c["clients"]["props"], c["clients"]["narr"])] if "clients" in c else []),
      sc("fin","sm_stats",c["fin"], c["n_fin"]),
      *([sc("threestmt","sm_financials",c["threestmt"], c["n_threestmt"])] if "threestmt" in c else []),
      sc("issue","sm_stats",c["issue"], c["n_issue"]),
      sc("proceeds","sm_iconcards",c["proceeds"], c["n_proceeds"]),
      *([sc("peers",c["peers"]["variant"],c["peers"]["props"], c["peers"]["narr"])] if "peers" in c else []),
      sc("verdict","sm_myths",c["verdict"], c["n_verdict"]),
      sc("apply","sm_iconcards",{"kicker":"HOW TO APPLY · SME IPO","title":"Platform & Money Needed","color":a,
          "items":sme_apply_items(c["sme_exchange"], c["sme_lot"], c["sme_min"])}, c["n_apply"]),
      sc("recap","sm_recap",c["recap"], c["n_recap_pre"] + DISCLAIMER),
    ]

SME_IPOS = {
"anawil": {
  "accent":"#FB923C","name":"Anawil Wire & Engineering IPO","kicker":"SME IPO ANALYSIS · NSE SME",
  "sub":"Telecom & transmission towers · ₹177.81 Cr · NSE SME · 3–5 Aug 2026",
  "n_title":("Let's break down the Anawil Wire and Engineering I-P-O — an S-M-E issue of about a hundred and seventy-eight crore, and "
    "one of the fastest-growing small companies of this batch. [pause] We'll cover what it does, its financials, where the money goes, "
    "and how S-M-E I-P-Os differ — including the much bigger minimum you need to apply. [pause] This is education, not investment advice."),
  "biz":{"kicker":"WHAT THE COMPANY DOES","title":"Inside Anawil Wire & Engineering","color":"#FB923C","items":[
    {"emoji":"🗼","k":"Makes transmission & telecom towers","v":"Manufactures and fabricates steel towers for power transmission and telecom — its core business","chip":"TOWERS"},
    {"emoji":"🔩","k":"Fabrication & engineering","v":"Heavy steel fabrication and galvanising — tower manufacturing was ~99.95% of FY25 revenue","chip":"STEEL"},
    {"emoji":"⚡","k":"A power-infra capex play","v":"Rides India's heavy spend on the power grid and telecom rollout — but it's a single-product business","chip":"GRID CAPEX"},
  ]},
  "n_biz":("So what does Anawil do? [pause] It manufactures and fabricates steel towers — the tall lattice structures that carry power "
    "transmission lines and telecom equipment. [pause] This is its core: tower manufacturing and fabrication made up almost ninety-"
    "nine point nine five percent of its revenue in FY twenty twenty-five. [pause] It rides a strong theme — India's heavy spending on "
    "the power grid and telecom. But be clear-eyed: this is essentially a single-product business, so its fortunes ride on that one line."),
  "fin":{"kicker":"FINANCIALS","title":"The Numbers","stats":[
    {"label":"Revenue FY26","to":143,"prefix":"₹","suffix":" Cr","color":"#34D399","sub":"+82% YoY (₹78.59 → ₹143.27 Cr)"},
    {"label":"Net Profit FY26","to":37,"prefix":"₹","suffix":" Cr","color":"#34D399","sub":"+198% YoY (₹12.30 → ₹36.63 Cr)"},
    {"label":"Grey-mkt premium","to":21,"prefix":"~","suffix":"%","color":"#FB923C","sub":"unofficial · drifts daily"}],
    "note":"Explosive growth — revenue up 82% and profit nearly tripling. Three-year path: revenue ₹54.07 → ₹78.59 → ₹143.27 Cr; profit ₹4.39 → ₹12.30 → ₹36.63 Cr."},
  "n_fin":("Now the financials — and the growth is striking. [pause] Revenue jumped about eighty-two percent, from seventy-eight point "
    "five nine crore to a hundred and forty-three point two seven crore in FY twenty twenty-six. And net profit nearly tripled — up a "
    "hundred and ninety-eight percent — from twelve point three zero crore to thirty-six point six three crore. [pause] Over three years, "
    "revenue has run from fifty-four, to seventy-nine, to a hundred and forty-three crore. [pause] The grey market is pricing a premium of "
    "around twenty-one percent — but that's unofficial, and it drifts every day."),
  "issue":{"kicker":"WHERE THE MONEY GOES","title":"Fresh Issue vs Offer-for-Sale","stats":[
    {"label":"Total issue","to":178,"prefix":"₹","suffix":" Cr","color":"#FB923C","sub":"₹177.81 Cr · band ₹257–270"},
    {"label":"Fresh (into company)","to":143,"prefix":"₹","suffix":" Cr","color":"#34D399","sub":"₹142.69 Cr · ~80% funds the business"},
    {"label":"OFS (to promoters)","to":35,"prefix":"₹","suffix":" Cr","color":"#F87171","sub":"₹35.12 Cr — promoters part-sell"}],
    "note":"A healthy mix: about 80% is a fresh issue that funds the company; only about 20% is a promoter sell-down."},
  "n_issue":("Where does your money go? [pause] Of the roughly one hundred and seventy-eight crore issue, about a hundred and forty-three "
    "crore — some eighty percent — is a fresh issue, money going into the company. [pause] The remaining thirty-five crore is an offer for "
    "sale, where the promoters sell a small part of their stake. [pause] So this is a mostly-fresh issue — four-fifths funds the business. "
    "That's a healthy structure."),
  "proceeds":{"kicker":"USE OF THE FRESH MONEY","title":"What the Fresh Money Funds","color":"#FB923C","items":[
    {"emoji":"🏦","k":"Mainly — repay debt","v":"The primary aim is to cut borrowings, which lowers finance costs and strengthens the balance sheet","chip":"DEBT"},
    {"emoji":"💵","k":"Better cash flows","v":"Lower interest frees up cash — useful for a fast-growing, fabrication-heavy business","chip":"CASH FLOW"},
    {"emoji":"🧰","k":"Balance — general corporate","v":"The remainder goes to general corporate purposes","chip":"GCP"},
  ]},
  "n_proceeds":("What does the fresh money fund? [pause] The main objective is to reduce debt by repaying borrowings. [pause] That lowers "
    "finance costs, improves cash flow, and strengthens the balance sheet — genuinely useful for a company growing this fast. [pause] The "
    "rest goes to general corporate purposes. It's a sensible, deleveraging use of the money."),
  "verdict":{"kicker":"SHOULD YOU SUBSCRIBE?","title":"Strengths vs Watch-outs","mythLabel":"⚠️ WATCH-OUTS","factLabel":"✅ STRENGTHS","pairs":[
    {"m":"Single-product — nearly all revenue is towers","f":"Explosive growth — revenue +82%, profit +198%"},
    {"m":"Tiny SME — volatile, thinly traded","f":"80% fresh — mostly funds the business, cuts debt"},
    {"m":"Customer & sector concentration risk","f":"Rides power-grid & telecom capex; GMP ~21%"}],
  },
  "n_verdict":("Should you subscribe? [pause] The strengths are eye-catching — revenue up eighty-two percent, profit up nearly two "
    "hundred percent, most of the issue is fresh money that also cuts debt, and it rides real power-grid and telecom spending. [pause] "
    "The watch-outs are just as important — almost all its revenue comes from one product, towers, so it's concentrated; it's a tiny "
    "S-M-E, which means volatility and thin trading; and it carries customer and sector concentration risk. [pause] The takeaway — "
    "terrific growth and a clean structure, but a concentrated, small-cap bet. Know that before you decide."),
  "sme_exchange":"NSE SME","sme_lot":"400 shares","sme_min":"about ₹1.08 lakh",
  "n_apply":("Now — how do you apply, and how does an S-M-E I-P-O differ? [pause] This lists on the N-S-E S-M-E platform, which is separate "
    "from the mainboard, with its own rules and risks. [pause] The big difference is the minimum. One lot here is four hundred shares — "
    "about one lakh eight thousand rupees. That's far more than a mainboard I-P-O, where fifteen thousand gets you in. [pause] And S-M-E "
    "stocks are volatile and thinly traded, so invest only what you can afford to lock up. [pause] Track the live subscription on the N-S-E "
    "S-M-E page, Chittorgarh, or your broker app — allotment is by lottery if it's oversubscribed."),
  "recap":{"title":"Anawil Wire & Engineering IPO — at a Glance","items":[
    "Business: transmission & telecom tower maker (single-product)","FY26: revenue ₹143.27 Cr (+82%), profit ₹36.63 Cr (+198%)",
    "₹177.81 Cr issue — ~80% fresh; NSE SME","Fresh money mainly repays debt","SME min ~₹1.08 lakh · GMP ~21% (unofficial)"],
    "closer":"Explosive growth and a clean, debt-cutting structure — but a single-product, small-cap SME. Read the RHP; decide for yourself."},
  "n_recap_pre":("Let's recap Anawil Wire and Engineering. [pause] A transmission and telecom tower maker on the power-capex theme, and one "
    "of the fastest growers here — revenue up eighty-two percent, profit up nearly two hundred. [pause] The issue is about eighty percent "
    "fresh, and that money mainly repays debt. [pause] But remember — it's a single-product S-M-E, so it's concentrated and volatile, and "
    "the minimum bid is about one lakh eight thousand rupees. [pause] "),
},
"aegeus": {
  "accent":"#34D399","name":"Aegeus Technologies IPO","kicker":"SME IPO ANALYSIS · BSE SME",
  "sub":"Solar-panel cleaning robots · ₹23.71 Cr · 100% Fresh · BSE SME · 4–6 Aug 2026",
  "n_title":("Let's break down the Aegeus Technologies I-P-O — a small, twenty-four crore S-M-E issue with a genuinely interesting niche: "
    "robots that clean solar panels. [pause] We'll cover what it does, its financials, where the money goes, and how much you'd need to "
    "apply on the S-M-E platform. [pause] This is education, not investment advice."),
  "biz":{"kicker":"WHAT THE COMPANY DOES","title":"Inside Aegeus Technologies","color":"#34D399","items":[
    {"emoji":"🤖","k":"Solar-cleaning robots","v":"Builds automation to clean and maintain solar panels — dust cuts a plant's output, so cleaning matters","chip":"ROBOTICS"},
    {"emoji":"🔆","k":"Unicorn & Shreem robots","v":"'Unicorn' for large ground-mounted solar plants; 'Shreem' for rooftop installations","chip":"2 PRODUCTS"},
    {"emoji":"🛠️","k":"Products + maintenance","v":"FY26 revenue split ~55% product sales and ~45% maintenance services — a recurring-revenue angle","chip":"55/45"},
  ]},
  "n_biz":("So what does Aegeus do? [pause] It makes robots that clean and maintain solar panels. It matters more than it sounds — dust "
    "and dirt can sharply cut a solar plant's output, so automated cleaning directly protects power generation. [pause] It has two main "
    "products: 'Unicorn', for large ground-mounted solar farms, and 'Shreem', for rooftop systems. [pause] And its revenue is nicely "
    "split — about fifty-five percent from selling products and forty-five percent from maintenance services, which adds a recurring angle."),
  "fin":{"kicker":"FINANCIALS","title":"The Numbers","stats":[
    {"label":"Total Income FY26","to":41,"prefix":"₹","suffix":" Cr","color":"#34D399","sub":"+88% YoY (₹21.90 → ₹41.22 Cr)"},
    {"label":"Net Profit FY26","to":4,"prefix":"₹","suffix":" Cr","color":"#34D399","sub":"nearly 3× (₹1.39 → ₹4.02 Cr)"},
    {"label":"Issue size","to":24,"prefix":"₹","suffix":" Cr","color":"#22D3EE","sub":"₹23.71 Cr · 100% fresh"}],
    "note":"Fast growth off a small base: income up 88% and profit nearly tripling. But the profit base is tiny — ₹4 Cr — so it's early-stage."},
  "n_fin":("Now the financials. [pause] Growth is rapid, off a small base — total income rose about eighty-eight percent, from twenty-one "
    "point nine zero crore to forty-one point two two crore. And net profit nearly tripled, from one point three nine crore to four point "
    "zero two crore. [pause] The whole issue is just under twenty-four crore. [pause] So keep it in proportion — the growth rate is "
    "excellent, but the absolute profit is small, around four crore, which makes this an early-stage company."),
  "issue":{"kicker":"WHERE THE MONEY GOES","title":"A 100% Fresh Issue","stats":[
    {"label":"Total issue","to":24,"prefix":"₹","suffix":" Cr","color":"#34D399","sub":"₹23.71 Cr · band ₹100–105"},
    {"label":"Fresh (into company)","to":24,"prefix":"₹","suffix":" Cr","color":"#34D399","sub":"100% — every rupee funds the business"},
    {"label":"OFS (to sellers)","to":0,"prefix":"₹","suffix":" Cr","color":"#64748B","sub":"none — no promoter sell-down"}],
    "note":"The best possible structure: this is a 100% fresh issue. Every rupee raised goes INTO the company — no promoter cashes out."},
  "n_issue":("Where does your money go? [pause] And here Aegeus has the best possible answer — this is a hundred percent fresh issue. "
    "[pause] There's no offer for sale at all. Every single rupee raised goes into the company, not into a promoter's pocket. [pause] For "
    "a young, growing business that needs capital to expand, that's exactly what you want to see."),
  "proceeds":{"kicker":"USE OF THE FRESH MONEY","title":"What the ₹23.7 Cr Funds","color":"#34D399","items":[
    {"emoji":"🔬","k":"Product development","v":"A slice funds R&D to develop and improve its cleaning robots","chip":"R&D"},
    {"emoji":"🏭","k":"A new manufacturing facility","v":"Capex to set up a new plant — expanding capacity to build more robots","chip":"CAPEX"},
    {"emoji":"🔄","k":"Working capital + GCP","v":"The rest funds day-to-day working capital and general corporate purposes","chip":"WC"},
  ]},
  "n_proceeds":("What does the fresh money fund? [pause] Three things, all about growth. Part goes into product development — R and D on "
    "the robots. [pause] Part funds capital expenditure for a new manufacturing facility, to build more units. [pause] And the rest goes "
    "to working capital and general corporate purposes. So the money is being used to expand the business — the right use for a young "
    "company."),
  "verdict":{"kicker":"SHOULD YOU SUBSCRIBE?","title":"Strengths vs Watch-outs","mythLabel":"⚠️ WATCH-OUTS","factLabel":"✅ STRENGTHS","pairs":[
    {"m":"Very small — only ~₹4 Cr profit","f":"100% fresh — all money funds growth"},
    {"m":"Early-stage; niche, competitive market","f":"Income +88%, profit nearly tripled"},
    {"m":"Tiny SME — volatile & thinly traded","f":"On the solar / clean-energy theme; recurring service revenue"}],
  },
  "n_verdict":("Should you subscribe? [pause] The strengths are appealing — it's a hundred percent fresh issue, so all the money funds "
    "growth; income is up eighty-eight percent and profit has nearly tripled; and it sits on the solar theme with a helpful chunk of "
    "recurring maintenance revenue. [pause] The watch-outs — it's very small, with only about four crore of profit; it's early-stage in a "
    "niche, competitive market; and as a tiny S-M-E it will be volatile and thinly traded. [pause] The takeaway — a promising, clean-"
    "structured micro-cap on a good theme, but a genuinely small and early bet. Size it accordingly."),
  "sme_exchange":"BSE SME","sme_lot":"1,200 shares","sme_min":"₹2,52,000 (2 lots)",
  "n_apply":("Now — how to apply, and how S-M-E I-P-Os differ. [pause] Aegeus lists on the B-S-E S-M-E platform, separate from the "
    "mainboard. [pause] The minimum is large. One lot is twelve hundred shares, and the smallest retail application here is two lots — "
    "about two lakh fifty-two thousand rupees. That's a big ticket compared with a mainboard I-P-O. [pause] And remember, S-M-E stocks are "
    "volatile and lightly traded, so only commit money you can lock away. [pause] Track the live subscription on the B-S-E S-M-E page, "
    "Chittorgarh, or your broker app — allotment is by lottery if oversubscribed."),
  "recap":{"title":"Aegeus Technologies IPO — at a Glance","items":[
    "Business: robots that clean & maintain solar panels","FY26: income ₹41.22 Cr (+88%), profit ₹4.02 Cr (nearly 3×)",
    "₹23.71 Cr issue — 100% FRESH; BSE SME","Funds R&D, a new plant & working capital","SME min ₹2,52,000 (2 lots) — a big ticket"],
    "closer":"A clean, 100%-fresh micro-cap on the solar theme with fast growth — but tiny and early-stage. Read the RHP; decide for yourself."},
  "n_recap_pre":("Let's recap Aegeus Technologies. [pause] It builds robots that clean solar panels — a niche on the clean-energy theme, "
    "growing fast off a small base, with income up eighty-eight percent. [pause] The whole twenty-four crore issue is fresh money funding "
    "R and D, a new plant and working capital. [pause] But it's tiny, with only about four crore of profit, and the S-M-E minimum is a "
    "hefty two lakh fifty-two thousand rupees. [pause] "),
},
"lapl": {
  "accent":"#FBBF24","name":"LAPL Automotive IPO","kicker":"SME IPO ANALYSIS · BSE SME",
  "sub":"Auto lighting & mirrors · ₹32.40 Cr · 100% Fresh · BSE SME · 6–10 Aug 2026",
  "n_title":("Let's break down the LAPL Automotive I-P-O — a thirty-two crore S-M-E issue from an auto-components maker, expanding into "
    "lighting and electronics. [pause] We'll cover what it does, its financials, where the money goes, and what it takes to apply on the "
    "S-M-E platform. [pause] This is education, not investment advice."),
  "biz":{"kicker":"WHAT THE COMPANY DOES","title":"Inside LAPL Automotive","color":"#FBBF24","items":[
    {"emoji":"💡","k":"Auto lighting & mirrors","v":"Manufactures automotive components — lighting systems and mirrors for vehicles","chip":"COMPONENTS"},
    {"emoji":"🏷️","k":"ODM + own-brand (OBM)","v":"78% of FY26 revenue is design-manufacturing for others (ODM); 22% is its own brands (OBM)","chip":"78/22"},
    {"emoji":"🔧","k":"An auto-ancillary play","v":"Rides India's large auto & aftermarket demand; own-brand sales can carry better margins","chip":"AUTO"},
  ]},
  "n_biz":("So what does LAPL Automotive do? [pause] It makes automotive components — chiefly lighting systems and mirrors for vehicles. "
    "[pause] It runs two models. About seventy-eight percent of its revenue is O-D-M — designing and manufacturing parts for other "
    "brands. The other twenty-two percent is O-B-M — selling under its own brands, which can carry better margins. [pause] So it's an "
    "auto-ancillary play, riding India's large vehicle and spare-parts demand, and slowly building its own brand."),
  "fin":{"kicker":"FINANCIALS","title":"The Numbers","stats":[
    {"label":"Revenue FY26","to":93,"prefix":"₹","suffix":" Cr","color":"#34D399","sub":"+41.3% YoY (₹66.00 → ₹93.30 Cr)"},
    {"label":"Net Profit FY26","to":9,"prefix":"₹","suffix":" Cr","color":"#34D399","sub":"+71.4% YoY (₹5.03 → ₹8.60 Cr)"},
    {"label":"Grey-mkt premium","to":18,"prefix":"~","suffix":"%","color":"#FBBF24","sub":"unofficial · drifts daily"}],
    "note":"Healthy growth with rising margins — revenue up 41% and profit up 71%, so profit grew faster than sales."},
  "n_fin":("Now the financials — healthy, with improving margins. [pause] Revenue rose about forty-one percent, from sixty-six crore to "
    "ninety-three point three zero crore in FY twenty twenty-six. And net profit jumped seventy-one point four percent, from five point "
    "zero three crore to eight point six zero crore. [pause] Notice that profit grew faster than sales — a sign margins are improving, "
    "helped by the own-brand mix. [pause] The grey market is pricing a premium of around eighteen percent — but that's unofficial and "
    "moves daily."),
  "issue":{"kicker":"WHERE THE MONEY GOES","title":"A 100% Fresh Issue","stats":[
    {"label":"Total issue","to":32,"prefix":"₹","suffix":" Cr","color":"#FBBF24","sub":"₹32.40 Cr · band ₹88–94"},
    {"label":"Fresh (into company)","to":32,"prefix":"₹","suffix":" Cr","color":"#34D399","sub":"100% — funds expansion"},
    {"label":"OFS (to sellers)","to":0,"prefix":"₹","suffix":" Cr","color":"#64748B","sub":"none — no promoter sell-down"}],
    "note":"A 100% fresh issue — no offer for sale. All the money goes into the company to fund a new plant and cut debt."},
  "n_issue":("Where does your money go? [pause] Like the last one, this is a hundred percent fresh issue — there's no offer for sale. "
    "[pause] Every rupee raised goes into the company. [pause] For a manufacturer that's about to expand capacity, putting all the money "
    "to work in the business — rather than paying out a promoter — is exactly the right structure."),
  "proceeds":{"kicker":"USE OF THE FRESH MONEY","title":"What the ₹32.4 Cr Funds","color":"#FBBF24","items":[
    {"emoji":"🏭","k":"₹19.56 Cr — a new plant","v":"The bulk builds a new manufacturing unit — expanding into lighting, electricals and electronic components","chip":"CAPEX"},
    {"emoji":"🏦","k":"₹4.8 Cr — reduce debt","v":"A slice repays borrowings, trimming interest costs","chip":"DEBT"},
    {"emoji":"🧰","k":"Balance — general corporate","v":"The remainder goes to general corporate purposes","chip":"GCP"},
  ]},
  "n_proceeds":("What does the fresh money fund? [pause] The bulk — about nineteen and a half crore — sets up a new manufacturing unit, "
    "expanding the company into lighting, electricals and electronic components. That's a capacity and product expansion. [pause] Around "
    "four point eight crore repays debt, cutting interest costs. [pause] And the rest is for general purposes. So most of the money funds "
    "real growth — the kind of use you want to see."),
  "verdict":{"kicker":"SHOULD YOU SUBSCRIBE?","title":"Strengths vs Watch-outs","mythLabel":"⚠️ WATCH-OUTS","factLabel":"✅ STRENGTHS","pairs":[
    {"m":"Small SME — volatile & thinly traded","f":"Strong growth — revenue +41%, profit +71%"},
    {"m":"Auto-cyclical; customer concentration","f":"100% fresh — funds a new plant, cuts debt"},
    {"m":"Execution risk on the new plant","f":"Rising margins & a growing own-brand (OBM)"}],
  },
  "n_verdict":("Should you subscribe? [pause] The strengths — revenue up forty-one percent and profit up seventy-one, so margins are "
    "improving; it's a hundred percent fresh issue funding a new plant and cutting debt; and it's building higher-margin own brands. "
    "[pause] The watch-outs — it's a small S-M-E, so volatile and thinly traded; auto components are cyclical and can depend on a few "
    "customers; and a new plant always carries execution risk. [pause] The takeaway — solid growth and a productive use of the money, but "
    "a small-cap, cyclical bet with expansion risk. Weigh that before you decide."),
  "sme_exchange":"BSE SME","sme_lot":"1,200 shares","sme_min":"₹2,25,600 (2 lots)",
  "n_apply":("Now — how to apply. [pause] LAPL lists on the B-S-E S-M-E platform, separate from the mainboard. [pause] The minimum is "
    "large: one lot is twelve hundred shares, and the smallest retail application is two lots — about two lakh twenty-five thousand six "
    "hundred rupees. [pause] As always with S-M-Es, expect volatility and thin trading, so invest only what you can afford to lock up. "
    "[pause] Track the live subscription on the B-S-E S-M-E page, Chittorgarh, or your broker app — allotment is by lottery if "
    "oversubscribed."),
  "recap":{"title":"LAPL Automotive IPO — at a Glance","items":[
    "Business: auto lighting & mirrors (ODM 78% + own-brand 22%)","FY26: revenue ₹93.30 Cr (+41%), profit ₹8.60 Cr (+71%)",
    "₹32.40 Cr issue — 100% FRESH; BSE SME","Funds a new plant (₹19.56 Cr) + debt cut","SME min ₹2,25,600 (2 lots)"],
    "closer":"Strong growth, improving margins and an all-fresh issue funding expansion — but a small, cyclical SME. Read the RHP; decide for yourself."},
  "n_recap_pre":("Let's recap LAPL Automotive. [pause] An auto-components maker — lighting and mirrors — growing well, with revenue up "
    "forty-one percent and profit up seventy-one, and rising margins from its own brands. [pause] The whole thirty-two crore issue is "
    "fresh money, funding a new plant and cutting debt. [pause] But it's a small, cyclical S-M-E, and the minimum bid is about two lakh "
    "twenty-five thousand rupees. [pause] "),
},
"optimystix": {
  "accent":"#F472B6","name":"Optimystix Entertainment IPO","kicker":"SME IPO ANALYSIS · NSE SME",
  "sub":"TV content — Comedy Circus, Crime Patrol · ₹107.88 Cr · NSE SME · 7–11 Aug 2026",
  "n_title":("Let's break down the Optimystix Entertainment I-P-O — a hundred and eight crore S-M-E issue from the production house behind "
    "shows like Comedy Circus and Crime Patrol. [pause] We'll cover what it does, its financials, where the money goes, and what it takes "
    "to apply. [pause] This is education, not investment advice."),
  "biz":{"kicker":"WHAT THE COMPANY DOES","title":"Inside Optimystix Entertainment","color":"#F472B6","items":[
    {"emoji":"📺","k":"A TV & content producer","v":"Makes television shows and content — behind popular titles like Comedy Circus and Crime Patrol","chip":"CONTENT"},
    {"emoji":"🎬","k":"A deep back-catalogue","v":"150+ TV shows and 7,500+ hours of original programming across television and films","chip":"150+ SHOWS"},
    {"emoji":"⭐","k":"First-ever IPO","v":"Led by veterans Vipul D. Shah and Rajesh Bahl; this is the company's debut on the market","chip":"DEBUT"},
  ]},
  "n_biz":("So what does Optimystix do? [pause] It's a television and content production house — the team behind well-known shows like "
    "Comedy Circus and Crime Patrol. [pause] It has a deep library: over a hundred and fifty T-V shows and more than seven thousand five "
    "hundred hours of original programming, across television and films. [pause] It's led by industry veterans Vipul D. Shah and Rajesh "
    "Bahl, and this is its first-ever public issue."),
  "fin":{"kicker":"FINANCIALS","title":"The Numbers","stats":[
    {"label":"Revenue FY26","to":136,"prefix":"₹","suffix":" Cr","color":"#34D399","sub":"+8.6% YoY (₹125.07 → ₹135.89 Cr)"},
    {"label":"Net Profit FY26","to":24,"prefix":"₹","suffix":" Cr","color":"#34D399","sub":"+39% YoY (₹17.24 → ₹24.04 Cr)"},
    {"label":"Valuation P/E","to":16.8,"decimals":1,"prefix":"~","suffix":"×","color":"#F472B6","sub":"est. ~₹405 Cr value ÷ ₹24.04 Cr PAT"}],
    "note":"Steady revenue but strong profit growth — profit up 39% while sales rose 9%, so margins jumped. Valued at ~17× earnings."},
  "n_fin":("Now the financials. [pause] Revenue was fairly steady — up about nine percent, from a hundred and twenty-five point zero seven "
    "crore to a hundred and thirty-five point eight nine crore. [pause] But profit grew much faster — up thirty-nine percent, from "
    "seventeen point two four crore to twenty-four point zero four crore. So margins improved sharply. [pause] On our estimate, from a "
    "post-issue value of about four hundred and five crore, that's roughly seventeen times earnings — a reasonable valuation for a "
    "profitable content business."),
  "issue":{"kicker":"WHERE THE MONEY GOES","title":"Fresh Issue vs Offer-for-Sale","stats":[
    {"label":"Total issue","to":108,"prefix":"₹","suffix":" Cr","color":"#F472B6","sub":"₹107.88 Cr · band ₹165–174"},
    {"label":"Fresh (into company)","to":87,"prefix":"₹","suffix":" Cr","color":"#34D399","sub":"~₹87 Cr · ~81% funds the business"},
    {"label":"OFS (to promoter)","to":21,"prefix":"₹","suffix":" Cr","color":"#F87171","sub":"₹20.88 Cr — promoter part-sells"}],
    "note":"A healthy mix: about 81% is a fresh issue funding the business; ~19% is promoter Vipul D. Shah selling part of his stake."},
  "n_issue":("Where does your money go? [pause] Of the roughly one hundred and eight crore issue, about eighty-seven crore — some eighty-"
    "one percent — is a fresh issue going into the company. [pause] The remaining twenty-one crore is an offer for sale, where promoter "
    "Vipul D. Shah sells part of his stake. [pause] So this is a mostly-fresh issue — four-fifths funds the business. A healthy structure."),
  "proceeds":{"kicker":"USE OF THE FRESH MONEY","title":"What the ₹87 Cr Funds","color":"#F472B6","items":[
    {"emoji":"🔄","k":"₹55.88 Cr — working capital","v":"The bulk funds working capital — content production ties up cash long before a show earns revenue","chip":"WC"},
    {"emoji":"🧰","k":"Balance — general corporate","v":"The remainder goes to general corporate purposes","chip":"GCP"},
    {"emoji":"🎥","k":"Why so much working capital","v":"Producing shows means paying crews and costs upfront, then collecting later — growth needs funding","chip":"CONTENT"},
  ]},
  "n_proceeds":("What does the fresh money fund? [pause] The bulk — about fifty-five point eight eight crore — goes into working capital. "
    "[pause] That makes sense for a content producer: you pay crews, cast and production costs upfront, and only collect revenue later, so "
    "growth ties up a lot of cash. [pause] The rest is for general corporate purposes. It's a straightforward, growth-oriented use of the "
    "money."),
  "verdict":{"kicker":"SHOULD YOU SUBSCRIBE?","title":"Strengths vs Watch-outs","mythLabel":"⚠️ WATCH-OUTS","factLabel":"✅ STRENGTHS","pairs":[
    {"m":"Content is hit-driven — revenue can be lumpy","f":"Profitable & known titles; margins jumped"},
    {"m":"Revenue growth is modest (~9%)","f":"~81% fresh; reasonable ~17× valuation"},
    {"m":"Small SME — volatile & thinly traded","f":"Deep library; experienced promoters"}],
  },
  "n_verdict":("Should you subscribe? [pause] The strengths — it's genuinely profitable, with recognisable titles and a sharp jump in "
    "margins; about eighty-one percent of the issue is fresh money; and at roughly seventeen times earnings, the valuation is reasonable. "
    "[pause] The watch-outs — content is a hit-driven business, so revenue can be lumpy year to year; top-line growth here was modest, "
    "under ten percent; and it's a small S-M-E, so volatile and thinly traded. [pause] The takeaway — a profitable, well-known content "
    "house at a fair price, but a hit-driven, small-cap bet. Decide with that in mind."),
  "sme_exchange":"NSE SME","sme_lot":"~₹1 lakh per lot","sme_min":"about ₹1 lakh+ (lot TBA)",
  "n_apply":("Now — how to apply. [pause] Optimystix lists on the N-S-E S-M-E platform, separate from the mainboard. [pause] As with all "
    "S-M-Es, the minimum is large — around one lakh rupees or more for a single lot, far above a mainboard I-P-O. The exact lot size is "
    "confirmed just before the issue opens, so check it on the day. [pause] And remember, S-M-E stocks are volatile and thinly traded, so "
    "invest only what you can afford to lock away. [pause] Track the live subscription and the final lot on the N-S-E S-M-E page, "
    "Chittorgarh, or your broker app — allotment is by lottery if oversubscribed."),
  "recap":{"title":"Optimystix Entertainment IPO — at a Glance","items":[
    "Business: TV content producer (Comedy Circus, Crime Patrol)","FY26: revenue ₹135.89 Cr (+9%), profit ₹24.04 Cr (+39%)",
    "₹107.88 Cr issue — ~81% fresh; NSE SME","Fresh money mainly funds working capital","Valued ~17× · SME min ~₹1 lakh+"],
    "closer":"A profitable, recognisable content house at a fair price — but a hit-driven, small-cap SME. Read the RHP; decide for yourself."},
  "n_recap_pre":("Let's recap Optimystix Entertainment. [pause] The production house behind Comedy Circus and Crime Patrol, with a deep "
    "library and a sharp jump in margins — profit up thirty-nine percent. [pause] The issue is about eighty-one percent fresh, mainly "
    "funding working capital, at a reasonable seventeen times earnings. [pause] But content is hit-driven and lumpy, it's a small S-M-E, "
    "and the minimum bid is around one lakh rupees or more. [pause] "),
},

# ===== BATCH 5 SME (8 Aug 2026 — SME IPOs opening next week, 11–14 Aug 2026) ====================
"fascinate": {
  "accent":"#EC4899","name":"Fascinate Textiles IPO","kicker":"SME IPO ANALYSIS · NSE SME",
  "sub":"Readymade garment OEM · ₹67 Cr · NSE SME · 11–13 Aug 2026",
  "n_title":("Let's break down the Fascinate Textiles I-P-O — an S-M-E issue of about sixty-seven crore from a readymade-garment maker. "
    "[pause] We'll cover what it does, its financials, where the money goes, who its competitors are, and how S-M-E I-P-Os differ — including "
    "the much bigger minimum you need to apply. [pause] This is education, not investment advice."),
  "biz":{"kicker":"WHAT THE COMPANY DOES","title":"Inside Fascinate Textiles","color":"#EC4899","items":[
    {"emoji":"👕","k":"B2B garment manufacturer","v":"An OEM that makes readymade garments for organised retailers — it supplies brands, it isn't a consumer brand itself","chip":"OEM · B2B"},
    {"emoji":"🧒","k":"Kids, men's & infant wear","v":"FY26 mix: kids' garments ~38%, men's wear ~29%, infant wear ~22% — a spread across categories","chip":"MULTI-CATEGORY"},
    {"emoji":"🏬","k":"Almost all wholesale","v":"About 99.75% of revenue is B2B — so it leans on a handful of large retail customers","chip":"~99.75% B2B"},
  ]},
  "n_biz":("So what does Fascinate do? [pause] It's a business-to-business garment manufacturer — an O-E-M that makes readymade clothes for "
    "organised retailers. It supplies other brands; it isn't a consumer brand you'd recognise. [pause] Its range spans kids' garments, "
    "about thirty-eight percent of revenue, men's wear at twenty-nine, and infant wear at twenty-two. [pause] But note this: almost all of "
    "its sales — around ninety-nine point seven five percent — are wholesale, business-to-business. That means it depends on a handful of "
    "large retail customers, which is a concentration risk."),
  "fin":{"kicker":"FINANCIALS","title":"The Numbers","stats":[
    {"label":"Revenue FY25","to":60,"prefix":"₹","suffix":" Cr","color":"#34D399","sub":"≈ ₹60.28 Cr (from ₹28.90 Cr)"},
    {"label":"Net Profit FY25","to":6,"prefix":"₹","suffix":" Cr","color":"#34D399","sub":"≈ ₹5.81 Cr (from ₹0.48 Cr)"},
    {"label":"Issue size","to":67,"prefix":"₹","suffix":" Cr","color":"#22D3EE","sub":"band ₹148–156 · NSE SME"}],
    "note":"Revenue doubled and profit jumped sharply — but off a tiny base, and garment margins are thin."},
  "n_fin":("Now the financials. [pause] Revenue roughly doubled, from about twenty-nine crore to sixty point two eight crore, and net profit "
    "jumped from under half a crore to about five point eight one crore. [pause] That's rapid growth — but keep it in proportion: it's off a "
    "very small base, and garment manufacturing is a thin-margin trade. [pause] So it's a fast-growing micro-company, not a proven, "
    "large-scale business."),
  "issue":{"kicker":"WHERE THE MONEY GOES","title":"Fresh Issue vs Offer-for-Sale","stats":[
    {"label":"Total issue","to":67,"prefix":"₹","suffix":" Cr","color":"#EC4899","sub":"~₹67 Cr"},
    {"label":"Fresh (into company)","to":54,"prefix":"₹","suffix":" Cr","color":"#34D399","sub":"₹53.94 Cr · ~80% funds business"},
    {"label":"OFS (to sellers)","to":13,"prefix":"₹","suffix":" Cr","color":"#F87171","sub":"~20% — a small sell-down"}],
    "note":"Mostly fresh — about four-fifths funds the company; a healthy structure."},
  "n_issue":("Where does your money go? [pause] Of the roughly sixty-seven crore issue, about fifty-four crore — some eighty percent — is a "
    "fresh issue that goes into the company. [pause] The remaining thirteen crore or so is an Offer for Sale — a small sell-down by existing "
    "owners. [pause] So this is a mostly-fresh issue, which is the healthier structure — four-fifths of your money funds the business."),
  "proceeds":{"kicker":"USE OF THE FRESH MONEY","title":"What the Fresh Money Funds","color":"#EC4899","items":[
    {"emoji":"🔄","k":"Working capital","v":"An OEM needs cash to buy fabric and fund orders, so the bulk supports working capital","chip":"WC"},
    {"emoji":"🏭","k":"Capacity & operations","v":"Part supports capacity and day-to-day operations as it scales","chip":"CAPACITY"},
    {"emoji":"🧰","k":"General corporate","v":"The balance is for general corporate purposes","chip":"GCP"},
  ]},
  "n_proceeds":("What does the fresh money fund? [pause] Mostly working capital. That matters, because a garment O-E-M ties up a lot of cash "
    "buying fabric and funding big orders before it gets paid. [pause] Part supports capacity and operations as it grows, and the rest is "
    "general corporate purposes. [pause] It's a sensible, growth-oriented use — but it also tells you this is a working-capital-hungry "
    "business that constantly needs cash."),
  "peers":{"variant":"sm_iconcards","props":{"kicker":"COMPETITORS · VALUATION","title":"Small Garment OEM — Few Direct Peers","color":"#EC4899","items":[
    {"emoji":"👔","k":"Big listed exporters, not peers","v":"Gokaldas Exports and Pearl Global are large LISTED garment makers — useful for scale, but far bigger and export-led, not direct peers","chip":"NOT DIRECT"},
    {"emoji":"⚖️","k":"A thin-margin, competitive trade","v":"Garment OEM is low-margin and crowded; success rides on order visibility and a few large customers","chip":"LOW MARGIN"},
    {"emoji":"🧾","k":"No clean SME P/E","v":"There's no like-for-like listed twin at this size, so a peer P/E comparison isn't meaningful — weigh the price against its small, young profit base","chip":"WATCH PRICE"},
  ]},
    "narr":("Now — the competitors. [pause] Fascinate is a small, business-to-business garment maker, and it doesn't have a clean listed "
      "twin. [pause] The big listed names in garments — Gokaldas Exports, Pearl Global — are far larger and export-led, so they're useful "
      "only as a sense of scale, not as direct peers. [pause] Garment manufacturing is a thin-margin, competitive trade that leans on a few "
      "large customers. And with no comparable listed company at this size, there's no meaningful peer P-E — so judge it on its order book "
      "and margins, not on a valuation multiple against rivals.")},
  "verdict":{"kicker":"SHOULD YOU SUBSCRIBE?","title":"Strengths vs Watch-outs","mythLabel":"⚠️ WATCH-OUTS","factLabel":"✅ STRENGTHS","pairs":[
    {"m":"~99.75% B2B — customer concentration risk","f":"Revenue doubled; profit jumped sharply"},
    {"m":"Thin garment margins; tiny SME","f":"~80% fresh — funds the business"},
    {"m":"Big ~₹2.5 lakh minimum bid; thin liquidity","f":"Multi-category spread; organised-retail demand"}],
  },
  "n_verdict":("Should you subscribe? [pause] The strengths — revenue doubled, profit jumped, and about eighty percent is fresh money funding "
    "the company across a spread of clothing categories. [pause] The watch-outs — nearly all its sales are to a few large customers, garment "
    "margins are thin, and it's a tiny S-M-E with a big minimum bid and thin trading. [pause] The takeaway — fast growth off a small base "
    "with a clean structure, but a concentrated, thin-margin micro-cap. Size it accordingly."),
  "sme_exchange":"NSE SME","sme_lot":"1,600 shares","sme_min":"about ₹2.5 lakh",
  "n_apply":("Now — how do you apply, and how does an S-M-E I-P-O differ? [pause] Fascinate lists on the N-S-E S-M-E platform, separate from "
    "the mainboard, with its own rules and risks. [pause] The big difference is the minimum. One lot here is sixteen hundred shares — about "
    "two and a half lakh rupees. That's far more than a mainboard I-P-O, where fifteen thousand gets you in. [pause] And S-M-E stocks are "
    "volatile and thinly traded, so invest only what you can afford to lock up. [pause] Track the live subscription on the N-S-E S-M-E page, "
    "Chittorgarh, or your broker app — allotment is by lottery if it's oversubscribed."),
  "recap":{"title":"Fascinate Textiles IPO — at a Glance","items":[
    "Business: B2B readymade garment OEM (kids/men/infant)","FY25: revenue ₹60.28 Cr, profit ₹5.81 Cr (both jumped)",
    "₹67 Cr issue — ~80% fresh; NSE SME","No direct listed peer — no meaningful P/E","SME min ~₹2.5 lakh · GMP flat at open (unofficial)"],
    "closer":"Fast-growing off a tiny base with a clean structure — but a thin-margin, concentrated SME. Read the RHP; decide for yourself."},
  "n_recap_pre":("Let's recap Fascinate Textiles. [pause] A small business-to-business garment maker for organised retailers, growing fast off "
    "a tiny base — revenue doubled and profit jumped. [pause] The issue is about eighty percent fresh, mainly funding working capital. [pause] "
    "But nearly all its sales go to a few big customers, margins are thin, and there's no listed peer to benchmark the price. The S-M-E "
    "minimum is about two and a half lakh rupees. [pause] "),
},

"shamfoam": {
  "accent":"#22D3EE","name":"Sham Foam IPO","kicker":"SME IPO ANALYSIS · NSE SME",
  "sub":"Foam & furniture maker · ₹40 Cr · NSE SME · 11–13 Aug 2026",
  "n_title":("Let's break down the Sham Foam I-P-O — a small, forty-crore S-M-E issue from a foam and furniture maker in Haryana. [pause] "
    "We'll cover what it does, its financials, where the money goes, how it stacks up against the big listed name, and how much you'd need "
    "to apply. [pause] This is education, not investment advice."),
  "biz":{"kicker":"WHAT THE COMPANY DOES","title":"Inside Sham Foam","color":"#22D3EE","items":[
    {"emoji":"🛏️","k":"Foam & furniture maker","v":"Manufactures foam-based products and furniture from its base in Ambala, Haryana","chip":"FOAM"},
    {"emoji":"🛢️","k":"Input-cost linked","v":"Foam is made from crude-linked chemicals, so raw-material costs — and margins — swing with oil prices","chip":"CRUDE-LINKED"},
    {"emoji":"📦","k":"Fixed-price SME issue","v":"A fixed-price issue at ₹130 a share — a small, lightly-covered offering on the NSE SME platform","chip":"FIXED ₹130"},
  ]},
  "n_biz":("So what does Sham Foam do? [pause] It manufactures foam-based products and furniture, from its base in Ambala, Haryana. [pause] "
    "One thing to understand about foam: it's made from chemicals whose prices track crude oil. So the company's raw-material costs — and "
    "therefore its margins — swing with oil prices, which is a real risk. [pause] And this is a fixed-price S-M-E issue at a hundred and "
    "thirty rupees a share — a small, lightly-covered offering, so expect thin research and thin trading."),
  "fin":{"kicker":"FINANCIALS","title":"The Numbers","stats":[
    {"label":"Revenue FY24","to":81,"prefix":"₹","suffix":" Cr","color":"#34D399","sub":"≈ ₹81.15 Cr (full year)"},
    {"label":"Net Profit FY24","to":4,"prefix":"₹","suffix":" Cr","color":"#FBBF24","sub":"≈ ₹3.58 Cr — thin ~4% margin"},
    {"label":"Issue size","to":40,"prefix":"₹","suffix":" Cr","color":"#22D3EE","sub":"fixed ₹130 · NSE SME"}],
    "note":"A reasonable revenue base but a thin ~4% profit margin — and recent figures look lumpy across periods. Read the RHP carefully."},
  "n_fin":("Now the financials. [pause] For the year to March twenty twenty-four, revenue was about eighty-one crore, with net profit of "
    "roughly three point five eight crore. [pause] Notice the margin — profit is only about four percent of revenue, which is thin. [pause] "
    "And the recent numbers look lumpy across reporting periods, so read the offer document carefully to understand the trend before you "
    "form a view."),
  "issue":{"kicker":"WHERE THE MONEY GOES","title":"A 100% Fresh Issue","stats":[
    {"label":"Total issue","to":40,"prefix":"₹","suffix":" Cr","color":"#22D3EE","sub":"₹40 Cr · fixed ₹130"},
    {"label":"Fresh (into company)","to":40,"prefix":"₹","suffix":" Cr","color":"#34D399","sub":"100% — funds the business"},
    {"label":"OFS (to sellers)","to":0,"prefix":"₹","suffix":" Cr","color":"#34D399","sub":"none — no promoter sell-down"}],
    "note":"The best possible structure: a 100% fresh issue. Every rupee raised goes INTO the company — no promoter cashes out."},
  "n_issue":("Where does your money go? [pause] And here Sham Foam has the best possible answer — this is a hundred percent fresh issue. "
    "[pause] There's no offer for sale at all. Every rupee raised goes into the company, not into a promoter's pocket. [pause] For a small, "
    "growing manufacturer that needs capital, that's exactly the structure you want to see."),
  "proceeds":{"kicker":"USE OF THE FRESH MONEY","title":"What the ₹40 Cr Funds","color":"#22D3EE","items":[
    {"emoji":"🔄","k":"Working capital","v":"Most of the fresh money funds working capital for its manufacturing operations","chip":"WC"},
    {"emoji":"🏭","k":"Capacity","v":"Part supports capacity and equipment to make more product","chip":"CAPACITY"},
    {"emoji":"🧰","k":"General corporate","v":"The balance is for general corporate purposes","chip":"GCP"},
  ]},
  "n_proceeds":("What does the fresh money fund? [pause] Mostly working capital, which a manufacturing business ties up in raw materials and "
    "inventory. [pause] Part supports capacity and equipment so it can make more product, and the rest is general corporate purposes. [pause] "
    "So the money is aimed at running and growing the business — the right use for a young manufacturer."),
  "peers":{"variant":"sm_iconcards","props":{"kicker":"COMPETITORS · VALUATION","title":"Sheela Foam Is the Big Name — Not a Peer","color":"#22D3EE","items":[
    {"emoji":"🛌","k":"Sheela Foam (Sleepwell)","v":"The dominant LISTED foam & mattress maker (Sleepwell). It's vastly larger and branded — a scale reference, not a like-for-like peer for a tiny SME","chip":"REFERENCE"},
    {"emoji":"🛢️","k":"Input-cost sensitive","v":"Foam uses crude-linked chemicals, so margins swing with oil prices; furniture is competitive and commoditised","chip":"CRUDE-LINKED"},
    {"emoji":"⚖️","k":"No clean SME P/E","v":"No reliable listed twin at this size means a P/E comparison isn't meaningful — weigh the fixed ₹130 price against its small, uneven profit","chip":"WATCH PRICE"},
  ]},
    "narr":("Now — the competitors. [pause] The obvious listed name in foam is Sheela Foam, the company behind Sleepwell. But it's vastly "
      "bigger and branded, so it's a reference for scale, not a real peer for a tiny S-M-E like this. [pause] As we said, foam is made from "
      "crude-linked chemicals, so margins move with oil prices, and furniture is a competitive, commoditised trade. [pause] With no "
      "comparable listed company at this size, there's no meaningful P-E to compare — so weigh the fixed price of one hundred and thirty "
      "rupees against Sham Foam's small and rather uneven profits, and read the offer document carefully.")},
  "verdict":{"kicker":"SHOULD YOU SUBSCRIBE?","title":"Strengths vs Watch-outs","mythLabel":"⚠️ WATCH-OUTS","factLabel":"✅ STRENGTHS","pairs":[
    {"m":"Thin ~4% margins; lumpy recent numbers","f":"100% fresh — all money funds the company"},
    {"m":"Input costs track crude — margins swing","f":"Reasonable revenue base (~₹81 Cr FY24)"},
    {"m":"Tiny SME; big minimum bid; thin liquidity","f":"No promoter sell-down"}],
  },
  "n_verdict":("Should you subscribe? [pause] The strengths — it's a hundred percent fresh issue with no promoter cashing out, and it has a "
    "reasonable revenue base of about eighty crore. [pause] The watch-outs — margins are thin at around four percent, the recent numbers are "
    "lumpy, its costs swing with crude oil, and it's a tiny S-M-E with a big minimum bid and thin trading. [pause] The takeaway — a "
    "cleanly-structured micro-cap, but a thin-margin, input-cost-sensitive one. Read the offer document closely before you decide."),
  "sme_exchange":"NSE SME","sme_lot":"1,000 shares (₹1.30 lakh)","sme_min":"about ₹2.60 lakh (2 lots)",
  "n_apply":("Now — how to apply, and how S-M-E I-P-Os differ. [pause] Sham Foam lists on the N-S-E S-M-E platform, separate from the "
    "mainboard. [pause] The minimum is large. One lot is a thousand shares — about one lakh thirty thousand rupees — and the smallest retail "
    "application is two lots, roughly two lakh sixty thousand rupees. That's a big ticket versus a mainboard I-P-O. [pause] And remember, "
    "S-M-E stocks are volatile and lightly traded, so only commit money you can lock away. [pause] Track the live subscription on the N-S-E "
    "S-M-E page, Chittorgarh, or your broker app — allotment is by lottery if oversubscribed."),
  "recap":{"title":"Sham Foam IPO — at a Glance","items":[
    "Business: foam & furniture maker, Ambala","FY24: revenue ₹81.15 Cr, profit ₹3.58 Cr (thin margin)",
    "₹40 Cr issue — 100% FRESH; NSE SME, fixed ₹130","No listed peer at its size — no meaningful P/E","SME min ~₹2.60 lakh · GMP flat at open (unofficial)"],
    "closer":"A cleanly-structured, all-fresh micro-cap — but thin-margin, input-cost sensitive and lumpy. Read the RHP; decide for yourself."},
  "n_recap_pre":("Let's recap Sham Foam. [pause] A foam and furniture maker from Ambala, with a reasonable revenue base but thin, lumpy "
    "profits. [pause] The best feature is the structure — a hundred percent fresh issue, no promoter selling. [pause] But margins are thin "
    "and swing with crude, there's no listed peer to benchmark, and the S-M-E minimum is about two lakh sixty thousand rupees. [pause] "),
},

"pramodini": {
  "accent":"#34D399","name":"Pramodini Medicare IPO","kicker":"SME IPO ANALYSIS · SME",
  "sub":"Diagnostics chain · ₹69 Cr · 12–14 Aug 2026",
  "n_title":("Let's break down the Pramodini Medicare I-P-O — a sixty-nine crore S-M-E issue from a diagnostics company. [pause] It's "
    "unusually profitable for its size, and we'll see how it compares to the big listed diagnostics names. We'll cover the business, the "
    "financials, the money trail, the competitors, and how to apply. [pause] This is education, not investment advice."),
  "biz":{"kicker":"WHAT THE COMPANY DOES","title":"Inside Pramodini Medicare","color":"#34D399","items":[
    {"emoji":"🩻","k":"Diagnostics services","v":"Provides technology-enabled radiology, pathology and nuclear-medicine diagnostics","chip":"DIAGNOSTICS"},
    {"emoji":"🏥","k":"Hospital & PPP model","v":"Runs services through hospitals, public-private-partnership projects, PSUs and standalone centres — contract-driven","chip":"PPP · CONTRACTS"},
    {"emoji":"📈","k":"Small but growing","v":"A regional player scaling its diagnostics footprint on India's rising healthcare demand","chip":"GROWTH"},
  ]},
  "n_biz":("So what does Pramodini do? [pause] It provides diagnostics services — radiology, pathology and nuclear medicine — using "
    "technology-enabled systems. [pause] Importantly, it runs these through hospitals, public-private-partnership projects, government PSUs "
    "and its own standalone centres. So it's a contract-driven business, not a chain of branded walk-in labs. [pause] It's a regional player "
    "scaling its footprint on India's rising demand for healthcare and diagnostics."),
  "fin":{"kicker":"FINANCIALS","title":"The Numbers","stats":[
    {"label":"Revenue FY25","to":39,"prefix":"₹","suffix":" Cr","color":"#34D399","sub":"≈ ₹38.55 Cr (from ₹35.79 Cr)"},
    {"label":"Net Profit FY25","to":10,"prefix":"₹","suffix":" Cr","color":"#34D399","sub":"≈ ₹10.04 Cr (+74% YoY)"},
    {"label":"Issue size","to":69,"prefix":"₹","suffix":" Cr","color":"#22D3EE","sub":"₹69.04 Cr · band ₹110–118"}],
    "note":"Modest revenue but a strong ~26% net margin, and profit up 74% — unusually profitable for a company this size."},
  "n_fin":("Now the financials, and they stand out. [pause] Revenue was modest — about thirty-eight point five five crore, up from thirty-six "
    "— but net profit was around ten crore, up a sharp seventy-four percent. [pause] Do the maths and that's a net margin near twenty-six "
    "percent, which is genuinely high for a company this small. [pause] So it's small, but unusually profitable — the key question is whether "
    "those contract-driven margins can hold as it grows."),
  "issue":{"kicker":"WHERE THE MONEY GOES","title":"Fresh Issue vs Offer-for-Sale","stats":[
    {"label":"Total issue","to":69,"prefix":"₹","suffix":" Cr","color":"#34D399","sub":"₹69.04 Cr"},
    {"label":"Fresh (into company)","to":63,"prefix":"₹","suffix":" Cr","color":"#34D399","sub":"~91% funds the business"},
    {"label":"OFS (to sellers)","to":6,"prefix":"₹","suffix":" Cr","color":"#F87171","sub":"~9% — ~5.0 lakh shares"}],
    "note":"Mostly fresh — about nine-tenths funds the company; a healthy structure."},
  "n_issue":("Where does your money go? [pause] Of the sixty-nine crore issue, roughly sixty-three crore — about ninety-one percent — is a "
    "fresh issue that goes into the company. [pause] Only a small slice, around six crore from about five lakh shares, is an Offer for Sale "
    "by existing holders. [pause] So this is a mostly-fresh issue — nine-tenths of your money funds the business, which is the healthier "
    "structure."),
  "proceeds":{"kicker":"USE OF THE FRESH MONEY","title":"What the Fresh Money Funds","color":"#34D399","items":[
    {"emoji":"🏭","k":"Equipment & centres","v":"Fresh money funds diagnostic equipment and expands its centres and contracts","chip":"CAPEX"},
    {"emoji":"🔄","k":"Working capital","v":"Supports working capital for its contract and PPP operations","chip":"WC"},
    {"emoji":"🧰","k":"General corporate","v":"The balance is for general corporate purposes","chip":"GCP"},
  ]},
  "n_proceeds":("What does the fresh money fund? [pause] Diagnostic equipment and expanding its centres and contracts — the capital a "
    "diagnostics business needs to grow. [pause] It also supports working capital for its contract and P-P-P operations, and the rest is "
    "general corporate purposes. [pause] So the money goes to genuine expansion — the right use for a small, profitable, growing company."),
  "peers":{"variant":"sm_iconcards","props":{"kicker":"COMPETITORS · VALUATION","title":"Big Diagnostics Names — For Scale Only","color":"#34D399","items":[
    {"emoji":"🧪","k":"Dr Lal PathLabs & Metropolis","v":"The large LISTED diagnostics chains. They trade richly — often around 50–60× — but are national brands many times Pramodini's size: a reference, not a direct peer","chip":"REFERENCE ~50–60×"},
    {"emoji":"🏥","k":"A regional, PPP-led player","v":"Pramodini is smaller and more contract-driven than the branded chains, so its economics differ","chip":"DIFFERENT MODEL"},
    {"emoji":"📈","k":"Strong margins, tiny scale","v":"A ~26% net margin and +74% profit are impressive — but at SME size, judge it on contract renewals, not a peer P/E","chip":"SME SCALE"},
  ]},
    "narr":("Now — the competitors. [pause] The big listed names in diagnostics are Dr Lal PathLabs and Metropolis. They command rich "
      "valuations — often around fifty to sixty times earnings — but they're national brands many times Pramodini's size, so they're a "
      "reference for what the sector can fetch, not direct peers. [pause] Pramodini is a smaller, contract-and-P-P-P-driven player, so its "
      "economics differ. [pause] What really stands out is its profitability — a net margin near twenty-six percent and profit up "
      "seventy-four percent. Impressive — but at this tiny scale, judge it on whether those contracts renew, rather than on a peer P-E.")},
  "verdict":{"kicker":"SHOULD YOU SUBSCRIBE?","title":"Strengths vs Watch-outs","mythLabel":"⚠️ WATCH-OUTS","factLabel":"✅ STRENGTHS","pairs":[
    {"m":"Tiny SME; contract/PPP concentration","f":"Strong ~26% net margin; profit +74%"},
    {"m":"Modest revenue growth (~8%)","f":"~91% fresh — funds the business"},
    {"m":"Big ~₹1.4 lakh minimum bid; thin liquidity","f":"Rides rising healthcare demand"}],
  },
  "n_verdict":("Should you subscribe? [pause] The strengths — it's unusually profitable for its size, with a net margin near twenty-six "
    "percent and profit up seventy-four percent, and about ninety percent is fresh money funding the business. [pause] The watch-outs — it's "
    "a tiny S-M-E with contract and P-P-P concentration, revenue growth is modest, and there's a big minimum bid with thin trading. [pause] "
    "The takeaway — an unusually profitable, cleanly-structured micro-cap, but small and contract-dependent. Judge it on whether those "
    "contracts renew."),
  "sme_exchange":"the SME platform","sme_lot":"1,200 shares","sme_min":"about ₹1.42 lakh",
  "n_apply":("Now — how to apply, and how S-M-E I-P-Os differ. [pause] Pramodini lists on the S-M-E platform, separate from the mainboard, "
    "with its own rules and risks. [pause] The minimum is large. One lot is twelve hundred shares — about one lakh forty-two thousand rupees "
    "— far above a mainboard I-P-O. [pause] And S-M-E stocks are volatile and thinly traded, so invest only what you can afford to lock up. "
    "[pause] Track the live subscription on the N-S-E and B-S-E S-M-E pages, Chittorgarh, or your broker app — allotment is by lottery if "
    "oversubscribed."),
  "recap":{"title":"Pramodini Medicare IPO — at a Glance","items":[
    "Business: radiology/pathology diagnostics (hospital & PPP)","FY25: revenue ₹38.55 Cr, profit ₹10.04 Cr (+74%)",
    "₹69.04 Cr issue — ~91% fresh","Big chains (Dr Lal/Metropolis) are references, not peers","SME min ~₹1.42 lakh · GMP flat at open (unofficial)"],
    "closer":"Unusually profitable for its size with a clean structure — but a tiny, contract-driven SME. Read the RHP; decide for yourself."},
  "n_recap_pre":("Let's recap Pramodini Medicare. [pause] A small, contract-and-P-P-P-driven diagnostics company that's unusually profitable "
    "— a net margin near twenty-six percent and profit up seventy-four percent. [pause] The issue is about ninety percent fresh, funding "
    "equipment and expansion. [pause] The big listed chains like Dr Lal and Metropolis are references for scale, not direct peers, so judge "
    "it on its own contracts. The S-M-E minimum is about one lakh forty-two thousand rupees. [pause] "),
},
}

# ===== BATCH 5 — "Clients, Business & Order Book" beat (from each RHP/DRHP) =====================
# Injected into each IPO dict below as c["clients"]; make_ipo/make_sme_ipo emit it after the biz beat.
CLIENTS = {
"dhoot": {"variant":"sm_iconcards","props":{"kicker":"BUSINESS DEEP-DIVE · CLIENTS & ORDER BOOK","title":"Who Buys From Dhoot","color":"#38BDF8","items":[
    {"emoji":"🤝","k":"Marquee auto-OEM clients","v":"Bajaj Auto is its biggest customer at ~32% of FY26 revenue, then TVS (~20%), Honda (~11%), Royal Enfield and Suzuki","chip":"BAJAJ ~32%"},
    {"emoji":"🏭","k":"A global, full-stack supplier","v":"Beyond harnesses it makes battery packs, sensors, switches and EV electronics — from 22 plants across India, the UK, Slovakia and Thailand","chip":"22 PLANTS · 4 COUNTRIES"},
    {"emoji":"⚠️","k":"No order book, but concentrated","v":"Auto-parts run on long-term OEM supply programs, not a quoted order book — and the top 5 customers are ~71.6% of revenue, a real concentration risk","chip":"TOP-5 = 71.6%"}]},
  "narr":("Let's go deeper on the business. [pause] Who actually buys from Dhoot? Its biggest client is Bajaj Auto — about thirty-two "
    "percent of revenue — then T-V-S at twenty percent, Honda at eleven, plus Royal Enfield and Suzuki. [pause] Beyond wiring harnesses "
    "it also makes battery packs, sensors, switches and E-V electronics, from twenty-two plants across India, the U-K, Slovakia and "
    "Thailand. [pause] On order book — auto-parts don't quote one; they run on long-term supply programs with these OEMs. But the flip "
    "side is concentration: the top five customers are about seventy-two percent of revenue, so losing one would hurt.")},
"molbio": {"variant":"sm_iconcards","props":{"kicker":"BUSINESS DEEP-DIVE · CLIENTS & ORDER BOOK","title":"Who Uses Molbio's Truenat","color":"#2DD4BF","items":[
    {"emoji":"🏛️","k":"Governments & public health","v":"Truenat is ICMR-validated and built into India's National TB Elimination Programme — governments are its anchor customers","chip":"GOVT ANCHOR"},
    {"emoji":"🌍","k":"WHO-endorsed, 100+ countries","v":"One of only two rapid molecular TB platforms endorsed by the WHO; Truenat is patented in over 100 countries and used well beyond India","chip":"100+ COUNTRIES"},
    {"emoji":"🔁","k":"Installed base, not an order book","v":"A device maker has no order book — it earns recurring revenue from test cartridges across a large installed base (TB, HIV, dengue, hepatitis & more)","chip":"RECURRING KITS"}]},
  "narr":("Let's go deeper. [pause] Who uses Molbio's Truenat? Its anchor customers are governments and public-health programs — the "
    "platform is I-C-M-R validated and built into India's National T-B Elimination Programme. [pause] It's also one of only two rapid "
    "molecular T-B platforms endorsed by the World Health Organization, patented in more than a hundred countries and used well beyond "
    "India. [pause] On order book — a device maker doesn't have one. Instead it earns recurring revenue from test cartridges across a "
    "large installed base of machines, for T-B, H-I-V, dengue, hepatitis and more. That razor-and-blade tail is the real prize.")},
"milkymist": {"variant":"sm_iconcards","props":{"kicker":"BUSINESS DEEP-DIVE · REACH & PRODUCTS","title":"How Milky Mist Reaches You","color":"#FBBF24","items":[
    {"emoji":"🚚","k":"A deep distribution network","v":"~3,000 distributors, 44 depots and 3.5 lakh-plus retail touchpoints across 22 states — this reach is its real moat","chip":"3.5 LAKH+ OUTLETS"},
    {"emoji":"🏪","k":"Many sales channels","v":"General trade, modern trade, HoReCa, e-commerce and 108 exclusive parlours — plus exports to 15-plus countries","chip":"5 CHANNELS"},
    {"emoji":"🧀","k":"Daily-consumption products","v":"About 75% of revenue is everyday items — paneer, curd, yogurt, ghee and butter — which repeat far more than occasional treats","chip":"~75% DAILY-USE"}]},
  "narr":("Let's go deeper on the business. [pause] Milky Mist's real strength is its reach. It sells through around three thousand "
    "distributors, forty-four depots and more than three and a half lakh retail touchpoints across twenty-two states. [pause] It reaches "
    "you through many channels — general trade, modern trade, hotels and restaurants, e-commerce, and a hundred and eight exclusive "
    "parlours — and it even exports to more than fifteen countries. [pause] As a food business there's no order book; what matters is "
    "repeat demand. And here about seventy-five percent of revenue is everyday items — paneer, curd, yogurt, ghee and butter — bought "
    "again and again.")},
"shiprocket": {"variant":"sm_iconcards","props":{"kicker":"BUSINESS DEEP-DIVE · MERCHANTS & VOLUME","title":"Who's On the Shiprocket Platform","color":"#A78BFA","items":[
    {"emoji":"🧑‍💼","k":"~2.15 lakh active merchants","v":"In FY26 it served about 2.15 lakh active merchants — mostly small and D2C sellers — reaching 155 million-plus end consumers across 19,000+ pin codes","chip":"2.15 LAKH SELLERS"},
    {"emoji":"📦","k":"Volume, not an order book","v":"As a platform there's no order book — instead it processes 25 million-plus shipments a month and around 200 million transactions a year","chip":"25M+ /MONTH"},
    {"emoji":"🚀","k":"D2C is the growth engine","v":"Small and solo sellers are ~60% of the base; venture-backed D2C brands in beauty, fashion and electronics are the fastest-growing revenue","chip":"D2C FASTEST"}]},
  "narr":("Let's go deeper. [pause] Who's actually on the platform? In FY twenty twenty-six, Shiprocket served about two point one five "
    "lakh active merchants — mostly small and D-2-C sellers — reaching over a hundred and fifty-five million end consumers across "
    "nineteen thousand-plus pin codes. [pause] As a platform there's no order book; the scale metric is volume — it processes more than "
    "twenty-five million shipments a month and around two hundred million transactions a year. [pause] Small and solo sellers are about "
    "sixty percent of the base, while venture-backed D-2-C brands in beauty, fashion and electronics are its fastest-growing revenue.")},
"beharilal": {"variant":"sm_iconcards","props":{"kicker":"BUSINESS DEEP-DIVE · CLIENTS & ORDER BOOK","title":"Clients & Order Book","color":"#F97316","items":[
    {"emoji":"🏢","k":"1,825 customers, many industries","v":"Serves ~1,825 domestic and international customers across steel, automobile, mining, infrastructure, power, aerospace-and-defence and cement","chip":"1,825 CLIENTS"},
    {"emoji":"🛠️","k":"Four product verticals","v":"Beyond metal rolls it makes castings, alloy-steel products and forgings — an integrated maker and trader from two plants in Mandi Gobindgarh, Punjab","chip":"4 VERTICALS"},
    {"emoji":"📘","k":"Order book ₹178.57 Cr","v":"As of 31 May 2026 its order book stood at about ₹178.57 crore — genuine forward visibility that several other names this week don't disclose","chip":"₹178.57 Cr"}]},
  "narr":("Let's go deeper — and here we finally get real order-book visibility. [pause] Behari Lal serves about eighteen hundred and "
    "twenty-five customers, domestic and international, across steel, automobiles, mining, infrastructure, power, aerospace-and-defence "
    "and cement — nicely diversified. [pause] Beyond metal rolls it makes castings, alloy-steel products and forgings, as an integrated "
    "maker and trader from two plants in Mandi Gobindgarh, Punjab. [pause] And its order book — as of the end of May twenty twenty-six — "
    "stood at about one hundred and seventy-eight crore. That's genuine forward visibility, which several other names this week simply "
    "don't disclose.")},
"fascinate": {"variant":"sm_iconcards","props":{"kicker":"BUSINESS DEEP-DIVE · CLIENTS & ORDERS","title":"Clients & How It Works","color":"#EC4899","items":[
    {"emoji":"🏬","k":"Large-format retailers & wholesalers","v":"Almost all revenue (~99.75%) is B2B — an OEM partner to organised retailers and wholesalers, in India and abroad","chip":"~99.75% B2B"},
    {"emoji":"✅","k":"Made only to confirmed orders","v":"It manufactures only after sample approval and a confirmed purchase order — demand-driven production is its version of an order book","chip":"MAKE-TO-ORDER"},
    {"emoji":"🧵","k":"Integrated, part-outsourced","v":"Cutting, printing, finishing, QC and sampling in-house; knitting, dyeing and some stitching outsourced — across infant, kids, men's and women's wear","chip":"IN-HOUSE + OUTSOURCED"}]},
  "narr":("Let's go deeper on the business. [pause] Who are its clients? Almost all of Fascinate's revenue — about ninety-nine point "
    "seven five percent — is business-to-business. It's an O-E-M partner to large-format retailers and wholesalers, in India and abroad. "
    "[pause] Instead of a fixed order book, it works make-to-order: it manufactures only after a sample is approved and a purchase order "
    "is confirmed, so production is demand-driven. [pause] It keeps the value-added steps — cutting, printing, finishing, quality control "
    "and sampling — in-house, and outsources knitting, dyeing and some stitching, across infant, kids, men's and women's wear.")},
"shamfoam": {"variant":"sm_iconcards","props":{"kicker":"BUSINESS DEEP-DIVE · PRODUCTS & CUSTOMERS","title":"Products & Customers","color":"#22D3EE","items":[
    {"emoji":"🛏️","k":"Mattresses & PU foam","v":"Makes memory-foam, hybrid and orthopedic mattresses and PU-foam products from Ambala, Haryana — led by the founding Jindal family","chip":"MATTRESSES"},
    {"emoji":"🏪","k":"Dealer & direct-to-home sales","v":"Sells through dealers and direct factory delivery, backed by long warranties — a branded, distribution-led mattress market","chip":"DEALERS + D2H"},
    {"emoji":"ℹ️","k":"No disclosed order book","v":"As a make-to-stock manufacturer it doesn't quote an order book — judge it on its revenue trend and margins, not forward orders","chip":"MAKE-TO-STOCK"}]},
  "narr":("Let's go deeper. [pause] Sham Foam makes mattresses — memory-foam, hybrid and orthopedic — and P-U foam products, from Ambala "
    "in Haryana, led by its founders, the Jindal family. [pause] It sells through dealers and direct factory delivery, backed by long "
    "warranties, competing in a branded, distribution-led mattress market. [pause] On order book — as a make-to-stock manufacturer it "
    "doesn't disclose one. So judge this one on its revenue trend and margins, rather than on any forward-order visibility.")},
"pramodini": {"variant":"sm_iconcards","props":{"kicker":"BUSINESS DEEP-DIVE · CLIENTS & CONTRACTS","title":"Clients & Contracts","color":"#34D399","items":[
    {"emoji":"🏥","k":"Hospitals, PSUs & med colleges","v":"Serves public and private hospitals, PSUs, medical colleges and standalone centres across Tier 1, 2 and 3 cities","chip":"MULTI-CLIENT"},
    {"emoji":"📘","k":"16 centres on long-term contracts","v":"Runs 16 diagnostic centres across 7 states via PPP, PSU and private partnerships — those long-term contracts are its order-book equivalent","chip":"16 CENTRES · 7 STATES"},
    {"emoji":"🩻","k":"Serious diagnostic hardware","v":"Operates 8 CT, 7 MRI, 20 X-ray and a PET-CT, plus a 24×7 teleradiology hub and central lab in Vijayawada","chip":"MRI · CT · PET-CT"}]},
  "narr":("Let's go deeper. [pause] Who are its clients? Pramodini serves public and private hospitals, government P-S-Us, medical "
    "colleges and standalone centres, across Tier one, two and three cities. [pause] Its order-book equivalent is its contracts: it runs "
    "sixteen diagnostic centres across seven states through public-private, P-S-U and private partnerships — long-term deals that give "
    "steady, recurring work. [pause] And it's backed by serious hardware — eight C-T scanners, seven M-R-I machines, twenty X-ray units "
    "and a PET-C-T, plus a twenty-four-seven teleradiology hub and a central lab in Vijayawada.")},
}
for _cid, _blk in CLIENTS.items():
    (IPOS.get(_cid) or SME_IPOS.get(_cid))["clients"] = _blk

CHAPTERS = {**{cid: make_ipo(cid, c) for cid, c in IPOS.items()},
            **{cid: make_sme_ipo(cid, c) for cid, c in SME_IPOS.items()}}

# ---- TTS + build machinery (identical to premarket build) --------------------------------------
def ffdur(path):
    out = subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","default=noprint_wrappers=1:nokey=1",path],capture_output=True,text=True,check=True)
    return round(float(out.stdout.strip()),3)

def tts_chunk(path, text):
    mp3 = path[:-4]+".mp3"
    for a in range(6):
        try:
            r = subprocess.run(["edge-tts","--voice",VOICE,f"--rate={RATE}","--text",text,"--write-media",mp3],capture_output=True,timeout=90)
        except subprocess.TimeoutExpired:
            if os.path.exists(mp3): os.remove(mp3)
            time.sleep(3+a*4); continue
        if r.returncode==0 and os.path.exists(mp3) and os.path.getsize(mp3)>0: break
        time.sleep(3+a*4)
    else: raise RuntimeError(f"tts failed {path}")
    subprocess.run(["ffmpeg","-y","-i",mp3,"-ar","24000","-ac","1",path],check=True,capture_output=True)
    os.remove(mp3)

def gen_one(seg_id, text):
    fin = os.path.join(FIN, seg_id+".wav")
    if os.path.exists(fin): return fin, ffdur(fin)
    chunks = [c.strip() for c in text.split("[pause]") if c.strip()]; paths=[]
    for ci,chunk in enumerate(chunks):
        cp = os.path.join(RAW, f"{seg_id}_c{ci}.wav")
        if not os.path.exists(cp): tts_chunk(cp, chunk)
        paths.append(cp)
    psil = os.path.join(RAW,"_pause.wav")
    if not os.path.exists(psil):
        subprocess.run(["ffmpeg","-y","-f","lavfi","-i","anullsrc=r=24000:cl=mono","-t",str(PAUSE),psil],check=True,capture_output=True)
    clist = os.path.join(RAW, f"{seg_id}_concat.txt")
    with open(clist,"w") as f:
        for i2,p2 in enumerate(paths):
            f.write(f"file '{p2}'\n")
            if i2 < len(paths)-1: f.write(f"file '{psil}'\n")
    subprocess.run(["ffmpeg","-y","-f","concat","-safe","0","-i",clist,"-c","copy",fin],check=True,capture_output=True)
    return fin, ffdur(fin)

def caption_cues(text, start, end):
    clean = re.sub(r"\s+"," ",text.replace("[pause]"," ")).strip()
    parts = re.split(r"(?<=[.?!])\s+", clean); cues=[]
    for pt in parts:
        pt=pt.strip()
        if not pt: continue
        if len(pt)>60 and ("," in pt or "—" in pt):
            buf=""
            for s in re.split(r"(?<=[,—])\s+", pt):
                if len(buf)+len(s)>60 and buf: cues.append(buf.strip()); buf=s
                else: buf=(buf+" "+s).strip()
            if buf: cues.append(buf.strip())
        else: cues.append(pt)
    total=sum(len(c) for c in cues) or 1; span,out,t=end-start,[],start
    for c in cues:
        d=span*(len(c)/total); out.append([round(t,3),round(t+d,3),c]); t+=d
    if out: out[-1][1]=round(end,3)
    return out

def build_chapter(ch):
    segs=CHAPTERS[ch]; manifest=[]
    for sid,variant,props,text in segs:
        path,dur=gen_one(sid,text)
        manifest.append({"id":sid,"variant":variant,"props":props,"wav":path,"duration":dur,"narration":text})
        print(f"  {sid:16s} {dur:6.2f}s",flush=True)
    silence=os.path.join(FIN,"_sil.wav")
    if not os.path.exists(silence):
        subprocess.run(["ffmpeg","-y","-f","lavfi","-i","anullsrc=r=24000:cl=mono","-t",str(GAP),silence],check=True,capture_output=True)
    clist=os.path.join(ROOT,f"concat_{ch}.txt")
    with open(clist,"w") as f:
        for i,m in enumerate(manifest):
            f.write(f"file '{m['wav']}'\n")
            if i<len(manifest)-1: f.write(f"file '{silence}'\n")
    subprocess.run(["ffmpeg","-y","-f","concat","-safe","0","-i",clist,"-c","copy",os.path.join(PUBLIC,f"{ch}.wav")],check=True,capture_output=True)
    cuts,cues,t=[],[],0.0
    for m in manifest:
        start,end=t,t+m["duration"]
        cuts.append({"id":m["id"],"type":m["variant"],"in_seconds":round(start,3),"out_seconds":round(end,3),"props":{**m["props"],"dur":round(m["duration"]+GAP,3)}})
        cues.extend(caption_cues(m["narration"],start,end)); t=end+GAP
    props={"cuts":cuts,"captions":cues,"audio":{"narration":{"src":f"{PREFIX}/{ch}.wav","volume":1.0}}}
    json.dump(props,open(os.path.join(ROOT,"artifacts",f"{ch}.json"),"w"),ensure_ascii=False,indent=2)
    print(f"{ch}: total {t-GAP:.2f}s ({(t-GAP)/60:.2f} min), {len(cuts)} scenes, {len(cues)} cues")

if __name__=="__main__":
    for ch in (sys.argv[1:] or list(CHAPTERS.keys())): build_chapter(ch)
