# QA Report — AGG_Estimate_Collation_2026-02-18_2359

## Summary

| Check | Result | Notes |
|-------|--------|-------|
| All 38 deliverables located | PASS | 40 snapshot directories found (38 unique deliverables) |
| Detail.csv schema validation | PASS | All 40 files contain required columns (LineID, CBS, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence) plus preferred columns (WBS_PackageID, WBS_DeliverableID, Notes) |
| Run_Context.md present | PASS | All 40 snapshots have Run_Context.md |
| Assumptions_Log.md present | PASS | All 40 snapshots have Assumptions_Log.md |
| Risk_Register present | FAIL (expected) | No Risk_Register files found in any snapshot. Documented in Coverage.csv and Project_Risks.csv. |
| Amount = Qty x UnitRate check | PASS | All production line items verify: Amount = Qty x UnitRate (within rounding tolerance) |
| Currency consistency | PASS | All lines are CAD |
| Basis of Estimate consistency | PASS | All 40 snapshots report BASIS_OF_ESTIMATE = RATE_TABLE |
| LineUID uniqueness | PASS | All LineUIDs (FromDeliverableID::LineID) are unique across the consolidated dataset |
| Dual-nature separation (DEL-01-03) | PASS | Production lines (L-001 through L-003) separated from financial allowances (L-004 through L-007) |
| Dual-nature separation (DEL-01-04) | PASS | Production lines (A-010 through A-030) separated from construction pricing (B-*/C-*) |
| Dual-nature separation (DEL-01-05) | PASS | Production lines (A-010 through A-030) separated from construction pricing (B-*/C-*) |
| DEL-01-04/05 duplicate detection | PASS | 41 intentional duplicate pairs documented in Duplicates.csv |
| Package rollup completeness | PASS | All 10 packages represented in Project_Summary_WBS.csv |
| No source files modified | PASS | All writes under _Aggregation/ only |

## Totals Verification

| Metric | Value | Cross-check |
|--------|-------|-------------|
| Total production cost | $111,000 CAD | Sum of all PRODUCTION lines in Project_Detail.csv |
| Total production hours | 786 hours | Sum of all HR-unit PRODUCTION lines |
| Construction pricing (Schedule A view) | $7,710,000 CAD | Sum of CONSTRUCTION_PRICING lines from DEL-01-04 |
| Construction pricing (Schedule B view) | $7,710,000 CAD | Sum of CONSTRUCTION_PRICING lines from DEL-01-05 (mirrors Schedule A) |
| Financial allowances | $543,500 CAD | Sum of FINANCIAL_ALLOWANCE lines from DEL-01-03 |
| Grand total (production + financial allowances) | $654,500 CAD | $111,000 + $543,500 |

## Warnings

1. **Risk_Register gaps**: No risk registers were produced by any ESTIMATING run. Project-level risks are documented in BOE Section 8 and individual Assumptions_Log.md files, but no structured risk register data was available for collation.

2. **Bond premium calculation inconsistency**: DEL-01-03 uses full contract value ($12M) for premium calculations while DEL-01-04/05 use 50% of contract value. See Conflicts.csv CONFLICT-001/002.

3. **Fire protection uncertainty**: $108,000 fire protection line (DEL-01-04 B-420 / DEL-01-05 B-BLD-420) carries LOW confidence; AHJ determination pending. If not required, construction pricing reduces by $108,000 per schedule.

4. **CCIP insurance rate uncertainty**: $240,000 CCIP premium carries LOW confidence with a range of $180,000-$300,000 depending on insurer and risk profile.

## Coverage Summary

- Deliverables with Detail.csv: 38/38 (100%)
- Deliverables with Run_Context.md: 38/38 (100%)
- Deliverables with Assumptions_Log.md: 38/38 (100%)
- Deliverables with Risk_Register: 0/38 (0%)
- Schema status OK: 38/38 (100%)
