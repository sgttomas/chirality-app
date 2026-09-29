# SCA-V4-001 checkpoint group 2 — accepted exact amendment and propagation plan

Recorded 2026-09-28 by node AK1, a Type 2 TASK (Claude Code subagent; no
delegation) dispatched by the HELP_HUMAN integrator of run
`APP-V4-BASIS-ALIGN-20260928`, which presented checkpoint A (K1). This record
transcribes the same owner act as the group-1 snapshot. One reply
addressed both subjects, and the owner accepted recording it in two snapshots
(OWNER_ITEMS O-24). It claims no inspection the owner did not perform.

## Custody of the act

Identical to `../SCA-V4-001_GROUP-1_2026-09-28/DECISION.md` "Custody of the
act": `AgentRuns/APP-V4-BASIS-ALIGN-20260928/OWNER_DECISIONS.md` (sha256
`cdc486801ae6315a8249459c3fd98cdc2d42390a178f5555b15c9fbee93d6d34`), section
"Checkpoint A: acceptance (owner, exact, 2026-09-28), DECISION-7", added by
commit `f4ba34c2ca80550fed012840e470dcbf5f2fedc3`; the owner's chat reply was
recorded verbatim there by the coordinating session.

## What the owner had in front of them

The packet revision 2 on the review page
https://claude.ai/artifact/3ek3uuPUR1v9jgpTjoF6ec (as recorded). For group 2
the subject is the exact amendment and the propagation plan:

- `AMENDMENT_PACKET/BASIS_AMENDMENT.md` (sha256
  `04bdc91622223510870ac8fe3994d708641c5e07a7853c5abc75ac59c0ed24cf`): the
  exact old → new text of Part A (the four basis documents, A01–A17) and
  Part B (the decomposition package D-01…D-16 and the `_CONTEXT.md` mirrors
  B7; the recompute rule B8), with the acceptance-conditional tokens;
- `AMENDMENT_PACKET/SOW_REVISIONS.md` (sha256
  `9b4d700ddc9d63d48135f84163f03eb8f1da99951ef813a84d17192515e7d27b`): the
  exact ScopeOfWork text for the 16 contracts;
- `AMENDMENT_PACKET/IMPACT_ASSESSMENT.md` (sha256
  `7fd523c26eb16a2d5bdf511c335c10403d7d7b2eb320601d72a5c0854e46348e`) §3.1
  (the proposed register and `ScopeChanging` values), §7 (supersession
  rows) and §9 (propagation-plan outline);
- `AMENDMENT_PACKET/OWNER_ITEMS.md` (sha256
  `2b90eb4a95f458e993eed69e27533aa10e31aea980fe2ec99c9c2345e6f498ef`) items
  O-3…O-7 and O-21…O-24.

## The owner's act (verbatim)

> "accept the remaining items as recommended"

No correction or exception was recorded.

## Interpretation (recording role's reading, not owner text)

| Item | Effect |
|---|---|
| O-3 | Write boundary as listed (the four docs; `SOFTWARE_DECOMP.md`, `ScopeLedger.csv`, `Vocabulary_Map.csv`, `Deliverables.csv`, `Consolidated_Coverage.csv`, `Packages.csv` (O-8), `Open_Issues.csv` (O-17); the `_CONTEXT.md` of DEL-02-03, DEL-05-01, DEL-09-07 and DEL-05-02; the 16 `ScopeOfWork.md` by `scope-of-work` MODE=REVISE only). Route: docs, decomposition and `_CONTEXT.md` edits applied as the candidate after K1; the 16 REVISE briefs only after group-3 acceptance |
| O-4 | V4-WF-05, V4-HI-42, V4-EXM-22 text (A01, A12, A15) and matching SoW and ledger edits |
| O-5 | V4-HOST-01, V4-ARC-11 text (A02, A08) |
| O-6 | V4-HOST-02 verbatim, V4-ARC-12, host-agent properties, V4-EXM-23 (A03, A09, A10, A16) |
| O-7 | Consequential edits A04, A05, A11, A13, A14, A07, A17 |
| O-8 | A06 and D-13 with the DEL-05-01/05-02 `_CONTEXT.md` mirrors |
| O-17 | D-14a/b; `Status` stays OPEN |
| O-21 | Supersession bindings typed `SUPERSESSION`; V4-WF-05 and V4-HI-42 rows note that the original holds again for workflows in the governance phase |
| O-22 | SoW frontmatter `decomposition_basis` unchanged (GROUP3) in all 16 SoWs |
| O-23 | `ScopeChanging` values as proposed in IMPACT_ASSESSMENT §3.1 |
| O-24 | Two decision snapshots for the one act; the group-2 snapshot binds `Amendment_Actions.csv` by hash |
| Acceptance-conditional edits | A07, A17a–c and D-15 carry `{ACCEPT_DATE}` (and D-15 `{AMENDMENT_SNAPSHOT}`), "filled from the accepted group-3 record" (BASIS_AMENDMENT header, D-15). They are applied only after group-3 acceptance |

The authoritative register is `Amendment_Actions.csv` (47 rows, all
`MODIFY`; `ScopeChanging` `YES` on 30; `SupersessionBindingPresent` `YES` on
22), bound in `ACCEPTED_MANIFEST.csv` with its role `action register`. It is
IMPACT_ASSESSMENT §3.1 with `{AMENDMENT_ID}` = `SCA-V4-001` and each
deliverable's `AffectedFiles` expanded to full repository paths, as §3.1
directs "at group-2 finalization". `Amendment_Preview.md`,
`Propagation_Plan.md` and `Supersession_Delta.csv` render the packet in the
scope-change layout; they were transcribed after the act, and the packet
files, also bound, govern.

No affected deliverable is CHECKING or ISSUED, so no register row authorizes a
reopening.

## What this acceptance authorizes and does not authorize

It authorizes checkpoint-group-3 preparation from this snapshot
(`ACCEPTED_GROUP2_DECISION_SNAPSHOT`):
- writing the candidate poststate: every Part A and Part B edit and the B7
  mirrors, except the acceptance-conditional A07, A17a–c and D-15;
- the B8 recompute of `Consolidated_Coverage.csv`;
- generating the candidate `Supersession_Map.csv` and
  `Post_Change_Coverage.json`, the post-change audit over the baseline's
  seven packages, and the independent review.

It does not authorize:
- A07, A17a–c or D-15;
- any `ScopeOfWork.md` edit (REVISE waits for group 3), any
  `Dependencies.csv`, `_DEPENDENCIES.md` or `_DAG` change;
- any `_STATUS.md` or lifecycle change;
- creating `_LATEST.md` or an accepted `SCA-*` snapshot.

## Basis

At the act (commit `f4ba34c2c`): the accepted decomposition
`_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z`; the working
package inputs hashed in `../../SCA-V4-001_2026-09-28_2155/Brief.md`, each
equal to the prefix recorded in BASIS_AMENDMENT "Basis"; the group-1 snapshot
`../SCA-V4-001_GROUP-1_2026-09-28/` (recorded from the same act).

Group-3 pointer posture: `FIRST_AMENDMENT`.
