# Specification: DEL-14.04 Process Piping Data Sheet Package

## Scope

Defines and substantiates process piping through a line list and material data sheets per ER requirements (source: Decomposition DEL-14.04; attributes: Datasheet.md Data Sheet Type; rationale: Guidance.md Purpose).

**Data sheet outputs** (source: Decomposition DEL-14.04; attributes: Datasheet.md Attributes; construction: Datasheet.md Construction section; procedure: Procedure.md Steps 2, 4):
- Line list (register of all piping lines with design data) (construction: Datasheet.md Construction item 1; requirements: FR-1, FR-2; procedure: Procedure.md Step 2; examples: Guidance.md Examples items 1, 2)
- Piping material data sheets (material specifications by class) (construction: Datasheet.md Construction item 2; requirements: FR-4, FR-5; procedure: Procedure.md Step 4; examples: Guidance.md Examples item 3)

## Requirements

### Functional Requirements

**Line List** (construction: Datasheet.md Construction item 1; rationale: Guidance.md Principles item 1; procedure: Procedure.md Steps 1-2):
- FR-1: List all piping lines in PKG-14 (headers, export lines, recycle, nitrogen) (applicability: Datasheet.md Applicability; scope: Specification.md Scope; rationale: Guidance.md Principles item 1; considerations: Guidance.md Considerations - Line List Development; quality: QR-1; procedure: Procedure.md Step 1, Step 2; verification: Verification; cross-reference DEL-14.01)
- FR-2: Include line number, service, from/to, size, material class, design P/T, insulation (construction: Datasheet.md Construction item 1 - Typical columns; rationale: Guidance.md Principles item 1; considerations: Guidance.md Considerations - Line List Development; trade-offs: Guidance.md Trade-offs item 2; procedure: Procedure.md Step 2; documentation: Documentation - Line list columns; examples: Guidance.md Examples item 1)
- FR-3: Provide traceability to P&IDs (DEL-14.01) and specifications (DEL-14.02) (construction: Datasheet.md Construction item 1 - Provides traceability; interface: IR-1, IR-2; rationale: Guidance.md Principles item 3; considerations: Guidance.md Considerations - Coordination; procedure: Procedure.md Step 1, Step 2; verification: Verification; cross-reference DEL-14.01, DEL-14.02)

**Piping Material Data Sheets** (construction: Datasheet.md Construction item 2; rationale: Guidance.md Principles item 2; procedure: Procedure.md Steps 3-4):
- FR-4: Define material classes for piping systems (attributes: Datasheet.md Material Classes; construction: Datasheet.md Material Class Examples; rationale: Guidance.md Principles item 2; considerations: Guidance.md Considerations - Material Data Sheets; trade-offs: Guidance.md Trade-offs item 1; procedure: Procedure.md Step 3; examples: Guidance.md Examples item 3)
- FR-5: Specify pipe, fittings, flanges, gaskets, bolting for each class (construction: Datasheet.md Construction item 2 - Each class specifies; requirements: FR-4; rationale: Guidance.md Principles item 2; considerations: Guidance.md Considerations - Material Data Sheets; procedure: Procedure.md Step 4; documentation: Documentation - Material data sheets; examples: Guidance.md Examples item 3)
- FR-6: Cross-reference DEL-14.02 (technical specification) (construction: Datasheet.md Construction item 2 - Cross-reference; interface: IR-2; rationale: Guidance.md Principles item 3; considerations: Guidance.md Considerations - Coordination; procedure: Procedure.md Step 4; verification: Verification; examples: Guidance.md Examples item 3)

### Performance Requirements

(rationale: Guidance.md Principles items 2, 3; interface: Specification.md Interface Requirements; procedure: Procedure.md Prerequisites, Step 2):
- PR-1: Design conditions from DEL-14.03 calculations (conditions: Datasheet.md Design pressure/temperature; interface: IR-3; rationale: Guidance.md Principles item 3; procedure: Procedure.md Prerequisites, Step 2; verification: Verification; cross-reference DEL-14.03)
- PR-2: Materials suitable for CSD canola oil service (food-grade) (product: Datasheet.md Product/Service; construction: Datasheet.md Material Class Examples; rationale: Guidance.md Principles item 2; procedure: Procedure.md Step 3; cross-reference DEL-14.02)
- PR-3: Materials suitable for coastal environment (corrosion protection) (construction: Datasheet.md Material Class Examples; rationale: Guidance.md Principles item 2; procedure: Procedure.md Step 3; cross-reference DEL-14.02)

### Interface Requirements

(rationale: Guidance.md Principles item 3; considerations: Guidance.md Considerations - Coordination; procedure: Procedure.md Prerequisites, Steps 1-2):
- IR-1: Line numbers from P&IDs (DEL-14.01) (requirements: FR-1, FR-3; construction: Datasheet.md Construction item 1 - Provides traceability; rationale: Guidance.md Principles item 3; procedure: Procedure.md Prerequisites, Step 1; verification: Verification; examples: Guidance.md Examples items 1, 2; cross-reference DEL-14.01)
- IR-2: Material specifications from DEL-14.02 (requirements: FR-5, FR-6; construction: Datasheet.md Construction item 2 - Cross-reference; interface noted above; rationale: Guidance.md Principles item 3; procedure: Procedure.md Prerequisites, Step 4; verification: Verification; examples: Guidance.md Examples item 3; cross-reference DEL-14.02)
- IR-3: Design P/T from DEL-14.03 calculations (performance: PR-1; requirements: FR-2; conditions: Datasheet.md Design pressure/temperature; construction: Datasheet.md Construction item 1 - Typical columns; rationale: Guidance.md Principles item 3; procedure: Procedure.md Prerequisites, Step 2; verification: Verification; cross-reference DEL-14.03)
- IR-4: Coordinate with equipment data sheets (PKG-13, PKG-15, PKG-16) (construction: Datasheet.md Construction item 1 - From/To Equipment; considerations: Guidance.md Considerations - Coordination; procedure: Procedure.md Step 2; cross-reference PKG-13, PKG-15, PKG-16)

### Quality Requirements

(rationale: Guidance.md Principles item 3; procedure: Procedure.md Step 5, Step 6):
- QR-1: Line list complete and accurate (all lines from P&IDs) (requirements: FR-1; construction: Datasheet.md Construction item 1; interface: IR-1; procedure: Procedure.md Step 1, Step 2, Step 5; verification: Verification; examples: Guidance.md Examples items 1, 2)
- QR-2: Material data sheets consistent with DEL-14.02 (requirements: FR-5, FR-6; construction: Datasheet.md Construction item 2 - Cross-reference; interface: IR-2; procedure: Procedure.md Step 4, Step 5; verification: Verification; cross-reference DEL-14.02)
- QR-3: Independent check by qualified engineer (procedure: Procedure.md Step 5; verification: Verification)
- QR-4: Data sheet format per project standards **TBD** (attributes: Datasheet.md Line List Format, Revision Control; procedure: Procedure.md Step 6; documentation: Documentation section)

## Standards

(rationale: Guidance.md Principles item 2; procedure: Procedure.md Prerequisites):
- ASME B31.3 — material selection (performance: PR-1; rationale: Guidance.md Principles item 2; procedure: Procedure.md Prerequisites, Step 3; cross-reference DEL-14.02, DEL-14.03)
- DEL-14.02 — piping material specification (primary reference) (requirements: FR-6, IR-2; construction: Datasheet.md Construction item 2 - Cross-reference; rationale: Guidance.md Principles items 2, 3; quality: QR-2; procedure: Procedure.md Prerequisites, Step 4; verification: Verification)

## Verification

(quality: QR-1, QR-2, QR-3; procedure: Procedure.md Step 5):
- Cross-check line list vs. P&IDs (all lines captured) (requirements: FR-1, FR-3; quality: QR-1; interface: IR-1; rationale: Guidance.md Principles item 3; procedure: Procedure.md Step 5; verification table; cross-reference DEL-14.01)
- Verify design P/T vs. DEL-14.03 calculations (performance: PR-1; requirements: FR-2; interface: IR-3; procedure: Procedure.md Step 5; verification table; cross-reference DEL-14.03)
- Verify material classes vs. DEL-14.02 specification (requirements: FR-5, FR-6; quality: QR-2; interface: IR-2; procedure: Procedure.md Step 5; verification table; cross-reference DEL-14.02)
- Independent check sign-off (quality: QR-3; procedure: Procedure.md Step 5; verification table)

**Acceptance:** Line list complete, material data sheets accurate, checked and approved (quality: QR-1, QR-2, QR-3; procedure: Procedure.md Step 6; verification table)

## Documentation

**Line list columns** (requirements: FR-2; construction: Datasheet.md Construction item 1 - Typical columns; procedure: Procedure.md Step 2; examples: Guidance.md Examples item 1):
- Line Number, Service Description, From Equipment/To Equipment (requirements: FR-2; procedure: Procedure.md Step 1, Step 2; examples: Guidance.md Examples item 1)
- Pipe Size (NPS/DN), Material Class, Design Pressure, Design Temperature (requirements: FR-2; interface: IR-3; procedure: Procedure.md Step 2; examples: Guidance.md Examples item 1)
- Insulation Required (Y/N), Spec Reference (requirements: FR-2, FR-3; procedure: Procedure.md Step 2; examples: Guidance.md Examples item 1)

**Material data sheets** (requirements: FR-5; construction: Datasheet.md Construction item 2; procedure: Procedure.md Step 4; examples: Guidance.md Examples item 3):
- Material class definition (e.g., CS-150, SS-300) (requirements: FR-4; construction: Datasheet.md Material Class Examples; procedure: Procedure.md Step 3)
- Pipe, fittings, flanges, gaskets, bolting specifications (requirements: FR-5; construction: Datasheet.md Construction item 2 - Each class specifies; procedure: Procedure.md Step 4)
- Reference to DEL-14.02 (requirements: FR-6; interface: IR-2; procedure: Procedure.md Step 4)

**Storage:** `2_Checking/` → `3_Issued/` (attributes: Datasheet.md Revision Control; procedure: Procedure.md Step 6, Records section)

**Format:** Excel or database for line list; PDF for data sheets (attributes: Datasheet.md Line List Format; procedure: Procedure.md Prerequisites, Records section)
