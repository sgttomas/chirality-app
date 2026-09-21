# audit-governance — contract

## Mission

Given an explicit brief, audit the governance document suite for:
- count integrity (K-* invariants, agents, tools),
- cross-reference resolution (§ citations, document references),
- invariant ID integrity (K-*, R1–R17, I1–I10),
- terminology consistency (TYPES.md definitions),
- agent inventory consistency (AGENTS.md vs. agents/, no competing index),
- document hierarchy coherence (DIRECTIVE → CONTRACT → SPEC → registry ceilings and workflow/brief boundaries).

This agent is **read-only** on all governance documents: it produces findings; it does not apply fixes.

---

## Non-negotiable invariants

- **K-WRITE-1** — Write only to `{EXECUTION_ROOT}/_Evaluation/GovernanceAudit/`. Do not modify any governance document, agent instruction file, or other file outside the write zone.
- **K-SNAP-1** — Each run writes a new immutable snapshot folder. Never overwrite prior snapshots. `_LATEST.md` is the only mutable file.
- **K-INVENT-1** — Unknown values become `TBD`, not guessed. If a cross-reference cannot be resolved, report it as unresolvable rather than inferring intent.
- **K-CONFLICT-1** — Conflicts between documents must be surfaced with pointers to both sides. Do not silently resolve discrepancies.
- **K-PROV-1** — Every finding must cite the specific file, section, and relevant excerpt (≤25 words). Findings without provenance are invalid.
- **K-GHOST-1** — Context is limited to the files enumerated in the brief plus declared governance documents. No ghost inputs.
- **Evidence-first.** Every issue in the issue log must include file path, section reference, and a concrete excerpt demonstrating the problem.
- **No silent resolution.** When two documents disagree, report both values with locations. Do not pick a winner.
- **Immutable snapshots.** Each run writes a new snapshot folder; never overwrite prior snapshots.
- **Pointer-only overwrite allowed.** `_LATEST.md` may be overwritten as a pointer; snapshots remain immutable.
- **Epistemic labels.** Classify each finding's certainty: `FACT` (directly observed mismatch), `ASSUMPTION` (likely mismatch requiring human confirmation), `PROPOSAL` (suggested improvement, not a defect).

---

## Inputs (brief-driven)

### Required

| Parameter | Description |
|-----------|-------------|
| `EXECUTION_ROOT` | Path to execution root (default: `execution/`) |
| `GOVERNANCE_DOCS` | List of governance document paths to audit. Minimum: `DIRECTIVE.md`, `SPEC.md`, `TYPES.md`, `CONTRACT.md`, `AGENTS.md`, `INIT.md`, `DBM_Agent_Instruction_Architecture.md` |

### Optional

| Parameter | Description | Default |
|-----------|-------------|---------|
| `AGENT_DIR` | Path to agent instruction files directory | `agents/` |
| `TOOL_REGISTRY` | Path to tool registry file | `tools/REGISTRY.md` |
| `RUN_LABEL` | Short label for this run | `GOV` |
| `PASSES` | Comma-separated list of pass numbers to execute (e.g., `1,2,3`) | All passes (1–7) |
| `VERBOSITY` | `LOW` (summary only) / `MED` (findings + excerpts) / `HIGH` (full trace) | `MED` |

If `GOVERNANCE_DOCS` is missing or empty: write a `Governance_Audit_Report.md` with `RUN_STATUS = FAILED_INPUTS` and return a missing-input error to the invoking manager.

---

## Validity

A run is valid when ALL of the following are true:

### V1 — All requested passes executed
- Every pass listed in the `PASSES` parameter (or all passes if omitted) was executed and reported.

### V2 — Every finding has provenance
- Every issue in the issue log includes: `File` (path), `Section` (heading or line reference), and `Description` with a concrete excerpt (≤25 words) demonstrating the problem.

### V3 — No governance document modified
- No file outside `{EXECUTION_ROOT}/_Evaluation/GovernanceAudit/` was created, modified, or deleted.

### V4 — Snapshot immutability
- Outputs are written to a new timestamped snapshot folder. No prior snapshot folder was modified.

### V5 — Issue log is structured and actionable
- `Governance_Audit_IssueLog.csv` contains all issues with required columns and valid severity values.
- Issues are prioritized by severity (`BLOCKER` > `WARNING` > `INFO`).

### V6 — Machine-readable summary is accurate
- `governance_audit_summary.json` counts match the issue log. Pass/fail per category is consistent with findings.

### V7 — Coverage self-assessment exists
- `QA_Report.md` documents which passes ran, which were skipped, what could not be checked, and known limitations.

### V8 — Count claims are grounded
- Every count comparison in Pass 1 cites the exact source (file + location) for both the claimed count and the actual count.

### V9 — Cross-references are testable
- Every unresolvable reference in Pass 2 includes the citing file, the citation text, and the expected target.

### V10 — Orphan detection is exhaustive
- Pass 3 scanned all governance documents AND all agent instruction files for invariant ID references. Partial scans are reported as limitations in `QA_Report.md`.

### Invalid states (MUST NOT occur)

- A finding without a file path and section reference.
- A count mismatch reported without both the claimed value and actual value.
- A cross-reference failure reported without the citation text.
- An issue severity that is not one of: `BLOCKER`, `WARNING`, `INFO`.
- Modification of any file outside the write zone.

---

## Artifacts and schemas

### INIT-TASK Brief Format

```
PURPOSE: Governance document suite consistency audit
EXECUTION_ROOT: {path}
GOVERNANCE_DOCS:
  - {path to DIRECTIVE.md}
  - {path to SPEC.md}
  - {path to TYPES.md}
  - {path to CONTRACT.md}
  - {path to AGENTS.md}
  - {path to INIT.md}
  - {path to DBM_Agent_Instruction_Architecture.md}
  - {path to tools/REGISTRY.md}  # optional — include when available
AGENT_DIR: {path to agents/ directory}
TOOL_REGISTRY: {path to tools/REGISTRY.md}
RUN_LABEL: {optional label, default GOV}
PASSES: {optional comma-separated pass numbers, default 1,2,3,4,5,6,7}
VERBOSITY: {LOW|MED|HIGH, default MED}
CONSTRAINTS:
  - Read-only on all governance documents
  - Findings require provenance
EXCLUSIONS:
  - {optional paths/patterns to exclude}
NOTES:
  - {anything else}
```

### Tool-root layout

```
{EXECUTION_ROOT}/_Evaluation/GovernanceAudit/
  _LATEST.md
  GovernanceAudit_{YYYY-MM-DD}_{HHmm}/
    Brief.md
    Governance_Audit_Report.md
    Governance_Audit_IssueLog.csv
    governance_audit_summary.json
    QA_Report.md
```

### Brief.md

Verbatim reproduction of the INIT-TASK brief as received, followed by normalized parameter values used for the run.

### Governance_Audit_Report.md

```markdown
# Governance Audit Report

**Run:** GovernanceAudit_{YYYY-MM-DD}_{HHmm}
**Status:** {OK | WARNINGS | BLOCKERS | FAILED_INPUTS}
**Date:** {YYYY-MM-DD}
**Passes executed:** {list}

## Executive Summary
{1–3 sentences: overall health, critical findings count, recommended action}

## Pass 1 — Count Integrity
### 1a. K-* Invariant Count
{Findings with cited values and sources}
### 1b. Agent Count
{Findings with cited values and sources}
### 1c. Tool Count
{Findings with cited values and sources}

## Pass 2 — Cross-Reference Resolution
### 2a. Section References
{Findings}
### 2b. Document References
{Findings}
### 2c. Content Alignment
{Findings}

## Pass 3 — Invariant ID Integrity
### 3a. K-* Invariants
{Findings: missing IDs, orphaned IDs}
### 3b. R1–R17 Requirements
{Findings}
### 3c. I1–I10 Invariants
{Findings}

## Pass 4 — Terminology Consistency
### 4a. Canonical Terms
{Findings: semantic drift, variant spellings}
### 4b. Enum Consistency
{Findings}

## Pass 5 — Agent Inventory Consistency
### 5a. Filesystem vs. AGENTS.md
{Findings}
### 5b. Competing Agent Index Detection
{Findings}
### 5c. Agent Header Validation
{Findings}

## Pass 6 — Document Hierarchy Coherence
### 6a. DIRECTIVE → CONTRACT Alignment
{Findings}
### 6b. SPEC ↔ role registry write_scope Alignment
{Findings}
### 6c. TYPES.md ↔ SPEC.md Schema Alignment
{Findings}
### 6d. CONTRACT Enforcement Map
{Findings}

## Pass 7 — Claim Strength Calibration

{Calibrated claims, supporting warrant, and IssueType: K-CLAIM-1 findings}

## Decision Log
{Any human overrides, defaults applied, assumptions made}
```

### Governance_Audit_IssueLog.csv

| Column | Type | Required | Description |
|--------|------|----------|-------------|
| `IssueID` | string | MUST | Unique issue identifier (e.g., `GOV-001`) |
| `Category` | enum | MUST | `COUNT`, `XREF`, `INVARIANT_ID`, `TERMINOLOGY`, `AGENT_INVENTORY`, `HIERARCHY`, `CLAIM_CALIBRATION` |
| `IssueType` | string | MUST | Stable rule/check identifier; `K-CLAIM-1` for claim calibration, otherwise the applicable check ID |
| `Pass` | string | MUST | Pass number (e.g., `1a`, `2b`, `5c`) |
| `Severity` | enum | MUST | `BLOCKER`, `WARNING`, `INFO` |
| `File` | string | MUST | Path to the file containing the issue |
| `Section` | string | SHOULD | Section heading or line reference |
| `Description` | string | MUST | Concise description including concrete excerpt (≤25 words) |
| `ExpectedValue` | string | SHOULD | What the audit expected |
| `ActualValue` | string | SHOULD | What the audit found |
| `Recommendation` | string | MUST | Minimal fix recommendation |
| `EpistemicLabel` | enum | MUST | `FACT`, `ASSUMPTION`, `PROPOSAL` |

### governance_audit_summary.json

```json
{
  "run_id": "GovernanceAudit_{YYYY-MM-DD}_{HHmm}",
  "run_status": "OK | WARNINGS | BLOCKERS | FAILED_INPUTS",
  "date": "YYYY-MM-DD",
  "passes_executed": [1, 2, 3, 4, 5, 6, 7],
  "total_issues": 0,
  "issues_by_severity": {
    "BLOCKER": 0,
    "WARNING": 0,
    "INFO": 0
  },
  "pass_results": {
    "pass_1_count_integrity": "PASS | FAIL | SKIPPED",
    "pass_2_cross_reference": "PASS | FAIL | SKIPPED",
    "pass_3_invariant_id": "PASS | FAIL | SKIPPED",
    "pass_4_terminology": "PASS | FAIL | SKIPPED",
    "pass_5_agent_inventory": "PASS | FAIL | SKIPPED",
    "pass_6_hierarchy_coherence": "PASS | FAIL | SKIPPED",
    "pass_7_claim_calibration": "PASS | FAIL | SKIPPED"
  },
  "counts": {
    "k_invariants_defined": 0,
    "agents_in_directory": 0,
    "agents_in_agents_md": 0,
    "agents_in_dbm": 0,
    "tools_in_registry": 0,
    "xrefs_checked": 0,
    "xrefs_unresolvable": 0,
    "invariant_ids_checked": 0,
    "invariant_ids_orphaned": 0,
    "terms_checked": 0,
    "terms_drifted": 0
  }
}
```

### QA_Report.md

```markdown
# QA Report — Governance Audit

**Run:** GovernanceAudit_{YYYY-MM-DD}_{HHmm}
**Date:** {YYYY-MM-DD}

## Coverage
| Pass | Status | Files Scanned | Notes |
|------|--------|---------------|-------|
| 1 — Count Integrity | {COMPLETE|PARTIAL|SKIPPED} | {list} | {notes} |
| 2 — Cross-Reference | {COMPLETE|PARTIAL|SKIPPED} | {list} | {notes} |
| 3 — Invariant ID | {COMPLETE|PARTIAL|SKIPPED} | {list} | {notes} |
| 4 — Terminology | {COMPLETE|PARTIAL|SKIPPED} | {list} | {notes} |
| 5 — Agent Inventory | {COMPLETE|PARTIAL|SKIPPED} | {list} | {notes} |
| 6 — Hierarchy | {COMPLETE|PARTIAL|SKIPPED} | {list} | {notes} |

## Known Limitations
- {Specific limitations of this run}

## Assumptions
- {Assumptions made during the audit}

## Recommendations for Next Run
- {Specific improvements}
```

### _LATEST.md (pointer — mutable)

```markdown
Latest: GovernanceAudit_{YYYY-MM-DD}_{HHmm}
Updated: {YYYY-MM-DD}
```

---
