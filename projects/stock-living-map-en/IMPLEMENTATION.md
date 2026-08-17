# Stock Market "Living Map" — Implementation Plan (India / NSE-BSE)

A factual, anti-hallucination agent that answers questions about a company and its stock
(price, P/E, earnings, quarterly results, recent news, future roadmap) by reasoning over an
**ontology → knowledge graph → digital twin → graph engineering → agentic** stack.

> **Core rule (non-negotiable):** the agent never states a number it read off a web page.
> Every fact is a **graph node with `source` + `asOf` timestamp**, pulled from a structured API/feed.
> The agent retrieves from the graph, computes derived numbers in code, and **cites source + time**.
> Missing or stale → it says "not available / as of <ts>", never guesses. (This is skill 12 rule 6.)
>
> **Not investment advice.** Public-source information only; consult a SEBI-registered advisor.

---

## 1. THE SOURCE LIST (free-first, cheap-paid noted)

Legend: 🟢 free · 🟡 free tier / cheap · 🔴 paid (small). Authority order for India numbers:
**NSE/BSE official > Moneycontrol/ET > screener/Tickertape/Trendlyne > broker blogs > aggregators.**

### A. Live / delayed PRICE & quotes
| Source | URL | Access | What you get | Notes |
|---|---|---|---|---|
| 🟢 NSE official | https://www.nseindia.com (`/api/quote-equity?symbol=`) | unofficial JSON (needs session cookie + headers) | close, quote, gainers/losers, indices, FII/DII provisional | **source of truth** for close; rate-limited, be gentle |
| 🟢 BSE official | https://www.bseindia.com | unofficial JSON | quote, corporate announcements | ISIN/scrip-code master |
| 🟢 jugaad-data | https://github.com/jugaad-py/jugaad-data | pip, no key | live + historical NSE, RBI; CLI + caching | future-proof (new NSE site) |
| 🟢 nsepython | https://pypi.org/project/nsepython | pip, no key | quotes, option chain, indices, heatmaps | |
| 🟢 yfinance | `pip install yfinance` | pip, no key | EOD + ~15-min-delayed intraday; use `RELIANCE.NS` / `.BO` | India fundamentals in `.info` can be stale |
| 🟡 Angel One SmartAPI | https://smartapi.angelbroking.com | free acct + API key | **real-time websocket ticks**, historical | **best free real-time**; needs a demat account |
| 🔴 Zerodha Kite Connect | https://kite.trade/docs/connect/v3/ | ₹500/mo/app | real-time websocket, historical candles | best docs/community; "free personal API" tier exists |
| 🔴 Upstox / Fyers / Dhan | upstox.com/developer · fyers.in/api | free-ish acct | real-time + historical minute data (Fyers deep) | |
| 🔴 TrueData / GlobalDatafeeds | truedata.in | paid | NSE-authorized real-time feed | for production real-time without a broker |
| 🟡 Twelve Data | https://twelvedata.com/exchanges/XNSE | free 800 req/day | quotes, earnings calendar, fundamentals | global + India |

### B. FUNDAMENTALS · P/E · ratios · shareholding
| Source | URL | Access | What you get |
|---|---|---|---|
| 🟢 screener.in | https://www.screener.in | web (scrape/export, respect ToS) | **best free fundamentals**: P/E, ROE, quarterly, annual, shareholding, concall links |
| 🟢 Tickertape | https://www.tickertape.in | web | scorecard, ratios, peers, forecasts |
| 🟢 Trendlyne | https://trendlyne.com | web | fundamentals, FII/DII, forecasts, results calendar |
| 🟢 Moneycontrol | https://www.moneycontrol.com | web + RSS | financials, ratios, news |
| 🟡 indianapi.in | https://indianapi.in/indian-stock-market | cheap REST key | one API: profile, prices, financials, key metrics, shareholding, corporate actions, news |
| 🟡 EODHD / Twelve Data | eodhd.com · twelvedata.com | free tier / cheap | fundamentals API (structured JSON) |

### C. EARNINGS · quarterly results (official filings)
| Source | URL | What you get |
|---|---|---|
| 🟢 BSE announcements | https://www.bseindia.com/corporates/ann.html | official results PDFs, board meetings, outcomes |
| 🟢 NSE corporate filings | https://www.nseindia.com/companies-listing/corporate-filings-announcements | official results, financial statements |
| 🟢 screener.in (Quarters tab) | per-company page | parsed quarterly revenue/PAT/margin, YoY/QoQ |
| 🟢 Trendlyne / Moneycontrol earnings calendar | | upcoming + past results dates |

### D. RECENT NEWS (per company)
| Source | URL | Access | Notes |
|---|---|---|---|
| 🟢 Google News RSS | `https://news.google.com/rss/search?q=<company>+stock` | free, no key | per-company query, dedupe by URL |
| 🟢 Moneycontrol RSS | https://www.moneycontrol.com/rss/ | free | market + company feeds |
| 🟢 ET Markets / Business Standard / Mint / Reuters India RSS | respective /rss | free | cross-source news |
| 🟢 NSE/BSE announcements | (see C) | free | events ARE news (orders, buybacks, splits) |
| 🟢 GDELT | https://www.gdeltproject.org | free API | global news event DB, tone |
| 🟡 Marketaux | https://www.marketaux.com | free 100/day incl **sentiment** | entity-tagged financial news |
| 🔴 EODHD news+sentiment · APITube · Stock News API | | cheap/paid | pre-scored sentiment, higher volume |

### E. FUTURE ROADMAP · guidance · management commentary (unstructured → LLM-extract)
| Source | URL | What you get |
|---|---|---|
| 🟢 Earnings-call transcripts | screener.in / trendlyne concall links; company IR | management guidance, capex, roadmap |
| 🟢 Investor presentations & annual reports | BSE filings + company IR pages | strategy, targets, segment outlook |
| 🟢 Results PDFs (BSE/NSE) | (see C) | guidance embedded in outcome docs |
| 🟢 SEBI / DRHP-RHP (for IPOs) | https://www.sebi.gov.in · chittorgarh.com | objects of issue, risk factors, roadmap |

### F. REFERENCE · identifiers · vocabulary
| Source | URL | Use |
|---|---|---|
| 🟢 NSE/BSE symbol & index master | nseindia.com equity list; index constituents | Company/Security backbone + sector |
| 🟢 ISIN | from NSE/BSE | **entity-resolution key** across sources |
| 🟢 FIBO ontology | https://edmcouncil.org/frameworks/industry-models/fibo | standard finance vocabulary (2,457+ classes) — reuse, don't reinvent |
| 🟢 Zerodha Varsity | https://zerodha.com/varsity | India market mechanics/definitions |
| 🟡 MCA | mca.gov.in | directors/corporate structure (paid per doc) |

**Free MVP stack (₹0):** yfinance + jugaad-data (price/EOD) · screener.in (fundamentals) · Google News + Moneycontrol RSS (news) · BSE/NSE announcements (results/roadmap) · Neo4j Community · local LLM (Ollama).
**Cheap upgrades (~₹500–1000/mo):** Angel SmartAPI (free real-time) or Kite ₹500/mo · indianapi.in (clean fundamentals) · Marketaux/EODHD (news+sentiment) · a hosted LLM API.

---

## 2. THE ARCHITECTURE (5 layers, mapped to stocks)

### Ontology (MEANING) — reuse FIBO where possible
Entities: `Company · Security · Exchange · Sector · PriceQuote(ts) · FinancialMetric(P/E,EPS,ROE…) ·
QuarterlyResult(rev,PAT,margin,YoY,QoQ) · Earnings · ShareholdingPattern · NewsEvent · Filing ·
ManagementGuidance · Person(promoter/exec)`.
Relations: `Company ISSUES Security · Security TRADES_ON Exchange · Company IN_SECTOR Sector ·
Company REPORTED QuarterlyResult · Company HAS_METRIC FinancialMetric · NewsEvent ABOUT Company ·
Filing DISCLOSES Guidance · PriceQuote OF Security AT <ts>`.
**SHACL rules (the factual guarantee):** every metric/price node MUST have `source` + `asOf`;
a "current price" is valid only if `asOf` within the freshness window; `P/E` MUST link to the
`EPS` and `PriceQuote` it was computed from.

### Knowledge Graph (MEMORY)
Ontology filled with instances, **each carrying provenance** (`source`, `asOf`, `confidence`).
**Entity resolution is critical:** unify `Reliance` / `RELIANCE.NS` / BSE `500325` / ISIN
`INE002A01018` into ONE `Company` node (dedupe on ISIN first, fuzzy name second).

### Digital Twin (LIVE SENSES) — this is where the two videos differ
- **Real-time video:** broker websocket (Angel SmartAPI / Kite ticker) streams ticks → updates
  `PriceQuote` nodes continuously.
- **15-min-delayed video:** scheduler polls yfinance/NSE every 15 min → updates `PriceQuote`.
- Fundamentals refresh nightly; news every ~15 min; results on filing. Each node type has a
  **freshness SLA**; breaching it flips the node "stale" (the agent then refuses to quote it).
- Simulation/what-if: "if P/E reverts to its 5-yr mean, implied price = EPS × meanP/E".

### Graph Engineering (THE BODY)
Construction pipelines (batch fundamentals nightly, stream prices+news), **SHACL validation gate**
(no fact enters without source+asOf), entity resolution, **text-to-Cypher** (agent's retrieval tool),
**bitemporal provenance** (price as-of any time), and a **staleness monitor** = the anti-hallucination guard.

### Agentic Engineering (THE MIND) + the anti-hallucination kit
1. **Grounded retrieval** — GraphRAG: pull only the queried company's subgraph; answer from it.
2. **Numbers-from-graph-only** — the agent may not emit a number that isn't a graph node; missing/stale → "not available as of <ts>".
3. **Deterministic math** — P/E, YoY, margins computed in **code tools**, never by the LLM.
4. **Provenance in every answer** — each fact cites `source` + `asOf`.
5. **Symbolic verify (neuro-symbolic)** — a freshness/SHACL gate validates retrieved facts before the answer is allowed.
6. **Typed MCP tools** — `price`, `fundamentals`, `results`, `news`, `filings`, `calc`; the agent has no free-form web access.
7. **Multi-factor reasoning** — assembles earnings + P/E + quarterly + news + roadmap subgraphs and reasons across them, each fact grounded+cited.
8. **Guardrails** — no buy/sell/target advice; mandatory disclaimer; refuse on stale/missing data.
Orchestration: **LangGraph** (loop + freshness-gate node) · retrieval: Neo4j GraphRAG / LlamaIndex · text-to-Cypher grounded on the ontology schema.

---

## 3. TECH STACK (free-first)
- **Graph DB:** Neo4j Community (free) or Memgraph; RDF alt: Oxigraph/GraphDB Free.
- **Ingestion:** Python — `yfinance`, `jugaad-data`, `nsepython`, `feedparser` (RSS), `requests`; schedule with APScheduler/cron; optional Kafka for streams.
- **Entity resolution:** ISIN/symbol keys + `rapidfuzz` name matching.
- **KG-from-text (news/filings/transcripts):** LLM extraction → triples → pySHACL validate → load. Local LLM via **Ollama** to cut cost.
- **Validation:** `pySHACL` (or Neo4j constraints + custom checks for property-graph).
- **Agent:** LangGraph + Neo4j-GraphRAG/LlamaIndex + **MCP** tools; LLM (Claude/GPT/local).
- **Semantic search (news):** `sentence-transformers` embeddings on `NewsEvent` nodes (hybrid retrieval).
- **Serving:** FastAPI + an MCP server exposing the typed tools.

---

## 4. STEP-BY-STEP (start Monday)
1. **Ontology (½ day):** 12–15 classes above + SHACL shapes ("every fact has source+asOf").
2. **Backbone:** Neo4j Community up; load NSE/BSE symbol master + ISIN + sector → `Company`/`Security` nodes (the entity-resolution keys).
3. **3 connectors first:** price (yfinance or Angel SmartAPI) · fundamentals (screener.in / indianapi.in) · news (Google News + Moneycontrol RSS). Each writes nodes **with provenance**.
4. **Scheduler:** price (15-min or websocket) · fundamentals nightly · news 15-min · results on filing.
5. **Derived metrics in code:** P/E, YoY, margins → nodes that **reference their inputs**.
6. **SHACL gate + staleness monitor** on every load.
7. **Agent:** text-to-Cypher retrieval → freshness gate → cite-source answer → `calc` MCP tools → LangGraph loop → disclaimer/guardrails.
8. **Eval:** a set of known-answer Q&A; measure factuality/coverage; log every fact's provenance for audit.

**Reference architectures to copy:** FIBO (vocabulary); FinReflectKG 2025 (agentic KG construction from filings — 4-layer: parse → table-aware chunk → agent triple-extraction → evaluation); Ontotext/Graphwise finance-KG write-ups; Neo4j GraphRAG.

---
*Sources: skill 12 directory; nseindia.com; github.com/jugaad-py/jugaad-data; pypi.org/project/nsepython;
yfinance; smartapi.angelbroking.com; kite.trade; screener.in; tickertape.in; trendlyne.com; indianapi.in;
twelvedata.com; marketaux.com; edmcouncil.org/frameworks/industry-models/fibo; FinReflectKG (ACM ICAIF 2025).*
