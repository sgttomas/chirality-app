# Bounded inquiry

### Step 1 — Classify the Question

Classify the request into one primary research mode:

| Mode | Purpose | Default evidence path |
|---|---|---|
| `ONTOLOGY` | explain structure, Categories, KTYs, Subjects | registers first, retrieval second |
| `SEMANTIC_DISCOVERY` | find conceptually related atoms/sections | dense or hybrid retrieval, then ledger/register verification |
| `LEXICAL_LOOKUP` | find exact phrases, rules, IDs, names | BM25 retrieval and direct file/register reads |
| `EVIDENCE_MAP` | build a cited map for a claim/question | hybrid retrieval + ledger/register joins |
| `CROSS_CATEGORY` | inspect interdisciplinary links | dense/hybrid retrieval across Categories, then explicit cross-category labeling |
| `AMENDMENT_CANDIDATE` | identify possible decomposition updates | evidence map + clear handoff to WORKING_ITEMS (workflow: scope-change)/WORKING_ITEMS (workflow: domain-decomp) amendment |
| `EXTERNAL_AUGMENTED` | compare accepted domain truth with outside sources | accepted domain evidence first, external evidence separately labeled |

If classification is unclear, choose the smallest mode that answers the user and state the assumption.

### Step 2 — Choose Retrieval and Register Reads

Use deterministic/local surfaces before broad language-model synthesis:
- For "what is the structure?" read `Category_Register.csv`, `Knowledge_Type_Register.csv`, `Knowledge_Subject_Register.csv`.
- For "what atoms support this?" query with `--chunk-type LEDGER_ATOM`, then inspect rows in the accepted KTY ledger.
- For "where is this in source?" use `SourceRef`, `SectionID`, source HTML, and source markdown line anchors.
- For exact rule/name lookups, start with `--mode bm25`.
- For conceptual similarity, start with `--mode dense` when embeddings exist; otherwise `hybrid`/`bm25` with a caveat.
- For balanced research, start with `--mode hybrid`.

Do not rely on a retrieval preview alone when the answer turns on exact wording. Open/read the cited source or ledger row.

### Step 3 — Synthesize With Evidence

Answers should distinguish:
- **Accepted structure** — Category/KTY/Subject membership and definitions.
- **Accepted atoms** — atom statements and stable IDs from the ledger.
- **Source evidence** — `SourceRef`, line anchors, and section IDs.
- **Retrieval evidence** — BM25/dense ranks/scores as discovery support.
- **Inference** — your reasoning from the above, explicitly labeled when non-trivial.
- **Unknowns / caveats** — missing evidence, stale index caveats, or unaccepted downstream artifacts.
