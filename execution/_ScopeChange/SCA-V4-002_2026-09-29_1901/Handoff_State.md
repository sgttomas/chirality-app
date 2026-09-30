# Handoff state — SCA-V4-002 (CANDIDATE, before group 3)

**Status.** Candidate awaiting the owner's checkpoint group 3. Groups 1 and 2
are accepted (DECISION-2 of run APP-V4-SCA002-20260929). Group 3 is **not
accepted**: no accepted-state marker exists, and `_ScopeChange/_LATEST.md`
still names SCA-V4-001.

**Candidate applied at:** `70376aff2`. **Independent review:**
`AgentRuns/APP-V4-SCA002-20260929/reviews/V14.md`, READY FOR GROUP 3, no
blocking finding.

## Applied only after group-3 acceptance (acceptance-conditional)

| # | Item | Slots filled at acceptance |
|---|---|---|
| H-1 | B-04: the SOFTWARE_DECOMP.md Decision Log entry | `SCA-V4-002`; the act date; this snapshot folder |
| H-2 | C-01: `_ScopeChange/_LATEST.md` in SPEC §11.2 form (`Latest:`/`Updated:`), naming SCA-V4-001 as the predecessor, the C-02 record at its actual path `_PostAcceptanceValidation/SCA-V4-001_20260930T010520Z_EFFECTIVE_STATE/`, and the open list | the act date |
| H-3 | Consolidated_Coverage recompute after H-1 | — |
| H-4 | Post-acceptance validation and an audit-decomp rerun with the seven-package scope (PKG-01, 02, 03, 04, 05, 09, 10); COV-139 should then be absent | — |

## Propagation after acceptance (accepted route, Q-3)

| Package | State | Next owning workflow |
|---|---|---|
| 9 ScopeOfWork contracts (DEL-10-03, 02-01, 02-03, 09-07, 01-04, 02-02, 03-03, 04-02, 01-01) | STALE; revise per SOW_REVISIONS.md | `scope-of-work` MODE=REVISE, STATUS_POLICY NO_STATUS_TOUCH, one deliverable per brief |
| B-06a: `_Decomposition/checkpoint_snapshots/_LATEST_ACCEPTED.md` reading-rule note | HELD, DAG-002-bound; applied with the REVISE stage so that it falls inside the DAG-003 departure | integrator, with the REVISEs |
| Dependency registers: the 9 revised deliverables, plus DEL-04-01/02/03 re-quoting (ASC-ISS-008) and DEP-09-07-016 (ASC-ISS-007) | STALE after REVISE | `dependency-extract` UPDATE |
| DAG-002 | Will depart: +4 held arcs (N-18, N-21, N-24, X-1); DAG pending expected for DEL-02-01, 02-03, 03-02, 03-03, 01-04 | `project-dag` currency audit, then TRIGGER=SUCCESSOR → DAG-003; owner checkpoint C |
| Coverage_Telemetry.json | STALE_REBUILD_REQUIRED (carried from SCA-V4-001; sequenced after this amendment) | decomposition owner, bounded brief |
| 17 Design files | Re-pin to the amended texts (carried; sequenced after this amendment) | App v4 design undertaking |

**Closure verdict:** OPEN_PENDING_DERIVATIVE_CLOSURE.

## COV-139 classification

The post-change audit flags this candidate folder as "historical snapshot
residue" because `Handoff_State.md` and `RUN_SUMMARY.md` were not yet written.
Classification: **EXPECTED_CONSEQUENCE** of the accepted sequence (group-2
Handoff_State step 6; IMPACT_ASSESSMENT §7 step 3; DECISION-2): those two
records follow the independent review. The script's "historical" label is a
wording limit; this is a candidate, not a historical snapshot. Closed by the
writing of these records; the H-4 rerun confirms it absent. Artifacts at
presentation:

| File | sha256 (prefix) |
|---|---|
| `Amendment_Actions.csv` | `158702bf610777e0` |
| `Amendment_Preview.md` | `d2099b70f51aab71` |
| `Brief.md` | `0d4f7c7b7500b28c` |
| `Decision_Log.md` | `fa2a967a4c7e23a6` |
| `Evidence/Application/DAG_CURRENCY.txt` | `76f971b510b2285f` |
| `Evidence/Application/Supersession_Findings.csv` | `c7312589902ad103` |
| `Evidence/Application/apply_log.json` | `56f2cce4a62a67ec` |
| `Evidence/Application/apply_sca002.py` | `476899f665fbab2e` |
| `Evidence/Application/gen_group2.py` | `d52b47cbd74edafc` |
| `Impact_Assessment.md` | `46444eab11d7af76` |
| `Intake_Actions.csv` | `576244b3bc4efbdc` |
| `Post_Change_Coverage.json` | `ba6a393b162ed20f` |
| `Pre_Change_Coverage.json` | `f89010ea5f0e12b4` |
| `Propagation_Plan.md` | `3fd8557a5d3d3215` |
| `Supersession_Delta.csv` | `8c3f1a5599450502` |
| `Supersession_Map.csv` | `45502bf57a1c1e35` |

## Dispositions carried from V14

- **R-1** The C-02 effective-state folder keeps its committed name
  (`…_EFFECTIVE_STATE`); the packet's other form is not used.
- **R-2** The packet cites `e9dc4633b` for the 16 REVISEs; git shows
  `340ecf341` (SoWs) and `b585e5ebe` (registers). The C-02 record states
  the true commits. Packet bytes are not edited.
- **R-3** IMPACT_ASSESSMENT §4 names six packages; the baseline and
  post-change audits used seven (PKG-05 added for register row 16). A
  stricter superset; no edit changed. Disclosed to the owner at group 3.
- **R-4** The Q-item split between the two snapshots is the recording
  role's reading; both manifests say so.
- **O-5** The packet's "6 `_CONTEXT.md` / 5 decomposition files" counts are
  transposed (5 files with 6 edits; 6 decomposition files). AffectedFiles
  are exact; the register governs.

## Carried from the predecessor

- SCA-V4-001's closure verdict is OPEN_PENDING_DERIVATIVE_CLOSURE.
  ASC-ISS-001 closes only at this amendment's group-3 acceptance, confirmed
  by a later `audit-scope-closure` rerun as a superseding snapshot.
