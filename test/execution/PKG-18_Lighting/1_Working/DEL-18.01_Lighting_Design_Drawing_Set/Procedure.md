# Procedure: DEL-18.01 Lighting Design Drawing Set

## Purpose

This procedure defines the process for producing and managing the **Lighting Design Drawing Set** within **PKG-18 Lighting** for the Canola Oil Transload Facility project.

**Deliverable Purpose:** Defines the design arrangement and details for lighting per ER requirements. *(Source: _CONTEXT.md, Decomposition DEL-18.01 description)*

**Deliverable Type:** Drawing
**Responsible Party:** D&B Contractor
**Discipline:** Electrical

**Scope of This Procedure:**
This procedure covers both:
1. **Production of the deliverable artifact** — How to develop the lighting design drawing set
2. **Use of the deliverable artifact** — How the drawings are used during construction, commissioning, and operations (as applicable)

## Prerequisites

### Dependencies

**Dependency Tracking Mode:** NOT_TRACKED
Dependencies are coordinated externally by humans per `_DEPENDENCIES.md` and `execution/_Coordination/_COORDINATION.md`.

**Typical Upstream Dependencies (to be confirmed by project coordination):**
- **Site survey and base drawings (PKG-01)** — Coordinate system, site topography, existing utilities — **TBD**
- **Hazardous area classification drawings (PKG-17 or PKG-24)** — Area classification for fixture selection — **TBD**
- **Architectural drawings (PKG-21, PKG-22)** — Building layouts, ceiling plans for interior lighting coordination — **TBD**
- **Electrical power distribution design (PKG-17)** — Panel locations, available capacity for lighting circuits — **TBD**
- **Control system architecture (PKG-19)** — Lighting control interfaces and integration requirements — **TBD**
- **Employer's Requirements** — Lighting performance requirements, standards, constraints — **TBD** *(Location TBD)*

**Downstream Deliverables (typical users of this drawing set):**
- **Lighting Technical Specification (DEL-18.02)** — Specification references drawings for layout and quantities
- **Lighting Design Calculations (DEL-18.03)** — Calculations validate layout shown on drawings
- **Lighting Data Sheet Package (DEL-18.04)** — Equipment data sheets for fixtures shown on drawings
- **Construction procurement and installation** — Drawings used by contractors for installation
- **Lighting Installation & Test Records (DEL-18.05)** — Testing and commissioning references drawings

### Reference Materials

**Required Inputs:**
- `_REFERENCES.md` — Applicable reference documents (currently minimal; to be populated)
- Package `0_References/` folder — Project reference materials
- **Employer's Requirements (Vol 2 Part 1, Part 2, Part 3)** — **TBD** *(Location TBD in 0_References/)*
- **Site survey drawings and CAD files** — **TBD**
- **Architectural and civil base drawings** — **TBD**
- **Electrical power distribution one-line and panel schedules** — **TBD**
- **Hazardous area classification drawings** — **TBD**

**Applicable Codes and Standards:**
- CSA C22.1 (Canadian Electrical Code) — **ASSUMPTION**
- CSA C22.2 — Electrical equipment standards — **ASSUMPTION**
- NBCC 2020 (National Building Code of Canada) — **ASSUMPTION**
- IESNA Lighting Handbook — **TBD** *(Edition and location TBD)*
- NFPA 101 (Life Safety Code) — **ASSUMPTION**
- CSA Z32 (Electrical and Electronics Diagrams) — **TBD** *(If applicable)*
- Project CAD standards and drawing templates — **TBD** *(Location TBD)*

### Personnel Requirements

**Design Team:**
- **Lead Electrical Engineer (Lighting)** — P.Eng. licensed in British Columbia — **TBD** *(Qualification requirements per project)*
- **Electrical Designer/Drafter** — Proficient in CAD software per project standards — **TBD**
- **Photometric Analysis Specialist** — Familiar with lighting calculation software (AGi32, DIALux, etc.) — **TBD**

**Review Team:**
- **Independent Checker** — P.Eng. not involved in original design — **TBD**
- **Interdisciplinary Coordinators** — Representatives from architectural, civil, electrical power, controls disciplines — **TBD**

**Approval Authority:**
- **Electrical Discipline Lead** — **TBD** *(Per project organization)*
- **Project Engineering Manager** — **TBD** *(Per approval matrix)*

**Competency Requirements:**
- Personnel shall be competent per project quality procedures — **ASSUMPTION**
- Continuing education and code update training for design team — **ASSUMPTION** *(Good practice)*

## Steps

### Step 1: Design Basis and Requirements Review

**Objective:** Establish design criteria and constraints before starting layout.

**Activities:**
1. Review Employer's Requirements for lighting performance requirements, illuminance levels, fixture preferences, and constraints — **TBD** *(ER location TBD)*
2. Review applicable codes and standards (CSA C22.1, IESNA, NFPA 101, NBCC) — **ASSUMPTION**
3. Identify required lighting zones:
   - Exterior process areas
   - Exterior roadways and parking
   - Perimeter security lighting
   - Interior process/warehouse areas
   - Interior control rooms and offices
   - Emergency egress paths
4. Obtain hazardous area classification drawings and identify areas requiring explosion-proof or special fixtures — **TBD**
5. Obtain architectural and civil base drawings in CAD format — **TBD**
6. Coordinate with electrical power distribution team (PKG-17) to identify available panel capacity and locations — **TBD**
7. Coordinate with controls team (PKG-19) to define lighting control requirements and interfaces — **TBD**

**Deliverable from Step 1:**
- Design basis memorandum or criteria document summarizing requirements — **TBD** *(Format and approval TBD)*

### Step 2: Preliminary Fixture Selection and Layout

**Objective:** Develop initial lighting layout for photometric analysis.

**Activities:**
1. Select preliminary fixture types based on:
   - Application (area lighting, high-bay, wall pack, etc.)
   - Environment (marine, outdoor, indoor, hazardous area)
   - Performance (lumen output, efficacy, color temperature)
   - LED technology per PKG-18 scope *(Source: Decomposition PKG-18 scope)*
2. Develop preliminary exterior lighting layout:
   - Locate poles on site plan considering:
     - Coverage area per photometric analysis
     - Avoidance of underground utilities and structures
     - Access for maintenance
     - Aesthetic and operational considerations
   - Assign mounting heights (typical 30-40 ft for area lighting) — **ASSUMPTION**
3. Develop preliminary interior lighting layout:
   - Locate fixtures on building floor plans and ceiling plans
   - Coordinate with architectural ceiling grid and HVAC/structure
   - Typical spacing for high-bay fixtures (20-30 ft) — **ASSUMPTION**
4. Develop preliminary emergency lighting layout:
   - Identify egress paths per architectural drawings and NFPA 101
   - Locate emergency fixtures at exits, corridors, stairwells — **ASSUMPTION**
5. Perform preliminary photometric calculations to verify coverage (see DEL-18.03 Lighting Design Calculations)

**Deliverable from Step 2:**
- Preliminary layout sketches or CAD files
- Preliminary fixture schedule — **TBD**

### Step 3: Photometric Analysis and Layout Refinement

**Objective:** Verify and optimize lighting layout to meet illuminance requirements.

**Activities:**
1. Perform detailed photometric calculations using lighting design software (AGi32, DIALux, or similar) — **TBD** *(Software to be confirmed)*
2. Input fixture photometric data (IES files from manufacturers) — **TBD**
3. Model site geometry, reflectances, and obstructions — **ASSUMPTION**
4. Calculate illuminance levels, uniformity ratios, and glare indices — **ASSUMPTION**
5. Compare results to required illuminance levels per ER and codes — **TBD**
6. Refine fixture locations, quantities, mounting heights, and aiming to optimize performance — **ASSUMPTION**
7. Iterate until illuminance requirements are met with acceptable uniformity — **ASSUMPTION**
8. Document calculations in DEL-18.03 Lighting Design Calculations — **ASSUMPTION**

**Deliverable from Step 3:**
- Photometric analysis report (DEL-18.03) — **ASSUMPTION**
- Refined lighting layout incorporating calculation results

### Step 4: CAD Drawing Production

**Objective:** Produce final lighting design drawings per project CAD standards.

**Activities:**
1. Set up CAD files using project drawing template and title block — **TBD** *(Template location TBD)*
2. Import or reference base drawings (site plan, building floor plans) — **TBD**
3. Draw lighting fixtures, poles, and equipment using project standard symbols — **TBD** *(Symbol library location TBD)*
4. Add fixture tags and reference designations (e.g., LP-01, EL-01) — **ASSUMPTION**
5. Show circuiting (dashed lines) connecting fixtures to panels with circuit numbers — **ASSUMPTION**
6. Add control devices (switches, sensors, contactors) and control zoning — **ASSUMPTION**
7. Create fixture schedules showing:
   - Tag number
   - Fixture type and manufacturer/model
   - Lamp type and wattage (LED module specifications)
   - Mounting height
   - Quantity
   - Circuit assignment
8. Add general notes, legends, and abbreviations — **ASSUMPTION**
9. Overlay photometric contours (optional) showing calculated illuminance levels — **ASSUMPTION**
10. Prepare details and typical sections as needed (pole foundation interface, mounting details, etc.) — **TBD**
11. Add dimensions, coordinates, and annotations per project drafting standards — **TBD**
12. Ensure compliance with project CAD layer standards, text styles, and file organization — **TBD** *(Standards location TBD)*

**Deliverable from Step 4:**
- CAD drawing files (native format) for:
  - Exterior lighting layout
  - Interior lighting layout
  - Emergency lighting layout
- PDF copies for review — **ASSUMPTION**

### Step 5: Self-Check

**Objective:** Designer/drafter reviews own work for completeness and accuracy.

**Activities:**
1. Review drawings against design basis and requirements (Step 1) — **ASSUMPTION**
2. Verify all fixtures are shown, tagged, and scheduled — **ASSUMPTION**
3. Check dimensions, coordinates, and spatial relationships — **ASSUMPTION**
4. Verify circuiting and panel assignments are complete and logical — **ASSUMPTION**
5. Check title block, revision block, drawing number, and sheet organization — **ASSUMPTION**
6. Verify compliance with CAD standards (layers, symbols, text styles) — **TBD**
7. Run CAD quality checks (purge, audit, check for errors) — **ASSUMPTION**
8. Document self-check on drawing or in review record — **TBD** *(Per project QA procedures)*

**Deliverable from Step 5:**
- Self-check sign-off or review record — **TBD**

### Step 6: Interdisciplinary Check (IDC)

**Objective:** Coordinate lighting drawings with other disciplines to identify and resolve conflicts.

**Activities:**
1. Distribute drawings to affected disciplines for review:
   - Architectural (PKG-21, PKG-22) — verify fixture locations compatible with ceilings, walls, building layout
   - Civil (PKG-01, PKG-02, PKG-03) — verify exterior pole locations clear of utilities, grading, paving
   - Structural (PKG-05, PKG-06, PKG-21) — verify mounting supports and pole foundations coordinated
   - Electrical Power (PKG-17) — verify circuits, panels, and feeders coordinated
   - Controls (PKG-19) — verify control interfaces and integration points
   - Fire Protection (PKG-23) — verify emergency lighting and clearances to sprinklers
2. Conduct coordination meeting or review session — **TBD** *(Per project coordination procedures)*
3. Resolve conflicts and incorporate comments — **ASSUMPTION**
4. Update drawings and issue revised version for re-check if significant changes made — **TBD**
5. Document IDC completion and comment resolution — **TBD** *(Per project QA procedures)*

**Deliverable from Step 6:**
- IDC review record with comments and resolutions — **TBD**
- Updated drawings incorporating IDC comments

### Step 7: Independent Check (Peer Review)

**Objective:** Independent peer review by qualified electrical engineer to verify design correctness and compliance.

**Activities:**
1. Assign independent checker (P.Eng. not involved in original design) — **TBD** *(Per project organization)*
2. Checker reviews drawings for:
   - Compliance with codes and standards (CSA C22.1, NBCC, IESNA, NFPA 101)
   - Compliance with Employer's Requirements — **TBD**
   - Design adequacy and constructability
   - Calculation support (DEL-18.03) matches layout — **ASSUMPTION**
   - Coordination with other deliverables (DEL-18.02, DEL-18.04)
3. Checker documents findings on review form or markup — **TBD** *(Form location TBD)*
4. Designer addresses checker comments and updates drawings — **ASSUMPTION**
5. Checker verifies comment resolution and provides sign-off — **TBD**

**Deliverable from Step 7:**
- Independent check review record with sign-off — **TBD**
- Final drawings incorporating checker comments

### Step 8: Approval and Issue

**Objective:** Obtain approval from discipline lead and project engineering manager; issue drawings for use.

**Activities:**
1. Submit drawings to Electrical Discipline Lead for review and approval — **TBD** *(Per approval matrix)*
2. Submit drawings to Project Engineering Manager for final approval — **TBD** *(Per approval matrix)*
3. Incorporate any final comments from approvers — **ASSUMPTION**
4. Finalize drawing revision, date, and approval signatures in title block — **TBD** *(Per project procedures)*
5. Issue approved drawings:
   - Place approved PDF copies in `3_Issued/` folder
   - Upload to project document management system — **TBD** *(System and procedure TBD)*
   - Distribute to stakeholders per distribution matrix — **TBD**
6. Update deliverable status in `_STATUS.md` per project workflow (e.g., IN_PROGRESS → CHECKING → ISSUED) — **ASSUMPTION** *(Human decision)*

**Deliverable from Step 8:**
- Approved and issued lighting design drawing set:
  - Exterior lighting layout
  - Interior lighting layout
  - Emergency lighting layout
- Issue record or transmittal — **TBD**

### Step 9: Revision Control (for changes after initial issue)

**Objective:** Manage drawing revisions in a controlled manner.

**Activities:**
1. When changes are required, update CAD files with revisions — **ASSUMPTION**
2. Add revision clouds and revision descriptions per project standards — **ASSUMPTION** *(Standard practice)*
3. Update revision block in title block with revision letter/number, date, and description — **TBD**
4. Repeat Steps 5-8 (self-check, IDC, independent check, approval) for revised drawings — **ASSUMPTION**
5. Issue revised drawings with new revision designation — **ASSUMPTION**
6. Maintain superseded revisions in archive per project records retention policy — **TBD**

**Deliverable from Step 9:**
- Revised drawing set with revision tracking — **ASSUMPTION**

## Verification

**Verification Activities Throughout Procedure:**

**V-1: Design Review (Step 7 — Independent Check)**
- Independent peer review by P.Eng. verifies compliance with codes, standards, and ER requirements — **TBD**
- Review of supporting calculations (DEL-18.03) — **ASSUMPTION**

**V-2: Dimensional Verification (Step 5 — Self-Check)**
- Check dimensions, coordinates, fixture locations for accuracy and constructability — **ASSUMPTION**

**V-3: Interdisciplinary Check (Step 6 — IDC)**
- Coordination verification with architectural, civil, electrical power, controls, and fire protection disciplines — **ASSUMPTION**
- Clash detection if 3D models available — **TBD**

**V-4: CAD Standards Compliance Check (Step 5 — Self-Check)**
- Verify compliance with project CAD layer standards, symbology, text styles, file naming — **TBD** *(Standards location TBD)*
- Title block completeness and accuracy — **ASSUMPTION**

**V-5: Calculation Cross-Check (Step 3 and Step 7)**
- Photometric calculations (DEL-18.03) support layout and verify illuminance requirements met — **ASSUMPTION**
- Independent checker verifies calculation results match drawing layout — **ASSUMPTION**

**V-6: Specification and Data Sheet Coordination (Step 7)**
- Verify fixture types on drawings match technical specification (DEL-18.02) and data sheets (DEL-18.04) — **ASSUMPTION**

**Sign-Off Requirements:**
- **Originator sign-off** (Step 5) — Designer/drafter completes self-check — **TBD**
- **Checker sign-off** (Step 7) — Independent checker approves — **TBD**
- **Discipline Lead sign-off** (Step 8) — Electrical Discipline Lead approves — **TBD**
- **Project Engineering Manager sign-off** (Step 8) — Final approval per project approval matrix — **TBD**

**Acceptance Criteria:**
- All review comments closed or dispositioned — **ASSUMPTION**
- No open IDC issues — **ASSUMPTION**
- Calculations (DEL-18.03) support design — **ASSUMPTION**
- Compliance with codes and standards verified by independent checker — **TBD**
- Drawings approved by required authorities per approval matrix — **TBD**

## Records

**Documentation Outputs:**

**Primary Deliverable Artifacts:**
Per decomposition and _CONTEXT.md:
1. **Exterior lighting layout** — Site lighting plan in CAD and PDF formats
2. **Interior lighting layout** — Building lighting plans in CAD and PDF formats
3. **Emergency lighting layout** — Emergency egress lighting in CAD and PDF formats

**Supporting Documentation:**
- Lighting fixture schedule (typically on drawings or separate schedule)
- Pole schedule (for exterior poles)
- General notes, legends, and details
- Design basis memorandum (Step 1) — **TBD**
- Photometric analysis report (DEL-18.03) supporting layout — **ASSUMPTION**

**Quality Records:**
- Self-check record (Step 5) — **TBD**
- IDC review record (Step 6) — **TBD**
- Independent check review record (Step 7) — **TBD**
- Approval signatures and transmittals (Step 8) — **TBD**

**Record Management:**
- **Working files** stored in `1_Working/` folder during development
- **Review copies** placed in `2_Checking/To/` during review cycles
- **Approved/issued copies** placed in `3_Issued/` folder upon approval — **ASSUMPTION** *(Per project workflow)*
- **Electronic records** uploaded to project document management system — **TBD** *(System and location TBD)*
- **Retention requirements** per project records management plan — **TBD**
- **Superseded revisions** archived per retention policy — **TBD**

**Metadata and Attributes:**
- Drawing files tagged with metadata per project DMS requirements — **TBD**
- Drawing number, revision, issue date, discipline, package captured in file properties — **ASSUMPTION**

**Use of Records During Construction and Operations:**

**During Construction:**
- Lighting drawings used by construction contractors for:
  - Procurement of fixtures, poles, and equipment (coordinated with DEL-18.02 and DEL-18.04)
  - Installation of lighting systems per layout and details
  - Coordination with other trades (electrical, civil, architectural)
- As-built markups captured during installation and incorporated into final as-built drawings — **TBD** *(As-built procedure location TBD)*

**During Commissioning:**
- Lighting drawings referenced during commissioning and testing (DEL-18.05):
  - Verification of fixture installation per design
  - Illumination level testing and comparison to design calculations (DEL-18.03)
  - Control system functional testing

**During Operations:**
- Lighting drawings maintained as facility record drawings for:
  - Maintenance planning and spare parts identification
  - Troubleshooting and repairs
  - Future modifications and expansions
