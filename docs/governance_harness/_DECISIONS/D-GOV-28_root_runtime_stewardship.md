# D-GOV-28 — Root Runtime Stewardship PRD Amendment

Status:       RULED
HumanRuling:  "APPROVE: D-GOV-28 Option O-A." (owner, 2026-07-26; full ruling recorded verbatim below)
AcceptedCandidateSHA: f78a83621cbd679e6af2c41199845aca74073480
CandidateSubjectSHA256: 0e36a03abc16b86f99024aa2a17c467ae7f4303f9740be3a6ba2e9dd1dfb2f2d
CandidateMergeSHA: 7553735922e2c72b38782a4a36bc3340226afd70
PublicationSHA: c2d727b2c8a8909691c03eb3f3b31b778c269215
EffectiveSHA: fb0b3d247d32e643a7fbb994d2f61b9b673ad0fb (merge of PR #364 into `main`, 2026-07-26, performed at explicit owner direction; backfilled by this closeout tranche)
Date:         2026-07-26
FramedBy:     Agent-drafted by HELP_HUMAN (Agent 0) from the accepted program-architecture evaluation and OD-2 Option A
AcceptedBasis: `main@18e5dda568689daadaa05aff65bd4b810489409b`
DecisionKey:  `root_runtime_stewardship_prd_amendment`
RecordConvention: exact-candidate-SHA; supersede-never-edit after ruling; publication/effective SHA backfill follows the established D-GOV-18/19/21/22 convention
CandidatePacket: `docs/governance_harness/_PROPOSALS/D-GOV-28_root_runtime_stewardship/PACKET.md`

## Status note

This record is RULED. The owner approved **O-A — Adopt the exact Rev 6
candidate** against commit
`f78a83621cbd679e6af2c41199845aca74073480`. The adopted subject is
`PRD_ROOT_REV6_CANDIDATE.md` at SHA-256
`0e36a03abc16b86f99024aa2a17c467ae7f4303f9740be3a6ba2e9dd1dfb2f2d`.
The packet at the AcceptedCandidateSHA governs on any disagreement with this
summary.

The Chirality Root PRD Revision 6 is adopted. The adopted status is carried by
this decision record, not by the PRD file. O-11 is now an adopted Root product
requirement. The ten D-GOV-20 architecture statements and the two SPEC O-1
sentences remain transcriptions of their already ruled sources; adoption does
not mint new authority for them.

## Recorded ruling

The owner ruled in-session on 2026-07-26:

<!-- BEGIN OWNER RULING VERBATIM -->
APPROVE: D-GOV-28 Option O-A. Adopt the exact Root PRD Revision 6 candidate contained in commit f78a83621cbd679e6af2c41199845aca74073480 and identified by SHA-256 0e36a03abc16b86f99024aa2a17c467ae7f4303f9740be3a6ba2e9dd1dfb2f2d. O-11 becomes an adopted Root product requirement. Publish the D-GOV-28 decision record and apply the accepted Revision 6 bytes to docs/PRD_ROOT.md through the required M2/CHANGE closeout.

This adoption does not amend the Root decomposition, create a deliverable or write locus, approve any SCOPE_CHANGE gate, change App or PEC scope, repin any contract, or authorize implementation. Root SCA-001 may advance beyond its confirmed Gate 1 only after the adoption is durably applied, and each remaining gate still requires its own explicit approval.
<!-- END OWNER RULING VERBATIM -->

## Effects

1. The exact Rev 6 bytes are the adopted Root PRD basis.
2. O-11, **Continuing Root stewardship of the generic runtime**, takes effect
   as a Root product requirement supporting OBJ-1, OBJ-2, OBJ-4, and OBJ-7.
3. Consequential generic `runtime/` semantics require a Root-owned scope
   carrier and declared write locus, with D-GOV-20 authority, security,
   residency, exclusion, and implementation-gate boundaries preserved.
4. App, PEC, and other clients do not acquire ownership of generic runtime
   semantics through their implementation work.
5. The six candidate open items remain OPEN or PROPOSED. Adoption supplies no
   unstated answer to them.
6. Root SCA-001 becomes eligible to proceed from its confirmed Gate 1 only
   after this tranche reaches its EffectiveSHA. Gates 2–5 remain separately
   human-gated.

## Scope limits

This ruling does not:

- amend the accepted Root decomposition or its registers;
- create, allocate, rename, or remove a package, deliverable, or scope item;
- create a `runtime/` write locus or authorize runtime implementation;
- approve any Root or App SCOPE_CHANGE gate;
- change App or PEC scope;
- repin any contract or accepted basis;
- rule any D-GOV-28 open item; or
- authorize release, issuance, or professional reliance.

## M2 application tranche

The separately human-gated application PR contains:

- this immutable decision record and its register entry;
- the exact accepted Rev 6 bytes at `docs/PRD_ROOT.md`;
- `ROOT-PRD-REV6-20260726.yaml`, recording M2 authorization, the serialized
  integration owner, the human merge gate, and M6 routing;
- narrow coordination notices to the App and PEC loops;
- regenerated public-export manifest and report derivatives; and
- validation evidence reported by CHANGE.

The proposal package remains immutable. PublicationSHA is the first commit
that publishes this record and applies the adopted bytes; it is backfilled
once in the same PR under the established SHA-backfill convention.
EffectiveSHA remains pending until the owner separately approves and Git
records the human-gated PR merge.
