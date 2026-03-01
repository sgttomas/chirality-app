# Specification — DEL-012-03: Office Space

**Document Type:** Specification (normative)
**Deliverable ID:** DEL-012-03
**Package:** PKG-012 — Interior Construction & Fit-Out
**Project:** 2026 Design Build — West Dried Meat Lake Regional Landfill Maintenance Shop Addition
**Owner:** Camrose County
**Revision:** R2 — 2026-02-26 (Pass 3 — Semantic Lensing Enrichment)
**Status:** SEMANTIC_READY

---

## Scope

### What This Specification Covers

This specification governs the interior construction and fit-out of the administrative office space (DEL-012-03) within the new north shop addition at the West Dried Meat Lake Regional Landfill, SW 14–44–21–W4, near Ferintosh, Alberta.

Covered scope includes:
- Interior partition and wall systems defining the office space
- Floor and ceiling finishes within the office
- Rough openings and door frames (door hardware and door leaf per IFC architectural specification)
- Electrical outlet rough-in and final installation of 15A/120V receptacles within the office — **scope boundary with PKG-015: TBD**. Resolution trigger: IFC contractor scope documents must explicitly assign rough-in vs. device installation responsibilities. See Guidance.md CONF-001. [Lensing: A-001]
- Installation of 1× 8' LED lighting fixture — **scope boundary with PKG-015: TBD**. Resolution trigger: IFC contractor scope documents. See Guidance.md CONF-001. [Lensing: A-001]
- Data and communications outlet locations (final low-voltage wiring by PKG-015)
- Safety and accessibility features within the office area
- Coordination interfaces with HVAC systems (PKG-013) including duct/register penetrations through partitions and ceilings

**Source:** _CONTEXT.md Scope; WDMLRL_Decomposition_Claude.md PKG-012 inclusion criteria; SOW-0031

### What This Specification Excludes

- Structural shell and envelope (PKG-011 — Building Structure & Envelope)
- HVAC equipment, ductwork, and mechanical systems (PKG-013)
- Final electrical panel, wiring, and equipment installation beyond office scope boundary (PKG-015)
- Final low-voltage/data system installation (PKG-015)
- Furniture, office equipment, and loose furnishings (ASSUMPTION: County-supplied; not referenced in RFP)
- Foundation (PKG-010)
- Renovation of existing north shop (PKG-017)

**Source:** WDMLRL_Decomposition_Claude.md PKG-012 Exclusions; PKG-011, PKG-013, PKG-015, PKG-017 descriptions

---

## Requirements

### REQ-001 — Professional Workplace Environment
**Statement:** The completed office space shall provide a professional workplace environment suitable for administrative and facility management activities.
**Acceptance Criteria (TBD):** Measurable quality benchmark for "professional workplace environment" not yet established. **Resolution trigger:** Define acceptance criteria by reference to IFC finish schedule (e.g., drywall finish level, flooring type minimum, ceiling system type) or link to a finish grade standard once IFC design is issued. [Lensing: F-004]
**Source:** _CONTEXT.md Key Requirements — "Professional workplace environment"
**Verification:** Visual inspection at completion; County acceptance per RFP §2.14; **acceptance criteria to be defined against IFC finish schedule** [Lensing: F-004]

### REQ-002 — Code-Compliant Construction
**Statement:** All construction shall comply with applicable Alberta building codes, Alberta Safety Codes, and all other regulations applicable in the Province of Alberta.
**Source:** _CONTEXT.md Key Requirements — "Code-compliant construction practices"; RFP §3.3.2 — "The building design must adhere to all applicable building codes and regulations"; RFP §3.3.2 — "The proposed building must adhere to all Alberta Safety Codes"
**Verification:** Municipal building permit inspection; Safety Code permit inspections; IFC drawings stamped by P.Eng. licensed in Alberta per RFP §3.3.2

### REQ-003 — Accessibility Compliance
**Statement:** The office space shall comply with applicable accessibility standards (Alberta equivalent of accessibility requirements, including barrier-free provisions under the Alberta Building Code).
**Acceptance Criteria (TBD — to be confirmed from Alberta Building Code barrier-free provisions, specific clause TBD):** [Lensing: A-003]
- Minimum door clear width: TBD (Alberta Building Code barrier-free clause, **location TBD**)
- Maximum threshold height: TBD
- Maneuvering clearance dimensions: TBD
- Floor finish: no trip hazards per accessibility standard

**Source:** _CONTEXT.md Key Requirements — "Accessibility standards compliance"
**Verification:** Building permit inspection; accessibility compliance review during design and construction; **measurable acceptance criteria to be added once Alberta Building Code barrier-free clause is confirmed** [Lensing: A-003]

### REQ-004 — Comfortable Environmental Conditions
**Statement:** The office space shall be served by the building's HVAC systems (PKG-013) to provide comfortable environmental conditions for occupancy.
**Quantified Comfort Targets (TBD):** [Lensing: D-004]
- Target temperature range: TBD (ASSUMPTION: reference ASHRAE 55 or Alberta Building Code comfort provisions — specific standard **location TBD**; coordinate with PKG-013 HVAC design)
- Ventilation rate per occupant: TBD (dependent on occupancy load — see Datasheet.md Conditions)
- Humidity range: TBD

**Source:** _CONTEXT.md Key Requirements — "Comfortable environmental conditions"; _DEPENDENCIES.md — DEL-013-01 (Heating), DEL-013-02 (Air Exchanger), DEL-013-03 (Makeup Air)
**Verification:** Systems functional test / commissioning (PKG-013 deliverable); occupancy comfort assessment **against quantified targets once established** [Lensing: D-004]

### REQ-005 — Integrated Communication and Data Systems
**Statement:** The office space shall be provided with electrical outlets and data points to support integrated communication and data systems.
**Source:** _CONTEXT.md Scope — "Electrical outlets and data points"; _CONTEXT.md Key Requirements — "Integrated communication and data systems"
**Verification:** Outlet and data point installation confirmed against IFC electrical/low-voltage drawing

### REQ-006 — Lighting
**Statement:** The office space shall be provided with 1× 8' LED lighting fixture as shown on the conceptual electrical drawing.
**Source:** SOW-0054 — "Install 1× 8' LED fixture in office"; App B (Electrical) — office lighting symbol shown
**Verification:** Fixture installed and operational; confirmed against IFC electrical drawing

### REQ-007 — Electrical Receptacles (15A/120V)
**Statement:** The office space shall be provided with 15A/120V electrical receptacles at locations to be confirmed in the IFC electrical design, consistent with the conceptual electrical drawing.
**Source:** App B (Electrical) — multiple (15) symbols shown in office area; SOW-0058 — "Install 15A/120V... receptacles per electrical drawing layout"
**Verification:** Receptacles installed and operational; confirmed against IFC electrical drawing

### REQ-008 — Interior Partitions
**Statement:** The office space shall be enclosed by interior partition and wall systems as defined in the IFC architectural drawings. Partitions shall be non-structural (structural shell provided by PKG-011).
**Fire Rating (TBD):** Whether office partitions require a fire rating depends on occupancy classification and Alberta Building Code analysis. **Resolution trigger:** IFC Architect / Code consultant to confirm fire rating requirements for office partitions based on occupancy classification and building code analysis. If fire-rated partitions are required, this requirement shall be updated with the fire-resistance rating. [Lensing: C-001]
**Source:** _CONTEXT.md Scope — "Wall and partition systems"; App B (Shop) — office partitions shown on floor plan; Guidance.md HVAC Integration reference to fire separation requirements
**Verification:** Partitions constructed per IFC architectural drawings; visual inspection; **fire separation verification TBD pending fire rating determination** [Lensing: C-001, C-002]

### REQ-009 — Floor and Ceiling Finishes
**Statement:** The office space shall receive floor and ceiling finishes appropriate for an administrative workplace environment, as defined in the IFC architectural finish schedule and reflected ceiling plans.
**Acceptance Criteria (TBD):** [Lensing: F-004, X-004]
- Drywall finish level: TBD (e.g., Level 4 for painted surfaces — to be defined in IFC finish schedule)
- Flooring material specification: TBD (to be defined in IFC finish schedule)
- Ceiling tile/system type: TBD (to be defined in IFC reflected ceiling plans)
- **Interim acceptance basis (pre-IFC):** Finishes shall be durable, easy to maintain, and appropriate for an industrial facility administrative context per Guidance.md Principle 3.

**Source:** _CONTEXT.md Scope — "Floor and ceiling finishes"
**Verification:** Finishes installed per IFC finish schedule; visual inspection at completion **against defined finish specifications once IFC finish schedule is issued** [Lensing: F-004, X-004]

### REQ-010 — Completion Deadline
**Statement:** All work associated with DEL-012-03, including construction, systems integration testing, inspection, and sign-off, shall be complete on or before December 31, 2026.
**Source:** RFP §3.1 — "All Work...must be completed on or before December 31, 2026"; OBJ-002
**Verification:** Construction Completion Certificate (CCC) issued on or before December 31, 2026

### REQ-011 — Inspection Access
**Statement:** The General Contractor shall submit all inspection requests and ensure the County project representative is present at all inspections. Copies of all completed inspection reports shall be provided to the County.
**Source:** RFP §3.3.2; SOW-0084; SOW-0085
**Verification:** Inspection reports on file; County representative attendance confirmed

### REQ-012 — IFC Drawing Conformance
**Statement:** Construction shall conform to the Issued For Construction (IFC) drawings, which must be stamped by a P.Eng. licensed in the Province of Alberta prior to construction commencement.
**Source:** RFP §3.3.2 — "All Issued For Construction Drawings must be signed/stamped by a professional engineer licensed to practice in the province of Alberta"
**Verification:** IFC drawings reviewed and stamped; construction inspection against IFC drawings

### REQ-013 — Emergency Egress and Life Safety Provisions [Lensing: F-002]
**Statement:** The office space shall be provided with emergency egress provisions including exit signage, emergency lighting, and fire extinguisher mounting as required by the Alberta Building Code and Fire Code. Specific provisions are TBD pending IFC design and code analysis.
**Source:** Alberta Building Code and Fire Code (**location TBD**); Procedure.md Step 2.12 (ASSUMPTION: per Alberta Building Code and Fire Code)
**Verification:** Installation per IFC drawings and Alberta Building Code/Fire Code requirements; Safety Code inspection
**Note:** This requirement captures a code-driven obligation currently addressed only in Procedure.md Step 2.12 as an assumption. It requires normative statement in the Specification.

### REQ-014 — Fire Sprinkler System Applicability [Lensing: F-001]
**Statement:** Whether a fire sprinkler system is required for the office area shall be determined by code analysis under the Alberta Building Code and Fire Code, given the occupancy classification and building area. If required, the office space shall be served by the building's fire sprinkler system. If not required, an explicit exclusion shall be documented.
**Source:** Alberta Building Code and Fire Code (**location TBD**); Procedure.md Step 2.7 (ASSUMPTION: "if required by Alberta Building Code for this occupancy")
**Verification:** Code consultant / IFC Architect determination; if required, sprinkler installation inspection per Alberta Fire Code
**Resolution trigger:** Code consultant / IFC Architect to determine sprinkler applicability and record result.

---

## Standards

| Standard / Code | Applicability | Status |
|---|---|---|
| Alberta Building Code (current edition) | Governing building code for the Province of Alberta | ASSUMPTION: applicable; **specific edition TBD — Resolution trigger: General Contractor to confirm adopted code edition with permit authority prior to IFC submission** [Lensing: A-002] |
| Alberta Safety Codes Act and Safety Codes | All construction must adhere to Alberta Safety Codes | Explicitly required by RFP §3.3.2 |
| National Building Code of Canada (NBC) | Referenced by Alberta Building Code | ASSUMPTION: applicable; location TBD |
| Alberta OH&S (Occupational Health and Safety) | Prime Contractor obligations apply throughout construction | RFP §2.15; SOW-0083 |
| CCDC 14–2013 | Design-Build Stipulated Price Contract form | RFP §2.7 |
| ADA / Barrier-Free Design | Accessibility requirements (Alberta Building Code barrier-free provisions govern; ADA referenced in _CONTEXT.md as general intent) | _CONTEXT.md Key Requirements |
| Canadian Electrical Code (CEC) Part I, as adopted in Alberta | Governs all electrical installations within the office. **Specific edition TBD — Resolution trigger: General Contractor / Electrical Engineer to confirm CEC edition with permit authority.** Also confirm whether the Alberta Electrical Utility Code applies to any scope elements. [Lensing: D-001] | _REFERENCES.md Standard References |
| Alberta Prompt Payment and Construction Lien Act | Governs lien holdback and payment | RFP §2.13.2 |

**Note:** Specific code editions and clause numbers are TBD pending confirmation of the applicable permit authority's adopted code version.

---

## Verification

| Requirement | Verification Method | Stage |
|---|---|---|
| REQ-001 Professional Workplace | Visual inspection; County acceptance; **acceptance criteria per IFC finish schedule (TBD)** [Lensing: F-004] | Construction completion |
| REQ-002 Code Compliance | Building/Safety Code permit inspections; P.Eng.-stamped IFC drawings | Design + Construction |
| REQ-003 Accessibility | Building permit review; accessibility inspection; **measurable acceptance criteria per Alberta Building Code barrier-free provisions (TBD)** [Lensing: A-003] | Design + Construction |
| REQ-004 Environmental Conditions | HVAC commissioning test (PKG-013); functional walk-through; **comfort assessment against quantified targets (TBD)** [Lensing: D-004] | Systems commissioning |
| REQ-005 Data/Communications | Outlet/data point count and location check against IFC drawings | Construction completion |
| REQ-006 Lighting | Fixture installation and operational test | Construction completion |
| REQ-007 Electrical Receptacles | Circuit test; count and location check against IFC drawings | Construction completion |
| REQ-008 Partitions | Construction inspection against IFC architectural drawings; **fire separation verification TBD per fire rating determination** [Lensing: C-001, C-002] | Construction |
| REQ-009 Finishes | Visual inspection against IFC finish schedule; **acceptance per defined finish specifications (TBD)** [Lensing: F-004, X-004] | Construction completion |
| REQ-010 Completion Deadline | CCC issued date | Project closeout |
| REQ-011 Inspection Access | Inspection reports on file with County | Throughout construction |
| REQ-012 IFC Conformance | IFC drawing stamp review; field inspections | Design + Construction |
| REQ-013 Emergency Egress/Life Safety | Installation per IFC drawings; Safety Code inspection [Lensing: F-002] | Construction completion |
| REQ-014 Fire Sprinkler Applicability | Code consultant determination; if required, sprinkler installation inspection [Lensing: F-001] | Design + Construction |

### Integrated Acceptance Protocol [Lensing: D-002]

**Note:** The Verification table above provides per-requirement verification methods. An integrated acceptance protocol (checklist or acceptance procedure) consolidating all verification methods into a single inspection sequence is TBD. **Resolution trigger:** Create an acceptance checklist in Procedure.md (or as an appendix to this Specification) that consolidates all REQ-001 through REQ-014 verification methods into a defined test and acceptance procedure. See Procedure.md Step 3.3 which references "Verify all requirements in Specification.md are met" but does not define the protocol.

---

## Documentation

### Required Artifacts (from _CONTEXT.md Anticipated Artifacts and RFP)

| Artifact | Responsible Party | Timing |
|---|---|---|
| IFC Architectural Drawings (floor plans, elevations, finish schedule, reflected ceiling plans, door/window schedule) | Architect (PKG-001) | Before construction |
| IFC Electrical Drawings (office receptacle and lighting layout) | Electrical Engineer (PKG-004) / PKG-015 | Before construction |
| IFC Mechanical Drawings (HVAC zoning for office) | Mechanical Engineer (PKG-003) / PKG-013 | Before construction |
| Building Permit | General Contractor (obtained) | Before construction |
| Safety Code Permit(s) | General Contractor | Before/during construction |
| Inspection Reports (building, electrical, mechanical) | General Contractor — copies to County | During/after construction |
| Construction Completion Certificate (CCC) | Owner (Camrose County) | Project closeout |
| Warranty documentation (2-year post-CCC). **Warranty scope for office-specific fit-out items (TBD):** Clarify whether the 2-year warranty covers finish defects, door hardware, ceiling systems, or only structural elements. **Resolution trigger:** Define warranty scope for interior fit-out items per CCDC 14-2013 warranty provisions and RFP §2.10.2. [Lensing: X-005] | General Contractor | At CCC |
| WCB Letter of Clearance | General Contractor | At final payment |
| Construction progress photo documentation (ASSUMPTION: standard practice; confirm if required by project). [Lensing: E-002] | General Contractor | During construction |
