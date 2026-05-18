# Run_Context — EST_DEL-014-05_2026-02-27_0202

## Run Identification

| Field | Value |
|---|---|
| RunID | EST_DEL-014-05_2026-02-27_0202 |
| AsOf | 2026-02-27T02:02:00-07:00 |
| Scope | DEL-014-05 |
| ScopeResolvedSummary | 1 deliverable (DEL-014-05 Emergency Shower) in PKG-014 (Plumbing & Water Systems Installation) |
| BASIS_OF_ESTIMATE | PARAMETRIC |
| CURRENCY | CAD |
| PRICE_SOURCES | Professional_Staff_Rates.csv, Level_of_Effort.csv, Assumed_Project_Parameters.csv, Underground_Utility_Rates.csv, Construction_Labour_Rates.csv, Equipment_Pricing.csv |
| DECOMPOSITION_PATH | {RUN_ROOT}/_Decomposition/WDMLRL_Decomposition_Claude.md |
| FALLBACK_POLICY | ALLOW_PARAMETRIC |
| ALLOW_MIXED_METHODS | TRUE |
| UPDATE_LATEST_POINTER | FALSE |
| OUTPUT_LABEL | DEL-014-05 |
| Rounding | NONE (default) |
| RUN_TIMESTAMP | 2026-02-27T02:02:00-07:00 |

## Resolved Defaults

- ROUNDING: NONE (default; not specified in brief)
- UPDATE_LATEST_POINTER: FALSE (explicit in brief)
- FALLBACK_POLICY: ALLOW_PARAMETRIC (explicit in brief)
- ALLOW_MIXED_METHODS: TRUE (explicit in brief)

## Documents Read

| Document | Status |
|---|---|
| _CONTEXT.md | Read |
| Datasheet.md | Read |
| Specification.md | Read |
| Guidance.md | Read |
| Procedure.md | Read |

## Warnings

- W-001: No emergency shower equipment pricing exists in PRICE_SOURCES. Equipment material costs priced via PARAMETRIC fallback (ALLOW_PARAMETRIC policy).
- W-002: Supply branch piping length is TBD in Datasheet (pipe size, pipe material not specified). Piping quantity and unit rate estimated parametrically.
- W-003: Multiple Datasheet attributes remain TBD pending IFC design (flow rate, water supply pressure, pipe material, pipe size, finish/material, activation mechanism, signage type, accessibility clearance, electrical interface).
- W-004: Thermostatic mixing valve may or may not be required (CF-001 unresolved). Included in estimate as ASSUMPTION.
