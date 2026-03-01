# Run Context — EST_DEL-011-04_2026-02-27_0949

| Field | Value |
|---|---|
| **RunID** | EST_DEL-011-04_2026-02-27_0949 |
| **AsOf** | 2026-02-27T09:49:00Z |
| **Scope** | DEL-011-04 |
| **ScopeResolvedSummary** | 1 deliverable (DEL-011-04 Entrance/Exit Doors) in PKG-011 Building Structure & Envelope |
| **BASIS_OF_ESTIMATE** | PARAMETRIC |
| **CURRENCY** | CAD |
| **PRICE_SOURCES** | Professional_Staff_Rates.csv, Level_of_Effort.csv, Assumed_Project_Parameters.csv, Structural_Concrete_Rates.csv, Building_Envelope_Rates.csv, Construction_Labour_Rates.csv, Equipment_Pricing.csv |
| **DECOMPOSITION_PATH** | _Decomposition/WDMLRL_Decomposition_Claude.md |
| **FALLBACK_POLICY** | ALLOW_PARAMETRIC |
| **ALLOW_MIXED_METHODS** | TRUE |
| **UPDATE_LATEST_POINTER** | FALSE |
| **Rounding** | NONE (default) |
| **OUTPUT_LABEL** | DEL-011-04 |

## Resolved Defaults

- `RUN_TIMESTAMP`: 2026-02-27T09:49:00Z (generated at runtime)
- `ROUNDING`: NONE (default — not provided in brief)
- Snapshot folder: `_Estimates/EST_DEL-011-04_2026-02-27_0949/`
- No pointer file updated (UPDATE_LATEST_POINTER = FALSE)

## Warnings

- **W-001:** Door quantity is TBD in the Datasheet. Assumed 3 EA pedestrian man-doors based on parametric reasoning for a ~13,000 sqft industrial maintenance shop (minimum: 1 accessible main entrance + 2 secondary egress/access doors). This is an assumption — see Assumptions_Log.md ASM-001.
- **W-002:** Door leaf material, dimensions, hardware specification, fire rating, glazing, and insulation values are all TBD pending IFC Architectural documents (DEL-001-07, DEL-001-11). Pricing uses parametric rates from Building_Envelope_Rates.csv for insulated steel man-doors.
- **W-003:** No explicit door hardware schedule exists in available sources. Hardware allowance is estimated parametrically.

## Documents Read

| Document | Status |
|---|---|
| _CONTEXT.md | Read |
| Datasheet.md | Read |
| Specification.md | Read |
| Guidance.md | Read |
| Procedure.md | Read |
| WDMLRL_Decomposition_Claude.md | Read (DEL-011-04 / SOW-0026 / PKG-011 sections) |
