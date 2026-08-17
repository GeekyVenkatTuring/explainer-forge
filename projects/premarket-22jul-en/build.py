#!/usr/bin/env python3
"""Pre-Market Brief (ENGLISH) — 22 July 2026. Reuses `sm` scene set. English TTS + English frames.
Verified: US close 21 Jul (Dow +0.74%/52,224.64, S&P +0.89%/7,509.20, Nasdaq +1.29%/25,837.21),
GIFT Nifty ~24,120, prev close Sensex 77,470 (-238)/Nifty 24,188, Brent ~$90, Nifty 22-Jul range
24,050-24,350 (support 24,050-24,100, resistance 24,300-24,350). Results 22 Jul: IndusInd Bank,
Nestle India, Dr Reddy's, BPCL, HPCL, Adani Power, Adani Green, Eternal, United Spirits, JSW Energy,
SRF, Tata Comm, Nippon Life AMC, Schaeffler, HFCL +54 firms. Sources: CNBC/TheStreet/Yahoo (US),
Business Standard/Upstox (results), EquityPandit (GIFT Nifty), Choice (levels).
WATCHLIST/SETUP, not a prediction; not investment advice.
Usage: python3 build.py            |   python3 build.py pm22e
"""
import json, os, re, subprocess, sys, time

VOICE = "en-IN-NeerjaNeural"; RATE = "-4%"; GAP = 0.5; PAUSE = 0.55; PREFIX = "sm"
ROOT = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(ROOT, "..", ".."))
PUBLIC = os.path.join(REPO, "composer", "public", PREFIX); RAW = os.path.join(ROOT, "assets", "raw"); FIN = os.path.join(ROOT, "assets")
for d in (PUBLIC, RAW, os.path.join(ROOT, "artifacts"), os.path.join(ROOT, "renders")):
    os.makedirs(d, exist_ok=True)

CHAPTERS = {
 "pm22e": [
 ("pm_title", "sm_ptitle",
  {"title": "Pre-Market Brief", "sub": "July 22, 2026 · Wednesday · before the open", "kicker": "PRE-MARKET · 22 JUL 2026"},
  "Good morning. It's Wednesday, July twenty-second — and here's your setup before the market opens. [pause] "
  "We'll cover the overnight global cues, the stocks and sectors in focus, the big results due today, and the key Nifty levels to watch. [pause] "
  "One important note up front — this is a watchlist and a setup, not a prediction of which stocks will go up. It's information, not investment advice."),
 ("pm_global", "sm_stats",
  {"kicker": "OVERNIGHT — WALL STREET RALLIED", "title": "Global Cues — a Positive Lead",
   "stats": [
    {"label": "Nasdaq", "to": 25837, "prefix": "", "suffix": "", "color": "#34D399", "sub": "+1.29% · chips surged"},
    {"label": "Dow Jones", "to": 52225, "prefix": "", "suffix": "", "color": "#34D399", "sub": "+0.74% · 3M, GM beat"},
    {"label": "GIFT Nifty", "to": 24120, "prefix": "", "suffix": "", "color": "#22D3EE", "sub": "+ firm open indicated"},
   ],
   "note": "Wall Street snapped a 3-day losing streak, led by technology — a tailwind for Indian IT. But Brent crude near $90 stays the key risk."},
  "First, the overnight cues — and they're positive. [pause] "
  "Wall Street rallied and snapped a three-day losing streak. The tech-heavy Nasdaq jumped one point three percent as semiconductor stocks surged. The Dow rose zero point seven four percent, helped by earnings beats — 3M up seven percent, General Motors up five. [pause] "
  "GIFT Nifty was trading around twenty-four thousand one hundred; combined with that strong US close, it points to a firm-to-positive open for our market. [pause] "
  "The tech strength is a tailwind for Indian IT after its recent weakness. But one thing hasn't changed — Brent crude near ninety dollars remains the key risk to watch."),
 ("pm_focus", "sm_iconcards",
  {"kicker": "STOCKS & SECTORS IN FOCUS", "title": "What to Watch at the Open", "color": "#22D3EE",
   "items": [
    {"emoji": "💻", "k": "IT — TCS, Infosys", "v": "Nasdaq +1.3% overnight → a likely tailwind for Indian IT after its recent weak run", "chip": "TAILWIND"},
    {"emoji": "🏍️", "k": "Autos — TVS, Bajaj", "v": "TVS at an all-time-high Q1 (stock +6%); Bajaj +46% PAT — watch the whole auto pack react", "chip": "EARNINGS"},
    {"emoji": "🛢️", "k": "OMCs — BPCL, HPCL", "v": "Both report today; crude near $90 pressures marketing margins — the crude-sensitive names", "chip": "CRUDE"},
    {"emoji": "🏦", "k": "Financials — IndusInd", "v": "IndusInd Bank Q1 today after the sector's NIM worries; Bandhan & M&M Fin beat yesterday", "chip": "IN FOCUS"},
   ]},
  "Now, the stocks and sectors in focus at the open. [pause] "
  "First — I-T. With the Nasdaq up one point three percent overnight, TCS, Infosys and the I-T pack could see a tailwind after their recent weakness. [pause] "
  "Second — autos. TVS Motor posted an all-time-high quarterly profit and its stock jumped six percent; Bajaj Auto's profit rose forty-six percent. Watch the whole auto ecosystem react. [pause] "
  "Third — the oil marketing companies, B-P-C-L and H-P-C-L. Both report today, and with crude near ninety dollars, their marketing margins are under the spotlight. [pause] "
  "Fourth — financials. IndusInd Bank reports today, closely watched after HDFC and Axis margin misses hit the sector. Bandhan Bank and M&M Financial both beat yesterday."),
 ("pm_results", "sm_iconcards",
  {"kicker": "BIG RESULTS DUE TODAY (~54 FIRMS)", "title": "Earnings to Watch Today", "color": "#FBBF24",
   "items": [
    {"emoji": "🏦", "k": "IndusInd Bank", "v": "Private-bank Q1 — the day's most-watched result after HDFC & Axis margin misses", "chip": "BANK"},
    {"emoji": "🍫", "k": "Nestle India · United Spirits", "v": "FMCG bellwethers — volume growth and rural demand in focus", "chip": "FMCG"},
    {"emoji": "💊", "k": "Dr Reddy's · SRF", "v": "Pharma after Cipla's weak day; SRF for the chemicals read-through", "chip": "PHARMA / CHEM"},
    {"emoji": "⚡", "k": "Adani Power · Adani Green · Eternal", "v": "Adani power pack + Eternal (Zomato) — the high-beta movers of the day", "chip": "HIGH BETA"},
   ]},
  "Today is another huge earnings day — over fifty-four companies report. Here are the big ones. [pause] "
  "IndusInd Bank — likely the day's most important result. After HDFC and Axis missed on margins, the market wants to see if the private-bank stress is spreading. [pause] "
  "Nestle India and United Spirits — F-M-C-G bellwethers. Watch volume growth and rural demand. [pause] "
  "Doctor Reddy's and S-R-F — pharma, especially after Cipla's weak day, and S-R-F for a read on chemicals. [pause] "
  "And the high-beta names — Adani Power, Adani Green, and Eternal, the company behind Zomato. These can move sharply on their numbers. Others reporting include Tata Communications, J-S-W Energy, and Nippon Life A-M-C."),
 ("pm_levels", "sm_myths",
  {"kicker": "THE SETUP · A TUG OF WAR", "title": "Headwinds vs Tailwinds Today", "mythLabel": "⚠️ HEADWINDS", "factLabel": "✅ TAILWINDS",
   "pairs": [
    {"m": "Brent crude near $90 (Middle East tension)", "f": "Strong US close — Nasdaq +1.3% boosts IT"},
    {"m": "Nifty fell 2 straight days; FIIs selling", "f": "Midcaps in the green — breadth stays positive"},
    {"m": "Heavy earnings = sharp single-stock swings", "f": "Nifty holding key support near 24,050"},
   ]},
  "So what's the overall setup? It's a tug of war. [pause] "
  "On the headwind side — Brent crude near ninety dollars on Middle East tension, the Nifty falling two days in a row, and foreign investors selling. [pause] "
  "On the tailwind side — a strong US close with the Nasdaq up one point three percent lifting I-T, positive market breadth with midcaps in the green, and the Nifty still holding key support. [pause] "
  "For levels — watch support at twenty-four thousand fifty to twenty-four thousand one hundred, and resistance at twenty-four thousand three hundred to three fifty. The outlook is sideways-to-bullish, with the range between twenty-four thousand fifty and twenty-four thousand three fifty."),
 ("pm_take", "sm_checklist",
  {"kicker": "HOW TO APPROACH THE OPEN", "title": "5 Things to Remember", "color": "#34D399", "icon": "💡",
   "items": [
    "This is a watchlist & setup — NOT a prediction of which stocks will rise",
    "GIFT Nifty points to a firm open — let the first 15 minutes settle",
    "Nifty range: ~24,050 support · ~24,350 resistance",
    "Earnings today = sharp single-stock moves; use stop-losses",
    "Key swing factors: crude near $90, and IT's reaction to Nasdaq",
   ]},
  "Finally, five things to remember as the market opens. [pause] "
  "One — this is a watchlist and a setup, not a prediction of which stocks will rise. Nobody can promise that. [pause] "
  "Two — GIFT Nifty points to a firm open, but let the first fifteen minutes settle before acting on any gap. [pause] "
  "Three — keep the Nifty range in mind: around twenty-four thousand fifty as support, twenty-four thousand three fifty as resistance. [pause] "
  "Four — with so many earnings today, expect sharp single-stock moves. Always use a stop-loss. [pause] "
  "Five — the two swing factors today are crude near ninety dollars, and how I-T reacts to that strong Nasdaq lead."),
 ("pm_recap", "sm_recap",
  {"title": "22 July — Pre-Market at a Glance",
   "items": [
    "US up: Nasdaq +1.3%, Dow +0.7% — a tech tailwind",
    "GIFT Nifty: firm-to-positive open indicated",
    "Focus: IT (US boost), autos (earnings), OMCs (crude)",
    "Results today: IndusInd, Nestle, Dr Reddy's, BPCL, Adani pack",
    "Nifty: ~24,050 support · ~24,350 resistance",
   ],
   "closer": "A watchlist, not a forecast — trade the reaction, not the prediction."},
  "July twenty-second, pre-market at a glance. [pause] "
  "US markets rose — Nasdaq up one point three percent, Dow up zero point seven — a tech tailwind. [pause] "
  "GIFT Nifty points to a firm-to-positive open. [pause] "
  "In focus — I-T on the US boost, autos on earnings, and the oil marketing companies on crude. [pause] "
  "Today's big results — IndusInd Bank, Nestle, Doctor Reddy's, B-P-C-L, and the Adani pack. [pause] "
  "And the levels — Nifty support near twenty-four thousand fifty, resistance near twenty-four thousand three fifty. [pause] "
  "Remember — this is a watchlist, not a forecast. Trade the reaction, not the prediction. [pause] "
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
