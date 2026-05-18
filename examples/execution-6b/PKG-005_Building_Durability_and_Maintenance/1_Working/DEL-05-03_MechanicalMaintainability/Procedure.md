# Procedure — DEL-05-03: Mechanical Maintainability

---

## Purpose

This document describes two related procedures:

1. **Production procedure:** How to produce the Mechanical Maintainability narrative (DEL-05-03) as a proposal deliverable within PKG-005 (Building Durability & Maintenance).
2. **Operational framework:** The maintenance approach the Town of Penhold will use to operate and maintain the mechanical systems after handover, with emphasis on apparatus bay exhaust ventilation, water fill stations, bay sump systems, bunker gear room ventilation, and backup generator.

The procedure ensures that mechanical maintainability is addressed consistently across all disciplines and is well-documented in the final O&M manual delivered at occupancy.

---

## Prerequisites

**Upstream dependencies (inputs to this deliverable):**

| Input | Status | Notes |
|---|---|---|
| DEL-02-04 (Mechanical Concept Narrative) | Upstream — must be substantially complete before this narrative is finalized | Defines baseline mechanical system selections (HVAC, plumbing, fire protection, emergency power, ventilation); DEL-05-03 elaborates the maintainability and lifecycle aspects of those selections |
| DEL-04-02 (Mechanical Energy and Solar Readiness) | Upstream — must identify specific HVAC and water heating equipment selections | Provides efficiency ratings, modular component details, and lifecycle implications; DEL-05-03 references these selections to finalize maintenance schedules and spare parts requirements |
| RFP §7.1.4; OSR §10.3.4 | Governing requirement | Primary authorities for mechanical maintainability requirements; both documents confirm "easy to maintain" as a design mandate |
| Addendum 03 (Jul 31, 2024) §§1.6, 1.8, 1.10–1.16 | Governing requirement (Addendum governs over base RFP where conflicts exist) | Defines specific mechanical system requirements: apparatus bay direct exhaust (§1.12), fill stations (§1.16), bunker gear room ventilation (§1.13, §1.14), bay sumps (§1.8), backup generator (§1.15), overhead door height (§1.10), gas service proximity (§1.6) |
| Decomposition v2 (DEL-05-03 entry; PKG-005 context) | Reference | Scope coverage (SOW-0013), responsible party, objective alignment (OBJ-005), design life constraints (50-yr main; 20-yr Cold Storage) |
| Existing 2021 Geotechnical Report (RFP Appendix D) | Reference | Required for sump pit design and below-grade mechanical equipment placement; no additional investigation per Decomposition v2 §DEC-013 (OI-004 resolution) |

**Required reference standards:**

- NFPA 25 (Inspection, Testing, and Maintenance of Water-Based Fire Protection Systems)
- NFPA 13 (Installation of Sprinkler Systems)
- NFPA 110 (Emergency and Standby Power Systems)
- ASHRAE 62.1 (Ventilation for Acceptable Indoor Air Quality — commercial/institutional zones)
- Alberta Building Code (current edition) — Section 6 (HVAC) and Section 7 (Plumbing)
- Alberta OH&S Regulations (mechanical room safety, lockout/tagout, confined space if applicable)
- CSA B139 (if oil-burning equipment is selected; may be superseded by natural gas codes)

---

## Steps

### Step A1 — Establish Mechanical Systems Inventory and Baseline Maintainability Strategy

**Phase:** Design Brief (proposal stage, concurrent with DEL-02-04)

**Inputs:** DEL-02-04 draft; RFP §11; Addendum 03 §§1.6, 1.8, 1.11–1.16; OSR §10.3.4; OSR §10.3.5.

**Actions:**

1. Extract system definitions from DEL-02-04 (or define preliminary assumptions if DEL-02-04 is not yet complete). For each of the following systems document the system type, zone served, and basis for system selection:
   - HVAC: heating, cooling, and ventilation by zone (offices, residential quarters, apparatus bays, PW bays, bunker gear room, decontamination rooms, mechanical room)
   - Plumbing: domestic hot water system type; water distribution; sanitary and storm drainage; sump systems; water fill stations (2" minimum, ground level, one per bay per Addendum 03 §1.16)
   - Fire protection: sprinkler system type (wet or dry pipe TBD); main shutoff location; inspector test connection location
   - Emergency power: generator capacity (kW TBD); fuel type (natural gas — available per Addendum 03 §1.6 — or diesel); transfer switch type; critical loads (kitchen, ICP/meeting room, 2 bathrooms; bay door secondary opening per Addendum 03 §1.15); runtime target: TBD pending Town confirmation (72-hour figure is ASSUMPTION from prior project context, not confirmed in Addendum 03 §1.15 — see Guidance CONF-01 for conflict resolution; _SEMANTIC_LENSING.md B-003)
   - Apparatus bay direct exhaust: makeup air intake and dedicated exhaust fan (2 apparatus per bay per Addendum 03 §1.12 and RFP §11.1.1); isolation damper design; filter access provisions
   - PW bay general ventilation: fan type; capacity for occasional vehicle idling and very occasional welding (Addendum 03 §1.11; no dedicated welding ventilation required)
   - Cold Storage ventilation: anti-condensation and anti-icing air circulation provisions (RFP §11.1.2); freeze-thaw rated equipment; **verify on drawings that condensate drain provisions are freeze-thaw rated** and that ventilation equipment housings are specified for unheated enclosure temperature ranges (see Guidance C-003; _SEMANTIC_LENSING.md A-003)
   - Bunker gear room ventilation: dedicated supply/exhaust; room-level air balancing for 40-locker room (Addendum 03 §1.13, §1.14; direct-to-locker NOT required)

2. **Confirm Building Automation System (BAS) scope decision:** Before proceeding with monitoring, alarm, and maintenance workflow design, confirm whether BAS integration is included in the project scope. BAS is currently marked as ASSUMPTION in the Datasheet Construction table (HVAC row). If BAS is included, document the BAS scope (monitoring points, alarm routing, manual override provisions) and its impact on maintenance workflow design. If BAS is excluded, document manual monitoring and alarm provisions as the alternative. This confirmation affects Specification R-MEL requirements for monitoring and Procedure Steps A2–A4 (see _SEMANTIC_LENSING.md F-002).

3. For each major system, identify and document the location and accessibility of:
   - Filter elements (size, type, replacement frequency)
   - Valve shutoff locations (isolation, emergency)
   - Drain points (fluid draining, system flushing)
   - Service ports (pressure gauges, refrigerant service access, oil replenishment)
   - Monitoring points (pressure-drop indicators, oil sight glasses, fuel level gauges)
   - Verify clearances meet minimum standards (equipment OEM recommendations; CSA/Alberta OH&S as applicable)

4. Draft preliminary maintenance schedule matrix by system and interval:

   | System | Quarterly | Semi-Annual | Annual | Remarks |
   |---|---|---|---|---|
   | Apparatus bay direct exhaust | Filter inspection; isolation damper test | — | Filter replacement; system airflow verification | Per Addendum 03 §1.12; RFP §11.1.1 |
   | PW bay general ventilation | — | — | Filter change; fan belt inspection | Addendum 03 §1.11; ASSUMPTION |
   | Cold Storage ventilation | Visual condensation check | — | Fan housing inspection; corrosion check | RFP §11.1.2; ASSUMPTION |
   | Bunker gear room ventilation | Filter inspection | — | Filter replacement; room air balance check | Addendum 03 §1.14 |
   | HVAC (high-load zones) | Filter replacement | — | Refrigerant pressure check; coil inspection | ASSUMPTION: quarterly for bay zones |
   | HVAC (low-load zones) | — | — | Filter replacement; annual service call | ASSUMPTION |
   | Water fill stations (both bays) | — | — | Strainer basket cleaning; system flush; pressure test; backflow device test | Addendum 03 §1.16 |
   | Bay sump pumps | Manual pump test | Discharge strainer inspection | Pump replacement evaluation | 3–5 year replacement cycle (ASSUMPTION — design basis to be validated during detailed design; see _SEMANTIC_LENSING.md F-003) |
   | Fire sprinkler system | — | — | Annual inspection per NFPA 25; main valve test | Specialist contractor required |
   | Backup generator | — | Fuel system inspection; battery check | Load test; oil/coolant service | NFPA 110; contractor-supervised |

5. Develop preliminary spare parts strategy:
   - Consumables (1-year supply): filters (all systems), belts, seals, fluids
   - Major replacement items (5-year cycle): pump impellers, motor bearings, valve cartridges
   - Estimated storage space: approximately 150–300 sq ft in mechanical room (ASSUMPTION)
   - Identify preferred suppliers and procurement lead times for critical items

6. Document preliminary lifecycle cost analysis for major equipment:
   - HVAC (heating and cooling units): capital cost vs. 20-year operating cost trade-off per Guidance T-001
   - Water heating: centralized tank vs. decentralized on-demand
   - Generator: natural gas (utility-dependent) vs. diesel (fuel storage required) per Guidance C-004
   - Note efficiency ratings (EER, HSPF, SEER, thermal efficiency) and estimated annual energy consumption
   - (Detailed analysis may be deferred to DEL-04-02 Mechanical Energy and Solar Readiness)

**Verification:** Mechanical Engineer and Architect confirm no access conflicts between mechanical equipment and architectural elements. Town representative (Operations Manager or equivalent) confirms preliminary maintenance schedule is operationally realistic.

**Responsible Party:** Mechanical Engineer (primary); Architect, Structural Engineer, Town Representatives (input/review).

**Timing:** Design Brief phase (concurrent with DEL-02-04 and DEL-04-02).

---

### Step A2 — Detailed Design Development of Equipment Access and Service Procedures

**Phase:** 60% Design Development

**Inputs:** Equipment schedules and preliminary design drawings from Step A1.

**Actions:**

1. Finalize equipment specifications and access layouts:
   - Equipment schedule: specific models, sizes, efficiency ratings, service valve locations, drain points for all major mechanical equipment
   - Mechanical room plan drawing showing: equipment layout with minimum 900 mm (3 ft) service aisle clearances; drain pan and floor slope configuration; service points labeled (fuel fill, oil/coolant fill, battery terminals); spare parts storage allocation (estimated 150–300 sq ft)
   - Apparatus bay exhaust system detail drawing: makeup air intake, filter cartridge access point, isolation damper hand-lever location, filter element size/type/part number, drain/condensate provisions (RFP §11.1.1; Addendum 03 §1.12)
   - Water fill station schematic: backflow prevention device, isolation shutoff valve, check valve, strainer basket location — all labeled for maintenance access (Addendum 03 §1.16)
   - Generator site plan: service clearances, fuel fill access, battery terminal access, ATS location, exterior load test pad dimensions

2. Confirm maintenance schedule intervals align with equipment OEM recommendations:
   - Cross-reference equipment data sheets to confirm filter replacement frequency, fluid change intervals, major service milestones
   - Adjust schedule for high-load duty cycles in fire and PW environments (apparatus bay exhaust may require quarterly or more frequent filter replacement depending on apparatus call frequency)
   - Document deviations from OEM baseline and justify in the narrative

3. Develop Operation and Maintenance (O&M) Manual outline:
   - Section 1: System Overview — general description, equipment list, control points
   - Section 2: Routine Maintenance Procedures — daily, weekly, monthly tasks with step-by-step instructions
   - Section 3: Preventive Maintenance Schedule — quarterly, semi-annual, annual tasks with responsible party, estimated time, and cost
   - Section 4: Emergency Repair Procedures — manual backups; emergency contractor contact information
   - Section 5: Spare Parts and Inventory — consumables stock list, major item replacement, supplier contacts, reorder lead times
   - Section 6: Equipment Specifications and Warranties — data sheets, warranty terms, manufacturer contacts
   - Section 7: Control System Documentation — BAS manual (if applicable), manual override procedures
   - Section 8: Troubleshooting Guide — common problems, diagnostic steps, when to call a specialist
   - Appendix A: Maintenance Log Forms — printable templates
   - Appendix B: Vendor Contact List — equipment suppliers, service contractors, emergency hotlines

4. Finalize spare parts inventory list:
   - Consumables (1-year supply): filters by system (HVAC main, apparatus bay exhaust, PW bay, bunker gear room, sump strainer, fill station strainer); belts; seals/O-rings; refrigerant (type and quantity); compressor oil; pump oil; generator oil and coolant
   - Major items (5-year replacement or emergency): pump impellers; motor bearings; fan blade assemblies (if modular); valve cartridges (if solenoid-operated valves used); BAS sensors/actuators (ASSUMPTION if BAS included)
   - Estimated storage space: 150–300 sq ft of shelving in mechanical room (ASSUMPTION)

5. Develop staff training plan:
   - Identify Town staff responsible for routine and preventive maintenance (Fire and PW)
   - Outline hands-on training topics: filter changes, drain valve operation, isolation damper testing, sump pump operation, fill station flushing, generator emergency operation, bay door secondary opening mechanism
   - Define which tasks are in-house staff responsibility vs. contracted specialist
   - Recommend annual refresher training

**Verification:** Mechanical Engineer confirms all equipment access points are documented on drawings. Architect confirms mechanical room layout integrates with architectural design. Town Operations Manager confirms maintenance schedule and training plan are feasible.

**Responsible Party:** Mechanical Engineer (primary); Architect, Commissioning Agent, Town Representatives (input/review).

**Timing:** 60% Design Development phase.

---

### Step A3 — Final Design and Construction Document Compliance Check

**Phase:** 100% Design Development / IFC package

**Inputs:** Final mechanical design drawings and equipment schedules.

**Actions:**

1. Verify maintainability requirements are reflected in detailed drawings:
   - All equipment service points accessible per Specification requirements R-MEL-01 through R-MEL-14
   - No unintended blocking of access by architectural or structural elements
   - Drain/fill/service valve locations clearly labeled on drawings
   - Maintenance procedures for key systems documented in drawing general notes

2. Confirm spare parts procurement and delivery timeline:
   - Identify long-lead items (custom-configured generators, specialized exhaust filters, valve cartridges)
   - Coordinate with Construction Manager to ensure spare parts inventory arrives before or during commissioning
   - Allocate and install mechanical room storage space before occupancy

3. Finalize O&M manual and training documentation:
   - Collect all equipment manuals from manufacturers (physical and digital)
   - Compile comprehensive O&M manual per outline from Step A2
   - Prepare training materials: photos and schematics of key maintenance points; step-by-step procedures for apparatus bay exhaust filter inspection, fill station flushing, generator emergency operation, bay door secondary opening mechanism operation
   - Schedule staff training dates with Commissioning Agent (pre-occupancy)

**Verification:** Design team conducts final maintainability review against Specification requirements R-MEL-01 through R-MEL-14. Commissioning Agent confirms O&M manual completeness.

**Responsible Party:** Mechanical Engineer (primary); Commissioning Agent, Design Manager, Construction Manager, Town Representatives.

**Timing:** 100% Design Development and IFC package phase.

---

### Step A4 — Commissioning and System Verification

**Phase:** Pre-occupancy commissioning

**Inputs:** Completed mechanical systems, as-built drawings, O&M manual draft.

**Actions:**

1. Commission all mechanical systems per design intent:
   - HVAC: verify thermostat set-points, zone balancing, filter airflow resistance
   - Apparatus bay exhaust: operate makeup air and exhaust dampers in isolation service mode; verify filter cartridge access and replacement procedure demonstrated to operations staff; confirm Addendum 03 §1.12 and RFP §11.1.1 compliance
   - Water fill stations: operate isolation shutoffs; demonstrate strainer basket removal and annual flushing procedure (Addendum 03 §1.16); test backflow prevention device
   - Fire sprinkler: confirm inspector test connection access; document system drain valve location; verify NFPA 25 compliance (initial inspection by specialist contractor)
   - Bay sump pumps: test manual backup pump provision; verify pump removal accessibility; confirm discharge strainer access
   - Generator: perform pre-occupancy baseline load test; confirm fuel fill, oil service, and battery access; confirm bay door secondary opening mechanism functional in test mode (Addendum 03 §1.15); document transfer time
   - Cold Storage ventilation: confirm anti-condensation/anti-icing circulation operational; verify freeze-thaw rated equipment specifications
   - Bunker gear room ventilation: confirm room air balance achieved; filter access demonstrated; airflow verified at 40-locker room level (Addendum 03 §1.14)
   - BAS/controls (if used): verify manual override procedures for all critical systems

2. Conduct staff training on maintenance procedures per training plan from Step A2. Confirm competency sign-off for: apparatus bay exhaust filter inspection; fill station flushing; generator emergency operation; bay door secondary opening (whichever method selected).

3. Verify spare parts inventory is in stock in mechanical room; confirm supplier contact list in O&M manual is current.

4. Document as-built conditions; resolve any deviations from design intent that compromise maintainability.

**Verification:** Commissioning Agent confirms all maintenance procedures tested and documented. Town Operations Manager signs off on staff training completion. Final O&M manual accepted (2 hard copies in 3-ring binders + digital).

**Responsible Party:** Commissioning Agent (primary); Mechanical Engineer, Construction Manager, Town Representatives.

**Timing:** Pre-occupancy commissioning phase (typically 2–4 weeks before occupancy permit).

---

### Step A5 — Post-Occupancy and 12-Month Warranty Period

**Phase:** Occupancy through 12-month warranty review

**Inputs:** Commissioned systems, trained staff, O&M manual.

**Actions:**

1. Town begins maintenance log entries per O&M manual schedule; Operations staff complete routine and preventive tasks as trained.
2. Annual major system inspections within first year: generator load test; fire sprinkler annual inspection per NFPA 25 (specialist contractor); water heater service call; HVAC annual efficiency check; fill station flushing.
3. Document any equipment failures or unexpected maintenance needs; contractor provides warranty support during 12-month period per RFP §7.6 and Supplementary Conditions SC54–SC55.
4. At end of warranty period: establish annual service contracts for specialized tasks (refrigerant service, sprinkler inspection, generator load test with portable load bank).

**Verification:** Town Operations Manager confirms routine maintenance is on schedule. Contractor provides warranty closeout documentation including punch list resolution and final 12-month review sign-off.

**Responsible Party:** Town Operations Manager (primary); Mechanical Contractor (warranty period support).

**Timing:** Occupancy through 12-month post-occupancy warranty review.

---

## Verification

**Requirement verification cross-reference (Specification R-MEL-01 through R-MEL-14):**

| Req ID | Requirement (short) | Verified in Procedure Step | Responsible Party | Timing |
|---|---|---|---|---|
| R-MEL-01 | Equipment access — service routes and 900 mm aisle widths | A2.1 (room plan confirmed); A4.1 (commissioning confirms accessibility) | Mechanical Engineer; Commissioning Agent | 60% DD; pre-occupancy |
| R-MEL-02 | Floor-level reach for routine maintenance | A2.1 (reach distances on drawings); A4.2 (staff training confirms) | Mechanical Engineer; Operations | 60% DD; commissioning |
| R-MEL-03 | HVAC filter accessibility and replacement intervals | A2.2 (schedule confirmed against OEM); A4.1 (filter change procedure tested) | Mechanical Engineer; Commissioning | 60% DD; commissioning |
| R-MEL-04 | Apparatus bay exhaust — filter and damper access | A3.1 (details finalized); A4.1 and A4.2 (isolation damper and filter access tested and demonstrated) | Mechanical Engineer; Commissioning; Operations | Design and commissioning |
| R-MEL-05 | Water fill station serviceability | A2.1 (schematic finalized); A4.1 and A4.2 (flushing procedure tested and demonstrated) | Mechanical Engineer; Commissioning; Operations | Design and commissioning |
| R-MEL-06 | Bay sump system accessibility | A2.1 (pit design confirmed against geotech report); A4.1 (manual backup pump tested) | Mechanical Engineer; Commissioning | Design and commissioning |
| R-MEL-07 | Bunker gear room ventilation serviceability | A2.2 (equipment spec confirmed; supplier verified); A4.1 (filter access and room air balance tested) | Mechanical Engineer; Commissioning | Design and commissioning |
| R-MEL-08 | Generator service access and load testing | A2.1 (site plan finalized); A4.1 (pre-occupancy baseline load test) | Mechanical Engineer; Commissioning | Design and commissioning |
| R-MEL-09 | Standard modular parts selection | A1.1 and A2.1 (equipment schedule documents standard components; non-standard items justified) | Mechanical Engineer | Design phases |
| R-MEL-10 | Spare parts storage allocation | A1.5 (inventory list created); A2.1 (mechanical room plan allocated); A4.3 (parts in stock confirmed before occupancy) | Mechanical Engineer; Contractor; Operations | Design and commissioning |
| R-MEL-11 | Maintenance schedule framework | A1.4 and A2.2 (schedule matrix finalized and aligned to OEM); A3.3 (O&M manual compiled); A4.2 (staff training confirms) | Mechanical Engineer; Commissioning | Design and commissioning |
| R-MEL-12 | Lifecycle cost analysis | A1.6 (preliminary analysis documented); A2.2 (finalized in narrative) | Mechanical Engineer | Design Brief phase |
| R-MEL-13 | Lockout/tagout (LOTO) provisions | A2.1 (LOTO points identified on mechanical drawings); A3.1 (LOTO hardware installed and labeled); A4.1 (LOTO procedures verified during commissioning) | Mechanical Engineer; Commissioning Agent | 60% DD; commissioning |
| R-MEL-14 | Overhead door mechanical hardware maintainability | A2.1 (door hardware maintainability provisions on door schedule); A3.1 (maintenance cycle documented); A4.1 (accessibility verified during commissioning) | Mechanical Engineer; Architect (DEL-05-01 coordination) | 60% DD; commissioning |

---

## Records

**Anticipated documentation artifacts:**

1. **Mechanical Maintainability Narrative** — primary deliverable artifact; system-by-system strategy, access approach, filter maintenance, spare parts strategy; addresses all SOW-0013 scope elements.

2. **Mechanical Room Layout Plan** (drawing) — equipment arrangement with 900 mm minimum service route clearances and spare parts storage allocation labeled.

3. **Apparatus Bay Exhaust Maintenance Detail** (drawing + procedure) — filter cartridge access detail, isolation damper location, quarterly inspection and annual replacement checklist; compliant with Addendum 03 §1.12 and RFP §11.1.1.

4. **Water Fill Station Maintenance Schematic** (drawing + procedure) — backflow device, check valve, strainer location, annual flushing steps; compliant with Addendum 03 §1.16.

5. **Bay Sump System Design and Maintenance Plan** (drawing + narrative) — pit layout, pump accessibility, manual backup provision, quarterly drainage test; consistent with existing 2021 geotechnical report.

6. **Maintenance Schedule Matrix** (table) — all systems × interval (daily/weekly/monthly/quarterly/semi-annual/annual); task descriptions; responsible party (in-house vs. contracted specialist).

7. **Equipment Schedule Summary** (table) — HVAC, plumbing, fire protection, emergency power; modular component notes; service valve and drain point locations.

8. **Spare Parts Inventory List** (table) — consumables (1-year supply) and major items (5-year cycle); quantity, part number, supplier, lead time.

9. **Lifecycle Cost Analysis Summary** (narrative or appendix) — equipment selection trade-off rationale; 20-year NPV or simple payback estimates for major systems.

10. **O&M Manual** (comprehensive document, delivered at occupancy) — system overviews, routine procedures, preventive maintenance schedule, emergency procedures, troubleshooting guide, maintenance log forms, vendor contacts; 2 hard copies in 3-ring binders + digital (per RFP §7.3.6 O&M manual delivery requirements).

11. **Staff Training Documentation** — attendance log; competency sign-off forms for key maintenance tasks; laminated procedure cards posted at equipment locations.

12. **As-Built Drawings** (updated mechanical plans) — final equipment locations, service valve and drain locations as-constructed.

13. **Commissioning Reports** — apparatus bay exhaust verification; fill station flushing sign-off; sump pump test results; generator pre-occupancy baseline load test report (per NFPA 110).

14. **Warranty Closeout Documentation** — final punch list resolution; 12-month warranty review sign-off (per RFP §7.6; SC54–SC55); transition plan to Owner's standard maintenance operations.
