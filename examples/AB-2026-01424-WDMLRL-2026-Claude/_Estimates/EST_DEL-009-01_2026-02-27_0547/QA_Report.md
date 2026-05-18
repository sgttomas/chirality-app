# QA Report — EST_DEL-009-01_2026-02-27_0547

## RUN_STATUS: WARNINGS

The estimate is substantially complete with all 9 line items priced. Warnings relate to LOW-confidence parametric estimates for 7 of 9 items where Level_of_Effort.csv does not provide hours. Labour pricing for 2 LoE-sourced items is MEDIUM confidence with full source traceability. All disbursement items are LOW confidence parametric allowances.

---

## Schema Validity

### Items.csv

| Check | Result |
|-------|--------|
| File parseable as CSV | PASS |
| Required columns present (ItemID, DeliverableID, Description, Qty, Unit, PricingMode, SourceDoc, SourceSection, Notes) | PASS |
| All PricingMode values valid (UNIT_RATE or LUMP_SUM) | PASS |
| Row count | 9 items |
| All rows trace to a source document and section | PASS |
| TBD quantities | 0 |

### Detail.csv

| Check | Result |
|-------|--------|
| File parseable as CSV | PASS |
| Required columns present (LineID, ItemID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes) | PASS |
| All Method values valid (PARAMETRIC) | PASS |
| Allowance/parametric convention respected (LS items have Qty=1, Unit=LS, UnitRate=Amount) | PASS |
| Row count | 9 lines |
| All ItemIDs in Detail.csv exist in Items.csv | PASS |

---

## Quantity Takeoff Coverage

| Metric | Value |
|--------|-------|
| Deliverables in scope | 1 (DEL-009-01) |
| Documents read | 5 (_CONTEXT.md, Datasheet.md, Specification.md, Guidance.md, Procedure.md) |
| Missing documents | 0 |
| Items extracted | 9 |
| Items with TBD quantity | 0 |

---

## Pricing Coverage

| Metric | Value |
|--------|-------|
| Total line items in Detail.csv | 9 |
| Items priced (non-TBD Amount) | 9 (100%) |
| Items with TBD Amount | 0 (0%) |
| Total estimate amount | $5,030.00 CAD |

---

## Provenance Completeness

| Metric | Value |
|--------|-------|
| Lines with non-TBD SourceRef | 9 / 9 (100%) |
| Lines with TBD SourceRef | 0 |

All lines have explicit source references pointing to pricing source files and/or assumption IDs.

---

## Basis-Consistency Check

| Metric | Value |
|--------|-------|
| BASIS_OF_ESTIMATE | PARAMETRIC |
| Method values in Detail.csv | PARAMETRIC (9/9 = 100%) |
| Mixed methods used | No |
| Basis-consistency | PASS — all lines match declared basis |

---

## Confidence Distribution

| Confidence | Line Count | Amount (CAD) | % of Total |
|-----------|------------|-------------|------------|
| MED | 2 | $1,530 | 30.4% |
| LOW | 7 | $3,500 | 69.6% |
| HIGH | 0 | $0 | 0.0% |

---

## Warnings

| # | Severity | Description | Affected Lines |
|---|----------|-------------|---------------|
| W-001 | MEDIUM | Level_of_Effort.csv provides only 2 of 6 labour roles for DEL-009-01 (10 of 29 hours, $1,530 of $4,030 labour). Remaining 4 roles (19 hours, $2,500) are parametrically estimated outside the LoE model at LOW confidence. | L-003, L-004, L-005, L-006 |
| W-002 | LOW | Pre-application consultation disbursement ($350) is a parametric allowance with no source pricing. Actual cost depends on proponent location and meeting logistics. | L-007 |
| W-003 | LOW | Courier/delivery cost ($150) is a parametric allowance with no source pricing. | L-008 |
| W-004 | LOW | Inspection coordination allowance ($500) is a parametric estimate for permit-related inspection scheduling. Scope boundary between development-permit inspections (DEL-009-01) and construction-phase inspections (DEL-009-04) is imprecise. | L-009 |
| W-005 | INFO | LoE Notes column for DEL-009-01 shows "PKG-009 Project Manager — TBD", indicating the LoE model may not have been fully validated for this deliverable. Hours accepted as-is per the parametric model. | L-001, L-002 |
| W-006 | INFO | Development permit fee explicitly excluded from estimate — County pays (R-01 §3.3.1; REQ-009-01-009). This is correct scope treatment, not a gap. | N/A |

---

## What to Fix for a Cleaner Rerun

1. **Expand Level_of_Effort.csv for DEL-009-01** to include Permitting Specialist (R-22), Document Controller (R-09), Senior Architect (R-11), and Civil Engineer (R-17) hours. This would elevate 4 lines from LOW to MEDIUM confidence and increase LoE coverage from 34% to 100% of labour.

2. **Add disbursement line items** to a disbursements pricing source (or to Fees_Permits_Insurance.csv) for pre-application consultation travel, courier/delivery, and inspection coordination. This would elevate 3 lines from LOW to MEDIUM confidence.

3. **Validate LoE Notes for PKG-009** — the "PKG-009 Project Manager — TBD" notation suggests the package-level effort model may be preliminary. Confirm hours with the Project Manager and Permitting Specialist.

4. **Clarify inspection coordination scope boundary** between DEL-009-01 (development permit inspections) and DEL-009-04 (construction-phase code compliance inspections) to avoid double-counting or gaps in the inspection effort estimate.

---

## Operator Acceptance Checklist

| Check | Status |
|-------|--------|
| RUN_STATUS is OK or WARNINGS with bounded gaps | PASS (WARNINGS — 7 LOW-confidence items totalling $3,500 / 69.6%; gaps are bounded and actionable) |
| Quantity takeoff reviewed for completeness | PASS (9 items extracted from all 4 documents + _CONTEXT.md) |
| Basis-consistency checks pass | PASS (100% PARAMETRIC) |
| Provenance completeness reported | PASS (100% non-TBD SourceRef) |
| Scope coverage explicit | PASS (1 deliverable, 0 excluded; permit fee exclusion documented) |
| No writes outside _Estimates/ | PASS |
