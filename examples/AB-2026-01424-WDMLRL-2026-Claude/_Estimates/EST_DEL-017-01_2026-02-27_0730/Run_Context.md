# Run Context — EST_DEL-017-01_2026-02-27_0730

| Field | Value |
|-------|-------|
| **RunID** | EST_DEL-017-01_2026-02-27_0730 |
| **AsOf** | 2026-02-27T07:30:00-07:00 |
| **Scope** | DEL-017-01 (Kitchenette Renovation) |
| **ScopeResolvedSummary** | 1 deliverable in 1 package (PKG-017). 4/4 documents present. |
| **BASIS_OF_ESTIMATE** | PARAMETRIC |
| **CURRENCY** | CAD |
| **PRICE_SOURCES** | Professional_Staff_Rates.csv, Level_of_Effort.csv, Assumed_Project_Parameters.csv, Interior_Architectural_Rates.csv, Construction_Labour_Rates.csv |
| **DECOMPOSITION_PATH** | _Decomposition/WDMLRL_Decomposition_Claude.md |
| **FALLBACK_POLICY** | ALLOW_PARAMETRIC |
| **ALLOW_MIXED_METHODS** | TRUE |
| **UPDATE_LATEST_POINTER** | FALSE |
| **Rounding** | NONE |

## Resolved Paths

| Item | Path |
|------|------|
| RUN_ROOT | /Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude |
| ESTIMATES_ROOT | /Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/_Estimates |
| Deliverable Folder | PKG-017_Existing Building Renovation (Old North Shop)/1_Working/DEL-017-01_Kitchenette-Reno |
| Decomposition | _Decomposition/WDMLRL_Decomposition_Claude.md |
| Price Source 1 | _EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Professional_Staff_Rates.csv |
| Price Source 2 | _EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Level_of_Effort.csv |
| Price Source 3 | _EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Assumed_Project_Parameters.csv |
| Price Source 4 | _EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Interior_Architectural_Rates.csv |
| Price Source 5 | _EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Construction_Labour_Rates.csv |

## Warnings

- Kitchenette area is 250 sqft (~23.2 m2) per RFP section 3.4 / SOW-0070. This is the only explicit quantity from source documents; all other physical quantities are design-gated (TBD pending IFC drawings).
- Appliance schedule is TBD pending design phase; appliance and cabinetry procurement responsibility is ambiguous (Datasheet Lensing: E-001).
- Fixture scope, plumbing scope, and electrical scope are TBD pending design completion (PKG-001, PKG-004, PKG-006).
- HVAC/mechanical ventilation scope is conditional on whether cooking appliances are included in the appliance schedule (Specification REQ-012, Guidance Lensing: F-001).
- Fire separation scope is conditional on renovation interaction with fire-rated assemblies (Specification REQ-013).
- Accessibility requirements are TBD pending Owner/Architect determination (Specification REQ-014).
