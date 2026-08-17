#!/usr/bin/env python3
"""Technical Analysis: Reading the Market's Own Language — English course.
~20 min, 32 scenes, prefix `tac`, Neerja Neural voice (en-IN-NeerjaNeural).
Budget: ~175 wpm (Neerja at -4% rate with 0.55s pauses) → ~3,500 words for 20 min.
Voice consistency: same Neerja as trader-tools-en — required for the series.
Usage: python3 build.py
"""
import json, os, re, subprocess, time

VOICE = "en-IN-NeerjaNeural"; RATE = "-4%"; GAP = 0.5; PAUSE = 0.55; PREFIX = "tac"
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
 ("s01_title", "tac_title", {},
  "Every price — every candle — is a vote. Bulls vote up, bears vote down. "
  "The chart is the running tally. [pause] "
  "This course: candle anatomy, candlestick patterns, chart formations, "
  "and confirming indicators — end to end. [pause] "
  "One note: technical analysis reads probabilities, not certainties. "
  "These are patterns, not guarantees. Education only, not investment advice. "
  "Consult a SEBI-registered advisor before investing."),

 # ── PART 1 ─────────────────────────────────────────────────────────────────
 ("s02_div1", "tac_div",
  {"n": 1, "title": "The Language of Charts", "sub": "Why charts · Timeframes · Reading one candle", "color": C},
  "Part one. The language of charts — why price tells the story before the headlines do."),

 ("s03_whyta", "tac_whyta", {},
  "Why bother with charts? By the time a story breaks in the press, "
  "the smart money has already acted. [pause] "
  "The chart recorded every transaction in real time — every buyer, every seller, "
  "every institutional order. Look at the two panels. "
  "The analyst consensus said buy. What did price actually do? "
  "It broke support, expanded on red days, and diverged on momentum. [pause] "
  "The chart was not wrong. Price already had the information. "
  "Our job is to learn to read it."),

 ("s04_timeframes", "tac_timeframes", {},
  "The same stock looks different on different timeframes. [pause] "
  "The one-hour chart is noisy — hard to read any direction. "
  "The daily shows a cleaner trend. The weekly? The move is unmistakable. [pause] "
  "Use the larger timeframe for your directional bias, the daily for your setup, "
  "and intraday only for precise entry. [pause] "
  "Trade WITH the larger timeframe. "
  "Fighting the weekly trend on a one-hour chart is one of the "
  "most expensive mistakes a beginner makes."),

 ("s05_anatomy", "tac_anatomy", {},
  "Every candle has four data points: Open, High, Low, and Close. [pause] "
  "The body spans Open to Close. "
  "Green means Close is above Open — bulls won the session. [pause] "
  "The upper wick shows how high price went — then pulled back. "
  "Sellers stepped in at the tip and pushed price back down. [pause] "
  "The lower wick shows how low price went — then recovered. "
  "Buyers stepped in and defended that level. [pause] "
  "One candle encodes a complete battle: where the session started, "
  "how far each side pushed, and who had the final say. "
  "The close is the verdict."),

 # ── PART 2 ─────────────────────────────────────────────────────────────────
 ("s06_div2", "tac_div",
  {"n": 2, "title": "Single Candle Patterns", "sub": "Doji · Hammer · Marubozu · Engulfing", "color": Y},
  "Part two. Single candle patterns — what one candle can tell you about the battle."),

 ("s07_doji", "tac_doji", {},
  "The doji: open and close are nearly identical — paper-thin body. "
  "Neither side won. [pause] "
  "Standard doji has equal wicks — pure indecision. [pause] "
  "Dragonfly doji: long lower wick, no upper. Bears pushed hard, "
  "buyers absorbed everything and closed price back at the open. Demand at lows. [pause] "
  "Gravestone: bulls pushed high, then sellers dragged it back. "
  "Long-legged: both sides tried and failed. Maximum uncertainty. [pause] "
  "Context matters — a doji after a long trend is far more significant."),

 ("s08_hammer", "tac_hammer", {},
  "Hammer: small body at the TOP of the range, long lower wick — at least twice the body. [pause] "
  "Sellers drove price sharply lower — but buyers absorbed everything and drove it back up. "
  "A sign of demand. [pause] "
  "The hammer only matters in a DOWNTREND. "
  "Left panel: five red candles, then the hammer. Potential reversal. [pause] "
  "Right panel: the identical shape in an uptrend — the Hanging Man. "
  "Same body, same wick, opposite meaning. "
  "After a rally, a long lower wick says bulls had trouble, not strength. [pause] "
  "Context decides everything."),

 ("s09_marubozu", "tac_marubozu", {},
  "If a doji shows indecision, a Marubozu shows the opposite: total conviction. [pause] "
  "Bullish Marubozu: no wicks. Open equals Low, Close equals High. "
  "From first tick to last, bulls controlled every moment. "
  "Not a single seller could push it back. [pause] "
  "Bearish Marubozu: no wicks. Open equals High, Close equals Low. "
  "Bears owned the entire session. [pause] "
  "A Marubozu at a key breakout level signals strong follow-through intent. "
  "There was no hesitation."),

 ("s10_engulfing", "tac_engulfing", {},
  "The engulfing pattern shows a clear shift in who controls the market. [pause] "
  "Left panel: a small red candle, then a much larger green candle "
  "whose body completely covers the previous body. "
  "Bullish engulfing — buyers came in with overwhelming force. [pause] "
  "Right panel: a small green candle, then a large red candle that swallows it whole. "
  "Bearish engulfing — sellers took the full range and more. [pause] "
  "The second body must fully cover the first. "
  "It's most significant after an extended trend — "
  "the bigger the momentum shift, the cleaner the signal."),

 # ── PART 3 ─────────────────────────────────────────────────────────────────
 ("s11_div3", "tac_div",
  {"n": 3, "title": "Multi-Candle Patterns", "sub": "Harami · Morning Star · Three Soldiers", "color": V},
  "Part three. Multi-candle patterns — when two or three candles together tell a stronger story."),

 ("s12_harami", "tac_harami", {},
  "Harami means 'pregnant' in Japanese — a large mother candle, "
  "a small baby nestled inside it. [pause] "
  "Bullish harami: a large bearish candle followed by a smaller bullish candle "
  "whose body fits entirely within the mother's body. "
  "The prior downward momentum has stalled. Selling pressure is narrowing. [pause] "
  "Bearish harami is the inverse: an uptrend, a large bullish candle, "
  "then a small bearish candle inside it. Buying momentum is drying up. [pause] "
  "Harami is an alert, not a signal. Wait for confirmation on the next candle."),

 ("s13_morningstar", "tac_morningstar", {},
  "Morning Star: three candles, one of the most reliable bullish reversals. [pause] "
  "Candle one: strong bearish — trend clearly down. "
  "Candle two: small body or doji — selling has exhausted itself. [pause] "
  "Candle three: strong bullish, closing well into the body of the first candle. "
  "Bulls have taken control. [pause] "
  "Most powerful when the second candle gaps from the first, "
  "and the third closes more than halfway into the first's body. [pause] "
  "Evening Star is the mirror: the same three-candle structure at the top of an uptrend."),

 ("s14_threewhite", "tac_threewhite", {},
  "Three White Soldiers is a momentum continuation signal — not a reversal. [pause] "
  "Three consecutive bullish candles, each opening within the previous body "
  "and closing near its own high. A staircase of buying pressure across three sessions. [pause] "
  "Three Black Crows is the same structure inverted: three consecutive bearish candles "
  "stepping down, each opening inside the previous body and closing near the low. "
  "Strong distribution. [pause] "
  "When Three Black Crows appears after a long rally, treat it as a serious warning."),

 # ── PART 4 ─────────────────────────────────────────────────────────────────
 ("s15_div4", "tac_div",
  {"n": 4, "title": "Chart Patterns", "sub": "SR · Trendlines · H&S · Double Top · Flag · Triangle", "color": C},
  "Part four. Chart patterns — formations that develop over days and weeks and carry measured-move targets."),

 ("s16_sr", "tac_sr", {},
  "Support is a price level where buyers historically step in. "
  "Resistance is the ceiling where sellers consistently appear. [pause] "
  "Watch the chart: each time price approaches resistance, it stalls and reverses. "
  "Each test of support finds buyers. [pause] "
  "These levels have memory. The more times a level holds, the more significant it becomes. "
  "And when price breaks cleanly ABOVE resistance — that resistance often "
  "flips and becomes the new support. [pause] "
  "Former resistance becomes support on a retest. "
  "This flip is one of the most reliable phenomena in all of technical analysis."),

 ("s17_trendlines", "tac_trendlines", {},
  "A trendline connects the lows of an uptrend — or the highs of a downtrend — "
  "into a straight line. [pause] "
  "In an uptrend: higher highs AND higher lows. "
  "Each pullback finds support at a higher point than the last. "
  "Connect those higher lows — that's your uptrend line. [pause] "
  "As long as price stays above the line, the trend is intact. "
  "Traders buy dips to the line. [pause] "
  "A close BELOW the trendline is the first warning. "
  "A second close below confirms the break. [pause] "
  "You need at least two points to draw a trendline. "
  "Three touches make it significant."),

 ("s18_hs", "tac_hs", {},
  "Head and Shoulders is one of the most reliable reversal patterns. [pause] "
  "Three parts: a rally to a peak and pullback — the left shoulder. "
  "A higher peak — the head. A third rally that fails to reach the head — the right shoulder. [pause] "
  "The neckline connects the two pullback lows. "
  "Break below the neckline confirms the pattern. [pause] "
  "Measured move: head minus neckline, projected below the breakdown. "
  "Here — head at one eighteen, neckline at one oh three — target is eighty-eight."),

 ("s19_doubletop", "tac_doubletop", {},
  "The double top — two roughly equal peaks, separated by a pullback. "
  "The shape of the letter M. [pause] "
  "Price rallied to a peak, was rejected, pulled back to the neckline, "
  "then rallied again to the same height. The second time, sellers were ready. [pause] "
  "When price breaks below the neckline, the pattern confirms. "
  "Target: project the height from neckline to peaks, downward from the breakdown. [pause] "
  "The double bottom — the letter W — is the mirror: two equal lows, "
  "breakout above the neckline, same measured move going up."),

 ("s20_flag", "tac_flag", {},
  "The bull flag is a continuation pattern — the trend isn't over, just pausing. [pause] "
  "Two parts. Flagpole: a sharp, strong move up with high volume. "
  "Then the flag: a slow, tight pullback in a downward channel, on declining volume. "
  "Bulls are resting, not retreating. [pause] "
  "Breakout above the flag's upper channel line resumes the prior trend. "
  "Volume should surge on breakout — that's the confirmation. [pause] "
  "Target: flagpole height added to the breakout point. "
  "Bear flag is the same structure inverted — sharp move down, "
  "tight upward consolidation, then continuation lower."),

 ("s21_triangle", "tac_triangle", {},
  "The ascending triangle shows buyers getting stronger while sellers hold the same level. [pause] "
  "A flat resistance line at the top — price tests it, gets rejected, "
  "pulls back, and tests again. Same ceiling every time. [pause] "
  "But the lows keep rising: each pullback finds support at a HIGHER level. "
  "Higher lows mean buyers are becoming more aggressive. [pause] "
  "As the lines converge, the setup coils. "
  "Eventually resistance gives way — and the move is often sharp and fast. [pause] "
  "Descending triangle: flat support, falling highs — sellers more aggressive. "
  "Usually resolves downward."),

 # ── PART 5 ─────────────────────────────────────────────────────────────────
 ("s22_div5", "tac_div",
  {"n": 5, "title": "Indicators", "sub": "Volume · MA · RSI · MACD · Bollinger Bands", "color": Y},
  "Part five. Indicators — tools that confirm what price action is already saying. Never use them instead of price — use them alongside it."),

 ("s23_volume", "tac_volume", {},
  "Before RSI, before MACD — there's volume. "
  "Volume is the number of shares traded in a session. [pause] "
  "A price move with high volume is meaningful. On low volume — it's suspect. [pause] "
  "Heavy green volume on up days means large buyers are accumulating. "
  "Heavy red volume on down days means distribution. [pause] "
  "Classic warning: price making new highs but volume shrinking. "
  "The rally is running out of fuel. [pause] "
  "On-Balance Volume adds volume on up days and subtracts on down days. "
  "The OBV line tracks whether money is flowing in or out over time."),

 ("s24_ma", "tac_ma", {},
  "A moving average smooths price noise by averaging closes over N periods. [pause] "
  "SMA ten: last ten closes averaged. SMA thirty: slower and smoother. [pause] "
  "When the faster SMA ten crosses above SMA thirty, "
  "recent momentum has shifted upward — the golden cross. Bullish signal. [pause] "
  "Death cross: faster MA crossing below the slower. Bearish momentum. [pause] "
  "EMA weights recent prices more heavily — reacts faster. "
  "Short-term traders prefer EMAs; position traders use simple MAs. [pause] "
  "Moving averages lag. They confirm trends after they start. Use alongside price action."),

 ("s25_rsi", "tac_rsi", {},
  "RSI measures the speed and size of recent price moves, on a scale of zero to one hundred. [pause] "
  "Above seventy: overbought. Below thirty: oversold. [pause] "
  "But in a STRONG uptrend, RSI can stay above seventy for weeks. "
  "Selling just because RSI is high is one of the most expensive mistakes in trading. [pause] "
  "The more powerful use: divergence. "
  "Price makes a higher high, RSI makes a lower high — "
  "momentum is weakening before price confirms it. "
  "That warns of a potential reversal. [pause] "
  "Use RSI to confirm a setup. Not to create one on its own."),

 ("s26_macd", "tac_macd", {},
  "MACD is built from three components: "
  "the MACD line — gap between a twelve and twenty-six period EMA. "
  "The signal line — a nine-period EMA of the MACD line. "
  "The histogram — gap between the two. [pause] "
  "Key signal: MACD line crossing above the signal line means "
  "short-term momentum has turned bullish. Crossing below — bearish. [pause] "
  "The histogram turning positive is often the earliest sign of the cross. "
  "Watch for it flipping near a support level. [pause] "
  "MACD is lagging. It confirms momentum has shifted — "
  "not where price will go. Combine with support, resistance, and candle signals."),

 ("s27_bb", "tac_bb", {},
  "Bollinger Bands: a dynamic volatility envelope. "
  "Middle band — twenty-period moving average. "
  "Upper and lower bands — two standard deviations away. [pause] "
  "When bands squeeze together, the market is coiling for a big move. "
  "Direction unknown until price breaks. [pause] "
  "After the squeeze, bands expand rapidly. "
  "Initial breakout direction usually tells you where the move goes. [pause] "
  "Touching the upper band does NOT mean sell. "
  "In a strong trend, price walks the band. Confirm with candle or RSI."),

 # ── PART 6 ─────────────────────────────────────────────────────────────────
 ("s28_div6", "tac_div",
  {"n": 6, "title": "Putting It Together", "sub": "Confluence · Risk · Pre-trade checklist", "color": G},
  "Part six. Putting it all together — confluence, risk management, and the ritual before every trade."),

 ("s29_confluence", "tac_confluence", {},
  "No single signal is reliable enough to trade on its own. "
  "The power comes from confluence — multiple signals pointing the same way. [pause] "
  "Look at the example: a support zone that has held three times. "
  "A bullish doji at that support. "
  "RSI entering oversold for the first time in weeks. "
  "A volume spike suggesting big buyers. "
  "Price touching the two-hundred-day moving average. [pause] "
  "Any one factor alone — maybe. "
  "All five together at the same price level? "
  "That's a high-probability setup. [pause] "
  "Stack three or four confluent signals before entering. Fewer is noise."),

 ("s30_risk", "tac_risk", {},
  "Even the best setup fails sometimes. Risk management is how you stay in the game. [pause] "
  "Every trade needs three levels defined BEFORE entry: "
  "Entry, Stop-loss, and Target. [pause] "
  "Entry at one hundred, stop at ninety-six — four points of risk, one R. "
  "Target at one oh eight — eight points of reward, two R. "
  "Risk-to-reward: two to one. [pause] "
  "At two-to-one R:R, you only need to win thirty-four percent of the time "
  "to be profitable long-term. "
  "You can lose two out of three trades and still make money "
  "if winners are twice your losers. [pause] "
  "Position sizing: never risk more than one to two percent of total capital per trade."),

 ("s31_checklist", "tac_checklist",
  {"items": [
   "What is the trend on the weekly chart? Are we WITH it?",
   "What is the key support or resistance level nearest to entry?",
   "Is there a candle signal — doji, engulfing, hammer — confirming?",
   "Does an indicator (RSI, MACD, BB) support the same direction?",
   "Where exactly is my stop-loss, and why is it there?",
   "Where is my target, and is R:R at least 2:1?",
   "Am I risking more than 2% of capital on this trade?",
   "Is volume confirming this move, or is it suspiciously low?",
  ]},
  "Before every trade, run this checklist. [pause] "
  "What is the weekly trend — are you trading with it? "
  "Is there a candle signal confirming? Does an indicator agree? [pause] "
  "Where is your stop — at a logical level, not a random number? "
  "Is R:R at least two to one? Are you risking more than two percent of capital? "
  "Is volume confirming? [pause] "
  "If you can't answer confidently — the setup isn't ready. Wait. "
  "Capital you protect today is ammunition for the setups that ARE ready."),

 # ── RECAP ──────────────────────────────────────────────────────────────────
 ("s32_recap", "tac_recap",
  {"items": [
   "Every candle = Open, High, Low, Close — a complete battle report",
   "Doji = indecision; Hammer = demand at lows (only in downtrend)",
   "Engulfing & Three White Soldiers = momentum shift with force",
   "Morning Star / Evening Star = three-candle trend reversals",
   "Support & Resistance: price has memory — these levels repeat",
   "H&S, Double Top, Flag, Triangle all carry measured-move targets",
   "Indicators (RSI, MACD, BB, Volume) CONFIRM — they don't predict",
   "Confluence: stack 3–4 signals before acting. Risk: 2:1 R:R minimum",
  ],
   "closer": "Charts don't lie — but they speak in probabilities, not certainties. Learn the language."},
  "The whole map. [pause] "
  "Doji: indecision. Hammer: demand at lows — only in a downtrend. "
  "Engulfing: momentum shift with force. Morning Star: three-candle reversal warning. [pause] "
  "Support and resistance have memory. "
  "H&S, double tops, flags, triangles — all have measured-move targets. [pause] "
  "Indicators confirm price — RSI, MACD, Bollinger Bands, volume. "
  "They do not replace price action. [pause] "
  "Before every trade: stack confluent signals, define stop and target first, "
  "two-to-one R:R minimum, two percent max risk per trade. [pause] "
  "These tools read probabilities, not certainties. "
  "Education only, not advice. Consult a SEBI-registered advisor. Thanks for watching."),
]

# ──────────────────────────── caption cue generator (verbatim from trader-tools-en)
def caption_cues(text, start, end):
    clean = re.sub(r"\s+", " ", text.replace("[pause]", " ")).strip()
    parts = re.split(r"(?<=[.?!])\s+", clean); cues = []
    for pt in parts:
        pt = pt.strip()
        if not pt: continue
        if len(pt) > 60 and ("," in pt or "—" in pt):
            buf = ""
            for s in re.split(r"(?<=[,—])\s+", pt):
                if len(buf) + len(s) > 60 and buf: cues.append(buf.strip()); buf = s
                else: buf = (buf + " " + s).strip()
            if buf: cues.append(buf.strip())
        else: cues.append(pt)
    total = sum(len(c) for c in cues) or 1; span, out, tc = end - start, [], start
    for c in cues:
        d = span * (len(c) / total); out.append([round(tc, 3), round(tc + d, 3), c]); tc += d
    if out: out[-1][1] = round(end, 3)
    return out

# ──────────────────────────── TTS engine (edge-tts, verbatim from trader-tools-en)
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
    manifest.append({"id": sid, "variant": variant, "props": props, "wav": path, "duration": dur, "narration": text})
    print(f"  {sid:18s} {dur:6.2f}s", flush=True)

silence = os.path.join(FIN, "_sil.wav")
subprocess.run(["ffmpeg","-y","-f","lavfi","-i","anullsrc=r=24000:cl=mono","-t",str(GAP),silence],
               check=True, capture_output=True)

concat_list = os.path.join(ROOT, "concat_tac.txt")
with open(concat_list, "w") as f:
    for i, m in enumerate(manifest):
        f.write(f"file '{m['wav']}'\n")
        if i < len(manifest) - 1:
            f.write(f"file '{silence}'\n")

subprocess.run(["ffmpeg","-y","-f","concat","-safe","0","-i",concat_list,"-c","copy",
                os.path.join(PUBLIC, "narration.wav")], check=True, capture_output=True)

cuts, cues, t = [], [], 0.0
for m in manifest:
    start, end = t, t + m["duration"]
    cuts.append({
        "id": m["id"], "type": m["variant"],
        "in_seconds": round(start, 3), "out_seconds": round(end, 3),
        "props": {**m["props"], "dur": round(m["duration"] + GAP, 3)},
    })
    cues.extend(caption_cues(m["narration"], start, end))
    t = end + GAP

props_out = {
    "cuts": cuts,
    "captions": cues,
    "audio": {"narration": {"src": f"{PREFIX}/narration.wav", "volume": 1.0}},
}
json.dump(props_out, open(os.path.join(ROOT, "artifacts", "edit_decisions.json"), "w"), indent=2)
total = t - GAP
print(f"\ntotal {total:.2f}s ({total/60:.2f} min) · {len(cuts)} scenes")
print("Next: render QA stills, then wait for orchestrator approval before final render.")
