# Run Context — EST_DEL-014-03_2026-02-27_0901

| Field | Value |
|---|---|
| **RunID** | EST_DEL-014-03_2026-02-27_0901 |
| **AsOf** | 2026-02-27T09:01Z |
| **Scope** | DEL-014-03 |
| **ScopeResolvedSummary** | 1 deliverable (DEL-014-03 Bulk Water Fill System) in 1 package (PKG-014 Plumbing & Water Systems Installation) |
| **BASIS_OF_ESTIMATE** | PARAMETRIC |
| **CURRENCY** | CAD |
| **PRICE_SOURCES** | Professional_Staff_Rates.csv, Level_of_Effort.csv, Assumed_Project_Parameters.csv, Underground_Utility_Rates.csv, Construction_Labour_Rates.csv, Equipment_Pricing.csv |
| **DECOMPOSITION_PATH** | {RUN_ROOT}/_Decomposition/WDMLRL_Decomposition_Claude.md |
| **FALLBACK_POLICY** | ALLOW_PARAMETRIC |
| **ALLOW_MIXED_METHODS** | TRUE |
| **UPDATE_LATEST_POINTER** | FALSE |
| **Rounding** | NONE (default) |
| **OUTPUT_LABEL** | DEL-014-03 |
| **DELIVERABLE_PATH** | {RUN_ROOT}/PKG-014_Plumbing & Water Systems Installation/1_Working/DEL-014-03_Bulk-Water |

## Resolved Paths

- Tool Root: `{RUN_ROOT}/_Estimates/`
- Snapshot: `{RUN_ROOT}/_Estimates/EST_DEL-014-03_2026-02-27_0901/`
- Deliverable Documents: All four documents present (Datasheet.md, Specification.md, Guidance.md, Procedure.md)
- _CONTEXT.md: Present and read

## Warnings

- Multiple critical design parameters (pump flow rate, fill connection size, freeze protection method, backflow device type, pipe material) remain TBD pending plumbing engineering IFC design (PKG-006). These TBDs limit the precision of material quantity takeoffs; parametric estimation is used as fallback per FALLBACK_POLICY.
- Pump equipment cost is estimated parametrically. No vendor quote available.
- No Mechanical_System_Rates.csv entry directly corresponds to a bulk water fill pump; parametric derivation used.
