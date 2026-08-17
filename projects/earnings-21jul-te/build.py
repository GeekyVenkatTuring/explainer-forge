#!/usr/bin/env python3
"""Q1 FY27 Earnings Day (Telugu) — 21 July 2026. Reuses `sm` scene set.
Every number verified in research/earnings-21jul2026.md. Info aggregation, not advice.
Usage: python3 build.py            (all)   |   python3 build.py er21
"""
import json, os, re, subprocess, sys, time

VOICE = "te-IN-ShrutiNeural"; RATE = "-4%"; GAP = 0.5; PAUSE = 0.55; PREFIX = "sm"
ROOT = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(ROOT, "..", ".."))
PUBLIC = os.path.join(REPO, "composer", "public", PREFIX); RAW = os.path.join(ROOT, "assets", "raw"); FIN = os.path.join(ROOT, "assets")
for d in (PUBLIC, RAW, os.path.join(ROOT, "artifacts"), os.path.join(ROOT, "renders")):
    os.makedirs(d, exist_ok=True)

CHAPTERS = {
 "er21": [
 ("er_title", "sm_ptitle",
  {"title": "నేటి Q1 ఫలితాలు", "sub": "జూలై 21, 2026 · ~45 కంపెనీల త్రైమాసిక ఫలితాలు · విశ్లేషణ", "kicker": "EARNINGS DAY · 21 JUL 2026"},
  "జూలై ఇరవై ఒకటి — నేడు ఒక భారీ ఫలితాల రోజు. దాదాపు నలభై ఐదు కంపెనీలు తమ మొదటి త్రైమాసిక ఫలితాలు ప్రకటించాయి. [pause] "
  "ఎవరి లాభం ఎంత పెరిగింది, ఎవరిది పడింది, ఏ అంకె వెనుక ఏ కథ ఉంది — అన్నీ విశ్లేషిద్దాం. [pause] "
  "ఒక ముఖ్య విషయం — ఈ ఫలితాలన్నీ గత ఏడాది ఇదే క్వార్టర్‌తో, అంటే YoY, పోల్చినవి. "
  "ఇది సమాచార విశ్లేషణ మాత్రమే — పెట్టుబడి సలహా కాదు."),
 ("er_score", "sm_stats",
  {"kicker": "TOP BEATS · NET PROFIT (YoY)", "title": "నేటి టాప్ 3 — నికర లాభం",
   "stats": [
    {"label": "Bajaj Auto", "to": 3226, "prefix": "₹", "suffix": " Cr", "color": "#34D399", "sub": "+46% YoY*"},
    {"label": "TVS Motor", "to": 1058, "prefix": "₹", "suffix": " Cr", "color": "#34D399", "sub": "+65% · ఆల్-టైమ్ Q1 గరిష్ఠం"},
    {"label": "M&M Financial", "to": 927, "prefix": "₹", "suffix": " Cr", "color": "#34D399", "sub": "+75% YoY"},
   ],
   "note": "ఆటో, ఫైనాన్షియల్ కంపెనీలు నేటి ఫలితాల్లో మెరిశాయి. *కానీ Bajaj Auto అంకె వెనుక ఒక కారణం ఉంది — తర్వాత చూద్దాం."},
  "ముందు నేటి టాప్ మూడు లాభాలు చూద్దాం. [pause] "
  "మొదటిది — Bajaj Auto. నికర లాభం మూడు వేల రెండు వందల ఇరవై ఆరు కోట్లు — గత ఏడాదితో పోలిస్తే నలభై ఆరు శాతం పెరిగింది. [pause] "
  "రెండోది — TVS Motor. లాభం వెయ్యి యాభై ఎనిమిది కోట్లు — అరవై ఐదు శాతం పెరిగింది. ఇది కంపెనీ చరిత్రలోనే అత్యధిక త్రైమాసిక లాభం. [pause] "
  "మూడోది — Mahindra & Mahindra Financial. లాభం తొమ్మిది వందల ఇరవై ఏడు కోట్లు — డెబ్బై ఐదు శాతం దూసుకెళ్లింది. [pause] "
  "ఆటో, ఫైనాన్షియల్ రంగాలు నేడు మెరిశాయి. కానీ Bajaj Auto అంకె వెనుక ఒక ముఖ్యమైన కారణం ఉంది — దాన్ని కాసేపట్లో చూద్దాం."),
 ("er_beats", "sm_iconcards",
  {"kicker": "THE BIG BEATS", "title": "బలమైన ఫలితాలు — 4 కంపెనీలు", "color": "#34D399",
   "items": [
    {"emoji": "🏍️", "k": "Bajaj Auto", "v": "లాభం ₹3,226 Cr (+46%), రెవెన్యూ ₹21,689 Cr (+65%) — కానీ కన్సాలిడేషన్ మార్పుతో పెరిగింది", "chip": "*ఆప్టికల్"},
    {"emoji": "🛵", "k": "TVS Motor", "v": "లాభం ₹1,058 Cr (+65%) — ఆల్-టైమ్ Q1 గరిష్ఠం; EV అమ్మకాలు +86%; షేర్ +6% పెరిగింది", "chip": "బిగ్ బీట్"},
    {"emoji": "🚜", "k": "M&M Financial", "v": "లాభం ₹927 Cr (+75%); రుణ పంపిణీ ₹15,560 Cr (+21%); AUM ₹1.37 లక్ష కోట్లు (+12%)", "chip": "+75%"},
    {"emoji": "🏦", "k": "Bandhan Bank", "v": "లాభం ₹502 Cr (+35%) — తక్కువ ప్రొవిజన్లు; NII ₹2,921 Cr (+6%); NIM 6.2%", "chip": "+35%"},
   ]},
  "ఇప్పుడు నేటి నాలుగు బలమైన ఫలితాలు వివరంగా. [pause] "
  "మొదటిది — Bajaj Auto. నికర లాభం మూడు వేల రెండు వందల ఇరవై ఆరు కోట్లు, రెవెన్యూ ఇరవై ఒక వేల ఆరు వందల ఎనభై తొమ్మిది కోట్లు — అరవై ఐదు శాతం. కానీ ఈ భారీ పెరుగుదల కన్సాలిడేషన్ మార్పు వల్ల వచ్చింది — దీని గురించి తర్వాత. [pause] "
  "రెండోది — TVS Motor. లాభం వెయ్యి యాభై ఎనిమిది కోట్లు, అరవై ఐదు శాతం — ఆల్-టైమ్ Q1 గరిష్ఠం. ఎలక్ట్రిక్ వాహన అమ్మకాలు ఎనభై ఆరు శాతం పెరిగాయి. ఫలితం తర్వాత షేర్ ఆరు శాతం ఎగిసింది. [pause] "
  "మూడోది — M&M Financial. లాభం తొమ్మిది వందల ఇరవై ఏడు కోట్లు, డెబ్బై ఐదు శాతం. రుణ పంపిణీ ఇరవై ఒక్క శాతం, ఆస్తులు పన్నెండు శాతం పెరిగాయి. [pause] "
  "నాలుగోది — Bandhan Bank. లాభం ఐదు వందల రెండు కోట్లు, ముప్పై ఐదు శాతం — ప్రొవిజన్లు తగ్గడం, ఆస్తి నాణ్యత మెరుగవడం వల్ల. వడ్డీ మార్జిన్ ఆరు పాయింట్ రెండు శాతం."),
 ("er_more", "sm_iconcards",
  {"kicker": "MORE RESULTS", "title": "మరిన్ని కంపెనీల ఫలితాలు", "color": "#22D3EE",
   "items": [
    {"emoji": "📞", "k": "Sagility", "v": "రెవెన్యూ ₹2,024 Cr (+27.6%); నికర లాభం +73.5% — హెల్త్‌కేర్ BPO బలంగా", "chip": "+73.5%"},
    {"emoji": "💻", "k": "NIIT", "v": "రెవెన్యూ +14%; నికర లాభం +85% — స్కిల్లింగ్, ట్రైనింగ్ డిమాండ్", "chip": "+85%"},
    {"emoji": "🛒", "k": "IndiaMART", "v": "రెవెన్యూ ₹414 Cr (+11.4%); లాభం ₹172 Cr (+12%) — స్థిరమైన B2B వృద్ధి", "chip": "+12%"},
    {"emoji": "🧪", "k": "Anthem Biosciences", "v": "లాభం ₹120 Cr; రెవెన్యూ ₹418 Cr — CDMO/ఫార్మా సర్వీసెస్", "chip": "కొత్త లిస్టింగ్"},
   ]},
  "ఇంకా చాలా కంపెనీలు ఫలితాలు ఇచ్చాయి. నాలుగు ముఖ్యమైనవి చూద్దాం. [pause] "
  "మొదటిది — Sagility. హెల్త్‌కేర్ BPO కంపెనీ. రెవెన్యూ రెండు వేల ఇరవై నాలుగు కోట్లు, ఇరవై ఏడున్నర శాతం. లాభం డెబ్బై మూడున్నర శాతం పెరిగింది. [pause] "
  "రెండోది — NIIT. రెవెన్యూ పద్నాలుగు శాతం పెరిగింది, కానీ లాభం ఎనభై ఐదు శాతం దూసుకెళ్లింది — స్కిల్లింగ్, శిక్షణ డిమాండ్ ఊతంతో. [pause] "
  "మూడోది — IndiaMART. B2B ఆన్‌లైన్ మార్కెట్‌ప్లేస్. రెవెన్యూ నాలుగు వందల పద్నాలుగు కోట్లు, లాభం నూట డెబ్బై రెండు కోట్లు — పన్నెండు శాతం స్థిరమైన వృద్ధి. [pause] "
  "నాలుగోది — Anthem Biosciences. ఇటీవల లిస్ట్ అయిన ఫార్మా సర్వీసెస్ కంపెనీ. లాభం నూట ఇరవై కోట్లు, రెవెన్యూ నాలుగు వందల పద్దెనిమిది కోట్లు."),
 ("er_lesson", "sm_myths",
  {"kicker": "READ BEYOND THE HEADLINE", "title": "అంకెలు కనిపించినంత సులభం కాదు",
   "pairs": [
    {"m": "Bajaj Auto రెవెన్యూ +65% — అద్భుత వృద్ధి!", "f": "కాదు — ఇది కన్సాలిడేషన్ మార్పు వల్ల; అంకెలు గత ఏడాదితో పోల్చదగినవి కావు. ఆర్గానిక్ వృద్ధి చాలా తక్కువ"},
    {"m": "JSW ఇన్‌ఫ్రా లాభం −10% పడింది = చెడ్డ ఫలితం", "f": "లాభం ₹347 Cr — కానీ భవిష్యత్ వృద్ధి కోసం క్యాపెక్స్‌కు నిధులు మళ్లించడం, ఎక్కువ పన్ను వల్ల. డిమాండ్ సమస్య కాదు"},
    {"m": "QoQ (గత క్వార్టర్‌తో) పోలిస్తే సరిపోతుంది", "f": "సీజనాలిటీ వల్ల QoQ తప్పుదోవ పట్టిస్తుంది — YoY, అంటే గత ఏడాది ఇదే క్వార్టర్‌తో పోలికే సరైనది"},
   ]},
  "ఇక్కడ నేటి అతి ముఖ్యమైన పాఠం — అంకెలు ఎప్పుడూ కనిపించినంత సులభం కాదు. [pause] "
  "మొదటి అపోహ — Bajaj Auto రెవెన్యూ అరవై ఐదు శాతం పెరిగింది, అద్భుతం అని. కాదు. ఈ కంపెనీ ఒక విదేశీ సబ్సిడరీని తన ఖాతాల్లో కలుపుకుంది — దీన్నే కన్సాలిడేషన్ మార్పు అంటారు. అందుకే అంకెలు గత ఏడాదితో నేరుగా పోల్చడానికి కుదరదు. అసలు ఆర్గానిక్ వృద్ధి చాలా తక్కువ. [pause] "
  "రెండో అపోహ — JSW ఇన్‌ఫ్రా లాభం పది శాతం పడింది, అంటే చెడ్డ కంపెనీ అని. కాదు. లాభం పడటానికి కారణం — భవిష్యత్ వృద్ధి కోసం మిగులు నిధులను కొత్త ప్రాజెక్టుల నిర్మాణానికి మళ్లించడం, పన్ను ఎక్కువ కావడం. ఇది డిమాండ్ సమస్య కాదు, ఒక ఉద్దేశపూర్వక పెట్టుబడి. [pause] "
  "మూడో అపోహ — గత క్వార్టర్‌తో, అంటే QoQ, పోలిస్తే చాలు అని. కానీ చాలా వ్యాపారాలకు సీజన్ ప్రభావం ఉంటుంది — పండగలు, వేసవి. అందుకే గత ఏడాది ఇదే క్వార్టర్‌తో, అంటే YoY, పోల్చడమే సరైన విశ్లేషణ."),
 ("er_take", "sm_checklist",
  {"kicker": "HOW TO READ ANY RESULT", "title": "ఏ ఫలితాన్నైనా ఇలా చదవండి", "color": "#34D399", "icon": "💡",
   "items": [
    "4 అంకెలు: రెవెన్యూ, నికర లాభం, మార్జిన్, మేనేజ్‌మెంట్ గైడెన్స్",
    "ఎప్పుడూ YoY (గత ఏడాది ఇదే క్వార్టర్)తో పోల్చండి — QoQ కాదు",
    "హెడ్‌లైన్ % వెనుక ఒన్-టైమ్, కన్సాలిడేషన్ ఎఫెక్ట్ ఉందా చూడండి",
    "మంచి ఫలితమైనా అంచనాల కంటే తక్కువైతే షేర్ పడొచ్చు",
    "ఒక క్వార్టర్ కథ కాదు — ట్రెండ్, స్థిరత్వం ముఖ్యం",
   ]},
  "మరి ఏ ఫలితాన్నైనా ఎలా చదవాలి? ఐదు సూత్రాలు. [pause] "
  "ఒకటి — నాలుగు అంకెలు చూడండి: రెవెన్యూ, నికర లాభం, మార్జిన్, మేనేజ్‌మెంట్ గైడెన్స్. [pause] "
  "రెండు — ఎప్పుడూ గత ఏడాది ఇదే క్వార్టర్‌తో, అంటే YoY, పోల్చండి. గత క్వార్టర్‌తో కాదు. [pause] "
  "మూడు — హెడ్‌లైన్ శాతం వెనుక ఏదైనా ఒన్-టైమ్ లాభం, లేదా కన్సాలిడేషన్ మార్పు ఉందా గమనించండి — Bajaj Auto లాంటిది. [pause] "
  "నాలుగు — మంచి ఫలితం వచ్చినా, మార్కెట్ అంచనాల కంటే తక్కువైతే షేర్ పడొచ్చు. [pause] "
  "ఐదు — ఒక్క క్వార్టర్ మొత్తం కథ కాదు. కొన్ని క్వార్టర్ల ట్రెండ్, స్థిరత్వమే అసలు ముఖ్యం."),
 ("er_recap", "sm_recap",
  {"title": "నేటి ఫలితాలు — ఒక్క చూపులో",
   "items": [
    "బలమైనవి: TVS (+65%), M&M Fin (+75%), Bandhan (+35%)",
    "Bajaj Auto +46% — కానీ కన్సాలిడేషన్ ఎఫెక్ట్*",
    "మరిన్ని: Sagility +73.5%, NIIT +85%, IndiaMART +12%",
    "పడింది: JSW ఇన్‌ఫ్రా −10% (క్యాపెక్స్ కారణంగా)",
    "పాఠం: YoY చూడండి, హెడ్‌లైన్ వెనుక కథ చదవండి",
   ],
   "closer": "అంకెలు కాదు — వాటి వెనుక కథే అసలు విశ్లేషణ."},
  "నేటి ఫలితాలు ఒక్క చూపులో. [pause] "
  "బలమైనవి — TVS Motor అరవై ఐదు శాతం, M&M Financial డెబ్బై ఐదు శాతం, Bandhan Bank ముప్పై ఐదు శాతం. [pause] "
  "Bajaj Auto నలభై ఆరు శాతం పెరిగినా — అది కన్సాలిడేషన్ మార్పు వల్ల. [pause] "
  "మరిన్ని — Sagility డెబ్బై మూడున్నర, NIIT ఎనభై ఐదు, IndiaMART పన్నెండు శాతం. [pause] "
  "పడింది — JSW ఇన్‌ఫ్రా పది శాతం, కానీ క్యాపెక్స్ కారణంగా. [pause] "
  "పాఠం — ఎప్పుడూ YoY చూడండి, హెడ్‌లైన్ శాతం వెనుక ఉన్న అసలు కథను చదవండి. [pause] "
  "అంకెలు కాదు — వాటి వెనుక కథే అసలు విశ్లేషణ. [pause] "
  "ఈ సమాచారం బహిరంగ వార్తల నుండి సేకరించింది — విశ్లేషణ కోసం మాత్రమే, పెట్టుబడి సలహా కాదు. మీ నిర్ణయాలకు ముందు నిపుణుల సలహా తీసుకోండి. చూసినందుకు ధన్యవాదాలు."),
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
