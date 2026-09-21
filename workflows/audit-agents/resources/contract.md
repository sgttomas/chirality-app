# audit-agents — contract

## Mission

Given an explicit set of `AGENT_*.md` files, produce:
- one reviewed-component record applying the relevant Roles or Workflows and tools criteria from docs/rubrics/AUDIT_AGENT.md,
- a prioritized Issue Log,
- a disposition and minimal remediation recommendation for every finding.

This agent is **read-only** on audited files: it proposes patches; it does not apply them.

---

## Non-negotiable invariants

- **Use the rubric.** Follow `docs/rubrics/AUDIT_AGENT.md` structure and evidence rules.
- **Evidence-first.** Any finding must cite a concrete excerpt + location (≤25 words).
- **No invention.** If canon/rubric is missing, mark checks as `BLOCKER` rather than guessing.
- **Read-only.** Do not edit any audited `AGENT_*.md` file; propose patches instead.
- **Mode-aware proposals.** CONFORMANCE repairs the accepted basis; explicitly authorized REDESIGN names the intended change and superseded contract.
- **Immutable snapshots.** Each run writes a new snapshot folder; never overwrite prior snapshots.
- **Pointer-only overwrite allowed.** `_LATEST.md` may be overwritten as a pointer; snapshots remain immutable.

---

## Inputs (brief-driven)

`AuditMode` is CONFORMANCE by default or REDESIGN under explicit design authority. Both modes return a patch plan; conformance proposals repair the accepted standard, while redesign proposals identify the intended standard change.

Required:
- `EXECUTION_ROOT`: default `execution/` (repo-relative)
- `FILES_TO_AUDIT`: explicit list of paths to `AGENT_*.md` files

Optional:
- `TASK_BRIEF_FILE`: optional markdown brief path (if manager wants file-based briefing)
- `RUN_LABEL`: short label for this run (default `AGENTS`)
- `CANON_FILE`: ratified standard path (default: `docs/WORKFLOW_COMPONENT_STANDARD.md`); ratified K-* governance controls conflicts
- `ROLE_REGISTRY`: default `agents/registry.json`; binds machine-readable role configuration
- `GOVERNING_FILES`: default `docs/DIRECTIVE.md`, `docs/CONTRACT.md`, `docs/SPEC.md`, `docs/TYPES.md`, and `AGENTS.md`
- `RUBRIC_FILE`: default `docs/rubrics/AUDIT_AGENT.md`
- `VERBOSITY`: `LOW` (default) | `MED` | `HIGH`
- `OUTPUT_FORMAT`: `RUBRIC_MARKDOWN` (default) | `RUBRIC+CSV`

If `FILES_TO_AUDIT` is missing or empty: write a `RUN_SUMMARY.md` with `RUN_STATUS = FAILED_INPUTS` and return a missing-input error to the invoking manager (do not infer scope).

---

## Outputs (write zone)

Ensure tool roots exist:
- `{EXECUTION_ROOT}/_Evaluation/AgentAudit/`
- `{EXECUTION_ROOT}/_Evaluation/AgentAudit/_Archive/`

Each run writes a new immutable snapshot folder:
- `{EXECUTION_ROOT}/_Evaluation/AgentAudit/AUDIT_{RUN_LABEL}_{YYYY-MM-DD}_{HHMM}/`

Snapshot contents (minimum):
- `Brief.md` (verbatim brief + normalized brief)
- `RUN_SUMMARY.md` (`RUN_STATUS = OK|WARNINGS|FAILED_INPUTS`)
- `QA_Report.md` (rubric coverage + blockers + limits)
- `Decision_Log.md` (defaults, overrides, tie-breaks)
- `Agent_Audit_Report.md` (reviewed-component records and applicable rubric assessments, grouped by file)
- `Agent_Audit_IssueLog.csv`
- `Agent_Audit_PatchPlan.diff` (or `.md`) — required

Pointer (overwrite allowed; pointer only):
- `{EXECUTION_ROOT}/_Evaluation/AgentAudit/_LATEST.md` → snapshot ID

---

## Validity

A run is valid when:
- Rubric applied to every file in `FILES_TO_AUDIT`.
- Every `PARTIAL` or `NONCONFORMANT` result includes an evidence excerpt and location.
- If canon exists, canon-dependent checks cite canon excerpts + locations.
- Issue log is prioritized and usable as a worklist.
- Patch plan exists (diff or rewrite blocks).
- No audited file is modified.
- Outputs are written to a new immutable snapshot folder.

---

## Artifacts and schemas

### Issue severity and reviewed-component schema

Agent_Audit_IssueLog.csv uses these columns: ID, Severity, File(s), Type, Symptom, Evidence, CanonRequirement, Fix. Severity is one of BLOCKER, HIGH, MEDIUM, LOW, INFO, with the meanings defined by docs/rubrics/AUDIT_AGENT.md. New findings use this vocabulary; historic audit snapshots remain unchanged.

Each reviewed-component record names the source path/revision/hash, accepted design basis, applicable rubric section, structural validator results, semantic findings, proposed corrections, and unresolved decisions. Role records reference agents/registry.json; workflow/tool records reference their own execution and I/O contracts.

### Output-root layout

```
{EXECUTION_ROOT}/_Evaluation/AgentAudit/
  _Archive/
  _LATEST.md
  AUDIT_{RUN_LABEL}_{YYYY-MM-DD}_{HHMM}/
    Brief.md
    RUN_SUMMARY.md
    QA_Report.md
    Decision_Log.md
    Agent_Audit_Report.md
    Agent_Audit_IssueLog.csv
    Agent_Audit_PatchPlan.diff
```

---
