Latest: SCA-V4-002_2026-09-29_1901
Updated: 2026-09-29
Amendment: SCA-V4-002
Accepted predecessor: SCA-V4-001_2026-09-28_2155
Closure: OPEN_PENDING_DERIVATIVE_CLOSURE

# Active SCOPE_CHANGE Snapshot

**Status:** `OPEN_PENDING_DERIVATIVE_CLOSURE`
**Active snapshot:** `execution/_ScopeChange/SCA-V4-002_2026-09-29_1901/`
**Amendment:** `SCA-V4-002`, the App v4 follow-on alignment (run `APP-V4-SCA002-20260929`)
**Accepted:** checkpoint group 3 on 2026-09-29 (`execution/_ScopeChange/checkpoint_snapshots/SCA-V4-002_GROUP-3_2026-09-29/`); groups 1 and 2 (`execution/_ScopeChange/checkpoint_snapshots/SCA-V4-002_GROUP-1_2026-09-29/`, `execution/_ScopeChange/checkpoint_snapshots/SCA-V4-002_GROUP-2_2026-09-29/`)
**Accepted predecessor:** `execution/_ScopeChange/SCA-V4-001_2026-09-28_2155/` (closure verdict: `OPEN_PENDING_DERIVATIVE_CLOSURE` per `execution/_ScopeChange/_PostAcceptanceValidation/SCA-V4-001_20260930T010520Z_EFFECTIVE_STATE/EFFECTIVE_STATE.md`)
**Post-acceptance validation:** `execution/_ScopeChange/_PostAcceptanceValidation/SCA-V4-002_20260930T021014Z/`

SCA-V4-002 makes MODIFY actions only: DEL-10-03 REQ-005 ("local-first"
aligned with DECISION-4 D4-3); the consumption sentences behind arcs
N-18, N-21, N-24 and X-1; OI-001/002/012 text in DEL-09-07, DEL-01-04 and DEL-02-02; the
DEL-03-03 CLM-002 tail; and the HOST_INTEGRATION line layout. Topology is
unchanged: 11 packages, 41 deliverables and 262 scope IDs.

Open, separately governed: the 9 ScopeOfWork REVISEs (`scope-of-work` MODE=REVISE, `STATUS_POLICY` `NO_STATUS_TOUCH`) with the B-06a reading-rule note on `_Decomposition/checkpoint_snapshots/_LATEST_ACCEPTED.md`; the dependency-register UPDATE (`dependency-extract`); the DAG-002 departure and the DAG-003 candidate (owner checkpoint C); `_Decomposition/Coverage_Telemetry.json` (`STALE_REBUILD_REQUIRED`, owned by the decomposition owner; carried from SCA-V4-001); the 17 Design re-pins (carried from SCA-V4-001); the confirmation of ASC-ISS-001's closure by a superseding `audit-scope-closure` snapshot for SCA-V4-001 (the SCA-V4-001 effective-state record is `execution/_ScopeChange/_PostAcceptanceValidation/SCA-V4-001_20260930T010520Z_EFFECTIVE_STATE/EFFECTIVE_STATE.md`); `audit-scope-closure` for SCA-V4-002.

It makes no release, publication or reliance claim.
