# Procedure: DEL-17.02 Electrical Power Technical Specification

## Purpose

This procedure defines the process for producing and managing **Electrical Power Technical Specification** within **PKG-17 Electrical Power Distribution**.

**Deliverable Purpose** (Source: Decomposition DEL-17.02 entry): Defines performance, materials, and workmanship requirements for electrical power per ER requirements.

**Deliverable Type**: Specification (Technical Specification)
**Responsible Party**: D&B Contractor
**Discipline**: Electrical

**This procedure addresses**:
1. **Production**: How to develop technical specifications for electrical equipment (transformers, switchgear, MCCs, cables)
2. **Verification**: How to verify specifications are complete, compliant with codes/standards, and suitable for procurement
3. **Management**: How to manage specification revisions and coordination with other deliverables

## Prerequisites

### Dependencies

**Per _DEPENDENCIES.md**: NOT_TRACKED — Dependencies are coordinated externally by humans (see execution/_Coordination/_COORDINATION.md).

**Typical upstream dependencies** (coordination required but not formally tracked):
- Load analysis and equipment sizing (DEL-17.03) — must be initiated concurrently with specification development
- Single line diagrams and equipment list (DEL-17.01) — provides equipment types, quantities, and ratings
- Employer's Requirements — provides project-specific performance and quality requirements
- Utility coordination (BC Hydro) — provides service voltage class and fault current for switchgear ratings
- Hazardous area classification study — determines equipment ratings for classified areas (if applicable)

**Downstream deliverables** (that require this specification):
- DEL-17.04 (Electrical Power Data Sheet Package) — equipment data sheets must demonstrate compliance with specifications
- Equipment procurement — specifications are basis for bid solicitation and evaluation
- DEL-17.05 (Electrical Power Installation & Test Records) — installation and testing performed per specifications

### Reference Materials

**Required references** (see _REFERENCES.md):
- **Employer's Requirements**: **TBD** — Volume 2 Parts 1-3 (electrical equipment specifications, performance criteria) — **location TBD**
- **Decomposition Document**: /Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md (Section 4 — PKG-17, DEL-17.02 entry)
- **Project Specification Template**: **TBD** — CSI MasterFormat Division 26 specification template or project-specific format

**Applicable codes and standards** (see Specification.md):
- CSA C88, C802 (Transformers)
- CSA C22.2 No. 31, No. 254, No. 38, C68.3 (Switchgear, MCCs, Cables)
- IEEE C37 series (Switchgear), IEEE C57 series (Transformers), IEEE 693 (Seismic)
- CEC (Canadian Electrical Code), CSA C22.3 No. 7, CSA Z462
- NEMA, UL standards

**Supporting deliverables**:
- DEL-17.01 (Electrical Power Design Drawing Set) — single line diagrams, equipment list
- DEL-17.03 (Electrical Power Design Calculations) — load analysis, short circuit, equipment sizing rationale
- Package 0_References/ folder — **TBD** — Manufacturer catalogs, precedent specifications, industry standards

### Personnel Requirements

**Specification Author**:
- Qualified electrical engineer or senior electrical designer
- **ASSUMPTION**: P.Eng. (Professional Engineer) registration in British Columbia preferred; experience with industrial electrical equipment specifications
- Knowledge of CSA, IEEE, UL, NEMA standards and specification writing best practices
- Familiarity with design-build procurement and equipment bid evaluation

**Reviewer/Checker**:
- Independent reviewer (not the author)
- P.Eng. or senior engineer with electrical equipment specification experience
- Knowledge of applicable codes, standards, and equipment performance requirements

**Discipline Lead/Approver**:
- Professional Engineer (P.Eng.) registered in British Columbia
- Authority to approve specifications for procurement and construction

**Interdisciplinary Coordination**:
- Mechanical engineer (motor loads, HVAC loads)
- Instrumentation engineer (control system power, UPS requirements)
- Civil engineer (equipment foundations, underground duct banks)
- Fire protection engineer (fire safety requirements, LSZH cable requirements)

**Personnel Competency**:
- **ASSUMPTION**: Personnel qualifications and competency verification per project quality procedures and professional registration requirements

## Steps

### Step 1: Specification Initiation and Requirements Gathering

**Objective**: Collect all necessary information to begin specification development.

**Activities**:
1.1. Review Employer's Requirements (ER) for electrical equipment requirements — **TBD** (ER location).
1.2. Review project decomposition (Section 4 — PKG-17) for package scope and deliverable description.
1.3. Review design drawings (DEL-17.01 — in progress concurrently):
     - Single line diagrams (equipment types and ratings)
     - Equipment list (quantities and general arrangement)
1.4. Review design calculations (DEL-17.03 — in progress concurrently):
     - Load analysis (transformer sizing)
     - Short circuit analysis (switchgear and MCC interrupting ratings)
     - Protection coordination (breaker settings and coordination)
1.5. Coordinate with BC Hydro:
     - Service voltage class (25 kV or 13.8 kV)
     - Available fault current (for switchgear ratings)
1.6. Obtain project-specific requirements:
     - Hazardous area classification (equipment for classified areas) — **TBD**
     - Seismic requirements (IEEE 693 or CSA C22.3 No. 7)
     - Corrosion protection requirements (marine environment)
     - SCADA/communication requirements (PKG-19 coordination)
1.7. Identify applicable codes, standards, and industry best practices.
1.8. Review manufacturer catalogs and data sheets:
     - Transformers (ABB, Schneider, Eaton, etc.)
     - Switchgear (ABB, Schneider, Eaton, etc.)
     - MCCs (ABB, Schneider, Eaton, Rockwell, etc.)
     - Cables (Southwire, General Cable, Nexans, etc.)

**Output**: Specification development checklist or requirements matrix confirming all required input information is available or identified as TBD.

**TBD**: Specification initiation meeting or kick-off checklist format.

### Step 2: Select Specification Template and Organization

**Objective**: Establish specification document structure and format.

**Activities**:
2.1. Obtain project specification template — **TBD** (project specification manual or CSI MasterFormat template).
2.2. Organize specification by equipment category (typical CSI MasterFormat Division 26 organization):
     - Section 26 05 00: General Electrical Requirements (scope, submittals, QA, references)
     - Section 26 11 00: Liquid-Filled Transformers
     - Section 26 12 00: Dry-Type Transformers
     - Section 26 24 00: Medium Voltage Switchgear
     - Section 26 25 00: Low Voltage Switchgear
     - Section 26 26 00: Motor Control Centers
     - Section 26 27 00: Medium Voltage Cables
     - Section 26 28 00: Low Voltage Power Cables
     - Section 26 29 00: Cable Accessories (terminations, tray, conduit, grounding materials)
2.3. Establish specification section structure (typical three-part CSI format):
     - **Part 1: General** (scope, related sections, references, definitions, submittals, quality assurance, warranty)
     - **Part 2: Products** (performance requirements, materials, construction, testing, manufacturers)
     - **Part 3: Execution** (installation, connections, field testing, commissioning)
2.4. Decide specification approach (per Guidance.md — Principle 2):
     - **Performance-based** (preferred for design-build): Specify required performance, allow multiple manufacturers
     - **Performance-based with pre-qualified manufacturers**: List acceptable manufacturers to limit bidders to proven suppliers
     - **Prescriptive ("or equal")**: Specify brand/model with "or approved equal" provision

**Output**: Specification template with sections and structure established.

**Decision**: **TBD** — Confirm specification approach with Employer and project team (performance-based with pre-qualified list recommended for major equipment).

### Step 3: Draft General Requirements Section (26 05 00)

**Objective**: Write general requirements applicable to all electrical equipment.

**Implements**: FR-5 (Submittal and Quality Requirements) — See Specification.md.
**Rationale**: See Guidance.md — Principle 5 (Submittal and Quality Assurance Requirements).

**Activities**:
3.1. **Scope and Related Sections**:
     - Define overall scope of electrical power distribution work
     - Identify related specification sections (civil, structural, mechanical, instrumentation)
3.2. **References**:
     - List applicable codes and standards (CSA, IEEE, UL, NEMA)
     - Reference project documents (drawings, calculations, Employer's Requirements)
3.3. **Definitions**:
     - Define technical terms and abbreviations used in specifications
3.4. **Submittals**:
     - **Pre-Award Submittals** (if applicable): Equipment data sheets for bid evaluation
     - **Pre-Installation Submittals**: Shop drawings, product data (manufacturer catalogs), certifications (CSA/UL marks, seismic qualification), installation instructions
     - **Post-Installation Submittals**: Factory acceptance test (FAT) reports, field test reports, as-built information, operation and maintenance (O&M) manuals
     - **Submittal Schedule**: Define submittal timing (e.g., shop drawings due 60 days after contract award, FAT reports due 30 days before shipment)
3.5. **Quality Assurance**:
     - **Manufacturer Qualifications**: Minimum years in business, ISO 9001 certification, equipment warranty
     - **Factory Testing**: FAT requirements per applicable standards (CSA, IEEE)
     - **Equipment Certification**: CSA or UL certification marks required
     - **Seismic Qualification**: IEEE 693 certificates required for major equipment
3.6. **Delivery, Storage, and Handling**:
     - Protection during shipping and storage
     - Environmental conditions for storage (temperature, humidity)
     - Handling procedures (lifting points, weight limits)
3.7. **Warranty**:
     - Minimum warranty period (typically 1 year from substantial completion or 18 months from shipment, whichever is earlier)
     - Warranty coverage (defects in materials and workmanship)

**Output**: General Requirements section (26 05 00) complete.

### Step 4: Draft Equipment-Specific Specification Sections

**Objective**: Write detailed specifications for each equipment category.

**Implements**: FR-1 (Comprehensive Equipment Specifications), SR-1 through SR-5 — See Specification.md.
**Rationale**: See Guidance.md — Principles 1-6, Considerations 1-10.

**For each equipment category (Transformers, Switchgear, MCCs, Cables), perform the following**:

#### Step 4a: Define Performance Requirements

**Transformer Specification** (Sections 26 11 00 / 26 12 00):
- Ratings: kVA, voltage ratio, impedance, temperature rise — **TBD** (from load analysis — DEL-17.03)
- Taps: ±5% (four 2.5% taps above and below nominal)
- Efficiency: TP-1 or better (NRCan Energy Efficiency Regulations)
- Sound level: Maximum dBA at 1 meter — **TBD**
- Cooling: ONAN (self-cooled) for liquid-filled; AN (air natural) for dry-type
- Seismic: IEEE 693 High Performance Level

**MV Switchgear Specification** (Section 26 24 00):
- Voltage class: 25 kV or 15 kV — **TBD** (from utility coordination)
- Continuous current rating: Bus and breaker ratings — **TBD** (from load analysis)
- Interrupting capacity: kA symmetrical RMS — **TBD** (from short circuit analysis — DEL-17.03)
- Arc-resistant: Type 2B per IEEE C37.20.7 (ASSUMPTION — see Guidance trade-offs)
- Circuit breakers: Vacuum (VCB), stored energy, electrically operated, drawout
- Protection: Microprocessor relays with communication (Modbus TCP or IEC 61850) — **TBD** (coordinate with PKG-19)

**LV Switchgear Specification** (Section 26 25 00):
- Voltage rating: 600V or 480V — **TBD**
- Continuous current rating: Bus and breaker ratings — **TBD**
- SCCR: kA RMS symmetrical — **TBD** (from short circuit analysis)
- Circuit breakers: ICCB or MCCB, drawout or bolt-on
- Trip units: Electronic (programmable LSIG)

**MCC Specification** (Section 26 26 00):
- Voltage rating: 600V or 480V — **TBD**
- Bus rating: Horizontal bus continuous current — **TBD**
- SCCR: kA RMS symmetrical — **TBD**
- Starters: NEMA combination starters (Size 1-5), FVNR
- VFDs: Specify VFD requirements for selected motors — **TBD** (coordinate with process/mechanical engineers)
- Control power: 120 VAC from CPT

**Cable Specification** (Sections 26 27 00 / 26 28 00):
- MV cables: Voltage class (25 kV or 15 kV), conductor (copper, Class B), insulation (XLPE), shielding, jacket (PE for direct burial)
- LV cables: Voltage rating (600V), conductor (copper, Class B), insulation (RW90 XLPE), configuration (3/C or 4/C), jacket (PVC or LSZH)
- Cable sizes: **TBD** — Reference cable schedules (DEL-17.01) and ampacity calculations (DEL-17.03)

#### Step 4b: Define Materials and Construction Requirements

**For each equipment type**:
- Standards compliance (CSA, IEEE, UL, NEMA)
- Construction type (e.g., metal-clad switchgear, modular MCC)
- Materials (copper vs. aluminum conductors, insulation types, enclosure materials)
- Accessories (instrumentation, protection devices, interlocks, space heaters)
- Enclosure ratings (NEMA 1 indoor, NEMA 3R outdoor, NEMA 4X outdoor corrosive environment)
- Seismic qualification (IEEE 693 or CSA C22.3 No. 7)

**Apply project-specific requirements** (from Step 1):
- Marine/industrial environment: NEMA 4X enclosures for outdoor equipment (stainless steel or coated per ISO 12944)
- High seismic zone: IEEE 693 High Performance Level
- Hazardous areas: Equipment suitable for Class I Division 2 or Zone 2 (if applicable) — **TBD**

#### Step 4c: Define Testing and Documentation Requirements

**Factory Tests** (per applicable standards):
- Transformers: Routine tests per CSA C88/C802 (resistance, polarity, voltage ratio, no-load loss, impedance, dielectric tests); optional tests (temperature rise, sound level)
- Switchgear: Dielectric test, primary injection test, relay functional test, mechanical operation test
- MCCs: Dielectric test, control circuit functional test, mechanical operation test
- Cables: Hi-Pot test (MV cables), insulation resistance test (optional for LV)

**Documentation Requirements**:
- Certified test reports (factory tests)
- Nameplate data (equipment ratings and serial numbers)
- Installation, operation, and maintenance (IOM) manuals
- Shop drawings (equipment layout, one-line diagrams, control schematics, dimensional drawings)
- As-built information (cable termination records, relay settings as-left)

#### Step 4d: Define Installation and Execution Requirements

**Installation**:
- Equipment location and mounting (coordinate with civil/structural for foundations and supports)
- Clearances and working space (per CEC Section 2)
- Equipment grounding and bonding
- Cable terminations and connections
- Seismic anchorage (per CSA C22.3 No. 7)

**Field Testing and Commissioning**:
- Installation inspection (verify proper installation per manufacturer instructions and code requirements)
- Insulation resistance (Megger) testing
- Protective relay functional testing and settings verification
- High-potential (Hi-Pot) testing (MV equipment and cables)
- Commissioning tests (integrated system testing, load testing)

**Output**: Equipment-specific specification sections (26 11 00, 26 12 00, 26 24 00, 26 25 00, 26 26 00, 26 27 00, 26 28 00) complete.

**Iteration**: Steps 4a-4d are iterative — draft initial specifications based on preliminary information, then refine as design calculations and drawings are finalized.

### Step 5: Coordinate with Design Calculations and Drawings

**Objective**: Ensure specifications are consistent with calculations and drawings.

**Activities**:
5.1. Cross-check equipment ratings in specifications against design calculations (DEL-17.03):
     - Transformer kVA ratings match load analysis
     - Switchgear interrupting capacity matches or exceeds short circuit analysis results
     - Cable sizes and ampacities match cable sizing calculations
5.2. Cross-check equipment specifications against single line diagrams and equipment list (DEL-17.01):
     - Equipment types and quantities consistent
     - Voltage classes and ratings consistent
     - Equipment identification tags consistent
5.3. Resolve any discrepancies:
     - If calculations show larger equipment needed, update specifications
     - If drawings show different equipment, coordinate changes with drawings and calculations
5.4. Document basis of design:
     - Reference calculations supporting equipment ratings (e.g., "Transformer sizing per DEL-17.03 Load Analysis")
     - Reference drawings showing equipment (e.g., "Equipment shown on DEL-17.01 Single Line Diagrams")

**Output**: Specifications consistent with calculations and drawings; discrepancies resolved.

**Verification**: Checker verifies consistency across deliverables.

### Step 6: Interdisciplinary Coordination and Review

**Objective**: Coordinate specifications with other disciplines and resolve interface issues.

**Activities**:
6.1. Distribute specification draft to affected disciplines:
     - **Mechanical**: Motor specifications, HVAC loads, pump data
     - **Instrumentation (PKG-19)**: Control system power requirements, UPS specifications, communication protocols
     - **Civil**: Equipment foundations, underground duct banks, grounding grid installation
     - **Fire Protection**: Fire safety requirements, LSZH cable requirements, transformer fire protection
6.2. Conduct interdisciplinary review meeting or review session:
     - Review specifications with discipline representatives
     - Identify interface requirements and coordination items
     - Document comments and action items
6.3. Resolve interdisciplinary comments:
     - Revise specifications to address discipline comments
     - Coordinate resolutions (may require input from other disciplines)
     - Obtain sign-off from commenting disciplines

**Output**: Specifications with interdisciplinary comments resolved and sign-offs obtained.

**TBD**: Interdisciplinary review comment tracking form or database.

### Step 7: Technical Review and Quality Check

**Objective**: Independent reviewer verifies specifications are complete, compliant, and suitable for procurement.

**Review Scope**:
- **Code Compliance**: Verify specifications reference and comply with applicable CSA, IEEE, UL, NEMA standards
- **Completeness**: Verify all equipment categories addressed, all performance requirements defined, all submittals and testing specified
- **Consistency**: Verify specifications consistent with drawings (DEL-17.01) and calculations (DEL-17.03)
- **Procurement Suitability**: Verify specifications are clear, unambiguous, and provide sufficient information for competitive bidding
- **Constructability**: Verify installation and testing requirements are practical and achievable

**Check Criteria**:
- [ ] All equipment types identified (transformers, switchgear, MCCs, cables)
- [ ] Performance requirements defined (ratings, standards, testing)
- [ ] Equipment sizing supported by calculations (DEL-17.03)
- [ ] Equipment consistent with drawings (DEL-17.01)
- [ ] Submittal requirements defined (shop drawings, test reports, certifications, manuals)
- [ ] Quality assurance requirements defined (manufacturer qualifications, factory testing, equipment certification)
- [ ] Installation and testing requirements defined (installation procedures, field testing, commissioning)
- [ ] Project-specific requirements addressed (seismic, corrosion protection, hazardous areas, SCADA communication)
- [ ] Applicable codes and standards referenced (CSA, IEEE, UL, NEMA, CEC)
- [ ] All TBDs and open items identified and documented

**Output**: Technical review report with comments and required corrections.

**TBD**: Independent check sign-off form and comment resolution process.

### Step 8: Incorporate Review Comments and Finalize

**Objective**: Resolve all review comments and finalize specifications for issue.

**Activities**:
8.1. Review technical review comments with reviewer and discipline lead.
8.2. Revise specifications to address all comments (technical corrections, clarifications, additions).
8.3. Update calculations (DEL-17.03) or drawings (DEL-17.01) if specification changes impact design.
8.4. Verify all comments are closed (reviewer concurrence).
8.5. Update specification revision (increment revision letter/number).
8.6. Update revision history and cover sheet.

**Output**: Finalized specifications with all review comments addressed — ready for approval.

**Verification**: Reviewer confirms all comments resolved.

### Step 9: Discipline Lead Approval

**Objective**: Discipline lead (P.Eng.) approves specifications for procurement and construction.

**Approval Process**:
9.1. Discipline lead reviews complete specification package and supporting calculations/drawings.
9.2. Verify specifications are suitable for procurement (competitive bidding) and construction.
9.3. Verify specifications comply with all applicable codes, standards, and Employer's Requirements.
9.4. Approve and sign specification cover sheet or transmittal.
9.5. Update specification status to "Issued for Construction" (IFC) or appropriate issue status.
9.6. Record approval in document register and document control system — **TBD**.

**P.Eng. Seal** (if required):
- **TBD**: Confirm if P.Eng. seal required on specifications (seal typically required for permit drawings but may not be required for specifications unless specifically requested by Employer or authority having jurisdiction).

**Output**: Approved specification package — issued for procurement and construction (IFC).

### Step 10: Specification Issuance and Distribution

**Objective**: Issue approved specifications to procurement and construction.

**Issuance Process**:
10.1. Prepare specification transmittal documenting:
      - Specification section numbers and titles
      - Issue date and issue status (IFC)
      - Distribution list (procurement, construction, Employer, design team)
10.2. Upload specifications to project document management system — **TBD** (system name/location).
10.3. Distribute hard copies (if required) — **TBD** (number of sets).
10.4. Update specification register to reflect issued status.
10.5. File issued specifications in package 3_Issued/ folder with transmittal.

**Output**: Issued specification package distributed to procurement and construction.

**TBD**: Specification transmittal template and distribution list.

### Step 11: Specification Maintenance During Procurement and Construction

**Objective**: Maintain specifications current during procurement; update to reflect actual equipment procured.

**Procurement Phase**:
11.1. Review equipment submittals (shop drawings, product data, test reports) against specifications.
11.2. Evaluate submittals for compliance:
      - Verify equipment meets or exceeds specified performance requirements
      - Verify equipment is certified to specified standards (CSA/UL marks, seismic qualification)
      - Verify manufacturer qualifications (ISO 9001, warranty, experience)
11.3. Approve, conditionally approve, or reject submittals:
      - **Approved**: Equipment meets specifications, proceed with procurement
      - **Approved as Noted**: Minor deviations acceptable, proceed with noted conditions
      - **Revise and Resubmit**: Equipment does not meet specifications, resubmit with corrections
      - **Rejected**: Equipment does not meet specifications, not acceptable
11.4. Track submittal status and maintain submittal register.
11.5. Issue specification revisions (addenda or bulletins) if changes required during procurement.

**Construction Phase**:
11.6. Track field queries and requests for information (RFIs) related to specifications.
11.7. Issue specification clarifications or revisions as needed (issued as "Revision A", "Revision B", etc.).
11.8. Maintain revision log and distribute updated specifications to construction.

**As-Built Phase**:
11.9. Update specifications to reflect actual equipment procured and installed:
      - Manufacturer, model, serial numbers
      - Equipment ratings and settings as-installed
      - Deviations from original specifications (if any)
11.10. Issue final as-built specification package (typically "Revision 0 As-Built" or "Record Specifications").
11.11. File as-built specifications in package 3_Issued/ folder with as-built designation.
11.12. Deliver as-built specifications to Owner for operations and maintenance use.

**Output**: As-built specification package reflecting actual equipment procured and installed.

**TBD**: Submittal review and as-built specification requirements per contract closeout procedures.

## Verification

**Verification Activities Summary**:

| Verification Activity | Performed By | Acceptance Criteria | Documented In |
|-----------------------|--------------|---------------------|---------------|
| **Requirements Gathering Check** | Specification author | All required input information identified (ER, calculations, drawings, codes/standards) | Requirements checklist |
| **Interdisciplinary Review** | Affected discipline representatives | No unresolved interface issues or missing coordination items | IDC comment log and sign-offs |
| **Technical Review** | Independent reviewer (P.Eng. or senior engineer) | Specifications complete, compliant with codes/standards, consistent with calculations/drawings, suitable for procurement | Technical review report and sign-off |
| **Code Compliance Verification** | Reviewer and approving P.Eng. | All applicable codes and standards referenced; requirements traceable to codes or design basis | Review report / approval sign-off |
| **Calculation/Drawing Consistency Check** | Reviewer | Equipment ratings in specifications match calculations; equipment types/quantities match drawings | Cross-check matrix or review report |
| **Procurement Suitability Review** | Reviewer and procurement team (if available) | Specifications clear, unambiguous, competitive, and provide sufficient information for bidding | Review report |
| **Approval** | Discipline lead (P.Eng.) | Specifications suitable for procurement and construction; all review comments resolved | P.Eng. approval signature on cover sheet or transmittal |

**Sign-Off Requirements**:
- **Author**: Initials and date on specification cover sheet (draft complete)
- **Reviewer**: Initials and date on specification cover sheet (technical review complete)
- **Approver (P.Eng.)**: Signature and date on specification cover sheet or transmittal (approval for procurement and construction)

**Acceptance Criteria for Issue**:
- All verification activities completed and signed off
- All review comments resolved (no outstanding technical issues)
- Specifications consistent with approved drawings and calculations
- P.Eng. approval obtained
- Specification register updated to "IFC" status
- Transmittal prepared and distribution complete

**TBD**: Specific sign-off protocols and forms per project quality procedures.

## Records

**Documentation Outputs** (Source: _CONTEXT.md anticipated artifacts):

1. **Transformer Specification**: Liquid-filled and dry-type transformer requirements (Sections 26 11 00 / 26 12 00)
2. **Switchgear Specification**: MV and LV switchgear requirements (Sections 26 24 00 / 26 25 00)
3. **MCC Specification**: Motor control center requirements (Section 26 26 00)
4. **Cable Specification**: MV, LV, and control cable requirements (Sections 26 27 00 / 26 28 00 / 26 29 00)
5. **General Requirements**: Submittals, QA, references applicable to all electrical equipment (Section 26 05 00)

**Record Management**:

**During Development (1_Working/ folder)**:
- Working drafts and revisions maintained in deliverable folder: `/test/execution/PKG-17_Electrical_Power_Distribution/1_Working/DEL-17.02_Electrical_Power_Technical_Specification/`
- Specification files (Microsoft Word or PDF), supporting reference materials

**During Review (2_Checking/ folder)**:
- Copies of specifications submitted for review (interdisciplinary, technical) filed in `2_Checking/To/` with transmittal
- Review comments and resolution records filed in `2_Checking/From/`
- **TBD**: File naming convention for review submittals (e.g., DEL-17.02_Electrical_Spec_Rev0_Check_2026-01-28.pdf)

**Upon Approval (3_Issued/ folder)**:
- Issued specification package (IFC) filed in `3_Issued/` with transmittal and approval records
- Subsequent revisions (Rev A, Rev B, addenda, bulletins) filed with revision transmittals
- As-built specification package filed with as-built designation
- **TBD**: File naming convention for issued specifications (e.g., DEL-17.02_Electrical_Spec_Rev0_IFC_2026-02-15.pdf)

**Specification Register**:
- Maintain specification register (list or database) tracking specification section numbers, titles, revisions, issue dates, and status
- **TBD**: Specification register format and location (project document management system)

**Retention Requirements**:
- Issued specifications: Retain for project life + **TBD** years per contract requirements
- As-built specifications: Deliver to Owner; retain copy for project records
- Supporting materials (manufacturer catalogs, submittal reviews): Retain for **TBD** years per professional practice and contract requirements
- **ASSUMPTION**: Electronic records managed in project document management system per project document control procedures

**Interfaces with Other Deliverables**:
- **DEL-17.01** (Electrical Power Design Drawing Set): Equipment shown on drawings must match specifications; drawings and specifications maintained together
- **DEL-17.03** (Electrical Power Design Calculations): Equipment ratings in specifications must be supported by calculations; calculations and specifications maintained together
- **DEL-17.04** (Electrical Power Data Sheet Package): Manufacturer data sheets must demonstrate compliance with specifications; equipment procurement based on specifications
- **DEL-17.05** (Electrical Power Installation & Test Records): Installation and testing performed per specifications; test results verify compliance

**Cross-Disciplinary Coordination Records**:
- Interdisciplinary review meeting minutes and comment logs
- Discipline coordination correspondence
- Interface agreements (where specifications affect other disciplines)
- **TBD**: Format and location for coordination records

**Submittal Review Records** (during procurement):
- Equipment submittal register (tracking status of shop drawings, product data, test reports)
- Submittal review forms (approved, approved as noted, revise and resubmit, rejected)
- Submittal review comments and contractor responses
- **TBD**: Submittal management system or database
