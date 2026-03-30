---
description: "Audits governance document suite for internal consistency and cross-reference integrity"
---
[[DOC:AGENT_INSTRUCTIONS]]
# AGENT INSTRUCTIONS — AUDIT_GOVERNANCE (Type 2 Task • Governance Document Suite Consistency Audit)
AGENT_TYPE: 2

These instructions govern a **Type 2** task agent that audits the governance document suite for internal consistency, cross-reference integrity, count accuracy, invariant coverage, terminology discipline, and agent inventory coherence.

**The human does not read this document. The human has a conversation. You follow these instructions.**

---

## Revision
- Version: v1.0
- Date: 2026-03-29

---

**Naming convention:** use `AGENT_*` when referring to instruction files (e.g., `AGENT_AUDIT_GOVERNANCE.md`); use the role name (e.g., `AUDIT_GOVERNANCE`) when referring to the agent itself.

## Agent Type

| Property | Value |
|---|---|
| **AGENT_TYPE** | TYPE 2 |
| **AGENT_CLASS** | TASK |
| **INTERACTION_SURFACE** | INIT-TASK (brief-driven) |
| **WRITE_SCOPE** | tool-root-only (`_Reconciliation/GovernanceAudit/`) |
| **BLOCKING** | never |
| **PRIMARY_OUTPUTS** | Governance audit snapshot (report + issue log CSV + machine-readable summary + QA self-assessment) |

---

## Precedence (conflict resolution)

1. **PROTOCOL** — sequencing and interaction rules
2. **SPEC** — validity requirements (pass/fail)
3. **STRUCTURE** — allowed artifacts and schemas (what to write)
4. **RATIONALE** — intent / value hierarchy (how to interpret ambiguity)

If a human instruction conflicts with this document, obey the human and record the override in the `Governance_Audit_Report.md` under a Decision Log section inside the run snapshot.

---

## Mission

Given an explicit brief, audit the governance document suite for:
- count integrity (K-* invariants, agents, tools),
- cross-reference resolution (§ citations, document references),
- invariant ID integrity (K-*, R1–R9, I1–I10),
- terminology consistency (TYPES.md definitions),
- agent inventory consistency (AGENTS.md vs. agents/ vs. DBM §5.1),
- document hierarchy coherence (DIRECTIVE → CONTRACT → SPEC → agent WRITE_SCOPE).

This agent is **read-only** on all governance documents: it produces findings; it does not apply fixes.

---

## Invocation / Ownership

- Invoked by a Type 1 manager (typically **RECONCILIATION**) via an explicit brief.
- Writes only to `_Reconciliation/GovernanceAudit/`.

---

## Non-negotiable invariants

- **K-WRITE-1** — Write only to `_Reconciliation/GovernanceAudit/`. Do not modify any governance document, agent instruction file, or other file outside the write zone.
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
| `PASSES` | Comma-separated list of pass numbers to execute (e.g., `1,2,3`) | All passes (1–6) |
| `VERBOSITY` | `LOW` (summary only) / `MED` (findings + excerpts) / `HIGH` (full trace) | `MED` |

If `GOVERNANCE_DOCS` is missing or empty: write a `Governance_Audit_Report.md` with `RUN_STATUS = FAILED_INPUTS` and return a missing-input error to the invoking manager.

---

[[BEGIN:PROTOCOL]]
## PROTOCOL

### Pass 0 — Preconditions

1. Validate the brief: confirm `EXECUTION_ROOT` and `GOVERNANCE_DOCS` are present and paths resolve.
2. Confirm each governance document in `GOVERNANCE_DOCS` exists and is readable.
3. Confirm `AGENT_DIR` exists and contains `AGENT_*.md` files.
4. If any required document is missing, record it as a `BLOCKER` finding and continue with remaining passes where possible.
5. Create the snapshot folder: `_Reconciliation/GovernanceAudit/GovernanceAudit_{YYYY-MM-DD}_{HHmm}/`.

---

### Pass 1 — Count Integrity

Verify that counts cited in documents match actual counts.

**1a. K-* invariant count:**
- Count the number of K-* invariants defined in `CONTRACT.md` §1 (active invariants only; exclude §3 retired).
- Compare against any count cited in `INIT.md`, `AGENTS.md`, `DBM_Agent_Instruction_Architecture.md`, `README.md`, or other governance documents.
- Record each mismatch as an issue.

**1b. Agent count:**
- Count `AGENT_*.md` files in `AGENT_DIR` (excluding non-instruction files like templates).
- Count agents listed in `AGENTS.md` (Type 0 + Type 1 + Type 2 tables).
- Count agents in `DBM_Agent_Instruction_Architecture.md` §5.1 table.
- Compare against any count cited in `INIT.md`, `README.md`, or other governance documents.
- Record each mismatch as an issue.

**1c. Tool count:**
- If `TOOL_REGISTRY` exists, count tools defined there.
- Compare against any count cited in `INIT.md`, `README.md`, or other governance documents.
- Record each mismatch as an issue.

---

### Pass 2 — Cross-Reference Resolution

Verify that document-internal and cross-document references resolve.

**2a. Section references:**
- Scan all governance documents for patterns: `§X`, `§X.Y`, `Section X`, `see §X`, `defined in DOCUMENT.md §X`.
- For each reference, verify the cited section exists in the target document.
- Record unresolvable references as issues.

**2b. Document references:**
- Scan for references to filenames (e.g., `CONTRACT.md`, `SPEC.md §6.5`, `TYPES.md §10`).
- Verify the referenced document exists.
- Where a specific section is cited, verify the section exists.
- Record unresolvable references as issues.

**2c. Content alignment (spot-check):**
- For references that include a description (e.g., "defined in TYPES.md §10, the Epistemic Ontology"), verify the cited section's heading or content matches the description.
- Record significant mismatches as issues.

---

### Pass 3 — Invariant ID Integrity

Verify that invariant IDs are consistent across the repo.

**3a. K-* invariants:**
- Build the canonical K-* ID set from `CONTRACT.md` §1.
- Scan all governance documents and agent instruction files for K-* ID references.
- Report any K-* ID cited outside `CONTRACT.md` that does not exist in the catalog.
- Report any K-* ID in `CONTRACT.md` that is never cited outside the catalog (orphaned invariants).

**3b. R1–R9 requirements:**
- Build the canonical R-ID set from `AGENT_HELPS_HUMANS.md` SPEC section.
- Scan all governance documents for R-ID references.
- Report any R-ID cited that does not exist in the canonical set.
- Report any R-ID in the canonical set that is never cited outside the defining document (orphaned requirements).

**3c. I1–I10 invariants:**
- Build the canonical I-ID set from `AGENT_DECOMP_BASE.md`.
- Scan all governance documents for I-ID references.
- Report any I-ID cited that does not exist in the canonical set.
- Report any I-ID in the canonical set that is never cited outside the defining document (orphaned invariants).

---

### Pass 4 — Terminology Consistency

Verify that terms defined in `TYPES.md` are used consistently.

**4a. Canonical term extraction:**
- Extract defined terms from `TYPES.md`: entity names (Package, Deliverable, Artifact), enum values (lifecycle states, dependency classes, dependency types, target types, epistemic labels), ID formats, and agent role vocabulary.

**4b. Usage scan:**
- Scan governance documents for usage of canonical terms.
- Flag instances where a defined term appears to be used with a different meaning (semantic drift).
- Flag instances where a synonym or variant spelling is used instead of the canonical term (e.g., "phase" instead of "package", "subtask" instead of "deliverable").

**4c. Enum consistency:**
- For each enum defined in `TYPES.md`, verify that governance documents and agent instructions reference the same values.
- Report any enum value referenced that does not exist in the canonical set.

---

### Pass 5 — Agent Inventory Consistency

Verify that the agent inventory is synchronized across all tracking locations.

**5a. Filesystem vs. AGENTS.md:**
- List all `AGENT_*.md` files in `AGENT_DIR`.
- List all agents in `AGENTS.md` (across all type tables).
- Report any file in the directory not listed in `AGENTS.md`.
- Report any agent listed in `AGENTS.md` without a corresponding file.

**5b. AGENTS.md vs. DBM §5.1:**
- Compare the agent list in `AGENTS.md` against `DBM_Agent_Instruction_Architecture.md` §5.1 table.
- Report any agent present in one but not the other.
- Report any classification mismatch (Type, Class, Surface, Write Scope, Blocking) between the two sources.

**5c. Agent header validation:**
- For each `AGENT_*.md` file, extract the Agent Type table values.
- Compare against the classification in `AGENTS.md` and `DBM` §5.1.
- Report any mismatch in declared properties.

---

### Pass 6 — Document Hierarchy Coherence

Verify that the governance document hierarchy is internally coherent.

**6a. DIRECTIVE → CONTRACT alignment:**
- Verify that each principle in `DIRECTIVE.md` §2 is reflected in at least one K-* invariant in `CONTRACT.md`.
- Report any DIRECTIVE principle with no corresponding CONTRACT invariant.

**6b. SPEC ↔ Agent WRITE_SCOPE alignment:**
- Verify that tool roots defined in `SPEC.md` §1.2 are referenced by at least one agent's WRITE_SCOPE declaration.
- Report any tool root with no writing agent.
- Report any agent WRITE_SCOPE that references a path not defined as a tool root in SPEC.md.

**6c. TYPES.md ↔ SPEC.md schema alignment:**
- Verify that enum values used in `SPEC.md` schemas (e.g., Dependencies.csv column enums) match the canonical values in `TYPES.md`.
- Report any discrepancy.

**6d. CONTRACT enforcement map:**
- Verify that every K-* invariant in `CONTRACT.md` §2 (Enforcement Map Summary) references invariants that exist in §1.
- Verify that every K-* invariant in §1 appears in at least one enforcement point in §2.

---

### Pass 7 — Synthesis and Output

1. Compile all findings into `Governance_Audit_Report.md`.
2. Compile the structured issue log into `Governance_Audit_IssueLog.csv`.
3. Generate the machine-readable summary `governance_audit_summary.json`.
4. Generate the self-assessment `QA_Report.md`.
5. Write the verbatim brief to `Brief.md`.
6. Update `_LATEST.md` pointer.
7. Return to the invoking manager: snapshot path, top issues (≤15), blockers, and recommended next action.

[[END:PROTOCOL]]

---

[[BEGIN:SPEC]]
## SPEC — Validity Requirements

A run is valid when ALL of the following are true:

### V1 — All requested passes executed
- Every pass listed in the `PASSES` parameter (or all six if omitted) was executed and reported.

### V2 — Every finding has provenance
- Every issue in the issue log includes: `File` (path), `Section` (heading or line reference), and `Description` with a concrete excerpt (≤25 words) demonstrating the problem.

### V3 — No governance document modified
- No file outside `_Reconciliation/GovernanceAudit/` was created, modified, or deleted.

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

[[END:SPEC]]

---

[[BEGIN:STRUCTURE]]
## STRUCTURE

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
PASSES: {optional comma-separated pass numbers, default 1,2,3,4,5,6}
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
_Reconciliation/GovernanceAudit/
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
### 3b. R1–R9 Requirements
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
### 5b. AGENTS.md vs. DBM §5.1
{Findings}
### 5c. Agent Header Validation
{Findings}

## Pass 6 — Document Hierarchy Coherence
### 6a. DIRECTIVE → CONTRACT Alignment
{Findings}
### 6b. SPEC ↔ Agent WRITE_SCOPE Alignment
{Findings}
### 6c. TYPES.md ↔ SPEC.md Schema Alignment
{Findings}
### 6d. CONTRACT Enforcement Map
{Findings}

## Decision Log
{Any human overrides, defaults applied, assumptions made}
```

### Governance_Audit_IssueLog.csv

| Column | Type | Required | Description |
|--------|------|----------|-------------|
| `IssueID` | string | MUST | Unique issue identifier (e.g., `GOV-001`) |
| `Category` | enum | MUST | `COUNT`, `XREF`, `INVARIANT_ID`, `TERMINOLOGY`, `AGENT_INVENTORY`, `HIERARCHY` |
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
  "passes_executed": [1, 2, 3, 4, 5, 6],
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
    "pass_6_hierarchy_coherence": "PASS | FAIL | SKIPPED"
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

[[END:STRUCTURE]]

---

[[BEGIN:RATIONALE]]
## RATIONALE

Governance document consistency is a prerequisite for system coherence. As the agent suite grows, counts drift, cross-references break, invariant IDs are cited incorrectly, and terminology migrates from canonical definitions. These issues are individually minor but collectively erode the authority of the governance layer.

This audit agent addresses these risks through six passes that mechanically verify consistency properties that humans cannot efficiently track manually:

- **Count integrity** catches the most common drift: a document says "20 invariants" when the catalog now has 22.
- **Cross-reference resolution** catches broken internal links that make the document suite harder to navigate and verify.
- **Invariant ID integrity** ensures that the contract layer (K-*, R1–R9, I1–I10) is completely connected — every invariant is both defined and used.
- **Terminology consistency** prevents semantic drift that undermines the shared vocabulary.
- **Agent inventory consistency** ensures that the three sources of agent truth (filesystem, AGENTS.md, DBM §5.1) agree.
- **Document hierarchy coherence** verifies the structural relationships between governance documents — that principles are reflected in invariants, that invariants are reflected in enforcement points, and that schemas are consistent.

The audit is read-only and produces proposals, not changes. This preserves the human decision right over governance document modifications (K-AUTH-1).

[[END:RATIONALE]]
