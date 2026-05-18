# QA Report — EST_DEL-002-09_2026-02-27_0630

## RUN_STATUS: OK

---

## S1 — Write Quarantine Respected

| Check | Result |
|---|---|
| All files written under `_Estimates/EST_DEL-002-09_2026-02-27_0630/` | PASS |
| No files outside `_Estimates/` modified | PASS |
| No deliverable content modified | PASS |
| No lifecycle files modified | PASS |
| No decomposition outputs modified | PASS |

**Verdict: PASS**

---

## S2 — Snapshot Created

| Check | Result |
|---|---|
| Snapshot folder `EST_DEL-002-09_2026-02-27_0630` exists | PASS |
| Naming convention matches `EST_{LABEL}_{YYYY-MM-DD}_{HHMM}` | PASS |
| UPDATE_LATEST_POINTER = FALSE; no pointer file modified | PASS |

**Verdict: PASS**

---

## S3 — BASIS_OF_ESTIMATE Validated

| Check | Result |
|---|---|
| BASIS_OF_ESTIMATE = PARAMETRIC | PASS |
| Value is in allowed enum (QUOTE, RATE_TABLE, HISTORICAL, PARAMETRIC, ALLOWANCE) | PASS |

**Verdict: PASS**

---

## S4 — Required Artifacts Exist

| Artifact | Required | Present |
|---|---|---|
| Run_Context.md | Yes | Yes |
| Items.csv | Yes | Yes |
| Summary.md | Yes | Yes |
| QA_Report.md | Yes | Yes |
| Source_Index.md | Yes | Yes |
| Decision_Log.md | Yes | Yes |
| Assumptions_Log.md | Yes | Yes |
| WBS_CBS_Matrix.csv | Yes | Yes |
| Detail.csv | Recommended | Yes |

**Verdict: PASS**

---

## S5 — CSV Schema Integrity

### Items.csv

| Check | Result |
|---|---|
| File is parseable CSV | PASS |
| Required columns present (ItemID, DeliverableID, Description, Qty, Unit, PricingMode, SourceDoc, SourceSection, Notes) | PASS |
| All rows have non-empty ItemID | PASS (16 items: ITM-001 through ITM-016) |
| All rows trace to SourceDoc (Datasheet/Specification/Guidance/Procedure) | PASS (all reference Procedure) |
| All rows have SourceSection | PASS |
| PricingMode values valid (UNIT_RATE or LUMP_SUM) | PASS (4 UNIT_RATE, 12 LUMP_SUM) |
| Lump-sum convention (Qty=1, Unit=LS) | PASS |

### Detail.csv

| Check | Result |
|---|---|
| File is parseable CSV | PASS |
| Required columns present (LineID, ItemID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes) | PASS |
| All rows have valid Method enum (QUOTE/RATE_TABLE/HISTORICAL/ALLOWANCE/PARAMETRIC) | PASS (all PARAMETRIC) |
| All amounts are numeric | PASS |
| Currency consistent (CAD) | PASS |
| Allowance/parametric convention check | N/A (all items are UNIT_RATE with explicit Qty and UnitRate; no allowance/parametric LS convention needed) |

**Verdict: PASS**

---

## S6 — Provenance Discipline

| Metric | Value |
|---|---|
| Total priced rows in Detail.csv | 4 |
| Rows with non-TBD SourceRef | 4 |
| Provenance completeness | **100%** |
| Rows with `location TBD` SourceRef | 0 |

### Top Missing-Source Offenders

None. All 4 priced line items have complete source references pointing to Level_of_Effort.csv and Professional_Staff_Rates.csv.

**Verdict: PASS**

---

## S7 — Status Reporting

**RUN_STATUS: OK**

Rationale:
- All totals are meaningful ($19,230.00 CAD).
- No critical input gaps for the pricing basis (PARAMETRIC hours and rates are fully sourced).
- No TBD amounts.
- Confidence is MEDIUM across all items (parametric basis, not firm quotes).
- Engineering TBDs in the deliverable documents (stair material, live load, seismic, fire rating, etc.) do not affect the design effort estimate; they affect downstream construction scope.

---

## S8 — Operator Acceptance Checklist

| Criterion | Status | Notes |
|---|---|---|
| RUN_STATUS is OK or WARNINGS with bounded gaps | OK | No unresolved gaps |
| Items.csv reviewed for completeness | PASS | 16 items extracted covering all procedure steps and 4 priced roles |
| Basis-consistency checks pass | PASS | All methods = PARAMETRIC; consistent with BASIS_OF_ESTIMATE |
| Provenance completeness reported | PASS | 100% (4/4 lines) |
| Scope coverage explicit | PASS | 1 deliverable (DEL-002-09) fully covered; 4 of 4 documents read |
| No writes outside _Estimates/ | PASS | Verified |

**Verdict: PASS — snapshot is publishable.**

---

## Quantity Takeoff Coverage

| Deliverable | Documents Available | Documents Read | Items Extracted | Warnings |
|---|---|---|---|---|
| DEL-002-09 | 5 (Context, Datasheet, Specification, Guidance, Procedure) | 5 | 16 (4 priced labour lines + 12 activity decomposition lines) | None |

---

## Pricing Coverage

| Metric | Value |
|---|---|
| Total items in Items.csv | 16 |
| Items with direct pricing in Detail.csv | 4 (labour lines ITM-001 through ITM-004) |
| Items that are activity sub-components (no separate pricing) | 12 (ITM-005 through ITM-016; costs captured within labour lines) |
| Items with TBD amount | 0 |
| Pricing coverage (priced lines / total priced lines) | **100%** |

---

## Basis-Consistency Check

| Check | Result |
|---|---|
| BASIS_OF_ESTIMATE = PARAMETRIC | Confirmed |
| All Detail.csv Method values | PARAMETRIC (4/4) |
| Mixed methods used | No |
| FALLBACK_POLICY invoked | No (all items directly supported by parametric sources) |

**Verdict: PASS — fully consistent.**

---

## What to Fix for a Cleaner Rerun

1. **No critical fixes required.** This run produced complete, consistent artifacts.
2. **Optional improvements:**
   - Obtain firm quotes for structural engineering services to upgrade from PARAMETRIC to QUOTE method with HIGH confidence.
   - Resolve engineering TBDs in deliverable documents (stair material, live load, code edition) to enable a construction cost estimate for this scope element.
   - Add overhead/markup rates to PRICE_SOURCES if fully-loaded cost estimates are desired (current estimate is direct labour only).
   - Consider adding disbursements (printing, travel, software licenses) if applicable.
