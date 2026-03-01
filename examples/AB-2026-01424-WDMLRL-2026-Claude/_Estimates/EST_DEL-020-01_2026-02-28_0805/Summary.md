# Estimate Summary — EST_DEL-020-01_2026-02-28_0805

## Basis of Estimate

| Field | Value |
|---|---|
| BASIS_OF_ESTIMATE | PARAMETRIC |
| CURRENCY | CAD |
| FALLBACK_POLICY | ALLOW_PARAMETRIC |
| ALLOW_MIXED_METHODS | TRUE |
| Pricing Model | Professional staff hourly rates x estimated level of effort (hours) + third-party inspection fees |
| Rate Source | Professional_Staff_Rates.csv (25 roles, MEDIUM confidence) |
| Hours Source | Level_of_Effort.csv (8 role-rows for DEL-020-01) |
| Fee Source | Fees_Permits_Insurance.csv (FP-09, FP-10; LOW confidence) |

## Totals by Deliverable

| WBS_DeliverableID | Deliverable Name | Amount (CAD) | Line Count | Notes |
|---|---|---|---|---|
| DEL-020-01 | Building Systems Commissioning | 20,790 | 18 | 0 TBDs remaining |

## Totals by CBS Category

| CBS | Amount (CAD) | Line Count | Description |
|---|---|---|---|
| Management | 2,340 | 3 | PM ($990) + Cost Estimator ($540) + QA/QC Lead ($810) |
| Construction | 3,250 | 3 | Construction PM ($1,240) + Site Superintendent ($1,450) + HSE Manager ($560) |
| Admin | 900 | 2 | Document Controller ($900) + documentation compilation ($0 -- labour included) |
| Specialty | 14,300 | 10 | Commissioning Agent ($4,800) + activity line items ($0 labour-only) + crane load testing ($6,000) + Safety Code inspection ($3,500) |
| **TOTAL** | **20,790** | **18** | |

## Total Labour Hours

| Role | RoleID | Hours | Rate (CAD/hr) | Amount (CAD) |
|---|---|---|---|---|
| Project Manager | R-01 | 6 | 165 | 990 |
| Construction Project Manager | R-02 | 8 | 155 | 1,240 |
| Site Superintendent | R-03 | 10 | 145 | 1,450 |
| HSE Manager | R-05 | 4 | 140 | 560 |
| QA/QC Lead | R-06 | 6 | 135 | 810 |
| Cost Estimator | R-08 | 4 | 135 | 540 |
| Document Controller | R-09 | 12 | 75 | 900 |
| Commissioning Agent | R-23 | 30 | 160 | 4,800 |
| **Total** | | **80** | | **11,290** |

## Third-Party / Inspection Fees

| Item | LineID | Amount (CAD) | Source |
|---|---|---|---|
| Crane load testing (2 x 5-tonne cranes) | DL-020-01-011 | 6,000 | Fees_Permits_Insurance.csv FP-09 |
| Safety Code inspection coordination | DL-020-01-018 | 3,500 | Fees_Permits_Insurance.csv FP-10 |
| **Total** | | **9,500** | |

## Key Warnings and Coverage Gaps

1. **Non-labour costs not modelled (except third-party fees).** The parametric model covers professional staff labour and third-party inspection fees. Non-labour costs (test equipment rental, consumables, printing/binding for O&M manuals, training materials) are assumed negligible for an industrial commissioning scope of this size but are not explicitly priced.

2. **All acceptance criteria TBD.** Specific performance acceptance criteria for most systems depend on IFC design documents not yet available. This does not affect cost estimation but introduces risk of scope change if criteria reveal additional testing requirements.

3. **Commissioning Agent not yet assigned.** The role is priced at the parametric rate ($160/hr) but the actual cost will depend on whether a dedicated Cx Agent is engaged or the PM absorbs the role.

4. **Third-party fee confidence is LOW.** Crane load testing ($6,000) and Safety Code inspection ($3,500) are parametric estimates from Fees_Permits_Insurance.csv with LOW confidence. Actual quotes may vary.

## Change from Prior Snapshot

| Metric | Prior (2026-02-27) | Current (2026-02-28) | Delta |
|---|---|---|---|
| Total (CAD) | 11,290 | 20,790 | +9,500 |
| TBD items | 2 | 0 | -2 |
| Line count | 18 | 18 | 0 |
