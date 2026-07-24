---
name: scc-resolution-case
description: Create or update a PKG-00 SCC resolution case that accumulates bounded TASK findings, evidence, human rulings, candidate remedies, and owner-workflow handoffs until DepClosure can verify closure.
compatibility: Chirality TASK in generic shell mode; dispatched by WORKING_ITEMS for PKG-00 SCC case coordination.
metadata:
  chirality-skill-version: "1"
  chirality-task-profile: NONE
---

# SKILL — scc-resolution-case

## Purpose

Create or update one **SCC Resolution Case** under a PKG-00 control deliverable. The case is a living receptacle for repeated bounded TASK work across affected deliverables, human rulings, candidate remedies, owner-workflow handoffs, and eventual DepClosure evidence.

This skill does not resolve an SCC by itself. It records and organizes the evidence needed for the owning workflows to act.

## Suitable Shell

- `TASK` in generic shell mode with `ScopePath` set to a PKG-00 control deliverable folder or to the case folder itself.

## Required Inputs

- `ScopePath` — PKG-00 control deliverable folder or case folder.
- `RuntimeOverrides.CASE_ID` — local case ID, for example `CASE-SCC-002`.
- `RuntimeOverrides.CASE_PATH` — absolute output folder inside `{control-deliverable}/scc-cases/`.
- `RuntimeOverrides.CASE_TITLE` — human-readable case title.
- `RuntimeOverrides.SCC_ID` — SCC identifier from DepClosure.
- `RuntimeOverrides.DEPCLOSURE_SNAPSHOT` — accepted upstream DepClosure snapshot.
- `RuntimeOverrides.AFFECTED_DELIVERABLES` — semicolon-separated deliverable IDs.
- `RuntimeOverrides.CASE_STATE` — one canonical case lifecycle state.

## Case Lifecycle States

- `OPEN_FOR_TASK_WORK`
- `EVIDENCE_ACCUMULATING`
- `HUMAN_RULINGS_PENDING`
- `REMEDY_CLASSIFIED`
- `READY_FOR_OWNER_WORKFLOWS`
- `DEP_CLOSURE_PENDING`
- `CLOSED_BY_DEPCLOSURE`
- `BLOCKED_TBD`

## Read Boundary

Read only:

- the PKG-00 control deliverable in scope;
- existing case files under `CASE_PATH`;
- existing `case-seeds/` artifacts;
- cited DepClosure snapshot evidence;
- explicitly affected product deliverable evidence when needed for case indexing.

Do not scan unrelated packages except to resolve explicitly listed affected deliverables.

## Write Boundary

Write only:

- `{CASE_PATH}/Case_Contract.md`
- `{CASE_PATH}/Case_Datasheet.md`
- `{CASE_PATH}/Task_Findings.csv`
- `{CASE_PATH}/Evidence_Register.csv`
- `{CASE_PATH}/Candidate_Remedies.csv`
- `{CASE_PATH}/Ruling_Register.csv`
- `{CASE_PATH}/Open_Questions.md`
- `{CASE_PATH}/Owner_Workflow_Handoff.md`
- `{CASE_PATH}/Case_QA.md`
- `{CASE_PATH}/case-seeds/` only when preserving prior packet artifacts
- `{ScopePath}/_run_records/TASK_RUN_*.md` or `{CASE_PATH}/_run_records/TASK_RUN_*.md`

Never write:

- product package files;
- any `Dependencies.csv`;
- `_ScopeChange/`;
- `_Reconciliation/`;
- decomposition files.

## Output Contract

`Case_Contract.md` defines contribution rules, TASK deposit protocol, authority limits, and owner-workflow boundaries.

`Case_Datasheet.md` records SCC identity, node set, latest DepClosure baseline, affected deliverables, current case state, and seed artifacts.

`Task_Findings.csv` indexes bounded TASK outputs contributed over time.

`Evidence_Register.csv` indexes all evidence citations used by the case.

`Candidate_Remedies.csv` records remedy candidates per issue/edge with owner workflow and evidence.

`Ruling_Register.csv` records human rulings and disposition state.

`Open_Questions.md` records active human-facing questions.

`Owner_Workflow_Handoff.md` records downstream handoffs by owning workflow.

`Case_QA.md` records validator status, case state, unresolved blockers, and closure boundary.

## Method

1. Load `AGENT_TASK.md`, this skill, and companion files.
2. Resolve `CASE_PATH` and confirm it is under a PKG-00 control deliverable.
3. Read existing packet seeds and case files when present.
4. Create or update the case receptacle files.
5. Preserve existing packet artifacts as seed evidence, not active SCOPE_CHANGE intake.
6. Keep remedies candidate-level unless supported by human rulings and owner-workflow evidence.
7. Write a TASK run record with outputs and validation notes.

## Non-Negotiable Constraints

- Do not claim dependency rows were changed.
- Do not claim an SCC was closed unless a cited DepClosure snapshot proves it.
- Do not claim SCOPE_CHANGE was initiated.
- Do not claim project-wide blocker status.
- Unknowns remain `TBD`.
- Every candidate remedy must cite evidence or carry a `TBD` reason.
- SCOPE_CHANGE is one possible owner workflow, not the default remedy.

