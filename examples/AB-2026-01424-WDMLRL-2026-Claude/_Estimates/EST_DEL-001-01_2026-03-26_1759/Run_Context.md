# Run Context — EST_DEL-001-01_2026-03-26_1759

| Field | Value |
|-------|-------|
| **RunID** | EST_DEL-001-01_2026-03-26_1759 |
| **AsOf** | 2026-03-26T17:59:00-06:00 |
| **Scope** | DEL-001-01 (Preliminary Architectural Design) |
| **ScopeResolvedSummary** | 1 deliverable in scope, 0 excluded, 0 blocked |
| **BASIS_OF_ESTIMATE** | RATE_TABLE |
| **CURRENCY** | CAD |
| **PRICE_SOURCES** | PriceSources/Professional_Staff_Rates.csv, PriceSources/Level_of_Effort.csv, PriceSources/Assumed_Project_Parameters.csv, PriceSources/Professional_Design_Fees.csv, PriceSources/Parametric_Building_Rates.csv, PriceSources/Fees_Permits_Insurance.csv |
| **DECOMPOSITION_PATH** | _Decomposition/WDMLRL_Decomposition_Claude.md (R2 -- 2026-03-26, SCA-001) |
| **DEPENDENCY_SOURCES** | AUTO (read from DEL-001-01/Dependencies.csv) |
| **FALLBACK_POLICY** | ALLOW_ALLOWANCE |
| **ALLOW_MIXED_METHODS** | TRUE |
| **UPDATE_LATEST_POINTER** | FALSE |
| **Rounding** | NONE |
| **OUTPUT_LABEL** | DEL-001-01 |

## Refresh Context

This run is an estimate refresh triggered by scope change SCA-001 (Addenda 2, 3, 4). The material change affecting DEL-001-01 is:

- **Interior wall material changed to precast concrete** (Add. 4, Q5). Previously assumed metal stud partitions; now interior walls must be precast concrete panels.

This impacts the preliminary architectural design effort because:
1. Precast concrete interior walls require coordination with the precast supplier on panel dimensions, openings, and embed details at the preliminary design stage.
2. The architect must account for thicker wall assemblies, different connection details, and structural interface coordination with the structural engineer (DEL-002-01).
3. Additional Senior Architect hours are warranted for precast coordination (+4 hrs) and BIM Technician hours for modeling precast wall assemblies (+3 hrs).

## Prior Estimate Reference

- **Prior snapshot:** EST_DEL-001-01_2026-02-27_0539
- **Prior total:** $10,365 CAD (5 line items, PARAMETRIC method, 70 total hours)
- **Prior basis:** PARAMETRIC (LOE x staff rates)

## CBS Mapping Rule

CBS codes assigned per CBS_Taxonomy.csv (PS-CBS):
- Professional staff management roles -> CBS-02 (Project Management)
- Professional staff design roles -> CBS-01 (Design & Engineering)

## Warnings

- LOE model hours from Level_of_Effort.csv have not been updated to reflect the precast interior wall scope change. The agent has applied a manual adjustment of +4 hrs Senior Architect and +3 hrs BIM Technician based on the nature of the scope change. This adjustment is documented in Decision_Log.md.
- BASIS_OF_ESTIMATE is RATE_TABLE; price sources provide staff hourly rates which serve as the rate table. The LOE model provides quantities (hours). Method is recorded as RATE_TABLE per the brief, consistent with ALLOW_MIXED_METHODS=TRUE.
