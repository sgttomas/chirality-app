# Blockers Report -- DEL-02-05

## Source

Dependency evidence from `Dependencies.csv` (18 rows; schema v3.1).

## Blockers Affecting Estimate Quality

| # | DependencyID | Type | Source Deliverable | Issue | Estimate Impact | Severity |
|---|-------------|------|--------------------|-------|-----------------|----------|
| 1 | DEP-0205-E12 | CONSTRAINT (External) | AHJ / Alberta Building Code | Applicable code editions not confirmed with AHJ; fire protection requirement is conditional | L-12 ($108,000) is LOW confidence; total could drop by 10.7% if fire protection not required | MEDIUM |
| 2 | DEP-0205-E08 | INTERFACE | DEL-02-02 | Compressed air scope boundary (CON-M-01) unresolved between DEL-02-05 and DEL-02-02 | No pricing impact on this estimate (compressed air excluded per brief cost ownership), but boundary needs confirmation | LOW |

## Prerequisites Noted (not blocking estimate, but relevant)

| DependencyID | Type | Source Deliverable | Note |
|-------------|------|--------------------|------|
| DEP-0205-E01 | PREREQUISITE | DEL-02-02 | Apparatus bay layout needed for exhaust design -- not needed for rate-table estimating (quantities confirmed via PP-11) |
| DEP-0205-E02 | PREREQUISITE | DEL-02-03 | PW bay layout needed for ventilation design -- not needed for rate-table estimating (quantities confirmed via PP-12) |
| DEP-0205-E03 | PREREQUISITE | DEL-02-01 | Architectural layout needed for design -- area zoning assumed per ASM-01 for estimating purposes |
| DEP-0205-E04 | PREREQUISITE | DEL-03-04 | Utility entry info needed for water fill station design -- not needed for unit-rate estimating |
| DEP-0205-E11 | CONSTRAINT | DEL-02-03 | PW bay count confirmation -- assumed 4 per PP-12 (CONFIRMED status); mitigated |

## Summary

- **Critical blockers:** 0
- **Medium blockers:** 1 (fire protection conditionality)
- **Low blockers:** 1 (compressed air boundary)
- **Informational prerequisites:** 5 (not blocking estimate at rate-table level)
