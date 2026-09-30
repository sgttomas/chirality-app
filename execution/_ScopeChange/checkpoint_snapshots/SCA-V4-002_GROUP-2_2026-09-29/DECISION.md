# SCA-V4-002 checkpoint group 2 — accepted exact amendment and propagation plan

Recorded 2026-09-29 by node AK1, a Type 2 TASK (Claude Code subagent; no
delegation) dispatched by the coordinating session of run
`APP-V4-SCA002-20260929`, which presented checkpoint A (K1). This record
transcribes the same owner act as the group-1 snapshot. One reply addressed
both subjects; it is recorded in two snapshots, as for SCA-V4-001. It claims
no inspection the owner did not perform.

## Custody of the act

Identical to `../SCA-V4-002_GROUP-1_2026-09-29/DECISION.md` "Custody of the
act": `AgentRuns/APP-V4-SCA002-20260929/OWNER_DECISIONS.md` (sha256
`2a1d24c1d8698868d5f8a93a66c52d2e3cf2239ef22094ea938fdf8624b7cf95`), section
"Checkpoint A: SCA-V4-002 scope-change groups 1 and 2 (owner, exact,
2026-09-29), DECISION-2", added by commit
`f061cf61efb3d21ec1601dbb7a012be5b9ad1be1`; the owner's chat reply was
recorded verbatim there by the coordinating session.

The timing disclosure in the group-1 `DECISION.md` applies to this record
too: the owner decided while the pre-change baseline was still running, and
the baseline then found nothing that changes the packet.

## What the owner had in front of them

The packet (commit `f05bd1bbd`) on the review page
https://claude.ai/artifact/QQmWJoHTRfkXriBs66ghNS (as recorded). For group 2
the subject is the exact amendment and the propagation plan:

- `AMENDMENT_PACKET/BASIS_AMENDMENT.md` (sha256
  `091871fd90283b27b2d067c1eeb3137e3cf8f9d50dab87ad92a9b871cc634238`): the
  exact old → new text of A-01, B-01…B-06, C-01 and C-02, and the Part D
  supersession rows, with the slot rules for the acceptance-conditional
  edits;
- `AMENDMENT_PACKET/SOW_REVISIONS.md` (sha256
  `440d4d50abd4d6bd2a639cfb2bcaa8bcc83a6c94061a27f9fc91e67c6a12d00d`): the
  exact ScopeOfWork text for the nine contracts (26 blocks);
- `AMENDMENT_PACKET/ARC_EFFECT.md` (sha256
  `4b3aeec0f041266dce0e2fae754c129d4473ff8c3268c0b5c638529c6951ddc0`) §2 (the
  sentences) and §4 (the expected DAG-003 departure);
- `AMENDMENT_PACKET/IMPACT_ASSESSMENT.md` (sha256
  `46444eab11d7af768484e3996a6be784a9448b5960cc0c7197fd6533fd830456`) §3.2
  (the proposed register, `ScopeChanging` and `SupersessionBindingPresent`
  values) and §7 (the propagation plan and its sequence);
- `AMENDMENT_PACKET/OWNER_ITEMS.md` (sha256
  `1d46458c966b6cc41be361eb2ddbc75df409bcc43202aff17478b81438ca51a8`) items
  Q-3, Q-8, Q-9 and Q-14, and the exact text behind Q-4, Q-6, Q-7 and Q-10
  to Q-13.

## The owner's act (verbatim)

> "accept the remaining items as recommended"

No correction or exception was recorded.

## Interpretation (recording role's reading, not owner text)

| Item | Effect |
|---|---|
| Q-3 | Write boundary: exactly the `AffectedFiles` of the 16-row register, plus the SCA-V4-002 snapshot folders and pointers. Route: the docs, decomposition and `_CONTEXT.md` edits go into the candidate; the SoWs change only after group 3, by `scope-of-work` REVISE, one per brief, with `STATUS_POLICY=NO_STATUS_TOUCH`; then the register UPDATE, the currency audit and DAG-003. `ScopeChanging` `YES` only for DEL-10-03; `SupersessionBindingPresent` `YES` only for row 14 |
| Q-4 | The two drafted sentences (ARC_EFFECT §2; SOW_REVISIONS F-0201-01, F-0203-01), applied by REVISE |
| Q-5 | Option A; BASIS_AMENDMENT B-03 makes no edit |
| Q-6 | SOW_REVISIONS F-0402-01…02 and F-0101-01…02, applied by REVISE |
| Q-7 | B-02: the OI-012 `Consequence` value; `Status` stays OPEN |
| Q-8 | A-01 as a line break (not a blank line) |
| Q-9 | C-01: `_ScopeChange/_LATEST.md` in SPEC §11.2 form at the group-3 pointer move; V13 F1 disclosed in `Brief.md`, not rewritten |
| Q-10 | Part D: 17 `DL-SCA-V4-001-…` rows in SCA-V4-002's `Supersession_Delta.csv`; the map re-accumulated from SCA-V4-001's map |
| Q-11 | B-05a and B-05b, with the D-014 row |
| Q-12 | B-06a, B-06b and B-06c. B-06a is timed with the SoW REVISEs, because the file is bound in DAG-002's source manifest |
| Q-13 | C-02, written after group 1; cited by C-01 at the pointer move |
| Q-14 | Each decision snapshot is committed before the next stage uses it |
| Acceptance-conditional edits | B-04 (`{ACCEPT_DATE}`, `{AMENDMENT_SNAPSHOT}` and the five clause slots) and C-01. They are applied only after group-3 acceptance |

The authoritative register is `Amendment_Actions.csv` (16 rows, all
`MODIFY`; `ScopeChanging` `YES` on 1; `SupersessionBindingPresent` `YES` on
1; `DownstreamReruns` comma-separated), bound in `ACCEPTED_MANIFEST.csv`
with its role `action register`. It is the IMPACT_ASSESSMENT §3.2 block with
`{AMENDMENT_ID}` = `SCA-V4-002`; no row was dropped, because the owner
declined no item, so no row is renumbered. The packet's draft (tokens
unfilled) has sha256 `dafa622e…af13`, which the §3.2 block reproduces.

`Supersession_Delta.csv` is the BASIS_AMENDMENT Part D block with
`{AMENDMENT_ID}` = `SCA-V4-002` and `{D_SEQ_DEL0401}` = `D-014` (18 rows).
The packet's draft (tokens unfilled) has sha256 `a14c4dd1…b04e`, which the
Part D block reproduces.

`Amendment_Preview.md` and `Propagation_Plan.md` render the packet in the
scope-change layout. All four files were transcribed after the act and
before application; the owner did not review these renderings. The packet
files, also bound, govern.

No affected deliverable is CHECKING or ISSUED, so no register row authorizes
a reopening.

## What this acceptance authorizes and does not authorize

It authorizes checkpoint-group-3 preparation from this snapshot
(`ACCEPTED_GROUP2_DECISION_SNAPSHOT`):
- writing the candidate poststate: A-01, B-02, B-05a, B-05b, B-06b and
  B-06c;
- the B-01 recompute of `Consolidated_Coverage.csv`;
- generating the candidate `Supersession_Map.csv`, the post-change audit over
  the baseline's seven packages, and the independent review.

It does not authorize, before group-3 acceptance:
- B-04 or C-01;
- B-06a (timed with the SoW REVISEs);
- any `ScopeOfWork.md` edit (REVISE waits for group 3), or any
  `Dependencies.csv`, `_DEPENDENCIES.md` or `_DAG` change;
- any `_STATUS.md` or lifecycle change, or any `Coverage_Telemetry.json`
  write;
- moving `_LATEST.md` or marking an accepted `SCA-*` snapshot.

## Basis

At the transcription (`HEAD` `39c97257ba5c354cff31f14487c05b538e806197`):
the accepted decomposition GROUP3 as amended by the accepted predecessor
`_ScopeChange/SCA-V4-001_2026-09-28_2155/`; the working package inputs hashed
in `../../SCA-V4-002_2026-09-29_1901/Brief.md`; the group-1 snapshot
`../SCA-V4-002_GROUP-1_2026-09-29/` (recorded from the same act). No
SCA-V4-002 edit had been applied when this snapshot was written.

Group-3 pointer posture: `ACCEPTED_PREDECESSOR`.
