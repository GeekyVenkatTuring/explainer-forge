#!/usr/bin/env python3
"""Pre-Market Brief (ENGLISH) — 23 July 2026. Reuses `sm` scene set. English TTS + English frames.
Verified data:
- 22 Jul close (3rd down day): Sensex -715.06 (-0.92%) 76,755.05; Nifty -191.45 (-0.79%) 23,996.25 (below 24k).
  Worst sectors: Media -2.68%, Realty -2.6%, PSU Bank -1.8%, IT -1.5%; pharma -up to 13% intraday.
- WHY it fell: US-Iran escalation -> Brent surged ~4% to $92-94 (5-wk high); Trump generic-drug tariff threat;
  weak rupee; FII -819cr & DII -418cr both net sellers.
- Overnight US (22 Jul close): Dow -0.01% 52,218; S&P -0.14% 7,498.96; Nasdaq -0.57% 25,690.90.
  After-hours: Alphabet -3% (raised capex), Tesla -4% (miss), IBM lower.
- THE TWIST (post-close): (1) Trump Truth Social clarifies generics EXEMPT 2 yrs from Aug 1 2026; 100% in 2028,
  200% in 2029 -> immediate India impact LIMITED (US=30%+ exports, India cost adv 40-60%). (2) Mediators tabled a
  10-day US-Iran ceasefire proposal -> crude swing factor.
- GIFT Nifty: cautious, marginally negative bias. Brent ~$91.5. Watch: Indiamart (Q1 PAT +12.18% to 172.2cr),
  Ather Energy (raised 1,300cr QIP), pharma pack (rebound candidates), OMCs (crude), Eternal/Nestle/Anant Raj.
Sources: HDFC Sky/The Week/Business Today (fall), Yahoo/Bloomberg (US), Business Standard (tariff detail),
CNBC (ceasefire), Goodreturns (outlook), Trendlyne (FII/DII).
Nifty levels approximate — 24,000 now the pivot to reclaim; framed qualitatively.
WATCHLIST/SETUP, not a prediction; not investment advice.
Usage: python3 build.py            |   python3 build.py pm23e
"""
import json, os, re, subprocess, sys, time

VOICE = "en-IN-NeerjaNeural"; RATE = "-4%"; GAP = 0.5; PAUSE = 0.55; PREFIX = "sm"
ROOT = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(ROOT, "..", ".."))
PUBLIC = os.path.join(REPO, "composer", "public", PREFIX); RAW = os.path.join(ROOT, "assets", "raw"); FIN = os.path.join(ROOT, "assets")
for d in (PUBLIC, RAW, os.path.join(ROOT, "artifacts"), os.path.join(ROOT, "renders")):
    os.makedirs(d, exist_ok=True)

CHAPTERS = {
 "pm23e": [
 ("pm_title", "sm_ptitle",
  {"title": "Pre-Market Brief", "sub": "July 23, 2026 · Thursday · before the open", "kicker": "PRE-MARKET · 23 JUL 2026"},
  "Good morning. It's Thursday, July twenty-third — and here's your setup before the market opens. [pause] "
  "Yesterday the market fell hard, so today we'll do three things — recap exactly why it dropped, look at what changed overnight, and then map the stocks, sectors and levels to watch. [pause] "
  "One important note up front — this is a watchlist and a setup, not a prediction of which stocks will go up. It's information, not investment advice."),
 ("pm_fall", "sm_stats",
  {"kicker": "YESTERDAY — A SHARP SELL-OFF", "title": "Where We Closed on July 22",
   "stats": [
    {"label": "Sensex", "to": 76755, "prefix": "", "suffix": "", "color": "#F87171", "sub": "-715 pts · -0.92%"},
    {"label": "Nifty 50", "to": 23996, "prefix": "", "suffix": "", "color": "#F87171", "sub": "-191 pts · below 24,000"},
    {"label": "FII selling", "to": 819, "prefix": "₹-", "suffix": " Cr", "color": "#FBBF24", "sub": "DII also sold ₹-418 Cr"},
   ],
   "note": "A third straight down day. What stung most: even domestic institutions were net sellers — nobody stepped in to buy the dip."},
  "First, let's be honest about yesterday. The market fell sharply — a third straight down day. [pause] "
  "The Sensex dropped seven hundred and fifteen points, nearly one percent, to seventy-six thousand seven fifty-five. The Nifty fell one hundred and ninety-one points and closed below the key twenty-four thousand mark, at twenty-three thousand nine ninety-six. [pause] "
  "And here's what stung most — it wasn't just foreign investors selling eight hundred and nineteen crore. Domestic institutions also sold four hundred and eighteen crore. Nobody stepped in to buy the dip. That's a sign of genuine caution."),
 ("pm_why", "sm_iconcards",
  {"kicker": "WHY IT FELL — TWO SHOCKS", "title": "The Reasons Behind the Drop", "color": "#F87171",
   "items": [
    {"emoji": "🛢️", "k": "Crude oil spiked", "v": "US–Iran conflict re-escalated; Brent surged ~4% past $92 to a five-week high — India's biggest macro risk", "chip": "GEOPOLITICS"},
    {"emoji": "💊", "k": "Pharma tariff scare", "v": "Trump floated a tariff on generic drug imports — some pharma names crashed up to 13% intraday", "chip": "PHARMA -13%"},
    {"emoji": "💱", "k": "Weak rupee + FII exit", "v": "A costlier oil bill pressured the rupee; foreign selling added to the risk-off mood", "chip": "RISK-OFF"},
   ]},
  "So why did it fall? Two overnight shocks, not anything wrong at home. [pause] "
  "The first, and biggest — crude oil. The U-S–Iran conflict re-escalated, and Brent crude surged about four percent, past ninety-two dollars, to a five-week high. Crude is India's single biggest macro vulnerability, because we import most of our oil. [pause] "
  "The second — a pharma scare. President Trump floated a tariff on generic drug imports, and some Indian pharma names crashed as much as thirteen percent intraday. [pause] "
  "Add a weakening rupee from that costlier oil bill, plus foreign investors selling, and you get broad-based, risk-off selling. And here's the lesson — when geopolitics and crude flare up, they override the charts. That's why yesterday's dip caught the setup off guard."),
 ("pm_overnight", "sm_stats",
  {"kicker": "OVERNIGHT — WALL STREET SOFTER", "title": "Global Cues This Morning",
   "stats": [
    {"label": "Nasdaq", "to": 25691, "prefix": "", "suffix": "", "color": "#F87171", "sub": "-0.57% · Alphabet, Tesla fell late"},
    {"label": "Dow Jones", "to": 52218, "prefix": "", "suffix": "", "color": "#FBBF24", "sub": "flat · -0.01%"},
    {"label": "Brent crude", "to": 92, "prefix": "$", "suffix": "", "color": "#FBBF24", "sub": "near a 5-week high"},
   ],
   "note": "GIFT Nifty points to a cautious, mildly negative open. After-hours: Alphabet -3% on higher capex, Tesla -4% on an earnings miss."},
  "Now, the overnight cues — and they're soft, but not scary. [pause] "
  "Wall Street closed mixed to lower. The Nasdaq slipped about half a percent, weighed down by oil, and the Dow was essentially flat. After the bell, two big names fell — Alphabet dropped three percent on higher spending plans, and Tesla fell four percent after missing estimates. [pause] "
  "Brent crude is still near ninety-two dollars, close to a five-week high — the number to keep watching all day. [pause] "
  "Put together, GIFT Nifty points to a cautious, mildly negative open. But the story doesn't end there — because two things changed overnight."),
 ("pm_twist", "sm_myths",
  {"kicker": "THE OVERNIGHT TWIST", "title": "Both Shocks Just Softened", "mythLabel": "⚠️ YESTERDAY'S FEAR", "factLabel": "✅ OVERNIGHT RELIEF",
   "pairs": [
    {"m": "Pharma tariff = 200% wall, exports doomed", "f": "Generics EXEMPT 2 years (from Aug 1); 100% only in 2028"},
    {"m": "US–Iran war escalating, crude spiking further", "f": "Mediators tabled a 10-day ceasefire proposal"},
    {"m": "India pharma loses its US market", "f": "India's 40–60% cost edge makes reshoring uneconomic"},
   ]},
  "Here's the twist — and it matters. Both of the shocks that sank the market yesterday actually eased after the close. [pause] "
  "On pharma — the fine print of Trump's own statement gives generic medicines a two-year exemption, starting August first. The steep tariffs only kick in from twenty twenty-eight. So the immediate hit to Indian pharma is limited, and India's forty-to-sixty percent cost advantage means shifting that manufacturing to America simply isn't economical. Yesterday's thirteen-percent crash now looks overdone. [pause] "
  "On oil — regional mediators have put a ten-day ceasefire proposal on the table for the U-S and Iran. If it gains traction, crude cools, and the whole market breathes easier. Nothing is settled — but the panic case is softer this morning than it was last night."),
 ("pm_focus", "sm_iconcards",
  {"kicker": "STOCKS & SECTORS IN FOCUS", "title": "What to Watch at the Open", "color": "#22D3EE",
   "items": [
    {"emoji": "💊", "k": "Pharma — Sun, Cipla, Dr Reddy's", "v": "The 2-year exemption eases the tariff fear — the most likely rebound candidates after yesterday's crash", "chip": "REBOUND?"},
    {"emoji": "🛢️", "k": "OMCs — BPCL, HPCL, IOC", "v": "Hostage to crude. Ceasefire progress = relief; strikes continuing = more pressure", "chip": "CRUDE"},
    {"emoji": "📈", "k": "Indiamart Intermesh", "v": "Strong Q1 — net profit up 12% to ₹172 cr, revenue up 11% — a bright spot in earnings", "chip": "Q1 BEAT"},
    {"emoji": "🔋", "k": "Ather Energy", "v": "EV maker raised ₹1,300 cr via a QIP — in focus on the fresh capital", "chip": "QIP"},
   ]},
  "So what should you actually watch at the open? [pause] "
  "First — pharma. With that two-year exemption easing the tariff fear, Sun Pharma, Cipla, Doctor Reddy's and the generics pack are the most likely rebound candidates after yesterday's crash. Watch whether buyers step back in. [pause] "
  "Second — the oil marketing companies, B-P-C-L, H-P-C-L and I-O-C. They're hostage to crude. Progress on the ceasefire is relief; continued strikes mean more pressure. [pause] "
  "Third — earnings bright spots. Indiamart posted a strong quarter, profit up twelve percent to a hundred and seventy-two crore. And Ather Energy is in focus after raising thirteen hundred crore through a share sale. This is stock-specific season — the numbers, not the noise, will move individual names."),
 ("pm_results", "sm_iconcards",
  {"kicker": "BIG RESULTS DUE TODAY (~50 FIRMS)", "title": "Earnings to Watch Today", "color": "#FBBF24",
   "items": [
    {"emoji": "💻", "k": "Infosys — IT bellwether", "v": "The day's most-watched print; sets the tone for the whole IT pack after Wall Street's tech wobble", "chip": "IT"},
    {"emoji": "💊", "k": "Cipla — pharma", "v": "The first big pharma result right AFTER the tariff scare — read closely for any US generics hit", "chip": "PHARMA"},
    {"emoji": "✈️", "k": "IndiGo (InterGlobe)", "v": "Airline earnings with crude near $92 — jet-fuel cost is the number that matters", "chip": "CRUDE"},
    {"emoji": "🏢", "k": "Mphasis · Coromandel · Vishal Mega Mart · PVR INOX", "v": "IT, fertilizers, retail & media — the notable mid-cap movers of the day", "chip": "MID-CAPS"},
   ]},
  "Now — today is another huge earnings day. Around fifty companies report their June-quarter results, and a few tie directly to this morning's themes. [pause] "
  "The biggest is Infosys. As the I-T bellwether, its numbers and guidance set the tone for the whole tech pack — especially after the recent weakness on Wall Street. [pause] "
  "Then Cipla — and this one matters. It's the first major pharma result right after yesterday's tariff scare, so the market will study it closely for any hit to U-S generic sales. [pause] "
  "IndiGo, the airline, reports too — and with crude near ninety-two dollars, jet-fuel cost is the number to watch. [pause] "
  "Also on the list — Mphasis in I-T, Coromandel in fertilizers, Vishal Mega Mart in retail, and P-V-R I-N-O-X in media. Remember — in earnings season, react to the actual numbers, not to the pre-result hype."),
 ("pm_setup", "sm_myths",
  {"kicker": "THE SETUP · A TUG OF WAR", "title": "Headwinds vs Tailwinds Today", "mythLabel": "⚠️ HEADWINDS", "factLabel": "✅ TAILWINDS",
   "pairs": [
    {"m": "Brent crude near $92 — still elevated", "f": "Both overnight shocks softened after close"},
    {"m": "3 down days; FIIs AND DIIs selling", "f": "Pharma set up for a possible relief bounce"},
    {"m": "Nifty slipped below 24,000", "f": "Q1 earnings beats offering selective longs"},
   ]},
  "So what's the overall setup? It's a genuine tug of war. [pause] "
  "On the headwind side — Brent crude is still near ninety-two dollars, the market has fallen three days running, and both foreign and domestic institutions are selling. [pause] "
  "On the tailwind side — both overnight shocks have softened, pharma is set up for a possible relief bounce, and strong earnings like Indiamart offer selective opportunities. [pause] "
  "For levels — twenty-four thousand is now the line in the sand. The Nifty closed just below it, so reclaiming twenty-four thousand would be the first sign of stability; failing to, and the next support zone near twenty-three thousand eight hundred comes into play. The likely tone — cautious, and completely headline-driven by crude."),
 ("pm_take", "sm_checklist",
  {"kicker": "HOW TO APPROACH THE OPEN", "title": "5 Things to Remember", "color": "#34D399", "icon": "💡",
   "items": [
    "This is a watchlist & setup — NOT a prediction of which stocks will rise",
    "Crude is the master switch — watch Brent and the ceasefire headlines",
    "Pharma is the rebound to watch after the 2-year tariff exemption",
    "Nifty: reclaim 24,000 = stability; ~23,800 is next support",
    "Earnings season = sharp single-stock moves; always use a stop-loss",
   ]},
  "Finally, five things to remember as the market opens. [pause] "
  "One — this is a watchlist and a setup, not a prediction of which stocks will rise. Yesterday proved exactly why — an overnight shock can flip the whole picture. [pause] "
  "Two — crude is the master switch today. Keep one eye on Brent and any ceasefire headline out of West Asia. [pause] "
  "Three — pharma is the rebound to watch, now that the tariff has a two-year exemption. [pause] "
  "Four — on levels, reclaiming twenty-four thousand signals stability; below it, twenty-three thousand eight hundred is the next support. [pause] "
  "Five — with earnings season in full swing, expect sharp single-stock moves. Always use a stop-loss."),
 ("pm_recap", "sm_recap",
  {"title": "23 July — Pre-Market at a Glance",
   "items": [
    "Yesterday: Sensex -715, Nifty below 24,000 (3rd down day)",
    "Why: crude spike (US–Iran) + pharma tariff scare",
    "Overnight twist: BOTH shocks softened after close",
    "Focus: pharma (rebound?), OMCs (crude), Indiamart (Q1 beat)",
    "Results today: Infosys, Cipla, IndiGo + ~50 firms",
    "Nifty: reclaim 24,000 = stability · ~23,800 support",
   ],
   "closer": "The setup improved overnight — but crude runs the day. Trade the reaction, not the prediction."},
  "July twenty-third, pre-market at a glance. [pause] "
  "Yesterday was ugly — the Sensex fell seven hundred and fifteen points and the Nifty slipped below twenty-four thousand, a third straight down day. [pause] "
  "The cause — a crude spike from the U-S–Iran conflict, and a pharma tariff scare. [pause] "
  "But overnight, both of those shocks softened — a two-year pharma exemption, and a ceasefire proposal on the table. [pause] "
  "In focus today — pharma for a possible rebound, the oil companies on crude, and Indiamart on a strong quarter. [pause] "
  "On earnings — Infosys, Cipla and IndiGo lead around fifty results due today. [pause] "
  "And the level that matters — reclaiming twenty-four thousand would signal stability. [pause] "
  "Remember — the setup improved overnight, but crude runs the day. Trade the reaction, not the prediction. [pause] "
  "This information is aggregated from public sources — for analysis only, not investment advice. Have a great trading day, and thanks for watching."),
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
