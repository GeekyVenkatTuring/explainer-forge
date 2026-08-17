#!/usr/bin/env python3
"""Post-Market Recap (ENGLISH) — 30 July 2026. Reuses `sm` scene set. English TTS + English frames.
Story: a QUIET GREEN day — but read the breadth. The index rose, yet midcaps, smallcaps and realty
closed RED. A narrow, large-cap / auto-led rally, not a broad one.

VERIFIED close (triangulated: Business Standard live blog + Prokerala, both independent, + prior-day
chain consistency; index figures to 2 decimals, NO ROUNDING):
  Sensex 77,928.15  (+273.55 pts, +0.35%)   [prev close 77,654.60]
  Nifty 50 24,317.15 (+66.95 pts, +0.28%)    [prev close 24,250.20]
  Nifty Realty -2.06% (day's weakest sector) · Nifty Midcap -0.35% · Nifty Smallcap -0.56%
  Leaders: Auto, Oil & Gas, Consumer Durables outperformed. Top Nifty gainers NAMED: M&M, Coal India,
  Eicher Motors. Global cue: US Fed HELD rates. Overhang: West Asia geopolitics kept trade watchful/subdued.

NOT reliably verifiable from web (contradictory sources — deliberately EXCLUDED, no fabricated decimals):
  Bank Nifty exact %, individual gainer/loser 2-decimal moves, today's FII/DII, Brent/WTI, rupee.
  Named laggards (Adani Ports, IndiGo, Bajaj Finserv, BEL) mentioned WITHOUT any % (single-source).
Sources: Business Standard (30 Jul live close), Prokerala (30 Jul), Goodreturns (Fed-hold outlook),
HDFCSky (28 Jul context). Info/analysis only, NOT investment advice.
Usage: python3 build.py            |   python3 build.py po30e
"""
import json, os, re, subprocess, sys, time

VOICE = "en-IN-NeerjaNeural"; RATE = "-4%"; GAP = 0.5; PAUSE = 0.55; PREFIX = "sm"
ROOT = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(ROOT, "..", ".."))
PUBLIC = os.path.join(REPO, "composer", "public", PREFIX); RAW = os.path.join(ROOT, "assets", "raw"); FIN = os.path.join(ROOT, "assets")
for d in (PUBLIC, RAW, os.path.join(ROOT, "artifacts"), os.path.join(ROOT, "renders")):
    os.makedirs(d, exist_ok=True)

CHAPTERS = {
 "po30e": [
 ("po_title", "sm_ptitle",
  {"title": "Post-Market Recap", "sub": "July 30, 2026 · a quiet green day — but read the breadth", "kicker": "POST-MARKET · 30 JUL 2026"},
  "The Indian market closed higher today — the Sensex and Nifty both finishing in the green after the US Federal Reserve left interest rates unchanged. [pause] "
  "But here's the twist most headlines will miss: this was NOT a broad rally. While the big indices rose, the wider market — midcaps, smallcaps, and real estate — actually closed red. [pause] "
  "So the real question isn't just did the market go up. It's who went up, who didn't, and what that gap is quietly telling us. "
  "Let's break down exactly what happened on July thirtieth. This is information analysis, not investment advice."),
 ("po_snap", "sm_stats",
  {"kicker": "INDEX SNAPSHOT", "title": "Closing Numbers — 30 July",
   "stats": [
    {"label": "SENSEX", "to": 77928.15, "decimals": 2, "prefix": "", "suffix": "", "color": "#34D399", "sub": "+273.55 pts · +0.35%"},
    {"label": "NIFTY 50", "to": 24317.15, "decimals": 2, "prefix": "", "suffix": "", "color": "#34D399", "sub": "+66.95 · +0.28%"},
    {"label": "NIFTY REALTY", "to": 2.06, "decimals": 2, "prefix": "−", "suffix": "%", "color": "#FB7185", "sub": "day's WEAKEST sector"},
   ],
   "note": "The headline is green — but the third box is the real story: Realty fell 2.06%, and BOTH midcaps and smallcaps closed red. A narrow rally, not a broad one."},
  "First, the scoreboard — and notice the colours. [pause] "
  "The Sensex rose two hundred seventy-three point five five points to close at seventy-seven thousand nine hundred twenty-eight point one five — up zero point three five percent. [pause] "
  "The Nifty added sixty-six point nine five points to twenty-four thousand three hundred seventeen point one five — up zero point two eight percent. [pause] "
  "But now look at the third box — the Nifty Realty index. It FELL two point zero six percent, the weakest sector of the day. And it wasn't alone: the midcap index slipped zero point three five percent, and the smallcap index dropped zero point five six percent. [pause] "
  "So while the front-page number is green, the market underneath it was mostly red. That divergence — big indices up, broad market down — is the single most important clue on this whole slide."),
 ("po_why", "sm_iconcards",
  {"kicker": "WHY THE INDEX ROSE", "title": "What Lifted the Large-Caps", "color": "#34D399",
   "items": [
    {"emoji": "🏦", "k": "The Fed held rates", "v": "The US Federal Reserve kept interest rates unchanged — a steady, risk-friendly global cue that supported equities at the open", "chip": "GLOBAL CUE"},
    {"emoji": "🚗", "k": "Autos led the charge", "v": "The Nifty Auto index was among the top-performing sectors, with heavyweights like M&M and Eicher doing the heavy lifting", "chip": "AUTO LED"},
    {"emoji": "🛢️", "k": "Oil & gas + durables joined", "v": "Nifty Oil & Gas and Consumer Durables also outperformed — a rotation into large, index-heavy names", "chip": "HEAVYWEIGHTS"},
    {"emoji": "🌍", "k": "But West Asia capped it", "v": "Investors stayed watchful of the geopolitical situation in West Asia, which kept the gains modest and trade subdued", "chip": "CAPPED"},
   ]},
  "So why did the large-cap indices rise? Three tailwinds — and one brake. [pause] "
  "First, the US Federal Reserve held interest rates steady. When the world's most important central bank signals stability, it's a risk-friendly cue that tends to support equities globally. [pause] "
  "Second, autos led the charge. The Nifty Auto index was among the day's top sectors, with heavyweights like Mahindra and Mahindra and Eicher Motors doing the heavy lifting. [pause] "
  "Third, oil and gas and consumer durables joined in — a clear rotation into large, index-heavy names. [pause] "
  "But there was a brake: investors stayed watchful of the geopolitical situation in West Asia. That caution is exactly why the gains were modest — under half a percent — and the mood stayed subdued rather than euphoric."),
 ("po_leaders", "sm_iconcards",
  {"kicker": "WHAT LED", "title": "Where the Money Went", "color": "#34D399",
   "items": [
    {"emoji": "🚜", "k": "M&M — top Nifty gainer", "v": "Mahindra & Mahindra led the index; autos were the standout sector as demand-sensitive large-caps found buyers", "chip": "AUTO"},
    {"emoji": "⛏️", "k": "Coal India", "v": "A large-cap PSU and a classic value / high-dividend name — the kind of heavyweight that lifts the index on a rotation day", "chip": "PSU"},
    {"emoji": "🏍️", "k": "Eicher Motors", "v": "The Royal Enfield maker rose with the auto pack — premium two-wheeler demand keeps it a market favourite", "chip": "AUTO"},
    {"emoji": "🛢️", "k": "Oil & Gas + Durables", "v": "Beyond single stocks, the Oil & Gas and Consumer Durables sectors outperformed — the leadership was large and defensive-cyclical", "chip": "SECTORS"},
   ]},
  "Now, where exactly did the money go? [pause] "
  "The top gainers on the Nifty were Mahindra and Mahindra, Coal India, and Eicher Motors. [pause] "
  "Notice the pattern. Mahindra and Eicher are autos — the standout sector today — as demand-sensitive large-caps found buyers. [pause] "
  "Coal India is a large-cap public-sector, high-dividend name — exactly the kind of index heavyweight that does well on a rotation day. [pause] "
  "And it wasn't just single stocks: the Oil and Gas and Consumer Durables sectors both outperformed. So the leadership was concentrated in large, index-heavy, cyclical names — which is precisely why the headline index rose even as the broader market fell."),
 ("po_breadth", "sm_iconcards",
  {"kicker": "LOOK UNDER THE HOOD", "title": "The Breadth Was Red", "color": "#FB7185",
   "items": [
    {"emoji": "🏗️", "k": "Realty −2.06%", "v": "Real estate was the worst-performing sector by a wide margin — rate-sensitive and the first to be sold when caution creeps in", "chip": "WORST SECTOR"},
    {"emoji": "📉", "k": "Midcaps −0.35%", "v": "The Nifty Midcap index closed lower even as the Nifty 50 rose — money left the middle of the market", "chip": "RED"},
    {"emoji": "🔻", "k": "Smallcaps −0.56%", "v": "Smallcaps fell even more — the riskier, retail-favourite end of the market was sold the hardest", "chip": "RED"},
    {"emoji": "🧭", "k": "The laggards", "v": "Names like Adani Ports and IndiGo were among the heavyweights that lagged — but the real weakness was broad, not in any one stock", "chip": "NARROW UP"},
   ]},
  "But here's the part the headline hides — look under the hood, and the breadth was red. [pause] "
  "Real estate was the worst-performing sector, down two point zero six percent. Realty is highly rate-sensitive, and it's often the first thing sold when caution creeps in. [pause] "
  "The midcap index closed down zero point three five percent, and the smallcap index fell zero point five six percent — the riskier, retail-favourite end of the market was sold the hardest. [pause] "
  "Among heavyweights, names like Adani Ports and IndiGo were among the laggards — but the key point isn't any single stock. It's that far more stocks fell than rose. When the index is green but the broader market is red, it means the rally is being carried by just a handful of large names. That's a narrow advance — and narrow advances are worth watching."),
 ("po_reads", "sm_myths",
  {"kicker": "READ BEHIND THE HEADLINE", "title": "What It Looks Like vs What's Real", "mythLabel": "🧐 THE HEADLINE SAYS", "factLabel": "🔍 WHAT'S REALLY HAPPENING",
   "pairs": [
    {"m": "Market closed green — it was a strong, broad rally", "f": "Only large-caps rose; midcaps, smallcaps & realty fell. Breadth was red"},
    {"m": "The Fed held rates, so risk is fully back on", "f": "Gains were under 0.4% — West Asia caution kept the mood subdued"},
    {"m": "A green index means my portfolio should be up", "f": "If you hold mid/smallcaps, today you likely felt the opposite"},
   ]},
  "Let's read behind the headlines — because a green day like this can be quietly misleading. [pause] "
  "The headline says the market closed green, so it was a strong, broad rally. The reality: only the large-caps rose. Midcaps, smallcaps and realty all fell. The breadth was red. [pause] "
  "The headline says the Fed held rates, so risk is fully back on. The reality: the gains were under half a percent, because West Asia caution kept the mood subdued. Stability is not the same as euphoria. [pause] "
  "And the headline says a green index means my portfolio should be up. But if you own mostly midcaps and smallcaps, today you likely felt the opposite. That gap between the index and your holdings is exactly why breadth matters more than the headline."),
 ("po_take", "sm_checklist",
  {"kicker": "TAKEAWAYS", "title": "5 Lessons to Carry Forward", "color": "#34D399", "icon": "💡",
   "items": [
    "A green index isn't always a green market — check the breadth",
    "When midcaps & smallcaps lag the Nifty, the rally is narrow",
    "A Fed 'hold' is a steadying cue — not a green light to chase risk",
    "Realty & rate-sensitive sectors lead the fall when caution rises",
    "For SIP investors, a +0.3% day is noise — stay on schedule",
   ]},
  "So, five takeaways to carry forward. [pause] "
  "One — a green index is not always a green market. Always check the breadth: how many stocks actually rose versus fell. Today, the index and the market disagreed. [pause] "
  "Two — when midcaps and smallcaps lag the Nifty, the rally is narrow, carried by a few large names. Narrow rallies are more fragile than broad ones. [pause] "
  "Three — a Fed hold is a steadying signal, not a green light to chase risk. The subdued gains today show the market took it calmly, not greedily. [pause] "
  "Four — realty and other rate-sensitive sectors tend to lead the fall when caution rises. They're a useful early-warning gauge. [pause] "
  "And five — for a long-term S-I-P investor, a zero point three percent day, up or down, is just noise. Keep investing on your schedule and ignore the daily colour."),
 ("po_recap", "sm_recap",
  {"title": "30 July — At a Glance",
   "items": [
    "Sensex +273.55 (77,928.15) · Nifty +66.95 (24,317.15) — both green",
    "But breadth RED: Realty −2.06%, Midcaps −0.35%, Smallcaps −0.56%",
    "Lift: Fed held rates + autos, oil & gas, durables led",
    "Gainers: M&M, Coal India, Eicher · Laggards: realty & broad market",
    "Lesson: a narrow, large-cap rally — check breadth, not just the index",
   ],
   "closer": "Green on the surface, red underneath. A narrow rally is a reminder to look past the headline number."},
  "July thirtieth, at a glance. [pause] "
  "The Sensex rose two hundred seventy-three points to seventy-seven thousand nine hundred twenty-eight, and the Nifty sixty-seven points to twenty-four thousand three hundred seventeen — both closing green after the Fed held rates. [pause] "
  "But under the surface the breadth was red: realty fell two point zero six percent, and both midcaps and smallcaps closed lower. [pause] "
  "The lift came from autos, oil and gas, and consumer durables — with Mahindra, Coal India and Eicher among the top gainers, while the broader market and rate-sensitive sectors lagged. [pause] "
  "The lesson — this was a narrow, large-cap rally. Green on the surface, red underneath. Always look past the headline number to the breadth beneath it. [pause] "
  "This information is aggregated from public sources — for analysis only, not investment advice. Thanks for watching, and I'll see you at the next close."),
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
