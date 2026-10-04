# Group-2 handoff — SCA-V4-003

**Decision.** Checkpoint group 2 is accepted, as recorded in `DECISION.md`
and `ACCEPTED_MANIFEST.csv` (owner act 2026-10-03, DECISION-1 of run
`APP-V4-SCA003-20261002`: "accept the remaining items as recommended"), on
the packet as committed at `60359d7372`.

**Authoritative register.** `checkpoint_snapshots/SCA-V4-003_GROUP-2_2026-10-03/Amendment_Actions.csv`,
SHA-256 `9b7c2ce8fbf97ec0cf829c5024e03d19b4117c1ca50abaea4ec0b2c340346d1c`
(23 rows; role `action register`). The packet's `Amendment_Actions.draft.csv`
is the same bytes and is bound only as what was presented. There is no
`Intake_Actions.csv`: the group-1 intake is the ledger and IMPACT_ASSESSMENT
§3, bound in the group-1 manifest. Resolved with
`tools/validation/check_amendment_reopen.py`'s own register lookup, read-only
over the working tree: it selects this file and the hash matches (unanchored;
no deliverable is ISSUED, so no reopening depends on it).

**Exact amendment, propagation plan and supersession input, by hash.** This
snapshot does not render `Amendment_Preview.md` or `Propagation_Plan.md`; it
binds their accepted sources: BASIS_AMENDMENT.md (`151bc6ff…35bf`; every
non-ScopeOfWork edit and the D-021 row), SOW_REVISIONS_A.md (`42c9167a…7fc07`)
and SOW_REVISIONS_B.md (`d7b5cb24…94df`; 147 ScopeOfWork blocks),
IMPACT_ASSESSMENT.md (`46ea15e5…35f3`; §10 propagation, §6 package roles) and
ARC_EFFECT.md (`25073317…94e7`; §4 departure). The prior map input is
SCA-V4-002's `Supersession_Map.csv` (`45502bf5…eb93`).

**Next owning stage.** Checkpoint-group-3 preparation from this snapshot
(`ACCEPTED_GROUP2_DECISION_SNAPSHOT`; AK1 stage 2, after HELP_HUMAN commits
both snapshots). Posture `ACCEPTED_PREDECESSOR`
(`ACCEPTED_PREDECESSOR_SNAPSHOT` =
`execution/_ScopeChange/SCA-V4-002_2026-09-29_1901/`). Candidate path
`execution/_ScopeChange/SCA-V4-003_2026-10-03_<HHMM>/` (set when it is
created):
1. Write the SCA-V4-002 effective-state note (BASIS_AMENDMENT C-02) in a new
   `_PostAcceptanceValidation/SCA-V4-002_{C02_UTC}_EFFECTIVE_STATE/` folder.
2. Apply B-02 (option B) and B-03 to `_Decomposition/Open_Issues.csv`,
   row-scoped, CRLF and quoting kept; the result must hash to
   `9c2d916c277f8ce4b847c9c532822d0566e59517ba9e0a86b650fe0450f3515d` (OPEN
   count 22). The current file must still hash to `a1178218…80f0` before the
   edit.
3. Write the candidate `Supersession_Delta.csv` as BASIS_AMENDMENT Part D
   exactly, and generate `Supersession_Map.csv` with
   `tools/coordination/accumulate_supersession_map.py` from SCA-V4-002's map
   (expected 30 rows, 0 findings).
4. Run the post-change audit with `RUN/BASELINE/audit_checks.py` over
   PKG-01, 02, 03, 04, 05, 09 and 10 and compare with the baseline; classify
   findings as `EXPECTED_CONSEQUENCE` or new. Attribute separately: the Q-13
   act (`baa6e618d7`; 16 Check 6 INFO → WARNING expected), the OI-009 status
   change (Check 9 wording and COV-116 counts), and the post-baseline Design
   edit to DEL-03-04 `Design/HOST_INTEGRATION_GUIDE.md` (`a68a9e06e2`).
5. Then the independent review, the candidate `RUN_SUMMARY.md` and
   `Handoff_State.md` with the exact acceptance-conditional edit list (B-01
   and C-01, slots as fixed in `DECISION.md`), and group 3 for the owner.

**Status of later stages.**

| Stage | State |
|---|---|
| Exact amendment and propagation decision | Accepted (this snapshot) |
| SCA-V4-002 effective-state note (C-02) | Not written at this record; after the group-1 snapshot is committed |
| Candidate poststate | Not started at this record |
| Acceptance-conditional edits (B-01, C-01) | Wait for group 3 |
| ScopeOfWork REVISE (19) | Wait for group 3 (`project-setup` INCREMENTAL → `scope-of-work` REVISE, `NO_STATUS_TOUCH`) |
| Register UPDATE (20) and DAG-004 | After the REVISEs (`dependency-extract` UPDATE; `project-dag` currency → SUCCESSOR; owner) |
| Design re-pins, GUIDE last | Next design touch after the REVISEs (outside the amendment) |
| `Coverage_Telemetry.json` | `STALE_REBUILD_REQUIRED`, carried; decomposition owner; outside SCA-V4-003 |
| Current basis | GROUP3 as amended by SCA-V4-001 and SCA-V4-002; `_ScopeChange/_LATEST.md` names `SCA-V4-002_2026-09-29_1901` |
| Pointer posture for group 3 | `ACCEPTED_PREDECESSOR` |

**State fields (at this record).**

| Field | Value |
|---|---|
| `DecompositionTruthState` | `NOT_STARTED` |
| `DerivativePackageState` | `INCOMPLETE` |
| `ContentRemediationState` | `NOT_REQUIRED` |
| `DownstreamRerunState` | `FROZEN` |
| `MetadataAlignmentState` | `NOT_REQUIRED` |
| `AuditState` | `NOT_RUN` (post-change) |
| `AdjustedAuditState` | `NOT_RUN` |
| `ReadyForNextPhase` | `NOT_APPLICABLE` |

**Remains unauthorized until group 3:**
- B-01 (Change Register entry) and C-01 (`_LATEST.md`);
- moving `_LATEST.md`, and any accepted-state marker on the SCA-V4-003
  candidate folder;
- any `ScopeOfWork.md`, `Dependencies.csv`, `_DEPENDENCIES.md`, `_DAG`,
  `_STATUS.md`, `_CONTEXT.md`, basis document or `Coverage_Telemetry.json`
  change, and any other decomposition file than `Open_Issues.csv`;
- DAG-004.

**Pointer.** `_ScopeChange/SCA-V4-003_GROUP-2_AUTHORIZED.md` is to be written
after this snapshot is complete. It lies outside AK1's write fence;
HELP_HUMAN writes it or authorizes it.

**Commit sequence (Q-16).** This snapshot and the register it binds are to
be committed, after the group-1 snapshot, before the application. AK1 has
read-only git and makes no commit; HELP_HUMAN commits.

Reopen only on a material departure from the accepted exact amendment or
register.
