# Specification: DEL-21.02 Building Technical Specification

## Scope

This specification defines the requirements for **Building Technical Specification** within **PKG-21 Building Structures & Envelope**.

**Purpose:** Defines performance, materials, and workmanship requirements for building per ER requirements.

**Source:** Decomposition document line 514

**Package Scope:** MCC building structure, cladding, roofing, doors, windows, operator shelters

**Source:** Decomposition document line 507

**Anticipated Specification Artifacts:**

Per decomposition (line 514):
1. **Modular building specification** — Materials, assembly, installation requirements
2. **Building envelope specification** — Cladding, roofing, insulation, air/vapor barriers, sealants, flashing
3. **Door specification** — Types, materials, hardware, fire ratings, accessibility

**Inclusions:**
- Material specifications (types, grades, performance criteria)
- Product standards and acceptable manufacturers
- Workmanship standards and installation requirements
- Testing and inspection criteria
- Quality assurance and quality control procedures
- Warranty requirements

**Exclusions:**
- Design calculations and engineering analysis (DEL-21.03)
- Installation test records (DEL-21.05)
- Shop/fabrication detailing (DEL-21.06)

## Requirements

### Functional Requirements

**FR-01: Specification Organization and Format**
- Organize per CSI MasterFormat (or project specification standard) — **TBD**
- Use 3-part section format: Part 1 General, Part 2 Products, Part 3 Execution
- Include section cross-references and coordination notes

**Source:** CSI MasterFormat standard specification organization

**FR-02: Material Performance Specifications**
- Specify materials by performance criteria, approved products, or reference standards
- Include test standards and acceptance criteria (ASTM, CSA, ULC)
- Specify corrosion protection for marine/industrial environment
- **TBD** — Specific material grades, product types, manufacturers

**Source:** NBC 2020 material requirements; coastal environment durability

**FR-03: Workmanship and Installation Requirements**
- Define installation methods and procedures
- Specify installer qualifications and certifications
- Reference industry installation standards (SMACNA, CSSBI, CISC, AWS, ACI)
- Define field quality control and testing
- **TBD** — Specific installation procedures and acceptance criteria

**Source:** Industry trade standards; NBC 2020 workmanship requirements

### Performance Requirements

**PR-01: Structural Material Performance**
- Comply with NBC 2020 Part 4 structural provisions
- Structural steel: **TBD** — CSA G40.20/G40.21 grades (350W, 300W typical)
- Concrete: **TBD** — CSA A23.1 mixes, strength, durability requirements
- Connections and fasteners per CSA S16, CSA W59
- Corrosion protection: **TBD** — Galvanizing (ASTM A653), paint systems, stainless fasteners

**Source:** NBC 2020 Part 4; CSA S16; CSA A23.3

**PR-02: Envelope Thermal Performance**
- Comply with NBC 2020 Part 5 thermal requirements (or ASHRAE 90.1 if applicable)
- Thermal resistance (R-value): **TBD** — Walls, roof, floor assemblies
- Air barrier system: **TBD** — CSA A123.21 performance requirements
- Vapor control: **TBD** — NBC 2020 Part 5 Section 5.5

**Source:** NBC 2020 Part 5; ASHRAE 90.1

**PR-03: Envelope Weathertightness**
- Water penetration resistance: ASTM E331 or equivalent
- Air leakage: ASTM E283 or CSA A123.21
- Wind load resistance: ASTM E330 (envelope components)
- **TBD** — Specific test pressures and acceptance criteria

**Source:** NBC 2020 Part 5; ASTM testing standards

**PR-04: Fire Performance**
- Comply with NBC 2020 Part 3 fire safety requirements
- Fire resistance ratings: **TBD** — ULC S101 tested assemblies (if required)
- Surface burning: **TBD** — CAN/ULC S102 flame spread and smoke development limits
- Fire-rated doors: **TBD** — ULC S104 tested assemblies with labeling

**Source:** NBC 2020 Part 3; ULC fire testing standards

**PR-05: Accessibility Performance**
- Comply with NBC 2020 Part 3 Section 3.8 (barrier-free design)
- Door hardware: Lever handles, appropriate opening force per CSA B651
- Door clearances: **TBD** — 810mm minimum clear width
- **TBD** — Accessible route provisions

**Source:** NBC 2020 Part 3 Div B Section 3.8; CSA B651

### Interface Requirements

**IR-01: Coordination with Design Drawings**
- Materials and systems specified shall match design drawings (DEL-21.01)
- Resolve conflicts between drawings and specifications — **TBD**: precedence rules

**IR-02: Coordination with Calculations**
- Material properties used in specifications shall match design calculations (DEL-21.03)
- Structural member sizes and connections coordinated

**IR-03: Coordination with Other Disciplines**
- Civil/site: Foundation interface materials and waterproofing
- MEP (PKG-22): Penetrations, flashings, roof equipment support provisions
- Coatings (PKG-26): Protective coating specifications for building steel/metal

Dependencies coordinated externally per `_DEPENDENCIES.md`

### Quality Requirements

**QR-01: Submittals**
- Product data submittals for Employer/Engineer review
- Shop drawings for fabricated items
- Manufacturer's certificates and test reports
- **TBD** — Submittal procedures and review timeframes

**QR-02: Quality Assurance**
- Manufacturer qualifications: **TBD** — years in business, references
- Installer qualifications: **TBD** — certifications, experience
- Quality control testing: **TBD** — Testing frequency, third-party testing requirements

**QR-03: Warranty**
- Material warranties: **TBD** — Manufacturer standard warranties
- Installation warranties: **TBD** — Contractor workmanship warranty
- Extended warranties: **TBD** — Roofing, envelope systems (10-20 years typical)

## Standards

**Governing Codes:**
- **NBC 2020** — National Building Code of Canada 2020 (all Parts)
- **Provincial code** — **TBD**: BCBC 2018 or ABC 2019

**Material Standards:**
- CSA A23.1/A23.2/A23.3 — Concrete
- CSA G40.20/G40.21 — Structural steel
- CSA S16 — Steel design
- CSA W47.1/W59 — Welding
- ASTM — Various material specifications (A36, A572, A653, etc.)

**Testing Standards:**
- CSA A123.21 — Air leakage
- ASTM C518 — Thermal transmission
- ASTM E283/E330/E331 — Air/water/structural testing
- ULC S101/S102/S104 — Fire testing

**Accessibility:**
- CSA B651 — Accessible Design

**Trade Standards:**
- SMACNA — Sheet metal
- CSSBI — Metal building panels
- CISC — Steel construction
- ACI — Concrete

**Employer's Requirements:**
- **TBD** — ER Volume 2 Part 3: Building Works

## Verification

**Verification Methods:**

**VM-01: Specification Review**
- Technical review by qualified specifier/engineer
- Review against ER requirements and design basis
- Check coordination with drawings (DEL-21.01) and calculations (DEL-21.03)

**VM-02: Standards and Code Compliance Check**
- Verify material specifications comply with NBC 2020 and applicable standards
- Verify test standards and acceptance criteria are appropriate

**VM-03: Constructability Review**
- Review specifications for constructability (availability of materials, feasibility of installation)
- Engage trade contractors for input (if design-build or design-assist)

**Acceptance Criteria:**
- Specification complete (all required sections present)
- Coordinated with drawings and calculations
- Complies with NBC 2020 and applicable standards
- Materials and products available and constructable
- **TBD** — Employer review and approval

## Documentation

**Required Documentation Outputs:**

Per decomposition (line 514):
1. **Modular Building Specification** (if modular approach used)
   - CSI Division 13: Relocatable Buildings or Fabricated Engineered Structures
2. **Building Envelope Specification**
   - CSI Division 07: Thermal and Moisture Protection (insulation, air barriers, roofing, sealants, flashing)
3. **Door Specification**
   - CSI Division 08: Openings (doors, frames, hardware)

**Supporting Documentation:**
- CSI specification sections per MasterFormat organization
- Product data sheets and technical literature
- Test standards and acceptance criteria
- Installer qualifications and certifications
- Warranty requirements

**Documentation Management:**
- **Format:** Text document (Word, PDF) — **TBD**
- **Revision control:** Per project document control procedures
- **Storage:** Project document management system — **TBD**
- **Lifecycle management:** `1_Working/` → `2_Checking/` → `3_Issued/` per `_STATUS.md`
