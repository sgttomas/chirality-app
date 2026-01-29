# Specification: DEL-08.04 Marine Geotechnical Report

## Scope

This document defines **minimum requirements for the deliverable artifact itself** (the Marine Geotechnical Report package): required report content, data traceability, QA/QC requirements, and packaging for design verification and approvals.

**Deliverable description (source-anchored):** Documents analysis and results for marine geotechnical report required for design verification and approvals. *(Source: Decomposition line 284 + `_CONTEXT.md`)*

**Package scope context (source-anchored):** PKG-08 covers piling, access trestle, loading platform structure, catwalk, and abutments. *(Source: Decomposition line 275)*

---

## Requirements (Deliverable Content)

### R-001 — Report Package Coverage (Minimum)

**Requirement:** The report package shall include, at minimum, the following anticipated report artifacts as listed in the decomposition deliverables table (line 284):

- Marine geotechnical investigation report
- Bathymetric survey report

**Report format:** Reports may be combined into a single document or issued as separate reports. If separate, ensure cross-references and consistent datum/coordinate systems.

**Source:** Decomposition line 284 (anticipated artifacts)

**Rationale:** See `Guidance.md` § Requirement Rationale Map, R-001

**Verification:** See `Procedure.md` § Requirement Coverage Map, R-001

---

### R-002 — Traceable Data, Methods, and Assumptions

**Requirement:** The report(s) shall document the following to enable independent verification, design use, and approval:

#### Data Traceability:
- **Investigation/survey scope:** Number, locations, and depths of borings/soundings/samples; survey extent and grid; investigation/survey dates
- **Field data:** Boring logs with soil/rock descriptions; field test data (SPT, CPT, etc.); survey data (depths/elevations, coordinates); site photos
- **Laboratory data:** Laboratory test results with sample identifications, test methods, and dates
- **Data custody:** Chain of custody for samples; responsible parties for field/lab work; QA/QC checks performed on data
- **Source citations:** Reference all data sources (field logs, lab reports, survey data files) with dates and versions

#### Methods Documentation:
- **Investigation methods:** Boring/sampling methods and equipment; field testing methods; laboratory testing methods and standards
- **Survey methods:** Survey equipment and calibration; positioning methods (GPS/GNSS); datum and coordinate system; accuracy assessment
- **Analysis methods:** Methods used for soil parameter interpretation, pile capacity analysis, scour assessment (cite codes/standards)

#### Assumptions and Limitations:
- **Explicit labeling:** All assumptions shall be explicitly labeled as "ASSUMPTION" in the report
- **Interpretation assumptions:** Assumptions about soil stratigraphy correlation between borings; groundwater/seawater level assumptions; soil parameter selection (e.g., conservative vs representative values)
- **Scope limitations:** Limitations of investigation (e.g., limited number of borings, localized scope); limitations of survey (e.g., survey accuracy, environmental conditions during survey); applicability of findings to design
- **Assumption justification:** Provide engineering rationale for assumptions or state when assumptions are conservative

**ASSUMPTION:** Project procedures or ER define data documentation and QA/QC standards for geotechnical/survey work; specific requirements TBD.

**Source:** Standard geotechnical and survey reporting practice; project-specific requirements TBD from ER

**Rationale:** See `Guidance.md` § Requirement Rationale Map, R-002

**Verification:** See `Procedure.md` § Requirement Coverage Map, R-002

---

### R-003 — QA/QC and Review

**Requirement:** The report package shall include evidence of appropriate quality assurance/quality control (QA/QC) and technical review prior to issue.

**QA/QC requirements:**
- **Field QA/QC:** Field QA/QC procedures for borings/soundings/survey (e.g., duplicate tests, calibration checks, survey checkpoints)
- **Laboratory QA/QC:** Laboratory QA/QC procedures and certifications (e.g., laboratory accreditation, duplicate tests, blind samples)
- **Data validation:** Data validation checks performed to identify and resolve anomalies or errors in field/lab/survey data
- **Documentation:** QA/QC procedures and results documented in report or appendices

**Technical review:**
- **Internal technical review:** Report reviewed by senior geotechnical engineer or discipline lead for technical adequacy, completeness, and reasonableness
- **Independent check (if required):** Independent check by qualified engineer not involved in original work (confirm requirement from ER or project QA plan)
- **Review documentation:** Review comments documented; originator resolves comments and updates report; reviewer signs off when satisfied

**Professional seal (if required):** Report sealed (stamped and signed) by Professional Engineer (P.Eng.) or Professional Geoscientist (P.Geo.) licensed in British Columbia if required by ER or regulatory requirements. **TBD** *(confirm requirement from ER or BC regulations)*

**ASSUMPTION:** QA/QC and review procedures are required per project QA plan or ER; specific procedures TBD.

**Source:** Standard geotechnical/survey practice; professional licensing requirements; project-specific requirements TBD from ER and QA plan

**Rationale:** See `Guidance.md` § Requirement Rationale Map, R-003

**Verification:** See `Procedure.md` § Requirement Coverage Map, R-003

---

### R-004 — ER Alignment and Approval Requirements

**Requirement:** Report scope, content, methods, and acceptance criteria shall comply with applicable ER requirements and referenced standards.

**Applicable ER clauses:** **TBD** *(ER Vol 2 Parts 1-2 present as PDFs; clause extraction pending; ER may specify investigation scope, survey requirements, acceptance criteria for approvals)*

**Codes and standards:** Investigations, surveys, and analyses shall comply with codes/standards required by ER. **TBD** *(pending ER clause review; likely: API RP 2A for pile capacity analysis; CFEM for geotechnical design; IHO S-44 or equivalent for hydrographic surveys; confirm from ER)*

**Approval requirements:** Report shall be suitable for submission to Employer and regulatory authorities for approvals (if required by ER or regulations). Include all information required for approval (e.g., regulatory authority may require certain investigation scope, data, or certifications).

**ASSUMPTION:** ER specifies geotechnical/survey requirements and approval process; specific ER clauses TBD.

**Source:** Decomposition line 284 (implicit approval requirement: "required for design verification and approvals"); ER requirements TBD

**Rationale:** See `Guidance.md` § Requirement Rationale Map, R-004

**Verification:** See `Procedure.md` § Requirement Coverage Map, R-004

---

### R-005 — Document Control and Packaging

**Requirement:** The report package shall comply with project document control requirements for numbering, revision control, and issue status.

**Report numbering:** **TBD** *(pending project document control procedures; likely: report type code + discipline + package + sequence, e.g., RPT-MAR-08-001)*

**Revision and issue status:** **TBD** *(typical: Rev 0/1/2 for issued; Rev A/B/C for internal review; confirm from project document control procedures)*

**Report format:** Reports shall include standard elements:
- **Cover page:** Report title, document number, revision, date, project name, prepared by (company/consultant), reviewed by, approved by, professional seal (if required)
- **Table of contents:** With section headings and page numbers
- **Executive summary:** Summary of key findings and recommendations
- **Body of report:** Per content requirements in R-001, R-002, R-003, R-004
- **References:** Standards, codes, and references cited
- **Appendices:** Field logs, lab results, survey data, calculations, photos, other supporting data

**ASSUMPTION:** Project document control procedures exist and define report numbering, format, and issue requirements; specific requirements TBD.

**Source:** Standard report practice; project-specific requirements TBD from ER and project document control procedures

**Rationale:** See `Guidance.md` § Requirement Rationale Map, R-005

**Verification:** See `Procedure.md` § Requirement Coverage Map, R-005

---

## Standards and References

### Codes and Standards (TBD)

Applicable codes and standards are **TBD** until the relevant ER clauses are extracted. Likely standards for marine geotechnical work and bathymetric surveys (to be confirmed from ER):

- **API RP 2A** — Planning, Designing and Constructing Fixed Offshore Platforms (for pile capacity analysis)
- **Canadian Foundation Engineering Manual (CFEM)** — For geotechnical design and analysis
- **CSA S6** — Canadian Highway Bridge Design Code (for foundation design if applicable)
- **ASTM standards** — For soil/rock testing (e.g., ASTM D1586 for SPT, ASTM D2487 for soil classification)
- **IHO S-44** — IHO Standards for Hydrographic Surveys (for bathymetric survey accuracy and procedures)
- **Transport Canada or Canadian Coast Guard guidelines** — For marine surveys and approvals (if applicable)

**ASSUMPTION:** Canadian and international standards apply; specific editions and clauses TBD from ER.

### Reference Documents

Minimum reference set for report development:

- **Employer's Requirements:** Vol 2 Parts 1-2 (available in repo as PDFs; clause extraction pending)
- **DEL-08.03 Marine Structures Design Calculations** (defines geotechnical parameter needs for design)
- **Project QA Plan** — **TBD** *(location in ER or project procedures TBD)*
- **Project Survey Control Basis** — **TBD** *(datum and coordinate system for bathymetric survey)*

Reference index: `test/execution/PKG-08_Marine_Structures/0_References/_REFERENCE_INDEX.md` *(currently stub; to be populated)*

---

## Verification and Acceptance

### Verification Requirements

Verification requirements are not fully stated in accessible sources within this deliverable folder. The following verification approach is **PROPOSED** pending confirmation from ER and project QA/QC procedures:

1. **Field/lab QA/QC:** Field and laboratory QA/QC procedures performed per standard practice or ER requirements
2. **Data validation:** Data validated for completeness, consistency, and accuracy before analysis
3. **Technical review:** Senior geotechnical engineer or discipline lead reviews report for technical adequacy
4. **Independent check (if required):** Independent checker reviews report (confirm requirement from ER or QA plan)
5. **Professional seal (if required):** P.Eng. or P.Geo. seal applied to report (confirm requirement from ER or BC regulations)
6. **Approval for issue:** Authorized approver signs off on report for issue to Employer

**Required reviews (to be confirmed):** Technical review, independent check (if required), professional seal (if required), approval for issue — **TBD**

### Acceptance Criteria

Acceptance criteria for "issue" status are **TBD** pending ER and project procedures. Typical acceptance criteria (to be confirmed):

- All review comments resolved and dispositioned
- All requirements (R-001 through R-005) verified as met
- QA/QC procedures performed and documented
- Professional seal applied if required
- Report suitable for Employer approval and regulatory submission (if applicable)

### Requirement Verification Map

| Spec ID | Verification Method | Evidence / Record | Status |
|---|---|---|---|
| R-001 | Report completeness check against decomposition artifacts list (line 284) | Both geotechnical investigation report and bathymetric survey report included in package | **TBD** |
| R-002 | Data/method/assumption traceability audit | Field logs, lab reports, survey data files referenced; methods documented; assumptions list | **TBD** |
| R-003 | QA/QC review check | QA/QC procedures documented; technical review sign-off; independent check sign-off (if required); professional seal (if required) | **TBD** |
| R-004 | ER compliance review | ER requirements mapped to report content; codes/standards compliance verified | **TBD** |
| R-005 | Document control compliance check | Report numbering, revision, format compliance verified | **TBD** |

---

## Documentation / Deliverable Outputs

### Expected Report Outputs (Minimum)

Per Decomposition line 284 and this Specification R-001:

- Marine geotechnical investigation report
- Bathymetric survey report

### Associated Records (TBD)

Records to retain with the report package or in project archive:

- Field investigation logs and photos — **TBD** *(typically included as appendices to geotechnical report)*
- Laboratory test results — **TBD** *(typically included as appendices to geotechnical report)*
- Bathymetric survey data files and contour maps — **TBD** *(typically included as appendices to bathymetric survey report or provided as CAD/GIS files)*
- QA/QC records — **TBD**
- Review comments and dispositions — **TBD**
- Professional seal (if required) — **TBD**
- Report transmittal — **TBD**

---

## Sources

- `test/execution/PKG-08_Marine_Structures/1_Working/DEL-08.04_Marine_Geotechnical_Report/_CONTEXT.md`
- `test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md` (lines 271-291: PKG-08 scope statement at line 275; deliverables table; DEL-08.04 at line 284)
- `test/Volume_2_Part_1_Employers_Requirements.pdf` *(present in repo; content not extracted here; clause locations TBD)*
- `test/Volume_2_Part_2_Employers_Requirements.pdf` *(present in repo; content not extracted here; clause locations TBD)*
- Standard geotechnical and survey reporting practice (for data documentation, QA/QC, professional seal requirements)
