# Procedure: DEL-02-06 Electrical Power, Lighting, IT/Telecom & PA

## Purpose

This procedure describes:
1. **Production process:** How the Design-Builder produces the Electrical Power, Lighting, IT/Telecom & PA design package during the proposal and design development phases.
2. **Operational process:** How the completed systems are verified, handed over, and used post-occupancy.

*(Source: RFP §7.1 design methodology; RFP §7.3.6 commissioning; OSR §10.4, §10.5, §10.6)*

---

## Prerequisites

### Required Inputs (before starting design)
- Architectural Program and Space Planning package (DEL-02-01): confirmed floor plan, room schedule, apparatus bay layouts, and IT room location/sizing required to locate receptacles, data outlets, lighting fixtures, and PA speakers; IT room location and sizing confirmation is a blocking prerequisite for Step A-5 (IT/Data plan) per A-004
- Firehall Functional Areas (DEL-02-02): apparatus bay layout and bay services coordination (compressed air, exhaust) required to locate electrical services within bays
- Mechanical, Plumbing, Ventilation (DEL-02-05): HVAC equipment loads and overhead door opener electrical requirements to coordinate with electrical distribution
- Emergency Power and Generator design (DEL-02-07): essential loads list and ATS location required to coordinate normal distribution with generator-backed circuits
- Owner Statement of Requirements — OSR §10.4, §10.5, §10.6 (accessible)
- Functional Program (Appendix B): meeting room workstation layout requirements and EM workstation positions — blocking prerequisite for Step A-7 (meeting room EM connectivity design) per F-002; location TBD
- Applicable electrical codes (CEC Part I, ABC Section 11 — location TBD; TBD per F-001)
- IES lighting standards applicable to the facility type — specific footcandle targets per space type (location TBD; TBD per B-002)

### Required Personnel
- Registered Professional Engineer (Electrical), licensed in Alberta (ASSUMPTION — per RFP §7.1.2)
- IT/telecommunications designer or consultant (ASSUMPTION — discipline coordination required for structured cabling and network infrastructure)

### Required References
- RFP 2024_004, OSR §10.4, §10.5, §10.6
- Decomposition FINAL v1.0, PKG-002, DEL-02-06 entry

---

## Steps

### Phase A: Proposal-Stage Design Package (Pre-Award)

**Step A-1: Establish Electrical Design Basis**
Review OSR §10.4 requirements. Develop a preliminary load schedule identifying major electrical loads: apparatus bays (4 bays × services), HVAC motors, overhead door openers, lighting, IT/data active equipment, PA equipment, kitchen/breakroom, office loads. Identify generator-essential vs. non-essential load classifications in coordination with DEL-02-07.
*(Source: OSR §10.4; Decomposition SOW-0227)*

**Step A-2: Develop Single-Line Diagram Concept**
Prepare a schematic single-line diagram showing: main service entry, main distribution panel, sub-panel locations (apparatus bays, shared spaces, office wing, IT room), and ATS tie-in point. Identify spare capacity provisions for future flexibility.
*(Source: OSR §10.4)*

**Step A-3: Develop Receptacle Plan Concept**
Overlay preliminary receptacle locations on floor plan concept. Confirm interior and exterior receptacle coverage. Identify GFCI and weatherproof locations. Coordinate with mechanical for door opener circuit requirements.
*(Source: OSR §10.4)*

**Step A-4: Develop Lighting Design Concept**
Identify IES illuminance categories for each space type (office, apparatus bay, corridors, washrooms, meeting room). Select LED fixture types for each category. Prepare a preliminary reflected ceiling plan concept showing fixture layout. Confirm fixture heights in bay areas for apparatus clearance. Document emergency exit light locations above all personal doors.
*(Source: OSR §10.5)*

**Step A-5: Develop IT/Data and Telecom Plan Concept**
**Prerequisite:** IT room location and sizing must be confirmed from DEL-02-01 before proceeding (A-004 — blocking input). Identify IT room location (in coordination with DEL-02-01 architectural plan); confirm adequate space for patch panels, active equipment, and future growth per R-11 (TIA-568 structured cabling). Lay out horizontal cabling routes to all occupied areas compliant with TIA-568 (F-003). Detail meeting room EM connectivity: 15 data outlet positions, patch panel/switch sizing basis, and power outlet positions for 15 workstations (15 concurrent access points per R-12). Confirm apparatus bay closest to office area for display system mounting; show power receptacle and data/HDMI outlet at display location (R-13).
*(Source: OSR §10.6; SOW-0224, SOW-0225; R-11, R-12, R-13; A-004, F-003)*

**Step A-6: Develop PA System Design Concept**
Identify head-end amplifier/controller location (ASSUMPTION: in IT room or adjacent equipment room). Lay out speaker locations to achieve coverage throughout all main building occupied areas. Confirm cold storage building is excluded. Describe system type (simple paging system — ASSUMPTION: analog or IP-based paging amplifier with passive or powered speakers).
*(Source: OSR §10.6; SOW-0226)*

**Step A-7: Develop Meeting Room EM Workstations Connectivity Plan**
**Prerequisite:** Functional Program (Appendix B) meeting room workstation layout must be obtained and reviewed before proceeding (F-002 — blocking input). Prepare a narrative or detail drawing showing how 15 concurrent EM workstations will be supported per R-12: power provisions (outlet count and positions for 15 workstations per C-003 "critical operational threshold"), data infrastructure (15 RJ45 ports or wireless access point with verified 15-user concurrent capacity), and floor box or raceway provisions for workstation connectivity. Clarify whether approach is wired (15 RJ45 ports), wireless (15-user access point capacity), or hybrid per C-003.
*(Source: OSR §10.6; SOW-0208, SOW-0224; R-12; C-003; F-002)*

**Step A-8: Compile Proposal-Stage Deliverable Package**
Assemble all concept-level documents for the proposal submission. At proposal stage, documents are design-basis narratives and schematic drawings; IFC-level detail follows post-award per RFP §7.1.8 milestones.
*(Source: RFP §7.1.1–§7.1.2)*

---

### Phase B: Post-Award Design Development (DD through IFC)

**Step B-1: Design Development (DD)**
Develop all concept drawings to Design Development level. Prepare:
- Detailed single-line diagram with panel schedules
- Full receptacle plan with circuit numbering
- IES photometric study confirming footcandle levels per space
- Full lighting fixture schedule (model, wattage, CRI, CCT, lamp life)
- Data outlet schedule and structured cabling riser diagram
- PA speaker layout with coverage calculations or acoustical basis

**Step B-2: 60% Detailed Design Review**
Submit 60% design package to Owner per RFP §7.1.8. Incorporate Owner review comments. Coordinate with all disciplines on:
- Ceiling height and fixture mounting confirmed with structural (DEL-02-04)
- HVAC duct routing conflicts with lighting and cabling (DEL-02-05)
- Generator essential loads list finalized with DEL-02-07
- IT room final size confirmed with DEL-02-01

**Step B-3: 100% Detailed Design and IFC Preparation**
Complete and seal all electrical, data/telecom, and PA drawings. Prepare specifications. Apply Alberta P.Eng. seal to all documents. Submit for building permit.

---

### Phase C: Construction

**Step C-1: Rough-In**
Install conduit, cable trays, and rough-in boxes per IFC drawings. Install underground conduits before slab pour. Inspect rough-in before covering.

**Step C-2: Cable Installation**
Pull electrical feeders, branch circuits, and structured cabling (data, PA speaker wire). Label all circuits and cables per panel schedule.

**Step C-3: Device and Equipment Installation**
Install receptacles, switches (with weatherproof covers at applicable locations), luminaires, emergency exit lights, PA speakers, display system mounting hardware, and data outlets. Install IT infrastructure in IT room (patch panels, rack — ASSUMPTION: Owner-furnished active equipment).

**Step C-4: Testing and Inspection**
Conduct electrical inspections with Authority Having Jurisdiction (AHJ). Test and document:
- Each circuit for continuity and no shorts
- GFCI protection on exterior and wet-location receptacles per CEC requirements (X-002)
- Emergency exit lights (battery backup function)
- PA system for coverage and intelligibility in all zones; document intelligibility criterion (STI score or zone coverage pass/fail per F-004, R-14 verification)
- Meeting room IT connectivity (15-port function test confirming 15 concurrent workstation capacity per R-12)
- Apparatus bay display system end-to-end (laptop to display connection; verify display size, resolution, viewing angle per D-002, D-004)
- Structured cabling certification testing per TIA-568 standard if required (X-004 — add to Phase C or D commissioning steps)

---

### Phase D: Commissioning and Handover

**Step D-1: Systems Commissioning**
Commission all electrical, lighting, IT, and PA systems per commissioning plan (coordinated under DEL-01-07). Document:
- Panel schedule as-built values
- Emergency lighting test records (battery backup function, execution time)
- PA system zone test records (coverage and intelligibility per R-14, F-004)
- IT connectivity test results (15-concurrent-workstation capacity verification per R-12)
- Structured cabling certification records (TIA-568 compliance, if required per F-003, X-004)
- Display system acceptance criteria verification (size, resolution, functional test per D-002, D-004)

**Step D-2: Owner Training**
Provide training to Owner's operations staff on:
- Circuit breaker panel locations and labeling
- Emergency lighting test/reset procedure
- PA system basic operation (paging, volume adjustment)
- Apparatus bay display system operation and connectivity

*(Source: RFP §7.3.6)*

**Step D-3: As-Built Documentation**
Submit as-built electrical drawings, data/telecom as-builts, PA riser as-built, and O&M manuals for all installed equipment to Owner.
*(Source: RFP §7.3.6; §7.5)*

---

### Phase E: Warranty Period

**Step E-1: 12-Month Warranty Monitoring**
Monitor and respond to electrical, lighting, IT infrastructure, and PA system deficiencies during the 12-month warranty period.
*(Source: RFP §7.6)*

**Step E-2: Warranty Corrections**
Correct any materials/workmanship deficiencies. Replace lamp failures during warranty if attributable to installation defects (ASSUMPTION — lamp warranty periods vary by manufacturer; coordinate with Design-Builder warranty policy).

---

## Verification

| Check | Verification Method | Reference |
|-------|---------------------|-----------|
| All OSR electrical requirements addressed | Cross-check R-01 through R-04 (Specification) against completed design package | Specification §Requirements |
| Lighting — IES compliance | Photometric study submitted and reviewed | Specification R-05 |
| LED fixtures throughout | Fixture schedule review | Specification R-06 |
| Emergency exit lighting installed | Site inspection + AHJ approval | Specification R-07 |
| 15 EM workstation capacity confirmed | IT design review; test at commissioning | Specification R-12 |
| Apparatus bay display system functional | End-to-end test (laptop → display connection) | Specification R-13 |
| PA system — main building coverage confirmed | Speaker layout review + commissioning zone test | Specification R-14 |
| No PA system in cold storage building | Drawing review confirms scope boundary | Specification R-14 |
| Code compliance | AHJ permit and inspection records | Specification R-15 |
| Sealed drawings | Drawing title block review | Specification R-16 |

---

## Records

The following records shall be produced and retained:

| Record | Owner | Timing |
|--------|-------|--------|
| Electrical design basis narrative | Design-Builder | Proposal / DD stage |
| Schematic single-line diagram (proposal) | Design-Builder | Proposal submission |
| Detailed single-line diagram + panel schedule (IFC) | Design-Builder | 100% IFC |
| Receptacle plan (IFC) | Design-Builder | 100% IFC |
| Lighting design — reflected ceiling plan + fixture schedule | Design-Builder | 100% IFC |
| Photometric study (IES compliance) | Design-Builder | DD stage |
| Data/telecom plan + riser diagram (IFC) | Design-Builder | 100% IFC |
| PA system layout + speaker schedule (IFC) | Design-Builder | 100% IFC |
| Meeting room EM connectivity detail | Design-Builder | DD stage |
| Apparatus bay display system design description | Design-Builder | Proposal / DD stage |
| AHJ inspection records | Design-Builder | Construction |
| Emergency lighting test records | Design-Builder | Commissioning |
| PA system commissioning test records | Design-Builder | Commissioning |
| Owner training records (sign-off) | Design-Builder | Commissioning |
| As-built drawings (electrical, data, PA) | Design-Builder | Closeout |
| O&M manuals (luminaires, PA head-end, display) | Design-Builder | Closeout |
| Warranty deficiency log | Design-Builder | Warranty period |
