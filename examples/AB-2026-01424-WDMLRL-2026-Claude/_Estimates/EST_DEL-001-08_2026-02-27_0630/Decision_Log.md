# Decision Log — EST_DEL-001-08_2026-02-27_0630

## Decisions Applied During This Run

| DecID | Decision | Rationale | Impact |
|---|---|---|---|
| DEC-001 | Used Level_of_Effort.csv (parametric LOE by role) as the primary pricing mechanism rather than Professional_Design_Fees.csv (percentage-of-construction-value) | LOE model provides deliverable-specific granularity; fee percentage model is a project-level cross-check, not a deliverable-level pricing tool. BASIS_OF_ESTIMATE=PARAMETRIC supports either, but LOE is more precise for a single deliverable. | Line items are priced at role x hours x rate. Fee percentage model could be used for project-level validation. |
| DEC-002 | Items ITEM-006 through ITEM-011 (work activities extracted from Datasheet, Specification, and Procedure) are recorded in Items.csv for scope traceability but are not separately priced in Detail.csv | These items represent the work content that the 5 labour roles (ITEM-001 through ITEM-005) perform. Pricing them separately would double-count the same labour. The LOE model in Level_of_Effort.csv is role-based, not activity-based. | 6 items in Items.csv with no corresponding Detail.csv lines. QA report documents this as intentional scope traceability, not a pricing gap. |
| DEC-003 | CBS categories assigned as Design-Management (PM, Cost Estimator) and Design-Production (Senior Architect, Architect, BIM Technician) | Standard CBS for professional design deliverables. Aligns with role categories in Professional_Staff_Rates.csv (Management vs Design). | WBS_CBS_Matrix.csv shows two CBS rows. |
| DEC-004 | Parametric_Building_Rates.csv not used for line-item pricing | PB-01 ($285/sf) and PB-02 ($70/sf) are construction cost rates, not design production cost rates. DEL-001-08 is a design document. These rates are noted in Source_Index.md for context only. | No impact on totals. |
| DEC-005 | UPDATE_LATEST_POINTER=FALSE respected; no pointer file modified | Per brief instruction. | No _LATEST.md file created or modified. |
