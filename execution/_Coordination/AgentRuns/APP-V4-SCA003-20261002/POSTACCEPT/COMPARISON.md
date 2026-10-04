# Post-acceptance audit vs post-change audit and simulation — SCA-V4-003 (H-3)

**Run.** `APP_V4_SCA_V4_003_POSTACCEPT`, 2026-10-04T01:00:17Z, by node AK2
(part 1; Type 2 TASK, Claude Code subagent; no delegation) of run
`APP-V4-SCA003-20261002`.

- **Subject:** the working tree at `84b520742d` (DECISION-2) plus the
  uncommitted acceptance-time edits: F-1 (the group-3 decision snapshot),
  H-1 (`SOFTWARE_DECOMP.md`), H-2 (`_ScopeChange/_LATEST.md`), and F-3 and
  F-4 (the accepted status lines). F-2 (`Decision_Log.md`) was written after
  this run; the script reads that file only for presence.
- **Scope:** **PKG-01, 02, 03, 04, 05, 09, 10** (32 deliverables).
- **Writes:** this folder only.

**Method.**
- `audit_checks.py` is byte-identical to `BASELINE/audit_checks.py`
  (`8c3bef06…b0d3`), unchanged as the presented H-3 requires (V24 m-1).
- `inventory.json` is a byte copy of the baseline's.
- `audit_structure.py` exit 0.

**Result.** **0 BLOCKER, 51 WARNING, 77 INFO** (POSTCHANGE: 0 / 52 / 77).
- **Check 10:** `active_snapshot_status` PASS and `handoff_state_status`
  PASS, with active snapshot `execution/_ScopeChange/SCA-V4-003_2026-10-03_1827`.
  No problem, no missing artifact, no residue.
- **Closure verdict read:** `OPEN_PENDING_DERIVATIVE_CLOSURE`. State fields
  are single-valued and allowed (DecompositionTruthState COMPLETE,
  DownstreamRerunState IN_PROGRESS).
- **Registered pointer parser:** target `SCA-V4-003_2026-10-03_1827`,
  `pointer_matches_active` True. No parser INFO.
- **Topology** is unchanged: 11 / 41 / 10 / 262.

## Against the simulation (`RUN/Application/SIMULATED_POSTACCEPT.md`)

`Decomp_Coverage_IssueLog.csv` and `Decomp_Coverage_Matrix.csv` are
**byte-identical** to the simulation's outputs. The simulation applied the
same H-1 bytes (`983199cc…a70d`, the same date) and a placeholder H-2 stamp;
the stamp is not read by any check.

## Against POSTCHANGE

| POSTCHANGE | POSTACCEPT | What differs | Attribution |
|---|---|---|---|
| COV-123 INFO (working `SOFTWARE_DECOMP.md` `ea3388bc…` vs GROUP3) | COV-123 INFO (`983199cc…` vs GROUP3) | the working hash | H-1 (B-01). The unchanged script still attributes the file to the SCA-V4-001/002 registers only (wording limit, disclosed) |
| COV-129 WARNING (candidate folder residue) | — | absent | The candidate records were written, and the folder is now the active snapshot. The `EXPECTED_CONSEQUENCE` classified at group 3 is closed |

Every other issue is identical, and the Matrix is identical.

**Input differences** (`POSTCHANGE/INPUT_MANIFEST.sha256` checked at this
subject). Four entries differ:
- `SOFTWARE_DECOMP.md` (H-1);
- `_ScopeChange/_LATEST.md` (H-2);
- `RUN/BRIEFS.md` and `RUN/OWNER_DECISIONS.md` (run records: the V24 and AK
  briefs; DECISION-2).

The candidate files added after POSTCHANGE are listed in this run's
`INPUT_MANIFEST.sha256`: 241 entries, the POSTCHANGE paths plus all 13
artifacts and the 3 group-3 snapshot files.
It was taken after F-2, so its `Decision_Log.md` entry is the finalized
file; the script reads that file only for presence.

**Known wording limits of the unchanged script** (disclosed, not edited):
- COV-121 and COV-123 attribute working-vs-GROUP3 differences only to the
  SCA-V4-001/002 registers.
- `expected_source.predecessor_amendment` reads SCA-V4-001.
- The parity extension lists `SOFTWARE_DECOMP.md`, `_ScopeChange/_LATEST.md`
  and `Open_Issues.csv` as differing from SCA-V4-002's accepted poststate.
  This is expected for the SCA-V4-003 edits.

**Classification.** No finding is new. The 51 WARNINGs are the 35
pre-existing ones plus the 16 Check 6 rows re-graded by the Q-13 act.
- `AuditState`: WARNINGS.
- `AdjustedAuditState`: WARNINGS. No finding is `EXPECTED_CONSEQUENCE` any
  longer.
