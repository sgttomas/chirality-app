# D-GOV-34 — Clean-Basis Branch and Worktree-Lane Creation Is Routine CHANGE Execution

Status:       RULED — CANDIDATE IMPLEMENTATION PREPARED; PUBLICATION PENDING
HumanRuling:  "Mint D-GOV-34 — I rule that clean-basis branch/worktree-lane creation is routine CHANGE execution and dirty-basis lanes remain non-routine, confirming my 2026-07-19 ruling (App LOOP_RECEIPTS.md Receipt-74 Owner-Direction). D-GOV-34 binds exactly the TM-ROOT-124 amendment to agents/AGENT_CHANGE.md §Routine closeout, its G4 tranche manifest, and routed notices to the App, Piping, and domain-engine loops. It grants nothing else."
Date:         2026-08-21
FramedBy:     HELP_HUMAN managed run `ROOT_DEL0206_ACCEPTANCE_DGOV34_2026-08-21`
AcceptedBasis: `main@33e871fc38d8ef4bb51f7c25cdc6ca2e8dcb69e0`
RecordConvention: owner ruling recorded before publication; candidate, publication, and effective SHAs remain `TBD` until their respective Git acts
DecisionKey:  `change_clean_basis_lane_routine`
Supersedes:   none
CandidateSHA: 8e704f2b63302c8568c48f8fee7c4681e3ec4262
PublicationSHA: d1a53697e6b7f54dcdb5862357bd0b395f51fff2
EffectiveSHA: 9f95250e4091a789ca82fb207deec6471d7044d1

## Recorded ruling

The owner ruled in-session on 2026-08-21:

<!-- BEGIN OWNER RULING VERBATIM -->
Mint D-GOV-34 — I rule that clean-basis branch/worktree-lane creation is routine CHANGE execution and dirty-basis lanes remain non-routine, confirming my 2026-07-19 ruling (App LOOP_RECEIPTS.md Receipt-74 Owner-Direction). D-GOV-34 binds exactly the TM-ROOT-124 amendment to agents/AGENT_CHANGE.md §Routine closeout, its G4 tranche manifest, and routed notices to the App, Piping, and domain-engine loops. It grants nothing else.
<!-- END OWNER RULING VERBATIM -->

The authoritative chat transcription is
`execution/_Coordination/AgentRuns/ROOT_DEL0206_ACCEPTANCE_DGOV34_2026-08-21/OWNER_DIRECTION_TRANSCRIPT_2026-08-21.md`.
The earlier confirming evidence is App
`projects/chirality-app-dev/loop/LOOP_RECEIPTS.md` Receipt-74
Owner-Direction: simple branch creation from a verified clean exact basis was
classified as completely routine. This record is the new Root governance act;
the App receipt remains evidence and is not substituted for a Root ruling.

## Decision

For CHANGE, creation of a task branch and, when isolation is warranted, its
worktree lane is routine execution when all of these clean-basis conditions
hold:

1. the exact integration-branch base is verified and its full commit SHA is
   recorded;
2. the source status is clean; and
3. no Git operation is in progress.

CHANGE reports the branch or lane name and base SHA and proceeds without an
`APPROVE:` token. Basing a lane on a dirty worktree, or any switch that would
discard or carry uncommitted work, remains non-routine and requires the
applicable approval gate.

## Bound implementation

This ruling binds exactly:

- the TM-ROOT-124 amendment within `agents/AGENT_CHANGE.md` §Routine closeout;
- G4 tranche manifest
  `docs/governance_harness/tranche_manifests/ROOT-TM124-CHANGE-ROUTINE-BRANCH-20260821.yaml`,
  whose `basis:` is the verified 40-character AcceptedBasis commit; and
- routed coordination notices to the App, Piping, and domain-engine loops.

The notices are coordination, never authority. Each receiving loop owns any
adoption, amendment, decline, deferral, current-corpus regeneration, or
SHA-pin follow-on under its own instruments and cadence.

## Scope limits

D-GOV-34 grants nothing beyond the bounded implementation above. In
particular, it does not:

- make dirty-basis lane creation routine;
- make a branch or worktree switch routine when it would discard or carry
  uncommitted work;
- authorize merge, rebase, reset, force push, cleanup, history rewrite,
  destructive action, or any other state-changing action;
- change human ownership of governance, semantic acceptance, issuance,
  integration, release, or reliance decisions;
- change any receiving loop's local discipline or write any foreign register;
  or
- authorize product implementation, lifecycle change, release, publication,
  professional reliance, or merge of this tranche.

## Publication posture

The owner ruling is recorded, and its bounded candidate implementation is
prepared on the AcceptedBasis. It becomes shared repository state only after
the exact validated source is published through the separately governed PR
path. `CandidateSHA`, `PublicationSHA`, and `EffectiveSHA` remain `TBD` until
their respective Git acts; this record does not invent or self-cite a commit.
