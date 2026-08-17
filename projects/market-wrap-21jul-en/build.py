#!/usr/bin/env python3
"""Market Wrap (ENGLISH) — 21 July 2026 post-close. English TTS + English frames.
Reuses the parameterized `sm` scene set with English props. Data verified in
../market-wrap-21jul-te/research/wrap-21jul2026.md. Info aggregation, not advice.
Usage: python3 build.py            (all)   |   python3 build.py mw21e
"""
import json, os, re, subprocess, sys

VOICE = "en-IN-NeerjaNeural"; RATE = "-4%"; GAP = 0.5; PAUSE = 0.55; PREFIX = "sm"
ROOT = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(ROOT, "..", ".."))
PUBLIC = os.path.join(REPO, "composer", "public", PREFIX); RAW = os.path.join(ROOT, "assets", "raw"); FIN = os.path.join(ROOT, "assets")
for d in (PUBLIC, RAW, os.path.join(ROOT, "artifacts"), os.path.join(ROOT, "renders")):
    os.makedirs(d, exist_ok=True)

CHAPTERS = {
 "mw21e": [
 ("mw_title", "sm_ptitle",
  {"title": "Why Did the Market Fall?", "sub": "July 21, 2026 · Tuesday · Post-Market Analysis", "kicker": "MARKET WRAP · 21 JUL 2026"},
  "July twenty-first, twenty twenty-six — Tuesday. The market has closed for the day. [pause] "
  "For the second day running, the Nifty and Sensex fell. So what moved them today? [pause] "
  "We'll break down the closing numbers, the stocks that fell, and the sectors that rose. "
  "This is information analysis only — not investment advice."),
 ("mw_snap", "sm_stats",
  {"kicker": "INDEX SNAPSHOT", "title": "Closing Numbers — 21 July",
   "stats": [
    {"label": "SENSEX", "to": 77470, "prefix": "", "suffix": "", "color": "#FB7185", "sub": "−238 pts · −0.31%"},
    {"label": "NIFTY 50", "to": 24188, "prefix": "", "suffix": "", "color": "#FB7185", "sub": "−51 pts · −0.21%"},
    {"label": "BRENT CRUDE", "to": 88, "prefix": "$", "suffix": "+", "color": "#FBBF24", "sub": "Middle East · Hormuz fears"},
   ],
   "note": "Headline indices fell, but Midcap rose +0.3% and Smallcap +0.53% — breadth was positive. A narrow, large-cap-led dip, not a broad sell-off."},
  "First, the closing numbers. [pause] "
  "The Sensex fell two hundred thirty-eight points to close at 77,470 — down about a third of a percent. [pause] "
  "The Nifty 50 lost fifty-one points to settle at 24,188. This was its second straight losing session. [pause] "
  "But here's the crucial point — the Midcap index rose a third of a percent, and the Smallcap index gained more than half a percent. [pause] "
  "That means most stocks were actually in the green. This fall was limited to a handful of large stocks — it was not a broad sell-off."),
 ("mw_why", "sm_iconcards",
  {"kicker": "WHY IT FELL", "title": "Four Reasons for the Fall", "color": "#FB7185",
   "items": [
    {"emoji": "🛢️", "k": "Crude + Middle East", "v": "Houthis threatened a naval blockade on Saudi Arabia; Strait of Hormuz supply fears pushed Brent to ~$88–90", "chip": "MAIN CAUSE"},
    {"emoji": "💻", "k": "IT Weakness", "v": "TCS and Infosys each fell about 1% — Nifty IT was among the worst-hit sectors", "chip": "IT DRAG"},
    {"emoji": "🏦", "k": "PSU Banks + HDFC", "v": "Nifty PSU Bank fell the most; HDFC Bank and SBI weakness dragged the index", "chip": "WEIGHTAGE"},
    {"emoji": "📤", "k": "FII Selling", "v": "Foreign investors stayed net sellers; risk-off sentiment across global markets", "chip": "NET SELLERS"},
   ]},
  "So why did it fall? Four reasons. [pause] "
  "The most important — crude oil and Middle East tension. [pause] "
  "Yemen's Houthis threatened a naval blockade on Saudi Arabia. That raised fears over oil supply through the Strait of Hormuz, pushing Brent crude to between eighty-eight and ninety dollars. Since India imports most of its oil, this pressures inflation and the rupee. [pause] "
  "Second — weakness in IT stocks. TCS and Infosys each fell about one percent. [pause] "
  "Third — PSU banks, HDFC Bank, and SBI. These high-weightage stocks dragged the Nifty down. [pause] "
  "Fourth — foreign institutions stayed net sellers, amid a risk-off mood across global markets."),
 ("mw_losers", "sm_iconcards",
  {"kicker": "TOP LOSERS", "title": "The Biggest Losers Today", "color": "#FB7185",
   "items": [
    {"emoji": "💊", "k": "Cipla", "v": "Worst Nifty performer — down about 2%; pharma and healthcare were weak today", "chip": "−2%"},
    {"emoji": "🏥", "k": "Dr Reddy's · Max Healthcare", "v": "Both fell more than 1% — healthcare sector under pressure", "chip": "−1%+"},
    {"emoji": "💻", "k": "TCS · Infosys", "v": "IT giants down ~1% each — weak global tech sentiment and the rupee", "chip": "−1%"},
    {"emoji": "🏦", "k": "HDFC Bank · SBI", "v": "High-weightage bank stocks — the losers that dragged the index most", "chip": "DRAG"},
   ]},
  "Now the biggest losers today, and the reasons behind them. [pause] "
  "First — Cipla. The worst Nifty performer, down about two percent. Pharma and healthcare stocks were weak across the board today. [pause] "
  "Second — Doctor Reddy's and Max Healthcare, both down more than one percent. [pause] "
  "Third — TCS and Infosys. These IT giants each fell about one percent, on weak global tech sentiment and rupee moves. [pause] "
  "Fourth — HDFC Bank and SBI. Because these carry the highest weightage in the index, even a small fall pulled the Nifty down noticeably."),
 ("mw_sectors", "sm_myths",
  {"kicker": "SECTOR SCOREBOARD", "title": "Sectors — Who Fell, Who Rose?", "mythLabel": "🔻 SECTORS THAT FELL", "factLabel": "🟢 SECTORS THAT ROSE",
   "pairs": [
    {"m": "Nifty PSU Bank — the worst-hit sector", "f": "Nifty Chemical — the top-gaining sector"},
    {"m": "Nifty IT — pressured by TCS, Infosys", "f": "Nifty Cement — defensive buying"},
    {"m": "FMCG — afternoon selling pressure", "f": "Midcap & Smallcap — in the green"},
   ]},
  "Let's look at today's sector scoreboard — who fell, and who rose? [pause] "
  "On the losing side — Nifty PSU Bank fell the most, followed by Nifty IT under pressure from TCS and Infosys. FMCG stocks also saw selling in the afternoon. [pause] "
  "On the winning side — the Nifty Chemical index rose the most, followed by Cement. When there's uncertainty, investors rotate into these defensive sectors. [pause] "
  "So while IT and banks fell, chemicals, cement, and midcaps rose. This is sector rotation — not a collapse of the whole market."),
 ("mw_lesson", "sm_myths",
  {"kicker": "THE KEY LESSON · CRUDE", "title": "Why Does Crude Oil Move the Market?",
   "pairs": [
    {"m": "Crude prices don't affect us", "f": "India imports ~85% of its oil — higher crude means a bigger import bill and inflation"},
    {"m": "Crude drags all stocks equally", "f": "No — bad for paints, airlines, autos; GOOD for oil producers like ONGC"},
    {"m": "This is India's own problem", "f": "No — it's driven by a global geopolitical event: Houthis and the Strait of Hormuz"},
   ]},
  "Here's the most important lesson from today — why does crude oil move the market? [pause] "
  "Many people think crude prices don't affect them. But India imports about eighty-five percent of its oil. When crude rises, the import bill, inflation, and pressure on the rupee all go up. [pause] "
  "But crude doesn't drag every stock equally. For paints, airlines, and auto companies it's bad news — crude is their raw material. But for oil producers like ONGC, it's actually good news. [pause] "
  "And one more key point — this isn't India's own problem. A global geopolitical event — the Houthis and the Strait of Hormuz — moved our market. Markets are always connected to the world."),
 ("mw_take", "sm_checklist",
  {"kicker": "TAKEAWAYS", "title": "5 Lessons from Today", "color": "#34D399", "icon": "💡",
   "items": [
    "Second down day, but breadth positive — a narrow, large-cap fall",
    "Crude near $90 = inflation and rupee pressure — keep watching it",
    "IT and banks fell while chemicals and cement rose — sector rotation",
    "Global news (Houthis, Hormuz) directly moves our market",
    "For SIP investors, a red day like this is noise — not a trend",
   ]},
  "Five lessons from today. [pause] "
  "One — even on a second down day, most stocks rose. This was a narrow, large-cap-led fall. [pause] "
  "Two — crude near ninety dollars raises inflation and rupee pressure. Keep an eye on it. [pause] "
  "Three — while IT and banks fell, chemicals and cement rose. This is sector rotation — money moving from one sector to another. [pause] "
  "Four — global news like the Houthis and Hormuz directly moves our market. Watch the world, not just India. [pause] "
  "Five — for regular SIP investors, one red day like this is just noise, not a long-term trend. Don't panic-sell."),
 ("mw_recap", "sm_recap",
  {"title": "21 July — At a Glance",
   "items": [
    "Sensex −238 (77,470) · Nifty −51 (24,188) — 2nd day down",
    "Cause: crude $90+ (Houthi/Hormuz) + IT + PSU Bank + FII selling",
    "Losers: Cipla, Dr Reddy's, TCS, Infosys, HDFC Bank, SBI",
    "Gainers: Chemical, Cement, Midcap, Smallcap",
    "Breadth positive — a narrow large-cap shock, not a market crash",
   ],
   "closer": "One red day isn't the whole story — long-term discipline wins."},
  "July twenty-first, at a glance. [pause] "
  "The Sensex fell two hundred thirty-eight points and the Nifty fifty-one — the second day down. [pause] "
  "The cause — crude crossing ninety dollars on Houthi and Hormuz fears, weakness in IT and PSU banks, and foreign investor selling. [pause] "
  "Cipla, Doctor Reddy's, TCS, Infosys, HDFC Bank, and SBI fell. Chemicals, cement, midcaps, and smallcaps rose. [pause] "
  "But breadth was positive — this was a narrow large-cap shock, not a market crash. [pause] "
  "One red day isn't the whole story — long-term discipline is what really wins. [pause] "
  "This information is aggregated from public sources — for analysis only, not investment advice. Please consult an expert before making decisions. Thanks for watching."),
 ],
}

def ffdur(path):
    out = subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","default=noprint_wrappers=1:nokey=1",path],capture_output=True,text=True,check=True)
    return round(float(out.stdout.strip()),3)

def tts_chunk(path, text):
    mp3 = path[:-4]+".mp3"
    for attempt in range(6):
        r = subprocess.run(["edge-tts","--voice",VOICE,f"--rate={RATE}","--text",text,"--write-media",mp3],capture_output=True)
        if r.returncode == 0 and os.path.exists(mp3) and os.path.getsize(mp3) > 0: break
        import time; time.sleep(3 + attempt*4)
    else: raise RuntimeError(f"edge-tts failed for {path}")
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
