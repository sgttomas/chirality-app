# Specification: DEL-22.03 Building MEP Design Calculations

## Scope

This specification defines the requirements for **Building MEP Design Calculations** within **PKG-22 Building Interior & MEP**.

**Deliverable Description:** Provides the engineering basis and sizing/verification calculations for building MEP per Employer's Requirements.

**Source:** Decomposition REVISED_v2.md, DEL-22.03 entry; _CONTEXT.md

### Included

This calculation deliverable shall include:

1. **HVAC load calculations** — Heating and cooling load calculations for equipment sizing
2. **Plumbing sizing calculations** — Water supply and drainage pipe sizing
3. **Ventilation calculations** — Outdoor air requirements per ASHRAE 62.1 (inferred from scope)
4. **Fire protection hydraulic calculations** — Sprinkler system sizing per NFPA 13 (inferred from scope)

**Source:** Decomposition REVISED_v2.md, DEL-22.03 anticipated artifacts; inferred from MEP design scope

### Excluded

The following are **excluded** from this deliverable and covered elsewhere:

- Structural calculations (covered by PKG-21 Building Structures & Envelope)
- Main electrical distribution calculations (covered by PKG-17 Electrical Power Distribution)
- Control system logic and programming (covered by PKG-19 Control Systems)
- Process equipment calculations (covered by other packages)

**Source:** Package scope boundaries per Decomposition

### Relationship to Other Deliverables

These calculations:

- **Support DEL-22.01 drawings** by providing sizing basis for equipment and systems
- **Verify DEL-22.02 specifications** by demonstrating equipment and materials meet performance requirements
- **Establish parameters for DEL-22.04 datasheets** by calculating required equipment capacities and operating conditions
- **Are verified during DEL-22.05 testing** by comparison to measured performance

**Source:** Standard EPC deliverable relationships

## Requirements

### Functional Requirements

#### FR-01: Calculation Completeness

Calculations shall provide complete engineering justification for all MEP equipment sizing and system design decisions shown in DEL-22.01 drawings and specified in DEL-22.02 specifications.

**Rationale**: See Guidance.md, Section "Purpose and Role of Design Calculations"

**Verification**: See Procedure.md, Step 4 (results interpretation and completeness check)

**Source:** ASSUMPTION: standard calculation completeness requirement

#### FR-02: HVAC Load Calculations

- **FR-02.1**: Heating load calculations shall determine design heating capacity for all building zones per ASHRAE Fundamentals methodology. **TBD** — Design heating load results (location TBD)
  - **Rationale**: See Guidance.md, Section "HVAC Load Calculation Principles"
  - **Verification**: See Procedure.md, Step 3.1 (HVAC load calculations); Datasheet.md (Design Basis Parameters)

- **FR-02.2**: Cooling load calculations shall determine design cooling capacity including envelope loads, internal gains, and ventilation loads. **TBD** — Design cooling load results (location TBD)
  - **Rationale**: See Guidance.md, Section "HVAC Load Calculation Principles"
  - **Verification**: See Procedure.md, Step 3.1; cross-check with DEL-22.01 equipment schedules

- **FR-02.3**: Ventilation calculations shall comply with ASHRAE 62.1 for building occupancy type. **TBD** — Outdoor air requirements (location TBD)
  - **Rationale**: See Guidance.md, Section "HVAC Load Calculation Principles"
  - **Verification**: See Procedure.md, Step 3.1; DEL-22.01 Specification FR-HVAC-02

**Source:** ASHRAE Fundamentals, ASHRAE 62.1 (locations TBD)

#### FR-03: Plumbing Sizing Calculations

- **FR-03.1**: Water supply piping shall be sized per fixture unit method (CSA B64 or NBC 2020) to provide adequate flow and pressure. **TBD** — Pipe sizes and flow rates (location TBD)
  - **Rationale**: See Guidance.md, Section "Plumbing Sizing Principles"
  - **Verification**: See Procedure.md, Step 3.2; cross-check with DEL-22.01 plumbing drawings

- **FR-03.2**: Drainage piping shall be sized per fixture units per NBC 2020 / CSA B64. **TBD** — Drainage pipe sizes (location TBD)
  - **Rationale**: See Guidance.md, Section "Plumbing Sizing Principles"
  - **Verification**: See Procedure.md, Step 3.2; DEL-22.01 Specification FR-PLUMB-01/02

**Source:** NBC 2020, CSA B64 (locations TBD)

#### FR-04: Fire Protection Hydraulic Calculations

Fire suppression system shall be hydraulically calculated per NFPA 13 to verify adequate flow and pressure for sprinkler system operation. **TBD** — Hydraulic calculation results (location TBD)

**Rationale**: See Guidance.md, Section "Fire Protection Calculation Principles"

**Verification**: See Procedure.md, Step 3.3; DEL-22.01 Specification FR-FIRE-01; coordinate with PKG-03 for water supply availability

**Source:** NFPA 13 (location TBD)

### Performance Requirements

#### PR-01: Calculation Accuracy and Method

- **PR-01.1**: Calculations shall use recognized engineering methods per applicable codes and standards
- **PR-01.2**: Software calculations shall use approved software with documented validation
- **PR-01.3**: Hand calculations shall follow step-by-step methodology with clear assumptions
- **PR-01.4**: All assumptions shall be documented and justified

**Rationale**: See Guidance.md, Section "Calculation Methodology Standards"

**Verification**: See Procedure.md, Step 2 (methodology selection), Step 5 (independent check)

**Source:** ASSUMPTION: standard engineering calculation quality requirements

#### PR-02: Design Margins and Safety Factors

- **PR-02.1**: Equipment sizing shall include appropriate design margins per industry practice. **TBD** — Design margin criteria (location TBD)
- **PR-02.2**: Peak load conditions and diversity factors shall be justified
- **PR-02.3**: Future expansion allowances: **TBD** — Per Employer's Requirements (location TBD)

**Rationale**: See Guidance.md, Trade-offs "Design Margins vs. Equipment Cost"

**Verification**: See Procedure.md, Step 4 (results interpretation)

**Source:** ASSUMPTION: standard design practice; specific requirements TBD

#### PR-03: Code Compliance Demonstration

Calculations shall demonstrate compliance with:
- NBC 2020 (building loads, climate data, plumbing sizing)
- ASHRAE 90.1 (energy efficiency)
- ASHRAE 62.1 (ventilation rates)
- NFPA 13 (fire protection system sizing)

**Rationale**: See Guidance.md, Section "Code Compliance Through Calculations"

**Verification**: See Procedure.md, Step 4 (code compliance checks); cross-check with DEL-22.01 Specification requirements

**Source:** Applicable codes and standards

### Interface Requirements

#### IF-01: Support for Drawings (DEL-22.01)

Calculations shall:
- Provide sizing basis for all equipment shown on DEL-22.01 drawings
- Justify all design assumptions shown on drawings
- Be cross-referenced on drawings where applicable

**Rationale**: See Guidance.md, Section "Calculations and Drawings Coordination"

**Verification**: See Procedure.md, Step 6 (cross-check with DEL-22.01)

**Source:** DEL-22.01 Specification QR-06

#### IF-02: Verification of Specifications (DEL-22.02)

Calculations shall:
- Verify equipment performance requirements specified in DEL-22.02
- Support material selections and installation requirements
- Demonstrate specification compliance with codes

**Rationale**: See Guidance.md, Section "Calculations and Specifications Coordination"

**Verification**: See Procedure.md, Step 6 (cross-check with DEL-22.02)

**Source:** DEL-22.02 Specification IF-02

#### IF-03: Equipment Parameters for Datasheets (DEL-22.04)

Calculations shall establish:
- Equipment capacities and operating conditions
- Performance parameters (flow, pressure, temperature, power)
- Selection criteria for vendor quotes

**Rationale**: See Guidance.md, Section "Calculations and Equipment Selection"

**Verification**: See Procedure.md, Step 6 (cross-check with DEL-22.04)

**Source:** Standard calculation/datasheet coordination

#### IF-04: Input from Site Services (PKG-03)

Fire protection calculations require:
- Fire water supply pressure and flow availability from PKG-03
- Domestic water supply parameters from PKG-03
- Sanitary sewer connection parameters from PKG-03

**Rationale**: See Guidance.md, Section "Considerations - Interface Coordination"

**Verification**: See Procedure.md, Step 1 (input data collection); coordinate with PKG-03

**Source:** Interface requirements per package scopes

### Quality Requirements

#### QR-01: Independent Check

- All calculations shall undergo independent check by qualified engineer not involved in original preparation
- Checker shall verify methodology, assumptions, inputs, calculations, and results
- Checker comments shall be resolved and documented

**Rationale**: See Guidance.md, Section "Quality Assurance for Calculations"

**Verification**: See Procedure.md, Step 5 (independent check process)

**Source:** ASSUMPTION: standard engineering quality procedure

#### QR-02: Professional Responsibility

Calculations shall:
- Be prepared under responsible charge of Professional Engineer registered in British Columbia
- Meet professional standard of care per engineering code of ethics
- Be signed and sealed by P.Eng. if required for NBC 2020 compliance

**Rationale**: Professional liability and code compliance requirements

**Verification**: See Procedure.md, Step 6 (approval and professional review)

**Source:** NBC 2020 professional requirements for BC

#### QR-03: Documentation Standards

- All calculation sheets shall include project identification, calculation title, preparer/checker/approver signatures, revision history
- All inputs and assumptions shall be clearly documented with sources
- All calculation steps shall be traceable and verifiable
- Results shall be clearly summarized

**Rationale**: See Guidance.md, Section "Calculation Documentation Standards"

**Verification**: See Procedure.md, Step 3 (calculation execution), Step 5 (format compliance check)

**Source:** ASSUMPTION: standard calculation documentation requirements

## Standards

### Applicable Codes and Standards

**Building Codes:**

- **NBC 2020** — National Building Code of Canada 2020
- **ABC 2019** — **TBD** — Identify full name and applicability (location TBD)

**HVAC Design Standards:**

- **ASHRAE 90.1** — Energy Standard for Buildings (latest edition) **TBD** (location TBD)
- **ASHRAE 62.1** — Ventilation for Acceptable Indoor Air Quality **TBD** (location TBD)
- **ASHRAE Fundamentals Handbook** — Load calculation methodology **TBD** (location TBD)

**Plumbing Standards:**

- **CSA B64** series — Plumbing fixture units and pipe sizing **TBD** (location TBD)

**Fire Protection Standards:**

- **NFPA 13** — Installation of Sprinkler Systems **TBD** (location TBD)

**Source:** Decomposition REVISED_v2.md standards list; MEP calculation standards; specific editions TBD per Employer's Requirements

### Calculation Software Standards

**Approved Calculation Software** (ASSUMPTION: to be confirmed with project procedures):

- **HVAC Load Calculations**: Carrier HAP, Trane TRACE, IES VE, or equivalent approved software
- **Hydraulic Calculations (Fire Protection)**: HydraCAD, AutoSPRINK, or equivalent NFPA 13 approved software
- **General Engineering Calculations**: Excel, MathCAD, or equivalent with documented formulas

**Software Validation**: All software shall have documented validation per recognized standards (e.g., ASHRAE 140 for energy modeling software).

**Source:** ASSUMPTION: industry-standard calculation software; project approval TBD

### Employer's Requirements

- **Employer's Requirements Volume 2** — **TBD** — Project-specific calculation criteria (location TBD)

Employer's Requirements shall take precedence over general standards where conflicts exist.

## Verification

### Verification Methods

| Verification Activity | Description | Responsibility |
|----------------------|-------------|----------------|
| Input Data Verification | Verify all inputs are from approved sources and correctly transcribed | Originator |
| Methodology Review | Verify calculation method complies with applicable codes | Checker |
| Calculation Verification | Independent check of calculations (spot-check or full recalculation) | Checker (P.Eng.) |
| Software Output Review | Verify software inputs and review outputs for reasonableness | Checker |
| Code Compliance Check | Verify calculations demonstrate code compliance per FR-02, FR-03, FR-04, PR-03 | Checker |
| Results Reasonableness Check | Compare results to industry benchmarks and similar projects | Lead Engineer |
| Interface Coordination Check | Verify calculations support DEL-22.01, DEL-22.02, DEL-22.04 per IF-01/02/03 | Lead Engineer |
| Documentation Review | Verify format, completeness, traceability per QR-03 | Checker |

**Source:** Requirements sections above; ASSUMPTION: standard calculation verification process

### Acceptance Criteria

**Calculation Quality:**

- [ ] All inputs documented with sources
- [ ] All assumptions justified and reasonable
- [ ] Methodology complies with applicable codes and standards
- [ ] Calculations are traceable and reproducible
- [ ] Results are clearly summarized

**Code Compliance:**

- [ ] NBC 2020 requirements met (building loads, climate data, plumbing)
- [ ] ASHRAE 90.1 energy requirements addressed
- [ ] ASHRAE 62.1 ventilation requirements met (if applicable)
- [ ] NFPA 13 fire protection requirements met (if applicable)

**Interface Coordination:**

- [ ] Equipment sizes match DEL-22.01 drawings
- [ ] Performance requirements match DEL-22.02 specifications
- [ ] Equipment parameters match DEL-22.04 datasheets
- [ ] Interface requirements coordinated with PKG-03, PKG-17, PKG-19, PKG-21

**Quality Checks:**

- [ ] Independent check completed and signed off (QR-01)
- [ ] All checker comments resolved
- [ ] Professional engineer review completed (QR-02)
- [ ] Documentation standards met (QR-03)

**Source:** ASSUMPTION: standard calculation acceptance criteria

## Documentation

### Required Documentation Outputs

**Calculation Packages (per Decomposition DEL-22.03 anticipated artifacts):**

1. **HVAC load calculations**
2. **Plumbing sizing calculations**

**Additional Calculations (inferred from scope):**

3. **Ventilation calculations** (ASHRAE 62.1)
4. **Fire protection hydraulic calculations** (NFPA 13)

**Supporting Documentation:**

- Calculation cover sheets with signatures
- Design basis and assumptions summary
- Input data sources and references
- Software validation documentation (if software used)
- Sensitivity analysis (if required)

**Source:** Decomposition REVISED_v2.md, DEL-22.03 anticipated artifacts; inferred from MEP scope

### Documentation Format and Control

- **Native calculation format**: **TBD** — Software native format (e.g., .hap, .trc, .xlsx) or handwritten calculation sheets
- **Issued format**: PDF for issue and review
- **Calculation numbering**: **TBD** — Per project calculation numbering system
- **Revision control**: All revisions tracked per project document control procedure
- **File naming**: **TBD** — Per project file naming convention

**Filing and retention:**

- Working files: `1_Working/` (this folder)
- Issued for review: `2_Checking/To/` (review copies with DEL-ID + date/rev)
- Issued for construction: `3_Issued/` (final issued copies)

**Source:** ASSUMPTION: standard project document control conventions per README.md Section 6
