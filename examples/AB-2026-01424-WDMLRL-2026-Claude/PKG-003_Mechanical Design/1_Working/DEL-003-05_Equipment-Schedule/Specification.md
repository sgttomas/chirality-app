# Specification — DEL-003-05 Mechanical Equipment Schedule
**Deliverable ID:** DEL-003-05
**Name:** Mechanical Equipment Schedule
**Package:** PKG-003 Mechanical Design
**Discipline:** Mechanical Engineering
**Type:** Schedule
**Responsible:** Mechanical Engineer
**Project:** 2026 Design Build — West Dried Meat Lake Regional Landfill Maintenance Shop Addition
**Owner:** Camrose County
**Revision:** R1 (Pass 3 enrichment — 2026-02-26)
**Date:** 2026-02-25

---

## 1. Scope

### 1.1 What This Deliverable Covers

The Mechanical Equipment Schedule (DEL-003-05) is a tabular design document that enumerates all mechanical equipment items required for the New North Shop Addition as part of the mechanical design package (PKG-003). It covers:

- All HVAC equipment (heating, air exchange, makeup air)
- All ventilation and exhaust equipment (heavy equipment exhaust, welding station exhaust)
- Service pit ventilation equipment (if provided by a dedicated mechanical system — see REQ-010)
- Ceiling fans in the main shop area
- Equipment service locations, quantities, performance parameters, and design data sufficient for procurement, construction, and IFC coordination

### 1.2 What This Deliverable Excludes

- Plumbing fixtures and plumbing equipment (covered by PKG-006, DEL-006-06 Plumbing Fixture Schedule)
- Electrical panel schedules and circuit specifications (covered by PKG-004, DEL-004-06 Panel Schedules)
- Structural supports for mechanical equipment (governed by PKG-002 Structural Design)
- Equipment commissioning checklists and startup records (governed by PKG-020 Commissioning & Closeout)
- Mechanical calculation package (covered by DEL-003-06 Mechanical Calculation Package)
- Equipment procurement and installation (covered by PKG-013 Mechanical & HVAC Installation)

### 1.3 Relationship to Other Mechanical Deliverables

This schedule is the companion tabular reference to the HVAC Plans (DEL-003-02), Ductwork Plans (DEL-003-03), Exhaust System Plans (DEL-003-04), Mechanical Calculation Package (DEL-003-06), and Mechanical Specification (DEL-003-07). Values in this schedule shall be consistent with values shown on the drawings and shall be cross-referenced to the drawing sheets.

---

## 2. Requirements

### 2.1 Content Requirements

#### REQ-001 — Completeness of Equipment Coverage
The schedule shall include every distinct mechanical equipment item required under SOW-0013 (final mechanical design — HVAC, ventilation, exhaust systems).
**Minimum required equipment categories** (per RFP §3.4 and App B):
- High-recovery heating system (SOW-0035)
- High-volume air exchanger (SOW-0036)
- Forced-air makeup air unit (SOW-0037)
- Heavy equipment exhaust systems — both repair bays (SOW-0038)
- Welding station exhaust system (SOW-0039)
- Ceiling fans — main shop (SOW-0040)
- Service pit ventilation (SOW-0028) — if provided by dedicated mechanical system (see REQ-010)
**Source:** RFP §3.4; Decomposition SOW-0035–SOW-0040; SOW-0028

#### REQ-002 — Equipment Tag Assignment
Each equipment item shall be assigned a unique tag designation. Tag format shall be consistent with project tag conventions. **The Mechanical Engineer shall establish and document the tag convention before schedule population begins** (see Procedure Step 1.3). The tag convention shall be confirmed at project start and communicated to the drawing team.
**Source:** Standard mechanical engineering practice; no project-specific tag convention specified in RFP. **Note (Pass 3, F-002):** ASSUMPTION qualifier removed per semantic lensing; the tag convention is to be confirmed by the Mechanical Engineer as a definitive requirement rather than left as an assumption.

#### REQ-003 — Minimum Data Fields per Equipment Item
For each piece of equipment, the schedule shall include at minimum:
- Equipment tag
- Equipment description / name
- Quantity
- Service area / location served
- Design capacity / performance parameters (heating output, airflow, static pressure, motor power as applicable)
- Connection requirements (fuel type, electrical characteristics including phase/voltage/FLA, duct connections)
- Equipment weight (for structural coordination — see Procedure Step 3.2)
- Vibration characteristics and mounting requirements (for structural coordination — see Procedure Step 3.2)
- Acoustical data (sound power level or sound pressure level, where applicable to occupied-space equipment)
- Basis of design notes (manufacturer/model reference or performance specification)
- Drawing sheet cross-reference (populated at IFC stage)
**Source:** Standard mechanical equipment schedule practice; RFP §3.3.2 (IFC drawing completeness requirement). **Note (Pass 3, X-003):** Equipment weight, vibration characteristics, and acoustical data added per semantic lensing — these fields are needed for structural coordination (Procedure Step 3.2) and occupant comfort evaluation but were absent from the original minimum data fields.

#### REQ-004 — Performance Parameters — Heating System
The high-recovery heating system (HTG-001) design data shall include:
- Total heating output (kW or BTU/h)
- Heat recovery type and efficiency (%)
- Fuel type (natural gas — per SOW-0080 utility tie-in)
- Electrical connection (phase, voltage, amperage)
- Applicable efficiency rating
- Equipment weight and mounting requirements
**Acceptance criteria:** Heating capacity shall be sufficient to maintain indoor design temperature at outdoor design heating temperature with doors closed, as demonstrated by DEL-003-06 calculations. Specific acceptance values TBD pending calculation completion.
**Source:** RFP §3.4 (SOW-0035); SOW-0080 (natural gas tie-in). **Note (Pass 3, X-004):** Acceptance criteria placeholder added per semantic lensing; specific pass/fail values are derived from DEL-003-06.

#### REQ-005 — Performance Parameters — Air Exchanger
The high-volume air exchanger (AEX-001) design data shall include:
- Supply airflow (CFM or L/s)
- Exhaust airflow (CFM or L/s)
- Heat/energy recovery effectiveness (%)
- Fan motor power (kW or hp)
- External static pressure (Pa or in. w.g.)
- Equipment weight and mounting requirements
**Acceptance criteria:** Airflow rates shall meet or exceed ASHRAE 62.1 minimum ventilation requirements for the served occupancy, as demonstrated by DEL-003-06 calculations. Specific acceptance values TBD pending calculation completion.
**Source:** RFP §3.4 (SOW-0036). **Note (Pass 3, X-004):** Acceptance criteria placeholder added.

#### REQ-006 — Performance Parameters — Makeup Air Unit
The forced-air makeup air unit (MAU-001) design data shall include:
- Supply airflow (CFM or L/s)
- Heating capacity (kW or BTU/h)
- Discharge temperature
- Gas input rating
- Electrical connection
- Equipment weight and mounting requirements
**Acceptance criteria:** Supply airflow and heating capacity shall be sufficient to maintain positive building pressure and indoor design temperature during exhaust system operation, as demonstrated by DEL-003-06 calculations. Specific acceptance values TBD pending calculation completion.
**Source:** RFP App B (Shop) ("Forced Air Makeup"); SOW-0037. **Note (Pass 3, X-004):** Acceptance criteria placeholder added.

#### REQ-007 — Performance Parameters — Equipment Exhaust
Heavy equipment exhaust systems (EXH-001, EXH-002) design data shall include:
- Exhaust fan airflow (CFM or L/s per bay)
- Fan static pressure rating
- Hose diameter and rated length
- Motor power
- Exhaust discharge location
**Acceptance criteria:** Exhaust fan capacity shall achieve adequate capture at tailpipe connection point per applicable industrial ventilation standards (ACGIH or NFPA 91), as demonstrated by DEL-003-06 calculations. Specific acceptance values TBD pending calculation completion.
**Source:** RFP §3.4 (SOW-0038). **Note (Pass 3, X-004):** Acceptance criteria placeholder added.

#### REQ-008 — Performance Parameters — Welding Exhaust
The welding station exhaust system (EXH-003) design data shall include:
- Capture airflow (CFM or L/s)
- Capture velocity at hood face (fpm or m/s)
- Fan static pressure
- Motor power
- Duct material and routing notes
**Acceptance criteria:** Capture velocity shall meet ACGIH Industrial Ventilation recommended practice for the applicable welding process (process type TBD pending County welding equipment specifications per SOW-0204). Specific acceptance values TBD.
**Source:** RFP §3.4 (SOW-0039); App B (Shop) (welding station location — north wall). **Note (Pass 3, X-004):** Acceptance criteria placeholder added.

#### REQ-009 — Performance Parameters — Ceiling Fans
Ceiling fans (CF-001 through CF-006) design data shall include:
- Fan diameter
- Number of fans (6 per SOW-0040)
- Motor power per fan
- Airflow (CFM per fan)
- Mounting height (35 ft ceiling, App B Shop)
- Control type (speed, direction reversibility)
**Acceptance criteria:** Fan airflow and distribution pattern shall achieve effective destratification at 35 ft ceiling height, as demonstrated by manufacturer data or engineering analysis in DEL-003-06. Specific acceptance values TBD.
**Source:** Decomposition SOW-0040; App B (Shop) (35' ceiling). **Note (Pass 3, X-004):** Acceptance criteria placeholder added.

#### REQ-010 — Service Pit Ventilation
If the service pit (SOW-0028) ventilation is provided by a mechanical system separate from the main shop systems, it shall be included in the schedule with its own tag and performance data. If served by the main shop exhaust/makeup systems, this shall be noted with the applicable equipment tag reference.
**Source:** RFP §3.4 (SOW-0028 — "ventilated and lighted service pit"); ASSUMPTION: mechanical engineer to confirm design approach

#### REQ-011 — IFC Stamp Requirement
The final issued schedule, as part of the IFC drawing set, shall be signed and stamped by a P.Eng. licensed in Alberta.
**Source:** RFP §3.3.2; SOW-0018

#### REQ-012 — Preliminary Design Approval
A preliminary mechanical design (DEL-003-01) covering the equipment selection approach shall receive County approval before finalization of this schedule per SOW-0010c. **Material changes** to equipment selections between County-approved preliminary design and IFC shall be flagged to the County for confirmation. See also REQ-016.
**Source:** RFP §3.3.2; SOW-0010c. **Note (Pass 3, D-001):** Material change notification language added per semantic lensing. The threshold for "material change" is TBD — to be defined by the Mechanical Engineer (see Guidance §2.4 and Conflict Table CON-005).

#### REQ-013 — Code Compliance
All equipment and their performance parameters shall comply with:
- Alberta Building Code (applicable edition — TBD; to be confirmed by Mechanical Engineer at design start per A-002)
- Alberta Safety Codes Act
- ASHRAE 62.1 (applicable edition — TBD; to be confirmed at design start)
- ASHRAE 90.1 or equivalent Alberta energy code (applicable edition — TBD; to be confirmed at design start)
- NFPA 91 (exhaust systems — ASSUMPTION: applicable; edition TBD)
- CSA B149.1 (gas-fired equipment — ASSUMPTION: applicable; edition TBD)
**Acceptance criteria:** TBD — to be defined per specific code clause requirements once editions are confirmed. ASSUMPTION: AHJ inspection and building permit process will serve as the compliance verification mechanism; however, a compliance checklist defining specific submission requirements for this deliverable is TBD (see A-003).
**Source:** RFP §3.3.2 (SOW-0008, SOW-0009). **Note (Pass 3, A-002, A-003):** Specific code editions must be confirmed at design start; compliance checklist items TBD per semantic lensing.

### 2.2 Format Requirements

#### REQ-014 — Schedule Format
The schedule shall be presented in tabular format, organized by system type. Each row represents one equipment item or one equipment sub-component where applicable (e.g., fan, coil, controls).
**Source:** ASSUMPTION (standard practice for mechanical equipment schedules)

#### REQ-015 — Cross-Reference to Drawings
Each schedule row shall include a drawing sheet cross-reference field, to be populated at IFC issue. This ensures traceability between the schedule and the HVAC/ductwork/exhaust plan drawings. **Verification of cross-reference completeness shall be bidirectional** — confirming both that (a) all schedule tags appear on the referenced drawings and (b) all equipment tags shown on drawings appear in the schedule.
**Source:** Standard IFC coordination practice; RFP §3.3.2. **Note (Pass 3, C-003):** Bidirectional reconciliation requirement added per semantic lensing — the original unidirectional check ("schedule tags match drawing tags") did not verify completeness in the reverse direction.

### 2.3 Coordination and Change Management Requirements

#### REQ-016 — Change Management for Post-Approval Deviations (Pass 3 enrichment, D-001)
If equipment selections in the IFC schedule deviate materially from the County-approved preliminary design (DEL-003-01), the deviation shall be documented and the County shall be notified before IFC issue. The threshold for "material change" is TBD — to be defined by the Mechanical Engineer. At minimum, the following should be considered material changes:
- Substitution of equipment type (e.g., radiant heater replacing unit heater for HTG-001)
- Change in equipment quantity
- Significant change in performance capacity (threshold TBD)
**Source:** RFP §3.3.2; SOW-0010c (County approval requirement implies change control for deviations). ASSUMPTION: change management threshold must be defined by Mechanical Engineer.

#### REQ-017 — IFC Schedule Completeness — No TBD Values (Pass 3 enrichment, A-005)
The IFC-issued schedule shall not contain TBD values in required performance fields (as enumerated in REQ-003). All performance parameters shall be resolved and supported by the Calculation Package (DEL-003-06) before IFC issue.
**Source:** Procedure.md Step 3.3 (already stated as a procedural requirement); formalized here as a specification requirement for verification purposes.

---

## 3. Standards

| Standard | Description | Applicability | Accessibility |
|---|---|---|---|
| Alberta Building Code | Provincial building code — mechanical provisions (edition TBD — to be confirmed at design start) | Code compliance for all HVAC equipment | Not directly accessible — location TBD |
| Alberta Safety Codes Act | Safety code compliance | All building systems | Not directly accessible — location TBD |
| ASHRAE 62.1 | Ventilation for Acceptable Indoor Air Quality (edition TBD — to be confirmed at design start) | Minimum ventilation rates for occupied spaces | Not accessible — location TBD |
| ASHRAE 90.1 | Energy Standard for Buildings (edition TBD — to be confirmed at design start) | Minimum efficiency ratings for HVAC equipment | Not accessible — location TBD |
| NFPA 91 | Exhaust Systems for Air Conveying of Vapors, Gases, Mists, and Particulate Solids (edition TBD) | Equipment exhaust and welding exhaust systems | Not accessible — ASSUMPTION: likely applicable |
| ACGIH Industrial Ventilation Manual | Industrial Ventilation: A Manual of Recommended Practice | Welding exhaust capture hood design | Not accessible — ASSUMPTION: likely applicable |
| CSA B149.1 | Natural Gas and Propane Installation Code (edition TBD) | Gas-fired equipment connections | Not accessible — ASSUMPTION: applicable for gas heating/MAU |

> All standards listed as "not accessible" are flagged as **ASSUMPTION: likely applicable** based on Alberta jurisdiction and equipment types. Clause-level requirements are not derived from inaccessible sources. Confirmation by the Mechanical Engineer of record is required at design stage.

> **Pass 3 enrichment note (A-002):** Specific editions of all listed standards must be confirmed by the Mechanical Engineer at design start. Without confirmed editions, clause-level compliance determination is indeterminate. "Edition TBD" annotations added to all standard entries.

---

## 4. Verification

### 4.1 Verification Matrix

| Requirement | Verification Method | Acceptance Criteria | Verification Milestone |
|---|---|---|---|
| REQ-001 — Completeness | Design review: check schedule against SOW-0035-SOW-0040 list and SOW-0028 | All required equipment categories present with assigned tags | Preliminary design review; IFC issue |
| REQ-002 — Tag assignment | Document review: confirm unique tags, consistent with drawing legend | Tags unique, follow documented convention, match drawing legend | IFC issue |
| REQ-003 — Minimum data fields | Document review: check all required columns are populated | All required columns present and populated (no TBD in required fields at IFC) | IFC issue |
| REQ-004 — Heating system parameters | Engineering calculation review (DEL-003-06); design team QC | Heating capacity sufficient per DEL-003-06 calculations; specific values TBD | IFC issue |
| REQ-005 — Air exchanger parameters | Engineering calculation review (DEL-003-06); design team QC | Airflow meets ASHRAE 62.1 minimums; specific values TBD | IFC issue |
| REQ-006 — Makeup air parameters | Engineering calculation review (DEL-003-06); design team QC | Supply airflow maintains positive pressure during exhaust operation; specific values TBD | IFC issue |
| REQ-007 — Equipment exhaust parameters | Engineering calculation review (DEL-003-06); design team QC | Capture at tailpipe per ACGIH/NFPA 91; specific values TBD | IFC issue |
| REQ-008 — Welding exhaust parameters | Engineering calculation review (DEL-003-06); design team QC | Capture velocity per ACGIH for applicable welding process; specific values TBD | IFC issue |
| REQ-009 — Ceiling fan parameters | Engineering calculation review (DEL-003-06); manufacturer data review | Effective destratification at 35 ft; specific values TBD | IFC issue |
| REQ-010 — Service pit ventilation | Design review: confirm pit ventilation coverage by system(s) | Ventilation approach confirmed and documented | Preliminary design; IFC issue |
| REQ-011 — P.Eng. stamp | Document review: confirm stamp on IFC set | Stamp present, P.Eng. licensed in Alberta | IFC issue |
| REQ-012 — County approval | Approval record from County (DEL-003-01 sign-off) | Written County approval on file | Before IFC |
| REQ-013 — Code compliance | Authority Having Jurisdiction (AHJ) inspection; building permit process; code compliance checklist (TBD — see A-003) | TBD — to be defined per confirmed code editions | During construction; CCC |
| REQ-014 — Format | Document review | Schedule in tabular format, organized by system type | IFC issue |
| REQ-015 — Cross-reference | Bidirectional drawing coordination check: (a) schedule tags appear on drawings AND (b) drawing equipment tags appear in schedule | Complete bidirectional tag reconciliation confirmed | IFC issue |
| REQ-016 — Change management | Design review: compare IFC selections against County-approved preliminary | Material changes identified and County notified before IFC | Before IFC |
| REQ-017 — IFC completeness (no TBDs) | Document review: confirm no TBD values in required performance fields | Zero TBD values in REQ-003 required fields | IFC issue |

> **Pass 3 enrichment note (X-004):** Acceptance Criteria column added to verification matrix. For REQ-004 through REQ-009, specific numeric acceptance criteria are derived from DEL-003-06 calculations and are TBD at this scaffold stage. Placeholder acceptance criteria describe the performance standard to be met.

> **Pass 3 enrichment note (E-003):** Verification milestones use relative terms ("IFC issue", "Before IFC"). These milestones should be linked to the project schedule (December 31, 2026 completion deadline per RFP §3.1, SOW-0091) or to DEL-003-01 timeline. Calendar date linkage is TBD pending project schedule development.

### 4.2 Site Verification (Construction Phase)

During construction (PKG-013), the mechanical contractor shall verify that installed equipment matches the specified schedule parameters. Any deviations shall be documented and processed as design changes per project change management protocols.
**Source:** ASSUMPTION (standard construction QC practice); RFP §1.0 (construction quality control management)

---

## 5. Documentation

### 5.1 Anticipated Artifacts

Per _CONTEXT.md and decomposition, the following artifacts are anticipated outputs:

| Artifact | Description | Status |
|---|---|---|
| Mechanical Equipment Schedule (tabular) | The primary schedule document — tabular listing of all mechanical equipment with tags, quantities, performance data | This deliverable (DEL-003-05) |
| Drawing sheet cross-reference list | Cross-reference from schedule tags to HVAC/exhaust plan sheets | Populated at IFC stage |
| Basis of Design notes | Equipment selection rationale linked to calculation package | Provided in DEL-003-06 (Mechanical Calculation Package) |

### 5.2 Related Deliverables

| Deliverable ID | Name | Relationship |
|---|---|---|
| DEL-003-01 | Preliminary Mechanical Design | Must be approved before this schedule is finalized |
| DEL-003-02 | HVAC Layout Plans | Drawings showing equipment locations; tags must match this schedule |
| DEL-003-03 | Ductwork & Distribution Plans | Ductwork coordinated with equipment in this schedule |
| DEL-003-04 | Exhaust System Plans | Exhaust equipment in this schedule shown on these plans |
| DEL-003-06 | Mechanical Calculation Package | Calculation basis for all performance values in this schedule |
| DEL-003-07 | Mechanical Specification | Equipment specifications aligned with schedule tags and performance data |
| DEL-013-01 thru DEL-013-06 | Mechanical & HVAC Installation deliverables | Construction phase; installed against this schedule |
| DEL-020-01 | Building Systems Commissioning | Equipment commissioned per schedule parameters |
