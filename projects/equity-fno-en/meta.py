#!/usr/bin/env python3
"""YouTube metadata + thumbnails for the English Equities/F&O/Commodities course.
Renders thumbnails via the Thumbnail composition and writes _YOUTUBE_METADATA.md.
Run:  python3 meta.py            (metadata + thumbnails)
      python3 meta.py --meta     (metadata only)
"""
import json, os, subprocess, sys
OUT = os.path.expanduser("~/Downloads/generated_videos/equity-fno-english")
COMPOSER = os.path.expanduser("~/Developer/explainer-forge/composer")
THUMBS = os.path.join(OUT, "_thumbnails")
G, C, R, M, V = "#34D399", "#22D3EE", "#FB7185", "#FBBF24", "#A78BFA"
BASE_TAGS = ["stock market course", "equities futures options", "options trading explained",
             "futures and options", "how to invest in stock market", "commodities trading",
             "options strategies", "stock market for beginners", "MCX gold trading", "F&O trading"]
DISC = "⚠️ Educational content only — NOT investment advice. Do your own research and consult a SEBI-registered adviser."
SUB = "👍 Like & subscribe for the full course. 🔔"
SER = "📚 Full course: Equities, Futures, Options & Commodities — see the playlist for all chapters."
H = "#StockMarket #Options #Futures #Investing #FnO #Commodities #Trading"

def desc(hook, covers, extra_h):
    return f"{hook}\n\n📌 In this chapter:\n{covers}\n\n{SER}\n\n{DISC}\n{SUB}\n\n{extra_h} {H}"

def th(title, sub, accent, hook, hookSmall, ep):
    return {"badge": "EQUITIES · F&O", "title": title, "sub": sub, "accent": accent, "hook": hook, "hookSmall": hookSmall, "ep": ep, "brand": "ENGLISH · FULL COURSE"}

VIDEOS = [
 ("eq01.mp4", "Stock Market Course: The Basics (Equities, F&O, Commodities) | Chapter 1",
  desc("What are equities, futures, options, and commodities — and how the Indian market actually works.",
       "• The four arenas: equities, futures, options, commodities\n• NSE, BSE, SEBI, demat & T+1\n• How the course is structured", "#StockMarketBasics"),
  BASE_TAGS + ["what are equities", "nse bse sebi", "stock market basics"],
  th("The Basics", "Equities · F&O · Commodities", G, "01", "Foundations", "PART 01")),
 ("eq02.mp4", "How to Select a Sector (Top-Down Method) | Stock Market Course Ch 2",
  desc("How professionals pick a sector before a stock — the top-down method, sector drivers, and rotation.",
       "• Why sector comes first\n• The main sectors & their drivers\n• Cyclical vs defensive · rotation\n• Top-down 4-step method", "#SectorAnalysis"),
  BASE_TAGS + ["how to select sector", "sector rotation", "top down investing"],
  th("Choosing a\nSector", "Top-down · drivers · rotation", C, "🔭", "Macro→Stock", "PART 02")),
 ("eq03.mp4", "How to Research a Stock — Fundamental Analysis | Stock Market Course Ch 3",
  desc("Read a company like a pro: the 3 financial statements, key ratios, the moat, and fair valuation.",
       "• P&L, balance sheet, cash flow\n• ROE, debt, P/E, promoter holding\n• Moat, management, runway\n• Valuation & margin of safety", "#FundamentalAnalysis"),
  BASE_TAGS + ["fundamental analysis", "how to research a stock", "how to read balance sheet"],
  th("Researching\na Stock", "3 statements · ratios · moat", C, "ROE", "Fundamentals", "PART 03")),
 ("eq04.mp4", "Technical Analysis, Tools & Best Research Channels | Stock Market Course Ch 4",
  desc("Charts, free research tools, and the trustworthy channels to learn from — plus how to spot a tip-seller.",
       "• Trend, support/resistance, volume, MA\n• Screener, Tickertape, Trendlyne\n• Zerodha Varsity, Rachana Ranade, fund managers\n• Method vs tip-seller", "#TechnicalAnalysis"),
  BASE_TAGS + ["best stock market youtube channels", "screener trendlyne", "technical analysis"],
  th("Charts, Tools\n& Sources", "Technicals · screeners · channels", M, "🔎", "Where to learn", "PART 04")),
 ("eq05.mp4", "Every Equity Investing Strategy Explained | Stock Market Course Ch 5",
  desc("Value, growth, quality, momentum, dividend, SIP, core-satellite, contrarian, rotation — and which fits you.",
       "• Buy & hold, SIP, core-satellite, index\n• Value · growth · quality (GARP)\n• Momentum, dividend, contrarian, rotation\n• Which strategy for whom", "#InvestingStrategy"),
  BASE_TAGS + ["value investing", "growth investing", "momentum investing", "investing strategies"],
  th("Equity\nStrategies", "Value · growth · momentum · SIP", G, "8+", "Strategies", "PART 05")),
 ("eq06.mp4", "Futures Trading Explained + Strategies | Stock Market Course Ch 6",
  desc("What a future is, lots, margin, mark-to-market, expiry, the real leverage maths, and futures strategies.",
       "• What is a future (a derivative)\n• Lot, margin, MTM, expiry\n• 10x leverage — the real maths\n• Hedging, spreads, arbitrage", "#FuturesTrading"),
  BASE_TAGS + ["what is futures trading", "futures explained", "leverage trading", "hedging"],
  th("Futures", "Lot · margin · leverage", V, "10x", "Leverage", "PART 06")),
 ("eq07.mp4", "Options Trading for Beginners — Calls, Puts & Payoffs | Stock Market Course Ch 7",
  desc("Options explained from zero: calls, puts, strike, premium, intrinsic vs time value, and payoff diagrams.",
       "• Option = insurance analogy\n• Call & put, strike, premium\n• Intrinsic + time value, ITM/ATM/OTM\n• The payoff diagram", "#OptionsTrading"),
  BASE_TAGS + ["options for beginners", "call and put options", "options basics", "what is an option"],
  th("Options\nBasics", "Calls · puts · payoff", V, "🎯", "Call / Put", "PART 07")),
 ("eq08.mp4", "Option Greeks & Strategies (+ the Hard Truth) | Stock Market Course Ch 8",
  desc("Delta, gamma, theta, vega; covered calls, spreads, straddles, iron condors; and why 91% of F&O traders lose.",
       "• The Greeks: delta, gamma, theta, vega\n• Time decay favours the seller\n• Covered call, protective put, spreads, condor\n• SEBI: 91% of F&O traders lose", "#OptionGreeks"),
  BASE_TAGS + ["option greeks", "options strategies", "iron condor", "covered call", "f&o loss sebi"],
  th("Options\nMastery", "Greeks · strategies · the truth", V, "91%", "F&O lose", "PART 08")),
 ("eq09.mp4", "Commodities Trading — Gold, Silver & Crude on MCX | Stock Market Course Ch 9",
  desc("How commodities trade on the MCX, their global drivers, and why gold belongs in your portfolio as a hedge.",
       "• Bullion, energy, base metals\n• MCX futures & leverage\n• Global drivers: USD, OPEC, geopolitics\n• Gold ETF/SGB as a 5–10% hedge", "#Commodities"),
  BASE_TAGS + ["mcx commodity trading", "gold trading india", "commodities for beginners", "gold etf"],
  th("Commodities", "Gold · silver · crude · MCX", M, "🥇", "MCX", "PART 09")),
 ("eq10.mp4", "Risk Management & Which Strategy Is For You | Stock Market Course Ch 10",
  desc("The survival rules that keep you in the game, and how to match the instrument to your goals — the master recap.",
       "• Position sizing, stop-loss, diversify\n• Never mix trading & investing capital\n• Which tool for beginner / experienced / pro\n• The whole course in one breath", "#RiskManagement"),
  BASE_TAGS + ["risk management trading", "position sizing", "stop loss", "how much to invest"],
  th("Risk & The\nWhole Picture", "Survival · fit · recap", G, "1-2%", "Risk/trade", "PART 10")),
 ("equity-fno-english-FULL.mp4", "Equities, Futures, Options & Commodities — FULL COURSE (English)",
  desc("The complete masterclass in one video: sectors, research, every strategy, futures, options, commodities, risk.",
       "• All 10 chapters back to back\n• Equities → F&O → commodities\n• Every major strategy + risk management", "#StockMarketCourse"),
  BASE_TAGS + ["stock market full course", "options full course", "complete trading course"],
  th("A to Z\nMasterclass", "Equities · F&O · Commodities", G, "10", "Chapters", "FULL")),
]

def emit():
    os.makedirs(OUT, exist_ok=True)
    lines = ["# 📺 YouTube Metadata — Equities, F&O & Commodities (English course)", "",
             f"{len(VIDEOS)} videos. Copy-paste per video. Keep the disclaimer (finance).", ""]
    for f, title, d, tags, thumb in VIDEOS:
        tg = ", ".join(dict.fromkeys(tags))
        lines += [f"---\n### 🎬 `{f}`", "", f"**Title:** {title}", "", "**Description:**", "```", d, "```",
                  f"**Tags:** `{tg}`", "", f"**Thumbnail:** `_thumbnails/{f.replace('.mp4','.png')}`", ""]
    open(os.path.join(OUT, "_YOUTUBE_METADATA.md"), "w").write("\n".join(lines))
    print(f"Wrote _YOUTUBE_METADATA.md ({len(VIDEOS)} videos)")

def thumbs():
    os.makedirs(THUMBS, exist_ok=True)
    for f, title, d, tags, thumb in VIDEOS:
        pj = os.path.join("/tmp", "eqth_" + f.replace(".mp4", ".json"))
        json.dump(thumb, open(pj, "w"), ensure_ascii=False)
        out = os.path.join(THUMBS, f.replace(".mp4", ".png"))
        subprocess.run(["npx", "remotion", "still", "Thumbnail", out, f"--props={pj}", "--frame=0"], cwd=COMPOSER, capture_output=True)
        print(f"  {'OK ' if os.path.exists(out) else 'ERR'} {os.path.basename(out)}")

if __name__ == "__main__":
    emit()
    if "--meta" not in sys.argv:
        thumbs()
