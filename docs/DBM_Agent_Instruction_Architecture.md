# Design Basis Memorandum — Agent Instruction Architecture

> **Status:** Current design basis under D-GOV-11 and D-GOV-12. Managed hierarchy, enforced child scopes, validated fan-in, and parent-mediated coordination are implemented. Briefs are durable runtime evidence, not a substitute for an executing child session.

## 1. Purpose

This memorandum explains why Chirality separates runtime delegation roles from normative documents and how agent instructions, skills, tools, briefs, filesystem state, and Git state compose into governed workflows.

The canonical operational definition is:

```text
agent = LLM + instructions + declared files/context + tools + permissions
```

An agent instance is one running system. A role is a stable responsibility such as EVALUATION. An instruction package is the persistent `AGENT_*.md` contract for a named role. These are related but not interchangeable.

## 2. Runtime Hierarchy

```text
Human ↔ Agent 0 → Agent 1 → Agent 2
```

| Position | Name | Responsibility |
|---|---|---|
| Agent 0 | Supervising Architect | Aligns scope, stakes, authority, decision points, and managers with the human; supervises cross-manager fan-in |
| Agent 1 | Manager | Freezes a workflow contract, owns human gates, delegates bounded work, validates returns, and closes or hands off |
| Agent 2 | Specialist | Executes one sealed brief with declared context, tools, write scope, output contract, and no delegation |

HELP_HUMAN is the sole canonical Agent 0. Every Agent 1 is also a valid direct human entry point. A human may start an untyped session and adopt the hierarchy through steering instructions.

Agent 0 delegates only to named Agent 1 roles. Agent 1 delegates to Agent 2.
Agent 2 does not delegate. Capabilities are not inherited: a named child uses
its approved role policy, a generalist is bounded by its parent and brief, and
no child capability becomes available to the parent.

## 3. Standards Are External

Ratified system invariants, accepted domain standards, and accepted project
governance constrain all runtime layers. `docs/WORKFLOW_COMPONENT_STANDARD.md`
and `docs/DECOMPOSITION_STANDARD.md` are candidate external standards pending
explicit owner acceptance. None of these documents is an agent or Agent 0.

HELPS_HUMANS is the Agent 1 manager that applies and maintains workflow-component governance. It is not itself the constitutional source.

## 4. Agent 2 Construction

Agent 2 has three valid forms:

1. `TASK + skill + brief` for a recurring method with stable instructions.
2. An ephemeral bounded generalist for a novel, purpose-specific task whose sealed brief is sufficient and which does not justify a persistent role.
3. A dedicated named specialist with an approved `AGENT_*.md` when persistent runtime semantics, permissions, or evidence contracts cannot be carried safely by TASK or a brief.

The qualification order is tool, TASK skill, ephemeral generalist, then dedicated specialist. A dedicated package requires HELPS_HUMANS to document the failed alternatives, persistent semantic need, callers, compatibility plan, tests, and deprecation conditions, followed by explicit human approval.

## 5. Workflow Components

| Component | Function |
|---|---|
| Agent role | Owns judgment, gates, delegation, or a persistent bounded execution contract |
| Skill | Reusable reasoning method hydrated by TASK |
| Tool | Deterministic transformation or validation with explicit inputs and outputs |
| Brief | Sealed run-specific scope, context, permissions, outputs, and acceptance criteria |
| Workflow package | Durable evidence: accepted basis, briefs, returns, findings, decisions, snapshots, and handoff state |

Skills do not acquire authority from their dispatcher. Tools do not carry hidden judgment policy. Briefs do not relax parent permissions. Workflow packages preserve state across otherwise isolated agent contexts.

## 6. Delegation and Coordination

Runtime delegation and communication are hierarchical. Coordination is
many-to-many through both parent-mediated live agency and accepted filesystem
artifacts, dependencies, immutable snapshots, handoff records, and Git state.

Two named patterns are canonical. Terminal fan-out/fan-in dispatches bounded
independent children and coordinates through validated terminal returns.
Supervised many-to-many agency permits active children to report notices to
their parent, which may selectively relay information or amend dependent work.
Arbitrary mixed sequential/concurrent compositions are represented by a work
graph and need no additional pattern names. Humans may prescribe the graph or
delegate selection to the responsible Agent 0 or Agent 1.

HELP_HUMAN owns the cross-package graph. Each WORKING_ITEMS instance owns one
activated package and its intra-package graph across deliverables. Agent 0
brokers Agent 1 coordination; Agent 1 brokers Agent 2 coordination.

Git records versions and transport state; a commit or push is not semantic acceptance. Accepted truth is identified by the owning workflow’s gate and snapshot/handoff contract.

Fan-out is allowed only over disjoint scopes or declared shared dependencies. Fan-in validates presence, schema, evidence, and acceptance criteria before synthesis. A failed sibling does not erase independent successful returns, but shared-dependency effects must be surfaced. Each Agent 2 receives only declared context; prior chat state is not an implicit input.

## 7. Live Role Decisions

- HELP_HUMAN is sole Agent 0.
- HELPS_HUMANS owns agent, skill, tool, brief, validator, registry, compatibility, migration, and deprecation design.
- `DECOMP_BASE` is replaced by `docs/DECOMPOSITION_STANDARD.md`; decomposition managers consume the standard.
- EVALUATION owns generic audit orchestration, coherence assessment, scoring, and remediation recommendations.
- RECONCILIATION owns deliverable-corpus concordance from the accepted app-dev and piping calibrations and ratified method.
- PROJECT_SETUP owns human-gated schedule-basis workflows; deterministic graph calculation and rendering remain tools or TASK methods.
- PDF2MD and DRAWING_EXTRACT remain Agent 1 because source targets, schemas, review depth, and recovery posture require human calibration before repetitive work.
- WORKING_ITEMS is the package-level production manager and may coordinate many
  deliverable-scoped Agent 2 instances.
- REVIEW, CHANGE, RESEARCH, decomposition managers, SCOPE_CHANGE,
  DOMAIN_ENGINE, DBM_PUBLISHER, and EQUATION_AUDIT remain Agent 1 around their
  real human decisions.
- SOFTWARE_DEV is deferred until real trials demonstrate persistent manager
  semantics that WORKING_ITEMS plus software profiles, skills, tools, and
  ephemeral generalists cannot carry safely.

## 8. Persistence and Closure

Every phase-changing workflow follows the integration rules in `AGENTS.md`: derivative packages cite accepted upstream snapshots; phase boundaries produce immutable snapshots where governed; stopped work emits handoff state; closure requires accepted truth, derivative disposition, audit status, blockers, and rerun requirements; cycles are resolved explicitly rather than silently linearized.

## 9. Runtime Implementation

The application supports untyped, Agent 0, and Agent 1 direct sessions and
managed 0→1→2 child sessions. `delegate_agent` persists work graphs, launch
briefs, parentage, child kinds, instruction/brief hashes, declared context,
tools, write targets, status, and returns. Waiting children support terminal
fan-in; background children plus notices, updates, amendments, acknowledgments,
and safe-boundary update delivery support supervised many-to-many coordination.

The old SDK Agent bridge is disabled after managed-delegation acceptance. It
remains only as a fail-closed compatibility surface; managed sessions are the
sole executable nested path.
If managed delegation is unavailable, multi-agent execution defers; a durable
brief may preserve intent but does not claim that a child ran.

## 10. Conformance

Conformance is established by the canonical doctrine in `AGENTS.md`, exact `CLAUDE.md` import, instruction and skill validators, path/entrypoint validators, role-specific tests, runtime hierarchy tests, and workflow acceptance scenarios. Narrative lists never override the live instruction files, skills registry, tools registry, or accepted decisions.

## References

- `AGENTS.md`
- `docs/WORKFLOW_COMPONENT_STANDARD.md`
- `docs/DECOMPOSITION_STANDARD.md`
- `docs/governance_harness/_DECISIONS/D-GOV-11_runtime_agent_hierarchy.md`
- `docs/AGENT_DISPOSITION_MATRIX.md`
- `docs/DELIVERABLE_CONCORDANCE_METHOD.md`
