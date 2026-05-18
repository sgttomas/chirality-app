# Estimate Summary — EST_DEL-018-01_2026-02-27_0600

## Basis of Estimate

| Field | Value |
|-------|-------|
| **BASIS_OF_ESTIMATE** | PARAMETRIC |
| **CURRENCY** | CAD |
| **FALLBACK_POLICY** | ALLOW_PARAMETRIC |
| **ALLOW_MIXED_METHODS** | TRUE |
| **Scope** | DEL-018-01 — Topsoil Stripping (PKG-018 — Sitework & Civil Construction) |
| **Run Timestamp** | 2026-02-27T06:00:00-07:00 |

The estimate uses a PARAMETRIC basis with unit rates from the Earthwork_Civil_Rates.csv, Construction_Labour_Rates.csv, and Professional_Staff_Rates.csv rate tables. Level of effort hours are drawn from Level_of_Effort.csv. Lump-sum items without direct rate evidence are priced as ALLOWANCE under the ALLOW_PARAMETRIC fallback policy.

---

## Total by Deliverable

| DeliverableID | Name | Currency | Total Amount | Line Count | Notes |
|---------------|------|----------|-------------|------------|-------|
| DEL-018-01 | Topsoil Stripping | CAD | $32,943.60 | 16 | Includes earthwork, professional staff, construction labour, management, environmental, safety, and survey |

---

## Total by CBS (Cost Breakdown Structure)

| CBS | Description | Amount (CAD) | % of Total | Line Count |
|-----|-------------|-------------|-----------|------------|
| EARTHWORK | Topsoil strip + mob/demob + stockpile | $16,200.00 | 49.2% | 3 |
| STAFF | Professional staff (management, supervision, QA, HSE) | $5,590.00 | 17.0% | 6 |
| LABOUR | Construction trade labour (operator + labourer) | $3,153.60 | 9.6% | 2 |
| MGMT | Pre-construction assessment + final inspection | $2,500.00 | 7.6% | 2 |
| ENVIRO | Erosion and sediment control | $2,500.00 | 7.6% | 1 |
| SURVEY | Staking and stockpile layout | $1,800.00 | 5.5% | 1 |
| SAFETY | Utility locate and ground disturbance permit | $1,200.00 | 3.6% | 1 |
| **TOTAL** | | **$32,943.60** | **100.0%** | **16** |

---

## Total by Method

| Method | Amount (CAD) | % of Total | Line Count |
|--------|-------------|-----------|------------|
| PARAMETRIC | $19,943.60 | 60.5% | 9 |
| ALLOWANCE | $13,000.00 | 39.5% | 7 |
| **TOTAL** | **$32,943.60** | **100.0%** | **16** |

---

## Key Warnings and Coverage Gaps

1. **Stripping area is TBD.** The 3,500 m2 area is a parametric assumption (ASM-002) pending site survey (SURVEY-001) and IFC drawings (DEL-005-02). The earthwork cost ($11,200) is the single largest line item and is directly proportional to this assumed area. If the actual area is larger, the total will increase significantly.

2. **Topsoil depth is TBD.** The 200 mm average depth is a parametric assumption (ASM-003). The EC-04 rate ($3.20/m2) is an all-in rate for stripping + stockpile that implicitly incorporates typical depth conditions. If depth is materially different, the unit rate and/or labour hours may need adjustment.

3. **39.5% of the total is ALLOWANCE.** Seven lump-sum items (mob/demob, pre-construction assessment, utility locate, staking, erosion control, stockpile protection, final inspection) are priced as allowances with LOW confidence due to lack of specific rate evidence. These represent $13,000 of the total.

4. **No IFC drawings available.** The stripping limits, subgrade elevations, and exact scope are all TBD pending issuance of DEL-005-02 (Site Grading Plan). This is the most critical input gap.

5. **Labour hours are parametric.** Equipment operator (24 hrs) and labourer (16 hrs) hours are derived from production rate assumptions, not from a specific work plan or schedule.

---

## Scope Coverage

| Aspect | Status |
|--------|--------|
| Deliverables in scope | 1 of 1 (DEL-018-01) |
| Documents read | 4 of 4 (Datasheet, Specification, Guidance, Procedure) + _CONTEXT.md |
| Items extracted | 16 |
| Items priced | 16 of 16 (100%) |
| Items with TBD amounts | 0 |
| Provenance completeness | 100% (all lines have SourceRef) |
| Confidence distribution | 9 MED, 7 LOW |
