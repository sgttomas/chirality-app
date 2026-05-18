# Run Context

| Field | Value |
|---|---|
| **RunID** | EST_DEL-01-03_2026-02-18_1400 |
| **AsOf** | 2026-02-18T14:00:00-07:00 |
| **Scope** | DEL-01-03 |
| **ScopeResolvedSummary** | 1 deliverable in scope; 0 excluded; 0 blocked |
| **BASIS_OF_ESTIMATE** | RATE_TABLE |
| **CURRENCY** | CAD |
| **PRICE_SOURCES** | Professional_Staff_Rates.csv, Level_of_Effort.csv, Assumed_Project_Parameters.csv, Fees_Permits_Insurance.csv |
| **DECOMPOSITION_PATH** | _Decomposition/Penhold_PSB_Project_Decomposition_v2.md (v2.3 FINAL) |
| **DEPENDENCY_SOURCES** | AUTO (read DEL-01-03/Dependencies.csv -- 13 rows) |
| **FALLBACK_POLICY** | ALLOW_ALLOWANCE |
| **ALLOW_MIXED_METHODS** | TRUE |
| **UPDATE_LATEST_POINTER** | FALSE |
| **Rounding** | DOLLAR |
| **Warnings** | None |

---

## Resolved Pricing Logic

### Production Cost (RATE_TABLE method)
- Hours by role from `Level_of_Effort.csv` (filtered to DEL-01-03)
- Hourly rates from `Professional_Staff_Rates.csv`
- Computation: Hours x HourlyRate = Amount per line

### Premium Allowances (ALLOWANCE method)
- Premiums from `Fees_Permits_Insurance.csv` (FP-01, FP-02, FP-03, FP-19)
- Contract value basis from `Assumed_Project_Parameters.csv` (PP-25 = $12,000,000 estimated total project value)
- Bond/insurance premiums are ALLOWANCE lines because actual contract value is TBD until Schedule A is priced
- Convention: Qty=1, Unit=LS, UnitRate=Amount

### CBS Mapping Rule
- Production hours for bonding/insurance documentation: CBS = `01.ADMIN.BOND_INS`
- Bond/insurance premiums: CBS = `01.PREMIUM.BOND` and `01.PREMIUM.INS`
- Surety broker fee: CBS = `01.PREMIUM.BROKER`
- This is a deterministic mapping; no CBSHint was provided in the decomposition

### Mixed Method Justification
- `ALLOW_MIXED_METHODS=TRUE` and `FALLBACK_POLICY=ALLOW_ALLOWANCE`
- Production hours are priced via RATE_TABLE (primary basis)
- Bond/insurance premiums are priced via ALLOWANCE (contract value is TBD; premiums are percentage-based estimates)
- This mixed approach is explicitly authorized by the brief's Special Instructions
