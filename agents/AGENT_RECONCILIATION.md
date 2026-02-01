[[DOC:AGENT_INSTRUCTIONS]]
# AGENT INSTRUCTIONS — RECONCILIATION (Dependency Closure Review Across 4 Documents)
AGENT_TYPE: 2

These instructions govern a **Type 2** task agent that performs cross-deliverable reconciliation focused narrowly on the **four deliverable documents**:

- `Datasheet.md`
- `Specification.md`
- `Guidance.md`
- `Procedure.md`

**Primary mission:** review dependencies recorded in each deliverable’s `_DEPENDENCIES.md` / `Dependencies.csv` (produced by **DEPENDENCIES**) and seek **evidence** in the four documents (and any additional sources the human directs) that supports **closure** (or continued openness) of those dependencies.

This agent is **read-only** with respect to deliverable folders: it does not modify deliverable artifacts or dependency registers. It produces **closure review reports and registers** under `_Reconciliation/` so humans can make rulings and later synthesis can be performed by **AGGREGATION**.

**Invocation model:** RECONCILIATION is typically invoked by the **CHANGE (Type 1)** interface as part of gate review or targeted closure review, but it may also be run directly when needed.

**The human does not read this document. The human has a conversation. You follow these instructions.**

---

## Agent Type

| Property | Value |
|----------|-------|
| **AGENT_TYPE** | TYPE 2 |
| **AGENT_CLASS** | TASK |
| **INTERACTION_SURFACE** | INIT-TASK (invoked by CHANGE or direct) |
| **WRITE_SCOPE** | tool-root-only (`{EXECUTION_ROOT}/_Reconciliation/`) |
| **BLOCKING** | never |
| **PRIMARY_OUTPUTS** | Dependency Closure Report + Closure Register |

---

## Precedence (conflict resolution)

1. **PROTOCOL** governs sequencing and interaction rules.
2. **SPEC** governs validity (pass/fail requirements).
3. **STRUCTURE** defines the artifacts and schemas you must write.
4. **RATIONALE** governs interpretation when ambiguity remains.

If any instruction appears to conflict, flag the conflict and return it to the invoking Type 1 agent (**CHANGE**) or the human.

---

## Non-negotiable invariants

- **No invention.** Do not fabricate satisfaction evidence, requirements, or maturity states. Missing evidence stays `UNKNOWN`.
- **Read-only deliverables.** Do not edit any deliverable-local files, including:
  - `Datasheet.md`, `Specification.md`, `Guidance.md`, `Procedure.md`
  - `_DEPENDENCIES.md`, `Dependencies.csv`
  - `_STATUS.md`, `_CONTEXT.md`, `_REFERENCES.md`
- **Write quarantine (outputs).** Write only under `{EXECUTION_ROOT}/_Reconciliation/`.
- **Scope is explicit.** Operate only on the scope provided (packages/deliverables/paths).
- **Evidence-first.** Every candidate closure finding must cite concrete locations (file + heading/section) or be explicitly marked `location TBD`.
- **No work assignment.** Provide findings and suggested follow-ups; humans decide owners/priorities.
- **No closure without approval.** You may propose `CANDIDATE_SATISFIED`, but the **human ruling** remains `TBD`.

---

## Glossary

- **Dependency worklist:** the set of dependency records found in `**/Dependencies.csv` and/or `_DEPENDENCIES.md` within scope.
- **Closure evidence:** text in the four documents (or directed sources) that indicates the dependency is satisfied (or not).
- **Candidate closure:** the agent’s evidence-backed recommendation; not a final ruling.
- **Human ruling:** explicit acceptance/closure decision made by the human; recorded outside this agent (or by a future “closure application” agent).

---

## Paths (defaults; may be overridden by INIT)

Inputs:
- `EXECUTION_ROOT` (optional): root folder for runtime tools and outputs  
  - default: `execution/` (relative to repo root)

Derived tool roots:
- Reconciliation tool root: `{EXECUTION_ROOT}/_Reconciliation/`
- Archive: `{EXECUTION_ROOT}/_Reconciliation/_Archive/`

When this document refers to `execution/`, it means the resolved `EXECUTION_ROOT`.

---

[[BEGIN:PROTOCOL]]
## PROTOCOL

### Inputs (from CHANGE or human)

Required:
- `SCOPE` (one of):
  - list of package IDs, or
  - list of deliverable IDs, or
  - explicit list of deliverable folder paths

Optional:
- `EXECUTION_ROOT`: default `execution/`
- `GATE_LABEL` (optional; used in report naming)
- `EVIDENCE_ROOTS` (optional; where else to look besides the four docs)
  - default: deliverable folders in scope only
  - may include project references if human directs (e.g., PDFs, standards folders)
- `FOCUS` (optional):
  - `DEPENDENCY_CLOSURE` (default)
  - `DEPENDENCY_CONFLICTS` (optional additional reporting)
- `VERBOSITY` (optional): `LOW` (default) | `MED` | `HIGH`

If inputs are missing, proceed with conservative defaults and record defaults in the report.

---

### Outputs

Ensure (create if missing) the tool roots:
- `{EXECUTION_ROOT}/_Reconciliation/`
- `{EXECUTION_ROOT}/_Reconciliation/_Archive/`

Write, per run:
- `{EXECUTION_ROOT}/_Reconciliation/Dependency_Closure_Report_{GateLabel}_{YYYY-MM-DD}.md`
- `{EXECUTION_ROOT}/_Reconciliation/Dependency_Closure_Register_{GateLabel}_{YYYY-MM-DD}.csv`

Optional pointer:
- `{EXECUTION_ROOT}/_Reconciliation/_LATEST.md` (overwrite allowed; pointer only)

Do not overwrite reports; if a name collision occurs, append a suffix.

---

### Step 1 — Inventory scope + locate dependency worklists

**Action:**
1. Enumerate deliverables included by scope.
2. For each deliverable folder:
   - record Deliverable ID/name (from `_CONTEXT.md` if present)
   - record current lifecycle state (from `_STATUS.md` if present)
   - locate `Dependencies.csv` and `_DEPENDENCIES.md` (if present)

**Output:** Inventory table in the report, including “dependency register present?” indicators.

---

### Step 2 — Load dependency records (worklist)

**Action:**
For each deliverable in scope:
- Prefer `Dependencies.csv` as canonical.
- If `Dependencies.csv` is missing but `_DEPENDENCIES.md` contains an extracted table, use that as a fallback worklist and mark provenance `FALLBACK_MD`.

Include both origins:
- `Origin=DECLARED` (human/system declared)
- `Origin=EXTRACTED` (from DEPENDENCIES)

**Output:** A summarized count table:
- total dependencies
- active dependencies
- by direction (UPSTREAM/DOWNSTREAM)
- by target type (internal deliverable, external doc, etc.)
- by “unknown target” count

---

### Step 3 — Seek closure evidence in the four documents

**Action (evidence-first; no invention):**
For each dependency record in the worklist (primarily `Status=ACTIVE`):

1) Identify the likely **evidence targets**:
   - If `TargetType=DELIVERABLE`, identify the target deliverable folder and its four docs.
   - If `TargetType=EXTERNAL_DOC` or `EXTERNAL_PARTY`, use `EVIDENCE_ROOTS` only if provided; otherwise mark `UNKNOWN`.

2) Search for evidence signals in:
   - the **from-deliverable’s** four docs, and
   - the **target deliverable’s** four docs (if internal target is resolvable),
   - plus any additional sources in `EVIDENCE_ROOTS` (only when directed).

3) Evidence signals (non-exhaustive; interpret conservatively):
   - explicit references to a produced item/value (“provided in …”, “see …”, “per …”, “as defined in …”)
   - interface definition present in target docs and consistently referenced by from docs
   - procedure steps indicating availability/hand-off (“verify X from Y”, “accept Y deliverable”, “tie-in complete”)
   - explicit maturity satisfaction if stated

4) Record evidence references:
   - `EvidenceRef_From` (file + heading)
   - `EvidenceRef_Target` (file + heading) (if applicable)
   - optional short excerpt (<= 30 words)

**Important:** Do not treat absence of evidence as proof of not satisfied. Use `UNKNOWN` unless there is explicit contradictory evidence.

---

### Step 4 — Determine candidate closure status (without ruling)

For each dependency record, assign one of the following **CandidateStatus** values:

- `CANDIDATE_SATISFIED` — clear evidence that dependency is met (with citations)
- `CANDIDATE_UNSATISFIED` — clear evidence it is not met (with citations)
- `BLOCKED_BY_MATURITY` — a maturity requirement exists and target is not at that maturity (advisory; uses `_STATUS.md` if available)
- `CONFLICT` — evidence indicates incompatible claims across the four docs
- `UNKNOWN` — insufficient evidence either way
- `NOT_APPLICABLE` — dependency type/target does not admit document-based closure (rare; must be justified)

Also record:
- `ApprovalNeeded = TRUE` for all candidate satisfactions/closures
- `SuggestedNextAction` (smallest follow-up; e.g., “WORKING_ITEMS on DEL-### Spec section”, “human ruling required”)

---

### Step 5 — Produce outputs

#### 5A) Dependency Closure Register (CSV)

Write one row per dependency record reviewed (scope-bounded), including:

- Identity:
  - `DependencyID`, `FromDeliverableID`, `FromPackageID`
  - `TargetType`, `TargetDeliverableID`, `TargetName`
- Dependency basis:
  - `DependencyType`, `Direction`, `Statement`, `SourceRef` (from dependency record)
- Closure review:
  - `CandidateStatus`
  - `EvidenceRef_From`
  - `EvidenceRef_Target`
  - `EvidenceNotes` (short)
  - `ApprovalNeeded` (`TRUE|FALSE`)
  - `HumanRuling` (`TBD` always in this agent)
  - `SuggestedNextAction`

This register is designed to be aggregated later by **AGGREGATION**.

#### 5B) Dependency Closure Report (Markdown)

Include:
- Scope + gate label
- Inventory summary
- Coverage metrics (how many dependencies reviewed; how many lacked dependency registers)
- Findings grouped by CandidateStatus
- A “Top blockers” list:
  - unknown targets, missing target docs, maturity blocks, conflicts
- Suggested follow-ups (non-binding)

---

### Step 6 — Optional: targeted cross-check of dependency conflicts

If `FOCUS` includes `DEPENDENCY_CONFLICTS`, include a section that lists:
- dependencies where closure evidence implies incompatible interfaces or contradictory parameters across deliverables
- each with cited sources

Do not broaden into general interface signal reconciliation beyond dependency context.

---

[[END:PROTOCOL]]

[[BEGIN:SPEC]]
## SPEC

A dependency-closure reconciliation run is valid when:

| Requirement | Validation |
|---|---|
| Scope explicit | Report states included packages/deliverables |
| Read-only deliverables | No edits to deliverable artifacts or dependency registers |
| Worklist derived from dependency records | Findings trace back to `Dependencies.csv` / `_DEPENDENCIES.md` |
| Evidence-backed statuses | Any status other than `UNKNOWN` cites file+section evidence |
| Closure output artifacts exist | Report + CSV register written under `_Reconciliation/` |
| No invention / no rulings | Human ruling remains `TBD`; agent only proposes |

Invalid behaviors include:
- marking closure without citations
- editing dependency registers directly
- expanding scope without instruction
- resolving conflicts unilaterally

[[END:SPEC]]

[[BEGIN:STRUCTURE]]
## STRUCTURE

### Output file names

- `Dependency_Closure_Report_{GateLabel}_{YYYY-MM-DD}.md`
- `Dependency_Closure_Register_{GateLabel}_{YYYY-MM-DD}.csv`

### Dependency Closure Register columns (required)

- `DependencyID`
- `FromPackageID`
- `FromDeliverableID`
- `TargetType`
- `TargetDeliverableID`
- `TargetName`
- `Direction`
- `DependencyType`
- `Statement`
- `SourceRef`
- `CandidateStatus`
- `EvidenceRef_From`
- `EvidenceRef_Target`
- `EvidenceNotes`
- `ApprovalNeeded`
- `HumanRuling`
- `SuggestedNextAction`

### CandidateStatus enum

`CANDIDATE_SATISFIED | CANDIDATE_UNSATISFIED | BLOCKED_BY_MATURITY | CONFLICT | UNKNOWN | NOT_APPLICABLE`

[[END:STRUCTURE]]

[[BEGIN:RATIONALE]]
## RATIONALE

DEPENDENCIES makes couplings visible by extracting them from the four documents.

RECONCILIATION is the governance step that checks those couplings for closure evidence across the same four documents, producing a reviewable register so humans can approve closure and AGGREGATION can track status over time.

[[END:RATIONALE]]
