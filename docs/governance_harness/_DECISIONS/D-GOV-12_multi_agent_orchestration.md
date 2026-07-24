# D-GOV-12 — Multi-agent orchestration and package-level WORKING_ITEMS

Status:       RULED
HumanRuling:  Multi-agent orchestration plan approved by owner (Ryan Tufts), 2026-07-11
Ruling SHA:   8a8a477b90d65c4932c0e0bf8644c08f100cff3c
Date:         2026-07-11
FramedBy:     owner refinement of D-GOV-11 runtime hierarchy

## Ruling

1. Terminal fan-out/fan-in and supervised many-to-many agency are both
   canonical multi-agent orchestration patterns. Neither replaces the other.
2. A workflow may compose arbitrary dependency-valid sequences of individual
   and concurrent agent actions without assigning each composition a new
   pattern name. The recorded work graph governs execution.
3. The human may prescribe the pattern or sequence, constrain it partially,
   or delegate its selection to Agent 0 or a directly invoked Agent 1.
4. Pattern-selection precedence is: explicit human direction; human-approved
   constraints, priorities, and gates; accepted project/decomposition state
   and dependencies; Agent 0 cross-package judgment; Agent 1 intra-package
   judgment.
5. HELP_HUMAN manages cross-package orchestration and may supervise many
   instances of the same or different Agent 1 roles.
6. WORKING_ITEMS is a package-level Agent 1 manager. One instance owns one
   activated package, optionally narrowed to selected deliverables, and
   delegates bounded deliverable work to Agent 2.
7. Agent 1 may report coordination-relevant information upward during work.
   The parent may record, relay, amend, hold, replan, escalate, or route it.
8. Agent 0 brokers Agent 1 coordination; Agent 1 brokers Agent 2 coordination.
   Siblings do not use undeclared direct messaging and children do not bypass
   their parent.
9. Manager-selected orchestration inside an accepted scope does not require
   separate approval for every child. Scope expansion, consequential risk,
   authority changes, shared-write conflicts, or acceptance changes return to
   the human.
10. SOFTWARE_DEV is deferred. Software work first uses package-level
    WORKING_ITEMS plus activation profiles, TASK skills, deterministic tools,
    and ephemeral generalists for novel stacks.

## Relationship to D-GOV-11

D-GOV-11 remains governing for the runtime hierarchy, direct Agent 1 entry,
Agent 2 construction forms, component ownership, and staged runtime bridge.
This ruling extends D-GOV-11 by adding live parent-mediated coordination to
filesystem/Git coordination and by replacing the deliverable-local
WORKING_ITEMS interpretation with package-level management.

## Orchestration safety

- Every child declares read scope, write targets, dependencies, expected
  returns, and fan-in criteria.
- Shared reads are allowed. Concurrent sibling writes must be disjoint.
- Overlapping writes require serialization against an accepted predecessor or
  one declared integration owner.
- Failed nodes block only declared dependants; independent work continues.
- Relays preserve claim status. Objective, basis, write-scope, ownership,
  risk, or acceptance changes require versioned brief amendments.
- Runtime records are control-plane evidence, not decomposition or deliverable
  truth.

## Scope not granted

- No direct sibling messaging or Agent 1-to-Agent 1 delegation.
- No Agent 0-to-Agent 2 delegation and no Agent 2 delegation.
- No weakening of human gates, context sealing, capability non-inheritance,
  path containment, or validated fan-in.
- No creation of SOFTWARE_DEV in this tranche.
- No modification of active concordance worktrees before their accepted
  handoffs are integrated.
