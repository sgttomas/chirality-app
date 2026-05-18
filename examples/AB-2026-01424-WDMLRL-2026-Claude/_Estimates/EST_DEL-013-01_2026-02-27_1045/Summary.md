# Summary — EST_DEL-013-01_2026-02-27_1045

## Basis of Estimate

| Field | Value |
|---|---|
| **BASIS_OF_ESTIMATE** | PARAMETRIC |
| **FALLBACK_POLICY** | ALLOW_PARAMETRIC |
| **ALLOW_MIXED_METHODS** | TRUE |
| **CURRENCY** | CAD |
| **Methods Used** | PARAMETRIC (24 lines), ALLOWANCE (2 lines) |

The estimate for DEL-013-01 (High-Recovery Heating System) is derived primarily from parametric rates using the provided price source tables. Two line items use ALLOWANCE method where parametric models are insufficient: the heating unit equipment (MS-01) and the deficiency rectification allowance. Mixed methods are authorized per ALLOW_MIXED_METHODS=TRUE and supported by FALLBACK_POLICY=ALLOW_PARAMETRIC.

---

## Total by Deliverable

| WBS_DeliverableID | Deliverable Name | Currency | Total |
|---|---|---|---|
| DEL-013-01 | High-Recovery Heating System | CAD | **$135,120.00** |

---

## Total by CBS Category

| CBS | Currency | Amount | % of Total | Line Count |
|---|---|---|---|---|
| Materials | CAD | $76,980.00 | 57.0% | 2 |
| Labour | CAD | $23,900.00 | 17.7% | 6 |
| Equipment | CAD | $13,000.00 | 9.6% | 1 |
| Commissioning | CAD | $8,900.00 | 6.6% | 5 |
| Management | CAD | $5,590.00 | 4.1% | 6 |
| Admin | CAD | $4,250.00 | 3.1% | 5 |
| Contingency | CAD | $2,500.00 | 1.9% | 1 |
| **TOTAL** | **CAD** | **$135,120.00** | **100.0%** | **26** |

---

## Total by Package

| WBS_PackageID | Package Name | Currency | Total |
|---|---|---|---|
| PKG-013 | Mechanical & HVAC Installation | CAD | **$135,120.00** |

---

## Key Warnings and Coverage Gaps

| Warning ID | Description | Impact |
|---|---|---|
| W-001 | Heating capacity (BTU/h or kW) is TBD pending DEL-003-06 | Equipment pricing uses generic allowance rate; actual cost could vary significantly once capacity is known |
| W-002 | Fuel/energy source not formally confirmed (assumed natural gas) | Gas connection line item ($3,500) is conditional; if electric, cost profile changes |
| W-003 | Equipment type (radiant vs. forced-air vs. hydronic) TBD per DEL-003-07 | Equipment unit cost ($6,500/ea from MS-01) is a generic unit heater rate; high-recovery specific equipment may cost more |
| W-004 | BMS communication protocol TBD | Controls integration ($6,000) is a parametric allowance; actual cost depends on protocol complexity |
| W-005 | Ductwork quantity derived parametrically from floor area | Ductwork ($72,480) is the largest single line item; actual quantity will differ once mechanical drawings are issued |

---

## Confidence Assessment

- **HIGH confidence lines:** 0 (no quotes or confirmed quantities available)
- **MEDIUM confidence lines:** 20 (parametric rates from published rate tables with reasonable assumptions)
- **LOW confidence lines:** 6 (allowance-based or conditional items)
- **Overall confidence:** MEDIUM — parametric basis with multiple TBD design inputs outstanding

---

## Scope Coverage

- **Deliverables in scope:** 1 (DEL-013-01)
- **Documents read:** 5 of 5 (CONTEXT, Datasheet, Specification, Guidance, Procedure)
- **Missing documents:** 0
- **Items extracted:** 26
- **Items priced:** 26 of 26 (100%)
- **Items with TBD amount:** 0
