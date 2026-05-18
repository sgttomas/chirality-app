# Estimate Summary -- DEL-01-04 Permitting, Inspections & AHJ Coordination

**RunID:** EST_DEL-01-04_2026-02-18_1400
**Date:** 2026-02-18
**Currency:** CAD
**Rounding:** DOLLAR

---

## Basis of Estimate Used

| Parameter | Value |
|---|---|
| PRIMARY method | RATE_TABLE (coordinator labour hours) |
| SECONDARY method | ALLOWANCE (permit/inspection fees) |
| ALLOW_MIXED_METHODS | TRUE |
| FALLBACK_POLICY | ALLOW_ALLOWANCE |
| Justification | Brief explicitly authorizes mixed methods: coordinator hours at RATE_TABLE; permit/inspection fees at ALLOWANCE where fee schedules are uncertain. |

---

## Totals by CBS

| CBS | Description | Amount (CAD) | Line Count | Method |
|---|---|---|---|---|
| 01-MGMT | Management and coordination labour | $7,960 | 2 | RATE_TABLE |
| 01-FEES | Regulatory permit and inspection fees | $71,950 | 5 | ALLOWANCE |
| **TOTAL** | | **$79,910** | **7** | |

## Totals by Package / Deliverable

| PackageID | DeliverableID | Name | Amount (CAD) |
|---|---|---|---|
| PKG-001 | DEL-01-04 | Permitting, Inspections & AHJ Coordination | **$79,910** |

## Labour Detail

| Role | Hours | Rate (CAD/hr) | Amount (CAD) |
|---|---|---|---|
| R-02 Project Manager | 40 | $175 | $7,000 |
| R-24 Administrative / Document Control | 12 | $80 | $960 |
| **Total Labour** | **52** | | **$7,960** |

## Permit Fee Detail

| Permit | Fee (CAD) | Confidence | Source |
|---|---|---|---|
| Building permit (FP-06) | $65,250 | LOW | 0.75% of $8,700,000 (PP-24); Penhold fee schedule TBD |
| Development permit (FP-07) | $1,200 | LOW | Recommended rate; Penhold fee schedule TBD |
| Electrical permit (FP-08) | $2,500 | MED | Recommended rate; Alberta Safety Codes |
| Plumbing permit (FP-09) | $2,000 | MED | Recommended rate; Alberta Safety Codes |
| Gas permit (FP-10) | $1,000 | MED | Recommended rate; Alberta Safety Codes |
| **Total Fees** | **$71,950** | | |

---

## Key Warnings

1. **Building permit fee dominates the estimate** ($65,250 of $79,910 = 81.7%). This fee is calculated as 0.75% of the estimated total construction value (PP-24 = $8,700,000), which itself is marked PARAMETRIC / LOW confidence. The actual Penhold fee schedule has not been confirmed. Sensitivity: if the fee rate is 0.50% instead of 0.75%, the building permit drops to $43,500 (delta = -$21,750); if 1.00%, it rises to $87,000 (delta = +$21,750).
2. **All permit fee line items use ALLOWANCE method** -- these are not firm prices. They reflect recommended rates from Fees_Permits_Insurance.csv where actual fee schedules are TBD.
3. **No environmental/AEP fees included.** Fees_Permits_Insurance.csv contains FP-16 (AEPA Water Act fee) and FP-17 (environmental consultant fees), but these relate to DEL-03-05 environmental compliance, not DEL-01-04. If AEP approval is triggered for this project, those costs would be carried in the appropriate deliverable estimate. This is logged in Decision_Log.md (DEC-EST-03).

## Blockers

No critical blockers prevent this estimate from being produced. The deliverable is Tier 0 (no upstream cost dependencies). Dependency evidence from Dependencies.csv identifies interface relationships (DEL-01-01, DEL-01-02, DEL-01-03, DEL-03-04, DEL-03-05, DEL-01-07) but none of these block pricing at this stage.
