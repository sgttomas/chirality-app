# Guidance: DEL-25.01 Communications Design Drawing Set

## Purpose

This guidance document supports the development of **Communications Design Drawing Set** for **PKG-25 Communications & IT**.

**Deliverable Purpose:** Defines the design arrangement and details for communications per ER requirements.

**Source:** `_CONTEXT.md` Description; Decomposition Table PKG-25 DEL-25.01

**Context:**
- Deliverable Type: **Drawing** (design documentation)
- Discipline: **Specialty** (communications infrastructure)
- Responsible Party: **D&B Contractor**
- Package: PKG-25 Communications & IT

**Source:** `_CONTEXT.md`; Decomposition Table PKG-25 DEL-25.01

**Role in Project:**

Communications infrastructure supports:
- Facility operations and management
- Control system data networks (integration with PKG-19)
- Administrative functions (offices, control building)
- Potential future expansion (OBJ-8)

This drawing set provides the spatial design and physical arrangement to implement the communications network specified in DEL-25.02 and composed of equipment defined in DEL-25.03.

**Source:** Inference from package scope; Decomposition Section 2 (OBJ-8 Future Expandability)

## Principles

**Engineering Rationale (Communications Infrastructure):**

1. **Structured Cabling Approach:**
   - Modern communications infrastructure typically follows structured cabling principles (TIA-568 family)
   - Hierarchical topology: equipment room (ER) → telecommunications rooms (TRs) → work areas
   - Physical layer independence: Cable plant supports multiple network technologies
   - **Source:** **ASSUMPTION** — Industry best practice for commercial/industrial facilities

2. **Redundancy and Reliability:**
   - Critical systems may require redundant pathways or fiber routes
   - Single points of failure should be identified and mitigated per OBJ-1 (Safe & Reliable Operation)
   - Equipment room locations should consider reliability (power, HVAC, accessibility)
   - **Source:** Decomposition Section 2 (OBJ-1); **ASSUMPTION** — Standard reliability engineering

3. **Scalability and Future Growth:**
   - Design should accommodate future capacity growth per OBJ-8 (Future Expandability)
   - Cable pathways should include spare capacity (typical 25-40% spare)
   - Equipment room space should allow for additional equipment
   - **Source:** Decomposition Section 2 (OBJ-8); **ASSUMPTION** — Industry practice for infrastructure longevity

4. **Physical Layer Performance:**
   - Cable plant design must support required bandwidth and distance limitations
   - Fiber optic for long distances and high bandwidth; copper for shorter runs
   - Proper termination and testing per TIA standards ensures performance
   - **Source:** **ASSUMPTION** — Telecommunications engineering principles

5. **Separation and Protection:**
   - Communications cables must be separated from power and EMI sources per code requirements
   - Physical protection required based on exposure (indoor vs outdoor, accessible vs restricted)
   - Fire-rated cables and firestopping for penetrations per building code
   - **Source:** **ASSUMPTION** — NEC/CSA and TIA-569 requirements

**Applicable Standards Context:**

- **TIA-568**: Defines structured cabling system architecture and performance
- **TIA-569**: Defines pathways, spaces, and design considerations for cable infrastructure
- **TIA-606**: Provides administration and labeling standards critical for operations and maintenance
- **CSA C22.1 / NEC**: Electrical safety requirements for cable installation
- **Source:** See Specification.md Standards section; **ASSUMPTION** of applicability

## Considerations

**Factors to Consider During Development:**

### 1. Facility Layout and Zones

- Identify all areas requiring network connectivity: offices, control rooms, MCC building, field enclosures
- Determine equipment room (main ER) location: typically in control building
- Identify telecommunications room (TR) locations for distributed areas
- Consider outdoor cable routing between buildings and to field equipment
- **TBD** — Site layout drawings to inform routing decisions
- **Source:** Inference from transload facility type; **TBD** for specific layouts

### 2. User Requirements and Density

- Determine number and type of network outlets per area
- Voice and data requirements: **TBD** — Based on operational staffing and functions
- Workstation density in offices vs. control rooms
- Field locations requiring network access (control panels, remote I/O, cameras if IP-based in future)
- **TBD** — Employer's operational requirements
- **Source:** **TBD** — Pending requirements definition

### 3. Network Architecture and Topology

- Fiber backbone topology: star, ring, or mesh based on redundancy needs
- Horizontal cabling architecture: home-run to TR vs. consolidation points
- Network segmentation: separation of operational network from administrative network (security consideration)
- Integration points with control system network (PKG-19)
- **TBD** — Network design basis and requirements
- **Source:** **TBD** — Network architecture decisions; coordination with PKG-19

### 4. Pathway Design

- Cable tray vs. conduit selection based on environment and flexibility needs
- Tray routing: overhead vs. underfloor vs. wall-mounted
- Conduit sizing for underground or concrete-encased runs
- Shared infrastructure with other disciplines: coordinate with electrical, I&C per Specification.md Interface Requirements
- Fire-rated pathway requirements at fire barriers
- **TBD** — Pathway routing corridors and sizing calculations
- **Source:** Specification.md Interface Requirements; **ASSUMPTION** — Standard pathway design practice

### 5. Equipment Room and TR Design

- Space requirements: racks, cable management, work clearance per TIA-569
- Environmental requirements: HVAC for equipment cooling, humidity control
- Power requirements: coordination with PKG-17 for UPS-backed power
- Grounding and bonding per TIA-607 and electrical codes
- Physical security and access control
- **TBD** — Equipment room layouts and environmental specifications
- **Source:** **ASSUMPTION** — TIA-569 and TIA-607 requirements; coordination with PKG-17, PKG-22

### 6. Coordination with Adjacent Packages

Per DEC-05 (Decomposition Section 7): Communications is separate from CCTV and access control (PKG-24), but may share:
- Cable pathways (with appropriate separation)
- Equipment room space
- Power distribution (different circuits but same panel potentially)

Coordination required:
- **PKG-19 Control Systems:** Network integration for SCADA/control data
- **PKG-21, PKG-22 Buildings:** Pathway routing, penetrations, equipment room space
- **PKG-17 Electrical:** Power supply to communications equipment
- **PKG-24 Security:** Shared infrastructure, separation of systems

**Source:** Decomposition Section 7 DEC-05; Specification.md Interface Requirements

### 7. Regulatory and Code Compliance

- Building code requirements for cable fire ratings (plenum, riser, general purpose)
- Electrical code requirements for cable separation and protection
- Alberta OHS requirements for worker safety during installation and maintenance
- **TBD** — Permit requirements for communications work
- **TBD** — Employer facility standards or terminal-wide communications standards
- **Source:** Specification.md Standards section; **ASSUMPTION** — Standard code applicability

### 8. Constructability and Operability

- Cable routing should be accessible for future maintenance and moves/adds/changes
- Avoid routing through difficult-to-access areas if possible
- Labeling per TIA-606 critical for operational efficiency
- Documentation: As-built drawings essential for future work
- **TBD** — Maintenance access requirements and constraints
- **Source:** **ASSUMPTION** — Lifecycle and maintainability considerations per OBJ-9

### 9. Drawing Organization and Clarity

- Organize drawings logically: overall layout, area details, rack elevations
- Use consistent symbols and legends across all drawings
- Provide adequate detail without cluttering drawings
- Cross-reference between drawings and to other deliverables
- **TBD** — Project drawing standards and conventions
- **Source:** **ASSUMPTION** — Engineering drawing best practices

## Trade-offs

**Competing Concerns to Evaluate:**

### 1. Fiber vs. Copper

**Trade-off:** Fiber optic vs. copper cabling for horizontal runs

**Considerations:**
- **Fiber advantages:** Higher bandwidth, longer distances, immune to EMI, future-proof
- **Fiber disadvantages:** Higher initial cost, specialized termination, more fragile
- **Copper advantages:** Lower cost, easier to terminate, existing equipment compatibility
- **Copper disadvantages:** Distance limitations (~100m), bandwidth limitations, EMI susceptibility

**Typical Resolution:**
- Fiber for backbone and long runs
- Copper (Cat 6/6A) for workstation connections unless special needs
- **TBD** — Project-specific decisions based on requirements and budget

**Source:** **ASSUMPTION** — Standard industry trade-off

### 2. Centralized vs. Distributed Architecture

**Trade-off:** Large centralized equipment room vs. multiple smaller TRs

**Considerations:**
- **Centralized advantages:** Easier management, better security, simpler power/HVAC
- **Centralized disadvantages:** Longer cable runs, single point of failure, may exceed distance limits
- **Distributed advantages:** Shorter cable runs, fault isolation, better coverage for large sites
- **Distributed disadvantages:** More equipment rooms to maintain, higher cost, complexity

**Typical Resolution:**
- Facility size and layout drive decision
- Transload facility may require multiple TRs due to geographic spread
- **TBD** — Based on site layout and operational requirements

**Source:** **ASSUMPTION** — Telecommunications design principles

### 3. Redundancy vs. Cost

**Trade-off:** Redundant fiber paths and equipment vs. cost constraints

**Considerations:**
- Criticality of communications to operations (OBJ-1 Safe & Reliable Operation)
- Financial impact of network downtime
- Budget constraints
- Maintenance windows and repair response time

**Typical Resolution:**
- Critical operational systems (control network) likely require redundancy
- Administrative network may accept lower availability
- **TBD** — Criticality assessment and redundancy requirements

**Source:** Decomposition Section 2 (OBJ-1); **ASSUMPTION** — Risk-based design approach

### 4. Pathway Capacity vs. Cost

**Trade-off:** Generous spare capacity vs. minimizing infrastructure cost

**Considerations:**
- Future expansion plans (OBJ-8)
- Cost of adding capacity later vs. upfront
- Likelihood of changes and additions over facility life
- Industry standard: 25-40% spare capacity typical

**Typical Resolution:**
- Balance based on facility lifecycle and expansion likelihood
- Higher spare capacity in main pathways, less in terminal branches
- **TBD** — Project specific spare capacity requirements

**Source:** Decomposition Section 2 (OBJ-8); **ASSUMPTION** — Industry practice

### 5. Design Detail vs. Schedule

**Trade-off:** Detailed design and coordination vs. schedule pressure

**Considerations:**
- Drawings must be sufficient for construction and coordination
- Over-detailing can delay schedule without proportionate value
- Under-detailing leads to RFIs and field issues

**Typical Resolution:**
- Detail level should match project stage (30%, 60%, 90%, IFC progression)
- Critical interfaces and complex areas require more detail
- Standard installations can reference typical details
- **TBD** — Project design stage and schedule milestones

**Source:** **ASSUMPTION** — Engineering project management principles

## Examples

**Reference Examples and Precedents:**

### Industry Standards and Guides

- **TIA-568**: Provides structured cabling design examples and topologies
- **TIA-569**: Contains pathway sizing examples and design calculations
- **BICSI Telecommunications Distribution Methods Manual (TDMM)**: Industry reference for design practices
- **Source:** **ASSUMPTION** — Standard industry references

### Project-Specific References

- **Employer's Requirements:** **TBD** — Review for communications requirements, performance criteria, and deliverable expectations
- **Employer's Existing Facility Standards:** **TBD** — Terminal may have existing communications standards to follow for consistency
- **Similar Facilities:** **TBD** — Lessons learned from other transload or terminal facilities

**Source:** **TBD** — Pending access to project-specific documents

### Anticipated Artifacts for Reference

Per Decomposition Table PKG-25 DEL-25.01:
- **Fiber network layout:** Shows fiber backbone routing, typically on overall site plan and building floor plans
- **Communications distribution drawings:** Shows structured cabling distribution, typically floor plans with cable pathways and outlet locations
- **Patch panel locations:** Shows equipment room rack elevations with patch panel and equipment mounting

**Source:** Decomposition Table PKG-25 DEL-25.01

### Typical Drawing Types

1. **Cover Sheet / Index:** Drawing list, legends, symbols, abbreviations, general notes
2. **Overall Site Communications Plan:** Fiber routes between buildings, buried/overhead pathways, pole/handhole locations
3. **Building Floor Plans:** Horizontal cabling, outlet locations, TR locations, cable pathway routing
4. **Riser Diagrams:** Vertical cable routing in multi-story buildings
5. **Equipment Room Layouts:** Floor plans showing rack locations, cable entry, clearances
6. **Rack Elevations:** Panel-by-panel layout with patch panels, switches, and cable management
7. **Details:** Cable tray supports, penetration details, grounding details, termination details

**Source:** **ASSUMPTION** — Typical structured cabling drawing set organization

### Coordination Drawing Examples

- **Cable tray coordination drawings:** Showing communications trays in relation to electrical, I&C, and other services
- **Equipment room coordination:** Showing multiple disciplines' equipment and clearances
- **Penetration schedules:** Coordinating all disciplines' sleeves and firestopping

**Source:** **ASSUMPTION** — Standard multi-discipline coordination practice

## Notes

**Document Status:** This guidance is based on initial deliverable context and inferred requirements. Further refinement expected during design development as:
- Employer's Requirements are reviewed and indexed
- Design basis is established
- Coordination with interfacing disciplines progresses
- Project-specific standards and procedures are obtained

**Key Assumptions to Validate:**
- Applicability of TIA standards vs. other international standards
- Facility operational requirements and staffing levels
- Integration requirements with existing terminal infrastructure (if any)
- Employer's preferences for network architecture and equipment
- Specific code editions and project design criteria

**Source:** **ASSUMPTION** — Standard design development process

**Production Workflow:**

The actual production of this drawing set follows the workflow defined in **Procedure.md**, which includes:
- Design initiation and planning (Step 1)
- Design development for each anticipated artifact (Steps 2-4)
- Drawing production and detailing (Step 5)
- Multi-level verification: self-check, IDC, independent check, approval (Steps 6-9)
- Submittal, issuance, and revision management (Steps 10-11)

The considerations and trade-offs discussed in this guidance document inform the design decisions made during the procedure steps.

**Source:** Cross-reference to Procedure.md; Pass 2 enrichment
