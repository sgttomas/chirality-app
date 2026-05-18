# Decision Log — EST_DEL-01-02_2026-02-18_2100

## Decisions Carried Forward from Prior Run

### DEC-EST-001 — LOE Quantities Treated as Rate-Table Input
Carried forward unchanged. See EST_DEL-01-02_2026-02-18_0900 Decision_Log.md.

### DEC-EST-002 — CBS Mapping Rule Applied
Carried forward unchanged. CBS = MGMT.PROJ_CONTROLS.

### DEC-EST-004 — Rounding Applied to DOLLAR
Carried forward unchanged.

## New Decisions in This Run

### DEC-EST-005 — Software/Tools TBD Resolved as Parametric Allowance

| Field | Value |
|---|---|
| Decision | L-003 (scheduling software/tools) resolved from TBD to $3,500 CAD as a parametric allowance. |
| Rationale | The human authorized ORCHESTRATOR to resolve TBD lines using best-guess parametric allowances. Scheduling software (Primavera P6 or MS Project) typically costs $2,000-5,000 for an 18-month project license. $3,500 is the midpoint estimate. |
| Method | ALLOWANCE (no rate table evidence exists; parametric estimate only) |
| Confidence | LOW |
| Prior Decision Superseded | DEC-EST-003 (which set L-003 to TBD under STRICT fallback) |
| Affected Lines | L-003 |

### DEC-EST-006 — Mixed Methods Authorized for TBD Resolution

| Field | Value |
|---|---|
| Decision | ALLOW_MIXED_METHODS changed from FALSE to TRUE for this revision. L-001/L-002 remain RATE_TABLE; L-003 is ALLOWANCE. |
| Rationale | Human authorized ORCHESTRATOR to resolve TBDs, which requires introducing ALLOWANCE method for items without rate table evidence. This is a controlled departure from the original STRICT/no-mixed-methods configuration. |
| Affected Lines | L-003 |
