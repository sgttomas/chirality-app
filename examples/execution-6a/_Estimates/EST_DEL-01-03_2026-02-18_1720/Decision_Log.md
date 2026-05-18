# Decision Log -- EST_DEL-01-03_2026-02-18_1720

## Decisions Made During This Run

### DEC-EST-001: Treatment of Level_of_Effort.csv hour quantities

| Field | Value |
|---|---|
| DecisionID | DEC-EST-001 |
| Date | 2026-02-18 |
| Context | Level_of_Effort.csv records Basis=PARAMETRIC for its hour estimates. This run uses BASIS_OF_ESTIMATE=RATE_TABLE. |
| Decision | Treat the LoE hours as **quantity inputs** (Qty column) and apply unit rates from Professional_Staff_Rates.csv. The Method for each line item is RATE_TABLE because the pricing action is rate x quantity, and the rate source is an explicit rate table. |
| Rationale | The LoE file provides "how many hours" (a quantity), not "how much it costs" (a price). The rate table provides the pricing. The RATE_TABLE method label reflects the pricing action, not the quantity derivation method. |
| Impact | All labour lines are Method=RATE_TABLE. No mixed methods. |

### DEC-EST-002: CBS codes derived by agent

| Field | Value |
|---|---|
| DecisionID | DEC-EST-002 |
| Date | 2026-02-18 |
| Context | No CBSHint is present in the decomposition for DEL-01-03. |
| Decision | Assign agent-derived CBS codes: CBS-LABOUR-SAFETY, CBS-LABOUR-ADMIN, CBS-TRAINING, CBS-SUPPLIES. |
| Rationale | CBS codes are needed for the WBS/CBS matrix. In the absence of a formal CBS, these labels are derived from the cost driver categories identified in the brief (safety officer hours, training costs, PPE/signage supplies) and the role categories in the rate table. |
| Impact | CBS codes should be reviewed and aligned with any formal CBS if one is established for the project. |

### DEC-EST-003: TBD for non-labour cost drivers under STRICT fallback

| Field | Value |
|---|---|
| DecisionID | DEC-EST-003 |
| Date | 2026-02-18 |
| Context | The brief identifies "training costs" and "PPE/signage supplies" as cost drivers for DEL-01-03. No pricing source (rate table, quote, or allowance) is available for these items. |
| Decision | Set Amount=TBD for L-0103-003 and L-0103-004. Do not invent prices. Surface in QA as WARNINGS. |
| Rationale | FALLBACK_POLICY=STRICT prohibits pricing without basis evidence. Recording TBD preserves human decision rights and avoids speculation. |
| Impact | Priced total ($7,240) is a known understatement. RUN_STATUS=WARNINGS. |

### DEC-EST-004: Scope limited to DEL-01-03 labour within PKG-001

| Field | Value |
|---|---|
| DecisionID | DEC-EST-004 |
| Date | 2026-02-18 |
| Context | Per PKG-001 cost ownership rules: "All project-level management and coordination costs are carried in PKG-001. Discipline-specific design hours are NOT in PKG-001." |
| Decision | All DEL-01-03 costs are project-level safety management costs, correctly carried in PKG-001. No discipline-specific design hours are included. |
| Rationale | Safety Officer (R-20) and Administrative/Doc Control (R-24) are project-level roles, not discipline-specific design roles. This is consistent with the PKG-001 cost ownership rule. |
| Impact | No scope boundary adjustment needed. |
