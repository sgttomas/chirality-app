# Assumptions Log — EST_DEL-013-03_2026-02-27_0901

| AssumID | Assumption | Source / Basis | Impact if Wrong | Lines Affected |
|---|---|---|---|---|
| ASM-001 | MUA unit is gas-fired (natural gas heating) | Guidance C3; consistency with DEL-013-01 (high-recovery heating); SOW-0080 gas tie-in | If electric or indirect heating: gas connection ($2,500) not needed; MUA unit cost may differ | L-001, L-024 |
| ASM-002 | Building floor area is 13,000 sqft (1,208 m2) per PP-10 | Assumed_Project_Parameters.csv PP-10 (DERIVED, MEDIUM confidence) | Ductwork parametric scales linearly; 10% area error = ~$7,248 ductwork cost change | L-003, L-007, L-011 |
| ASM-003 | Ductwork parametric rate of $60/m2 (normalized per floor area) includes main trunk, branch runs, fittings, and basic hangers | Mechanical_System_Rates.csv MS-06 (PARAMETRIC, MEDIUM confidence) | If rate excludes certain items, supplementary line items may be needed | L-003 |
| ASM-004 | 4 fire/smoke dampers required at fire-rated assembly penetrations | Estimate based on typical industrial shop with limited fire separations | Actual count could be 2-8+; $650/EA impact per damper | L-005 |
| ASM-005 | Ductwork insulation cost is approximately 15% of supply ductwork installed cost | Industry parametric ratio for commercial/industrial insulated ductwork | Actual depends on insulation type, thickness, and vapor barrier (all TBD per DEL-003-07) | L-007 |
| ASM-006 | Ductwork hanger/support cost is approximately 7.5% of supply ductwork installed cost | Industry parametric ratio; elevated for 35ft ceiling height | Complex structural attachments near crane rails may increase cost | L-011 |
| ASM-007 | Centralized single MUA unit serving all zones via duct distribution | Guidance T2 suggests centralized approach most likely | Multiple smaller units would change equipment cost structure significantly | L-001 |
| ASM-008 | TAB (test and balance) cost of $4,500 for MUA system | Industry parametric for commercial HVAC TAB with multiple distribution points | Actual depends on number of supply terminals and TAB contractor pricing | L-014 |
| ASM-009 | MUA unit requires crane/rigging for setting ($3,500) | Procedure Step 1.3 notes large/heavy unit | Smaller units may not require crane; larger may require more expensive rigging | L-023 |
| ASM-010 | Commissioning scope (start-up + controls + integrated test + pressurization) totals $7,500 | Parametric based on complexity of multi-system integration (5 related deliverables) | Commissioning scope depends on mechanical engineer's requirements (TBD) | L-016, L-017, L-018 |
| ASM-011 | Controls/BAS integration cost of $5,500 for MUA-to-building integration | MUA interfaces with DEL-013-01 (heating) and DEL-013-02 (air exchanger); assumed moderate complexity | If controls scope is more extensive (e.g., full DDC with multiple sensors), cost increases | L-010 |
| ASM-012 | Dampers and control valves cost $4,500 (intake + supply + zone dampers) | Parametric for motorized intake damper + main supply damper + zone volume dampers | Actual depends on number of zones and damper sizes (TBD per design) | L-004 |
| ASM-013 | Wash bay is included in MUA distribution scope | Datasheet ASSUMPTION per Enrichment X-001; pending confirmation from DEL-003-02 | If excluded: slight reduction in ductwork extent and TAB scope | L-003 |
| ASM-014 | AHJ inspection fees are $350/EA for rough-in and final inspections | Alberta mechanical inspection fee parametric | Actual fees per Camrose County AHJ schedule | L-025 |
| ASM-015 | Mechanical permit fee is $1,500 | Alberta mechanical permit parametric for commercial HVAC | Actual fee per Camrose County AHJ fee schedule | L-012 |
