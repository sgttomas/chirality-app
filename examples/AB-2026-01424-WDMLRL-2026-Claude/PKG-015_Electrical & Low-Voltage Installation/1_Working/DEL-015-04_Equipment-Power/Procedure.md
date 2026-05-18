# Procedure — DEL-015-04 Equipment Power Circuits

---

## Purpose

This procedure describes the steps to produce and install the equipment power circuits deliverable for DEL-015-04. It covers both the design coordination activities that must precede installation and the installation sequence itself, as well as the verification activities and records required.

The procedure is written from the perspective of the Electrical Contractor in coordination with the Electrical Engineer (PKG-004), General Contractor / Project Manager (PKG-019), and Crane Contractor (PKG-016).

**Source:** _CONTEXT.md; Decomposition PKG-015; Specification REQ-015-04-001 through REQ-015-04-013

---

## Prerequisites

The following must be in place before installation of equipment power circuits begins:

| Prerequisite | Description | Responsible Party | Reference |
|---|---|---|---|
| P-01 | IFC Electrical Drawings (DEL-004-02) and Panel Schedules (DEL-004-06) issued, P.Eng.-stamped | Electrical Engineer | SOW-0018; REQ-015-04-008 |
| P-02 | Electrical Calculation Package (DEL-004-08) completed, confirming conductor sizing and load calculations | Electrical Engineer | REQ-015-04-008 |
| P-03 | Three-Phase Power Service (DEL-015-01) installed and main distribution panel energized (or at minimum, roughed-in to allow circuit termination) | Electrical Contractor | _DEPENDENCIES.md; REQ-015-04-009 |
| P-04 | Building structure and crane support structure complete (crane runway beams in place) — required before crane runway power supply installation | General Contractor / Structural Contractor | DEL-011 (superstructure); DEL-002-07 (crane supports) |
| P-05 | Crane manufacturer's electrical requirements received | Crane Contractor / Electrical Contractor | DEL-016-01; REQ-015-04-001 |
| P-06 | Equipment specifications confirmed for compressor (40 A), fire hose pump (70 A), pressure washer (70 A), exhaust fan(s), and overhead door operators | Project Manager / Equipment Procurement | REQ-015-04-002 through REQ-015-04-006 |
| P-07 | Alberta Safety Code electrical permit obtained | Electrical Contractor | SOW-0007; REQ-015-04-007 |
| P-08 | Safety Code Authority Having Jurisdiction (AHJ) notified per applicable permit requirements | Electrical Contractor | REQ-015-04-007 |

---

## Steps

### Phase 1 — Design Coordination (Pre-Installation)

**Step 1.1 — Obtain IFC Electrical Design**
Confirm that DEL-004-02 (Power Distribution Plans) and DEL-004-06 (Panel Schedules) have been issued for construction with a P.Eng. stamp. Verify that all six equipment circuit types (cranes, overhead doors, compressor, fire hose pump, pressure washer, exhaust fans) are reflected in the panel schedules with confirmed amperage and voltage.

**Step 1.2 — Review Crane Manufacturer's Electrical Requirements**
Coordinate with the Crane Contractor (PKG-016 / DEL-016-01) to obtain crane manufacturer's installation data including: supply voltage, phase, frequency, amperage draw, required disconnect type, and recommended runway power supply method. Confirm that IFC design matches these requirements.

**Step 1.3 — Confirm Equipment Nameplate Data**
Obtain nameplate data for the air compressor, fire hose pump, pressure washer, exhaust fan(s), and overhead door operators. Verify that the circuit ratings in the IFC panel schedules match or exceed the nameplate requirements. Flag any discrepancies to the Electrical Engineer for design revision before proceeding.

**Step 1.4 — Confirm Scope Boundary for Exhaust Fans**
Confirm with the Project Manager and Mechanical Contractor (PKG-013) which exhaust fans are supplied under SOW-0066 (this deliverable) versus SOW-0038 / SOW-0039 (PKG-013 mechanical scope). Confirm fan locations from IFC electrical drawing. Record the agreed scope boundary. (Refer to CON-015-04-001 in Guidance.md for the open conflict on this boundary.)

**Step 1.5 — Obtain Safety Code Permit**
Apply for the required Alberta Safety Code electrical permit(s) covering the equipment power circuit work.

---

### Phase 2 — Rough-In Installation

**Step 2.1 — Install Conduit/Raceway for Equipment Circuits**
Install conduit, raceway, or cable tray for all equipment power circuits per the IFC electrical drawings. Coordinate routing with other trades (mechanical, structural) to avoid conflicts. Wiring method and conduit sizing are per the IFC design.

**Step 2.2 — Install Crane Runway Power Supply System**
Install the crane runway power supply system (conductor bar, festoon cable system, or as specified in IFC design) along the crane runway. Coordinate with the Crane Contractor to ensure compatibility with crane collector / conductor specifications. Install feed circuit conduit and wire from the distribution panel to the runway power supply enclosure per the IFC design.

**Step 2.3 — Install Conduit / Rough-In for Overhead Door Circuits**
Install conduit and rough-in for all overhead door operator circuits per the IFC drawing. Pull conductors per IFC sizing schedule.

**Step 2.4 — Install Conduit and Pull Wire — Compressor, Pumps, Pressure Washer**
Install conduit and pull conductors for the 40 A compressor circuit, 70 A fire hose pump circuit, and 70 A pressure washer circuit per IFC design. Stage termination points at the equipment locations.

**Step 2.5 — Install Conduit and Pull Wire — Exhaust Fan(s)**
Install conduit and pull conductors for exhaust fan circuit(s) per the IFC electrical drawing. Locations to be confirmed per Step 1.4 scope clarification.

---

### Phase 2A — Grounding and Bonding Installation

**[A-004]** **Step 2A.1 — Install Equipment Grounding Conductors**
Install equipment grounding conductors for all equipment power circuits per CEC requirements and the IFC electrical design. Ensure grounding conductors are sized per the IFC design / DEL-004-08 calculations and CEC Table 16 (or applicable CEC table — **location TBD**). This includes grounding conductors within the conduit/raceway system and bonding jumpers at equipment enclosures, disconnects, and motor termination points.

**Step 2A.2 — Install Bonding Connections**
Install bonding connections at all metallic raceways, enclosures, and equipment chassis per CEC bonding requirements. Verify bonding continuity for each circuit path from the distribution panel through to the equipment termination point.

**Source:** CEC Part I grounding and bonding rules (**location TBD**); ASSUMPTION: grounding and bonding required for all equipment circuits

---

### Phase 3 — Panel Termination and Overcurrent Protection Installation

**Step 3.1 — Install Circuit Breakers / Overcurrent Protection Devices**
Install circuit breakers (or fused disconnects as applicable) in the distribution panel(s) per the IFC panel schedules. Verify breaker ratings match the values specified: 40 A (compressor), 70 A (fire hose pump), 70 A (pressure washer), and per panel schedule for cranes, overhead doors, and exhaust fans.

**Step 3.2 — Terminate Panel-End Conductors**
Terminate all circuit conductors at the distribution panel(s) per the IFC design. Label circuits per panel schedule.

**Step 3.3 — Install Motor Disconnecting Means**
Install motor disconnects within sight of each motor load (cranes, compressor, fire hose pump, pressure washer, exhaust fans) per CEC requirements. Label each disconnect with circuit ID and equipment served.

**Step 3.4 — Circuit and Disconnect Labeling Verification**
**[C-003]** Verify that all circuits are labeled at the distribution panel per the IFC panel schedule (Step 3.2) and that all motor disconnects are labeled with circuit ID and equipment served (Step 3.3). Perform a consolidated labeling check to confirm completeness, legibility, and durability of all labels before proceeding to equipment-end terminations.

**Source:** CEC labeling requirements (**location TBD**); IFC design

---

### Phase 4 — Equipment-End Terminations

**Step 4.1 — Terminate Crane Runway Feed**
Complete the termination of the crane runway power supply feed circuit at the runway power supply enclosure. Verify electrical ratings match crane manufacturer's requirements.

**Step 4.2 — Terminate Overhead Door Operator Circuits**
Terminate circuits at each overhead door operator location. Coordinate with the door operator supplier/installer for final connections.

**Step 4.3 — Terminate Compressor, Pump, and Pressure Washer Circuits**
Terminate circuits at the equipment connection points (motor terminals, junction boxes, or disconnect enclosures) per the IFC design and equipment manufacturer's requirements. Confirm equipment is present before final termination.

**Step 4.4 — Terminate Exhaust Fan Circuit(s)**
Terminate exhaust fan circuit(s) at each fan connection point per the IFC design.

---

### Phase 5 — Pre-Energization Checks

**Step 5.1 — Continuity and Insulation Testing**
Perform continuity and insulation resistance testing on all installed circuits prior to energization. Record results. **[A-005]** Acceptable insulation resistance limit: TBD — specify minimum megohm value per CEC Part I requirements and/or test equipment manufacturer specifications. ASSUMPTION: a minimum of 1 megohm at 500 V test voltage is a common threshold for low-voltage circuits, but the specific pass criterion for this project must be confirmed by the Electrical Engineer or per applicable CEC clause (**location TBD**).

**Step 5.2 — Visual Inspection**
Perform a visual inspection of all installations against the IFC drawings. Verify: correct conductor sizing, correct breaker ratings, all connections tight, all raceways properly supported, disconnects labeled, no exposed conductors.

**Step 5.3 — Request Safety Code Inspection**
Notify the Alberta Safety Code AHJ and request the required electrical rough-in and/or final inspection. **[X-005]** Ensure the County project representative is notified to attend with a minimum advance notification period of TBD business days (source: RFP §3.3.2 / Project Manager — **location TBD**). Obtain confirmation of attendance from the County representative prior to scheduling the inspection. Do not energize until inspection is passed.

---

### Phase 6 — Energization and Functional Testing

**Step 6.0 — Pre-Energization Go/No-Go Checkpoint**
**[F-002]** Before proceeding with energization, formally confirm the following go/no-go conditions and document the checkpoint:
1. DEL-015-01 (Three-Phase Power Service) is energized and the distribution panel feeding these circuits is live and stable (per REQ-015-04-013).
2. Safety Code inspection has been passed (Step 5.3 complete with signed inspection report).
3. All pre-energization tests (Step 5.1) have passed.
4. All visual inspection items (Step 5.2) are satisfactory.

Record the go/no-go determination with date, responsible party signature, and any conditions. Do not proceed to Step 6.1 unless all conditions are met.

**Source:** REQ-015-04-009; REQ-015-04-013; _DEPENDENCIES.md (Upstream: DEL-015-01)

**Step 6.1 — Energize Circuits**
Upon go/no-go checkpoint pass (Step 6.0), energize each equipment circuit under supervision. **[E-003]** Verify and record the measured voltage at each equipment termination point. Acceptable voltage range: TBD — specify per CEC requirements and/or equipment manufacturer voltage tolerance specifications (**location TBD**). Record measured values on a circuit-by-circuit basis for inclusion in the commissioning record.

**Step 6.2 — Functional Test — Cranes**
Coordinate with the Crane Contractor (DEL-016-01) to perform powered functional testing of both 5-tonne overhead cranes. **[E-002]** Acceptance criteria: full travel range (bridge and trolley) without fault; rated load test per crane manufacturer specifications (TBD); verify limit switches operate correctly at each end of travel; no circuit trip during normal operation. Record all test results including measured values where applicable.

**Source:** Crane manufacturer requirements (TBD via DEL-016-01); CAN/CSA standards for overhead cranes (**location TBD**)

**Step 6.3 — Functional Test — Overhead Doors**
Cycle each overhead door through open/close operation using the door operator. Verify normal operation and safety reversal function (if applicable). Record test results.

**Step 6.4 — Functional Test — Compressor**
Start the air compressor and verify normal operation. Confirm circuit breaker does not trip under normal start/run load. Record test results.

**Step 6.5 — Functional Test — Fire Hose Pump**
Start the fire hose pump under supervision and verify normal operation. Confirm circuit breaker does not trip under normal start/run load. Record test results.

**Step 6.6 — Functional Test — Pressure Washer**
Start the pressure washer and verify normal operation. Confirm circuit breaker does not trip under normal start/run load. Record test results.

**Step 6.7 — Functional Test — Exhaust Fan(s)**
Energize exhaust fan circuit(s) and verify fan operation. Record test results.

---

### Phase 7 — Closeout

**Step 7.1 — Produce As-Built Markups**
Mark up IFC drawings with any field deviations. Submit as-built markups per the project closeout requirements (DEL-020-01 / DEL-020-03).

**Step 7.1A — As-Built Verification**
**[D-002]** Before submitting as-built markups, verify that all markups are reviewed against the original IFC drawings to confirm accuracy and completeness. The reviewer (Electrical Contractor foreman or designee) shall confirm that every field deviation is documented, and that no installed work is missing from the markup. Record the verification with reviewer name, date, and confirmation signature.

**Source:** Procedure Step 7.1; ASSUMPTION: as-built accuracy verification is standard practice per Electrical Contractor / Electrical Engineer requirements

**Step 7.2 — Assemble Inspection Reports**
Collect all Safety Code inspection reports and provide copies to the Owner/County project manager (per SOW-0085).

**Step 7.3 — Coordinate Commissioning Record**
Provide functional test records (Steps 6.2–6.7) to the Commissioning Agent / Project Manager for inclusion in the building systems commissioning package (DEL-020-01).

---

## Verification

| Step | Verification Check | Pass Criterion |
|---|---|---|
| After Step 2A.2 | **[A-004]** Grounding and bonding continuity | Bonding continuity verified from distribution panel through to each equipment termination point; grounding conductor sizing confirmed per IFC / CEC |
| After Step 3.4 | **[C-003]** Circuit and disconnect labeling | All circuits labeled at panel per IFC schedule; all disconnects labeled with circuit ID and equipment served; labels legible and durable |
| After Step 5.1 | Continuity and insulation test | All circuits continuous; **[A-005]** insulation resistance at minimum TBD megohms at 500 V test voltage (confirm per CEC / Electrical Engineer — **location TBD**) |
| After Step 5.3 | Safety Code inspection | AHJ inspection pass; signed inspection report obtained; **[A-003]** zero outstanding deficiencies |
| After Step 6.0 | **[F-002]** Pre-energization go/no-go checkpoint | DEL-015-01 energized; Safety Code passed; pre-energization tests passed; visual inspection satisfactory; documented determination with signature |
| After Step 6.1 | Energization voltage check | **[E-003]** Measured voltage recorded at each equipment termination point; voltage within acceptable range (TBD per CEC / equipment manufacturer — **location TBD**) |
| After Step 6.2 | Crane functional test | **[E-002]** Full travel range without fault; rated load test per manufacturer (TBD); limit switches functional; no circuit trip |
| After Step 6.3 | Overhead door functional test | All doors cycle normally |
| After Step 6.4 | Compressor functional test | Compressor starts and runs; no circuit trip |
| After Step 6.5 | Fire hose pump functional test | Pump starts and runs; no circuit trip |
| After Step 6.6 | Pressure washer functional test | Pressure washer starts and runs; no circuit trip |
| After Step 6.7 | Exhaust fan functional test | All fans operate normally |
| After Step 7.1A | **[D-002]** As-built markup verification | All field deviations documented; reviewer confirmation with name, date, signature |

---

## Records

The following records shall be produced and retained as evidence of deliverable completion:

| Record | Description | Produced At |
|---|---|---|
| Pre-energization test reports | Continuity and insulation resistance test results for all circuits | Phase 5 |
| Safety Code inspection report(s) | AHJ-signed electrical inspection reports | Phase 5 |
| Functional test records | Results of Steps 6.2–6.7 for each equipment type | Phase 6 |
| As-built markup drawings | Field record of any deviations from IFC design | Phase 7 |
| Commissioning package contribution | Test records submitted to commissioning agent (DEL-020-01) | Phase 7 |
| Deficiency correction records | **[X-004]** Documentation of any deficiencies found at inspection and their resolution. Deficiency register shall be maintained by the Electrical Contractor (or designee), with each deficiency assigned a unique ID, description, responsible party, target closure date, and actual closure date. Escalation path: deficiencies not resolved within TBD business days shall be escalated to the Project Manager. Closure requires documented verification that the deficiency has been corrected and re-inspected where applicable. Source: CCDC 14 deficiency provisions / Project Manager (**location TBD**) | As required |
| **[E-003]** Voltage measurement records | Measured voltage at each equipment termination point during Step 6.1 energization, with acceptable range noted | Phase 6 |
| **[F-002]** Go/no-go checkpoint record | Documented pre-energization go/no-go determination (Step 6.0) with date, responsible party signature, and conditions | Phase 6 |
| **[D-002]** As-built verification record | Reviewer confirmation that as-built markups are complete and accurate (Step 7.1A) | Phase 7 |
