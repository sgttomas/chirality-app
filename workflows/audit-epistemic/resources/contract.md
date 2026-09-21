# audit-epistemic — contract

## Mission

Given one or more deliverable folders, audit the epistemic state of the
production contract selected by the accepted basis (`SOW_V1` or transitional
`LEGACY_FOUR_DOC`) and `Dependencies.csv` against the
epistemic ontology in `TYPES.md` §10.

In an exactly authorized isolated `MIGRATION_DUAL` workspace, audit the
candidate `ScopeOfWork.md` and verify the four source documents for parity.
Missing, partial, invalid, ambiguous, and unauthorized dual states fail closed.

Produce:
- an epistemic audit report with findings across seven audit passes,
- a structured issue log with per-claim findings,
- a machine-readable JSON summary with aggregate metrics,
- a self-assessment of audit coverage and limitations.

The goal is to make the epistemic state of a deliverable's claims **visible and actionable** so that a licensed professional can determine what to rely on.

---

## Non-negotiable invariants

- **Read-only on deliverables.** Never modify any deliverable file (document kit, Dependencies.csv, metadata files).
- **Evidence-first.** Every finding MUST cite the specific file, section or line, and claim text that triggered it. Findings without evidence are invalid.
- **No invention (K-INVENT-1).** If the agent cannot determine epistemic status, mark as `INDETERMINATE` and continue. Do not guess epistemic labels or warrant states.
- **Mandatory provenance standard (K-PROV-1).** The audit itself enforces provenance requirements — every claim labeled FACT must have a source citation, or the absence is a finding.
- **Conflict surfacing (K-CONFLICT-1).** Cross-document inconsistencies MUST be surfaced as findings, not silently ignored.
- **Epistemic ontology authority.** The six epistemic primitives (Claim, Warrant, Status, Gap, Conflict, Ruling) as defined in `TYPES.md` §10 are the authoritative vocabulary. Do not introduce alternative terminology.
- **Deterministic.** Keep the inventory and metric rules reproducible; record the evidence and limits of semantic judgments.
- **Immutable snapshots (K-SNAP-1).** Each run writes a new snapshot folder; never overwrite prior snapshots.
- **Pointer-only overwrite allowed.** `_LATEST.md` may be overwritten as a pointer; snapshots remain immutable.
- **Scope-bounded.** Audit only deliverables explicitly named in the brief. Do not expand scope.

---

## Inputs (brief schema)

```
PURPOSE: Epistemic audit of deliverable content against TYPES.md §10
SCOPE: <list of deliverable IDs or paths>
EXECUTION_ROOT: <default execution/>
RUN_LABEL: <short label for this run; default EPISTEMIC>
REQUESTED_BY: <invoking agent name; default WORKING_ITEMS>
CONFIG:
  - AUDIT_DEPTH: STANDARD | DEEP
    (STANDARD: structural checks — label presence, provenance fields, TBD markers, parameter consistency)
    (DEEP: adds semantic claim extraction — attempts to identify unlabeled non-trivial claims in prose)
  - INCLUDE_DEPENDENCIES_CSV: true | false (default true)
  - SEVERITY_THRESHOLD: ALL | WARNING | BLOCKER (minimum severity to include in issue log; default ALL)
CONSTRAINTS:
  - Read-only on deliverable files
  - Epistemic ontology per TYPES.md §10
EXCLUSIONS:
  - <paths/patterns to exclude; default none>
NOTES:
  - <additional context>
```

If `SCOPE` is missing or empty: write `Brief.md` with `RUN_STATUS = FAILED_INPUTS` and return.

If a deliverable in scope has neither a complete legacy kit nor a validated
SOW production contract, record `NOT_INITIALIZED` in coverage
and skip epistemic analysis. Partial or unauthorized dual formats are
`INVALID`, not `NOT_INITIALIZED`.

---

## Outputs (write zone)

Tool root: `{EXECUTION_ROOT}/_Evaluation/EpistemicAudit/`

Each run writes a new immutable snapshot folder:

```
{EXECUTION_ROOT}/_Evaluation/EpistemicAudit/
  _Archive/
  _LATEST.md
  EpistemicAudit_{DEL-ID}_{YYYY-MM-DD}_{HHmm}/
    Brief.md
    Epistemic_Audit_Report.md
    Epistemic_Audit_IssueLog.csv
    epistemic_audit_summary.json
    QA_Report.md
```

When scope includes multiple deliverables, `{DEL-ID}` in the snapshot folder name is replaced with the `{RUN_LABEL}` (e.g., `EpistemicAudit_EPISTEMIC_2026-03-29_1430/`).

Pointer (overwrite allowed; pointer only):
- `{EXECUTION_ROOT}/_Evaluation/EpistemicAudit/_LATEST.md` -> snapshot folder name

---

## Validity

A run is valid when:

- Outputs are written to a new immutable snapshot folder under `{EXECUTION_ROOT}/_Evaluation/EpistemicAudit/`.
- `Brief.md`, `Epistemic_Audit_Report.md`, `Epistemic_Audit_IssueLog.csv`, `epistemic_audit_summary.json`, and `QA_Report.md` all exist in the snapshot.
- The report includes findings for all seven audit passes (or marks passes as `INCOMPLETE` or `SKIPPED` with reasons).
- Every finding in the issue log includes evidence: file path, section or line reference, and claim text.
- No deliverable file is modified.
- The `epistemic_audit_summary.json` includes at minimum: `labelCoveragePercent`, `provenanceCompletenessPercent`, `gapCount`, `conflictCount`, `warrantStateDistribution` (counts per state), `deliverablesCovered`, `passesCompleted`.
- Findings reference the correct epistemic primitives from `TYPES.md` §10 (Claim, Warrant, Status, Gap, Conflict, Ruling).
- Warrant state classifications use only the four canonical states: UNWARRANTED, CITED, REVIEWED, AUTHENTICATED.
- Epistemic labels use only the four canonical labels: FACT, ASSUMPTION, PROPOSAL, TBD.

A run is **invalid** when:
- Any deliverable file is modified.
- Findings are asserted without evidence (file + location + claim text).
- Epistemic labels or warrant states are invented outside the canonical vocabulary.
- The snapshot overwrites a prior snapshot.

---

## Artifacts and schemas

### Tool-root layout

```
{EXECUTION_ROOT}/_Evaluation/EpistemicAudit/
  _Archive/
  _LATEST.md
  EpistemicAudit_{DEL-ID|RUN_LABEL}_{YYYY-MM-DD}_{HHmm}/
    Brief.md
    Epistemic_Audit_Report.md
    Epistemic_Audit_IssueLog.csv
    epistemic_audit_summary.json
    QA_Report.md
```

### INIT-TASK Brief format

```markdown
# Epistemic Audit Brief

**Run label:** {RUN_LABEL}
**Requested by:** {REQUESTED_BY}
**Date:** {YYYY-MM-DD}
**Execution root:** {EXECUTION_ROOT}

## Scope
- {DEL-ID_1}: {path_1}
- {DEL-ID_2}: {path_2}
- ...

## Configuration
- AUDIT_DEPTH: {STANDARD|DEEP}
- INCLUDE_DEPENDENCIES_CSV: {true|false}
- SEVERITY_THRESHOLD: {ALL|WARNING|BLOCKER}

## Exclusions
- {exclusion patterns, if any}

## Notes
- {additional context}
```

### Epistemic_Audit_Report.md structure

```markdown
# Epistemic Audit Report

**Deliverable(s):** {DEL-IDs}
**Run label:** {RUN_LABEL}
**Date:** {YYYY-MM-DD HH:mm}
**Audit depth:** {STANDARD|DEEP}

## Executive Summary
- Label coverage: {X}%
- Provenance completeness: {X}%
- Gaps identified: {N}
- Conflicts detected: {N}
- Warrant state: {N} UNWARRANTED / {N} CITED / {N} REVIEWED / {N} AUTHENTICATED

## Pass 1 — Epistemic Label Coverage
{Per-document and aggregate findings}

## Pass 2 — Provenance Verification
{Per-label-category findings}

## Pass 3 — Gap Detection
{Explicit gaps and potential unwarranted claims}

## Pass 4 — Conflict Detection
{Cross-document parameter/value conflicts}

## Pass 5 — Warrant Lifecycle Assessment
{Warrant state distribution and critical-section analysis}

## Pass 6 — Cross-Document Consistency
{Scope, parameter, criteria, and intent alignment findings}

## Pass 7 — Dependencies.csv Provenance Audit
{Provenance completeness for dependency register}

## Recommendations
{Prioritized actions to improve epistemic state}
```

### Epistemic_Audit_IssueLog.csv schema

| Column | Type | Description |
|--------|------|-------------|
| `IssueID` | string | Unique within the run (e.g., `EA-001`) |
| `Category` | enum | `LABEL_COVERAGE`, `PROVENANCE`, `GAP`, `CONFLICT`, `WARRANT_STATE`, `CONSISTENCY`, `DEP_PROVENANCE` |
| `Severity` | enum | `BLOCKER`, `WARNING`, `INFO` |
| `ClaimText` | string | The claim or value in question (max 50 words) |
| `File` | string | Source file path (relative to deliverable) |
| `Section` | string | Section heading or line reference |
| `EpistemicStatus` | enum | `FACT`, `ASSUMPTION`, `PROPOSAL`, `TBD`, `UNLABELED`, `N/A` |
| `WarrantState` | enum or empty | `UNWARRANTED`, `CITED`, `REVIEWED`, `AUTHENTICATED`; empty when assessment is indeterminate |
| `AuditAssessment` | enum | `DETERMINATE`, `INDETERMINATE`; assessment status is separate from warrant state |
| `Recommendation` | string | Specific action to resolve the issue |

### epistemic_audit_summary.json schema

```json
{
  "runLabel": "string",
  "date": "YYYY-MM-DD",
  "deliverablesInScope": ["DEL-XX-YY"],
  "deliverablesCovered": 0,
  "passesCompleted": [],
  "labelCoveragePercent": 0.0,
  "provenanceCompletenessPercent": 0.0,
  "gapCount": 0,
  "conflictCount": 0,
  "indeterminateAssessments": 0,
  "warrantStateDistribution": {
    "UNWARRANTED": 0,
    "CITED": 0,
    "REVIEWED": 0,
    "AUTHENTICATED": 0
  },
  "depProvenanceCompletenessPercent": 0.0,
  "issueCountBySeverity": {
    "BLOCKER": 0,
    "WARNING": 0,
    "INFO": 0
  },
  "issueCountByCategory": {
    "LABEL_COVERAGE": 0,
    "PROVENANCE": 0,
    "GAP": 0,
    "CONFLICT": 0,
    "WARRANT_STATE": 0,
    "CONSISTENCY": 0,
    "DEP_PROVENANCE": 0
  }
}
```

### QA_Report.md structure

```markdown
# QA Report — Epistemic Audit

## Audit Coverage
- Deliverables in scope: {N}
- Deliverables analyzed: {N}
- Deliverables skipped (NOT_INITIALIZED): {N}
- Documents scanned: {N}
- Dependencies.csv files analyzed: {N}

## Passes Completed
- Pass 1 (Label Coverage): {COMPLETE|INCOMPLETE|SKIPPED} — {reason if not COMPLETE}
- Pass 2 (Provenance): {COMPLETE|INCOMPLETE|SKIPPED}
- Pass 3 (Gap Detection): {COMPLETE|INCOMPLETE|SKIPPED}
- Pass 4 (Conflict Detection): {COMPLETE|INCOMPLETE|SKIPPED}
- Pass 5 (Warrant State): {COMPLETE|INCOMPLETE|SKIPPED}
- Pass 6 (Cross-Document Consistency): {COMPLETE|INCOMPLETE|SKIPPED}
- Pass 7 (Dep Provenance): {COMPLETE|INCOMPLETE|SKIPPED}

## Limitations
- {Known limitations of this audit run}
- {Claims that could not be assessed and why}
- {Areas where AUDIT_DEPTH=DEEP would improve coverage}

## Methodology Notes
- {Claim identification heuristics used}
- {How non-trivial claims were distinguished from boilerplate}
- {Any assumptions made during the audit}
```

---
