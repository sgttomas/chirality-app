# SCA-V4-003 — Brief

**Standing: CANDIDATE amendment folder (posture `ACCEPTED_PREDECESSOR`). Not
an accepted or active snapshot.** Checkpoint groups 1 and 2 are accepted
(owner DECISION-1 of run `APP-V4-SCA003-20261002`); checkpoint group 3 is not
yet presented. `_ScopeChange/_LATEST.md` names the accepted predecessor
`SCA-V4-002_2026-09-29_1901` and is not moved before group-3 acceptance.

Transcribed on 2026-10-03 by node AK1 (stage 2; a Type 2 TASK, Claude Code
subagent; no delegation) of run `APP-V4-SCA003-20261002`, after the act and
after both decision snapshots were committed (`3e747b7685`, `ec267bdb9f`),
from the accepted packet (`AgentRuns/APP-V4-SCA003-20261002/AMENDMENT_PACKET/`)
and the run's `OWNER_DECISIONS.md`. Neither decision snapshot binds this
file; the packet files they bind govern. Method:
`chirality-root:bundled:workflow:scope-change` (`workflows/scope-change/`).

It describes the request, the resolution and the pre-change state only.

## The human's request (verbatim)

From run `APP-V4-DESIGN-PASS-3-20261001`, as quoted in this run's
`OWNER_DECISIONS.md`, "Direction to prepare":

- 2026-10-01, answering a recommendation that included "Apply this pass's
  contract proposals as a third amendment … folded in when it's cheapest,
  since the amendment can also carry contract changes from the next pass":

  > Proceed as recommended.

- 2026-10-02, answering "Should I run the closeout now, starting with the
  three wording fixes and preparing the contract amendment for your
  sign-off?":

  > yes, run the closeout.

HELP_HUMAN's recorded reading: SCA-V4-003 carries the contract proposals of
design passes 2 and 3, prepared through `scope-change` to its first
checkpoint, each item's disposition put to the owner.

## The acceptance of checkpoint groups 1 and 2 (verbatim)

Owner, 2026-10-03, DECISION-1 (same `OWNER_DECISIONS.md`, sha256
`59b20bb0…f919`, added by `5b16bb6831`):

> accept the remaining items as recommended

Recorded in `../checkpoint_snapshots/SCA-V4-003_GROUP-1_2026-10-03/` and
`../checkpoint_snapshots/SCA-V4-003_GROUP-2_2026-10-03/`, with the pointers
`../SCA-V4-003_GROUP-1_AUTHORIZED.md` and `../SCA-V4-003_GROUP-2_AUTHORIZED.md`.
No timing disclosure is needed: the pre-change baseline was committed
(`eaa6a37730`) before the act.

## Parsed actions

23 atomic actions, all `MODIFY` (IMPACT_ASSESSMENT §3): rows 1–20 are
deliverables (19 ScopeOfWork contracts and their registers, and DEL-05-02's
register alone), row 21 OI-009, row 22 OI-018, row 23 the Change Register
entry. They carry the ledger's 191 INCLUDE rows. Intake:
[Intake_Actions.csv](Intake_Actions.csv) (every row `PROPOSED`). The accepted
register is `Amendment_Actions.csv`, bound by hash in the group-2 snapshot.

## Resolution (method step 1; IMPACT_ASSESSMENT §1)

| Variable | Value |
|---|---|
| `DECOMP_VARIANT` | `SOFTWARE` |
| `CONTEXT_ROOT` | `projects/chirality-app-v4/execution/` |
| `DECOMPOSITION_PATH` | `execution/_Decomposition/SOFTWARE_DECOMP.md`; the Change Register binds to `## Decision Log` |
| `SCOPE_CHANGE_ROOT` | `execution/_ScopeChange/` |
| `AMENDMENT_ID` | `SCA-V4-003` (Q-1), from `tools/query/scan_next_amendment_id.sh projects/chirality-app-v4/execution/_ScopeChange V4` under zsh (IMPACT_ASSESSMENT §1) |
| Pointer posture | `ACCEPTED_PREDECESSOR`: `_ScopeChange/_LATEST.md` (sha256 `2b7938bc82aa9b08a2bd26d7f2c0169c538edb1e6ae5423d5757def968f0c2e1`) names `SCA-V4-002_2026-09-29_1901`; unchanged |
| Predecessor's closure | `OPEN_PENDING_DERIVATIVE_CLOSURE`, for derivatives only (IMPACT_ASSESSMENT §9) |
| `ALLOW_RENUMBERING` | `false` |
| `ALLOWED_PROPAGATION_WRITES` | The group-2 write boundary (Q-3): `_Decomposition/Open_Issues.csv` (B-02, B-03) and the SCA-V4-003 snapshot folders in the candidate; after group 3, `SOFTWARE_DECOMP.md` (B-01) and `_ScopeChange/_LATEST.md` (C-01); the 19 ScopeOfWork files only by REVISE after group 3 |

## Basis commits

| Commit | What it is |
|---|---|
| `897a107cc9` | The packet's basis (P1) and the baseline's subject |
| `eaa6a37730` | The pre-change baseline (P3) |
| `60359d7372` | The packet as presented at K1 (after RP1 and V23b) |
| `5b16bb6831` | DECISION-1 added to `OWNER_DECISIONS.md` |
| `baa6e618d7` | The Q-13 act: six `_STATUS.md` files INITIALIZED → IN_PROGRESS (outside the amendment) |
| `3e747b7685`, `ec267bdb9f` | Group-1 and group-2 decision snapshots and pointers; `ec267bdb9f` is the application basis |

Between `eaa6a37730` and `ec267bdb9f`, the audited surfaces changed only in
the six `_STATUS.md` files of the Q-13 act and in DEL-03-04
`Design/HOST_INTEGRATION_GUIDE.md` (`a68a9e06e2`, the pass-3 closeout's V22
record fixes). No `ScopeOfWork.md`, `Dependencies.csv`, `_DEPENDENCIES.md`,
`_Decomposition/`, `_DAG/` or basis byte changed.

## Pre-change baseline (method step 5)

Node P3's `audit-decomp` run, `AgentRuns/APP-V4-SCA003-20261002/BASELINE/`,
scope **PKG-01, 02, 03, 04, 05, 09, 10** (32 deliverables).
[Pre_Change_Coverage.json](Pre_Change_Coverage.json) is a byte copy of
`BASELINE/coverage_summary.json` (sha256 `99f016cc…e37f`), bound in the
group-1 manifest. Result: 0 BLOCKER, 35 WARNING, 93 INFO, 0
EXPECTED_CONSEQUENCE. A fresh run, not a reuse (BASELINE D-4).

## Pre-application input hashes (sha256 at `ec267bdb9f`)

Every `AffectedFiles` path of the register equals its blob at
`ec267bdb9f` before the application (checked by script; list in
`AgentRuns/APP-V4-SCA003-20261002/Application/target_hashes.txt`). The
direct-write and acceptance-conditional targets:

| Register row | File (under `execution/`) | sha256 |
|---|---|---|
| 21, 22 | `_Decomposition/Open_Issues.csv` | `a11782181531ce77e564b774787537d3e11cc1d4304123cba0d83f539bb280f0` |
| 23 | `_Decomposition/SOFTWARE_DECOMP.md` (B-01 held) | `ea3388bcb05b2280d8bb10db2578aec9818f40c559b4214e1732da754d9bd7d5` |
| — | `_ScopeChange/_LATEST.md` (C-01 held) | `2b7938bc82aa9b08a2bd26d7f2c0169c538edb1e6ae5423d5757def968f0c2e1` |
| — | `_ScopeChange/SCA-V4-002_2026-09-29_1901/Supersession_Map.csv` (prior map) | `45502bf57a1c1e354b769b2b9426381c2fa1d1e4f9b4482fbc393f85e79eeb93` |

The 19 ScopeOfWork files equal the "Prior SoW sha256" values in
SOW_REVISIONS_A and SOW_REVISIONS_B, 19/19; the candidate does not write
them.

## Files in this folder

| File | Role | Source |
|---|---|---|
| `Brief.md` | intake brief | this transcription (after the act) |
| `Intake_Actions.csv` | group-1 intake evidence (23 rows, `PROPOSED`) | the accepted register's rows with `ScopeChanging` blank and `Status` appended (transcription after the act) |
| `Impact_Assessment.md` | group-1 output | byte copy of `AMENDMENT_PACKET/IMPACT_ASSESSMENT.md` (sha256 `46ea15e5…35f3`, bound in both manifests); its relative links resolve against the packet folder |
| `Pre_Change_Coverage.json` | pre-change baseline | byte copy of `BASELINE/coverage_summary.json` (bound in the group-1 manifest) |
| `Amendment_Actions.csv` | accepted register | byte copy of the group-2 snapshot's register (sha256 `9b7c2ce8…6d1c`) |
| `Amendment_Preview.md`, `Propagation_Plan.md` | group-2 exact amendment and plan, rendered | transcriptions after the act; the bound packet files govern |
| `Supersession_Delta.csv` | supersession delta (D-021) | BASIS_AMENDMENT Part D, byte for byte |
| `Supersession_Map.csv`, `Decision_Log.md`, `Post_Change_Coverage.json`, `Handoff_State.md`, `RUN_SUMMARY.md` | group-3 preparation | written in this stage |
