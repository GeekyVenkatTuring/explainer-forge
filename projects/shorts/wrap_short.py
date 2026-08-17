#!/usr/bin/env python3
"""Standalone vertical Shorts for the 21-Jul-2026 market wrap (Telugu + English).
Uses the `Short` composition. ~50-60s recap, NO captions. Emits mp4 + youtube.md + instagram.md.
Does NOT touch the course shorts.csv files. Usage: python3 wrap_short.py"""
import json, os, re, subprocess, time

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
COMPOSER = os.path.join(REPO, "composer"); PUBLIC = os.path.join(COMPOSER, "public", "short")
RAW = os.path.join(os.path.dirname(__file__), "assets", "raw"); ART = os.path.join(os.path.dirname(__file__), "artifacts")
GV = os.path.expanduser("~/Downloads/generated_videos")
for d in (PUBLIC, RAW, ART): os.makedirs(d, exist_ok=True)
VOICE = {"te": "te-IN-ShrutiNeural", "en": "en-IN-NeerjaNeural"}; RATE = "-4%"; PAUSE = 0.4

SHORTS = [
 dict(sid="mw21-recap", lang="te", folder="stock-market-telugu/shorts", accent="#FB7185",
   badge="21 జూలై", title="మార్కెట్\nఎందుకు పడింది?", sub="Sensex −238 · Nifty −51",
   keyword="2వ రోజు పతనం", brand="MARKET WRAP · 21 JUL",
   highlights=["సెన్సెక్స్ −238 (77,470) · నిఫ్టీ −51 (24,188)","క్రూడ్ $90+ — హౌతీ / హోర్ముజ్ ఆందోళన",
     "పడినవి: Cipla, TCS, Infosys, HDFC","పెరిగినవి: కెమికల్, సిమెంట్, మిడ్‌క్యాప్","బ్రెడ్త్ పాజిటివ్ — ఇరుకైన లార్జ్‌క్యాప్ షాక్"],
   script=("జూలై ఇరవై ఒకటి — మార్కెట్ వరుసగా రెండో రోజు పడింది. [pause] "
     "సెన్సెక్స్ రెండు వందల ముప్పై ఎనిమిది పాయింట్లు పడి డెబ్బై ఏడు వేల నాలుగు వందల డెబ్బై వద్ద, నిఫ్టీ యాభై ఒక్క పాయింట్లు పడి ఇరవై నాలుగు వేల ఒక వంద ఎనభై ఏడు వద్ద ముగిసింది. [pause] "
     "కారణం — హౌతీలు సౌదీపై దిగ్బంధం హెచ్చరించడంతో క్రూడ్ తొంభై డాలర్లు దాటింది. దీంతో IT, PSU బ్యాంక్, HDFC షేర్లు పడ్డాయి, విదేశీ సంస్థలు అమ్మేశాయి. [pause] "
     "సిప్లా, డాక్టర్ రెడ్డీస్, TCS, ఇన్ఫోసిస్ ఎక్కువ పడ్డాయి. కానీ కెమికల్, సిమెంట్ సెక్టార్లు పెరిగాయి. [pause] "
     "ముఖ్యంగా — మిడ్‌క్యాప్, స్మాల్‌క్యాప్ పెరిగాయి. అంటే ఇది ఇరుకైన లార్జ్‌క్యాప్ పతనం, భారీ సెల్-ఆఫ్ కాదు. [pause] "
     "SIP పెట్టుబడిదారులకు ఇలాంటి ఎర్ర రోజు కేవలం నాయిస్. ఇది విశ్లేషణ మాత్రమే — పెట్టుబడి సలహా కాదు."),
   ytdesc="21 జూలై 2026 మార్కెట్ ఎందుకు పడింది — 60 సెకన్లలో తెలుగులో.",
   tags=["market wrap telugu","stock market today telugu","nifty sensex today","why market fell telugu","shorts"]),
 dict(sid="mw21e-recap", lang="en", folder="equity-fno-english/shorts", accent="#FB7185",
   badge="21 JULY", title="Why Did the\nMarket Fall?", sub="Sensex −238 · Nifty −51",
   keyword="2nd day down", brand="MARKET WRAP · 21 JUL",
   highlights=["Sensex −238 (77,470) · Nifty −51 (24,188)","Crude $90+ — Houthi / Hormuz fears",
     "Losers: Cipla, TCS, Infosys, HDFC","Gainers: Chemical, Cement, Midcaps","Breadth positive — a narrow large-cap dip"],
   script=("July twenty-first — the market fell for a second straight day. [pause] "
     "The Sensex dropped two hundred thirty-eight points to 77,470, and the Nifty fell fifty-one points to 24,188. [pause] "
     "The reason — the Houthis threatened a blockade on Saudi Arabia, pushing crude past ninety dollars. That dragged down IT, PSU banks, and HDFC, while foreign investors kept selling. [pause] "
     "The biggest losers were Cipla, Dr Reddy's, TCS, and Infosys. But chemical and cement sectors rose. [pause] "
     "And crucially — midcaps and smallcaps went up. So this was a narrow, large-cap fall, not a broad sell-off. [pause] "
     "For SIP investors, a red day like this is just noise. This is analysis only — not investment advice."),
   ytdesc="Why the Indian market fell on 21 July 2026 — explained in 60 seconds.",
   tags=["stock market today","market wrap","nifty sensex today","why market fell today","shorts"]),
]

def ffdur(p): return round(float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","default=noprint_wrappers=1:nokey=1",p],capture_output=True,text=True).stdout.strip()),3)

def tts(sid, lang, text):
    wav = os.path.join(PUBLIC, f"{sid}.wav")
    chunks = [c.strip() for c in text.split("[pause]") if c.strip()]; paths=[]
    for ci,ch in enumerate(chunks):
        cp = os.path.join(RAW, f"{sid}_c{ci}.wav"); mp3 = cp[:-4]+".mp3"
        for a in range(6):
            r = subprocess.run(["edge-tts","--voice",VOICE[lang],f"--rate={RATE}","--text",ch,"--write-media",mp3],capture_output=True)
            if r.returncode==0 and os.path.exists(mp3) and os.path.getsize(mp3)>0: break
            time.sleep(3+a*4)
        else: raise RuntimeError(f"tts failed {sid} {ci}")
        subprocess.run(["ffmpeg","-y","-i",mp3,"-ar","24000","-ac","1",cp],check=True,capture_output=True); os.remove(mp3); paths.append(cp)
    sil = os.path.join(RAW,"_p.wav")
    if not os.path.exists(sil): subprocess.run(["ffmpeg","-y","-f","lavfi","-i","anullsrc=r=24000:cl=mono","-t",str(PAUSE),sil],check=True,capture_output=True)
    lst = os.path.join(RAW,f"{sid}_l.txt")
    with open(lst,"w") as f:
        for i,pp in enumerate(paths):
            f.write(f"file '{pp}'\n")
            if i<len(paths)-1: f.write(f"file '{sil}'\n")
    subprocess.run(["ffmpeg","-y","-f","concat","-safe","0","-i",lst,"-c","copy",wav],check=True,capture_output=True)
    return ffdur(wav)

DISC = {"te":"⚠️ ఇది విద్య కోసమే — పెట్టుబడి సలహా కాదు.","en":"⚠️ Educational only — not investment advice."}
for s in SHORTS:
    dur = tts(s["sid"], s["lang"], s["script"]) + 1.0
    props = {k:s[k] for k in ("badge","title","sub","keyword","accent","brand","highlights")}
    props.update({"audioSrc":f"short/{s['sid']}.wav","durationSec":round(dur,2)})
    pj = os.path.join(ART,f"{s['sid']}.json"); json.dump(props,open(pj,"w"),ensure_ascii=False)
    subdir = os.path.join(GV,s["folder"]); os.makedirs(subdir,exist_ok=True)
    out = os.path.join(subdir,f"{s['sid']}-short.mp4")
    subprocess.run(["npx","remotion","render","Short",out,f"--props={pj}","--concurrency=4"],cwd=COMPOSER,capture_output=True)
    ok = os.path.exists(out) and ffdur(out)>40
    plain = re.sub(r"\s+"," ",s["script"].replace("[pause]"," ")).strip()
    tags = ", ".join(s["tags"])
    ttl = f"{s['title'].replace(chr(10),' ')} #Shorts"
    yt = f"# {ttl}\n\n**Description**\n{s['ytdesc']}\n\n{plain}\n\nFull video on the channel. ▶️\n\n{DISC[s['lang']]}\n\n#Shorts #StockMarket #MarketWrap\n\n**Tags**\n{tags}"
    ig = f"**Reel — {s['title'].replace(chr(10),' ')}**\n\n{s['ytdesc']}\n\nFull video → link in bio.\n{DISC[s['lang']]}\n\n#reels #stockmarket #marketwrap #nifty #sensex #{'telugu' if s['lang']=='te' else 'investing'}"
    open(os.path.join(subdir,f"{s['sid']}-short.youtube.md"),"w").write(yt)
    open(os.path.join(subdir,f"{s['sid']}-short.instagram.md"),"w").write(ig)
    print(f"  {'OK ' if ok else 'ERR'} {s['sid']} ({props['durationSec']}s) -> {s['folder']}", flush=True)
print("done")
