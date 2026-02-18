# Specification — DEL-05-03: Mechanical Maintainability

---

## Scope

**In Scope:**

- Mechanical systems maintainability strategy for a combined Fire Hall and Public Works Operations facility (main building, 50-year design life)
- Cold Storage ancillary building mechanical maintainability provisions (20-year design life)
- Equipment access provisions: mechanical room layout, service route clearances, spacing standards
- Equipment serviceability and modular component approach: replaceable units, standard parts availability, design for non-invasive routine servicing
- Maintenance schedule framework for HVAC, plumbing, fire protection, and emergency power systems
- Lifecycle cost considerations for major mechanical equipment: energy efficiency, durability trade-offs, replacement cycles
- Ventilation system filter access and maintenance, with special emphasis on apparatus bay direct exhaust systems
- Bay sump systems maintainability (apparatus bay and PW bay)
- Water fill station (2" minimum) serviceability and annual flushing provisions
- Backup generator service access and testing provisions
- Bunker gear room ventilation serviceability
- Coordination interface with DEL-05-01 (Architectural Durability), DEL-05-02 (Structural Durability), and DEL-05-04 (Electrical Maintainability)

**Out of Scope:**

- Detailed mechanical equipment specifications (deferred to 60% Design Development phase)
- Vendor-specific maintenance manuals (produced during construction and commissioning)
- Staff training procedures (addressed in DEL-08-01 — Commissioning/Training/Closeout)
- Pickled Sand Storage building mechanical systems (removed from project scope per Addendum 03 §1.2)
- Day-to-day operational maintenance tasks after occupancy (Owner's responsibility; O&M manual and training from DEL-08-01 govern this)

---

## Requirements

| Req ID | Requirement | Source | Verification Approach |
|---|---|---|---|
| **R-MEL-01** | Mechanical systems shall be arranged to be practical and easy to maintain: all equipment shall allow inspection, maintenance, and emergency repair without removal of building elements or other equipment; minimum 900 mm (3 ft) service aisle widths in mechanical rooms. | RFP OSR §10.3.4 ("practical ... easy to maintain" verbatim); RFP §7.1.4 ("ease of repair and maintenance"); ASSUMPTION: 900 mm minimum aisle width consistent with Alberta Building Code mechanical room access provisions — **specific ABC clause TBD** (Mechanical Engineer to confirm whether this is a prescriptive code requirement under ABC Section 6 or a design assumption; see _SEMANTIC_LENSING.md A-001) | Design review: mechanical room plan confirms clear service routes and minimum aisle widths; site walk-through at substantial performance |
| **R-MEL-02** | Equipment requiring routine maintenance (filters, belts, fluid replenishment, drain valves) shall be accessible from finished floor level without climbing equipment or requiring specialized tools, except where trade-standard tools are unavoidable. Maximum reach height for routine maintenance points shall not exceed 1800 mm (6 ft) from finished floor level (ASSUMPTION: ergonomic reach standard consistent with ASHRAE or applicable ergonomic guideline — specific standard TBD; see _SEMANTIC_LENSING.md X-002). | RFP §7.1.4 ("ease of maintenance"); RFP OSR §10.3.4; ASSUMPTION: operations-aware design practice for small municipal team; reach-height standard: ASSUMPTION (Mechanical Engineer to confirm applicable ergonomic reference) | Design review: reach-distance measurements for filter racks, valve handles, and drain plugs confirmed on drawings against 1800 mm maximum; site walk-through at substantial performance |
| **R-MEL-03** | HVAC filters shall be accessible and replaceable, with visual or pressure-drop indicators provided. Replacement frequency shall not exceed quarterly for high-load zones (apparatus bays, PW bays) and annual for low-load zones (offices, storage). | RFP §7.1.4; RFP §11.1.1 (apparatus bay HVAC requirement); Addendum 03 §1.12 (apparatus bay exhaust requirement drives filter duty cycle); ASSUMPTION: zone-based intervals consistent with operations environment | Equipment schedule specifies filter type, size, and replacement interval by zone; design drawings show filter racks with indicator locations |
| **R-MEL-04** | The apparatus bay direct exhaust system (2 apparatus per bay) shall have filters and isolation dampers accessible for quarterly inspection and filter replacement without full system depressurization or shutdown of the entire exhaust system. | RFP §11.1.1 (direct exhaust per bay mandatory, verbatim); Addendum 03 §1.12 ("direct exhaust ventilation for fire apparatus is required to accommodate two apparatus per bay", verbatim); SOW-0013 | Exhaust duct design detail confirms isolation dampers and filter cartridge access ports; commissioning test report documents accessibility procedure |
| **R-MEL-05** | Water fill stations (one in fire apparatus bay, one in PW bay; 2" minimum; both at ground level) shall include backflow prevention with accessible test ports, isolation shutoff valves, and strainer baskets accessible for annual flushing and cleaning without system shutdown. | Addendum 03 §1.16 (verbatim: "one fill station at ground level in the fire apparatus bay and one fill station at ground level in the public works bay. Both fill stations should be 2" minimum"); RFP §11.2 | Fill station design schematic shows backflow device, check valve, strainer location, and labeled shutoff valves; annual flushing protocol documented in O&M manual |
| **R-MEL-06** | Bay sump systems (apparatus bay and PW bay) shall include accessible sump pumps replaceable on a 3–5 year cycle (ASSUMPTION — design basis to be validated during detailed design based on pump duty cycle and operational conditions; see _SEMANTIC_LENSING.md F-003); a manual backup pumping capability shall be documented; sump pit design shall be consistent with the existing 2021 geotechnical report conditions. | Addendum 03 §1.8 ("all bays require sumps", verbatim); Decomposition v2 §DEC-013 (existing geotech report only); ASSUMPTION: 3–5 year pump replacement cycle is a design basis to be validated, not a confirmed requirement | Sump pit design drawing shows pump location, check valve, and discharge strainer accessibility; manual pump provision documented in O&M manual |
| **R-MEL-07** | The bunker gear room ventilation system shall be designed with accessible filters and dampers adjustable without building disturbance; the room shall have room-level ventilation (not direct-to-locker) sufficient to prevent moisture and mold accumulation across 40 lockers; minimum ventilation rate TBD (ASSUMPTION: ASHRAE 62.1 ventilation rates for locker/storage rooms are the applicable baseline — specific air changes per hour or cfm/locker TBD pending Mechanical Engineer calculation; see _SEMANTIC_LENSING.md C-001); filter replacement parts shall be commonly available (ASSUMPTION: 48-hour procurement or in-house stock). | Addendum 03 §1.13 (40 lockers); §1.14 ("the room itself should have ventilation", verbatim); SOW-0013; quantitative ventilation threshold: TBD (Mechanical Engineer to define measurable acceptance criterion per ASHRAE 62.1 or equivalent) | Equipment specification confirms cartridge-type filters; filter type and part number documented in spare parts inventory; supplier availability confirmed at design stage; **acceptance criterion for moisture/mold prevention: TBD** (quantitative threshold required for compliance testing) |
| **R-MEL-08** | The backup generator shall have accessible fuel fill point, oil and coolant service ports, battery terminals, and a designated exterior area or access provision for annual load testing with a portable load bank. Generator runtime target: TBD pending Town confirmation (72-hour figure is ASSUMPTION from prior project context, not confirmed in Addendum 03 §1.15 — see Guidance CONF-01; _SEMANTIC_LENSING.md B-003). If the runtime target is confirmed, fuel storage capacity, fuel system inspection schedule, and fuel turnover provisions shall be sized accordingly. | Addendum 03 §1.15 (generator required; minimum loads: kitchen, ICP/meeting room, 2 bathrooms; bay door secondary opening mechanism required — generator-powered or manual, verbatim); ASSUMPTION: standard industrial generator maintenance practice; runtime target: TBD pending human ruling per CONF-01 | Generator floor plan or site plan confirms service clearances; fuel fill, oil service, and battery access documented; annual load test provision included in O&M manual; if runtime target confirmed, fuel storage capacity verified against runtime requirement |
| **R-MEL-09** | All mechanical equipment selections shall favor industry-standard modular components, standardized refrigerant types, common valve configurations, and standard pump models to minimize spare parts inventory and avoid proprietary supplier lock-in. Any non-standard component selection shall include a documented justification demonstrating that the lifecycle cost premium (including higher maintenance costs and longer procurement lead times) is offset by measurable performance or efficiency benefits; acceptance threshold for "non-standard justification" TBD (ASSUMPTION: Mechanical Engineer to define quantitative acceptance criteria such as lifecycle cost premium threshold; see _SEMANTIC_LENSING.md A-002). | RFP §7.1.4 ("serviceability" emphasis); RFP §11.3 ("durable, flexible materials for easy maintenance", verbatim); ASSUMPTION: municipal operations best practice | Equipment selection checklist requires justification for any non-standard components with documented lifecycle cost comparison; refrigerant type, valve configurations, pump models documented in equipment schedules; **acceptance threshold for non-standard justification: TBD** |
| **R-MEL-10** | Mechanical room(s) shall include dedicated storage space (shelving or bins) for in-house spare parts inventory, sized to support at minimum a 1-year supply of consumables (filters, belts, seals) and a 5-year replacement cycle for major items (pump impellers, motor bearings, valve cartridges). | RFP §7.1.4 (maintenance strategy); ASSUMPTION: fire and PW facility standard practice | Mechanical room floor plan allocates dedicated shelving space (estimated 150–300 sq ft); spare parts list generated from equipment schedules at Design Development |
| **R-MEL-11** | A maintenance schedule framework shall document routine (daily/weekly/monthly), preventive (quarterly/semi-annual/annual), and corrective (as-needed) tasks for all mechanical systems, aligned with OEM recommendations and applicable code requirements (NFPA, Alberta Building Code, CSA). | RFP §7.1.4 ("ease of repair and maintenance of the building and all systems and components", verbatim); SOW-0013 | Maintenance schedule matrix (system × interval × task) included in the Mechanical Maintainability narrative and carried forward into the O&M manual |
| **R-MEL-12** | Lifecycle cost analysis shall document the equipment selection rationale for major mechanical systems (HVAC, water heating, pumping, emergency power), identifying trade-offs between capital cost, operating efficiency, and replacement cycle length, using a 20-year planning horizon. The analysis shall include: (a) a minimum of two alternatives compared per major system, (b) stated economic assumptions (energy cost escalation rate, discount rate, maintenance cost escalation rate), and (c) either a simple payback calculation or 20-year NPV comparison (ASSUMPTION: Mechanical Engineer and Design Committee to confirm minimum analysis depth; see _SEMANTIC_LENSING.md F-001). | RFP §7.1.4 ("lifecycle cost considerations for major mechanical equipment" explicit in SOW-0013 scope); RFP OSR §10.3.4 ("cost effective"); SOW-0013; analysis depth criteria: ASSUMPTION | Lifecycle cost narrative or worksheet included in Mechanical Maintainability narrative or DEL-04-02; major equipment trade-offs documented with simple payback or NPV estimates; **acceptance criteria: minimum two alternatives per system, stated economic assumptions, and quantified payback or NPV** |

| **R-MEL-13** | All mechanical equipment requiring servicing shall be provided with lockout/tagout (LOTO) provisions compliant with Alberta OH&S Regulations, including labeled lockout points, isolation device hardware, and documented LOTO procedures for each major system (HVAC units, exhaust fans, sump pumps, generator ATS). | Alberta OH&S Regulations (LOTO provisions referenced in Standards table); ASSUMPTION: LOTO hardware and procedures required for contractor and Owner maintenance personnel (see _SEMANTIC_LENSING.md C-002) | Design review: LOTO points identified on mechanical drawings; LOTO procedure documented in O&M manual; hardware installed and labeled at each lockout point; verified during commissioning |
| **R-MEL-14** | Overhead door mechanical hardware (springs, motors, tracks) specified as "car wash grade" (corrosion-resistant) per OSR §10.3.9 shall include maintainability provisions: accessible spring adjustment points, motor lubrication fittings at reachable height, and track cleaning access without scaffolding. Maintenance cycle for overhead door mechanical components TBD (ASSUMPTION: coordinate with DEL-05-01 Architectural Durability for door hardware scope boundary; see _SEMANTIC_LENSING.md X-003). | RFP OSR §10.3.9 ("car wash grade hardware for the main building"); Addendum 03 §1.10 (16 ft door height); scope boundary with DEL-05-01: TBD | Design review: overhead door hardware maintainability provisions shown on door schedule and detail drawings; maintenance cycle documented in maintenance schedule matrix |

---

## Standards

| Standard | Applicability | Notes |
|---|---|---|
| **NFPA 25** (Standard for the Inspection, Testing, and Maintenance of Water-Based Fire Protection Systems) | Fire sprinkler and fire pump maintenance and inspection access | Governs inspection intervals, drain valve access, main control valve access, inspector's test connection locations; specific clause locations TBD at detailed design phase |
| **NFPA 13** (Standard for the Installation of Sprinkler Systems) | Automatic sprinkler system design and maintenance provisions | Governs system component access, drain provisions, and inspection clearances; specific clause locations TBD |
| **ASHRAE 62.1** (Ventilation and Acceptable Indoor Air Quality in Residential and Commercial Buildings) | Ventilation rates, filter sizing, and ductwork cleanability for occupied spaces | Filter sizing requirements; minimum ventilation rates by zone; ASSUMPTION: ASHRAE 62.1 governs commercial/institutional zones in this facility; specific clause locations TBD |
| **ASHRAE 15** (Safety Standard for Refrigeration Systems) | Refrigerant system safety, service valve placement, pressure relief access | Refrigerant isolation valve accessibility; pressure relief device access; ASSUMPTION: applicable if mechanical cooling is selected |
| **CSA B139** (Installation Code for Oil-Burning Equipment) | Applicable if fuel oil heating is selected | Burner service access, nozzle and strainer accessibility; ASSUMPTION: may be superseded by natural gas codes if gas heating selected |
| **Alberta Building Code (ABC)** — current edition | HVAC, plumbing, and mechanical system design and installation | Section 6 (HVAC equipment spacing, ductwork dimensions, damper/control accessibility); Section 7 (plumbing); adopted with Alberta amendments; specific clause locations TBD at detailed design |
| **NFPA 110** (Standard for Emergency and Standby Power Systems) | Backup generator design, testing, and maintenance | Generator capacity verification, transfer switch testing intervals, annual load test requirements; specific clause locations TBD |
| **Alberta OH&S Regulations** (Occupational Health and Safety Act, Regulation, and Code) | Workplace safety for mechanical room access, equipment service, confined space entry (if applicable) | Lockout/tagout (LOTO) provisions; confined space procedures for sump entry; ASSUMPTION: applicable to contractor and Owner maintenance personnel |

**Note on Standards Accessibility:** Detailed clause-level requirements will be confirmed during the 60% Design Development phase. Requirements above reflect best-practice intent drawn from the RFP scope and decomposition. Specific code compliance details are TBD pending final mechanical system selections.

---

## Verification

| Req ID | Requirement (short) | Verification Method | Responsible Party | Timing |
|---|---|---|---|---|
| R-MEL-01 | Equipment access — service routes and aisle widths | Design review: mechanical room plan and equipment layouts confirm minimum 900 mm aisle widths; no access blockages; site walk-through at substantial performance | Mechanical Engineer; Commissioning Agent | 60% Design Development; substantial performance inspection |
| R-MEL-02 | Floor-level reach for routine maintenance | Design review: reach-distance measurements for filter racks, valve handles, and drain plugs confirmed on drawings | Mechanical Engineer | 60% Design Development |
| R-MEL-03 | HVAC filter accessibility and replacement intervals | Equipment schedule specifies filter type, size, and replacement interval by zone; design drawings show filter racks with indicator; commissioning confirms procedure with operations staff | Mechanical Engineer | 60% Design Development; pre-occupancy commissioning |
| R-MEL-04 | Apparatus bay exhaust — filter and damper access | Design detail confirmed; commissioning test verifies filter removal and isolation damper operation without system shutdown; procedure demonstrated to operations staff | Mechanical Engineer; Commissioning Agent | 60% Design Development; pre-occupancy commissioning |
| R-MEL-05 | Water fill station serviceability | Fill station schematic confirmed; commissioning verifies strainer basket removal, flushing procedure, and shutoff operation; annual procedure documented in O&M manual | Mechanical Engineer; Commissioning Agent | 60% Design Development; pre-occupancy commissioning |
| R-MEL-06 | Bay sump system accessibility | Sump pit design confirmed against geotech report; commissioning verifies pump removal access and manual backup provision | Mechanical Engineer | 60% Design Development; pre-occupancy commissioning |
| R-MEL-07 | Bunker gear room ventilation serviceability | Equipment specification confirms cartridge filter type; supplier availability confirmed; part number in spare parts inventory; room air balance demonstrated | Mechanical Engineer | 60% Design Development; pre-occupancy commissioning |
| R-MEL-08 | Generator service access and load testing | Generator site plan confirms all service clearances; load test provision documented; pre-occupancy baseline load test performed and documented | Mechanical Engineer; Commissioning Agent | 60% Design Development; pre-occupancy commissioning |
| R-MEL-09 | Standard modular parts selection | Equipment selection checklist documents justifications for all non-standard components; refrigerant type, valve types, pump models listed in equipment schedules | Mechanical Engineer | 60% Design Development |
| R-MEL-10 | Spare parts storage allocation | Mechanical room floor plan allocates dedicated shelving; spare parts list from equipment schedules; parts in stock confirmed at occupancy | Mechanical Engineer; Contractor | 60% Design Development; pre-occupancy |
| R-MEL-11 | Maintenance schedule framework | Maintenance schedule matrix created at Design Development; finalized in O&M manual delivered at occupancy permit; demonstrated to operations staff at training | Mechanical Engineer; Commissioning Agent | 60% Design Development; commissioning/training |
| R-MEL-12 | Lifecycle cost analysis | Narrative or worksheet documenting trade-offs for major equipment included in Mechanical Maintainability narrative or DEL-04-02; major equipment selections justified with payback or NPV estimates; acceptance criteria: minimum two alternatives per system, stated economic assumptions, and quantified payback or NPV | Mechanical Engineer | Concept/Design Brief phase |
| R-MEL-13 | Lockout/tagout (LOTO) provisions | Design review: LOTO points identified on mechanical drawings; LOTO procedure documented in O&M manual; hardware installed and labeled at each lockout point; verified during commissioning | Mechanical Engineer; Commissioning Agent | 60% Design Development; pre-occupancy commissioning |
| R-MEL-14 | Overhead door mechanical hardware maintainability | Design review: overhead door hardware maintainability provisions shown on door schedule and detail drawings; maintenance cycle documented in maintenance schedule matrix; spring adjustment, motor lubrication, and track cleaning access verified without scaffolding | Mechanical Engineer; Architect (DEL-05-01 coordination) | 60% Design Development; pre-occupancy commissioning |

---

## Documentation

**Anticipated Artifacts (from _CONTEXT.md):**

1. **Mechanical Maintainability Narrative** (primary artifact)
   - System-by-system maintainability strategy: HVAC, plumbing, fire protection, emergency power
   - Equipment access and clearance approach
   - Filter maintenance procedures and replacement schedules
   - Spare parts strategy and storage plan

2. **Maintenance Schedule Matrix** (tabular, embedded in narrative or as appendix)
   - All mechanical systems × maintenance interval (daily/weekly/monthly/quarterly/semi-annual/annual)
   - Task descriptions aligned to OEM and code requirements
   - Responsible party (Fire/PW operations staff vs. contracted specialist)

3. **Equipment Schedule Summary** (cross-reference or appendix)
   - HVAC, plumbing, fire protection, emergency power equipment
   - Modular component and spare parts notes per item

4. **Spare Parts Inventory List** (embedded in narrative or as appendix)
   - Consumables (1-year supply): filters, belts, seals, fluids
   - Major items (5-year cycle): impellers, bearings, valve cartridges

5. **Lifecycle Cost Analysis Summary** (narrative or appendix)
   - Equipment selection rationale for major systems
   - Trade-offs documented with 20-year NPV or simple payback estimates

**Cross-References to Coordination Documents:**

| Deliverable | Relationship |
|---|---|
| DEL-02-04 (Mechanical Concept Narrative) | Upstream — initial system selections define the maintainability approach addressed here |
| DEL-04-02 (Mechanical Energy and Solar Readiness) | Upstream — equipment selections and lifecycle implications for HVAC and water heating |
| DEL-05-01 (Architectural Durability) | Coordination — building finish and envelope choices impact mechanical equipment access |
| DEL-05-02 (Structural Durability) | Coordination — structural support provisions for mechanical equipment; sump pit design |
| DEL-05-04 (Electrical Maintainability) | Coordination — electrical panel access, controls serviceability, generator ATS accessibility |
| DEL-08-01 (Commissioning/Training/Closeout) | Downstream — O&M manual and staff training content derived from this narrative |
