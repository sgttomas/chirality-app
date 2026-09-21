# D-GOV-33 — Task Management Invocation-Local Federation Survey

Status:       RULED — PUBLISHED AND EFFECTIVE
HumanRuling:  "Require the survey whenever TASK_MANAGEMENT is already invoked; do not require loops to invoke TASK_MANAGEMENT." (owner, 2026-08-02; confirmed in-session and persisted in the managed run's `HUMAN_DIRECTION.md`)
ImplementationDirection: implement `plans/chirality-task-management/FEDERATION_SURVEY_IMPLEMENTATION_PLAN_2026-08-02.md` (owner goal, 2026-08-02)
Date:         2026-08-02
FramedBy:     HELP_HUMAN managed run `TM-FEDERATION-SURVEY-20260802`
AcceptedBasis: `main@4d55dea0f375034b66949723a7b849a2c962d8a3` (final PR base; the candidate was implemented from `3e03b257748822dba2ad7697453f3495fb7578db`, validated after refresh to `fe57138e6ce68fbcfe99b50676fcdd6114ec591a`, and finally synchronized through the approved source HEAD named below)
RecordConvention: owner ruling recorded before publication; validated implementation, approved source, final base, publication, and effective merge identities backfilled from completed Git/PR acts
DecisionKey:  `task_management_invocation_local_federation_survey`
Supersedes:   none; interprets D-GOV-32 and K-TM-4 without editing either
CandidateSHA: bb44d71c93cc5431d5fc8a902e716cc88966ea9f (validated implementation commit; PR #478)
ApprovedSourceSHA: 08ed85ae1a1ae2be9eba971e6567fad2bb202b56 (exact checked PR #478 source HEAD approved for merge)
FinalBaseSHA: 4d55dea0f375034b66949723a7b849a2c962d8a3 (PR #478 base immediately before merge)
PublicationSHA: 08ed85ae1a1ae2be9eba971e6567fad2bb202b56 (approved source HEAD carrying this record and the bounded federation-survey tranche)
EffectiveSHA: 2c25bd2c47c4b2f4190275ad39579a983f8786aa (merge of PR #478 into `main`, 2026-08-02)

## Recorded ruling

The owner aligned the behavior in-session on 2026-08-02:

<!-- BEGIN OWNER RULING VERBATIM -->
Require the survey whenever TASK_MANAGEMENT is already invoked; do not require loops to invoke TASK_MANAGEMENT.
<!-- END OWNER RULING VERBATIM -->

The owner then directed implementation of the bounded plan named above. The
managed run persists both acts at
`execution/_Coordination/AgentRuns/TM-FEDERATION-SURVEY-20260802/HUMAN_DIRECTION.md`.
On 2026-08-02 the owner subsequently directed, verbatim, "Merge via PR."
That act satisfies H2 publication direction and authorizes merge of this
validated tranche through its exact pull-request HEAD after required checks;
it does not authorize a direct `main` push or check bypass.

## Decision

Whenever `TASK_MANAGEMENT` is invoked for a loop with a canonical Task
Management register, the invoked instance must first perform a read-only
federation survey of every canonical Git-tracked Task Management register.
The survey reports its coverage before the requested mode and then the
manager continues under its existing authority.

This is an invocation-local requirement on an already-invoked manager. It is
not a standing loop sweep, loop-entry reader binding, schedule, workflow gate,
CI task, daemon, or requirement that any loop invoke `TASK_MANAGEMENT`.

## Effects

1. `agents/AGENT_TASK_MANAGEMENT.md` carries the mandatory preflight,
   `COMPLETE`/`PARTIAL` semantics, Root/global and non-Root/relevant
   presentation behavior, and a manual read-only fallback when the helper is
   unavailable.
2. `tools/taskmgmt/taskmgmt.py` gains a deterministic `federation` command
   that discovers tracked registers in sanctioned shapes, validates them,
   constructs typed-field relationships, and writes a rebuildable projection
   beside the invoking register.
3. The projection is derived, gitignored, rebuildable, and never authority.
   Its observations create no duty, disposition, approval, scope, lifecycle,
   schedule, or closure effect.
4. Every survey preserves register hashes. No receiving row is automatically
   created and no foreign register is written.
5. A `PARTIAL` or operational result prohibits a global-absence or global-
   closure claim; it does not bind or stop unrelated development-loop work.

## Relationship to D-GOV-32 and K-TM-4

D-GOV-32 remains the adoption record for the accepted Task Management PRD and
K-TM-1..6. K-TM-4 graceful absence still means that no act anywhere may
require Task Management to be invoked. D-GOV-33 distinguishes that rejected
standing obligation from the complete receive-side survey required after the
owner or loop has already chosen to invoke the manager.

The adopted PRD bytes and `docs/CONTRACT.md` are not edited. This record
carries the later owner interpretation and implementation direction.

## Scope limits

This ruling does not:

- amend any `LOOP_INIT.md`, standing workplan, register row, schema column,
  adopted PRD byte, or CONTRACT invariant;
- schedule or automatically invoke `TASK_MANAGEMENT`;
- create CI, daemon, event-bus, broker, or App-runtime integration;
- grant foreign-register writes, automatic row creation, or semantic
  disposition authority;
- create product, decomposition, deliverable, dependency, lifecycle, release,
  or professional-reliance effects; or
- authorize any publication route other than the owner-directed, checked PR
  merge of this bounded tranche.

## Publication posture

The bounded tranche was published through
[PR #478](https://github.com/sgttomas/chirality/pull/478). Immediately before
merge, CHANGE verified exact source HEAD
`08ed85ae1a1ae2be9eba971e6567fad2bb202b56` against final base
`4d55dea0f375034b66949723a7b849a2c962d8a3` and observed `SUCCESS` for
`Harness pre-merge`, `harness`, and `pec`. GitHub merged that exact head as
`2c25bd2c47c4b2f4190275ad39579a983f8786aa`, by `sgttomas`, at
`2026-08-02T22:13:19Z`. The ordinary closeout comment is
[recorded on the PR](https://github.com/sgttomas/chirality/pull/478#issuecomment-5160591595).
No direct `main` push or check bypass occurred.
