# Assumptions Log -- EST_DEL-05-03_2026-02-18_1700

## Assumptions

| AssumptionID | Assumption | Source | Impact if Wrong | Linked Decision |
|---|---|---|---|---|
| ASM-001 | Number of controlled access zones is 10. | PP-28 (Assumed_Project_Parameters.csv) | If zone count exceeds 10, each additional zone adds ~$3,200 (OPT-07). If fewer than 10, system may still be priced as 10-zone base. | DEC-RUN-002 |
| ASM-002 | Zone distribution: Exterior entries (4) + apparatus bay entries (2) + PW bay entries (2) + server/electrical rooms (2) = 10. | PP-28 Notes | Actual distribution depends on DEL-02-01 floor plan. Changed zone types may not affect total price significantly at this parametric level. | DEC-RUN-002 |
| ASM-003 | All access control equipment, wiring, installation, and software licensing costs are included in the OPT-06 system price. | OPT-06 Notes in Optional_Items_Pricing.csv | If significant scope elements are excluded from OPT-06 (e.g., annual software licensing fees), additional line items would be needed. | DEC-RUN-003 |
| ASM-004 | Ancillary buildings (cold storage) are excluded from access control scope. | SOW-0502 (OSR S12.3) | If Owner elects to extend access control to cold storage, additional zones and wiring would be required (not priced here). | -- |
| ASM-005 | Access control system is designed as self-contained and does not require integration with security camera system (DEL-05-04) for pricing purposes. | DEP-05-03-005; Guidance.md | If integration is required, additional costs for software integration, shared head-end, etc. may apply. | -- |
| ASM-006 | IT network infrastructure, door hardware, and electrical power circuits to controllers are excluded from this estimate and are the cost responsibility of other deliverables. | Brief: Cost Ownership Rules | If scope boundaries shift, items may need to be re-allocated. | DEC-RUN-005 |
