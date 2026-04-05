# QA_CHECKS — four-documents

Invariants and quality gates for a four-documents run. These apply to the pass set executed by `RUN_PASSES` (`FULL`, `P1_P2`, or `P3_ONLY`).

## Non-negotiable invariants (all runs)

| # | Invariant | Validation |
|---|---|---|
| I1 | One deliverable per invocation | The run operated on a single `DELIVERABLE_PATH`; no cross-deliverable scanning or editing |
| I2 | All four documents exist after success | `Datasheet.md`, `Specification.md`, `Guidance.md`, `Procedure.md` all present in `{DELIVERABLE_PATH}` (for any successful pass set) |
| I3 | Stable interface | Document names unchanged; default section headings preserved (additional sections allowed) |
| I4 | Source-anchored with explicit assumptions | Non-trivial statements cite sources; inferences labeled `ASSUMPTION`; unknowns marked `TBD` |
| I5 | No human input | Run did not pause for human input; worked entirely from folder + references + decomposition |
| I6 | Respect human work | If `_STATUS.md` state NOT in `ALLOW_OVERWRITE_STATES`, run returned `SKIPPED_PROTECT_HUMAN_WORK` without overwriting docs |
| I7 | Cross-document consistency | Terminology, entity names, and values consistent across all four docs, or conflicts captured in Conflict Table |
| I8 | Metadata files unmodified | `_CONTEXT.md`, `_DEPENDENCIES.md`, `_REFERENCES.md`, `_MEMORY.md`, `_SEMANTIC.md`, `_SEMANTIC_LENSING.md` NOT modified |
| I9 | Decomposition not overstated | Decomposition-derived claims do not exceed what source material supports |
| I10 | Pass 3 source rereads evidenced | Each substantive Pass 3 change records which source slice was consulted |
| I11 | Safe `_STATUS.md` update only | `_STATUS.md` modified only under safe-update rules (`OPEN → INITIALIZED` when Pass 1/2 ran); no state regression |
| I12 | DOMAIN variant rejected | If `DECOMP_VARIANT=DOMAIN`, run returned `UNSUPPORTED_VARIANT` without modifying files |

## Default section schemas (I3 validation)

Each document MUST retain its default section headings. Additional sections are allowed; defaults may not be removed.

| Document | Default Schema Sections |
|----------|--------------------------|
| `Datasheet.md` | Identification, Attributes, Conditions, Construction, References |
| `Specification.md` | Scope, Requirements, Standards, Verification, Documentation |
| `Guidance.md` | Purpose, Principles, Considerations, Trade-offs, Examples |
| `Procedure.md` | Purpose, Prerequisites, Steps, Verification, Records |

## QA Contract (per-run checks)

After completing the pass directive, the skill verifies:

| Check | Validation |
|-------|-----------|
| Four docs exist | `Datasheet.md`, `Specification.md`, `Guidance.md`, `Procedure.md` all present |
| Default sections present | All default schema headings exist in each document |
| Authoritative source set identified | At least one locally accessible source was read from `_REFERENCES.md` |
| Substantive claims source-grounded | Non-trivial values, requirements, and rationale grounded in locally accessible authority where available |
| TBDs for unknowns | Missing information is `TBD`, not invented |
| Assumptions labeled | Inferred content is labeled `ASSUMPTION` |
| Sources cited | Non-trivial values/requirements cite sources (`SourcePath` + `SectionRef` or `location TBD`) |
| Decomposition not overstated | Decomposition-derived claims do not exceed what the source material supports |
| Cross-doc consistency | Terminology/values consistent, or conflicts captured in Conflict Table |
| Pass 3 source rereads evidenced | Each substantive Pass 3 change records which source slice was consulted |
| Status update safe | `_STATUS.md` only modified per safe-update rules |

## Conflict Table (when needed)

When contradictions cannot be resolved from available information, the skill adds a Conflict Table to `Guidance.md`:

```
## Conflict Table (for human ruling)
```

Required columns:
- `Conflict ID`
- `Conflict` (short statement)
- `Source A` (file + section)
- `Source B` (file + section)
- `Impacted sections`
- `Proposed authority` (PROPOSAL)
- `Human ruling` (TBD until decided)

The skill does NOT fill `Human ruling` — conflicts are surfaced, not silently resolved.

## Cross-document consistency checks (Pass 2 + final sweep)

| Check | What to Verify |
|-------|----------------|
| Datasheet ↔ Specification | Entities/attributes in Datasheet are reflected in requirements where appropriate |
| Specification ↔ Guidance | Requirements have rationale/considerations where appropriate |
| Specification ↔ Procedure | Requirements have verification hooks in Procedure |
| Terminology | Same terms used consistently across all four documents |
| Values | Numeric values/units consistent across documents |

When inconsistencies are not resolvable from drafts alone, the skill re-reads authoritative source slices (per Step 5 logic). When still unresolvable: prefer `TBD` or add to Conflict Table.

## Pass-specific invariants

### P1_P2 (Pass 1 + Pass 2)

| Check | Validation |
|---|---|
| Pass 1 generation ran | Four documents generated or refreshed from DOMAIN + TASK + source grounding |
| Pass 2 consistency ran | Cross-document consistency checks completed; Conflict Table added if needed |
| Step 6 skipped | Semantic lensing enrichment NOT executed |
| `_STATUS.md` updated | `OPEN → INITIALIZED` when current state is `OPEN`; skipped otherwise |

### P3_ONLY (Pass 3 only)

| Check | Validation |
|---|---|
| Preconditions met | Four docs existed before run; `_SEMANTIC_LENSING.md` existed before run |
| Candidate worklist consumed | Each warranted row in `_SEMANTIC_LENSING.md` either incorporated or converted to `TBD`/Conflict Table entry |
| Source rereads evidenced | Each substantive change records which source slice was consulted |
| Final consistency sweep ran | Step 5 consistency checks executed after Pass 3 edits |
| Pass 1 NOT re-run | Four documents not regenerated from scratch (only enriched) |
| `_STATUS.md` not modified by Pass 3 | Status update step skipped in `P3_ONLY` mode |

### FULL (Pass 1 + Pass 2 + Pass 3)

All checks from P1_P2 PLUS all P3 checks (except the `Pass 1 NOT re-run` constraint, since Pass 1 runs here by design).

If `_SEMANTIC_LENSING.md` is missing during a `FULL` run, Pass 3 is skipped, final consistency sweep runs, and the missing lensing file is reported (run still returns successfully with warning).

## Failure reporting

| `RUN_STATUS` value | Condition |
|---|---|
| `OK` | Pass set completed; all invariants satisfied; `_STATUS.md` updated when applicable |
| `WARNINGS` | Pass set completed with surfaced conflicts, missing `_SEMANTIC_LENSING.md` during `FULL`, or partial source accessibility |
| `SKIPPED_PROTECT_HUMAN_WORK` | `_STATUS.md` state NOT in `ALLOW_OVERWRITE_STATES`; no files modified |
| `FAILED_INPUTS` | Missing required inputs; `_REFERENCES.md` absent or empty; NO locally accessible references; `P3_ONLY` preconditions not met |
| `UNSUPPORTED_VARIANT` | `DECOMP_VARIANT=DOMAIN` — route to `domain-documents` skill |

The run report MUST declare exactly one `RUN_STATUS` value.

## Invalid runs

A run is invalid when any of the following hold:

- Fewer than four docs exist after a successful run.
- Content is asserted as fact without source citation or `ASSUMPTION` labeling.
- No locally accessible authoritative source was read (run should have returned `FAILED_INPUTS`).
- Pass 3 changes were applied without re-reading the implicated source slice.
- `_STATUS.md` regresses or is modified outside the safe rule.
- Metadata files other than `_STATUS.md` are modified.
- `DECOMP_VARIANT=DOMAIN` was accepted and files were modified (should have returned `UNSUPPORTED_VARIANT`).

## Evidence and logs required per run

| Artifact | Purpose |
|---|---|
| Run report (returned to invoker) | Declares `RUN_STATUS`, pass set executed, any warnings/conflicts, Pass 3 source reread evidence |
| Conflict Table (in `Guidance.md`) | Unresolved contradictions with Proposed authority (human ruling `TBD`) |
| `_STATUS.md` | State transition `OPEN → INITIALIZED` (when applicable) via `tools/scaffolding/write_status.sh` |

## Human decision rights (must remain human)

This skill may propose, but MUST NOT decide:

- Rulings on conflicts surfaced in the Conflict Table.
- Overriding `_STATUS.md` protection (the operator adjusts `ALLOW_OVERWRITE_STATES` if intentional).
- Resolving source-vs-decomposition disagreements by elevating decomposition above source.
- Scope boundary decisions beyond what `_CONTEXT.md` and accessible sources support.

Human rulings are recorded in the Conflict Table or returned to the invoker for upstream resolution.
