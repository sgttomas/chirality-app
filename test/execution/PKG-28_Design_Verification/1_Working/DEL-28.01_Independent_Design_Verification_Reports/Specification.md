# Specification: DEL-28.01 Independent Design Verification Reports

## Scope

This specification defines the requirements for **Independent Design Verification Reports** within **PKG-28 Design Verification**.

**Purpose:** Documents analysis and results for independent design verification reports required for design verification and approvals, supporting **OBJ-6: Regulatory Compliance** — "The Works comply with all permits, codes, and authority requirements."

**Source:** _CONTEXT.md (DEL-28.01 description); Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md (Section 2, OBJ-6; Section 6, Objective-to-Deliverable Mapping)

**Anticipated deliverable artifacts:**
- IDV reports (by discipline/submission stage)

**Scope Inclusions:**
- Independent verification of design calculations, drawings, and specifications across all disciplines
- Verification of compliance with applicable codes, standards, and Employer's Requirements
- Identification of non-compliances and design deficiencies
- Verification of resolution of identified issues
- IDV reports prepared at 30%, 60%, 90%, and IFC design submission stages — **ASSUMPTION**: Standard D&B milestone sequence

**Scope Exclusions:**
- Design work itself (performed under discipline packages PKG-01 through PKG-27, PKG-29 through PKG-36)
- VFPA IP Review process (covered under DEL-28.02)
- Inter-discipline coordination records (covered under DEL-28.03)
- Testing and commissioning verification (covered under PKG-29)

**Source:** Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md (PKG-28 scope: Independent design verification, VFPA IP coordination, inter-discipline coordination; Section 1.2: Scope Focus)

## Requirements

### Functional Requirements

**FR-1: Independent Review**
- IDV shall be performed by qualified third-party reviewers independent of the design team
- Reviewers shall be licensed professional engineers in the applicable discipline and jurisdiction — **TBD**: Specific licensing requirements per discipline
- **Source:** ISO 9001 quality management principles; **ASSUMPTION**: Typical D&B independent verification requirements

**FR-2: Design Stage Coverage**
- IDV reports shall be produced for each major design submission stage: 30%, 60%, 90%, IFC
- Each stage shall verify all design documents issued at that stage
- **TBD**: Specific document lists per stage and discipline
- **Source:** _CONTEXT.md (anticipated artifacts by stage); **ASSUMPTION**: Typical D&B submission sequence

**FR-3: Discipline Coverage**
- IDV shall cover all applicable design disciplines including but not limited to:
  - Civil (site, earthworks, drainage, pavements)
  - Structural (concrete, steel, marine, rail)
  - Mechanical (tanks, piping, equipment)
  - Process (unloading, loading, metering)
  - Electrical (power, lighting, grounding)
  - Instrumentation & Control (I&C, SCADA, safety systems)
  - Fire Protection (detection, suppression)
- **Source:** Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md (Section 4, Package Summary)

**FR-4: Compliance Verification**
- IDV shall verify compliance with:
  - Applicable codes and standards (BC Building Code, CSA, ASME, API, etc.) — **TBD**: Complete code list per discipline
  - Employer's Requirements — **TBD**: Specific ER sections applicable to each discipline
  - Design criteria and design basis documents
  - Regulatory authority requirements (VFPA, municipal, provincial)
- **Source:** Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md (Section 2, OBJ-6); **ASSUMPTION**: Typical regulatory compliance requirements

**FR-5: Finding Documentation**
- Non-compliances and deficiencies shall be documented as numbered findings with:
  - Finding description
  - Affected design document reference
  - Applicable code/standard reference
  - Severity classification (Critical, Major, Minor) — **TBD**: Classification criteria
  - Recommended corrective action
- **ASSUMPTION**: Standard IDV finding format

**FR-6: Closure Verification**
- IDV reports shall verify closure of findings from previous stages
- Design revisions addressing findings shall be reviewed and confirmed compliant
- **ASSUMPTION**: Iterative review process typical of D&B projects

### Performance Requirements

**PR-1: Review Completeness**
- IDV shall review 100% of design documents within scope for each stage
- **TBD**: Sampling approach for large drawing sets, if applicable

**PR-2: Review Timeliness**
- IDV reports shall be issued within **TBD** days of receipt of design submission
- **ASSUMPTION**: Review schedule coordinated with overall project submission schedule (see DEL-27.04)

**PR-3: Reviewer Qualifications**
- Reviewers shall hold professional engineering licenses in applicable jurisdiction (BC) — **TBD**: Specific P.Eng. requirements
- Reviewers shall have minimum **TBD** years of experience in applicable discipline
- **ASSUMPTION**: Reviewer qualification requirements per ISO 9001 and project quality plan

### Interface Requirements

**IR-1: Design Submission Packages**
- IDV reports interface with DEL-27.04 (Design Submission Packages: 30%, 60%, 90%, IFC)
- IDV review scope includes all design documents submitted at each stage
- **Source:** Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md (DEL-27.04 description); **ASSUMPTION**: IDV follows design submissions

**IR-2: Regulatory Submissions**
- IDV reports support regulatory submissions to VFPA, building authorities, and other regulatory bodies
- IDV verification statements may be required for permit applications — **TBD**: Specific regulatory submission requirements
- Related to DEL-28.02 (VFPA IP Review Responses) — **ASSUMPTION**: IDV addresses issues raised during IP review
- **Source:** Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md (PKG-28 scope includes VFPA IP coordination)

**IR-3: Quality Management System**
- IDV process shall comply with project Quality Management Plan — **TBD**: QMP reference
- IDV findings shall be tracked in project quality/corrective action system — **TBD**: Tracking system specification
- **ASSUMPTION**: QMS per ISO 9001

**IR-4: Coordination with Design Teams**
- IDV reviewers shall coordinate with discipline design leads to clarify findings and verify closures
- See `_DEPENDENCIES.md` for dependency tracking (NOT_TRACKED — dependencies coordinated externally)
- **Source:** _DEPENDENCIES.md (NOT_TRACKED mode)

### Quality Requirements

**QR-1: ISO 9001 Compliance**
- All IDV work shall comply with ISO 9001 Quality Management System requirements
- **Source:** Datasheet.md (applicable standards: ISO 9001)

**QR-2: Report Quality**
- IDV reports shall be technically accurate, complete, and clearly written
- Reports shall be checked and approved prior to issue — **TBD**: Specific QA/QC procedures
- **ASSUMPTION**: Standard engineering document QA/QC process

**QR-3: Document Control**
- IDV reports shall be controlled per project document control procedures — **TBD**: Document control system reference
- Revisions shall be tracked and managed — **TBD**: Revision control protocol
- **ASSUMPTION**: Electronic document management system per project standards

## Standards

**Applicable codes and standards (Design discipline):**

- ISO 9001 — Quality Management Systems
- Employer's Requirements — **TBD**: Specific ER sections governing IDV requirements
- **TBD**: Discipline-specific codes and standards to be verified during IDV (e.g., BC Building Code, CSA Standards, ASME, API, IEEE, NFPA)

**Professional Standards:**
- Engineers and Geoscientists BC (EGBC) practice standards — **ASSUMPTION**: Professional practice requirements for BC-registered engineers
- **TBD**: Additional professional practice standards

**Source:** Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md (Section 1.1, Location: Fraser Surrey Terminal, Surrey, BC); **ASSUMPTION**: BC jurisdiction applies

## Verification

**Verification methods for Report deliverables:**

**V-1: Technical Review of IDV Methodology**
- IDV methodology and review checklists shall be reviewed and approved prior to commencement — **TBD**: Approval authority
- **ASSUMPTION**: Methodology review by project quality manager

**V-2: IDV Report Review**
- IDV reports shall be subject to internal QA/QC review prior to issue
- Checker and approver roles — **TBD**: Specific sign-off requirements
- **ASSUMPTION**: Standard engineering document review protocol

**V-3: Finding Tracking and Closure**
- All IDV findings shall be tracked to closure
- Closure verification shall be documented in subsequent stage IDV reports
- **TBD**: Finding tracking system and closure criteria

**V-4: Regulatory Acceptance**
- IDV reports may be subject to review by regulatory authorities (VFPA, building officials)
- Acceptance criteria per authority requirements — **TBD**
- **Source:** Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md (Section 2, OBJ-6: Regulatory Compliance)

**Acceptance criteria:**
- IDV reports complete and compliant with this specification
- All critical and major findings identified and tracked
- IDV reviewer qualifications verified
- Report approved by D&B Contractor project management — **TBD**: Specific approval authority
- **Source:** _CONTEXT.md (responsible party: D&B Contractor)

## Documentation

**Required documentation outputs:**
- IDV reports (by discipline/submission stage): IDV-[Discipline]-[Stage] (e.g., IDV-CIVIL-30, IDV-STRUCT-60, IDV-MECH-90, IDV-ELEC-IFC)
- **Source:** _CONTEXT.md (anticipated artifacts); Datasheet.md (report series naming convention)

**Documentation requirements:**

**D-1: Report Content**
Each IDV report shall include (minimum):
- Executive summary
- Review scope and objectives
- Methodology and review criteria
- Design documents reviewed (list with revision numbers)
- Code and standard compliance checklist
- Findings (non-compliances and recommendations)
- Closure verification (for findings from previous stages)
- Reviewer qualifications and certifications
- Verification statement and sign-off
- **ASSUMPTION**: Standard IDV report format

**D-2: Document Control**
- All IDV reports shall comply with project document control procedures
- Document numbering: **TBD** — **ASSUMPTION**: Per project numbering system
- Revision control: **TBD** — **ASSUMPTION**: Revision tracking per document management system
- Format: **TBD** — **ASSUMPTION**: PDF for issued reports, editable source for working documents
- **Source:** Datasheet.md (report format TBD)

**D-3: Record Management**
- IDV reports shall be filed in project document management system
- Filing location: `2_Checking/` (during review) → `3_Issued/` (upon approval)
- Retention: **TBD** — **ASSUMPTION**: Project records retention per contract requirements
- **Source:** Procedure.md (record management section)

**D-4: Submittal**
- IDV reports shall be submitted to Employer as part of or alongside design submission packages (DEL-27.04)
- Submittal format and protocol — **TBD**
- **Source:** Datasheet.md (related deliverable: DEL-27.04)
