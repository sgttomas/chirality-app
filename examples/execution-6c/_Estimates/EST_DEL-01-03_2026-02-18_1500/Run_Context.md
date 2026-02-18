# Run Context: EST_DEL-01-03_2026-02-18_1500

| Field | Value |
|---|---|
| **RunID** | EST_DEL-01-03_2026-02-18_1500 |
| **AsOf** | 2026-02-18T15:00:00-07:00 |
| **Scope** | DEL-01-03 |
| **ScopeResolvedSummary** | 1 deliverable in scope; 1 priced |
| **BASIS_OF_ESTIMATE** | RATE_TABLE (production lines) + ALLOWANCE (bond/insurance premium lines) |
| **BOE_Source** | `_Estimates/BASIS_OF_ESTIMATE.md` (validated enum: RATE_TABLE per BOE Section 4 PKG-01 table; ALLOW_ALLOWANCE fallback enabled) |
| **CURRENCY** | CAD |
| **PRICE_SOURCES** | `Professional_Staff_Rates.csv`, `Level_of_Effort.csv`, `Fees_Permits_Insurance.csv`, `Assumed_Project_Parameters.csv` |
| **DECOMPOSITION_PATH** | `_Decomposition/Penhold_PSB_Project_Decomposition_Final_AddendumIntegrated_v1.md` |
| **DEPENDENCY_SOURCES** | AUTO (read `DEL-01-03/Dependencies.csv` -- 12 dependency rows) |
| **FALLBACK_POLICY** | ALLOW_ALLOWANCE |
| **ALLOW_MIXED_METHODS** | TRUE |
| **UPDATE_LATEST_POINTER** | FALSE |
| **Rounding** | DOLLAR |
| **Upstream Context** | DEL-05-01 Schedule A base construction = $9,863,000 (from EST_DEL-05-01_2026-02-18_1400). This provides the contract value basis for bond/insurance percentage calculations. |

---

## Resolved Defaults

- **CBS mapping rule**: Production lines assigned CBS=ADMIN (administrative effort) and CBS=LEGAL (legal review). Bond/insurance premium lines assigned CBS=BOND and CBS=INS. Surety broker fee assigned CBS=LEGAL.
- **Method mix**: RATE_TABLE for production hours; ALLOWANCE for bond/insurance premiums and broker fee. Mixed methods explicitly authorized by `ALLOW_MIXED_METHODS=TRUE` and `FALLBACK_POLICY=ALLOW_ALLOWANCE`.
- **Contract value for percentage calculations**: $9,863,000 (base construction excluding GST from DEL-05-01 Schedule A Summary L-010 through L-022 subtotal). This excludes Additional Options and GST per standard bonding practice.

## Warnings

- **W-001**: Bond premium rates (FP-01, FP-02) are MARKET estimates at MEDIUM confidence. Actual surety quotes should be obtained.
- **W-002**: Insurance rates (FP-03, FP-04, FP-05) are MARKET/LOW confidence estimates. Actual insurance quotes required before submission.
- **W-003**: RFP Section 5.3.1 bond requirements have not been fully extracted from the PDF (DEP-01-03-005 status PENDING). Bond types and amounts are assumed standard.
- **W-004**: Contract value basis ($9,863,000) is from a PARAMETRIC construction estimate (DEL-05-01). Actual construction pricing will change these premium amounts.
