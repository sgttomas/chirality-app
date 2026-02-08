# AUDIT_DEPENDENCIES.md — Rubric for Auditing Dependency Registers

This rubric is used by **AUDIT_DEPENDENCIES (Type 2)** to audit deliverable-local dependency artifacts:
- `{deliverable}/Dependencies.csv`
- `{deliverable}/_DEPENDENCIES.md`

## Severity Levels (use consistently)

- `BLOCKER`: register cannot be safely consumed (missing/invalid CSV, missing critical columns, non-unique IDs, pervasive missing evidence).
- `HIGH`: likely to cause incorrect downstream planning/reconciliation (bad enums, broken referential integrity, anchor ID misuse).
- `MED`: quality gaps that increase rework (duplicates, weak evidence, inconsistent summaries).
- `LOW`: polish/clarity (formatting variance, minor note gaps).

## Checks (apply per deliverable)

### D1 — Artifact Presence

- `Dependencies.csv` exists.
- `_DEPENDENCIES.md` exists.

Severity:
- Missing `Dependencies.csv`: `BLOCKER`
- Missing `_DEPENDENCIES.md`: `MED` (unless the project requires it always, then `HIGH`)

### D2 — CSV Parseability

- CSV is parseable with a standard comma delimiter.
- Header row exists and column names are unique.

Severity:
- Unparseable CSV: `BLOCKER`

### D3 — Required Columns (by detected schema)

Schema detection (best-effort):
- If `RegisterSchemaVersion` exists, use it.
- Else if columns include `DependencyClass` and `AnchorType`, treat as “v3-like”.
- Else treat as “v2-like”.

Required minimum (all schemas):
- `DependencyID`, `FromPackageID`, `FromDeliverableID`, `Direction`, `DependencyType`, `TargetType`, `Statement`, `EvidenceFile`, `SourceRef`, `SatisfactionStatus`, `FirstSeen`, `LastSeen`, `Status`, `Origin`, `Notes`

Additional required for v3-like schemas:
- `DependencyClass`, `AnchorType`, `TargetRefID`

Severity:
- Missing `DependencyID` or `Status`: `BLOCKER`
- Missing v3-only columns in v3-like file: `HIGH`

### D4 — ID Hygiene

- `DependencyID` present for every row.
- `DependencyID` values unique within the file.
- `FromDeliverableID` consistent across rows (matches the host deliverable identity when known).

Severity:
- Non-unique `DependencyID`: `BLOCKER`
- Mixed `FromDeliverableID`: `HIGH`

### D5 — Enum Validity (Write-Form)

Validate (where present):
- `Direction`: `UPSTREAM|DOWNSTREAM`
- `Status`: `ACTIVE|RETIRED`
- `Origin`: `DECLARED|EXTRACTED`
- `Explicitness`: `EXPLICIT|IMPLICIT`
- `Confidence`: `HIGH|MEDIUM|LOW`
- `SatisfactionStatus`: `TBD|PENDING|IN_PROGRESS|SATISFIED|WAIVED|NOT_APPLICABLE`

Severity:
- Non-canonical enums on ACTIVE rows: `HIGH` (unless explicitly marked legacy and normalized guidance exists)

### D6 — Evidence Completeness (ACTIVE rows)

For `Status=ACTIVE` rows:
- `EvidenceFile` present.
- `SourceRef` present (or explicit `location TBD`).

Severity:
- Missing evidence on ACTIVE rows: `HIGH`

### D7 — Target ID Placement (v3-like schemas)

Rules:
- `TargetDeliverableID` MUST be reserved for `TargetType=DELIVERABLE` and must match the project’s deliverable ID format (typically `DEL-###`).
- For `TargetType=WBS_NODE` / `REQUIREMENT` (and similar non-deliverable stable IDs), use `TargetRefID`. `TargetDeliverableID` MUST be empty.

Severity:
- Non-DEL ID in `TargetDeliverableID` on anchor rows: `HIGH`

### D8 — Anchor Integrity (v3-like schemas)

Checks:
- For `DependencyClass=ANCHOR` rows:
  - `Direction=UPSTREAM`
  - `DependencyType=OTHER`
  - `AnchorType != NOT_APPLICABLE`
- For `DependencyClass=EXECUTION` rows:
  - `AnchorType=NOT_APPLICABLE`

Warnings:
- `FLOATING_NODE`: no ACTIVE parent anchor (`ANCHOR + IMPLEMENTS_NODE`).
- `AMBIGUOUS_ANCHOR`: multiple ACTIVE parent anchors.

Severity:
- Schema-invalid anchor fields: `HIGH`
- Floating/ambiguous anchors: `MED` (unless the project requires strict anchoring, then `HIGH`)

### D9 — Lifecycle Hygiene

- `FirstSeen` and `LastSeen` present.
- `FirstSeen <= LastSeen` (lexicographic ISO timestamps or consistent date format).
- Rows are retired, not deleted (best-effort check when historical context exists).

Severity:
- Missing lifecycle fields: `MED` (or `HIGH` if required by consumer)

### D10 — Duplicate/Conflict Detection

Flag as issues (do not rewrite registers):
- Duplicate semantics (same target + type + direction + statement, different IDs).
- Contradictory closure (`SATISFIED` and `PENDING` duplicates for same edge).

Severity:
- Contradictory closure states: `HIGH`
- Duplicates without contradiction: `MED`

## Issue Log Schema (recommended)

`Dependency_Audit_IssueLog.csv` columns:
- `IssueID`
- `Severity`
- `DeliverablePath`
- `FromDeliverableID`
- `DependencyID` (blank if file-level issue)
- `File`
- `Field`
- `Symptom`
- `Evidence`
- `RecommendedFix`

