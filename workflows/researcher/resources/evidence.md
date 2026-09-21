# Research evidence and packet contract

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
- `RecommendedRoute` ∈ `WORKING_ITEMS (workflow: scope-change) | WORKING_ITEMS (workflow: domain-decomp) | WORKING_ITEMS (workflow: change) | WORKING_ITEMS (workflow: dbm-publisher)`.
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
