# Procedure: DEL-02.03 Earthworks Design Calculations

## Purpose

Define the calculation workflow for Earthworks Design Calculations to ensure the deliverable satisfies Specification requirements R1-R6, implements Guidance principles P1-P4, and supports PKG-02 Earthworks & Ground Improvement objectives.

**Dual-Use Note:** This procedure describes how to **produce** the design calculations deliverable. It does not describe field execution procedures (see DEL-02.07 for field procedures).

Source: _CONTEXT.md; decomposition DEL-02.03 entry (location TBD).

## Prerequisites

### Dependencies
**Coordination status:** Dependencies coordinated externally by humans (see _DEPENDENCIES.md).

**Key coordination interfaces:**
- DEL-02.04 (Geotechnical Reports): Provides soil parameters, bearing capacity recommendations, ground improvement design; required input for bearing capacity calculations (R3).
- DEL-02.05 (Survey Reports): Provides topographic survey data; required input for cut/fill calculations (R2).
- DEL-02.01 (Earthworks Design Drawing Set): Uses calculation results to define grading and ground improvement; calculations must support design intent.
- DEL-02.02 (Earthworks Technical Specification): Uses calculation results for performance criteria and acceptance requirements; calculations must align with specification.

**Note:** Maturity of upstream deliverables to be managed per project schedule and coordination plan.

### Reference Materials Required

**Primary References:**
- Employer's Requirements volumes (Vol 2 Parts 1-3): **TBD** — not yet provided in _REFERENCES.md.
- Project calculation template and format standards: **TBD** — per ER or Contractor standards.
- Project document numbering system: **TBD**.

**Design Inputs:**
- Geotechnical investigation and design from DEL-02.04 (soil parameters, bearing capacity, ground improvement).
- Topographic survey from DEL-02.05 (existing grades, site limits, benchmarks).
- Proposed finish grades and grading extents from DEL-02.01 (or preliminary design if calculations precede drawings).
- Loading conditions: **TBD** — pavement loads (PKG-04), structural loads (PKG-05, PKG-06), equipment loads.
- Design criteria: **TBD** — bearing capacity factors of safety, settlement limits, cut/fill tolerances.

**Technical Standards and Codes:**
- Geotechnical design codes: **TBD** — e.g., Canadian Foundation Engineering Manual, CSA standards.
- Bearing capacity methods: **TBD** — Terzaghi, Meyerhof, or code-specified methods.
- Civil design standards: **TBD** — grading, earthwork measurement.

### Tools and Resources
- Calculation tools: Spreadsheets, Civil 3D (cut/fill), geotechnical analysis software (bearing capacity).
- Access to referenced codes and standards.
- Project calculation template (if applicable).
- Document management system for revision control (R6).
- **ASSUMPTION**: Standard D&B engineering calculation tools and infrastructure.

## Steps

### Step 1: Compile and Validate Inputs
**Objective:** Gather all required reference materials and design inputs; confirm completeness and quality.

**Actions:**
1. Obtain and review ER volumes and extract earthworks design criteria:
   - Bearing capacity factors of safety and design methods.
   - Settlement limits.
   - Cut/fill tolerances and allowances.
   - **Status:** **TBD** — ER volumes not yet provided.
   - **Guidance reference:** Principle P3 (Design Conservatism).

2. Obtain geotechnical reports (DEL-02.04) and extract design data:
   - Soil classification and stratigraphy.
   - Strength parameters (cohesion, friction angle, unit weight).
   - Groundwater levels.
   - Bearing capacity recommendations.
   - Ground improvement design (if applicable).
   - **Verification:** Geotechnical data is complete and adequate for bearing capacity calculations (R3).
   - **Datasheet reference:** Calculation Content section 2 (bearing capacity).

3. Obtain survey reports (DEL-02.05) and extract topographic data:
   - Existing topography (contours, spot elevations, DTM).
   - Survey datum and coordinate system.
   - Survey accuracy and coverage.
   - **Verification:** Survey data is complete and adequate for cut/fill calculations (R2).
   - **Datasheet reference:** Calculation Content section 1 (cut/fill).

4. Obtain design drawing data (DEL-02.01) or preliminary design:
   - Proposed finish grades and contours.
   - Grading limits and extents.
   - Ground improvement zones (if applicable).
   - **Note:** Calculations may precede final drawings; coordinate with design team on iteration sequence.
   - **Guidance reference:** Principle P4 (Multi-Deliverable Coordination).

5. Identify loading conditions and design criteria:
   - Pavement loads, structural loads, equipment loads.
   - Design factors of safety, settlement limits.
   - **TBD**: Specific loads and criteria pending ER and adjacent package designs.

**Outputs:**
- Validated input data package.
- Input data gaps documented as **TBD** or flagged for resolution.

**Datasheet alignment:** Input validation confirms data availability for Calculation Content sections.

### Step 2: Confirm Scope and Calculation Requirements
**Objective:** Define calculation scope, required calculation packages, and documentation requirements per Specification R1-R6.

**Actions:**
1. Review PKG-02 scope (grading, excavation, fill placement, ground improvement) and confirm calculation coverage.
   - **Specification reference:** R4 (scope coverage).
   - **Guidance reference:** Principle P4 (Multi-Deliverable Coordination).

2. Confirm required calculation packages per R2-R3:
   - Cut/fill quantity calculations (R2).
   - Bearing capacity calculations (R3).
   - Additional calculations if required by ER or design (e.g., settlement, slope stability).

3. Establish calculation format and documentation requirements:
   - Calculation template per project or Contractor standard.
   - Documentation of inputs, assumptions, methods, outputs per R5.
   - Independent check requirement per R6.
   - **Datasheet reference:** Calculation format attribute, Check status attribute.

4. Establish document numbering, revision scheme, and control requirements:
   - **Specification reference:** R6 (document control and checking).
   - **Datasheet reference:** Calculation package ID, Revision attributes.

**Outputs:**
- Scope definition and calculation package list.
- Calculation format and documentation plan.
- Document control plan (numbering, revision, checking, approvals).

**Verification reference:** Specification V2 (scope alignment).

### Step 3: Develop Calculations
**Objective:** Perform calculations per Specification R2-R3 and Guidance principles P1-P4.

**Actions:**
1. **Develop Cut/Fill Quantity Calculations (R2):**

   **Inputs:**
   - Existing topography from DEL-02.05.
   - Proposed finish grades from DEL-02.01 or preliminary design.
   - Grading limits and extents.

   **Method:**
   - Select calculation method (cross-section method, average end area, DTM).
   - If using software (e.g., Civil 3D), document software version and key settings.
   - Calculate cut and fill volumes.
   - Apply allowances for compaction shrinkage, over-excavation, waste factors.
   - **TBD**: Specific method and allowances pending ER and design criteria; typical allowances are +5% shrinkage, +2% over-excavation (**ASSUMPTION**).
   - **Guidance reference:** Principle P1 (Accuracy), P2 (Traceability), P3 (Conservatism).

   **Outputs:**
   - Total cut volume.
   - Total fill volume.
   - Net cut/fill balance.
   - Volumetric breakdown by zone or phase (if applicable).
   - Haul quantities and distances (if applicable).

   **Documentation:**
   - Document inputs (survey data, proposed grades, limits).
   - Show calculation method and key steps.
   - Present results with units; include sketches or cross-sections where helpful.
   - **Datasheet reference:** Calculation Content section 1.

2. **Develop Bearing Capacity Calculations (R3):**

   **Inputs:**
   - Soil parameters from DEL-02.04 (cohesion, friction angle, unit weight, groundwater level).
   - Loading conditions (pavement loads, structural loads, equipment loads).
   - Foundation depth and configuration (if applicable).

   **Method:**
   - Select bearing capacity method per code/standard or DEL-02.04 recommendations (e.g., Terzaghi, Meyerhof).
   - Calculate ultimate bearing capacity.
   - Apply factor of safety per ER or code requirements.
   - Calculate allowable bearing capacity.
   - Calculate settlement estimates (if required).
   - **TBD**: Specific method and factor of safety pending ER and DEL-02.04; typical FS = 2.5-3.0 (**ASSUMPTION**).
   - **Guidance reference:** Principle P1 (Accuracy), P2 (Traceability), P3 (Conservatism), P4 (Coordination with DEL-02.04).

   **Outputs:**
   - Ultimate bearing capacity.
   - Allowable bearing capacity.
   - Settlement estimates (if required).
   - Ground improvement requirements (if bearing capacity is inadequate).

   **Documentation:**
   - Document inputs (soil parameters, loads, geometry).
   - Document assumptions (foundation depth, load distribution, groundwater conditions).
   - Show calculation method, equations, and steps.
   - Present results with units; include sketch of bearing capacity model.
   - **Datasheet reference:** Calculation Content section 2.

3. **General Documentation Requirements (All Calculations, per R5):**
   - Title page or header: Calculation title, project name, calculation ID, preparer, date.
   - Design basis: List input sources, design criteria, applicable standards.
   - Assumptions: State all assumptions clearly; note basis where applicable.
   - References: Cite all data sources (DEL-02.04, DEL-02.05, ER, codes/standards).
   - Calculation body: Show inputs, method, steps, results clearly and traceably.
   - Summary: Present key results in summary table or section.
   - Sketches/diagrams: Include where they aid understanding.
   - **Guidance reference:** Principle P2 (Traceability and Documentation).

**Outputs:**
- Complete calculation packages for cut/fill (R2) and bearing capacity (R3).
- Calculations formatted per project template.
- All documentation requirements (R5) satisfied.

**Guidance alignment:** Calculation development applies Principles P1-P4 and addresses Trade-offs (detail level, software vs. manual, conservatism).

### Step 4: Perform Internal Verification and Checking
**Objective:** Verify calculation completeness, accuracy, and coordination with Specification requirements R1-R6 and verification items V1-V4.

**Actions:**
1. **Content Completeness Check (V1):**
   - Verify all required calculation packages (cut/fill, bearing capacity) are present.
   - Verify all documentation requirements (inputs, assumptions, methods, outputs, references) are complete per R5.
   - Verify document control fields (calculation ID, preparer, checker, dates) are complete per R6.
   - **Specification reference:** Verification V1.
   - **Datasheet reference:** Compare delivered content to Calculation Content sections.

2. **Scope Alignment Check (V2):**
   - Verify calculations address all PKG-02 scope items relevant to earthworks design (grading, excavation, fill, ground improvement).
   - **Specification reference:** Verification V2.
   - **Guidance reference:** Principle P4 (Coordination).

3. **ER Compliance Check (V3):**
   - Verify calculation methods, criteria, and factors of safety align with ER requirements.
   - **Status:** **TBD** — pending ER volumes.
   - **Specification reference:** Verification V3.

4. **Independent Check (V4a — Required per R6):**
   - **Checker:** Qualified engineer different from preparer.
   - **Check scope:**
     - Verify input data is from approved sources and is accurate.
     - Verify assumptions are reasonable and documented.
     - Verify calculation method is appropriate and correctly applied.
     - Verify calculations (arithmetic, equations, software inputs/outputs).
     - Verify results are reasonable and consistent.
   - **Records:** Checker signs and dates calculation package; checker comments documented and addressed.
   - **Guidance reference:** Principle P1 (Accuracy and Verification), QA/QC Considerations (Independent Checking).

5. **Design and Construction Coordination Check (V4b):**
   - **Design Coordination:**
     - Verify cut/fill quantities align with DEL-02.01 (Design Drawing Set) and DEL-02.05 (Survey Reports).
     - Verify bearing capacity results support loads and ground improvement shown in DEL-02.01.
     - Verify calculation outputs provide basis for performance criteria in DEL-02.02 (Technical Specification).
     - Check for conflicts or inconsistencies between calculations, drawings, specifications, and geotechnical reports.

   - **Specification reference:** Verification V4.
   - **Guidance reference:** Principle P4 (Multi-Deliverable Coordination), QA/QC Considerations (Cross-Document Verification).

6. **Cross-Document Consistency Check:**
   - Verify terminology and values are consistent across Datasheet, Specification, Guidance, and Procedure.
   - Verify calculation outputs match values cited in other documents.

**Outputs:**
- Verification and check records.
- Nonconformances documented and resolved.
- Calculation package ready for issuance or flagged for revision.

**Records:** Check records and sign-offs per Documentation section in Specification.md.

### Step 5: Issue Controlled Deliverable
**Objective:** Issue calculation package per document control requirements (R6) and capture approval records.

**Actions:**
1. Finalize calculation package with all check comments addressed.
   - Update revision and date fields.
   - Obtain checker sign-off.
   - **Specification reference:** R6 (document control and checking).

2. Obtain required approvals (preparer, independent checker, design lead, Employer if applicable).
   - **ASSUMPTION:** Approval workflow per standard D&B document control.
   - **Records:** Approval signatures or electronic approval records.

3. Issue controlled calculation package through document management system.
   - Assign final calculation package ID and revision per project numbering system.
   - Distribute to relevant stakeholders (design team, construction team, QA/QC, Employer).
   - **Datasheet reference:** Calculation package ID, Check status, Revision attributes.

4. Capture issuance records and maintain revision history.
   - **Specification reference:** Documentation section (review comments and response log).
   - **Records:** Transmittal, distribution list, revision log.

**Outputs:**
- Issued Earthworks Design Calculations (controlled revision).
- Approval and check records.
- Distribution records and transmittal.

**Guidance reference:** QA/QC Considerations (Review Workflow).

## Verification

### Calculation Completeness
**Check:** All required calculation packages (R2-R3) and documentation (R5-R6) are present and complete.
- **Method:** Compare delivered content against Datasheet Calculation Content sections and Specification R2-R6.
- **Criteria:** All required calculations present with inputs, methods, assumptions, outputs clearly documented; independent check complete and signed.
- **Reference:** Specification V1; Datasheet Calculation Content sections.

### Scope Coverage
**Check:** Calculations address all PKG-02 scope items relevant to earthworks design.
- **Method:** Review calculation content against PKG-02 scope.
- **Criteria:** All scope items have corresponding design basis; no scope gaps.
- **Reference:** Specification V2; Guidance Principle P4.

### Calculation Accuracy
**Check:** Calculations are accurate, verifiable, and based on valid inputs and methods.
- **Method:** Independent check by qualified engineer.
- **Criteria:** Inputs correct, assumptions reasonable, methods appropriate, calculations accurate, results consistent and reasonable.
- **Reference:** Specification V4; Guidance Principle P1.

### Design and Construction Coordination
**Check:** Calculations are consistent with design deliverables and support construction execution.
- **Method:** Cross-reference calculations with DEL-02.01 (drawings), DEL-02.02 (specification), DEL-02.04 (geotechnical), DEL-02.05 (survey).
- **Criteria:** No contradictions or inconsistencies; calculation outputs used correctly in drawings and specifications.
- **Reference:** Specification V4; Guidance Principle P4.

### ER Compliance
**Check:** Calculations align with ER design criteria and methods.
- **Method:** Review against ER requirements when available.
- **Criteria:** **TBD** — pending ER volumes.
- **Reference:** Specification V3.
- **Status:** Requirements not yet available; compliance check deferred.

## Records

### Primary Deliverable Records
- **Issued Earthworks Design Calculations:** Controlled revision with calculation package ID, preparer/checker sign-offs, revisions, dates per R6.

### Production Records
- **Input Data Package:** Documentation of reference materials used (ER, geotechnical reports, survey data, design drawings, codes/standards).
- **Independent Check Records:** Checker sign-off, check comments and resolutions.
- **Calculation Review Checklist:** Record of internal verification (Step 4) against V1-V4.
- **Review Comments and Responses:** Log of review comments (internal, design, Employer) and resolutions.

### Approval and Distribution Records
- **Approval Records:** Preparer, checker, approver signatures or electronic approvals.
- **Transmittal Records:** Distribution list, transmittal letter, issuance date.
- **Revision History:** Log of revisions, dates, and reasons for revision.

### Coordination Records
- **Coordination Notes:** Documentation of coordination with DEL-02.01, DEL-02.02, DEL-02.04, DEL-02.05.
- **Conflict Resolutions:** Documentation of any conflicts identified and resolved during calculation development (e.g., between survey data and proposed grades, between bearing capacity and design loads).

**Assumption:** Records management per standard D&B engineering calculation and QA/QC procedures.

## References

- _CONTEXT.md: Deliverable identity, description, and anticipated artifacts.
- _DEPENDENCIES.md: Dependency coordination mode (NOT_TRACKED); coordination managed externally.
- Decomposition file: `/Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md` — PKG-02 scope, DEL-02.03 entry, Section 1.2 Scope Focus (location TBD).
- Datasheet.md: Calculation content and attributes; steps validate against Datasheet.
- Specification.md: Requirements R1-R6 and verification items V1-V4; steps implement requirements.
- Guidance.md: Principles P1-P4 and considerations; steps apply principles.
- _REFERENCES.md: Currently empty; ER volumes and reference materials pending.
- Related deliverables: DEL-02.01, DEL-02.02, DEL-02.04, DEL-02.05 (coordination interfaces).
