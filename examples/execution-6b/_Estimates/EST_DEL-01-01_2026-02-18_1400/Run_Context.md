# Run Context

| Field | Value |
|---|---|
| **RunID** | EST_DEL-01-01_2026-02-18_1400 |
| **AsOf** | 2026-02-18T14:00:00 |
| **Scope** | DEL-01-01 |
| **ScopeResolvedSummary** | 1 deliverable in scope; 0 excluded; 0 blocked |
| **BASIS_OF_ESTIMATE** | RATE_TABLE |
| **CURRENCY** | CAD |
| **PRICE_SOURCES** | Professional_Staff_Rates.csv; Level_of_Effort.csv; Assumed_Project_Parameters.csv |
| **DECOMPOSITION_PATH** | _Decomposition/Penhold_PSB_Project_Decomposition_v2.md (v2.3 FINAL) |
| **DEPENDENCY_SOURCES** | AUTO (read DEL-01-01/Dependencies.csv) |
| **FALLBACK_POLICY** | STRICT |
| **ALLOW_MIXED_METHODS** | FALSE |
| **UPDATE_LATEST_POINTER** | FALSE |
| **Rounding** | DOLLAR |
| **Warnings** | None |

## Resolved Paths

- **ESTIMATES_ROOT:** `test/execution-6b/_Estimates/`
- **DELIVERABLE_PATH:** `test/execution-6b/PKG-001_Proposal_Compliance_Commercial_and_Team_Qualifications/1_Working/DEL-01-01_ComplianceMatrixAndChecklist/`
- **Professional_Staff_Rates.csv:** `test/execution-6b/_PriceSources/Professional_Staff_Rates.csv`
- **Level_of_Effort.csv:** `test/execution-6b/_PriceSources/Level_of_Effort.csv`
- **Assumed_Project_Parameters.csv:** `test/execution-6b/_PriceSources/Assumed_Project_Parameters.csv`
- **Dependencies.csv:** `DEL-01-01_ComplianceMatrixAndChecklist/Dependencies.csv` (18 rows; 0 blocking)

## CBS Mapping Rule

CBS codes are assigned deterministically based on the role `Category` field from `Professional_Staff_Rates.csv`:
- `Administrative` category roles -> CBS = `LABOUR.ADMIN`
- `Management` category roles -> CBS = `LABOUR.MGMT`
- `Design` category roles -> CBS = `LABOUR.DESIGN`
- `Production` category roles -> CBS = `LABOUR.PROD`
- `Construction` category roles -> CBS = `LABOUR.CONST`
- `Financial` category roles -> CBS = `LABOUR.FIN`
- `Legal` category roles -> CBS = `LABOUR.LEGAL`
- `Specialty` category roles -> CBS = `LABOUR.SPEC`
- `External` category roles -> CBS = `LABOUR.EXT`

For DEL-01-01, the only role is R-22 (Proposal Coordinator / Writer, Category=Administrative), mapped to CBS = `LABOUR.ADMIN`.

## BOE Context (from Brief)

- **Deliverable:** DEL-01-01 -- Compliance Matrix & Checklist
- **Tier:** T0 (no upstream production dependencies)
- **Substance:** Administrative
- **Cost Drivers:** Proposal coordinator hours; compliance review against all RFP sections; addenda integration checklist
- **Cost Ownership:** Compliance checking + addenda integration assigned to DEL-01-01; final PDF assembly + submission logistics assigned to DEL-01-02 (excluded from this estimate)
