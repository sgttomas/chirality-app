# Guidance: DEL-27.01 Design Basis Documents

## Purpose

This guidance document supports the development of **Design Basis Documents** for **PKG-27 Engineering Design**.

**Context:** Documents analysis and results for design basis documents required for design verification and approvals (per _CONTEXT.md).

**Role in Project:** The Design Basis Documents establish the technical foundation for all engineering design work on the Canola Oil Transload Facility Phase 1. These documents translate project objectives and Employer's Requirements into actionable design criteria that guide all downstream discipline engineering.

**Deliverable Classification:**
- Type: Report
- Discipline: Design
- Responsible: D&B Contractor
- Submission stages: 30%, 60%, 90%, IFC (per DEL-27.04)

**Source:** _CONTEXT.md; Decomposition DEL-27.01; Datasheet.md

## Principles

### Design & Build Context

**Principle 1: Foundation for Integrated Design**
- In Design & Build contracts, the Design Basis Documents serve as the contractual and technical bridge between Employer's Requirements and detailed engineering
- These documents must be sufficiently detailed to guide design while maintaining flexibility for contractor optimization
- **ASSUMPTION**: Design basis establishes "what" and "why"; detailed design determines "how"
- **Source:** **ASSUMPTION**: Standard Design & Build practice

**Principle 2: Objective-Driven Design**
- All design criteria must be traceable to Project Objectives (OBJ-1 through OBJ-10)
- Design decisions should be evaluated against objective achievement, particularly:
  - OBJ-1 (Safe & Reliable Operation) — paramount importance for industrial facility
  - OBJ-2 (Throughput Capacity) — fundamental performance requirement
  - OBJ-6 (Regulatory Compliance) — non-negotiable legal requirement
  - OBJ-8 (Future Expandability) — long-term value consideration
- **Source:** Decomposition Section 2 (Project Objectives), Section 6 (Objective Mapping)

**Principle 3: Multi-Discipline Integration**
- Design basis must address all disciplines coherently: civil, structural, mechanical, electrical, controls, safety
- Interface requirements between disciplines must be clearly defined to prevent gaps and conflicts
- Early coordination between discipline leads is essential during design basis development
- **Source:** **ASSUMPTION**: Multi-discipline coordination essential for integrated facility design

**Principle 4: Code and Standard Basis**
- Canadian codes and standards form the regulatory baseline for design in BC
- National Building Code of Canada (NBC/NBCC) establishes minimum requirements for structural, seismic, wind, snow loads
- CSA standards provide discipline-specific technical requirements
- Where codes/standards are silent or offer options, design basis must document selections and rationale
- **Source:** Datasheet.md; **ASSUMPTION**: Canadian codes apply for Fraser Surrey Terminal location

### Design Criteria Philosophy

**Principle 5: Performance-Based Criteria**
- Design criteria should specify performance requirements (what the system must achieve) rather than prescriptive solutions (how to achieve it)
- This approach allows engineering teams to optimize solutions while ensuring requirements are met
- Example: Specify tank storage capacity and product quality maintenance requirements rather than prescribing tank design details
- **Source:** **ASSUMPTION**: Performance-based approach aligns with Design & Build philosophy

**Principle 6: Worst-Case Design Envelope**
- Design criteria should establish worst-case conditions that envelope all anticipated operating scenarios
- Include normal, upset, emergency, and maintenance conditions
- Consider simultaneous worst-case combinations (e.g., high throughput + high ambient temperature + maintenance outage)
- **Source:** **ASSUMPTION**: Conservative engineering practice for industrial facility design

**Principle 7: Phase 2 Future-Proofing**
- Design basis must consider Phase 2 expansion interfaces per OBJ-8
- Phase 1 design should not preclude Phase 2 expansion or require major rework
- Key considerations: additional tank connections, piping expansion points, electrical capacity, control system scalability
- Balance Phase 2 provisions against Phase 1 cost and complexity (avoid over-designing)
- **Source:** Decomposition Section 2 (OBJ-8); **ASSUMPTION**: Coordination with DEL-27.03

### Safety and Risk Management

**Principle 8: Inherent Safety by Design**
- Apply inherent safety principles: eliminate, minimize, substitute, moderate, simplify
- HAZOP study results (DEL-27.02) inform safety-critical design criteria
- Design should minimize reliance on administrative controls; prefer engineered safeguards
- **Source:** Decomposition Section 2 (OBJ-1); **ASSUMPTION**: Coordination with DEL-27.02

**Principle 9: Environmental Protection**
- Design basis must ensure adequate containment, spill prevention, and environmental controls per OBJ-7
- Consider spill scenarios: tank overfill, piping failures, loading arm disconnection, etc.
- Secondary containment sizing per worst-case spill volume
- **TBD** — Specific environmental protection requirements from Employer's Requirements and permits
- **Source:** Decomposition Section 2 (OBJ-7)

## Considerations

### Project-Specific Factors

**Location-Specific Considerations:**
- **Marine/waterfront environment:** Corrosion protection requirements for steel structures and equipment
- **Seismic zone:** BC is moderate-to-high seismic risk; NBC/NBCC seismic provisions apply
- **Fraser River proximity:** Flood risk considerations, geotechnical conditions
- **Existing terminal operations:** Design must minimize disruption per OBJ-5; consider construction phasing and logistics
- **TBD** — Specific site conditions from geotechnical and environmental assessments
- **Source:** Decomposition Section 1.1, Section 2 (OBJ-5); **ASSUMPTION**: Fraser River waterfront location characteristics

**Product-Specific Considerations:**
- **CSD canola oil properties:** Viscosity, temperature sensitivity, handling requirements
- **Food-grade product:** Contamination prevention, material compatibility, cleaning requirements
- **TBD** — Specific product properties and handling requirements from Employer's Requirements
- **Source:** Decomposition Section 1.1; **ASSUMPTION**: Food-grade handling standards apply

**Operational Considerations:**
- **Throughput requirement:** 1,000,000 MT/annum drives equipment sizing, redundancy, availability
- **Dual operating modes:** Tank storage vs. direct rail-to-ship; design for mode transitions
- **32 railcar unloading capacity:** Determines unloading system sizing and rail track configuration
- **Continuous operation:** Consider 24/7 operation, seasonal variations, maintenance windows
- **TBD** — Specific operational requirements and operating philosophy from Employer's Requirements
- **Source:** Decomposition Section 1.1, Section 2 (OBJ-2, OBJ-4)

### Multi-Discipline Coordination

**Civil and Site Considerations:**
- Site grading, drainage, pavement design for heavy rail and truck loads
- Underground utilities routing and conflicts
- Coordination with existing terminal infrastructure
- **ASSUMPTION**: Coordination with PKG-01 through PKG-04 deliverables

**Structural Considerations:**
- Tank foundation design for soil conditions and seismic loads
- Structural steel for pipe racks, loading platforms, equipment supports
- Building structures for control rooms, pump houses, etc.
- **ASSUMPTION**: Coordination with PKG-05, PKG-06, PKG-08 deliverables

**Mechanical and Process Considerations:**
- Piping design pressures, temperatures, materials
- Pump sizing and redundancy
- Metering accuracy requirements per OBJ-10
- Tank heating/cooling requirements for product quality
- **ASSUMPTION**: Coordination with PKG-10 through PKG-16 deliverables

**Electrical and Controls Considerations:**
- Power distribution for motors, heating systems, lighting
- Control system architecture for integrated operations
- Safety instrumented systems (SIS) requirements from HAZOP
- **ASSUMPTION**: Coordination with PKG-17 through PKG-23 deliverables

**Source:** Decomposition Section 4 (Package Summary); **ASSUMPTION**: Interface coordination per `_DEPENDENCIES.md` (NOT_TRACKED)

### Regulatory and Compliance Factors

**Authority Having Jurisdiction:**
- **TBD** — Identify all authorities with approval jurisdiction: municipal, provincial, federal, port authority (VFPA), etc.
- Coordinate approval requirements and timelines
- **Source:** **ASSUMPTION**: Multiple authorities typical for marine terminal project in BC

**Permit Requirements:**
- Employer obtains permits; Contractor responsible for design compliance with permit conditions
- Design basis must address all permit conditions and constraints
- **TBD** — Specific permit requirements to be provided by Employer
- **Source:** Decomposition Section 1.2 (Scope Focus — Employer-responsible permits)

**Independent Design Verification:**
- IDV requirements per DEL-28.01 may influence design basis documentation level of detail
- Consider IDV scope and criteria during design basis development to ensure adequate documentation
- **Source:** **ASSUMPTION**: Coordination with DEL-28.01

### Design Submission Considerations

**Staged Submission Approach:**
- Design basis evolves through 30%, 60%, 90%, IFC submission stages per DEL-27.04
- Early stages (30%) establish overall approach, key decisions, and criteria framework
- Later stages (60%, 90%) refine criteria based on detailed engineering feedback
- IFC represents final frozen design basis for construction
- **TBD** — Specific submission content requirements per stage
- **Source:** Datasheet.md; **ASSUMPTION**: Standard Design & Build staged submission approach

**Comment Resolution:**
- Employer and authority comments must be tracked and resolved
- Significant changes to design basis may require revision to downstream design work
- Maintain traceability of comment responses and design changes
- **TBD** — Comment tracking and resolution procedures
- **Source:** **ASSUMPTION**: Standard design submission and review process

## Trade-offs

### Design Conservatism vs. Cost Optimization

**Trade-off 1: Safety Factors and Redundancy**
- **Conservative approach:** Higher safety factors, more redundancy, increased equipment capacity margins
  - Advantages: Greater reliability, easier to meet OBJ-1 (Safe & Reliable Operation)
  - Disadvantages: Higher capital cost, larger footprint, higher operating energy
- **Optimized approach:** Design to code minimum, optimize redundancy, tighter capacity margins
  - Advantages: Lower capital cost, compact footprint, efficient operations
  - Disadvantages: Less margin for upsets, potential availability impacts
- **Recommendation:** Balance based on lifecycle cost analysis (OBJ-9) and throughput assurance needs (OBJ-2)
- **Source:** Decomposition Section 2 (OBJ-1, OBJ-2, OBJ-9); **ASSUMPTION**: Lifecycle cost optimization guidance

**Trade-off 2: Phase 2 Provisions**
- **Phase 2-ready approach:** Design Phase 1 with full Phase 2 capacity in infrastructure (piping sizes, electrical capacity, control system)
  - Advantages: Minimal Phase 2 rework, lower overall lifecycle cost, operational continuity
  - Disadvantages: Higher Phase 1 capital cost, potential over-design if Phase 2 deferred
- **Phase 1-focused approach:** Design for Phase 1 only; defer Phase 2 provisions
  - Advantages: Lower Phase 1 capital cost, flexibility for Phase 2 design changes
  - Disadvantages: Higher Phase 2 rework cost, operational disruption during expansion
- **Recommendation:** Identify critical Phase 2 interfaces and provide upsizing for difficult-to-change items (underground utilities, foundations); defer non-critical provisions
- **Source:** Decomposition Section 2 (OBJ-8, OBJ-9); **ASSUMPTION**: Balance Phase 2 provisions per DEL-27.03 coordination

### Code Selection and Application

**Trade-off 3: Code Edition Selection**
- **Latest codes:** Use most recent code editions
  - Advantages: Most current technical requirements, easier future compliance
  - Disadvantages: Potential for unfamiliar requirements, possible increased conservatism
- **Established codes:** Use well-established code editions with proven track record
  - Advantages: Familiar to design team, proven interpretation, predictable approval
  - Disadvantages: Potential for obsolete technical requirements, future upgrade costs
- **Recommendation:** Use codes required by authorities having jurisdiction; where discretion exists, prefer latest editions unless specific project constraints apply
- **Source:** **ASSUMPTION**: Code selection considerations

**Trade-off 4: Code-Minimum vs. Enhanced Performance**
- **Code-minimum design:** Design to minimum code requirements
  - Advantages: Lower cost, faster design, clear compliance baseline
  - Disadvantages: Minimal performance margin, potential future upgrade needs
- **Enhanced design:** Exceed code minimums for critical performance areas
  - Advantages: Better long-term performance, easier to accommodate changes, improved reliability
  - Disadvantages: Higher cost, potentially over-designed for actual needs
- **Recommendation:** Code-minimum for non-critical items; enhanced performance for throughput-critical and safety-critical systems (align with OBJ-1, OBJ-2)
- **Source:** Decomposition Section 2 (OBJ-1, OBJ-2); **ASSUMPTION**: Risk-based approach to design conservatism

### Design Flexibility vs. Standardization

**Trade-off 5: Prescriptive vs. Performance Criteria**
- **Prescriptive criteria:** Specify detailed design requirements, materials, configurations
  - Advantages: Clear requirements, predictable outcomes, easier verification
  - Disadvantages: Limits contractor optimization, may not leverage best value solutions
- **Performance criteria:** Specify performance requirements; allow design flexibility
  - Advantages: Enables contractor innovation, potentially lower cost, optimized solutions
  - Disadvantages: More interpretation needed, requires robust verification, potential disputes
- **Recommendation:** Performance-based criteria aligned with Design & Build philosophy; prescriptive requirements only where specific solution is mandated by Employer or authorities
- **Source:** **ASSUMPTION**: Design & Build contract performance-based approach

### Environmental and Sustainability Considerations

**Trade-off 6: Environmental Protection Level**
- **Enhanced protection:** Exceed regulatory minimums for containment, emissions control, environmental monitoring
  - Advantages: Reduced environmental risk, better community relations, future-proof for stricter regulations
  - Disadvantages: Higher capital and operating costs
- **Regulatory minimum:** Meet but not exceed environmental requirements
  - Advantages: Lower cost, simpler compliance demonstration
  - Disadvantages: Less margin for upsets, potential future upgrade costs if regulations tighten
- **Recommendation:** Enhanced protection for high-risk areas (product containment); regulatory minimum where risk is lower (align with OBJ-7)
- **Source:** Decomposition Section 2 (OBJ-7); **ASSUMPTION**: Risk-based environmental protection approach

## Examples

### Design Basis Document Precedents

**Example 1: Tank Storage Design Criteria**

Typical design criteria structure for storage tank system:
- **Performance requirements:**
  - Total storage capacity: 45,000 MT (3 × 15,000 MT)
  - Product: CSD canola oil
  - Operating temperature range: [TBD] °C
  - Turnover rate: [TBD] per [throughput requirement]
- **Design loads:**
  - Internal pressure: atmospheric + vapor pressure
  - External wind loads per NBC/NBCC
  - Seismic loads per NBC/NBCC for BC location
  - Snow loads per NBC/NBCC for Surrey, BC
- **Materials:**
  - Tank shell: Carbon steel, food-grade coating
  - Foundation: Reinforced concrete per CSA A23.3
- **Codes:**
  - API 650 or equivalent for tank design
  - CSA A23.3 for foundation design
  - NBC/NBCC for seismic and environmental loads

**Source:** **ASSUMPTION**: Typical tank design criteria structure; **TBD** — Specific values from detailed design

**Example 2: Piping Design Criteria**

Typical design criteria structure for process piping:
- **Performance requirements:**
  - Flow rates: [TBD] m³/hr for unloading, transfer, loading operations
  - Pressure: [TBD] kPa design pressure
  - Temperature: [TBD] °C operating temperature
- **Design conditions:**
  - Fluid: CSD canola oil
  - Material compatibility: food-grade, corrosion-resistant
  - Worst-case pressure/temperature combinations
- **Codes:**
  - CSA B51 or CSA B31.3 equivalent for piping design
  - CSA B137 or equivalent for underground piping
- **Hazardous area classification:** [TBD] — per DEL-27.02 HAZOP results

**Source:** **ASSUMPTION**: Typical piping design criteria structure; **TBD** — Specific values from detailed design; Coordination with DEL-27.02

**Example 3: Seismic Design Basis**

Typical seismic design approach for BC location:
- **Site seismic parameters:** Per NBC/NBCC for Surrey, BC
  - Spectral acceleration values: [TBD]
  - Site class: [TBD] — from geotechnical investigation
  - Importance category: [TBD] — based on facility classification
- **Design approach:**
  - Structural systems per NBC/NBCC seismic provisions
  - Tank anchorage per API 650 Appendix E or equivalent
  - Piping flexibility and support design per CSA B51/B31.3 seismic requirements
  - Non-structural component anchorage per NBC/NBCC
- **Performance objectives:**
  - Life safety: No collapse under design seismic event
  - Property protection: [TBD] — based on risk tolerance and OBJ-1
  - Operational continuity: [TBD] — based on throughput assurance needs (OBJ-2)

**Source:** **ASSUMPTION**: Typical BC seismic design approach; **TBD** — Site-specific seismic parameters; Decomposition Section 2 (OBJ-1, OBJ-2)

### Key Decision Documentation

**Example 4: Design Philosophy Statement**

Typical design philosophy content for Design Basis Memorandum:

"The design philosophy for the Canola Oil Transload Facility Phase 1 prioritizes safe and reliable operation (OBJ-1) while achieving the required throughput capacity of 1,000,000 MT per annum (OBJ-2). The design approach emphasizes:

1. **Inherent safety:** Minimize hazards through design rather than relying solely on procedural controls. HAZOP study results (DEL-27.02) inform safety-critical design features.

2. **Operational flexibility:** The facility shall support both tank storage operations and direct rail-to-ship transfer (OBJ-4), with seamless mode transitions and minimal operational complexity.

3. **Regulatory compliance:** All design shall comply with applicable Canadian codes, BC provincial requirements, municipal regulations, and port authority (VFPA) requirements (OBJ-6). Independent design verification (DEL-28.01) provides additional assurance.

4. **Future expandability:** Phase 1 design shall accommodate Phase 2 expansion with minimal disruption (OBJ-8). Critical interfaces and upsizing provisions are identified in coordination with Phase 2 Expansion Documentation (DEL-27.03).

5. **Lifecycle cost optimization:** Design decisions consider both capital cost and long-term operating/maintenance costs (OBJ-9), with preference for reliable, maintainable equipment over lowest first cost.

6. **Environmental stewardship:** Design includes robust containment, spill prevention, and environmental controls exceeding regulatory minimums for high-risk areas (OBJ-7)."

**Source:** **ASSUMPTION**: Typical design philosophy structure aligned with Project Objectives (Decomposition Section 2)

### Lessons Learned Considerations

**Consideration 1: Early Stakeholder Alignment**
- Engage Employer, authorities, and independent verifiers early in design basis development
- Early alignment on key criteria reduces downstream rework and comment cycles
- **TBD** — Specific stakeholder engagement plan
- **Source:** **ASSUMPTION**: Best practice for Design & Build projects

**Consideration 2: Living Document Approach**
- Design basis should evolve through submission stages (30%, 60%, 90%, IFC) as design matures
- Establish change control process for design basis revisions
- Maintain traceability of criteria changes and impact on downstream design
- **TBD** — Design basis change control procedure
- **Source:** **ASSUMPTION**: Staged submission approach per DEL-27.04

**Consideration 3: Interface Management**
- Dedicate specific attention to interfaces: discipline-to-discipline, Contractor-to-Employer, Phase 1-to-Phase 2
- Interface mismatches are common source of design errors and rework
- Use interface control documents or matrices to track and resolve interface requirements
- **TBD** — Interface management approach and tools
- **Source:** **ASSUMPTION**: Interface management best practice for complex projects

**Source for Examples section:** **ASSUMPTION**: Typical design basis content and structure for industrial facility Design & Build project; specific values **TBD** pending Employer's Requirements and detailed design development
