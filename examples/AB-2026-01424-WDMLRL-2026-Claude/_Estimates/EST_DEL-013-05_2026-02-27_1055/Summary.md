# Estimate Summary — DEL-013-05: Welding Station Exhaust System

## Basis of Estimate

| Field | Value |
|---|---|
| BASIS_OF_ESTIMATE | PARAMETRIC |
| FALLBACK_POLICY | ALLOW_PARAMETRIC |
| ALLOW_MIXED_METHODS | TRUE |
| CURRENCY | CAD |
| RunID | EST_DEL-013-05_2026-02-27_1055 |

The estimate uses a **PARAMETRIC** basis. Equipment and materials pricing is derived from the Mechanical_System_Rates.csv allowance rate MS-05 ("Welding station exhaust/vent system" at $8,000/EA recommended, range $4,500-$12,000). Labour, professional services, and management hours are derived from parametric rates in Professional_Staff_Rates.csv, Construction_Labour_Rates.csv, and Level_of_Effort.csv. Mixed methods (PARAMETRIC + ALLOWANCE) are applied under ALLOW_MIXED_METHODS=TRUE.

---

## Total Estimated Cost

| Category | Amount (CAD) |
|---|---|
| **TOTAL** | **$22,338.70** |

---

## Breakdown by Cost Breakdown Structure (CBS)

| CBS | Amount (CAD) | % of Total | Line Count |
|---|---|---|---|
| MECHANICAL-EQUIP | $8,000.00 | 35.8% | 9 |
| MANAGEMENT | $3,680.00 | 16.5% | 3 |
| DESIGN-ENGINEERING | $2,640.00 | 11.8% | 1 |
| CONSTRUCTION-LABOUR | $2,618.70 | 11.7% | 2 |
| COMMISSIONING | $1,280.00 | 5.7% | 1 |
| PROCUREMENT | $1,110.00 | 5.0% | 1 |
| QA-QC | $810.00 | 3.6% | 1 |
| CLOSEOUT | $600.00 | 2.7% | 1 |
| HSE | $560.00 | 2.5% | 1 |
| ESTIMATING | $540.00 | 2.4% | 1 |
| PERMITTING | $500.00 | 2.2% | 1 |
| **TOTAL** | **$22,338.70** | **100.0%** | **22** |

---

## Breakdown by WBS

| WBS_PackageID | WBS_DeliverableID | Amount (CAD) |
|---|---|---|
| PKG-013 | DEL-013-05 | $22,338.70 |

---

## Method Mix

| Method | Line Count | Amount (CAD) | % of Total |
|---|---|---|---|
| ALLOWANCE | 9 | $8,000.00 | 35.8% |
| PARAMETRIC | 13 | $14,338.70 | 64.2% |
| **TOTAL** | **22** | **$22,338.70** | **100.0%** |

ALLOWANCE method is used for equipment/materials (MS-05 system rate) under FALLBACK_POLICY=ALLOW_PARAMETRIC. PARAMETRIC method is used for all labour and professional services.

---

## Key Warnings and Coverage Gaps

| Warning ID | Description | Impact |
|---|---|---|
| W-001 | Number of welding stations TBD (1 shown on plans, final count pending County confirmation). Estimate assumes 1 station. | If more than 1 station is required, the equipment, materials, ductwork, and installation labour costs will scale approximately linearly. The MS-05 rate of $8,000 is per station. |
| W-002 | Many system design parameters remain TBD (airflow CFM, capture velocity, filtration type/efficiency, fan size, ductwork routing, stack height). | Equipment pricing is based on a parametric allowance (MS-05) which is LOW confidence with a wide range ($4,500-$12,000). Actual cost may differ significantly from the $8,000 recommended rate. |
| W-003 | Welding process types TBD (County to supply equipment specifications per R-01 Section 3.4). | Welding process directly affects filtration requirements and cost. High-particulate processes (e.g., flux-core) or exotic base metals (e.g., stainless steel with hexavalent chromium) could require more expensive filtration. |
| W-004 | MS-05 rate basis is ALLOWANCE with LOW confidence. Mixed method used under ALLOW_MIXED_METHODS=TRUE. | 35.8% of the total estimate relies on LOW confidence ALLOWANCE pricing. |
| W-005 | Spark arrestor (ITM-009 / DL-009) is priced at $0 pending design evaluation per REQ-013. | If required, estimated cost impact is $200-$500. |
| W-006 | Installation labour hours (28 hr) and design engineering hours (16 hr) are parametric estimates for a single-station system and could vary based on actual complexity. | Actual hours depend on duct routing complexity, building height (35 ft ceiling), and coordination with other systems. |

---

## Scope Coverage

- **Deliverables in scope:** 1 (DEL-013-05 Welding Station Exhaust System)
- **Documents read:** 4 of 4 (Datasheet.md, Specification.md, Guidance.md, Procedure.md) + _CONTEXT.md
- **Missing documents:** None
- **Items extracted:** 22 priceable items
- **Items priced:** 22 of 22 (100%)
- **Items with Amount = $0:** 1 (DL-009 spark arrestor, contingent on design evaluation)
