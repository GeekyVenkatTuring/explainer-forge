#!/usr/bin/env python3
"""Generate thumbnail props JSON + YouTube metadata for BATCH 6 (week of 17-23 Aug 2026 IPOs).
Chapter timestamps are derived from each artifact JSON so they stay accurate after the new
three-statement (sm_financials) beat was added."""
import json, os
ROOT = os.path.dirname(os.path.abspath(__file__))
ART = os.path.join(ROOT, "artifacts")
DELIV = os.path.join(ROOT, "delivery_batch6"); os.makedirs(DELIV, exist_ok=True)

BRAND = "ENGLISH · NEXT WEEK'S IPOs"

D = {
"horizon": {
  "accent":"#38BDF8","badge":"IPO ANALYSIS","title":"Horizon\nIndustrial Parks","sub":"Warehousing · ₹2,600 Cr · 100% Fresh · 17–19 Aug",
  "hook":"−₹204\nCr","hookSmall":"loss — at a ₹17,298 Cr price",
  "titles":["Horizon Industrial Parks IPO Review: 100% Fresh — But Loss-Making | Full Analysis",
            "Horizon Industrial Parks IPO (₹2,600 Cr): 3 Statements, ₹6,884 Cr Debt, Valuation",
            "Should You Apply? Blackstone's Horizon Industrial Parks IPO — Warehousing, Financials, Price"],
  "one":"Horizon Industrial Parks IPO — Blackstone-backed warehousing & industrial parks, ₹2,600 Cr (100% fresh), opens 17–19 Aug 2026.",
},
"lalithaa": {
  "accent":"#FBBF24","badge":"IPO ANALYSIS","title":"Lalithaa\nJewellery IPO","sub":"South-India jeweller · ₹1,700 Cr · 17–19 Aug",
  "hook":"~11×","hookSmall":"vs ~44× peers — cheaper",
  "titles":["Lalithaa Jewellery IPO Review: Cheaper Than Titan & Kalyan? | Full Analysis & P/E",
            "Lalithaa Jewellery Mart IPO (₹1,700 Cr): 3 Statements, Peer P/E, Fresh vs OFS, GMP",
            "Should You Apply? Lalithaa Jewellery IPO — Financials, Competitors, Valuation Explained"],
  "one":"Lalithaa Jewellery Mart IPO — South-India jewellery chain (56 stores), ₹1,700 Cr, opens 17–19 Aug 2026.",
},
"shankesh": {
  "accent":"#FB923C","badge":"IPO ANALYSIS","title":"Shankesh\nJewellers IPO","sub":"B2B gold jewellery · ₹367 Cr · 18–20 Aug",
  "hook":"+165%","hookSmall":"profit jump · asset-light",
  "titles":["Shankesh Jewellers IPO Review: Profit Up 165% — But No Peer | Full Analysis",
            "Shankesh Jewellers IPO (₹367 Cr): 3 Statements, Asset-Light Model, Fresh vs OFS, GMP",
            "Should You Apply? Shankesh Jewellers IPO — Financials, Valuation, Competitors Explained"],
  "one":"Shankesh Jewellers IPO — B2B asset-light handcrafted gold jewellery (Mumbai), ₹367.18 Cr, opens 18–20 Aug 2026.",
},
"sunshine": {
  "accent":"#A78BFA","badge":"IPO ANALYSIS","title":"Sunshine\nPictures IPO","sub":"Film & content · ₹282 Cr · 18–20 Aug",
  "hook":"~32×","hookSmall":"P/E on lumpy film profit",
  "titles":["Sunshine Pictures IPO Review: A Film Studio At 32× Earnings? | Full Analysis",
            "Sunshine Pictures IPO (₹282 Cr): 3 Statements, Lumpy Earnings, Fresh vs OFS, Valuation",
            "Should You Apply? Vipul Shah's Sunshine Pictures IPO — Financials & Price Explained"],
  "one":"Sunshine Pictures IPO — Vipul Shah's film/TV/web content house (Mumbai), ₹282.14 Cr, opens 18–20 Aug 2026.",
},
"gaja": {
  "accent":"#34D399","badge":"IPO ANALYSIS","title":"Gaja Capital\n(Alt. Asset Mgmt) IPO","sub":"India's 1st PE listing · ₹550 Cr · 19–21 Aug",
  "hook":"52%","hookSmall":"net margin · India's 1st PE IPO",
  "titles":["Gaja Capital IPO Review: India's FIRST Private-Equity Listing | Full Analysis",
            "Gaja Alternative Asset Mgmt IPO (₹550 Cr): 3 Statements, 52% Margin, Valuation, GMP",
            "Should You Apply? Gaja Capital IPO — How To Value A PE Firm, Fresh vs OFS Explained"],
  "one":"Gaja Alternative Asset Management (Gaja Capital) IPO — India's first home-grown PE/AIF manager to list, ₹550 Cr, opens 19–21 Aug 2026.",
},
}

LABELS = {"title":"Intro","biz":"What the company does","fin":"FY financials",
  "threestmt":"Income statement, balance sheet & cash flow","issue":"Fresh issue vs OFS",
  "proceeds":"Use of proceeds","peers":"Competitors & valuation (P/E)","verdict":"Should you subscribe?",
  "retail":"How to apply (retail vs HNI)","recap":"Recap & disclaimer"}

DESC_TAIL = ("\n\n⚠️ DISCLAIMER: This video is for EDUCATION ONLY. It is not investment advice, not a buy/sell "
  "recommendation, and not a prediction of listing gains. Figures are from RHP/DRHP-based public reporting and may "
  "be revised; grey-market premium (GMP) is UNOFFICIAL and changes hourly. Cash-flow line items that public "
  "summaries omit are shown as 'not disclosed' — read the RHP for the full cash-flow statement. Always read the RHP "
  "and check the live subscription before applying. Consult a SEBI-registered advisor.\n\n"
  "Sources: company RHP/DRHP, BusinessToday, Business Standard, Outlook Business, Free Press Journal, Upstox, "
  "IPO Watch, indiaipo, ipocentral, ipoplatform, Groww, Chittorgarh, Moneycontrol (accessed 14 Aug 2026).")

TAGS = ("ipo, ipo 2026, upcoming ipo, ipo analysis, ipo review, mainboard ipo, stock market india, "
  "ipo gmp, grey market premium, fresh issue vs ofs, ipo valuation, ipo financials, balance sheet, cash flow, "
  "should i apply ipo, nse, bse, ipo this week, new ipo, ipo allotment, {name} ipo, {name} share price")

def chapters_ts(cid):
    """Build mm:ss chapter list from the artifact JSON cuts."""
    path = os.path.join(ART, f"{cid}.json")
    if not os.path.exists(path):
        return None
    cuts = json.load(open(path))["cuts"]
    lines = []
    for c in cuts:
        suffix = c["id"].split("_", 1)[1] if "_" in c["id"] else c["id"]
        if suffix not in LABELS:
            continue
        s = int(c["in_seconds"]); mm, ss = divmod(s, 60)
        lines.append(f"{mm}:{ss:02d} {LABELS[suffix]}")
    return "\n".join(lines)

for cid, m in D.items():
    thumb = {"badge":m["badge"],"title":m["title"],"sub":m["sub"],"accent":m["accent"],
             "hook":m["hook"],"hookSmall":m["hookSmall"],"brand":BRAND,"badgeHi":True}
    json.dump(thumb, open(os.path.join(ART, f"{cid}.thumb.json"),"w"), ensure_ascii=False, indent=2)
    name = m["title"].replace("\n"," ").replace(" IPO","")
    ts = chapters_ts(cid) or "(build the chapter first to populate timestamps)"
    desc = (f"{m['one']}\n\nA calm, education-first breakdown: what the company does, its FULL financials — income "
            f"statement, balance sheet AND cash flow — where your money actually goes (fresh issue vs offer-for-sale), "
            f"how it's priced against its competitors (P/E), whether you'd apply as a retail or HNI investor, and how "
            f"much you need.\n\nCHAPTERS\n{ts}\n{DESC_TAIL}")
    with open(os.path.join(DELIV, f"{cid}.youtube.md"),"w") as f:
        f.write(f"# {name} — YouTube metadata\n\n## Title options\n")
        for t in m["titles"]: f.write(f"- {t}\n")
        f.write(f"\n## Description\n\n{desc}\n\n## Tags\n\n{TAGS.replace('{name}', name)}\n")
    print(f"{cid}: thumb + youtube.md written")
print("done")
