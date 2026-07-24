# D-GOV-10 — Workflow-component architecture normalization

Status:       RULED
HumanRuling:  All four architecture recommendations accepted by owner (Ryan Tufts), 2026-07-11
Ruling SHA:   923e5f9ad2143ddde4730c66bd9f412220c03a6c
Date:         2026-07-11
FramedBy:     owner-requested evaluation of the governance-harness overhaul and the live agent suite

## Ruling basis

The owner requested an evaluation beginning with
`agents/AGENT_HELPS_HUMANS.md`, including which agent instructions should
persist and which should move into skills, tools, or other forms.

The evaluation returned four recommendations:

1. Separate the normative workflow-component design standard from the
   executable HELPS_HUMANS persona. The standard belongs in `docs/`; the
   persona applies and maintains it.
2. Reserve semantic acceptance, issuance, conflict rulings, scope rulings,
   merges, destructive Git actions, and baseline decisions to humans. Permit
   routine commit/push closeout as an operational act when an explicit task or
   accepted handoff already authorizes it; the Git act is evidence capture,
   not approval.
3. Do not grandfather bespoke Type 2 agents. Every existing Type 2 instruction
   must requalify as an agent; otherwise its recurring reasoning method moves
   to a TASK skill and its deterministic operations move to tools.
4. Isolate this redesign from the active `chirality-piping` and
   `chirality-app-dev` reconciliation lanes, then rebase and integrate only
   after those lanes reach stable handoffs.

Owner response, verbatim:

> "I agree with all your recommendations."

The owner subsequently authorized the isolated implementation lane and
directed work to begin on branch `codex/agent-governance-redesign` in a
dedicated sibling worktree.

## Recorded outcome

The four recommendations above are ruled direction. This record governs the
implementation on the redesign branch. The exact wording of the new standard,
the agent disposition matrix, and migration patches remain reviewable
implementation artifacts; they do not acquire authority merely because they
were written.

## Consequences

1. A new `docs/WORKFLOW_COMPONENT_STANDARD.md` becomes the normative design
   standard for agents, skills, tools, briefs, and workflow packages.
2. `AGENT_HELPS_HUMANS.md` becomes a Type 1 persona that applies and maintains
   the standard. It no longer serves as the constitutional source itself.
3. Routine commit/push may occur under bounded prior authorization, but must
   never be represented as human acceptance, issuance, authentication, or a
   substantive ruling.
4. Every live agent receives one disposition:
   `RETAIN`, `SLIM`, `MERGE`, `CONVERT_TO_SKILL`, `CONVERT_TO_TOOL`, or
   `RETIRE`.
5. Type 2 identity is exceptional. TASK remains the canonical execution shell;
   another Type 2 agent persists only if it owns shell-level authorization,
   context, invocation, or runtime semantics that TASK cannot lawfully carry.
6. The current reconciliation worktrees are not modified by this branch.
   Integration follows rebase, conflict review, governance validation, and
   owner review.

## Scope not granted

- No existing agent is retired by this record alone.
- No skill migration is accepted until its method contract, compatibility
  posture, dispatcher changes, and validation evidence are reviewed.
- No deliverable, project, or domain reconciliation state is changed.
- No routine Git action becomes an approval or gate ruling.

## Supersession rule

Changing any of the four ruled directions above requires a superseding owner
decision. Implementation detail may change through review without superseding
this record when the ruled direction remains intact.
