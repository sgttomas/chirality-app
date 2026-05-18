# Run Context — EST_DEL-013-06_2026-02-27_0201

| Field | Value |
|---|---|
| **RunID** | EST_DEL-013-06_2026-02-27_0201 |
| **AsOf** | 2026-02-27T02:01 (local) |
| **Scope** | DEL-013-06 |
| **ScopeResolvedSummary** | 1 deliverable (DEL-013-06: Ceiling Fans), 1 package (PKG-013: Mechanical & HVAC Installation) |
| **BASIS_OF_ESTIMATE** | PARAMETRIC |
| **CURRENCY** | CAD |
| **PRICE_SOURCES** | Professional_Staff_Rates.csv, Level_of_Effort.csv, Assumed_Project_Parameters.csv, Mechanical_System_Rates.csv, Construction_Labour_Rates.csv, Equipment_Pricing.csv |
| **DECOMPOSITION_PATH** | {RUN_ROOT}/_Decomposition/WDMLRL_Decomposition_Claude.md |
| **DELIVERABLE_PATH** | {RUN_ROOT}/PKG-013_Mechanical & HVAC Installation/1_Working/DEL-013-06_Ceiling-Fans |
| **FALLBACK_POLICY** | ALLOW_PARAMETRIC |
| **ALLOW_MIXED_METHODS** | TRUE |
| **UPDATE_LATEST_POINTER** | FALSE |
| **Rounding** | NONE (default) |
| **OUTPUT_LABEL** | DEL-013-06 |

## Warnings

- W-01: No explicit ceiling fan unit pricing found in any PRICE_SOURCES file. Mechanical_System_Rates.csv and Equipment_Pricing.csv contain no ceiling fan line items. Parametric estimate derived from industry knowledge and available labour/staff rates.
- W-02: Fan model, diameter, motor power, and voltage are all TBD in the Datasheet. Equipment pricing is parametric based on HVLS industrial fan class assumption.
- W-03: Ceiling structure type (concrete vs. steel purlin/beam) is unresolved (Conflict CF-013-06-03), which affects mounting hardware cost.
- W-04: Control type (individual wall switches vs. centralized panel) is TBD, affecting control system cost.
- W-05: Multiple specification requirements have TBD acceptance criteria (noise dBA, vibration threshold, air circulation criterion, clearance values).
