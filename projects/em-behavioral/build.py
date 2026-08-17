#!/usr/bin/env python3
"""The Engineering Manager Behavioral Interview — build script.

Each question gets: a short "how to answer" coaching scene (em_q) followed by a
full 2-3 min worked-example STAR-L story (em_story). Stories are illustrative,
big-tech-scale model answers to adapt to your own experience.

Pipeline: narration TTS (idempotent) -> concat with gaps -> edit_decisions.json.
TTS backend: Voicebox.app local HTTP API (must be open). Run:  python3 build.py
"""
import json, os, subprocess, time, urllib.request

BASE = "http://127.0.0.1:17493"
PROFILE = "c488e05c-3407-46a3-874d-1b09b3aff78d"  # "TTS Bright (Nova)"
GAP = 0.5
PAUSE = 0.6
ATEMPO = 0.95
PREFIX = "em"
ROOT = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(ROOT, "..", ".."))
PUBLIC = os.path.join(REPO, "composer", "public", PREFIX)
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
 # ================= OPEN =================
 ("s01_title", "em_title", {},
  "You've passed the coding rounds. [pause] Now comes the round that actually decides "
  "if you get to lead a team. The behavioral interview."),

 ("s02_hook", "em_hook", {},
  "By now, they believe you can build things. [pause] This round asks a different "
  "question. Would we hand you a team? [pause] Every prompt that starts with tell me "
  "about a time is really one question. How do you lead when it's hard? [pause] "
  "The stories are your evidence. The structure is the skill. Let's build both. "
  "For every question, I'll give you the method, and then a full example answer you "
  "can adapt."),

 ("s03_compass", "em_compass", {},
  "First, know what's being measured. [pause] Almost every question maps to one of "
  "four things. Can you grow and keep people? Can you deliver under pressure? Can you "
  "make good judgment calls? [pause] And can you look in the mirror and own a failure? "
  "[pause] When you hear a question, silently label which one it's testing. That tells "
  "you what to emphasize."),

 ("s04_star", "em_star", {},
  "Every answer needs a spine. [pause] Use STAR. Situation, the one line of setup. "
  "Task, what you were responsible for. Action, what you personally did. And Result, "
  "the outcome. [pause] But at the management level, add a letter. L, for learning. "
  "[pause] What would you do again, or differently? That's what separates a doer from "
  "a leader. Spend most of your airtime on the Action."),

 ("s05_iwe", "em_iwe", {},
  "Before the questions, fix the two traps that sink almost everyone. [pause] "
  "Trap one. You say we did this, we did that. The interviewer can't see you in the "
  "story. Own your decisions with I. Then hand credit to the team. [pause] Trap two. "
  "Most people spend ninety seconds on backstory and twenty on the decision. "
  "[pause] Flip it. Two sentences of context, then live in the action."),

 # ================= PART 1: PEOPLE =================
 ("s06_div1", "em_divider", {"n": 1, "title": "People", "sub": "grow them, or manage them out", "color": YOU},
  "Part one. People. [pause] This is the heart of the job, and where managers are "
  "tested hardest."),

 # --- Q1 GROWTH ---
 ("s07_grow", "em_q", Q(
   "PEOPLE · GROWTH", "Growing an engineer to the next level",
   "Tell me about a time you helped an engineer grow.", YOU,
   [("S", "Set a concrete bar", "Name the specific gap between where they were and the next level."),
    ("A", "Create the reps", "Hand them a stretch project with real scope, then step back."),
    ("A", "Coach, don't rescue", "Weekly one-on-ones on the how; let them own the mistakes."),
    ("R", "Show the promotion", "End on the outcome: promoted, or leading what they couldn't before.")],
   "“I told them to do better and they improved.” No plan, no proof.",
   "You build people deliberately, and can scale yourself through others.",
   "Growth stories are the most under-prepared, and the most predictive of a good manager."),
  "Start with growth, because it's what most people forget to prepare. [pause] "
  "Tell me about a time you grew an engineer. [pause] Don't say you told them to do "
  "better. Instead, set a concrete bar. Name the gap to the next level. Then create "
  "the reps. Give them a stretch project with real scope. [pause] Coach them, but "
  "don't rescue them. Let them own the mistakes. [pause] And land on the result. A "
  "promotion, or a person now leading what they couldn't before."),

 ("s07s_grow", "em_story", St(
   "WORKED EXAMPLE · GROWTH", "Growing an engineer to senior — a full answer", YOU,
   "On a payments platform doing forty million transactions a day, I had a mid-level engineer, Priya. Technically excellent, but she'd been passed over for senior twice, and she was frustrated.",
   "My mandate: get her to the senior bar within a year — for real, without lowering it.",
   ["Wrote the exact gap down with her — it was scope and influence, not coding — mapped to our senior rubric.",
    "Handed her the payment-retry idempotency redesign: cross-team, high-stakes, and I deliberately stayed out of it.",
    "Coached the how in weekly one-on-ones — design reviews, stakeholder pushback — but she made every call.",
    "Created visibility: she presented the design to the org, and I pre-wired the promotion committee."],
   [("11 months", "promoted to Senior"), ("↓ 90%", "retry failures"), ("3 mentees", "she now grows others")],
   "Define the gap in writing on day one. Vague growth goals grow no one.",
   "Every action is “I did” — but it ends on her growth, not mine. That's the balance."),
  "Here's what a strong answer actually sounds like. Listen to the structure. [pause] "
  "The situation. I was running a team on a payments platform that handled about forty "
  "million transactions a day. On that team I had a mid-level engineer, Priya. She was "
  "one of the sharpest coders I had. But she'd been passed over for senior twice. And "
  "by the time I inherited the team, she was frustrated, and honestly, close to "
  "leaving. [pause] So my mandate was clear. Get her to the senior bar within a year. "
  "For real. Not by lowering the bar, but by actually closing the gap. [pause] Now, "
  "what did I do? Four things. [pause] First, I sat down with her, and we wrote the "
  "exact gap down, together. And this mattered, because it turned out the gap wasn't "
  "her coding at all. It was scope, and influence. She built beautifully whatever she "
  "was handed. So we mapped that to our senior rubric, so it stopped being a vague "
  "feeling and became a concrete checklist. [pause] Second, I handed her a genuinely "
  "hard, visible project. The idempotency redesign for our payment retries. It touched "
  "three teams, it was high-stakes, and I deliberately stayed out of it. I resisted the "
  "urge to jump in and rescue her. [pause] Third, I coached the how, not the what. In "
  "our weekly one-on-ones, we would rehearse. How to run a design review. How to hold "
  "your ground when a staff engineer pushes back. But in the real meetings, she made "
  "the calls. Including a couple of wrong ones, which she then had to recover from. "
  "That's where the growth actually happened. [pause] And fourth, I created visibility "
  "for her. She presented the final design to the whole org, and I quietly pre-wired "
  "the promotion committee, so her work was already known before her packet even "
  "landed. [pause] The result. She was promoted to senior in eleven months. Her "
  "redesign cut payment retry failures by ninety percent. And today, she mentors three "
  "engineers of her own. [pause] What did I learn? Define the gap in writing on day "
  "one. Vague growth goals grow no one. [pause] And notice the shape of that answer. "
  "Every single action was I did. But it ended on her growth, not mine. That balance "
  "is exactly what they're listening for."),

 # --- Q2 UNDERPERFORMER ---
 ("s08_underperf", "em_q", Q(
   "PEOPLE · PERFORMANCE", "Handling an underperformer",
   "How did you handle an engineer who was underperforming?", YOU,
   [("S", "Diagnose first", "Skill, will, or fit? Each needs a different fix, so don't guess."),
    ("A", "Make it explicit", "Clear expectations, in writing, with dates. No surprises."),
    ("A", "Support, then decide", "Real coaching and a fair runway, then act either way."),
    ("L", "Protect the team", "One tolerated low performer taxes everyone around them.")],
   "“They weren't good enough, so I let them go.” No diagnosis, no support.",
   "You're fair and direct, and you don't avoid hard conversations.",
   "They want to see compassion and a spine. Most candidates show only one."),
  "Next, the underperformer. [pause] The trap is to jump straight to letting them go. "
  "Don't. Diagnose first. Is it a skill problem, a motivation problem, or a fit "
  "problem? [pause] Then make expectations explicit. In writing, with dates. Give "
  "real support and a fair runway. [pause] And then decide, either way. Because one "
  "tolerated low performer quietly taxes the whole team."),

 ("s08s_underperf", "em_story", St(
   "WORKED EXAMPLE · PERFORMANCE", "Turning around an underperformer — a full answer", YOU,
   "On an ads-ranking team, a solid mid-level engineer, David, had missed his commitments for a full quarter. His code reviews were slow and the team had started to notice.",
   "My mandate: turn it around fairly within a quarter, or make a clear call.",
   ["Diagnosed privately first — it wasn't skill. A new baby at home, and he felt his work had gone invisible.",
    "Set explicit written expectations: three concrete deliverables over six weeks, with dates.",
    "Rebalanced his load and gave him a latency project matched to his real strength.",
    "Checked in weekly and documented everything, so there were no surprises for him or me."],
   [("6 weeks", "back to meeting the bar"), ("p99 ↓ 35%", "his latency project"), ("0 surprises", "at his review")],
   "Diagnose before you judge. Most “underperformance” is context, not capacity.",
   "Compassion and a spine in the same story. That's exactly the balance they score."),
  "Here's the story. [pause] The situation. On an ads-ranking team, one of my mid-level "
  "engineers, David, had missed his commitments for an entire quarter. His code reviews "
  "were slow, he'd gone quiet in stand-ups, and the rest of the team was starting to "
  "notice and quietly resent it. [pause] My mandate was to turn it around fairly within "
  "a quarter, or make a clear call. [pause] Now, the easy thing, the lazy thing, is to "
  "decide he's just not good enough and start building a case to let him go. I didn't "
  "do that. [pause] First, I diagnosed before I judged. I sat down with him privately, "
  "and I just asked, genuinely, what's going on. And it turned out it wasn't a skill "
  "problem at all. He had a new baby at home and was running on no sleep. And on top of "
  "that, after a recent reorg, he felt his work had become completely invisible. He'd "
  "checked out because he thought no one cared. [pause] So now I knew it was will and "
  "context, not capacity. And that changes everything about the fix. [pause] Second, I "
  "made expectations explicit anyway. Because empathy is not the same as lowering the "
  "bar. Three concrete deliverables, over six weeks, in writing, with dates. So we both "
  "knew exactly what good looked like. [pause] Third, I gave real support. I rebalanced "
  "his load for a few weeks so he could breathe. And I handed him a latency "
  "optimization project that played directly to his strengths, and that was visible to "
  "leadership, so he could feel like he mattered again. [pause] Fourth, I checked in "
  "every single week, and I documented all of it. If this didn't work and we ended up "
  "parting ways, there would be no surprise for anyone, including him. [pause] The "
  "result. Within six weeks, he was back to meeting the bar. His project cut p "
  "ninety-nine latency by thirty-five percent. And his next review was clean, with zero "
  "surprises. [pause] What I learned. Diagnose before you judge. Most underperformance "
  "is context, not capacity. But you hold the bar the whole way through."),

 # --- Q3 FEEDBACK ---
 ("s09_feedback", "em_q", Q(
   "PEOPLE · FEEDBACK", "Delivering hard feedback",
   "Tell me about a difficult piece of feedback you gave.", YOU,
   [("S", "Pick real stakes", "Choose feedback that was genuinely hard. Behavior, not a typo."),
    ("A", "Specific and kind", "Name the exact behavior and its impact, not their character."),
    ("A", "Make it a dialogue", "Ask for their view; agree on one concrete change together."),
    ("R", "Follow the thread", "Show what changed after. Feedback with no follow-up is venting.")],
   "You picked a trivial example, or softened it until there was no message.",
   "You have the uncomfortable conversation early, before it becomes a crisis.",
   "Candor delivered with care is the single most-tested manager skill."),
  "Now, difficult feedback. [pause] Pick an example with real stakes. A behavior "
  "problem, not a typo. [pause] Be specific and kind. Name the exact behavior and its "
  "impact, never attack their character. Then make it a dialogue. Agree together on one "
  "concrete change. [pause] Finally, follow the thread. Show what actually changed. "
  "Feedback with no follow-up is just venting."),

 ("s09s_feedback", "em_story", St(
   "WORKED EXAMPLE · FEEDBACK", "The brilliant engineer nobody wanted to work with", YOU,
   "I had a staff engineer, Marco — technically the best on the team. But he was condescending in reviews and meetings, and two engineers had quietly asked to transfer off his projects.",
   "My mandate: keep his output, fix the behavior, or I'd lose the rest of the team.",
   ["Gathered specifics first — exact quotes from reviews and meetings, not a vague vibe.",
    "Had a direct, private conversation: named the behavior and its impact on attrition, not his character.",
    "Made it two-way — asked what was driving it; he felt others shipped sloppy work. We agreed on two concrete changes.",
    "Followed up weekly, and deliberately caught him doing it right and reinforced it."],
   [("0 transfers", "both engineers stayed"), ("eNPS +20", "team sentiment"), ("still #1 IC", "output intact")],
   "Talent never excuses a toxic tax. Address it early, and be specific, not general.",
   "Specific, kind, two-way, with follow-up. That's the whole feedback muscle in one story."),
  "This one is about a brilliant engineer that nobody wanted to work with. [pause] The "
  "situation. I had a staff engineer, Marco. Technically, he was the best on the team, "
  "no question. But he was condescending in code reviews and dismissive in meetings. "
  "And it had reached the point where two of my engineers had quietly come to me and "
  "asked to move off his projects. [pause] So my mandate was uncomfortable. Keep his "
  "output, fix the behavior, or I was going to lose the rest of the team around him. "
  "[pause] Here's what I did. [pause] First, I gathered specifics. Because the worst "
  "thing you can do is walk in and say, hey, people find you difficult. That's a vibe, "
  "and it's impossible to act on. So I collected exact examples. Specific comments from "
  "code reviews. A specific moment in a planning meeting. [pause] Second, I had a "
  "direct, private conversation. And I was very careful here. I named the behavior, and "
  "its impact. I actually told him, two people have asked to stop working with you, and "
  "here's the pattern. But I never once attacked his character. It was always the "
  "behavior, and the effect it was having. [pause] Third, I made it two-way. I didn't "
  "just deliver a verdict. I asked him what was driving it. And it was revealing. He "
  "felt like he was the only one holding the quality bar, and that others were shipping "
  "sloppy work. That's real. So we agreed on two concrete changes in how he'd give that "
  "feedback going forward. [pause] Fourth, I followed up every week. And I deliberately "
  "caught him doing it right, and reinforced it, so the new behavior actually stuck. "
  "[pause] The result. Both engineers stayed. Team sentiment jumped twenty points on "
  "our next survey. And Marco remained our strongest engineer, just no longer a tax on "
  "everyone around him. [pause] What I learned. Talent never excuses a toxic tax on the "
  "team. You address it early, and you get specific, because specifics are the only "
  "thing anyone can actually change."),

 # --- Q4 LET GO ---
 ("s10_letgo", "em_q", Q(
   "PEOPLE · THE HARD CALL", "Letting someone go",
   "Tell me about a time you had to let someone go.", YOU,
   [("S", "Own the context", "Briefly: performance or role fit. Never gossip about the person."),
    ("A", "Show the runway", "What you tried first: feedback, a plan, a fair chance."),
    ("A", "Act with dignity", "Decisive, humane, by the book. Protect their exit, not just yours."),
    ("L", "Carry the lesson", "Earlier feedback? A better hire? Show you learned from it.")],
   "You sound cavalier about firing, or you dodged it until HR forced you.",
   "You'll make the hard call, and you'll make it like a human.",
   "They're checking you won't keep a bad situation alive out of fear."),
  "The hardest one. Letting someone go. [pause] Give the context briefly. Performance, "
  "or role fit. Never gossip about the person. [pause] Show the runway. The feedback, "
  "the plan, the fair chance to recover. Then act with dignity. Decisive, humane, by "
  "the book. [pause] And carry the lesson forward."),

 ("s10s_letgo", "em_story", St(
   "WORKED EXAMPLE · THE HARD CALL", "When a good person can't scale with the platform", YOU,
   "I had an engineer, Sam, eight years tenured and genuinely loved by the team. But we'd moved to large-scale distributed systems, his skills hadn't kept up, and he was now blocking projects.",
   "My mandate: resolve it — humanely, and without pretending it wasn't happening.",
   ["Gave honest feedback and a real development plan — training, pairing, a scoped role — over two quarters.",
    "Was explicit about the bar and the risk. No false comfort that things were fine.",
    "When it wasn't closing, I partnered with HR early and arranged a dignified exit with severance and a strong reference.",
    "Protected his dignity — he told the team himself, on his own terms."],
   [("2 quarters", "a fair, real runway"), ("kept his reference", "and his dignity"), ("↑ velocity", "team unblocked")],
   "Kindness is clarity early, not avoidance that ends in a cliff.",
   "You made the call, and you made it like a human. That's exactly the signal."),
  "This is the hardest kind of story to tell well, because it's about letting a good "
  "person go. [pause] The situation. I had an engineer, Sam. Eight years at the "
  "company, deep institutional knowledge, and genuinely loved by the team. But the "
  "platform had changed underneath him. We'd moved to large-scale distributed systems, "
  "and his skills just hadn't kept pace. And now, kindly but truly, he was blocking "
  "projects and slowing the team down. [pause] My mandate was to resolve it. Humanely. "
  "But without pretending it wasn't happening, which is the trap most managers fall "
  "into. [pause] So, first, I gave him honest feedback, and I built a real development "
  "plan. Not a check-the-box formality. Actual training, pairing him with a strong "
  "systems engineer, and a scoped role where he could succeed, over two full quarters. "
  "I genuinely wanted him to make it. [pause] Second, I was explicit about the bar and "
  "the risk. I never gave him false comfort that everything was fine. At every "
  "check-in, he knew exactly where he stood, and what would happen if the gap didn't "
  "close. [pause] Third, when it became clear the plan wasn't working, I didn't drag it "
  "out. I partnered with H R early, and I arranged a dignified exit. Real severance, "
  "and a strong reference, because his eight years of contribution had been real and "
  "deserved to be honored. [pause] And fourth, I protected his dignity on the way out. "
  "We agreed that he would tell the team himself, on his own terms. No awkward "
  "announcement, no rumors. [pause] The result. He got two quarters of a genuinely fair "
  "runway. He left with his reference and his dignity intact. And the team's velocity "
  "recovered because the blocker was gone. [pause] What I learned. Kindness is clarity, "
  "early. It is not avoidance that ends in a cliff for everyone."),

 # ================= PART 2: CONFLICT & INFLUENCE =================
 ("s11_div2", "em_divider", {"n": 2, "title": "Conflict", "sub": "and influence without authority", "color": SIT},
  "Part two. Conflict, and influence. [pause] Can the room get calmer when you walk in?"),

 # --- Q5 CONFLICT ---
 ("s12_conflict", "em_q", Q(
   "CONFLICT · WITHIN THE TEAM", "Two engineers at war",
   "Two of your engineers strongly disagree. What do you do?", SIT,
   [("S", "Get underneath it", "Talk to each privately; find the real interest, not the position."),
    ("A", "Reframe to a shared goal", "Anchor both on the outcome they actually both want."),
    ("A", "Decide if they can't", "Facilitate a decision, and make the call yourself if needed."),
    ("L", "Repair the relationship", "The goal isn't a winner; it's two people who work together tomorrow.")],
   "You took a side, or you let it fester hoping it would resolve itself.",
   "You de-escalate, stay neutral, and can still make a decision.",
   "The test: is the team calmer or tenser after you get involved?"),
  "Conflict between two of your engineers. [pause] First, get underneath it. Meet each "
  "one privately, and find the real interest behind the position. [pause] Then reframe "
  "toward a shared goal. Usually they want the same outcome. [pause] If they still "
  "can't agree, facilitate a decision, and if you must, make the call yourself. But the "
  "goal isn't a winner. It's two people who work together tomorrow."),

 ("s12s_conflict", "em_story", St(
   "WORKED EXAMPLE · CONFLICT", "Two staff engineers, deadlocked for weeks", SIT,
   "Two of my staff engineers had been deadlocked for weeks over a new notifications system — one wanted synchronous, one wanted asynchronous. The team was paralyzed and quietly picking sides.",
   "My mandate: unblock the decision without either of them becoming an enemy.",
   ["Met each privately — the real fears were different: one feared latency, the other feared operational complexity. Both valid.",
    "Reframed around the shared goal in a joint doc: reliability at scale, with the actual requirements written down.",
    "Ran a time-boxed bake-off with success criteria they both signed off on beforehand.",
    "The data pointed to async; I made the final call publicly, and credited both of them by name."],
   [("5 days", "decided, after weeks stuck"), ("both stayed", "no one left angry"), ("99.99%", "the system's uptime")],
   "Conflict is usually two right people optimizing different things. Surface the interest.",
   "Neutral, structured, decisive — and the relationship survived. That's the whole test."),
  "Two staff engineers, at war. [pause] The situation. Two of my most senior engineers "
  "had been deadlocked for weeks over the architecture of a new notifications system. "
  "One wanted it synchronous, one wanted it asynchronous. And it had gotten personal. "
  "The whole team was paralyzed, waiting, and quietly taking sides. It was poisoning "
  "the room. [pause] My mandate was to unblock the decision, without either of them "
  "walking away an enemy. [pause] The tempting thing here is to just pick the smarter "
  "engineer's side and move on. That ends the argument, but it makes a lasting enemy "
  "and it might be the wrong call. So I didn't. [pause] First, I got underneath it. I "
  "met each of them privately. And what I found was that their real fears were "
  "completely different. One was terrified of latency, of making the user wait. The "
  "other was terrified of operational complexity, of getting paged at three in the "
  "morning. And here's the thing. Both of those fears were completely valid. [pause] "
  "Second, I reframed around the shared goal. I got them in a room around a joint doc, "
  "and we wrote down the actual requirement. Reliability at scale. Suddenly the argument "
  "wasn't sync versus async and whose ego wins. It was, what actually meets this bar? "
  "[pause] Third, when they still leaned different ways, I didn't let it drift. I ran a "
  "time-boxed bake-off. A short spike, with real success criteria that both of them "
  "agreed to beforehand. So the data would decide, not volume. [pause] The data pointed "
  "to asynchronous. And I made the final call, publicly, and I credited both of them by "
  "name for pressure-testing it. [pause] The result. Decided in five days, after weeks "
  "of being stuck. Both of them stayed. And that system has since held four nines of "
  "uptime. [pause] What I learned. Conflict is usually two right people optimizing for "
  "different things. Your job is to surface the interest hiding under the position."),

 # --- Q6 DISAGREE UP ---
 ("s13_disagree", "em_q", Q(
   "CONFLICT · MANAGING UP", "Disagreeing with leadership",
   "Tell me about a time you disagreed with your manager.", SIT,
   [("S", "Pick a real one", "Something that mattered, not the color of a button."),
    ("A", "Disagree with data", "Bring evidence and user or business impact, not just opinion."),
    ("A", "Commit once decided", "Say it clearly, then disagree and commit, and mean it."),
    ("L", "Know when you're wrong", "Bonus points if the leader was right, and you say so.")],
   "You were a pushover, or you undermined the decision afterward.",
   "You have a spine, and you can be an adult about losing a call.",
   "They want someone who tells them the truth, then rows in one direction."),
  "Disagreeing with your own manager. [pause] Pick a real disagreement, one that "
  "mattered. Then disagree with data, not opinion. Bring the user or business impact. "
  "[pause] But here's the key. Once the decision is made, commit. Disagree, and commit, "
  "and genuinely mean it. [pause] And if the leader turns out to be right, say so."),

 ("s13s_disagree", "em_story", St(
   "WORKED EXAMPLE · MANAGING UP", "Pushing back on a date that would ship broken", SIT,
   "My director wanted to commit to a hard external launch date for a checkout redesign, tied to a marketing campaign. I believed it was about six weeks too aggressive and would ship broken.",
   "My mandate: push back honestly, without becoming the blocker in the room.",
   ["Didn't argue in the meeting — I came back with data: a bottom-up estimate, the top risk areas, and our QA gap.",
    "Proposed an alternative, not just an objection: a phased rollout that still hit the marketing beat with a smaller scope.",
    "Stated my view clearly once, then said: if we go for the full date, I'm all in. Disagree and commit.",
    "The director chose the phased plan — and I owned the delivery of it."],
   [("hit the date", "phased, not broken"), ("0 P0 bugs", "at launch"), ("+12%", "checkout conversion")],
   "Bring an alternative, not just an objection. And mean the commit.",
   "A spine and professional maturity in one answer — exactly what managing up needs."),
  "Disagreeing with leadership, done right. [pause] The situation. My director wanted to "
  "commit us to a hard external launch date for a checkout redesign. It was tied to a "
  "big marketing campaign, so the date was very public. And I genuinely believed it was "
  "about six weeks too aggressive, and that we would ship something broken and damage "
  "the brand. [pause] My mandate to myself was to push back, honestly and hard, without "
  "becoming the person who just says no in the room. [pause] So here's what I did. "
  "[pause] First, I did not argue in the meeting on instinct and emotion. That never "
  "works upward. Instead, I went away and came back with data. A bottom-up estimate "
  "from the team, the three specific risk areas that scared me, and a clear picture of "
  "our Q A gap. I made it about evidence, not vibes. [pause] Second, and this is the "
  "part most people miss, I brought an alternative, not just an objection. Anyone can "
  "say the date's too soon. I proposed a phased rollout, that still hit the marketing "
  "moment on time, but with a smaller, safer initial scope, and the risky pieces "
  "following two weeks later. Now I was solving his problem, not just blocking it. "
  "[pause] Third, I stated my view clearly, once. And then I said something that "
  "matters. I said, look, this is my honest recommendation, but if you decide we go for "
  "the full launch, I am all in, and I'll make it work. Disagree, and commit. And I "
  "meant it. [pause] In the end, the director chose the phased plan. And I owned "
  "delivering it. [pause] The result. We hit the date, phased instead of broken. Zero P "
  "zero bugs at launch. And checkout conversion went up twelve percent. [pause] What I "
  "learned. Bring an alternative, not just an objection. And when the call is made, "
  "genuinely commit. That combination is how you earn the right to disagree next time."),

 # --- Q7 INFLUENCE ---
 ("s14_influence", "em_q", Q(
   "INFLUENCE · CROSS-TEAM", "Influence without authority",
   "How did you drive a decision across teams you don't own?", SIT,
   [("S", "Name the stakeholders", "Who cared, what they wanted, where incentives clashed."),
    ("A", "Sell the why", "Build a shared narrative plus data, so it becomes their idea too."),
    ("A", "Trade and align", "Find the win-win; give something to get the alignment you need."),
    ("R", "Land it, credit others", "Show the decision shipped, and spread the credit widely.")],
   "You “escalated to your VP.” That's borrowing authority, not influence.",
   "You can move an org through persuasion, the core senior-EM muscle.",
   "The higher the role, the more your power is influence, not your title."),
  "Influence without authority. [pause] Driving a decision across teams you don't "
  "control. Start by naming the stakeholders. Who cared, and where incentives clashed. "
  "[pause] Then sell the why. Build a shared story and the data, so it becomes their "
  "idea too. Trade to align. [pause] And when it lands, spread the credit. Escalating "
  "to your V P is borrowing authority. That's not influence."),

 ("s14s_influence", "em_story", St(
   "WORKED EXAMPLE · INFLUENCE", "Three teams, three feature-flag systems, no authority", SIT,
   "Three teams had each built their own feature-flag system. It was wasteful, inconsistent, and had caused two incidents. Nobody owned consolidation, and I had zero authority over the other two teams.",
   "My mandate — self-assigned: get all three onto one platform.",
   ["Mapped the stakeholders and their incentives — one team cared about speed, one about safety, one about cost.",
    "Built a shared proposal and a small working prototype that solved each team's single biggest pain point.",
    "Traded: I offered to have my team own and staff the platform, if they adopted it.",
    "Landed it in an architecture review, and credited the other teams' input publicly."],
   [("3 → 1", "systems consolidated"), ("↓ 80%", "flag-related incidents"), ("3 teams", "all adopted it")],
   "Influence is finding the win-win, then doing the unglamorous integration work yourself.",
   "You moved an org through persuasion, not your title. That's the senior-EM muscle."),
  "Influence without authority, in practice. [pause] The situation. We had three "
  "different teams that had each, over time, built their own feature-flag system. Three "
  "systems doing basically the same job. It was wasteful, it was inconsistent, and it "
  "had already caused two production incidents where a flag behaved differently than "
  "someone expected. Everyone agreed it was dumb. But nobody owned fixing it. And "
  "critically, I had zero authority over the other two teams. I couldn't just order "
  "them to change. [pause] So I self-assigned the mandate. Get all three onto one "
  "platform. [pause] First, I mapped the stakeholders and their real incentives. And "
  "they were all different. One team's manager cared about shipping speed. One cared "
  "about safety and reliability. And one was under pressure on cost. If I'd walked into "
  "all three with the same generic pitch, I'd have lost two of them immediately. "
  "[pause] Second, I sold the why, tailored to each. I built a shared proposal, and, "
  "importantly, a small working prototype that visibly solved each team's single "
  "biggest pain point. Once they could see their own problem solved, it became their "
  "idea too, not a thing being done to them. [pause] Third, I traded. I offered "
  "something real and concrete. I said, my team will own this platform, we'll staff it, "
  "and we'll carry the on-call, if you adopt it. That dramatically lowered the cost of "
  "saying yes for everyone else. [pause] Fourth, I landed the decision in an "
  "architecture review, and I made a point of crediting the other teams' input out "
  "loud, so nobody felt steamrolled. [pause] The result. Three systems became one. "
  "Flag-related incidents dropped by eighty percent. And all three teams adopted it "
  "willingly. [pause] What I learned. Influence is finding the win-win, and then being "
  "willing to do the unglamorous integration work yourself, so that yes becomes easy "
  "for everyone else."),

 # ================= PART 3: DELIVERY =================
 ("s15_div3", "em_divider", {"n": 3, "title": "Delivery", "sub": "shipping when it's on fire", "color": RES},
  "Part three. Delivery. [pause] Everyone ships late sometimes. What matters is how you "
  "handle it."),

 # --- Q8 DEADLINE ---
 ("s16_deadline", "em_q", Q(
   "DELIVERY · THE SLIP", "A project that missed its deadline",
   "Tell me about a project that slipped or missed a deadline.", RES,
   [("S", "Own it plainly", "No blaming QA, the PM, or “requirements changed.”"),
    ("A", "Detect it early", "How you saw the slip coming and re-planned, not last minute."),
    ("A", "Communicate up early", "You raised the risk and options before it blew up."),
    ("L", "Fix the system", "What you changed so it can't recur: estimation, scope, staffing.")],
   "A blameless story where nothing was your fault and you learned nothing.",
   "You surface bad news early and turn a miss into a durable fix.",
   "How you handle a slip matters more than the slip itself."),
  "The project that slipped. [pause] First, own it plainly. No blaming Q A, the P M, or "
  "shifting requirements. Then show you detected it early, and re-planned. [pause] And "
  "you communicated up early, with risks and options, before it blew up. [pause] "
  "Finally, the systemic fix. What you changed so it can't happen again."),

 ("s16s_deadline", "em_story", St(
   "WORKED EXAMPLE · THE SLIP", "The launch that was going to miss by two months", RES,
   "We'd committed a major search-relevance launch to the org for the third quarter. Six weeks out, a core dependency team slipped, and it was clear we were going to miss badly.",
   "My mandate: recover the situation, not just the date.",
   ["Caught it early — our burn-down stopped adding up, so I flagged it six weeks out, not the week before.",
    "Re-planned with the team: cut two non-critical features and parallelized the critical path.",
    "Communicated up immediately — the risk, the new plan, and the trade-offs — before anyone asked.",
    "Set a weekly exec update so leadership was never surprised again."],
   [("2 weeks late", "not eight"), ("0 surprise", "for leadership"), ("+9%", "search relevance shipped")],
   "The miss is survivable. Hiding it is not. Escalate early, with a plan.",
   "You turned a slip into a controlled, communicated recovery. That's what they want."),
  "A project that missed its deadline. And notice, I'm not going to pretend it was "
  "someone else's fault. [pause] The situation. We had committed a major "
  "search-relevance launch to the whole org, for the third quarter. It was on the "
  "roadmap, leadership was counting on it. Then, about six weeks out, a core dependency "
  "team we relied on slipped their own deadline. And it became clear, pretty quickly, "
  "that we were going to miss, and miss badly. Maybe two months late. [pause] My mandate "
  "was to recover the situation, not just the date. [pause] So, first, the most "
  "important thing. I caught it early. I wasn't looking at a green status report that "
  "suddenly turned red the week before launch. I was watching our burn-down, and when "
  "the math stopped adding up, I flagged it six weeks out. Early detection is the whole "
  "game here. [pause] Second, I re-planned with the team, fast. We went through scope "
  "ruthlessly. We cut two non-critical features that we could add later, and we "
  "re-sequenced the work to parallelize the critical path. We found a way to protect "
  "most of the value. [pause] Third, I communicated up immediately. I did not wait to "
  "be asked, and I did not wait until I had a perfect answer. I went to leadership with "
  "the risk, the new plan, and the honest trade-offs, while there was still time to "
  "react. [pause] Fourth, I set up a weekly executive update for the rest of the "
  "project, so there was full transparency, and leadership was never surprised again. "
  "[pause] The result. We slipped two weeks, not two months. There was zero surprise "
  "for leadership, which protected trust. And the launch still moved search relevance "
  "up nine percent. [pause] What I learned. The miss itself is almost always "
  "survivable. Hiding it is not. Escalate early, and always walk in with a plan, not "
  "just a problem."),

 # --- Q9 TRADEOFF ---
 ("s17_tradeoff", "em_q", Q(
   "DELIVERY · PRIORITIES", "A hard trade-off, or saying no",
   "Tell me about a hard trade-off, or a time you said no.", RES,
   [("S", "Frame the tension", "Speed versus quality; a feature versus paying down debt."),
    ("A", "Make criteria explicit", "Decide on principles and data, not the loudest voice."),
    ("A", "Say no with a reason", "Decline clearly, explain the why, offer an alternative."),
    ("R", "Stand by it", "Show the outcome, and that you'd defend the call again.")],
   "You tried to please everyone, so nothing was actually prioritized.",
   "You can prioritize under pressure and hold the line when it's right.",
   "Managers who can't say no ship blurry roadmaps and burned-out teams."),
  "The hard trade-off. [pause] Frame the tension clearly. Speed versus quality. A "
  "feature versus paying down debt. Then make your criteria explicit. Principles and "
  "data, not whoever is loudest. [pause] When you say no, say it clearly, explain the "
  "reasoning, and offer an alternative. Then stand by it."),

 ("s17s_tradeoff", "em_story", St(
   "WORKED EXAMPLE · PRIORITIES", "Saying no to the biggest customer", RES,
   "Our largest enterprise customer demanded a custom reporting feature, and sales was pushing hard. Meanwhile, reliability debt had caused three incidents that quarter and was threatening our SLA.",
   "My mandate: decide where the team's next quarter actually goes.",
   ["Made the criteria explicit — I laid out the cost of the incidents in churn risk versus the value of one deal.",
    "Took it to data: one customer's request, versus SLA breaches affecting hundreds of accounts.",
    "Said no to the custom feature, clearly, with the reasoning — and offered a lighter alternative on the standard roadmap.",
    "Held the line with sales and my VP, and put the quarter on reliability."],
   [("3 → 0", "incidents that quarter"), ("99.95%", "SLA restored"), ("kept them", "the customer stayed")],
   "Saying no with a reason and an alternative builds more trust than a reluctant yes.",
   "You prioritized under real pressure and held the line. That's the judgment they test."),
  "A hard trade-off. Specifically, saying no to our biggest customer. [pause] The "
  "situation. Our single largest enterprise customer was demanding a custom reporting "
  "feature. And sales was pushing incredibly hard for it, because this was a renewal "
  "worth a lot of money. At the exact same time, we had reliability debt that had "
  "already caused three incidents that quarter, and was genuinely threatening our S L A "
  "across the entire customer base. [pause] My mandate was to decide where my team's "
  "next quarter actually went. One team, one quarter, two things pulling hard in "
  "opposite directions. [pause] The weak move here is to try to do a bit of both, "
  "please everyone, and end up doing neither well. I didn't. [pause] First, I made the "
  "criteria explicit. I didn't argue based on who was loudest, and sales was very loud. "
  "I laid out the real cost. What do these ongoing incidents cost us in churn risk "
  "across our whole base, versus the value of this one deal? [pause] Second, I took it "
  "to data. And framed that way, it wasn't close. One customer's custom request, versus "
  "S L A breaches affecting hundreds of accounts. The reliability work protected far "
  "more revenue. [pause] Third, I said no to the custom feature. Clearly. Not a vague "
  "maybe-next-quarter. A clear no, with the reasoning laid out. And crucially, I offered "
  "an alternative. A lighter version of what they needed that was already on our "
  "standard roadmap. [pause] Fourth, I held the line. With sales, and with my own V P, "
  "who was feeling the pressure. And I put the quarter on reliability. [pause] The "
  "result. Incidents went from three to zero. We restored our S L A to ninety-nine "
  "point nine five percent. And we kept that big customer anyway, because rock-solid "
  "reliability turned out to be what they actually needed. [pause] What I learned. "
  "Saying no, with a clear reason and a real alternative, builds far more trust than a "
  "reluctant, resentful yes."),

 # --- Q10 INCIDENT ---
 ("s18_incident", "em_q", Q(
   "DELIVERY · CRISIS", "Leading through an incident",
   "Walk me through a major outage you led through.", RES,
   [("S", "Set the stakes fast", "Impact in one line: users, revenue, duration. Then move on."),
    ("A", "Lead calm, coordinate", "You ran the response, roles and comms, not solo heroics."),
    ("A", "Communicate outward", "Honest, frequent updates to stakeholders during the fire."),
    ("L", "Blameless postmortem", "The real leadership: the fix that makes a repeat impossible.")],
   "You personally fixed it at 3am. Heroic, but you led no one.",
   "You're the calm center in a crisis, and you build systems, not patches.",
   "In an incident they watch one thing: does the room calm down when you speak?"),
  "A major outage. [pause] Set the stakes fast. Impact in one line. Users, revenue, "
  "duration. Then move on. The core is this. You led the response. Roles and "
  "communication. You didn't just hero-debug it alone. [pause] Keep stakeholders "
  "updated honestly. And the real signal, the blameless postmortem, and the fix that "
  "makes a repeat impossible."),

 ("s18s_incident", "em_story", St(
   "WORKED EXAMPLE · CRISIS", "Checkout down on Black Friday", RES,
   "On Black Friday, checkout started failing. A payment-provider integration degraded, and about fifteen percent of transactions were erroring. We were bleeding revenue by the minute.",
   "My mandate: lead the response — as the manager, not the debugger.",
   ["Set stakes and structure fast — declared a Sev-1, took incident-commander, assigned a comms lead and a debug lead. I did not touch the code.",
    "Ran one clear channel and updated stakeholders honestly every fifteen minutes.",
    "We failed over to the backup provider within forty minutes to stop the bleeding, then root-caused calmly.",
    "Ran a blameless postmortem; the durable fix was an automatic circuit-breaker and failover."],
   [("40 min", "to full mitigation"), ("auto-failover", "shipped the next week"), ("0 repeats", "since")],
   "In a crisis, your job is to coordinate and communicate — not to be the hero.",
   "Calm center, honest comms, systemic fix. That's the leadership they're scanning for."),
  "Leading through a crisis. This one is checkout going down on Black Friday. [pause] "
  "The situation. On our single biggest revenue day of the year, checkout started "
  "failing. One of our payment-provider integrations degraded, and suddenly about "
  "fifteen percent of all transactions were erroring out. We were, very literally, "
  "bleeding revenue by the minute, and the whole company knew it. [pause] My mandate "
  "was to lead the response. And the key phrase there is lead. As the manager, not as "
  "the best debugger in the room. [pause] So, first, I set stakes and structure, fast. "
  "I declared a sev-one. I took the incident-commander role. And I explicitly assigned "
  "a communications lead and a debugging lead. And here is the most important thing I "
  "did. I did not dive into the code myself. Every fiber of my engineer brain wanted "
  "to. But my job in that moment was to run the room, not the terminal. [pause] Second, "
  "I ran one single, clear channel, and I updated stakeholders honestly, every fifteen "
  "minutes. Even when the update was, we still don't know. Predictable, honest comms is "
  "what keeps a panicking organization calm. [pause] Third, we made a call to stop the "
  "bleeding before we fully understood the root cause. We failed over to our backup "
  "payment provider within about forty minutes. That stopped the revenue loss. Then we "
  "could root-cause calmly, without the clock screaming at us. [pause] And fourth, "
  "afterward, the real leadership. We ran a blameless postmortem. No finger-pointing. "
  "And the durable fix was an automatic circuit-breaker and failover, so that a single "
  "provider degrading could never take down checkout like that again. [pause] The "
  "result. Full mitigation in forty minutes. The automated failover shipped the "
  "following week. And we've had zero repeats since. [pause] What I learned. In a "
  "crisis, your job as a manager is to coordinate and communicate. Not to be the hero "
  "who fixes it alone."),

 # ================= PART 4: SCALE, STRATEGY & SELF =================
 ("s19_div4", "em_divider", {"n": 4, "title": "Scale & Self", "sub": "the senior-EM bar", "color": META},
  "Part four. Scale, strategy, and self-awareness. [pause] This is the senior manager "
  "bar, where you lead beyond a single team."),

 # --- Q11 SCALING ---
 ("s20_scaling", "em_q", Q(
   "SCALE · TEAM BUILDING", "Building and scaling a team",
   "Tell me about a time you built or scaled a team.", META,
   [("A", "Hire to a bar", "Define the bar and raise it. Who you said no to, not just yes."),
    ("A", "Build for diversity", "Widen the funnel and structure interviews to reduce bias."),
    ("A", "Onboard for impact", "How new hires reached real output fast, ramp not sink-or-swim."),
    ("R", "Show the health", "Retention, velocity, promotions. The team outlived the hiring.")],
   "“I hired ten people.” Headcount is not a skill; the bar is.",
   "You build durable teams, not just bigger ones.",
   "Senior signal: you scale the org, and the quality bar goes up, not down."),
  "Building and scaling a team. [pause] Don't just say you hired ten people. Headcount "
  "isn't a skill. Talk about hiring to a bar, and raising it. Mention who you said no "
  "to. [pause] Talk about building for diversity, and structuring interviews to reduce "
  "bias. And onboarding people to real impact fast. [pause] Then prove the team was "
  "healthy. Retention, velocity, promotions."),

 ("s20s_scaling", "em_story", St(
   "WORKED EXAMPLE · TEAM BUILDING", "From four engineers to twenty in a year", META,
   "We got funding to grow a new infrastructure team from four engineers to twenty in a year. I owned the hiring bar and the culture, under real pressure to just fill seats fast.",
   "My mandate: scale fast without dropping the bar or building a monoculture.",
   ["Defined the bar explicitly and trained every interviewer — and I personally reviewed the rejections, not just the offers.",
    "Widened the funnel deliberately: partnered with programs for underrepresented candidates and used structured interviews to cut bias.",
    "Built real onboarding — a 30-60-90 plan and a buddy — so new hires shipped in weeks, not months.",
    "Protected the culture with explicit values and fast, early feedback for every new hire."],
   [("4 → 19", "in twelve months"), ("40%", "from underrepresented groups"), ("92%", "one-year retention")],
   "Headcount is easy. A high bar and a healthy culture at speed is the actual job.",
   "You scaled the org and the bar went up, not down. That's the senior signal."),
  "Building and scaling a team, for real. [pause] The situation. We secured funding to "
  "grow a brand-new infrastructure team from four engineers to twenty, inside of a "
  "year. And I owned both the hiring bar and the culture. And there was enormous "
  "pressure, from above, to just fill the seats fast, because the roadmap was waiting. "
  "[pause] My mandate, as I defined it, was to scale fast without dropping the bar, and "
  "without accidentally building a monoculture of people who all looked and thought the "
  "same. [pause] Now, the weak answer to this question is just, I hired sixteen people. "
  "Headcount is not a skill. So here's what I actually did. [pause] First, I defined "
  "the bar explicitly, wrote it down, and trained every single interviewer on it. And "
  "here's the tell that I took it seriously. I personally reviewed the rejections, not "
  "just the offers. Because that's the only way you catch the bar quietly drifting down "
  "under deadline pressure. [pause] Second, I widened the funnel deliberately. I did "
  "not want twenty clones. We partnered with programs for underrepresented candidates, "
  "and we moved to structured interviews, same questions, same rubric, to cut "
  "unconscious bias out of the process. [pause] Third, I built real onboarding, because "
  "hiring fast is worthless if people flounder for six months. Every new hire got a "
  "thirty-sixty-ninety day plan and a dedicated buddy, so they were shipping real work "
  "in weeks, not months. [pause] And fourth, I protected the culture actively, with a "
  "short set of explicit values, and fast, early feedback so small problems never "
  "calcified. [pause] The result. We went from four to nineteen engineers in twelve "
  "months. Forty percent of the new hires came from underrepresented groups. And a full "
  "year later, retention was ninety-two percent, which tells you the culture actually "
  "held. [pause] What I learned. Headcount is easy. Maintaining a high bar and a "
  "healthy culture, at speed, is the actual job."),

 # --- Q12 AMBIGUITY ---
 ("s21_ambiguity", "em_q", Q(
   "STRATEGY · AMBIGUITY", "Acting with no direction",
   "Tell me about a time you acted with no clear direction.", META,
   [("S", "Name the fog", "No spec, no owner, unclear goal. Be honest about the ambiguity."),
    ("A", "Create the clarity", "You wrote the doc, set the goal, drew the line to follow."),
    ("A", "Make a reversible bet", "Pick a direction, ship small, learn. Don't wait for permission."),
    ("L", "Bring people with you", "You aligned the team around the clarity you manufactured.")],
   "You waited for someone above you to tell you what to do.",
   "You generate direction instead of consuming it. The leap into leadership.",
   "The more senior the role, the more the job IS the ambiguity."),
  "Acting with no clear direction. [pause] This separates leaders from strong "
  "individual contributors. Name the fog honestly. No spec, no owner, unclear goal. "
  "[pause] Then create the clarity yourself. Write the doc. Set the goal. Make a "
  "reversible bet. Ship something small, and learn. [pause] Don't wait for permission. "
  "Leaders generate direction. They don't just consume it."),

 ("s21s_ambiguity", "em_story", St(
   "WORKED EXAMPLE · AMBIGUITY", "“Developer productivity is too low” — go fix it", META,
   "My VP said, “developer productivity is too low,” and handed it to me. No spec, no metric, no team. Just a vague, politically charged problem and an expectation that I'd figure it out.",
   "My mandate: turn a complaint into an actual direction.",
   ["Named the ambiguity and created clarity — I interviewed thirty engineers and instrumented our build and CI pipeline to find the real bottlenecks.",
    "Wrote a one-page strategy with a single north-star metric: time from commit to production.",
    "Made a reversible bet — started with the biggest bottleneck, flaky tests, and shipped a fix in three weeks to show a win.",
    "Aligned the org around the one-pager and pulled together a small team to go further."],
   [("3 days → 8 hrs", "commit to production"), ("↓ 70%", "flaky test failures"), ("org-wide", "the metric was adopted")],
   "Leaders manufacture direction out of ambiguity instead of waiting for a spec.",
   "You generated direction where there was none. That's the leap into real leadership."),
  "Acting with total ambiguity, with no direction at all. [pause] The situation. My V P "
  "walked into my one-on-one and said, quote, developer productivity is too low, fix "
  "it. And that was it. No spec. No metric. No definition of what productivity even "
  "meant. No dedicated team. Just a vague, politically charged complaint, and a clear "
  "expectation that I would go figure it out. [pause] My mandate, which I had to define "
  "for myself, was to turn that complaint into an actual, concrete direction. [pause] "
  "And this is the moment that separates a leader from a strong individual contributor. "
  "The IC waits for the ambiguity to be resolved by someone above them. The leader "
  "resolves it. [pause] So, first, I named the ambiguity honestly, and then I went and "
  "created clarity myself. I interviewed about thirty engineers across the org, and I "
  "instrumented our build and C I pipeline, so I could see where the time was actually "
  "going, with data instead of anecdotes. [pause] Second, I wrote a one-page strategy. "
  "One page, on purpose, so people would actually read it. And in it, I proposed a "
  "single north-star metric. Time from commit to production. Now, suddenly, this fuzzy "
  "complaint was a number we could move. [pause] Third, I made a reversible bet. I did "
  "not try to boil the ocean and fix everything at once. The data showed the single "
  "biggest bottleneck was flaky tests. So I started there, and shipped a fix in three "
  "weeks, to get a visible, early win that built belief. [pause] And fourth, I brought "
  "people with me. I aligned the org around that one-pager, and used the early win to "
  "pull together a small, funded team to go further. [pause] The result. Time from "
  "commit to production dropped from three days to eight hours. Flaky test failures fell "
  "seventy percent. And that north-star metric got adopted across the whole "
  "organization. [pause] What I learned. Leaders manufacture direction out of "
  "ambiguity. They do not sit and wait for a spec to arrive."),

 # --- Q13 FAILURE ---
 ("s22_failure", "em_q", Q(
   "SELF · THE MATURITY TEST", "Your biggest failure",
   "What's the biggest failure of your career?", META,
   [("S", "Pick a real one", "A genuine failure with real cost, not “I work too hard.”"),
    ("A", "Own your part fully", "Your decisions and their consequences. Don't diffuse blame."),
    ("L", "Extract the lesson", "The specific principle you now operate by because of it."),
    ("R", "Prove it changed you", "A later time you did it differently, and it worked.")],
   "A humblebrag disguised as a failure. Interviewers spot it instantly.",
   "You're self-aware, accountable, and you genuinely learn.",
   "This is the most important story you'll tell. Have a real one."),
  "The most important question. Your biggest failure. [pause] Please, don't give a "
  "humblebrag like I care too much. They see through it instantly. Pick a real "
  "failure, with real cost. [pause] Own your part fully, without diffusing the blame. "
  "Then extract the lesson. And prove it changed you, with a later story where you did "
  "it differently, and it worked."),

 ("s22s_failure", "em_story", St(
   "WORKED EXAMPLE · THE MATURITY TEST", "The person I kept too long", META,
   "Early as a manager, I had an engineer who was quietly underperforming. I liked him, so I gave him “one more quarter” — three times, across a whole year. This is a real mistake I own.",
   "The honest version: I avoided a hard conversation and told myself it was kindness.",
   ["Own it plainly: I dodged the hard conversation because it was uncomfortable, and I dressed it up as being kind.",
    "The real cost: two of my strongest engineers burned out covering for him, and one of them left the company.",
    "The lesson: tolerating underperformance isn't kindness to anyone — it's a tax on your best people.",
    "How I changed: the next time, I gave clear feedback and a firm 60-day plan in week one, and acted when it didn't close."],
   [("1 great engineer", "lost — that's on me"), ("60 days", "my rule now, not a year"), ("changed", "how I manage")],
   "Avoiding a hard conversation is a decision — and it's usually the wrong one.",
   "A real failure, fully owned, with proof you changed. That's the maturity test, passed."),
  "And here is the most important story you will ever tell in one of these interviews. "
  "Your biggest failure. So let me actually give you a real one, told the right way. "
  "[pause] The situation. Early in my management career, I had an engineer on my team "
  "who was quietly underperforming. Not dramatically. Just consistently below the bar. "
  "And here's the human part. I liked him. He was a good person, everyone liked him. So "
  "I gave him one more quarter to turn it around. And then, when that quarter came and "
  "went, I gave him another. And another. Three times, across a full year. [pause] Now "
  "let me be completely honest about what that actually was, because the whole point of "
  "this answer is honesty. I was avoiding a hard conversation because it was "
  "uncomfortable for me. And I dressed it up in my own head as being kind and patient. "
  "[pause] I own that completely. It was my decision, repeated, and it was a mistake. "
  "[pause] And here's the real cost, which is the part that still stings. While I was "
  "protecting him, two of my strongest engineers were quietly picking up his slack. "
  "They burned out. And one of them, someone I genuinely valued and wanted to keep for "
  "years, left the company. [pause] So in trying to be kind to one struggling person, I "
  "damaged the whole team, and I lost a great one. [pause] The lesson I took from that, "
  "and now operate by every day. Tolerating underperformance is not kindness to "
  "anyone. It is a tax you levy on your very best people. [pause] And I proved that I "
  "learned it. The very next time I faced a similar situation, I gave clear, direct "
  "feedback and a firm sixty-day plan in the very first week. And when it didn't close, "
  "I acted, with compassion, but I acted. [pause] What I learned, in one line. Avoiding "
  "a hard conversation is itself a decision. And it is almost always the wrong one. "
  "[pause] That is the answer that shows an interviewer you are actually ready to lead."),

 # ================= CLOSE =================
 ("s23_signals", "em_signals", {},
  "So what are they actually scoring? [pause] Not the story itself, but five things "
  "underneath it. [pause] Ownership. Did you drive it? People judgment. Did you treat "
  "humans as humans? Structured thinking. Was there a clear spine? [pause] Measurable "
  "impact. Was there a number, not a vibe? And self-awareness. What would you do "
  "differently? [pause] Every answer you give either earns or loses points on these five."),

 ("s24_redflags", "em_redflags", {},
  "Now the instant credibility killers. [pause] Blaming your team. You're the manager, "
  "so where were you? Being the lone hero who developed no one. A story that just ends, "
  "with no outcome. [pause] Saying only we, with no I. Learning nothing, so you didn't "
  "grow. And the five minute ramble with no structure. [pause] If your best story "
  "contains one of these, pick a different story."),

 ("s25_matrix", "em_matrix", {},
  "Here's how to prepare efficiently. [pause] Don't memorize fifty answers. Build a "
  "story matrix. [pause] Down the side, your best real stories. Across the top, the "
  "question categories. People, conflict, delivery, failure. [pause] A great story "
  "answers four different questions from four different angles. [pause] You only need "
  "twelve to fifteen. In the room, you're not remembering. You're just picking a column."),

 ("s26_recap", "em_recap",
  {"items": [
     "It's one question: how do you lead when it's hard?",
     "Structure every answer with STAR, plus the Learning.",
     "Say “I” for your decisions; give the team the credit.",
     "Two sentences of context, then live in the Action.",
     "End on a measurable result, and what you learned.",
     "Prep 12 to 15 real stories in a category matrix.",
   ],
   "closer": "They're not testing what you did. They're testing how you think."},
  "Let's put it all together. [pause] It's really one question. How do you lead when "
  "it's hard? Structure every answer with STAR, plus the learning. Say I for your "
  "decisions, and give your team the credit. [pause] Keep context short, and live in "
  "the action. End on a real result, and what you learned. And prepare twelve to "
  "fifteen stories in a matrix. [pause] And one more thing. The example stories in this "
  "video are templates. Take them, and rewrite each one with your own real experience. "
  "Your genuine story, told in this structure, always beats a polished fake. [pause] "
  "Because in the end, they're not testing what you did. They're testing how you "
  "think. [pause] Good luck. Thanks for watching."),
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
         "audio": {"narration": {"src": f"{PREFIX}/narration.wav", "volume": 1.0}}}
json.dump(props, open(os.path.join(ROOT, "artifacts", "edit_decisions.json"), "w"), indent=2)
words = sum(len(x[3].replace("[pause]", "").split()) for x in SEGMENTS)
print(f"total {t - GAP:.2f}s ({(t-GAP)/60:.2f} min), {len(cuts)} scenes, {words} words, NO captions, NO music")
