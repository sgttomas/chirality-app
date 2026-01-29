# Specification: DEL-08.05 Marine Structures Installation & Test Records

## Scope

This document defines **minimum requirements for the deliverable artifact itself** (the Marine Structures Installation & Test Records package): required record types, format and traceability requirements, acceptance criteria, and packaging for completion verification and close-out.

**Deliverable description (source-anchored):** Provides evidence of completion, inspection, and testing for marine structures. *(Source: Decomposition line 285 + `_CONTEXT.md`)*

**Package scope context (source-anchored):** PKG-08 covers piling, access trestle, loading platform structure, catwalk, and abutments. *(Source: Decomposition line 275)*

---

## Requirements (Deliverable Content)

### R-001 — Record Package Coverage (Minimum)

**Requirement:** The records package shall include, at minimum, the following anticipated record types as listed in the decomposition deliverables table (line 285):

- Pile driving records
- Pile integrity test records
- Weld inspection records

**Additional scope coverage requirement:** All inspection and testing requirements specified in DEL-08.02 Marine Structures Technical Specification shall have corresponding records in the package. Any specified inspection/test without corresponding records shall be flagged as non-conformance.

**Source:** Decomposition line 285 (anticipated artifacts); DEL-08.02 specification requirements

**Rationale:** See `Guidance.md` § Requirement Rationale Map, R-001

**Verification:** See `Procedure.md` § Requirement Coverage Map, R-001

---

### R-002 — Record Format, Traceability, and Completeness

**Requirement:** Each record shall provide sufficient information for verification, acceptance, and traceability:

#### Record Identification and Traceability:
- **Unique identification:** Each record shall have unique identification
- **Work identification:** Identify what was inspected/tested (pile number, weld ID, structural member, location)
- **Date and personnel:** Date/time, inspector/tester name, qualifications
- **Witness identification (if applicable):** Third-party witness name and organization

#### Record Content:
- **Procedure reference:** Reference to inspection/test procedure or standard
- **Acceptance criteria:** State acceptance criteria
- **Results:** Record results and pass/fail determination
- **Non-conformances:** Document defects and disposition
- **Sign-offs:** Required signatures

#### Supporting Documentation:
- **Calibration certificates:** Equipment calibration (valid and current)
- **Material certificates:** MTRs, mill certificates
- **Qualifications:** Personnel certifications
- **Procedures:** Approved WPS, inspection procedures

**Record format:** **TBD** *(from ER or project QA procedures)*

**ASSUMPTION:** Project QA/QC procedures define record formats; specific requirements TBD.

**Source:** Standard QA/QC practice; project-specific requirements TBD from ER

**Rationale:** See `Guidance.md` § Requirement Rationale Map, R-002

**Verification:** See `Procedure.md` § Requirement Coverage Map, R-002

---

### R-003 — Inspection and Test Plan (ITP) Alignment

**Requirement:** Records shall be collected per an approved Inspection and Test Plan (ITP).

**ITP Requirements:**
- **Inspection/test activities:** List all inspections/tests required
- **Hold points and witness points:** Define hold/witness points
- **Procedures and acceptance criteria:** Reference procedures and criteria
- **Responsible parties:** Define who performs and who witnesses
- **Record requirements:** Define required records

**ITP approval:** **TBD** *(from ER)*

**ASSUMPTION:** ER or project QA plan requires an ITP; specific format TBD.

**Source:** Standard construction QA/QC practice; requirements TBD from ER

**Rationale:** See `Guidance.md` § Requirement Rationale Map, R-003

**Verification:** See `Procedure.md` § Requirement Coverage Map, R-003

---

### R-004 — ER and Code Compliance

**Requirement:** Records shall demonstrate compliance with ER requirements and codes/standards.

**Applicable ER clauses:** **TBD**

**Codes compliance:** **TBD** *(likely: CSA W59, API RP 2A, ASTM standards)*

**Acceptance criteria:** All inspections/tests shall meet acceptance criteria; non-conformances dispositioned.

**Source:** Decomposition line 285; ER requirements TBD; codes TBD from DEL-08.02

**Rationale:** See `Guidance.md` § Requirement Rationale Map, R-004

**Verification:** See `Procedure.md` § Requirement Coverage Map, R-004

---

### R-005 — Record Storage, Retention, and Close-Out Package

**Requirement:** Records shall be properly stored, retained, and packaged for close-out.

**Record storage:** Secure physical/electronic storage; indexed for retrieval

**Record retention:** **TBD** *(from ER; typical: life of project plus regulatory period)*

**Close-out package:**
- Record register/index
- Organized records
- Summary report
- Transmittal

**ASSUMPTION:** ER defines storage, retention, close-out requirements; specific requirements TBD.

**Source:** Standard close-out practice; requirements TBD from ER

**Rationale:** See `Guidance.md` § Requirement Rationale Map, R-005

**Verification:** See `Procedure.md` § Requirement Coverage Map, R-005

---

## Standards and References

**Codes and Standards (TBD):** CSA W59, AWS D1.1, API RP 2A, ASTM, CGSB/ASNT, SSPC/NACE, CSA S16/S6

**Reference Documents:** ER Vol 2 Parts 1-2, DEL-08.01, DEL-08.02, DEL-08.04, Project QA Plan, ITP

---

## Verification and Acceptance

**Verification Requirements (PROPOSED):**
1. Real-time verification during construction
2. Record completeness review
3. ITP compliance check
4. Close-out package review

**Acceptance Criteria (TBD):** All ITP points satisfied, acceptance criteria met, non-conformances dispositioned, records complete, Employer acceptance

### Requirement Verification Map

| Spec ID | Verification Method | Evidence / Record | Status |
|---|---|---|---|
| R-001 | Completeness check vs DEL-08.02 | Record index | **TBD** |
| R-002 | Format/traceability audit | Records reviewed | **TBD** |
| R-003 | ITP compliance check | ITP satisfied | **TBD** |
| R-004 | Compliance review | Criteria met, NCRs dispositioned | **TBD** |
| R-005 | Storage/close-out check | Package complete, Employer acceptance | **TBD** |

---

## Documentation / Deliverable Outputs

**Expected Outputs (Minimum):** Pile driving records, pile integrity test records, weld inspection records

**Additional Outputs:** Material certificates, erection records, coating inspection, dimensional inspection

**Close-Out Package:** Record register, organized records, summary report, transmittal

---

## Sources

- `test/execution/PKG-08_Marine_Structures/1_Working/DEL-08.05_Marine_Structures_Installation_and_Test_Records/_CONTEXT.md`
- `test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md` (lines 271-291: PKG-08 scope at line 275; deliverables table; DEL-08.05 at line 285)
- `test/Volume_2_Part_1_Employers_Requirements.pdf` *(present in repo; content not extracted here; clause locations TBD)*
- `test/Volume_2_Part_2_Employers_Requirements.pdf` *(present in repo; content not extracted here; clause locations TBD)*
- Standard construction QA/QC practice
