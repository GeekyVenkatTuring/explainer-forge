#!/usr/bin/env python3
"""Chapter 1 — Part 1: What AI trading actually is."""
import aitcore as core

SEGMENTS = [
 ("s10_divider", "ait_divider",
  {"n": 1, "title": "What It Really Is", "sub": "The mechanics behind the buzzword", "color": "data", "parts": 6},
  "Part one. What A I trading actually is. [pause] Before you can judge it, or build "
  "it, you need the real mental model. Let's start there."),

 ("s11_pipeline", "ait_pipeline",
  {"kicker": "THE SIGNAL STACK", "title": "Every trading system is one pipeline",
   "stages": [
     {"label": "Data", "sub": "prices, news, fundamentals", "c": "data"},
     {"label": "Features", "sub": "turn data into numbers", "c": "data"},
     {"label": "Model", "sub": "the decision maker", "c": "ai"},
     {"label": "Signal", "sub": "buy, sell, or hold", "c": "edge"},
     {"label": "Risk", "sub": "how much to bet", "c": "risk"},
     {"label": "Order", "sub": "sent to the broker", "c": "money"}],
   "caption": "Remember these six boxes. Every bot in this course is a version of them."},
  "Here is the single most useful idea in this whole course. [pause] Every trading "
  "system, from a simple script to a hedge fund's engine, is the same pipeline. [pause] "
  "It starts with data. Prices, news, company numbers. Then features. We turn that raw "
  "data into clean numbers a computer can use. [pause] Then the model. This is the "
  "decision maker. It looks at the features and produces a signal. Buy, sell, or hold. "
  "[pause] Then risk. How much do we actually bet? And finally, the order goes to the "
  "broker. [pause] Six boxes. Data, features, model, signal, risk, order. Keep them in "
  "your head. Everything else is detail."),

 ("s12_notmagic", "ait_compare",
  {"kicker": "CLEAR THE MYTH", "title": "So where does the “AI” fit in?",
   "left": {"emoji": "🔮", "title": "What people imagine", "c": "risk", "mark": "✕",
     "items": ["A crystal ball that predicts prices", "It “knows” the market will go up", "Set it and get rich while you sleep"]},
   "right": {"emoji": "🧩", "title": "What it really is", "c": "money", "mark": "✓",
     "items": ["A pattern finder, only in the model box", "It estimates odds, and is often wrong", "A tool that still needs your judgement"]},
   "caption": "AI replaces the model box. The other five boxes are still your job."},
  "So where does the A I actually fit? [pause] Most people imagine a crystal ball. A "
  "machine that knows the price will go up, so you get rich while you sleep. [pause] "
  "That is not what it is. A I lives inside just one box. The model. [pause] And the "
  "model is not a fortune teller. It is a pattern finder. It looks at the past and "
  "estimates the odds of what might happen next. [pause] It is often wrong. The other "
  "five boxes, the data, the risk, the execution, are still completely your job. A I "
  "does not remove the hard parts. It just changes how the decision gets made."),

 ("s13_spectrum", "ait_spectrum",
  {"kicker": "THE SPECTRUM", "title": "From simple rules to full AI agents",
   "axis": ["simpler, transparent", "more autonomous, opaque"],
   "levels": [
     {"label": "Rules", "sub": "if this, then that", "tag": "1", "c": "data"},
     {"label": "Classic ML", "sub": "trees, regression", "tag": "2", "c": "money"},
     {"label": "Deep RL", "sub": "learns by trial", "tag": "3", "c": "edge"},
     {"label": "LLM agents", "sub": "reason and act", "tag": "4", "c": "ai"}],
   "caption": "More autonomy is not more profit — it is more ways to be wrong."},
  "Now, the word A I covers a whole spectrum. [pause] At the simple end are rules. If "
  "this, then that. Buy when a stock gets cheap by some measure. There is no learning "
  "here, but it is honest and easy to check. [pause] Next, classic machine learning. "
  "Models like decision trees that learn patterns from data. [pause] Then deep "
  "reinforcement learning. An agent that learns by trial and error, like a game "
  "player. [pause] And at the far end, language model agents that can read, reason, "
  "and act. [pause] Here is the trap. As you move right, the system gets more "
  "autonomous, but also harder to understand. And more autonomy is not more profit. "
  "It is just more ways to be wrong."),

 ("s14_fiveways", "ait_cards",
  {"kicker": "HOW PEOPLE USE IT", "title": "Five real jobs AI does in markets", "color": "ai",
   "cards": [
     {"emoji": "⚡", "title": "Execution", "body": "Slice a huge order so it doesn't move the price.", "tag": "biggest real use", "c": "money"},
     {"emoji": "📈", "title": "Prediction", "body": "Forecast the next move from historical patterns.", "tag": "quant", "c": "data"},
     {"emoji": "📰", "title": "Reading text", "body": "Scan news and filings for tone and surprise.", "tag": "NLP", "c": "edge"},
     {"emoji": "🤖", "title": "Learning agents", "body": "Reinforcement learners that discover a strategy.", "tag": "research", "c": "ai"},
     {"emoji": "🧭", "title": "Copilots", "body": "Assistants that help you research and code faster.", "tag": "you, today", "c": "data"}]},
  "So what jobs does A I actually do in markets? Five main ones. [pause] First, and "
  "biggest, execution. When a fund buys millions of shares, an algorithm slices it "
  "into tiny pieces so the price does not jump. This is where A I genuinely shines. "
  "[pause] Second, prediction. Models that forecast the next move. [pause] Third, "
  "reading text. Scanning thousands of news stories and filings for tone and surprises "
  "faster than any human. [pause] Fourth, learning agents that discover strategies on "
  "their own. [pause] And fifth, copilots. Assistants that help you research and write "
  "code. That last one is the most useful thing for you, today."),

 ("s15_institutions", "ait_stat",
  {"kicker": "HOW THE BIG PLAYERS USE IT", "title": "AI is already the market's plumbing", "color": "money",
   "stats": [
     {"value": 75, "suffix": "%", "label": "of institutional desks use AI or ML", "src": "industry survey, 2025", "c": "money"},
     {"value": 1978, "label": "a top broker's roots in automated trading", "src": "decades of head start", "c": "data", "comma": False},
     {"value": 100, "prefix": "up to ", "suffix": "x", "label": "faster order speed than a home setup", "src": "co-located servers", "c": "risk"}],
   "note": "Example: JP Morgan's execution engine uses reinforcement learning to hide big orders."},
  "Let's be clear about how the big players use this. [pause] Around seventy five "
  "percent of large trading desks now use A I or machine learning somewhere in their "
  "workflow. [pause] For example, J P Morgan runs an execution engine that uses "
  "reinforcement learning to hide huge orders from the market. [pause] These firms have "
  "spent decades and hundreds of millions building this. Their servers sit right next "
  "to the exchange, so their orders arrive up to a hundred times faster than yours. "
  "[pause] For them, A I is not a gimmick. It is the plumbing. That is the world you "
  "are stepping into."),

 ("s16_speed", "ait_compare",
  {"kicker": "THE SPEED GAME", "title": "Two very different games under one word",
   "left": {"emoji": "🏎️", "title": "High-frequency", "c": "ai", "mark": "▸",
     "items": ["Wins by being microseconds faster", "Needs co-located servers and huge capital", "You cannot compete here — don't try"]},
   "right": {"emoji": "🧠", "title": "Slower, smarter", "c": "money", "mark": "▸",
     "items": ["Wins by a better idea, over days or weeks", "Runs fine on a laptop and cheap data", "This is the only game open to you"]},
   "caption": "Forget speed. Your only hope is a smarter, slower idea."},
  "Now, one word, A I trading, actually hides two very different games. [pause] The "
  "first is high frequency trading. Here you win by being microseconds faster than the "
  "next machine. It needs servers next to the exchange and enormous capital. [pause] "
  "You cannot compete in this game. Do not even try. [pause] The second game is slower "
  "and smarter. You win by having a better idea that plays out over days or weeks. This "
  "runs fine on a normal laptop with cheap data. [pause] This second game is the only "
  "one open to you. So for the rest of this course, forget about speed. Your only edge "
  "will be a smarter, slower idea."),

 ("s17_retail", "ait_orbit",
  {"kicker": "HOW PEOPLE LIKE YOU USE IT", "title": "The retail AI-trading toolkit today",
   "hub": {"emoji": "🙋", "label": "Retail trader", "c": "data"},
   "items": [
     {"emoji": "🖱️", "label": "No-code builders", "sub": "click a strategy", "c": "data"},
     {"emoji": "🔔", "label": "Signal services", "sub": "someone else's calls", "c": "edge"},
     {"emoji": "🤝", "label": "Copy trading", "sub": "mirror a trader", "c": "money"},
     {"emoji": "💬", "label": "LLM copilots", "sub": "research helpers", "c": "ai"},
     {"emoji": "🐍", "label": "Custom bots", "sub": "your own code", "c": "risk"}],
   "caption": "The gap between a click-built bot and a real edge is enormous — mind it."},
  "So how do people like you actually use A I in markets right now? [pause] Five ways. "
  "There are no code builders, where you click together a strategy with no programming. "
  "[pause] There are signal services that sell you someone else's buy and sell calls. "
  "And copy trading, where your account mirrors another trader automatically. [pause] "
  "There are language model copilots that help you research and reason. And finally, "
  "custom bots that you write yourself. [pause] Here is the honest warning. The gap "
  "between a bot you clicked together in five minutes and one that actually makes "
  "money is enormous. Easy to start is not the same as easy to profit."),

 ("s14b_data", "ait_cards",
  {"kicker": "WHAT FEEDS THE MODEL", "title": "The four kinds of data people trade on", "color": "data",
   "cards": [
     {"emoji": "💹", "title": "Price & volume", "body": "The classic. Open, high, low, close, and how much traded.", "tag": "everyone has this", "c": "data"},
     {"emoji": "📑", "title": "Fundamentals", "body": "Earnings, debt, growth — the health of the business itself.", "tag": "slower signals", "c": "money"},
     {"emoji": "📰", "title": "News & text", "body": "Headlines, filings, transcripts — where language models shine.", "tag": "NLP territory", "c": "edge"},
     {"emoji": "🛰️", "title": "Alternative data", "body": "Satellite images, app downloads, card spending — the edge hunt.", "tag": "expensive & niche", "c": "ai"}]},
  "Before we move on, let's answer a basic question. What data do these systems "
  "actually eat? Four kinds. [pause] First, price and volume. The classic. Open, high, "
  "low, close, and how much traded. Everyone has this, so on its own it rarely gives an "
  "edge. [pause] Second, fundamentals. Earnings, debt, growth. The health of the "
  "business. These move slowly. [pause] Third, news and text. Headlines, filings, "
  "earnings call transcripts. This is where language models genuinely shine. [pause] "
  "And fourth, alternative data. Satellite photos of parking lots, app download counts, "
  "card spending. This is where funds hunt for a real edge, and it is expensive. [pause]"
  " The pattern is simple. The more unusual your data, the better your chance. And the "
  "harder it is to get."),

 ("s15c_example", "ait_cards",
  {"kicker": "A CONCRETE EXAMPLE", "title": "A simple momentum bot, in five sentences", "color": "edge",
   "cards": [
     {"emoji": "1️⃣", "title": "Watch", "body": "Every day, scan the 50 biggest stocks.", "c": "data"},
     {"emoji": "2️⃣", "title": "Rank", "body": "Sort them by their return over the last 3 months.", "c": "data"},
     {"emoji": "3️⃣", "title": "Buy", "body": "Hold the top few. Winners tend to keep winning, briefly.", "c": "money"},
     {"emoji": "4️⃣", "title": "Protect", "body": "Set a stop-loss on each; never bet the whole account.", "c": "risk"},
     {"emoji": "5️⃣", "title": "Rotate", "body": "Each month, drop laggards and add new leaders.", "c": "edge"}]},
  "Let's make this concrete with one real, simple strategy. Momentum. [pause] The idea "
  "is that recent winners tend to keep winning, for a little while. [pause] Here is the "
  "whole bot in five sentences. One. Every day, watch the fifty biggest stocks. Two. "
  "Rank them by their return over the last three months. [pause] Three. Buy and hold "
  "the top few. Four. Protect every position with a stop loss, and never bet the whole "
  "account. [pause] Five. Each month, drop the laggards and add the new leaders. "
  "[pause] That is it. No neural network. No magic. A real, tradable strategy that fund "
  "managers have used for decades. Notice how it maps perfectly onto our six boxes. "
  "Data, a ranking feature, a rule, a signal, risk, and orders."),

 ("s16c_crypto", "ait_compare",
  {"kicker": "TWO ARENAS", "title": "AI trading: stocks vs crypto",
   "left": {"emoji": "📈", "title": "Stocks (India)", "c": "money", "mark": "▸",
     "items": ["Regulated by SEBI, with real protections", "Fixed market hours — your bot sleeps", "Deep, liquid, and relatively stable"]},
   "right": {"emoji": "🪙", "title": "Crypto", "c": "risk", "mark": "▸",
     "items": ["Lightly regulated — you're on your own", "Trades 24/7 — great for bots, brutal on you", "Wildly volatile; scams are everywhere"]},
   "caption": "Bots love crypto's 24/7 markets — but that's also where most fraud lives."},
  "You will hear about A I trading in two arenas, and they are very different. [pause] "
  "Stocks, in India, are regulated by SEBI. There are real protections. The market has "
  "fixed hours, so your bot actually sleeps at night. And it is deep and relatively "
  "stable. [pause] Crypto is another world. It is lightly regulated, so you are largely "
  "on your own. It trades twenty four hours a day, seven days a week. [pause] That non "
  "stop nature is exactly why bots swarm to crypto. A machine never needs sleep. [pause]"
  " But hear me clearly. That same arena is where the wildest volatility and the vast "
  "majority of scams live. Everything in this course applies to both. But if you are "
  "learning, start with regulated stocks, where the guardrails exist."),

 ("s17c_efficient", "ait_callout",
  {"kicker": "WHY THIS IS GENUINELY HARD", "color": "risk",
   "text": "You're not fighting the market. You're fighting everyone else trying to beat it.",
   "sub": "Every obvious edge is already traded away by someone smarter and faster."},
  "There is one more idea you must internalise before part two. Why is this so hard? "
  "[pause] Because the market is not a passive puzzle. It is a crowd of millions of "
  "people and machines, all trying to outsmart each other. [pause] You are not fighting "
  "the market. You are fighting everyone else who is also trying to beat it. [pause] "
  "And many of them are smarter, faster, and better funded than you. So any edge that "
  "is obvious has already been found and traded away. [pause] This is close to what "
  "economists call an efficient market. Not perfectly efficient, there are cracks. But "
  "efficient enough that easy money does not survive. [pause] Your job is to find one "
  "of those small cracks, and to do it before the crowd closes it. Keep that image. It "
  "explains everything that follows."),

 ("s18_homogenization", "ait_callout",
  {"kicker": "THE MODERN CATCH", "color": "edge",
   "text": "When everyone uses the same AI, the edge disappears.",
   "sub": "Same models, same data, same trades — arbitraged away in seconds."},
  "And there is a brand new catch in twenty twenty six. [pause] A few years ago, only "
  "hedge funds had powerful A I. Today, millions of people prompt the very same models, "
  "using the same public data. [pause] Think about what that means. If everyone's A I "
  "sees the same signal and shouts buy at the same moment, the opportunity is gone in "
  "seconds. [pause] It gets arbitraged away, usually by someone faster than you. So an "
  "edge that everyone can copy is not an edge at all. Real advantage now comes from a "
  "unique question, unique data, or a niche too small for the giants to bother with. "
  "Hold on to that idea. It comes back again and again."),
]

if __name__ == "__main__":
    core.build("ch1", SEGMENTS, target_min=13)
