# Datasheet: DEL-14.05 Process Piping Installation & Test Records

## Identification

| Field | Value |
|-------|-------|
| Deliverable ID | DEL-14.05 |
| Name | Process Piping Installation & Test Records |
| Package | PKG-14 Process Piping |
| Discipline | Mechanical |
| Type | Record |
| Responsible | D&B Contractor (QA/QC) |
| Status | INITIALIZED |

## Attributes

| Attribute | Value |
|-----------|-------|
| Record Type | QA/QC documentation (material certificates, inspection records, test records) (scope: Specification.md Scope; rationale: Guidance.md Purpose; procedure: Procedure.md Purpose) |
| Scope | All process piping in PKG-14 (headers, export lines, recycle lines, nitrogen distribution) (scope: Specification.md Scope; applicability: Conditions below; cross-reference DEL-14.01, DEL-14.04) |
| Quality Standard | ASME B31.3 Chapter VI (Inspection, Examination, Testing) (requirements: Specification.md Standards section; rationale: Guidance.md Principles items 2, 3; procedure: Procedure.md Prerequisites; referenced in DEL-14.01, DEL-14.02) |
| Retention Period | Permanent — facility life + regulatory retention requirements (considerations: Guidance.md Considerations - Regulatory Compliance; procedure: Procedure.md Step 5, Records section) |

## Conditions

**Applicability:** All installed process piping in PKG-14 (scope: Specification.md Scope; attributes: Scope; cross-reference DEL-14.01, DEL-14.04)

**Documentation Requirements:**
- Material traceability (MTRs with heat numbers) (construction: Construction item 1; requirements: Specification.md FR-1, PR-1; rationale: Guidance.md Principles item 1; procedure: Procedure.md Step 1; cross-reference DEL-14.02, DEL-14.04)
- Weld quality verification (visual and NDE per ASME B31.3) (construction: Construction item 2; requirements: Specification.md FR-2, PR-2; quality standard: Attributes; rationale: Guidance.md Principles item 2; procedure: Procedure.md Step 2; cross-reference DEL-14.02)
- Hydrostatic testing (pressure integrity verification) (construction: Construction item 3; requirements: Specification.md FR-3, PR-3; quality standard: Attributes; rationale: Guidance.md Principles item 3; procedure: Procedure.md Step 3; cross-reference DEL-14.02)

## Construction

**Anticipated artifacts** (source: Decomposition DEL-14.05; scope: Specification.md Scope; procedure: Procedure.md Steps 1-3; documentation: Specification.md Documentation):

**1. Material Certificates (MTRs):**
- Material Test Reports for all pressure-containing components (pipe, fittings, flanges, bolting) (requirements: Specification.md FR-1, PR-1; quality: Specification.md QR-1; rationale: Guidance.md Principles item 1; considerations: Guidance.md Considerations - Material Certificates; procedure: Procedure.md Step 1; verification: Specification.md Verification - Material certificates; documentation: Specification.md Documentation - Record types; examples: Guidance.md Examples item 1; cross-reference DEL-14.02, DEL-14.04)
- Verify material grade, heat number, mechanical properties, chemical composition (requirements: Specification.md PR-1; rationale: Guidance.md Principles item 1; considerations: Guidance.md Considerations - Material Certificates; procedure: Procedure.md Step 1; verification: Specification.md Verification - Material certificates)
- Traceability from procurement through installation (requirements: Specification.md FR-1; rationale: Guidance.md Principles item 1; considerations: Guidance.md Considerations - Material Certificates; quality: Specification.md QR-2; procedure: Procedure.md Step 1; cross-reference DEL-14.02)

**2. Weld Inspection Records:**
- Visual inspection records (100% of welds) (requirements: Specification.md FR-2, PR-2; quality standard: Attributes - ASME B31.3 Chapter VI; rationale: Guidance.md Principles item 2; considerations: Guidance.md Considerations - Weld Inspection; procedure: Procedure.md Step 2; verification: Specification.md Verification - Weld inspection; documentation: Specification.md Documentation - Record types; examples: Guidance.md Examples item 2)
- Non-destructive examination (NDE) records per ASME B31.3 requirements (radiography, ultrasonic, etc.) (requirements: Specification.md FR-2, PR-2; quality standard: Attributes; rationale: Guidance.md Principles item 2; standards: Specification.md Standards section; considerations: Guidance.md Considerations - Weld Inspection; trade-offs: Guidance.md Trade-offs item 2; procedure: Procedure.md Step 2; verification: Specification.md Verification - Weld inspection; documentation: Specification.md Documentation - Record types; examples: Guidance.md Examples item 2; cross-reference DEL-14.02)
- Weld maps showing weld locations and numbers (requirements: Specification.md FR-2; considerations: Guidance.md Considerations - Weld Inspection; procedure: Procedure.md Step 2; documentation: Specification.md Documentation - Record types; examples: Guidance.md Examples item 2; cross-reference DEL-14.01)
- Welder qualifications and procedure qualifications (WPS/PQR) (requirements: Specification.md FR-2; rationale: Guidance.md Principles item 2; standards: Specification.md Standards section; considerations: Guidance.md Considerations - Weld Inspection; procedure: Procedure.md Step 2; verification: Specification.md Verification - Weld inspection; documentation: Specification.md Documentation - Record types; cross-reference DEL-14.02)

**3. Hydrostatic Test Records:**
- Test certificates documenting pressure testing per ASME B31.3 (requirements: Specification.md FR-3, PR-3; quality standard: Attributes; rationale: Guidance.md Principles item 3; standards: Specification.md Standards section; procedure: Procedure.md Step 3; verification: Specification.md Verification - Hydrostatic test; documentation: Specification.md Documentation - Record types; examples: Guidance.md Examples item 3)
- Test pressure (typically 1.5 × design pressure), duration (minimum 10 minutes), results (pass/fail) (requirements: Specification.md PR-3; rationale: Guidance.md Principles item 3; considerations: Guidance.md Considerations - Hydrostatic Testing; procedure: Procedure.md Step 3; verification: Specification.md Verification - Acceptance; examples: Guidance.md Examples item 3; cross-reference DEL-14.03, DEL-14.04)
- System boundaries and isolation points for each test (considerations: Guidance.md Considerations - Hydrostatic Testing; procedure: Procedure.md Step 3; examples: Guidance.md Examples item 3; cross-reference DEL-14.01)

## References

**Project References:**
- Decomposition file: /Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md
- ER Volume 2 Part 1, Part 2 (procedure: Procedure.md Prerequisites; standards: Specification.md Standards section)

**Applicable Standards:**
- ASME B31.3 Chapter VI — Inspection, Examination, and Testing (quality standard: Attributes; construction: Construction items 2, 3; requirements: Specification.md Standards section; rationale: Guidance.md Principles items 2, 3; procedure: Procedure.md Prerequisites, Steps 2-3; examples: Guidance.md Principles items 2, 3)
- AWS D1.1 or equivalent — welding acceptance criteria (construction: Construction item 2; requirements: Specification.md Standards section; rationale: Guidance.md Principles item 2; procedure: Procedure.md Step 2; cross-reference DEL-14.02)
- Project Quality Management Plan **TBD** (requirements: Specification.md QR-1, Standards section; procedure: Procedure.md Prerequisites; cross-reference DEL-14.02)

**Cross-references:**
- DEL-14.02 (Process Piping Technical Specification) — quality requirements and material specifications (construction: Construction items 1, 2; interface: Specification.md IR-1; requirements: Specification.md FR-1, PR-1; quality: Specification.md QR-1; rationale: Guidance.md Principles items 1, 2; considerations: Guidance.md Considerations - Material Certificates, Weld Inspection; procedure: Procedure.md Prerequisites, Step 1, Step 2; verification: Specification.md Verification - Material certificates)
- DEL-14.04 (Process Piping Data Sheet Package) — line list for record organization and completeness verification (interface: Specification.md IR-1; construction: Construction item 1 - Traceability; rationale: Guidance.md Principles item 4; considerations: Guidance.md Considerations - Material Certificates; procedure: Procedure.md Step 1, Step 4; verification: Specification.md Verification - Material certificates; examples: Guidance.md Examples item 1)
- DEL-14.01 (Process Piping Design Drawings) — weld maps reference drawing isometrics (construction: Construction item 2 - Weld maps; considerations: Guidance.md Considerations - Weld Inspection; procedure: Procedure.md Step 2; examples: Guidance.md Examples item 2)
- DEL-14.03 (Process Piping Design Calculations) — design pressure for hydrostatic test (construction: Construction item 3 - Test pressure; requirements: Specification.md PR-3; rationale: Guidance.md Principles item 3; procedure: Procedure.md Step 3)
- PKG-33, PKG-34 (Commissioning) — records required for system turnover (interface: Specification.md IR-2; requirements: Specification.md FR-4; rationale: Guidance.md Principles item 4; considerations: Guidance.md Considerations - Regulatory Compliance; procedure: Procedure.md Step 5)

**Related Project Objectives:**
- OBJ-1: Safe & Reliable Operation — QA/QC records ensure piping installed to code requirements (requirements: Specification.md FR-4; rationale: Guidance.md Principles items 1, 2, 3; procedure: Procedure.md Purpose)
- OBJ-6: Regulatory Compliance — records provide evidence of compliance for permitting/approvals (requirements: Specification.md QR-3; considerations: Guidance.md Considerations - Regulatory Compliance; procedure: Procedure.md Step 5)
