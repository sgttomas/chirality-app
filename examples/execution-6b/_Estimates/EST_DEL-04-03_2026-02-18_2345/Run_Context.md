# Run Context

| Field | Value |
|---|---|
| **RunID** | EST_DEL-04-03_2026-02-18_2345 |
| **AsOf** | 2026-02-18T23:45:00-07:00 |
| **Scope** | DEL-04-03 |
| **ScopeResolvedSummary** | 1 deliverable in scope; 0 excluded; 0 blocked |
| **BASIS_OF_ESTIMATE** | RATE_TABLE |
| **CURRENCY** | CAD |
| **PRICE_SOURCES** | Professional_Staff_Rates.csv; Level_of_Effort.csv; Assumed_Project_Parameters.csv |
| **DECOMPOSITION_PATH** | _Decomposition/Penhold_PSB_Project_Decomposition_v2.md (v2.3 FINAL) |
| **DEPENDENCY_SOURCES** | AUTO (read DEL-04-03/Dependencies.csv) |
| **FALLBACK_POLICY** | STRICT |
| **ALLOW_MIXED_METHODS** | FALSE |
| **UPDATE_LATEST_POINTER** | FALSE |
| **Rounding** | DOLLAR |
| **Warnings** | None |

## Scope Resolution

| DeliverableID | PackageID | Path | InScope | Notes |
|---|---|---|---|---|
| DEL-04-03 | PKG-004 | PKG-004_Sustainability_and_Energy/1_Working/DEL-04-03_ElectricalEnergyEfficiency/ | TRUE | Electrical Energy Efficiency (T2, Narrative) |

## CBS Mapping Rule

CBS codes are assigned using a deterministic discipline-based rule:
- Deliverables authored by Electrical Engineer -> `PROF_SERVICES.ELECTRICAL`

This rule is documented here for reproducibility. No explicit `CBSHint` was present in the decomposition.

## Pricing Methodology

- Hours sourced from `Level_of_Effort.csv` (filtered to Execution=6b, DeliverableID=DEL-04-03)
- Hourly rates sourced from `Professional_Staff_Rates.csv` (matched by RoleID)
- Amount = Qty (hours) x UnitRate (hourly rate), rounded to nearest dollar per ROUNDING=DOLLAR
- FALLBACK_POLICY=STRICT: no line items priced without basis evidence
- ALLOW_MIXED_METHODS=FALSE: all line items use Method=RATE_TABLE
