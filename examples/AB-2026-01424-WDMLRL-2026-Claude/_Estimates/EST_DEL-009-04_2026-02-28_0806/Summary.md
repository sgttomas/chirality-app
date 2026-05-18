# Summary.md
## Estimate Snapshot — DEL-009-04 Code Compliance Register & Inspection Log

---

## Basis of Estimate

| Field | Value |
|---|---|
| **BASIS_OF_ESTIMATE** | PARAMETRIC |
| **Method** | Hours (from Level_of_Effort.csv) x Rates (from Professional_Staff_Rates.csv); 3 items as fixed ALLOWANCE |
| **Currency** | CAD |
| **FALLBACK_POLICY** | ALLOW_PARAMETRIC |
| **ALLOW_MIXED_METHODS** | TRUE |
| **RUN_STATUS** | WARNINGS |

---

## Totals

### By Package / Deliverable

| WBS_PackageID | WBS_DeliverableID | Priced Amount (CAD) | TBD Lines | Priced Lines | Notes |
|---|---|---|---|---|---|
| PKG-009 | DEL-009-04 | 10,670.00 | 0 | 20 | All lines priced; 3 ALLOWANCE items at LOW confidence |

### By CBS

| CBS | Priced Amount (CAD) | PARAMETRIC Lines | ALLOWANCE Lines |
|---|---|---|---|
| Professional Services | 10,670.00 | 17 | 3 |

### By Method

| Method | Amount (CAD) | Line Count |
|---|---|---|
| PARAMETRIC | 6,770.00 | 17 |
| ALLOWANCE | 3,900.00 | 3 |
| **Total** | **10,670.00** | **20** |

### LOE Source Totals (Cross-check)

| Role | Hours | Rate (CAD/h) | Amount (CAD) | Source |
|---|---|---|---|---|
| R-01 Project Manager | 6 | 165.00 | 990.00 | Level_of_Effort.csv row 255 |
| R-06 QA/QC Lead | 16 | 135.00 | 2,160.00 | Level_of_Effort.csv row 580 |
| R-08 Cost Estimator | 4 | 135.00 | 540.00 | Level_of_Effort.csv row 256 |
| R-09 Document Controller | 12 | 75.00 | 900.00 | Level_of_Effort.csv row 581 |
| R-22 Permitting Specialist | 20 | 125.00 | 2,500.00 | Level_of_Effort.csv row 582 |
| **Total LOE** | **58** | | **7,090.00** | |

### LOE Hours Allocation vs. Detail Lines

| Role | LOE Total Hours | Hours Allocated in Detail | Remaining | Notes |
|---|---|---|---|---|
| R-01 PM | 6 | 6 (DL-019) | 0 | Fully allocated across DL-001 through DL-008 |
| R-06 QA/QC Lead | 16 | 6+4+2+2=14 consumed explicitly | 2 | DL-010(2h) + DL-012(4h) + DL-018(2h partial) + DL-015 allowance absorbs ~4h equivalent |
| R-08 CE | 4 | 4 (DL-020) | 0 | Fully allocated across DL-001 through DL-008 |
| R-09 Doc Controller | 12 | 6+2=8 consumed explicitly | 4 | DL-014(6h) + DL-018(2h partial); balance absorbed in allowance items |
| R-22 Permitting Specialist | 20 | 2+12+2=16 consumed explicitly | 4 | DL-009(2h) + DL-011(12h) + DL-018(2h partial); balance absorbed in allowance items |

The priced total of $10,670.00 CAD comprises:
- **$3,090.00** from prior-snapshot priced lines (DL-001 through DL-008 setup allocation + DL-019/DL-020 LOE source cross-checks)
- **$7,580.00** from newly resolved lines (DL-009 through DL-018)

DL-019 and DL-020 represent the original R-01 and R-08 LOE source amounts in aggregate form and are NOT additive with DL-001 through DL-008. The deduplicated estimate total is **$10,670.00**.

---

## Key Warnings

1. **3 ALLOWANCE items at LOW confidence:** DL-015 (deficiency tracking, $1,500), DL-016 (regulatory change, $900), and DL-017 (guarantee period, $1,500) are fixed allowances totalling $3,900 for operationally contingent activities whose scope cannot be parametrically derived from current sources.

2. **Allowance items represent 36.6% of total:** The $3,900 in allowances represents a material share of the $10,670 total and carries LOW confidence.

3. **LOE hours not fully consumed:** Approximately 6 LOE hours across R-06, R-09, and R-22 are implicitly absorbed within the allowance items rather than explicitly allocated to detail lines.

---

## Scope

- **Included:** DEL-009-04 -- Code Compliance Register & Inspection Log (1 deliverable in PKG-009)
- **Excluded:** All other deliverables and packages. Permit fees excluded per RFP S3.3.1 (County responsibility). Upstream permit deliverables (DEL-009-01, DEL-009-02, DEL-009-03) estimated separately.
