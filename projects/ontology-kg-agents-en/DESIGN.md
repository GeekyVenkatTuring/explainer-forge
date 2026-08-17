# The Living Map — design doc

**Topic:** Ontology → Knowledge Graph → Digital Twin → Graph Engineering → Agentic Engineering,
as ONE stack, made concrete on a real multi-source Azure/ADO project.
**Audience:** hands-on engineer. **Length:** ~60 min. **Voice:** Nova (en). **Captions:** ON. 16:9 1080p30.

## Thesis (the connective spine)
Five layers of one system that gives machines a world they can *understand and act on*:
- **Ontology** = MEANING (grammar) — what things ARE + rules. RDF/OWL/SHACL/SKOS, Protégé, DTDL, Palantir.
- **Knowledge Graph** = MEMORY (living map) — the ontology filled with real instances. Neo4j/Cypher, RDF/SPARQL, GraphRAG.
- **Digital Twin** = MIRROR (live senses) — the graph synced to reality via telemetry + simulation. DTDL/ADT, Ditto, AAS/ISO 23247, Omniverse.
- **Graph Engineering** = SUBSTRATE (the body) — building/operating it at scale. SHACL, entity resolution, GQL, GNNs.
- **Agentic Engineering** = MOTION (the acting mind) — agents that retrieve/reason/ACT. LangGraph, LlamaIndex, GraphRAG, MCP, cognee, neuro-symbolic.
Payoff: an agent WITHOUT this hallucinates; WITH it, it has a governable world model. (GraphRAG 86% vs 32% vector; entity-res +34%; RCA F1 0.61→0.91.)

## Running example (threaded through all 60 min)
"The DataPlatform project" — knowledge scattered across SIX silos:
1. ADO **Wiki** (📘 architecture/design)  2. ADO **Repo** (🗂 report defs/SQL/code)
3. **Azure SQL** (🗄 relational business data)  4. **Cosmos DB** (🌐 documents)
5. **Blob** (🖼 images/assets)  6. **AKS logs** (📜 runtime events)
Pain: "Report X shows wrong numbers — why?" = 6 tabs + 3 Slack pings.
Cure: ontology → unified KG → live twin → agent that traverses
`Report→Query→Table→schema-change ⨝ AKS error → root cause` and ACTS (opens ADO work item).

## Identity
- Theme: near-black indigo. Primary accent = graph indigo `#6366F1`.
- Semantic colors (one per LAYER — the motif): ONT amber `#FBBF24` · KG cyan `#22D3EE` ·
  TWIN violet `#A78BFA` · ENG green `#34D399` · AGENT pink `#F472B6` · BAD red `#F87171`.
- Motif: the **5-layer stack** (built in title/dividers, persistent mini-map) + a **living node-graph**
  with Flow particles (the "map that breathes"). Six source glyphs recur.
- Captions ON → local Foot sits at y=856 centered; SceneProgress bar every scene; REVEAL_SPAN=0.62.

## Scene archetypes (parameterized; chapters.py owns copy) — prefix `kg`
title · divider(n,title,sub,color) · roadmap(the 5-layer stack) · silos(6 Azure sources) ·
hook · graph(nodes,edges,flow) · triple(RDF s-p-o) · compare(A vs B cols) · cards(2–4 grid) ·
orbit(hub+items) · code(Type query panel: Cypher/SPARQL/SHACL) · chart(bars/line stat) ·
tower(stacked maturity levels) · gauge · pipeline(nodes+wires+flow) · ingest(6→1 graph) ·
merge(entity resolution, computed) · telemetry(update wave) · cascade(what-if propagation, computed) ·
agentloop · traverse(computed RCA path — THE payoff) · timeline(adoption steps) · recap.

## Chapter/beat plan (7 parts, ~45 scenes)
CH01 Problem & Stack: title · silos · hook · roadmap(stack) · graph-basics · thread-preview
CH02 Ontology (amber): divider · ont-vs-schema(compare) · triple · ont-build(graph) · shacl(code) · standards(orbit) · decision-centric(recap)
CH03 Knowledge Graph (cyan): divider · instantiate · pg-vs-rdf(compare) · ingest(6→1) · entityres(merge) · cypher(code) · graphrag(chart) · query-live(recap)
CH04 Digital Twin (violet): divider · twin-def · telemetry(wave) · maturity(tower) · standards(cards) · simulate(cascade) · operational-twin(recap)
CH05 Graph Engineering (green): divider · disciplines(orbit) · querylangs(compare) · validation(shacl gate) · gnn(graph msg-pass) · ops(recap)
CH06 Agentic (pink): divider · agentloop · retrieval(graphrag) · neurosymbolic(two-brain) · frameworks(orbit) · mcp-hands(hub) · traverse(RCA payoff) · guardrails(recap)
CH07 Together & Start Monday (indigo): divider · architecture(full) · thread-replay · adopt(timeline) · pitfalls(cards) · future · recap

## Hard-rule checklist
- All phasing useP(dur) fractions; SceneProgress on every scene; ≥1 continuous layer/frame.
- Compute the real thing: entity-res merge, what-if cascade, GNN message passing, RCA traversal.
- ≤2 new terms/min; say-and-show numbers; micro-recap ending each Part.
- Captions ON: no default Foot (use local y856); numbers on screen for 86/32/34/0.91.
