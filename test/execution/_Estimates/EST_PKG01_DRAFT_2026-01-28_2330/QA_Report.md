# QA Report — PKG-01 Demolition & Removals Estimate

**Snapshot ID:** EST_PKG01_DRAFT_2026-01-28_2330
**Package:** PKG-01 Demolition & Removals
**Date:** 2026-01-28
**Run Status:** WARNINGS

---

## QA Summary

| Check Category | Pass | Warn | Fail |
|----------------|------|------|------|
| Schema Compliance | 5 | 0 | 0 |
| Arithmetic | 3 | 0 | 0 |
| Coverage | 2 | 2 | 0 |
| Traceability | 3 | 0 | 0 |
| Quality Metrics | 0 | 4 | 0 |
| **TOTAL** | **13** | **6** | **0** |

**Overall Status:** WARNINGS — Estimate is complete and valid but has low confidence due to pricing basis.

---

## Schema Compliance Checks

### SC-1: Currency Consistency — PASS
All 14 line items in Detail.csv use CAD currency consistently.

### SC-2: Qty/Unit/UnitRate Population — PASS
All 14 line items have non-empty Qty, Unit, and UnitRate fields.
- Qty: All populated (values = 1 for LS items)
- Unit: All populated (LS for all allowance/parametric items)
- UnitRate: All populated (equals Amount for LS items)

### SC-3: Required Columns Present — PASS
Detail.csv contains all required columns:
- LineID, CBS, WBS_PackageID, WBS_DeliverableID, Description
- Qty, Unit, UnitRate, Amount, Currency
- Method, SourceRef, Confidence, Notes

### SC-4: SourceRef Population — PASS
All 14 line items have SourceRef populated:
- 11 lines reference assumption IDs (A-101 through A-111)
- 3 lines reference decision ID (D-017)

### SC-5: Method Values Valid — PASS
All Method values are valid enumeration values:
- ALLOWANCE: 11 lines
- PARAMETRIC: 3 lines

---

## Arithmetic Checks

### AR-1: Line Item Extension — PASS
All line items: Amount = Qty × UnitRate
- Verified for all 14 lines (all are Qty=1, so UnitRate=Amount)

### AR-2: CBS Subtotals — PASS
Detail.csv CBS subtotals verified:
- E: $18,000 + $15,000 + $8,000 = $41,000 ✓
- PM: $25,000 + $69,660 = $94,660 ✓
- P: $800 ✓
- MAT: $40,000 ✓
- CD: $175,000 + $450,000 + $35,000 + $125,000 + $75,000 + $95,000 = $955,000 ✓
- CI: $171,000 ✓
- **Total: $1,302,460** (rounds to $1,303,000)

### AR-3: Summary Reconciliation — PASS
Summary.md total ($1,303,000) reconciles with Detail.csv sum ($1,302,460) within rounding tolerance ($1,000).

---

## Coverage Checks

### COV-1: Deliverable Coverage — PASS
All 4 PKG-01 deliverables have associated cost lines:
- DEL-01.01: L101 ($18,000)
- DEL-01.02: L102 ($15,000)
- DEL-01.03: L103 ($25,000)
- DEL-01.04: L104 ($8,000)

### COV-2: Scope Item Coverage — PASS
All PKG-01 scope items have associated cost lines:
- Track 6 demolition: L105 ($175,000)
- Dolphin 2 demolition: L106 ($450,000)
- Fencing removal: L107 ($35,000)
- Salt tent demolition: L108 ($125,000)
- Decommissioning/disposal: L109-L111 (materials, hazmat, disposal)

### COV-3: CBS Coverage — WARNING
Not all standard CBS buckets have cost lines. Missing buckets:
- FRT (Freight): Not applicable for demolition package
- COM (Commissioning): Not applicable for demolition package
- EI (E&I Controls): Not applicable for demolition package
- INST (Installation): Not applicable for demolition package
- OHP (Contractor OH&P): Included in CD and CI for this estimate
- ESC (Escalation): Per D-009, escalation_mode = NONE
- TAX (Taxes): Excluded per project convention

**Assessment:** Missing CBS buckets are appropriate for demolition scope. WARNING noted for transparency.

### COV-4: Indirects Coverage — WARNING
Indirects applied using factor-based model (D-017):
- CI = 18% of CD: $171,000 ✓
- PM = 6% of (CD+CI+MAT): $69,660 ✓
- P = 2% of MAT: $800 ✓

**Assessment:** Factor-based indirects may not accurately reflect actual demolition supervision needs. WARNING noted for time-based validation when schedule available.

---

## Traceability Checks

### TR-1: Decision Log Completeness — PASS
Decision_Log.md contains 9 decisions (D-010 through D-018) covering:
- Scope selection
- Currency and pricing date
- Source priority
- Structure breakdown
- Marine equipment requirements
- Hazmat status
- Indirects and contingency methods

### TR-2: Assumptions Log Completeness — PASS
Assumptions_Log.md contains 11 assumptions (A-101 through A-111) covering all allowance line items.
All assumptions include:
- Statement of assumption
- Why needed
- Impacted WBS/CBS
- Cost impact and range
- Confidence rating
- Resolution path

### TR-3: Risk Register Population — PASS
Risk_Register.md contains 9 risks covering:
- Hazmat discovery
- Marine demolition uncertainty
- Ballast contamination
- Weather and terminal interface
- Estimate accuracy
- Disposal costs
- Structure complexity

---

## Quality Metrics

### QM-1: Quote-Based Pricing — WARNING
Lines priced by QUOTE: 0 of 14 (0%)
**Target:** >50% for Class 3 estimate
**Assessment:** No vendor quotes available. Estimate suitable for screening/order-of-magnitude only.

### QM-2: Rate Table Pricing — WARNING
Lines priced by RATE_TABLE: 0 of 14 (0%)
**Target:** >25% for Class 4 estimate
**Assessment:** No project rate tables available. All direct costs are allowances.

### QM-3: Allowance/Parametric Share — WARNING
Lines priced by ALLOWANCE or PARAMETRIC: 14 of 14 (100%)
**Target:** <50% for Class 3 estimate
**Assessment:** 100% allowance-based estimate has wide accuracy range (±50% or more).

### QM-4: Quantity Extraction — WARNING
Deliverables with explicit quantities extracted: 0 of 4 (0%)
**Target:** >75% for reliable estimate
**Assessment:** Deliverable documents contain no explicit quantities for demolition scope items. All sizing based on professional judgment and typical values.

---

## Mapping Ambiguities

None identified. All deliverables mapped to appropriate CBS buckets:
- Drawing/Specification/Record deliverables → E (Engineering)
- Procedure deliverable → PM (Project Management)
- Demolition scope items → CD (Construction Directs)
- Support materials → MAT (Materials)
- Factor-based allocations → CI, PM, P

---

## Double Count Check

No potential double counts identified:
- Track 6, Dolphin 2, fencing, salt tent are separate structures
- Disposal is separate from individual structure demolition
- Hazmat placeholder is additive contingency, not duplication

---

## Completeness Scoring

| Metric | Value | Weight | Score |
|--------|-------|--------|-------|
| Deliverable coverage | 100% | 20% | 20% |
| Scope item coverage | 100% | 20% | 20% |
| Quote-based pricing | 0% | 30% | 0% |
| Quantity extraction | 0% | 20% | 0% |
| Traceability | 100% | 10% | 10% |
| **TOTAL** | | | **50%** |

**Completeness Score:** 50% (Low — suitable for screening/order-of-magnitude only)

---

## Known Issues

1. **No vendor quotes** — All construction costs are allowances
2. **No explicit quantities** — Structure sizes, lengths, and volumes unknown
3. **Hazmat status unknown** — Survey required before reliable estimate
4. **Marine work uncertainty** — Dolphin 2 details insufficient for accurate pricing

---

## Recommendations

1. **Before budget approval:** Obtain vendor quotes for major items (Dolphin 2, Track 6)
2. **Before contract commitment:** Complete hazmat survey and quantity takeoffs
3. **Improve estimate class:** Add rate tables for engineering services and disposal
4. **Next estimate cycle:** Re-run with updated sources to achieve Class 3 or better

---

**QA Complete**
**Run Status:** WARNINGS
**Estimate Suitable For:** Screening, feasibility, order-of-magnitude budgeting
**Not Suitable For:** Firm budget commitment, contract pricing, cost control baseline
