# Guidance: DEL-14.04 Process Piping Data Sheet Package

## Purpose

Provides comprehensive data package defining all piping lines (line list) and material specifications (data sheets) for PKG-14 Process Piping (scope: Specification.md Scope; attributes: Datasheet.md Data Sheet Type).

## Principles

**1. Line List:**
- Central register of all piping lines in the facility (construction: Datasheet.md Construction item 1; requirements: Specification.md FR-1; procedure: Procedure.md Step 2)
- Each line has unique line number (typically format: size-fluid-sequence, e.g., 6"-CO-101) (construction: Datasheet.md Construction item 1 - Typical columns; requirements: Specification.md FR-2; interface: Specification.md IR-1; procedure: Procedure.md Step 1; examples: below items 1, 2)
- Provides quick reference for line service, size, material, design conditions (construction: Datasheet.md Construction item 1; requirements: Specification.md FR-2; rationale: above; procedure: Procedure.md Step 2; documentation: Specification.md Documentation - Line list columns)
- Foundation for procurement, fabrication, installation, and operations (rationale: above; considerations: below - Coordination; procedure: Procedure.md Step 2; cross-reference DEL-14.01, DEL-14.02, DEL-14.05)

**2. Material Classification:**
- Group similar services into material classes (e.g., CS-150 for carbon steel, Class 150 canola oil service) (attributes: Datasheet.md Material Classes; construction: Datasheet.md Material Class Examples; requirements: Specification.md FR-4; considerations: below - Material Data Sheets; trade-offs: below item 1; procedure: Procedure.md Step 3; examples: below item 3)
- Standardization reduces procurement complexity and inventory (source: OBJ-9; requirements: Specification.md FR-4; rationale: above; trade-offs: below item 1; procedure: Procedure.md Step 3; cross-reference DEL-14.02)
- Typical facility has 3-6 material classes (attributes: Datasheet.md Material Classes; construction: Datasheet.md Material Class Examples; requirements: Specification.md FR-4; trade-offs: below item 1; procedure: Procedure.md Step 3)

**3. Traceability:**
- Line list traces to P&IDs (graphical representation) (construction: Datasheet.md Construction item 1 - Provides traceability; requirements: Specification.md FR-3, IR-1; rationale: above; considerations: below - Coordination; procedure: Procedure.md Step 1; verification: Specification.md Verification; examples: below items 1, 2; cross-reference DEL-14.01)
- Material data sheets trace to DEL-14.02 (detailed specification) (construction: Datasheet.md Construction item 2 - Cross-reference; requirements: Specification.md FR-6, IR-2; rationale: above; considerations: below - Coordination; quality: Specification.md QR-2; procedure: Procedure.md Step 4; verification: Specification.md Verification; examples: below item 3; cross-reference DEL-14.02)
- Design P/T traces to DEL-14.03 (calculations) (conditions: Datasheet.md Design pressure/temperature; performance: Specification.md PR-1; requirements: Specification.md FR-2; interface: Specification.md IR-3; rationale: above; procedure: Procedure.md Step 2; verification: Specification.md Verification; cross-reference DEL-14.03)

## Considerations

**Line List Development:**
- Extract line numbers from P&IDs (DEL-14.01) (construction: Datasheet.md Construction item 1; requirements: Specification.md FR-1, FR-3; interface: Specification.md IR-1; rationale: above item 3; procedure: Procedure.md Prerequisites, Step 1; examples: below items 1, 2; cross-reference DEL-14.01)
- Assign material class based on service and conditions (construction: Datasheet.md Construction item 1 - Typical columns; requirements: Specification.md FR-2, FR-4; rationale: above item 2; procedure: Procedure.md Step 2, Step 3)
- Populate design P/T from calculations (DEL-14.03) (conditions: Datasheet.md Design pressure/temperature; performance: Specification.md PR-1; requirements: Specification.md FR-2; interface: Specification.md IR-3; rationale: above item 3; procedure: Procedure.md Step 2; verification: Specification.md Verification; cross-reference DEL-14.03)
- Identify insulation requirements (personnel protection, energy conservation) (construction: Datasheet.md Construction item 1 - Typical columns; requirements: Specification.md FR-2; procedure: Procedure.md Step 2; cross-reference DEL-14.02)

**Material Data Sheets:**
- Define material classes based on pressure rating and service (attributes: Datasheet.md Material Classes; construction: Datasheet.md Material Class Examples; requirements: Specification.md FR-4; rationale: above item 2; trade-offs: below item 1; procedure: Procedure.md Step 3; examples: below item 3)
- Example classes: CS-150 (carbon steel Class 150), CS-300 (carbon steel Class 300), SS-150 (stainless steel Class 150 for nitrogen) (construction: Datasheet.md Material Class Examples; requirements: Specification.md FR-4; rationale: above item 2; procedure: Procedure.md Step 3; examples: below item 3)
- Each class specifies: pipe material/schedule, fitting type, flange rating, gasket type, bolting material (construction: Datasheet.md Construction item 2 - Each class specifies; requirements: Specification.md FR-5; rationale: above item 2; procedure: Procedure.md Step 4; documentation: Specification.md Documentation - Material data sheets; examples: below item 3)

**Coordination:**
- Equipment nozzles: Line sizes match equipment connections (interface: Specification.md IR-4; construction: Datasheet.md Construction item 1 - From/To Equipment; procedure: Procedure.md Step 2; cross-reference PKG-13, PKG-15, PKG-16)
- Specifications: Material classes align with DEL-14.02 (requirements: Specification.md FR-6, IR-2; construction: Datasheet.md Construction item 2 - Cross-reference; quality: Specification.md QR-2; rationale: above item 3; procedure: Procedure.md Step 4; verification: Specification.md Verification; cross-reference DEL-14.02)
- Drawings: Line numbers on isometrics match line list (requirements: Specification.md FR-3; interface: Specification.md IR-1; rationale: above item 3; procedure: Procedure.md Step 1, Step 2; verification: Specification.md Verification; cross-reference DEL-14.01)

## Trade-offs

**1. Material Class Granularity:**
- Few classes (e.g., 2-3): Simple, may over-spec some lines (cost penalty) (attributes: Datasheet.md Material Classes; requirements: Specification.md FR-4; rationale: above item 2; procedure: Procedure.md Step 3)
- Many classes (e.g., 8-10): Optimized, but complex procurement and inventory (rationale: above item 2; considerations: above - Material Data Sheets)
- **Guidance:** 3-6 classes typical balance (attributes: Datasheet.md Material Classes; construction: Datasheet.md Material Class Examples; requirements: Specification.md FR-4; rationale: above item 2; procedure: Procedure.md Step 3; cross-reference DEL-14.02)

**2. Line List Detail:**
- Minimal (line number, size, material): Fast to create, limited usefulness (requirements: Specification.md FR-2; rationale: above item 1)
- Comprehensive (add from/to, P/T, insulation, spec, etc.): More useful, higher effort (construction: Datasheet.md Construction item 1 - Typical columns; requirements: Specification.md FR-2; rationale: above item 1; considerations: above - Line List Development; procedure: Procedure.md Step 2; documentation: Specification.md Documentation - Line list columns)
- **Guidance:** Include key parameters for operations and maintenance value (requirements: Specification.md FR-2; rationale: above item 1; considerations: above - Line List Development; procedure: Procedure.md Step 2)

## Examples

**1. Typical line list entry:**
- Line Number: 8"-CO-201 (construction: Datasheet.md Construction item 1; requirements: Specification.md FR-2; interface: Specification.md IR-1; rationale: above item 1; procedure: Procedure.md Step 1, Step 2; documentation: Specification.md Documentation - Line list columns)
- Service: Canola Oil from Railcar Header to Tank T-101 (product: Datasheet.md Product/Service; requirements: Specification.md FR-2; procedure: Procedure.md Step 2)
- From: Railcar Unloading Header / To: Tank T-101 Inlet Nozzle (construction: Datasheet.md Construction item 1 - Typical columns; requirements: Specification.md FR-2; interface: Specification.md IR-4; procedure: Procedure.md Step 2)
- Pipe Size: DN 200 (8") (requirements: Specification.md FR-2; interface: Specification.md IR-3; procedure: Procedure.md Step 2; cross-reference DEL-14.03)
- Material Class: CS-150 (construction: Datasheet.md Material Class Examples; requirements: Specification.md FR-2, FR-4; procedure: Procedure.md Step 2, Step 3)
- Design Pressure: 1,035 kPa (150 psi) (conditions: Datasheet.md Design pressure/temperature; performance: Specification.md PR-1; requirements: Specification.md FR-2; interface: Specification.md IR-3; procedure: Procedure.md Step 2; cross-reference DEL-14.03)
- Design Temperature: 60°C (conditions: Datasheet.md Design pressure/temperature; performance: Specification.md PR-1; requirements: Specification.md FR-2; interface: Specification.md IR-3; procedure: Procedure.md Step 2)
- Insulation: N (requirements: Specification.md FR-2; procedure: Procedure.md Step 2; cross-reference DEL-14.02)
- Spec Reference: DEL-14.02 (requirements: Specification.md FR-3, FR-6; interface: Specification.md IR-2; procedure: Procedure.md Step 2)

**2. Additional line list examples:**
- 12"-CO-101: Canola Oil Marine Loading Export Line, Tank T-101 to Loading Arm LA-1, DN 300, CS-300, 2,070 kPa, 60°C, Insulation: N (construction: Datasheet.md Construction item 1; requirements: Specification.md FR-2; procedure: Procedure.md Step 2; cross-reference DEL-14.01, DEL-14.03)
- 2"-N2-001: Nitrogen Supply to Tank T-101 Blanketing, Nitrogen Skid to Tank T-101, DN 50, SS-150, 690 kPa, Ambient, Insulation: N (construction: Datasheet.md Material Class Examples - SS-150; requirements: Specification.md FR-2; procedure: Procedure.md Step 2; cross-reference DEL-14.01, DEL-14.02)

**3. Typical material data sheet (Material Class CS-150):**
- **Class:** CS-150 (Carbon Steel, ASME B16.5 Class 150) (construction: Datasheet.md Material Class Examples; requirements: Specification.md FR-4; rationale: above item 2; procedure: Procedure.md Step 3, Step 4)
- **Service:** Canola oil liquid service, moderate pressure (performance: Specification.md PR-2; construction: Datasheet.md Material Class Examples; procedure: Procedure.md Step 3)
- **Pipe:** ASTM A106 Gr. B seamless, Schedule 40 typical (size-dependent) (construction: Datasheet.md Material Class Examples; requirements: Specification.md FR-5; interface: Specification.md IR-2; procedure: Procedure.md Step 4; cross-reference DEL-14.02)
- **Fittings:** ASME B16.9 butt-weld, carbon steel (requirements: Specification.md FR-5; interface: Specification.md IR-2; procedure: Procedure.md Step 4; cross-reference DEL-14.02)
- **Flanges:** ASME B16.5 Class 150 weld neck or slip-on, ASTM A105, raised face (construction: Datasheet.md Material Class Examples; requirements: Specification.md FR-5; interface: Specification.md IR-2; trade-offs: Guidance.md Trade-offs item 1; procedure: Procedure.md Step 4; cross-reference DEL-14.02)
- **Gaskets:** Spiral-wound (ASME B16.20) or compressed fiber (ASME B16.21), food-grade compatible (requirements: Specification.md FR-5; performance: Specification.md PR-2; interface: Specification.md IR-2; procedure: Procedure.md Step 4; cross-reference DEL-14.02)
- **Bolting:** ASTM A193 Gr. B7 bolts with A194 Gr. 2H nuts (requirements: Specification.md FR-5; interface: Specification.md IR-2; procedure: Procedure.md Step 4; cross-reference DEL-14.02)
- **Reference:** DEL-14.02 Process Piping Technical Specification (requirements: Specification.md FR-6, IR-2; quality: Specification.md QR-2; rationale: above item 3; procedure: Procedure.md Step 4; verification: Specification.md Verification)
