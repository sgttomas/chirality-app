# Estimate Summary -- DEL-001-01 Preliminary Architectural Design

**RunID:** EST_DEL-001-01_2026-03-26_1759
**Date:** 2026-03-26
**Basis of Estimate:** RATE_TABLE
**Currency:** CAD
**RUN_STATUS:** OK

---

## Basis of Estimate Used

| Field | Value |
|-------|-------|
| **Primary Method** | RATE_TABLE |
| **Fallback Policy** | ALLOW_ALLOWANCE |
| **Mixed Methods** | TRUE (allowed) |
| **Methods Actually Used** | RATE_TABLE (100% of lines) |

The estimate for DEL-001-01 (Preliminary Architectural Design) is derived using professional staff hourly rates from `Professional_Staff_Rates.csv` (the rate table) applied to hours-by-role from `Level_of_Effort.csv`, with manual adjustments for the precast concrete interior wall scope change (Add. 4, Q5). Both sources carry MEDIUM confidence. All 5 line items are priced with full provenance.

---

## Totals by Package

| WBS_PackageID | Currency | Amount_Total | Line Count |
|---|---|---|---|
| PKG-001 | CAD | $11,370 | 5 |

## Totals by Deliverable

| WBS_DeliverableID | Name | Currency | Amount_Total | Line Count |
|---|---|---|---|---|
| DEL-001-01 | Preliminary Architectural Design | CAD | $11,370 | 5 |

## Totals by CBS (Cost Breakdown Structure)

| CBS | Description | Currency | Amount_Total | Line Count |
|---|---|---|---|---|
| CBS-02 | Project Management | CAD | $1,530 | 2 |
| CBS-01 | Design & Engineering | CAD | $9,840 | 3 |
| **Total** | | **CAD** | **$11,370** | **5** |

---

## Hours Breakdown

| Role | Hours | Rate (CAD/hr) | Amount (CAD) | Notes |
|---|---|---|---|---|
| Project Manager (R-01) | 6 | 165 | 990 | Unchanged from prior |
| Cost Estimator (R-08) | 4 | 135 | 540 | Unchanged from prior |
| Senior Architect (R-11) | 31 | 180 | 5,580 | +4 hrs vs prior (precast interior wall coordination) |
| Architect (R-12) | 21 | 135 | 2,835 | Unchanged from prior |
| BIM Technician (R-13) | 15 | 95 | 1,425 | +3 hrs vs prior (precast wall modelling) |
| **Total** | **77** | | **$11,370** | +7 hrs / +$1,005 vs prior |

---

## Change vs Prior Estimate

| Metric | Prior (2026-02-27) | Current (2026-03-26) | Delta |
|---|---|---|---|
| Total Amount | $10,365 | $11,370 | +$1,005 (+9.7%) |
| Total Hours | 70 | 77 | +7 hrs |
| Line Count | 5 | 5 | 0 |
| Method | PARAMETRIC | RATE_TABLE | Changed per brief |

The increase is driven by the precast concrete interior wall scope change (Add. 4, Q5), which adds coordination effort at the preliminary design stage. See Decision_Log.md DEC-001.

---

## Parametric Cross-Check

Using Professional_Design_Fees.csv (DF-01: Architectural design fee at recommended 4.5% of construction value) and Parametric_Building_Rates.csv (PB-01: $285/sf recommended rate for industrial maintenance shop):

- Estimated construction value: 13,000 sf x $285/sf = $3,705,000 CAD
- Architectural design fee at 4.5%: $3,705,000 x 0.045 = $166,725 CAD (full architectural package, all DEL-001-xx deliverables)
- DEL-001-01 is only the preliminary design presentation (1 of 11 architectural deliverables); this LOE-based estimate of $11,370 represents approximately 6.8% of the total estimated architectural fee, which is reasonable for a preliminary design stage gate deliverable with increased precast coordination.

---

## Warnings and Coverage Gaps

- **None critical.** All 5 items are priced with full provenance. No TBD amounts.
- Staff rates carry MEDIUM confidence (rate table basis, not firm quotes).
- LOE base hours carry MEDIUM confidence (parametric model, not activity-level build-up).
- The +7 hour adjustment for precast interior walls is a professional judgment estimate. If precast coordination proves more complex (e.g., multiple panel types, complex opening schedules), additional hours may be warranted.
