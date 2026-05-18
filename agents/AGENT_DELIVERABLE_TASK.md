---
description: "Compatibility pointer for legacy DELIVERABLE_TASK briefs"
---
[[DOC:AGENT_INSTRUCTIONS]]
# AGENT INSTRUCTIONS — DELIVERABLE_TASK Compatibility Pointer
AGENT_TYPE: 2

`DELIVERABLE_TASK` is no longer a separate operational agent pathway.

Use canonical `TASK` (`agents/AGENT_TASK.md`) for bounded Type 2 work. When a
brief provides `DeliverablePath`, `TASK` automatically enters deliverable-local
mode and must read the deliverable-local truth set before analysis or edits:

1. `_CONTEXT.md`
2. `_STATUS.md`
3. `_REFERENCES.md`
4. `_DEPENDENCIES.md`
5. `MEMORY.md`
6. Primary deliverable artifacts, normally `Datasheet.md`, `Specification.md`,
   `Guidance.md`, and `Procedure.md`

Legacy briefs may still include `TaskProfile: DELIVERABLE_TASK`; `TASK` treats
that value as a compatibility label for deliverable-local mode, not as a
separate profile with independent authority.

Closeout rules are also in `AGENT_TASK.md`: `TASK` writes the durable
`_run_records/TASK_RUN_*.md`; `MEMORY.md` is updated when there is durable
context to preserve; `_STATUS.md` remains read-only unless explicitly
authorized by the human and the brief states the exact status change.

For tranche orchestration, `WORKING_ITEMS` remains the Type 1 parent posture:
it proposes a bounded tranche, waits for human approval, dispatches canonical
`TASK` workers with explicit scopes, and fans in review/audit results.
