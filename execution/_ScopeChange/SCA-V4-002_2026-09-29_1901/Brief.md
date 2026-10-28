# SCA-V4-002 — Brief

**Standing: CANDIDATE amendment folder (posture `ACCEPTED_PREDECESSOR`). Not
an accepted or active snapshot.** Checkpoint groups 1 and 2 are accepted
(owner DECISION-2 of run `APP-V4-SCA002-20260929`); checkpoint group 3 is not
yet presented. `_ScopeChange/_LATEST.md` names the accepted predecessor
`SCA-V4-001_2026-09-28_2155` and is not moved before group-3 acceptance.

Transcribed on 2026-09-29 by node AK1 (a Type 2 TASK, Claude Code subagent;
no delegation) of run `APP-V4-SCA002-20260929`, from the accepted packet
(`AgentRuns/APP-V4-SCA002-20260929/AMENDMENT_PACKET/`, revision 2) and the
run's `OWNER_DECISIONS.md`. The packet's own words are the accepted content;
this file restates the request and resolution. Method:
`chirality-root:bundled:workflow:scope-change` (`workflows/scope-change/`).

This file was written before any SCA-V4-002 edit was applied. It describes
the request, the resolution and the pre-change state only.

## The human's request (verbatim)

Owner direction to start the undertaking, 2026-09-29, recorded in
`execution/_Coordination/AgentRuns/APP-V4-SCA002-20260929/OWNER_DECISIONS.md`,
section "Direction to start". The owner asked:

> "Should you run a closure audit on SCA-V4-001 first or can we run the audit
> after you complete SCA-V4-002 and determine if a DAG-003 is required?"

The recorder proposed to run the SCA-V4-001 closure audit and the SCA-V4-002
preparation in parallel, then the SCA-V4-002 checkpoints, the SoW REVISEs,
DAG-003 for owner acceptance if the new arcs are confirmed, and SCA-V4-002's
closure audit. The owner answered:

> "Proposal accepted.  Proceed accordingly."

The sources of the change are `APP-V4-BASIS-ALIGN-20260928` DECISION-8
(answer 3: "Small follow-on amendment (Recommended)") and DECISION-10
(option A), as the same record states under "Scope of SCA-V4-002, as decided
so far".

## The acceptance of checkpoint groups 1 and 2 (verbatim)

Owner, 2026-09-29, DECISION-2 (same `OWNER_DECISIONS.md`, section
"Checkpoint A: SCA-V4-002 scope-change groups 1 and 2"):

> "accept the remaining items as recommended"

Recorded in the decision snapshots
`../checkpoint_snapshots/SCA-V4-002_GROUP-1_2026-09-29/` and
`../checkpoint_snapshots/SCA-V4-002_GROUP-2_2026-09-29/`.

**Timing disclosure (DECISION-2).** The owner decided while the pre-change
`audit-decomp` baseline (node P3, method step 5) was still running; it had
been interrupted by a connection error and resumed. The baseline then
completed (commit `39c97257b`) and found nothing that changes the packet
(`DISPATCH.md`, rows P3 and K1). The group-1 decision snapshot was written
after the baseline completed.

## Parsed actions

16 atomic actions, all `MODIFY` (IMPACT_ASSESSMENT §3): rows 1–9 are nine
ScopeOfWork contracts, row 10 the HOST_INTEGRATION line layout, rows 11–13
the decomposition package, row 14 the DEL-04-01 description with its
`_CONTEXT.md` mirror, and rows 15–16 the reading-rule notes. Intake:
[Intake_Actions.csv](Intake_Actions.csv) (every row `PROPOSED`). The accepted
register is `Amendment_Actions.csv`, bound by hash in the group-2 snapshot.

## Resolution (method step 1; IMPACT_ASSESSMENT §1)

| Variable | Value |
|---|---|
| `DECOMP_VARIANT` | `SOFTWARE` |
| `CONTEXT_ROOT` | `projects/chirality-app-v4/execution/` |
| `DECOMPOSITION_PATH` | `execution/_Decomposition/SOFTWARE_DECOMP.md` with the companion registers of `Companion_Inventory.csv`. The Change Register binds to `## Decision Log` |
| `SCOPE_CHANGE_ROOT` | `execution/_ScopeChange/` |
| `AMENDMENT_ID` | `SCA-V4-002` (owner item Q-1). `zsh tools/query/scan_next_amendment_id.sh projects/chirality-app-v4/execution/_ScopeChange V4` returned `SCA-V4-002` before this folder existed |
| Pointer posture | `ACCEPTED_PREDECESSOR`: `_ScopeChange/_LATEST.md` (sha256 `a9a7cdc8c50a36fbdd25fc53c72322972ba4f9b4d301d811e1a9c1381966339d`) names `SCA-V4-001_2026-09-28_2155`; it stays unchanged |
| Predecessor's closure | `OPEN_PENDING_DERIVATIVE_CLOSURE`; closure audit CA1 verdict OPEN (`_Evaluation/ScopeClosureAudit/ScopeClosure_SCA-V4-001_2026-09-29_1222/`) |
| `ALLOW_RENUMBERING` | `false` |
| `ALLOWED_PROPAGATION_WRITES` | The group-2 write boundary (owner item Q-3): the `AffectedFiles` of the 16-row register, plus the SCA-V4-002 snapshot folders and pointers |

## Basis commits

| Commit | What it is |
|---|---|
| `102f09c1a` | The basis against which the packet checked every old block |
| `f05bd1bbd` | The packet as the owner reviewed it; the subject of the pre-change baseline |
| `f061cf61e` | Added DECISION-2 to `OWNER_DECISIONS.md` (it changes only that file) |
| `39c97257b` | The pre-change baseline; the application basis (`HEAD` when this file was written) |

`git diff --stat 102f09c1a 39c97257b` changes only files under
`_Coordination/AgentRuns/APP-V4-SCA002-20260929/` and
`_Evaluation/ScopeClosureAudit/`. No docs, decomposition, `_CONTEXT.md`,
ScopeOfWork, register, `_DAG` or `_ScopeChange` byte differs between the
packet's basis and the application basis.

## Pre-change baseline (method step 5)

The pre-change baseline is node P3's `audit-decomp` run,
`AgentRuns/APP-V4-SCA002-20260929/BASELINE/`, subject `f05bd1bbd`, scope
**PKG-01, 02, 03, 04, 05, 09, 10** (32 deliverables).
[Pre_Change_Coverage.json](Pre_Change_Coverage.json) is a byte-identical copy
of `BASELINE/coverage_summary.json` (sha256
`f89010ea5f0e12b4b3c79a693abb825fe4996cdf317c982086f39d04c6cb0edb`).

- It is a fresh run, not a reuse (BASELINE `Decision_Log.md` D-4).
- Result: 0 BLOCKER, 38 WARNING, 101 INFO, 0 EXPECTED_CONSEQUENCE.
- IMPACT_ASSESSMENT §4 names six packages. The baseline adds PKG-05, because
  register row 16 edits the `_CONTEXT.md` of DEL-05-01 and DEL-05-02
  (BASELINE finding 1). The post-change audit uses the same seven packages.
  The accepted packet text is not changed for this.

## Pre-application input hashes (sha256 at `39c97257b`)

Paths are under `projects/chirality-app-v4/`.

| Register row | File | sha256 |
|---|---|---|
| 10 | `docs/HOST_INTEGRATION.md` | `6c6854f941c714d8287bf799e1427bd4d99450847341bdf885ce4158d77eb122` |
| 11 | `execution/_Decomposition/Consolidated_Coverage.csv` | `4eee4bcb1cb296a9e96f9c44f934f19913dd827b43666475505e684a646a8db1` |
| 12 | `execution/_Decomposition/Open_Issues.csv` | `f6b92362c4f334ffe65522557acb515d247ba67133403cc6c805f1c5c4182bf7` |
| 13 | `execution/_Decomposition/SOFTWARE_DECOMP.md` | `7434058164f9e53f146793b85c38845a562fbc9ffd46f2b97de18e8d597e5747` |
| 14 | `execution/_Decomposition/Deliverables.csv` | `2480cbef8f597c76482dda22c652e182d3dcfa2a9a1eb07621ca6bda7fe06f44` |
| 14, 16 | DEL-04-01 `_CONTEXT.md` | `3f981bd6036744b524cbc67e257cdbc3821d10d829492660e4640f76386e0abd` |
| 15 | `execution/_Decomposition/checkpoint_snapshots/_LATEST_ACCEPTED.md` | `d5d873b3b918fd508685871abf177e90104b98524c5cea52944dfa2f5a695ead` |
| 15 | `execution/_Decomposition/_LATEST.md` | `8eb0519416e80c1016cf464efb86624a42eaa94c867fe2b46ead7e5b80c9bb91` |
| 16 | DEL-02-03 `_CONTEXT.md` | `d8cfefa0ce4cb3cb7cf81fcb4ef94b054823cbef2069804df30dee26ed76b148` |
| 16 | DEL-05-01 `_CONTEXT.md` | `58f0bc84d23c883451dd0cd2304cc1fb85abb0cddc009831dba4a54d02c789a1` |
| 16 | DEL-05-02 `_CONTEXT.md` | `e889d2b79d8c3d37482c3cd80e2fd034abcadf37ea3c42f4c700172ab5b94f4c` |
| 16 | DEL-09-07 `_CONTEXT.md` | `8f7927ff0a77d0b31341909004b167cd15d228e2aad474ca2974273e97b9e78f` |
| — | `execution/_ScopeChange/SCA-V4-001_2026-09-28_2155/Supersession_Map.csv` (the prior map) | `e8e433208bce44faf3f65d43b31e48b1a3476d4d6afec554a4e5319d9ef1a801` |

Each equals the hash in the BASELINE report, "Pre-change hashes of the
SCA-V4-002 targets". The nine ScopeOfWork hashes (rows 1–9) are in that
table; this amendment's candidate does not write them.

## The SCA-V4-001 basis, and a correction to one of its labels (V13 F1)

The accepted predecessor is `SCA-V4-001_2026-09-28_2155`, accepted at
checkpoint group 3 on 2026-09-29 (`APP-V4-BASIS-ALIGN-20260928` DECISION-8).
Its group-3 `ACCEPTED_MANIFEST.csv` gives the `OWNER_DECISIONS.md` row the
boundary text "hash at 3d006a909 (= presented bytes at
230bf1e64/9ae24fc0f)". For that one row the equality is false:

| Commit | sha256 of `AgentRuns/APP-V4-BASIS-ALIGN-20260928/OWNER_DECISIONS.md` |
|---|---|
| `9ae24fc0f` | `cdc486801ae6315a8249459c3fd98cdc2d42390a178f5555b15c9fbee93d6d34` |
| `3d006a909` | `752876c16f7f96ef5d63609d995596f1ac838152b561bc7b9c0b2aa6e3ddea10` |

DECISION-8 was appended after the presentation. The hash in that manifest
(`752876c1…`) and its Role column ("commit 3d006a909") are correct. The
snapshot is immutable and is not rewritten; this paragraph is the disclosure
(owner item Q-9). Both hashes were re-read here with `git show`.

## Files in this folder

| File | Role | Stage | Source |
|---|---|---|---|
| `Brief.md` | intake brief | group 1 | this transcription |
| `Intake_Actions.csv` | group-1 intake evidence (16 rows, `PROPOSED`) | group 1 | the IMPACT_ASSESSMENT §3.2 rows with `{AMENDMENT_ID}` filled, `ScopeChanging` left blank and `Status` appended |
| `Impact_Assessment.md` | group-1 output | group 1 | byte-identical copy of the accepted `AMENDMENT_PACKET/IMPACT_ASSESSMENT.md` (sha256 `46444eab…0456`); its relative links resolve against the packet folder |
| `Pre_Change_Coverage.json` | pre-change baseline | group 1 | byte-identical copy of `BASELINE/coverage_summary.json` |
| `Amendment_Preview.md`, `Propagation_Plan.md`, `Amendment_Actions.csv`, `Supersession_Delta.csv` | group-2 exact amendment, plan, register and supersession delta | group 2 | written for the group-2 decision snapshot, which binds them |
| `Supersession_Map.csv`, `Decision_Log.md` and the group-3 preparation files | candidate | group-3 preparation | written after the group-2 snapshot |
