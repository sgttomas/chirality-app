# research-orchestration — method

## Method

### Step 0 — Ground the Research Context

Before answering a domain-grounded question:
1. Resolve `DOMAIN_ROOT`.
2. Read the canonical accepted decomposition pointer at
   `checkpoint_snapshots/_LATEST_ACCEPTED.md`.
3. Read its accepted `HANDOFF_STATE.md` and `ACCEPTED_MANIFEST.csv`. When the
   canonical pointer is absent, resolve the historical
   `gate_snapshots/_LATEST_GATE6.md` or latest explicitly accepted legacy gate
   pointer and clearly label that compatibility basis.
4. Record the active retrieval snapshot from `{LOCAL_INDEX_ROOT}/_LATEST.md`.
5. Note any caveats, especially source-database freshness caveats or deferred refresh issues.

If the question is lightweight and the accepted context was already read in the same session, you may reuse it, but do not invent snapshot state from memory.

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

### Step 4 — Optional Research Packet

If the human asks for a durable research artifact, write under:

```text
{RESEARCH_ROOT}/RCH_<UTC>_<slug>/
```

Each packet is an immutable derivative snapshot. Do not overwrite an existing packet. If a new run supersedes an earlier packet, create a new `RCH_*` directory and, when useful, update `{RESEARCH_ROOT}/_LATEST.md` as the mutable pointer.

Minimum packet contents:
- `RESEARCH_NOTE.md`
- `Query_Log.csv`
- `Evidence_Map.csv`
- `Open_Questions.csv`
- `HANDOFF_STATE.md`

Conditional packet contents:
- `Conflicts.csv` when conflicting accepted evidence, source evidence, or derivative index evidence is found.
- `Amendment_Candidates.csv` when research surfaces a possible change to accepted truth (see STRUCTURE § Amendment Candidate Columns). Routing these as structured rows — not prose — is what gets them to `WORKING_ITEMS (workflow: scope-change)` / `WORKING_ITEMS (workflow: domain-decomp)` in Step 5.

The packet may be scaffolded deterministically with `tools/retrieval/scaffold_research_packet.py`
(immutable `RCH_<UTC>_<slug>/` with canonical headers; refuses to overwrite), so the packet shape
is not re-derived by reasoning each run.

Research packets are derivative packages. Their `HANDOFF_STATE.md` must name accepted upstream snapshot(s), retrieval snapshot(s), derivative-package status, caveats, conflict status, pointer status, coverage gaps (work not completed), and whether any amendment/downstream action is recommended.

### Step 5 — Handoff If Action Is Needed

If research identifies possible changes:
- For source/decomposition truth changes, hand off to `WORKING_ITEMS (workflow: scope-change)` or the relevant decomposition agent.
- For publication from accepted truth, hand off to `WORKING_ITEMS (workflow: dbm-publisher)` or the relevant publisher.
- For repository edits, hand the evidence and exact change scope to the
  responsible current role. That role follows the applicable project's change
  skill or repository conventions when present; the research workflow does not
  require Git or select the retained legacy `change` workflow. Preserve an
  explicitly selected historical `change` identity when processing a legacy
  run.
- For audits, hand off to the appropriate audit/review agent.

WORKING_ITEMS does not apply those changes itself.

---
