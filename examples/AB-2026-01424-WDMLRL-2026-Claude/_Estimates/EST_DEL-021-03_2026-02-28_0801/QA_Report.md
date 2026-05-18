# QA Report — EST_DEL-021-03_2026-02-28_0801

**RUN_STATUS: OK**

---

## Schema Validity

### Items.csv

| Check | Result |
|---|---|
| File parseable | PASS |
| Required columns present (ItemID, DeliverableID, Description, Qty, Unit, PricingMode, SourceDoc, SourceSection, Notes) | PASS |
| All rows have DeliverableID = DEL-021-03 | PASS |
| PricingMode values valid (UNIT_RATE or LUMP_SUM) | PASS |
| Lump-sum convention (Qty=1, Unit=LS) | PASS — applied to ITEM-001 through ITEM-005 |
| SourceDoc values valid (Datasheet, Specification, Procedure) | PASS |
| No TBD quantities in Items.csv | PASS — all quantities determined from Level_of_Effort.csv or set to 1 for lump-sum |
| Total items | 13 |

### Detail.csv

| Check | Result |
|---|---|
| File parseable | PASS |
| Required columns present (LineID, ItemID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes) | PASS |
| ItemID references valid (each maps to Items.csv) | PASS |
| Method values valid (PARAMETRIC) | PASS |
| Allowance/parametric convention (Qty=1, Unit=LS, UnitRate=Amount for LS items) | PASS — applied to L-001 through L-005 |
| Currency consistent | PASS — all CAD |
| TBD amounts flagged | PASS — 0 TBD lines; all 13 lines fully priced |
| Amount arithmetic (Qty * UnitRate = Amount) | PASS — verified for all 13 lines |
| Total lines | 13 |

### Summary.md

| Check | Result |
|---|---|
| File parseable | PASS |
| RunID matches snapshot directory | PASS — EST_DEL-021-03_2026-02-28_0801 |
| Currency matches Run_Context | PASS — CAD |
| CBS totals match Detail.csv rollup | PASS — INS $74,000 (5 lines) + LAB $7,960 (8 lines) = $81,960 (13 lines) |
| Labour hours match Detail.csv | PASS — 60 total hours across 8 roles |

### Cross-File Consistency

| Check | Result |
|---|---|
| Items.csv row count matches Detail.csv row count | PASS — 13 items, 13 lines |
| All ItemIDs in Detail.csv exist in Items.csv | PASS |
| CBS codes in Detail.csv match Summary.md CBS table | PASS — INS and LAB |
| WBS_PackageID consistent | PASS — all PKG-021 |
| WBS_DeliverableID consistent | PASS — all DEL-021-03 |

---

## Quantity Takeoff Coverage

| Deliverable | Items Extracted | Documents Read | Documents Missing |
|---|---|---|---|
| DEL-021-03 | 13 | 4 of 4 (Datasheet, Specification, Guidance, Procedure) | None |

**Coverage assessment:** All four production documents were read. Priceable items were extracted from:
- Datasheet: 1 item (builders risk, from coverage table)
- Specification: 4 items (REQ-INS-001 through REQ-INS-004 coverage policies)
- Procedure: 8 items (labour by role from Level_of_Effort.csv aligned to procedural steps)

---

## Pricing Coverage

| Metric | Value |
|---|---|
| Total items | 13 |
| Items priced | 13 |
| Items TBD | 0 |
| Pricing coverage | 100.0% |

All 13 line items are fully priced. The 3 previously-TBD insurance premium lines (WCB, E&O, Employer's Liability) have been resolved using FP-06, FP-07, and FP-08 from Fees_Permits_Insurance.csv.

---

## Provenance Completeness

| Metric | Value |
|---|---|
| Lines with SourceRef | 13 of 13 (100.0%) |
| Lines with "location TBD" | 0 of 13 (0.0%) |

All 13 lines have traceable SourceRef values pointing to specific rows in Professional_Staff_Rates.csv, Level_of_Effort.csv, or Fees_Permits_Insurance.csv.

---

## Basis-Consistency Checks

| Check | Result |
|---|---|
| BASIS_OF_ESTIMATE | PARAMETRIC |
| Method values in Detail.csv | All PARAMETRIC |
| ALLOW_MIXED_METHODS | TRUE (allowed but not needed; all lines are PARAMETRIC) |
| FALLBACK_POLICY | ALLOW_PARAMETRIC — applied; all lines now priced using parametric data |
| Basis consistency | PASS — no method mix violations |

---

## Scope Coverage

| Metric | Value |
|---|---|
| Deliverables in scope | 1 (DEL-021-03) |
| Deliverables estimated | 1 |
| SOW items mapped | SOW-0102 (insurance coverage per S4.2), SOW-0103 (name County as additional insured) |
| SOW items covered by line items | Both — SOW-0102 maps to ITEM-001 through ITEM-005; SOW-0103 covered within policy conditions (no separate cost line) |

---

## Confidence Distribution

| Confidence Level | Line Count | Amount (CAD) |
|---|---|---|
| MED | 10 | 30,960 |
| LOW | 3 | 54,000 |
| **Total** | **13** | **81,960** |

The 3 LOW-confidence lines (L-003 WCB $28,000, L-004 E&O $18,000, L-005 Employer's Liability $8,000) are newly resolved using parametric ranges with wide bands. All other lines are MED confidence.

---

## Warnings Summary

| # | Severity | Description |
|---|---|---|
| W-001 | MODERATE | Builders risk ($14,000) may not be required per RFP S4.2; depends on CCDC 14-2013 review |
| W-002 | MODERATE | Insurance premiums are contract-value-dependent; parametric ranges are wide (e.g., WCB $15,000-$45,000; E&O $12,000-$25,000) |
| W-003 | MODERATE | 3 of 5 insurance premium lines are LOW confidence; actual premiums will depend on final contract value, payroll, and claims history |
| W-004 | LOW | E&O tail coverage cost not included; may be needed for 2-year guarantee period |
| W-005 | LOW | Subcontractor insurance costs excluded; assumes individual subcontractor responsibility |
| W-006 | LOW | Broker fees assumed included in premium amounts; no separate line item |

---

## Comparison to Prior Run (EST_DEL-021-03_2026-02-26_2233)

| Metric | Prior Run | This Run | Delta |
|---|---|---|---|
| RUN_STATUS | WARNINGS | OK | Improved |
| Items priced | 10 of 13 | 13 of 13 | +3 resolved |
| Pricing coverage | 76.9% | 100.0% | +23.1 pp |
| Provenance completeness | 76.9% | 100.0% | +23.1 pp |
| Total estimate (CAD) | 27,960 (partial) | 81,960 (complete) | +54,000 |
| TBD count | 3 | 0 | -3 |

---

## What to Fix for a Cleaner Rerun

1. **Confirm builders risk requirement** — Review CCDC 14-2013 insurance provisions (GC 11.1) to confirm whether builders risk is required or optional. If not required, remove L-001 ($14,000).
2. **Narrow premium ranges** — Once project contract value is estimated, narrow the parametric ranges for all 5 insurance premium lines to improve confidence from LOW/MED to MED/HIGH.
3. **Resolve E&O tail coverage** — Determine whether tail coverage is contractually required for the 2-year guarantee period and price accordingly.
4. **Validate subcontractor insurance assumption** — Confirm with County whether a wrap-up or OCIP policy is needed; if so, add a line item.
5. **Obtain broker quotes** — Replace parametric premium estimates with actual broker quotes to move from PARAMETRIC to QUOTED basis.
