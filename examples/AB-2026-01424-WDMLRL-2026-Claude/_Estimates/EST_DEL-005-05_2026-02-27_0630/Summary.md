# Estimate Summary — EST_DEL-005-05_2026-02-27_0630

## Basis of Estimate

| Field | Value |
|---|---|
| **BASIS_OF_ESTIMATE** | PARAMETRIC |
| **Method Used** | Staff hours (from Level_of_Effort.csv) multiplied by hourly rates (from Professional_Staff_Rates.csv) |
| **Currency** | CAD |
| **Fallback Policy** | ALLOW_PARAMETRIC |
| **Mixed Methods** | TRUE (allowed); all lines are PARAMETRIC — no mixing required |
| **Rounding** | NONE |

## Scope

| Field | Value |
|---|---|
| **Deliverable** | DEL-005-05: Civil Sections & Details |
| **Package** | PKG-005 — Civil Design |
| **Discipline** | Civil Engineering |
| **Delivery Type** | Drawing Set |
| **SOW Coverage** | SOW-0015 |
| **Objectives** | OBJ-001, OBJ-003 |

## Total by Deliverable

| WBS_DeliverableID | Description | Amount (CAD) |
|---|---|---|
| DEL-005-05 | Civil Sections & Details | **18,390.00** |

## Total by CBS

| CBS | Amount (CAD) | Line Count |
|---|---|---|
| Professional Services — Management | 1,530.00 | 2 |
| Professional Services — Design | 16,860.00 | 2 |
| **TOTAL** | **18,390.00** | **4** |

## Total by Role

| RoleID | Role | Hours | Rate (CAD/hr) | Amount (CAD) |
|---|---|---|---|---|
| R-01 | Project Manager | 6 | 165.00 | 990.00 |
| R-08 | Cost Estimator | 4 | 135.00 | 540.00 |
| R-13 | BIM Technician | 36 | 95.00 | 3,420.00 |
| R-17 | Civil Engineer | 84 | 160.00 | 13,440.00 |
| | **TOTAL** | **130** | | **18,390.00** |

## Key Observations

1. **This is a professional design services estimate only.** The scope of DEL-005-05 is the production of civil section and detail drawings. It does not include construction costs for civil works (gravel, drainage structures, mud sump, etc.), which would be priced under PKG-018 (Sitework & Civil Construction).

2. **Civil engineer hours dominate.** R-17 Civil Engineer accounts for 84 of 130 total hours (64.6%) and $13,440 of $18,390 total cost (73.1%). This is expected for a drawing set deliverable that involves engineering design, coordination, review, and IFC stamping.

3. **All quantities sourced from Level_of_Effort.csv.** The parametric LOE model provides hour estimates by role for each deliverable. All 4 line items are fully priced with PARAMETRIC method.

4. **No TBD amounts.** All 4 priced line items have defined quantities, rates, and computed amounts. Provenance completeness is 100%.

## Coverage Gaps and Warnings

| Warning | Description |
|---|---|
| Design services only | Estimate covers professional staff hours for drawing production. Does not include printing/reproduction, travel/site visits, subconsultant costs, software licensing, or disbursements. |
| Geotechnical dependency | DEL-005-05 has a critical upstream dependency on the PKG-008 geotechnical report. If the geotech report requires design revisions after initial drafting, additional hours may be needed beyond the LOE estimate. |
| Interdisciplinary coordination | Coordination with PKG-002, PKG-004, PKG-006, and PKG-018 is included in the LOE but the effort could vary depending on coordination complexity. |
| Retaining wall scope TBD | If the grading design (DEL-005-02) requires retaining walls, additional design and drafting hours may be needed beyond the current LOE. |
| No escalation applied | Rates are base-year 2026 rates with no escalation factor. |
| Fee cross-check | Professional_Design_Fees.csv suggests civil/site design fee of ~1.0% of construction value. Without a known construction value, this cross-check cannot be performed for this run. |
