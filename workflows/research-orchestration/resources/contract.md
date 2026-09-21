# research-orchestration — contract

## Runtime Variables and Defaults

This file is **repo-generic**. Do not embed project-specific absolute paths.

Defaults, when not otherwise specified:
- `DOMAIN_ROOT` = the domain package named by the human, e.g. `domains/chirality`
- `DECOMP_ROOT = {DOMAIN_ROOT}/_Decomposition`
- `LOCAL_INDEX_ROOT = {DOMAIN_ROOT}/_LocalIndexes`
- `ACCEPTED_DECOMP_POINTER = {DECOMP_ROOT}/checkpoint_snapshots/_LATEST_ACCEPTED.md`
- `LEGACY_ACCEPTED_GATE_POINTER = {DECOMP_ROOT}/gate_snapshots/_LATEST_GATE6.md`
- `RESEARCH_ROOT = {DOMAIN_ROOT}/_Research`
- `RETRIEVAL_SNAPSHOT = {LOCAL_INDEX_ROOT}/_LATEST.md`
- `DEFAULT_RETRIEVAL_MODE = hybrid`

Resolve the canonical accepted decomposition pointer first. For a historical
package that has no canonical pointer, use the legacy Gate 6 pointer or the
latest explicitly accepted legacy gate pointer. Never translate or rename a
historical pointer in place.

If a user asks a general research question without naming a domain, first look for the nearest active domain context in the prompt/session. If none is clear, ask for the domain root or accepted decomposition snapshot.

---

## Write Scope Contract

WORKING_ITEMS is read-only by default. It may write only when the human clearly asks for a durable research artifact.

Allowed writes are limited to derivative research packets under:

```text
{RESEARCH_ROOT}/RCH_<UTC>_<slug>/
```

Research packet directories are immutable run snapshots. Do not overwrite an existing `RCH_*` packet; reruns must create a new packet. `{RESEARCH_ROOT}/_LATEST.md` may be updated as a mutable pointer only after a research packet is intentionally written.

WORKING_ITEMS must not edit accepted snapshots, ledgers, registers, decomposition files, source catalogs, local indexes, source materials, publication packages, or repository metadata.

---

## Non-Negotiable Invariants

- **Accepted decomposition truth comes first.** The accepted grouped-checkpoint snapshot and companion registers are the authority boundary. An explicitly accepted legacy Gate snapshot remains a valid historical authority boundary. Mutable working files and regenerated packages are not automatically authoritative.
- **Derivative-package rule.** Source catalogs, BM25 indexes, dense embedding arrays, hypergraphs, concordance packages, summaries, and research packets are derivative unless separately accepted. They aid discovery; they do not replace accepted decomposition truth.
- **No invention.** If a claim is not supported by accepted source/decomposition evidence, mark it `UNKNOWN`, `TBD`, or `INFERENCE` and say what evidence would be needed.
- **Evidence-first answers.** Material claims must cite stable evidence: `AtomicUnitID`, `SourceRef`, `SectionID`, `CategoryID`, `KnowledgeTypeID`, `SubjectID`, source path, or accepted snapshot artifact.
- **Separate structure from similarity.** Category/KTY/Subject registers provide ontology/navigation. BM25 and dense retrieval provide discovery/significance. Semantic similarity results are not membership proof.
- **Read-only default.** Do not edit sources, ledgers, decompositions, snapshots, indexes, or registers. Optional written research notes must go under `{RESEARCH_ROOT}` and must be labeled derivative.
- **No silent refresh.** Do not rebuild source databases, retrieval indexes, embeddings, or accepted ledgers as part of ordinary research. If freshness matters, report the snapshot and any recorded caveats, then ask before refresh work.
- **External sources are separate.** If external web/library research is needed, label it as external evidence and keep it distinct from accepted domain truth. Do not merge it into the domain decomposition without a governed update path.
- **Human decision rights.** WORKING_ITEMS may recommend interpretations, candidate amendments, or downstream tasks; it does not approve them.

---

## Accepted WORKING_ITEMS (workflow: domain-decomp) Surfaces

When researching an accepted WORKING_ITEMS (workflow: domain-decomp) package, prefer these surfaces:

| Surface | Role |
|---|---|
| `checkpoint_snapshots/_LATEST_ACCEPTED.md` | canonical latest accepted checkpoint-group-3 snapshot pointer |
| `checkpoint_snapshots/<snapshot>/HANDOFF_STATE.md` | accepted source/checkpoint basis, derivative status, closure, rerun requirements, and blockers |
| `checkpoint_snapshots/<snapshot>/ACCEPTED_MANIFEST.csv` | canonical accepted artifact inventory and hashes |
| `*_Domain_Decomposition.md` or equivalent main document named by the accepted manifest | concise control surface and human-readable summary |
| `Atomic_Domain_Ledger.csv` | accepted atom ledger from checkpoint group 1 |
| accepted domain ledger named by the manifest | atom rows with accepted Category/KTY/Subject mappings; a historical `Domain_Ledger_Gate4_KTY_Draft.csv` filename may remain accepted by a legacy snapshot |
| `Category_Register.csv` | flat Category ontology/navigation partition |
| `Knowledge_Type_Register.csv` | accepted KTY definitions and parent Category |
| `Knowledge_Subject_Register.csv` | accepted Subjects and parent KTY |
| `Vocabulary_Map.csv` | accepted vocabulary/synonym surface |
| `Section_Coverage_Register.csv` | checkpoint-group-3 section coverage and attestation |
| `_LocalIndexes/_LATEST.md` | pointer to derived source catalog/retrieval snapshot |

For historical packages without `checkpoint_snapshots/_LATEST_ACCEPTED.md`,
use `gate_snapshots/_LATEST_GATE6.md` and its `HANDOFF_STATE.md` and
`Gate6_Publication_Manifest.csv`, or the latest explicitly accepted legacy gate
pointer. Clearly label that basis as legacy and state the highest accepted
checkpoint. If neither canonical nor legacy accepted evidence exists, do not
treat a working decomposition as accepted.

---

## Retrieval Stack Awareness

The source/retrieval database is a **derived local query package**. It usually includes:
- `catalog.sqlite` — derived query catalog for a source snapshot
- `SourceDocs.csv`, `Artifacts.csv`, `Chunks.csv` — review/export surfaces
- `bm25/` — lexical retrieval sidecar
- `embeddings.npy`, `embeddings_norm.npy` — dense vector sidecars, when built
- `meta.json`, `QA_Report.md` — snapshot metadata and QA

Use `tools/retrieval/query_source_index.py` for retrieval. Supported modes:

| Mode | Use |
|---|---|
| `hybrid` | default; BM25 + dense reciprocal-rank fusion when embeddings exist |
| `dense` | semantic similarity over embeddings; use for conceptual discovery |
| `bm25` | lexical matching; use for exact phrases, identifiers, and rules |

Useful filters include:
- `--chunk-type LEDGER_ATOM` for accepted atom-level retrieval
- `--chunk-type SECTION_NODE` for section-level review/search
- `--source-doc <SourceDocID>`
- `--category-id <CAT-###>`
- `--knowledge-type-id <KTY-CC-TT_*>`
- `--subject-id <SUB-CC-TT-SS_*>`
- `--archive-state ACTIVE`
- `--json` when structured post-processing is needed

Retrieval interpretation:
- Dense cosine is computed over embeddings and is corpus/model-relative.
- BM25 scores are lexical relevance evidence, not truth.
- A result outside the expected Category/KTY may be valuable interdisciplinary evidence; do not force it back into the current ontology unless the user requests an amendment analysis.

---

## Delegating to TASK with the researcher skill (Fan-Out)

For a small, in-session question, WORKING_ITEMS answers directly. For breadth — many sub-questions,
a large corpus, or a synthesis spanning several areas — WORKING_ITEMS dispatches the Type-2
executor with the effective **`researcher` skill** as one or more bounded
research streams, then synthesizes their returned packets. Discover the skill
through the effective catalog and retain its complete descriptor in the ordered
`methods` field:
`[{kind: "skill", name: "researcher", source: <descriptor.source>, sourceRootId: <descriptor.sourceRootId>}]`.
Do not hardcode an origin or reduce the selected identity to its basename. The
TASK brief supplies this file's evidence rubric, packet schema, and invariants
and the selected skill adds its bounded execution contract (runtime parameters,
structured return, re-verification of load-bearing anchors, write-as-you-go,
and partial return on failure).

When fanning out, follow the `research-orchestration` workflow (`workflows/research-orchestration/`):
triage cheap greppable facts to a direct `query_source_index.py` call; anchor lightly and
require each TASK stream using the selected `researcher` skill to re-verify load-bearing anchors; run an adversarial live critic on
load-bearing claims before they enter authority; on a transient `API 500`/timeout, **retry only
the failed stream(s)** (resume, do not restart the whole batch), cap retries, and surface
coverage-gaps rather than dropping a stream silently. WORKING_ITEMS owns the synthesis and the
recommendation; it approves nothing.

---

## Validity

### Valid Research Answer

A valid WORKING_ITEMS answer:
- identifies the accepted domain/snapshot basis, unless already obvious in-session,
- answers the user’s question directly,
- cites accepted evidence for material claims,
- distinguishes ontology/register truth from retrieval evidence,
- labels external evidence and inference separately,
- preserves caveats and unresolved issues,
- records the verification source of each evidence row (live source, retrieval index, or inherited brief),
- self-flags load-bearing claims, and reports partial results with a coverage-gaps statement when a run is incomplete rather than failing silently,
- avoids changing accepted decomposition truth.

### Evidence Quality Levels

| Level | Meaning |
|---|---|
| `R0` | Unsupported claim; not allowed except as a clearly labeled hypothesis |
| `R1` | Retrieval hit only; useful lead, not enough for exact claims |
| `R2` | Accepted ledger/register row supports the claim |
| `R3` | Accepted ledger/register row plus SourceRef/source section supports the claim |
| `R4` | Multiple accepted sources/atoms converge |
| `R5` | Accepted snapshot/gate decision explicitly records the claim |

Prefer `R3` or better for final claims. Use `R1` only as discovery evidence.

### Assertion Mode (`:READ` vs `:RUN`)

Each evidence row also carries an **AssertionMode** suffix, orthogonal to the R-level (it does not change R0–R5):

- `:READ` — supported by inspecting an artifact's existence or contents (a file is present, a row exists, a name matches). Static.
- `:RUN` — supported by an executed result (a test suite ran green, a validator passed, a query was executed, a build succeeded). Dynamic.

`:READ` and `:RUN` qualify the *same* R-level. "Tests pass," backed only by a matching filename, is at most `R2:READ`; only an executed green suite earns `:RUN`. Prefer `R3:RUN` or better for any load-bearing claim about behavior or state that can be executed or checked; never let `:READ` masquerade as `:RUN`.

### Verification Source

Each evidence row records how it was verified:

- `LIVE_TREE` — checked against the current live source/tree.
- `RETRIEVAL_INDEX` — supported only by the (possibly stale) retrieval index; a lead, not a warrant.
- `INHERITED_BRIEF` — asserted by a dispatching brief and not yet independently verified; treat as `R1`-equivalent until verified.

Recording the source makes false consensus from over-anchoring visible.

### Load-Bearing Claims

A claim is **load-bearing** when a downstream decision (acceptance, dispatch, sequencing, amendment, release) depends on it being true. WORKING_ITEMS self-flags load-bearing claims (`LoadBearing = TRUE`) so a caller knows what to double-cover. Load-bearing claims carry stricter duties: independent re-verification (never inherited from a brief), an explicit `VerificationSource`, and a `:RUN` AssertionMode wherever the claim concerns behavior or state that can be executed or checked. A load-bearing claim MUST NOT reach `R3` or better while its `VerificationSource` is `INHERITED_BRIEF`.

### Research Output Minimum

For non-trivial answers include:
- short conclusion,
- evidence bullets/table,
- caveats,
- suggested next step only when useful.

For large research packets include:
- query log,
- evidence map,
- limitations,
- handoff state.

---

## Artifacts and schemas

### Evidence Map Columns

When producing `Evidence_Map.csv`, use (the last three columns are appended to the historical
schema; readers MUST NOT reorder existing columns):

```text
EvidenceID,ClaimID,EvidenceLevel,SourceKind,ArtifactPath,SourceDocID,SourceRef,AtomicUnitID,SectionID,CategoryID,KnowledgeTypeID,SubjectID,RetrievalMode,Rank,Score,QuotedOrParaphrasedEvidence,Interpretation,Limitations,VerificationSource,AssertionMode,LoadBearing
```

- `VerificationSource` ∈ `LIVE_TREE | RETRIEVAL_INDEX | INHERITED_BRIEF` (see SPEC § Verification Source).
- `AssertionMode` ∈ `READ | RUN` (see SPEC § Assertion Mode). `RunAsserted` is expressed only via this column — no separate boolean.
- `LoadBearing` ∈ `TRUE | FALSE` (see SPEC § Load-Bearing Claims).

### Query Log Columns

`Query_Log.csv` SHOULD be **tool-emitted**, not hand-written: run
`tools/retrieval/query_source_index.py --run-log <packet>/Query_Log.csv` so logged queries
match executed queries exactly. WORKING_ITEMS appends tool-emitted rows; it does not transcribe
queries from memory. Columns:

```text
QueryID,UTC,DomainRoot,Snapshot,Mode,Query,Filters,K,ResultCount,Notes
```

### Conflict Columns

When producing `Conflicts.csv`, use:

```text
ConflictID,ClaimID,ConflictKind,Description,Contenders,SourceRefs,ProposedAuthority,HumanRuling,Limitations
```

### Amendment Candidate Columns

When research surfaces a possible change to accepted truth, record it as a first-class row in
`Amendment_Candidates.csv` (do not bury it in prose) so it can be routed to `WORKING_ITEMS (workflow: scope-change)` /
`WORKING_ITEMS (workflow: domain-decomp)`:

```text
AmendmentID,ClaimID,CandidateKind,TargetSurface,CurrentState,ProposedChange,EvidenceRefs,LoadBearing,VerificationSource,RecommendedRoute,HumanRuling,Limitations
```

- `CandidateKind` ∈ `NEW_ATOM | SCOPE_GAP | KTY_REMAP | CATEGORY_CONFLICT | SOURCE_UPDATE | VOCAB`.
- `RecommendedRoute` ∈ `WORKING_ITEMS (workflow: scope-change) | WORKING_ITEMS (workflow: domain-decomp) | RESPONSIBLE_ROLE_WITH_APPLICABLE_CHANGE_CONVENTIONS | WORKING_ITEMS (workflow: dbm-publisher)`.
- Readers may continue to accept historical `WORKING_ITEMS (workflow: change)`
  values without rewriting them. New repository-edit rows use
  `RESPONSIBLE_ROLE_WITH_APPLICABLE_CHANGE_CONVENTIONS`.
- `HumanRuling` defaults `TBD` — WORKING_ITEMS proposes; the human rules.

### Open Questions Columns

When producing `Open_Questions.csv`, use:

```text
OpenQuestionID,ClaimID,Question,WhyItMatters,EvidenceNeeded,Status
```

### Research Note Sections

```markdown
# Research Note - <topic>

Status: DERIVATIVE_RESEARCH_PACKET

## Question
## Accepted Basis
## Short Answer
## Evidence
## Interpretation
## Caveats
## Open Questions
## Handoff / Next Action
```

---
