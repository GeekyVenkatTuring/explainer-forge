#!/usr/bin/env python3
"""Chapter 4 — Part 4: Where you can actually do it (platforms + SEBI rules)."""
import aitcore as core

SEGMENTS = [
 ("s40_divider", "ait_divider",
  {"n": 4, "title": "Where To Do It", "sub": "Trusted platforms and the rules", "color": "money", "parts": 6},
  "Part four. Where you can actually do this, safely and legally. [pause] We will go "
  "tier by tier, from no code to full code. And then, the rules that changed in India."),

 ("s41_tiers", "ait_tiers",
  {"kicker": "THE THREE TIERS", "title": "Three levels of platform, by how much you code",
   "tiers": [
     {"level": "T1", "effort": "no code", "name": "Strategy builders", "desc": "Point and click to build, backtest, and deploy — zero programming.", "tools": ["Streak", "Tradetron", "AlgoTest"], "c": "data"},
     {"level": "T2", "effort": "some code", "name": "Broker APIs", "desc": "You write the logic; the broker gives you data and execution.", "tools": ["Kite Connect", "SmartAPI", "Dhan", "Fyers"], "c": "ai"},
     {"level": "T3", "effort": "full code", "name": "Cloud quant labs", "desc": "Data, backtesting, and paper trading, all in one environment.", "tools": ["QuantConnect", "Alpaca", "IBKR"], "c": "money"}],
   "caption": "Start at Tier 1 to learn the loop. Graduate to Tier 3 to control everything."},
  "Think of platforms in three tiers, sorted by how much code you write. [pause] Tier "
  "one, no code. Strategy builders where you point and click to build, test, and deploy. "
  "In India, that is Streak, Tradetron, and AlgoTest. [pause] Tier two, some code. "
  "Broker A P Is. You write the logic, and the broker hands you live data and "
  "execution. Think Kite Connect, Angel's SmartAPI, Dhan, and Fyers. [pause] Tier "
  "three, full code. Cloud quant labs that bundle data, backtesting, and paper trading "
  "together, like QuantConnect and Alpaca. [pause] My advice. Start at tier one to "
  "learn the loop. Graduate to tier three when you want to control everything."),

 ("s42_nocode", "ait_cards",
  {"kicker": "TIER ONE · NO-CODE", "title": "The click-and-build platforms", "color": "data",
   "cards": [
     {"emoji": "🟢", "title": "Streak", "body": "Zerodha's own no-code tool. The gentlest place to start for beginners.", "tag": "beginner-friendly", "c": "money"},
     {"emoji": "🔵", "title": "Tradetron", "body": "A marketplace where you can build, or subscribe to others' strategies.", "tag": "multi-broker", "c": "data"},
     {"emoji": "🟠", "title": "AlgoTest", "body": "Strong for options backtesting. Free tier, then paid plans.", "tag": "options focus", "c": "edge"}]},
  "Let's look inside tier one. [pause] Streak is Zerodha's own no code tool. It is the "
  "gentlest possible on ramp. You pick conditions, backtest, and deploy, all by "
  "clicking. If you are brand new, start here. [pause] Tradetron is a marketplace. You "
  "can build your own strategy, or subscribe to someone else's, and it works across "
  "many brokers. [pause] And AlgoTest is especially strong for options strategies and "
  "serious backtesting. It has a free tier, then paid plans. [pause] One honest "
  "warning. A marketplace strategy that looks amazing is often overfit to the past. "
  "Everything you learned in part two still applies here. A pretty backtest is not a "
  "promise."),

 ("s43_brokerapi", "ait_cards",
  {"kicker": "TIER TWO · BROKER APIs", "title": "The rails your own code plugs into", "color": "ai",
   "cards": [
     {"emoji": "⚙️", "title": "Kite Connect", "body": "Zerodha's API. Rock-solid and popular; around ₹2,000 a month.", "tag": "the standard", "c": "money"},
     {"emoji": "🆓", "title": "Angel SmartAPI", "body": "A full-featured API that is free to use. Great for learning.", "tag": "free", "c": "data"},
     {"emoji": "🚀", "title": "Dhan & Fyers", "body": "Modern, developer-first APIs; free order placement, paid data add-ons.", "tag": "developer-first", "c": "edge"},
     {"emoji": "🔎", "title": "How to choose", "body": "Match the API to the broker you already trust with your money.", "tag": "key rule", "c": "ai"}]},
  "Tier two. Broker A P Is. This is where your own Python code plugs into a real "
  "broker. [pause] Kite Connect, from Zerodha, is the standard. Rock solid, widely "
  "used, and it costs around two thousand rupees a month. [pause] Angel One's SmartAPI "
  "is full featured and free, which makes it excellent for learning. [pause] Dhan and "
  "Fyers are modern, developer first APIs. Order placement is typically free, with paid "
  "add ons for richer data. [pause] Prices and features change, so always check the "
  "broker's own page. And the key rule. Choose the A P I that belongs to the broker you "
  "already trust with your money. The A P I is just a door into your existing account."),

 ("s44_cloud", "ait_cards",
  {"kicker": "TIER THREE · CLOUD QUANT", "title": "Full-code labs, mostly global", "color": "money",
   "cards": [
     {"emoji": "🧪", "title": "QuantConnect", "body": "Free historical data, a cloud backtester, and paper trading in one place.", "tag": "best free lab", "c": "money"},
     {"emoji": "🦙", "title": "Alpaca", "body": "Clean US-market API with free, unlimited paper trading. A joy to learn on.", "tag": "US markets", "c": "data"},
     {"emoji": "🌐", "title": "Interactive Brokers", "body": "Global access and deep instruments; heavier to set up.", "tag": "advanced", "c": "edge"}]},
  "Tier three. Cloud quant labs. These are the professional sandboxes, and most are "
  "global. [pause] QuantConnect is the best free lab I know of. Free historical data, a "
  "powerful cloud backtester, and paper trading, all in one place. [pause] Alpaca is a "
  "clean, modern A P I for U S markets, with free unlimited paper trading. It is a joy "
  "to learn on, even if you never trade a single U S share. [pause] And Interactive "
  "Brokers gives you global access to almost everything, though it is heavier to set "
  "up. [pause] A great free path is to learn the craft on QuantConnect and Alpaca, "
  "then apply the exact same skills to your Indian broker's A P I."),

 ("s45_sebi", "ait_list",
  {"kicker": "THE RULES · SEBI", "title": "India's new algo-trading rules, in plain words", "tone": "neutral", "color": "risk",
   "items": [
     {"h": "Under 10 orders per second? You're fine", "sub": "Normal personal automation stays light-touch — no heavy registration.", "c": "money"},
     {"h": "Your API key must use a whitelisted static IP", "sub": "A security step to stop anyone else using your access.", "c": "data"},
     {"h": "Faster or shared strategies get an “Algo ID”", "sub": "Every real algo order becomes traceable to its source.", "c": "edge"},
     {"h": "White-box is open; black-box needs a licence", "sub": "Selling a hidden-logic strategy requires SEBI Research Analyst status.", "c": "risk"}],
   "caption": "The broker is now the responsible principal for every algo on its platform."},
  "Now the rules, because this genuinely changed in India. SEBI, the market regulator, "
  "built a new framework for algo trading. [pause] Here is what actually matters to "
  "you. [pause] If you trade for yourself and stay under about ten orders per second, "
  "you are in the light touch zone. No heavy registration. [pause] Your A P I key must "
  "be tied to a whitelisted static I P address. That is just a security step so nobody "
  "else can use your access. [pause] If you cross that speed, or you share a strategy "
  "with others, your orders get tagged with an Algo I D, so they are traceable. [pause] "
  "And a strategy whose logic is open, a white box, is fine. But selling a hidden, "
  "black box strategy requires a SEBI research analyst licence. Your broker is now "
  "responsible for every algo running on its platform."),

 ("s46_sebidates", "ait_list",
  {"kicker": "THE TIMELINE", "title": "The dates worth knowing", "tone": "neutral", "color": "edge",
   "items": [
     {"h": "Late 2025 — brokers register with exchanges", "sub": "The framework is switched on across the industry."},
     {"h": "Early 2026 — non-compliant brokers restricted", "sub": "Brokers who aren't ready get cut off from new API clients."},
     {"h": "April 2026 — full framework mandatory", "sub": "Algo-ID tagging and the complete rulebook apply to everyone."}],
   "caption": "Rules evolve — always confirm the current position on the SEBI and exchange sites."},
  "There is also a timeline, and it is worth knowing. [pause] Through late twenty "
  "twenty five, brokers register with the exchanges and switch the framework on. "
  "[pause] In early twenty twenty six, brokers who are not compliant get restricted "
  "from taking new A P I clients. [pause] And by April twenty twenty six, the full "
  "framework, including Algo I D tagging, is mandatory for everyone. [pause] Now, rules "
  "like these get refined over time. So please do not take my dates as frozen. Before "
  "you go live, spend ten minutes confirming the current position on the SEBI and "
  "exchange websites. The point is simple. Trade through a proper, compliant broker, "
  "and you have nothing to fear here."),

 ("s44b_data", "ait_cards",
  {"kicker": "DON'T FORGET DATA", "title": "Where your bot's data comes from", "color": "data",
   "cards": [
     {"emoji": "🆓", "title": "Free & fine to learn", "body": "yfinance and NSE's own site — great for building and backtesting.", "tag": "start here", "c": "money"},
     {"emoji": "🔌", "title": "Broker live feed", "body": "Real-time ticks via your broker's API, often a small monthly add-on.", "tag": "for live", "c": "data"},
     {"emoji": "🏛️", "title": "Paid vendors", "body": "Clean, deep history and fundamentals — for when you're serious.", "tag": "later", "c": "edge"},
     {"emoji": "⚠️", "title": "Quality > quantity", "body": "Bad data quietly produces confident, wrong backtests.", "tag": "the rule", "c": "risk"}]},
  "One thing beginners forget when picking a platform. The data. Your bot is only as "
  "good as what it reads. [pause] For learning and backtesting, free sources like "
  "yfinance and the N S E's own website are perfectly fine. Start there. [pause] For "
  "live trading, you will want your broker's real time feed. On many brokers that is a "
  "small monthly add on, often a few hundred rupees. [pause] And when you get serious, "
  "there are paid vendors with clean, deep history and fundamentals. That is a later "
  "problem. [pause] But hold this rule above all. Quality beats quantity. Bad or messy "
  "data does not announce itself. It quietly produces a confident backtest that is "
  "completely wrong. Garbage in, garbage out, once again."),

 ("s46b_setup", "ait_list",
  {"kicker": "A REAL SETUP, STEP BY STEP", "title": "From zero to a live-ready account", "tone": "neutral", "color": "money",
   "items": [
     {"h": "1 — Open a demat account with a compliant broker", "sub": "Zerodha, Angel, Dhan, Upstox, Fyers — all SEBI-registered."},
     {"h": "2 — Subscribe to their API and get your keys", "sub": "Bind the key to a static IP, as SEBI now requires."},
     {"h": "3 — Connect in paper / sandbox mode first", "sub": "Every serious API has a test mode. Live there for weeks."},
     {"h": "4 — Flip to live only when the ladder says so", "sub": "Backtest, walk-forward, paper — then tiny real size."}],
   "caption": "The credentials change from paper to live. Your discipline should not."},
  "So what does a real setup actually look like? Four steps. [pause] One. Open a demat "
  "and trading account with a compliant broker. Zerodha, Angel, Dhan, Upstox, Fyers, "
  "they are all SEBI registered. [pause] Two. Subscribe to their A P I and generate "
  "your keys. Bind the key to a static I P address, exactly as SEBI now requires. "
  "[pause] Three. Connect in paper, or sandbox, mode first. Every serious A P I has a "
  "test mode that mimics the real one. Live there for weeks. [pause] Four. Flip to live "
  "only when the ladder from part five says you are ready. Backtest, then walk forward, "
  "then paper, then a tiny real size. [pause] The credentials are the only thing that "
  "changes from paper to live. Your discipline should not."),

 ("s46c_copytrade", "ait_callout",
  {"kicker": "A WORD ON COPY TRADING", "color": "risk",
   "text": "Copying a trader means inheriting their risk — without their reasons.",
   "sub": "You feel their drawdowns in full, and you can't see when they change their mind."},
  "Quick word on copy trading, because it tempts everyone who does not want to code. "
  "[pause] The pitch is simple. Link your account to a skilled trader, and mirror their "
  "every move automatically. [pause] The problem is just as simple. When you copy a "
  "trader, you inherit their risk, but not their reasoning. [pause] You feel their "
  "drawdowns in full, on your own money. And you cannot see when they change their "
  "mind, or when their edge quietly stops working. [pause] You are also trusting that "
  "their track record is real, and not survivorship or a lucky streak. [pause] Copy "
  "trading is not evil. But it is not passive, and it is not safe. If you would not "
  "take a trade yourself, do not let a stranger take it with your money."),

 ("s46d_cost", "ait_bars",
  {"kicker": "WHAT IT COSTS TO RUN", "title": "Rough monthly cost, by tier", "color": "money", "unit": "", "max": 3000,
   "bars": [
     {"label": "no-code free tier", "v": 0, "c": "money"},
     {"label": "free broker API", "v": 0, "c": "money"},
     {"label": "no-code paid", "v": 1500, "c": "edge"},
     {"label": "Kite Connect", "v": 2000, "c": "ai"},
     {"label": "+ live data add-on", "v": 2500, "c": "risk"}],
   "note": "Figures in ₹ per month, approximate — always confirm on the provider's own page."},
  "Let's talk money. What does it actually cost to run this? [pause] The honest answer "
  "for a learner is often zero. No code platforms have free tiers. And several broker A "
  "P Is, like Angel's SmartAPI, are completely free. [pause] If you go paid, a no code "
  "platform runs around fifteen hundred rupees a month. Zerodha's Kite Connect is about "
  "two thousand. Add a live data feed, and you are near twenty five hundred. [pause] "
  "These are rough figures in rupees per month, so always check the provider's own page. "
  "[pause] But here is the point. Cost is not your real problem. You can learn "
  "everything for free. Your scarce resource is not money. It is the discipline and the "
  "time to do this properly."),

 ("s47_choose", "ait_list",
  {"kicker": "HOW TO CHOOSE", "title": "Pick your platform in four questions", "tone": "ok", "color": "money",
   "items": [
     {"h": "Can I paper trade for free? If not, skip it", "sub": "This is non-negotiable. No sandbox, no deal."},
     {"h": "Is it my existing, trusted, compliant broker?", "sub": "Keep your money where it already lives, under SEBI's rules."},
     {"h": "Does the cost fit how often I'll trade?", "sub": "A monthly API fee only makes sense past a certain activity."},
     {"h": "Can I grow here — from clicks to full code?", "sub": "Choose a place you won't outgrow in three months."}],
   "caption": "The best platform is the boring, compliant one you'll actually stick with."},
  "So how do you choose? Ask four questions. [pause] One. Can I paper trade here, for "
  "free? If the answer is no, skip it entirely. This is not negotiable. [pause] Two. Is "
  "this my existing, trusted, SEBI compliant broker? Keep your money where it already "
  "lives. [pause] Three. Does the cost match how often I will actually trade? A two "
  "thousand rupee monthly A P I fee only makes sense above a certain activity level. "
  "[pause] Four. Can I grow here, from clicking strategies to writing full code, "
  "without having to move? [pause] The honest answer is usually boring. The best "
  "platform is the compliant, reliable one you will actually stick with. Not the "
  "flashiest one on a Telegram ad."),

 ("s48_micro", "ait_callout",
  {"kicker": "PART FOUR IN ONE LINE", "color": "money",
   "text": "Start no-code, keep your money in your own broker, follow the rules.",
   "sub": "Now the fun part — building your own from scratch."},
  "Part four in one line. [pause] Start no code to learn. Keep your money inside your "
  "own compliant broker. And follow the rules, which mostly means, just use a proper "
  "broker. [pause] You now know what A I trading is, why most bots fail, what to learn, "
  "and where to do it. [pause] Which means you are finally ready for the part everyone "
  "came for. Building your very own trading bot, from scratch, in real code. Let's go."),
]

if __name__ == "__main__":
    core.build("ch4", SEGMENTS, target_min=14)
