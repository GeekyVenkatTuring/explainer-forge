#!/usr/bin/env python3
"""The Engineering Manager Behavioral Interview — Part 3: Change & Hard Calls.

Standalone follow-up. Reuses the `em` scene set; narration staged under public/em3.
Each question: a short coaching scene (em_q) + a ~2 min worked story (em_story).
Stories are illustrative, big-tech-scale model answers to adapt to your own.

Run:  python3 build.py    (Voicebox.app must be open)
"""
import json, os, subprocess, time, urllib.request

BASE = "http://127.0.0.1:17493"
PROFILE = "c488e05c-3407-46a3-874d-1b09b3aff78d"  # "TTS Bright (Nova)"
GAP = 0.5
PAUSE = 0.6
ATEMPO = 0.95
AUDIO = "em3"
ROOT = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(ROOT, "..", ".."))
PUBLIC = os.path.join(REPO, "composer", "public", AUDIO)
RAW = os.path.join(ROOT, "assets", "raw")
FIN = os.path.join(ROOT, "assets")
for d in (PUBLIC, RAW, os.path.join(ROOT, "artifacts"), os.path.join(ROOT, "renders")):
    os.makedirs(d, exist_ok=True)

YOU, SIT, RES, META, FLAG = "#F5A524", "#38BDF8", "#34D399", "#A78BFA", "#FB7185"


def Q(cat, title, q, color, moves, trap, signal, foot):
    return {"cat": cat, "title": title, "q": q, "color": color,
            "moves": [{"node": n, "title": t, "desc": d} for (n, t, d) in moves],
            "trap": trap, "signal": signal, "foot": foot}


def St(cat, title, color, situation, task, actions, metrics, learning, foot):
    return {"cat": cat, "title": title, "color": color, "situation": situation,
            "task": task, "actions": [{"d": a} for a in actions],
            "metrics": [{"v": v, "l": l} for (v, l) in metrics],
            "learning": learning, "foot": foot}


# ---------------------------------------------------------------- SCREENPLAY
SEGMENTS = [
 ("s01_title", "em_titlex",
  {"kicker": "ENGINEERING LEADERSHIP · PART THREE", "line1": "Leading Through",
   "line2": "Change & Hard Calls", "sub": "four more behavioral questions · with full worked answers · Senior EM"},
  "Welcome to part three. [pause] We've covered the classic questions, and how to "
  "operate and scale a team. Now, the hardest tier. Leading through change, through "
  "pressure, and through your own mistakes. [pause] Four more questions. Same format. "
  "The method, and then a full worked answer for each one."),

 ("s02_star", "em_star", {},
  "One more time, the spine, because it never changes. [pause] STAR. Situation, task, "
  "action, result. Plus L, for learning. [pause] Own your decisions with the word I. "
  "Keep the setup short. And live in the action. Let's begin."),

 # --- Q1 MANAGING UP / EXECS ---
 ("s03_execs", "em_q", Q(
   "INFLUENCE · MANAGING UP", "Managing a difficult executive",
   "How do you handle a demanding or skeptical executive?", SIT,
   [("S", "Understand their world", "What are they measured on, what are they afraid of? Map their incentives first."),
    ("A", "Lead with the headline", "Bottom line up front, then the detail. Execs buy the conclusion, then the data."),
    ("A", "Bring bad news early, with options", "Never surprise them. A risk plus two options beats a polished excuse."),
    ("L", "Build trust between fires", "Credibility is banked in the calm times and spent in the hard ones.")],
   "You either avoided them, or you caved on every push without pushing back.",
   "You manage upward with candor and structure — a trusted partner, not an order-taker.",
   "Execs don't want a yes-man or a wall. They want a clear-eyed partner who tells the truth."),
  "First question. How do you handle a demanding, or skeptical, executive? [pause] The "
  "trap is to go to one of two extremes. Either you avoid them, or you cave on every "
  "single push. Neither earns respect. [pause] Instead, first understand their world. "
  "What are they measured on? What are they afraid of? [pause] Then lead with the "
  "headline. Bottom line up front, then the detail. And bring bad news early, with "
  "options, never a surprise. [pause] And here's the secret. You build the trust in the "
  "calm times, so you have it to spend when things get hard."),

 ("s03s_execs", "em_story", St(
   "WORKED EXAMPLE · MANAGING UP", "Winning over the VP who didn't trust my team", SIT,
   "A new VP joined over my org and, frankly, didn't trust my platform team. He'd heard we were slow, and in our very first meeting he pushed to outsource half our roadmap to a vendor. It was existential.",
   "My mandate: change his mind — with evidence, not defensiveness.",
   ["Didn't get defensive — instead I asked what HE was measured on. It was cost, and delivery speed to the board.",
    "Led with his language — I came back with a one-page plan framed entirely in cost and speed, not in technology.",
    "Gave him early wins and honest bad news both — a fortnightly update he could take straight to the board.",
    "Proved it with a 90-day bet — I committed to a visible delivery milestone, and we hit it."],
   [("outsourcing", "shelved"), ("90 days", "to earn his trust"), ("+ headcount", "he later funded us")],
   "Managing up is translation — put your work in the language of what your exec is measured on.",
   "You turned a skeptic into a sponsor by speaking his metrics, not defending your turf."),
  "Here's the story. [pause] The situation. A new V P joined the company, over my whole "
  "org. And frankly, he did not trust my platform team. He'd been told, before he even "
  "met us, that we were slow and expensive. And in our very first one-on-one, he pushed "
  "hard to outsource half of our roadmap to an external vendor. For my team, this was "
  "existential. [pause] My mandate was to change his mind. But with evidence, not with "
  "defensiveness, because defensiveness would have just confirmed his fears. [pause] "
  "First, I did not get defensive, even though every instinct wanted to. Instead, I "
  "flipped it, and I asked him what he was measured on. And it was simple. Cost, and "
  "delivery speed, that he had to report up to the board. Now I understood his actual "
  "world. [pause] Second, I led with his language. I went away and came back, not with "
  "a technical defense of my team, but with a one-page plan framed entirely in his "
  "terms. Cost, and speed. I translated everything my team did into the two things he "
  "cared about. [pause] Third, I gave him both early wins and honest bad news. I set up "
  "a short, fortnightly update, written so cleanly that he could take it straight into "
  "his board meeting. When something slipped, he heard it from me first, with options. "
  "That's how you build trust with an executive. [pause] And fourth, I proved it with a "
  "bet. I committed, publicly, to a specific, visible delivery milestone in ninety "
  "days. And we hit it. [pause] The result. The outsourcing plan was shelved. It took "
  "about ninety days to fully earn his trust. And within the year, he was actually "
  "funding more headcount for the team he'd wanted to gut. [pause] What I learned. "
  "Managing up is really an act of translation. You put your work in the language of "
  "whatever your executive is measured on."),

 # --- Q2 DRIVING CHANGE ---
 ("s04_change", "em_q", Q(
   "CHANGE · DRIVING ADOPTION", "Driving a change nobody asked for",
   "Tell me about a time you drove a change against resistance.", RES,
   [("S", "Start with the why and the pain", "People resist change, not improvement. Anchor on a pain they already feel."),
    ("A", "Pilot, don't mandate", "Prove it with one willing team and real data before you roll it wide."),
    ("A", "Recruit champions", "Change spreads through respected peers, not top-down email decrees."),
    ("L", "Make the new way the easy way", "Bake it into tooling and defaults so it sticks after you look away.")],
   "You mandated it top-down, and it died the moment you stopped pushing.",
   "You drive durable change through influence and evidence, not authority.",
   "Lasting change is pulled by the org, not pushed by a mandate. Make the right way the easy way."),
  "Second question. Tell me about a time you drove a change against resistance. [pause] "
  "The trap is the top-down mandate. You decree it, and it dies the moment you stop "
  "pushing. [pause] Instead, start with the why, and a pain people already feel. People "
  "resist change, but they don't resist relief. [pause] Then pilot it with one willing "
  "team, prove it with data, and recruit a respected champion. Change spreads through "
  "peers, not decrees. [pause] And finally, make the new way the easy way. Bake it into "
  "the tooling, so it sticks after you look away."),

 ("s04s_change", "em_story", St(
   "WORKED EXAMPLE · DRIVING CHANGE", "Getting 200 engineers to actually write tests", RES,
   "Our org of about two hundred engineers had a testing-culture problem. Coverage was low, incidents were high, and two previous top-down “you must write tests” mandates had quietly failed.",
   "My mandate: actually change the testing culture, where two mandates had already died.",
   ["Started with the shared pain — I showed the data linking our worst outages to untested code. Nobody could argue with that.",
    "Piloted with one willing, respected team instead of mandating everyone — and made testing genuinely easy for them.",
    "Recruited that team's staff engineer as a visible champion — peers listen to peers, not to my slide deck.",
    "Made it the default — CI gates, test scaffolding, and templates, so the easy path was now the tested path."],
   [("22% → 78%", "coverage in 2 quarters"), ("↓ 60%", "test-escaped incidents"), ("bottom-up", "adopted, not forced")],
   "You don't mandate culture change. You make the right way the easy way, and let peers spread it.",
   "Two mandates failed; a pilot plus champions plus good defaults worked. That's how change sticks."),
  "Here's a concrete one. [pause] The situation. Our engineering org, about two hundred "
  "people, had a real testing-culture problem. Test coverage was low, production "
  "incidents were high, and the two of them were obviously connected. And here's the "
  "kicker. Two previous leaders had already tried a top-down, you must write tests "
  "mandate. Both had quietly failed. Everyone nodded, and nothing changed. [pause] So "
  "my mandate was to actually change the culture, in a place where mandates had already "
  "died twice. [pause] First, I started with the shared pain, not a rule. I pulled the "
  "data and showed, clearly, that our worst outages of the year traced directly back to "
  "untested code. People will argue with a policy, but nobody could argue with their "
  "own outages. [pause] Second, I did not mandate anything. I piloted it, with one "
  "willing, well-respected team. And I made testing genuinely easy for them, removing "
  "the friction, so they could actually succeed and become proof. [pause] Third, I "
  "recruited that team's staff engineer as a visible champion. Because engineers listen "
  "to a respected peer showing real results. They do not listen to a manager's slide "
  "deck about quality. [pause] And fourth, I made the new way the easy way. We built it "
  "into the system. Continuous-integration gates, automatic test scaffolding, and "
  "templates. So the path of least resistance was now the tested path. [pause] The "
  "result. Coverage went from twenty-two percent to seventy-eight percent in two "
  "quarters. Test-escaped incidents dropped sixty percent. And because it was adopted "
  "bottom-up, it stuck, long after I'd moved on. [pause] What I learned. You do not "
  "mandate a culture change. You make the right way the easy way, and you let respected "
  "peers spread it for you."),

 # --- Q3 A WRONG TECHNICAL CALL ---
 ("s05_wrongcall", "em_q", Q(
   "JUDGMENT · A WRONG CALL", "A technical decision you got wrong",
   "Tell me about a technical decision you made that was wrong.", META,
   [("S", "Pick a real, owned call", "A decision that was clearly yours, with real consequences — not a team mistake."),
    ("A", "Own the blast radius", "State honestly what it cost — time, money, reliability. No minimizing."),
    ("A", "Course-correct decisively", "How you caught it, admitted it, and changed direction without ego."),
    ("L", "Extract the principle", "The engineering judgment you now apply because of it.")],
   "You blamed the requirements, the vendor, or “unknowable” circumstances.",
   "You have technical judgment AND the humility to reverse your own bad call fast.",
   "Senior engineers are judged by how fast they kill their own bad ideas, not by never having them."),
  "Third question. Tell me about a technical decision you made that was wrong. [pause] "
  "The trap is to secretly not answer it. To blame the requirements, or a vendor, or "
  "some unknowable circumstance. They see right through that. [pause] Instead, pick a "
  "real call that was clearly yours. Own the blast radius honestly. What did it cost? "
  "[pause] Then show how you caught it, admitted it, and course-corrected without ego. "
  "[pause] And extract the principle you now operate by. Because senior engineers are "
  "judged by how fast they kill their own bad ideas. Not by never having them."),

 ("s05s_wrongcall", "em_story", St(
   "WORKED EXAMPLE · A WRONG CALL", "The microservices migration I pushed too early", META,
   "As a newly-promoted senior EM, I pushed hard to break our monolith into microservices. It was the fashionable move, and I championed it. But we were a 15-person team with none of the platform maturity to run twenty services.",
   "The honest version: I owned this call, and it started actively hurting the team.",
   ["Owned the blast radius honestly — velocity dropped, on-call exploded, and a one-line feature now touched five services.",
    "Caught it fast and said it out loud — in a team meeting, I admitted the call was premature. That reset trust.",
    "Course-corrected without ego — we consolidated back to a few well-bounded services, keeping only the splits that earned their keep.",
    "Changed how I decide — I now require the operational maturity to exist BEFORE adopting a pattern, not after."],
   [("20 → 5", "services, consolidated"), ("velocity", "recovered in a quarter"), ("a rule", "maturity before pattern")],
   "Adopt architecture for your real scale and maturity, not for the blog posts — and kill bad calls fast.",
   "You owned it, reversed it fast, and turned it into judgment. That's exactly the answer they want."),
  "Here's a real one, and it's a little embarrassing, which is the point. [pause] The "
  "situation. I had just been promoted to senior manager, and I was eager to make my "
  "mark. And I pushed, hard, to break our monolith into microservices. It was the "
  "fashionable architecture at the time, every conference talk was about it, and I "
  "championed it loudly. The problem? We were a fifteen-person team, with none of the "
  "platform maturity, the tooling, the observability, to actually run twenty separate "
  "services. [pause] So let me be honest. This was my call. I drove it. And it started "
  "actively hurting the team. [pause] First, let me own the blast radius, because "
  "minimizing it would defeat the purpose. Our velocity dropped, badly. Our on-call "
  "load exploded, because now there were twenty things to page on. And a change that "
  "used to be one line in the monolith now had to be coordinated across five different "
  "services. We had made everything harder. [pause] Second, I caught it fast, and "
  "critically, I said it out loud. In a team meeting, I stood up and admitted that my "
  "decision had been premature, and that I'd gotten it wrong. And you know what? That "
  "actually reset the team's trust in me, rather than losing it. [pause] Third, I "
  "course-corrected without ego. This is hard, because it meant undoing my own idea. We "
  "consolidated back down to a handful of well-bounded services, and we only kept the "
  "splits that genuinely earned their keep. [pause] And fourth, I changed how I make "
  "these decisions permanently. I now require that the operational maturity for a "
  "pattern exists before we adopt it, not as a thing we'll figure out later. [pause] "
  "The result. We went from twenty services back down to five. Velocity recovered "
  "within a quarter. And I walked away with a hard rule I still use. [pause] What I "
  "learned. Adopt architecture for your actual scale and maturity, not for the blog "
  "posts. And when you get it wrong, kill your own bad call fast."),

 # --- Q4 RE-ORG / LAYOFF ---
 ("s06_layoff", "em_q", Q(
   "LEADERSHIP · HARD TIMES", "Leading through a re-org or layoff",
   "How did you lead your team through a layoff or re-org?", YOU,
   [("S", "Absorb, then lead", "Process your own reaction privately first. The team needs you steady, not raw."),
    ("A", "Be honest and human", "Say what you know, admit what you don't, never spin. Trust is the only currency left."),
    ("A", "Protect and re-anchor the team", "Fight for your people behind closed doors; give the survivors clarity fast."),
    ("L", "Rebuild momentum deliberately", "Survivor guilt and fear are real. Re-establish direction and small wins quickly.")],
   "You went silent, hid behind an HR script, or pretended everything was fine.",
   "You lead with honesty and humanity under pressure, and hold the team together after.",
   "In a layoff, your team remembers exactly how you treated people. That memory outlives the re-org."),
  "The last question, and the heaviest. How did you lead your team through a layoff, or "
  "a re-org? [pause] The trap is to go silent, hide behind an H R script, or pretend "
  "everything is fine. The team sees through all of it. [pause] Instead, absorb your "
  "own reaction privately first. Then be honest and human. Say what you know, admit "
  "what you don't. [pause] Protect your people behind closed doors, and re-anchor the "
  "survivors with clarity, fast. [pause] Because in a moment like that, your team "
  "remembers exactly how you treated people. And that memory long outlives the re-org."),

 ("s06s_layoff", "em_story", St(
   "WORKED EXAMPLE · HARD TIMES", "Holding the team together through a 20% cut", YOU,
   "During a downturn, I was told the company was cutting twenty percent. I had to lose two people from my team of ten, deliver that news myself, and then keep the shaken survivors together.",
   "My mandate: handle the cut with humanity, and rebuild the team that remained.",
   ["Absorbed it privately first — I was angry and sad, but the team needed me steady, so I processed it before facing them.",
    "Fought for my people behind closed doors — I couldn't change the number, but I influenced the who, and secured strong severance and references.",
    "Told the truth, humanely — I delivered the news directly and in person, took the hard questions, and never hid behind a script.",
    "Re-anchored the survivors fast — within a week: honest one-on-ones, a reset on priorities, and a clear, lighter mission."],
   [("2 exits", "handled with dignity"), ("0", "further attrition"), ("re-focused", "in one week")],
   "In hard times, people don't remember the strategy. They remember whether you were honest and humane.",
   "You carried the hard news like a leader, and rebuilt trust after. That's the truest test of one."),
  "This is the heaviest story, and it's about a layoff. [pause] The situation. During a "
  "downturn, I was told, in confidence, that the company was cutting twenty percent of "
  "staff. For my team, that meant I had to lose two people out of ten. I had to help "
  "choose, deliver the news myself, and then hold the shaken survivors together "
  "afterward. [pause] My mandate was to handle the cut with as much humanity as "
  "possible, and then rebuild the team that remained. [pause] First, I absorbed it "
  "privately. Honestly, I was angry, and I was sad. But I knew the team needed me "
  "steady, not raw and venting. So I processed my own reaction, with my own manager and "
  "at home, before I ever faced the team. [pause] Second, I fought for my people behind "
  "closed doors. I could not change the number, twenty percent was fixed. But I could "
  "influence the how, and the who. And I fought hard to secure strong severance, "
  "extended benefits, and personal references for the two people leaving. [pause] "
  "Third, when it came time, I told the truth, humanely. I delivered the news directly, "
  "in person, one-on-one. I did not hide behind an H R script. I sat in the discomfort "
  "with them, and I took every hard question honestly. [pause] And fourth, I "
  "re-anchored the survivors, fast, because survivor guilt and fear are absolutely "
  "real. Within a week, I did honest one-on-ones with everyone left, I reset our "
  "priorities to match the smaller team, and I gave them a clear, lighter, achievable "
  "mission. [pause] The result. The two exits were handled with genuine dignity. We had "
  "zero further attrition, nobody else fled in fear. And the team was re-focused and "
  "moving again within a week. [pause] What I learned. In hard times, people do not "
  "remember your strategy. They remember whether you were honest, and whether you were "
  "humane."),

 # --- RECAP ---
 ("s07_recap", "em_recap",
  {"items": [
     "Manage up by speaking your exec's metrics, not your tech.",
     "Drive change with pilots and champions, never mandates.",
     "Own a wrong call fast, and turn it into judgment.",
     "In a layoff, lead with honesty and humanity above all.",
     "Same spine every time: STAR, plus what you learned.",
   ],
   "closer": "The hardest moments are where they find out who you really are as a leader."},
  "Let's recap part three. [pause] When you manage up, translate your work into the "
  "metrics your executive is judged on. Drive change with pilots and champions, not "
  "mandates. When you make a wrong call, own it fast, and turn it into judgment. "
  "[pause] And in the hardest moments, a layoff, a crisis, lead with honesty and "
  "humanity above everything else. [pause] Same spine every time. STAR, plus the "
  "learning. Take these, and make them your own. [pause] Because the hardest moments "
  "are exactly where they find out who you really are as a leader. Thanks for watching."),
]


def post(p, b):
    req = urllib.request.Request(BASE + p, data=json.dumps(b).encode(),
                                 headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode())


def get(p):
    with urllib.request.urlopen(BASE + p, timeout=30) as r:
        return r.read()


def tts_chunk(path, text):
    gid = post("/generate", {"profile_id": PROFILE, "text": text, "engine": "kokoro"})["id"]
    for _ in range(300):
        raw = get(f"/generate/{gid}/status").decode()
        line = [l for l in raw.splitlines() if l.startswith("data:")]
        st = json.loads(line[-1][5:].strip()) if line else None
        if st and st.get("status") == "completed":
            break
        time.sleep(1)
    open(path, "wb").write(get(f"/audio/{gid}"))


def gen_one(seg_id, text):
    fin = os.path.join(FIN, seg_id + ".wav")
    if os.path.exists(fin):
        out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                              "-of", "default=noprint_wrappers=1:nokey=1", fin],
                             capture_output=True, text=True, check=True)
        return fin, round(float(out.stdout.strip()), 3)
    chunks = [c.strip() for c in text.split("[pause]") if c.strip()]
    paths = []
    for ci, chunk in enumerate(chunks):
        cp = os.path.join(RAW, f"{seg_id}_c{ci}.wav")
        if not os.path.exists(cp):
            tts_chunk(cp, chunk)
        paths.append(cp)
    psil = os.path.join(RAW, "_pause.wav")
    if not os.path.exists(psil):
        subprocess.run(["ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=24000:cl=mono",
                        "-t", str(PAUSE), psil], check=True, capture_output=True)
    clist = os.path.join(RAW, f"{seg_id}_concat.txt")
    with open(clist, "w") as f:
        for i2, p2 in enumerate(paths):
            f.write(f"file '{p2}'\n")
            if i2 < len(paths) - 1:
                f.write(f"file '{psil}'\n")
    af = f"atempo={ATEMPO}" if ATEMPO != 1.0 else "anull"
    subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", clist,
                    "-filter:a", af, fin], check=True, capture_output=True)
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "default=noprint_wrappers=1:nokey=1", fin],
                         capture_output=True, text=True, check=True)
    return fin, round(float(out.stdout.strip()), 3)


manifest = []
for sid, variant, props, text in SEGMENTS:
    path, dur = gen_one(sid, text)
    manifest.append({"id": sid, "variant": variant, "props": props, "wav": path, "duration": dur})
    print(f"  {sid:16s} {dur:6.2f}s", flush=True)

silence = os.path.join(FIN, "_sil.wav")
subprocess.run(["ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=24000:cl=mono", "-t", str(GAP), silence],
               check=True, capture_output=True)
concat_list = os.path.join(ROOT, "concat.txt")
with open(concat_list, "w") as f:
    for i, m in enumerate(manifest):
        f.write(f"file '{m['wav']}'\n")
        if i < len(manifest) - 1:
            f.write(f"file '{silence}'\n")
subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_list, "-c", "copy",
                os.path.join(PUBLIC, "narration.wav")], check=True, capture_output=True)

cuts, t = [], 0.0
for m in manifest:
    start, end = t, t + m["duration"]
    cuts.append({"id": m["id"], "type": m["variant"], "in_seconds": round(start, 3),
                 "out_seconds": round(end, 3),
                 "props": {**m["props"], "dur": round(m["duration"] + GAP, 3)}})
    t = end + GAP
props = {"cuts": cuts,
         "audio": {"narration": {"src": f"{AUDIO}/narration.wav", "volume": 1.0}}}
json.dump(props, open(os.path.join(ROOT, "artifacts", "edit_decisions.json"), "w"), indent=2)
words = sum(len(x[3].replace("[pause]", "").split()) for x in SEGMENTS)
print(f"total {t - GAP:.2f}s ({(t-GAP)/60:.2f} min), {len(cuts)} scenes, {words} words, NO captions, NO music")
