#!/usr/bin/env python3
"""Chapter 6 — Part 6: Your realistic plan + the honest verdict."""
import aitcore as core

SEGMENTS = [
 ("s60_divider", "ait_divider",
  {"n": 6, "title": "Your Plan", "sub": "A realistic path, and an honest verdict", "color": "data", "parts": 6},
  "Part six. Your plan. [pause] Let's turn everything into a concrete path, and then I "
  "will give you my genuinely honest verdict on whether you should do this at all."),

 ("s61_plan", "ait_list",
  {"kicker": "THE FIRST 90 DAYS", "title": "A month-by-month starting plan", "tone": "neutral", "color": "edge",
   "items": [
     {"h": "Month 1 — Learn the ground", "sub": "Varsity for markets, a short Python course, and read part two again."},
     {"h": "Month 2 — Build one white-box bot", "sub": "Idea to code to backtest to walk-forward. No AI yet."},
     {"h": "Month 3 — Paper trade and journal", "sub": "Run it live with fake money. Write down every trade and feeling."},
     {"h": "Only after that — go live, tiny", "sub": "Real money so small a total loss wouldn't sting. Then decide."}],
   "caption": "Notice AI isn't in the first ninety days. Skill comes before intelligence."},
  "Here is a realistic first ninety days. [pause] Month one, learn the ground. Zerodha "
  "Varsity for how markets work, a short Python course, and re read part two of this "
  "course until the traps are burned in. [pause] Month two, build one white box bot. "
  "Take it all the way. Idea, to code, to backtest, to walk forward. Still no A I. "
  "[pause] Month three, paper trade it and keep a journal. Every trade, every emotion, "
  "written down. [pause] And only after all of that, if it survived, do you go live "
  "with an amount so small that losing all of it would not sting. [pause] Notice what "
  "is not in these ninety days. A I. Because skill has to come before intelligence."),

 ("s61b_whyquit", "ait_list",
  {"kicker": "WHY MOST PEOPLE QUIT", "title": "The five exits — and how to avoid them", "tone": "bad", "color": "risk",
   "items": [
     {"h": "They expected fast money", "sub": "Fix: expect a multi-year craft, and the disappointment never comes."},
     {"h": "They blew up by skipping risk rules", "sub": "Fix: 1% per trade, always. You can't quit if you're still standing."},
     {"h": "They chased a new strategy every week", "sub": "Fix: master one simple edge before touching a second."},
     {"h": "They couldn't sit through a drawdown", "sub": "Fix: paper trading builds the stomach before real money does."},
     {"h": "They traded alone, in the dark", "sub": "Fix: journal, and learn beside honest people building in the open."}],
   "caption": "Almost nobody quits because the math was too hard. They quit for these five reasons."},
  "Before the verdict, let's look at why most people quit. Because almost nobody quits "
  "because the math was too hard. [pause] They quit for five reasons. One, they expected "
  "fast money, and got bored or disappointed. The fix is to expect a multi year craft "
  "from day one. [pause] Two, they blew up by skipping the risk rules. The fix is one "
  "percent per trade, always. You cannot quit if you are still standing. [pause] Three, "
  "they chased a shiny new strategy every week. The fix is to master one simple edge "
  "first. [pause] Four, they could not sit through a drawdown. The fix is paper trading, "
  "which builds the stomach before real money is at stake. [pause] And five, they "
  "traded alone, in the dark. The fix is to journal, and learn beside honest people. "
  "[pause] Notice, every single exit is avoidable. You now know how to avoid all five."),

 ("s62_good", "ait_stat",
  {"kicker": "REALISTIC EXPECTATIONS", "title": "What success actually looks like", "color": "money",
   "stats": [
     {"value": 90, "suffix": "%", "label": "of your effort is process, not prediction", "src": "the unglamorous truth", "c": "data"},
     {"value": 1, "suffix": "", "label": "one small, durable edge is a real career", "src": "you don't need ten", "c": "money"},
     {"value": 0, "suffix": "", "label": "shortcuts that actually work", "src": "it's a craft, not a jackpot", "c": "risk"}],
   "note": "The realistic win is a modest, repeatable edge you defend for years — not a jackpot."},
  "Let's set honest expectations for what winning even looks like. [pause] First, "
  "ninety percent of your effort will be unglamorous process. Cleaning data, managing "
  "risk, checking your system. Not brilliant predictions. [pause] Second, you do not "
  "need ten edges. One small, durable advantage that you understand and defend is a "
  "genuine career. [pause] And third, the number of get rich quick outcomes on offer "
  "here is zero. [pause] This is a craft, like surgery or carpentry. The realistic win "
  "is a modest, repeatable edge that you protect for years. If that sounds "
  "disappointing, this may not be for you. If it sounds like a worthy challenge, you "
  "are exactly the right kind of person for it."),

 ("s63_verdict", "ait_compare",
  {"kicker": "THE HONEST VERDICT", "title": "Should you actually do this?",
   "left": {"emoji": "✅", "title": "Do it if…", "c": "money", "mark": "✓",
     "items": ["You love the process, not just profit", "You'll treat it as a multi-year craft", "You can risk money you won't miss", "You enjoy coding and data puzzles"]},
   "right": {"emoji": "🛑", "title": "Skip it if…", "c": "risk", "mark": "✕",
     "items": ["You need this money to grow safely", "You want passive, hands-off income", "A guaranteed-returns ad pulled you in", "You won't paper trade patiently first"]},
   "caption": "For most people, low-cost index investing beats a home-made bot. That's okay."},
  "So, the honest verdict. Should you actually do this? [pause] Do it if you love the "
  "process itself, not just the profit. If you will treat it as a multi year craft. If "
  "you can risk money you will not miss. And if you genuinely enjoy code and data "
  "puzzles. [pause] But skip it if you need this money to grow safely. If you want "
  "passive, hands off income. If a guaranteed returns advertisement is what pulled you "
  "in. Or if you will not paper trade patiently first. [pause] And here is the most "
  "honest sentence in this course. For most people, boring, low cost index investing "
  "will beat a home made bot. [pause] And that is completely okay. Knowing that is "
  "wisdom, not weakness."),

 ("s62b_weekly", "ait_list",
  {"kicker": "ONCE YOU'RE RUNNING", "title": "A simple weekly routine", "tone": "neutral", "color": "edge",
   "items": [
     {"h": "Check the logs — did the bot behave?", "sub": "Every trade should match a rule you can point to."},
     {"h": "Compare live results to the backtest", "sub": "Drifting apart is your early warning of edge decay."},
     {"h": "Review your journal, not just your P&L", "sub": "Did you override the bot? Why? Be honest with yourself."},
     {"h": "Research one improvement — test it offline", "sub": "Never edit a live bot on a whim. Change it deliberately."}],
   "caption": "The work is never 'set and forget'. It's a calm, weekly loop of checking and improving."},
  "Trading is not set and forget. Once your bot is live, you settle into a calm weekly "
  "routine. [pause] First, check the logs. Did the bot behave? Every trade should match "
  "a rule you can point to. [pause] Second, compare live results to the backtest. When "
  "they start drifting apart, that is your early warning that the edge is decaying. "
  "[pause] Third, review your journal, not just your profit and loss. Did you override "
  "the bot this week? Why? Be brutally honest. [pause] Fourth, research one improvement, "
  "and test it offline, never on the live bot on a whim. [pause] That is the whole job. "
  "A quiet, disciplined loop of check, compare, reflect, and carefully improve. Do it "
  "every week, for years. That is what mastery actually looks like here."),

 ("s63b_learn", "ait_cards",
  {"kicker": "KEEP GOING", "title": "Where to keep learning", "color": "ai",
   "cards": [
     {"emoji": "📚", "title": "Zerodha Varsity", "body": "Free, deep, India-specific market and F&O education.", "tag": "foundations", "c": "money"},
     {"emoji": "🧪", "title": "QuantConnect docs & bootcamp", "body": "Learn real backtesting on a professional engine, free.", "tag": "hands-on", "c": "data"},
     {"emoji": "📄", "title": "Open-source & papers", "body": "Read FinRL and TradingAgents; skim quant finance papers.", "tag": "frontier", "c": "edge"},
     {"emoji": "🧑‍🤝‍🧑", "title": "Serious communities", "body": "Learn in the open. Avoid any group promising signals.", "tag": "careful", "c": "risk"}]},
  "This course is a map, not the whole journey. Here is where to keep going. [pause] "
  "For foundations, Zerodha Varsity. Free, deep, and India specific. Read it more than "
  "once. [pause] For hands on skill, QuantConnect's documentation and bootcamp. You "
  "learn real backtesting on a professional engine, for free. [pause] For the frontier, "
  "read the open source projects. FinRL and Trading Agents are on GitHub. And skim the "
  "occasional quant finance paper, even if you only get half of it. [pause] And for "
  "community, learn in the open, from people showing their code and their losses. "
  "[pause] Run, fast, from any group that promises signals or guaranteed returns. You "
  "already know exactly why."),

 ("s64_final", "ait_callout",
  {"kicker": "THE WHOLE COURSE IN ONE THOUGHT", "color": "edge",
   "text": "AI trading is real — but the edge is a process you build, not a product you buy.",
   "sub": "Master the pipeline, respect the risk, and the AI becomes a tool, not a gamble."},
  "If you take just one thought from this entire course, let it be this. [pause] A I "
  "trading is completely real. But the edge is a process you build, not a product you "
  "buy. [pause] Anyone selling you the product, the bot, the signal, the guaranteed "
  "system, has it exactly backwards. [pause] Master the pipeline. Respect the risk. "
  "Test everything honestly. Do that, and A I stops being a gamble, and becomes just a "
  "tool. A powerful one, in the hands of someone who did the work. [pause] Let's tie "
  "the whole map together."),
]

if __name__ == "__main__":
    core.build("ch6", SEGMENTS, target_min=7)
