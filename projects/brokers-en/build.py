#!/usr/bin/env python3
"""Broker Comparison (ENGLISH) — 2026. English TTS + English frames. Reuses `sm` scene set.
Data verified in ../brokers-te/research/brokers-2026.md. Neutral, not affiliated, not advice.
Usage: python3 build.py            (all)   |   python3 build.py bre
"""
import json, os, re, subprocess, sys, time

VOICE = "en-IN-NeerjaNeural"; RATE = "-4%"; GAP = 0.5; PAUSE = 0.55; PREFIX = "sm"
ROOT = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(ROOT, "..", ".."))
PUBLIC = os.path.join(REPO, "composer", "public", PREFIX); RAW = os.path.join(ROOT, "assets", "raw"); FIN = os.path.join(ROOT, "assets")
for d in (PUBLIC, RAW, os.path.join(ROOT, "artifacts"), os.path.join(ROOT, "renders")):
    os.makedirs(d, exist_ok=True)

CHAPTERS = {
 "bre": [
 ("br_title", "sm_ptitle",
  {"title": "Which Broker App Is Best?", "sub": "Zerodha · Groww · Angel One · Dhan · Upstox — 2026 Comparison", "kicker": "BROKER COMPARISON · 2026"},
  "To invest in stocks, mutual funds, or F&O, the first step is a broker app. But with so many apps, which one is best? [pause] "
  "In this video — the major brokers' commissions, their apps, the issues users have faced recently, and which app is best for what — we'll cover it all. [pause] "
  "One important note — this is not a promotion for any broker, and not investment advice. Charges change often — check the current rates in the app before you choose."),
 ("br_players", "sm_iconcards",
  {"kicker": "THE PLAYERS + CHARGES", "title": "The Major Brokers — Users & Charges", "color": "#22D3EE",
   "items": [
    {"emoji": "🟢", "k": "Groww", "v": "1.3 Cr users (#1) · delivery ₹20*, F&O ₹20, AMC ₹0 · *others give delivery free", "chip": "SIMPLEST"},
    {"emoji": "🔵", "k": "Zerodha", "v": "79.5 lakh · delivery ₹0, F&O ₹20, AMC ₹300 · Kite, Coin, Varsity", "chip": "ECOSYSTEM"},
    {"emoji": "🟠", "k": "Angel One", "v": "76.4 lakh · delivery ₹0, F&O ₹20, AMC ₹240 · strong research", "chip": "RESEARCH"},
    {"emoji": "🟣", "k": "Dhan", "v": "New-age · delivery ₹0, F&O ₹20, AMC ₹0 · the #1 options app", "chip": "F&O FOCUS"},
   ]},
  "First, the major brokers, their users, and their charges. [pause] "
  "First — Groww. Now the country's number one, with one point three crore users. The simplest app. But one difference — it charges twenty rupees on delivery; the other brokers give this free. Its AMC is zero. [pause] "
  "Second — Zerodha. Seventy-nine and a half lakh users. Delivery is free, F&O is twenty rupees, AMC three hundred. It has a strong ecosystem — Kite, Coin, and Varsity. [pause] "
  "Third — Angel One. Seventy-six point four lakh users. Delivery free, AMC two hundred forty. Known for strong research reports. [pause] "
  "Fourth — Dhan. A new-age broker. Delivery free, AMC zero. Currently the number one app for options traders. Upstox and Fyers are also good options for F&O."),
 ("br_apps", "sm_iconcards",
  {"kicker": "THE APPS", "title": "The Apps — Where Each One Wins", "color": "#34D399",
   "items": [
    {"emoji": "🛠️", "k": "Zerodha", "v": "Kite (pro trading), Coin (2000+ direct MF, XIRR), Console, Varsity free education, Sensibull options", "chip": "ALL-ROUNDER"},
    {"emoji": "👶", "k": "Groww", "v": "The simplest interface; MF needs no demat; best for beginners — but limited for power users", "chip": "BEGINNERS"},
    {"emoji": "📊", "k": "Dhan", "v": "TradingView charts, option chain, strategy tools, speed — built for F&O traders", "chip": "OPTIONS"},
    {"emoji": "🔍", "k": "Angel One", "v": "Strong research reports and smart suggestions — but users complain of heavy notifications", "chip": "RESEARCH"},
   ]},
  "Now the apps — where each one is strongest. [pause] "
  "Zerodha — Kite is a pro trading platform, Coin has over two thousand direct mutual funds, and a single XIRR view across funds and stocks. Varsity is free education, Sensibull is for options analysis. Everything in one place. [pause] "
  "Groww — the simplest app. For mutual funds you don't even need a demat account, just KYC. Best for beginners. But experienced traders find the features limited. [pause] "
  "Dhan — TradingView charts, option chain, strategy tools, and great speed. An app built specifically for F&O and options traders. [pause] "
  "Angel One — strong research reports and smart suggestions. But some users complain about heavy notifications and promotions."),
 ("br_issues", "sm_iconcards",
  {"kicker": "RECENT USER-REPORTED ISSUES", "title": "Recent Issues — User Complaints", "color": "#FB7185",
   "items": [
    {"emoji": "🌐", "k": "Cloudflare outage (Dec 5, 2025)", "v": "Zerodha, Angel, Upstox, Groww all down ~12 min — login, order failures. But a third-party issue, not the brokers' fault", "chip": "GLOBAL"},
    {"emoji": "⏳", "k": "Zerodha — Kite slowdowns", "v": "Historic slowdowns on expiry / high-volume days (#KiteDown) — much improved now; WhatsApp backup added", "chip": "IMPROVED"},
    {"emoji": "💸", "k": "Groww — delivery charge", "v": "Charges ₹20 on delivery that peers give free; occasional charge / statement complaints", "chip": "CHARGES"},
    {"emoji": "🔔", "k": "Angel One — square-off", "v": "Intraday auto square-off at 3:15 PM + heavy notifications, mis-selling complaints", "chip": "COMPLAINTS"},
   ]},
  "Now the important part — the issues users have faced recently. [pause] "
  "The biggest — on December fifth, twenty twenty-five, a global service called Cloudflare went down, and Zerodha, Angel One, Upstox, and Groww — all the apps stopped working for about twelve minutes. Logins and orders were stuck. But this was no broker's fault — it was a third-party issue. [pause] "
  "Zerodha — in the past, Kite would slow down on expiry and high-volume days. It's much improved now, and they've added a WhatsApp backup. [pause] "
  "Groww — it charges twenty rupees on delivery that other brokers give for free. There are occasional complaints about charges and statements. [pause] "
  "Angel One — automatically closing intraday positions at three fifteen, and heavy notifications — these draw complaints. [pause] "
  "One reassurance — all these brokers are SEBI-registered. Your shares are not with the broker; they're safe in your name at NSDL and CDSL."),
 ("br_best", "sm_iconcards",
  {"kicker": "BEST FOR EACH NEED", "title": "Which App Is Best for What?", "color": "#34D399",
   "items": [
    {"emoji": "📈", "k": "Mutual Funds", "v": "Groww (simple, ₹0, no demat) for beginners; or Zerodha Coin (XIRR, ecosystem) if you also trade", "chip": "MF"},
    {"emoji": "🏦", "k": "Stocks / Delivery", "v": "Zerodha or Dhan (₹0 delivery + good tools + low AMC). Groww is costly for large delivery", "chip": "STOCKS"},
    {"emoji": "⚡", "k": "Futures & Options", "v": "Dhan (#1 options app, TradingView, speed) or Zerodha (Kite + Sensibull, reliability)", "chip": "F&O"},
    {"emoji": "🎯", "k": "All in One Place", "v": "Zerodha — full ecosystem, education, reliability; Dhan — a modern, fast alternative", "chip": "ALL-IN-ONE"},
   ]},
  "Now the real question — which app is best for what? Let's go by need. [pause] "
  "For mutual funds — Groww is best. Simple, no cost, and you don't even need a demat. If you also trade, then Zerodha Coin, because funds and stocks sit in one place. [pause] "
  "For stocks and delivery — Zerodha or Dhan. Free delivery, good tools, low AMC. If you do large delivery volumes, Groww becomes a bit costly. [pause] "
  "For futures and options — Dhan. With its speed and TradingView charts, it's number one for options. Or Zerodha — with Kite, Sensibull, and reliability. [pause] "
  "If you want everything in one place — Zerodha, the best all-rounder with a full ecosystem. Dhan is a modern, fast alternative."),
 ("br_take", "sm_checklist",
  {"kicker": "HOW TO CHOOSE", "title": "How to Choose — 5 Rules", "color": "#34D399", "icon": "💡",
   "items": [
    "Define your need: only MF, or stocks, or F&O too?",
    "Add AMC + delivery charge together — not just the F&O rate",
    "Charges change often — verify current rates in the app",
    "All are SEBI-registered — shares are safe in NSDL/CDSL",
    "This is not advice or promotion — the best is what fits you",
   ]},
  "So how do you choose a broker? Five rules. [pause] "
  "One — first, define your need. Only mutual funds, or stocks, or F&O too? [pause] "
  "Two — don't look at just the F&O rate. Add up the total cost, including AMC and delivery charges. [pause] "
  "Three — charges change often. Verify the current rates in the app before you choose. [pause] "
  "Four — all these brokers are SEBI-registered. Your shares are safe at NSDL and CDSL. [pause] "
  "Five — this is not a promotion for any broker, and not advice. The best one is simply the one that fits your need."),
 ("br_recap", "sm_recap",
  {"title": "Brokers — At a Glance",
   "items": [
    "Groww: simple, MF, beginners — but delivery costs",
    "Zerodha: best all-rounder, ecosystem, F&O",
    "Dhan: fast app for F&O/options, ₹0 AMC",
    "Angel One: research; Upstox/Fyers: active/algo",
    "Verify charges · SEBI protection applies",
   ],
   "closer": "No app is 'the best' — the one that fits your need is best."},
  "Brokers, at a glance. [pause] "
  "Groww — simple, great for mutual funds and beginners. But delivery is a bit costly. [pause] "
  "Zerodha — the best all-rounder. Strong ecosystem, education, and F&O. [pause] "
  "Dhan — a fast app for F&O and options, with zero AMC. [pause] "
  "Angel One — for research; Upstox and Fyers — for active and algo traders. [pause] "
  "No app is best for everyone — the one that fits your need is best for you. And verify the charges. [pause] "
  "This information is aggregated from public sources — it's not a promotion for any broker, and not investment advice. Thanks for watching."),
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
