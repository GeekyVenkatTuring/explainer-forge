#!/usr/bin/env python3
"""Q1 FY27 Earnings Day (ENGLISH) — 21 July 2026. English TTS + English frames.
Reuses the parameterized `sm` scene set. Data verified in
../earnings-21jul-te/research/earnings-21jul2026.md. Info aggregation, not advice.
Usage: python3 build.py            (all)   |   python3 build.py er21e
"""
import json, os, re, subprocess, sys, time

VOICE = "en-IN-NeerjaNeural"; RATE = "-4%"; GAP = 0.5; PAUSE = 0.55; PREFIX = "sm"
ROOT = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(ROOT, "..", ".."))
PUBLIC = os.path.join(REPO, "composer", "public", PREFIX); RAW = os.path.join(ROOT, "assets", "raw"); FIN = os.path.join(ROOT, "assets")
for d in (PUBLIC, RAW, os.path.join(ROOT, "artifacts"), os.path.join(ROOT, "renders")):
    os.makedirs(d, exist_ok=True)

CHAPTERS = {
 "er21e": [
 ("er_title", "sm_ptitle",
  {"title": "Today's Q1 Results", "sub": "July 21, 2026 · ~45 companies reported Q1 · Analysis", "kicker": "EARNINGS DAY · 21 JUL 2026"},
  "July twenty-first — a huge earnings day. Around forty-five companies reported their first-quarter results. [pause] "
  "Whose profit jumped, whose fell, and what's the story behind each number — let's break it all down. [pause] "
  "One key point — all these results are compared with the same quarter last year, that is, year-on-year. "
  "This is information analysis only — not investment advice."),
 ("er_score", "sm_stats",
  {"kicker": "TOP BEATS · NET PROFIT (YoY)", "title": "Today's Top 3 — Net Profit",
   "stats": [
    {"label": "Bajaj Auto", "to": 3226, "prefix": "₹", "suffix": " Cr", "color": "#34D399", "sub": "+46% YoY*"},
    {"label": "TVS Motor", "to": 1058, "prefix": "₹", "suffix": " Cr", "color": "#34D399", "sub": "+65% · all-time Q1 high"},
    {"label": "M&M Financial", "to": 927, "prefix": "₹", "suffix": " Cr", "color": "#34D399", "sub": "+75% YoY"},
   ],
   "note": "Autos and financials shone today. *But there's a reason behind Bajaj Auto's number — we'll get to it."},
  "First, today's top three profits. [pause] "
  "Number one — Bajaj Auto. Net profit of three thousand two hundred twenty-six crore — up forty-six percent from last year. [pause] "
  "Number two — TVS Motor. Profit of one thousand fifty-eight crore — up sixty-five percent. This is the highest quarterly profit in the company's history. [pause] "
  "Number three — Mahindra and Mahindra Financial. Profit of nine hundred twenty-seven crore — surging seventy-five percent. [pause] "
  "Autos and financials led today. But there's an important reason behind Bajaj Auto's number — we'll look at it shortly."),
 ("er_beats", "sm_iconcards",
  {"kicker": "THE BIG BEATS", "title": "Strong Results — 4 Companies", "color": "#34D399",
   "items": [
    {"emoji": "🏍️", "k": "Bajaj Auto", "v": "Profit ₹3,226 Cr (+46%), revenue ₹21,689 Cr (+65%) — but boosted by a consolidation change", "chip": "*OPTICAL"},
    {"emoji": "🛵", "k": "TVS Motor", "v": "Profit ₹1,058 Cr (+65%) — all-time Q1 high; EV sales +86%; stock rose +6%", "chip": "BIG BEAT"},
    {"emoji": "🚜", "k": "M&M Financial", "v": "Profit ₹927 Cr (+75%); disbursements ₹15,560 Cr (+21%); AUM ₹1.37 lakh Cr (+12%)", "chip": "+75%"},
    {"emoji": "🏦", "k": "Bandhan Bank", "v": "Profit ₹502 Cr (+35%) — lower provisions; NII ₹2,921 Cr (+6%); NIM 6.2%", "chip": "+35%"},
   ]},
  "Now the four strong results in detail. [pause] "
  "First — Bajaj Auto. Net profit three thousand two hundred twenty-six crore, revenue twenty-one thousand six hundred eighty-nine crore — up sixty-five percent. But this big jump came from a consolidation change — more on that soon. [pause] "
  "Second — TVS Motor. Profit one thousand fifty-eight crore, up sixty-five percent — an all-time Q1 high. Electric vehicle sales rose eighty-six percent. After the results, the stock jumped six percent. [pause] "
  "Third — M&M Financial. Profit nine hundred twenty-seven crore, up seventy-five percent. Disbursements rose twenty-one percent and assets twelve percent. [pause] "
  "Fourth — Bandhan Bank. Profit five hundred two crore, up thirty-five percent — driven by lower provisions and better asset quality. Its net interest margin was six point two percent."),
 ("er_more", "sm_iconcards",
  {"kicker": "MORE RESULTS", "title": "More Company Results", "color": "#22D3EE",
   "items": [
    {"emoji": "📞", "k": "Sagility", "v": "Revenue ₹2,024 Cr (+27.6%); net profit +73.5% — healthcare BPO strong", "chip": "+73.5%"},
    {"emoji": "💻", "k": "NIIT", "v": "Revenue +14%; net profit +85% — skilling and training demand", "chip": "+85%"},
    {"emoji": "🛒", "k": "IndiaMART", "v": "Revenue ₹414 Cr (+11.4%); profit ₹172 Cr (+12%) — steady B2B growth", "chip": "+12%"},
    {"emoji": "🧪", "k": "Anthem Biosciences", "v": "Profit ₹120 Cr; revenue ₹418 Cr — pharma services / CDMO", "chip": "NEW LISTING"},
   ]},
  "Many more companies reported too. Let's look at four important ones. [pause] "
  "First — Sagility, a healthcare BPO company. Revenue two thousand twenty-four crore, up nearly twenty-eight percent. Profit rose seventy-three point five percent. [pause] "
  "Second — NIIT. Revenue rose fourteen percent, but profit surged eighty-five percent, driven by skilling and training demand. [pause] "
  "Third — IndiaMART, the B2B online marketplace. Revenue four hundred fourteen crore, profit one hundred seventy-two crore — a steady twelve percent growth. [pause] "
  "Fourth — Anthem Biosciences, a recently listed pharma services company. Profit one hundred twenty crore, revenue four hundred eighteen crore."),
 ("er_lesson", "sm_myths",
  {"kicker": "READ BEYOND THE HEADLINE", "title": "Numbers Aren't as Simple as They Look",
   "pairs": [
    {"m": "Bajaj Auto revenue +65% — amazing growth!", "f": "No — it's from a consolidation change; the numbers aren't comparable to last year. Organic growth is far lower"},
    {"m": "JSW Infra profit fell 10% = a bad result", "f": "Profit ₹347 Cr — but funds were diverted to future-growth capex, plus higher tax. It's not a demand problem"},
    {"m": "Comparing QoQ (vs last quarter) is enough", "f": "Seasonality makes QoQ misleading — YoY, versus the same quarter last year, is the right comparison"},
   ]},
  "Here's today's most important lesson — numbers are never as simple as they look. [pause] "
  "First myth — Bajaj Auto's revenue rose sixty-five percent, so it's amazing. No. The company folded a foreign subsidiary into its accounts — a consolidation change. So the numbers can't be compared directly with last year. The real organic growth is much lower. [pause] "
  "Second myth — JSW Infrastructure's profit fell ten percent, so it's a bad company. No. The profit fell because it diverted surplus cash to building new projects for future growth, and paid more tax. This isn't a demand problem — it's a deliberate investment. [pause] "
  "Third myth — comparing with last quarter, that is QoQ, is enough. But most businesses have a seasonal effect — festivals, summer. So comparing with the same quarter last year, year-on-year, is the correct analysis."),
 ("er_take", "sm_checklist",
  {"kicker": "HOW TO READ ANY RESULT", "title": "How to Read Any Result", "color": "#34D399", "icon": "💡",
   "items": [
    "Four numbers: revenue, net profit, margin, management guidance",
    "Always compare year-on-year (same quarter last year) — not QoQ",
    "Check if the headline % hides a one-time or consolidation effect",
    "A good result can still fall short of expectations — stock may drop",
    "One quarter isn't the story — the trend and consistency matter",
   ]},
  "So how should you read any result? Five rules. [pause] "
  "One — look at four numbers: revenue, net profit, margin, and management guidance. [pause] "
  "Two — always compare with the same quarter last year, that is year-on-year, not with the previous quarter. [pause] "
  "Three — check whether the headline percentage hides a one-time gain or a consolidation change — like Bajaj Auto. [pause] "
  "Four — even a good result can fall short of market expectations, and the stock may drop. [pause] "
  "Five — one quarter isn't the whole story. It's the trend and consistency over several quarters that really matter."),
 ("er_recap", "sm_recap",
  {"title": "Today's Results — At a Glance",
   "items": [
    "Strong: TVS (+65%), M&M Fin (+75%), Bandhan (+35%)",
    "Bajaj Auto +46% — but a consolidation effect*",
    "More: Sagility +73.5%, NIIT +85%, IndiaMART +12%",
    "Fell: JSW Infra −10% (due to capex)",
    "Lesson: read YoY, and the story behind the headline",
   ],
   "closer": "It's not the numbers — it's the story behind them that's the real analysis."},
  "Today's results, at a glance. [pause] "
  "The strong ones — TVS Motor up sixty-five percent, M&M Financial seventy-five percent, Bandhan Bank thirty-five percent. [pause] "
  "Bajaj Auto rose forty-six percent — but that was from a consolidation change. [pause] "
  "More — Sagility seventy-three point five, NIIT eighty-five, IndiaMART twelve percent. [pause] "
  "The one that fell — JSW Infrastructure, down ten percent, but because of capex. [pause] "
  "The lesson — always look year-on-year, and read the real story behind the headline percentage. [pause] "
  "It's not the numbers — it's the story behind them that is the real analysis. [pause] "
  "This information is aggregated from public sources — for analysis only, not investment advice. Please consult an expert before making decisions. Thanks for watching."),
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
