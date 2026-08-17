#!/usr/bin/env python3
"""The Engineering Manager Behavioral Interview — Part 4: Culture & The Long Game.

Standalone follow-up. Reuses the `em` scene set; narration staged under public/em4.
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
AUDIO = "em4"
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
  {"kicker": "ENGINEERING LEADERSHIP · PART FOUR", "line1": "Culture &",
   "line2": "The Long Game", "sub": "four more behavioral questions · with full worked answers · Senior EM"},
  "Welcome to part four. The final set. [pause] These are the questions about the long "
  "game. Building culture, protecting your people, and setting direction across an "
  "entire org. [pause] The systemic work that quietly defines a senior leader. Four "
  "questions, same format as always."),

 ("s02_star", "em_star", {},
  "One last time through the spine. [pause] STAR. Situation, task, action, result. Plus "
  "L, for learning. [pause] Own your decisions with the word I. Keep the setup tight. "
  "And live in the action. Here we go."),

 # --- Q1 REMOTE / DISTRIBUTED ---
 ("s03_remote", "em_q", Q(
   "TEAMS · DISTRIBUTED", "Leading a remote or distributed team",
   "How do you lead a remote or globally distributed team?", SIT,
   [("S", "Default to written and async", "Docs and clear decisions over meetings. Timezone-fair, not meeting-heavy."),
    ("A", "Engineer connection on purpose", "Trust doesn't happen by accident remotely. Create the moments deliberately."),
    ("A", "Measure outcomes, not presence", "Judge output and impact, never hours online or the green dot."),
    ("L", "Over-communicate context", "Remote teams starve on missing context. You feed it relentlessly.")],
   "You recreated the office online — back-to-back calls across incompatible timezones.",
   "You build trust and clarity across distance, and treat async as a feature, not a compromise.",
   "Remote leadership is a discipline: written clarity, deliberate connection, outcomes over optics."),
  "First question. How do you lead a remote, or globally distributed, team? [pause] The "
  "trap is to just recreate the office online. Back-to-back video calls across "
  "timezones that don't overlap. That burns everyone out. [pause] Instead, default to "
  "written and async. Decisions in docs, not in meetings. [pause] Engineer connection "
  "on purpose, because trust doesn't happen by accident over video. Measure outcomes, "
  "not presence. Never the green dot. [pause] And over-communicate context, because "
  "remote teams starve on the context that used to travel by hallway."),

 ("s03s_remote", "em_story", St(
   "WORKED EXAMPLE · DISTRIBUTED", "Building one team across three continents", SIT,
   "I inherited a team split across San Francisco, London, and Bangalore — a fourteen-hour spread. In reality it was three sub-teams that didn't trust each other; meetings excluded someone by design, and context lived in people's heads.",
   "My mandate: turn three timezones into one team, without burning anyone out on 2am calls.",
   ["Moved decisions to writing — every significant decision landed in a doc, so nobody was excluded by their timezone.",
    "Rotated the pain fairly — the one necessary sync meeting rotated its awkward hour, so it wasn't always Bangalore's midnight.",
    "Engineered connection deliberately — regional leads, cross-site pairing, and real budget for periodic in-person weeks.",
    "Judged outcomes, not presence — I killed the green-dot culture and measured shipped impact instead."],
   [("3 silos → 1", "one real team"), ("async-first", "decisions in docs"), ("↑ trust", "cross-site pairing")],
   "Distributed teams run on written clarity and deliberate trust, not on more meetings.",
   "You made distance a design constraint you solved, not an excuse. That's modern EM leadership."),
  "Here's the story. [pause] The situation. I inherited a team that was split across "
  "three sites. San Francisco, London, and Bangalore. A fourteen-hour spread from one "
  "end to the other. And on paper it was one team, but in reality it was three "
  "sub-teams that didn't trust each other. Meetings, by their very timing, always "
  "excluded someone. And critical context lived in people's heads in one office, and "
  "never made it to the others. [pause] My mandate was to turn three timezones into one "
  "actual team. And to do it without burning people out on two a m calls. [pause] "
  "First, I moved decisions to writing. Every significant decision now had to land in a "
  "document, with the reasoning. That single change meant nobody was excluded from a "
  "decision just because they were asleep when it was made. [pause] Second, I rotated "
  "the pain fairly. There was one genuinely necessary all-hands sync each week, and "
  "instead of it always being convenient for San Francisco and brutal for Bangalore, we "
  "rotated the awkward hour, so everyone shared the load. [pause] Third, I engineered "
  "connection on purpose, because trust does not form by accident over a video call. I "
  "set up regional leads, I paired engineers across sites on projects, and I fought for "
  "real budget to fly the team together in person a couple of times a year. [pause] And "
  "fourth, I judged outcomes, not presence. I explicitly killed the green-dot culture, "
  "where people felt they had to look online. I measured what shipped, and the impact "
  "it had. [pause] The result. Over a few months, three silos genuinely became one "
  "team. Decisions were async-first, and written down. And trust rose sharply, "
  "especially between the engineers who'd paired across sites. [pause] What I learned. "
  "Distributed teams run on written clarity and deliberate trust. Not on more "
  "meetings."),

 # --- Q2 DEI / INCLUSION ---
 ("s04_dei", "em_q", Q(
   "CULTURE · INCLUSION", "Building an inclusive team in practice",
   "What have you actually done to build a diverse, inclusive team?", META,
   [("S", "Move past slogans to actions", "Talk about what you changed in hiring and daily practice, not your values."),
    ("A", "Fix the system, not the people", "Structured interviews, diverse panels, wider sourcing — take bias out of the process."),
    ("A", "Make inclusion a daily practice", "Airtime in meetings, credit attribution, equitable stretch work and on-call."),
    ("L", "Hold yourself to data", "Track representation, promotion rates, and who gets the good projects.")],
   "You gave a values speech with no concrete action or measurement behind it.",
   "You treat inclusion as an operational discipline with real interventions and metrics.",
   "Inclusion isn't a poster. It's who you hire, who speaks, who gets the growth work, and who gets promoted."),
  "Second question. What have you actually done to build a diverse and inclusive team? "
  "[pause] The trap is the values speech. Lots of belief, zero concrete action. That "
  "impresses no one. [pause] Instead, talk about what you changed in the system. "
  "Structured interviews, diverse panels, wider sourcing, to take bias out of the "
  "process. [pause] Make inclusion a daily practice. Who gets airtime, who gets credit, "
  "who gets the growth work. [pause] And hold yourself to data. Representation, "
  "promotion rates, and who actually gets the good projects."),

 ("s04s_dei", "em_story", St(
   "WORKED EXAMPLE · INCLUSION", "The team where only some voices got heard", META,
   "I took over a team that, on paper, looked fairly diverse. But the same three senior men made every real decision, and our quieter engineers and women were leaving faster than anyone else.",
   "My mandate: turn nominal diversity into real inclusion, and stop the lopsided attrition.",
   ["Looked at the data first — the growth projects and the promotions were all going to the same few people.",
    "Changed the meeting mechanics — round-robin input, written proposals before discussion, and I attributed ideas to their real authors.",
    "Redistributed the good work — rotated high-visibility projects and on-call, so growth wasn't reserved for the loudest.",
    "Fixed hiring too — diverse interview panels and a structured rubric, so the funnel genuinely widened."],
   [("attrition gap", "closed"), ("+3 promotions", "from underrepresented groups"), ("who decides", "widened")],
   "Diversity is who's in the room. Inclusion is who actually gets heard, grown, and promoted.",
   "You made inclusion measurable and operational, not a slogan. That's what interviewers respect."),
  "Here's a concrete story. [pause] The situation. I took over a team that, on paper, "
  "looked reasonably diverse. The headcount numbers were fine. But when you watched how "
  "it actually worked, the same three senior men made every real decision. And our "
  "quieter engineers, and the women on the team, were leaving noticeably faster than "
  "anyone else. So we had diversity on paper, but not inclusion in practice. [pause] My "
  "mandate was to turn that nominal diversity into real inclusion, and to stop the "
  "lopsided attrition. [pause] First, I looked at the data before doing anything. And "
  "the pattern was stark. The growth projects and the promotions were all flowing to "
  "the same handful of people. Everyone else was stuck. [pause] Second, I changed the "
  "mechanics of how we met and decided. I introduced round-robin input, so everyone was "
  "actually asked. I had people write proposals before we discussed them, so the loudest "
  "voice didn't dominate. And I made a point of attributing ideas to the person who "
  "actually had them, because credit had been quietly getting reassigned. [pause] "
  "Third, I redistributed the good work. I rotated the high-visibility projects and the "
  "on-call, so that the opportunities to grow and be seen weren't permanently reserved "
  "for the same few. [pause] And fourth, I fixed the top of the funnel too. Diverse "
  "interview panels, and a structured rubric, so our hiring genuinely widened instead "
  "of cloning the existing team. [pause] The result. Within a year, the attrition gap "
  "had closed. We had three promotions from underrepresented groups, people who'd been "
  "stuck. And the set of people who actually made decisions was much wider. [pause] "
  "What I learned. Diversity is who is in the room. Inclusion is who actually gets "
  "heard, grown, and promoted. And only the second one is your real job."),

 # --- Q3 ON-CALL / RELIABILITY CULTURE ---
 ("s05_reliability", "em_q", Q(
   "OPERATIONS · RELIABILITY", "Building a healthy on-call & reliability culture",
   "How do you build a sustainable on-call and reliability culture?", RES,
   [("S", "Treat toil as a bug", "A brutal on-call is a systems failure, not a rite of passage. Own it."),
    ("A", "Make reliability visible and funded", "SLOs and error budgets, with real time allocated to pay down toil."),
    ("A", "Blameless by default", "Postmortems find system fixes, not scapegoats — or people stop reporting."),
    ("L", "Protect the humans", "Fair rotation, comp for pages, hard caps. Burnout is a reliability risk too.")],
   "You treated a painful on-call as normal, and let your best people burn out on it.",
   "You build reliability as a system and a culture, and you protect the people running it.",
   "Reliability is a culture: SLOs, blameless learning, and humane rotations — not heroics."),
  "Third question. How do you build a sustainable on-call, and reliability, culture? "
  "[pause] The trap is treating a brutal on-call as a rite of passage, and letting your "
  "best people burn out on it. [pause] Instead, treat the toil as a bug, a systems "
  "failure you own. Make reliability visible and funded, with S L Os and error budgets. "
  "[pause] Keep postmortems blameless, or people simply stop reporting problems. [pause] "
  "And protect the humans. Fair rotation, and hard caps. Because burnout is a "
  "reliability risk, just like bad code is."),

 ("s05s_reliability", "em_story", St(
   "WORKED EXAMPLE · RELIABILITY", "The on-call rotation that was burning people out", RES,
   "I took over a team with a brutal on-call. Engineers were getting paged around twenty times a week, mostly for noise. Two people had already quit citing burnout, and everyone dreaded their week on rotation.",
   "My mandate: make on-call sustainable, without letting reliability actually get worse.",
   ["Treated the toil as a bug — I had the team spend twenty percent of every sprint killing the top sources of alerts.",
    "Made reliability visible — introduced SLOs and an error budget, so reliability work got real, funded priority.",
    "Went fully blameless — rewrote postmortems to hunt system fixes, never people, so incidents got surfaced, not hidden.",
    "Protected the humans — fair rotation, follow-the-sun where possible, and a hard rule: a bad night earns the next day off."],
   [("20 → 3", "pages per week"), ("99.95%", "reliability, and rising"), ("0", "burnout attrition since")],
   "A painful on-call is a systems failure. Fix the toil, fund reliability, and protect the people.",
   "You turned a burnout machine into a healthy system. That's operational leadership, not heroics."),
  "Here's how that looks in practice. [pause] The situation. I took over a team with a "
  "genuinely brutal on-call. Engineers were getting paged around twenty times a week, "
  "and most of it was noise. False alarms, flapping alerts. Two good people had already "
  "quit, explicitly citing burnout. And everyone on the team quietly dreaded the week "
  "their rotation came up. [pause] My mandate was to make on-call sustainable. But "
  "critically, without letting the actual reliability get any worse in the process. "
  "[pause] First, I reframed the whole thing. I told the team that this level of toil "
  "was not normal, and it was not a rite of passage. It was a bug in our system. So we "
  "treated it like one, and spent twenty percent of every sprint hunting down and "
  "killing the top sources of alerts. [pause] Second, I made reliability visible and "
  "funded. I introduced S L Os, service level objectives, and an error budget. That "
  "turned reliability from an invisible chore into a real, prioritized, funded piece of "
  "work that leadership could see. [pause] Third, I made our postmortems completely "
  "blameless. I rewrote how we did them, so they hunted for system fixes, never for a "
  "person to blame. Because the moment people fear blame, they stop reporting the near "
  "misses, and you go blind. [pause] And fourth, I protected the humans directly. Fair "
  "rotation, follow-the-sun coverage where we could, compensation for being on call, "
  "and a hard rule that if you got paged through the night, you took the next day off, "
  "no questions. [pause] The result. Pages dropped from about twenty a week to three. "
  "Reliability actually improved, to about ninety-nine point nine five percent and "
  "climbing. And we had zero burnout attrition after that. [pause] What I learned. A "
  "painful on-call is a systems failure. You fix the toil, you fund reliability, and "
  "you protect the people running it."),

 # --- Q4 CROSS-ORG STRATEGY ---
 ("s06_strategy", "em_q", Q(
   "STRATEGY · CROSS-ORG", "Setting technical strategy across teams",
   "Tell me about a time you set technical strategy beyond your team.", YOU,
   [("S", "Start from the business goal", "Strategy connects tech investment to where the business is going, not to a favorite rewrite."),
    ("A", "Get the org bought in", "Write it down, socialize it, and let stakeholders shape it so they own it."),
    ("A", "Sequence bets, and say no", "A roadmap is mostly what you WON'T do. Make the trade-offs explicit."),
    ("L", "Make it real and measurable", "Tie it to milestones and metrics, and revisit it. A static strategy is a wish.")],
   "You proposed a grand rewrite with no link to business value and no buy-in.",
   "You think in bets and trade-offs at the org level, and can align people behind a direction.",
   "A technical strategy is funded bets tied to business outcomes — and the things you chose NOT to do."),
  "The final question, and the most senior. Tell me about a time you set technical "
  "strategy beyond your own team. [pause] The trap is to propose a grand rewrite, with "
  "no link to business value and no buy-in. That's an architecture opinion, not a "
  "strategy. [pause] Instead, start from the business goal. Then get the org bought in, "
  "by writing it down and letting people shape it. [pause] Sequence your bets, and be "
  "explicit about what you won't do. And make it measurable, with milestones. Because a "
  "strategy you never revisit is just a wish."),

 ("s06s_strategy", "em_story", St(
   "WORKED EXAMPLE · CROSS-ORG", "A three-year platform strategy nobody had written", YOU,
   "Across our engineering org of eighty people, every team was independently reinventing infrastructure — auth, data pipelines, deploy tooling. There was no shared platform strategy, and it was quietly costing us a fortune in duplicated effort and incidents.",
   "My mandate — I raised my hand for it: write and drive a shared platform strategy for the whole org.",
   ["Started from the business goal — I tied the strategy to shipping faster and cheaper, not to elegant architecture.",
    "Built it WITH the org, not for it — interviewed every team lead, wrote a one-page strategy, and let them shape it so they'd own it.",
    "Made it a sequence of bets — I named what we'd build, what we'd buy, and what we'd deliberately NOT do, staged over three phases.",
    "Made it measurable — every bet had a milestone and a metric, and we revisited the whole strategy each quarter."],
   [("8 teams", "aligned on one platform"), ("↓ 40%", "infrastructure duplication"), ("3-yr roadmap", "with quarterly reviews")],
   "Strategy is funded bets tied to business outcomes — and the courage to write down what you won't do.",
   "You aligned a whole org behind a direction and made the trade-offs explicit. The senior-EM ceiling."),
  "And the last story, which is the most senior-level one. [pause] The situation. "
  "Across our engineering org, about eighty people, every single team was independently "
  "reinventing the same infrastructure. Their own authentication, their own data "
  "pipelines, their own deploy tooling. There was no shared platform strategy at all. "
  "And it was quietly costing us a fortune, in duplicated effort, and in incidents from "
  "everyone maintaining their own fragile version of everything. [pause] Nobody owned "
  "fixing it, so I raised my hand. My self-assigned mandate was to write, and then "
  "actually drive, a shared platform strategy for the entire org. [pause] First, I "
  "started from the business goal, not from architecture. I tied the whole strategy to "
  "one thing leadership cared about. Shipping faster, and cheaper. I did not lead with "
  "elegant design, because nobody funds elegance. [pause] Second, I built it with the "
  "org, not for it. This is the part that makes or breaks cross-team strategy. I "
  "interviewed every team lead, I wrote a single one-page strategy, and I let them "
  "genuinely shape it, so that it became their strategy, not a mandate I was imposing. "
  "[pause] Third, I made it a clear sequence of bets. I was explicit about what we'd "
  "build ourselves, what we'd buy off the shelf, and, most importantly, what we would "
  "deliberately not do. And I staged it over three phases, so it wasn't a boil-the-ocean "
  "fantasy. [pause] And fourth, I made it measurable and alive. Every bet had a "
  "milestone and a metric, and we revisited the whole strategy every quarter, and "
  "adjusted. [pause] The result. Eight teams aligned onto one shared platform. "
  "Infrastructure duplication dropped forty percent. And we had a real, living, "
  "three-year roadmap with quarterly reviews. [pause] What I learned. Strategy is a set "
  "of funded bets, tied to business outcomes. And it takes the courage to write down, "
  "clearly, what you will not do."),

 # --- RECAP ---
 ("s07_recap", "em_recap",
  {"items": [
     "Lead remote teams with written clarity and deliberate trust.",
     "Make inclusion operational: who's heard, grown, and promoted.",
     "Build reliability as a culture, and protect your on-call people.",
     "Strategy is funded bets tied to business outcomes.",
     "Across all four parts: STAR, plus what you learned.",
   ],
   "closer": "Great managers build systems and cultures that outlast them."},
  "Let's recap part four, and the whole series. [pause] Lead distributed teams with "
  "written clarity and deliberate trust. Make inclusion operational. It's who gets "
  "heard, grown, and promoted. Build reliability as a culture, and protect the people "
  "running it. And treat strategy as funded bets tied to business outcomes, including "
  "what you choose not to do. [pause] Across all four parts, it's been the same spine. "
  "STAR, plus the learning. Own your decisions, and end on what you learned. [pause] "
  "That's twenty-five situations, and really one idea. Great managers build systems and "
  "cultures that outlast them. [pause] Now, go make these stories your own. Good luck, "
  "and thanks for watching."),
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
