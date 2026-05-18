# Assumptions Log

## EST_DEL-05-04_2026-02-18_1800

| AssumptionID | Assumption | Source | Impact if Wrong | Confidence |
|---|---|---|---|---|
| ASM-01 | Camera system includes 16 camera locations: exterior (8), interior common areas (4), apparatus bays (2), entrances (2) | PP-29 in Assumed_Project_Parameters.csv | System price could vary significantly; OPT-08 range is $40,000-$60,000 for 16 cameras. More/fewer cameras would shift the total proportionally. | LOW |
| ASM-02 | OPT-08 system price ($50,000) includes IP cameras, NVR + storage, network switches (camera-side), cabling, mounting, programming, and commissioning | OPT-08 Notes column in Optional_Items_Pricing.csv | If scope of OPT-08 excludes any of these components, additional line items would be needed. | LOW |
| ASM-03 | Camera-side network switches and cabling are part of DEL-05-04; building IT backbone/VLAN configuration is part of DEL-02-06 | Brief cost ownership rules + DEP-0504-004 interface description | If ownership boundary is drawn differently, cost could shift between DEL-05-04 and DEL-02-06. Risk of double-count or gap. | LOW |
| ASM-04 | Monitoring service is a single annual subscription at $5,400/year | OPT-09 in Optional_Items_Pricing.csv | Multi-year contract terms, escalation clauses, or different service levels could change the annual cost. Only Year 1 is priced. | LOW |
| ASM-05 | No integration cost with access control system (DEL-05-03) is included | DEP-0504-006 (conditional interface) + DEC-EST-07 | If both options are elected and integration is desired, additional cost (not quantified) would apply. | MEDIUM |
| ASM-06 | All prices are in CAD and do not require currency conversion | Project context: CURRENCY=CAD; source file implicit CAD | No impact expected; all sources appear to use CAD. | HIGH |
