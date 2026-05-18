# Specification — DEL-013-02: High-Volume Air Exchanger

---

## Scope

### What This Deliverable Covers

DEL-013-02 covers the procurement, delivery, installation, integration, and commissioning of a high-volume air exchanger (heat recovery ventilator / energy recovery ventilator) for the New North Shop addition at the West Dried Meat Lake Regional Landfill, near Ferintosh, Alberta.

The air exchanger system is required to:
- Exchange stale facility air with fresh outside air at high volume suitable for the ~13,000 sq ft industrial maintenance shop with 35 ft ceilings.
- Recover thermal energy from the exhaust air stream to reduce heating load on the facility.
- Distribute fresh air to all facility areas and remove stale/contaminated air.
- Integrate with the High-Recovery Heating System (DEL-013-01) and coordinate with the Forced-Air Makeup System (DEL-013-03), Heavy Equipment Exhaust System (DEL-013-04), and Welding Station Exhaust System (DEL-013-05).

Specific work included in scope (Source: _CONTEXT.md):
1. Equipment procurement and delivery
2. Equipment installation in the Utility Room
3. Fresh air intake ductwork installation
4. Exhaust outlet ductwork installation
5. Integration with heating system (DEL-013-01)
6. Controls and sensor setup
7. Performance testing and commissioning

### What This Deliverable Excludes

- Mechanical design documentation (covered by PKG-003 — Mechanical Design; deliverable DEL-003-02 HVAC Plans, DEL-003-03 Ductwork Plans)
- Utility Room construction (covered by DEL-012-02)
- Forced-Air Makeup System installation (covered by DEL-013-03)
- Heavy Equipment Exhaust System (covered by DEL-013-04)
- Welding Station Exhaust System (covered by DEL-013-05)
- Electrical power feed to the unit (covered by PKG-015 Electrical Installation; ASSUMPTION — specific electrical work scope boundary to be confirmed at design stage)
- Building exterior wall penetration structural detailing (covered by architectural/structural design packages)

---

## Requirements

### REQ-001 — Equipment Performance: Air Exchange Capacity
**Requirement:** The air exchanger shall be sized to provide high-volume air exchange for the facility volume. Minimum ventilation rate shall comply with ASHRAE 62.1 (Ventilation for Acceptable Indoor Air Quality) for the applicable occupancy type (industrial maintenance/vehicle maintenance shop). **The specific ASHRAE 62.1 occupancy category and ventilation rate procedure (Ventilation Rate Procedure or IAQ Procedure) applicable to this industrial maintenance shop shall be identified by the Mechanical Engineer; this determination may significantly affect airflow sizing.** (Lensing item A-001)
**Source:** R-01 §3.4 "High volume air exchanger"; _CONTEXT.md Key Requirements; ASSUMPTION: ASHRAE 62.1 applicability inferred — exact requirement, occupancy category, and rate procedure to be confirmed by Mechanical Engineer in DEL-003-07.
**Verification:** Performance test confirming design airflow rate (CFM/L/s) during commissioning.

### REQ-002 — Equipment Performance: Heat Recovery
**Requirement:** The air exchanger shall incorporate a heat recovery core that recovers thermal energy from the exhaust air stream. The heat recovery efficiency (sensible and/or total) shall meet or exceed applicable code and energy-efficiency standards for the Alberta climate zone. **A minimum numeric heat recovery efficiency target (percentage) shall be specified by the Mechanical Engineer in DEL-003-07; TBD pending design.** (Lensing item B-002)
**Source:** _CONTEXT.md: "Heat recovery efficiency" listed as Key Requirement; R-01 §3.4 "High recovery heating system" (context — ASSUMPTION that heat recovery function is required on the air exchanger as well, consistent with system description in _CONTEXT.md).
**Verification:** Manufacturer's published efficiency data; commissioning test data. **Heat recovery performance test conditions shall be defined: specify outdoor temperature, indoor temperature, airflow rate, and baseline against which efficiency is measured during commissioning. TBD — Mechanical Engineer to define commissioning test protocol in DEL-003-07.** (Lensing item D-002)

### REQ-003 — Fresh Air Distribution
**Requirement:** The system shall distribute fresh air to all facility areas, including the main shop, wash bay, repair bays, parts room, utility room, office, and washroom areas.
**Source:** _CONTEXT.md Key Requirements: "Fresh air distribution to all facility areas."
**Verification:** Ductwork design review; air balance test during commissioning.

### REQ-004 — Stale Air Removal
**Requirement:** The system shall collect and exhaust stale and contaminated air from all facility areas. Exhaust shall be discharged to the exterior of the building.
**Source:** _CONTEXT.md Key Requirements: "Stale air removal and exhaust."
**Verification:** Ductwork design review; air balance test during commissioning; negative pressure verification at exhaust points (ASSUMPTION — verification method to be confirmed by Mechanical Engineer).

### REQ-005 — Fresh Air Intake Location
**Requirement:** The fresh air intake shall be located on the building exterior such that it does not re-entrain exhaust air, diesel/vehicle exhaust, or other contaminants. Minimum separation between intake and exhaust shall comply with applicable mechanical code requirements.
**Source:** _DEPENDENCIES.md Constraint Notes: "Fresh air intake location must avoid contamination." ASSUMPTION: Minimum separation distance per National Mechanical Code of Canada or equivalent — confirmed by Mechanical Engineer in design.
**Verification:** Design review by Mechanical Engineer; site inspection.

### REQ-006 — Exhaust Outlet Location
**Requirement:** The exhaust outlet shall be placed to prevent nuisance, contamination, or re-entrainment. Outlet shall comply with setback requirements per applicable mechanical code.
**Source:** _DEPENDENCIES.md Constraint Notes: "Exhaust outlet placement critical for air quality."
**Verification:** Design review; inspection by authority having jurisdiction (AHJ).

### REQ-007 — Integration with Heating System
**Requirement:** The air exchanger shall integrate with the High-Recovery Heating System (DEL-013-01) such that recovered thermal energy can supplement building heating. Controls shall coordinate with the heating system.
**Source:** _CONTEXT.md Scope: "Integration with heating system"; _DEPENDENCIES.md: "Supply of heated air and integration" with DEL-013-01.
**Verification:** Functional test during commissioning confirming coordinated operation.

### REQ-008 — Controls and Sensors
**Requirement:** The air exchanger shall be equipped with controls and sensors appropriate for automatic operation. Controls shall coordinate with the heating system (DEL-013-01). Control type and sensor configuration to be specified by Mechanical Engineer.
**Source:** _CONTEXT.md Scope: "Controls and sensor setup."
**Verification:** Controls commissioning test; sequence of operations verification.

### REQ-009 — Code Compliance
**Requirement:** Installation shall comply with all applicable Alberta Safety Codes, Alberta Building Code (ABC), National Building Code of Canada (NBC), National Mechanical Code of Canada (NMeCC), and any other code or standard required by the authority having jurisdiction in Alberta.
**Source:** R-01 §3.3.2: "The proposed building must adhere to all Alberta Safety Codes"; R-01 §3.3.2: "The building design must adhere to all applicable building codes and regulations."
**Verification:** Inspection and sign-off by Alberta Safety Codes Officer; building permit records. **Acceptance criteria for AHJ inspection shall be defined: the Mechanical Contractor shall prepare an inspection checklist identifying specific items the Safety Codes Officer will inspect for this equipment and what constitutes a pass. The checklist shall reference specific NMeCC provisions applicable to this installation.** (Lensing items A-003, C-002)

### REQ-010 — Sizing for Facility Volume
**Requirement:** The air exchanger shall be sized based on the actual facility volume as determined by final mechanical design. Facility floor area is approximately 13,000 sq ft with 35 ft ceilings (volume approximately 455,000 cu ft — ASSUMPTION pending design confirmation).
**Source:** _DEPENDENCIES.md Constraint Notes: "Air exchanger must be sized for facility volume"; R-01 §3.1 (13,000 sq ft usable area); R-01 §3.4 (35 ft ceiling); R-04 Appendix B (floor plan dimensions 130' × 100').
**Verification:** Mechanical Engineer design calculation confirming unit selection for facility volume.

### REQ-011 — Cold Climate Operation
**Requirement:** The air exchanger and all associated components (ductwork, controls, defrost system) shall be rated and configured for reliable operation in the Alberta cold-climate environment, including freeze protection for the heat recovery core. **The selected unit shall carry a cold-climate certification or manufacturer rating to a minimum design temperature suitable for the project location (TBD — ASSUMPTION: -40C based on Alberta climate extremes; Mechanical Engineer to confirm minimum design temperature).** (Lensing item A-002)
**Source:** ASSUMPTION — based on project location (near Ferintosh, AB; continental cold climate). Manufacturer specifications to confirm cold-climate rating, minimum operating temperature, and defrost provisions.
**Verification:** Manufacturer cold-climate rating documentation confirming minimum design temperature; commissioning in operating condition.

### REQ-012 — Performance Testing and Commissioning
**Requirement:** The Mechanical Contractor shall perform performance testing and commissioning of the air exchanger system. Commissioning results shall be documented and provided to the Owner.
**Source:** _CONTEXT.md Scope: "Performance testing and commissioning"; R-01 §2.14 Completion and Acceptance.
**Verification:** Commissioning report; Owner acceptance.

### REQ-013 — Guarantee Period
**Requirement:** All materials and workmanship shall be guaranteed for a period of two (2) years following the Construction Completion Certificate (CCC). Defects shall be rectified within ten (10) days of written instruction by the Owner.
**Source:** R-01 §2.10 Guarantee Period; R-01 §2.10.6.
**Verification:** CCC issuance; guarantee period tracking.

### REQ-014 — Fire Stopping at Wall Penetrations
**Requirement:** All wall penetrations for fresh air intake and exhaust outlet ductwork shall include fire stopping / firestopping assemblies where ductwork penetrates fire-rated assemblies, per applicable fire code (Alberta Building Code / NBC). TBD — confirm fire rating of penetrated walls and applicable fire stopping requirements. (Lensing item C-003)
**Source:** ASSUMPTION — fire stopping is typically required where ductwork penetrates fire-rated assemblies per NBC and Alberta Building Code; specific applicability TBD pending confirmation of wall fire ratings.
**Verification:** Site inspection confirming fire stopping installed per approved detail; AHJ inspection.

### REQ-015 — Maintenance Access
**Requirement:** The air exchanger unit shall be installed with sufficient clearance on all sides for filter replacement, heat recovery core cleaning, and routine service per manufacturer minimum clearance requirements. (Lensing item X-002)
**Source:** ASSUMPTION — maintenance access is a standard requirement for commercial/industrial HRV/ERV installations; manufacturer clearance requirements TBD pending equipment selection. Procedure Step 3.2 references "service clearances."
**Verification:** Site inspection confirming clearances meet or exceed manufacturer-specified minimums; manufacturer installation checklist.

### REQ-016 — Vibration Isolation
**Requirement:** TBD — confirm whether vibration isolation is required for the air exchanger installation. If required, specify the type of isolation (spring mounts, rubber pads, inertia base) and performance criteria (maximum transmitted vibration). Large industrial HRV/ERV units typically require vibration isolation. (Lensing item F-003)
**Source:** ASSUMPTION — vibration isolation is standard practice for large commercial/industrial rotating equipment; requirement and specification TBD per Mechanical Engineer in DEL-003-07.
**Verification:** Vibration measurement during commissioning (if vibration isolation is specified); visual inspection of isolation installation.

### REQ-017 — Noise and Acoustic Criteria
**Requirement:** TBD — maximum sound level generated by the air exchanger at the nearest occupied workspace shall not exceed TBD dBA. Noise criteria shall consider both equipment noise and ductwork-generated noise. Industrial HRV/ERV units can generate significant noise affecting occupant comfort and workplace safety (hearing protection thresholds). (Lensing item F-004)
**Source:** ASSUMPTION — no acoustic or noise requirement appears in accessible project sources; Mechanical Engineer to specify acoustic criteria in DEL-003-07 or confirm that no specific limit applies beyond general workplace safety regulations.
**Verification:** Noise measurement during commissioning (if acoustic criteria are specified).

### REQ-018 — Independent Commissioning / Air Balance
**Requirement:** TBD — confirm whether independent commissioning or third-party air balancing agency involvement is required, or whether Mechanical Contractor self-certification is acceptable for commissioning evidence. (Lensing item F-001)
**Source:** ASSUMPTION — Specification REQ-012 requires "performance testing and commissioning" but does not specify whether independent verification is required; Owner/Design-Builder to determine.
**Verification:** Engagement letter or contract with independent commissioning agent (if required); or documented Mechanical Contractor self-certification protocol (if acceptable).

---

## Standards

The following standards are identified as applicable or likely applicable. Standards marked ASSUMPTION have not been confirmed against the full text of accessible sources; clause-level requirements TBD pending Mechanical Engineer design. **The Mechanical Engineer shall confirm whether each standard listed below is mandatory or advisory for this Alberta jurisdiction, and identify the exact edition and applicable clauses.** (Lensing item C-001)

| Standard | Applicability | Source / Note |
|---|---|---|
| Alberta Safety Codes Act (Alberta) | Mandatory | R-01 §3.3.2 |
| Alberta Building Code (ABC) — current edition | Mandatory | R-01 §3.3.2 (ASSUMPTION: ABC references NBC with provincial amendments) |
| National Building Code of Canada (NBC) | Mandatory (with AB amendments) | ASSUMPTION: standard code hierarchy for Alberta construction |
| National Mechanical Code of Canada (NMeCC) | Mandatory | ASSUMPTION: applies to HVAC/mechanical installations in Alberta; location TBD |
| ASHRAE 62.1 — Ventilation for Acceptable Indoor Air Quality | Likely applicable | ASSUMPTION — standard for indoor ventilation design; location TBD |
| ASHRAE 90.1 — Energy Standard for Buildings | Likely applicable | ASSUMPTION — may govern HRV efficiency minimums in conjunction with Alberta energy code; location TBD |
| CSA standards for HVAC equipment (as applicable) | Likely applicable | ASSUMPTION — CSA certification typically required for equipment used in Canada; specific standard TBD |
| Manufacturer installation instructions | Required | Equipment not yet selected; TBD |
| CCDC 14–2013 Design-Build Stipulated Price Contract | Governing contract form | R-01 §2.7 |

---

## Verification

| Requirement ID | Verification Method | Stage | Responsible Party |
|---|---|---|---|
| REQ-001 | Airflow rate performance test during commissioning; design calculation review. **Airflow measurement tolerance: TBD (ASSUMPTION: +/-10% of design — to be confirmed normatively by Mechanical Engineer in DEL-003-07).** (Lensing item A-005) | Construction / Commissioning | Mechanical Contractor / Mechanical Engineer |
| REQ-002 | Manufacturer published heat recovery efficiency data; commissioning measurement | Procurement / Commissioning | Mechanical Contractor / Mechanical Engineer |
| REQ-003 | Air balance test; ductwork design review. **Air balance report shall include: measurements by zone, supply/return/exhaust flow rates at each register/grille, total system airflow, and comparison to design values.** (Lensing item X-004) | Commissioning | Mechanical Contractor / Commissioning Agent |
| REQ-004 | Air balance test; exhaust flow verification. **Air balance report minimum content per X-004 above applies.** | Commissioning | Mechanical Contractor / Commissioning Agent |
| REQ-005 | Design review; site inspection for intake-exhaust separation | Design / Inspection | Mechanical Engineer / AHJ |
| REQ-006 | Design review; AHJ inspection | Design / Inspection | Mechanical Engineer / AHJ |
| REQ-007 | Functional test — coordinated operation with DEL-013-01 | Commissioning | Mechanical Contractor / Commissioning Agent |
| REQ-008 | Controls commissioning test; sequence of operations walk-through | Commissioning | Mechanical Contractor |
| REQ-009 | Safety Codes Officer inspection; permit records | Inspection | Safety Codes Officer / AHJ |
| REQ-010 | Mechanical Engineer calculation confirming unit selection | Design | Mechanical Engineer |
| REQ-011 | Manufacturer cold-climate documentation; commissioning | Procurement / Commissioning | Mechanical Contractor |
| REQ-012 | Commissioning report submitted to Owner | Commissioning | Mechanical Contractor |
| REQ-013 | CCC documentation; guarantee period log | Closeout / Post-CCC | Project Manager / Mechanical Contractor |
| REQ-014 | Site inspection confirming fire stopping installed per approved detail; AHJ inspection | Construction / Inspection | Mechanical Contractor / AHJ |
| REQ-015 | Site inspection confirming manufacturer clearances met | Construction | Mechanical Contractor |
| REQ-016 | Vibration measurement during commissioning (if specified); visual inspection | Commissioning | Mechanical Contractor |
| REQ-017 | Noise measurement during commissioning (if acoustic criteria specified) | Commissioning | Mechanical Contractor |
| REQ-018 | Engagement letter with independent commissioning agent, or documented self-certification protocol | Pre-Commissioning | Owner / Design-Builder |

---

## Documentation

The following artifacts are anticipated for this deliverable (Source: _CONTEXT.md Scope; R-01 §2.14; Decomposition):

| Artifact | Description | Status |
|---|---|---|
| Equipment submittal / shop drawing | Manufacturer's data sheet, model selection, performance data, dimensional drawings | TBD — pending equipment selection |
| Installation drawings | Ductwork layout, equipment mounting, penetration details (produced under PKG-003 Mechanical Design; used for installation) | TBD |
| Controls sequence of operations | Documented control logic and sensor configuration | TBD |
| Commissioning report | Performance test results, airflow measurements, heat recovery data, sign-off | TBD |
| Safety Codes inspection records | Mechanical permit and inspection sign-off | TBD |
| Operation and maintenance (O&M) manual | Manufacturer O&M manual; filter maintenance schedule | TBD |
| As-built mark-ups | Field-verified ductwork routing, penetration locations | TBD |
