# Procedure — DEL-02-05: Electrical/IT Concept Narrative

---

## Purpose

This procedure describes the steps to **produce** the Electrical/IT Concept Narrative — the artifact that constitutes DEL-02-05. This document is authored by the Electrical Engineer as the discipline-specific contribution to the PKG-002 Conceptual Design package.

The output is a standalone narrative suitable for inclusion in the RFP proposal response under Section 7.1.1 (Proposed Conceptual Design). It covers: electrical service and distribution, LED lighting, generator transfer switching, IT/telecommunications, access control provisions, security / camera provisions, solar-capable roof electrical provisions, fire alarm, and fill station electrical supply.

(Source: _CONTEXT.md; RFP 7.1.1; Decomposition §8 PKG-002; SOW-0009, SOW-0010)

---

## Prerequisites

### Information Prerequisites

| Item | Description | Owner Deliverable |
|---|---|---|
| Architectural Concept (draft) | Building floor plan(s), zone layout, MER location, mechanical room location, roof orientation | DEL-02-01 |
| Mechanical Concept (draft) | Generator type, fuel selection, placement / mechanical room layout, fill station plumbing locations | DEL-02-04 |
| Civil/Site Concept (draft) | Utility entry point(s), site electrical distribution approach | DEL-02-02 |
| Structural Concept (draft) | Roof loading concept, roof penetration strategy | DEL-02-03 |

### Reference Materials

| Reference | Relevance |
|---|---|
| RFP Section 7.1.1 | Proposed Conceptual Design requirements and evaluation criteria |
| RFP Appendix A (OSR) | Owner Statement of Requirements — space program and functional requirements |
| RFP Appendix B (Functional Program) | Room program; equipment and power requirements by space |
| Addendum 03 | Generator essential loads; solar-capable roof orientation; fill station requirements; security supplier note; program clarifications |
| IES Recommended Practices | LED lighting footcandle targets and fixture selection guidance |
| Alberta Building Code / NBCC | Electrical, fire alarm, and life safety code requirements |
| Alberta Fire Code | Fire alarm system requirements |
| Canadian Electrical Code Part I | Electrical installations standard |
| Decomposition v2.3 FINAL | Scope items SOW-0009, SOW-0010; objectives; vocabulary; cross-deliverable relationships |

### Team

| Role | Contribution |
|---|---|
| Electrical Engineer | Primary author; all electrical sections |
| IT / Telecom Consultant | Supporting author for IT/telecommunications section (ASSUMPTION: available; if not, Electrical Engineer drafts with TBD notes) |
| Mechanical Engineer | Generator coordination confirmation (fuel type, location, sizing) |
| Architect | Architectural layout coordination (MER location, switchgear room, roof orientation) |
| Proposal Manager | Final review and proposal assembly |

---

## Steps

### Step 1 — Assemble Source Information and Build Requirements Checklist

**Duration:** 2–3 hours

1. Collect draft floor plans from Architect (DEL-02-01 in-progress version).
2. Collect generator assumptions from Mechanical Engineer (DEL-02-04 in-progress version): fuel type, estimated kW output, location.
3. Collect utility entry point from Civil Engineer (DEL-02-02 in-progress version).
4. Read and annotate RFP Section 7.1.1 and Addendum 03 for all electrical-relevant requirements.
5. Construct an Addendum 03 Electrical Checklist:

| Addendum 03 Item | Electrical Implication | Section of Narrative |
|---|---|---|
| Generator: kitchen, ICP, 2 bathrooms, bay door secondary | Essential panel and ATS design | §3 Generator |
| Solar-capable roof (flat/south/west/southwest) | Conduit, breaker space, inverter stub-out | §7 Solar Provisions |
| 2" fill stations — 1 fire bay, 1 PW bay | Dedicated 240V circuits | §9 Fill Stations |
| No Town supplier preference on security/cameras | Neutral system description in security section | §6 Security |
| 40 bunker gear lockers + room ventilation | Ventilation fan motor supply (coordinate DEL-02-04) | §2 Lighting / §8 Fire Alarm |
| 16 ft overhead doors — bay door secondary opening | Electrical supply to secondary door mechanism | §3 Generator essential load |
| Bay sumps — snow melting, minor washing | Electrical supply to sump pump (if electrically operated) | §1 Distribution |

6. Confirm all items in the checklist have an assigned narrative section before proceeding.

**Output:** Annotated requirements checklist; confirmed architectural and mechanical interface assumptions.

---

### Step 2 — Develop Electrical Service and Distribution Concept

**Duration:** 3–5 hours

1. Establish main service entry point based on civil utility layout (DEL-02-02).
2. Determine main switchgear location — coordinate with mechanical room in DEL-02-01.
3. Sketch branch distribution approach: sub-panels per zone (apparatus bays, offices, kitchen, residential quarters, Cold Storage feed).
4. Identify essential panel location and ATS location relative to main switchgear and generator (from DEL-02-04).
5. Address Cold Storage building feed: separate metering? Sub-panel location? Freeze-rated equipment?
6. Address sump pump electrical supply if electrically operated (coordinate with DEL-02-04 on sump design).
7. Document service assumptions for voltage level and service size. At concept stage, the Electrical Engineer should:
   - **Voltage level:** State the assumed utility voltage (typically 120/208V 3-phase for facilities under ~200A service, or 347/600V 3-phase for larger facilities requiring step-down transformers). Selection depends on estimated total connected load, utility provider standard offerings in the Penhold/Central Alberta area, and equipment voltage requirements (e.g., large motor loads may favor higher voltage). Record the assumed voltage as TBD with the rationale for the assumed range pending utility provider confirmation and detailed load calculation.
   - **Service size:** State the assumed service amperage range based on a preliminary load estimate (sum of major load categories from Steps 2-9). Typical range for a combined fire hall / public works facility of this scale: ASSUMPTION 400A–800A at 120/208V, or 200A–400A at 347/600V. Final service size is determined at detailed design after full load calculation.
   - Record all assumptions explicitly as ASSUMPTION items. (Semantic Lensing B-003)

**Verification (V-001):** Service entry, switchgear location, and sub-panel zones are consistent with architectural floor plan from DEL-02-01. Cold Storage addressed.

**Output:** Electrical distribution concept sketch; assumptions list.

---

### Step 3 — Develop LED Lighting Concept

**Duration:** 3–4 hours

1. Identify all space categories from RFP Functional Program (Appendix B) and DEL-02-01 floor plan.
2. Assign LED lighting approach and ASSUMPTION illuminance target to each space category:

| Space Category | ASSUMPTION Illuminance Target | Fixture Type | Control Approach |
|---|---|---|---|
| Fire apparatus bays (high-bay) | 300–500 lux | LED high-bay; dusty environment rated | Manual on/off; occupancy dimming optional |
| PW apparatus / workshop bays | 200–300 lux | LED high-bay | Manual on/off |
| Administrative offices | 300–400 lux | LED panel troffer | Occupancy sensor + manual override |
| Residential quarters | 150–200 lux | LED surface / recessed | Manual + occupancy sensor in corridors |
| Kitchen | 300–400 lux | LED surface | Manual on/off |
| Training / ICP meeting room | 300–400 lux | LED panel; dimmer optional | Manual dimmer |
| Bathrooms | 200–300 lux | LED surface | Occupancy sensor; 5-min timeout |
| Storage / support spaces | 100–150 lux | LED strip or surface | Occupancy sensor |
| Corridors and exits | 150–200 lux | LED surface | Occupancy assist; emergency lighting circuit |
| Exterior / site | 20–50 lux (ASSUMPTION: IES RP-6 parking area guidance) | LED area / wall pack | Photo sensor + scheduling |
| Cold Storage building | TBD lux | Freeze-rated LED strip (rated to –40°C) | Manual on/off |

3. Note IES standard references (specific RP numbers to be confirmed by Electrical Engineer; e.g., RP-5 for roadway, RP-6 for parking, and IES DG-4 for emergency egress — ASSUMPTION).
4. Address emergency lighting: dedicated circuit, LED egress luminaires, battery backup minimum 90 minutes (ASSUMPTION: Alberta Building Code minimum).
5. Address exit signs: LED with integral battery backup.
6. Coordinate with Mechanical on ventilation for high-intensity areas (apparatus bay heat load).

**Verification (V-002):** All space categories from Functional Program addressed. IES reference cited. Emergency lighting and exit signs addressed.

**Output:** Lighting concept table (space category × illuminance × fixture × control); IES reference list; emergency lighting strategy.

---

### Step 4 — Develop Generator Connection and Transfer Switching Concept

**Duration:** 2–3 hours

1. Obtain confirmed generator parameters from DEL-02-04: fuel type (diesel / natural gas / propane — TBD), kW output, voltage, location.
2. Establish essential load list, consistent with Addendum 03 minimum:

| Essential Load | Estimated Demand |
|---|---|
| Kitchen equipment | ~15 kW (ASSUMPTION) |
| Meeting room / ICP | ~5 kW (ASSUMPTION) |
| Two bathrooms | ~3 kW (ASSUMPTION) |
| Bay door secondary opening mechanism | ~2 kW (ASSUMPTION) |
| **Subtotal** | ~25 kW |
| Design margin (20%) | ~5 kW |
| **Recommended essential panel capacity** | ~30 kW |

3. Describe ATS type: automatic transfer switch (ATS), open transition (de-energize before transfer — standard practice for standby generators).
4. Describe load shedding logic (if demand exceeds essential panel capacity, non-critical loads shed first).
5. State that generator sizing, fuel, and enclosure are per DEL-02-04.
6. Note that ATS provides manual bypass for maintenance.

**Verification (V-003):** Essential load list matches all four Addendum 03 minimum loads. Coordination statement with DEL-02-04 present. ATS type described.

**Output:** Essential load list table; ATS concept description; coordination notes.

---

### Step 5 — Develop IT / Telecommunications Infrastructure Concept

**Duration:** 3–4 hours

1. Identify IT-intensive spaces from Functional Program: fire dispatch, administrative offices, ICP meeting room, PW operations, training room.
2. Propose Main Equipment Room (MER) location: secure, climate-controlled, accessible — coordinate with DEL-02-01 floor plan.
3. Describe cabling architecture:
   - Fiber backbone from MER to distribution points (future bandwidth capacity for 50-year facility).
   - Cat 6A (ASSUMPTION) copper horizontal cabling from distribution to all workstations, IP phones, and network devices.
   - 25% spare conduit capacity reserved for future cabling expansion (ASSUMPTION: standard practice).
4. Describe network zones (VLANs): fire dispatch / CAD, administrative, building systems (access control, CCTV, BAS), guest / visitor (if applicable).
5. Address UPS for MER: continuous power during utility outage; bridge power until generator online; ASSUMPTION 4-hour runtime target.
6. Address IT interface with fire dispatch CAD system: dedicated VLAN, QoS prioritization.
7. Note that Internet service entry point and carrier coordination are subject to Town utility availability (TBD at detailed design).

**Verification (V-004):** MER location coordinated with DEL-02-01. Cabling architecture described (fiber backbone + copper horizontal). Spare capacity noted. UPS addressed. Network zone strategy described.

**Output:** IT infrastructure concept (MER location, cabling architecture, network zones, UPS strategy).

---

### Step 6 — Describe Access Control and Security Provisions (Additional Options 3 and 4)

**Duration:** 2–3 hours

1. **Access Control — Option 3:**
   - Identify entry points for card reader / keypad access concept: main public entrance, apparatus bay entry, administrative area, residential quarters corridor, secure storage areas.
   - Describe infrastructure provisions in base design: dedicated conduit to each reader location, controller location in or adjacent to MER, 120V dedicated circuit for access control equipment.
   - Note fail-safe release on fire alarm activation (code requirement — ASSUMPTION: applicable per Alberta Fire Code).
   - State that complete access control system is Additional Option 3 (Schedule A/B); base design provides infrastructure only.

2. **Security / Cameras — Option 4:**
   - Identify camera coverage concept: apparatus bays, exterior parking areas, main building entries, interior secure areas.
   - Describe infrastructure provisions in base design: conduit or cable tray to camera locations (PoE or dedicated power — TBD), NVR/VMS space allocation in MER, network capacity on CCTV VLAN.
   - Note no Town supplier preference per Addendum 03.
   - State that complete CCTV system is Additional Option 4 (Schedule A/B); base design provides infrastructure only.

**Verification (V-005):** Option 3 provisions described with retrofit capability. Option 4 provisions described; no supplier named. Both options explicitly identified as Additional Options, not base scope.

**Output:** Access control and security provisions concept; infrastructure reservation list; optional system scope description.

---

### Step 7 — Describe Solar-Capable Roof Electrical Provisions

**Duration:** 2–3 hours

1. Confirm roof orientation from DEL-02-01: flat, south, west, or southwest per Addendum 03 — this is an established design parameter.
2. Describe electrical provisions for future PV installation:
   - 2-inch conduit routed from main switchgear room to roof penetration point, sized for future PV DC output conductors.
   - Two spare 60A (ASSUMPTION) breaker spaces reserved in main distribution panel for future solar inverter AC output connection.
   - Floor space allocation (ASSUMPTION: 4 linear feet) adjacent to main switchgear for future inverter assembly.
   - Utility interconnection coordination pathway noted (subject to AUC approval at time of solar installation).
3. State clearly: provisions are included in base electrical scope; PV panels, mounting hardware, and inverter are not included in this proposal.
4. Note coordination with Architect on roof penetration flashing and with Mechanical on inverter room ventilation.

**Verification (V-006):** Roof orientation stated and consistent with Addendum 03. Three provision elements described (conduit, breaker space, inverter space). Clear statement distinguishing provisions from solar installation.

**Output:** Solar provisions section; coordination notes with DEL-02-01 and DEL-02-04.

---

### Step 8 — Describe Fire Alarm System Concept

**Duration:** 2–3 hours

1. Specify FACP type: addressable analog (preferred for multi-zone municipal facility — allows zone-by-zone annunciation and flexible future expansion).
2. Describe detector placement concept by zone:
   - Smoke detectors: all occupied spaces, corridors, mechanical rooms, storage areas.
   - Heat detectors: apparatus bays (high ambient temperatures may defeat smoke detection — ASSUMPTION: standard practice for fire hall environments).
   - Duct smoke detectors: major HVAC supply ducts (interface with mechanical — coordinate DEL-02-04).
3. Describe manual pull stations: all stairwells, major exits, apparatus bay entry doors (ASSUMPTION: Alberta Building Code spacing requirements).
4. Describe audio/visual notification appliances: all occupied spaces, apparatus bays, exterior.
5. Address HVAC interface: fire alarm activates apparatus bay exhaust fans; shuts down HVAC supply in alarm condition (coordinate with DEL-02-04).
6. Address emergency lighting: dedicated circuit, LED egress luminaires, 90-minute battery backup (ASSUMPTION: Alberta Building Code minimum), exit signs with integral battery.
7. Note 24/7 monitoring service (TBD — typically contracted by Owner).
8. Reference code compliance pathway: Alberta Building Code, Alberta Fire Code, ULC S524 (ASSUMPTION).

**Verification (V-007):** Addressable FACP specified. All space categories addressed for detection. HVAC interface noted. Emergency lighting addressed. Code references included.

**Output:** Fire alarm concept section; component placement description; code compliance statement.

---

### Step 9 — Describe Water Fill Station Electrical Supply

**Duration:** 1–2 hours

1. Confirm fill station locations from Addendum 03: 1 fire apparatus bay, 1 PW bay (2" minimum per station).
2. Coordinate with DEL-02-04 on pump type and motor voltage.
3. Describe electrical supply provisions:
   - Dedicated 240V, single-phase (ASSUMPTION) circuit to each fill station pump motor.
   - Weatherproof disconnects or combination starters at each fill station.
   - Conduit routing from respective sub-panels to fill station locations.
   - ASSUMPTION: fill stations are not on the essential panel (non-critical load); confirm with Owner at detailed design if fire apparatus fill station should be on generator backup.

**Verification (V-008):** Both fill station locations confirmed. Electrical supply concept described. Coordination with DEL-02-04 noted.

**Output:** Fill station electrical supply section; circuit description.

---

### Step 10 — Integration Review and Draft Narrative

**Duration:** 5–7 hours

1. **Integration check:** Confirm all content sections from Specification.md (R-EL-01 through R-EL-17) are addressed in draft narrative.
2. Confirm all Addendum 03 Electrical Checklist items (from Step 1) are resolved in a specific narrative section.
3. Confirm electrical concept is spatially consistent with DEL-02-01 architectural layout.
4. Confirm generator section does not contradict DEL-02-04 approach.
5. Assemble narrative document with sections in order matching Specification.md scope:
   - §1 Electrical Service and Power Distribution
   - §2 Lighting — LED per IES
   - §3 Generator Connection and Transfer Switching
   - §4 IT / Telecommunications Infrastructure
   - §5 Access Control Provisions (Option 3)
   - §6 Security / Camera Provisions (Option 4)
   - §7 Solar-Capable Roof Electrical Provisions
   - §8 Fire Alarm System
   - §9 Water Fill Station Electrical Supply
   - §10 PA / Paging System (if applicable — TBD pending Owner confirmation; see R-EL-17)
   - §11 Codes and Standards Compliance
   - §12 Coordination with Other Disciplines (summary)
6. Incorporate assumptions explicitly labeled as ASSUMPTION throughout.
7. Confirm narrative tone is professional, technically credible, and proposal-appropriate (persuasive without overstating certainty).

**Verification (V-009):** All specification requirements addressed. Addendum 03 checklist complete. Cross-discipline consistency confirmed. Narrative ready for QA review.

**Output:** Complete draft Electrical/IT Concept Narrative.

---

### Step 11 — QA Review and Sign-Off

**Duration:** 2–3 hours

Perform the following review checklist before finalizing:

| Check | Reviewer | Pass Criteria |
|---|---|---|
| Addendum 03 integration | Electrical Engineer | All checklist items from Step 1 addressed |
| Generator coordination | Mechanical Engineer | No contradictions with DEL-02-04 |
| Architectural consistency | Architect | MER location, switchgear room, and zone descriptions match DEL-02-01 |
| Essential load list | Electrical Engineer | All four Addendum 03 minimum loads confirmed |
| Solar provisions | Electrical Engineer | Conduit, breaker space, inverter stub-out described; orientation stated |
| Options 3 and 4 clarity | Proposal Manager | Base vs. optional scope clearly distinguished |
| IES reference | Electrical Engineer | IES standard cited; space-by-space approach present |
| Code references | Electrical Engineer | Alberta Building Code, Alberta Fire Code, CEC Part I, ULC S524 cited |
| Assumptions labeled | Proposal Manager | All ASSUMPTION items clearly labeled |
| No supplier named (cameras) | Proposal Manager | Security section contains no specific supplier name per Addendum 03 |
| PA/paging system | Electrical Engineer | PA/paging system addressed or explicitly excluded per R-EL-17 |

**Verification (V-010):** All QA checklist items pass. Sign-off received from Electrical Engineer and Proposal Manager.

**Output:** Finalized Electrical/IT Concept Narrative — ready for proposal assembly.

---

## Verification

| Verification ID | Checkpoint | Source Requirement |
|---|---|---|
| V-001 | Electrical service and distribution concept consistent with DEL-02-01 | R-EL-01 |
| V-002 | LED lighting space-by-space approach; IES cited; emergency lighting addressed | R-EL-02, R-EL-03 |
| V-003 | Essential load list complete; ATS described; DEL-02-04 coordination noted | R-EL-04, R-EL-05 |
| V-004 | IT concept: MER location, cabling architecture, network zones, UPS | R-EL-06 |
| V-005 | Option 3 and Option 4 provisions; no supplier; base vs. optional distinction | R-EL-07, R-EL-08 |
| V-006 | Solar provisions: conduit, breaker space, inverter stub-out; orientation confirmed | R-EL-09 |
| V-007 | Fire alarm: addressable FACP; detectors; HVAC interface; code references | R-EL-10 |
| V-008 | Fill station electrical supply: both locations; electrical concept | R-EL-11 |
| V-009 | All Addendum 03 items addressed in narrative; R-EL-14 through R-EL-17 addressed | R-EL-12, R-EL-14, R-EL-15, R-EL-16, R-EL-17 |
| V-010 | Full QA review and sign-off; final consistency check with DEL-02-01 | R-EL-13 |
| V-011 | PA/paging system addressed or explicitly excluded | R-EL-17 |

---

## Records

| Record | Description |
|---|---|
| Electrical/IT Concept Narrative | Final narrative document (DEL-02-05 primary artifact) |
| Addendum 03 Electrical Checklist | Completed checklist from Step 1 confirming all program requirements addressed |
| Cross-discipline Coordination Notes | Notes from Mechanical, Architectural, and Civil coordination confirming interface assumptions |
| QA Sign-Off Documentation | Completed review checklist with reviewer identification |

---

## Notes

1. **Generator coordination dependency:** Steps 4 and 9 depend on fuel type and pump voltage from DEL-02-04. Obtain these assumptions from the Mechanical Engineer before finalizing those sections.
2. **Architectural layout dependency:** Steps 2, 3, 5, and 7 depend on a draft floor plan from DEL-02-01. Ensure that deliverable is at least in schematic form before authoring this narrative.
3. **Addendum 03 is mandatory, not optional:** The solar provisions (Step 7) and fill station provisions (Step 9) are Addendum 03 requirements, not enhancements. They must be in the base narrative.
4. **Options 3 and 4 scope discipline:** The narrative must be explicit that base design provides infrastructure only; the complete access control and CCTV systems are priced as Additional Options 3 and 4 in Appendix H. This prevents pricing ambiguity.
5. **IES citation:** Before finalizing Step 3, confirm which IES Recommended Practice documents are applicable (e.g., RP-6 for parking, RP-5 for roadway, IES DG-4 for emergency egress). Cite specific documents in the narrative.
6. **Pitfall — generic statements:** Avoid stating "LED lighting will be provided throughout" without space-by-space qualification. Evaluators expect the Electrical Engineer to demonstrate awareness of the different operational environments in the PSB.
7. **Duration estimate basis:** The duration estimates in Steps 1-11 (ranging from 1-2 hours to 5-7 hours) assume: (a) a single Electrical Engineer as primary author with supporting input from other disciplines as noted in the Team table; (b) draft architectural and mechanical concepts are available (not authored in parallel); (c) the Electrical Engineer has prior experience with municipal fire hall / public works facilities of comparable scope; (d) reference materials (RFP, Addendum 03, IES standards, applicable codes) have been reviewed at least once before starting. For less experienced teams or projects where upstream deliverables are less mature, durations may increase by 50-100%. The total estimated effort for Steps 1-11 is approximately 28-40 hours of Electrical Engineer time. (Semantic Lensing D-001)
