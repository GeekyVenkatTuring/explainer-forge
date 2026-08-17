#!/usr/bin/env python3
"""The Engineering Manager Behavioral Interview — Part 2: Operating & Scaling.

A standalone follow-up to em-behavioral. Reuses the `em` scene set (EMScenes.tsx),
but stages its narration under public/em2 so it never clobbers video one.
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
AUDIO = "em2"                                     # audio folder (variants stay em_*)
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
  {"kicker": "ENGINEERING LEADERSHIP · PART TWO", "line1": "Operating &",
   "line2": "Scaling a Team", "sub": "four more behavioral questions · with full worked answers · Senior EM"},
  "Welcome back. This is part two. [pause] The first video covered the classic "
  "behavioral questions. Now we go up a level. Four questions about operating and "
  "scaling a team. The ones that separate a manager from a senior one. [pause] Same "
  "format as before. The method, and then a full example answer for each."),

 ("s02_star", "em_star", {},
  "Quick refresher on the spine, because it still applies to every answer. [pause] "
  "STAR. Situation, task, action, result. Plus L, for learning. [pause] Own your "
  "decisions with the word I. Keep the setup short. And spend most of your time on the "
  "action. Now, let's get into it."),

 # --- Q1 MEASURING PERFORMANCE ---
 ("s03_measure", "em_q", Q(
   "OPERATING · METRICS", "Measuring team performance",
   "How do you measure your team's performance?", RES,
   [("S", "Reject vanity metrics", "Velocity and lines of code measure motion, not impact. Don't lead with them."),
    ("A", "Measure outcomes", "Tie the team to business and user outcomes — did the work move the needle?"),
    ("A", "Track delivery health", "The DORA metrics: deploy frequency, lead time, change-fail rate, time to restore."),
    ("L", "Watch the humans", "Retention, on-call load, and eNPS. Hitting numbers while burning out is failing.")],
   "“We track story points and velocity.” That rewards busywork, not value.",
   "You manage outcomes and team health, not activity theater.",
   "Great managers measure whether the work mattered — and whether the team can keep doing it."),
  "First question. How do you measure your team's performance? [pause] The trap is to "
  "reach for vanity metrics. Story points, velocity, lines of code. They measure "
  "motion, not impact. [pause] Instead, measure outcomes. Did the work actually move a "
  "business or user metric? [pause] Then track delivery health, with the DORA metrics. "
  "Deploy frequency, lead time, change-fail rate, and time to restore. [pause] And "
  "always watch the humans. Retention, on-call load, and morale. A team hitting its "
  "numbers while burning out is not a high-performing team."),

 ("s03s_measure", "em_story", St(
   "WORKED EXAMPLE · METRICS", "When the velocity chart lied", RES,
   "I inherited a team whose velocity chart looked fantastic — story points up and to the right. But leadership was frustrated, features weren't really landing, and two engineers were quietly interviewing elsewhere.",
   "My mandate: figure out why a supposedly high-performing team wasn't actually delivering.",
   ["Ignored the vanity metrics and instrumented what mattered — the DORA metrics and real feature outcomes.",
    "Found the truth: lead time was three weeks, change-fail rate was 30%, and on-call was brutal.",
    "Refocused the team on outcomes and reliability, and made lead time and deploy frequency the visible goals.",
    "Added a lightweight team-health pulse, so morale was a number I watched, not a surprise."],
   [("3 wks → 2 days", "lead time"), ("30% → 4%", "change-fail rate"), ("0 regretted", "attrition after")],
   "Velocity measures motion. Outcomes, reliability, and team health measure performance.",
   "You looked past the flattering chart to what the team actually produced. That's judgment."),
  "Here's a story that makes this concrete. [pause] The situation. I inherited a team "
  "whose velocity chart looked fantastic. Story points climbing every single sprint, up "
  "and to the right. If you only looked at that chart, this was a high-performing team. "
  "But something was clearly off. Leadership was quietly frustrated. Features were "
  "technically shipping, but they weren't actually landing with users. And two of the "
  "best engineers were interviewing elsewhere. The chart and the reality did not match. "
  "[pause] So my mandate was to figure out why a supposedly high-performing team wasn't "
  "really delivering. [pause] First, I ignored the vanity metrics completely. Story "
  "points can be gamed, and this team had gotten very good at generating them. Instead, "
  "I instrumented what actually mattered. The DORA delivery metrics, and the real "
  "business outcomes of the features we shipped. [pause] Second, the data told the "
  "truth the velocity chart was hiding. Our lead time, from a commit to it reaching "
  "production, was three weeks. Our change-fail rate was thirty percent, meaning nearly "
  "a third of our deploys caused an incident or a rollback. And on-call was so brutal "
  "that it was burning people out. The team was extremely busy. It just wasn't "
  "effective. [pause] Third, I refocused everyone on outcomes and reliability. I retired "
  "the story-point theater entirely. And I made lead time and deploy frequency the "
  "goals we actually watched in reviews, so the whole team optimized for getting real, "
  "working value to users faster. [pause] And fourth, I added a lightweight team-health "
  "pulse. A short, regular check on morale and on-call load, so that a person's "
  "unhappiness became a number I could see and act on, instead of a resignation letter "
  "that blindsided me. [pause] The result, over about two quarters. Lead time went from "
  "three weeks to two days. Change-fail rate dropped from thirty percent to four. And "
  "we had zero regretted attrition after that. [pause] What I learned. Velocity measures "
  "motion. Outcomes, reliability, and the health of your people, those measure actual "
  "performance."),

 # --- Q2 MOTIVATING A DEMORALIZED TEAM ---
 ("s04_motivate", "em_q", Q(
   "OPERATING · MORALE", "Re-energizing a demoralized team",
   "How do you motivate a team that has lost its motivation?", YOU,
   [("S", "Find the real cause", "Burnout, a failed launch, no autonomy, unclear purpose? Diagnose, don't cheerlead."),
    ("A", "Restore meaning and wins", "Reconnect the work to real impact, and engineer a few early, visible wins."),
    ("A", "Give autonomy back", "Remove the blockers and the thrash; let them own decisions again."),
    ("L", "Fix the system", "Repair whatever burned them out, or morale just slides back to zero.")],
   "You threw a pizza party or a speech at a structural problem.",
   "You treat morale as a system to diagnose and fix, not a mood to hype.",
   "Motivation is a symptom. You fix the cause — purpose, autonomy, and a sane pace."),
  "Second question. How do you motivate a team that's lost its motivation? [pause] The "
  "trap is to reach for a pizza party, or a motivational speech. That does nothing for "
  "a structural problem. [pause] Instead, find the real cause. Is it burnout? A failed "
  "launch? No autonomy? No clear purpose? Diagnose it. [pause] Then restore meaning, and "
  "engineer a few early wins to rebuild belief. Give the team autonomy back. Let them "
  "own decisions again. [pause] And fix the underlying system, or the morale you rebuilt "
  "just slides right back to zero."),

 ("s04s_motivate", "em_story", St(
   "WORKED EXAMPLE · MORALE", "The team that survived a death march", YOU,
   "I took over a team right after a brutal six-month death march — nights and weekends — to ship a launch that then got cancelled. Morale was on the floor, velocity had collapsed, and cynicism was everywhere.",
   "My mandate: rebuild the team's energy and output, without another forced march.",
   ["Started by listening — one-on-ones with everyone, no agenda, just what's broken and what they'd change.",
    "Reconnected them to impact — killed the low-value work and picked a project with real, visible user value.",
    "Engineered early wins — shipped something small but real in two weeks to rebuild belief.",
    "Fixed the cause — capped the hours, protected focus time, and gave decisions back to the team."],
   [("6 weeks", "to real momentum"), ("+31", "team eNPS"), ("0", "attrition that year")],
   "You can't pep-talk your way out of burnout. Remove the cause, then rebuild belief with wins.",
   "You diagnosed the cause and rebuilt trust with action, not slogans. That's leadership."),
  "Let me make that real with a story. [pause] The situation. I took over a team right "
  "after a brutal, six-month death march. Nights and weekends, for half a year, to ship "
  "a huge launch. And then, right at the finish line, leadership cancelled the whole "
  "thing. All of it, thrown away. [pause] So by the time I arrived, morale was "
  "completely on the floor. Velocity had collapsed. And the cynicism was thick. People "
  "were showing up, doing the bare minimum, and watching the clock. A few of the best "
  "ones had already started looking. [pause] My mandate was to rebuild this team's "
  "energy and output. And critically, to do it without ordering another forced march, "
  "which would have finished them off entirely. [pause] Now, the tempting, lazy move "
  "here is a motivational speech, or a team lunch. I knew that would just breed more "
  "cynicism. So I didn't. [pause] First, I started by listening, not talking. I did "
  "one-on-ones with every single person, with no agenda. Just two questions. What's "
  "broken, and what would you change? People have to feel genuinely heard before "
  "they'll re-engage with anything. [pause] Second, I reconnected them to impact. The "
  "cancelled project had made everyone feel like their work was pointless. So I killed "
  "off a pile of low-value busywork, and I picked one project with real, visible user "
  "value, something they could be proud of again. [pause] Third, I engineered an early "
  "win, on purpose. We shipped something small but genuinely real within two weeks. Not "
  "because the feature was huge, but because the team needed to prove to itself that it "
  "could still ship, and still matter. [pause] And fourth, I fixed the actual cause of "
  "the burnout. I capped the working hours. I protected focus time. And I gave real "
  "decision-making back to the team, because the death march had stripped away every "
  "bit of their autonomy. [pause] The result. Within six weeks, the team had real "
  "momentum again. On our next engagement survey, morale jumped thirty-one points. And "
  "we had zero attrition that year. [pause] What I learned. You cannot pep-talk your way "
  "out of burnout. You remove the cause, and then you rebuild belief with real, visible "
  "wins."),

 # --- Q3 RETAINING A KEY ENGINEER ---
 ("s05_retain", "em_q", Q(
   "PEOPLE · RETENTION", "Retaining a key engineer",
   "A key engineer says they're thinking of leaving. Now what?", SIT,
   [("S", "Understand the real reason", "Money, growth, manager, boredom, burnout? The stated reason is rarely the whole one."),
    ("A", "Act on what you can", "Fix growth, scope, or recognition fast; be honest about what you can't change."),
    ("A", "Make a genuine case", "A specific future here — not a panic counter-offer that resets in six months."),
    ("L", "Learn from every exit", "If they still go, run an honest retro and fix the pattern for the rest.")],
   "You only reacted with a counter-offer once they'd already mentally quit.",
   "You retain people through growth and trust, and handle regretted attrition with grace.",
   "The best retention happens months before the resignation — but you can still save some."),
  "Third question. A key engineer tells you they're thinking of leaving. Now what? "
  "[pause] The trap is to panic and throw money at someone who has already mentally "
  "quit. [pause] Instead, first understand the real reason. Money, growth, their "
  "manager, boredom, burnout. The reason they say out loud is rarely the whole story. "
  "[pause] Then act fast on what you can actually change, and be honest about what you "
  "can't. Make a genuine case for their future here. Not a desperate counter-offer. "
  "[pause] And if they still leave, learn from it, and fix the pattern for everyone "
  "else."),

 ("s05s_retain", "em_story", St(
   "WORKED EXAMPLE · RETENTION", "The star engineer with one foot out the door", SIT,
   "My strongest engineer, Ana — the one who owned our core service — asked for a private one-on-one and told me she'd started interviewing. Losing her would have set the team back a year.",
   "My mandate: understand why, and keep her — but only if staying was genuinely right for her.",
   ["Listened first, didn't panic — and the real reason wasn't pay. She felt stuck and unchallenged.",
    "Acted fast on what I could — carved out a new architecture charter that stretched her, within two weeks.",
    "Made a specific, honest case for her future here, instead of a desperate counter-offer.",
    "Fixed the root cause for others too — I'd under-invested in growth across all my senior engineers."],
   [("stayed 2+ yrs", "and re-engaged"), ("promoted", "to Principal"), ("growth plans", "for every senior")],
   "Retention is built months early through growth. A counter-offer alone just delays the exit.",
   "You addressed the real cause, not the symptom — and fixed it for the whole team."),
  "Here's how that plays out in practice. [pause] The situation. My strongest engineer, "
  "Ana, the person who single-handedly owned our entire core service, asked me for a "
  "private one-on-one. And she told me, calmly, that she'd started interviewing "
  "elsewhere. My stomach dropped, honestly. Losing her would have set the team back by a "
  "year, easily, and put our most critical system at risk. [pause] My mandate, in that "
  "moment, was to understand why. And to keep her, but only if staying was genuinely the "
  "right thing for her, and not just convenient for me. [pause] First, I listened, and I "
  "did not panic. Every instinct was screaming at me to immediately blurt out a raise, a "
  "counter-offer, anything. I held back, and I just asked her to walk me through it. And "
  "it turned out the real reason had nothing to do with pay. She felt stuck. "
  "Unchallenged. She'd been doing the same kind of work for two years, and she'd stopped "
  "growing. [pause] Second, I acted fast on what I could actually control. This wasn't a "
  "money problem, it was a growth problem, and that I could fix. Within two weeks, I "
  "carved out a brand-new architecture charter for her. A genuinely hard, ambiguous, "
  "high-impact problem that would stretch her in exactly the way she was missing. "
  "[pause] Third, I made a specific, honest case for her future here. Not a vague "
  "promise to do better. A concrete path, with the new scope, and a real route to "
  "principal engineer, with the milestones spelled out. [pause] And fourth, and this is "
  "the part that matters most, I treated her as a signal, not an isolated exception. My "
  "logic was, if Ana is this bored, others probably are too, and they just haven't said "
  "it yet. I realized I'd quietly under-invested in growth across all of my senior "
  "engineers. So I fixed it for the entire group, not just for her. [pause] The result. "
  "She stayed, for more than two years, fully re-engaged. She was promoted to principal. "
  "And I built real, individual growth plans for every senior engineer on the team. "
  "[pause] What I learned. Retention is really built months in advance, through growth. "
  "A counter-offer, by itself, just delays the exit by a few months."),

 # --- Q4 MANAGING MANAGERS ---
 ("s06_managers", "em_q", Q(
   "SCALE · LEADING LEADERS", "Managing managers, and scaling yourself",
   "How do you lead when you're managing managers, not engineers?", META,
   [("S", "Change what you optimize", "You no longer ship features. You ship healthy teams and good managers."),
    ("A", "Delegate outcomes, not tasks", "Set the what and the why; let them own the how, and the mistakes."),
    ("A", "Use skip-levels and signals", "Skip-level one-on-ones and team-health metrics — lead through, not around, your managers."),
    ("L", "Grow your managers", "Coach them like you once coached engineers. Your leverage is their growth.")],
   "You kept operating like a lead — in the code, in the details, undermining your managers.",
   "You lead through others and scale your impact past what you could do alone.",
   "The job stops being about your output, and starts being about your leaders' output."),
  "Last question, and it's the senior-most one. How do you lead when you're managing "
  "managers, not engineers? [pause] The trap is to keep operating like a tech lead. "
  "Staying in the code and the details, and quietly undermining your own managers. "
  "[pause] Instead, change what you optimize for. You no longer ship features. You "
  "ship healthy teams and good managers. [pause] Delegate outcomes, not tasks. Use "
  "skip-level one-on-ones and team-health signals, so you lead through your managers, "
  "not around them. [pause] And coach them, the way you once coached engineers. Your "
  "leverage now is their growth."),

 ("s06s_managers", "em_story", St(
   "WORKED EXAMPLE · LEADING LEADERS", "Turning a great engineer into a first-time manager", META,
   "As my org grew past twenty people, I had to split it into teams. My strongest tech lead, Ravi, was the obvious choice to run one — but he'd never managed, and great engineers often make miserable managers.",
   "My mandate: grow Ravi into a real manager, without losing him or breaking his team.",
   ["Set the new bar explicitly — his job was now his team's output and growth, not his own commits.",
    "Delegated outcomes, not tasks — I gave him the goals and let him own the how, including early mistakes.",
    "Coached him weekly on the craft — feedback, prioritization, one-on-ones — and used skip-levels to sense the team without going around him.",
    "Protected his authority — I let his team see him as the decision-maker, and backed his calls in public."],
   [("6 months", "to a self-sufficient manager"), ("first launch", "shipped under him"), ("0", "attrition on his team")],
   "Managing managers means coaching the craft and leading through them, never around them.",
   "You scaled yourself by growing a leader, not by staying the hero engineer. The senior bar."),
  "Here's the story for that one. [pause] The situation. As my org grew past twenty "
  "people, it got too big for me to manage directly, so I had to split it into smaller "
  "teams, each with its own manager. And my strongest tech lead, Ravi, was the obvious "
  "person to run one of them. He was respected, and technically brilliant. But there was "
  "a real risk here. He had never managed anyone in his life. And, honestly, great "
  "engineers often make miserable first-time managers, because the skills are almost "
  "completely different. The thing that made him great, going deep and solving it "
  "himself, was exactly the wrong instinct for a manager. [pause] So my mandate was to "
  "grow Ravi into a real manager, without losing him, and without breaking the team I "
  "was handing him. [pause] First, I set the new bar explicitly, on day one. I told him, "
  "directly, your job is no longer your own commits. Your job is now your team's output, "
  "and your team's growth. If you write all the important code yourself, you have "
  "failed, even if the code is perfect. That reframe is everything, and most first-time "
  "managers never hear it said out loud. [pause] Second, I delegated outcomes, not "
  "tasks. I gave him the goals and the why, and then I forced myself to let him own the "
  "how. That included watching him make some early mistakes, like taking on too much "
  "himself, that I had to sit on my hands and allow, because that's how he'd learn. "
  "[pause] Third, I coached him every single week on the actual craft of management. How "
  "to give difficult feedback. How to prioritize ruthlessly. How to run a one-on-one "
  "that isn't just a status update. And I used skip-level one-on-ones with his engineers "
  "to sense how the team was really doing, without ever going around him or undermining "
  "him. [pause] And fourth, I actively protected his authority. In front of his team, "
  "he was the decision-maker, full stop. I backed his calls in public, even the "
  "occasional one I might have made differently, and I gave him my disagreements only in "
  "private. [pause] The result. Within about six months, he was a genuinely "
  "self-sufficient manager. His team shipped its first major launch under his "
  "leadership. And he had zero attrition. [pause] What I learned. Managing managers "
  "means coaching the craft, and leading through your managers, never around them. That "
  "is how you scale your own impact, instead of staying the hero engineer who doesn't "
  "scale at all."),

 # --- RECAP ---
 ("s07_recap", "em_recap",
  {"items": [
     "Measure outcomes and team health, never just velocity.",
     "Motivation is a system — fix the cause, don't throw a party.",
     "Retain people through growth, months before they quit.",
     "Managing managers means leading through them, not around.",
     "Same spine every time: STAR, plus what you learned.",
   ],
   "closer": "Lead the team, grow the leaders, and the output takes care of itself."},
  "Let's recap part two. [pause] Measure outcomes and team health, not vanity metrics. "
  "Treat motivation as a system, and fix the real cause. Retain your best people "
  "through growth, long before they think about leaving. [pause] And when you manage "
  "managers, lead through them, not around them. Same spine every time. STAR, plus the "
  "learning. [pause] Take these example answers, and rewrite them with your own real "
  "stories. [pause] Lead the team, grow the leaders, and the output takes care of "
  "itself. Thanks for watching."),
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
