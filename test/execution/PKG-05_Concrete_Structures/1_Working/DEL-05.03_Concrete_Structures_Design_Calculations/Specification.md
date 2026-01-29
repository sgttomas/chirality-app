# Specification: DEL-05.03 Concrete Structures Design Calculations

## Scope

This deliverable defines the engineering basis and sizing/verification calculations for concrete structures within PKG-05. (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:234.)

**Package scope context:** foundations, containment walls, equipment pads, thrust blocks, ground liner system. (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:226.)

**Project context:** Canola Oil Transload Facility Phase 1, Fraser Surrey Terminal, Surrey, BC. Design & Build contract. Storage capacity 45,000 MT (3 × 15,000 MT tanks). (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:10; test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:44; test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:41-42.)

**Anticipated calculation artifacts:**
- Foundation calculations (tank foundations, equipment pads, building foundations, thrust blocks)
- Containment wall calculations (structural design, serviceability, seismic)
- Seismic analysis (design basis, methodology, element-specific analysis)

(Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:234; Datasheet.md: Construction.)

**Exclusions:**
- Employer-responsible items except for interface connections. (Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:49.)
- Building interior structural calculations (covered under PKG-21/PKG-22 if applicable).
- Marine structures calculations (covered under PKG-08 if applicable).

## Requirements

### Functional Requirements

**FR-01: Calculation Artifact Coverage**
The calculation package shall include three core calculation sets:
1. Foundation calculations (tank foundations, equipment pads, building foundations if in scope, thrust blocks)
2. Containment wall calculations (structural design, serviceability, seismic)
3. Seismic analysis (design basis, methodology, element-specific analysis)
Each calculation set shall include design basis, assumptions, methodology, results, and verification.
(Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:234; Datasheet.md: Construction.)

**FR-02: Design Basis and Assumptions Documentation**
The calculation package shall document:
- Design basis statement (Employer's Requirements references, applicable codes/standards)
- Input data register (loads, geotechnical properties, material properties, code parameters)
- Assumptions register (provisional parameters, interface assumptions, TBD items)
- Load combination summary (governing load cases by element type)
- Design criteria (strength, serviceability, durability) with source citations
**Note:** Assumptions and TBD items shall be clearly identified for future resolution and interdisciplinary coordination.
(Source: test/Volume_2_Part_1_Employers_Requirements.pdf, location TBD; Guidance.md: Principles; Procedure.md: Prerequisites.)

**FR-03: Foundation Calculations**
The calculation package shall include foundation calculations for:
- **Tank foundations (3 × 15,000 MT tanks):**
  - Bearing capacity verification under dead, live, product storage, and seismic loads
  - Settlement analysis (total and differential settlement within allowable limits)
  - Foundation sizing (diameter, thickness) with optimization considerations
  - Reinforcement design (bottom mat, top mat if applicable, edge reinforcement)
  - Seismic analysis (overturning, sliding, bearing pressure under seismic loads)
- **Equipment pad foundations:**
  - Bearing capacity verification for equipment loads (pumps, meters, unloading equipment)
  - Settlement analysis and tolerance verification
  - Pad sizing and reinforcement design
  - Anchor bolt design (tension, shear, combined loading, pullout verification)
  - Dynamic loading analysis for vibrating equipment if applicable (**TBD** equipment list)
- **Building foundations** (if within PKG-05 scope — **TBD** scope boundary)
- **Thrust blocks:**
  - Piping thrust load analysis (coordinate with PKG-14)
  - Passive soil resistance verification
  - Block sizing and reinforcement design
  - Sliding and overturning stability
(Source: Datasheet.md: Construction; test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:226; test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:41-42.)

**FR-04: Containment Wall Calculations**
The calculation package shall include containment wall calculations for:
- **Structural design:**
  - Earth pressure analysis (active/at-rest/passive pressures as applicable)
  - Hydrostatic pressure analysis (product containment scenarios for OBJ-7)
  - Wall sizing (height, thickness, base width/footing if applicable)
  - Reinforcement design (vertical bars, horizontal bars, joint reinforcement)
  - Foundation bearing capacity and sliding stability verification
  - Overturning stability verification
- **Serviceability analysis (OBJ-7 Environmental Protection):**
  - Crack control analysis (crack width limits for containment integrity — **TBD** limits from ERs)
  - Joint design (construction joints, control joints, expansion joints — spacing and details)
  - Waterproofing and liner interface considerations
  - Leakage pathway evaluation and mitigation
- **Seismic analysis:**
  - Dynamic earth pressure (Mononobe-Okabe method or equivalent)
  - Seismic overturning and sliding stability
  - Seismic reinforcement detailing requirements (ductility, confinement)
- **Containment volume verification:**
  - Verify containment volume supports OBJ-3 (45,000 MT storage capacity)
  - Freeboard analysis and spillage scenario evaluation
(Source: Datasheet.md: Construction; test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:786; test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:41-42.)

**FR-05: Seismic Analysis**
The calculation package shall include seismic analysis covering:
- **Seismic design basis:**
  - Seismic zone and site class determination (BC location)
  - Spectral acceleration values (Sa(0.2), Sa(1.0), or equivalent)
  - Importance factors (likely elevated for storage facility)
  - Ductility and overstrength factors (R values) by element type
  - Drift limits and deformation criteria
- **Seismic analysis methodology:**
  - Justify methodology selection (equivalent static vs dynamic analysis)
  - Define load combinations with seismic effects
  - Define seismic detailing requirements
- **Element-specific seismic analysis:**
  - Tank foundations under seismic loads (overturning, sliding, bearing pressure)
  - Containment walls under seismic earth pressure (dynamic increment)
  - Equipment pads under seismic equipment loads (anchor bolt verification)
  - Thrust blocks under seismic piping loads
- **Seismic performance verification:**
  - Strength verification under seismic load combinations
  - Deformation/drift verification (if applicable)
  - Detailing requirements for ductile behavior (confinement, lap splices, anchorage)
(Source: Datasheet.md: Construction; Datasheet DEL-05.01: Conditions; test/Volume_2_Part_2_Employers_Requirements.pdf, location TBD.)

**FR-06: Calculation Results and Verification**
The calculation package shall provide:
- Calculation results summary tables (element sizing, reinforcement quantities, demand/capacity ratios)
- Governing load cases identification (which combination controls design)
- Design verification statement (confirm adequacy per code requirements)
- Recommendations for drawings and specifications (element sizes, reinforcement details, construction notes)
- Sensitivity analysis or parametric study if critical assumptions are uncertain (**TBD** if required)
(Source: test/Volume_2_Part_1_Employers_Requirements.pdf, location TBD; Datasheet.md: Construction.)

### Performance Requirements

**PR-01: Strength and Serviceability Verification**
Calculations shall verify both strength and serviceability criteria:
- **Strength:** Ultimate limit state verification per design code (factored loads and resistances)
- **Serviceability:** Service limit state verification (crack control, settlement, deflection, vibration if applicable)
- **Containment serviceability:** Special emphasis on crack control for containment walls (OBJ-7 Environmental Protection) — **TBD** crack width limits from ERs
- **Settlement limits:** Foundation settlement within allowable limits for equipment operation and tank performance — **TBD** limits from ERs
(Source: test/Volume_2_Part_2_Employers_Requirements.pdf, location TBD; Datasheet.md: Conditions; test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:786.)

**PR-02: Seismic Performance**
Calculations shall verify seismic performance appropriate to BC seismic zone and facility importance:
- Seismic design per applicable code (likely NBCC or BC Building Code)
- Importance factors reflect facility function (storage of hazardous/valuable product)
- Ductile detailing requirements identified where applicable
- Seismic deformation limits verified (drift, overturning stability margins)
- **TBD:** Specific seismic design parameters from Employer's Requirements and design basis
(Source: Datasheet.md: Construction; test/Volume_2_Part_2_Employers_Requirements.pdf, location TBD.)

**PR-03: Alignment with Project Objectives**
Calculations shall support project objectives:
- **OBJ-3 (Storage Capacity 45,000 MT):** Foundation and containment designs support intended storage capacity
- **OBJ-7 (Environmental Protection):** Containment wall serviceability analysis ensures leak prevention
- **OBJ-9 (Lifecycle Cost Optimization):** Design optimization balances initial cost with long-term durability and maintenance
(Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:782; test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:786.)

### Interface Requirements

**IR-01: Dependency Coordination**
Dependencies are coordinated externally (NOT_TRACKED mode). Calculations shall coordinate with:
- **DEL-05.01 (Design Drawing Set):** Calculation results (element sizing, reinforcement) shall align with drawing dimensions and details
- **DEL-05.02 (Technical Specification):** Material properties assumed in calculations (concrete strength, modulus) shall align with specification values
- **DEL-02.04 (Geotechnical Reports):** Foundation calculations shall use geotechnical parameters from investigation reports (PKG-02)
- **Equipment packages (PKG-10, PKG-11, PKG-13, PKG-15):** Equipment loads and anchor bolt requirements shall be obtained from equipment vendors
- **PKG-14 (Process Piping):** Piping support loads and thrust block requirements shall be obtained from piping design
(Source: `_DEPENDENCIES.md`; test/execution/_Coordination/_COORDINATION.md; test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:232; test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:233; Procedure.md: Prerequisites.)

**IR-02: Assumption Identification and Coordination**
Calculations shall identify assumptions that require interdisciplinary coordination:
- Provisional loads where equipment data is not yet available (document assumptions and flag for update)
- Provisional geotechnical parameters if investigation is incomplete (document assumptions and flag for update)
- Interface elevations and connection details (coordinate with drawings during IDC)
- Construction sequencing assumptions if relevant to design (coordinate with construction methodology)
**Note:** Assumptions register shall be maintained and updated as inputs are confirmed.
(Source: Guidance.md: Principles; Procedure.md: Steps; test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:49.)

### Quality Requirements

**QR-01: Document Control**
The calculation package shall comply with project document control requirements (**TBD** pending clause extraction):
- Calculation numbering per project document control system
- Revision tracking and approval workflow
- Calculation format standards (cover sheet, index, summary, detailed calculations)
- Metadata consistency with Datasheet
(Source: test/Volume_2_Part_1_Employers_Requirements.pdf, location TBD; Datasheet.md: Attributes.)

**QR-02: Independent Check**
The calculation package shall include independent check evidence:
- Independent checker review (not the originator)
- Check comments and resolutions documented
- Checker sign-off on calculation package
- Check scope includes: logic, units, load cases, code compliance, arithmetic verification
- **TBD:** Specific check forms and procedures from project QA/QC requirements
(Source: test/Volume_2_Part_1_Employers_Requirements.pdf, location TBD; Procedure.md: Verification.)

**QR-03: Traceability**
Calculations shall be traceable and reproducible:
- All inputs clearly identified with sources
- All assumptions clearly stated
- All code references cited with clause numbers
- All calculation steps documented (or software input/output files retained)
- Results summarized for easy verification
- Checker shall be able to reproduce key results independently
(Source: Guidance.md: Principles; test/Volume_2_Part_1_Employers_Requirements.pdf, location TBD.)

## Standards

**Governing requirements:** Employer's Requirements Volume 2 Part 2 (concrete/structural requirements) is the authoritative source; specific referenced codes/standards to be extracted (**TBD**). (Source: test/Volume_2_Part_2_Employers_Requirements.pdf, location TBD.)

**Applicable design codes and standards (**TBD** — to be confirmed from Employer's Requirements and design basis):**
- Concrete design: likely CSA A23.3 (Design of Concrete Structures)
- Building code: likely BC Building Code / NBCC (loads, seismic, structural design requirements)
- Foundation design: likely CSA foundation design standards or Canadian Foundation Engineering Manual
- Geotechnical design: likely Canadian Geotechnical Society guidelines
- Seismic design: likely NBCC seismic provisions or CSA seismic design standards
- Load standards: likely NBCC Part 4 (Structural Design) or CSA loading standards

**ASSUMPTION:** British Columbia location suggests Canadian codes/standards (CSA, NBCC); to be confirmed from Employer's Requirements.

**Calculation software:** Calculation methodology and software selection shall be appropriate to element type and complexity. Software validation and verification per project QA requirements (**TBD**). (Source: Datasheet.md: Attributes; Procedure.md: Steps.)

**Document control standards:** Employer's Requirements Volume 2 Part 1 (general requirements) defines QA/document control conventions for calculations; clause locations TBD. (Source: test/Volume_2_Part_1_Employers_Requirements.pdf, location TBD.)

## Verification

**Completeness Verification:**
- Verify calculation package includes all anticipated artifacts (foundations, containment walls, seismic) per FR-01.
- Verify each calculation includes design basis, assumptions, methodology, results, and verification per FR-02.
- Verify all PKG-05 elements are covered (tank foundations, equipment pads, containment walls, thrust blocks).
(Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:234; Datasheet.md: Construction; Procedure.md: Verification.)

**Alignment Verification:**
- Verify calculation results align with DEL-05.01 (drawing dimensions, reinforcement details) per IR-01.
- Verify material properties align with DEL-05.02 (specification values) per IR-01.
- Verify geotechnical inputs align with DEL-02.04 (geotechnical reports) per IR-01.
(Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:232; test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:233; Procedure.md: Verification.)

**Performance Verification:**
- Verify strength and serviceability criteria are met per PR-01.
- Verify seismic performance criteria are met per PR-02.
- Verify containment wall crack control supports OBJ-7 Environmental Protection per PR-01, PR-03.
- Verify foundation settlement is within allowable limits per PR-01.
(Source: test/Volume_2_Part_2_Employers_Requirements.pdf, location TBD; Procedure.md: Verification.)

**Quality Verification:**
- Verify independent check is complete with findings addressed per QR-02.
- Verify traceability (inputs, assumptions, references clearly documented) per QR-03.
- Verify document control metadata matches Datasheet per QR-01.
(Source: test/Volume_2_Part_1_Employers_Requirements.pdf, location TBD; Datasheet.md: Attributes; Procedure.md: Verification.)

**Requirements Coverage Verification:**
- Verify each requirement in this Specification (FR-01 through QR-03) is addressed by calculation content.
- Verify each calculation output maps to a Procedure step and verification check.
(Source: Procedure.md: Verification; Procedure.md: Steps.)

## Documentation

**Calculation Package Deliverables:**
- Foundation calculations (tank foundations, equipment pads, building foundations if applicable, thrust blocks)
- Containment wall calculations (structural design, serviceability, seismic)
- Seismic analysis (design basis, methodology, element-specific analysis)
(Source: test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:234; Datasheet.md: Construction.)

**Supporting Documentation:**
- Calculation cover sheet and index
- Design basis statement and references
- Input data register (loads, geotechnical properties, material properties, code parameters)
- Assumptions register (provisional parameters, TBD items)
- Load combination summary
- Calculation methodology description (hand calcs, spreadsheets, FEM models)
- Software description and validation (if applicable)
- Calculation results summary tables
- Design verification statement
- Recommendations for drawings and specifications
(Source: Datasheet.md: Construction; test/Volume_2_Part_1_Employers_Requirements.pdf, location TBD.)

**QA/QC Records:**
- Independent check records (checker name, date, comments, resolutions)
- Check sign-off and approval records
- Calculation files (spreadsheets, FEM models, hand calculations)
- Revision history per project document control (**TBD**)
(Source: test/Volume_2_Part_1_Employers_Requirements.pdf, location TBD; Procedure.md: Records.)

## Requirements Traceability Matrix

| Requirement ID | Requirement Summary | Datasheet § | Guidance § | Procedure Step | Verification Method |
|----------------|---------------------|-------------|------------|----------------|---------------------|
| FR-01 | Calculation Artifact Coverage | Construction (all) | E-01 Organization | Step 1 | Completeness verification |
| FR-02 | Design Basis and Assumptions | Conditions (TBD items), Construction: Supporting Docs | P-01 Traceability, P-03 Evidence-Based, C-05 Assumptions | Step 2 | Traceability review |
| FR-03 | Foundation Calculations | Construction: Foundation Calcs | P-04 Optimization, P-05 Consistency, C-01 Input Data | Step 4 | Independent check |
| FR-04 | Containment Wall Calculations | Construction: Containment Wall Calcs | P-02 Containment Sensitivity, C-02 Serviceability | Step 4 | Independent check |
| FR-05 | Seismic Analysis | Construction: Seismic Analysis | C-03 Seismic Importance | Step 4 | Independent check |
| FR-06 | Calculation Results and Verification | Construction: Supporting Docs | P-01 Traceability, E-02 Good Practice | Step 5 | Results review |
| PR-01 | Strength and Serviceability | Conditions | P-02 Containment, C-02 Serviceability | Step 4 | Performance verification |
| PR-02 | Seismic Performance | Attributes (Design Codes), Conditions | C-03 Seismic Importance | Step 4 | Performance verification |
| PR-03 | Alignment with Objectives | Conditions (OBJ-3, OBJ-7) | P-02 Containment Sensitivity | Steps 4, 5 | Supports objectives |
| IR-01 | Dependency Coordination | — | P-05 Consistency, C-01 Input Data | Steps 2, 4, 7 | Alignment verification |
| IR-02 | Assumption Identification | Conditions (TBD items) | C-05 Assumption Management | Step 2 | Assumptions register |
| QR-01 | Document Control | Attributes | — | Step 7 | Document control verification |
| QR-02 | Independent Check | — | P-01 Traceability | Step 6 | Quality verification |
| QR-03 | Traceability | Construction: Supporting Docs | P-01 Traceability, E-02 Good Practice | Steps 2, 4, 6 | Quality verification |

## Cross-Document Notes

- **Datasheet:** Holds calculation package metadata (§Attributes) and scope expectations. Specification requirements must align with §Construction artifacts (foundations, containment walls, seismic). (Source: Datasheet.md: Attributes; Datasheet.md: Construction; Datasheet.md: Cross-Document Traceability.)
- **Guidance:** Provides principles for calculation development: §P-01 traceability, §P-02 containment sensitivity, §P-03 evidence-based code, §P-04 design optimization, §P-05 consistency. The Requirements Traceability Matrix above maps requirements to supporting Guidance sections. (Source: Guidance.md: Principles; Guidance.md: Guidance-to-Specification Traceability.)
- **Procedure:** Defines calculation development, checking, and issue workflow (Steps 1-7). The Requirements Traceability Matrix above maps each requirement to its Procedure step. (Source: Procedure.md: Steps; Procedure.md: Verification; Procedure.md: Procedure Steps Traceability.)
- **Related Deliverables:** Calculations must maintain consistency with:
  - DEL-05.01 drawing dimensions and details — §IR-01 (element sizing, reinforcement)
  - DEL-05.02 material properties and specification values — §IR-01 (concrete strength, modulus)
  - DEL-02.04 geotechnical parameters — §IR-01 (bearing capacity, settlement, soil properties)
