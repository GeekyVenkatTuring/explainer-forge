#!/usr/bin/env python3
"""The Macro-Dip Playbook — internal research / education video.
~11-12 min, 17 scenes, prefix `dip`, Neerja Neural (en-IN-NeerjaNeural).
Companion to ta-course-en / intraday-en — same Neerja voice. NO captions, NO music.

IMPORTANT — DATA HONESTY:
This is a METHODOLOGY video, built deliberately WITHOUT specific stock buy-calls
or unverified per-stock figures, because live per-stock market data could not be
verified to this repo's accuracy standard (skill 12). Every market number below is
QUALITATIVE / INDICATIVE macro context (crude "near $100", rupee "past ~96", index
"~2-3%", "worst week in months") — consistent across multiple sources and matching
the user's own description of last week — NOT precision claims. No PE, quarterly, or
"X% below peers" figure is asserted for any individual company. Disclaimer in title
+ recap. Usage: python3 build.py
"""
import json, os, subprocess, time

VOICE = "en-IN-NeerjaNeural"; RATE = "-4%"; GAP = 0.5; PAUSE = 0.55; PREFIX = "dip"
ROOT = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(ROOT, "..", ".."))
PUBLIC = os.path.join(REPO, "composer", "public", PREFIX)
RAW = os.path.join(ROOT, "assets", "raw")
FIN = os.path.join(ROOT, "assets")
for d in (PUBLIC, RAW, os.path.join(ROOT, "artifacts"), os.path.join(ROOT, "renders")):
    os.makedirs(d, exist_ok=True)

C = "#22D3EE"; G = "#34D399"; V = "#A78BFA"; Y = "#FBBF24"; R = "#FB7185"

SEGMENTS = [

 ("s01_title", "dip_title", {},
  "Last week, the market fell for five straight sessions — its worst week in months. [pause] "
  "When that happens, good companies get sold off alongside the bad. "
  "Prices fall for reasons that have nothing to do with the business. [pause] "
  "This is an internal playbook for those moments: how to tell a genuine, market-wide "
  "bargain from a value trap — and how to screen for it. [pause] "
  "Education only, not investment advice. Every market figure here is indicative — "
  "always verify the data yourself."),

 ("s02_thesis", "dip_thesis", {},
  "Here's the core idea. When a big wave of selling hits, it's like a tide going out. "
  "It drags the good boats down with the bad. [pause] "
  "A market-wide sell-off pulls almost everything lower together — including quality "
  "companies whose fundamentals haven't changed at all. [pause] "
  "That creates two very different situations. One: a macro dip, where a great business "
  "fell for external reasons. That's an opportunity. [pause] "
  "Two: company damage, where the stock fell because something is genuinely wrong. "
  "That's a value trap. [pause] "
  "The entire skill is telling these apart. Buy the first. "
  "Never buy the second just because it looks cheap."),

 ("s03_div1", "dip_div",
  {"n": 1, "title": "The Setup", "sub": "What dragged the market down — and who it hit", "color": Y},
  "Part one. The setup — what actually dragged the market down last week, "
  "and which sectors each force hit."),

 ("s04_setup", "dip_setup", {},
  "Last week wasn't one problem. It was five macro forces landing at once. [pause] "
  "Crude oil surged toward a hundred dollars a barrel. "
  "The rupee weakened past around ninety-six to the dollar. "
  "Foreign investors turned net sellers. "
  "War and geopolitical tension spiked global fear. "
  "And fresh US restrictions hit the IT sector. [pause] "
  "Notice what's missing from that list: any single company's results. [pause] "
  "That's the signature of a macro sell-off. The index fell roughly two to three percent "
  "over the week — but the reasons were external. When the cause is macro, quality gets "
  "mispriced. Let's take each force in turn."),

 ("s05_crude", "dip_crude", {},
  "Factor one: expensive crude. [pause] "
  "When oil pushes toward a hundred dollars, it raises input and fuel costs across the economy. [pause] "
  "It pressures the oil marketing companies, whose margins get squeezed. "
  "It hits paints and tyres, which use crude derivatives. "
  "And it raises costs for aviation and logistics. [pause] "
  "But the same high price benefits the upstream producers — the companies that pump the oil. [pause] "
  "The key question: is this crude spike temporary, driven by conflict, or a structural shift? "
  "Temporary spikes are exactly where strong importers get oversold."),

 ("s06_rupee", "dip_rupee", {},
  "Factor two: a weaker rupee. [pause] "
  "A falling rupee cuts both ways. Imports get more expensive — so importers and "
  "companies with dollar debt feel the pain. [pause] "
  "But exporters win. When they earn in dollars and convert back to rupees, "
  "a weak rupee means more revenue. That helps IT services, pharma, and specialty chemicals. [pause] "
  "Now hold onto a puzzle. A weak rupee is a tailwind for IT. "
  "Yet IT still fell hard last week. [pause] "
  "When a stock drops despite a tailwind, something else is going on. We'll come back to that."),

 ("s07_fii", "dip_fii", {},
  "Factor three: foreign investors selling. [pause] "
  "This one is the richest hunting ground, and here's why. "
  "When foreign funds pull money out, they don't sell what's overvalued. "
  "They sell what they own, and what's easy to sell. [pause] "
  "That means the index heavyweights, the private banks and financials, "
  "and the large-cap leaders in every sector — great businesses included. [pause] "
  "Meanwhile, domestic institutions often step in and absorb that selling. [pause] "
  "So a wonderful company can fall simply because it's big and liquid and foreigners "
  "needed to raise cash. The fundamentals never changed. That's a textbook macro dip."),

 ("s08_war", "dip_war", {},
  "Factor four: war and geopolitics. [pause] "
  "Conflict creates uncertainty, and uncertainty triggers risk-off selling. "
  "Volatility spikes, and almost every sector dips together. "
  "High-beta and cyclical names fall hardest. [pause] "
  "A few areas benefit — defence, and safe-havens like gold. [pause] "
  "But here's the pattern with fear: markets price it in fast, and forgive it slowly. "
  "If the conflict doesn't actually change a company's earnings, "
  "that fear-driven dip tends to reverse once the headlines fade."),

 ("s09_usit", "dip_usit", {},
  "Factor five brings us back to that IT puzzle. [pause] "
  "Fresh US restrictions hit the sector. And this is where you have to be careful, "
  "because it forces the single most important question in dip-buying. [pause] "
  "Is the fall temporary, or structural? [pause] "
  "If it's a one-off cost or a policy scare, and the earnings power is intact — "
  "that's a genuine dip to buy. [pause] "
  "But if it permanently impairs the business model and lowers growth for years — "
  "that's not a dip. That's a re-rating to a lower value. "
  "A cheap price doesn't help you if earnings are permanently lower. [pause] "
  "With IT and these US curbs, treat that risk seriously."),

 ("s10_div2", "dip_div",
  {"n": 2, "title": "The Playbook", "sub": "Dip vs trap · quality · value · the screen · risk", "color": G},
  "Part two. The playbook — how to separate a real opportunity from a trap, "
  "and screen for it systematically."),

 ("s11_dipvstrap", "dip_dipvstrap", {},
  "So how do you actually tell a macro dip from company damage? Here's the checklist. [pause] "
  "It's likely a macro dip when the whole sector or market fell together, "
  "there's no company-specific bad news, earnings and guidance are intact, "
  "the trigger is external and temporary, and the balance sheet is unchanged. [pause] "
  "It's probably company damage when only that one stock fell hard, "
  "there's an earnings miss or a guidance cut, there are governance or accounting red flags, "
  "a permanent shift in the business, or rising debt and cash-flow stress. [pause] "
  "The fastest test: did the peers fall too? "
  "If the whole sector dropped together, it's macro. "
  "If only this name cratered, dig deeper before you touch it."),

 ("s12_quality", "dip_quality", {},
  "Once you have a candidate, run two filters. "
  "The first: is it actually a good business? [pause] "
  "Look for a return on equity above roughly fifteen percent — a sign it uses capital efficiently. "
  "Low debt, with a debt-to-equity under about half. "
  "Consistent profit growth over three to five years. "
  "Positive free cash flow — real cash, not just paper profit. "
  "And a durable moat, ideally a leader in its space. [pause] "
  "Here's the point: none of these numbers move because of a war or a crude spike. "
  "If they're all intact, the business is fine. Only the price changed."),

 ("s13_value", "dip_value", {},
  "The second filter: is it actually cheap? [pause] "
  "And this matters — a stock can fall five percent and still be expensive. "
  "Falling is not the same as cheap. [pause] "
  "So compare. Is its PE below the industry or peer median? "
  "Is the PEG reasonable — cheap relative to its own growth? "
  "Is the price-to-book below its five-year average? "
  "Is it trading well below its fifty-two-week high? [pause] "
  "Look at the illustration: the same quality, but a lower multiple than its peers. "
  "That is a discount. [pause] "
  "The reason to buy is never just 'it fell.' "
  "It's 'a leader is now trading below its peers and its own history.'"),

 ("s14_screen", "dip_screen", {},
  "Now let's make this systematic, so you're not guessing. [pause] "
  "On a screener, encode the filters as a query. "
  "Market cap above twenty thousand crore, to stay in large and mid-caps. "
  "Return on equity above fifteen. Debt-to-equity below zero point five. "
  "Profit growth above ten percent. "
  "And price-to-earnings below the industry PE — cheaper than peers. [pause] "
  "That gives you a list of strong, low-debt, growing companies trading at a discount. [pause] "
  "Then intersect it with last week's top losers, from a tool like Trendlyne. "
  "Keep only the names in both lists — strong, cheap, and freshly dipped. [pause] "
  "But remember: the screen produces a shortlist, never a buy. "
  "Every name still has to pass the checks by hand."),

 ("s15_confirm", "dip_confirm", {},
  "Before you buy any name on that shortlist, four steps. [pause] "
  "One: confirm why it fell. Read the news. Sector-wide and macro? Good. "
  "Company-specific? Stop right there. [pause] "
  "Two: wait for it to stabilise. Don't try to catch a falling knife. "
  "Let the price base out before you enter. [pause] "
  "Three: enter in tranches. Buy in parts, not all at once — "
  "you will not pick the exact bottom. [pause] "
  "Four: write down your thesis and your exit. "
  "Why you bought, and what would prove you wrong. [pause] "
  "A cheap price is an invitation, not a signal."),

 ("s16_risk", "dip_risk", {},
  "Finally, risk management — because even a perfect shortlist fails sometimes. [pause] "
  "Size each position so no single name can hurt you too much. "
  "Spread across the shortlist rather than betting everything on one idea. [pause] "
  "Give the thesis time — dips reward patience, not panic. [pause] "
  "And exit if the thesis actually breaks, not just because the price wobbled for a day. [pause] "
  "Sizing and diversification are what let you be wrong sometimes and still come out ahead over time."),

 ("s17_recap", "dip_recap",
  {"items": [
   "A market-wide sell-off drags quality down with the junk — that's the opening",
   "Last week: crude, weak rupee, FII selling, war, and US curbs on IT",
   "Macro DIP (business fine) vs company DAMAGE (business broken) — did peers fall too?",
   "Filter 1 — strong: high ROE, low debt, steady growth, real cash flow",
   "Filter 2 — cheap: PE below peers & its own history, not just 'fallen'",
   "Screen it → intersect with the week's losers → verify every name by hand",
   "Confirm why it fell, wait for stability, enter in tranches, manage risk",
  ],
   "closer": "Buying the dip isn't courage — it's a repeatable process. The market hands you quality on sale; the checklist tells you which."},
  "Let's bring the playbook together. [pause] "
  "A market-wide sell-off drags quality down with the junk — that's the opportunity. [pause] "
  "Last week it was five macro forces: crude, a weak rupee, foreign selling, war, "
  "and US curbs on IT. [pause] "
  "The one distinction that matters: a macro dip, where the business is fine, "
  "versus company damage, where it isn't. Did the peers fall too? [pause] "
  "Then two filters — is it a genuinely strong business, and is it genuinely cheaper than its peers. [pause] "
  "Screen for it, intersect with the week's losers, then verify every name by hand. "
  "Confirm why it fell, wait for stability, enter in tranches, and manage your risk. [pause] "
  "Buying the dip isn't about courage. It's about a process. [pause] "
  "This is internal education, not investment advice — verify all data, "
  "and consult a SEBI-registered advisor. Thanks for watching."),
]

# ──────────────────────────── TTS engine (edge-tts, from ta-course-en / intraday-en)
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

manifest = []
for sid, variant, props, text in SEGMENTS:
    path, dur = gen_one(sid, text)
    manifest.append({"id": sid, "variant": variant, "props": props, "wav": path, "duration": dur})
    print(f"  {sid:16s} {dur:6.2f}s", flush=True)

silence = os.path.join(FIN, "_sil.wav")
subprocess.run(["ffmpeg","-y","-f","lavfi","-i","anullsrc=r=24000:cl=mono","-t",str(GAP),silence],
               check=True, capture_output=True)
concat_list = os.path.join(ROOT, "concat_dip.txt")
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
    cuts.append({"id": m["id"], "type": m["variant"], "in_seconds": round(start, 3),
                 "out_seconds": round(end, 3), "props": {**m["props"], "dur": round(m["duration"] + GAP, 3)}})
    t = end + GAP
json.dump({"cuts": cuts, "audio": {"narration": {"src": f"{PREFIX}/narration.wav", "volume": 1.0}}},
          open(os.path.join(ROOT, "artifacts", "edit_decisions.json"), "w"), indent=2)
total = t - GAP
words = sum(len(text.replace("[pause]", " ").split()) for _, _, _, text in SEGMENTS)
print(f"\ntotal {total:.2f}s ({total/60:.2f} min) · {len(cuts)} scenes · {words} words · NO captions · NO music")
