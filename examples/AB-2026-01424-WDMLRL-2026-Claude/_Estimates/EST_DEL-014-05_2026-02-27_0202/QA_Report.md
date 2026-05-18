# QA_Report — EST_DEL-014-05_2026-02-27_0202

## RUN_STATUS: WARNINGS

---

## Schema Validity

### Items.csv

| Check | Result |
|---|---|
| Parseable CSV | PASS |
| Required columns present (ItemID, DeliverableID, Description, Qty, Unit, PricingMode, SourceDoc, SourceSection, Notes) | PASS |
| All PricingMode values valid (UNIT_RATE or LUMP_SUM) | PASS |
| Every row has SourceDoc | PASS |
| Every row has SourceSection | PASS |
| Row count | 16 |

### Detail.csv

| Check | Result |
|---|---|
| Parseable CSV | PASS |
| Required columns present (LineID, ItemID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes) | PASS |
| All Method values valid (PARAMETRIC) | PASS |
| Allowance/parametric convention (Qty=1, Unit=LS, UnitRate=Amount for LS items) | PASS (L-03, L-04 are LS with Qty=1) |
| Row count | 16 |
| All ItemIDs in Detail.csv match Items.csv | PASS |

---

## Quantity Takeoff Coverage

| Metric | Value |
|---|---|
| Deliverables in scope | 1 (DEL-014-05) |
| Documents read | 5 of 5 (_CONTEXT.md, Datasheet.md, Specification.md, Guidance.md, Procedure.md) |
| Missing documents | 0 |
| Items extracted | 16 |
| Items with TBD quantities | 0 (all quantities resolved or estimated parametrically) |

---

## Pricing Coverage

| Metric | Value |
|---|---|
| Total line items | 16 |
| Items priced (Amount != TBD) | 16 (100%) |
| Items with TBD Amount | 0 |
| Items priced via direct PRICE_SOURCES evidence | 11 (L-06 through L-16: labour rates from Construction_Labour_Rates.csv and staff rates from Professional_Staff_Rates.csv with hours from Level_of_Effort.csv) |
| Items priced via PARAMETRIC fallback (no direct source) | 5 (L-01 through L-05: material items with no pricing in PRICE_SOURCES) |
| Pricing coverage (rate-supported) | 68.75% (11/16 lines have rate table + LOE evidence) |
| Pricing coverage (amount-supported) | 100% (all lines have a computed amount) |

---

## Provenance Completeness

| Metric | Value |
|---|---|
| Total lines in Detail.csv | 16 |
| Lines with non-TBD SourceRef | 16 (100%) |
| Lines with explicit file reference in SourceRef | 11 (Construction_Labour_Rates.csv, Professional_Staff_Rates.csv, Level_of_Effort.csv) |
| Lines with parametric narrative SourceRef | 5 (PARAMETRIC estimate descriptions for material items) |
| Provenance completeness | 100% |

### Top Missing-Source Offenders

None — all lines have SourceRef populated. However, 5 material lines (L-01 through L-05) rely on parametric estimation narratives rather than file-based pricing evidence. These are the priority items for quote replacement.

| LineID | Description | Amount (CAD) | Issue |
|---|---|---|---|
| L-01 | Emergency shower unit | $2,800.00 | No vendor quote; PARAMETRIC estimate |
| L-02 | Thermostatic mixing valve | $650.00 | No vendor quote; PARAMETRIC estimate; CF-001 unresolved |
| L-03 | Supply branch piping | $750.00 | No quote; piping specs TBD |
| L-04 | Pipe supports | $200.00 | No quote; bundled with piping |
| L-05 | Signage | $150.00 | No quote; type TBD |

---

## Basis-Consistency Checks

| Check | Result |
|---|---|
| BASIS_OF_ESTIMATE | PARAMETRIC |
| ALLOW_MIXED_METHODS | TRUE |
| Methods used | PARAMETRIC only (16/16 lines) |
| Non-basis methods used | None |
| Basis consistency | PASS |

---

## Scope Coverage

| Metric | Value |
|---|---|
| Deliverables requested | 1 (DEL-014-05) |
| Deliverables estimated | 1 (DEL-014-05) |
| Deliverables excluded | 0 |
| SOW items covered | SOW-0048 (Install emergency shower) |

---

## Write Quarantine Check

| Check | Result |
|---|---|
| All outputs written under _Estimates/ | PASS |
| No deliverable files modified | PASS |
| No lifecycle files modified | PASS |
| No decomposition files modified | PASS |

---

## What to Fix for a Cleaner Rerun

1. **Obtain vendor quotes** for the emergency shower unit (ITEM-01) and thermostatic mixing valve (ITEM-02) to replace PARAMETRIC LOW-confidence material costs with QUOTE-based HIGH-confidence values.
2. **Resolve CF-001** (tepid water / TMV requirement) to confirm or remove ITEM-02 from the estimate.
3. **Resolve CF-002** (combination vs. shower-only) to confirm unit type and refine ITEM-01 pricing.
4. **Obtain IFC plumbing design** to confirm pipe material, size, and routing for ITEM-03 (supply branch piping).
5. **Confirm permit fee allocation** for ITEM-08 across PKG-014 deliverables.
6. **Review overhead proportion** (42.8%) — typical for a small single-fixture installation but may warrant LOE matrix review if the ratio appears disproportionate at package rollup level.
