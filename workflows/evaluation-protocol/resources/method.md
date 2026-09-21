# evaluation-protocol — method

## Method

Five phases, each gated; see the `evaluation-protocol` workflow for the per-step method.

1. **Frame and freeze** — confirm `EXECUTION_ROOT`, snapshots, basis, questions, scope, and stakes; propose the minimal toolbelt and decision points; gate on human acceptance and write `_Evaluation/EVALUATION_PROTOCOL.md`.
2. **Collect evidence** — prefer deterministic tools; dispatch TASK workflows or bounded TASK assignments for bounded judgment; stepwise unless the accepted protocol authorizes fan-out; preserve each return unrepaired.
3. **Validate fan-in** — confirm each artifact exists and matches its schema, cited evidence lies within frozen basis and scope, and record missing coverage, contradictions, and rerun requirements; refuse fan-in until mandatory returns are valid or explicitly waived.
4. **Evaluate and synthesize** — analyze the selected concerns; distinguish observations, non-conformances, conflicts, duplicates, blockers, and unknowns; score only requested dimensions against the accepted rubric; produce findings and recommendations without implementing them.
5. **Close and hand off** — write `_Evaluation/EVALUATION_REPORT.md` and a handoff state; route proposed file-state work to the appropriate manager (normally WORKING_ITEMS (workflow: change), WORKING_ITEMS (workflow: project-setup), WORKING_ITEMS (workflow: scope-change), WORKING_ITEMS (workflow: review), or HELPS_HUMANS); record basis, coverage, waivers, blockers, rerun requirements, and derivative-package status.
