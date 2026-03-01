# QA Report — EST_DEL-021-02_2026-02-27_0540

## RUN_STATUS: WARNINGS

**Rationale:** Totals are meaningful and all items are priced, but the bond premium amounts are parametric allowances dependent on a TBD contract price. The estimate provides a reasonable parametric baseline but material assumptions remain.

---

## Schema Validity

### Items.csv

| Check | Result |
|---|---|
| File exists and is parseable | PASS |
| Required columns present (ItemID, DeliverableID, Description, Qty, Unit, PricingMode, SourceDoc, SourceSection, Notes) | PASS |
| PricingMode values valid (UNIT_RATE or LUMP_SUM) | PASS — 2 LUMP_SUM, 8 UNIT_RATE |
| All rows trace to a source document and section | PASS — 10/10 rows have SourceDoc and SourceSection |
| Qty values present (numeric or TBD) | PASS — all numeric |

### Detail.csv

| Check | Result |
|---|---|
| File exists and is parseable | PASS |
| Required columns present (LineID, ItemID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes) | PASS |
| Method values valid (QUOTE, RATE_TABLE, HISTORICAL, ALLOWANCE, PARAMETRIC) | PASS — all PARAMETRIC |
| Allowance/parametric convention: Qty=1, Unit=LS, UnitRate=Amount for lump-sum items | PASS — DL-001 and DL-002 follow convention |
| ItemID references valid | PASS — all 10 Detail rows reference valid Items.csv ItemIDs |

---

## Quantity Takeoff Coverage

| Metric | Value |
|---|---|
| Deliverables in scope | 1 (DEL-021-02) |
| Documents read | 4 of 4 (Datasheet, Specification, Guidance, Procedure) |
| Missing documents | 0 |
| Items extracted | 10 |
| Items with TBD quantities | 0 |

### Item Sources by Document

| SourceDoc | Item Count |
|---|---|
| Datasheet | 2 (bond premiums) |
| Specification | 1 (QA/QC verification) |
| Procedure | 7 (labour for steps execution) |

---

## Pricing Coverage

| Metric | Value |
|---|---|
| Total items | 10 |
| Items priced (non-TBD Amount) | 10 (100%) |
| Items with TBD Amount | 0 (0%) |
| Total priced amount | $46,960 CAD |

---

## Provenance Completeness

| Metric | Value |
|---|---|
| Total Detail rows | 10 |
| Rows with non-TBD SourceRef | 10 (100%) |
| Rows with TBD SourceRef | 0 (0%) |
| Provenance completeness | 100% |

---

## Basis-Consistency Checks

| Check | Result |
|---|---|
| BASIS_OF_ESTIMATE | PARAMETRIC |
| Methods used in Detail.csv | PARAMETRIC (10/10 lines) |
| Method mix consistent with basis | PASS — 100% PARAMETRIC, consistent with BASIS_OF_ESTIMATE |
| ALLOW_MIXED_METHODS | TRUE (not exercised — all methods are PARAMETRIC) |
| FALLBACK_POLICY | ALLOW_PARAMETRIC (not exercised — all items priced under primary basis) |

---

## Warnings

| # | Severity | Description | Action |
|---|---|---|---|
| W-001 | HIGH | Contract price is TBD — bond face amounts (50% each) cannot be verified; bond premium allowances are parametric estimates dependent on actual contract value | Reprice bond premiums when contract price is confirmed |
| W-002 | MEDIUM | Bond premium ranges are wide: Performance $12K–$35K, Payment $9K–$28K. Combined total could vary from $21K to $63K vs. recommended $39K | Obtain surety quotes once contract price is known |
| W-003 | LOW | All labour hours are parametric allocations from Level_of_Effort.csv with MEDIUM confidence | Monitor actual hours against estimates |
| W-004 | LOW | Surety company fees beyond premium (e.g., administrative fees, rider fees) are not separately itemized — assumed included in premium allowances | Confirm with surety company |

---

## What to Fix for a Cleaner Rerun

1. **Confirm contract price** to compute exact bond face amounts and obtain actual surety quotes for bond premiums (replace PARAMETRIC with QUOTE basis).
2. **Obtain surety quotes** for performance and payment bond premiums to replace parametric allowances with actual quoted costs.
3. **Validate labour hours** against actual project delivery experience once bonding process is complete.
4. **Itemize any surety company administrative fees** separately if applicable.
