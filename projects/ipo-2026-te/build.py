#!/usr/bin/env python3
"""IPO Special (Telugu) — 2026 calendar + Reliance Jio + allotment lottery.
Reuses `sm` scene set. Facts verified via IPO-digest search (20 Jul 2026).
Info aggregation, not advice. Usage: python3 build.py  |  python3 build.py ip01
"""
import json, os, re, subprocess, sys

VOICE = "te-IN-ShrutiNeural"; RATE = "-4%"; GAP = 0.5; PAUSE = 0.55; PREFIX = "sm"
ROOT = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(ROOT, "..", ".."))
PUBLIC = os.path.join(REPO, "composer", "public", PREFIX); RAW = os.path.join(ROOT, "assets", "raw"); FIN = os.path.join(ROOT, "assets")
for d in (PUBLIC, RAW, os.path.join(ROOT, "artifacts"), os.path.join(ROOT, "renders")):
    os.makedirs(d, exist_ok=True)

CHAPTERS = {
 "ip01": [
 ("ip_title", "sm_ptitle",
  {"title": "2026 IPO పూర్తి గైడ్", "sub": "క్యాలెండర్ · Reliance Jio · అలాట్‌మెంట్ లాటరీ", "kicker": "IPO SPECIAL · 2026"},
  "IPO — కొత్త కంపెనీ మొదటిసారి మార్కెట్‌లోకి వచ్చే క్షణం. [pause] "
  "వచ్చే వారం, వచ్చే నెలలో ఏ IPOలు వస్తున్నాయి? అత్యధిక ఆసక్తి ఏ IPOపై? [pause] "
  "అలాట్‌మెంట్ లాటరీ ఎలా పనిచేస్తుంది, ఎలా దరఖాస్తు చేయాలి, అవకాశం ఎలా పెంచుకోవాలి — "
  "అన్నీ ఈ ఒక్క వీడియోలో. ఇది సమాచారం కోసమే, సలహా కాదు."),
 ("ip_calendar", "sm_iconcards",
  {"kicker": "THIS WEEK", "title": "వచ్చే వారం IPOలు (21–27 జూలై)", "color": "#22D3EE",
   "items": [
    {"emoji": "🛣️", "k": "Cube Highways Trust", "v": "మెయిన్‌బోర్డ్ InvIT · ధర ₹151–152 · లిస్టింగ్ 29 జూలై", "chip": "22–24 జూలై"},
    {"emoji": "⛏️", "k": "Caliber Mining", "v": "మెయిన్‌బోర్డ్ · ధర ₹402–424 · లిస్టింగ్ 24 జూలై", "chip": "17–21 జూలై"},
    {"emoji": "🏭", "k": "Gulf Lloyds", "v": "SME · ధర ₹100 · లిస్టింగ్ 27 జూలై — SMEలో రిస్క్ ఎక్కువ", "chip": "20–22 జూలై"},
    {"emoji": "🔩", "k": "Metalic Technoforge", "v": "SME · ధర ₹72–77 · లిస్టింగ్ 28 జూలై", "chip": "21–23 జూలై"},
   ]},
  "ముందు వచ్చే వారం క్యాలెండర్. [pause] "
  "మెయిన్‌బోర్డ్‌లో రెండు ముఖ్యమైనవి. [pause] "
  "Cube Highways Trust — ఇది ఒక ఇన్విట్, హైవే ప్రాజెక్టుల ట్రస్ట్. జూలై ఇరవై రెండు నుండి ఇరవై నాలుగు వరకు, ధర శ్రేణి నూట యాభై ఒకటి నుండి నూట యాభై రెండు. [pause] "
  "Caliber Mining అండ్ లాజిస్టిక్స్ — ధర నాలుగు వందల రెండు నుండి నాలుగు వందల ఇరవై నాలుగు. [pause] "
  "SME విభాగంలో Gulf Lloyds, Metalic Technoforge వస్తున్నాయి. [pause] "
  "ఒక ముఖ్య జాగ్రత్త — SME IPOలలో రిస్క్, హెచ్చుతగ్గులు మెయిన్‌బోర్డ్ కంటే చాలా ఎక్కువ. కొత్తవారు జాగ్రత్తగా ఉండాలి. [pause] "
  "కచ్చితమైన తేదీలు మారవచ్చు — NSE, BSE వెబ్‌సైట్‌లో నిర్ధారించుకోండి."),
 ("ip_pipeline", "sm_iconcards",
  {"kicker": "THE MONTH AHEAD", "title": "2026 పెద్ద IPO పైప్‌లైన్", "color": "#A78BFA",
   "items": [
    {"emoji": "📡", "k": "Reliance Jio", "v": "చరిత్రలోనే అతిపెద్ద IPO కావచ్చు — H1 2026 అంచనా", "chip": "మెగా"},
    {"emoji": "🏛️", "k": "NSE", "v": "స్టాక్ ఎక్స్ఛేంజే లిస్ట్ అవుతోంది — ఏళ్లుగా ఎదురుచూస్తున్న IPO", "chip": "వెయిటెడ్"},
    {"emoji": "💳", "k": "PhonePe · Flipkart", "v": "పెద్ద డిజిటల్ కంపెనీలు — 2026లో లిస్టింగ్ అంచనా", "chip": "టెక్"},
    {"emoji": "📊", "k": "మొత్తం పైప్‌లైన్", "v": "2026లో దాదాపు ₹2.5 లక్షల కోట్ల IPOలు — రికార్డు స్థాయి", "chip": "₹2.5L Cr"},
   ]},
  "ఇక వచ్చే నెలలు, అంటే మిగతా 2026 పైప్‌లైన్. [pause] "
  "కచ్చితమైన తేదీలు ఇంకా ఖరారు కాలేదు — కానీ ఈ పెద్ద పేర్లను అందరూ గమనిస్తున్నారు. [pause] "
  "Reliance Jio — దీనిపైనే అత్యధిక ఆసక్తి. తర్వాత చూద్దాం. [pause] "
  "NSE — స్టాక్ ఎక్స్ఛేంజ్ స్వయంగా లిస్ట్ అవుతోంది. ఏళ్లుగా ఎదురుచూస్తున్న IPO ఇది. [pause] "
  "PhonePe, Flipkart, boAt, Zepto లాంటి పెద్ద డిజిటల్ కంపెనీలు కూడా క్యూలో ఉన్నాయి. [pause] "
  "మొత్తంగా 2026లో దాదాపు రెండున్నర లక్షల కోట్ల రూపాయల IPOలు వస్తాయని అంచనా — ఇది రికార్డు స్థాయి."),
 ("ip_jio", "sm_stats",
  {"kicker": "MOST ANTICIPATED", "title": "Reliance Jio — ఎందుకంత హైప్?", "color": "#A78BFA",
   "stats": [
    {"label": "అంచనా విలువ", "to": 12, "prefix": "₹", "suffix": " లక్షల కోట్లు", "color": "#A78BFA", "sub": "~$170 బిలియన్"},
    {"label": "ఇష్యూ సైజు (అంచనా)", "to": 52, "prefix": "₹", "suffix": " వేల కోట్లు", "color": "#FBBF24", "sub": "30–52 వేల కోట్ల శ్రేణి"},
    {"label": "Jio చందాదారులు", "to": 52.7, "decimals": 1, "suffix": " కోట్లు", "color": "#34D399", "sub": "దేశంలో అతిపెద్ద టెలికాం"},
   ],
   "note": "చరిత్రలోనే అతిపెద్ద IPO కావచ్చు · H1 2026 · NSE, BSE రెండింటిలో లిస్టింగ్. కానీ — హైప్ ఎక్కువైతే రిటైల్ అలాట్‌మెంట్ అవకాశం చాలా తక్కువ."},
  "ఇప్పుడు — అత్యధిక ఆసక్తి ఉన్న IPO. Reliance Jio. ఎందుకంత హైప్? [pause] "
  "మొదటిది — పరిమాణం. దీని అంచనా విలువ పదకొండు నుండి పన్నెండు లక్షల కోట్లు. దాదాపు నూట డెబ్బై బిలియన్ డాలర్లు. [pause] "
  "ఇష్యూ సైజు ముప్పై వేల నుండి యాభై రెండు వేల కోట్ల వరకు ఉండవచ్చు — ఇది భారత చరిత్రలోనే అతిపెద్ద IPO కావచ్చు. [pause] "
  "Jioకు దేశంలో దాదాపు యాభై మూడు కోట్ల చందాదారులు — దేశంలో అతిపెద్ద టెలికాం సంస్థ. [pause] "
  "అందుకే — ప్రతి రిటైల్ ఇన్వెస్టర్ దీనికోసం ఎదురుచూస్తున్నారు. లిస్టింగ్ H1 2026లో అంచనా. [pause] "
  "కానీ ఒక వాస్తవం — హైప్ ఎంత ఎక్కువైతే, దరఖాస్తులు అంత ఎక్కువ. అంటే — రిటైల్‌కు అలాట్‌మెంట్ అవకాశం చాలా తక్కువగా ఉంటుంది. అది ఎందుకో ఇప్పుడు చూద్దాం."),
 ("ip_process", "sm_steps",
  {"kicker": "HOW TO APPLY", "title": "IPOకి దరఖాస్తు — 4 అడుగులు", "color": "#34D399",
   "note": "Zerodha, Groww, Upstox — మూడింటిలోనూ ఇదే. డబ్బు బ్లాక్ మాత్రమే, డెబిట్ కాదు",
   "items": [
    {"emoji": "📱", "label": "IPO ఎంచుకోండి", "sub": "యాప్ IPO విభాగంలో"},
    {"emoji": "🎯", "label": "లాట్లు + కట్-ఆఫ్", "sub": "రిటైల్ ≤₹2 లక్ష"},
    {"emoji": "🔒", "label": "UPI మాండేట్", "sub": "డబ్బు బ్లాక్ అవుతుంది"},
    {"emoji": "🔔", "label": "అలాట్ → లిస్టింగ్", "sub": "T+3 రోజుల్లో"},
   ]},
  "మరి IPOకి ఎలా దరఖాస్తు చేయాలి? నాలుగు అడుగులు. [pause] "
  "ఒకటి — Zerodha, Groww లేదా Upstox యాప్‌లో IPO విభాగం తెరిచి, ఆ IPO ఎంచుకోండి. [pause] "
  "రెండు — ఎన్ని లాట్లు కావాలో పెట్టి, కట్-ఆఫ్ ధరను టిక్ చేయండి. రిటైల్ ఇన్వెస్టర్ రెండు లక్షల వరకు దరఖాస్తు చేయవచ్చు. "
  "కట్-ఆఫ్ ఎంచుకోవడం చాలా ముఖ్యం — తక్కువ ధరకు వేస్తే దరఖాస్తు రద్దవుతుంది. [pause] "
  "మూడు — UPI మాండేట్ ఆమోదించండి. ఇక్కడ మీ డబ్బు బ్లాక్ మాత్రమే అవుతుంది — డెబిట్ కాదు. అలాట్ అయ్యేదాకా అది మీ ఖాతాలోనే వడ్డీ సంపాదిస్తుంది. [pause] "
  "నాలుగు — ప్రస్తుత T ప్లస్ త్రీ నిబంధన ప్రకారం, ఇష్యూ ముగిసిన దాదాపు మూడు పని రోజుల్లో లిస్టింగ్. అలాట్ కాకపోతే, బ్లాక్ చేసిన డబ్బు నాలుగు ఐదు రోజుల్లో విడుదల అవుతుంది."),
 ("ip_lottery", "sm_lossgrid",
  {"kicker": "ALLOTMENT LOTTERY", "title": "10× సబ్‌స్క్రైబ్ అయితే — ఎవరికి వస్తుంది?", "lossPct": 90,
   "mainLabel": "అలాట్ కానివారు", "statLabel": "అలాట్ అయ్యేవారు", "statTo": 10, "statSuffix": "%",
   "source": "SEBI నిబంధన · కంప్యూటరైజ్డ్ లాటరీ",
   "note": "ప్రతి దరఖాస్తుకు 1 ఛాన్స్ — ఎక్కువ లాట్లు వేసినా అవకాశం పెరగదు"},
  "ఇప్పుడు అసలు రహస్యం — అలాట్‌మెంట్ లాటరీ. [pause] "
  "IPO ఓవర్‌సబ్‌స్క్రైబ్ అయితే — అంటే డిమాండ్ షేర్ల కంటే ఎక్కువైతే — రిటైల్‌కు కంప్యూటరైజ్డ్ లాటరీ ద్వారా అలాట్ చేస్తారు. [pause] "
  "ఉదాహరణకు, ఒక IPO పది రెట్లు సబ్‌స్క్రైబ్ అయిందనుకోండి. [pause] "
  "అప్పుడు, దాదాపు ప్రతి పది దరఖాస్తులకు ఒక్కరికే — ఒక లాట్ వస్తుంది. మిగతా తొమ్మిది మందికి రాదు. [pause] "
  "ఇక్కడ SEBI నియమం చాలా న్యాయమైనది — వీలైనంత ఎక్కువ మందికి కనీసం ఒక లాట్ ఇవ్వాలి. [pause] "
  "అందుకే — ఇక్కడ అతి ముఖ్యమైన విషయం. ప్రతి దరఖాస్తుకూ ఒకే ఒక్క ఛాన్స్. మీరు ఐదు లాట్లు వేసినా, ఒక లాట్ వేసినా — లాటరీలో అవకాశం ఒకటే. [pause] "
  "అంటే — ఎక్కువ లాట్లు వేయడం వల్ల అలాట్‌మెంట్ అవకాశం పెరగదు."),
 ("ip_maximize", "sm_checklist",
  {"kicker": "MAXIMIZE ODDS", "title": "అలాట్‌మెంట్ అవకాశం పెంచుకునే మార్గాలు", "color": "#34D399", "icon": "✅",
   "items": [
    "కట్-ఆఫ్ ధరకే దరఖాస్తు చేయండి — తక్కువ వేస్తే రద్దు",
    "ఒక PANకి ఒకే దరఖాస్తు — అదే PANతో రెండు వేస్తే రెండూ రద్దు",
    "అసలు మార్గం: కుటుంబ PANలు (మీరు+భాగస్వామి+తల్లిదండ్రులు) ఒక్కో డీమ్యాట్",
    "మొదటి 1–2 రోజుల్లో వేయండి — చివరి నిమిషం గ్లిచ్‌లు వద్దు",
    "GMP కేవలం సెంటిమెంట్ సూచిక — అనధికారికం, హామీ కాదు",
   ]},
  "మరి అలాట్‌మెంట్ అవకాశం నిజంగా ఎలా పెంచుకోవాలి? [pause] "
  "ఒకటి — ఎప్పుడూ కట్-ఆఫ్ ధరకే దరఖాస్తు చేయండి. తక్కువ ధరకు వేస్తే రద్దవుతుంది. [pause] "
  "రెండు — ఒక PANకి ఒకే దరఖాస్తు. అదే PANతో రెండు వేస్తే రెండూ రద్దవుతాయి. ఎక్కువ లాట్లు వేయడమూ వృథా. [pause] "
  "మూడు — నిజమైన మార్గం ఇదొక్కటే. మీరు, జీవిత భాగస్వామి, తల్లిదండ్రులు — ఒక్కొక్కరి PAN, ఒక్కొక్క డీమ్యాట్ ఖాతా నుండి విడిగా దరఖాస్తు చేయడం. ప్రతి దరఖాస్తూ లాటరీలో ఒక టికెట్. [pause] "
  "నాలుగు — మొదటి ఒకటి రెండు రోజుల్లోనే వేయండి. చివరి నిమిషం UPI గ్లిచ్‌లు తప్పించుకోండి. [pause] "
  "ఐదు — GMP, అంటే గ్రే మార్కెట్ ప్రీమియం, కేవలం సెంటిమెంట్ సూచిక. ఇది అనధికారికం, ఎప్పటికీ హామీ కాదు."),
 ("ip_myths", "sm_myths",
  {"kicker": "REALITY CHECK", "title": "IPO అపోహలు — జాగ్రత్త",
   "pairs": [
    {"m": "IPO అంటే గ్యారంటీ లిస్టింగ్ లాభం", "f": "చాలా పెద్ద IPOలు ఇష్యూ ధర కిందికే లిస్ట్ అయ్యాయి"},
    {"m": "GMP ఎక్కువుంది — ఖచ్చితంగా లాభం", "f": "GMP అనధికారికం, మారుతూ ఉంటుంది — హామీ కాదు"},
    {"m": "ఎక్కువ లాట్లు వేస్తే అలాట్ ఖాయం", "f": "ఓవర్‌సబ్‌స్క్రిప్షన్‌లో ప్రతి దరఖాస్తుకు ఒకే ఛాన్స్"},
   ]},
  "చివరగా — IPO చుట్టూ మూడు ప్రమాదకర అపోహలు. [pause] "
  "మొదటిది — IPO అంటే లిస్టింగ్ రోజు లాభం ఖాయం అనేది. [pause] "
  "నిజం — చాలా పెద్ద, హైప్ ఉన్న IPOలు కూడా ఇష్యూ ధర కంటే తక్కువకే లిస్ట్ అయ్యాయి. హైప్ ఎక్కువైన కొద్దీ రిస్క్ ఎక్కువ. [pause] "
  "రెండోది — GMP ఎక్కువుంది కాబట్టి లాభం ఖాయం అనేది. [pause] "
  "GMP అనధికారిక గ్రే మార్కెట్ అంచనా. అది క్షణక్షణం మారుతుంది, ఏ హామీ ఇవ్వదు. [pause] "
  "మూడోది — ఎక్కువ లాట్లు వేస్తే అలాట్ ఖాయం అనేది. మనం చూశాం కదా — ఓవర్‌సబ్‌స్క్రిప్షన్‌లో ప్రతి దరఖాస్తుకూ ఒకే ఛాన్స్. [pause] "
  "అలాట్ కాకపోతే బాధపడకండి — లిస్ట్ అయ్యాక మార్కెట్‌లో, తరచుగా IPO ధర కంటే తక్కువకే కొనొచ్చు."),
 ("ip_recap", "sm_recap",
  {"title": "IPO గైడ్ — సారాంశం",
   "items": [
    "వచ్చే వారం: Cube Highways, Caliber Mining + SMEలు",
    "మెగా పైప్‌లైన్: Jio, NSE, PhonePe — 2026లో ₹2.5L Cr",
    "Jio = అతిపెద్ద IPO కావచ్చు — కానీ అలాట్ అవకాశం తక్కువ",
    "దరఖాస్తు: కట్-ఆఫ్ + UPI బ్లాక్ + T+3 లిస్టింగ్",
    "10× సబ్: ప్రతి 10కి 1 — కుటుంబ PANలే నిజమైన మార్గం",
   ],
   "closer": "హైప్‌కు కాదు — విలువకు, RHPకి దరఖాస్తు చేయండి."},
  "IPO గైడ్ సారాంశం. [pause] "
  "వచ్చే వారం Cube Highways, Caliber Mining, కొన్ని SMEలు వస్తున్నాయి. [pause] "
  "మెగా పైప్‌లైన్‌లో Jio, NSE, PhonePe — 2026లో దాదాపు రెండున్నర లక్షల కోట్లు. [pause] "
  "Jio చరిత్రలోనే అతిపెద్ద IPO కావచ్చు — కానీ హైప్ వల్ల రిటైల్ అలాట్‌మెంట్ అవకాశం తక్కువ. [pause] "
  "దరఖాస్తు — కట్-ఆఫ్ ధర, UPI బ్లాక్, T ప్లస్ త్రీ లిస్టింగ్. [pause] "
  "పది రెట్లు సబ్‌స్క్రైబ్ అయితే ప్రతి పదికి ఒక్కరికే. అవకాశం పెంచే నిజమైన మార్గం — కుటుంబ PANలు. [pause] "
  "గుర్తుంచుకోండి — హైప్‌కు కాదు, కంపెనీ విలువకు, RHP చదివి దరఖాస్తు చేయండి. [pause] "
  "ఈ సమాచారం బహిరంగ వార్తల నుండి సేకరించింది — విశ్లేషణ కోసమే, పెట్టుబడి సలహా కాదు. తేదీలు, ధరలు మారవచ్చు, NSE BSEలో నిర్ధారించుకోండి. చూసినందుకు ధన్యవాదాలు."),
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
