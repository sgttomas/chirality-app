# BRIEF SCHEMA — scc-resolution-case

Use this skill when WORKING_ITEMS needs to create or update a PKG-00 SCC case file.

## Required Fields

```yaml
PURPOSE: Create or update one SCC resolution case.
RequestedBy: WORKING_ITEMS
ScopePath: /abs/path/to/DEL-00-XX_...
TaskSkill: scc-resolution-case
ApplyEdits: true
AllowedWriteTargets:
  - /abs/path/to/DEL-00-XX_.../scc-cases/<case-folder>/
  - /abs/path/to/DEL-00-XX_.../_run_records/
RuntimeOverrides:
  CASE_ID: CASE-SCC-002
  CASE_PATH: /abs/path/to/DEL-00-XX_.../scc-cases/<case-folder>
  CASE_TITLE: SCC-002 PKG-10 Policy Proposal
  SCC_ID: SCC-002
  DEPCLOSURE_SNAPSHOT: /abs/path/to/execution/_Reconciliation/DepClosure/CLOSURE_...
  AFFECTED_DELIVERABLES: DEL-10-02;DEL-10-03
  CASE_STATE: OPEN_FOR_TASK_WORK
ExpectedOutputs:
  - Case_Contract.md
  - Case_Datasheet.md
  - Task_Findings.csv
  - Evidence_Register.csv
  - Candidate_Remedies.csv
  - Ruling_Register.csv
  - Open_Questions.md
  - Owner_Workflow_Handoff.md
  - Case_QA.md
```

## Optional Runtime Overrides

- `SEED_PACKET_PATHS` — semicolon-separated paths to prior packets to preserve under `case-seeds/`.
- `SCC_NODE_SET` — semicolon-separated SCC node set.
- `FOCUS_PAIRS` — semicolon-separated bidirectional pairs.

## Required Custom Instructions

- Treat existing scope-change packets as seed evidence, not active SCOPE_CHANGE intake.
- Do not edit product deliverables, dependency registers, decomposition files, `_ScopeChange/`, or `_Reconciliation/`.
- Do not report SCC closure or project-wide blocked/unblocked status.

