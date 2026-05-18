# Assumptions_Log — EST_DEL-013-01_2026-02-27_1045

| AssumptionID | Assumption | Source / Basis | Risk if Wrong | Used By |
|---|---|---|---|---|
| ASM-001 | Natural gas is the fuel source for the heating system | R-01 Section 3.3.2 references natural gas tie-in; Datasheet notes ASSUMPTION: natural gas | If electric or propane, gas connection scope removed; equipment pricing changes; gas fitter requirement (REQ-012) does not apply | L-004, L-001 |
| ASM-002 | Two (2) heating units are required for the 13,000 sqft high-bay shop | Building area and ceiling height (35 ft) suggest multiple units for adequate coverage; single large unit is alternative | If 1 large unit, equipment count changes; if 3+ units, cost increases | L-001 |
| ASM-003 | Heat recovery ductwork connections allowance is $4,500 | Derived from MS-06 scope range; accounts for additional ductwork tie-ins to DEL-013-02 air exchanger loop | Actual cost depends on equipment type and duct routing | L-003 |
| ASM-004 | Gas line connection scope is approximately 38 hours of plumber/gas fitter work at $92.80/hr | Based on typical gas piping run from utility room connection point to equipment; includes leak testing | If longer run or complex routing, hours increase | L-004 |
| ASM-005 | Electrical connection scope is approximately 16 hours of electrician work at $96/hr | Based on typical circuit termination and coordination for 2 heating units | If complex 3-phase with VFDs, hours increase | L-005 |
| ASM-006 | Controls and BMS integration allowance is $6,000 | Based on ~24 hours of controls specialist (R-24 at $155/hr = $3,720) plus $2,280 for materials, sensors, and wiring | If BMS protocol is complex (e.g., full BACnet integration), cost increases significantly | L-006 |
| ASM-007 | Equipment positioning and securing allowance is $3,000 | Based on 2-person rigging crew x 16 hours (T-06 at $91.20/hr + T-08 at $65.10/hr) plus anchorage materials | If equipment is exceptionally heavy or requires crane, cost increases | L-007 |
| ASM-008 | Pre-commissioning inspection effort is $1,200 | Based on QA/QC lead (4 hr x $135) + superintendent (4 hr x $145) walkthrough | Minimal risk; inspection scope is well defined in Procedure | L-008 |
| ASM-009 | Safety Code inspection coordination effort is $500 | Scheduling and documentation effort only; permit fees paid by Owner | Minimal risk; scope is administrative | L-009 |
| ASM-010 | Initial start-up effort is $2,400 | Based on commissioning agent (8 hr x $160) + controls specialist (8 hr x $155) for one full start-up day | If start-up requires multiple days, cost increases | L-010 |
| ASM-011 | Integrated HVAC system test effort is $3,200 | Based on commissioning agent (16 hr x $160) + trade support; shared across PKG-013 deliverables | Cost allocation across 6 PKG-013 deliverables TBD; full cost allocated here | L-011 |
| ASM-012 | Performance verification testing effort is $1,600 | Based on commissioning agent (8 hr x $160) + instruments and data recording | If multiple test iterations required, cost increases | L-012 |
| ASM-013 | Commissioning report preparation effort is $1,200 | Based on document controller (8 hr x $75) + QA/QC lead review (4 hr x $135) | Minimal risk; report scope is defined in Procedure | L-013 |
| ASM-014 | As-built mark-ups effort is $750 | Based on BIM technician (8 hr x $95) for mark-up digitization | If extensive deviations from IFC drawings, effort increases | L-014 |
| ASM-015 | O&M manual compilation effort is $500 | Based on document controller (6 hr x $75) for compilation and submission | Minimal risk; compilation scope | L-015 |
| ASM-016 | Equipment submittal preparation is $800 | Based on mechanical engineer review time (4 hr x $165) plus admin support | Minimal risk if single submittal cycle; resubmittals add cost | L-016 |
| ASM-017 | Ductwork routing coordination meeting allowance is $1,000 | Multi-discipline coordination meeting + documentation for structural/architectural/MEP alignment | Minimal risk; standard coordination practice | L-017 |
| ASM-018 | Deficiency rectification allowance is $2,500 (approximately 2% of installation value) | Standard contingency for post-commissioning punch list work | If no deficiencies, cost is zero; if significant, could exceed allowance | L-026 |
| ASM-019 | Building floor area is 13,000 sqft (approximately 1,208 m2) | Assumed_Project_Parameters.csv PP-10 (DERIVED, MEDIUM confidence) | Ductwork line item ($72,480) is directly proportional to this parameter | L-002 |
