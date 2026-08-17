#!/usr/bin/env python3
"""Expert Strategies (Telugu) — what India's top market voices are saying, 2026.
Reuses `sm` scene set. Views paraphrased & attributed per skill rules (their views,
not recommendations). Sources in research/experts-2026.md. Not advice.
Usage: python3 build.py  |  python3 build.py ex01
"""
import json, os, re, subprocess, sys

VOICE = "te-IN-ShrutiNeural"; RATE = "-4%"; GAP = 0.5; PAUSE = 0.55; PREFIX = "sm"
ROOT = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(ROOT, "..", ".."))
PUBLIC = os.path.join(REPO, "composer", "public", PREFIX); RAW = os.path.join(ROOT, "assets", "raw"); FIN = os.path.join(ROOT, "assets")
for d in (PUBLIC, RAW, os.path.join(ROOT, "artifacts"), os.path.join(ROOT, "renders")):
    os.makedirs(d, exist_ok=True)

CHAPTERS = {
 "ex01": [
 ("ex_title", "sm_ptitle",
  {"title": "నిపుణులు ఏం చెబుతున్నారు?", "sub": "భారత్ టాప్ మార్కెట్ వాయిస్‌లు · వ్యూహాలు · 2026", "kicker": "EXPERT STRATEGIES · 2026"},
  "మార్కెట్‌లో అనుభవం, పేరు ఉన్న నిపుణులు — ఫండ్ మేనేజర్లు, విశ్లేషకులు — 2026లో ఏం చెబుతున్నారు? [pause] "
  "నలుగురు అగ్రశ్రేణి వాయిస్‌ల వ్యూహాలను తీసుకుని, వాటిలోని ఉమ్మడి సందేశాన్ని చూద్దాం. [pause] "
  "ఇవి వారి వ్యక్తిగత అభిప్రాయాలు — సమాచారం కోసమే, పెట్టుబడి సలహా కాదు."),
 ("ex_hook", "sm_stats",
  {"kicker": "ONE COMMON MESSAGE", "title": "వేర్వేరు నిపుణులు — ఒకే దిశ",
   "stats": [
    {"label": "భారత్ చారిత్రక ఆదాయ వృద్ధి", "to": 15, "suffix": "%", "color": "#34D399", "sub": "Samir Arora — 13–15% (రూపాయిల్లో)"},
    {"label": "రాబడిలో అసెట్ అలొకేషన్ వాటా", "to": 90, "suffix": "%", "color": "#22D3EE", "sub": "Nilesh Shah — స్టాక్ ఎంపిక 10%"},
    {"label": "స్మాల్/మిడ్ క్యాప్ వాల్యుయేషన్", "to": 20, "suffix": " ఏళ్ల గరిష్ఠం", "color": "#FB7185", "sub": "Saurabh Mukherjea హెచ్చరిక"},
   ],
   "note": "నలుగురు టాప్ నిపుణులు — ఉమ్మడి సందేశం: క్వాలిటీ + అసెట్ అలొకేషన్ + క్రమశిక్షణ."},
  "ముందు కొన్ని అంకెలు చూడండి — ఇవే నిపుణుల ఆలోచనకు పునాది. [pause] "
  "Helios ఫండ్ మేనేజర్ సమీర్ అరోరా ప్రకారం — భారత్ చారిత్రకంగా పదమూడు నుండి పదిహేను శాతం ఆదాయ వృద్ధి చూపింది. ఇది స్థిరమైన వృద్ధి. [pause] "
  "Kotak నిలేష్ షా ప్రకారం — మీ రాబడిలో తొంభై శాతం అసెట్ అలొకేషన్ నుండే వస్తుంది, స్టాక్ ఎంపిక నుండి కేవలం పది శాతం. [pause] "
  "Marcellus సౌరభ్ ముఖర్జియా హెచ్చరిక — స్మాల్, మిడ్ క్యాప్ వాల్యుయేషన్‌లు రెండు దశాబ్దాల గరిష్ఠ స్థాయిలో ఉన్నాయి. [pause] "
  "వేర్వేరు నిపుణులు — కానీ ఉమ్మడి సందేశం ఒకటే. క్వాలిటీ, అసెట్ అలొకేషన్, క్రమశిక్షణ. ఒక్కొక్కరి వ్యూహం చూద్దాం."),
 ("ex_panel", "sm_iconcards",
  {"kicker": "THE 4 VOICES", "title": "నలుగురు నిపుణులు — వారి వ్యూహం", "color": "#22D3EE",
   "items": [
    {"emoji": "🧠", "k": "Samir Arora", "v": "'ఎలిమినేషన్ స్ట్రాటజీ' — విజేతలను వెతకడం కంటే, చెత్త బాటమ్ 150 షేర్లను వదిలేయడం సులభం", "chip": "Helios"},
    {"emoji": "🏛️", "k": "Saurabh Mukherjea", "v": "క్వాలిటీ లార్జ్ క్యాప్ వైపు — క్లీన్ అకౌంటింగ్, మంచి క్యాపిటల్ కేటాయింపు, బలమైన మోట్", "chip": "Marcellus"},
    {"emoji": "⚖️", "k": "Nilesh Shah", "v": "అసెట్ అలొకేషనే రాజు — ఈక్విటీ, గోల్డ్, డెట్ మధ్య సమతుల్యం; 80–20 రూల్", "chip": "Kotak"},
    {"emoji": "🤖", "k": "Deepak Shenoy", "v": "రూల్స్-బేస్డ్, క్వాంటిటేటివ్ మొమెంటమ్ — భావోద్వేగాన్ని తీసేసి, డేటా ప్రకారం నడవడం", "chip": "Capitalmind"},
   ]},
  "ఇప్పుడు నలుగురు నిపుణులు, వారి వ్యూహాలు. [pause] "
  "మొదటిది — సమీర్ అరోరా, Helios. ఆయన 'ఎలిమినేషన్ స్ట్రాటజీ' అనుసరిస్తారు. "
  "ఎవరు గెలుస్తారో ఊహించడం కష్టం — కానీ ఎవరు ఓడతారో గుర్తించడం సులభం అంటారు. అందుకే బాటమ్ నూట యాభై చెత్త షేర్లను వదిలేస్తారు. [pause] "
  "రెండోది — సౌరభ్ ముఖర్జియా, Marcellus. క్వాలిటీ లార్జ్ క్యాప్ కంపెనీలవైపు. "
  "క్లీన్ అకౌంటింగ్, మంచి పాలన, తెలివైన క్యాపిటల్ కేటాయింపు, బలమైన మోట్ — ఈ లక్షణాలున్న కంపెనీలనే ఎంచుకుంటారు. [pause] "
  "మూడోది — నిలేష్ షా, Kotak. ఆయన దృష్టిలో అసెట్ అలొకేషనే రాజు. ఈక్విటీ, గోల్డ్, డెట్ మధ్య సమతుల్యమే అసలు కీలకం. [pause] "
  "నాలుగోది — దీపక్ శెనోయ్, Capitalmind. రూల్స్-బేస్డ్, క్వాంటిటేటివ్ మొమెంటమ్. భావోద్వేగాన్ని తీసేసి, డేటా, నియమాల ప్రకారం నడవడం."),
 ("ex_views", "sm_myths",
  {"kicker": "WHAT THEY DEBUNK", "title": "నిపుణులు కొట్టిపారేసే అపోహలు",
   "pairs": [
    {"m": "గెలిచే షేర్‌ను వెతికి పట్టుకోవాలి", "f": "Arora: ఓడేవాటిని వదిలేయడం సులభం, సురక్షితం — రిస్క్ కంట్రోల్"},
    {"m": "స్మాల్ క్యాప్ దూసుకుపోతోంది, కొనాలి", "f": "Mukherjea: వాల్యుయేషన్ 20 ఏళ్ల గరిష్ఠం — క్వాలిటీ లార్జ్ క్యాప్ వైపు"},
    {"m": "మనసుతో, వార్తలతో ట్రేడ్ చేయాలి", "f": "Shenoy: భావోద్వేగం తీసేసి, నియమాల ప్రకారం నడవాలి"},
   ]},
  "ఈ నిపుణులు ఉమ్మడిగా కొట్టిపారేసే అపోహలు మూడు. [pause] "
  "మొదటిది — గెలిచే షేర్‌ను ముందే వెతికి పట్టుకోవాలనేది. [pause] "
  "అరోరా అంటారు — ఎవరు గెలుస్తారో ఊహించడం కష్టం. ఓడేవాటిని, ప్రమాదకరమైన వాటిని వదిలేయడమే తెలివైన, సురక్షితమైన మార్గం. ఇదే రిస్క్ కంట్రోల్. [pause] "
  "రెండోది — స్మాల్ క్యాప్ దూసుకుపోతోంది కదా, ఇప్పుడే కొనాలనేది. [pause] "
  "ముఖర్జియా హెచ్చరిస్తారు — ఈ వాల్యుయేషన్‌లు ఇరవై ఏళ్ల గరిష్ఠంలో ఉన్నాయి, రెండు వేల నాలుగు నాటి రియల్ ఎస్టేట్ బూమ్‌ను గుర్తు చేస్తున్నాయి. క్వాలిటీ లార్జ్ క్యాప్ వైపు మళ్లమంటారు. [pause] "
  "మూడోది — మనసుతో, వార్తలతో ట్రేడ్ చేయాలనేది. [pause] "
  "శెనోయ్ అంటారు — భావోద్వేగమే అతిపెద్ద శత్రువు. నియమాల ప్రకారం, డేటా ప్రకారం నడవాలి."),
 ("ex_alloc", "sm_alloc",
  {"kicker": "NILESH SHAH · ASSET ALLOCATION", "title": "అసెట్ అలొకేషనే రాజు — ఒక నమూనా",
   "slices": [
    {"label": "ఈక్విటీ", "pct": 60, "c": "#34D399"},
    {"label": "గోల్డ్ / సిల్వర్", "pct": 20, "c": "#FBBF24"},
    {"label": "డెట్", "pct": 20, "c": "#22D3EE"},
   ],
   "note": "Nilesh Shah: రాబడిలో 90% అసెట్ అలొకేషన్ నుండే · 80–20 రూల్ — 80% దీర్ఘకాలం, 20% హై-రిస్క్ · ఇది నమూనా, సలహా కాదు"},
  "నలుగురిలో అత్యంత ఆచరణాత్మక సందేశం నిలేష్ షాది — అసెట్ అలొకేషన్. [pause] "
  "ఆయన అంటారు — మీ దీర్ఘకాల రాబడిలో తొంభై శాతం, మీరు డబ్బును ఏ తరగతుల్లో పంచారు అనేదానిపైనే ఆధారపడి ఉంటుంది. ఏ షేర్ ఎంచుకున్నారన్నది కేవలం పది శాతం. [pause] "
  "ఒక నమూనా — అరవై శాతం ఈక్విటీ, ఇరవై శాతం గోల్డ్, సిల్వర్, ఇరవై శాతం డెట్. [pause] "
  "ఆయన 80–20 రూల్ కూడా చెబుతారు — ఎనభై శాతం డబ్బు దీర్ఘకాల అసెట్ అలొకేషన్‌లో, మిగతా ఇరవై శాతం మాత్రమే హై-రిస్క్ ఆలోచనలకు. [pause] "
  "ముఖ్యంగా — మార్కెట్ పతనాన్ని ఆయన అవకాశంగా చూడమంటారు. హెచ్చుతగ్గులు ఈక్విటీలో సహజం. [pause] "
  "గుర్తుంచుకోండి — ఇది ఒక నమూనా మాత్రమే, మీ లక్ష్యాలను బట్టి నిష్పత్తి మీరే నిర్ణయించుకోవాలి."),
 ("ex_thread", "sm_iconcards",
  {"kicker": "THE COMMON THREAD", "title": "నలుగురి ఉమ్మడి సందేశం", "color": "#34D399",
   "items": [
    {"emoji": "💎", "k": "క్వాలిటీ ముందు", "v": "అధిక వాల్యుయేషన్ స్మాల్ క్యాప్‌ల వెంట పరుగు వద్దు — నాణ్యమైనవి", "chip": "1"},
    {"emoji": "⚖️", "k": "అలొకేషన్ కీలకం", "v": "ఏ షేర్ కంటే — ఈక్విటీ, గోల్డ్, డెట్ మధ్య పంపిణీయే రాబడిని నిర్ణయిస్తుంది", "chip": "2"},
    {"emoji": "🧘", "k": "క్రమశిక్షణ", "v": "భావోద్వేగం కాదు — నియమాలు, డేటా, ఓపిక", "chip": "3"},
    {"emoji": "🇮🇳", "k": "భారత్‌పై నమ్మకం", "v": "క్రాష్ అంచనా లేదు — స్థిరమైన ఆదాయ వృద్ధిపై పెట్టుబడి కొనసాగించండి", "chip": "4"},
   ]},
  "ఇప్పుడు అసలు విలువ — నలుగురి ఉమ్మడి సందేశం. నాలుగు అంశాలు. [pause] "
  "ఒకటి — క్వాలిటీ ముందు. అధిక వాల్యుయేషన్ ఉన్న స్మాల్ క్యాప్‌ల వెంట పరుగెత్తవద్దు. నాణ్యమైన కంపెనీలవైపు మొగ్గు. [pause] "
  "రెండు — అలొకేషన్ కీలకం. ఏ షేర్ ఎంచుకున్నారన్నది కాదు — ఈక్విటీ, గోల్డ్, డెట్ మధ్య ఎలా పంచారన్నదే రాబడిని నిర్ణయిస్తుంది. [pause] "
  "మూడు — క్రమశిక్షణ. భావోద్వేగంతో కాదు, నియమాలు, డేటా, ఓపికతో పెట్టుబడి. [pause] "
  "నాలుగు — భారత్‌పై నమ్మకం. ఎవరూ క్రాష్ అంచనా వేయడం లేదు. స్థిరమైన ఆదాయ వృద్ధిపై పెట్టుబడి కొనసాగించమనే చెబుతున్నారు. [pause] "
  "కోట్ల రూపాయలు నిర్వహించే నిపుణులు — అందరూ ఒకే మౌలిక సూత్రాల వైపు చూపిస్తున్నారు."),
 ("ex_apply", "sm_checklist",
  {"kicker": "FOR YOU", "title": "సామాన్య పెట్టుబడిదారు కోసం — 5 పాఠాలు", "color": "#34D399", "icon": "💡",
   "items": [
    "కోర్ = క్వాలిటీ లార్జ్ క్యాప్ / ఇండెక్స్ ఫండ్ SIP",
    "ఈక్విటీ, గోల్డ్, డెట్ మధ్య పంచండి — అలొకేషన్‌కు ప్రాధాన్యం",
    "అధిక వాల్యుయేషన్ స్మాల్ క్యాప్ హైప్‌ను వెంబడించొద్దు",
    "నియమాలు రాసుకుని, భావోద్వేగంతో మార్చొద్దు",
    "పతనం = అవకాశం; SIP ఆపొద్దు — భారత్ కథ దీర్ఘకాలం",
   ]},
  "మరి సామాన్య పెట్టుబడిదారు ఈ నిపుణుల మాటల నుండి ఏం తీసుకోవాలి? ఐదు పాఠాలు. [pause] "
  "ఒకటి — మీ పోర్ట్‌ఫోలియో కోర్‌ను క్వాలిటీ లార్జ్ క్యాప్ లేదా ఇండెక్స్ ఫండ్ SIPలో ఉంచండి. [pause] "
  "రెండు — డబ్బును ఈక్విటీ, గోల్డ్, డెట్ మధ్య పంచండి. ఏ షేర్ కంటే ఈ పంపిణీయే ముఖ్యం. [pause] "
  "మూడు — అధిక వాల్యుయేషన్ ఉన్న స్మాల్ క్యాప్ హైప్‌ను గుడ్డిగా వెంబడించవద్దు. [pause] "
  "నాలుగు — మీ నియమాలు ముందే రాసుకోండి. మార్కెట్ ఊగినప్పుడు భావోద్వేగంతో వాటిని మార్చవద్దు. [pause] "
  "ఐదు — పతనాన్ని అవకాశంగా చూడండి. SIP ఆపవద్దు. భారత్ వృద్ధి కథ దీర్ఘకాలానిది. [pause] "
  "ఈ ఐదూ — నలుగురు నిపుణుల సారాంశం, ఒక్క సామాన్యుడి భాషలో."),
 ("ex_recap", "sm_recap",
  {"title": "నిపుణుల వ్యూహాలు — సారాంశం",
   "items": [
    "Arora: ఎలిమినేషన్ — ఓడేవాటిని వదిలేయి (రిస్క్ కంట్రోల్)",
    "Mukherjea: క్వాలిటీ లార్జ్ క్యాప్; స్మాల్ క్యాప్ హెచ్చరిక",
    "Nilesh Shah: అసెట్ అలొకేషనే 90% రాబడి; 80–20 రూల్",
    "Shenoy: రూల్స్-బేస్డ్, భావోద్వేగం వద్దు",
    "ఉమ్మడి: క్వాలిటీ + అలొకేషన్ + క్రమశిక్షణ + ఓపిక",
   ],
   "closer": "నిపుణులు వేర్వేరు — మౌలిక సూత్రాలు ఒకటే."},
  "నిపుణుల వ్యూహాల సారాంశం. [pause] "
  "సమీర్ అరోరా — ఎలిమినేషన్ స్ట్రాటజీ, ఓడేవాటిని వదిలేయడం. [pause] "
  "సౌరభ్ ముఖర్జియా — క్వాలిటీ లార్జ్ క్యాప్, స్మాల్ క్యాప్ ఫ్రెంజీపై హెచ్చరిక. [pause] "
  "నిలేష్ షా — రాబడిలో తొంభై శాతం అసెట్ అలొకేషన్ నుండే, 80–20 రూల్. [pause] "
  "దీపక్ శెనోయ్ — రూల్స్-బేస్డ్, భావోద్వేగం లేని పెట్టుబడి. [pause] "
  "ఉమ్మడి సందేశం — క్వాలిటీ, అసెట్ అలొకేషన్, క్రమశిక్షణ, ఓపిక. [pause] "
  "నిపుణులు వేర్వేరు, కానీ మౌలిక సూత్రాలు ఒకటే. [pause] "
  "ఇవి ఆయా నిపుణుల వ్యక్తిగత అభిప్రాయాలు, బహిరంగ వార్తల నుండి సేకరించినవి — విశ్లేషణ కోసమే, పెట్టుబడి సలహా కాదు. మీ నిర్ణయాలకు SEBI రిజిస్టర్డ్ సలహాదారును సంప్రదించండి. చూసినందుకు ధన్యవాదాలు."),
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
