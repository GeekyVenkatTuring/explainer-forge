#!/usr/bin/env python3
"""Equities, Futures, Options & Commodities — full ENGLISH course.
Voice: en-IN-NeerjaNeural (Indian English). Reuses `sm` parameterized scenes (English
props) + `eq` computed F&O scenes. Facts verified in research/dossier.md (sub-agent:
GO-WITH-CORRECTIONS, applied). Education only, not advice.

Usage: python3 build.py            (all)   |   python3 build.py eq01 eq02
"""
import json, os, re, subprocess, sys

VOICE = "en-IN-NeerjaNeural"; RATE = "-4%"; GAP = 0.5; PAUSE = 0.5; PREFIX = "eq"
ROOT = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(ROOT, "..", ".."))
PUBLIC = os.path.join(REPO, "composer", "public", PREFIX); RAW = os.path.join(ROOT, "assets", "raw"); FIN = os.path.join(ROOT, "assets")
for d in (PUBLIC, RAW, os.path.join(ROOT, "artifacts"), os.path.join(ROOT, "renders")):
    os.makedirs(d, exist_ok=True)

G, C, R, M, V = "#34D399", "#22D3EE", "#FB7185", "#FBBF24", "#A78BFA"  # up, mkt, down, money, deriv
SER = "📚 Part of the complete 'Equities, F&O & Commodities' course — see the playlist."
DISC = "⚠️ Educational content only — not investment advice. Consult a SEBI-registered adviser."

CHAPTERS = {
 # =================== CHAPTER 1 — FOUNDATIONS ===================
 "eq01": [
 ("a1_title", "sm_ptitle",
  {"title": "Equities, Futures & Options", "sub": "Sectors · Research · Strategies · Commodities — full course", "kicker": "MASTERCLASS · 2026"},
  "Welcome to the complete course on equities, futures, options, and commodities. [pause] "
  "This is a long, structured masterclass. We start from the very basics — what these instruments are — "
  "and build up, step by step, to the strategies professional investors and traders actually use. [pause] "
  "We will cover how to pick a sector, how to research a stock, where to find trustworthy research, "
  "futures and options explained simply, commodities, and every major strategy for each. [pause] "
  "One promise up front: this is education, not tips. We will never tell you what to buy. "
  "We will teach you how to think, so you can decide for yourself."),
 ("a1_promise", "sm_checklist",
  {"kicker": "WHAT YOU'LL LEARN", "title": "The roadmap of this course", "color": G, "icon": "🎯",
   "items": [
    "Which sector to select — and the top-down method",
    "How to research a stock — fundamentals + technicals",
    "Where to find real research — channels, tools, voices",
    "Futures & Options — what they are, and every strategy",
    "Commodities — gold, silver, crude on MCX",
    "Risk management — the rules that keep you in the game",
   ]},
  "Here is the roadmap. Six big blocks. [pause] "
  "First — which sector to select, using a top-down method the professionals use. [pause] "
  "Second — how to research a stock, both the fundamentals, the business and its numbers, and the technicals, the price chart. [pause] "
  "Third — where to find genuine research: the trustworthy YouTube channels, data tools, and market voices, and how to tell a real source from a tip-seller. [pause] "
  "Fourth — futures and options, explained from zero, with every major strategy. [pause] "
  "Fifth — commodities: gold, silver, and crude oil on the MCX. [pause] "
  "And running through all of it — sixth — risk management, the discipline that decides who survives. [pause] "
  "Let's begin with the big picture."),
 ("a1_arenas", "sm_iconcards",
  {"kicker": "THE FOUR ARENAS", "title": "Four ways to participate in markets", "color": C,
   "items": [
    {"emoji": "🏢", "k": "Equities", "v": "Owning a piece of a company. Buy a share, own a slice; grow as the business grows", "chip": "Ownership"},
    {"emoji": "📜", "k": "Futures", "v": "A contract to buy/sell later at a set price. Leveraged, expires — a derivative", "chip": "Contract"},
    {"emoji": "🎯", "k": "Options", "v": "The right, not obligation, to buy/sell at a strike. Pay a premium — a derivative", "chip": "Right"},
    {"emoji": "🥇", "k": "Commodities", "v": "Gold, silver, crude on the MCX — traded via futures contracts", "chip": "MCX"},
   ]},
  "There are four arenas we will master. [pause] "
  "The first is equities. This is ownership. When you buy a share, you own a small slice of a real business, and you grow as it grows. This is where wealth is built. [pause] "
  "The second is futures. A future is a contract to buy or sell something later, at a price fixed today. It is leveraged and it expires. It is a derivative — its value derives from an underlying asset. [pause] "
  "The third is options. An option gives you the right, but not the obligation, to buy or sell at a set price, for a small fee called a premium. Also a derivative. [pause] "
  "The fourth is commodities — gold, silver, crude oil — traded on the MCX, mostly through futures. [pause] "
  "Equities are for investing. Futures and options are powerful but risky tools. Commodities are a world of their own. We will do them all."),
 ("a1_structure", "sm_iconcards",
  {"kicker": "HOW THE MARKET WORKS", "title": "The Indian market — the basics", "color": C,
   "items": [
    {"emoji": "🏛️", "k": "Exchanges", "v": "NSE (1992) and BSE (1875) — where buyers and sellers meet electronically", "chip": "NSE · BSE"},
    {"emoji": "🛡️", "k": "SEBI", "v": "The regulator (1992) — the umpire that protects investors from fraud", "chip": "Regulator"},
    {"emoji": "🗄️", "k": "Demat", "v": "Shares held digitally with NSDL/CDSL; you need a demat + trading account", "chip": "Required"},
    {"emoji": "⏱️", "k": "Settlement", "v": "T+1 — shares reach your demat the next working day; hours 9:15 to 3:30", "chip": "T+1"},
   ]},
  "Before we go deeper, the plumbing — how the Indian market actually works. [pause] "
  "Buyers and sellers meet on two exchanges: the National Stock Exchange, founded 1992, and the Bombay Stock Exchange, Asia's oldest, from 1875. [pause] "
  "Watching over everyone is the regulator, SEBI — the Securities and Exchange Board of India. Think of it as the umpire whose job is to protect you. [pause] "
  "Your shares are held digitally, in a demat account, with one of two depositories, NSDL or CDSL. To trade you need a demat plus a trading account — most brokers open both together. [pause] "
  "When you buy, the shares reach your account the next working day — that's T plus one settlement. And the market is open from nine-fifteen in the morning to three-thirty in the afternoon, Monday to Friday. [pause] "
  "That's the stage. Now the play."),
 ("a1_recap", "sm_recap",
  {"title": "Chapter 1 — the foundation",
   "items": [
    "Four arenas: equities, futures, options, commodities",
    "Equities = ownership; F&O = derivatives; commodities = MCX",
    "NSE & BSE exchanges · SEBI the regulator",
    "Demat account, T+1 settlement, 9:15 to 3:30",
    "This course: learn to think, never blindly follow tips",
   ],
   "closer": "Master the basics — everything else is built on them."},
  "Let's lock in chapter one. [pause] "
  "There are four arenas: equities, futures, options, and commodities. [pause] "
  "Equities are ownership; futures and options are derivatives; commodities trade on the MCX. [pause] "
  "The NSE and BSE are the exchanges, SEBI is the regulator, your shares sit in a demat account, and settlement is T plus one. [pause] "
  "And the spirit of this course: we learn to think for ourselves — we never blindly follow tips. [pause] "
  "Next, the first real skill: how to choose a sector."),
 ],

 # =================== CHAPTER 2 — SECTOR SELECTION ===================
 "eq02": [
 ("b2_div", "sm_divider", {"n": 2, "title": "Choosing a Sector", "sub": "Top-down · drivers · rotation", "color": C},
  "Chapter two — choosing a sector. [pause] "
  "Before you pick a stock, pick the right neighbourhood. A great company in a struggling sector "
  "is an uphill battle; an average company in a booming sector often gets carried up. Let's learn how the pros choose."),
 ("b2_why", "sm_iconcards",
  {"kicker": "TOP-DOWN", "title": "Why start with the sector?", "color": C,
   "items": [
    {"emoji": "🌊", "k": "Ride the tide", "v": "A rising sector lifts most stocks in it; a falling one drags them down", "chip": "Tailwind"},
    {"emoji": "🔭", "k": "Top-down flow", "v": "Read the macro → pick the sector with the tailwind → pick the leaders in it", "chip": "Macro→Stock"},
    {"emoji": "🧭", "k": "Fewer, better bets", "v": "Narrowing to 1–2 strong sectors focuses your research and your risk", "chip": "Focus"},
    {"emoji": "⚖️", "k": "Balance", "v": "Spreading across a few uncorrelated sectors protects you when one falls", "chip": "Diversify"},
   ]},
  "Why start with the sector at all? Because of the tide. [pause] "
  "When a sector is in favour, money flows in and lifts almost every stock in it. When it falls out of favour, even good companies get dragged down. You want the tailwind, not the headwind. [pause] "
  "This gives us the professional method: top-down. First read the macro picture — interest rates, crude oil, the rupee, the economy. Then pick the sector that the macro favours. Then, and only then, pick the strongest one or two companies inside that sector. [pause] "
  "Macro, to sector, to stock. Narrowing your focus this way means better research and controlled risk. [pause] "
  "But you also spread across a few sectors that don't move together — so when one zigs, another zags."),
 ("b2_sectors", "sm_iconcards",
  {"kicker": "THE MAP", "title": "The main sectors of the market", "color": G,
   "items": [
    {"emoji": "🏦", "k": "Banking & Financials", "v": "The market's heaviest weight — banks, NBFCs, insurers", "chip": "Heavy"},
    {"emoji": "💻", "k": "IT Services", "v": "Exporters — TCS, Infosys; earn in dollars", "chip": "Export"},
    {"emoji": "💊", "k": "Pharma & FMCG", "v": "Defensives — steady demand in good times and bad", "chip": "Defensive"},
    {"emoji": "🚗", "k": "Auto · Metals · Realty", "v": "Cyclicals — boom in expansion, suffer in slowdowns", "chip": "Cyclical"},
    {"emoji": "🛢️", "k": "Energy & OMCs", "v": "BPCL, HPCL, IOC — moved by crude oil prices", "chip": "Crude"},
    {"emoji": "🛡️", "k": "PSU & Defence", "v": "HAL, BEL — government capex, budgets, order books", "chip": "Govt"},
   ]},
  "Let's map the main sectors. [pause] "
  "Banking and financials are the heaviest weight in the index — when banks move, the market moves. [pause] "
  "IT services are exporters; they earn in dollars, so a weak rupee helps them. [pause] "
  "Pharma and consumer staples, the FMCG companies, are defensives — people buy medicine and soap in every kind of economy, so their demand is steady. [pause] "
  "Auto, metals, and real estate are cyclicals — they boom when the economy expands and suffer when it slows. [pause] "
  "Energy and the oil marketing companies move with the price of crude. [pause] "
  "And public-sector and defence names live on government spending, budgets, and order books. [pause] "
  "Notice the deep split there: defensives versus cyclicals. That split is the key to timing sectors."),
 ("b2_drivers", "sm_compare3",
  {"kicker": "WHAT MOVES EACH", "title": "Every sector has a driver — watch it",
   "cols": [
    {"name": "Rate-sensitive", "color": G, "emoji": "🏦", "hi": True, "rows": [
     {"k": "Banks / NBFCs", "v": "RBI rates, credit growth, NIM"},
     {"k": "Realty / Infra", "v": "interest rates, govt capex"},
     {"k": "Auto", "v": "demand, rates, input costs"},
     {"k": "Watch", "v": "RBI policy day"}]},
    {"name": "Global-linked", "color": C, "emoji": "🌍", "rows": [
     {"k": "IT services", "v": "USD/INR, US & EU demand"},
     {"k": "Pharma", "v": "US FDA approvals / warnings"},
     {"k": "Metals", "v": "global cycle, China demand"},
     {"k": "Watch", "v": "dollar, crude, US data"}]},
    {"name": "Event-driven", "color": M, "emoji": "📢", "rows": [
     {"k": "OMCs (BPCL…)", "v": "crude oil price"},
     {"k": "PSU / Defence", "v": "Budget, order wins"},
     {"k": "FMCG / Auto", "v": "GST, monsoon, rural demand"},
     {"k": "Watch", "v": "Budget, results, policy"}]},
   ]},
  "Here is the single most useful table in sector analysis: what drives each one. [pause] "
  "Some sectors are rate-sensitive. Banks, non-bank lenders, real estate, and autos all care deeply about interest rates set by the RBI, about credit growth, and about margins. On RBI policy day, watch these. [pause] "
  "Others are globally linked. IT services live on the dollar-rupee rate and Western demand. Pharma swings on US FDA approvals and warnings. Metals follow the global commodity cycle and China. For these, watch the dollar, crude, and US data. [pause] "
  "And some are event-driven. Oil marketing companies move inversely with crude. Public-sector and defence names jump on the Budget and on order wins. Consumer and auto names react to GST changes, the monsoon, and rural demand. [pause] "
  "Learn each sector's one main driver, and the news suddenly tells you a story."),
 ("b2_cyclical", "sm_myths",
  {"kicker": "TIMING SECTORS", "title": "Cyclical vs Defensive — the rotation", "mythLabel": "✗ MYTH", "factLabel": "✓ REALITY",
   "pairs": [
    {"m": "One sector is always best to hold", "f": "Leadership rotates — different sectors lead in different phases"},
    {"m": "In a slowdown, hide in cash only", "f": "Defensives (FMCG, pharma, IT) tend to hold up better"},
    {"m": "Cyclicals are just risky", "f": "In an expansion, cyclicals (auto, metals, banks) often lead the rally"},
   ]},
  "Now the timing idea that ties it together — sector rotation. [pause] "
  "The first myth is that one sector is always the best place to be. It isn't. Leadership rotates. Different sectors lead in different phases of the economic cycle. [pause] "
  "In a slowdown or a risk-off market, you don't only hide in cash. Defensives — consumer staples, pharma, and often IT — tend to hold up better because their demand doesn't vanish. [pause] "
  "And cyclicals aren't just risky gambles. When the economy is expanding, cyclicals — autos, metals, banks — often lead the rally hardest. [pause] "
  "So the skill is reading which phase we're in, and rotating toward the sectors that phase favours. That's what the top-down process is really for."),
 ("b2_process", "sm_steps",
  {"kicker": "THE METHOD", "title": "Top-down sector selection — 4 steps", "color": G,
   "note": "Macro → Sector → Leaders → Position size. Never skip straight to a stock tip.",
   "items": [
    {"emoji": "🌐", "label": "Read macro", "sub": "rates, crude, USD/INR"},
    {"emoji": "🎯", "label": "Pick sector", "sub": "with the tailwind"},
    {"emoji": "🏆", "label": "Pick leaders", "sub": "strongest 1–2 in it"},
    {"emoji": "⚖️", "label": "Size & spread", "sub": "diversify, control risk"},
   ]},
  "Let's turn this into a repeatable four-step method. [pause] "
  "Step one — read the macro. Where are interest rates heading? What is crude doing? Is the rupee strong or weak? What's the state of the economy? [pause] "
  "Step two — pick the sector that this macro favours. If rates are falling, rate-sensitive banks and realty may benefit. If crude is spiking, oil producers gain and oil consumers hurt. [pause] "
  "Step three — inside that sector, pick the strongest one or two companies. The leaders, with the best balance sheets and the widest moats — not the weakest name hoping to catch up. [pause] "
  "Step four — size your position and spread across a few sectors so no single call can sink you. [pause] "
  "Macro, sector, leaders, size. Never skip straight from nowhere to a stock tip. That process is what the next chapter — research — makes real."),
 ("b2_recap", "sm_recap",
  {"title": "Chapter 2 — sectors",
   "items": [
    "Pick the neighbourhood before the house — ride the tailwind",
    "Top-down: macro → sector → leaders → size",
    "Learn each sector's one main driver",
    "Defensives hold up in slowdowns; cyclicals lead expansions",
    "Leadership rotates — that's sector rotation",
   ],
   "closer": "The right sector does half the work for you."},
  "Chapter two, in one breath. [pause] "
  "Pick the neighbourhood before the house — ride the tailwind, not the headwind. [pause] "
  "Use the top-down method: macro, to sector, to leaders, to position size. [pause] "
  "Learn each sector's single main driver, so the news becomes readable. [pause] "
  "Remember that defensives hold up in slowdowns while cyclicals lead expansions, and leadership rotates through the cycle. [pause] "
  "Next, we go inside a company — how to actually research a stock."),
 ],

 # =================== CHAPTER 3 — RESEARCH: FUNDAMENTALS ===================
 "eq03": [
 ("c3_div", "sm_divider", {"n": 3, "title": "Researching a Stock", "sub": "Fundamentals · the numbers · valuation", "color": G},
  "Chapter three — how to research a stock. [pause] "
  "This is the heart of investing. A share is not a lottery ticket with a symbol; it is a piece of a living business. "
  "Fundamental research is the craft of reading that business — what it earns, what it owns, what it owes, and whether its price is fair. Let's learn it properly."),
 ("c3_three", "sm_compare3",
  {"kicker": "THE 3 STATEMENTS", "title": "Read a company like a shopkeeper",
   "cols": [
    {"name": "Profit & Loss", "color": G, "emoji": "🧾", "hi": True, "rows": [
     {"k": "Shows", "v": "sales, costs, profit for the year"},
     {"k": "Shopkeeper", "v": "how much I sold & kept"},
     {"k": "Watch", "v": "sales & profit rising YoY"},
     {"k": "Key line", "v": "revenue, net profit, margin"}]},
    {"name": "Balance Sheet", "color": C, "emoji": "⚖️", "rows": [
     {"k": "Shows", "v": "assets vs debts — a snapshot"},
     {"k": "Shopkeeper", "v": "what the shop owns & owes"},
     {"k": "Watch", "v": "debt under control"},
     {"k": "Key line", "v": "assets, borrowings, equity"}]},
    {"name": "Cash Flow", "color": M, "emoji": "💧", "rows": [
     {"k": "Shows", "v": "real cash in and out"},
     {"k": "Shopkeeper", "v": "actual money in the till"},
     {"k": "Watch", "v": "positive operating cash"},
     {"k": "Key line", "v": "cash from operations"}]},
   ]},
  "Every listed company publishes three statements each year. Let's read them in the language of a simple shopkeeper. [pause] "
  "The first is the profit and loss statement. It shows sales, costs, and the profit left over for the year. In shop terms — how much I sold, and how much I kept. What you watch for is sales and profit rising year over year, and healthy margins. [pause] "
  "The second is the balance sheet. It is a snapshot, on one day, of everything the company owns — its assets — against everything it owes — its debts. In shop terms, what the shop owns and what it owes. Here you watch that debt is under control. [pause] "
  "The third, and most honest, is the cash flow statement. Profit on paper is an opinion; cash is a fact. This shows the real money that actually came in and went out. In shop terms, the actual money in the till. You want strong, positive cash from operations. [pause] "
  "A company with rising paper profit but weak cash flow is a shop selling everything on credit. That is a warning sign. Read all three together, and the business reveals itself."),
 ("c3_ratios", "sm_iconcards",
  {"kicker": "KEY RATIOS", "title": "Four numbers that reveal quality", "color": C,
   "items": [
    {"emoji": "💹", "k": "ROE / ROCE", "v": "Return on the owners' money. Above ~15% and steady is a strong sign", "chip": "Efficiency"},
    {"emoji": "🏋️", "k": "Debt-to-Equity", "v": "Borrowings vs own funds. Below 1 is generally safer; watch high debt", "chip": "Safety"},
    {"emoji": "🏷️", "k": "P/E ratio", "v": "Price you pay per ₹1 of earnings. Compare to the sector, never alone", "chip": "Valuation"},
    {"emoji": "📊", "k": "Promoter holding", "v": "Owners' stake — high & unpledged = conviction; pledged shares = red flag", "chip": "Trust"},
   ]},
  "From those statements come a handful of ratios that reveal quality fast. Four to know. [pause] "
  "The first is return on equity, and its cousin return on capital employed. This measures how much profit the company squeezes from the owners' money. Above roughly fifteen percent, held steadily for years, is the mark of a good business. [pause] "
  "The second is debt-to-equity — borrowings against the company's own funds. Below one is generally safer. A mountain of debt turns a small problem into a crisis. [pause] "
  "The third is the price-to-earnings ratio — the price you pay for one rupee of the company's annual earnings. A high P E means the stock is expensive. But never judge it alone — always compare it to the sector average and to the company's own history. [pause] "
  "The fourth is promoter holding — how much the founders themselves own. A high stake means their skin is in the game. But if those promoter shares are pledged — borrowed against — treat it as a red flag. [pause] "
  "These four, checked in a free screener in minutes, filter out most weak companies."),
 ("c3_moat", "sm_iconcards",
  {"kicker": "THE QUALITATIVE SIDE", "title": "Numbers aren't enough — find the moat", "color": G,
   "items": [
    {"emoji": "🏰", "k": "Moat", "v": "A durable edge rivals can't cross — brand, network, low cost, switching cost", "chip": "Durable"},
    {"emoji": "💰", "k": "Pricing power", "v": "Can it raise prices without losing customers? That's a great business", "chip": "Power"},
    {"emoji": "🧑‍💼", "k": "Management", "v": "Honest, capable, sensible with capital — read the annual report & concalls", "chip": "Integrity"},
    {"emoji": "🌱", "k": "Runway", "v": "A big, growing market ahead — room to compound for years", "chip": "Growth"},
   ]},
  "But numbers only tell you the past. Great investing needs the qualitative side — the story behind the numbers. Four things to judge. [pause] "
  "The first is the moat. Warren Buffett's word for a durable competitive edge that rivals cannot easily cross — a beloved brand, a powerful network, the lowest cost, or high switching costs that lock customers in. [pause] "
  "The second follows from it — pricing power. Can the company raise its prices a little without losing customers? If yes, that is a wonderful business, protected from inflation. [pause] "
  "The third is management. Are the people running it honest, capable, and sensible with the company's money? You judge this by reading the annual report and listening to the quarterly conference calls, where management answers analysts. [pause] "
  "The fourth is runway — is there a large and growing market ahead of the company, room to keep compounding for a decade? [pause] "
  "A wonderful business with a wide moat, run by honest people, in a growing market — that is what you hunt for."),
 ("c3_valuation", "sm_myths",
  {"kicker": "VALUATION", "title": "Great company ≠ great stock", "mythLabel": "✗ MYTH", "factLabel": "✓ REALITY",
   "pairs": [
    {"m": "A great company is always a great buy", "f": "Even the best business is a bad stock if you overpay"},
    {"m": "A low P/E always means cheap", "f": "It can be a trap — a dying business or hidden problem"},
    {"m": "Valuation is exact science", "f": "It's a range with a margin of safety — buy below your estimate"},
   ]},
  "Which brings us to the hardest lesson — valuation. The price you pay decides your return. [pause] "
  "The first myth is that a great company is always a great buy. It is not. Even the finest business in the world becomes a poor investment if you pay too high a price for it. The company can thrive while the stock goes nowhere for years, simply because it started too expensive. [pause] "
  "The second myth is that a low price-to-earnings ratio always means cheap. Sometimes it is a value trap — the market is pricing in a dying business or a hidden problem you haven't found yet. Cheap can get cheaper. [pause] "
  "The third myth is that valuation is an exact science. It isn't. It is a reasoned range. The wise investor estimates a fair value, then insists on buying comfortably below it. That gap is the margin of safety — your protection against being wrong. [pause] "
  "Great business, fair price, margin of safety. Get those three, and time does the rest."),
 ("c3_recap", "sm_recap",
  {"title": "Chapter 3 — fundamentals",
   "items": [
    "Read all 3 statements — P&L, balance sheet, cash flow",
    "Cash is fact; paper profit is opinion",
    "ROE >15%, low debt, P/E vs sector, promoter holding",
    "Find the moat, pricing power, honest management, runway",
    "Great company ≠ great stock — price + margin of safety",
   ],
   "closer": "Buy a wonderful business at a fair price."},
  "Chapter three, distilled. [pause] "
  "Read all three statements — profit and loss, balance sheet, and cash flow — and remember that cash is a fact while paper profit is only an opinion. [pause] "
  "Check the four ratios: return on equity above fifteen, low debt, price-to-earnings against the sector, and honest promoter holding. [pause] "
  "Then find the qualitative edge — the moat, pricing power, trustworthy management, and a long runway. [pause] "
  "And never forget: a great company is not a great stock unless the price is fair, with a margin of safety. [pause] "
  "Next, the other half of research — the price chart, the tools, and where to find real research."),
 ],

 # =================== CHAPTER 4 — RESEARCH: TECHNICALS, TOOLS & CHANNELS ===================
 "eq04": [
 ("d4_div", "sm_divider", {"n": 4, "title": "Charts, Tools & Sources", "sub": "Technicals · screeners · trusted channels", "color": C},
  "Chapter four — the price chart, the tools, and where to find genuine research. [pause] "
  "Fundamentals tell you WHAT to buy. Technicals help with WHEN. And knowing the right sources "
  "keeps you learning from teachers, not from tip-sellers. Let's cover all three."),
 ("d4_tech", "sm_iconcards",
  {"kicker": "TECHNICAL BASICS", "title": "Reading the price chart", "color": C,
   "items": [
    {"emoji": "📈", "k": "Trend", "v": "The direction — higher highs = uptrend. Rule one: don't fight the trend", "chip": "Direction"},
    {"emoji": "🛗", "k": "Support / Resistance", "v": "A floor where buyers step in; a ceiling where sellers appear", "chip": "Levels"},
    {"emoji": "📊", "k": "Volume", "v": "The conviction behind a move. A move without volume is suspect", "chip": "Proof"},
    {"emoji": "➰", "k": "Moving averages", "v": "Smoothed direction. 50-day crossing above 200-day = 'golden cross'", "chip": "Signal"},
   ]},
  "Technical analysis is the study of the price chart. It doesn't tell you what a company is worth — it tells you what the crowd is doing, which helps with timing. Four basics. [pause] "
  "The first is trend — simply the direction. A series of higher highs and higher lows is an uptrend. The trader's first rule is: don't fight the trend. Don't try to catch a falling knife. [pause] "
  "The second is support and resistance. Support is a price floor where buyers repeatedly step in. Resistance is a ceiling where sellers repeatedly appear. These levels are where the action happens. [pause] "
  "The third is volume — how many shares changed hands. Volume is the conviction behind a move. A big price move on strong volume is real; a move on thin volume is suspect. [pause] "
  "The fourth is moving averages, which smooth out the daily noise to reveal the true direction. When the fifty-day average crosses above the two-hundred-day, traders call it a golden cross — a classic sign of strength. [pause] "
  "A final caution: technicals are probabilities, not prophecy. The chart shows the past. Use it humbly."),
 ("d4_tools", "sm_iconcards",
  {"kicker": "THE TOOLKIT", "title": "Free & paid research tools", "color": M,
   "items": [
    {"emoji": "🔎", "k": "Screener.in", "v": "Free fundamentals, filings & custom screens — start here", "chip": "Screens"},
    {"emoji": "📇", "k": "Tickertape / Trendlyne", "v": "Ratios, scores, FII/DII flows, results calendar, broker reports", "chip": "Data"},
    {"emoji": "📑", "k": "Annual report + concall", "v": "The primary source — read management in their own words", "chip": "Primary"},
    {"emoji": "🏛️", "k": "NSE / BSE / SEBI", "v": "Official filings, announcements — the ground truth", "chip": "Official"},
   ]},
  "Where do you actually do this research? A toolkit — and the good news is the best tools are free. [pause] "
  "Start with Screener dot in. It gives you a company's financials, its filings, and lets you build custom screens — for example, all companies with return on equity above fifteen and debt below one. It is the beginner's best friend. [pause] "
  "Next, platforms like Tickertape and Trendlyne add clean ratios, quality scores, foreign and domestic investor flows, the results calendar, and broker reports in one place. [pause] "
  "But the single most valuable source is primary: the company's own annual report and its quarterly concall transcript. This is management speaking in their own words. Reading a few of these teaches you more than a hundred videos. [pause] "
  "And for the ground truth — official filings, announcements, order wins — go straight to the NSE, BSE, and SEBI websites. When in doubt, check the source."),
 ("d4_channels", "sm_iconcards",
  {"kicker": "TRUSTED CHANNELS", "title": "Where to learn — the popular channels", "color": G,
   "items": [
    {"emoji": "🎓", "k": "Zerodha Varsity", "v": "Free, structured, no tips — the gold standard for learning from zero", "chip": "Learn"},
    {"emoji": "📺", "k": "Educators", "v": "CA Rachana Ranade, Pranjal Kamra (Finology), Asset Yogi — concepts, not calls", "chip": "YouTube"},
    {"emoji": "🧮", "k": "Deeper / technical", "v": "Elearnmarkets by StockEdge, Yadnya — structured technical & derivatives", "chip": "Advanced"},
    {"emoji": "🗣️", "k": "Voices to follow", "v": "Fund managers on X: Samir Arora, Saurabh Mukherjea, Nilesh Shah, Deepak Shenoy", "chip": "Macro"},
   ]},
  "Now, where should you learn — the popular channels people actually trust. Present all of these as teachers of concepts, not sources of tips. [pause] "
  "For structured learning from absolute zero, the gold standard is Zerodha Varsity — free, thorough, and it never gives buy or sell calls. [pause] "
  "On YouTube, the most respected educators include CA Rachana Ranade, a chartered accountant who teaches fundamentals clearly; Pranjal Kamra of Finology, focused on long-term value investing; and Asset Yogi for financial literacy. They teach concepts, not calls. [pause] "
  "For deeper, more technical learning, Elearnmarkets by StockEdge and Yadnya Investment Academy offer structured courses on technicals and derivatives. [pause] "
  "And to follow seasoned market voices on X, formerly Twitter, watch fund managers like Samir Arora of Helios, Saurabh Mukherjea of Marcellus, Nilesh Shah of Kotak, and Deepak Shenoy of Capitalmind — for their thinking on the market, not stock tips. [pause] "
  "Learn from these; verify everything; and remember that the numbers of subscribers matter far less than whether a creator shows their reasoning."),
 ("d4_pickchannel", "sm_myths",
  {"kicker": "SPOT THE TIP-SELLER", "title": "Trustworthy source vs tip-seller", "mythLabel": "✗ AVOID", "factLabel": "✓ TRUST",
   "pairs": [
    {"m": "Gives specific 'buy this now' calls & targets", "f": "Explains the reasoning so you can decide yourself"},
    {"m": "Only posts in bull markets; sells courses on hype", "f": "Posts steadily through bull AND bear phases"},
    {"m": "Hides credentials & sources; 'guaranteed' returns", "f": "Shows credentials, cites sources, no guarantees"},
   ]},
  "This is the most important filter of all — how to tell a real teacher from a tip-seller. Three tests. [pause] "
  "First, avoid anyone whose main product is specific buy-this-now calls with price targets. Trust the ones who explain the reasoning behind an idea, so you can judge it yourself. A tip makes you dependent; a method makes you independent. [pause] "
  "Second, avoid creators who only appear in roaring bull markets and vanish when it turns, or who exist mainly to sell you an expensive course on hype. Trust those who post steadily through bull and bear phases alike. [pause] "
  "Third, avoid anyone who hides their credentials and sources or promises guaranteed returns — there is no such thing. Trust those who show who they are, cite where their facts come from, and are honest that nothing is guaranteed. [pause] "
  "Apply these three tests, and ninety percent of the noise falls away."),
 ("d4_recap", "sm_recap",
  {"title": "Chapter 4 — tools & sources",
   "items": [
    "Technicals help WHEN; fundamentals decide WHAT",
    "Trend, support/resistance, volume, moving averages",
    "Tools: Screener, Tickertape, Trendlyne, annual reports",
    "Learn from Varsity, Rachana Ranade, Kamra; follow fund managers",
    "Trust methods, not tips — verify everything",
   ],
   "closer": "Learn from teachers; never trade on tips."},
  "Chapter four, in brief. [pause] "
  "Technicals help with when to act; fundamentals decide what to own. Know trend, support and resistance, volume, and moving averages. [pause] "
  "Do the work in free tools — Screener, Tickertape, Trendlyne — but treasure the primary sources, the annual reports and concalls. [pause] "
  "Learn from trustworthy channels like Zerodha Varsity, CA Rachana Ranade, and Pranjal Kamra, and follow seasoned fund managers for their thinking. [pause] "
  "Above all, trust methods over tips, and verify everything. [pause] "
  "Now we put research to work — the equity investment strategies."),
 ],

 # =================== CHAPTER 5 — EQUITY STRATEGIES ===================
 "eq05": [
 ("e5_div", "sm_divider", {"n": 5, "title": "Equity Strategies", "sub": "Value · growth · momentum · SIP · more", "color": G},
  "Chapter five — the equity investment strategies. [pause] "
  "There is no single best strategy — only the one that fits your temperament, your goals, and your time. "
  "Let's walk through every major approach: what it is, its risk, and who it suits."),
 ("e5_longterm", "sm_iconcards",
  {"kicker": "THE FOUNDATION", "title": "Long-term wealth strategies", "color": G,
   "items": [
    {"emoji": "🌳", "k": "Buy & Hold", "v": "Own quality for years; let compounding work. Time in market beats timing", "chip": "Beginner"},
    {"emoji": "🔄", "k": "SIP / Averaging", "v": "Invest a fixed sum monthly; rupee-cost averaging removes timing stress", "chip": "Discipline"},
    {"emoji": "🧱", "k": "Core-Satellite", "v": "70–80% low-cost index core + 20–30% satellite bets", "chip": "Framework"},
    {"emoji": "📉", "k": "Index / Passive", "v": "Own the whole market cheaply; most active funds don't beat it", "chip": "Simple"},
   ]},
  "Let's begin with the foundation — the long-term strategies that build most real wealth. [pause] "
  "The first is buy and hold. Own quality businesses for years, even decades, and let compounding do the heavy lifting. As the saying goes, time in the market beats timing the market. This is the beginner's — and often the master's — strategy. [pause] "
  "The second is the systematic investment plan, the SIP. Invest a fixed sum every month, automatically. Because you buy more units when prices are low and fewer when high, your average cost stays reasonable — that's rupee-cost averaging, and it removes the stress of timing. [pause] "
  "The third is core-satellite, a framework. Keep seventy to eighty percent of your money in a low-cost index core for stability, and use the remaining twenty to thirty percent for satellite bets — a sector, a factor, a conviction stock. [pause] "
  "The fourth is pure passive investing — simply owning the whole market cheaply through an index fund. Over the long run, most active funds fail to beat it. Simple, and powerful."),
 ("e5_styles", "sm_compare3",
  {"kicker": "STOCK-PICKING STYLES", "title": "Value · Growth · Quality",
   "cols": [
    {"name": "Value", "color": G, "emoji": "🏷️", "hi": True, "rows": [
     {"k": "Idea", "v": "buy below intrinsic value"},
     {"k": "Look for", "v": "low P/E, P/B, margin of safety"},
     {"k": "Icons", "v": "Graham, Buffett"},
     {"k": "Risk", "v": "value traps"}]},
    {"name": "Growth", "color": C, "emoji": "🚀", "rows": [
     {"k": "Idea", "v": "buy fast-growing earnings"},
     {"k": "Look for", "v": "high growth, big runway"},
     {"k": "Pay", "v": "higher P/E accepted"},
     {"k": "Risk", "v": "overpaying, de-rating"}]},
    {"name": "Quality / GARP", "color": V, "emoji": "💎", "rows": [
     {"k": "Idea", "v": "great business, fair price"},
     {"k": "Look for", "v": "high ROE, moat; PEG < 1"},
     {"k": "Icons", "v": "Marcellus style"},
     {"k": "Risk", "v": "crowded, pricey"}]},
   ]},
  "Now the stock-picking styles — three great schools. [pause] "
  "The first is value investing. The idea, from Benjamin Graham and Warren Buffett, is to buy a rupee of value for fifty paise — to find companies trading below their intrinsic worth. You look for low price-to-earnings and price-to-book, and you demand a margin of safety. The risk is the value trap — cheap for a good reason. [pause] "
  "The second is growth investing. Here you buy companies whose earnings are growing fast, with a long runway ahead, and you accept a higher price-to-earnings for that growth. The risk is overpaying — if growth slows, the stock can de-rate sharply. [pause] "
  "The third blends the two — quality, or growth at a reasonable price. Buy a wonderful business — high return on equity, a real moat — but only at a fair price. A useful gauge is the PEG ratio: growth-adjusted P E below one is attractive. This is the Marcellus, Saurabh Mukherjea school. The risk is that quality gets crowded and expensive. [pause] "
  "None is right or wrong. They fit different temperaments."),
 ("e5_active", "sm_iconcards",
  {"kicker": "MORE APPROACHES", "title": "Momentum, dividend, contrarian, rotation", "color": V,
   "items": [
    {"emoji": "🚀", "k": "Momentum / Factor", "v": "Buy recent strength (Nifty 200 Momentum 30); rebalances; prone to sharp 'crashes'", "chip": "Aggressive"},
    {"emoji": "💵", "k": "Dividend / Income", "v": "Own steady payers for regular income; suits retirees", "chip": "Income"},
    {"emoji": "🎣", "k": "Contrarian", "v": "Buy fear, sell greed — go against the crowd at extremes", "chip": "Bold"},
    {"emoji": "🔃", "k": "Sector Rotation", "v": "Rotate into the sector the macro cycle favours", "chip": "Cyclical"},
   ]},
  "Beyond the core styles, four more approaches worth knowing. [pause] "
  "First, momentum, or factor investing. Buy what has recently been strong, on the evidence that strength tends to persist a while. You can do this simply through a Nifty 200 Momentum 30 index fund, which rebalances every six months. The warning: momentum is aggressive and prone to sudden, sharp reversals called momentum crashes. Keep it as a small satellite. [pause] "
  "Second, dividend or income investing. Own steady, cash-generating companies for the regular dividends they pay. This suits retirees and anyone wanting income rather than only capital growth. [pause] "
  "Third, contrarian investing — the boldest. Buy when others are fearful, sell when they are greedy. It means going against the crowd precisely at the extremes, which is psychologically very hard, and very rewarding when right. [pause] "
  "Fourth, sector rotation — the strategy from chapter two: keep rotating your weight toward the sector the macro cycle currently favours. [pause] "
  "Different tools for different investors — and different market weathers."),
 ("e5_which", "sm_checklist",
  {"kicker": "CHOOSING YOURS", "title": "Which strategy is for you?", "color": G, "icon": "🧭",
   "items": [
    "Beginner / busy: index SIP + buy & hold quality",
    "Patient bargain-hunter: value investing",
    "Believe in a growth story: growth or GARP",
    "Want income: dividend investing",
    "Whatever you pick — position size, diversify, stay the course",
   ]},
  "So which strategy is for you? A simple guide. [pause] "
  "If you are a beginner, or simply busy with life, the honest best answer is an index SIP plus buying and holding a few quality companies. It wins more often than clever trading, with far less effort. [pause] "
  "If you are patient and enjoy hunting for bargains, value investing will suit you. [pause] "
  "If you can identify and stomach a long growth story, growth or growth-at-a-reasonable-price is your path. [pause] "
  "If you need regular income, tilt toward dividend investors. [pause] "
  "But whatever you choose, the same discipline applies to all: size your positions sensibly, diversify across sectors, and stay the course through the ups and downs. The strategy matters less than the discipline to follow it. [pause] "
  "Now we cross into the world of derivatives — futures."),
 ("e5_recap", "sm_recap",
  {"title": "Chapter 5 — equity strategies",
   "items": [
    "Foundation: buy & hold, SIP, core-satellite, index",
    "Styles: value, growth, quality/GARP (PEG<1)",
    "Also: momentum, dividend, contrarian, sector rotation",
    "No single best — fit it to your temperament & goals",
    "Discipline beats the choice of strategy",
   ],
   "closer": "The best strategy is the one you can stick to."},
  "Chapter five, gathered up. [pause] "
  "The foundation strategies build wealth quietly: buy and hold, the SIP, core-satellite, and plain index investing. [pause] "
  "The picking styles are value, growth, and quality or growth-at-a-reasonable-price. [pause] "
  "And the active approaches — momentum, dividend, contrarian, and sector rotation — each suit a different temperament and market. [pause] "
  "There is no single best strategy; there is only the one that fits you, executed with discipline. [pause] "
  "Next, we enter the high-octane world of derivatives, starting with futures."),
 ],

 # =================== CHAPTER 6 — FUTURES ===================
 "eq06": [
 ("f6_div", "sm_divider", {"n": 6, "title": "Futures", "sub": "Contracts · leverage · strategies", "color": V},
  "Chapter six — futures. [pause] "
  "We now leave investing and enter trading — the world of derivatives. These are powerful, professional tools. "
  "They can protect a portfolio or destroy an account. Let's understand them clearly, and respect them."),
 ("f6_what", "sm_steps",
  {"kicker": "THE ORIGIN", "title": "A future = a price locked in advance", "color": M,
   "note": "A derivative: its value derives from an underlying — a stock, an index, or a commodity.",
   "items": [
    {"emoji": "👨‍🌾", "label": "Farmer's fear", "sub": "price may fall by harvest"},
    {"emoji": "🏭", "label": "Miller's fear", "sub": "price may rise by then"},
    {"emoji": "🤝", "label": "Lock a deal", "sub": "fixed price, future date"},
    {"emoji": "🔒", "label": "Both protected", "sub": "this is a futures contract"},
   ]},
  "To understand a future, picture a farmer and a flour mill. [pause] "
  "The farmer's crop is three months away. His fear: prices might crash by harvest. [pause] "
  "The mill owner needs that grain in three months. His fear: prices might spike. [pause] "
  "So today, they agree a deal — a fixed price, for delivery in three months. Now both are protected, whichever way prices move. [pause] "
  "That agreement, to buy or sell something later at a price fixed today, is a futures contract. On the stock market, the underlying is a stock, an index like the Nifty, or a commodity — and the value of the future derives from that underlying. That is why we call it a derivative. [pause] "
  "The farmer's motive here is protection — hedging. Hold onto that word; it is the honest purpose of all derivatives."),
 ("f6_mechanics", "sm_iconcards",
  {"kicker": "FUTURES 101", "title": "Four things that define a future", "color": V,
   "items": [
    {"emoji": "📦", "k": "Lot size", "v": "Trade in fixed lots, not single shares. Nifty lot = 65 (from Jan 2026)", "chip": "Lots"},
    {"emoji": "💰", "k": "Margin", "v": "Pay only ~10–15% of contract value upfront — that's the leverage", "chip": "~10–15%"},
    {"emoji": "📅", "k": "Expiry", "v": "Every contract expires. Nifty weekly = Tuesday; monthly = last Tuesday", "chip": "Expiry"},
    {"emoji": "🔄", "k": "Mark-to-market", "v": "Profit/loss settled to your account DAILY; a loss can trigger a margin call", "chip": "Daily"},
   ]},
  "Four features define a stock or index future. [pause] "
  "First, lot size. You don't trade single shares; you trade fixed bundles called lots. The Nifty futures lot, for example, is sixty-five units as of January twenty twenty-six — so one lot is worth several lakh rupees. [pause] "
  "Second, margin. You don't pay the full contract value. You pay a deposit, roughly ten to fifteen percent, and control the whole position. That is leverage — and we'll see its danger in a moment. [pause] "
  "Third, expiry. Unlike a share you can hold forever, every future has a last day. Nifty's weekly contracts expire on Tuesday; the monthly on the last Tuesday. The Sensex expires Thursday. [pause] "
  "Fourth, and crucial — mark-to-market. Your profit or loss is not settled at the end; it is calculated and settled to your account every single day. If the market moves against you and your margin runs low, the broker issues a margin call — pay up, or your position is closed. [pause] "
  "That daily settlement means futures give you no room to simply sit and wait out a bad move."),
 ("f6_leverage", "eq_leverage",
  {"kicker": "FUTURES P&L", "title": "Leverage — the real maths", "margin": 150000, "exposure": 1500000, "movePct": 5, "cur": "₹"},
  "Let's see leverage with real numbers, because this is where fortunes are made and lost. [pause] "
  "Suppose one index futures lot is worth fifteen lakh rupees. Your margin to hold it is about one and a half lakh — so you control ten times your money. Ten-x leverage. [pause] "
  "Now, if the market rises five percent, your position gains seventy-five thousand rupees. On your one-and-a-half-lakh margin, that's a fifty percent return. Intoxicating. [pause] "
  "But flip it. If the market falls five percent, you lose seventy-five thousand — half your margin, gone, on a mere five percent move. [pause] "
  "Leverage multiplies your gains and your losses by the very same factor. It does not care which. And because of daily mark-to-market, those losses are very real, very fast. [pause] "
  "This is why trading futures without a stop-loss is like racing without brakes."),
 ("f6_strategies", "sm_iconcards",
  {"kicker": "FUTURES STRATEGIES", "title": "How futures are actually used", "color": V,
   "items": [
    {"emoji": "🛡️", "k": "Hedging", "v": "Own a portfolio? Short index futures to protect it in a fall — insurance", "chip": "Protect"},
    {"emoji": "🎯", "k": "Directional", "v": "Long if bullish, short if bearish — leveraged bet; highest risk", "chip": "Risky"},
    {"emoji": "📆", "k": "Calendar spread", "v": "Long one expiry, short another — trade the price gap between months", "chip": "Spread"},
    {"emoji": "⚖️", "k": "Cash-futures arbitrage", "v": "Exploit spot vs futures price gap — low-risk, mostly institutional", "chip": "Arb"},
   ]},
  "So how are futures actually used? Four strategies, from safest to riskiest. [pause] "
  "The first, and the honest one, is hedging. If you hold a large portfolio and fear a short-term fall, you can short index futures. If the market drops, your futures profit offsets your portfolio loss. It is portfolio insurance — the reason futures exist. [pause] "
  "The second is directional trading — going long if you're bullish, short if bearish, with leverage. This is the highest-risk use, and where most retail traders lose. [pause] "
  "The third is a calendar spread — buying one expiry and selling another, to trade the price difference between months rather than the market's direction. Lower risk, more advanced. [pause] "
  "The fourth is cash-futures arbitrage — capturing the small gap between a stock's price in the cash market and its futures price. It's low-risk but tiny per trade, so it's dominated by institutional algorithms. [pause] "
  "Remember the three players: hedgers reduce risk, speculators take it on, and arbitrageurs exploit gaps. Retail should aspire to hedge, not gamble."),
 ("f6_recap", "sm_recap",
  {"title": "Chapter 6 — futures",
   "items": [
    "A future = buy/sell later at a price fixed today (a derivative)",
    "Traded in lots; ~10–15% margin → ~10x leverage",
    "Daily mark-to-market + expiry — no room to just wait",
    "Leverage cuts both ways — always use a stop-loss",
    "Real purpose: hedging. Speculation is where most lose",
   ],
   "closer": "Futures are power tools — for hedging first, not gambling."},
  "Chapter six, secured. [pause] "
  "A future is a contract to buy or sell later at a price fixed today — a derivative of an underlying. [pause] "
  "You trade it in lots, paying only ten to fifteen percent margin, which gives you roughly ten-times leverage. [pause] "
  "Daily mark-to-market and a fixed expiry mean you cannot simply wait out a bad move — and leverage cuts both ways, so a stop-loss is non-negotiable. [pause] "
  "The honest purpose of futures is hedging; speculation is where most retail traders lose. [pause] "
  "Next, the most fascinating instrument of all — options."),
 ],

 # =================== CHAPTER 7 — OPTIONS BASICS ===================
 "eq07": [
 ("g7_div", "sm_divider", {"n": 7, "title": "Options — The Basics", "sub": "Calls · puts · premium · payoff", "color": V},
  "Chapter seven — options, the basics. [pause] "
  "Options are the most flexible instrument in all of finance, and the most misunderstood. "
  "Master the foundation here, and the strategies in the next chapter will click into place."),
 ("g7_insurance", "sm_steps",
  {"kicker": "THE ANALOGY", "title": "An option is like insurance", "color": C,
   "note": "Premium payer gets a RIGHT; premium taker takes on an OBLIGATION.",
   "items": [
    {"emoji": "🚗", "label": "Car insurance", "sub": "pay a yearly premium"},
    {"emoji": "💥", "label": "If accident", "sub": "insurer pays big"},
    {"emoji": "😊", "label": "If nothing", "sub": "premium is gone — that's all"},
    {"emoji": "📜", "label": "This is an option", "sub": "small premium, big right"},
   ]},
  "To truly get options, think of your car insurance. [pause] "
  "You pay a small premium each year. [pause] "
  "If you have an accident, the insurer pays out a large sum. [pause] "
  "If nothing happens, your premium is simply gone — and that is your entire loss. Small, known, capped. [pause] "
  "An option works exactly like this. You pay a small premium to buy a right — the right to buy or sell an asset at a set price. If it works in your favour, you exercise it for a big gain. If not, you let it lapse, losing only the premium. [pause] "
  "And here is the key symmetry: the person who pays the premium gets the right; the person who receives the premium takes on the obligation — like the insurance company. Buyer has rights; seller has duties. Hold that thought."),
 ("g7_callput", "sm_iconcards",
  {"kicker": "CALL & PUT", "title": "Just two building blocks", "color": V,
   "items": [
    {"emoji": "📈", "k": "Call option", "v": "The RIGHT to BUY at the strike. Buy a call if you expect the price to RISE", "chip": "Bullish"},
    {"emoji": "📉", "k": "Put option", "v": "The RIGHT to SELL at the strike. Buy a put if you expect the price to FALL", "chip": "Bearish"},
    {"emoji": "🎯", "k": "Strike price", "v": "The fixed price at which you may buy (call) or sell (put)", "chip": "Strike"},
    {"emoji": "⏳", "k": "Expiry & premium", "v": "The last valid day; the premium is the price of the right", "chip": "Expiry"},
   ]},
  "Everything in options is built from just two blocks: the call and the put. [pause] "
  "A call option is the right to buy at a fixed price. You buy a call when you expect the price to rise. If it soars, you can still buy cheaply at your strike and profit. [pause] "
  "A put option is the right to sell at a fixed price. You buy a put when you expect the price to fall — or to protect shares you already own, like insurance on your holdings. [pause] "
  "That fixed price — the price at which you may buy or sell — is called the strike price. [pause] "
  "And two more terms: expiry, the last day the option is valid, and the premium, the price you pay for the right itself. [pause] "
  "Just remember: call is the right to buy, put is the right to sell. From these two atoms, every options strategy is built."),
 ("g7_value", "sm_iconcards",
  {"kicker": "WHAT DRIVES PREMIUM", "title": "Intrinsic value + time value", "color": M,
   "items": [
    {"emoji": "💠", "k": "Intrinsic value", "v": "Real value now. Call = spot − strike (if positive); put = strike − spot", "chip": "Now"},
    {"emoji": "⏳", "k": "Time value", "v": "Extra paid for the hope the option moves your way before expiry", "chip": "Hope"},
    {"emoji": "🎯", "k": "ITM / ATM / OTM", "v": "In / at / out of the money — is the strike favourable vs the spot?", "chip": "Moneyness"},
    {"emoji": "📉", "k": "Decay", "v": "Time value melts as expiry nears — fast in the final days", "chip": "Melts"},
   ]},
  "Why does a premium cost what it costs? It has two parts. [pause] "
  "The first is intrinsic value — the option's real, exercise-it-right-now worth. For a call, that's the spot price minus the strike, if positive. For a put, the strike minus the spot. If the option isn't yet profitable to exercise, its intrinsic value is zero. [pause] "
  "The second is time value — the extra you pay for the hope that the option moves your way before it expires. The more time left, and the more the stock swings, the higher this hope premium. [pause] "
  "This gives us three words you'll hear constantly: in-the-money, at-the-money, and out-of-the-money — simply whether the strike is favourable, level with, or unfavourable versus the current price. [pause] "
  "And the crucial fact: time value melts away as expiry approaches, faster and faster in the final days. That melting is the single most important force in options — and it's the subject of the next chapter."),
 ("g7_payoffs", "eq_payoff",
  {"kind": "call", "side": "buy", "strike": 100, "premium": 5, "cur": "$",
   "note": "Long call: loss capped at the premium ($5); profit is unlimited above break-even."},
  "Let's make this visual with a payoff diagram — the picture of profit and loss at expiry. [pause] "
  "Here is a long call. Say the stock is at one hundred, and you buy the hundred-strike call for a premium of five. [pause] "
  "Look at the left side. If the stock falls, you simply let the option lapse. Your loss is flat — capped at the five you paid, no matter how far it drops. [pause] "
  "Now the right side. Above one hundred and five — your strike plus your premium, the break-even — every further rupee is profit, and there is no ceiling. [pause] "
  "That is the buyer's dream shape: limited, known loss; large, open-ended gain. [pause] "
  "It sounds like free money. So why do most option buyers lose? Because of that melting time value. Let's confront it head-on."),
 ("g7_recap", "sm_recap",
  {"title": "Chapter 7 — options basics",
   "items": [
    "Option = the RIGHT (not obligation) — like insurance",
    "Call = right to buy; Put = right to sell",
    "Strike, expiry, premium — the core terms",
    "Premium = intrinsic value + time value",
    "Buyer: limited loss (premium), large upside",
   ],
   "closer": "Two atoms — call and put — build every strategy."},
  "Chapter seven, in one breath. [pause] "
  "An option is the right, not the obligation, to act — just like an insurance policy. [pause] "
  "A call is the right to buy; a put is the right to sell; and strike, expiry, and premium are the core terms. [pause] "
  "The premium is made of intrinsic value plus time value, and time value melts as expiry nears. [pause] "
  "For the buyer, the loss is limited to the premium while the upside is large. [pause] "
  "Now, the deeper mechanics — the Greeks — and the real strategies."),
 ],

 # =================== CHAPTER 8 — OPTIONS: GREEKS & STRATEGIES ===================
 "eq08": [
 ("h8_div", "sm_divider", {"n": 8, "title": "Options Mastery", "sub": "The Greeks · strategies · the hard truth", "color": V},
  "Chapter eight — options mastery. [pause] "
  "Now we go professional: the Greeks that measure risk, the real multi-leg strategies, "
  "and the hard, honest truth about who actually makes money in options. Stay with me."),
 ("h8_greeks", "sm_iconcards",
  {"kicker": "THE GREEKS", "title": "Four letters that measure risk", "color": V,
   "items": [
    {"emoji": "Δ", "k": "Delta", "v": "How much the option moves per 1-point move in the stock (call 0→1, put 0→−1)", "chip": "Direction"},
    {"emoji": "Γ", "k": "Gamma", "v": "How fast delta itself changes — the acceleration", "chip": "Speed"},
    {"emoji": "Θ", "k": "Theta", "v": "Daily time decay — how much value the option loses each day (negative for buyers)", "chip": "Decay"},
    {"emoji": "ν", "k": "Vega", "v": "Sensitivity to a 1% change in volatility — big swings pump premiums up", "chip": "Volatility"},
   ]},
  "Professionals don't just guess; they measure their risk with the Greeks — four letters, each capturing one force. [pause] "
  "Delta measures direction: how much the option's price moves for a one-point move in the stock. A call's delta runs from zero to one; a put's from zero to minus one. [pause] "
  "Gamma measures how fast delta itself changes — the acceleration. High gamma means your risk shifts quickly. [pause] "
  "Theta measures time decay — how much value the option bleeds every single day just from the clock ticking. For the buyer, theta is negative; it is the enemy. [pause] "
  "Vega measures sensitivity to volatility — how much the premium changes when the market's expected swings rise or fall by one percent. When fear spikes, vega pumps premiums up. [pause] "
  "Delta and gamma track the price; theta and vega track time and fear. Together, they are the dashboard of every serious options trader."),
 ("h8_theta", "eq_theta",
  {"kicker": "OPTIONS · TIME DECAY", "title": "Theta — the melting ice cube",
   "note": "The buyer must be right on direction AND speed. The seller just needs time to pass."},
  "Let's dwell on theta, because it decides who wins. [pause] "
  "Picture the time value in an option as a block of ice, sitting in the sun. Every day, a little melts away — and near expiry, it melts fast. [pause] "
  "This is why so many option buyers lose even when they guess the direction right. Suppose you buy a call and the stock does rise — but slowly. The time value can melt faster than the stock rises, and you still lose. The buyer must be right on direction and on speed. [pause] "
  "Now flip the coin. The option seller, who collected that premium, watches the ice melt in their favour. Time is their ally. They just need the passage of days. [pause] "
  "This is the deep truth of options: time is on the seller's side. It's why most options expire worthless, and why disciplined sellers — with deep pockets and strict risk control — win more often than buyers. But the seller's loss can be huge, so they must manage risk ruthlessly."),
 ("h8_income", "sm_iconcards",
  {"kicker": "STRATEGIES · INCOME & HEDGE", "title": "The first real strategies", "color": G,
   "items": [
    {"emoji": "🏠", "k": "Covered Call", "v": "Own the stock + sell a call. Earn premium income; caps your upside", "chip": "Income"},
    {"emoji": "🛡️", "k": "Protective Put", "v": "Own the stock + buy a put. Insurance against a crash", "chip": "Insurance"},
    {"emoji": "💰", "k": "Cash-Secured Put", "v": "Sell a put to get paid while waiting to buy a stock lower", "chip": "Entry"},
    {"emoji": "⚠️", "k": "Naked selling", "v": "Selling options without cover = large/unlimited risk. Not for beginners", "chip": "Danger"},
   ]},
  "Now the real strategies — starting with the sensible, income-and-hedge trio that pairs options with stock you own. [pause] "
  "The covered call: you own a stock, and you sell a call against it. You pocket the premium as income. The trade-off — if the stock rockets past the strike, your gains are capped. Great in a flat or mildly rising market. [pause] "
  "The protective put: you own a stock and you buy a put on it. This is pure insurance — if the stock crashes, the put pays off and limits your loss. You pay a premium for peace of mind. [pause] "
  "The cash-secured put: you sell a put on a stock you'd happily buy anyway, at a lower price. You get paid the premium while you wait; if it falls to your strike, you buy it — effectively at a discount. [pause] "
  "And a warning: selling options naked, without owning the stock or a hedge, exposes you to large or even unlimited losses. That is strictly for well-capitalized professionals — never a beginner's game."),
 ("h8_spreads", "sm_iconcards",
  {"kicker": "STRATEGIES · SPREADS & VOLATILITY", "title": "Defined-risk & volatility plays", "color": C,
   "items": [
    {"emoji": "🐂", "k": "Bull Call / Bear Put Spread", "v": "Buy one option, sell another — cheaper, with capped risk AND reward", "chip": "Directional"},
    {"emoji": "🎗️", "k": "Long Straddle", "v": "Buy a call AND a put at the same strike — profit from a big move either way", "chip": "Big move"},
    {"emoji": "🎯", "k": "Strangle", "v": "Like a straddle but cheaper, wider strikes — needs an even bigger move", "chip": "Cheaper"},
    {"emoji": "🦅", "k": "Iron Condor", "v": "Sell an OTM call spread + put spread — profit if the market stays in a range", "chip": "Range"},
   ]},
  "Beyond single legs come the combination strategies — where options truly shine. [pause] "
  "First, spreads. In a bull call spread you buy one call and sell a higher one; the sale cuts your cost, in exchange for a cap on your reward. Both your risk and your reward are defined and limited. The bear put spread is its mirror for a fall. These are the disciplined trader's bread and butter. [pause] "
  "Next, volatility strategies, for when you expect a big move but aren't sure which way. A long straddle buys both a call and a put at the same strike — you profit if the stock moves sharply in either direction, say around a big result. A strangle is the cheaper version, using wider strikes, but it needs an even bigger move to pay off. [pause] "
  "And for the opposite view — that the market will stay calm and range-bound — the iron condor sells an out-of-the-money call spread and put spread, collecting premium that you keep if the market goes nowhere. [pause] "
  "Each has a precise payoff shape and a precise use. This is the craft of options."),
 ("h8_truth", "sm_lossgrid",
  {"kicker": "SEBI STUDY · FY25", "title": "The hard truth about F&O", "lossPct": 91,
   "mainLabel": "Individuals who lost", "statLabel": "Total net loss (FY25)", "statTo": 1.06, "statDecimals": 2,
   "statPrefix": "₹", "statSuffix": "L cr", "sourcePrefix": "Source: ", "source": "SEBI study, Jul 2025",
   "note": "9 in 10 lose money. Options are for the educated, well-capitalized and disciplined — not beginners."},
  "Before you touch any of this, the hard truth — the number every options course should be forced to show. [pause] "
  "SEBI, the regulator, studied real trading accounts. In the financial year twenty twenty-five, ninety-one percent of individual futures and options traders lost money. [pause] "
  "Ninety-one out of every hundred. [pause] "
  "Their combined net loss in a single year was over one lakh crore rupees — around one lakh ten thousand rupees each, on average. And an earlier study found seventy-one percent of intraday equity traders also lost. [pause] "
  "This is not to scare you; it is to arm you with reality before the excitement does. Options are a professional instrument — for the educated, the well-capitalized, and the ruthlessly disciplined. [pause] "
  "My honest guidance: master investing first. Come to options later, in tiny size, only after real study — and never with money you cannot afford to lose."),
 ("h8_recap", "sm_recap",
  {"title": "Chapter 8 — options mastery",
   "items": [
    "Greeks: delta (direction), gamma (speed), theta (decay), vega (volatility)",
    "Time decay favours the seller — buyers need direction AND speed",
    "Income/hedge: covered call, protective put, cash-secured put",
    "Combinations: spreads, straddle/strangle, iron condor",
    "SEBI: 91% of F&O traders lose — respect the risk",
   ],
   "closer": "Options reward the disciplined and punish the reckless."},
  "Chapter eight, the big one, gathered up. [pause] "
  "The Greeks measure your risk: delta for direction, gamma for speed, theta for time decay, vega for volatility. [pause] "
  "Time decay favours the seller — the buyer must be right on both direction and speed. [pause] "
  "The sensible strategies pair options with stock: covered calls, protective puts, cash-secured puts; and the combinations — spreads, straddles, strangles, and iron condors — each fit a precise view. [pause] "
  "But never forget the ninety-one percent. Options reward the disciplined and punish the reckless. [pause] "
  "Next, a different market entirely — commodities."),
 ],

 # =================== CHAPTER 9 — COMMODITIES ===================
 "eq09": [
 ("i9_div", "sm_divider", {"n": 9, "title": "Commodities", "sub": "Gold · silver · crude on the MCX", "color": M},
  "Chapter nine — commodities. [pause] "
  "Beyond stocks lies a parallel market — real, physical things: gold, silver, crude oil, metals. "
  "In India these trade on the MCX. Let's learn how, and why gold in particular belongs in a portfolio."),
 ("i9_what", "sm_iconcards",
  {"kicker": "THE MCX", "title": "What are commodities?", "color": M,
   "items": [
    {"emoji": "🥇", "k": "Bullion", "v": "Gold and silver — safe-haven assets, wealth stores", "chip": "Metals"},
    {"emoji": "🛢️", "k": "Energy", "v": "Crude oil and natural gas — driven by OPEC & geopolitics", "chip": "Energy"},
    {"emoji": "🔩", "k": "Base metals", "v": "Copper, zinc, aluminium — track global growth & China", "chip": "Industrial"},
    {"emoji": "🏛️", "k": "The MCX", "v": "India's main commodity exchange, SEBI-regulated; open ~9 AM to ~11:55 PM", "chip": "Exchange"},
   ]},
  "So, what are commodities? Raw, physical goods, grouped into families. [pause] "
  "First, bullion — gold and silver. These are safe-haven assets, stores of wealth that people flee to in uncertain times. [pause] "
  "Second, energy — crude oil and natural gas, driven by OPEC decisions, demand, and geopolitics. [pause] "
  "Third, base metals — copper, zinc, aluminium — the industrial metals that rise and fall with global growth and, especially, China. [pause] "
  "In India, these trade on the MCX, the Multi Commodity Exchange — the largest, and, like the stock market, regulated by SEBI. One big difference: because commodities track global markets, the MCX stays open far longer — from about nine in the morning until nearly midnight, around eleven fifty-five p m, so it can react to overnight news from around the world. [pause] "
  "That long window, plus leverage, makes commodities a fast, demanding market."),
 ("i9_how", "sm_iconcards",
  {"kicker": "HOW THEY TRADE", "title": "Traded through futures — with leverage", "color": V,
   "items": [
    {"emoji": "📜", "k": "Via futures", "v": "You trade commodity futures contracts, not the physical metal", "chip": "Futures"},
    {"emoji": "📦", "k": "Lot sizes", "v": "Standardised — e.g. Gold 1kg (main) and a Gold Mini (100g) for smaller size", "chip": "Lots"},
    {"emoji": "💰", "k": "Small margin", "v": "Pay a fraction of value — same double-edged leverage as stock futures", "chip": "Leverage"},
    {"emoji": "🌍", "k": "Global drivers", "v": "USD, real interest rates, geopolitics, OPEC — plus India's festival gold demand", "chip": "Macro"},
   ]},
  "How do you actually trade a commodity? Almost always through futures — you trade a contract, not a vault of gold. [pause] "
  "The contracts come in standardised lot sizes. Gold, for instance, has a main one-kilogram contract, and a smaller Gold Mini of one hundred grams so ordinary traders can take part. [pause] "
  "As with stock futures, you pay only a small margin — a fraction of the contract's value — which means the same double-edged leverage. A small favourable move is magnified; so is an unfavourable one. [pause] "
  "And what moves commodity prices? Global forces. Gold and silver respond to the US dollar, to real interest rates, and to geopolitical fear — plus, in India, the huge festival and wedding demand. Crude follows OPEC and the world economy. Base metals follow global growth. [pause] "
  "This is a macro trader's arena — you're really trading world events."),
 ("i9_gold", "sm_iconcards",
  {"kicker": "GOLD IN A PORTFOLIO", "title": "You don't have to trade the leverage", "color": M,
   "items": [
    {"emoji": "🥇", "k": "Gold ETF", "v": "Own gold in your demat — no leverage, no storage, easy to sell", "chip": "ETF"},
    {"emoji": "🧾", "k": "Sovereign Gold Bond", "v": "Government gold that also pays interest — a non-leveraged way to hold", "chip": "SGB"},
    {"emoji": "🛡️", "k": "The hedge role", "v": "Gold often rises when equities fall — low correlation = a cushion", "chip": "Cushion"},
    {"emoji": "⚖️", "k": "How much", "v": "Around 5–10% of a portfolio, as ballast — not the main engine", "chip": "5–10%"},
   ]},
  "Here is the most useful commodity idea for a normal investor: you do not have to touch the leverage at all. [pause] "
  "You can own gold simply, without a futures contract. A gold ETF holds gold in your demat account — no storage, no leverage, sell it in one click. A Sovereign Gold Bond is government-issued gold that even pays you a small interest on top. Both are calm, non-leveraged ways to own gold. [pause] "
  "Why own gold at all? Because of its role as a hedge. Gold often rises exactly when equities fall — they have low correlation. So a slice of gold cushions your portfolio in a crash. [pause] "
  "How much? Around five to ten percent of your portfolio, as ballast — a stabiliser, not the main engine of growth. [pause] "
  "For traders, commodities offer trend-following, hedging, and spread strategies like the gold-silver ratio. But for the everyday investor, gold's real job is quiet insurance."),
 ("i9_recap", "sm_recap",
  {"title": "Chapter 9 — commodities",
   "items": [
    "Bullion, energy, base metals — trade on the MCX",
    "Traded via futures, with the same leverage risk",
    "Driven by global macro: USD, rates, OPEC, geopolitics",
    "Gold ETF / SGB = own gold without leverage",
    "Keep ~5–10% gold as a portfolio hedge",
   ],
   "closer": "For most investors, gold is insurance — not a bet."},
  "Chapter nine, in brief. [pause] "
  "Commodities — bullion, energy, and base metals — trade on the MCX, mostly through leveraged futures. [pause] "
  "Their prices are driven by global macro forces: the dollar, interest rates, OPEC, and geopolitics. [pause] "
  "But you don't need the leverage — a gold ETF or a Sovereign Gold Bond lets you own gold calmly. [pause] "
  "And gold's real value to a portfolio is as a hedge — keep around five to ten percent as insurance, not as a bet. [pause] "
  "Finally, the thread that ties everything together — risk management."),
 ],

 # =================== CHAPTER 10 — RISK & PUTTING IT TOGETHER ===================
 "eq10": [
 ("j10_div", "sm_divider", {"n": 10, "title": "Risk & The Whole Picture", "sub": "Survival · fit · the master recap", "color": G},
  "Chapter ten, the final chapter — risk management, and putting the whole course together. [pause] "
  "Everything we've learned means nothing without this. The first job of an investor is not to make money — it is to not go broke. Survival first."),
 ("j10_rules", "sm_checklist",
  {"kicker": "THE SURVIVAL RULES", "title": "Risk management — the rules that keep you in the game", "color": G, "icon": "🛡️",
   "items": [
    "Risk only 1–2% of capital on any single trade",
    "Always use a stop-loss on leveraged or active positions",
    "Diversify across sectors AND asset classes",
    "Never mix investing capital with trading capital",
    "Never borrow / use MTF leverage to chase returns",
   ]},
  "Here are the survival rules — the discipline the ninety-one percent ignored. [pause] "
  "One — risk only one to two percent of your total capital on any single trade. Then even ten losses in a row cannot ruin you. This one rule separates survivors from casualties. [pause] "
  "Two — always use a stop-loss on any leveraged or active position. Decide, before you enter, where you are wrong and will exit. No exceptions, especially in futures and options. [pause] "
  "Three — diversify across sectors and across asset classes. Equities, some debt, a little gold. When one zigs, another zags. [pause] "
  "Four — never mix your investing capital with your trading capital. Keep the long-term wealth pot completely separate from the money you actively trade. [pause] "
  "Five — never borrow money, or use margin-trading leverage, to chase returns. Remember the ninety-one percent — leverage is what turned their losses catastrophic. [pause] "
  "Follow these five, and you will still be standing when opportunity comes."),
 ("j10_fit", "sm_compare3",
  {"kicker": "WHICH IS FOR YOU?", "title": "Match the instrument to yourself",
   "cols": [
    {"name": "Beginner / Investor", "color": G, "emoji": "🌱", "hi": True, "rows": [
     {"k": "Use", "v": "index SIP + quality equity"},
     {"k": "Goal", "v": "long-term wealth"},
     {"k": "Time", "v": "a few hours a month"},
     {"k": "F&O?", "v": "not yet"}]},
    {"name": "Experienced", "color": C, "emoji": "📈", "rows": [
     {"k": "Use", "v": "equity + hedging with futures"},
     {"k": "Goal", "v": "growth + protection"},
     {"k": "Time", "v": "weekly research"},
     {"k": "F&O?", "v": "hedging, small size"}]},
    {"name": "Professional", "color": V, "emoji": "⚡", "rows": [
     {"k": "Use", "v": "options strategies, commodities"},
     {"k": "Goal", "v": "active returns"},
     {"k": "Time", "v": "full-time focus"},
     {"k": "F&O?", "v": "with strict risk rules"}]},
   ]},
  "So which of all these tools is for you? Match the instrument to yourself — honestly. [pause] "
  "If you are a beginner or a long-term investor, your toolkit is simple and powerful: an index SIP plus a few quality stocks, aimed at long-term wealth, needing just a few hours a month. Futures and options? Not yet — you don't need them. [pause] "
  "If you are experienced, you can add hedging — using futures to protect your portfolio — while your core stays invested for growth, with weekly research. Here F&O earns its place, in small size, mainly for protection. [pause] "
  "Only the dedicated, near full-time trader — with a tested method and iron discipline — should run active options strategies and trade commodities. And even then, only with strict risk rules. [pause] "
  "There is no shame in the first column. It quietly builds more wealth for more people than the third ever will."),
 ("j10_master", "sm_recap",
  {"title": "The whole course — in one breath",
   "items": [
    "Sector first: top-down macro → sector → leaders",
    "Research: 3 statements, ratios, moat, fair price",
    "Learn from methods & trusted channels — never tips",
    "Equity strategies: SIP & quality for most; know them all",
    "F&O = powerful tools: hedge first; 91% of speculators lose",
    "Commodities: gold ~5–10% as a hedge; respect leverage",
    "Risk rules keep you in the game — survival first",
   ],
   "closer": "Learn deeply, risk little, compound patiently."},
  "Let's bring the entire course together, in one breath. [pause] "
  "Start with the sector — top-down, from macro to sector to the leaders within it. [pause] "
  "Research properly: the three statements, the key ratios, the moat, and always a fair price with a margin of safety. [pause] "
  "Learn from methods and trustworthy channels — Varsity, honest educators, seasoned fund managers — and never from tips. [pause] "
  "For equity strategy, an index SIP and a few quality names serve most people beautifully, even though you now know them all. [pause] "
  "Futures and options are powerful tools — use them to hedge first, and never forget that ninety-one percent of speculators lose. [pause] "
  "In commodities, let gold be a five-to-ten-percent hedge, and always respect the leverage. [pause] "
  "And binding it all — the risk rules that keep you in the game. Survival first, returns second. [pause] "
  "You now have the complete map. Learn deeply, risk little, and compound patiently. That is how wealth is truly built. This is educational content, not investment advice — do your own research, and consult a SEBI-registered adviser. Thank you for watching."),
 ],
}

# ------------------------------------------------------------------- helpers
def ffdur(path):
    out = subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","default=noprint_wrappers=1:nokey=1",path],capture_output=True,text=True,check=True)
    return round(float(out.stdout.strip()),3)

def tts_chunk(path, text):
    mp3 = path[:-4]+".mp3"
    subprocess.run(["edge-tts","--voice",VOICE,f"--rate={RATE}","--text",text,"--write-media",mp3],check=True,capture_output=True)
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
        if len(pt)>62 and ("," in pt or "—" in pt):
            buf=""
            for s in re.split(r"(?<=[,—])\s+", pt):
                if len(buf)+len(s)>62 and buf: cues.append(buf.strip()); buf=s
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
        print(f"  {sid:12s} {dur:6.2f}s",flush=True)
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
