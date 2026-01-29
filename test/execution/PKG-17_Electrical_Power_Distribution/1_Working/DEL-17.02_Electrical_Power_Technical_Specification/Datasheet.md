# Datasheet: DEL-17.02 Electrical Power Technical Specification

## Identification

| Field | Value |
|-------|-------|
| Deliverable ID | DEL-17.02 |
| Name | Electrical Power Technical Specification |
| Package | PKG-17 Electrical Power Distribution |
| Discipline | Electrical |
| Type | Specification |
| Responsible | D&B Contractor |
| Status | INITIALIZED |

## Attributes

| Attribute | Value |
|-----------|-------|
| Document Number | **TBD** — To be assigned per project document numbering system |
| Specification Type | Technical Specification (equipment performance, materials, workmanship) |
| Revision | 0 (Initial issue) |
| Format | Written specification document (text-based, organized by equipment category) |
| Classification | For Construction |
| Specification Sections | Transformer, Switchgear, MCC, Cable (Source: _CONTEXT.md anticipated artifacts) |

### Specification Structure

**ASSUMPTION**: Technical specification organized by equipment/material category:

| Section | Content | Specification Reference | Guidance Reference | Procedure Step |
|---------|---------|------------------------|-------------------|----------------|
| **Section 1: General** | Scope, references, definitions, submittals, quality assurance | Specification.md — General Requirements | Principle 5 (Guidance.md) | Step 3 (Procedure.md) |
| **Section 2: Transformer Specification** | Performance, construction, materials, testing, documentation for transformers | Specification.md — SR-1 | Consideration 3 (Guidance.md) | Step 4a (Procedure.md) |
| **Section 3: Switchgear Specification** | Performance, construction, materials, testing, documentation for switchgear | Specification.md — SR-2 | Consideration 2 (Guidance.md) | Step 4a (Procedure.md) |
| **Section 4: MCC Specification** | Performance, construction, materials, testing, documentation for motor control centers | Specification.md — SR-3 | Consideration 4 (Guidance.md) | Step 4a (Procedure.md) |
| **Section 5: Cable Specification** | Performance, construction, materials, testing, documentation for power cables | Specification.md — SR-4 | Consideration 5 (Guidance.md) | Step 4a (Procedure.md) |
| **Section 6: Accessories** | Cable terminations, supports, grounding materials, labels | Specification.md — SR-5 | Consideration 6 (Guidance.md) | Step 4a (Procedure.md) |

**Source**: _CONTEXT.md (anticipated artifacts); typical electrical specification organization per CSI MasterFormat Division 26.

### Equipment Categories and Typical Quantities

**ASSUMPTION** — based on facility scope (1,000,000 MT/a transload facility with 32 railcar positions, 3 storage tanks, marine loading):

| Equipment Category | Typical Quantity | Voltage/Rating Range | Purpose |
|--------------------|------------------|----------------------|---------|
| **Unit Substations (Liquid-Filled Transformers with Switchgear)** | 2-3 units | 1000-1500 kVA, MV/600V | Main distribution for pumps, process loads |
| **Dry-Type Transformers** | 2-4 units | 150-500 kVA, 600V/208V-120V or 480V/208V-120V | Lighting, receptacles, small loads |
| **MV Switchgear** | 1 lineup (4-8 breaker positions) | 25 kV or 15 kV class, 1200-2000A bus | Utility service, transformer feeders |
| **LV Switchgear** | 2-3 lineups | 600V or 480V, 1600-4000A bus | Secondary distribution from transformers |
| **Motor Control Centers (MCCs)** | 4-8 lineups | 600V or 480V, 600-1600A bus | Motor starters for pumps, heating circulation |
| **MV Power Cables** | 500-1000 m total | 25 kV or 15 kV class, 1/C 1/0 to 4/0 AWG | MV feeders to transformers |
| **LV Power Cables** | 5000-15000 m total | 600V class, 3/C or 4/C, 14 AWG to 500 kcmil | LV feeders, branch circuits, motor connections |

**Note**: Quantities are ASSUMPTION pending detailed load analysis (DEL-17.03) and design drawings (DEL-17.01).

## Conditions

**Operating / Environmental Context:**

This technical specification defines performance, materials, and workmanship requirements for electrical power distribution equipment per Employer's Requirements.

**Project Context** (Source: Decomposition Section 1):
- **Location**: Fraser Surrey Terminal, 11060 Elevator Road, Surrey, BC
- **Facility Type**: Canola oil transload (rail-to-storage-to-ship)
- **Throughput**: 1,000,000 MT per annum (permitted capacity — OBJ-2)
- **Key Loads**: Railcar unloading (32 positions), transfer pumps, marine loading, storage tank heating, control/instrumentation

**Environmental Conditions** (applicable to all electrical equipment):
- **Climate Zone**: **ASSUMPTION**: CSA Climate Zone 2 (coastal British Columbia) — outdoor equipment rated for -20°C to +40°C ambient
- **Indoor vs. Outdoor**: **TBD** — Equipment locations (indoor electrical rooms vs. outdoor substations) affects enclosure ratings (NEMA 1 vs. NEMA 3R/4X)
- **Hazardous Area Classification**: **TBD** — Some equipment may be in Class I Division 2 or Zone 2 areas (to be confirmed by hazardous area classification study per CEC Section 18)
- **Seismic Requirements**: **ASSUMPTION**: High seismic zone (coastal BC) — equipment anchorage per CSA C22.3 No. 7 and IEEE 693 seismic qualification
- **Corrosion Environment**: **ASSUMPTION**: Marine/industrial atmosphere — outdoor equipment with enhanced corrosion protection (NEMA 4X stainless steel or coated enclosures per ISO 12944 C4 or C5)

**Performance Context**:
- **Service Continuity** (OBJ-1): Equipment shall support continuous industrial duty (24/7 operation) with high reliability
- **Design Life**: **TBD** — **ASSUMPTION**: 25+ years minimum per facility operational life expectancy
- **Maintenance Philosophy**: Industrial-grade equipment with reasonable maintenance intervals to minimize unplanned downtime (OBJ-9 — Lifecycle Cost Optimization)
- **Safety**: Equipment shall support safe installation, operation, and maintenance per CSA Z462 and NFPA 70E electrical safety requirements

## Construction

**Materials / Configuration:**

Anticipated specification artifacts (Source: _CONTEXT.md and Decomposition DEL-17.02 entry):

### 1. Transformer Specification (Section 2)

**Equipment Types and Applications**:
- **Liquid-Filled Unit Substations**: MV/LV transformers (typically 1000-1500 kVA) with integrated MV and LV switchgear for main distribution
- **Dry-Type Transformers**: LV/LV transformers (150-500 kVA) for lighting and small power (480V or 600V primary, 208V-120V secondary)

**Key Material and Construction Requirements** (ASSUMPTION — typical industrial specifications):
- **Standards**: CSA C88 (liquid-filled), CSA C802 (dry-type), IEEE C57 series
- **Insulation System**: Liquid-filled (mineral oil or less-flammable fluid); Dry-type (cast resin or VPI — vacuum pressure impregnated)
- **Windings**: Copper conductors (aluminum permitted for large transformers but copper preferred for reliability)
- **Voltage Regulation**: ±5% taps (4 x 2.5% taps above and below nominal) — de-energized tap changer
- **Impedance**: **TBD** — Selected based on short circuit coordination (typical: 5.5-6.5% for unit substations)
- **Temperature Rise**: Liquid-filled 65°C rise (55°C or 65°C per CSA C88); Dry-type 150°C or 115°C insulation class rise
- **Efficiency**: High-efficiency (TP-1 or better per NRCan regulations to minimize energy losses)
- **Sound Level**: **TBD** — Limits for indoor vs. outdoor locations (typical: 55-65 dBA at 1 m for liquid-filled; 60-70 dBA for dry-type)
- **Bushings**: MV bushings (liquid-filled outdoor units), LV bushings or cable entry
- **Accessories**: Liquid level gauge, temperature gauge (winding and oil), pressure relief device, drain valve, ground pads (liquid-filled units)
- **Seismic Qualification**: IEEE 693 High Performance Level or equivalent
- **Enclosure**: Outdoor NEMA 3R (liquid-filled), NEMA 1 (dry-type indoor), or NEMA 3R (dry-type outdoor)

### 2. Switchgear Specification (Section 3)

**Equipment Types**:
- **MV Switchgear**: Metal-clad, arc-resistant construction for utility service and transformer feeders
- **LV Switchgear**: Metal-enclosed power switchgear for secondary distribution

**Key Material and Construction Requirements**:

**MV Switchgear** (ASSUMPTION):
- **Voltage Class**: 25 kV or 15 kV (to match utility service) — **TBD**
- **Bus Rating**: 1200A, 2000A, or 3000A continuous current rating — **TBD**
- **Interrupting Capacity**: **TBD** — Based on utility fault current (typical: 25-40 kA symmetrical for 25 kV; 40-63 kA for 15 kV)
- **Standards**: CSA C22.2 No. 31 (metal-clad switchgear), IEEE C37.20.7 (arc-resistant), IEEE C37.04 (ratings)
- **Arc-Resistant Type**: Type 2B (personnel access to front, rear, top during arcing event) — **ASSUMPTION** for enhanced safety
- **Circuit Breakers**: Vacuum circuit breakers (VCBs) with stored energy (spring-charged) operators, electrically operated, drawout type
- **Interrupting Medium**: Vacuum interrupters (maintenance-free, long life)
- **Mechanical Endurance**: 10,000 operations minimum
- **Electrical Endurance**: Per IEEE C37.04 and C37.09
- **Protection Relays**: Microprocessor-based (digital) relays per IEEE C37.90 and IEC 60255; communication capability (Modbus TCP, DNP3, or IEC 61850)
- **Instrumentation**: Digital multifunction meters (V, A, kW, kVAR, kWh, PF, THD) with display and communication
- **Control Power**: 125 VDC (station battery) or 120 VAC (UPS supply) — **TBD**
- **Interlocks**: Mechanical and electrical interlocks to prevent unsafe operations (breaker/disconnect coordination, grounding switch interlocks)
- **Bus Material**: Copper or tin-plated copper (silver plating not recommended for corrosive environments)
- **Enclosure**: Indoor NEMA 1 (steel, painted) or outdoor NEMA 3R/4X (stainless steel or coated steel)

**LV Switchgear** (ASSUMPTION):
- **Voltage Rating**: 600V or 480V nominal — **TBD**
- **Bus Rating**: 1600A, 2500A, or 4000A continuous — **TBD**
- **Short Circuit Current Rating (SCCR)**: **TBD** — Based on fault current analysis (typical: 65 kA or 100 kA RMS symmetrical)
- **Standards**: CSA C22.2 No. 31, UL 1558, NEMA PB 2
- **Circuit Breakers**: Insulated-case circuit breakers (ICCBs) or low-voltage power circuit breakers (LVPCBs), drawout type
- **Trip Units**: Electronic (programmable) trip units with LSIG (long-time, short-time, instantaneous, ground fault) protection
- **Instrumentation**: Digital metering per feeder or main bus
- **Control Power**: 120 VAC derived from CPT (control power transformer) or external source
- **Bus Material**: Tin-plated copper
- **Enclosure**: Indoor NEMA 1 or outdoor NEMA 3R/4X

### 3. MCC (Motor Control Center) Specification (Section 4)

**Equipment Type**: Low voltage motor control centers with combination motor starters

**Key Material and Construction Requirements** (ASSUMPTION):
- **Voltage Rating**: 600V or 480V class — **TBD**
- **Bus Rating**: Horizontal bus 600A, 800A, 1600A continuous — **TBD**
- **SCCR**: **TBD** — Based on fault current (typical: 65 kA or 100 kA)
- **Standards**: CSA C22.2 No. 254, UL 845, NEMA ICS 18
- **Construction**: Modular ("bucket") design with withdrawable units, plug-in or bolt-on bus connections
- **Starter Types**: Combination starters (FVNR — full voltage non-reversing) with IEC or NEMA contactors, overload relays (thermal-magnetic or electronic), disconnect switch
- **VFDs / Soft Starters**: **TBD** — Variable frequency drives or reduced-voltage soft starters for selected large motors (pump applications)
- **Protection**: Motor circuit protectors (MCPs) or molded-case circuit breakers (MCCBs); overload relays
- **Control Power**: 120 VAC control, derived from control power transformer in MCC or fed from external source
- **Pilot Devices**: Start/stop pushbuttons (NEMA 4X, 4, or 13), selector switches (hand-off-auto), indicating lights (LED)
- **Instrumentation**: **TBD** — Motor-level metering or MCC-level energy monitoring
- **Communication**: **TBD** — Ethernet or serial communication for SCADA/DCS integration (if VFDs or smart starters)
- **Enclosure**: Indoor NEMA 1 (steel, painted) or outdoor NEMA 3R or 4X (stainless steel or coated steel) with space heaters (anti-condensation) for outdoor units
- **Bus Material**: Tin-plated copper
- **Wiring**: Color-coded per NEMA standards, with terminal blocks and adequate wire management

### 4. Cable Specification (Section 5)

**Cable Types and Applications**:
- **MV Power Cables**: 25 kV or 15 kV class, single conductor, for MV switchgear to transformer primary connections
- **LV Power Cables**: 600V class, multi-conductor (3/C or 4/C plus ground), for LV distribution feeders, branch circuits, motor connections
- **Control Cables**: 600V instrumentation and control cables for motor control, instrumentation (may be separate spec or included)

**Key Material and Construction Requirements**:

**MV Cables** (ASSUMPTION):
- **Voltage Class**: 25 kV or 15 kV (133% or 173% insulation level per CSA C68.3) — **TBD**
- **Conductor**: Copper, stranded Class B per CSA C68.3 (aluminum permitted for very large feeders but copper preferred)
- **Insulation**: EPR (ethylene propylene rubber) or XLPE (cross-linked polyethylene), rated 90°C or 105°C
- **Shielding**: Semiconducting insulation shield and metallic shield (copper tape or concentric neutral wires)
- **Jacket**: PVC, PE, or CPE (chlorinated polyethylene), rated for direct burial or duct installation
- **Standards**: CSA C68.3, ICEA S-93-639 (AEIC CS8)
- **Ampacity**: Per CSA C68.3 tables or manufacturer data (function of conductor size, installation method, ambient, soil thermal resistivity)
- **Testing**: Factory acceptance test (FAT) including AC high-potential test (Hi-Pot), DC leakage test, partial discharge test (for cables > 100 m or > 15 kV)

**LV Power Cables** (ASSUMPTION):
- **Voltage Rating**: 600V (or 1000V for export compliance)
- **Conductor**: Copper, stranded Class B per CSA C22.2 No. 38 (flexible for installation)
- **Insulation**: RW90 XLPE (90°C dry and wet rating, standard Canadian LV cable)
- **Configuration**: 2-conductor, 3-conductor, or 4-conductor (with neutral); plus separate ground conductor (green or bare per CEC Section 10)
- **Jacket**: PVC (standard) or LSZH (low smoke zero halogen) for indoor installations where fire/smoke is a concern — **TBD**
- **Standards**: CSA C22.2 No. 38, CEC Section 4 (conductors) and Section 12 (wiring methods)
- **Ampacity**: Per CEC Table 1, 2, 3, 4 (function of conductor size, insulation type, ambient, installation method, number of conductors in conduit/tray)
- **Color Coding**: Per CEC Section 4 (Phase A: red, black, or brown; Phase B: black, white, or orange; Phase C: blue, red, or yellow; Neutral: white or grey; Ground: green or bare)

**Control Cables** (ASSUMPTION):
- **Voltage Rating**: 600V
- **Conductor**: Copper, stranded, 16 AWG or 14 AWG typical
- **Configuration**: Individual conductors, twisted pairs, or triads (for noise immunity)
- **Shielding**: Overall foil or braid shield with drain wire for analog/instrumentation signals
- **Insulation**: PVC or PE, color-coded
- **Jacket**: PVC or LSZH
- **Standards**: CSA C22.2 No. 38, UL 1277

### 5. Accessories and Ancillary Equipment (Section 6)

**Cable Terminations**:
- **MV Terminations**: Heat-shrink or cold-shrink stress-relief termination kits per cable manufacturer recommendations (indoor and outdoor types)
- **LV Terminations**: Compression lugs (UL listed, copper or tin-plated copper), mechanical lugs (where compression not feasible), terminal blocks (DIN rail or screw type)

**Cable Supports**:
- **Cable Tray**: Ladder tray or ventilated trough, galvanized steel (standard) or aluminum (lightweight) or FRP (fiberglass-reinforced plastic for corrosive areas)
- **Conduit**: Rigid steel conduit (RSC), IMC (intermediate metal conduit), EMT (electrical metallic tubing), or rigid PVC per CEC Section 12
- **Cable Tray Accessories**: Fittings (elbows, tees, reducers, drop-outs), covers (where required), support brackets and hangers

**Grounding Materials**:
- **Ground Grid Conductors**: Bare copper, 2/0 AWG or 4/0 AWG (per IEEE Std 80 and DEL-17.03 grounding calculations)
- **Ground Rods**: Copper-clad steel, 16 mm diameter × 3 m length (per CEC Section 10)
- **Grounding Connectors**: Exothermic weld (Cadweld or Thermoweld) for permanent, low-resistance connections; or bolted bronze/copper connectors with anti-oxidant compound

**Labels and Nameplates**:
- **Equipment Nameplates**: Engraved phenolic or stainless steel, per project tagging system (format and numbering **TBD**)
- **Cable Labels**: Permanent, UV-resistant, wrap-around or tie-on tags at cable terminations and pull boxes
- **Arc Flash Labels**: Per CSA Z462 requirements (incident energy level, PPE category, arc flash boundary, limited approach boundary)

## References

**Primary References**:
- **Decomposition Document**: /Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md (Section 4 — PKG-17, DEL-17.02 entry)
- **_CONTEXT.md**: Deliverable identity and anticipated artifacts (transformer, switchgear, MCC, cable specifications)
- **Employer's Requirements**: **TBD** — Volume 2 Parts 1-3 (electrical equipment specifications) — **location TBD**

**Applicable Standards** (Equipment Specifications — Canadian jurisdiction):

**Transformers**:
- CSA C88 (Power Transformers and Reactors — liquid-filled)
- CSA C802 (Dry-Type Distribution Transformers)
- IEEE C57 series (Transformer standards)
- NRCan Energy Efficiency Regulations (TP-1 or better)

**Switchgear and MCCs**:
- CSA C22.2 No. 31 (Metal-Clad and Metal-Enclosed Switchgear)
- CSA C22.2 No. 254 (Motor Control Centers)
- IEEE C37.20.7 (Arc-Resistant Switchgear)
- IEEE C37.04 (Rating Structure for AC High-Voltage Circuit Breakers)
- UL 1558 (Switchboards), UL 845 (MCCs)
- NEMA PB 2 (Switchboards), NEMA ICS 18 (MCCs)

**Cables**:
- CSA C68.3 (MV Cables — 5 kV to 46 kV)
- CSA C22.2 No. 38 (LV Cables — 1000V and under)
- ICEA S-93-639 / AEIC CS8 (MV cable specifications)
- CEC Section 4 (Conductors) and Section 12 (Wiring Methods)

**General Electrical**:
- CSA C22.1 (Canadian Electrical Code) — overall compliance
- CSA C22.3 No. 7 (Underground Systems, Seismic Requirements)
- IEEE 693 (Seismic Qualification of Equipment)
- CSA Z462 (Workplace Electrical Safety)
- ISO 12944 (Corrosion Protection of Steel Structures)

**Additional References**:
- See DEL-17.01 (Electrical Power Design Drawing Set) for equipment arrangements, single line diagrams, cable schedules
- See DEL-17.03 (Electrical Power Design Calculations) for equipment sizing rationale, short circuit analysis, protection coordination
- See DEL-17.04 (Electrical Power Data Sheet Package) for manufacturer-specific equipment data sheets
- **TBD**: Manufacturer catalogs and technical data for equipment selection

**Cross-references**:
- Dependencies coordinated externally (per _DEPENDENCIES.md — NOT_TRACKED mode)
- Interface with PKG-13 (Storage Tanks) for tank heating equipment specifications
- Interface with PKG-15 (Pumps and Rotating Equipment) for motor and starter specifications
- Interface with PKG-19 (Control & Instrumentation) for control cable, UPS, and instrumentation power specifications

---
**Cross-Document Alignment Verified (Pass 3):** Equipment categories and specifications consistent with Specification.md (SR-1 through SR-5), Guidance.md (Principles 1-6, Considerations 1-10), and Procedure.md (Steps 1-11). No conflicts identified.
