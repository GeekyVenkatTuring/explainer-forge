#!/usr/bin/env python3
"""Vertical Shorts / Reels generator (9:16) — ~60s mini-lessons, LLM/Math-for-ML style.
Per chapter: CH badge + glowing title + subtitle + keyword + 5 highlights (revealed across
the minute) + a full ~60s spoken script (Telugu for stock-market, English otherwise).
NO captions. Renders the `Short` Remotion composition. Emits youtube.md + instagram.md +
a master shorts.csv per folder.
Usage: python3 gen.py [eqfno|sectors|smteic]   (default: all).  Add 'force' to re-TTS.
"""
import json, os, re, subprocess, sys, csv

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
COMPOSER = os.path.join(REPO, "composer")
PUBLIC = os.path.join(COMPOSER, "public", "short")
RAW = os.path.join(os.path.dirname(__file__), "assets", "raw")
GV = os.path.expanduser("~/Downloads/generated_videos")
for d in (PUBLIC, RAW): os.makedirs(d, exist_ok=True)
G, C, R, M, V = "#34D399", "#22D3EE", "#FB7185", "#FBBF24", "#A78BFA"
VOICE = {"te": "te-IN-ShrutiNeural", "en": "en-IN-NeerjaNeural"}
RATE = "-4%"; PAUSE = 0.4
FORCE = "force" in sys.argv

FOLDERS = {
 "eqfno":  ("equity-fno-english/shorts", "EQUITIES · F&O", ["stock market", "options trading", "futures", "investing", "shorts"]),
 "sectors":("sector-deep-dives/shorts",  "SECTOR SERIES",  ["sector analysis", "stock market", "how to analyse stocks", "investing", "shorts"]),
 "smteic": ("stock-market-telugu/shorts","తెలుగులో · STOCK MARKET", ["stock market telugu", "share market telugu", "investing telugu", "తెలుగు", "shorts"]),
}

def S(folder, sid, lang, accent, badge, title, sub, keyword, highlights, script, ytdesc, tags):
    return dict(folder=folder, sid=sid, lang=lang, accent=accent, badge=badge, title=title,
                sub=sub, keyword=keyword, highlights=highlights, script=script, ytdesc=ytdesc, tags=tags)

SHORTS = [
 # ================= EQUITIES / F&O (English) — ~60s each =================
 S("eqfno","eq01","en",G,"CH 01","The Basics","Equities, F&O, commodities","4 arenas",
   ["Equities = ownership in a business","Futures = a contract, leveraged","Options = a right, like insurance","Commodities trade on the MCX","NSE, BSE, SEBI, demat, T+1"],
   "There are four ways to play the market, and mixing them up is the first mistake beginners make. [pause] "
   "One: equities. When you buy a share, you own a real slice of a business, and you grow as it grows. This is where wealth is built. [pause] "
   "Two: futures. A contract to buy or sell later at a price fixed today. It's leveraged, and it expires. [pause] "
   "Three: options. The right, but not the obligation, to buy or sell at a set price — for a small premium, exactly like insurance. [pause] "
   "Four: commodities — gold, silver, crude — traded on the M-C-X. [pause] "
   "Behind it all: the NSE and BSE exchanges, SEBI the regulator, your shares in a demat account, settling T plus one. Master this map, and everything else clicks into place.",
   "The four arenas of the market — equities, futures, options and commodities — plus how the Indian market works.",
   ["stock market basics","equities","derivatives","how markets work"]),
 S("eqfno","eq02","en",C,"CH 02","Choosing a Sector","The top-down method","macro → stock",
   ["Ride the sector's tailwind","Read macro → pick sector → pick leaders","Each sector has one main driver","Cyclicals lead booms; defensives lead slowdowns","Leadership rotates through the cycle"],
   "Before you pick a stock, pick the right neighbourhood — because a rising sector lifts almost every stock in it, and a falling one drags them all down. [pause] "
   "The professional method is top-down. First, read the macro — interest rates, crude oil, the rupee, the economy. [pause] "
   "Then pick the sector that macro favours. If rates are falling, banks and real estate benefit. If crude spikes, oil producers gain and oil consumers hurt. [pause] "
   "Then, inside that sector, buy the strongest one or two leaders — not the weakest name hoping to catch up. [pause] "
   "Remember the deep split: cyclicals like autos and metals lead in booms, while defensives like FMCG and pharma hold up in slowdowns. [pause] "
   "Leadership keeps rotating through the cycle — and riding that rotation is what the top-down method is really for.",
   "How professionals pick a sector before a stock — the top-down method, drivers, and rotation.",
   ["sector selection","top down investing","sector rotation"]),
 S("eqfno","eq03","en",C,"CH 03","Researching a Stock","Fundamental analysis","read the business",
   ["3 statements: P&L, balance sheet, cash flow","Cash is fact; paper profit is opinion","ROE, debt, P/E, promoter holding","Find the moat + honest management","Great company ≠ great stock — price matters"],
   "A share isn't a lottery ticket — it's a piece of a business, so you must read that business. [pause] "
   "Start with the three statements: the profit and loss shows earnings, the balance sheet shows assets versus debt, and the cash flow shows real money — because cash is a fact while paper profit is only an opinion. [pause] "
   "Then four ratios: return on equity above fifteen percent, low debt, price-to-earnings against the sector, and high, unpledged promoter holding. [pause] "
   "Then the qualitative edge — the moat that rivals can't cross, and honest, capable management. [pause] "
   "And the hardest lesson of all: a great company is not a great stock if you overpay. Demand a fair price, with a margin of safety. [pause] "
   "Great business, fair price, patience — that's the whole game.",
   "Fundamental analysis — the three statements, key ratios, the moat, and fair valuation.",
   ["fundamental analysis","how to research a stock","balance sheet"]),
 S("eqfno","eq04","en",M,"CH 04","Charts & Sources","Technicals + where to learn","learn, don't tip",
   ["Trend, support/resistance, volume, MA","Free tools: Screener, Trendlyne, Tickertape","Read annual reports & concalls","Learn from Varsity, credible educators","Trust methods, not stock tips"],
   "Fundamentals tell you what to buy; technicals help with when. [pause] "
   "The basics of a chart: the trend — don't fight it; support and resistance, the floor and ceiling; volume, the conviction behind a move; and moving averages that reveal the true direction. [pause] "
   "Where do you do the research? The best tools are free — Screener, Trendlyne, and Tickertape — but the gold is primary: a company's own annual report and its earnings calls. [pause] "
   "To learn the craft, follow structured, credible sources like Zerodha Varsity and educators who teach concepts, not calls. [pause] "
   "And the single most important filter: trust the people who explain their reasoning so you can decide for yourself, and avoid anyone selling specific buy-this-now tips or guaranteed returns. [pause] "
   "A tip makes you dependent; a method makes you independent.",
   "Technical analysis basics, the best free tools, trusted channels, and how to spot a tip-seller.",
   ["technical analysis","best stock market channels","screener"]),
 S("eqfno","eq05","en",G,"CH 05","Equity Strategies","Every major approach","find your fit",
   ["Buy & hold + SIP: the foundation","Value: buy below intrinsic worth","Growth & GARP: pay fairly for growth","Momentum, dividend, contrarian, rotation","Discipline beats the choice of strategy"],
   "There's no single best strategy — only the one that fits you. Let's speed through them. [pause] "
   "The foundation is buy-and-hold and the SIP: own quality, invest monthly, let compounding work. This alone beats most clever trading. [pause] "
   "Then the picking styles: value — buying a rupee of worth for fifty paise; growth — buying fast-growing earnings; and quality, or growth at a reasonable price, blending the two. [pause] "
   "Then the active approaches: momentum, buying strength; dividend, for income; contrarian, buying fear; and sector rotation. [pause] "
   "For most people, an index SIP plus a few quality names wins, with far less stress. [pause] "
   "But whichever you choose, the discipline to stick with it matters far more than the strategy itself.",
   "Every major equity strategy — value, growth, quality, momentum, dividend, SIP, core-satellite, and more.",
   ["value investing","growth investing","investing strategies"]),
 S("eqfno","eq06","en",V,"CH 06","Futures","Leverage, decoded","double-edged",
   ["A contract to buy/sell later at a set price","Traded in lots, ~10–15% margin","That margin gives ~10x leverage","+5% move = +50% on margin; −5% = half gone","Real purpose is hedging, not gambling"],
   "A future is simply a contract to buy or sell something later, at a price fixed today — think of a farmer locking in his crop price. [pause] "
   "You trade it in fixed lots, and you pay only about ten to fifteen percent as margin. That's the catch and the thrill: it gives you roughly ten-times leverage. [pause] "
   "Here's the maths. On a fifteen-lakh position with one-and-a-half-lakh margin, a five percent rise earns you fifty percent on your money. [pause] "
   "But a five percent fall wipes out half your margin — on a mere five percent move. Leverage multiplies gains and losses by the exact same factor. [pause] "
   "And because profit and loss settle daily, those losses are very real, very fast. [pause] "
   "The honest purpose of futures is hedging — protecting a portfolio. Speculation is where most retail traders lose.",
   "What a future is, lots, margin, mark-to-market, the real 10x leverage maths, and strategies.",
   ["futures trading","leverage","what is futures"]),
 S("eqfno","eq07","en",V,"CH 07","Options Basics","Calls, puts & payoffs","like insurance",
   ["An option = a RIGHT, like insurance","Call = right to buy (bullish)","Put = right to sell (bearish)","Premium = intrinsic value + time value","Buyer's loss is capped at the premium"],
   "The easiest way to get options is your car insurance. You pay a small premium; if something happens, you're covered; if not, you only lose the premium. [pause] "
   "An option works the same way. You pay a premium for a right — and there are just two kinds. [pause] "
   "A call is the right to buy at a fixed strike price — you buy it when you expect the price to rise. [pause] "
   "A put is the right to sell at a strike — you buy it when you expect a fall, or to insure shares you own. [pause] "
   "The premium has two parts: intrinsic value, its real worth right now, and time value, the hope it moves your way before expiry. [pause] "
   "The buyer's beauty is a capped, known loss — just the premium — with a large upside. But time decay is the enemy, and that's the next lesson.",
   "Options from scratch — calls, puts, strike, premium, intrinsic vs time value, and payoff diagrams.",
   ["options for beginners","call and put","options basics"]),
 S("eqfno","eq08","en",V,"CH 08","Options Mastery","Greeks & the hard truth","91% lose",
   ["Delta, gamma, theta, vega — the Greeks","Theta = time decay, the buyer's enemy","Covered call, protective put, spreads","Straddle, strangle, iron condor","SEBI: 91% of F&O traders lose money"],
   "Professionals don't guess — they measure risk with the Greeks. [pause] "
   "Delta is direction, gamma is its acceleration, vega is sensitivity to volatility, and theta is time decay — how much value the option bleeds every single day. For the buyer, theta is the enemy; time is on the seller's side. [pause] "
   "The real strategies pair options with stock: the covered call for income, the protective put for insurance. [pause] "
   "Then the combinations: spreads with defined risk, straddles and strangles for a big move either way, and iron condors for a market that stays flat. [pause] "
   "But before any of it, the number every course should show you: SEBI found that ninety-one percent of individual F-and-O traders lose money. [pause] "
   "Options are a professional tool — for the educated, well-capitalised and disciplined. Master investing first.",
   "The Greeks, covered calls, spreads, straddles, iron condors, and the SEBI 91% loss truth.",
   ["option greeks","options strategies","f&o loss sebi"]),
 S("eqfno","eq09","en",M,"CH 09","Commodities","Gold, silver, crude on MCX","the hedge",
   ["Bullion, energy, base metals on MCX","Traded via leveraged futures","Driven by USD, OPEC, geopolitics","Gold ETF / SGB = own gold, no leverage","Keep ~5–10% gold as a portfolio hedge"],
   "Beyond stocks lies a parallel market of real, physical things — gold, silver, crude oil, metals — traded in India on the M-C-X. [pause] "
   "They're grouped into bullion, energy, and base metals, and almost always traded through leveraged futures, so a small move is magnified. [pause] "
   "What moves them is global — the dollar, real interest rates, OPEC, and geopolitical fear. You're really trading world events. [pause] "
   "But here's the key idea for a normal investor: you don't need the leverage. A gold ETF or a Sovereign Gold Bond lets you own gold calmly, in your demat, no futures required. [pause] "
   "Why own gold at all? Because it often rises when stocks fall, so a slice of it cushions your portfolio in a crash. [pause] "
   "Keep around five to ten percent as ballast — insurance, not a bet.",
   "How commodities trade on the MCX, their global drivers, and gold as a portfolio hedge.",
   ["commodity trading","mcx gold","gold etf"]),
 S("eqfno","eq10","en",G,"CH 10","Risk & The Whole Picture","Survival first","stay in the game",
   ["Risk only 1–2% of capital per trade","Always use a stop-loss on active trades","Diversify across sectors AND assets","Never mix trading & investing capital","Match the instrument to your goal & skill"],
   "Everything we've learned means nothing without this: the first job isn't to make money — it's to not go broke. Survival first. [pause] "
   "Rule one: risk only one to two percent of your capital on any single trade. Then even ten losses in a row can't ruin you. [pause] "
   "Rule two: always use a stop-loss on leveraged or active positions — decide where you're wrong before you enter. [pause] "
   "Rule three: diversify across sectors and asset classes, so when one zigs, another zags. [pause] "
   "Rule four: never mix your long-term investing pot with your trading money, and never borrow to chase returns. [pause] "
   "And match the tool to yourself: for most people, an index SIP and a few quality stocks quietly build more wealth than any amount of clever trading. Learn deeply, risk little, compound patiently.",
   "The risk-management rules that keep you in the game, and which instrument fits whom.",
   ["risk management","position sizing","stop loss"]),

 # ================= SECTOR DEEP-DIVES (English) — ~60s each =================
 S("sectors","fin","en",C,"SECTOR","Bank Stocks","How to analyse finance","NIM · CASA · CAR",
   ["NIM: the lending spread (~3–4%)","GNPA/NNPA: asset quality is king","CASA: cheap deposits = fatter margins","CAR: the safety buffer (RBI min ~11.5%)","Value on Price-to-Book, NOT P/E"],
   "You cannot analyse a bank like a normal company, because a bank's product is money itself. It needs its own metrics. [pause] "
   "First, N-I-M — the net interest margin, the spread between what a bank earns on loans and pays on deposits. Around three to four percent is healthy, and rising is great. [pause] "
   "Second, asset quality — the bad-loan ratios. This is where banks quietly die, so keep them low. [pause] "
   "Third, the CASA ratio — the share of cheap current and savings deposits. Higher means cheaper funding and fatter margins. [pause] "
   "Fourth, capital adequacy, the safety buffer against losses. [pause] "
   "And crucially, you value a bank on price-to-book, never price-to-earnings — a low multiple often hides bad loans. In banking, a clean book always beats a cheap price.",
   "How to analyse bank & finance stocks — NIM, NPA, CASA, CAR, P/B valuation, technicals and strategies.",
   ["bank stock analysis","nim casa car","banking sector","bank nifty"]),
 S("sectors","def","en",M,"SECTOR","Defence Stocks","Order books & risk","P/E ~57",
   ["Record budgets + indigenisation + exports","Order book = the #1 metric","Book-to-bill = years of visibility","Watch cash flow (long cycles lock cash)","Danger: overpaying after a huge run"],
   "Defence is one of the most exciting and most hyped themes in the market — a long-cycle, order-driven business powered by government spending. [pause] "
   "The tailwind is real: record budgets, an indigenisation push reserving items for Indian makers, and rising exports. [pause] "
   "The number-one metric is the order book — the value of confirmed, unexecuted orders. Divide it by yearly revenue and you get the book-to-bill: how many years of revenue are locked in. Bharat Electronics carries roughly four and a half years. [pause] "
   "But watch cash flow, because long project cycles lock up cash, and paper profit can mislead. [pause] "
   "And here's the real danger: the index has traded near fifty-seven times earnings. Even a wonderful theme is a poor investment if you overpay. [pause] "
   "Love the theme, but buy the dips — never the war-news spike.",
   "How to analyse defence stocks — order books, indigenisation, technicals, and the valuation risk.",
   ["defence stocks india","order book","hal bel","nifty india defence"]),
 S("sectors","tec","en",V,"SECTOR","IT / Tech Stocks","Constant currency & AI","selection matters",
   ["Export-driven: US demand + USD/INR","Constant-currency growth = true growth","Deal TCV = tomorrow's revenue","EBIT margin & attrition matter","AI creates winners AND losers"],
   "Indian I-T is a great export story — these firms earn mostly abroad, in dollars, serving the world's biggest companies. [pause] "
   "So they dance to a different beat: US demand, the dollar-rupee rate, and US client budgets. A weak rupee helps; a US slowdown hurts. [pause] "
   "The key metrics: constant-currency revenue growth, which strips out the currency to show true demand; deal T-C-V, the value of new contracts — tomorrow's revenue today; consistent EBIT margins; and low attrition, since it's a people business. [pause] "
   "And the defining question of the decade — artificial intelligence. Is it a threat that automates the work, or a wave of new deals? It's both. [pause] "
   "After a sharp correction, valuations look tempting, but selection now matters more than simply owning I-T. Pick the AI winners.",
   "How to analyse IT stocks — constant-currency growth, deal TCV, attrition, the USD link, and AI winners.",
   ["it sector stocks","how to analyse it stocks","nifty it","ai stocks"]),
 S("sectors","pha","en",G,"SECTOR","Pharma Stocks","USFDA is everything","the #1 risk",
   ["India: largest generics maker; 1/3 to US","USFDA status is the #1 risk","Warning letters can crush a stock","Watch pipeline & US price erosion","China+1 CDMO is a structural winner"],
   "India is the world's largest maker of generic drugs, and about a third of its pharma exports go to America. That one fact shapes everything. [pause] "
   "Because so much revenue comes from the US, the biggest risk is the American regulator, the FDA. A single warning letter can halt approvals and crush a stock overnight. That's the number-one thing to track. [pause] "
   "Beyond it, watch the approvals pipeline, which is future US revenue; the revenue mix between risky-but-high-margin US and steady domestic; and constant US price erosion eating margins. [pause] "
   "The bright structural theme is contract manufacturing and ingredients — the China-plus-one shift as the world diversifies drug supply toward India. [pause] "
   "Pharma is defensive as a sector, but a single-plant FDA problem makes an individual stock anything but safe. Favour clean compliance records.",
   "How to analyse pharma & healthcare stocks — USFDA risk, pipeline, price erosion, and strategies.",
   ["pharma stocks india","usfda","nifty pharma","healthcare stocks"]),
 S("sectors","aut","en",V,"SECTOR","Auto Stocks","Volumes, EV & the cycle","peak trap",
   ["Monthly sales volumes = the #1 signal","Segment mix: 2W, PV, CV, tractors","Steel & aluminium costs squeeze margins","EV shift creates winners & losers","Cyclicals look cheapest at the PEAK"],
   "Autos are one of the great cyclicals, and right now, one of the most disrupted. [pause] "
   "The heartbeat of the sector is monthly sales volumes — reported every month, they're the clearest demand signal in any sector. When volumes turn, the stocks turn. [pause] "
   "Know the segment mix too: two-wheelers are rural-sensitive, commercial vehicles track the economy, tractors track the monsoon. [pause] "
   "Watch input costs — steel and aluminium — which link autos straight to the metals cycle. [pause] "
   "And the defining shift: electric vehicles, creating clear winners and losers. [pause] "
   "The classic trap? Buying when profits are at a record and the P-E looks low — because cyclicals look cheapest right at the peak, just before margins roll over. Buy into a recovery, not at peak margins.",
   "How to analyse auto stocks — monthly volumes, segment mix, input costs, the EV shift, and strategies.",
   ["auto stocks india","ev stocks","nifty auto","automobile sector"]),
 S("sectors","fmc","en",M,"SECTOR","FMCG Stocks","Volume & valuation","never overpay",
   ["The great defensive — steady demand","VOLUME growth, not value growth","Rural is ~1/3 of sales","Pricing power is the real moat","Biggest risk: overpaying for the calm"],
   "FMCG — the soaps, foods and everyday products in every home — is the great defensive of the market. People buy them in booms and busts alike. [pause] "
   "That makes these classic slow-and-steady compounders, but the metrics are subtle. [pause] "
   "The number-one number is volume growth — real units sold, not value inflated by price hikes. A company can raise prices while selling fewer packs, and that isn't healthy. [pause] "
   "Watch the rural-urban split, since rural is about a third of sales and swings with the monsoon. And watch pricing power — the ability to pass on cost rises without losing customers. That's the real moat. [pause] "
   "But here's the one big risk: these leaders trade at rich valuations. Overpay, and your returns stay flat for years even as the business thrives. Great companies — just never overpay for the comfort.",
   "How to analyse FMCG stocks — volume growth, rural demand, margins, the defensive role, and valuation.",
   ["fmcg stocks india","consumer staples","nifty fmcg","defensive stocks"]),
 S("sectors","met","en",R,"SECTOR","Metal Stocks","LME, cost & the cycle","buy the fear",
   ["LME prices & China set the revenue","Lowest cost-per-tonne producer wins","EBITDA per tonne compares true profit","Net debt is deadly at the cycle bottom","Low P/E appears at the PEAK — a trap"],
   "Metals — steel, aluminium, copper — are the most cyclical corner of the market, and they don't control their own destiny. [pause] "
   "Global prices, set on the London Metal Exchange, and China's demand, decide their revenue — more than anything happening in India. So you watch the world, not local news. [pause] "
   "In a business where everyone sells at the same price, the lowest cost-per-tonne producer wins every cycle, because when prices crash, the cheap producer survives while the expensive one bleeds. [pause] "
   "Compare EBITDA per tonne for true profitability, and above all, fear debt — a net-debt load that looks fine at the top becomes lethal at the bottom. [pause] "
   "The great trap is a low P-E, which appears right at the cyclical peak. Judge them by the cycle, not the multiple. In metals, buy the fear and sell the euphoria.",
   "How to analyse metal stocks — LME prices, cost per tonne, net debt, and cyclical timing.",
   ["metal stocks india","steel stocks","nifty metal","commodity cycle"]),
 S("sectors","ene","en",M,"SECTOR","Energy Stocks","Oil, gas & power","which side of crude?",
   ["4 businesses: upstream, OMCs, gas, power","Crude HELPS producers, HURTS refiners","OMCs: GRM + marketing margin","Cheap valuations hide policy risk","Power & renewables = structural growth"],
   "Energy isn't one business — it's four, and they react in opposite ways. [pause] "
   "Upstream producers, who pull oil from the ground, profit when crude is high. But the oil marketing companies — the refiners — benefit when crude is low, because their margins expand. So the same crude move sends different energy stocks in opposite directions. [pause] "
   "For refiners, watch the gross refining margin and the marketing margin, adjusted for crude-driven inventory swings. [pause] "
   "These stocks look temptingly cheap, but that reflects real policy risk — governments can force them to hold pump prices, crushing margins. [pause] "
   "The structural growth is in power and renewables, riding India's rising electricity demand and the green shift. [pause] "
   "So before you buy any energy stock, always ask: which side of crude am I on?",
   "How to analyse energy stocks — upstream vs OMCs vs gas vs power, GRM, crude sensitivity, and strategies.",
   ["energy stocks india","oil and gas","omc stocks","refining margin"]),
 S("sectors","rea","en",V,"SECTOR","Realty & Infra","Cash & the cycle","watch pre-sales",
   ["Rate cuts are the master driver","Pre-sales/bookings > reported revenue","Collections = the real cash engine","Net debt is deadly in a downturn","REITs pay steady rental income"],
   "Real estate builds the nation, and it's one of the most cyclical sectors of all — driven above all by interest rates. A rate-cut cycle is often the fuse that lights a property boom. [pause] "
   "But here, reported profit lies, because accounting makes sold homes show up as revenue years later. [pause] "
   "So the number-one metric is pre-sales, or bookings — the value of homes actually sold this period — a far truer measure of demand. [pause] "
   "Then collections, the real cash coming in from buyers, and net debt, which turns deadly in a downturn, exactly like metals. [pause] "
   "Favour the low-debt, branded developers who survived the last bust — they gain share every cycle. [pause] "
   "And if you'd rather have steady income than developer risk, REITs pay you a regular rental yield. In realty, watch the cash and fear the debt.",
   "How to analyse real estate & infra stocks — pre-sales, collections, net debt, the rate cycle, and REITs.",
   ["real estate stocks","realty","reit india","nifty realty"]),
 S("sectors","che","en",C,"SECTOR","Chemical Stocks","Specialty vs commodity","China+1",
   ["Not all chemicals are equal","Specialty = sticky clients, fat margins","Commodity = cyclical, like metals","China+1 is the tailwind; dumping the risk","Margin stability reveals the winners"],
   "Chemicals is one of India's most exciting structural stories, but 'chemicals' hides two very different worlds. [pause] "
   "Specialty chemicals are custom, high-value molecules with sticky customers, pricing power, and fat, stable margins. These are the great compounders. [pause] "
   "Commodity, or bulk, chemicals are sold purely on price — cyclical and low-margin, and you analyse them just like metals. [pause] "
   "The whole investment thesis is China-plus-one: as the world de-risks its supply chains away from China, India's specialty and contract-manufacturing players win multi-year contracts. The risk is Chinese dumping, which can crash prices. [pause] "
   "The tell that separates the two? Margin stability. High, steady margins reveal a specialty winner; violent swings reveal a commodity cyclical. [pause] "
   "So hold specialty for years, trade commodity like a cycle, and never call every chemical stock a China-plus-one winner.",
   "How to analyse chemical stocks — specialty vs commodity, the China+1 theme, margins, and strategies.",
   ["chemical stocks india","specialty chemicals","china plus one","nifty chemicals"]),
 S("sectors","mtl","en",V,"SECTOR","Telecom & Media","ARPU & disruption","back the disruptor",
   ["Telecom: ARPU is the #1 metric","A 3-player market = pricing power","Telecom's weakness is heavy debt","Media: subscription > cyclical ads","Streaming: demand a path to PROFIT"],
   "Telecom and media — connecting and entertaining a billion-plus people. [pause] "
   "For telecom, the master metric is A-R-P-U: the average revenue per user. After years of price wars, tariff hikes are finally lifting it, and with a fixed subscriber base, every rupee of higher ARPU flows straight to profit. [pause] "
   "The market has consolidated to three big players, which restores real pricing power. But telecom's weakness is heavy debt — buying spectrum and building networks costs staggering sums. [pause] "
   "On the media side, favour steady subscription revenue over cyclical advertising, and beware legacy TV and print in structural decline. [pause] "
   "For any streaming platform, demand a real path to profit — subscriber growth funded by an endless content arms race destroys value. [pause] "
   "The whole sector comes down to one question: is this company the disruptor, or the one being disrupted? Back the disruptor.",
   "How to analyse telecom & media stocks — ARPU, debt, 5G, the digital shift, and strategies.",
   ["telecom stocks india","media stocks","arpu","ott streaming"]),

 # ================= STOCK MARKET (Telugu) — course, ~60s each =================
 S("smteic","sm-ch01","te",G,"పార్ట్ 01","షేర్ అంటే\nఏమిటి?","బేసిక్స్ · IPO · Nifty","సున్నా నుండి",
   ["షేర్ = కంపెనీలో చిన్న యాజమాన్య వాటా","IPO ద్వారా కంపెనీ డబ్బు సేకరిస్తుంది","NSE, BSE = మార్కెట్ యార్డులు","SEBI = అంపైర్; డీమ్యాట్‌లో షేర్లు","Sensex 30, Nifty 50 = థర్మామీటర్లు"],
   "షేర్ అంటే ఏమిటి? ఒక కంపెనీని చిన్న ముక్కలుగా విభజిస్తే, ప్రతి ముక్కా ఒక షేర్. [pause] "
   "మీరు షేర్ కొంటే — ఆ కంపెనీలో మీరు భాగస్వామి. కంపెనీ ఎదిగితే మీ షేర్ విలువా పెరుగుతుంది. [pause] "
   "కంపెనీలు మొదటిసారి షేర్లు అమ్మడాన్నే IPO అంటారు — దీంతో అవి పెట్టుబడి సేకరిస్తాయి. [pause] "
   "ఈ షేర్లు కొనడం, అమ్మడం జరిగేది NSE, BSE అనే స్టాక్ ఎక్స్ఛేంజీల్లో. వీటన్నిటిపై SEBI అనే నియంత్రణ సంస్థ నిఘా పెడుతుంది. [pause] "
   "మీ షేర్లు డీమ్యాట్ ఖాతాలో భద్రంగా ఉంటాయి. [pause] "
   "టీవీలో వినే సెన్సెక్స్, నిఫ్టీ అంటే — మార్కెట్ మొత్తానికి థర్మామీటర్లు. ఇదే స్టాక్ మార్కెట్ పునాది.",
   "Stock market basics in Telugu — shares, IPO, NSE, BSE, SEBI, Sensex and Nifty.",
   ["stock market basics telugu","what is share telugu"]),
 S("smteic","sm-ch02","te",C,"పార్ట్ 02","మొదటి\nఅడుగు","డీమ్యాట్ · బ్రోకర్","ఖాతా తెరవడం",
   ["3 ఖాతాలు: బ్యాంక్, ట్రేడింగ్, డీమ్యాట్","KYCకి PAN + ఆధార్ చాలు","కొత్తవారికి డిస్కౌంట్ బ్రోకర్","మార్కెట్ vs లిమిట్ vs స్టాప్-లాస్","T+1: రేపటికి షేర్లు డీమ్యాట్‌లో"],
   "పెట్టుబడి మొదలుపెట్టడానికి మూడు ఖాతాలు కావాలి — బ్యాంక్, ట్రేడింగ్, డీమ్యాట్. [pause] "
   "ఈ రోజుల్లో బ్రోకర్ యాప్‌లో PAN, ఆధార్‌తో KYC పది నిమిషాల్లో పూర్తవుతుంది. [pause] "
   "కొత్తవారికి Zerodha, Groww లాంటి డిస్కౌంట్ బ్రోకర్ సరిపోతుంది — డెలివరీపై బ్రోకరేజ్ సున్నా. [pause] "
   "ఆర్డర్ పెట్టేటప్పుడు — మార్కెట్ ఆర్డర్ అంటే ఇప్పటి ధరకే కొనడం, లిమిట్ ఆర్డర్ అంటే మీరు చెప్పిన ధరకే, స్టాప్-లాస్ అంటే నష్టం హద్దు దాటితే ఆటోమేటిక్ అమ్మకం. [pause] "
   "ఈ రోజు కొంటే, రేపటికి — అంటే T ప్లస్ వన్‌కి — షేర్లు మీ డీమ్యాట్‌లోకి వస్తాయి. [pause] "
   "చిన్న మొత్తంతో, తెలిసిన కంపెనీలతో మొదలుపెట్టండి.",
   "How to open a demat account and place your first order — in Telugu.",
   ["demat account telugu","how to buy shares telugu"]),
 S("smteic","sm-ch03","te",G,"పార్ట్ 03","ఈక్విటీ\nపెట్టుబడి","కాంపౌండింగ్ మహిమ","సంపద",
   ["కాంపౌండింగ్ = లాభంపై లాభం","మార్కెట్ క్యాప్, PE, డివిడెండ్","లార్జ్ = స్థిరం, స్మాల్ = రిస్క్","కొనే ముందు 5 ప్రశ్నలు","డైవర్సిఫికేషన్ — గుడ్లన్నీ ఒకే బుట్టలో వద్దు"],
   "దీర్ఘకాల సంపదకు అసలు రహస్యం — కాంపౌండింగ్. మీ లాభంపై మళ్ళీ లాభం. [pause] "
   "మొదటి పది సంవత్సరాలు నెమ్మదిగా అనిపిస్తుంది, తర్వాతే మ్యాజిక్ మొదలవుతుంది. అందుకే గెలిచేది తెలివైనవాడు కాదు — ఓపిక ఉన్నవాడు. [pause] "
   "కంపెనీని కొలవడానికి — మార్కెట్ క్యాప్, PE రేషియో, డివిడెండ్, లాభాల వృద్ధి చూడండి. [pause] "
   "సైజు బట్టి లార్జ్ క్యాప్ స్థిరం, మిడ్ వేగం, స్మాల్ రిస్క్. కొత్తవారు లార్జ్ క్యాప్‌తో మొదలుపెట్టడం సురక్షితం. [pause] "
   "కొనే ముందు అడగండి — వ్యాపారం అర్థమైందా, లాభాలు పెరుగుతున్నాయా, అప్పులు అదుపులో ఉన్నాయా. [pause] "
   "చివరిగా — గుడ్లన్నీ ఒకే బుట్టలో పెట్టవద్దు. రంగాల మధ్య, సాధనాల మధ్య పంచండి.",
   "Equity investing and the magic of compounding — in Telugu.",
   ["equity investing telugu","compounding telugu"]),
 S("smteic","sm-ch04","te",G,"పార్ట్ 04","మ్యూచువల్\nఫండ్స్ & SIP","NAV · SIP మ్యాజిక్","₹500 నుండి",
   ["అందరి డబ్బు + నిపుణుల నిర్వహణ","NAV = యూనిట్ ధర","ఈక్విటీ, డెట్, హైబ్రిడ్ ఫండ్స్","SIP = నెల నెలా ఆటోమేటిక్","పడినప్పుడు ఎక్కువ యూనిట్లు"],
   "సొంతంగా షేర్లు ఎంచుకునే సమయం, పరిజ్ఞానం లేకపోతే — మ్యూచువల్ ఫండ్ చక్కటి పరిష్కారం. [pause] "
   "వేలాది మంది డబ్బును ఒక చోట పోగు చేసి, నిపుణుడైన ఫండ్ మేనేజర్ ఎన్నో కంపెనీల్లో పెడతాడు. ₹500 తోనే మొదలుపెట్టవచ్చు. [pause] "
   "ఇక్కడ షేర్ బదులు యూనిట్లు కొంటారు — యూనిట్ ధరనే NAV అంటారు. [pause] "
   "ఫండ్ రకాలు — ఈక్విటీ దీర్ఘకాలానికి, డెట్ స్థిరత్వానికి, హైబ్రిడ్ మధ్యలో. [pause] "
   "అసలు మ్యాజిక్ — SIP. ప్రతి నెలా నిర్ణీత మొత్తం ఆటోమేటిక్‌గా పెడతారు. మార్కెట్ తగ్గిన నెలలో ఎక్కువ యూనిట్లు వస్తాయి. [pause] "
   "దీన్నే రూపీ-కాస్ట్ యావరేజింగ్ అంటారు — టైమింగ్ ఊహించే పని లేదు.",
   "Mutual funds and SIP explained in Telugu — start with ₹500.",
   ["mutual funds telugu","sip telugu"]),
 S("smteic","sm-ch05","te",M,"పార్ట్ 05","ఫండ్స్\nలోతుగా","డైరెక్ట్ · ELSS","పన్ను ఆదా",
   ["ఎక్స్‌పెన్స్ రేషియో ఏటా కట్","డైరెక్ట్ ప్లాన్ = కమీషన్ లేదు","ELSS = 80C పన్ను ఆదా","గత ఏడాది టాపర్ కాదు — స్థిరత్వం","డైరెక్ట్ + గ్రోత్ = డిఫాల్ట్"],
   "ప్రతి ఫండ్ నిర్వహణకు ఏటా ఒక ఫీజు తీసుకుంటుంది — దాన్నే ఎక్స్‌పెన్స్ రేషియో అంటారు. చిన్నదిగా అనిపించినా, దీర్ఘకాలంలో లక్షల తేడా చేస్తుంది. [pause] "
   "ప్రతి ఫండ్‌కు రెండు వెర్షన్లు — రెగ్యులర్‌లో ఏజెంట్ కమీషన్ ఉంటుంది, డైరెక్ట్‌లో ఉండదు. అదే ఫండ్, తక్కువ ఖర్చు, ఎక్కువ రాబడి. [pause] "
   "పాత పన్ను విధానంలో ఉంటే — ELSS తో 80C కింద పన్ను ఆదా, లాక్-ఇన్ మూడేళ్లే. [pause] "
   "ఫండ్ ఎంచుకునేటప్పుడు గత ఏడాది టాపర్ కాదు — ఐదు, పదేళ్ల స్థిరత్వం, తక్కువ ఎక్స్‌పెన్స్ రేషియో చూడండి. [pause] "
   "డిఫాల్ట్ ఎంపిక సింపుల్ — డైరెక్ట్ ప్లాన్, గ్రోత్ ఆప్షన్.",
   "Expense ratio, direct plans, ELSS — mutual funds deep dive in Telugu.",
   ["direct mutual fund telugu","elss telugu"]),
 S("smteic","sm-ch06","te",C,"పార్ట్ 06","ఇండెక్స్\n& ETF","పాసివ్ · చౌక","0.2% ఖర్చు",
   ["ఇండెక్స్ ఫండ్ = మార్కెట్‌నే కాపీ","ఫీజు ~0.2% మాత్రమే","చాలా యాక్టివ్ ఫండ్స్ ఓడిపోతాయి","ETF = షేర్ లా లైవ్ ట్రేడ్","SIPకి ఇండెక్స్, లైవ్‌కి ETF"],
   "మంచి షేర్లు ఎంచుకోవడం నిపుణులకే కష్టం. మరి ఎంచుకోకుండా, నిఫ్టీలోని యాభై కంపెనీలనూ అదే నిష్పత్తిలో కొనేస్తే? అదే ఇండెక్స్ ఫండ్. [pause] "
   "మేనేజర్ ప్రత్యేక నిర్ణయాలు తీసుకోడు, ఇండెక్స్‌ను కాపీ చేస్తాడు. అందుకే ఫీజు అతి తక్కువ — ఏటా దాదాపు పాయింట్ రెండు శాతమే. [pause] "
   "ఆసక్తికరం ఏమిటంటే — దీర్ఘకాలంలో చాలా యాక్టివ్ ఫండ్స్ ఈ సింపుల్ ఇండెక్స్‌ను ఓడించలేకపోతున్నాయి. [pause] "
   "ETF అంటే — ఇండెక్స్ బుట్టే, కానీ షేర్ లాగా ఎక్స్ఛేంజ్‌లో లైవ్‌గా ట్రేడ్ అవుతుంది. దీనికి డీమ్యాట్ కావాలి. [pause] "
   "సూత్రం సింపుల్ — SIPకి ఇండెక్స్ ఫండ్, లైవ్ ట్రేడింగ్‌కి ETF.",
   "Index funds and ETFs explained in Telugu — the cheap way to own the market.",
   ["index fund telugu","etf telugu"]),
 S("smteic","sm-ch07","te",V,"పార్ట్ 07","ఇంట్రాడే\nనిజాలు","చార్ట్ · రిస్క్","71% నష్టం",
   ["ఇంట్రాడే = ఆ రోజే కొని అమ్మడం","క్యాండిల్ చార్ట్ చదవడం","లివరేజ్ రెండు వైపులా కత్తి","SEBI: 71% మంది నష్టపోతారు","ముందు ఇన్వెస్టింగ్ నేర్చుకోండి"],
   "ఇంట్రాడే అంటే — ఈ రోజు కొని, ఇదే రోజు అమ్మడం. షేర్లు మీ దగ్గర ఉండవు, పొజిషన్ అదే రోజు క్లోజ్ అవుతుంది. [pause] "
   "ట్రేడర్లు చూసేది క్యాండిల్ చార్ట్ — ఆకుపచ్చ అంటే పెరిగిన రోజు, ఎరుపు అంటే తగ్గిన రోజు. [pause] "
   "ఇక్కడ బ్రోకర్లు లివరేజ్ ఇస్తారు — చిన్న డబ్బుకు పెద్ద పొజిషన్. కానీ లివరేజ్ లాభాలతో పాటు నష్టాలనూ పెంచుతుంది. [pause] "
   "ఇక్కడ ఎవరూ చెప్పని నిజం — SEBI అధ్యయనం ప్రకారం, ఇంట్రాడేలో పది మందిలో ఏడుగురు, అంటే డెబ్బై ఒక్క శాతం మంది నష్టపోయారు. [pause] "
   "అందుకే కొత్తవారికి మా సూచన — ముందు ఇన్వెస్టింగ్ నేర్చుకోండి, ట్రేడింగ్ తర్వాత, చిన్నగా.",
   "The truth about intraday trading in Telugu — 71% lose money.",
   ["intraday trading telugu","candlestick telugu"]),
 S("smteic","sm-ch08","te",V,"పార్ట్ 08","ఫ్యూచర్స్","లాట్ · మార్జిన్","10x లివరేజ్",
   ["ఫ్యూచర్ = భవిష్యత్ ధరపై ఒప్పందం","లాట్‌లుగానే ట్రేడ్","మార్జిన్ ~10–15% → 10x లివరేజ్","రోజూ మార్క్-టు-మార్కెట్","హెడ్జింగ్ = అసలు ఉపయోగం"],
   "ఫ్యూచర్ అంటే — భవిష్యత్ ధరపై ఈ రోజే కుదిరే ఒప్పందం. ఒక రైతు తన పంట ధరను ముందే లాక్ చేసుకున్నట్టు. [pause] "
   "ఇవి లాట్‌లుగానే ట్రేడ్ అవుతాయి — ఒక్క లాట్ విలువే లక్షల్లో ఉంటుంది. [pause] "
   "పూర్తి విలువ కట్టనవసరం లేదు — దాదాపు పది, పదిహేను శాతం మార్జిన్ చాలు. అంటే పది రెట్ల లివరేజ్. మార్కెట్ ఐదు శాతం పెరిగితే మీ మార్జిన్‌పై యాభై శాతం లాభం. కానీ పడితే అదే వేగంతో నష్టం. [pause] "
   "ఫ్యూచర్స్‌లో లాభనష్టాలు రోజూ లెక్కకట్టి సర్దుబాటు చేస్తారు — దీన్నే మార్క్-టు-మార్కెట్ అంటారు. [pause] "
   "ఫ్యూచర్స్ అసలు ఉపయోగం హెడ్జింగ్ — రక్షణ. స్పెక్యులేషన్‌లోనే చాలామంది నష్టపోతారు.",
   "Futures trading explained in Telugu — lots, margin, and 10x leverage.",
   ["futures telugu","fno telugu"]),
 S("smteic","sm-ch09","te",V,"పార్ట్ 09","ఆప్షన్స్\nబేసిక్స్","కాల్ · పుట్","బీమా లాంటిది",
   ["ఆప్షన్ = బీమా లాంటి హక్కు","కాల్ = కొనే హక్కు (పెరుగుతుందని)","పుట్ = అమ్మే హక్కు (పడుతుందని)","స్ట్రైక్ ధర, ప్రీమియం, ఎక్స్పైరీ","కొన్నవారి నష్టం = ప్రీమియం వరకే"],
   "ఆప్షన్ అర్థం కావాలంటే మీ కారు బీమా గుర్తు చేసుకోండి. చిన్న ప్రీమియం కడతారు, ప్రమాదం జరిగితే కంపెనీ కడుతుంది, జరగకపోతే ప్రీమియం మాత్రమే పోతుంది. [pause] "
   "ఆప్షన్ కూడా అంతే — చిన్న ప్రీమియంతో ఒక హక్కు కొంటారు. రెండే రకాలు. [pause] "
   "కాల్ ఆప్షన్ — ఒక ధరకు కొనే హక్కు. షేర్ పెరుగుతుందని నమ్మితే కాల్ కొంటారు. [pause] "
   "పుట్ ఆప్షన్ — ఒక ధరకు అమ్మే హక్కు. షేర్ పడుతుందని నమ్మితే పుట్ కొంటారు. [pause] "
   "ఆ నిర్ణీత ధరను స్ట్రైక్ అంటారు, హక్కు గడువును ఎక్స్పైరీ అంటారు. [pause] "
   "కొన్నవారి అందం — నష్టం ప్రీమియం వరకే పరిమితం, లాభం మాత్రం పెద్దది. కానీ టైమ్ డికే శత్రువు.",
   "Options basics in Telugu — calls, puts, and payoffs, like insurance.",
   ["options telugu","call put telugu"]),
 S("smteic","sm-ch10","te",R,"పార్ట్ 10","ఆప్షన్స్\nనిజాలు","టైమ్ డికే","91% నష్టం",
   ["టైమ్ డికే = కరిగే ఐస్ ముక్క","ప్రతి రోజూ ప్రీమియం కరుగుతుంది","టైమ్ అమ్మేవారి పక్షం","SEBI: 91% F&O ట్రేడర్లు నష్టం","F&O చివరి మెట్టు మాత్రమే"],
   "ఆప్షన్ కొన్నవారి అతిపెద్ద శత్రువు — సమయం. [pause] "
   "ప్రీమియంలోని టైమ్ విలువ, ఎండలో పెట్టిన ఐస్ ముక్క లాగా ప్రతి రోజూ కరుగుతుంది. షేర్ కదలకపోయినా, కొన్నవారి డబ్బు తగ్గుతూనే ఉంటుంది. [pause] "
   "అందుకే — టైమ్ ఎప్పుడూ అమ్మేవారి పక్షం. చాలా ఆప్షన్లు విలువ లేకుండా ఎక్స్పైర్ అవుతాయి. [pause] "
   "ఇప్పుడు అతి ముఖ్యమైన నిజం — SEBI అధ్యయనం ప్రకారం, F&O ట్రేడ్ చేసిన వారిలో తొంభై ఒక్క శాతం మంది నష్టపోయారు. ఒకే ఏడాదిలో లక్ష కోట్లకు పైగా నష్టం. [pause] "
   "అందుకే F&O అనేది — నేర్చుకున్నాక, పెద్ద పోర్ట్‌ఫోలియో వచ్చాక, చివరి మెట్టు మాత్రమే. కొత్తవారికి అస్సలు అవసరం లేదు.",
   "Options reality in Telugu — time decay and the SEBI 91% loss study.",
   ["options reality telugu","time decay telugu"]),
 S("smteic","sm-ch11","te",M,"పార్ట్ 11","పన్నులు &\nఛార్జీలు","STCG · LTCG","12.5%",
   ["≤12 నెలలు: STCG 20%","‌>12 నెలలు: LTCG 12.5%","ఏటా ₹1.25 లక్ష లాభం పన్ను రహితం","STT, GST, బ్రోకరేజ్ ఛార్జీలు","తక్కువ ట్రేడ్ = ఎక్కువ ఆదా"],
   "లాభం రావడం ఒక ఎత్తు — దాన్ని ఎంత మిగుల్చుకుంటారన్నది ఇంకో ఎత్తు. [pause] "
   "ఈక్విటీ లాభంపై పన్ను హోల్డింగ్ కాలాన్ని బట్టి — పన్నెండు నెలల్లోపు అమ్మితే STCG, ఇరవై శాతం. [pause] "
   "పన్నెండు నెలలు దాటాక అమ్మితే LTCG, పన్నెండున్నర శాతం. అందులోనూ ఏటా మొదటి లక్షా పావు లాభంపై పన్నే లేదు. [pause] "
   "అంటే — ఏడాది ఓపిక పడితే పన్ను సగానికి పైగా తగ్గుతుంది. ఓపికకు ప్రభుత్వమే బహుమతి. [pause] "
   "పన్నే కాదు — ప్రతి ట్రేడ్‌పై STT, GST, బ్రోకరేజ్, ఇతర ఛార్జీలు కూడా పడతాయి. [pause] "
   "ఒక్కో ట్రేడ్‌కు చిన్నవే అయినా, రోజూ ట్రేడ్ చేస్తే పెద్ద మొత్తం. తక్కువ ట్రేడ్ చేయడమే పెద్ద ఆదా.",
   "Stock market taxes in Telugu — STCG, LTCG, and the ₹1.25L exemption.",
   ["capital gains tax telugu","ltcg stcg telugu"]),
 S("smteic","sm-ch12","te",G,"పార్ట్ 12","పోర్ట్‌ఫోలియో\nరోడ్‌మ్యాప్","పునాది · కేటాయింపు","ప్రణాళిక",
   ["ముందు అత్యవసర నిధి + బీమా","అధిక వడ్డీ అప్పులు తీర్చండి","ఈక్విటీ, గోల్డ్, డెట్ మధ్య పంచండి","మోసాల నుండి రక్షణ","ఖాతా → SIP → నేర్చుకో → పెంచు"],
   "పెట్టుబడి మొదలుపెట్టే ముందు పునాది మెట్లు ఎక్కాలి. [pause] "
   "మొదటిది — ఆరు నెలల ఖర్చులకు అత్యవసర నిధి. రెండోది — టర్మ్ లైఫ్, హెల్త్ బీమా. మూడోది — క్రెడిట్ కార్డ్ లాంటి అధిక వడ్డీ అప్పులు ముందు తీర్చండి. [pause] "
   "ఆ తర్వాతే పెట్టుబడి. డబ్బును ఈక్విటీ, గోల్డ్, డెట్ మధ్య పంచండి — ఇదే అసెట్ కేటాయింపు, రాబడిలో ఇదే కీలకం. [pause] "
   "మోసాల నుండి జాగ్రత్త — గ్యారంటీడ్ రిటర్న్స్ అనేవాడు మోసగాడు, టిప్స్ గ్రూపులకు దూరంగా, OTP ఎవరికీ చెప్పకండి. [pause] "
   "రోడ్‌మ్యాప్ సింపుల్ — ఖాతా తెరవండి, ఇండెక్స్ SIP మొదలుపెట్టండి, నేర్చుకుంటూ పెంచండి, ఓపిక పట్టండి. పర్ఫెక్ట్ టైమ్ కోసం ఎదురుచూడకండి.",
   "Portfolio building and a 5-step roadmap in Telugu.",
   ["portfolio telugu","asset allocation telugu"]),
 S("smteic","sm-ch13","te",C,"పార్ట్ 13","IPO\nమాస్టర్‌క్లాస్","దరఖాస్తు · అలాట్","లాటరీ",
   ["IPO = మొదటిసారి ప్రజలకు షేర్లు","UPIతో దరఖాస్తు, డబ్బు బ్లాక్","ఓవర్‌సబ్‌స్క్రైబ్ అయితే లాటరీ","ఎక్కువ లాట్లు వేసినా అవకాశం పెరగదు","GMP అనధికారికం — జోస్యం కాదు"],
   "IPO అంటే — ఒక కంపెనీ మొదటిసారి ప్రజలకు షేర్లు అమ్మడం. [pause] "
   "మీరు బ్రోకర్ యాప్‌లో లాట్ల చొప్పున దరఖాస్తు చేసి, UPI మాండేట్ ఆమోదిస్తారు. ఇక్కడ డబ్బు కట్ అవదు — బ్లాక్ మాత్రమే అవుతుంది. [pause] "
   "డిమాండ్ ఎక్కువైతే, అంటే ఓవర్‌సబ్‌స్క్రైబ్ అయితే — అలాట్‌మెంట్ కంప్యూటరైజ్డ్ లాటరీ ద్వారా జరుగుతుంది. అందరికీ రాదు. [pause] "
   "ముఖ్య విషయం — ప్రతి దరఖాస్తుకు ఒకే ఛాన్స్. ఎక్కువ లాట్లు వేసినా అవకాశం పెరగదు. నిజంగా పెంచుకోవాలంటే — కుటుంబ సభ్యుల PANలతో విడిగా దరఖాస్తు చేయడమే మార్గం. [pause] "
   "GMP, అంటే గ్రే మార్కెట్ ప్రీమియం, అనధికారికం — దాన్ని జోస్యంగా కాదు, సూచికగా మాత్రమే చూడండి. హైప్‌కు కాదు, కంపెనీ విలువకు దరఖాస్తు చేయండి.",
   "IPO masterclass in Telugu — process, application, and allotment.",
   ["ipo telugu","ipo allotment telugu"]),
 S("smteic","sm-ch14","te",V,"పార్ట్ 14","పెట్టుబడి\nమనస్తత్వం","భయం · దురాశ","EQ ఆట",
   ["మంద మనస్తత్వం, FOMO","నష్ట భయం — పడినప్పుడు అమ్మేయడం","దురాశ శిఖరం = ప్రమాదం","భయం తారస్థాయి = అవకాశం","రాతపూర్వక ప్లాన్ + SIP ఆటోమేషన్"],
   "మార్కెట్‌లో మీ అతిపెద్ద శత్రువు మార్కెట్ కాదు — మీ మనసే. [pause] "
   "మెదడు ఆడే ట్రిక్కులు — అందరూ కొంటున్నారని కొనడం, మిస్ అవుతానేమో అనే FOMO, పడినప్పుడు భయంతో అమ్మేయడం. [pause] "
   "మార్కెట్ ఎప్పుడూ రెండు భావోద్వేగాల మధ్య ఊగుతుంది — భయం, దురాశ. అందరూ దురాశతో కొనే శిఖరమే ప్రమాదం, అందరూ భయపడే తారస్థాయే మంచి కొనుగోలు సమయం. [pause] "
   "వారెన్ బఫెట్ సూత్రం ఇదే — ఇతరులు దురాశ పడుతున్నప్పుడు భయపడు, భయపడుతున్నప్పుడు దురాశ పడు. [pause] "
   "మనసును గెలవడానికి — రాతపూర్వక ప్లాన్ పెట్టుకోండి, SIP ఆటోమేట్ చేయండి, పోర్ట్‌ఫోలియో నెలకోసారి చూడండి. [pause] "
   "పెట్టుబడి తెలివితేటల ఆట కాదు — నిగ్రహం ఆట.",
   "Investor psychology in Telugu — the 4 biases and how to beat them.",
   ["investor psychology telugu","trading psychology telugu"]),
 S("smteic","sm-ch15","te",C,"పార్ట్ 15","కంపెనీని\nచదవడం","బాలెన్స్ షీట్ · ROE","అనాలిసిస్",
   ["P&L, బాలెన్స్ షీట్, క్యాష్ ఫ్లో","నగదు నిజం, కాగితపు లాభం అభిప్రాయం","ROE 15%+, తక్కువ అప్పు, PE","ప్రమోటర్ హోల్డింగ్ చూడండి","మోట్ + నిజాయితీ యాజమాన్యం"],
   "షేర్ అంటే తెరపై కదిలే సంఖ్య కాదు — వెనుక ఉన్న సజీవ వ్యాపారం. దాన్ని చదవడం నేర్చుకుందాం. [pause] "
   "ప్రతి కంపెనీ మూడు పత్రాలు ఇస్తుంది — లాభనష్టాల పట్టీ, బాలెన్స్ షీట్, క్యాష్ ఫ్లో. గుర్తుంచుకోండి — నగదు నిజం, కాగితపు లాభం కేవలం అభిప్రాయం. [pause] "
   "నాలుగు నిష్పత్తులు — ROE పదిహేను శాతం పైన, అప్పు తక్కువ, PE రంగం సగటుతో పోల్చి, ప్రమోటర్ హోల్డింగ్ ఎక్కువ. [pause] "
   "వాటాలు తనఖా పెడితే జాగ్రత్త. [pause] "
   "అంకెలు గతాన్ని చెబుతాయి. అసలు కావాల్సింది — మోట్, అంటే పోటీదారులు దాటలేని బలం, బలమైన బ్రాండ్, తక్కువ ఖర్చు. [pause] "
   "గొప్ప కంపెనీ — మోట్, ధర పెంచగల శక్తి, నిజాయితీ యాజమాన్యం ఉన్నది. దాన్ని మంచి ధరకు కొని దశాబ్దాలు ఉంచుకోండి.",
   "Fundamental analysis in Telugu — balance sheet, ROE, PE, and moats.",
   ["fundamental analysis telugu","roe pe telugu"]),
 S("smteic","sm-ch16","te",M,"పార్ట్ 16","గోల్డ్ · REIT\n· బాండ్లు","ఈక్విటీకి ఆవల","వైవిధ్యం",
   ["నగలు కాదు — గోల్డ్ ETF/ఫండ్స్","గోల్డ్ 5–10% హెడ్జ్‌గా","REIT = భవనాల్లో వాటా + అద్దె","ప్రభుత్వ బాండ్లు సురక్షితం","4 ఆస్తి తరగతులు = స్థిరం"],
   "ఈక్విటీకి ఆవల ఉన్న ప్రపంచం — గోల్డ్, రియల్ ఎస్టేట్, బాండ్లు. వీటిని కూడా డీమ్యాట్ నుండే కొనవచ్చు. [pause] "
   "బంగారం పెట్టుబడికి నగలు తెలివైన దారి కాదు — మేకింగ్ ఛార్జీలు పోతాయి. బదులుగా గోల్డ్ ETF లేదా గోల్డ్ ఫండ్స్ వాడండి. ఈక్విటీ పడినప్పుడు బంగారం నిలబడుతుంది — అందుకే ఐదు నుండి పది శాతం హెడ్జ్‌గా ఉంచండి. [pause] "
   "REIT అంటే — పెద్ద ఆఫీస్ భవనాల్లో మీకు వాటా. షేర్ లాగా కొనొచ్చు, అద్దెల నుండి ఆదాయం వస్తుంది. [pause] "
   "బాండ్లు అంటే — స్థిర వడ్డీతో మీరిచ్చే అప్పు. ప్రభుత్వ బాండ్లు అత్యంత సురక్షితం, కార్పొరేట్‌లో రేటింగ్ చూడండి. [pause] "
   "నాలుగు ఆస్తి తరగతుల బల్ల ఎప్పుడూ స్థిరంగా నిలబడుతుంది. ఏటా ఒకసారి రీబ్యాలెన్స్ చేయండి.",
   "Gold ETF, REITs and bonds in Telugu — beyond equity.",
   ["gold etf telugu","reit telugu"]),
 S("smteic","sm-ch17","te",G,"పార్ట్ 17","టెక్నికల్\nఅనాలిసిస్","ట్రెండ్ · సపోర్ట్","చార్ట్‌లు",
   ["ట్రెండ్ = దిశ; ఎదురు ఈదకు","సపోర్ట్ = నేల, రెసిస్టెన్స్ = పైకప్పు","వాల్యూమ్ = కదలికకు సాక్ష్యం","మూవింగ్ యావరేజ్ = అసలు దిశ","టెక్నికల్స్ = టైమింగ్, జోస్యం కాదు"],
   "టెక్నికల్ అనాలిసిస్ అంటే — చార్ట్ చదవడం. ఇది కంపెనీ విలువ చెప్పదు, కానీ మార్కెట్ మూడ్, ఎంట్రీ టైమింగ్ చూపిస్తుంది. [pause] "
   "మొదటి పాఠం — ట్రెండ్, అంటే దిశ. ధర వరుసగా పైకి కదులుతూ ఉంటే అప్‌ట్రెండ్. ట్రెండ్‌కు ఎదురు ఈదకండి. [pause] "
   "సపోర్ట్ అంటే నేల — ధర పడుతూ వచ్చి ఆగే స్థాయి. రెసిస్టెన్స్ అంటే పైకప్పు — పెరుగుతూ వచ్చి ఆగే స్థాయి. [pause] "
   "వాల్యూమ్ అంటే ఎన్ని షేర్లు చేతులు మారాయో — కదలికకు సాక్ష్యం. వాల్యూమ్ లేని కదలిక అనుమానాస్పదం. [pause] "
   "మూవింగ్ యావరేజ్ రోజువారీ గందరగోళాన్ని తీసేసి అసలు దిశ చూపిస్తుంది. [pause] "
   "కానీ గుర్తుంచుకోండి — ఇవన్నీ సంభావ్యత సాధనాలు, జోస్యం కాదు. దీర్ఘకాల పెట్టుబడికి ఫండమెంటల్సే పునాది.",
   "Technical analysis basics in Telugu — trend, support, resistance, MA.",
   ["technical analysis telugu","chart telugu"]),
 S("smteic","sm-ch18","te",G,"పార్ట్ 18","లక్ష్యాల\nప్రణాళిక","బకెట్లు · రిటైర్మెంట్","ప్లానింగ్",
   ["లక్ష్యాలను కాలం వారీగా విభజించు","దగ్గరివి = డెట్, దూరవి = ఈక్విటీ","10 ఏళ్ల ఆలస్యం = కార్పస్ మూడో వంతు","ద్రవ్యోల్బణం కలిపి లెక్కించు","గడువు ముందే ఈక్విటీ → డెట్"],
   "పెట్టుబడి ఎంత అన్నది కాదు మొదటి ప్రశ్న — దేనికోసం అన్నదే. [pause] "
   "లక్ష్యాలను కాలం వారీగా విభజించండి. మూడేళ్లలోపు లక్ష్యాలకు — కారు, ట్రిప్ — ఈక్విటీ వద్దు, FD, డెట్ ఫండ్స్ చాలు. [pause] "
   "ఏడేళ్లు దాటిన లక్ష్యాలకు — పిల్లల చదువు, రిటైర్మెంట్ — ఈక్విటీ పూర్తి శక్తి, ఎందుకంటే సమయం మీ పక్షాన. [pause] "
   "రిటైర్మెంట్ లెక్కలో అతిపెద్ద ఖర్చు ఆలస్యం. పదేళ్లు ఆలస్యం చేస్తే కార్పస్ మూడో వంతుకు పడిపోతుంది — కాంపౌండింగ్ చివరి ఏళ్లలోనే పేలుతుంది. [pause] "
   "ద్రవ్యోల్బణం మర్చిపోవద్దు — నేటి యాభై లక్షలు పదిహేనేళ్లకు కోటి. [pause] "
   "గడువు దగ్గర పడుతుంటే ఈక్విటీ నుండి డెట్‌కు మార్చండి. మొదలుపెట్టడానికి ఉత్తమ రోజు ఈ రోజే.",
   "Goal-based planning in Telugu — time buckets and retirement maths.",
   ["goal planning telugu","retirement telugu"]),
 S("smteic","sm-ch19","te",M,"పార్ట్ 19","రిటైర్మెంట్\nసాధనాలు","EPF · PPF · NPS","పెన్షన్",
   ["EPF = ఉద్యోగుల ఆటోమేటిక్","PPF = 15 ఏళ్లు, పన్ను రహితం","NPS = మార్కెట్ ఆధారిత పెన్షన్","స్థిర వడ్డీ − ద్రవ్యోల్బణం = ~2%","వృద్ధికి ఈక్విటీ తప్పనిసరి"],
   "రిటైర్మెంట్ కోసం మూడు ప్రభుత్వ సాధనాలు. [pause] "
   "EPF — ఉద్యోగుల ప్రావిడెంట్ ఫండ్. జీతం నుండి ఆటోమేటిక్‌గా కట్ అయ్యి, స్థిర వడ్డీ ఇస్తుంది. [pause] "
   "PPF — ఎవరైనా తెరవచ్చు, పదిహేనేళ్ల లాక్-ఇన్, పూర్తి పన్ను రహిత రాబడి. [pause] "
   "NPS — మీ డబ్బు ఈక్విటీ, డెట్ మిక్స్‌లో పెరుగుతుంది, అదనపు పన్ను మినహాయింపులతో. [pause] "
   "కానీ ఒక నిజం — స్థిర వడ్డీ ఎనిమిది శాతం అయినా, ద్రవ్యోల్బణం ఆరు శాతం తీసేస్తే నికరంగా మిగిలేది రెండు శాతమే. [pause] "
   "అందుకే భద్రతకు EPF, PPF, వృద్ధికి ఈక్విటీ, NPS — రెండూ కలిస్తేనే పూర్తి జట్టు. యువ వయసులో ఈక్విటీ ఎక్కువ, వయసుతో డెట్ వైపు.",
   "Retirement instruments in Telugu — EPF, PPF, NPS vs equity.",
   ["epf ppf nps telugu","retirement telugu"]),
 S("smteic","sm-ch20","te",G,"పార్ట్ 20","రిజల్ట్స్ &\nడివిడెండ్లు","Q1 · మార్జిన్","ఫలితాలు",
   ["4 అంకెలు: రెవెన్యూ, లాభం, మార్జిన్, గైడెన్స్","YoY పోల్చండి","మంచి ఫలితం ≠ షేర్ పెరుగుదల","డివిడెండ్ = పంట మీద పండు","ధరను కాదు, వ్యాపారాన్ని ఫాలో"],
   "ప్రతి కంపెనీ మూడు నెలలకోసారి ఫలితాలు ప్రకటిస్తుంది — దీన్నే రిజల్ట్స్ సీజన్ అంటారు. [pause] "
   "చూడాల్సినవి నాలుగు అంకెలు — రెవెన్యూ అంటే అమ్మకాలు, నెట్ ప్రాఫిట్, మార్జిన్, మేనేజ్‌మెంట్ గైడెన్స్. గత ఏడాది ఇదే క్వార్టర్‌తో పోల్చండి. [pause] "
   "ఇక్కడ ఆశ్చర్యం — మంచి ఫలితం వచ్చినా షేర్ పడొచ్చు. ఎందుకంటే మార్కెట్ అంచనాలతో నడుస్తుంది. అంచనాల కంటే మెరుగ్గా వస్తేనే ధర స్పందిస్తుంది. [pause] "
   "డివిడెండ్ అంటే — కంపెనీ లాభాల్లో మీకు పంచే వాటా. షేర్ ధర పెరుగుదల పైన అదనపు ఆదాయం. [pause] "
   "కానీ మరీ ఎక్కువ ఈల్డ్ కనిపిస్తే అనుమానించండి. మీ పని — ఒక రోజు ధర కదలిక కాదు, వ్యాపార దిశ చదవడం.",
   "Reading quarterly results and dividends in Telugu.",
   ["quarterly results telugu","dividend telugu"]),
 S("smteic","sm-ch21","te",C,"పార్ట్ 21","కొత్తవారి\nప్రశ్నలు","15 FAQ","సందేహాలు",
   ["₹500తో ఈ రోజే మొదలుపెట్టవచ్చు","SIPకి మార్కెట్ టైమింగ్ అనవసరం","షేర్లు NSDL/CDSLలో భద్రం","పోర్ట్‌ఫోలియో నెలకోసారి చాలు","టిప్స్ గ్రూపులకు దూరంగా"],
   "కొత్త పెట్టుబడిదారుల టాప్ ప్రశ్నలకు సూటి జవాబులు. [pause] "
   "ఎంతతో మొదలుపెట్టాలి? ఐదు వందలు చాలు — మొత్తం కాదు, అలవాటే ముఖ్యం. మార్కెట్ ఎప్పుడు ఎంటర్ అవ్వాలి? SIP చేసేవారికి టైమింగ్ అనవసరం, ఈ రోజే ఉత్తమ రోజు. [pause] "
   "బ్రోకర్ మునిగిపోతే నా షేర్లు పోతాయా? లేదు — షేర్లు బ్రోకర్ దగ్గర కాదు, NSDL, CDSL డిపాజిటరీల్లో మీ పేరుతో ఉంటాయి. [pause] "
   "రోజూ ఎంతసేపు చూడాలి? దీర్ఘకాలికులకు నెలకోసారి చాలు — ఎక్కువ చూస్తే ఎక్కువ తప్పులు. [pause] "
   "టిప్స్ గ్రూపులు జాయిన్ అవ్వాలా? వద్దు — ఉచిత టిప్ వెనుక ఎప్పుడూ స్వార్థం ఉంటుంది. [pause] "
   "మొదటి ఏడాది లక్ష్యం లాభం కాదు — నేర్చుకోవడం.",
   "Top beginner questions answered in Telugu.",
   ["stock market faq telugu","beginner telugu"]),

 # ================= STOCK MARKET (Telugu) — updates, ~60s each =================
 S("smteic","sm-expert","te",V,"అప్‌డేట్","నిపుణులు ఏం\nచెబుతున్నారు?","4 టాప్ వాయిస్‌లు","2026",
   ["Arora: ఓడేవాటిని వదిలేయి","Mukherjea: క్వాలిటీ లార్జ్ క్యాప్","Nilesh Shah: 90% అసెట్ అలొకేషన్","Shenoy: రూల్స్, భావోద్వేగం వద్దు","ఉమ్మడి: క్వాలిటీ + అలొకేషన్ + ఓపిక"],
   "కోట్లు నిర్వహించే నిపుణులు 2026లో ఏం చెబుతున్నారో చూద్దాం. [pause] "
   "సమీర్ అరోరా — ఎలిమినేషన్ స్ట్రాటజీ. ఎవరు గెలుస్తారో ఊహించడం కష్టం, ఓడేవాటిని వదిలేయడం సులభం. [pause] "
   "సౌరభ్ ముఖర్జియా — క్వాలిటీ లార్జ్ క్యాప్ వైపు. స్మాల్ క్యాప్ వాల్యుయేషన్‌లు ఇరవై ఏళ్ల గరిష్ఠంలో ఉన్నాయని హెచ్చరిక. [pause] "
   "నిలేష్ షా — రాబడిలో తొంభై శాతం అసెట్ అలొకేషన్ నుండే వస్తుంది, స్టాక్ ఎంపిక నుండి పదే. [pause] "
   "దీపక్ శెనోయ్ — రూల్స్-బేస్డ్, భావోద్వేగం లేని పెట్టుబడి. [pause] "
   "నిపుణులు వేర్వేరు, కానీ ఉమ్మడి సందేశం ఒకటే — క్వాలిటీ, అసెట్ అలొకేషన్, క్రమశిక్షణ, ఓపిక. ఇవి వారి వ్యక్తిగత అభిప్రాయాలు, సలహా కాదు.",
   "What top fund managers are saying — Telugu strategy digest.",
   ["expert strategy telugu","saurabh mukherjea telugu"]),
 S("smteic","sm-ipoguide","te",V,"అప్‌డేట్","2026 IPO\nగైడ్","Jio · లాటరీ","మెగా IPO",
   ["వచ్చే వారం + మెగా పైప్‌లైన్","Reliance Jio = అతిపెద్ద IPO","దరఖాస్తు: కట్-ఆఫ్ + UPI బ్లాక్","10x సబ్: ప్రతి 10కి 1","GMP వెంట పరుగెత్తొద్దు"],
   "2026లో దాదాపు రెండున్నర లక్షల కోట్ల IPOలు వస్తాయని అంచనా — రికార్డు స్థాయి. [pause] "
   "అత్యధిక ఆసక్తి Reliance Jio పైనే — దాదాపు పన్నెండు లక్షల కోట్ల విలువతో, చరిత్రలోనే అతిపెద్ద IPO కావచ్చు. [pause] "
   "దరఖాస్తు ఎలా? యాప్‌లో ఫండ్ ఎంచుకుని, కట్-ఆఫ్ ధరకు లాట్లు వేసి, UPI మాండేట్ ఆమోదించండి. డబ్బు బ్లాక్ మాత్రమే అవుతుంది. [pause] "
   "ఓవర్‌సబ్‌స్క్రైబ్ అయితే అలాట్‌మెంట్ లాటరీ. పది రెట్లు సబ్‌స్క్రైబ్ అయితే ప్రతి పది దరఖాస్తులకు ఒక్కరికే. ఎక్కువ లాట్లు వేసినా అవకాశం పెరగదు. [pause] "
   "GMP అనధికారిక సూచిక — జోస్యం కాదు. హైప్‌కు కాదు, కంపెనీ విలువకు దరఖాస్తు చేయండి.",
   "2026 IPO guide in Telugu — calendar, Reliance Jio, allotment lottery.",
   ["ipo 2026 telugu","reliance jio ipo telugu"]),
 S("smteic","sm-ipolisting","te",V,"అప్‌డేట్","IPO\nలిస్టింగ్","GMP · ఎగ్జిట్","సెంటిమెంట్",
   ["సబ్‌స్క్రిప్షన్ + GMP = సెంటిమెంట్","SME = అధిక రిస్క్, తక్కువ లిక్విడిటీ","GMP క్షణక్షణం మారుతుంది","ఎగ్జిట్: టార్గెట్ + స్టాప్-లాస్","SMEకి లిమిట్ ఆర్డర్ వాడండి"],
   "లిస్టింగ్ రోజు ముందు సెంటిమెంట్ ఎలా చదవాలి? రెండు అంకెలు — సబ్‌స్క్రిప్షన్, GMP. [pause] "
   "ఎక్కువ సబ్‌స్క్రిప్షన్, ఎక్కువ GMP అంటే హైప్ ఎక్కువ. కానీ ఇది గ్యారంటీ కాదు — చాలా IPOలు ఇష్యూ ధర కంటే కిందికే లిస్ట్ అయ్యాయి. [pause] "
   "SME IPOలలో GMP తొంభై శాతం కనిపించినా — SME అంటే అధిక రిస్క్, తక్కువ లిక్విడిటీ, ఆకస్మిక రివర్సల్‌లు. [pause] "
   "GMP అనధికారికం, క్షణక్షణం మారుతుంది — దాన్ని జోస్యంగా చూడకండి. [pause] "
   "ఎగ్జిట్ స్ట్రాటజీ — లిస్టింగ్‌కు ముందే నిర్ణయించుకోండి, టార్గెట్, స్టాప్-లాస్ పెట్టండి. SME అమ్మేటప్పుడు లిమిట్ ఆర్డర్ వాడండి, లేకపోతే తక్కువ ధరకు అమ్ముడుపోవచ్చు.",
   "IPO listing sentiment, GMP and exit strategy in Telugu.",
   ["ipo listing telugu","ipo gmp telugu"]),
 S("smteic","sm-wrap","te",R,"అప్‌డేట్","మార్కెట్ ఎందుకు\nపడింది?","20 జూలై","−443",
   ["సెన్సెక్స్ −443, నిఫ్టీ −96","HDFC, Axis మార్జిన్ మిస్","క్రూడ్ $90+ (US-Iran)","FII అమ్మకం","మిడ్‌క్యాప్ పచ్చగా — సెక్టార్ షాక్"],
   "జూలై ఇరవైన మార్కెట్ ఎందుకు పడింది? సెన్సెక్స్ నాలుగు వందల నలభై మూడు, నిఫ్టీ తొంభై ఆరు పాయింట్లు తగ్గాయి. [pause] "
   "మొదటి కారణం — ప్రైవేట్ బ్యాంకుల మార్జిన్ మిస్. HDFC, Axis బ్యాంకుల Q1 NIM అంచనాలను అందుకోలేదు, రెండూ ఐదు శాతం పడ్డాయి. [pause] "
   "రెండోది — US, Iran ఉద్రిక్తతతో క్రూడ్ తొంభై డాలర్లు దాటడం. మూడోది — విదేశీ సంస్థల అమ్మకం. [pause] "
   "కానీ ఒక ముఖ్య విషయం — మిడ్‌క్యాప్, స్మాల్‌క్యాప్ పెరిగాయి. అంటే ఇది ఒక సెక్టార్‌కు పరిమితమైన షాక్, భారీ పతనం కాదు. [pause] "
   "పాఠం — లాభం పెరిగినా NIM తగ్గితే బ్యాంక్ షేర్ పడుతుంది. SIP పెట్టుబడిదారులకు ఇలాంటి ఒక ఎర్ర రోజు కేవలం నాయిస్.",
   "Why the market fell — Telugu post-market wrap.",
   ["market wrap telugu","nifty fell telugu"]),
 S("smteic","sm-premarket","te",M,"అప్‌డేట్","రేపటి\nవాచ్‌లిస్ట్","లార్జ్/మిడ్/స్మాల్","ప్రీ-మార్కెట్",
   ["GIFT Nifty = ఓపెనింగ్ సూచిక","క్రూడ్ $90+, ఎక్స్‌పైరీ రోజు","లార్జ్: RIL, ICICI, HDFC","గోల్డ్ థీమ్: Titan, Kalyan","ఇది వాచ్‌లిస్ట్ — జోస్యం కాదు"],
   "రేపటి ప్రీ-మార్కెట్ సెటప్ చూద్దాం. ముందుగా ఒక నిజం — రేపు ఏ షేర్ ఖచ్చితంగా పెరుగుతుందో ఎవరూ చెప్పలేరు. ఇది వాచ్‌లిస్ట్, జోస్యం కాదు. [pause] "
   "GIFT Nifty రేపటి ఓపెనింగ్‌కు సూచిక — ఇది మెత్తగా ఉంది. క్రూడ్ తొంభై దాటింది, రేపు ఎక్స్‌పైరీ రోజు — హెచ్చుతగ్గులు ఎక్కువ. [pause] "
   "లార్జ్ క్యాప్ ఫోకస్ — Reliance, ICICI బ్యాంక్ ఫలితాలతో, HDFC మిక్స్డ్. [pause] "
   "మిడ్, స్మాల్ క్యాప్‌లో వేడి థీమ్ — జ్యువెలరీ, బంగారం. Titan, Kalyan, Thangamayil — రికార్డు బంగారం ధరల ఊతంతో. [pause] "
   "ఫోకస్‌లో ఉంది అంటే వార్త ఉంది అని — పెరుగుతుందని కాదు. ఉదయం కదలిక చూసి, స్టాప్-లాస్‌తో నిర్ణయించండి.",
   "Tomorrow's pre-market watchlist in Telugu.",
   ["pre market telugu","stocks to watch telugu"]),
 S("smteic","sm-strat1","te",G,"అప్‌డేట్","కొత్త\nవ్యూహాలు","SEBI రూల్స్","2026",
   ["SEBI true-to-label రూల్స్","కోర్-శాటిలైట్ 70/30","మొమెంటమ్ ఇండెక్స్ ఫండ్స్","₹1.25 లక్ష LTCG హార్వెస్టింగ్","అన్నీ ఫ్రేమ్‌వర్క్‌లు, టిప్స్ కాదు"],
   "2026లో స్టాక్ మార్కెట్ చాలా మారింది. నాలుగు తాజా వ్యూహాలు. [pause] "
   "మొదటిది — SEBI కొత్త రూల్స్. ఫండ్ పేరు ఏం చెబుతుందో అదే పెట్టాలి — ట్రూ-టు-లేబుల్. మిస్-సెల్లింగ్ తగ్గుతుంది. [pause] "
   "రెండోది — కోర్-శాటిలైట్. డెబ్బై శాతం చౌక ఇండెక్స్ ఫండ్‌లో కోర్, ముప్పై శాతం మొమెంటమ్, థీమ్‌లో శాటిలైట్. [pause] "
   "మూడోది — మొమెంటమ్ ఇండెక్స్ ఫండ్స్. బలంగా పెరుగుతున్న షేర్లు, కానీ శాటిలైట్‌గా మాత్రమే, రిస్క్ తెలిసి. [pause] "
   "నాలుగోది — ప్రతి ఏడాది లక్షా పావు LTCG మినహాయింపును వాడుకోవడం. లాభాలు అమ్మి మళ్ళీ కొంటే పన్ను శాశ్వతంగా తగ్గుతుంది. [pause] "
   "ఇవన్నీ ఫ్రేమ్‌వర్క్‌లు — టిప్స్ కాదు.",
   "2026 new investing strategies in Telugu — SEBI rules and momentum.",
   ["investing strategy telugu","sebi rules telugu"]),
 S("smteic","sm-strat2","te",C,"అప్‌డేట్","ఎలా అమలు\nచేయాలి","Zerodha · Groww","స్టెప్-బై-స్టెప్",
   ["SIP: ఫండ్ → Direct+Growth → మాండేట్","Groww సులభం, Zerodha ఎకోసిస్టమ్","మొమెంటమ్: ఇండెక్స్ లేదా smallcase","పన్ను హార్వెస్టింగ్: అమ్ము→ఆగు→కొను","SIF ₹10L — కొత్తవారికి కాదు"],
   "వ్యూహాలు నేర్చుకున్నాం, ఇప్పుడు యాప్‌లలో ఎలా అమలు చేయాలో చూద్దాం. [pause] "
   "SIP పెట్టడం నాలుగు అడుగులు — ఫండ్ వెతకండి, డైరెక్ట్ ప్లాన్ గ్రోత్ ఎంచుకోండి, మొత్తం, తేదీ పెట్టండి, UPI మాండేట్ ఆమోదించండి. [pause] "
   "Groww సులభమైన ఇంటర్‌ఫేస్, Zerodha ఎకోసిస్టమ్ — Coin, smallcase, Varsity. కొత్తవారికి Groww బెస్ట్. [pause] "
   "మొమెంటమ్‌ను చౌక ఇండెక్స్ ఫండ్‌తో లేదా Zerodha smallcase తో అమలు చేయవచ్చు. [pause] "
   "పన్ను హార్వెస్టింగ్ — మార్చి ముప్పై ఒకటి లోపు లాభాలు అమ్మి, ఒక సెషన్ ఆగి, మళ్ళీ కొనండి. [pause] "
   "SIF అనే కొత్త సాధనం పది లక్షల కనీస పెట్టుబడితో — ఇది అడ్వాన్స్‌డ్, కొత్తవారికి కాదు.",
   "How to implement strategies in Zerodha, Groww, Upstox — Telugu.",
   ["zerodha groww telugu","how to invest telugu"]),
]

DISC_EN = "⚠️ Educational only — not investment advice."
DISC_TE = "⚠️ ఇది విద్య కోసమే — పెట్టుబడి సలహా కాదు."

def ffdur(p):
    return round(float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","default=noprint_wrappers=1:nokey=1",p],capture_output=True,text=True).stdout.strip()),3)

def tts(sid, lang, text):
    wav = os.path.join(PUBLIC, f"{sid}.wav")
    if os.path.exists(wav) and not FORCE: return ffdur(wav)
    chunks = [c.strip() for c in text.split("[pause]") if c.strip()]
    paths = []
    import time
    for ci, ch in enumerate(chunks):
        cp = os.path.join(RAW, f"{sid}_c{ci}.wav"); mp3 = cp[:-4] + ".mp3"
        for attempt in range(6):
            r = subprocess.run(["edge-tts","--voice",VOICE[lang],f"--rate={RATE}","--text",ch,"--write-media",mp3],capture_output=True)
            if r.returncode == 0 and os.path.exists(mp3) and os.path.getsize(mp3) > 0:
                break
            time.sleep(3 + attempt * 4)  # backoff on transient TTS/network/rate-limit failures
        else:
            raise RuntimeError(f"edge-tts failed after retries for {sid} chunk {ci}")
        subprocess.run(["ffmpeg","-y","-i",mp3,"-ar","24000","-ac","1",cp],check=True,capture_output=True); os.remove(mp3)
        paths.append(cp)
    sil = os.path.join(RAW, "_p.wav")
    if not os.path.exists(sil):
        subprocess.run(["ffmpeg","-y","-f","lavfi","-i","anullsrc=r=24000:cl=mono","-t",str(PAUSE),sil],check=True,capture_output=True)
    lst = os.path.join(RAW, f"{sid}_l.txt")
    with open(lst,"w") as f:
        for i,pp in enumerate(paths):
            f.write(f"file '{pp}'\n")
            if i < len(paths)-1: f.write(f"file '{sil}'\n")
    subprocess.run(["ffmpeg","-y","-f","concat","-safe","0","-i",lst,"-c","copy",wav],check=True,capture_output=True)
    return ffdur(wav)

def build_one(s):
    dur = tts(s["sid"], s["lang"], s["script"]) + 1.0
    props = {"badge": s["badge"], "title": s["title"], "sub": s["sub"], "keyword": s["keyword"],
             "accent": s["accent"], "brand": FOLDERS[s["folder"]][1], "highlights": s["highlights"],
             "audioSrc": f"short/{s['sid']}.wav", "durationSec": round(dur, 2)}
    pj = os.path.join(os.path.dirname(__file__), "artifacts", f"{s['sid']}.json")
    json.dump(props, open(pj, "w"), ensure_ascii=False)
    subdir = os.path.join(GV, FOLDERS[s["folder"]][0]); os.makedirs(subdir, exist_ok=True)
    out = os.path.join(subdir, f"{s['sid']}-short.mp4")
    subprocess.run(["npx","remotion","render","Short",out,f"--props={pj}","--concurrency=4"], cwd=COMPOSER, capture_output=True)
    ok = os.path.exists(out) and ffdur(out) > 40
    disc = DISC_TE if s["lang"]=="te" else DISC_EN
    title_yt = f"{s['title'].replace(chr(10),' ')} in 60 Seconds #Shorts"
    tags = ", ".join(dict.fromkeys(s["tags"] + FOLDERS[s["folder"]][2]))
    plain = re.sub(r"\s+"," ",s["script"].replace("[pause]"," ")).strip()
    yt = (f"# {s['title'].replace(chr(10),' ')} — Short\n\n**Title**\n{title_yt}\n\n"
          f"**Description**\n{s['ytdesc']}\n\n{plain}\n\nFull video on the channel. ▶️\n\n{disc}\n\n"
          f"#Shorts #StockMarket #Investing\n\n**Tags**\n{tags}")
    ig = (f"**Instagram Reel — {s['title'].replace(chr(10),' ')}**\n\n{s['ytdesc']}\n\n"
          f"Full video → link in bio.\n{disc}\n\n"
          f"#reels #stockmarket #investing #trading #finance #{'telugu' if s['lang']=='te' else 'stocks'}")
    open(os.path.join(subdir, f"{s['sid']}-short.youtube.md"), "w").write(yt)
    open(os.path.join(subdir, f"{s['sid']}-short.instagram.md"), "w").write(ig)
    print(f"  {'OK ' if ok else 'ERR'} {s['sid']} ({props['durationSec']}s)", flush=True)
    return {"file": f"{s['sid']}-short.mp4", "title": title_yt, "description": s["ytdesc"], "tags": tags}

if __name__ == "__main__":
    keys = [a for a in sys.argv[1:] if a in FOLDERS] or list(FOLDERS)
    rows = {}
    for s in SHORTS:
        if s["folder"] in keys:
            rows.setdefault(s["folder"], []).append(build_one(s))
    for folder, rr in rows.items():
        subdir = os.path.join(GV, FOLDERS[folder][0])
        with open(os.path.join(subdir, "shorts.csv"), "w", newline="") as f:
            w = csv.writer(f); w.writerow(["file","title","description","tags"])
            for r in rr: w.writerow([r["file"], r["title"], r["description"], r["tags"]])
        print(f"{folder}: {len(rr)} shorts + metadata")
