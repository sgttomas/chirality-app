# Procedure: DEL-08.03 Marine Structures Design Calculations

## Purpose

This procedure defines a **repeatable production workflow** for the Marine Structures Design Calculations deliverable. It describes the steps to develop the calculation package from initial setup through final issue, including verification steps aligned to the Specification requirements.

**Deliverable intent (source-anchored):** Provides the engineering basis and sizing/verification calculations for marine structures. *(Source: Decomposition line 283 + `_CONTEXT.md`)*

**Package scope context (source-anchored):** PKG-08 covers piling, access trestle, loading platform structure, catwalk, and abutments. *(Source: Decomposition line 275)*

---

## Prerequisites

### Dependencies

**Dependency tracking mode:** NOT_TRACKED *(per `_DEPENDENCIES.md`)*

Dependencies are coordinated externally by humans (see `test/execution/_Coordination/_COORDINATION.md`).

**Note:** Even though dependencies are NOT_TRACKED, the following upstream deliverables and inputs are anticipated to be required before calculation work can be finalized. Coordination of timing and availability is managed externally:

- **DEL-08.01 Marine Structures Design Drawing Set** — provides geometry, layout, member sizes, pile locations used as calculation inputs
- **DEL-08.02 Marine Structures Technical Specification** — provides material properties (steel grades, strengths)
- **DEL-08.04 Marine Geotechnical Report** — provides soil parameters, pile capacity recommendations, scour depth
- **DEL-08.06 Berthing Energy Calculation Report** — provides berthing loads (coordinate scope to avoid duplication)
- **DEL-08.09 Mooring Analysis Report** — provides mooring loads (coordinate scope to avoid duplication)
- **DEL-08.10 Current Assessment Basis Report** — provides current loads on structure
- **PKG-09 Marine Outfitting deliverables** — provide fender and bollard loads
- **PKG-11 Marine Loading System deliverables** — provide loading arm and operator shelter loads
- **ER clauses extraction** — ER Vol 2 Parts 1-2 clauses applicable to marine structures design criteria and methods must be identified
- **Project engineering procedures** — calculation format, QA/QC, independent check procedures

### Inputs / References (TBD)

The following inputs/references are **TBD** and must be available before calculation work can commence:

| Input / Reference | Required For | Status |
|---|---|---|
| Employer's Requirements clauses for marine structures design criteria and methods | R-003 compliance; design criteria, load combinations, acceptance criteria | **TBD** *(ER Vol 2 Parts 1-2 PDFs available; clause extraction pending)* |
| Codes and standards required by ER (with editions/years) | R-003 compliance; calculation methods | **TBD** *(likely: CSA S6, CSA S16, API RP 2A; editions TBD from ER)* |
| Design loads and load combinations | All structural calculations | **TBD** *(dead, live, environmental loads; load factors and combinations per ER and codes)* |
| Geotechnical design parameters from DEL-08.04 | Pile capacity calculations | **TBD** *(soil parameters, pile capacity, scour depth)* |
| Marine environment data | Environmental load calculations | **TBD** *(wind, current, wave, water levels, seismic)* |
| Vessel and mooring/berthing data | Mooring analysis, berthing loads | **TBD** *(design vessel characteristics; mooring arrangement; berthing energy from DEL-08.06)* |
| Equipment loads and envelopes from PKG-09, PKG-11 | Structural calculations | **TBD** *(loading arm loads, fender reactions, bollard loads)* |
| Material properties from DEL-08.02 | All structural calculations | **TBD** *(steel grades, yield/tensile strength)* |
| Geometry and layout from DEL-08.01 | All structural calculations | **TBD** *(member sizes, spans, elevations, pile locations)* |
| Calculation format and documentation standards | R-002, R-005 compliance | **TBD** *(project engineering procedures or ER)* |

---

## Procedure Steps (Production Workflow)

These steps are a **PROPOSAL** pending confirmation against ER and project engineering procedures. Actual workflow may vary based on project-specific requirements and practices.

### Step 1: Setup, Planning, and Scope Coordination

**Objective:** Establish calculation framework, confirm scope coverage, and coordinate scope with related deliverables.

**Actions:**
1. Review `Specification.md` R-001 to confirm minimum required calculation artifacts:
   - Pile capacity calculations
   - Trestle structural calculations
   - Mooring analysis
2. Review PKG-08 scope (Decomposition line 275) to confirm all scope elements will have calculations: piling, access trestle, loading platform structure, catwalk, abutments
3. Coordinate scope with related calculation deliverables to avoid duplication and ensure no gaps:
   - **DEL-08.06 Berthing Energy Calculation Report:** Clarify who calculates berthing energy and fender reaction loads (likely DEL-08.06); DEL-08.03 uses berthing loads from DEL-08.06 in structural calculations
   - **DEL-08.09 Mooring Analysis Report:** Clarify who performs mooring analysis and calculates bollard loads (likely DEL-08.09); DEL-08.03 uses mooring loads from DEL-08.09 in structural calculations
   - **DEL-08.10 Current Assessment Basis Report:** Clarify who calculates current loads on structure (likely DEL-08.10); DEL-08.03 uses current loads from DEL-08.10 in structural calculations
   - Document scope coordination agreements in design coordination meeting minutes or interface register
4. Develop preliminary calculation index listing all calculations to be performed:
   - Pile capacity calculations (geotechnical, structural, lateral, group effects, scour)
   - Trestle structural calculations (load analysis, member design, connection design, deflection/stability checks)
   - Platform structural calculations (if applicable)
   - Catwalk structural calculations (if applicable)
   - Abutment structural calculations (if applicable)
   - Mooring analysis or mooring load application (coordinate with DEL-08.09)
5. Prepare input register template for tracking input documents and parameters per `Specification.md` R-002
6. Prepare assumptions list template for tracking assumptions per `Specification.md` R-002

**Verification:**
- Calculation scope covers all required artifacts per R-001
- Scope coordination with DEL-08.06/08.09/08.10 documented
- Calculation index prepared
- Input register and assumptions list templates prepared

**Outputs:**
- Preliminary calculation index
- Scope coordination documentation (meeting minutes or interface register)
- Input register template
- Assumptions list template

**Sources:**
- `Specification.md` R-001
- `Guidance.md` § Calculation Scope Checklist
- Decomposition line 283 (anticipated artifacts), line 275 (PKG-08 scope)

---

### Step 2: Design Criteria and Code/Standard Identification

**Objective:** Identify and document all applicable design criteria, codes/standards, load cases, and acceptance criteria per `Specification.md` R-003.

**Actions:**
1. Review ER Vol 2 Parts 1-2 to identify clauses applicable to marine structures design *(TBD)*
2. Extract design criteria from ER:
   - Applicable codes/standards (with specific editions/years)
   - Design approach (allowable stress design (ASD) or limit states design (LSD))
   - Load cases and load combinations (ULS, SLS)
   - Serviceability criteria (deflection limits, vibration limits)
   - Environmental exposure factors (marine environment classification, corrosion allowance, scour assessment)
   - Acceptance criteria (unity checks, factors of safety, margins)
3. Identify codes and standards required by ER: *(TBD)*
   - Structural design codes (likely: CSA S6 for bridge-type structures, CSA S16 for steel design)
   - Marine structures codes (likely: API RP 2A for piling and marine structures)
   - Geotechnical codes (likely: Canadian Foundation Engineering Manual or API RP 2A for pile capacity)
   - Load codes (likely: NBCC or BCBC for dead/live/environmental loads)
   - Other applicable standards (mooring, berthing, etc.)
4. Document design criteria in design basis memorandum or design criteria section of calculation package:
   - List applicable codes/standards with editions
   - Define load cases and load combinations with references to code clauses or ER
   - State material properties to be used (from DEL-08.02)
   - State allowable stresses or resistance factors per code
   - State serviceability criteria per code or ER
   - State acceptance criteria for calculations
5. Populate input register with ER clauses, code references, and design criteria
6. Flag any ER requirements that are ambiguous or require clarification; prepare Request for Information (RFI) to Employer *(if needed)*

**Verification:**
- All applicable ER clauses identified and extracted
- All codes/standards required by ER identified (with editions/years)
- Design criteria documented
- Clarification requests (RFIs) prepared for ambiguous requirements

**Outputs:**
- Design criteria documentation (design basis memorandum or calculation section)
- Codes/standards list with editions
- Load cases and load combinations defined
- RFIs to Employer *(if needed)*
- Updated input register

**Sources:**
- `Specification.md` R-003
- `Guidance.md` § Requirement Rationale Map, R-003
- ER Vol 2 Parts 1-2 PDFs *(TBD)*

---

### Step 3: Input Collection and Assumptions Definition

**Objective:** Collect all input data required for calculations and define assumptions per `Specification.md` R-002.

**Actions:**
1. Collect input documents and record in input register:
   - DEL-08.01 Marine Structures Design Drawing Set (geometry, layout, member sizes, pile locations) *(document number, revision, date)*
   - DEL-08.02 Marine Structures Technical Specification (material properties) *(document number, revision, date)*
   - DEL-08.04 Marine Geotechnical Report (soil parameters, pile capacity, scour depth) *(document number, revision, date)*
   - DEL-08.06 Berthing Energy Calculation Report (berthing loads) *(if available; document number, revision, date)*
   - DEL-08.09 Mooring Analysis Report (mooring loads) *(if available; document number, revision, date)*
   - DEL-08.10 Current Assessment Basis Report (current loads) *(if available; document number, revision, date)*
   - PKG-09, PKG-11 deliverables (equipment loads) *(if available; document numbers, revisions, dates)*
   - ER Vol 2 Parts 1-2 (design requirements, environmental data) *(document numbers, revisions)*
   - Codes/standards (editions identified in Step 2)
2. Extract input parameters from input documents and record in input register with source citations:
   - Geometry: spans, elevations, member sizes, pile locations (from DEL-08.01)
   - Material properties: steel grades, yield/tensile strength, elastic modulus (from DEL-08.02 or code)
   - Loads: dead loads (self-weight), live loads, equipment loads, environmental loads (wind, current, wave, seismic), berthing loads, mooring loads (from various sources)
   - Geotechnical parameters: soil layering, soil strength parameters, pile capacity, scour depth (from DEL-08.04)
   - Environmental data: design wind speed, current velocity, wave height/period, water levels, seismic parameters (from ER or environmental reports)
   - Vessel data: design vessel dimensions, displacement, draft, mooring arrangement (from ER or mooring analysis)
3. Identify and document assumptions:
   - **Input assumptions:** If input not yet available or uncertain, state assumption and label (e.g., "ASSUMPTION: Preliminary pile locations from DEL-08.01 Rev A; final locations TBD from DEL-08.01 final issue")
   - **Load assumptions:** Assumptions about load application, load distribution, load coincidence (e.g., "ASSUMPTION: Maximum environmental loads (wind, current, wave) assumed to occur simultaneously; conservative for design")
   - **Geometry assumptions:** Assumptions about geometry, boundary conditions, load paths (e.g., "ASSUMPTION: Pile head connection assumed pinned for trestle analysis; verify connection detail in DEL-08.01")
   - **Material assumptions:** Assumptions about material properties if not fully specified (e.g., "ASSUMPTION: Steel elastic modulus = 200 GPa per CSA S16")
   - Record all assumptions in assumptions list with labels and justification/notes
4. Flag inputs that are TBD or need confirmation; plan to update calculations when inputs are confirmed

**Verification:**
- Input register complete with all required input documents and parameters
- Source citations provided for all input values (document, section, page, table)
- Assumptions list complete with all assumptions labeled and justified
- TBD inputs identified with plan for resolution

**Outputs:**
- Populated input register
- Populated assumptions list
- Input data summary (organized by topic: geometry, materials, loads, geotechnical, environmental, vessel)

**Sources:**
- `Specification.md` R-002
- `Guidance.md` § Requirement Rationale Map, R-002
- Input documents from DEL-08.01, DEL-08.02, DEL-08.04, DEL-08.06, DEL-08.09, DEL-08.10, PKG-09, PKG-11 *(TBD)*

---

### Step 4: Perform Calculations

**Objective:** Execute calculations per design criteria and document results per `Specification.md` R-002, R-003.

**Actions:**

Perform calculations for each topic in calculation scope (coordinate sequence based on dependencies):

#### 4a: Pile Capacity Calculations

1. **Geotechnical pile capacity:** Calculate axial pile capacity (compression and tension) based on soil parameters from DEL-08.04; use calculation method per code (API RP 2A or Canadian Foundation Engineering Manual); check geotechnical capacity for each pile type/location
2. **Structural pile capacity:** Calculate structural capacity of pile (axial, bending, shear, combined loading); use pile material properties from DEL-08.02; check buckling for unsupported pile lengths; design per CSA S6 or CSA S16
3. **Lateral pile capacity:** Calculate lateral load capacity and deflection using p-y curve method or equivalent; use soil parameters from DEL-08.04; check lateral capacity for mooring/berthing loads
4. **Pile group effects:** Calculate group efficiency factors if piles are closely spaced; distribute loads among pile groups
5. **Scour assessment:** Assess scour depth per DEL-08.04 or marine codes; check effect on pile embedment and capacity
6. **Summary:** Tabulate pile capacity results (geotechnical capacity, structural capacity, governing capacity, unity checks) for each pile type/location
7. Document calculation narrative, assumptions, methods, and results; cite sources for all inputs and methods

#### 4b: Trestle Structural Calculations

1. **Load analysis:** Calculate dead loads (self-weight), live loads, environmental loads (wind, current if applicable); define load combinations per CSA S6 or ER; calculate member forces (axial, shear, moment) using structural analysis (hand, spreadsheet, or software)
2. **Member sizing and design:** Design beams, columns, braces for trestle framing; select material grades per DEL-08.02; calculate section properties; perform unity checks for axial, bending, shear, combined loading per CSA S16 or CSA S6; iterate member sizes to achieve unity checks ≤ 1.0 with adequate margin
3. **Connection design:** Design bolted and/or welded connections for trestle framing; calculate connection capacity for shear, tension, moment; select bolt grades, weld sizes per CSA S16 or CSA S6; perform unity checks for connections
4. **Deflection and serviceability checks:** Calculate deflections under service loads; check against deflection limits per code or ER; assess vibration if applicable
5. **Stability checks:** Check overall trestle stability (overturning, sliding); check lateral bracing adequacy; check buckling for compression members
6. **Summary:** Tabulate trestle structural results (member sizes, capacities, unity checks, deflections) in summary table
7. Document calculation narrative, assumptions, methods, and results; cite sources

#### 4c: Mooring Analysis (or Mooring Load Application)

1. **Scope coordination:** Confirm scope with DEL-08.09; if DEL-08.09 performs detailed mooring analysis, DEL-08.03 uses mooring loads from DEL-08.09 as input; if DEL-08.03 performs mooring analysis, calculate as follows:
2. **Environmental loads on moored vessel:** Calculate wind, current, wave loads on design vessel; use environmental data from ER or DEL-08.10; use calculation methods per OCIMF MEG4 or equivalent
3. **Mooring line loads:** Calculate mooring line tensions under environmental loading; use mooring arrangement from ER or vessel assumptions; calculate load sharing among mooring lines; check mooring line capacity
4. **Structure loads from mooring:** Calculate loads transferred from mooring bollards to structure (platform, trestle); apply bollard loads to structural model; include in load combinations for structural design
5. **Summary:** Tabulate mooring loads (line tensions, bollard loads) for use in structural calculations
6. Document calculation narrative, assumptions, methods, results; cite sources; cross-reference DEL-08.09 if applicable

#### 4d: Platform, Catwalk, Abutment Structural Calculations (If Applicable)

1. Perform structural calculations for platform, catwalk, abutments similar to trestle calculations (Step 4b) with appropriate loads and criteria
2. Document narrative, assumptions, methods, results

#### For All Calculations:

1. Provide calculation narrative explaining approach, logic, and key steps
2. Show intermediate calculations and results (not every arithmetic step, but sufficient to follow logic)
3. Use consistent units throughout (metric or imperial; state clearly); show appropriate precision
4. Cite sources for all inputs, assumptions, methods, and criteria (reference input register, assumptions list, code clauses)
5. Summarize results in tables with clear headings and units
6. Highlight critical results (governing capacities, limiting unity checks, critical deflections)
7. For software calculations: document software name/version, model description, input file summary, output file printout, verification/benchmark check

**Verification:**
- All required calculations per calculation index completed
- All inputs traceable to input register
- All assumptions traceable to assumptions list
- Calculation narrative clear and sufficient for independent check
- Results summarized in tables
- Acceptance criteria met (unity checks ≤ 1.0, deflections within limits, etc.) or non-conformances flagged

**Outputs:**
- Completed calculation package (pile capacity, trestle structural, mooring analysis, platform/catwalk/abutment calculations)
- Results summary tables
- Software files (if applicable: input files, output files, model files)

**Sources:**
- `Specification.md` R-002, R-003
- `Guidance.md` § Calculation Scope Checklist, § Trade-offs and Decisions
- Design criteria from Step 2
- Input data from Step 3
- Codes/standards per Step 2

---

### Step 5: Self-Check and Package Assembly

**Objective:** Verify calculation accuracy and completeness before submittal for independent check.

**Actions:**
1. Perform self-check of calculations:
   - Verify all inputs used match input register and are from correct document revisions
   - Verify all assumptions are labeled and listed in assumptions list
   - Verify calculation methods are correct and consistent with design criteria
   - Check arithmetic and formulas for errors (spot check or use alternate method)
   - Verify units are consistent and correct
   - Verify results are reasonable (order of magnitude checks, comparison to similar projects if available)
   - Verify acceptance criteria are met or non-conformances flagged
2. Assemble calculation package per `Specification.md` R-005:
   - **Cover sheet:** Calculation title, document number, revision, date, originator name/signature, checker name/signature (blank), approver name/signature (blank), professional seal (blank if P.Eng. seal required)
   - **Table of contents:** List all calculation sections/topics with page numbers
   - **Design criteria section:** Design criteria documentation from Step 2
   - **Input register:** Populated input register from Step 3
   - **Assumptions list:** Populated assumptions list from Step 3
   - **Calculations:** All calculations from Step 4, organized by topic (pile capacity, trestle structural, mooring analysis, etc.)
   - **Summary of results:** Summary tables of key results from all calculations
   - **Appendices:** Supporting documentation (software input/output files, referenced documents, vendor data, etc.)
3. Number pages consecutively; add headers/footers with document number, revision, page number
4. Prepare calculation transmittal or cover letter (if required for submittal)
5. Document self-check in self-check checklist

**Verification:**
- Self-check completed
- Calculation package assembled per R-005 format requirements
- All required sections present (cover sheet, TOC, design criteria, input register, assumptions list, calculations, summary, appendices)
- Pages numbered, headers/footers complete

**Outputs:**
- Assembled calculation package ready for independent check
- Self-check checklist

**Sources:**
- `Specification.md` R-002, R-005
- `Guidance.md` § Requirement Rationale Map R-005

---

### Step 6: Independent Check

**Objective:** Obtain independent verification of calculations per `Specification.md` R-004.

**Actions:**
1. Submit calculation package to independent checker (qualified engineer not involved in original calculations)
2. Independent checker reviews calculations:
   - Verify inputs are correct and traceable (check input register against source documents)
   - Verify assumptions are reasonable and appropriately labeled
   - Verify calculation methods are correct and consistent with design criteria and code
   - Verify arithmetic and formulas (spot check or full check per project QA/QC procedures)
   - Verify units and precision
   - Verify results are reasonable and acceptance criteria are met
   - Identify errors, omissions, non-conformances, or areas needing clarification
3. Independent checker documents review comments (markup on calculations or separate comment register)
4. Hold comment resolution meeting with originator and checker
5. Originator resolves checker comments:
   - Correct errors and update calculations
   - Clarify ambiguous areas and update calculation narrative
   - Revise assumptions if needed and update assumptions list
   - Update input register if inputs corrected
   - Update results summary if results changed
6. Resubmit updated calculations to checker for review of resolutions
7. Checker verifies resolutions are satisfactory and signs off on cover sheet when satisfied

**Verification:**
- Independent check completed
- All checker comments documented
- All checker comments resolved to checker's satisfaction
- Checker sign-off obtained on cover sheet

**Outputs:**
- Independent check comment register or markup
- Updated calculation package incorporating checker comment resolutions
- Checker sign-off on cover sheet

**Sources:**
- `Specification.md` R-004
- `Guidance.md` § Requirement Rationale Map, R-004
- Project QA/QC procedures *(TBD)*

---

### Step 7: Discipline Check and Professional Seal (If Required)

**Objective:** Obtain discipline lead review and professional seal if required.

**Actions:**
1. Submit checked calculation package to discipline lead (senior marine engineer or engineering manager) for discipline check:
   - Verify calculation approach is appropriate and consistent with project standards
   - Verify results are reasonable and consistent with design intent
   - Verify major assumptions are appropriate
   - Verify calculation package is complete and ready for issue
2. Collect discipline lead comments and resolve if needed
3. Obtain discipline lead approval/sign-off
4. If professional seal (P.Eng.) is required per ER or BC regulatory requirements *(TBD)*:
   - Submit calculation package to Professional Engineer (P.Eng.) licensed in BC for review and seal
   - P.Eng. reviews calculations for compliance with professional standards and code of ethics
   - P.Eng. may require changes or additional verification before sealing
   - P.Eng. applies professional seal (stamp) and signature to cover sheet with date
   - P.Eng. takes professional responsibility for calculations
5. Update cover sheet with all required signatures and seal

**Verification:**
- Discipline check completed and approval obtained
- Professional seal applied if required
- Cover sheet complete with all required signatures and seal

**Outputs:**
- Discipline check approval
- Professional seal on cover sheet (if required)
- Fully approved calculation package

**Sources:**
- `Specification.md` R-004
- `Guidance.md` § Requirement Rationale Map, R-004
- ER requirements for professional seal *(TBD)*
- BC regulatory requirements (Engineers and Geoscientists BC) *(TBD)*

---

### Step 8: Finalize for Issue

**Objective:** Finalize calculation package for issue.

**Actions:**
1. Update document control metadata:
   - Set document number per project numbering scheme *(TBD)*
   - Set revision to issue revision (e.g., "Rev 0" for first issue) per project document control *(TBD)*
   - Set issue status (e.g., "Issued for Construction", "Issued for Design") per project requirements *(TBD)*
   - Update date to issue date on cover sheet
2. Perform final QA check:
   - Verify all required signatures and seal are on cover sheet
   - Verify document number, revision, date are correct and consistent throughout package
   - Verify calculation package is complete (cover sheet, TOC, design criteria, input register, assumptions list, calculations, summary, appendices)
   - Verify pages are numbered consecutively and headers/footers are correct
3. Prepare calculation transmittal or cover letter per project document control *(TBD)*
4. Assemble issue package:
   - Calculation package (PDF or hardcopy)
   - Calculation transmittal
   - Supporting electronic files (spreadsheets, software files) if required

**Verification:**
- Document control metadata correct
- Final QA check completed
- Issue package assembled and complete

**Outputs:**
- Final calculation package ready for issue
- Calculation transmittal
- Issue package assembled

**Sources:**
- `Specification.md` R-005
- Project document control procedures *(TBD)*

---

### Step 9: Issue and Archive

**Objective:** Issue calculation package and archive records.

**Actions:**
1. Issue calculation package per project document control procedures:
   - Submit to Employer via project document management system or transmittal *(TBD)*
   - Obtain issue receipt or acknowledgment *(TBD)*
2. Copy issued calculation package to `test/execution/PKG-08_Marine_Structures/3_Issued/` folder:
   - Include calculation package (PDF), transmittal, and supporting electronic files
   - Name files with deliverable ID, revision, and date (e.g., `DEL-08.03_Rev0_2026-01-28.pdf`)
3. Update `_STATUS.md` to ISSUED with issue date and revision in history entry
4. Archive working files and review records:
   - Input register
   - Assumptions list
   - Self-check records
   - Independent check comment register and markups
   - Discipline check records
   - Approval records
   - Software files (input/output/model files with version control)
   - Store in project archive per project records management procedures *(TBD)*

**Verification:**
- Calculation package issued and receipt confirmed
- Issued package copied to `3_Issued/` folder
- `_STATUS.md` updated to ISSUED
- Records archived

**Outputs:**
- Issued calculation package (in project document management system and `3_Issued/` folder)
- Updated `_STATUS.md`
- Archived working files and review records

**Sources:**
- Project document control procedures *(TBD)*
- Project records management procedures *(TBD)*

---

## Requirement Coverage Map

This table maps each `Specification.md` requirement to the procedure step(s) that address it and the expected verification evidence:

| Spec ID | Requirement | Covered by Step(s) | Expected Output / Evidence |
|---|---|---|---|
| R-001 | Calculation package coverage (minimum artifacts and scope elements); scope coordination | Step 1 (setup/planning/scope coordination), Step 4 (perform calculations) | Calculation index; scope coordination documentation; completed calculations covering all required topics |
| R-002 | Traceable inputs, assumptions, and results | Step 3 (input collection/assumptions), Step 4 (perform calculations), Step 5 (package assembly) | Input register; assumptions list; calculation narrative with source citations; results summary |
| R-003 | Design methods, criteria, and code compliance | Step 2 (design criteria/codes), Step 4 (perform calculations) | Design criteria documentation; code references; acceptance criteria met; unity checks/margins documented |
| R-004 | Independent check and professional seal | Step 6 (independent check), Step 7 (discipline check/seal) | Independent check sign-off; checker comment register; professional seal (if required) |
| R-005 | Calculation package format and document control | Step 5 (package assembly), Step 8 (finalize for issue), Step 9 (issue/archive) | Calculation package assembled per format requirements; document control metadata complete; issue package with transmittal |

---

## Verification Summary

Verification/acceptance criteria are **TBD** pending ER and project engineering/QA/QC procedures. The following verification approach is **PROPOSED** based on standard engineering practice:

| Verification Activity | Performed In Step | Acceptance Criteria |
|---|---|---|
| Self-check | Step 5 | Self-check completed; inputs/assumptions verified; arithmetic checked; results reasonable; acceptance criteria met |
| Independent check | Step 6 | Checker reviews inputs, assumptions, methods, results; comments documented and resolved; checker sign-off obtained |
| Discipline check | Step 7 | Discipline lead verifies approach, results, completeness; approval obtained |
| Professional seal (if required) | Step 7 | P.Eng. reviews and seals calculations; professional responsibility accepted |
| Final QA check | Step 8 | All required signatures/seal on cover sheet; document control metadata correct; package complete |

**Final acceptance:** Calculation package issued per Step 9 with all required approvals, verifications, and professional seal (if required) complete.

---

## Records

### Minimum Expected Deliverable Outputs (per Specification.md)

Per `Specification.md` R-001 and Decomposition line 283:

- Pile capacity calculations
- Trestle structural calculations
- Mooring analysis

### Additional Calculation Outputs (Based on Scope)

Based on PKG-08 scope and typical requirements:

- Platform structural calculations
- Catwalk structural calculations
- Abutment structural calculations
- Connection design calculations

### Associated Records (TBD)

Records to retain with the calculation package or in project archive:

- Design criteria documentation — **TBD**
- Input register — **TBD**
- Assumptions list — **TBD**
- Self-check records — **TBD**
- Independent check comment register and markups — **TBD**
- Discipline check records — **TBD**
- Approval records and sign-offs — **TBD**
- Professional seal — **TBD** *(if required)*
- Calculation transmittal — **TBD**
- Software files (input/output/model files) — **TBD** *(if applicable)*

---

## Sources

- `test/execution/PKG-08_Marine_Structures/1_Working/DEL-08.03_Marine_Structures_Design_Calculations/_CONTEXT.md`
- `test/execution/PKG-08_Marine_Structures/1_Working/DEL-08.03_Marine_Structures_Design_Calculations/_DEPENDENCIES.md`
- `test/execution/PKG-08_Marine_Structures/1_Working/DEL-08.03_Marine_Structures_Design_Calculations/Specification.md`
- `test/execution/PKG-08_Marine_Structures/1_Working/DEL-08.03_Marine_Structures_Design_Calculations/Guidance.md`
- `test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md` (lines 271-291: PKG-08 scope statement at line 275; deliverables table; DEL-08.03 at line 283)
- `test/Volume_2_Part_1_Employers_Requirements.pdf` *(present in repo; content not extracted here; clause locations TBD)*
- `test/Volume_2_Part_2_Employers_Requirements.pdf` *(present in repo; content not extracted here; clause locations TBD)*
- Standard engineering calculation practice (for calculation workflow, QA/QC, independent check, professional seal requirements)
