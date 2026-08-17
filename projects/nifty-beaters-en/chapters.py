#!/usr/bin/env python3
"""CHAPTERS for "50 to Beat the Nifty". Built from research/picks.json (50 picks,
exact real fundamentals). Per-stock narration weaves the standout metric (shown
exactly on screen) with the curated 3-point thesis. Framework / risk / recap
chapters are hand-written. High-conviction tone; honesty gates in the copy."""
import json, os

ROOT = os.path.dirname(os.path.abspath(__file__))
PICKS = json.load(open(os.path.join(ROOT, "research", "picks.json")))
BYT = {"1": [p for p in PICKS if p["tier"] == "1"],
       "2": [p for p in PICKS if p["tier"] == "2"],
       "3": [p for p in PICKS if p["tier"] == "3"]}
GLOBAL_IDX = {p["ticker"]: i + 1 for i, p in enumerate(PICKS)}  # 1..50 in tier order

# ---- per-stock narration ---------------------------------------------------
def hero_intro(p):
    m = next((x for x in p["metrics"] if x["hero"]), p["metrics"][0])
    k, cap, sector = m["k"], p["cap"].lower(), p["sector"]
    if k == "P / E":
        return f"a {cap} {sector} name trading cheap for the quality you get"
    if k == "ROE":
        return f"a {cap} {sector} business earning strong, durable returns on equity"
    if k == "ROCE":
        return f"a {cap} {sector} business with elite returns on the capital it puts to work"
    if "profit" in k.lower():
        return f"a {cap} {sector} name with profits compounding at a genuinely rare pace"
    if "sales" in k.lower():
        return f"a {cap} {sector} name growing its top line fast"
    return f"a {cap} {sector} name with standout fundamentals"

def _num(s):
    """pull the leading number out of a metric string like '18.1', '15.9%', '₹10.16L Cr'."""
    import re
    m = re.search(r"-?\d+\.?\d*", s.replace(",", ""))
    return float(m.group()) if m else None

def spoken_metrics(p):
    mv = {x["k"]: x["v"] for x in p["metrics"]}
    pe = _num(mv.get("P / E", "")); roe = _num(mv.get("ROE", "")); roce = _num(mv.get("ROCE", ""))
    pg = _num(mv.get("5Y profit CAGR", "")); sg = _num(mv.get("5Y sales CAGR", ""))
    bits = []
    if pe is not None:
        if pe < 15: bits.append(f"it trades at just {round(pe)} times earnings")
        elif pe < 35: bits.append(f"it trades at about {round(pe)} times earnings")
        else: bits.append(f"it isn't cheap, at {round(pe)} times earnings")
    if roce is not None and roce >= 18: bits.append(f"it earns a {round(roce)} percent return on capital")
    elif roe is not None: bits.append(f"return on equity runs near {round(roe)} percent")
    gr = pg if (pg is not None and pg > 0) else (sg if sg is not None else None)
    if gr is not None and gr > 0:
        word = "profits" if (pg is not None and pg > 0) else "sales"
        bits.append(f"and {word} have compounded around {round(gr)} percent a year")
    if not bits:
        return "The exact fundamentals are on screen."
    return "The numbers: " + ", ".join(bits) + "."

def stock_segment(p):
    gi = GLOBAL_IDX[p["ticker"]]
    props = {"idx": gi, "total": 50, "tier": p["tier"], "name": p["name"], "ticker": p["ticker"],
             "sector": p["sector"], "cap": p["cap"], "metrics": p["metrics"],
             "thesis": p["thesis"], "growth": p["growth"], "take": p["take"]}
    t = p["thesis"]
    narr = (f"Pick number {gi}. {p['name']}. [pause] "
            f"This is {hero_intro(p)}. [pause] "
            f"{spoken_metrics(p)} [pause] "
            f"Here's the case. {t[0]} [pause] {t[1]} [pause] {t[2]} [pause] "
            f"In short: {p['take'].lower()}.")
    return (f"s{gi:02d}_{p['ticker'].replace('&','').replace('-','').lower()}", "nb_stock", props, narr)

def tierboard_segment(tier, title, sub):
    names = [p["name"] for p in BYT[tier]]
    n = len(names)
    speak = ", ".join(names[:4]) + f", and {n - 4} more"
    return (f"board", "nb_tierboard", {"tier": tier, "title": title, "sub": sub, "names": names},
            f"Here is the full Tier {tier} line-up — {n} companies. {speak}. [pause] "
            f"Let's take them one at a time, and see why each one earns its place.")

# ============================================================ CHAPTER 1
ch1 = [
 ("title", "nb_title", {"dur": 0},
  "Fifty stocks. One benchmark to beat. [pause] The Nifty 50 is the index most Indian "
  "portfolios are measured against. [pause] In this series we go through every listed "
  "sector, and build a conviction portfolio of fifty companies we believe can beat that "
  "index over the next one to five years — and we show you the real numbers behind each one."),

 ("bar", "nb_statement", {"dur": 0, "kicker": "THE BAR", "color": "#38BDF8",
   "lines": ["The index is the bar.", "Beating it is the job.", "Most funds don't."],
   "sub": "To beat the Nifty, you can't just own the Nifty."},
  "Start with a hard truth. [pause] Over the long run, most active funds fail to beat the "
  "index they benchmark against. [pause] So why try to pick stocks at all? [pause] Because "
  "the index is just the average — market-cap weighted, dominated by a handful of giants. "
  "To beat the average, your portfolio has to look different from it. That difference is "
  "where the extra return, the alpha, has to come from."),

 ("funnel", "nb_funnel", {"dur": 0},
  "So here's how we got to fifty. [pause] We started with the entire universe — roughly "
  "two thousand four hundred companies listed on the exchange, across twenty-two sectors. "
  "[pause] From that, we drew up a shortlist of about two hundred and sixty quality and "
  "growth candidates, and pulled their real fundamentals — price-to-earnings, return on "
  "equity and capital, and multi-year growth. [pause] Then we scored, ranked, and "
  "diversified down to a final fifty. Every number you'll see is real, and sourced."),

 ("score", "nb_scorecard", {"dur": 0},
  "Each of the fifty had to pass five tests. [pause] One — quality: the business earns "
  "high, durable returns on its capital. [pause] Two — growth: sales and profits have "
  "been compounding, not stalling. [pause] Three — valuation sanity: we won't pay any "
  "price, so we weigh price against the growth we're buying. [pause] Four — a moat and a "
  "runway: a structural tailwind the next five years extend. [pause] And five — "
  "investability: enough size and liquidity to actually own it."),

 ("tiers", "nb_statement", {"dur": 0, "kicker": "THREE TIERS", "color": "#34D399",
   "lines": ["Tier 1 — Core compounders.", "Tier 2 — Growth accelerators.", "Tier 3 — High risk, high reward."],
   "sub": "Sorted by conviction and risk, not by hype."},
  "We've sorted the fifty into three tiers, by conviction and risk. [pause] Tier one — the "
  "core compounders: the highest-quality businesses, steadier, the ones you can hold "
  "through a storm. [pause] Tier two — the growth accelerators: faster-growing, riding "
  "clear structural themes, with a little more volatility. [pause] And tier three — high "
  "risk, high reward: cyclicals, turnarounds, and smaller companies where the upside is "
  "bigger, and so is the risk. Size those positions accordingly."),

 ("how", "nb_statement", {"dur": 0, "kicker": "BEFORE WE BEGIN", "color": "#FB7185",
   "lines": ["This is analysis.", "Not investment advice.", "Do your own work."],
   "sub": "Figures point-in-time (screener.in, Aug 2026). Past performance ≠ future returns."},
  "One important thing before we begin. [pause] Everything here is analysis built from "
  "public data — it is not investment advice, and it is not a recommendation to buy or "
  "sell anything. [pause] The figures are point-in-time, from public sources as of August "
  "twenty twenty-six, and they change. Past performance does not guarantee future returns. "
  "[pause] Treat this as a starting point for your own research, and if you need it, talk "
  "to a registered advisor. Now — let's meet the fifty."),
]

# ============================================================ CHAPTER 2 (Tier 1)
ch2 = [
 ("div", "nb_divider", {"dur": 0, "n": 2, "title": "Core Compounders", "sub": "Tier 1 · the sleep-well-at-night quality", "tier": "1", "total": 5},
  "Chapter two. Tier one — the core compounders. [pause] These sixteen are the backbone of "
  "the portfolio: high-quality businesses with durable returns and reasonable valuations. "
  "The kind of companies you can own through a downturn and keep compounding."),
 tierboard_segment("1", "Tier 1 · Core Compounders", "Sixteen quality businesses to anchor the portfolio"),
] + [stock_segment(p) for p in BYT["1"]] + [
 ("wrap", "nb_statement", {"dur": 0, "kicker": "TIER 1 · IN ONE LINE", "color": "#34D399",
   "lines": ["Quality, bought fairly,", "held for years,", "compounds quietly."],
   "sub": "The core does the steady work. Now the accelerators."},
  "So that's tier one. [pause] Sixteen quality franchises — banks, industrials, consumer, "
  "pharma, IT — bought at fair prices, built to compound quietly for years. [pause] They "
  "won't be the flashiest names in the portfolio. They're the ones that let you sleep. "
  "[pause] Next, we shift up a gear — to the growth accelerators."),
]

# ============================================================ CHAPTER 3 (Tier 2)
ch3 = [
 ("div", "nb_divider", {"dur": 0, "n": 3, "title": "Growth Accelerators", "sub": "Tier 2 · structural themes, compounding faster", "tier": "2", "total": 5},
  "Chapter three. Tier two — the growth accelerators. [pause] Eighteen companies riding "
  "clear structural themes: electronics manufacturing, financialisation, premium "
  "consumption, healthcare, real estate. Faster growth, a little more volatility, and a "
  "lot of runway."),
 tierboard_segment("2", "Tier 2 · Growth Accelerators", "Eighteen names levered to India's structural themes"),
] + [stock_segment(p) for p in BYT["2"]] + [
 ("wrap", "nb_statement", {"dur": 0, "kicker": "TIER 2 · IN ONE LINE", "color": "#FBBF24",
   "lines": ["Ride the theme,", "pay for growth carefully,", "let the runway work."],
   "sub": "The accelerators drive returns. Now the high-torque bets."},
  "That's tier two. [pause] Eighteen accelerators, each plugged into a theme that should "
  "outlast the next few years — manufacturing, financial-market infrastructure, "
  "premiumisation, hospitals, housing. [pause] Here you're paying more for growth, so the "
  "discipline is to pay carefully and let the runway do the work. [pause] Finally, the "
  "part of the portfolio with the biggest swings — tier three."),
]

# ============================================================ CHAPTER 4 (Tier 3)
ch4 = [
 ("div", "nb_divider", {"dur": 0, "n": 4, "title": "High Risk, High Reward", "sub": "Tier 3 · cyclicals, turnarounds, small-caps", "tier": "3", "total": 5},
  "Chapter four. Tier three — high risk, high reward. [pause] Sixteen companies with the "
  "biggest potential upside in the portfolio, and the biggest risks: defence and railway "
  "cyclicals, commodity plays, turnarounds, and smaller names. [pause] These are the "
  "positions you size smaller, and watch closer."),
 tierboard_segment("3", "Tier 3 · High Risk · High Reward", "Sixteen higher-torque bets — size them smaller"),
] + [stock_segment(p) for p in BYT["3"]] + [
 ("wrap", "nb_statement", {"dur": 0, "kicker": "TIER 3 · IN ONE LINE", "color": "#FB7185",
   "lines": ["Bigger upside,", "bigger risk,", "smaller position."],
   "sub": "High-torque bets earn their place — in moderation."},
  "And that completes tier three. [pause] Sixteen higher-torque bets — where an order win, "
  "a commodity up-cycle, or a turnaround landing can drive outsized returns, but where the "
  "downside is real too. [pause] The rule here is simple: bigger upside, bigger risk, "
  "smaller position. [pause] Now let's put all fifty together, and talk honestly about "
  "what could go wrong."),
]

# ============================================================ CHAPTER 5 (Portfolio + Risks)
def portfolio_props():
    return {"dur": 0, "picks": [{"t": p["tier"], "nm": p["name"]} for p in PICKS]}

ch5 = [
 ("div", "nb_divider", {"dur": 0, "n": 5, "title": "The Portfolio", "sub": "All fifty · allocation, risks, and honesty", "tier": "1", "total": 5},
  "Chapter five. The portfolio. [pause] Fifty companies, three tiers, across more than ten "
  "sectors. Let's see the whole thing at once, weigh the risks, and be honest about the "
  "limits of an exercise like this."),

 ("grid", "nb_portfolio", portfolio_props(),
  "Here they are — all fifty, colour-coded by tier. [pause] Green is the core, amber the "
  "accelerators, rose the high-risk bets. [pause] Notice what's here — and what isn't. "
  "We've deliberately leaned away from the very largest index heavyweights, because owning "
  "those simply is owning the Nifty. To beat the index, this portfolio has to look "
  "different from it — and it does."),

 ("alloc", "nb_bars", {"dur": 0, "kicker": "THE SHAPE OF IT", "title": "Where the conviction sits", "unit": "",
   "bars": [{"label": "Tier 1\nCore", "v": 16, "c": "#34D399"},
            {"label": "Tier 2\nGrowth", "v": 18, "c": "#FBBF24"},
            {"label": "Tier 3\nHigh-risk", "v": 16, "c": "#FB7185"}],
   "foot": "A barbell: a steady core, a growth engine, and a smaller high-torque sleeve."},
  "The shape of the portfolio is a barbell. [pause] Sixteen steady compounders at the core. "
  "Eighteen growth accelerators as the engine. And sixteen high-risk, high-reward bets as a "
  "smaller, higher-torque sleeve. [pause] In practice you would weight the core most "
  "heavily, the accelerators next, and keep each high-risk position small — so no single "
  "bet can sink the whole ship."),

 ("risk", "nb_statement", {"dur": 0, "kicker": "WHAT COULD GO WRONG", "color": "#FB7185",
   "lines": ["Valuations can compress.", "Cycles can turn.", "Theses can break."],
   "sub": "Five honest risks every one of these carries."},
  "Now the part most stock lists skip — what could go wrong. [pause] First, valuation: "
  "several of these are priced for perfection, and a growth wobble can compress the "
  "multiple hard. [pause] Second, cyclicality: the defence, metals, and infra names swing "
  "with government orders and commodity prices. [pause] Third, execution: turnarounds and "
  "capacity build-outs don't always land on time. [pause] Fourth, concentration: leaning "
  "into a few themes cuts both ways. [pause] And fifth, the macro: rates, elections, and "
  "global shocks move everything at once."),

 ("use", "nb_statement", {"dur": 0, "kicker": "HOW TO USE THIS", "color": "#38BDF8",
   "lines": ["Position sizing.", "Stagger your entries.", "Review every quarter."],
   "sub": "A framework to research — not a signal to buy."},
  "So how should you use this? [pause] As a research map, not a buy button. [pause] Size "
  "your positions to your own risk appetite. Stagger your entries instead of buying all at "
  "once. Re-check the thesis and the numbers every quarter — because both change. [pause] "
  "And remember, the goal isn't to own all fifty. It's to find the handful that fit your "
  "conviction, and understand them deeply."),

 ("recap", "nb_recap", {"dur": 0, "items": [
    "Beating the Nifty means looking different from the Nifty",
    "Fifty picks, filtered from 2,397 on real fundamentals",
    "Five tests: quality, growth, valuation, moat, investability",
    "Tier 1 core · Tier 2 growth · Tier 3 high-risk — sized accordingly",
    "Every figure is public, point-in-time, and yours to re-check",
    "This is analysis, not advice — do your own work"],
   "closer": "Find your conviction. Do the work. Beat the average."},
  "Let's bring it all together. [pause] Beating the Nifty means building a portfolio that "
  "looks different from it. [pause] We filtered two thousand four hundred companies down to "
  "fifty on real fundamentals, across five tests, sorted into three tiers of conviction "
  "and risk. [pause] Every figure is public and point-in-time — yours to verify. [pause] "
  "This was analysis, not advice. The work of turning it into a portfolio is yours. "
  "[pause] Find your conviction, do the work, and go beat the average. Thanks for watching."),
]

CHAPTERS = [
 {"id": "ch01", "segments": ch1},
 {"id": "ch02", "segments": ch2},
 {"id": "ch03", "segments": ch3},
 {"id": "ch04", "segments": ch4},
 {"id": "ch05", "segments": ch5},
]

if __name__ == "__main__":
    for ch in CHAPTERS:
        w = sum(len(s[3].replace("[pause]", " ").split()) for s in ch["segments"])
        print(f'{ch["id"]}: {len(ch["segments"])} segments, {w} words (~{w/155:.1f} min)')
    tot = sum(sum(len(s[3].replace("[pause]", " ").split()) for s in ch["segments"]) for ch in CHAPTERS)
    print(f"TOTAL ~{tot} words (~{tot/155:.0f} min)")
