# dependency-extract — QA Checks

This file enumerates the mandatory invariants and local quality checks that must hold for a `dependency-extract` run to be considered valid. These are migrated verbatim from `AGENT_DEPENDENCIES.md` Non-negotiable invariants, PROTOCOL Function 5 (local quality checks), and SPEC validity requirements.

## Non-negotiable invariants (migrated from source agent)

1. **Evidence-first.** Each dependency row must cite at least one concrete evidence location (`EvidenceFile` + `SourceRef`) or explicitly state `location TBD`.
2. **Do not modify source documents.** Never edit deliverable docs, `_REFERENCES.md`, or decomposition outputs.
3. **Writes limited to dependency artifacts only:** `{deliverable}/_DEPENDENCIES.md` and `{deliverable}/Dependencies.csv`.
4. **No invention.** If the target cannot be resolved confidently, record `TargetType=UNKNOWN` and preserve the raw reference text.
5. **No hierarchy discovery.** This skill does not create or restructure the decomposition Tree; it only anchors to identifiers that already exist.
6. **Straight-through.** No human decisions required mid-run; defaults are conservative and logged.
7. **Non-destructive updates.** Do not delete rows; retire extracted rows when no longer seen.
8. **Epistemic separation.** Distinguish FACT vs ASSUMPTION vs PROPOSAL in `Notes`.
9. **Schema discipline.** `Dependencies.csv` must remain parseable and include all 29 canonical required columns.
10. **Enum normalization on write.** Normalize legacy variants to canonical enums.
11. **Lifecycle hygiene.** Track both extraction lifecycle (`FirstSeen`/`LastSeen`/`Status`) and closure lifecycle (`RequiredMaturity`/`ProposedMaturity`/`SatisfactionStatus`).
12. **Referential integrity.** `FromDeliverableID` must match the current deliverable; preserve unresolved targets as `UNKNOWN`/`TBD` rather than guessing.
13. **Information flow only.** Do not create edges that are merely "coordination" or "structural adjacency."

## Mandatory local quality checks (from PROTOCOL Function 5)

### Schema validation

- Run: `python3 tools/validation/validate_dependencies_schema.py {deliverable_folder}/Dependencies.csv`
  - Confirms all 29 required v3.1 columns are present and CSV is parseable.
- `DependencyID` is present and unique within the file.

### Enum validation

- Validate enum fields on write using `python3 tools/validation/validate_enum.py`:
  - `DEPENDENCY_CLASS`, `ANCHOR_TYPE`, `DIRECTION`, `DEPENDENCY_TYPE`, `TARGET_TYPE`, `EXPLICITNESS`, `CONFIDENCE`, `ORIGIN`, `STATUS`, `SATISFACTION_STATUS`
- Normalize legacy values: `INBOUND` -> `UPSTREAM`, `OUTBOUND` -> `DOWNSTREAM` on write.

### ID format validation

- Validate all ID fields: `tools/validation/validate_id_format.sh DEL {FromDeliverableID}`, `tools/validation/validate_id_format.sh PKG {FromPackageID}`, etc.

### Evidence & provenance checks

- ACTIVE rows contain `EvidenceFile` and `SourceRef` (or explicit `location TBD`).
- `_DEPENDENCIES.md` counts do not contradict `Dependencies.csv`.
- Obvious duplicate extracted rows are merged or explicitly justified in `Notes`.

### Tree x DAG integrity checks

- **Parent anchor check:**
  - Count rows where `Status=ACTIVE`, `DependencyClass=ANCHOR`, `AnchorType=IMPLEMENTS_NODE`.
  - If count == 0: add `[WARNING] FLOATING_NODE: No parent anchor (IMPLEMENTS_NODE) found.` to Run Notes.
  - If count > 1: add `[WARNING] AMBIGUOUS_ANCHOR: Multiple parent anchors found.` to Run Notes.

## Validity requirements (from source agent SPEC)

A `dependency-extract` run is valid when all of the following hold:

- Source documents in scope are not modified.
- `Dependencies.csv` exists (created if missing) and is parseable.
- Required columns are present (including `DependencyClass`, `AnchorType`, `TargetRefID`).
- Every ACTIVE row includes `EvidenceFile` and `SourceRef` (or `location TBD`).
- Targets are not invented (`UNKNOWN` permitted).
- Updates are non-destructive (no row deletions).
- `DependencyID` values are unique within each deliverable register.
- Write-form enums are canonical (legacy values normalized).
- `_DEPENDENCIES.md` summary/lifecycle counts are consistent with `Dependencies.csv`.
- If decomposition cannot be located, `_DEPENDENCIES.md` Run Notes include `[WARNING] MISSING_DECOMPOSITION` and anchor validation/label resolution is explicitly marked degraded.

## Non-fatal integrity warnings (required)

The following warnings MUST be emitted to `_DEPENDENCIES.md` Run Notes when conditions are met (they do not fail the run):

- **`[WARNING] FLOATING_NODE`** — no ACTIVE parent anchor (zero rows with `Status=ACTIVE`, `DependencyClass=ANCHOR`, `AnchorType=IMPLEMENTS_NODE`).
- **`[WARNING] AMBIGUOUS_ANCHOR`** — multiple ACTIVE parent anchors (more than one row with the same classification).
- **`[WARNING] MISSING_DECOMPOSITION`** — decomposition document could not be located; anchor validation/label resolution is degraded.

## Failure-reporting expectations

If checks fail and cannot be auto-repaired conservatively:
- Keep files non-destructively updated.
- Add explicit issues to `_DEPENDENCIES.md` Run Notes.
- Set uncertain fields to `TBD`/`UNKNOWN` rather than inventing values.

## Schema-freeze reminder (Dependencies.csv v3.1)

The 29 required columns are fixed by the v3.1 schema and must appear in `Dependencies.csv` (order enforced by `validate_dependencies_schema.py`):

`RegisterSchemaVersion`, `DependencyID`, `FromPackageID`, `FromDeliverableID`, `FromDeliverableName`, `DependencyClass`, `AnchorType`, `Direction`, `DependencyType`, `TargetType`, `TargetPackageID`, `TargetDeliverableID`, `TargetRefID`, `TargetName`, `TargetLocation`, `Statement`, `EvidenceFile`, `SourceRef`, `EvidenceQuote`, `Explicitness`, `RequiredMaturity`, `ProposedMaturity`, `SatisfactionStatus`, `Confidence`, `Origin`, `FirstSeen`, `LastSeen`, `Status`, `Notes`

Extension columns `EstimateImpactClass` and `ConsumerHint` are optional (non-breaking); populating them is required only when `CONSUMER_CONTEXT=TASK_ESTIMATING` and evidence supports the values.
