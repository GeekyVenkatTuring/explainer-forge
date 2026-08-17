#!/usr/bin/env python3
"""Sector Deep-Dives (ENGLISH) — Finance, Defence, Technology.
Each: sector-specific fundamentals + technicals + strategies. Voice en-IN-NeerjaNeural.
Reuses `sm` parameterized scenes with English props. Facts verified 2026-07 via web
search (research/sectors.md). Education only, not advice.
Usage: python3 build.py            (all)  |  python3 build.py fin
"""
import json, os, re, subprocess, sys

VOICE = "en-IN-NeerjaNeural"; RATE = "-4%"; GAP = 0.5; PAUSE = 0.5; PREFIX = "sx"
ROOT = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(ROOT, "..", ".."))
PUBLIC = os.path.join(REPO, "composer", "public", PREFIX); RAW = os.path.join(ROOT, "assets", "raw"); FIN = os.path.join(ROOT, "assets")
for d in (PUBLIC, RAW, os.path.join(ROOT, "artifacts"), os.path.join(ROOT, "renders")):
    os.makedirs(d, exist_ok=True)

G, C, R, M, V = "#34D399", "#22D3EE", "#FB7185", "#FBBF24", "#A78BFA"
DISC = "⚠️ Educational content only — not investment advice. Company names are examples, not recommendations."

CHAPTERS = {
 # ============================== FINANCE / BANKING ==============================
 "fin": [
 ("f_title", "sm_ptitle",
  {"title": "How to Analyse Bank Stocks", "sub": "Finance sector · fundamentals · technicals · strategies", "kicker": "SECTOR DEEP-DIVE · FINANCE"},
  "Welcome to the first of our sector deep-dives — the finance sector, the beating heart of the market. [pause] "
  "Banks and financials are the single heaviest weight in the index — when they move, the whole market moves. [pause] "
  "But you cannot analyse a bank like a normal company. A bank's product is money itself, so it needs its own special metrics. [pause] "
  "In this video: the fundamentals unique to banks, the technicals for the sector, and the strategies that work here. "
  "Company names are only examples, never recommendations."),
 ("f_why", "sm_iconcards",
  {"kicker": "WHY IT MATTERS", "title": "The finance sector — the market's engine", "color": C,
   "items": [
    {"emoji": "🏦", "k": "Heaviest weight", "v": "Banking & financials are ~35–40% of the Nifty — the market's engine", "chip": "Index driver"},
    {"emoji": "🔀", "k": "Many kinds", "v": "Private banks, PSU banks, NBFCs, insurers, AMCs — each analysed a bit differently", "chip": "Sub-sectors"},
    {"emoji": "🏛️", "k": "RBI-driven", "v": "Rate decisions, credit growth and liquidity move this sector first", "chip": "Macro"},
    {"emoji": "💧", "k": "Most liquid", "v": "Bank Nifty is India's most traded derivative — huge participation", "chip": "Bank Nifty"},
   ]},
  "First, why this sector matters so much. [pause] "
  "Banking and financials make up roughly thirty-five to forty percent of the Nifty. When banking leads, the index almost always follows — so it is the single most important sector to watch. [pause] "
  "It is not one thing but many: private banks, public-sector banks, non-bank lenders or NBFCs, insurers, and asset managers — each analysed a little differently. [pause] "
  "It is driven, before anything else, by the RBI — interest-rate decisions, the credit cycle, and liquidity. [pause] "
  "And it is the most liquid corner of the market: Bank Nifty is India's most heavily traded derivative contract. [pause] "
  "So let's learn the metrics that actually tell you whether a bank is healthy."),
 ("f_fund1", "sm_iconcards",
  {"kicker": "FUNDAMENTALS · CORE", "title": "The four numbers that define a bank", "color": G,
   "items": [
    {"emoji": "📊", "k": "NIM", "v": "Net Interest Margin — the spread a bank earns on lending. ~3–4% is healthy", "chip": "Profit"},
    {"emoji": "⚠️", "k": "GNPA / NNPA", "v": "Bad-loan ratio — asset quality. Below 1% is strong; above ~2% is a worry", "chip": "Quality"},
    {"emoji": "🏧", "k": "CASA ratio", "v": "Share of cheap current & savings deposits. Higher = cheaper funding = better margins", "chip": "Funding"},
    {"emoji": "🛡️", "k": "CAR", "v": "Capital Adequacy Ratio — the safety buffer. RBI minimum ~11.5%; strong banks 17–22%+", "chip": "Safety"},
   ]},
  "Here are the four numbers that define a bank's health. Learn these, and you can read any bank. [pause] "
  "The first is Net Interest Margin, the N I M. A bank borrows money as deposits and lends it out; the gap between the two is its core profit. Around three to four percent is healthy for an Indian bank. A rising N I M is a very good sign. [pause] "
  "The second is asset quality — the gross and net non-performing asset ratios, the share of loans that have gone bad. Below one percent is strong; above roughly two percent is a warning. This is where banks quietly die, so watch it closely. [pause] "
  "The third is the CASA ratio — the proportion of cheap current and savings-account deposits. The higher the CASA, the cheaper the bank's money, and the fatter its margins. The best banks run CASA near fifty percent. [pause] "
  "The fourth is the Capital Adequacy Ratio, the CAR — the safety buffer against losses. The RBI insists on around eleven and a half percent; the strongest banks carry seventeen to twenty-two percent or more."),
 ("f_fund2", "sm_compare3",
  {"kicker": "FUNDAMENTALS · MORE", "title": "Two more essentials — and how banks are valued",
   "cols": [
    {"name": "Returns", "color": G, "emoji": "💹", "hi": True, "rows": [
     {"k": "ROA", "v": "profit on assets; >1% good, >1.5% great"},
     {"k": "ROE", "v": "return on shareholder funds"},
     {"k": "Provision cover", "v": "cushion set aside vs bad loans"},
     {"k": "Watch", "v": "steady, high, improving"}]},
    {"name": "Growth", "color": C, "emoji": "📈", "rows": [
     {"k": "Credit growth", "v": "loan-book growth vs system"},
     {"k": "Deposit growth", "v": "funding keeping pace"},
     {"k": "Cost-to-income", "v": "efficiency; lower is better"},
     {"k": "Watch", "v": "growth WITH quality"}]},
    {"name": "Valuation", "color": M, "emoji": "🏷️", "rows": [
     {"k": "Use P/B", "v": "banks valued on Price-to-Book, not P/E"},
     {"k": "Quality premium", "v": "HDFC ~3x book; SBI ~1.5–2x"},
     {"k": "PSU discount", "v": "cheaper for a reason — check quality"},
     {"k": "Watch", "v": "pay up for clean books"}]},
   ]},
  "Beyond the core four, a few more essentials — and the one thing beginners always get wrong: valuation. [pause] "
  "On returns: Return on Assets, or R O A, above one percent is good and above one and a half is excellent. Return on equity and provision coverage — the cushion set aside against bad loans — complete the picture. You want them steady, high, and improving. [pause] "
  "On growth: watch loan-book, or credit, growth against the banking system, that deposits are keeping pace, and the cost-to-income ratio, where lower means a more efficient bank. But growth without asset quality is a trap — chase both together. [pause] "
  "And here is the crucial one — valuation. You do not value a bank on price-to-earnings. You value it on price-to-book — the price versus its net worth. A clean, high-return private bank like HDFC may trade near three times book, while a public-sector bank like SBI trades at one and a half to two. That P S U discount is often deserved — so pay up for clean books, don't just chase the cheapest."),
 ("f_tech", "sm_iconcards",
  {"kicker": "TECHNICAL ANALYSIS", "title": "Reading the sector on the chart", "color": C,
   "items": [
    {"emoji": "📉", "k": "Track Bank Nifty", "v": "The sector index. Its trend leads the broad market — watch its 50 & 200-DMA", "chip": "Index"},
    {"emoji": "💪", "k": "Relative strength", "v": "Is Bank Nifty outperforming the Nifty? Buy the sector that's leading", "chip": "vs Nifty"},
    {"emoji": "🌡️", "k": "Breadth", "v": ">70% of bank stocks green with a positive index = real rotation, not 1–2 names", "chip": "Breadth"},
    {"emoji": "🗓️", "k": "The catalyst", "v": "RBI policy day & quarterly results (NIM, NPA) drive the big moves", "chip": "RBI"},
   ]},
  "Now the technicals — how to read the finance sector on the chart. [pause] "
  "Start with the sector index itself, Bank Nifty. Its trend tends to lead the whole market, so track its fifty-day and two-hundred-day moving averages, its support and resistance. [pause] "
  "Then measure relative strength — is Bank Nifty outperforming the broad Nifty, or lagging it? The rule of sector rotation is simple: lean toward the sector that is leading, not the one that is fading. [pause] "
  "Check breadth. If more than seventy percent of bank stocks are green while the index rises, that's genuine institutional rotation into the sector — not just one or two heavyweights dragging the average up. [pause] "
  "And know your catalysts. For banks, the big moves cluster around RBI policy day and around quarterly results — specifically the N I M and the bad-loan numbers. Mark those dates."),
 ("f_strat", "sm_iconcards",
  {"kicker": "STRATEGIES", "title": "Strategies for the finance sector", "color": G,
   "items": [
    {"emoji": "👑", "k": "Own the leaders", "v": "For long-term, hold the highest-quality private banks — clean books, high ROA", "chip": "Quality"},
    {"emoji": "🔄", "k": "PSU re-rating", "v": "In up-cycles, cheap PSU banks with improving asset quality can re-rate hard", "chip": "Cyclical"},
    {"emoji": "📉", "k": "Play the rate cycle", "v": "Falling rates can lift NBFCs & rate-sensitives; watch RBI direction", "chip": "Macro"},
    {"emoji": "🎯", "k": "Buy on NIM stability", "v": "After a margin-miss fall (like HDFC/Axis), quality can be a patient entry", "chip": "Contrarian"},
   ]},
  "So how do you actually play the finance sector? Four strategies. [pause] "
  "First, for the long term, simply own the leaders — the highest-quality private banks with clean loan books and high returns on assets. Boring, and it compounds beautifully. [pause] "
  "Second, the cyclical play — in an economic up-cycle, cheap public-sector banks whose asset quality is improving can re-rate sharply, closing that discount to private banks. Higher risk, higher reward. [pause] "
  "Third, play the rate cycle. When the RBI is cutting rates, non-bank lenders and rate-sensitive financials often benefit — so watch the direction of policy. [pause] "
  "Fourth, a contrarian entry — when a quality bank falls hard on a temporary margin miss, as we saw with HDFC and Axis on their results, that can be a patient long-term entry, once the N I M stabilises. [pause] "
  "Whichever you choose, in banking, asset quality is king — never buy cheap growth built on bad loans."),
 ("f_check", "sm_checklist",
  {"kicker": "HOW TO EVALUATE", "title": "Evaluating a bank stock — checklist", "color": G, "icon": "✅",
   "items": [
    "Asset quality first: GNPA/NNPA low & improving?",
    "NIM healthy (~3–4%) and stable or rising?",
    "CASA high (cheap funding) & CAR well above 11.5%?",
    "ROA above 1%, with credit growth WITH quality?",
    "Valuation on P/B vs peers — pay up for clean books",
   ]},
  "Let's turn all of that into a practical checklist for any bank stock. Five steps. [pause] "
  "Step one — check asset quality first. Are the bad-loan ratios low, and are they improving? Never buy a bank whose asset quality is deteriorating. [pause] "
  "Step two — is the net interest margin healthy, around three to four percent, and stable or rising? [pause] "
  "Step three — is the CASA ratio high, giving cheap funding, and is capital adequacy comfortably above the RBI minimum? [pause] "
  "Step four — is return on assets above one percent, with loan growth that comes together with quality, not reckless lending? [pause] "
  "Step five — finally, value it on price-to-book against its peers, and be willing to pay up for a clean, well-run book rather than chasing the cheapest name. [pause] "
  "Run that, and you can size up any bank. Now the traps."),
 ("f_risk", "sm_myths",
  {"kicker": "WHAT TO AVOID", "title": "Finance sector — traps to avoid", "mythLabel": "✗ TRAP", "factLabel": "✓ REALITY",
   "pairs": [
    {"m": "This bank is cheap on P/E — bargain!", "f": "Value banks on P/B; a low multiple often hides bad loans"},
    {"m": "Fast loan growth = a great bank", "f": "Reckless growth today = the NPA crisis of tomorrow"},
    {"m": "High dividend PSU bank is safe", "f": "Check asset quality & capital first — yield can't fix a weak book"},
   ]},
  "Finally, the traps that catch beginners in this sector. [pause] "
  "The first trap — thinking a bank is a bargain because its price-to-earnings looks low. Banks are valued on price-to-book, and a low multiple very often hides a book full of bad loans. Cheap can be cheap for a deadly reason. [pause] "
  "The second trap — assuming fast loan growth means a great bank. Reckless lending today becomes the bad-loan crisis of tomorrow. Every banking blow-up in history began with someone growing too fast. [pause] "
  "The third trap — chasing a public-sector bank purely for its high dividend. A yield cannot fix a weak balance sheet. Always check asset quality and capital adequacy first. [pause] "
  "Respect asset quality above all, and the finance sector rewards you for decades."),
 ("f_recap", "sm_recap",
  {"title": "Finance sector — recap",
   "items": [
    "Analyse banks with NIM, GNPA/NNPA, CASA, CAR",
    "Also ROA (>1%), credit growth, cost-to-income",
    "Value on Price-to-Book, never P/E",
    "Technicals: track Bank Nifty, relative strength, breadth, RBI day",
    "Strategy: own quality leaders; asset quality is king",
   ],
   "closer": "In banking, a clean book beats a cheap price."},
  "The finance sector, in one breath. [pause] "
  "Analyse a bank with its special metrics — N I M, the bad-loan ratios, CASA, and capital adequacy — plus return on assets, credit growth, and efficiency. [pause] "
  "Value it on price-to-book, never on price-to-earnings. [pause] "
  "On the chart, track Bank Nifty, its relative strength versus the Nifty, its breadth, and the RBI calendar. [pause] "
  "And in strategy, own the quality leaders for the long run, because in banking a clean book always beats a cheap price. [pause] "
  "Next, a very different sector — defence."),
 ],

 # ============================== DEFENCE ==============================
 "def": [
 ("d_title", "sm_ptitle",
  {"title": "How to Analyse Defence Stocks", "sub": "Defence sector · fundamentals · technicals · strategies", "kicker": "SECTOR DEEP-DIVE · DEFENCE"},
  "Our second deep-dive — the defence sector, one of the most exciting and most hyped themes in the Indian market. [pause] "
  "This is a long-cycle, order-driven business, powered by government spending and India's push to build its own weapons. [pause] "
  "That makes it very different from a bank or an IT firm — it has its own language of order books and indigenisation. [pause] "
  "We'll cover the fundamentals unique to defence, the technicals, the strategies — and, importantly, the valuation risk after a huge rally."),
 ("d_why", "sm_iconcards",
  {"kicker": "THE BIG PICTURE", "title": "Why defence is a structural theme", "color": M,
   "items": [
    {"emoji": "💰", "k": "Record budgets", "v": "Union Budget 2026-27: ₹6.81 lakh crore for defence (+13%); capital outlay ₹2.19 lakh crore", "chip": "Govt spend"},
    {"emoji": "🇮🇳", "k": "Indigenisation", "v": "509 items reserved for Indian makers; 60% local content rule; 75% target by 2029", "chip": "Make in India"},
    {"emoji": "🌍", "k": "Exports rising", "v": "Defence exports ₹686 cr (FY17) → ₹21,083 cr (FY24); ₹50,000 cr target by 2029", "chip": "Exports"},
    {"emoji": "⚔️", "k": "Geopolitics", "v": "Global tensions keep defence spending — and investor attention — elevated", "chip": "Tailwind"},
   ]},
  "First, why defence is a genuine structural theme, not just a fad. Four forces. [pause] "
  "One — record government budgets. The Union Budget for twenty twenty-six to twenty-seven set aside six point eight one lakh crore rupees for defence, up thirteen percent, with a capital outlay — the money for actual equipment — of two point one nine lakh crore. [pause] "
  "Two — indigenisation. India now reserves over five hundred defence items to be bought only from Indian manufacturers, has raised the minimum local-content rule to sixty percent, and targets seventy-five percent home-made by twenty twenty-nine. That structurally protects domestic order flows. [pause] "
  "Three — exports. Defence exports have exploded from under seven hundred crore rupees in twenty seventeen to over twenty-one thousand crore by twenty twenty-four, with a fifty-thousand-crore target ahead. [pause] "
  "Four — geopolitics. A tense world keeps defence spending, and investor attention, high. [pause] "
  "That's a powerful, multi-year tailwind. Now, how do you actually analyse these companies?"),
 ("d_fund", "sm_iconcards",
  {"kicker": "FUNDAMENTALS · CORE", "title": "The metrics unique to defence", "color": G,
   "items": [
    {"emoji": "📚", "k": "Order book", "v": "The #1 metric — confirmed future orders. Bigger = more visible revenue", "chip": "Backlog"},
    {"emoji": "🔭", "k": "Book-to-bill", "v": "Order book ÷ annual revenue = years of visibility. E.g. BEL ~₹76,000 cr ≈ 4.5 yrs", "chip": "Visibility"},
    {"emoji": "🏭", "k": "Execution & margins", "v": "Can they convert orders to revenue on time? Watch EBITDA margin & delivery track record", "chip": "Delivery"},
    {"emoji": "💧", "k": "Working capital", "v": "Long project cycles lock up cash — watch receivables & cash flow, not just profit", "chip": "Cash"},
   ]},
  "Defence has its own special metrics, and the first one is everything. [pause] "
  "The order book — the total value of confirmed, signed orders a company has yet to execute. A large order book means visible, locked-in future revenue. This is the single most important number in the sector. [pause] "
  "Even better, divide the order book by annual revenue to get the book-to-bill ratio — literally, how many years of revenue are already in hand. Bharat Electronics, for example, carries an order book around seventy-six thousand crore rupees — roughly four and a half years of visibility. That is a fortress. [pause] "
  "But a big order book is worthless if the company can't deliver. So watch execution — can they convert those orders into revenue on time? Track the EBITDA margin and their historical delivery record. [pause] "
  "And watch working capital. Defence projects run for years, which locks up enormous cash in receivables. A company can show fat profits on paper while starving for cash — so follow the cash flow, not just the profit line."),
 ("d_tech", "sm_iconcards",
  {"kicker": "TECHNICAL ANALYSIS", "title": "Reading defence on the chart", "color": C,
   "items": [
    {"emoji": "📈", "k": "Nifty India Defence", "v": "The sector index. Concentrated: HAL ~24%, Solar ~14%, Mazagon ~8%, Bharat Forge ~7%", "chip": "Index"},
    {"emoji": "🚀", "k": "Momentum theme", "v": "A strong momentum sector — but momentum can crash hard after a big run", "chip": "Momentum"},
    {"emoji": "🗓️", "k": "Event catalysts", "v": "Budget, order-win announcements, geopolitics spike these stocks — often on the news", "chip": "Events"},
    {"emoji": "🌪️", "k": "High volatility", "v": "Sharp swings; use wider stops and never chase a vertical, news-driven spike", "chip": "Volatile"},
   ]},
  "Now the technicals for defence — a momentum-heavy, event-driven sector. [pause] "
  "There is a dedicated sector index, the Nifty India Defence index, but note it's concentrated: Hindustan Aeronautics alone is about a quarter of it, with Solar Industries, Mazagon Dock, and Bharat Forge making up much of the rest. So the index can be moved by a few giants. [pause] "
  "It is a strong momentum sector — it has delivered spectacular runs. But remember the lesson from options: momentum can crash hard and fast after a big move. What went vertical up can go vertical down. [pause] "
  "The catalysts are events — the Budget, order-win announcements, and geopolitical flare-ups. These stocks often spike the moment such news hits. [pause] "
  "And expect high volatility. Use wider stop-losses if you trade them, and never, ever chase a vertical, news-driven spike — that's exactly where latecomers get trapped."),
 ("d_strat", "sm_iconcards",
  {"kicker": "STRATEGIES", "title": "Strategies for the defence sector", "color": G,
   "items": [
    {"emoji": "🌳", "k": "Order-book compounders", "v": "For the long term, hold leaders with huge, growing order books & strong execution", "chip": "Hold"},
    {"emoji": "📉", "k": "Buy the dips, not the hype", "v": "Accumulate quality on corrections — not on a Budget-day or war-news spike", "chip": "Patience"},
    {"emoji": "🧺", "k": "Basket / index fund", "v": "A Nifty India Defence index fund spreads single-stock risk across the theme", "chip": "Diversify"},
    {"emoji": "🏭", "k": "PSU vs private", "v": "PSU giants (HAL, BEL) for scale; select private names for niche, higher-growth plays", "chip": "Mix"},
   ]},
  "So how do you invest in defence sensibly? Four strategies. [pause] "
  "First, treat the leaders as long-term order-book compounders — companies with huge, growing order books and a proven ability to execute. Hold them for the multi-year theme. [pause] "
  "Second, and this is vital here — buy the dips, not the hype. Accumulate quality on market corrections, not on the day a big order or a war headline sends the stock vertical. The news is already in the price by then. [pause] "
  "Third, if picking single stocks feels risky, a Nifty India Defence index fund lets you own the whole theme, spreading the single-company risk. [pause] "
  "Fourth, mix your exposure — the public-sector giants like Hindustan Aeronautics and Bharat Electronics for scale and stability, and select private players for niche, higher-growth stories. [pause] "
  "The theme is real and long. The danger is only ever the price you pay for it."),
 ("d_check", "sm_checklist",
  {"kicker": "HOW TO EVALUATE", "title": "Evaluating a defence stock — checklist", "color": G, "icon": "✅",
   "items": [
    "Order book size AND book-to-bill (years of visibility)",
    "Execution track record — can they deliver on time?",
    "Cash flow & working capital (long cycles lock cash)",
    "Indigenisation & export angle (structural growth)",
    "Valuation vs the order book — is the growth already priced in?",
   ]},
  "Let's make defence a practical checklist. Five steps. [pause] "
  "Step one — look at the order book size and the book-to-bill ratio together, to see how many years of revenue are locked in. [pause] "
  "Step two — check the execution track record. A big order book is worthless if the company can't deliver on time. [pause] "
  "Step three — examine cash flow and working capital, since long project cycles lock up cash and paper profit can mislead. [pause] "
  "Step four — assess the indigenisation and export angle, which provides the structural, multi-year growth. [pause] "
  "Step five — and crucially, weigh the valuation against that order book. Ask honestly: is all this wonderful growth already priced into the stock? In defence, the growth is real, but it's often expensive. [pause] "
  "Now the risks."),
 ("d_risk", "sm_myths",
  {"kicker": "WHAT TO AVOID", "title": "Defence sector — the big risks", "mythLabel": "✗ TRAP", "factLabel": "✓ REALITY",
   "pairs": [
    {"m": "War news — buy defence stocks now!", "f": "The spike is usually already priced in; latecomers get trapped"},
    {"m": "Order book is huge, so any price is fine", "f": "Nifty Defence P/E ~57 vs ~52 median — rich; valuation still matters"},
    {"m": "Profit is strong, so it's healthy", "f": "Long cycles lock cash — weak cash flow can hide behind paper profit"},
   ]},
  "Now the risks — because this is where the excitement does the most damage. [pause] "
  "The first trap — buying defence stocks the moment war or tension hits the news. By then, the spike is almost always already priced in, and the people buying the headline are the ones who get trapped when it fades. [pause] "
  "The second trap — believing that because the order book is huge, any price is justified. It isn't. The Nifty India Defence index has traded around fifty-seven times earnings, richer than its own three-year median near fifty-two. Even a wonderful theme becomes a poor investment if you overpay. Valuation always matters. [pause] "
  "The third trap — assuming strong profit means a healthy company. In this sector, long project cycles lock up cash, so weak cash flow can hide behind healthy-looking paper profit. Always check the cash. [pause] "
  "Love the theme, but respect the price and the cash — that is how you win in defence."),
 ("d_recap", "sm_recap",
  {"title": "Defence sector — recap",
   "items": [
    "Structural theme: record budgets, indigenisation, exports",
    "Key metrics: order book, book-to-bill visibility, execution, cash",
    "Index concentrated (HAL ~24%); momentum + event-driven",
    "Strategy: order-book compounders; buy dips, not hype",
    "Biggest risk: overpaying after a run (P/E ~57)",
   ],
   "closer": "A great theme is not a licence to overpay."},
  "The defence sector, gathered up. [pause] "
  "It's a genuine structural theme — record budgets, indigenisation, and rising exports give it a multi-year tailwind. [pause] "
  "Analyse it with its own metrics: the order book, the book-to-bill visibility, execution ability, and — crucially — cash flow, since long cycles lock up money. [pause] "
  "On the chart it's a concentrated, momentum-and-event-driven sector, so beware chasing spikes. [pause] "
  "In strategy, hold the order-book compounders and buy dips rather than hype, because the one real danger is overpaying after a huge run. [pause] "
  "Finally, our third sector — technology."),
 ],

 # ============================== TECHNOLOGY / IT ==============================
 "tec": [
 ("t_title", "sm_ptitle",
  {"title": "How to Analyse IT Stocks", "sub": "Technology sector · fundamentals · technicals · strategies", "kicker": "SECTOR DEEP-DIVE · TECHNOLOGY"},
  "Our third deep-dive — the technology sector, India's great export success story. [pause] "
  "Indian I T services companies earn most of their money abroad, in dollars, serving the world's biggest firms. [pause] "
  "That makes this sector move to a completely different beat from banks or defence — it dances to the US economy, the dollar, and now, to artificial intelligence. [pause] "
  "We'll cover the fundamentals of an I T company, the technicals, and the strategies — including how to think about the big correction of twenty twenty-six."),
 ("t_why", "sm_iconcards",
  {"kicker": "THE BIG PICTURE", "title": "What drives Indian IT", "color": V,
   "items": [
    {"emoji": "🌎", "k": "Export-driven", "v": "Most revenue comes from the US & Europe — global demand is everything", "chip": "Global"},
    {"emoji": "💵", "k": "Dollar-sensitive", "v": "Earns in dollars — a weaker rupee boosts profits; a stronger rupee hurts", "chip": "USD/INR"},
    {"emoji": "🏦", "k": "Client cycles", "v": "US client tech budgets & their quarterly results are the key catalyst", "chip": "US spend"},
    {"emoji": "🤖", "k": "The AI question", "v": "Is AI a threat that automates work, or a huge new deal opportunity? Both", "chip": "AI"},
   ]},
  "First, what makes I T tick — because it's unlike anything else we've covered. Four forces. [pause] "
  "One — it is export-driven. The vast majority of revenue comes from the United States and Europe, so global demand, not the Indian economy, is what matters most. [pause] "
  "Two — it is dollar-sensitive. These firms earn in dollars but report in rupees, so a weaker rupee boosts their profits, while a stronger rupee is a headwind. Always know which way the currency is moving. [pause] "
  "Three — client cycles. The tech budgets of big US clients, and their own quarterly results, are the single most-watched catalyst. Strong US data lifts Indian I T; a US slowdown hurts it. [pause] "
  "Four — the big question of our era: artificial intelligence. Is it a threat that automates away the work these firms do, or a massive new wave of deals to build AI for clients? Honestly, it is both — and telling the winners from the losers is now the whole game."),
 ("t_fund", "sm_iconcards",
  {"kicker": "FUNDAMENTALS · CORE", "title": "The metrics unique to IT", "color": G,
   "items": [
    {"emoji": "📈", "k": "Constant-currency growth", "v": "Revenue growth stripped of currency swings — the true underlying growth", "chip": "Real growth"},
    {"emoji": "📜", "k": "Deal TCV / pipeline", "v": "Total Contract Value of new deals — tomorrow's revenue, today's signal", "chip": "Future"},
    {"emoji": "📊", "k": "EBIT margin", "v": "Profitability & its consistency; ~20%+ for large-caps is the benchmark", "chip": "Margin"},
    {"emoji": "🚪", "k": "Attrition", "v": "Employee-exit rate. Lower = stable & efficient; a spike raises costs", "chip": "People"},
   ]},
  "Now the metrics that define an I T company — quite different from a bank's. [pause] "
  "The first is constant-currency revenue growth. Because the currency swings around, companies report growth stripped of that effect, to show the true underlying demand. This is the real growth number to anchor on. [pause] "
  "The second is deal wins — the Total Contract Value, or T C V, of new orders, and the strength of the deal pipeline. This is tomorrow's revenue showing up today; a strong pipeline is the best forward signal there is. [pause] "
  "The third is the EBIT margin — profitability, and above all its consistency. For the large-caps, around twenty percent or more is the benchmark. Margin discipline separates the great from the good. [pause] "
  "The fourth is attrition — how fast employees leave. This is a people business, so a low, stable attrition rate signals a healthy, efficient firm, while a sudden spike raises costs and disrupts projects. [pause] "
  "Together — real growth, a full pipeline, steady margins, and low attrition — these paint the picture of a strong I T company."),
 ("t_tech", "sm_iconcards",
  {"kicker": "TECHNICAL ANALYSIS", "title": "Reading IT on the chart", "color": C,
   "items": [
    {"emoji": "📉", "k": "Nifty IT index", "v": "The sector gauge. In 2026 it fell ~25% YTD — a deep correction into a 'value zone'", "chip": "Index"},
    {"emoji": "💵", "k": "Watch USD/INR", "v": "Overlay the rupee — dollar strength is a tailwind for the whole sector", "chip": "Currency"},
    {"emoji": "🌙", "k": "US market cues", "v": "US tech (Nasdaq) & US client results guide IT's direction overnight", "chip": "Global"},
    {"emoji": "💪", "k": "Relative strength", "v": "Defensive in slowdowns; check if IT is leading or lagging the Nifty", "chip": "Rotation"},
   ]},
  "The technicals for I T carry a global flavour. [pause] "
  "Track the Nifty I T index as your sector gauge. And here's the timely context: through twenty twenty-six it has fallen around twenty-five percent, a deep correction that has pushed valuations into what many now call a value zone — even as the companies keep winning deals. [pause] "
  "Overlay the dollar-rupee rate on the chart. Dollar strength is a tailwind for the entire sector, so the currency and the index often move together. [pause] "
  "Watch overnight US cues — the Nasdaq and, especially, the quarterly results of big US clients guide where Indian I T opens the next morning. This is a sector you analyse with one eye on America. [pause] "
  "And check relative strength. I T is a partial defensive — it can hold up when domestic cyclicals fall — so see whether it's leading or lagging the Nifty in the current rotation."),
 ("t_strat", "sm_iconcards",
  {"kicker": "STRATEGIES", "title": "Strategies for the technology sector", "color": G,
   "items": [
    {"emoji": "💎", "k": "Buy quality in the correction", "v": "A 25% fall in strong franchises can be a long-term accumulation zone", "chip": "Value"},
    {"emoji": "💵", "k": "Cash returners", "v": "IT throws off cash — dividends + buybacks reward patient holders", "chip": "Income"},
    {"emoji": "⚖️", "k": "Large vs mid-cap", "v": "Large-caps for stability; mid-caps for higher growth (and higher risk)", "chip": "Mix"},
    {"emoji": "🤖", "k": "Pick AI winners", "v": "Favour firms turning AI into deals over those most exposed to automation", "chip": "Selective"},
   ]},
  "So how do you play technology? Four strategies, well suited to today. [pause] "
  "First, buy quality into the correction. A twenty-five-percent fall in a strong, cash-rich franchise — one still winning deals — can be a fine long-term accumulation zone. Fear creates the opportunity. [pause] "
  "Second, treat I T as a cash returner. These companies generate enormous free cash and hand it back through generous dividends and share buybacks, which rewards patient holders even when growth is slow. [pause] "
  "Third, balance large versus mid-cap. The large-caps offer stability and those cash returns; the mid-caps offer higher growth, with higher risk. Mix to taste. [pause] "
  "Fourth — and this is the defining call of the decade — pick the AI winners. Favour the firms that are turning artificial intelligence into new client deals, and be wary of those whose core work is most easily automated away. In this sector, stock selection now matters far more than simply owning I T. [pause] "
  "The tide alone will not lift all boats here."),
 ("t_check", "sm_checklist",
  {"kicker": "HOW TO EVALUATE", "title": "Evaluating an IT stock — checklist", "color": G, "icon": "✅",
   "items": [
    "Is constant-currency revenue growth healthy?",
    "Is the deal pipeline (TCV) strong & growing?",
    "Are EBIT margins consistent (~20%+ large-cap)?",
    "Is attrition low & stable (a healthy people business)?",
    "Is it an AI winner or the one being automated away?",
   ]},
  "Let's turn IT into a checklist. Five steps. [pause] "
  "Step one — is the constant-currency revenue growth healthy, showing real underlying demand beneath the currency noise? [pause] "
  "Step two — is the deal pipeline, the total contract value, strong and growing, promising tomorrow's revenue? [pause] "
  "Step three — are the EBIT margins consistent, around twenty percent or more for a large-cap, showing disciplined delivery? [pause] "
  "Step four — is attrition low and stable, the sign of a healthy people business? [pause] "
  "Step five — and the defining question of the decade — is this company an AI winner turning the technology into new deals, or the one whose work is being automated away? [pause] "
  "Run that checklist, and you can judge any IT name. Now the traps."),
 ("t_risk", "sm_myths",
  {"kicker": "WHAT TO AVOID", "title": "Technology sector — traps to avoid", "mythLabel": "✗ TRAP", "factLabel": "✓ REALITY",
   "pairs": [
    {"m": "It fell 25% — it must be cheap now", "f": "Cheap can get cheaper if US demand keeps slowing — check the deal pipeline"},
    {"m": "AI will lift every IT company", "f": "AI will create winners AND losers — selection is everything"},
    {"m": "A weak rupee alone makes IT a buy", "f": "Currency helps margins, but demand & deals drive the real story"},
   ]},
  "And the traps in technology — subtle, because the story sounds so good. [pause] "
  "The first trap — assuming that because I T fell twenty-five percent, it must be cheap. Cheap can get cheaper if US demand keeps slowing. Don't buy the fall blindly; check that the deal pipeline is still healthy. A falling price with a shrinking order book is a trap, not a bargain. [pause] "
  "The second trap — believing artificial intelligence will lift every I T company alike. It won't. AI will create clear winners and clear losers, and treating the sector as one basket ignores the most important divide of the decade. Selection is everything. [pause] "
  "The third trap — buying I T just because the rupee is weak. A favourable currency helps the margins, yes, but it cannot rescue a company losing deals. Demand and deal wins drive the real story; currency is only the tailwind. [pause] "
  "Read the demand, read the pipeline, pick the AI winners — that's how you navigate technology."),
 ("t_recap", "sm_recap",
  {"title": "Technology sector — recap",
   "items": [
    "Export-driven: US demand, USD/INR, client cycles, AI",
    "Metrics: constant-currency growth, deal TCV, EBIT margin, attrition",
    "Technicals: Nifty IT (−25% in 2026), USD & US cues, relative strength",
    "Strategy: buy quality in the fall; cash returns; pick AI winners",
    "Selection now matters more than owning the sector",
   ],
   "closer": "In IT today, choose the winners — don't just buy the theme."},
  "The technology sector, in one breath. [pause] "
  "It's export-driven, moving to US demand, the dollar-rupee rate, client cycles, and now artificial intelligence. [pause] "
  "Analyse it with its own metrics: constant-currency growth, deal T C V, EBIT margin, and attrition. [pause] "
  "On the chart, track the Nifty I T index — down about twenty-five percent in twenty twenty-six — alongside the dollar and US cues. [pause] "
  "In strategy, buy quality into the correction, enjoy the dividends and buybacks, and above all pick the AI winners — because selection now matters more than simply owning the sector. [pause] "
  "That completes our three sector deep-dives. Apply the same method — sector-specific fundamentals, technicals, and strategy — to any sector you study. This is education, not advice; always do your own research. Thank you for watching."),
 ],

 # ============================== PHARMA / HEALTHCARE ==============================
 "pha": [
 ("p_title", "sm_ptitle",
  {"title": "How to Analyse Pharma Stocks", "sub": "Pharma & healthcare · fundamentals · technicals · strategies", "kicker": "SECTOR DEEP-DIVE · PHARMA"},
  "The pharma and healthcare sector — India's medicine cabinet to the world. [pause] "
  "India is the largest maker of generic drugs on earth, and about a third of its pharma exports go to the United States. [pause] "
  "That single fact shapes everything — because it means the US regulator, the FDA, holds enormous power over these stocks. [pause] "
  "Let's learn the sector's unique fundamentals, its technicals, and its strategies. Company names are examples only."),
 ("p_overview", "sm_iconcards",
  {"kicker": "SUB-SECTORS", "title": "Pharma is several businesses", "color": G,
   "items": [
    {"emoji": "💊", "k": "US generics", "v": "Sell copies of off-patent drugs in the US — high margin, but FDA-and-price-risk", "chip": "Exports"},
    {"emoji": "🏠", "k": "Domestic formulations", "v": "Branded medicines sold in India — steady, defensive, brand-driven", "chip": "Stable"},
    {"emoji": "🧪", "k": "API / CDMO", "v": "Ingredients & contract manufacturing — a China+1 structural winner", "chip": "B2B"},
    {"emoji": "🏥", "k": "Hospitals & diagnostics", "v": "Healthcare services — a domestic consumption growth story", "chip": "Services"},
   ]},
  "First, understand that pharma is really several different businesses under one label. [pause] "
  "The first is US generics — making low-cost copies of off-patent drugs to sell in America. It's high-margin, but it carries the twin risks of FDA regulation and relentless price competition. [pause] "
  "The second is domestic formulations — branded medicines sold here in India. This is a steady, defensive, brand-driven business, much safer than the US game. [pause] "
  "The third is active ingredients and contract manufacturing — the API and CDMO businesses that supply other drug-makers. This is a big China-plus-one structural winner. [pause] "
  "And the fourth is healthcare services — hospitals and diagnostic-testing chains, which are really a domestic consumption growth story rather than a drug business. [pause] "
  "A company focused on US generics is analysed very differently from a hospital chain — so always know which pharma you're looking at."),
 ("p_drivers", "sm_iconcards",
  {"kicker": "WHAT MOVES PHARMA", "title": "The forces that drive the sector", "color": C,
   "items": [
    {"emoji": "🏛️", "k": "USFDA actions", "v": "Inspections, approvals, warning letters — the biggest swing factor for exporters", "chip": "Regulator"},
    {"emoji": "💵", "k": "US price erosion", "v": "Brutal generic competition steadily erodes US drug prices & margins", "chip": "Pricing"},
    {"emoji": "🌏", "k": "China+1", "v": "Global supply chains diversifying to India — a tailwind for API & CDMO", "chip": "Structural"},
    {"emoji": "💊", "k": "Domestic growth", "v": "Rising incomes, insurance & chronic disease drive steady home-market demand", "chip": "India"},
   ]},
  "What moves pharma? Four forces. [pause] "
  "The first, and the biggest swing factor, is USFDA action — inspections, approvals, and warning letters. A single regulatory outcome can move an exporter's stock by twenty percent. [pause] "
  "The second is US price erosion. The American generics market is brutally competitive, and prices grind steadily lower, constantly pressuring the margins of Indian exporters. [pause] "
  "The third is the China-plus-one shift, a genuine tailwind for the ingredients and contract-manufacturing businesses as the world diversifies its drug supply chains toward India. [pause] "
  "The fourth is domestic growth — rising incomes, expanding health insurance, and an unfortunate rise in chronic disease all drive steady, defensive demand in the home market. [pause] "
  "Now, the metrics that let you value these businesses."),
 ("p_fund", "sm_iconcards",
  {"kicker": "FUNDAMENTALS · CORE", "title": "The metrics unique to pharma", "color": G,
   "items": [
    {"emoji": "🏛️", "k": "USFDA status", "v": "The #1 risk. A Form 483, warning letter or import alert can stall approvals & crush a stock", "chip": "Regulatory"},
    {"emoji": "💊", "k": "Approvals pipeline", "v": "ANDA filings & approvals = future US revenue; a rich pipeline is the growth engine", "chip": "Pipeline"},
    {"emoji": "🌍", "k": "Revenue mix", "v": "US vs India vs API/emerging. US = high-margin but risky; domestic = steady & defensive", "chip": "Mix"},
    {"emoji": "🔬", "k": "R&D & margins", "v": "R&D spend fuels the pipeline; watch gross margins and US price erosion", "chip": "Quality"},
   ]},
  "Pharma has its own special metrics, and the first one dominates all others. [pause] "
  "It is the USFDA status of a company's factories. Because so much revenue comes from America, a bad inspection — a Form 483, a warning letter, or an import alert — can halt new approvals and hit revenue overnight. A single warning letter has cratered many a pharma stock. This is the number-one risk to track. [pause] "
  "The second is the approvals pipeline — the count of ANDA filings and approvals, which are the pending applications to sell generic drugs in the US. A rich pipeline is the growth engine. [pause] "
  "The third is the revenue mix — how much comes from the US, from India, and from ingredients or emerging markets. US business is high-margin but regulatory-risky; the domestic business is steady and defensive. [pause] "
  "The fourth is R&D spend, which fuels tomorrow's pipeline, alongside gross margins and the constant threat of price erosion in the crowded US generics market."),
 ("p_tech", "sm_iconcards",
  {"kicker": "TECHNICAL ANALYSIS", "title": "Reading pharma on the chart", "color": C,
   "items": [
    {"emoji": "📈", "k": "Nifty Pharma / Healthcare", "v": "The sector indices to track for trend and relative strength", "chip": "Index"},
    {"emoji": "🛡️", "k": "Defensive nature", "v": "Tends to hold up in slowdowns & risk-off — check if it's leading a defensive rotation", "chip": "Defensive"},
    {"emoji": "⚡", "k": "News-driven gaps", "v": "FDA outcomes & approvals cause sharp single-stock gaps — stock-specific, not just index", "chip": "Events"},
    {"emoji": "💵", "k": "Weak-rupee tailwind", "v": "Dollar earners — a weaker rupee helps, like IT", "chip": "USD"},
   ]},
  "On the chart, pharma behaves in a distinctive way. [pause] "
  "Track the Nifty Pharma and Nifty Healthcare indices for the sector trend and its relative strength versus the market. [pause] "
  "Remember it is a defensive sector — people need medicine in every economy — so it often holds up when cyclicals fall. In a risk-off market, check whether pharma is leading a flight to defensives. [pause] "
  "But individual pharma stocks are famously news-driven. An FDA outcome or a big approval can gap a single stock ten or twenty percent overnight, regardless of the index. So here, stock-specific chart levels matter as much as the sector. [pause] "
  "And like IT, these are dollar earners, so a weaker rupee is a quiet tailwind for the whole sector."),
 ("p_strat", "sm_iconcards",
  {"kicker": "STRATEGIES", "title": "Strategies for pharma", "color": G,
   "items": [
    {"emoji": "✅", "k": "Clean-record leaders", "v": "Favour companies with a strong FDA compliance track record — fewer nasty surprises", "chip": "Quality"},
    {"emoji": "🏥", "k": "Domestic & hospitals", "v": "India-focused pharma, hospitals & diagnostics = steadier, less FDA-exposed growth", "chip": "Stable"},
    {"emoji": "🧪", "k": "CDMO / API theme", "v": "Contract manufacturing & ingredients ride the 'China+1' shift — a structural play", "chip": "Theme"},
    {"emoji": "📉", "k": "Buy the FDA over-reaction", "v": "A quality name oversold on a resolvable FDA issue can be a patient entry", "chip": "Contrarian"},
   ]},
  "How do you play pharma sensibly? Four strategies. [pause] "
  "First, favour the leaders with a clean FDA compliance record. Fewer regulatory surprises means fewer sleepless nights and fewer sudden crashes. [pause] "
  "Second, lean on the domestic side — India-focused pharma, plus hospitals and diagnostics, which offer steadier, defensive growth with far less US regulatory exposure. [pause] "
  "Third, ride the structural theme — contract manufacturing, the CDMO business, and active ingredients, or APIs. As the world diversifies supply chains away from China — the China-plus-one shift — Indian makers benefit for years. [pause] "
  "Fourth, a contrarian entry: when a genuinely good company is oversold on an FDA issue that is likely resolvable, that fear can create a patient long-term opportunity. But only for quality — a weak company with FDA trouble can stay broken. [pause] "
  "In pharma, compliance quality is your compass."),
 ("p_check", "sm_checklist",
  {"kicker": "HOW TO EVALUATE", "title": "Evaluating a pharma stock — checklist", "color": G, "icon": "✅",
   "items": [
    "Check the FDA status of ALL key plants first",
    "Assess US vs domestic revenue mix (risk vs stability)",
    "Look at the approvals pipeline & R&D spend",
    "Watch gross margins for US price-erosion pressure",
    "Prefer a clean compliance track record over a cheap price",
   ]},
  "Before the risks, let's turn this into a practical checklist for any pharma stock. Five steps. [pause] "
  "Step one — check the FDA status of all the company's key plants first, because one troubled facility can sink the whole stock. [pause] "
  "Step two — assess the revenue mix between the high-margin but risky US business and the steady, defensive domestic business. [pause] "
  "Step three — look at the approvals pipeline and R&D spend, which together tell you the future growth. [pause] "
  "Step four — watch the gross margins for signs of US price-erosion pressure eating into profits. [pause] "
  "Step five — and above all, prefer a company with a clean compliance track record over one that merely looks cheap. In pharma, compliance quality beats a low price every time. [pause] "
  "Now, the traps to avoid."),
 ("p_risk", "sm_myths",
  {"kicker": "WHAT TO AVOID", "title": "Pharma sector — the risks", "mythLabel": "✗ TRAP", "factLabel": "✓ REALITY",
   "pairs": [
    {"m": "Cheap pharma stock after a fall = bargain", "f": "An unresolved FDA warning can keep revenue & the stock down for years"},
    {"m": "Big US pipeline guarantees growth", "f": "US generic price erosion can eat the gains — margins matter"},
    {"m": "Pharma is defensive, so always safe", "f": "Single-plant FDA risk makes individual stocks anything but safe"},
   ]},
  "Now the traps unique to pharma. [pause] "
  "The first — assuming a pharma stock that has fallen hard is automatically a bargain. If it fell on an unresolved FDA warning letter, its revenue and its stock can stay depressed for years until the issue is fixed. Check the compliance status first. [pause] "
  "The second — believing a large US pipeline guarantees growth. The US generics market is brutally competitive, and constant price erosion can eat those gains. A pipeline only helps if margins survive. [pause] "
  "The third — thinking that because pharma is defensive, every pharma stock is safe. The sector is defensive, but an individual company that depends on one FDA-troubled plant is anything but safe. Diversify, and mind the plant risk. [pause] "
  "Respect the FDA, respect price erosion, and pharma rewards you."),
 ("p_recap", "sm_recap",
  {"title": "Pharma sector — recap",
   "items": [
    "USFDA status is the #1 metric — warning letters crush stocks",
    "Watch approvals pipeline, revenue mix, R&D, price erosion",
    "Defensive sector, but stocks gap hard on FDA news",
    "Strategy: clean-record leaders, domestic/hospitals, China+1 CDMO",
    "Weak rupee = tailwind (dollar earners)",
   ],
   "closer": "In pharma, FDA compliance is everything."},
  "Pharma, in one breath. [pause] "
  "The USFDA status of the factories is the number-one metric — a warning letter can crush a stock, so watch it above all. [pause] "
  "Also track the approvals pipeline, the revenue mix, R&D spend, and US price erosion. [pause] "
  "It's a defensive sector, but individual stocks gap violently on FDA news, and a weak rupee helps the whole group. [pause] "
  "In strategy, favour clean-record leaders, the steadier domestic and hospital names, and the China-plus-one contract-manufacturing theme. [pause] "
  "Next, a very cyclical sector — autos."),
 ],

 # ============================== AUTO ==============================
 "aut": [
 ("a_title", "sm_ptitle",
  {"title": "How to Analyse Auto Stocks", "sub": "Automobile sector · fundamentals · technicals · strategies", "kicker": "SECTOR DEEP-DIVE · AUTO"},
  "The automobile sector — one of the great cyclicals, and right now, one of the most disrupted. [pause] "
  "Autos rise and fall with the economy, with interest rates, and with the price of steel. [pause] "
  "And layered on top is the biggest shift in a century — the move to electric vehicles, which is creating clear winners and losers. [pause] "
  "Let's learn the fundamentals, the technicals, and the strategies for this fast-changing sector."),
 ("a_overview", "sm_iconcards",
  {"kicker": "SUB-SECTORS", "title": "Auto is many segments", "color": V,
   "items": [
    {"emoji": "🏍️", "k": "Two-wheelers", "v": "Bikes & scooters — mass-market, rural-sensitive, huge volumes", "chip": "2W"},
    {"emoji": "🚗", "k": "Passenger vehicles", "v": "Cars & SUVs — urban, discretionary, premiumisation & EV shift", "chip": "PV"},
    {"emoji": "🚚", "k": "Commercial vehicles", "v": "Trucks & buses — pure economy play; track freight & capex", "chip": "CV"},
    {"emoji": "🧩", "k": "Ancillaries", "v": "Component makers supplying all of the above — plus global & EV clients", "chip": "Suppliers"},
   ]},
  "First, understand that auto is not one market but several segments, each with its own cycle. [pause] "
  "Two-wheelers — bikes and scooters — are mass-market and highly sensitive to rural income, with enormous volumes. [pause] "
  "Passenger vehicles — cars and SUVs — are an urban, discretionary purchase, where premiumisation and the EV shift are playing out fastest. [pause] "
  "Commercial vehicles — trucks and buses — are a pure play on the economy; when freight and infrastructure boom, so do they. [pause] "
  "And tractors are a rural-and-monsoon play of their own. Sitting beneath all of them are the ancillaries — the component makers who supply every segment, and the best of whom also serve global and EV customers. [pause] "
  "Know which segment a maker depends on, because their cycles don't move together."),
 ("a_drivers", "sm_iconcards",
  {"kicker": "WHAT MOVES AUTO", "title": "The forces that drive the sector", "color": C,
   "items": [
    {"emoji": "📊", "k": "Demand cycle", "v": "Incomes, sentiment & the economy — autos are a discretionary big-ticket buy", "chip": "Economy"},
    {"emoji": "🏛️", "k": "Interest rates", "v": "Most vehicles are bought on loans — cheaper EMIs lift demand", "chip": "Rates"},
    {"emoji": "🔩", "k": "Commodity costs", "v": "Steel & aluminium prices drive the margin — links auto to the metals cycle", "chip": "Inputs"},
    {"emoji": "⚡", "k": "Fuel & EV policy", "v": "Fuel prices, emission norms & EV incentives reshape demand & the winners", "chip": "Policy"},
   ]},
  "What drives the auto sector? Four forces. [pause] "
  "The first is the demand cycle. A vehicle is a big-ticket, discretionary purchase, so demand rises and falls with incomes, sentiment, and the broader economy. [pause] "
  "The second is interest rates. Most vehicles are bought on loans, so cheaper EMIs from lower rates directly lift demand — a rate-cut cycle is good for autos. [pause] "
  "The third is commodity costs. Steel and aluminium are the biggest input costs, so the metals cycle flows straight into auto margins. [pause] "
  "The fourth is fuel and EV policy — petrol prices, emission norms, and electric-vehicle incentives together reshape what people buy and, crucially, which makers win. [pause] "
  "Now, the metrics for analysing an auto company."),
 ("a_fund", "sm_iconcards",
  {"kicker": "FUNDAMENTALS · CORE", "title": "The metrics unique to auto", "color": V,
   "items": [
    {"emoji": "🚗", "k": "Monthly sales volumes", "v": "The heartbeat — wholesale & retail unit sales, reported every month. The #1 signal", "chip": "Volumes"},
    {"emoji": "🏍️", "k": "Segment mix", "v": "2-wheelers, cars, commercial vehicles, tractors — each has its own cycle", "chip": "Mix"},
    {"emoji": "🔩", "k": "Input costs", "v": "Steel & aluminium are big cost lines — commodity prices squeeze or fatten margins", "chip": "Costs"},
    {"emoji": "⚡", "k": "EV transition", "v": "Who is winning the shift to electric — and who is being disrupted?", "chip": "EV"},
   ]},
  "Auto has four defining metrics. [pause] "
  "The first, and the heartbeat of the sector, is monthly sales volumes — the units sold, reported every single month. No other sector gives you such a clear, high-frequency demand signal. When volumes turn, the stocks turn. [pause] "
  "The second is the segment mix. Two-wheelers, passenger cars, commercial vehicles, and tractors each move on their own cycle — commercial vehicles track the economy, tractors track the monsoon and rural income. Know which segment a company depends on. [pause] "
  "The third is input costs. Steel and aluminium are huge cost lines for a car-maker, so when those commodity prices rise, margins get squeezed; when they fall, margins fatten. This links auto directly to the metals cycle. [pause] "
  "The fourth is the electric-vehicle transition — the defining question of the decade. Watch closely who is winning the shift to EVs, and whose traditional business is being quietly disrupted."),
 ("a_tech", "sm_iconcards",
  {"kicker": "TECHNICAL ANALYSIS", "title": "Reading auto on the chart", "color": C,
   "items": [
    {"emoji": "📈", "k": "Nifty Auto", "v": "The sector index. Track its trend and relative strength versus the Nifty", "chip": "Index"},
    {"emoji": "🗓️", "k": "1st-of-month spike", "v": "Monthly sales numbers land at month-start — the sector's biggest recurring catalyst", "chip": "Sales day"},
    {"emoji": "🔄", "k": "Cyclical timing", "v": "A classic cyclical — leads in economic recoveries, lags in slowdowns", "chip": "Cyclical"},
    {"emoji": "🔩", "k": "Inverse to metals", "v": "Rising steel/aluminium often pressures auto margins — watch that link", "chip": "Costs"},
   ]},
  "On the chart, auto has a wonderfully predictable rhythm. [pause] "
  "Track the Nifty Auto index for the sector trend and its relative strength. [pause] "
  "The single biggest recurring catalyst is the monthly sales data, which lands at the start of every month. The whole sector reacts to whether volumes beat or missed. Mark the first of the month. [pause] "
  "Treat auto as a classic cyclical — it tends to lead in an economic recovery, when people finally buy that new car, and to lag in a slowdown. Time it with the economic cycle. [pause] "
  "And watch its inverse relationship with metals — a sharp rise in steel and aluminium prices often pressures auto margins, so the two sectors can move against each other."),
 ("a_strat", "sm_iconcards",
  {"kicker": "STRATEGIES", "title": "Strategies for auto", "color": G,
   "items": [
    {"emoji": "🔄", "k": "Play the volume cycle", "v": "Buy leaders early in a demand up-cycle; trim as volumes & margins peak", "chip": "Cyclical"},
    {"emoji": "⚡", "k": "Back the EV winners", "v": "Favour makers gaining EV share; be wary of those most exposed to disruption", "chip": "Future"},
    {"emoji": "🧩", "k": "Ancillaries too", "v": "Auto-component makers ride the same cycle — and some supply EV & global clients", "chip": "Suppliers"},
    {"emoji": "🚜", "k": "Segment-specific", "v": "Match your bet to the segment cycle — tractors on a good monsoon, CVs on capex", "chip": "Targeted"},
   ]},
  "How do you play autos? Four strategies. [pause] "
  "First, play the volume cycle. Buy the leaders early in a demand up-cycle, when sales are just recovering, and trim as volumes and margins reach a peak. Cyclicals are about timing. [pause] "
  "Second, back the EV winners. Favour the makers who are gaining share in electric vehicles, and be cautious with those whose bread-and-butter models face the most disruption. This is a structural, not just cyclical, call. [pause] "
  "Third, don't forget the ancillaries — the auto-component makers ride the very same cycle, and the best of them supply EVs and global customers, giving an extra growth angle. [pause] "
  "Fourth, be segment-specific. Bet on tractor-makers when the monsoon is good and rural income is rising; on commercial-vehicle makers when infrastructure and freight are booming. Match the bet to the segment's own cycle. [pause] "
  "In autos, timing the cycle and picking the EV side correctly are everything."),
 ("a_check", "sm_checklist",
  {"kicker": "HOW TO EVALUATE", "title": "Evaluating an auto stock — checklist", "color": G, "icon": "✅",
   "items": [
    "Track the multi-month sales-volume trend (not one month)",
    "Know the segment mix (2W / PV / CV / tractor) & its cycle",
    "Watch input costs (steel/aluminium) squeezing margins",
    "Judge the company's EV position — winner or disrupted?",
    "Time your entry to the demand cycle, not to peak profits",
   ]},
  "Let's make that a checklist for any auto stock. Five steps. [pause] "
  "Step one — track the multi-month trend in sales volumes, not a single month that could be festive or discount-driven. [pause] "
  "Step two — know the segment mix and its cycle: two-wheelers, cars, commercial vehicles, or tractors, each moving to a different beat. [pause] "
  "Step three — watch input costs, especially steel and aluminium, which squeeze or fatten margins. [pause] "
  "Step four — judge the company's electric-vehicle position honestly: is it a winner in the transition, or the one being disrupted? [pause] "
  "Step five — and crucially, time your entry to the demand cycle, buying into a recovery rather than at peak profits when the stock only looks cheap. [pause] "
  "Now, the cyclical traps."),
 ("a_risk", "sm_myths",
  {"kicker": "WHAT TO AVOID", "title": "Auto sector — the risks", "mythLabel": "✗ TRAP", "factLabel": "✓ REALITY",
   "pairs": [
    {"m": "Record profits — buy the auto stock!", "f": "Cyclicals look cheapest (low P/E) at the TOP, just before margins fall"},
    {"m": "The market leader can't be disrupted", "f": "EV shifts can dethrone incumbents — yesterday's giant, tomorrow's laggard"},
    {"m": "Good sales one month = a trend", "f": "One month can be festive/discount-driven — watch the multi-month trend"},
   ]},
  "Now the cyclical traps in auto. [pause] "
  "The first, and the classic cyclical trap — buying because profits are at a record and the price-to-earnings looks low. Cyclicals look cheapest right at the top, just before margins roll over. Low P E at a peak is a warning, not a bargain. [pause] "
  "The second — assuming the current market leader can never be disrupted. The EV shift can dethrone incumbents; a dominant maker of petrol cars can become tomorrow's laggard if it misses the transition. [pause] "
  "The third — reading one strong sales month as a trend. A single month can be inflated by festive demand or heavy discounts. Always look at the multi-month volume trend, not one data point. [pause] "
  "Respect the cycle, watch the EV shift, and autos can be very rewarding."),
 ("a_recap", "sm_recap",
  {"title": "Auto sector — recap",
   "items": [
    "Monthly sales volumes are the #1 signal",
    "Watch segment mix, input costs (steel), the EV shift",
    "A cyclical — leads recoveries, lags slowdowns",
    "Strategy: play the volume cycle; back EV winners",
    "Trap: cyclicals look cheapest at the peak",
   ],
   "closer": "Buy autos into a recovery — never at peak margins."},
  "Autos, gathered up. [pause] "
  "Monthly sales volumes are the sector's heartbeat and its number-one signal. [pause] "
  "Watch the segment mix, input costs like steel, and above all the electric-vehicle transition. [pause] "
  "It's a classic cyclical — it leads recoveries and lags slowdowns — so time it with the economy. [pause] "
  "In strategy, play the volume cycle and back the EV winners, and never forget that cyclicals look cheapest exactly at the peak. [pause] "
  "Next, the ultimate defensive — consumer staples, or FMCG."),
 ],

 # ============================== FMCG ==============================
 "fmc": [
 ("m_title", "sm_ptitle",
  {"title": "How to Analyse FMCG Stocks", "sub": "Consumer staples · fundamentals · technicals · strategies", "kicker": "SECTOR DEEP-DIVE · FMCG"},
  "The FMCG sector — fast-moving consumer goods, the soaps, foods, and everyday products in every home. [pause] "
  "This is the great defensive of the market. People buy toothpaste and biscuits in booms and busts alike, so demand is steady and predictable. [pause] "
  "That stability makes these the classic slow-and-steady compounders — but it comes at a price, quite literally, in valuation. [pause] "
  "Let's learn the fundamentals, technicals, and strategies for this calm corner of the market."),
 ("m_overview", "sm_iconcards",
  {"kicker": "SUB-SECTORS", "title": "What sits inside FMCG", "color": M,
   "items": [
    {"emoji": "🍜", "k": "Food & beverages", "v": "Packaged foods, tea, snacks — everyday staples with steady demand", "chip": "Food"},
    {"emoji": "🧼", "k": "Home & personal care", "v": "Soaps, detergents, cosmetics — high-frequency, brand-driven", "chip": "HPC"},
    {"emoji": "🚬", "k": "Staples & tobacco", "v": "Cigarettes & basics — cash-generative, very pricing-power-rich", "chip": "Cash"},
    {"emoji": "✨", "k": "Premium & new-age", "v": "Premium and D2C brands riding India's trade-up — the faster growth", "chip": "Premium"},
   ]},
  "First, a quick map of what sits inside FMCG. [pause] "
  "There's food and beverages — packaged foods, tea, and snacks, everyday staples with beautifully steady demand. [pause] "
  "There's home and personal care — soaps, detergents, and cosmetics — high-frequency, deeply brand-driven purchases. [pause] "
  "There are the pure staples and tobacco names — hugely cash-generative, with some of the strongest pricing power in the whole market. [pause] "
  "And there's the premium and new-age end — premium brands and direct-to-consumer names riding India's trade-up, where the faster growth hides in an otherwise slow sector. [pause] "
  "All share the same defensive DNA, but their growth rates and valuations differ — so know the mix."),
 ("m_drivers", "sm_iconcards",
  {"kicker": "WHAT MOVES FMCG", "title": "The forces that drive the sector", "color": C,
   "items": [
    {"emoji": "🏘️", "k": "Rural demand", "v": "About a third of sales — monsoon & farm income swing the whole sector", "chip": "Rural"},
    {"emoji": "🛢️", "k": "Input costs", "v": "Palm oil, crude derivatives & packaging drive margins up and down", "chip": "Costs"},
    {"emoji": "💰", "k": "Pricing power", "v": "Ability to pass on cost rises without losing customers — the real moat", "chip": "Power"},
    {"emoji": "✨", "k": "Premiumisation", "v": "Consumers trading up to costlier products — the sector's growth engine", "chip": "Growth"},
   ]},
  "What drives FMCG? Four gentle forces. [pause] "
  "The first is rural demand, roughly a third of sales, which swings with the monsoon and farm incomes — a good monsoon is a genuine tailwind for the sector. [pause] "
  "The second is input costs — palm oil, crude-derived materials, and packaging — which push margins up and down as commodity prices move. [pause] "
  "The third is pricing power — a company's ability to pass those cost rises on to customers without losing them. That is the real moat in consumer goods, and it separates the great brands from the also-rans. [pause] "
  "The fourth is premiumisation — consumers steadily trading up to costlier, fancier products. In a slow-growing sector, this is where the faster growth comes from. [pause] "
  "Now, the metrics that reveal a healthy FMCG business."),
 ("m_fund", "sm_iconcards",
  {"kicker": "FUNDAMENTALS · CORE", "title": "The metrics unique to FMCG", "color": M,
   "items": [
    {"emoji": "📦", "k": "Volume growth", "v": "The #1 metric — real growth in units sold, NOT just value inflated by price hikes", "chip": "Real growth"},
    {"emoji": "🏘️", "k": "Rural vs urban", "v": "Rural is ~a third of sales — its recovery (monsoon, income) swings the sector", "chip": "Demand"},
    {"emoji": "💰", "k": "Gross margin", "v": "Input costs — palm oil, crude derivatives — drive margins; pricing power protects them", "chip": "Margins"},
    {"emoji": "🛒", "k": "Distribution & premium", "v": "Reach into millions of stores + premiumisation (trading up) = the growth levers", "chip": "Moat"},
   ]},
  "FMCG has its own gentle set of metrics. [pause] "
  "The first, and the one that separates the real from the illusory, is volume growth — the growth in actual units sold, not the value inflated by price hikes. A company can grow sales value by raising prices while selling fewer packs — that is not healthy. Always look for real volume growth. [pause] "
  "The second is the rural-versus-urban split. Rural India is roughly a third of FMCG sales, and its ups and downs — driven by the monsoon and farm income — swing the whole sector. [pause] "
  "The third is gross margin. Input costs like palm oil and crude-derived packaging drive margins, and a company's pricing power — its ability to pass on cost rises without losing customers — is what protects them. [pause] "
  "The fourth is the moat itself — a vast distribution network reaching millions of tiny stores, plus premiumisation, as customers trade up to fancier products. Those are the sector's real growth levers."),
 ("m_tech", "sm_iconcards",
  {"kicker": "TECHNICAL ANALYSIS", "title": "Reading FMCG on the chart", "color": C,
   "items": [
    {"emoji": "📈", "k": "Nifty FMCG", "v": "The sector index — usually a smooth, low-volatility trend", "chip": "Index"},
    {"emoji": "🛡️", "k": "Defensive rotation", "v": "Outperforms when markets get scared — a 'flight to safety' signal", "chip": "Safe haven"},
    {"emoji": "🌧️", "k": "Monsoon & rural cues", "v": "A good monsoon lifts rural demand hopes — a recurring seasonal driver", "chip": "Seasonal"},
    {"emoji": "🐌", "k": "Low beta", "v": "Moves less than the market — gentle trends, not sharp swings", "chip": "Stable"},
   ]},
  "On the chart, FMCG is the calmest sector of all. [pause] "
  "Track the Nifty FMCG index, which usually traces a smooth, low-volatility trend rather than wild swings. [pause] "
  "Its key technical role is as a defensive. When markets get scared and money flees risk, FMCG tends to outperform — so its relative strength rising versus the Nifty is a classic flight-to-safety signal that tells you something about the whole market's mood. [pause] "
  "Watch the seasonal cues — a good monsoon forecast lifts hopes for rural demand and can move the sector. [pause] "
  "And understand its low beta — it moves less than the market in both directions. That means gentle trends, smaller drawdowns, and a place to hide, not a place for fireworks."),
 ("m_strat", "sm_iconcards",
  {"kicker": "STRATEGIES", "title": "Strategies for FMCG", "color": G,
   "items": [
    {"emoji": "🌳", "k": "Steady compounders", "v": "Own the market-leading brands for slow, reliable long-term compounding", "chip": "Hold"},
    {"emoji": "📉", "k": "Buy input-cost dips", "v": "When rising input costs dent margins & the stock, quality names can be accumulated", "chip": "Contrarian"},
    {"emoji": "✨", "k": "Premiumisation plays", "v": "Favour firms riding the trade-up to premium products & new categories", "chip": "Growth"},
    {"emoji": "🛡️", "k": "Portfolio ballast", "v": "Use FMCG to steady a portfolio — it cushions the fall when cyclicals drop", "chip": "Defence"},
   ]},
  "How do you play FMCG? Four gentle strategies. [pause] "
  "First, simply own the steady compounders — the market-leading brands with unbreakable distribution — for slow, reliable, long-term compounding. This is a buy-and-hold sector by nature. [pause] "
  "Second, buy the input-cost dip. When commodity costs rise and temporarily dent margins, a quality FMCG stock may fall — and that fear can be a fine accumulation point, because the costs eventually normalise. [pause] "
  "Third, favour the premiumisation plays — the firms riding India's trade-up, as consumers move to premium products and new categories. That's where the faster growth hides in a slow sector. [pause] "
  "Fourth, use FMCG as portfolio ballast. Its job in your portfolio is to steady the ship — to cushion the fall when cyclicals like autos and metals drop. [pause] "
  "The one thing to always respect here is the price you pay."),
 ("m_check", "sm_checklist",
  {"kicker": "HOW TO EVALUATE", "title": "Evaluating an FMCG stock — checklist", "color": G, "icon": "✅",
   "items": [
    "Look at VOLUME growth, not just value/sales growth",
    "Check rural vs urban demand trends",
    "Watch gross margins & the company's pricing power",
    "Assess distribution reach & premiumisation runway",
    "Compare valuation (P/E) to its own history — don't overpay",
   ]},
  "Let's turn FMCG into a checklist. Five steps. [pause] "
  "Step one — look at volume growth, the real units sold, not just value or sales growth that can be inflated by price hikes. [pause] "
  "Step two — check the rural-versus-urban demand trends, since rural swings the sector. [pause] "
  "Step three — watch gross margins and, above all, the company's pricing power — its ability to pass on cost rises. [pause] "
  "Step four — assess the distribution reach and the premiumisation runway, the two real growth levers. [pause] "
  "Step five — and always compare the valuation to the company's own history, so you don't overpay for the comfort of a defensive. In FMCG, the business is usually great; the entry price is what you must get right. [pause] "
  "Now, the quiet traps."),
 ("m_risk", "sm_myths",
  {"kicker": "WHAT TO AVOID", "title": "FMCG sector — the risks", "mythLabel": "✗ TRAP", "factLabel": "✓ REALITY",
   "pairs": [
    {"m": "It's safe, so any price is fine", "f": "FMCG trades at rich P/E — overpaying caps returns for years"},
    {"m": "Sales value is up, so it's growing", "f": "Check VOLUME — value can rise on price hikes while units shrink"},
    {"m": "Defensives never fall", "f": "They fall less, but a stretched premium stock can still de-rate"},
   ]},
  "Now the quiet traps in FMCG. [pause] "
  "The first, and the big one — assuming that because the sector is safe, any price is worth paying. FMCG leaders trade at rich price-to-earnings multiples, and if you overpay, your returns can be flat for years even as the business does fine. Safety is not the same as a good entry price. [pause] "
  "The second — celebrating rising sales value without checking volumes. As we said, value can climb on price hikes while units actually shrink. Always look under the hood at volume growth. [pause] "
  "The third — believing defensives never fall. They fall less than cyclicals, yes, but a stretched, premium-priced FMCG stock can still de-rate meaningfully when its lofty valuation corrects. [pause] "
  "Own the quality, but never overpay for the comfort."),
 ("m_recap", "sm_recap",
  {"title": "FMCG sector — recap",
   "items": [
    "Volume growth is the #1 metric — not value",
    "Rural/urban split, gross margins, distribution moat",
    "The great defensive — low beta, flight-to-safety",
    "Strategy: steady compounders; buy input-cost dips",
    "Biggest risk: overpaying for a rich valuation",
   ],
   "closer": "Great businesses — just never overpay for calm."},
  "FMCG, in one breath. [pause] "
  "Volume growth is the number-one metric — real units, not price-inflated value. [pause] "
  "Watch the rural-urban split, gross margins, and the distribution moat. [pause] "
  "It's the great defensive — low beta and a flight-to-safety haven when markets wobble. [pause] "
  "In strategy, own the steady compounders and buy the input-cost dips, but never forget the one real risk: overpaying for the comfort of a rich valuation. [pause] "
  "Next, the deepest cyclical of all — metals."),
 ],

 # ============================== METALS ==============================
 "met": [
 ("me_title", "sm_ptitle",
  {"title": "How to Analyse Metal Stocks", "sub": "Metals & mining · fundamentals · technicals · strategies", "kicker": "SECTOR DEEP-DIVE · METALS"},
  "The metals and mining sector — steel, aluminium, copper, zinc. The most cyclical corner of the entire market. [pause] "
  "These companies don't really control their own destiny. Their fortunes are set by global commodity prices, by China, and by the US dollar. [pause] "
  "Get the cycle right and metals can multiply your money; get it wrong and they can halve it. Timing is everything here. [pause] "
  "Let's learn the fundamentals, technicals, and strategies for this high-risk, high-reward sector."),
 ("me_overview", "sm_iconcards",
  {"kicker": "SUB-SECTORS", "title": "Ferrous, non-ferrous & mining", "color": R,
   "items": [
    {"emoji": "🏗️", "k": "Ferrous (steel)", "v": "The biggest piece — driven by construction, autos & infrastructure", "chip": "Steel"},
    {"emoji": "🔌", "k": "Non-ferrous", "v": "Aluminium, copper, zinc — global, LME-priced, electrification-linked", "chip": "Base metals"},
    {"emoji": "⛏️", "k": "Mining", "v": "Coal, iron-ore & ore producers — feed the metal-makers; policy-sensitive", "chip": "Ore"},
    {"emoji": "🔗", "k": "Integrated vs converters", "v": "Own the ore (low cost, safer) vs buy it (higher cost, more cyclical)", "chip": "Cost edge"},
   ]},
  "First, split metals into its pieces. [pause] "
  "The biggest is ferrous — steel — driven by construction, autos, and infrastructure, and closely tied to India's own capex story. [pause] "
  "Then there's non-ferrous — aluminium, copper, and zinc — which are global, priced on the London Metal Exchange, and increasingly linked to electrification and the energy transition. [pause] "
  "There's mining — the coal, iron-ore, and ore producers who feed the metal-makers, and who are especially sensitive to government policy. [pause] "
  "And a crucial distinction cuts across all of it: integrated producers who own their own ore have a low-cost, safer position, while converters who buy their raw material are higher-cost and far more cyclical. [pause] "
  "That cost position, as we'll see, decides who survives the cycle."),
 ("me_drivers", "sm_iconcards",
  {"kicker": "WHAT MOVES METALS", "title": "The forces that drive the sector", "color": C,
   "items": [
    {"emoji": "🇨🇳", "k": "China", "v": "The world's largest producer & consumer — its demand & output rule prices", "chip": "China"},
    {"emoji": "🌍", "k": "LME / global prices", "v": "Metals are globally priced — domestic realisations follow LME with a lag", "chip": "Prices"},
    {"emoji": "💵", "k": "US dollar", "v": "Commodities are priced in dollars — a strong dollar often pressures metals", "chip": "USD"},
    {"emoji": "🏛️", "k": "Domestic capex", "v": "India's infrastructure & construction demand gives steel a structural floor", "chip": "India"},
   ]},
  "What drives metals? Four forces, almost all global. [pause] "
  "The first, and the giant, is China — the world's largest producer and consumer of metals. Its demand and its output policy rule global prices more than anything else. When China stimulates, metals soar; when it slows or dumps, they crash. [pause] "
  "The second is LME and global prices — metals are priced worldwide, and Indian producers' realisations simply follow the London Metal Exchange with a short lag. [pause] "
  "The third is the US dollar. Because commodities are priced in dollars, a strong dollar often pushes metal prices down, and vice versa. [pause] "
  "The fourth, and the one bright domestic spot, is India's own capex — the infrastructure and construction boom that gives steel demand a structural floor beneath the global cycle. [pause] "
  "Now, the metrics for analysing a metal company."),
 ("me_fund", "sm_iconcards",
  {"kicker": "FUNDAMENTALS · CORE", "title": "The metrics unique to metals", "color": R,
   "items": [
    {"emoji": "🌍", "k": "Global prices (LME)", "v": "LME copper, aluminium & steel prices set the revenue ceiling — track them weekly", "chip": "Prices"},
    {"emoji": "🏭", "k": "Cost per tonne", "v": "The lowest-cost producer wins every cycle — cheap production survives the downturn", "chip": "Cost"},
    {"emoji": "⚖️", "k": "EBITDA per tonne", "v": "Compares true profitability across firms, stripping out leverage differences", "chip": "Profit"},
    {"emoji": "🏋️", "k": "Net debt / EBITDA", "v": "Deadly at the cycle bottom — high debt + collapsing profit can sink a company", "chip": "Debt"},
   ]},
  "Metals have their own hard-edged metrics. [pause] "
  "The first is global prices, set on the London Metal Exchange, the LME. Copper, aluminium, and steel prices there set the revenue ceiling for Indian producers, whose realisations follow with a week or two lag. Track the LME weekly — it matters more than any domestic factor. [pause] "
  "The second is cost per tonne. In a commodity business, everyone sells at the same market price, so the lowest-cost producer wins every single cycle — because when prices crash, the cheap producer survives while the expensive one bleeds. [pause] "
  "The third is EBITDA per tonne — profit per unit of metal — which lets you compare true operating profitability across companies, stripping out their different debt levels. [pause] "
  "The fourth, and the one that kills, is net debt to EBITDA. A debt load that looks fine at the top of the cycle becomes lethal at the bottom, when profits collapse but the debt remains. In metals, debt is the difference between survival and ruin."),
 ("me_tech", "sm_iconcards",
  {"kicker": "TECHNICAL ANALYSIS", "title": "Reading metals on the chart", "color": C,
   "items": [
    {"emoji": "📈", "k": "Nifty Metal", "v": "The sector index — highly volatile, moves in big cyclical waves", "chip": "Index"},
    {"emoji": "🇨🇳", "k": "China & LME cues", "v": "China's demand & output, and LME prices, drive the sector — watch global, not local", "chip": "Global"},
    {"emoji": "💵", "k": "Dollar link", "v": "Commodities are priced in dollars — dollar strength often pressures metals", "chip": "USD"},
    {"emoji": "🌊", "k": "Big cyclical swings", "v": "Trends in long waves — great for cycle timing, punishing if you chase the top", "chip": "Cyclical"},
   ]},
  "On the chart, metals move in dramatic, sweeping waves. [pause] "
  "Track the Nifty Metal index, one of the most volatile sector indices, which trends in big cyclical swings rather than gentle drifts. [pause] "
  "Its drivers are almost entirely global. China's steel output and its export policy, plus LME commodity prices, move these stocks more than anything happening in India. So you analyse metals with your eyes on China and the world, not on domestic news. [pause] "
  "Watch the dollar link too — commodities are priced in dollars, so a strong dollar often pressures metal prices, and therefore metal stocks. [pause] "
  "Those big cyclical swings are a gift for patient cycle-timers and a trap for anyone who chases a vertical rally at the top."),
 ("me_strat", "sm_iconcards",
  {"kicker": "STRATEGIES", "title": "Strategies for metals", "color": G,
   "items": [
    {"emoji": "🔄", "k": "Buy low in the cycle", "v": "Accumulate when metals are hated & prices are depressed — sell into the boom", "chip": "Cycle"},
    {"emoji": "🏭", "k": "Own the low-cost king", "v": "The lowest-cost producer with low debt survives every downturn — own it", "chip": "Survivor"},
    {"emoji": "🧺", "k": "Diversified vs pure-play", "v": "Diversified miners are steadier; single-metal names are higher-beta bets", "chip": "Risk"},
    {"emoji": "🏛️", "k": "Ride India's capex", "v": "Domestic infrastructure & construction demand supports steel structurally", "chip": "Theme"},
   ]},
  "How do you play the deepest cyclical of all? Four strategies. [pause] "
  "First, and most important — buy low in the cycle. Accumulate metals when they are hated, when prices are depressed and headlines are grim, and sell into the boom when everyone loves them. This is the opposite of what feels comfortable, and it's exactly right. [pause] "
  "Second, own the low-cost king. The lowest-cost producer, carrying low debt, survives every downturn and thrives in every upturn. In a commodity business, the cheapest and safest operator is the one to hold. [pause] "
  "Third, choose your risk level — a diversified miner across several metals is steadier, while a single-metal pure-play is a higher-beta bet on one commodity's price. [pause] "
  "Fourth, ride the structural theme — India's own infrastructure and construction boom provides a steady floor of domestic demand for steel, softening the global cycle's blows. [pause] "
  "In metals, buy fear and sell greed, and always mind the debt."),
 ("me_check", "sm_checklist",
  {"kicker": "HOW TO EVALUATE", "title": "Evaluating a metal stock — checklist", "color": G, "icon": "✅",
   "items": [
    "Start with the LME price trend & China demand",
    "Find the lowest cost-per-tonne producer (the survivor)",
    "Compare EBITDA per tonne across companies",
    "Stress-test net debt/EBITDA at cycle-BOTTOM prices",
    "Buy when hated & cheap; never chase the price peak",
   ]},
  "Let's make metals a checklist. Five steps. [pause] "
  "Step one — start with the big picture: the LME price trend and China's demand, because these set the sector's fate. [pause] "
  "Step two — find the lowest cost-per-tonne producer, the one that survives every downturn. [pause] "
  "Step three — compare EBITDA per tonne across companies to see who is genuinely more profitable, stripping out leverage. [pause] "
  "Step four — and this is vital — stress-test the net-debt-to-EBITDA ratio using cycle-bottom prices, not today's. Ask: could this company survive if metal prices halved? [pause] "
  "Step five — buy when the sector is hated and cheap, and never chase a euphoric price peak. In metals, your entry point in the cycle is almost everything. [pause] "
  "Now, the severe cyclical traps."),
 ("me_risk", "sm_myths",
  {"kicker": "WHAT TO AVOID", "title": "Metals sector — the risks", "mythLabel": "✗ TRAP", "factLabel": "✓ REALITY",
   "pairs": [
    {"m": "Metal prices are soaring — buy now!", "f": "Buying at the price peak locks in compressed future margins"},
    {"m": "Low P/E metal stock = cheap", "f": "Cyclicals show low P/E at the TOP; use price-to-book & the cycle instead"},
    {"m": "High debt is fine, profits are huge", "f": "At the cycle bottom, that debt can bankrupt the company"},
   ]},
  "Now the cyclical traps in metals — and they are severe. [pause] "
  "The first — buying because metal prices are soaring and profits are gushing. Buying at the price peak means buying compressed future margins, because prices will eventually mean-revert down. The best time to buy is when prices are low, not high. [pause] "
  "The second — the classic cyclical illusion of a low price-to-earnings. Metal stocks show their lowest P E right at the top, when earnings are peaking. Don't be fooled — judge them by price-to-book and by where you are in the cycle, not by P E. [pause] "
  "The third — dismissing high debt because current profits are huge. At the top of the cycle, that debt looks harmless. At the bottom, when EBITDA collapses, the same debt can bankrupt the company. Debt is the number-one killer in this sector. [pause] "
  "Buy low, own the low-cost survivor, and fear leverage — that is how you win in metals."),
 ("me_recap", "sm_recap",
  {"title": "Metals sector — recap",
   "items": [
    "LME prices & China set the revenue — track global",
    "Cost per tonne & EBITDA per tonne — lowest cost wins",
    "Net debt/EBITDA is deadly at the cycle bottom",
    "Deep cyclical: buy low & hated, sell high & loved",
    "Trap: low P/E and record profits at the PEAK",
   ],
   "closer": "In metals, buy the fear — never the euphoria."},
  "Metals, gathered up. [pause] "
  "Global LME prices and China set the revenue, so you track the world, not India. [pause] "
  "Cost per tonne and EBITDA per tonne reveal the real winner — the lowest-cost producer — and net debt is deadly at the cycle bottom. [pause] "
  "It's the deepest cyclical of all: buy when metals are low and hated, sell when they're high and loved. [pause] "
  "And never fall for the trap of a low price-to-earnings at the peak. In metals, buy the fear, never the euphoria. [pause] "
  "Next, energy — oil, gas, and power."),
 ],

 # ============================== ENERGY / OIL & GAS + POWER ==============================
 "ene": [
 ("e_title", "sm_ptitle",
  {"title": "How to Analyse Energy Stocks", "sub": "Oil, gas & power · fundamentals · technicals · strategies", "kicker": "SECTOR DEEP-DIVE · ENERGY"},
  "The energy sector — oil, gas, and power. The fuel that runs the entire economy. [pause] "
  "It is not one business but several very different ones, from drilling crude out of the ground to selling petrol at the pump to generating electricity. [pause] "
  "Each sub-sector has its own economics, its own metrics, and its own relationship with the price of crude oil. [pause] "
  "This is a detailed sector, so we'll take it carefully — the sub-sectors, the fundamentals, the technicals, and the strategies. Company names are examples only."),
 ("e_overview", "sm_iconcards",
  {"kicker": "SUB-SECTORS", "title": "Energy is really four businesses", "color": M,
   "items": [
    {"emoji": "🛢️", "k": "Upstream (E&P)", "v": "Explorers & producers like ONGC — they profit when crude prices are HIGH", "chip": "Producers"},
    {"emoji": "⛽", "k": "OMCs (downstream)", "v": "BPCL, HPCL, IOC — refine & sell fuel; they benefit when crude is LOW/soft", "chip": "Refiners"},
    {"emoji": "🔥", "k": "Gas", "v": "Gas transmission & city-gas distribution — volume-and-tariff businesses", "chip": "Gas"},
    {"emoji": "⚡", "k": "Power & utilities", "v": "Generators, transmission, renewables — steady, regulated, capex-heavy", "chip": "Power"},
   ]},
  "The first thing to understand about energy is that it is really four different businesses, and they don't move together. [pause] "
  "The first is upstream — the explorers and producers, like ONGC, who pull crude oil and gas out of the ground. Crucially, they profit when crude prices are high. [pause] "
  "The second is the oil marketing companies, the downstream refiners like BPCL, HPCL, and IOC. They buy crude, refine it, and sell you petrol and diesel. And here's the twist — they generally benefit when crude is low or soft, because their margins expand. So upstream and downstream are almost mirror images. [pause] "
  "The third is gas — the pipelines and city-gas distributors, which are really volume-and-tariff businesses, steadier than oil. [pause] "
  "The fourth is power and utilities — the electricity generators, transmission companies, and the fast-growing renewables. These are steady, often regulated, and very capital-heavy. [pause] "
  "Because they behave so differently, you must always know which sub-sector a stock belongs to before you analyse it."),
 ("e_drivers", "sm_iconcards",
  {"kicker": "WHAT MOVES ENERGY", "title": "The forces that drive the sector", "color": C,
   "items": [
    {"emoji": "🌍", "k": "Crude oil price", "v": "The master variable — helps upstream, hurts OMCs; watch Brent & OPEC", "chip": "Crude"},
    {"emoji": "🏛️", "k": "Government policy", "v": "Fuel pricing, subsidies, taxes — the state heavily influences OMC economics", "chip": "Policy"},
    {"emoji": "💵", "k": "USD & imports", "v": "India imports most of its oil in dollars — a weak rupee raises the import bill", "chip": "Forex"},
    {"emoji": "🔋", "k": "Energy transition", "v": "The long shift to renewables & EVs — an opportunity for power, a risk for oil", "chip": "Long-term"},
   ]},
  "What moves the energy sector? Four big forces. [pause] "
  "The master variable is the price of crude oil. It helps upstream producers and hurts oil marketing companies, so a single crude move sends different energy stocks in opposite directions. Watch Brent crude and OPEC decisions closely. [pause] "
  "The second is government policy. Because fuel touches every citizen, the state heavily influences it — through fuel pricing, subsidies, and taxes. This political layer makes OMC earnings less predictable than a normal business. [pause] "
  "The third is the dollar and the import bill. India imports most of its oil, priced in dollars, so a weak rupee raises the cost of that oil and pressures the whole economy, not just the sector. [pause] "
  "The fourth is the long energy transition — the multi-decade shift to renewables and electric vehicles. This is a structural opportunity for the power and renewables sub-sector, and a slow, long-term risk hanging over oil. [pause] "
  "Now, the metrics that let you value these businesses."),
 ("e_fund", "sm_iconcards",
  {"kicker": "FUNDAMENTALS · OMCs", "title": "The metrics for refiners (OMCs)", "color": G,
   "items": [
    {"emoji": "🏭", "k": "GRM", "v": "Gross Refining Margin — profit per barrel refined. In Q3FY26 it jumped to ~$10 from ~$3", "chip": "Refining"},
    {"emoji": "⛽", "k": "Marketing margin", "v": "Profit on selling fuel — squeezed when crude rises but pump prices are held", "chip": "Retail"},
    {"emoji": "📦", "k": "Inventory gain/loss", "v": "Rising crude = paper inventory gains; falling crude = losses. Adjust for it", "chip": "One-off"},
    {"emoji": "🏷️", "k": "Cheap valuation", "v": "OMCs trade at low P/E (~6–7x) & high dividends — a value/cyclical profile", "chip": "Value"},
   ]},
  "Let's take the oil marketing companies first, because they're the most-watched and the trickiest. Four metrics. [pause] "
  "The first is the Gross Refining Margin, the GRM — the profit a refiner makes on each barrel it processes. It swings a lot: for the public-sector OMCs it jumped to around ten dollars a barrel in the third quarter of financial year twenty twenty-six, up from just over three the quarter before. A fat GRM lifts profits fast. [pause] "
  "The second is the marketing margin — the profit on actually selling the fuel. This gets squeezed when crude rises but the government holds pump prices steady, which is a recurring worry. [pause] "
  "The third is inventory gain or loss. Because OMCs hold huge stocks of crude, a rising crude price creates paper inventory gains and a falling price creates losses — so you must strip these one-offs out to see the true, underlying earnings. [pause] "
  "The fourth is valuation. OMCs typically trade at low price-to-earnings, around six to seven times, with generous dividends — a classic value and cyclical profile. That cheapness is partly the political uncertainty."),
 ("e_fund2", "sm_compare3",
  {"kicker": "FUNDAMENTALS · THE REST", "title": "Upstream, gas & power — what to check",
   "cols": [
    {"name": "Upstream", "color": M, "emoji": "🛢️", "rows": [
     {"k": "Key driver", "v": "crude realisation per barrel"},
     {"k": "Watch", "v": "output volumes, reserves"},
     {"k": "Profits when", "v": "crude is HIGH"},
     {"k": "Valuation", "v": "cheap, high dividend"}]},
    {"name": "Gas", "color": C, "emoji": "🔥", "hi": True, "rows": [
     {"k": "Key driver", "v": "volumes + tariff/margin per unit"},
     {"k": "Watch", "v": "volume growth, gas prices"},
     {"k": "Profits when", "v": "volumes & spreads grow"},
     {"k": "Valuation", "v": "steadier, re-rating story"}]},
    {"name": "Power", "color": G, "emoji": "⚡", "rows": [
     {"k": "Key driver", "v": "capacity, PLF, tariffs"},
     {"k": "Watch", "v": "debt, receivables, capex"},
     {"k": "Profits when", "v": "demand & capacity rise"},
     {"k": "Valuation", "v": "regulated, asset-heavy"}]},
   ]},
  "Now the other three sub-sectors, each with its own scorecard. [pause] "
  "For upstream producers, the key driver is the crude realisation — the price they get per barrel — so you watch output volumes and reserves, and you remember they profit when crude is high. Like OMCs, they're usually cheap with high dividends. [pause] "
  "For gas companies, it's a volumes-plus-margin story — how much gas they move and the tariff or spread they earn per unit. You watch volume growth and gas prices. These are steadier businesses, often with a re-rating angle as India's gas usage grows. [pause] "
  "For power and utilities, the drivers are installed capacity, the plant load factor — how fully the plants run — and tariffs. Because these are hugely capital-intensive, you watch debt, receivables from state distribution companies, and the capex plan. They're regulated, asset-heavy, and steady. [pause] "
  "Four sub-sectors, four different scorecards — that's the essence of analysing energy."),
 ("e_check", "sm_checklist",
  {"kicker": "HOW TO EVALUATE", "title": "Evaluating an energy stock — checklist", "color": G, "icon": "✅",
   "items": [
    "Identify the sub-sector first (upstream / OMC / gas / power)",
    "For OMCs: GRM + marketing margin, adjusted for inventory swings",
    "Map the stock's crude sensitivity — helped or hurt by high crude?",
    "Check debt & receivables (critical for power utilities)",
    "Weigh the low valuation against policy & transition risk",
   ]},
  "Let's turn all of that into a practical checklist you can actually use on an energy stock. Five steps. [pause] "
  "Step one — identify the sub-sector before anything else. Is it an upstream producer, an oil marketing company, a gas business, or a power utility? Everything flows from that. [pause] "
  "Step two — if it's an OMC, look at the gross refining margin and the marketing margin together, and adjust the reported profit for those crude-driven inventory swings, so you see the real earnings. [pause] "
  "Step three — map the stock's crude sensitivity. Ask plainly: does this company get helped or hurt when crude rises? That single answer tells you how to trade the oil price. [pause] "
  "Step four — check debt and receivables, which is absolutely critical for the capital-heavy power utilities that are owed money by state distributors. [pause] "
  "Step five — weigh the tempting low valuation against the real risks — government policy interference and the slow, long-term energy transition. Cheap for a reason is a recurring theme here. [pause] "
  "Run that checklist, and you can analyse any energy name."),
 ("e_tech", "sm_iconcards",
  {"kicker": "TECHNICAL ANALYSIS", "title": "Reading energy on the chart", "color": C,
   "items": [
    {"emoji": "📈", "k": "Nifty Energy / Oil & Gas", "v": "The sector indices — track trend & relative strength", "chip": "Index"},
    {"emoji": "🛢️", "k": "Overlay crude", "v": "Put Brent on the chart — but remember it's inverse for OMCs, direct for producers", "chip": "Crude"},
    {"emoji": "🗓️", "k": "Policy & results", "v": "Fuel-price decisions, subsidy news & GRM at results drive the moves", "chip": "Events"},
    {"emoji": "🛡️", "k": "Defensive tilt", "v": "Utilities & city-gas can act defensively; oil is more cyclical", "chip": "Mixed"},
   ]},
  "The technicals for energy demand that you think in sub-sectors even on the chart. [pause] "
  "Track the Nifty Energy and Nifty Oil and Gas indices for the broad trend and relative strength. [pause] "
  "Overlay Brent crude on your chart — but interpret it correctly. Rising crude is bullish for upstream producers and bearish for OMCs, so the same crude line means opposite things for different stocks. Never apply it blindly to the whole sector. [pause] "
  "Watch the event catalysts — government fuel-pricing decisions, subsidy announcements, and the GRM number at quarterly results. These, not chart patterns alone, drive the big moves. [pause] "
  "And note the split personality: power utilities and city-gas distributors can behave defensively, holding up in weak markets, while oil is far more cyclical. So the sector's relative strength depends on which sub-sector is leading."),
 ("e_strat", "sm_iconcards",
  {"kicker": "STRATEGIES", "title": "Strategies for energy", "color": G,
   "items": [
    {"emoji": "⛽", "k": "OMCs on soft crude", "v": "When crude falls & stays soft, OMC margins & re-rating can be a strong play", "chip": "Cyclical"},
    {"emoji": "💵", "k": "Dividend harvest", "v": "Upstream & OMCs pay big dividends — a steady income play at cheap valuations", "chip": "Income"},
    {"emoji": "⚡", "k": "Power & renewables theme", "v": "India's rising power demand + green shift — a structural, multi-year growth play", "chip": "Growth"},
    {"emoji": "🔥", "k": "City-gas re-rating", "v": "Volume-growth gas distributors offer steadier, less crude-driven upside", "chip": "Steady"},
   ]},
  "So how do you play energy? Four strategies, one per angle. [pause] "
  "First, the OMC cyclical play — when crude oil falls and stays soft, refining and marketing margins expand, and these cheap stocks can re-rate strongly. Time it with the crude cycle. [pause] "
  "Second, the dividend harvest. Upstream producers and OMCs pay some of the market's biggest dividends at very low valuations, making them a genuine income play for patient investors — you get paid well to wait. [pause] "
  "Third, the structural growth play — power and renewables. India's electricity demand keeps rising, and the green-energy shift is a multi-year theme, so well-run power and renewable companies offer real long-term growth. [pause] "
  "Fourth, the city-gas re-rating story — gas distributors growing volumes offer steadier upside that is far less hostage to the crude price. [pause] "
  "Match the strategy to the sub-sector, and energy offers something for both the income-seeker and the growth-investor."),
 ("e_risk", "sm_myths",
  {"kicker": "WHAT TO AVOID", "title": "Energy sector — the risks", "mythLabel": "✗ TRAP", "factLabel": "✓ REALITY",
   "pairs": [
    {"m": "Crude is rising — buy all energy stocks", "f": "Rising crude HELPS producers but HURTS OMCs — know which you hold"},
    {"m": "OMCs are super cheap, so a steal", "f": "Cheap reflects policy risk — governments can hold pump prices & squeeze margins"},
    {"m": "Oil is forever — ignore the transition", "f": "The long shift to renewables & EVs is a real structural headwind for oil"},
   ]},
  "Now the traps in energy — and they catch people who treat it as one sector. [pause] "
  "The first — hearing that crude is rising and buying all energy stocks. Rising crude helps the producers but hurts the oil marketing companies, so a blanket bet on the sector is half right and half wrong. Always know which side of crude your stock sits on. [pause] "
  "The second — buying OMCs purely because they look super cheap. That cheapness reflects genuine policy risk: when crude spikes, governments often force OMCs to hold pump prices steady, crushing their marketing margins. The low valuation is partly a warning. [pause] "
  "The third — assuming oil demand is forever and ignoring the energy transition. The multi-decade shift to renewables and electric vehicles is a slow but real structural headwind for oil, and a tailwind for power. Don't ignore the long game. [pause] "
  "Know your sub-sector, respect the policy risk, and energy rewards the careful."),
 ("e_recap", "sm_recap",
  {"title": "Energy sector — recap",
   "items": [
    "Four businesses: upstream, OMCs, gas, power — they differ",
    "Crude HELPS producers, HURTS OMCs — opposite reactions",
    "OMCs: GRM + marketing margin, adjust for inventory swings",
    "Cheap valuations reflect policy + transition risk",
    "Strategy: OMCs on soft crude; dividends; power/renewables growth",
   ],
   "closer": "In energy, always ask: which side of crude am I on?"},
  "Energy, gathered up. [pause] "
  "It's four different businesses — upstream producers, oil marketing companies, gas, and power — and they react in opposite ways. [pause] "
  "The master rule: rising crude helps producers and hurts OMCs. For OMCs, read the refining and marketing margins, adjusted for inventory swings. [pause] "
  "The tempting low valuations reflect real policy and transition risk, so cheap is not automatically a bargain. [pause] "
  "In strategy, play OMCs on soft crude, harvest the fat dividends, and ride the structural power-and-renewables growth. Always ask which side of crude you're on. [pause] "
  "Next, the bricks-and-mortar cyclical — real estate."),
 ],

 # ============================== REALTY / INFRASTRUCTURE ==============================
 "rea": [
 ("re_title", "sm_ptitle",
  {"title": "How to Analyse Realty & Infra Stocks", "sub": "Real estate & infrastructure · fundamentals · technicals · strategies", "kicker": "SECTOR DEEP-DIVE · REALTY"},
  "Real estate and infrastructure — the sector that builds the nation, and one of the most cyclical of all. [pause] "
  "Property moves in long, powerful cycles — years of boom followed by years of bust — driven above all by interest rates and incomes. [pause] "
  "It's also a sector where the reported profit can badly mislead you, because of the way long projects are accounted. So you need special metrics. [pause] "
  "We'll cover the sub-sectors, the fundamentals, the technicals, and the strategies in detail. Company names are examples only."),
 ("re_overview", "sm_iconcards",
  {"kicker": "SUB-SECTORS", "title": "Realty & infra — the pieces", "color": V,
   "items": [
    {"emoji": "🏠", "k": "Residential developers", "v": "Build & sell homes — driven by affordability, rates & the property cycle", "chip": "Homes"},
    {"emoji": "🏢", "k": "Commercial / REITs", "v": "Offices & malls; REITs let you own rent-yielding property for income", "chip": "Rent"},
    {"emoji": "🏗️", "k": "Infra / construction (EPC)", "v": "Roads, bridges, projects — order-book businesses driven by govt capex", "chip": "Capex"},
    {"emoji": "🧱", "k": "Building materials", "v": "Cement, tiles, pipes, paints — the 'picks & shovels' of the whole boom", "chip": "Suppliers"},
   ]},
  "Let's start by splitting this broad sector into its pieces. [pause] "
  "First, residential developers, who build and sell homes. They're driven by affordability, interest rates, and the property cycle — this is the classic real-estate stock. [pause] "
  "Second, commercial real estate and REITs. Offices and malls generate rent, and a REIT — a Real Estate Investment Trust — lets you own a slice of that rent-yielding property for regular income, without buying a building. [pause] "
  "Third, infrastructure and construction — the EPC companies that build roads, bridges, and large projects. These are order-book businesses, driven by government capital spending, and they resemble the defence sector in how you analyse them. [pause] "
  "Fourth, building materials — cement, tiles, pipes, and paints. These are the picks-and-shovels of the whole construction boom; they profit whoever wins the projects. [pause] "
  "Four quite different businesses under one roof — and, as always, you analyse each differently."),
 ("re_drivers", "sm_iconcards",
  {"kicker": "WHAT MOVES REALTY", "title": "The forces that drive the sector", "color": C,
   "items": [
    {"emoji": "🏛️", "k": "Interest rates", "v": "The master driver — cheap loans fuel home demand; rate cuts light the fuse", "chip": "Rates"},
    {"emoji": "💼", "k": "Income & jobs", "v": "Rising incomes and IT/urban job growth power housing demand", "chip": "Demand"},
    {"emoji": "🏗️", "k": "Govt capex", "v": "Budget spending on roads & infrastructure drives the EPC & materials side", "chip": "Policy"},
    {"emoji": "🔄", "k": "The long cycle", "v": "Property runs in multi-year up-and-down cycles — timing matters enormously", "chip": "Cyclical"},
   ]},
  "What drives real estate? Four forces, and the first towers over the rest. [pause] "
  "Interest rates are the master driver. A home is usually bought with a loan, so when rates fall, monthly instalments drop and demand ignites; when rates rise, demand cools. A rate-cut cycle is often the fuse that lights a property boom. [pause] "
  "Second, incomes and jobs. Rising salaries and strong urban and IT-sector employment give people the confidence and the means to buy homes. [pause] "
  "Third, government capital spending. The Budget's allocation to roads, railways, and infrastructure directly drives the construction and building-materials side of the sector. [pause] "
  "Fourth, and never to be forgotten — the long cycle. Property doesn't drift; it runs in multi-year waves of boom and bust. Buying near the bottom of that cycle versus near the top can be the difference between doubling your money and halving it. Timing matters enormously here."),
 ("re_fund", "sm_iconcards",
  {"kicker": "FUNDAMENTALS · CORE", "title": "The metrics unique to realty", "color": G,
   "items": [
    {"emoji": "📈", "k": "Pre-sales / bookings", "v": "The #1 metric — the value of homes SOLD this period. Better than reported revenue", "chip": "Demand"},
    {"emoji": "💵", "k": "Collections", "v": "Cash actually received from buyers — the real cash engine of a developer", "chip": "Cash"},
    {"emoji": "🏋️", "k": "Net debt", "v": "Developers can carry heavy debt — deadly in a downturn. Lower is far safer", "chip": "Safety"},
    {"emoji": "🏬", "k": "Launches & inventory", "v": "New project pipeline (future sales) and unsold inventory (overhang risk)", "chip": "Pipeline"},
   ]},
  "Now the metrics that make real estate special — and here, reported profit lies, so we look elsewhere. [pause] "
  "The number-one metric is pre-sales, also called bookings — the total value of homes a developer has actually sold in the period. Because of accounting rules, sold homes may not show up as revenue for years, so pre-sales is a far truer, more current measure of demand than the reported top line. This is the number to watch. [pause] "
  "The second is collections — the cash actually received from home-buyers. This is the real cash engine of a developer; strong collections fund the next project without more debt. [pause] "
  "The third is net debt. Property developers can carry heavy debt, and in a downturn that debt turns deadly, exactly as it does in metals. Lower debt is dramatically safer through the cycle. [pause] "
  "The fourth is the launch pipeline and unsold inventory — new launches signal future sales, while a big pile of unsold inventory signals an overhang that will weigh on prices and cash."),
 ("re_check", "sm_checklist",
  {"kicker": "HOW TO EVALUATE", "title": "Evaluating a realty stock — checklist", "color": G, "icon": "✅",
   "items": [
    "Watch pre-sales/bookings growth — not just reported revenue",
    "Confirm collections are strong (real cash coming in)",
    "Demand low net debt — survivors of the last downturn",
    "Judge the developer's execution & delivery reputation",
    "Read the interest-rate cycle — the sector's master switch",
   ]},
  "Let's make that practical with a checklist for any real-estate stock. Five steps. [pause] "
  "Step one — look at pre-sales, the bookings, and their growth, not the reported revenue, which lags reality by years. Rising bookings mean rising demand. [pause] "
  "Step two — confirm collections are strong, so real cash is flowing in from buyers to fund the business. [pause] "
  "Step three — demand low net debt. Favour the developers who survived the last property downturn with clean balance sheets; they'll survive the next one too and gain share. [pause] "
  "Step four — judge execution. In real estate, a developer's reputation for delivering projects on time and on quality is priceless — buyers pay a premium for trusted names, and so should you. [pause] "
  "Step five — read the interest-rate cycle, the master switch for the whole sector. Are rates rising or falling? That single question frames every real-estate decision. [pause] "
  "That checklist keeps you on the safe side of a treacherous sector."),
 ("re_tech", "sm_iconcards",
  {"kicker": "TECHNICAL ANALYSIS", "title": "Reading realty on the chart", "color": C,
   "items": [
    {"emoji": "📈", "k": "Nifty Realty", "v": "A very high-beta index — huge cyclical swings, big rallies and deep falls", "chip": "Index"},
    {"emoji": "🏛️", "k": "Rate-cut catalyst", "v": "RBI rate cuts are the classic spark for a realty rally — watch policy", "chip": "RBI"},
    {"emoji": "🔄", "k": "Cyclical leadership", "v": "Realty leads early in a rate-cut / recovery cycle, then fades", "chip": "Cycle"},
    {"emoji": "🌊", "k": "Boom-bust waves", "v": "Trends in long waves — reward cycle-timers, punish those who chase the top", "chip": "Volatile"},
   ]},
  "On the chart, real estate is one of the most dramatic sectors there is. [pause] "
  "Track the Nifty Realty index, but respect that it's very high-beta — it delivers enormous rallies and equally deep falls, far more violent than the broad market. [pause] "
  "The classic catalyst is an RBI rate cut, which lowers home-loan costs and is often the spark that ignites a realty rally. So watch the interest-rate policy calendar as your key signal. [pause] "
  "In terms of rotation, realty tends to lead early in a rate-cut or economic-recovery cycle, when cheap money and optimism return, and then to fade as the cycle matures. [pause] "
  "And like metals, it moves in long boom-and-bust waves. That rewards the patient cycle-timer who buys in the gloom, and punishes the latecomer who chases a euphoric top."),
 ("re_strat", "sm_iconcards",
  {"kicker": "STRATEGIES", "title": "Strategies for realty & infra", "color": G,
   "items": [
    {"emoji": "🔄", "k": "Play the property cycle", "v": "Buy quality developers early in a rate-cut cycle; trim as the boom matures", "chip": "Cyclical"},
    {"emoji": "👑", "k": "Own low-debt leaders", "v": "The strongest, low-debt branded developers gain share every cycle", "chip": "Quality"},
    {"emoji": "🏢", "k": "REITs for income", "v": "Prefer steady rental income over developer risk? REITs pay regular yield", "chip": "Income"},
    {"emoji": "🧱", "k": "Picks & shovels", "v": "Cement, pipes, tiles & EPC ride the whole boom with less single-project risk", "chip": "Suppliers"},
   ]},
  "How do you play real estate and infrastructure? Four strategies. [pause] "
  "First, play the property cycle. Buy the quality developers early in a rate-cut cycle, when demand is just reviving, and trim as the boom matures and everyone piles in. Cyclicals reward timing. [pause] "
  "Second, own the low-debt leaders. The strongest, best-capitalised, branded developers gain market share in every cycle — especially after downturns clear out the weak. Quality compounds here. [pause] "
  "Third, if you'd rather have steady income than developer risk, use REITs. They hand you a regular rental yield from commercial property, a calmer way to invest in real estate. [pause] "
  "Fourth, the picks-and-shovels approach — building-materials companies like cement, pipes, and tiles, and the EPC construction firms, ride the entire boom with less exposure to any single project going wrong. [pause] "
  "In this sector, low debt and cycle timing are your two best friends."),
 ("re_risk", "sm_myths",
  {"kicker": "WHAT TO AVOID", "title": "Realty sector — the risks", "mythLabel": "✗ TRAP", "factLabel": "✓ REALITY",
   "pairs": [
    {"m": "Reported profit is strong — it's healthy", "f": "Accounting lags reality — check pre-sales & CASH, not just profit"},
    {"m": "Property only ever goes up", "f": "Realty has brutal multi-year busts — high debt developers can go bust"},
    {"m": "Cheap builder stock = bargain", "f": "Heavy debt + unsold inventory can make 'cheap' a value trap"},
   ]},
  "Now the traps in real estate — and this sector has buried many investors. [pause] "
  "The first — trusting strong reported profit as proof of health. Accounting rules make property profit lag reality by years, so a company can report healthy profits from old projects even as new sales dry up. Always check current pre-sales and cash collections, not just the profit line. [pause] "
  "The second — the dangerous belief that property only ever goes up. Real estate has suffered brutal, multi-year busts, and in those busts, heavily indebted developers have gone bankrupt. This is a cyclical, not a one-way bet. [pause] "
  "The third — buying a builder just because the stock looks cheap. Heavy debt plus a pile of unsold inventory can make a cheap-looking developer a classic value trap that gets cheaper. [pause] "
  "Watch the cash, fear the debt, respect the cycle — and real estate can be hugely rewarding at the right time."),
 ("re_recap", "sm_recap",
  {"title": "Realty & infra — recap",
   "items": [
    "Sub-sectors: residential, commercial/REITs, EPC infra, materials",
    "Interest rates are the master driver — rate cuts spark rallies",
    "Watch pre-sales, collections & net debt — NOT just profit",
    "High-beta cyclical — leads recoveries, brutal busts",
    "Strategy: low-debt leaders, cycle timing, REITs for income",
   ],
   "closer": "In realty, watch the cash and fear the debt."},
  "Real estate and infrastructure, gathered up. [pause] "
  "It spans residential developers, commercial and REITs, infrastructure construction, and building materials — each analysed differently. [pause] "
  "Interest rates are the master driver, and a rate-cut cycle is the classic spark for a rally. [pause] "
  "The key metrics are pre-sales, collections, and net debt — never trust reported profit alone, because accounting lags reality. [pause] "
  "It's a high-beta cyclical with brutal busts, so favour low-debt leaders, time the cycle, and use REITs for income. Watch the cash and fear the debt. [pause] "
  "Next, one of India's best structural stories — specialty chemicals."),
 ],

 # ============================== CHEMICALS ==============================
 "che": [
 ("c_title", "sm_ptitle",
  {"title": "How to Analyse Chemical Stocks", "sub": "Chemicals sector · fundamentals · technicals · strategies", "kicker": "SECTOR DEEP-DIVE · CHEMICALS"},
  "The chemicals sector — one of India's most exciting structural growth stories of the decade. [pause] "
  "As the world diversifies its supply chains away from China — the so-called China-plus-one shift — India's chemical makers are winning global business. [pause] "
  "But 'chemicals' hides two very different worlds — high-quality specialty chemicals and boom-bust commodity chemicals — and confusing them is the biggest mistake investors make. [pause] "
  "We'll cover the sub-sectors, the fundamentals, the technicals, and the strategies in detail. Company names are examples only."),
 ("c_overview", "sm_iconcards",
  {"kicker": "SUB-SECTORS", "title": "Not all chemicals are equal", "color": C,
   "items": [
    {"emoji": "💎", "k": "Specialty chemicals", "v": "Custom, high-value molecules with sticky customers & pricing power — the prize", "chip": "Quality"},
    {"emoji": "🛢️", "k": "Commodity / bulk", "v": "Mass chemicals sold on price alone — cyclical, low-margin, like metals", "chip": "Cyclical"},
    {"emoji": "🌾", "k": "Agrochemicals", "v": "Crop-protection & fertilisers — driven by farm demand and the monsoon", "chip": "Agri"},
    {"emoji": "🧪", "k": "CRAMS / custom synthesis", "v": "Making molecules for global pharma & others — a big China+1 winner", "chip": "Export"},
   ]},
  "The very first thing in chemicals is to realise that not all chemicals are equal — there are several worlds here. [pause] "
  "The first, and the prize, is specialty chemicals — custom, high-value molecules made to a client's exact need. Because they're hard to switch away from, these businesses have sticky customers, pricing power, and fat, stable margins. This is where the great compounders live. [pause] "
  "The second is commodity or bulk chemicals — mass-produced products sold purely on price. These are cyclical and low-margin, and you analyse them almost exactly like metals, watching spreads and the cycle. [pause] "
  "The third is agrochemicals — crop-protection chemicals and fertilisers, driven by farm demand and the monsoon, so they carry a seasonal, rural flavour. [pause] "
  "The fourth is custom synthesis, or CRAMS — making molecules to order for global pharma and other industries. This is one of the biggest China-plus-one winners. [pause] "
  "Specialty and CRAMS are the quality end; commodity is the cyclical end. Never confuse the two."),
 ("c_drivers", "sm_iconcards",
  {"kicker": "WHAT MOVES CHEMICALS", "title": "The forces that drive the sector", "color": V,
   "items": [
    {"emoji": "🌏", "k": "China+1", "v": "The world de-risking away from Chinese supply — India's structural opportunity", "chip": "Structural"},
    {"emoji": "🛢️", "k": "Raw-material costs", "v": "Many inputs are crude-oil derivatives — crude & currency swings hit margins", "chip": "Inputs"},
    {"emoji": "🌍", "k": "Global demand", "v": "Exporters ride global industrial, pharma & agri demand cycles", "chip": "Export"},
    {"emoji": "🇨🇳", "k": "China dumping", "v": "When China floods the market with cheap chemicals, prices & margins crash", "chip": "Risk"},
   ]},
  "What drives the chemicals sector? Four forces — two tailwinds and a big risk. [pause] "
  "The first, and the whole investment thesis, is China-plus-one. As global companies de-risk their supply chains away from an over-concentration in China, India is the natural alternative, winning multi-year contracts. This is a genuine structural tailwind. [pause] "
  "The second is raw-material costs. Many chemical inputs are derived from crude oil, so crude prices and the rupee directly move the sector's margins. Rising input costs squeeze; falling costs relieve. [pause] "
  "The third is global demand. Because these are exporters, they ride the industrial, pharmaceutical, and agricultural demand cycles of the whole world, not just India. [pause] "
  "And the fourth — the big risk — is Chinese dumping. When China, for its own reasons, floods the global market with cheap chemicals, prices and margins can crash, hurting Indian players hardest in the commodity end. That risk never fully goes away."),
 ("c_fund", "sm_iconcards",
  {"kicker": "FUNDAMENTALS · CORE", "title": "The metrics that separate winners", "color": G,
   "items": [
    {"emoji": "💰", "k": "Gross & EBITDA margins", "v": "High, stable margins = specialty (pricing power); thin, swinging = commodity", "chip": "Quality tell"},
    {"emoji": "🔬", "k": "R&D & customer stickiness", "v": "R&D + long-term client relationships = a real, durable moat", "chip": "Moat"},
    {"emoji": "🏭", "k": "Capex & capacity", "v": "Growth needs new plants — watch capex plans and how they'll be funded", "chip": "Growth"},
    {"emoji": "📊", "k": "Return ratios & debt", "v": "High ROCE with controlled debt marks a genuinely great chemicals business", "chip": "Returns"},
   ]},
  "Now the metrics — and in chemicals, they literally tell you whether you're looking at a great business or a cyclical one. [pause] "
  "The first tell is the margin profile. High and stable gross and EBITDA margins signal a specialty business with real pricing power. Thin, wildly swinging margins signal a commodity business at the mercy of the cycle. The margin chart alone often tells you which world you're in. [pause] "
  "The second is R&D spend and customer stickiness. A specialty maker that invests in research and builds long-term, hard-to-replace relationships with global clients has a genuine, durable moat. [pause] "
  "The third is capex and capacity. Growth in this sector requires building new plants, so watch the capital-expenditure plans and, crucially, whether they're funded by internal cash or by piling on debt. [pause] "
  "The fourth is the return ratios and debt. A high return on capital employed alongside controlled debt is the signature of a truly great chemicals company — the kind that compounds for years."),
 ("c_check", "sm_checklist",
  {"kicker": "HOW TO EVALUATE", "title": "Evaluating a chemical stock — checklist", "color": G, "icon": "✅",
   "items": [
    "First classify it: specialty vs commodity vs agrochem",
    "Check margin stability — the tell-tale of pricing power",
    "Look for R&D + sticky global clients (the moat)",
    "Assess capex vs debt — is growth self-funded?",
    "Weigh the China+1 tailwind against China-dumping risk",
   ]},
  "Let's make this a working checklist for any chemical stock. Five steps. [pause] "
  "Step one — classify it first. Is this a specialty maker, a commodity producer, or an agrochemical company? Your entire analysis depends on the answer, because they're valued completely differently. [pause] "
  "Step two — check margin stability over several years. Steady, high margins reveal pricing power and a specialty profile; violent swings reveal a commodity business. [pause] "
  "Step three — look for the moat: real R&D investment and long-standing, sticky relationships with global clients. That's what protects a specialty maker from competition. [pause] "
  "Step four — assess capex against debt. The best growers fund their new plants largely from their own cash flow, rather than borrowing heavily and risking the balance sheet. [pause] "
  "Step five — weigh the two-sided China factor: the powerful China-plus-one tailwind on one hand, and the ever-present risk of Chinese dumping on the other. [pause] "
  "Run that, and you'll separate the compounders from the cyclicals."),
 ("c_tech", "sm_iconcards",
  {"kicker": "TECHNICAL ANALYSIS", "title": "Reading chemicals on the chart", "color": C,
   "items": [
    {"emoji": "📈", "k": "Nifty Chemicals", "v": "A dedicated sector index now exists — track trend & relative strength", "chip": "Index"},
    {"emoji": "💎", "k": "Specialty vs commodity", "v": "Specialty names trend steadily; commodity names swing with the cycle", "chip": "Split"},
    {"emoji": "🛢️", "k": "Crude & currency cues", "v": "Input-cost moves (crude, rupee) and global demand guide the sector", "chip": "Macro"},
    {"emoji": "📊", "k": "Results-driven", "v": "Margin trends at quarterly results are the key catalyst — watch them", "chip": "Results"},
   ]},
  "The technicals for chemicals reflect that same split personality. [pause] "
  "There's now a dedicated Nifty Chemicals index you can track for the sector's trend and relative strength. [pause] "
  "But interpret it knowing the divide: specialty names tend to trend steadily upward, like quality compounders, while commodity chemical names swing with their price cycle, like metals. The index blends both. [pause] "
  "Watch the macro cues that hit input costs — crude oil and the rupee — along with signals of global industrial demand, which together shape margins. [pause] "
  "And above all, this is a results-driven sector on the chart. The margin trend reported each quarter is the key catalyst — margins expanding signals the specialty thesis is working; margins compressing warns of dumping or a cyclical downturn. Trade around those results."),
 ("c_strat", "sm_iconcards",
  {"kicker": "STRATEGIES", "title": "Strategies for chemicals", "color": G,
   "items": [
    {"emoji": "🌳", "k": "Own specialty compounders", "v": "For the long term, hold high-margin specialty leaders with sticky clients", "chip": "Quality"},
    {"emoji": "🌏", "k": "Ride China+1", "v": "Favour exporters & CRAMS players directly winning global de-risking contracts", "chip": "Theme"},
    {"emoji": "🔄", "k": "Trade commodity cyclically", "v": "Treat bulk-chemical names like metals — buy the down-cycle, sell the up", "chip": "Cyclical"},
    {"emoji": "📉", "k": "Buy quality in de-rating", "v": "Great specialty names occasionally get cheap on a scare — a patient entry", "chip": "Contrarian"},
   ]},
  "So how do you play chemicals? Four strategies. [pause] "
  "First, for the long term, own the specialty compounders — the high-margin leaders with sticky global clients and pricing power. These are among the best businesses in the whole market, and you simply hold them. [pause] "
  "Second, ride the China-plus-one theme directly — favour the exporters and custom-synthesis players who are actually winning the contracts as the world de-risks from China. This is the structural growth engine. [pause] "
  "Third, treat the commodity-chemical names exactly like metals — a cyclical trade, where you buy in the down-cycle when prices and margins are depressed, and sell into the up-cycle. [pause] "
  "Fourth, a contrarian entry — even great specialty names occasionally de-rate on a China-dumping scare or a demand wobble. For a genuinely high-quality business, that fear can be a patient long-term opportunity. [pause] "
  "The golden rule: know whether you're holding a compounder or trading a cycle."),
 ("c_risk", "sm_myths",
  {"kicker": "WHAT TO AVOID", "title": "Chemicals sector — the risks", "mythLabel": "✗ TRAP", "factLabel": "✓ REALITY",
   "pairs": [
    {"m": "It's a chemical stock, so it's a China+1 winner", "f": "Only specialty/CRAMS truly win; commodity names are just cyclicals"},
    {"m": "Thin-margin bulk maker at low P/E = cheap", "f": "Commodity chemicals are cyclical — low P/E often marks the peak"},
    {"m": "The structural story means any price is fine", "f": "Quality specialty names can get very expensive — valuation still matters"},
   ]},
  "Now the traps in chemicals — and they come from that specialty-versus-commodity confusion. [pause] "
  "The first trap — assuming any chemical stock is a China-plus-one winner. It isn't. Only the specialty and custom-synthesis players truly benefit from that structural shift. A commodity bulk-chemical maker is just a cyclical, dressed up in the sector's exciting story. [pause] "
  "The second trap — thinking a thin-margin bulk maker on a low price-to-earnings is cheap. Like metals, commodity chemicals show their lowest P E right at the cyclical peak. Don't be fooled. [pause] "
  "The third trap — believing the wonderful structural story justifies any price. The best specialty names can become very expensive, and overpaying even for a great business caps your returns for years. Valuation always matters. [pause] "
  "Separate specialty from commodity, respect valuation, and chemicals offer some of the market's finest compounders."),
 ("c_recap", "sm_recap",
  {"title": "Chemicals sector — recap",
   "items": [
    "Split it: specialty (quality) vs commodity (cyclical) vs agrochem",
    "China+1 is the structural tailwind; dumping is the risk",
    "Margin stability & R&D reveal the specialty compounders",
    "Trade commodity names like metals; hold specialty long-term",
    "Trap: calling every chemical stock a China+1 winner",
   ],
   "closer": "In chemicals, specialty compounds — commodity just cycles."},
  "Chemicals, gathered up. [pause] "
  "Always split the sector: specialty and custom-synthesis are the quality compounders, commodity is a cyclical, and agrochem is seasonal. [pause] "
  "China-plus-one is the powerful structural tailwind, and Chinese dumping is the recurring risk. [pause] "
  "Stable, high margins and real R&D reveal the true specialty winners. [pause] "
  "Hold the specialty compounders for years, trade the commodity names like metals, and never call every chemical stock a China-plus-one winner. [pause] "
  "Finally, the sector of screens and signals — media and telecom."),
 ],

 # ============================== MEDIA & TELECOM ==============================
 "mtl": [
 ("mt_title", "sm_ptitle",
  {"title": "How to Analyse Telecom & Media", "sub": "Telecom, media & digital · fundamentals · technicals · strategies", "kicker": "SECTOR DEEP-DIVE · TELECOM & MEDIA"},
  "Our final sector — telecom and media, the business of connecting and entertaining a billion-plus people. [pause] "
  "Telecom has transformed from a brutal price war into a stable, few-player market with real pricing power returning. [pause] "
  "Media, meanwhile, is being reshaped by streaming and digital, creating both disruption and opportunity. [pause] "
  "We'll cover the sub-sectors, the fundamentals, the technicals, and the strategies in detail. Company names are examples only."),
 ("mt_overview", "sm_iconcards",
  {"kicker": "SUB-SECTORS", "title": "Telecom, media & digital", "color": V,
   "items": [
    {"emoji": "📶", "k": "Telecom operators", "v": "A 3-player market — the network businesses selling data & voice", "chip": "Networks"},
    {"emoji": "🗼", "k": "Telecom infra", "v": "Tower & fibre companies renting infrastructure to the operators", "chip": "Infra"},
    {"emoji": "📺", "k": "Media & broadcasting", "v": "TV, print & film — ad-revenue businesses facing digital disruption", "chip": "Legacy"},
    {"emoji": "🎬", "k": "Digital / OTT / platforms", "v": "Streaming & internet platforms — the fast-growing new-age winners", "chip": "New-age"},
   ]},
  "Let's split this final sector into its parts. [pause] "
  "First, the telecom operators — the network companies selling data and voice. After years of bruising competition, India has consolidated into essentially a three-player market, which changes everything about the economics. [pause] "
  "Second, telecom infrastructure — the tower and fibre companies that rent their infrastructure to those operators, a steadier, rental-style business. [pause] "
  "Third, traditional media and broadcasting — television, print, and film. These are advertising-revenue businesses, and they're squarely in the path of digital disruption. [pause] "
  "Fourth, the digital and OTT platforms — streaming services and internet platforms — the fast-growing new-age winners taking share from the old media. [pause] "
  "So within one sector you have a maturing, cash-generating telecom oligopoly on one side, and a disruptive, fast-changing media-and-digital world on the other."),
 ("mt_drivers", "sm_iconcards",
  {"kicker": "WHAT MOVES THE SECTOR", "title": "The forces at work", "color": C,
   "items": [
    {"emoji": "💵", "k": "ARPU", "v": "Average Revenue Per User — the master telecom metric; tariff hikes lift it", "chip": "Telecom #1"},
    {"emoji": "📈", "k": "Data & 5G", "v": "Rising data use and 5G monetisation drive future telecom revenue", "chip": "Growth"},
    {"emoji": "🤝", "k": "Consolidation", "v": "Fewer players = more pricing power = a healthier, more profitable market", "chip": "Structure"},
    {"emoji": "📱", "k": "The digital shift", "v": "Advertising & viewers moving from TV to streaming — reshapes media", "chip": "Disruption"},
   ]},
  "What drives telecom and media? Four forces. [pause] "
  "For telecom, the master metric is ARPU — Average Revenue Per User, the monthly revenue a company earns from each subscriber. After years of destructive price wars, tariff hikes are finally lifting ARPU, and that is the single most important number to watch in the sector. [pause] "
  "The second driver is data and 5G. Indians consume enormous and growing amounts of mobile data, and the monetisation of 5G networks is the next leg of revenue growth. [pause] "
  "The third is consolidation. With only three big players left, the market has real pricing power again — fewer competitors means a healthier, more profitable industry, which is why telecom is far more investable now than a decade ago. [pause] "
  "The fourth, on the media side, is the digital shift — advertising money and viewers steadily moving from television to streaming. That reshapes who wins and who fades, rewarding the digital platforms and pressuring legacy broadcasters."),
 ("mt_fund", "sm_iconcards",
  {"kicker": "FUNDAMENTALS · TELECOM", "title": "The metrics for telecom", "color": G,
   "items": [
    {"emoji": "💵", "k": "ARPU", "v": "The #1 metric — revenue per subscriber; rising ARPU is the whole bull case", "chip": "Revenue"},
    {"emoji": "👥", "k": "Subscriber trends", "v": "Net adds and, crucially, share of high-value data users", "chip": "Users"},
    {"emoji": "🏋️", "k": "Debt", "v": "Telecom is brutally capital-intensive — spectrum & networks pile on debt", "chip": "Leverage"},
    {"emoji": "📶", "k": "Network capex", "v": "Ongoing 5G & fibre spend — necessary, but it must eventually earn a return", "chip": "Capex"},
   ]},
  "Let's take telecom's fundamentals first. Four metrics. [pause] "
  "The first, again, is ARPU — revenue per subscriber. Rising ARPU is essentially the entire bull case for telecom, because with a fixed subscriber base, every rupee of higher ARPU flows powerfully to profit. Watch it above all. [pause] "
  "The second is subscriber trends — net additions, and, more importantly, the share of high-value data users a company is gaining or losing. Quality of subscribers beats quantity. [pause] "
  "The third, and the sector's great weakness, is debt. Telecom is brutally capital-intensive: buying spectrum and building networks costs staggering sums, so operators carry heavy debt. A stretched balance sheet is the number-one risk here. [pause] "
  "The fourth is network capex — the ongoing spending on 5G and fibre. It's necessary to stay competitive, but you must judge whether that huge investment will eventually earn a proper return, or just burn cash."),
 ("mt_fund_med", "sm_iconcards",
  {"kicker": "FUNDAMENTALS · MEDIA", "title": "The metrics for media", "color": M,
   "items": [
    {"emoji": "📺", "k": "Ad vs subscription", "v": "The revenue mix — ad-dependent media is more cyclical than subscription", "chip": "Mix"},
    {"emoji": "👀", "k": "Viewership / reach", "v": "Audience share drives ad rates — but it's shifting to digital", "chip": "Eyeballs"},
    {"emoji": "🎬", "k": "Content cost", "v": "Streaming's arms race in content can burn cash — watch profitability, not just growth", "chip": "Costs"},
    {"emoji": "📉", "k": "Disruption risk", "v": "Legacy TV & print face structural decline as audiences go digital", "chip": "Decline"},
   ]},
  "Now media's fundamentals, which are quite different. Four things to watch. [pause] "
  "The first is the revenue mix — advertising versus subscription. Advertising revenue is cyclical, rising and falling with the economy, while subscription revenue is steadier and more predictable. A media company leaning on ads is a riskier, more cyclical bet. [pause] "
  "The second is viewership and reach. Audience share is what sets advertising rates — but remember, those eyeballs are steadily shifting from television to digital, so today's viewership can erode. [pause] "
  "The third is content cost. In the streaming era, there's an expensive arms race to produce content, which can burn enormous cash. So judge a streaming or media business on its path to profitability, not just its subscriber growth. Growth that never turns a profit is a trap. [pause] "
  "The fourth is disruption risk. Legacy television and print face a structural, long-term decline as audiences move online. Be very careful buying a cheap-looking legacy media stock that is quietly shrinking."),
 ("mt_check", "sm_checklist",
  {"kicker": "HOW TO EVALUATE", "title": "Evaluating a telecom/media stock — checklist", "color": G, "icon": "✅",
   "items": [
    "Telecom: is ARPU rising, and is debt under control?",
    "Judge subscriber QUALITY (data users), not just quantity",
    "Media: growing subscription revenue vs shrinking ad/legacy?",
    "For streaming: is there a real path to PROFIT, not just growth?",
    "Ask: is this a disruptor or the one being disrupted?",
   ]},
  "Let's turn it into a checklist. Five steps. [pause] "
  "Step one — for a telecom operator, ask the two questions that matter most: is ARPU rising, and is the debt under control? A rising ARPU with falling debt is the ideal setup. [pause] "
  "Step two — judge subscriber quality, not just quantity. Gaining high-value data users is worth far more than adding cheap, low-usage ones. [pause] "
  "Step three — for a media company, check whether steady subscription revenue is growing while cyclical advertising and legacy formats shrink. You want the mix moving the right way. [pause] "
  "Step four — for any streaming or digital business, insist on a credible path to profit, not just endless subscriber growth funded by burning cash. [pause] "
  "Step five — and this frames everything — ask the simple question: is this company a disruptor, or the one being disrupted? In this fast-changing sector, that single distinction often decides your returns. [pause] "
  "Run that, and you can size up any telecom or media name."),
 ("mt_strat", "sm_iconcards",
  {"kicker": "STRATEGIES", "title": "Strategies for telecom & media", "color": G,
   "items": [
    {"emoji": "📶", "k": "Ride the ARPU cycle", "v": "In a 3-player market, rising tariffs & ARPU reward the leading operators", "chip": "Telecom"},
    {"emoji": "🗼", "k": "Tower/infra for stability", "v": "Rental-style infra players offer steadier, less-competitive cash flows", "chip": "Steady"},
    {"emoji": "🎬", "k": "Back the digital winners", "v": "Favour profitable digital & OTT platforms over declining legacy media", "chip": "Growth"},
    {"emoji": "⚠️", "k": "Avoid the debt trap", "v": "Steer clear of weak, over-indebted operators that can't fund 5G", "chip": "Caution"},
   ]},
  "So how do you play telecom and media? Four strategies. [pause] "
  "First, ride the ARPU cycle in telecom. In a healthy three-player market, rising tariffs and ARPU flow straight to the bottom line, richly rewarding the strong, leading operators. This is the core telecom investment case today. [pause] "
  "Second, for steadier exposure, consider the tower and fibre infrastructure players — their rental-style cash flows are calmer and less exposed to the operators' price competition. [pause] "
  "Third, on the media side, back the digital winners — the profitable streaming and internet platforms taking share — over the structurally declining legacy broadcasters. Go with the disruptor. [pause] "
  "Fourth, and defensively, avoid the debt trap — steer well clear of weak, heavily indebted operators that can't afford the 5G investment, because in this capital-hungry sector, they can spiral downward. [pause] "
  "Favour the strong, the profitable, and the disruptors — and avoid the indebted and the disrupted."),
 ("mt_risk", "sm_myths",
  {"kicker": "WHAT TO AVOID", "title": "Telecom & media — the risks", "mythLabel": "✗ TRAP", "factLabel": "✓ REALITY",
   "pairs": [
    {"m": "Millions of subscribers = a great stock", "f": "ARPU & debt matter more; huge users with low ARPU & high debt can bleed"},
    {"m": "Cheap legacy TV/print stock = bargain", "f": "It may be in structural decline — a classic value trap"},
    {"m": "A growing OTT platform must be a winner", "f": "Subscriber growth that never turns a profit destroys value"},
   ]},
  "Finally, the traps in telecom and media. [pause] "
  "The first — being dazzled by a huge subscriber count. Millions of users mean little if the ARPU is low and the debt is high; such an operator can bleed cash despite its size. ARPU and the balance sheet matter far more than raw subscriber numbers. [pause] "
  "The second — buying a cheap-looking legacy television or print stock as a bargain. If its audience is structurally migrating to digital, that low price is a value trap, and the business may simply keep shrinking. [pause] "
  "The third — assuming any fast-growing streaming platform is a winner. Subscriber growth funded by an endless, unprofitable content arms race destroys value rather than creating it. Demand a path to profit. [pause] "
  "Focus on ARPU, debt, and profitable disruption — and this modern sector rewards you."),
 ("mt_recap", "sm_recap",
  {"title": "Telecom & media — recap",
   "items": [
    "Telecom: ARPU is the #1 metric; watch debt & data share",
    "A 3-player market = restored pricing power",
    "Media: subscription > ads; beware legacy decline",
    "Streaming: demand a path to PROFIT, not just growth",
    "Strategy: strong operators, infra, digital winners; avoid debt",
   ],
   "closer": "Back the disruptor — never the disrupted."},
  "Telecom and media, gathered up — and with it, our sector series. [pause] "
  "In telecom, ARPU is the number-one metric, alongside debt and the share of high-value data users, and the new three-player market has restored real pricing power. [pause] "
  "In media, favour subscription revenue over advertising, and beware the structural decline of legacy formats. [pause] "
  "For streaming, always demand a genuine path to profit, not just subscriber growth. [pause] "
  "Back the strong operators, the steady infrastructure, and the profitable digital disruptors — and avoid the indebted and the disrupted. [pause] "
  "And that completes our tour of the market's sectors. Apply this same method — sub-sectors, sector-specific fundamentals, technicals, and strategy — to any sector you ever study. This is education, not investment advice; always do your own research and consult a SEBI-registered adviser. Thank you for watching."),
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
