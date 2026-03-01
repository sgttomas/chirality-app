# Run Context — EST_DEL-015-01_2026-02-26_2232

| Field | Value |
|---|---|
| RunID | EST_DEL-015-01_2026-02-26_2232 |
| AsOf | 2026-02-26T22:32 |
| Scope | DEL-015-01 (Power Service) |
| ScopeResolvedSummary | 1 deliverable in 1 package (PKG-015) |
| BASIS_OF_ESTIMATE | PARAMETRIC |
| CURRENCY | CAD |
| PRICE_SOURCES | Professional_Staff_Rates.csv, Level_of_Effort.csv, Assumed_Project_Parameters.csv, Electrical_System_Rates.csv, Underground_Utility_Rates.csv, Construction_Labour_Rates.csv |
| DECOMPOSITION_PATH | _Decomposition/WDMLRL_Decomposition_Claude.md |
| FALLBACK_POLICY | ALLOW_PARAMETRIC |
| ALLOW_MIXED_METHODS | TRUE |
| UPDATE_LATEST_POINTER | FALSE |
| Rounding | NONE |
| OUTPUT_LABEL | DEL-015-01 |

## Warnings

- Service voltage (208Y/120V vs 480Y/277V) is TBD pending PKG-004 design — affects conductor sizing and material costs.
- Service ampacity/size is TBD pending IFC electrical design drawings — the single most critical sizing parameter.
- Utility provider identity is TBD — affects tie-in costs and lead times.
- Multiple downstream load quantities are approximate (from conceptual drawing only).
- HVAC/mechanical loads, low-voltage system loads, and future expansion loads are TBD.
- Welding equipment specifications not yet received from Owner.
- Several items priced using ALLOWANCE method under ALLOW_PARAMETRIC fallback where parametric data was insufficient.

## Documents Read

| Document | Status |
|---|---|
| _CONTEXT.md | Read |
| Datasheet.md | Read |
| Specification.md | Read |
| Guidance.md | Read |
| Procedure.md | Read |
| Decomposition | Read (DEL-015-01 section) |
