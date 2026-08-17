#!/usr/bin/env python3
"""The Engineering Manager Behavioral Interview — Part 5: Partnership & Self-Awareness.

Standalone follow-up. Reuses the `em` scene set; narration staged under public/em5.
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
AUDIO = "em5"
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
  {"kicker": "ENGINEERING LEADERSHIP · PART FIVE", "line1": "Partnership &",
   "line2": "Self-Awareness", "sub": "four more behavioral questions · with full worked answers · Senior EM"},
  "Welcome to part five. [pause] This set is about the more human, reflective side of "
  "leadership. Taking over a new team, partnering with product, lifting other people "
  "up, and hearing hard truths about yourself. [pause] Four questions, same format. "
  "The method, and then a full worked answer for each."),

 ("s02_star", "em_star", {},
  "The spine, one more time, because it carries every answer. [pause] STAR. Situation, "
  "task, action, result. Plus L, for learning. [pause] Own it with the word I. Keep "
  "the setup short. And live in the action. Let's begin."),

 # --- Q1 NEW / STRUGGLING TEAM ---
 ("s03_newteam", "em_q", Q(
   "LEADERSHIP · ONBOARDING", "Taking over a new or struggling team",
   "How do you approach your first 90 days with a new team?", SIT,
   [("S", "Listen before you change", "Resist reorganizing on day one. Diagnose first — earn the right to lead."),
    ("A", "Meet everyone, read everything", "One-on-ones with the whole team and key partners; learn the system and the history."),
    ("A", "Find and ship an early win", "Pick one visible, real problem and fix it fast, to build trust and momentum."),
    ("L", "Then set direction with them", "Only once you understand it, set a clear direction the team helped shape.")],
   "You came in as the “hero fixer” and reorganized everything before you understood it.",
   "You lead with humility and diagnosis, then act — you don't impose before you understand.",
   "The first 90 days are for listening and one early win — not a grand reorg you'll regret."),
  "First question. How do you approach your first ninety days with a new team? [pause] "
  "The trap is to charge in as the hero fixer, and reorganize everything before you "
  "understand any of it. [pause] Instead, listen before you change. Resist the urge to "
  "reorganize on day one. [pause] Meet everyone, read everything. One-on-ones with the "
  "team and your partners. Then find and ship one early, visible win, to build trust. "
  "[pause] And only then, set direction, with the team, not at them."),

 ("s03s_newteam", "em_story", St(
   "WORKED EXAMPLE · ONBOARDING", "Taking over a team that had lost the company's trust", SIT,
   "I was asked to take over a team with a terrible reputation. It had missed three launches in a row, other teams had stopped depending on it, and morale was rock bottom. Leadership wanted a fast turnaround.",
   "My mandate: turn it around — but I resisted the pressure to slash and reorganize on day one.",
   ["Listened first, for three weeks — one-on-ones with every engineer and every frustrated partner team, just asking what was really wrong.",
    "Found the real problem — it wasn't the people. It was impossible scope, no clear priorities, and constant thrash from above.",
    "Shipped a fast, visible win — I renegotiated scope, cut the roadmap in half, and we delivered one solid thing in a month.",
    "Then set direction with them — a focused mission the team helped write, and I shielded them from the thrash."],
   [("3 misses → on-time", "delivery restored"), ("trust", "rebuilt with partners"), ("+28", "team morale")],
   "Resist the hero-fixer urge. Diagnose first, ship one early win, then set direction together.",
   "You led with humility and a fast win, not a reorg. That's how you earn a team, not command it."),
  "Here's the story. [pause] The situation. I was asked to take over a team that had a "
  "genuinely terrible reputation. It had missed three launches in a row. Other teams "
  "had quietly stopped depending on it. And the morale inside it was at rock bottom. "
  "And leadership wanted a fast turnaround, which created a lot of pressure to come in "
  "swinging. [pause] My mandate was to turn it around. But I made a deliberate choice to "
  "resist the pressure to slash and reorganize on day one. [pause] First, I listened, "
  "for a full three weeks before changing anything. I did one-on-ones with every single "
  "engineer, and with every frustrated partner team. And I just asked one question. "
  "What's actually wrong here? [pause] Second, that listening found the real problem. "
  "And it wasn't the people, which is what everyone had assumed. It was an impossible "
  "scope, no clear priorities, and constant thrash coming down from above. The team "
  "wasn't lazy. It was set up to fail. [pause] Third, I shipped a fast, visible win. I "
  "went and renegotiated our scope with leadership. I cut the roadmap in half. And with "
  "that focus, the team delivered one solid, real thing within a month. That single win "
  "started rebuilding trust, inside and outside the team. [pause] And fourth, only then "
  "did I set direction, with them. A focused mission that the team helped write. And I "
  "put myself between them and the thrash from above. [pause] The result. After three "
  "straight misses, we were delivering on time again. Trust with our partner teams was "
  "rebuilt. And team morale jumped twenty-eight points. [pause] What I learned. Resist "
  "the hero-fixer urge. Diagnose first, ship one early win, and then set the direction "
  "together."),

 # --- Q2 CONFLICT WITH PRODUCT ---
 ("s04_pmconflict", "em_q", Q(
   "CROSS-FUNCTIONAL · PRODUCT", "Partnering, and clashing, with Product",
   "Tell me about a conflict with a product manager or partner.", RES,
   [("S", "Assume a shared goal", "You and the PM both want a great product. Start from the goal, not the turf."),
    ("A", "Separate the what from the how", "PM owns the what and why; you own the how and its cost. Respect the line."),
    ("A", "Bring data and options, not a veto", "“No” becomes “here's the cost, and two paths.” Make the trade-off shared."),
    ("L", "Protect the relationship", "You'll work with this person for years. Win the decision, keep the partnership.")],
   "You made it engineering versus product, or you silently complied and resented it.",
   "You're a true partner to product — candid, data-driven, and durable across disagreements.",
   "The EM–PM relationship is a marriage. Disagree on the decision; never damage the partnership."),
  "Second question. Tell me about a conflict with a product manager, or a partner. "
  "[pause] The trap is to make it engineering versus product. Or, just as bad, to "
  "silently comply and quietly resent it. [pause] Instead, assume a shared goal. You "
  "both want a great product. Separate the what from the how. The P M owns the what and "
  "the why. You own the how, and what it costs. [pause] Bring data and options, not a "
  "veto. And above all, protect the relationship, because you'll work with this person "
  "for years."),

 ("s04s_pmconflict", "em_story", St(
   "WORKED EXAMPLE · PRODUCT", "The PM who wanted it all shipped by Friday", RES,
   "My product partner wanted a major feature shipped in two weeks to hit a launch event. My team was certain it needed four — and doing it in two meant cutting testing on a payments flow. It got tense fast.",
   "My mandate: protect quality and the relationship, without just stonewalling with a “no.”",
   ["Anchored on the shared goal — we both wanted a successful launch, not a demo that broke live on stage.",
    "Respected the line — I acknowledged the launch date was his call; the engineering risk was mine to make visible.",
    "Brought options, not a veto — I showed the real risk, and offered a phased plan: a solid core at the event, the rest a week later.",
    "Made the trade-off jointly — we chose the phased plan together, and I put it in writing as a shared decision."],
   [("launched on time", "the core, safely"), ("0 payment bugs", "live on stage"), ("stronger", "EM–PM partnership")],
   "Turn a “versus” into a shared trade-off. Win the decision with data, and keep the partner.",
   "You disagreed hard on the how and still strengthened the partnership. That's the maturity they want."),
  "Here's the story. [pause] The situation. My product partner wanted a major feature "
  "shipped in two weeks, to hit a big launch event. My team was certain it needed four "
  "weeks. And doing it in two would have meant cutting our testing on a payments flow, "
  "where a bug means real money lost. It got tense, fast, and it was starting to feel "
  "like engineering versus product. [pause] My mandate was to protect both the quality "
  "and the relationship, without just stonewalling him with a flat no. [pause] First, I "
  "anchored us both back on the shared goal. We both wanted a successful launch. "
  "Neither of us wanted a demo that broke, live, on stage. Once that was said out loud, "
  "we were on the same side of the table again. [pause] Second, I respected the line "
  "between us. I explicitly acknowledged that the launch date was his call to make. But "
  "the engineering risk was mine to make visible, clearly and without drama. [pause] "
  "Third, I brought options, not a veto. I laid out the real risk of the payments flow. "
  "And instead of just saying no, I offered a phased plan. A solid, well-tested core "
  "feature ready for the event, and the rest following about a week later. [pause] And "
  "fourth, we made the trade-off jointly. We chose the phased plan together, and I put "
  "it in writing, so it was clearly a shared decision, not me overruling him. [pause] "
  "The result. We launched on time, with the core, safely. There were zero payment bugs "
  "on stage. And honestly, the partnership came out stronger, because he learned he "
  "could trust me to find a path, not just block him. [pause] What I learned. Turn a "
  "versus into a shared trade-off. Win the decision with data, and keep the partner."),

 # --- Q3 MENTORING / SPONSORSHIP ---
 ("s05_sponsor", "em_q", Q(
   "PEOPLE · SPONSORSHIP", "Mentoring and sponsoring others",
   "Tell me about someone you mentored or sponsored.", YOU,
   [("S", "Know the difference", "Mentoring is advice you give them. Sponsorship is advocacy when they're not in the room."),
    ("A", "Invest beyond your reports", "The best mentoring often crosses team lines and levels — not just your org chart."),
    ("A", "Sponsor with your capital", "Put their name forward, hand them visible work, and defend it where it matters."),
    ("L", "Measure it by their trajectory", "Did they get promoted, unstuck, or braver? Their growth is the receipt.")],
   "You described giving generic advice, with no real risk or advocacy on your part.",
   "You actively grow people and spend your own credibility to lift them — a force multiplier.",
   "Mentoring is talking. Sponsorship is spending your own capital to open a door. Great leaders do both."),
  "Third question. Tell me about someone you mentored, or sponsored. [pause] And know "
  "the difference, because it matters. Mentoring is advice you give them. Sponsorship is "
  "advocacy for them when they are not in the room. [pause] Invest beyond just your own "
  "reports. And sponsor with your capital. Put their name forward, hand them visible "
  "work, and defend it in the rooms that matter. [pause] Then measure it by their "
  "trajectory. Did they get promoted, or unstuck? Their growth is the receipt."),

 ("s05s_sponsor", "em_story", St(
   "WORKED EXAMPLE · SPONSORSHIP", "Sponsoring an engineer everyone had overlooked", YOU,
   "A quiet, mid-level engineer on a neighboring team, Meera, did consistently excellent work but got no recognition. She wasn't loud, she was on a low-visibility team, and she'd been stuck at the same level for years.",
   "She wasn't even my report, but her own manager wasn't advocating for her — so I decided to sponsor her.",
   ["Started with mentoring — regular sessions on scope, visibility, and how to navigate the promotion process.",
    "Then actually sponsored her — I pulled her onto a high-visibility cross-team project that I could influence.",
    "Spent my own capital — I put her name forward in staffing rooms, and vouched for her in the promotion calibration.",
    "Coached her manager too — so the advocacy would keep going after I stepped back."],
   [("promoted", "to Senior, then lead"), ("cross-team", "visibility earned"), ("pattern fixed", "for her whole team")],
   "Mentoring is advice. Sponsorship is spending your credibility to open a door someone has earned.",
   "You spent your own capital to lift someone, with no upside for you. That's the leader they want."),
  "Here's a story about sponsorship, specifically. [pause] The situation. There was a "
  "quiet, mid-level engineer on a neighboring team. Her name was Meera. And she did "
  "consistently excellent work. But she got almost no recognition for it. She wasn't "
  "loud. She was on a low-visibility team. And she'd been stuck at the same level for "
  "years, watching louder people get promoted past her. [pause] Now, here's the thing. "
  "She wasn't even my report. But I could see her own manager wasn't advocating for "
  "her. So I decided to sponsor her anyway. [pause] First, I started with mentoring. "
  "Regular sessions on how to scope her work bigger, how to make it visible, and how to "
  "actually navigate our promotion process, which nobody had ever explained to her. "
  "[pause] Second, I moved from mentoring to real sponsorship, and that's the key "
  "difference. I pulled her onto a high-visibility, cross-team project that I had "
  "influence over. I put her where the important work was. [pause] Third, I spent my "
  "own political capital on her. I put her name forward in staffing rooms she wasn't in. "
  "And I vouched for her, specifically, in the promotion calibration meeting, where "
  "decisions actually get made. [pause] And fourth, I coached her own manager on how to "
  "advocate for her, so that the support would continue long after I stepped back. "
  "[pause] The result. She was promoted to senior, and within another year, to a lead "
  "role. She'd earned genuine cross-team visibility. And I'd helped fix the pattern for "
  "her whole overlooked team. [pause] What I learned. Mentoring is advice. Sponsorship "
  "is spending your own credibility to open a door that someone has already earned."),

 # --- Q4 RECEIVING HARD FEEDBACK ---
 ("s06_coachable", "em_q", Q(
   "SELF · COACHABILITY", "Getting hard feedback — and changing",
   "Tell me about tough feedback you received, and what you did.", META,
   [("S", "Pick feedback that stung", "A real criticism of you as a leader — not “I take on too much.”"),
    ("A", "Own it without defending", "The tell is your first reaction: did you get curious, or defensive?"),
    ("A", "Make a visible change", "A concrete behavior you altered, that other people could actually see."),
    ("L", "Close the loop", "Go back to the person who gave the feedback and show them it landed.")],
   "You picked flattering feedback, or you explained why the feedback was actually wrong.",
   "You're coachable — you can hear a hard truth about yourself and genuinely change.",
   "How you take feedback is how they predict you'll grow. Coachability is a senior-leadership signal."),
  "Last question, and it's really a test of coachability. Tell me about tough feedback "
  "you received, and what you did with it. [pause] The trap is to pick flattering "
  "feedback, or to explain why the feedback was actually wrong. That fails the test "
  "instantly. [pause] Instead, pick feedback that genuinely stung. Own it, without "
  "defending. The tell is your first reaction. Did you get curious, or defensive? "
  "[pause] Then make a visible change, and close the loop with the person who gave it."),

 ("s06s_coachable", "em_story", St(
   "WORKED EXAMPLE · COACHABILITY", "The feedback that I was intimidating my own team", META,
   "In a skip-level review, my manager told me something that stung. My team found me intimidating in technical discussions. As a strong engineer, I'd jump in with the answer — and people had started staying quiet and deferring to me instead of thinking.",
   "My mandate to myself: actually change this, rather than explain it away.",
   ["Sat with the discomfort — my first instinct was to defend myself, but I made myself get curious and ask for specifics.",
    "Made a visible behavior change — I stopped giving my opinion first in design reviews, and started asking questions instead.",
    "Created space on purpose — I had others present and decide, and I deliberately let the silences sit.",
    "Closed the loop — months later, I asked the team, and my manager, whether it had changed. It had."],
   [("team spoke up", "measurably more"), ("better decisions", "not just faster ones"), ("closed the loop", "and it stuck")],
   "How you receive hard feedback about yourself is the truest measure of whether you'll grow.",
   "You heard a painful truth, changed a real behavior, and checked that it landed. That's coachability."),
  "And the final story, which is about hearing something hard about yourself. [pause] "
  "The situation. In a skip-level review, my own manager told me something that really "
  "stung. He said my team found me intimidating in technical discussions. As a strong "
  "engineer, my instinct was to jump straight in with the answer. And the effect was "
  "that people had started staying quiet, and just deferring to me, instead of actually "
  "thinking for themselves. I was accidentally making my own team worse. [pause] My "
  "mandate to myself was to actually change this. Not to explain it away. [pause] First, "
  "I sat with the discomfort. And I'll be honest, my very first instinct was to defend "
  "myself, to say, well, I'm just trying to help. I caught that instinct, and instead I "
  "made myself get curious, and I asked for specific examples. [pause] Second, I made a "
  "visible behavior change. In design reviews, I stopped giving my opinion first. "
  "Instead, I started asking questions, and I waited. [pause] Third, I created space on "
  "purpose. I had other people present the designs and make the calls. And I "
  "deliberately let the silences sit, even when they were uncomfortable, so that "
  "someone else would fill them. [pause] And fourth, I closed the loop. A few months "
  "later, I went back and explicitly asked the team, and my manager, whether it had "
  "actually changed. And it had. [pause] The result. The team spoke up measurably more. "
  "We started making better decisions, not just faster ones. And because I closed the "
  "loop, the change actually stuck. [pause] What I learned. How you receive a hard "
  "truth about yourself is the single truest measure of whether you will keep growing "
  "as a leader."),

 # --- RECAP ---
 ("s07_recap", "em_recap",
  {"items": [
     "In a new role, listen and ship one win before you reorganize.",
     "Turn product conflict into a shared trade-off, not a turf war.",
     "Sponsorship is spending your capital, not just giving advice.",
     "Coachability — hearing hard feedback and changing — is senior.",
     "Same spine every time: STAR, plus what you learned.",
   ],
   "closer": "The best leaders listen hard, lift others, and never stop being coachable."},
  "Let's recap part five. [pause] When you take over a team, listen first and ship one "
  "early win before you reorganize anything. Turn a conflict with product into a shared "
  "trade-off, never a turf war. [pause] Remember that sponsorship is spending your own "
  "capital to lift someone, not just giving advice. And that being coachable, hearing a "
  "hard truth and actually changing, is one of the strongest senior signals there is. "
  "[pause] Same spine every time. STAR, plus the learning. [pause] The best leaders "
  "listen hard, lift others, and never stop being coachable. Make these stories your "
  "own, and good luck. Thanks for watching."),
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
