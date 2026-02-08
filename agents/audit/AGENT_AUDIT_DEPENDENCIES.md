[[DOC:AGENT_INSTRUCTIONS]]
# AGENT INSTRUCTIONS — AUDIT_DEPENDENCIES (Type 2 Task • Audit Dependency Registers)
AGENT_TYPE: 2

These instructions govern a **Type 2** task agent that audits deliverable-local dependency registers for:
- schema hygiene,
- evidence/provenance completeness,
- enum/ID normalization,
- and referential integrity.

It reads (per deliverable):
- `_DEPENDENCIES.md`
- `Dependencies.csv`

And it writes **audit artifacts only** to a reconciliation tool root. It does **not** edit deliverables.

This task is designed to be invoked by **RECONCILIATION (Type 1)** (and MAY also be invoked by **WORKING_ITEMS (Type 1)** with an explicit brief).

**The human does not read this document. The human has a conversation. You follow these instructions.**

---

**Naming convention:** use `AGENT_*` when referring to instruction files (e.g., `AGENT_CHANGE.md`); use the role name (e.g., `CHANGE`) when referring to the agent itself. This applies to all agents.

## Agent Type

| Property | Value |
|---|---|
| **AGENT_TYPE** | TYPE 2 |
| **AGENT_CLASS** | TASK |
| **INTERACTION_SURFACE** | INIT-TASK |
| **WRITE_SCOPE** | tool-root-only (`{EXECUTION_ROOT}/_Reconciliation/DependencyAudit/`) |
| **BLOCKING** | never |
| **PRIMARY_OUTPUTS** | Dependency Audit Report + Issue Log |

---

## Non-negotiable invariants

- **Read-only deliverables.** Do not edit any deliverable-local file (`Dependencies.csv`, `_DEPENDENCIES.md`, or the four documents).
- **Evidence-first.** Every finding MUST cite a concrete file + location (line/heading if available).
- **No invention.** If a check cannot be completed (missing files, unparseable CSV), record that as a finding with the smallest next check.
- **Minimal fix bias.** Recommend the smallest change that restores validity (prefer field normalization over semantic reinterpretation).
- **Schema-flexible.** Handle legacy schemas:
  - If `RegisterSchemaVersion` is present, use it.
  - Otherwise infer schema from column presence (e.g., v3 has `DependencyClass`/`AnchorType`; v2 does not).

---

## Inputs (brief-driven)

Required:
- `EXECUTION_ROOT`: default `execution/`
- `RUN_LABEL`: short label for naming outputs (default `DEPENDENCY_AUDIT`)
- `SCOPE`: deliverable IDs, package IDs, explicit paths, or `ALL` (only if explicitly requested)

Optional:
- `RUBRIC_FILE`: default `AUDIT_DEPENDENCIES.md`
- `EVIDENCE_ROOTS`: optional extra folders/files to search for supporting evidence (default: deliverables in scope only)
- `VERBOSITY`: `LOW` (default) | `MED` | `HIGH`

---

## Outputs

Ensure (create if missing) the tool root:
- `{EXECUTION_ROOT}/_Reconciliation/DependencyAudit/`
- `{EXECUTION_ROOT}/_Reconciliation/DependencyAudit/_Archive/`

Per run, create a run folder:
- `{EXECUTION_ROOT}/_Reconciliation/DependencyAudit/{YYYY-MM-DD}_{RUN_LABEL}/`

Write:
- `{EXECUTION_ROOT}/_Reconciliation/DependencyAudit/{YYYY-MM-DD}_{RUN_LABEL}/Dependency_Audit_Report.md`
- `{EXECUTION_ROOT}/_Reconciliation/DependencyAudit/{YYYY-MM-DD}_{RUN_LABEL}/Dependency_Audit_IssueLog.csv`

Optional pointer (overwrite allowed; pointer only):
- `{EXECUTION_ROOT}/_Reconciliation/DependencyAudit/_LATEST.md`

---

[[BEGIN:PROTOCOL]]
## PROTOCOL

### Step 0 — Preconditions

1) Confirm `RUBRIC_FILE` exists and is readable; if missing, continue with built-in checks and record `[WARNING] MISSING_RUBRIC_FILE`.
2) Resolve `EXECUTION_ROOT` and `SCOPE`.
3) Determine `RunID = {YYYY-MM-DD}_{RUN_LABEL}`.

### Step 1 — Enumerate deliverables in scope

For each deliverable folder in `SCOPE`, attempt to locate:
- `{deliverable}/Dependencies.csv`
- `{deliverable}/_DEPENDENCIES.md`

Record missing artifacts as findings (do not guess contents).

### Step 2 — Audit dependency registers

For each deliverable with a readable `Dependencies.csv`:
- Validate CSV is parseable.
- Validate required columns are present for its inferred/declared schema version.
- Validate `DependencyID` presence + uniqueness.
- Validate canonical enums where applicable (Direction/Status/SatisfactionStatus/etc.).
- Validate evidence completeness for `Status=ACTIVE` rows (`EvidenceFile` + `SourceRef` or explicit `location TBD`).
- Validate target-ID placement rules when anchor fields exist:
  - `TargetDeliverableID` MUST be reserved for `TargetType=DELIVERABLE` and must match DEL ID format.
  - `TargetRefID` MUST be used for `TargetType=WBS_NODE`/`REQUIREMENT` (and similar non-deliverable IDs).
- Validate lifecycle hygiene (FirstSeen/LastSeen present; Status transitions are non-destructive).
- Flag obvious duplicates (same semantics, different IDs) as `MED` unless evidence indicates a blocker.

For each deliverable with a readable `_DEPENDENCIES.md`:
- Confirm it contains declared sections (do not enforce exact headings beyond “declared” vs “extracted” separation).
- If it contains summary counts, ensure they do not contradict CSV counts (best-effort; tolerate formatting variance).

### Step 3 — Produce report + issue log

Write:
- A report with:
  - scope summary,
  - audit coverage (how many deliverables had readable registers),
  - top findings by severity,
  - schema-version distribution (if detectable),
  - and a short “next actions” section for RECONCILIATION/CHANGE/ORCHESTRATOR.
- An issue log CSV with at least:
  - `IssueID`, `Severity`, `DeliverablePath`, `FromDeliverableID`, `DependencyID`, `File`, `Field`, `Symptom`, `Evidence`, `RecommendedFix`

### Step 4 — Return a concise run summary

In the task’s final message to the invoking manager, include:
- output paths written,
- counts by severity,
- and any blockers.

[[END:PROTOCOL]]

---

[[BEGIN:SPEC]]
## SPEC

An AUDIT_DEPENDENCIES run is valid when:
- No deliverable files are modified.
- Outputs are written to the specified tool root.
- Findings include concrete evidence locations.
- The issue log is complete and usable as a worklist for follow-up.

[[END:SPEC]]

