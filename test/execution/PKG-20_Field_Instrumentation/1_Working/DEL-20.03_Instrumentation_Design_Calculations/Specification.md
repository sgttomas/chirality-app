# Specification: DEL-20.03 Instrumentation Design Calculations

## Scope

This specification defines the requirements for **Instrumentation Design Calculations** within **PKG-20 Field Instrumentation** for the Canola Oil Transload Facility Phase 1 at Fraser Surrey Terminal, Surrey, BC.

**Deliverable Purpose:**

Provides the engineering basis and sizing/verification calculations for instrumentation.

**Source:** Decomposition document `/Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md`, DEL-20.03 description (line 498)

**Calculation Scope:**

This deliverable provides calculations to:
- Size instruments (ranges, capacities, physical dimensions)
- Verify instrument performance (accuracy, response time, turndown)
- Verify specification compliance (DEL-20.02 requirements are met)
- Support equipment selection (data sheet specifications per DEL-20.04)
- Verify installation requirements (mounting loads, impulse piping, winterization)

**Anticipated Calculation Artifacts:**
- Instrument sizing calculations (level, pressure, temperature, flow)

**Source:** Decomposition DEL-20.03 Anticipated Artifacts (line 498); `_CONTEXT.md`

## Requirements

### Functional Requirements

**FR-1: Calculation Completeness**

Calculations shall be provided for all instruments where sizing or verification is required. Calculations verify DEL-20.02 specification requirements and support DEL-20.04 data sheets.

**FR-2: Range Selection Calculations**

Range selection calculations verify instrument range covers normal operating range with adequate margin (typically 30-70% of span for optimal accuracy).

**FR-3: Accuracy Verification Calculations**

Total loop uncertainty (TLU) calculations demonstrate measurement accuracy meets requirements for process control, safety, or custody transfer applications.

**FR-4: Sizing Calculations**

Sizing calculations provided for flow elements, thermowells, impulse piping, and instrument mounting as applicable.

**FR-5: Installation Verification Calculations**

Installation calculations address impulse piping slope, winterization, seismic restraints per applicable codes and project location (Surrey, BC).

**Source:** **ASSUMPTION** based on typical instrumentation calculation requirements

### Performance Requirements

**PR-1: Calculation Methodology**

All calculations shall use recognized engineering methods (codes, standards, industry references), document assumptions explicitly, and show step-by-step reproducible calculations.

**PR-2: Design Margin**

Calculations shall include appropriate design margins (range margin, overpressure rating ≥2× range, accuracy budget including calibration drift).

**PR-3: Software and Tools**

Calculation software shall allow formula visibility and review (not black-box). Acceptable tools include Excel, MathCAD, and recognized specialty software.

**Source:** **ASSUMPTION** based on typical EPC calculation tool requirements

### Interface Requirements

**INT-1: Design Input Coordination**

Calculations require process design data (operating conditions, fluid properties), piping design basis (pressures, temperatures), equipment specifications, and environmental criteria.

**INT-2: Related Deliverable Coordination**

Calculations support DEL-20.02 (verify specification), DEL-20.04 (provide data sheet parameters), DEL-20.01 (installation requirements), and DEL-20.05 (test criteria).

**Source:** Decomposition PKG-20 deliverables (lines 496-500)

### Quality Requirements

**QR-1: Calculation Verification**

All calculations shall be independently checked by qualified engineer (P.Eng. or senior engineer). Check documentation includes signed check sheets.

**QR-2: Calculation Revision Control**

Calculations shall be revision-controlled with revision log. Superseded revisions archived per project document retention plan.

**QR-3: Traceability**

All calculation inputs referenced to source documents. Calculation numbers cross-referenced in related deliverables.

**QR-4: Professional Seal**

**TBD** — Professional seal requirements per Employer's Requirements and BC regulations (Engineers and Geoscientists BC).

**Source:** **ASSUMPTION** based on typical Canadian professional practice

## Standards

**Instrumentation Calculation Standards:**

- ISA 5.1, ISA 84 / IEC 61511, API 554, API 2350
- API 14.3 / ISO 5167 (flow element sizing)
- API MPMS (custody transfer metering)
- ASME PTC 19.3 (thermowell design)
- NBC 2015 (seismic loads for Surrey, BC)

**Note:** Specific standards **TBD** based on calculation requirements. Calculations shall cite specific standard sections used.

## Verification

**Verification Methods:**

All calculations require self-check + independent check. Safety-critical calculations may require third-party review. Software calculations require input/output verification.

**Acceptance Criteria:**

Calculations acceptable when: methodology appropriate, inputs documented and traceable, assumptions explicit, calculations reproducible, results meet specification, independent check complete with sign-off.

**Source:** **ASSUMPTION** based on typical calculation acceptance criteria

## Documentation

**Required Documentation Outputs:**

1. **Instrument Sizing Calculations**
   - Format: **TBD** — Calculation sheets (Excel, MathCAD, PDF)
   - Content: Range selection, accuracy verification, sizing calculations
   - Organization: **TBD** — By instrument type or calculation number

**Supporting Documentation:**

- Calculation index
- Design basis summary
- Vendor data references
- Check sheets

**Project Objective Alignment:**

Supports **OBJ-1: Safe & Reliable Operation** — Proper sizing and verification calculations ensure instruments are correctly specified for safe and reliable facility operations.

**Source:** Decomposition Section 6 (line 780)

## Cross-Document Traceability

This Specification defines requirements for DEL-20.03. The following documents provide complementary information:

| Document | Purpose | Key Linkages |
|----------|---------|--------------|
| Datasheet.md | Factual identification, attributes, conditions, references | Conditions § provides design basis; Construction § defines calculation types and format |
| Guidance.md | Engineering rationale and decision context | Principles explain calculation approach; Trade-offs address methodology decisions |
| Procedure.md | Production workflow and verification steps | Steps 1-6 implement FR-1 to FR-5; Verification implements QR-1 to QR-4 |

**Requirement-to-Procedure Mapping:**

| Requirement | Procedure Step | What Is Implemented |
|-------------|----------------|---------------------|
| FR-1 Completeness | Step 1 | Calculation scope identification |
| FR-2 Range Selection | Step 3.1 | Range selection methodology |
| FR-3 Accuracy Verification | Step 3.2 | TLU calculations |
| FR-4 Sizing | Step 3.3 | Flow element, thermowell sizing |
| FR-5 Installation | Step 3.4 | Impulse piping, seismic calculations |
| QR-1 Verification | Step 5 | Independent check process |
