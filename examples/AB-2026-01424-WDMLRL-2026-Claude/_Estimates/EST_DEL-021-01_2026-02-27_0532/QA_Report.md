# QA Report — EST_DEL-021-01_2026-02-27_0532

## RUN_STATUS: WARNINGS

The estimate is substantially complete with all line items priced. Warnings relate to LOW-confidence parametric estimates for two non-labour items (bid bond premium and courier cost). Labour pricing is MEDIUM confidence with full source traceability.

---

## Schema Validity

### Items.csv

| Check | Result |
|-------|--------|
| File parseable as CSV | PASS |
| Required columns present (ItemID, DeliverableID, Description, Qty, Unit, PricingMode, SourceDoc, SourceSection, Notes) | PASS |
| All PricingMode values valid (UNIT_RATE or LUMP_SUM) | PASS |
| Row count | 10 items |
| All rows trace to a source document and section | PASS |
| TBD quantities | 0 |

### Detail.csv

| Check | Result |
|-------|--------|
| File parseable as CSV | PASS |
| Required columns present (LineID, ItemID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes) | PASS |
| All Method values valid (PARAMETRIC) | PASS |
| Allowance/parametric convention respected (LS items have Qty=1, Unit=LS, UnitRate=Amount) | PASS |
| Row count | 10 lines |
| All ItemIDs in Detail.csv exist in Items.csv | PASS |

---

## Quantity Takeoff Coverage

| Metric | Value |
|--------|-------|
| Deliverables in scope | 1 (DEL-021-01) |
| Documents read | 5 (_CONTEXT.md, Datasheet.md, Specification.md, Guidance.md, Procedure.md) |
| Missing documents | 0 |
| Items extracted | 10 |
| Items with TBD quantity | 0 |

---

## Pricing Coverage

| Metric | Value |
|--------|-------|
| Total line items in Detail.csv | 10 |
| Items priced (non-TBD Amount) | 10 (100%) |
| Items with TBD Amount | 0 (0%) |
| Total estimate amount | $9,610.00 CAD |

---

## Provenance Completeness

| Metric | Value |
|--------|-------|
| Lines with non-TBD SourceRef | 10 / 10 (100%) |
| Lines with TBD SourceRef | 0 |

All lines have explicit source references pointing to pricing source files and/or assumption IDs.

---

## Basis-Consistency Check

| Metric | Value |
|--------|-------|
| BASIS_OF_ESTIMATE | PARAMETRIC |
| Method values in Detail.csv | PARAMETRIC (10/10 = 100%) |
| Mixed methods used | No |
| Basis-consistency | PASS — all lines match declared basis |

---

## Confidence Distribution

| Confidence | Line Count | Amount (CAD) | % of Total |
|-----------|------------|-------------|------------|
| MED | 8 | $7,960 | 82.8% |
| LOW | 2 | $1,650 | 17.2% |
| HIGH | 0 | $0 | 0.0% |

---

## Warnings

| # | Severity | Description | Affected Lines |
|---|----------|-------------|---------------|
| W-001 | MEDIUM | Bid bond premium estimated parametrically at LOW confidence; no explicit bid bond premium in Fees_Permits_Insurance.csv. Actual premium depends on surety underwriting and final bid amount. | L-009 |
| W-002 | LOW | Courier delivery cost estimated parametrically at LOW confidence; no source pricing available. | L-010 |
| W-003 | INFO | Labour hours sourced from Level_of_Effort.csv show "PKG-021 TBD — TBD" in Notes column, indicating the LoE model may not have been fully validated for this package. Hours are accepted as-is per the parametric model. | L-001 through L-008 |

---

## What to Fix for a Cleaner Rerun

1. **Add a bid bond premium line to Fees_Permits_Insurance.csv** with a range specific to bid bonds (distinct from performance bond premium FP-01). This would elevate L-009 from LOW to MEDIUM confidence.
2. **Add a courier/delivery allowance line to Fees_Permits_Insurance.csv** or a separate logistics cost source. This would elevate L-010 from LOW to MEDIUM confidence.
3. **Validate Level_of_Effort.csv for PKG-021** — the "TBD — TBD" notes in the LoE source suggest the package-level effort model may be preliminary. Confirm hours with the Contract Administrator and Project Manager.
4. **Confirm bid amount range** — the bid bond premium is sensitive to the total bid amount. Once the bid amount is estimated, the bid bond premium should be re-estimated with surety input.

---

## Operator Acceptance Checklist

| Check | Status |
|-------|--------|
| RUN_STATUS is OK or WARNINGS with bounded gaps | PASS (WARNINGS — two LOW-confidence items totalling $1,650 / 17.2%) |
| Quantity takeoff reviewed for completeness | PASS (10 items extracted from all 4 documents) |
| Basis-consistency checks pass | PASS (100% PARAMETRIC) |
| Provenance completeness reported | PASS (100% non-TBD SourceRef) |
| Scope coverage explicit | PASS (1 deliverable, 0 excluded) |
| No writes outside _Estimates/ | PASS |
