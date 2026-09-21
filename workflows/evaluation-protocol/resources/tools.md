# TOOL POLICY — evaluation-protocol

## Preferred tool order

1. Read the accepted basis, snapshots, and in-scope subject files named by the
   brief.
2. Prefer deterministic validators for deterministic checks (structure,
   dependency closure, schema conformance) when they are in the permitted
   toolbelt.
3. Use bounded audit capabilities or TASK workflows for bounded judgment work, as
   selected in the accepted toolbelt.
4. Fall back to direct reasoning to synthesize findings, conflicts, and the
   report content contract.

Dispatch of any audit, TASK workflow, tool, or bounded specialist is performed by
the WORKING_ITEMS shell, not by this workflow. The workflow carries the selection method
(the audit-toolbelt table) and the fan-in validation criteria; the shell issues
the sealed briefs and validates returns.

## Allowed deterministic tools

### Declared command restrictions

None. The execution.json command restriction is intentionally omitted. This workflow
declares no additional command restriction; permitted deterministic
validators are named per run in the accepted toolbelt and dispatched by the
WORKING_ITEMS shell.

### Operationally invoked

The structure and dependency audit CLIs are documented in WORKFLOW.md. Other deterministic validators and audit capabilities are
drawn from the brief's `PermittedToolbelt` and invoked under the WORKING_ITEMS
shell's authority (for example structure, dependency-closure, or governance
validators, or `TASK + content-digest`).

## Expected use of reasoning

This workflow is reasoning-first for evaluation judgment: distinguishing
observations, non-conformances, conflicts, duplicates, blockers, and unknowns;
verifying that cited evidence lies within the frozen basis and scope; and
composing the findings register, optional scorecard, recommendations, and
handoff. Reasoning never substitutes for a deterministic check that the accepted
toolbelt provides.

## Disallowed use

- No writes outside the brief's `AllowedWriteTargets` (normally under
  `{EXECUTION_ROOT}/_Evaluation/`).
- No modification of any subject file: deliverables, decomposition truth, source
  material, tool roots, or Git state.
- No dispatch of any capability absent from the accepted `PermittedToolbelt`.
- No scoring without an accepted rubric.
- No widening of write authority beyond the executing role and effective brief.

## Write boundary

The workflow may write only within the brief's `AllowedWriteTargets`, normally the
`_Evaluation/` artifact set: `EVALUATION_PROTOCOL.md`, `EVALUATION_REPORT.md`,
`FINDINGS.csv`, `HANDOFF.md`, and the `returns/`, `reports/`, and
`content-digests/` subtrees. It creates no files outside those targets.
