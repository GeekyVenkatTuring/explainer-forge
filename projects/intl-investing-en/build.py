#!/usr/bin/env python3
"""How to invest in international (US) stock markets FROM INDIA (English, Nova). Prefix `gw`,
scene set GWScenes.tsx. India-context investor education — read skills/12-market-research.md §5.

VERIFIED NUMBERS TABLE (pre-render gate, skill 12 rule 7) — rules confirmed 4 Aug 2026:
  • LRS (RBI Liberalised Remittance Scheme): up to US$250,000 per PERSON per FINANCIAL YEAR.
        [RBI LRS; ClearTax; HDFC Sky — all agree]
  • TCS on LRS for INVESTMENT: 20% on the amount ABOVE ₹10 lakh/FY (first ₹10L exempt);
        threshold raised ₹7L→₹10L by Finance Act 2025 (eff 1 Apr 2025). TCS is REFUNDABLE /
        adjustable against income-tax in the ITR. [ClearTax fetch, verbatim; PKC; Bajaj Finserv]
        (One search returned a stale "5%" — REJECTED after triangulating a 3rd source.)
  • US DIVIDENDS: 25% withheld at source for Indian investors; claim Foreign Tax Credit under
        the India-US DTAA so it isn't taxed twice. [INDmoney; Winvesta; Vested]
  • CAPITAL GAINS on US stocks for a resident Indian: taxed ONLY in India (US doesn't tax
        NRA capital gains). LTCG (held >24 months) = 12.5% without indexation; STCG (≤24 months)
        = income-tax slab. [INDmoney; Winvesta; CABlogs — 2026 rules]
  • Schedule FA: MANDATORY disclosure of ALL foreign holdings in the ITR (even 1 fractional
        share, even with no gains). [multiple]
  • Platforms (direct): INDmoney, Vested, Groww (fintech apps — partner a US broker, ₹→$,
        fractional, mostly ₹0 brokerage); Interactive Brokers (~$0.005/share, min $1/order);
        ICICI Direct Global (+ Kotak/HDFC/Axis tie-ups); GIFT City / NSE IFSC route.
        Platform fees change — narration says "check live pricing"; figures are illustrative.
  • Indirect (no LRS, in ₹): India-listed international MFs / FoFs + ETFs tracking S&P 500 /
        Nasdaq 100 — subject to SEBI overseas-investment limits (funds can pause fresh inflows).

  Education only — NOT investment advice (disclaimer in narration recap + description).

Voice: Kokoro "Nova" (Voicebox, English). Usage: python3 build.py
"""
import json, os, subprocess, time, urllib.request

BASE = "http://127.0.0.1:17493"
PROFILE = "c488e05c-3407-46a3-874d-1b09b3aff78d"  # "TTS Bright (Nova)"
GAP = 0.5
PAUSE = 0.6
ATEMPO = 0.95
PREFIX = "gw"
ROOT = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(ROOT, "..", ".."))
PUBLIC = os.path.join(REPO, "composer", "public", PREFIX)
RAW = os.path.join(ROOT, "assets", "raw")
FIN = os.path.join(ROOT, "assets")
for d in (PUBLIC, RAW, os.path.join(ROOT, "artifacts"), os.path.join(ROOT, "renders")):
    os.makedirs(d, exist_ok=True)

INR, USD, COST, TAX, OK = "#F59E0B", "#4F86F7", "#FB7185", "#A78BFA", "#34D399"

DISCLAIMER = ("And one final, important note. [pause] This video is education, not investment "
    "advice. It is not a recommendation to buy any stock, platform, or fund. Rules, tax rates and "
    "platform fees change — always check the current numbers and, for your own taxes, consult a "
    "SEBI-registered advisor or a chartered accountant. Thanks for watching.")

# ---------------------------------------------------------------- SCREENPLAY
SEGMENTS = [

 # ===== PART 1 — Is it even possible? =====
 ("gw01_title", "gw_title", {},
  "You've heard the names — Apple, Nvidia, Google, the S and P five hundred. [pause] But sitting "
  "here in India, can you actually own them? And if you can — how, through whom, and at what cost? "
  "[pause] Let's answer all of it, end to end. This is education, not investment advice."),

 ("gw02_routes", "gw_routes", {
    "kicker": "TWO DOORS", "title": "First — yes, it's absolutely possible",
    "left": {"label": "Direct", "sub": "you own the actual US shares",
             "items": ["Send rupees abroad under LRS", "Buy real US stocks — even fractions", "Via apps like INDmoney, Vested, IBKR"]},
    "right": {"label": "Indirect", "sub": "invest in rupees, from India",
              "items": ["No dollars leave the country", "India-listed ETFs and mutual funds", "They hold the US stocks for you"]},
  },
  "So, is it even legal from India? [pause] Yes — completely. And there are two doors in. [pause] "
  "The first is the direct route: you send your rupees abroad and buy the actual American shares, "
  "in your own name. [pause] The second is the indirect route: you never move a dollar. You buy an "
  "Indian mutual fund or an exchange-traded fund, in rupees, and it holds the US stocks for you. "
  "[pause] Both are legal, both are easy. We'll cover the direct route in depth, then come back to "
  "the indirect one. Let's start with how the money actually travels."),

 ("gw03_pipe", "gw_pipe", {},
  "Here's the part most people don't understand — how your rupees legally reach Wall Street. [pause] "
  "It runs on a rule from the Reserve Bank of India called the Liberalised Remittance Scheme, or "
  "L-R-S. [pause] It works like a pipeline. You start with rupees in your Indian bank. When you add "
  "money on a US-investing platform, your bank sends it abroad through the L-R-S gateway. [pause] At "
  "that gateway, two things happen — your rupees are converted into dollars, and the transfer is "
  "recorded against your yearly limit. [pause] Those dollars land in a US brokerage account that is "
  "yours, held in your name. And from there, you buy shares. [pause] The key idea — this is a fully "
  "legal, RBI-sanctioned path. You're not doing anything grey. You're using a scheme built exactly "
  "for this."),

 ("gw04_stats", "gw_stats", {
    "kicker": "THE LEGAL FRAME", "title": "The one limit you must know", "color": USD,
    "stats": [
      {"label": "You can send abroad each year", "to": 250000, "prefix": "$", "color": USD, "sub": "the LRS limit — per person"},
      {"label": "Minimum to start (many apps)", "to": 1, "prefix": "$", "color": OK, "sub": "fractional shares — buy a slice"},
      {"label": "US stocks & ETFs you can buy", "to": 5000, "prefix": "", "suffix": "+", "color": INR, "sub": "from your phone, in India"},
    ],
    "note": "No special RBI permission is needed — LRS is automatic up to $250,000 a year, across ALL your foreign spending combined.",
  },
  "Under L-R-S, there's really just one number you must remember. [pause] You can send up to two "
  "hundred and fifty thousand dollars abroad every financial year — that's per person. For almost "
  "every retail investor, that's far more headroom than you'll ever use. [pause] And you don't need "
  "any special approval; it's automatic. [pause] On the other end, the barrier to entry is tiny. "
  "Because these platforms allow fractional shares, you can start with as little as a dollar and "
  "still own a slice of a five-hundred-dollar stock. [pause] So: a huge annual ceiling, and a "
  "one-dollar floor. Access is not the problem. Choosing well is."),

 # ===== PART 2 — The platforms =====
 ("gw05_div2", "gw_divider", {"n": 2, "title": "Which Platforms?", "sub": "Where you actually open an account and buy", "color": USD},
  "Part two — the platforms. [pause] Where do you actually open an account, and who lets you buy?"),

 ("gw06_cards", "gw_cards", {
    "kicker": "ROUTE A · INDIAN APPS", "title": "The easy on-ramp: Indian fintech apps", "color": USD,
    "items": [
      {"emoji": "📱", "k": "INDmoney", "v": "A popular super-app — US stocks with zero brokerage and fractional investing built in", "chip": "₹0 BROKERAGE"},
      {"emoji": "🦺", "k": "Vested", "v": "A US-stocks specialist; start from about a dollar, with ready-made portfolios", "chip": "FROM ~$1"},
      {"emoji": "🌱", "k": "Groww", "v": "The familiar Indian investing app now offers US stocks and ETFs too", "chip": "EASY START"},
      {"emoji": "🤝", "k": "What they share", "v": "Each partners with a US broker, does the rupee-to-dollar conversion, and allows fractions", "chip": "BEGINNER-FRIENDLY"},
    ],
  },
  "The easiest way in is an Indian app you may already know. [pause] INDmoney is a popular "
  "financial super-app that offers US stocks with zero brokerage and fractional shares. [pause] "
  "Vested is a specialist built just for US investing — you can start with about a dollar and even "
  "buy ready-made baskets. [pause] Groww, the familiar Indian app, now offers US stocks and E-T-Fs "
  "as well. [pause] What they all have in common is the important bit: behind the scenes each one "
  "partners with a US broker, quietly handles your rupee-to-dollar conversion, and lets you buy "
  "fractions. For a beginner, this is the smoothest on-ramp there is."),

 ("gw07_cards", "gw_cards", {
    "kicker": "ROUTE B · GLOBAL & FULL-SERVICE", "title": "For bigger or more serious investors", "color": USD,
    "items": [
      {"emoji": "🌐", "k": "Interactive Brokers", "v": "A global broker you join directly — the lowest costs and pro tools, best for serious money", "chip": "PRO · LOW-COST"},
      {"emoji": "🏦", "k": "ICICI Direct Global", "v": "Full-service Indian brokers offer US investing via tie-ups — also Kotak, HDFC and Axis", "chip": "BANK-BACKED"},
      {"emoji": "🏙️", "k": "GIFT City route", "v": "Buy select US stocks from India's own GIFT City, or NSE IFSC — a newer LRS pathway", "chip": "GIFT CITY"},
      {"emoji": "🧭", "k": "Rule of thumb", "v": "New with small sums? Use an Indian app. Large sums or active trading? Go global", "chip": "HOW TO CHOOSE"},
    ],
  },
  "If you're investing larger sums, or want more control, there's a second tier. [pause] Interactive "
  "Brokers is a giant global brokerage you can join directly. It has the lowest costs and the most "
  "powerful tools — but it's built for more serious investors. [pause] Then there are the "
  "full-service Indian brokers — I-C-I-C-I Direct Global, and tie-ups from Kotak, H-D-F-C and Axis "
  "— which bolt US investing onto an account you may already have. [pause] And there's a newer path "
  "through India's own Gift City, which lets you buy select US stocks under L-R-S from within India. "
  "[pause] The rule of thumb — small and new, start with an app; large or active, go global."),

 ("gw08_compare", "gw_compare", {
    "kicker": "PLATFORMS · SIDE BY SIDE", "title": "How three popular choices compare", "color": USD,
    "cols": [
      {"name": "INDmoney", "color": USD, "emoji": "📱", "rows": [
        {"k": "BROKERAGE", "v": "Zero on US stocks"},
        {"k": "MINIMUM", "v": "Fractional — a few $"},
        {"k": "BEST FOR", "v": "All-in-one beginners"},
        {"k": "WATCH", "v": "Withdrawal & FX fees"},
      ]},
      {"name": "Vested", "color": OK, "emoji": "🦺", "rows": [
        {"k": "BROKERAGE", "v": "Zero commission"},
        {"k": "MINIMUM", "v": "From about $1"},
        {"k": "BEST FOR", "v": "US-stocks focus"},
        {"k": "WATCH", "v": "Withdrawal fee"},
      ]},
      {"name": "Interactive Brokers", "color": INR, "emoji": "🌐", "hi": True, "rows": [
        {"k": "BROKERAGE", "v": "~$0.005 per share"},
        {"k": "MINIMUM", "v": "Low; fractional too"},
        {"k": "BEST FOR", "v": "Large / active money"},
        {"k": "WATCH", "v": "Steeper learning curve"},
      ]},
    ],
  },
  "Let's put three popular choices side by side. [pause] INDmoney and Vested both charge zero "
  "brokerage on US stocks and let you start with just a few dollars, which makes them ideal for "
  "beginners. INDmoney is more of an all-in-one money app; Vested is laser-focused on US investing. "
  "[pause] Interactive Brokers charges a tiny per-share fee — around half a cent — but gives you "
  "professional tools and the deepest access, so it suits larger or more active investors. [pause] "
  "One honest caveat — these fees change often. Always check a platform's live pricing page before "
  "you commit. The right pick depends on your size and your style."),

 # ===== PART 3 — The costs =====
 ("gw09_div3", "gw_divider", {"n": 3, "title": "What Does It Cost?", "sub": "Every charge, from buying to bringing money home", "color": COST},
  "Part three — the costs. [pause] This is where people get surprised, so let's follow the money "
  "carefully, from buying all the way to bringing it home."),

 ("gw10_fees", "gw_fees", {},
  "Let's make it concrete. Say you invest one lakh rupees. What actually reaches your US stocks? "
  "[pause] First, the big one — the forex markup. Every time your rupees become dollars, the "
  "platform takes a small spread, usually around one percent. On one lakh, that's roughly a thousand "
  "rupees. [pause] Next, T-C-S — tax collected at source. But here's the good news: it only kicks in "
  "above ten lakh rupees in a year. At one lakh, your T-C-S is zero. [pause] Brokerage? On most apps, "
  "also zero. [pause] So from your one lakh, about ninety-nine thousand rupees actually gets invested. "
  "The currency conversion, not some hidden fee, is your real cost. Keep your eye on that markup."),

 ("gw11_cards", "gw_cards", {
    "kicker": "THE FOUR COSTS", "title": "Every charge, buying and selling", "color": COST,
    "items": [
      {"emoji": "💱", "k": "Forex markup", "v": "A spread on every rupee-to-dollar conversion — roughly half to two percent. Your biggest real cost", "chip": "~0.5–2%"},
      {"emoji": "🧾", "k": "TCS on remittance", "v": "20% on money sent above ₹10 lakh a year — but it's fully refundable against your income tax", "chip": "REFUNDABLE"},
      {"emoji": "💸", "k": "Brokerage & fees", "v": "Often zero to buy; tiny US regulatory fees on selling; some apps add a withdrawal fee", "chip": "OFTEN ₹0"},
      {"emoji": "🔁", "k": "Bringing money back", "v": "Repatriation means another currency conversion, and sometimes a transfer fee on exit", "chip": "EXIT COST"},
    ],
  },
  "Let's name every cost you'll meet. [pause] One — the forex markup, the spread on converting "
  "rupees to dollars. It's small per trade, but it's on every transfer, so it's the one that "
  "actually adds up. [pause] Two — T-C-S, which we'll unpack in a second, but remember it's "
  "refundable. [pause] Three — brokerage, which is often zero to buy, though selling carries tiny "
  "US regulatory fees, and some apps charge to withdraw. [pause] And four, the cost people forget — "
  "when you finally bring your money home, it gets converted back to rupees, with another markup. "
  "Every conversion, in and out, has a spread."),

 ("gw12_stats", "gw_stats", {
    "kicker": "TCS · DECODED", "title": "TCS sounds scary — it isn't", "color": TAX,
    "stats": [
      {"label": "TCS rate, above the yearly limit", "to": 20, "suffix": "%", "color": TAX, "sub": "only on the amount over ₹10 lakh"},
      {"label": "Send this much with ZERO TCS", "to": 1000000, "prefix": "₹", "color": OK, "sub": "₹10 lakh per financial year"},
      {"label": "Of that TCS, you get back", "to": 100, "suffix": "%", "color": OK, "sub": "adjust or refund it in your ITR"},
    ],
    "note": "TCS is not a tax you lose — it's a prepayment you claim back. For most investors, it's effectively zero.",
  },
  "T-C-S scares people off, and it shouldn't. Let's decode it. [pause] The rate is twenty percent — "
  "but only on the amount you send above ten lakh rupees in a single year. Send less than ten lakh, "
  "and your T-C-S is exactly zero. [pause] And even if you cross that limit, this is the part "
  "everyone misses — T-C-S is not a tax you lose. It's a prepayment. [pause] You claim every rupee "
  "of it back when you file your income-tax return, either as a credit against your tax, or as a "
  "straight refund. [pause] So for the vast majority of investors, the real cost of T-C-S is nothing "
  "at all."),

 # ===== PART 4 — Taxes on your returns =====
 ("gw13_div4", "gw_divider", {"n": 4, "title": "Then, The Taxman", "sub": "How your dividends and gains are taxed", "color": TAX},
  "Part four — tax on what you earn. [pause] Once your money is making money, two kinds of tax "
  "appear. Let's keep them separate and simple."),

 ("gw14_compare", "gw_compare", {
    "kicker": "TAX ON RETURNS", "title": "Dividends vs capital gains", "color": TAX,
    "cols": [
      {"name": "Dividends", "color": TAX, "emoji": "💵", "rows": [
        {"k": "TAXED FIRST IN", "v": "The USA, at source"},
        {"k": "RATE", "v": "25% withheld"},
        {"k": "THEN IN INDIA", "v": "Added to your income"},
        {"k": "RELIEF", "v": "Foreign Tax Credit (DTAA)"},
        {"k": "RESULT", "v": "No double taxation"},
      ]},
      {"name": "Capital gains", "color": OK, "emoji": "📈", "hi": True, "rows": [
        {"k": "TAXED IN", "v": "Only India"},
        {"k": "LONG-TERM > 24 mo", "v": "12.5%, no indexation"},
        {"k": "SHORT-TERM ≤ 24 mo", "v": "Your income-tax slab"},
        {"k": "US SIDE", "v": "No US gains tax for you"},
        {"k": "REMEMBER", "v": "Compute it in rupees"},
      ]},
    ],
  },
  "There are two kinds of return, taxed two different ways. [pause] First, dividends — the cash a "
  "company pays you. The U-S taxes these first, withholding twenty-five percent before it even "
  "reaches you. Back in India, you declare that income — but you claim a foreign tax credit under "
  "the India-U-S tax treaty, so you're never taxed twice on the same money. [pause] Second, capital "
  "gains — your profit when you sell. These are taxed only in India. Hold for more than twenty-four "
  "months and it's long-term, at twelve and a half percent. Sell sooner, and it's short-term, at "
  "your normal slab rate. [pause] The U-S charges you nothing on those gains — just remember to "
  "calculate everything in rupees."),

 ("gw15_cards", "gw_cards", {
    "kicker": "STAY ON THE RIGHT SIDE", "title": "The compliance you cannot skip", "color": TAX,
    "items": [
      {"emoji": "📋", "k": "Schedule FA is mandatory", "v": "Declare every foreign holding in your ITR — even one fractional share, even with no gains", "chip": "MUST FILE"},
      {"emoji": "🧮", "k": "Claim your credits", "v": "Use the India-US treaty to offset that 25% US dividend tax against your Indian tax", "chip": "DTAA · FTC"},
      {"emoji": "🗂️", "k": "Keep every record", "v": "Save trade notes, dividend statements and remittance receipts — you'll need them at tax time", "chip": "RECORDS"},
      {"emoji": "👩‍⚖️", "k": "When in doubt, ask a CA", "v": "Cross-border tax gets tricky fast; a chartered accountant usually pays for itself here", "chip": "GET HELP"},
    ],
  },
  "Now the compliance you genuinely cannot skip. [pause] The big one — Schedule F-A. As a resident, "
  "you must declare every foreign holding in your tax return. Even a single fractional share. Even "
  "if you made no profit at all. This is not optional, and the penalties for missing it are harsh. "
  "[pause] Second, claim your credits — use that India-U-S treaty to recover the twenty-five percent "
  "withheld on dividends. [pause] Third, keep your paperwork — trade notes, dividend statements, "
  "remittance receipts. [pause] And if any of this feels heavy, a good chartered accountant is worth "
  "every rupee. Cross-border tax is where small mistakes get expensive."),

 # ===== PART 5 — Doing it right =====
 ("gw16_div5", "gw_divider", {"n": 5, "title": "Doing It Right", "sub": "The steps, the rupee route, and the real risks", "color": OK},
  "Part five — doing it well. [pause] The exact steps, the simpler rupee route, and the risks nobody "
  "puts on the brochure."),

 ("gw17_steps", "gw_steps", {
    "kicker": "START IN 5 STEPS", "title": "From zero to your first US share", "color": USD,
    "items": [
      {"emoji": "🔍", "label": "Pick a platform", "sub": "app or global broker", "c": USD},
      {"emoji": "🪪", "label": "Open & KYC", "sub": "PAN, ID, bank link", "c": USD},
      {"emoji": "💰", "label": "Add & convert", "sub": "rupees → dollars, LRS", "c": INR},
      {"emoji": "🛒", "label": "Buy shares", "sub": "whole or fractional", "c": OK},
      {"emoji": "📑", "label": "Track & file", "sub": "Schedule FA at tax time", "c": TAX},
    ],
    "note": "Start small, automate a fixed monthly amount, and treat it as a long-term global allocation.",
  },
  "So, practically, how do you begin? Five steps. [pause] One — pick your platform, an app if you're "
  "starting out, a global broker if you're not. [pause] Two — open the account and finish K-Y-C with "
  "your PAN, an I-D, and your bank. [pause] Three — add rupees; the platform converts them to "
  "dollars under L-R-S. [pause] Four — buy your shares, whole or fractional. [pause] And five — "
  "track your holdings and declare them at tax time. [pause] My honest advice? Start small, automate "
  "a fixed amount each month, and treat this as a long-term global slice of your portfolio — not a "
  "place to gamble."),

 ("gw18_cards", "gw_cards", {
    "kicker": "THE RUPEE ROUTE", "title": "Don't want the LRS hassle? Go indirect", "color": OK,
    "items": [
      {"emoji": "🧺", "k": "International mutual funds", "v": "Indian funds and fund-of-funds that invest in US or global equities — bought in rupees, no LRS", "chip": "IN ₹, NO LRS"},
      {"emoji": "📊", "k": "India-listed ETFs", "v": "ETFs on the NSE that track the S&P 500 or Nasdaq 100 — one click, in rupees", "chip": "NSE-LISTED"},
      {"emoji": "⛔", "k": "The overseas-limit catch", "v": "SEBI caps how much these funds send abroad; some pause fresh buying when the limit is full", "chip": "WATCH LIMITS"},
      {"emoji": "🏙️", "k": "GIFT City middle path", "v": "Direct US stocks under LRS, but routed through India's GIFT City — a hybrid of both routes", "chip": "HYBRID"},
    ],
  },
  "Not everyone wants the L-R-S paperwork — and you don't have to. [pause] The indirect route lets "
  "you invest in rupees, right here. You can buy an Indian mutual fund or fund-of-funds that holds "
  "US stocks. [pause] Or you can buy an E-T-F listed on our own N-S-E that simply tracks the S and P "
  "five hundred or the Nasdaq one hundred — one click, in rupees, no dollars leaving the country. "
  "[pause] There's one catch to know — S-E-B-I limits how much these funds can invest abroad, so "
  "some occasionally pause fresh purchases. [pause] And Gift City sits in between: real US stocks, "
  "under L-R-S, but through an Indian gateway."),

 ("gw19_cards", "gw_cards", {
    "kicker": "BEFORE YOU JUMP IN", "title": "The risks nobody advertises", "color": COST,
    "items": [
      {"emoji": "💱", "k": "Currency cuts both ways", "v": "A weaker rupee lifts your returns; a stronger rupee eats them — you're taking a dollar bet too", "chip": "₹ vs $"},
      {"emoji": "🧊", "k": "Costs bite small sums", "v": "Markups and fixed fees hurt tiny transfers — invest in larger, less frequent chunks", "chip": "GO BIGGER"},
      {"emoji": "⏳", "k": "Access can pause", "v": "Indirect funds can shut fresh inflows, and platforms can change terms — don't over-rely on one", "chip": "STAY FLEXIBLE"},
      {"emoji": "📜", "k": "Compliance is on you", "v": "Miss Schedule FA and the penalties are steep — the tax paperwork is simply not optional", "chip": "FILE IT"},
    ],
  },
  "Before you jump in, the risks nobody advertises. [pause] First, currency. When you own US stocks, "
  "you're also betting on the dollar. A weaker rupee boosts your returns; a stronger rupee quietly "
  "eats them. [pause] Second, costs hurt small sums the most — those markups and flat fees sting on "
  "tiny transfers, so invest in bigger, less frequent chunks. [pause] Third, access isn't "
  "guaranteed. Indirect funds can pause, platforms change terms — so don't depend on a single one. "
  "[pause] And fourth, the compliance is on you. Miss Schedule F-A, and the penalties are steep. "
  "Respect the paperwork."),

 ("gw20_recap", "gw_recap", {
    "title": "Investing abroad, in one breath",
    "items": [
      "Yes — it's legal via RBI's LRS: up to $250,000 a year",
      "Direct: apps like INDmoney, Vested, Groww, or IBKR",
      "Indirect: India-listed ETFs & funds — in rupees, no LRS",
      "Real cost is the forex markup; brokerage is often ₹0",
      "TCS 20% only above ₹10 lakh — and it's refundable",
      "Tax: 25% on US dividends (credited), gains taxed in India",
      "Always declare foreign holdings in Schedule FA",
    ],
    "closer": "The whole world is investable from India — go in with your eyes open.",
  },
  "Let's bring it all together. [pause] Yes, you can invest abroad from India — legally, through "
  "R-B-I's L-R-S, up to two hundred and fifty thousand dollars a year. [pause] Go direct with an app "
  "like INDmoney, Vested, Groww or Interactive Brokers — or go indirect with an Indian E-T-F or fund, "
  "in rupees. [pause] Your real cost is the forex markup; brokerage is often zero, and T-C-S applies "
  "only above ten lakh and is refundable. [pause] On your returns, the U-S takes twenty-five percent "
  "of dividends, which you credit back, and your gains are taxed in India. [pause] And always, always "
  "declare your foreign holdings in Schedule F-A. " + DISCLAIMER),
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
    warn = "  ⚠ LONG — split or ensure it develops to p≈0.85" if dur > 90 else ""
    print(f"  {sid:14s} {dur:6.2f}s{warn}", flush=True)

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
print(f"total {t - GAP:.2f}s ({(t-GAP)/60:.2f} min), {len(cuts)} scenes, NO captions, NO music")
