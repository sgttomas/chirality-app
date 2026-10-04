# Handoff state — SCA-V4-003 (CANDIDATE, before group 3)

**Status.** Candidate awaiting the owner's checkpoint group 3. Groups 1 and 2
are accepted (DECISION-1 of run `APP-V4-SCA003-20261002`, 2026-10-03). Group 3
is **not accepted**: no accepted-state marker exists, and
`_ScopeChange/_LATEST.md` still names `SCA-V4-002_2026-09-29_1901`.

**Independent review: not yet run.** This file was written by node AK1
(stage 2), the role that applied the candidate, before the method's
independent review (step 5). That review may change it before group 3 is
presented.

## Candidate and pointer posture

| Item | Value |
|---|---|
| Candidate snapshot | `execution/_ScopeChange/SCA-V4-003_2026-10-03_1827/` |
| Posture | `ACCEPTED_PREDECESSOR` |
| Accepted predecessor | `execution/_ScopeChange/SCA-V4-002_2026-09-29_1901/` (closure `OPEN_PENDING_DERIVATIVE_CLOSURE`; effective state updated by `_PostAcceptanceValidation/SCA-V4-002_20261004T002903Z_EFFECTIVE_STATE/EFFECTIVE_STATE.md`) |
| `ACCEPTED_GROUP2_DECISION_SNAPSHOT` | `execution/_ScopeChange/checkpoint_snapshots/SCA-V4-003_GROUP-2_2026-10-03/` (committed `ec267bdb9f`; pointer `SCA-V4-003_GROUP-2_AUTHORIZED.md`) |
| Group-1 decision snapshot | `execution/_ScopeChange/checkpoint_snapshots/SCA-V4-003_GROUP-1_2026-10-03/` (committed `3e747b7685`) |
| Expected pre-acceptance pointer state | `_ScopeChange/_LATEST.md` sha256 `2b7938bc82aa9b08a2bd26d7f2c0169c538edb1e6ae5423d5757def968f0c2e1`, naming SCA-V4-002 (verified unchanged) |
| Candidate applied on | `ec267bdb9f` plus the uncommitted files listed under "Repository-change evidence" in `RUN_SUMMARY.md` |

## Authoritative action register

`Amendment_Actions.csv`, SHA-256
`9b7c2ce8fbf97ec0cf829c5024e03d19b4117c1ca50abaea4ec0b2c340346d1c`, as bound
in the group-2 `ACCEPTED_MANIFEST.csv` (the copy in this folder is
byte-identical). It has 23 `MODIFY` rows; `ScopeChanging` is `YES` on rows
2, 3, 4, 5, 7, 8, 9 and 10; `SupersessionBindingPresent` is `YES` on row 21.
`Intake_Actions.csv` is group-1 evidence only.

## Authoritative truth changed in this candidate

| Edit | Target | Result |
|---|---|---|
| B-02 option B (row 21), B-03 (row 22) | `_Decomposition/Open_Issues.csv` | sha256 `9c2d916c277f8ce4b847c9c532822d0566e59517ba9e0a86b650fe0450f3515d` (was `a1178218…80f0`); OI-009 `RESOLVED_BY_OWNER_DECISION`; OI-018 pointer; OPEN 23 → 22 |
| D-021 | `Supersession_Delta.csv` (this folder) | 1 row; `Supersession_Map.csv` 30 rows (29 carried + D-021), 0 findings |
| C-02 | `_PostAcceptanceValidation/SCA-V4-002_20261004T002903Z_EFFECTIVE_STATE/EFFECTIVE_STATE.md` | sha256 `ef2c22d74707a34b7804e2a3a6e83fa56f7f4f0219002b18e6b831e8abee6385` |

Nothing else in the decomposition package, no basis document, no
`_CONTEXT.md` or `_STATUS.md`, no ScopeOfWork, register or `_DAG` file was
written.

## Applied only after group-3 acceptance (acceptance-conditional), exactly

| # | Item | Target and old bytes | Slots / rule | Expected result |
|---|---|---|---|---|
| H-1 | B-01, the Change Register entry | `_Decomposition/SOFTWARE_DECOMP.md` (now `ea3388bc…d7d5`); old block "Snapshot: `../_ScopeChange/SCA-V4-002_2026-09-29_1901`.⏎⏎## Checkpoint and next stage" occurs once | `{ACCEPT_DATE}` = group-3 act date; `{AMENDMENT_SNAPSHOT}` = `SCA-V4-003_2026-10-03_1827`; `{Q5_CLAUSE}` = `, including the App act control in DEL-01-04`; `{OI009_CLAUSE}` = `Open_Issues OI-009 Status (RESOLVED_BY_OWNER_DECISION) and Consequence`; `{OI018_CLAUSE}` = ` and the OI-018 Consequence pointer`; `{D021_CLAUSE}` = `; and a Supersession_Delta row binding the GROUP3 OI-009 Status` (group-2 `DECISION.md`) | Determined by the act date; no `{` remains; nothing else in the file changes |
| H-2 | C-01, `_ScopeChange/_LATEST.md` in SPEC §11.2 form (BASIS_AMENDMENT C-01 text) | whole file (now `2b7938bc…c2e1`) | `{AMENDMENT_SNAPSHOT}` = `SCA-V4-003_2026-10-03_1827`; `{ACCEPT_DATE}`; `{CLOSURE_VERDICT}` (expected `OPEN_PENDING_DERIVATIVE_CLOSURE`); `{G1_DATE}` = `{G2_DATE}` = `2026-10-03`; `{C02_UTC}` = `20261004T002903Z`; `{UTC}` = the post-acceptance validation folder's stamp | The registered parser `_latest_pointer_target` must return the snapshot name |
| H-3 | Post-acceptance validation | new `_PostAcceptanceValidation/SCA-V4-003_{UTC}/` | compare applied bytes with H-1 and H-2; rerun the audit with `RUN/BASELINE/audit_checks.py` adapted only to the new active snapshot, scope PKG-01, 02, 03, 04, 05, 09, 10; COV-129 should then be absent | — |

No other edit waits for acceptance. An edit not on this list goes back to
the owner.

## Post-change validation

`RUN/POSTCHANGE/` (`COMPARISON.md`) shows **0 BLOCKER, 52 WARNING, 77 INFO**
(baseline 0 / 35 / 93):
- 35 WARNINGs are pre-existing.
- **16 Check 6 WARNINGs** were INFO before. They are pre-existing artifact
  absences of the six deliverables the Q-13 act moved to IN_PROGRESS. They
  are attributed to that separate owner act, not to the amendment.
- **COV-129** (Check 10, WARNING): this candidate folder lacked
  `Post_Change_Coverage.json`, `Decision_Log.md`, `Handoff_State.md` and
  `RUN_SUMMARY.md` at the audit. Classification: **`EXPECTED_CONSEQUENCE`**
  of the accepted sequence (group-2 `Handoff_State.md` step 5;
  IMPACT_ASSESSMENT §10 step 3; DECISION-1). The script's "historical
  residue" label is a wording limit. It closes now that these records exist.
  A control rerun of the same script in scratch, after this file and
  `RUN_SUMMARY.md` were drafted, gives 0 / 51 / 77: the IssueLog differs
  from POSTCHANGE only by the absent COV-129, and the Matrix is identical.
  The post-acceptance rerun (H-3) confirms it on the record.
- COV-116 and COV-121 (INFO) changed wording and hash. These are the
  intended effects of B-02 and B-03.
- The DEL-03-04 GUIDE change (`a68a9e06e2`) moves no finding.

| State | Value |
|---|---|
| `AuditState` | `WARNINGS` |
| `AdjustedAuditState` | `WARNINGS` (51, excluding COV-129) |

DAG-003 currency: 130/130 OK (`RUN/Application/DAG_CURRENCY.txt`).

## State fields

| Field | Value |
|---|---|
| `DecompositionTruthState` | `INCOMPLETE` (B-02, B-03 applied; B-01 waits for group 3) |
| `DerivativePackageState` | `INCOMPLETE` |
| `ContentRemediationState` | `NOT_REQUIRED` |
| `DownstreamRerunState` | `FROZEN` (until group 3) |
| `MetadataAlignmentState` | `NOT_REQUIRED` |
| `AuditState` | `WARNINGS` |
| `AdjustedAuditState` | `WARNINGS` |
| `ReadyForNextPhase` | `NOT_APPLICABLE` |

## Derivative packages and propagation after acceptance (accepted route, Q-3)

| Package | Owner | Status | Next required action |
|---|---|---|---|
| 19 `ScopeOfWork.md` (DEL-01-01…01-05, 02-01…02-04, 03-01…03-04, 04-01…04-03, 05-01, 09-06, 09-09) | `project-setup` INCREMENTAL → `scope-of-work` | STALE after acceptance; blocks in SOW_REVISIONS_A (`42c9167a…fc07`, 63) and _B (`d7b5cb24…94df`, 84) | MODE=REVISE, one deliverable per brief, then MODE=VERIFY; `STATUS_POLICY=NO_STATUS_TOUCH`; `AMENDMENT_REF` (SCA-V4-003, the accepted snapshot, the register row and hash), `REVISION_SCOPE`, `PRIOR_CONTRACT_SHA256` (all 19 equal the SOW_REVISIONS prior hashes now) |
| 20 `Dependencies.csv` and DEL-04-03 `_DEPENDENCIES.md` | `dependency-extract` | STALE after the REVISEs | UPDATE, from `ScopeOfWork.md` only, with the guards of IMPACT §10 and ARC_EFFECT §3 (DEL-04-01 gains no supplier; no SCC-002 row on DEL-09-06; R17-10; exactly the 10 new arcs; NR-03, NR-06, NR-10 not extracted; the 15 RP1-MX mirrors added) |
| DAG-003 | `project-dag` | CURRENT now (130/130); departs after the UPDATEs: +10 arcs (5 admitted, 5 held), SCCs unchanged | currency audit → TRIGGER=SUCCESSOR → DAG-004 (owner) |
| Design pins and GUIDE pin table (20 deliverables) | App v4 design undertaking | STALE after the REVISEs | re-pin at the next design touch, GUIDE last; with the ACCESS §13 follow-up (R22-7) |
| `_Decomposition/Coverage_Telemetry.json` | decomposition owner | STALE_REBUILD_REQUIRED (carried from SCA-V4-001; now off by one more open issue) | bounded rebuild, outside SCA-V4-003 |
| `_Decomposition/Consolidated_Coverage.csv` | scope-change | NO_CHANGE (no basis text changes) | none |

**Active derivative surfaces (SOFTWARE):**
- DIRECT_EDIT, applied: `Open_Issues.csv`.
- DIRECT_EDIT, held for group 3: `SOFTWARE_DECOMP.md` (B-01) and
  `_ScopeChange/_LATEST.md` (C-01).
- RECOMPUTE, open: `Coverage_Telemetry.json`.
- NO_CHANGE: the rest (Propagation_Plan §2).

KTY remediation and KTY metadata alignment do not apply (SOFTWARE).

## Closure verdict

**Expected closure verdict at group 3:** `OPEN_PENDING_DERIVATIVE_CLOSURE`.
After acceptance, authoritative truth is complete once H-1 is applied. These
remain open:
- the 19 REVISEs;
- the register UPDATE;
- DAG-004;
- the Design re-pins;
- `Coverage_Telemetry.json`.

No deliverable is `ISSUED` or `CHECKING` (all 20 targets are IN_PROGRESS), so
the amendment authorizes no reopening and holds nothing for a reversal.

## Remaining human decisions

- Group 3: accept or return this audited poststate, its closure verdict and
  the open obligations above.
- DAG-004 acceptance, after the REVISEs and UPDATEs.

## Next owning workflows

1. The independent review of this candidate (before group 3).
2. After acceptance: H-1, H-2, H-3; then `project-setup` INCREMENTAL →
   `scope-of-work` REVISE (19) and `dependency-extract` UPDATE (20).
3. `project-dag` currency audit and the DAG-004 candidate (owner).
4. The decomposition owner, for `Coverage_Telemetry.json`.
5. The App v4 design undertaking, for the re-pins.
6. `audit-scope-closure`, for SCA-V4-003.

## Carried from the predecessor

- SCA-V4-002 is `OPEN_PENDING_DERIVATIVE_CLOSURE` for
  `Coverage_Telemetry.json` only. Its updated effective-state note (C-02)
  records the Design re-pins and the SWBPIPE handoff line as done.
- Not in this amendment (OWNER_ITEMS "Not in this amendment"):
  - the DEL-04-01 → DEL-01-02 mirror and DEL-11-02's row for DEP-02-04-013
    (register owners);
  - the root `AGENTS.md` instruction notices (their own scope);
  - the Codex version-advance check (needs the owner's yes).
- Held items stay out until a later decision: Q-7 (S-01-4), Q-9 (the four
  A12-mapping rows), Q-14 (R-02-4), and the three DEFER basis items.

## Artifacts at writing (sha256 prefix; this file not self-listed)

| File | sha256 |
|---|---|
| `Amendment_Actions.csv` | `9b7c2ce8fbf97ec0` |
| `Amendment_Preview.md` | `23edb2ab81060c27` |
| `Brief.md` | `156bf1bb7ee81618` |
| `Decision_Log.md` | see `RUN_SUMMARY.md` |
| `Impact_Assessment.md` | `46ea15e5b2930c66` |
| `Intake_Actions.csv` | `c65b107afea246e7` |
| `Post_Change_Coverage.json` | `17fd4b0e8d13af9f` |
| `Pre_Change_Coverage.json` | `99f016cc3c3d40f7` |
| `Propagation_Plan.md` | `54891ede651588f4` |
| `Supersession_Delta.csv` | `9c84814a942ce0ba` |
| `Supersession_Map.csv` | `def52d1689a95ba4` |
