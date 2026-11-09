---
name: chirality-app-operating-entry
description: Locate and carry App work under the selected execution basis.
metadata:
  kind: instruction
  surface: operating-entry
  upstream:
    source: workflows/project-setup/resources/project-entry.md
    edition: library-v3.3.0
---
# App v4 development entry

## Direction

**Target:** public App v4, version 4.0.0. It is defined in the execution
basis [Release target and authority](../execution/_Coordination/CURRENT_EXECUTION_BASIS.md#release-target-and-authority)
and in the [publication punchlist](../execution/_Coordination/PUBLICATION_PUNCHLIST.md).

**Opening duty:** at the start of each session, Agent 0 states the path from
the current state to that target and identifies the work that can proceed
independently. Agent 0 runs that work in parallel through standalone Type 1
sessions.

**Working posture.** The owner's standing instruction (2026-11-09 00:29 UTC):
"This is just a standing instruction for you: Your top priority is to keep
productive work moving forward. Don't stall out in repetitive cycles of testing
and documenting of work. Some of that is necessary but easy to get absorbed in.
Keep development moving towards the publication goals. Tell your interlocutor
this is important for them to remind you of too, when relevant circumstances
arise."

- Testing and documenting serve the next step.
- When something outside Agent 0's authority blocks work, Agent 0 brings it
  to the owner at once as one decision with a recommendation, and keeps the
  other lanes moving.
- Agent 0 acts on authority already given and does not re-ask settled
  decisions.
- Budgets, caps and gates that Agent 0 sets itself are its own to change,
  and Agent 0 labels them as its own.

## Discovery

App v4 is this repository's product; v3 remains frozen in its release tags.
The normal discovery route is:

- [AGENTS](../AGENTS.md): authority, selected shared Library source, roles,
  verification, Git grant, privacy and platform/acquisition boundaries.
- [Current execution basis](../execution/_Coordination/CURRENT_EXECUTION_BASIS.md):
  release target, owning results, pending choices and recovery pointers.
- The affected `execution/PKG-nn/DEL-nn-nn/ScopeOfWork.md`, `Work/` and
  `deliverable.yaml`: commitments, current findings and dependency conditions.
  References written before 2026-10-30 to `Design/` mean `Work/`.
- [Deliverable tools](../tools/deliverables/README.md): neighborhood, impact,
  touches and graph queries; [PRD](../docs/PRD.md) and companion contracts:
  requirements and interfaces relevant to the undertaking.
- [App README](../app/README.md) and [CI selection](../docs/CI_SELECTION.md):
  build/test entry and what changed paths run.
- [Cross-project interface basis](../execution/_Coordination/HANDOFF_SWBPIPE_DOMAINS.md):
  App/host boundaries and retained receiving routes. PEC is retired and is not
  an App prerequisite.

Open PRs, issues and Git provide the review and change history. Current sessions
are discovered through T3 as AGENTS describes; repository lane records are not
live dispatch routes. The owner's launch steering supplies each session's
undertaking and per-session settings; the Direction above holds across sessions.
