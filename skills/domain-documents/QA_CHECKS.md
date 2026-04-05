# domain-documents — QA Checks

Minimum checks for a valid run and the non-negotiable invariants preserved from the source agent.

## Non-negotiable invariants

These invariants MUST hold for every run. Violating any of them makes the run invalid.

| Invariant | Requirement |
|---|---|
| **DOMAIN pipeline only** | `DECOMP_VARIANT` must be `DOMAIN`; otherwise halt with `UNSUPPORTED_VARIANT`. This skill is not called by PROJECT or SOFTWARE variants |
| **Variable Knowledge Artifact schema** | Artifact count and names derive from `KnowledgeSubjects` in the decomposition. No fixed 4-doc kit |
| **Subject-to-Artifact bijection** | Each Knowledge Subject maps to exactly one Knowledge Artifact file. No splitting or merging |
| **KA-* naming convention** | Default `KA-01_{Type}__{Slug}.md`; configurable via `ARTIFACT_NAMING`. Stable ordinal prefix when `PREFIXED_*` |
| **One deliverable per run** | Each invocation processes exactly one Knowledge Type folder (`KTY_PATH`). No cross-Knowledge-Type scanning |
| **No human input** | The skill works from folder contents, references, and decomposition. Human interacts with ORCHESTRATOR/WORKING_ITEMS, not this skill |
| **Respect human work** | `_STATUS.md` `Current State` must be within `ALLOW_OVERWRITE_STATES` (default `OPEN, INITIALIZED`) before any overwrite. Halt with `SKIPPED_PROTECT_HUMAN_WORK` otherwise |
| **No metadata modification** | Never modify `_CONTEXT.md`, `_REFERENCES.md`, `_MEMORY.md`/`MEMORY.md`, or `_SEMANTIC.md` |
| **No invention** | Missing information marked `TBD`; inferences labeled `ASSUMPTION`. Do not fabricate source excerpts when source is inaccessible |
| **Authoritative source required** | All passes require the source file(s) bounded by `SourceSpan` to be accessible. Halt with `FAILED_INPUTS` if source cannot be read |
| **Source fidelity is the quality gate** | Pass 3 verifies artifact-to-source fidelity. No semantic lensing / semantic enrichment is used in the DOMAIN pipeline |
| **Safe-update status only** | `_STATUS.md` transitions `OPEN → INITIALIZED` only when Pass 1/2 ran. Never regress state |
| **No SEMANTIC_READY state** | DOMAIN lifecycle is `OPEN → INITIALIZED → IN_PROGRESS`; `SEMANTIC_READY` is NOT a valid DOMAIN state |

## Structural checks (Pass 1)

| Check | Validation |
|---|---|
| Scoping exists | `Scoping.md` present in `{KTY_PATH}` |
| Scoping identity | Contains KTY identity, Category, CanonicalSchema, intended users, when-used context |
| Evidence set table | Table present with UnitID → AtomicStatement → SourceRef columns |
| Artifact plan table | Table present with ArtifactID → SubjectID → SubjectName → BaseType → AddOns → Filename |
| Conflict Table | Present with stable schema (Conflict ID, Conflict, Source A, Source B, Impacted artifacts, Proposed authority, Human ruling) |
| Artifacts created | Every artifact listed in the plan table exists as a `.md` file in `{KTY_PATH}` |
| Default sections present | Each Knowledge Artifact contains all default schema sections for its base type (Reference/Guidance/Checklist/Procedure) |
| Metadata block present | Each `KA-*.md` has an Artifact Metadata block with Knowledge Type, Category, Knowledge Subject, Artifact ID, Base Type, Add-ons, Evidence Units |
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
| Source file accessed | Source file(s) bounded by `SourceSpan` successfully read for this KTY |
| Coverage verified | Every substantive source statement compared against artifact content |
| Accuracy verified | Every non-TBD, non-ASSUMPTION artifact claim traced to a specific source location |
| Corrections logged | Each artifact correction recorded in `Scoping.md` `## Source-Fidelity Log` section |
| Gaps logged | Source content not captured in any artifact recorded as a gap with source location |
| Unverified flagged | Claims not traceable to source marked `UNVERIFIED` or downgraded to `ASSUMPTION` |
| Source reread evidence | Each correction/enrichment records which source slice was re-read before the change was applied |
| Structural sweep re-run | After corrections, Pass 2 structural completeness checks (items 1–3) re-verified |

## SPEC-level validity

A DOMAIN_DOCUMENTS run is **valid** when:
- `Scoping.md` exists and contains identity, canonical schema, evidence table, artifact plan table, conflict table.
- Each planned Knowledge Artifact file exists and includes the default section schema for its base type.
- Missing information is represented as `TBD`, not fabricated.
- Cross-artifact consistency checks were run (Pass 2) or explicitly skipped by directive.
- Source-fidelity verification was run (Pass 3) against the authoritative source, or explicitly skipped by directive.
- `_STATUS.md` is updated only under safe-update rules (`OPEN → INITIALIZED` only when Pass 1/2 ran).

A DOMAIN_DOCUMENTS run is **invalid** when:
- Files are overwritten while `Current State` is outside `ALLOW_OVERWRITE_STATES`.
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
| Source file inaccessible | `RUN_STATUS=FAILED_INPUTS` (no pass should proceed without source access) |
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
| TBDs for unknowns | Missing information is `TBD`, not invented |
| Assumptions labeled | Inferred content is labeled `ASSUMPTION` |
| Sources cited | Non-trivial values/requirements cite sources (or are marked `location TBD`) |
| Decomposition not overstated | Decomposition-derived claims do not exceed what the source material supports |
| Cross-doc consistency | Identity/evidence pointers consistent, or conflicts recorded |
| Source fidelity verified (Pass 3) | Every substantive source claim compared against artifact; corrections logged in Source-Fidelity Log |
| Pass 3 source rereads evidenced | Each correction/enrichment records which source slice was re-read |
| Status update safe | `_STATUS.md` only modified per safe-update rules |
