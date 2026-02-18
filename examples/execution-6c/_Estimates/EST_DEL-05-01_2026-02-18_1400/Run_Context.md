# Run Context

## Run Identity

| Field | Value |
|---|---|
| **RunID** | EST_DEL-05-01_2026-02-18_1400 |
| **AsOf** | 2026-02-18T14:00:00-07:00 |
| **Agent** | ESTIMATING (Type 2) |

---

## Brief Inputs (as provided)

| Parameter | Value |
|---|---|
| **SCOPE** | DEL-05-01 |
| **RUN_ROOT** | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6c |
| **ESTIMATES_ROOT** | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6c/_Estimates |
| **BASIS_OF_ESTIMATE** | RATE_TABLE (validated; per BOE Section 4 DEL-05-01 entry) |
| **CURRENCY** | CAD |
| **OUTPUT_LABEL** | EST_DEL-05-01 |
| **UPDATE_LATEST_POINTER** | FALSE |
| **FALLBACK_POLICY** | ALLOW_ALLOWANCE |
| **ALLOW_MIXED_METHODS** | TRUE |
| **ROUNDING** | DOLLAR |

---

## Resolved Inputs

| Parameter | Resolved Value |
|---|---|
| **DECOMPOSITION_PATH** | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6c/_Decomposition/Penhold_PSB_Project_Decomposition_Final_AddendumIntegrated_v1.md |
| **DEPENDENCY_SOURCES** | AUTO -- read from DEL-05-01 deliverable folder |
| **Dependencies.csv** | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6c/PKG-02_Financial Proposal (Appendix H)/1_Working/DEL-05-01_AppendixH_ScheduleA_PricingSummary/Dependencies.csv |

### PRICE_SOURCES (resolved)

| # | Path | Type | Status |
|---|---|---|---|
| 1 | Professional_Staff_Rates.csv | Rate Table (30 roles) | Loaded |
| 2 | Level_of_Effort.csv | Rate Table (hours; 3 rows for DEL-05-01) | Loaded |
| 3 | Assumed_Project_Parameters.csv | Parameters (29 params) | Loaded |
| 4 | Structural_Concrete_Rates.csv | Construction Rate Table (15 items) | Loaded |
| 5 | Building_Envelope_Rates.csv | Construction Rate Table (15 items) | Loaded |
| 6 | Interior_Architectural_Rates.csv | Construction Rate Table (25 items) | Loaded |
| 7 | Mechanical_System_Rates.csv | Construction Rate Table (14 items) | Loaded |
| 8 | Electrical_System_Rates.csv | Construction Rate Table (14 items) | Loaded |
| 9 | Earthwork_Civil_Rates.csv | Construction Rate Table (11 items) | Loaded |
| 10 | Paving_Surfacing_Rates.csv | Construction Rate Table (9 items) | Loaded |
| 11 | Underground_Utility_Rates.csv | Construction Rate Table (12 items) | Loaded |
| 12 | Equipment_Pricing.csv | Construction Equipment Pricing (15 items) | Loaded |
| 13 | Optional_Items_Pricing.csv | Optional Items Pricing (18 items) | Loaded |
| 14 | Parametric_Building_Rates.csv | Parametric Cross-Check (9 items) | Loaded |
| 15 | Construction_Labour_Rates.csv | Construction Labour Rates (15 trades) | Loaded |
| 16 | Professional_Design_Fees.csv | Design Fee Percentages (8 items) | Loaded |
| 17 | Fees_Permits_Insurance.csv | Fees/Permits/Insurance (19 items) | Loaded |

All files located under: /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6c/_PriceSources/

---

## Scope Resolved Summary

| Metric | Value |
|---|---|
| Deliverables in scope | 1 |
| Deliverables estimated | 1 |
| Deliverables blocked | 0 |
| Deliverables excluded | 0 |

---

## Dual Cost Nature

DEL-05-01 has two distinct line groups per BOE Section 3.2 and INDEX.md:

1. **Production cost lines** (Method=RATE_TABLE): Estimator/PM hours to compile the Schedule A form
2. **Construction pricing content lines** (Method=PARAMETRIC/ALLOWANCE): The actual proposal prices that populate Schedule A

Both line groups are present in Detail.csv. Production costs represent the cost of PREPARING the document. Construction pricing content represents the prices WRITTEN INTO the document.

---

## CBS Mapping Rule

CBS codes are assigned based on cost type:

| Cost Type | CBS Code | Description |
|---|---|---|
| Production -- Financial roles | FIN | Estimator/PM hours to compile Schedule A |
| Production -- Management roles | MGMT | PM review and pricing strategy |
| Construction content -- General Requirements | GR | General requirements and project overhead |
| Construction content -- Building Structure | STRUCT | Structural and concrete scope |
| Construction content -- Building Envelope | ENVLP | Envelope and cladding scope |
| Construction content -- Interior | INTARCH | Interior architectural finishes |
| Construction content -- Mechanical | MECH | Mechanical systems |
| Construction content -- Electrical | ELEC | Electrical systems |
| Construction content -- Site/Civil | CIVIL | Earthwork, paving, utilities |
| Construction content -- Equipment | EQUIP | Specialty equipment |
| Construction content -- Design Fees | DESFEE | Professional design fees |
| Construction content -- Fees/Permits/Insurance | FEES | Permits, bonds, insurance |
| Construction content -- Optional Items | OPT | Additional Options 1-6 |

---

## Warnings

1. **ALLOW_MIXED_METHODS=TRUE**: This run intentionally uses mixed methods (RATE_TABLE for production lines; PARAMETRIC and ALLOWANCE for construction content lines) per BOE Section 3.2.
2. **OI-004 (FF&E)**: Resolved per BOE recommendation as $20,000 cash allowance under Additional Option 6 (OPT-18).
3. **Construction pricing confidence is LOW to MEDIUM**: All construction content lines are parametric estimates; no vendor quotes obtained.
4. **Bond/insurance percentages applied to base construction value**: Uses PP-24 ($8,700,000) as the base for percentage calculations.
5. **Parametric cross-check**: PB-07 suggests $415/sf for combined facility = $7,470,000 for 18,000 sf main building (vs our $6,600,000 from PP-21). Difference is within parametric range; PP-21 used as stated.
