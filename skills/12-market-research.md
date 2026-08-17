# Skill 12 — Market Research & Data Validation (read BEFORE any stock-market video)

This repo produces dated market videos (pre-market, post-market, wraps), IPO analysis,
and trading/investment education. **A wrong number in a finance video misleads real
investors — it is the worst defect this repo can ship.** This skill exists because a
delivered video rounded stock moves (said 2.1% for a 2.08% close) and cited "$92 Brent"
that was actually a mislabeled WTI figure. Both were caught by the user, not by QA.
Follow this skill and neither happens again.

## 0. The three query families

Every market-video brief falls into one of these; each has its own recipe below.

| Family | Examples | Recipe |
|---|---|---|
| **Current market rates** | pre-market brief, post-market wrap, weekly recap, "what moved today" | §3 |
| **Current IPOs** | IPO analysis, subscription status, GMP, listing-day recap | §4 |
| **Investment opportunities / education** | how to trade, F&O, mutual funds, sector deep-dives, strategy videos | §5 |

## 1. Hard data rules (violations = defects)

1. **2-decimal precision, no rounding.** Every stock/index/commodity % appears to exact
   2 decimals in BOTH the on-screen frame AND the spoken narration ("two point zero
   eight percent", never "about two percent"). Index levels to 2 decimals on screen
   (76,059.77); points changes exact (−331.62).
2. **Official close over intraday.** Vendors snapshot at different times. When two
   sources disagree, triangulate a THIRD before committing. Authority order:
   NSE/BSE official close > Moneycontrol/ET Markets close pages > broker blogs
   (HDFC Sky, Liquide) > aggregator news. Never average conflicting figures.
3. **Name the benchmark.** Brent ≠ WTI (they differ by $3–6). Nifty 50 ≠ Nifty 500.
   Sensex ≠ BSE 500. If a source says "crude at $X", confirm WHICH benchmark before
   using it. Sanity-check against the prior day's level — a $8 overnight move in
   crude without a headline event means you have the wrong benchmark or a stale quote.
4. **Date-check every source.** Web search returns look-alike articles from prior
   years (same "July 24" from 2024/2025). Confirm the article's dateline matches the
   video's date before extracting any number.
5. **Know the reporting lag.** FII/DII cash figures are confirmed T+1. For a same-day
   video say "provisional" or use yesterday's confirmed figure and say so. Same for
   subscription numbers late on an IPO day.
6. **Never fabricate or interpolate.** If a figure isn't published yet, say so on
   screen ("provisional", "as of 3:30 PM") or frame qualitatively. A missing number
   is honest; an invented one is a defect.
7. **The numbers table is a pre-render gate.** Before generating TTS, write the full
   table (indices, %, points, gainers/losers with exact %, sector moves, crude, rupee,
   FII/DII) into the build.py docstring WITH the source of each figure. Re-verify the
   table against sources ONCE, as a checklist, before rendering. QA stills verify the
   table made it to screen — they cannot catch a wrong table.
8. **Disclaimer is mandatory.** Every video: "information/analysis from public
   sources, NOT investment advice; consult a SEBI-registered advisor." Say it in the
   narration (title or recap scene) and put it in the description. Education videos
   additionally avoid "guaranteed", "sure-shot", specific buy/sell calls, and price
   targets presented as advice.

## 2. Source directory (India)

**Indices & stocks (close data)**
- NSE official: nseindia.com (close, gainers/losers, FII/DII provisional) — the
  single source of truth when sources conflict.
- Moneycontrol (moneycontrol.com), ET Markets (economictimes.indiatimes.com/markets) —
  reliable close pages, good for cross-checks.
- Business Standard markets live blog — good narrative + numbers, updates all day.
- Broker close reports: HDFC Sky market reports, Liquide daily blog — convenient
  structured summaries; treat as SECONDARY (they've disagreed with the NSE close by
  ~20bps in practice).

**Commodities / currency / global**
- Crude: Fortune's daily "price of oil" article (states benchmark explicitly),
  TradingEconomics commodity pages, Investing.com. ALWAYS confirm Brent vs WTI.
- Rupee: RBI reference rate, or the level quoted in the close reports (cross-check 2).
- US/global lead for pre-market: CNBC/Reuters close reports, GIFT Nifty level.

**FII/DII**
- NSE provisional (same evening), Trendlyne / niftytrader.in FII-DII pages (tabulated
  history). Label same-day figures "provisional".

**IPOs**
- Chittorgarh.com — subscription status by category (QIB/NII/retail), GMP, timeline;
  the standard aggregator.
- NSE/BSE IPO pages — official subscription numbers.
- SEBI website — RHP/DRHP for fresh-issue vs OFS split, objects of the issue,
  promoter holding (the analysis backbone of ipo-series-en videos).
- Moneycontrol/Mint IPO sections — anchor book, listing-day coverage.
- GMP is UNOFFICIAL grey-market data: always label it as such on screen, never
  present it as a listing prediction.

**Education / concepts**
- Zerodha Varsity — the reference for Indian market mechanics (F&O, margins,
  settlement, taxation). Prefer it over generic sources for India-specific rules.
- SEBI investor-education material + circulars — for regulation (T+1 settlement,
  F&O lot sizes, margin rules change; VERIFY current rules, don't trust training data).
- NSE/BSE circulars for contract specs, lot sizes, expiry-day conventions.
- Investopedia — generic concepts only; check every India-specific claim against
  Varsity/SEBI (US rules differ: settlement, taxes, PDT rules don't apply).

## 3. Recipe — current market rates (pre/post-market, wraps)

1. Search: `Sensex Nifty close <date>` → collect 2 independent close reports.
2. Fetch the most structured one (HDFC Sky close report / Liquide) for the full
   table: indices, sectors, top gainers/losers with %.
3. Cross-check gainers/losers % against a second source. **Any disagreement → fetch a
   third (Moneycontrol/NSE) and take the official close.**
4. Separately verify: crude (with benchmark name), rupee, FII/DII (label provisional),
   weekly/streak context ("Nifty −2.33% for the week" needs its own source).
5. Find the STORY, not just the table: what diverged (sector rotation, breadth vs
   headline, a green Bank Nifty on a red day). The teaching angle is what makes these
   videos better than a news ticker — but the angle must sit on verified numbers.
6. Write the numbers table into the build.py docstring with per-figure sources.
   Gate: re-read the table against the sources once before TTS.
7. Pre-market variant: GIFT Nifty, US close, Asia open, crude overnight, and
   yesterday's FII/DII confirmed figure. Frame as SETUP not forecast, and flag the
   key risk explicitly (the flagged risk deciding the day is a recurring, honest beat).

## 4. Recipe — current IPOs

1. Chittorgarh for the live table: dates, price band, lot size, issue size,
   subscription by category, GMP (labeled unofficial).
2. RHP/DRHP (SEBI or Chittorgarh's summary) for: fresh issue vs OFS split, objects,
   promoter/anchor detail, financials (3-yr revenue/PAT), peer valuation.
3. Cross-check subscription numbers against NSE/BSE official pages on the final day —
   aggregators lag by hours.
4. Analysis backbone (per ipo-series-en pattern): fresh-vs-OFS is the honesty lens
   (who gets the money?), valuation vs listed peers, use-of-proceeds, risks from the
   RHP's own risk-factors section.
5. Never say "apply/avoid" as advice — present the framework and the disclaimer.
6. Listing-day recap: listing price vs issue price vs GMP expectation — exact %.

## 5. Recipe — investment opportunities & education

1. These are less date-sensitive but RULE-sensitive: settlement cycles, lot sizes,
   margin %, tax rates, and platform features change. Verify every regulatory/number
   claim against SEBI/NSE/Varsity CURRENT pages — do not trust training data for
   rates in force (STT, LTCG/STCG rates, F&O lot sizes).
2. Platform videos (Zerodha/Groww/Upstox how-tos): verify current pricing/brokerage
   from the platform's own pricing page, dated.
3. "Opportunity" videos (sector/theme/strategy): every performance claim needs a
   source and a time window on screen ("Nifty IT +12% in 2026 YTD, as of 24 Jul").
   Backtested or historical returns get a "past performance ≠ future returns" line.
4. Education explainer math (option payoffs, SIP compounding, margin): COMPUTE it
   (hard rule 3 of the contract) — precompute the real numbers at module scope and
   show the actual curve, don't draw an indicative sketch.

## 6. Pre-render validation checklist (run every time, in order)

- [ ] Every % in props/narration is 2-decimal exact and matches the docstring table
- [ ] Every table figure has a named source; conflicts were resolved via a 3rd source
- [ ] Commodity benchmarks named (Brent vs WTI); levels sanity-checked vs prior day
- [ ] All source article datelines match the video date
- [ ] Provisional data (FII/DII same-day, live subscriptions) labeled as such
- [ ] GMP (if any) labeled unofficial
- [ ] Regulatory/tax/lot-size claims verified against current SEBI/NSE/Varsity pages
- [ ] Disclaimer present in narration AND description
- [ ] User-provided corrections adopted verbatim (user-validated figures outrank any
      vendor — record them in the docstring as "user-validated")

Then proceed to skills/06-qa.md stills. QA stills check layout; THIS checklist checks
truth. Both are mandatory; neither substitutes for the other.
