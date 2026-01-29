# Specification: DEL-14.05 Process Piping Installation & Test Records

## Scope

QA/QC documentation providing evidence of completion, inspection, and testing per ASME B31.3 for PKG-14 process piping (source: Decomposition DEL-14.05; attributes: Datasheet.md Record Type; rationale: Guidance.md Purpose).

**Record outputs** (source: Decomposition DEL-14.05; attributes: Datasheet.md Attributes; construction: Datasheet.md Construction section; procedure: Procedure.md Steps 1-3):
- Material certificates (MTRs) (construction: Datasheet.md Construction item 1; procedure: Procedure.md Step 1; examples: Guidance.md Examples item 1)
- Weld inspection records (construction: Datasheet.md Construction item 2; procedure: Procedure.md Step 2; examples: Guidance.md Examples item 2)
- Hydrostatic test records (construction: Datasheet.md Construction item 3; procedure: Procedure.md Step 3; examples: Guidance.md Examples item 3)

## Requirements

### Functional Requirements

(construction: Datasheet.md Construction section; rationale: Guidance.md Principles items 1-4; procedure: Procedure.md Steps 1-4):
- FR-1: Document material traceability (MTRs for all pressure-containing components) (construction: Datasheet.md Construction item 1; quality standard: Datasheet.md Quality Standard; rationale: Guidance.md Principles item 1; quality: QR-1; procedure: Procedure.md Step 1; verification: Verification - Material certificates; documentation: Documentation - Record types; examples: Guidance.md Examples item 1; cross-reference DEL-14.02, DEL-14.04)
- FR-2: Document weld quality (visual inspection, NDE per ASME B31.3) (construction: Datasheet.md Construction item 2; quality standard: Datasheet.md Quality Standard; rationale: Guidance.md Principles item 2; performance: PR-2; quality: QR-1; procedure: Procedure.md Step 2; verification: Verification - Weld inspection; documentation: Documentation - Record types; examples: Guidance.md Examples item 2; cross-reference DEL-14.01, DEL-14.02)
- FR-3: Document hydrostatic testing (test pressure, duration, results) (construction: Datasheet.md Construction item 3; quality standard: Datasheet.md Quality Standard; rationale: Guidance.md Principles item 3; performance: PR-3; procedure: Procedure.md Step 3; verification: Verification - Hydrostatic test; documentation: Documentation - Record types; examples: Guidance.md Examples item 3; cross-reference DEL-14.03)
- FR-4: Provide evidence of ASME B31.3 compliance for facility startup (quality standard: Datasheet.md Quality Standard; rationale: Guidance.md Principles item 4; interface: IR-2; quality: QR-3; procedure: Procedure.md Step 4, Step 5; verification: Verification - Acceptance; cross-reference PKG-33, PKG-34)

### Performance Requirements

(rationale: Guidance.md Principles items 1-3; procedure: Procedure.md Steps 1-3):
- PR-1: Material certificates verify material specifications per DEL-14.02 (construction: Datasheet.md Construction item 1; requirements: FR-1; interface: IR-1; rationale: Guidance.md Principles item 1; considerations: Guidance.md Considerations - Material Certificates; quality: QR-1; procedure: Procedure.md Step 1; verification: Verification - Material certificates; cross-reference DEL-14.02, DEL-14.04)
- PR-2: Weld inspection per ASME B31.3 acceptance criteria (construction: Datasheet.md Construction item 2; requirements: FR-2; quality standard: Datasheet.md Quality Standard; rationale: Guidance.md Principles item 2; standards: Standards section; considerations: Guidance.md Considerations - Weld Inspection; trade-offs: Guidance.md Trade-offs item 2; procedure: Procedure.md Step 2; verification: Verification - Weld inspection; examples: Guidance.md Examples item 2)
- PR-3: Hydrostatic test per ASME B31.3 (1.5 × design pressure, 10 min minimum) (construction: Datasheet.md Construction item 3 - Test pressure, duration; requirements: FR-3; quality standard: Datasheet.md Quality Standard; rationale: Guidance.md Principles item 3; standards: Standards section; considerations: Guidance.md Considerations - Hydrostatic Testing; procedure: Procedure.md Step 3; verification: Verification - Hydrostatic test, Acceptance; examples: Guidance.md Examples item 3; cross-reference DEL-14.03, DEL-14.04)

### Interface Requirements

(rationale: Guidance.md Principles items 1, 4; considerations: Guidance.md Considerations sections; procedure: Procedure.md Prerequisites, Steps 1, 4, 5):
- IR-1: Material certificates match DEL-14.04 (line list and material data sheets) (construction: Datasheet.md Construction item 1 - Traceability; requirements: FR-1; performance: PR-1; rationale: Guidance.md Principles item 1; considerations: Guidance.md Considerations - Material Certificates; quality: QR-2; procedure: Procedure.md Step 1, Step 4; verification: Verification - Material certificates; examples: Guidance.md Examples item 1; cross-reference DEL-14.02, DEL-14.04)
- IR-2: Test records coordinate with commissioning (PKG-33, PKG-34) (requirements: FR-4; rationale: Guidance.md Principles item 4; considerations: Guidance.md Considerations - Regulatory Compliance; procedure: Procedure.md Step 5; cross-reference PKG-33, PKG-34)

### Quality Requirements

(quality standard: Datasheet.md Quality Standard; rationale: Guidance.md Principles items 1-4; procedure: Procedure.md Steps 1-5):
- QR-1: All records reviewed and approved by QA/QC (construction: Datasheet.md Construction items 1, 2, 3; requirements: FR-1, FR-2, FR-3; performance: PR-1, PR-2; rationale: Guidance.md Principles items 1, 2, 3; trade-offs: Guidance.md Trade-offs item 1; procedure: Procedure.md Step 1, Step 2, Step 3, Step 4; verification: Verification sections)
- QR-2: Records filed and archived per project document control (attributes: Datasheet.md Retention Period; interface: IR-1; rationale: Guidance.md Principles item 4; considerations: Guidance.md Considerations - Regulatory Compliance; procedure: Procedure.md Step 4, Step 5; documentation: Documentation - Storage, Retention)
- QR-3: Compliance package for regulatory authorities **TBD** (requirements: FR-4; considerations: Guidance.md Considerations - Regulatory Compliance; procedure: Procedure.md Step 5; documentation: Documentation section)

## Standards

(quality standard: Datasheet.md Quality Standard; rationale: Guidance.md Principles items 2, 3; procedure: Procedure.md Prerequisites; cross-reference DEL-14.02):
- ASME B31.3 Chapter VI — Inspection, Examination, Testing (construction: Datasheet.md Construction items 2, 3; requirements: FR-2, FR-3; performance: PR-2, PR-3; quality: QR-1; rationale: Guidance.md Principles items 2, 3; procedure: Procedure.md Prerequisites, Step 2, Step 3; examples: Guidance.md Principles items 2, 3; referenced in DEL-14.01, DEL-14.02)
- AWS D1.1 or equivalent — welding acceptance criteria (construction: Datasheet.md Construction item 2; requirements: FR-2; performance: PR-2; rationale: Guidance.md Principles item 2; procedure: Procedure.md Step 2; cross-reference DEL-14.02)
- Project Quality Management Plan **TBD** (quality: QR-1; procedure: Procedure.md Prerequisites; cross-reference DEL-14.02)

## Verification

(quality: QR-1; procedure: Procedure.md Step 4, Verification section; verification table):
- Material certificates verified by QA/QC (heat numbers, specifications) (requirements: FR-1; performance: PR-1; construction: Datasheet.md Construction item 1; interface: IR-1; rationale: Guidance.md Principles item 1; quality: QR-1; procedure: Procedure.md Step 1; verification table; cross-reference DEL-14.04)
- Weld inspection records signed by qualified inspector (requirements: FR-2; performance: PR-2; construction: Datasheet.md Construction item 2; rationale: Guidance.md Principles item 2; quality: QR-1; procedure: Procedure.md Step 2; verification table)
- Hydrostatic test witnessed and signed by QA/QC (requirements: FR-3; performance: PR-3; construction: Datasheet.md Construction item 3; rationale: Guidance.md Principles item 3; quality: QR-1; procedure: Procedure.md Step 3; verification table)

**Acceptance:** All piping systems tested and accepted per ASME B31.3 (requirements: FR-4; quality standard: Datasheet.md Quality Standard; performance: PR-3; rationale: Guidance.md Principles item 3; quality: QR-1; procedure: Procedure.md Step 4; verification table)

## Documentation

**Record types** (construction: Datasheet.md Construction section; requirements: FR-1, FR-2, FR-3; procedure: Procedure.md Steps 1-3):
- Material Test Reports (MTRs) (construction: Datasheet.md Construction item 1; requirements: FR-1; procedure: Procedure.md Step 1; examples: Guidance.md Examples item 1)
- Weld maps and inspection records (construction: Datasheet.md Construction item 2; requirements: FR-2; procedure: Procedure.md Step 2; examples: Guidance.md Examples item 2)
- NDE reports (radiography, ultrasonic, etc.) (construction: Datasheet.md Construction item 2; requirements: FR-2; performance: PR-2; procedure: Procedure.md Step 2; examples: Guidance.md Examples item 2)
- Hydrostatic test certificates (construction: Datasheet.md Construction item 3; requirements: FR-3; performance: PR-3; procedure: Procedure.md Step 3; examples: Guidance.md Examples item 3)
- Final acceptance certificate (requirements: FR-4; quality: QR-1; procedure: Procedure.md Step 4; verification: Verification - Acceptance)

**Storage:** `3_Issued/` → Project archive (attributes: Datasheet.md Retention Period; quality: QR-2; procedure: Procedure.md Step 5; records: Procedure.md Records section)

**Retention:** Permanent (facility life + regulatory period) (attributes: Datasheet.md Retention Period; quality: QR-2; considerations: Guidance.md Considerations - Regulatory Compliance; procedure: Procedure.md Step 5)
