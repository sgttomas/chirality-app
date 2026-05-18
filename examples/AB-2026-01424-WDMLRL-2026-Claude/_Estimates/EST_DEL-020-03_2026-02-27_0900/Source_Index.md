# Source Index — EST_DEL-020-03_2026-02-27_0900

## Pricing Sources

| # | Source File | Source Type | Parsing Notes | Supports | Limitations |
|---|---|---|---|---|---|
| 1 | `Professional_Staff_Rates.csv` | PARAMETRIC (rate table) | CSV; 25 roles with RoleID, HourlyRate_CAD, Confidence=MEDIUM | Hourly rates for all professional/admin roles in scope | Rates are PARAMETRIC estimates (not firm quotes); MEDIUM confidence |
| 2 | `Level_of_Effort.csv` | PARAMETRIC (effort model) | CSV; filtered for DEL-020-03 rows — 8 role allocations found | Hour estimates for each role assigned to DEL-020-03 Closeout Documentation | Hours are PARAMETRIC estimates; PKG-020 notes show "TBD" for sub-category |
| 3 | `Assumed_Project_Parameters.csv` | PARAMETRIC (parameters) | CSV; 19 project parameters | Context parameters (project identity, facility attributes, currency=CAD) | No direct pricing data; used for context validation |
| 4 | `Optional_Items_Pricing.csv` | ALLOWANCE | CSV; 2 optional items (winter conditions, contaminated soils) | Allowance pricing for optional scope items | Not applicable to DEL-020-03 closeout documentation scope |

## Document Sources (Quantity Takeoff Basis)

| # | Document | Path | Used For |
|---|---|---|---|
| 1 | _CONTEXT.md | `PKG-020_Commissioning & Closeout/1_Working/DEL-020-03_Closeout-Docs/_CONTEXT.md` | Deliverable identification, scope definition, success criteria |
| 2 | Datasheet.md | `PKG-020_Commissioning & Closeout/1_Working/DEL-020-03_Closeout-Docs/Datasheet.md` | Attributes, document categories, conditions, prerequisites |
| 3 | Specification.md | `PKG-020_Commissioning & Closeout/1_Working/DEL-020-03_Closeout-Docs/Specification.md` | Requirements REQ-001 through REQ-009, verification criteria, standards |
| 4 | Guidance.md | `PKG-020_Commissioning & Closeout/1_Working/DEL-020-03_Closeout-Docs/Guidance.md` | Principles, trade-offs, conflict table, rationale |
| 5 | Procedure.md | `PKG-020_Commissioning & Closeout/1_Working/DEL-020-03_Closeout-Docs/Procedure.md` | Work steps (Steps 1-9), prerequisites, verification, records |
| 6 | WDMLRL_Decomposition_Claude.md | `_Decomposition/WDMLRL_Decomposition_Claude.md` | WBS traceability (PKG-020, DEL-020-03), SOW mapping (SOW-0094-0096), objective links |
