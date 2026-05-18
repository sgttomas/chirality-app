# Run Context — EST_DEL-011-06_2026-02-27_0600

| Field | Value |
|---|---|
| **RunID** | EST_DEL-011-06_2026-02-27_0600 |
| **AsOf** | 2026-02-27T06:00:00-07:00 |
| **Scope** | DEL-011-06 |
| **ScopeResolvedSummary** | 1 deliverable (DEL-011-06 Service Pit/Trench) within PKG-011 Building Structure & Envelope |
| **BASIS_OF_ESTIMATE** | PARAMETRIC |
| **CURRENCY** | CAD |
| **PRICE_SOURCES** | Professional_Staff_Rates.csv, Level_of_Effort.csv, Assumed_Project_Parameters.csv, Structural_Concrete_Rates.csv, Building_Envelope_Rates.csv, Construction_Labour_Rates.csv, Equipment_Pricing.csv |
| **DECOMPOSITION_PATH** | _Decomposition/WDMLRL_Decomposition_Claude.md |
| **FALLBACK_POLICY** | ALLOW_PARAMETRIC |
| **ALLOW_MIXED_METHODS** | TRUE |
| **UPDATE_LATEST_POINTER** | FALSE |
| **Rounding** | NONE (default) |
| **OUTPUT_LABEL** | DEL-011-06 |

## Resolved Price Source Paths

1. `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Professional_Staff_Rates.csv`
2. `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Level_of_Effort.csv`
3. `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Assumed_Project_Parameters.csv`
4. `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Structural_Concrete_Rates.csv`
5. `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Building_Envelope_Rates.csv`
6. `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Construction_Labour_Rates.csv`
7. `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Equipment_Pricing.csv`

## Documents Read

| Document | Status |
|---|---|
| DEL-011-06 _CONTEXT.md | Read |
| DEL-011-06 Datasheet.md | Read |
| DEL-011-06 Specification.md | Read |
| DEL-011-06 Guidance.md | Read |
| DEL-011-06 Procedure.md | Read |
| WDMLRL_Decomposition_Claude.md | Read (DEL-011-06 sections) |

## Warnings

- Pit plan dimensions (depth, width, length) are TBD pending IFC structural drawings (DEL-002-06) and Owner equipment fleet data. Quantities for excavation, concrete, formwork, rebar, waterproofing, and lining are derived from ASSUMPTIONS based on typical heavy-equipment maintenance pit geometry.
- Several scope items have unresolved design decisions (cover type, ventilation method, access/egress method, drainage scope boundary) per Guidance Conflict Table.
- No IFC drawings available; all structural quantities are parametric estimates.
