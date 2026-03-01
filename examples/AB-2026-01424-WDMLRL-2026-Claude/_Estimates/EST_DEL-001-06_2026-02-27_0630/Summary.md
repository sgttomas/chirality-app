# Estimate Summary — DEL-001-06 Reflected Ceiling Plans

**RunID:** EST_DEL-001-06_2026-02-27_0630
**As Of:** 2026-02-27T06:30:00-07:00
**Currency:** CAD

---

## Basis of Estimate

| Field | Value |
|---|---|
| BASIS_OF_ESTIMATE | PARAMETRIC |
| Method | Staff hours (from Level_of_Effort.csv) x hourly rates (from Professional_Staff_Rates.csv) |
| FALLBACK_POLICY | ALLOW_PARAMETRIC |
| ALLOW_MIXED_METHODS | TRUE |
| Methods Used | PARAMETRIC only (no fallback required) |

---

## Totals by Deliverable

| WBS_DeliverableID | Name | Amount (CAD) | Line Count |
|---|---|---|---|
| DEL-001-06 | Reflected Ceiling Plans | $19,200.00 | 5 |

## Totals by CBS

| CBS | Amount (CAD) | Line Count |
|---|---|---|
| Design-Labour | $17,670.00 | 3 |
| Management-Labour | $1,530.00 | 2 |
| **TOTAL** | **$19,200.00** | **5** |

## Totals by Package

| WBS_PackageID | Amount (CAD) |
|---|---|
| PKG-001 (Architectural Design) | $19,200.00 |

## Labour Hours Breakdown

| Role | RoleID | Hours | Rate (CAD/hr) | Amount (CAD) |
|---|---|---|---|---|
| Senior Architect | R-11 | 54 | $180.00 | $9,720.00 |
| Architect | R-12 | 42 | $135.00 | $5,670.00 |
| BIM Technician | R-13 | 24 | $95.00 | $2,280.00 |
| Project Manager | R-01 | 6 | $165.00 | $990.00 |
| Cost Estimator | R-08 | 4 | $135.00 | $540.00 |
| **Total** | | **130** | | **$19,200.00** |

---

## Cross-Check: Design Fee Method

As a reasonableness cross-check using Professional_Design_Fees.csv:
- Parametric building rate (PB-01): $285/sf x 13,000 sf = $3,705,000 estimated construction value
- Architectural design fee (DF-01): 4.5% of $3,705,000 = $166,725 total architectural design fee
- PKG-001 has 11 deliverables; if equally weighted, per-deliverable share = ~$15,157
- DEL-001-06 estimate of $19,200 is within a reasonable range of the per-deliverable share (~127% of equal-weight share), which is plausible given that RCPs are a coordination-intensive drawing set requiring more effort than simpler deliverables like schedules
- This cross-check supports the parametric LOE-based estimate as reasonable

---

## Key Warnings and Coverage Gaps

1. **Items.csv scope items ITM-006 through ITM-023 are not independently priced.** These represent the scope of work (drawing sheets, element placement, coordination activities, QA, P.Eng. stamp) whose production effort is captured within the five labour line items. No separate material, equipment, or subcontractor costs are applicable for this design deliverable.
2. **TBD quantities in Items.csv:** Items ITM-016 (exhaust fans), ITM-018 (forced air makeup units), and ITM-019 (exhaust hose drop points) have TBD quantities. These do not affect the estimate total because they represent elements to be placed on the RCP drawings during the billed hours, not independently procured items.
3. **All rates and hours are MEDIUM confidence per price sources.** No HIGH-confidence pricing inputs were available.
