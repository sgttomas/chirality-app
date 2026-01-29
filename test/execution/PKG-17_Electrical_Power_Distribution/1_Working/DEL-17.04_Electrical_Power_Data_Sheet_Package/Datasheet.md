# Datasheet: DEL-17.04 Electrical Power Data Sheet Package

## Identification

| Field | Value |
|-------|-------|
| Deliverable ID | DEL-17.04 |
| Name | Electrical Power Data Sheet Package |
| Package | PKG-17 Electrical Power Distribution |
| Discipline | Electrical |
| Type | Data Sheet |
| Responsible | D&B Contractor |
| Status | INITIALIZED |

## Attributes

| Attribute | Value |
|-----------|-------|
| Data Sheet Package Contents | Transformer data sheets, MCC data sheets, switchgear data sheets, UPS data sheet (Source: _CONTEXT.md) |
| Number of Equipment Items | **TBD** — Based on equipment list from DEL-17.01 (anticipated: 2-3 transformers, 4-8 MCCs, 1-2 switchgear lineups, 1 UPS) |
| Data Sheet Format | Manufacturer standard format supplemented with project requirements |
| Revision | 0 (Initial issue) |
| Classification | For Construction |

### Data Sheet Types and Purposes

| Data Sheet Type | Equipment Covered | Purpose | Source | Specification Reference | Guidance Reference | Procedure Step |
|-----------------|-------------------|---------|--------|------------------------|-------------------|----------------|
| **Transformer Data Sheets** | Unit substations (liquid-filled), dry-type transformers | Nameplate ratings, construction details, test results, compliance certifications | Manufacturer submittal | FR-1 (Specification.md) | Principle 1, 2 (Guidance.md) | Step 3 (Procedure.md) |
| **Switchgear Data Sheets** | MV switchgear, LV switchgear | Bus ratings, breaker ratings, protection relay data, test results | Manufacturer submittal | FR-2 (Specification.md) | Principle 1, 2 (Guidance.md) | Step 3 (Procedure.md) |
| **MCC Data Sheets** | Motor control centers (600V or 480V) | Bus rating, bucket schedule, motor starter data, test results | Manufacturer submittal | FR-2 (Specification.md) | Principle 1, 2 (Guidance.md) | Step 3 (Procedure.md) |
| **UPS Data Sheet** | Uninterruptible power supply for control systems | Capacity (kVA), battery backup time, input/output characteristics | Manufacturer submittal | FR-1 (Specification.md) | Principle 1 (Guidance.md) | Step 3 (Procedure.md) |

**Source**: _CONTEXT.md (anticipated artifacts); Decomposition DEL-17.04 entry.

## Conditions

**Design Basis and Context:**

This data sheet package defines and substantiates electrical power equipment in accordance with Employer's Requirements and project specifications.

**Project Context** (Source: Decomposition Section 1):
- **Location**: Fraser Surrey Terminal, 11060 Elevator Road, Surrey, BC
- **Facility Type**: Canola oil transload (rail-to-storage-to-ship)
- **Throughput**: 1,000,000 MT per annum (OBJ-2)
- **Key Electrical Equipment**: Transformers for main distribution, switchgear for utility service and secondary distribution, MCCs for motor control, UPS for control system reliability

**Equipment Operating Conditions**:
- **Ambient Temperature**: -20°C to +40°C (outdoor equipment, coastal BC)
- **Altitude**: Sea level (Fraser Surrey waterfront)
- **Humidity**: High (coastal marine environment)
- **Corrosion Environment**: Marine/industrial (salt air, industrial pollutants) — ISO 12944 C4/C5
- **Seismic**: High seismic zone (coastal BC) — IEEE 693 qualification required
- **Service Duty**: Continuous (24/7 operation, 8760 hours/year)
- **Design Life**: 25+ years minimum

**Data Sheet Purpose**:
- Verify equipment compliance with specifications (DEL-17.02)
- Verify equipment ratings match design calculations (DEL-17.03)
- Provide equipment data for installation planning
- Provide baseline for commissioning and testing (DEL-17.05)
- Provide equipment information for operations and maintenance

## Construction

**Data Sheet Content by Equipment Type:**

### 1. Transformer Data Sheets

**Liquid-Filled Unit Substations** (anticipated: 2-3 units for main distribution):

**Nameplate Data**:
- Manufacturer, model, serial number
- kVA rating (typical: 1000-1500 kVA based on load analysis — DEL-17.03)
- Voltage ratio (primary/secondary): 25 kV or 13.8 kV / 600Y-347V or 480Y-277V — **TBD**
- Impedance (% on transformer base): typical 5.5-6.5%
- Temperature rise: 65°C (55/65°C oil/winding per CSA C88)
- Cooling: ONAN (oil natural, air natural — self-cooled)
- Frequency: 60 Hz
- Phases: 3
- Connection: Delta primary / Wye secondary (grounded neutral)

**Construction Details**:
- Standards: CSA C88, IEEE C57.12.00
- Insulation: Mineral oil (or less-flammable fluid — **TBD**)
- Core material: Grain-oriented silicon steel
- Winding material: Copper (or aluminum — **TBD**)
- Taps: ±5% (four 2.5% taps above and below nominal), de-energized tap changer
- Bushings: MV bushings (primary), LV bushings or cable compartment (secondary)
- Tank: Steel, welded construction
- Finish: Epoxy paint or similar (outdoor rated)
- Enclosure: Outdoor NEMA 3R or equivalent

**Performance Data**:
- Efficiency: TP-1 or better (NRCan Energy Efficiency Regulations)
- No-load losses: Per manufacturer (typical: 1-2 kW for 1000-1500 kVA)
- Load losses: Per manufacturer (typical: 10-15 kW at rated load)
- Sound level: Per manufacturer (typical: 55-65 dBA at 1m)
- Short circuit withstand: Per IEEE C57.12.00 (Category II or III)

**Accessories**:
- Liquid level gauge
- Winding temperature indicator (WTI)
- Liquid temperature indicator (LTI)
- Pressure relief device
- Drain valve
- Sampling valve (for oil testing)
- Ground pads (primary and secondary)
- Lifting lugs
- Nameplate (stainless steel, engraved)

**Test Reports**:
- Routine tests per CSA C88: Resistance, polarity, voltage ratio, no-load loss, impedance, applied voltage test, induced voltage test
- Optional tests (if specified): Temperature rise, sound level, short circuit test
- Test certificates and reports included with submittal

**Dry-Type Transformers** (anticipated: 2-4 units for lighting/small power):

**Nameplate Data**:
- kVA rating (typical: 150-500 kVA)
- Voltage ratio: 600V or 480V / 208Y-120V — **TBD**
- Impedance: typical 4-6%
- Temperature rise: 150°C or 115°C insulation class
- Cooling: AN (air natural — self-cooled)

**Construction Details**:
- Standards: CSA C802, IEEE C57.12.01
- Insulation: Cast resin or VPI (vacuum pressure impregnated)
- Core and windings: Copper or aluminum
- Taps: ±5% (two 2.5% taps above and below nominal)
- Enclosure: NEMA 1 (indoor) or NEMA 3R (outdoor) — **TBD**

**Performance Data**:
- Efficiency: TP-1 or better
- No-load and load losses per manufacturer
- Sound level: typical 60-70 dBA at 1m

### 2. Switchgear Data Sheets

**MV Switchgear** (anticipated: 1 lineup with 4-8 breaker positions):

**Nameplate Data**:
- Manufacturer, model, serial number
- Voltage class: 25 kV or 15 kV — **TBD** (based on utility service)
- Bus continuous current rating: 1200A, 2000A, or 3000A — **TBD**
- Short circuit current rating: 25-40 kA (25 kV) or 40-63 kA (15 kV) — **TBD** (based on DEL-17.03 short circuit analysis)
- Standards: CSA C22.2 No. 31, IEEE C37.20.2 (metal-clad), IEEE C37.20.7 (arc-resistant)
- Arc-resistant type: Type 2B (personnel access to front, rear, top)

**Circuit Breaker Data** (per breaker position):
- Breaker type: Vacuum circuit breaker (VCB)
- Continuous current rating: **TBD** (per circuit)
- Interrupting capacity: **TBD** (match switchgear SCCR)
- Operating mechanism: Stored energy (spring-charged), electrically operated
- Mounting: Drawout (removable)
- Mechanical endurance: 10,000 operations minimum
- Electrical endurance: Per IEEE C37.04 and C37.09
- Control voltage: 125 VDC or 120 VAC — **TBD**

**Protection and Metering**:
- Protective relays: Microprocessor-based (manufacturer/model — **TBD**)
- Relay functions: 50/51 (overcurrent), 50/51G (ground overcurrent), 27/59 (under/overvoltage) — **TBD** per application
- Relay settings: Per DEL-17.03 protection coordination study
- Metering: Digital multifunction meters (V, A, kW, kVAR, kWh, PF, THD) with communication (Modbus TCP or IEC 61850)

**Test Reports**:
- Dielectric (high-potential) test
- Primary current injection test
- Protective relay functional test and settings verification
- Mechanical operation test
- Insulation resistance test
- Test certificates included with submittal

**LV Switchgear** (anticipated: 2-3 lineups):

**Nameplate Data**:
- Voltage rating: 600V or 480V — **TBD**
- Bus continuous current rating: 1600A, 2500A, or 4000A — **TBD**
- SCCR: 65 kA or 100 kA RMS symmetrical — **TBD**
- Standards: CSA C22.2 No. 31, UL 1558

**Circuit Breaker Data** (per position):
- Breaker type: Insulated-case (ICCB), molded-case (MCCB), or low-voltage power circuit breaker (LVPCB)
- Ratings and trip unit settings: **TBD** per circuit
- Control voltage: 120 VAC

**Metering and Communication**:
- Digital metering per feeder (V, A, kW, kVAR, kWh, PF)
- Communication: **TBD** (Modbus, Ethernet)

### 3. MCC Data Sheets

**Motor Control Centers** (anticipated: 4-8 lineups):

**Nameplate Data**:
- Manufacturer, model, serial number
- Voltage rating: 600V or 480V — **TBD**
- Horizontal bus continuous current rating: 600A, 800A, or 1600A — **TBD**
- SCCR: 65 kA or 100 kA — **TBD**
- Standards: CSA C22.2 No. 254, UL 845, NEMA ICS 18

**Bucket Schedule** (for each MCC lineup):
- Bucket number, motor/load served, starter size (NEMA Size 1-5), breaker/disconnect rating, overload setting, control devices (HOA switch, start/stop buttons, pilot lights)

**Starter Data** (per bucket):
- Starter type: Combination starter (FVNR — full voltage non-reversing)
- Contactor: IEC or NEMA type, continuous current rating, coil voltage
- Overload relay: Electronic or thermal-magnetic, trip class (Class 10, 20, 30), adjustable range
- Disconnect: Fused or non-fused disconnect switch
- VFD (if applicable): Manufacturer, model, HP rating, input/output voltage, control features

**Control Power**:
- Source: Control power transformer (CPT) in MCC or external feed
- Voltage: 120 VAC

**Test Reports**:
- High-potential (dielectric) test
- Control circuit functional test
- Mechanical operation test
- Test certificates included with submittal

### 4. UPS Data Sheet

**UPS System** (for control system and instrumentation power):

**Nameplate Data**:
- Manufacturer, model, serial number
- Capacity: **TBD** kVA (based on control system loads from PKG-19)
- Input voltage: 208V or 480V, 3-phase — **TBD**
- Output voltage: 120V, single-phase or 208Y/120V, 3-phase — **TBD**
- Frequency: 60 Hz
- Topology: Double-conversion (online) or line-interactive — **TBD**
- Efficiency: Per manufacturer (typical: 90-95%)

**Battery Data**:
- Battery type: Valve-regulated lead-acid (VRLA) or lithium-ion — **TBD**
- Battery capacity: **TBD** Ah
- Backup time: **TBD** minutes at full load (typical: 15-30 minutes for orderly shutdown)
- Battery voltage: **TBD** VDC
- Recharge time: **TBD** hours

**Features**:
- Automatic bypass (maintenance bypass and static bypass)
- Communication: SNMP, Modbus, or proprietary (for SCADA integration)
- Alarms: Battery low, overload, bypass, fault
- Display: LCD with status indicators

**Test Reports**:
- Factory acceptance test (FAT) report
- Battery discharge test
- Load test
- Test certificates included with submittal

## References

**Primary References**:
- **Decomposition Document**: /Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md (Section 4 — PKG-17, DEL-17.04 entry)
- **_CONTEXT.md**: Deliverable identity and anticipated data sheet artifacts
- **Employer's Requirements**: **TBD** — Volume 2 Parts 1-3 (equipment requirements) — **location TBD**

**Supporting Deliverables**:
- **DEL-17.01** (Electrical Power Design Drawing Set): Equipment list, single line diagrams showing equipment to be documented
- **DEL-17.02** (Electrical Power Technical Specification): Equipment performance and construction specifications that data sheets must demonstrate compliance with
- **DEL-17.03** (Electrical Power Design Calculations): Equipment ratings and sizing basis that data sheets must verify
- **DEL-17.05** (Electrical Power Installation & Test Records): Data sheets provide baseline for commissioning tests

**Applicable Standards** (Equipment Data Sheets):
- CSA C88, CSA C802 (Transformers)
- CSA C22.2 No. 31, No. 254 (Switchgear and MCCs)
- IEEE C57 series (Transformers)
- IEEE C37 series (Switchgear and circuit breakers)
- UL 1558, UL 845 (Switchgear and MCCs)

**Cross-references**:
- Dependencies coordinated externally (per _DEPENDENCIES.md — NOT_TRACKED mode)
- Interface with PKG-19 (Control & Instrumentation) for UPS capacity and control system loads

---
**Cross-Document Alignment Verified (Pass 3):** Data sheet types and content requirements consistent with Specification.md (FR-1 through FR-3, QR-1, QR-2), Guidance.md (Principles 1-3, Considerations 1-3), and Procedure.md (Steps 1-6). No conflicts identified.
