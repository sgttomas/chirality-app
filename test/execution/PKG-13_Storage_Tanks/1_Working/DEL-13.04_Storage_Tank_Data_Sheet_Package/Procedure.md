# Procedure: DEL-13.04 Storage Tank Data Sheet Package

## Purpose

This procedure defines the process for producing and managing **Storage Tank Data Sheet Package** within **PKG-13 Storage Tanks**.

**Deliverable Description:** Defines and substantiates storage tank in accordance with ER requirements.

**Source:** _CONTEXT.md, Decomposition document DEL-13.04

### Scope of This Procedure

This procedure describes the workflow for:
1. Producing tank data sheets (3) from design documents
2. Producing agitator data sheets (3) integrating vendor data
3. Producing overflow protection data sheet(s)
4. Verifying data sheet content against source documents and interfacing disciplines
5. Managing data sheet revisions and issuance

**Deliverable type:** Data Sheet
**Responsible party:** D&B Contractor

---

## Prerequisites

### Dependencies

**Dependency tracking:** See `_DEPENDENCIES.md` — **NOT_TRACKED**: Dependencies are coordinated externally by humans (see `execution/_Coordination/_COORDINATION.md`)

**Upstream deliverables required:**

| Deliverable | Content Needed | Status |
|-------------|----------------|--------|
| DEL-13.01: Storage Tank Design Drawing Set | Tank GAs, nozzle schedules, dimensions, arrangement | **TBD** — Verify availability |
| DEL-13.02: Storage Tank Technical Specification | Material specifications, performance requirements, standards | **TBD** — Verify availability |
| DEL-13.03: Storage Tank Design Calculations | Capacity, sizing, design basis, foundation loads | **TBD** — Verify availability |
| PKG-14 P&IDs | Nozzle service descriptions, line numbers, piping interfaces | **TBD** — Verify availability |

**Source:** Typical data sheet input requirements

### Reference Materials

**Required references:**
- See `_REFERENCES.md` for applicable reference documents
- See `0_References/` in package directory for reference materials
- Employer's Requirements (Volume 2 Part 2) — **Location TBD**
- Project data sheet templates — **TBD** — Obtain from project engineering standards
- Project tagging system — **TBD** — Obtain from project document control procedures

**Source:** Typical data sheet production references

### Personnel Requirements

**Required personnel:**
- **Lead Mechanical Engineer:** Reviews design documents, populates data sheets, coordinates vendor data
- **Checker:** Performs independent check of data sheet content
- **Piping Engineer:** Reviews nozzle data and piping interfaces
- **Instrumentation Engineer:** Reviews instrumentation connections and tag numbers
- **Electrical Engineer:** Reviews agitator motor data and electrical supply
- **Control Systems Engineer:** Reviews agitator control interface and overflow protection logic

**TBD** — Specific personnel qualifications per project quality procedures

**Source:** Typical interdisciplinary data sheet review team

### Tools and Templates

**Required tools:**
- Data sheet template (Excel or database form) — **TBD** — Obtain from project engineering standards
- Project document management system access
- Design document access (drawings, calculations, specifications)

**Source:** Typical data sheet production tools

---

## Steps

### Step 1: Prepare Tank Data Sheets (3)

**Objective:** Produce preliminary tank data sheets from design documents.

**Actions:**

1.1. Obtain tank data sheet template from project engineering standards

1.2. For each tank (Tank 1, Tank 2, Tank 3):

1.2.1. **Assign tag number:**
- Obtain tag number from project tagging system (e.g., TK-101, TK-102, TK-103 — **TBD**)
- Enter tag number in data sheet identification section

1.2.2. **Populate identification section:**
- Service: CSD canola oil storage (from Decomposition Section 1.1)
- Design standard: API 650 (from DEL-13.02)
- Location: Fraser Surrey Terminal, Surrey, BC (from Decomposition Section 1)

1.2.3. **Populate capacity section:**
- Capacity (mass): 15,000 MT (from Decomposition Section 1.1)
- Capacity (volume): **TBD** — Calculate from mass and product density (requires product specification or ER extraction)
- Product density: **TBD** — From product specification or ER

1.2.4. **Populate dimensions section:**
- Tank diameter: From design calculations (DEL-13.03)
- Tank height: From design calculations (DEL-13.03)
- Shell courses: From design drawings (DEL-13.01)
- Shell plate thickness: From design drawings (DEL-13.01) and calculations (DEL-13.03)

1.2.5. **Populate materials section:**
- Shell material: From technical specification (DEL-13.02)
- Bottom material: From technical specification (DEL-13.02)
- Roof material: From technical specification (DEL-13.02)
- Coating systems (internal/external): From PKG-26 coordination

1.2.6. **Populate design conditions section:**
- Design pressure: Atmospheric (API 650 tank)
- Design temperature: From ER or specification (DEL-13.02) — **TBD**
- Seismic design: From design calculations (DEL-13.03) and NBC 2020
- Wind/snow loads: From design calculations (DEL-13.03) and NBC 2020

1.2.7. **Populate nozzle summary section:**
- Extract nozzle data from nozzle schedule (DEL-13.01)
- For each nozzle: Size, rating, service, line number (from P&ID coordination)
- Include: Inlet, outlet, overflow, vent, drain, water draw-off, instrumentation, agitator, Phase 2 connections

1.2.8. **Populate internals section:**
- Agitator: Reference agitator tag number (e.g., AGI-101, AGI-102, AGI-103)
- Overflow protection: Reference overflow protection system
- Water draw-off: From design (DEL-13.01)

1.2.9. **Populate foundation section:**
- Foundation type: From design calculations (DEL-13.03) and PKG-05 coordination
- Foundation loads: From design calculations (DEL-13.03)

1.3. Mark any missing data as **TBD** with explanation

1.4. Save preliminary tank data sheets in `1_Working/DEL-13.04/` folder

**Verification:** Self-check for completeness and internal consistency

**Source:** Typical tank data sheet production workflow

---

### Step 2: Prepare Agitator Data Sheets (3)

**Objective:** Produce preliminary agitator data sheets from design documents, to be updated with vendor data.

**Actions:**

2.1. Obtain agitator data sheet template from project engineering standards

2.2. For each agitator (Agitator 1, Agitator 2, Agitator 3):

2.2.1. **Assign tag number:**
- Obtain tag number from project tagging system (e.g., AGI-101, AGI-102, AGI-103 — **TBD**)
- Enter tag number in data sheet identification section

2.2.2. **Populate identification section:**
- Service: CSD canola oil mixing
- Tank tag: Cross-reference to tank tag number (e.g., AGI-101 serves TK-101)

2.2.3. **Populate design basis section (D&B Contractor specified):**
- Agitator type: From specification (DEL-13.02) — **TBD**
- Mixing intensity: From process requirements — **TBD**
- Turnover time: From process requirements — **TBD**
- Tank dimensions: From tank data sheet
- Product properties: From product specification — **TBD**

2.2.4. **Populate vendor data section (to be provided by vendor):**
- Mark fields as **TBD — Vendor to provide:**
  - Manufacturer, model, serial number
  - Impeller type, diameter, speed
  - Motor power, speed, voltage, enclosure
  - Shaft length, diameter, material
  - Seal type
  - Weight, dimensions
  - Mounting requirements

2.2.5. **Populate electrical interface section:**
- Electrical supply: From PKG-17 coordination (voltage, phase, frequency) — **TBD**
- Motor control: From PKG-19 coordination (starter type, control interface) — **TBD**

2.3. Mark vendor data fields as **TBD — Vendor to provide**

2.4. Save preliminary agitator data sheets in `1_Working/DEL-13.04/` folder

**Verification:** Self-check for completeness of design basis sections

**Source:** Typical agitator data sheet production workflow

---

### Step 3: Prepare Overflow Protection Data Sheet(s)

**Objective:** Produce overflow protection data sheet(s).

**Actions:**

3.1. Determine system configuration:
- **Option A:** Single overflow protection system serving all three tanks
- **Option B:** Individual overflow protection system per tank (3 systems)
- **TBD** — Configuration requires process design and control logic review

3.2. Obtain overflow protection data sheet template (or create based on project standards)

3.3. **Populate identification section:**
- System tag: **TBD** — From project tagging system
- Service: Tank overfill protection

3.4. **Populate system configuration section:**
- System type: From specification (DEL-13.02) and process design — **TBD**
  - Options: High-level switch, overflow pipe, level transmitter with alarm, etc.
- Set point(s): From design calculations (DEL-13.03) and safety analysis — **TBD**
- Alarm configuration: From PKG-19 coordination (high-level alarm, high-high level alarm) — **TBD**

3.5. **Populate instrumentation section:**
- Instrumentation tag numbers: From PKG-20 coordination — **TBD**
- Instrument type: From PKG-20 coordination — **TBD**
- Set points and ranges: From design — **TBD**

3.6. **Populate interlock logic section:**
- Interlock actions: From PKG-19 coordination (e.g., stop railcar unloading pump on high-high level) — **TBD**
- Alarm actions: From PKG-19 coordination — **TBD**

3.7. **Populate overflow discharge section:**
- Overflow capacity: From design calculations — **TBD**
- Discharge location: From design and environmental coordination — **TBD**

3.8. Save overflow protection data sheet(s) in `1_Working/DEL-13.04/` folder

**Verification:** Self-check for completeness and coordination with control logic

**Source:** Typical overflow protection documentation workflow

---

### Step 4: Verify Data Sheets Against Source Documents

**Objective:** Verify data sheet content against design documents for accuracy and consistency.

**Actions:**

4.1. **Cross-check tank data sheets:**

4.1.1. Verify capacity data against design calculations (DEL-13.03)

4.1.2. Verify dimensions against design drawings (DEL-13.01) and calculations (DEL-13.03)

4.1.3. Verify materials against specification (DEL-13.02)

4.1.4. Verify nozzle summary against nozzle schedule (DEL-13.01)

4.1.5. Document discrepancies in discrepancy log

4.1.6. Resolve discrepancies through design document corrections or data sheet corrections

4.2. **Cross-check agitator data sheets:**

4.2.1. Verify design basis data against specification (DEL-13.02) and process requirements

4.2.2. Verify tank cross-references against tank data sheets

4.2.3. Verify electrical interface data against PKG-17 coordination

4.2.4. Document discrepancies and resolve

4.3. **Cross-check overflow protection data sheet(s):**

4.3.1. Verify set points against design calculations and safety analysis

4.3.2. Verify instrumentation tag numbers against PKG-20 coordination

4.3.3. Verify interlock logic against PKG-19 coordination

4.3.4. Document discrepancies and resolve

4.4. **Verify units and nomenclature:**

4.4.1. Check all units are consistent with project unit system

4.4.2. Check all nomenclature is consistent with project conventions

4.4.3. Correct any inconsistencies

**Verification:** Independent checker verifies cross-checks are complete and discrepancies are resolved

**Source:** Typical data sheet verification process

---

### Step 5: Conduct Interdisciplinary Check

**Objective:** Verify data sheet interfaces with other disciplines.

**Actions:**

5.1. **Piping discipline review:**
- Review nozzle data (size, rating, service, line number)
- Verify consistency with P&IDs and piping design (PKG-14)
- Piping engineer sign-off on data sheets

5.2. **Instrumentation discipline review:**
- Review instrumentation connections and tag numbers
- Verify consistency with instrument data sheets (PKG-20)
- Instrumentation engineer sign-off on data sheets

5.3. **Electrical discipline review:**
- Review agitator motor data and electrical supply
- Verify consistency with electrical design (PKG-17)
- Electrical engineer sign-off on data sheets

5.4. **Control systems discipline review:**
- Review agitator control interface and overflow protection logic
- Verify consistency with control system design (PKG-19)
- Control systems engineer sign-off on data sheets

5.5. **Document interdisciplinary check results:**
- Record comments and action items in interdisciplinary check log
- Resolve comments through data sheet revisions or design clarifications

**Verification:** All required disciplines have signed off on data sheets

**Source:** Typical interdisciplinary check process

---

### Step 6: Integrate Vendor Data (Agitator Data Sheets)

**Objective:** Update agitator data sheets with vendor-supplied information.

**Actions:**

6.1. **Obtain vendor data:**
- Request vendor data from agitator manufacturer per specification (DEL-13.02) requirements
- **TBD** — Vendor data submission timing and format per procurement process

6.2. **Validate vendor data:**

6.2.1. Verify vendor data complies with specification (DEL-13.02) requirements:
- Mixing performance (intensity, turnover time)
- Motor power minimum
- Material compatibility
- Mounting configuration

6.2.2. Identify discrepancies between vendor data and specification

6.2.3. Resolve discrepancies through engineering review and/or vendor clarification

6.3. **Integrate vendor data into agitator data sheets:**
- Populate vendor data fields (manufacturer, model, impeller data, motor data, etc.)
- Update **TBD — Vendor to provide** fields with actual vendor values
- Retain design basis fields (specified by D&B Contractor)

6.4. **Update data sheet revision:**
- Increment revision number
- Update revision history (e.g., "Rev 1: Vendor data integrated")

**Verification:** Checker verifies vendor data is complete and compliant with specification

**Source:** Typical vendor data integration workflow

---

### Step 7: Issue Data Sheets for Review/Approval

**Objective:** Issue data sheets for internal review and client approval.

**Actions:**

7.1. **Prepare issuance package:**
- Compile all data sheets (3 tank, 3 agitator, overflow protection)
- Include cover letter/transmittal summarizing content
- Include discrepancy log (if applicable) and resolution status

7.2. **Internal review:**
- Discipline lead reviews data sheets
- Checker performs final check
- Approver signs off on data sheets

7.3. **File data sheets in 2_Checking/To/ folder:**
- Move data sheets from `1_Working/` to `2_Checking/To/` for client review
- **TBD** — Client review process and approval requirements per ER

7.4. **Issue for construction (after approval):**
- Move approved data sheets to `3_Issued/` folder
- Notify downstream users (fabrication, procurement, installation)
- **TBD** — Issuance notification process

**Verification:** All required approvals obtained before issuance for construction

**Source:** Typical document issuance workflow

---

### Step 8: Manage Revisions

**Objective:** Manage data sheet revisions throughout project lifecycle.

**Actions:**

8.1. **Track revision triggers:**
- Design changes (drawings, calculations, specifications updated)
- Vendor data updates
- As-built changes
- Client comments requiring revision

8.2. **Revise data sheets:**
- Update affected data sheets
- Increment revision number
- Update revision history
- Highlight changes (if required by project standards)

8.3. **Re-verify revised data sheets:**
- Repeat Steps 4-5 (cross-check and interdisciplinary check) for revised content

8.4. **Re-issue revised data sheets:**
- Repeat Step 7 (issuance) for revised data sheets
- Notify downstream users of revisions

8.5. **Archive superseded revisions:**
- Move superseded revisions to archive folder
- Retain per project document retention policy

**Verification:** Revision history is accurate and complete

**Source:** Typical document revision management

---

## Verification

### Verification Activities

**Self-Check (Step 4):**
- Data sheet content verified against source documents (drawings, calculations, specifications)
- Units and nomenclature verified for consistency
- Internal consistency verified (e.g., nozzle summary matches individual entries)

**Independent Check (Step 7):**
- Qualified checker performs independent review
- Checker verifies accuracy, completeness, and compliance with standards

**Interdisciplinary Check (Step 5):**
- Piping, instrumentation, electrical, control systems disciplines review interfaces
- Discrepancies identified and resolved

**Vendor Data Verification (Step 6):**
- Vendor data verified for compliance with specification (DEL-13.02)
- Discrepancies identified and resolved

**Source:** Typical data sheet verification methods (see Specification.md V-01 through V-05)

### Sign-off Requirements

**Originator sign-off:**
- Lead Mechanical Engineer completes data sheets and certifies accuracy

**Checker sign-off:**
- Independent checker verifies data sheets and certifies review complete

**Interdisciplinary sign-off:**
- Piping, instrumentation, electrical, control systems engineers sign off on interfaces

**Approver sign-off:**
- Discipline lead approves data sheets for issuance

**Client approval:**
- **TBD** — Client review and approval requirements per ER

**Source:** Typical data sheet approval workflow

---

## Records

### Documentation Outputs

**Primary outputs:**
- Tank data sheets (3) — Filed in `3_Issued/` after approval
- Agitator data sheets (3) — Filed in `3_Issued/` after approval
- Overflow protection data sheet(s) — Filed in `3_Issued/` after approval

**Supporting records:**
- Discrepancy log (cross-check results)
- Interdisciplinary check log (IDC comments and resolutions)
- Vendor data validation records
- Revision history log

**Source:** _CONTEXT.md (Anticipated Artifacts); Typical data sheet records

### Record Management

**Filing locations:**
- `1_Working/DEL-13.04/` — Work-in-progress data sheets
- `2_Checking/To/` — Data sheets issued for review (awaiting approval)
- `2_Checking/From/` — Data sheets returned from review with comments
- `3_Issued/` — Approved data sheets issued for construction
- `Archive/` — Superseded data sheet revisions

**Retention requirements:**
- **TBD** — Retention requirements per project procedures and ER
- Final as-built data sheets retained for facility lifecycle

**Electronic records:**
- All data sheets managed in project document management system
- Revision history and approval records maintained electronically

**Source:** ASSUMPTION based on typical project document control procedures

---

## Cross-Document References

**For detailed requirements:** See `Specification.md`
- FR-01, FR-02, FR-03 → Implemented in Steps 1, 2, 3
- PR-01, PR-02, PR-03, PR-04 → Verified in Steps 4, 5, 6
- DR-01 through DR-05 → Managed in Steps 7, 8
- IR-01 through IR-07 → Verified in Step 5

**For principles and guidance:** See `Guidance.md`
- DP-01: Equipment Documentation Philosophy → Applied in Steps 1, 2, 3
- DP-02: Vendor Data Integration → Implemented in Step 6
- DP-03: Cross-Discipline Coordination → Implemented in Step 5
- DP-04: Standardization → Applied in template selection (Steps 1, 2, 3)
- DP-05: Traceability → Managed in Step 8
- Considerations and Trade-offs → Inform workflow decisions

**For entity attributes:** See `Datasheet.md`
- Tank, Agitator, Overflow Protection attributes → Populated in Steps 1, 2, 3

---

**Document Status:** Pass 3 (Final) — Enrichment complete. Procedure steps defined with verification points and cross-document references. All TBDs marked. ASSUMPTIONs labeled. Ready for WORKING_ITEMS refinement.

**Last Updated:** 2026-01-28
