# Run Context — EST_DEL-011-07_2026-02-27_0955

| Field | Value |
|---|---|
| **RunID** | EST_DEL-011-07_2026-02-27_0955 |
| **AsOf** | 2026-02-27T09:55:00Z |
| **Scope** | DEL-011-07 |
| **ScopeResolvedSummary** | 1 deliverable (DEL-011-07 Mezzanine Structure & Stairs) in PKG-011 Building Structure & Envelope |
| **BASIS_OF_ESTIMATE** | PARAMETRIC |
| **CURRENCY** | CAD |
| **PRICE_SOURCES** | Professional_Staff_Rates.csv, Level_of_Effort.csv, Assumed_Project_Parameters.csv, Structural_Concrete_Rates.csv, Building_Envelope_Rates.csv, Construction_Labour_Rates.csv, Equipment_Pricing.csv |
| **DECOMPOSITION_PATH** | _Decomposition/WDMLRL_Decomposition_Claude.md |
| **FALLBACK_POLICY** | ALLOW_PARAMETRIC |
| **ALLOW_MIXED_METHODS** | TRUE |
| **UPDATE_LATEST_POINTER** | FALSE |
| **Rounding** | NONE (default) |
| **OUTPUT_LABEL** | DEL-011-07 |

## Warnings

- Mezzanine floor area is TBD per Datasheet; estimate uses parametric assumption of 93 m2 (approx. 1,000 sq ft) based on App B floor plan layout (parts room ~400 sq ft + utility room + partial wash bay span).
- Structural system assumed steel-framed per Guidance Trade-offs (TBD per Structural Engineer of Record).
- Floor deck type assumed composite steel deck with concrete topping per Guidance Trade-offs (TBD per Structural Engineer of Record).
- Design live load TBD; Guidance references 4.8-7.2 kPa industrial range. This does not affect structural steel pricing directly (parametric per m2) but may affect member sizing and thus $/m2 rates.
- Stair width TBD per Alberta Safety Codes / Structural Engineer.
- Mezzanine extent over wash bay is unresolved (CFT-011-07-01); floor area assumption may change.
- Scope boundary with PKG-012 for wearing surface is unresolved (CFT-011-07-02); estimate includes structural deck only.
