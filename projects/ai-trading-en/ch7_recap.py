#!/usr/bin/env python3
"""Chapter 7 — Recap + disclaimer."""
import aitcore as core

SEGMENTS = [
 ("s70_recap", "ait_recap",
  {"kicker": "RECAP — THE WHOLE MAP", "title": "AI trading in one breath",
   "items": [
     "AI trading = the Data → Model → Signal → Risk → Order pipeline, automated",
     "AI only lives in the model box — it finds patterns, it can't predict",
     "Institutions win on speed and scale; your only hope is a smarter, slower niche",
     "Most bots die of overfitting, costs, and latency — the backtest is a hypothesis",
     "Start no-code, keep money in your own broker, and follow SEBI's rules",
     "Build in code box-by-box; add AI last; walk-forward is your honesty test",
     "The edge is a process you build, not a product you buy"],
   "closer": "Trade the process, not the hype. Thanks for watching."},
  "Let's tie the whole map together, in one breath. [pause] A I trading is the data, "
  "model, signal, risk, order pipeline, automated. [pause] The A I lives only in the "
  "model box. It finds patterns. It cannot see the future. [pause] Institutions win on "
  "speed and scale, so your only hope is a smarter, slower niche. [pause] Most bots die "
  "of overfitting, costs, and latency. Always remember, the backtest is a hypothesis, "
  "not a promise. [pause] Start no code, keep your money in your own broker, and follow "
  "the rules. [pause] Build in code, box by box, and add the A I last. Walk forward is "
  "your honesty test. [pause] And above all, the edge is a process you build, not a "
  "product you buy. [pause] Trade the process, not the hype."),

 ("s71_disclaimer", "ait_list",
  {"kicker": "BEFORE YOU GO", "title": "One important disclaimer", "tone": "neutral", "color": "risk",
   "items": [
     {"h": "This is education, not investment advice", "sub": "Nothing here is a buy, sell, or hold recommendation for anyone."},
     {"h": "Markets carry real risk of real loss", "sub": "You can lose money, quickly. Never risk what you can't afford to lose."},
     {"h": "Verify every rule and figure yourself", "sub": "Regulations and costs change — confirm on official SEBI and exchange sites."},
     {"h": "For personal advice, see a SEBI-registered advisor", "sub": "A licensed professional can look at your specific situation."}],
   "caption": "Learn deeply, act carefully, and let the process protect you."},
  "One last, important note before you go. [pause] Everything in this course is "
  "education, not investment advice. Nothing here is a recommendation to buy, sell, or "
  "hold anything. [pause] Markets carry a real risk of real loss. You can lose money "
  "quickly, so never risk what you cannot afford to lose. [pause] The rules, costs, and "
  "figures I mentioned can change, so verify them yourself on the official SEBI and "
  "exchange websites. [pause] And for advice about your specific situation, please "
  "speak with a SEBI registered advisor. [pause] Learn deeply, act carefully, and let "
  "the process protect you. Good luck, and thanks for watching."),
]

if __name__ == "__main__":
    core.build("ch7", SEGMENTS, target_min=3.5)
