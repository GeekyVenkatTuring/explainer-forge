#!/usr/bin/env python3
"""Q1 FY27 Earnings Day (ENGLISH) — 22 July 2026. Reuses `sm` scene set. English TTS + English frames.
A day of extremes tied to the crude spike. Verified (all YoY vs Q1 FY26):
IndusInd Bank PAT Rs 1,037 cr (+71.6%; NII Rs 4,685 cr; GNPA 3.25% improved). Nestle India PAT
Rs 958.7 cr consol (+48%; std Rs 975.1 cr; rev Rs 6,378 cr +25.16%; stock 52-wk high +4%).
Eternal (Zomato) PAT Rs 92 cr (+268% from Rs 25 cr) but MISSED ~Rs 258 cr estimate; rev Rs 20,211 cr
(+182%); Blinkit drag; stock fell. Dr Reddy's PAT Rs 443.5 cr (-68.7% from Rs 1,417.8 cr; US price
erosion). BPCL net LOSS Rs 3,962 cr (vs +Rs 6,124 cr YoY; crude spike crushed margins). HPCL also to a
loss on the crude/inventory hit. Sources: BusinessToday, Upstox, Business Standard, Republic, Outlook,
Free Press Journal, Sahi. Info, not advice.
Usage: python3 build.py            |   python3 build.py er22e
"""
import json, os, re, subprocess, sys, time

VOICE = "en-IN-NeerjaNeural"; RATE = "-4%"; GAP = 0.5; PAUSE = 0.55; PREFIX = "sm"
ROOT = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(ROOT, "..", ".."))
PUBLIC = os.path.join(REPO, "composer", "public", PREFIX); RAW = os.path.join(ROOT, "assets", "raw"); FIN = os.path.join(ROOT, "assets")
for d in (PUBLIC, RAW, os.path.join(ROOT, "artifacts"), os.path.join(ROOT, "renders")):
    os.makedirs(d, exist_ok=True)

CHAPTERS = {
 "er22e": [
 ("er_title", "sm_ptitle",
  {"title": "Today's Q1 Results", "sub": "July 22, 2026 · a day of extremes — record highs AND big losses", "kicker": "EARNINGS DAY · 22 JUL 2026"},
  "July twenty-second — another huge earnings day, with more than sixty companies reporting. But today was a day of extremes. [pause] "
  "On the same day, one stock hit a record high on a stellar result, while an oil giant posted a nearly four-thousand-crore loss. And it all ties back to one thing — the crude spike that crashed the market today. [pause] "
  "Let's break down who won, who lost, and why. Remember — all comparisons are year-on-year, and this is information analysis, not investment advice."),
 ("er_score", "sm_stats",
  {"kicker": "THE EXTREMES · NET PROFIT (YoY)", "title": "Today's Story in 3 Numbers",
   "stats": [
    {"label": "IndusInd Bank", "to": 1037, "prefix": "₹", "suffix": " Cr", "color": "#34D399", "sub": "+72% YoY · beat"},
    {"label": "Nestle India", "to": 959, "prefix": "₹", "suffix": " Cr", "color": "#34D399", "sub": "+48% · 52-week high"},
    {"label": "BPCL", "to": 3962, "prefix": "−₹", "suffix": " Cr", "color": "#FB7185", "sub": "Q1 LOSS · crude hit"},
   ],
   "note": "Two big beats and a shock loss — on the same day. The dividing line? Crude oil. Let's see who was on which side."},
  "Let's start with today's story in three numbers. [pause] "
  "IndusInd Bank — net profit one thousand thirty-seven crore, up seventy-two percent. A big beat. [pause] "
  "Nestle India — profit nine hundred fifty-nine crore, up forty-eight percent, sending the stock to a fifty-two-week high. [pause] "
  "But B-P-C-L — the oil giant — swung to a loss of nearly four thousand crore. [pause] "
  "Two big beats and a shock loss, all on the same day. And the dividing line between them is crude oil. Let's see who was on which side."),
 ("er_winners", "sm_iconcards",
  {"kicker": "THE WINNERS", "title": "Who Beat Today", "color": "#34D399",
   "items": [
    {"emoji": "🏦", "k": "IndusInd Bank", "v": "PAT ₹1,037 Cr (+72%); NII ₹4,685 Cr; GNPA improved to 3.25% — reassuring for private banks", "chip": "+72%"},
    {"emoji": "🍫", "k": "Nestle India", "v": "PAT ₹959 Cr (+48%); revenue ₹6,378 Cr (+25%); stock hit a 52-week high, up 4%", "chip": "RECORD HIGH"},
    {"emoji": "🍔", "k": "Eternal (Zomato)", "v": "Revenue ₹20,211 Cr (+182%!), PAT ₹92 Cr (+268%) — but it MISSED estimates; stock fell", "chip": "MISSED*"},
    {"emoji": "🛡️", "k": "The read-through", "v": "FMCG and private banks shrugged off crude; but the day belonged to oil — see the losers next", "chip": "CONTRAST"},
   ]},
  "First, the winners. [pause] "
  "IndusInd Bank posted a net profit of one thousand thirty-seven crore, up seventy-two percent. Its net interest income was strong, and asset quality improved, with bad loans falling to three point two five percent. That's reassuring for the whole private-bank space, which had been under a cloud. [pause] "
  "Nestle India was the star — profit up forty-eight percent, revenue up twenty-five percent, sending the stock to a fifty-two-week high. [pause] "
  "Then a fascinating one — Eternal, the parent of Zomato. Its revenue jumped a huge one hundred eighty-two percent and profit rose two hundred sixty-eight percent. And yet the stock fell. Why? We'll explain that in a moment. [pause] "
  "The read-through — F-M-C-G and private banks shrugged off crude. But the day truly belonged to oil, as we'll see next."),
 ("er_losers", "sm_iconcards",
  {"kicker": "THE CRUDE CASUALTIES", "title": "Who Lost — and Why", "color": "#FB7185",
   "items": [
    {"emoji": "🛢️", "k": "BPCL", "v": "Net LOSS ₹3,962 Cr — vs a ₹6,124 Cr profit a year ago; the crude spike crushed refining margins", "chip": "LOSS"},
    {"emoji": "⛽", "k": "HPCL", "v": "Also swung to a loss on the same crude and inventory hit — OMCs pay the price when crude jumps", "chip": "LOSS"},
    {"emoji": "💊", "k": "Dr Reddy's", "v": "PAT −69% to ₹444 Cr — US price erosion hit pharma; a separate pressure, not crude", "chip": "−69%"},
    {"emoji": "🔗", "k": "The crude connection", "v": "The same crude spike that crashed the market today is what pushed the oil marketers into the red", "chip": "TIE-IN"},
   ]},
  "Now the losers — and the theme is crude. [pause] "
  "B-P-C-L, the oil marketing giant, swung to a loss of nearly four thousand crore, versus a six-thousand-crore profit a year ago. When crude spikes suddenly, oil marketers take inventory and margin losses — and that's exactly what happened. [pause] "
  "H-P-C-L told the same story, also slipping into a loss on the crude and inventory hit. [pause] "
  "Doctor Reddy's was a different kind of loser — its profit fell sixty-nine percent, but that was due to US price erosion in pharma, a separate pressure, not crude. [pause] "
  "And here's the big connection — the very same crude spike that crashed the market today is what pushed these oil marketers into the red. The market's fear and these losses are two sides of one coin."),
 ("er_lesson", "sm_myths",
  {"kicker": "READ BEYOND THE HEADLINE", "title": "Three Lessons from Today", "mythLabel": "🔮 THE HEADLINE SAYS", "factLabel": "✅ THE REALITY IS",
   "pairs": [
    {"m": "Eternal's profit jumped 268% — brilliant!", "f": "It MISSED estimates (₹92 Cr vs ~₹258 Cr expected) — so the stock fell. Beating expectations matters, not just growth"},
    {"m": "OMC losses mean broken businesses", "f": "It's a crude-inventory hit from the price spike — often one-off, not a structural problem"},
    {"m": "All results move the same way", "f": "Same day: Nestle at a record high, BPCL in a ₹3,962 Cr loss — sector and expectations decide"},
   ]},
  "So what are the lessons? Three of them. [pause] "
  "First, and the most important — Eternal grew its profit two hundred sixty-eight percent, yet the stock fell. Why? Because it missed what analysts expected — ninety-two crore versus around two hundred fifty-eight crore. The market pays for beating expectations, not just for growth. [pause] "
  "Second — the oil marketers posting losses does not mean they're broken. A sudden crude spike causes one-off inventory and margin losses that often reverse when prices stabilise. [pause] "
  "Third — never assume all results move together. On this one day, Nestle hit a record high while B-P-C-L posted a four-thousand-crore loss. Sector and expectations decide the reaction — not the headline number alone."),
 ("er_take", "sm_checklist",
  {"kicker": "HOW TO READ AN EARNINGS DAY", "title": "5 Things to Remember", "color": "#34D399", "icon": "💡",
   "items": [
    "Compare vs expectations, not just last year (Eternal +268% yet fell)",
    "Sector context decides the reaction — crude helped no OMC today",
    "OMC losses are often crude-inventory driven — check if one-off",
    "A record profit (Nestle) can send a stock to a 52-week high",
    "One quarter isn't the trend — watch consistency over time",
   ]},
  "Finally, five things to remember when reading any earnings day. [pause] "
  "One — always compare against expectations, not just last year. Eternal grew profit two hundred sixty-eight percent and still fell, because it missed estimates. [pause] "
  "Two — sector context decides the reaction. Today, crude helped no oil marketer, but F-M-C-G and banks thrived. [pause] "
  "Three — oil marketer losses are often crude-inventory driven. Check whether it's a one-off before you judge the business. [pause] "
  "Four — a genuine record profit, like Nestle's, can send a stock straight to a fifty-two-week high. [pause] "
  "Five — one quarter is never the whole story. Watch consistency over several quarters before you conclude anything."),
 ("er_recap", "sm_recap",
  {"title": "22 July Earnings — At a Glance",
   "items": [
    "Beats: IndusInd Bank +72%, Nestle +48% (record high)",
    "Losses: BPCL −₹3,962 Cr, HPCL loss — crude crushed OMCs",
    "Dr Reddy's PAT −69% (US price erosion)",
    "Eternal profit +268% but MISSED estimates → stock fell",
    "Lesson: expectations & sector decide, not the headline",
   ],
   "closer": "It's not the number — it's the number versus what was expected."},
  "July twenty-second earnings, at a glance. [pause] "
  "The beats — IndusInd Bank up seventy-two percent, and Nestle up forty-eight percent to a record high. [pause] "
  "The losses — B-P-C-L down nearly four thousand crore and H-P-C-L in the red, as the crude spike crushed the oil marketers. [pause] "
  "Doctor Reddy's profit fell sixty-nine percent on US pricing pressure. [pause] "
  "And the lesson of the day — Eternal grew profit two hundred sixty-eight percent but missed estimates, so its stock fell. [pause] "
  "It's not the number — it's the number versus what was expected, and the sector it's in. [pause] "
  "This information is aggregated from public sources — for analysis only, not investment advice. Thanks for watching."),
 ],
}

def ffdur(path):
    out = subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","default=noprint_wrappers=1:nokey=1",path],capture_output=True,text=True,check=True)
    return round(float(out.stdout.strip()),3)

def tts_chunk(path, text):
    mp3 = path[:-4]+".mp3"
    for a in range(6):
        r = subprocess.run(["edge-tts","--voice",VOICE,f"--rate={RATE}","--text",text,"--write-media",mp3],capture_output=True)
        if r.returncode==0 and os.path.exists(mp3) and os.path.getsize(mp3)>0: break
        time.sleep(3+a*4)
    else: raise RuntimeError(f"tts failed {path}")
    subprocess.run(["ffmpeg","-y","-i",mp3,"-ar","24000","-ac","1",path],check=True,capture_output=True)
    os.remove(mp3)

def gen_one(seg_id, text):
    fin = os.path.join(FIN, seg_id+".wav")
    if os.path.exists(fin): return fin, ffdur(fin)
    chunks = [c.strip() for c in text.split("[pause]") if c.strip()]; paths=[]
    for ci,chunk in enumerate(chunks):
        cp = os.path.join(RAW, f"{seg_id}_c{ci}.wav")
        if not os.path.exists(cp): tts_chunk(cp, chunk)
        paths.append(cp)
    psil = os.path.join(RAW,"_pause.wav")
    if not os.path.exists(psil):
        subprocess.run(["ffmpeg","-y","-f","lavfi","-i","anullsrc=r=24000:cl=mono","-t",str(PAUSE),psil],check=True,capture_output=True)
    clist = os.path.join(RAW, f"{seg_id}_concat.txt")
    with open(clist,"w") as f:
        for i2,p2 in enumerate(paths):
            f.write(f"file '{p2}'\n")
            if i2 < len(paths)-1: f.write(f"file '{psil}'\n")
    subprocess.run(["ffmpeg","-y","-f","concat","-safe","0","-i",clist,"-c","copy",fin],check=True,capture_output=True)
    return fin, ffdur(fin)

def caption_cues(text, start, end):
    clean = re.sub(r"\s+"," ",text.replace("[pause]"," ")).strip()
    parts = re.split(r"(?<=[.?!])\s+", clean); cues=[]
    for pt in parts:
        pt=pt.strip()
        if not pt: continue
        if len(pt)>60 and ("," in pt or "—" in pt):
            buf=""
            for s in re.split(r"(?<=[,—])\s+", pt):
                if len(buf)+len(s)>60 and buf: cues.append(buf.strip()); buf=s
                else: buf=(buf+" "+s).strip()
            if buf: cues.append(buf.strip())
        else: cues.append(pt)
    total=sum(len(c) for c in cues) or 1; span,out,t=end-start,[],start
    for c in cues:
        d=span*(len(c)/total); out.append([round(t,3),round(t+d,3),c]); t+=d
    if out: out[-1][1]=round(end,3)
    return out

def build_chapter(ch):
    segs=CHAPTERS[ch]; manifest=[]
    for sid,variant,props,text in segs:
        path,dur=gen_one(sid,text)
        manifest.append({"id":sid,"variant":variant,"props":props,"wav":path,"duration":dur,"narration":text})
        print(f"  {sid:12s} {dur:6.2f}s",flush=True)
    silence=os.path.join(FIN,"_sil.wav")
    if not os.path.exists(silence):
        subprocess.run(["ffmpeg","-y","-f","lavfi","-i","anullsrc=r=24000:cl=mono","-t",str(GAP),silence],check=True,capture_output=True)
    clist=os.path.join(ROOT,f"concat_{ch}.txt")
    with open(clist,"w") as f:
        for i,m in enumerate(manifest):
            f.write(f"file '{m['wav']}'\n")
            if i<len(manifest)-1: f.write(f"file '{silence}'\n")
    subprocess.run(["ffmpeg","-y","-f","concat","-safe","0","-i",clist,"-c","copy",os.path.join(PUBLIC,f"{ch}.wav")],check=True,capture_output=True)
    cuts,cues,t=[],[],0.0
    for m in manifest:
        start,end=t,t+m["duration"]
        cuts.append({"id":m["id"],"type":m["variant"],"in_seconds":round(start,3),"out_seconds":round(end,3),"props":{**m["props"],"dur":round(m["duration"]+GAP,3)}})
        cues.extend(caption_cues(m["narration"],start,end)); t=end+GAP
    props={"cuts":cuts,"captions":cues,"audio":{"narration":{"src":f"{PREFIX}/{ch}.wav","volume":1.0}}}
    json.dump(props,open(os.path.join(ROOT,"artifacts",f"{ch}.json"),"w"),ensure_ascii=False,indent=2)
    print(f"{ch}: total {t-GAP:.2f}s ({(t-GAP)/60:.2f} min), {len(cuts)} scenes, {len(cues)} cues")

if __name__=="__main__":
    for ch in (sys.argv[1:] or list(CHAPTERS.keys())): build_chapter(ch)
