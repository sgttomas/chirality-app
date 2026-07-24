---
name: evaluation-protocol
description: Carry the five-phase read-only evaluation method — frame and freeze, collect evidence, validate fan-in, evaluate and synthesize, close and hand off — with the audit-toolbelt selection table, findings schema, scoring scale, and output-artifact contracts for a project evaluation dispatched by EVALUATION.
compatibility: Chirality TASK method pack; loaded under the EVALUATION (Type 1) shell, which supplies all write authority and remains the only dispatch/fan-in/validation surface
metadata:
  chirality-skill-version: "1"
  chirality-task-profile: NONE
---

# SKILL — evaluation-protocol

## Purpose

Carry the evaluation **method**: the read-only, evidence-grounded protocol for
assessing a human-defined project scope, producing decision-ready findings, an
optional scorecard, remediation recommendations, and a handoff state.

This skill is method-only. It holds the five-phase protocol, the audit-toolbelt
selection table, the `FINDINGS.csv` column schema, the default scoring scale,
the `_Evaluation/` output-artifact schemas, and the report content contract. It
does **not** hold decision rights, write scope, or a dispatch surface.

The authority to select stakes, accept the toolbelt and plan, dispatch children,
validate fan-in, waive returns, and approve a scoring rubric resides in the
**EVALUATION** Agent 1 shell (`agents/AGENT_EVALUATION.md`). This skill supports
those duties; it never performs them on its own authority. EVALUATION remains
the only surface that dispatches, validates fan-in, and writes governed state.

## Suitable agent shells

- `TASK` (generic shell mode, no profile)

Typical dispatcher: `EVALUATION` (Type 1). The dispatching brief supplies the
accepted basis, scope, evaluation questions, permitted toolbelt, and the write
target under `{EXECUTION_ROOT}/_Evaluation/`.

## Inputs

### Required

- `RuntimeOverrides.EXECUTION_ROOT` — absolute path to the project execution root
- Accepted basis / snapshot references — the frozen upstream snapshots and
  source/decomposition basis the evaluation judges against
- Evaluation questions — the human-framed questions the evaluation answers
- Scope — the deliverables, packages, or governed surfaces in scope
- Permitted toolbelt — the accepted audits, TASK skills, tools, or bounded
  specialists this run may use (nothing outside this list is dispatched)
- `AllowedWriteTargets` — the write target(s), normally under
  `{EXECUTION_ROOT}/_Evaluation/`
- `ExpectedOutputs` — the artifacts this run must produce

### Optional

- Scoring rubric — required before any dimension is scored; without it, no score
  is produced
- Fan-out authorization — required before independent scopes are dispatched
  concurrently; absent it, dispatch is stepwise (at most one Agent 2 per cycle)

## Runtime overrides

| Key | Meaning | Default | Allowed values |
|---|---|---|---|
| `EXECUTION_ROOT` | Project execution root | **Required** | Valid directory path |

All other run parameters (basis, questions, scope, toolbelt, write targets,
rubric, fan-out authorization) are carried by the dispatching brief, not by
free-form overrides. See `BRIEF_SCHEMA.md`.

## Precedence

1. PROTOCOL governs sequencing and interaction.
2. SPEC governs validity.
3. STRUCTURE governs output contracts.
4. RATIONALE resolves remaining ambiguity.

Conflicts are surfaced to the human through EVALUATION; they are never silently
reconciled.

## Invariants

- **Human-defined basis.** The project root, accepted snapshots, source basis,
  evaluation questions, scope, and decision criteria are confirmed by EVALUATION
  before any judgment is formed.
- **Read-only subject.** Never edit deliverables, decomposition truth, source
  material, tool roots, or Git state. Proposed changes are recommendations or
  explicit handoffs.
- **Evidence first.** Every finding cites a file, immutable snapshot, tool
  output, or validated Agent 2 return. Unsupported observations are labeled
  `ASSUMPTION`; missing evidence is `UNKNOWN`.
- **Human-directed toolbelt.** Only audits, TASK skills, tools, or bounded
  specialists included in the accepted evaluation plan are used.
- **Stepwise by default.** Without an accepted fan-out plan, run at most one
  Agent 2 dispatch per cycle and return its implications before continuing.
- **Validated fan-in.** Do not synthesize a child return until required
  artifacts exist and satisfy the brief schema. Missing, invalid, or conflicting
  returns remain visible.
- **No invented score.** Score only when requested and only against an accepted
  rubric.
- **No false closure.** A report is not closure unless basis, coverage,
  unresolved conflicts, blockers, and rerun requirements are recorded.

## Audit toolbelt selection

Select the smallest accepted combination needed for the evaluation question.
Selection is confirmed by EVALUATION as part of the accepted plan; this table is
the method reference, not a grant to dispatch anything absent from the brief.

| Concern | Typical bounded capability |
|---|---|
| Structure and lifecycle state | `EVALUATION_STRUCTURE_AUDIT` or deterministic validators |
| Dependency integrity and closure | `EVALUATION_DEPENDENCY_AUDIT`, `AUDIT_DEP_CLOSURE` |
| Decomposition conformance | `AUDIT_DECOMP` |
| Epistemic ontology | `AUDIT_EPISTEMIC` |
| Governance and instruction conformance | `AUDIT_GOVERNANCE`, `AUDIT_AGENTS` |
| Hypergraph closure | `AUDIT_HYPERGRAPH_CLOSURE` |
| Deliverable content summaries | `TASK + content-digest` |
| Scored dimensions | `EVALUATION_REPORT` |

Dedicated audit roles remain compatibility-capable Agent 2 specialists until
their callers, replacement TASK skills or tools, migration behavior, and tests
land together. Dispatch, brief-sealing, and fan-in for any of these capabilities
are performed by the EVALUATION shell, never by this skill.

## Agent 2 brief contract (supported, not owned)

When EVALUATION dispatches a child under this method, every dispatch identifies:
`REQUESTED_BY`, accepted basis and snapshot references, scope, declared
files/context, permitted tools, write target, required outputs, acceptance
criteria, escalation conditions, and dependency assumptions. Independent scopes
may fan out only after the human accepts the plan; shared dependencies are
declared. This skill records the contract shape; EVALUATION seals and issues it.

## Method

### Phase 1 — Frame and freeze

1. Confirm `EXECUTION_ROOT`, accepted upstream snapshots, source/decomposition
   basis, evaluation questions, scope, and stakes.
2. Inventory available deterministic validators and bounded audit capabilities.
3. Propose the minimal toolbelt, dispatch order, output locations, scoring
   rubric if any, and decision points.
4. Obtain human acceptance (through EVALUATION) and write
   `_Evaluation/EVALUATION_PROTOCOL.md`.

### Phase 2 — Collect evidence

1. Prefer deterministic tools for deterministic checks.
2. Dispatch TASK skills or named specialists for bounded judgment work.
3. Use stepwise dispatch unless the accepted protocol authorizes independent
   fan-out.
4. Preserve each return as produced; do not silently repair it.

### Phase 3 — Validate fan-in

1. Confirm each expected artifact exists and matches its output schema.
2. Verify cited evidence lies within the frozen basis and scope.
3. Record missing coverage, contradictions, invalid returns, and rerun
   requirements.
4. Refuse fan-in until mandatory returns are valid or explicitly waived by the
   human.

### Phase 4 — Evaluate and synthesize

1. Analyze structural, dependency, epistemic, governance, instruction, and
   cross-deliverable coherence as selected by the protocol.
2. Distinguish observations, non-conformances, conflicts, duplicates, blockers,
   and unknowns.
3. Score only requested dimensions against the accepted rubric.
4. Produce findings and remediation recommendations; do not implement them.

### Phase 5 — Close and hand off

1. Write `_Evaluation/EVALUATION_REPORT.md` and a handoff state.
2. Identify human decisions and route proposed file-state work to the
   appropriate manager, normally CHANGE, PROJECT_SETUP, SCOPE_CHANGE, REVIEW, or
   HELPS_HUMANS.
3. Record accepted basis, audit coverage, waivers, blockers, rerun
   requirements, and derivative-package status.

## Scoring scale

Scoring is optional and gated on an accepted rubric selected by EVALUATION.
The default scoring scale, when approved, is:

```text
EXEMPLARY | CONFORMANT | PARTIAL | NON-CONFORMANT
```

An overall weakest-link score may be used only if the accepted protocol selects
it. Without an accepted rubric, no score is produced.

## Output structure

All outputs are written under the write target the brief supplies, normally:

```text
{EXECUTION_ROOT}/_Evaluation/
  EVALUATION_PROTOCOL.md
  EVALUATION_REPORT.md
  FINDINGS.csv
  HANDOFF.md
  returns/<DispatchID>/...
  reports/...
  content-digests/...
```

`FINDINGS.csv` minimally records these columns, in order:

```text
FindingID, Concern, Classification, Severity, Scope, Claim, EvidenceRefs, Status, RecommendedOwner, RerunRequirement
```

Every findings row is evidence-linked through `EvidenceRefs` (a file, immutable
snapshot, tool output, or validated Agent 2 return). Unsupported rows are labeled
`ASSUMPTION` and missing-evidence rows `UNKNOWN` in `Classification`/`Status`.

### Report content contract

`EVALUATION_REPORT.md` contains, at minimum, these sections:

- **Basis** — accepted snapshots, source/decomposition basis, decision criteria.
- **Method** — the accepted toolbelt and protocol actually run.
- **Coverage** — what was and was not assessed within scope.
- **Validated-return inventory** — each child dispatch and its fan-in verdict.
- **Findings** — the register content, aligned with `FINDINGS.csv`.
- **Conflicts / unknowns** — unresolved contradictions and missing evidence,
  kept visible rather than averaged away.
- **Optional scorecard** — only when a rubric was accepted.
- **Recommendations** — remediation guidance; not implemented here.
- **Decision queue** — the human decisions this evaluation surfaces.
- **Handoff summary** — named decisions, remediation owners, blockers, and rerun
  requirements, consistent with `HANDOFF.md`.

## Outputs

- `_Evaluation/EVALUATION_PROTOCOL.md` — accepted basis, toolbelt, dispatch
  order, output locations, rubric (if any), and decision points.
- `_Evaluation/EVALUATION_REPORT.md` — the report content contract above.
- `_Evaluation/FINDINGS.csv` — schema-complete, evidence-linked findings.
- `_Evaluation/HANDOFF.md` — decisions, owners, blockers, reruns, derivative
  status.
- `_Evaluation/returns/<DispatchID>/`, `reports/`, `content-digests/` — preserved
  child returns and evidence, as produced.

Exact filenames and the write root come from the brief. This skill never writes
outside the brief's `AllowedWriteTargets`.

## Non-negotiable constraints

- **Method only, no write authority.** This skill carries no write scope. Write
  targets come solely from the dispatching brief (normally under
  `{EXECUTION_ROOT}/_Evaluation/`). The skill never widens write authority
  beyond what the TASK shell and effective brief allow.
- **EVALUATION is the only dispatch/fan-in/validation surface.** Selecting
  stakes, accepting the plan and toolbelt, dispatching children, validating
  fan-in, waiving returns, and approving a scoring rubric are EVALUATION duties.
  This skill supports them and never assumes them.
- **Read-only subject.** Never modify deliverables, decomposition truth, source
  material, tool roots, or Git state. Proposed changes are recommendations or
  handoffs.
- **Quarantined outputs.** All writes stay under the brief's `_Evaluation/`
  targets. Historical `_Reconciliation/` artifacts are immutable evidence, never
  current evaluation authority.
- **Evidence-linked and rubric-linked.** Every finding is evidence-linked; every
  score is rubric-linked. No invented scores.
- **Validated fan-in before synthesis.** Required child outputs must pass schema
  and coverage checks before they are synthesized. Invalid or conflicting
  returns remain visible.
- **No false closure.** A report is closure only when basis, coverage,
  unresolved conflicts, blockers, and rerun requirements are recorded.

## QA expectations

- `EVALUATION_PROTOCOL.md` exists and names the accepted basis, toolbelt, and
  decision points.
- `FINDINGS.csv` rows are schema-complete (all ten columns) and each row is
  evidence-linked.
- `EVALUATION_REPORT.md` contains every section of the report content contract.
- `HANDOFF.md` names decisions, remediation owners, blockers, and rerun
  requirements.
- No files were written outside the brief's `AllowedWriteTargets`; no subject
  file outside `_Evaluation/` was modified.
- Any score present is backed by an accepted rubric.
