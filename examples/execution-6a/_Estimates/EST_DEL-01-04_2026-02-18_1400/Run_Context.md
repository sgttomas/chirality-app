# Run Context

| Field | Value |
|---|---|
| **RunID** | EST_DEL-01-04_2026-02-18_1400 |
| **AsOf** | 2026-02-18T14:00:00-07:00 |
| **Scope** | DEL-01-04 (Permitting, Inspections & AHJ Coordination) |
| **ScopeResolvedSummary** | 1 deliverable in scope; 0 excluded; 0 blocked |
| **BASIS_OF_ESTIMATE** | RATE_TABLE |
| **CURRENCY** | CAD |
| **PRICE_SOURCES** | Professional_Staff_Rates.csv; Level_of_Effort.csv; Assumed_Project_Parameters.csv; Fees_Permits_Insurance.csv |
| **DECOMPOSITION_PATH** | _Decomposition/Penhold_PSB_Project_Decomposition_FINAL_v1.0_PHASE7.md |
| **DEPENDENCY_SOURCES** | AUTO (read DEL-01-04/Dependencies.csv) |
| **FALLBACK_POLICY** | ALLOW_ALLOWANCE |
| **ALLOW_MIXED_METHODS** | TRUE |
| **UPDATE_LATEST_POINTER** | FALSE |
| **Rounding** | DOLLAR |
| **Warnings** | None critical. Mixed methods used as authorized (RATE_TABLE for labour; ALLOWANCE for permit fees). |

## Scope Resolution

| DeliverableID | PackageID | Path | InScope | Notes |
|---|---|---|---|---|
| DEL-01-04 | PKG-001 | PKG-001_General Requirements & Delivery Controls/1_Working/DEL-01-04_Permitting, Inspections & AHJ Coordination | TRUE | Permitting, Inspections & AHJ Coordination |

## CBS Mapping Rule

No explicit `CBSHint` was provided in the decomposition for DEL-01-04. The following deterministic mapping is applied:

- **01-MGMT**: Management and coordination labour (staff hours for permit coordination, AHJ liaison, documentation)
- **01-FEES**: Regulatory permit and inspection fees (building permit, development permit, trade permits)

This mapping is consistent with the deliverable's substance as described in the brief: "Management + Fees."

## Price Source Resolution

| Source File | Type | Supports |
|---|---|---|
| Professional_Staff_Rates.csv | Rate table | Hourly rates by role (R-01 through R-30) |
| Level_of_Effort.csv | Level of effort (hours) | Estimated hours by deliverable and role; rows for DEL-01-04 found (R-02: 40h, R-24: 12h) |
| Assumed_Project_Parameters.csv | Project parameters | PP-24 total construction value ($8,700,000 CAD) used as basis for percentage-based permit fee (FP-06) |
| Fees_Permits_Insurance.csv | Fee/permit schedule | Permit fee estimates FP-06 through FP-10; recommended rates used |
