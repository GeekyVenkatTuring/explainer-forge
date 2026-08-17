#!/usr/bin/env python3
"""Pre-Market Brief (ENGLISH) — 3 August 2026 (Monday). Reuses `sm` scene set. English TTS + English frames.

NUMBERS TABLE (pre-render gate — verify once before TTS; sources per figure):
- Fri 31 Jul 2026 CLOSE (all indices consistent across sources — used at exact 2-dec on screen):
    Sensex  78,094.64  +166.49  +0.21%        [Liquide close report; cross-checked Goodreturns/dhan]
    Nifty50 24,383.60  +66.45   +0.27%        [Liquide; Goodreturns Aug3-7 outlook; dhan closing bell]
    BankNifty 57,264.85 +117.35 +0.21%        [Liquide close report]
- Weekly (to 31 Jul): Nifty > +2.5% — biggest weekly gain in ~4 months   [Goodreturns Aug3-7 outlook]
- Monthly (Jul): Nifty +2.2%, Sensex +2.1% — 2nd straight monthly gain    [Liquide]
- Sectors 31 Jul (Liquide table): Auto +1.64% (best), Fin Services +1.31%, Energy +1.09%, Pharma +0.72%;
    IT -1.56% (worst), FMCG -1.05%, Cons Durables -0.44%.
- Leaders: Bajaj Finance hit a fresh 52-WEEK HIGH after Q1 FY27 PAT +29% YoY to Rs 5,436 cr, NII +24% to
    Rs 11,495 cr, GNPA 0.96%  [Business Standard / Goodreturns]. NOTE: intraday move quoted 3.5%-8.3% across
    vendors (BSE vs NSE, intraday-high vs close) -> framed QUALITATIVELY ("52-wk high"), no contested % on screen.
    Bajaj Finserv & Jio Financial also gained. Laggards: TCS/Infosys/HCL Tech/Tech Mahindra/Wipro fell ~2-3%.
- FII/DII 31 Jul (PROVISIONAL, cash): FII +Rs 277.50 cr, DII +Rs 2,260.40 cr  [5paisa FII/DII page]
- US Fri 31 Jul close: Dow 52,485.03 +276.97 (+0.53%); S&P 500 7,489.72 (+0.7%); Nasdaq 25,373.85 (~+1.0%).
    Amazon surged on Q2 earnings; Dow logged a 4th straight winning month.  [Yahoo Finance / CNBC / Washington Post]
- Brent crude: $88.16, -0.98% (Fri) — eased from the ~$92 US-Iran spike of the prior week  [named BRENT, Yahoo]
- Weekend / month-start data:
    GST (Jul): Rs 2.11 lakh crore, +15.4% YoY (imports +28.8%)  [Business Standard / BusinessToday, dated 1 Aug 2026]
    Auto (Jul): M&M +26% (1,03,860), Hyundai record 75,360 (+25.4%), Maruti 2,41,421  [Autocar/Autopunditz]
    Manufacturing PMI stayed in expansion (read 53-54 range across vendors) -> framed qualitatively.  [S&P Global]
- THE WEEK AHEAD: RBI MPC decision Wed 5 Aug (rate + stance = master switch). Q1 results: SBI, Bharti Airtel,
    ONGC, Power Grid, Trent, Hindalco, Titan.  [Goodreturns / CNBC outlook]
- IPO corner: MV Electrosystems (mainboard, Rs 290 cr, band Rs 400-425) subscription CLOSES today (3 Aug),
    lists 6 Aug; Ardee Industries opens 5 Aug (band Rs 50-53, Rs 425.87 cr); Technocraft Ventures (EPC) opens 7 Aug.
    GMP is unofficial and NOT cited.  [Chittorgarh / zeebiz / PNI]
- Levels: resistance 24,500-24,600, then 24,750 (200-DMA); support 24,150 / 24,000 / 23,800.  [Goodreturns outlook]

WATCHLIST / SETUP, not a prediction. Aggregated from public sources; NOT investment advice.
Usage: python3 build.py            |   python3 build.py pm03e
"""
import json, os, re, subprocess, sys, time

VOICE = "en-IN-NeerjaNeural"; RATE = "-4%"; GAP = 0.5; PAUSE = 0.55; PREFIX = "sm"
ROOT = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(ROOT, "..", ".."))
PUBLIC = os.path.join(REPO, "composer", "public", PREFIX); RAW = os.path.join(ROOT, "assets", "raw"); FIN = os.path.join(ROOT, "assets")
for d in (PUBLIC, RAW, os.path.join(ROOT, "artifacts"), os.path.join(ROOT, "renders")):
    os.makedirs(d, exist_ok=True)

CHAPTERS = {
 "pm03e": [
 ("pm_title", "sm_ptitle",
  {"title": "Pre-Market Brief", "sub": "August 3, 2026 · Monday · before the open", "kicker": "PRE-MARKET · 03 AUG 2026"},
  "Good morning. It's Monday, August third — and here's your setup before the market opens. [pause] "
  "The market comes into this week on a strong note — so today we'll do three things. Recap how Friday and last week closed, look at the weekend cues and data, and then map out the week's big events — the R-B-I policy, the earnings, and the levels to watch. [pause] "
  "One note up front — this is a watchlist and a setup, not a prediction of which stocks will go up. It's information, not investment advice."),
 ("pm_close", "sm_stats",
  {"kicker": "FRIDAY'S CLOSE — A STRONG FINISH", "title": "Where We Closed on July 31",
   "stats": [
    {"label": "Sensex", "to": 78094.64, "prefix": "", "suffix": "", "decimals": 2, "color": "#34D399", "sub": "+166.49 pts · +0.21%"},
    {"label": "Nifty 50", "to": 24383.60, "prefix": "", "suffix": "", "decimals": 2, "color": "#34D399", "sub": "+66.45 pts · +0.27%"},
    {"label": "Bank Nifty", "to": 57264.85, "prefix": "", "suffix": "", "decimals": 2, "color": "#34D399", "sub": "+117.35 pts · +0.21%"},
   ],
   "note": "That capped Nifty's biggest weekly gain in nearly four months — up over 2.5% for the week, and a second straight monthly gain."},
  "First, Friday. It was a quietly strong finish. [pause] "
  "The Sensex added one hundred sixty-six points, up zero point two one percent, to close at seventy-eight thousand ninety-four. The Nifty rose sixty-six points, up zero point two seven percent, to twenty-four thousand three eighty-three. And the Bank Nifty climbed one hundred seventeen points, also up zero point two one percent. [pause] "
  "But the day is the small story — the week is the big one. That close capped the Nifty's biggest weekly gain in nearly four months, up more than two and a half percent, and a second straight monthly gain. After a rough patch in July, the bulls are firmly back in control coming into this week."),
 ("pm_split", "sm_iconcards",
  {"kicker": "UNDER THE SURFACE — A CLEAR SPLIT", "title": "What Led and What Lagged on Friday", "color": "#22D3EE",
   "items": [
    {"emoji": "🏦", "k": "Financials led the charge", "v": "Bajaj Finance hit a fresh 52-week high after Q1 profit jumped 29% to ₹5,436 cr; Bajaj Finserv and Jio Financial gained too", "chip": "52-WK HIGH"},
    {"emoji": "🚗", "k": "Autos were the best sector", "v": "Nifty Auto rose 1.64% — the top-performing index — riding a blockbuster set of July sales numbers", "chip": "+1.64%"},
    {"emoji": "💻", "k": "IT was the biggest drag", "v": "Nifty IT fell 1.56%; TCS, Infosys, HCL Tech, Tech Mahindra and Wipro all slipped 2 to 3 percent", "chip": "IT -1.56%"},
    {"emoji": "🧴", "k": "FMCG stayed soft", "v": "Nifty FMCG eased 1.05% — the defensives took a back seat as money rotated into financials and autos", "chip": "FMCG -1.05%"},
   ]},
  "Now, look under the surface, because Friday had a very clear split. [pause] "
  "Financials led the charge. Bajaj Finance hit a fresh fifty-two-week high after its June-quarter profit jumped twenty-nine percent to five thousand four hundred thirty-six crore — and Bajaj Finserv and Jio Financial rose with it. [pause] "
  "Autos were the best-performing sector, up one point six four percent, riding a blockbuster set of July sales numbers we'll come to in a moment. [pause] "
  "On the other side, I-T was the biggest drag — down one point five six percent, with T-C-S, Infosys, H-C-L Tech, Tech Mahindra and Wipro all slipping two to three percent. And F-M-C-G stayed soft. The lesson — this was a rotation, money moving into financials and autos and out of I-T and defensives. That rotation is the story to watch again today."),
 ("pm_global", "sm_stats",
  {"kicker": "OVERNIGHT — WALL STREET HIGHER", "title": "Global Cues This Morning",
   "stats": [
    {"label": "Dow Jones", "to": 52485.03, "prefix": "", "suffix": "", "decimals": 2, "color": "#34D399", "sub": "+276.97 pts · +0.53%"},
    {"label": "Nasdaq", "to": 25373.85, "prefix": "", "suffix": "", "decimals": 2, "color": "#34D399", "sub": "≈ +1.0% · Amazon surged"},
    {"label": "Brent crude", "to": 88.16, "prefix": "$", "suffix": "", "decimals": 2, "color": "#34D399", "sub": "-0.98% · eased from the $92 spike"},
   ],
   "note": "A supportive backdrop: US stocks closed higher Friday, the Dow logged a 4th straight winning month, and crude has cooled."},
  "Now, the overnight and weekend cues — and they're supportive. [pause] "
  "Wall Street closed higher on Friday. The Dow rose two hundred seventy-seven points, up zero point five three percent, and logged its fourth straight winning month. The Nasdaq climbed about one percent, powered by Amazon, which surged after strong results. [pause] "
  "And crucially for us — crude oil. Brent eased zero point nine eight percent to around eighty-eight dollars a barrel. That's a big relief. Remember, just two weeks ago Brent had spiked past ninety-two on the U-S–Iran flare-up. Cheaper oil is a genuine tailwind for India — it eases inflation, the import bill, and the rupee. Put it together, and the global setup this morning leans positive."),
 ("pm_weekend", "sm_iconcards",
  {"kicker": "WEEKEND DATA — THE ECONOMY IS HOT", "title": "Three Strong Numbers Over the Weekend", "color": "#34D399",
   "items": [
    {"emoji": "🧾", "k": "GST at ₹2.11 lakh crore", "v": "July collections rose 15.4% year-on-year — one of the strongest prints yet, with import revenue up nearly 29%", "chip": "+15.4% YoY"},
    {"emoji": "🚙", "k": "Auto sales boomed in July", "v": "M&M up 26%, Hyundai a record 75,360 units, Maruti 2.41 lakh — why autos led Friday and stay in focus today", "chip": "RECORD"},
    {"emoji": "🏭", "k": "Factory activity still expanding", "v": "The manufacturing PMI held firmly in expansion, pointing to steady momentum in the real economy", "chip": "EXPANSION"},
   ]},
  "Over the weekend, three data points landed — and all three were strong. [pause] "
  "First, G-S-T. July collections came in at two point one one lakh crore rupees, up fifteen point four percent from a year ago — one of the strongest readings yet, with revenue from imports up nearly twenty-nine percent. That's a sign of a busy, growing economy. [pause] "
  "Second, auto sales. July was a blockbuster — Mahindra up twenty-six percent, Hyundai posting a record seventy-five thousand three hundred sixty units, and Maruti at two point four one lakh. That is exactly why autos led on Friday, and why the auto pack stays in focus at the open today. [pause] "
  "Third, factory activity — the manufacturing P-M-I held firmly in expansion. Three green lights for the domestic economy, right as the week begins."),
 ("pm_rbi", "sm_iconcards",
  {"kicker": "THE WEEK'S BIGGEST EVENT", "title": "RBI Policy — Wednesday, August 5", "color": "#FBBF24",
   "items": [
    {"emoji": "🏛️", "k": "The rate decision", "v": "The Monetary Policy Committee announces its verdict Wednesday — the single biggest swing factor for the whole week", "chip": "AUG 5"},
    {"emoji": "🗣️", "k": "The stance & commentary", "v": "Beyond the rate itself, the Governor's tone on inflation and growth guides where the market heads next", "chip": "WATCH TONE"},
    {"emoji": "🏦", "k": "Who reacts most", "v": "Rate-sensitives — banks, autos, and real estate — will move hardest on the decision and the guidance", "chip": "RATE-SENSITIVE"},
   ]},
  "Now to the week ahead — and it's dominated by one event. [pause] "
  "On Wednesday, the R-B-I's Monetary Policy Committee announces its decision. This is the single biggest swing factor for the entire week. [pause] "
  "And it's not just about the rate itself — it's the stance. The Governor's commentary on inflation and growth will tell the market where policy is headed next, and that guidance often matters more than the number. [pause] "
  "The stocks that react most are the rate-sensitives — the banks, the autos, and the real-estate names. Expect them to swing hardest on Wednesday. Until then, the market may stay a touch cautious ahead of the verdict — so don't over-read Monday and Tuesday's moves."),
 ("pm_earnings", "sm_iconcards",
  {"kicker": "EARNINGS SEASON — HEAVYWEIGHTS DUE", "title": "Big Q1 Results This Week", "color": "#22D3EE",
   "items": [
    {"emoji": "🏦", "k": "State Bank of India", "v": "The country's largest lender — its asset quality and loan growth set the tone for the whole banking pack", "chip": "PSU BANK"},
    {"emoji": "📶", "k": "Bharti Airtel", "v": "A telecom bellwether; watch ARPU — the average revenue per user — and subscriber additions", "chip": "TELECOM"},
    {"emoji": "🛢️", "k": "ONGC · Power Grid · Hindalco", "v": "Energy, power and metals — cyclical heavyweights that move the broader index", "chip": "CYCLICALS"},
    {"emoji": "🛍️", "k": "Titan · Trent", "v": "The consumption story — jewellery and retail; a read on how the Indian shopper is spending", "chip": "CONSUMER"},
   ]},
  "It's also a heavy earnings week, with several index heavyweights reporting. [pause] "
  "The biggest is State Bank of India — the country's largest lender. Its asset quality and loan growth set the tone for the entire banking pack. [pause] "
  "Bharti Airtel reports too — a telecom bellwether. The number to watch there is A-R-P-U, the average revenue per user, along with subscriber additions. [pause] "
  "Then the cyclicals — O-N-G-C in energy, Power Grid, and Hindalco in metals — heavyweights that can move the broader index. And on the consumption side, Titan and Trent give us a fresh read on how the Indian shopper is spending. In earnings season, remember — react to the actual numbers, not the pre-result hype."),
 ("pm_ipo", "sm_iconcards",
  {"kicker": "THE IPO CORNER", "title": "Primary Market — What's Live", "color": "#A78BFA",
   "items": [
    {"emoji": "⚡", "k": "MV Electrosystems — closes TODAY", "v": "Mainboard issue of ₹290 cr, price band ₹400–425; subscription ends today, listing on August 6", "chip": "LAST DAY"},
    {"emoji": "🏗️", "k": "Ardee Industries — opens Aug 5", "v": "A ₹425.87 cr issue, price band ₹50–53, open August 5 to 7; listing expected August 12", "chip": "OPENS AUG 5"},
    {"emoji": "🛠️", "k": "Technocraft Ventures — opens Aug 7", "v": "An EPC infrastructure play; a ₹138 cr fresh issue plus an offer-for-sale, open from August 7", "chip": "OPENS AUG 7"},
   ]},
  "The primary market is busy too. [pause] "
  "M-V Electrosystems, a mainboard issue of two hundred ninety crore with a band of four hundred to four hundred twenty-five rupees, closes for subscription today — it lists on August sixth. [pause] "
  "Then two more open later this week — Ardee Industries, a four hundred twenty-six crore issue at fifty to fifty-three rupees, opens Wednesday the fifth; and Technocraft Ventures, an infrastructure and construction company, opens Friday the seventh. [pause] "
  "A quick, honest word on I-P-Os — do your own homework on the price, the financials, and how the money will be used. And ignore grey-market chatter; it's unofficial and it is not a listing prediction."),
 ("pm_setup", "sm_myths",
  {"kicker": "THE SETUP · A TUG OF WAR", "title": "Tailwinds vs Headwinds Today", "mythLabel": "⚠️ HEADWINDS", "factLabel": "✅ TAILWINDS",
   "pairs": [
    {"m": "RBI policy Wednesday — event risk", "f": "Strong momentum: biggest weekly gain in ~4 months"},
    {"m": "IT sector weak and out of favour", "f": "Crude cooled to ~$88; supportive global cues"},
    {"m": "Nifty nearing 24,500–24,600 resistance", "f": "Hot data: GST, auto sales and DII buying (₹2,260 cr)"},
   ]},
  "So what's the overall setup? A genuine tug of war between strong momentum and event risk. [pause] "
  "On the headwind side — the R-B-I decision on Wednesday is a real event risk, the market may tread carefully into it, I-T remains weak, and the Nifty is now approaching resistance. [pause] "
  "On the tailwind side — momentum is strong after the best week in four months, crude has cooled to around eighty-eight dollars, the weekend data was hot, and domestic institutions bought over two thousand two hundred crore on Friday alone. [pause] "
  "For levels — on the upside, twenty-four thousand five hundred to twenty-four thousand six hundred is the first resistance, and above that sits the two-hundred-day average near twenty-four thousand seven fifty. On the downside, twenty-four thousand one fifty is immediate support, then twenty-four thousand. Reclaiming and holding twenty-four thousand five hundred would keep the rally alive."),
 ("pm_take", "sm_checklist",
  {"kicker": "HOW TO APPROACH THE WEEK", "title": "5 Things to Remember", "color": "#34D399", "icon": "💡",
   "items": [
    "This is a watchlist & setup — NOT a prediction of which stocks will rise",
    "RBI on Wednesday is the master switch — don't over-trade before it",
    "Autos & financials lead; IT is the laggard to watch for a turn",
    "Nifty: hold 24,500 = rally continues; 24,150 is first support",
    "Earnings season = sharp single-stock moves; always use a stop-loss",
   ]},
  "Finally, five things to remember for the week. [pause] "
  "One — this is a watchlist and a setup, not a prediction of which stocks will rise. [pause] "
  "Two — the R-B-I decision on Wednesday is the master switch. It's usually unwise to over-trade in the two days before a big policy event. [pause] "
  "Three — autos and financials are the leaders right now; I-T is the laggard, so watch it for any sign of a turn. [pause] "
  "Four — on levels, holding twenty-four thousand five hundred keeps the rally alive; twenty-four thousand one fifty is the first support below. [pause] "
  "Five — with earnings season in full swing, expect sharp single-stock moves. Always use a stop-loss."),
 ("pm_recap", "sm_recap",
  {"title": "3 August — Pre-Market at a Glance",
   "items": [
    "Friday: Sensex +166 (78,094), Nifty +66 (24,383) — strong finish",
    "Best week in ~4 months; autos & financials led, IT lagged",
    "Global: Wall Street up, Brent eased to ~$88",
    "Weekend data hot: GST +15.4%, record July auto sales",
    "Big event: RBI policy Wednesday, Aug 5",
    "Earnings: SBI, Airtel, ONGC, Titan, Trent + more",
    "Nifty: 24,500 resistance · 24,150 support",
   ],
   "closer": "Momentum is strong — but the RBI runs the week. Trade the reaction, not the prediction."},
  "August third, pre-market at a glance. [pause] "
  "Friday was a strong finish — the Sensex up one hundred sixty-six points and the Nifty up sixty-six, capping the best week in nearly four months. [pause] "
  "Under the surface, autos and financials led, while I-T lagged. [pause] "
  "Globally, Wall Street closed higher and Brent crude eased to around eighty-eight dollars — a relief for India. [pause] "
  "The weekend data was hot — G-S-T up fifteen point four percent, and record July auto sales. [pause] "
  "But the week belongs to one event — the R-B-I policy decision on Wednesday. [pause] "
  "On earnings — S-B-I, Airtel, O-N-G-C, Titan and Trent lead a heavy week. [pause] "
  "And the level that matters — holding twenty-four thousand five hundred keeps the rally alive. [pause] "
  "Remember — momentum is strong, but the R-B-I runs the week. Trade the reaction, not the prediction. [pause] "
  "This information is aggregated from public sources — for analysis only, not investment advice. Have a great trading week, and thanks for watching."),
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
