# Decision Log -- EST_DEL-01-06_2026-02-18_1030

## Defaults Applied

| DecisionID | Decision | Rationale |
|---|---|---|
| DEC-EST-001 | CBS codes assigned using deterministic rule: PKG-001 construction management labor -> `01-CMGT`; PKG-001 non-labor site costs -> `01-SITE`. | No explicit CBSHint found in decomposition for DEL-01-06. Rule documented in Run_Context.md. |
| DEC-EST-002 | Level_of_Effort.csv used as the quantity source for labor hours, combined with Professional_Staff_Rates.csv for unit rates. | Level_of_Effort.csv provides deliverable-specific hour estimates per role. Professional_Staff_Rates.csv provides the hourly rates. Together they form a complete rate table pricing chain. |
| DEC-EST-003 | Hours basis noted as PARAMETRIC in Level_of_Effort.csv is accepted as-is. | The Level_of_Effort.csv is an explicit PRICE_SOURCE provided by the invoker. The PARAMETRIC basis notation within the source describes how the hours were derived; it does not make the Method of this estimate PARAMETRIC. The Method remains RATE_TABLE because we are applying rate table unit rates to those quantities. |

## Scope Resolution Decisions

| DecisionID | Decision | Rationale |
|---|---|---|
| DEC-EST-004 | DEL-01-06 resolved as the sole in-scope deliverable. SCOPE=DEL-01-06 maps directly to a single deliverable in the decomposition. | No expansion or exclusion logic needed. |

## Fallback Decisions

| DecisionID | Decision | Rationale |
|---|---|---|
| DEC-EST-005 | Non-labor line items (L-0106-003, L-0106-004) set to TBD rather than priced via allowance or parametric method. | FALLBACK_POLICY=STRICT and ALLOW_MIXED_METHODS=FALSE. No rate table evidence exists for temporary facilities, fencing, or cleaning costs. Cannot price without evidence. |

## Cost Ownership Decisions

| DecisionID | Decision | Rationale |
|---|---|---|
| DEC-EST-006 | All costs in this estimate are carried under PKG-001 per brief cost ownership rules. | Brief states: "All project-level management and coordination costs are carried in PKG-001." Site supervision and logistics are project-level management functions. |
