#!/usr/bin/env python3
"""YouTube metadata + thumbnails for the 3 English sector deep-dives."""
import json, os, subprocess, sys
OUT = os.path.expanduser("~/Downloads/generated_videos/sector-deep-dives")
COMPOSER = os.path.expanduser("~/Developer/explainer-forge/composer")
THUMBS = os.path.join(OUT, "_thumbnails")
C, M, V, G, R = "#22D3EE", "#FBBF24", "#A78BFA", "#34D399", "#FB7185"
BASE = ["sector analysis india", "how to analyse stocks", "stock market sectors",
        "fundamental analysis", "technical analysis", "stock market course", "investing india"]
DISC = "⚠️ Educational content only — NOT investment advice. Company names are examples, not recommendations. Do your own research / consult a SEBI-registered adviser."
SUB = "👍 Like & subscribe. 🔔"
SER = "📚 Sector Deep-Dives series — Finance, Defence, Technology & more."
def desc(hook, covers, h):
    return f"{hook}\n\n📌 In this video:\n{covers}\n\n{SER}\n\n{DISC}\n{SUB}\n\n{h}"
def th(title, sub, accent, hook, hookSmall):
    return {"badge": "SECTOR DEEP-DIVE", "title": title, "sub": sub, "accent": accent, "hook": hook, "hookSmall": hookSmall, "ep": "ENGLISH", "brand": "SECTOR SERIES · ENGLISH"}

VIDEOS = [
 ("sector-finance.mp4", "src/renders/fin.mp4",
  "How to Analyse Bank & Finance Stocks (Full Guide) | Sector Deep-Dive",
  desc("Analyse the finance sector like a pro — the bank-specific fundamentals, technicals, and strategies.",
       "• Fundamentals: NIM, GNPA/NNPA, CASA, CAR, ROA\n• Why banks are valued on P/B, not P/E\n• Technicals: Bank Nifty, relative strength, breadth\n• Strategies + traps to avoid", "#Banking #FinanceSector #StockMarket #Investing #NIM #BankNifty"),
  BASE + ["bank stock analysis", "how to analyse bank stocks", "nim casa car", "bank nifty analysis", "banking sector"],
  th("Bank Stocks", "NIM · NPA · CASA · CAR · P/B", C, "P/B", "not P/E")),
 ("sector-defence.mp4", "src/renders/def.mp4",
  "How to Analyse Defence Stocks (Order Books & Risks) | Sector Deep-Dive",
  desc("Analyse India's defence sector — order books, indigenisation, technicals, strategies, and the valuation risk.",
       "• Structural theme: budgets, indigenisation, exports\n• Fundamentals: order book, book-to-bill, cash\n• Technicals: Nifty India Defence, momentum risk\n• Strategy: buy dips, not hype (P/E ~57 caution)", "#DefenceStocks #Defence #StockMarket #Investing #MakeInIndia #HAL #BEL"),
  BASE + ["defence stocks india", "how to analyse defence stocks", "order book analysis", "nifty india defence", "hal bel stocks"],
  th("Defence Stocks", "Order book · indigenisation · risk", M, "4.5", "yrs order book")),
 ("sector-technology.mp4", "src/renders/tec.mp4",
  "How to Analyse IT / Tech Stocks (Constant Currency & AI) | Sector Deep-Dive",
  desc("Analyse India's IT sector — constant-currency growth, deal TCV, attrition, the USD link, and the AI winners.",
       "• Drivers: US demand, USD/INR, client cycles, AI\n• Fundamentals: constant-currency growth, TCV, margin, attrition\n• Technicals: Nifty IT (−25% in 2026), USD & US cues\n• Strategy: buy quality in the fall, pick AI winners", "#ITStocks #TechStocks #StockMarket #Investing #NiftyIT #AI"),
  BASE + ["it sector stocks india", "how to analyse it stocks", "nifty it analysis", "constant currency", "it sector 2026"],
  th("IT / Tech\nStocks", "Growth · TCV · USD · AI", V, "AI", "winners")),
 ("sector-pharma.mp4", "src/renders/pha.mp4",
  "How to Analyse Pharma & Healthcare Stocks (USFDA Risk) | Sector Deep-Dive",
  desc("Analyse India's pharma sector — USFDA status, the approvals pipeline, price erosion, technicals and strategies.",
       "• USFDA warning letters — the #1 risk\n• Pipeline, revenue mix, R&D, price erosion\n• Technicals: Nifty Pharma, defensive, news gaps\n• Strategy: clean-record leaders, China+1 CDMO", "#Pharma #HealthcareStocks #StockMarket #Investing #USFDA"),
  BASE + ["pharma stocks india", "how to analyse pharma stocks", "usfda warning letter", "nifty pharma", "healthcare stocks"],
  th("Pharma\nStocks", "USFDA · pipeline · margins", G, "FDA", "the #1 risk")),
 ("sector-auto.mp4", "src/renders/aut.mp4",
  "How to Analyse Auto Stocks (Volumes, EV & the Cycle) | Sector Deep-Dive",
  desc("Analyse the auto sector — monthly sales volumes, segment mix, input costs, the EV shift, technicals and strategies.",
       "• Monthly sales volumes — the #1 signal\n• Segment mix, steel costs, EV transition\n• Technicals: Nifty Auto, cyclical timing\n• Strategy: play the volume cycle, back EV winners", "#AutoStocks #EV #StockMarket #Investing #NiftyAuto"),
  BASE + ["auto stocks india", "how to analyse auto stocks", "ev stocks india", "nifty auto", "automobile sector"],
  th("Auto Stocks", "Volumes · EV · the cycle", V, "EV", "winners")),
 ("sector-fmcg.mp4", "src/renders/fmc.mp4",
  "How to Analyse FMCG Stocks (Volume Growth & Valuation) | Sector Deep-Dive",
  desc("Analyse the FMCG / consumer-staples sector — volume growth, rural demand, margins, the defensive role, and valuation.",
       "• Volume growth (not value), rural vs urban\n• Gross margin, pricing power, distribution moat\n• Technicals: Nifty FMCG, defensive, low beta\n• Strategy: steady compounders; never overpay", "#FMCG #ConsumerStocks #StockMarket #Investing #NiftyFMCG"),
  BASE + ["fmcg stocks india", "how to analyse fmcg stocks", "consumer staples", "nifty fmcg", "defensive stocks"],
  th("FMCG Stocks", "Volume · margins · moat", M, "🛒", "defensive")),
 ("sector-metals.mp4", "src/renders/met.mp4",
  "How to Analyse Metal Stocks (LME, Cost & the Cycle) | Sector Deep-Dive",
  desc("Analyse the metals sector — LME prices, cost per tonne, EBITDA per tonne, net debt, and cyclical timing.",
       "• LME prices & China set the revenue\n• Cost/tonne & EBITDA/tonne — lowest cost wins\n• Net debt is deadly at the cycle bottom\n• Strategy: buy low & hated, sell high & loved", "#MetalStocks #Steel #StockMarket #Investing #NiftyMetal"),
  BASE + ["metal stocks india", "how to analyse metal stocks", "steel stocks", "nifty metal", "commodity cycle"],
  th("Metal Stocks", "LME · cost/tonne · cycle", R, "🔄", "buy the fear")),
 ("sector-energy.mp4", "src/renders/ene.mp4",
  "How to Analyse Energy Stocks (Oil, Gas & Power) | Sector Deep-Dive",
  desc("Analyse the energy sector — upstream vs OMCs vs gas vs power, GRM, crude sensitivity, technicals and strategies.",
       "• 4 sub-sectors: upstream, OMCs, gas, power\n• GRM, marketing margin, crude inverse for OMCs\n• Technicals: overlay crude (correctly!)\n• Strategy: OMCs on soft crude, dividends, power/renewables", "#EnergyStocks #OilAndGas #StockMarket #Investing #OMC"),
  BASE + ["energy stocks india", "how to analyse oil gas stocks", "omc stocks", "gross refining margin", "power stocks"],
  th("Energy Stocks", "Oil · gas · power · GRM", M, "GRM", "the OMC key")),
 ("sector-realty.mp4", "src/renders/rea.mp4",
  "How to Analyse Real Estate & Infra Stocks | Sector Deep-Dive",
  desc("Analyse realty & infrastructure — pre-sales, collections, net debt, the rate cycle, REITs, technicals and strategies.",
       "• Sub-sectors: residential, commercial/REITs, EPC, materials\n• Pre-sales, collections, net debt (not just profit)\n• Technicals: Nifty Realty, rate-cut catalyst\n• Strategy: low-debt leaders, cycle timing, REITs", "#RealEstate #Realty #StockMarket #Investing #REITs"),
  BASE + ["real estate stocks india", "how to analyse realty stocks", "reit india", "nifty realty", "infrastructure stocks"],
  th("Realty &\nInfra", "Pre-sales · debt · the cycle", V, "🏗️", "watch the cash")),
 ("sector-chemicals.mp4", "src/renders/che.mp4",
  "How to Analyse Chemical Stocks (Specialty vs Commodity, China+1) | Sector Deep-Dive",
  desc("Analyse chemicals — specialty vs commodity vs agrochem, margins, the China+1 theme, technicals and strategies.",
       "• Specialty (quality) vs commodity (cyclical)\n• China+1 tailwind vs China-dumping risk\n• Margin stability & R&D reveal the winners\n• Strategy: hold specialty, trade commodity", "#ChemicalStocks #SpecialtyChemicals #StockMarket #Investing #ChinaPlusOne"),
  BASE + ["chemical stocks india", "how to analyse chemical stocks", "specialty chemicals", "china plus one", "nifty chemicals"],
  th("Chemical\nStocks", "Specialty vs commodity", C, "🌏", "China+1")),
 ("sector-telecom-media.mp4", "src/renders/mtl.mp4",
  "How to Analyse Telecom & Media Stocks (ARPU & Disruption) | Sector Deep-Dive",
  desc("Analyse telecom & media — ARPU, subscribers, debt, the digital shift, streaming, technicals and strategies.",
       "• Telecom: ARPU, subscribers, debt, 5G\n• A 3-player market = pricing power\n• Media: subscription vs ads, streaming disruption\n• Strategy: back the disruptor, avoid the debt trap", "#Telecom #Media #StockMarket #Investing #ARPU #OTT"),
  BASE + ["telecom stocks india", "how to analyse telecom stocks", "media stocks", "arpu", "ott streaming stocks"],
  th("Telecom &\nMedia", "ARPU · 5G · streaming", V, "ARPU", "the key")),
]

def emit():
    os.makedirs(OUT, exist_ok=True)
    lines = ["# 📺 YouTube Metadata — Sector Deep-Dives (English)", "", f"{len(VIDEOS)} videos.", ""]
    for f, _, title, d, tags, thumb in VIDEOS:
        tg = ", ".join(dict.fromkeys(tags))
        lines += [f"---\n### 🎬 `{f}`", "", f"**Title:** {title}", "", "**Description:**", "```", d, "```",
                  f"**Tags:** `{tg}`", "", f"**Thumbnail:** `_thumbnails/{f.replace('.mp4','.png')}`", ""]
    open(os.path.join(OUT, "_YOUTUBE_METADATA.md"), "w").write("\n".join(lines))
    print(f"Wrote metadata ({len(VIDEOS)})")

def thumbs():
    os.makedirs(THUMBS, exist_ok=True)
    for f, _, title, d, tags, thumb in VIDEOS:
        pj = os.path.join("/tmp", "sxth_" + f.replace(".mp4", ".json"))
        json.dump(thumb, open(pj, "w"), ensure_ascii=False)
        out = os.path.join(THUMBS, f.replace(".mp4", ".png"))
        subprocess.run(["npx", "remotion", "still", "Thumbnail", out, f"--props={pj}", "--frame=0"], cwd=COMPOSER, capture_output=True)
        print(f"  {'OK ' if os.path.exists(out) else 'ERR'} {os.path.basename(out)}")

if __name__ == "__main__":
    emit()
    if "--meta" not in sys.argv:
        thumbs()
