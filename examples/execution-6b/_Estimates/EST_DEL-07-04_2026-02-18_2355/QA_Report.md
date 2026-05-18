# QA Report -- EST_DEL-07-04_2026-02-18_2355

## RUN_STATUS: OK

---

## 1. Schema Validity (Detail.csv)

| Check | Result |
|---|---|
| Detail.csv exists | PASS |
| All required columns present (LineID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes) | PASS |
| Method values valid (RATE_TABLE) | PASS |
| Allowance/parametric convention (N/A -- no ALLOWANCE or PARAMETRIC lines) | N/A |
| Amount = Qty x UnitRate for all rows | PASS (6 x 175 = 1050) |
| Currency consistent (CAD) | PASS |

## 2. Coverage

| Metric | Value |
|---|---|
| Deliverables in scope | 1 (DEL-07-04) |
| Deliverables covered (at least 1 priced line) | 1 |
| Deliverables missing | 0 |
| Deliverables blocked | 0 |
| Total line items | 1 |

## 3. Provenance Completeness

| Metric | Value |
|---|---|
| Total priced rows | 1 |
| Rows with non-TBD SourceRef | 1 |
| Provenance completeness | **100%** |
| Top missing-source offenders | None |

## 4. Basis-Consistency Check

| Check | Result |
|---|---|
| BASIS_OF_ESTIMATE | RATE_TABLE |
| All Detail.csv Method values | RATE_TABLE |
| Mixed methods detected | NO |
| ALLOW_MIXED_METHODS setting | FALSE |
| Consistency | **PASS** |

## 5. Blocker Analysis (from Dependencies)

| Metric | Value |
|---|---|
| Total dependencies loaded | 9 |
| Upstream prerequisites (EXECUTION class) | 2 (DEL-09-01, DEL-07-01) |
| Upstream interfaces (EXECUTION class) | 3 (DEL-07-02, DEL-07-03, DEL-08-01/DEL-08-02 combined with DEP-0704-E008/E009) |
| Upstream constraints | 1 (CCDC 14-2013 + Appendix J) |
| Downstream handovers | 1 (DEL-01-02) |
| Anchor dependencies | 2 (SOW-0022, OBJ-002) |
| **Dependencies blocking estimate** | **0** (no dependency prevents pricing) |

Note: Dependencies inform content readiness, not pricing. The CCDC 14-2013 constraint (DEP-0704-E006) has status ASSUMPTION (specific clauses not yet located), but this does not block the cost estimate.

## 6. Warnings

| ID | Severity | Description |
|---|---|---|
| W-001 | LOW | Decomposition lists "PM / Construction Manager" as responsible parties for DEL-07-04, but Level_of_Effort.csv assigns only PM (R-02) hours. If Construction Manager review/input is expected, the estimate may be understated by 2-4 hours ($310-$620 CAD). See ASM-002. |

## 7. What to Fix for a Cleaner Rerun

1. **Confirm whether Construction Manager (R-15) hours should be added to DEL-07-04 in Level_of_Effort.csv.** The decomposition suggests dual responsibility (PM + CM) but only PM hours are present.
2. No other gaps identified. All sources are complete and consistent for the current scope.

## 8. Write Quarantine Verification

All files written exclusively under:
`test/execution-6b/_Estimates/EST_DEL-07-04_2026-02-18_2355/`

No files outside `_Estimates/` were created, modified, or deleted.
