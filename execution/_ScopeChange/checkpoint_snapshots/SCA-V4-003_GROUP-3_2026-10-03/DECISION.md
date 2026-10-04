# SCA-V4-003 checkpoint group 3 — accepted audited poststate

Recorded 2026-10-03 (local; America/Denver, MDT) by node AK2 (part 1). AK2
is a Type 2 TASK (a Claude Code subagent; no delegation), dispatched by the
HELP_HUMAN session of run `APP-V4-SCA003-20261002`, which presented
checkpoint K2 to the owner.

This record transcribes the owner's act as the run's `OWNER_DECISIONS.md`
records it. It is not a new request for the same decision. It claims no
inspection the owner did not perform.

## Custody of the act

| Item | Value |
|---|---|
| Record | `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-SCA003-20261002/OWNER_DECISIONS.md`, section "DECISION-2 — Checkpoint K2: SCA-V4-003 group 3 (owner, exact, 2026-10-03, local time America/Denver, MDT)" |
| Record sha256 at transcription | `29c0a07b50d695a15bbff52b36d5925725cc7f3e78d0caf997ee9fd3c3b28c2e`. The working-tree file and its blob at `84b520742d` give the same hash |
| Commit that added DECISION-2 | `84b520742d399dddef3cc04845064727834f5b01` ("docs(app-v4): SCA-V4-003 checkpoint K2 accepted (group 3), DECISION-2", 2026-10-03 18:56:32 -0600). It changes only that file (24 insertions) |
| Channel | The owner's chat message to HELP_HUMAN, recorded verbatim in the record above. AK2 did not observe the chat; it relies on that record |
| Earlier acts in this amendment | The directions ("Proceed as recommended."; "yes, run the closeout.") and DECISION-1 (groups 1 and 2, "accept the remaining items as recommended"), recorded in `../SCA-V4-003_GROUP-1_2026-10-03/` and `../SCA-V4-003_GROUP-2_2026-10-03/` |

## What the owner had in front of them

DECISION-2 "Custody" records that HELP_HUMAN presented the audited poststate
in chat:
- the candidate `_ScopeChange/SCA-V4-003_2026-10-03_1827/`, with
  `Handoff_State.md` (sha256 prefix `4f3f31b971a8a7c8`) committed at
  `388fc730b9`;
- the closure verdict `OPEN_PENDING_DERIVATIVE_CLOSURE`;
- the post-change audit: 0 BLOCKER, with the WARNING rise attributed to the
  Q-13 act;
- review V24: READY FOR GROUP 3, M-1 fixed at AK1-R;
- the open obligations: the 19 REVISEs, the register UPDATE, DAG-004, the
  Design re-pins and `Coverage_Telemetry.json`.

The commit `388fc730b9` → `84b520742d` changes only `OWNER_DECISIONS.md`, so
every presented file has its presented bytes at `84b520742d`.
`ACCEPTED_MANIFEST.csv` binds those bytes. The 13 candidate artifacts equal
`RUN/Application/CANDIDATE_ARTIFACTS.sha256` (13/13 at the act).

The presented `Handoff_State.md` (sha256
`4f3f31b971a8a7c817a32604a22b99697731cd18283f72de4e443d6e099ec167`) contains:
- the exact acceptance-time list F-1…F-4 and H-1…H-3, with its date rule;
- the propagation table for the accepted route (Q-3);
- the parsable closure verdict;
- the post-change classification (COV-129 `EXPECTED_CONSEQUENCE`; the 16
  Q-13 re-gradings kept in the adjusted state);
- the notes m-3, m-4, m-5, O-1 and O-2.

`RUN` = `execution/_Coordination/AgentRuns/APP-V4-SCA003-20261002`.

## The owner's act (verbatim)

> I accept the audited result.

No correction or exception was recorded.

## Interpretation (recording role's reading, not owner text)

| Item | Effect |
|---|---|
| Audited poststate | The candidate is accepted as presented: applied at `fa16393978`, its records revised at `388fc730b9`. That covers B-02 option B and B-03 in `Open_Issues.csv`, D-021 and the 30-row `Supersession_Map.csv`, the C-02 note, and the post-change audit. So are its closure verdict `OPEN_PENDING_DERIVATIVE_CLOSURE` and the open obligations listed in it |
| `{ACCEPT_DATE}` | `2026-10-03`, the owner's local date of the act (DECISION-2 "Effects"; the presented date rule) |
| Acceptance-time edits | Exactly F-1…F-4 and H-1…H-3 of the presented `Handoff_State.md`. F-1 is this folder. H-1 is B-01 with `{ACCEPT_DATE}` = `2026-10-03` and `{AMENDMENT_SNAPSHOT}` = `SCA-V4-003_2026-10-03_1827`; its expected result is sha256 `983199cc22c84398000612cd95308c840ad011d302fe31ca110a5aa97e64a70d` (`RUN/Application/SIMULATED_POSTACCEPT.md`). H-2 is C-01 with `{CLOSURE_VERDICT}` = `OPEN_PENDING_DERIVATIVE_CLOSURE`, `{G1_DATE}` = `{G2_DATE}` = `2026-10-03`, `{C02_UTC}` = `20261004T002903Z`, and `{UTC}` = the H-3 folder's stamp. F-2…F-4 are the status lines of the candidate's `Decision_Log.md`, `Handoff_State.md` and `RUN_SUMMARY.md`. H-3 is the post-acceptance record, using the baseline audit script unchanged |
| Accepted amendment snapshot | The candidate folder `_ScopeChange/SCA-V4-003_2026-10-03_1827/` becomes the immutable accepted snapshot, and `_ScopeChange/_LATEST.md` moves to it. Its group-1 and group-2 copies and transcriptions are not rewritten. Only its three status records change (F-2…F-4) |
| Supersession | D-021 takes effect through the accumulated `Supersession_Map.csv` (30 rows) when `_LATEST.md` names this snapshot |
| Reopening | No affected deliverable is `ISSUED` or `CHECKING`: all 20 register deliverables are IN_PROGRESS. This acceptance authorizes no `ISSUED → IN_PROGRESS` reopening, and no `write_status.sh --amendment` use arises. The `ScopeChanging` `YES` rows record scope-changing text edits, not reopenings |

## What this acceptance authorizes and does not authorize

It authorizes:
- this decision folder;
- F-2…F-4 and H-1…H-3, exactly as listed;
- finalizing `SCA-V4-003_2026-10-03_1827/` as the accepted snapshot, and
  moving `_ScopeChange/_LATEST.md` to it;
- the propagation recorded in DECISION-2 "Effects", each step through its
  own workflow and brief, in this order:
  1. `scope-of-work` MODE=REVISE for the 19 Scopes of Work
     (`STATUS_POLICY` `NO_STATUS_TOUCH`), one deliverable per brief, each
     closing with MODE=VERIFY;
  2. `dependency-extract` UPDATE for the 20 registers and DEL-04-03's
     `_DEPENDENCIES.md`;
  3. the `project-dag` currency audit and a DAG-004 candidate, which
     returns to the owner.

It does not authorize:
- any edit not on the presented acceptance-time list;
- any `ScopeOfWork.md`, `Dependencies.csv`, `_DEPENDENCIES.md` or `_DAG/`
  write under this record (those have their own briefs);
- any write to `Coverage_Telemetry.json`;
- any `_STATUS.md` or lifecycle change;
- acceptance of DAG-004;
- any release, publication or reliance claim.

The standing Git authorization governs commits. This TASK makes none.

## Basis

- **Accepted group-1 snapshot:**
  `checkpoint_snapshots/SCA-V4-003_GROUP-1_2026-10-03/`
  - `DECISION.md`: `7acf609dcc4eb2af90985fa40434387ed554345742501a01cd65cffb3fce0665`
  - `ACCEPTED_MANIFEST.csv`: `733a6b892458a8d9ff909b2f28ed19b1acf218ce0e6f7ae5619c05d36006d78d`
- **Accepted group-2 snapshot:**
  `checkpoint_snapshots/SCA-V4-003_GROUP-2_2026-10-03/`
  - `DECISION.md`: `cf13461175ca6c1ccd9ced4956afbfcde6d67fc1c7969d63434899aab826ce86`
  - `ACCEPTED_MANIFEST.csv`: `8b6287633b72b201ca652799ba794456b4d83e28a6789770542682db39548bb8`
  - It binds the register `Amendment_Actions.csv` at
    `9b7c2ce8fbf97ec0cf829c5024e03d19b4117c1ca50abaea4ec0b2c340346d1c`,
    which is unchanged.
- **Pointer posture:** `ACCEPTED_PREDECESSOR`. Before this act,
  `_ScopeChange/_LATEST.md` (sha256
  `2b7938bc82aa9b08a2bd26d7f2c0169c538edb1e6ae5423d5757def968f0c2e1`) names
  the accepted predecessor `SCA-V4-002_2026-09-29_1901`.
- **Evidence base:** commit `84b520742d`, working tree clean before this
  node's writes.
