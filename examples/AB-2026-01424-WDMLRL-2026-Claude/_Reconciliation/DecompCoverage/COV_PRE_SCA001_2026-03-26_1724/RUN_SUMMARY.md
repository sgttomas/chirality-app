# RUN_SUMMARY — AUDIT_DECOMP

| Field | Value |
|-------|-------|
| **RUN_LABEL** | PRE_SCA001 |
| **RUN_STATUS** | WARNINGS |
| **TIMESTAMP** | 2026-03-26T17:24 |
| **REQUESTED_BY** | SCOPE_CHANGE |
| **DECOMP_VARIANT** | PROJECT |
| **SCOPE** | ALL |

## Summary

All 9 checks executed. No BLOCKERs found. 1 WARNING identified (telemetry count mismatch in decomposition §9). Full forward and reverse coverage confirmed for all 21 packages and 117 deliverables. All deliverables are in SEMANTIC_READY lifecycle state with complete standard four-document sets and _CONTEXT.md files present.

## Metrics at a Glance

| Metric | Value |
|--------|-------|
| Packages declared | 21 |
| Packages found | 21 |
| Deliverables declared (§7 actual count) | 117 |
| Deliverables found | 117 |
| Forward coverage (packages) | 100.0% |
| Forward coverage (deliverables) | 100.0% |
| Reverse coverage | 100.0% |
| Context fidelity | 100.0% (all present, general match) |
| Artifact presence | 100.0% (standard four-doc set) |
| Objective coverage | 100.0% (8/8 objectives mapped) |
| Issues — BLOCKER | 0 |
| Issues — WARNING | 1 |
| Issues — INFO | 0 |

## Recommended Next Action

Fix the §9 Coverage & Telemetry `DeliverableCount` value from 111 to 117 in the decomposition document before proceeding with the scope change.
