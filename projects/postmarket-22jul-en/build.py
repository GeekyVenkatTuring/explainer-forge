#!/usr/bin/env python3
"""Post-Market Recap (ENGLISH) — 22 July 2026. Reuses `sm` scene set. English TTS + English frames.
Honest self-review: yesterday's pre-market leaned positive (US lead) but FLAGGED crude as the key risk;
that exact risk dominated. Verified close: Sensex 76,755.05 (-715.06/-0.92%), Nifty 23,996.25
(-191.45/-0.79%, below 24,000), Bank Nifty 57,126.80 (-1.23%); 3rd straight down day, steepest in ~2 wks.
Cause: Brent +4.68% to $95.27 (5-wk high, West Asia conflict) + bank selloff + broad selling (IT/pharma/realty).
Losers: InterGlobe/IndiGo, Dr Reddy's, Jio Financial, Infosys, SBI, ICICI, Axis, UltraTech.
Gainers: Bajaj Auto, TVS Motor (earnings), HUL, NTPC, Power Grid, Titan.
Sources: The Week, Business Standard, ETV Bharat, Free Press Journal, Liquide. Info, not advice.
Usage: python3 build.py            |   python3 build.py po22e
"""
import json, os, re, subprocess, sys, time

VOICE = "en-IN-NeerjaNeural"; RATE = "-4%"; GAP = 0.5; PAUSE = 0.55; PREFIX = "sm"
ROOT = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(ROOT, "..", ".."))
PUBLIC = os.path.join(REPO, "composer", "public", PREFIX); RAW = os.path.join(ROOT, "assets", "raw"); FIN = os.path.join(ROOT, "assets")
for d in (PUBLIC, RAW, os.path.join(ROOT, "artifacts"), os.path.join(ROOT, "renders")):
    os.makedirs(d, exist_ok=True)

CHAPTERS = {
 "po22e": [
 ("po_title", "sm_ptitle",
  {"title": "Post-Market Recap", "sub": "July 22, 2026 · we expected a recovery — the market crashed", "kicker": "POST-MARKET · 22 JUL 2026"},
  "This morning, our pre-market brief leaned positive — a firm-to-positive open, on a strong US lead. [pause] "
  "But the market did the opposite. It crashed for a third straight day. So let's be honest, and analyse exactly what went wrong and why. [pause] "
  "Here's the twist — the one thing our pre-market brief flagged as the key risk is exactly what brought the market down. This is information analysis, not investment advice."),
 ("po_snap", "sm_stats",
  {"kicker": "INDEX SNAPSHOT", "title": "Closing Numbers — 22 July",
   "stats": [
    {"label": "SENSEX", "to": 76755, "prefix": "", "suffix": "", "color": "#FB7185", "sub": "−715 pts · −0.92%"},
    {"label": "NIFTY 50", "to": 23996, "prefix": "", "suffix": "", "color": "#FB7185", "sub": "−191 · below 24,000"},
    {"label": "BANK NIFTY", "to": 57127, "prefix": "", "suffix": "", "color": "#FB7185", "sub": "−709 · −1.23%"},
   ],
   "note": "Third straight down day — the steepest fall in nearly two weeks. And this time it was broad-based: no midcap cushion."},
  "First, the damage. [pause] "
  "The Sensex crashed seven hundred fifteen points to close at seventy-six thousand seven hundred fifty-five — down almost a percent. [pause] "
  "The Nifty fell one hundred ninety-one points to twenty-three thousand nine hundred ninety-six — closing below the key twenty-four thousand mark. [pause] "
  "And the Bank Nifty was the worst hit, down one point two three percent. [pause] "
  "This was the third straight down day, and the steepest fall in nearly two weeks. Unlike yesterday, there was no midcap cushion — the selling was broad-based across the market."),
 ("po_why", "sm_iconcards",
  {"kicker": "WHY IT CRASHED", "title": "Four Reasons for the Fall", "color": "#FB7185",
   "items": [
    {"emoji": "🛢️", "k": "Crude spiked to $95", "v": "Brent jumped 4.68% to $95.27 — a 5-week high on an escalating West Asia conflict. THE trigger", "chip": "MAIN CAUSE"},
    {"emoji": "🏦", "k": "Bank selloff", "v": "Bank Nifty −1.23%; SBI, ICICI, Axis dragged — financials led the fall for a 3rd day", "chip": "−1.23%"},
    {"emoji": "📉", "k": "Broad-based selling", "v": "IT, pharma and realty all bled — no sector was spared, no cushion this time", "chip": "NO CUSHION"},
    {"emoji": "🌍", "k": "Middle East + tariffs", "v": "Fresh regional escalation plus US tariff fears kept global sentiment risk-off", "chip": "RISK-OFF"},
   ]},
  "So why did it crash? Four reasons — and the first one is the whole story. [pause] "
  "Number one — crude oil. Brent crude jumped four point six eight percent to ninety-five point two seven dollars, a five-week high, as the West Asia conflict escalated. India imports most of its oil, so this is the trigger that hit everything. [pause] "
  "Number two — a bank selloff. The Bank Nifty fell one point two three percent, with S-B-I, I-C-I-C-I and Axis dragging financials down for a third straight day. [pause] "
  "Number three — the selling was broad-based. I-T, pharma and realty all bled. Unlike yesterday, no sector was spared. [pause] "
  "Number four — the backdrop. Fresh Middle East escalation and US tariff fears kept global markets in a risk-off mood."),
 ("po_losers", "sm_iconcards",
  {"kicker": "TOP LOSERS", "title": "The Biggest Losers", "color": "#FB7185",
   "items": [
    {"emoji": "✈️", "k": "InterGlobe (IndiGo)", "v": "Top Nifty loser — airlines are hit hardest by a crude spike; fuel is their single biggest cost", "chip": "CRUDE HIT"},
    {"emoji": "🏦", "k": "SBI · ICICI · Axis", "v": "The banking selloff — the single biggest drag on the index", "chip": "BANKS"},
    {"emoji": "💻", "k": "Infosys · Jio Financial", "v": "IT fell despite a strong Nasdaq overnight — crude and geopolitics overrode the tech tailwind", "chip": "IT"},
    {"emoji": "💊", "k": "Dr Reddy's · UltraTech", "v": "Pharma weak for a 2nd day; cement also among the laggards", "chip": "LAGGARDS"},
   ]},
  "Now the biggest losers. [pause] "
  "The top loser was InterGlobe Aviation — IndiGo. This makes perfect sense: airlines are hit hardest by a crude spike, because jet fuel is their single biggest cost. [pause] "
  "Next, the banks — S-B-I, I-C-I-C-I and Axis. The banking selloff was the single biggest drag on the index. [pause] "
  "Then Infosys and Jio Financial. Note this carefully — I-T fell even though the Nasdaq was strong overnight. Crude and geopolitics completely overrode the tech tailwind we expected. [pause] "
  "And Doctor Reddy's stayed weak for a second day, with UltraTech Cement also among the laggards."),
 ("po_gainers", "sm_iconcards",
  {"kicker": "THE FEW WINNERS", "title": "What Held Up", "color": "#34D399",
   "items": [
    {"emoji": "🏍️", "k": "Bajaj Auto · TVS Motor", "v": "Rose on strong Q1 results, defying the selloff — exactly the earnings reaction we flagged this morning", "chip": "EARNINGS"},
    {"emoji": "🧼", "k": "HUL · Titan", "v": "Defensive consumer names — money rotated to safety in a falling market", "chip": "DEFENSIVE"},
    {"emoji": "⚡", "k": "NTPC · Power Grid", "v": "Utilities held up — steady, rate-insensitive, and shielded from crude", "chip": "UTILITIES"},
    {"emoji": "🛡️", "k": "The pattern", "v": "In a crude-driven crash, money hides in defensives, utilities and genuine earnings beats", "chip": "ROTATION"},
   ]},
  "It wasn't all red. A few names held up — and the pattern is a lesson in itself. [pause] "
  "Bajaj Auto and TVS Motor actually rose, defying the selloff, on their strong quarterly results — exactly the earnings reaction we flagged this morning. [pause] "
  "Defensive consumer names like Hindustan Unilever and Titan held up, as money rotated to safety. [pause] "
  "And utilities — N-T-P-C and Power Grid — stayed steady, because they're rate-insensitive and shielded from crude. [pause] "
  "The pattern is clear: in a crude-driven crash, money hides in defensives, utilities, and genuine earnings beats."),
 ("po_lesson", "sm_myths",
  {"kicker": "THE HONEST REVIEW", "title": "What We Expected vs What Happened", "mythLabel": "🔮 PRE-MARKET EXPECTED", "factLabel": "💥 WHAT ACTUALLY HAPPENED",
   "pairs": [
    {"m": "Strong US lead → a firm, positive open", "f": "Crude spiked to $95 → a 3rd-day crash instead"},
    {"m": "Nasdaq +1.3% would lift Indian IT", "f": "Infosys and IT fell — crude overrode the tailwind"},
    {"m": "…but we flagged crude as THE key risk", "f": "That exact risk is what dominated the whole day"},
   ]},
  "Now the honest review — what we expected this morning, versus what actually happened. [pause] "
  "We expected a firm, positive open on a strong US lead. Instead, crude spiked and the market crashed for a third day. [pause] "
  "We thought the Nasdaq's one point three percent jump would lift Indian I-T. Instead, Infosys and I-T fell — crude and geopolitics overrode that tailwind completely. [pause] "
  "But here's the key point — this morning we explicitly flagged crude near ninety dollars as the number-one risk. And that exact risk is what dominated the entire day. [pause] "
  "That's the real lesson: a pre-market brief is a setup, not a forecast. Overnight cues can be wiped out by a single geopolitical shock — and the risk you flag can be the one that decides the day."),
 ("po_take", "sm_checklist",
  {"kicker": "TAKEAWAYS", "title": "5 Lessons from Today", "color": "#34D399", "icon": "💡",
   "items": [
    "A pre-market is a SETUP, not a forecast — the flagged risk can win",
    "Geopolitical shocks (crude) override overnight cues in minutes",
    "Crude near $95 hurts airlines, paints & OMCs the most",
    "In a broad selloff, defensives & real earnings-beats hold up",
    "For SIP investors, a 3-day dip is still noise — don't panic-sell",
   ]},
  "So, five lessons from today. [pause] "
  "One — a pre-market brief is a setup, not a forecast. The risk you flag can be the very thing that wins the day. [pause] "
  "Two — geopolitical shocks, like a crude spike, can override overnight cues within minutes of the open. [pause] "
  "Three — crude near ninety-five dollars hurts airlines, paint companies and oil marketers the most. Watch those. [pause] "
  "Four — in a broad selloff, defensives, utilities and genuine earnings-beats are where money hides. [pause] "
  "Five — for a long-term S-I-P investor, a three-day dip is still just noise. Don't panic-sell into a geopolitical scare."),
 ("po_recap", "sm_recap",
  {"title": "22 July — At a Glance",
   "items": [
    "Sensex −715 (76,755) · Nifty −191 (23,996) — 3rd day down",
    "Cause: crude +4.68% to $95 + bank selloff + Middle East",
    "Losers: IndiGo, SBI, ICICI, Infosys, Dr Reddy's",
    "Gainers: Bajaj Auto, TVS, HUL, NTPC (defensives)",
    "Lesson: the risk we flagged (crude) is exactly what hit",
   ],
   "closer": "A pre-market is a setup, not a promise — and today, the flagged risk won."},
  "July twenty-second, at a glance. [pause] "
  "The Sensex fell seven hundred fifteen points and the Nifty broke below twenty-four thousand — the third straight down day. [pause] "
  "The cause — crude jumping almost five percent to ninety-five dollars, a bank selloff, and Middle East escalation. [pause] "
  "The losers — IndiGo, S-B-I, I-C-I-C-I, Infosys, and Doctor Reddy's. The winners — Bajaj Auto, T-V-S, and defensives like Hindustan Unilever and N-T-P-C. [pause] "
  "And the lesson — the risk we flagged this morning, crude, is exactly what hit. A pre-market is a setup, not a promise — and today, the flagged risk won. [pause] "
  "This information is aggregated from public sources — for analysis only, not investment advice. Thanks for watching, and see you at tomorrow's open."),
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
