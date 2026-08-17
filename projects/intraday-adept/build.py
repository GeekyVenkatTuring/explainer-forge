#!/usr/bin/env python3
"""Intraday Trading, From First Principles — ADEPT + Feynman edition.
~20 min, 26 scenes, prefix `ia`, Prabhat Neural voice (en-IN-PrabhatNeural).

A recreation of projects/intraday-en taught through two learning frameworks,
applied UNDER THE HOOD (no on-screen method labels):
  ADEPT   — every concept flows Analogy → Diagram → Example → Plain-English →
            Technical-term-LAST.
  Feynman — explain as if to a smart 12-year-old: short sentences, everyday
            words, lead with intuition, name the jargon only after it's felt.

Every teaching beat OPENS with the everyday analogy (spoken first — reveals are
front-loaded to match), then the diagram builds, then the worked numbers, then a
plain-English restatement, and only then the technical term. Usage: python3 build.py

Budget: Prabhat +6% ≈ 144 wpm raw; with [pause] (0.55s) + 0.5s gaps ≈ 130 effective
→ ~2,700 words ≈ 20 min. build.py prints the real total — iterate to ±5%.

════════════════════════════════════════════════════════════════════════════
VERIFIED NUMBERS TABLE  (skill 12 gate — figures PORTED from the verified
projects/intraday-en build; general education, not platform-specific)
─────────────────────────────────────────────────────────────────────────────
SEBI study: 71% of individual intraday traders lost (FY23); 80% of very-frequent
  (>500 trades/yr); 76% of under-30s.  SEBI study Jul-2024.
Intraday leverage cap (equity MIS) ~5x (20% margin) — SEBI peak-margin regime.
Equity intraday STT 0.025% sell-only; delivery 0.10% both sides.
Stamp duty 0.003% buy; brokerage ₹20 or 0.03%/order; GST 18% on brok+txn.
Computed cost / round-trip (₹1L/side) ≈ ₹82; ≈ ₹98k/yr at 5 trades/day.
Auto square-off ~3:15–3:20 PM; NSE hours 9:15 AM–3:30 PM.
All computed examples (5x on ₹50k; 1% sizing; R:R break-even; per-trade cost;
VWAP) are recomputed at module scope in IAScenes.tsx — never redrawn.
Disclaimer present in narration (title + recap) AND must go in the description.
════════════════════════════════════════════════════════════════════════════
"""
import json, os, subprocess, time

VOICE = "en-IN-PrabhatNeural"; RATE = "+6%"; GAP = 0.5; PAUSE = 0.55; PREFIX = "ia"
ROOT = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(ROOT, "..", ".."))
PUBLIC = os.path.join(REPO, "composer", "public", PREFIX)
RAW = os.path.join(ROOT, "assets", "raw")
FIN = os.path.join(ROOT, "assets")
QA_DIR = os.path.join(ROOT, "renders", "qa")
for d in (PUBLIC, RAW, os.path.join(ROOT, "artifacts"), os.path.join(ROOT, "renders"), QA_DIR):
    os.makedirs(d, exist_ok=True)

# divider colours (match IAScenes accents): C sky, G green, Y amber
C = "#38BDF8"; G = "#43D9A3"; Y = "#F6A723"

SEGMENTS = [

 # ── TITLE ──────────────────────────────────────────────────────────────────
 ("s01_title", "ia_title", {},
  "A promise before we start. Every idea here, I'll explain with something you already know — "
  "a rented bike, a toll booth, a seatbelt. [pause] "
  "The topic is intraday trading — buying and selling a stock the same day. [pause] "
  "It looks easy, but most who try it lose money. [pause] "
  "So instead of hot tips, here's one method, built from the ground up. [pause] "
  "Education only, not advice. Please consult a SEBI-registered advisor."),

 # ── PART 1 ─────────────────────────────────────────────────────────────────
 ("s02_div1", "ia_div",
  {"n": 1, "title": "What Intraday Really Is", "sub": "Mechanics · Costs · Leverage · The honest odds", "color": Y},
  "Part one. What intraday trading actually is — the mechanics, the costs, "
  "and the honest odds, before you risk a single rupee."),

 ("s03_hook", "ia_hook", {},
  "Let's start with the number nobody likes to lead with. [pause] "
  "Picture a casino. The longer you sit at the table, the more the odds grind you down. "
  "Intraday looks a lot like that. [pause] "
  "A SEBI study found that in the year twenty twenty-three, "
  "seventy-one percent of individual intraday traders lost money. Seven in ten. [pause] "
  "And it gets worse the more you play. "
  "Trade over five hundred times a year, and eighty percent lost. "
  "Under thirty years old, seventy-six percent lost. [pause] "
  "Read that again. The more they traded, the more they lost. [pause] "
  "I'm not showing you this to scare you off. The other twenty-nine percent aren't luckier. "
  "They follow rules. This whole video is about joining them."),

 ("s04_whatis", "ia_whatis", {},
  "So what is intraday, exactly? [pause] "
  "Think of a rented bike. You take it out in the morning, ride it all day, "
  "and you must return it by evening. You never own it. [pause] "
  "Intraday is the same. You buy a stock after the open, and you sell it before the close. "
  "Nothing is carried to tomorrow. [pause] "
  "Watch the line — you enter, and you're flat again before the day ends. [pause] "
  "Forget to close it yourself? Your broker returns the bike for you — "
  "it auto-closes your trade near three fifteen. That forced exit has a name: the square-off. [pause] "
  "You're not investing in the company. You're renting the day's price move. "
  "That one rule — a single day — changes everything about how you trade."),

 ("s05_vsdelivery", "ia_vsdelivery", {},
  "How is this different from normal investing? [pause] "
  "Think of renting a home versus buying one. [pause] "
  "When you buy — that's called delivery — you pay the full price and can hold for years. "
  "When you rent — that's intraday — you put down only a deposit, and you must be out by the deadline. [pause] "
  "Renting for a day has one nice perk: no overnight risk. "
  "You're gone before any bad news hits after hours. [pause] "
  "The sell tax, called STT, is also lower — zero point zero two five percent, on the sell side only. [pause] "
  "But renting is relentless — the clock never stops. "
  "Intraday isn't better than investing. It's faster, cheaper per go, and far less forgiving."),

 ("s06_session", "ia_session", {},
  "The trading day isn't one flat block. It has rush hours, just like a city's roads. [pause] "
  "From nine fifteen to about ten — the morning rush — you get the heaviest traffic: "
  "the most volume and the biggest moves. The day's direction is often set here. [pause] "
  "Through the middle of the day, roughly eleven to two, the roads empty out. "
  "Price goes quiet and choppy. This is where most false signals live. [pause] "
  "Then near the close, from about two thirty, traffic returns for the evening rush, "
  "as everyone heads home and squares off. [pause] "
  "The lesson is simple. Trade the rush hours. Respect the mid-day lull — it drains accounts quietly."),

 ("s07_leverage", "ia_leverage", {},
  "Now leverage — the feature that pulls people in, and the one that ruins them. [pause] "
  "Think of a magnifying glass. It makes a tiny thing look huge. "
  "Leverage does that to price moves. [pause] "
  "Say you have fifty thousand rupees. At five times leverage, "
  "you control a position worth two and a half lakh. [pause] "
  "Here's the catch. If price moves two percent your way, "
  "you make five thousand — ten percent of your money. Wonderful. [pause] "
  "But if it moves two percent against you, you lose five thousand — the same ten percent. "
  "A tiny move becomes a big swing on your cash. [pause] "
  "A magnifying glass can start a fire. That's exactly why SEBI now caps intraday leverage "
  "near five times — bigger was wiping beginners out."),

 ("s08_costs", "ia_costs", {},
  "Every trade also starts in a small hole, because of costs. [pause] "
  "Think of a toll booth. Every trip, you pay — no matter what. [pause] "
  "Take one round trip on one lakh of turnover. Brokerage, about forty rupees. "
  "The sell tax, twenty-five. Exchange fees, a few rupees. Stamp duty, three. "
  "Then eighteen percent GST on top. [pause] "
  "Add it up: roughly eighty-two rupees, just to get in and out once. "
  "Price must move that far before you earn a single rupee. [pause] "
  "Now take five trips a day. That's about ninety-eight thousand rupees a year — in tolls alone. [pause] "
  "This is why over-trading is deadly. It bleeds you through costs, "
  "and forced trades are usually bad trades. Fewer, better setups win."),

 ("s09_edge", "ia_edge", {},
  "So why do most lose? It's rarely the market. It's the method. [pause] "
  "Think of a pilot. In fog, they trust the instruments, not a gut feeling. "
  "Losing traders fly on gut. [pause] "
  "They trade with no edge — just tips, news, and hope. "
  "They trade with no stop, so a small loss becomes an account-ender. "
  "They use too much leverage, so one bad trade does huge damage. "
  "And they over-trade, letting costs and emotion pile up. [pause] "
  "Here's the good news. Every one of those is a rules problem, not a talent problem. [pause] "
  "The rest of this video is one recipe with five parts: "
  "a bias, a level, a trigger, a stop, and a size. Discipline is the edge."),

 # ── PART 2 ─────────────────────────────────────────────────────────────────
 ("s10_div2", "ia_div",
  {"n": 2, "title": "The Framework", "sub": "Bias · Levels · VWAP · Setups · Stops · Sizing · Psychology", "color": C},
  "Part two. The framework — a repeatable way to find, enter, and manage a trade. "
  "These are the tips that actually matter."),

 ("s11_bias", "ia_bias", {},
  "Tip one. Trade with the trend. [pause] "
  "Think of a river. Swim with the current and it carries you. "
  "Fight it, and you exhaust yourself. The trend is your current. [pause] "
  "So work top-down. Start on the daily chart and ask one thing: "
  "which way is this stock flowing? That's your bias. [pause] "
  "Then drop to the fifteen-minute chart to see today's structure. [pause] "
  "Finally, the five-minute chart — but only for your entry, "
  "and only in the same direction as the river. [pause] "
  "From our technical analysis video, the rule holds: never fight the higher timeframe. "
  "Longs in an uptrend, shorts in a downtrend. Swimming upstream is one of the most expensive beginner mistakes."),

 ("s12_levels", "ia_levels", {},
  "Tip two. Mark your levels before the market opens. [pause] "
  "Think of a bouncing ball in a room. It reacts at the floor and at the ceiling — "
  "not in empty air. Price is the same. [pause] "
  "So decide your floors and ceilings in advance. "
  "Mark yesterday's high and yesterday's low — price reacts strongly at both. [pause] "
  "Then, once the first fifteen minutes are done, mark that early high and low too — "
  "the opening range. [pause] "
  "Now you have a map. When price nears one of these lines, you pay attention. "
  "When it's floating in the middle, you wait. [pause] "
  "The map keeps you out of random, low-quality trades."),

 ("s13_vwap", "ia_vwap", {},
  "Tip three. Use VWAP. [pause] "
  "Think of the water level in a tank. Things float around it, and the water keeps pulling them back. "
  "VWAP is the day's water level for price. [pause] "
  "Technically, it's the average price of the day, weighted by how much volume traded at each price. "
  "It's the one line big institutions watch. [pause] "
  "The rule is simple. When price is above the water line, the day leans up — favour buying. "
  "Below the line, it leans down — favour selling. [pause] "
  "And price keeps floating back to the line. "
  "A pullback to VWAP, in the direction of your trend, is one of the cleanest entries you'll find. [pause] "
  "Above the line, buy dips. Below it, sell rallies."),

 ("s14_orb", "ia_orb", {},
  "Tip four. Wait for a setup — don't invent one. [pause] "
  "Think of a horse in the starting gate. You don't bet before the gate opens. "
  "You wait for the horse to break out and run. [pause] "
  "Here's the beginner-friendly version: the opening range breakout. [pause] "
  "Let the first fifteen minutes play out. The high and low of that window is the gate — "
  "the box on screen. Don't guess which way it breaks. [pause] "
  "Then wait. When price closes firmly above the box, that's your signal to go long. "
  "Below it, a short. [pause] "
  "The power of a setup is that it's a rule, not a feeling. "
  "You know your entry before it happens — so you follow a plan, not fear."),

 ("s15_pullback", "ia_pullback", {},
  "Tip five. Don't chase. Wait for the retest. [pause] "
  "Think of a bus pulling away. Sprint after it and you're gasping in the road. "
  "Wait calmly at the next stop, and it comes to you. [pause] "
  "When a stock rips straight up, every instinct says jump in. "
  "Look at the left chart — buy that vertical spike, and you often buy the exact top. "
  "It fades, and you're in the red. [pause] "
  "On the right, the patient version. Price breaks out, "
  "then pulls back to retest the level — and only then do you enter. [pause] "
  "The retest gives you two gifts: a better price, and a tight stop just below. [pause] "
  "A bus you missed is not a bus you must chase. The best entries feel a little boring."),

 ("s16_volume", "ia_volume", {},
  "Tip six. Make volume confirm the move. [pause] "
  "Think of a stadium. When a real goal goes in, the crowd roars. A fake cheer fools no one. [pause] "
  "Volume is the number of shares changing hands — the crowd's roar. "
  "It's the one thing that can't be faked. [pause] "
  "Look at the breakout candle. It rides a clear spike in volume — "
  "real buyers showed up, and the move has fuel. [pause] "
  "Now the warning. A breakout in silence, on thin volume, is the classic trap. "
  "Price pops above a level, nobody follows, and it snaps right back. [pause] "
  "So the rule: big move plus a big roar — trust it. Big move in silence — be very suspicious."),

 ("s17_stop", "ia_stop", {},
  "Tip seven. The stop-loss is non-negotiable. [pause] "
  "Think of a seatbelt. You buckle it before you drive — not during the crash. [pause] "
  "Before you enter, you decide the price at which you're wrong, "
  "and you commit to leaving there. [pause] "
  "Say you enter at two hundred and two, with a stop at one ninety-nine. "
  "If it goes wrong, you're out for a three-rupee loss. Small. Planned. Survivable. "
  "You live to trade again. [pause] "
  "Now the alternative — no belt, just hope. It'll come back, you tell yourself. "
  "Price slides all the way to one seventy-eight — a twenty-four-rupee loss. [pause] "
  "One trade like that undoes ten good ones. "
  "A stop-loss is the difference between a bad day and a blown-up account. Set it. Then honour it."),

 ("s18_rr", "ia_rr", {},
  "Tip eight. Demand a good payoff. [pause] "
  "Think of a bet where you risk one rupee to make two. "
  "Even if you're wrong often, the math protects you. [pause] "
  "For every trade, compare what you risk to what you can make. "
  "Enter at five hundred, stop at four ninety-six — that's four rupees of risk. Call it one R. [pause] "
  "If your target is five-oh-eight, that's eight rupees — two R. A one-to-two payoff. [pause] "
  "Here's why it's powerful. At one-to-two, "
  "you only need to win about a third of the time just to break even. [pause] "
  "You can be wrong two out of every three trades and still make money — "
  "because your winners are twice your losers. That ratio is called risk-to-reward. "
  "Refuse anything below two-to-one."),

 ("s19_sizing", "ia_sizing", {},
  "Tip nine. Size by risk, not by greed. [pause] "
  "Think of a poker player. A good one never bets the whole bankroll on one hand. [pause] "
  "Most beginners ask, how many shares can I afford? Wrong question. "
  "Ask instead: how much am I willing to lose if I'm wrong? [pause] "
  "Here's the rule: risk one percent per trade. Say your bankroll is one lakh. "
  "One percent is one thousand rupees — the most you'll lose on this trade. [pause] "
  "Your entry is two hundred, your stop one ninety-six — four rupees of risk per share. [pause] "
  "So: one thousand divided by four is two hundred and fifty shares. "
  "Your stop decides your size — never the other way around. [pause] "
  "At one percent a hand, it takes a hundred losses in a row to bust. "
  "That's how you survive long enough to win."),

 ("s20_timeofday", "ia_timeofday", {},
  "Tip ten. Trade the right hours. [pause] "
  "Think of fishing. You go at dawn and dusk, when the fish are biting — not under the noon sun. [pause] "
  "The prime windows are the open — nine fifteen to ten — "
  "and the close — two thirty to three thirty. Volume, momentum, cleaner moves. [pause] "
  "The hours around them are okay, but be selective. [pause] "
  "The mid-day stretch, roughly eleven to two, is dead water — "
  "low volume, choppy, full of whipsaws. Avoid it. [pause] "
  "And one tip for beginners: skip the first five minutes too. "
  "The opening auction is wild. Let a little structure form first."),

 ("s21_psych", "ia_psych", {},
  "Tip eleven. Master yourself. [pause] "
  "Poker players have a word — tilt. It's when emotion takes the wheel and you throw money away. "
  "Your toughest opponent is the one in the mirror. [pause] "
  "After a loss, the urge is to win it back right now — revenge trading. Don't. Step away. [pause] "
  "When you miss a move, FOMO says jump in late. Don't — there's always another setup. [pause] "
  "Over-trading feels productive but isn't: three good trades beat thirty forced ones. [pause] "
  "And review everything. Journal every trade — your entry, your reason, your exit. "
  "Your mistakes become your syllabus. [pause] "
  "Rules only work if you follow them on a bad day. Discipline under pressure is the whole game."),

 ("s22_mistakes", "ia_mistakes", {},
  "Before we put it together, a quick tour of the fastest ways to lose. [pause] "
  "These are potholes you can see coming — and still step in. [pause] "
  "Averaging into a loser — throwing good money after bad. "
  "Moving your stop when it's about to hit. [pause] "
  "Trading on tips and TV noise. Using maximum leverage on every trade. "
  "Entering with no plan, on a hunch. And trading all day, every day. [pause] "
  "Notice the pattern. Every one is a rule you already know, broken. "
  "Losing, most of the time, is self-inflicted."),

 # ── PART 3 ─────────────────────────────────────────────────────────────────
 ("s23_div3", "ia_div",
  {"n": 3, "title": "Putting It Together", "sub": "One clean trade · The pre-trade checklist", "color": G},
  "Part three. Putting it all together — one clean trade from start to finish, "
  "and the checklist to run before every single one."),

 ("s24_walkthrough", "ia_walkthrough", {},
  "Let's trade one setup, end to end, like assembling a puzzle. "
  "Each piece we've learned clicks into place. [pause] "
  "Piece one, the bias: the trend is up and price is above the water line. We only look to buy. [pause] "
  "Piece two, the trigger: price coils, then breaks the gate with a clear roar of volume. "
  "We enter at two hundred and two. [pause] "
  "Piece three, the seatbelt: a stop just below the range, at one ninety-eight. "
  "That's four rupees of risk — one R. [pause] "
  "Piece four, the target: two R away, at two hundred and ten. "
  "Price runs, hits it, and we book the trade. [pause] "
  "We risked four rupees to make eight. Planned before entry. Repeatable. "
  "A little boring — that's exactly the point."),

 ("s25_checklist", "ia_checklist",
  {"items": [
   "Bias: am I swimming WITH the trend, and on the right side of VWAP?",
   "Level: what floor or ceiling is this trade based on — breakout, retest, or S/R?",
   "Volume: is the crowd roaring, or is it suspiciously quiet?",
   "Seatbelt: is my stop at a level that proves me wrong — not a random number?",
   "Payoff: is my target at least twice my risk (2R minimum)?",
   "Size: does a stop-out cost at most 1% of my bankroll?",
   "Timing: are the fish biting — a prime hour, not the dead mid-day?",
   "Mindset: am I calm and on plan — not on tilt, chasing or bored?",
  ]},
  "Here's the ritual to run before you click buy — a pilot's pre-flight check, sixty seconds, every time. [pause] "
  "What's my bias, and is price on the right side of the water line? "
  "What exact level is this trade based on? Is volume confirming — is the crowd roaring? [pause] "
  "Where's my seatbelt — at a level that proves me wrong? "
  "Is my reward at least twice my risk? Is my size within the one-percent rule? [pause] "
  "Is it a prime hour, and am I calm — not chasing or bored? [pause] "
  "If you can't tick every box, it isn't a trade. It's a gamble. "
  "The best traders skip more setups than they take."),

 # ── RECAP ──────────────────────────────────────────────────────────────────
 ("s26_recap", "ia_recap",
  {"items": [
   "Intraday = a rented bike: open AND close the same day; flat by 3:30, no overnight risk",
   "Leverage is a magnifying glass; costs are tolls — both cut BOTH ways. Respect them",
   "Swim WITH the higher-timeframe trend; use VWAP as your water line",
   "Mark floors & ceilings before the open: previous-day high/low and the opening range",
   "Wait for the gate to break — breakout or retest — confirmed by the crowd (volume). Don't chase",
   "Every trade: seatbelt (stop) first, target at 2R minimum, size by the 1% bankroll rule",
   "Fish when the fish bite — prime hours; avoid the dead mid-day and the first 5 minutes",
   "Discipline beats prediction — 71% lose by breaking rules they already know",
  ],
   "closer": "You can't control the market — only your risk, your rules, and your patience. Master those, and you're ahead of most."},
  "Let's bring it all together in one breath. [pause] "
  "Intraday means you open and close the same day — like a rented bike, returned by three thirty. "
  "No overnight risk. [pause] "
  "Leverage is a magnifying glass, and costs are tolls — both cut both ways, so respect them. [pause] "
  "Swim with the trend, and use VWAP as your water line. "
  "Mark your floors and ceilings before the open. [pause] "
  "Wait for the gate to break, confirmed by the crowd's roar. Don't chase the bus. [pause] "
  "Every trade: seatbelt first, target at twice your risk, size like a poker bankroll — one percent a hand. "
  "Fish when the fish are biting. [pause] "
  "And remember why seventy-one percent lose — they break rules they already know. "
  "You can't control the market. Only your risk, your rules, and your patience. "
  "Master those, and you're ahead of most. [pause] "
  "Education only, not investment advice. Consult a SEBI-registered advisor. Thanks for watching."),
]

# ──────────────────────────── TTS engine (edge-tts, from projects/intraday-en)
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

concat_list = os.path.join(ROOT, "concat_ia.txt")
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
