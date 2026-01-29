# Guidance: DEL-22.02 Building MEP Technical Specification

## Purpose

This guidance document supports the development of **Building MEP Technical Specification** for **PKG-22 Building Interior & MEP**.

**Deliverable Purpose:** Defines performance, materials, and workmanship requirements for building MEP per Employer's Requirements.

**Source:** Decomposition REVISED_v2.md, DEL-22.02 entry; _CONTEXT.md

### Purpose and Role of Technical Specifications

Technical specifications translate design intent from drawings (DEL-22.01) into prescriptive requirements for:
- **Procurement**: Define equipment and materials for quotations and purchases
- **Construction**: Establish workmanship standards and installation methods
- **Quality Control**: Define testing, inspection, and acceptance criteria
- **Contract Administration**: Form part of contract documents governing work

This deliverable complements DEL-22.01 drawings. Drawings show WHAT and WHERE; specifications define HOW and WITH WHAT.

**Deliverable Classification:**
- **Type:** Specification
- **Discipline:** Buildings
- **Responsible Party:** D&B Contractor

**Source:** Standard role of technical specifications in EPC projects

## Principles

### Codes and Standards Framework

Technical specifications must reference and enforce compliance with applicable codes:
- **NBC 2020**: Governs all building systems design and installation in Canada
- **ASHRAE 90.1 & 62.1**: Energy efficiency and ventilation standards
- **NFPA 13**: Fire suppression system installation
- **CSA B64 series**: Plumbing installation standards
- **CEC**: Canadian Electrical Code (if electrical scope included)
- **SMACNA**: HVAC duct construction standards

**Source:** Specification.md Standards section; Datasheet.md applicable standards

### Specification Format and Structure

**ASSUMPTION**: Specifications typically follow CSI MasterFormat three-part structure:

1. **Part 1 - General**: Scope, references, submittals, quality assurance, delivery/storage
2. **Part 2 - Products**: Materials, equipment, manufacturers, fabrication
3. **Part 3 - Execution**: Installation, field quality control, startup, warranties

This structure provides consistency and completeness.

**Source:** CSI MasterFormat industry standard; Datasheet.md typical structure

### Performance-Based vs. Prescriptive Specifications

**Performance-Based**: Define required performance; allow contractor flexibility in means/methods
- Advantage: Encourages innovation, competitive pricing
- Risk: May require more review of proposed solutions

**Prescriptive**: Define specific materials, manufacturers, installation methods
- Advantage: Greater control over outcome, less review effort
- Risk: May limit competition, higher cost

**Recommendation**: Use hybrid approach—prescribe critical items, allow performance-based alternatives for non-critical items with approval process.

**Source:** ASSUMPTION: standard specification writing philosophy

### Equipment Specification Approaches

**Sole Source**: Single manufacturer specified (e.g., "Manufacturer X Model Y")
- Use when: Standardization critical, specific performance required, owner preference

**Approved Manufacturers List**: List 2-3 acceptable manufacturers
- Use when: Multiple qualified sources exist, competition desired

**Performance-Based with "Or Equal"**: Define performance, allow substitutions meeting performance
- Use when: Performance is measurable, multiple solutions acceptable

**Recommendation**: Approved manufacturers list (2-3) with "or approved equal" clause for most equipment.

**Source:** ASSUMPTION: standard equipment specification approaches

### Quality Assurance Through Submittals

Submittals provide quality control checkpoints before and during construction:
- **Shop Drawings**: Verify fabrication details match design intent (DEL-22.06)
- **Product Data**: Verify equipment selections meet specification requirements (DEL-22.04)
- **Test Reports**: Verify performance and compliance
- **O&M Manuals**: Enable proper operation and maintenance

Specification must clearly define what submittals are required, format, review time, and approval process.

**Source:** Specification.md FR-07; industry best practice

### Specification Writing Best Practices

**Imperative Language**: Use "shall" for requirements, not "should" or "may"

**Clarity**: Avoid ambiguous terms; be specific
- Bad: "Provide adequate ventilation"
- Good: "Provide minimum 15 L/s per person ventilation per ASHRAE 62.1"

**Completeness**: Every item shown on drawings must be specified

**Consistency**: Use same terminology throughout; coordinate with drawings

**Constructability**: Write for the contractor who will build it, not just for design peer review

**Source:** ASSUMPTION: industry best practices for specification writing

## Considerations

### Drawings and Specifications Coordination

Critical coordination between DEL-22.02 (specifications) and DEL-22.01 (drawings):
- Equipment shown on drawings must be specified
- Material call-outs on drawings must match specification nomenclature
- Drawing notes should reference specification sections (e.g., "See Section 23 74 00")
- No contradictions between drawings and specifications (specification typically governs in conflicts)

**Process**: Perform IDC (Interdisciplinary Check) to verify coordination before issue.

**Source:** Specification.md IF-01; standard drawings/specifications coordination

### Calculations Support

Specification requirements must be supported by design calculations (DEL-22.03):
- Equipment capacities specified must match calculated loads
- Performance criteria must be achievable per calculations
- Safety factors and design margins must be consistent

**Source:** Specification.md IF-02

### Material Selection

Consider:
- **Code Compliance**: NBC 2020, CEC, CSA standards
- **Environmental Compatibility**: Corrosion resistance, temperature ratings
- **Availability**: Standard products vs. long-lead specialty items
- **Lifecycle**: Durability, maintainability, replacement parts availability
- **Cost**: First cost vs. lifecycle cost (OBJ-9)

**Source:** Specification.md FR-04; ASSUMPTION: material selection criteria

### Constructability and Installation

Specifications must be constructible:
- Installation methods must be practical and safe
- Access and rigging requirements must be feasible
- Coordination with other trades (structural supports, electrical connections, etc.)
- **DEC-06 Note**: "MCC building equipment installed on-site after building erection"—sequencing affects specification of installation methods

**Source:** Specification.md FR-06; Decomposition DEC-06

### Control System Interfaces

MEP equipment interfaces with BAS (Building Automation System) per PKG-19:
- Specify control points required (start/stop, speed control, temperature setpoints, etc.)
- Specify communication protocols (BACnet, Modbus, etc.)—coordinate with PKG-19
- Specify equipment-mounted controls vs. remote BAS control
- Define control sequences in specification or reference PKG-19 control narrative

**Source:** Specification.md IF-04; PKG-19 interface requirement

### Electrical Coordination

MEP equipment requires electrical power per PKG-17:
- Specify voltage, phase, full-load amps for each equipment item
- Specify disconnect and overcurrent protection requirements per CEC
- Coordinate with PKG-17 panel schedules and circuit assignments
- Specify equipment nameplates and labeling

**Source:** Specification.md IF-05; CEC requirements

### Commissioning and Acceptance

Specifications must define commissioning requirements:
- Functional performance testing (system operates as designed)
- Capacity verification testing (meets specified capacity)
- Training requirements (for owner's operators)
- Documentation requirements (test reports, O&M manuals)
- Warranty commencement (after successful commissioning)

Coordinate with DEL-22.05 Installation and Test Records for documentation of results.

**Source:** Specification.md FR-08; standard commissioning practice

### Quality Assurance Process

Specifications require review at multiple stages:
- **Internal Technical Review**: Engineering review for technical adequacy
- **IDC Review**: Interdisciplinary coordination review
- **Constructability Review**: Review by construction team (if available)
- **Employer Review**: Review by client for compliance with Employer's Requirements

**Source:** Specification.md QR-01; standard EPC quality process

## Trade-offs

### First Cost vs. Lifecycle Cost

**Decision Point**: Specify minimum-code-compliant equipment vs. higher-efficiency equipment

**Trade-off**:
- Minimum compliance: Lower capital cost, higher operating cost (energy)
- High efficiency: Higher capital cost, lower operating cost, faster payback period

**Recommendation**: Perform lifecycle cost analysis per OBJ-9 Lifecycle Cost Optimization. Consider energy escalation rates and equipment life. ASHRAE 90.1 sets minimum; exceeding minimum requires economic justification.

**Source:** Specification.md PR-03; Decomposition OBJ-9

### Sole Source vs. Competitive Specification

**Decision Point**: Specify single manufacturer vs. multiple approved manufacturers

**Trade-off**:
- Sole source: Greater control, standardization, potential single-source risk
- Competitive: Lower cost through competition, multiple supply sources, more review effort

**Recommendation**: Use competitive specifications (2-3 manufacturers) for standard equipment. Consider sole source only for critical standardization or integration requirements.

**Source:** Principles section "Equipment Specification Approaches"

### Performance vs. Prescriptive Specification

**Decision Point**: Performance-based spec (define outcome) vs. prescriptive spec (define method)

**Trade-off**:
- Performance-based: Encourages innovation, transfers risk to contractor, requires more review
- Prescriptive: Greater control, less risk, may limit innovation and cost savings

**Recommendation**: Hybrid approach—prescribe critical design elements, allow performance-based alternatives for non-critical elements with engineering review and approval.

**Source:** Principles section "Performance-Based vs. Prescriptive Specifications"

### Detail Level: Complete vs. Reference Standards

**Decision Point**: Fully describe installation methods vs. reference industry standards

**Trade-off**:
- Fully described: No ambiguity, more specification writing effort, may conflict with standard practice
- Reference standards: Less writing, industry-accepted methods, assumes contractor familiarity

**Recommendation**: Reference standards for standard work (e.g., "Install ductwork per SMACNA HVAC Duct Construction Standards"). Provide project-specific requirements for non-standard work.

**Source:** ASSUMPTION: specification writing best practice

## Examples

### Specification Section Example (CSI Format)

**Example: Section 23 74 00 - Packaged Outdoor HVAC Equipment**

```
PART 1 - GENERAL

1.1 SECTION INCLUDES
  A. Packaged rooftop HVAC units
  B. Curb adapters and supports

1.2 RELATED SECTIONS
  A. Section 23 05 00 - Common Work Results for HVAC
  B. Section 23 07 00 - HVAC Insulation
  C. Section 23 31 00 - HVAC Ducts and Casings

1.3 REFERENCES
  A. ASHRAE 90.1 - Energy Standard for Buildings
  B. NBC 2020 - National Building Code of Canada

1.4 SUBMITTALS
  A. Product Data: Manufacturer's data sheets per DEL-22.04
  B. Shop Drawings: Unit layout, duct connections per DEL-22.06
  C. Test Reports: Factory test reports, field startup reports per DEL-22.05

PART 2 - PRODUCTS

2.1 MANUFACTURERS
  A. Acceptable Manufacturers (or approved equal):
    1. Carrier
    2. Trane
    3. Lennox

2.2 HVAC UNITS
  A. Capacity: As indicated on drawings and per DEL-22.03 calculations
  B. Efficiency: Minimum ASHRAE 90.1 requirements
  C. Construction: [materials, coatings, etc.]

PART 3 - EXECUTION

3.1 INSTALLATION
  A. Install per manufacturer's instructions and NBC 2020
  B. Provide seismic restraints per NBC 2020 for Surrey, BC location
  C. Coordinate with structural supports (PKG-21)

3.2 FIELD QUALITY CONTROL
  A. Factory Testing: Per AHRI standards
  B. Startup Testing: Functional performance test per DEL-22.05
  C. Commissioning: Per Section 01 91 00 Commissioning
```

**Source:** ASSUMPTION: typical CSI MasterFormat specification section structure

### Anticipated Specification Artifacts

Per Decomposition DEL-22.02:

1. **HVAC specification** — Divisions 23 (HVAC systems, equipment, ductwork, controls interfaces)
2. **Building plumbing specification** — Division 22 (plumbing systems, fixtures, piping, equipment)
3. **Fire suppression specification** — Division 21 (sprinkler systems, equipment, piping)
4. **Electrical building services specification** (if required—TBD) — Portions of Division 26 applicable to building services

**Source:** Decomposition REVISED_v2.md, DEL-22.02 anticipated artifacts; Datasheet.md specification sections

## Conflict Table (for human ruling)

No conflicts identified at this stage. Conflicts will be documented here if contradictions are found between sources during specification development.

**Format**:

| Conflict ID | Conflict | Source A | Source B | Impacted Sections | Proposed Authority | Human Ruling |
|-------------|----------|----------|----------|-------------------|-------------------|--------------|
| (none yet) | | | | | | |
