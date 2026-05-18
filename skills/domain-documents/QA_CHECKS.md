# domain-documents — QA Checks

Minimum checks for a valid run and the non-negotiable invariants preserved from the source agent.

## Non-negotiable invariants

These invariants MUST hold for every run. Violating any of them makes the run invalid.

| Invariant | Requirement |
|---|---|
| **DOMAIN pipeline only** | `DECOMP_VARIANT` must be `DOMAIN`; otherwise halt with `UNSUPPORTED_VARIANT`. This skill is not called by PROJECT or SOFTWARE variants |
| **Variable Knowledge Artifact schema** | Artifact count and names derive from `KnowledgeSubjects` in the decomposition. No fixed 4-doc kit |
| **Subject-to-Artifact bijection** | Each Knowledge Subject maps to exactly one Knowledge Artifact file. No splitting or merging |
| **Maximally comprehensive KAs** | The KA set captures all material source-backed facts, parameters, scope boundaries, interfaces, assumptions, exceptions, open issues, and current-state authority notes within the approved KTY/Subject scope |
| **KA-* naming convention** | Default `KA-01_{Type}__{Slug}.md`; configurable via `ARTIFACT_NAMING`. Stable ordinal prefix when `PREFIXED_*` |
| **One deliverable per run** | Each invocation processes exactly one Knowledge Type folder (`KTY_PATH`). No cross-Knowledge-Type scanning |
| **No human input** | The skill works from folder contents, references, and decomposition. Human interacts with ORCHESTRATOR/WORKING_ITEMS, not this skill |
| **Respect human work** | `_STATUS.md` `Current State` must be within `ALLOW_OVERWRITE_STATES` (default `OPEN, INITIALIZED`) before any overwrite. Halt with `SKIPPED_PROTECT_HUMAN_WORK` otherwise |
| **Authority mode default** | `AUTHORITY_MODE` defaults to `SOURCE_FIDELITY`; non-SCA behavior remains unchanged |
| **SCA authority mode** | `AUTHORITY_MODE: SCA_DRIVEN` requires admitted decomposition state, structured SCA artifacts, and `SUPERSESSION_MAP_PATH`; source material is provenance verification only |
| **Supersession map gate** | `SUPERSESSION_MAP_PATH` without `AUTHORITY_MODE: SCA_DRIVEN` fails input validation |
| **Supersession applicability filter** | When `ROOT_NAME` or `FACILITY_ID` is provided, supersession rows are filtered by `AppliesToRoots` / `AppliesToFacilities` before application |
| **Additional source authority root** | `COMBINED_SOURCE_AUTHORITY_PATH`, when provided, is used only as admitted source material and remains subordinate to structured SCA supersession in `SCA_DRIVEN` mode |
| **SCA overwrite override** | `ALLOW_OVERWRITE_OVERRIDE: SCA_AUTHORIZED` is valid only with `AUTHORITY_MODE: SCA_DRIVEN`, `SCA_SNAPSHOT_PATH`, and `SUPERSESSION_MAP_PATH`, and only for the dispatched KTY |
| **No metadata modification** | Never modify `_CONTEXT.md`, `_REFERENCES.md`, `_MEMORY.md`/`MEMORY.md`, or `_SEMANTIC.md`. Metadata drift discovered during regeneration must be surfaced as a follow-on alignment action, not fixed inside this skill |
| **Status-memory paired read** | Whenever `_STATUS.md` is read, sibling `_MEMORY.md` / `MEMORY.md` is read when present as non-authoritative operational context only |
| **No invention** | Missing information marked `TBD`; inferences labeled `ASSUMPTION`. Do not fabricate source excerpts when source is inaccessible |
| **Authoritative source required in default mode** | In `SOURCE_FIDELITY` mode, all passes require the source file(s) bounded by `SourceSpan` to be accessible. Halt with `FAILED_INPUTS` if source cannot be read |
| **Structured supersession only** | Do not infer supersessions from SCA prose; use structured SCA artifacts and `SUPERSESSION_MAP_PATH` |
| **Authority fidelity is the quality gate** | Pass 3 verifies artifact-to-source fidelity in `SOURCE_FIDELITY` mode and artifact-to-SCA fidelity in `SCA_DRIVEN` mode. No semantic lensing / semantic enrichment is used in the DOMAIN pipeline |
| **Safe-update status only** | `_STATUS.md` transitions `OPEN → INITIALIZED` only when Pass 1/2 ran. Never regress state |
| **No SEMANTIC_READY state** | DOMAIN lifecycle is `OPEN → INITIALIZED → IN_PROGRESS`; `SEMANTIC_READY` is NOT a valid DOMAIN state |

## Structural checks (Pass 1)

| Check | Validation |
|---|---|
| Scoping exists | `Scoping.md` present in `{KTY_PATH}` |
| Scoping identity | Contains KTY identity, Category, CanonicalSchema, intended users, when-used context |
| Scoping context | Records Subject coverage, active authority basis, and SCA/supersession impact summary when available |
| Evidence set table | Table present with UnitID → AtomicStatement → SourceRef columns |
| Artifact plan table | Table present with ArtifactID → SubjectID → SubjectName → BaseType → AddOns → Filename |
| Conflict Table | Present with stable schema (Conflict ID, Conflict, Source A, Source B, Impacted artifacts, Proposed authority, Human ruling) |
| Artifacts created | Every artifact listed in the plan table exists as a `.md` file in `{KTY_PATH}` |
| Default sections present | Each Knowledge Artifact contains all default schema sections for its base type (Reference/Guidance/Checklist/Procedure) |
| Metadata block present | Each `KA-*.md` has an Artifact Metadata block with Knowledge Type, Category, Knowledge Subject, Artifact ID, Base Type, Add-ons, Evidence Units |
| KA comprehensiveness | Each KA captures the material subject-scope facts, values, interfaces, assumptions, exceptions, open issues, and current-state authority notes available from the accepted authority inputs |
| No invented content | TBDs used for missing info; ASSUMPTION label for inferences |
| Conflicts surfaced | Contradictions logged in Scoping.md Conflict Table with evidence pointers |

## Cross-artifact consistency checks (Pass 2)

| Check | Validation |
|---|---|
| Plan-to-file closure | Every plan-table entry has a file; every `KA-*.md` file has a plan-table entry |
| No duplicate filenames | File names unique across the KTY folder |
| Identity consistency | KTY ID, Name, Category consistent across `Scoping.md` and every `KA-*.md` metadata block |
| Subject-Artifact mapping | `SubjectID ↔ ArtifactID` mappings in artifact metadata match `Scoping.md` plan table |
| Cross-artifact value consistency | Parameters, design values, equipment tags, operating conditions identical or non-contradictory across artifacts |
| Evidence traceability | Every non-trivial claim cites a UnitID, SourceRef, or is marked TBD/ASSUMPTION |
| UnitID presence | UnitIDs referenced in artifacts exist in the evidence set table in `Scoping.md` |
| SourceRef syntax | SourceRef pointers syntactically consistent across all docs |
| Terminology consistency | Same terms used consistently across artifacts; synonym drift flagged as Conflict Table entries |

## Source-fidelity checks (Pass 3)

| Check | Validation |
|---|---|
| Source file accessed in `SOURCE_FIDELITY` | Source file(s) bounded by `SourceSpan` successfully read for this KTY |
| SCA authority checked | In `AUTHORITY_MODE: SCA_DRIVEN`, admitted decomposition state, structured SCA artifacts, and `SUPERSESSION_MAP_PATH` were read before source provenance checks |
| Coverage verified | Every substantive source statement compared against artifact content |
| Accuracy verified | Every non-TBD, non-ASSUMPTION artifact claim traced to a specific source location |
| Corrections logged | Each artifact correction recorded in `Scoping.md` `## Source-Fidelity Log` section |
| Gaps logged | Source content not captured in any artifact recorded as a gap with source location |
| Unverified flagged | Claims not traceable to source marked `UNVERIFIED` or downgraded to `ASSUMPTION` |
| Source reread evidence | Each correction/enrichment records which source slice was re-read before the change was applied |
| Structural sweep re-run | After corrections, Pass 2 structural completeness checks (items 1–3) re-verified |

## Audit-on-write retrieval check (Pass 4 — when retrieval index present)

In domains where a merged Atomic_Domain_Ledger and a retrieval index over it
exist, each authored KA runs a post-draft self-audit of its claim sentences
against the retrieval index. This is independent of Pass 3 (which is per-claim
trace to source span) and serves as a corpus-grounded sanity check that the
right cited HBAs were actually selected.

**Index discovery.** The dispatcher specifies the index via the
`RETRIEVAL_INDEX_PATH` runtime override. The value is a V2 source database
snapshot directory or a `_LATEST.md` pointer, normally
`<domain-root>/_LocalIndexes/_LATEST.md`. If omitted, the skill looks for a
domain-local `_LocalIndexes/_LATEST.md`; if neither is present the skill
records `PASS_4_SKIPPED_INDEX_UNAVAILABLE` and does not run the check.

**Staleness check.** The skill reads the snapshot `meta.json` and treats the
source database as stale if source/audit/decomposition inputs have changed
since the snapshot was built. If stale, it records
`PASS_4_SKIPPED_INDEX_STALE` and does not run.

**Procedure.** Build `claims.csv` (one row per claim sentence in the KA
draft), then invoke the query tool specified by `RETRIEVAL_QUERY_TOOL`
(default `tools/retrieval/query_source_index.py`):

```
python3 {RETRIEVAL_QUERY_TOOL} --snapshot {RETRIEVAL_INDEX_PATH} --batch claims.csv --k 5 --json
```

Per-claim verdict (judged on **source spans**, not on cosine score — cosine is a
sanity check on retrieval quality, not the audit verdict):

| Verdict | Condition |
|---|---|
| **PASS** | At least one cited HBA appears in retrieval top-5 AND the cited source span supports the claim with full qualifiers preserved (Pass-3 confirmed). |
| **WARN** | A cited HBA appears in top-5 but a higher-ranked uncited HBA also appears with cosine ≥ `RETRIEVAL_COSINE_THRESHOLD` (default `0.75`). The agent opens the uncited HBA's source span and decides whether to add the citation, demote the existing one, or note the alternative. |
| **FAIL** | No cited HBA in top-5 (retrieval doesn't even surface the cited evidence for this claim text), OR re-read of the cited source span shows the claim has lost a qualifier or scope. Resolve before run-closure. |

The cosine threshold is empirical and may be tuned per domain via
`RETRIEVAL_COSINE_THRESHOLD` based on observed false-positive / false-negative
rates after the first batch of KAs.

## SPEC-level validity

A `domain-documents` skill run is **valid** when:
- `Scoping.md` exists and contains identity, canonical schema, evidence table, artifact plan table, conflict table.
- `Scoping.md` contains Subject coverage, active authority basis, and SCA/supersession impact summary when those inputs are available.
- Each planned Knowledge Artifact file exists and includes the default section schema for its base type.
- Each planned Knowledge Artifact is comprehensive for its Knowledge Subject within the accepted source/SCA authority boundaries.
- Missing information is represented as `TBD`, not fabricated.
- `_MEMORY.md` / `MEMORY.md`, when present, was read with `_STATUS.md` and
  not used as factual authority.
- Cross-artifact consistency checks were run (Pass 2) or explicitly skipped by directive.
- Source-fidelity verification was run (Pass 3) against the authoritative source, or explicitly skipped by directive.
- `_STATUS.md` is updated only under safe-update rules (`OPEN → INITIALIZED` only when Pass 1/2 ran).

A `domain-documents` skill run is **invalid** when:
- Files are overwritten while `Current State` is outside `ALLOW_OVERWRITE_STATES`.
- `ALLOW_OVERWRITE_OVERRIDE` is used without `SCA_AUTHORIZED` or without complete SCA inputs.
- `SUPERSESSION_MAP_PATH` is provided without `AUTHORITY_MODE: SCA_DRIVEN`.
- In `SCA_DRIVEN` mode, source material overrides accepted SCA/decomposition truth.
- `_CONTEXT.md`, `_REFERENCES.md`, or `_SEMANTIC.md` are modified.
- Identity is ambiguous and not reported as `FAILED_INPUTS`.
- Content is invented rather than marked `TBD` / `ASSUMPTION`.
- No authoritative source file was read for any pass (run should have returned `FAILED_INPUTS`).
- Pass 3 ran but the source file was not actually read (source fidelity cannot be claimed without source access).
- Pass 3 corrections were applied without recording source reread evidence in the Source-Fidelity Log.
- `SEMANTIC_READY` state was introduced (not a valid DOMAIN lifecycle state).

## Failure reporting

| Condition | Report |
|---|---|
| `DECOMP_VARIANT != DOMAIN` | `RUN_STATUS=UNSUPPORTED_VARIANT` |
| `Current State` outside `ALLOW_OVERWRITE_STATES` | `RUN_STATUS=SKIPPED_PROTECT_HUMAN_WORK` + observed state |
| `SUPERSESSION_MAP_PATH` without `AUTHORITY_MODE: SCA_DRIVEN` | `RUN_STATUS=FAILED_INPUTS` |
| `ALLOW_OVERWRITE_OVERRIDE` without complete SCA authority inputs | `RUN_STATUS=FAILED_INPUTS` |
| Source file inaccessible in `SOURCE_FIDELITY` mode | `RUN_STATUS=FAILED_INPUTS` (no pass should proceed without source access) |
| Multiple KTY rows match identity | `RUN_STATUS=FAILED_INPUTS` (ambiguous identity) with evidence |
| `P3_ONLY` with no existing `KA-*.md` files | `RUN_STATUS=FAILED_INPUTS` |
| `_CONTEXT.md` missing or listed references inaccessible | Record as missing; treat content as `TBD`; do not fail |
| Decomposition CSVs missing | Best-effort; do not fail unless identity becomes ambiguous |

## Success case

A clean run reports:
- `RUN_STATUS=OK`
- `KTY_PATH` processed
- Count of Knowledge Artifacts created/updated
- `_STATUS.md` state transition (or explicit note that update was skipped)
- `AUTHORITY_MODE` used, including whether `SCA_DRIVEN` authority and `SUPERSESSION_MAP_PATH` were applied
- Passes executed (per `RUN_PASSES` directive)
- Pass 3 Source-Fidelity Log entry counts (corrections, gaps, unverified) when Pass 3 ran
- Count of Conflict Table entries awaiting human ruling (may be zero)
- No warnings (or explicit statement of any encountered)

## QA Contract summary

After completing the pass directive, the skill verifies:

| Check | Validation |
|---|---|
| Scoping exists | `Scoping.md` present |
| Artifacts exist | All artifacts listed in Scoping exist as `.md` files |
| Default sections present | All default schema headings exist in each Knowledge Artifact |
| Authoritative source read | Source file(s) referenced by `SourceSpan` were successfully accessed and read |
| Substantive claims source-grounded | Artifact content grounded in source slices, not only decomposition summaries |
| KA set comprehensive | KTY-local KA set captures the full approved Knowledge Subject scope, not merely a source summary |
| TBDs for unknowns | Missing information is `TBD`, not invented |
| Assumptions labeled | Inferred content is labeled `ASSUMPTION` |
| Sources cited | Non-trivial values/requirements cite sources (or are marked `location TBD`) |
| Decomposition not overstated | Decomposition-derived claims do not exceed what the source material supports |
| Cross-doc consistency | Identity/evidence pointers consistent, or conflicts recorded |
| Source fidelity verified (Pass 3) | Every substantive source claim compared against artifact; corrections logged in Source-Fidelity Log |
| Pass 3 source rereads evidenced | Each correction/enrichment records which source slice was re-read |
| Status update safe | `_STATUS.md` only modified per safe-update rules |
