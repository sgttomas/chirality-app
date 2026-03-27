# RUN_SUMMARY — COV_POST_SCA001

**RUN_STATUS:** OK
**Timestamp:** 2026-03-26T17:48
**Decomposition Revision:** R2 — 2026-03-26 (SCA-001)
**Scope:** ALL
**Variant:** PROJECT

## Key Metrics

| Metric | Value |
|---|---|
| Partitions declared | 21 |
| Partitions found | 21 |
| Production units declared | 117 |
| Production units found | 117 |
| Forward coverage (packages) | 100.0% |
| Forward coverage (deliverables) | 100.0% |
| Reverse coverage | 100.0% |
| Context fidelity | 100.0% |
| Artifact presence | 100.0% |
| Objective coverage | 100.0% |
| Issues — BLOCKER | 0 |
| Issues — WARNING | 0 |
| Issues — INFO | 0 |

## Comparison vs Prior Run (PRE_SCA001)

| Metric | PRE_SCA001 | POST_SCA001 | Delta |
|---|---|---|---|
| Decomposition revision | R1 | R2 | Upgraded |
| Partitions declared | 21 | 21 | No change |
| Partitions found | 21 | 21 | No change |
| Production units declared | 117 | 117 | No change |
| Production units found | 117 | 117 | No change |
| Forward coverage (packages) | 100.0% | 100.0% | No change |
| Forward coverage (deliverables) | 100.0% | 100.0% | No change |
| Reverse coverage | 100.0% | 100.0% | No change |
| Issues — BLOCKER | 0 | 0 | No change |
| Issues — WARNING | 1 | 0 | -1 (RESOLVED) |
| Issues — INFO | 0 | 0 | No change |
| Overall status | WARNINGS | OK | Improved |

## Resolved Issues

- **COV-001 (WARNING):** Decomposition §9 Telemetry stated DeliverableCount=111 but actual count was 117. **RESOLVED** in R2 — §9 now correctly states DeliverableCount=117.

## Regressions

None.

## Verdict

All 9 checks PASS. The prior run's sole WARNING has been resolved. No regressions detected. The scope change (SCA-001) was cleanly incorporated: +1 IN scope item (SOW-0122), +1 OUT scope item (SOW-0206), no new deliverables or packages, no structural changes to the filesystem.
