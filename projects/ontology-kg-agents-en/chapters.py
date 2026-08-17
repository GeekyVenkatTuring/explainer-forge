# -*- coding: utf-8 -*-
"""The Living Map — screenplay (ontology · KG · digital twin · graph & agentic eng).

Each chapter renders to its own MP4; all concat into the master. A chapter is a list
of scene segments: {id, variant, props, narration}. Narration is SPOKEN language
(numbers as words), with [pause] (0.6s) after new terms / big numbers / key ideas.
Every on-screen element is mentioned in its beat, phased to ~when it is said.

Running example threaded throughout: ONE project whose knowledge lives in six silos —
ADO Wiki, ADO Repo, Azure SQL, Cosmos DB, Blob Storage, AKS logs.

Semantic colors (KGScenes.A): ONT amber · KG cyan · TWIN violet · ENG green ·
AGENT pink · GRAPH indigo · BAD red. ~43 scenes · 6 parts · target ~62 min.
"""

GRAPH, ONT, KG, TWIN, ENG, AGENT, BAD, OK, MUT = (
    "#818CF8", "#FBBF24", "#22D3EE", "#A78BFA", "#34D399", "#F472B6", "#F87171", "#34D399", "#8B93B0")


CHAPTERS = [
    # ========================================================= CH01 — PROBLEM & STACK
    {"id": "kg-ch01-the-problem", "title": "The Problem & The Stack", "segments": [
        {"id": "title", "variant": "kg_title", "props": {}, "narration":
            "Every serious software team has the same quiet problem. [pause] Not a lack of data — "
            "the opposite. Too much of it, scattered everywhere, and none of it talking to each "
            "other. [pause] Over the next hour we are going to fix that, for real. We will connect "
            "five ideas that are usually taught in separate corners of the internet — ontologies, "
            "knowledge graphs, digital twins, graph engineering, and agentic engineering. [pause] "
            "And we will build them into one thing you can use on a normal Tuesday: a living map "
            "of your own system that an AI agent can read, reason over, and safely act on. [pause] "
            "This is not a glossary. It is an architecture. Let's start with the pain."},

        {"id": "silos", "variant": "kg_silos", "props": {}, "narration":
            "Here is a real project — maybe yours. [pause] The architecture and design decisions "
            "live in an Azure DevOps wiki. [pause] The report definitions and SQL live in a "
            "DevOps repo. [pause] The business data is split across Azure SQL and Cosmos DB. "
            "[pause] Images and assets sit in Blob storage. And the runtime logs stream out of "
            "your Kubernetes cluster. [pause] Six systems. Each one perfectly good on its own. "
            "[pause] Now a stakeholder asks a simple question: report X is showing wrong numbers "
            "— why? [pause] To answer, you open six tabs. You read the wiki, grep the logs, check "
            "the schema, skim the repo, and ping three colleagues on Slack. [pause] The knowledge "
            "to answer existed the whole time. It was just never connected. That gap — between "
            "data you have and meaning you can use — is what this entire video is about."},

        {"id": "whynow", "variant": "kg_cards", "props": {"kicker": "WHY THIS, WHY NOW", "title": "Three walls just fell — that's why this is worth your hour", "color": GRAPH,
            "cards": [
                {"head": "Construction got cheap", "emoji": "🤖", "body": "Building a graph from messy wikis and code used to need a team of analysts. A language model now extracts the entities and links in an afternoon.", "tag": "2023 →"},
                {"head": "Agents hit a wall", "emoji": "🎯", "body": "Everyone shipped chatbots; everyone learned a model with no world just makes things up. A graph is the grounding that fixes it.", "tag": "the wall"},
                {"head": "The standards landed", "emoji": "📏", "body": "GQL became an ISO standard in 2024. GraphRAG, MCP and SHACL are production-ready today — not research toys.", "tag": "mature"}],
            "foot": "For a decade this was a rich-company secret. The tooling finally reached the rest of us."}, "narration":
            "You might reasonably ask — if these ideas are so powerful, why aren't they everywhere "
            "already? [pause] They were, quietly, inside a few giant companies. What changed is that "
            "three walls just fell. [pause] First, construction got cheap. Building a graph from "
            "messy wikis and code used to take a team of analysts a year. Now a language model "
            "extracts the entities and relationships for you, in an afternoon. [pause] Second, the "
            "agent boom hit a wall. Everyone shipped a chatbot, and everyone discovered the same "
            "thing — a model with no grounded world just makes things up. A knowledge graph is the "
            "grounding that fixes it. [pause] And third, the standards landed. GQL became an ISO "
            "standard in twenty twenty-four. GraphRAG, the Model Context Protocol, and SHACL are "
            "production-ready today. [pause] For a decade this was a rich-company secret. The "
            "tooling finally reached the rest of us — which is exactly why it's worth the next hour."},

        {"id": "hook", "variant": "kg_hook", "props": {}, "narration":
            "So here is the hinge the whole field turns on. [pause] Raw data answers the question "
            "‘what’. What rows, what files, what log lines. [pause] But almost every real question "
            "is a ‘so what’. Why did this break, what depends on that, who owns this. [pause] And "
            "‘so what’ does not live inside any single table. It lives in the connections between "
            "them. [pause] A report USES a query. A query READS a table. A table was CHANGED by a "
            "migration. A pod EMITTED an error. [pause] Write those connections down, explicitly, "
            "as nodes and edges — and something remarkable happens. A machine can now follow the "
            "trail the way a senior engineer would. [pause] That is a knowledge graph. And it is "
            "the beating heart of everything ahead. [pause] But a graph alone is not enough. To "
            "make it trustworthy, to make it live, and to let an agent act on it — we need a full "
            "stack. Let me show you the shape of it."},

        {"id": "stack", "variant": "kg_stack", "props": {"foot":
            "Meaning → memory → live senses → the body → the acting mind. Build it bottom-up."}, "narration":
            "Five layers, and each one earns its place. [pause] At the bottom, the ontology. This "
            "is meaning — the shared grammar. It says what a Report is, what a Table is, and the "
            "rules that connect them. Think of it as the dictionary everything else agrees on. "
            "[pause] On top of that, the knowledge graph. This is memory — the ontology filled "
            "with your actual instances and their links. The living map. [pause] Next, the digital "
            "twin. This is live senses — the graph kept in sync with reality by telemetry, so it "
            "reflects the system as it is right now, and can even simulate what-if. [pause] Then "
            "graph engineering — the body. The unglamorous craft of building and running all this "
            "at scale: pipelines, validation, queries, graph machine learning. [pause] And at the "
            "top, agentic engineering — the acting mind. AI agents that read the graph, reason "
            "across it, and take safe, governed actions. [pause] Here is the punchline for the "
            "whole hour. An agent without this stack hallucinates, because it has no world. An "
            "agent with it has a governable world model. [pause] We will build these layers one at "
            "a time, always on the same six-source project. Part one: meaning."},
    ]},

    # ========================================================= CH02 — ONTOLOGY
    {"id": "kg-ch02-ontology", "title": "Ontology", "segments": [
        {"id": "divider", "variant": "kg_divider", "props": {"n": 1, "title": "Ontology", "sub": "the layer of meaning — a shared grammar machines can agree on", "color": ONT, "layer": 0}, "narration":
            "Part one. Ontology — the layer of meaning. [pause] Before you can connect anything, "
            "everyone and everything has to agree on what the words mean."},

        {"id": "vs", "variant": "kg_compare", "props": {"kicker": "WHAT AN ONTOLOGY ACTUALLY IS", "title": "Not a schema. Not a taxonomy. A model of meaning.", "color": ONT,
            "left": {"head": "Schema / taxonomy", "sub": "structure only", "c": MUT, "rows": [
                "A database schema says how bytes are stored.",
                "A taxonomy is just a tree of categories.",
                "Neither one tells a machine what a thing MEANS.",
                "Change the storage, and the meaning is lost."]},
            "right": {"head": "Ontology", "sub": "shared, explicit meaning", "c": ONT, "rows": [
                "Defines entities: Report, Query, Table, Service.",
                "Defines relationships: USES, READS, DEPLOYED_AS.",
                "Defines rules: every Report must use ≥1 Query.",
                "Independent of any one database or vendor."]},
            "foot": "The ontology is the contract every source, every query, and every agent shares."}, "narration":
            "First, let's kill a common confusion. An ontology is not a database schema, and it is "
            "not a taxonomy. [pause] A schema describes how bytes are laid out on disk. A taxonomy "
            "is a tidy tree of categories. Useful — but neither one tells a machine what a thing "
            "actually means. [pause] An ontology does. It names the entities in your world — "
            "Report, Query, Table, Service. [pause] It names the relationships between them — a "
            "report USES a query, a query READS a table, a service is DEPLOYED_AS a pod. [pause] "
            "And it names the rules — for example, every report must use at least one query. "
            "[pause] Crucially, it is independent of any single database or vendor. It is the "
            "shared contract. [pause] So when the wiki says ‘orders table’ and the SQL database "
            "says ‘ORDERS’, the ontology is what lets us know those are the same idea. That shared "
            "vocabulary is the foundation the entire stack is built on."},

        {"id": "triple", "variant": "kg_triple", "props": {"kicker": "THE ATOM OF MEANING", "title": "Everything reduces to a triple: subject → predicate → object",
            "subj": "Report", "pred": "USES", "obj": "Query",
            "examples": ["Query READS Table", "Service DEPLOYED_AS Pod", "Wiki DOCUMENTS Service", "Pod EMITS LogEvent"],
            "foot": "Millions of triples, sharing one vocabulary, become a graph of meaning."}, "narration":
            "Here is the beautiful part: no matter how complex your world is, it is built from one "
            "tiny atom. [pause] The triple. Subject, predicate, object. [pause] Report — uses — "
            "query. That is a complete, machine-readable fact. [pause] And you just keep adding "
            "them. Query reads table. Service is deployed as a pod. The wiki documents a service. "
            "A pod emits a log event. [pause] Each triple is trivial on its own. But because they "
            "all draw from the same shared vocabulary, they snap together. [pause] String a "
            "million of them together and you no longer have facts — you have a fabric. A graph of "
            "meaning where you can start at any node and walk to any related fact. [pause] This "
            "triple is the format behind the web standard called RDF, which we'll meet in a "
            "moment. But the idea is older and simpler than any technology: write meaning down as "
            "relationships, not as isolated values."},

        {"id": "reuse", "variant": "kg_cards", "props": {"kicker": "DON'T START FROM A BLANK PAGE", "title": "Most of your ontology has already been written", "color": ONT,
            "cards": [
                {"head": "Upper ontologies", "emoji": "🌐", "body": "Generic building blocks for things, people, documents — schema.org, Gist, Dublin Core.", "tag": "generic"},
                {"head": "Domain ontologies", "emoji": "🏦", "body": "Whole worlds, pre-built: FIBO for finance, SNOMED for health, Microsoft's DTDL ontologies for buildings.", "tag": "domain"},
                {"head": "Import & extend", "emoji": "🧩", "body": "Pull in a standard vocabulary, then add only your project's specifics on top.", "tag": "reuse"}],
            "foot": "Reuse buys you interoperability for free — and saves months of arguing about words."}, "narration":
            "Before you model a single class, know this: you rarely start from a blank page. [pause] "
            "There are upper ontologies — generic building blocks for universal concepts like "
            "things, people, and documents. schema.org, Gist, and Dublin Core are common ones. "
            "[pause] And there are domain ontologies — entire worlds already modeled by experts. "
            "FIBO covers finance. SNOMED covers medicine. Microsoft ships DTDL ontologies for smart "
            "buildings and energy. [pause] The smart move is to import a standard vocabulary and "
            "then extend it with only what's unique to your project. [pause] For our example, most "
            "of the software concepts — services, deployments, incidents — map to existing DevOps "
            "and observability vocabularies. You'd add just your report-and-pipeline specifics. "
            "[pause] Reuse isn't laziness. It buys you interoperability for free, and saves months "
            "of a committee arguing about what a word means."},

        {"id": "code", "variant": "kg_code", "props": {"kicker": "OWL SAYS WHAT IS · SHACL SAYS WHAT MUST BE", "title": "Meaning you can reason on, and rules you can enforce", "color": ONT, "lang": "turtle",
            "lines": [
                ":Report  a owl:Class .",
                ":Query   a owl:Class .",
                ":uses    a owl:ObjectProperty ;",
                "         rdfs:domain :Report ;",
                "         rdfs:range  :Query .",
                "",
                "sh:ReportShape a sh:NodeShape ;",
                "  sh:targetClass :Report ;",
                "  sh:property [ sh:path :uses ;",
                "               sh:minCount 1 ] ."],
            "caption": "OWL declares the concepts · SHACL validates every instance against the rules",
            "foot": "Machine-checkable meaning: the ontology can catch a broken model before an agent ever sees it."}, "narration":
            "Now, how do we actually write an ontology down? [pause] Two W3C standards do most of "
            "the work, and they are complementary. [pause] The first is OWL — the Web Ontology "
            "Language. OWL declares your concepts. Here, Report is a class, Query is a class, and "
            "‘uses’ is a relationship whose subject is a Report and whose object is a Query. "
            "[pause] From declarations like these, a reasoner can actually infer new facts you "
            "never stated. [pause] The second standard is SHACL — the Shapes Constraint Language. "
            "Where OWL says what things are, SHACL says what must be true. [pause] This shape says: "
            "every Report must use at least one Query. [pause] Feed your data in, and SHACL flags "
            "any report that violates it. [pause] Hold onto that idea. That same SHACL rule will "
            "come back at the very end as the guardrail that keeps an AI agent honest. Meaning you "
            "can reason on, plus rules you can enforce — in plain, portable text."},

        {"id": "inference", "variant": "kg_pipeline", "props": {"kicker": "REASONING · FACTS YOU NEVER WROTE DOWN", "title": "OWL lets the machine derive new truths from stated ones", "color": ONT,
            "nodes": [
                {"emoji": "✍️", "label": "Stated", "sub": "Report uses Query", "c": ONT},
                {"emoji": "🦉", "label": "Reasoner", "sub": "applies OWL rules", "c": GRAPH},
                {"emoji": "💡", "label": "Inferred", "sub": "Report DEPENDS_ON Table", "c": KG},
                {"emoji": "🧹", "label": "Less to maintain", "sub": "derive, don't duplicate", "c": OK}],
            "foot": "Declare the rules once; the reasoner keeps the derived facts correct for free."}, "narration":
            "Here's a superpower that separates an ontology from a plain data model: inference. "
            "[pause] You state a few facts — a report uses a query, a query reads a table. [pause] "
            "Then you declare a rule once: depends-on is transitive, and it flows across uses and "
            "reads. [pause] Now an OWL reasoner can derive a fact nobody ever typed: this report "
            "depends on that table. [pause] Multiply that across thousands of nodes and the reasoner "
            "maintains a whole layer of derived truth for you — automatically, and always "
            "consistent. [pause] The practical payoff is huge. You don't hand-maintain the "
            "‘depends-on’ edges; you declare the rule and let the machine keep them correct as the "
            "graph changes. [pause] Stated facts plus rules become inferred facts. That's meaning "
            "you can compute on — not just store."},

        {"id": "standards", "variant": "kg_orbit", "props": {"kicker": "THE ONTOLOGY TOOLBOX", "title": "The standards and tools you'll actually reach for", "color": ONT, "hub": "Ontology\nstack",
            "items": [
                {"emoji": "🔗", "label": "RDF — triples, global IDs"},
                {"emoji": "🦉", "label": "OWL — classes + inference"},
                {"emoji": "⚖️", "label": "SHACL — validation"},
                {"emoji": "🏷️", "label": "SKOS — vocabularies"},
                {"emoji": "🛠️", "label": "Protégé — the editor"},
                {"emoji": "☁️", "label": "DTDL — Azure twins"},
                {"emoji": "🏛️", "label": "Palantir — enterprise"}],
            "foot": "Standards for portability; a good editor for the humans; a platform when you scale."}, "narration":
            "Let's ground this in real tools you can open today. [pause] RDF is the data model — "
            "the triple, with global identifiers so two teams can point at the exact same concept. "
            "[pause] OWL, as we saw, adds classes and inference. SHACL adds validation. [pause] "
            "SKOS is a lightweight way to manage controlled vocabularies and synonyms — handy when "
            "the business calls the same thing five different names. [pause] To edit all of this, "
            "the classic tool is Protégé — it's free, and it's what the medical and scientific "
            "world uses to build enormous ontologies. [pause] In the Microsoft world, there's "
            "DTDL — a JSON-based ontology language built specifically for digital twins, which "
            "we'll use in part three. [pause] And at the enterprise end, Palantir's Foundry treats "
            "the ontology as the product itself. [pause] You do not need all of these on day one. "
            "You need the idea — shared, explicit meaning — and one place to write it down."},

        {"id": "wild", "variant": "kg_cards", "props": {"kicker": "THIS ALREADY RUNS THE INTERNET", "title": "You use ontology-backed knowledge graphs every day", "color": ONT,
            "cards": [
                {"head": "Google", "emoji": "🔍", "body": "The Knowledge Graph behind every search panel — billions of entities and facts.", "tag": "search"},
                {"head": "Amazon · LinkedIn", "emoji": "🛒", "body": "Product graphs, and LinkedIn's ‘Economic Graph’ of people, jobs and skills.", "tag": "commerce"},
                {"head": "Health · Finance", "emoji": "🏥", "body": "SNOMED for medicine, FIBO for finance — safety-critical shared meaning.", "tag": "regulated"}],
            "foot": "Proven at planet scale. What's new is that a normal team can finally build one too."}, "narration":
            "If this still feels abstract, look around — you already use it every day. [pause] When "
            "Google shows a panel about a person or a place, that's the Google Knowledge Graph — "
            "billions of entities and facts, backed by an ontology. [pause] Amazon runs a product "
            "graph; LinkedIn famously built its ‘Economic Graph’ of people, jobs, and skills. "
            "[pause] In regulated worlds, medicine runs on SNOMED and finance on FIBO — shared "
            "ontologies where a wrong meaning is a safety or compliance failure. [pause] So this is "
            "not a research curiosity. It's the proven backbone of the biggest systems on the "
            "internet. [pause] The only thing that changed is that the tooling — LLM extraction, "
            "GraphRAG, open standards — finally lets a normal team build one for their own project. "
            "Which is exactly what we're doing."},

        {"id": "design", "variant": "kg_cards", "props": {"kicker": "HOW TO DESIGN ONE THAT SHIPS", "title": "The principles that keep an ontology from becoming a swamp", "color": ONT,
            "cards": [
                {"head": "Start from questions", "emoji": "❓", "body": "List the ‘competency questions’ it must answer — ‘which reports break if this table changes?’ — and model just enough to answer them.", "tag": "scope"},
                {"head": "Small, then grow", "emoji": "🌱", "body": "Twenty classes that earn their keep beat five hundred that never ship. Add classes when a real question needs them.", "tag": "iterate"},
                {"head": "Test-driven", "emoji": "✅", "body": "Encode the rules as SHACL shapes — your ontology gets a test suite, exactly like code.", "tag": "TDD"}],
            "foot": "An ontology is software. Scope it, iterate it, test it — don't try to model the universe."}, "narration":
            "So how do you design one that actually ships, instead of a five-hundred-class swamp "
            "nobody finishes? Three principles. [pause] First, start from questions. Before "
            "modeling anything, write down the competency questions the graph must answer — like, "
            "‘which reports break if this table changes?’ Then model just enough to answer them, and "
            "no more. [pause] Second, start small and grow. Twenty well-chosen classes beat five "
            "hundred speculative ones. Add a class the day a real question needs it. [pause] Third, "
            "make it test-driven. Encode your rules as SHACL shapes, and suddenly your ontology has "
            "a test suite — just like code. [pause] That reframe is the whole trick: an ontology is "
            "software. You scope it, you iterate it, you test it. You do not try to model the "
            "universe in one sitting. [pause] Now, the idea that makes all this matter for agents."},

        {"id": "decision", "variant": "kg_cards", "props": {"kicker": "WHY AGENTS NEED THIS · THE DECISION-CENTRIC ONTOLOGY", "title": "Palantir's insight: meaning isn't enough — model the action too", "color": ONT,
            "cards": [
                {"head": "Data", "emoji": "📦", "body": "The objects and links — your report, query, table, and how they relate.", "tag": "semantic"},
                {"head": "Logic", "emoji": "🧮", "body": "Derived facts and business rules computed over the objects.", "tag": "semantic"},
                {"head": "Action", "emoji": "⚡", "body": "The typed, allowed operations — ‘open a work item’, ‘page the owner’.", "tag": "kinetic"},
                {"head": "Security", "emoji": "🔒", "body": "Who — human or agent — may see and do what, enforced at the meaning layer.", "tag": "kinetic"}],
            "foot": "So: an ontology is the shared grammar — and it defines the safe verbs an agent is allowed to use."}, "narration":
            "One more idea before we move on, and it's the one that makes ontologies matter for AI. "
            "[pause] Palantir popularized a decision-centric view: a good ontology models four "
            "things, not one. [pause] Data — the objects and their links. [pause] Logic — the "
            "rules and derived facts computed over them. [pause] Those two are the semantic side: "
            "what is true. [pause] But then two more. Action — the typed operations that are "
            "actually allowed, like ‘open a work item’ or ‘page the on-call owner’. [pause] And "
            "security — who, human or agent, may see and do what. [pause] These are the kinetic "
            "side: what can be done. [pause] This is the key that unlocks agents. The ontology "
            "doesn't just tell an agent what exists — it hands it a menu of safe verbs. [pause] So, "
            "to recap part one: an ontology is the shared grammar of your world, and, done right, "
            "it also defines the governed actions an agent may take. Now let's fill that grammar "
            "with real data."},
    ]},

    # ========================================================= CH03 — KNOWLEDGE GRAPH
    {"id": "kg-ch03-knowledge-graph", "title": "The Knowledge Graph", "segments": [
        {"id": "divider", "variant": "kg_divider", "props": {"n": 2, "title": "Knowledge Graph", "sub": "the layer of memory — the ontology, filled with your real world", "color": KG, "layer": 1}, "narration":
            "Part two. The knowledge graph — the layer of memory. [pause] An ontology is an empty "
            "template. Pour your actual data into it, and it comes alive."},

        {"id": "instantiate", "variant": "kg_pipeline", "props": {"kicker": "FROM TEMPLATE TO INSTANCES", "title": "Classes become nodes; rules become edges", "color": KG,
            "nodes": [
                {"emoji": "🦉", "label": "Ontology", "sub": "classes + rules", "c": ONT},
                {"emoji": "📥", "label": "Your data", "sub": "6 sources", "c": GRAPH},
                {"emoji": "🔵", "label": "Instances", "sub": "actual nodes", "c": KG},
                {"emoji": "🕸️", "label": "Graph", "sub": "nodes + edges", "c": KG}],
            "foot": "The class :Report becomes the node ‘Regional Sales’; the rule :uses becomes a real edge."}, "narration":
            "The move here is simple but profound. [pause] Your ontology has a class called Report. "
            "Your real world has a specific report named Regional Sales. [pause] So Regional Sales "
            "becomes a node — an instance of the Report class. [pause] The ontology said a report "
            "uses a query; in your data, Regional Sales uses the query Q sales by region — so that "
            "becomes a real edge between two real nodes. [pause] Do that for every object across "
            "all six sources, and the empty template becomes a populated graph. Thousands of "
            "concrete nodes, connected by concrete edges, every one of them conforming to the "
            "shared meaning. [pause] That populated graph is your knowledge graph. It is the "
            "system's long-term memory — and unlike a pile of tables, you can traverse it. [pause] "
            "The obvious next question: which technology do you actually store it in?"},

        {"id": "modeling", "variant": "kg_cards", "props": {"kicker": "MODELING PRINCIPLES", "title": "Three rules that keep a graph clean instead of a hairball", "color": KG,
            "cards": [
                {"head": "Relationships are first-class", "emoji": "➡️", "body": "If you'll ever ask about a connection, make it a real edge — not a foreign key hidden inside a row.", "tag": "edges"},
                {"head": "Node vs. property", "emoji": "⚖️", "body": "Something you query or connect to becomes a node. A plain attribute stays a property on one.", "tag": "granularity"},
                {"head": "Beware super-nodes", "emoji": "🕸️", "body": "A single node with a million edges wrecks performance — model around the hotspots deliberately.", "tag": "scale"}],
            "foot": "Good graph modeling is mostly deciding what deserves to be an edge, and what doesn't."}, "narration":
            "Before we store anything, a word on modeling — because a sloppy graph becomes a "
            "hairball fast. Three rules. [pause] One: relationships are first-class citizens. If "
            "you will ever ask a question about a connection, make it a real edge — not a foreign "
            "key buried inside a row where no traversal can find it. [pause] Two: know when "
            "something is a node versus a property. If you query it or connect to it, it's a node. "
            "If it's just a plain attribute — a color, a timestamp — it's a property on a node. "
            "[pause] Three: watch out for super-nodes. A single node with a million edges — say, a "
            "‘user’ node everything links to — becomes a performance sinkhole. Model around those "
            "hotspots on purpose. [pause] Most of graph modeling is just this: deciding, "
            "deliberately, what earns the right to be an edge. Get that right and everything above "
            "stays fast. Now, where do we actually put it?"},

        {"id": "pgvsrdf", "variant": "kg_compare", "props": {"kicker": "THE TWO FAMILIES", "title": "Property graph vs RDF triplestore — pick by the job", "color": KG,
            "left": {"head": "Property graph", "sub": "Neo4j · Cypher · GQL", "c": KG, "rows": [
                "Nodes & edges carry properties directly.",
                "Fast to model, great developer velocity.",
                "Cypher / the new ISO GQL for queries.",
                "Best for operational apps and analytics."]},
            "right": {"head": "RDF triplestore", "sub": "SPARQL · OWL · SHACL", "c": ONT, "rows": [
                "Pure triples with global, shareable IDs.",
                "Formal semantics, inference, W3C standards.",
                "SPARQL queries; portable across vendors.",
                "Best for interop, governance, shared meaning."]},
            "foot": "Many teams do both: RDF for the meaning contract, a property graph for speed. Bridges exist."}, "narration":
            "There are two big families, and the internet loves to argue about them. Let's make it "
            "practical. [pause] On the left, the property graph — think Neo4j. Nodes and edges "
            "carry properties directly, it's fast to model, and developers love it. You query it "
            "with Cypher, or with the new ISO standard called GQL. [pause] It shines for "
            "operational apps and analytics — exactly the report-and-pipeline world of our "
            "example. [pause] On the right, the RDF triplestore. Everything is pure triples with "
            "global identifiers, backed by formal W3C standards, inference, and SHACL validation. "
            "You query it with SPARQL. [pause] It shines when meaning must be shared across teams "
            "and vendors, and when governance matters. [pause] So which do you pick? Honestly, "
            "mature teams often use both — RDF as the portable contract of meaning, a property "
            "graph for speed — and there are bridges, like R2RML, between them. [pause] For our "
            "project, we'll picture a property graph. Now, the hard part: filling it from six very "
            "different sources."},

        {"id": "joins", "variant": "kg_compare", "props": {"kicker": "WHY NOT JUST SQL?", "title": "Relationships are where relational databases hurt", "color": KG,
            "left": {"head": "SQL, many joins", "sub": "relational", "c": BAD, "rows": [
                "Every hop is another JOIN.",
                "A 6-hop question = a 6-table join.",
                "Queries get slow and unreadable fast.",
                "Rigid schema changes ripple everywhere."]},
            "right": {"head": "Graph traversal", "sub": "native", "c": KG, "rows": [
                "A hop is just following an edge.",
                "6 hops = a short, fast walk.",
                "The query reads like the question.",
                "New relationships just add edges."]},
            "foot": "Relational is great for rows. Graphs win the moment the question is about connections."}, "narration":
            "A fair pushback: we already have SQL — why a graph at all? [pause] Because of joins. In "
            "a relational database, every relationship you follow is another join. A question that "
            "hops from report, to query, to table, to schema change, to log is a five- or six-table "
            "join — slow to run, and painful to read. [pause] In a graph, a hop is just following "
            "an edge. That same six-hop question becomes a short, fast walk, and the query reads "
            "almost exactly like the question you asked. [pause] And when the world changes, you "
            "don't reshape a rigid schema — you just add an edge. [pause] Relational databases are "
            "still excellent for what they're for: rows and transactions. But the moment your "
            "question is fundamentally about connections, the graph wins. And our entire problem is "
            "about connections."},

        {"id": "ingest", "variant": "kg_ingest", "props": {"foot":
            "Each silo keeps its home; the graph just adds the connective tissue between them."}, "narration":
            "This is where knowledge graphs get real, so let's go source by source. [pause] The "
            "DevOps wiki is unstructured prose, so we run a large language model over it to extract "
            "entities and relationships — this is exactly what Microsoft's GraphRAG and Neo4j's "
            "LLM graph builder do. [pause] The DevOps repo is semi-structured, so we parse report "
            "definitions and SQL to link each report to the queries and tables it touches. [pause] "
            "Azure SQL is relational, so we map its tables into graph nodes — a standard called "
            "R2RML, or a virtual-graph engine like Ontop, does this. [pause] Cosmos DB holds "
            "documents, so each document becomes a node with its fields as properties. [pause] "
            "Blob storage contributes asset metadata — filenames, owners, which report embeds "
            "which image. [pause] And the AKS logs stream in as time-stamped log-event nodes. "
            "[pause] Every source flows through a builder that extracts, resolves, and loads. Six "
            "silos in; one connected graph out. Nothing is moved or deleted — we're adding the "
            "connective tissue that was always missing."},

        {"id": "merge", "variant": "kg_merge", "props": {"foot":
            "Match on keys and context, collapse the duplicates — meaning stays consistent everywhere."}, "narration":
            "But that raises an obvious danger. [pause] The wiki says ‘orders’. The SQL database "
            "says ‘ORDERS’, all caps. The repo calls it ‘OrderTbl’. [pause] To a naive importer, "
            "those are three different things — and your graph is instantly polluted with "
            "duplicates. [pause] The fix is a discipline called entity resolution: detecting that "
            "several records refer to the same real-world thing, and collapsing them into one "
            "canonical node. [pause] Watch — three names, three sources, converging into a single "
            "node: Table Orders. [pause] Every edge that pointed at any of the three now points at "
            "the one. [pause] This is not a nice-to-have. Microsoft measured that adding "
            "LLM-driven entity resolution to GraphRAG improved query accuracy by about thirty-four "
            "percent. [pause] Skip this step and your beautiful graph quietly lies to you. Get it "
            "right, and the same concept means the same thing no matter which silo it came from. "
            "That consistency is the entire value."},

        {"id": "provenance", "variant": "kg_cards", "props": {"kicker": "PROVENANCE & VERSIONING", "title": "Every fact should say where it came from — and when", "color": KG,
            "cards": [
                {"head": "Source on every fact", "emoji": "🏷️", "body": "Each node and edge records which of the six sources produced it, and when — so you can always trace a claim.", "tag": "lineage"},
                {"head": "Bitemporal history", "emoji": "🕰️", "body": "Keep what was true, and when you learned it. Now you can ask ‘what did the graph believe last Tuesday?’", "tag": "time-travel"},
                {"head": "Confidence scores", "emoji": "📊", "body": "LLM-extracted edges carry a confidence; the shaky ones get flagged for human review, not trusted blindly.", "tag": "trust"}],
            "foot": "A graph you can't audit is a rumor mill. Provenance is what makes it evidence."}, "narration":
            "One discipline separates a toy graph from one you'd bet a decision on: provenance. "
            "[pause] Every node and every edge should record where it came from — which of the six "
            "sources produced it — and when. So when an agent later claims ‘this report depends on "
            "that table’, you can trace exactly why it believes that. [pause] Go a step further and "
            "make it bitemporal: store not just what is true, but when you learned it. Now you can "
            "run time-travel queries — what did the graph believe last Tuesday, before the "
            "migration? [pause] And because a lot of edges are extracted by a language model, "
            "attach a confidence score. The shaky ones get flagged for a human, not trusted "
            "blindly. [pause] Here's the mindset: a graph you can't audit is just a rumor mill. "
            "Provenance is what turns it into evidence — which is exactly what you need before an "
            "agent acts on it. Now, the query that pays it all off."},

        {"id": "cypher", "variant": "kg_code", "props": {"kicker": "ONE QUERY, MANY HOPS", "title": "Ask a question that no single table could answer", "color": KG, "lang": "cypher",
            "lines": [
                "MATCH (r:Report {name:'Report X'})",
                "      -[:USES]->(q:Query)",
                "      -[:READS]->(t:Table)",
                "      <-[:CHANGED_BY]-(c:SchemaChange)",
                "WHERE c.at > datetime() - duration('P1D')",
                "RETURN r.name, t.name, c.migration"],
            "result": ["Report X", "→ Orders", "← migration #482", "3 hops · 4 ms"],
            "caption": "one traversal spans a report, its table, and yesterday's schema change",
            "foot": "This is a graph's superpower: multi-hop questions become a single, fast walk."}, "narration":
            "Now the payoff of having a graph instead of six tables. [pause] Remember our original "
            "question — report X is wrong, why? [pause] In a graph, that's a single query. Start "
            "at Report X, hop along the ‘uses’ edge to its query, hop again along ‘reads’ to the "
            "table, then jump to any schema change on that table in the last day. [pause] This is "
            "written in Cypher, but read it as English: follow the trail from the report to the "
            "thing that changed underneath it. [pause] Three hops. A few milliseconds. And it "
            "returns the answer directly: Report X reads the Orders table, which was changed by "
            "migration four eighty-two, yesterday. [pause] No single database could answer that, "
            "because the answer lived in the connections between them. [pause] Multi-hop questions "
            "— which are most of the interesting ones — become a single, fast walk. Which is "
            "exactly why AI systems started reaching for graphs."},

        {"id": "catalog", "variant": "kg_cards", "props": {"kicker": "YOU MAY ALREADY HAVE HALF OF ONE", "title": "A data catalog is a knowledge graph in disguise", "color": KG,
            "cards": [
                {"head": "Assets as nodes", "emoji": "🗃️", "body": "Tables, columns, dashboards, jobs — the things a catalog already tracks — are graph nodes.", "tag": "nodes"},
                {"head": "Lineage as edges", "emoji": "🧬", "body": "‘This report reads that table’ is exactly the edge a lineage tool already draws.", "tag": "edges"},
                {"head": "Go further", "emoji": "🚀", "body": "Add services, incidents, owners and docs, and the catalog becomes the living map.", "tag": "extend"}],
            "foot": "DataHub, OpenMetadata and Atlan are graphs under the hood — a real running start."}, "narration":
            "Here's some good news: you may already be halfway there. [pause] A modern data catalog "
            "is a knowledge graph wearing a different name. [pause] The assets it tracks — tables, "
            "columns, dashboards, jobs — are nodes. The lineage it draws — this report reads that "
            "table — are edges. [pause] Tools like DataHub, OpenMetadata, and Atlan are literally "
            "graphs under the hood. [pause] So if you run one, you already have the skeleton of "
            "your project's knowledge graph. The work is extending it beyond data assets — adding "
            "the services, the incidents, the owners, and the design docs from your wiki. [pause] "
            "That's the leap from a passive catalog to the living map we've been building: not just "
            "what data exists, but how the whole system fits together. Don't start from zero if you "
            "don't have to."},

        {"id": "hybrid", "variant": "kg_compare", "props": {"kicker": "VECTORS AND GRAPHS — NOT EITHER/OR", "title": "The best retrieval uses both meaning and structure", "color": KG,
            "left": {"head": "Vector search", "sub": "meaning", "c": AGENT, "rows": [
                "Finds text that sounds similar.",
                "Fuzzy, tolerant of wording.",
                "Great for ‘find me something about X’.",
                "But blind to explicit structure."]},
            "right": {"head": "Graph traversal", "sub": "structure", "c": KG, "rows": [
                "Follows exact, named relationships.",
                "Multi-hop and fully explainable.",
                "Great for ‘how is X connected to Y’.",
                "But blind to fuzzy meaning."]},
            "foot": "Store embeddings ON the graph nodes: retrieve by meaning, then expand along the edges."}, "narration":
            "Quick myth-buster, because people treat this as a religious war: vectors versus graphs. "
            "[pause] It's not either-or. They're good at opposite things. [pause] Vector search "
            "finds text that sounds similar to your question. It's fuzzy and forgiving — perfect "
            "for ‘find me something about regional sales’. But it's blind to structure; it has no "
            "idea what connects to what. [pause] Graph traversal follows exact, named "
            "relationships, multi-hop, and every answer comes with an explainable path. But it's "
            "blind to fuzzy meaning — it won't match ‘revenue’ to ‘sales’ unless you told it to. "
            "[pause] The winning move is to use both. Store the embedding right on the graph node. "
            "Then retrieve by meaning to find the entry points, and expand along the edges to get "
            "the structure. [pause] That hybrid — semantic entry, structural expansion — is how the "
            "best GraphRAG systems actually work. Speaking of which, here's the number."},

        {"id": "scale", "variant": "kg_cards", "props": {"kicker": "WHEN IT GROWS — AND WHEN IT'S OVERKILL", "title": "Making graphs fast, fresh, and used only where they earn it", "color": KG,
            "cards": [
                {"head": "Index & partition", "emoji": "📈", "body": "Index the properties you look up by; partition huge graphs. Azure Cosmos DB even speaks the Gremlin graph API.", "tag": "performance"},
                {"head": "Build incrementally", "emoji": "♻️", "body": "Re-ingest only what changed — logs stream, wikis update nightly. Never rebuild the whole world.", "tag": "freshness"},
                {"head": "Know the limits", "emoji": "🚦", "body": "No multi-hop questions? A graph is overkill. Reach for it exactly where the connections carry the value.", "tag": "judgment"}],
            "foot": "A graph is a tool, not a religion. Use it where relationships are the point."}, "narration":
            "A note on scale, before the headline result — because ‘it worked on my laptop’ is not a "
            "strategy. [pause] Performance comes from the basics: index the properties you look up "
            "by, and partition a truly large graph across machines. And you may not need a new "
            "database at all — Azure Cosmos DB, already in our stack, speaks the Gremlin graph API "
            "directly. [pause] Freshness comes from incremental builds. Logs stream in continuously; "
            "the wiki re-syncs nightly. You re-ingest only what changed — you never rebuild the "
            "whole world. [pause] And the most important one: judgment. If a part of your system "
            "never gets multi-hop questions, a graph there is overkill. [pause] A graph is a tool, "
            "not a religion. Reach for it exactly where relationships are the point — and skip it "
            "where they aren't. Now, the result that made everyone pay attention."},

        {"id": "graphrag", "variant": "kg_chart", "props": {"kicker": "GRAPHRAG vs PLAIN VECTOR SEARCH", "title": "Why grounding an LLM on a graph beats grounding it on text chunks", "color": KG,
            "bars": [{"label": "Vector RAG", "v": 32, "c": BAD}, {"label": "GraphRAG (multi-hop)", "v": 86, "c": KG}],
            "note": "Microsoft Research — accuracy on multi-hop enterprise questions",
            "foot": "Structured retrieval finds the PATH, not just similar-sounding paragraphs."}, "narration":
            "Here's the number that put knowledge graphs back on every AI roadmap. [pause] The "
            "popular way to give a language model context is vector search — chop your documents "
            "into chunks, and retrieve the ones that sound similar to the question. [pause] It's "
            "great for ‘find me a paragraph about X’. It's terrible at ‘what connects X to Y "
            "across three systems’, because nothing in the text says so out loud. [pause] "
            "Microsoft Research pitted graph-based retrieval — GraphRAG — against plain vector "
            "search on multi-hop enterprise questions. [pause] Vector search scored about "
            "thirty-two percent. [pause] GraphRAG, which retrieves along the actual relationships, "
            "scored about eighty-six percent. [pause] Same model, same data — the difference was "
            "structure. [pause] The graph doesn't just find similar-sounding text; it finds the "
            "path. [pause] So, to recap part two: a knowledge graph is your ontology filled with "
            "resolved, real instances — and it turns the hardest questions into a single walk. "
            "Next, we make that graph breathe."},
    ]},

    # ========================================================= CH04 — DIGITAL TWIN
    {"id": "kg-ch04-digital-twin", "title": "The Digital Twin", "segments": [
        {"id": "divider", "variant": "kg_divider", "props": {"n": 3, "title": "Digital Twin", "sub": "the layer of live senses — the graph, synchronized with reality", "color": TWIN, "layer": 2}, "narration":
            "Part three. The digital twin — the layer of live senses. [pause] A knowledge graph "
            "tells you how the world is wired. A twin tells you how it's doing, right now."},

        {"id": "whatis", "variant": "kg_cards", "props": {"kicker": "WHAT MAKES A GRAPH A TWIN", "title": "Three ingredients turn a static map into a living one", "color": TWIN,
            "cards": [
                {"head": "Structure", "emoji": "🕸️", "body": "The knowledge graph — every entity and relationship in your system.", "tag": "the map"},
                {"head": "Live state", "emoji": "📡", "body": "Telemetry streams — logs, metrics, DB state — updating node properties continuously.", "tag": "the senses"},
                {"head": "Simulation", "emoji": "🔮", "body": "Run what-if changes over the graph before you touch production.", "tag": "the crystal ball"}],
            "foot": "Twin = knowledge graph + live telemetry + the ability to simulate. Not a 3D render — a live model."}, "narration":
            "Let's define the term precisely, because it's badly overused. [pause] A digital twin "
            "is not a fancy 3D render. It is three things layered together. [pause] First, "
            "structure — and we already built that: the knowledge graph of every entity and "
            "relationship. [pause] Second, live state. Telemetry streams — your logs, your "
            "metrics, your database state — flow in and continuously update the properties on those "
            "nodes. Is this pod healthy? Is this report stale? The twin knows, second by second. "
            "[pause] Third, simulation. Because the model mirrors reality, you can run a change "
            "against the model first, and watch what happens — before you touch production. "
            "[pause] So the equation is: twin equals knowledge graph, plus live telemetry, plus the "
            "ability to simulate. [pause] Structure, senses, and a crystal ball. For our project, "
            "that means the graph you already have — but now it's plugged into the running system."},

        {"id": "telemetry", "variant": "kg_telemetry", "props": {"foot":
            "A model that mirrors reality now — not a diagram someone drew last quarter."}, "narration":
            "Here's the twin actually breathing. [pause] Each node is a piece of the running "
            "system — the API gateway, the orders service, the SQL pool, Cosmos, and a specific "
            "AKS pod. [pause] The AKS logs and health probes stream in, and the node colors change "
            "with them in real time: green for healthy, amber for degraded, red for failing. "
            "[pause] Notice this is the same graph from part two — but where that one was a static "
            "map, this one is a live dashboard with meaning baked in. [pause] When that pod turns "
            "red, you don't just see an alert. You see exactly which services depend on it, which "
            "queries run through it, and which reports will go wrong because of it — because those "
            "relationships are right there in the graph. [pause] This is the difference between an "
            "architecture diagram someone drew last quarter, and a model that reflects the system "
            "as it actually is this second. [pause] And once your model is live and accurate, you "
            "can start asking it to think ahead."},

        {"id": "syncarch", "variant": "kg_pipeline", "props": {"kicker": "HOW THE SYNC ACTUALLY WORKS", "title": "Change events flow in and update the graph in seconds", "color": TWIN,
            "nodes": [
                {"emoji": "📡", "label": "Source events", "sub": "logs · metrics · CDC", "c": TWIN},
                {"emoji": "🚌", "label": "Event bus", "sub": "Event Hubs / feed", "c": GRAPH},
                {"emoji": "🔁", "label": "Update rules", "sub": "event → node state", "c": ONT},
                {"emoji": "🕸️", "label": "Live twin", "sub": "always current", "c": KG}],
            "foot": "Change-data-capture on the DBs plus a log stream keep the model within seconds of reality."}, "narration":
            "So how does the graph actually stay in sync — is a human refreshing it? No. It's "
            "event-driven, and the pattern is worth knowing. [pause] Your sources emit change "
            "events: logs and health probes from AKS, metrics, and change-data-capture from Azure "
            "SQL and Cosmos when a row moves. [pause] Those events flow onto an event bus — in "
            "Azure, that's Event Hubs or a change feed. [pause] A set of update rules maps each "
            "event to a change in the graph: this pod's event flips that node's health; this row "
            "change updates that table's row count. [pause] And the twin stays current, "
            "continuously, with no nightly batch and no human in the loop. [pause] This is the "
            "architecture behind Azure Digital Twins, and it's why the model can be trusted to "
            "reflect the system within seconds — not last quarter. A live model needs a live feed. "
            "Now, how far up the ladder can a twin go?"},

        {"id": "maturity", "variant": "kg_tower", "props": {"kicker": "THE MATURITY LADDER", "title": "Twins climb from ‘what is’ to ‘act on its own’", "color": TWIN,
            "levels": [
                {"label": "Descriptive", "sub": "mirrors the current state"},
                {"label": "Informational", "sub": "adds history and context"},
                {"label": "Predictive", "sub": "forecasts what happens next"},
                {"label": "Prescriptive", "sub": "recommends the best fix"},
                {"label": "Autonomous", "sub": "acts within guardrails"}],
            "foot": "Most teams live on rungs one and two. The top rung is where agents plug in."}, "narration":
            "Digital twins aren't all-or-nothing. They climb a ladder of maturity, and it's worth "
            "knowing where you stand. [pause] Rung one, descriptive: the twin simply mirrors the "
            "current state. [pause] Rung two, informational: it adds history and context, so you "
            "can ask what changed and when. [pause] Rung three, predictive: it forecasts what "
            "happens next — this table's growth will breach the quota in a week. [pause] Rung four, "
            "prescriptive: it doesn't just predict, it recommends the best fix. [pause] And rung "
            "five, autonomous: within strict guardrails, it acts on its own. [pause] Be honest — "
            "most teams today live on rungs one and two, and that's already hugely valuable. "
            "[pause] But notice where this ladder is heading. The top rung, autonomous action, is "
            "exactly where the agents from part five plug in. The twin gives them a live world; "
            "they provide the action. [pause] First, though, the standards that make twins real."},

        {"id": "whouses", "variant": "kg_cards", "props": {"kicker": "NOT JUST FACTORIES ANYMORE", "title": "Who runs digital twins today", "color": TWIN,
            "cards": [
                {"head": "Industry & energy", "emoji": "🏭", "body": "Factories, jet engines, and power grids — the original, hard-ROI twins.", "tag": "classic"},
                {"head": "Cities & buildings", "emoji": "🏙️", "body": "Traffic, utilities, and whole ‘digital city’ models used for planning.", "tag": "urban"},
                {"head": "Software & data", "emoji": "💻", "body": "The newest frontier: a live twin of your systems, pipelines, and services — ours.", "tag": "you"}],
            "foot": "Any complex system you can model as a graph, you can twin — including your software."}, "narration":
            "Digital twins started in heavy industry, but they've spread far beyond it — and that "
            "tells you how mature the idea is. [pause] The classics are industrial: factories, jet "
            "engines, power grids, where a twin saves millions in downtime. [pause] Then came "
            "cities and buildings — traffic systems, utilities, entire digital-city models used for "
            "planning before a shovel hits the ground. [pause] And the newest frontier is the one "
            "we care about: software and data systems. A live twin of your own services, pipelines, "
            "and databases. [pause] The reason it generalizes so well is simple. Any complex system "
            "you can model as a graph, you can turn into a twin by feeding it live data. [pause] "
            "Your software estate is exactly such a system — which is why this technique has finally "
            "arrived for engineering teams like yours."},

        {"id": "platforms", "variant": "kg_cards", "props": {"kicker": "THE PLATFORMS YOU'LL EVALUATE", "title": "Real digital-twin tech, from IT systems to physical factories", "color": TWIN,
            "cards": [
                {"head": "Azure Digital Twins", "emoji": "☁️", "body": "Model in DTDL (JSON-LD), build a live graph in the cloud. Natural fit for our Azure stack.", "tag": "DTDL"},
                {"head": "Eclipse Ditto", "emoji": "🔌", "body": "Open-source twins for fleets of IoT devices, with clean JSON APIs.", "tag": "IoT"},
                {"head": "Asset Admin Shell", "emoji": "🏭", "body": "The Industry-4.0 & ISO 23247 standard for twins of machines and plants.", "tag": "ISO 23247"},
                {"head": "NVIDIA Omniverse", "emoji": "🌌", "body": "OpenUSD-based twins for physical AI — factories, robots, ‘the $50T opportunity’.", "tag": "OpenUSD"}],
            "foot": "Our project maps cleanly onto Azure Digital Twins + DTDL — same ontology idea, twin-flavored."}, "narration":
            "This is a real, funded field, so here are the platforms you'd actually evaluate. "
            "[pause] For an IT system like ours, Azure Digital Twins is the natural fit. You model "
            "your world in DTDL — that JSON-based ontology language we mentioned — and it builds a "
            "live graph in the cloud. [pause] For fleets of physical devices, Eclipse Ditto is a "
            "clean open-source option with simple JSON APIs. [pause] For factories and machines, "
            "the Asset Administration Shell, backed by ISO twenty-three thousand two forty-seven, "
            "is the Industry 4.0 standard. [pause] And at the frontier, NVIDIA's Omniverse builds "
            "twins of the physical world in OpenUSD — the backbone of what Jensen Huang calls the "
            "fifty-trillion-dollar physical AI opportunity. [pause] Notice the through-line: every "
            "one of these starts with an ontology and a graph. The twin is that same idea, plus a "
            "live feed. [pause] And here's the capability that makes twins genuinely magical: "
            "simulation."},

        {"id": "pipelinetwin", "variant": "kg_cards", "props": {"kicker": "THE TWIN YOU'LL BUILD FIRST", "title": "A twin of your data pipeline = live data observability", "color": TWIN,
            "cards": [
                {"head": "Freshness", "emoji": "⏱️", "body": "Every table node carries ‘last updated’. A stale report becomes visible before any human notices it's wrong.", "tag": "SLA"},
                {"head": "Lineage", "emoji": "🧬", "body": "source → table → query → report is already in the graph. That IS column-level data lineage, for free.", "tag": "lineage"},
                {"head": "Data contracts", "emoji": "📜", "body": "SHACL on the twin enforces the schema a downstream report was promised — a broken contract fails loudly.", "tag": "contracts"}],
            "foot": "For a reporting platform like ours, the twin doubles as a live data-quality cockpit."}, "narration":
            "Here's the twin most teams should build first — because it pays for itself immediately. "
            "[pause] A twin of your data pipeline is, in effect, data observability. [pause] Give "
            "every table node a ‘last updated’ timestamp, and a stale report becomes visible the "
            "moment it goes stale — before a stakeholder notices the numbers are wrong. [pause] "
            "Your lineage comes for free: source, to table, to query, to report is already encoded "
            "as edges. That is column-level data lineage, the thing whole products are sold for. "
            "[pause] And you can enforce data contracts — SHACL rules on the twin that guarantee a "
            "downstream report gets the schema it was promised. Break the contract, and the build "
            "fails loudly. [pause] For a reporting platform like our example, this one twin doubles "
            "as a live data-quality cockpit. It's the fastest ROI in the whole stack. [pause] And "
            "the ambition doesn't stop at pipelines."},

        {"id": "roi", "variant": "kg_cards", "props": {"kicker": "WHAT THE TWIN IS WORTH", "title": "Four payoffs that justify the build", "color": TWIN,
            "cards": [
                {"head": "Faster incidents", "emoji": "⚡", "body": "Root cause in minutes, not hours — the RCA agent we build in part five.", "tag": "MTTR"},
                {"head": "Safer changes", "emoji": "🛡️", "body": "Simulate blast radius before shipping — no more 2 a.m. surprises.", "tag": "risk"},
                {"head": "Instant onboarding", "emoji": "🧭", "body": "New engineers ask the graph how the system fits together — and get a real answer.", "tag": "ramp"},
                {"head": "Trustworthy AI", "emoji": "🤖", "body": "A grounded world model is what lets an agent act without hallucinating.", "tag": "agents"}],
            "foot": "Every payoff here is something a stakeholder can feel — that's how the project gets funded."}, "narration":
            "Let's be blunt about why anyone would fund this, because ‘it's elegant’ won't get you "
            "budget. Four payoffs. [pause] Faster incidents: root cause in minutes instead of hours "
            "— that's the agent we build in part five, and it's a number your on-call team feels "
            "immediately. [pause] Safer changes: simulate the blast radius before you ship, so "
            "there are no two-a-m surprises. [pause] Instant onboarding: a new engineer asks the "
            "graph how the system fits together and gets a real, current answer, instead of hunting "
            "down the one person who knows. [pause] And trustworthy AI: a grounded world model is "
            "the thing that lets an agent act without making things up. [pause] Notice that every "
            "one of these is something a stakeholder can feel. That's how a project like this "
            "actually gets funded — not on elegance, on outcomes."},

        {"id": "opstwin", "variant": "kg_cards", "props": {"kicker": "THE ENDGAME · OPERATIONAL DIGITAL TWIN", "title": "Palantir's leap: a live twin of the whole organization", "color": TWIN,
            "cards": [
                {"head": "Beyond IT", "emoji": "🏢", "body": "Not just servers and tables — orders, shipments, customers and decisions become live objects too.", "tag": "the org"},
                {"head": "Semantic + kinetic", "emoji": "⚙️", "body": "Things you can see, plus the actions you can take, unified in one governed model.", "tag": "act"},
                {"head": "Humans + agents share it", "emoji": "🤝", "body": "The same operational twin is the workspace for people and AI alike — one source of truth.", "tag": "shared"}],
            "foot": "The horizon: your business itself, as a living, queryable, actionable model."}, "narration":
            "The biggest version of this idea is what Palantir calls an operational digital twin — "
            "a live model not of a server, but of an entire organization. [pause] It goes beyond "
            "IT. Orders, shipments, customers, financial transactions, even decisions — all become "
            "live objects in the graph. [pause] And it's both semantic and kinetic, in the "
            "language from part one: the things you can see, plus the actions you can take, unified "
            "in one governed model. [pause] Crucially, the same twin is the shared workspace for "
            "humans and agents. A dispatcher and an AI look at the exact same objects and take the "
            "exact same governed actions. [pause] That's the horizon this whole stack is climbing "
            "toward: your business itself, as a living, queryable, actionable model. [pause] For "
            "now, back to our project — and the single most valuable thing a twin lets you do."},

        {"id": "cascade", "variant": "kg_cascade", "props": {"foot":
            "Simulate the blast radius on the twin, instead of discovering it in production at 2 a.m."}, "narration":
            "Let me show you the moment a twin earns its budget. [pause] An engineer proposes "
            "dropping a column — orders dot region — to clean up the schema. Reasonable. [pause] "
            "But instead of merging and praying, we run it against the twin first. [pause] The "
            "model knows the graph, so it propagates the change downstream. The column feeds the "
            "Orders table. The table feeds two queries. Those queries feed three reports. [pause] "
            "Watch the impact spread through the graph like a shockwave: column, table, queries, "
            "reports — and three dashboards light up red. [pause] They will break the moment you "
            "ship. [pause] You learned that in seconds, from a model, instead of at two in the "
            "morning from an angry stakeholder. [pause] That is prescriptive, predictive power — "
            "and it's only possible because the relationships are explicit in the graph. [pause] "
            "So, to recap part three: a digital twin is your knowledge graph plus a live feed plus "
            "simulation — a model of your system you can actually trust to be current. Now, how do "
            "we build and run all this at scale?"},
    ]},

    # ========================================================= CH05 — GRAPH ENGINEERING
    {"id": "kg-ch05-graph-engineering", "title": "Graph Engineering", "segments": [
        {"id": "divider", "variant": "kg_divider", "props": {"n": 4, "title": "Graph Engineering", "sub": "the substrate — the craft of building and running graphs at scale", "color": ENG, "layer": 3}, "narration":
            "Part four. Graph engineering — the substrate. [pause] Everything so far assumed the "
            "graph exists, stays correct, and performs. That doesn't happen by accident. It's a "
            "discipline."},

        {"id": "disciplines", "variant": "kg_orbit", "props": {"kicker": "THE CRAFT", "title": "What a graph engineer actually owns", "color": ENG, "hub": "Graph\nEngineering",
            "items": [
                {"emoji": "📐", "label": "Ontology & schema design"},
                {"emoji": "🏗️", "label": "Construction pipelines"},
                {"emoji": "🔗", "label": "Entity resolution"},
                {"emoji": "⚖️", "label": "Validation (SHACL)"},
                {"emoji": "🗂️", "label": "Versioning & governance"},
                {"emoji": "🧠", "label": "Graph ML / GNNs"}],
            "foot": "It's data engineering — but the product is meaning, and meaning has to stay true."}, "narration":
            "So what does a graph engineer actually do all day? Six things, and you've met most of "
            "them already. [pause] They design the ontology and schema — the shared meaning. "
            "[pause] They build the construction pipelines that pull from every source, like our "
            "six connectors. [pause] They own entity resolution, keeping duplicates out. [pause] "
            "They wire in validation with SHACL, so bad data can't silently enter. [pause] They "
            "handle versioning and governance — because meaning changes over time, and you need to "
            "know what the graph believed last Tuesday. [pause] And they apply graph machine "
            "learning, which we'll get to in a minute. [pause] Here's the mindset shift: this is "
            "data engineering, but the product isn't a table or a dashboard — it's meaning. And "
            "meaning has to stay true, continuously, or everything above it rots. [pause] Two of "
            "these deserve a closer look. Let's start with how you actually query at scale."},

        {"id": "construction", "variant": "kg_pipeline", "props": {"kicker": "THE CONSTRUCTION PIPELINE", "title": "Building the graph is an ETL job whose output is meaning", "color": ENG,
            "nodes": [
                {"emoji": "📥", "label": "Extract", "sub": "connector / source", "c": GRAPH},
                {"emoji": "🔧", "label": "Transform", "sub": "map to ontology", "c": ONT},
                {"emoji": "🔗", "label": "Resolve", "sub": "dedupe entities", "c": KG},
                {"emoji": "⚖️", "label": "Validate", "sub": "SHACL gate", "c": ENG},
                {"emoji": "🕸️", "label": "Load", "sub": "publish graph", "c": TWIN}],
            "foot": "Batch the wikis, stream the logs, do it incrementally — classic data engineering, new product."}, "narration":
            "Let's make ‘construction pipeline’ concrete, because this is where a graph engineer "
            "spends most of their time. It's an ETL job — extract, transform, load — but the output "
            "is meaning. [pause] Extract: a connector per source pulls the raw data. [pause] "
            "Transform: map each record onto the ontology — this SQL table becomes a Table node "
            "with these properties. [pause] Resolve: run entity resolution to collapse the "
            "duplicates, like we saw with the Orders table. [pause] Validate: the SHACL gate checks "
            "the candidate graph before anything is published. [pause] Load: publish the new "
            "version. [pause] And the cadence differs per source. The wiki and repo you can batch "
            "nightly. The AKS logs you stream continuously. Everything runs incrementally — only "
            "what changed. [pause] It's the same shape as any data pipeline you've built. The "
            "twist is that the product isn't a table — it's a validated model of meaning. Now, how "
            "you talk to it."},

        {"id": "querylangs", "variant": "kg_compare", "props": {"kicker": "SPEAKING TO THE GRAPH", "title": "The query languages — and the standard that's unifying them", "color": ENG,
            "left": {"head": "Cypher & GQL", "sub": "property graphs", "c": KG, "rows": [
                "Cypher: readable ASCII-art patterns.",
                "‘(a)-[:USES]->(b)’ says what you mean.",
                "GQL: the 2024 ISO standard — SQL for graphs.",
                "The default for operational graph apps."]},
            "right": {"head": "SPARQL", "sub": "RDF triplestores", "c": ONT, "rows": [
                "The W3C standard for querying triples.",
                "Federates across many endpoints at once.",
                "Pairs with OWL inference and SHACL.",
                "The default when meaning must be portable."]},
            "foot": "GQL is doing for graphs what SQL did for tables — one standard everyone can target."}, "narration":
            "You talk to graphs in one of two dialects. [pause] For property graphs, it's Cypher — "
            "and its patterns are almost pictures. You literally write parentheses-a, arrow-uses, "
            "parentheses-b, and it reads like the diagram. [pause] The big news is GQL — the "
            "Graph Query Language — which became an official ISO standard in twenty twenty-four. "
            "[pause] GQL is doing for graphs exactly what SQL did for tables decades ago: giving "
            "everyone one standard to target. That's a signal this whole field is maturing. [pause] "
            "For RDF triplestores, the language is SPARQL — a W3C standard that can federate a "
            "query across many databases at once, and pairs naturally with OWL inference and "
            "SHACL. [pause] The rule of thumb: Cypher or GQL when you're building an operational "
            "app; SPARQL when meaning has to travel across teams and vendors. [pause] Now, the step "
            "that keeps the whole thing trustworthy — validation."},

        {"id": "text2cypher", "variant": "kg_code", "props": {"kicker": "TEXT-TO-CYPHER", "title": "Let the model write the query — the ontology keeps it honest", "color": ENG, "lang": "python + cypher",
            "lines": [
                "# user: “what breaks if we drop orders.region?”",
                "cypher = llm.to_cypher(question, schema=ONTOLOGY)",
                "",
                "MATCH (c:Column {name:'orders.region'})",
                "  <-[:HAS_COLUMN]-(:Table)<-[:READS]-(:Query)",
                "  <-[:USES]-(r:Report)",
                "RETURN r.name    // validated before it runs"],
            "result": ["Regional Sales", "Exec Dashboard", "Ops Heatmap"],
            "caption": "the ontology is the schema that keeps a generated query valid and safe",
            "foot": "This is the bridge to part six: the agent's main tool is ‘turn a question into a graph query’."}, "narration":
            "Here's a technique that quietly changed everything: text-to-Cypher. [pause] A user asks "
            "in plain English — ‘what breaks if we drop orders dot region?’ [pause] A language "
            "model translates that into a graph query. But — and this is the key — it's given the "
            "ontology as the schema. So it knows a Column has-column a Table, which is read-by a "
            "Query, which is used-by a Report. [pause] It writes a correct multi-hop query, and "
            "that query is validated against the ontology before it's ever run. A hallucinated "
            "table name simply fails the check. [pause] The result comes straight back: three "
            "reports would break. [pause] Notice what just happened — non-engineers can now ask the "
            "graph anything, safely. [pause] And this is the bridge to part five. The agent's single "
            "most important tool is exactly this: turn a question into a validated graph query. "
            "Which is why the graph engineer's work is what makes the agent possible. First, one "
            "more guardrail."},

        {"id": "shaclgate", "variant": "kg_code", "props": {"kicker": "VALIDATION AS A GATE", "title": "Bad meaning should fail the build, like bad code does", "color": ENG, "lang": "shacl / ci",
            "lines": [
                "# every ingest run, before load:",
                "shacl validate \\",
                "  --shapes  ontology/shapes.ttl \\",
                "  --data    build/candidate-graph.ttl",
                "",
                "✗ Report ‘Exec Dashboard’ violates ReportShape",
                "  → sh:minCount 1 on :uses  (found 0)",
                "BUILD FAILED · graph not published"],
            "result": ["12,481 nodes", "checked", "1 violation", "load blocked ✓"],
            "caption": "the same SHACL shapes from part one, now running in CI on every rebuild",
            "foot": "Neuro-symbolic in miniature: the rules are the symbolic guard on everything that enters."}, "narration":
            "Remember that SHACL shape from part one — every report must use at least one query? "
            "[pause] Here's where it pays off. [pause] A graph engineer runs SHACL validation as a "
            "gate in the build pipeline. Every time you rebuild the graph, before anything is "
            "published, the candidate graph is checked against the shapes. [pause] Look: the Exec "
            "Dashboard report has zero queries attached — it violates the rule. [pause] So the "
            "build fails, loudly, and the broken graph is never published. [pause] This is exactly "
            "how we treat code: bad code fails the tests. Now bad meaning fails the build. [pause] "
            "And here's a preview of something important — this is neuro-symbolic thinking in "
            "miniature. The symbolic rules stand guard over whatever tries to enter the graph. "
            "[pause] Hold that thought, because in part five, those same rules will stand guard "
            "over an AI agent. [pause] But first — the most powerful thing you can do with graph "
            "structure: learn from it."},

        {"id": "governance", "variant": "kg_cards", "props": {"kicker": "SECURITY & GOVERNANCE", "title": "Who can see and do what — enforced on the graph", "color": ENG,
            "cards": [
                {"head": "Relationship-level access", "emoji": "🔒", "body": "Hide sensitive nodes and edges per role — the ontology's security dimension, made real.", "tag": "access"},
                {"head": "PII & compliance", "emoji": "🛡️", "body": "Tag sensitive nodes; lineage proves exactly where regulated data flows, for audits.", "tag": "compliance"},
                {"head": "Change control", "emoji": "📝", "body": "Version the ontology and review changes to meaning like you review changes to code.", "tag": "governance"}],
            "foot": "Once agents act on the graph, governance is the line between a system that helps and one that harms."}, "narration":
            "One area engineers underestimate until an auditor shows up: governance. [pause] "
            "Remember the security dimension of the ontology from part one? This is where it becomes "
            "real. [pause] You enforce access at the relationship level — hiding sensitive nodes "
            "and edges depending on who is asking, human or agent. [pause] You tag the nodes that "
            "hold personal or regulated data, and because lineage is already in the graph, you can "
            "prove exactly where that data flows — which is gold during a compliance audit. [pause] "
            "And you version the ontology itself, reviewing changes to meaning the same way you "
            "review changes to code. [pause] Here's why this matters more than it used to. The "
            "moment an AI agent can act on the graph, governance stops being paperwork. It becomes "
            "the line between a system that helps, and one that quietly does harm."},

        {"id": "observability", "variant": "kg_cards", "props": {"kicker": "GRAPH DATA QUALITY", "title": "Monitor the graph like a production service", "color": ENG,
            "cards": [
                {"head": "Quality metrics", "emoji": "📊", "body": "Track orphan nodes, duplicate rate, and constraint violations over time — a dashboard for the graph itself.", "tag": "metrics"},
                {"head": "Drift alerts", "emoji": "🚨", "body": "If extraction quality drops, page someone. The graph is a product with an SLA, not a side project.", "tag": "SLO"},
                {"head": "Golden queries", "emoji": "🎯", "body": "A suite of known-answer queries runs on every build — integration tests, but for meaning.", "tag": "tests"}],
            "foot": "You already monitor your services. Monitor the graph the same way — everything now leans on it."}, "narration":
            "One last piece of the craft, and it's the one teams forget until it bites them: "
            "observability of the graph itself. [pause] Once the graph is load-bearing — once "
            "reports, twins, and agents all depend on it — it needs the same operational care as "
            "any service. [pause] Track quality metrics: how many orphan nodes, what's the "
            "duplicate rate, how many constraint violations, and are those trending up? [pause] Set "
            "drift alerts. If your LLM extraction quality quietly degrades, someone should get "
            "paged — because the graph has an SLA now. [pause] And keep a suite of golden queries: "
            "known questions with known answers that run on every rebuild. They're integration "
            "tests, but for meaning. [pause] The mindset is simple: you already monitor your "
            "microservices. Monitor the graph exactly the same way, because everything above it now "
            "leans on it. [pause] Alright — the most powerful thing graph engineering unlocks: "
            "learning from structure."},

        {"id": "gnn", "variant": "kg_gnn", "props": {"foot":
            "Uber ETAs, Pinterest recs, fraud rings, drug discovery — all learned on graph structure."}, "narration":
            "Everything so far has queried the graph. But you can also learn from its shape, using "
            "graph neural networks — GNNs. [pause] The core idea is beautifully simple. Each node "
            "gathers information from its neighbors. [pause] Then it gathers from its neighbors' "
            "neighbors. [pause] Watch the signal spread outward, one ring per layer. After a few "
            "hops, every node holds a rich summary of its whole neighborhood — an embedding. "
            "[pause] Why does that matter? Because the structure itself is predictive. [pause] A "
            "GNN can predict missing edges — ‘this report probably depends on that table, even "
            "though nobody wrote it down’. It can spot anomalies — a node behaving unlike its "
            "neighbors. [pause] This isn't academic. Uber uses GNNs for Eats recommendations and "
            "map ETAs. Pinterest uses them at billions-of-queries scale. Banks use them to catch "
            "fraud rings. [pause] So, to recap part four: graph engineering is the craft of "
            "building, validating, querying, and learning from the graph, so every layer above it "
            "can trust it. [pause] Which brings us, finally, to the mind that acts."},
    ]},

    # ========================================================= CH06 — AGENTIC ENGINEERING
    {"id": "kg-ch06-agentic", "title": "Agentic Engineering", "segments": [
        {"id": "divider", "variant": "kg_divider", "props": {"n": 5, "title": "Agentic Engineering", "sub": "the acting mind — AI agents that retrieve, reason, and act on the graph", "color": AGENT, "layer": 4}, "narration":
            "Part five. Agentic engineering — the acting mind. [pause] Now we put an AI on top of "
            "everything we've built. And this is where the whole stack finally pays off."},

        {"id": "loop", "variant": "kg_agentloop", "props": {"foot":
            "The graph is the agent's memory, its senses, and its list of safe things to do."}, "narration":
            "An AI agent runs a simple loop: observe, reason, act. [pause] What changes everything "
            "is what it observes, reasons over, and acts through. [pause] It observes the "
            "knowledge graph and the live twin — so it sees the real, current state of your "
            "system, not a stale snapshot. [pause] It reasons by walking multi-hop paths across "
            "the graph — following relationships the way a senior engineer would, not guessing "
            "from similar-sounding text. [pause] And it acts through the typed actions the "
            "ontology defined back in part one — a fixed menu of safe verbs, not arbitrary "
            "commands. [pause] Look at the shape of this. The graph is simultaneously the agent's "
            "memory, its senses, and its list of allowed moves. [pause] That's the thesis of the "
            "entire hour in one picture. [pause] Strip the graph away and this loop is just a "
            "chatbot spinning stories. Wrap it around the graph, and it becomes a colleague that "
            "actually knows your system. Let's unpack each piece."},

        {"id": "retrieval", "variant": "kg_cards", "props": {"kicker": "GROUNDING & MEMORY", "title": "How the agent stays factual and remembers", "color": AGENT,
            "cards": [
                {"head": "GraphRAG retrieval", "emoji": "🎯", "body": "Pull the exact connected subgraph the question needs — that 86%-vs-32% edge from part two.", "tag": "grounding"},
                {"head": "Persistent memory", "emoji": "🧠", "body": "Tools like cognee give the agent a graph-shaped memory across sessions — not a goldfish.", "tag": "cognee"},
                {"head": "Typed actions", "emoji": "⚡", "body": "It can only call the operations the ontology allows — open a work item, page an owner.", "tag": "governed"}],
            "foot": "Grounded retrieval + durable memory + a safe action menu — the anti-hallucination kit."}, "narration":
            "First, how does the agent stay factual? Three pieces. [pause] Grounding, through "
            "GraphRAG. Instead of dumping random text into the prompt, the agent retrieves the "
            "exact connected subgraph the question needs. That's the eighty-six versus thirty-two "
            "advantage from part two, now working for the agent. [pause] Memory. On its own, a "
            "model is a goldfish — it forgets everything between sessions. Tools like cognee give "
            "it a persistent, graph-shaped memory, so it remembers your system across "
            "conversations. [pause] And typed actions. The agent can only invoke the operations "
            "the ontology declared safe — open a work item, page an owner. It cannot freelance. "
            "[pause] Grounded retrieval, durable memory, and a bounded action menu. That's the "
            "core anti-hallucination kit. [pause] But there's one more guarantee we can add — a "
            "way to verify the agent before it ever acts."},

        {"id": "context", "variant": "kg_cards", "props": {"kicker": "CONTEXT ENGINEERING", "title": "The real skill: what you put in front of the model", "color": AGENT,
            "cards": [
                {"head": "The subgraph", "emoji": "🕸️", "body": "Retrieve the small, relevant slice of the graph — not the whole thing, not random text.", "tag": "retrieve"},
                {"head": "The schema", "emoji": "📐", "body": "Give the model the ontology so it grounds its terms and writes valid queries.", "tag": "ground"},
                {"head": "Tools & memory", "emoji": "🧰", "body": "Expose exactly the right MCP tools and recall past context — no more, no less.", "tag": "scope"}],
            "foot": "Prompt engineering grew up into context engineering — and the graph is your best context source."}, "narration":
            "Here's a shift in how good agents get built — the field moved from prompt engineering to "
            "context engineering. [pause] The insight is that an agent is only as good as what you "
            "put in front of the model, and the graph is your best possible context source. [pause] "
            "First, you retrieve the subgraph — the small, relevant slice the question actually "
            "needs, not the whole graph and not a pile of random text. [pause] Second, you hand the "
            "model the ontology as schema, so it grounds its terms and writes valid queries. "
            "[pause] Third, you expose exactly the right tools and the right memory — no more, no "
            "less. [pause] Done well, the model spends its intelligence on reasoning, not on "
            "guessing what things mean. [pause] That discipline — curating precise, grounded "
            "context from the graph — is the real craft of agentic engineering."},

        {"id": "ragpatterns", "variant": "kg_compare", "props": {"kicker": "TWO FLAVORS OF GRAPHRAG", "title": "Pinpoint questions and big-picture questions need different retrieval", "color": AGENT,
            "left": {"head": "Local (entity) search", "sub": "pinpoint", "c": KG, "rows": [
                "Starts at specific entities.",
                "Follows their local neighborhood.",
                "Best for ‘why did THIS break?’",
                "Precise, fast, and cheap."]},
            "right": {"head": "Global (community) search", "sub": "big picture", "c": TWIN, "rows": [
                "Summarizes graph ‘communities’.",
                "Answers broad, thematic questions.",
                "Best for ‘what are our top risks?’",
                "Reasons over the whole corpus."]},
            "foot": "Local for a pinpoint question, global for the big picture — serious systems ship both."}, "narration":
            "A practical detail that trips people up: GraphRAG isn't one thing. There are two "
            "retrieval modes, and you pick per question. [pause] Local search — sometimes called "
            "entity search — starts at specific nodes and explores their neighborhood. It's perfect "
            "for a pinpoint question like ‘why did this report break?’ Precise, fast, cheap. [pause] "
            "Global search is different. It pre-summarizes clusters of the graph — communities — "
            "and reasons over those summaries. It's built for broad, thematic questions like ‘what "
            "are the biggest risks across our whole platform?’ [pause] Vector RAG simply can't "
            "answer that second kind, because the answer isn't in any single chunk — it's spread "
            "across the whole corpus. [pause] The takeaway: a pinpoint question wants local; a "
            "big-picture question wants global. Real systems implement both and route between them. "
            "[pause] Now, the guarantee that makes any of this safe to act on."},

        {"id": "twobrain", "variant": "kg_twobrain", "props": {"foot":
            "Creativity from the model, guarantees from the graph — together, that's trustworthy AI."}, "narration":
            "This is the idea I've been promising since part one: neuro-symbolic AI. [pause] Two "
            "brains, working together. [pause] On the left, the language model. It's flexible, "
            "fluent, and fast. It reads the messy prose, spots the pattern, and proposes an answer "
            "or an action. [pause] But — it can hallucinate. On its own, you can't fully trust it. "
            "[pause] So on the right, a symbolic brain: a reasoner and our SHACL rules. It doesn't "
            "guess. It checks the model's proposal against the ontology before anything is allowed "
            "to happen. [pause] The candidate flows from the fast, creative brain to the strict, "
            "auditable one — and only a valid proposal gets stamped and passed through. [pause] "
            "This is the same validation gate from part four, now standing between the agent and "
            "the real world. [pause] Creativity from the model, guarantees from the graph. Neither "
            "half is trustworthy alone; together, they're the architecture behind serious "
            "enterprise AI. [pause] Now, the concrete frameworks that build all this."},

        {"id": "patterns", "variant": "kg_cards", "props": {"kicker": "AGENT DESIGN PATTERNS", "title": "Three loops worth knowing by name", "color": AGENT,
            "cards": [
                {"head": "ReAct", "emoji": "🔁", "body": "Reason, then act with a tool, then observe — and repeat. The workhorse loop.", "tag": "reason+act"},
                {"head": "Plan-and-execute", "emoji": "🗺️", "body": "Draft a full plan first, then run the steps — better for complex, multi-tool tasks.", "tag": "plan"},
                {"head": "Reflection", "emoji": "🔍", "body": "The agent critiques its own output and retries — catching mistakes before you see them.", "tag": "self-check"}],
            "foot": "LangGraph makes all three explicit as graphs of steps — pick the shape per task."}, "narration":
            "A quick vocabulary upgrade, because these three patterns come up constantly. [pause] "
            "The first is ReAct — reason, then act with a tool, then observe the result, and repeat. "
            "It's the workhorse loop behind most agents, including our root-cause investigator. "
            "[pause] The second is plan-and-execute. Instead of deciding one step at a time, the "
            "agent drafts a whole plan up front, then runs it. That's stronger for complex tasks "
            "that touch many tools. [pause] The third is reflection: the agent critiques its own "
            "output and tries again — a cheap way to catch mistakes before you ever see them. "
            "[pause] You don't choose forever; LangGraph lets you express all three as graphs of "
            "steps and pick the right shape per task. [pause] Knowing their names makes the whole "
            "ecosystem of tutorials and frameworks suddenly legible."},

        {"id": "multiagent", "variant": "kg_cards", "props": {"kicker": "ONE AGENT, OR A TEAM?", "title": "Split the work when a single prompt gets overloaded", "color": AGENT,
            "cards": [
                {"head": "Planner", "emoji": "🧭", "body": "Breaks the question into steps — retrieve, correlate, decide — and delegates each.", "tag": "orchestrate"},
                {"head": "Specialists", "emoji": "🔬", "body": "A graph-query agent, a log agent, an action agent — each an expert at exactly one tool.", "tag": "divide"},
                {"head": "Orchestrator", "emoji": "🔀", "body": "LangGraph wires them with loops and checks, so the team retries and revises instead of failing.", "tag": "LangGraph"}],
            "foot": "Start with one agent. Split into a team only when a single prompt is doing too much."}, "narration":
            "As tasks get harder, one question comes up: should this be a single agent, or a team? "
            "[pause] The multi-agent pattern splits the work. [pause] A planner reads the request "
            "and breaks it into steps — retrieve this, correlate that, then decide. [pause] "
            "Specialist agents each own one tool: a graph-query agent, a log agent, an action "
            "agent. Each one is simple and expert, instead of one giant prompt trying to do "
            "everything. [pause] And an orchestrator — LangGraph is the common choice — wires them "
            "together with loops and checkpoints, so when a step fails, the team retries or revises "
            "rather than collapsing. [pause] A word of caution, though: don't start here. A "
            "multi-agent system is harder to debug and more expensive to run. [pause] Begin with "
            "one well-grounded agent. Split into a team only when a single prompt is visibly doing "
            "too much. [pause] Now, the concrete frameworks that build all of this."},

        {"id": "frameworks", "variant": "kg_orbit", "props": {"kicker": "THE 2026 TOOLKIT", "title": "The frameworks you'll actually wire together", "color": AGENT, "hub": "Agent\n+ graph",
            "items": [
                {"emoji": "🔀", "label": "LangGraph — control flow & loops"},
                {"emoji": "📚", "label": "LlamaIndex — retrieval"},
                {"emoji": "🕸️", "label": "MS GraphRAG — the index"},
                {"emoji": "🔌", "label": "MCP — the agent's hands"},
                {"emoji": "🧠", "label": "cognee — graph memory"},
                {"emoji": "⚡", "label": "Neo4j Aura Agent — ontology→agent"}],
            "foot": "Retrieval + control flow + tools + memory — composed, not a single magic box."}, "narration":
            "You don't build this from scratch — you compose it. [pause] LangGraph gives you the "
            "control flow: agents as a graph of steps, with loops and branches, so the agent can "
            "retry and revise instead of running in a straight line. [pause] LlamaIndex and "
            "Microsoft's GraphRAG handle retrieval and indexing — turning your documents and graph "
            "into something the agent can query. [pause] MCP — the Model Context Protocol — is how "
            "the agent gets hands. It's a standard way to expose tools, so the agent can reach into "
            "your DevOps, your SQL, your logs through safe, typed connectors. [pause] cognee "
            "supplies that graph-shaped memory. [pause] And watch this space: in February twenty "
            "twenty-six, Neo4j shipped Aura Agent, which builds an agent directly from your "
            "ontology and hosts it over MCP. [pause] The ontology-to-agent pipeline is becoming a "
            "product. [pause] Now let me put every one of these pieces together, on our project, to "
            "answer the question we started with."},

        {"id": "mcptools", "variant": "kg_orbit", "props": {"kicker": "MCP · THE AGENT'S HANDS", "title": "Every source becomes a typed, permissioned tool", "color": AGENT, "hub": "Agent",
            "items": [
                {"emoji": "📘", "label": "Wiki tool — read & search"},
                {"emoji": "🗂️", "label": "Repo tool — files & PRs"},
                {"emoji": "🗄️", "label": "SQL tool — run queries"},
                {"emoji": "🌐", "label": "Cosmos tool — documents"},
                {"emoji": "🖼️", "label": "Blob tool — assets"},
                {"emoji": "📜", "label": "AKS tool — logs & health"}],
            "foot": "MCP standardizes tools, so one agent reaches every source through typed, permissioned connectors."}, "narration":
            "Let's make ‘the agent takes action’ concrete, because it sounds scarier than it is. "
            "[pause] The agent's hands are tools, and the Model Context Protocol — MCP — is the "
            "standard way to give it those hands. [pause] Each of our six sources becomes an MCP "
            "tool. A wiki tool that can read and search. A repo tool for files and pull requests. "
            "A SQL tool that runs queries. Tools for Cosmos, for Blob, and for the AKS logs and "
            "health. [pause] Because it's a standard, the same agent can reach every system through "
            "clean, typed, permissioned connectors — and you control exactly what each tool is "
            "allowed to do. [pause] This is why MCP took off so fast: it turns ‘integrate an agent "
            "with my stack’ from a custom project into plugging in a few standard tools. [pause] "
            "The graph tells the agent what to do; MCP is how it actually reaches out and does it. "
            "[pause] But before we let it loose — how do we know we can trust it?"},

        {"id": "eval", "variant": "kg_cards", "props": {"kicker": "TRUST, BUT VERIFY", "title": "An agent you can't evaluate or audit isn't production-ready", "color": AGENT,
            "cards": [
                {"head": "Eval sets", "emoji": "📋", "body": "Known incidents with known root causes — measure the agent's F1 like a model, on every change.", "tag": "measure"},
                {"head": "Human-in-the-loop", "emoji": "✋", "body": "Read-only actions auto-run; risky writes wait for one click of human approval.", "tag": "gate"},
                {"head": "Full audit trail", "emoji": "🧾", "body": "Every hop and action is logged on the graph — you can always ask ‘why did it do that?’", "tag": "explain"}],
            "foot": "The great demo is easy. Evaluation, approval gates, and audit are what make it shippable."}, "narration":
            "Before an agent touches production, three things separate a slick demo from something "
            "you can actually ship. [pause] First, evaluation. Build a set of known incidents with "
            "known root causes, and measure the agent's accuracy — its F1 — on every change, just "
            "like you'd evaluate a model. If a prompt tweak drops the score, you'll know before "
            "your users do. [pause] Second, human-in-the-loop. Let read-only actions run freely, "
            "but make risky writes — deleting, deploying, paging an exec — wait for one click of "
            "approval. [pause] Third, a full audit trail. Because every hop and every action is "
            "logged on the graph, you can always answer the question a regulator or a teammate will "
            "ask: why did it do that? [pause] The demo is the easy part. Evaluation, approval "
            "gates, and audit are what make an agent trustworthy. [pause] Now — everything we've "
            "built, working as one, on the question we started with."},

        {"id": "traverse", "variant": "kg_traverse", "props": {"foot":
            "Retrieve on the graph, reason over the path, act through a governed tool. That's the whole video."}, "narration":
            "One hour ago, ‘report X is wrong, why?’ meant six tabs and three Slack pings. Watch "
            "what it means now. [pause] The agent starts at Report X. It walks the ‘uses’ edge to "
            "the query. [pause] It walks ‘reads’ to the Orders table. [pause] From the table, it "
            "finds a schema change from nine-fourteen this morning — a column was renamed. [pause] "
            "It correlates that with a spike of null-region errors in AKS pod seven-f. [pause] And "
            "it lands on the root cause: a breaking migration, number four eighty-two. [pause] "
            "Then — because the ontology gave it a safe action — it opens a DevOps work item and "
            "assigns the owner. It doesn't just diagnose; it acts, with an audit trail. [pause] "
            "This isn't hypothetical. Research on graph-guided root-cause agents pushed accuracy "
            "from an F-one of point-six-one to point-nine-one, and turned thirty-minute "
            "investigations into about two minutes. [pause] Retrieve on the graph, reason over the "
            "path, act through a governed tool. Every layer we built, working as one. [pause] So, "
            "to recap part five: an agent grounded on this stack is trustworthy because the graph "
            "gives it truth, memory, and guardrails. Let's assemble the whole picture."},
    ]},

    # ========================================================= CH07 — TOGETHER
    {"id": "kg-ch07-together", "title": "Putting It Together", "segments": [
        {"id": "divider", "variant": "kg_divider", "props": {"n": 6, "title": "Put It Together", "sub": "the full architecture, an adoption path, and how to start Monday", "color": GRAPH, "layer": -1}, "narration":
            "Part six. Putting it together. [pause] Let's zoom all the way out, see the whole "
            "machine at once, and then figure out how you actually start."},

        {"id": "architecture", "variant": "kg_architecture", "props": {"foot":
            "One coherent stack — every layer earns its place, and the agent sees all of it."}, "narration":
            "Here is the entire architecture on one screen. [pause] At the bottom, your six sources "
            "— wiki, repo, SQL, Cosmos, Blob, and logs — flow upward. [pause] They feed the "
            "ontology, which gives them shared meaning. [pause] The ontology, filled with resolved "
            "data, becomes the knowledge graph — the memory. [pause] Telemetry turns that graph "
            "into a live digital twin — the senses. [pause] Graph engineering, all around it, "
            "keeps it built, valid, and fast — the body. [pause] And at the top, the agent, "
            "reasoning across every layer and acting for you — the mind. [pause] Follow the flow "
            "rising up the spine: raw data enters at the bottom, and grounded, governed action "
            "comes out the top. [pause] Every layer we spent the last hour on is here, and each one "
            "makes the next one possible. This is the coherent whole those five separate blog-post "
            "topics were always trying to be. [pause] Now — how do you get here without boiling "
            "the ocean?"},

        {"id": "dayinlife", "variant": "kg_cards", "props": {"kicker": "A DAY IN THE LIFE", "title": "Three questions the living map answers for you", "color": GRAPH,
            "cards": [
                {"head": "“What breaks if…?”", "emoji": "💥", "body": "Impact analysis before any change — the cascade simulation from part three.", "tag": "change"},
                {"head": "“Why is this wrong?”", "emoji": "🔎", "body": "Autonomous root cause across data, code, and logs — the traversal from part five.", "tag": "incident"},
                {"head": "“How does this work?”", "emoji": "🧭", "body": "A new hire asks the graph and gets the real architecture, not tribal knowledge.", "tag": "onboard"}],
            "foot": "This is the ‘use it every day’ payoff: three threads of Slack become three answered questions."}, "narration":
            "Let's make the day-to-day payoff concrete, because that's the whole point of building "
            "this. Three questions you'll ask it constantly. [pause] One: what breaks if I change "
            "this? That's impact analysis — the cascade simulation from part three — run before you "
            "ship, not after. [pause] Two: why is this wrong? That's the autonomous root cause from "
            "part five, walking across your data, code, and logs to the real answer. [pause] Three: "
            "how does this even work? A new engineer asks the graph and gets the actual, current "
            "architecture — not half-remembered tribal knowledge from whoever is still around. "
            "[pause] Every one of these used to be a thread of Slack messages and a lost afternoon. "
            "[pause] With the living map, they're just questions with answers. That is what it means "
            "to use this every single day."},

        {"id": "adopt", "variant": "kg_timeline", "props": {"kicker": "START MONDAY · THE ADOPTION PATH", "title": "You build one layer at a time — each is useful on its own", "color": GRAPH,
            "steps": [
                {"label": "Model the ontology", "sub": "20 core entities and their links — the shared words for your domain"},
                {"label": "Build the graph", "sub": "wire 2–3 sources, resolve entities, ship one multi-hop query"},
                {"label": "Make it live", "sub": "stream telemetry into node state — now it's a twin"},
                {"label": "Add the agent", "sub": "GraphRAG + typed actions + SHACL guardrails"}],
            "foot": "Each step ships value before the next one starts. Never a two-year moonshot."}, "narration":
            "The trap is thinking this is a two-year moonshot. It isn't. You build it one layer at "
            "a time, and each layer is useful before the next one exists. [pause] Step one: model "
            "a small ontology. Twenty core entities for your domain — Report, Query, Table, "
            "Service, and so on — plus the key relationships. A whiteboard afternoon, not a "
            "committee. [pause] Step two: build the graph from just two or three sources, resolve "
            "the entities, and ship a single multi-hop query that used to take a human an hour. "
            "That alone will win people over. [pause] Step three: stream in telemetry so the graph "
            "reflects the live system — now you have a twin. [pause] Step four: put an agent on top "
            "— GraphRAG for grounding, typed actions for safety, SHACL as the guardrail. [pause] "
            "Notice the order. Meaning first, then memory, then senses, then the mind. [pause] "
            "Skip ahead — bolt an agent onto raw data with no graph — and you get exactly the "
            "confident, wrong chatbot everyone's tired of. Build in order, and each step earns the "
            "next."},

        {"id": "buildbuy", "variant": "kg_compare", "props": {"kicker": "BUILD vs BUY", "title": "A quick decision guide for the whole stack", "color": GRAPH,
            "left": {"head": "Assemble open-source", "sub": "control", "c": ENG, "rows": [
                "Neo4j or RDF + GraphRAG + LangGraph + MCP.",
                "Maximum control, low license cost.",
                "You own the integration work.",
                "Best for custom or unusual domains."]},
            "right": {"head": "Adopt a platform", "sub": "speed", "c": TWIN, "rows": [
                "Palantir Foundry or Azure Digital Twins.",
                "Faster to value, governance built in.",
                "Less glue code, more opinions.",
                "Best when speed beats fine control."]},
            "foot": "Most teams start open-source on one use case, then buy where scale and governance demand it."}, "narration":
            "You'll face one big decision early: build it from open-source parts, or buy a "
            "platform? Here's a clean way to think about it. [pause] Assembling open-source gives "
            "you maximum control and almost no license cost. Neo4j or an RDF store, GraphRAG for "
            "retrieval, LangGraph for orchestration, MCP for tools. The trade is that you own the "
            "integration work. It's the right call for a custom or unusual domain. [pause] Adopting "
            "a platform — Palantir Foundry, or Azure Digital Twins for our stack — gets you to "
            "value faster, with governance and security built in. The trade is less flexibility and "
            "more opinions baked in. It's the right call when speed matters more than fine control. "
            "[pause] And honestly, it's rarely all-or-nothing. Most teams start open-source to prove "
            "one use case cheaply, then buy a platform for the parts where scale and governance "
            "become the hard problem. [pause] Whichever way you go, someone has to build it — so who?"},

        {"id": "pitfalls", "variant": "kg_cards", "props": {"kicker": "WHAT GOES WRONG", "title": "The four failure modes to design against", "color": BAD,
            "cards": [
                {"head": "Over-modeling", "emoji": "🐘", "body": "A perfect 500-class ontology no one finishes. Start with 20 that earn their keep.", "tag": "ontology"},
                {"head": "The stale twin", "emoji": "🕰️", "body": "Telemetry drifts and the model lies. An out-of-date twin is worse than none.", "tag": "twin"},
                {"head": "Skipping resolution", "emoji": "👥", "body": "No entity resolution → duplicate nodes → quietly wrong answers everywhere.", "tag": "graph"},
                {"head": "Ungoverned agents", "emoji": "🔥", "body": "Untyped actions and no SHACL gate → a confident agent doing real damage.", "tag": "agent"}],
            "foot": "Every one of these is a discipline problem, not a technology problem."}, "narration":
            "Let me save you some scars. Four failure modes, one per layer. [pause] At the ontology "
            "layer: over-modeling. Teams try to build the perfect five-hundred-class ontology and "
            "never ship. Start with twenty classes that earn their keep, and grow. [pause] At the "
            "twin layer: staleness. If your telemetry drifts, the model quietly starts lying — and "
            "an out-of-date twin is worse than no twin, because people trust it. [pause] At the "
            "graph layer: skipping entity resolution. We saw it — duplicate nodes give you "
            "confidently wrong answers everywhere. [pause] And at the agent layer: no governance. "
            "Untyped actions and no validation gate mean a confident agent can do real damage, "
            "fast. [pause] Notice something. Not one of these is a technology problem. Every single "
            "one is a discipline problem — which means every one is in your control. [pause] So "
            "where is all of this heading?"},

        {"id": "metrics", "variant": "kg_cards", "props": {"kicker": "PROVE IT'S WORKING", "title": "The numbers that show the map is earning its keep", "color": GRAPH,
            "cards": [
                {"head": "MTTR down", "emoji": "⏱️", "body": "Mean time to resolve incidents — the clearest before-and-after number you have.", "tag": "incidents"},
                {"head": "Self-served answers", "emoji": "💬", "body": "Questions answered by the graph instead of by a senior engineer's DMs.", "tag": "leverage"},
                {"head": "Coverage", "emoji": "📊", "body": "The share of your systems and sources actually modeled and kept live.", "tag": "growth"}],
            "foot": "Pick one, baseline it before you start, and let the graph earn the next round of investment."}, "narration":
            "Finally, how do you prove it's working — so you get to keep building it? Track three "
            "numbers. [pause] Mean time to resolve incidents. This is the clearest before-and-after "
            "story: an afternoon of investigation becomes a two-minute answer. Baseline it before "
            "you start. [pause] Self-served answers: how many questions the graph handles that used "
            "to land in a senior engineer's direct messages. That's pure leverage, and people "
            "notice it fast. [pause] And coverage: what share of your systems and sources are "
            "actually modeled and kept live. That's your growth metric. [pause] The move is simple "
            "— pick one, baseline it honestly, and let the results earn the next round of "
            "investment. [pause] A living map that can't show its value won't survive next "
            "quarter's priorities. Make it prove itself."},

        {"id": "roles", "variant": "kg_cards", "props": {"kicker": "WHO BUILDS THE LIVING MAP", "title": "Three hats — sometimes worn by two people", "color": GRAPH,
            "cards": [
                {"head": "Ontologist / domain expert", "emoji": "🦉", "body": "Owns the shared meaning. Usually a senior engineer who knows the domain — not a PhD in logic.", "tag": "meaning"},
                {"head": "Graph / data engineer", "emoji": "🏗️", "body": "Owns construction, entity resolution, validation, and performance — the whole substrate.", "tag": "substrate"},
                {"head": "Agent engineer", "emoji": "🤖", "body": "Owns retrieval, tools, guardrails, and evaluation — the acting mind on top.", "tag": "agents"}],
            "foot": "Add a graph-ML specialist when GNNs enter the picture. You don't need a big team to start."}, "narration":
            "So who actually builds this? Reassuringly few people. Three hats, and often just two "
            "humans wearing them. [pause] The ontologist, or domain expert, owns the shared "
            "meaning. And here's the myth to kill — this is usually a senior engineer who deeply "
            "knows the domain, not a philosopher with a PhD in logic. [pause] The graph or data "
            "engineer owns the substrate: the construction pipelines, entity resolution, "
            "validation, and performance. If you have data engineers, they already have most of "
            "these skills. [pause] And the agent engineer owns the acting mind — retrieval, tools, "
            "guardrails, and evaluation. [pause] Add a graph-ML specialist only when GNNs enter the "
            "picture. [pause] The point is, you do not need a moonshot team to begin. A couple of "
            "capable engineers and a clear domain can ship the first useful layer in weeks. [pause] "
            "So where is all of this heading next?"},

        {"id": "future", "variant": "kg_cards", "props": {"kicker": "WHERE THIS IS GOING", "title": "The 2026 convergence — and why it matters now", "color": GRAPH,
            "cards": [
                {"head": "Ontology ⨝ Agents", "emoji": "🤝", "body": "Ontology-to-agent pipelines like Neo4j Aura Agent and Palantir + NVIDIA are becoming products.", "tag": "convergence"},
                {"head": "Physical-AI twins", "emoji": "🤖", "body": "Omniverse & OpenUSD extend this exact stack to robots, factories, and cities.", "tag": "frontier"},
                {"head": "Neuro-symbolic default", "emoji": "⚖️", "body": "LLM-proposes / graph-verifies is becoming the standard pattern for trustworthy AI.", "tag": "standard"}],
            "foot": "The five topics are collapsing into one discipline — and the teams that see it early win."}, "narration":
            "Three currents are converging right now, and they're the reason this matters today, "
            "not someday. [pause] First, ontology and agents are merging into single products. "
            "Neo4j's Aura Agent turns an ontology straight into a hosted agent. Palantir and NVIDIA "
            "are building an operational-AI stack on exactly this pattern. [pause] Second, the "
            "physical frontier. Omniverse and OpenUSD are extending this same stack — meaning, "
            "graph, twin, agent — to robots, factories, and whole cities. [pause] Third, "
            "neuro-symbolic is becoming the default. The pattern of an LLM proposing and a graph "
            "verifying is quietly becoming the standard for any AI you're willing to trust. [pause] "
            "Step back and you can see it clearly: the five separate topics we started with — "
            "ontology, knowledge graph, digital twin, graph engineering, agentic engineering — are "
            "collapsing into one discipline. [pause] The teams that see that early are the ones "
            "who'll build the systems everyone else copies. Let's tie it all off."},

        {"id": "recap", "variant": "kg_recap", "props": {"kicker": "RECAP · THE WHOLE MAP", "title": "The living map in one breath", "closer": "Give your machines a world — and they'll stop guessing, and start knowing.",
            "items": [
                "Ontology = meaning: the shared grammar of entities, relations, and rules.",
                "Knowledge graph = memory: the ontology filled with resolved, real instances.",
                "Digital twin = live senses: the graph synced to reality, able to simulate.",
                "Graph engineering = the body: building, validating, querying, learning at scale.",
                "Agentic engineering = the mind: retrieve, reason, and act — grounded and governed.",
                "Build bottom-up on your own sources; each layer ships value before the next."]}, "narration":
            "Let's hold the whole map in one breath. [pause] Ontology is meaning — the shared "
            "grammar of your world. [pause] The knowledge graph is memory — that grammar filled "
            "with your real, resolved data. [pause] The digital twin is live senses — the graph "
            "kept in sync with reality, and able to simulate. [pause] Graph engineering is the "
            "body — the craft that keeps it built, valid, fast, and learning. [pause] And agentic "
            "engineering is the mind — an AI that retrieves, reasons, and acts, grounded and "
            "governed by everything beneath it. [pause] Five ideas, one stack, built bottom-up on "
            "your own six sources — and every layer pays for itself before the next one begins. "
            "[pause] That report that was wrong? Now it answers itself. [pause] Give your machines "
            "a world, and they'll stop guessing — and start knowing. [pause] Thanks for watching."},
    ]},
]
