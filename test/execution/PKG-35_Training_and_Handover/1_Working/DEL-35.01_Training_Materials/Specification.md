# Specification: DEL-35.01 Training Materials

## Scope

This specification defines the requirements for **Training Materials** within **PKG-35 Training & Handover**.

**Purpose:** Provides project management/control documentation for training materials required by the Employer's Requirements.

*Source: _CONTEXT.md, Decomposition Section 5 (PKG-35, DEL-35.01)*

**Scope Coverage:**

Training materials shall address the complete canola oil transload facility including:
- Railcar unloading system (32 stations on 2 tracks)
- Storage tank operations (3 × 15,000 MT tanks, 45,000 MT total capacity)
- Marine loading system (ship loading via marine loading arms)
- Product transfer and metering systems
- Process control and instrumentation systems
- Electrical power distribution and lighting
- Safety and environmental protection systems
- Emergency response and spill management

*Source: Decomposition Section 1.1 (Key Parameters)*

**Anticipated Deliverable Artifacts:**
- Training manuals (comprehensive written documentation)
- Training presentations (instructional slide decks and visual aids)

*Source: _CONTEXT.md (Anticipated Artifacts)*

**Out of Scope:**
- Employer-provided nitrogen supply system operation (Employer responsibility per Decomposition Section 1.2)
- Training delivery services (instruction/facilitation) — **TBD** whether included in Contractor scope
- Post-handover refresher training — **TBD**

## Requirements

### Functional Requirements

**FR-01: Content Coverage**
Training materials shall provide comprehensive coverage of:
- **FR-01.1**: Normal operating procedures for all facility systems
- **FR-01.2**: Startup and shutdown procedures
- **FR-01.3**: Routine maintenance procedures and schedules
- **FR-01.4**: Troubleshooting guides for common operational issues
- **FR-01.5**: Emergency response procedures including spill response, fire response, and evacuation
- **FR-01.6**: Safety procedures including permit-to-work, lockout/tagout (LOTO), confined space entry
- **FR-01.7**: Environmental protection procedures and monitoring requirements
- **FR-01.8**: Quality control procedures relevant to operations
- **FR-01.9**: Regulatory compliance requirements for terminal operations

*Source: **ASSUMPTION** based on typical bulk liquid terminal training requirements; **TBD**: Confirm specific ER requirements*

**FR-02: Operational Training Content**
- **FR-02.1**: Railcar unloading operations (connection, heating if required, pumping, disconnection, safety interlocks)
- **FR-02.2**: Storage tank operations (level monitoring, temperature monitoring, blending if applicable, inventory management)
- **FR-02.3**: Marine loading operations (ship connection, pre-transfer checks, loading sequence, flow rate control, emergency shutdown)
- **FR-02.4**: Custody transfer metering operations (meter proving, data recording, custody transfer procedures)
- **FR-02.5**: Control system operations (HMI navigation, alarm response, manual override procedures, system diagnostics)

*Source: **ASSUMPTION** based on facility systems per Decomposition Section 1.1*

**FR-03: Maintenance Training Content**
- **FR-03.1**: Preventive maintenance procedures for pumps, valves, loading arms, and instrumentation
- **FR-03.2**: Predictive maintenance techniques (vibration monitoring, thermography, oil analysis if applicable)
- **FR-03.3**: Corrective maintenance procedures and troubleshooting
- **FR-03.4**: Spare parts identification and inventory management
- **FR-03.5**: Equipment-specific OEM maintenance procedures

*Source: **ASSUMPTION** — typical facility maintenance training; **TBD**: Confirm with PKG-31 (Maintenance & Asset Management) deliverables*

**FR-04: Safety Training Content**
- **FR-04.1**: Hazards associated with canola oil handling (slip hazards, hot oil, confined spaces, flammable vapors if applicable)
- **FR-04.2**: Personal protective equipment (PPE) requirements and use
- **FR-04.3**: Permit-to-work system procedures
- **FR-04.4**: Emergency response roles and responsibilities
- **FR-04.5**: Spill containment and response procedures
- **FR-04.6**: First aid and emergency medical response

*Source: **ASSUMPTION** — typical bulk liquid terminal safety training; **TBD**: Confirm with PKG-32 (Health, Safety & Environmental Management) and PKG-33 (Emergency Response Planning)*

**FR-05: Training Material Format**
- **FR-05.1**: Training manuals shall be produced in searchable electronic format (PDF or equivalent)
- **FR-05.2**: Training presentations shall be produced in editable format (PowerPoint or equivalent) for future updates
- **FR-05.3**: All materials shall include table of contents, section numbering, and page numbering
- **FR-05.4**: All materials shall include revision control information (document number, revision, date, author)
- **FR-05.5**: Diagrams, P&IDs, and equipment photos shall be included where they aid understanding

*Source: **ASSUMPTION** — good practice for technical documentation; **TBD**: Confirm project document control requirements*

**FR-06: Language and Accessibility**
- **FR-06.1**: Training materials shall be provided in English as a minimum
- **FR-06.2**: **TBD** — Additional language versions if required by workforce demographics
- **FR-06.3**: Materials shall use clear, concise language appropriate for target audience education level
- **FR-06.4**: Technical jargon shall be defined in a glossary

*Source: **ASSUMPTION** — good practice; **TBD**: Confirm Employer requirements*

### Performance Requirements

**PR-01: Completeness**
Training materials shall cover 100% of facility systems and operations required for safe and compliant operation.

*Source: **ASSUMPTION** — inferred from OBJ-1 (Safe & Reliable Operation, Decomposition Section 2)*

**PR-02: Accuracy**
Training materials shall be technically accurate and consistent with:
- As-built drawings and documentation
- Equipment OEM manuals
- Operating procedures
- Safety procedures
- Regulatory requirements

*Source: **ASSUMPTION** — fundamental quality requirement*

**PR-03: Usability**
Training materials shall be structured to facilitate learning and reference use:
- Logical organization by system or function
- Progressive complexity (basic to advanced topics)
- Cross-referencing between related topics
- Index for quick reference

*Source: **ASSUMPTION** — good practice for training documentation*

**PR-04: Lifecycle Cost Optimization**
Training materials shall support OBJ-9 (Lifecycle Cost Optimization) by:
- Enabling effective knowledge transfer to minimize operating errors
- Reducing maintenance downtime through clear maintenance procedures
- Facilitating future training of new personnel with minimal external training costs
- Supporting self-sufficiency in facility operations and maintenance

*Source: Decomposition Section 2 (OBJ-9), Section 6 (Objective-to-Deliverable Mapping showing DEL-35.01 supports OBJ-9)*
*Note: See Guidance.md Principle 1 for detailed rationale on lifecycle cost optimization through training.*

### Interface Requirements

**IF-01: Integration with Other Deliverables**
Training materials shall reference and integrate content from:
- **IF-01.1**: PKG-27 Operating Manuals (DEL-27.01 to DEL-27.05)
- **IF-01.2**: PKG-31 Maintenance & Asset Management documentation (DEL-31.01 to DEL-31.11)
- **IF-01.3**: PKG-32 Health, Safety & Environmental documentation (DEL-32.01 to DEL-32.08)
- **IF-01.4**: PKG-33 Emergency Response Plans (DEL-33.01 to DEL-33.08)
- **IF-01.5**: PKG-19 Control Systems documentation (DEL-19.01 to DEL-19.05)
- **IF-01.6**: Equipment OEM manuals from equipment supply packages

*Source: **ASSUMPTION** based on package scope; **TBD**: Confirm specific interface deliverables with _DEPENDENCIES.md coordination*

**IF-02: OEM/Supplier Coordination**
- **IF-02.1**: OEM/supplier-provided training materials shall be integrated into comprehensive facility training program
- **IF-02.2**: OEM materials shall be reviewed and supplemented with facility-specific procedures
- **IF-02.3**: Contractor responsible for coordination with OEM/suppliers per _CONTEXT.md (Responsible: D&B Contractor with OEM/Supplier)

*Source: _CONTEXT.md (Responsible party)*

**IF-03: Employer Review and Approval**
- **IF-03.1**: Training materials shall be submitted to Employer for review and approval prior to training commencement
- **IF-03.2**: **TBD** — Submission schedule and review duration per project schedule
- **IF-03.3**: **TBD** — Approval criteria and acceptance process

*Source: **ASSUMPTION** — typical Design & Build contract review process*

### Quality Requirements

**QR-01: Document Control**
All training materials shall comply with the project Quality Management Plan and document control procedures.

*Source: **ASSUMPTION** — standard project requirement*

**QR-02: Technical Review**
Training materials shall undergo:
- **QR-02.1**: Internal technical review by subject matter experts
- **QR-02.2**: Quality assurance review for completeness and accuracy
- **QR-02.3**: Employer review and approval
- **QR-02.4**: **TBD** — Third-party review if required

*Source: **ASSUMPTION** — typical document production quality process*

**QR-03: Version Control**
- **QR-03.1**: Each document/presentation shall have unique document number
- **QR-03.2**: Revision history shall be maintained and documented
- **QR-03.3**: Superseded versions shall be clearly marked and archived

*Source: **ASSUMPTION** — good practice for document management*

**QR-04: As-Built Alignment**
Training materials shall be updated to reflect as-built conditions:
- **QR-04.1**: Materials shall incorporate design changes and construction modifications
- **QR-04.2**: Final training materials shall be issued after commissioning completion to capture operational learnings
- **QR-04.3**: **TBD** — Process for updating training materials during commissioning phase

*Source: **ASSUMPTION** — necessary for accurate training content*

## Standards

**Applicable Codes and Standards:**

**Quality Management:**
- ISO 9001:2015 — Quality Management Systems
  *Source: **ASSUMPTION** — typical project quality standard*

**Health, Safety, and Environmental:**
- ISO 14001:2015 — Environmental Management Systems
- ISO 45001:2018 — Occupational Health and Safety Management Systems
- ANSI/API RP 75 — Safety and Environmental Management Systems for Onshore Plants
  *Source: **ASSUMPTION** — applicable to bulk liquid terminal operations*

**Training and Competency:**
- **TBD** — Industry-specific training standards (e.g., ISGOTT for marine operations if applicable)
- **TBD** — Canadian regulatory training requirements for bulk liquid terminals

**Documentation Standards:**
- **TBD** — Project document management standards
- **TBD** — Employer's document formatting and style guide requirements

**Employer's Requirements:**
- Volume 2 Part 1: General Requirements — **TBD: Specific training material requirements (section number TBD)**
- Volume 2 Part 2: Civil & Process Mechanical Works — **TBD: System-specific training requirements (section number TBD)**
- Volume 2 Part 3: Building Works — **TBD: Building systems training requirements (section number TBD)**

*Source: Decomposition Section 3 (Reference Documents); specific sections TBD pending document access*

## Verification

**Verification Methods:**

**VM-01: Technical Accuracy Review**
- Subject matter expert review of technical content
- Cross-check with design documentation (P&IDs, drawings, specifications)
- Cross-check with equipment OEM manuals
- **Acceptance criteria**: Zero technical errors identified during final review
- **Implementation**: See Procedure.md Step 3.1 (Internal Technical Review)

**VM-02: Completeness Check**
- Verify all facility systems are covered
- Verify all operational modes are addressed (normal, startup, shutdown, emergency)
- Verify all maintenance activities are documented
- **Acceptance criteria**: 100% coverage of requirements FR-01 through FR-06

**VM-03: Format and Standards Compliance**
- Review document formatting against project standards
- Verify revision control information is present
- Verify all diagrams and images are legible and correctly referenced
- **Acceptance criteria**: Full compliance with project document control procedures

**VM-04: Stakeholder Review**
- Employer review and approval
- Operations team review (if Employer operations team established)
- OEM/supplier review of equipment-specific content
- **Acceptance criteria**: All review comments resolved and approvals obtained

**VM-05: Usability Testing**
- **ASSUMPTION**: Pilot training session to validate material effectiveness
- **ASSUMPTION**: Trainee feedback on clarity and completeness
- **Acceptance criteria**: **TBD** — Trainee comprehension assessment passing rate

**VM-06: Alignment with Training Records**
- Verify training materials align with DEL-35.02 (Training Installation & Test Records) competency requirements
- **Acceptance criteria**: Training materials support all competencies defined in DEL-35.02

*Source: **ASSUMPTION** — typical document verification process; cross-reference to DEL-35.02 per package deliverables*

## Documentation

**Required Documentation Outputs:**

**Output-01: Training Manuals**
- Comprehensive written training manuals organized by system/discipline
- Format: Searchable PDF, minimum 8.5" × 11" page size
- Content: Text, diagrams, P&IDs, photos, procedures, troubleshooting guides
- Quantity: **TBD** — Number of copies (electronic and printed)

*Source: _CONTEXT.md (Anticipated Artifacts)*

**Output-02: Training Presentations**
- Instructional slide decks for classroom or self-study use
- Format: PowerPoint (editable) and PDF
- Content: Key concepts, system overviews, operational sequences, safety highlights
- Quantity: **TBD** — One presentation per training module

*Source: _CONTEXT.md (Anticipated Artifacts)*

**Output-03: Supporting Materials (ASSUMPTION)**
- Quick reference guides (laminated cards or posters)
- Training videos (if produced)
- Competency assessment forms (cross-reference DEL-35.02)
- Training attendance records template (cross-reference DEL-35.02)

**Documentation Management:**

**DM-01: Revision Control**
- Document numbering system: **TBD** — Per project document control procedures
- Revision tracking: All changes documented in revision history
- Supersession: Superseded versions clearly marked and archived

**DM-02: Distribution**
- Electronic copies: Uploaded to project document management system
- Printed copies: **TBD** — Number and distribution locations
- Access control: **TBD** — Restricted distribution or general access

**DM-03: Records Retention**
- Training materials retained per project records retention schedule
- Retention period: **TBD** — Minimum facility design life (25 years assumed) or per regulatory requirements
- Archive location: **TBD** — Employer's document archive system

**DM-04: Update Process**
- Process for updating materials based on facility modifications: **TBD**
- Responsibility for future updates: **ASSUMPTION** — Employer/facility operator post-handover
- Change request procedure: **TBD**

*Source: **ASSUMPTION** — good practice for document management; specific requirements TBD*
