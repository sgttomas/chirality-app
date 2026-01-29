# Guidance: DEL-27.01 Design Basis Documents

## Purpose

This guidance document supports the development of **Design Basis Documents** for **PKG-27 Engineering Design**.

**Context:** Documents analysis and results for design basis documents required for design verification and approvals (per _CONTEXT.md).

**Role in Project:** The Design Basis Documents establish the technical foundation for all engineering design work on the Canola Oil Transload Facility Phase 1. These documents translate project objectives and Employer's Requirements into actionable design criteria that guide all downstream discipline engineering.

**Deliverable Classification:**
- Type: Report (see Datasheet § Identification)
- Discipline: Design
- Responsible: D&B Contractor
- Submission stages: 30%, 60%, 90%, IFC (per DEL-27.04; see Specification § QR-3)

**Cross-Document Links:**
- Datasheet.md: Identification, Attributes, Conditions, References
- Specification.md: Requirements (FR, PR, IR, QR, RC), Verification, Documentation
- Procedure.md: Steps 1-6 for producing Design Basis Documents

**Source:** _CONTEXT.md; Decomposition DEL-27.01; Datasheet.md

## Principles

### Design & Build Context

**Principle 1: Foundation for Integrated Design**
- In Design & Build contracts, the Design Basis Documents serve as the contractual and technical bridge between Employer's Requirements and detailed engineering
- These documents must be sufficiently detailed to guide design while maintaining flexibility for contractor optimization
- **ASSUMPTION**: Design basis establishes "what" and "why"; detailed design determines "how"
- **Specification §:** FR-1 (Design Basis Establishment), Scope (Included/Excluded)
- **Procedure Step:** Step 1.1 (Review Project Requirements), Step 3.1 (Content development guidance)
- **Source:** **ASSUMPTION**: Standard Design & Build practice

**Principle 2: Objective-Driven Design**
- All design criteria must be traceable to Project Objectives (OBJ-1 through OBJ-10)
- Design decisions should be evaluated against objective achievement, particularly:
  - OBJ-1 (Safe & Reliable Operation) — paramount importance for industrial facility (see Principle 8)
  - OBJ-2 (Throughput Capacity) — fundamental performance requirement (see Specification § PR-1)
  - OBJ-6 (Regulatory Compliance) — non-negotiable legal requirement (see Specification § RC-1)
  - OBJ-8 (Future Expandability) — long-term value consideration (see Principle 7)
- **Specification §:** FR-2 (Objective Alignment)
- **Procedure Step:** Step 3.1 (Address all Project Objectives)
- **Source:** Decomposition Section 2 (Project Objectives), Section 6 (Objective Mapping)

**Principle 3: Multi-Discipline Integration**
- Design basis must address all disciplines coherently: civil, structural, mechanical, electrical, controls, safety
- Interface requirements between disciplines must be clearly defined to prevent gaps and conflicts
- Early coordination between discipline leads is essential during design basis development
- **Specification §:** FR-1, IR-1 (Multi-Discipline Coordination)
- **Procedure Step:** Step 2.2 (Multi-Discipline Coordination Workshops)
- **Source:** **ASSUMPTION**: Multi-discipline coordination essential for integrated facility design

**Principle 4: Code and Standard Basis**
- Canadian codes and standards form the regulatory baseline for design in BC
- National Building Code of Canada (NBC/NBCC) establishes minimum requirements for structural, seismic, wind, snow loads
- CSA standards provide discipline-specific technical requirements
- Where codes/standards are silent or offer options, design basis must document selections and rationale
- **Datasheet §:** References (Applicable Standards)
- **Specification §:** RC-3 (Code and Standard Application), Standards section
- **Procedure Step:** Step 2.2 (Code and standard selection workshop topic)
- **Source:** Datasheet.md; **ASSUMPTION**: Canadian codes apply for Fraser Surrey Terminal location

### Design Criteria Philosophy

**Principle 5: Performance-Based Criteria**
- Design criteria should specify performance requirements (what the system must achieve) rather than prescriptive solutions (how to achieve it)
- This approach allows engineering teams to optimize solutions while ensuring requirements are met
- Example: Specify tank storage capacity (45,000 MT) and product quality maintenance requirements rather than prescribing tank design details
- **Specification §:** FR-3 (Design Criteria Definition), PR-1 through PR-4
- **Procedure Step:** Step 3.2 (Quantitative criteria development)
- **Trade-off Link:** See Trade-offs §5 (Prescriptive vs. Performance Criteria)
- **Source:** **ASSUMPTION**: Performance-based approach aligns with Design & Build philosophy

**Principle 6: Worst-Case Design Envelope**
- Design criteria should establish worst-case conditions that envelope all anticipated operating scenarios
- Include normal, upset, emergency, and maintenance conditions
- Consider simultaneous worst-case combinations (e.g., high throughput + high ambient temperature + maintenance outage)
- **Specification §:** FR-3, PR-1 through PR-4
- **Procedure Step:** Step 2.2 (Operating conditions workshop topic), Step 2.3 (Design Criteria Calculations)
- **Source:** **ASSUMPTION**: Conservative engineering practice for industrial facility design

**Principle 7: Phase 2 Future-Proofing**
- Design basis must consider Phase 2 expansion interfaces per OBJ-8
- Phase 1 design should not preclude Phase 2 expansion or require major rework
- Key considerations: additional tank connections, piping expansion points, electrical capacity, control system scalability
- Balance Phase 2 provisions against Phase 1 cost and complexity (avoid over-designing)
- **Specification §:** FR-4 (Phase 2 Expansion Provisions), IR-4 (Phase 2 Expansion Interfaces)
- **Procedure Step:** Step 2.2 (Phase 2 expansion provisions workshop topic)
- **Trade-off Link:** See Trade-offs §2 (Phase 2 Provisions)
- **Cross-Reference:** DEL-27.03 (Phase 2 Expansion Documentation)
- **Source:** Decomposition Section 2 (OBJ-8); **ASSUMPTION**: Coordination with DEL-27.03

### Safety and Risk Management

**Principle 8: Inherent Safety by Design**
- Apply inherent safety principles: eliminate, minimize, substitute, moderate, simplify
- HAZOP study results (DEL-27.02) inform safety-critical design criteria
- Design should minimize reliance on administrative controls; prefer engineered safeguards
- **Specification §:** PR-4 (Safety and Reliability)
- **Procedure Step:** Step 2.2 (Safety requirements workshop topic)
- **Cross-Reference:** DEL-27.02 (HAZOP Study Reports)
- **Source:** Decomposition Section 2 (OBJ-1); **ASSUMPTION**: Coordination with DEL-27.02

**Principle 9: Environmental Protection**
- Design basis must ensure adequate containment, spill prevention, and environmental controls per OBJ-7
- Consider spill scenarios: tank overfill, piping failures, loading arm disconnection, etc.
- Secondary containment sizing per worst-case spill volume
- **TBD** — Specific environmental protection requirements from Employer's Requirements and permits
- **Specification §:** RC-2 (Environmental Compliance)
- **Procedure Step:** Step 2.2 (Environmental conditions workshop topic)
- **Trade-off Link:** See Trade-offs §6 (Environmental Protection Level)
- **Source:** Decomposition Section 2 (OBJ-7)

## Considerations

### Project-Specific Factors

**Location-Specific Considerations:**

| Factor | Consideration | Specification § | Procedure Step |
|--------|---------------|-----------------|----------------|
| Marine/waterfront environment | Corrosion protection requirements for steel structures and equipment | RC-2 | Step 2.2 |
| Seismic zone | BC is moderate-to-high seismic risk; NBC/NBCC seismic provisions apply | RC-3 | Step 2.2, 2.3 |
| Fraser River proximity | Flood risk considerations, geotechnical conditions | RC-2 | Step 2.1 |
| Existing terminal operations | Design must minimize disruption per OBJ-5; consider construction phasing and logistics | IR-3 | Step 2.1 |

- **TBD** — Specific site conditions from geotechnical and environmental assessments
- **Source:** Decomposition Section 1.1, Section 2 (OBJ-5); **ASSUMPTION**: Fraser River waterfront location characteristics

**Product-Specific Considerations:**

| Factor | Consideration | Specification § | Procedure Step |
|--------|---------------|-----------------|----------------|
| CSD canola oil properties | Viscosity, temperature sensitivity, handling requirements | PR-1, PR-2 | Step 2.2 |
| Food-grade product | Contamination prevention, material compatibility, cleaning requirements | PR-4 | Step 2.2 |

- **TBD** — Specific product properties and handling requirements from Employer's Requirements
- **Datasheet §:** Conditions (Product)
- **Source:** Decomposition Section 1.1; **ASSUMPTION**: Food-grade handling standards apply

**Operational Considerations:**

| Factor | Value | Consideration | Specification § |
|--------|-------|---------------|-----------------|
| Throughput requirement | 1,000,000 MT/annum | Drives equipment sizing, redundancy, availability | PR-1 |
| Dual operating modes | Tank storage vs. direct rail-to-ship | Design for mode transitions | PR-3 |
| Railcar unloading capacity | 32 stations | Determines unloading system sizing and rail track configuration | PR-1 |
| Operating regime | Continuous | Consider 24/7 operation, seasonal variations, maintenance windows | PR-4 |

- **TBD** — Specific operational requirements and operating philosophy from Employer's Requirements
- **Datasheet §:** Conditions (Permitted Throughput, Railcar Capacity)
- **Procedure Step:** Step 2.2 (Performance requirements workshop topic)
- **Source:** Decomposition Section 1.1, Section 2 (OBJ-2, OBJ-4)

### Multi-Discipline Coordination

| Discipline | Considerations | Package Cross-References | Specification § |
|------------|----------------|--------------------------|-----------------|
| Civil and Site | Site grading, drainage, pavement design for heavy rail and truck loads; underground utilities routing; coordination with existing terminal infrastructure | PKG-01 through PKG-04 | IR-1, IR-3 |
| Structural | Tank foundation design for soil conditions and seismic loads; structural steel for pipe racks, loading platforms, equipment supports; building structures | PKG-05, PKG-06, PKG-08 | IR-1 |
| Mechanical and Process | Piping design pressures, temperatures, materials; pump sizing and redundancy; metering accuracy requirements per OBJ-10; tank heating/cooling | PKG-10 through PKG-16 | IR-1, PR-1, PR-2 |
| Electrical and Controls | Power distribution for motors, heating systems, lighting; control system architecture; safety instrumented systems (SIS) from HAZOP | PKG-17 through PKG-23 | IR-1, PR-4 |

- **ASSUMPTION**: Interface coordination per `_DEPENDENCIES.md` (NOT_TRACKED)
- **Procedure Step:** Step 2.2 (Interface requirements matrix)
- **Source:** Decomposition Section 4 (Package Summary)

### Regulatory and Compliance Factors

**Authority Having Jurisdiction:**
- **TBD** — Identify all authorities with approval jurisdiction: municipal, provincial, federal, port authority (VFPA), etc.
- Coordinate approval requirements and timelines
- **Specification §:** RC-1 (Regulatory Compliance)
- **Procedure Step:** Step 1.1 (Identify applicable regulations)
- **Source:** **ASSUMPTION**: Multiple authorities typical for marine terminal project in BC

**Permit Requirements:**
- Employer obtains permits; Contractor responsible for design compliance with permit conditions
- Design basis must address all permit conditions and constraints
- **TBD** — Specific permit requirements to be provided by Employer
- **Specification §:** IR-2 (Employer Interfaces)
- **Procedure Step:** Step 1.1, Step 2.1 (Permit conditions)
- **Source:** Decomposition Section 1.2 (Scope Focus — Employer-responsible permits)

**Independent Design Verification:**
- IDV requirements per DEL-28.01 may influence design basis documentation level of detail
- Consider IDV scope and criteria during design basis development to ensure adequate documentation
- **Specification §:** QR-2 (Design Verification)
- **Procedure Step:** Verification § V-4
- **Cross-Reference:** DEL-28.01
- **Source:** **ASSUMPTION**: Coordination with DEL-28.01

### Design Submission Considerations

**Staged Submission Approach:**

| Stage | Content Level | Specification § | Procedure Step |
|-------|---------------|-----------------|----------------|
| 30% | Overall approach, key decisions, criteria framework | QR-3 | Step 5.2 |
| 60% | Refined criteria based on detailed engineering feedback | QR-3 | Step 5.2 |
| 90% | Near-final criteria, all major decisions resolved | QR-3 | Step 5.2 |
| IFC | Final frozen design basis for construction | QR-3 | Step 5.4 |

- **TBD** — Specific submission content requirements per stage
- **Datasheet §:** Attributes (Submission Stages)
- **Cross-Reference:** DEL-27.04 (Design Submission Packages)
- **Source:** Datasheet.md; **ASSUMPTION**: Standard Design & Build staged submission approach

**Comment Resolution:**
- Employer and authority comments must be tracked and resolved
- Significant changes to design basis may require revision to downstream design work
- Maintain traceability of comment responses and design changes
- **TBD** — Comment tracking and resolution procedures
- **Procedure Step:** Step 5.3 (Employer Review and Comment Resolution)
- **Source:** **ASSUMPTION**: Standard design submission and review process

## Trade-offs

### Design Conservatism vs. Cost Optimization

**Trade-off 1: Safety Factors and Redundancy**

| Approach | Advantages | Disadvantages | Specification § |
|----------|------------|---------------|-----------------|
| Conservative | Greater reliability, easier to meet OBJ-1 (Safe & Reliable Operation) | Higher capital cost, larger footprint, higher operating energy | PR-4 |
| Optimized | Lower capital cost, compact footprint, efficient operations | Less margin for upsets, potential availability impacts | PR-1 |

- **Recommendation:** Balance based on lifecycle cost analysis (OBJ-9) and throughput assurance needs (OBJ-2)
- **Principle Link:** Principles §6 (Worst-Case Design Envelope)
- **Procedure Step:** Step 2.2 (Design philosophy workshop topic)
- **Source:** Decomposition Section 2 (OBJ-1, OBJ-2, OBJ-9); **ASSUMPTION**: Lifecycle cost optimization guidance

**Trade-off 2: Phase 2 Provisions**

| Approach | Advantages | Disadvantages | Specification § |
|----------|------------|---------------|-----------------|
| Phase 2-ready | Minimal Phase 2 rework, lower overall lifecycle cost, operational continuity | Higher Phase 1 capital cost, potential over-design if Phase 2 deferred | FR-4, IR-4 |
| Phase 1-focused | Lower Phase 1 capital cost, flexibility for Phase 2 design changes | Higher Phase 2 rework cost, operational disruption during expansion | FR-4, IR-4 |

- **Recommendation:** Identify critical Phase 2 interfaces and provide upsizing for difficult-to-change items (underground utilities, foundations); defer non-critical provisions
- **Principle Link:** Principles §7 (Phase 2 Future-Proofing)
- **Procedure Step:** Step 2.2 (Phase 2 expansion provisions workshop topic)
- **Cross-Reference:** DEL-27.03 (Phase 2 Expansion Documentation)
- **Source:** Decomposition Section 2 (OBJ-8, OBJ-9); **ASSUMPTION**: Balance Phase 2 provisions per DEL-27.03 coordination

### Code Selection and Application

**Trade-off 3: Code Edition Selection**

| Approach | Advantages | Disadvantages | Specification § |
|----------|------------|---------------|-----------------|
| Latest codes | Most current technical requirements, easier future compliance | Potential for unfamiliar requirements, possible increased conservatism | RC-3 |
| Established codes | Familiar to design team, proven interpretation, predictable approval | Potential for obsolete technical requirements, future upgrade costs | RC-3 |

- **Recommendation:** Use codes required by authorities having jurisdiction; where discretion exists, prefer latest editions unless specific project constraints apply
- **Principle Link:** Principles §4 (Code and Standard Basis)
- **Procedure Step:** Step 2.2 (Code selection workshop topic)
- **Source:** **ASSUMPTION**: Code selection considerations

**Trade-off 4: Code-Minimum vs. Enhanced Performance**

| Approach | Advantages | Disadvantages | Specification § |
|----------|------------|---------------|-----------------|
| Code-minimum | Lower cost, faster design, clear compliance baseline | Minimal performance margin, potential future upgrade needs | RC-3 |
| Enhanced | Better long-term performance, easier to accommodate changes, improved reliability | Higher cost, potentially over-designed for actual needs | RC-3 |

- **Recommendation:** Code-minimum for non-critical items; enhanced performance for throughput-critical and safety-critical systems (align with OBJ-1, OBJ-2)
- **Principle Link:** Principles §2 (Objective-Driven Design)
- **Procedure Step:** Step 3.2 (Criteria development with rationale)
- **Source:** Decomposition Section 2 (OBJ-1, OBJ-2); **ASSUMPTION**: Risk-based approach to design conservatism

### Design Flexibility vs. Standardization

**Trade-off 5: Prescriptive vs. Performance Criteria**

| Approach | Advantages | Disadvantages | Specification § |
|----------|------------|---------------|-----------------|
| Prescriptive | Clear requirements, predictable outcomes, easier verification | Limits contractor optimization, may not leverage best value solutions | FR-3 |
| Performance | Enables contractor innovation, potentially lower cost, optimized solutions | More interpretation needed, requires robust verification, potential disputes | FR-3 |

- **Recommendation:** Performance-based criteria aligned with Design & Build philosophy; prescriptive requirements only where specific solution is mandated by Employer or authorities
- **Principle Link:** Principles §1, §5 (Foundation for Integrated Design, Performance-Based Criteria)
- **Procedure Step:** Step 3.2 (Content development guidance)
- **Source:** **ASSUMPTION**: Design & Build contract performance-based approach

### Environmental and Sustainability Considerations

**Trade-off 6: Environmental Protection Level**

| Approach | Advantages | Disadvantages | Specification § |
|----------|------------|---------------|-----------------|
| Enhanced protection | Reduced environmental risk, better community relations, future-proof for stricter regulations | Higher capital and operating costs | RC-2 |
| Regulatory minimum | Lower cost, simpler compliance demonstration | Less margin for upsets, potential future upgrade costs if regulations tighten | RC-2 |

- **Recommendation:** Enhanced protection for high-risk areas (product containment); regulatory minimum where risk is lower (align with OBJ-7)
- **Principle Link:** Principles §9 (Environmental Protection)
- **Procedure Step:** Step 2.2 (Environmental conditions workshop topic)
- **Source:** Decomposition Section 2 (OBJ-7); **ASSUMPTION**: Risk-based environmental protection approach

## Examples

### Design Basis Document Precedents

**Example 1: Tank Storage Design Criteria**

Typical design criteria structure for storage tank system (see Specification § PR-2):

| Category | Parameter | Value | Source |
|----------|-----------|-------|--------|
| Performance | Total storage capacity | 45,000 MT (3 × 15,000 MT) | Decomposition Section 1.1 (OBJ-3) |
| Performance | Product | CSD canola oil | Decomposition Section 1.1 |
| Performance | Operating temperature range | **TBD** °C | Employer's Requirements |
| Performance | Turnover rate | **TBD** per throughput requirement | Specification § PR-1 |
| Design loads | Internal pressure | Atmospheric + vapor pressure | **ASSUMPTION** |
| Design loads | Wind loads | Per NBC/NBCC for Surrey, BC | Specification § RC-3 |
| Design loads | Seismic loads | Per NBC/NBCC for BC location | Specification § RC-3 |
| Design loads | Snow loads | Per NBC/NBCC for Surrey, BC | Specification § RC-3 |
| Materials | Tank shell | Carbon steel, food-grade coating | **ASSUMPTION** |
| Materials | Foundation | Reinforced concrete per CSA A23.3 | Specification § Standards |
| Codes | Tank design | API 650 or equivalent | Specification § Standards |
| Codes | Foundation design | CSA A23.3 | Specification § Standards |

- **Procedure Step:** Step 3.2 (Design Criteria preparation)
- **Source:** **ASSUMPTION**: Typical tank design criteria structure; **TBD** — Specific values from detailed design

**Example 2: Piping Design Criteria**

Typical design criteria structure for process piping (see Specification § PR-1, PR-3):

| Category | Parameter | Value | Source |
|----------|-----------|-------|--------|
| Performance | Flow rates | **TBD** m³/hr for unloading, transfer, loading operations | Employer's Requirements |
| Performance | Design pressure | **TBD** kPa | Detailed design |
| Performance | Operating temperature | **TBD** °C | Employer's Requirements |
| Design conditions | Fluid | CSD canola oil | Decomposition Section 1.1 |
| Design conditions | Material compatibility | Food-grade, corrosion-resistant | **ASSUMPTION** |
| Design conditions | Load combinations | Worst-case pressure/temperature combinations | Principles §6 |
| Codes | Piping design | CSA B51 or CSA B31.3 equivalent | Specification § Standards |
| Codes | Underground piping | CSA B137 or equivalent | **ASSUMPTION** |
| Safety | Hazardous area classification | **TBD** — per DEL-27.02 HAZOP results | Specification § PR-4 |

- **Procedure Step:** Step 3.2 (Design Criteria preparation)
- **Cross-Reference:** DEL-27.02 (HAZOP Study Reports)
- **Source:** **ASSUMPTION**: Typical piping design criteria structure; **TBD** — Specific values from detailed design

**Example 3: Seismic Design Basis**

Typical seismic design approach for BC location (see Specification § RC-3):

| Category | Parameter | Value | Source |
|----------|-----------|-------|--------|
| Site parameters | Spectral acceleration values | **TBD** | NBC/NBCC for Surrey, BC |
| Site parameters | Site class | **TBD** — from geotechnical investigation | Site investigation |
| Site parameters | Importance category | **TBD** — based on facility classification | Specification § FR-1 |
| Design approach | Structural systems | Per NBC/NBCC seismic provisions | Specification § RC-3 |
| Design approach | Tank anchorage | Per API 650 Appendix E or equivalent | Specification § Standards |
| Design approach | Piping flexibility | Per CSA B51/B31.3 seismic requirements | Specification § Standards |
| Design approach | Non-structural anchorage | Per NBC/NBCC | Specification § RC-3 |
| Performance objectives | Life safety | No collapse under design seismic event | **ASSUMPTION** |
| Performance objectives | Property protection | **TBD** — based on risk tolerance and OBJ-1 | Specification § PR-4 |
| Performance objectives | Operational continuity | **TBD** — based on throughput assurance (OBJ-2) | Specification § PR-1 |

- **Procedure Step:** Step 2.3 (Design Criteria Calculations)
- **Source:** **ASSUMPTION**: Typical BC seismic design approach; **TBD** — Site-specific seismic parameters; Decomposition Section 2 (OBJ-1, OBJ-2)

### Key Decision Documentation

**Example 4: Design Philosophy Statement**

Typical design philosophy content for Design Basis Memorandum (see Specification § Documentation):

"The design philosophy for the Canola Oil Transload Facility Phase 1 prioritizes safe and reliable operation (OBJ-1) while achieving the required throughput capacity of 1,000,000 MT per annum (OBJ-2). The design approach emphasizes:

1. **Inherent safety:** Minimize hazards through design rather than relying solely on procedural controls. HAZOP study results (DEL-27.02) inform safety-critical design features. (See Principles §8)

2. **Operational flexibility:** The facility shall support both tank storage operations and direct rail-to-ship transfer (OBJ-4), with seamless mode transitions and minimal operational complexity. (See Specification § PR-3)

3. **Regulatory compliance:** All design shall comply with applicable Canadian codes, BC provincial requirements, municipal regulations, and port authority (VFPA) requirements (OBJ-6). Independent design verification (DEL-28.01) provides additional assurance. (See Specification § RC-1, QR-2)

4. **Future expandability:** Phase 1 design shall accommodate Phase 2 expansion with minimal disruption (OBJ-8). Critical interfaces and upsizing provisions are identified in coordination with Phase 2 Expansion Documentation (DEL-27.03). (See Principles §7; Specification § FR-4, IR-4)

5. **Lifecycle cost optimization:** Design decisions consider both capital cost and long-term operating/maintenance costs (OBJ-9), with preference for reliable, maintainable equipment over lowest first cost. (See Trade-offs §1)

6. **Environmental stewardship:** Design includes robust containment, spill prevention, and environmental controls exceeding regulatory minimums for high-risk areas (OBJ-7). (See Principles §9; Trade-offs §6)"

- **Procedure Step:** Step 3.1 (Design Basis Memorandum preparation)
- **Source:** **ASSUMPTION**: Typical design philosophy structure aligned with Project Objectives (Decomposition Section 2)

### Lessons Learned Considerations

**Consideration 1: Early Stakeholder Alignment**
- Engage Employer, authorities, and independent verifiers early in design basis development
- Early alignment on key criteria reduces downstream rework and comment cycles
- **TBD** — Specific stakeholder engagement plan
- **Specification §:** Verification (VM-4, VM-3)
- **Procedure Step:** Step 5.2, Step 5.3
- **Source:** **ASSUMPTION**: Best practice for Design & Build projects

**Consideration 2: Living Document Approach**
- Design basis should evolve through submission stages (30%, 60%, 90%, IFC) as design matures
- Establish change control process for design basis revisions
- Maintain traceability of criteria changes and impact on downstream design
- **TBD** — Design basis change control procedure
- **Specification §:** QR-1, QR-3
- **Procedure Step:** Step 6.1 (Change Control)
- **Source:** **ASSUMPTION**: Staged submission approach per DEL-27.04

**Consideration 3: Interface Management**
- Dedicate specific attention to interfaces: discipline-to-discipline, Contractor-to-Employer, Phase 1-to-Phase 2
- Interface mismatches are common source of design errors and rework
- Use interface control documents or matrices to track and resolve interface requirements
- **TBD** — Interface management approach and tools
- **Specification §:** IR-1 through IR-4
- **Procedure Step:** Step 2.2 (Interface requirements matrix)
- **Source:** **ASSUMPTION**: Interface management best practice for complex projects

---

**Cross-Document Verification (Pass 3):**
- All Principles linked to Specification § and Procedure Step
- All Considerations linked to Specification § and Procedure Step
- All Trade-offs linked to relevant Principles and Specification §
- All Examples linked to Specification § and Procedure Step
- Terminology verified consistent with Datasheet.md, Specification.md, Procedure.md
- Project parameters verified consistent: 1,000,000 MT/annum (OBJ-2), 45,000 MT storage / 3 × 15,000 MT (OBJ-3), 32 railcar stations
- Cross-references to DEL-27.02, DEL-27.03, DEL-27.04, DEL-28.01 verified consistent across all documents

**Source for Examples section:** **ASSUMPTION**: Typical design basis content and structure for industrial facility Design & Build project; specific values **TBD** pending Employer's Requirements and detailed design development
