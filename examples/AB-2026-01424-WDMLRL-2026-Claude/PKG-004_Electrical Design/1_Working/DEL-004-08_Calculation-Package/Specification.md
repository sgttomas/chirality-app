# Specification — DEL-004-08 Electrical Calculation Package

---

## Scope

### What This Deliverable Covers

DEL-004-08 is the Electrical Calculation Package for the 2026 Design Build — West Dried Meat Lake Regional Landfill Maintenance Shop Addition. This deliverable encompasses all engineering calculations required to design and justify the electrical systems for the new ~13,000 sq ft maintenance shop addition (referred to informally as "New North Shop" in some project documentation), as described in RFP §1.0, §3.4, and Appendix B (Electrical).

The calculation package shall support the following systems:

- Three-phase power service distribution and service entrance sizing
- Lighting calculations for all zones: main shop, wash bay, office, utility room, parts/tool room, and service pit
- Receptacle circuit sizing: 15 A/120 V, 20 A/120 V, 20 A/240 V, 30 A/240 V, 50 A/240 V
- Dedicated equipment circuit sizing: cranes (×2), overhead doors, compressor (40 A), fire hose pump (70 A), pressure washer (70 A), ceiling fans (×6), exhaust fans
- Low-voltage system wiring design basis: security cameras, 2-way radio antenna
- Load schedule and panel schedule calculations underpinning DEL-004-06 (Panel Schedules)
- Voltage drop and conductor sizing calculations

### What This Deliverable Excludes

- Mechanical equipment selection or sizing (scope of PKG-003)
- Plumbing system electrical interfaces beyond circuit provision (scope of PKG-006)
- Structural design of crane supports (scope of PKG-002)
- Procurement of electrical equipment
- Installation work (scope of PKG-015 — Electrical and Low-Voltage Installation)
- As-built documentation (post-construction)
- Renovation electrical work for Old North Shop unless explicitly referenced in electrical drawings (scope of PKG-001/PKG-017)

---

## Requirements

### REQ-004-08-01: Three-Phase Power Service
**Source:** RFP §3.4; Decomposition SOW-0051
The calculation package shall include a service entrance sizing calculation demonstrating that the three-phase power supply to the building is adequate for all connected and demand loads.

### REQ-004-08-02: Load Schedule
**Source:** RFP §3.4; App B (Electrical); Decomposition SOW-0014
A connected load schedule and demand load calculation shall be produced, accounting for all lighting, receptacle, equipment, and special-purpose loads identified in Appendix B (Electrical) and RFP §3.4.

### REQ-004-08-03: Lighting — Main Shop
**Source:** App B (Electrical)
Calculations shall verify that the proposed 20 × 150 W LED high bay fixtures (22,000 lumens each) achieve adequate illuminance for the main shop work environment. Circuit loading for 5 rows × 4 fixtures shall be documented.

### REQ-004-08-04: Lighting — Wash Bay
**Source:** App B (Electrical)
Calculations shall account for 2 rows × 3 high bay fixtures in the wash bay. Fixture wattage TBD by Electrical Engineer (conceptual drawing does not specify wash bay fixture wattage; ASSUMPTION: same 150 W LED type as main shop unless Electrical Engineer determines otherwise).

### REQ-004-08-05: Lighting — Office, Utility Room, Parts/Tool Room
**Source:** App B (Electrical)
Calculations shall account for:
- Office: 1 × 8' LED fixture
- Utility Room: 2 × 8' LED fixtures
- Parts/Tool Room: 6 × 8' LED fixtures
Wattage per fixture TBD by Electrical Engineer (standard commercial 8' LED strip — ASSUMPTION: 80 W each adopted as conservative planning value for load schedule calculations; Electrical Engineer to confirm per selected product). (Lensing X-001)

### REQ-004-08-06: Service Pit Lighting
**Source:** RFP §3.4; Decomposition SOW-0028
The service pit is required to be "ventilated and lighted." Calculations shall include service pit lighting circuit sizing. Fixture type and illuminance TBD by Electrical Engineer; ASSUMPTION: a dedicated lighting circuit is required for the pit area.

### REQ-004-08-07: Receptacle Circuits
**Source:** App B (Electrical); Decomposition SOW-0058
Circuit calculations shall address all receptacle types shown on the conceptual electrical drawing:
- 15 A / 120 V (general purpose)
- 20 A / 120 V (general power)
- 20 A / 240 V (medium power)
- 30 A / 240 V (heavy power)
- 50 A / 240 V (welding-grade)

Quantity and layout per App B (Electrical); final quantities and groupings per Electrical Engineer's panel schedule.

### REQ-004-08-08: Welding-Grade Receptacles
**Source:** RFP §3.4; Decomposition SOW-0057; Decision D-009
Multiple 50 A / 240 V receptacles shall be provided throughout the shop area for connecting high-voltage welding equipment. The County will supply welding equipment specifications; the Electrical Engineer shall confirm circuit ratings upon receipt. 50 A / 240 V is used as the ASSUMPTION (per Decomposition D-009) pending County confirmation.

### REQ-004-08-09: Crane Power
**Source:** App B (Electrical); RFP §3.4; Decomposition SOW-0059, SOW-0067
Dedicated power feeds for two 5-tonne overhead cranes on trolley shall be calculated. Ampacity, conductor sizing, and protection device ratings TBD by Electrical Engineer based on crane manufacturer data (not provided in RFP or Appendix B). ASSUMPTION: crane power feeds will require dedicated circuits; sizing shall be per manufacturer requirements and applicable code.

### REQ-004-08-10: Overhead Door Power
**Source:** App B (Electrical); Decomposition SOW-0060
Power provision for all overhead doors shall be included. Quantity of overhead doors and operator ampacity TBD by Electrical Engineer in coordination with architectural drawings (DEL-001-07). ASSUMPTION: standard overhead door operators (~15–20 A / 120 V per unit) based on typical practice; Electrical Engineer to confirm.

### REQ-004-08-11: Dedicated Equipment Circuits
**Source:** App B (Electrical); Decomposition SOW-0061, SOW-0062, SOW-0063
Calculations shall size dedicated circuits for:
- Compressor: 40 A (rating stated on App B drawing)
- Fire hose pump: 70 A (rating stated on App B drawing)
- Pressure washer: 70 A (rating stated on App B drawing)

### REQ-004-08-12: Ceiling Fans
**Source:** App B (Electrical); Decomposition SOW-0040
Six ceiling fans in the main shop area shall be accounted for in load calculations. Fan wattage TBD by Electrical Engineer.

### REQ-004-08-13: Exhaust Fans
**Source:** App B (Electrical); Decomposition SOW-0066
Exhaust fan(s) as shown on the electrical drawing shall be included. Quantity and wattage TBD by Electrical Engineer.

### REQ-004-08-14: Low-Voltage Systems
**Source:** App B (Electrical); Decomposition SOW-0064, SOW-0065
The calculation package shall include design basis documentation for:
- Security camera wiring
- 2-way radio antenna wiring
Detailed low-voltage calculations are documented in DEL-004-07 (Low-Voltage System Plans); this package shall confirm power supply requirements for any powered low-voltage equipment.

### REQ-004-08-15: Voltage Drop
**Source:** ASSUMPTION — standard Alberta electrical engineering practice
Voltage drop calculations shall be performed for feeders and branch circuits to confirm compliance with applicable code limits. Specific code requirements TBD by Electrical Engineer (applicable edition of the Canadian Electrical Code, Part I — location TBD in accessible sources).

### REQ-004-08-16: Conductor and Protection Sizing
**Source:** ASSUMPTION — standard Alberta electrical engineering practice
All conductors, conduit, and overcurrent protection devices shall be sized per the applicable Canadian Electrical Code, Part I. Specific code clause references TBD by Electrical Engineer (code not provided as a source).

### REQ-004-08-17: P.Eng. Stamp
**Source:** RFP §3.3.2 (SOW-0018)
All IFC calculations and drawings shall be signed and stamped by a Professional Engineer licensed to practice in the Province of Alberta.

### REQ-004-08-18: Alberta Safety Codes
**Source:** RFP §3.3.2 (SOW-0008, SOW-0009)
The design shall adhere to all applicable Alberta building codes, regulations, and Alberta Safety Codes.

### REQ-004-08-19: Demand Factor Documentation
**Source:** ASSUMPTION — standard Alberta electrical engineering practice; Lensing F-001
The calculation package shall document the demand factor basis for each load category (lighting, receptacles, welding, motor loads, general loads). The demand factor applied and the CEC clause or engineering rationale supporting it shall be recorded for each category.

### REQ-004-08-20: Panel Configuration Documentation
**Source:** ASSUMPTION — standard electrical engineering practice; Lensing X-002
The calculation package shall include a panel configuration determination documenting the number of panels, main vs. sub-panel arrangement, and the sizing basis for each panel. This output directly feeds DEL-004-06 (Panel Schedules).

### REQ-004-08-21: Available Fault Current Determination
**Source:** ASSUMPTION — standard CEC requirement for service entrance design; Lensing X-003
The calculation package shall include a determination of the available fault current at the service entrance and shall verify that all overcurrent protection devices have adequate interrupting ratings for the available fault current. ASSUMPTION: this is a standard CEC requirement; specific clause reference TBD by Electrical Engineer once applicable edition is confirmed.

### REQ-004-08-22: Heating and Makeup Air Unit Circuit Sizing
**Source:** ASSUMPTION — Procedure Step 3.1 lists heating system and forced-air makeup air unit as connected loads; Lensing C-003, E-002
The calculation package shall include circuit sizing calculations for the heating system and forced-air makeup air unit (MUA). Electrical load data shall be obtained from PKG-003 (Mechanical Design). ASSUMPTION: these loads are within the scope of this calculation package based on their inclusion in the connected load schedule; Electrical Engineer to confirm scope with Mechanical Engineer.

### REQ-004-08-23: Mezzanine Electrical Loads
**Source:** App B (Electrical) — mezzanine identified in conceptual layout; Lensing E-001
The calculation package shall account for mezzanine-specific electrical loads (lighting and receptacle circuits for the mezzanine area above parts room, utility room, and wash bay). Load quantities and types TBD by Electrical Engineer in coordination with architectural floor plans.

### REQ-004-08-24: Hazardous Area Classification Assessment
**Source:** ASSUMPTION — CEC rules for areas with potential flammable vapors; Lensing B-004
The Electrical Engineer shall determine whether the service pit area requires hazardous area classification under CEC rules (potential flammable vapors from vehicle maintenance). If hazardous area classification applies, the calculation package shall document the classification and its impact on fixture type selection and circuit design for the service pit zone. ASSUMPTION: assessment is required; classification result TBD by Electrical Engineer.

---

## Standards

| Standard | Applicability | Accessibility |
|---|---|---|
| Canadian Electrical Code (CEC), Part I — current Alberta adopted edition | Governs all electrical installation design; conductor sizing, protection, voltage drop. **ACTION REQUIRED (Lensing A-001):** Electrical Engineer to confirm the specific CEC edition adopted by Alberta at the time of design and record it here. Without the edition, CEC clause references in requirements (REQ-004-08-15, REQ-004-08-16, and others) cannot be anchored to an authoritative code text. | ASSUMPTION: applicable; specific edition TBD by Electrical Engineer (not provided in RFP sources — location TBD) |
| Alberta Safety Codes Act and associated electrical safety codes | Governs Safety Code permit requirements | Referenced in RFP §3.3.2; specific clauses location TBD |
| CCDC 14–2013 | Design-build contract form; governs deliverable obligations | Referenced in RFP §2.7; contract-level standard |
| IES (Illuminating Engineering Society) recommended practice for industrial facilities, or equivalent Alberta-accepted illuminance standard | Required for establishing quantitative illuminance targets for lighting calculations (REQ-004-08-03 through REQ-004-08-06). **ACTION REQUIRED (Lensing C-002):** Electrical Engineer to confirm the applicable illuminance standard and move from ASSUMPTION to confirmed. Without a committed standard, the adequacy of lighting calculations cannot be verified against a normative benchmark. | ASSUMPTION: applicable; specific standard TBD by Electrical Engineer (not referenced directly in RFP sources) |

---

## Verification

| Requirement | Verification Method |
|---|---|
| REQ-004-08-01: Three-phase service sizing | Engineering review of service entrance calculation; comparison against total demand load |
| REQ-004-08-02: Load schedule | Internal QC review of load schedule against all items in App B (Electrical) and RFP §3.4 |
| REQ-004-08-03: Lighting — Main shop | Illuminance calculation output reviewed against applicable illuminance standard (TBD per Lensing D-001); minimum illuminance target for heavy equipment maintenance work documented and achieved; circuit loading confirmed in panel schedule |
| REQ-004-08-04: Lighting — Wash bay | Illuminance calculation output reviewed against applicable illuminance standard (TBD); minimum illuminance target for wash bay operations documented and achieved; IP rating suitability confirmed for wet environment; circuit loading confirmed in panel schedule |
| REQ-004-08-05: Lighting — Office/Utility/Parts | Illuminance calculation output reviewed against applicable illuminance standard (TBD); minimum illuminance target for each room type documented and achieved; circuit loading confirmed in panel schedule |
| REQ-004-08-06: Service pit lighting | Illuminance calculation output reviewed; fixture type suitability for below-grade confined space confirmed; hazardous area classification assessment (REQ-004-08-24) reviewed |
| REQ-004-08-07 to REQ-004-08-08: Receptacle circuits | Panel schedule check; circuit ratings confirmed against App B (Electrical) layout |
| REQ-004-08-09: Crane power — conductor sizing | Crane manufacturer FLA data cross-checked against conductor sizing per CEC Section 40 (or equivalent); overcurrent protection rated for crane duty cycle (Lensing C-001 — CEC clause references to be added once edition confirmed) |
| REQ-004-08-10: Overhead door power | Overhead door operator data (quantity, ampacity) confirmed with DEL-001-07; circuit sizing cross-checked against operator requirements |
| REQ-004-08-11: Dedicated equipment circuits (compressor, fire hose pump, pressure washer) | Stated ratings from App B cross-checked against protection device sizing per CEC |
| REQ-004-08-12: Ceiling fans | Fan motor data confirmed with PKG-003; circuit sizing cross-checked |
| REQ-004-08-13: Exhaust fans | Fan motor data confirmed with PKG-003; circuit sizing cross-checked |
| REQ-004-08-14: Low-voltage | Coordination check with DEL-004-07 (Low-Voltage Plans) |
| REQ-004-08-15: Voltage drop — feeders | Feeder voltage drop calculation output reviewed against CEC limits by P.Eng.; CEC clause reference recorded (Lensing C-001) |
| REQ-004-08-16: Conductor and protection sizing — branch circuits | Branch circuit conductor sizing reviewed against CEC; conduit sizing per CEC; CEC clause reference recorded per circuit (Lensing C-001) |
| REQ-004-08-16: Conductor and protection sizing — feeders | Feeder conductor sizing reviewed against CEC; CEC clause reference recorded (Lensing C-001) |
| REQ-004-08-16: Conductor and protection sizing — dedicated equipment | Dedicated equipment circuit sizing reviewed against CEC and manufacturer requirements; CEC clause reference recorded (Lensing C-001) |
| REQ-004-08-17: P.Eng. stamp | Stamp and signature present on all IFC calculation sheets |
| REQ-004-08-18: Code compliance | Safety Code inspection and permit sign-off (administered via PKG-009). **Internal pre-PKG-009 acceptance criterion (Lensing A-003):** all CEC clause references recorded for each sizing calculation; Electrical Engineer to verify clause traceability before submitting to PKG-009 |
| REQ-004-08-19: Demand factor documentation | QC review confirms demand factor basis documented for each load category with CEC clause or engineering rationale |
| REQ-004-08-20: Panel configuration | QC review confirms panel arrangement documented with sizing basis; output cross-checked against DEL-004-06 |
| REQ-004-08-21: Available fault current | QC review confirms fault current determination documented; overcurrent device interrupting ratings verified against available fault current |
| REQ-004-08-22: Heating/MUA circuit sizing | Mechanical load data receipt confirmed from PKG-003; circuit sizing per CEC |
| REQ-004-08-23: Mezzanine electrical loads | Mezzanine lighting and receptacle loads documented in connected load schedule; circuit sizing per CEC |
| REQ-004-08-24: Hazardous area classification | Assessment documented by Electrical Engineer; if applicable, fixture and circuit design for service pit zone compliant with CEC hazardous area requirements |

---

## Documentation

### Anticipated Artifacts (from _CONTEXT.md)
- Calculation Package documents per RFP

### Expected Calculation Package Contents (ASSUMPTION — standard electrical engineering practice for Alberta design-build projects)
- Cover sheet with project identification, P.Eng. stamp, revision table
- Design criteria summary (applicable codes, assumptions, design basis)
- Service entrance and main panel sizing calculation
- Available fault current determination and overcurrent device interrupting rating verification (Lensing X-003)
- Connected and demand load schedule (all circuits), with demand factor basis documented per load category (Lensing F-001)
- Lighting calculation sheets by zone (main shop, wash bay, office, utility room, parts/tool room, service pit, mezzanine) with quantitative illuminance targets documented (Lensing D-001, E-001)
- Hazardous area classification assessment for service pit (Lensing B-004)
- Branch circuit and feeder sizing calculations, with CEC clause references per circuit (Lensing C-001)
- Voltage drop calculations (feeders and critical branch circuits)
- Dedicated equipment circuit calculations (cranes, compressor, fire hose pump, pressure washer)
- Heating/MUA circuit calculations (Lensing C-003)
- Panel configuration determination and documentation (Lensing X-002)
- Low-voltage power supply summary
- Panel schedule calculation basis (supporting DEL-004-06)
- Cross-reference table linking each calculation section to the corresponding drawing (Lensing D-003)

### Related Deliverables
| Deliverable ID | Name | Relationship |
|---|---|---|
| DEL-004-02 | Single-Line Diagram | Calculation package supports SLD design |
| DEL-004-03 | Power Distribution Plans | Calculations underpin conductor/conduit routing |
| DEL-004-04 | Lighting Plans | Lighting calculations verify fixture layout |
| DEL-004-05 | Receptacle Layout Plans | Circuit calculations confirm receptacle groupings |
| DEL-004-06 | Panel Schedules | Load schedule output populates panel schedules |
| DEL-004-07 | Low-Voltage System Plans | Power requirements coordinated |
| DEL-004-09 | Electrical Specification | Specification references calculation outputs for product requirements |
