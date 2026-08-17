# Credit Cards in India — Telugu Master Video · Outline & Identity

Prefix: `cc` · Aspect 16:9 1080p30 · Voice te-IN-ShrutiNeural · Telugu narration + on-screen
Telugu labels (brand names / ₹ / numbers / % stay Latin) · Telugu burned-in captions · no music.
Target ≈ 120 min. Pace ≈ 110 Telugu-words/min → budget ≈ 12,000 Telugu words total.

## Visual identity
- **Theme**: near-black blue-tinted (`makeTheme` defaults, accent = cyan). Fintech/banking feel.
- **Semantic accent colors (meanings are consistent across ALL scenes):**
  - `card`  **cyan** `#22D3EE` — the card itself, mechanics, neutral "the tool"
  - `good`  **green** `#34D399` — benefits, rewards, paying in full, healthy score
  - `bad`   **rose** `#FB7185` — debt, interest, the trap, wrong usage, danger
  - `money` **amber** `#FBBF24` — rupees, credit limit, the bank's money, fees
  - `fin`   **violet** `#A78BFA` — CIBIL score & fintech/startup cards (OneCard/Uni)
- **Recurring motif**: a drawn **credit card** (rounded rect + chip + magstripe) — appears in the
  title, every divider, and faintly in backgrounds. Secondary motif: **billing-cycle ring** (a
  circular clock) for the mechanics chapters, and **₹ particles** (Flow) for money movement.
- Typography per skill 09. Telugu headings in Noto Sans Telugu 800; Latin data in MONO.

## Chapters (24 beats-groups; each chapter = several scenes)
PART 1 — పునాదులు (Foundations)
1. **Title + hook** — India's card boom: 114.9M cards, ₹2.88L cr outstanding; power tool + trap.
2. **క్రెడిట్ కార్డ్ అంటే ఏమిటి** — borrow-now-pay-later; bank's money; the limit.
3. **క్రెడిట్ vs డెబిట్ vs UPI** — whose money, when paid, what it builds.
4. **కార్డ్ శరీర నిర్మాణం** — number, chip (EMV), CVV, expiry, network (Visa/RuPay/Mastercard).
5. **స్వైప్ వెనుక ఏం జరుగుతుంది** — cardholder→merchant→acquirer→network→issuer flow.

PART 2 — ఎలా పనిచేస్తుంది (Mechanics)  [Divider before ch6]
6. **బిల్లింగ్ సైకిల్** — statement date vs due date (the cycle ring).
7. **వడ్డీ లేని గ్రేస్ పీరియడ్** — 20–50 days; the purchase-timing trick.
8. **కనీస మొత్తం (Minimum Due)** — 5%; keeps account current but not interest-free.
9. **వడ్డీ / ఫైనాన్స్ ఛార్జెస్** — up to ~3.75%/mo (~45% p.a.); computed compounding.
10. **ఫీజులు విడమర్చడం** — annual, late, forex 2–3.5%, cash advance, 18% GST.

PART 3 — క్రెడిట్ స్కోర్ (Credit score)  [Divider before ch11]
11. **CIBIL స్కోర్** — 300–900, TransUnion, what moves it, >750 = good.
12. **క్రెడిట్ యుటిలైజేషన్** — keep < 30%; computed utilization example.
13. **మొదటి కార్డ్ ఎలా పొందాలి** — eligibility, income, secured cards, add-on.

PART 4 — సరైన వినియోగం (Using it right)  [Divider before ch14]
14. **రివార్డ్స్ & క్యాష్‌బ్యాక్** — points, cashback, redemption; SBI Cashback / Amazon Pay ICICI.
15. **నో-కాస్ట్ EMI నిజం** — 18% GST on interest + processing fee; cashback lost.
16. **ట్రావెల్, లాంజ్, ఫారెక్స్, ఇన్సూరెన్స్** — perks worth using.
17. **మంచి అలవాట్లు** — autopay, pay-in-full, track spends, one-card discipline.

PART 5 — తప్పుడు వినియోగం (Wrong usage / trap)  [Divider before ch18]
18. **మినిమం-డ్యూ ఉచ్చు** — computed multi-year payoff on ₹50,000.
19. **నగదు ఉపసంహరణ & ఇతర తప్పులు** — cash advance (no grace), overspending psychology.
20. **అప్పు నుండి బయటపడటం** — EMI conversion (12–18%), consolidation, settlement.

PART 6 — భారత మార్కెట్ (Indian market)  [Divider before ch21]
21. **బ్యాంకు కార్డులు** — SBI (Cashback, ELITE), HDFC (Millennia, Regalia, Infinia), ICICI (Amazon Pay), Axis (ACE, Flipkart).
22. **ఫిన్‌టెక్ కార్డులు** — OneCard (metal, LTF, 5x, 1% forex) & the Uni story (Uni Pay 1/3rd → RBI 2022 → GoldX pivot).
23. **మీ కార్డ్ ఎలా ఎంచుకోవాలి** — spending profile → card match decision.
24. **రీక్యాప్ + బంగారు నియమాలు** — the whole map in one breath; golden rules; thanks.

## Production order
Foundation done → Chapter 1 (title+hook) fully to render as pipeline proof → then ch2… in order.
Each chapter: scenes in `CCScenes.tsx` (prefix `cc`), narration+TTS in `build.py`, QA still, render.
Chapters rendered separately then concatenated into the final 2h master.
