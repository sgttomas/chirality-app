# Specification: DEL-31.03 Operation Manuals

## Scope

This specification defines the requirements for **Operation Manuals** within **PKG-31 Documentation & Deliverables**.

**Purpose:**
Defines and substantiates operation manuals in accordance with Employer's Requirements (ER), providing comprehensive guidance for safe and effective operation of the Canola Oil Transload Facility Phase 1.

**Source:** Decomposition DEL-31.03 (line 688)

**Scope Inclusions:**

The Operation Manuals shall include:
- System-specific operating procedures for all major facility systems (Railcar Unloading, Marine Loading, Product Transfer & Metering, Storage Tanks, Process Piping, Pumps, Valves, Electrical, Control Systems, Instrumentation, Fire Protection, Safety Systems, Buildings)
- Normal operating procedures (start-up, steady-state operation, shutdown)
- Emergency operating procedures (emergency shutdown, alarm response, spill response, fire response)
- Operating parameters, setpoints, and control limits
- Safety procedures and precautions
- Monitoring and inspection requirements
- Troubleshooting guidance
- Facility-wide procedures (overall start-up/shutdown, shift handover, permits-to-work)

**Scope Exclusions:**

- Maintenance procedures and schedules (covered under DEL-31.04 Maintenance Manuals)
- Equipment-specific vendor operation manuals (covered under DEL-31.05 Vendor Documentation, but may be referenced)
- Training materials and programs (separate training deliverables, though operation manuals inform training content)
- Design documentation and calculations (covered under discipline-specific design deliverables)

**Source:** **ASSUMPTION** based on typical operation manual scope; distinction from maintenance manuals per industry practice

**Anticipated deliverable artifacts:**
- System operation manuals

**Source:** _CONTEXT.md; Decomposition line 688

## Requirements

### Functional Requirements

**FR-01: Completeness**
- Operation Manuals shall cover all systems and equipment necessary for facility operations
- All normal, abnormal, and emergency operating scenarios shall be addressed
- **Source:** **ASSUMPTION** per operations documentation requirements; **TBD** — specific scope per Employer's Requirements
- **Rationale:** See Guidance.md (Principle 1: Comprehensive Coverage)
- **Verification:** See Procedure.md (Step 1.1: Develop Operation Manual Outline; Step 6: Completeness Review)

**FR-02: Accuracy and Currency**
- Operation Manuals shall accurately reflect the as-built facility configuration, control systems, and operating procedures
- Manuals shall be based on As-Built Drawings (DEL-31.02), commissioning test results (PKG-30), and verified operating procedures
- **Source:** **ASSUMPTION** per operations documentation accuracy requirements; cross-reference DEL-31.02, PKG-30
- **Rationale:** See Guidance.md (Principle 2: Accuracy and Field Verification)
- **Verification:** See Procedure.md (Step 2: Gather Reference Information; Step 4.2: Field Verification; Step 5: Technical Review)

**FR-03: Usability**
- Operation Manuals shall be written in clear, concise language appropriate for operations personnel
- Procedures shall be logically organized and easy to follow
- Manuals shall include visual aids (diagrams, flowcharts, photographs) where beneficial
- **Source:** **ASSUMPTION** per user-centered documentation requirements
- **Rationale:** See Guidance.md (Principle 3: Operator-Centered Design)
- **Verification:** See Procedure.md (Step 3.4: Format and Usability Check; Step 5.3: Operations Personnel Review)

**FR-04: Safety Integration**
- Operation Manuals shall prominently identify hazards, safety precautions, and safe work practices
- Emergency procedures shall be clearly identified and readily accessible
- Safety critical procedures shall be clearly marked
- **Source:** **ASSUMPTION** per safety management requirements; OBJ-1 (Safe & Reliable Operation, Decomposition line 59)
- **Rationale:** See Guidance.md (Principle 4: Safety First)
- **Verification:** See Procedure.md (Step 3.2: Safety Content Review; Step 5.2: HSE Review)

**FR-05: Operational Flexibility**
- Operation Manuals shall address multiple operating modes (rail-to-tank storage, tank-to-ship loading, direct rail-to-ship transfer)
- Procedures shall support operational flexibility per OBJ-4
- **Source:** OBJ-4 (Operational Flexibility, Decomposition line 62)
- **Verification:** See Procedure.md (Step 3.1: Operating Procedures Development)

### Performance Requirements

**PR-01: Procedure Quality**
- Operating procedures shall be complete, accurate, step-by-step instructions
- Critical steps and cautions shall be clearly identified
- Prerequisites, initial conditions, and expected outcomes shall be stated
- **Source:** **ASSUMPTION** per procedure writing standards; **TBD** — specific procedure format per Employer's Requirements

**PR-02: Document Format and Standards**
- Operation Manuals shall comply with project documentation standards and Employer's format requirements (if specified)
- Consistent terminology, units, and nomenclature shall be used throughout
- Equipment tags and identifiers shall align with As-Built Drawings (DEL-31.02) and Asset Hierarchy (DEL-31.06)
- **Source:** **ASSUMPTION** per documentation standards; cross-reference DEL-31.02, DEL-31.06

**PR-03: Accessibility and Availability**
- Operation Manuals shall be readily accessible to operations personnel (control room, operations offices)
- Electronic and/or hard copy formats per Employer's requirements
- **TBD** — Specific format and distribution requirements per Employer's Requirements

### Interface Requirements

**IR-01: As-Built Drawings Interface**
- Operation Manuals shall reference As-Built Drawings (DEL-31.02) for system configurations, layouts, and P&IDs
- **Source:** Datasheet (References); cross-reference DEL-31.02

**IR-02: Maintenance Manuals Interface**
- Operation Manuals shall be coordinated with Maintenance Manuals (DEL-31.04) to ensure clear delineation between operations and maintenance responsibilities
- **Source:** **ASSUMPTION** per O&M documentation integration; cross-reference DEL-31.04

**IR-03: Vendor Documentation Interface**
- Operation Manuals shall reference Vendor Documentation (DEL-31.05) for equipment-specific operating details
- **Source:** **ASSUMPTION** per vendor documentation integration; cross-reference DEL-31.05

**IR-04: Control Systems Interface**
- Operation Manuals shall describe control system operation, HMI screens, and alarm management consistent with Control System Design (DEL-19.01)
- **Source:** **ASSUMPTION** per control system operations documentation; cross-reference DEL-19.01, PKG-19

**IR-05: Asset Hierarchy Interface**
- Equipment tags and identifiers in Operation Manuals shall align with Asset Hierarchy (DEL-31.06)
- **Source:** **ASSUMPTION** per asset management integration; cross-reference DEL-31.06

**IR-06: Commissioning Records Interface**
- Operation Manuals shall incorporate final operating parameters, setpoints, and procedures validated during commissioning (PKG-30)
- **Source:** **ASSUMPTION** per commissioning closeout; cross-reference PKG-30

### Quality Requirements

**QR-01: Quality Management System Compliance**
- All work shall comply with the project Quality Management Plan

**QR-02: Technical Review and Approval**
- Operation Manuals shall undergo technical review by qualified personnel (discipline engineers, operations subject matter experts)
- Operations personnel shall review manuals for usability and accuracy
- HSE personnel shall review manuals for safety content

**QR-03: Approval Authority**
- Operation Manuals shall be approved by authorized personnel per project procedures
- Employer acceptance/approval (if required per contract)

**QR-04: Version Control and Updates**
- Operation Manuals shall be under version control per project document control procedures
- Change management process shall be established for future updates

### Safety and Regulatory Requirements

**SR-01: Safe & Reliable Operation Support**
- Operation Manuals shall support OBJ-1 (Safe & Reliable Operation) by providing clear, accurate, and safety-focused operating guidance
- **Source:** Decomposition Section 2, OBJ-1 (line 59); Objective Mapping (line 780)

**SR-02: Regulatory Compliance**
- Operation Manuals shall support regulatory compliance requirements (environmental, safety, marine operations)
- **Source:** OBJ-6 (Regulatory Compliance, Decomposition line 64); OBJ-7 (Environmental Protection, line 65)

**SR-03: Emergency Preparedness**
- Emergency operating procedures shall be comprehensive and readily accessible
- Emergency shutdown, spill response, fire response, and evacuation procedures shall be clearly documented

### Lifecycle and Operations Requirements

**LR-01: Lifecycle Cost Optimization**
- Operation Manuals shall support OBJ-9 (Lifecycle Cost Optimization) by enabling efficient operations and reducing operational errors
- **Source:** Decomposition Section 2, OBJ-9 (line 67); Objective Mapping (line 788)

**LR-02: Training Support**
- Operation Manuals shall be suitable for use as training references for operations personnel

**LR-03: Continuous Improvement**
- Operation Manuals shall support continuous improvement by documenting lessons learned and operational best practices

## Standards

**Applicable codes and standards:**

- ISO 9001:2015 — Quality Management Systems
- ISO 14001 — Environmental Management Systems
- ISO 45001 — Occupational Health and Safety Management Systems
- API RP 752 — Management of Hazards (for emergency response procedures) — **ASSUMPTION** if applicable
- NFPA 30 — Flammable and Combustible Liquids Code — **ASSUMPTION** if applicable
- Employer's Requirements — **TBD** — **location TBD**

## Verification

**Verification methods:**

1. **Completeness Review** — All systems and procedures covered
2. **Technical Review** — Technical accuracy verified by qualified engineers
3. **HSE Review** — Safety content reviewed and approved
4. **Operations Personnel Review** — Usability and practicality confirmed
5. **Format and Standards Compliance** — Documentation standards verified
6. **Field Verification** — Procedures verified against actual facility conditions

**Overall Acceptance Criteria:**
- All facility systems covered
- Technical accuracy verified
- Safety content approved
- Operations personnel confirm usability
- Standards compliance confirmed
- Employer acceptance obtained (if required)

## Documentation

**Required outputs:**

1. System Operation Manuals (electronic and hard copy)
2. Operation Manual Master Index
3. Operations Procedures Index
4. Review and Approval Records

**Filing and Archiving:**
- Working documents in `1_Working/`
- Review packages in `2_Checking/To/`
- Issued manuals in `3_Issued/`
- Copies in control room and operations offices
