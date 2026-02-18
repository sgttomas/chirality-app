# QA Report: EST_DEL-03-04_2026-02-18_2100

## RUN_STATUS: WARNINGS

Some totals exist but material TBDs and assumptions remain. The estimate is meaningful for proposal-stage budgeting but requires rerun with actual survey data post-award.

---

## S1 -- Write Quarantine

| Check | Result |
|-------|--------|
| All files written under _Estimates/ only | PASS |
| No modifications to deliverable content, lifecycle, decomposition, or dependency files | PASS |

## S2 -- Snapshot Created

| Check | Result |
|-------|--------|
| Snapshot folder EST_DEL-03-04_2026-02-18_2100 exists | PASS |

## S3 -- BASIS_OF_ESTIMATE Validated

| Check | Result |
|-------|--------|
| BASIS_OF_ESTIMATE = RATE_TABLE | PASS (valid enum) |
| Mixed methods authorized | PASS (ALLOW_MIXED_METHODS=TRUE; FALLBACK_POLICY=ALLOW_ALLOWANCE) |

## S4 -- Required Artifacts Exist

| Artifact | Status |
|----------|--------|
| Run_Context.md | PRESENT |
| Summary.md | PRESENT |
| QA_Report.md | PRESENT (this file) |
| Source_Index.md | PRESENT |
| Decision_Log.md | PRESENT |
| Assumptions_Log.md | PRESENT |
| WBS_CBS_Matrix.csv | PRESENT |
| Detail.csv | PRESENT |
| Blockers.md | PRESENT |

## S5 -- Detail Schema Integrity

| Check | Result |
|-------|--------|
| Detail.csv parseable | PASS |
| Required columns present (LineID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes) | PASS (14 columns) |
| Method values valid | PASS (12x RATE_TABLE, 6x ALLOWANCE) |
| Allowance convention (Qty=1, Unit=LS, UnitRate=Amount) | PASS (6 ALLOWANCE lines all use Qty=1, Unit=LS, UnitRate=Amount) |
| Amount = Qty x UnitRate (all rows) | PASS |
| ROUNDING=DOLLAR applied | PASS (all amounts are whole dollars) |
| Line count | 18 lines |

## S6 -- Provenance Discipline

| Check | Result |
|-------|--------|
| Priced rows with SourceRef | 18/18 (100%) |
| Rows with "location TBD" SourceRef | 0/18 (0%) |
| Provenance completeness | 100% |

**Top source references:**
- Underground_Utility_Rates.csv: 12 lines
- Fees_Permits_Insurance.csv: 5 lines
- Professional_Design_Fees.csv: 1 line

## S7 -- Status Reporting

| Check | Result |
|-------|--------|
| RUN_STATUS declared | WARNINGS |
| Reason | Material assumptions on utility run lengths (ASM-001 through ASM-003); DEC-004 allowance value pending Owner confirmation; Cold Storage utility requirements partially TBD |

## S8 -- Operator Acceptance Checklist

| Criterion | Status | Notes |
|-----------|--------|-------|
| RUN_STATUS is OK or WARNINGS with bounded gaps | PASS | WARNINGS; gaps are clearly enumerated |
| Basis-consistency checks pass | PASS | Mixed methods authorized; 67% RATE_TABLE / 33% ALLOWANCE |
| Provenance completeness reported | PASS | 100% (18/18 rows have SourceRef) |
| Scope coverage explicit | PASS | 1 deliverable in scope; 1 covered; 0 missing; 0 blocked |
| No writes outside _Estimates/ | PASS |

---

## Coverage Summary

| Metric | Value |
|--------|-------|
| Deliverables in scope | 1 |
| Deliverables covered | 1 (DEL-03-04) |
| Deliverables missing | 0 |
| Deliverables blocked | 0 |
| Line items produced | 18 |
| Total estimate | $226,930 CAD |

## Basis-Consistency Check

| Method | Line Count | Amount | Pct of Total |
|--------|-----------|--------|-------------|
| RATE_TABLE | 12 | $152,930 | 67% |
| ALLOWANCE | 6 | $74,000 | 33% |
| **Total** | **18** | **$226,930** | **100%** |

BASIS_OF_ESTIMATE = RATE_TABLE. ALLOWANCE lines are present due to:
1. DEC-004 (municipal tie-in allowance) -- explicitly required by brief as dual-method
2. Utility connection fees -- no rate table evidence exists; FALLBACK_POLICY=ALLOW_ALLOWANCE authorizes these
3. ALLOW_MIXED_METHODS=TRUE permits the mix

**Verdict:** Basis-consistency check PASS (deviations explicitly authorized and logged).

## Blocker Summary (from Dependency Evidence)

| Blocker Count | Status |
|--------------|--------|
| Upstream prerequisites PENDING | 4 (DEP-03-04-006, -007, -009, -010) |
| Upstream prerequisites blocking estimate | 0 (estimate proceeds with assumptions) |
| Upstream interfaces | 2 (DEL-03-01, DEL-03-02 -- parallel progression expected) |

## What to Fix for a Cleaner Rerun

1. **Obtain actual utility run lengths** from post-award survey files and underground services drawings. Replace ASM-001, ASM-002, ASM-003 with measured values and rerun.
2. **Confirm DEC-004 allowance value** with Owner. The $35,000 from UU-12 is a recommended value only.
3. **Confirm Cold Storage utility requirements** during design (ASM-004, ASM-005, ASM-006, ASM-007). Add or remove distribution lines as confirmed.
4. **Obtain Town of Penhold fee schedules** for utility connection fees. Replace FP-11 through FP-15 recommended values with actual fees.
5. **Confirm utility provider identities** and their connection standards (DEP-03-04-010). May affect both method and cost.
