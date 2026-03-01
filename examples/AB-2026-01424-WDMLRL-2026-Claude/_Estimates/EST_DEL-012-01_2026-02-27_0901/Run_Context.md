# Run Context

| Field | Value |
|---|---|
| **RunID** | EST_DEL-012-01_2026-02-27_0901 |
| **AsOf** | 2026-02-27T09:01Z |
| **Scope** | DEL-012-01 |
| **ScopeResolvedSummary** | 1 deliverable (DEL-012-01 Parts Storage Room) in PKG-012 Interior Construction & Fit-Out |
| **BASIS_OF_ESTIMATE** | PARAMETRIC |
| **CURRENCY** | CAD |
| **PRICE_SOURCES** | Professional_Staff_Rates.csv, Level_of_Effort.csv, Assumed_Project_Parameters.csv, Interior_Architectural_Rates.csv, Construction_Labour_Rates.csv |
| **DECOMPOSITION_PATH** | {RUN_ROOT}/_Decomposition/WDMLRL_Decomposition_Claude.md |
| **FALLBACK_POLICY** | ALLOW_PARAMETRIC |
| **ALLOW_MIXED_METHODS** | TRUE |
| **UPDATE_LATEST_POINTER** | FALSE |
| **Rounding** | NONE (default) |
| **OUTPUT_LABEL** | DEL-012-01 |
| **DELIVERABLE_PATH** | {RUN_ROOT}/PKG-012_Interior Construction & Fit-Out/1_Working/DEL-012-01_Parts-Room |

## Resolved Defaults

- RUN_TIMESTAMP generated at runtime: 2026-02-27T09:01Z
- ROUNDING: NONE (default; not specified in brief)
- UPDATE_LATEST_POINTER: FALSE (as specified)
- ALLOW_MIXED_METHODS: TRUE (as specified) -- allows mixing PARAMETRIC with ALLOWANCE fallback methods where pricing sources do not directly support PARAMETRIC derivation
- FALLBACK_POLICY: ALLOW_PARAMETRIC -- permits parametric estimation for items lacking explicit rate table or quote evidence

## Documents Read

| Document | Status |
|---|---|
| _CONTEXT.md | READ |
| Datasheet.md | READ |
| Specification.md | READ |
| Guidance.md | READ |
| Procedure.md | READ |

## Warnings

- W-001: Wall finishes specification TBD -- finish schedule (DEL-001-08) not yet available; parametric rate applied based on assumed industrial finish
- W-002: Floor finishes specification TBD -- finish schedule not yet available; parametric rate for concrete sealer applied
- W-003: Ceiling treatment TBD -- assumed exposed structure (no ceiling finish cost allocated)
- W-004: Shelving type and capacity TBD in design -- parametric estimate based on industrial metal racking assumption
- W-005: Roll-up door motorized vs. manual TBD -- estimated as motorized insulated unit per Guidance recommendation
- W-006: Security hardware specification TBD -- included as nominal allowance within roll-up door pricing
- W-007: Electrical scope (lighting, receptacles, door circuit) EXCLUDED per scope boundary (PKG-015)
- W-008: HVAC scope EXCLUDED per scope boundary (PKG-013)
