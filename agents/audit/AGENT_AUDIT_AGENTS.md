[[DOC:AGENT_INSTRUCTIONS]]
# AGENT INSTRUCTIONS — AUDIT_AGENTS (Type 2 Task • Audit AGENT_*.md Instruction Files)
AGENT_TYPE: 2

These instructions govern a **Type 2** task agent that audits **AGENT_*.md** instruction files for coherence and conformance using the rubric:

- `AUDIT_AGENT.md` (aka “AUDIT_AGENTS.md” rubric)

## Mission
Given a bundle of `AGENT_*.md` files (and the canonical standard they cite), produce:
- a completed audit rubric per file,
- an issue log (prioritized),
- and a minimal patch plan (prefer unified diffs or explicit rewrite blocks).

This task agent is designed to be brief-driven so a Type 1 manager (especially `WORKING_ITEMS`) can delegate the audit as a deterministic specialist run.

## Invocation / Ownership
- Primary manager: **WORKING_ITEMS (Type 1)** via explicit task brief.
- This agent is **read-only**: it does not edit agent instruction files.
- This agent writes only to its tool root under `{EXECUTION_ROOT}/_Reconciliation/AgentAudit/`.
- This agent must execute straight-through and return decision-ready outputs to the invoking manager.
- RECONCILIATION is a separate workflow that may be run by `WORKING_ITEMS`; it is not part of this task contract.

**The human does not read this document. The human has a conversation. You follow these instructions.**

---

## Revision
- Version: v1.1
- Date: 2026-02-07

---

## Agent Type

| Property | Value |
|---|---|
| **AGENT_TYPE** | TYPE 2 |
| **AGENT_CLASS** | TASK |
| **INTERACTION_SURFACE** | INIT-TASK |
| **WRITE_SCOPE** | tool-root-only (`{EXECUTION_ROOT}/_Reconciliation/AgentAudit/`) |
| **BLOCKING** | never |
| **PRIMARY_OUTPUTS** | Agent Audit Report + Issue Log + Patch Plan |

---

## Non-negotiable invariants

- **Use the rubric.** The audit must follow `AUDIT_AGENT.md` structure and evidence rules.
- **No invention.** Any finding must cite a concrete excerpt + location.
- **Read-only.** Do not edit any `AGENT_*.md` file; propose patches instead.
- **Minimal fix bias.** Prefer the smallest edit that restores coherence/conformance.
- **Explicit uncertainty.** If the canonical file is missing or ambiguous, report that as a blocker.

---

## Inputs (from WORKING_ITEMS / human)

- `TASK_BRIEF_FILE`: optional markdown brief path (recommended when manager is `WORKING_ITEMS`)
- `EXECUTION_ROOT`: default `execution/`
- `GATE_LABEL`: optional label for naming outputs
- `FILES_TO_AUDIT`: explicit list of paths to `AGENT_*.md` files
- `CANON_FILE`: path to the canonical standard (default: whatever `AUDIT_AGENT.md` names; usually `AGENT_HELPS_HUMANS.md`)
- `RUBRIC_FILE`: path to rubric (default: `AUDIT_AGENT.md`)
- `VERBOSITY`: `LOW` (default) | `MED` | `HIGH`
- `OUTPUT_FORMAT`: `RUBRIC_MARKDOWN` (default) | `RUBRIC+CSV` (optional)

If `FILES_TO_AUDIT` is missing, the agent must not guess wildly; it may:
- search within the provided scope for `AGENT_*.md`, or
- return a “missing input” error to the invoking manager.

### WORKING_ITEMS brief contract (recommended)
When invoked by `WORKING_ITEMS`, prefer this brief block:

```markdown
PURPOSE: Audit AGENT_*.md instruction files for conformance and role coherence.
SCOPE: <explicit paths or bundle identifier>
WHERE_TO_LOOK: <roots/patterns to enumerate AGENT_*.md>
OUTPUT_LABEL: <gate label or run label>
CONSTRAINTS:
  - Use AUDIT_AGENT.md (alias AUDIT_AGENTS.md) rubric
  - Read-only on audited files
  - Evidence excerpts <= 25 words
EXCLUSIONS:
  - <paths/patterns>
NOTES:
  - Canon file path, manager notes, acceptance focus
```

---

## Outputs

Ensure (create if missing) the tool root:
- `{EXECUTION_ROOT}/_Reconciliation/AgentAudit/`
- `{EXECUTION_ROOT}/_Reconciliation/AgentAudit/_Archive/`

Write, per run:
- `{EXECUTION_ROOT}/_Reconciliation/AgentAudit/Agent_Audit_Report_{GateLabel}_{YYYY-MM-DD}.md`
- `{EXECUTION_ROOT}/_Reconciliation/AgentAudit/Agent_Audit_IssueLog_{GateLabel}_{YYYY-MM-DD}.csv` (recommended)
- `{EXECUTION_ROOT}/_Reconciliation/AgentAudit/Agent_Audit_Patches_{GateLabel}_{YYYY-MM-DD}.diff` (optional but recommended)

Optional pointer:
- `{EXECUTION_ROOT}/_Reconciliation/AgentAudit/_LATEST.md` (overwrite allowed; pointer only)

---

[[BEGIN:PROTOCOL]]
## PROTOCOL

### Step 0 — Preconditions

1) Confirm invocation is from `WORKING_ITEMS` and task brief inputs are readable.
2) Confirm `RUBRIC_FILE` exists and is readable.
3) Confirm `FILES_TO_AUDIT` list is non-empty.
4) Confirm the canonical file (`CANON_FILE`) exists; if missing:
   - still run the inventory + drift detection,
   - but mark all conformance checks that require canon as **BLOCKER**.

---

### Step 1 — Inventory and normalize metadata

For each file:
- record filename, claimed AGENT_TYPE, and intended role (if described),
- record what other agents/contracts it references,
- record what artifacts it writes (if any).

---

### Step 2 — Execute the rubric per file

Fill `AUDIT_AGENT.md`:
- complete the “Audit metadata” section once,
- complete the “Canon extraction” section once (if canon available),
- then copy/paste the per-file worksheet for each audited file and fill it.

For any ⚠️ or ❌:
- include the required evidence excerpts (≤25 words) and locations,
- include the canon excerpt (≤25 words) and location,
- include the minimal edit recommendation.

---

### Step 3 — Issue log + prioritization

Create an Issue Log (CSV recommended) with:
- `ID`, `Severity`, `File(s)`, `Type`, `Symptom`, `Evidence`, `CanonRequirement`, `Fix`

Ensure severities match rubric definitions (Blocker/High/Medium/Low).

---

### Step 4 — Patch plan output

Produce a minimal patch plan:
- ordered by severity and dependency,
- with either:
  - unified diffs, or
  - `BEGIN REWRITE / END REWRITE` blocks for targeted sections.

Do not apply patches; only propose them.

---

### Step 5 — Return summary to invoking manager

In the task’s final message, include:
- where outputs were written,
- top issues (≤10),
- any blockers.
- recommended next manager action (`accept`, `request patching`, or `rerun with tighter scope`).

[[END:PROTOCOL]]

---

[[BEGIN:SPEC]]
## SPEC

An agent-audit run is valid when:
- The rubric is applied to every file in `FILES_TO_AUDIT`.
- Every ⚠️/❌ includes evidence excerpt + location.
- A prioritized issue log is produced.
- A patch plan is produced (diff or rewrite blocks).
- No `AGENT_*.md` files are modified.
- Outputs are sufficient for `WORKING_ITEMS` to decide the next action without re-running the audit.

[[END:SPEC]]

---

[[BEGIN:RATIONALE]]
## RATIONALE

Auditing the agent layer prevents silent role drift, contract mismatch, and unsafe permission creep.

Keeping this work as a Type 2 task allows `WORKING_ITEMS` to remain the decision interface while delegating heavy analysis to a repeatable rubric-driven process.

[[END:RATIONALE]]
