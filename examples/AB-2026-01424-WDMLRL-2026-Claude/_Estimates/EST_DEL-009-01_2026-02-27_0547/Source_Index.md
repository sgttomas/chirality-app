# Source Index — EST_DEL-009-01_2026-02-27_0547

## Pricing Sources

| # | Source File | Source Type | Parsing Notes | Supports |
|---|-----------|-------------|---------------|----------|
| 1 | `PriceSources/Professional_Staff_Rates.csv` | RATE_TABLE | 25 roles with CAD hourly rates; Basis=PARAMETRIC; Confidence=MEDIUM | Unit rates for all 6 labour line items (ITEM-001 through ITEM-006) |
| 2 | `PriceSources/Level_of_Effort.csv` | PARAMETRIC | Hours by DeliverableID x RoleID; 2 rows for DEL-009-01 totalling 10 hours across 2 roles (R-01: 6 hrs, R-08: 4 hrs) | Quantities (hours) for ITEM-001 and ITEM-002 only |
| 3 | `PriceSources/Assumed_Project_Parameters.csv` | PARAMETRIC | 19 project parameters; PP-17 confirms CAD currency; PP-03/PP-04 confirm location (Ferintosh AB / SW 14-44-21-W4) | Project context; currency confirmation; location context for disbursement estimates |

## Source Limitations

- **Level_of_Effort.csv coverage for DEL-009-01:** Only 2 roles (Project Manager and Cost Estimator) are represented, totalling 10 hours. The four deliverable documents describe substantial additional effort for permitting specialist coordination, document control, design support for application, and inspection coordination that is not captured in the LoE model. Four additional roles (R-22, R-09, R-11, R-17) are parametrically estimated outside the LoE.
- **No fees/permits pricing used:** Fees_Permits_Insurance.csv (FP-05) includes a safety code / building permit fee allowance, but development permit fees are explicitly excluded from Proponent scope (County pays per R-01 §3.3.1). No items from Fees_Permits_Insurance.csv are used in this estimate.
- **No disbursement rate source:** Pre-application consultation travel, courier delivery, and inspection coordination disbursements have no explicit source. All are parametric allowances (see Assumptions_Log ASM-007 through ASM-009).
- **LoE Notes column:** The Level_of_Effort.csv Notes column for DEL-009-01 rows shows "PKG-009 Project Manager — TBD", indicating the LoE model may not have been fully validated for this deliverable.
