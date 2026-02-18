# Mechanical Concept Narrative — Specification

**Deliverable ID:** DEL-02-04
**Package:** PKG-002 — Conceptual Design
**Type:** Design Specification (Normative)
**Last Updated:** 2026-02-17

---

## Scope

### What This Deliverable Covers

The Mechanical Concept Narrative provides the conceptual design for all mechanical systems in the Public Services Building and Cold Storage building, addressing:

1. **HVAC Systems** — heating, ventilation, and air-conditioning for all occupied zones (office, residential quarters, apparatus bays, shared spaces, Cold Storage); second-story shared spaces if architectural option is adopted per Addendum 03 §1.5
2. **Fire Apparatus Bay Direct Exhaust Ventilation** — dedicated exhaust for fire apparatus emissions per RFP §11.1.1 and Addendum 03 §1.12 (2 apparatus per bay)
3. **Public Works Bay General Ventilation** — general building ventilation for occasional vehicle idling and very occasional welding per Addendum 03 §1.11
4. **Bunker Gear Room Ventilation** — room-level dedicated ventilation per Addendum 03 §1.14
5. **Decontamination Room and Shower Plumbing** — hot/cold water supply, floor drains, sanitary drainage, and exhaust ventilation for decontamination room and showers per Addendum 03 §1.21
6. **SCBA Room Climate Control and Compressor Room Ventilation** — temperature-stabilized environment for SCBA cylinders; heat-rejection ventilation for SCBA compressor per Addendum 03 §1.21
7. **Plumbing Systems** — domestic water supply, distribution, hot water, sanitary drainage; including 2" water fill stations per Addendum 03 §1.16; dishwasher and laundry set connections per OSR §12.6
8. **Bay Sumps** — sump pit design and drainage for snow melting and minor washing in all bays per Addendum 03 §1.8
9. **Backup Generator System** — sizing and integration for minimum emergency loads per Addendum 03 §1.15
10. **Fire Protection System** — approach for building-wide fire suppression per code
11. **Kitchen Exhaust** — range hoods and makeup air per OSR §12.6 appliance list

### What This Deliverable Excludes

- Detailed mechanical design drawings (60% or 100% IFC drawings); concept narrative only
- Detailed equipment specifications and manufacturer data; TBD in design phase
- Exact ductwork routing, piping layouts, and schematics; to be developed during design
- Cross-discipline construction coordination details; resolved during design development
- Fire department vehicle fueling systems; not in mechanical scope per program
- Site servicing tie-in design (utility connections); cash allowance per Addendum 03 §1.7 permits exclusion from pricing
- Pickled Sand Storage building; removed from project scope per Addendum 03 §1.2 and constraint C-10
- Optional Built-In Wash Bay (OSR §12.1); priced as additional item only; not in base mechanical scope

---

## Requirements

All requirements are derived from the RFP, Addendum 03, and Owner Statement of Requirements. Requirements labeled **CONSTRAINT** are mandatory; **TARGET** are aspirational but strongly supported by RFP intent.

### Fire Apparatus Bay Direct Exhaust Ventilation

| Req ID | Requirement | Source | Type | Notes |
|---|---|---|---|---|
| **R-MEL-01** | Fire apparatus bays must have direct exhaust ventilation capable of capturing and removing apparatus emissions (diesel exhaust, particulates) from **2 apparatus per bay** during and after operation | RFP §11.1.1; Add 03 §1.12 | CONSTRAINT | Critical operational requirement; health and safety priority; quantified acceptance criterion for exhaust airflow rate (CFM per bay) TBD in design phase -- needed for verification pass/fail determination (Lensing A-005) |
| **R-MEL-02** | Exhaust system must be activated during apparatus presence via manual damper control or automatic control (door sensor, CO sensor, or timer); design approach TBD | RFP §11.1.1; Add 03 §1.12 (context) | CONSTRAINT | ASSUMPTION: some form of controlled damper operation required; exact control strategy TBD in design |
| **R-MEL-03** | Apparatus bay exhaust must be routed to roof or exterior wall; exhaust must not recirculate to occupied spaces | ASSUMPTION: Alberta Building Code + common fire hall code practice | CONSTRAINT | Ductwork design and routing TBD; must clear 16 ft overhead door height (Add 03 §1.10) |

### Public Works Bay General Ventilation

| Req ID | Requirement | Source | Type | Notes |
|---|---|---|---|---|
| **R-MEL-04** | Public Works equipment bays (PW bays) must have adequate general ventilation for occasional short-term vehicle idling | Add 03 §1.11 | CONSTRAINT | Quantified airflow rate target (air changes per hour) TBD in design; typically 4-8 ACH for vehicle bay; measurable acceptance criterion needed for verification (Lensing A-005) |
| **R-MEL-05** | PW bay ventilation must handle **very occasional welding** at a general building level; no dedicated welding extraction hood required | Add 03 §1.11 (explicit: "very occasional welding" + "no specific welding ventilation required") | CONSTRAINT | General dilution ventilation sufficient per Addendum 03 explicit language |

### Bunker Gear Room Ventilation

| Req ID | Requirement | Source | Type | Notes |
|---|---|---|---|---|
| **R-MEL-06** | Bunker gear storage room must have room-level ventilation (dedicated exhaust fan at room level) to address moisture management and odor control | Add 03 §1.14 | CONSTRAINT | Direct ventilation to each locker is NOT required; room-level ventilation is sufficient per Addendum 03 §1.14 explicit answer; quantified exhaust airflow rate (CFM or ACH) TBD in design phase (Lensing A-005) |
| **R-MEL-07** | Bunker gear room ventilation must exhaust to exterior (not recirculate to adjacent spaces) to prevent moisture and odor bleed-over | ASSUMPTION: code compliance + operational practice | CONSTRAINT | Local exhaust fan to exterior or roof |

### Decontamination Room and Shower Plumbing

| Req ID | Requirement | Source | Type | Notes |
|---|---|---|---|---|
| **R-MEL-08a** | Decontamination room (150–200 sf) must be provided with hot and cold water supply, floor drain(s) with trap(s), and sanitary drainage per code | Add 03 §1.21 (room sizing table); ASSUMPTION: Alberta Building Code plumbing requirements applicable | CONSTRAINT | Room size range from Addendum 03 §1.21; floor drain locations to be finalized with Architectural |
| **R-MEL-08b** | Decontamination showers/WR (50–60 sf x 2) must be provided with hot and cold water, shower fixtures, floor drain, and sanitary drainage per code | Add 03 §1.21; ASSUMPTION: Alberta Building Code plumbing requirements applicable | CONSTRAINT | Dedicated ventilation recommended to control moisture; exhaust to exterior |
| **R-MEL-08c** | Decontamination area exhaust ventilation must be dedicated to exterior to control moisture accumulation and prevent contaminated air recirculation to adjacent spaces | ASSUMPTION: Alberta Building Code + fire hall operational practice | CONSTRAINT | Exhaust fan to exterior or roof; separate from general HVAC return system; quantified ventilation rate (ACH) TBD in design phase (Lensing A-005) |

### Cold Storage Building Ventilation

| Req ID | Requirement | Source | Type | Notes |
|---|---|---|---|---|
| **R-MEL-09** | Cold Storage building must have adequate ventilation or alternate air circulation to prevent condensation and icing | RFP §11.1.2 | CONSTRAINT | Unheated building; passive or low-energy active ventilation acceptable. Measurable acceptance criterion TBD in design phase -- must define verifiable threshold (e.g., maximum interior relative humidity limit, or absence of visible condensation/ice formation on interior surfaces after 72-hour monitoring period in winter conditions) to enable pass/fail determination during commissioning and first-winter monitoring (Lensing X-003) |

### SCBA Room and Compressor Room

| Req ID | Requirement | Source | Type | Notes |
|---|---|---|---|---|
| **R-MEL-10a** | SCBA room (150–200 sf) must be maintained within an acceptable temperature range for SCBA cylinder storage | Add 03 §1.21; ASSUMPTION: SCBA cylinder manufacturers specify acceptable storage temperature ranges; fire department operational practice | CONSTRAINT | Acceptable temperature range TBD in design phase (confirm with fire department and manufacturer); minimum conditioned air supply required |
| **R-MEL-10b** | Compressor room (100–150 sf) must have adequate ventilation to remove heat generated by the SCBA compressor during operation; ventilation to exterior required | Add 03 §1.21; ASSUMPTION: compressor rooms require dedicated ventilation per mechanical code | CONSTRAINT | Ventilation sizing TBD in design phase; locate compressor room adjacent to exterior wall where possible |

### Heating, Cooling, and General HVAC

| Req ID | Requirement | Source | Type | Notes |
|---|---|---|---|---|
| **R-MEL-11** | All occupied zones (offices, residential quarters, kitchen, shared spaces) must be served by HVAC maintaining comfort conditions year-round per Alberta Building Code | RFP §11.1.1; Alberta Building Code (ASSUMPTION: applicable) | CONSTRAINT | If second story adopted (Add 03 §1.5), HVAC zoning must extend to upper floor |
| **R-MEL-12** | HVAC system must be designed to comply with National Energy Code of Canada (NECB) requirements for heating, cooling, and ventilation energy performance | ASSUMPTION: NECB applicable for this institutional building in Alberta | TARGET | Design phase energy modeling and code compliance verification required |
| **R-MEL-13** | Heating system should be high-efficiency (condensing boiler, heat pump, or equivalent) to achieve NECB energy targets | RFP energy and sustainability emphasis (OBJ-004); cold climate context; RFP §10.3.4 (practical, energy efficient, cost effective, easy to maintain) | TARGET | Specific system TBD in design development; energy modeling to confirm |

### Plumbing — Water Supply, Fill Stations, Hot Water, Appliances

| Req ID | Requirement | Source | Type | Notes |
|---|---|---|---|---|
| **R-MEL-14** | Two (2) water fill stations required: minimum 2" diameter, at **ground level**, one in the fire apparatus bay and one in the PW bay | Add 03 §1.16 | CONSTRAINT | CRITICAL; both must be ground level and minimum 2" diameter; female coupling standard (ASSUMPTION) |
| **R-MEL-15** | Municipal water service must include backflow prevention and pressure regulation at point of service entry | RFP §11.2; standard code (ASSUMPTION) | CONSTRAINT | Backflow preventer type per AHJ requirement TBD; note that domestic water service entry and fire protection service connection (R-MEL-26) may require different device types (e.g., RPZ typical for fire service connections, DCVA or PVB may suffice for domestic); confirm both service entries with AHJ (Lensing F-001) |
| **R-MEL-16** | Domestic hot water system must meet peak demand for kitchen, bathrooms, decontamination showers, dishwasher, and two laundry sets | RFP Functional Program (kitchen + bathrooms in program); OSR §12.6 (dishwasher + 2 laundry sets); Add 03 §1.21 (decontamination showers) | CONSTRAINT | Tankless or storage tank acceptable; sizing TBD in design; peak demand higher than base RFP implies due to laundry + decon showers |
| **R-MEL-17** | All water piping in exterior or unheated spaces must be protected from freeze-up via insulation, trace heating, or relocation to heated zones | ASSUMPTION: Alberta Building Code cold climate requirement | CONSTRAINT | Includes sump discharge piping, outdoor hose bibs, and any exposed pipe |

### Plumbing — Sanitary Drainage and Bay Sumps

| Req ID | Requirement | Source | Type | Notes |
|---|---|---|---|---|
| **R-MEL-18** | All bays (apparatus bays and PW bays) must have floor sump pits for snow melting and minor washing drainage | Add 03 §1.8 | CONSTRAINT | Sump pit location, dimensions, and coordination with floor slab design TBD |
| **R-MEL-19** | Sump pits must be served by submersible pump(s) discharging to daylight discharge, percolation-infiltration field, or municipal sanitary sewer (discharge routing TBD based on civil and site conditions) | Add 03 §1.8; RFP §11.2 context | CONSTRAINT | Discharge routing requires civil coordination; freeze protection of discharge line required. Terminology normalized per Lensing E-002 |
| **R-MEL-20** | Building sanitary drainage must ensure positive drainage of condensation within wall construction and water entering at joints, directing it to exterior face per RFP §11.2 | RFP §11.2 | CONSTRAINT | No storm sewer on site; efficient roof drainage away from building to natural drainage off site |

### Backup Generator System

| Req ID | Requirement | Source | Type | Notes |
|---|---|---|---|---|
| **R-MEL-21** | Backup generator required; minimum loads to be supported: kitchen, ICP/meeting room, 2 bathrooms | Add 03 §1.15 | CONSTRAINT | CRITICAL; these three loads are explicitly specified as minimums |
| **R-MEL-22** | Bay doors require secondary opening mechanism; either generator-powered opener OR manual override; Design-Builder chooses approach | Add 03 §1.15 | CONSTRAINT | Bay door secondary opening is an explicit requirement; method is Design-Builder's choice |
| **R-MEL-23** | Generator must include automatic transfer switch (ATS) to provide seamless power switchover during utility grid outage | ASSUMPTION: standard practice for emergency power systems | CONSTRAINT | Coordinate generator specs with Electrical (DEL-02-05); transfer switchover time TBD |
| **R-MEL-24** | Generator capacity estimated at 25–30 kW (ASSUMPTION pending detailed load calculation); fuel type natural gas preferred (municipal gas within few feet of site) | Add 03 §1.15; Add 03 §1.6 (gas service available); ASSUMPTION | TARGET | Detailed load calculation required in design phase with Electrical; generator size may change |

### Fire Protection System

| Req ID | Requirement | Source | Type | Notes |
|---|---|---|---|---|
| **R-MEL-25** | Building-wide fire protection system (wet or dry sprinkler) required per Alberta Building Code for this institutional occupancy | ASSUMPTION: Alberta Building Code (applicable) | CONSTRAINT | System type (wet vs. dry) TBD in design; confirmed in Functional Program row 12.0 (Mechanical/sprinkler room) |
| **R-MEL-26** | Fire protection system must connect to municipal water supply with check valve and backflow prevention | RFP §11.2; standard code | CONSTRAINT | System design and AHJ approval required before construction |
| **R-MEL-27** | Fire protection system design must be reviewed and approved by the Authority Having Jurisdiction (AHJ) prior to construction; AHJ pre-consultation should be initiated during concept or early design phase to confirm wet vs. dry sprinkler preference for apparatus bays before detailed design proceeds (Lensing A-003) | RFP §7.2; standard code | CONSTRAINT | AHJ approval is permit prerequisite; early AHJ engagement at concept stage reduces risk of late-stage fire protection redesign |

### Kitchen Exhaust

| Req ID | Requirement | Source | Type | Notes |
|---|---|---|---|---|
| **R-MEL-28** | Kitchen must be equipped with range hoods over all cooking appliances (stove/oven with range hoods) with code-required makeup air | OSR §12.6 (appliance list: stove and oven with range hoods); ASSUMPTION: Alberta Building Code kitchen exhaust requirement | CONSTRAINT | Appliance list confirmed: stove, oven, 2 refrigerators with freezers, 2 microwaves, dishwasher, 2 laundry sets |

### Integration and Coordination

| Req ID | Requirement | Source | Type | Notes |
|---|---|---|---|---|
| **R-MEL-29** | Apparatus bay exhaust ductwork must clear the 16 ft minimum overhead door height; routing must not interfere with door operation or apparatus clearance | Add 03 §1.10 (door height); coordination requirement | CONSTRAINT | Confirms with Architectural (DEL-02-01) that adequate ceiling/truss height exists |
| **R-MEL-30** | Bay sump pits must coordinate with structural slab design for penetration locations, drainage slope, and structural continuity | DEL-02-03 (Structural Concept); Add 03 §1.8 | CONSTRAINT | Sump location TBD; Structural provides opening; Mechanical provides liner and pump |
| **R-MEL-31** | Generator electrical output specifications (capacity, voltage, phase, fuel type) must be provided to Electrical (DEL-02-05) for ATS and distribution panel design | Add 03 §1.15; coordination requirement | CONSTRAINT | Generator and ATS specifications must be aligned between Mechanical and Electrical |
| **R-MEL-32** | Decontamination room floor drain penetration must be coordinated with Structural slab design for penetration location, trap sizing, and structural continuity | Add 03 §1.21; coordination requirement | CONSTRAINT | Drain location finalized with Architectural and Structural; Mechanical provides drain specification |

---

## Standards

### Applicable Building Codes and Standards

| Standard / Code | Applicability | Status |
|---|---|---|
| **Alberta Building Code (ABC)** | All mechanical systems; primary design authority for Penhold, Alberta jurisdiction; edition TBD -- confirm whether ABC 2019 or ABC 2023 applies (Lensing A-001) | ASSUMPTION: applicable; edition and detailed requirements TBD -- location TBD |
| **National Energy Code of Canada (NECB)** | HVAC and ventilation energy performance; supports OBJ-004 energy goals; edition TBD -- confirm whether NECB 2017 or NECB 2020 is adopted in Alberta (Lensing A-001) | ASSUMPTION: applicable; energy modeling TBD |
| **Alberta Plumbing Code** | All plumbing installations (domestic water supply, sanitary drainage, sump discharge, decontamination plumbing, water fill stations); jurisdictional plumbing code governing installation practice for R-MEL-08a, R-MEL-08b, R-MEL-15, R-MEL-18 (Lensing E-001) | ASSUMPTION: applicable; full text not accessed at concept stage -- location TBD |
| **NFPA 13 (or equivalent Canadian standard adopted in Alberta)** | Fire protection sprinkler system design standard; applicable to R-MEL-25, R-MEL-26, R-MEL-27 (Lensing C-001) | ASSUMPTION: applicable; confirm which fire protection design standard is adopted in Alberta jurisdiction -- location TBD |
| **Canadian Standards Association (CSA) Standards** | Plumbing (CSA B125 series), HVAC equipment, boilers and pressure vessels | ASSUMPTION: applicable; TBD |
| **ASME / ULC Standards** | Pressure vessels, backflow prevention, fire sprinkler systems | ASSUMPTION: applicable; TBD |
| **Town of Penhold Bylaws** | Utility connection requirements, noise, discharge permits; generator noise and exhaust emissions constraints to be confirmed -- outdoor generator has noise implications for adjacent properties (Lensing C-002) | TBD in design phase; confirm noise bylaw limits and emissions requirements applicable to standby generator operation |
| **RFP §11 Mechanical Systems (Owner Statement of Requirements)** | Owner-stated mechanical requirements; governs over general practice where explicit | Accessible; cited throughout |
| **RFP §11.3 Materials Standard** | Buildings must feature watertight, non-combustible construction; durable, flexible materials for longevity and easy maintenance; applies to all mechanical system selections | RFP §11.3, page 44 |

**Note:** Full text of codes and standards other than RFP not accessible at concept phase. Detailed design phase will conduct comprehensive code compliance review.

---

## Verification

### Requirements Verification Matrix

| Req ID(s) | Requirement Summary | Verification Method | Phase | Responsible Party |
|---|---|---|---|---|
| **R-MEL-01, -02, -03** | Apparatus bay direct exhaust | (1) Exhaust ductwork drawing review; (2) Fan and damper shop drawing review; (3) Commissioning: damper operation test and exhaust performance test | Design → Construction → Commissioning | Mechanical Consultant + Commissioning Agent |
| **R-MEL-04, -05** | PW bay general ventilation | (1) Ventilation design drawing review; (2) Air change rate calculation review; (3) Commissioning air balance test | Design → Commissioning | Mechanical Consultant + Commissioning Agent |
| **R-MEL-06, -07** | Bunker gear room ventilation | (1) Exhaust fan location drawing review; (2) Separate exhaust path confirmed; (3) Commissioning moisture check | Design → Commissioning | Mechanical Consultant + Commissioning Agent |
| **R-MEL-08a, -08b, -08c** | Decontamination room / shower plumbing and ventilation | (1) Plumbing design drawing review (hot/cold water, drains confirmed); (2) Exhaust fan to exterior confirmed; (3) Pressure test and commissioning flow check | Design → Construction → Commissioning | Mechanical/Plumbing Consultant + Inspector + Commissioning Agent |
| **R-MEL-09** | Cold Storage ventilation | (1) Ventilation opening design review; (2) Site inspection confirming opening installation; (3) Condensation/icing monitoring first winter against defined acceptance criterion (e.g., no visible condensation/ice on interior surfaces after 72-hour winter monitoring period, or maximum interior RH threshold -- criterion TBD in design phase per Lensing X-003) | Design → Construction → Post-Occupancy | Mechanical Consultant + Owner |
| **R-MEL-10a, -10b** | SCBA room climate + compressor room ventilation | (1) HVAC zoning drawing confirming conditioned supply to SCBA room; (2) Compressor room exhaust fan confirmed; (3) Commissioning temperature check in SCBA room during winter and summer | Design → Commissioning | Mechanical Consultant + Commissioning Agent |
| **R-MEL-11, -12, -13** | HVAC system and energy compliance | (1) HVAC design drawing and energy model review; (2) Code compliance narrative at 60% design; (3) Commissioning testing and air balancing | Design → Commissioning | Mechanical Consultant + Building Science + Commissioning Agent |
| **R-MEL-14** | Water fill stations | (1) Confirm 2" minimum diameter measurement at each station; (2) Confirm ground-level installation; (3) Flow rate test at each station; (4) Female coupling connection test (Lensing X-001) | Design → Construction → Commissioning | Mechanical/Plumbing Consultant + Inspector + Commissioning Agent |
| **R-MEL-15, -16** | Water supply, hot water, appliance connections | (1) Plumbing design drawing review (hot water sizing covers all loads including simultaneous laundry + decontamination + kitchen demand); (2) Pressure test; (3) Backflow prevention device certification for both domestic and fire service entries; (4) Laundry set and dishwasher hot/cold water supply, drain connections verified (Lensing X-002) | Design → Construction → Commissioning | Mechanical/Plumbing Consultant + Inspector + Commissioning Agent |
| **R-MEL-17** | Freeze protection of water piping | (1) Plumbing design drawing review confirming freeze protection strategy; (2) Commissioning: freeze-protection inspection of all piping in exterior walls, unheated spaces, and sump discharge lines before first winter operation; (3) Verify trace heating (if used) is operational and alarmed (Lensing F-002) | Design → Construction → Commissioning (pre-winter) | Mechanical/Plumbing Consultant + Inspector + Commissioning Agent |
| **R-MEL-18, -19, -20** | Bay sumps and drainage | (1) Sump pit design reviewed; (2) Structural coordination confirmed; (3) Drainage discharge route permitted; (4) Sump pump operation tested during commissioning | Design → Construction → Commissioning | Mechanical + Structural + Civil Consultant + Commissioning Agent |
| **R-MEL-21, -22, -23, -24** | Backup generator | (1) Load calculation and generator sizing review; (2) Bay door secondary mechanism design reviewed; (3) ATS design and generator specs coordinated with Electrical; (4) Commissioning: load bank test, ATS switchover test, bay door secondary test | Design → Construction → Commissioning | Mechanical + Electrical Consultant + Commissioning Agent |
| **R-MEL-25, -26, -27** | Fire protection system | (1) Design drawings reviewed for code compliance; (2) AHJ plan review and approval; (3) Hydrostatic pressure test; (4) Final system test; (5) AHJ final sign-off | Design → Permits → Construction → Commissioning | Mechanical/Fire Protection Consultant + AHJ + Inspector |
| **R-MEL-28** | Kitchen range hoods | (1) Range hood design reviewed (capacity, makeup air); (2) Site inspection confirming installation; (3) Commissioning airflow test | Design → Construction → Commissioning | Mechanical Consultant + Inspector |
| **R-MEL-29, -30, -31, -32** | Cross-discipline integration | (1) Cross-discipline coordination drawing review; (2) Clash detection / coordination meetings; (3) Site inspection for correct rough-in; (4) Commissioning verification of interfaces | Design (ongoing) → Construction | All disciplines + PM |

---

## Documentation

### Deliverable Artifacts

| Artifact | Description | Format | Timing |
|---|---|---|---|
| **Mechanical Concept Narrative** | Main narrative covering all mechanical systems; this document | Markdown (.md) / Word (.docx) + PDF | Proposal submission (RFP response) |
| **System Selection Rationale** | Preliminary system selections (HVAC approach, exhaust strategy, generator estimate) | Embedded in narrative | Proposal submission |
| **Cross-Discipline Interface Summary** | Interface assumptions with Architectural, Structural, Electrical, Civil | Embedded in narrative | Proposal submission |
| **Concept Drawings** | Mechanical schematic and system diagrams; NOT required at concept stage | AutoCAD .dwg / PDF | Deferred to design development (DEL-06-02) |

### References to Other Deliverables

The Mechanical Concept Narrative references and is informed by:

- **DEL-02-01** (Architectural Concept) — building layout, room dimensions, door heights, roof orientation; second-story adoption decision
- **DEL-02-02** (Civil/Site Concept) — site drainage, utility entry points, sump discharge routing
- **DEL-02-03** (Structural Concept) — slab design for sump pit and decontamination drain coordination, structural system
- **DEL-02-05** (Electrical/IT Concept) — generator electrical connection and ATS; backup power load list
- **DEL-04-02** (Mechanical Energy and Solar Readiness) — PKG-004 scope; detailed energy strategy and solar-ready provisions
- **DEL-05-03** (Mechanical Maintainability) — PKG-005 scope; operational and maintenance design rationale

---

## Conflicts

### Conflict Table (for human ruling)

All mechanical requirements from RFP §11, Addendum 03, and OSR are consistent with each other and with standard fire hall/public works design practice except for the generator sizing range noted below. Additional contradictions, if identified during design development, will be recorded here for human resolution.

| Conflict ID | Conflict | Source A | Source B | Impacted Sections | Proposed Authority | Human Ruling |
|---|---|---|---|---|---|---|
| CON-001 | Generator capacity range varies across documents: Datasheet states "25-30 kW (ASSUMPTION)"; Specification R-MEL-24 states "25-30 kW"; Guidance EX-002 calculates design load at 16,000-25,000 W and recommends "25 kW unit as concept baseline"; Guidance C-002 Option 1 states "~20-25 kW" for minimum loads. While ranges overlap, they are not identical and could cause confusion in design phase load calculations. (Lensing B-003) | Datasheet > Construction > Backup Generator; Specification R-MEL-24 | Guidance C-002 (20-25 kW minimum); Guidance EX-002 (25 kW baseline) | Specification R-MEL-24; Datasheet Construction; Guidance C-002, EX-002 | Specification (PROPOSAL: reconcile all documents to a single stated range after detailed load calculation in design phase) | TBD |

---

**End of Specification**
