#!/usr/bin/env python3
"""Broker Comparison (Telugu) — 2026. Reuses `sm` scene set.
Data verified in research/brokers-2026.md. Neutral, not affiliated, not advice. Verify live charges.
Usage: python3 build.py            (all)   |   python3 build.py br
"""
import json, os, re, subprocess, sys, time

VOICE = "te-IN-ShrutiNeural"; RATE = "-4%"; GAP = 0.5; PAUSE = 0.55; PREFIX = "sm"
ROOT = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(ROOT, "..", ".."))
PUBLIC = os.path.join(REPO, "composer", "public", PREFIX); RAW = os.path.join(ROOT, "assets", "raw"); FIN = os.path.join(ROOT, "assets")
for d in (PUBLIC, RAW, os.path.join(ROOT, "artifacts"), os.path.join(ROOT, "renders")):
    os.makedirs(d, exist_ok=True)

CHAPTERS = {
 "br": [
 ("br_title", "sm_ptitle",
  {"title": "ఏ బ్రోకర్ యాప్ బెస్ట్?", "sub": "Zerodha · Groww · Angel One · Dhan · Upstox — 2026 పోలిక", "kicker": "BROKER COMPARISON · 2026"},
  "స్టాక్స్, మ్యూచువల్ ఫండ్స్, F&O — వీటిలో పెట్టుబడి పెట్టాలంటే మొదటి అడుగు ఒక బ్రోకర్ యాప్. కానీ ఇన్ని యాప్‌లలో ఏది బెస్ట్? [pause] "
  "ఈ వీడియోలో — ప్రధాన బ్రోకర్ల కమిషన్లు, వాటి యాప్‌లు, ఇటీవల వినియోగదారులు ఎదుర్కొన్న సమస్యలు, ఏ యాప్ దేనికి బెస్ట్ — అన్నీ చూద్దాం. [pause] "
  "ముఖ్య గమనిక — ఇది ఏ బ్రోకర్ ప్రచారం కాదు, పెట్టుబడి సలహా కాదు. ఛార్జీలు తరచూ మారతాయి — ఎంచుకునే ముందు యాప్‌లో ప్రస్తుత రేట్లు చెక్ చేయండి."),
 ("br_players", "sm_iconcards",
  {"kicker": "THE PLAYERS + CHARGES", "title": "ప్రధాన బ్రోకర్లు — యూజర్లు & ఛార్జీలు", "color": "#22D3EE",
   "items": [
    {"emoji": "🟢", "k": "Groww", "v": "1.3 కోట్ల యూజర్లు (#1) · డెలివరీ ₹20*, F&O ₹20, AMC ₹0 · *ఇతరులు డెలివరీ ఫ్రీ", "chip": "అతి సింపుల్"},
    {"emoji": "🔵", "k": "Zerodha", "v": "79.5 లక్షలు · డెలివరీ ₹0, F&O ₹20, AMC ₹300 · Kite, Coin, Varsity", "chip": "ఎకోసిస్టమ్"},
    {"emoji": "🟠", "k": "Angel One", "v": "76.4 లక్షలు · డెలివరీ ₹0, F&O ₹20, AMC ₹240 · బలమైన రీసెర్చ్", "chip": "రీసెర్చ్"},
    {"emoji": "🟣", "k": "Dhan", "v": "కొత్త తరం · డెలివరీ ₹0, F&O ₹20, AMC ₹0 · ఆప్షన్స్‌కు #1 యాప్", "chip": "F&O ఫోకస్"},
   ]},
  "మొదట ప్రధాన బ్రోకర్లు, వాళ్ల యూజర్లు, ఛార్జీలు చూద్దాం. [pause] "
  "మొదటిది — Groww. ఇప్పుడు దేశంలో నంబర్ వన్, ఒక కోటి ముప్పై లక్షల యూజర్లతో. అత్యంత సరళమైన యాప్. కానీ ఒక తేడా — డెలివరీపై ఇరవై రూపాయలు వసూలు చేస్తుంది; మిగతా బ్రోకర్లు దీన్ని ఫ్రీగా ఇస్తారు. AMC సున్నా. [pause] "
  "రెండోది — Zerodha. డెబ్బై తొమ్మిదిన్నర లక్షల యూజర్లు. డెలివరీ ఫ్రీ, F&Oకి ఇరవై రూపాయలు, AMC మూడు వందలు. Kite, Coin, Varsity అనే బలమైన ఎకోసిస్టమ్. [pause] "
  "మూడోది — Angel One. డెబ్బై ఆరున్నర లక్షల యూజర్లు. డెలివరీ ఫ్రీ, AMC రెండు వందల నలభై. బలమైన రీసెర్చ్ రిపోర్ట్‌లకు పేరు. [pause] "
  "నాలుగోది — Dhan. కొత్త తరం బ్రోకర్. డెలివరీ ఫ్రీ, AMC సున్నా. ఆప్షన్స్ ట్రేడర్లకు ప్రస్తుతం నంబర్ వన్ యాప్. F&O కుడి, Upstox, Fyers కూడా మంచి ఎంపికలు."),
 ("br_apps", "sm_iconcards",
  {"kicker": "THE APPS", "title": "యాప్‌లు — ఏది దేనిలో బలం?", "color": "#34D399",
   "items": [
    {"emoji": "🛠️", "k": "Zerodha", "v": "Kite (ప్రో ట్రేడింగ్), Coin (2000+ డైరెక్ట్ MF, XIRR), Console, Varsity ఉచిత విద్య, Sensibull ఆప్షన్స్", "chip": "ఆల్-రౌండర్"},
    {"emoji": "👶", "k": "Groww", "v": "అత్యంత సరళమైన ఇంటర్‌ఫేస్; MFకి డీమ్యాట్ అవసరం లేదు; కొత్తవారికి బెస్ట్ — కానీ పవర్ యూజర్లకు పరిమితం", "chip": "బిగినర్స్"},
    {"emoji": "📊", "k": "Dhan", "v": "TradingView చార్ట్‌లు, ఆప్షన్ చెయిన్, స్ట్రాటజీ టూల్స్, వేగం — F&O ట్రేడర్లకు రూపొందించింది", "chip": "ఆప్షన్స్"},
    {"emoji": "🔍", "k": "Angel One", "v": "బలమైన రీసెర్చ్ రిపోర్ట్‌లు, స్మార్ట్ సూచనలు — కానీ ఎక్కువ నోటిఫికేషన్లు వస్తాయని ఫిర్యాదు", "chip": "రీసెర్చ్"},
   ]},
  "ఇప్పుడు యాప్‌లు — ఏది దేనిలో బలంగా ఉందో చూద్దాం. [pause] "
  "Zerodha — Kite ప్రో ట్రేడింగ్ ప్లాట్‌ఫారం, Coin లో రెండు వేలకు పైగా డైరెక్ట్ మ్యూచువల్ ఫండ్స్, స్టాక్స్, ఫండ్స్ కలిపి ఒకే XIRR వ్యూ. Varsity ఉచిత విద్య, Sensibull ఆప్షన్స్ విశ్లేషణ. అన్నీ ఒకే చోట. [pause] "
  "Groww — అత్యంత సరళమైన యాప్. మ్యూచువల్ ఫండ్‌కి డీమ్యాట్ కూడా అవసరం లేదు, కేవలం KYC చాలు. కొత్తవారికి బెస్ట్. కానీ అనుభవజ్ఞులైన ట్రేడర్లకు ఫీచర్లు పరిమితం. [pause] "
  "Dhan — TradingView చార్ట్‌లు, ఆప్షన్ చెయిన్, స్ట్రాటజీ టూల్స్, చాలా వేగం. F&O, ఆప్షన్స్ ట్రేడర్ల కోసం ప్రత్యేకంగా రూపొందించిన యాప్. [pause] "
  "Angel One — బలమైన రీసెర్చ్ రిపోర్ట్‌లు, స్మార్ట్ సూచనలు. కానీ ఎక్కువ నోటిఫికేషన్లు, ప్రమోషన్లు వస్తాయని కొందరు వినియోగదారుల ఫిర్యాదు."),
 ("br_issues", "sm_iconcards",
  {"kicker": "RECENT USER-REPORTED ISSUES", "title": "ఇటీవలి సమస్యలు — వినియోగదారుల ఫిర్యాదులు", "color": "#FB7185",
   "items": [
    {"emoji": "🌐", "k": "Cloudflare అవుటేజ్ (డిసెం 5, 2025)", "v": "Zerodha, Angel, Upstox, Groww అన్నీ ~12 నిమిషాలు డౌన్ — లాగిన్, ఆర్డర్ సమస్యలు. కానీ ఇది థర్డ్-పార్టీ సమస్య, బ్రోకర్ తప్పు కాదు", "chip": "గ్లోబల్"},
    {"emoji": "⏳", "k": "Zerodha — Kite స్లో", "v": "గతంలో ఎక్స్‌పైరీ, హై-వాల్యూమ్ రోజుల్లో Kite స్లో అయ్యేది (#KiteDown) — ఇప్పుడు మెరుగుపడింది; WhatsApp బ్యాకప్ ఉంది", "chip": "మెరుగుపడింది"},
    {"emoji": "💸", "k": "Groww — డెలివరీ ఛార్జ్", "v": "ఇతరులు ఫ్రీ ఇచ్చే డెలివరీపై ₹20 వసూలు; అప్పుడప్పుడు ఛార్జ్, స్టేట్‌మెంట్ ఫిర్యాదులు", "chip": "ఛార్జీలు"},
    {"emoji": "🔔", "k": "Angel One — స్క్వేర్-ఆఫ్", "v": "ఇంట్రాడే 3:15కి ఆటో స్క్వేర్-ఆఫ్ + ఎక్కువ నోటిఫికేషన్లు, మిస్-సెల్లింగ్ ఫిర్యాదులు", "chip": "ఫిర్యాదులు"},
   ]},
  "ఇప్పుడు ముఖ్యమైనది — ఇటీవల వినియోగదారులు ఎదుర్కొన్న సమస్యలు. [pause] "
  "అతిపెద్దది — డిసెంబర్ ఐదు, రెండు వేల ఇరవై ఐదున, Cloudflare అనే గ్లోబల్ సర్వీస్ డౌన్ కావడంతో Zerodha, Angel One, Upstox, Groww — అన్ని యాప్‌లూ దాదాపు పన్నెండు నిమిషాలు పనిచేయలేదు. లాగిన్, ఆర్డర్లు ఆగిపోయాయి. కానీ ఇది ఏ బ్రోకర్ తప్పూ కాదు — థర్డ్-పార్టీ సమస్య. [pause] "
  "Zerodha — గతంలో ఎక్స్‌పైరీ, ఎక్కువ ట్రేడింగ్ ఉన్న రోజుల్లో Kite స్లో అయ్యేది. ఇప్పుడు చాలా మెరుగుపడింది, WhatsApp బ్యాకప్ కూడా ఇచ్చారు. [pause] "
  "Groww — మిగతా బ్రోకర్లు ఉచితంగా ఇచ్చే డెలివరీపై ఇరవై రూపాయలు వసూలు చేస్తుంది. అప్పుడప్పుడు ఛార్జీలు, స్టేట్‌మెంట్ల గురించి ఫిర్యాదులు వస్తాయి. [pause] "
  "Angel One — ఇంట్రాడే పొజిషన్లను మూడు పదిహేనుకి ఆటోమేటిక్‌గా క్లోజ్ చేయడం, ఎక్కువ నోటిఫికేషన్లు — వీటిపై ఫిర్యాదులు. [pause] "
  "ఒక భరోసా — ఈ బ్రోకర్లన్నీ SEBI రిజిస్టర్డ్. మీ షేర్లు బ్రోకర్ దగ్గర కాదు, NSDL, CDSLలో మీ పేరుతో సురక్షితం."),
 ("br_best", "sm_iconcards",
  {"kicker": "BEST FOR EACH NEED", "title": "ఏ యాప్ దేనికి బెస్ట్?", "color": "#34D399",
   "items": [
    {"emoji": "📈", "k": "మ్యూచువల్ ఫండ్స్", "v": "Groww (సింపుల్, ₹0, డీమ్యాట్ అవసరం లేదు) — కొత్తవారికి; లేదా Zerodha Coin (XIRR, ఎకోసిస్టమ్)", "chip": "MF"},
    {"emoji": "🏦", "k": "స్టాక్స్ / డెలివరీ", "v": "Zerodha లేదా Dhan (₹0 డెలివరీ + మంచి టూల్స్ + తక్కువ AMC). పెద్ద డెలివరీకి Groww ఖరీదు", "chip": "STOCKS"},
    {"emoji": "⚡", "k": "ఫ్యూచర్స్ & ఆప్షన్స్", "v": "Dhan (#1 ఆప్షన్స్ యాప్, TradingView, వేగం) లేదా Zerodha (Kite + Sensibull, విశ్వసనీయత)", "chip": "F&O"},
    {"emoji": "🎯", "k": "అన్నీ ఒకే చోట", "v": "Zerodha — పూర్తి ఎకోసిస్టమ్, విద్య, విశ్వసనీయత; Dhan — ఆధునిక, వేగవంతమైన ప్రత్యామ్నాయం", "chip": "ఆల్-ఇన్-వన్"},
   ]},
  "ఇప్పుడు అసలు ప్రశ్న — ఏ యాప్ దేనికి బెస్ట్? అవసరాన్ని బట్టి చూద్దాం. [pause] "
  "మ్యూచువల్ ఫండ్స్ కోసం — Groww బెస్ట్. సింపుల్, ఖర్చు లేదు, డీమ్యాట్ కూడా అవసరం లేదు. మీరు ట్రేడ్ కూడా చేస్తే — Zerodha Coin, ఎందుకంటే ఫండ్స్, స్టాక్స్ కలిపి ఒకే చోట. [pause] "
  "స్టాక్స్, డెలివరీ కోసం — Zerodha లేదా Dhan. డెలివరీ ఫ్రీ, మంచి టూల్స్, తక్కువ AMC. పెద్ద మొత్తంలో డెలివరీ చేస్తే Groww కొంచెం ఖరీదు అవుతుంది. [pause] "
  "ఫ్యూచర్స్, ఆప్షన్స్ కోసం — Dhan. వేగం, TradingView చార్ట్‌లతో ఆప్షన్స్‌కు నంబర్ వన్. లేదా Zerodha — Kite, Sensibull, విశ్వసనీయతతో. [pause] "
  "అన్నీ ఒకే చోట కావాలంటే — Zerodha, పూర్తి ఎకోసిస్టమ్‌తో బెస్ట్ ఆల్-రౌండర్. Dhan ఒక ఆధునిక, వేగవంతమైన ప్రత్యామ్నాయం."),
 ("br_take", "sm_checklist",
  {"kicker": "HOW TO CHOOSE", "title": "ఎలా ఎంచుకోవాలి — 5 సూత్రాలు", "color": "#34D399", "icon": "💡",
   "items": [
    "మీ అవసరం చూడండి: MF మాత్రమేనా, స్టాక్స్, లేదా F&O?",
    "AMC + డెలివరీ ఛార్జ్ కలిపి లెక్కించండి — కేవలం F&O రేటు కాదు",
    "ఛార్జీలు తరచూ మారతాయి — యాప్‌లో ప్రస్తుత రేట్లు వెరిఫై చేయండి",
    "అన్నీ SEBI-రిజిస్టర్డ్ — షేర్లు NSDL/CDSLలో సురక్షితం",
    "ఇది సలహా, ప్రచారం కాదు — మీకు సరిపోయేదే బెస్ట్",
   ]},
  "బ్రోకర్ ఎలా ఎంచుకోవాలి? ఐదు సూత్రాలు. [pause] "
  "ఒకటి — ముందు మీ అవసరం తేల్చుకోండి. మ్యూచువల్ ఫండ్స్ మాత్రమేనా, స్టాక్స్, లేదా F&O కూడానా? [pause] "
  "రెండు — కేవలం F&O రేటు చూడకండి. AMC, డెలివరీ ఛార్జ్ కలిపి మొత్తం ఖర్చు లెక్కించండి. [pause] "
  "మూడు — ఛార్జీలు తరచూ మారతాయి. ఎంచుకునే ముందు యాప్‌లో ప్రస్తుత రేట్లు వెరిఫై చేసుకోండి. [pause] "
  "నాలుగు — ఈ బ్రోకర్లన్నీ SEBI రిజిస్టర్డ్. మీ షేర్లు NSDL, CDSLలో సురక్షితం. [pause] "
  "ఐదు — ఇది ఏ బ్రోకర్ ప్రచారం కాదు, సలహా కాదు. మీ అవసరానికి సరిపోయేదే మీకు బెస్ట్."),
 ("br_recap", "sm_recap",
  {"title": "బ్రోకర్లు — ఒక్క చూపులో",
   "items": [
    "Groww: సింపుల్, MF, కొత్తవారికి — కానీ డెలివరీ ఖరీదు",
    "Zerodha: బెస్ట్ ఆల్-రౌండర్, ఎకోసిస్టమ్, F&O",
    "Dhan: F&O/ఆప్షన్స్‌కు వేగవంతమైన యాప్, ₹0 AMC",
    "Angel One: రీసెర్చ్; Upstox/Fyers: యాక్టివ్/అల్గో",
    "ఛార్జీలు వెరిఫై చేయండి · SEBI రక్షణ ఉంది",
   ],
   "closer": "ఏ యాప్ 'బెస్ట్' కాదు — మీ అవసరానికి సరిపోయేదే బెస్ట్."},
  "బ్రోకర్లు ఒక్క చూపులో. [pause] "
  "Groww — సింపుల్, మ్యూచువల్ ఫండ్స్, కొత్తవారికి బెస్ట్. కానీ డెలివరీ కొంచెం ఖరీదు. [pause] "
  "Zerodha — బెస్ట్ ఆల్-రౌండర్. ఎకోసిస్టమ్, విద్య, F&Oకి బలం. [pause] "
  "Dhan — F&O, ఆప్షన్స్‌కు వేగవంతమైన యాప్, AMC సున్నా. [pause] "
  "Angel One — రీసెర్చ్‌కి; Upstox, Fyers — యాక్టివ్, అల్గో ట్రేడర్లకు. [pause] "
  "ఏ యాప్ కూడా అందరికీ బెస్ట్ కాదు — మీ అవసరానికి సరిపోయేదే మీకు బెస్ట్. ఛార్జీలు వెరిఫై చేయండి. [pause] "
  "ఈ సమాచారం బహిరంగ వార్తల నుండి సేకరించింది — ఇది ఏ బ్రోకర్ ప్రచారం కాదు, పెట్టుబడి సలహా కాదు. చూసినందుకు ధన్యవాదాలు."),
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
