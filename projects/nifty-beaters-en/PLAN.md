# 50 to Beat the Nifty — build plan

**Brief:** From 2,397 NSE-listed companies, select 50 that (thesis) can beat the Nifty
over 1–5 years, and defend the picks in a chaptered video. English · high-conviction
tone · organized by CONVICTION TIER · real scraped fundamentals behind every pick.

## Data (honest basis)
- Universe: `ALL_companies_master.csv` (2,397 cos, 22 sectors) — name/price/desc only.
- Shortlist: 260 curated quality/growth candidates → real fundamentals scraped from
  screener.in (`research/fundamentals/*.json`, rollup `research/fundamentals.csv`):
  P/E, ROE, ROCE, mkt cap, 5Y/3Y sales & profit CAGR, pros/cons. Point-in-time Aug 2026.
- Selection: transparent scorecard (quality + growth + valuation sanity + size),
  sector-aware (bank ROCE ≠ industrial ROCE), diversified → final 50 in 3 tiers.

## Identity (prefix `nb`)
- Theme: near-black; primary accent = growth green. Semantic: green=quality/growth,
  amber=valuation, cyan=Nifty benchmark, violet=structural theme, red=risk.
- Motif: an "alpha gap" — a stock line breaking ABOVE the Nifty benchmark line; a
  vs-Nifty scoreboard; tier badges T1/T2/T3.

## Chapters (each = own build_chN.py → own MP4, delivered on completion)
1. **The Framework** — why beat Nifty, funnel 2,397→50, the scorecard, tier system,
   sector spread. (~10 min)
2. **Tier 1 — Core Compounders** (~16 stocks) — highest quality + durable growth.
3. **Tier 2 — Growth Accelerators** (~18 stocks) — structural-theme growth.
4. **Tier 3 — High Risk / High Reward** (~14 stocks) — cyclical/turnaround/small-cap.
5. **The Portfolio & Risks** — full 50, allocation logic, what breaks the thesis,
   disclaimer, recap.
- Master = ffmpeg concat of chapter MP4s.

## Hard gates
- skill 12: 2-decimal figures, named source (screener.in, Aug 2026), "past performance
  ≠ future returns", NO price targets as advice, disclaimer in narration + description.
- skill 03/09: duration-aware phasing, continuous motion, overlap-proof layout, QA stills.

## Status
- [x] Universe explored, scraper validated, 260-candidate scrape (168 w/ full data)
- [x] Score + select 50 (T1=16 T2=18 T3=16) → research/picks.json (exact real figures)
- [x] NBScenes.tsx scene set (10 variants) + registered
- [x] Ch01 build + QA (funnel overflow fixed) — validated
- [x] Ch02 build + QA (stock workhorse validated, financial+non-fin, thesis fits)
- [~] Ch01+Ch02 rendering + delivering (background)
- [~] Ch03/04/05 TTS (background)
- [ ] QA new scene types (portfolio, bars, recap) → render ch03/04/05
- [ ] Master concat + deliver
Note: telecom + oil&gas absent (screener IP-block); deliberate index-heavyweight
underweight framed as a feature in ch05 narration.
