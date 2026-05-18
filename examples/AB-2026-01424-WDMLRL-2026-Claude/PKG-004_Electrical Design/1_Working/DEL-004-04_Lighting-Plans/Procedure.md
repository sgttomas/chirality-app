# Procedure — DEL-004-04 Lighting Plans

---

## Purpose

This procedure describes the steps to produce the Lighting Plans drawing set (DEL-004-04) for the New North Shop addition at the West Dried Meat Lake Regional Landfill Maintenance Shop. The drawing set is a design deliverable under PKG-004 (Electrical Design) and must be produced at IFC quality with a P.Eng. stamp before the electrical contractor (PKG-015) can install the lighting system.

---

## Prerequisites

### Input Deliverables and Information Required Before Starting

| Prerequisite | Source | Status | Resolution Path [C-003] | Critical-Path? |
|---|---|---|---|---|
| Conceptual electrical layout (App B-Elec) | RFP Appendix B (Electrical) | Available -- R-05 in _REFERENCES.md | Resolved | N/A |
| RFP electrical design requirements (§3.4) | RFP §3.4 | Available -- R-01 in _REFERENCES.md | Resolved | N/A |
| Preliminary Electrical Design (DEL-004-01) -- County approved | PKG-004 Electrical Design | Required before IFC issue; status TBD | Blocks Step 4 (final IFC drawings). Preliminary layout (Step 2) can proceed without this. Trigger: County approval milestone. | Yes -- blocks IFC issue |
| Architectural floor plans (DEL-001-02) | PKG-001 Architectural Design | Required for drawing background; status TBD | Blocks Step 2.1 (scaled floor plan background) and dimension confirmation (Step 1.2). Can proceed with conceptual dimensions from App B-Elec for preliminary layout. Trigger: DEL-001-02 issue. | Yes -- blocks accurate scaled drawing |
| Structural framing plans (DEL-002-03) -- for mounting point coordination | PKG-002 Structural Design | Required for pendant/mount coordination at 35' ceiling; status TBD | Can proceed in parallel with preliminary layout. Required before final mounting detail in Step 4.3. Trigger: DEL-002-03 issue. | No -- parallel with preliminary design |
| Mechanical HVAC/fan layout (DEL-003-02 or DEL-003-04) | PKG-003 Mechanical Design | Required for coordination of ceiling fan and exhaust fan locations relative to high bay fixture rows; status TBD | Can proceed in parallel. Required before Step 2.6 coordination check and Step 4.3 construction notes. Trigger: DEL-003 mechanical layout issue. | No -- parallel with preliminary design |
| Authority Having Jurisdiction (AHJ) confirmation of applicable electrical codes | Electrical Engineer / Permit process | TBD -- confirm CEC edition and Alberta amendments applicable | Blocks code compliance verification (REQ-LT-008) and emergency lighting determination (CONF-LT-003). Should be initiated early in Step 1.3. Trigger: Electrical Engineer AHJ inquiry. | Yes -- blocks code compliance determination |

### Responsible Party

Electrical Engineer (licensed P.Eng. in Alberta) — per _CONTEXT.md.

### Required References

- AB-2026-01424-Appendix B (Electrical).pdf (R-05) — primary layout source
- AB-2026-01424-WDMLRL RFP.pdf (R-01) — §3.4 design requirements, §3.3.2 IFC requirements
- Applicable edition of the Canadian Electrical Code (CEC) Part I — location TBD
- Alberta Safety Codes and Alberta Building Code — location TBD

---

## Steps

### Step 1 — Confirm Scope and Design Basis

1.1 Review App B-Elec (R-05) and extract the lighting fixture inventory:
- Main shop: 5 rows × 4 = 20 high bay LED fixtures @ 150W, 22,000 lm.
- Wash bay: 2 rows × 3 = 6 high bay fixtures (specifications TBD — see CONF-LT-001).
- Office: 1 × 8' LED.
- Utility room: 2 × 8' LED.
- Parts/tool room: 6 × 8' LED.
- Service pit/trench: lighted (type TBD — see CONF-LT-002).

1.2 Confirm building dimensions and zone geometry from architectural floor plans (DEL-001-02) once available. Reference dimensions: 130' × 100' overall; 35' ceiling height; 24' wash bay width.

1.3 Confirm code requirements: identify applicable CEC edition, Alberta amendments, and any Safety Code authority requirements for lighting in heavy-equipment industrial occupancies.

1.4 Assess emergency and exit lighting requirements per applicable code (see CONF-LT-003).

Source: App B-Elec; RFP §3.4; RFP §3.3.2.

### Step 2 — Develop Preliminary Lighting Layout (for DEL-004-01)

2.1 Place fixture symbols on a floor plan background (to scale) matching the layout shown in App B-Elec.

2.2 Assign preliminary circuit designations to each zone's fixtures (zone-based grouping recommended — see Guidance C-2).

2.3 Identify preliminary switching scheme per zone.

2.4 Perform or commission photometric calculations for the main shop (35' ceiling, 150W/22,000 lm high bays) to verify adequate illuminance.
  - **Conditionality note [F-003]:** If a separate Electrical Calculation Package (DEL-004-08) is being produced, photometric calculations may be performed as part of that deliverable rather than duplicated here. However, the Electrical Engineer shall confirm before proceeding past Step 2.7 whether: (a) photometric calculations will be performed under DEL-004-08, or (b) photometric calculations will be performed as part of this deliverable's workflow. If (a), record the dependency and confirm that DEL-004-08 results will be available before IFC issue. If (b), perform the calculations as part of this step.
  - **Trigger criteria:** Photometric calculation is required whenever illuminance targets are specified (see REQ-LT-012) or when code compliance requires demonstration of adequate illuminance. If no illuminance targets are established, this step remains as a TBD pending REQ-LT-012 resolution.

2.5 Specify or shortlist fixture products for all zones:
- Main shop / wash bay: high bay LED (150W for main shop; wash bay specifications TBD).
- Office, utility, parts/tool room: 8-foot LED strip fixtures.
- Service pit: wet/damp-location fixture (TBD).

2.5a **Service Pit Fixture Selection [A-005]:** The service pit fixture selection requires a dedicated resolution path:
  1. Assess the service pit environment: determine whether the location is classified as a wet location, damp location, or hazardous location per the applicable CEC edition (TBD -- see REQ-LT-008).
  2. Determine impact resistance requirements: service pits in heavy equipment maintenance shops are subject to physical hazard from tools, equipment, and vehicle movement. Select fixtures rated for the expected impact exposure.
  3. Identify candidate fixture products: select fixtures suitable for the assessed environment classification, with appropriate enclosure rating (IP rating / CEC wet-location marking), impact resistance, and lumen output appropriate for the service pit task (close-range inspection lighting from below).
  4. Determine quantity and mounting positions: based on service pit dimensions (TBD -- from DEL-001-02 architectural drawings) and required illuminance level (TBD -- see REQ-LT-012).
  5. Document selection in the fixture schedule (Step 4.2) and update Datasheet.md accordingly.
  6. If the service pit environment classification or fixture selection cannot be resolved at preliminary design, document it as a TBD in the preliminary design submission (DEL-004-01) and flag for resolution before IFC issue.

2.6 Coordinate with Mechanical Engineer regarding ceiling fan locations (6 fans in main shop, SOW-0040) and exhaust fan locations (App B-Elec "E" symbols) to confirm no fixture conflicts.

2.7 Package preliminary lighting layout as part of DEL-004-01 (Preliminary Electrical Design) for County approval.

Source: App B-Elec; RFP §3.3.2; SOW-0010d.

### Step 3 — Obtain County Approval of Preliminary Design

3.1 Submit DEL-004-01 (Preliminary Electrical Design) to County for approval per RFP §3.3.2.

3.2 Document any County-directed changes to the lighting layout. Incorporate approved changes before proceeding to final design.

3.3 Record approval in the project file.

Source: RFP §3.3.2; SOW-0010d; SOW-0086.

### Step 4 — Produce Final Lighting Plans Drawing Set (IFC Quality)

4.1 Produce plan-view lighting layout drawing(s) at a scale appropriate for construction use, showing:
- All fixture symbols per zone, with circuit designations.
- Fixture tags cross-referenced to the fixture schedule.
- Switching legend.
- Zone labels consistent with architectural drawings.
- Drawing reference to related electrical drawings (Single-Line, Power Distribution, Panel Schedules).

4.2 Produce Fixture Schedule on drawing or as separate schedule sheet, including:
- Zone / area.
- Fixture type designation.
- Manufacturer and model (or performance specification if prescriptive).
- Wattage (W).
- Lumen output (lm).
- Voltage / phase.
- Mounting type.
- Enclosure rating (IP / wet-location rating where applicable).
- Quantity.

4.3 Add construction notes addressing:
- Mounting heights / pendant lengths for high bay fixtures.
- Wet-location requirements for wash bay and service pit fixtures.
- Coordination notes for ceiling fan and exhaust fan locations.

4.4 Coordinate circuit IDs with:
- DEL-004-03 Power Distribution Plans (circuit routing).
- DEL-004-06 Panel Schedules (breaker sizing, panel assignment).

4.5 Confirm that emergency and exit lighting (if required by code — see CONF-LT-003) is shown on the drawings or on a separate life-safety drawing sheet.

Source: RFP §3.3.2; SOW-0014; App B-Elec; SOW-0018.

### Step 5 — Internal Review and Quality Check

5.1 Verify fixture counts against App B-Elec specifications:
- Main shop: 20 fixtures (5 rows × 4). Wattage: 150W. Lumens: 22,000.
- Wash bay: 6 fixtures (2 rows × 3).
- Office: 1 × 8' LED.
- Utility room: 2 × 8' LED.
- Parts/tool room: 6 × 8' LED.
- Service pit: lighted (per design resolution).

5.2 Verify all circuit IDs on lighting plans match those in Panel Schedules (DEL-004-06).

5.3 Verify drawing title block is complete: project name, drawing number, revision, date, scale.

5.4 Confirm drawing is production-ready for P.Eng. review and stamp.

### Step 6 — P.Eng. Review and Stamp

6.1 Professional Engineer licensed in Alberta reviews the Lighting Plans for:
- Code compliance (CEC, Alberta Safety Codes, Alberta Building Code).
- Accuracy of fixture schedule.
- Adequacy of circuit designations and panel coordination.
- Completeness of construction notes.

6.2 P.Eng. stamps and signs the drawing set.

6.3 IFC drawings are issued. Drawing set is formally released as DEL-004-04 Lighting Plans (IFC).

Source: RFP §3.3.2; SOW-0018.

### Step 7 — Transmit to Downstream Users

7.1 Provide IFC Lighting Plans to:
- PKG-015 Electrical Contractor (for lighting installation per DEL-015-02).
- PKG-009 Permitting (Safety Code permit application — DEL-009-03).
- PKG-020 Commissioning (reference for system commissioning — DEL-020-01).

7.2 Confirm transmittal is logged.

Source: Decomposition §7 PKG-015, PKG-009, PKG-020.

---

## Verification

| Check | Method | Pass Criteria |
|---|---|---|
| Fixture count — main shop | Count fixtures on plan | 20 (5 rows × 4), 150W LED, 22,000 lm |
| Fixture count — wash bay | Count fixtures on plan | 6 (2 rows × 3) |
| Fixture count — office | Count fixtures on plan | 1 × 8' LED |
| Fixture count — utility room | Count fixtures on plan | 2 × 8' LED |
| Fixture count — parts/tool room | Count fixtures on plan | 6 × 8' LED |
| Service pit lighting shown | Check plan | At least one fixture symbol at service pit location |
| Fixture schedule complete | Review schedule | All fixtures have type, wattage, lumens, enclosure rating, quantity |
| Circuit IDs match Panel Schedules | Cross-check DEL-004-06 | No orphan circuits; all circuits accounted for |
| P.Eng. stamp and signature | Title block review | Stamp and signature present from P.Eng. licensed in Alberta |
| County preliminary approval obtained | Project file | Approval letter/record on file before IFC issue |
| Code compliance | P.Eng. attestation against confirmed code editions (see REQ-LT-008 [A-004/F-001]) | Engineer's stamp certifies compliance; code editions verified against are documented |
| Mechanical coordination [X-004] | Overlay check of ceiling fan (6 units) and exhaust fan positions against high bay fixture positions on lighting plan | No spatial conflicts between fan locations and fixture locations; coordination confirmed with Mechanical Engineer |
| Illuminance adequacy [D-002] | Photometric calculation results per REQ-LT-012 (if illuminance targets defined) | Each zone meets or exceeds minimum maintained illuminance target; TBD until targets are established |

---

## Records

The following records shall result from this procedure:

| Record | Purpose | Retained By |
|---|---|---|
| DEL-004-04 Lighting Plans — IFC drawing set (PDF and native format) | Construction reference; permit submission | Design-Builder / PKG-004 |
| Fixture schedule (on drawing or separate) | Procurement and installation reference | Design-Builder / PKG-004 |
| Photometric calculation output (if produced) | Code compliance evidence; part of DEL-004-08 | Design-Builder / PKG-004 |
| County approval record for preliminary design (DEL-004-01) | Confirms Owner approval before IFC issue | Design-Builder / Project Manager |
| P.Eng. stamp record | Professional liability and permit compliance | Electrical Engineer |
| Transmittal log to PKG-015 and PKG-009 | Confirms downstream delivery | Project Manager |

### Revision Control and Change Tracking [X-005]

Design changes to the Lighting Plans after initial IFC issue (or after County preliminary approval) shall be documented and traced using the following provisions:

| Element | Description |
|---|---|
| Revision numbering | Each revision to the drawing set shall carry an incremented revision number (e.g., Rev 0, Rev 1, Rev 2) in the title block. |
| Revision log | A revision log (on the drawing or in a separate document) shall record: revision number, date, description of change, reason for change, and approving authority. |
| Delta cloud / revision marks | Changed areas on the drawings shall be identified with revision clouds or delta marks per standard drawing practice. |
| Re-stamping | If changes affect code compliance or structural coordination, the P.Eng. shall re-review and re-stamp the revised drawing set. |
| Downstream notification | When revised drawings are issued, downstream users (PKG-015, PKG-009, PKG-020) shall be notified via updated transmittal. |

ASSUMPTION: Revision control provisions are based on standard engineering drawing practice for IFC document sets. The Project Manager or QA lead should confirm whether the project has a specific document control procedure that supersedes these provisions.
