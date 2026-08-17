#!/usr/bin/env python3
"""Pre-Market Brief (Telugu) — Tue 21 July 2026. Reuses `sm` scene set.
HONEST framing: a catalyst WATCHLIST, not a guaranteed-gainers list. Facts verified
in research/premarket-21jul2026.md. Not advice. Usage: python3 build.py [pm01]
"""
import json, os, re, subprocess, sys

VOICE = "te-IN-ShrutiNeural"; RATE = "-4%"; GAP = 0.5; PAUSE = 0.55; PREFIX = "sm"
ROOT = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(ROOT, "..", ".."))
PUBLIC = os.path.join(REPO, "composer", "public", PREFIX); RAW = os.path.join(ROOT, "assets", "raw"); FIN = os.path.join(ROOT, "assets")
for d in (PUBLIC, RAW, os.path.join(ROOT, "artifacts"), os.path.join(ROOT, "renders")):
    os.makedirs(d, exist_ok=True)

CHAPTERS = {
 "pm01": [
 ("pm_title", "sm_ptitle",
  {"title": "రేపటి ప్రీ-మార్కెట్ విశ్లేషణ", "sub": "మంగళవారం · 21 జూలై 2026 · నిఫ్టీ వీక్లీ ఎక్స్‌పైరీ", "kicker": "PRE-MARKET · 21 JUL"},
  "రేపు మంగళవారం, జూలై ఇరవై ఒకటి. నిఫ్టీ వీక్లీ ఎక్స్‌పైరీ రోజు. [pause] "
  "ముందుగా ఒక నిజాయితీ మాట — రేపు ఏ షేర్ ఖచ్చితంగా పెరుగుతుందో ఎవరూ చెప్పలేరు. అలా చెప్పేవాడు మోసగాడే. [pause] "
  "కానీ — ఏ షేర్లపై వార్తలు, ఫలితాలు, ట్రిగ్గర్లు ఉన్నాయో చూడగలం. అదే ఈ వాచ్‌లిస్ట్. "
  "లార్జ్, మిడ్, స్మాల్ క్యాప్ — మూడింటిలోనూ ఫోకస్‌లో ఉన్న షేర్లు చూద్దాం."),
 ("pm_setup", "sm_stats",
  {"kicker": "THE SETUP", "title": "రేపటి ఓపెనింగ్ సెటప్",
   "stats": [
    {"label": "GIFT Nifty", "to": 24300, "color": "#FB7185", "sub": "−0.42% · నిన్నటి క్లోజ్ 24,404"},
    {"label": "బ్రెంట్ క్రూడ్", "to": 90, "prefix": "$", "suffix": "+", "color": "#FBBF24", "sub": "మిడిల్ ఈస్ట్ · OMC/ఆటో ఒత్తిడి"},
    {"label": "FII నిన్నటి అమ్మకం", "to": 4200, "prefix": "−₹", "suffix": " కోట్లు", "color": "#FB7185", "sub": "DII కొనుగోలుతో ఆసరా"},
   ],
   "note": "రేపు నిఫ్టీ వీక్లీ ఎక్స్‌పైరీ (మంగళవారం) — హెచ్చుతగ్గులు ఎక్కువ. GIFT Nifty మెత్తని ఓపెనింగ్ సూచిస్తోంది."},
  "ముందు రేపటి ఓపెనింగ్ సెటప్. [pause] "
  "GIFT Nifty — రేపటి ఓపెనింగ్‌కు అతి ముఖ్యమైన సూచిక — ఇరవై నాలుగు వేల మూడు వందల వద్ద, దాదాపు అర శాతం తక్కువగా ఉంది. అంటే మెత్తని, జాగ్రత్తగల ఓపెనింగ్. [pause] "
  "బ్రెంట్ క్రూడ్ తొంభై డాలర్లు దాటింది — మిడిల్ ఈస్ట్ ఉద్రిక్తతతో. ఇది ఆయిల్ కంపెనీలు, ఆటో షేర్లపై ఒత్తిడి పెంచుతుంది. [pause] "
  "నిన్న విదేశీ సంస్థలు నాలుగు వేల రెండు వందల కోట్లు అమ్మాయి. [pause] "
  "పైగా రేపు నిఫ్టీ వీక్లీ ఎక్స్‌పైరీ — మంగళవారం. ఈ రోజుల్లో హెచ్చుతగ్గులు, ఊహించని కదలికలు సహజం. [pause] "
  "కాబట్టి రేపటి మూడ్ — కొంచెం జాగ్రత్త."),
 ("pm_large", "sm_iconcards",
  {"kicker": "LARGE CAP · IN FOCUS", "title": "లార్జ్ క్యాప్ — ఫోకస్‌లో (ట్రిగ్గర్‌తో)", "color": "#22D3EE",
   "items": [
    {"emoji": "🛢️", "k": "Reliance", "v": "Q1 లాభం ₹23,196 కోట్లు (+6.1%); ఆదాయం +24.5% → ₹3.4 లక్షల కోట్లు; Jio లాభం +9.2%", "chip": "రిజల్ట్"},
    {"emoji": "🟢", "k": "ICICI Bank", "v": "Q1 లాభం +15.9% → ₹14,804 కోట్లు; NII +12.7% — బలమైన ఫలితం", "chip": "బలం"},
    {"emoji": "🟡", "k": "HDFC Bank", "v": "Q1 లాభం +5% కానీ NIM మిస్ — నిన్న పడింది; రేపు రియాక్షన్ చూడాలి", "chip": "మిక్స్డ్"},
    {"emoji": "💎", "k": "Titan", "v": "జ్యువెలరీ మొమెంటమ్ — నెలలో +14%, ఆల్-టైమ్ హై; బంగారం ధరల ఊతం", "chip": "మొమెంటమ్"},
   ]},
  "ఇప్పుడు లార్జ్ క్యాప్‌లో ఫోకస్‌లో ఉన్న షేర్లు — ప్రతి ఒక్కదానికీ ఒక కారణం ఉంది. [pause] "
  "మొదటిది — రిలయన్స్. Q1 లాభం ఇరవై మూడు వేల కోట్లు, ఆదాయం ఇరవై నాలుగున్నర శాతం పెరిగి మూడున్నర లక్షల కోట్లకు. Jio లాభం తొమ్మిది శాతం పెరిగింది. రేపు దీనిపై దృష్టి ఉంటుంది. [pause] "
  "రెండోది — ICICI బ్యాంక్. Q1 లాభం పదిహేను శాతానికి పైగా పెరిగి పద్నాలుగు వేల ఎనిమిది వందల కోట్లకు. చాలా బలమైన ఫలితం. [pause] "
  "మూడోది — HDFC బ్యాంక్. లాభం ఐదు శాతం పెరిగినా, NIM మిస్‌తో నిన్న పడింది. రేపు మార్కెట్ ఎలా స్పందిస్తుందో చూడాలి. [pause] "
  "నాలుగోది — Titan. బంగారం ధరల ఊతంతో నెలలో పద్నాలుగు శాతం పెరిగి ఆల్-టైమ్ హై తాకింది. [pause] "
  "గుర్తుంచుకోండి — ఫోకస్‌లో ఉంది అంటే వార్త ఉంది అని — పెరుగుతుంది అని కాదు."),
 ("pm_gold", "sm_iconcards",
  {"kicker": "MID & SMALL CAP · GOLD THEME", "title": "మిడ్/స్మాల్ క్యాప్ — జ్యువెలరీ థీమ్", "color": "#FBBF24",
   "items": [
    {"emoji": "🏅", "k": "Kalyan Jewellers", "v": "మిడ్ క్యాప్ — Q1 ఆదాయం +38% YoY; 4 రోజుల్లో +47% ర్యాలీ", "chip": "మిడ్"},
    {"emoji": "💍", "k": "Thangamayil", "v": "స్మాల్ క్యాప్ — నెలలో +28%, ఆల్-టైమ్ హై", "chip": "స్మాల్"},
    {"emoji": "✨", "k": "Sky Gold", "v": "స్మాల్ క్యాప్ — నెలలో +21%, ఆల్-టైమ్ హై", "chip": "స్మాల్"},
    {"emoji": "📈", "k": "అసలు డ్రైవర్", "v": "రికార్డు బంగారం ధరలు + పండుగ/పెళ్లి డిమాండ్ + అసంఘటిత రంగం నుండి మార్కెట్ షేర్", "chip": "గోల్డ్"},
   ]},
  "ఇప్పుడు మిడ్, స్మాల్ క్యాప్‌లో అత్యంత వేడిగా ఉన్న థీమ్ — జ్యువెలరీ, బంగారం. [pause] "
  "మిడ్ క్యాప్‌లో — Kalyan Jewellers. Q1 ఆదాయం ముప్పై ఎనిమిది శాతం పెరిగింది. నాలుగు రోజుల్లోనే షేర్ నలభై ఏడు శాతం ఎగిసింది. [pause] "
  "స్మాల్ క్యాప్‌లో — Thangamayil నెలలో ఇరవై ఎనిమిది శాతం, Sky Gold ఇరవై ఒక్క శాతం పెరిగి, రెండూ ఆల్-టైమ్ హై తాకాయి. [pause] "
  "అసలు డ్రైవర్ ఏమిటి? రికార్డు స్థాయి బంగారం ధరలు, పెళ్లిళ్ల సీజన్ డిమాండ్, పైగా అసంఘటిత చిన్న దుకాణాల నుండి ఈ బ్రాండెడ్ కంపెనీలు మార్కెట్ షేర్ లాక్కోవడం. [pause] "
  "కానీ ఒక పెద్ద హెచ్చరిక — ఇవి ఇప్పటికే బాగా పెరిగి ఆల్-టైమ్ హై వద్ద ఉన్నాయి. అంత పెరిగిన షేర్లు వేగంగా రివర్స్ కూడా అవ్వొచ్చు."),
 ("pm_honest", "sm_myths",
  {"kicker": "THE HONEST TRUTH", "title": "రేపు ఇవి పెరుగుతాయా? — నిజం",
   "pairs": [
    {"m": "ఈ వీడియో చెప్పిన షేర్లు రేపు ఖచ్చితంగా పెరుగుతాయి", "f": "ఇది వాచ్‌లిస్ట్ — ట్రిగ్గర్ ఉన్న షేర్లు; దిశ ఎవరూ గ్యారంటీ చేయలేరు"},
    {"m": "మంచి Q1 ఫలితం = రేపు షేర్ పెరుగుతుంది", "f": "నిన్న HDFC లాభం పెరిగినా పడింది — 'సెల్ ఆన్ న్యూస్'"},
    {"m": "ఎక్స్‌పైరీ రోజు సులభంగా సంపాదించొచ్చు", "f": "ఎక్స్‌పైరీ = అధిక హెచ్చుతగ్గులు, ఊహించని రివర్సల్‌లు"},
   ]},
  "ఇక్కడ అతి ముఖ్యమైన నిజం. రేపు ఇవి పెరుగుతాయా? [pause] "
  "మొదటి అపోహ — ఈ వీడియో చెప్పిన షేర్లు రేపు ఖచ్చితంగా పెరుగుతాయని. [pause] "
  "నిజం — ఇది కేవలం వాచ్‌లిస్ట్. వీటిపై వార్తలు, ట్రిగ్గర్లు ఉన్నాయి. కానీ రేపటి దిశను ఎవరూ గ్యారంటీ చేయలేరు. [pause] "
  "రెండో అపోహ — మంచి Q1 ఫలితం వస్తే రేపు షేర్ పెరుగుతుందని. [pause] "
  "నిన్ననే చూశాం — HDFC బ్యాంక్ లాభం పెరిగినా, మార్జిన్ మిస్‌తో పడింది. దీన్నే 'సెల్ ఆన్ న్యూస్' అంటారు. [pause] "
  "మూడో అపోహ — ఎక్స్‌పైరీ రోజు సులభంగా సంపాదించొచ్చని. [pause] "
  "నిజానికి ఎక్స్‌పైరీ రోజు అధిక హెచ్చుతగ్గులు, ఊహించని రివర్సల్‌లు ఉంటాయి — ఇది అనుభవజ్ఞులకే కష్టం. [pause] "
  "కాబట్టి — దీన్ని జోస్యంగా కాదు, ఒక వాచ్‌లిస్ట్‌గా వాడండి."),
 ("pm_use", "sm_checklist",
  {"kicker": "HOW TO USE", "title": "ఈ వాచ్‌లిస్ట్‌ను ఎలా వాడాలి", "color": "#34D399", "icon": "🧭",
   "items": [
    "ఇది వాచ్‌లిస్ట్ — ముందే గుడ్డిగా కొనమని కాదు",
    "ఉదయం మొదటి 15–30 నిమిషాల కదలిక చూసి నిర్ణయించండి",
    "ఫలితాలను మార్కెట్ ఎలా తీసుకుందో గమనించండి (గ్యాప్-అప్/డౌన్)",
    "స్టాప్-లాస్ లేకుండా ఎంట్రీ వద్దు — ముఖ్యంగా ఎక్స్‌పైరీ రోజు",
    "SIP పెట్టుబడిదారులకు రోజువారీ కదలిక అనవసరం — ప్లాన్ కొనసాగించండి",
   ]},
  "మరి ఈ వాచ్‌లిస్ట్‌ను బాధ్యతగా ఎలా వాడాలి? ఐదు సూత్రాలు. [pause] "
  "ఒకటి — ఇది వాచ్‌లిస్ట్ మాత్రమే. ఓపెనింగ్‌లోనే గుడ్డిగా కొనవద్దు. [pause] "
  "రెండు — ఉదయం మొదటి పదిహేను, ముప్పై నిమిషాల కదలికను గమనించి, అప్పుడు నిర్ణయించండి. [pause] "
  "మూడు — ఫలితాలు వచ్చిన షేర్లు గ్యాప్-అప్ అయ్యాయా, గ్యాప్-డౌన్ అయ్యాయా — మార్కెట్ ఆ వార్తను ఎలా తీసుకుందో చూడండి. [pause] "
  "నాలుగు — స్టాప్-లాస్ లేకుండా ఎప్పుడూ ఎంట్రీ ఇవ్వొద్దు. ఎక్స్‌పైరీ రోజు ఇది మరింత ముఖ్యం. [pause] "
  "ఐదు — మీరు దీర్ఘకాల SIP పెట్టుబడిదారు అయితే — రోజువారీ ఈ హడావిడి మీకు అనవసరం. మీ ప్లాన్ ప్రకారం కొనసాగండి. [pause] "
  "వాచ్‌లిస్ట్ ఒక పరికరం — జోస్యం కాదు."),
 ("pm_recap", "sm_recap",
  {"title": "రేపటి ప్రీ-మార్కెట్ — సారాంశం",
   "items": [
    "సెటప్: GIFT Nifty −0.42% · క్రూడ్ $90+ · ఎక్స్‌పైరీ రోజు",
    "లార్జ్ ఫోకస్: Reliance, ICICI (బలం), HDFC (మిక్స్డ్)",
    "గోల్డ్ థీమ్: Titan · Kalyan (మిడ్) · Thangamayil, Sky Gold (స్మాల్)",
    "డ్రైవర్: రికార్డు బంగారం ధరలు + డిమాండ్",
    "ఇది వాచ్‌లిస్ట్ — జోస్యం కాదు; దిశ ఎవరూ గ్యారంటీ చేయలేరు",
   ],
   "closer": "జోస్యం చెప్పేవాడు కాదు — ప్లాన్ ఉన్నవాడే గెలుస్తాడు."},
  "రేపటి ప్రీ-మార్కెట్ సారాంశం. [pause] "
  "సెటప్ — GIFT Nifty మెత్తగా, క్రూడ్ తొంభై దాటి, రేపు ఎక్స్‌పైరీ రోజు. [pause] "
  "లార్జ్ క్యాప్ ఫోకస్ — రిలయన్స్, ICICI బలంగా, HDFC మిక్స్డ్. [pause] "
  "గోల్డ్ థీమ్ — Titan, మిడ్ క్యాప్ Kalyan, స్మాల్ క్యాప్ Thangamayil, Sky Gold. [pause] "
  "అసలు డ్రైవర్ — రికార్డు స్థాయి బంగారం ధరలు, బలమైన డిమాండ్. [pause] "
  "కానీ మళ్ళీ చెబుతున్నాను — ఇది వాచ్‌లిస్ట్, జోస్యం కాదు. రేపటి దిశను ఎవరూ గ్యారంటీ చేయలేరు. [pause] "
  "జోస్యం చెప్పేవాడు కాదు — ప్లాన్, స్టాప్-లాస్ ఉన్నవాడే మార్కెట్‌లో నిలుస్తాడు. [pause] "
  "ఈ సమాచారం బహిరంగ వార్తల నుండి సేకరించింది — విశ్లేషణ కోసమే, పెట్టుబడి సలహా కాదు. మీ నిర్ణయాలకు నిపుణుల సలహా తీసుకోండి. చూసినందుకు ధన్యవాదాలు."),
 ],
}

def ffdur(path):
    out = subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","default=noprint_wrappers=1:nokey=1",path],capture_output=True,text=True,check=True)
    return round(float(out.stdout.strip()),3)

def tts_chunk(path, text):
    mp3 = path[:-4]+".mp3"
    subprocess.run(["edge-tts","--voice",VOICE,f"--rate={RATE}","--text",text,"--write-media",mp3],check=True,capture_output=True)
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
