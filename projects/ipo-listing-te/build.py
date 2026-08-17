#!/usr/bin/env python3
"""IPO Listing Preview (Telugu) — SBI MF + Millworks SME, list Tue 21 Jul 2026.
Reuses `sm` scene set. GMP = unofficial signal, NOT a guarantee (stated in-video).
Facts verified in research/listing-21jul2026.md. Not advice. Usage: python3 build.py [il01]
"""
import json, os, re, subprocess, sys

VOICE = "te-IN-ShrutiNeural"; RATE = "-4%"; GAP = 0.5; PAUSE = 0.55; PREFIX = "sm"
ROOT = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(ROOT, "..", ".."))
PUBLIC = os.path.join(REPO, "composer", "public", PREFIX); RAW = os.path.join(ROOT, "assets", "raw"); FIN = os.path.join(ROOT, "assets")
for d in (PUBLIC, RAW, os.path.join(ROOT, "artifacts"), os.path.join(ROOT, "renders")):
    os.makedirs(d, exist_ok=True)

CHAPTERS = {
 "il01": [
 ("il_title", "sm_ptitle",
  {"title": "రేపటి IPO లిస్టింగ్‌లు", "sub": "SBI Mutual Fund + Millworks SME · 21 జూలై 2026", "kicker": "IPO LISTING · 21 JUL"},
  "రేపు రెండు IPOలు స్టాక్ మార్కెట్‌లో లిస్ట్ అవుతున్నాయి. [pause] "
  "ఒకటి — SBI మ్యూచువల్ ఫండ్, అంటే SBI ఫండ్స్ మేనేజ్‌మెంట్. రెండోది — Millworks Technologies, ఒక SME. [pause] "
  "సెంటిమెంట్ ఎలా ఉంది? GMP ఎంత లాభం సూచిస్తోంది? ఎగ్జిట్ స్ట్రాటజీ ఏమిటి? [pause] "
  "ఒక ముందస్తు హెచ్చరిక — GMP అనధికారికం, ఇది జోస్యం కాదు. వాస్తవ లిస్టింగ్ వేరుగా ఉండవచ్చు."),
 ("il_sbi", "sm_stats",
  {"kicker": "SBI FUNDS MANAGEMENT", "title": "SBI మ్యూచువల్ ఫండ్ — సెంటిమెంట్", "color": "#34D399",
   "stats": [
    {"label": "సబ్‌స్క్రిప్షన్ (మొత్తం)", "to": 41.66, "decimals": 2, "suffix": "x", "color": "#34D399", "sub": "QIB 140x · రిటైల్ 3.6x"},
    {"label": "GMP (అనధికారిక)", "to": 18, "suffix": "%", "color": "#FBBF24", "sub": "≈₹102 · లిస్టింగ్ ~₹676"},
    {"label": "ఇష్యూ సైజు", "to": 9.8, "decimals": 1, "prefix": "₹", "suffix": " వేల కోట్లు", "color": "#22D3EE", "sub": "పూర్తిగా OFS · ధర ₹545–574"},
   ],
   "note": "బలమైన సంస్థాగత డిమాండ్ (QIB 140x) · రిటైల్ మధ్యస్థం · నాణ్యమైన పెద్ద AMC. GMP మధ్యస్థ ~18%."},
  "మొదట SBI మ్యూచువల్ ఫండ్. [pause] "
  "ఇది మొత్తం నలభై ఒకటిన్నర రెట్లు సబ్‌స్క్రైబ్ అయింది. [pause] "
  "ముఖ్యంగా సంస్థాగత పెట్టుబడిదారులు — QIB — నూట నలభై రెట్లు దరఖాస్తు చేశారు. ఇది చాలా బలమైన సంకేతం. రిటైల్ మాత్రం మూడున్నర రెట్లు — మధ్యస్థం. [pause] "
  "GMP దాదాపు పద్దెనిమిది శాతం — అంటే ఐదు వందల డెబ్బై నాలుగు ధరపై, దాదాపు ఆరు వందల డెబ్బై ఆరుకు లిస్ట్ అవ్వొచ్చని గ్రే మార్కెట్ సూచన. [pause] "
  "ఇష్యూ దాదాపు తొమ్మిది వేల ఎనిమిది వందల కోట్లు — పూర్తిగా ఆఫర్ ఫర్ సేల్. అంటే కొత్త డబ్బు కంపెనీకి రాదు, పాత వాటాదారులు అమ్ముతున్నారు. [pause] "
  "సారాంశం — ఇది నాణ్యమైన పెద్ద AMC, సంస్థల డిమాండ్ బలంగా ఉంది. GMP మధ్యస్థం — పెద్ద పేలుడు కాదు, నిలకడైన లిస్టింగ్."),
 ("il_mill", "sm_stats",
  {"kicker": "MILLWORKS · BSE SME", "title": "Millworks SME — సెంటిమెంట్", "color": "#A78BFA",
   "stats": [
    {"label": "సబ్‌స్క్రిప్షన్ (మొత్తం)", "to": 219.5, "decimals": 1, "suffix": "x", "color": "#A78BFA", "sub": "NII 260x · QIB 194x · రిటైల్ 217x"},
    {"label": "GMP (అనధికారిక)", "to": 90, "suffix": "%+", "color": "#FBBF24", "sub": "≈₹297–400 · చాలా అస్థిరం"},
    {"label": "ఇష్యూ సైజు", "to": 160, "prefix": "₹", "suffix": " కోట్లు", "color": "#22D3EE", "sub": "BSE SME · ధర ₹315–331"},
   ],
   "note": "SME ఫ్రెంజీ — 219x సబ్‌స్క్రైబ్. కానీ SME = అధిక రిస్క్, తక్కువ లిక్విడిటీ, GMP నమ్మదగదు."},
  "ఇప్పుడు Millworks Technologies — ఒక BSE SME. [pause] "
  "ఇది ఏకంగా రెండు వందల పంతొమ్మిది రెట్లు సబ్‌స్క్రైబ్ అయింది. NII రెండు వందల అరవై రెట్లు, రిటైల్ రెండు వందల పదిహేడు రెట్లు — ఇది SME ఫ్రెంజీ. [pause] "
  "GMP దాదాపు తొంభై శాతం, కొన్ని సోర్సుల్లో నూట ఇరవై శాతం వరకు కూడా చూపిస్తోంది. [pause] "
  "ఇక్కడే మొదటి రెడ్ ఫ్లాగ్ — GMP విలువ చాలా అస్థిరంగా, వేర్వేరుగా ఉంది. ఇంత అస్థిర GMPను నమ్మలేం. [pause] "
  "ఇష్యూ కేవలం నూట అరవై కోట్లు — చిన్న SME. [pause] "
  "సారాంశం — హైప్ చాలా ఎక్కువ. పెద్ద లిస్టింగ్ పేలుడు రావచ్చు. కానీ SME అంటే — అధిక రిస్క్, తక్కువ లిక్విడిటీ, ఆకస్మిక రివర్సల్‌లు. జాగ్రత్త."),
 ("il_gmp", "sm_myths",
  {"kicker": "THE GMP TRUTH", "title": "GMP గురించి నిజం — జోస్యం కాదు",
   "pairs": [
    {"m": "GMP 90% ఉంది — ఖచ్చితంగా అంత లాభం", "f": "GMP అనధికారికం, క్షణక్షణం మారుతుంది — లిస్టింగ్‌కి కుప్పకూలవచ్చు"},
    {"m": "219x సబ్‌స్క్రైబ్ = గ్యారంటీ లాభం", "f": "ఎక్కువ సబ్‌స్క్రిప్షన్ ఉన్న IPOలూ ఫ్లాట్‌గా/కిందికి లిస్ట్ అయ్యాయి"},
    {"m": "SME లిస్టింగ్ = సులభ డబ్బు", "f": "SME తక్కువ లిక్విడిటీ — కోట్ ధరకు అమ్మలేకపోవచ్చు; సర్క్యూట్‌లు"},
   ]},
  "ఇక్కడ అతి ముఖ్యమైన నిజం — GMP గురించి. [pause] "
  "మొదటి అపోహ — GMP తొంభై శాతం ఉంది కాబట్టి, ఖచ్చితంగా అంత లాభం వస్తుందని. [pause] "
  "నిజం — GMP అనధికారిక గ్రే మార్కెట్ అంచనా. ఇది క్షణక్షణం మారుతుంది, లిస్టింగ్ రోజుకల్లా కుప్పకూలవచ్చు. [pause] "
  "రెండో అపోహ — రెండు వందల రెట్లు సబ్‌స్క్రైబ్ అయింది కాబట్టి లాభం ఖాయమని. [pause] "
  "నిజం — భారీగా సబ్‌స్క్రైబ్ అయిన IPOలు కూడా ఫ్లాట్‌గా, కొన్నిసార్లు ఇష్యూ ధర కంటే కిందికే లిస్ట్ అయ్యాయి. [pause] "
  "మూడో అపోహ — SME లిస్టింగ్ అంటే సులభ డబ్బని. [pause] "
  "నిజం — SMEలో లిక్విడిటీ చాలా తక్కువ. మీరు చూసిన ధరకు అమ్మలేకపోవచ్చు, సర్క్యూట్ లిమిట్‌లు అడ్డుపడతాయి. [pause] "
  "కాబట్టి — GMPను జోస్యంగా కాదు, ఒక సెంటిమెంట్ సూచికగా మాత్రమే చూడండి."),
 ("il_exit", "sm_checklist",
  {"kicker": "EXIT STRATEGY", "title": "ఎగ్జిట్ స్ట్రాటజీ — 5 నియమాలు", "color": "#34D399", "icon": "🎯",
   "items": [
    "లిస్టింగ్‌కు ముందే నిర్ణయించండి — ఫ్లిప్ చేయాలా, ఉంచాలా",
    "టార్గెట్ + స్టాప్-లాస్ రెండూ ముందే పెట్టుకోండి",
    "SME అమ్మేటప్పుడు లిమిట్ ఆర్డర్ వాడండి — లిక్విడిటీ తక్కువ",
    "లిస్టింగ్ రోజు అమ్మితే షార్ట్ టర్మ్ పన్ను 20%",
    "GMP వెంట పరుగెత్తొద్దు — అలాట్ కాకపోతే పోయిందేమీ లేదు",
   ]},
  "ఇప్పుడు అసలు ముఖ్యమైనది — ఎగ్జిట్ స్ట్రాటజీ. ఐదు నియమాలు. [pause] "
  "ఒకటి — లిస్టింగ్‌కు ముందే నిర్ణయించుకోండి. ఇది లిస్టింగ్ లాభం కోసమా — ఫ్లిప్ — లేక దీర్ఘకాలం ఉంచడానికా? ఈ నిర్ణయం ముందే ఉండాలి. [pause] "
  "రెండు — టార్గెట్, స్టాప్-లాస్ రెండూ ముందే పెట్టుకోండి. ఉదాహరణకు, పదిహేను శాతం లాభం వస్తే అమ్ముతా, లేదా పడితే ఇక్కడ ఆపుతా — అని. [pause] "
  "మూడు — SME అమ్మేటప్పుడు తప్పకుండా లిమిట్ ఆర్డర్ వాడండి. మార్కెట్ ఆర్డర్ వేస్తే, లిక్విడిటీ తక్కువ వల్ల చాలా తక్కువ ధరకు అమ్ముడుపోవచ్చు. [pause] "
  "నాలుగు — లిస్టింగ్ రోజునే అమ్మితే, ఆ లాభంపై ఇరవై శాతం షార్ట్ టర్మ్ పన్ను పడుతుంది. దీన్ని లెక్కలో పెట్టుకోండి. [pause] "
  "ఐదు — GMP ఎక్కువుందని FOMOతో పరుగెత్తొద్దు. అలాట్ కాకపోతే మీరు పోగొట్టుకున్నదేమీ లేదు — లిస్ట్ అయ్యాక కూడా కొనొచ్చు."),
 ("il_compare", "sm_compare3",
  {"kicker": "HOLD vs FLIP", "title": "ఉంచాలా, ఫ్లిప్ చేయాలా?",
   "cols": [
    {"name": "SBI Mutual Fund", "color": "#34D399", "emoji": "🏦", "hi": True, "rows": [
     {"k": "ఏమిటి", "v": "పెద్ద నాణ్యమైన AMC"},
     {"k": "థీసిస్", "v": "భారత్ MF బూమ్ · AUM ₹82L Cr"},
     {"k": "వ్యూహం", "v": "లిస్టింగ్ గెయిన్ లేదా దీర్ఘకాలం"},
     {"k": "రిస్క్", "v": "OFS · valuation చూడండి"}]},
    {"name": "Millworks SME", "color": "#A78BFA", "emoji": "⚡", "rows": [
     {"k": "ఏమిటి", "v": "చిన్న SME · హైప్ ఎక్కువ"},
     {"k": "సిగ్నల్", "v": "219x · GMP 90%+"},
     {"k": "వ్యూహం", "v": "ఫ్లిప్ మాత్రమే — ఉంచడం రిస్క్"},
     {"k": "రిస్క్", "v": "తక్కువ లిక్విడిటీ · రివర్సల్"}]},
    {"name": "మీ నిర్ణయం", "color": "#22D3EE", "emoji": "🧭", "rows": [
     {"k": "సూత్రం", "v": "నాణ్యత > హైప్"},
     {"k": "ఫ్లిప్", "v": "టార్గెట్ + స్టాప్ తప్పనిసరి"},
     {"k": "SME", "v": "కొత్తవారికి కాదు"},
     {"k": "అలాట్ కాలేదా?", "v": "బాధపడకండి — వదిలేయండి"}]},
   ]},
  "మరి ఉంచాలా, ఫ్లిప్ చేయాలా? రెండింటినీ పోల్చి చూద్దాం. [pause] "
  "SBI మ్యూచువల్ ఫండ్ — పెద్ద, నాణ్యమైన AMC. భారత్ మ్యూచువల్ ఫండ్ పరిశ్రమ ఎనభై రెండు లక్షల కోట్లకు చేరిన వృద్ధి కథ దీని వెనుక ఉంది. "
  "కాబట్టి కొందరు లిస్టింగ్ లాభం తీసుకోవచ్చు, కొందరు దీర్ఘకాలం ఉంచుకోవచ్చు. కానీ valuation చూసుకోండి. [pause] "
  "Millworks — చిన్న SME, హైప్ చాలా ఎక్కువ. ఇక్కడ వ్యూహం ఫ్లిప్ మాత్రమే — దీన్ని దీర్ఘకాలం ఉంచడం చాలా రిస్క్. తక్కువ లిక్విడిటీ, ఆకస్మిక రివర్సల్‌లు. [pause] "
  "మీ నిర్ణయానికి సూత్రం — నాణ్యత హైప్ కంటే ముఖ్యం. ఫ్లిప్ చేస్తే టార్గెట్, స్టాప్ తప్పనిసరి. SME కొత్తవారికి కాదు. అలాట్ కాకపోతే బాధపడకండి."),
 ("il_recap", "sm_recap",
  {"title": "రేపటి లిస్టింగ్‌లు — సారాంశం",
   "items": [
    "SBI MF: 41.66x · QIB 140x బలం · GMP ~18% · నాణ్యత",
    "Millworks SME: 219x · GMP ~90% · హైప్ + అధిక రిస్క్",
    "GMP = అనధికారిక సూచిక, జోస్యం కాదు — మారుతుంది",
    "ఎగ్జిట్: ముందే నిర్ణయం + టార్గెట్ + స్టాప్ + లిమిట్ ఆర్డర్",
    "SBI ఉంచొచ్చు · SME ఫ్లిప్ మాత్రమే · నాణ్యత > హైప్",
   ],
   "closer": "GMPకి కాదు — మీ ప్లాన్‌కు కట్టుబడండి."},
  "రేపటి లిస్టింగ్‌ల సారాంశం. [pause] "
  "SBI మ్యూచువల్ ఫండ్ — నలభై ఒకటిన్నర రెట్లు సబ్‌స్క్రైబ్, QIB డిమాండ్ బలంగా, GMP పద్దెనిమిది శాతం. నాణ్యమైనది. [pause] "
  "Millworks SME — రెండు వందల పంతొమ్మిది రెట్లు, GMP తొంభై శాతం. హైప్ ఎక్కువ, రిస్క్ కూడా ఎక్కువ. [pause] "
  "GMP అనధికారిక సూచిక మాత్రమే — జోస్యం కాదు, ఇది మారుతుంది. [pause] "
  "ఎగ్జిట్ స్ట్రాటజీ — లిస్టింగ్‌కు ముందే నిర్ణయం, టార్గెట్, స్టాప్-లాస్, SMEకి లిమిట్ ఆర్డర్. [pause] "
  "SBIని ఉంచుకోవచ్చు, SMEను ఫ్లిప్ మాత్రమే చేయండి. ఎప్పుడూ నాణ్యత హైప్ కంటే ముఖ్యం. [pause] "
  "GMPకి కాదు — మీ సొంత ప్లాన్‌కు కట్టుబడండి. [pause] "
  "ఈ సమాచారం బహిరంగ వార్తల నుండి సేకరించింది, GMP అనధికారికం — విశ్లేషణ కోసమే, పెట్టుబడి సలహా కాదు. మీ నిర్ణయాలకు నిపుణుల సలహా తీసుకోండి. చూసినందుకు ధన్యవాదాలు."),
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
