# Source Index — EST_DEL-002-08_2026-02-27_0630

## Price Sources Indexed

| # | Source File | Source Type | Items Supported | Parsing Notes |
|---|---|---|---|---|
| 1 | `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Professional_Staff_Rates.csv` | PARAMETRIC (rate table) | ITM-001 through ITM-004 (unit rates by role) | 25 roles; CSV with columns RoleID, Role, Category, HourlyRate_CAD, Basis, Confidence, Notes. All rates marked PARAMETRIC / MEDIUM confidence. |
| 2 | `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Level_of_Effort.csv` | PARAMETRIC (hours model) | ITM-001 through ITM-004 (hours per role per deliverable) | Large CSV covering all deliverables; filtered to rows where DeliverableID = DEL-002-08. Provides EstimatedHours for 4 roles: R-01 (6 hr), R-08 (4 hr), R-13 (36 hr), R-14 (84 hr). All marked PARAMETRIC basis. |
| 3 | `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Assumed_Project_Parameters.csv` | PARAMETRIC (parameters) | Context validation only — no direct pricing | 19 parameters including building area (~13,000 sqft), crane count (2 x 5 ton), currency (CAD). Used to validate scope context; not used for direct line-item pricing. |
| 4 | `_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/Professional_Design_Fees.csv` | PARAMETRIC (fee model) | Not used for this deliverable | Provides percentage-based design fees (e.g., Structural = 1.8% of construction value). Not applied because LOE-based pricing (Sources 1+2) provides more granular, deliverable-specific pricing for DEL-002-08. Fee-based pricing would be an alternative method if LOE data were unavailable. |

## Engineering Documents Read (Quantity Takeoff Sources)

| Document | Path | Items Extracted |
|---|---|---|
| _CONTEXT.md | `PKG-002_Structural Design/1_Working/DEL-002-08_Embedment-Plan/_CONTEXT.md` | Deliverable identity, package, discipline, type |
| Datasheet.md | `PKG-002_Structural Design/1_Working/DEL-002-08_Embedment-Plan/Datasheet.md` | 6 steel plate zones (SP-01 to SP-06); building floor context; material TBDs; embedment method TBD |
| Specification.md | `PKG-002_Structural Design/1_Working/DEL-002-08_Embedment-Plan/Specification.md` | 11 requirements (REQ-001 through REQ-010 plus REQ-008A); verification matrix; standards table |
| Guidance.md | `PKG-002_Structural Design/1_Working/DEL-002-08_Embedment-Plan/Guidance.md` | 5 principles (P-01 to P-05); 7 considerations (C-01 to C-07); 2 trade-offs (T-01, T-02) |
| Procedure.md | `PKG-002_Structural Design/1_Working/DEL-002-08_Embedment-Plan/Procedure.md` | 8-step procedure with prerequisites; work activities mapped to roles |

## What Sources Cannot Support

- **Physical material costs:** No steel plate material pricing (plate steel per kg or per m2) is available. This deliverable is a design drawing set, not a procurement/construction deliverable, so material costs are not in scope for pricing.
- **Peer review hours:** Level_of_Effort.csv does not include hours for independent peer review (ITM-006). Amount is TBD.
- **Printing/reproduction costs:** Not addressed in any price source.
