# Specification — DEL-020-01: Building Systems Commissioning

**Document Type:** Specification (normative)
**Deliverable ID:** DEL-020-01_Commissioning
**Package:** PKG-020 — Commissioning & Closeout
**Generated:** 2026-02-26 (Pass 1+2, P1_P2 run)
**Enriched:** 2026-02-26 (Pass 3, Semantic Lensing)

---

## Scope

### In Scope

This deliverable covers the comprehensive commissioning of all building systems installed under the 2026 Design Build of West Dried Meat Lake Regional Landfill Maintenance Shop Addition (AB-2026-01424), including:

- Functional testing and performance verification of all mechanical, plumbing, electrical, low-voltage, and crane systems. (Source: SOW-0090, R-01 §1.0)
- Operator training for County facility staff on all commissioned systems. (Source: `_CONTEXT.md` Scope Definition)
- Documentation compilation: test records, O&M manuals, training logs, and commissioning reports. (Source: `_CONTEXT.md` Scope Definition)
- System optimization to achieve specified performance criteria. (Source: `_CONTEXT.md` Scope Definition)
- Confirmation of facility readiness for occupancy. (Source: `_CONTEXT.md` Success Criteria)
- Coordination with County project manager throughout commissioning activities. (Source: RFP §3.1)

**Note [C-002]:** Fire protection systems are not mentioned in any accessible source (RFP §3.4, Decomposition, or design package references) as installed systems for this facility. If fire protection or fire alarm systems are included in the IFC design, they would require commissioning and Safety Code compliance under this deliverable. If no fire protection is provided, the absence should be documented as a scope determination in the Commissioning Plan. This is TBD pending review of IFC design documents. (Source: _SEMANTIC_LENSING.md C-002. ProposedAuthority: RFP §3.4; Alberta Building Code fire protection requirements.)

### Out of Scope

- Trade installations (covered by PKG-013, PKG-014, PKG-015, PKG-016). (Source: Decomposition PKG-020 Exclusions)
- Warranty and guarantee period obligations post-CCC (covered by PKG-021). (Source: Decomposition PKG-020 Exclusions)
- Final inspection activities (covered by DEL-020-02). (Source: Decomposition §7 PKG-020)
- Closeout documentation package assembly (covered by DEL-020-03). (Source: Decomposition §7 PKG-020)
- Permit fee payments (Owner responsibility). (Source: RFP §3.3.1)

---

## Requirements

### REQ-020-01-001: Commissioning Scope — All Building Systems

**Statement:** The Proponent shall perform commissioning of all building systems installed under this contract.

**Source:** SOW-0090; R-01 §1.0

**Priority:** Mandatory

**Notes:** "All building systems" is interpreted to include at minimum the mechanical/HVAC systems, plumbing and water systems, electrical and low-voltage systems, crane and lifting systems, and building envelope operational systems (doors, service pit). ASSUMPTION: scope interpretation per Decomposition OBJ-004 (mechanical, plumbing, water storage) and OBJ-005 (electrical and low-voltage).

---

### REQ-020-01-002: Completion Deadline

**Statement:** All commissioning work, including documentation, shall be completed on or before December 31, 2026.

**Source:** SOW-0091; RFP §3.1 (bold heading: "All Work pertaining to the Design Build of West Dried Meat Lake Regional Landfill Maintenance Shop Addition must be completed on or before December 31, 2026.")

**Priority:** Mandatory (contractual deadline)

**Notes:** This is an absolute deadline. Commissioning scheduling must account for construction completion and allow adequate time before this date.

---

### REQ-020-01-003: Commissioning Prerequisites — Construction Completion

**Statement:** Commissioning shall not commence until construction is substantially complete and quality control has verified all work meets specifications.

**Source:** `_DEPENDENCIES.md` (declared upstream dependency: PKG-019 completion); Decomposition PKG-020 Exclusions ("Trade installations [respective packages]")

**Priority:** Mandatory

**Notes:** This requirement is a sequencing constraint, not an acceptance criterion. PKG-019 quality control sign-off (DEL-019-04) is the gate event.

---

### REQ-020-01-003A: Commissioning Plan Required

**Statement:** A Commissioning Plan shall be developed and approved before commissioning testing activities begin. The plan shall define scope, protocols, system-by-system acceptance criteria, schedule, and responsibility assignments.

**Source:** Procedure.md Prerequisites (previously ASSUMPTION-tagged); standard commissioning practice; CCDC 14-2013 (general obligation for work planning). Note [A-002]: This requirement was previously stated only as an ASSUMPTION in Procedure prerequisites and is now formalized as a normative requirement.

**Priority:** Mandatory

**Notes:** The Commissioning Plan is the foundational governance document for all testing activities. Without a formally required and approved plan, commissioning execution and acceptance criteria lack a controlled basis. (Source for elevation: _SEMANTIC_LENSING.md A-002.)

---

### REQ-020-01-004: Functional Testing per Specifications

**Statement:** All systems shall be functionally tested. Testing shall confirm that each system operates per its design specifications and meets the performance criteria established in the design documents.

**Source:** `_CONTEXT.md` Success Criteria ("All systems commissioned and tested per specifications"); SOW-0090

**Priority:** Mandatory

**Notes:** Specific acceptance criteria per system (e.g., HVAC air exchange rate, cistern pump flow rate, crane load capacity, electrical circuit ratings) are TBD pending completion of IFC design documents. ASSUMPTION: performance parameters will derive from IFC drawings and engineered specifications produced under PKG-003, PKG-004, PKG-006 design packages.

**Note [A-003]:** Measurable acceptance criteria for mechanical systems (HVAC air exchange rate, heating output), electrical systems (circuit load verification method), and building envelope systems (door operation criteria) remain TBD pending IFC documents. Without defined criteria, compliance determination cannot be made. These criteria must be established in the Commissioning Plan once IFC documents are available. (Source: _SEMANTIC_LENSING.md A-003. ProposedAuthority: IFC design documents from PKG-003, PKG-004, PKG-006.)

---

### REQ-020-01-005: Performance Criteria — Mechanical Systems

**Statement:** Mechanical and HVAC systems shall be verified to achieve operational readiness, including the heating system, makeup air unit, air exchanger, exhaust systems, and ceiling fans.

**Source:** Decomposition OBJ-004 ("Install and commission all mechanical, plumbing, and water storage systems to operational readiness"); RFP §3.4 (design requirements for high recovery heating, high volume air exchanger, exhaust hoses and fans, welding ventilation, ceiling fans)

**Priority:** Mandatory

**Specific Performance Criteria:** TBD — to be established in IFC design documents and Commissioning Plan.

---

### REQ-020-01-006: Performance Criteria — Plumbing and Water Systems

**Statement:** Plumbing and water storage systems shall be verified to achieve operational readiness, including the 50,000 L cistern, pump system, septic system, drainage systems, and bulk water fill.

**Source:** Decomposition OBJ-004; RFP §3.4 (50,000 L cistern; pump 100 LPM with 2.5" fill connection; 2,000 US Gallon septic tank; sump drains; mud sump; bulk water fill)

**Priority:** Mandatory

**Specific Performance Criteria:**

| System | Design Parameter | Source |
|---|---|---|
| Cistern | Minimum 50,000 L capacity | RFP §3.4 |
| Pump | 100 LPM flow rate; 2.5 inch cistern filling connection | RFP §3.4 |
| Septic Tank | 2,000 US Gallon holding capacity | RFP §3.4 |
| Other systems | TBD — per IFC plumbing drawings | |

---

### REQ-020-01-007: Performance Criteria — Electrical and Low-Voltage Systems

**Statement:** All electrical and low-voltage systems shall be verified to achieve operational readiness, including three-phase power distribution, all lighting circuits, all receptacle circuits, crane power, overhead door power, security camera wiring, and radio antenna wiring.

**Source:** Decomposition OBJ-005 ("Install and commission all electrical and low-voltage systems to operational readiness"); RFP §3.4 (three-phase power; multiple electrical plugs for welding — high voltage); RFP §3.3.2

**Priority:** Mandatory

**Specific Performance Criteria:** TBD — per IFC electrical drawings (PKG-004). ASSUMPTION: Welding receptacles are 50A/240V per Decomposition Decision D-009.

**Note [X-001]:** The commissioning scope boundary for low-voltage systems (security cameras, radio antenna) is TBD. It is unclear whether commissioning includes only wiring continuity testing or also functional testing of end devices. End device functional testing may require Owner-supplied equipment. This scope determination must be resolved in the Commissioning Plan with Owner input. (Source: Procedure.md Step 3 item 7; _SEMANTIC_LENSING.md X-001. ProposedAuthority: Owner (Camrose County) — who supplies end devices.)

---

### REQ-020-01-008: Performance Criteria — Crane and Lifting Systems

**Statement:** The two (2) 5-tonne overhead cranes on trolley shall be functionally tested and verified to achieve operational readiness.

**Source:** Decomposition OBJ-005; RFP §3.4 ("2 – 5-tonne overhead cranes on a trolley")

**Priority:** Mandatory

**Specific Performance Criteria:** TBD — load testing protocol to be established in Commissioning Plan. ASSUMPTION: load testing per applicable Alberta Safety Code requirements for overhead cranes (specific code reference TBD — location TBD in accessible sources).

**Note [C-001]:** Crane load testing is safety-critical and subject to mandatory Alberta regulation. The specific Alberta crane safety code section and edition governing overhead crane load testing and acceptance are TBD. Both this requirement and Procedure Step 4 acknowledge this gap explicitly. The applicable code must be identified during the design phase and included in the Commissioning Plan. (Source: _SEMANTIC_LENSING.md C-001. ProposedAuthority: Alberta Safety Codes Officer; crane manufacturer documentation.)

---

### REQ-020-01-009: Operator Training

**Statement:** Operator training shall be completed for County facility staff covering the operation and maintenance of all commissioned systems prior to facility occupancy.

**Source:** `_CONTEXT.md` Scope Definition; `_CONTEXT.md` Success Criteria ("Operator training completed")

**Priority:** Mandatory

**Notes:** Training schedule, format, and responsible party for delivery are TBD pending Commissioning Plan development. ASSUMPTION: Training shall include O&M documentation handover.

---

### REQ-020-01-010: Commissioning Documentation

**Statement:** All commissioning activities, test results, and operator training shall be documented and compiled into a commissioning report delivered to the Owner.

**Source:** `_CONTEXT.md` Success Criteria ("Commissioning reports documented"); `_CONTEXT.md` Scope Definition ("documentation compilation")

**Priority:** Mandatory

**Required Artifacts:** Commissioning Plan; system test records; performance verification report; operator training records; O&M manuals. (ASSUMPTION: artifact list is standard practice; specific Owner requirements for format are TBD.)

---

### REQ-020-01-011: Coordination with County Project Manager

**Statement:** The Proponent shall coordinate all commissioning inspections and activities through the County project manager.

**Source:** RFP §3.1 ("The successful Proponent shall coordinate inspections, weekly meetings, and billing through the County project manager.")

**Priority:** Mandatory

**Notes:** County project manager identity is TBD — to be confirmed at project award per RFP §3.1.

**Note [F-003]:** The Owner acceptance process for commissioning results is currently undefined. "County PM sign-off" is referenced in multiple documents but no formal acceptance mechanism is specified — no acceptance criteria for the overall commissioning package, no dispute resolution mechanism, and no provisions for conditional acceptance. The acceptance process must be defined in the Commissioning Plan or project agreement, with reference to CCDC 14-2013 acceptance provisions. (Source: Specification.md REQ-020-01-011; Procedure.md Step 11; _SEMANTIC_LENSING.md F-003. ProposedAuthority: CCDC 14-2013 acceptance provisions; RFP §2.14.)

---

### REQ-020-01-012: Handoff to Final Inspection

**Statement:** Commissioning shall be completed and confirmed prior to initiating final inspection activities (DEL-020-02). Commissioning documentation shall be available for the final inspection.

**Source:** `_DEPENDENCIES.md` ("DEL-020-02: Final inspection activities include verification of commissioning completion"); Decomposition §7 PKG-020

**Priority:** Mandatory (sequencing requirement)

---

### REQ-020-01-013: Alberta Safety Code Compliance

**Statement:** All commissioned systems shall comply with applicable Alberta Safety Codes.

**Source:** RFP §3.3.2 ("The proposed building must adhere to all Alberta Safety Codes."); SOW-0084, SOW-0085 (inspection coordination and reports)

**Priority:** Mandatory

**Notes:** Specific Safety Code sections applicable to each commissioned system are TBD — specific code references not cited in accessible sources (location TBD).

**Note [A-001]:** The reference to "applicable Alberta Safety Codes" is cited repeatedly across all documents but no specific code sections or editions are identified for any discipline (building, electrical, plumbing, gas, crane). This creates risk of incomplete compliance scoping. Specific Alberta Safety Code sections applicable to each commissioned system discipline must be identified during the design phase and documented in the Commissioning Plan. (Source: Specification.md Standards; Datasheet.md Conditions; _SEMANTIC_LENSING.md A-001. ProposedAuthority: RFP §3.3.2; Alberta Safety Codes Act.)

---

### REQ-020-01-014: Commissioning Agent Qualifications

**Statement:** The Commissioning Agent shall possess qualifications appropriate to direct and manage commissioning of an industrial maintenance facility, including authority to halt testing if safety concerns arise during commissioning activities.

**Source:** Note [F-002] — elevated from gap identified in `_CONTEXT.md` Key Roles and `_STATUS.md` Outstanding Items. ASSUMPTION: minimum qualifications, independence requirements, and authority scope are TBD pending project governance decisions.

**Priority:** Mandatory

**Notes:** The Commissioning Agent is the single most critical role for this deliverable, yet no qualification requirements, experience criteria, or authority scope were previously specified. The Guidance document discusses the dedicated-vs-embedded question (see Guidance Trade-offs). Minimum qualifications should be established when the role is assigned. (Source: _SEMANTIC_LENSING.md F-002. ProposedAuthority: Project governance; Owner decision.)

---

## Standards

| Standard / Code | Applicability | Accessibility Status |
|---|---|---|
| Alberta Safety Codes Act and applicable Safety Codes (building, electrical, plumbing, gas, etc.) | Governs all commissioned systems — specific code sections per discipline TBD (see Note [A-001]) | ASSUMPTION: likely applicable — specific code editions not cited in RFP (location TBD) |
| CCDC 14–2013 Design-Build Stipulated Price Contract | Governs contractual obligations including commissioning and completion | Referenced in RFP §2.7; Decomposition §1 |
| Alberta OH&S Act and Regulations | Governs site safety during commissioning activities | Referenced indirectly via SOW-0083; Prime Contractor obligations (RFP §2.15) |
| Applicable crane safety standards (Alberta) | Governs load testing and operation of overhead cranes — specific code section TBD (see Note [C-001]) | ASSUMPTION: likely applicable (location TBD) |
| Prompt Payment and Construction Lien Act (Alberta) | Governs lien holdback related to project payment | RFP §2.13.2 (Lien Holdback) |

---

## Verification

| Requirement | Verification Approach |
|---|---|
| REQ-020-01-001: Commissioning scope — all systems | Review Commissioning Plan scope list; confirm all installed systems included |
| REQ-020-01-002: Completion deadline (Dec 31, 2026) | Track commissioning schedule against contractual deadline |
| REQ-020-01-003: Construction completion prerequisite | Confirm PKG-019 sign-off and DEL-019-04 QC completion before commissioning start |
| REQ-020-01-003A: Commissioning Plan required | Confirm Commissioning Plan approved before testing commences |
| REQ-020-01-004: Functional testing | Review completed system test records; verify all systems tested |
| REQ-020-01-005: Mechanical systems performance | Review HVAC/mechanical test records against IFC design parameters |
| REQ-020-01-006: Plumbing and water systems performance | Review flow/capacity test records; confirm cistern (50,000 L), pump (100 LPM), septic (2,000 USG) |
| REQ-020-01-007: Electrical and low-voltage performance | Review electrical test records; confirm all circuits energized and functional |
| REQ-020-01-008: Crane systems performance | Review crane functional and load test records |
| REQ-020-01-009: Operator training | Review training attendance records, training delivery confirmation, and demonstrated competence evidence (see Note [E-002]) |
| REQ-020-01-010: Commissioning documentation | Review completeness of commissioning report package before handoff |
| REQ-020-01-011: County PM coordination | Review meeting and communication records throughout commissioning |
| REQ-020-01-012: Handoff to final inspection | Confirm commissioning report package delivered to PM prior to DEL-020-02 initiation |
| REQ-020-01-013: Alberta Safety Code compliance | Confirm all applicable Safety Code inspections passed; obtain copies of inspection reports |
| REQ-020-01-014: Commissioning Agent qualifications | Confirm Commissioning Agent assignment documentation includes qualification evidence |

**Note [E-002]:** Operator training verification (REQ-020-01-009) currently relies solely on attendance records and delivery confirmation, which confirms training was delivered but not that competence was achieved. Training effectiveness verification should include at least one of: demonstrated operation of key systems, written/oral assessment, or observed task performance. The specific mechanism is TBD — to be defined in the Commissioning Plan. (Source: Specification.md Verification REQ-020-01-009 row; Procedure.md Step 10; _SEMANTIC_LENSING.md E-002. ProposedAuthority: Owner training requirements; standard commissioning practice.)

---

## Documentation

### Required Artifacts

| Artifact | Description | Required By |
|---|---|---|
| Commissioning Plan | Scope, protocols, schedule, responsibilities, acceptance criteria | REQ-020-01-003A |
| System Test Records | Completed functional test checklists per system | REQ-020-01-004 through REQ-020-01-008 |
| Performance Verification Report | Summary of system performance results vs. design criteria | REQ-020-01-004; `_CONTEXT.md` Success Criteria |
| Operator Training Records | Training attendance logs; training materials provided; competence evidence | REQ-020-01-009 |
| O&M Manuals | Operation and maintenance documentation for all systems | REQ-020-01-010; `_CONTEXT.md` Scope Definition |
| Commissioning Completion Report | Formal report confirming commissioning outcomes | REQ-020-01-010 |
| Safety Code Inspection Reports | Copies of all completed inspection reports | RFP §3.3.2; SOW-0085 |

ASSUMPTION: Specific format and submission requirements for documentation are TBD — to be confirmed with Owner at project award.
