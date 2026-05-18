# Decision Log — EST_DEL-01-02_2026-02-18_0900

## Decisions Made During This Run

### DEC-EST-001 — LOE Quantities Treated as Rate-Table Input

| Field | Value |
|---|---|
| Decision | The `Level_of_Effort.csv` source declares its hour quantities with `Basis=PARAMETRIC`. However, these quantities are used as **input quantities** to a rate-table pricing calculation (Qty x UnitRate from `Professional_Staff_Rates.csv`). The resulting line items are assigned `Method=RATE_TABLE`, consistent with `BASIS_OF_ESTIMATE=RATE_TABLE`. |
| Rationale | The rate-table method is defined by how pricing is derived (unit rate x quantity), not by how quantities were originally estimated. The LOE quantities are substantiated by a provided source file, and the rates come from an explicit rate table. This satisfies the RATE_TABLE basis. |
| Affected Lines | L-001, L-002 |
| ALLOW_MIXED_METHODS Impact | No mixed methods required; all lines are RATE_TABLE. |

### DEC-EST-002 — CBS Mapping Rule Applied

| Field | Value |
|---|---|
| Decision | No explicit CBSHint was provided in the decomposition for DEL-01-02. A deterministic CBS code `MGMT.PROJ_CONTROLS` was assigned based on the deliverable's substance (Management) and discipline (Project controls). |
| Rationale | The brief identifies the deliverable substance as "Management" and the Datasheet identifies the discipline as "Project controls". This mapping is documented in Run_Context.md for reproducibility. |
| Affected Lines | L-001, L-002, L-003 |

### DEC-EST-003 — Software/Tools Line Set to TBD (STRICT Fallback)

| Field | Value |
|---|---|
| Decision | The brief identifies "software/tools" as a cost driver for DEL-01-02. No pricing source (rate table entry, quote, or allowance) was provided for this item. Under `FALLBACK_POLICY=STRICT`, the line is included with `Amount=TBD` and flagged in QA. |
| Rationale | STRICT fallback requires that no price be assigned without basis evidence. Including the line as TBD preserves visibility of the cost driver while avoiding invention. |
| Affected Lines | L-003 |

### DEC-EST-004 — Rounding Applied to DOLLAR

| Field | Value |
|---|---|
| Decision | Per the brief, `ROUNDING=DOLLAR`. All computed amounts are rounded to the nearest whole dollar. |
| Impact | L-001: 80 x 130 = $10,400 (no rounding effect). L-002: 20 x 175 = $3,500 (no rounding effect). Both amounts are already whole dollars. |

## Defaults Applied

| Parameter | Default Used | Source |
|---|---|---|
| FALLBACK_POLICY | STRICT | Brief (explicit) |
| ALLOW_MIXED_METHODS | FALSE | Brief (explicit) |
| UPDATE_LATEST_POINTER | FALSE | Brief (explicit) |
| ROUNDING | DOLLAR | Brief (explicit) |
| DEPENDENCY_SOURCES | AUTO | Brief (explicit); resolved to DEL-01-02/Dependencies.csv |
