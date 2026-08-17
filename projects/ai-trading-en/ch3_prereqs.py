#!/usr/bin/env python3
"""Chapter 3 — Part 3: What you need before you start."""
import aitcore as core

SEGMENTS = [
 ("s30_divider", "ait_divider",
  {"n": 3, "title": "Before You Start", "sub": "The skills, the money, the mindset", "color": "edge", "parts": 6},
  "Part three. What you actually need before you start. [pause] Good news. It is less "
  "than the gurus tell you. But it is also different from what beginners expect."),

 ("s31_prereq", "ait_orbit",
  {"kicker": "THE FOUR PILLARS", "title": "Four skills hold up every AI trader",
   "hub": {"emoji": "🎯", "label": "A working trader", "c": "edge"},
   "items": [
     {"emoji": "📚", "label": "Market basics", "sub": "how trading works", "c": "data"},
     {"emoji": "📊", "label": "A little statistics", "sub": "probability, not calculus", "c": "money"},
     {"emoji": "🐍", "label": "Basic Python", "sub": "enough to glue tools", "c": "ai"},
     {"emoji": "🛡️", "label": "Risk discipline", "sub": "the one that matters most", "c": "risk"}]},
  "There are four pillars, and you need all four. [pause] One, market basics. How "
  "orders, prices, and settlement actually work. [pause] Two, a little statistics. And "
  "I mean a little. Probability and averages, not university calculus. [pause] Three, "
  "basic Python. Just enough to glue tools together and read data. [pause] And four, "
  "risk discipline. [pause] Here is the surprise. That last pillar, risk, matters more "
  "than the other three combined. The people who last are not the best coders or the "
  "best forecasters. They are the ones who never blow up. Let's walk each pillar."),

 ("s32_markets", "ait_cards",
  {"kicker": "PILLAR ONE · MARKETS", "title": "The market basics you can't skip", "color": "data",
   "cards": [
     {"emoji": "📗", "title": "Orders & spreads", "body": "Market vs limit orders, and the bid-ask gap you pay.", "c": "data"},
     {"emoji": "🕒", "title": "Liquidity & timing", "body": "Why thin stocks and open/close are dangerous for bots.", "c": "edge"},
     {"emoji": "⚖️", "title": "Leverage & margin", "body": "How borrowed money multiplies losses, not just gains.", "c": "risk"},
     {"emoji": "🧾", "title": "Settlement & taxes", "body": "T-plus-one settlement, STT, and how gains are taxed.", "c": "money"}]},
  "Pillar one. Market basics. You cannot automate what you do not understand. [pause] "
  "Know your order types. A market order fills instantly but pays the spread. A limit "
  "order controls your price but might not fill. [pause] Understand liquidity. In a "
  "thinly traded stock, or in the chaos at the open and close, your bot can get "
  "terrible prices. [pause] Respect leverage. Borrowed money multiplies your losses "
  "just as fast as your gains, and it is how most accounts die. [pause] And learn "
  "settlement and taxes. When trades settle, and how your gains are taxed. For India, "
  "Zerodha's free Varsity is the best place to learn all of this properly."),

 ("s33_math", "ait_cards",
  {"kicker": "PILLAR TWO · STATISTICS", "title": "The tiny bit of math that matters", "color": "money",
   "cards": [
     {"emoji": "🎲", "title": "Expectancy", "body": "Win rate times average win, minus loss rate times average loss.", "tag": "the core idea", "c": "money"},
     {"emoji": "🔗", "title": "Correlation ≠ cause", "body": "Two things moving together doesn't mean one drives the other.", "c": "data"},
     {"emoji": "📉", "title": "Distributions & fat tails", "body": "Markets have rare, violent moves that averages hide.", "c": "risk"},
     {"emoji": "🧪", "title": "In-sample vs out-of-sample", "body": "Only results on unseen data are worth trusting.", "c": "ai"}]},
  "Pillar two. Statistics. And you need far less than you fear. [pause] The single most "
  "important idea is expectancy. Your win rate times your average win, minus your loss "
  "rate times your average loss. If that number is positive, you have something. If it "
  "is negative, no amount of A I will save you. [pause] Learn that correlation is not "
  "causation. Two things moving together does not mean one causes the other. [pause] "
  "Know that markets have fat tails. Rare, violent moves that simple averages hide. "
  "[pause] And burn this in. In sample results, on data you trained on, mean nothing. "
  "Only out of sample results, on data the model has never seen, are worth anything."),

 ("s34_python", "ait_code",
  {"kicker": "PILLAR THREE · PYTHON", "title": "You need less code than you think", "file": "first_look.py", "color": "ai",
   "lines": [
     "# the entire beginner toolkit is about 5 lines",
     "import yfinance as yf",
     "import pandas as pd",
     "",
     "# download two years of daily prices for one stock",
     "df = yf.download('RELIANCE.NS', period='2y')",
     "",
     "# a 'feature': the 20-day average price",
     "df['sma20'] = df['Close'].rolling(20).mean()",
     "print(df.tail())   # look at your data — always"],
   "side": {"title": "What to actually learn", "points": ["Variables, loops, functions", "The pandas DataFrame — your data table", "How to read a library's docs", "That's genuinely enough to begin"]},
   "caption": "If you can read these lines, you already know enough Python to start."},
  "Pillar three. Python. And look how little it takes. [pause] These few lines download "
  "two years of price data for a stock, and then compute a twenty day average. That "
  "average is your first feature. [pause] That is the shape of almost everything you "
  "will do. Load data into a table, add some columns, look at it. [pause] So what "
  "should you actually learn? Variables, loops, and functions. The pandas data frame, "
  "which is just a smart spreadsheet in code. And how to read a library's "
  "documentation. [pause] That is genuinely enough to begin. You do not need to be a "
  "software engineer. You need to be comfortable gluing a few tools together."),

 ("s35_capital", "ait_stat",
  {"kicker": "PILLAR FOUR · THE MONEY", "title": "Set expectations before you set up an account", "color": "risk",
   "stats": [
     {"value": 0, "prefix": "₹", "label": "the money you should risk that you can't lose", "src": "the only safe amount at first", "c": "risk"},
     {"value": 6, "prefix": "", "suffix": "+ mo", "label": "learning before real money is normal", "src": "paper trading is free", "c": "edge"},
     {"value": 2, "prefix": "1–", "suffix": "%", "label": "of capital risked per trade, at most", "src": "the survivor's rule", "c": "money"}],
   "note": "The goal at the start is not profit. It is to not blow up while you learn."},
  "Pillar four. The money and the mindset. This is where dreams meet arithmetic. "
  "[pause] Rule one. The amount you should risk that you cannot afford to lose is zero "
  "rupees. If losing it would hurt your life, it does not belong in a trading bot. "
  "[pause] Rule two. Expect to spend six months or more learning before real money is "
  "even in the picture. And that learning is free, because paper trading is free. "
  "[pause] Rule three, the survivor's rule. Never risk more than one or two percent of "
  "your capital on a single trade. [pause] At the start, your goal is not to make "
  "money. It is to still be standing, and still learning, a year from now."),

 ("s35c_time", "ait_callout",
  {"kicker": "THE HONEST TIME COST", "color": "risk",
   "text": "Expect months of unpaid learning before your first sensible live trade.",
   "sub": "This is a skill you earn slowly — not a switch you flip."},
  "Let's be honest about time, because the ads never are. [pause] This is not a weekend "
  "project. Expect months of unpaid learning before your first sensible live trade. "
  "[pause] A few hours a week, for half a year, just to build the foundation. Then more, "
  "to build and test a real strategy. [pause] If that sounds like a lot, compare it to "
  "any other skill worth money. Nobody becomes a surgeon, or a pianist, or an engineer, "
  "in a weekend. [pause] Trading with A I is a real skill, and like every real skill, "
  "you earn it slowly. Anyone telling you otherwise is selling you something. [pause] "
  "The people who make it are simply the ones who kept going after the excitement wore "
  "off, and the boring work began."),

 ("s36_paper", "ait_callout",
  {"kicker": "THE ONE NON-NEGOTIABLE", "color": "money",
   "text": "Paper trade first. Every strategy. No exceptions.",
   "sub": "Fake money, real prices, real feelings — for weeks, before a rupee is at risk."},
  "If you remember one instruction from this entire course, make it this one. [pause] "
  "Paper trade first. Every strategy, without exception. [pause] Paper trading means "
  "running your bot on live, real prices, but with fake money. Every serious platform "
  "offers it for free. [pause] It does two priceless things. It proves your code "
  "actually works in live conditions. And it lets you feel the emotions, the fear and "
  "the doubt, when the fake money swings, before any real money is on the line. [pause] "
  "Run it for weeks. If it survives paper trading, then, and only then, do you consider "
  "going live with the smallest amount you can."),

 ("s33b_risk_rules", "ait_list",
  {"kicker": "PILLAR FOUR, DEEPER", "title": "The risk commandments", "tone": "ok", "color": "risk",
   "items": [
     {"h": "Risk ≤ 1–2% of capital per trade", "sub": "So no single trade can seriously hurt you. This is the master rule."},
     {"h": "Every position has a stop-loss, set in advance", "sub": "Decide where you're wrong before you enter, not after."},
     {"h": "Cap your total loss for a single day", "sub": "If you hit it, the bot stops. Live to trade tomorrow."},
     {"h": "Don't put all your risk in one bet", "sub": "Correlated positions are secretly one big position."},
     {"h": "Size down when volatility spikes", "sub": "Wild markets deserve smaller bets, not braver ones."}],
   "caption": "Returns are what you hope for. Risk is what you actually control."},
  "Risk is the pillar that decides everything, so let's go deeper. Five commandments. "
  "[pause] One. Risk no more than one or two percent of your capital on any single "
  "trade. This is the master rule. It means no one trade can ever seriously hurt you. "
  "[pause] Two. Every position gets a stop loss, decided before you enter. Decide where "
  "you are wrong in advance, not in the heat of a loss. [pause] Three. Cap your total "
  "loss for a single day. If the bot hits that limit, it stops. You live to trade "
  "tomorrow. [pause] Four. Do not pile all your risk into one bet. Five positions that "
  "all move together are secretly just one big position. [pause] Five. When volatility "
  "spikes, size down, not up. [pause] Returns are what you hope for. Risk is what you "
  "actually control. Control it obsessively."),

 ("s34b_toolstack", "ait_cards",
  {"kicker": "SET UP YOUR BENCH", "title": "The free tools to install today", "color": "ai",
   "cards": [
     {"emoji": "🐍", "title": "Python + venv", "body": "Install Python, and use a virtual environment for each project.", "tag": "the base", "c": "ai"},
     {"emoji": "📓", "title": "Jupyter / VS Code", "body": "A notebook to explore data, an editor to write real bots.", "tag": "your workbench", "c": "data"},
     {"emoji": "📦", "title": "pandas · yfinance · pandas-ta", "body": "Data table, free prices, and technical indicators.", "tag": "the core three", "c": "money"},
     {"emoji": "🧪", "title": "backtesting.py", "body": "A clean, beginner-friendly engine to test strategies.", "tag": "validate", "c": "edge"}]},
  "Let's set up your workbench. The good news, it is entirely free. [pause] First, "
  "install Python, and get in the habit of using a virtual environment for each "
  "project, so their libraries do not clash. [pause] Second, a notebook, like Jupyter, "
  "to explore data interactively. And a proper editor, like V S Code, to write your "
  "real bots. [pause] Third, the core libraries. Pandas for your data table. Yfinance "
  "for free prices. And pandas T A for technical indicators. [pause] Fourth, a "
  "backtesting engine. Backtesting dot py is clean and beginner friendly. [pause] That "
  "is the entire professional starter kit, and it costs nothing but an afternoon to set "
  "up. You will spend the next months living inside these tools."),

 ("s36b_mindset", "ait_callout",
  {"kicker": "THE RIGHT MINDSET", "color": "edge",
   "text": "You're not gambling. You're running a small, data-driven business.",
   "sub": "Boring consistency beats brilliant, occasional bets — every year."},
  "Let's fix the mindset, because it decides whether you last. [pause] You are not "
  "gambling. You are running a small, data driven business. [pause] A business measures "
  "everything, controls its costs, cuts its losers quickly, and lets its winners run. "
  "It does not bet the company on a hunch. [pause] The trader who wins is not the one "
  "with the most exciting week. It is the one with the most boring decade. [pause] "
  "Consistency, discipline, and process beat brilliant, occasional bets. Every single "
  "year. [pause] So drop the fantasy of the lone genius who cracks the market. Pick up "
  "the identity of a calm operator, running a small machine, carefully, for a very long "
  "time."),

 ("s37_path", "ait_list",
  {"kicker": "THE ORDER TO LEARN", "title": "A sane path from zero to your first bot", "tone": "neutral", "color": "edge",
   "items": [
     {"h": "Learn market basics on Zerodha Varsity", "sub": "Free, India-specific, and genuinely excellent."},
     {"h": "Do a short beginner Python course", "sub": "Focus on pandas and reading data — skip the rest for now."},
     {"h": "Build one rule-based strategy by hand", "sub": "No AI yet. Just prove you can go idea to code to backtest."},
     {"h": "Paper trade it for a month, and journal", "sub": "Write down what happened and what you felt. Every day."},
     {"h": "Only then add machine learning", "sub": "AI is step five, not step one. Walk before you run."}],
   "caption": "Most people fail by starting at step five. Start at step one."},
  "So what is the sane order to learn all this? [pause] Step one. Market basics, on "
  "Zerodha Varsity. It is free and India specific. [pause] Step two. A short beginner "
  "Python course. Focus on pandas and reading data. Ignore the rest for now. [pause] "
  "Step three. Build one simple rule based strategy by hand. No A I yet. Just prove to "
  "yourself you can go from an idea, to code, to a backtest. [pause] Step four. Paper "
  "trade it for a month, and keep a journal of what happened and how you felt. [pause] "
  "And step five. Only now do you add machine learning. [pause] Most people fail "
  "because they start at step five. You are going to start at step one. Now let's find "
  "you a place to actually do this."),
]

if __name__ == "__main__":
    core.build("ch3", SEGMENTS, target_min=12)
