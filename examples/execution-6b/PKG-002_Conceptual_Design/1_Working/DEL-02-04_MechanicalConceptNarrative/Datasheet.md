# Mechanical Concept Narrative — Datasheet

**Deliverable ID:** DEL-02-04
**Package:** PKG-002 — Conceptual Design
**Discipline:** Mechanical Engineering
**Type:** Design / Narrative
**Responsible Party:** Mechanical Engineer
**Last Updated:** 2026-02-17

---

## Identification

| Field | Value |
|---|---|
| **Deliverable Name** | Mechanical Concept Narrative |
| **Project** | Town of Penhold — Public Services Building (RFP 2024_004) |
| **Building Type** | Combined Fire Hall + Public Works Operations + Shared Spaces + Cold Storage building |
| **Site** | 12-acre developable site, Lot 1, Block 1, Plan 212 1668, Waskasoo Avenue North, Penhold, Alberta |
| **Deliverable Type** | Design Narrative (concept-stage) |
| **Primary Artifact** | Mechanical concept narrative document |
| **Scope Items Covered** | SOW-0009, SOW-0010 |
| **Objective Supported** | OBJ-003 (Proposed Conceptual Design, 20 pts) |
| **Status** | INITIALIZED |

---

## Attributes

### Scope of Mechanical Systems

| System | Coverage | Status |
|---|---|---|
| **HVAC (Heating, Ventilation, Air-Conditioning)** | All occupied zones: office areas, residential quarters, apparatus bays, shared spaces (kitchen, ICP/meeting room, bathrooms); second-story shared spaces if adopted (Addendum 03 §1.5) | Primary responsibility |
| **Fire Apparatus Bay Direct Exhaust Ventilation** | 2 apparatus per bay; dedicated tailpipe-capture exhaust per RFP §11.1.1 and Addendum 03 §1.12 | REQUIRED |
| **Public Works Bay General Ventilation** | Occasional short-term vehicle idling + very occasional welding; general building ventilation (no dedicated welding hood) per Addendum 03 §1.11 | REQUIRED |
| **Bunker Gear Room Ventilation** | Room-level ventilation for 40 bunker gear lockers per Addendum 03 §1.14 | REQUIRED |
| **Decontamination Room / Shower Plumbing** | Hot and cold water supply, floor drain, and sanitary drainage for decontamination room (150–200 sf) and decontamination showers/WR (50–60 sf x2) per Addendum 03 §1.21 | REQUIRED |
| **SCBA Room Climate Control** | Temperature-stabilized storage environment for SCBA cylinders (100–150 sf compressor room + 150–200 sf SCBA room per Addendum 03 §1.21); compressor heat removal ventilation | REQUIRED |
| **Cold Storage Building Ventilation** | Adequate ventilation or alternate air circulation to prevent condensation and icing per RFP §11.1.2 | REQUIRED |
| **Plumbing (Domestic Water Supply & Distribution)** | All fixtures; includes 2" water fill stations per Addendum 03 §1.16; dishwasher and laundry sets per OSR §12.6 | Primary responsibility |
| **Bay Sumps** | Snow melting and minor washing in all bays per Addendum 03 §1.8; structural coordination required | REQUIRED |
| **Backup Generator System** | Minimum loads: kitchen, ICP/meeting room, 2 bathrooms, bay door secondary opening per Addendum 03 §1.15 | REQUIRED |
| **Fire Protection System** | Building-wide approach; type, coverage, activation; code compliance per Alberta Building Code | REQUIRED per code |
| **Kitchen Exhaust (Range Hoods)** | Range hoods over stove/oven per OSR §12.6; makeup air per code | REQUIRED per code |
| **Domestic Hot Water** | Supply and distribution for bathrooms, kitchen, cleaning areas, decontamination showers, dishwasher, laundry sets per OSR §12.6 and Addendum 03 §1.21 | Primary responsibility |

### Building Zones Requiring Mechanical Design

**Terminology note:** "PW bays" is the canonical short form for Public Works Equipment Bays (also referred to as "Workshop/Storage Bay" in Addendum 03 §1.21 and Functional Program row 28.0). See Guidance Terminology Note (Lensing X-004) for full normalization register.

**Room size data note (Lensing B-002):** Several zones below list size as "TBD (Functional Program row X.0)." These TBD values must be obtained from the Functional Program (Appendix B) or confirmed with the Architectural concept (DEL-02-01) before HVAC sizing and load calculations can proceed in design phase. Without confirmed room sizes, HVAC zone sizing, hot water demand, generator load estimates, and range hood makeup air calculations cannot be finalized.

| Zone | Approx. Size | Mechanical Priority | Source |
|---|---|---|---|
| **Fire Apparatus Bays** | 2,000–2,200 sf each | Direct exhaust ventilation, sump, fill station | RFP §11.1.1; Add 03 §1.12, §1.8, §1.16 |
| **Public Works Equipment Bays (PW bays)** | 2,000–2,200 sf each | General ventilation, sump, fill station | Add 03 §1.11, §1.8, §1.16, §1.21 |
| **Bunker Gear Storage Room (Fire Gear Storage)** | 200–350 sf | Room-level exhaust ventilation | Add 03 §1.14, §1.21 |
| **Decontamination Room** | 150–200 sf | Hot/cold water supply, floor drain, sanitary drainage | Add 03 §1.21 |
| **Decontamination Shower / WR** | 50–60 sf x2 | Hot/cold water, drainage, ventilation | Add 03 §1.21 |
| **SCBA Room** | 150–200 sf | Climate-controlled storage; temperature stability for cylinders | Add 03 §1.21 |
| **Compressor Room** | 100–150 sf | Ventilation for heat rejection from SCBA compressor | Add 03 §1.21 |
| **Kitchen** | TBD (Functional Program row 16.0) -- room size needed for HVAC sizing and range hood makeup air calculation | Range hood, domestic hot water, dishwasher drain, generator load | OSR §12.6; Add 03 §1.15 |
| **ICP / Meeting Room** | TBD (Functional Program row 19.0) -- room size needed for HVAC sizing and generator load estimate | HVAC, generator load (minimum specified) | Add 03 §1.15 |
| **2 Bathrooms (Generator Load)** | TBD -- room sizes needed for HVAC sizing and generator load estimate | HVAC, plumbing, generator load (minimum specified) | Add 03 §1.15 |
| **Office Areas** | TBD -- room sizes needed for HVAC zone sizing | Standard commercial HVAC | RFP §11.1.1 |
| **Residential Quarters** | TBD -- room sizes needed for HVAC zone sizing and laundry hot water demand | Sleeping quarters HVAC; laundry hot water/drainage | RFP §11.1.1; OSR §12.6 |
| **Mechanical/Sprinkler Room** | TBD (Functional Program row 12.0) | Equipment location; sprinkler system central connection | Functional Program row 12.0 |
| **Cold Storage Building** | 60 ft x 100 ft (6,000 sf) | Condensation/icing prevention ventilation | RFP §11.1.2 |

### Confirmed Addendum 03 Requirements (Mechanical Scope)

All of the following are mandatory and must be embedded in the mechanical concept:

| Requirement | Addendum 03 Reference | Notes |
|---|---|---|
| Bay sumps (snow melt + minor washing) — all bays | §1.8 | Structural coordination required (slab penetrations) |
| Fire apparatus bay: direct exhaust, 2 apparatus per bay | §1.12 | Also confirmed in RFP §11.1.1 |
| PW bay: general ventilation (occasional idling + very occasional welding) | §1.11 | No dedicated welding hood required |
| Bunker gear room: room-level ventilation (not per-locker) | §1.14 | 40 lockers per §1.13 |
| Backup generator: kitchen, ICP/meeting room, 2 bathrooms, bay door secondary opening | §1.15 | Bay door: generator power OR manual override (Design-Builder chooses) |
| Water fill stations: 2" minimum, ground level — 1 fire bay, 1 PW bay | §1.16 | Female couplings; ground level; both bays |
| Room sizing table (multiple rooms with mechanical implications) | §1.21 | Decontamination room/shower, SCBA room, compressor room, fire gear storage, apparatus bays all sized per table |

---

## Conditions

### Environmental and Operational Constraints

| Constraint | Impact on Mechanical Design | Source |
|---|---|---|
| **Cold Climate (Penhold, Alberta)** | Heating load dominance; freeze-thaw risk for water piping and sumps; energy recovery ventilation valuable | Geography; Alberta Building Code |
| **Fire Department 24/7 Operations** | Bay exhaust must handle periodic high-load events; generator must be reliable at all times | RFP §11.1.1; Add 03 §1.15 |
| **Public Works Vehicle Idling** | Short-term exhaust gas and fume generation in PW bays; general ventilation adequate | Add 03 §1.11 |
| **Apparatus Bay Thermal Dynamics** | Frequent 16 ft door opening causes large thermal loss; HVAC must compensate; freeze protection required for wet sprinkler if applicable | Add 03 §1.10 (doors) |
| **Bunker Gear Moisture Management** | Wet gear stored in lockers; moisture accumulation is mold/degradation risk; ventilation is mitigation | Add 03 §1.14; common fire hall operations practice |
| **Decontamination Requirements** | Dedicated decontamination room and showers require hot water and drainage; water temperature and drainage code compliance | Add 03 §1.21 |
| **SCBA Cylinder Temperature Sensitivity** | SCBA cylinders require storage within an acceptable temperature range; compressor heat must be managed | Add 03 §1.21; common fire hall practice (ASSUMPTION: temperature stability required) |
| **Cold Storage Unheated** | Freeze-thaw cycling throughout year; condensation and icing are primary risks; no active heating planned (ASSUMPTION) | RFP §11.1.2 |
| **Second-Story Option** | Mechanical HVAC zoning must accommodate second-story shared spaces if architectural design adopts this option | Add 03 §1.5 |
| **Site Utilities** | Water and wastewater stubbed at site corner; gas, electrical, communications within a few feet of site | Add 03 §1.6 |
| **Plumbing Drainage** | No storm sewer on site; efficient roof drainage to natural drainage off site required | RFP §11.2 |
| **Geotechnical Basis** | 2021 geotechnical report (Appendix D) is design basis; no additional investigation planned per DEC-013 | Decomposition v2.3, DEC-013 |
| **Materials Standard** | Buildings must comply with all building code requirements: watertight, non-combustible construction; durable, flexible materials for longevity and easy maintenance | RFP §11.3 |

### Reference Design Standards and Codes

| Standard / Code | Applicability | Status |
|---|---|---|
| **Alberta Building Code (ABC)** | All mechanical systems; primary authority for Penhold, Alberta jurisdiction | ASSUMPTION: applicable; full text not accessed at concept stage — location TBD |
| **National Energy Code of Canada (NECB)** | HVAC, ventilation energy performance | ASSUMPTION: applicable; TBD in design phase |
| **Alberta Plumbing Code** | All plumbing installations (domestic water, sanitary drainage, sump discharge, decontamination plumbing); jurisdictional plumbing code governing installation practice (Lensing E-001) | ASSUMPTION: applicable; full text not accessed at concept stage -- location TBD |
| **Canadian Standards Association (CSA) Standards** | Plumbing (CSA B125 series), boiler and pressure vessel | ASSUMPTION: applicable; TBD |
| **ASME / ULC Standards** | Pressure vessels, fire sprinkler systems | ASSUMPTION: applicable; TBD |
| **Town of Penhold Bylaws** | Utility connections, noise, emissions | TBD in design phase |

---

## Construction

### Anticipated Mechanical System Selections (Concept Level)

All preliminary selections below are **ASSUMPTION** (concept stage; final selection in design development).

| System | Component | Preliminary Concept Approach | Source Basis |
|---|---|---|---|
| **Heating Plant** | Main heating | High-efficiency condensing boiler OR heat pump (TBD); sized for Penhold winter design temperature | Alberta cold climate + NECB energy targets |
| **Cooling** | Cooling plant | TBD; distributed split-system units or central chilled water (small system likely) | Design development |
| **Ventilation — Offices/Residential** | Air handling | Energy recovery ventilator (ERV/HRV); standard commercial supply/return | Cold climate best practice |
| **Fire Apparatus Bay Exhaust** | Dedicated exhaust fan | 10,000–15,000 CFM exhaust fan(s) per bay; damper control; tailpipe capture connection stubs; makeup air via high-performance louver | RFP §11.1.1; Add 03 §1.12 |
| **PW Bay Ventilation** | General ventilation | Roof-mounted or wall exhaust fan(s); sized for occasional vehicle idling and welding fumes; no dedicated hood | Add 03 §1.11 |
| **Bunker Gear Room** | Local exhaust | Dedicated wall or roof-mounted exhaust fan; intake via louvered vent or return air path | Add 03 §1.14 |
| **Decontamination Room / Shower** | Plumbing fixtures + ventilation | Hot and cold water supply piping; floor drain with trap; sanitary stack; dedicated exhaust fan (moisture + contaminant control) | Add 03 §1.21 |
| **SCBA Room** | Climate control | Conditioned air supply from main HVAC; temperature maintenance within acceptable cylinder storage range; no extreme temperature swings | Add 03 §1.21; ASSUMPTION: temperature stability required |
| **Compressor Room** | Ventilation | Dedicated ventilation for heat rejection from SCBA compressor; wall or roof exhaust fan | Add 03 §1.21 |
| **Cold Storage Ventilation** | Passive or mechanical | Ventilation openings or ceiling fans; no active heating (ASSUMPTION); sized to prevent condensation and icing; concept approach TBD -- must determine whether passive ridge/soffit ventilation, ceiling fans, or mechanical exhaust is the baseline (see Guidance for ventilation approach considerations) (Lensing A-004) | RFP §11.1.2 |
| **Domestic Water Supply** | Municipal service | Pressure regulation and backflow prevention at service entry | Add 03 §1.6; RFP §11.2 |
| **Water Fill Stations** | 2" female coupling | Ground-level connection in fire apparatus bay and PW bay; both 2" minimum diameter | Add 03 §1.16 |
| **Domestic Hot Water** | Water heater | Tankless or small storage tank; sized for peak demand (kitchen + bathrooms + decontamination showers + dishwasher + laundry sets) | OSR §12.6; Add 03 §1.21 |
| **Sanitary Drainage** | Gravity drainage | Main stack(s) to municipal sewer; roof vents per code; decontamination room drain; kitchen dishwasher drain; laundry set drain | RFP §11.2; OSR §12.6; Add 03 §1.21 |
| **Bay Sumps** | Sump pit + pump | Floor sump pits; submersible pump(s); discharge to daylight discharge, percolation-infiltration field, or municipal sanitary sewer (TBD per civil) | Add 03 §1.8 |
| **Backup Generator** | Diesel or natural gas standby | Outdoor pad-mounted (ASSUMPTION: consistent with Functional Program row 30.0); min. 25–30 kW (ASSUMPTION pending load calc); ATS | Add 03 §1.15; Functional Program row 30.0 |
| **Fire Protection** | Wet or dry sprinkler | Type TBD (wet preferred if bay thermal control reliable; dry if not); municipal water supply connection | Alberta Building Code; Functional Program row 12.0 |
| **Kitchen Exhaust** | Range hoods | Over stove/oven with range hoods per appliance list; code-required makeup air | OSR §12.6 |

### Design Integration Points

| Interface | Disciplines | Coordination Notes |
|---|---|---|
| **Apparatus bay exhaust above 16 ft doors** | Mechanical + Architectural + Structural | Ductwork routing above 16 ft door clearance; confirm ceiling/truss height allows mechanical routing |
| **Bay sump pits** | Mechanical + Structural + Civil | Floor slab penetrations; drainage routing; sump discharge to civil drainage strategy |
| **Generator electrical connection** | Mechanical + Electrical (DEL-02-05) | Generator output specs (kW, voltage, phase) to Electrical; ATS design |
| **SCBA compressor room heat rejection** | Mechanical + Architectural | Compressor room ventilation to exterior; locate compressor room adjacent to exterior wall where possible |
| **Decontamination room rough-in** | Mechanical + Architectural + Structural | Floor drain location finalized with Architectural; structural slab opening for drain |
| **Solar-ready roof provisions** | Mechanical + Electrical + Architectural | Mechanical HVAC clearance; Electrical conduit rough-in; structural loading |
| **Second-story HVAC zoning** | Mechanical + Architectural | If second story adopted, HVAC zoning and ductwork routing to upper floor must be confirmed with Architectural layout |
| **Building envelope thermal performance** | Mechanical + Architectural | HVAC sizing depends on envelope R-value; coordinate insulation and air sealing approach |
| **Cold Storage ventilation openings** | Mechanical + Architectural | Location and sizing of ventilation openings; screened to prevent pest entry |

---

## References

### Primary Sources

| Source | Section / Page | Relevance |
|---|---|---|
| RFP 2024_004 (Jul 10, 2024) | §11 Mechanical Systems (§11.1.1, §11.1.2, §11.2, §11.3); §10.3.4 (design requirements); §7.1.1 (Proposed Conceptual Design) | Primary mechanical requirements; materials standard |
| Addendum 03 (Jul 31, 2024) | §1.8 (sumps); §1.11 (PW bay ventilation); §1.12 (fire apparatus exhaust); §1.13 (bunker gear lockers); §1.14 (bunker gear room ventilation); §1.15 (backup generator); §1.16 (water fill stations); §1.21 (room sizing table) | Critical clarifications governing mechanical scope; room size ranges with mechanical implications |
| RFP Appendix B — Functional Program | Rows 1.0–2.0 (Apparatus Bays); row 12.0 (Mech/sprinkler room); row 16.0 (Kitchen); row 19.0 (Training/ICP); row 28.0 (Workshop/Storage Bay); row 30.0 (Generator) | Space-by-space equipment and power requirements |
| OSR §12.6 Appliances (RFP page 45) | Appliance list: 2 refrigerators with freezers, 2 microwaves, stove and oven with range hoods, dishwasher, 2 laundry sets | Kitchen and laundry plumbing loads; range hood requirement |
| Penhold_PSB_Project_Decomposition_v2.md | DEL-02-04; PKG-002; §4 Addenda Integration Summary; DEC-013 | Deliverable context; no additional geotechnical investigation |

### Cross-Referenced Deliverables

| Deliverable | Purpose |
|---|---|
| DEL-02-01 (Architectural Concept Package) | Building layout, room dimensions, door heights, roof orientation — mechanical zones must fit |
| DEL-02-02 (Civil/Site Concept Plan) | Site grading, drainage, utility entry — sump discharge routing |
| DEL-02-03 (Structural Concept Narrative) | Slab design for sump pit and decontamination drain coordination; structural provisions |
| DEL-02-05 (Electrical/IT Concept Narrative) | Generator transfer switching coordination; electrical power to mechanical equipment |
| DEL-04-02 (Mechanical Energy and Solar Readiness) | Detailed energy efficiency strategy and solar-ready provisions (PKG-004 scope) |
| DEL-05-03 (Mechanical Maintainability) | Operational and maintenance design rationale (PKG-005 scope) |

---

## TBD Summary

| Item | Why TBD | Resolution Path |
|---|---|---|
| Final HVAC system selection (boiler vs. heat pump) | Multiple viable technologies; energy modeling required | Design development; energy modeling and cost-benefit analysis |
| Generator capacity (kW) and fuel type | Load calculation requires finalized electrical load list | Detailed load analysis; coordinate with Electrical (DEL-02-05) |
| Bay sump discharge routing | Depends on site grading and municipal sewer availability | Civil design to confirm; mechanical to size pumps |
| Fire protection system type (wet vs. dry) | Depends on bay thermal conditioning reliability and AHJ preference | Design phase code review and AHJ consultation |
| Bunker gear room ventilation airflow rate | Exact rate depends on room dimensions and locker count from architecture | Design phase coordination with architectural layout |
| Water fill station pressure and flow requirements | Fire department operational requirements not specified beyond "2" minimum" | Confirm with Owner/fire department during design |
| Generator fuel source (natural gas vs. diesel) | Depends on gas line availability and utility confirmation; Addendum 03 ss1.6 states gas service "within a few feet" of site but formal confirmation not yet documented (Lensing A-002) | Confirm with utility and civil team during design phase; obtain written utility confirmation of natural gas availability at site boundary |
| SCBA cylinder temperature range requirement | NFPA or manufacturer specification not accessed at concept stage; numeric storage temperature range needed to size HVAC supply to SCBA room per R-MEL-10a (Lensing B-001) | Design phase consultation with fire department and SCBA cylinder manufacturer; obtain NFPA specification or manufacturer data sheet for acceptable storage temperature range |
| Decontamination drain disposal method | May require special waste permit depending on contaminants | Confirm with AHJ and environmental consultant during design |
| Second-story adoption | Architectural design decision not yet made | Confirm with Architectural (DEL-02-01) during concept coordination |

---

**End of Datasheet**
