# Specification: DEL-25.02 Communications Technical Specification

## Scope

This specification defines the requirements for **Communications Technical Specification** within **PKG-25 Communications & IT**.

**Purpose:** Defines performance, materials, and workmanship requirements for communications per ER requirements.

**Source:** `_CONTEXT.md` Description; Decomposition Table PKG-25 DEL-25.02

**Anticipated deliverable artifacts:**
- Fiber cable specification
- Network cabling specification

**Source:** Decomposition Table PKG-25 DEL-25.02

**Package Scope Context:**

PKG-25 covers:
- Communications network
- Fiber infrastructure
- Patch panels
- Workstation connectivity

**Source:** Decomposition Section 5 PKG-25 (Scope)

**Specification Organization:**

This technical specification document is expected to contain two major sections:
1. Fiber optic cable system specification
2. Copper network cabling system specification

Each section addresses materials, performance, installation, testing, and workmanship requirements.

**Source:** Inference from anticipated artifacts; **ASSUMPTION** — Standard technical specification structure

## Requirements

### Functional Requirements

#### FR-1: Fiber Optic Cable System

**FR-1.1 System Performance:**
- The fiber optic cable system shall support the data rates and transmission distances required by the facility network architecture
- **TBD** — Specific data rates (1G, 10G, 40G, 100G Ethernet or other)
- **TBD** — Maximum transmission distances for each link type
- **Source:** **TBD** — Pending network architecture definition from design basis

**FR-1.2 Fiber Type and Grade:**
- Single-mode fiber (SMF): **ASSUMPTION**: OS2 grade (9/125 µm) minimum for backbone and long-distance links per TIA-568.3
  - Attenuation: ≤ 0.5 dB/km at 1310nm, ≤ 0.5 dB/km at 1550nm
  - Zero dispersion wavelength: 1300-1324 nm

- Multi-mode fiber (MMF): **ASSUMPTION**: OM3 (50/125 µm) minimum for short intra-building links
  - Attenuation: ≤ 3.0 dB/km at 850nm, ≤ 1.0 dB/km at 1300nm
  - Bandwidth: ≥ 1500 MHz·km at 850nm

- **TBD** — Actual fiber type selection based on network design and distance requirements
- **Source:** TIA-568.3-D Table 4 (fiber performance); **ASSUMPTION** for grades; **TBD** for selections

**FR-1.3 Cable Configuration:**
- Fiber count: **TBD** — Based on port count requirements (typical 6, 12, 24, 48, or 72 fiber)
- Color coding: Per TIA-598-C fiber optic color coding standard
  - Fiber 1-12: Blue, Orange, Green, Brown, Slate, White, Red, Black, Yellow, Violet, Rose, Aqua
  - Repeat for higher fiber counts with binder groups
- **Source:** TIA-598-C; **TBD** for fiber counts

**FR-1.4 Environmental Suitability:**
- Indoor cables (building pathways):
  - Tight-buffered construction
  - Plenum-rated (OFNP) or riser-rated (OFNR) jacket per installation location and building code
  - Operating temperature: **TBD** — Typically -20°C to +60°C minimum

- Outdoor cables (inter-building, OSP):
  - Loose-tube construction with water-blocking gel or dry water-blocking materials
  - UV-resistant black PE jacket
  - Operating temperature: **TBD** — Per Surrey, BC climate (recommend -40°C to +70°C)
  - Crush and rodent resistance: **TBD** — For direct burial applications

- **Source:** **ASSUMPTION** — TIA-568.3 and industry practice; **TBD** for specific environmental ratings

#### FR-2: Copper Network Cabling System

**FR-2.1 System Performance:**
- The copper cabling system shall support structured cabling per TIA-568 for horizontal and backbone applications
- Minimum cable category: **ASSUMPTION**: Category 6 (Class E) or Category 6A (Class EA)
  - Cat 6: 1000Base-T (1 Gbps), 250 MHz bandwidth, 100m channel
  - Cat 6A: 10GBase-T (10 Gbps), 500 MHz bandwidth, 100m channel
- **TBD** — Actual category selection based on bandwidth requirements and budget
- **Source:** TIA-568.2-D; **ASSUMPTION** for minimum category; **TBD** for selection

**FR-2.2 Cable Construction:**
- Conductor: 23 AWG (0.57 mm) solid bare copper
- Configuration: 4-pair (8 conductor) per TIA-568 standard
- Insulation: Polyethylene or FEP as applicable for category rating
- Shielding: **TBD** — UTP (unshielded), F/UTP (overall foil), or F/FTP (foil per pair and overall) based on EMI environment
  - **ASSUMPTION**: UTP for office/control building; F/UTP near electrical or process equipment
- Pair twist and balance: Per TIA-568.2-D requirements for selected category
- **Source:** TIA-568.2-D Table 1-4; **ASSUMPTION** for shielding selection; **TBD** for final selection

**FR-2.3 Cable Jacket Rating:**
- Jacket material and fire rating per NEC Article 800 or CSA C22.1:
  - CMP (plenum): For air handling spaces
  - CMR (riser): For vertical risers between floors
  - CMG or CM (general purpose): For general building use
- **TBD** — Jacket rating selection per cable routing and building code requirements
- **Source:** NEC Article 800 / CSA C22.1; **TBD** for specific applications

**FR-2.4 Environmental Suitability:**
- Indoor installation: Operating temperature **TBD** — Typically -20°C to +60°C
- Outdoor or harsh environment cabling (if required): **TBD** — UV-resistant, moisture-resistant jackets; conduit installation recommended
- **Source:** **ASSUMPTION** — Standard cable environmental ratings; **TBD** for specific requirements

#### FR-3: Connectivity and Hardware

**FR-3.1 Connectors:**
- Fiber connectors: **TBD** — LC, SC, ST, or MPO/MTP per network equipment and patch panel specifications (see DEL-25.03)
  - **ASSUMPTION**: LC connectors common for enterprise networks
  - Polish type: UPC (Ultra Physical Contact) for multimode and single-mode; APC (Angled Physical Contact) for long-haul single-mode if required
  - Insertion loss: ≤ 0.75 dB typical per TIA-568.3

- Copper connectors: 8-position modular connector (RJ45) per TIA-568.2-D
  - Category rating matching cable (Cat 6 or Cat 6A)
  - Shielded connector if F/UTP or F/FTP cable used

- **Source:** TIA-568.2-D and TIA-568.3; **ASSUMPTION** for LC; **TBD** for specific selections

**FR-3.2 Patch Panels and Termination Hardware:**
- See DEL-25.03 Communications Data Sheet Package for patch panel specifications
- Fiber termination: Factory-terminated pigtails or field termination per installer qualifications
- Copper termination: 110-style punch-down or keystone jack per patch panel type
- **TBD** — Termination method selection based on installer capabilities and project quality requirements
- **Source:** Cross-reference to DEL-25.03; **TBD** for methods

#### FR-4: Cable Pathways (Coordinate with DEL-25.01)

**FR-4.1 Pathway Requirements:**
- See DEL-25.01 Communications Design Drawing Set for pathway design and routing
- Pathways shall comply with TIA-569 requirements:
  - Adequate capacity for initial installation plus spare capacity for future growth
  - Physical protection appropriate to environment
  - Separation from EMI sources and power cables per TIA-569 Table 4.3-1
- **TBD** — Pathway fill ratios and spare capacity percentage
- **Source:** TIA-569-D; Cross-reference to DEL-25.01

### Performance Requirements

#### PR-1: Transmission Performance

**PR-1.1 Fiber Link Performance:**
- Maximum link attenuation (insertion loss):
  - Multimode links: **TBD** — Typically ≤ 2.0 dB for 100m, ≤ 3.5 dB for 300m per TIA-568.3
  - Single-mode links: **TBD** — Varies with distance; typically ≤ 1.5 dB for 2km
- Connector insertion loss: ≤ 0.75 dB per connector pair (typical) per TIA-568.3
- Splice loss: ≤ 0.3 dB per splice (if splices used)
- Return loss (reflectance): **TBD** — Typically ≥ 20 dB for UPC, ≥ 60 dB for APC
- **Source:** TIA-568.3-D Tables; **TBD** for project-specific limits based on equipment and distances

**PR-1.2 Copper Link/Channel Performance:**
- All installed cabling shall meet or exceed TIA-568.2-D Category 6 or 6A performance requirements:
  - Insertion loss, NEXT, PS-NEXT, ELFEXT, PS-ELFEXT, return loss per TIA-568.2-D Tables
  - DC resistance: ≤ 9.38 Ω/100m for 23 AWG
  - Propagation delay: ≤ 555 ns/100m
  - Delay skew: ≤ 50 ns/100m
- **TBD** — Specific performance class (Class E for Cat 6, Class EA for Cat 6A)
- **Source:** TIA-568.2-D Tables 6-12 through 6-23; **TBD** for class selection

**PR-1.3 Testing Requirements:**
- All installed cable links shall be tested per TIA-568 and test results documented
- See DEL-25.04 Communications Installation & Test Records for test record requirements
- **Source:** TIA-568 field testing requirements; cross-reference to DEL-25.04

#### PR-2: Physical Performance

**PR-2.1 Cable Physical Properties:**
- Minimum bend radius:
  - Fiber: 10× cable OD for installed, 20× cable OD during installation (no load)
  - Copper: 4× cable OD for installed horizontal, 10× cable OD for installed backbone
- Maximum pulling tension:
  - Fiber: Per manufacturer (typically 220N for distribution cable)
  - Copper: 110N (25 lbf) maximum for Cat 6/6A
- Crush resistance: **TBD** — For outdoor and buried cables
- **Source:** TIA-568; **ASSUMPTION** for typical values; **TBD** for specific requirements

**PR-2.2 Fire Performance:**
- All cables shall meet fire rating per NEC Article 770/800 or CSA C22.1:
  - Plenum cables: UL 910 / CAN/ULC-S102 flame and smoke test
  - Riser cables: UL 1666 vertical tray flame test
- **TBD** — Specific fire test standards applicable to project jurisdiction
- **Source:** NEC Article 770.179, 800.179; **ASSUMPTION** for UL/ULC standards; **TBD** for jurisdiction

#### PR-3: Reliability and Quality

**PR-3.1 Product Quality:**
- All cables and connectivity hardware shall be listed by a recognized testing laboratory:
  - **ASSUMPTION**: UL listed or CSA certified
  - **TBD** — Other acceptable certifications (ETL, CE, etc.)
- Manufacturer warranty: **TBD** — Minimum warranty period (typical 20-25 years for structured cabling systems if installed per manufacturer requirements)
- **Source:** **ASSUMPTION** — Industry standard practice; **TBD** for specific requirements

**PR-3.2 Installation Quality:**
- All installations shall comply with manufacturer's installation instructions
- Workmanship shall meet TIA-568 requirements and industry best practices
- See Workmanship Requirements section below
- **Source:** TIA-568; **ASSUMPTION** — Standard quality requirements

### Interface Requirements

**Coordination Required With:**

- **DEL-25.01 Communications Design Drawing Set:**
  - Cable routes and pathway design inform cable types and lengths
  - Equipment room and TR layouts inform patch panel and cable requirements

- **DEL-25.03 Communications Data Sheet Package:**
  - Network equipment specifications inform cable category and fiber type requirements
  - Patch panel specifications must match cable termination types

- **DEL-25.04 Communications Installation & Test Records:**
  - Testing requirements and acceptance criteria defined in this specification
  - Test methods and documentation per DEL-25.04

- **PKG-17 Electrical Power Distribution:**
  - Cable separation requirements from power cables and EMI sources
  - Grounding and bonding coordination per TIA-607

- **PKG-19 Control Systems:**
  - Network cable requirements for control system integration
  - Cable shielding requirements near control equipment

- **PKG-21, PKG-22 Buildings:**
  - Fire-rated cable requirements for building penetrations
  - Firestopping and fire barrier penetrations

- **PKG-24 Security Systems:**
  - Cable separation per DEC-05 (separate systems)
  - Potential shared pathways with appropriate separation

**Source:** Logical dependencies; DEC-05 (Decomposition Section 7); cross-references to PKG-25 deliverables

### Quality Requirements

#### QR-1: Material Quality

**QR-1.1 Product Standards:**
- All cables shall comply with applicable TIA-568 performance standards
- All cables shall be manufactured per:
  - **ASSUMPTION**: UL 444 (Communications Cables) or CSA C22.2 No. 214
  - **ASSUMPTION**: TIA-568.2-D (copper) and TIA-568.3-D (fiber)
- Product certifications required: **TBD** — UL listing, CSA certification, or other
- **Source:** **ASSUMPTION** for standards; **TBD** for specific certifications

**QR-1.2 Manufacturer Qualifications:**
- Cable manufacturers shall have demonstrated experience in telecommunications cable manufacturing
- **TBD** — Minimum years of experience or approved manufacturer list
- **ASSUMPTION**: Major telecommunications cable manufacturers acceptable (e.g., Belden, CommScope, Panduit, Corning, etc.)
- **Source:** **ASSUMPTION** for typical acceptable manufacturers; **TBD** for project-specific requirements

**QR-1.3 Material Submittals:**
- Contractor shall submit product data sheets and certifications for all cables and connectivity hardware
- Submittals shall include:
  - Manufacturer and model/part numbers
  - Performance test data demonstrating compliance with TIA-568
  - UL/CSA listings and certifications
  - Warranty information
- **TBD** — Submittal requirements and approval process per project procedures
- **Source:** **ASSUMPTION** — Standard construction submittal practice; **TBD** for project process

#### QR-2: Installation Quality

**QR-2.1 Installer Qualifications:**
- Installers shall be trained and experienced in structured cabling installation
- **ASSUMPTION**: BICSI-certified installers preferred (Installer 2 or higher)
- **TBD** — Mandatory installer certifications or qualifications
- **Source:** **ASSUMPTION** for industry standard qualifications; **TBD** for project requirements

**QR-2.2 Workmanship Standards:**

**General:**
- All work shall comply with TIA-568, TIA-569, and manufacturer's installation instructions
- Installations shall be neat, accessible, and maintainable
- Cable identification and labeling per TIA-606 (see DEL-25.01)

**Cable Installation:**
- No kinks, sharp bends, or crushing of cables
- Minimum bend radius maintained at all times
- Maximum pulling tension not exceeded
- Cable jacket damage repaired or cable replaced
- Horizontal cables: Single, continuous length from TR to outlet (no splices)
- Backbone cables: Splices only at designated splice locations per design

**Terminations:**
- Fiber terminations: Clean, inspected, and tested per TIA-568.3
  - Connector end-face cleanliness per IEC 61300-3-35
  - Visual inspection for scratches, contamination, or damage
- Copper terminations: Per TIA-568.2-D
  - Maintain pair twist to within 13mm (0.5 in) of termination point
  - No untwisting of pairs beyond requirements
  - Proper punch-down or crimp per connector type

**Cable Support:**
- Support spacing: **TBD** — Per TIA-569 and building code (typical 1.5m for horizontal, less for vertical)
- Support type: J-hooks, D-rings, or cable ties (Velcro wraps preferred; no metal zip ties on cables)
- No over-tightening of support fasteners

**Cable Separation:**
- Maintain separation from power cables per TIA-569 Table 4.3-1:
  - **ASSUMPTION**: 300mm (12 in) from power cables < 5kVA unshielded, 150mm if in separate conduit
  - **TBD** — Separation requirements for higher power levels or specific project conditions

**Source:** TIA-568, TIA-569, TIA-606, TIA-607, IEC 61300-3-35; **ASSUMPTION** for typical practices; **TBD** for project-specific requirements

**QR-2.3 Quality Control and Inspection:**
- Contractor shall perform self-inspection prior to testing
- **TBD** — Third-party inspection or owner's representative witness requirements
- **TBD** — Hold points for inspection (e.g., before concealment, after termination)
- **Source:** **TBD** — Per project quality plan; **ASSUMPTION** for self-inspection

#### QR-3: Testing and Acceptance

**QR-3.1 Field Testing Requirements:**
- All copper links: Test per TIA-568.2-D using qualified test equipment
  - Test to permanent link or channel configuration as applicable
  - Test reports showing pass/fail and margin for all parameters

- All fiber links: Test per TIA-568.3-D
  - OTDR testing for backbone and long runs
  - Insertion loss testing for all links
  - Polarity verification

- **TBD** — Acceptance testing witnessed by Owner or representative
- **Source:** TIA-568; **TBD** for witness requirements

**QR-3.2 Test Equipment:**
- Test equipment shall be calibrated and certified
- **ASSUMPTION**: Fluke, Ideal Networks, or equivalent test equipment
- Calibration current (within past 12 months)
- **Source:** **ASSUMPTION** for typical test equipment; TIA-568 test equipment requirements

**QR-3.3 Test Documentation:**
- See DEL-25.04 Communications Installation & Test Records
- Test reports for all installed links
- **TBD** — Electronic submittal format and requirements
- **Source:** Cross-reference to DEL-25.04; **TBD** for format

## Standards

**Applicable Codes and Standards:**

**Primary Telecommunications Standards:**
- TIA-568.0-D: Generic Telecommunications Cabling for Customer Premises
- TIA-568.1-E: Commercial Building Telecommunications Cabling Standard - General Requirements
- TIA-568.2-D: Balanced Twisted-Pair Telecommunications Cabling and Components Standard
- TIA-568.3-D: Optical Fiber Cabling and Components Standard
- TIA-569-D: Telecommunications Pathways and Spaces
- TIA-606-B: Administration Standard for Telecommunications Infrastructure
- TIA-607-C: Generic Telecommunications Bonding and Grounding for Customer Premises
- TIA-598-C: Optical Fiber Cable Color Coding

**Alternative/International Standards:**
- **TBD** — ISO/IEC 11801 series if applicable as alternative to TIA standards
- **TBD** — Other international standards (EN, IEC, etc.)

**Electrical Codes:**
- CSA C22.1 Canadian Electrical Code, Part I (or NEC as applicable):
  - Article 770: Optical Fiber Cables and Raceways
  - Article 800: Communications Circuits
- Alberta OHS Code
- CSA Z462: Electrical Safety in the Workplace

**Fire and Building Codes:**
- National Building Code of Canada (NBCC) (or BC Building Code as applicable)
- CAN/ULC-S102: Standard Method of Test for Surface Burning Characteristics of Building Materials and Assemblies
- **ASSUMPTION**: UL 910 (Plenum cable test) and UL 1666 (Riser cable test) or CSA equivalents

**Product Standards:**
- UL 444: Communications Cables (or CSA C22.2 No. 214)
- UL 2043: Fire Test for Heat and Visible Smoke Release (plenum cables)
- **TBD** — Other applicable UL, CSA, or international product standards

**Testing Standards:**
- TIA-526-7: Measurement of Optical Power Loss of Installed Single-Mode Fiber Cable Plant
- TIA-526-14: Measurement of Optical Power Loss of Installed Multimode Fiber Cable Plant
- IEC 61300-3-35: Fiber Optic Connector and Passive Component Endface Cleaning and Inspection

**Project-Specific Requirements:**
- Employer's Requirements: **TBD** — Specific communications requirements sections to be identified
- **TBD** — Project Technical Specifications or Master Specification sections
- **TBD** — Project Quality Management Plan
- **TBD** — Project Design Criteria

**Source:** Industry standard references; **TBD** for project-specific documents

**Standard Application Notes:**
- Latest edition of standards in effect at time of specification preparation unless otherwise specified
- Where conflicts exist between standards, resolution required per project procedures
- TIA standards are primary; where TIA is silent, refer to manufacturer recommendations and industry best practice

## Verification

**Verification Methods for Specification Deliverables:**

1. **Technical Review Against Standards:**
   - Verify all requirements cite appropriate TIA, NEC/CSA, or other standards
   - Check that specified cable categories, fiber grades, and performance criteria align with TIA-568
   - Confirm fire ratings and jacket types comply with electrical code
   - **Verification by:** Originating engineer or specification writer

2. **Interdisciplinary Review:**
   - Coordinate with DEL-25.01 (drawings) to ensure specification aligns with design
   - Coordinate with DEL-25.03 (data sheets) for equipment compatibility
   - Review with PKG-17 (Electrical) for grounding, bonding, and separation requirements
   - Review with PKG-19 (Control Systems) for network integration requirements
   - **Verification by:** Interdisciplinary coordination meeting or document review

3. **Employer Review and Comment:**
   - Submit draft specification to Employer (or Employer's representative) for review
   - Address and incorporate Employer comments
   - **TBD** — Employer review process and timeline
   - **Verification by:** Employer or designated representative

4. **Compliance Matrix Verification:**
   - Develop matrix showing how specification requirements map to Employer's Requirements
   - **TBD** — Compliance matrix format and requirements
   - **Verification by:** Quality or engineering lead

**Source:** **ASSUMPTION** for typical specification verification methods; **TBD** for project-specific processes

**Acceptance Criteria:**

Per the verification workflow (to be defined in Procedure.md):
- All technical review comments resolved and closed
- Specification checked and approved by discipline lead
- No unresolved interdisciplinary conflicts
- Employer review comments addressed and incorporated (if applicable)
- Compliance with project specification format and standards verified
- **TBD** — Specific approval authorities and sign-off requirements

**Source:** **ASSUMPTION** — Standard acceptance criteria; **TBD** for project-specific approvals; cross-reference to Procedure.md

**Verification Records:**
- Review comment logs and resolutions
- Interdisciplinary coordination meeting minutes or comment responses
- Employer review transmittals and comment responses (if applicable)
- Compliance matrix (if required)
- Approval signatures per project procedures
- **TBD** — Records location and retention requirements

**Source:** **ASSUMPTION** — Standard QA/QC record practice; **TBD** for project requirements

## Documentation

**Required Documentation Outputs:**

Per Decomposition Table PKG-25 DEL-25.02:
- **Fiber cable specification**
- **Network cabling specification**

These may be organized as:
- Two separate specification documents (one for fiber, one for copper), or
- One combined communications cabling specification with separate sections for fiber and copper
- **TBD** — Document organization per project specification format

**Source:** Decomposition Table PKG-25 DEL-25.02; **TBD** for organization

**Supporting Documentation:**

- Product data sheets and cut sheets for specified materials (part of submittal process during construction, not part of this deliverable)
- Design calculations (if applicable): **TBD** — May include link loss budgets, power budgets, etc.
- Compliance matrix mapping specification requirements to Employer's Requirements: **TBD**
- **Source:** **TBD** for supporting documentation requirements

**Documentation Requirements:**

**Format and Media:**
- Electronic format: **TBD** — PDF, Word, or other formats per project EDMS requirements
- **ASSUMPTION**: Formatted per project specification template or master spec format
- Revision control: Per project document numbering system — **TBD**

**Submittal Requirements:**
- **TBD** — Submittal schedule and milestones (align with DEL-25.01 drawing submittals)
- **TBD** — Number of copies and distribution list
- **TBD** — Review and approval workflow

**File Management:**
- Native files: **TBD** — Word, InDesign, or other source files
- Archive and backup: **TBD** — Project archive requirements

**Source:** **ASSUMPTION** for standard practices; **TBD** for project-specific requirements

**Cross-Reference to Related Deliverables:**

- DEL-25.01 Communications Design Drawing Set — Design drawings implement this specification's requirements
- DEL-25.03 Communications Data Sheet Package — Equipment selections must be compatible with cable specifications
- DEL-25.04 Communications Installation & Test Records — Installation and testing per this specification's requirements
- See Datasheet.md References section for additional cross-references

**Source:** Logical relationship between PKG-25 deliverables

---

## Cross-Document Consistency Check

**This section verifies alignment between the four documents for DEL-25.02:**

| Requirement/Entity | Datasheet | Specification | Guidance | Procedure |
|-------------------|-----------|---------------|----------|-----------|
| Fiber cable specification | Construction | FR-1, PR-1.1 | Principles, Examples | (Steps TBD) |
| Network cabling specification | Construction | FR-2, PR-1.2 | Principles, Examples | (Steps TBD) |
| TIA-568 standards | References | Standards, Requirements | Principles | Prerequisites |
| Cat 6/6A copper cable | Construction | FR-2.1, FR-2.2 | Trade-offs | (Steps TBD) |
| SMF/MMF fiber types | Construction | FR-1.2 | Trade-offs | (Steps TBD) |
| Cable performance testing | Construction | PR-1, QR-3 | Considerations | Verification |
| Fire ratings (plenum/riser) | Construction | FR-2.3, PR-2.2 | Considerations | (Steps TBD) |
| Workmanship requirements | Construction | QR-2.2 | Principles | (Steps TBD) |
| Installer qualifications | — | QR-2.1 | Considerations | Prerequisites |
| Material submittals | — | QR-1.3 | — | (Steps TBD) |
| Interface with DEL-25.01 | References | Interface Req. | Considerations | Prerequisites |
| Interface with DEL-25.03 | References | Interface Req. | Considerations | Prerequisites |
| Interface with DEL-25.04 | References | Interface Req., QR-3 | — | Verification |

**Consistency verification:** All key entities and requirements are addressed across all four documents where applicable.

**Source:** Cross-document consistency check (Pass 1 enrichment)
