# evaluation-protocol — contract

## Invariants

- **Human-defined basis.** Confirm the project root, accepted snapshots, source basis, evaluation questions, scope, and decision criteria before judging.
- **Read-only subject.** Never edit deliverables, decomposition truth, source material, tool roots, or Git state. Proposed changes are recommendations or explicit handoffs.
- **Evidence first.** Every finding cites a file, immutable snapshot, tool output, or validated Agent 2 return. Unsupported observations are labeled `ASSUMPTION`; missing evidence is `UNKNOWN`.
- **Human-directed toolbelt.** Dispatch only audits, TASK workflows, tools, or bounded specialists included in the accepted evaluation plan.
- **Stepwise by default.** Without an approved fan-out plan, run at most one Agent 2 dispatch per cycle and return its implications before continuing.
- **Validated fan-in.** Do not synthesize a child return until required artifacts exist and satisfy the brief schema. Missing, invalid, or conflicting returns remain visible.
- **No invented score.** Score only when requested and only against an accepted rubric.
- **No false closure.** A report is not closure unless basis, coverage, unresolved conflicts, blockers, and rerun requirements are recorded.

## Agent 2 Brief Contract

Every dispatch identifies: `REQUESTED_BY`, accepted basis and snapshot references, scope, declared files/context, permitted tools, write target, required outputs, acceptance criteria, escalation conditions, and dependency assumptions. Independent scopes may fan out only after the human accepts the plan. Shared dependencies must be declared.

## Validity

An evaluation is valid only when:

1. Its accepted basis, scope, toolbelt, and decision criteria are explicit.
2. Subject files outside `_Evaluation/` were not modified.
3. Every finding is evidence-linked and every score is rubric-linked.
4. Required Agent 2 outputs passed schema and coverage checks before fan-in.
5. Conflicts and missing evidence remain visible rather than being averaged away.
6. Cross-deliverable coherence findings distinguish genuine contradiction from project-specific divergence.
7. The final handoff names decisions, remediation owners, blockers, and rerun requirements.

Score only when requested and only against an accepted rubric. The `evaluation-protocol` workflow defines the default scoring scale and the overall weakest-link option; either applies only when the accepted protocol selects it.

## Artifacts and schemas

Outputs are quarantined under the authorized execution root’s _Evaluation directory. TOOL_ROOT identifies executable tools, not report storage:

```text
{EXECUTION_ROOT}/_Evaluation/
  EVALUATION_PROTOCOL.md
  EVALUATION_REPORT.md
  FINDINGS.csv
  HANDOFF.md
  returns/<DispatchID>/...
```

The `evaluation-protocol` workflow defines the `FINDINGS.csv` column schema and the final-report section contract.
