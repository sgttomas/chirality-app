# SCA-V4-002 — effective state

**Record written:** 20260930T044342Z, by HELP_HUMAN (the integrator of run
`APP-V4-SCA002-20260929`), at HEAD `a5a4deaa72d3c7060523393131b48b6cfd0d018c`.

**Authority.** The SCA-V4-002 closure audit
`_Evaluation/ScopeClosureAudit/ScopeClosure_SCA-V4-002_2026-09-29_2233/`,
finding ASC-ISS-001 (MINOR, METADATA_STALE), and its rerun requirement: an
append-only record citing the completed downstream work.

**What this record is.** An append-only statement of where SCA-V4-002's
downstream work stands. It edits no SCA-V4-002 group-bound byte, names no
different active snapshot (`_ScopeChange/_LATEST.md` still names
`SCA-V4-002_2026-09-29_1901`), accepts nothing, and makes no release,
publication or reliance claim.

## Downstream work now complete

| Work | Evidence | Commit |
|---|---|---|
| 9 ScopeOfWork REVISE + VERIFY (NO_STATUS_TOUCH) | run folder `RV/RV_<DEL>.md` | `1efd4bcda` |
| B-06a reading-rule note on `_LATEST_ACCEPTED.md` | same | `1efd4bcda` |
| 11 dependency-extract UPDATEs (4 new arc rows; 34 re-quoted cells; DEP-09-07-016) | `DX/DX_<DEL>.md`, `DX/DX_SCC-CHECK.md` | `8cd783d8d` |
| Closure and currency audits (DEPARTURE, +4 held, 5 pending) | `_Evaluation/DepClosure/CLOSURE_APP_V4_SCA002_2026-09-29_2056`, `_Evaluation/DAGCurrency/CURRENCY_APP_V4_SCA002_2026-09-29_2057` | `b547125db` |
| DAG-003 accepted (owner DECISION-4) and published; currency CURRENT, 0 pending | `_DAG/DAG-003/ACCEPTANCE_RECORD.md`; `_Evaluation/DAGCurrency/CURRENCY_APP_V4_DAG003_ACCEPTED_2026-09-29_2218` | `a254be160` |
| Superseding SCA-V4-001 closure audit: CLOSED_WITH_OBSERVATIONS; ASC-ISS-001 closed | `_Evaluation/ScopeClosureAudit/ScopeClosure_SCA-V4-001_2026-09-29_2221` | `a5a4deaa7` |
| SCA-V4-002 closure audit: CLOSED_WITH_OBSERVATIONS | `…/ScopeClosure_SCA-V4-002_2026-09-29_2233` | this commit |

## Still open (owner-deferred, DECISION-8 of run APP-V4-BASIS-ALIGN-20260928)

- Coverage_Telemetry.json rebuild (STALE_REBUILD_REQUIRED), then an
  audit-decomp rerun with a script carrying the (f)/(g) pointer fix or a
  repaired base.
- The 17 Design files' re-pin to the amended basis texts, GUIDE last.
- The SWBPIPE handoff "local-first" line, carried with the next relay.

**Closure verdict of the amendment record:** OPEN_PENDING_DERIVATIVE_CLOSURE,
for those derivatives only.
