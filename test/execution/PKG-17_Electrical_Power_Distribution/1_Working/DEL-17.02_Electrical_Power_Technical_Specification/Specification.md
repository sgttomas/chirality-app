# Specification: DEL-17.02 Electrical Power Technical Specification

## Scope

This specification defines the requirements for **Electrical Power Technical Specification** within **PKG-17 Electrical Power Distribution**.

**Purpose** (Source: Decomposition DEL-17.02 entry): Defines performance, materials, and workmanship requirements for electrical power per ER requirements.

**Package Scope** (Source: Decomposition Section 4 — PKG-17): MV/LV distribution, transformers, switchgear, MCC, panels, grounding, cable installation.

**Anticipated deliverable artifacts** (Source: _CONTEXT.md):
- Transformer specification
- Switchgear specification
- MCC specification
- Cable specification

**Project Context** (Source: Decomposition Section 1):
- **Facility**: Canola oil transload facility at Fraser Surrey Terminal, Surrey, BC
- **Throughput**: 1,000,000 MT/a (OBJ-2)
- **Key Equipment**: Transformers, MV/LV switchgear, motor control centers, power cables for distribution and motor connections

## Requirements

### Functional Requirements

**FR-1: Comprehensive Equipment Specifications**
- Technical specification shall provide complete performance, material, construction, testing, and documentation requirements for all electrical power distribution equipment.
- **Source**: Decomposition DEL-17.02 description (defines performance, materials, and workmanship requirements).
- Equipment categories: Transformers, Switchgear (MV and LV), Motor Control Centers (MCCs), Power Cables (MV and LV).
- **Rationale**: See Guidance.md — Principle 1 (Equipment Specification Completeness).
- **Procedure**: See Procedure.md — Step 4 (Draft Equipment-Specific Specification Sections).

**FR-2: Design-Build Procurement Suitability**
- Specifications shall be suitable for design-build procurement, allowing contractors to propose equipment that meets performance requirements from multiple manufacturers.
- **Source**: Project delivery model (Design & Build contract — Decomposition Section 1).
- **ASSUMPTION**: Performance-based specifications preferred over prescriptive (brand-specific) specifications to encourage competition and value engineering.
- **Rationale**: See Guidance.md — Principle 2 (Performance-Based vs. Prescriptive Specifications).
- **Procedure**: See Procedure.md — Step 2 (Select Specification Template and Organization).

**FR-3: Code and Standards Compliance**
- All equipment specifications shall reference and require compliance with applicable Canadian codes and international standards.
- **Source**: OBJ-6 (Regulatory Compliance — Decomposition Section 2); CEC, CSA, IEEE standards.
- Mandatory standards: CSA C22.1 (CEC), CSA equipment standards (C88, C802, C22.2 series), IEEE standards (C37, C57, 80, 693).
- **Rationale**: See Guidance.md — Principle 3 (Standards-Based Equipment Requirements).
- **Procedure**: See Procedure.md — Step 3 (Draft General Requirements Section), Step 4b (Define Materials and Construction Requirements).

**FR-4: Environmental and Seismic Requirements**
- Specifications shall address environmental conditions (coastal BC climate, corrosion protection) and seismic qualification requirements.
- **Source**: Project location (Fraser Surrey Terminal — marine/industrial environment); BC high seismic zone.
- **ASSUMPTION**: NEMA 3R or 4X enclosures for outdoor equipment; IEEE 693 seismic qualification or CSA C22.3 No. 7 anchorage requirements.
- **Rationale**: See Guidance.md — Principle 4 (Environmental and Application-Specific Requirements), Consideration 9 (Seismic Qualification).
- **Procedure**: See Procedure.md — Step 4b (Apply project-specific requirements).

**FR-5: Submittal and Quality Requirements**
- Specifications shall define submittal requirements (shop drawings, product data, test reports, certifications) and quality assurance/quality control (QA/QC) procedures.
- **Source**: Project quality management plan (standard design-build practice).
- Submittals required: Equipment data sheets (pre-purchase), shop drawings, factory acceptance test (FAT) reports, installation test records.
- **Rationale**: See Guidance.md — Principle 5 (Submittal and Quality Assurance Requirements).
- **Procedure**: See Procedure.md — Step 3 (Draft General Requirements Section — Submittals and QA), Step 4c (Define Testing and Documentation Requirements).

### Specification Requirements by Equipment Category

#### SR-1: Transformer Specification Requirements

**Performance Requirements**:
- **Ratings**: kVA rating, voltage ratio (primary/secondary), impedance, temperature rise, efficiency — **TBD** (based on load analysis — DEL-17.03).
- **Voltage Regulation**: ±5% taps (4 x 2.5% above and below nominal, de-energized tap changer).
- **Efficiency**: TP-1 or better per NRCan Energy Efficiency Regulations (minimize lifecycle energy losses per OBJ-9).
- **Temperature Rise**: Liquid-filled 65°C rise; Dry-type 150°C or 115°C insulation class (per CSA C88/C802).
- **Sound Level**: **TBD** — Maximum sound power level for indoor and outdoor installations (typical: 55-65 dBA for liquid-filled, 60-70 dBA for dry-type).
- **Seismic Qualification**: IEEE 693 High Performance Level or equivalent seismic anchorage per CSA C22.3 No. 7.

**Material and Construction Requirements**:
- **Standards**: CSA C88 (liquid-filled), CSA C802 (dry-type), IEEE C57 series.
- **Windings**: Copper conductors (aluminum permitted for large units but copper preferred for reliability and connections).
- **Insulation**: Liquid-filled (mineral oil or less-flammable fluid); Dry-type (cast resin or VPI).
- **Core**: Grain-oriented silicon steel, core form or shell form construction.
- **Bushings**: MV bushings (liquid-filled outdoor units); LV bushings or cable termination compartments.
- **Accessories (Liquid-Filled)**: Liquid level gauge, winding temperature indicator (WTI), liquid temperature indicator (LTI), pressure relief device, drain/sampling valve, ground pads.
- **Enclosure**: Outdoor NEMA 3R (liquid-filled); Indoor NEMA 1 or outdoor NEMA 3R (dry-type).

**Testing and Documentation**:
- **Factory Tests**: Routine tests per CSA C88/C802 (resistance, polarity, voltage ratio, no-load loss, impedance, applied voltage/induced voltage tests).
- **Optional Tests** (if specified): Temperature rise test, sound level test, short circuit withstand test.
- **Submittals**: Certified test reports, nameplate data, installation/operation manuals, outline/dimensional drawings.

#### SR-2: Switchgear Specification Requirements

**MV Switchgear**:

**Performance Requirements**:
- **Voltage Class**: 25 kV or 15 kV class (to match utility service) — **TBD**.
- **Continuous Current Rating**: 1200A, 2000A, or 3000A bus rating — **TBD** (based on load analysis).
- **Interrupting Capacity**: **TBD** — Based on utility fault current (DEL-17.03 short circuit analysis); typical: 25-40 kA (25 kV), 40-63 kA (15 kV).
- **Arc-Resistant Construction**: Type 2B per IEEE C37.20.7 (personnel access to front, rear, top during arcing event) — **ASSUMPTION** (enhances safety per OBJ-1).
- **Circuit Breaker Type**: Vacuum circuit breakers (VCBs) with stored energy operators, electrically operated, drawout type.
- **Mechanical Endurance**: 10,000 operations minimum.
- **Electrical Endurance**: Per IEEE C37.04 and C37.09.

**Material and Construction Requirements**:
- **Standards**: CSA C22.2 No. 31 (metal-clad switchgear), IEEE C37.20.7 (arc-resistant), IEEE C37.04 (ratings), IEEE C37.09 (test procedures).
- **Construction**: Compartmentalized metal-clad design with separate compartments for circuit breakers, bus, cable, and control/instrumentation.
- **Bus Material**: Copper or tin-plated copper (silver plating not recommended for marine environment).
- **Interlocks**: Mechanical and electrical interlocks (breaker/disconnect coordination, grounding switch interlocks, door interlocks).
- **Protection Relays**: Microprocessor-based protective relays (IEEE C37.90, IEC 60255) with ANSI device function numbers; communication capability (Modbus TCP, DNP3, or IEC 61850) — **TBD** (per control system requirements).
- **Instrumentation**: Digital multifunction meters (V, A, kW, kVAR, kWh, PF, THD) with local display and communication.
- **Control Power**: 125 VDC (station battery) or 120 VAC (UPS) — **TBD**.
- **Enclosure**: Indoor NEMA 1 or outdoor NEMA 3R/4X (stainless steel or coated steel for marine environment).

**LV Switchgear**:

**Performance Requirements**:
- **Voltage Rating**: 600V or 480V nominal — **TBD**.
- **Continuous Current Rating**: 1600A, 2500A, or 4000A bus rating — **TBD**.
- **Short Circuit Current Rating (SCCR)**: **TBD** — Based on fault current analysis (typical: 65 kA or 100 kA RMS symmetrical).
- **Circuit Breaker Type**: Insulated-case (ICCB) or molded-case (MCCB) circuit breakers, or low-voltage power circuit breakers (LVPCB), drawout or bolt-on.
- **Trip Units**: Electronic programmable trip units with LSIG (long-time, short-time, instantaneous, ground fault) protection.

**Material and Construction Requirements**:
- **Standards**: CSA C22.2 No. 31, UL 1558, NEMA PB 2.
- **Bus Material**: Tin-plated copper.
- **Instrumentation**: Digital metering per feeder (V, A, kW, kVAR, kWh, PF).
- **Control Power**: 120 VAC from CPT or external source.
- **Enclosure**: Indoor NEMA 1 or outdoor NEMA 3R/4X.

**Testing and Documentation** (MV and LV Switchgear):
- **Factory Tests**: High-potential (dielectric) test, primary current injection test, protective relay functional test, control circuit functional test, mechanical operation test, insulation resistance test.
- **Submittals**: One-line diagrams, three-line diagrams, control schematics, shop drawings (front/plan/section views), relay settings documentation, certified test reports, installation/operation/maintenance manuals.

#### SR-3: MCC (Motor Control Center) Specification Requirements

**Performance Requirements**:
- **Voltage Rating**: 600V or 480V class — **TBD**.
- **Horizontal Bus Rating**: 600A, 800A, or 1600A continuous — **TBD** (based on motor loads).
- **SCCR**: **TBD** — Based on fault current (typical: 65 kA or 100 kA).
- **Starter Types**: Combination starters (FVNR — full voltage non-reversing) with contactors (IEC or NEMA), overload relays (electronic or thermal-magnetic), disconnect switches.
- **VFDs / Soft Starters**: **TBD** — Variable frequency drives or soft starters for selected large pumps (reduces inrush, provides speed control, improves energy efficiency per OBJ-9).

**Material and Construction Requirements**:
- **Standards**: CSA C22.2 No. 254, UL 845, NEMA ICS 18.
- **Construction**: Modular ("bucket") design with withdrawable units, plug-in or bolt-on bus connections.
- **Bus Material**: Tin-plated copper (horizontal and vertical bus).
- **Control Power**: 120 VAC control from CPT (in MCC) or external source.
- **Pilot Devices**: NEMA 4 or 4X start/stop pushbuttons (red/green), selector switches (hand-off-auto), LED indicating lights.
- **Wiring**: Factory-wired with color-coded conductors per NEMA standards; terminal blocks for field connections; adequate wire management (cable troughs, wire ducts).
- **Enclosure**: Indoor NEMA 1 or outdoor NEMA 3R/4X; space heaters (thermostatically controlled, anti-condensation) for outdoor installations in coastal climate.
- **Seismic Qualification**: IEEE 693 or anchorage per CSA C22.3 No. 7.

**Testing and Documentation**:
- **Factory Tests**: High-potential test, control circuit functional test, mechanical operation test, insulation resistance test.
- **Submittals**: MCC one-line diagram, bucket schedule (starter sizes, breaker ratings, motor data), control schematics, shop drawings, certified test reports, installation/operation/maintenance manuals.

#### SR-4: Cable Specification Requirements

**MV Power Cables**:

**Performance Requirements**:
- **Voltage Class**: 25 kV or 15 kV (133% or 173% insulation level per CSA C68.3) — **TBD**.
- **Ampacity**: Per CSA C68.3 or manufacturer data (function of conductor size, installation method, ambient, soil thermal resistivity).
- **Installation Method**: Direct burial or duct bank (underground) per CEC Section 12.
- **Bend Radius**: Minimum bend radius per manufacturer recommendations (typically 12-15 times cable OD for single-conductor MV cables).

**Material and Construction Requirements**:
- **Standards**: CSA C68.3, ICEA S-93-639 (AEIC CS8).
- **Conductor**: Copper, stranded Class B per CSA C68.3 (aluminum permitted for very large feeders >500 kcmil, but copper preferred).
- **Conductor Sizes**: **TBD** — Based on cable schedules (DEL-17.01) and ampacity calculations (DEL-17.03); typical range: 1/0 AWG to 4/0 AWG or 250 kcmil.
- **Insulation**: EPR (ethylene propylene rubber) or XLPE (cross-linked polyethylene), rated 90°C or 105°C.
- **Shielding**: Semiconducting insulation shield (inner and outer), metallic shield (copper tape or concentric neutral wires).
- **Jacket**: PVC, PE, or CPE (chlorinated polyethylene), rated for direct burial or duct installation, UV-resistant (if exposed), moisture-resistant.
- **Color**: Black jacket (standard) with color-coded phase identification bands or tags at terminations.

**Testing and Documentation**:
- **Factory Tests**: AC high-potential (Hi-Pot) test, DC leakage test, partial discharge test (for cables > 100 m length or > 15 kV class).
- **Submittals**: Cable data sheets (conductor size, insulation type, jacket type, ampacity tables), test reports, installation instructions, termination instructions.

**LV Power Cables**:

**Performance Requirements**:
- **Voltage Rating**: 600V (or 1000V for export compliance).
- **Ampacity**: Per CEC Table 1, 2, 3, 4 (function of conductor size, insulation type, ambient, installation method, number of conductors).
- **Installation Method**: Cable tray, conduit, or direct burial per CEC Section 12.

**Material and Construction Requirements**:
- **Standards**: CSA C22.2 No. 38, CEC Section 4 and Section 12.
- **Conductor**: Copper, stranded Class B per CSA C22.2 No. 38 (flexibility for installation).
- **Conductor Sizes**: **TBD** — Based on cable schedules (DEL-17.01) and ampacity/voltage drop calculations (DEL-17.03); typical range: 14 AWG to 500 kcmil.
- **Insulation**: RW90 XLPE (90°C dry and wet rating, standard Canadian LV cable insulation).
- **Configuration**: 2-conductor, 3-conductor, or 4-conductor (with neutral); plus separate grounding conductor (per CEC Section 10).
- **Jacket**: PVC (standard) or LSZH (low smoke zero halogen) for indoor installations where fire/smoke is a concern — **TBD** (per fire protection requirements).
- **Color Coding**: Per CEC Section 4 (grounded conductor: white or grey; grounding conductor: green or bare; ungrounded conductors: other colors, typically red/black/blue for phases).

**Testing and Documentation**:
- **Factory Tests**: Insulation resistance test (optional for LV cables), continuity test.
- **Submittals**: Cable data sheets (conductor size, insulation type, ampacity tables, voltage drop data), installation instructions.

**Control Cables**:
- **Voltage Rating**: 600V.
- **Standards**: CSA C22.2 No. 38, UL 1277.
- **Construction**: Twisted pairs or triads (for noise immunity), overall foil or braid shield with drain wire (for analog/instrumentation signals).
- **Insulation**: PVC or PE, color-coded per application.
- **Jacket**: PVC or LSZH.
- **Submittals**: Cable data sheets, installation instructions.

#### SR-5: Accessories and Ancillary Equipment Requirements

**Cable Terminations**:
- **MV Terminations**: Heat-shrink or cold-shrink stress-relief termination kits per cable and equipment manufacturer recommendations; indoor and outdoor types (weatherproof seals for outdoor).
- **LV Terminations**: UL-listed compression or mechanical lugs (copper or tin-plated copper); terminal blocks (DIN rail or screw type) for control circuits.

**Cable Supports**:
- **Cable Tray**: Ladder tray or ventilated trough; material: galvanized steel (standard), aluminum (lightweight), or FRP (corrosive areas); load rating per cable weight and fill; per CEC Section 12 and NEMA VE 1.
- **Conduit**: Rigid steel conduit (RSC), IMC, EMT, or rigid PVC per CEC Section 12 and application (underground, outdoor, indoor, hazardous areas).

**Grounding Materials**:
- **Ground Grid Conductors**: Bare copper, 2/0 AWG or 4/0 AWG per IEEE Std 80 and grounding calculations (DEL-17.03).
- **Ground Rods**: Copper-clad steel, 16 mm diameter × 3 m length per CEC Section 10.
- **Grounding Connectors**: Exothermic weld (Cadweld or equivalent) for permanent connections (grid-to-grid, grid-to-equipment); or bolted bronze/copper connectors with anti-oxidant compound.

**Labels and Nameplates**:
- **Equipment Nameplates**: Engraved laminated phenolic or stainless steel, per project equipment tagging system — **TBD** (tag number format and database).
- **Cable Labels**: Permanent, UV-resistant, wrap-around or tie-on tags at all terminations, pull boxes, and intermediate access points; circuit number and source/destination identification.
- **Arc Flash Labels**: Per CSA Z462 — incident energy level (cal/cm²), PPE category, arc flash boundary distance, limited approach boundary distance, shock hazard voltage — **TBD** (based on arc flash study — see DEL-17.03 or separate study).

### Quality Requirements

**QR-1: Submittal Requirements**
- **Shop Drawings**: Equipment layout, one-line diagrams, control schematics, dimensional drawings, cable connection diagrams.
- **Product Data**: Manufacturer catalogs, data sheets, specifications, performance curves (transformer losses, breaker time-current curves, etc.).
- **Test Reports**: Factory acceptance test (FAT) reports for all major equipment (transformers, switchgear, MCCs).
- **Certifications**: CSA/UL certification marks, seismic qualification certificates (IEEE 693), mill test reports (cables).
- **Manuals**: Installation, operation, and maintenance (IOM) manuals for all equipment.

**QR-2: Equipment Certification**
- All electrical equipment shall be certified to applicable CSA or UL standards and bear certification marks.
- **Source**: CEC Section 2 (equipment approval); BC Safety Authority requirements.
- Equipment not bearing CSA/UL marks may be accepted if certified by an accredited certification body (e.g., ETL, Intertek) — subject to approval.

**QR-3: Factory Acceptance Testing (FAT)**
- Major equipment (transformers, switchgear, MCCs) shall undergo FAT at manufacturer's facility prior to shipment.
- Contractor or Owner representative may witness FAT — **TBD** (witness requirements per contract).
- FAT procedures per applicable standards (CSA, IEEE) and manufacturer's standard test procedures.

**QR-4: Quality Assurance During Manufacture**
- Manufacturer shall have ISO 9001 certified quality management system — **ASSUMPTION** (standard requirement for major electrical equipment).
- Manufacturer shall provide quality documentation (inspection and test plans, non-conformance reports, corrective actions).

## Standards

**Primary Codes and Standards** (Canadian jurisdiction):

| Standard | Title | Application |
|----------|-------|-------------|
| **CSA C22.1** | Canadian Electrical Code, Part I (CEC) | Mandatory — overall electrical compliance |
| **CSA C88** | Power Transformers and Reactors | Liquid-filled transformer specifications |
| **CSA C802** | Dry-Type Distribution Transformers | Dry-type transformer specifications |
| **CSA C68.3** | Cable — 5 kV to 46 kV | MV power cable specifications |
| **CSA C22.2 No. 31** | Switchgear Assemblies | MV and LV switchgear specifications |
| **CSA C22.2 No. 38** | Cable — 1000V and Under | LV power cable specifications |
| **CSA C22.2 No. 254** | Motor Control Centers | MCC specifications |
| **CSA C22.3 No. 7** | Underground Systems, Seismic | Seismic anchorage and underground installations |

**IEEE Standards** (reference and specification):

| Standard | Title | Application |
|----------|-------|-------------|
| **IEEE C37 series** | Switchgear, Circuit Breakers, Relays | Switchgear ratings, testing, arc-resistant construction |
| **IEEE C57 series** | Transformers | Transformer design, testing, loading |
| **IEEE 693** | Seismic Qualification | Equipment seismic qualification testing |
| **IEEE Std 80** | Grounding Grid Design | Grounding system design (referenced by cable grounding spec) |

**Other Standards**:

| Standard | Title | Application |
|----------|-------|-------------|
| **UL 1558** | Switchboards | LV switchboard (alternative to CSA) |
| **UL 845** | Motor Control Centers | MCC (alternative to CSA) |
| **NEMA Standards** | Various (PB 2, ICS 18, VE 1) | Switchboard, MCC, cable tray specifications |
| **NRCan Energy Efficiency** | Transformer Efficiency | TP-1 or better efficiency requirements |
| **ISO 9001** | Quality Management System | Manufacturer QA/QC certification |
| **ISO 12944** | Corrosion Protection | Outdoor equipment corrosion protection (marine environment) |

**Regulatory Authority**:
- **BC Safety Standards Act** and **BC Electrical Safety Regulation**
- **BC Safety Authority** — electrical permit and inspection authority

**Additional Standards**:
- **TBD**: Employer's Requirements (project-specific equipment standards) — **location TBD** (Volume 2 Parts 1-3)

## Verification

**Verification Methods**:

| Verification Activity | Method | Acceptance Criteria | Responsibility |
|-----------------------|--------|---------------------|----------------|
| **Technical Review** | Review specifications against applicable codes, standards, and design calculations | All requirements traceable to codes/standards or design basis; no conflicts or omissions | Specification author + independent reviewer (P.Eng.) |
| **Interdisciplinary Review** | Review by affected disciplines for coordination and interface requirements | No unresolved interface issues (coordination with piping, civil, instrumentation) | Discipline leads |
| **Design Calculation Cross-Check** | Verify equipment ratings and sizes match approved calculations (DEL-17.03) | Consistency between specifications and load analysis, short circuit, voltage drop, coordination studies | Electrical engineer + checker |
| **Drawing Consistency Check** | Verify equipment specifications match equipment shown on drawings (DEL-17.01) | Equipment types, ratings, and configurations consistent between specs and drawings | Specification author + drawing checker |
| **Employer Review** | Submit specifications to Employer for review and comment | Employer comments addressed or resolved; Employer approval obtained (if required per contract) | D&B Contractor project manager |
| **Compliance Matrix** | Verify specifications address all ER requirements (if checklist provided) | All ER requirements addressed; compliance documented | Specification author + quality manager |

**Acceptance Criteria**:
- All verification activities completed and signed off
- No outstanding technical comments or design issues
- Specifications approved by discipline lead (P.Eng.)
- Employer review comments resolved (if applicable)
- **TBD**: Specific approval protocol per project quality procedures

## Documentation

**Required Documentation Outputs** (Source: _CONTEXT.md anticipated artifacts):

1. **Transformer Specification**: Performance, material, construction, testing, and documentation requirements for liquid-filled and dry-type transformers
2. **Switchgear Specification**: Performance, material, construction, testing, and documentation requirements for MV and LV switchgear
3. **MCC Specification**: Performance, material, construction, testing, and documentation requirements for motor control centers
4. **Cable Specification**: Performance, material, construction, testing, and documentation requirements for MV, LV, and control cables

**Documentation Format**:
- **ASSUMPTION**: Written technical specification organized by CSI MasterFormat Division 26 (Electrical) sections
- Format: **TBD** — Microsoft Word or PDF, per project document control standards
- Sections: General (scope, references, submittals, QA), Equipment-Specific Sections (transformers, switchgear, MCCs, cables), Execution (installation, testing, commissioning)

**Documentation Requirements**:
- All specifications shall comply with project document control procedures
- Revision control per project numbering system — **TBD**
- Electronic files managed in project document management system — **TBD** (system name/location)
- Hard copy issuance: **TBD** (number of copies for construction)

**Deliverable Maturity Stages** (typical design-build):
- **30% Design**: Preliminary equipment types and performance criteria
- **60% Design**: Detailed equipment specifications for procurement
- **90% Design / IFC**: Final specifications for construction and equipment purchase
- **As-Built**: Specifications updated to reflect actual equipment procured and installed

**Cross-References**:
- **Datasheet.md**: Equipment categories, environmental conditions, and material requirements
- **Guidance.md**: Engineering rationale for specification requirements, equipment selection criteria, and trade-off analysis
- **Procedure.md**: Step-by-step process for developing, reviewing, and approving specifications
- **DEL-17.01** (Electrical Power Design Drawing Set): Equipment shown on drawings shall match specifications
- **DEL-17.03** (Electrical Power Design Calculations): Equipment ratings shall be supported by calculations
- **DEL-17.04** (Electrical Power Data Sheet Package): Manufacturer data sheets shall demonstrate compliance with specifications
- **DEL-17.05** (Electrical Power Installation & Test Records): Installation and testing shall be per specifications

---
**Cross-Document Alignment Verified (Pass 3):** All functional requirements (FR-1 through FR-5), specification requirements (SR-1 through SR-5), and quality requirements (QR-1 through QR-4) are traceable to Datasheet.md equipment categories, Guidance.md principles/considerations, and Procedure.md steps. No conflicts identified.
