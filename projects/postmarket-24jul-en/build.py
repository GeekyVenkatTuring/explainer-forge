#!/usr/bin/env python3
"""Post-Market Recap (ENGLISH) — 24 July 2026. Reuses `sm` scene set. English TTS + English frames.
Story: 5th straight down day (longest losing streak in >6 months) — but a MILD -0.43% slow bleed, not a crash.
Verified close: Sensex 76,059.77 (-331.62/-0.43%), Nifty 23,767.45 (-102.15/-0.43%, below 23,800),
Bank Nifty 56,693.50 (+0.18%, GREEN). Weekly: Nifty -2.33%, Sensex -2.70%.
Cause: a full week of $100+ Brent (Iran/West Asia) + FII selling (~-3,000 cr) + weak rupee (96.63) +
inflation/growth overhang. Nuance: Brent eased to $97.04 (-1.47%, Fortune) but stayed elevated — market
priced the week. (Earlier "$92" was WTI/erroneous.) Gainers to EXACT close %: HCLTech +2.08%, Wipro +1.32%,
Cipla +1.23% (user-validated NSE close), Nifty IT +0.82%. Banks green (Bank Nifty +0.18%); Autos led fall.
Losers: Bajaj Finance -2.60%, Eternal -2.47%, M&M -2.11%; Auto -1.10%, Energy -0.57%, Metals/Realty -0.55%.
Levels: Nifty 23,600 sup / 23,900 res. NO ROUNDING — 2 decimals in frames AND narration.
Sources: HDFCSky (close), Liquide, Fortune (oil), Business Standard, Sunday Guardian. Info, not advice.
Usage: python3 build.py            |   python3 build.py po24e
"""
import json, os, re, subprocess, sys, time

VOICE = "en-IN-NeerjaNeural"; RATE = "-4%"; GAP = 0.5; PAUSE = 0.55; PREFIX = "sm"
ROOT = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(ROOT, "..", ".."))
PUBLIC = os.path.join(REPO, "composer", "public", PREFIX); RAW = os.path.join(ROOT, "assets", "raw"); FIN = os.path.join(ROOT, "assets")
for d in (PUBLIC, RAW, os.path.join(ROOT, "artifacts"), os.path.join(ROOT, "renders")):
    os.makedirs(d, exist_ok=True)

CHAPTERS = {
 "po24e": [
 ("po_title", "sm_ptitle",
  {"title": "Post-Market Recap", "sub": "July 24, 2026 · five days down — but this was no crash", "kicker": "POST-MARKET · 24 JUL 2026"},
  "The Indian market just closed lower for the fifth straight day — its longest losing streak in more than six months. [pause] "
  "But here's the twist most headlines miss: today was not a crash. The Nifty fell less than half a percent — a slow, quiet drift, not a plunge. [pause] "
  "So the real question isn't how far did it fall — it's why won't it stop falling, and what the market is quietly telling us underneath. "
  "Let's break down exactly what happened on July twenty-fourth. This is information analysis, not investment advice."),
 ("po_snap", "sm_stats",
  {"kicker": "INDEX SNAPSHOT", "title": "Closing Numbers — 24 July",
   "stats": [
    {"label": "SENSEX", "to": 76060, "prefix": "", "suffix": "", "color": "#FB7185", "sub": "−332 pts · −0.43%"},
    {"label": "NIFTY 50", "to": 23767, "prefix": "", "suffix": "", "color": "#FB7185", "sub": "−102 · below 23,800"},
    {"label": "BANK NIFTY", "to": 56694, "prefix": "", "suffix": "", "color": "#34D399", "sub": "+0.18% · GREEN"},
   ],
   "note": "Mild on the day — but 5 red sessions add up: Nifty −2.33% for the WEEK. Notice the green box: Bank Nifty held up. The damage was narrow, not broad."},
  "First, the scoreboard. [pause] "
  "The Sensex fell three hundred thirty-two points to close at seventy-six thousand sixty — down zero point four three percent. [pause] "
  "The Nifty slipped one hundred two points to twenty-three thousand seven hundred sixty-seven, closing below twenty-three thousand eight hundred. [pause] "
  "But look at the third number — the Bank Nifty actually closed green, up zero point one eight percent. That one green box is the most important clue on this whole slide. [pause] "
  "Because while any single day was mild, five red sessions add up: the Nifty lost two point three three percent for the week, the Sensex two point seven zero. "
  "That's the real story — not a crash, but a slow, steady bleed. And underneath it, the damage was surprisingly narrow."),
 ("po_why", "sm_iconcards",
  {"kicker": "WHY IT KEPT FALLING", "title": "Four Forces Behind the Streak", "color": "#FB7185",
   "items": [
    {"emoji": "🛢️", "k": "A week of $100 oil", "v": "Brent topped $100 mid-week on the West Asia conflict. It eased to $97.04 (−1.47%) on Friday but stayed highly elevated — damage done", "chip": "THE ROOT"},
    {"emoji": "🌍", "k": "West Asia tensions", "v": "Escalating Middle East conflict kept global markets in a risk-off mood all week long", "chip": "RISK-OFF"},
    {"emoji": "💸", "k": "FII selling + weak rupee", "v": "Foreign investors stayed net sellers (~₹3,000 cr out); the rupee slid to ₹96.6 to the dollar", "chip": "−₹3,000 Cr"},
    {"emoji": "📉", "k": "Growth + inflation worry", "v": "Costlier oil feeds inflation and dents India's growth outlook — the overhang that won't lift", "chip": "OVERHANG"},
   ]},
  "So why five days down? Four forces — and the first is the root of it all. [pause] "
  "Number one — oil. Earlier this week Brent crude topped one hundred dollars a barrel as the West Asia conflict flared. And here's the key nuance: even though oil eased slightly on Friday, to ninety-seven dollars a barrel, down about one and a half percent, it stayed highly elevated — and the week's damage was already done. Markets price the trend, not just today's tick. [pause] "
  "Number two — those Middle East tensions kept global markets in a risk-off mood all week. [pause] "
  "Number three — foreign investors kept selling, pulling out around three thousand crore, and a weakening rupee near ninety-six point six to the dollar added to the pressure. [pause] "
  "Number four — the overhang. Costlier oil feeds inflation and dents India's growth outlook. That's the worry that simply refused to lift — and it's why one mild down-day became five."),
 ("po_losers", "sm_iconcards",
  {"kicker": "TOP LOSERS", "title": "Who Got Hit", "color": "#FB7185",
   "items": [
    {"emoji": "🏦", "k": "Bajaj Finance −2.60%", "v": "The single biggest Nifty loser — NBFCs are sensitive to rate and liquidity worries, so they lead the selling", "chip": "TOP LOSER"},
    {"emoji": "🛒", "k": "Eternal −2.47%", "v": "The Zomato parent slid — high-growth, richly-valued names are the first to be sold in a risk-off tape", "chip": "HIGH-GROWTH"},
    {"emoji": "🚗", "k": "M&M −2.11% · Auto −1.10%", "v": "Autos led the sector declines; costlier fuel and inputs weigh on demand sentiment", "chip": "AUTO DRAG"},
    {"emoji": "⚡", "k": "Energy −0.57% · Metals −0.55%", "v": "Realty −0.55% too — the classic crude-and-rates losers. Notice: every loser is domestic & cyclical", "chip": "CYCLICALS"},
   ]},
  "Now, who got hit. [pause] "
  "The single biggest loser was Bajaj Finance, down two point six zero percent. N-B-F-Cs are sensitive to interest-rate and liquidity worries, so they lead the selling when the mood sours. [pause] "
  "Next, Eternal — the parent of Zomato — fell two point four seven percent. High-growth, richly-valued names are always the first to be sold in a risk-off market. [pause] "
  "Then Mahindra and Mahindra, down two point one one percent, as the whole auto sector fell one point one zero percent — the worst-performing sector today. Costlier fuel and inputs weigh on demand. [pause] "
  "And the usual crude-and-rates crowd — energy down zero point five seven, metals and realty each down zero point five five percent. Notice the pattern: every loser is a domestic, rate-sensitive, cyclical name."),
 ("po_gainers", "sm_iconcards",
  {"kicker": "WHAT HELD UP", "title": "Where the Money Hid", "color": "#34D399",
   "items": [
    {"emoji": "💻", "k": "IT: HCLTech +2.08%, Wipro +1.32%", "v": "IT was the top-performing sector (+0.82%). A weak rupee HELPS IT — they earn in dollars, report in rupees", "chip": "TOP SECTOR"},
    {"emoji": "🏦", "k": "Bank Nifty +0.18%", "v": "Financials steadied and closed green — a tentative but real sign they're trying to stabilise", "chip": "GREEN"},
    {"emoji": "💊", "k": "Cipla +1.23%", "v": "Rose on strong Q1FY27 results. Pharma, like IT, is both defensive AND a dollar earner", "chip": "Q1 BEAT"},
    {"emoji": "🛡️", "k": "FMCG defensives", "v": "Consumer staples stayed green as money rotated to safety in a weak-rupee, high-oil market", "chip": "DEFENSIVE"},
   ]},
  "But it wasn't all red — and what held up tells you where the smart money hid. [pause] "
  "The standout was I-T. HCL Technologies rose two point zero eight percent, Wipro one point three two, and I-T was the top-performing sector, up zero point eight two percent. Here's why: a weak rupee actually helps I-T, because these companies earn in dollars and report in rupees. The very same weak rupee that hurt importers helped the exporters. [pause] "
  "Second, the banks. The Bank Nifty closed green — a tentative, but real, sign that financials are trying to stabilise. [pause] "
  "Cipla rose one point two three percent on strong quarterly results — and pharma, like I-T, is both defensive and a dollar earner. [pause] "
  "And defensive consumer, F-M-C-G names, stayed green. The lesson: in a weak-rupee, high-oil market, money rotates to exporters and defensives."),
 ("po_reads", "sm_myths",
  {"kicker": "READ BEHIND THE HEADLINE", "title": "What It Looks Like vs What's Real", "mythLabel": "🧐 THE HEADLINE SAYS", "factLabel": "🔍 WHAT'S REALLY HAPPENING",
   "pairs": [
    {"m": "Fifth day down — the market is crashing", "f": "Only −0.43% today; a slow drift, not a plunge. A streak ≠ a crash"},
    {"m": "Oil eased to $97 — so the fall makes no sense", "f": "Markets price the whole week's trend, not just today's single tick"},
    {"m": "Everything is selling off", "f": "IT & banks closed GREEN — the damage was narrow, not broad-based"},
   ]},
  "Now let's read behind the headlines — because today had three things that look confusing until you understand them. [pause] "
  "The headline says the fifth day down means the market is crashing. The reality: today's fall was under half a percent — a slow drift, not a plunge. A streak and a crash are not the same thing. [pause] "
  "The headline says oil eased to ninety-seven dollars, so the fall makes no sense. The reality: markets price the trend of the whole week, not just today's single tick. Sentiment has a lag. [pause] "
  "And the headline says everything is selling off. But I-T and the banks closed green — the damage was narrow, not broad-based. Reading that nuance is exactly what separates calm analysis from panic."),
 ("po_take", "sm_checklist",
  {"kicker": "TAKEAWAYS", "title": "5 Lessons to Carry Forward", "color": "#34D399", "icon": "💡",
   "items": [
    "A losing streak isn't a crash — five −0.4% days ≠ one −2% day",
    "A weak rupee HELPS IT & pharma, HURTS importers & autos",
    "Watch Nifty 23,600 support — a clean break opens more downside",
    "Bank Nifty closing green = the first tentative sign of a bottom",
    "For SIP investors, a −2.33% week is still noise — keep buying",
   ]},
  "So, five takeaways to carry into next week. [pause] "
  "One — a losing streak is not a crash. Five gentle down-days is very different from one violent one; don't let the word streak scare you. [pause] "
  "Two — currency matters. A weak rupee quietly helps I-T and pharma, and hurts importers and autos. When oil and the rupee move, always check who earns in dollars. [pause] "
  "Three — watch the level. The Nifty has support around twenty-three thousand six hundred; a clean break below it opens up more downside. Resistance is near twenty-three thousand nine hundred. [pause] "
  "Four — the Bank Nifty closing green is the first tentative sign that a bottom may be forming. Watch closely if it holds. [pause] "
  "And five — for a long-term S-I-P investor, a two point three three percent week is still just noise. Keep buying on your schedule."),
 ("po_recap", "sm_recap",
  {"title": "24 July — At a Glance",
   "items": [
    "Sensex −332 (76,060) · Nifty −102 (23,767) — 5th day down",
    "Weekly: Nifty −2.33% — longest losing streak in 6 months",
    "Cause: a week of $100 oil + FII selling + weak rupee",
    "Red: Bajaj Finance, Eternal, M&M, autos · Green: IT, banks, Cipla",
    "Watch: Nifty 23,600 support · green Bank Nifty = tentative bottom",
   ],
   "closer": "Not a crash — a slow bleed. And underneath, IT and banks are quietly holding the line."},
  "July twenty-fourth, at a glance. [pause] "
  "The Sensex fell three hundred thirty-two points and the Nifty one hundred two — the fifth straight down day, and the longest losing streak in more than six months, with the Nifty down two point three three percent for the week. [pause] "
  "The cause — a full week of hundred-dollar oil, foreign investors selling, and a weakening rupee. [pause] "
  "The red — Bajaj Finance, Eternal, Mahindra and the autos. The green — I-T, the banks, and Cipla on its results. [pause] "
  "And what to watch — Nifty support at twenty-three thousand six hundred, and a green Bank Nifty as a tentative sign of a bottom. "
  "It was not a crash — it was a slow bleed. And underneath it, I-T and the banks are quietly holding the line. [pause] "
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
