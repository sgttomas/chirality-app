# Summary — EST_DEL-014-05_2026-02-27_0202

## Basis of Estimate Used

| Field | Value |
|---|---|
| BASIS_OF_ESTIMATE | PARAMETRIC |
| CURRENCY | CAD |
| FALLBACK_POLICY | ALLOW_PARAMETRIC |
| ALLOW_MIXED_METHODS | TRUE |
| Method Mix | 100% PARAMETRIC (16/16 lines) |
| Basis Consistency | PASS — all lines use PARAMETRIC, consistent with BASIS_OF_ESTIMATE |

## Total by Deliverable

| WBS_DeliverableID | Name | Amount (CAD) | Lines | Notes |
|---|---|---|---|---|
| DEL-014-05 | Emergency Shower | $13,052.80 | 16 | Single deliverable in scope |

## Total by Package

| WBS_PackageID | Amount (CAD) | Lines |
|---|---|---|
| PKG-014 | $13,052.80 | 16 |

## Total by CBS

| CBS | Amount (CAD) | Lines | % of Total |
|---|---|---|---|
| Material | $4,550.00 | 5 | 34.9% |
| Labour | $2,412.80 | 4 | 18.5% |
| Permit | $500.00 | 1 | 3.8% |
| Overhead | $5,590.00 | 6 | 42.8% |
| **TOTAL** | **$13,052.80** | **16** | **100.0%** |

## Grand Total

**$13,052.80 CAD**

## Key Warnings and Coverage Gaps

1. **W-001 — No equipment pricing in PRICE_SOURCES.** The emergency shower unit ($2,800), TMV ($650), piping ($750), pipe supports ($200), and signage ($150) are priced via PARAMETRIC fallback. These 5 material lines ($4,550 total, 34.9% of estimate) carry LOW confidence. Recommend obtaining vendor quotes to replace these parametric values.

2. **W-002 — Supply branch piping quantity is TBD.** Pipe material, size, and length are not specified in the Datasheet (pending IFC design). A parametric lump-sum allowance of $750 is carried. Actual cost may vary significantly based on routing and material selection.

3. **W-003 — Multiple TBD attributes in Datasheet.** Flow rate, water supply pressure, pipe material, pipe size, finish/material, activation mechanism, signage type, and accessibility clearance are all TBD pending IFC design. These do not block cost estimation at parametric level but represent design uncertainty.

4. **W-004 — Thermostatic mixing valve is ASSUMPTION (CF-001 unresolved).** If the TMV is not required, material cost reduces by $650 and some installation labour would be saved. If required, no change.

5. **W-005 — Overhead is 42.8% of total cost.** This is characteristic of a small single-item installation deliverable where fixed professional oversight hours represent a significant share. The 38 staff hours from the LOE matrix represent coordination, safety management, and quality oversight for a relatively simple plumbing installation.

6. **W-006 — Combination vs. shower-only (CF-002 unresolved).** If a shower-only unit is confirmed sufficient, the equipment cost may be lower ($1,500-$2,500 range vs. $2,000-$4,000 for combination). Current estimate assumes combination unit.
