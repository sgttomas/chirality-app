# Agent Instruction Conformance and Disposition Rubric

**Normative basis:** `docs/WORKFLOW_COMPONENT_STANDARD.md`, with inherited
authority from `DIRECTIVE.md`, `CONTRACT.md`, `SPEC.md`, `TYPES.md`, and
`AGENTS.md`. `AGENT_HELPS_HUMANS.md` is the applying persona, not the canon.

Use this rubric for semantic review of every live `AGENT_*.md` file. Run
`tools/validation/validate_agent_instructions.py` first; do not spend semantic
review time rediscovering mechanically detectable structure errors.

## 1. Audit metadata

- Auditor:
- Date:
- Git SHA / branch:
- Files audited:
- Workflow-component standard SHA:
- Root governance SHA:
- Live `AGENTS.md` SHA:
- Deterministic validator result:
- Declared observation boundary:

## 2. Finding scheme

### Conformance

- `CONFORMS` — contract is coherent within the declared boundary.
- `PARTIAL` — directionally aligned but ambiguous, incomplete, or stale.
- `NONCONFORMANT` — contradicts authority, exceeds permissions, or cannot
  execute its claimed contract safely.
- `NOT_APPLICABLE` — check does not apply; reason required.

### Severity

- `BLOCKER` — unsafe authority/write behavior, unbounded execution, invalid
  structural contract, or active contradiction with a binding invariant.
- `HIGH` — changes outcomes, decision rights, or handoff/closure reliability.
- `MEDIUM` — material drift, duplication, compatibility risk, or avoidable
  execution ambiguity.
- `LOW` — localized hygiene or clarity issue.
- `INFO` — relevant fact, including a migration candidate with no current
  defect.

Every `PARTIAL` or `NONCONFORMANT` finding includes:

1. agent excerpt and section;
2. governing excerpt and section;
3. impact;
4. minimal correction or transformation; and
5. whether human judgment is required.

Do not overstate a structural check as proof of semantic safety.

## 3. Per-agent file card

| Field | Entry |
|---|---|
| Agent | |
| Current type/class/surface | |
| Current write scope | |
| Human interaction/gates | |
| Decision or escalation rights | |
| Shell/context/authorization semantics | |
| State/handoff ownership | |
| Main callers/dispatchers | |
| Primary outputs and authority classes | |
| Referenced skills/tools | |
| Compatibility obligations | |

## 4. Universal conformance checks

### 4.1 Authority and precedence

- Does the file defer to root governance, `AGENTS.md`, and the workflow-
  component standard without redefining them?
- Does it distinguish a human ruling from agent execution, validation, commit,
  push, report generation, or recommendation?
- Can lower-level instructions narrow but not silently weaken higher
  authority?

### 4.2 Write authorization

- Is the declared write scope consistent with every described write?
- For TASK execution, are `AllowedWriteTargets` distinct from read scope?
- Is active-checkout containment preserved?
- Are protected/authoritative paths identified where applicable?

### 4.3 Epistemic integrity

- Are non-trivial governed claims provenance-bearing or explicitly gaps?
- Are unknowns `TBD` rather than invented?
- Are conflicts surfaced for human ruling?
- Does claim strength comply with K-CLAIM-1?
- Does the file avoid incorrectly requiring producer-emitted FACT/warrant-state
  labels contrary to D-GOV-08?

### 4.4 Artifact authority

- Are outputs classified as authoritative truth, candidates, derivative
  packages, evidence, generated views, or convenience state?
- Can any generated or derivative output feed back as shadow authority?
- Are snapshot and pointer rules appropriate to the artifact class rather than
  applied universally?

### 4.5 Multi-phase integration

Where applicable:

- accepted upstream snapshot named;
- derivative-package currency tracked;
- explicit handoff state emitted;
- closure verdict includes audit and blockers;
- rerun requirements recorded;
- cycle behavior follows the recorded-move rule.

### 4.6 Runtime contract

- Inputs, outputs, failure posture, and stopping conditions are explicit.
- Human gates occur only at consequential decisions.
- Straight-through execution contains no mid-run human decision.
- Tool use respects the skill/tool boundary.
- Repeated prompt text is not substituting for a skill contract.

### 4.7 Lifecycle and compatibility

- Is active/deprecated/retired status explicit?
- Are stale names or callers present?
- If transformed, are replacement, compatibility scope, dispatcher updates,
  and removal condition defined?

## 5. Agent requalification test

Answer each with evidence:

| Question | Yes/No | Evidence |
|---|---|---|
| Distinct human interaction or gate lifecycle? | | |
| Distinct decision-right or escalation contract? | | |
| Distinct shell-level context/invocation/authorization semantics? | | |
| Durable workflow-state or handoff ownership? | | |
| Write posture impossible to express through bounded TASK? | | |
| Recurring reasoning method separable into a skill? | | |
| Deterministic operations separable into tools? | | |
| Run-specific material that belongs only in briefs? | | |

An agent needs at least one substantiated agent-level distinction. A dedicated
topic, output schema, tool sequence, or snapshot location does not qualify it.

For Type 2 agents other than TASK, require evidence that their shell behavior
cannot be represented by TASK. Absence of such evidence makes
`CONVERT_TO_SKILL` or `CONVERT_TO_TOOL` the default proposal, not an automatic
retirement act.

## 6. Disposition

Choose exactly one primary disposition:

| Disposition | Meaning |
|---|---|
| `RETAIN` | Agent-level contract is justified and current. |
| `SLIM` | Agent remains; reusable method and deterministic detail move down. |
| `MERGE` | Authority/interaction surface belongs in another persona. |
| `CONVERT_TO_SKILL` | Bounded reasoning moves under TASK. |
| `CONVERT_TO_TOOL` | Deterministic behavior moves to tools; any residual reasoning is separately classified. |
| `RETIRE` | No live role remains after compatibility closure. |

Required disposition record:

- Primary disposition:
- Confidence and evidence boundary:
- Retained agent-level contract, if any:
- Skill candidate(s):
- Tool candidate(s):
- Target dispatcher/owner:
- Active callers to migrate:
- Compatibility window:
- Removal condition:
- Required validation:
- Human decision still needed:

## 7. Suite-level synthesis

The audit package includes:

1. one file card and disposition per live agent;
2. cross-agent overlap and missing-ownership findings;
3. proposed target topology;
4. migration waves ordered by dependency and compatibility risk;
5. registry and narrative updates per wave;
6. deterministic tool/validator gaps;
7. unresolved human decisions; and
8. explicit statement that disposition proposals do not retire components by
   themselves.
