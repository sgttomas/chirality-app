# Procedure: DEL-27.03 Phase 2 Expansion Documentation

## Purpose

This procedure defines the process for producing **Phase 2 Expansion Documentation** within **PKG-27 Engineering Design**.

**Scope:** Documents Phase 2 expansion requirements, Phase 1-Phase 2 interfaces, and Phase 1 design provisions to facilitate future Phase 2 expansion with minimal disruption per OBJ-8.

**Deliverable type:** Report (General Arrangement Drawing + Engineering Memo)
**Responsible party:** D&B Contractor

**Downstream use:** Phase 2 Expansion Documentation informs Phase 1 detailed engineering (all disciplines implement provisions), Employer strategic planning (Phase 2 business case and timing decisions), and future Phase 2 engineering (Phase 2 design builds on Phase 1 provisions).

**Source:** _CONTEXT.md; Decomposition DEL-27.03; Specification.md

## Prerequisites

### Dependencies

Per `_DEPENDENCIES.md`: **NOT_TRACKED** — Dependencies coordinated externally.

**Key dependencies:**
- DEL-27.01 (Design Basis Documents) — Phase 1 design basis informs Phase 2 interface requirements
- Employer's Phase 2 strategic direction and scope guidance — **TBD**
- Phase 1 P&IDs, site plans, general arrangement (preliminary or developing) — **TBD**
- Site investigation data (geotechnical, survey, environmental) — **TBD**
- Fraser Surrey Terminal master plan — **TBD**

**Source:** _DEPENDENCIES.md; Specification.md (Interface Requirements)

### Reference Materials

- DEL-27.01: Design Basis Documents
- Employer's Requirements (all volumes) — **location TBD**
- Phase 1 P&IDs, drawings, site plans — **TBD**
- Site investigation reports — **TBD**
- Fraser Surrey Terminal master plan — **TBD**
- Applicable codes/standards (same as Phase 1): NBC/NBCC, CSA standards — **location TBD**

**Source:** _REFERENCES.md; Datasheet.md

### Personnel Requirements

- Expansion Planning Lead (P.Eng. with multi-discipline facility design and expansion experience)
- Discipline leads (civil, structural, mechanical, electrical, controls) — input on provisions
- Project Manager — coordination and Employer interface
- CAD technician/designer — Phase 2 general arrangement drawing

**Source:** **ASSUMPTION**: Typical personnel for expansion planning deliverable

## Steps

### Step 1: Define Phase 2 Scope and Requirements

**1.1 Obtain Employer's Phase 2 Direction**
- Engage Employer to understand Phase 2 strategic objectives, drivers, timeline
- Obtain Phase 2 capacity targets (**TBD**: throughput, storage, railcar/marine loading)
- Understand Phase 2 business case triggers and decision points
- Clarify Phase 2 budget for provisions in Phase 1

**Outputs:** Phase 2 scope statement (conceptual level); Employer's strategic guidance documented

**1.2 Define Phase 2 Expansion Scenarios**
- If Phase 2 scope uncertain, define planning scenarios (e.g., Low/Base/High expansion cases)
- Base scenario: Most likely Phase 2 scope (e.g., double Phase 1 capacity)
- High scenario: Maximum credible Phase 2 expansion for provision sizing
- Document assumptions for each scenario

**Outputs:** Phase 2 expansion scenarios defined with capacity ranges and facility requirements

**Source:** Specification.md (FR-1); **ASSUMPTION**: Scenario planning if Phase 2 scope uncertain

### Step 2: Identify Phase 1-Phase 2 Interfaces

**2.1 Conduct Multi-Discipline Interface Workshops**
- Hold workshops with all discipline leads to brainstorm Phase 1-Phase 2 interfaces
- Systematic review by system: Railcar unloading, storage tanks, transfer piping, marine loading, utilities, electrical, controls, civil/site

**Interface identification checklist (by discipline):**
- **Mechanical/Process:** Piping tie-in points, pump capacity, tank connections, loading arm additions
- **Electrical:** Power distribution tie-ins, transformer capacity, spare breakers, cable routing
- **Controls:** I/O capacity, network infrastructure, control room expansion, HMI scalability
- **Civil/Structural:** Foundations (tanks, equipment), pipe racks, access roads, drainage, site grading
- **Safety/Fire Protection:** Fire water capacity, detection/suppression coverage, emergency access

**Outputs:** Phase 1-Phase 2 interface register (list of all identified interfaces with locations, sizes, capacities)

**2.2 Assess Interface Criticality**
- Prioritize interfaces based on cost-to-change analysis (Guidance.md Principle 3):
  - Critical (must provide in Phase 1): Underground utilities, foundations, footprint
  - Important (should provide): Spare connections, capacity margins, structural provisions
  - Low priority (can defer): Above-ground modifications, instrumentation, procedures

**Outputs:** Interface register with priority rankings

**Source:** Specification.md (FR-2); Guidance.md (Principle 3); **ASSUMPTION**: Multi-discipline workshop approach

### Step 3: Define Phase 1 Design Provisions

**3.1 Develop Provision Recommendations by Discipline**
- Each discipline lead develops recommendations for Phase 1 provisions to support Phase 2
- Provisions categorized: Upsizing, Spare connections, Footprint reservations, Capacity margins, Design flexibility

**Provision examples (see Guidance.md Examples):**
- Upsizing: Main piping, electrical transformers/feeders, foundations, pipe racks
- Spare connections: Piping blind flanges, electrical spare breakers, control system spare I/O
- Footprint: Tank pad extensions, equipment pads, laydown areas, access roads
- Capacity margins: Pump capacity, relief valve sizing, fire water flow, drainage capacity

**Outputs:** Discipline-specific provision recommendations with technical justification and cost impact estimates (order-of-magnitude)

**3.2 Coordinate and Consolidate Provisions**
- Review all discipline provisions for coordination and consistency
- Resolve conflicts (e.g., piping route conflicts with Phase 2 footprint reservation)
- Ensure multi-discipline provisions align (e.g., piping spare connection has corresponding electrical breaker, structural support, control system I/O)

**Outputs:** Consolidated Phase 1 provision list with multi-discipline coordination confirmed

**3.3 Cost-Benefit Assessment**
- Estimate incremental Phase 1 cost for each provision (order-of-magnitude)
- Estimate Phase 2 rework cost if provision omitted (order-of-magnitude)
- Calculate provision value: Phase 2 savings / Phase 1 incremental cost
- Prioritize provisions by value; recommend high-value provisions for Phase 1 implementation

**Outputs:** Provision cost-benefit analysis; prioritized provision recommendations

**Source:** Specification.md (FR-3); Guidance.md (Trade-offs); **ASSUMPTION**: Cost-benefit analysis supports provision decision-making

### Step 4: Prepare Phase 2 General Arrangement Drawing

**4.1 Develop Phase 1 Site Layout (Baseline)**
- Obtain Phase 1 site plan/general arrangement from civil/site design team
- Verify Phase 1 facility locations, dimensions, access, utilities

**4.2 Develop Phase 2 Expansion Layout (Conceptual)**
- Position Phase 2 facilities on site plan based on:
  - Phase 2 capacity requirements (number/size of tanks, unloading stations, loading arms, etc.)
  - Site constraints (available land, setbacks, existing facilities, access, utilities)
  - Operational efficiency (minimize piping runs, optimize truck/rail/marine access)
  - Phase 1-Phase 2 interfaces (proximity for tie-ins)
  - Construction logistics (laydown, access independent of Phase 1 operations)
- Develop 2-3 Phase 2 layout options if multiple configurations feasible

**4.3 Prepare Phase 2 General Arrangement Drawing**
- Compile Phase 1 (as-designed) and Phase 2 (conceptual) on single site plan drawing
- Show Phase 1-Phase 2 interface locations (tie-in points, spare connections, expansion boundaries)
- Show Phase 2 footprint reservations (areas reserved for Phase 2, not to be built on in Phase 1)
- Include legend, notes, title block per project CAD standards — **TBD**
- Scale: Typically 1:500 to 1:2000 for site plan — **TBD**

**Outputs:** Phase 2 General Arrangement Drawing (draft for review)

**Source:** Specification.md (FR-4); Datasheet.md; **ASSUMPTION**: General arrangement drawing prepared by CAD technician under engineer direction

### Step 5: Prepare Phase 2 Engineering Memo

**5.1 Compile Phase 2 Engineering Memo**

Prepare comprehensive memo per Datasheet.md structure:

1. **Executive Summary:** Phase 2 objectives, Phase 1 provisions, key recommendations
2. **Phase 2 Scope and Requirements:** Capacity targets, facility additions, timeline, regulatory considerations
3. **Phase 1-Phase 2 Interface Requirements:** Interface register with locations, sizes, capacities, priorities
4. **Phase 1 Upsizing and Provisions:** Detailed provision recommendations by discipline with justification and cost impact
5. **Phase 2 Facility Concept:** Phase 2 description, general arrangement (reference drawing), cost estimate (OME), schedule estimate
6. **Construction and Operational Continuity:** Phase 2 construction approach, tie-in strategies, shutdown minimization
7. **Recommendations:** Prioritized list of Phase 1 provisions required for Phase 2 expandability; future Phase 2 studies/decisions

**Content guidance:**
- Be specific: Provision recommendations must be actionable for Phase 1 design teams (sizes, locations, quantities)
- Document assumptions: Phase 2 scope assumptions, cost assumptions, schedule assumptions
- Flag TBDs: Items requiring further study or Employer decision
- Provide options: If multiple approaches feasible, present options with pros/cons/recommendations

**Outputs:** Phase 2 Engineering Memo (draft for review)

**Source:** Specification.md (FR-5); Datasheet.md; **ASSUMPTION**: Memo structure per Datasheet.md template

### Step 6: Review and Finalize

**6.1 Multi-Discipline Review**
- Distribute draft Phase 2 documentation to all discipline leads for review
- Reviewers verify: Provisions are feasible, correctly specified, incorporated in their discipline scope
- Address review comments; revise documents

**Outputs:** Reviewed and revised Phase 2 Expansion Documentation

**6.2 Internal Approval**
- Obtain internal approvals: Expansion Planning Lead, Project Engineering Manager, Project Manager
- **TBD** — Approval workflow per project procedures

**Outputs:** Internally approved Phase 2 Expansion Documentation

**6.3 Employer Review and Approval**
- Submit Phase 2 Expansion Documentation to Employer
- **TBD** — Submission timing (likely 60% or 90% design stage when Phase 1 design mature)
- Address Employer comments; obtain Employer approval

**Outputs:** Employer-approved Phase 2 Expansion Documentation; issued to `3_Issued/`

**Source:** Specification.md (QR-2, Verification); **ASSUMPTION**: Standard review and approval process

### Step 7: Implementation and Tracking

**7.1 Distribute Provisions to Discipline Teams**
- Distribute provision list to all discipline leads with implementation instructions
- Each discipline incorporates provisions into their deliverables (P&IDs, drawings, specs, calcs)
- Mark provisions clearly: "Future Phase 2" labels on drawings, specs include Phase 2 notes

**7.2 Track Provision Implementation**
- Maintain provision tracking register: Provision ID, Description, Discipline, Status (Open/In Progress/Closed), Evidence (where documented in Phase 1 deliverables)
- Periodic reviews to verify provisions are not missed or omitted during detailed engineering

**7.3 Final Verification**
- Before Phase 1 design finalization (IFC stage), verify all Phase 2 provisions are implemented
- Expansion Planning Lead reviews Phase 1 deliverables to confirm provisions present

**Outputs:** Phase 1 design incorporates all approved Phase 2 provisions; tracking register shows all provisions closed

**Source:** Specification.md (VM-2); **ASSUMPTION**: Provision implementation tracking ensures provisions not lost during detailed engineering

## Verification

**Verification activities:**
- VM-1: Phase 2 scope defined (Employer approval)
- VM-2: Phase 1-Phase 2 interfaces identified (completeness check by discipline leads)
- VM-3: Phase 1 provisions specified and implemented in Phase 1 deliverables (tracking register, spot checks)
- VM-4: Multi-discipline coordination verified (no conflicts, no gaps)
- VM-5: Employer approval obtained

**Source:** Specification.md (Verification)

## Records

**Primary outputs:**
1. Phase 2 General Arrangement Drawing
2. Phase 2 Engineering Memo
3. Phase 1-Phase 2 interface register
4. Provision tracking register

**Filing:** Working versions `1_Working/`; review versions `2_Checking/`; issued versions `3_Issued/`

**Source:** Specification.md (Documentation); **ASSUMPTION**: Standard deliverable lifecycle per AGENTS.md
