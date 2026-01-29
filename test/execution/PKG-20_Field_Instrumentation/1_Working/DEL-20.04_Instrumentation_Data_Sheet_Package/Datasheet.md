# Datasheet: DEL-20.04 Instrumentation Data Sheet Package

## Identification

| Field | Value |
|-------|-------|
| Deliverable ID | DEL-20.04 |
| Name | Instrumentation Data Sheet Package |
| Package | PKG-20 Field Instrumentation |
| Discipline | I&C |
| Type | Data Sheet |
| Responsible | D&B Contractor |
| Status | INITIALIZED |
| Project | Canola Oil Transload Facility — Phase 1 |
| Location | Fraser Surrey Terminal, 11060 Elevator Road, Surrey, BC |

**Source:** Decomposition document, DEL-20.04 (line 499)

## Attributes

**Data Sheet Package Characteristics:**

| Attribute | Value |
|-----------|-------|
| Package Type | Equipment data sheets for field instrumentation |
| Data Sheet Format | **TBD** — Tabular format per project standards |
| Numbering Convention | **TBD** — Per project instrument numbering system (ISA 5.1 tagging) |
| Revision Control | **TBD** — Per project document control procedures |
| Typical Content | Equipment specifications, performance parameters, materials, certifications |
| Usage | Procurement (vendor quotes), construction (installation verification), operations (asset records) |

**Anticipated Data Sheet Types:**
- Level transmitter data sheets (radar, guided wave, switches)
- Pressure transmitter data sheets (gauge, differential, switches)
- Flow instrument data sheets (meters, switches) — coordinate with PKG-12 for custody transfer
- Temperature element data sheets (RTDs, thermocouples, thermowells)

**Source:** Decomposition DEL-20.04 Anticipated Artifacts (line 499); **ASSUMPTION** based on typical data sheet package scope

## Conditions

**Project Context:**

Data sheets support the Canola Oil Transload Facility Phase 1 (1,000,000 MT/annum throughput, 3 × 15,000 MT storage tanks, 32 railcar unloading stations).

**Source:** Decomposition Section 1.1 Key Parameters

**Data Sheet Purpose:**

Equipment data sheets serve multiple purposes:
1. **Procurement:** Basis for vendor RFQs, bid evaluation, equipment purchase
2. **Engineering verification:** Demonstrate compliance with DEL-20.02 specification and DEL-20.03 calculations
3. **Construction:** Installation reference (mounting, connections, power requirements)
4. **Commissioning:** Calibration and testing basis (see DEL-20.05)
5. **Operations:** Asset records for maintenance and spare parts

**Data Sheet Content (Typical):**

Each instrument data sheet contains:
- **Identification:** Tag number (per ISA 5.1), service description, P&ID reference
- **Service Conditions:** Process fluid, operating pressure/temperature, environmental conditions
- **Performance:** Range, accuracy, output signal (4-20 mA, HART, digital)
- **Construction:** Materials (wetted parts, enclosure), hazardous area rating, mounting
- **Electrical:** Power supply, signal wiring, cable entry
- **Certifications:** Hazardous area certification (CSA/UL), material certifications
- **Vendor Information:** Manufacturer, model number, serial number (as-built)

**Source:** **ASSUMPTION** based on typical instrument data sheet content

**Instrument Population (Estimated):**

- **Level instruments:** 10-20 transmitters (storage tanks, process vessels, pits), 20-40 switches (alarms, interlocks)
- **Pressure instruments:** 30-50 transmitters (pumps, piping, loading), 20-30 switches (alarms)
- **Temperature instruments:** 20-30 RTDs (product temperature, equipment monitoring), 10-20 thermocouples (high-temp applications)
- **Flow instruments:** 5-10 meters (process control), 10-20 switches (pump protection) — custody transfer meters in PKG-12

**Source:** **ASSUMPTION** based on facility scope (32 railcar stations, 3 storage tanks, pumping systems) and typical bulk terminal instrumentation density

## Construction

**Data Sheet Development Workflow:**

1. **Template Preparation:** Develop data sheet templates aligned with DEL-20.02 specification requirements
2. **Design Data Population:** Complete data sheets with calculated ranges (DEL-20.03) and specification requirements (DEL-20.02)
3. **Vendor Solicitation:** Issue data sheets to vendors for quotations (RFQ process)
4. **Vendor Data Review:** Review vendor-completed data sheets for compliance
5. **Approval:** Approve vendor data sheets for procurement
6. **As-Built Update:** Update data sheets with actual equipment serial numbers and test data (DEL-20.05)

**Source:** **ASSUMPTION** based on typical EPC data sheet workflow

**Data Sheet Types by Instrument Category:**

### Level Transmitter Data Sheets

**Radar Level Transmitters (Storage Tanks):**
- Application: 3 × 15,000 MT storage tanks (continuous level measurement)
- Technology: Non-contact radar (26 GHz typical)
- Range: 0 to 15 m (tank height — **TBD**)
- Accuracy: ±3 mm (tank gauging accuracy for inventory)
- Output: 4-20 mA + HART
- Enclosure: NEMA 4X, stainless steel or marine aluminum
- Hazardous area: CSA Class I, Div 2 / Zone 2 (**TBD**: per hazardous area classification)

### Pressure Transmitter Data Sheets

**Pump Suction/Discharge Pressure Transmitters:**
- Application: Pump performance monitoring
- Range: **TBD** — Based on pump design (suction: 0-2 bar, discharge: 0-10 bar typical)
- Accuracy: ±0.5% of span (process control)
- Output: 4-20 mA + HART
- Wetted materials: 316 stainless steel
- Overpressure rating: ≥2× range or piping MAWP
- Hazardous area: CSA Class I, Div 2 / Zone 2 (**TBD**)

### Temperature Element Data Sheets

**RTD Temperature Elements (Product Temperature):**
- Application: Storage tank and transfer line temperature monitoring
- Element type: Pt100 Class A (±0.15°C + 0.002|t|)
- Range: -50°C to +100°C (canola oil service)
- Construction: 3-wire or 4-wire, 316 stainless steel thermowell
- Output: 4-20 mA transmitter or direct RTD signal
- Response time: **TBD** — Based on thermowell design

**Source:** **ASSUMPTION** based on typical instrumentation for canola oil storage and transfer; **TBD**: Specific ranges and parameters from process design

## References

**Primary References:**

- Decomposition document, Section PKG-20 (lines 486-501)
- DEL-20.02 Instrumentation Technical Specification (requirements basis)
- DEL-20.03 Instrumentation Design Calculations (calculated ranges and parameters)
- DEL-20.01 Instrumentation Design Drawing Set (installation context)
- P&IDs and instrument list (tag numbers, service descriptions)

**Vendor References:**

- Vendor catalogs and technical literature
- Vendor quotations and proposals
- Manufacturer installation and operation manuals

**Applicable Standards:**

- ISA 5.1 (instrument tagging conventions)
- DEL-20.02 specification references (ISA 84, API 554, CSA C22.1, etc.)

**Related Deliverables:**

- DEL-20.05 (Installation & Test Records) — test data updates data sheets as-built

**Dependencies:** See `_DEPENDENCIES.md` — **NOT_TRACKED** (coordinated externally)

**Project Objective Alignment:**

Supports **OBJ-1: Safe & Reliable Operation** — Data sheets ensure specified and procured instruments are suitable for safe and reliable facility operations.

**Source:** Decomposition Section 6 (line 780)

## Cross-Document Traceability

This Datasheet provides factual identification, attributes, conditions, and references for DEL-20.04. The following documents provide complementary information:

| Document | Purpose | Key Linkages |
|----------|---------|--------------|
| Specification.md | Requirements and verification criteria | FR-1 to FR-4 define functional requirements; QR-1 to QR-3 define quality requirements |
| Guidance.md | Engineering rationale and decision context | Principles 1-3 explain data sheet lifecycle; Trade-off addresses standardization |
| Procedure.md | Production workflow and verification steps | Steps 1-5 define three-phase lifecycle (design, procurement, as-built) |

**Document Consistency Verification:**

- All data sheet types in Datasheet Attributes § appear in Specification Documentation and Procedure Records
- Related deliverables in Datasheet References § appear in Specification INT requirements and Procedure Prerequisites
- Data sheet purpose and usage in Datasheet Conditions § align with Guidance Principles and Procedure Steps
