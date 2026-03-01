# Source Index

**RunID:** EST_DEL-004-07_2026-02-28_0810

---

## Price Sources

### PS-01 — Professional_Staff_Rates.csv

| Field | Value |
|---|---|
| **Path** | _EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Professional_Staff_Rates.csv |
| **Source Type** | Rate Table (Parametric) |
| **Content** | 25 professional staff roles with hourly rates in CAD |
| **Basis** | PARAMETRIC |
| **Confidence** | MEDIUM (all rates) |
| **Supports** | Unit rate pricing for all labour line items (LN-001 through LN-004) |
| **Parsing Notes** | Standard CSV; 7 columns; RoleID as key; HourlyRate_CAD as rate field |
| **Limitations** | Rates are parametric estimates, not confirmed quotes; no overtime/premium rates included |

### PS-02 — Level_of_Effort.csv

| Field | Value |
|---|---|
| **Path** | _EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Level_of_Effort.csv |
| **Source Type** | Parametric Model (Labour Hours) |
| **Content** | Estimated hours per role per deliverable for the entire project |
| **Basis** | PARAMETRIC |
| **Confidence** | MEDIUM (all entries for DEL-004-07 are PARAMETRIC basis) |
| **Supports** | Quantity (hours) for line items LN-001 through LN-004 |
| **Parsing Notes** | Standard CSV; 8 columns; filtered to DeliverableID = DEL-004-07; 4 matching rows (R-01, R-08, R-13, R-16) totaling 130 hours |
| **Limitations** | Hours are parametric estimates for a drawing set deliverable; not validated against actual project complexity. Low-voltage scope is narrow (2 confirmed systems) but 1 residual TBD exists. |

### PS-03 — Assumed_Project_Parameters.csv

| Field | Value |
|---|---|
| **Path** | _EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Assumed_Project_Parameters.csv |
| **Source Type** | Parametric Parameters |
| **Content** | 19 project-level parameters (identity, location, contract, facility, equipment, currency) |
| **Basis** | Mixed (CONFIRMED, DERIVED, ASSUMPTION, DESIGN_BASIS) |
| **Supports** | Context validation — currency CAD (PP-17), facility area 13,000 sqft (PP-10), ceiling 35 ft (PP-11) |
| **Parsing Notes** | Standard CSV; 8 columns |
| **Limitations** | Does not contain line-item pricing data; provides context parameters only |

### PS-04 — Professional_Design_Fees.csv

| Field | Value |
|---|---|
| **Path** | _EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Professional_Design_Fees.csv |
| **Source Type** | Parametric Model (Fee Percentage) |
| **Content** | Design fee percentages by discipline as % of construction value |
| **Basis** | PARAMETRIC |
| **Confidence** | MEDIUM |
| **Supports** | Alternative cross-check for electrical design cost (DF-04: 1.6% of construction value); not used as primary pricing method for this deliverable because (a) construction value is not yet established, and (b) DF-04 covers all of PKG-004 not just DEL-004-07 |
| **Parsing Notes** | Standard CSV; 10 columns; DF-04 row applicable to Electrical discipline |
| **Limitations** | Requires known construction value to compute; applies to full PKG-004 not individual deliverables; used for reasonableness cross-check only |

---

## Document Sources (Deliverable Content)

| Source | Path | Usage |
|---|---|---|
| Datasheet.md | PKG-004_Electrical Design/1_Working/DEL-004-07_Low-Voltage-Plans/Datasheet.md | Priceable item identification — low-voltage systems, facility context, conditions, construction attributes |
| Specification.md | PKG-004_Electrical Design/1_Working/DEL-004-07_Low-Voltage-Plans/Specification.md | Requirements (REQ-007-01 through REQ-007-09), verification activities, standards |
| Guidance.md | PKG-004_Electrical Design/1_Working/DEL-004-07_Low-Voltage-Plans/Guidance.md | Design context, trade-offs, scope uncertainty, coordination considerations |
| Procedure.md | PKG-004_Electrical Design/1_Working/DEL-004-07_Low-Voltage-Plans/Procedure.md | Work steps (8 steps), prerequisites, verification checks, records |
| _CONTEXT.md | PKG-004_Electrical Design/1_Working/DEL-004-07_Low-Voltage-Plans/_CONTEXT.md | Deliverable identity, package, discipline, type |

---

## Decomposition Source

| Source | Path | Usage |
|---|---|---|
| WDMLRL_Decomposition_Claude.md | _Decomposition/WDMLRL_Decomposition_Claude.md | WBS traceability (PKG-004, DEL-004-07); SOW mapping (SOW-0014, SOW-0064, SOW-0065); objective mapping (OBJ-001, OBJ-003, OBJ-005) |
