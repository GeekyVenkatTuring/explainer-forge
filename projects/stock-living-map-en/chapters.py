# -*- coding: utf-8 -*-
"""The Factual Stock Agent — screenplay (ontology · KG · digital twin · graph/agentic eng, for India NSE/BSE).

A factual, anti-hallucination agent that answers questions about a company and its stock by
reasoning over a knowledge graph whose every fact carries a source + timestamp. NOT advice.

Discipline (skill 12): no buy/sell/target calls; any specific figure on screen is ILLUSTRATIVE
and labelled; the whole thesis is "numbers come from the graph, never from the model". Disclaimer
in the title beat and the recap. Colors mirror SMLScenes (teal graph accent).
"""

GRAPH, ONT, KG, TWIN, ENG, AGENT, BAD, OK, MUT = (
    "#2DD4BF", "#FBBF24", "#22D3EE", "#A78BFA", "#34D399", "#F472B6", "#F87171", "#34D399", "#8B93B0")

DISC = "This is an educational architecture, not investment advice. Any figure shown is illustrative; consult a SEBI-registered advisor."

CHAPTERS = [
    # ================================================================= CH01
    {"id": "sml-ch01-the-problem", "title": "The Problem & The Stack", "segments": [
        {"id": "title", "variant": "sml_title", "props": {"kicker": "A GROUNDED, ANTI-HALLUCINATION STOCK AGENT",
            "sub": "ontology · knowledge graph · digital twin · agentic — strictly factual, India NSE/BSE"}, "narration":
            "You want to ask a simple question — how is a company doing right now? — and get a "
            "straight, factual answer. [pause] Not a guess. Not a vibe from a chatbot that read "
            "half a webpage. A real answer, where every number comes with a source and a "
            "timestamp. [pause] Over this course we will build exactly that: an agent for the "
            "Indian stock market that answers questions about any company — its price, its P/E, "
            "its earnings, the latest news, its roadmap — by reasoning over a knowledge graph. "
            "[pause] And critically, an agent that cannot make numbers up. [pause] One thing "
            "before we start, and I will repeat it. This is an educational architecture, not "
            "investment advice. Every figure you see is illustrative. Always consult a "
            "SEBI-registered advisor. [pause] Now — why is this so hard today?"},

        {"id": "silos", "variant": "sml_silos", "props": {}, "narration":
            "Here is the reality of researching one stock. [pause] The live price is on your "
            "broker or NSE. The P/E and fundamentals are on screener dot in. The quarterly "
            "results are a PDF on the BSE filings page. The news is scattered across a dozen "
            "sites. The company's roadmap is buried in an earnings-call transcript. And "
            "real-time ticks only come from a broker API. [pause] Six sources. To answer ‘how is "
            "TCS doing right now?’ you open six tabs, spend twenty minutes, and you are still not "
            "sure the numbers agree — or whether any of them is current. [pause] The facts "
            "existed the whole time. They were just scattered, and disconnected, with no "
            "guarantee of freshness. [pause] That gap is what we are going to close."},

        {"id": "whynow", "variant": "sml_cards", "props": {"kicker": "WHY THIS IS NOW POSSIBLE", "title": "Three things make a factual stock agent buildable today", "color": GRAPH,
            "cards": [
                {"head": "Open data + free APIs", "emoji": "🔌", "body": "yfinance, jugaad-data, screener, RSS feeds, and free broker APIs put NSE/BSE data within reach of one developer.", "tag": "access"},
                {"head": "Graphs ground LLMs", "emoji": "🎯", "body": "A knowledge graph gives the model verified facts to stand on — the fix for hallucination.", "tag": "grounding"},
                {"head": "The tooling landed", "emoji": "📏", "body": "GraphRAG, MCP, SHACL and Neo4j are production-ready — not research toys.", "tag": "mature"}],
            "foot": "You can build a personal version of this on free tiers. We'll list every source."}, "narration":
            "You might ask — if this is so useful, why isn't it everywhere? Three things just "
            "changed. [pause] First, access. Free and low-cost tools — yfinance, jugaad-data, "
            "screener, RSS news feeds, and free broker APIs like Angel One's SmartAPI — put "
            "Indian market data within reach of a single developer. [pause] Second, grounding. "
            "Language models on their own hallucinate numbers. A knowledge graph gives them "
            "verified facts to stand on — that is the fix. [pause] Third, the tooling landed. "
            "GraphRAG, the Model Context Protocol, and graph databases are production-ready today. "
            "[pause] So a personal, factual stock agent is genuinely buildable now — on free "
            "tiers. We will list every source you need."},

        {"id": "hook", "variant": "sml_hook", "props": {}, "narration":
            "Here is the core idea the whole system turns on. [pause] A price, on its own, is just "
            "a number. Is TCS at four thousand a good price? You cannot say — not without its "
            "earnings, its P/E, its peers, the latest news, and what management just guided. "
            "[pause] The meaning of any single fact lives in how it connects to the others. "
            "[pause] So instead of six disconnected tabs, we link everything: the company to its "
            "price, its price to its P/E, its P/E to its earnings, its earnings to the concall, "
            "the news to the company. [pause] Write those connections down as a graph, and a "
            "machine can finally reason across all of it at once — the way a good analyst does. "
            "[pause] That graph is the heart of the system. But a graph alone isn't enough to be "
            "trustworthy. For that, we need a full stack."},

        {"id": "stack", "variant": "sml_stack", "props": {"foot":
            "Meaning → memory → live prices → the plumbing → a cited answer. Build it bottom-up."}, "narration":
            "Five layers, and each one does a job. [pause] At the bottom, the ontology — meaning. "
            "It defines what a Company is, what a P/E is, what a QuarterlyResult is, and the rules "
            "that connect them. [pause] On top, the knowledge graph — memory. The ontology filled "
            "with real companies and their facts, every fact stamped with its source and time. "
            "[pause] Then the digital twin — live senses. The graph kept current by price feeds "
            "and news, so it reflects the market now, not last week. [pause] Then graph "
            "engineering — the plumbing that keeps it built, valid, and fast. [pause] And at the "
            "top, agentic engineering — the mind that answers your questions. [pause] Here is the "
            "punchline for the whole course. An agent without this stack invents numbers. An "
            "agent with it can only speak facts that are in the graph — each with a citation. "
            "That is the anti-hallucination kit. Part one: meaning."},
    ]},

    # ================================================================= CH02
    {"id": "sml-ch02-ontology", "title": "Ontology", "segments": [
        {"id": "divider", "variant": "sml_divider", "props": {"n": 1, "title": "Ontology", "sub": "the layer of meaning — a shared vocabulary for companies, prices, and results", "color": ONT, "layer": 0}, "narration":
            "Part one. Ontology — the layer of meaning. [pause] Before we connect anything, we "
            "have to agree on what the words mean: what a company, a price, a result actually are."},

        {"id": "vs", "variant": "sml_compare", "props": {"kicker": "WHAT AN ONTOLOGY IS", "title": "Not a spreadsheet — a model of financial meaning", "color": ONT,
            "left": {"head": "A table / spreadsheet", "sub": "structure only", "c": MUT, "rows": [
                "Rows and columns of numbers.",
                "No idea a P/E links a price to an EPS.",
                "No rule that a price needs a timestamp.",
                "Meaning lives only in your head."]},
            "right": {"head": "An ontology", "sub": "explicit meaning + rules", "c": ONT, "rows": [
                "Entities: Company, Security, PriceQuote, P/E.",
                "Relations: Company REPORTED Result.",
                "Rules: every price MUST carry a source + time.",
                "Independent of any one data vendor."]},
            "foot": "The ontology is the contract every source, query, and the agent all share."}, "narration":
            "First, what an ontology actually is — because it is not just a spreadsheet. [pause] A "
            "table is rows and columns. It has no idea that a P/E ratio links a price to an "
            "earnings figure, or that a price is meaningless without a timestamp. [pause] An "
            "ontology captures exactly that. It names the entities — Company, Security, "
            "PriceQuote, financial metric. [pause] It names the relationships — a company issues a "
            "security, a company reported a quarterly result. [pause] And it names the rules — for "
            "example, every price node must carry a source and an as-of time. That single rule is "
            "the seed of our anti-hallucination guarantee. [pause] Best of all, it is independent "
            "of any one vendor — so screener, NSE, and your broker all map to the same shared "
            "meaning."},

        {"id": "triple", "variant": "sml_triple", "props": {"kicker": "THE ATOM OF MEANING", "title": "Everything is a triple: subject → predicate → object",
            "subj": "Company", "pred": "REPORTED", "obj": "Q-Result",
            "examples": ["Company HAS_METRIC P/E", "PriceQuote OF Security", "NewsEvent ABOUT Company", "Filing DISCLOSES Guidance"],
            "foot": "Millions of these, sharing one vocabulary, become a company knowledge graph."}, "narration":
            "No matter how complex the market is, it is built from one tiny atom: the triple. "
            "Subject, predicate, object. [pause] Company — reported — quarterly result. That is a "
            "complete, machine-readable fact. [pause] And you keep adding them. A company has a "
            "metric called P/E. A price quote is of a security. A news event is about a company. "
            "A filing discloses guidance. [pause] Each triple is trivial alone, but because they "
            "all draw from the same shared vocabulary, they snap together into a fabric. [pause] "
            "String enough of them together and you no longer have scattered facts — you have a "
            "graph you can walk from any company to any fact about it."},

        {"id": "fibo", "variant": "sml_cards", "props": {"kicker": "DON'T INVENT THE VOCABULARY", "title": "Finance already has a standard ontology", "color": ONT,
            "cards": [
                {"head": "FIBO", "emoji": "🏦", "body": "The Financial Industry Business Ontology — 2,400+ classes for instruments, entities and holdings. Reuse it.", "tag": "standard"},
                {"head": "Your extension", "emoji": "🧩", "body": "Add only what's India-specific: NSE symbol, BSE scrip code, sector index membership.", "tag": "local"},
                {"head": "Definitions", "emoji": "📖", "body": "Anchor terms (P/E, EPS, ROE) to Investopedia/Varsity definitions so the meaning is unambiguous.", "tag": "clarity"}],
            "foot": "Import a standard, extend for India — months of committee argument avoided."}, "narration":
            "Here is a shortcut: you do not invent the vocabulary. Finance already standardized it. "
            "[pause] FIBO — the Financial Industry Business Ontology — has over two thousand four "
            "hundred classes for instruments, companies, and holdings. You import it. [pause] Then "
            "you extend it with only what is India-specific: the NSE symbol, the BSE scrip code, "
            "sector-index membership. [pause] And you anchor each term — P/E, EPS, return on "
            "equity — to a clear definition, from Investopedia or Zerodha Varsity, so nobody "
            "argues about what it means. [pause] Reuse a standard, extend for India. That alone "
            "saves months."},

        {"id": "code", "variant": "sml_code", "props": {"kicker": "THE FACTUAL RULE, IN SHACL", "title": "Every price must carry a source and a time — enforced", "color": ONT, "lang": "turtle",
            "lines": [
                ":PriceQuote a owl:Class .",
                ":source  a owl:DatatypeProperty .",
                ":asOf    a owl:DatatypeProperty .",
                "",
                "sh:PriceShape a sh:NodeShape ;",
                "  sh:targetClass :PriceQuote ;",
                "  sh:property [ sh:path :source ; sh:minCount 1 ] ;",
                "  sh:property [ sh:path :asOf   ; sh:minCount 1 ] ."],
            "caption": "OWL declares the concept · SHACL forbids a price with no source or time",
            "foot": "This shape is the anti-hallucination kit's foundation: a fact with no provenance can't enter."}, "narration":
            "Let me show you the single most important rule, written down. [pause] Two standards do "
            "the work. OWL declares the concepts — here, a price quote has a source and an as-of "
            "time. [pause] Then SHACL, the shapes constraint language, enforces it. This shape "
            "says: every price quote must have at least one source and at least one timestamp. "
            "[pause] Feed in a price with no provenance, and SHACL rejects it — it never enters "
            "the graph. [pause] Hold onto this. That exact rule is the foundation of the whole "
            "anti-hallucination kit: if a number cannot say where it came from and when, the "
            "system refuses to store it — and therefore the agent can never quote it."},

        {"id": "standards", "variant": "sml_orbit", "props": {"kicker": "THE ONTOLOGY TOOLBOX", "title": "The standards and tools you'll reach for", "color": ONT, "hub": "Ontology\nstack",
            "items": [
                {"emoji": "🔗", "label": "RDF — triples, global IDs"},
                {"emoji": "🦉", "label": "OWL — classes + inference"},
                {"emoji": "⚖️", "label": "SHACL — validation"},
                {"emoji": "🏦", "label": "FIBO — finance vocabulary"},
                {"emoji": "🛠️", "label": "Protégé — the editor"},
                {"emoji": "📖", "label": "Varsity — definitions"}],
            "foot": "Standards for portability; FIBO for the domain; a good editor for the humans."}, "narration":
            "The concrete toolbox. [pause] RDF is the data model — the triple, with global "
            "identifiers so two sources point at the exact same concept. [pause] OWL adds classes "
            "and inference; SHACL adds the validation we just saw. [pause] FIBO gives you the "
            "finance vocabulary out of the box. [pause] To edit it all, the classic free tool is "
            "Protégé. And for India-specific definitions, Zerodha Varsity is the reference. "
            "[pause] You do not need all of these on day one. You need the idea — shared, "
            "enforceable meaning — and one place to write it down. [pause] So, to recap part one: "
            "an ontology is the agreed vocabulary of your market, and its rules are what will keep "
            "the agent honest. Now let's fill it with real data."},
    ]},

    # ================================================================= CH03
    {"id": "sml-ch03-knowledge-graph", "title": "The Knowledge Graph", "segments": [
        {"id": "divider", "variant": "sml_divider", "props": {"n": 2, "title": "Knowledge Graph", "sub": "the layer of memory — the ontology filled with real companies and facts", "color": KG, "layer": 1}, "narration":
            "Part two. The knowledge graph — the layer of memory. [pause] An empty ontology is a "
            "template. Pour in real companies and their facts, and it comes alive."},

        {"id": "ingest", "variant": "sml_ingest", "props": {}, "narration":
            "This is where it gets real, so let's go source by source. [pause] Prices come from "
            "NSE and BSE — polled every few minutes from yfinance or jugaad-data, or streamed live "
            "from a broker API. [pause] Fundamentals — P/E, ratios, shareholding — are parsed from "
            "screener dot in. [pause] Quarterly results are official PDFs on the BSE filings page; "
            "a language model extracts the numbers. [pause] News flows in from Google News and "
            "Moneycontrol RSS feeds, with sentiment scored. [pause] Roadmap and guidance come from "
            "earnings-call transcripts, again via LLM extraction. [pause] Every source runs "
            "through a builder that extracts, resolves, and loads — and stamps each fact with its "
            "source and time. Six sources in, one connected company graph out."},

        {"id": "merge", "variant": "sml_merge", "props": {}, "narration":
            "But that raises a subtle danger. [pause] The news calls it ‘Reliance’. NSE and "
            "yfinance call it ‘RELIANCE dot N-S’. The BSE calls it scrip code five-oh-oh-three-"
            "two-five. [pause] To a naive importer, those are three different companies — and your "
            "graph is instantly polluted, your numbers double-counted. [pause] The fix is entity "
            "resolution: recognizing that all three refer to the same company and collapsing them "
            "into one node. [pause] The trick for stocks is to resolve on the ISIN first — the "
            "unique international identifier — and the name only as a fallback. [pause] Watch three "
            "names, three sources, become one canonical Reliance node. Get this right and the same "
            "company means the same thing no matter which feed it came from. Skip it, and your "
            "agent quietly contradicts itself."},

        {"id": "provenance", "variant": "sml_cards", "props": {"kicker": "THE ANTI-HALLUCINATION CORE", "title": "Every fact carries where and when it came from", "color": KG,
            "cards": [
                {"head": "Source on every fact", "emoji": "🏷️", "body": "‘P/E 29.4’ isn't stored alone — it's stored with ‘source: screener, asOf: 15:29’.", "tag": "provenance"},
                {"head": "Freshness built in", "emoji": "⏱️", "body": "A price older than its window is marked stale — the agent then refuses to quote it as current.", "tag": "freshness"},
                {"head": "Derived, not guessed", "emoji": "🧮", "body": "P/E is computed in code from a stored price and EPS, and links back to both inputs.", "tag": "audit"}],
            "foot": "This is the whole game: a number with no source + time never gets stored — so it can never be spoken."}, "narration":
            "This is the single most important scene in the course, so slow down with me. [pause] "
            "Every fact carries where and when it came from. A P/E of twenty-nine point four is not "
            "stored as a lonely number. It is stored with — source, screener; as-of, three "
            "twenty-nine PM. [pause] Freshness is built in. A price older than its window is "
            "automatically marked stale, and the agent will then refuse to present it as current. "
            "[pause] And derived numbers are computed, not guessed: the P/E is calculated in code "
            "from a stored price and a stored earnings figure, and it links straight back to both "
            "inputs. [pause] Here is the whole game in one line. A number with no source and no "
            "time never gets stored — so the agent can never speak it. That is how you make an AI "
            "factual: not by trusting it, but by only giving it facts that can prove themselves."},

        {"id": "factors", "variant": "sml_cards", "props": {"kicker": "MODELING THE FIVE FACTORS", "title": "Everything you asked to reason over — as graph nodes", "color": KG,
            "cards": [
                {"head": "Earnings & P/E", "emoji": "💰", "body": "EPS, PAT, and P/E as metric nodes, each linked to the price and result they derive from.", "tag": "valuation"},
                {"head": "Quarterly results", "emoji": "📑", "body": "Revenue, PAT, margins per quarter, with YoY and QoQ computed and stored.", "tag": "growth"},
                {"head": "News & roadmap", "emoji": "📰", "body": "NewsEvent nodes with sentiment; ManagementGuidance extracted from concalls.", "tag": "context"}],
            "foot": "Five factors, one graph — so the agent can weigh them together, each fact cited."}, "narration":
            "Let's map the exact factors you want the agent to reason over — because each one "
            "becomes nodes in this graph. [pause] Earnings and valuation: EPS, profit, and the P/E, "
            "each linked back to the price and the result it came from. [pause] Growth: revenue, "
            "profit, and margins for every quarter, with year-on-year and quarter-on-quarter "
            "changes computed and stored. [pause] And context: news events, each with a sentiment "
            "score, plus management guidance extracted from the earnings call — that's your future "
            "roadmap. [pause] Put all five factors in one graph, and the agent can finally weigh "
            "them together — earnings against valuation against the latest news — with every "
            "single fact cited. That is multi-factor reasoning, grounded."},

        {"id": "cypher", "variant": "sml_code", "props": {"kicker": "ONE QUERY, MANY FACTS", "title": "Ask for a whole company view in a single graph query", "color": KG, "lang": "cypher",
            "lines": [
                "MATCH (c:Company {isin:'INE467B01029'})",
                "OPTIONAL MATCH (c)-[:HAS_METRIC]->(m)",
                "OPTIONAL MATCH (c)-[:REPORTED]->(q:Quarter)",
                "OPTIONAL MATCH (n:News)-[:ABOUT]->(c)",
                "WHERE n.asOf > datetime() - duration('P7D')",
                "RETURN c, m, q, n"],
            "result": ["TCS", "P/E 29.4", "Q3 PAT +12%", "2 news · 7d"],
            "caption": "one traversal gathers price, metrics, results and recent news — all with provenance",
            "foot": "The agent's main tool: turn a question into a query, get back facts with sources attached."}, "narration":
            "Now the payoff of a graph over six tabs. [pause] To pull a whole company view, it's a "
            "single query. Start at the company by its ISIN, then gather its metrics, its latest "
            "quarter, and any news from the last seven days. [pause] This is Cypher, but read it as "
            "English: get me this company and everything currently attached to it. [pause] Back "
            "comes the P/E, the latest result, the recent news — each row carrying its source and "
            "timestamp. [pause] No single website could answer that in one shot, because the "
            "answer lived in the connections. This one query is what the agent will run under the "
            "hood — and it is why the answer can always be cited."},

        {"id": "graphrag", "variant": "sml_chart", "props": {"kicker": "GROUNDED vs UNGROUNDED", "title": "Why grounding on the graph beats a model guessing", "color": KG,
            "bars": [{"label": "LLM alone (guessing)", "v": 32, "c": BAD}, {"label": "Graph-grounded (GraphRAG)", "v": 86, "c": KG}],
            "note": "illustrative — accuracy on grounded, multi-hop financial questions",
            "foot": "The graph doesn't just find similar text — it returns the exact, sourced fact."}, "narration":
            "Here is the difference grounding makes. [pause] Ask a language model on its own for a "
            "company's numbers and it will confidently produce something — often wrong, sometimes "
            "months stale. On grounded, multi-hop financial questions, that approach is unreliable. "
            "[pause] Retrieve from a knowledge graph instead — an approach called GraphRAG — and "
            "the model is handed the exact, sourced fact. Accuracy jumps dramatically. [pause] "
            "These bars are illustrative, but the direction is the whole point: the graph does not "
            "find text that sounds right, it returns the number that is right, with its citation. "
            "[pause] So, to recap part two: the knowledge graph is your ontology filled with "
            "resolved, sourced, timestamped facts — and it is what lets the agent answer without "
            "guessing. Next, we make it live."},
    ]},

    # ================================================================= CH04
    {"id": "sml-ch04-digital-twin", "title": "The Digital Twin", "segments": [
        {"id": "divider", "variant": "sml_divider", "props": {"n": 3, "title": "Digital Twin", "sub": "the layer of live senses — the graph kept current with the market", "color": TWIN, "layer": 2}, "narration":
            "Part three. The digital twin — the layer of live senses. [pause] A knowledge graph "
            "tells you how a company is wired. A twin tells you how it's doing right now."},

        {"id": "telemetry", "variant": "sml_telemetry", "props": {}, "narration":
            "Here is the twin breathing. [pause] Each node is a live instrument — Reliance, TCS, "
            "HDFC Bank, Infosys, the Nifty index. Price updates stream in and the colours change: "
            "green for up, red for down. [pause] This is the same graph from part two, but now it "
            "is a live picture, with meaning baked in. [pause] The crucial detail: every value "
            "carries its as-of time. So the twin doesn't just say ‘the price is four thousand’ — "
            "it says ‘four thousand, as of fifteen twenty-nine, from NSE’. [pause] And when a feed "
            "goes quiet, the node knows it is stale, and the agent will say so rather than quote a "
            "frozen number. A live model that is honest about how live it actually is."},

        {"id": "syncarch", "variant": "sml_pipeline", "props": {"kicker": "TWO WAYS TO STAY CURRENT", "title": "Real-time ticks, or a 15-minute refresh — same graph", "color": TWIN,
            "nodes": [
                {"emoji": "⚡", "label": "Real-time", "sub": "broker websocket", "c": BAD},
                {"emoji": "🕒", "label": "15-min", "sub": "poll yfinance/NSE", "c": KG},
                {"emoji": "🔁", "label": "Update rule", "sub": "write PriceQuote", "c": ONT},
                {"emoji": "🕸️", "label": "Live twin", "sub": "with asOf time", "c": TWIN}],
            "foot": "Real-time needs a broker/data subscription; 15-min delayed runs on free tiers. We'll build both."}, "narration":
            "Now, how fresh is ‘current’? There are two modes, and they define our two videos. "
            "[pause] Real-time: a broker websocket — Angel One's SmartAPI or Zerodha's Kite ticker "
            "— streams live ticks straight into the graph, tick by tick. That needs a broker "
            "account or a data subscription. [pause] Or fifteen-minute delayed: a scheduler polls "
            "a free source like yfinance or the NSE site every few minutes. It runs on free tiers, "
            "and for research and analysis it is perfectly fine. [pause] Either way, the update "
            "rule is the same: write a new price-quote node, stamped with its as-of time. [pause] "
            "Same graph, same agent — only the freshness of the price changes. We'll build the "
            "real-time deep-dive as a separate video; here, either mode plugs into the same twin."},

        {"id": "maturity", "variant": "sml_tower", "props": {"kicker": "THE MATURITY LADDER", "title": "From ‘what is the price’ to ‘what does it all mean’", "color": TWIN,
            "levels": [
                {"label": "Descriptive", "sub": "the current price & metrics"},
                {"label": "Informational", "sub": "history, YoY, trends"},
                {"label": "Comparative", "sub": "vs peers and sector"},
                {"label": "Explanatory", "sub": "why it moved, from news"},
                {"label": "Analytical", "sub": "weigh all factors, cited"}],
            "foot": "We're building toward the top rung — and every rung still answers from the graph."}, "narration":
            "A factual agent climbs a ladder of usefulness. [pause] Rung one, descriptive: it "
            "tells you the current price and metrics. [pause] Rung two, informational: it adds "
            "history — the year-on-year growth, the trend. [pause] Rung three, comparative: it "
            "places the company against its peers and its sector. [pause] Rung four, explanatory: "
            "it links a price move to the news that drove it. [pause] And rung five, analytical: it "
            "weighs all the factors together — earnings, valuation, growth, news, guidance — into "
            "a grounded, cited view. [pause] Notice what it never does: give you a buy or sell "
            "call. It informs; you decide. And every rung, top to bottom, answers only from the "
            "graph."},

        {"id": "cascade", "variant": "sml_cascade", "props": {}, "narration":
            "Here is where a twin does something a spreadsheet cannot: simulation. [pause] Suppose "
            "crude oil jumps ten percent. Which of your watchlist names are exposed? [pause] "
            "Because the graph already links companies to sectors, and sectors to their cost "
            "drivers, the shock propagates along real edges. Crude up, input costs up — and it "
            "flows to the crude-sensitive sectors, and from there to the specific companies in "
            "them. [pause] Watch it spread: driver, sectors, holdings — flagged before the market "
            "opens. [pause] Now, an honest caveat, and it matters. This is illustrative. It traces "
            "links that are in the graph — it is not a prediction of where prices will go. [pause] "
            "So, to recap part three: the digital twin is your graph kept live, honest about "
            "freshness, and able to trace what connects to what. Now, the engineering that keeps "
            "it all trustworthy."},
    ]},

    # ================================================================= CH05
    {"id": "sml-ch05-graph-engineering", "title": "Graph Engineering", "segments": [
        {"id": "divider", "variant": "sml_divider", "props": {"n": 4, "title": "Graph Engineering", "sub": "the plumbing — building, validating and querying the graph at scale", "color": ENG, "layer": 3}, "narration":
            "Part four. Graph engineering — the plumbing. [pause] Everything so far assumed the "
            "graph is correct and current. That doesn't happen by accident. It's a craft."},

        {"id": "disciplines", "variant": "sml_orbit", "props": {"kicker": "THE CRAFT", "title": "What keeps a market graph trustworthy", "color": ENG, "hub": "Graph\nEngineering",
            "items": [
                {"emoji": "📐", "label": "Ontology & schema design"},
                {"emoji": "🏗️", "label": "Ingestion pipelines"},
                {"emoji": "🔗", "label": "Entity resolution (ISIN)"},
                {"emoji": "⚖️", "label": "Validation & freshness"},
                {"emoji": "🗂️", "label": "Provenance & versioning"},
                {"emoji": "🧠", "label": "Graph ML (peers, sectors)"}],
            "foot": "It's data engineering — but the product is trustworthy facts, and they must stay true."}, "narration":
            "So what does keeping this graph trustworthy actually involve? Six things. [pause] "
            "Designing the ontology. Building the ingestion pipelines from every source. [pause] "
            "Entity resolution — keeping duplicates out with the ISIN. [pause] Validation and "
            "freshness — the SHACL rules that reject bad or stale data. [pause] Provenance and "
            "versioning — so you can prove where every number came from, and what the graph "
            "believed at any point in time. [pause] And graph machine learning — finding peers and "
            "sector relationships from the structure itself. [pause] It's data engineering, but "
            "the product isn't a dashboard — it's trustworthy facts. And they have to stay true, "
            "continuously. Two of these deserve a closer look."},

        {"id": "validation", "variant": "sml_code", "props": {"kicker": "THE FRESHNESS GATE", "title": "Stale or source-less data fails the load — automatically", "color": ENG, "lang": "shacl / ci",
            "lines": [
                "# on every ingest, before publish:",
                "validate(candidate_graph, shapes)",
                "",
                "✗ PriceQuote(TCS) rejected",
                "  → :asOf is 41 min old (limit 15)",
                "✗ Metric(P/E) rejected",
                "  → :source missing",
                "LOAD BLOCKED · bad facts never enter"],
            "result": ["1,842 facts", "checked", "2 rejected", "graph stays clean"],
            "caption": "the SHACL rules from part one, now guarding every single load",
            "foot": "This gate is the anti-hallucination kit in code: the agent can only see facts that passed."}, "narration":
            "Remember the SHACL rule from part one — every price needs a source and a fresh "
            "timestamp? Here is where it earns its keep. [pause] On every single load, before "
            "anything is published, the candidate facts are checked. [pause] Look: a TCS price is "
            "rejected because its timestamp is forty-one minutes old, past the fifteen-minute "
            "limit. A P/E is rejected because it has no source. [pause] Neither one enters the "
            "graph. [pause] This is the anti-hallucination kit, but now in running code. The agent "
            "can only ever see facts that passed this gate — so it is structurally incapable of "
            "quoting a stale or source-less number. [pause] You don't ask the model to be careful. "
            "You make it impossible for it to be careless."},

        {"id": "text2cypher", "variant": "sml_code", "props": {"kicker": "TEXT-TO-CYPHER", "title": "The user asks in English; the ontology keeps the query honest", "color": ENG, "lang": "python + cypher",
            "lines": [
                "# user: “what's Infosys P/E and last quarter?”",
                "cypher = llm.to_cypher(question, schema=ONTOLOGY)",
                "",
                "MATCH (c:Company {name:'Infosys'})",
                "  -[:HAS_METRIC]->(pe:Metric {kind:'P/E'})",
                "MATCH (c)-[:REPORTED]->(q:Quarter)",
                "RETURN pe.value, pe.asOf, q  // validated"],
            "result": ["P/E 24.1", "asOf 15:29", "Q3 shown"],
            "caption": "the ontology is the schema that stops the model inventing fields",
            "foot": "Anyone can ask in plain English — and only valid, grounded queries ever run."}, "narration":
            "How does a non-programmer ask the graph anything? Text-to-Cypher. [pause] The user "
            "types in plain English — what's Infosys's P/E and last quarter? [pause] A language "
            "model translates it into a graph query, but — and this is the key — it is handed the "
            "ontology as the schema. So it knows the real fields: a company has a metric, a company "
            "reported a quarter. [pause] It writes a correct query, which is validated against the "
            "ontology before it runs. A hallucinated field name simply fails. [pause] Back come the "
            "P/E, its as-of time, and the quarter. [pause] Anyone can ask in plain language — and "
            "only valid, grounded queries ever touch the data. This is the agent's single most "
            "important tool."},

        {"id": "gnn", "variant": "sml_gnn", "props": {"foot":
            "Learn peer groups, sector clusters, and anomalies from the graph's own structure."}, "narration":
            "One more capability: learning from the graph's shape, using graph neural networks. "
            "[pause] The idea is simple — each company learns from its neighbours: the sector it's "
            "in, the peers it trades with, the funds that hold it. [pause] Watch the signal spread "
            "outward, one ring at a time. After a few hops, each company holds a rich summary of "
            "its whole neighbourhood. [pause] Why does that matter for stocks? It finds true peer "
            "groups — not just the obvious ones — spots companies behaving unlike their sector, and "
            "surfaces hidden links through shared ownership. [pause] So, to recap part four: graph "
            "engineering builds, validates, queries, and learns from the graph, so every layer "
            "above it can trust it. Which brings us to the agent itself."},
    ]},

    # ================================================================= CH06
    {"id": "sml-ch06-agentic", "title": "Agentic Engineering", "segments": [
        {"id": "divider", "variant": "sml_divider", "props": {"n": 5, "title": "Agentic Engineering", "sub": "the acting mind — an agent that retrieves, reasons, and answers with citations", "color": AGENT, "layer": 4}, "narration":
            "Part five. Agentic engineering — the acting mind. [pause] Now we put an AI on top of "
            "everything, and the whole design finally pays off."},

        {"id": "loop", "variant": "sml_agentloop", "props": {}, "narration":
            "The agent runs a simple loop: observe, reason, answer. [pause] What makes it factual "
            "is what it does at each step. [pause] It observes the knowledge graph and the live "
            "twin — the real, current facts about the company. [pause] It reasons by walking the "
            "graph across the five factors — price, valuation, growth, news, guidance — the way an "
            "analyst would. [pause] And it answers with citations — every figure carrying its "
            "source and time, and never a number that isn't in the graph. [pause] Notice it does "
            "not place trades and it does not give advice. It informs, factually, and you decide. "
            "[pause] Strip the graph away and this loop is just a chatbot inventing numbers. Wrap "
            "it around the graph, and it becomes a research assistant you can actually trust. "
            "Let's unpack how."},

        {"id": "kit", "variant": "sml_cards", "props": {"kicker": "THE ANTI-HALLUCINATION KIT", "title": "The six rules that make the agent factual", "color": AGENT,
            "cards": [
                {"head": "Answer from the graph only", "emoji": "🎯", "body": "GraphRAG retrieves the company's subgraph; the agent may not emit a number that isn't a node.", "tag": "grounding"},
                {"head": "Cite source + time", "emoji": "🏷️", "body": "Every figure shows where and when it came from. Missing or stale → ‘not available as of…’.", "tag": "provenance"},
                {"head": "Math in code", "emoji": "🧮", "body": "P/E, YoY, margins computed by a tool, never by the model.", "tag": "no-arithmetic"},
                {"head": "Verify before answer", "emoji": "⚖️", "body": "A freshness/SHACL gate checks the facts; typed tools only; no free web access; no advice.", "tag": "guardrails"}],
            "foot": "None of these trusts the model. Each one makes it structurally unable to make things up."}, "narration":
            "This is the heart of the whole course — the anti-hallucination kit, in four rules. "
            "[pause] One: answer from the graph only. The agent retrieves the company's subgraph "
            "and may not emit a number that isn't a node in it. [pause] Two: cite source and time "
            "on every figure. If a fact is missing or stale, it says ‘not available as of’ — never "
            "a guess. [pause] Three: do the math in code. P/E, year-on-year, margins are computed "
            "by a tool, never by the model — because models are bad at arithmetic and good at "
            "sounding confident. [pause] Four: verify before answering. A freshness gate checks "
            "every fact; the agent has only typed tools, no open web, and never gives advice. "
            "[pause] Notice not one of these asks the model to behave. Each one makes it "
            "structurally unable to misbehave. That is the difference between a demo and something "
            "you'd rely on."},

        {"id": "twobrain", "variant": "sml_twobrain", "props": {"foot":
            "The model drafts the answer; the graph's rules verify every fact before it's shown."}, "narration":
            "The pattern behind that is called neuro-symbolic — two brains working together. "
            "[pause] On the left, the language model. Flexible and fluent. It reads your question, "
            "gathers the facts, and drafts a clear answer. [pause] But on its own, it can "
            "hallucinate. [pause] So on the right, a symbolic brain: the freshness and SHACL rules. "
            "It doesn't write prose — it checks. Is every number in the draft actually a graph "
            "node, with a source and a fresh timestamp? [pause] Only a verified draft is allowed "
            "through. [pause] Fluency from the model, guarantees from the graph. Neither half is "
            "trustworthy alone; together, they are the architecture behind any serious factual AI."},

        {"id": "frameworks", "variant": "sml_orbit", "props": {"kicker": "THE TOOLKIT", "title": "The frameworks you'll wire together", "color": AGENT, "hub": "Agent\n+ graph",
            "items": [
                {"emoji": "🔀", "label": "LangGraph — control + gate"},
                {"emoji": "📚", "label": "LlamaIndex — retrieval"},
                {"emoji": "🕸️", "label": "Neo4j GraphRAG"},
                {"emoji": "🔌", "label": "MCP — the tools"},
                {"emoji": "🧠", "label": "Ollama — local LLM"},
                {"emoji": "⚡", "label": "FastAPI — serve it"}],
            "foot": "Free-first: Neo4j Community + GraphRAG + LangGraph + a local model = ₹0 to prototype."}, "narration":
            "You don't build this from scratch — you compose it, and mostly from free parts. "
            "[pause] LangGraph gives you the control flow, including that all-important verification "
            "gate as a step the agent must pass. [pause] LlamaIndex and Neo4j's GraphRAG handle "
            "retrieval from the graph. [pause] MCP — the Model Context Protocol — is how the agent "
            "gets its tools. [pause] For the model itself, you can run a local one with Ollama to "
            "keep costs at zero while prototyping. [pause] And FastAPI serves the whole thing. "
            "[pause] Neo4j Community, GraphRAG, LangGraph, and a local model — that's a real "
            "prototype for zero rupees. Now, the tools the agent actually uses."},

        {"id": "mcptools", "variant": "sml_orbit", "props": {"kicker": "MCP · THE AGENT'S TOOLS", "title": "Each source becomes a typed, permissioned tool", "color": AGENT, "hub": "Agent",
            "items": [
                {"emoji": "📈", "label": "price — live / delayed quote"},
                {"emoji": "📊", "label": "fundamentals — P/E, ratios"},
                {"emoji": "📑", "label": "results — quarterly filings"},
                {"emoji": "📰", "label": "news — recent + sentiment"},
                {"emoji": "🎤", "label": "guidance — concall extract"},
                {"emoji": "🧮", "label": "calc — P/E, YoY, margins"}],
            "foot": "Typed tools only — no open web. The agent literally cannot fetch an unverified number."}, "narration":
            "Here are the agent's hands — its tools, exposed through MCP. [pause] A price tool for "
            "the live or delayed quote. A fundamentals tool for P/E and ratios. A results tool for "
            "the quarterly filings. A news tool with sentiment. A guidance tool that reads the "
            "concall. And a calc tool that does the arithmetic deterministically. [pause] Notice "
            "what is not on this list: an open web browser. The agent has typed tools and nothing "
            "else. [pause] It literally cannot reach out and grab an unverified number off a random "
            "page — every fact must come through a tool that stamps it with a source. That "
            "restriction is a feature, not a limitation. Now, let's put it all together on a real "
            "question."},

        {"id": "traverse", "variant": "sml_traverse", "props": {}, "narration":
            "Twenty minutes and six tabs ago, ‘how is TCS doing?’ was a chore. Watch what it is "
            "now. [pause] You ask: analyze TCS. [pause] The agent pulls the price — four thousand "
            "one oh two, from NSE, as of fifteen twenty-nine. [pause] The P/E — twenty-nine point "
            "four, from screener. [pause] The latest quarter — profit up twelve percent year on "
            "year, from the BSE filing. [pause] Two recent news items, from Moneycontrol. [pause] "
            "And the guidance from the last concall — margins steady. [pause] Then it composes one "
            "grounded answer, where every single figure carries its source and its timestamp. Zero "
            "uncited numbers. Zero guesses. [pause] If a fact were missing or stale, it would say "
            "so, not invent it. [pause] Retrieve from the graph, reason over the factors, answer "
            "with citations. That is the entire video, working as one. [pause] So, to recap part "
            "five: an agent grounded on this stack is trustworthy because the graph gives it "
            "facts, freshness, and citations. Let's assemble the whole picture."},
    ]},

    # ================================================================= CH07
    {"id": "sml-ch07-together", "title": "Putting It Together", "segments": [
        {"id": "divider", "variant": "sml_divider", "props": {"n": 6, "title": "Put It Together", "sub": "the full architecture, an adoption path, and how to start", "color": GRAPH, "layer": -1}, "narration":
            "Part six. Putting it together. [pause] Let's zoom out, see the whole machine, and "
            "figure out how you actually start building it."},

        {"id": "architecture", "variant": "sml_architecture", "props": {}, "narration":
            "Here is the entire architecture on one screen. [pause] At the bottom, your six "
            "sources — prices, fundamentals, filings, news, concalls, and the broker feed — flow "
            "upward. [pause] They feed the ontology, which gives them shared meaning. [pause] The "
            "ontology, filled with resolved and sourced data, becomes the knowledge graph. [pause] "
            "Live feeds turn it into a digital twin. [pause] Graph engineering keeps it built, "
            "valid, and fresh. [pause] And at the top, the agent reasons across every layer and "
            "answers you — with citations. [pause] Follow the flow up the spine: raw, scattered "
            "data enters at the bottom, and a single grounded, cited answer comes out the top. "
            "[pause] Every layer earns its place, and each makes the next one possible."},

        {"id": "adopt", "variant": "sml_timeline", "props": {"kicker": "START THIS WEEKEND", "title": "Build one layer at a time — each is useful on its own", "color": GRAPH,
            "steps": [
                {"label": "Ontology + Neo4j", "sub": "12 classes, SHACL freshness rule, symbol+ISIN backbone"},
                {"label": "3 free connectors", "sub": "yfinance price, screener fundamentals, Google-News RSS"},
                {"label": "Make it live", "sub": "poll every 15 min; add stale flags → a twin"},
                {"label": "The agent", "sub": "text-to-Cypher + calc tool + cite-source + guardrails"}],
            "foot": "Each step ships value before the next. A single engineer can reach step 4 in weeks."}, "narration":
            "This is not a moonshot. You build it one layer at a time, and each layer is useful "
            "before the next exists. [pause] Step one: a small ontology — twelve classes — with the "
            "freshness rule, on Neo4j Community, seeded with the NSE symbol list and ISINs. [pause] "
            "Step two: wire three free connectors — yfinance for price, screener for fundamentals, "
            "Google News for headlines. Each writes facts with provenance. [pause] Step three: poll "
            "every fifteen minutes and add stale flags — now you have a twin. [pause] Step four: "
            "the agent — text-to-Cypher, a calc tool, cite-your-source, and the no-advice "
            "guardrails. [pause] Meaning first, then memory, then live senses, then the mind. Skip "
            "ahead and bolt a chatbot onto raw data, and you get exactly the confident, wrong "
            "answers we set out to avoid. Build in order, and each step earns the next."},

        {"id": "pitfalls", "variant": "sml_cards", "props": {"kicker": "WHAT GOES WRONG", "title": "The four traps to design against", "color": BAD,
            "cards": [
                {"head": "Trusting a scraped number", "emoji": "🕳️", "body": "Web-scraped figures go stale and wrong. Prefer structured APIs; always store source + time.", "tag": "data"},
                {"head": "No entity resolution", "emoji": "👥", "body": "Skip the ISIN merge and you double-count and contradict yourself.", "tag": "graph"},
                {"head": "The stale twin", "emoji": "🕰️", "body": "A feed dies, the graph keeps the old price, the agent quotes it. Freshness flags prevent this.", "tag": "twin"},
                {"head": "Drifting into advice", "emoji": "⚠️", "body": "The moment it says ‘buy’, you have a compliance problem. Inform, cite, disclaim — never advise.", "tag": "legal"}],
            "foot": "Every one of these is a discipline choice, not a technology limit."}, "narration":
            "Let me save you some pain. Four traps. [pause] One: trusting a scraped number. "
            "Web-scraped figures go stale and wrong; prefer structured APIs, and always store the "
            "source and time. [pause] Two: skipping entity resolution. Without the ISIN merge, you "
            "double-count and the agent contradicts itself. [pause] Three: the stale twin. A feed "
            "dies, the graph holds the old price, and the agent quotes it as current — which is "
            "why the freshness flag is non-negotiable. [pause] Four: drifting into advice. The "
            "moment your system says ‘buy’, you have a regulatory problem. Inform, cite, and "
            "disclaim — never advise. [pause] Notice: every one of these is a discipline choice, "
            "not a technology limit. Which means every one is in your control."},

        {"id": "buildbuy", "variant": "sml_compare", "props": {"kicker": "FREE-FIRST, CHEAP-PAID", "title": "Where free is enough, and where a little money helps", "color": GRAPH,
            "left": {"head": "Free tier (start here)", "sub": "₹0", "c": ENG, "rows": [
                "yfinance / jugaad-data — delayed prices.",
                "screener / Tickertape — fundamentals.",
                "Google News + Moneycontrol RSS — news.",
                "Neo4j Community + Ollama — graph + model."]},
            "right": {"head": "Small paid upgrades", "sub": "~₹500–1000/mo", "c": AGENT, "rows": [
                "Angel SmartAPI (free) / Kite ₹500 — real-time.",
                "indianapi.in — clean fundamentals API.",
                "Marketaux / EODHD — news + sentiment.",
                "A hosted LLM API — better answers."]},
            "foot": "Prototype for free; pay only for real-time ticks and cleaner data when you need them."}, "narration":
            "On cost — because you asked for free-first. [pause] You can prototype the entire "
            "system for zero rupees. yfinance and jugaad-data for delayed prices. Screener and "
            "Tickertape for fundamentals. Google News and Moneycontrol RSS for news. Neo4j "
            "Community for the graph, and a local model through Ollama. [pause] Then, small paid "
            "upgrades where they earn it. Angel One's SmartAPI is free for real-time; Zerodha's "
            "Kite is five hundred rupees a month. indianapi.in gives cleaner fundamentals through "
            "one API. Marketaux or EODHD add scored news. And a hosted model gives better answers. "
            "[pause] The rule: prototype for free, and pay only for real-time ticks and cleaner "
            "data once you actually need them. Every source is in the plan doc alongside this "
            "video."},

        {"id": "recap", "variant": "sml_recap", "props": {"kicker": "RECAP · THE WHOLE MAP", "title": "The factual stock agent in one breath", "closer": "Give the machine only facts that can prove themselves — and it stops guessing.",
            "items": [
                "Ontology = meaning: the vocabulary, and the rule that every fact needs a source + time.",
                "Knowledge graph = memory: companies and factors, each fact sourced and timestamped.",
                "Digital twin = live senses: prices kept current (real-time or 15-min), honest about staleness.",
                "Graph engineering = the plumbing: pipelines, the freshness gate, entity resolution, graph ML.",
                "Agentic engineering = the mind: retrieve, reason over five factors, answer with citations.",
                "Anti-hallucination kit: graph-only answers, cited, math in code — and never investment advice."]}, "narration":
            "Let's hold the whole map in one breath. [pause] Ontology is meaning — the vocabulary, "
            "and the rule that every fact needs a source and a time. [pause] The knowledge graph "
            "is memory — companies and their factors, each fact sourced and timestamped. [pause] "
            "The digital twin is live senses — prices kept current, real-time or delayed, and "
            "honest about staleness. [pause] Graph engineering is the plumbing — the pipelines, "
            "the freshness gate, entity resolution, and graph learning. [pause] And agentic "
            "engineering is the mind — retrieve, reason over the five factors, and answer with "
            "citations. [pause] The thread through all of it is the anti-hallucination kit: "
            "graph-only answers, every number cited, arithmetic in code — and never, ever, "
            "investment advice. [pause] One last time: this is an educational architecture, not "
            "advice; consult a SEBI-registered advisor. [pause] Give the machine only facts that "
            "can prove themselves — and it stops guessing. Thanks for watching."},
    ]},
]
