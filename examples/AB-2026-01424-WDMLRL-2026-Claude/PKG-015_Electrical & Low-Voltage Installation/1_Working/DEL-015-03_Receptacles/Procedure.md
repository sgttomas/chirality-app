# Procedure — DEL-015-03 Receptacle Installation

---

## Purpose

This procedure describes the steps to produce and deliver the receptacle installation for the New North Shop addition at the West Dried Meat Lake Regional Landfill Maintenance Shop. It covers pre-installation design coordination, rough-in, device installation, testing, inspection, and closeout documentation.

---

## Prerequisites

### Upstream Deliverables (must be complete or substantially advanced)

| Item | Deliverable / Condition | Status Check |
|---|---|---|
| P-01 | DEL-015-01 Three-Phase Power Service: main distribution panelboard(s) installed and branch circuit capacity available for receptacle circuits | Confirm with PKG-015 electrical lead before rough-in terminations |
| P-02 | DEL-004-05 Receptacle Layout Plans (IFC): signed/stamped drawings issued for construction | Drawings must be current revision before rough-in begins |
| P-03 | DEL-004-06 Panel Schedules (IFC): circuit assignments confirmed for all receptacle circuits | Required before breaker installation and circuit identification |
| P-04 | DEL-004-09 Electrical Specification (IFC): installation specification available | Required before device procurement and installation |
| P-05 | Building structure (walls, framing, concrete): rough framing and pour complete for areas receiving receptacles | Confirm with structural/general contractor |
| P-06 | Electrical Safety Code Permit: obtained and posted on site | Required before commencing installation work |

Source: _DEPENDENCIES.md (upstream: DEL-015-01, building structure); Decomposition PKG-004; RFP §3.3.2

### Required References

- App B-Elec: Conceptual electrical drawing (intent reference during design coordination)
- IFC Receptacle Layout Plans (DEL-004-05)
- IFC Panel Schedules (DEL-004-06)
- IFC Electrical Specification (DEL-004-09)
- Canadian Electrical Code (CEC) Part I (applicable Alberta edition — specific edition TBD per REQ-015-03-04)
- Alberta Safety Codes Act

### Required Personnel

- Licensed Electrical Contractor (journeypersons and apprentices per Alberta requirements)
- Safety Codes Officer (for inspections — coordinate scheduling with AHJ)
- County project representative (must be present for all inspections per RFP §3.3.2)

### Personnel Qualification Verification [Ref: F-003]

Before commencing installation work, the Electrical Contractor shall:
1. Verify that all personnel assigned to this work hold valid Alberta journeyperson or apprentice credentials as applicable.
2. Confirm journeyperson-to-apprentice ratios comply with Alberta requirements.
3. Retain documentation of personnel qualifications on site for the duration of the work.

This verification step is a prerequisite for Phase 1 commencement. Source: _SEMANTIC_LENSING.md F-003; Alberta Safety Codes Act / contractor licensing requirements.

---

## Steps

### Phase 1 — Design Coordination and Pre-Construction

**Step 1.1 — Confirm Welding Receptacle Specifications**

Before procuring welding-grade receptacle devices, confirm with the County the actual plug/receptacle configuration required for their welding equipment. The current design assumes 50A/240V (NEMA configuration TBD — e.g., NEMA 6-50 or NEMA 14-50) per Decomposition D-009. If County-supplied specifications differ, notify the Electrical Designer and Project Manager immediately to initiate a design revision before rough-in.

Source: RFP §3.4; Decomposition D-009; CONF-015-03-01

**Step 1.2 — Review IFC Drawings**

Upon receipt of IFC drawings (DEL-004-05, DEL-004-06, DEL-004-09):
- Confirm receptacle locations, types, and quantities match the contracted scope (SOW-0057, SOW-0058)
- Identify any conflicts with structural elements, mechanical rough-in, or other trades
- Submit RFIs for any conflicts to the designer before commencing work

**Step 1.3 — Material Procurement**

Procure all devices, conduit, wire, outlet boxes, cover plates, and breakers per the IFC specification (DEL-004-09) and the device type mix from the IFC drawings. Verify device ratings match the circuit ratings (15A, 20A, 30A, 50A as applicable). Confirm device grade (specification-grade or industrial-grade) per DEL-004-09 requirements (see REQ-015-03-09).

**Step 1.4 — Permit Confirmation**

Confirm the Electrical Safety Code Permit is posted on site and covers the receptacle installation scope. Coordinate inspection scheduling with the Safety Codes Officer (AHJ) and notify the County project representative of anticipated inspection dates.

**Step 1.5 — Panel Capacity Coordination with DEL-015-02 [Ref: C-003]**

Before finalizing circuit assignments, coordinate with the DEL-015-02 (Lighting) installation team to confirm shared panel capacity allocation. Since DEL-015-02 and DEL-015-03 share the same panel infrastructure (see Guidance — Sequencing with Other PKG-015 Deliverables), circuit assignments must be reviewed jointly to avoid overloading panel buses or circuits.

**Hold Point:** Do not finalize breaker installation until panel capacity coordination with DEL-015-02 is confirmed and documented. Source: _SEMANTIC_LENSING.md C-003; Guidance — Sequencing with Other PKG-015 Deliverables.

---

### Phase 2 — Rough-In

**Step 2.1 — Layout and Box Installation**

Mark outlet box locations per IFC drawings (DEL-004-05). Install outlet boxes at the correct heights and positions, properly secured to framing or structure. In the wash bay and wet areas, use weatherproof boxes rated for the environment.

Source: IFC DEL-004-05; CEC requirements for wet/damp locations

**Step 2.2 — Conduit and Rough-In Wiring**

Install conduit runs from panelboard(s) to outlet boxes per the IFC drawings and electrical specification. Pull conductors sized per the circuit rating and CEC table requirements. Maintain separation from other trades per CEC requirements.

Source: IFC DEL-004-09; CEC Part I

**Step 2.3 — Rough-In Inspection Coordination**

Before closing walls or concealing conduit, request rough-in inspection from the Safety Codes Officer. Notify the County project representative at least 48 hours in advance (consistent with Step 5.1 notification protocol) [Ref: X-005]. Do not close walls until rough-in inspection is passed.

Source: RFP §3.3.2; Alberta Safety Codes Act

**Step 2.4 — Rough-In Deficiency Resolution [Ref: X-003]**

If the rough-in inspection identifies deficiencies:
1. Document all deficiencies identified by the Safety Codes Officer.
2. Resolve all deficiencies before proceeding to Phase 3.
3. Request re-inspection if required by the Safety Codes Officer.
4. Obtain confirmation (written or via inspection report) that all rough-in deficiencies are cleared.

**Hold Point:** Do not proceed to Phase 3 (Device Installation) until all rough-in inspection deficiencies are resolved and confirmed cleared. Source: _SEMANTIC_LENSING.md X-003.

---

### Phase 3 — Device Installation

**Step 3.1 — Receptacle Device Installation**

After walls are finished and painting/surface preparation is complete, install receptacle devices:
- Terminate conductors to devices per manufacturer instructions and CEC requirements
- Torque terminations per manufacturer specification (see Torque Documentation Protocol below)
- Install devices plumb and flush with the wall surface (see REQ-015-03-08 workmanship criteria in Specification)
- Apply correct cover plates (standard covers for general areas; weatherproof/in-use covers with appropriate NEMA ratings for wash bay and wet areas per REQ-015-03-10)

**Torque Documentation Protocol [Ref: A-004]:**
- Obtain manufacturer-specified torque values for each device type before commencing terminations.
- Use a calibrated torque tool (torque screwdriver or wrench) set to the manufacturer-specified value.
- Record the torque value applied for each device type in the installation log.
- If manufacturer torque specifications are not available for a device, contact the manufacturer or refer to DEL-004-09 for guidance. Do not estimate torque values.

Source: _SEMANTIC_LENSING.md A-004; Specification REQ-015-03-08; Specification Verification table.

**Step 3.2 — Circuit Identification**

Label each receptacle circuit at the panelboard per the IFC panel schedule (DEL-004-06). Circuit ID labels must be clear, permanent, and legible (see REQ-015-03-08 workmanship criteria in Specification).

**Step 3.3 — GFCI / AFCI Installation**

Install GFCI protection (device or breaker as specified in DEL-004-09) at all locations required by the CEC. If the applicable CEC edition requires AFCI protection in any zone (see REQ-015-03-07), install AFCI breakers as specified. Test GFCI and AFCI functionality before cover plate installation.

Source: REQ-015-03-07; CEC Part I

---

### Phase 4 — Testing and Commissioning

**Step 4.1 — Pre-Energization Check**

Before energizing receptacle circuits:
- Verify conductor polarity and grounding at each device using a wiring tester or multimeter
- Verify no short-circuits in the circuit runs
- Verify circuit breaker ratings match the circuit design (per DEL-004-06)

**Step 4.2 — Energization and Functional Test**

After DEL-015-01 (Three-Phase Power Service) is energized:
- Energize each receptacle circuit in sequence
- Verify correct voltage at each device using a calibrated meter: 120V (+/-5%) for 15A/20A 120V circuits; 240V (+/-5%) for 240V circuits [Ref: X-002 — tolerance aligned with Verification table]
- Test receptacle polarity and grounding with a plug-in tester at each 120V outlet
- Verify 240V receptacle configurations match the intended NEMA configuration
- For three-phase receptacle circuits (if any): perform phase rotation verification and measure voltage between phases to confirm correct phase assignment per DEL-004-06 [Ref: X-004]

**Step 4.3 — GFCI Trip Test**

Test each GFCI-protected circuit by:
- Pressing the TEST button on each GFCI device (or using a GFCI tester)
- Confirming power is interrupted
- Pressing RESET and confirming power is restored

If AFCI protection is installed, test each AFCI breaker per manufacturer instructions.

**Step 4.4 — Load Test (Welding Receptacles)**

ASSUMPTION: For welding-grade 50A/240V receptacles, a load test using appropriate equipment is recommended to verify conductor capacity and circuit integrity under load.

**Load Test Protocol [Ref: A-005]:**
- **Test definition authority:** TBD — confirm whether the load test protocol is defined in DEL-004-09, by the County, or by the Electrical Contractor based on industry practice.
- **Equipment:** TBD — specify the load bank or test equipment to be used (capacity, type).
- **Pass criteria:** TBD — define what constitutes a successful load test (e.g., sustained rated current for a defined duration without breaker trip, conductor temperature within limits, voltage drop within acceptable range).
- **Mandatory vs. optional:** TBD — confirm whether this step is mandatory or recommended. If mandatory, it must be completed before final inspection (Phase 5).

Until the load test protocol is defined, this step remains **recommended** pending confirmation from DEL-004-09 and County welding equipment specifications. Source: _SEMANTIC_LENSING.md A-005.

---

### Phase 5 — Final Inspection and Closeout

**Step 5.1 — Final Electrical Inspection**

Request final inspection from the Safety Codes Officer. Notify the County project representative at least 48 hours in advance. Ensure all receptacle covers are installed and all wiring is complete before the final inspection.

Source: RFP §3.3.2

**Step 5.2 — Deficiency Resolution**

Resolve all deficiencies identified in the final inspection report within the timeframe specified by the Safety Codes Officer and/or the Owner. Notify the County project representative when deficiencies are resolved.

Source: RFP §2.14.1

**Step 5.3 — As-Built Comparison and Documentation [Ref: D-002]**

Update the IFC electrical drawings to reflect as-built conditions, including any field changes to receptacle locations, circuit routing, or circuit assignments.

**As-Built Comparison Protocol:**
1. Compare the as-built state against the IFC drawings (DEL-004-05, DEL-004-06).
2. Document all deviations from the IFC design, including reasons for each deviation.
3. Submit as-built drawings to the designated reviewer for acceptance (TBD — Project Manager, Designer, or both; see Specification REQ-015-03-03 Verification Protocol).
4. Acceptance tolerance for location deviations: TBD — per Specification.
5. Obtain sign-off from the designated authority before including in closeout documentation.

Source: _SEMANTIC_LENSING.md D-002; Specification REQ-015-03-03 Verification Protocol.

**Step 5.4 — Submit Closeout Documentation**

Assemble and submit to the County project manager:
- Electrical Safety Code Permit (closed/final sign-off)
- Safety Codes Officer inspection reports (all inspections, including rough-in and final)
- As-built electrical drawings (receptacle layout) with deviation log
- Updated panel schedule (as-installed)
- GFCI test records
- AFCI test records (if applicable per REQ-015-03-07) [Ref: B-003]
- Functional test records (voltage, polarity, grounding)
- Torque documentation records [Ref: A-004]
- Load test records (if welding receptacle load test is performed) [Ref: A-005]
- Personnel qualification records [Ref: F-003]

---

## Verification

| Step | Verification Check | Pass Criteria |
|---|---|---|
| Personnel qualification [Ref: F-003] | Verify installer credentials and ratios | All personnel hold valid Alberta credentials; journeyperson/apprentice ratios compliant |
| Panel coordination [Ref: C-003] | Panel capacity coordination with DEL-015-02 | Coordination documented; no overloading of shared panel infrastructure |
| Rough-in inspection | Safety Codes Officer rough-in inspection | Inspection passed; no outstanding deficiencies |
| Rough-in deficiency clearance [Ref: X-003] | Confirmation that all rough-in deficiencies resolved | Written confirmation or re-inspection report showing all deficiencies cleared before Phase 3 |
| Device installation | Wiring tester check at each device | Correct polarity, grounding, and voltage at every outlet |
| Torque verification [Ref: A-004] | Torque documentation review | All terminations torqued to manufacturer specification; values recorded |
| GFCI test | Test/reset cycle at all GFCI locations | GFCI trips on TEST and resets correctly |
| AFCI test (if applicable) [Ref: B-003] | AFCI breaker test per manufacturer instructions | AFCI breaker trips and resets correctly |
| Voltage check | Meter reading at each device | 120V (+/-5%) for 120V circuits; 240V (+/-5%) for 240V circuits |
| Three-phase verification [Ref: X-004] | Phase identification at representative circuits | Measured phase assignment matches panel schedule; voltage between phases correct |
| Final inspection | Safety Codes Officer final inspection | Final inspection passed; permit closed |
| Circuit labelling | Visual check of panel schedule labels | All circuits labelled correctly per DEL-004-06 |
| Welding receptacle configuration | Physical verification of device NEMA type vs. specification | Device type matches IFC drawings and County welder specs |
| As-built comparison [Ref: D-002] | As-built drawings reviewed against IFC | All deviations documented; sign-off obtained from designated authority |

---

## Records

| Record | Description | Retained By |
|---|---|---|
| Personnel Qualification Records [Ref: F-003] | Documentation of installer credentials and Alberta licensing | Electrical Contractor / Project file |
| Electrical Safety Code Permit | Permit document with final sign-off | Electrical Contractor / Project closeout package |
| Rough-in Inspection Report | Safety Codes Officer sign-off on rough-in | Project file; copy to County |
| Rough-in Deficiency Clearance [Ref: X-003] | Confirmation that rough-in deficiencies are resolved | Project file |
| Panel Coordination Record [Ref: C-003] | Documentation of panel capacity coordination with DEL-015-02 | Project file |
| Final Inspection Report | Safety Codes Officer final sign-off | Project file; copy to County (RFP §3.3.2) |
| GFCI Test Log | Record of GFCI test/reset results by location | Project file |
| AFCI Test Log (if applicable) [Ref: B-003] | Record of AFCI breaker test results | Project file |
| Voltage/Polarity Test Log | Record of device-by-device test results | Project file |
| Torque Documentation [Ref: A-004] | Record of termination torque values by device type | Project file |
| Load Test Records (if performed) [Ref: A-005] | Record of welding receptacle load test results | Project file |
| As-Built Drawings | Marked-up IFC drawings showing final installed conditions with deviation log | Submitted to County at project closeout |
| As-Built Panel Schedule | Updated circuit assignments as installed | Submitted to County at project closeout |
