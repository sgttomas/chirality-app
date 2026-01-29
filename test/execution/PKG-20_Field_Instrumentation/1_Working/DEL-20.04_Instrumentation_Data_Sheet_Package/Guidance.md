# Guidance: DEL-20.04 Instrumentation Data Sheet Package

## Purpose

Supports development of **Instrumentation Data Sheet Package** for **PKG-20 Field Instrumentation**.

**Deliverable Objective:** Defines and substantiates instrumentation in accordance with ER requirements.

**Source:** Decomposition document, DEL-20.04 (line 499)

**Cross-Document Context:** Data sheets implement DEL-20.02 specifications, incorporate DEL-20.03 calculated parameters, and support DEL-20.05 testing. See Procedure.md for data sheet development workflow.

## Principles

**Principle 1: Data Sheets Bridge Design and Procurement**

Data sheets translate engineering requirements (specifications, calculations) into equipment procurement documents that vendors can quote and supply against.

**Principle 2: Three-Phase Lifecycle**

- **Design phase:** Engineer-completed data sheets issued to vendors (RFQ basis)
- **Procurement phase:** Vendor-completed data sheets demonstrate compliance (bid evaluation, approval)
- **As-built phase:** Updated with actual equipment data (serial numbers, test results)

**Principle 3: Traceability**

Each data sheet traces to: P&ID (tag number), specification (requirements), calculations (verified parameters), drawings (installation location).

**Source:** **ASSUMPTION** based on typical EPC data sheet philosophy

## Considerations

**Project-Specific:**

- Large instrument population (32 railcar stations, 3 storage tanks) requires efficient template-based approach
- Standardization preferred where possible (reduce spare parts inventory, simplify training)
- Marine environment (corrosion) and hazardous area requirements drive material and certification specifications

**Technical:**

**Level Instruments:**
- Storage tanks: High-accuracy radar for inventory (±3 mm typical)
- Process vessels: Guided wave or float for reliability
- Overfill protection: Independent level switches per API 2350

**Pressure Instruments:**
- Pump monitoring: Standard ranges (0-2 bar suction, 0-10 bar discharge typical)
- Marine loading: Pressure control for loading rate

**Temperature:**
- Product temperature: RTDs for accuracy (viscosity-temperature correlation)
- Equipment protection: Thermocouples cost-effective for alarms

**Source:** **ASSUMPTION** based on typical bulk liquid terminal instrumentation; **TBD**: Specific applications from P&IDs

## Trade-offs

**Trade-off: Standardization vs. Optimization**

- **Standardized instruments:** Fewer models/vendors, simplified procurement, reduced spare parts — may not be optimal for all applications
- **Optimized instruments:** Best-fit for each application — increased complexity, spare parts inventory

**Recommendation:** Standardize within instrument types (e.g., single manufacturer for all radar level transmitters); optimize for specialized applications (custody transfer, safety-critical).

**Source:** **ASSUMPTION** based on typical EPC instrumentation procurement strategy; supports OBJ-9 (Lifecycle Cost Optimization)

## Examples

**Example Data Sheet Content:**

```
Tag: LT-001
Service: Storage Tank #1 Level
P&ID: P-001
Range: 0-15 m
Accuracy: ±3 mm
Technology: Radar (26 GHz)
Output: 4-20 mA + HART
Enclosure: NEMA 4X, 316 SS
Hazardous Area: CSA Class I, Div 2, T3
Power: 24 VDC
Manufacturer: [Vendor to complete]
Model: [Vendor to complete]
Serial No: [As-built]
```

**Source:** **ASSUMPTION** — Example data sheet format

**Project Objective Alignment:** Supports **OBJ-1: Safe & Reliable Operation** and **OBJ-9: Lifecycle Cost Optimization**.

**Source:** Decomposition Section 6 (lines 780, 788)

## Cross-Document Traceability

This Guidance document provides engineering rationale for DEL-20.04. The following documents provide complementary information:

| Document | Purpose | Key Linkages |
|----------|---------|--------------|
| Datasheet.md | Factual identification, attributes, conditions, references | Conditions § explains data sheet purpose; Construction § provides instrument type examples |
| Specification.md | Requirements and verification criteria | FR-1 to FR-4 implement Principles; QR-1 to QR-3 implement quality approach |
| Procedure.md | Production workflow and verification steps | Steps 1-5 implement three-phase lifecycle per Principle 2 |

**Guidance-to-Specification Mapping:**

| Guidance Section | Specification Section | Rationale Provided |
|------------------|----------------------|-------------------|
| Principle 1 | INT-1 | Data sheets bridge design and procurement |
| Principle 2 | FR-1 to FR-4 | Three-phase lifecycle (design, procurement, as-built) |
| Principle 3 | PR-2 | Traceability requirements |
| Trade-off | Documentation | Standardization vs. optimization |
| Technical Considerations | FR-2 | Instrument-specific requirements |
