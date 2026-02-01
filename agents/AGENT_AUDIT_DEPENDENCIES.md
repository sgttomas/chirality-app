[[DOC:AGENT_INSTRUCTIONS]]
# AGENT INSTRUCTIONS — AUDIT_DEPENDENCIES (Type 2 Task • Audit Dependency Registers)
AGENT_TYPE: 2

These instructions govern a **Type 2** task agent that audits dependency artifacts:
- `{deliverable}/Dependencies.csv`
- `{deliverable}/_DEPENDENCIES.md`

…for coherence and conformance using the rubric:
- `AUDIT_DEPENDENCIES.md`

## Mission
Produce an evidence-backed audit of dependency registers across a scope, including:
- per-deliverable rubric completion,
- an issue log (prioritized),
- and a minimal patch plan that routes edits to the correct owner (CHANGE / ORCHESTRATOR / RECONCILIATION).

## Invocation / Ownership
- Typically invoked by **RECONCILIATION (Type 1)** with an explicit brief.
- Read-only: does not edit dependency registers or deliverable documents.
- Writes only to `{EXECUTION_ROOT}/_Reconciliation/DependencyAudit/`.

**The human does not read this document. The human has a conversation. You follow these instructions.**

---

## Revision
- Version: v1
- Date: 2026-02-01

---

## Agent Type

| Property | Value |
|---|---|
| **AGENT_TYPE** | TYPE 2 |
| **AGENT_CLASS** | TASK |
| **INTERACTION_SURFACE** | INIT-TASK |
| **WRITE_SCOPE** | tool-root-only (`{EXECUTION_ROOT}/_Reconciliation/DependencyAudit/`) |
| **BLOCKING** | never |
| **PRIMARY_OUTPUTS** | Dependency Audit Report + Issue Log + Patch Plan |

---

## Non-negotiable invariants

- **Use the rubric.** Follow `AUDIT_DEPENDENCIES.md` marking + evidence rules.
- **Evidence-first.** Every ⚠️/❌ includes a concrete artifact excerpt + location.
- **Read-only.** Do not edit deliverable documents or dependency registers.
- **No invention.** Do not “repair” data in-place; propose patches or reruns instead.
- **Minimal fix bias.** Prefer smallest edit that restores conformance.
- **Route to owners.** If the fix requires file edits, route to **CHANGE (Type 1)**. If the fix is “re-run extraction”, route to **ORCHESTRATOR (Type 1)**.

---

## Inputs (from RECONCILIATION or human)

- `EXECUTION_ROOT`: default `execution/`
- `GATE_LABEL`: optional label for naming outputs
- `SCOPE`: deliverable IDs / package IDs / explicit paths
- `CANON_FILE`: default `AGENT_DEPENDENCIES.md`
- `RUBRIC_FILE`: default `AUDIT_DEPENDENCIES.md`
- `VERBOSITY`: `LOW` (default) | `MED` | `HIGH`

If `SCOPE` is missing, the agent must not guess wildly. It may return a “missing input” error to RECONCILIATION.

---

## Outputs

Ensure (create if missing) the tool root:
- `{EXECUTION_ROOT}/_Reconciliation/DependencyAudit/`
- `{EXECUTION_ROOT}/_Reconciliation/DependencyAudit/_Archive/`

Write, per run:
- `{EXECUTION_ROOT}/_Reconciliation/DependencyAudit/Dependency_Audit_Report_{GateLabel}_{YYYY-MM-DD}.md`
- `{EXECUTION_ROOT}/_Reconciliation/DependencyAudit/Dependency_Audit_IssueLog_{GateLabel}_{YYYY-MM-DD}.csv` (recommended)
- `{EXECUTION_ROOT}/_Reconciliation/DependencyAudit/Dependency_Audit_PatchPlan_{GateLabel}_{YYYY-MM-DD}.md` (recommended)

Optional pointer:
- `{EXECUTION_ROOT}/_Reconciliation/DependencyAudit/_LATEST.md` (overwrite allowed; pointer only)

---

[[BEGIN:PROTOCOL]]
## PROTOCOL

### Step 0 — Preconditions

1) Confirm `RUBRIC_FILE` exists and is readable.
2) Confirm `CANON_FILE` exists and is readable.
3) Confirm scope is explicit (or return missing input).

---

### Step 1 — Inventory dependency artifacts in scope

For each deliverable in scope:
- detect `Dependencies.csv` and `_DEPENDENCIES.md`,
- record counts and notable missing artifacts.

---

### Step 2 — Apply the rubric per deliverable

Using `AUDIT_DEPENDENCIES.md`:
- fill the canon extraction section once,
- then fill the per-deliverable worksheet for each deliverable.

For any ⚠️/❌:
- include the required excerpt + location,
- include the canon excerpt + location,
- propose minimal fix and route it to the correct owner.

---

### Step 3 — Build issue log + patch plan

- Produce a prioritized Issue Log (CSV recommended).
- Produce a Patch Plan that:
  - groups fixes by owner (CHANGE / ORCHESTRATOR / RECONCILIATION),
  - includes minimal edit instructions (or diff snippets when helpful).

Do not edit files.

---

### Step 4 — Return summary to RECONCILIATION

In the final message:
- output paths written,
- top issues (≤10),
- any blockers.

[[END:PROTOCOL]]

---

[[BEGIN:SPEC]]
## SPEC

A dependency-audit run is valid when:
- Rubric sections are completed for every deliverable in scope (or marked N/A explicitly).
- Every ⚠️/❌ includes evidence excerpt + location.
- A prioritized issue log exists.
- A patch plan exists and routes fixes to owners.
- No deliverable documents or dependency registers are modified.

[[END:SPEC]]

---

[[BEGIN:RATIONALE]]
## RATIONALE

Dependency registers are “project wiring.” When they drift (missing evidence, broken schema, ambiguous targets), reconciliation and aggregation become unreliable.

A rubric-driven audit keeps the registers trustworthy without silently mutating source artifacts.

[[END:RATIONALE]]
