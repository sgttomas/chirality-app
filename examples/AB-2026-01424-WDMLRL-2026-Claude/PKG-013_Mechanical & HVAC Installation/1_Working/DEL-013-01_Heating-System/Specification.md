# Specification — DEL-013-01: High-Recovery Heating System

---

## Scope

### What This Deliverable Covers

DEL-013-01 covers the complete procurement, supply, installation, integration, testing, and commissioning of the high-recovery heating system for the New North Shop addition at the West Dried Meat Lake Regional Landfill Maintenance Shop Addition project.

This deliverable encompasses:
- Equipment procurement and delivery to site
- System assembly and positioning within the utility room (DEL-012-02)
- Ductwork connections to the building distribution system
- Integration with DEL-013-02 (High-Volume Air Exchanger), DEL-013-03 (Forced-Air Makeup System), DEL-013-04 (Heavy Equipment Exhaust System), DEL-013-05 (Welding Station Exhaust System), and DEL-013-06 (Ceiling Fans)
- Controls and monitoring system setup and integration
- Performance testing and commissioning
- All required documentation and records

**Source:** `_CONTEXT.md` Scope; WDMLRL_Decomposition_Claude.md §7 DEL-013-01; R-01 §3.4

### What This Deliverable Excludes

- Mechanical system design (covered by PKG-003, specifically DEL-003-02, DEL-003-03, DEL-003-07)
- Plumbing connections (covered by PKG-014)
- Electrical power supply and circuit installation (covered by DEL-015-04)
- Utility room structural construction (covered by DEL-012-02)
- Utility tie-in to natural gas main (covered by PKG-018, SOW-0080 per decomposition)
- Commissioning closeout documentation at project level (covered by PKG-020)

**Source:** WDMLRL_Decomposition_Claude.md §6 PKG-013 Exclusions

---

## Requirements

### REQ-001: System Type — High-Recovery Heating
The heating system shall be a high-recovery type that recovers thermal energy for reuse in facility space heating.

**Acceptance Criterion:** TBD — Minimum thermal recovery efficiency percentage or COP to be defined by Mechanical Engineer in DEL-003-07. Equipment must demonstrate quantitative recovery performance that qualifies as "high-recovery" per the mechanical specification. *(Lensing ref: C-002)*

**Source:** R-01 §3.4 ("High recovery heating system.") — explicit RFP requirement.
**Verification:** Factory documentation and/or equipment nameplate confirming high-recovery designation; equipment performance data sheet confirming recovery efficiency meets or exceeds the threshold defined in DEL-003-07; commissioning test records.

---

### REQ-002: Integration with HVAC Subsystems
The heating system shall be integrated with the following interconnected systems:
- (a) DEL-013-02: High-Volume Air Exchanger — for heat recovery loop coordination
- (b) DEL-013-03: Forced-Air Makeup System — for conditioned fresh-air supply
- (c) DEL-013-04/05: Exhaust Systems — for exhaust-stream coordination
- (d) DEL-013-06: Ceiling Fans — for distributed air circulation

**Source:** R-01 §3.4 (lists heating, air exchanger, makeup air, exhaust as required components); `_DEPENDENCIES.md` Internal Package Dependencies.
**Verification:** Commissioning test confirming integrated operation across all subsystems; controls loop verification.

---

### REQ-003: Code-Compliant Installation
The installation shall comply with all applicable codes and regulations, including:
- Alberta Safety Codes (as referenced in R-01 §3.3.2) — **Note:** Specific applicable code sections (gas code, mechanical code, electrical code) to be identified by Mechanical Engineer during design phase (DEL-003-07). *(Lensing ref: A-001)*
- National Building Code of Canada and applicable provincial amendments (ASSUMPTION: applicable given Alberta project)
- Alberta Mechanical Code / ASHRAE standards as applicable (ASSUMPTION: location TBD in mechanical design)
- Manufacturer installation specifications — **Note:** Mandatory adherence to manufacturer installation procedures is required as a normative practice; see REQ-011. *(Lensing ref: A-002)*

**AHJ Inspection Scope:** TBD — Acceptance criteria defining what constitutes passing vs. failing the Safety Code inspection (scope of inspection, inspector qualifications, documentation required) to be documented once AHJ requirements are confirmed. *(Lensing ref: A-003)*

**Source:** R-01 §3.3.2 ("The proposed building must adhere to all Alberta Safety Codes."); `_CONTEXT.md` Key Requirements.
**Verification:** Safety Code inspection sign-off with documented scope of inspection; as-built drawings; installer certification records.

---

### REQ-004: IFC Drawing Compliance
Installation shall follow Issued for Construction (IFC) drawings stamped by a Professional Engineer licensed to practice in the Province of Alberta.

**Source:** R-01 §3.3.2 ("All Issued For Construction Drawings must be signed/stamped by a professional engineer licensed to practice in the province of Alberta.").
**Verification:** IFC drawing set on file with P.Eng. stamp; installation sign-off referencing IFC drawing revision.

---

### REQ-005: Equipment Fit and Clearances
Equipment shall fit within the utility room (DEL-012-02) with all code-required clearances maintained for operation, maintenance, and service access.

**Source:** `_DEPENDENCIES.md` Constraint Notes ("Equipment must fit in utility room with proper clearances.").
**Verification:** As-installed dimensional check against equipment submittal dimensions (see Datasheet: Equipment Dimensions); Mechanical Engineer or inspector sign-off on clearances.

---

### REQ-006: Ductwork Routing — No Structural Conflicts
Ductwork routing shall avoid structural conflicts and shall be coordinated with the structural and architectural drawings prior to installation.

**Source:** `_DEPENDENCIES.md` Constraint Notes ("Ductwork routing must avoid structural conflicts.").
**Verification:** Pre-installation coordination drawing review; site inspection confirming no unauthorized penetrations or conflicts.

---

### REQ-007: Utility Connection Availability
Installation shall not commence until all required utility connections (electrical, gas, water as applicable) are confirmed available and commissioned to the utility room.

**Source:** `_DEPENDENCIES.md` Constraint Notes and External Dependencies.
**Verification:** Utility connection confirmation sign-off prior to installation start.

---

### REQ-008: Controls Integration
The heating system controls shall integrate with the building management system (BMS) or facility control infrastructure, as defined by the approved mechanical design.

**BMS Communication Protocol:** TBD — minimum BMS communication protocol (e.g., BACnet, Modbus, LON) and minimum point list to be defined by design team in PKG-003/PKG-004 design phase. *(Lensing ref: B-003)*

**Source:** `_DEPENDENCIES.md` Constraint Notes ("Controls must integrate with building management system.").
**Verification:** Controls integration test during commissioning; BMS point verification against defined point list.

---

### REQ-009: Performance Testing and Commissioning
The installed system shall be tested to confirm operational performance prior to acceptance.

**Pass/Fail Criteria:** TBD — explicit pass/fail criteria for the commissioning test (what constitutes a failed test, and the remediation path) to be defined in the commissioning plan (part of DEL-003-07 or commissioning scope). *(Lensing ref: X-003)*

**Source:** `_CONTEXT.md` Scope ("Performance testing and commissioning."); R-01 §3.1 (completion and acceptance obligations); OBJ-004 ("commission all mechanical... systems to operational readiness").
**Verification:** Commissioning report signed by Mechanical Contractor and accepted by Mechanical Engineer; performance test data on file. *(Note: Mechanical Engineer acceptance of commissioning report resolves sign-off authority; see CONF-004 in Guidance.)*

---

### REQ-010: Heating Capacity
The system shall provide sufficient heating capacity for the New North Shop addition (approx. 13,000 sq ft, 35 ft ceiling, Alberta cold-climate conditions).

**Minimum Heating Output Threshold:** TBD — minimum heating output (BTU/h or kW) and design temperature basis to be established once DEL-003-06 Mechanical Calculation Package is issued. *(Lensing ref: F-001, A-005)*

**Quantitative Performance Acceptance Criteria:** TBD — numeric thresholds for heating output, temperature uniformity, and recovery efficiency to be defined by Mechanical Engineer. *(Lensing ref: A-005)*

**Source:** R-01 §3.1 (building area ~13,000 sq ft); R-01 §3.4 (35 ft ceiling); ASSUMPTION: capacity to be confirmed by DEL-003-06 Mechanical Calculation Package.
**Verification:** Mechanical calculation package (DEL-003-06) confirming required output; commissioning test confirming system meets design load against defined numeric thresholds.

> **ASSUMPTION:** Specific capacity values (BTU/h or kW) are not stated in the RFP. These shall be determined by the Mechanical Engineer in the Mechanical Calculation Package (DEL-003-06) and Mechanical Specification (DEL-003-07). All capacity-related requirements herein are subject to update once design documentation is issued.

---

### REQ-011: Manufacturer Installation Specification Compliance *(NEW — Lensing ref: A-002)*
The Mechanical Contractor shall install the heating system equipment in strict accordance with the manufacturer's published installation specifications, instructions, and procedures.

**Source:** ASSUMPTION: standard practice for mechanical equipment installation; referenced in REQ-003 code list and `_REFERENCES.md` Standard References. Manufacturer installation specifications are listed as applicable in the Standards table but were not previously captured as a standalone normative requirement.
**Verification:** Installation checklist referencing manufacturer installation manual sections; installer sign-off confirming compliance. Equipment must not be installed until manufacturer documentation is on site.

---

### REQ-012: Gas-Fitter Certification and Gas Permit *(NEW — Lensing ref: F-002)*
If the heating system is gas-fired, installation of gas piping and gas-fired equipment shall be performed by a certified gas fitter, and a gas permit shall be obtained from the AHJ prior to gas installation work.

> **CONDITIONAL:** This requirement applies only if the fuel source is confirmed as natural gas (see CONF-001 in Guidance). If an alternate fuel source is selected, this requirement shall be replaced with the applicable certification and permit requirements.

**Source:** ASSUMPTION: Alberta Gas Safety Regulation and Safety Codes Act require certified gas fitters for gas appliance installation; R-01 §3.3.2 (Proponent obtains permits). **Location TBD** — specific Gas Safety Regulation clause not accessed.
**Verification:** Gas fitter certification documentation on file; gas permit obtained and posted before gas installation commences.

---

### REQ-013: Substantial Completion Definition *(NEW — Lensing ref: D-002)*
A formal substantial completion milestone shall be confirmed before the heating system proceeds from installation (Phase 3) to commissioning (Phase 4). Substantial completion for DEL-013-01 means:
- All equipment is installed, secured, and connected per IFC drawings
- All utility connections (electrical, gas, controls) are complete
- All ductwork connections are made and sealed
- Pre-commissioning inspection (Procedure Step 4.1) is passed
- Safety Code inspection (Procedure Step 4.2) is passed

**Source:** ASSUMPTION: standard construction practice; derived from existing Procedure phase transition logic. No explicit "substantial completion" definition for DEL-013-01 exists in source documents.
**Verification:** Substantial completion sign-off by Mechanical Contractor; Mechanical Engineer confirmation that system is ready for commissioning.

---

### REQ-014: Warranty Documentation *(NEW — Lensing ref: X-004)*
The Mechanical Contractor shall provide warranty registration documentation and warranty terms for all installed heating system equipment, including:
- Manufacturer warranty certificates and registration confirmation
- Warranty coverage period and scope
- Warranty exclusions and conditions
- Contact information for warranty claims

**Source:** Procedure Step 5.3 references "Warranty registration and terms" as part of O&M manuals, but no prior requirement mandated this. ASSUMPTION: standard practice for equipment handover documentation.
**Verification:** Warranty documentation submitted as part of O&M manual package; warranty registration confirmed with manufacturer.

---

### REQ-015: Equipment Submittal Approval *(NEW — Lensing ref: X-002)*
Equipment submittal packages shall be reviewed and approved by the Mechanical Engineer prior to equipment procurement. No equipment shall be ordered until written submittal approval is received.

**Source:** Procedure Step 1.2 describes the submittal process; ASSUMPTION: standard design-build practice. This was previously a procedural step but not captured in the Verification table as a formal milestone.
**Verification:** Written submittal approval from Mechanical Engineer on file before purchase order is placed.

---

### REQ-016: As-Built Drawing Submission *(NEW — Lensing ref: E-002)*
As-built drawings (as-installed mark-ups) reflecting the actual installed configuration shall be submitted to the Mechanical Engineer. As-built drawings shall accurately depict all deviations from IFC drawings, including equipment positioning, ductwork routing changes, utility connection locations, and any field modifications.

**Acceptance Criteria:** As-built drawings shall be verified for accuracy against installed conditions by the Mechanical Engineer before acceptance. Significant deviations from IFC drawings shall be noted and approved.

**Source:** As-built drawings are listed in the Documentation table but were not previously captured as a formal verification requirement with acceptance criteria. ASSUMPTION: standard construction practice.
**Verification:** As-built drawings submitted and accepted by Mechanical Engineer; field verification of accuracy for significant deviations.

---

## Standards

| Standard | Applicability | Accessibility |
|---|---|---|
| Alberta Safety Codes Act and applicable Safety Codes | Governing code — all installations in Alberta. **Note:** Specific applicable sections (gas code, mechanical code, electrical code) to be identified per A-001. | Location TBD (not accessed directly; cited in R-01 §3.3.2) |
| National Building Code of Canada (NBC) — current Alberta edition | Building systems code baseline | ASSUMPTION: applicable; location TBD |
| ASHRAE Standards (HVAC systems) | Industry standard for HVAC design and installation. **Note:** Specific standard numbers (e.g., ASHRAE 90.1, ASHRAE 62.1) to be identified by Mechanical Engineer in DEL-003-07. *(Lensing ref: C-001)* | ASSUMPTION: applicable per `_REFERENCES.md`; specific standard numbers TBD |
| Alberta Mechanical Code / CSA B149 (gas appliances) | Gas-fired heating equipment; gas fitter certification required if gas-fired (REQ-012) | ASSUMPTION: applicable if gas-fired; location TBD |
| Alberta Gas Safety Regulation | Gas permit and certified gas fitter requirements (if gas-fired) *(Lensing ref: F-002)* | ASSUMPTION: applicable if gas-fired; **location TBD** |
| Manufacturer Installation Specifications | Equipment-specific requirements; mandatory compliance per REQ-011 | TBD — equipment not yet selected |
| CCDC 14–2013 | Contract form governing all work | R-01 §1.1; decomposition project header |

> All standards listed as ASSUMPTION or location TBD are identified as such because the full text was not available for review. Requirements shall be updated once mechanical design (PKG-003) is issued.

---

## Verification

| Requirement | Verification Method | Responsible Party | Timing |
|---|---|---|---|
| REQ-001: High-recovery system type | Equipment documentation review; nameplate inspection; recovery efficiency verification against DEL-003-07 threshold *(C-002)* | Mechanical Contractor / Mechanical Engineer | Pre-installation / commissioning |
| REQ-002: HVAC subsystem integration | Integrated commissioning test; controls loop verification | Mechanical Contractor | Commissioning |
| REQ-003: Code-compliant installation | Safety Code inspection with documented scope; installer certification | Inspector / Mechanical Contractor | During and post-installation |
| REQ-004: IFC drawing compliance | IFC drawing set on file; installation sign-off | Mechanical Contractor / P.Eng. | Pre-installation (drawings); post-installation (sign-off) |
| REQ-005: Equipment fit and clearances | Dimensional check against submittal data; Mechanical Engineer/inspector sign-off | Mechanical Engineer / Inspector | Post-installation |
| REQ-006: No structural conflicts | Coordination drawing review; site inspection | Design team / Mechanical Contractor | Pre-installation coordination; post-installation inspection |
| REQ-007: Utility availability | Utility connection confirmation sign-off | General Contractor / Project Manager | Before installation start |
| REQ-008: Controls integration | BMS point verification against defined point list; commissioning records | Mechanical Contractor / Controls Contractor | Commissioning |
| REQ-009: Performance testing | Commissioning report with explicit pass/fail criteria applied *(X-003)*; test data; Mechanical Engineer acceptance | Mechanical Contractor / Mechanical Engineer | Commissioning |
| REQ-010: Heating capacity | Mechanical calculation package (DEL-003-06) confirming required output; commissioning test against defined numeric thresholds *(A-005, F-001)* | Mechanical Engineer / Mechanical Contractor | Design phase (calculation); commissioning (test) |
| REQ-011: Manufacturer installation compliance *(NEW)* | Installation checklist vs. manufacturer manual; installer sign-off | Mechanical Contractor | During installation |
| REQ-012: Gas-fitter certification *(NEW, conditional)* | Gas fitter certification on file; gas permit obtained | Mechanical Contractor / AHJ | Before gas installation |
| REQ-013: Substantial completion *(NEW)* | Substantial completion checklist sign-off; Mechanical Engineer confirmation | Mechanical Contractor / Mechanical Engineer | End of Phase 3 / before commissioning |
| REQ-014: Warranty documentation *(NEW)* | Warranty documents in O&M package; registration confirmed | Mechanical Contractor | Project closeout |
| REQ-015: Equipment submittal approval *(NEW)* | Written approval from Mechanical Engineer on file | Mechanical Engineer | Before procurement |
| REQ-016: As-built drawing submission *(NEW)* | As-built drawings submitted and accepted; field verification of accuracy | Mechanical Engineer | Post-commissioning |

---

## Documentation

The following artifacts are anticipated as outputs of this deliverable:

| Artifact | Description | Timing |
|---|---|---|
| Equipment submittal package | Manufacturer data sheets, model numbers, performance data for Owner/Engineer review and approval. **Formal verification milestone per REQ-015.** | Pre-procurement |
| IFC drawing compliance record | Reference to IFC mechanical drawings used for installation | Pre-installation |
| Installation records | Site sign-off confirming installation complete per drawings and specifications; manufacturer installation compliance per REQ-011 | Post-installation |
| Safety Code inspection sign-off | Documented inspection approval by qualified authority having jurisdiction (AHJ), with scope of inspection documented per A-003 | Post-installation |
| Gas permit and gas-fitter certification *(conditional)* | Gas permit and certified gas fitter documentation, if gas-fired (REQ-012) *(Lensing ref: F-002)* | Before gas installation |
| Substantial completion sign-off | Formal sign-off confirming DEL-013-01 is ready for commissioning (REQ-013) *(Lensing ref: D-002)* | End of installation phase |
| Commissioning report | Performance test results with explicit pass/fail criteria applied; system functional verification; integrated HVAC subsystem test results | Commissioning |
| As-built drawings (as-installed mark-ups) | Mark-ups or redlines reflecting actual installed configuration; verified for accuracy per REQ-016 *(Lensing ref: E-002)* | Post-commissioning |
| Controls integration record | BMS/controls point list verification against defined protocol and point list; system setpoints documented | Commissioning |
| Warranty documentation | Manufacturer warranty certificates, registration, terms, and exclusions per REQ-014 *(Lensing ref: X-004)* | Project closeout |
| O&M manuals | Manufacturer operation and maintenance documentation for Owner handover, including warranty package | Project closeout (PKG-020) |

**Source:** `_CONTEXT.md` Scope; R-01 §2.14 (completion and acceptance); OBJ-004; PKG-020 (commissioning and closeout).

---

## Semantic Lensing Enrichment Log (Pass 3)

The following items from `_SEMANTIC_LENSING.md` were applied to this document:

| ItemID | Action Taken |
|---|---|
| A-001 | Added note to REQ-003 that specific Alberta Safety Code sections to be identified by Mechanical Engineer; updated Standards table |
| A-002 | Created REQ-011 (Manufacturer Installation Specification Compliance) as standalone normative requirement |
| A-003 | Added AHJ Inspection Scope TBD note to REQ-003; updated verification row |
| A-005 | Added Quantitative Performance Acceptance Criteria TBD to REQ-010; updated verification row |
| B-003 | Added BMS Communication Protocol TBD to REQ-008 with protocol examples |
| C-001 | Added note to ASHRAE Standards row in Standards table to specify standard numbers (e.g., 90.1, 62.1) |
| C-002 | Added Acceptance Criterion TBD to REQ-001 for minimum recovery efficiency/COP threshold |
| D-002 | Created REQ-013 (Substantial Completion Definition) formalizing the installation-to-commissioning gate |
| E-002 | Created REQ-016 (As-Built Drawing Submission) with acceptance criteria for accuracy |
| E-004 | Updated REQ-009 verification to reflect Mechanical Engineer acceptance of commissioning report; cross-referenced CONF-004 |
| F-001 | Added Minimum Heating Output Threshold TBD to REQ-010 |
| F-002 | Created REQ-012 (Gas-Fitter Certification and Gas Permit) as conditional requirement; added Alberta Gas Safety Regulation to Standards table |
| X-002 | Created REQ-015 (Equipment Submittal Approval) as formal verification milestone |
| X-003 | Added Pass/Fail Criteria TBD to REQ-009 for commissioning test |
| X-004 | Created REQ-014 (Warranty Documentation) as new requirement |
