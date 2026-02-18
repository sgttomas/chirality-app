# Decision Log — EST_DEL-02-01_2026-02-18_1400

| DecisionID | Decision | Rationale |
|---|---|---|
| DEC-EST-001 | CBS codes assigned by role category (DESIGN-ARCH, PRODUCTION-CAD, DESIGN-CIVIL, etc.) rather than by activity type | Deterministic mapping from Professional_Staff_Rates.csv Category field; documented in Run_Context.md CBS Mapping Rule table |
| DEC-EST-002 | All 12 Level_of_Effort.csv rows for DEL-02-01 used as-is; no adjustments to hours | LOE source is a parametric estimate for execution-6c; no basis to override without operator instruction |
| DEC-EST-003 | Optional 3D rendering (16-24h R-06) excluded from estimate | BOE context states this is optional; STRICT fallback policy requires explicit inclusion to price; no operator instruction to include |
| DEC-EST-004 | Rounding applied at DOLLAR level to all Amount fields | Per brief ROUNDING=DOLLAR; all Amount values are whole-dollar (no rounding adjustment needed since all products of integer hours x integer rates produce whole dollars) |
| DEC-EST-005 | Upstream document PENDING statuses treated as informational only (no estimate blockers) | Rate-table pricing (hours x rates) is independent of document availability; hours represent planned effort regardless of prerequisite status |
| DEC-EST-006 | DEPENDENCY_SOURCES resolved via AUTO to DEL-02-01/Dependencies.csv (16 rows) | Per protocol Step 3; file found at expected path |
| DEC-EST-007 | Assumed_Project_Parameters.csv loaded for context validation only; no direct pricing derived | Parameters inform scope context (building areas, site size) but DEL-02-01 pricing is purely hours x rates from LOE + Staff Rates |
