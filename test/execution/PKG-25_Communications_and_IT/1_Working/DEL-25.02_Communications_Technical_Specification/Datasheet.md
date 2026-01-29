# Datasheet: DEL-25.02 Communications Technical Specification

## Identification

| Field | Value |
|-------|-------|
| Deliverable ID | DEL-25.02 |
| Name | Communications Technical Specification |
| Package | PKG-25 Communications & IT |
| Discipline | Specialty |
| Type | Specification |
| Responsible | D&B Contractor |
| Status | INITIALIZED |

**Source:** `_CONTEXT.md` (deliverable folder); Decomposition Section 5 PKG-25

## Attributes

| Attribute | Value | Source/Notes | Spec § | Proc Step |
|-----------|-------|--------------|--------|-----------|
| Document Number | **TBD** | To be assigned per project specification numbering system | Documentation | Step 10 |
| Specification Type | Technical Specification | Product and performance requirements per `_CONTEXT.md` Description | Scope | Purpose |
| Specification Format | **ASSUMPTION**: Section-based (CSI/MasterFormat or similar) | Typical for construction technical specifications | — | Steps 2-4 |
| Revision | **TBD** | Initial issue typically Rev 0 or A | Documentation | Step 11 |
| Applicable Standard | See Standards section below | Multiple telecommunications and electrical standards apply | Standards | Step 1.2 |
| Classification | **ASSUMPTION**: For Construction | Technical specification for procurement and installation | Scope | Step 10.3 |
| Specification Scope | Fiber cable specification, network cabling specification | Decomposition Table PKG-25 DEL-25.02 | Scope | Step 1.5 |

**Source:** `_CONTEXT.md`; Decomposition Table PKG-25 DEL-25.02; **ASSUMPTION** for format

## Conditions

**Operating / Environmental Context:**

Defines performance, materials, and workmanship requirements for communications per ER requirements.

**Source:** `_CONTEXT.md` Description; Decomposition Table PKG-25 DEL-25.02

**Environmental Conditions Affecting Material Selection:**

- **Operating temperature range:** **TBD** — Influences cable jacket ratings and equipment specifications
  - Indoor conditioned spaces: Typical 15-30°C
  - Outdoor installation: **TBD** — Per site climate data (Surrey, BC climate)
  - Industrial areas: **TBD** — May experience elevated temperatures near process equipment

- **Environmental classification:**
  - Indoor dry: Office and control building areas
  - Indoor wet/damp: **TBD** — Potential in some building areas
  - Outdoor: Cable routing between buildings and to field locations
  - Underground: Buried conduit systems
  - **Source:** **ASSUMPTION** based on facility type; **TBD** for specific classifications

- **Hazardous area classification:** **ASSUMPTION**: Most communications infrastructure in Non-Hazardous areas
  - Office and control building: Assumed Non-Hazardous
  - Process areas: **TBD** — Confirm hazardous area classification where cables may route through or near
  - Marine loading area: **TBD** — Confirm classification (likely Class I Div 2 or Zone 2 in some areas)
  - **Source:** **ASSUMPTION**; **TBD** pending facility hazardous area classification study

- **Exposure to UV, chemicals, moisture:**
  - UV exposure: Outdoor cables require UV-resistant jackets
  - Chemical exposure: **TBD** — Canola oil compatibility if cables exposed (unlikely in conduit)
  - Moisture: Outdoor and underground cables require moisture barriers
  - **Source:** **ASSUMPTION** based on facility type

- **Seismic requirements:** **TBD** — BC seismic zone; may affect cable support and equipment mounting
  - **Source:** **TBD** — Per BC Building Code and project seismic criteria

- **Design life:** **ASSUMPTION**: 25 years minimum
  - Cable plant: Typically 20-25 year design life
  - Equipment: Typically 10-15 years before technology refresh
  - **Source:** **ASSUMPTION** — Standard infrastructure design life; **TBD** for project-specific requirements

**Interface Context:**

Per DEC-05 (Decomposition Section 7): Communications is separate from CCTV and access control (PKG-24) but:
- May share cable pathways (with appropriate separation)
- Physical separation required in equipment rooms for security
- Distinct cabling systems per DEC-05

**Source:** Decomposition Section 7 DEC-05

## Construction

**Materials / Configuration:**

Anticipated artifacts (source: Decomposition Table PKG-25 DEL-25.02):
- **Fiber cable specification**
- **Network cabling specification**

**Cable Types and Materials:**

### Fiber Optic Cables

**Fiber Types:**
- Single-mode fiber (SMF): **ASSUMPTION**: OS2 grade (9/125 µm) for long-distance backbone
  - Applications: Building-to-building links, long horizontal runs
  - Distance: Supports multi-kilometer transmission

- Multi-mode fiber (MMF): **ASSUMPTION**: OM3 or OM4 grade (50/125 µm) for shorter runs
  - Applications: Intra-building backbone, equipment room to TR links
  - Distance: 300m (OM3) to 550m (OM4) for 10 Gigabit Ethernet

**Source:** **ASSUMPTION** — Industry standard fiber grades per TIA-568; **TBD** based on system architecture

**Fiber Cable Construction:**
- Fiber count: **TBD** — Based on network design (typical 6, 12, 24, or 48 fiber counts)
- Cable construction: **ASSUMPTION**: Tight-buffered for indoor/building use; loose-tube for outdoor/OSP use
- Jacket material: **TBD** — OFNR (riser), OFNP (plenum), or OSP (outdoor) rating as applicable per installation environment
- Tensile strength: **TBD** — Per installation method (direct burial, aerial, duct, building)
- Bend radius: Typically 10× cable OD minimum per TIA-568
- **Source:** **ASSUMPTION** — TIA-568.3 fiber optic cabling standard; **TBD** for specific selections

### Copper Network Cabling

**Cable Category:**
- **ASSUMPTION**: Category 6 (Cat 6) or Category 6A (Cat 6A) UTP or F/UTP
  - Cat 6: Supports up to 1000Base-T (1 Gigabit Ethernet), 250 MHz
  - Cat 6A: Supports up to 10GBase-T (10 Gigabit Ethernet), 500 MHz
- **TBD** — Actual category based on bandwidth requirements and future-proofing strategy

**Cable Construction:**
- Conductor size: **ASSUMPTION**: 23 AWG (0.57mm) solid copper
- Pair count: 4-pair (8 conductor) per TIA-568 structured cabling standard
- Shielding: **ASSUMPTION**: UTP (unshielded) or F/UTP (foiled) depending on EMI environment
  - UTP for typical office/control building
  - F/UTP or F/FTP (shielded) near electrical equipment or EMI sources
- Jacket rating: **TBD** — CM (communications), CMR (riser), or CMP (plenum) per NEC/CSA and installation location
- **Source:** **ASSUMPTION** — TIA-568.2-D copper cabling standard; **TBD** for specific selections

**Other Communications Materials:**

- **Patch cords:** Factory-terminated, same category as installed cable, various lengths
- **Connectors:**
  - Fiber: LC, SC, or MPO/MTP connectors per system design — **TBD**
  - Copper: RJ45 modular connectors per TIA-568
- **Patch panels:** Fiber and copper, rack-mounted per DEL-25.03
- **Cable management:** J-hooks, D-rings, Velcro wraps, cable managers (no metal fasteners on cables)
- **Grounding and bonding:** Telecommunications bonding backbone (TBB) and telecommunications bonding conductor (TBC) per TIA-607
- **Labeling:** Machine-printed labels per TIA-606 administration standard

**Source:** **ASSUMPTION** — Industry standard practice per TIA standards

**Installation Requirements:**

- Installation methods: Per TIA-568 and TIA-569 pathways and spaces
- Minimum bend radius: Per cable manufacturer and TIA-568 (typically 4× cable OD for horizontal, 10× for vertical/backbone)
- Maximum pulling tension: Per cable manufacturer (typically 110N for Cat 6/6A)
- Cable support spacing: **TBD** — Per TIA-569 and building code (typical 1.5m horizontal, less for vertical)
- Separation from power: **TBD** — Per NEC/CSA and TIA-569 (typical 300mm from power < 5kVA)
- Firestopping: Per building code for all penetrations through fire-rated assemblies
- Testing requirements: See DEL-25.04 for installation and test records

**Source:** **ASSUMPTION** — TIA standards and NEC/CSA requirements; **TBD** for project-specific installation criteria

**Workmanship Requirements:**

- Terminations: Per TIA-568 termination standards and cable manufacturer instructions
- Cable dressing: Neat, organized, no kinks or sharp bends
- Cable jacket removal: Minimum necessary, maintain cable integrity
- No crushing or deforming of cables during installation
- Label all cables, patch panels, and outlets per TIA-606
- **TBD** — Project-specific workmanship standards and quality control

**Source:** **ASSUMPTION** — Industry standard workmanship per TIA standards

## References

**Decomposition:**
- `/Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md` — Section 5 PKG-25, Section 7 DEC-05

**Deliverable Folder:**
- `_CONTEXT.md` — Deliverable identity and description
- `_REFERENCES.md` — Reference materials (currently no references identified)
- `_DEPENDENCIES.md` — Dependency tracking mode: NOT_TRACKED

**Applicable Standards:**

**Telecommunications Standards:**
- **ASSUMPTION**: TIA-568.0 (Generic Telecommunications Cabling for Customer Premises)
- **ASSUMPTION**: TIA-568.1 (Commercial Building Telecommunications Cabling Standard - General Requirements)
- **ASSUMPTION**: TIA-568.2-D (Balanced Twisted-Pair Telecommunications Cabling and Components Standard)
- **ASSUMPTION**: TIA-568.3-D (Optical Fiber Cabling and Components Standard)
- **ASSUMPTION**: TIA-569-D (Telecommunications Pathways and Spaces)
- **ASSUMPTION**: TIA-606-B (Administration Standard for Telecommunications Infrastructure)
- **ASSUMPTION**: TIA-607-C (Generic Telecommunications Bonding and Grounding for Customer Premises)
- **TBD** — ISO/IEC 11801 series if applicable as alternative/supplement to TIA standards

**Cable and Component Standards:**
- **ASSUMPTION**: UL 444 (Communications Cables) or CSA C22.2 No. 214 equivalent
- **ASSUMPTION**: UL 1666 (Test for Flame Propagation Height of Electrical and Optical-Fiber Cable Installed Vertically in Shafts)
- **ASSUMPTION**: CAN/ULC-S102 (Standard Method of Test for Surface Burning Characteristics of Building Materials and Assemblies)
- **TBD** — Specific cable product standards for selected cable types

**Electrical and Safety Standards:**
- CSA C22.1 (Canadian Electrical Code) or NEC Article 770 (Optical Fiber Cables and Raceways) and Article 800 (Communications Circuits)
- Alberta OHS Code
- CSA Z462 (Electrical Safety in the Workplace)

**Testing Standards:**
- **ASSUMPTION**: TIA-568 (field testing standards for copper and fiber)
- **ASSUMPTION**: TIA-526-7, TIA-526-14 (optical power loss measurement)
- **ASSUMPTION**: TIA-568.2-D Annex (transmission performance testing for copper)

**Project-Specific Requirements:**
- Employer's Requirements: **TBD** — Specific sections related to communications to be identified
- **TBD** — Project Technical Specifications template or master spec
- **TBD** — Project Quality Management Plan

**Source:** **ASSUMPTION** for industry standards; **TBD** for project-specific documents not yet indexed

**Cross-references:**
- DEL-25.01 — Communications Design Drawing Set (spatial design implements this specification)
- DEL-25.03 — Communications Data Sheet Package (equipment specifications complement cable specifications)
- DEL-25.04 — Communications Installation & Test Records (testing per this specification's requirements)
- PKG-24 — Security Systems (coordination for cable separation per DEC-05)
- PKG-19 — Control Systems (network integration)
- PKG-17 — Electrical Power Distribution (grounding and bonding)

**Project Objectives:**
- **Note:** PKG-25 not explicitly listed in Objective-to-Deliverable Mapping (Decomposition Section 6)
- **ASSUMPTION**: General applicability of:
  - OBJ-1 (Safe & Reliable Operation) — Material and performance standards ensure reliable communications
  - OBJ-6 (Regulatory Compliance) — Compliance with electrical codes and safety standards
  - OBJ-9 (Lifecycle Cost Optimization) — Material selection and quality affect long-term costs

---

## Summary of Key TBDs and Assumptions

**Critical TBDs Requiring Resolution:**
1. Employer's Requirements for communications cable performance and materials
2. Cable category selection (Cat 6 vs Cat 6A) based on bandwidth requirements and budget
3. Fiber type and grade selection (SMF vs MMF, OM3 vs OM4) based on network architecture
4. Environmental conditions (temperature ranges, hazardous area classification) affecting cable ratings
5. Project specification format and template

**Key Assumptions Requiring Validation:**
1. Applicability of TIA-568 family of standards (vs ISO/IEC 11801 or other international standards)
2. CSA C22.1 applicability vs NEC or other electrical codes
3. Standard telecommunications materials and construction practices
4. 25-year design life for cable plant infrastructure
5. Non-hazardous area classification for majority of communications infrastructure

**Source:** Compilation from TBDs and ASSUMPTIONs across document

---

## Cross-Document Verification (Pass 3)

| Check | Status | Notes |
|-------|--------|-------|
| Datasheet ↔ Specification consistency | ✓ Verified | Cable types, standards, materials aligned |
| Datasheet ↔ Guidance consistency | ✓ Verified | Principles align with material selections |
| Datasheet ↔ Procedure consistency | ✓ Verified | Attributes traceable to procedure steps |
| Terminology consistency | ✓ Verified | Consistent use of: Cat 6/6A, SMF/MMF, OM3/OM4/OS2, TIA standards |
| TBD completeness | ✓ Verified | All unknowns marked TBD with resolution path |
| ASSUMPTION labeling | ✓ Verified | All inferences labeled ASSUMPTION |
| Source citations | ✓ Verified | Non-trivial values cite TIA standards or decomposition |

**Pass 3 enrichment completed:** Cross-document linkages strengthened with explicit Specification § and Procedure Step references in Attributes table.
