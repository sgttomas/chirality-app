# Summary — EST_DEL-013-02_2026-02-27_0901

## Basis of Estimate Used

| Field | Value |
|---|---|
| **BASIS_OF_ESTIMATE** | PARAMETRIC |
| **FALLBACK_POLICY** | ALLOW_PARAMETRIC |
| **ALLOW_MIXED_METHODS** | TRUE |
| **CURRENCY** | CAD |
| **Methods Used** | PARAMETRIC (23 lines), ALLOWANCE (1 line — equipment MS-03) |
| **Mixed Method Justification** | Equipment unit (ITM-001) priced from Mechanical_System_Rates.csv as ALLOWANCE per ALLOW_MIXED_METHODS=TRUE and FALLBACK_POLICY=ALLOW_PARAMETRIC |

---

## Total by Package / Deliverable

| WBS_PackageID | WBS_DeliverableID | Currency | Total |
|---|---|---|---|
| PKG-013 | DEL-013-02 | CAD | **$82,423.60** |

---

## Total by CBS Category

| CBS | Currency | Amount | Line Count | Notes |
|---|---|---|---|---|
| EQUIPMENT | CAD | $13,500.00 | 1 | HRV/ERV unit supply (ALLOWANCE from MS-03) |
| MATERIAL+LABOUR | CAD | $40,786.40 | 8 | Ductwork, wall penetrations, fire stopping, vibration isolation, controls, condensate drain |
| LABOUR | CAD | $17,247.20 | 7 | Equipment installation, heating integration, electrical connection, shop drawings, closeout docs, HVAC trades, general labourer |
| COMMISSIONING | CAD | $3,800.00 | 1 | Commissioning agent + controls specialist |
| PERMITS | CAD | $1,500.00 | 1 | Mechanical permit and inspections |
| PROFESSIONAL | CAD | $5,590.00 | 6 | PM, CPM, Superintendent, Estimator, QA/QC, HSE |
| **TOTAL** | **CAD** | **$82,423.60** | **24** | |

---

## Key Warnings and Coverage Gaps

| ID | Warning | Impact |
|---|---|---|
| W-001 | Air exchange capacity (CFM) is TBD — equipment unit price from MS-03 is an ALLOWANCE range ($9K–$18K); actual price will depend on unit selection by Mechanical Engineer | Equipment cost could range from $9,000 to $18,000 (current estimate uses $13,500 midpoint) |
| W-002 | Distribution ductwork quantity is parametric (35% of whole-building ductwork at $60/m2 x 1,208 m2) — actual allocation depends on HVAC design | Ductwork cost ($25,368) is the largest single line; high sensitivity to design outcome |
| W-003 | Several items priced using parametric assumptions without rate-table backing: vibration isolation ($2,000), controls ($4,500), heating integration ($3,500), permits ($1,500), condensate drain ($800), closeout ($1,500) | Combined $13,800 of assumption-based items (17% of total) |
| W-004 | Electrical scope boundary PKG-013/PKG-015 is TBD | Power connection allowance ($1,200) may shift depending on scope split |
| W-005 | HVAC labour hours (80 hrs ductwork + 16 hrs install + 16 hrs intake + 16 hrs exhaust + misc) are parametric estimates | Labour costs sensitive to actual ductwork complexity and building geometry |

---

## Coverage Summary

| Metric | Value |
|---|---|
| Deliverables in scope | 1 |
| Items extracted (Items.csv) | 24 |
| Lines priced (Detail.csv) | 24 |
| Lines with Amount = TBD | 0 |
| Lines with Method = PARAMETRIC | 23 |
| Lines with Method = ALLOWANCE | 1 |
| Provenance completeness (non-TBD SourceRef) | 100% (24/24) |
| Lines with Confidence = LOW | 3 (L-001, L-008, L-010) |
| Lines with Confidence = MEDIUM | 21 |
