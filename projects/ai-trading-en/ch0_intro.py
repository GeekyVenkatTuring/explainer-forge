#!/usr/bin/env python3
"""Chapter 0 — Intro: title, the two-truths hook, the roadmap."""
import aitcore as core

SEGMENTS = [
 ("s00_title", "ait_title", {},
  "A lot of people are talking about A I trading. Bots and agents that trade the "
  "markets for you. [pause] So let's do this honestly. What it really is, how to start, "
  "where to do it safely, and how to build your own from scratch."),

 ("s01_hook", "ait_hook",
  {"kicker": "TWO THINGS ARE TRUE", "title": "Start with the honest picture",
   "left": {"emoji": "🏦", "h": "Wall Street runs on AI", "body": "Roughly three in four big trading desks already use machine learning.", "c": "money"},
   "right": {"emoji": "📉", "h": "Most retail bots lose", "body": "Studies suggest the large majority of small traders' bots lose money.", "c": "risk"},
   "closer": "This course takes both seriously — the real power, and the very real trap."},
  "Here is the honest picture, up front. [pause] On one side, the biggest funds in the "
  "world trade with A I every single day. Roughly three out of four large desks use "
  "machine learning. [pause] On the other side, when ordinary people run trading bots, "
  "the large majority lose money. [pause] Both of these are true at the same time. "
  "So we are not going to hype this, and we are not going to dismiss it. We are going "
  "to understand it."),

 ("s02_roadmap", "ait_cards",
  {"kicker": "THE MAP", "title": "Six parts, one honest goal", "color": "data",
   "cards": [
     {"emoji": "🧠", "title": "1 · What it is", "body": "The real mechanics behind the buzzword.", "c": "data"},
     {"emoji": "⚠️", "title": "2 · The reality", "body": "Why most bots quietly lose — and the scams.", "c": "risk"},
     {"emoji": "🎒", "title": "3 · Before you start", "body": "What to learn, and the honest mindset.", "c": "edge"},
     {"emoji": "🏛️", "title": "4 · Where to do it", "body": "Trustworthy platforms and the SEBI rules.", "c": "money"},
     {"emoji": "🛠️", "title": "5 · Build your own", "body": "From a first strategy to an AI agent, in code.", "c": "ai"},
     {"emoji": "🗺️", "title": "6 · Your plan", "body": "A realistic ninety-day path.", "c": "data"}]},
  "Here is the map. [pause] Part one, what A I trading actually is, underneath the "
  "buzzword. Part two, the reality check. Why so many bots lose, and how to spot the "
  "scams. [pause] Part three, what you need to know before you start. Part four, where "
  "you can actually do this safely, including India's new rules. [pause] Part five is "
  "the big one. Building your own bot from scratch, in real code. And part six, a "
  "realistic plan for your first ninety days. [pause] Quick note before we go. This is "
  "education, not investment advice. Nothing here is a buy or sell call."),
]

if __name__ == "__main__":
    core.build("ch0", SEGMENTS, target_min=3.5)
