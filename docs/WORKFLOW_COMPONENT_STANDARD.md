# Workflow-Component Design Standard

Status: prospective Chirality v3 amendment authorized for Root implementation
by the owner on 2026-09-09. These candidate bytes do not themselves establish
final acceptance, downstream qualification, release, or project-loop adoption.
The D-GOV-14 edition remains the ratified basis until governed closeout;
historical text remains available at
`ee35409f5cf3a81ecb29a271527156b991df97b9`.

## Components

A role describes a persistent way of contributing. Chirality has four durable
roles: HELP_HUMAN (Type 0), HELPS_HUMANS and WORKING_ITEMS (Type 1), and TASK
(Type 2). An ephemeral Type 2 instance performs a bounded assignment without a
persistent role file. Subject matter and repeated methods belong in workflows.

A skill is reusable bounded contextual instruction with a canonical `SKILL.md`.
A workflow is reusable coordination or method guidance with a canonical
`WORKFLOW.md`. Either may be simple or complex and may have supporting
resources. A workflow may describe reasoning, operations, coordination,
branching, iteration, decisions, outputs, and recovery as applicable; selecting
one is optional unless the brief or an accepted instrument requires it. A
workflow may compose managers and executors and may help construct or invoke
other workflows. Loading a skill or workflow never creates another role,
launches execution, or grants additional capabilities.

A tool performs a deterministic operation with explicit inputs, outputs,
scope, errors, and repeat-execution behavior. A brief binds work to one run:
purpose, accepted basis, context, permissions, targets, outputs, and checks.
Runtime configuration defines selectable roles, capability ceilings, and
applicable workflow execution restrictions.

## Role instructions

Each role has one `agents/AGENT_<ROLE>.md`, with a title and four sections:

| Section | Content |
|---|---|
| PROTOCOL | Characteristic conduct and attention |
| SPEC | Standards by which the role judges its contribution |
| STRUCTURE | Relationships and forms of contribution |
| RATIONALE | Why this role is useful |

Write the essential behavior clearly and concisely. Keep machine metadata,
operational schemas, duplicated governance, and particular methods in their
own components. These sections retain the interpretation order PROTOCOL,
SPEC, STRUCTURE, RATIONALE; rationale does not create permissions.

## Workflow packages and loading

Use the project, user, and bundled library paths and precedence defined in
`AGENT_WORKFLOW_RUNTIME.md`. Project workflow discovery recognizes packages at
`.chirality/workflows/<name>/WORKFLOW.md`; historical flat
`.chirality/workflows/*.md` files remain ordinary documents and are not
canonical packages. Keep a short name and description. Organize a workflow
body for the undertaking; supporting references, templates, and helpers are
optional. Ordinary selective context includes Root `AGENTS.md`,
applicable project instructions, the active role, and available skill
descriptions. Load selected method bodies and only the resources needed for the
current stage. Specialized tool policy belongs in optional `execution.json`.
Selection retains source-qualified identity and collision origins. The runtime
contract defines catalog, ordering, history, replay, replacement, and selection
interfaces.

Write enough to preserve the decisions, outputs, interfaces, and recovery that
make the method work. Consolidate repetitions and use deterministic tools for
operations that need no semantic judgment. Workflow validity and successful
execution are distinct from the acceptance of its outputs.

## Authority, execution, and evidence

Human acceptance, scope decisions, conflict rulings, issuance, release, and
merge authority remain governed by the owning instruments. Execution, file
creation, validation, Git transport, and a coordination notice do not supply
those acts. Existing authority and checkout-containment rules apply to every
component.

A manager may coordinate any explicitly bounded undertaking. Method selection,
role compatibility, coordination, and execution remain separate; no selection
silently changes role or launches work. Package and
deliverable contracts continue to govern assignments expressed in those forms.
Every run has declared context, capability limits, write targets, and expected
returns. Shared reads are allowed; concurrent writes are disjoint or serialized
through a declared integration owner. Use actual executable child sessions and
record the mechanism and its enforcement limits. Type 2 returns coordination
needs to its caller and does not delegate.

Keep claim strength proportionate to evidence. Cite sources for nontrivial
governed claims, expose missing evidence and conflicts, and distinguish
interpretation from the human's commitments. Apply K-PROV-1, K-INVENT-1,
K-CONFLICT-1, and K-CLAIM-1 in their canonical contracts.

## Artifacts and completion

Distinguish accepted authoritative state, candidate governed records,
derivative packages, factual evidence, generated views, and convenience state.
A derivative package cites its accepted upstream snapshots and never replaces
their authority.

A phase-boundary decision that changes or validates governed state terminates
in a new immutable snapshot. Update a pointer only where its owning workflow
permits it. Later phases consume accepted snapshots and required current
derivatives; mutable working files alone are insufficient.

Handoffs name accepted upstream snapshots, derivative status, closure verdict,
rerun requirements, remaining blockers, and the next owner. Closure requires
accepted truth, current or explicitly deferred derivatives, recorded audit
status, and exposed unresolved blockers.

Resolve dependency cycles through recorded decomposition, inversion, merge, or
cut; merge and cut remain human decisions. Hold cycle-participating edges
non-gating until resolved, following `CYCLE_DRIVEN_RESOLUTION.md`.

## Maintenance and migration

HELPS_HUMANS develops component designs and governing amendments. WORKING_ITEMS
coordinates implementation after the undertaking is sufficiently understood.
Retirement includes a disposition ledger, replacement relationships, current
caller updates, compatibility handling, and validation. Preserve historical
records and accepted snapshots. Existing lifecycle labels ACTIVE, CANDIDATE,
DEPRECATED, and RETIRED keep their meaning in the migration inventory.

A changed instruction format carries an adoption hold for incompatible
consumers. Identify affected pins and mirrors, route coordination notices, and
leave receiving-loop adoption to its owner. A new Root candidate does not
silently amend accepted project instruments.

Design evidence is proportionate to the work: concrete decisions, necessary
contracts, relevant checks, and explicit unresolved matters. Behavioral trials
are not a prerequisite for this approved migration.

## Requirement identifier continuity

These identifiers remain available to existing audit and compatibility records.
Their component placement is interpreted through this edition; historical
reports retain their original cited meaning.

| ID | Requirement |
|---|---|
| R1 | Preserve explicit human decision rights. |
| R2 | Type 2 returns decisions to its caller and does not delegate. |
| R3 | Give runs explicit write boundaries; derived outputs do not replace source truth. |
| R4 | Match snapshot requirements to authority and phase boundaries; preserve immutable snapshots. |
| R5 | Cite evidence for nontrivial governed claims or record the source-location gap. |
| R6 | Expose unknowns and missing evidence. |
| R7 | Surface conflicts; human semantic rulings remain distinct from execution. |
| R8 | Bound Type 2 context, permissions, outputs, and failure returns through the brief. |
| R9 | Keep publication and Git operations reviewable; they do not establish semantic approval. |
| R10 | Make applicable workflow tool restrictions explicit in execution configuration. |
| R11 | Give deterministic tools explicit I/O, scope, errors, verification, and rerun behavior. |
| R12 | Distinguish role, runtime, workflow, tool, and brief responsibilities. |
| R13 | Calibrate claims to their warrant. |
| R14 | Preserve accepted-source, derivative, snapshot, handoff, closure, sequencing, and cycle requirements. |
| R15 | Keep registry membership and lifecycle status explicit; surface narrative drift. |
| R16 | Contain writes within the authorized active checkout. |
| R17 | Cover applicable execution and authority concerns with proportionate design evidence. |
