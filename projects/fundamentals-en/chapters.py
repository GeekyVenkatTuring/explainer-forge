# -*- coding: utf-8 -*-
"""Screenplay for the Fundamental Analysis course (prefix `fa`).

Each chapter: {id, title, segments:[(seg_id, variant, props, narration), ...]}.
Narration = SPOKEN language (numbers as words), [pause] = 0.55s silence. Every
on-screen number is also mentioned. Figures are APPROX FY26 (see build.py header).
ADEPT arc: Analogy → Diagram → Example → Plain-English → Technical.
"""

# semantic accents (must match FAScenes.tsx)
REV = "#38BDF8"; COST = "#F87171"; PROFIT = "#34D399"; VAL = "#A78BFA"
DEBT = "#FBBF24"; TEAL = "#2DD4BF"; GRAY = "#8B93B0"
ARDEE = "#2DD4BF"; GRAV = "#818CF8"; PONDY = "#FB923C"

# ════════════════════════════════════════════════════════════════════════════
# CHAPTER 1 — THE STATEMENTS  (revenue → profit, line by line)
# ════════════════════════════════════════════════════════════════════════════
CH01 = {
 "id": "ch01",
 "title": "The Statements",
 "segments": [

 ("s01_title", "fa_title",
  {"kicker": "FUNDAMENTAL ANALYSIS · FROM SCRATCH",
   "line1": "Reading a Business", "line2": "by the Numbers",
   "sub": "Chapter 1 — the three financial statements", "color": TEAL},
  "Open any company's annual report, and you drown in numbers. [pause] "
  "But behind all of them sit just a handful of simple ideas. "
  "This course teaches every one, from scratch. [pause] "
  "By the end, you'll read a business the way an analyst does."),

 ("s02_roadmap", "fa_roadmap",
  {"kicker": "THE COURSE · SEVEN CHAPTERS",
   "parts": [
     {"n": 1, "title": "The Statements", "sub": "revenue to profit, line by line", "c": REV},
     {"n": 2, "title": "Margins", "sub": "how much of each rupee you keep", "c": PROFIT},
     {"n": 3, "title": "Returns", "sub": "R O E, R O C E, and DuPont", "c": TEAL},
     {"n": 4, "title": "Valuation", "sub": "market cap, E V, P E, E V to EBITDA", "c": VAL},
     {"n": 5, "title": "Leverage", "sub": "debt, coverage, solvency", "c": DEBT},
     {"n": 6, "title": "Growth & Quality", "sub": "C A G R, free cash flow", "c": REV},
     {"n": 7, "title": "Putting It Together", "sub": "reading a company end to end", "c": PROFIT},
   ]},
  "Here's the map. [pause] Seven chapters. "
  "First, the statements, where every number is born. "
  "Then margins, returns, and valuation, the three questions that matter most. "
  "Then leverage, growth and quality. [pause] "
  "And finally, we put it all together on one real company. "
  "We'll learn each idea on three real businesses. "
  "Ardee, Gravita, and Pondy. Three companies that recycle old batteries into lead."),

 ("s03_analogy", "fa_analogy",
  {"kicker": "ANALOGY · WHAT A COMPANY IS", "title": "A company is a money machine",
   "left": {"emoji": "🍋", "label": "A lemonade stall", "cap": "Buy lemons and sugar. Sell juice. Keep what's left.", "c": GRAY},
   "right": {"emoji": "🏭", "label": "Any company", "cap": "Buy inputs. Sell output. Keep the profit.", "c": TEAL},
   "note": "Every business, big or small, runs on this one loop: money in, costs out, profit left.",
   "color": TEAL},
  "Before any jargon, hold one picture in your head. [pause] "
  "A company is just a money machine. "
  "Think of a child's lemonade stall. "
  "She buys lemons and sugar. She sells juice. [pause] "
  "Whatever is left over is her profit. "
  "A giant factory works exactly the same way. "
  "Money comes in, costs go out, and profit is what survives. [pause] "
  "Every ratio in this course is just a sharper way to study that one loop."),

 ("s04_three", "fa_compare",
  {"kicker": "THREE STATEMENTS · ONE COMPANY", "title": "How a business reports itself",
   "cos": [
     {"name": "Income statement", "c": PROFIT, "tag": "the P&L",
      "stats": [{"k": "Question", "v": "Did we profit?"}, {"k": "Covers", "v": "a period"},
                {"k": "Top line", "v": "Revenue", "hot": True}, {"k": "Bottom line", "v": "Net profit", "hot": True}]},
     {"name": "Balance sheet", "c": REV, "tag": "what we own & owe",
      "stats": [{"k": "Question", "v": "How strong?"}, {"k": "Covers", "v": "a moment"},
                {"k": "Left", "v": "Assets", "hot": True}, {"k": "Right", "v": "Debt + equity", "hot": True}]},
     {"name": "Cash flow", "c": VAL, "tag": "real money moving",
      "stats": [{"k": "Question", "v": "Did cash come?"}, {"k": "Covers", "v": "a period"},
                {"k": "Watch", "v": "Operating cash", "hot": True}, {"k": "Truth test", "v": "Cash ≠ profit", "hot": True}]},
   ],
   "note": "This chapter lives mostly in the first one — the income statement.", "color": TEAL},
  "A company reports itself in three statements. [pause] "
  "The income statement, also called the P and L, answers one question. "
  "Over the last year, did we make a profit? [pause] "
  "The balance sheet is a snapshot. It shows what the company owns and what it owes, at one moment. [pause] "
  "And the cash flow statement tracks the real money that actually moved. "
  "Because profit on paper, and cash in the bank, are not the same thing. "
  "We'll start with the first one, the P and L."),

 ("s05_pnl_ledger", "fa_ledger",
  {"kicker": "THE INCOME STATEMENT", "title": "Revenue at the top, profit at the bottom",
   "rows": [
     {"label": "Revenue", "val": "1,168", "c": REV, "bold": True},
     {"label": "less  Operating costs", "val": "(1,021)", "c": COST, "indent": 1},
     {"label": "EBITDA", "val": "147", "c": PROFIT, "bold": True, "rule": True},
     {"label": "less  Depreciation", "val": "(20)", "c": COST, "indent": 1},
     {"label": "less  Interest", "val": "(18)", "c": DEBT, "indent": 1},
     {"label": "less  Tax", "val": "(24)", "c": COST, "indent": 1},
     {"label": "Net profit  (PAT)", "val": "85", "c": PROFIT, "bold": True, "rule": True},
   ],
   "caption": "Ardee, FY26, ₹ crore (approx). Read it top to bottom, like a staircase down.",
   "color": TEAL},
  "Here is a real income statement, simplified. This is Ardee, in crores of rupees. [pause] "
  "You read it top to bottom, like walking down a staircase. "
  "At the very top sits revenue, one thousand one hundred sixty eight crore. [pause] "
  "Then, step by step, we subtract costs. "
  "Operating costs, depreciation, interest, and tax. "
  "And whatever reaches the bottom step is net profit. "
  "Just eighty five crore. [pause] "
  "Notice how much fell away on the way down. That gap is the whole story of the business."),

 ("s06_waterfall", "fa_waterfall",
  {"kicker": "THE P&L WATERFALL", "title": "Watch the money fall from revenue to profit",
   "unit": "₹ Cr",
   "segs": [
     {"label": "Revenue", "value": 1168, "c": REV, "subtotal": True},
     {"label": "− Operating costs", "delta": -1021, "c": COST},
     {"label": "EBITDA", "value": 147, "c": PROFIT, "subtotal": True},
     {"label": "− Depreciation", "delta": -20, "c": COST},
     {"label": "− Interest", "delta": -18, "c": DEBT},
     {"label": "− Tax", "delta": -24, "c": COST},
     {"label": "Net profit", "value": 85, "c": PROFIT, "subtotal": True},
   ],
   "note": "Ardee FY26 (approx). Of every ₹100 that came in, about ₹7 survived as profit.",
   "color": REV},
  "Let's watch that staircase as a waterfall. [pause] "
  "The tall blue bar on the left is all the revenue, everything that came in. "
  "Then each red drop is a cost being taken out. [pause] "
  "The biggest drop, by far, is operating costs. "
  "That's the lead, the labour, the power to run the plant. "
  "What's left standing after it is EBITDA, one hundred forty seven crore. [pause] "
  "Then smaller drops for depreciation, interest, and tax. "
  "And the green bar at the end is profit. "
  "Of every hundred rupees that came in, only about seven rupees survived."),

 ("s07_revenue", "fa_keyidea",
  {"kicker": "TERM 1 · REVENUE", "color": REV,
   "big": "Revenue is the top line — all the money coming in, before a single cost.",
   "sub": "Also called sales or turnover. Big revenue is not the same as big profit."},
  "Let's name the lines properly, starting at the top. [pause] "
  "Revenue is simply all the money a company brought in from selling its product. "
  "You'll also hear it called sales, or turnover. [pause] "
  "It is the top line, before any cost is taken out. "
  "And here is the trap for beginners. "
  "A company can have huge revenue and still make almost no profit. [pause] "
  "Ardee sells over eleven hundred crore, but keeps only eighty five. "
  "So revenue tells you the size of a business, not its quality."),

 ("s08_gross", "fa_formula",
  {"kicker": "TERM 2 · GROSS PROFIT", "title": "Revenue minus the cost of the goods",
   "name": "Gross profit  =  Revenue  −  Cost of goods sold",
   "num": [{"label": "Revenue", "val": 1168, "c": REV}],
   "den": [{"label": "Cost of goods sold", "val": 1021, "c": COST}],
   "op": "−",
   "result": {"label": "Gross profit — what's left to run everything else", "val": 147, "unit": "₹ Cr", "decimals": 0, "c": PROFIT},
   "note": "Here shown against operating cost. Gross profit pays for everything downstream.",
   "color": PROFIT},
  "The first real profit line is gross profit. [pause] "
  "It's revenue, minus the direct cost of the goods you sold. "
  "For Ardee, that direct cost is mostly the old batteries and metal it buys to recycle. [pause] "
  "Revenue of eleven sixty eight, minus that cost, "
  "leaves roughly one hundred forty seven crore. "
  "Gross profit is the money left over to pay for everything else. "
  "The offices, the interest, the taxes. [pause] "
  "If gross profit is thin, the business has very little room to work with."),

 ("s09_ebitda", "fa_keyidea",
  {"kicker": "TERM 3 · EBITDA", "color": PROFIT,
   "big": "EBITDA is profit from the core operations — before interest, tax, and depreciation.",
   "sub": "It asks: ignoring how the company is financed, does the actual business make money?"},
  "Now the term everyone quotes, but few explain. EBITDA. [pause] "
  "It's an ugly word for a simple idea. "
  "It's the profit from just running the business, "
  "before we worry about loans, taxes, or ageing machines. [pause] "
  "The letters stand for earnings before interest, tax, depreciation and amortisation. "
  "In plain words, strip away how the company is financed, "
  "and ask, does the core operation itself make money? [pause] "
  "For Ardee, EBITDA is one hundred forty seven crore. "
  "It's the cleanest look at the engine, before the accountants and bankers get involved."),

 ("s10_ebit_dep", "fa_ledger",
  {"kicker": "TERM 4 · DEPRECIATION & EBIT", "title": "The cost of machines wearing out",
   "rows": [
     {"label": "EBITDA  (core operating profit)", "val": "147", "c": PROFIT, "bold": True},
     {"label": "less  Depreciation — machines ageing", "val": "(20)", "c": COST, "indent": 1},
     {"label": "EBIT  (operating profit)", "val": "127", "c": TEAL, "bold": True, "rule": True},
   ],
   "caption": "Depreciation spreads a machine's cost over the years it is used. No cash leaves today.",
   "color": TEAL},
  "Next we subtract depreciation. [pause] "
  "When a company buys a machine, it doesn't count the whole cost in one year. "
  "It spreads that cost across all the years the machine will be used. "
  "That yearly slice is depreciation. [pause] "
  "It's a real cost, but a strange one. No cash actually leaves the bank today. "
  "Take depreciation out of EBITDA, and you get EBIT. "
  "Earnings before interest and tax, also called operating profit. [pause] "
  "For Ardee, that's about one hundred twenty seven crore."),

 ("s11_pat", "fa_keyidea",
  {"kicker": "TERM 5 · INTEREST, TAX & PAT", "color": PROFIT,
   "big": "After interest to lenders and tax to the government, what remains is Net Profit — PAT.",
   "sub": "The true bottom line. This is the money that belongs to the shareholders."},
  "Two subtractions remain. [pause] "
  "First, interest, the rent a company pays on its loans. "
  "Ardee pays about eighteen crore to its lenders. [pause] "
  "Then tax, the government's share, around twenty four crore. "
  "And what finally remains is net profit, or PAT. "
  "Profit after tax. [pause] "
  "This is the true bottom line, eighty five crore. "
  "This is the money that actually belongs to the owners, the shareholders. "
  "Every other number we've seen was just a step on the way down to this one."),

 ("s12_eps", "fa_formula",
  {"kicker": "TERM 6 · EARNINGS PER SHARE", "title": "Profit, sliced per share",
   "name": "EPS  =  Net profit  ÷  Number of shares",
   "num": [{"label": "Net profit (PAT)", "val": 85, "c": PROFIT}],
   "den": [{"label": "Shares (crore)", "val": 30, "c": REV}], "op": "÷",
   "result": {"label": "Earnings per share — profit behind one share", "val": 2.8, "unit": "₹", "decimals": 1, "c": TEAL},
   "note": "≈ 30 crore shares (approx). EPS lets you compare profit to the share price later.",
   "color": TEAL},
  "One more number turns profit into something personal. Earnings per share, or EPS. [pause] "
  "A company's profit is shared among all its shares. "
  "So we divide net profit by the number of shares. [pause] "
  "Ardee's eighty five crore of profit, split across roughly thirty crore shares, "
  "is about two rupees and eighty paise per share. "
  "That's the profit sitting behind a single share. [pause] "
  "Hold on to EPS. In chapter four, we'll compare it to the share price, "
  "and that's where valuation begins."),

 ("s13_balance", "fa_analogy",
  {"kicker": "THE BALANCE SHEET", "title": "What you own must equal what you owe plus your own money",
   "left": {"emoji": "🏠", "label": "Buying a house", "cap": "House worth ₹1 crore = bank loan + your savings.", "c": REV},
   "right": {"emoji": "⚖️", "label": "The balance sheet", "cap": "Assets = Liabilities + Equity. Always balances.", "c": PROFIT},
   "note": "Assets are what the company owns. Liabilities are what it owes. Equity is the owners' share.",
   "color": REV},
  "Now leave the P and L, and look at the balance sheet. [pause] "
  "Think about buying a house worth one crore. "
  "Part is a bank loan, and part is your own savings. "
  "Those two must add up to the value of the house. [pause] "
  "A company is identical. "
  "Everything it owns, its assets, is funded either by money it owes, called liabilities, "
  "or by the owners' own money, called equity. [pause] "
  "Assets equal liabilities plus equity. "
  "That equation always balances. That's why it's called a balance sheet."),

 ("s14_cashflow", "fa_keyidea",
  {"kicker": "THE CASH FLOW STATEMENT", "color": VAL,
   "big": "Profit is an opinion. Cash is a fact.",
   "sub": "A company can report profit yet run out of cash — so we track the money that truly moved."},
  "That leaves the third statement, cash flow. And it exists to catch a lie. [pause] "
  "Profit is partly an opinion. "
  "It depends on judgement calls, like how fast machines wear out. "
  "Cash is a fact. It's either in the bank, or it isn't. [pause] "
  "A company can report a healthy profit and still run out of cash, "
  "if customers haven't paid, or stock is piling up. "
  "So the cash flow statement follows the real money. [pause] "
  "The most important line is cash from operations. "
  "Healthy businesses turn their profit into actual cash. We'll return to this in chapter six."),

 ("s15_recap", "fa_recap",
  {"kicker": "RECAP · CHAPTER 1", "title": "The statements in one breath",
   "items": [
     "Three statements: income (P&L), balance sheet, cash flow",
     "The P&L runs top to bottom: Revenue → costs → Profit",
     "Revenue is size; profit is what survives every cost",
     "EBITDA = core operating profit, before interest, tax, depreciation",
     "PAT is the true bottom line; EPS is PAT per share",
     "Balance sheet: Assets = Liabilities + Equity, always",
     "Profit is an opinion; cash is a fact",
   ],
   "closer": "Master these lines — every ratio ahead is just built from them.",
   "color": TEAL},
  "Let's lock it in. [pause] "
  "A company reports in three statements. "
  "The income statement runs from revenue at the top, down through costs, to profit at the bottom. "
  "Revenue is size. Profit is what survives. [pause] "
  "EBITDA is the core engine. PAT is the true bottom line, and EPS is that profit per share. "
  "The balance sheet always balances, assets equal liabilities plus equity. "
  "And profit is an opinion, while cash is a fact. [pause] "
  "Every ratio in the coming chapters is just built from these lines. "
  "One last thing. This course is education, not investment advice. "
  "Always do your own research, or talk to a registered advisor. "
  "In chapter two, we turn these numbers into margins. Thanks for watching."),

 ],
}

# ════════════════════════════════════════════════════════════════════════════
# CHAPTER 2 — MARGINS  (how much of each rupee the business keeps)
# ════════════════════════════════════════════════════════════════════════════
CH02 = {
 "id": "ch02",
 "title": "Margins",
 "segments": [

 ("s01_divider", "fa_divider",
  {"n": 2, "title": "Margins", "sub": "how much of each rupee you actually keep", "color": PROFIT, "total": 7},
  "Chapter two. Margins. [pause] "
  "In chapter one, we watched revenue fall, step by step, down to profit. "
  "A margin simply measures how big each of those steps is. "
  "It's the single fastest way to judge the quality of a business."),

 ("s02_analogy", "fa_analogy",
  {"kicker": "ANALOGY · THE KEEP-RATE", "title": "A margin is your keep-rate",
   "left": {"emoji": "💵", "label": "₹100 comes in", "cap": "Every sale brings money through the door.", "c": REV},
   "right": {"emoji": "🪙", "label": "₹7 you keep", "cap": "After every cost, this is what stays with you.", "c": PROFIT},
   "note": "Net margin is just that keep-rate as a percentage. For Ardee, about seven rupees in every hundred.",
   "color": PROFIT},
  "Here's the whole idea in one picture. [pause] "
  "Imagine one hundred rupees walks in the door as revenue. "
  "By the time all the costs are paid, only a few rupees stay in your pocket. [pause] "
  "That keep-rate is the margin. "
  "For Ardee, out of every hundred rupees of sales, "
  "only about seven rupees survive as profit. "
  "So its net margin is roughly seven percent. [pause] "
  "A higher keep-rate means a stronger, more valuable business."),

 ("s03_what", "fa_keyidea",
  {"kicker": "WHAT A MARGIN IS", "color": PROFIT,
   "big": "A margin is a profit line, divided by revenue — shown as a percentage.",
   "sub": "It turns a rupee figure into a rate you can compare across companies of any size."},
  "Let's define it properly. [pause] "
  "A margin is any profit line, divided by revenue. "
  "We write it as a percentage. [pause] "
  "Why bother turning rupees into a percentage? "
  "Because it lets you compare a tiny company with a giant. "
  "Profit in rupees depends on size. "
  "Margin does not. [pause] "
  "A small shop and a huge factory can both have a twenty percent margin, "
  "and that tells you they keep the same share of every sale."),

 ("s04_net", "fa_formula",
  {"kicker": "MARGIN 1 · NET MARGIN", "title": "The keep-rate, as a formula",
   "name": "Net margin  =  Net profit  ÷  Revenue",
   "num": [{"label": "Net profit (PAT)", "val": 85, "c": PROFIT}],
   "den": [{"label": "Revenue", "val": 1168, "c": REV}], "op": "÷",
   "result": {"label": "Net margin — rupees kept per ₹100 of sales", "val": 7.3, "unit": "%", "decimals": 1, "c": PROFIT},
   "note": "Ardee FY26 (approx). ₹85 profit on ₹1,168 revenue.", "color": PROFIT},
  "Start with the margin you already understand. Net margin. [pause] "
  "Take net profit, and divide it by revenue. "
  "Ardee's eighty five crore of profit, divided by eleven sixty eight of revenue, "
  "is about seven point three percent. [pause] "
  "That's the final keep-rate, after every single cost. "
  "For a business that just buys and melts metal, seven percent is actually decent. "
  "Now let's climb back up the ladder, and meet the margins above it."),

 ("s05_ladder", "fa_bars",
  {"kicker": "THE LADDER OF MARGINS", "title": "Each layer of cost keeps a little less",
   "unit": "%", "decimals": 1,
   "bars": [
     {"label": "EBITDA margin", "val": 12.6, "c": PROFIT, "note": "core engine"},
     {"label": "Operating margin", "val": 10.9, "c": TEAL, "note": "after depreciation"},
     {"label": "Net margin", "val": 7.3, "c": REV, "note": "after interest & tax"},
   ],
   "note": "Same company, three margins. Each step down is another layer of cost.",
   "color": PROFIT},
  "A company doesn't have one margin. It has a whole ladder of them. [pause] "
  "At the top sits the EBITDA margin, the core engine, twelve point six percent. "
  "Take out depreciation, and you get the operating margin, about eleven percent. [pause] "
  "Take out interest and tax, and you drop to the net margin, seven point three. "
  "Notice the pattern. "
  "Each step down the ladder is another layer of cost being paid. [pause] "
  "The gap between the top and the bottom tells you where a company's money is really going."),

 ("s06_ebitda_m", "fa_formula",
  {"kicker": "MARGIN 2 · EBITDA MARGIN", "title": "The margin analysts quote most",
   "name": "EBITDA margin  =  EBITDA  ÷  Revenue",
   "num": [{"label": "EBITDA", "val": 147, "c": PROFIT}],
   "den": [{"label": "Revenue", "val": 1168, "c": REV}], "op": "÷",
   "result": {"label": "EBITDA margin — profitability of the core operation", "val": 12.6, "unit": "%", "decimals": 1, "c": PROFIT},
   "note": "The cleanest margin for comparing two companies' core operations.", "color": PROFIT},
  "The margin you'll hear quoted most is the EBITDA margin. [pause] "
  "It's EBITDA, divided by revenue. "
  "For Ardee, that's one forty seven over eleven sixty eight, "
  "twelve point six percent. [pause] "
  "Analysts love it because it strips out how a company is financed and taxed. "
  "So it compares two businesses on their operations alone. "
  "It's the fairest way to ask, whose core engine is stronger?"),

 ("s07_gauge", "fa_gauge",
  {"kicker": "READING THE NEEDLE", "title": "Is a 7% net margin good?",
   "value": 7.3, "min": 0, "max": 30, "unit": "%",
   "zones": [{"to": 6, "c": COST, "label": "thin"}, {"to": 15, "c": DEBT, "label": "typical"}, {"to": 30, "c": PROFIT, "label": "fat"}],
   "caption": "Thin margins are normal for commodity businesses. Brands and software sit far to the right.",
   "note": "Judge a margin against its industry, never in isolation.", "color": PROFIT},
  "So, is seven percent good or bad? [pause] "
  "The honest answer is, it depends on the industry. "
  "A business that buys and sells a commodity, like metal, "
  "will always run on thin margins. That's the nature of the game. [pause] "
  "A strong consumer brand might keep twenty or thirty percent. "
  "A software company, even more. "
  "So never judge a margin alone. "
  "Always compare it to its own industry, and to its own past."),

 ("s08_compare", "fa_bars",
  {"kicker": "SAME BUSINESS · THREE RIVALS", "title": "EBITDA margin: Ardee vs Gravita vs Pondy",
   "unit": "%", "decimals": 1,
   "bars": [
     {"label": "Ardee", "val": 12.6, "c": ARDEE, "note": "highest keep-rate"},
     {"label": "Gravita", "val": 10.6, "c": GRAV, "note": "the scaled leader"},
     {"label": "Pondy", "val": 7.4, "c": PONDY, "note": "thinnest"},
   ],
   "note": "All three recycle lead. Ardee keeps the most per rupee — its operating edge.",
   "color": TEAL},
  "Now watch margins do real work. [pause] "
  "Here are our three recyclers, all in the same business. "
  "Ardee's EBITDA margin is twelve point six percent. "
  "Gravita, the largest and most respected, is ten point six. "
  "And Pondy is the thinnest, at seven point four. [pause] "
  "This one chart says a lot. "
  "Ardee squeezes the most profit out of every rupee of sales. "
  "That operating edge is the first real clue that its business is running well."),

 ("s09_type", "fa_keyidea",
  {"kicker": "WHAT MARGINS REVEAL", "color": VAL,
   "big": "Margin is a fingerprint of the business model.",
   "sub": "Fat margins hint at pricing power or a brand. Thin margins mean price is set by the market."},
  "Step back, and margins tell you what kind of business you're looking at. [pause] "
  "Fat margins are a signal of power. "
  "Maybe a strong brand, a patent, or a product customers can't easily replace. "
  "The company sets its own price. [pause] "
  "Thin margins mean the opposite. "
  "The market sets the price, and the company just has to accept it. "
  "That's why steel, cement and metals all run thin. "
  "The margin is a fingerprint of the business model itself."),

 ("s10_trap", "fa_keyidea",
  {"kicker": "THE TRAP · MARGIN ISN'T EVERYTHING", "color": TEAL,
   "big": "A thin margin can still be a great business — if the money turns over fast enough.",
   "sub": "A supermarket keeps ₹3 per ₹100, but sells its entire stock many times a year."},
  "But here's the trap. A thin margin is not automatically a bad business. [pause] "
  "Think of a supermarket. "
  "It might keep only three rupees on every hundred. "
  "That sounds terrible. [pause] "
  "But it sells its entire stock over and over, many times a year. "
  "Small margin, huge volume, and the profits add up. "
  "So margin alone is only half the story. "
  "The other half is how fast the money turns over. "
  "And that is exactly what returns measure. Which is chapter three."),

 ("s11_recap", "fa_recap",
  {"kicker": "RECAP · CHAPTER 2", "title": "Margins in one breath",
   "items": [
     "A margin = a profit line ÷ revenue, shown as a %",
     "It turns rupees into a rate you can compare at any size",
     "The ladder: EBITDA margin → operating → net (each keeps less)",
     "Ardee net margin ≈ 7.3%, EBITDA margin ≈ 12.6%",
     "Ardee's EBITDA margin beats Gravita and Pondy — an operating edge",
     "Judge a margin by its industry, never alone",
     "Thin margin + fast turnover can still be a great business",
   ],
   "closer": "Margins show the keep-rate. Next: how hard the money works.",
   "color": PROFIT},
  "Let's lock in chapter two. [pause] "
  "A margin is a profit line divided by revenue, written as a percentage. "
  "It turns rupees into a rate, so you can compare any two companies. "
  "There's a ladder of them, from EBITDA margin at the top, down to net margin. [pause] "
  "Ardee keeps about seven rupees in every hundred, "
  "and its EBITDA margin beats both Gravita and Pondy. "
  "Always judge a margin against its industry. [pause] "
  "And remember, a thin margin with fast turnover can still be excellent. "
  "That link, between margin and speed, is where returns begin. "
  "See you in chapter three. Thanks for watching."),

 ],
}

# ════════════════════════════════════════════════════════════════════════════
# CHAPTER 3 — RETURNS  (how hard the money works: ROE, ROCE, ROA, DuPont)
# Internally-consistent illustrative capital base for Ardee (approx FY26):
#   Equity ≈ 300 · Debt ≈ 180 · Capital employed ≈ 480 · Total assets ≈ 600
#   ROE = 85/300 = 28% · ROCE = 127/480 = 26% · ROA = 85/600 = 14%
#   DuPont: net margin 7.3% × asset turnover 1.95 × equity multiplier 2.0 ≈ 28%
# ════════════════════════════════════════════════════════════════════════════
CH03 = {
 "id": "ch03",
 "title": "Returns",
 "segments": [

 ("s01_divider", "fa_divider",
  {"n": 3, "title": "Returns", "sub": "how hard each rupee of capital works", "color": TEAL, "total": 7},
  "Chapter three. Returns. [pause] "
  "Margins told us how much a company keeps from each sale. "
  "Returns ask a deeper question. "
  "For every rupee of capital put into this business, how much profit comes back?"),

 ("s02_analogy", "fa_analogy",
  {"kicker": "ANALOGY · THE BUSINESS'S INTEREST RATE", "title": "A return is the business's interest rate",
   "left": {"emoji": "🏦", "label": "A fixed deposit", "cap": "Put in ₹100. The bank pays you, say, ₹7 a year.", "c": REV},
   "right": {"emoji": "🏭", "label": "A business", "cap": "Put in ₹100 of capital. It earns ₹28 of profit.", "c": TEAL},
   "note": "Return on equity is the interest rate a company earns on the owners' money.",
   "color": TEAL},
  "Think about a fixed deposit. [pause] "
  "You put in one hundred rupees, and the bank pays you maybe seven rupees a year. "
  "That's a seven percent return. [pause] "
  "A business works the same way, but the interest rate is its own. "
  "Put one hundred rupees of capital into Ardee, "
  "and it generates around twenty eight rupees of profit in a year. [pause] "
  "That's a twenty eight percent return. "
  "Return ratios are simply the interest rate a business earns on the money inside it."),

 ("s03_what", "fa_keyidea",
  {"kicker": "WHAT A RETURN IS", "color": TEAL,
   "big": "A return = profit ÷ the capital used to make it.",
   "sub": "Margins judge the sale. Returns judge the capital. A great business earns a high return."},
  "So the shape of every return ratio is the same. [pause] "
  "Profit on top, divided by the capital used to earn it, on the bottom. "
  "The only thing that changes is which profit, and whose capital. [pause] "
  "This is arguably the most important idea in the whole course. "
  "A business can have thin margins, and still be wonderful, "
  "if it earns a high return on its capital. "
  "That's the real mark of quality."),

 ("s04_roe", "fa_formula",
  {"kicker": "RETURN 1 · RETURN ON EQUITY", "title": "The owners' return",
   "name": "ROE  =  Net profit  ÷  Shareholders' equity",
   "num": [{"label": "Net profit (PAT)", "val": 85, "c": PROFIT}],
   "den": [{"label": "Equity", "val": 300, "c": TEAL}], "op": "÷",
   "result": {"label": "Return on Equity — profit per ₹ of owners' money", "val": 28, "unit": "%", "decimals": 0, "c": TEAL},
   "note": "Ardee approx. Equity is the owners' own money in the business.", "color": TEAL},
  "The first return is the one owners care about most. Return on equity, or ROE. [pause] "
  "It's net profit, divided by equity. "
  "Remember, equity is the owners' own money inside the company. [pause] "
  "Ardee earns eighty five crore on roughly three hundred crore of equity. "
  "That's about twenty eight percent. "
  "In plain words, every hundred rupees the owners have tied up "
  "is throwing off twenty eight rupees of profit a year. "
  "For any business, that is a genuinely strong number."),

 ("s05_roce", "fa_formula",
  {"kicker": "RETURN 2 · RETURN ON CAPITAL", "title": "The return on all the money at work",
   "name": "ROCE  =  Operating profit (EBIT)  ÷  Capital employed",
   "num": [{"label": "EBIT", "val": 127, "c": TEAL}],
   "den": [{"label": "Equity + Debt", "val": 480, "c": DEBT}], "op": "÷",
   "result": {"label": "Return on Capital Employed — before financing choices", "val": 26, "unit": "%", "decimals": 0, "c": TEAL},
   "note": "Capital employed = equity + debt. ROCE ignores how the capital was raised.", "color": TEAL},
  "The second return is a fairer one. Return on capital employed, or ROCE. [pause] "
  "This time we use operating profit, EBIT, on top. "
  "And on the bottom, all the capital at work, both equity and debt. [pause] "
  "Ardee's one twenty seven of EBIT, on four hundred eighty of total capital, "
  "is about twenty six percent. "
  "ROCE asks a cleaner question than ROE. "
  "Ignoring how the money was raised, how good is the business at using capital? [pause] "
  "That's why serious investors watch ROCE closely."),

 ("s06_roe_vs", "fa_keyidea",
  {"kicker": "ROE vs ROCE · THE DEBT TRICK", "color": DEBT,
   "big": "Debt can flatter ROE. ROCE can't be fooled.",
   "sub": "Borrow heavily and ROE can look great — even if the business is weak. Always check both."},
  "Now, why do we need two return ratios? [pause] "
  "Because ROE has a blind spot. "
  "A company can boost its ROE simply by borrowing more money. "
  "More debt, less equity on the bottom, and the ratio jumps. [pause] "
  "But that higher ROE came from risk, not skill. "
  "ROCE can't be tricked this way, because it counts debt as capital too. "
  "So here's the rule. "
  "A high ROE with a high ROCE is real quality. "
  "A high ROE with a weak ROCE is just borrowed money. Always check both."),

 ("s07_ladder", "fa_bars",
  {"kicker": "ARDEE'S RETURNS · vs THE HURDLE", "title": "Every return clears the cost of capital",
   "unit": "%", "decimals": 0,
   "bars": [
     {"label": "ROE", "val": 28, "c": PROFIT, "note": "owners' money"},
     {"label": "ROCE", "val": 26, "c": TEAL, "note": "all capital"},
     {"label": "ROA", "val": 14, "c": REV, "note": "all assets"},
   ],
   "baseline": {"val": 12, "label": "≈ cost of capital"},
   "note": "All three sit well above the ~12% cost of capital. That gap is value being created.",
   "color": TEAL},
  "Let's see Ardee's returns together. [pause] "
  "ROE is twenty eight percent. ROCE, twenty six. "
  "And return on assets, ROA, which uses everything the company owns, is about fourteen. [pause] "
  "Now look at the dashed line. "
  "That's the cost of capital, very roughly twelve percent. "
  "It's the return investors expect just for taking the risk. [pause] "
  "Every one of Ardee's returns sits above that line. "
  "And that gap, between what the business earns and what capital costs, "
  "is the definition of value being created."),

 ("s08_dupont", "fa_dupont",
  {"kicker": "DUPONT · WHERE RETURN COMES FROM", "title": "ROE = margin × turnover × leverage",
   "factors": [
     {"name": "Net margin\n(profit per sale)", "val": 7.3, "unit": "%", "c": PROFIT, "decimals": 1},
     {"name": "Asset turnover\n(sales per asset)", "val": 1.95, "unit": "×", "c": REV, "decimals": 2},
     {"name": "Leverage\n(assets per equity)", "val": 2.0, "unit": "×", "c": DEBT, "decimals": 1},
   ],
   "result": {"name": "Return on Equity", "val": 28, "unit": "%", "c": TEAL, "decimals": 0},
   "note": "The DuPont formula splits ROE into three levers you can actually diagnose.",
   "color": TEAL},
  "Here's the most powerful tool in this chapter. The DuPont breakdown. [pause] "
  "It splits ROE into three simple levers. "
  "First, net margin. How much profit per sale. "
  "Second, asset turnover. How many rupees of sales you get from each rupee of assets. "
  "And third, leverage. How much the company borrows. [pause] "
  "Multiply the three together, and you get ROE. "
  "For Ardee, a seven percent margin, times nearly two turns, times two on leverage, "
  "gives twenty eight percent. [pause] "
  "Now you can see exactly where a company's return is coming from, "
  "and whether it's from skill, speed, or just debt."),

 ("s09_value", "fa_keyidea",
  {"kicker": "THE PUNCHLINE", "color": PROFIT,
   "big": "A business creates value only when its return on capital beats the cost of that capital.",
   "sub": "Earn 26% on money that costs 12%, and every rupee reinvested makes the owners richer."},
  "Let's end this chapter with the single most important sentence in investing. [pause] "
  "A business creates value only when its return on capital "
  "is higher than the cost of that capital. [pause] "
  "If Ardee earns twenty six percent on money that costs twelve, "
  "then every rupee it reinvests makes its owners wealthier. "
  "But if a company earns less than its cost of capital, "
  "growth actually destroys value. [pause] "
  "This is why returns matter more than almost any other number. "
  "They tell you whether growth is worth having at all."),

 ("s10_recap", "fa_recap",
  {"kicker": "RECAP · CHAPTER 3", "title": "Returns in one breath",
   "items": [
     "A return = profit ÷ the capital used to earn it",
     "ROE = net profit ÷ equity (the owners' interest rate)",
     "ROCE = EBIT ÷ capital employed (ignores financing)",
     "Debt can flatter ROE; ROCE can't be tricked — check both",
     "DuPont: ROE = margin × asset turnover × leverage",
     "Ardee: ROE ≈ 28%, ROCE ≈ 26% — well above ~12% cost of capital",
     "Value is created only when return beats the cost of capital",
   ],
   "closer": "Returns tell you the quality. Next: what you pay for it — valuation.",
   "color": TEAL},
  "Let's lock in chapter three. [pause] "
  "A return is profit divided by the capital used to earn it. "
  "ROE is the owners' interest rate. ROCE measures all the capital at work, "
  "and unlike ROE, it can't be flattered by debt. [pause] "
  "The DuPont breakdown shows return as margin, times turnover, times leverage. "
  "Ardee earns around twenty eight percent, well above its cost of capital. "
  "And that is the whole point. [pause] "
  "A business only creates value when its return beats what its capital costs. "
  "We now know the quality of the business. "
  "In chapter four, we ask what you should pay for it. Thanks for watching."),

 ],
}

# ════════════════════════════════════════════════════════════════════════════
# CHAPTER 4 — VALUATION  (what you pay: market cap, EV, P/E, EV/EBITDA, P/B, yields)
# Ardee (approx): price 70 · shares 30 · Mcap 2,100 · debt 180 · cash 30 · EV 2,250
#   EPS 2.8 · P/E 25x · EV/EBITDA 15x · book(equity) 300 → BVPS 10 → P/B 7x
#   earnings yield 1/25 ≈ 4%. Peers P/E: Gravita 31, Pondy 40. EV/EBITDA: Grav 26, Pondy 25.
# ════════════════════════════════════════════════════════════════════════════
CH04 = {
 "id": "ch04",
 "title": "Valuation",
 "segments": [

 ("s01_divider", "fa_divider",
  {"n": 4, "title": "Valuation", "sub": "price is what you pay; value is what you get", "color": VAL, "total": 7},
  "Chapter four. Valuation. [pause] "
  "So far we've judged the business itself. "
  "Its profit, its margins, its returns. "
  "Now we ask the question that decides whether it's a good investment. "
  "What price should you pay for it?"),

 ("s02_analogy", "fa_analogy",
  {"kicker": "ANALOGY · PRICE vs VALUE", "title": "A great company can be a terrible buy",
   "left": {"emoji": "🏪", "label": "A shop for sale", "cap": "It earns ₹1 lakh a year. Solid little business.", "c": PROFIT},
   "right": {"emoji": "🏷️", "label": "The asking price", "cap": "₹50 lakh? Or ₹5 lakh? Same shop — very different deal.", "c": VAL},
   "note": "Valuation compares the price you pay to the profit you get. Even a great shop is a bad buy if overpriced.",
   "color": VAL},
  "Picture a small shop for sale. [pause] "
  "It earns one lakh rupees of profit a year. A nice little business. "
  "But should you buy it? [pause] "
  "It completely depends on the asking price. "
  "At five lakh, it pays for itself in five years. A bargain. "
  "At fifty lakh, it takes fifty years. A terrible deal. [pause] "
  "Same shop, same profit. "
  "The only thing that changed is the price. "
  "That is the entire job of valuation. Comparing price to what you actually get."),

 ("s03_what", "fa_keyidea",
  {"kicker": "THE BIG IDEA", "color": VAL,
   "big": "Price is what you pay. Value is what you get.",
   "sub": "A valuation multiple divides the price by a fundamental — profit, cash flow, or assets."},
  "So hold this line in your head. [pause] "
  "Price is what you pay. Value is what you get. "
  "They are not the same thing. [pause] "
  "To compare them, we build valuation multiples. "
  "Every multiple is a price, divided by something fundamental. "
  "Profit, or cash flow, or assets. [pause] "
  "The multiple tells you how many rupees you're paying "
  "for one rupee of what the business produces. Let's build them up."),

 ("s04_mcap", "fa_formula",
  {"kicker": "PRICE TAG 1 · MARKET CAP", "title": "The price of all the shares",
   "name": "Market cap  =  Share price  ×  Number of shares",
   "num": [{"label": "Share price", "val": 70, "c": VAL}],
   "den": [{"label": "Shares (crore)", "val": 30, "c": REV}], "op": "×",
   "result": {"label": "Market capitalisation — the equity price tag", "val": 2100, "unit": "₹ Cr", "decimals": 0, "c": VAL},
   "note": "Ardee approx. Market cap is what the stock market says the equity is worth.", "color": VAL},
  "Start with the simplest price tag. Market capitalisation. [pause] "
  "It's just the share price, times the number of shares. "
  "Ardee trades near seventy rupees, and has about thirty crore shares. [pause] "
  "Multiply them, and the whole company's equity is worth around two thousand one hundred crore. "
  "That's market cap. "
  "It's the price the stock market is putting on all the shares, right now. [pause] "
  "But market cap is not the full cost of owning the business. Here's why."),

 ("s05_ev", "fa_stack",
  {"kicker": "PRICE TAG 2 · ENTERPRISE VALUE", "title": "The true takeover price",
   "unit": "₹ Cr",
   "segs": [
     {"label": "Market cap", "val": 2100, "c": VAL, "op": "+"},
     {"label": "add  Debt you inherit", "val": 180, "c": DEBT, "op": "+"},
     {"label": "less  Cash you receive", "val": -30, "c": PROFIT, "op": "−"},
   ],
   "result": {"label": "Enterprise Value (EV)", "val": 2250, "c": VAL},
   "note": "Buy the whole company and you take on its debt but pocket its cash. EV is the real price.",
   "color": VAL},
  "If you bought the entire company, you'd get more than its shares. [pause] "
  "You'd also inherit its debt, which you have to repay. "
  "But you'd also get its cash, which is yours to keep. [pause] "
  "So the true price is market cap, plus debt, minus cash. "
  "That's enterprise value, or EV. "
  "For Ardee, two thousand one hundred, plus one eighty of debt, minus thirty of cash. "
  "About two thousand two hundred fifty crore. [pause] "
  "EV is what it would really cost to take the whole business home."),

 ("s06_ev_why", "fa_keyidea",
  {"kicker": "WHY EV MATTERS", "color": VAL,
   "big": "EV lets you compare two companies fairly — even if one is loaded with debt.",
   "sub": "Market cap ignores debt. Enterprise value doesn't. That's why pros value on EV."},
  "Why go to this trouble? [pause] "
  "Because market cap can lie when you compare two companies. "
  "Imagine two identical businesses. "
  "One has no debt. The other is buried in loans. [pause] "
  "They might have the same market cap. "
  "But the indebted one is far more expensive to actually own, "
  "because you take on all that debt. "
  "Enterprise value captures that. Market cap doesn't. [pause] "
  "That's why professional investors value companies on EV, not just market cap."),

 ("s07_pe", "fa_formula",
  {"kicker": "MULTIPLE 1 · THE P/E RATIO", "title": "The most famous number in the market",
   "name": "P/E  =  Share price  ÷  Earnings per share",
   "num": [{"label": "Share price", "val": 70, "c": VAL}],
   "den": [{"label": "EPS", "val": 2.8, "c": PROFIT}], "op": "÷",
   "result": {"label": "Price-to-Earnings — ₹ paid per ₹1 of annual profit", "val": 25, "unit": "×", "decimals": 0, "c": VAL},
   "note": "Ardee ≈ 25×. Remember EPS from chapter one: profit per share.", "color": VAL},
  "Now the most famous number in all of investing. The P E ratio. [pause] "
  "It's the share price, divided by earnings per share. "
  "Remember EPS from chapter one? Profit, per share. [pause] "
  "Ardee at seventy rupees, with EPS near two rupees eighty, "
  "trades at a P E of about twenty five. "
  "So you're paying twenty five rupees "
  "for every one rupee of annual profit the company makes."),

 ("s08_pe_mean", "fa_keyidea",
  {"kicker": "READING THE P/E", "color": VAL,
   "big": "A P/E of 25 means ~25 years of today's profit to earn back your price.",
   "sub": "A high P/E isn't 'expensive' — it's the market pricing in future growth. Low isn't always cheap."},
  "What does a P E of twenty five actually mean? [pause] "
  "One way to read it. "
  "If profits never grew, it would take about twenty five years "
  "of earnings to get your money back. [pause] "
  "But here's the subtle part. "
  "A high P E doesn't simply mean expensive. "
  "It usually means the market expects profits to grow fast. "
  "And a low P E isn't always a bargain. "
  "Sometimes it's a warning that trouble is coming. "
  "The P E is a question, not an answer."),

 ("s09_evebitda", "fa_formula",
  {"kicker": "MULTIPLE 2 · EV / EBITDA", "title": "The professional's multiple",
   "name": "EV / EBITDA  =  Enterprise value  ÷  EBITDA",
   "num": [{"label": "Enterprise value", "val": 2250, "c": VAL}],
   "den": [{"label": "EBITDA", "val": 147, "c": PROFIT}], "op": "÷",
   "result": {"label": "EV/EBITDA — price of the whole business per ₹ of core profit", "val": 15, "unit": "×", "decimals": 0, "c": VAL},
   "note": "Ardee ≈ 15×. Uses EV (whole business) over EBITDA (core operating profit).", "color": VAL},
  "The P E has a weakness. It ignores debt, and it's affected by tax tricks. [pause] "
  "So professionals prefer another multiple. E V to EBITDA. "
  "On top, enterprise value, the whole business. "
  "On the bottom, EBITDA, the core operating profit. [pause] "
  "For Ardee, two thousand two hundred fifty, over one forty seven, "
  "is about fifteen times. "
  "Because it uses EV, it accounts for debt. "
  "So it compares two companies far more fairly than the P E can."),

 ("s10_compare_pe", "fa_bars",
  {"kicker": "P/E · ARDEE vs GRAVITA vs PONDY", "title": "Who is the market paying up for?",
   "unit": "×", "decimals": 0,
   "bars": [
     {"label": "Ardee", "val": 25, "c": ARDEE, "note": "cheapest"},
     {"label": "Gravita", "val": 31, "c": GRAV, "note": "the leader"},
     {"label": "Pondy", "val": 40, "c": PONDY, "note": "priciest"},
   ],
   "note": "On P/E, Ardee is the cheapest of the three — but a low multiple has two meanings.",
   "color": VAL},
  "Let's put our three recyclers side by side, on the P E. [pause] "
  "Ardee trades at about twenty five times earnings. "
  "Gravita, the established leader, at thirty one. "
  "And Pondy, the priciest, at around forty. [pause] "
  "So on the P E, Ardee looks the cheapest of the three. "
  "But remember what we said. "
  "Cheap can mean a bargain, or it can mean the market is worried. "
  "One ratio alone can't tell you which. Let's add the fairer one."),

 ("s11_compare_ev", "fa_bars",
  {"kicker": "EV / EBITDA · THE FAIRER LENS", "title": "The gap widens on the professional multiple",
   "unit": "×", "decimals": 0,
   "bars": [
     {"label": "Ardee", "val": 15, "c": ARDEE, "note": "~half its peers"},
     {"label": "Gravita", "val": 26, "c": GRAV, "note": "quality premium"},
     {"label": "Pondy", "val": 25, "c": PONDY, "note": "pricey for its margin"},
   ],
   "note": "On EV/EBITDA, Ardee (~15×) is roughly half of Gravita and Pondy (~26×). A real discount.",
   "color": VAL},
  "Now the same three, on E V to EBITDA. [pause] "
  "And look how the gap widens. "
  "Ardee is about fifteen times. "
  "Gravita and Pondy are both around twenty five to twenty six. [pause] "
  "So on the fairer, debt-adjusted multiple, "
  "Ardee trades at roughly half the price of its peers. "
  "That's a genuine discount. "
  "The question every investor must then ask is simply, why? "
  "Is it a bargain, or is the discount deserved?"),

 ("s12_pb_yield", "fa_formula",
  {"kicker": "MULTIPLE 3 · PRICE-TO-BOOK & YIELD", "title": "Price against the company's own net worth",
   "name": "P/B  =  Share price  ÷  Book value per share",
   "num": [{"label": "Share price", "val": 70, "c": VAL}],
   "den": [{"label": "Book value / share", "val": 10, "c": TEAL}], "op": "÷",
   "result": {"label": "Price-to-Book — ₹ paid per ₹1 of net worth", "val": 7, "unit": "×", "decimals": 0, "c": VAL},
   "note": "Also: earnings yield = 1 ÷ P/E ≈ 4%. It's the flip side of the P/E, like an interest rate.",
   "color": VAL},
  "Two more quick tools. [pause] "
  "Price to book compares the share price to the company's net worth per share. "
  "Ardee's book value is about ten rupees a share, "
  "so at seventy, its price to book is around seven times. [pause] "
  "High price to book is justified only by high returns, "
  "which, remember, Ardee has. "
  "And finally, flip the P E upside down, and you get the earnings yield. "
  "One divided by twenty five is about four percent. "
  "It lets you compare a stock's profit to a bank deposit's interest."),

 ("s13_map", "fa_quadrant",
  {"kicker": "THE VALUATION MAP", "title": "Cheap vs quality — where each one sits",
   "xlab": "cheaper", "ylab": "higher quality", "xlo": "expensive", "xhi": "cheap",
   "points": [
     {"x": 0.82, "y": 0.72, "label": "Ardee — cheap + high return", "c": ARDEE},
     {"x": 0.34, "y": 0.80, "label": "Gravita — quality, pay up", "c": GRAV},
     {"x": 0.22, "y": 0.40, "label": "Pondy — pricey, thin margin", "c": PONDY},
   ],
   "note": "The dream is top-right: cheap AND high quality. Ardee screens there — if its numbers hold.",
   "color": VAL},
  "Let's put it all on one map. [pause] "
  "Across the bottom, cheap to expensive. "
  "Up the side, low quality to high quality. [pause] "
  "Gravita sits top left. High quality, but you pay a full price for it. "
  "Pondy sits lower and to the left. Pricey, with the thinnest margins. "
  "And Ardee sits top right. "
  "The cheapest, with the strongest returns. [pause] "
  "Top right is the dream corner. Cheap and good. "
  "Ardee screens there, if, and only if, its numbers hold up. "
  "And checking whether they hold is what the last chapters are for."),

 ("s14_recap", "fa_recap",
  {"kicker": "RECAP · CHAPTER 4", "title": "Valuation in one breath",
   "items": [
     "Price is what you pay; value is what you get",
     "Market cap = price × shares (the equity tag)",
     "Enterprise value = market cap + debt − cash (true takeover price)",
     "P/E = price ÷ EPS — ₹ paid per ₹1 of profit",
     "EV/EBITDA is fairer — it accounts for debt",
     "Ardee: P/E ≈ 25×, EV/EBITDA ≈ 15× — cheapest of the three",
     "A low multiple = bargain OR warning; context decides",
   ],
   "closer": "You now know quality and price. Next: the risk hiding in the debt.",
   "color": VAL},
  "Let's lock in chapter four. [pause] "
  "Price is what you pay, value is what you get. "
  "Market cap is the price of the shares. "
  "Enterprise value adds debt and removes cash, for the true cost of the whole business. [pause] "
  "The P E tells you the price per rupee of profit. "
  "E V to EBITDA does the same, but fairer, because it counts debt. "
  "On both, Ardee looks the cheapest of our three companies. [pause] "
  "But a low multiple is a question, not an answer. "
  "To answer it, we need to look at the risk. "
  "And risk lives in the debt. That's chapter five. Thanks for watching."),

 ],
}

# ════════════════════════════════════════════════════════════════════════════
# CHAPTER 5 — LEVERAGE & SOLVENCY  (debt, D/E, net debt, coverage, liquidity)
# Ardee (approx): debt 180 · equity 300 · cash 30 · EBIT 127 · EBITDA 147 · interest 18
#   D/E = 180/300 = 0.6x (down from ~1.25 pre-IPO) · net debt = 150 · net D/E 0.5
#   interest coverage = 127/18 ≈ 7x · Debt/EBITDA = 180/147 ≈ 1.2x
#   Peers D/E: Gravita 0.14, Pondy 0.17 (near debt-free)
# ════════════════════════════════════════════════════════════════════════════
CH05 = {
 "id": "ch05",
 "title": "Leverage",
 "segments": [

 ("s01_divider", "fa_divider",
  {"n": 5, "title": "Leverage", "sub": "debt: cheap fuel, and hidden risk", "color": DEBT, "total": 7},
  "Chapter five. Leverage. [pause] "
  "In chapter four, Ardee looked cheap. "
  "Now we hunt for the reason why. "
  "And very often, the answer is hiding in one place. The debt."),

 ("s02_analogy", "fa_analogy",
  {"kicker": "ANALOGY · THE DOUBLE-EDGED SWORD", "title": "Debt is like driving faster",
   "left": {"emoji": "🏎️", "label": "More speed", "cap": "You reach the destination sooner.", "c": PROFIT},
   "right": {"emoji": "💥", "label": "More danger", "cap": "But any mistake becomes a bigger crash.", "c": COST},
   "note": "Debt magnifies returns when times are good — and magnifies losses when they aren't.",
   "color": DEBT},
  "Think of debt like pressing harder on the accelerator. [pause] "
  "When the road is clear, you get where you're going faster. "
  "Borrowed money lets a company grow quicker, and boosts returns. [pause] "
  "But the moment something goes wrong, "
  "that same speed becomes a much bigger crash. "
  "Interest still has to be paid, even in a bad year. [pause] "
  "So debt is a double-edged sword. "
  "It magnifies the good times, and it magnifies the bad. "
  "Our job is to measure how sharp that edge is."),

 ("s03_de", "fa_formula",
  {"kicker": "RATIO 1 · DEBT-TO-EQUITY", "title": "How much is borrowed vs owned",
   "name": "Debt-to-Equity  =  Total debt  ÷  Shareholders' equity",
   "num": [{"label": "Total debt", "val": 180, "c": DEBT}],
   "den": [{"label": "Equity", "val": 300, "c": TEAL}], "op": "÷",
   "result": {"label": "D/E — ₹ borrowed per ₹1 of owners' money", "val": 0.6, "unit": "×", "decimals": 1, "c": DEBT},
   "note": "Ardee ≈ 0.6× — down from about 1.25× before its IPO raised fresh equity.", "color": DEBT},
  "The first and most common measure is debt to equity. [pause] "
  "Simply, total debt divided by equity. "
  "It asks, for every rupee the owners have put in, how many rupees are borrowed? [pause] "
  "Ardee has about one eighty of debt against three hundred of equity. "
  "So its debt to equity is around zero point six. "
  "Here's an encouraging detail. "
  "Before its IPO, that number was closer to one point two five. "
  "The fresh money from listing paid down debt, and cut the ratio in half."),

 ("s04_de_read", "fa_keyidea",
  {"kicker": "READING D/E", "color": DEBT,
   "big": "Below 1 is comfortable. Above 2 starts to worry.",
   "sub": "But it's industry-specific — banks and infrastructure run high by design; asset-light firms run low."},
  "How do you read a debt to equity number? [pause] "
  "As a rough guide, below one is comfortable. "
  "The owners have more skin in the game than the lenders. [pause] "
  "Above two, and you should start paying close attention. "
  "The company leans heavily on borrowed money. [pause] "
  "But context matters, as always. "
  "Banks and infrastructure firms run high debt by their very nature. "
  "A software company runs almost none. "
  "So compare a company only to its own industry, and its own history."),

 ("s05_netdebt", "fa_formula",
  {"kicker": "RATIO 2 · NET DEBT", "title": "Debt, minus the cash you already hold",
   "name": "Net debt  =  Total debt  −  Cash",
   "num": [{"label": "Total debt", "val": 180, "c": DEBT}],
   "den": [{"label": "Cash", "val": 30, "c": PROFIT}], "op": "−",
   "result": {"label": "Net debt — the debt that truly remains", "val": 150, "unit": "₹ Cr", "decimals": 0, "c": DEBT},
   "note": "A company with more cash than debt is 'net cash' — the strongest position of all.", "color": DEBT},
  "Not all debt is equally worrying. [pause] "
  "If a company holds a big pile of cash, "
  "it could pay off some of its loans tomorrow. "
  "So we subtract cash from debt, to get net debt. [pause] "
  "Ardee's one eighty of debt, minus thirty of cash, "
  "is one hundred fifty of net debt. "
  "And when a company's cash is actually larger than its debt, "
  "we call it net cash. "
  "That's the strongest balance sheet a business can have."),

 ("s06_coverage", "fa_formula",
  {"kicker": "RATIO 3 · INTEREST COVERAGE", "title": "Can it comfortably pay the interest?",
   "name": "Interest coverage  =  Operating profit (EBIT)  ÷  Interest",
   "num": [{"label": "EBIT", "val": 127, "c": TEAL}],
   "den": [{"label": "Interest", "val": 18, "c": DEBT}], "op": "÷",
   "result": {"label": "Interest coverage — times over it earns its interest bill", "val": 7, "unit": "×", "decimals": 0, "c": PROFIT},
   "note": "Ardee earns its interest ~7× over. Below ~2–3× is a danger zone.", "color": DEBT},
  "Debt itself isn't dangerous. Not being able to pay it is. [pause] "
  "So the sharpest safety check is interest coverage. "
  "Operating profit, divided by the interest bill. "
  "It asks, how many times over can the company pay its interest? [pause] "
  "Ardee earns one twenty seven of operating profit, "
  "against an interest bill of just eighteen. "
  "That's about seven times cover. "
  "Very comfortable. [pause] "
  "If this number ever falls near two or three, that's a real warning sign."),

 ("s07_debtebitda", "fa_gauge",
  {"kicker": "RATIO 4 · DEBT / EBITDA", "title": "How many years to repay the debt?",
   "value": 1.2, "min": 0, "max": 5, "unit": "×",
   "zones": [{"to": 2, "c": PROFIT, "label": "safe"}, {"to": 3.5, "c": DEBT, "label": "watch"}, {"to": 5, "c": COST, "label": "stretched"}],
   "caption": "Ardee ≈ 1.2× — barely over a year of core profit would clear all its debt.",
   "note": "Debt ÷ EBITDA. Lenders watch this one closely. Under ~3× is generally comfortable.", "color": DEBT},
  "One more, and lenders love this one. Debt to EBITDA. [pause] "
  "It answers a simple question. "
  "Using its core profit, how many years would it take to repay all the debt? [pause] "
  "Ardee's one eighty of debt, against one forty seven of EBITDA, "
  "is about one point two. "
  "So in a little over a year, its core profit alone could wipe out every loan. [pause] "
  "Under three is generally comfortable. "
  "Above four or five, the company is carrying a heavy load."),

 ("s08_compare", "fa_bars",
  {"kicker": "LEVERAGE · THE THREE RIVALS", "title": "Here is why Ardee is 'cheap'",
   "unit": "×", "decimals": 2,
   "bars": [
     {"label": "Ardee", "val": 0.6, "c": ARDEE, "note": "most levered"},
     {"label": "Gravita", "val": 0.14, "c": GRAV, "note": "net cash"},
     {"label": "Pondy", "val": 0.17, "c": PONDY, "note": "near debt-free"},
   ],
   "note": "Debt-to-equity. Ardee carries far more debt than its peers — the single biggest reason for its discount.",
   "color": DEBT},
  "Now the chart that explains the whole puzzle. [pause] "
  "Debt to equity, across our three recyclers. "
  "Gravita and Pondy are almost debt-free, at around zero point one five. "
  "Ardee, at zero point six, carries far more debt. [pause] "
  "And there it is. "
  "This is the single biggest reason Ardee trades cheaper than its peers. "
  "The market is charging it a discount for the extra risk. [pause] "
  "The key question becomes, is Ardee paying that debt down fast enough "
  "to deserve a higher price later?"),

 ("s09_liquidity", "fa_keyidea",
  {"kicker": "SHORT-TERM SAFETY · LIQUIDITY", "color": REV,
   "big": "The current ratio asks: can it pay this year's bills?",
   "sub": "Current assets ÷ current liabilities. Above 1 means short-term assets cover short-term dues."},
  "Leverage is about long-term debt. "
  "But a company also has to survive the next twelve months. [pause] "
  "That's liquidity. "
  "The current ratio divides short-term assets by short-term bills. "
  "Above one means it can cover what's due this year. [pause] "
  "The quick ratio is stricter. "
  "It ignores inventory, because unsold stock can't pay a bill today. "
  "A company can be profitable on paper, "
  "and still fail if it can't pay its bills on time. "
  "Liquidity is what keeps the lights on."),

 ("s10_recap", "fa_recap",
  {"kicker": "RECAP · CHAPTER 5", "title": "Leverage in one breath",
   "items": [
     "Debt magnifies both returns and risk — a double-edged sword",
     "D/E = debt ÷ equity; below 1 comfortable, above 2 worrying",
     "Net debt = debt − cash; 'net cash' is strongest",
     "Interest coverage = EBIT ÷ interest (Ardee ≈ 7×, safe)",
     "Debt/EBITDA ≈ years to repay (Ardee ≈ 1.2×, low)",
     "Ardee is far more levered than Gravita/Pondy — the discount's cause",
     "Liquidity (current ratio) keeps the lights on short-term",
   ],
   "closer": "Debt explains the discount. Next: is the growth — and the cash — real?",
   "color": DEBT},
  "Let's lock in chapter five. [pause] "
  "Debt is a double-edged sword. It speeds you up, and it can crash you. "
  "Debt to equity shows how much is borrowed. Net debt takes out the cash. [pause] "
  "Interest coverage and debt to EBITDA both say Ardee's debt is very manageable, "
  "even though it carries more than its peers. "
  "And that extra leverage is exactly why the market prices it cheaply. [pause] "
  "The discount is now explained. "
  "But two questions remain. Is the growth real, and does the profit turn into cash? "
  "That's chapter six. Thanks for watching."),

 ],
}

# ════════════════════════════════════════════════════════════════════════════
# CHAPTER 6 — GROWTH & QUALITY  (CAGR, FCF, cash conversion, working capital)
# Ardee real 3-yr (public, approx): Revenue 463 → 743 → 1,168 · PAT 9 → 33 → 85
#   Revenue CAGR ≈ (1168/463)^(1/2) − 1 ≈ 57%
#   Illustrative cash: CFO ≈ 110 · Capex ≈ 70 · FCF ≈ 40 (capex-heavy, expanding)
# ════════════════════════════════════════════════════════════════════════════
CH06 = {
 "id": "ch06",
 "title": "Growth & Quality",
 "segments": [

 ("s01_divider", "fa_divider",
  {"n": 6, "title": "Growth & Quality", "sub": "is the growth real — and does it become cash?", "color": REV, "total": 7},
  "Chapter six. Growth, and quality. [pause] "
  "A cheap, well-run company is only exciting if it's also going somewhere. "
  "So now we measure growth. "
  "And then we ask the harder question. Is that growth actually worth anything?"),

 ("s02_ramp", "fa_bars",
  {"kicker": "GROWTH · ARDEE'S REVENUE", "title": "Three years of revenue",
   "unit": "", "decimals": 0,
   "bars": [
     {"label": "FY24", "val": 463, "c": REV, "note": "₹463 Cr"},
     {"label": "FY25", "val": 743, "c": TEAL, "note": "₹743 Cr"},
     {"label": "FY26", "val": 1168, "c": PROFIT, "note": "₹1,168 Cr"},
   ],
   "note": "Revenue more than doubled in two years — a compound annual growth rate of about 57%.",
   "color": REV},
  "Let's start with the good news. Growth. [pause] "
  "Here is Ardee's revenue over three years. "
  "Four hundred sixty three crore, then seven forty three, then eleven sixty eight. [pause] "
  "In just two years, revenue has more than doubled. "
  "Its profit grew even faster, from nine crore to eighty five. "
  "That is a seriously fast-growing company. "
  "But how do we describe that growth in a single, fair number?"),

 ("s03_cagr", "fa_keyidea",
  {"kicker": "THE SMOOTHED RATE · CAGR", "color": REV,
   "big": "CAGR is the one steady yearly rate that connects the start to the end.",
   "sub": "It smooths bumpy years into a single 'speed'. Ardee's revenue CAGR is about 57% a year."},
  "Growth is never smooth. Some years jump, some years dip. [pause] "
  "So we use CAGR. The compound annual growth rate. "
  "Think of it as one steady speed. [pause] "
  "It's the single yearly rate that would take you "
  "from the starting number to the ending number, if growth were perfectly smooth. "
  "For Ardee's revenue, that rate is about fifty seven percent a year. [pause] "
  "CAGR lets you compare the growth of any two companies, "
  "over any time period, on a level field. "
  "Just always check how many years it covers."),

 ("s04_quality", "fa_keyidea",
  {"kicker": "THE CATCH · QUALITY OF GROWTH", "color": TEAL,
   "big": "Growth is only good if it earns more than it costs — and turns into cash.",
   "sub": "Chasing revenue with heavy debt and no cash profit is how fast-growing companies go bust."},
  "But here is the trap that catches beginners. [pause] "
  "Not all growth is good growth. "
  "A company can grow revenue quickly by selling cheaply, or by piling on debt. [pause] "
  "That kind of growth actually destroys value, "
  "just like we saw in chapter three. "
  "Good growth has to clear the cost of capital. "
  "And it has to turn into real cash. [pause] "
  "Fast growth with no cash and rising debt "
  "is exactly how exciting companies quietly go bankrupt. "
  "So growth always needs a quality check."),

 ("s05_fcf", "fa_formula",
  {"kicker": "QUALITY 1 · FREE CASH FLOW", "title": "The cash left after keeping the lights on",
   "name": "Free cash flow  =  Operating cash flow  −  Capital spending",
   "num": [{"label": "Operating cash flow", "val": 110, "c": PROFIT}],
   "den": [{"label": "Capex", "val": 70, "c": COST}], "op": "−",
   "result": {"label": "Free cash flow — truly surplus cash", "val": 40, "unit": "₹ Cr", "decimals": 0, "c": PROFIT},
   "note": "Illustrative. Fast-growing firms spend heavily on capacity, so FCF is often thin — that's fine, if intentional.",
   "color": PROFIT},
  "The most honest measure of quality is free cash flow. [pause] "
  "Start with the cash the business actually generated from operations. "
  "Then subtract what it must spend on new plants and machines, called capex. "
  "What's left is free cash flow. Truly surplus money. [pause] "
  "For a company expanding as fast as Ardee, "
  "a lot of cash goes straight back into new capacity. "
  "So free cash flow is thin right now. "
  "That's acceptable, as long as it's a choice to grow, "
  "and not a sign the profit was never real."),

 ("s06_conversion", "fa_keyidea",
  {"kicker": "QUALITY 2 · CASH CONVERSION", "color": VAL,
   "big": "Does the paper profit actually show up as cash in the bank?",
   "sub": "Compare cash from operations to net profit. A healthy business converts most of its profit to cash."},
  "Remember our line from chapter one? [pause] "
  "Profit is an opinion. Cash is a fact. "
  "This is where we test it. [pause] "
  "We compare the cash a company generated from operations "
  "against the profit it reported. "
  "A healthy business turns most of its profit into actual cash. [pause] "
  "If profit keeps rising, but cash doesn't follow, "
  "something is wrong. "
  "Maybe customers aren't paying, or unsold stock is piling up. "
  "Cash conversion is the lie-detector of the income statement."),

 ("s07_workcap", "fa_keyidea",
  {"kicker": "QUALITY 3 · WORKING CAPITAL", "color": REV,
   "big": "Working capital is the cash trapped in day-to-day operations.",
   "sub": "Money stuck in unpaid invoices and unsold stock. The less trapped, the healthier the business."},
  "There's one more place cash hides. Working capital. [pause] "
  "Every business has money tied up in the everyday cycle. "
  "Stock sitting in the warehouse. "
  "Invoices customers haven't paid yet. [pause] "
  "That trapped cash is working capital. "
  "We even measure it in days. "
  "How many days until customers pay? "
  "How many days does stock sit before it sells? [pause] "
  "The faster a company collects its cash and turns its stock, "
  "the less money is trapped, and the healthier it is. "
  "For a commodity business, this discipline is everything."),

 ("s08_checklist", "fa_keyidea",
  {"kicker": "PUTTING QUALITY TOGETHER", "color": PROFIT,
   "big": "Great quality = growing, high returns, converts profit to cash, low debt.",
   "sub": "Ardee scores well on growth and returns; the things to watch are its cash conversion and debt."},
  "So let's define a quality business. [pause] "
  "It's growing. "
  "It earns high returns on capital. "
  "It turns its profit into cash. "
  "And it doesn't rely too heavily on debt. [pause] "
  "By that scorecard, Ardee is genuinely strong on growth and returns. "
  "The two things to keep watching "
  "are whether its profit is converting to cash, "
  "and whether its debt keeps falling. [pause] "
  "Growth plus quality is the rarest and most valuable combination in investing."),

 ("s09_recap", "fa_recap",
  {"kicker": "RECAP · CHAPTER 6", "title": "Growth & quality in one breath",
   "items": [
     "CAGR = the single smoothed yearly growth rate",
     "Ardee revenue: ₹463 → ₹743 → ₹1,168 Cr (~57% CAGR)",
     "Growth only counts if it beats the cost of capital",
     "Free cash flow = operating cash − capex (real surplus)",
     "Cash conversion: does profit become cash? (the lie-detector)",
     "Working capital = cash trapped in receivables + stock",
     "Quality = growing + high returns + cash + low debt",
   ],
   "closer": "You now have every tool. Next: read a whole company with them.",
   "color": REV},
  "Let's lock in chapter six. [pause] "
  "CAGR smooths bumpy growth into one steady rate. "
  "Ardee's revenue has compounded at about fifty seven percent. "
  "But growth only matters if it beats the cost of capital, and becomes cash. [pause] "
  "Free cash flow, cash conversion, and working capital "
  "are the three tests of quality. "
  "Ardee is strong on growth and returns, "
  "with cash conversion and debt as the things to watch. [pause] "
  "You now hold every tool in the kit. "
  "In our final chapter, we'll use all of them together, on one company, start to finish. "
  "Thanks for watching."),

 ],
}

# ════════════════════════════════════════════════════════════════════════════
# CHAPTER 7 — PUTTING IT TOGETHER  (the whole framework on one company)
# ════════════════════════════════════════════════════════════════════════════
CH07 = {
 "id": "ch07",
 "title": "Putting It Together",
 "segments": [

 ("s01_divider", "fa_divider",
  {"n": 7, "title": "Putting It Together", "sub": "reading a whole company, end to end", "color": PROFIT, "total": 7},
  "Chapter seven. Putting it all together. [pause] "
  "You now know every term. "
  "Revenue and profit, margins, returns, valuation, leverage and cash. "
  "In this final chapter, we use all of them, as one connected checklist."),

 ("s02_fivequestions", "fa_keyidea",
  {"kicker": "THE WHOLE FRAMEWORK", "color": TEAL,
   "big": "Every analysis is really just five questions.",
   "sub": "Is it growing? Are margins healthy? Are returns high? Is debt safe? Is the price fair?"},
  "Here's a comforting truth. [pause] "
  "Everything in this course collapses into just five questions. [pause] "
  "One. Is the business growing? "
  "Two. Are its margins healthy? "
  "Three. Does it earn high returns on capital? "
  "Four. Is its debt safe? "
  "And five. Is the price fair? [pause] "
  "Answer those five, in order, and you've done a real fundamental analysis. "
  "Let's run Ardee through all five, one last time."),

 ("s03_scorecard", "fa_ledger",
  {"kicker": "ARDEE · THE FULL SCORECARD", "title": "Five questions, five answers",
   "rows": [
     {"label": "1 · Growth", "val": "Revenue CAGR ~57%", "c": PROFIT, "bold": True},
     {"label": "2 · Margins", "val": "EBITDA 12.6% — best of peers", "c": PROFIT, "bold": True},
     {"label": "3 · Returns", "val": "ROCE ~26%  (>> ~12% cost)", "c": PROFIT, "bold": True},
     {"label": "4 · Leverage", "val": "D/E 0.6× — highest of peers", "c": DEBT, "bold": True},
     {"label": "5 · Valuation", "val": "EV/EBITDA ~15× — cheapest", "c": VAL, "bold": True},
   ],
   "caption": "Four green lights, one amber (debt). Approx figures — verify before acting.",
   "color": TEAL},
  "Here's the whole scorecard on one screen. [pause] "
  "Growth? Revenue compounding at fifty seven percent. A green light. "
  "Margins? The best of its three peers. Green. "
  "Returns? Around twenty six percent, double its cost of capital. Green. [pause] "
  "Leverage? More debt than its rivals. That's the one amber light. "
  "Valuation? The cheapest of the three, on E V to EBITDA. Green. [pause] "
  "So four green lights, and one to watch. "
  "In a single glance, that's the entire investment case."),

 ("s04_compare", "fa_compare",
  {"kicker": "THE FINAL COMPARISON", "title": "Three recyclers, side by side",
   "cos": [
     {"name": "Ardee", "c": ARDEE, "tag": "cheap + risky",
      "stats": [{"k": "EBITDA margin", "v": "12.6%", "hot": True}, {"k": "ROCE", "v": "~26%", "hot": True},
                {"k": "D/E", "v": "0.6×", "hot": True}, {"k": "EV/EBITDA", "v": "~15×", "hot": True}]},
     {"name": "Gravita", "c": GRAV, "tag": "quality leader",
      "stats": [{"k": "EBITDA margin", "v": "10.6%"}, {"k": "ROCE", "v": "high"},
                {"k": "D/E", "v": "0.14×"}, {"k": "EV/EBITDA", "v": "~26×"}]},
     {"name": "Pondy", "c": PONDY, "tag": "pricey",
      "stats": [{"k": "EBITDA margin", "v": "7.4%"}, {"k": "ROCE", "v": "mid"},
                {"k": "D/E", "v": "0.17×"}, {"k": "EV/EBITDA", "v": "~25×"}]},
   ],
   "note": "Same business, three profiles: Ardee cheap+levered, Gravita quality+net-cash, Pondy pricey+thin.",
   "color": TEAL},
  "Now the same five questions, across all three rivals. [pause] "
  "Ardee has the fattest margins, the cheapest price, but the most debt. "
  "Gravita is the quality leader. Net cash, proven, but you pay up for it. "
  "Pondy is the priciest, with the thinnest margins. [pause] "
  "See how the numbers paint three completely different characters, "
  "from the very same business? "
  "That is fundamental analysis doing its job. "
  "It turns a vague feeling into a clear, comparable picture."),

 ("s05_cyclical", "fa_keyidea",
  {"kicker": "KNOW THE BUSINESS TYPE", "color": DEBT,
   "big": "A recycler is a cyclical — its fortunes swing with the metal price.",
   "sub": "Cyclicals can look cheapest at the top of the cycle. Never judge one on a single great year."},
  "One vital warning before you use any of this. [pause] "
  "Know what kind of business you're holding. "
  "Our three recyclers are cyclical companies. "
  "Their profits rise and fall with the price of lead. [pause] "
  "And cyclicals play a nasty trick. "
  "They often look cheapest, on a low P E, "
  "right at the very top of their cycle, "
  "just before profits fall. [pause] "
  "So never judge a cyclical on one brilliant year. "
  "Look across a full cycle, "
  "and ask whether these margins and returns can actually last."),

 ("s06_redflags", "fa_keyidea",
  {"kicker": "THE RED FLAGS", "color": COST,
   "big": "Profit rising but cash flat. Debt climbing. Margins slipping.",
   "sub": "Any one of these is a reason to dig deeper — or to walk away. Numbers hide stories."},
  "Let's also name the warning signs. The red flags. [pause] "
  "Profit that keeps rising, while cash flow stays flat. "
  "Debt that climbs, year after year. "
  "Margins that quietly slip. [pause] "
  "A company that reports profit, but never seems to have any money. "
  "Promoters selling or pledging their own shares. [pause] "
  "None of these, on its own, proves anything is wrong. "
  "But each one is a reason to slow down, and dig deeper. "
  "The numbers always hide a story. Your job is to find it."),

 ("s07_verdict", "fa_keyidea",
  {"kicker": "THE HONEST VERDICT", "color": PROFIT,
   "big": "Ardee screens as cheap and high-quality — if the debt keeps falling and profit turns to cash.",
   "sub": "That 'if' is the whole game. A screen is where research starts, never where it ends."},
  "So what's the verdict on Ardee? [pause] "
  "On the numbers, it screens beautifully. "
  "Cheap, fast-growing, and highly profitable. "
  "The dream top-right corner of our map. [pause] "
  "But it rests on two ifs. "
  "If the debt keeps falling. "
  "And if that paper profit keeps turning into real cash. [pause] "
  "That word, if, is the whole game. "
  "A good screen tells you where to start digging. "
  "It never, ever tells you to stop. "
  "Now you know exactly what to dig for."),

 ("s08_recap", "fa_recap",
  {"kicker": "THE WHOLE COURSE · IN ONE BREATH", "title": "Everything, on one page",
   "items": [
     "The statements: revenue → costs → profit; cash ≠ profit",
     "Margins: the keep-rate; judge against the industry",
     "Returns: ROE & ROCE — must beat the cost of capital",
     "Valuation: market cap, EV, P/E, EV/EBITDA — price vs value",
     "Leverage: debt magnifies returns AND risk",
     "Growth & quality: real growth turns into cash",
     "Together: five questions — grow, margin, return, debt, price",
   ],
   "closer": "Buy good businesses at fair prices — and always do your own homework.",
   "color": TEAL},
  "Let's bring the whole course together, in one breath. [pause] "
  "The statements show revenue becoming profit, and remind us cash is king. "
  "Margins are the keep-rate. Returns must beat the cost of capital. [pause] "
  "Valuation compares price to value, through market cap, E V and the multiples. "
  "Leverage magnifies everything, good and bad. "
  "And real growth always turns into cash. [pause] "
  "It all reduces to five questions. "
  "Is it growing, profitable, high-returning, safely financed, and fairly priced? "
  "Answer those, and you can read any company in the world. [pause] "
  "One last, important word. "
  "This has been education, not investment advice. "
  "Every figure here was approximate, from public sources. "
  "Always verify the latest numbers yourself, "
  "and talk to a registered financial advisor before you invest. [pause] "
  "Buy good businesses, at fair prices, and always do your own homework. "
  "Thank you for watching this course."),

 ],
}

CHAPTERS = [CH01, CH02, CH03, CH04, CH05, CH06, CH07]
