# Specification: DEL-13.03 Storage Tank Design Calculations

## Scope

This specification defines the requirements for **Storage Tank Design Calculations** within **PKG-13 Storage Tanks**.

### Deliverable Description

Provides the engineering basis and sizing/verification calculations for storage tank per ER requirements.

**Source:** _CONTEXT.md, Decomposition document DEL-13.03

### Coverage

**This deliverable shall produce calculation packages for:**

1. **API 650 Tank Design Calculations (3)** — One set per tank covering shell thickness, bottom, roof, wind, seismic, nozzles
2. **Foundation Calculations** — Tank loading on foundation (bearing pressure, settlement, anchorage)
3. **Seismic Calculations** — Seismic analysis per API 650 Appendix E (may be integrated with tank design calcs)

**Source:** _CONTEXT.md (Anticipated Artifacts)

**Included in API 650 Tank Design Calculations:**
- Tank geometry optimization (diameter, height)
- Shell thickness calculation per API 650 Section 5.6
- Bottom plate design per API 650 Sections 5.4 and 5.5
- Roof design per API 650 Section 5.10
- Wind stability and stiffener requirements per API 650 Section 5.9
- Seismic stability per API 650 Appendix E
- Nozzle reinforcement per API 650 Section 5.7
- Load cases and load combinations
- Compliance verification with API 650

**Included in Foundation Calculations:**
- Foundation loading summary (dead, live, wind, seismic)
- Bearing pressure distribution
- Settlement estimate and compliance with API 650 Appendix B limits
- Anchor bolt design (if anchorage required for seismic)

**Source:** Datasheet.md Calculation Types; API 650 requirements

**Excluded:**
- Foundation structural design (slab reinforcement, ring wall design) — Covered by PKG-05 (Concrete Structures) — **ASSUMPTION**
- Piping stress analysis — Covered by PKG-14 (Process Piping) — **ASSUMPTION**
- Detailed agitator structural analysis — Vendor responsibility; interface loads provided to tank design — **ASSUMPTION**

---

## Requirements

### Functional Requirements

**FR-01: Design Verification**
- Calculations shall verify that the tank design complies with API 650 and applicable codes
- All design decisions (geometry, materials, configuration) shall be supported by calculations
- Calculations shall demonstrate adequate safety factors and compliance margins
- **Source:** Engineering best practice; OBJ-1 (Safe & Reliable Operation)

**FR-02: Geometry Optimization**
- Calculations shall optimize tank geometry (diameter, height) based on capacity, site constraints, and cost
- Typical optimization targets: minimize shell weight, minimize foundation size, meet site constraints
- **TBD** — Specific optimization criteria and constraints require project input
- **Source:** Typical tank design optimization practice

**FR-03: Load Case Coverage**
- Calculations shall address all applicable load cases per Datasheet.md: Operating (full/empty), Hydrostatic Test, Wind, Seismic, combinations
- Critical load cases shall be identified and governing conditions highlighted
- **Source:** API 650 load requirements; NBC 2020 load combinations

**FR-04: Interface Definition**
- Calculations shall clearly define interfaces with adjacent deliverables:
  - Tank geometry → DEL-13.01 (Design Drawings)
  - Material specifications → DEL-13.02 (Technical Specification)
  - Foundation loading → DEL-05.03 (Foundation Calculations)
- **Source:** Multi-deliverable coordination requirement

**FR-05: Traceability and Transparency**
- Calculations shall be clear, well-organized, and traceable
- Assumptions, input data sources, and references shall be clearly identified
- Calculation steps shall be logical and verifiable by independent checker
- **Source:** Engineering calculation best practice

### Content Requirements

**CR-01: Calculation Package Structure**

Each calculation package shall include the following sections (minimum):

| Section | Content | Source |
|---------|---------|--------|
| **Cover Sheet** | Title, calc number, project, date, revision, preparer, checker, approver signatures | Project calculation format |
| **1. Scope and Objective** | What is being calculated, deliverable context | Calculation best practice |
| **2. Design Basis** | Codes/standards, tank capacity, product, operating conditions, environmental loads | Datasheet.md Conditions; ER |
| **3. Input Data** | Tank geometry (trial or final), material properties, load parameters | Datasheet.md; DEL-13.02; ER |
| **4. Assumptions** | Design assumptions clearly stated and justified | Calculation best practice |
| **5. Methodology** | Calculation approach, methods, software tools used | API 650; calculation best practice |
| **6. Calculations** | Detailed calculations with formulas, intermediate steps, results | Calculation content |
| **7. Results Summary** | Tabulated results (shell thicknesses, stresses, ratios, loads) | Calculation best practice |
| **8. Compliance Check** | Verification of compliance with API 650 and codes | API 650; engineering practice |
| **9. Conclusions and Recommendations** | Conclusions, design recommendations, action items | Calculation best practice |
| **10. References** | Referenced documents, standards, deliverables | Calculation best practice |
| **Appendices** | Supporting data, software outputs, charts, tables | As needed |

**Source:** ASSUMPTION based on typical engineering calculation format

**CR-02: Shell Thickness Calculation Content**

Shell thickness calculations shall include:
- Hydrostatic pressure at each shell course
- Required thickness per API 650 Equation 5-2
- Corrosion allowance (if applicable) — **TBD**
- Minimum thickness per API 650 Table 5-1a
- Actual thickness selected (commercial plate thickness)
- Utilization ratio for each course

**Source:** API 650 Section 5.6

**CR-03: Seismic Calculation Content**

Seismic calculations per API 650 Appendix E shall include:
- Site seismic parameters (PGA, spectral acceleration) — **TBD** (NBC 2020 or site study)
- Tank response parameters (sloshing height, period, participation factors)
- Base shear calculation (impulsive and convective components)
- Overturning moment calculation
- Anchorage requirement determination (anchored vs. unanchored)
- If anchored: Anchor bolt design, anchor chair design, shell compression check
- If unanchored: Uplift check, base plate yielding check per Appendix E

**Source:** API 650 Appendix E methodology

**CR-04: Foundation Loading Content**

Foundation loading calculations shall provide:
- Dead load: Empty tank weight + shell, roof, appurtenances
- Live load: Product weight at design capacity, roof live load (snow, maintenance)
- Wind load: Overturning moment and base shear from wind
- Seismic load: Overturning moment and base shear from seismic
- Load combinations per NBC 2020
- Bearing pressure distribution (uniform, triangular, or uplift condition)
- Maximum bearing pressure vs. allowable (from DEL-02.04)
- Settlement estimate and comparison to API 650 Appendix B limits

**Source:** API 650 foundation requirements; typical structural load transfer

### Performance Requirements

**PR-01: Code Compliance**
- Calculations shall demonstrate compliance with API 650 as the primary design code
- Edition and addenda of API 650 shall be stated — **TBD** (match DEL-13.02 specification)
- All API 650 requirements applicable to the tank configuration shall be addressed
- **Source:** Decomposition PKG-13 Scope; Specification DEL-13.02

**PR-02: Seismic Compliance**
- Seismic design shall comply with API 650 Appendix E and NBC 2020
- Site-specific seismic parameters shall be used — **TBD** (ER or site study)
- Seismic analysis shall consider impulsive and convective (sloshing) components
- **Source:** ASSUMPTION based on BC seismic zone; API 650 Appendix E

**PR-03: Material Consistency**
- Material properties used in calculations shall match those specified in DEL-13.02 (Technical Specification)
- Allowable stresses shall be per API 650 Table 5-2
- **Source:** Calculation-specification consistency requirement

**PR-04: Accuracy and Precision**
- Calculations shall use appropriate significant figures and units
- Software calculations shall be verified by hand calculations or independent methods for critical elements
- **TBD** — Software validation requirements per project quality procedures
- **Source:** Engineering calculation best practice

**PR-05: Safety Factors**
- Calculations shall demonstrate adequate safety factors per API 650 and applicable codes
- Critical elements (shell compression, overturning, bearing pressure) shall show utilization ratios < 1.0
- **Source:** API 650 safety philosophy; engineering practice

### Verification Requirements

**VR-01: Independent Checking**
- All calculations shall be independently checked by a qualified engineer (not the originator)
- Checker shall verify: methodology, input data, calculation logic, results, conclusions
- Checker comments shall be resolved before approval
- **Source:** Engineering quality control best practice

**VR-02: Software Verification**
- If software tools are used, software shall be validated for the application
- Critical software outputs shall be verified by hand calculations or alternative methods
- Software version and validation status shall be documented
- **TBD** — Software validation procedures per project QA plan
- **Source:** Engineering software quality assurance

**VR-03: Cross-Deliverable Consistency**
- Calculations shall be checked for consistency with:
  - DEL-13.01 (Design Drawings) — Geometry, configuration
  - DEL-13.02 (Technical Specification) — Materials, standards
  - DEL-02.04 (Geotechnical Reports) — Bearing capacity, settlement
- Discrepancies shall be resolved and documented
- **Source:** Multi-deliverable coordination requirement

**VR-04: Design Review**
- Significant design decisions and critical calculations shall be reviewed in design review meetings
- Design review shall include discipline leads and affected disciplines
- **TBD** — Design review scope and frequency per project procedures
- **Source:** ASSUMPTION based on typical design review process

---

## Standards

### Primary Standards

| Standard | Title | Application |
|----------|-------|-------------|
| **API 650** | Welded Tanks for Oil Storage | Primary tank design standard (shell, bottom, roof, nozzles) |
| **API 650 Appendix E** | Seismic Design of Storage Tanks | Seismic analysis and anchorage design |
| **API 650 Appendix B** | Settlement | Foundation settlement limits |
| **NBC 2020** | National Building Code of Canada | Environmental loads (wind, snow, seismic parameters) |

### Supporting Standards

| Standard | Title | Application |
|----------|-------|-------------|
| **CSA G40.21** | Structural Quality Steel | Material properties for structural steel elements |
| **AISC Steel Construction Manual** | Steel design reference (if applicable for structural elements) | ASSUMPTION — if needed for anchor chairs, stiffeners |

**Source:** Datasheet.md Primary Standards; ASSUMPTION for supporting standards

---

## Verification

### Calculation Checking Process

**V-01: Self-Check**
- Originator reviews calculation for completeness, accuracy, and clarity
- Verify all input data sources are referenced
- Verify all assumptions are stated
- Verify all calculation steps are logical and traceable

**V-02: Independent Check**
- Independent checker (qualified engineer, not originator) performs detailed review:
  - Verify methodology is appropriate and complies with standards
  - Verify input data is correct and properly sourced
  - Spot-check critical calculations (minimum 20% of calculations, all critical elements)
  - Verify results are reasonable and conclusions are supported
- Checker provides comments
- Originator resolves comments by revision or justification
- Checker signs off when satisfied

**V-03: Design Review**
- Critical calculations and design decisions reviewed in design review meetings
- Participants: Mechanical Lead, Civil/Structural Lead, Project Manager, QA/QC
- Review key results: tank geometry, shell thicknesses, seismic anchorage decision, foundation loads
- Document design review minutes and action items

**Source:** ASSUMPTION based on typical engineering calculation verification process

### Acceptance Criteria

**AC-01: Completeness**
- All required calculation packages produced per Datasheet.md scope
- All sections per CR-01 are complete
- All load cases per Datasheet.md are addressed
- No critical TBDs or assumptions left unresolved at final issue

**AC-02: Code Compliance**
- Calculations demonstrate compliance with API 650 and NBC 2020
- All utilization ratios and safety factors are acceptable (< 1.0 for critical elements)
- Compliance statements clearly documented

**AC-03: Accuracy**
- Input data is correct and properly referenced
- Calculation methodology is sound and follows standards
- Results are accurate and reasonable
- Independent checker has verified and signed off

**AC-04: Consistency**
- Calculations consistent with DEL-13.01 (drawings), DEL-13.02 (specification), DEL-02.04 (geotechnical)
- No internal contradictions within calculation package
- Material properties and allowable stresses consistent with specifications

**AC-05: Approval**
- Self-check completed
- Independent check completed and signed off
- Design review completed (if applicable)
- Discipline Lead (P.Eng.) approval obtained

---

## Documentation

### Required Calculation Outputs

| Calculation Package | Quantity | Description |
|---------------------|----------|-------------|
| **API 650 Tank Design Calculations** | 3 | One per tank: shell, bottom, roof, wind, seismic, nozzles |
| **Foundation Calculations** | **TBD** (1 or 3) | Tank loading, bearing pressure, settlement, anchorage |
| **Seismic Calculations** | **TBD** (integrated or separate) | Seismic analysis per API 650 Appendix E |

**Source:** _CONTEXT.md (Anticipated Artifacts)

### Calculation Management

**DM-01: Document Control**
- Calculations managed per project document control procedures
- Electronic master copies maintained in project document management system
- **TBD** — Document management system and procedures

**DM-02: Issuance**
- Calculations issued for review: Filed in `2_Checking/To/` with transmittal
- Calculations issued for design/construction: Filed in `3_Issued/` with issue record
- **TBD** — Issuance workflow and approval matrix

**DM-03: Revision Management**
- Revisions tracked with revision table and clouding/highlighting of changes
- Revision history maintained in calculation document
- Superseded revisions archived per project retention policy
- **TBD** — Revision conventions per project procedures

---

---

## Cross-Document References

**See Datasheet.md:** Calculation types, inputs/outputs, load cases → Referenced in FR-03, CR series
**See Guidance.md:** API 650 methodology (CP series), seismic principles, trade-offs → Support requirements
**See Procedure.md:** Steps 3-9 perform calculations per requirements here; Steps 10-12 verify compliance

---

**Document Status:** Pass 3 (Final) — Enrichment complete. Calculation requirements defined. Cross-document consistency verified. Ready for WORKING_ITEMS refinement.

**Last Updated:** 2026-01-28
