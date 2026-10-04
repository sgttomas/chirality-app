# Owner decisions — APP-V4-SCA003-20261002 (SCA-V4-003)

Exact owner text, as given in the chat session with HELP_HUMAN. Custody: the
session transcript; recorded by HELP_HUMAN. A record here is not a claim
that the owner reviewed any file.

## Direction to prepare (owner, exact)

From run `APP-V4-DESIGN-PASS-3-20261001` (OWNER_DECISIONS.md there):

- 2026-10-01, answering HELP_HUMAN's recommendation, which included "Apply
  this pass's contract proposals as a third amendment … folded in when it's
  cheapest, since the amendment can also carry contract changes from the
  next pass":

  > Proceed as recommended.

- 2026-10-02, answering "Should I run the closeout now, starting with the
  three wording fixes and preparing the contract amendment for your
  sign-off?":

  > yes, run the closeout.

**Reading (HELP_HUMAN):** SCA-V4-003 is prepared through `scope-change` to
its first owner checkpoint. As in SCA-V4-002, groups 1 (change and impact)
and 2 (exact amendment and propagation plan) may be presented together.
Nothing is applied before the owner accepts. The amendment carries the
contract proposals of design passes 2 and 3; its scope is the consolidated
ledger, with each item's disposition put to the owner.

## DECISION-1 — Checkpoint K1: SCA-V4-003 scope-change groups 1 and 2 (owner, exact, 2026-10-03)

**Custody:** the owner's chat message to HELP_HUMAN, after the package was
presented as `AMENDMENT_PACKET/OWNER_ITEMS.md` (sha256 prefix `72c53db208ff42cc`,
committed at `60359d7372`, with the packet files it cites, reviewed by V23
and V23b) and as the review page
https://claude.ai/artifact/A8XbVqJPNoWCHK3RM7YaYJ (Version 1).

> accept the remaining items as recommended

**Effects** (each is the recommendation in OWNER_ITEMS.md's quick answer
sheet; "remaining" is read as all seventeen, since none had been answered):

- **Q-1:** identity `SCA-V4-003`, posture ACCEPTED_PREDECESSOR (SCA-V4-002).
- **Q-2 (group 1 accepted):** the ledger's 191 INCLUDE rows.
- **Q-3 (group 2 accepted):** the write boundary, route and register as
  drafted (`Amendment_Actions.draft.csv`, `BASIS_AMENDMENT.md`,
  `SOW_REVISIONS_A.md`, `SOW_REVISIONS_B.md`), including the disclosed
  wording conventions; the Scopes of Work change only after group 3, by
  `scope-of-work` REVISE with `NO_STATUS_TOUCH`.
- **Q-4:** the 10 new links; NR-01, NR-02 and NR-04 with their sentences;
  NR-03 dropped.
- **Q-5:** the App act control in DEL-01-04, with REQ-008 as adjusted and the
  drafted OUT-005, AC-008 and VER-008, as worded.
- **Q-6:** S-01-2 and S-01-3 included. **Q-7:** S-01-4 held. **Q-8:** DEL-03-01
  keeps custody of FX-PIPE-01 and SH-1 (S-01-5 included). **Q-9:** the four
  A12-mapping rows held.
- **Q-10:** option B, status `RESOLVED_BY_OWNER_DECISION`, with supersession
  row D-021.
- **Q-11:** the optional items included; SC3-02-02-5 and S-0906-4 dropped.
- **Q-12:** no basis change. **Q-14:** R-02-4 held.
- **Q-13:** DEL-01-02, 01-03, 01-04, 01-05, 02-02 and 02-04 move from
  INITIALIZED to IN_PROGRESS now, as a separate act (recorded in each
  `_STATUS.md` by HELP_HUMAN relaying this direction, as DECISION-6 of
  `APP-V4-BASIS-ALIGN-20260928` was).
- **Q-15:** the receivers sentences P1-06…P1-10 and R22-7's DEL-04-03 sentence
  and row. **Q-17:** the 15 further mirror rows.
- **Q-16:** each decision snapshot is committed before the next stage uses
  it; the SCA-V4-002 effective-state note is written.
- The drafted text listed under "Drafted text for your review" is accepted as
  worded.

Group 3 (the audited poststate) and DAG-004 remain for the owner.

## DECISION-2 — Checkpoint K2: SCA-V4-003 group 3 (owner, exact, 2026-10-03, local time America/Denver, MDT)

**Custody:** the owner's chat message to HELP_HUMAN, after HELP_HUMAN
presented the audited poststate in chat: the candidate
`_ScopeChange/SCA-V4-003_2026-10-03_1827/` (Handoff_State.md sha256 prefix
`4f3f31b971a8a7c8`, committed at `388fc730b9`), its closure verdict
`OPEN_PENDING_DERIVATIVE_CLOSURE`, the post-change audit (0 BLOCKER, the
WARNING rise attributed to the Q-13 act), review V24 (READY FOR GROUP 3,
M-1 fixed at AK1-R) and the open obligations (the 19 REVISEs, the register
UPDATE, DAG-004, the Design re-pins, `Coverage_Telemetry.json`).

> I accept the audited result.

**Effects:**

- Group 3 is accepted: the audited poststate, its closure verdict
  `OPEN_PENDING_DERIVATIVE_CLOSURE`, and the open obligations as listed.
- `{ACCEPT_DATE}` = `2026-10-03` (the owner's local date of the act).
- The acceptance-time edits F-1…F-4 and H-1…H-3 of the candidate's
  Handoff_State follow, then the accepted route of Q-3: `scope-of-work`
  REVISE for the 19 Scopes of Work (`NO_STATUS_TOUCH`), `dependency-extract`
  UPDATE for the 20 registers, the `project-dag` currency audit and a DAG-004
  candidate, which returns to the owner.

## DECISION-3 — Checkpoint K3: DAG-004 (owner, exact, 2026-10-03, local time America/Denver)

**Custody:** the owner's chat message to HELP_HUMAN, after HELP_HUMAN
presented in chat the DAG-004 candidate staged in `DAG_PREP/`
(CHECKPOINT_C.md sha256 prefix `710de58450fafb86`, REVIEW_PACKET.md, committed by
`4ca22437f7`), the currency DEPARTURE against DAG-003, and review V25
(READY FOR CHECKPOINT C, committed `6358ce132d`), with the recommendations
below.

> I accept DAG-004.

**Effects** (CHECKPOINT_C §8 as recommended, with V25's notes):

1. DAG-004 is accepted as the single successor to DAG-003 for the ten links
   (project-dag checkpoints 1 and 2 together).
2. The handoff records the four new sequencing waits (DEL-01-04, 02-02,
   02-03, 03-03), the route re-examination list (a light check: V25 O-1),
   X-1's narrow scope, the DEL-09-06 guard, V25 m-1 (DEL-05-01 → DEL-01-05
   representative row is information-only; for the register owners), V25 m-2
   (hub growth) and the carried obligations.
3. The integrator moves the staged files to their method homes and writes the
   pointers at publication; INDEPENDENT_REVIEW.md is added at publication
   (V25 m-4).
4. The DEL-01-03 absolute TargetLocation is repaired after acceptance.
