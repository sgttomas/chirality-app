# Run Context — EST_DEL-018-06_2026-02-27_0930

## Run Identity

| Field | Value |
|-------|-------|
| **RunID** | EST_DEL-018-06_2026-02-27_0930 |
| **AsOf** | 2026-02-27T09:30:00-07:00 |
| **Scope** | DEL-018-06 |
| **ScopeResolvedSummary** | 1 deliverable (DEL-018-06 Utility Tie-Ins) in PKG-018 (Sitework & Civil Construction) |
| **BASIS_OF_ESTIMATE** | PARAMETRIC |
| **CURRENCY** | CAD |
| **PRICE_SOURCES** | Professional_Staff_Rates.csv, Level_of_Effort.csv, Assumed_Project_Parameters.csv, Earthwork_Civil_Rates.csv, Paving_Surfacing_Rates.csv, Underground_Utility_Rates.csv, Construction_Labour_Rates.csv |
| **DECOMPOSITION_PATH** | _Decomposition/WDMLRL_Decomposition_Claude.md |
| **FALLBACK_POLICY** | ALLOW_PARAMETRIC |
| **ALLOW_MIXED_METHODS** | TRUE |
| **UPDATE_LATEST_POINTER** | FALSE |
| **Rounding** | NONE (default) |
| **OUTPUT_LABEL** | DEL-018-06 |

## Scope Resolution

- **Deliverable**: DEL-018-06 — Utility Tie-Ins
- **Package**: PKG-018 — Sitework & Civil Construction
- **Responsible Party**: General Contractor
- **Type**: Construction
- **SOW References**: SOW-0080 (Natural Gas Tie-In), SOW-0081 (Electrical Service Tie-In), SOW-0082 (Communication Lines Tie-In)
- **Objective Alignment**: OBJ-001, OBJ-005

## Documents Read

| Document | Status |
|----------|--------|
| _CONTEXT.md | Read |
| Datasheet.md | Read |
| Specification.md | Read |
| Guidance.md | Read |
| Procedure.md | Read |

## Warnings

- W-001: Multiple TBD quantities in source documents (trench distances, burial depths, service sizes). Parametric estimates used where possible; remaining items marked TBD.
- W-002: Gas main extension distance unknown — could materially impact cost (see Guidance Gas Service Extension Risk Assessment).
- W-003: Transformer ownership (utility vs. customer) unresolved — could add $30,000-$80,000 if customer-owned.
- W-004: Level_of_Effort.csv provides professional staff hours for DEL-018-06; these are supervision/management hours only and do not include trade labour or materials.
