#!/usr/bin/env python3
"""Generate thumbnail props JSON + YouTube metadata for BATCH 5 (next week's IPOs)."""
import json, os
ROOT = os.path.dirname(os.path.abspath(__file__))
ART = os.path.join(ROOT, "artifacts"); os.makedirs(ART, exist_ok=True)
DELIV = os.path.join(ROOT, "delivery_batch5"); os.makedirs(DELIV, exist_ok=True)

BRAND = "ENGLISH · NEXT WEEK'S IPOs"

# thumb props + youtube meta per chapter
D = {
"dhoot": {
  "accent":"#38BDF8","badge":"IPO ANALYSIS","title":"Dhoot\nTransmission IPO","sub":"EV wiring · ₹3,067 Cr · 10–12 Aug",
  "hook":"44.9×","hookSmall":"vs ~57× peers — cheaper",
  "titles":["Dhoot Transmission IPO Review: Cheaper Than Its Rivals? | Fresh vs OFS, Peers & P/E",
            "Dhoot Transmission IPO (₹3,067 Cr): Full Analysis, Competitors & Valuation",
            "Should You Apply? Dhoot Transmission IPO — Financials, Peer P/E, GMP Explained"],
  "one":"Dhoot Transmission IPO — auto wiring & EV connectors, ₹3,066.89 Cr, opens 10–12 Aug 2026.",
},
"molbio": {
  "accent":"#2DD4BF","badge":"IPO ANALYSIS","title":"Molbio\nDiagnostics IPO","sub":"Truenat testing · ₹940 Cr · 10–12 Aug",
  "hook":"NO\nPEER","hookSmall":"so how do you value it?",
  "titles":["Molbio Diagnostics IPO Review: A Company With NO Listed Peer | Full Analysis",
            "Molbio Diagnostics IPO (₹940 Cr): Truenat, Financials, Valuation & GMP",
            "Should You Apply? Molbio Diagnostics IPO — Fresh vs OFS, Competitors Explained"],
  "one":"Molbio Diagnostics IPO — point-of-care molecular testing (Truenat), ₹939.70 Cr, opens 10–12 Aug 2026.",
},
"milkymist": {
  "accent":"#FBBF24","badge":"IPO ANALYSIS","title":"Milky Mist\nIPO","sub":"Value-added dairy · ₹1,553 Cr · 11–13 Aug",
  "hook":"~85×","hookSmall":"above EVERY dairy peer",
  "titles":["Milky Mist IPO Review: Priced Above EVERY Dairy Peer? | Full Analysis & P/E",
            "Milky Mist IPO (₹1,553 Cr): Financials, Competitors (Hatsun/Dodla), Valuation, GMP",
            "Should You Apply? Milky Mist Dairy IPO — Fresh vs OFS, Peer P/E Explained"],
  "one":"Milky Mist IPO — value-added dairy (paneer/cheese), ₹1,553 Cr, opens 11–13 Aug 2026.",
},
"shiprocket": {
  "accent":"#A78BFA","badge":"IPO ANALYSIS","title":"Shiprocket\nIPO","sub":"E-com logistics · ₹1,617 Cr · 12–14 Aug",
  "hook":"−₹79\nCr","hookSmall":"loss-making — worth it?",
  "titles":["Shiprocket IPO Review: Still Loss-Making — Worth ₹1,617 Cr? | Full Analysis",
            "Shiprocket IPO (₹1,617 Cr): Financials, Delhivery Comparison, Valuation, GMP",
            "Should You Apply? Shiprocket IPO — Fresh vs OFS, Competitors & Price-to-Sales"],
  "one":"Shiprocket IPO — asset-light e-commerce logistics platform, ₹1,617.5 Cr, opens 12–14 Aug 2026.",
},
"beharilal": {
  "accent":"#F97316","badge":"IPO ANALYSIS","title":"Behari Lal\nEngineering IPO","sub":"Metal rolls · ₹302 Cr · 12–14 Aug",
  "hook":"~17×","hookSmall":"cheap — but no peer",
  "titles":["Behari Lal Engineering IPO Review: Cheap At ~17×? | Full Analysis & Valuation",
            "Behari Lal Engineering IPO (₹302 Cr): Financials, Fresh vs OFS, GMP Explained",
            "Should You Apply? Behari Lal Engineering IPO — Metal Rolls, No Listed Peer"],
  "one":"Behari Lal Engineering IPO — metal rolls maker, ₹301.62 Cr, opens 12–14 Aug 2026.",
},
"fascinate": {
  "accent":"#EC4899","badge":"SME IPO","title":"Fascinate\nTextiles IPO","sub":"Garment OEM · ₹67 Cr · NSE SME · 11–13 Aug",
  "hook":"2×","hookSmall":"revenue doubled · SME",
  "titles":["Fascinate Textiles SME IPO Review: Revenue Doubled | Full Analysis & Risks",
            "Fascinate Textiles IPO (₹67 Cr, NSE SME): Financials, Competitors, GMP",
            "Should You Apply? Fascinate Textiles SME IPO — Fresh vs OFS, Big Minimum Bid"],
  "one":"Fascinate Textiles SME IPO — B2B garment OEM, ~₹67 Cr, NSE SME, opens 11–13 Aug 2026.",
},
"shamfoam": {
  "accent":"#22D3EE","badge":"SME IPO","title":"Sham Foam\nIPO","sub":"Foam & furniture · ₹40 Cr · NSE SME · 11–13 Aug",
  "hook":"100%\nFRESH","hookSmall":"₹40 Cr SME · thin margins",
  "titles":["Sham Foam SME IPO Review: 100% Fresh — But Thin Margins | Full Analysis",
            "Sham Foam IPO (₹40 Cr, NSE SME): Financials, Sheela Foam Comparison, GMP",
            "Should You Apply? Sham Foam SME IPO — Fixed ₹130, Foam & Furniture Explained"],
  "one":"Sham Foam SME IPO — foam & furniture maker, ₹40 Cr, NSE SME, fixed ₹130, opens 11–13 Aug 2026.",
},
"pramodini": {
  "accent":"#34D399","badge":"SME IPO","title":"Pramodini\nMedicare IPO","sub":"Diagnostics · ₹69 Cr · SME · 12–14 Aug",
  "hook":"26%","hookSmall":"net margin · profit +74%",
  "titles":["Pramodini Medicare SME IPO Review: Unusually Profitable | Full Analysis",
            "Pramodini Medicare IPO (₹69 Cr, SME): Financials, Diagnostics Peers, GMP",
            "Should You Apply? Pramodini Medicare SME IPO — 26% Margin, Fresh vs OFS"],
  "one":"Pramodini Medicare SME IPO — radiology/pathology diagnostics, ₹69.04 Cr, SME, opens 12–14 Aug 2026.",
},
}

DESC_TAIL = ("\n\n⚠️ DISCLAIMER: This video is for EDUCATION ONLY. It is not investment advice, not a buy/sell "
  "recommendation, and not a prediction of listing gains. Figures are from RHP-based public reporting and may be "
  "revised; grey-market premium (GMP) is UNOFFICIAL and changes hourly. Always read the RHP and check the live "
  "subscription before applying. Consult a SEBI-registered advisor.\n\n"
  "Sources: company RHP/DRHP, BusinessToday, Business Standard, Outlook Money, IPO Watch, InvestorGain, IPOJi, "
  "Groww, Chittorgarh, Moneycontrol (accessed 8 Aug 2026).")

CHAPTERS_TS = ("0:00 Intro\n0:30 What the company does\n1:15 FY financials\n2:00 Fresh issue vs OFS\n"
  "2:45 Use of proceeds\n3:25 Competitors & valuation (P/E)\n4:10 Should you subscribe?\n"
  "4:55 How to apply (retail vs HNI / SME)\n5:35 Recap & disclaimer")

TAGS = ("ipo, ipo 2026, upcoming ipo, ipo analysis, ipo review, mainboard ipo, sme ipo, stock market india, "
  "ipo gmp, grey market premium, fresh issue vs ofs, ipo valuation, should i apply ipo, nse, bse, "
  "ipo this week, new ipo, ipo allotment, {name} ipo, {name} share price")

for cid, m in D.items():
    thumb = {"badge":m["badge"],"title":m["title"],"sub":m["sub"],"accent":m["accent"],
             "hook":m["hook"],"hookSmall":m["hookSmall"],"brand":BRAND,"badgeHi":True}
    json.dump(thumb, open(os.path.join(ART, f"{cid}.thumb.json"),"w"), ensure_ascii=False, indent=2)
    name = m["title"].replace("\n"," ").replace(" IPO","")
    desc = (f"{m['one']}\n\nA calm, education-first breakdown: what the company does, its financials, where your money "
            f"actually goes (fresh issue vs offer-for-sale), how it's priced against its competitors (P/E), whether "
            f"you'd apply as a retail or HNI investor, and how much you need.\n\nCHAPTERS\n{CHAPTERS_TS}\n{DESC_TAIL}")
    with open(os.path.join(DELIV, f"{cid}.youtube.md"),"w") as f:
        f.write(f"# {name} — YouTube metadata\n\n## Title options\n")
        for t in m["titles"]: f.write(f"- {t}\n")
        f.write(f"\n## Description\n\n{desc}\n\n## Tags\n\n{TAGS.replace('{name}', name)}\n")
    print(f"{cid}: thumb + youtube.md written")
print("done")
