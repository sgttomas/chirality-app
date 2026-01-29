# Procedure: DEL-16.04 Valve Data Sheet Package

## Purpose

This procedure defines the process for producing and managing **Valve Data Sheet Package** within **PKG-16 Valves & Specialty Equipment**.

**Deliverable Purpose:** Defines and substantiates individual valve selections per ER requirements for the Canola Oil Transload Facility.

**Source:** `_CONTEXT.md`

**Deliverable Type:** Data Sheet
**Responsible Party:** D&B Contractor
**Discipline:** Mechanical

**Scope:** This procedure covers the development of valve datasheets from initial parameter identification through vendor data incorporation and As-Built documentation, for three valve categories: control valves, isolation valves, and relief valves.

## Prerequisites

### Dependencies

**Dependency Tracking Mode:** NOT_TRACKED
- Dependencies are coordinated externally by humans (see `execution/_Coordination/_COORDINATION.md`)
- Upstream deliverables and input data to be confirmed prior to commencement

**Source:** `_DEPENDENCIES.md`

**Typical Upstream Inputs (advisory only — not formally tracked):**

**For All Valve Datasheets:**
- P&IDs (piping and instrumentation diagrams) — valve tag numbers, service descriptions, line numbers, fail-safe modes
- Piping line list — line sizes, pressure classes, pipe material
- Equipment datasheets — protected equipment data for relief valves (MAWP, volume, geometry)

**For Control Valve Datasheets:**
- DEL-16.03 Valve Design Calculations — required Cv, selected valve size, trim type, actuator size
- DEL-16.02 Valve Technical Specification — materials, leakage class, testing requirements
- Process design (PFDs, process simulations) — flow rates, pressures, temperatures, fluid properties
- Control philosophy document — fail-safe modes, control requirements, instrumentation

**For Isolation Valve Datasheets:**
- P&IDs — valve locations and operation type (manual, pneumatic, electric)
- Piping design — line sizes, pressure classes, flange ratings
- HAZOP (DEL-27.02) — safety-critical isolation valves and fail-safe modes (if applicable)

**For Relief Valve Datasheets:**
- DEL-16.03 Valve Design Calculations — set pressure, orifice designation, relief capacity
- Equipment datasheets — protected equipment MAWP, design pressure, volume (for pressure vessels)
- HAZOP (DEL-27.02) — relief scenarios and recommendations
- Relief valve discharge piping design — discharge routing, back pressure

**Source:** Inputs inferred from datasheet requirements; specific coordination TBD

### Reference Materials

**Required References:**
- See `_REFERENCES.md` for applicable reference documents
- See `0_References/` in package directory for reference materials

**Key References (to be obtained):**
- Employer's Requirements (Volume 2 Parts 1–3) — **TBD** — datasheet format and content requirements
- Project Engineering Standards — **TBD** — datasheet templates, numbering system, review/approval procedures
- Applicable codes and standards (see Specification.md, Section "Standards")
  - ISA Form S20.50 (Control Valve Datasheet Template)
  - API 526 (Relief Valve Standard Orifices)
  - API 600/608/609 (Isolation Valve Standards)
  - ASME B16.34 (Valve Pressure-Temperature Ratings)
  - CSA B51 (Canadian Pressure Equipment Code)

**Source:** Reference requirements inferred from deliverable type; `_REFERENCES.md` indicates no references identified yet

**Datasheet Templates:**
- **Control Valves:** ISA Form S20.50 or project-specific template based on ISA format — **TBD**
- **Isolation Valves:** Project-specific template — **TBD** (no industry-standard form)
- **Relief Valves:** Project-specific template — **TBD** (no industry-standard form)
- **Specialty Items:** Project-specific template (check valves, strainers, etc.) — **TBD**

**Vendor Data (post-procurement):**
- Vendor certified data (Cv tables, torque curves, dimensional data)
- Vendor submittal drawings (outline drawings, cross-sections)
- Vendor test certificates (pressure test, seat leakage test, set pressure test)
- Vendor material certificates (MTRs for body, trim, bolting)

### Personnel Requirements

**Qualifications:**
- **Design Engineer (Originator):** Mechanical engineer with experience in valve selection for process facilities; familiarity with control valves, isolation valves, and relief valves
- **Reviewer:** Senior mechanical engineer or discipline lead; familiarity with datasheet content and format
- **Discipline Lead (Approver):** Professional Engineer (P.Eng.) authorized to approve datasheets per project authority matrix

**Source:** Typical personnel requirements for datasheet development; specific qualifications TBD per project quality procedures

**Competency Requirements:**
- Familiarity with P&IDs and piping line lists
- Understanding of valve types (control, isolation, relief) and applications
- Knowledge of valve sizing principles (Cv, set pressure, actuator torque)
- Proficiency in datasheet software/tools (Excel, Word, specialized datasheet software)
- **ASSUMPTION:** Personnel competency per project quality procedures

## Steps

### Step 1: Parameter Identification and Data Collection

**Action:** Identify valves requiring datasheets and collect input data from source documents.

**Valve Identification:**

1. **Review P&IDs:** Identify all valves with tag numbers:
   - Control valves: FV, PCV, LCV, TCV prefixes (flow, pressure, level, temperature control)
   - Isolation valves (automated): MOV, AOV, SOV prefixes (motor, air, solenoid operated)
   - Isolation valves (manual): XV, HV, or similar prefix
   - Relief valves: PSV, PRV, TSV prefixes (pressure, thermal safety valves)
   - Check valves: CV or similar prefix
   - Specialty items: Strainers, filters, etc.

2. **Create Valve Register:** Compile list of all valves with:
   - Tag number
   - Valve type (control, isolation, relief, check, etc.)
   - Service description
   - P&ID reference (document number, revision, sheet number)
   - Line number
   - Status (datasheet required: Yes/No)

3. **Prioritize Datasheet Development:**
   - **Priority 1 (Critical Valves):** Control valves, relief valves, ESD valves — required for early procurement and safety review
   - **Priority 2 (Automated Isolation):** Motor-operated and pneumatic-operated isolation valves — required for electrical/control design
   - **Priority 3 (Manual Isolation, Check Valves):** Manual valves, check valves — lower priority; may be standardized with minimal custom datasheets

**Data Collection Checklists (by Valve Type):**

**Control Valve Data Collection:**
- Tag number and service description (from P&ID)
- P&ID reference and line number
- DEL-16.03 calculation number and results (Cv, valve size, trim type, actuator size)
- Process conditions (flow rates, pressures, temperatures, fluid properties) — from DEL-16.03 or process datasheets
- Fail-safe mode (FC, FO, FL) — from P&ID or control philosophy
- Material requirements (body, trim, seat) — from DEL-16.02 specification
- Leakage class — from DEL-16.02 specification or project standards
- Instrumentation requirements (positioner type, limit switches, solenoids) — from instrumentation datasheets or control philosophy

**Isolation Valve Data Collection:**
- Tag number and service description (from P&ID)
- P&ID reference and line number
- Valve type (gate, ball, butterfly) — from P&ID or piping specification
- Valve size (DN or NPS) — from piping line list
- Pressure class — from piping line list or DEL-14.02 specification
- Operation type (manual, pneumatic, electric) — from P&ID
- Actuator requirements (if automated) — from DEL-16.03 calculations (torque, fail-safe mode)
- Material requirements — from DEL-16.02 specification or piping specification
- End connections — from piping specification (flanged, threaded, welded)

**Relief Valve Data Collection:**
- Tag number and protected equipment (from P&ID)
- P&ID reference
- DEL-16.03 calculation number and results (set pressure, orifice designation, relief capacity, governing scenario)
- Protected equipment data (MAWP, design pressure, volume, geometry) — from equipment datasheets
- Relief valve type (conventional, balanced-bellows, pilot-operated) — from DEL-16.03 calculation
- Inlet/outlet connection sizes — from DEL-16.03 calculation or piping design
- Discharge arrangement (location, piping size, back pressure) — from DEL-16.01 valve arrangement drawings or piping design
- Material requirements — from DEL-16.02 specification
- ASME stamp required ("UV" for vessels, "V" for piping) — from protected equipment type
- CSA B51 registration requirement — **TBD** per project regulatory strategy

**Data Verification:**
- Verify all data is from approved/issued source documents (not draft or superseded revisions)
- Check for consistency (valve size matches line size, pressure class adequate for design pressure, etc.)
- Identify any TBD items requiring resolution

**Source:** Typical data collection process for valve datasheets

### Step 2: Datasheet Preparation (Initial Issue)

**Action:** Populate datasheet templates with collected data.

**Datasheet Format Selection:**
- **Control Valves:** Use ISA Form S20.50 template or project adaptation — **TBD**
- **Isolation Valves:** Use project-specific template based on typical content (see Datasheet.md — Construction section)
- **Relief Valves:** Use project-specific template based on API 526 requirements
- **Format:** **TBD** — Electronic forms (Excel, Word), database (Access, project datasheet software), or hybrid

**Datasheet Preparation Process:**

**For Each Valve:**

1. **Open Datasheet Template:** Select appropriate template for valve type (control, isolation, relief)

2. **Populate Identification Section:**
   - Valve tag number
   - Service description
   - P&ID reference (document number, revision, sheet)
   - Line number
   - System (e.g., Railcar Unloading, Marine Loading, Tank Farm)

3. **Populate Process Conditions Section:**
   - Fluid name and properties (density, viscosity, vapor pressure)
   - Operating conditions (flow rates, pressures, temperatures)
   - Design conditions (maximum flow, pressure, temperature)
   - Special conditions (viscosity variation, winterization, heat tracing)

4. **Populate Valve Specifications Section:**
   - Valve type (globe, ball, butterfly, gate, relief, etc.)
   - Valve size (DN or NPS)
   - Pressure class (ASME Class 150, 300, etc.)
   - Body material (316SS, carbon steel, etc. per DEL-16.02)
   - Trim material
   - Seat material (soft-seated PTFE or metal)
   - End connections (flanged, threaded, welded)
   - Leakage class (for control and isolation valves)

5. **Populate Sizing/Performance Section (from DEL-16.03):**
   - **Control Valves:** Required Cv, selected Cv, trim characteristic, rangeability, cavitation assessment
   - **Relief Valves:** Set pressure, orifice designation, relief capacity, governing scenario
   - **Isolation Valves:** N/A (no sizing typically required; size matches line size)

6. **Populate Actuation Section (if applicable):**
   - Actuator type (pneumatic, electric, manual)
   - Actuator action (ATO, ATC, etc.)
   - Fail-safe mode (FC, FO, FL) with justification
   - Required torque/thrust (from DEL-16.03)
   - Selected actuator size (TBD vendor selection at this stage)
   - Safety factor
   - Stroking time requirement
   - Accessories (positioner, limit switches, solenoid, air set, manual override)

7. **Populate Codes & Standards Section:**
   - Design code (IEC 60534, API 600/608/609, API 526, etc.)
   - Flange standard (ASME B16.5)
   - Testing standard (API 598, IEC 60534-4, API 527, etc.)
   - Material standards (ASTM)

8. **Populate Vendor Data Section (Initially Blank):**
   - Mark as "TBD — To be populated post-procurement"
   - Vendor data incorporated in Step 4 after valve procurement

9. **Add Calculation Reference:**
   - Reference DEL-16.03 calculation number for sizing data

10. **Add Notes (if applicable):**
    - Special requirements, design considerations, TBD items

**Quality Check During Preparation:**
- All required fields populated (or marked TBD)
- Units indicated for all numerical values
- Consistent terminology and abbreviations
- Clear and concise service descriptions
- Cross-references correct (calculation numbers, P&ID references)

**Source:** Typical datasheet preparation workflow; specific process TBD per project datasheet tool/software

### Step 3: Interdisciplinary Check (IDC) and Review

**Action:** Coordinate datasheets with other disciplines for interface verification; conduct technical review.

**Interdisciplinary Check (see also Specification.md — Interface Requirements):**

Distribute datasheets for IDC review via project document management system — **TBD**. Coordinate with:

1. **Process Discipline:**
   - Verify flow rates, pressures, temperatures match process design
   - Verify fluid properties correct
   - Confirm control valve sizing assumptions (pressure drop allocation)

2. **Piping Discipline:**
   - Verify valve sizes match line sizes
   - Verify pressure classes match piping specification
   - Verify end connections and flange ratings correct
   - Coordinate relief valve discharge piping (back pressure limits)

3. **Instrumentation Discipline:**
   - Verify control valve instrumentation (positioner type, signal type 4–20 mA/HART/Fieldbus)
   - Verify limit switches and position transmitters
   - Coordinate solenoid valves for ESD function

4. **Control Systems Discipline:**
   - Verify fail-safe modes consistent with control logic
   - Verify ESD valve closure time requirements
   - Verify communication protocol for smart positioners (HART, Foundation Fieldbus, Profibus)

5. **Electrical Discipline:**
   - Verify electric actuator motor specifications (voltage, phase, frequency, enclosure rating)
   - Coordinate motor starter and MCC requirements

6. **Safety / HAZOP:**
   - Verify relief valve scenarios consistent with HAZOP recommendations
   - Verify control valve and ESD valve fail-safe modes per HAZOP safety requirements

**IDC Comment Collection and Resolution:**
- Allow review period (typically 5–10 working days) — **TBD**
- Collect IDC comments via project comment management system — **TBD**
- Categorize comments:
  - **Category A (Must Resolve):** Technical errors, non-compliance with codes/standards, safety issues
  - **Category B (Incorporate if Feasible):** Recommendations, optimizations, clarifications
  - **Category C (Noted):** Informational comments, suggestions for future
- Resolve Category A comments; respond to Category B/C comments
- Update datasheets if significant changes result from IDC

**Technical Review (Internal):**
- Senior mechanical engineer or discipline lead reviews datasheets for:
  - Technical accuracy (correct valve types, materials, sizes)
  - Consistency with calculations (DEL-16.03) and specifications (DEL-16.02)
  - Compliance with codes and standards
  - Completeness (all fields populated or marked TBD)
  - Clarity and presentation quality

**Source:** Typical IDC process for multi-discipline projects; specific procedures TBD per project quality plan

### Step 4: Vendor Data Incorporation (Post-Procurement)

**Action:** After valve procurement, incorporate vendor-supplied data into datasheets and update to As-Built status.

**Vendor Data Submittal Review:**

After valve procurement, vendor submits the following data (see also Specification.md — Verification section, Vendor Data Cross-Check):

**Control Valves:**
- Certified Cv tables (flow coefficient vs. travel)
- Outline dimensional drawings
- Actuator sizing data (actual output torque/thrust, stroking time, air consumption)
- Positioner specifications (model, communication protocol, calibration range)
- Material certificates (MTRs for body, trim, bolting)
- Factory acceptance test (FAT) report (if FAT performed)
- O&M manual

**Isolation Valves:**
- Outline dimensional drawings
- Actuator data (if automated: output torque, stroking time)
- Test certificates (pressure test per API 598 or ISO 5208; seat leakage test)
- Material certificates (MTRs)

**Relief Valves:**
- ASME capacity certification (stamped capacity at set pressure)
- Set pressure test certificate (CDTP, test date, test medium, as-found/as-left set pressure)
- Outline dimensional drawings
- Material certificates (MTRs for body, spring, trim)
- ASME National Board Number (stamped on valve nameplate)
- Seat tightness test certificate (API 527 if required)

**Vendor Data Review Process:**

1. **Receive Vendor Submittal:** Vendor submits data package per procurement specification requirements
2. **Assign Submittal Number:** Track vendor submittal with unique number (e.g., "SUB-PKG16-001") — **TBD** per project submittal tracking system
3. **Distribute for Review:** Engineering team reviews vendor data for compliance with datasheet requirements
4. **Check Compliance:**
   - **Control Valves:** Verify vendor Cv ≥ required Cv; verify materials per datasheet; verify leakage class per datasheet
   - **Relief Valves:** Verify ASME stamped capacity ≥ required capacity; verify set pressure and tolerance per datasheet; verify orifice designation
   - **Actuators:** Verify output torque/thrust ≥ required × safety factor; verify stroking time meets requirements; verify fail-safe capability
5. **Identify Discrepancies:** Note any deviations from datasheet requirements
6. **Resolve Discrepancies:**
   - **Minor Deviations (<10%, non-safety-critical):** Accept with engineering justification; document in vendor data review comments
   - **Major Deviations (>10%, safety-critical, non-compliance):** Reject and request vendor resubmittal or design revision
7. **Approve Vendor Submittal:** Mark submittal as "Approved," "Approved as Noted," or "Rejected" per project submittal procedures — **TBD**

**Datasheet Update with Vendor Data:**

After vendor submittal approval, update datasheets with actual vendor data:

1. **Open Datasheet (Current Revision):** Retrieve datasheet from document management system
2. **Update Vendor Data Section:**
   - Manufacturer name and model number
   - Serial number (if assigned at this stage; otherwise TBD until delivery)
   - Vendor-certified performance data (Cv, relief capacity, actuator output)
   - Test results (FAT results, set pressure test results)
   - Material certificate numbers (MTR reference numbers)
   - O&M manual reference (document number)
3. **Verify Consistency:** Ensure vendor data consistent with original datasheet requirements; flag any approved deviations
4. **Add Revision Note:** "Revision 1 (or B): Incorporated vendor [Vendor Name] data per submittal [Submittal Number], dated [Date]"
5. **Update Revision Status:** Increment revision (Rev 0 → Rev 1, or Rev A → Rev B) — **TBD** per project revision convention
6. **Issue Updated Datasheet:** Issue via document management system with new revision

**As-Built Datasheet (Final):**

After valve installation and commissioning, create As-Built datasheet:
- Incorporate final serial numbers (from installed valves)
- Incorporate commissioning test results (as-found/as-left set pressure for relief valves; stroking time verification for control valves)
- Mark as "As-Built" or final revision (Rev 2 or Rev C, or "IFC" = Issued for Construction)
- Transfer As-Built datasheets to Owner for O&M use

**Source:** Typical vendor data incorporation process for EPC projects; specific procedures TBD per project execution plan

### Step 5: Approval and Issue

**Action:** Obtain discipline lead approval and issue datasheets per project procedures.

**Approval Process:**

**Approval Signatories:**
- **Originator:** Design engineer who prepared the datasheets (signed at completion of preparation and self-check)
- **Reviewer:** Senior engineer or discipline lead who reviewed datasheets (signed after technical review and IDC complete)
- **Approver:** Discipline lead (P.Eng.) authorized to approve datasheets (signs after review and approval)

**Approver Review:**
- Discipline lead reviews datasheets for technical adequacy and compliance with project standards
- Approver verifies IDC complete (Category A comments resolved)
- Approver verifies consistency with calculations (DEL-16.03) and specifications (DEL-16.02)
- Approver may request revisions before approval

**Datasheet Issue:**
- Assign datasheet number per project numbering system — **TBD**
  - **Option A:** Datasheet number = Valve tag number (e.g., datasheet for FV-1234 is "FV-1234 Data Sheet")
  - **Option B:** Sequential numbering (e.g., "DS-PKG16-001, DS-PKG16-002, ...")
- Assign revision code (Rev 0 or A for initial issue; increment per project convention) — **TBD**
- Update datasheet header/footer with approval signatures and issue date
- Issue datasheets via project document management system — **TBD**
- Update valve register with datasheet numbers and issue status

**Issue Purpose Codes (typical):**
- **IFD (Issued for Design):** Datasheet approved for internal design use
- **IFP (Issued for Procurement):** Datasheet issued to vendors for bidding (30%, 60%, or 90% design)
- **IFC (Issued for Construction):** Final datasheet approved for construction (with vendor data incorporated)
- **IFR (Issued for Review):** Datasheet issued to Employer or Authority for review/comment (if required)

**Source:** Typical datasheet approval and issue process; specific codes and procedures TBD per project document control procedures

## Verification

**Verification activities for Data Sheet deliverables:**

### Designer Self-Check (Step 2)
- Originator reviews datasheet for completeness (all fields populated or marked TBD)
- Verify data accuracy against source documents (calculations, P&IDs, specifications)
- Verify units consistency and clarity
- Verify internal consistency (valve size matches line size, pressure rating adequate, etc.)
- Sign-off: Originator initials datasheet "Prepared By" field — **TBD**

### Calculation Cross-Check (Step 2 or 3)
- Verify sizing data matches DEL-16.03 valve design calculations:
  - Control valves: Required Cv, selected valve size, trim type, actuator size match calculation results
  - Relief valves: Set pressure, orifice designation, relief capacity match calculation results
- Acceptance criterion: Datasheet sizing data shall match calculations within rounding tolerance (±2%)

### Specification Compliance Check (Step 2 or 3)
- Verify datasheet specifications comply with DEL-16.02 valve technical specification:
  - Materials (body, trim, gaskets, bolting) comply with specification
  - Leakage class complies with specification
  - Testing requirements comply with specification
  - Codes and standards correctly cited

### P&ID Cross-Check (Step 2 or 3)
- Verify datasheets match P&IDs:
  - Tag numbers match P&ID tag numbers
  - Service descriptions consistent with P&ID
  - Line numbers match P&ID
  - Fail-safe modes (FC, FO, FL) match P&ID notation
- Verify all valves on P&ID have datasheets; all datasheets reference P&ID location
- Acceptance criterion: 100% match; discrepancies resolved by updating P&ID or datasheet

### Interdisciplinary Check (Step 3)
- Multi-discipline coordination to verify interface assumptions and data correctness
- IDC Category A comments must be resolved before datasheet approval
- Sign-off: IDC complete when comments resolved and responses documented

### Vendor Data Cross-Check (Step 4, Post-Procurement)
- Verify vendor-supplied data matches datasheet requirements:
  - Vendor Cv ≥ required Cv (control valves)
  - Vendor ASME stamped capacity ≥ required capacity (relief valves)
  - Vendor actuator output ≥ required × safety factor
  - Vendor materials comply with datasheet specifications
- Acceptance criterion: Vendor data complies; discrepancies <10% acceptable with justification; discrepancies >10% require revision or vendor resubmittal

### Approval (Step 5)
- Discipline lead (P.Eng.) reviews and approves datasheets for issue
- Sign-off: Approver signs and stamps datasheet "Approved By" field with P.Eng. seal — **TBD**

**Acceptance Criteria:**
- All verification steps completed per project quality procedures
- IDC Category A comments resolved; Category B/C comments responded to
- Datasheet consistent with calculations, specifications, and P&IDs
- All required fields populated (or TBD items flagged and tracked)
- Originator, reviewer, and approver signatures obtained per project authority matrix — **TBD**

**Source:** Verification activities typical for valve datasheets; specific sign-off requirements TBD per project quality procedures

## Records

**Documentation outputs:**

### Primary Deliverables
- **Control Valve Data Sheets:** Individual datasheets for each control valve; multiple datasheets anticipated
- **Isolation Valve Data Sheets:** Individual datasheets for each automated isolation valve; manual valves may have simplified datasheets or grouped datasheets
- **Relief Valve Data Sheets:** Individual datasheets for each relief valve; multiple datasheets anticipated
- **Specialty Item Data Sheets:** Datasheets for check valves, strainers, specialty items (as required)

**Format:** **TBD** — **ASSUMPTION:** PDF datasheets with supporting native files (Excel, Word templates)

### Supporting Records
- **Valve Register/Index:** List of all valves with tag numbers, types, sizes, datasheet numbers, and revision status
- **Datasheet Summary:** Consolidated summary of key valve data (sizes, types, quantities by system)
- **IDC Comment/Response Log:** Record of interdisciplinary comments and resolutions
- **Vendor Submittal Register:** List of vendor submittals with datasheet cross-references (post-procurement)
- **Vendor Data Comparison:** Post-procurement comparison of vendor data vs. datasheet requirements

**Record Management:**

**During Development (WORKING Status):**
- Working datasheets maintained in `1_Working/` folder in deliverable directory
- Native datasheet files (Excel, Word, database) and PDF drafts
- **Source:** Folder structure per README.md Section "What lives where"

**During Review (CHECKING Status):**
- Datasheets placed in `2_Checking/To/` folder for IDC and technical review
- Track IDC comments and resolutions
- **Source:** Recommended convention per README.md Section 6 (Review and issue)

**Upon Issue (ISSUED Status):**
- Issued datasheets placed in `3_Issued/` folder
- Include PDF and native files
- Archive superseded revisions (if datasheet revised after vendor data incorporation)
- Update valve register
- **Source:** Recommended convention per README.md Section 6 (Review and issue)

**Retention Requirements:**
- Retention period: **TBD** — **ASSUMPTION:** Facility life + 10 years typical for equipment datasheets (operational record; supports O&M)
- Archival format: **TBD** — **ASSUMPTION:** PDF/A for long-term preservation; retain native files for future updates
- As-Built datasheets transferred to Owner/Operator for O&M reference

**Electronic Document Management:**
- **ASSUMPTION:** Electronic records managed in project document management system (e.g., Aconex, ProjectWise, SharePoint, or equivalent)
- Document control procedures: **TBD** — Per project document control plan
- Access permissions: **TBD** — Per project data security requirements; O&M datasheets accessible to Owner/Operator

**Source:** Record management practices typical for EPC projects; specific requirements TBD per project procedures

## Revision History and Configuration Management

**Datasheet Revisions:**
- Initial issue (for procurement): Rev 0 (or Rev A) — **TBD** per project convention
- Vendor data incorporation: Rev 1 (or Rev B) — **TBD**
- As-Built (final): Rev 2 (or Rev C), or "IFC" (Issued for Construction) designation — **TBD**
- Revision description noted in datasheet revision table or header

**Reasons for Datasheet Revision:**
- Vendor data incorporation (post-procurement)
- P&ID changes (tag number change, service change, fail-safe mode change)
- Calculation update (revised Cv, set pressure, actuator size)
- Specification update (material change, leakage class change)
- Design change (valve type change, size change)
- As-Built updates (final serial numbers, commissioning test results)

**Configuration Control:**
- Datasheet supersedes previous revision upon issue
- Prior revision archived but retained for traceability
- Valve register maintains current and superseded revision status
- No working from superseded datasheets (document management system access control) — **TBD**

**Coordination with Other Deliverables:**
- Datasheet changes coordinated with related deliverables:
  - P&ID updates if tag number or fail-safe mode changes
  - Calculation updates if sizing data changes
  - Specification updates if materials or requirements change
  - Drawing updates (DEL-16.01) if valve size or type changes

**Source:** Configuration management typical for valve datasheets; specific procedures TBD per project document control plan
