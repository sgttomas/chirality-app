# Run_Context — EST_DEL-014-06_2026-02-27_0201

## Run Identification

| Field | Value |
|---|---|
| **RunID** | EST_DEL-014-06_2026-02-27_0201 |
| **AsOf** | 2026-02-27T09:01:52Z |
| **Scope** | DEL-014-06 |
| **ScopeResolvedSummary** | 1 deliverable (DEL-014-06 Plumbing Fixtures), 1 package (PKG-014) |
| **BASIS_OF_ESTIMATE** | PARAMETRIC |
| **CURRENCY** | CAD |
| **FALLBACK_POLICY** | ALLOW_PARAMETRIC |
| **ALLOW_MIXED_METHODS** | TRUE |
| **UPDATE_LATEST_POINTER** | FALSE |
| **Rounding** | NONE (default) |
| **OUTPUT_LABEL** | DEL-014-06 |

## PRICE_SOURCES (resolved)

| PS-ID | File | Notes |
|---|---|---|
| PS-STAFF | Professional_Staff_Rates.csv | Staff hourly rates (25 roles) |
| PS-LOE | Level_of_Effort.csv | DEL-014-06 rows: 6 role-hour entries |
| PS-PARAMS | Assumed_Project_Parameters.csv | Project parameters (18 rows) |
| PS-UU | Underground_Utility_Rates.csv | Underground utility rates (5 rows) |
| PS-LAB | Construction_Labour_Rates.csv | Trade labour rates (10 trades) |
| PS-EQ | Equipment_Pricing.csv | Major equipment allowances (3 items) |

## DECOMPOSITION_PATH

`{RUN_ROOT}/_Decomposition/WDMLRL_Decomposition_Claude.md`

DEL-014-06 maps to PKG-014 (Plumbing & Water Systems Installation), SOW-0049 and SOW-0050.

## DELIVERABLE_PATH

`{RUN_ROOT}/PKG-014_Plumbing & Water Systems Installation/1_Working/DEL-014-06_Fixtures`

## Documents Read

| Document | Status |
|---|---|
| _CONTEXT.md | Read |
| Datasheet.md | Read |
| Specification.md | Read |
| Guidance.md | Read |
| Procedure.md | Read |

## Warnings

- [WARNING] Many fixture attributes are TBD pending DEL-006-06 (Plumbing Fixture Schedule) which has not been produced yet.
- [WARNING] Hot water supply for industrial wash station is unresolved (CONF-014-06-01); point-of-use water heater carried as conditional allowance.
- [WARNING] Pressure washer unit ownership unclear (CONF-014-06-02); reel and water connection in scope, pressure washer machine TBD.
- [WARNING] No direct fixture material pricing in PRICE_SOURCES; parametric estimates used per FALLBACK_POLICY=ALLOW_PARAMETRIC.
