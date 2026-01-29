# Specification: DEL-08.03 Marine Structures Design Calculations

## Scope

This document defines **minimum requirements for the deliverable artifact itself** (the Marine Structures Design Calculations package): required calculation content, input traceability, verification requirements, and packaging for issue.

**Deliverable description (source-anchored):** Provides the engineering basis and sizing/verification calculations for marine structures. *(Source: Decomposition line 283 + `_CONTEXT.md`)*

**Package scope context (source-anchored):** PKG-08 covers piling, access trestle, loading platform structure, catwalk, and abutments. *(Source: Decomposition line 275)*

---

## Requirements (Deliverable Content)

### R-001 — Calculation Package Coverage (Minimum)

**Requirement:** The calculation package shall include, at minimum, the following anticipated calculation artifacts as listed in the decomposition deliverables table (line 283):

- Pile capacity calculations
- Trestle structural calculations
- Mooring analysis

**Additional scope coverage requirement:** All marine structures scope elements listed in PKG-08 scope (Decomposition line 275) — piling, access trestle, loading platform structure, catwalk, abutments — shall have engineering basis and sizing/verification calculations included in the package or explicitly noted as covered by another deliverable.

**Scope coordination requirement:** Coordinate with related calculation deliverables (DEL-08.06 Berthing Energy Calculation Report, DEL-08.09 Mooring Analysis Report, DEL-08.10 Current Assessment Basis Report) to avoid duplication and ensure all required calculations are covered. Document scope boundaries and cross-references.

**Source:** Decomposition line 283 (anticipated artifacts); Decomposition line 275 (PKG-08 scope)

**Rationale:** See `Guidance.md` § Requirement Rationale Map, R-001

**Verification:** See `Procedure.md` § Requirement Coverage Map, R-001

---

### R-002 — Traceable Inputs, Assumptions, and Results

**Requirement:** Each calculation shall document the following to enable independent verification and auditability:

#### Input Traceability:
- **Input register:** List all input documents used (drawings, reports, specifications, standards) with document numbers, revisions, and dates
- **Input parameters:** List all numerical inputs (loads, dimensions, material properties, geotechnical parameters, environmental data) with sources and references
- **Source citations:** Cite the specific document, section, page, or table for each input value

#### Assumptions:
- **Explicit labeling:** All assumptions shall be explicitly labeled as "ASSUMPTION" and clearly distinguished from facts derived from referenced documents
- **Assumption list:** Maintain a consolidated assumption list for the calculation package
- **Assumption justification:** Provide engineering rationale or state when assumptions are conservative or require confirmation

#### Results Documentation:
- **Calculation narrative:** Provide sufficient narrative and commentary to explain calculation approach, logic, and intermediate steps
- **Results summary:** Summarize key results (member sizes, capacities, unity checks, margins) in a clear format (tables or summary sheets)
- **Units and precision:** Use consistent units throughout (metric or imperial; state clearly); show appropriate precision for results

**ASSUMPTION:** Calculation format and documentation standards exist in project procedures or ER; specific format requirements: **TBD**

**Source:** Standard engineering calculation practice; project-specific requirements TBD from ER or project engineering procedures

**Rationale:** See `Guidance.md` § Requirement Rationale Map, R-002

**Verification:** See `Procedure.md` § Requirement Coverage Map, R-002

---

### R-003 — Design Methods, Criteria, and Code Compliance (ER-Driven)

**Requirement:** Calculation methods, design criteria, and acceptance criteria shall comply with applicable ER requirements and referenced codes/standards.

**Applicable ER clauses:** **TBD** *(ER Vol 2 Parts 1-2 present as PDFs; clause extraction pending)*

**Codes and standards:** Calculations shall use design methods and criteria from codes/standards required by ER. **TBD** *(pending ER clause review; likely codes: CSA S6 for bridge-type structures, CSA S16 for steel design, API RP 2A for marine structures and piling, geotechnical codes for pile capacity; confirm editions from ER)*

**Design criteria documentation:** Document the following design criteria used in calculations:
- **Load cases and combinations:** Define all load cases (dead, live, environmental, accidental) and load combinations (ULS, SLS) per code or ER
- **Material properties:** Steel grades, yield/tensile strength, elastic modulus used in calculations (reference DEL-08.02 specification)
- **Allowable stresses or resistance factors:** Allowable stress design (ASD) or limit states design (LSD) approach per code; resistance factors or safety factors used
- **Serviceability criteria:** Deflection limits, vibration limits, other serviceability criteria per code or ER
- **Environmental exposure factors:** Marine environment exposure classification; corrosion allowance (if applicable); durability considerations

**Acceptance criteria:** State acceptance criteria for each calculation (e.g., unity checks ≤ 1.0; deflection ≤ limit; factor of safety ≥ minimum). Reference ER or code clauses for acceptance criteria.

**ASSUMPTION:** ER specifies design codes and criteria for marine structures; specific ER clauses TBD.

**Source:** Decomposition line 283 (implicit ER compliance); ER requirements TBD; codes/standards TBD from ER

**Rationale:** See `Guidance.md` § Requirement Rationale Map, R-003

**Verification:** See `Procedure.md` § Requirement Coverage Map, R-003

---

### R-004 — Independent Check and Professional Seal

**Requirement:** Calculations shall be independently checked prior to issue.

**Independent check requirement:**
- **Checker qualifications:** Independent checker shall be a qualified engineer not involved in the original calculations
- **Check scope:** Checker shall verify calculation inputs, assumptions, methods, and results; check for errors, omissions, and non-conformances with code/ER requirements
- **Check documentation:** Checker shall document review comments; originator shall resolve comments and update calculations; checker shall sign off when satisfied

**Professional seal requirement:** Calculations shall be sealed (stamped and signed) by a Professional Engineer (P.Eng.) licensed in British Columbia (or jurisdiction having authority) if required by ER or regulatory requirements. **TBD** *(confirm from ER or BC Building Code / regulatory requirements for marine structures)*

**ASSUMPTION:** Independent check is required per project QA/QC procedures; professional seal (P.Eng.) is required for structural calculations in BC; confirm from ER and regulatory requirements.

**Source:** Standard EPC QA/QC practice; professional engineering licensing requirements in BC; project-specific requirements TBD from ER

**Rationale:** See `Guidance.md` § Requirement Rationale Map, R-004

**Verification:** See `Procedure.md` § Requirement Coverage Map, R-004

---

### R-005 — Calculation Package Format and Document Control

**Requirement:** The calculation package shall comply with project document control requirements for numbering, revision control, issue status, and packaging.

**Calculation package number:** **TBD** *(pending project document control procedures; likely: discipline code + package code + type code + sequence, e.g., CALC-MAR-08-001)*

**Revision and issue status:** **TBD** *(typical: Rev A/B/C for internal review; Rev 0/1/2 for issued; confirm from project document control procedures)*

**Calculation format and organization:** Organize calculation package for clarity and ease of review:
- **Cover sheet:** Calculation title, document number, revision, date, originator, checker, approver, seal (if required)
- **Table of contents:** List all calculations/sections with page numbers
- **Input register and assumptions list:** Per R-002
- **Calculations:** Organized by topic (e.g., pile capacity, trestle structural, mooring analysis); each calculation with clear title, inputs, methods, results
- **Summary of results:** Tabular summary of key results (member sizes, capacities, unity checks)
- **Appendices:** Supporting documentation (software input/output files, referenced documents, vendor data, etc.)

**Calculation deliverable format:** Define format for issued calculations:
- **Hand calculations:** Scanned or PDF of calculation sheets with handwritten or typed calculations; checker markups visible or separate
- **Spreadsheet calculations:** Excel or equivalent files with formulas visible; summary sheets; input/output clearly identified
- **Software calculations:** Software input files, output files (printouts), model description; verification of software use (version, validation)
- **Mixed format:** Combination of hand, spreadsheet, and software calculations as appropriate; clearly identify calculation method for each section

**ASSUMPTION:** Project document control procedures exist and define calculation package numbering, revision scheme, and format requirements; specific requirements TBD.

**Source:** Standard engineering calculation practice; project-specific requirements TBD from ER and project engineering/document control procedures

**Rationale:** See `Guidance.md` § Requirement Rationale Map, R-005

**Verification:** See `Procedure.md` § Requirement Coverage Map, R-005

---

## Standards and References

### Codes and Standards (TBD)

Applicable codes and standards are **TBD** until the relevant ER clauses are extracted. Likely codes for Canadian marine structures (to be confirmed from ER):

- **CSA S6** — Canadian Highway Bridge Design Code (for bridge-type structures such as trestle, platform access)
- **CSA S16** — Design of Steel Structures (for structural steel design)
- **API RP 2A** — Planning, Designing and Constructing Fixed Offshore Platforms (for marine structures and piling design)
- **Canadian Foundation Engineering Manual (CFEM)** — For geotechnical design and pile capacity (if not covered by API RP 2A)
- **NBCC (National Building Code of Canada)** or **BCBC (BC Building Code)** — For loads, load combinations, seismic design (if applicable)
- **OCIMF Mooring Equipment Guidelines (MEG4)** — For mooring analysis (if applicable)
- **PIANC** — For berthing and mooring design guidelines (if applicable)

**ASSUMPTION:** Canadian codes and standards apply unless otherwise specified by ER. Specific editions and clauses: **TBD**

### Reference Documents

Minimum reference set for calculation development:

- **Employer's Requirements:** Vol 2 Parts 1-2 (available in repo as PDFs; clause extraction pending)
- **DEL-08.01 Marine Structures Design Drawing Set** (provides geometry, layout, member sizes, pile locations)
- **DEL-08.02 Marine Structures Technical Specification** (provides material properties)
- **DEL-08.04 Marine Geotechnical Report** (provides soil parameters, pile capacity recommendations, scour depth)
- **DEL-08.06 Berthing Energy Calculation Report** (provides berthing loads; coordinate scope)
- **DEL-08.09 Mooring Analysis Report** (provides mooring loads; coordinate scope)
- **DEL-08.10 Current Assessment Basis Report** (provides current loads on structure)
- **PKG-09 Marine Outfitting deliverables** (fender and bollard loads)
- **PKG-11 Marine Loading System deliverables** (loading arm and operator shelter loads)
- **Project Engineering Procedures** — **TBD** *(calculation format, QA/QC, independent check procedures)*

Reference index: `test/execution/PKG-08_Marine_Structures/0_References/_REFERENCE_INDEX.md` *(currently stub; to be populated)*

---

## Verification and Acceptance

### Verification Requirements

Verification requirements are not fully stated in accessible sources within this deliverable folder. The following verification approach is **PROPOSED** pending confirmation from ER and project QA/QC procedures:

1. **Originator self-check:** Engineer performing calculations verifies inputs, methods, and results before submittal for independent check
2. **Independent check:** Independent checker (qualified engineer not involved in original work) reviews calculations per R-004; comments documented and resolved
3. **Discipline check:** Senior marine engineer or discipline lead reviews calculation approach, assumptions, and results for technical adequacy
4. **Design review:** Calculations reviewed as part of overall design review (30%, 60%, 90% or equivalent milestones if applicable)
5. **Approval for issue:** Authorized approver signs off; professional seal applied if required

**Required reviews (to be confirmed):** Self-check, independent check, discipline check, approval for issue — **TBD**

**Professional seal requirement (to be confirmed):** P.Eng. seal required for structural calculations in BC — **TBD**

### Acceptance Criteria

Acceptance criteria for "issue" status are **TBD** pending ER and project procedures. Typical acceptance criteria (to be confirmed):

- All review comments resolved and dispositioned
- All requirements (R-001 through R-005) verified as met
- All calculations meet design criteria and acceptance criteria per R-003 (unity checks ≤ 1.0, deflections within limits, etc.)
- Input register and assumptions list complete per R-002
- Independent check sign-off obtained per R-004
- Professional seal applied if required per R-004
- Document control metadata complete per R-005

### Requirement Verification Map

| Spec ID | Verification Method | Evidence / Record | Status |
|---|---|---|---|
| R-001 | Calculation package completeness check against decomposition artifacts list (line 283) and PKG-08 scope (line 275); scope coordination with DEL-08.06/08.09/08.10 | Calculation index showing all required calculations; scope coordination documented | **TBD** |
| R-002 | Input traceability audit; assumptions list review | Input register with document revisions; assumptions list; calculation narrative with source citations | **TBD** |
| R-003 | Code compliance check; design criteria verification | Design criteria statement; code references; acceptance criteria verified; unity checks/margins documented | **TBD** |
| R-004 | Independent check review; professional seal verification (if required) | Independent check sign-off; checker comment resolution; professional seal on cover sheet (if required) | **TBD** |
| R-005 | Document control compliance check; calculation format review | Calculation package number, revision, format compliance; cover sheet, TOC, organization verified | **TBD** |

---

## Documentation / Deliverable Outputs

### Expected Calculation Outputs (Minimum)

Per Decomposition line 283 and this Specification R-001:

- Pile capacity calculations
- Trestle structural calculations
- Mooring analysis

### Additional Calculation Outputs (Based on Scope)

Based on PKG-08 scope (line 275) and typical marine structures design, the following additional calculations may be required (confirm scope with design development):

- Platform structural calculations
- Catwalk structural calculations
- Abutment structural calculations
- Connection design calculations
- Foundation design calculations (if not covered under pile capacity)

### Associated Records (TBD)

Records to retain with the calculation package or in project archive:

- Input register with document revisions used — **TBD** *(format and location TBD)*
- Assumptions list — **TBD**
- Independent check comment register and resolutions — **TBD**
- Independent check sign-off — **TBD**
- Professional seal (if required) — **TBD**
- Calculation transmittal — **TBD**
- Software files (if applicable: input files, output files, model files) — **TBD**

---

## Sources

- `test/execution/PKG-08_Marine_Structures/1_Working/DEL-08.03_Marine_Structures_Design_Calculations/_CONTEXT.md`
- `test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md` (lines 271-291: PKG-08 scope statement at line 275; deliverables table; DEL-08.03 at line 283)
- `test/Volume_2_Part_1_Employers_Requirements.pdf` *(present in repo; content not extracted here; clause locations TBD)*
- `test/Volume_2_Part_2_Employers_Requirements.pdf` *(present in repo; content not extracted here; clause locations TBD)*
- Standard engineering calculation practice (for input traceability, assumptions documentation, independent check, professional seal requirements)
