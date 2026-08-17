#!/usr/bin/env python3
"""Intraday Trading: A Framework You Can Actually Follow — English course.
~15 min, 26 scenes, prefix `in`, Neerja Neural voice (en-IN-NeerjaNeural).
Companion to ta-course-en (Technical Analysis) — SAME Neerja voice for series
consistency. NO captions, NO music (repo defaults). Usage: python3 build.py

Budget: ~175 wpm effective (Neerja -4% + 0.55s pauses) → ~2,600 words ≈ 15 min.

════════════════════════════════════════════════════════════════════════════
VERIFIED NUMBERS TABLE  (skill 12 pre-render gate — re-verify before TTS)
Education video (§5): rule-sensitive facts verified against current sources
2026-07-25. This is general education — NOT platform-specific (per brief).
─────────────────────────────────────────────────────────────────────────────
FIGURE                                   VALUE            SOURCE
SEBI study: individual intraday          71% lost (FY23)  SEBI study Jul-2024, via
  traders in equity cash making loss                      Business Standard / Moneylife /
                                                          ThePrint (7-in-10; up from 65% FY19)
  - very frequent (>500 trades/yr)       80% lost         same SEBI study
  - traders under age 30                 76% lost         same SEBI study
Intraday leverage cap (equity MIS)       ~5x (20% margin) SEBI peak-margin regime;
  full VaR+ELM upfront; brokers can't    max              Bajaj Finserv / StockGro / HDFC Sky
  offer more than ~5x since peak margin
Equity intraday STT                      0.025% SELL only zerodha.com/charges; StockGro
Equity delivery STT (for contrast)       0.10% both sides zerodha.com/charges
Stamp duty (intraday)                    0.003% BUY only  zerodha.com/charges
Brokerage (representative)               ₹20 or 0.03%     zerodha.com/charges
  per executed order, whichever lower
GST                                      18% on brok+txn  zerodha.com/charges
Exchange txn charge (NSE, approx)        ~0.00297% turn.  zerodha.com/charges
Computed cost / round-trip (₹1L/side)    ≈ ₹82            computed in INScenes.tsx
Auto square-off time (MIS equity)        ~3:15–3:20 PM    5paisa / StockGro / Groww
NSE equity market hours                  9:15 AM–3:30 PM  NSE
─────────────────────────────────────────────────────────────────────────────
All computed examples (leverage 5x on ₹50k; 1% position sizing; R:R break-even
win-rate; per-trade cost; VWAP) are computed at module scope in INScenes.tsx.
Disclaimer present in narration (title + recap) AND must go in the description.
════════════════════════════════════════════════════════════════════════════
"""
import json, os, subprocess, time

VOICE = "en-IN-NeerjaNeural"; RATE = "-4%"; GAP = 0.5; PAUSE = 0.55; PREFIX = "in"
ROOT = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(ROOT, "..", ".."))
PUBLIC = os.path.join(REPO, "composer", "public", PREFIX)
RAW = os.path.join(ROOT, "assets", "raw")
FIN = os.path.join(ROOT, "assets")
QA_DIR = os.path.join(ROOT, "renders", "qa")
for d in (PUBLIC, RAW, os.path.join(ROOT, "artifacts"), os.path.join(ROOT, "renders"), QA_DIR):
    os.makedirs(d, exist_ok=True)

C = "#22D3EE"; G = "#34D399"; V = "#A78BFA"; Y = "#FBBF24"; R = "#FB7185"

SEGMENTS = [

 # ── TITLE ──────────────────────────────────────────────────────────────────
 ("s01_title", "in_title", {},
  "Intraday trading. Buy and sell the same stock, the same day. [pause] "
  "It looks simple, and it's heavily promoted online. "
  "But here's the truth up front: most people who try it lose money. [pause] "
  "This video is not a set of hot tips. It's one repeatable framework — "
  "what intraday really is, what it costs, and a step-by-step way to trade it with rules. [pause] "
  "Education only. Not investment advice. Please consult a SEBI-registered advisor."),

 # ── PART 1 ─────────────────────────────────────────────────────────────────
 ("s02_div1", "in_div",
  {"n": 1, "title": "What Intraday Really Is", "sub": "Mechanics · Costs · Leverage · The honest odds", "color": Y},
  "Part one. What intraday trading actually is — the mechanics, the costs, "
  "and the honest odds, before you risk a single rupee."),

 ("s03_hook", "in_hook", {},
  "Let's start with the number nobody wants to lead with. [pause] "
  "A SEBI study found that in the financial year twenty twenty-three, "
  "seventy-one percent of individual intraday traders in the cash market made a net loss. [pause] "
  "And it gets worse the more you trade. "
  "For very frequent traders — over five hundred trades a year — eighty percent lost money. "
  "Among traders under thirty, seventy-six percent lost. [pause] "
  "Read that again. The more they traded, the more they lost. [pause] "
  "I'm not showing you this to scare you off. "
  "I'm showing you because the other twenty-nine percent aren't luckier. "
  "They follow rules. This whole video is about being on that side."),

 ("s04_whatis", "in_whatis", {},
  "So what is intraday trading, exactly? [pause] "
  "You buy a stock and sell it within the same trading session. "
  "Nothing is carried to the next day. [pause] "
  "If you don't close a position yourself, your broker automatically squares it off — "
  "usually around three fifteen to three twenty in the afternoon. [pause] "
  "Watch the line. You enter after the open, and you're flat before the close. [pause] "
  "You are not investing in the company. You never plan to own it tomorrow. "
  "You're trying to profit from the price move within these few hours. "
  "That one constraint — a single day — changes everything about how you trade."),

 ("s05_vsdelivery", "in_vsdelivery", {},
  "How is this different from normal investing — from delivery? [pause] "
  "With delivery, you pay the full value of the shares and hold them for days, months, or years. "
  "With intraday, you post only a margin — a fraction of the value — and you must exit by close. [pause] "
  "Intraday carries no overnight risk: no nasty gap when bad news breaks after hours. [pause] "
  "The tax called STT is lower for intraday — zero point zero two five percent, on the sell side only. [pause] "
  "But the pace is relentless, minute by minute. "
  "Intraday isn't better or worse. It's faster, cheaper per trade, and far less forgiving."),

 ("s06_session", "in_session", {},
  "The trading day is not one flat block. It has a rhythm. [pause] "
  "From nine fifteen to about ten — the opening drive — you get the highest volume and volatility of the day. "
  "The day's trend is often set here. But so are the traps. [pause] "
  "Through the middle of the day, roughly eleven to two, volume dries up. "
  "Price goes choppy and range-bound. This is where most false signals live. [pause] "
  "Then from about two thirty to the close, volume returns. "
  "Trends resume or reverse as everyone squares off. [pause] "
  "The lesson: trade the open and the close. "
  "Respect the mid-day chop — it drains accounts quietly."),

 ("s07_leverage", "in_leverage", {},
  "Now, leverage — the feature that attracts people, and the one that ruins them. [pause] "
  "With intraday margin, your broker lets you control more than your cash. "
  "Say you have fifty thousand rupees. At five times leverage, "
  "you can take a position worth two and a half lakh. [pause] "
  "Here's the catch. If price moves two percent your way, "
  "you make five thousand — ten percent of your capital. Wonderful. [pause] "
  "But if it moves two percent against you, you lose five thousand — the same ten percent. "
  "A tiny move becomes a big swing on your money. [pause] "
  "This is exactly why SEBI now caps intraday leverage near five times. "
  "Bigger leverage was wiping beginners out."),

 ("s08_costs", "in_costs", {},
  "Every trade also starts in a small hole — because of costs. [pause] "
  "Take one round trip on one lakh of turnover. "
  "Brokerage, around forty rupees. STT, twenty-five. "
  "Exchange charges, a few rupees. Stamp duty, three. Then eighteen percent GST on top. [pause] "
  "Add it up: roughly eighty-two rupees, just to enter and exit once. "
  "Price has to move that much before you make a single rupee of profit. [pause] "
  "Now trade five times a day. That's about ninety-eight thousand rupees a year — in costs alone. [pause] "
  "This is why overtrading is deadly. It bleeds you through costs, "
  "and forced trades are usually bad trades. Fewer, better setups win."),

 ("s09_edge", "in_edge", {},
  "So why do most lose? It's rarely the market. It's the method. [pause] "
  "They trade with no edge — on tips, news, and gut feeling. "
  "They trade with no stop-loss, so small losses become account-enders. "
  "They over-leverage, so one bad trade does outsized damage. "
  "And they overtrade and revenge-trade, letting costs and emotion compound. [pause] "
  "Here's the good news. Every one of those is a rules problem, not a talent problem. [pause] "
  "The rest of this video is one framework with five parts: "
  "a bias, a level, a trigger, a stop, and a size. "
  "Discipline is the edge."),

 # ── PART 2 ─────────────────────────────────────────────────────────────────
 ("s10_div2", "in_div",
  {"n": 2, "title": "The Framework", "sub": "Bias · Levels · VWAP · Setups · Stops · Sizing · Psychology", "color": C},
  "Part two. The framework — a repeatable way to find, enter, and manage an intraday trade. "
  "These are the tips that actually matter."),

 ("s11_bias", "in_bias", {},
  "Tip one. Trade with the trend. [pause] "
  "Work top-down. Start on the daily chart and ask one question: "
  "which way is this stock trending? That's your bias. [pause] "
  "Then drop to the fifteen-minute chart for today's structure — where the key areas are. [pause] "
  "Finally, the five-minute chart, only for your entry — "
  "and only in the same direction as your bias. [pause] "
  "From our technical analysis video, the rule holds here too: never fight the higher timeframe. "
  "Take longs in an uptrend, shorts in a downtrend. "
  "Trading against the bigger trend is one of the most expensive beginner mistakes."),

 ("s12_levels", "in_levels", {},
  "Tip two. Mark your levels before the market opens. [pause] "
  "Good trades happen at levels, not in empty space. "
  "So decide in advance where you actually care. [pause] "
  "Mark yesterday's high and yesterday's low — the previous-day high and low. "
  "Price reacts strongly at both. [pause] "
  "Then, once the first fifteen minutes are done, mark the opening range — "
  "the high and low of that early window. [pause] "
  "Now you have a map. When price approaches one of these lines, you pay attention. "
  "When it's in no-man's-land, you wait. "
  "The map keeps you out of random, low-quality trades."),

 ("s13_vwap", "in_vwap", {},
  "Tip three. Use VWAP — the volume-weighted average price. [pause] "
  "It's the average price of the day, weighted by how much volume traded at each price. "
  "It's the one line big institutions watch, so it matters. [pause] "
  "The rule is simple. When price is above VWAP, the intraday bias is up — favour longs. "
  "When price is below VWAP, favour shorts. [pause] "
  "And VWAP often acts as support or resistance. "
  "A pullback to VWAP, in the direction of your trend, "
  "is one of the cleanest entries you'll find. [pause] "
  "Above the line, look to buy dips. Below it, look to sell rallies."),

 ("s14_orb", "in_orb", {},
  "Tip four. Wait for a setup — don't invent one. [pause] "
  "Here's a classic, beginner-friendly setup: the opening range breakout. [pause] "
  "Let the first fifteen minutes play out. "
  "The high and low of that window is your opening range — the box on screen. "
  "Do not guess which way it breaks. [pause] "
  "Then wait. When price closes decisively above the box, that's your long trigger. "
  "Below the box, a short. [pause] "
  "The power of a setup is that it's a rule, not a feeling. "
  "You know your entry before it happens — so you react to a plan, not to fear or excitement."),

 ("s15_pullback", "in_pullback", {},
  "Tip five. Don't chase. Wait for the retest. [pause] "
  "When a stock rips straight up, every instinct screams to jump in. "
  "Look at the left chart — buy that vertical spike, and you often buy the exact top. "
  "It fades, and you're in the red. [pause] "
  "On the right, the patient version. Price breaks out, "
  "then pulls back to retest the breakout level — and only then do you enter. [pause] "
  "The retest gives you two gifts: a better price, and a tight, logical stop just below. [pause] "
  "A breakout you missed is not a trade you must take. The best entries feel a little boring."),

 ("s16_volume", "in_volume", {},
  "Tip six. Make volume confirm the move. [pause] "
  "Volume is the number of shares changing hands. It's the one thing that can't be faked. [pause] "
  "Look at the breakout candle — it rides a clear spike in volume. "
  "That tells you real buyers showed up, and the move has fuel. [pause] "
  "Now the warning: a breakout on thin, shrinking volume is the classic trap. "
  "Price pops above a level, nobody follows, and it snaps right back. [pause] "
  "So the rule: big move plus big volume — trust it. "
  "Big move with no volume — be very suspicious."),

 ("s17_stop", "in_stop", {},
  "Tip seven. The stop-loss is non-negotiable. [pause] "
  "Before you enter, you decide the price at which you're wrong — "
  "and you commit to exiting there. [pause] "
  "Say you enter at two hundred and two, with a stop at one ninety-nine. "
  "If it goes wrong, you exit for a three-rupee loss. Small. Planned. Survivable. "
  "You live to trade the next setup. [pause] "
  "Now the alternative — no stop, just hope. It'll come back, you tell yourself. "
  "Price slides from two-oh-two down to one seventy-eight — a twenty-four-rupee loss. [pause] "
  "One trade like that undoes ten good ones. "
  "A stop-loss is the difference between a bad day and a blown-up account. "
  "Set it. Then honour it."),

 ("s18_rr", "in_rr", {},
  "Tip eight. Demand a good risk-to-reward ratio. [pause] "
  "For every trade, compare what you're risking to what you can make. "
  "Entry at five hundred, stop at four ninety-six — that's four rupees of risk. Call it one R. [pause] "
  "If your target is five-oh-eight, that's eight rupees — two R. A one-to-two risk-reward. [pause] "
  "Here's why that's powerful. At one-to-two, "
  "you only need to win about thirty-three percent of the time to break even. [pause] "
  "You can be wrong two out of every three trades and still make money — "
  "because your winners are twice your losers. [pause] "
  "Refuse any setup that doesn't offer at least two-to-one."),

 ("s19_sizing", "in_sizing", {},
  "Tip nine. Size your position by risk — not by greed. [pause] "
  "Most beginners ask, how many shares can I afford? Wrong question. "
  "Ask instead: how much am I willing to lose if I'm wrong? [pause] "
  "Here's the one-percent rule. Say your capital is one lakh. "
  "One percent is one thousand rupees — the most you'll lose on this trade. [pause] "
  "Your entry is two hundred, your stop is one ninety-six — four rupees of risk per share. [pause] "
  "So: one thousand divided by four equals two hundred and fifty shares. "
  "A fifty-thousand-rupee position. [pause] "
  "Your stop decides your size, never the other way around. "
  "At one percent risk, it would take a hundred losses in a row to blow up. "
  "That's how you survive long enough to win."),

 ("s20_timeofday", "in_timeofday", {},
  "Tip ten. Trade the right hours. When you trade matters as much as what. [pause] "
  "The prime windows are the opening — nine fifteen to ten — "
  "and the close — two thirty to three thirty. "
  "Volume, momentum, cleaner moves. [pause] "
  "The hours around them are okay, but be selective. [pause] "
  "The mid-day stretch, roughly eleven to two, is the danger zone: "
  "low volume, choppy, full of whipsaws. Avoid it. [pause] "
  "And a tip for beginners — skip the first five minutes too. "
  "The opening auction is wild. Let a little structure form first."),

 ("s21_psych", "in_psych", {},
  "Tip eleven. Master yourself. Your biggest opponent is in the mirror. [pause] "
  "After a loss, the urge is to win it back immediately — revenge trading. "
  "Don't. Step away. [pause] "
  "When you miss a move, FOMO says jump in late. "
  "Don't — there's always another setup. [pause] "
  "Overtrading feels productive but isn't: three good trades beat thirty forced ones. "
  "Quality over activity. [pause] "
  "And review everything. Journal every trade — your entry, your reason, your exit. "
  "Your mistakes become your syllabus. [pause] "
  "Rules only work if you follow them on a bad day. "
  "Discipline under pressure is the entire game."),

 ("s22_mistakes", "in_mistakes", {},
  "Before we put it all together, a quick montage of the fastest ways to lose. [pause] "
  "Averaging into a losing position — adding good money to a bad trade. "
  "Moving or deleting your stop-loss when it's about to hit. [pause] "
  "Trading on tips and TV noise. Using maximum leverage on every single trade. "
  "Entering with no plan, purely on a hunch. And trading all day, every day. [pause] "
  "Notice the pattern. Every one of these is breaking a rule you already know. "
  "Losing, most of the time, is self-inflicted."),

 # ── PART 3 ─────────────────────────────────────────────────────────────────
 ("s23_div3", "in_div",
  {"n": 3, "title": "Putting It Together", "sub": "One clean trade · The pre-trade checklist", "color": G},
  "Part three. Putting it all together — one clean trade from start to finish, "
  "and the checklist to run before every single one."),

 ("s24_walkthrough", "in_walkthrough", {},
  "Let's trade one setup, end to end, using the framework. [pause] "
  "Step one, the bias: the trend is up and price is holding above VWAP. We only look for longs. [pause] "
  "Step two, the trigger: price consolidates, then breaks the range with a clear volume spike. "
  "We enter at two hundred and two. [pause] "
  "Step three, the stop: just below the range, at one ninety-eight. "
  "That's four rupees of risk — one R. [pause] "
  "Step four, the target: two R away, at two hundred and ten. "
  "Price runs, hits it, and we book the trade. [pause] "
  "We risked four rupees to make eight. Planned before entry. Repeatable. "
  "A little boring. That's exactly the point."),

 ("s25_checklist", "in_checklist",
  {"items": [
   "Bias: am I trading WITH the trend, and is price on the right side of VWAP?",
   "Level: what exact level is this trade based on — breakout, retest, or S/R?",
   "Volume: is it confirming the move, or is it suspiciously thin?",
   "Stop: is it at a level that proves me wrong — not a random number?",
   "Reward: is my target at least twice my risk (2R minimum)?",
   "Size: does a stop-out cost at most 1% of my capital?",
   "Timing: is it a prime hour — not the dead mid-day chop?",
   "Mindset: am I calm and following my plan — not chasing or bored?",
  ]},
  "Here's the ritual to run before you click buy — sixty seconds, every time. [pause] "
  "What's my bias, and is price on the right side of VWAP? "
  "What exact level is this trade based on? Is volume confirming? [pause] "
  "Where's my stop — at a level that proves me wrong? "
  "Is my reward at least twice my risk? Is my size within the one-percent rule? [pause] "
  "Is it a prime hour, and am I calm — not chasing or bored? [pause] "
  "If you can't tick every box, it isn't a trade. It's a gamble. "
  "The best traders skip more setups than they take."),

 # ── RECAP ──────────────────────────────────────────────────────────────────
 ("s26_recap", "in_recap",
  {"items": [
   "Intraday = open AND close the same day; you're flat by 3:30, no overnight risk",
   "Leverage (~5× max) and low per-trade cost cut BOTH ways — respect them",
   "Trade WITH the higher-timeframe trend; use VWAP as your intraday anchor",
   "Mark levels before the open: previous-day high/low and the opening range",
   "Wait for a setup — breakout or retest — confirmed by volume. Don't chase",
   "Every trade: stop-loss first, target at 2R minimum, size by the 1% rule",
   "Trade prime hours; avoid the mid-day chop and the first 5 minutes",
   "Discipline beats prediction — 71% lose by breaking rules they already know",
  ],
   "closer": "You can't control the market — only your risk, your rules, and your patience. Master those, and you're ahead of most."},
  "Let's bring it all together in one breath. [pause] "
  "Intraday means you open and close the same day — flat by three thirty, no overnight risk. [pause] "
  "Leverage and low per-trade costs cut both ways, so respect them. "
  "Trade with the higher-timeframe trend, and use VWAP as your anchor. [pause] "
  "Mark your levels before the open — previous-day high and low, and the opening range. "
  "Wait for a setup — a breakout or a retest — confirmed by volume. Don't chase. [pause] "
  "On every trade: stop-loss first, target at two R minimum, then size by the one-percent rule. "
  "Trade prime hours, avoid the mid-day chop. [pause] "
  "And remember why seventy-one percent lose — they break rules they already know. "
  "You can't control the market. Only your risk, your rules, and your patience. "
  "Master those, and you're already ahead of most. [pause] "
  "Education only, not investment advice. Consult a SEBI-registered advisor. Thanks for watching."),
]

# ──────────────────────────── TTS engine (edge-tts, from ta-course-en)
def ffdur(path):
    out = subprocess.run(
        ["ffprobe","-v","error","-show_entries","format=duration",
         "-of","default=noprint_wrappers=1:nokey=1",path],
        capture_output=True, text=True, check=True)
    return round(float(out.stdout.strip()), 3)

def tts_chunk(path, text):
    mp3 = path[:-4] + ".mp3"
    for attempt in range(6):
        r = subprocess.run(
            ["edge-tts","--voice",VOICE,f"--rate={RATE}","--text",text,"--write-media",mp3],
            capture_output=True)
        if r.returncode == 0 and os.path.exists(mp3) and os.path.getsize(mp3) > 0:
            break
        time.sleep(3 + attempt * 4)
    else:
        raise RuntimeError(f"tts failed after 6 attempts: {path}")
    subprocess.run(["ffmpeg","-y","-i",mp3,"-ar","24000","-ac","1",path],
                   check=True, capture_output=True)
    os.remove(mp3)

def gen_one(seg_id, text):
    fin = os.path.join(FIN, seg_id + ".wav")
    if os.path.exists(fin):
        return fin, ffdur(fin)
    chunks = [c.strip() for c in text.split("[pause]") if c.strip()]
    paths = []
    for ci, chunk in enumerate(chunks):
        cp = os.path.join(RAW, f"{seg_id}_c{ci}.wav")
        if not os.path.exists(cp):
            tts_chunk(cp, chunk)
        paths.append(cp)
    psil = os.path.join(RAW, "_pause.wav")
    if not os.path.exists(psil):
        subprocess.run(["ffmpeg","-y","-f","lavfi","-i","anullsrc=r=24000:cl=mono",
                        "-t",str(PAUSE), psil], check=True, capture_output=True)
    clist = os.path.join(RAW, f"{seg_id}_concat.txt")
    with open(clist, "w") as f:
        for i2, p2 in enumerate(paths):
            f.write(f"file '{p2}'\n")
            if i2 < len(paths) - 1:
                f.write(f"file '{psil}'\n")
    subprocess.run(["ffmpeg","-y","-f","concat","-safe","0","-i",clist,"-c","copy",fin],
                   check=True, capture_output=True)
    return fin, ffdur(fin)

# ──────────────────────────── main build
manifest = []
for sid, variant, props, text in SEGMENTS:
    path, dur = gen_one(sid, text)
    manifest.append({"id": sid, "variant": variant, "props": props, "wav": path, "duration": dur})
    print(f"  {sid:18s} {dur:6.2f}s", flush=True)

silence = os.path.join(FIN, "_sil.wav")
subprocess.run(["ffmpeg","-y","-f","lavfi","-i","anullsrc=r=24000:cl=mono","-t",str(GAP),silence],
               check=True, capture_output=True)

concat_list = os.path.join(ROOT, "concat_in.txt")
with open(concat_list, "w") as f:
    for i, m in enumerate(manifest):
        f.write(f"file '{m['wav']}'\n")
        if i < len(manifest) - 1:
            f.write(f"file '{silence}'\n")

subprocess.run(["ffmpeg","-y","-f","concat","-safe","0","-i",concat_list,"-c","copy",
                os.path.join(PUBLIC, "narration.wav")], check=True, capture_output=True)

cuts, t = [], 0.0
for m in manifest:
    start, end = t, t + m["duration"]
    cuts.append({
        "id": m["id"], "type": m["variant"],
        "in_seconds": round(start, 3), "out_seconds": round(end, 3),
        "props": {**m["props"], "dur": round(m["duration"] + GAP, 3)},
    })
    t = end + GAP

props_out = {
    "cuts": cuts,
    "audio": {"narration": {"src": f"{PREFIX}/narration.wav", "volume": 1.0}},
}
json.dump(props_out, open(os.path.join(ROOT, "artifacts", "edit_decisions.json"), "w"), indent=2)
total = t - GAP
words = sum(len(text.replace("[pause]", " ").split()) for _, _, _, text in SEGMENTS)
print(f"\ntotal {total:.2f}s ({total/60:.2f} min) · {len(cuts)} scenes · {words} words · NO captions · NO music")
print("Next: QA stills for every scene, LOOK at each, fix, then final render.")
