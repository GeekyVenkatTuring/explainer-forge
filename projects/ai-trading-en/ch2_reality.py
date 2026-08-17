#!/usr/bin/env python3
"""Chapter 2 — Part 2: The reality check (why bots lose, costs, scams)."""
import aitcore as core

SEGMENTS = [
 ("s20_divider", "ait_divider",
  {"n": 2, "title": "The Reality Check", "sub": "Why most bots quietly lose money", "color": "risk", "parts": 6},
  "Part two. The reality check. [pause] I am putting this early on purpose, before you "
  "spend a rupee or write a line of code. Because this part is what protects you."),

 ("s21_numbers", "ait_stat",
  {"kicker": "THE UNCOMFORTABLE NUMBERS", "title": "What the studies actually show", "color": "risk",
   "stats": [
     {"value": 80, "suffix": "%+", "label": "of retail bot users end up losing money", "src": "multiple industry studies", "c": "risk"},
     {"value": 0.025, "prefix": "R² < ", "decimals": 3, "label": "how well a backtest predicts live results", "src": "study of 888 strategies", "c": "edge"},
     {"value": 90, "prefix": "~", "suffix": " days", "label": "how fast many bots blow up", "src": "reported bot lifetimes", "c": "ai"}],
   "note": "Treat scary stats as directional, not gospel — but the direction is clear."},
  "Let's start with the uncomfortable numbers. [pause] Across multiple studies, more "
  "than eighty percent of people who run retail trading bots end up losing money. "
  "[pause] Here is the one that really matters. Researchers looked at eight hundred and "
  "eighty eight real trading strategies. They found that how well a strategy did in "
  "backtesting told you almost nothing about how it would do live. [pause] The link "
  "was statistically close to zero. [pause] Now, I would treat the scariest headline "
  "numbers as directional, not gospel. Some come from marketing. But the direction is "
  "not in doubt. A great backtest is not a promise. Not even close."),

 ("s21b_biases", "ait_cards",
  {"kicker": "FOUR WAYS BACKTESTS LIE", "title": "The biases that fake a great result", "color": "risk",
   "cards": [
     {"emoji": "🔮", "title": "Look-ahead", "body": "Using data that didn't exist yet at that moment.", "tag": "the classic", "c": "risk"},
     {"emoji": "⚰️", "title": "Survivorship", "body": "Testing only on companies that didn't go bust.", "tag": "silent", "c": "edge"},
     {"emoji": "🎣", "title": "Data snooping", "body": "Trying 1,000 ideas and keeping the one that 'worked'.", "tag": "sneaky", "c": "ai"},
     {"emoji": "🧴", "title": "Cherry-picking", "body": "Choosing the one period where your bot shines.", "tag": "human", "c": "data"}]},
  "A backtest can lie to you in four distinct ways. Learn their names, so you can catch "
  "them. [pause] One, look ahead bias. Using data that did not exist yet at that moment. "
  "We will fix this in code later. [pause] Two, survivorship bias. Testing only on the "
  "companies that survived. The ones that went bankrupt vanished from your data, so your "
  "results look far safer than reality. [pause] Three, data snooping. You try a thousand "
  "random ideas, and one of them looks brilliant by pure luck. You keep that one and "
  "forget the rest. [pause] Four, cherry picking. You quietly choose the one time period "
  "where your bot happens to shine. [pause] Every one of these produces a beautiful, "
  "fake result. Half of becoming good at this is simply learning not to fool yourself."),

 ("s22_overfitting", "ait_callout",
  {"kicker": "THE NUMBER ONE KILLER", "color": "risk",
   "text": "Overfitting: your bot memorised the past instead of learning.",
   "sub": "A 70% win rate on old data can flip to a loss the day it goes live."},
  "So why do they fail? The number one reason has a name. Overfitting. [pause] Here is "
  "what it means in plain English. You tweak your strategy until it looks perfect on "
  "old data. Ninety, ninety five percent winners. It feels amazing. [pause] But you did "
  "not find a real pattern. You memorised the noise. You fit your rules to random luck "
  "that will never repeat. [pause] The moment that bot meets tomorrow's market, which "
  "it has never seen, the magic vanishes. That glorious backtest becomes a real loss. "
  "[pause] Almost every blown up retail bot died of overfitting. Later, in part five, "
  "I will show you the exact technique that fights it."),

 ("s23_whyfail", "ait_cards",
  {"kicker": "THE FIVE HORSEMEN", "title": "Five ways a bot quietly bleeds out", "color": "risk",
   "cards": [
     {"emoji": "🧬", "title": "Overfitting", "body": "It learned noise, not a real edge.", "tag": "the big one", "c": "risk"},
     {"emoji": "💸", "title": "Costs", "body": "Fees, taxes and slippage eat a thin edge alive.", "tag": "silent killer", "c": "edge"},
     {"emoji": "🐢", "title": "Latency", "body": "You fill seconds after the pros — at worse prices.", "tag": "structural", "c": "ai"},
     {"emoji": "🌊", "title": "Regime change", "body": "The market that fit your bot is already gone.", "tag": "inevitable", "c": "data"},
     {"emoji": "😰", "title": "You", "body": "Panic, overrides and greed break the best system.", "tag": "human", "c": "money"}]},
  "Overfitting is the biggest killer, but it has four companions. [pause] Costs. Fees, "
  "taxes, and slippage quietly eat a thin edge alive. We will do the actual math in a "
  "moment. [pause] Latency. You fill your orders seconds after the professionals, at "
  "worse prices. [pause] Regime change. Markets shift. The calm market your bot learned "
  "on gets replaced by a wild one, and your rules no longer fit. [pause] And the last "
  "one is you. The human. Panic selling, overriding the bot, doubling down out of "
  "greed. The best system in the world cannot survive an emotional operator. Five "
  "horsemen. Respect all of them."),

 ("s24_costs", "ait_gauge",
  {"kicker": "THE SILENT KILLER", "title": "In India, costs are brutal for frequent trading", "color": "risk",
   "segs": [
     {"label": "brokerage · ~₹20 / order", "h": 130, "c": "edge", "note": "Flat per order. It grows with how often you trade, not with profit."},
     {"label": "S T T · the big one", "h": 250, "c": "risk", "note": "On a delivery round-trip, tax can be the bulk of your cost."},
     {"label": "slippage + GST + stamp", "h": 170, "c": "ai", "note": "The gap between the backtest price and the price you truly get."}],
   "counter": {"value": 22, "suffix": "%", "label": "annual drag at just ~100 trades", "c": "risk"},
   "caption": "The more your bot trades, the more it must beat just to break even."},
  "Let's talk about the silent killer. Costs. And in India, they are brutal for a bot "
  "that trades a lot. [pause] Every single order pays brokerage. Roughly twenty rupees. "
  "That fee grows with how often you trade, not with how much you make. [pause] Then "
  "there is the securities transaction tax, the S T T. On a delivery trade, this tax "
  "can be the biggest single cost of the whole round trip. [pause] Add slippage, G S "
  "T, and stamp duty on top. [pause] Stack it all up, and even at a modest hundred "
  "trades, costs can drag your yearly return down by around twenty percent. The more "
  "your bot trades, the bigger the edge it needs just to break even."),

 ("s25_costbars", "ait_bars",
  {"kicker": "FOLLOW ONE RUPEE", "title": "Watch costs eat a ₹100 gross profit", "color": "risk", "unit": "", "max": 100,
   "bars": [
     {"label": "gross edge", "v": 100, "c": "money"},
     {"label": "after brokerage", "v": 82, "c": "edge"},
     {"label": "after taxes", "v": 55, "c": "risk"},
     {"label": "after slippage", "v": 34, "c": "ai"},
     {"label": "net you keep", "v": 22, "c": "data"}],
   "note": "Illustrative — but this shape is exactly why over-trading turns edges negative."},
  "Let's follow a single rupee to make this real. [pause] Say your strategy makes a "
  "hundred rupees of gross profit before any costs. [pause] Take out brokerage, you are "
  "down to eighty two. Take out the taxes, and you are near fifty five. [pause] Now "
  "slippage. The price you actually get is worse than the price in your backtest. That "
  "drops you to the thirties. [pause] By the time everything clears, you might keep "
  "around twenty two out of your hundred. [pause] These exact figures are just an "
  "illustration. But the shape is real. This is precisely why a strategy that looks "
  "profitable on paper can bleed money the moment it trades often. Costs are not a "
  "detail. They decide who wins."),

 ("s26_regime", "ait_callout",
  {"kicker": "A MOVING TARGET", "color": "ai",
   "text": "The market you perfectly fit yesterday no longer exists.",
   "sub": "Edges decay. A live strategy is a garden, not a statue."},
  "There is one more truth that beginners always miss. [pause] The market is not a "
  "fixed puzzle you solve once. It is alive, and it changes. [pause] When you find an "
  "edge, other people find it too. They pile in, and it fades. This is called edge "
  "decay, and it happens to everyone, even the giants. [pause] So the market you fit "
  "perfectly yesterday does not quite exist today. [pause] This changes how you should "
  "think. A live strategy is not a statue you carve once and admire forever. It is a "
  "garden. It needs constant checking, weeding, and sometimes tearing out. If that "
  "sounds like work, it is. That is the job."),

 ("s27_scams", "ait_list",
  {"kicker": "PROTECT YOURSELF", "title": "How to spot an AI-trading scam", "tone": "bad", "color": "risk",
   "items": [
     {"h": "It promises guaranteed or “assured” returns", "sub": "No real strategy can promise profit in a volatile market. None."},
     {"h": "It asks you to deposit into their account", "sub": "Your money must always stay in your own broker account."},
     {"h": "It claims to be “SEBI approved”", "sub": "Check the registration number on the SEBI site. Most are fake."},
     {"h": "Influencers and Telegram groups push urgency", "sub": "“Act now, seats closing” is the oldest trick in the book."}],
   "caption": "Reported losses to such scams in India ran into tens of thousands of crores in 2024."},
  "Now the part that can save you real money. Scams. [pause] Fake A I trading products "
  "are everywhere, and in twenty twenty four, reported losses in India ran into tens of "
  "thousands of crores. [pause] They share the same fingerprints. One. They promise "
  "guaranteed or assured returns. No honest strategy ever can. That word alone should "
  "end the conversation. [pause] Two. They ask you to deposit money into their account. "
  "Never do this. Your money stays in your own broker account, always. [pause] Three. "
  "They claim to be SEBI approved. So check the registration number yourself, on the "
  "official SEBI website. Most simply do not exist. [pause] Four. Influencers and "
  "Telegram groups pushing urgency. Real investing is never seats closing in ten "
  "minutes."),

 ("s28_verify", "ait_list",
  {"kicker": "THREE RULES THAT KEEP YOU SAFE", "title": "Your permanent scam shield", "tone": "ok", "color": "money",
   "items": [
     {"h": "Money never leaves your own broker account", "sub": "Legit tools connect via API. They never hold your cash."},
     {"h": "Verify every claim on the official SEBI site", "sub": "Type the name yourself. Never trust a forwarded link."},
     {"h": "“Guaranteed” means walk away — every time", "sub": "Risk is the price of return. Anyone hiding it is lying."}],
   "caption": "These three habits alone stop the vast majority of investment fraud."},
  "So here is your permanent shield. Three rules, and they never change. [pause] Rule "
  "one. Your money never leaves your own broker account. A legitimate tool connects "
  "through an official A P I. It never holds your cash. [pause] Rule two. Verify every "
  "single claim yourself on the official SEBI website. Type the name in with your own "
  "fingers. Never trust a link someone forwarded you. [pause] Rule three. The word "
  "guaranteed means walk away. Every time, no exceptions. Risk is the price you pay for "
  "return. Anyone who hides the risk is lying to you. [pause] These three habits alone "
  "will stop almost every scam that will ever come your way."),

 ("s23b_overfit_demo", "ait_bars",
  {"kicker": "SEE OVERFITTING HAPPEN", "title": "₹100 in the backtest vs the real world", "color": "risk", "unit": "", "max": 220,
   "bars": [
     {"label": "backtest says", "v": 218, "c": "money"},
     {"label": "you expect", "v": 218, "c": "money"},
     {"label": "first month", "v": 112, "c": "edge"},
     {"label": "after 3 months", "v": 91, "c": "risk"},
     {"label": "after costs", "v": 79, "c": "risk"}],
   "note": "Illustrative ₹ value of a ₹100 stake — but this cliff is retail's most common shape."},
  "Let me show you the shape of overfitting, because you will feel this. [pause] Imagine "
  "a bot that turned a hundred rupees into two hundred and eighteen in your backtest. "
  "You are thrilled. You expect roughly that going forward. [pause] Then it goes live. "
  "After the first month, your hundred rupees is worth a hundred and twelve. "
  "Disappointing, but okay. [pause] After three months, it is down to ninety one. And "
  "once you subtract the trading costs, you are at seventy nine. A real loss. [pause] "
  "These numbers are illustrative. But this exact cliff, glorious in the backtest, then "
  "a slow bleed live, is the single most common shape in all of retail trading. [pause] "
  "The backtest was not lying about the past. It was lying about the future. Never "
  "forget the difference."),

 ("s25b_marketplace", "ait_list",
  {"kicker": "A SPECIFIC TRAP", "title": "Why marketplace strategies look too good", "tone": "bad", "color": "risk",
   "items": [
     {"h": "Survivorship on display", "sub": "You see the strategies that happened to work — not the thousands that died."},
     {"h": "Backtests are marketing, not proof", "sub": "A curve tuned to the past is designed to make you subscribe."},
     {"h": "Crowding kills the edge", "sub": "The moment a strategy is popular, too many people trade it and it fades."},
     {"h": "Their incentive is subscriptions, not your profit", "sub": "They earn whether you win or lose. Remember that."}],
   "caption": "Use marketplaces to learn the mechanics — never to blindly copy an edge."},
  "Let's expose one specific trap, because it catches beginners constantly. The "
  "strategy marketplace. [pause] You open a platform and see strategies boasting "
  "incredible returns. Here is what you are not seeing. [pause] Survivorship. You see "
  "the handful that happened to work. The thousands that failed were quietly deleted. "
  "[pause] Those pretty backtests are marketing, tuned to the past to make you "
  "subscribe. [pause] And even the genuinely good ones get crowded. The moment a "
  "strategy becomes popular, too many people pile in, and its edge fades. [pause] "
  "Above all, remember their incentive. They earn from your subscription, whether you "
  "win or lose. [pause] Use marketplaces to learn how strategies are built. Never to "
  "blindly copy an edge."),

 ("s26b_psychology", "ait_cards",
  {"kicker": "THE ENEMY IN THE MIRROR", "title": "Four emotions that break good bots", "color": "risk",
   "cards": [
     {"emoji": "😱", "title": "Fear", "body": "You kill the bot during a drawdown — right before it recovers.", "c": "risk"},
     {"emoji": "🤑", "title": "Greed", "body": "You override its size limits after a winning streak.", "c": "edge"},
     {"emoji": "🎰", "title": "Revenge", "body": "You force trades to win back a loss. The account bleeds faster.", "c": "ai"},
     {"emoji": "🙈", "title": "Hope", "body": "You cancel the stop-loss, praying a loser turns around.", "c": "data"}]},
  "We said the fifth horseman is you. Let's name the four emotions that do the damage. "
  "[pause] Fear. The bot hits a rough patch, a drawdown, and you panic and switch it "
  "off, right before it would have recovered. [pause] Greed. After a winning streak, "
  "you feel invincible and override the size limits. Then one bad trade wipes out ten "
  "good ones. [pause] Revenge. You take a loss, and you force new trades to win it "
  "back. The account bleeds faster. [pause] And hope. A trade goes against you, so you "
  "cancel the stop loss, praying it turns around. [pause] Here is the irony. We "
  "automate trading to remove emotion. But the human who can override the bot is still "
  "the biggest risk. The discipline to leave your own system alone is a superpower."),

 ("s28b_case", "ait_list",
  {"kicker": "ANATOMY OF A SCAM", "title": "How a fake AI-bot pitch actually unfolds", "tone": "bad", "color": "risk",
   "items": [
     {"h": "1 — The hook: a screenshot of huge profits", "sub": "Faked or cherry-picked. Anyone can photoshop a P&L."},
     {"h": "2 — The proof: a paid influencer vouches", "sub": "Borrowed trust. They're an actor, not a client."},
     {"h": "3 — The ask: “deposit to activate the AI”", "sub": "The instant money leaves your account, it's gone."},
     {"h": "4 — The trap: small fake “profits” to lure more", "sub": "You see gains on their dashboard — until you try to withdraw."}],
   "caption": "The dashboard is a puppet show. Real profit you can't withdraw isn't profit."},
  "Let's walk through exactly how one of these scams unfolds, so you recognise it "
  "instantly. [pause] Step one, the hook. A screenshot of massive profits. It is faked, "
  "or cherry picked. Anyone can photoshop a profit and loss statement. [pause] Step "
  "two, the proof. A paid influencer vouches for it. That is borrowed trust. They are "
  "an actor, not a happy customer. [pause] Step three, the ask. Deposit money to "
  "activate the A I. The moment your money leaves your own account, it is gone. [pause] "
  "Step four, the trap. Their dashboard shows small fake profits, to lure you into "
  "depositing more. [pause] Then you try to withdraw, and everything freezes. The whole "
  "dashboard was a puppet show. Profit you cannot withdraw was never profit."),

 ("s29_micro", "ait_callout",
  {"kicker": "PART TWO IN ONE LINE", "color": "risk",
   "text": "If it's guaranteed, it's a lie. If it's easy, it's already gone.",
   "sub": "Now that you're protected, let's build real skill."},
  "Let's lock in part two with one line. [pause] If it is guaranteed, it is a lie. And "
  "if it is easy, the edge is already gone. [pause] That is not me being negative. That "
  "is me handing you the two sentences that separate people who survive this game from "
  "people who fund it. [pause] Okay. You now know the traps. From here on, we build "
  "real skill. Let's talk about what you actually need to get started."),
]

if __name__ == "__main__":
    core.build("ch2", SEGMENTS, target_min=14)
