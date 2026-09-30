# SCA-V4-002 checkpoint group 1 — accepted proposed change and impact

Recorded 2026-09-29 by node AK1, a Type 2 TASK (Claude Code subagent; no
delegation) dispatched by the coordinating session of run
`APP-V4-SCA002-20260929`, which presented checkpoint A (K1) to the owner.
This record transcribes the owner's act as it is recorded in the run's
`OWNER_DECISIONS.md`. It is not a new request for the same decision, and it
claims no inspection the owner did not perform.

## Custody of the act

| Item | Value |
|---|---|
| Record | `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-SCA002-20260929/OWNER_DECISIONS.md`, section "Checkpoint A: SCA-V4-002 scope-change groups 1 and 2 (owner, exact, 2026-09-29), DECISION-2" |
| Record sha256 at transcription | `2a1d24c1d8698868d5f8a93a66c52d2e3cf2239ef22094ea938fdf8624b7cf95` |
| Commit that added DECISION-2 | `f061cf61efb3d21ec1601dbb7a012be5b9ad1be1` ("docs(app-v4): SCA-V4-002 checkpoint A accepted (groups 1-2)", 2026-09-29 18:53:37 -0600; it changes only that file) |
| Channel | The owner's reply in chat to the coordinating session, which recorded it verbatim in the record above. AK1 did not observe the chat; it relies on that record |
| Earlier direction | "Direction to start" (same record): "Proposal accepted.  Proceed accordingly." It started the undertaking and accepted neither group |

## Timing disclosure

DECISION-2 records this, and it is restated here as the record gives it:

- The owner decided while the pre-change `audit-decomp` baseline (node P3,
  method step 5) was still running. The baseline had been interrupted by a
  connection error and resumed.
- The group-1 snapshot is written only after the baseline completes.
- If the baseline finds anything that changes the packet, the owner is told
  before application.

What happened afterwards, from the run's `DISPATCH.md` and `BASELINE/`:

- The baseline completed and was committed at `39c97257b` (2026-09-29
  18:57:11 -0600), after the act was committed at `f061cf61e` (18:53:37).
  Its result is 0 BLOCKER, 38 WARNING (all pre-existing), 101 INFO.
- `DISPATCH.md` row P3 records: "No finding changes the accepted packet".
- This snapshot was written after that commit, and before any SCA-V4-002
  edit was applied.

So the owner did not have the baseline's result in front of them at the act.
The pre-change baseline bound in `ACCEPTED_MANIFEST.csv` is execution
evidence that completed after the act; it is not a human-reviewed artifact.

One baseline finding concerns the packet's wording and changes no edit:
IMPACT_ASSESSMENT §4 names six packages for the baseline, and the baseline
used seven (PKG-05 added, because register row 16 edits the `_CONTEXT.md` of
DEL-05-01 and DEL-05-02). The accepted packet bytes are not changed. Whether
the owner has been told of this finding is for the coordinating session to
record; AK1 has no record of it beyond `DISPATCH.md`.

## What the owner had in front of them

As recorded in `OWNER_DECISIONS.md` (DECISION-2 "Context"): the owner
reviewed the packet (commit `f05bd1bbd`) on the review page
https://claude.ai/artifact/QQmWJoHTRfkXriBs66ghNS. The record gives the
packet hashes by prefix; each matches the committed packet file in full:

| Packet file | Recorded prefix | Full sha256 |
|---|---|---|
| `AMENDMENT_PACKET/OWNER_ITEMS.md` | `1d46458c…` | `1d46458c966b6cc41be361eb2ddbc75df409bcc43202aff17478b81438ca51a8` |
| `AMENDMENT_PACKET/IMPACT_ASSESSMENT.md` | `46444eab…` | `46444eab11d7af768484e3996a6be784a9448b5960cc0c7197fd6533fd830456` |
| `AMENDMENT_PACKET/BASIS_AMENDMENT.md` | `091871fd…` | `091871fd90283b27b2d067c1eeb3137e3cf8f9d50dab87ad92a9b871cc634238` |
| `AMENDMENT_PACKET/SOW_REVISIONS.md` | `440d4d50…` | `440d4d50abd4d6bd2a639cfb2bcaa8bcc83a6c94061a27f9fc91e67c6a12d00d` |
| `AMENDMENT_PACKET/ARC_EFFECT.md` | `4b3aeec0…` | `4b3aeec0f041266dce0e2fae754c129d4473ff8c3268c0b5c638529c6951ddc0` |

The files at `f05bd1bbd` and at the transcription are byte-identical. The
record states that the recorder's message said: "When you're ready, reply
'accept the remaining items as recommended', or name the items you want
changed." The page itself is not a repository file; AK1 has not read it.

For group 1 the subject is the proposed change and its impact: OWNER_ITEMS
items Q-1, Q-2, Q-4 to Q-7, Q-10 to Q-13 and Q-15, with IMPACT_ASSESSMENT
§§1–6 and 8–11 and ARC_EFFECT §§1 and 3.

## The owner's act (verbatim)

> "accept the remaining items as recommended"

No correction or exception was recorded.

## Interpretation (recording role's reading, not owner text)

The reply is the quick-answer form of OWNER_ITEMS revision 2 ("'Accept the
remaining items as recommended' accepts every row below"). DECISION-2
"Effects" records its coverage as Q-1…Q-15. Which items belong to group 1
and which to group 2 is AK1's reading; OWNER_ITEMS itself labels only Q-2
(group 1) and Q-3 (group 2). For checkpoint group 1 the act accepts:

| Item | Effect |
|---|---|
| Q-1 | Amendment ID `SCA-V4-002`; posture `ACCEPTED_PREDECESSOR`; `_ScopeChange/_LATEST.md` keeps naming SCA-V4-001 until group 3 |
| Q-2 | The scope of the change: DEL-10-03 REQ-005; the four consumption sentences; the OI-001/002/012 text in DEL-09-07, DEL-01-04 and DEL-02-02; the DEL-03-03 CLM-002 tail with REQ-005; the A17b line join; the pointer fix. All actions `MODIFY`; no ID, package or deliverable is added, removed or moved |
| Q-4 | All four arcs kept: N-18, N-21, N-24 and X-1 |
| Q-5 | Option A: OI-001 and OI-002 stay OPEN; no edit |
| Q-6 | The same-class fixes in DEL-04-02 CLM-004 and the DEL-01-01 [N] line are included |
| Q-7 | The OI-012 pointer is included; the row stays OPEN |
| Q-10 | ASC-ISS-001 option (a): 17 path-level supersession rows for SCA-V4-001 actions 18–25, 36, 42 and 46 |
| Q-11 | ASC-ISS-002: the DEL-04-01 qualifier is included, with its `_CONTEXT.md` mirror |
| Q-12 | ASC-ISS-006 option (a): the reading-rule notes |
| Q-13 | ASC-ISS-003: the SCA-V4-001 effective-state record, written after group 1 |
| Q-15 | `APP-V4-BASIS-ALIGN-20260928` DECISION-8 confirmed as the record that deferred the 17 Design re-pins |

The accepted intake is `Intake_Actions.csv` (16 rows, all `PROPOSED`), the
impact assessment is `Impact_Assessment.md`, and the pre-change baseline is
`Pre_Change_Coverage.json`, all bound in `ACCEPTED_MANIFEST.csv`. The intake
and the brief are transcriptions made after the act; the owner reviewed the
packet files, which are also bound.

## What this acceptance authorizes and does not authorize

It authorizes group-2 preparation from this snapshot, and the SCA-V4-001
effective-state record (Q-13; BASIS_AMENDMENT C-02). Because the same act
also accepted group 2 (see `../SCA-V4-002_GROUP-2_2026-09-29/`), no separate
group-2 preparation step follows.

On its own it applies no change to the docs, the decomposition package, any
`_CONTEXT.md`, `ScopeOfWork.md`, `_STATUS.md`, `Dependencies.csv`,
`_DEPENDENCIES.md` or `_DAG` file, and it does not move `_LATEST.md`.

## Basis

At the transcription (`HEAD` `39c97257ba5c354cff31f14487c05b538e806197`,
working tree clean before this run's writes):
- the accepted decomposition
  `_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z`, as amended
  by the accepted predecessor `_ScopeChange/SCA-V4-001_2026-09-28_2155/`
  (named by `_ScopeChange/_LATEST.md`, sha256 `a9a7cdc8…339d`);
- the working package inputs hashed in
  `../../SCA-V4-002_2026-09-29_1901/Brief.md`, all pre-application.

Every file this snapshot binds was written before any SCA-V4-002 edit was
applied, and none of them describes a post-application state.
