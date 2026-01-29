# Guidance: DEL-17.02 Electrical Power Technical Specification

## Purpose

This guidance document supports the development of **Electrical Power Technical Specification** for **PKG-17 Electrical Power Distribution**.

**Deliverable Purpose** (Source: Decomposition DEL-17.02 entry): Defines performance, materials, and workmanship requirements for electrical power per ER requirements.

**Downstream Use**:
- Equipment manufacturers use specifications to prepare quotes and proposals
- Procurement team uses specifications for bid evaluation and equipment selection
- Construction contractor uses specifications for equipment installation and testing
- Quality assurance team uses specifications for inspection and acceptance
- Commissioning team uses specifications for system testing and verification
- Operations and maintenance personnel use specifications to understand equipment capabilities and limitations

**Deliverable Classification**:
- **Type**: Specification (Technical Specification)
- **Discipline**: Electrical
- **Responsible**: D&B Contractor
- **Project Phase**: Design & Build — Phase 1

## Principles

**Engineering Rationale** (Electrical Equipment Specifications):

**1. Equipment Specification Completeness (Performance + Materials + Testing)**
- Effective technical specifications address three aspects: **Performance** (what the equipment must do), **Materials/Construction** (how it's built), and **Testing/Documentation** (how compliance is verified).
- **Rationale**: Complete specifications enable fair bid evaluation, ensure quality, and provide acceptance criteria.
- **Source**: Best practice per CSI MasterFormat specification organization; EJCDC specification guidance.

**2. Performance-Based vs. Prescriptive Specifications**
- **Performance-Based**: Specifies required performance, allows multiple manufacturers/models (e.g., "transformer shall have TP-1 efficiency, 65°C rise, ±5% taps").
- **Prescriptive**: Specifies exact product or brand (e.g., "transformer shall be ABB model XYZ or approved equal").
- **Rationale**: Design-build contracts typically use performance-based specifications to encourage competition and value engineering while maintaining quality standards.
- **Source**: Design-build delivery model (Decomposition Section 1); industry best practice.
- **Trade-off**: Performance specs require more engineering judgment during bid evaluation; prescriptive specs are simpler but may limit competition and increase cost.

**3. Standards-Based Equipment Requirements**
- Electrical equipment specifications shall reference applicable CSA, IEEE, UL, and NEMA standards rather than duplicating standard requirements.
- **Rationale**: Standards represent industry consensus on safety, performance, and testing; referencing standards ensures equipment meets minimum requirements without rewriting standard language.
- **Source**: CEC Section 2 (equipment approval requires certification to standards); regulatory requirement.
- **Example**: "Transformer shall comply with CSA C88" rather than listing all CSA C88 requirements in specification.

**4. Environmental and Application-Specific Requirements**
- Standard equipment may not be suitable for all environments; specifications must address project-specific conditions (seismic, corrosion, hazardous areas, outdoor vs. indoor).
- **Rationale**: Coastal BC has high seismic risk and marine corrosion environment; standard equipment may require upgrades (seismic anchorage, corrosion-resistant enclosures).
- **Source**: Project location (Fraser Surrey Terminal — marine environment); BC high seismic zone.
- **Requirements**: IEEE 693 seismic qualification, NEMA 3R/4X outdoor enclosures, ISO 12944 corrosion protection.

**5. Submittal and Quality Assurance Requirements**
- Specifications must define submittal requirements (what documentation contractor provides) and quality assurance procedures (how compliance is verified).
- **Rationale**: Submittals enable design review before equipment is procured/fabricated (catch errors early); QA procedures ensure installed equipment meets specifications.
- **Source**: Project quality management plan; standard design-build practice.
- **Typical Submittals**: Shop drawings, product data, test reports, certifications, IOM manuals.
- **Typical QA**: Factory acceptance testing (FAT), installation inspection, commissioning tests.

**6. Lifecycle Cost Considerations (OBJ-9)**
- Equipment specifications should balance initial cost with lifecycle cost (energy efficiency, maintenance, reliability, spare parts availability).
- **Rationale**: OBJ-9 (Lifecycle Cost Optimization — Decomposition Section 2) prioritizes long-term value over minimum first cost.
- **Example**: Specifying high-efficiency transformers (TP-1 or better) increases initial cost but reduces energy losses over 25+ year facility life; specifying vacuum circuit breakers (VCBs) in MV switchgear eliminates oil maintenance and reduces environmental risk.
- **Source**: OBJ-9 (Decomposition Section 2); IEEE Std 141 (Red Book) lifecycle cost guidance.

**Applicable Standards Context**:

| Standard Category | Key Standards | Specification Application |
|-------------------|---------------|---------------------------|
| **Transformers** | CSA C88 (liquid-filled), CSA C802 (dry-type), IEEE C57 series | Performance ratings, construction requirements, testing procedures, efficiency requirements (NRCan TP-1) |
| **Switchgear** | CSA C22.2 No. 31, IEEE C37 series (C37.20.7 arc-resistant, C37.04 ratings, C37.09 testing) | Voltage class, current rating, interrupting capacity, arc-resistant construction, circuit breaker specifications |
| **MCCs** | CSA C22.2 No. 254, UL 845, NEMA ICS 18 | Bus rating, SCCR, combination starter specifications, control power requirements |
| **Cables** | CSA C68.3 (MV), CSA C22.2 No. 38 (LV), ICEA/AEIC (MV), CEC Section 4 and 12 (installation) | Voltage rating, insulation type, conductor material, ampacity, installation methods |
| **Seismic** | IEEE 693, CSA C22.3 No. 7 | Seismic qualification testing (IEEE 693 High Performance Level), anchorage requirements for coastal BC high seismic zone |
| **Quality** | ISO 9001 | Manufacturer quality management system certification |

## Considerations

**Factors to Consider During Development**:

**1. Equipment Selection Strategy (Performance-Based with Pre-Qualified List)**
- **Option A**: Fully performance-based (any manufacturer meeting requirements).
- **Option B**: Performance-based with "approved manufacturers" list (limits bidders to pre-qualified manufacturers).
- **Option C**: Prescriptive ("or equal" basis manufacturer).
- **Consideration**: Option B balances competition with quality assurance (pre-qualify manufacturers with good track record, suitable products); Option A maximizes competition but increases bid evaluation effort; Option C limits competition.
- **Recommendation**: **TBD** — Confirm with Employer and project team; Option B typical for major equipment (transformers, switchgear).

**2. Arc-Resistant Switchgear (Safety vs. Cost)**
- **Requirement**: Specify arc-resistant MV switchgear (IEEE C37.20.7 Type 2B) or standard metal-clad switchgear?
- **Consideration**: Arc-resistant switchgear significantly reduces personnel injury risk during internal arcing fault but adds 30-50% cost premium.
- **Factors**: CSA Z462 requires arc flash hazard analysis and risk mitigation; arc-resistant switchgear is one mitigation strategy (others: remote operation, extensive PPE, optimized protective device settings).
- **Recommendation**: **ASSUMPTION** in Datasheet/Specification — specify arc-resistant Type 2B for MV switchgear to prioritize personnel safety (OBJ-1) and reduce arc flash hazard exposure; cost justified by safety benefit and reduced PPE/training requirements.
- **Reference**: See DEL-17.01 Guidance — Trade-off 6 (Arc Flash Mitigation Strategies).

**3. Transformer Type Selection (Liquid-Filled vs. Dry-Type)**
- **Liquid-Filled (Oil-Immersed)**: Lower cost, better cooling, longer life, requires spill containment and fire protection.
- **Dry-Type (Cast Resin or VPI)**: Higher cost, less efficient, suitable for indoor installations without fire/spill concerns.
- **Consideration**: Outdoor unit substations typically use liquid-filled transformers (cost-effective, proven reliability); indoor transformers serving lighting/small power typically dry-type (fire safety).
- **Decision**: **TBD** — Specify both types per application (liquid-filled for main distribution, dry-type for indoor lighting transformers).

**4. VFDs and Soft Starters for Motor Control**
- **Standard Starters (FVNR)**: Full-voltage non-reversing across-the-line starters (simple, low cost, high inrush current).
- **Soft Starters**: Reduced-voltage starting (lower inrush, less mechanical stress, moderate cost).
- **VFDs (Variable Frequency Drives)**: Full speed control, energy savings for variable loads, higher cost, generates harmonics.
- **Consideration**: Large pump motors (>50 HP) benefit from reduced-voltage starting (soft starters or VFDs); pumps with variable flow benefit from VFDs (energy savings per OBJ-9); VFDs require harmonic mitigation (filters or reactors) and may require larger cables (derating for harmonics).
- **Decision**: **TBD** — Identify motor applications requiring VFDs or soft starters based on process requirements (variable flow) and motor size (inrush current concerns); specify as MCC options.

**5. Cable Insulation Type (EPR vs. XLPE for MV; PVC vs. LSZH for LV)**
- **MV Cables**: EPR (ethylene propylene rubber) and XLPE (cross-linked polyethylene) are both common; XLPE has better thermal properties and is lighter; EPR has better flexibility and lower cost.
- **LV Cables**: PVC jacket is standard and economical; LSZH (low smoke zero halogen) is required in some indoor installations for fire safety (tunnels, high-occupancy buildings) but more expensive.
- **Consideration**: XLPE is industry standard for MV cables (better performance); LSZH may be required for indoor electrical rooms or enclosed spaces per fire protection requirements — **TBD** (confirm with fire protection engineer).
- **Decision**: Specify XLPE for MV cables (standard); specify PVC for outdoor/underground LV cables, LSZH for indoor cables if required by fire code.

**6. Equipment Enclosure Ratings (NEMA 1 vs. 3R vs. 4X)**
- **NEMA 1**: Indoor, general-purpose (not dust-tight or water-tight).
- **NEMA 3R**: Outdoor, rain-tight (protection from rain, sleet, snow; not dust-tight).
- **NEMA 4X**: Outdoor, watertight and corrosion-resistant (stainless steel, suitable for marine/corrosive environments).
- **Consideration**: Coastal BC has marine/industrial corrosive atmosphere; outdoor equipment should be NEMA 4X (stainless steel or coated steel per ISO 12944 C4/C5) for long-term reliability; NEMA 3R (painted carbon steel) may have shorter life and higher maintenance cost.
- **Trade-off**: NEMA 4X is 50-100% more expensive than NEMA 3R but justified by 25+ year facility life and reduced maintenance (OBJ-9).
- **Recommendation**: Specify NEMA 4X for outdoor equipment in marine environment; NEMA 1 for indoor equipment in controlled environment.

**7. Control Power (AC vs. DC)**
- **AC Control Power (120 VAC)**: Derived from control power transformer (CPT) in switchgear/MCC; simple, low cost, loses control during power outage.
- **DC Control Power (125 VDC)**: Derived from station battery and charger; maintains control during power outage (can operate circuit breakers for safe shutdown), higher cost (battery system).
- **Consideration**: Critical facilities often use DC control for MV switchgear (allows breaker operation during utility outage); LV equipment typically uses AC control (adequate for most applications).
- **Decision**: **TBD** — Confirm control power requirements with Employer; **ASSUMPTION**: 125 VDC for MV switchgear (critical utility service), 120 VAC for LV switchgear and MCCs (adequate reliability).

**8. Communication and SCADA Integration**
- **Stand-Alone Equipment**: No communication (local control and indication only).
- **Communicating Equipment**: Switchgear with protective relays and meters that communicate via Modbus TCP, DNP3, or IEC 61850; MCCs with VFDs or smart starters that communicate via Ethernet or serial protocols.
- **Consideration**: Facility may require SCADA system for remote monitoring and control (throughput capacity 1,000,000 MT/a suggests significant automation); communication capability allows centralized monitoring, alarm management, energy management.
- **Decision**: **TBD** — Confirm SCADA requirements with control system engineer (PKG-19); specify communication protocols and capabilities as required.

**9. Seismic Qualification and Anchorage**
- **Seismic Qualification**: Equipment tested and certified to withstand seismic events per IEEE 693 or equivalent.
- **Seismic Anchorage**: Equipment mounting and anchorage designed per CSA C22.3 No. 7 or NBC seismic provisions.
- **Consideration**: Coastal BC is high seismic zone (Zone 4 per NBC); seismic qualification and proper anchorage are mandatory for code compliance and life safety.
- **Specification Requirement**: Specify IEEE 693 High Performance Level for major equipment (transformers, switchgear, MCCs); specify anchorage design per CSA C22.3 No. 7 (may be design-build contractor responsibility or separate structural engineering deliverable).

**10. Spare Parts and Standardization**
- **Standardization**: Using single manufacturer for switchgear and MCCs reduces spare parts inventory, simplifies training, and improves maintenance efficiency.
- **Spare Parts**: Specify spare parts requirements (quantity and types) in specification or separate spare parts list.
- **Consideration**: Facility is remote from major electrical equipment suppliers (BC); spare parts availability and lead times may impact maintenance planning.
- **Recommendation**: Specify common equipment families where practical (e.g., single switchgear manufacturer, single MCC manufacturer); require contractor to provide recommended spare parts list; consider requiring initial spare parts package as part of contract (circuit breakers, contactors, overload relays, fuses).

## Trade-offs

**Competing Concerns to Evaluate**:

**1. Equipment Quality vs. Initial Cost**
- **Trade-off**: Premium brands (ABB, Schneider, Eaton, Siemens) vs. economy brands; industrial-grade vs. commercial-grade equipment.
- **Decision Factors**: Facility design life (25+ years), continuous duty requirements, harsh environment, lifecycle cost (OBJ-9), Employer risk tolerance.
- **Recommendation**: Specify industrial-grade equipment from established manufacturers; accept moderate cost premium for quality, reliability, and long-term support.

**2. Standardization vs. Optimization**
- **Trade-off**: Single manufacturer for all switchgear/MCCs (standardization, training, spare parts) vs. best-of-breed for each application (optimization, potentially lower cost).
- **Decision Factors**: Operations preference, maintenance staff size/training, spare parts budget, procurement complexity.
- **Recommendation**: Standardize within equipment categories (single MCC manufacturer, single LV switchgear manufacturer) but allow different manufacturers for different categories (MV switchgear, transformers, MCCs may be different manufacturers).

**3. Performance Specifications vs. Prescriptive (Brand-Specific)**
- **Trade-off**: Open competition (performance-based) vs. limited competition (prescriptive).
- **Decision Factors**: Design-build model encourages performance-based; Employer may have brand preferences based on experience; procurement schedule (limited competition may reduce bidding time).
- **Recommendation**: Performance-based with pre-qualified manufacturer list for major equipment; allows competition among proven manufacturers while maintaining quality standards.

**4. Arc-Resistant Switchgear vs. Standard (Safety vs. Cost)**
- **Trade-off**: 30-50% cost premium for arc-resistant MV switchgear.
- **Decision Factors**: Personnel safety (OBJ-1), arc flash hazard levels, CSA Z462 compliance strategy, frequency of maintenance/switching operations.
- **Recommendation**: Specify arc-resistant Type 2B for MV switchgear (safety justifies cost; reduces arc flash PPE requirements and training burden).

**5. Liquid-Filled vs. Dry-Type Transformers (Cost vs. Fire Safety)**
- **Trade-off**: Liquid-filled is lower cost and more efficient but requires spill containment and fire protection; dry-type is higher cost and less efficient but no fire/spill risk.
- **Decision Factors**: Indoor vs. outdoor location, fire protection requirements, environmental regulations, lifecycle cost.
- **Recommendation**: Liquid-filled for outdoor unit substations (cost-effective); dry-type for indoor lighting transformers (fire safety).

**6. VFDs for Pumps (Energy Savings vs. Initial Cost and Complexity)**
- **Trade-off**: VFDs add 20-40% cost vs. standard starters but provide energy savings for variable-flow pumps and reduced mechanical stress on motors/driven equipment.
- **Decision Factors**: Pump operating profile (constant vs. variable flow), motor size, energy cost, lifecycle cost (OBJ-9).
- **Recommendation**: Specify VFDs for large pumps (>50 HP) with variable flow requirements (transfer pumps, marine loading pumps); energy savings justify initial cost over facility life; use standard starters for constant-speed pumps (heating circulation).

**7. Communication Capability (SCADA Integration vs. Stand-Alone)**
- **Trade-off**: Communicating equipment (protective relays, meters, VFDs with Ethernet/serial communication) adds cost but enables centralized monitoring, alarm management, energy management.
- **Decision Factors**: Facility size/complexity, operations staffing, SCADA system requirements (PKG-19), remote monitoring needs.
- **Recommendation**: **TBD** — Coordinate with control system engineer; likely specify communication capability for MV switchgear (protective relays), LV switchgear (metering), and VFDs (process control) to support facility-wide SCADA system.

**8. NEMA 3R vs. NEMA 4X Outdoor Enclosures (Cost vs. Corrosion Protection)**
- **Trade-off**: NEMA 4X (stainless steel or coated steel) is 50-100% more expensive than NEMA 3R (painted carbon steel) but provides superior corrosion resistance in marine environment.
- **Decision Factors**: Facility location (marine/industrial atmosphere), design life (25+ years), maintenance cost and frequency, lifecycle cost (OBJ-9).
- **Recommendation**: Specify NEMA 4X for outdoor equipment (marine environment justifies cost premium; reduces maintenance and extends equipment life).

## Examples

**Reference Examples and Precedents**:

**1. Transformer Specification Example (Performance-Based)**

**Performance Requirements** (from Specification.md SR-1):
- kVA Rating: 1500 kVA (based on load analysis)
- Voltage Ratio: 25 kV delta primary / 600Y/347V secondary (grounded wye)
- Impedance: 5.75% ±7.5% on transformer base (for coordination with upstream utility protection)
- Temperature Rise: 65°C (55/65°C oil/winding per CSA C88)
- Cooling: ONAN (oil natural, air natural) — self-cooled
- Taps: Four 2.5% taps above rated voltage, four 2.5% taps below rated voltage (±10% range), de-energized tap changer
- Efficiency: TP-1 or better per NRCan Energy Efficiency Regulations
- Sound Level: Maximum 60 dBA at 1 meter
- Standards: CSA C88, IEEE C57.12.00
- Seismic: IEEE 693 High Performance Level
- Enclosure: Outdoor NEMA 3R, stainless steel or epoxy-coated carbon steel

**2. MV Switchgear Specification Example (Performance-Based with Pre-Qualified Manufacturers)**

**Acceptable Manufacturers** (example):
- ABB (SafeRing or SafePlus MV switchgear)
- Schneider Electric (Premset or SM6 MV switchgear)
- Eaton (VacClad-W MV switchgear)
- Or approved equal (subject to submittal review and approval 60 days prior to bid)

**Performance Requirements** (from Specification.md SR-2):
- Voltage Class: 25 kV class (27 kV maximum rating per IEEE C37.04)
- Continuous Current Rating: 1200A bus, 1200A circuit breakers
- Interrupting Capacity: 25 kA symmetrical RMS (based on utility fault current)
- Arc-Resistant: Type 2B per IEEE C37.20.7 (personnel access to front, rear, top)
- Circuit Breakers: Vacuum (VCB), stored energy operators, electrically operated, drawout, 10,000 mechanical operations minimum
- Protection: Microprocessor relays (SEL, Schweitzer Engineering Labs, or approved equal) with ANSI 50/51 overcurrent, 50/51G ground overcurrent, 27/59 under/overvoltage functions; Modbus TCP communication
- Instrumentation: Multifunction meters (PM8000 series or equivalent) with V, A, kW, kVAR, kWh, PF, THD; Modbus TCP communication
- Control Power: 125 VDC (station battery system separate package)
- Standards: CSA C22.2 No. 31, IEEE C37.20.2 (metal-clad), IEEE C37.20.7 (arc-resistant), IEEE C37.04 (ratings)
- Seismic: IEEE 693 High Performance Level
- Enclosure: Indoor NEMA 1 (electrical room installation)

**3. MCC Specification Example (Performance-Based)**

**Performance Requirements** (from Specification.md SR-3):
- Voltage Rating: 600V class
- Horizontal Bus Rating: 600A
- SCCR: 65 kA RMS symmetrical
- Construction: NEMA ICS 18 modular construction, withdrawable buckets, plug-in bus connections
- Starters: Size 1 through Size 5 NEMA combination starters (contactor + overload + disconnect), FVNR (full voltage non-reversing)
- VFDs: Provide VFDs (480V input, 0-60 Hz output) for pump motors P-101, P-102, P-201 per motor schedule (separate VFD specification section or include in MCC spec)
- Overload Protection: Electronic overload relays (current sensing, adjustable trip class, automatic reset)
- Control Power: 120 VAC derived from CPT (control power transformer) in MCC
- Pilot Devices: NEMA 4X heavy-duty pushbuttons (green start, red stop), HOA (hand-off-auto) selector switches, LED indicating lights (run, stop, fault)
- Standards: CSA C22.2 No. 254, UL 845, NEMA ICS 18
- Seismic: Anchorage per CSA C22.3 No. 7
- Enclosure: Outdoor NEMA 4X (stainless steel Type 316), space heaters (thermostatically controlled)

**4. Cable Specification Example**

**MV Cable** (feeder from MV switchgear to unit substation transformer):
- Voltage Class: 25 kV (28 kV insulation rating, 133% insulation level per CSA C68.3)
- Conductor: Copper, stranded Class B, 1/0 AWG (three single-conductor cables for three-phase circuit)
- Insulation: XLPE (cross-linked polyethylene), 90°C rated, 175 mils thickness
- Shielding: Extruded semiconducting insulation shield (inner and outer), copper tape metallic shield with drain wire (full neutral return capacity)
- Jacket: Black PE (polyethylene), 80 mils thickness, suitable for direct burial
- Installation: Underground duct bank (PVC conduit), 600 mm depth, concrete-encased
- Ampacity: 180A at 25°C ambient, 1.0 RHO soil thermal resistivity (verify by calculation — DEL-17.03)
- Testing: Factory AC high-potential (Hi-Pot) test per CSA C68.3, DC leakage test
- Standards: CSA C68.3, ICEA S-93-639

**LV Cable** (feeder from MCC to pump motor):
- Voltage Rating: 600V
- Conductor: Copper, stranded Class B, 3/C #2 AWG + 1/C #6 AWG ground
- Insulation: RW90 XLPE (90°C dry and wet)
- Jacket: Black PVC
- Installation: Cable tray (ladder tray)
- Ampacity: 115A (three current-carrying conductors in cable tray, 30°C ambient, per CEC Table 2)
- Color Coding: Red-Black-Blue (phases), White (neutral if present), Green (ground)
- Standards: CSA C22.2 No. 38, CEC Section 4 and 12

**5. Typical Specification Organization (CSI MasterFormat Division 26)**

```
SECTION 26 05 00 — GENERAL ELECTRICAL REQUIREMENTS
  1.1 Scope
  1.2 Related Sections
  1.3 References (CSA, IEEE, UL, NEMA standards)
  1.4 Definitions
  1.5 Submittals (shop drawings, product data, test reports, certifications, manuals)
  1.6 Quality Assurance (manufacturer qualifications, factory testing, installation inspection)
  1.7 Delivery, Storage, and Handling
  1.8 Warranty

SECTION 26 11 00 — LIQUID-FILLED TRANSFORMERS
  2.1 General
  2.2 Products (performance requirements, materials, construction, accessories, testing)
  2.3 Execution (installation, connections, testing, commissioning)

SECTION 26 12 00 — DRY-TYPE TRANSFORMERS
  [Similar organization]

SECTION 26 24 00 — MV SWITCHGEAR
  [Similar organization]

SECTION 26 25 00 — LV SWITCHGEAR
  [Similar organization]

SECTION 26 26 00 — MOTOR CONTROL CENTERS
  [Similar organization]

SECTION 26 27 00 — MV CABLES
  [Similar organization]

SECTION 26 28 00 — LV POWER CABLES
  [Similar organization]
```

**Reference Sources**:
- **Employer's Requirements**: **TBD** — Volume 2 Parts 1-3 (electrical equipment specifications) — **location TBD** — may provide project-specific requirements or precedent specifications
- **CSA/IEEE Standards**: CSA C88, C802, C22.2 series, IEEE C37 and C57 series — provide technical requirements and testing procedures
- **Manufacturer Catalogs**: ABB, Schneider Electric, Eaton, Siemens — provide performance data, construction details, testing capabilities
- **Similar Facilities**: Other bulk liquid transload terminals (vegetable oil, petroleum products) — **TBD** — lessons learned and precedent specifications
- **Industry Specifications**: EJCDC, CSI MasterFormat — provide specification organization and language templates

---
**Cross-Document Alignment Verified (Pass 3):** Principles 1-6 and Considerations 1-10 align with Specification.md functional and specification requirements (FR-1 through FR-5, SR-1 through SR-5). Trade-offs and examples support engineering decisions reflected in Datasheet.md and Procedure.md. No conflicts identified.
