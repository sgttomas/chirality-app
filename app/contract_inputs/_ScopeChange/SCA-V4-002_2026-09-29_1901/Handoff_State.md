# Handoff state — SCA-V4-002 (ACCEPTED, active snapshot)

**Status.** The owner accepted checkpoint group 3 on 2026-09-29 (DECISION-3
of run `APP-V4-SCA002-20260929`: "Accept (Recommended)"). This folder is now
the immutable accepted amendment snapshot, and `_ScopeChange/_LATEST.md`
names it in SPEC §11.2 form.

This file, `RUN_SUMMARY.md` and `Decision_Log.md` were finalized after the
act by node AK2. The candidate version of this file, which the owner
accepted, is sha256 `c522d3fe8d7b334e5fa4e89ac80d4c735e47f675b6fc9c11b27640435140362b`
(at `ffdb56e1a`), and the group-3 `ACCEPTED_MANIFEST.csv` binds it.

`Brief.md` keeps its candidate standing line because the group-1 manifest
binds its bytes; `Amendment_Preview.md` and `Propagation_Plan.md` keep
theirs because the group-2 manifest binds them. This file and `_LATEST.md`
govern the standing.

## Accepted snapshot and decision records

| Item | Path |
|---|---|
| **Accepted amendment snapshot** | `execution/_ScopeChange/SCA-V4-002_2026-09-29_1901/` |
| Active pointer | `execution/_ScopeChange/_LATEST.md` (`Latest: SCA-V4-002_2026-09-29_1901`) |
| Group 1 (DECISION-2) | `execution/_ScopeChange/checkpoint_snapshots/SCA-V4-002_GROUP-1_2026-09-29/` |
| Group 2 (DECISION-2) | `execution/_ScopeChange/checkpoint_snapshots/SCA-V4-002_GROUP-2_2026-09-29/` |
| Group 3 (DECISION-3) | `execution/_ScopeChange/checkpoint_snapshots/SCA-V4-002_GROUP-3_2026-09-29/` |
| Post-acceptance validation (H-4) | `execution/_ScopeChange/_PostAcceptanceValidation/SCA-V4-002_20260930T021014Z/` |
| Post-acceptance audit | `execution/_Coordination/AgentRuns/APP-V4-SCA002-20260929/POSTACCEPT/` |
| Accepted predecessor | `execution/_ScopeChange/SCA-V4-001_2026-09-28_2155/` (immutable; its effective state is recorded at `execution/_ScopeChange/_PostAcceptanceValidation/SCA-V4-001_20260930T010520Z_EFFECTIVE_STATE/`) |

- **Pointer posture:** `ACCEPTED_PREDECESSOR`. Before this act `_LATEST.md`
  named SCA-V4-001 (sha256 `a9a7cdc8…339d`); after it, only SCA-V4-002.
- **Authoritative action register:** `Amendment_Actions.csv`, SHA-256
  `158702bf610777e008e304268fcbd967756f9186ded946942430a391957c579d`
  (16 `MODIFY` rows; `ScopeChanging` `YES` on row 1;
  `SupersessionBindingPresent` `YES` on row 14), as bound in the group-2
  `ACCEPTED_MANIFEST.csv`. `Intake_Actions.csv` is group-1 evidence only.
- **Supersession:** the 18 bindings in `Supersession_Delta.csv` (17
  `DL-SCA-V4-001-…` rows and D-014) are active through
  `Supersession_Map.csv` (29 rows), now that `_LATEST.md` names this
  snapshot.

## Authoritative truth changed

- **Candidate, accepted as presented (applied at `70376aff2`):** A-01
  (HOST_INTEGRATION line break); B-01 (31-row recompute); B-02 (OI-012
  pointer); B-05a and B-05b (DEL-04-01 qualifier and mirror); B-06b
  (`_Decomposition/_LATEST.md`); B-06c (five `_CONTEXT.md` lines).
- **Acceptance-conditional, applied after the act (2026-09-29, node AK2):**

| # | Item | Target | Result sha256 |
|---|---|---|---|
| H-1 | B-04, the Decision Log entry (`{ACCEPT_DATE}` = 2026-09-29; `{AMENDMENT_SNAPSHOT}` = `SCA-V4-002_2026-09-29_1901`; the five clause slots filled, no item declined; Q-5 option A adds nothing) | `_Decomposition/SOFTWARE_DECOMP.md` | `ea3388bcb05b2280d8bb10db2578aec9818f40c559b4214e1732da754d9bd7d5` |
| H-2 | C-01, the pointer in SPEC §11.2 form (`Latest:` / `Updated:` first; predecessor SCA-V4-001; the C-02 record at its committed path, V14 R-1). The registered parser `_latest_pointer_target` returns `SCA-V4-002_2026-09-29_1901` and `_pointer_matches` is True | `_ScopeChange/_LATEST.md` | `2b7938bc82aa9b08a2bd26d7f2c0169c538edb1e6ae5423d5757def968f0c2e1` |
| H-3 | Recompute check after H-1: the B8 rule over all 144 rows against the post-H-1 documents changes no row. The register carries no `SOFTWARE_DECOMP.md` row, so H-1 shifts none | `_Decomposition/Consolidated_Coverage.csv` | unchanged, `366773650b588dc995f396be02d7e2690d9738c8d22afb98a85260dfb87313ea` |
| H-4 | Post-acceptance validation, plus the audit-decomp rerun over the seven packages | `_PostAcceptanceValidation/SCA-V4-002_20260930T021014Z/` | see that record |

The filled B-04 "old" block matched exactly once. B-06a is not applied here:
the accepted timing puts it with the SoW REVISEs (propagation stage 1).

## State fields

| Field | Value |
|---|---|
| `DecompositionTruthState` | `COMPLETE` |
| `DerivativePackageState` | `INCOMPLETE` |
| `ContentRemediationState` | `NOT_REQUIRED` |
| `DownstreamRerunState` | `IN_PROGRESS` |
| `MetadataAlignmentState` | `NOT_REQUIRED` |
| `AuditState` | `WARNINGS` |
| `AdjustedAuditState` | `WARNINGS` |
| `ReadyForNextPhase` | `NOT_APPLICABLE` |

The notes behind these values:
- `DownstreamRerunState` is `IN_PROGRESS` because DECISION-3 authorizes the
  propagation, and no rerun had completed when this file was finalized.
- The post-acceptance audit (`POSTACCEPT/`) finds 0 BLOCKER, 38 WARNING and
  100 INFO (POSTCHANGE: 0 / 39 / 101). COV-139 (the candidate folder as
  "historical residue") is absent: the folder holds its records. The
  registered-parser INFO is absent: the pointer resolves.
- The 38 WARNINGs are pre-existing: 37 lifecycle WARNINGs (Check 6,
  DECISION-6) and COV-137 (Check 9b heading bindings for Ledger, Objectives,
  Partitions and Production Units); none stems from this amendment.
- No finding is `EXPECTED_CONSEQUENCE` any longer.

## Derivative packages and propagation (accepted route, Q-3)

| Package | Owner | Status | Evidence | Next required action |
|---|---|---|---|---|
| 9 `ScopeOfWork.md` contracts (DEL-10-03, 02-01, 02-03, 09-07, 01-04, 02-02, 03-03, 04-02, 01-01) | `scope-of-work` | **STALE**; to be revised per `SOW_REVISIONS.md` (sha256 `440d4d50…d00d`), 26 blocks | Register rows 1–9 | MODE=REVISE, one deliverable per brief, `STATUS_POLICY` `NO_STATUS_TOUCH`, closing with MODE=VERIFY. Frontmatter `decomposition_basis` is unchanged (O-22) |
| B-06a: `_Decomposition/checkpoint_snapshots/_LATEST_ACCEPTED.md` reading-rule note | integrator, with the REVISEs | **HELD**, DAG-002-bound | BASIS_AMENDMENT B-06a; register row 15 | Applied with the REVISE stage so that it falls inside the DAG-003 departure |
| Dependency registers: the 9 revised deliverables, plus DEL-04-01/02/03 re-quoting (ASC-ISS-008) and DEP-09-07-016 (ASC-ISS-007) | `dependency-extract` | **STALE** after REVISE | IMPACT_ASSESSMENT §7 step 5 | UPDATE, from `ScopeOfWork.md` only, with the guards of IMPACT §7 |
| DAG-002 | `project-dag` | CURRENT now (130/130 OK after H-1…H-3; no bound file changed). It **will depart** when the REVISEs and B-06a change its bound entries: +4 held arcs (N-18, N-21, N-24, X-1); DAG pending expected for DEL-02-01, 02-03, 03-02, 03-03, 01-04 | `_PostAcceptanceValidation/…/DAG_CURRENCY.txt` | Currency audit after REVISE, then TRIGGER=SUCCESSOR → DAG-003; owner checkpoint C |
| `_Decomposition/Coverage_Telemetry.json` | the decomposition owner | **STALE_REBUILD_REQUIRED** (carried from SCA-V4-001, DECISION-8 answer 2; ASC-ISS-004) | sha256 `178ec20a…f620`, unchanged | Rebuilt once, after this amendment, by a bounded brief; not written under SCA-V4-002 |
| 17 Design files | App v4 design undertaking | **STALE_REBUILD_REQUIRED** (carried; ASC-ISS-005; deferral record DECISION-8, confirmed at Q-15) | Propagation_Plan §6 | Re-pin to the amended texts at the next design pass, after the REVISEs |
| `_Decomposition/Consolidated_Coverage.csv` | scope-change (B-01 RECOMPUTE) | CURRENT (B-01 in the candidate; H-3 confirms no shift) | `_PostAcceptanceValidation/…/apply_log.json` | None |

**Active derivative surfaces (SOFTWARE):**
- **DIRECT_EDIT, applied:** `docs/HOST_INTEGRATION.md`, `SOFTWARE_DECOMP.md`
  (B-04), `Open_Issues.csv`, `Deliverables.csv`, `_Decomposition/_LATEST.md`,
  five `_CONTEXT.md`, and `_ScopeChange/_LATEST.md` (C-01).
- **DIRECT_EDIT, held:** `checkpoint_snapshots/_LATEST_ACCEPTED.md` (B-06a).
- **RECOMPUTE, applied:** `Consolidated_Coverage.csv` (B-01).
- **RECOMPUTE, open:** `Coverage_Telemetry.json`.
- **NO_CHANGE:** the rest, per Propagation_Plan §2.

KTY remediation and KTY metadata alignment do not apply (SOFTWARE).

## Closure verdict

**Closure verdict:** `OPEN_PENDING_DERIVATIVE_CLOSURE`

Authoritative truth is complete. These derivative packages are still open:
- the 9 SoWs, with B-06a;
- the registers;
- DAG-003;
- `Coverage_Telemetry.json`;
- the design re-pins.

No deliverable is `ISSUED` or `CHECKING` (among the nine: five IN_PROGRESS,
four INITIALIZED), so this amendment authorizes no reopening and holds
nothing for a reversal.

## Next owning workflows

1. `scope-of-work` MODE=REVISE for the 9 deliverables above, one per brief,
   each closing with MODE=VERIFY. Each brief carries:
   - `AMENDMENT_REF`: SCA-V4-002, this snapshot, the deliverable's register
     row and the register hash;
   - `REVISION_SCOPE` (that deliverable's blocks in `SOW_REVISIONS.md`);
   - `PRIOR_CONTRACT_SHA256` (the packet's prior hash);
   - `SOURCE_STATE`;
   - `STATUS_POLICY=NO_STATUS_TOUCH`.
   B-06a is applied by the integrator with these runs.
2. `dependency-extract` UPDATE, per deliverable, for the register rows.
3. `project-dag`: the DAG-002 currency audit, then the DAG-003 candidate, for
   owner checkpoint C.
4. The decomposition owner, with a bounded brief for `Coverage_Telemetry.json`.
5. The App v4 design undertaking, for the 17 re-pins.
6. `audit-scope-closure`, as the post-acceptance closure check for
   SCA-V4-002 and as the superseding snapshot for SCA-V4-001.

## COV-139 classification (closed)

The post-change audit flagged this folder as "historical snapshot residue"
because `Handoff_State.md` and `RUN_SUMMARY.md` were not yet written.
Classification at presentation: **EXPECTED_CONSEQUENCE** of the accepted
sequence (group-2 Handoff_State step 6; IMPACT_ASSESSMENT §7 step 3;
DECISION-2). The script's "historical" label is a wording limit. The finding
is closed: this folder holds every required artifact, and the H-4 rerun
confirms COV-139 absent. The artifacts as presented at group 3 are listed
with hashes in the group-3 `ACCEPTED_MANIFEST.csv`.

## Dispositions carried from V14

- **R-1** The C-02 effective-state folder keeps its committed name
  (`…_EFFECTIVE_STATE`); C-01 cites that path.
- **R-2** The packet cites `e9dc4633b` for the 16 SCA-V4-001 REVISEs; git
  shows `340ecf341` (SoWs) and `b585e5ebe` (registers). The C-02 record
  states the true commits. Packet bytes are not edited.
- **R-3** IMPACT_ASSESSMENT §4 names six packages; the baseline, post-change
  and post-acceptance audits use seven (PKG-05 added for register row 16).
  Disclosed to the owner in the checkpoint-B question; a stricter superset;
  no edit changed.
- **R-4** The Q-item split between the two snapshots is the recording
  role's reading; both manifests say so.
- **O-5** The packet's "6 `_CONTEXT.md` / 5 decomposition files" counts are
  transposed (5 files with 6 edits; 6 decomposition files). AffectedFiles
  are exact; the register governs.

## Carried from the predecessor

- SCA-V4-001's closure verdict is `OPEN_PENDING_DERIVATIVE_CLOSURE`, as its
  accepted `Handoff_State.md` and the effective-state record state.
- **ASC-ISS-001 is closed by this acceptance** (DECISION-3 "Effects"): the
  17 path-level rows are active through this snapshot's
  `Supersession_Map.csv`. The closure is confirmed by a superseding
  `audit-scope-closure` snapshot for SCA-V4-001; until it exists, the CA1
  record (`_Evaluation/ScopeClosureAudit/ScopeClosure_SCA-V4-001_2026-09-29_1222/`)
  keeps its `OPEN` status as written.
- `Coverage_Telemetry.json` and the 17 Design re-pins remain open under the
  owner's deferral (DECISION-8), sequenced after this amendment.
