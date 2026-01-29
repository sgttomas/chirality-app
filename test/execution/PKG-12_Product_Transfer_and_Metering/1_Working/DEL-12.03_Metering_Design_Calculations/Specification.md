# Specification: DEL-12.03 Metering Design Calculations

## Scope

### Deliverable Definition

This specification defines the requirements for the **Metering Design Calculations** deliverable within **PKG-12 Product Transfer & Metering**.

DEL-12.03 provides the engineering basis and sizing/verification calculations for custody transfer metering (Source: Decomposition:358).

### Package Scope Context

PKG-12 scope covers custody transfer flow meters (rail unloading and marine loading) and metering instrumentation (Source: Decomposition:350).

The facility transfers CSD (Crude Super Degummed) canola oil from rail tank cars to storage tanks (via rail unloading metering) and from storage tanks to liquid bulk carriers for export (via marine loading metering), with a permitted throughput of 1,000,000 MT per annum (Source: Decomposition:41, 43).

### Inclusions

The calculation package shall include, at minimum:

| Artifact | Description | Source |
|----------|-------------|--------|
| Flow Meter Sizing | Meter size selection based on flow range, product properties, pressure drop calculation, turndown ratio verification; separate sizing for rail unloading and marine loading services | Decomposition:358 |
| Accuracy / Uncertainty Calculations | Uncertainty budget development, uncertainty component identification and quantification, uncertainty propagation per applicable standard, combined expanded uncertainty calculation, accuracy class verification | Decomposition:358 |
| Proving Calculations | Proving method selection basis (in-line prover, portable prover, master meter), prover sizing if applicable, proving repeatability requirements, meter factor acceptance criteria, proving frequency rationale | Decomposition:358 |

### Exclusions

The following are outside the scope of DEL-12.03:

- Detailed vendor-specific sizing (captured in vendor proprietary sizing tools and submitted data; calculations use vendor results as inputs or verify vendor sizing)
- Control system logic calculations (covered in PKG-19 Control Systems)
- Piping hydraulic calculations beyond metering pressure drop (covered in PKG-14 Process Piping; metering calculations provide pressure drop as input to piping hydraulics)
- Electrical load calculations (covered in PKG-17 Electrical)

## Requirements

### Functional Requirements

| Req ID | Requirement | Source | Verification |
|--------|-------------|--------|--------------|
| REQ-01 | The calculation package shall document basis, inputs, assumptions, methodology, and results for custody transfer metering design in a structured calculation report format | ASSUMPTION based on Decomposition:358 and engineering calculation standards | Document review per Procedure.md Step 8 |
| REQ-02 | The calculation package shall cover both rail unloading and marine loading metering services with separate analysis for each service where service-specific conditions differ | Decomposition:350 | Checklist review per Procedure.md Step 1; verify both services addressed |
| REQ-03 | The calculation package shall include all decomposition-listed artifacts: (1) flow meter sizing, (2) accuracy calculations, (3) proving calculations | Decomposition:358 | Checklist review; verify all three calculation types present |
| REQ-04 | All calculation inputs shall be documented with sources (ER clause numbers, DEL-12.02 specification references, design basis document references, vendor data references, standard references) | ASSUMPTION; traceability requirement | Input table review per Procedure.md Step 2.6 |
| REQ-05 | All assumptions shall be stated explicitly with rationale; unknowns shall be marked TBD with source needed | Epistemic rule | Assumption review per Procedure.md Step 2 |

### Performance Requirements

| Req ID | Requirement | Source | Verification |
|--------|-------------|--------|--------------|
| REQ-06 | Calculations shall demonstrate meter sizing supports OBJ-2 (1,000,000 MT/a throughput) by verifying: (a) meter flow capacity accommodates design flow rates for rail unloading and marine loading, (b) meter pressure drop does not excessively constrain system hydraulics, (c) meter turndown ratio accommodates flow variations | Decomposition:781 | Technical review per Procedure.md Step 3.5; verify throughput alignment |
| REQ-07 | Calculations shall demonstrate accuracy/uncertainty meets OBJ-10 (Custody Transfer Accuracy) by: (a) developing uncertainty budget per applicable standard, (b) calculating combined expanded uncertainty, (c) verifying combined uncertainty meets accuracy requirement from DEL-12.02 specification | Decomposition:789 | Technical review per Procedure.md Step 4.6; verify accuracy alignment |
| REQ-08 | Accuracy class and acceptance criteria shall be per ER Vol 2 Part 2 and DEL-12.02 specification | TBD; ER Vol 2 Part 2, location TBD; DEL-12.02 specification | Technical review; cross-check with DEL-12.02 per Procedure.md Step 6 |
| REQ-09 | Calculations shall demonstrate meter turndown ratio accommodates expected flow variations from minimum to maximum flow rates for each service without accuracy degradation beyond specified limits | ASSUMPTION based on custody transfer requirements | Technical review per Procedure.md Step 3.4; verify turndown |
| REQ-10 | Calculations shall verify meter pressure drop at maximum flow is within acceptable limits to avoid constraining system hydraulic capacity | ASSUMPTION; coordinate with PKG-14 piping hydraulics | Technical review per Procedure.md Step 3.3; pressure drop verification |

### Methodology Requirements

| Req ID | Requirement | Source | Verification |
|--------|-------------|--------|--------------|
| REQ-11 | Flow meter sizing calculations shall use recognized methodology: manufacturer sizing tools, first-principles calculations, or industry-standard methods; methodology shall be clearly documented | ASSUMPTION | Methodology review per Procedure.md Step 3 |
| REQ-12 | Uncertainty analysis shall follow recognized custody transfer uncertainty methodology: API MPMS Chapter 13, OIML R117, ISO GUM, or other applicable standard; methodology shall be cited | ASSUMPTION; standard-based requirement | Methodology review per Procedure.md Step 4.3; verify standard citation |
| REQ-13 | Proving calculations shall cite applicable proving standard for methodology and acceptance criteria: API MPMS Chapter 4, OIML R117, Measurement Canada regulations, or other | ASSUMPTION; standard-based requirement | Methodology review per Procedure.md Step 5; verify standard citation |

### Interface Requirements

| Req ID | Requirement | Source | Verification |
|--------|-------------|--------|--------------|
| REQ-14 | Calculations shall clearly state boundary conditions and interface assumptions including: (a) upstream and downstream pressure conditions, (b) flow control philosophy (constant flow, variable flow, batch operation), (c) proving method constraints (space availability, operational schedule), (d) temperature control assumptions | ASSUMPTION based on calculation best practices | Boundary condition review per Procedure.md Step 2; verify assumptions documented |
| REQ-15 | Calculation results shall be cross-checked with DEL-12.02 specification requirements; any conflicts or performance shortfalls shall be flagged for resolution | ASSUMPTION; cross-document consistency | Cross-check per Procedure.md Step 6; verify consistency with DEL-12.02 |
| REQ-16 | Calculation implications for other deliverables shall be documented: (a) DEL-12.01 drawings (meter sizes, straight-run requirements, proving connections), (b) DEL-12.04 data sheets (flow ranges, accuracy class), (c) DEL-12.05 test records (acceptance criteria) | ASSUMPTION; downstream traceability | Implications review per Procedure.md Step 8.3; verify downstream links documented |
| REQ-17 | Interface coordination with adjacent packages (PKG-14 piping hydraulics for pressure drop, PKG-10/PKG-11 for flow rates) is managed externally per dependency mode NOT_TRACKED | _DEPENDENCIES.md | Coordination meeting; verify pressure drop provided to PKG-14 |

### Quality Requirements

| Req ID | Requirement | Source | Verification |
|--------|-------------|--------|--------------|
| REQ-18 | Calculations shall be independently checked by a qualified Process engineer (not the originator); checker shall verify inputs, methodology, calculations, and results | TBD; ER Vol 2 Part 1, location TBD; ASSUMPTION based on engineering standards | Check record per Procedure.md Step 9; verify checker signature |
| REQ-19 | Calculation report shall include revision history documenting: revision number, date, description of changes, originator, checker, approver | ASSUMPTION; document control requirement | Revision history review; verify revision tracking |
| REQ-20 | Calculations shall include clear list of inputs with sources, assumptions with rationale, and references to standards/codes applied | ASSUMPTION; traceability and auditability | Input table and assumption list review per Procedure.md Step 2 |
| REQ-21 | All work shall comply with project Quality Management Plan | ASSUMPTION | QA/QC audit |
| REQ-22 | Calculation units shall be consistent and clearly stated; unit conversions shall be shown and verified | ASSUMPTION; calculation quality requirement | Unit consistency check per Procedure.md Step 9.3 |

### Sensitivity Analysis Requirements

| Req ID | Requirement | Source | Verification |
|--------|-------------|--------|--------------|
| REQ-23 | Calculations shall include sensitivity analysis for key parameters: (a) flow rate variation (accuracy at minimum vs. maximum flow), (b) temperature variation (compensation error at extremes), (c) other critical parameters identified during calculation development | ASSUMPTION; risk identification | Sensitivity analysis review per Procedure.md Step 7 |
| REQ-24 | Sensitivity analysis shall identify critical assumptions and parameters where small variations significantly impact results; risks shall be documented | ASSUMPTION; risk management | Sensitivity results review per Procedure.md Step 7.4 |

## Standards

### Governing References

| Standard/Reference | Applicability | Source |
|--------------------|---------------|--------|
| Employer's Requirements Vol 2 Part 1 | General requirements, document control, calculation standards, quality procedures | TBD |
| Employer's Requirements Vol 2 Part 2 | Process mechanical requirements, metering requirements, flow rates, operating conditions, fluid properties, accuracy requirements, proving requirements | TBD |
| Project Document Control Procedures | Calculation numbering, revision control, approval requirements | TBD |
| Project Quality Management Plan | Calculation check procedures, approval authorities | TBD |

### Custody Transfer Metering Standards (TBD — ASSUMPTION)

Applicable standards for sizing methodology, uncertainty analysis, and proving requirements; specific applicability TBD from ER Vol 2 Part 2 and DEL-12.02 specification:

| Standard | Description | Potential Applicability |
|----------|-------------|------------------------|
| API MPMS Chapter 4 (Proving Systems) | Proving system design, operation, and maintenance; prover types (tank provers, pipe provers, master meter provers); proving procedures; acceptance criteria | Applicable if API MPMS is governing standard; provides methodology for proving calculations (prover sizing, proving repeatability, acceptance criteria) |
| API MPMS Chapter 5 (Metering) | Metering system design and installation; meter types (displacement, turbine, Coriolis, ultrasonic); installation requirements (straight-run, orientation) | Applicable if API MPMS is governing standard; provides meter sizing guidance and installation requirements |
| API MPMS Chapter 11 (Physical Properties) | Temperature and pressure effects on volume; density, thermal expansion, compressibility | Applicable for temperature and pressure compensation in accuracy calculations |
| API MPMS Chapter 13 (Statistical Aspects of Measuring and Sampling) | Uncertainty analysis for custody transfer measurement; uncertainty sources, propagation, reporting | Applicable for uncertainty budget development; comprehensive framework for custody transfer uncertainty; likely primary reference for REQ-12 |
| OIML R117 (Dynamic Measuring Systems for Liquids Other Than Water) | Accuracy classes (0.3, 0.5, 1.0, 1.5, 2.5); uncertainty requirements; installation requirements; proving/verification requirements | Likely primary standard for vegetable oil custody transfer; provides accuracy framework and uncertainty methodology |
| ISO GUM (Guide to the Expression of Uncertainty in Measurement) | General uncertainty framework; Type A (statistical) and Type B (systematic) uncertainties; uncertainty propagation; coverage factors | General uncertainty methodology applicable if metering-specific standard does not prescribe approach; may be used in conjunction with API MPMS Chapter 13 or OIML R117 |
| Measurement Canada (Weights and Measures Act, Regulations, and Specifications) | Canadian regulatory requirements for custody transfer; meter approval, periodic verification, proving requirements | Applicable for custody transfer in Canada; may prescribe specific calculation requirements or acceptance criteria |
| ISO 4185 (Measurement of Liquid Flow in Closed Conduits — Weighing and Volumetric Methods) | Reference methods for flowmeter calibration | May be applicable for proving system design and uncertainty |

**Note:** Standard applicability and specific clauses to be confirmed from ER Vol 2 Part 2 and DEL-12.02 specification. Calculations shall cite specific standard clauses for methodology (REQ-11, REQ-12, REQ-13).

## Verification

### Verification Methods

| Method | Description | Applicable Requirements |
|--------|-------------|------------------------|
| Document Review | Review calculation report for completeness, structure, documentation of inputs/assumptions/methodology/results | REQ-01, REQ-02, REQ-03, REQ-04, REQ-05, REQ-14, REQ-16, REQ-19, REQ-20 |
| Technical Review | Review calculations for technical correctness: verify inputs are reasonable, methodology is appropriate, calculations are correct, results are sensible | REQ-06, REQ-07, REQ-08, REQ-09, REQ-10, REQ-11, REQ-12, REQ-13 |
| Cross-Document Check | Verify calculation inputs align with DEL-12.02 specification requirements; verify calculation results are reflected in DEL-12.01 drawings and DEL-12.04 data sheets | REQ-08, REQ-15, REQ-16 |
| Independent Check | Independent engineer verifies all calculations: re-perform key calculations, verify methodology, check unit consistency, verify results | REQ-18, REQ-22 |
| Sensitivity Analysis Review | Review sensitivity analysis for completeness and identification of critical parameters and risks | REQ-23, REQ-24 |
| Standard Compliance Check | Verify calculations cite applicable standards and follow standard-prescribed methodology | REQ-11, REQ-12, REQ-13 |

### Acceptance Criteria

| Criterion | Description | Source |
|-----------|-------------|--------|
| Artifact Completeness | All three calculation types present: (1) flow meter sizing (rail and marine), (2) accuracy/uncertainty calculations (rail and marine), (3) proving calculations | Decomposition:358; REQ-03 |
| Service Coverage | Both rail unloading and marine loading services addressed with separate analysis where conditions differ | REQ-02 |
| Technical Correctness | Calculations verified by independent checker; methodology appropriate; calculations correct; units consistent; results reasonable | REQ-18, REQ-22 |
| Input Traceability | All inputs documented with sources; assumptions stated with rationale; TBDs flagged | REQ-04, REQ-05, REQ-20 |
| Methodology Citation | Calculation methodology cites applicable standards (API MPMS, OIML R117, ISO GUM, Measurement Canada) | REQ-11, REQ-12, REQ-13 |
| Objective Alignment | Results demonstrate support for OBJ-2 (throughput): meter sizing accommodates design flow rates without excessive constraints; results demonstrate support for OBJ-10 (accuracy): combined uncertainty meets accuracy requirement | REQ-06, REQ-07 |
| Specification Consistency | Calculation inputs align with DEL-12.02 specification; calculation results meet specification requirements; conflicts flagged | REQ-08, REQ-15 |
| Downstream Implications | Implications for DEL-12.01, DEL-12.04, DEL-12.05 documented | REQ-16 |
| Sensitivity Analysis | Sensitivity analysis performed for key parameters; critical assumptions and risks identified | REQ-23, REQ-24 |
| Check Records Complete | Independent check record complete with checker signature confirming verification | REQ-18 |

## Documentation

### Required Documentation Outputs

| Output | Description | Source |
|--------|-------------|--------|
| Flow Meter Sizing Calculation | Calculation report documenting meter size selection for rail unloading and marine loading services based on flow range, product properties, pressure drop, and turndown | Decomposition:358; REQ-03, REQ-06, REQ-09, REQ-10 |
| Accuracy / Uncertainty Calculation | Calculation report documenting uncertainty budget, uncertainty components, uncertainty propagation methodology, combined expanded uncertainty, and accuracy class verification | Decomposition:358; REQ-03, REQ-07, REQ-12 |
| Proving Calculation | Calculation report documenting proving method selection, prover sizing (if applicable), proving repeatability, meter factor acceptance criteria, and proving frequency rationale | Decomposition:358; REQ-03, REQ-07, REQ-13 |
| Independent Check Record | Record documenting independent check completion with checker signature, check comments, and comment resolution | REQ-18 |

### Calculation Report Structure

The calculation report(s) should include the following sections to satisfy requirements (per Datasheet.md Construction section; ASSUMPTION based on typical calculation report structure):

| Section | Content | Requirements Addressed |
|---------|---------|----------------------|
| 1. Purpose and Scope | Calculation objectives, services covered (rail unloading, marine loading), CSD canola oil product, custody transfer application | REQ-01, REQ-02 |
| 2. Inputs and Sources | ER requirements (cite clause numbers), DEL-12.02 specification (cite requirements), product properties (cite source), flow rates (cite source), operating conditions (cite source), standards and codes (cite clause numbers), vendor data (cite vendor and document) | REQ-04, REQ-05, REQ-20 |
| 3. Assumptions and Boundary Conditions | Stated assumptions with rationale; TBD items flagged; boundary conditions (upstream/downstream pressure, flow control, proving constraints, temperature control) | REQ-05, REQ-14, REQ-20 |
| 4. Methodology | Sizing methodology (manufacturer tools, first-principles, standard methods; cite approach), uncertainty methodology (API MPMS Ch 13, OIML R117, ISO GUM; cite standard), proving methodology (cite standard), calculation tools and software | REQ-11, REQ-12, REQ-13 |
| 5. Flow Meter Sizing Calculations | Rail unloading: flow rates, product properties, meter technology, meter size, pressure drop, turndown verification; Marine loading: same structure; results comparison | REQ-03, REQ-06, REQ-09, REQ-10 |
| 6. Accuracy / Uncertainty Analysis | Uncertainty budget (list components), uncertainty component quantification (meter, temperature, pressure, density, proving), uncertainty propagation per standard, combined standard uncertainty, coverage factor application, expanded uncertainty, accuracy verification | REQ-03, REQ-07, REQ-12 |
| 7. Proving Basis | Proving method selection rationale, prover sizing (if in-line prover), proving frequency rationale, meter factor acceptance criteria (cite standard), proving uncertainty contribution | REQ-03, REQ-07, REQ-13 |
| 8. Sensitivity Analysis | Flow rate sensitivity (min vs. max flow accuracy), temperature sensitivity (compensation error), other parameter sensitivities, critical assumptions identification, risk documentation | REQ-23, REQ-24 |
| 9. Results Summary | Meter sizing results (sizes, pressure drops, turndowns), accuracy results (combined uncertainties, compliance with requirements), proving results (method, frequency, criteria), conclusions (OBJ-2 and OBJ-10 alignment) | REQ-01, REQ-06, REQ-07 |
| 10. Implications for Other Deliverables | DEL-12.01 implications (meter sizes, straight-runs, proving connections), DEL-12.02 cross-check (conflicts flagged), DEL-12.04 implications (flow ranges, accuracy class), DEL-12.05 implications (acceptance criteria) | REQ-15, REQ-16 |
| 11. References | Standards and codes cited, project documents cited, vendor data cited, technical literature if applicable | REQ-04, REQ-11, REQ-12, REQ-13 |
| 12. Revision History | Revision number, date, description of changes, originator, checker, approver | REQ-19 |
| Appendices | Detailed calculation sheets, vendor tool outputs, uncertainty budget tables, sensitivity analysis details, standard excerpts | Supporting documentation |

### Documentation Requirements

| Requirement | Description | Source |
|-------------|-------------|--------|
| Calculation Summary | Executive summary with key results traceable to procurement and installation decisions | REQ-01; facilitate downstream use |
| Input Documentation | All inputs in table format with values, units, and sources | REQ-04, REQ-20 |
| Assumption Documentation | All assumptions stated with rationale; TBD items flagged with source needed | REQ-05, REQ-20 |
| Methodology Documentation | Calculation methodology clearly described; standards cited; tools/software identified | REQ-11, REQ-12, REQ-13 |
| Unit Consistency | Units clearly stated throughout; unit conversions shown and verified | REQ-22 |
| Cross-Reference | Reference DEL-12.02 specification requirements; document implications for DEL-12.01, DEL-12.04, DEL-12.05 | REQ-08, REQ-15, REQ-16 |
| Revision Control | Per project document control procedures; revision history documented | REQ-19; TBD ER Vol 2 Part 1 |

## Cross-Document Traceability

| Document | Traceability Points |
|----------|---------------------|
| Datasheet.md | Identification section defines calculation attributes (number, software/tools, design code/standard basis, revision); Conditions section lists design context (service application, product, throughput, metering points) and all calculation input parameters with TBD sources matching REQ-04; Construction section lists anticipated calculation content (sizing, accuracy, proving) matching REQ-03 and defines calculation methodology and report structure matching Documentation section above |
| Guidance.md | Purpose section explains calculations provide engineering basis for meter selection, accuracy verification, and proving methodology, driving DEL-12.01, DEL-12.04, DEL-12.05 per REQ-16; Principles section explains calculation development rationale (objective demonstration per REQ-06/REQ-07, traceability per REQ-04, auditability per REQ-18) and methodology principles (sizing per REQ-11, uncertainty per REQ-12, proving per REQ-13); Considerations section identifies factors affecting sizing (flow range, product properties, pressure drop, turndown, meter technology), accuracy/uncertainty (uncertainty components, propagation), proving (method, size, frequency, criteria), and service-specific considerations (rail vs. marine per REQ-02) |
| Procedure.md | Steps section defines calculation workflow aligned to requirements: Step 1 (Define cases per REQ-02), Step 2 (Collect inputs per REQ-04 and document assumptions per REQ-05), Step 3 (Perform sizing per REQ-06, REQ-09, REQ-10, REQ-11), Step 4 (Perform accuracy/uncertainty per REQ-07, REQ-12), Step 5 (Perform proving per REQ-07, REQ-13), Step 6 (Cross-check with DEL-12.02 per REQ-15), Step 7 (Perform sensitivity per REQ-23, REQ-24), Step 8 (Assemble report per REQ-01, REQ-16, REQ-19, REQ-20), Step 9 (Independent check per REQ-18, REQ-22); Verification section confirms requirement satisfaction per Acceptance Criteria; Records section identifies calculation outputs matching Documentation section |
