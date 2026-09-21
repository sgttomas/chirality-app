# D-GOV-31 — Merge-Gate Policy Succession (adoption of Candidate B, shared-CHANGE scope)

Status:       RULED
HumanRuling:  "APPROVE D-GOV-31 15fba9c3 — Ryan Tufts 2026-07-29" (owner, 2026-07-29; recorded verbatim below)
AcceptedCandidateSHA: 3ad43c27bbab0da7d43cb1921ff9c8b186d1b2cd (the candidate-only commit containing the adopted subject)
CandidateSubjectSHA256: 15fba9c36a197b36b281297af123115bcd3f282fe6c6f2fae05cd703b3743748
SelectionRecordSHA: 482ec0b79e65e7302e2352bd4b04a54d41429f1b (the commit recording the owner's SELECT act in the run HANDOFF_STATE)
CandidateMergeSHA: ea3db3607fbcbb7ce5f65bab31268a7eca431adb (merge of PR #416 into `main`, 2026-07-29; backfilled by the Step-4 propagation tranche per the D-GOV-18/19/21/22 convention)
PublicationSHA: ea3db3607fbcbb7ce5f65bab31268a7eca431adb (the same merge publishes this record; backfilled by the same tranche)
EffectiveSHA: ea3db3607fbcbb7ce5f65bab31268a7eca431adb (merge of PR #416 into `main`, 2026-07-29; the adopted Rev 7 bytes became live at this commit; backfilled by the same tranche)
Date:         2026-07-29
FramedBy:     HELP_HUMAN session of record (Agent 0); authored by bounded Agent 2 AUTHOR run `GOV-STEP3-D8-ADOPTION-20260729` under the HELPS_HUMANS lane
AcceptedBasis: `main@4f7808acb2802443370d045efa198152934c1674`
RecordConvention: exact-candidate-SHA; supersede-never-edit after ruling; publication/effective SHA backfill follows the established D-GOV-18/19/21/22 convention
DecisionKey:  `merge_gate_policy_succession`
CandidatePacket: `docs/governance_harness/_PROPOSALS/D-GOV-31_2026-07-29_merge_gate_policy_succession/PACKET.md`

## Status note

This record is RULED. Git closeout remains pending: `CandidateMergeSHA`,
`PublicationSHA`, and `EffectiveSHA` are backfilled after the human-gated
PR merge, per the D-GOV-18/19/21/22 convention. The adopted subject is the
Candidate B PRD revision
`docs/governance_harness/_PROPOSALS/D-GOV-31_2026-07-29_merge_gate_policy_succession/CANDIDATE_B_SHARED_CHANGE/PRD_ROOT_REV7_CANDIDATE.md`,
SHA-256
`15fba9c36a197b36b281297af123115bcd3f282fe6c6f2fae05cd703b3743748`
(token SHA8 = `15fba9c3`), within candidate commit
`3ad43c27bbab0da7d43cb1921ff9c8b186d1b2cd` on candidate basis
`main@4f7808acb2802443370d045efa198152934c1674`. The packet governs on any
disagreement with this summary.

This publication itself runs under the still-current D-8. The packet's §6
pipeline discipline, verbatim:

> **Publication runs under the still-current D-8**: the adoption and
> application PR is human-gated and is not self-merged. The successor
> never consumes its own not-yet-effective merge exception.

## Selection and pipeline recap

The owner selected Candidate B in-session on 2026-07-29, against the
packet's pre-fixed identities; the selection was recorded in the run
HANDOFF_STATE at commit `482ec0b79e65e7302e2352bd4b04a54d41429f1b`.
Selection was not adoption. The owner's return, verbatim:

<!-- BEGIN OWNER SELECTION VERBATIM -->
SELECT CANDIDATE-B — Ryan Tufts 2026-07-29
<!-- END OWNER SELECTION VERBATIM -->

Candidate A (`CANDIDATE_A_ROOT_ONLY/`, subject SHA-256
`d21a2d8d4bc2deb2a32dbe4936f1e4647efabac24158adeae4f45fa4a18d8d35`) was
not selected and is not adopted.

### HZN-GOV-01 rerun (pre-adoption)

Per the packet's §6 pipeline, HZN-GOV-01 was rerun against the exact
committed candidate before adoption. Verdict:
**ADOPTION_CLEAR_WITH_NOTES** — no blocking finding. The full return
lives in the Agent 0 session record; the run HANDOFF_STATE carries a
summary. Prior-finding dispositions: HZN-GOV-001, HZN-GOV-003,
HZN-GOV-004, HZN-GOV-005, HZN-GOV-006, and HZN-GOV-007 RESOLVED;
HZN-GOV-002 partially resolved with a nonblocking residual (RB-1).

New nonblocking notes RB-1..RB-8, with their recorded dispositions:

- **RB-1** — residual of HZN-GOV-002: the successor policy leaves
  "self-merge" undefined for downstream reconciliation, and the
  changed-surface census misses `DEL-04-06/_CONTEXT.md` (lines 11, 21).
  Disposition: the definitional residual is cured in this record
  (Effect 3); the census gap is a Step-4 obligation — the POLICY_DELTA
  §4 row-2 surface list gains `DEL-04-06/_CONTEXT.md` at drafting.
- **RB-2** — grant recording and authorship for PR-carried grants.
  Disposition: Step-4 drafting preference — grants recorded strictly
  before exercise preferred, owner-authored when PR-carried.
- **RB-3** — the mandatory pre-merge pin lacks a registered home.
  Disposition: Step-4 obligation — a tranche-manifest grant-reference
  field is the pin's registered home, carried in the rows-4–6 tools
  tranche.
- **RB-4** — binding of the adoption token to the exact subject.
  Disposition: cured by the adoption token itself carrying the subject
  SHA8 (`15fba9c3`), recorded here.
- **RB-5** — wording of the LOOP_INIT/AGENT_CHANGE amendments.
  Disposition: Step-4 drafting preference — "local merge discipline
  remains controlling" wording when those surfaces are amended.
- **RB-6** — deterministic-check coverage under the successor policy.
  Disposition: Step-4 obligation — the rows-4–6 tools tranche restates
  the full deterministic-check suite.
- **RB-7** — confirmed that no retroactive-legitimization pathway
  exists. No disposition required.
- **RB-8** — the PACKET §3 OWNER_DECLARED intent quote's verbatim status
  self-disclosed UNKNOWN pending owner confirmation at adoption.
  Disposition: resolved by confirmation-by-non-objection at adoption
  (next paragraph).

### §3 intent-quote confirmation

Before adoption, the supervising session presented the owner with: "one
confirmation rides along: the PACKET §3 OWNER_DECLARED intent quote … the
record will mark it owner-confirmed at adoption unless you say
otherwise." The owner returned the adoption token without objection. The
§3 intent quote is therefore recorded as confirmed by non-objection at
adoption, with the presentation quoted above. This is expressly not an
independent verbatim re-attestation by the owner.

## Recorded ruling

The owner adopted in-session on 2026-07-29, returning one line to the
Agent 0 session of record. It is recorded verbatim (51 bytes UTF-8,
SHA-256
`906efafcea5e842dbfb544c5d139a53572bcba7cbf7f2c8a392a2e3d70bccb2b`):

<!-- BEGIN OWNER RULING VERBATIM -->
APPROVE D-GOV-31 15fba9c3 — Ryan Tufts 2026-07-29
<!-- END OWNER RULING VERBATIM -->

## Effects

1. **Adoption and supersession.** Candidate B is adopted. On the
   publication merge becoming effective, `docs/PRD_ROOT.md` Revision 7
   (subject SHA-256
   `15fba9c36a197b36b281297af123115bcd3f282fe6c6f2fae05cd703b3743748`)
   supersedes the prior Rev 6 D-8 row ("never self-merge"), and annex
   §5.3.1 — bounded owner grants; the four closeout identities (semantic
   approval, approved source SHA, merge authorization, effective merge
   SHA); the owner token grammar; the express exclusions; K-MERGE-1
   unchanged with strengthened pre-merge evidencing — becomes the live
   merge-gate policy with shared-CHANGE scope.
2. **Default unchanged; no grant.** The default remains human-gated
   permission-required. No grant is issued, exercised, or pre-approved by
   this record.
3. **RB-1 residual cure** — carried as record-level interpretive guidance
   to §5.3.1: a bounded grant MAY name the same actor as authoring actor
   and merge executor; and for downstream reconciliation, "self-merge" is
   defined as: a merge whose merge executor is the authoring actor of the
   merged content, lawful only under a bounded owner grant recorded per
   §5.3.1 and still requiring the per-merge human approval vehicle bound
   to the exact source HEAD.
4. **Step-4 propagation obligations — enumerated, not performed.** The
   nine POLICY_DELTA §4 propagation rows attach as Step-4 obligations:
   (1) root scope ledger SOW-042 restatement — SCOPE_CHANGE; (2)
   DEL-04-06 ScopeOfWork reconciliation — downstream contract owner via
   WORKING_ITEMS; (3) `execution/_Coordination/LOOP_INIT.md` §7
   amendment — HELPS_HUMANS via a human-gated M2 tranche; (4)
   `tools/validation/validate_instruction_tranche_manifest.py` G4-check
   extension — HELPS_HUMANS via a human-gated tools tranche; (5) its
   test update — same tranche as row 4; (6) tranche-manifest schema
   semantics for declaring a bounded grant — HELPS_HUMANS; (7)
   practitioner-harness K-MERGE-1 mapping verification — HELPS_HUMANS;
   (8) `agents/AGENT_CHANGE.md` reconciliation under the agent-index
   change-notice rule — HELPS_HUMANS; (9) routed M6 notices to every
   registered loop — Agent 0 / HELPS_HUMANS. The RB-derived additions
   also attach: the row-2 surface list gains `DEL-04-06/_CONTEXT.md`
   (lines 11, 21); the rows-4–6 tools tranche carries the mandatory
   pre-merge pin's registered home (a tranche-manifest grant-reference
   field) and restates the full deterministic-check suite; and the
   LOOP_INIT/AGENT_CHANGE amendments prefer the "local merge discipline
   remains controlling" wording and grants recorded strictly before
   exercise (owner-authored when PR-carried). POLICY_DELTA §4's express
   non-obligation stands: SHA-pinned historical mirrors, frozen proposal
   and evidence packages, receipts, and OD transcription records are not
   rewritten.
5. **M6 notices obligated.** Routed coordination notices to every
   registered loop (app-dev, pec, piping) are obligated as Step-4 work.
   Notices are coordination, never authority; each loop's stricter local
   merge discipline remains controlling until that loop adopts or
   acknowledges the policy under its own instruments.

## Scope limits

This ruling does not:

- retroactively cure, excuse, or reclassify the 2026-07-28 merge window;
  the D-GOV-30 framing is preserved — the disclosed exceptions remain
  exceptions;
- issue, exercise, or pre-approve any grant;
- rule any loop-local substance — App, PEC, and Piping are bound only
  through their own instruments and acts;
- perform any Step-4 write — every propagation obligation above is
  enumerated only;
- create lifecycle, implementation, activation, runtime, dependency,
  decomposition, scope, estimate, schedule, repin, release, or
  professional-reliance authority; or
- adopt anything from Candidate A, which remains an unselected frozen
  proposal, superseding nothing.

## Merge-execution note (2026-07-29, appended at backfill)

CI green and 11/11 independent verification preceded the merge. The owner
returned in-session, verbatim, `Merge PR #416 and then proceed accordingly.`
(2026-07-29) and, after the session surfaced the tension with the
still-current D-8, reiterated the direction; the merge was thereupon executed
by the supervising agent session via the owner-authenticated `gh` CLI (GitHub
merge actor `sgttomas`), effective merge
`ea3db3607fbcbb7ce5f65bab31268a7eca431adb`. This was an owner-directed
execution disclosed against the PACKET §6 publication expectation
("human-gated and is not self-merged") — disclosed, not cured, and not
precedent.
