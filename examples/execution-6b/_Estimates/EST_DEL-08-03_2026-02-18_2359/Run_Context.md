# Run Context

| Field | Value |
|---|---|
| **RunID** | EST_DEL-08-03_2026-02-18_2359 |
| **AsOf** | 2026-02-18T23:59:00-07:00 |
| **Scope** | DEL-08-03 |
| **ScopeResolvedSummary** | 1 deliverable in scope; 0 excluded; 0 blocked |
| **BASIS_OF_ESTIMATE** | RATE_TABLE |
| **CURRENCY** | CAD |
| **PRICE_SOURCES** | `test/execution-6b/_PriceSources/Professional_Staff_Rates.csv`, `test/execution-6b/_PriceSources/Level_of_Effort.csv`, `test/execution-6b/_PriceSources/Assumed_Project_Parameters.csv` |
| **DECOMPOSITION_PATH** | `test/execution-6b/_Decomposition/Penhold_PSB_Project_Decomposition_v2.md` (v2.3 FINAL) |
| **DEPENDENCY_SOURCES** | AUTO -- resolved to `test/execution-6b/PKG-008_Commissioning_Closeout_and_Warranty/1_Working/DEL-08-03_WarrantyRequirementsNarrative/Dependencies.csv` |
| **FALLBACK_POLICY** | STRICT |
| **ALLOW_MIXED_METHODS** | FALSE |
| **UPDATE_LATEST_POINTER** | FALSE |
| **Rounding** | DOLLAR |
| **OUTPUT_LABEL** | DEL-08-03 |
| **Warnings** | None |

## CBS Mapping Rule

Deterministic rule applied for this run: All DEL-08-03 line items are professional staff hours for narrative authoring. CBS assigned as `PROFESSIONAL_SERVICES` based on deliverable type (Commissioning / Narrative) and cost driver category (labour hours from rate table).

## Scope Resolution

DEL-08-03 (Warranty Requirements Narrative) is a single deliverable within PKG-008 (Commissioning, Closeout & Warranty). It implements SOW-0032 and supports OBJ-002. The responsible party is PM. Two staff roles contribute: Project Manager (R-02) and Commissioning Lead (R-21).

## Pricing Approach

Hours sourced from `Level_of_Effort.csv` (rows filtered to `DeliverableID=DEL-08-03`). Rates sourced from `Professional_Staff_Rates.csv` (matched by `RoleID`). Amount = Hours x Rate, rounded to nearest dollar per `ROUNDING=DOLLAR`. Method = RATE_TABLE for all lines.
