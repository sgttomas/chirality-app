# Run Context -- EST_DEL-018-06_2026-03-26_1759

| Field | Value |
|-------|-------|
| **RunID** | EST_DEL-018-06_2026-03-26_1759 |
| **AsOf** | 2026-03-26T17:59:00-06:00 |
| **Scope** | DEL-018-06 (Utility Tie-Ins) |
| **ScopeResolvedSummary** | 1 deliverable in scope (4 SOW items: SOW-0080, SOW-0081, SOW-0082, SOW-0122), 0 excluded, 0 blocked |
| **BASIS_OF_ESTIMATE** | RATE_TABLE |
| **CURRENCY** | CAD |
| **PRICE_SOURCES** | PriceSources/Professional_Staff_Rates.csv, PriceSources/Level_of_Effort.csv, PriceSources/Assumed_Project_Parameters.csv, PriceSources/Earthwork_Civil_Rates.csv, PriceSources/Underground_Utility_Rates.csv, PriceSources/Construction_Labour_Rates.csv, PriceSources/Electrical_System_Rates.csv, PriceSources/Fees_Permits_Insurance.csv |
| **DECOMPOSITION_PATH** | _Decomposition/WDMLRL_Decomposition_Claude.md (R2 -- 2026-03-26, SCA-001) |
| **DEPENDENCY_SOURCES** | AUTO (read from DEL-018-06/Dependencies.csv) |
| **FALLBACK_POLICY** | ALLOW_ALLOWANCE |
| **ALLOW_MIXED_METHODS** | TRUE |
| **UPDATE_LATEST_POINTER** | FALSE |
| **Rounding** | NONE |
| **OUTPUT_LABEL** | DEL-018-06 |

## Refresh Context

This run is an estimate refresh triggered by scope change SCA-001 (Addenda 2, 3, 4). The material changes affecting DEL-018-06 are:

1. **New scope: SOW-0122 -- Electrical pole/transformer relocation** (Add. 3, Q7). The contractor is responsible for relocating electrical pole(s) and transformer(s) as required, coordinating with the local service provider(s). This is new scope not in the prior estimate.

2. **Gas supply parameters now defined** (Add. 3, Q8): 2-inch PVC pipe at 50 PSI constant pressure. This firms up the gas tie-in scope (SOW-0080) and allows more confident sizing of the gas service connection, though the prior estimate already carried a parametric allowance.

## Prior Estimate Reference

- **Prior snapshot:** EST_DEL-018-06_2026-02-27_0930
- **Prior total:** $139,480.20 CAD (23 line items, PARAMETRIC method)
- **Prior basis:** PARAMETRIC
- **Prior RUN_STATUS:** WARNINGS

## CBS Mapping Rule

CBS codes assigned per CBS_Taxonomy.csv (PS-CBS):
- Professional staff -> CBS-02 (Project Management) or CBS-03 (Professional Staff)
- Utility connections -> CBS-24 (Utility Connections)
- Earthwork -> CBS-22 (Earthwork, Surfacing & Landscaping)
- Underground utilities -> CBS-23 (Underground Utilities & Site Services)
- Construction labour -> CBS-05 (General Construction Labour)
- Permits -> CBS-28 (Permits, Fees & Bonding)
- Commissioning -> CBS-25 (Commissioning, Testing & Inspection)
- General conditions -> CBS-29 (General Requirements & Indirect)
- Electrical power distribution -> CBS-17 (Power Distribution & Equipment)

## Warnings

- SOW-0122 (electrical pole/transformer relocation) is priced as an ALLOWANCE ($35,000-$85,000 range, $55,000 recommended) because no quotes from utility providers are available. This is the largest single source of estimate uncertainty.
- Trench distance remains assumed at 75m. Actual distance TBD pending civil design.
- Utility service connection costs remain parametric allowances (no provider quotes).
- Gas supply parameters (2" PVC, 50 PSI) now defined, reducing uncertainty on gas tie-in but not materially changing the cost estimate.
