# Handoff state — SCA-V4-001 (ACCEPTED, active snapshot)

**Status.** The owner accepted checkpoint group 3 on 2026-09-29 (DECISION-8:
"Accept (Recommended)"). This folder is now the immutable accepted amendment
snapshot, and `_ScopeChange/_LATEST.md` names it.

This file, `RUN_SUMMARY.md` and `Decision_Log.md` were finalized after the
act by node AK2. The candidate version of this file, which the owner
accepted, is sha256 `17713b07ffaf699e1630ee69a5ebfa124c16d25b28026457bcff7485f4647e2c`
(at `9ae24fc0f`), and the group-3 `ACCEPTED_MANIFEST.csv` binds it.

`Brief.md` keeps its candidate standing line because the group-1 manifest
binds its bytes; this file and `_LATEST.md` govern the standing.

## Accepted snapshot and decision records

| Item | Path |
|---|---|
| **Accepted amendment snapshot** | `execution/_ScopeChange/SCA-V4-001_2026-09-28_2155/` |
| Active pointer | `execution/_ScopeChange/_LATEST.md` |
| Group 1 (DECISION-7) | `execution/_ScopeChange/checkpoint_snapshots/SCA-V4-001_GROUP-1_2026-09-28/` |
| Group 2 (DECISION-7) | `execution/_ScopeChange/checkpoint_snapshots/SCA-V4-001_GROUP-2_2026-09-28/` |
| Group 3 (DECISION-8) | `execution/_ScopeChange/checkpoint_snapshots/SCA-V4-001_GROUP-3_2026-09-29/` |
| Post-acceptance validation (H-5) | `execution/_ScopeChange/_PostAcceptanceValidation/SCA-V4-001_20260929T132946Z/` |
| Post-acceptance audit | `execution/_Coordination/AgentRuns/APP-V4-BASIS-ALIGN-20260928/POSTACCEPT/` |

- **Pointer posture:** `FIRST_AMENDMENT`. There is no predecessor, and
  `_LATEST.md` did not exist before this act.
- **Authoritative action register:** `Amendment_Actions.csv`, SHA-256
  `069645d979efa1e0a20f50194acca08afa8715ce647f36ad507c5bf2b76f14d2`
  (47 `MODIFY` rows), as bound in the group-2 `ACCEPTED_MANIFEST.csv`.
  `Intake_Actions.csv` is group-1 evidence only.
- **Supersession:** the 11 bindings in `Supersession_Delta.csv` are active
  through `Supersession_Map.csv` (sha256 `e8e43320…a801`).

## Authoritative truth changed

- **Candidate, accepted as presented (applied at `230bf1e64`):**
  - BASIS_AMENDMENT Part A (A01–A06, A08–A16) in the four basis documents;
  - Part B D-01…D-14b and D-16 in the decomposition package;
  - the B7 `_CONTEXT.md` mirrors;
  - the first B8 recompute.
- **Acceptance-conditional, applied after the act (2026-09-29, node AK2):**

| # | Item | Target | Result sha256 |
|---|---|---|---|
| H-1 | A07, three pairs (`{AMENDMENT_ID}` = SCA-V4-001; `{ACCEPT_DATE}` = 2026-09-29) | `docs/PRD.md` | `bb6e786f7a6c01dc5ce2f16f58e6c600989a12808ff47ce4fd87924bcc6c49bd` |
| H-2 | A17a | `docs/ARCHITECTURE.md` | `317d5789272c5206599936fa9b4e68551b30016d226b88039f0153afa02d828c` |
| H-2 | A17b | `docs/HOST_INTEGRATION.md` | `6c6854f941c714d8287bf799e1427bd4d99450847341bdf885ce4158d77eb122` |
| H-2 | A17c | `docs/EXAMINATION.md` | `471798bc2f2dc0202ae40d9d5cf033a22ae41af2a0afdf58032cf37a687957d0` |
| H-3 | D-15, the new `## Decision Log` (`{AMENDMENT_SNAPSHOT}` = `SCA-V4-001_2026-09-28_2155`) | `_Decomposition/SOFTWARE_DECOMP.md` | `7434058164f9e53f146793b85c38845a562fbc9ffd46f2b97de18e8d597e5747` |
| H-4 | B8, second recompute: SHA256, ReadSnapshot and SourceLine of 126 rows. `Standing` already carries "amended by SCA-V4-001" on 9 rows and is not appended again | `_Decomposition/Consolidated_Coverage.csv` | `4eee4bcb1cb296a9e96f9c44f934f19913dd827b43666475505e684a646a8db1` |
| H-5 | Post-acceptance validation, plus the audit-decomp rerun over the seven packages | `_PostAcceptanceValidation/SCA-V4-001_20260929T132946Z/` | see that record |

Each filled "old" block matched exactly once. D-15 is applied verbatim,
including "where accepted" (V11 F7; the owner offered no correction). Reading
B8's "recompute after the Part A edits" as applying again after A07/A17 is
the recorder's reading (V11 F1), and it is listed as H-4.

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
- `DownstreamRerunState` is `IN_PROGRESS` because DECISION-8 authorizes the
  propagation, and no rerun has completed yet.
- The post-acceptance audit (`POSTACCEPT/`) finds 0 BLOCKER, 38 WARNING and
  94 INFO, the same counts as POSTCHANGE. The Change Register part of
  COV-131 is now closed: "Decision Log" binds at rank exact. COV-131 stays a
  WARNING only for the pre-existing heading bindings (Ledger, Objectives,
  Partitions, Production Units).
- The 37 lifecycle WARNINGs come from DECISION-6, not from this amendment.
- No finding is `EXPECTED_CONSEQUENCE` any longer.

## Derivative packages and propagation

| Package | Owner | Status | Evidence | Next required action |
|---|---|---|---|---|
| 16 `ScopeOfWork.md` contracts: the 14 IN_PROGRESS (DEL-01-01, 02-01, 02-03, 03-01, 03-02, 03-03, 03-04, 04-01, 04-02, 04-03, 05-01, 05-02, 09-06, 09-09) plus DEL-09-07 and DEL-08-01 (INITIALIZED) | `project-setup` INCREMENTAL → `scope-of-work` | **STALE**; to be revised per `SOW_REVISIONS.md` (sha256 `9b4d700d…7d27b`) | Register rows 32–47; Propagation_Plan §5 | `scope-of-work` MODE=REVISE, one deliverable per brief, closing with MODE=VERIFY. Frontmatter `decomposition_basis` is unchanged (O-22) |
| Dependency registers: `Dependencies.csv` and `_DEPENDENCIES.md` (69 rows; 50 deferred) | `dependency-extract`, per deliverable | **STALE**. The rows are in `DAG_PREP/REGISTER_CHANGES.md` | `AgentRuns/APP-V4-BASIS-ALIGN-20260928/DAG_PREP/` | After the REVISE runs |
| DAG-001 | `project-dag` | CURRENT now (130/130 OK after H-1…H-4). It **will depart** when the SoW REVISE runs change its bound entries | `_PostAcceptanceValidation/…/DAG_CURRENCY.txt` | Run the currency audit after REVISE, then `TRIGGER=SUCCESSOR` for the DAG-002 candidate. Owner checkpoint C decides |
| `_Decomposition/Coverage_Telemetry.json` | **the decomposition owner** | **STALE_REBUILD_REQUIRED** (COV-119/120, and the inputs are now stale). DECISION-8 answer 2: "Record as stale, fix later (Recommended)" | The register-derivable values are in `POSTCHANGE/projections.json` | Write a bounded brief that names the writer and the exact bytes. It is not written under SCA-V4-001 |
| Design files (17) that pin the basis docs | App v4 design undertaking | STALE_REBUILD_REQUIRED | Propagation_Plan §5 | Re-pin to the amended texts at the next design pass |
| `_Decomposition/Consolidated_Coverage.csv` | scope-change (B8 RECOMPUTE) | CURRENT (H-4) | `_PostAcceptanceValidation/…/apply_log.json` | None |

**Active derivative surfaces (SOFTWARE):**
- **DIRECT_EDIT, applied:** the four docs, `SOFTWARE_DECOMP.md`,
  `ScopeLedger.csv`, `Vocabulary_Map.csv`, `Deliverables.csv`,
  `Packages.csv`, `Open_Issues.csv`, and four `_CONTEXT.md`.
- **RECOMPUTE, applied:** `Consolidated_Coverage.csv`.
- **RECOMPUTE, open:** `Coverage_Telemetry.json`.
- **NO_CHANGE:** the rest, per Propagation_Plan §5.

KTY remediation and KTY metadata alignment do not apply (SOFTWARE).

## Closure verdict

**Closure verdict:** `OPEN_PENDING_DERIVATIVE_CLOSURE`

Authoritative truth is complete. These derivative packages are still open:
- the 16 SoWs;
- the registers;
- DAG-002;
- `Coverage_Telemetry.json`;
- the design re-pins.

No deliverable is `ISSUED` or `CHECKING` (27 INITIALIZED, 14 IN_PROGRESS), so
this amendment authorizes no reopening and holds nothing for a reversal.

## Next owning workflows

1. `project-setup` in `INCREMENTAL` mode, which routes `scope-of-work`
   MODE=REVISE for the 16 deliverables above, one per brief. Each brief
   carries:
   - `AMENDMENT_REF`: SCA-V4-001, this snapshot, the deliverable's register
     row and the register hash;
   - `REVISION_SCOPE`;
   - `PRIOR_CONTRACT_SHA256`;
   - `SOURCE_STATE`;
   - `STATUS_POLICY=NO_STATUS_TOUCH`.
2. `dependency-extract`, per deliverable, for the register rows.
3. `project-dag`: the DAG-001 currency audit, then the DAG-002 candidate, for
   owner checkpoint C.
4. The decomposition owner, with a bounded brief for `Coverage_Telemetry.json`.
5. `audit-scope-closure`, as the post-acceptance closure check of the setup
   and the downstream reruns.
6. `scope-change` for SCA-V4-002, after SCA-V4-001 closes (see the residuals).

## Residuals outside SCA-V4-001

- **DEL-10-03 `ScopeOfWork.md` REQ-005.** It still reads "the minimal
  local-first host loop". It is routed to the follow-on amendment
  **SCA-V4-002**, after SCA-V4-001 closes (DECISION-8 answer 3: "Small
  follow-on amendment (Recommended)"). It is not edited here.
- **`_Coordination/HANDOFF_SWBPIPE_DOMAINS.md` l.22** ("local-first host
  operation"). This note is carried with the next relay to SWBPIPE,
  together with the DECISION-5 obligations.
- **`_Decomposition/Allocation_Rationale.csv`.** It stays NO_CHANGE as a
  historical allocation rationale, as the owner accepted.
- **`tools/query/scan_next_amendment_id.sh`.** It is zsh by design and works
  when invoked directly. Under `bash` its quoted regex rejects every prefix.
  This is a tooling observation only; a portability fix would be a
  separately authorized Root tooling change.

## Crosswalk for inconsistent action IDs (V11 residual 4)

The hash-bound register is not changed. The register rows map to the
BASIS_AMENDMENT edits as follows:

| Register row | BASIS_AMENDMENT edit | State |
|---|---|---|
| 7 | A07 (3 pairs) | applied as H-1 |
| 11 | A11a + A11b | applied in the candidate |
| 17 | A17a–c | applied as H-2 |
| 30 | D-16 + D-15 | D-16 applied in the candidate; D-15 applied as H-3 |
| 31 | B8 | first pass in the candidate; second pass as H-4 |

IMPACT §3 and §3.1 differ in `EntityID` for A07, A11 and A17 (Decision_Log
E-5). All of those rows are `EntityType` `OTHER`.

## Process disclosure (V11 F3)

The group-1 manifest binds a candidate `Brief.md` that already describes the
post-change audit. The group-1 snapshot bytes were therefore finalized after
application, and application landed in the same commit (`230bf1e64`). The
snapshots are not rewritten; this note discloses the sequence. For later
amendments, each decision snapshot should be committed before the next stage
applies.

**Minor notes carried:**
- V11 F4: only A07's first pair carries `{ACCEPT_DATE}`.
- V11 F5: the register uses `;` separators in DownstreamReruns; it is
  hash-bound.
- V11 F6: the post-change audit was run by the applying node and reproduced
  by V11.
- V11 F7: D-15's "where accepted" is applied verbatim.
- V11 F8: the standing lines of `Amendment_Preview.md` and
  `Propagation_Plan.md`.
