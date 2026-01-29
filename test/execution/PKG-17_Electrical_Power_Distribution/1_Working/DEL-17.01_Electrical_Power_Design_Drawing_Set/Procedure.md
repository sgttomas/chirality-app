# Procedure: DEL-17.01 Electrical Power Design Drawing Set

## Purpose

This procedure defines the process for producing and managing **Electrical Power Design Drawing Set** within **PKG-17 Electrical Power Distribution**.

**Deliverable Purpose** (Source: Decomposition DEL-17.01 entry): Defines the design arrangement and details for electrical power per ER requirements.

**Deliverable Type**: Drawing
**Responsible Party**: D&B Contractor
**Discipline**: Electrical

**This procedure addresses**:
1. **Production**: How to produce the electrical power design drawing set
2. **Verification**: How to verify drawings are complete, accurate, and code-compliant
3. **Management**: How to manage drawing revisions and issuance

## Prerequisites

### Dependencies

**Per _DEPENDENCIES.md**: NOT_TRACKED — Dependencies are coordinated externally by humans (see execution/_Coordination/_COORDINATION.md).

**Typical upstream dependencies** (coordination required but not formally tracked):
- Site survey and civil site plan (property boundaries, elevations, existing utilities)
- Architectural and structural drawings (building layouts, equipment locations, floor elevations)
- Process engineering information (equipment list, motor data, load requirements)
- Hazardous area classification study (electrical area classification boundaries)
- Utility coordination (BC Hydro service voltage, available fault current, metering requirements)
- Load analysis and design calculations (DEL-17.03) — must be initiated concurrently with drawing development

**Downstream deliverables** (that require this drawing set):
- DEL-17.02 (Electrical Power Technical Specification) — equipment specifications must match drawing set
- DEL-17.04 (Electrical Power Data Sheet Package) — equipment data sheets must match drawing set
- DEL-17.05 (Electrical Power Installation & Test Records) — installation and testing based on drawing set
- Construction procurement and installation — drawing set is primary construction document

### Reference Materials

**Required references** (see _REFERENCES.md):
- **Employer's Requirements**: **TBD** — Volume 2 Parts 1-3 (electrical sections) — **location TBD**
- **Decomposition Document**: /Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md (Section 4 — PKG-17, DEL-17.01 entry)
- **Project CAD Manual**: **TBD** — drawing standards, symbols, layer conventions, title block template
- **Project Document Control Procedures**: **TBD** — drawing numbering, revision control, transmittal procedures

**Applicable codes and standards** (see Specification.md):
- CSA C22.1 (Canadian Electrical Code)
- CSA C22.2 (Equipment standards)
- CSA C22.3 No. 7 (Underground systems, seismic)
- IEEE C2 (NESC)
- IEEE Std 80 (Grounding)
- IEEE Std 141 (Red Book — industrial power distribution)
- IEEE Std 142 (Green Book — grounding practices)
- CSA Z462 / NFPA 70E (Electrical safety)

**Supporting deliverables**:
- DEL-17.03 (Electrical Power Design Calculations) — load analysis, short circuit, voltage drop, protection coordination
- Package 0_References/ folder — **TBD** — BC Hydro standards, manufacturer data, previous project precedents

### Personnel Requirements

**Drawing Originator**:
- Qualified electrical designer or electrical engineer
- **ASSUMPTION**: P.Eng. (Professional Engineer) registration in British Columbia preferred; C.E.T. (Certified Engineering Technologist) acceptable under P.Eng. supervision
- Proficient in electrical design software (CAD) and electrical analysis tools
- Knowledge of CEC, CSA, IEEE standards

**Checker/Reviewer**:
- Independent checker (not the originator)
- P.Eng. or senior C.E.T. with electrical design experience
- Knowledge of CEC requirements and electrical design best practices

**Discipline Lead/Approver**:
- Professional Engineer (P.Eng.) registered in British Columbia
- **Rationale**: P.Eng. seal required for permit submission to BC Safety Authority
- Authority to approve design for construction and sign/seal drawings

**Interdisciplinary Coordination**:
- Representatives from civil, structural, mechanical, instrumentation disciplines for interdisciplinary check (IDC)

**Personnel Competency**:
- **ASSUMPTION**: Personnel qualifications and competency verification per project quality procedures and professional registration requirements

## Steps

### Step 1: Design Initiation and Information Gathering

**Objective**: Collect all necessary input information to begin electrical design.

**Activities**:
1.1. Review Employer's Requirements (ER) for electrical system requirements — **TBD** (ER location).
1.2. Review project decomposition (Section 4 — PKG-17) for package scope and deliverable description.
1.3. Obtain process engineering information:
     - Equipment list with motor nameplate data (HP, voltage, phase, FLA)
     - Process flow diagrams (PFDs) showing equipment relationships
     - Heat tracing requirements and load estimates
     - Control system power requirements
1.4. Coordinate with BC Hydro:
     - Determine available service voltage and location
     - Obtain available fault current (short circuit duty)
     - Confirm metering and protection requirements
     - Identify service installation lead time
1.5. Obtain site survey and civil drawings:
     - Property boundaries, site dimensions, elevations
     - Existing utilities (overhead/underground)
     - Building locations and floor plans
1.6. Obtain hazardous area classification study (if available) — **TBD**.
1.7. Identify applicable codes, standards, and project-specific requirements.

**Output**: Design basis document or checklist confirming all required input information is available or identified as TBD.

**TBD**: Design initiation meeting or kick-off checklist format.

### Step 2: Electrical Load Analysis (Concurrent with Drawing Development)

**Objective**: Determine electrical load requirements and transformer/switchgear sizing.

**Activities**:
2.1. Develop preliminary load list (motors, lighting, HVAC, process loads, control systems).
2.2. Apply diversity/demand factors (not all loads operate simultaneously).
2.3. Estimate transformer and switchgear sizing based on total connected load and demand load.
2.4. Identify load categories: normal power, critical power (UPS), emergency power.
2.5. Document load analysis in DEL-17.03 (Design Calculations).

**Output**: Load analysis summary with transformer sizes, switchgear ratings, and load allocations.

**Interface**: Load analysis (DEL-17.03) is performed concurrently with drawing development — iterative process.

### Step 3: Develop Single Line Diagrams (SLDs)

**Objective**: Create one-line representation of electrical distribution architecture.

**Implements**: FR-1 (System Architecture Representation) — See Specification.md.
**Rationale**: See Guidance.md — Principle 1 (Hierarchical Distribution Architecture).

**Activities**:
3.1. Develop overall facility SLD showing:
     - Utility service entrance and metering
     - MV switchgear lineup
     - Transformers (unit substations) with ratings
     - LV switchgear and MCC lineup
     - Major feeders and distribution panels
     - Protection devices (breakers, fuses) with ratings and settings (preliminary)
3.2. Develop detailed SLDs for major distribution sections:
     - MV distribution (one-line)
     - LV distribution (one-line)
     - MCC bucket schedules (if included in SLD or separate)
3.3. Indicate equipment identification tags (to be coordinated with P&ID and equipment list).
3.4. Show cable/conductor sizes for major feeders (based on preliminary calculations).
3.5. Include one-line legend with symbols and abbreviations.

**CAD Requirements**:
- Use project-standard electrical symbol library — **TBD** (per project CAD manual).
- Follow layer conventions for one-line diagrams — **TBD**.
- Use standard title block template — **TBD**.

**Output**: Single line diagram drawing set (multiple sheets as required).

**Verification**: Self-check for completeness and consistency with load analysis.

### Step 4: Develop MV/LV Distribution Drawings (Site Plans and Layouts)

**Objective**: Document physical locations and arrangements of electrical equipment.

**Implements**: FR-2 (MV Distribution), FR-3 (LV Distribution) — See Specification.md.
**Rationale**: See Guidance.md — Principle 2 (Voltage Level Selection), Consideration 4 (Cable Routing and Installation Methods).

**Activities**:
4.1. Develop site electrical plan showing:
     - Utility service entrance location
     - MV switchgear and transformer locations (substations)
     - LV distribution equipment locations (MCCs, panels)
     - Underground duct bank routing (MV and LV feeders)
     - Overhead routing (if any)
     - Major equipment connections (pumps, tanks, marine loading)
4.2. Develop equipment arrangement drawings:
     - Switchgear and MCC room layouts (plan and elevation views)
     - Equipment spacing and working clearances (per CEC Section 2)
     - Equipment access and maintenance space
4.3. Develop cable routing drawings:
     - Cable tray routing (plan and elevation/isometric views)
     - Conduit routing for branch circuits
     - Duct bank cross-sections and details
4.4. Coordinate with other disciplines:
     - Civil: Duct bank trenching, equipment foundations, grounding grid installation
     - Structural: Cable tray supports, equipment mounting, roof/wall penetrations
     - Mechanical: Avoid conflicts with piping, HVAC, avoid heat sources
     - Architectural: Equipment room layouts, door sizes, access routes

**CAD Requirements**:
- Use project-standard base drawings (site plan, building plans) — coordinate with civil/architectural.
- Follow layer conventions for electrical overlays — **TBD**.
- Use standard electrical equipment symbols and line types — **TBD**.

**Output**: MV/LV distribution drawing set (site plans, equipment layouts, cable routing).

**Verification**: Interdisciplinary check (IDC) to confirm no conflicts with other disciplines.

### Step 5: Develop Cable Schedules

**Objective**: Document all power cables with circuit identification, sizing, routing, and terminations.

**Implements**: FR-4 (Cable Routing and Sizing Documentation) — See Specification.md.
**Rationale**: See Guidance.md — Consideration 2 (Voltage Drop and Power Quality), Consideration 4 (Cable Routing and Installation Methods).

**Activities**:
5.1. Develop cable schedule tables with columns:
     - Circuit ID (circuit number or tag)
     - Description (load served)
     - Voltage level
     - Cable size (AWG or kcmil)
     - Cable type (insulation type, e.g., RW90 XLPE, MV-105 EPR)
     - Number of conductors
     - Cable length
     - Source (equipment and terminal)
     - Destination (equipment and terminal)
     - Protection device (breaker/fuse rating)
     - Conduit/cable tray assignment
     - Installation method (underground, overhead, cable tray, conduit)
5.2. Size cables per CEC Section 4 (ampacity) and voltage drop requirements:
     - Verify ampacity based on conductor size, insulation type, ambient temperature, and installation method
     - Calculate voltage drop for each circuit (max 3% feeders, 5% total)
     - Document cable sizing calculations in DEL-17.03
5.3. Assign cables to conduit or cable tray:
     - Calculate conduit fill per CEC Section 12
     - Calculate cable tray fill per CEC Section 12
5.4. Identify cable color coding or tagging requirements — **TBD** (per project standards).

**Output**: Cable schedule drawing set (multiple sheets as required).

**Verification**: Cross-check cable sizes with load analysis and voltage drop calculations (DEL-17.03).

### Step 6: Develop Grounding Drawings

**Objective**: Document facility grounding system for personnel safety and equipment protection.

**Implements**: FR-5 (Grounding System Documentation) — See Specification.md.
**Rationale**: See Guidance.md — Principle 4 (Grounding and Bonding).

**Activities**:
6.1. Develop site grounding grid layout:
     - Grid conductor size and spacing (based on IEEE Std 80 analysis — DEL-17.03)
     - Ground rod locations (at grid intersections, equipment locations, building corners)
     - Burial depth (typically 0.5-0.6 m)
     - Grid connections to equipment and structures
6.2. Develop equipment grounding details:
     - Transformer and switchgear grounding connections
     - Motor and equipment grounding
     - Tank and piping bonding (equipotential bonding)
     - Lightning protection system (if applicable) — **TBD**
6.3. Detail grounding connection methods:
     - Exothermic welds (Cadweld or equivalent) for permanent connections
     - Bolted connections with corrosion protection (anti-oxidant compound)
     - Ground rod installation details
6.4. Identify grounding electrode resistance requirements and test point locations:
     - Target ground resistance: **ASSUMPTION** < 5 ohms (typical industrial standard)
     - Test well locations for periodic ground resistance testing
6.5. Document grounding calculations in DEL-17.03 (IEEE Std 80 step/touch potential analysis).

**Output**: Grounding drawing set (site grounding plan, equipment grounding details).

**Verification**: Verify grounding system design meets CEC Section 10 and IEEE Std 80 requirements.

### Step 7: Design Calculations (DEL-17.03 Interface)

**Objective**: Perform and document electrical design calculations to verify drawing set.

**Calculations Required** (documented in DEL-17.03):
- Load analysis (connected load, demand load, transformer sizing)
- Short circuit analysis (available fault current at each bus)
- Protection coordination study (breaker/relay settings for selective coordination)
- Voltage drop calculations (cable sizing verification)
- Grounding grid analysis (IEEE Std 80 step/touch potential)
- Arc flash hazard analysis (CSA Z462 incident energy levels) — **TBD** (may be separate study)

**Interface**: Calculations and drawings must be consistent — iterative process:
- Initial drawings based on preliminary calculations
- Final calculations verify drawing set
- Drawings updated if calculations reveal deficiencies

**Output**: Design calculation package (DEL-17.03) supporting drawing set.

### Step 8: Self-Check (Originator Review)

**Objective**: Drawing originator verifies completeness and accuracy before submitting for independent check.

**Self-Check Checklist**:
- [ ] All required drawing types completed (SLDs, distribution, cable schedules, grounding)
- [ ] All equipment identified with consistent tags (match equipment list and P&IDs)
- [ ] Cable sizes verified against calculations (DEL-17.03)
- [ ] Equipment ratings verified against load analysis and short circuit calculations
- [ ] Protection device ratings and settings verified against coordination study
- [ ] Drawing dimensions and elevations verified against civil/structural drawings
- [ ] CAD standards compliance (layers, line weights, text size, symbols)
- [ ] Title block information complete (drawing number, revision, date, originator initials)
- [ ] Drawing cross-references correct (related drawings identified)
- [ ] All TBDs and open items identified and documented

**Output**: Self-checked drawing set with originator sign-off — ready for interdisciplinary check.

**TBD**: Self-check sign-off form or stamp.

### Step 9: Interdisciplinary Check (IDC)

**Objective**: Coordinate electrical drawings with other disciplines to identify and resolve interface issues.

**IDC Process**:
9.1. Distribute drawing set to affected disciplines:
     - Civil: Verify duct bank routing, equipment foundations, grounding grid installation
     - Structural: Verify cable tray support locations and loading, equipment mounting
     - Mechanical: Verify no conflicts with piping, HVAC; verify equipment power connections
     - Instrumentation: Verify control system power, UPS requirements, instrument power distribution
     - Architectural: Verify equipment room layouts, door sizes, access clearances
9.2. Conduct IDC meeting or review session:
     - Review drawings with discipline representatives
     - Identify conflicts or missing interfaces
     - Document comments and action items
9.3. Resolve IDC comments:
     - Revise drawings to address discipline comments
     - Coordinate resolutions (may require design changes by other disciplines)
     - Document resolutions and obtain sign-off from commenting disciplines

**Output**: Drawing set with IDC comments resolved and sign-offs obtained.

**TBD**: IDC comment tracking form or database.

### Step 10: Independent Check (Peer Review)

**Objective**: Independent checker (not the originator) reviews drawing set for technical accuracy and code compliance.

**Independent Check Scope**:
- Technical accuracy: Verify design is sound and calculations support drawing set
- Code compliance: Verify design meets CEC, CSA, IEEE requirements
- Completeness: Verify all required information is present and consistent
- Constructability: Verify drawings are suitable for construction (sufficient detail, no ambiguities)

**Check Criteria**:
- [ ] Load analysis (DEL-17.03) supports equipment sizing shown on drawings
- [ ] Short circuit calculations verify equipment interrupting capacity and withstand ratings
- [ ] Protection coordination study supports protective device settings shown on SLDs
- [ ] Voltage drop calculations verify cable sizes shown on cable schedules
- [ ] Grounding system design complies with CEC Section 10 and IEEE Std 80
- [ ] Equipment spacing and working clearances comply with CEC Section 2
- [ ] Hazardous area equipment (if applicable) complies with CEC Section 18
- [ ] Seismic anchorage requirements identified (CSA C22.3 No. 7)
- [ ] Utility coordination requirements addressed (BC Hydro)
- [ ] All cross-references and interfaces verified

**Output**: Independent check report with comments and required corrections.

**TBD**: Independent check sign-off form and comment resolution process.

### Step 11: Incorporate Check Comments and Finalize

**Objective**: Resolve all check comments and finalize drawing set for approval.

**Activities**:
11.1. Review independent check comments with checker and discipline lead.
11.2. Revise drawings to address all comments (technical corrections, clarifications, additions).
11.3. Update calculations (DEL-17.03) if design changes impact analysis.
11.4. Verify all comments are closed (checker concurrence).
11.5. Update drawing revision (increment revision letter/number).
11.6. Update revision cloud and revision description on each affected drawing sheet.

**Output**: Finalized drawing set with all check comments addressed — ready for approval.

**Verification**: Checker reviews revised drawings and confirms all comments resolved.

### Step 12: Discipline Lead Approval and P.Eng. Seal

**Objective**: Discipline lead (P.Eng.) approves drawing set for construction and affixes professional seal.

**Approval Process**:
12.1. Discipline lead reviews complete drawing set and supporting calculations.
12.2. Verify design is suitable for construction and complies with all applicable codes and standards.
12.3. Affix P.Eng. seal and signature to drawing title blocks (per BC professional practice requirements).
12.4. Update drawing status to "Issued for Construction" (IFC) or appropriate issue status.
12.5. Record approval in drawing register and document control system — **TBD**.

**P.Eng. Seal Requirements** (BC professional practice):
- Professional Engineer registered in British Columbia
- Seal includes P.Eng. name, registration number, signature, and date
- **Rationale**: P.Eng. seal required for submission to BC Safety Authority for electrical permit

**Output**: Approved drawing set with P.Eng. seal — issued for construction (IFC).

### Step 13: Drawing Issuance and Distribution

**Objective**: Issue approved drawing set to construction and other stakeholders.

**Issuance Process**:
13.1. Prepare drawing transmittal documenting:
      - Drawing numbers and revision letters
      - Issue date and issue status (IFC)
      - Distribution list (recipients)
13.2. Upload drawings to project document management system — **TBD** (system name/location).
13.3. Distribute hard copies (if required) — **TBD** (number of sets).
13.4. Update drawing register to reflect issued status.
13.5. File issued drawings in package 3_Issued/ folder with transmittal.

**Output**: Issued drawing set distributed to construction and stakeholders.

**TBD**: Drawing transmittal template and distribution list.

### Step 14: Drawing Maintenance and As-Built Updates (Post-Construction)

**Objective**: Maintain drawing set current during construction; update to as-built conditions upon completion.

**Construction Phase**:
14.1. Track field queries and requests for information (RFIs) related to electrical drawings.
14.2. Issue drawing revisions as needed to clarify or correct design (issued as "Revision A", "Revision B", etc.).
14.3. Maintain revision log and distribute updated drawings to construction.

**As-Built Phase**:
14.4. Obtain marked-up drawings from construction showing actual installed conditions (deviations from design).
14.5. Incorporate as-built redlines into drawing set.
14.6. Issue final as-built drawing set (typically "Revision 0 As-Built" or "Record Drawings").
14.7. File as-built drawings in package 3_Issued/ folder with as-built designation.
14.8. Deliver as-built drawing set to Owner for operations and maintenance use.

**Output**: As-built drawing set reflecting actual installed conditions.

**TBD**: As-built drawing requirements per contract closeout procedures.

## Verification

**Verification Activities Summary**:

| Verification Activity | Performed By | Acceptance Criteria | Documented In |
|-----------------------|--------------|---------------------|---------------|
| **Self-Check** | Drawing originator | No errors or omissions; calculations support design | Self-check checklist / stamp on drawings |
| **Interdisciplinary Check (IDC)** | Affected discipline representatives | No unresolved interface issues or conflicts | IDC comment log and sign-offs |
| **Independent Check** | Independent checker (P.Eng. or senior C.E.T.) | Design is technically sound, code-compliant, and constructible | Independent check report and sign-off |
| **Code Compliance Verification** | Checker and approving P.Eng. | Design complies with CEC, CSA, IEEE, BC regulations | Check report / P.Eng. approval |
| **Calculation Cross-Check** | Checker | Drawing content consistent with approved calculations (DEL-17.03) | Check report referencing calculations |
| **CAD Standards Check** | Originator and checker | Drawings comply with project CAD manual | Self-check and independent check |
| **Approval** | Discipline lead (P.Eng.) | Drawing set suitable for construction and permit submission | P.Eng. seal and signature on drawings |

**Sign-Off Requirements**:
- **Originator**: Initials and date in title block (self-check complete)
- **Checker**: Initials and date in title block (independent check complete)
- **Approver (P.Eng.)**: Professional seal, signature, and date in title block (approval for construction)

**Acceptance Criteria for Issue**:
- All verification activities completed and signed off
- All check comments resolved (no outstanding design issues)
- Drawings comply with project CAD standards — **TBD**
- P.Eng. approval obtained (seal affixed)
- Drawing register updated to "IFC" status
- Transmittal prepared and distribution complete

**TBD**: Specific sign-off protocols and forms per project quality procedures.

## Records

**Documentation Outputs** (Source: _CONTEXT.md anticipated artifacts):

1. **Single Line Diagrams (SLDs)**: Overall electrical distribution architecture, MV/LV one-lines, protection coordination
2. **MV/LV Distribution Drawings**: Site electrical plan, equipment layouts, cable routing
3. **Cable Schedules**: Power cable tabulations with circuit ID, sizing, routing, terminations
4. **Grounding Drawings**: Site grounding grid, equipment grounding, lightning protection

**Record Management**:

**During Development (1_Working/ folder)**:
- Working drafts and revisions maintained in deliverable folder: `/test/execution/PKG-17_Electrical_Power_Distribution/1_Working/DEL-17.01_Electrical_Power_Design_Drawing_Set/`
- Design files (CAD native format), PDFs, calculation support files

**During Review (2_Checking/ folder)**:
- Copies of drawing set submitted for review (IDC, independent check) filed in `2_Checking/To/` with transmittal
- Check comments and resolution records filed in `2_Checking/From/`
- **TBD**: File naming convention for review submittals (e.g., DEL-17.01_Rev0_Check_2026-01-28.pdf)

**Upon Approval (3_Issued/ folder)**:
- Issued drawing set (IFC) filed in `3_Issued/` with transmittal and approval records
- Subsequent revisions (Rev A, Rev B, etc.) filed with revision transmittals
- As-built drawing set filed with as-built designation
- **TBD**: File naming convention for issued drawings (e.g., DEL-17.01_Rev0_IFC_2026-02-15.pdf)

**Drawing Register**:
- Maintain drawing register (list or database) tracking drawing numbers, titles, revisions, issue dates, and status
- **TBD**: Drawing register format and location (project document management system)

**Retention Requirements**:
- Issued drawings: Retain for project life + **TBD** years per contract requirements
- As-built drawings: Deliver to Owner; retain copy for project records
- Design files (CAD native): Retain for **TBD** years per professional practice and contract requirements
- **ASSUMPTION**: Electronic records managed in project document management system per project document control procedures

**Interfaces with Other Deliverables**:
- DEL-17.02 (Electrical Power Technical Specification): Equipment specifications must be consistent with drawing set
- DEL-17.03 (Electrical Power Design Calculations): Calculations support and verify drawing set; calculations and drawings maintained together
- DEL-17.04 (Electrical Power Data Sheet Package): Equipment data sheets match equipment shown on drawings
- DEL-17.05 (Electrical Power Installation & Test Records): Installation and testing performed per drawings; as-built updates reflect test results

**Cross-Disciplinary Coordination Records**:
- IDC meeting minutes and comment logs
- Discipline coordination correspondence
- Interface agreements (where design responsibilities cross discipline boundaries)
- **TBD**: Format and location for coordination records
