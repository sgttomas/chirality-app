# Summary — EST_DEL-014-04_2026-02-27_1130

## Basis of Estimate Used

| Field | Value |
|---|---|
| **BASIS_OF_ESTIMATE** | PARAMETRIC |
| **FALLBACK_POLICY** | ALLOW_PARAMETRIC |
| **ALLOW_MIXED_METHODS** | TRUE |
| **CURRENCY** | CAD |
| **Method Mix** | PARAMETRIC: 10 lines; RATE_TABLE: 17 lines |

This estimate uses a parametric basis. Where rate tables were available in PRICE_SOURCES (underground sanitary piping, plumber and labourer labour rates, professional staff rates with level-of-effort allocations), those rates were applied directly (Method=RATE_TABLE). Where no rate table existed (drain bodies, grates, traps, trap primers, above-ground vent piping, permit fees, coordination costs), parametric estimates were used based on Alberta industrial construction benchmarks (Method=PARAMETRIC, Confidence=LOW).

---

## Total by Deliverable

| WBS_DeliverableID | Deliverable Name | Currency | Total |
|---|---|---|---|
| DEL-014-04 | Floor Drains & Sump Drains | CAD | **$38,094.40** |

---

## Total by CBS Category

| CBS | Description | Amount (CAD) | % of Total |
|---|---|---|---|
| MAT-PLUMB | Drain materials (bodies, grates, traps, primers) | $9,065.00 | 23.8% |
| MAT-PIPE | Drain piping (underground + above-ground) | $10,225.00 | 26.8% |
| LAB-PLUMB | Plumber trade labour | $8,352.00 | 21.9% |
| LAB-GEN | General labourer | $1,562.40 | 4.1% |
| MGMT-COORD | Submittal and coordination | $1,500.00 | 3.9% |
| PERMIT-INSP | Permit and inspection fees | $1,800.00 | 4.7% |
| MGMT-PM | Project management (PM, Constr PM, Cost Est) | $2,770.00 | 7.3% |
| MGMT-FIELD | Site superintendent | $1,450.00 | 3.8% |
| QA-QC | QA/QC lead | $810.00 | 2.1% |
| HSE | HSE manager | $560.00 | 1.5% |
| **TOTAL** | | **$38,094.40** | **100.0%** |

---

## Cost Breakdown Summary

| Category | Amount (CAD) | % of Total |
|---|---|---|
| Materials (drain bodies + piping) | $19,290.00 | 50.7% |
| Direct trade labour (plumber + labourer) | $9,914.40 | 26.0% |
| Management and supervision | $5,590.00 | 14.7% |
| Permits, inspections, and coordination | $3,300.00 | 8.7% |
| **TOTAL** | **$38,094.40** | **100.0%** |

---

## Key Warnings and Coverage Gaps

| ID | Warning | Impact |
|---|---|---|
| W-01 | Drain type, body material, grate material, body diameter, flow rate, and trap type are all TBD per IFC plumbing design (DEL-006-03) | Material unit rates are parametric (LOW confidence); actual costs may vary significantly when specifications are finalized |
| W-02 | Sump drain quantity assumed minimum 2 (one per repair bay); final count per IFC design | Could increase if design adds more sump points |
| W-03 | No dedicated plumbing drain/fixture unit pricing in PRICE_SOURCES | 10 of 27 line items priced parametrically without rate table support |
| W-04 | Oil/grease interceptor requirement TBD (REQ-014-04-11) | If required, interceptor supply and installation cost is NOT included in this estimate; could add $3,000-$8,000+ |
| W-05 | Wash bay drain scope boundary with DEL-018-05 is TBD | Interior drain body and stub to exterior wall included; exterior drainage piping to mud sump excluded |
| W-06 | Pipe run lengths are parametric estimates based on building geometry (~13,000 sqft, 35 ft ceiling) | Actual routing TBD per IFC plumbing drawings; lengths could vary +/-30% |
| W-07 | Plumber labour hours are parametric; no production rate data in PRICE_SOURCES | Labour hours could vary depending on site conditions and drain specifications |
