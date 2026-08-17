#!/usr/bin/env python3
"""Market Wrap (Telugu) — 20 July 2026 post-close. Reuses `sm` scene set.
Every number verified in research/wrap-20jul2026.md. Info aggregation, not advice.
Usage: python3 build.py            (all)   |   python3 build.py md01
"""
import json, os, re, subprocess, sys

VOICE = "te-IN-ShrutiNeural"; RATE = "-4%"; GAP = 0.5; PAUSE = 0.55; PREFIX = "sm"
ROOT = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(ROOT, "..", ".."))
PUBLIC = os.path.join(REPO, "composer", "public", PREFIX); RAW = os.path.join(ROOT, "assets", "raw"); FIN = os.path.join(ROOT, "assets")
for d in (PUBLIC, RAW, os.path.join(ROOT, "artifacts"), os.path.join(ROOT, "renders")):
    os.makedirs(d, exist_ok=True)

CHAPTERS = {
 "md01": [
 ("md_title", "sm_ptitle",
  {"title": "మార్కెట్ ఎందుకు పడింది?", "sub": "జూలై 20, 2026 · సోమవారం · పోస్ట్-మార్కెట్ విశ్లేషణ", "kicker": "MARKET WRAP · 20 JUL 2026"},
  "జూలై ఇరవై, రెండు వేల ఇరవై ఆరు — సోమవారం. మార్కెట్ మూడున్నరకు ముగిసింది. [pause] "
  "ఈ రోజు నిఫ్టీ, సెన్సెక్స్ ఎందుకు పడ్డాయి? ఏ వార్తలు వాటిని కదిలించాయి? [pause] "
  "పది షేర్లను తీసుకుని — ఏ వార్త దేన్ని ఎలా ప్రభావితం చేసిందో విశ్లేషిద్దాం. "
  "ఇది సమాచార విశ్లేషణ మాత్రమే — పెట్టుబడి సలహా కాదు."),
 ("md_snap", "sm_stats",
  {"kicker": "INDEX SNAPSHOT", "title": "ముగింపు గణాంకాలు — 20 జూలై",
   "stats": [
    {"label": "సెన్సెక్స్", "to": 77708, "prefix": "", "suffix": "", "color": "#FB7185", "sub": "−443 pts · −0.57%"},
    {"label": "నిఫ్టీ 50", "to": 24238, "prefix": "", "suffix": "", "color": "#FB7185", "sub": "−96 pts · −0.39%"},
    {"label": "FII నికర అమ్మకం", "to": 4200, "prefix": "−₹", "suffix": " కోట్లు", "color": "#FBBF24", "sub": "DII కొనుగోలుతో ఆసరా"},
   ],
   "note": "కానీ మిడ్‌క్యాప్ +0.6%, స్మాల్‌క్యాప్ +0.16% పెరిగాయి — బ్రెడ్త్ పాజిటివ్. అంటే పతనం పరిమితం."},
  "ముందు ముగింపు గణాంకాలు చూద్దాం. [pause] "
  "సెన్సెక్స్ నాలుగు వందల నలభై మూడు పాయింట్లు పడి, డెబ్బై ఏడు వేల ఏడు వందల ఎనిమిది వద్ద ముగిసింది. అర శాతం పైనే తగ్గింది. [pause] "
  "నిఫ్టీ ఫిఫ్టీ తొంభై ఆరు పాయింట్లు పడి, ఇరవై నాలుగు వేల రెండు వందల ముప్పై ఎనిమిది వద్ద నిలిచింది. [pause] "
  "విదేశీ సంస్థలు — FIIలు — దాదాపు నాలుగు వేల రెండు వందల కోట్లు అమ్మేశాయి. దేశీయ సంస్థలు కొనడంతో పతనం కొంత ఆగింది. [pause] "
  "కానీ ఒక ముఖ్యమైన విషయం — మిడ్‌క్యాప్, స్మాల్‌క్యాప్ ఇండెక్స్‌లు పెరిగాయి. [pause] "
  "అంటే మార్కెట్‌లో ఎక్కువ షేర్లు నిజానికి పచ్చగానే ఉన్నాయి. ఇది భారీ పతనం కాదు — కొన్ని పెద్ద షేర్ల ప్రభావం మాత్రమే."),
 ("md_why", "sm_iconcards",
  {"kicker": "WHY IT FELL", "title": "పతనానికి 4 కారణాలు", "color": "#FB7185",
   "items": [
    {"emoji": "🏦", "k": "ప్రైవేట్ బ్యాంక్ మార్జిన్", "v": "HDFC, Axis బ్యాంక్‌ల Q1 NIM (మార్జిన్) అంచనాలను అందుకోలేదు — ఐదు శాతం పడ్డాయి", "chip": "ప్రధాన కారణం"},
    {"emoji": "🛢️", "k": "US–ఇరాన్ ఉద్రిక్తత", "v": "బ్రెంట్ క్రూడ్ 90 డాలర్లు దాటింది — ద్రవ్యోల్బణం, దిగుమతి బిల్లు, రూపాయిపై ఒత్తిడి", "chip": "$90+"},
    {"emoji": "📤", "k": "FII అమ్మకం", "v": "విదేశీ సంస్థల నికర అమ్మకం, బలహీన ఆసియా మార్కెట్ సంకేతాలు", "chip": "−₹4,200Cr"},
    {"emoji": "🛡️", "k": "పరిమితం చేసినవి", "v": "PSU బ్యాంకులు, ఫార్మా, మెటల్, రిటైల్ షేర్లు పెరగడంతో నష్టం ఆగింది", "chip": "కుషన్"},
   ]},
  "మరి ఎందుకు పడింది? నాలుగు కారణాలు. [pause] "
  "అన్నిటికంటే ముఖ్యమైనది — ప్రైవేట్ బ్యాంకుల మార్జిన్. [pause] "
  "HDFC బ్యాంక్, Axis బ్యాంక్ — వీటి మొదటి త్రైమాసిక ఫలితాల్లో NIM, అంటే నికర వడ్డీ మార్జిన్, అంచనాల కంటే తక్కువ వచ్చింది. రెండూ దాదాపు ఐదు శాతం పడ్డాయి. [pause] "
  "రెండోది — అమెరికా, ఇరాన్ మధ్య ఉద్రిక్తతతో బ్రెంట్ క్రూడ్ ధర తొంభై డాలర్లు దాటింది. ఇది ద్రవ్యోల్బణం, దిగుమతి బిల్లు, రూపాయిపై ఒత్తిడి పెంచుతుంది. [pause] "
  "మూడోది — విదేశీ సంస్థల అమ్మకం, బలహీన ఆసియా సంకేతాలు. [pause] "
  "నాలుగోది శుభవార్త — PSU బ్యాంకులు, ఫార్మా, మెటల్, రిటైల్ షేర్లు పెరగడంతో మొత్తం పతనం పరిమితమైంది."),
 ("md_losers", "sm_iconcards",
  {"kicker": "TOP LOSERS", "title": "ఈ రోజు ఎక్కువ పడిన షేర్లు", "color": "#FB7185",
   "items": [
    {"emoji": "🔻", "k": "Axis Bank", "v": "నిఫ్టీలో అతిపెద్ద నష్టం — NIM 16 bps తగ్గి 3.46%; విశ్లేషకులు అంచనాలు తగ్గించారు", "chip": "−5%+"},
    {"emoji": "🔻", "k": "HDFC Bank", "v": "NIM 3.53% నుండి 3.4%కి; లాభం పెరిగినా మార్జిన్ మిస్; ఇండెక్స్‌లో అత్యధిక వెయిట్", "chip": "−5%"},
    {"emoji": "🚗", "k": "Maruti Suzuki", "v": "టాప్ లూజర్లలో ఒకటి — 2026లో ~25% డీ-రేటింగ్; క్రూడ్ పెరుగుదల ఆటోలకు ప్రతికూలం", "chip": "లూజర్"},
    {"emoji": "📱", "k": "Paytm", "v": "Q1 ఫలితాలు + బోనస్ ప్రకటన తర్వాత 'సెల్ ఆన్ న్యూస్' — నెలలో 21% ర్యాలీ తర్వాత ప్రాఫిట్ బుకింగ్", "chip": "−1.5%"},
   ]},
  "ఇప్పుడు ఈ రోజు ఎక్కువ పడిన షేర్లు, వాటి వెనుక వార్తలు. [pause] "
  "మొదటిది — Axis బ్యాంక్. నిఫ్టీలో అతిపెద్ద నష్టం. NIM పదహారు బేసిస్ పాయింట్లు తగ్గి మూడు పాయింట్ నలభై ఆరు శాతానికి చేరింది. దీంతో విశ్లేషకులు అంచనాలు తగ్గించారు. [pause] "
  "రెండోది — HDFC బ్యాంక్. NIM మూడు పాయింట్ ఐదు మూడు నుండి మూడు పాయింట్ నలుగురికి పడింది. లాభం పెరిగినా, మార్జిన్ తగ్గడంతో షేర్ పడింది. ఇది ఇండెక్స్‌లో అత్యధిక వెయిటేజీ ఉన్న షేర్ కావడంతో, నిఫ్టీని ఎక్కువగా లాగింది. [pause] "
  "మూడోది — మారుతి సుజుకి. ఈ రోజు టాప్ లూజర్లలో ఒకటి. ఇది ఇప్పటికే రెండు వేల ఇరవై ఆరులో దాదాపు ఇరవై ఐదు శాతం పడింది — డిమాండ్, మార్జిన్ ఆందోళనలతో. క్రూడ్ ధర పెరగడం ఆటో షేర్లకు మరో ప్రతికూలం. [pause] "
  "నాలుగోది — Paytm. మంచి Q1 ఫలితాలు, బోనస్ షేర్ల ప్రకటన వచ్చినా షేర్ ఒకటిన్నర శాతం పడింది. ఎందుకంటే — గత నెలలో ఇరవై ఒక్క శాతం పెరిగింది. వార్త రాగానే లాభాలు తీసుకునే 'సెల్ ఆన్ న్యూస్' ధోరణి ఇది."),
 ("md_nim", "sm_myths",
  {"kicker": "THE KEY LESSON · NIM", "title": "మంచి లాభం = షేర్ పెరుగుతుందా?",
   "pairs": [
    {"m": "లాభం పెరిగింది కదా — బ్యాంక్ షేర్ పెరగాలి", "f": "NIM (మార్జిన్) తగ్గితే, లాభం పెరిగినా షేర్ పడుతుంది — HDFC, Axis అదే"},
    {"m": "అన్ని ప్రైవేట్ బ్యాంకులూ పడ్డాయి", "f": "కాదు — ICICI Bank మంచి NIMతో పెరిగింది; YES, Kotak పడ్డాయి"},
    {"m": "బ్యాంక్ నిఫ్టీ పడింది = మార్కెట్ పతనం", "f": "మిడ్‌క్యాప్ పెరిగింది — ఇది ఒక సెక్టార్ షాక్, బ్రాడ్ సెల్-ఆఫ్ కాదు"},
   ]},
  "ఇక్కడ ఈ రోజు నేర్చుకోవాల్సిన అతి ముఖ్యమైన పాఠం ఉంది. [pause] "
  "చాలామంది అనుకుంటారు — లాభం పెరిగింది కదా, షేర్ పెరగాలి అని. కానీ బ్యాంకుల విషయంలో అసలు కీలకం NIM — నికర వడ్డీ మార్జిన్. [pause] "
  "బ్యాంక్ అప్పు ఇచ్చి వసూలు చేసే వడ్డీకి, డిపాజిట్లపై కట్టే వడ్డీకి మధ్య తేడాయే NIM. ఇదే బ్యాంక్ అసలు లాభదాయకత. [pause] "
  "HDFC, Axis లాభం పెంచినా, ఈ మార్జిన్ తగ్గడంతో షేర్లు పడ్డాయి. [pause] "
  "మరో అపోహ — అన్ని ప్రైవేట్ బ్యాంకులూ పడ్డాయని. కాదు. ICICI బ్యాంక్ మంచి మార్జిన్‌తో పెరిగింది, YES బ్యాంక్, కోటక్ పడ్డాయి. [pause] "
  "కాబట్టి — బ్యాంక్ నిఫ్టీ పడిందని మొత్తం మార్కెట్ పడిపోయిందని అనుకోవద్దు. మిడ్‌క్యాప్ పెరిగింది. ఇది ఒక సెక్టార్‌కు పరిమితమైన షాక్."),
 ("md_gainers", "sm_iconcards",
  {"kicker": "GAINERS · THE CUSHION", "title": "పతనాన్ని ఆపిన షేర్లు", "color": "#34D399",
   "items": [
    {"emoji": "🟢", "k": "ICICI Bank", "v": "Q1 నికర లాభం +15.9% → ₹14,804 కోట్లు; NII +12.7% — మంచి మార్జిన్‌తో పెరిగింది", "chip": "పెరిగింది"},
    {"emoji": "🟢", "k": "PNB", "v": "Q1 లాభం +213.6% → ₹5,253 కోట్లు; PSU బ్యాంక్ ఇండెక్స్ టాప్ గెయినర్", "chip": "సర్జ్"},
    {"emoji": "🛍️", "k": "Trent", "v": "నిఫ్టీలో టాప్ గెయినర్ — రిటైల్ షేర్ల బలం", "chip": "+2.56%"},
    {"emoji": "🏭", "k": "JSW Steel · Cipla", "v": "మెటల్, ఫార్మా షేర్లు పెరిగి ఇండెక్స్ నష్టాన్ని పరిమితం చేశాయి", "chip": "పెరిగాయి"},
   ]},
  "ఇప్పుడు పతనాన్ని ఆపిన షేర్లు — ఈ రోజు నిజంగా పెరిగినవి. [pause] "
  "మొదటిది — ICICI బ్యాంక్. ఇతర ప్రైవేట్ బ్యాంకులు పడుతున్నా, ఇది పెరిగింది. Q1 నికర లాభం పదిహేను శాతానికి పైగా పెరిగి పద్నాలుగు వేల ఎనిమిది వందల కోట్లకు చేరింది. మార్జిన్ కూడా బాగుంది. [pause] "
  "రెండోది — PNB, పంజాబ్ నేషనల్ బ్యాంక్. దాని లాభం రెండు వందల పదమూడు శాతం పెరిగింది — ఐదు వేల రెండు వందల కోట్లకు. PSU బ్యాంక్ ఇండెక్స్‌ను ఇవి పైకి నెట్టాయి. [pause] "
  "మూడోది — Trent. నిఫ్టీలో టాప్ గెయినర్, రెండున్నర శాతం పెరిగింది. రిటైల్ షేర్ల బలం. [pause] "
  "నాలుగోది — JSW స్టీల్, సిప్లా లాంటి మెటల్, ఫార్మా షేర్లు. ఇవి పెరిగి ఇండెక్స్ పతనాన్ని బాగా పరిమితం చేశాయి. [pause] "
  "అందుకే — ఈ రోజు ఒక వైపు కథ కాదు. కొన్ని పడ్డాయి, కొన్ని పెరిగాయి."),
 ("md_take", "sm_checklist",
  {"kicker": "TAKEAWAYS", "title": "ఈ రోజు నుండి 5 పాఠాలు", "color": "#34D399", "icon": "💡",
   "items": [
    "ఇండెక్స్ పడినా బ్రెడ్త్ పాజిటివ్ — ఇది సెక్టార్-నిర్దిష్ట షాక్, భారీ పతనం కాదు",
    "NIM = బ్యాంక్ అసలు లాభదాయకత — లాభం కంటే మార్జిన్ ముఖ్యం",
    "US–ఇరాన్ → క్రూడ్ $90+ → ద్రవ్యోల్బణం, రూపాయి ఒత్తిడి — గమనించండి",
    "SIP పెట్టుబడిదారులకు ఒక ఎర్ర రోజు = నాయిస్, ట్రెండ్ కాదు",
    "వార్తలపై కంగారుగా ట్రేడ్ చేయొద్దు — ఇది విశ్లేషణ, సలహా కాదు",
   ]},
  "ఈ రోజు నుండి ఐదు పాఠాలు. [pause] "
  "ఒకటి — ఇండెక్స్ పడినా, ఎక్కువ షేర్లు పెరిగాయి. ఇది ఒక సెక్టార్‌కు పరిమితమైన షాక్, భారీ పతనం కాదు. [pause] "
  "రెండు — బ్యాంకుల విషయంలో లాభం కంటే NIM, అంటే మార్జిన్, ముఖ్యం. [pause] "
  "మూడు — అమెరికా, ఇరాన్ ఉద్రిక్తతతో క్రూడ్ తొంభై డాలర్లు దాటడాన్ని గమనిస్తూ ఉండండి — ఇది ద్రవ్యోల్బణం, రూపాయిపై ప్రభావం చూపుతుంది. [pause] "
  "నాలుగు — క్రమం తప్పకుండా SIP చేసేవారికి ఇలాంటి ఒక ఎర్ర రోజు కేవలం నాయిస్. దీర్ఘకాల ట్రెండ్ కాదు. [pause] "
  "ఐదు — వార్తలు చూసి కంగారుగా కొనడం, అమ్మడం చేయొద్దు. ఇది విశ్లేషణ మాత్రమే, పెట్టుబడి సలహా కాదు."),
 ("md_recap", "sm_recap",
  {"title": "20 జూలై — ఒక్క చూపులో",
   "items": [
    "సెన్సెక్స్ −443 (77,708) · నిఫ్టీ −96 (24,238)",
    "కారణం: HDFC, Axis మార్జిన్ మిస్ + క్రూడ్ $90+ + FII అమ్మకం",
    "పడినవి: Axis, HDFC, Maruti, Paytm, YES, Kotak",
    "పెరిగినవి: ICICI, PNB, Trent, JSW Steel, Cipla",
    "మిడ్‌క్యాప్ పచ్చగా — సెక్టార్ షాక్, మార్కెట్ పతనం కాదు",
   ],
   "closer": "ఒక ఎర్ర రోజు కథ కాదు — దీర్ఘకాల క్రమశిక్షణే విజయం."},
  "ఇరవై జూలై మార్కెట్ ఒక్క చూపులో. [pause] "
  "సెన్సెక్స్ నాలుగు వందల నలభై మూడు, నిఫ్టీ తొంభై ఆరు పాయింట్లు పడ్డాయి. [pause] "
  "కారణం — HDFC, Axis బ్యాంకుల మార్జిన్ మిస్, క్రూడ్ తొంభై డాలర్లు దాటడం, విదేశీ సంస్థల అమ్మకం. [pause] "
  "Axis, HDFC, మారుతి, Paytm, YES, కోటక్ పడ్డాయి. ICICI, PNB, Trent, JSW స్టీల్, సిప్లా పెరిగాయి. [pause] "
  "కానీ మిడ్‌క్యాప్ పచ్చగా ఉంది — ఇది ఒక సెక్టార్ షాక్, మార్కెట్ పతనం కాదు. [pause] "
  "ఒక ఎర్ర రోజు మొత్తం కథ కాదు — దీర్ఘకాల క్రమశిక్షణే అసలు విజయం. [pause] "
  "ఈ సమాచారం బహిరంగ వార్తల నుండి సేకరించింది — విశ్లేషణ కోసం మాత్రమే, పెట్టుబడి సలహా కాదు. మీ నిర్ణయాలకు ముందు నిపుణుల సలహా తీసుకోండి. చూసినందుకు ధన్యవాదాలు."),
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
