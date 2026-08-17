#!/usr/bin/env python3
"""Market Wrap (Telugu) — 21 July 2026 post-close. Reuses `sm` scene set.
Every number verified in research/wrap-21jul2026.md. Info aggregation, not advice.
Usage: python3 build.py            (all)   |   python3 build.py mw21
"""
import json, os, re, subprocess, sys

VOICE = "te-IN-ShrutiNeural"; RATE = "-4%"; GAP = 0.5; PAUSE = 0.55; PREFIX = "sm"
ROOT = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(ROOT, "..", ".."))
PUBLIC = os.path.join(REPO, "composer", "public", PREFIX); RAW = os.path.join(ROOT, "assets", "raw"); FIN = os.path.join(ROOT, "assets")
for d in (PUBLIC, RAW, os.path.join(ROOT, "artifacts"), os.path.join(ROOT, "renders")):
    os.makedirs(d, exist_ok=True)

CHAPTERS = {
 "mw21": [
 ("mw_title", "sm_ptitle",
  {"title": "మార్కెట్ ఎందుకు పడింది?", "sub": "జూలై 21, 2026 · మంగళవారం · పోస్ట్-మార్కెట్ విశ్లేషణ", "kicker": "MARKET WRAP · 21 JUL 2026"},
  "జూలై ఇరవై ఒకటి, రెండు వేల ఇరవై ఆరు — మంగళవారం. మార్కెట్ మూడున్నరకు ముగిసింది. [pause] "
  "వరుసగా రెండో రోజు నిఫ్టీ, సెన్సెక్స్ పడ్డాయి. ఈ రోజు వాటిని ఏ వార్తలు కదిలించాయి? [pause] "
  "ముగింపు గణాంకాలు, పడిన షేర్లు, సెక్టార్లు — అన్నీ విశ్లేషిద్దాం. "
  "ఇది సమాచార విశ్లేషణ మాత్రమే — పెట్టుబడి సలహా కాదు."),
 ("mw_snap", "sm_stats",
  {"kicker": "INDEX SNAPSHOT", "title": "ముగింపు గణాంకాలు — 21 జూలై",
   "stats": [
    {"label": "సెన్సెక్స్", "to": 77470, "prefix": "", "suffix": "", "color": "#FB7185", "sub": "−238 pts · −0.31%"},
    {"label": "నిఫ్టీ 50", "to": 24188, "prefix": "", "suffix": "", "color": "#FB7185", "sub": "−51 pts · −0.21%"},
    {"label": "బ్రెంట్ క్రూడ్", "to": 88, "prefix": "$", "suffix": "+", "color": "#FBBF24", "sub": "మధ్యప్రాచ్యం · హోర్ముజ్ ఆందోళన"},
   ],
   "note": "హెడ్‌లైన్ ఇండెక్స్ పడినా, మిడ్‌క్యాప్, స్మాల్‌క్యాప్ పెరిగాయి — బ్రెడ్త్ పాజిటివ్. ఇది లార్జ్‌క్యాప్‌కు పరిమితమైన, ఇరుకైన పతనం."},
  "ముందు ముగింపు గణాంకాలు చూద్దాం. [pause] "
  "సెన్సెక్స్ రెండు వందల ముప్పై ఎనిమిది పాయింట్లు పడి, డెబ్బై ఏడు వేల నాలుగు వందల డెబ్బై వద్ద ముగిసింది. దాదాపు మూడో వంతు శాతం తగ్గింది. [pause] "
  "నిఫ్టీ ఫిఫ్టీ యాభై ఒక్క పాయింట్లు పడి, ఇరవై నాలుగు వేల ఒక వంద ఎనభై ఏడు వద్ద నిలిచింది. ఇది వరుసగా రెండో నష్టపు రోజు. [pause] "
  "కానీ చాలా ముఖ్యమైన విషయం — మిడ్‌క్యాప్ ఇండెక్స్ మూడో వంతు శాతం, స్మాల్‌క్యాప్ అర శాతానికి పైగా పెరిగాయి. [pause] "
  "అంటే మార్కెట్‌లో ఎక్కువ షేర్లు నిజానికి పచ్చగానే ఉన్నాయి. ఈ పతనం కొన్ని పెద్ద షేర్లకే పరిమితం — భారీ సెల్-ఆఫ్ కాదు."),
 ("mw_why", "sm_iconcards",
  {"kicker": "WHY IT FELL", "title": "పతనానికి 4 కారణాలు", "color": "#FB7185",
   "items": [
    {"emoji": "🛢️", "k": "క్రూడ్ + మధ్యప్రాచ్యం", "v": "హౌతీలు సౌదీ అరేబియాపై నావికా దిగ్బంధం హెచ్చరిక; హోర్ముజ్ జలసంధి ఆందోళన — బ్రెంట్ ~$88–90", "chip": "ప్రధాన కారణం"},
    {"emoji": "💻", "k": "IT షేర్ల బలహీనత", "v": "TCS, ఇన్ఫోసిస్ దాదాపు 1% చొప్పున పడ్డాయి — నిఫ్టీ IT టాప్ లూజర్ సెక్టార్లలో ఒకటి", "chip": "IT డ్రాగ్"},
    {"emoji": "🏦", "k": "PSU బ్యాంక్ + HDFC", "v": "నిఫ్టీ PSU బ్యాంక్ ఎక్కువ పడింది; HDFC బ్యాంక్, SBI బలహీనత ఇండెక్స్‌ను లాగింది", "chip": "వెయిటేజ్"},
    {"emoji": "📤", "k": "FII అమ్మకం", "v": "విదేశీ సంస్థల నికర అమ్మకం కొనసాగింది; ప్రపంచవ్యాప్త రిస్క్-ఆఫ్ సెంటిమెంట్", "chip": "నికర అమ్మకం"},
   ]},
  "మరి ఎందుకు పడింది? నాలుగు కారణాలు. [pause] "
  "అన్నిటికంటే ముఖ్యమైనది — క్రూడ్ ఆయిల్, మధ్యప్రాచ్య ఉద్రిక్తత. [pause] "
  "యెమెన్‌లోని హౌతీలు సౌదీ అరేబియాపై నావికా దిగ్బంధం విధిస్తామని హెచ్చరించారు. దీంతో హోర్ముజ్ జలసంధి ద్వారా చమురు సరఫరాపై ఆందోళన పెరిగి, బ్రెంట్ క్రూడ్ ఎనభై ఎనిమిది నుండి తొంభై డాలర్ల మధ్యకు చేరింది. భారత్ అతిపెద్ద చమురు దిగుమతిదారు కావడంతో, ఇది ద్రవ్యోల్బణం, రూపాయిపై ఒత్తిడి పెంచుతుంది. [pause] "
  "రెండోది — IT షేర్ల బలహీనత. TCS, ఇన్ఫోసిస్ దాదాపు ఒక శాతం చొప్పున పడ్డాయి. [pause] "
  "మూడోది — PSU బ్యాంకులు, HDFC బ్యాంక్, SBI. ఇండెక్స్‌లో ఎక్కువ వెయిటేజీ ఉన్న ఈ షేర్లు నిఫ్టీని కిందికి లాగాయి. [pause] "
  "నాలుగోది — విదేశీ సంస్థల నికర అమ్మకం కొనసాగడం, ప్రపంచవ్యాప్త రిస్క్-ఆఫ్ సెంటిమెంట్."),
 ("mw_losers", "sm_iconcards",
  {"kicker": "TOP LOSERS", "title": "ఈ రోజు ఎక్కువ పడిన షేర్లు", "color": "#FB7185",
   "items": [
    {"emoji": "💊", "k": "Cipla", "v": "నిఫ్టీలో అత్యధిక నష్టం — దాదాపు 2% పడింది; ఫార్మా, హెల్త్‌కేర్ ఈ రోజు బలహీనం", "chip": "−2%"},
    {"emoji": "🏥", "k": "Dr Reddy's · Max Healthcare", "v": "రెండూ 1%కి పైగా పడ్డాయి — హెల్త్‌కేర్ సెక్టార్ ప్రెషర్", "chip": "−1%+"},
    {"emoji": "💻", "k": "TCS · Infosys", "v": "IT దిగ్గజాలు దాదాపు 1% చొప్పున — బలహీన గ్లోబల్ టెక్ సెంటిమెంట్, రూపాయి", "chip": "−1%"},
    {"emoji": "🏦", "k": "HDFC Bank · SBI", "v": "అధిక వెయిటేజీ బ్యాంక్ షేర్లు — ఇండెక్స్‌ను ఎక్కువగా లాగిన లూజర్లు", "chip": "డ్రాగ్"},
   ]},
  "ఇప్పుడు ఈ రోజు ఎక్కువ పడిన షేర్లు, వాటి వెనుక కారణాలు. [pause] "
  "మొదటిది — సిప్లా. నిఫ్టీలో అత్యధిక నష్టం, దాదాపు రెండు శాతం పడింది. ఈ రోజు ఫార్మా, హెల్త్‌కేర్ షేర్లు మొత్తంగా బలహీనంగా ఉన్నాయి. [pause] "
  "రెండోది — డాక్టర్ రెడ్డీస్, మ్యాక్స్ హెల్త్‌కేర్. రెండూ ఒక శాతానికి పైగా పడ్డాయి. [pause] "
  "మూడోది — TCS, ఇన్ఫోసిస్. ఈ IT దిగ్గజాలు దాదాపు ఒక శాతం చొప్పున పడ్డాయి — బలహీన గ్లోబల్ టెక్ సెంటిమెంట్, రూపాయి కదలికల ప్రభావంతో. [pause] "
  "నాలుగోది — HDFC బ్యాంక్, SBI. ఇవి ఇండెక్స్‌లో అత్యధిక వెయిటేజీ ఉన్న షేర్లు కావడంతో, కొంచెం పడినా నిఫ్టీని ఎక్కువగా కిందికి లాగాయి."),
 ("mw_sectors", "sm_myths",
  {"kicker": "SECTOR SCOREBOARD", "title": "సెక్టార్లు — ఎవరు పడ్డారు, ఎవరు పెరిగారు?", "mythLabel": "🔻 పడిన సెక్టార్లు", "factLabel": "🟢 పెరిగిన సెక్టార్లు",
   "pairs": [
    {"m": "నిఫ్టీ PSU బ్యాంక్ — ఎక్కువ పడిన సెక్టార్", "f": "నిఫ్టీ కెమికల్ — ఎక్కువ పెరిగిన సెక్టార్"},
    {"m": "నిఫ్టీ IT — TCS, ఇన్ఫోసిస్ ఒత్తిడితో", "f": "నిఫ్టీ సిమెంట్ — డిఫెన్సివ్ కొనుగోళ్లు"},
    {"m": "FMCG — మధ్యాహ్నం అమ్మకపు ఒత్తిడి", "f": "మిడ్‌క్యాప్, స్మాల్‌క్యాప్ — పచ్చగా"},
   ]},
  "ఈ రోజు సెక్టార్ స్కోర్‌బోర్డ్ చూద్దాం — ఎవరు పడ్డారు, ఎవరు పెరిగారు? [pause] "
  "పడిన వైపు — నిఫ్టీ PSU బ్యాంక్ ఎక్కువ పడింది. దాని వెంట నిఫ్టీ IT — TCS, ఇన్ఫోసిస్ ఒత్తిడితో. మధ్యాహ్నం FMCG షేర్లలోనూ అమ్మకపు ఒత్తిడి కనిపించింది. [pause] "
  "పెరిగిన వైపు — నిఫ్టీ కెమికల్ ఇండెక్స్ ఎక్కువ పెరిగింది, దాని వెంట సిమెంట్. అనిశ్చితి ఉన్నప్పుడు పెట్టుబడిదారులు ఇలాంటి డిఫెన్సివ్ సెక్టార్ల వైపు మళ్లుతారు. [pause] "
  "అందుకే — ఒక వైపు IT, బ్యాంకులు పడితే, మరో వైపు కెమికల్, సిమెంట్, మిడ్‌క్యాప్ షేర్లు పెరిగాయి. ఇది సెక్టార్ రొటేషన్ — మొత్తం మార్కెట్ పతనం కాదు."),
 ("mw_lesson", "sm_myths",
  {"kicker": "THE KEY LESSON · CRUDE", "title": "క్రూడ్ ఆయిల్ ఎందుకు మార్కెట్‌ను కదిలిస్తుంది?",
   "pairs": [
    {"m": "క్రూడ్ ధర మనకు సంబంధం లేదు", "f": "భారత్ చమురులో 85% దిగుమతి చేస్తుంది — క్రూడ్ పెరిగితే దిగుమతి బిల్లు, ద్రవ్యోల్బణం పెరుగుతాయి"},
    {"m": "క్రూడ్ అన్ని షేర్లనూ ఒకేలా పడేస్తుంది", "f": "కాదు — పెయింట్స్, ఎయిర్‌లైన్స్, ఆటోలకు చెడు; ONGC లాంటి చమురు ఉత్పత్తిదారులకు మంచిది"},
    {"m": "ఇది భారత్ సొంత సమస్య", "f": "కాదు — ఇది హౌతీ, హోర్ముజ్ జలసంధి అనే ప్రపంచ భౌగోళిక-రాజకీయ వార్త వల్ల"},
   ]},
  "ఇక్కడ ఈ రోజు నేర్చుకోవాల్సిన అతి ముఖ్యమైన పాఠం — క్రూడ్ ఆయిల్ ఎందుకు మార్కెట్‌ను కదిలిస్తుంది? [pause] "
  "చాలామంది అనుకుంటారు — క్రూడ్ ధర మనకేంటి సంబంధం అని. కానీ భారత్ తన చమురు అవసరాల్లో దాదాపు ఎనభై ఐదు శాతం దిగుమతి చేస్తుంది. క్రూడ్ పెరిగితే దిగుమతి బిల్లు, ద్రవ్యోల్బణం, రూపాయిపై ఒత్తిడి — అన్నీ పెరుగుతాయి. [pause] "
  "కానీ క్రూడ్ అన్ని షేర్లనూ ఒకేలా పడేయదు. పెయింట్స్, ఎయిర్‌లైన్స్, ఆటో కంపెనీలకు ఇది చెడు వార్త — వాటికి క్రూడ్ ముడి పదార్థం. కానీ ONGC లాంటి చమురు ఉత్పత్తి కంపెనీలకు ఇది మంచి వార్త. [pause] "
  "మరో ముఖ్య విషయం — ఇది భారత్ సొంత సమస్య కాదు. హౌతీలు, హోర్ముజ్ జలసంధి అనే ప్రపంచ భౌగోళిక-రాజకీయ వార్త మన మార్కెట్‌ను కదిలించింది. మార్కెట్ ఎప్పుడూ ప్రపంచంతో అనుసంధానమై ఉంటుంది."),
 ("mw_take", "sm_checklist",
  {"kicker": "TAKEAWAYS", "title": "ఈ రోజు నుండి 5 పాఠాలు", "color": "#34D399", "icon": "💡",
   "items": [
    "వరుసగా రెండో నష్టపు రోజు అయినా బ్రెడ్త్ పాజిటివ్ — ఇది ఇరుకైన, లార్జ్‌క్యాప్ పతనం",
    "క్రూడ్ $90 దగ్గర = ద్రవ్యోల్బణం, రూపాయి ఒత్తిడి — దీన్ని గమనిస్తూ ఉండండి",
    "IT + బ్యాంకులు పడితే కెమికల్, సిమెంట్ పెరిగాయి — సెక్టార్ రొటేషన్",
    "గ్లోబల్ వార్తలు (హౌతీ, హోర్ముజ్) మన మార్కెట్‌ను నేరుగా ప్రభావితం చేస్తాయి",
    "SIP పెట్టుబడిదారులకు ఇలాంటి ఎర్ర రోజులు నాయిస్ — ట్రెండ్ కాదు",
   ]},
  "ఈ రోజు నుండి ఐదు పాఠాలు. [pause] "
  "ఒకటి — వరుసగా రెండో నష్టపు రోజు అయినా, ఎక్కువ షేర్లు పెరిగాయి. ఇది ఇరుకైన, లార్జ్‌క్యాప్‌కు పరిమితమైన పతనం. [pause] "
  "రెండు — క్రూడ్ తొంభై డాలర్ల దగ్గర ఉండటం ద్రవ్యోల్బణం, రూపాయిపై ఒత్తిడి పెంచుతుంది. దీన్ని గమనిస్తూ ఉండండి. [pause] "
  "మూడు — ఒక వైపు IT, బ్యాంకులు పడితే మరో వైపు కెమికల్, సిమెంట్ పెరిగాయి. ఇది సెక్టార్ రొటేషన్ — డబ్బు ఒక సెక్టార్ నుండి మరో సెక్టార్‌కు మారుతోంది. [pause] "
  "నాలుగు — హౌతీ, హోర్ముజ్ లాంటి ప్రపంచ వార్తలు మన మార్కెట్‌ను నేరుగా కదిలిస్తాయి. గ్లోబల్ న్యూస్‌ను గమనించండి. [pause] "
  "ఐదు — క్రమం తప్పకుండా SIP చేసేవారికి ఇలాంటి ఒక ఎర్ర రోజు కేవలం నాయిస్. దీర్ఘకాల ట్రెండ్ కాదు — కంగారుగా అమ్మొద్దు."),
 ("mw_recap", "sm_recap",
  {"title": "21 జూలై — ఒక్క చూపులో",
   "items": [
    "సెన్సెక్స్ −238 (77,470) · నిఫ్టీ −51 (24,188) — 2వ రోజు పతనం",
    "కారణం: క్రూడ్ $90+ (హౌతీ/హోర్ముజ్) + IT + PSU బ్యాంక్ + FII అమ్మకం",
    "పడినవి: Cipla, Dr Reddy's, TCS, Infosys, HDFC Bank, SBI",
    "పెరిగినవి: కెమికల్, సిమెంట్, మిడ్‌క్యాప్, స్మాల్‌క్యాప్",
    "బ్రెడ్త్ పాజిటివ్ — ఇరుకైన లార్జ్‌క్యాప్ షాక్, మార్కెట్ పతనం కాదు",
   ],
   "closer": "ఒక ఎర్ర రోజు కథ కాదు — దీర్ఘకాల క్రమశిక్షణే విజయం."},
  "ఇరవై ఒకటో తేదీ మార్కెట్ ఒక్క చూపులో. [pause] "
  "సెన్సెక్స్ రెండు వందల ముప్పై ఎనిమిది, నిఫ్టీ యాభై ఒక్క పాయింట్లు పడ్డాయి — వరుసగా రెండో రోజు. [pause] "
  "కారణం — క్రూడ్ తొంభై డాలర్లు దాటడం, హౌతీ, హోర్ముజ్ ఆందోళన, IT, PSU బ్యాంక్ షేర్లు, విదేశీ సంస్థల అమ్మకం. [pause] "
  "సిప్లా, డాక్టర్ రెడ్డీస్, TCS, ఇన్ఫోసిస్, HDFC బ్యాంక్, SBI పడ్డాయి. కెమికల్, సిమెంట్, మిడ్‌క్యాప్, స్మాల్‌క్యాప్ పెరిగాయి. [pause] "
  "బ్రెడ్త్ పాజిటివ్‌గా ఉంది — ఇది ఇరుకైన లార్జ్‌క్యాప్ షాక్, మొత్తం మార్కెట్ పతనం కాదు. [pause] "
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
