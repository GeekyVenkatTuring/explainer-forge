#!/usr/bin/env python3
"""INDmoney — an honest, unbiased review (English, Nova). Prefix `idm`, scene set IDMScenes.tsx.
Companion to intl-investing-en (which named INDmoney). India-context PLATFORM review — read
skills/12-market-research.md §5.2 (platform pricing from the platform's OWN dated page; every
complaint sourced; unbiased, no sponsorship).

VERIFIED NUMBERS / CLAIMS TABLE (pre-render gate, skill 12 rule 7) — verified 4 Aug 2026.
Full sourcing in research/indmoney-dossier.md.
  • Regulatory: broking arm INDstocks Pvt Ltd — SEBI stock-broker INZ000305337, DP IN-DP-690-2022;
        advisory arm Finzoom Investment Advisors = SEBI RIA. Company operating since 2018.
        [SEBI registered-broker DB; Chittorgarh "Is INDmoney SEBI registered"; CB Insights]
  • US custody: shares bought via US brokers DriveWealth LLC and Alpaca Securities LLC — both
        SEC-registered + FINRA members + SIPC members. Shares held in YOUR name at the US broker.
        [INDmoney "Is INDmoney safe"; vested.blog; DriveWealth PRNewswire 2020]
  • SIPC: up to $500,000 per investor incl. up to $250,000 cash — covers BROKER FAILURE, NOT
        market losses (said explicitly on screen + narration). [INDmoney; SIPC]
  • Fees (INDmoney OWN pages = primary): account-open / AMC / platform / withdrawal = ₹0;
        brokerage on US stocks = 0.25% per trade (small cap; INDmoney fee page says $25, some
        aggregators $35 → narration says "check live pricing", no hard cap on screen);
        forex markup ~0.5%–1.2% ("charged by the bank"), overall ~0.5%–1.5%.
        [indmoney.com/us-stocks + /learn/us-stocks/inr-to-usd-conversion-and-forex-markup;
         Chittorgarh; vested.blog pegs INDmoney FX at 50–80 paise/USD ≈ 0.6–0.96%]
  • Comparison FX (illustrative, vested.blog — Vested's OWN blog, noted as biased): inbound
        markup INDmoney ~0.6–1.0% (50–80 p/USD) < Vested ~0.9–1.2% (75–100 p/USD); IBKR
        near-interbank (1–5 p/USD). Brokerage: INDmoney/Vested 0.25%/trade; IBKR ~$0.005/share.
        Narration flags "fees change — check each platform's live pricing".
  • TCS: nil ≤ ₹10L/FY, 20% above, REFUNDABLE in ITR (govt rule, not INDmoney).
  • INDprime: optional paid membership ~₹99/month (instant funding + perks). [Blind; Chittorgarh]
  • On-ramp: 10,000+ US stocks & global ETFs; fractional from $1; paperless PAN KYC ~5 min;
        SIP/auto-invest; one-tap withdrawal. [indmoney.com/us-stocks]
  • App-store rating framed softly ("around four stars, from hundreds of thousands of reviews")
        vs low third-party complaint-site scores (PissedConsumer 1.4/5 on ~7) — selection bias
        stated on screen. Complaints (dated, sourced): slow US-stock withdrawals (days→weeks,
        Oct 2025), funds stuck mid-transfer (₹90k/36h, Feb 2026), weak/scripted support,
        app bugs + slow KYC. [PissedConsumer; Trustpilot; MouthShut]

  Education only — NOT investment advice; NOT sponsored. Disclaimer in recap + description.

Voice: Kokoro "Nova" (Voicebox, English). Usage: python3 build.py
"""
import json, os, subprocess, time, urllib.request

BASE = "http://127.0.0.1:17493"
PROFILE = "c488e05c-3407-46a3-874d-1b09b3aff78d"  # "TTS Bright (Nova)"
GAP = 0.5
PAUSE = 0.6
ATEMPO = 0.95
PREFIX = "idm"
ROOT = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(ROOT, "..", ".."))
PUBLIC = os.path.join(REPO, "composer", "public", PREFIX)
RAW = os.path.join(ROOT, "assets", "raw")
FIN = os.path.join(ROOT, "assets")
for d in (PUBLIC, RAW, os.path.join(ROOT, "artifacts"), os.path.join(ROOT, "renders")):
    os.makedirs(d, exist_ok=True)

# identity accents (mirror IDMScenes A{})
BRAND, USD, COST, WARN, OK, TAX = "#2DD4BF", "#60A5FA", "#FB7185", "#F59E0B", "#4ADE80", "#A78BFA"

DISCLAIMER = ("And one last, important note. [pause] This is education, not investment advice — and "
    "I'm not sponsored by INDmoney, or by anyone else. [pause] Platform fees and rules change, so "
    "always check the current numbers yourself. And for your own taxes, talk to a SEBI-registered "
    "advisor or a chartered accountant. Thanks for watching.")

# ---------------------------------------------------------------- SCREENPLAY
SEGMENTS = [

 # ===== HOOK =====
 ("idm01_title", "idm_title", {},
  "You've loaded some money into INDmoney to buy US stocks. [pause] So here's the real question — "
  "is it actually any good? [pause] Let's do this properly. How the app really works. Whether your "
  "money is safe. Every rupee it costs. And what real users complain about. [pause] An honest "
  "look — this is education, not investment advice."),

 ("idm02_ask", "idm_steps", {
    "kicker": "WHAT WE'LL ANSWER", "title": "We'll go in three honest passes", "color": BRAND,
    "items": [
      {"emoji": "🧭", "label": "How it works", "sub": "sign-up to first US share", "c": BRAND},
      {"emoji": "🛡️", "label": "Is it safe?", "sub": "custody & regulation", "c": USD},
      {"emoji": "⚖️", "label": "Worth it?", "sub": "costs, rivals, complaints", "c": OK},
    ],
    "note": "Then a straight verdict for the money you've already put in — no hype, no sponsorship.",
  },
  "Here's how we'll do it — in three honest passes. [pause] First, how INDmoney actually works: "
  "from signing up to buying your first US share. [pause] Second, the question that really "
  "matters — is your money safe? Who is actually holding your shares? [pause] And third, is it "
  "worth it: what it truly costs, how it stacks up against rivals, and what real users complain "
  "about. [pause] Then a straight verdict for the money you've already put in. No hype, and no "
  "sponsorship."),

 # ===== PART 1 — HOW IT WORKS =====
 ("idm03_div1", "idm_divider", {"n": 1, "title": "How It Works", "sub": "From signing up to your first US share", "color": BRAND},
  "Part one — how it actually works. [pause] Forget the marketing. Let's walk the real path, from "
  "opening the app to owning your first slice of an American company."),

 ("idm04_what", "idm_cards", {
    "kicker": "MORE THAN US STOCKS", "title": "INDmoney is a financial super-app", "color": BRAND,
    "items": [
      {"emoji": "🇺🇸", "k": "US stocks", "v": "10,000+ US stocks and global ETFs, from just $1 — the part you're using", "chip": "FRACTIONAL"},
      {"emoji": "🇮🇳", "k": "Indian stocks", "v": "A full SEBI-registered broker for Indian shares and mutual funds too", "chip": "INDstocks"},
      {"emoji": "📊", "k": "Track it all", "v": "Links your banks, cards and EPF to show your whole net worth in one place", "chip": "MONEY VIEW"},
      {"emoji": "🎯", "k": "One login", "v": "The pitch: your entire financial life — invest, track, plan — in a single app", "chip": "ALL-IN-ONE"},
    ],
  },
  "First, know what you've signed up for. INDmoney isn't just a US-stocks app. [pause] It's a "
  "financial super-app. [pause] Yes, it gives you over ten thousand US stocks and global funds, "
  "starting from a single dollar. That's the part you're using. [pause] But it's also a full "
  "Indian stockbroker, registered with SEBI, for Indian shares and mutual funds. [pause] And it "
  "can link your banks, cards, even your provident fund, to track your entire net worth on one "
  "screen. [pause] The whole idea is one app for your money. That's the promise. Let's test it."),

 ("idm05_steps", "idm_steps", {
    "kicker": "US STOCKS · THE FLOW", "title": "From zero to your first US share", "color": BRAND,
    "items": [
      {"emoji": "📝", "label": "Sign up + KYC", "sub": "PAN, paperless, ~5 min", "c": BRAND},
      {"emoji": "💰", "label": "Add money", "sub": "bank → wallet, ₹→$", "c": WARN},
      {"emoji": "🛒", "label": "Buy", "sub": "fractional, from $1", "c": USD},
      {"emoji": "🔁", "label": "SIP", "sub": "auto-invest monthly", "c": TAX},
      {"emoji": "🏧", "label": "Withdraw", "sub": "one tap to your bank", "c": OK},
    ],
    "note": "The rupee-to-dollar hop runs on the RBI's LRS — the app files the paperwork for you.",
  },
  "Here's the actual flow, in five steps. [pause] One — sign up with your phone number, and finish "
  "K-Y-C with your PAN. It's paperless, and often done in about five minutes. [pause] Two — add "
  "money. You move rupees from your bank into your US-stocks wallet, and they're converted to "
  "dollars. [pause] Three — buy. Pick any stock and invest a fixed dollar amount, even one dollar, "
  "thanks to fractional shares. [pause] Four — you can automate it with a monthly S-I-P. [pause] "
  "And five — withdraw, which sends money back to your Indian bank in a tap. [pause] That "
  "rupee-to-dollar hop uses the R-B-I's remittance scheme, and the app fills the forms for you."),

 ("idm06_stats", "idm_stats", {
    "kicker": "THE ON-RAMP", "title": "Why beginners start here", "color": BRAND,
    "stats": [
      {"label": "US stocks & ETFs you can buy", "to": 10000, "suffix": "+", "color": USD, "sub": "Apple, Nvidia, S&P 500…"},
      {"label": "Minimum to buy one", "to": 1, "prefix": "$", "color": OK, "sub": "fractional — own a slice"},
      {"label": "Account & withdrawal fees", "to": 0, "prefix": "₹", "color": BRAND, "sub": "zero to open, zero to withdraw"},
    ],
    "note": "A tiny floor and no account fees — that low barrier is why it's a popular first app.",
  },
  "This is why beginners start here. [pause] You get more than ten thousand US stocks and funds to "
  "choose from. [pause] The minimum to buy one is about a dollar — so a five-hundred-dollar share "
  "is still within reach. You just own a slice. [pause] And there's no fee to open the account, "
  "and none to withdraw. [pause] A tiny floor, and no account charges. That low barrier is the "
  "whole reason it's so many people's first US-stocks app. [pause] But a low barrier is not the "
  "same as low cost. Hold that thought."),

 # ===== PART 2 — IS IT SAFE? =====
 ("idm07_div2", "idm_divider", {"n": 2, "title": "Is It Safe?", "sub": "Who actually holds your shares", "color": USD},
  "Part two — the question that actually keeps people up at night. [pause] You're sending money "
  "abroad, into an app. If INDmoney disappeared tomorrow, what happens to your shares?"),

 ("idm08_pipe", "idm_pipe", {
    "kicker": "WHERE YOUR SHARES LIVE", "title": "Your money doesn't sit inside INDmoney", "color": USD,
    "nodes": [
      {"emoji": "🧑‍💻", "label": "You", "sub": "KYC in your name", "c": BRAND},
      {"emoji": "📱", "label": "INDmoney", "sub": "the app / the pipe", "c": USD},
      {"emoji": "🏛️", "label": "US broker", "sub": "DriveWealth · Alpaca", "c": USD},
      {"emoji": "📈", "label": "Your shares", "sub": "held in your name", "c": OK},
    ],
    "note": "The US broker is SEC- and FINRA-regulated. INDmoney is the app — not the vault your stock sits in.",
  },
  "Here's the reassuring part. Your shares don't actually sit inside INDmoney. [pause] INDmoney is "
  "the app — the pipe. [pause] When you buy, the trade goes to a regulated U-S broker behind the "
  "scenes: either DriveWealth or Alpaca. [pause] Both are registered with America's market "
  "regulators — the S-E-C and FINRA. [pause] And the shares are held there, in your name. [pause] "
  "So if the INDmoney app itself went under, your stocks still exist, at the U-S broker, belonging "
  "to you. [pause] That's the key idea. The app is a middleman, not the vault."),

 ("idm09_safe", "idm_stats", {
    "kicker": "THE SAFETY NET", "title": "Regulated at both ends", "color": OK,
    "stats": [
      {"label": "US broker protection (SIPC)", "to": 500000, "prefix": "$", "color": OK, "sub": "if the US broker fails"},
      {"label": "…of which cash is covered", "to": 250000, "prefix": "$", "color": USD, "sub": "the rest covers your shares"},
      {"label": "Regulators overseeing it", "to": 3, "prefix": "", "color": BRAND, "sub": "SEC · FINRA · SEBI"},
    ],
    "note": "Honest caveat: SIPC covers a broker FAILURE — NOT your losses if the stock falls.",
  },
  "And there's a safety net at the U-S end too. [pause] Those brokers are covered by S-I-P-C "
  "insurance — up to five hundred thousand dollars per investor if the broker itself fails. "
  "[pause] Of that, up to two hundred and fifty thousand covers cash; the rest covers your "
  "shares. [pause] Back in India, INDmoney's broking arm is registered with SEBI. [pause] So "
  "you've got regulators watching at both ends — the S-E-C and FINRA in America, and SEBI here at "
  "home. [pause] But read this carefully. S-I-P-C protects you if the broker collapses. [pause] It "
  "does not protect you if your stock simply falls in value. That risk is always yours."),

 # ===== PART 3 — WHAT IT COSTS =====
 ("idm10_div3", "idm_divider", {"n": 3, "title": "What It Costs", "sub": "The fee that hides in plain sight", "color": COST},
  "Part three — the money question. [pause] INDmoney loves to say zero brokerage, zero account "
  "fees. And that's true. [pause] But it is not the same as free. Let's follow a real rupee."),

 ("idm11_fees", "idm_fees", {
    "kicker": "WHAT IT COSTS", "title": "Add ₹1,00,000 — what actually gets invested?", "gross": 100000,
    "steps": [
      {"label": "Forex markup (~1%)", "delta": -1000, "c": COST, "note": "the ₹→$ spread"},
      {"label": "TCS (>₹10L/yr)", "delta": 0, "c": TAX, "note": "₹0 — you're under ₹10L"},
      {"label": "Brokerage (0.25%)", "delta": -250, "c": COST, "note": "about ₹250"},
      {"label": "Invested", "delta": 0, "c": OK, "note": "this buys stock"},
    ],
    "note": "The forex markup — not brokerage — is your real cost. It hits every rupee you convert.",
  },
  "Say you add one lakh rupees. Where does it go? [pause] First, the big one — the forex markup. "
  "Every time rupees become dollars, there's a small spread, usually around one percent. On one "
  "lakh, that's roughly a thousand rupees. [pause] Next, T-C-S — the tax collected at source. "
  "Below ten lakh rupees a year, it's zero. So here, nothing. [pause] Then brokerage — a quarter "
  "of one percent, about two hundred and fifty rupees. [pause] So from your one lakh, nearly "
  "ninety-nine thousand actually gets invested. [pause] Notice what dominated — not brokerage, but "
  "the currency conversion. That forex markup is the real price of using any of these apps."),

 ("idm12_costcards", "idm_cards", {
    "kicker": "THE COSTS, HONESTLY", "title": "Four truths about the price", "color": COST,
    "items": [
      {"emoji": "💱", "k": "Forex is the real fee", "v": "Roughly 0.5% to 1.5% each way, on every conversion — INDmoney's true cost", "chip": "~0.5–1.5%"},
      {"emoji": "🔁", "k": "Withdrawing costs too", "v": "Money coming home is converted back — a second forex markup. Don't do it often", "chip": "DOUBLE FX"},
      {"emoji": "🧾", "k": "TCS is refundable", "v": "20% only above ₹10 lakh a year — and you claim it back in your tax return", "chip": "REFUNDABLE"},
      {"emoji": "💎", "k": "INDprime is optional", "v": "A ~₹99/month membership adds instant funding and perks. You don't need it to start", "chip": "₹99/MO"},
    ],
  },
  "Four honest truths about the price. [pause] One — the forex markup is the fee that matters. "
  "Roughly half a percent to one and a half percent, each way, on every conversion. That, not "
  "brokerage, is what INDmoney really costs you. [pause] Two — withdrawing isn't free either. "
  "Bringing money home converts it back, with a second markup. So don't hop in and out. [pause] "
  "Three — that scary T-C-S only applies above ten lakh a year, and you claim it back at tax "
  "time. [pause] And four — INDmoney pushes a paid membership called INDprime, around ninety-nine "
  "rupees a month. It's optional. You do not need it to begin."),

 # ===== PART 4 — WORTH IT? =====
 ("idm13_div4", "idm_divider", {"n": 4, "title": "So — Worth It?", "sub": "How it stacks up against the rivals", "color": BRAND},
  "Part four — is it actually worth it? [pause] The only way to answer that is to put INDmoney "
  "next to its main rivals, and see where it wins, and where it doesn't."),

 ("idm14_compare", "idm_compare", {
    "kicker": "PLATFORMS · SIDE BY SIDE", "title": "INDmoney vs Vested vs Interactive Brokers", "color": BRAND,
    "cols": [
      {"name": "INDmoney", "color": BRAND, "emoji": "📱", "hi": True, "rows": [
        {"k": "FOREX MARKUP", "v": "~0.6–1.0% (mid-pack)"},
        {"k": "BROKERAGE", "v": "0.25% per trade"},
        {"k": "BEST FOR", "v": "All-in-one beginners"},
        {"k": "ITS EDGE", "v": "Fast funding, super-app"},
      ]},
      {"name": "Vested", "color": USD, "emoji": "🦺", "rows": [
        {"k": "FOREX MARKUP", "v": "~0.9–1.2% (pricier)"},
        {"k": "BROKERAGE", "v": "0.25% per trade"},
        {"k": "BEST FOR", "v": "US-stocks focus"},
        {"k": "ITS EDGE", "v": "Curated US baskets"},
      ]},
      {"name": "Interactive Brokers", "color": OK, "emoji": "🌐", "rows": [
        {"k": "FOREX MARKUP", "v": "Near-zero (tiny)"},
        {"k": "BROKERAGE", "v": "~$0.005 / share"},
        {"k": "BEST FOR", "v": "Large / serious money"},
        {"k": "ITS EDGE", "v": "Cheapest FX at scale"},
      ]},
    ],
  },
  "Let's line up the three names most Indians consider. [pause] On forex — the cost that matters — "
  "INDmoney sits in the middle. It's cheaper than Vested, but nowhere near Interactive Brokers, "
  "whose currency markup is tiny. [pause] On brokerage, INDmoney and Vested both charge a quarter "
  "percent per trade; Interactive Brokers charges a small per-share fee instead. [pause] Where "
  "INDmoney wins is convenience — fast funding, and everything in one super-app. Vested is more "
  "narrowly focused on U-S stocks. [pause] And Interactive Brokers is the low-cost giant, but it's "
  "built for serious, larger investors, and has a steeper learning curve. [pause] One caveat — "
  "these fees change. Always check each platform's live pricing before you commit."),

 ("idm15_verdict", "idm_routes", {
    "kicker": "THE VERDICT", "title": "Keep it — or switch?",
    "left": {"label": "Keep INDmoney if…", "sub": "the beginner's sweet spot", "color": OK, "emoji": "✅",
             "items": ["You invest small, regular amounts", "You want one simple all-in-one app",
                       "You're holding for the long term", "Your $100 start — this is totally fine"]},
    "right": {"label": "Look elsewhere if…", "sub": "bigger or busier plans", "color": WARN, "emoji": "⚠️",
              "items": ["You'll remit large sums (₹10L+ a year)", "You trade often — per-trade fees add up",
                        "You want the lowest possible forex cost", "Then compare IBKR, or Vested / Rovia"]},
  },
  "So here's the honest verdict. [pause] Keep using INDmoney if you're investing small, regular "
  "amounts, you want one simple app for everything, and you're in it for the long term. [pause] "
  "For the hundred dollars you've already put in — that's a perfectly sensible place to be. Don't "
  "overthink it. [pause] But look elsewhere if your plans are bigger. [pause] If you'll send large "
  "sums abroad — say, over ten lakh rupees a year — Interactive Brokers' tiny forex markup will "
  "save you real money. [pause] If you trade often, those per-trade fees stack up. [pause] And if "
  "you just want the cheapest possible currency conversion, it's worth comparing I-B-K-R, or "
  "focused apps like Vested and Rovia."),

 # ===== PART 5 — THE COMPLAINTS =====
 ("idm16_div5", "idm_divider", {"n": 5, "title": "The Complaints", "sub": "What real users actually report", "color": WARN},
  "Part five — the part reviews usually skip. [pause] What do real users actually complain about? "
  "I read the angry ones, so you don't have to."),

 ("idm17_complaints", "idm_cards", {
    "kicker": "WHAT USERS REPORT", "title": "The recurring complaints", "color": WARN,
    "items": [
      {"emoji": "⏳", "k": "Slow withdrawals", "v": "The loudest gripe: US-stock withdrawals that took weeks, not the promised days", "chip": "WITHDRAWALS"},
      {"emoji": "🧊", "k": "Funds stuck", "v": "Money added but not showing — deposits 'stuck' mid-transfer for a day or more", "chip": "FUNDING"},
      {"emoji": "🎧", "k": "Weak support", "v": "Slow, scripted replies; no easy phone or live chat when something goes wrong", "chip": "SUPPORT"},
      {"emoji": "🐞", "k": "Bugs & slow KYC", "v": "Occasional failed orders, and account or KYC setups that dragged on for weeks", "chip": "RELIABILITY"},
    ],
  },
  "Across the app stores and complaint forums, the same handful of issues come up. [pause] The "
  "loudest — slow withdrawals. Some users describe U-S-stock withdrawals that were quoted in days, "
  "but took weeks to land. [pause] Second — funds getting stuck. Money added that didn't show up "
  "for a day or more, mid-transfer. [pause] Third — support. When something breaks, people report "
  "slow, scripted replies, and no easy phone line or live chat. [pause] And fourth — the usual app "
  "bugs: the odd failed order, and K-Y-C or account setups that dragged on far longer than five "
  "minutes. [pause] These are real, and they repeat. You should know them going in."),

 ("idm18_balance", "idm_cards", {
    "kicker": "KEEP IT IN PROPORTION", "title": "But read the complaints fairly", "color": USD,
    "items": [
      {"emoji": "📣", "k": "Angry voices are loud", "v": "Complaint sites collect the furious few. Millions use INDmoney without ever posting a word", "chip": "SELECTION BIAS"},
      {"emoji": "⭐", "k": "The averages are high", "v": "On the official app stores, its rating sits around four stars — from hundreds of thousands of reviews", "chip": "~4★ · MANY"},
    ],
  },
  "Now, balance. [pause] Complaint sites are where furious people go; happy users almost never "
  "post. So a wall of one-star rants is not the whole picture. [pause] On the official app stores, "
  "where far more people rate it, INDmoney sits around four stars — from hundreds of thousands of "
  "reviews. [pause] So the truth is in the middle. It's a legitimate, widely-used app — with a "
  "real, repeating weakness around withdrawals and support. [pause] Go in knowing both."),

 ("idm19_smart", "idm_steps", {
    "kicker": "USE IT WISELY", "title": "Four habits that matter more than the app", "color": OK,
    "items": [
      {"emoji": "📦", "label": "Invest in chunks", "sub": "fewer, bigger transfers", "c": BRAND},
      {"emoji": "🚫", "label": "Don't hop out", "sub": "avoid the double forex", "c": COST},
      {"emoji": "🧾", "label": "File Schedule FA", "sub": "declare foreign holdings", "c": TAX},
      {"emoji": "📸", "label": "Keep records", "sub": "screenshots, ticket IDs", "c": OK},
    ],
    "note": "Do these, and which app you picked matters far less than how you use it.",
  },
  "Whatever app you use, four habits matter more than the logo. [pause] One — invest in fewer, "
  "larger chunks. The forex markup stings small, frequent transfers most. [pause] Two — don't hop "
  "in and out; every round trip pays that currency spread twice. [pause] Three — at tax time, "
  "declare your foreign shares in Schedule F-A. It's mandatory, even for a single fractional "
  "share. [pause] And four — keep records. Screenshots, ticket numbers, statements — so if a "
  "withdrawal stalls, you have evidence. [pause] Do these, and honestly, which app you chose "
  "matters far less than how you use it."),

 ("idm20_recap", "idm_recap", {
    "title": "INDmoney, honestly, in one breath",
    "items": [
      "INDmoney is a legit, SEBI-registered super-app",
      "US shares sit at a regulated US broker, in your name",
      "SIPC covers broker failure — not market losses",
      "The real cost is forex (~0.5–1.5%), not brokerage",
      "Great for small, long-term, all-in-one investing",
      "For big sums or active trading, compare IBKR",
      "Real weak spots: slow withdrawals & thin support",
    ],
    "closer": "For your $100 — keep going, and invest smart.",
  },
  "Let's bring it together. [pause] INDmoney is a legitimate, SEBI-registered financial super-app. "
  "[pause] Your U-S shares sit at a regulated U-S broker, in your name — and S-I-P-C covers a "
  "broker failure, though never your market losses. [pause] Its real cost is the forex markup, "
  "roughly half to one and a half percent — not brokerage. [pause] For small, long-term, "
  "all-in-one investing, it's a genuinely good pick. [pause] For large sums or frequent trading, "
  "compare Interactive Brokers. [pause] And its honest weak spots are slow withdrawals and thin "
  "support. [pause] So, for the hundred dollars you've already put in? Keep going — just invest in "
  "bigger chunks, and file your taxes. " + DISCLAIMER),
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
    print(f"  {sid:16s} {dur:6.2f}s{warn}", flush=True)

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
