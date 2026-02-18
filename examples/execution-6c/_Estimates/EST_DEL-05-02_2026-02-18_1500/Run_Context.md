# Run Context: EST_DEL-05-02_2026-02-18_1500

## Resolved Parameters

| Field | Value |
|---|---|
| **RunID** | EST_DEL-05-02_2026-02-18_1500 |
| **AsOf** | 2026-02-18T15:00:00-07:00 |
| **Scope** | DEL-05-02 |
| **ScopeResolvedSummary** | 1 deliverable in scope; 1 priced |
| **BASIS_OF_ESTIMATE** | RATE_TABLE (production lines) + PARAMETRIC/RATE_TABLE/ALLOWANCE (construction content) -- validated per BOE Section 3.2 dual cost nature |
| **CURRENCY** | CAD |
| **ROUNDING** | DOLLAR |
| **FALLBACK_POLICY** | ALLOW_ALLOWANCE |
| **ALLOW_MIXED_METHODS** | TRUE |
| **UPDATE_LATEST_POINTER** | FALSE |
| **OUTPUT_LABEL** | EST_DEL-05-02 |

## Resolved Paths

| Input | Resolved Path |
|---|---|
| RUN_ROOT | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6c |
| ESTIMATES_ROOT | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6c/_Estimates |
| DECOMPOSITION_PATH | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6c/_Decomposition/Penhold_PSB_Project_Decomposition_Final_AddendumIntegrated_v1.md |
| DEPENDENCY_SOURCES | AUTO -- read from DEL-05-02 deliverable folder Dependencies.csv |
| Dependencies.csv | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6c/PKG-02_Financial Proposal (Appendix H)/1_Working/DEL-05-02_AppendixH_ScheduleB_CostBreakdown/Dependencies.csv |

## Resolved PRICE_SOURCES

| # | File | Type | Key Items |
|---|---|---|---|
| 1 | Professional_Staff_Rates.csv | Rate table | 30 roles; R-02, R-18, R-19 used for production lines |
| 2 | Level_of_Effort.csv | Parametric hours | DEL-05-02 rows: R-18 (24 hrs), R-19 (16 hrs), R-02 (4 hrs) |
| 3 | Assumed_Project_Parameters.csv | Project parameters | PP-05 through PP-29 for quantity derivations |
| 4 | Structural_Concrete_Rates.csv | Construction rates | SC-01 through SC-15 for structural breakdown |
| 5 | Building_Envelope_Rates.csv | Construction rates | BE-01 through BE-15 for envelope breakdown |
| 6 | Interior_Architectural_Rates.csv | Construction rates | IA-01 through IA-25 for interior breakdown |
| 7 | Mechanical_System_Rates.csv | Construction rates | MS-01 through MS-14 for mechanical breakdown |
| 8 | Electrical_System_Rates.csv | Construction rates | ES-01 through ES-14 for electrical breakdown |
| 9 | Earthwork_Civil_Rates.csv | Construction rates | EC-01 through EC-11 for site/civil breakdown |
| 10 | Paving_Surfacing_Rates.csv | Construction rates | PS-01 through PS-09 for paving breakdown |
| 11 | Underground_Utility_Rates.csv | Construction rates | UU-01 through UU-12 for utility breakdown |
| 12 | Equipment_Pricing.csv | Construction pricing | EQ-01 through EQ-15 for equipment breakdown |
| 13 | Optional_Items_Pricing.csv | Construction pricing | OPT-01 through OPT-18 for options breakdown |
| 14 | Parametric_Building_Rates.csv | Parametric cross-check | PB-01 through PB-09 for cross-check |
| 15 | Construction_Labour_Rates.csv | Labour rates | T-01 through T-15 for reference |
| 16 | Professional_Design_Fees.csv | Design fees | DF-01 through DF-08 for fee breakdown |
| 17 | Fees_Permits_Insurance.csv | Fees and permits | FP-01 through FP-19 for bonds/insurance/permits |

## Reconciliation Context

DEL-05-01 (Schedule A) has already been estimated in snapshot EST_DEL-05-01_2026-02-18_1400 with the following totals:

| Schedule A Line | Amount (CAD) |
|---|---|
| Production cost (72 hrs) | $9,960 |
| Base Construction (excl. GST) | $9,863,000 |
| GST on Base (5%) | $493,000 |
| Additional Options (excl. GST) | $355,000 |
| GST on Options (5%) | $18,000 |
| Construction Content Total | $10,729,000 |
| Grand Total | $10,738,960 |

Schedule B construction pricing detail MUST reconcile to these Schedule A totals.

## CBS Mapping Rule

CBS codes are assigned as follows:
- FIN = Financial roles (estimator production hours)
- MGMT = Management roles (PM production hours)
- GR = General Requirements
- STRUCT = Structural and Concrete
- ENVLP = Building Envelope
- INTARCH = Interior Architectural
- MECH = Mechanical Systems
- ELEC = Electrical Systems
- CIVIL = Site/Civil Works
- UG = Underground Utilities
- EQUIP = Specialty Equipment
- COLDSTG = Cold Storage Building
- DESFEE = Professional Design Fees
- FEES = Bonds, Insurance, Permits
- OPT = Additional Options
- TAX = GST

## Warnings

- [WARNING] All construction pricing content is PARAMETRIC (no vendor quotes). Accuracy is +/-20-50%.
- [WARNING] OI-004 (FF&E) is implemented as recommended ($20k allowance) but is still formally OPEN per decomposition status.
- [WARNING] Schedule B detail provides MORE granularity than Schedule A summary; line items here are broken out further but must sum to Schedule A CBS-level totals.
