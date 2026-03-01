# QA Report — EST_DEL-021-03_2026-02-26_2233

**RUN_STATUS: WARNINGS**

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
| TBD amounts flagged | PASS — 3 lines (L-003, L-004, L-005) have Amount=TBD |
| Total lines | 13 |

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
| Items priced | 10 |
| Items TBD | 3 |
| Pricing coverage | 76.9% |

### TBD Items (top missing-source offenders)

| LineID | ItemID | Description | Reason |
|---|---|---|---|
| L-003 | ITEM-003 | WCB coverage — Alberta statutory | WCB premiums are payroll-based; no payroll data in price sources |
| L-004 | ITEM-004 | E&O — $5M | E&O premium not in Fees_Permits_Insurance.csv; Proponent-specific |
| L-005 | ITEM-005 | Employer's Liability — $5M | Not in Fees_Permits_Insurance.csv; often bundled with WCB or CGL |

---

## Provenance Completeness

| Metric | Value |
|---|---|
| Lines with SourceRef | 10 of 13 (76.9%) |
| Lines with "location TBD" | 3 of 13 (23.1%) |

All 10 priced lines have traceable SourceRef pointing to specific rows in Professional_Staff_Rates.csv, Level_of_Effort.csv, or Fees_Permits_Insurance.csv.

---

## Basis-Consistency Checks

| Check | Result |
|---|---|
| BASIS_OF_ESTIMATE | PARAMETRIC |
| Method values in Detail.csv | All PARAMETRIC |
| ALLOW_MIXED_METHODS | TRUE (allowed but not needed; all lines are PARAMETRIC) |
| FALLBACK_POLICY | ALLOW_PARAMETRIC — applied; 3 lines remain TBD because even parametric data is unavailable |
| Basis consistency | PASS — no method mix violations |

---

## Scope Coverage

| Metric | Value |
|---|---|
| Deliverables in scope | 1 (DEL-021-03) |
| Deliverables estimated | 1 |
| SOW items mapped | SOW-0102 (insurance coverage per §4.2), SOW-0103 (name County as additional insured) |
| SOW items covered by line items | Both — SOW-0102 maps to ITEM-001 through ITEM-005; SOW-0103 covered within policy conditions (no separate cost line) |

---

## Warnings Summary

| # | Severity | Description |
|---|---|---|
| W-001 | MATERIAL | 3 of 5 insurance premium lines (WCB, E&O, Employer's Liability) are TBD — total estimate is incomplete |
| W-002 | MODERATE | Builders risk ($14,000) may not be required per RFP §4.2; depends on CCDC 14-2013 review |
| W-003 | MODERATE | Insurance premiums are contract-value-dependent; FP-03 and FP-04 ranges are wide |
| W-004 | LOW | E&O tail coverage cost not included; may be needed for 2-year guarantee period |
| W-005 | LOW | Subcontractor insurance costs excluded; assumes individual subcontractor responsibility |

---

## What to Fix for a Cleaner Rerun

1. **Add WCB premium data** — Provide total project payroll estimate and Proponent's WCB rate classification to price ITEM-003.
2. **Add E&O premium data** — Obtain broker quote or historical premium data for design-build E&O coverage at $5M limit to price ITEM-004.
3. **Add Employer's Liability premium data** — Obtain standalone or bundled premium amount to price ITEM-005.
4. **Confirm builders risk requirement** — Review CCDC 14-2013 insurance provisions (GC 11.1) to confirm whether builders risk is required or optional.
5. **Resolve contract value dependency** — Once project contract value is estimated, narrow the premium ranges for builders risk and CGL.
