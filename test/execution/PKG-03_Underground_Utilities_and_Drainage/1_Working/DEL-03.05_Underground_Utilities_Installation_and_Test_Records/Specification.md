# Specification: DEL-03.05 Underground Utilities Installation & Test Records

## Scope
Documents the evidence of completion, inspection, and testing for storm drainage, OWS, and duct bank systems in PKG-03 as required by the decomposition scope and Employer's Requirements (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:202).

## Requirements

### Functional Requirements
- Record pressure test details, CCTV inspection findings, and as-built survey confirmations that prove compliance with the civil installation scope.
- Log deviations or nonconformances, including remedial actions and approvals, so downstream reviewers can confirm resolutions.
- Align the records with the Datasheet attributes that define coverage and storage expectations (Datasheet.md: Attributes).

### Performance Requirements
- Testing must demonstrate that installed systems meet the hydraulic, structural, and environmental performance expectations cited in the Employer's Requirements (Source: test/Volume_2_Part_2_Employers_Requirements.pdf).
- CCTV inspections should detect and document defects in storm pipe and culvert installations to support future remediation recommendations (Source: `_CONTEXT.md` for anticipated artifact). 
- Reflect the Guidance trade-offs (Guidance.md: Trade-offs) when prioritizing which defects require immediate remediation versus monitoring.

### Interface Requirements
- Coordinate test record formats with DEL-03.01 (Drawings) and DEL-03.04 (Data Sheets) so that field observations reference the correct drawing numbers and material codes.
- Deliver records per project coordination procedures even though dependencies are not tracked in `_DEPENDENCIES.md` (NOT_TRACKED mode).
- Reference Procedure.md to ensure the sequencing (pressure tests before CCTV before surveys) matches the documented field workflow.

### Quality Requirements
- Records follow the Quality Management Plan prescribed in Volume 2 Part 1 (Source: test/Volume_2_Part_1_Employers_Requirements.pdf), including sign-offs, reviewer initials, and storage instructions.
- Records should include data traceability to the verification steps outlined in DEL-03.02 (Specification) and DEL-03.03 (Calculations).

## Standards
- Employer's Requirements Volume 2 Part 1 and Part 2 describe QA/QC and inspection expectations for underground utilities (Source: test/Volume_2_Part_1_Employers_Requirements.pdf & test/Volume_2_Part_2_Employers_Requirements.pdf).
- Inspection coding and CCTV reporting conventions follow the project standard where available; specifics remain TBD until the relevant sections of the Employer's Requirements are extracted.

## Verification
- Each pressure test, CCTV log, and as-built survey is validated by QA/QC per the project Quality Management Plan.
- Verification includes reviewing calibration certificates for test equipment and cross-referencing survey data with the issued drawing set.
- Update the Datasheet metadata to reflect verification outcomes and tie back to the Procedure's verification checkpoints so the Drawing Set sees the QA trail (Datasheet.md: Construction; Procedure.md: Verification).

## Documentation
- Records include pressure test records, CCTV inspection records, and as-built survey records as listed in `_CONTEXT.md` (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:202).
- Archive records in the document control system and reference them during commissioning packages.

## Cross-Document Notes

- Datasheet: The Specification’s requirements dictate which records are captured; match those record types to the Datasheet’s coverage field for clarity (Datasheet.md: Conditions, Attributes).
- Guidance: Guidance instructions about referencing drawing numbers and materials inform how the Specification structures interface clauses rather than leaving them implicit (Guidance.md: Considerations).
- Procedure: Sequence and verification details in Procedure.md show how each Specification clause gets QA-checked before finalization, enabling traceability (Procedure.md: Steps, Verification).
