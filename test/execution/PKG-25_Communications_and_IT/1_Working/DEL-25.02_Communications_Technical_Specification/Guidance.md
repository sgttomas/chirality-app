# Guidance: DEL-25.02 Communications Technical Specification

## Purpose

This guidance document supports the development of **Communications Technical Specification** for **PKG-25 Communications & IT**.

**Deliverable Purpose:** Defines performance, materials, and workmanship requirements for communications per ER requirements.

**Source:** `_CONTEXT.md` Description; Decomposition Table PKG-25 DEL-25.02

**Context:**
- Deliverable Type: **Specification** (technical requirements document)
- Discipline: **Specialty** (communications infrastructure)
- Responsible Party: **D&B Contractor**
- Package: PKG-25 Communications & IT

**Source:** `_CONTEXT.md`; Decomposition Table PKG-25 DEL-25.02

**Role in Project:**

This technical specification defines the "what" and "how" for communications cable materials, performance, and installation quality. It serves as:
- Procurement specification for cable and materials procurement
- Installation standard for construction contractors
- Acceptance criteria for testing and commissioning (DEL-25.04)
- Design input for spatial layout (DEL-25.01) and equipment selection (DEL-25.03)

The specification ensures that the communications infrastructure meets performance requirements, complies with codes and standards, and supports reliable facility operations per OBJ-1.

**Source:** Inference from deliverable type and role; Decomposition Section 2 (OBJ-1)

## Principles

**Engineering Rationale (Communications Cabling):**

### 1. Structured Cabling System Design

**Principle:** Structured cabling follows a standardized, hierarchical architecture that provides flexibility, scalability, and vendor independence.

**Rationale:**
- **TIA-568 compliance** ensures interoperability between equipment from different vendors
- **Physical layer independence** allows network technology changes without recabling
- **Standardized components** (connectors, patch panels, cable categories) simplify procurement, installation, and maintenance
- **Star topology** (from equipment room/TRs to work areas) provides fault isolation and ease of troubleshooting

**Application:**
- Specify standard cable categories (Cat 6, Cat 6A) and fiber grades (OM3, OM4, OS2) per TIA-568
- Require standard connector types (RJ45, LC, SC) for compatibility
- Design for modularity: work areas connect to TRs, TRs connect to equipment room

**Source:** **ASSUMPTION** — TIA-568 structured cabling principles; industry best practice

### 2. Performance-Based Specification

**Principle:** Specify performance requirements rather than prescriptive materials where possible, allowing contractor/vendor flexibility while ensuring outcomes.

**Rationale:**
- Performance-based approach allows innovation and cost optimization
- Vendor competition on performance rather than specific products
- Outcome focus: "shall support 10GBase-T" rather than "shall be Brand X cable"

**Balance:**
- Must specify minimum standards (TIA-568 category, fiber grade) for baseline quality
- May specify acceptable manufacturers or "or approved equal" for quality control
- Prescriptive requirements where specific interoperability needed (e.g., connector types matching equipment)

**Application:**
- Specify cable category/grade and performance criteria per TIA-568
- Allow contractor to select manufacturer within approved list
- Require submitted products to demonstrate compliance via test data

**Source:** **ASSUMPTION** — Performance-based specification philosophy common in construction

### 3. Code and Standard Compliance

**Principle:** All materials and installation methods shall comply with applicable electrical codes, fire codes, and telecommunications standards.

**Rationale:**
- **Safety:** Electrical codes (CSA C22.1/NEC) ensure safe installation and operation
- **Fire safety:** Fire-rated cables and firestopping prevent fire spread through cable pathways
- **Performance:** TIA standards ensure cable system performance for network operation
- **Regulatory compliance:** Meets OBJ-6 (Regulatory Compliance)

**Key Code Requirements:**
- Cable fire ratings (plenum, riser, general) per NEC Article 770/800 or CSA C22.1
- Cable separation from power circuits per TIA-569 and electrical code
- Grounding and bonding per TIA-607 and electrical code
- Firestopping at fire-rated barriers per building code

**Application:**
- Reference applicable code articles in specification requirements
- Specify fire-rated cables per installation environment
- Require installer compliance with codes and manufacturer instructions

**Source:** CSA C22.1, NEC, TIA-568, TIA-569, TIA-607; Decomposition Section 2 (OBJ-6)

### 4. Quality Through Testing and Verification

**Principle:** Field testing of all installed cable links verifies performance and provides documentation for future troubleshooting.

**Rationale:**
- **Proof of performance:** Testing confirms installed system meets specification
- **Early defect detection:** Identifies installation defects before energization
- **Documentation:** Test records provide baseline for future troubleshooting and maintenance

**Testing Scope:**
- **100% testing required:** All copper and fiber links tested per TIA-568
- Copper: Insertion loss, NEXT, return loss, and all Category parameters
- Fiber: Insertion loss (light loss) and OTDR for backbone cables

**Application:**
- Specify field testing requirements in specification per TIA-568 test methods
- Require calibrated test equipment and qualified testers
- Require test documentation per DEL-25.04

**Source:** TIA-568 field testing requirements; **ASSUMPTION** — Industry standard practice

### 5. Lifecycle and Maintainability Considerations

**Principle:** Material and installation quality decisions should consider total lifecycle cost, not just initial cost.

**Rationale:**
- **Long design life:** Communications infrastructure typically 20-25 years
- **Future technology support:** Higher-grade cables (Cat 6A vs. Cat 6, OM4 vs. OM3) may support future bandwidth needs without replacement
- **Maintenance access:** Proper installation and labeling reduce troubleshooting time and cost
- **Warranty:** Manufacturer system warranties (20-25 years common) require compliant installation

**Application:**
- Consider Cat 6A vs. Cat 6 trade-off for future 10Gig support (see Trade-offs section)
- Specify proper cable support, bend radius, and workmanship for reliability
- Require labeling per TIA-606 for maintainability
- Balance initial cost vs. lifecycle cost per OBJ-9 (Lifecycle Cost Optimization)

**Source:** **ASSUMPTION** — Lifecycle cost principles; Decomposition Section 2 (OBJ-9)

**Applicable Standards Context:**

- **TIA-568 family:** The foundation for structured cabling; defines architecture, performance, and testing
- **TIA-569:** Cable pathways and spaces; informs routing and separation requirements
- **TIA-606:** Administration and labeling; critical for operations and maintenance
- **TIA-607:** Grounding and bonding; ensures electrical safety and proper system grounding
- **CSA C22.1 / NEC:** Electrical safety; mandates fire-rated cables and installation methods
- **Source:** See Specification.md Standards section

## Considerations

**Factors to Consider During Development:**

### 1. Cable Category and Grade Selection

**Copper Cable Category:**
- **Cat 6** (Category 6, Class E):
  - Supports: 1000Base-T (1 Gigabit Ethernet), 250 MHz bandwidth
  - Distance: 100m channel per TIA-568
  - Cost: Lower material and installation cost than Cat 6A

- **Cat 6A** (Category 6A, Class EA):
  - Supports: 10GBase-T (10 Gigabit Ethernet), 500 MHz bandwidth
  - Distance: 100m channel per TIA-568 (vs. 55m for Cat 6 at 10Gig)
  - Cost: Higher material cost, larger cable diameter (more difficult to install)

**Fiber Type and Grade:**
- **Multimode (OM3, OM4):**
  - Applications: Short links (< 300-550m), intra-building backbone
  - Cost: Lower transceiver cost (LED or VCSEL), higher cable cost than single-mode
  - OM4 supports longer 10G+ distances than OM3

- **Single-mode (OS2):**
  - Applications: Long links (> 500m), inter-building, long-term future-proofing
  - Cost: Higher transceiver cost (laser), lower cable cost than multimode
  - Future-proof: Supports all current and foreseeable data rates

**Decision Drivers:**
- Current bandwidth requirements vs. future expansion (OBJ-8)
- Link distances per site layout (from DEL-25.01)
- Budget constraints
- Technology lifecycle planning

**Source:** TIA-568; Decomposition Section 2 (OBJ-8); **ASSUMPTION** — Industry considerations

### 2. Shielding Requirements (UTP vs. F/UTP vs. F/FTP)

**Shielding Options for Copper Cabling:**
- **UTP (Unshielded Twisted Pair):**
  - Lower cost, smaller diameter, easier to install and terminate
  - Suitable for typical office/control building with low EMI

- **F/UTP (Foiled Unshielded Twisted Pair):**
  - Overall foil shield around all pairs
  - Better EMI immunity for installations near electrical equipment or process areas
  - Requires grounded patch panels and proper bonding

- **F/FTP (Foiled Foiled Twisted Pair) or S/FTP:**
  - Individual foil shields per pair plus overall shield
  - Maximum EMI immunity, higher cost, more difficult to install

**Decision Drivers:**
- Proximity to power cables and electrical equipment
- Hazardous area classification (shielded may be preferred in some cases)
- Grounding infrastructure availability (shielded requires proper grounding)
- Budget and installation complexity

**Typical Application:**
- UTP: Office areas, control building (away from power distribution)
- F/UTP: Near electrical rooms, cable routing with power cables, industrial areas
- F/FTP: High-EMI environments, near VFDs or high-power equipment

**Source:** TIA-568.2-D; **ASSUMPTION** for typical applications; **TBD** based on facility EMI assessment

### 3. Cable Fire Ratings and Jacket Selection

**Fire Rating Hierarchy (highest to lowest):**
- **CMP (Plenum):** For air-handling spaces (plenums, ducts)
  - Lowest smoke generation, highest fire resistance
  - Required by building code for plenum spaces
  - Highest cost

- **CMR (Riser):** For vertical risers between floors
  - Prevents vertical fire spread
  - Required by building code for vertical penetrations

- **CMG/CM (General Purpose):** For general building use (horizontal runs on same floor)
  - Lower cost
  - Acceptable for non-plenum, non-riser applications

- **CMX (Residential):** Not typically used in commercial/industrial

**Outdoor Cables:**
- **OSP (Outside Plant):** UV-resistant, moisture-resistant, may be direct-burial rated
- Typically not fire-rated (outdoor, not in building)

**Decision Drivers:**
- Cable routing per DEL-25.01 design (plenum spaces, risers, general areas)
- Building code requirements
- Cost optimization: Don't over-specify (e.g., plenum cable in conduit not necessary)

**Source:** NEC Article 800, CSA C22.1; **ASSUMPTION** for typical application

### 4. Fiber Connector Types

**Common Fiber Connector Options:**
- **LC (Lucent Connector):** Small form-factor, duplex or simplex, most common in modern enterprise networks
- **SC (Subscriber Connector):** Square connector, duplex or simplex, older standard still in use
- **ST (Straight Tip):** Bayonet mount, simplex, older standard
- **MPO/MTP (Multi-fiber Push-On):** 12 or 24-fiber array connector, used for high-density trunk cables

**Decision Drivers:**
- Network equipment ports (see DEL-25.03) — must match equipment
- Patch panel type — must match connector type
- Density requirements — LC or MPO for high density
- Standardization — consistency across facility for interoperability

**Typical Selection:**
- **LC** for most modern installations (equipment room and TR patch panels)
- **MPO/MTP** for high-density backbone trunks (optional)

**Source:** **ASSUMPTION** — Industry trends and typical practice; **TBD** based on equipment selection (DEL-25.03)

### 5. Installation Environment and Physical Protection

**Environmental Factors:**
- Indoor conditioned (office, control building): Standard indoor-rated cables
- Indoor harsh (wet, damp areas): Moisture-resistant jackets, conduit recommended
- Outdoor (inter-building): OSP-rated cables, UV-resistant, moisture barriers
- Underground (buried): Direct-burial rated or in duct, crush-resistant, rodent protection (armored jacket or innerduct)
- Aerial (overhead): Messenger wire support or self-supporting (figure-8 cable)

**Physical Protection:**
- Conduit (rigid, EMT, PVC): Maximum protection, required in some areas by code
- Cable tray: Good protection for large cable quantities, accessible
- Innerduct (in larger conduit or direct burial): Allows future cable replacement
- Direct burial: Lowest cost for outdoor, requires burial depth and route marking

**Source:** TIA-569; **ASSUMPTION** for typical methods; **TBD** based on routing design (DEL-25.01)

### 6. Coordination with Design and Equipment Selection

**Interfaces with Other PKG-25 Deliverables:**
- **DEL-25.01 (Design Drawings):** Cable routing informs cable types and lengths; TR and equipment room layouts inform patch panel and cable requirements
- **DEL-25.03 (Data Sheets):** Equipment port types (fiber LC vs. SC, copper Cat 6 vs. 6A) must match cable specifications
- **DEL-25.04 (Test Records):** Test methods and acceptance criteria defined in this specification

**Coordination Required:**
- Iterate between specification, design, and equipment selection for consistency
- Ensure cable performance supports network equipment requirements
- Confirm connector types match patch panels and equipment ports

**Source:** Cross-references to PKG-25 deliverables

### 7. Regulatory and Code Compliance

**Key Compliance Areas:**
- **Electrical Safety:** CSA C22.1 or NEC compliance for cable installation and separation
- **Fire Safety:** Building code compliance for cable fire ratings and firestopping
- **Workplace Safety:** Alberta OHS and CSA Z462 for installation work safety
- **Telecommunications Standards:** TIA-568 compliance for system performance

**Compliance Strategy:**
- Reference applicable code articles in specification
- Require installer compliance certifications or training (e.g., BICSI, manufacturer)
- Require third-party product certifications (UL, CSA listings)
- Conduct testing per TIA-568 to verify performance compliance

**Source:** Specification.md Standards section; **ASSUMPTION** for compliance strategy

### 8. Submittal and Procurement Process

**Material Submittal Considerations:**
- Contractor submits product data sheets and certifications before procurement
- Review submittal for compliance with specification requirements
- Approve or reject with comments
- **TBD** — Submittal process and timeline per project procedures

**Procurement Lead Time:**
- Standard cables: Typically stock items, short lead time
- Custom cables (special fiber counts, lengths, jacket types): May require manufacturing lead time
- Consider lead times in project schedule coordination

**Source:** **ASSUMPTION** — Standard construction procurement process; **TBD** for project specifics

### 9. Quality and Warranty

**Quality Considerations:**
- Specify reputable manufacturers with demonstrated telecommunications experience
- Require UL/CSA listings for product quality assurance
- Require installer qualifications (BICSI or equivalent) for installation quality

**Manufacturer Warranty:**
- Many manufacturers offer 20-25 year system warranties if:
  - All components (cable, connectors, patch panels) are from same manufacturer
  - Installation performed per manufacturer instructions
  - System tested and registered with manufacturer
- Consider warranty benefits vs. mixed-vendor cost savings

**Source:** **ASSUMPTION** — Industry warranty practices; **TBD** for project warranty requirements

## Trade-offs

**Competing Concerns to Evaluate:**

### 1. Cable Category: Cat 6 vs. Cat 6A

**Trade-off:** Cat 6 (1 Gig) vs. Cat 6A (10 Gig) for horizontal copper cabling

**Cat 6 Advantages:**
- Lower material cost
- Smaller cable diameter, easier to install, more cables fit in pathways
- Adequate for current 1 Gig Ethernet requirements

**Cat 6A Advantages:**
- Supports 10GBase-T for full 100m (Cat 6 limited to 55m at 10G)
- Future-proofs for bandwidth growth per OBJ-8
- May avoid re-cabling in 5-10 years if 10 Gig becomes standard

**Typical Resolution:**
- Cat 6A recommended for new installations unless budget-constrained
- Consider hybrid: Cat 6A for backbone and critical areas, Cat 6 for general workstations
- **TBD** — Project decision based on budget and future requirements

**Source:** **ASSUMPTION** — Industry trend toward Cat 6A; Decomposition Section 2 (OBJ-8); **TBD** for project decision

### 2. Fiber Type: Multimode vs. Single-Mode

**Trade-off:** Multimode (OM3/OM4) vs. Single-mode (OS2) for backbone and inter-building links

**Multimode Advantages:**
- Lower transceiver cost (LED/VCSEL optics vs. laser)
- Adequate for short intra-building links (< 300-550m depending on data rate and grade)

**Single-Mode Advantages:**
- Longer distances (kilometers), suitable for any facility size
- Lower cable cost (simpler construction, smaller core)
- Future-proof for all data rates
- No distance limitations for campus

**Typical Resolution:**
- Single-mode recommended for all backbone and inter-building
- Multimode acceptable for short intra-building if distance < 300m and cost savings significant
- Consider total cost: transceiver cost difference vs. cable cost difference and future-proofing
- **TBD** — Project decision based on facility layout (DEL-25.01) and budget

**Source:** **ASSUMPTION** — Industry practice; **TBD** for project decision

### 3. Shielding: UTP vs. F/UTP

**Trade-off:** Unshielded vs. foil-shielded copper cabling

**UTP Advantages:**
- Lower cost
- Easier to install and terminate
- Adequate for typical office/control building with low EMI

**F/UTP Advantages:**
- Better EMI immunity for industrial environment or near electrical equipment
- May be required in certain hazardous area classifications (verify with AHJ)

**Typical Resolution:**
- UTP for office and control building areas (away from power distribution)
- F/UTP for industrial areas, near electrical rooms, or routing with power cables
- Balance cost vs. EMI risk based on facility layout and equipment locations
- **TBD** — Project decision based on EMI assessment and facility zoning

**Source:** **ASSUMPTION** — Typical application guidelines; **TBD** for project EMI assessment

### 4. Plenum vs. Riser Cable

**Trade-off:** Plenum-rated (CMP) vs. Riser-rated (CMR) cable in non-plenum risers or conduit

**Plenum Advantages:**
- Can be used anywhere (plenum, riser, or general)
- Simplifies inventory (one cable type for all)

**Riser/General Advantages:**
- Lower cost than plenum
- Adequate when not in plenum space or in conduit

**Typical Resolution:**
- Use appropriate rating for location per building code:
  - Plenum (CMP) for air-handling spaces
  - Riser (CMR) for vertical shafts not used for air handling
  - General (CM/CMG) for horizontal runs on same floor or in conduit
- Don't over-specify (e.g., plenum cable in conduit not required, wastes budget)
- **TBD** — Cable routing and fire rating requirements per DEL-25.01 and building code review

**Source:** NEC Article 800, CSA C22.1; **ASSUMPTION** for cost optimization approach

### 5. Quality vs. Cost: Approved Manufacturers

**Trade-off:** Limiting approved manufacturers vs. allowing broader competition

**Limited Manufacturer List Advantages:**
- Ensures known quality and warranty support
- Simplifies standardization and future procurement
- May simplify coordination if system warranty desired (all from one vendor)

**Broader Competition Advantages:**
- Lower cost through competition
- Availability and lead time flexibility
- Contractor preference and experience

**Typical Resolution:**
- Specify "or approved equal" to allow competition while maintaining quality baseline
- List 3-5 acceptable major manufacturers (e.g., Belden, CommScope, Panduit, Corning, etc.) to guide quality level
- Require submittals with performance test data demonstrating TIA-568 compliance
- **TBD** — Approved manufacturer list or "or equal" approach per project procurement strategy

**Source:** **ASSUMPTION** — Construction specification practice; **TBD** for project approach

## Examples

**Reference Examples and Precedents:**

### Industry Standards and Guides

- **TIA-568 Standards:** Provide detailed cable specifications, performance tables, and testing requirements
- **BICSI TDMM (Telecommunications Distribution Methods Manual):** Industry reference for design and installation practices
- **Manufacturer Installation Guides:** (e.g., Belden, CommScope, Panduit) provide detailed cable specifications and installation instructions
- **Source:** **ASSUMPTION** — Standard industry references

### Project-Specific References

- **Employer's Requirements:** **TBD** — Review for communications cable requirements, performance criteria, and acceptable materials
- **Employer's Existing Facility Standards:** **TBD** — Terminal may have existing communications standards to follow for consistency
- **Similar Facilities:** **TBD** — Lessons learned from other transload or terminal facilities regarding cable types and installation methods

**Source:** **TBD** — Pending access to project-specific documents

### Anticipated Artifacts for Reference

Per Decomposition Table PKG-25 DEL-25.02:
- **Fiber cable specification:** Typically includes fiber type/grade, cable construction, connector types, performance requirements, testing requirements
- **Network cabling specification:** Typically includes cable category, jacket rating, connector types, performance requirements, workmanship standards, testing requirements

**Source:** Decomposition Table PKG-25 DEL-25.02

### Typical Specification Organization

Technical specifications for communications cabling often organized as:

1. **Section 1: General**
   - Scope and related work
   - References and standards
   - Submittals and quality assurance
   - Delivery, storage, and handling

2. **Section 2: Products**
   - Cable specifications (fiber and copper)
   - Connectivity hardware (connectors, patch panels, jacks)
   - Cable support and protection (trays, conduits, J-hooks)
   - Grounding and bonding materials
   - Labeling materials

3. **Section 3: Execution**
   - Installation methods and workmanship
   - Cable routing and support
   - Terminations and connections
   - Testing and commissioning
   - Cleanup and protection

**Source:** **ASSUMPTION** — CSI MasterFormat or similar specification organization

### Example Performance Tables

**Example: TIA-568.2-D Category 6A Performance (simplified):**
- Frequency range: 1-500 MHz
- Insertion loss: ≤ 2.0 dB/100m at 1 MHz to ≤ 23.1 dB/100m at 500 MHz
- NEXT: ≥ 74.3 dB at 1 MHz to ≥ 53.3 dB at 500 MHz
- Return loss: ≥ 20.0 dB at 1 MHz to ≥ 10.0 dB at 500 MHz
(Full tables in TIA-568.2-D)

**Example: TIA-568.3-D Fiber Performance (simplified):**
- OS2 single-mode: ≤ 0.5 dB/km attenuation at 1310nm and 1550nm
- OM3 multimode: ≤ 3.0 dB/km attenuation at 850nm, 1500 MHz·km bandwidth
- OM4 multimode: ≤ 3.0 dB/km attenuation at 850nm, 3500 MHz·km bandwidth
(Full tables in TIA-568.3-D)

**Source:** TIA-568.2-D and TIA-568.3-D (actual standard tables for reference)

## Notes

**Document Status:** This guidance is based on initial deliverable context and industry standard practices. Further refinement expected during specification development as:
- Employer's Requirements are reviewed for specific cable performance and material requirements
- Network architecture is defined (from design basis) to inform cable category and fiber type selections
- Site layout and cable routing are developed (DEL-25.01) to inform cable types, lengths, and environmental ratings
- Equipment selections are made (DEL-25.03) to confirm connector types and compatibility

**Key Assumptions to Validate:**
- Applicability of TIA-568 standards vs. ISO/IEC 11801 or other international standards
- CSA C22.1 vs. NEC applicability for cable fire ratings and installation
- Cable category (Cat 6 vs. Cat 6A) based on bandwidth requirements and budget
- Fiber type (OM3, OM4, OS2) based on distances and network architecture
- Environmental conditions and hazardous area classifications affecting cable ratings

**Production Workflow:**

The actual production of this specification follows the workflow defined in **Procedure.md**, which includes requirements gathering, drafting, technical review, interdisciplinary coordination, comment resolution, and approval. The considerations and trade-offs discussed in this guidance document inform the technical content and decisions made during the specification writing process.

**Source:** **ASSUMPTION** — Standard specification development process; Cross-reference to Procedure.md
