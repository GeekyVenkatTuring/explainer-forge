#!/usr/bin/env python3
"""The Trader's Toolkit (ENGLISH) — helper platforms for Indian traders, July 2026.
Reuses `sm` scene set (ptitle, divider, iconcards, compare3, steps, myths, checklist, recap).
6 chapter PARTs: Screeners/Fundamentals · Charting · Options · Backtesting/Algo · Research/Portfolio · Learning.
Data validation (skills/12-market-research.md):
- Screener.in premium ₹4,999/yr — VERIFIED from screener.in/premium 24-Jul-2026 (aggregators wrongly said ₹10k).
- Sensibull Pro free for Zerodha users — 2 independent sources (AlgoTest blog, optionsscanners.com); own pricing
  page is JS-only, so NO exact ₹ quoted for other brokers.
- Trendlyne from ~₹119/mo, Tickertape from ~₹249/mo — single-source (techjockey); marked "~" + "check site".
- Quantsapp/Streak/StockEdge prices NOT quoted (unverified) — tiers described qualitatively.
- "Momentum Hunter" search results were syndicated PR spam — excluded.
Not sponsored, not affiliated, not advice. Prices "as of Jul 2026, check site" framing throughout.
Usage: python3 build.py            |   python3 build.py tte
"""
import json, os, re, subprocess, sys, time

VOICE = "en-IN-NeerjaNeural"; RATE = "-4%"; GAP = 0.5; PAUSE = 0.55; PREFIX = "sm"
ROOT = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(ROOT, "..", ".."))
PUBLIC = os.path.join(REPO, "composer", "public", PREFIX); RAW = os.path.join(ROOT, "assets", "raw"); FIN = os.path.join(ROOT, "assets")
for d in (PUBLIC, RAW, os.path.join(ROOT, "artifacts"), os.path.join(ROOT, "renders")):
    os.makedirs(d, exist_ok=True)

G = "#34D399"; C = "#22D3EE"; V = "#A78BFA"; A = "#FBBF24"; R = "#FB7185"

CHAPTERS = {
 "tte": [
 ("tt_title", "sm_ptitle",
  {"title": "The Trader's Toolkit", "sub": "Screener.in · Sensibull · TradingView · Streak & more — the platforms that do the homework", "kicker": "TOOLS GUIDE · 2026"},
  "Your broker app can place a trade in one second. But it can't tell you WHICH trade. [pause] "
  "That's why serious traders quietly use a second layer of platforms — screeners, options analysers, charting tools, backtesters. Most have generous free plans. Most beginners have never heard of them. [pause] "
  "In this video: the full toolkit — what each platform does, what's free, and how to combine them into a workflow. [pause] "
  "One note before we start. This video is not sponsored by any platform, and it is not investment advice. Prices are as of July 2026 — always check the site for current plans."),
 ("tt_map", "sm_steps",
  {"kicker": "THE MAP", "title": "A Trade Has Six Jobs — Each Has a Tool", "color": C,
   "items": [
    {"emoji": "🔍", "label": "Screen", "sub": "Filter 5,000 stocks to 20", "c": G},
    {"emoji": "📚", "label": "Research", "sub": "Read the company's numbers", "c": G},
    {"emoji": "📈", "label": "Chart", "sub": "Time the entry & exit", "c": C},
    {"emoji": "🎯", "label": "Strategise", "sub": "Build the F&O position", "c": V},
    {"emoji": "🧪", "label": "Backtest", "sub": "Test the rule on history", "c": A},
   ],
   "note": "…and job #6 underneath them all: 🎓 LEARN. The broker app only EXECUTES — these jobs before the order are where trades are won."},
  "Here's the map for this whole video. Every trade has six jobs. [pause] "
  "Screen — filter five thousand listed stocks down to twenty worth your time. Research — read the company's actual numbers. Chart — time your entry and exit. [pause] "
  "Then, for F and O traders — strategise, building the option position. Backtest — test your rule on years of history BEFORE risking money. And underneath it all — learn. [pause] "
  "Your broker app does none of these. It only executes. So we'll take the six jobs one by one, and meet the best platforms for each. Six parts. Let's go."),
 ("tt_div1", "sm_divider",
  {"n": 1, "title": "Screeners & Fundamentals", "sub": "Screener.in · Trendlyne · Tickertape · StockEdge", "color": G},
  "Part one. Screeners and fundamentals — the tools that turn five thousand stocks into a shortlist."),
 ("tt_screener2", "tt_screener",
  {},
  "The workhorse of Indian fundamental research — Screener dot in. Let me show you, live, on screen. [pause] "
  "Watch the query box. I type a filter in plain language — return on capital above twenty, debt to equity below zero point three. And hit run. [pause] "
  "Now watch the table. The weak companies get struck out one by one — high debt, low returns, gone. Five thousand listed stocks collapse to just twenty-three matches. [pause] "
  "Every survivor gets a green PASS badge, and each one links to a clean page with ten years of sales, profits, margins and shareholding. [pause] "
  "The free plan covers everything you just saw. Premium is four thousand nine hundred ninety-nine rupees a year for alerts and Excel exports. If you bookmark one site from this video — make it this one."),
 ("tt_trio2", "tt_trio",
  {},
  "Three modern screeners build on that base — and each has a signature visual. Watch. [pause] "
  "On the left, Trendlyne's D-V-M score. Three rings filling up — Durability seventy-two, Value fifty-eight, Momentum eighty-one. Quality, price and trend, each compressed into one honest number. [pause] "
  "In the middle, Tickertape's Market Mood Index. Watch the needle swing — past fear, into the greed zone at sixty-two. One glance tells you if the whole market is euphoric or terrified. [pause] "
  "And on the right, StockEdge — a phone-first app whose daily scans light up: fifty-two week breakouts, volume spikes, F-I-I buying. Analytics in your pocket. [pause] "
  "Trendlyne from around one hundred nineteen rupees a month, Tickertape from around two forty-nine — as of July 2026, check the sites. Start free on all three."),
 ("tt_div2", "sm_divider",
  {"n": 2, "title": "Charting & Technicals", "sub": "TradingView · Chartink", "color": C},
  "Part two. Charting — because even a great stock bought at the wrong time feels like a bad stock."),
 ("tt_tv2", "tt_tv",
  {},
  "For charts, one platform became the global standard — TradingView. Watch a chart come alive. [pause] "
  "First the candles draw in — green for up days, red for down days — each one a day's battle between buyers and sellers. [pause] "
  "Then the yellow line glides over them — a moving average, smoothing the noise into a trend you can actually see. [pause] "
  "Next, a trendline snaps onto the lows — that's the drawing toolbar on the left, every tool a pro uses. [pause] "
  "And below, a second pane — the R-S-I — oscillating between overbought at seventy and oversold at thirty. Price above, momentum below: one screen, the full story. [pause] "
  "Indian brokers like Zerodha and Dhan connect directly, so the trade happens from the chart. The free plan is genuinely usable — learn here before paying anyone for a special indicator."),
 ("tt_chartink2", "tt_chartink",
  {},
  "TradingView charts one stock beautifully. But which stock should you even open? That's Chartink — watch a scan get built. [pause] "
  "Condition one slides in: R-S-I crossed above sixty. Condition two: price above the two-hundred-day average. Condition three: volume double its normal. All picked from dropdowns — zero code. [pause] "
  "Now — run scan. [pause] "
  "The results populate in real time: five stocks out of the whole N-S-E pass all three conditions, each with today's move drawn as a bar. That's your day's watchlist, built in thirty seconds, for free. [pause] "
  "So parts one and two combine into a funnel: a fundamental screen finds good companies. Chartink finds which are moving now. TradingView times the entry. Shortlist, signal, timing."),
 ("tt_div3", "sm_divider",
  {"n": 3, "title": "Options & F&O Analytics", "sub": "Sensibull · Opstra · Quantsapp", "color": V},
  "Part three. Options — where trading without an analytics tool is like flying blind in a storm."),
 ("tt_sensibull2", "tt_sensibull",
  {},
  "Now, Sensibull — India's largest options platform. Watch it build a real strategy, live. [pause] "
  "Step one — pick a view. We tap bullish. It suggests a bull call spread. [pause] "
  "Step two — the legs appear. Buy the twenty-three thousand eight hundred call for one hundred fifty rupees. Sell the twenty-four thousand call, collecting sixty back. Net cost: ninety points. [pause] "
  "And now — the part that saves accounts. The payoff graph draws itself. [pause] "
  "Look at the numbers popping in: maximum profit — one hundred ten. Maximum loss — capped at ninety. Breakeven — twenty-three thousand eight ninety, marked in yellow. Every rupee of risk visible BEFORE the order is placed. [pause] "
  "Most option losses come from traders who discovered their real risk after entry. This graph is how you never become one of them. Pro is free for Zerodha users, paid on other brokers — as of July 2026."),
 ("tt_optools", "sm_iconcards",
  {"kicker": "THE DEEPER BENCH", "title": "Opstra · Quantsapp · NiftyTrader", "color": V,
   "items": [
    {"emoji": "🔬", "k": "Opstra (Definedge)", "v": "Deeper strategy analytics — IV charts, futures OI, strategy simulation for serious F&O students", "chip": "ANALYSIS"},
    {"emoji": "🧠", "k": "Quantsapp", "v": "Pro-grade options data platform — treats options as a data problem; premium pricing", "chip": "PRO"},
    {"emoji": "🆓", "k": "NiftyTrader", "v": "Free option chain, max-pain, PCR and FII/DII pages — a solid zero-cost daily reference", "chip": "FREE"},
    {"emoji": "⚖️", "k": "How to choose", "v": "Start Sensibull/NiftyTrader free → graduate to Opstra/Quantsapp only when strategies get complex", "chip": "LADDER"},
   ]},
  "Three more names complete the options bench. [pause] "
  "Opstra, from Definedge, goes deeper on analytics — implied-volatility charts, futures open interest, and strategy simulation. Traders who study their positions love it. [pause] "
  "Quantsapp is the professional end — a data-heavy platform for traders who treat options as a numbers problem, at premium prices. [pause] "
  "And NiftyTrader dot in is the free daily reference — option chain, max pain, put-call ratio, and F-I-I data, at zero cost. [pause] "
  "The ladder is simple: start free with Sensibull and NiftyTrader. Graduate to Opstra or Quantsapp only when your strategies genuinely get complex. Part three done — never trade an option without seeing its payoff first."),
 ("tt_div4", "sm_divider",
  {"n": 4, "title": "Backtesting & Algos", "sub": "Streak · AlgoTest · Stockmock · Tradetron", "color": A},
  "Part four. Backtesting — the difference between 'I think this works' and 'I tested this on ten years of data'."),
 ("tt_backtest2", "tt_backtest",
  {},
  "So you have a trading rule. Does it actually work? Watch a backtest answer that in seconds. [pause] "
  "The rule types itself in plain English — buy when price crosses the twenty-day high, stop loss one percent, target two. That's Streak, from the Zerodha stable — no code anywhere. Hit backtest. [pause] "
  "And here comes the equity curve — sixty trades compressed into one line. Watch it climb... stumble... and climb again. [pause] "
  "See that red valley in the middle? That's the max drawdown — the deepest fall from a peak. The backtest is asking you an honest question: could you have sat through that without quitting? [pause] "
  "The stats land at the bottom — sixty trades, a fifty-something percent win rate, two-to-one average win. A real edge, but a bumpy one. [pause] "
  "AlgoTest does this for F and O strategies with free core backtests; Stockmock for intraday options; Tradetron deploys strategies live. One honest warning before you fall in love with a backtest — next scene."),
 ("tt_btmyths", "sm_myths",
  {"kicker": "BACKTEST HONESTLY", "title": "What a Backtest Says vs What It Doesn't", "mythLabel": "😍 THE BACKTEST SAYS", "factLabel": "⚠️ REALITY CHECK",
   "pairs": [
    {"m": "This rule made 40% a year for 10 years", "f": "Past patterns can stop working — a backtest is evidence, not a guarantee"},
    {"m": "I tweaked it until the curve looked perfect", "f": "That's overfitting — you optimised for history, not the future"},
    {"m": "The backtest ignores costs", "f": "Brokerage, slippage & taxes eat thin edges — always include them"},
   ]},
  "Here's what a backtest says, versus what it doesn't. [pause] "
  "The backtest says: this rule made forty percent a year for ten years. Reality: past patterns can stop working. A backtest is evidence — never a guarantee. [pause] "
  "You tweaked parameters until the curve looked perfect? That's called overfitting — you optimised for history, and history won't repeat exactly. Test on data the rule has never seen. [pause] "
  "And most backtests quietly ignore brokerage, slippage and taxes — which eat thin edges alive. Always include costs. [pause] "
  "Used honestly, backtesting is the single best filter between a real edge and a story you told yourself. That's part four."),
 ("tt_div5", "sm_divider",
  {"n": 5, "title": "Research, News & Portfolio", "sub": "Moneycontrol · Value Research · Chittorgarh · smallcase", "color": G},
  "Part five. The information layer — news, mutual funds, IPOs, and ready-made portfolios."),
 ("tt_infowall2", "tt_infowall",
  {},
  "Next, the information layer — four dashboards where you check facts, not opinions. [pause] "
  "Top left, Moneycontrol — watch the headlines stream past. News, results, and the portfolio tracker most of India already uses. [pause] "
  "Top right, Value Research — the mutual fund referee. Watch the stars fill in: independent ratings that cut through fund-house marketing. [pause] "
  "Bottom left, Chittorgarh — the I-P-O tracker. Those bars filling up are subscription numbers by category — Q-I-B, N-I-I, retail. And note the warning: the grey-market premium shown there is unofficial data, never a listing prediction. [pause] "
  "And bottom right — the N-S-E and B-S-E official sites: announcements, F-I-I flows, circulars. Remember the pulsing line: when two websites disagree on a number, the exchange wins."),
 ("tt_smallcase2", "tt_smallcase",
  {},
  "One more platform sits between doing it yourself and mutual funds — smallcase. Watch how a basket comes together. [pause] "
  "Five stocks fly in, one by one — a bank, an I-T name, a jeweller, an engineer, a pharma company — each with a weight. Twenty-two percent, twenty-four, eighteen... until the total locks at exactly one hundred. [pause] "
  "That's a smallcase: a curated basket around a theme, built and rebalanced by a SEBI-registered manager. [pause] "
  "And the clever part — follow the particles flowing to the right. The basket executes through your own broker, so every share lands in YOUR demat, under your control. [pause] "
  "Free smallcases exist; managed ones charge subscription fees — read the fee page first. And remember: structure and discipline, yes. A shortcut past understanding what you own — no. That's part five."),
 ("tt_div6", "sm_divider",
  {"n": 6, "title": "Learning Platforms", "sub": "Zerodha Varsity · SEBI Investor Education", "color": R},
  "Part six — the layer under everything else. Learning. Because no tool can outperform its user."),
 ("tt_learn2", "tt_learn",
  {},
  "Every platform so far amplifies your decisions. This part makes the decisions better. [pause] "
  "Watch the bookshelf build — Zerodha Varsity's modules rising one by one: intro to markets, technical analysis, fundamentals, futures, options theory, taxation. Every single one free. Watch the progress bars fill — that's you, module by module, at your own pace. [pause] "
  "If you read nothing else in this entire video, read Varsity. [pause] "
  "SEBI and the exchanges add official investor education — your rights and scam warnings from the regulator itself. TradingQnA, Zerodha's forum, answers the practical questions no course covers. [pause] "
  "And the red panel on the right is what to run from: guaranteed returns, sure-shot paid tips, unregistered advisors, profit-screenshot bragging. If returns are guaranteed — walk away. Learn before you leverage."),
 ("tt_stack", "sm_compare3",
  {"kicker": "PICK YOUR STACK", "title": "Three Trader Types, Three Toolkits",
   "cols": [
    {"name": "Long-term Investor", "color": G, "emoji": "🌱", "rows": [
     {"k": "Screen", "v": "Screener.in"},
     {"k": "Research", "v": "Value Research · NSE"},
     {"k": "Portfolio", "v": "smallcase / Coin"},
     {"k": "Learn", "v": "Varsity basics"},
    ]},
    {"name": "Swing Trader", "color": C, "emoji": "📈", "hi": True, "rows": [
     {"k": "Screen", "v": "Chartink scans"},
     {"k": "Chart", "v": "TradingView"},
     {"k": "Backtest", "v": "Streak"},
     {"k": "News", "v": "Moneycontrol"},
    ]},
    {"name": "Options Trader", "color": V, "emoji": "🎯", "rows": [
     {"k": "Strategy", "v": "Sensibull"},
     {"k": "Data", "v": "NiftyTrader · Opstra"},
     {"k": "Backtest", "v": "AlgoTest"},
     {"k": "Learn", "v": "Varsity F&O module"},
    ]},
   ]},
  "So which tools do YOU need? Not all of them. Pick the stack that matches your style. [pause] "
  "A long-term investor needs just four: Screener dot in to filter, Value Research for funds, smallcase or Coin for the portfolio, and Varsity's basics. [pause] "
  "A swing trader lives in a different stack: Chartink scans to find movers, TradingView to time entries, Streak to test the rules, Moneycontrol for news. [pause] "
  "An options trader: Sensibull for strategy and payoff, NiftyTrader and Opstra for data, AlgoTest for backtests, and Varsity's F and O module — twice. [pause] "
  "Notice something: every stack starts free. Three or four tools, not fifteen."),
 ("tt_toolmyths", "sm_myths",
  {"kicker": "TOOL TRAPS", "title": "Myths About Trading Tools", "mythLabel": "🧨 THE MYTH", "factLabel": "✅ THE TRUTH",
   "pairs": [
    {"m": "A paid tool will make me profitable", "f": "Tools improve decisions — they don't create an edge you don't have"},
    {"m": "More tools = better trading", "f": "Tool-hopping is procrastination; masters use 3–4 tools deeply"},
    {"m": "The screener's output is a buy list", "f": "A screen is a SHORTLIST — research each name before buying"},
   ]},
  "Before the checklist, three myths about tools themselves. [pause] "
  "Myth one: a paid tool will make me profitable. Truth: tools improve your decisions — they cannot create an edge you don't have. A payoff graph shows the risk; it doesn't remove it. [pause] "
  "Myth two: more tools means better trading. Truth: tool-hopping is a sophisticated form of procrastination. The best traders use three or four tools, deeply. [pause] "
  "Myth three: the screener's output is a buy list. Truth: a screen is a shortlist. Twenty names out of five thousand still need research — that's the next tool's job, and finally yours."),
 ("tt_choose", "sm_checklist",
  {"kicker": "BEFORE YOU PAY", "title": "The 5-Point Tool Checklist", "color": A, "icon": "🧰",
   "items": [
    "Start with FREE tiers — they cover 80% of a beginner's needs",
    "One tool per job — screen, chart, options, backtest; skip overlap",
    "Verify pricing on the official site — plans change, videos age",
    "Pay for a tool only when its free tier is the thing limiting you",
    "No tool replaces learning — Varsity before any paid subscription",
   ]},
  "So here's the five-point checklist before you spend a rupee on any platform. [pause] "
  "One — start with free tiers. Screener, Chartink, TradingView, Sensibull on Zerodha, NiftyTrader, Varsity — free covers eighty percent of a beginner's needs. [pause] "
  "Two — one tool per job. A screener, a chart, an options tool, a backtester. Overlapping subscriptions are wasted money. [pause] "
  "Three — verify pricing on the official site. Plans change; videos like this one age. [pause] "
  "Four — pay only when the free tier is genuinely the thing limiting you. Not before. [pause] "
  "And five — no tool replaces learning. Finish the relevant Varsity module before any paid subscription. The order matters."),
 ("tt_recap", "sm_recap",
  {"title": "The Trader's Toolkit — At a Glance",
   "items": [
    "Screen: Screener.in (free · ₹4,999/yr) · Trendlyne · Tickertape · StockEdge",
    "Chart: TradingView (global standard) + Chartink (free NSE scans)",
    "Options: Sensibull (payoff first!) · Opstra · NiftyTrader (free)",
    "Backtest: Streak · AlgoTest · Stockmock — mind overfitting & costs",
    "Info & learning: Moneycontrol · Value Research · Chittorgarh · VARSITY",
   ],
   "closer": "Every stack starts free. Three or four tools, used deeply — and learning underneath it all."},
  "The full toolkit, at a glance. [pause] "
  "To screen: Screener dot in — free, or four thousand nine hundred ninety-nine a year — plus Trendlyne, Tickertape and StockEdge. [pause] "
  "To chart: TradingView, the global standard, with Chartink for free N-S-E scans. [pause] "
  "For options: Sensibull — payoff graph before every trade — with Opstra and NiftyTrader. To backtest: Streak, AlgoTest, Stockmock — honestly, including costs. [pause] "
  "And the information layer: Moneycontrol, Value Research, Chittorgarh for I-P-Os — with Zerodha Varsity underneath it all, free. [pause] "
  "Remember the pattern: every stack starts free, and three or four tools used deeply beat fifteen used shallowly. [pause] "
  "This video is not sponsored by any platform. Prices are as of July 2026 — check each site. And none of this is investment advice; consult a SEBI-registered advisor before investing. Thanks for watching — and happy building."),
 ],
}

def ffdur(path):
    out = subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","default=noprint_wrappers=1:nokey=1",path],capture_output=True,text=True,check=True)
    return round(float(out.stdout.strip()),3)

def tts_chunk(path, text):
    mp3 = path[:-4]+".mp3"
    for a in range(6):
        r = subprocess.run(["edge-tts","--voice",VOICE,f"--rate={RATE}","--text",text,"--write-media",mp3],capture_output=True)
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
        print(f"  {sid:14s} {dur:6.2f}s",flush=True)
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
