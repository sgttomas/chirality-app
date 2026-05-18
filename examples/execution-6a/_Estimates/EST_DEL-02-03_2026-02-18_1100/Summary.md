# Estimate Summary: DEL-02-03 Public Works Shop Bays, Workshop & Support Spaces

## Run Identity

| Field | Value |
|---|---|
| Snapshot | EST_DEL-02-03_2026-02-18_1100 |
| Date | 2026-02-18 |
| Scope | DEL-02-03 (PKG-002) |
| Basis of Estimate | RATE_TABLE |
| Currency | CAD |
| Rounding | DOLLAR |

## BasisOfEstimate_Used

Primary method: **RATE_TABLE** -- unit rates derived from project price source files (Interior_Architectural_Rates.csv, Equipment_Pricing.csv, and others).

Secondary method: **ALLOWANCE** -- used for 5 line items where no specific rate table entry exists (compressed air piping, warehouse racking, PPE room fit-up, workshop equipment, shower rough-in). Approved via FALLBACK_POLICY=ALLOW_ALLOWANCE and ALLOW_MIXED_METHODS=TRUE.

## Estimate Total

| | Amount (CAD) |
|---|---|
| **DEL-02-03 Total** | **$212,396** |

## Totals by CBS

| CBS | Description | Amount (CAD) | Lines | % of Total |
|---|---|---|---|---|
| 21.03.01 | PW Shop Bay Sealed Concrete / Floor Finish | $31,850 | 3 | 15.0% |
| 21.03.02 | PW Shop Bay Functional Fit-up | $40,188 | 4 | 18.9% |
| 21.03.03 | PW Workshop and Storage Areas | $34,000 | 2 | 16.0% |
| 21.03.04 | PW PPE / Locker Room Fit-up | $95,060 | 12 | 44.8% |
| 21.03.05 | PW Shop Office and Washroom Fit-up | $11,298 | 11 | 5.3% |
| **TOTAL** | | **$212,396** | **32** | **100.0%** |

## Totals by Method

| Method | Amount (CAD) | Lines | % of Total |
|---|---|---|---|
| RATE_TABLE | $151,896 | 27 | 71.5% |
| ALLOWANCE | $60,500 | 5 | 28.5% |
| **TOTAL** | **$212,396** | **32** | **100.0%** |

## Scope Coverage

- **In scope:** 1 deliverable (DEL-02-03)
- **Scope items covered:** SOW-0209, SOW-0210, SOW-0211, SOW-0212
- **Excluded (by cost ownership):** Overhead doors (DEL-02-04), HVAC/ventilation (DEL-02-05), electrical/lighting (DEL-02-06), general interior partitions for shared areas (DEL-02-01), bay sumps (DEL-02-05), water fill stations (DEL-02-05)

## Cost Driver Summary

The largest cost concentration is in **CBS 21.03.04 (PPE/Locker Room Fit-up)** at $95,060 (44.8% of total), driven primarily by:
- 40 PW lockers at $1,000 each = $40,000 (18.8% of total)
- Ceramic tile in wet areas, moisture-resistant partitions, and gypsum ceilings
- Shower rough-in and washroom accessories

The second largest concentration is **CBS 21.03.02 (Shop Bay Functional Fit-up)** at $40,188 (18.9%), driven by the compressed air piping allowance ($15,000) and exposed structure painting across four bays.

## Key Warnings and Blockers

1. **Mixed methods:** 5 of 32 lines (28.5% of total value) use ALLOWANCE method due to missing rate table entries. These items are flagged for future refinement with actual quotes or detailed estimates.
2. **Area assumptions:** All support space areas (locker room, PPE, office, washroom) are based on functional program hints and professional judgment, not confirmed floor plans. See Assumptions_Log.md.
3. **Scope boundary ambiguity:** Bay slab/structural slab may overlap with DEL-02-04. This estimate includes only the floor finish (densifier + sealer) per IA-08, not the structural slab itself. See Decision_Log.md DEC-RUN-001.
4. **No overhead doors included:** Per cost ownership rules, all 4 PW overhead doors ($20,000 each = $80,000) are allocated to DEL-02-04.
5. **No HVAC/ventilation included:** Per cost ownership rules, PW bay ventilation (MS-07, $11,000/bay) and bay sumps (EQ-10, $4,500/each) are allocated to DEL-02-05.
6. **No electrical/lighting included:** Per cost ownership rules, bay power (ES-02) and lighting (ES-04) are allocated to DEL-02-06.

## Blockers (from dependency evidence)

No critical blockers preventing estimate generation. The following execution dependencies are noted for awareness:
- DEL-02-01 must provide overall building layout before PW zone boundaries are final
- DEL-02-04 must provide structural bay dimensions and clear height confirmation
- Owner must confirm whether optional wash bay (SOW-0500) is selected (impacts bay count)
