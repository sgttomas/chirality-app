# D-GOV-32 — Adoption of the Chirality Task Management PRD (Revision 2)

Status:       RULED
HumanRuling:  "The PRD is accepted." (owner, 2026-07-31, in-session; recorded verbatim below with its carrying direction)
AcceptedCandidateSHA: 584319dc9 (the commit carrying the adopted PRD bytes, merged to `main` via PR #423)
CandidateSubjectSHA256: 97e2ae6525ecbfdc52ff22aee85e1182a751c1090c2aa2f52faaf9e080f35d18 (`plans/chirality-task-management/PRD_CANDIDATE_2026-07-31.md`, Revision 2)
CandidateMergeSHA: c1156837f9559038d8a1fc1e1b37fb3c5f9aeb0b (merge of PR #423 into `main`, 2026-07-31; the adopted bytes became repository state at this commit, harness green)
PublicationSHA: 1c80a2bc1b2631039149b0fb75dffa3550c583aa (merge of PR #424 into `main`, 2026-07-31, publishing this record; backfilled by the Stage-A step-0 tranche per the D-GOV-18/19/21/22/31 convention)
EffectiveSHA: 1c80a2bc1b2631039149b0fb75dffa3550c583aa (same merge; this record's adoption status became repository state at the PR #424 merge — the adopted PRD bytes were already live at CandidateMergeSHA `c1156837f`; backfilled by the Stage-A step-0 tranche)
Date:         2026-07-31
FramedBy:     HELP_HUMAN session of record (Agent 0), the same 2026-07-31 working session that ran the fresh PRD inquiry, the four-lens architecture review, and the Rev 1 → Rev 2 restructuring
AcceptedBasis: `main@a7371ed94` (inquiry and review basis) → `main@c1156837f` (adopted bytes on main)
RecordConvention: exact-candidate-SHA; supersede-never-edit after ruling; publication/effective SHA backfill follows the established convention
DecisionKey:  `task_management_prd_adoption`
Subject:      `plans/chirality-task-management/PRD_CANDIDATE_2026-07-31.md` (Revision 2), with the supporting review record `plans/chirality_task_management_architecture_review_2026-07-31.html` (same commit; evidentiary, not adopted as authority)

## Status note

This record is RULED. The adopted subject is the Chirality Task Management
PRD candidate, Revision 2, exactly as merged at PR #423 — file SHA-256
`97e2ae6525ecbfdc52ff22aee85e1182a751c1090c2aa2f52faaf9e080f35d18` within
commit `584319dc9`, effective on `main` at merge
`c1156837f9559038d8a1fc1e1b37fb3c5f9aeb0b`. The PRD file's own front-matter
status line (`NON_AUTHORITATIVE_PRD_CANDIDATE`) is superseded by this
record without editing the adopted bytes, per supersede-never-edit: the
candidate is adopted as the accepted product basis for Chirality Task
Management. On any disagreement between this summary and the PRD bytes,
the PRD bytes govern for product content and this record governs for
adoption status.

Provenance context, for the reader: the PRD was authored in a fresh
Agent 0 inquiry per the authoring basis
(`plans/chirality-task-management/PRD_AUTHORING_BASIS_2026-07-28.md` §12),
its source corpus verified by SHA-256 against
`plans/chirality-task-management/SOURCE_MANIFEST.md`, and its Revision 2
produced by the four-lens architecture review at frozen basis
`main@a7371ed94`, whose findings F-1..F-30 are dispositioned in PRD §20.
Two owner directions of record given in the same session are load-bearing
PRD text (work discovery and resolution remain development-loop-owned;
the register is a session-residue disposition ledger) and are quoted in
PRD §1.

## Recorded ruling

The owner ruled in-session on 2026-07-31, in two returns to the Agent 0
session of record.

Acceptance (60 bytes UTF-8, SHA-256
`696c326d07518934107b10cbdb91366cc3a02b6442015cb40f1cb52df7e53099`):

<!-- BEGIN OWNER RULING VERBATIM -->
commit this and open a PR for merging.  The PRD is accepted.
<!-- END OWNER RULING VERBATIM -->

Execution direction for this record (90 bytes UTF-8, SHA-256
`38264975f3231a2fb437236d3a79b76f39c1f53fe2c44f75ee8daabcc010fe64`):

<!-- BEGIN OWNER DIRECTION VERBATIM -->
merge it and draft the adoption record then open a PR for that and merge on this approval.
<!-- END OWNER DIRECTION VERBATIM -->

The acceptance was returned against the Revision 2 bytes as presented in
the session; the framing session bound it to the exact candidate SHA per
K-AUTH-2 at commit time (`584319dc9`), before merge. The second direction
supplies plan-bounded authority for exactly two merges: PR #423 (the
accepted PRD) and the PR carrying this record. Per the 07-28 hinge
guidance, its scope, SHA binding, merge authority, and exclusions are
stated in the Merge-execution note below; it expires on completion of
those two merges and grants nothing else.

## Effects

1. **Adoption.** The Chirality Task Management PRD, Revision 2, is
   adopted as the accepted product basis for Chirality Task Management.
   This is the "new product function" act that `docs/PRD_ROOT.md` OBJ-6
   requires for any aggregated cross-root coordination layer, performed
   at the owner's initiative by PRD act — never through decomposition or
   SOW prose.
2. **Stage-A follow-on obligations — enumerated, not performed.** Per PRD
   §23.1, the following owner-gated execution items attach to the root
   loop as the next work, each through its proper instrument:
   (a) the K-TM-1..6 rows entering `docs/CONTRACT.md` via a human-gated
   governed tranche; (b) minting the root-loop register home
   `execution/_Coordination/_TaskManagement/` and seeding it from the
   measured backlog (~115 items, PRD §17); (c) the root
   `execution/_Coordination/LOOP_INIT.md` reader-binding amendment;
   (d) the first owner triage session dispositioning the seed;
   (e) `taskmgmt` scan/validate v0 per PRD §9.
3. **Acknowledged PEC side-effect.** Adoption decides PEC PRD §16 open
   decision 1 (structure-at-source) for the Action Item register class
   specifically. A routed coordination notice to the PEC loop's
   coordination surface is obligated as Stage-A work; the notice is
   coordination, never authority, and PEC's own instruments govern any
   PEC-side reconciliation.
4. **Per-loop adoption preserved.** No loop other than the root loop is
   bound. App-dev, Piping, and PEC registers exist only after those
   loops' own rulings under their own fences (F-APP-5, F-PIP-5, D-PEC
   packet). Routed notices carrying the standard to each registered
   loop's coordination surface are obligated as Stage-B work.
5. **Invariant candidacy.** K-TM-1..6 (PRD §10) are adopted as product
   invariants of Task Management by this record; their entry into the
   ratified `docs/CONTRACT.md` catalog remains the Effect 2(a) governed
   tranche, not this record.

## Scope limits

This ruling does not:

- mint any directory, register, or file beyond this record and its
  register row — every Effect 2 item is enumerated only;
- amend `docs/CONTRACT.md`, `docs/SPEC.md`, any `agents/` instruction,
  any loop instrument, or the adopted PRD bytes;
- create decomposition, packages, deliverables, lifecycle, estimates,
  schedule, implementation, release, or professional-reliance authority;
- bind App-dev, Piping, PEC, or Tier-0 — each is bound only through its
  own instruments and acts;
- adopt the architecture review HTML as authority (it remains a
  derivative, non-governing record per its own footer); or
- grant any merge authority beyond the two merges named in the recorded
  direction.

## Merge-execution note (2026-07-31)

The owner directed, verbatim above, that PR #423 and this record's PR be
merged on this approval. PR #423 was merged first (harness green,
auto-merge on checks passing), effective
`c1156837f9559038d8a1fc1e1b37fb3c5f9aeb0b`. This record's PR is merged
under the same direction by the supervising agent session via the
owner-authenticated `gh` CLI (GitHub merge actor `sgttomas`), consistent
with the PRD_ROOT Rev 7 §5.3.1 merge-gate policy: the owner's direction
above is the semantic approval and merge authorization; the approved
source SHA and effective merge SHA are backfilled by the Stage-A tranche
per convention. The authoring actor and merge executor are the same agent
session under an express owner grant bounded to these two merges.
