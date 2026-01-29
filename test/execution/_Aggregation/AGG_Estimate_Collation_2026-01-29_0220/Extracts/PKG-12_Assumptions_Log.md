# Assumptions Log

## Snapshot Identification

| Field | Value |
|-------|-------|
| Snapshot ID | EST_PKG12_DRAFT_2026-01-28_2341 |
| Estimate Label | PKG12_DRAFT |
| Package | PKG-12 Product Transfer & Metering |
| Date | 2026-01-28 |

---

## Equipment Quantities

### A-001: Flow Meter Quantity (2 Units)

**Statement:** Two custody transfer flow meters required: one for rail unloading, one for marine loading

**Why Needed:** Metering configuration not explicitly specified; typical custody transfer practice for dual-service installations

**Impacted WBS/CBS:** PKG-12 / MAT, CD, COM

**Cost Impact:** $300k-500k (2 meters @ $150k-250k/unit)

**Confidence:** MED

**Resolution Path:** Confirm in DEL-12.01 drawings and DEL-12.02 specification whether rail and marine use separate meters or shared/manifolded configuration

---

### A-002: Flow Meter Technology (Coriolis Mass Flowmeter)

**Statement:** Assume Coriolis mass flowmeter technology for both rail and marine custody transfer meters

**Why Needed:** Technology not selected in INITIALIZED deliverables; custody transfer accuracy requirement suggests Coriolis

**Impacted WBS/CBS:** PKG-12 / MAT, CD

**Cost Impact:** $300k-500k for 2 Coriolis meters; range reflects meter size uncertainty

**Range:** Coriolis $150k-250k/unit; ultrasonic $80k-150k/unit; turbine $30k-80k/unit; positive displacement $50k-120k/unit

**Confidence:** LOW (technology selection materially affects cost and performance)

**Resolution Path:** Confirm meter technology in DEL-12.02 specification based on accuracy requirements, product properties, flow range, and proving method

---

### A-003: Flow Meter Sizes

**Statement:** Rail unloading meter: 6" (150mm); Marine loading meter: 10" (250mm)

**Why Needed:** Flow rates not specified; meter sizes parametrically estimated from throughput and typical flow velocities

**Basis:**
- Facility throughput: 1,000,000 MT/a (Decomposition:41)
- Rail unloading: 32 stations (Decomposition:44); typical railcar unloading rate 50-100 m³/h/station
- Marine loading: High flow for vessel loading; typical bulk vegetable oil loading 500-2000 m³/h
- Meter sizing for 1-5 m/s velocity range typical for liquid flowmeters

**Impacted WBS/CBS:** PKG-12 / MAT, CD

**Cost Impact:** Affects meter cost (larger meters cost more); 6" meter ~$150k-200k, 10" meter ~$200k-250k

**Confidence:** LOW

**Resolution Path:** Obtain design flow rates from ER Vol 2 Part 2 or from PKG-10/PKG-11 calculations; perform meter sizing calculation in DEL-12.03

---

### A-004: Temperature Transmitters (4 Units)

**Statement:** Four temperature transmitters: 2 for rail unloading (inlet/outlet or redundancy), 2 for marine loading

**Why Needed:** Transmitter count not specified; typical custody transfer metering includes temperature compensation

**Impacted WBS/CBS:** PKG-12 / MAT, CD

**Cost Impact:** $16k-32k (4 units @ $4k-8k/unit for RTD Pt100 transmitters with HART)

**Confidence:** MED

**Resolution Path:** Confirm transmitter count and configuration in DEL-12.02 specification and DEL-12.04 data sheets

---

### A-005: Pressure Transmitters (2 Units)

**Statement:** Two pressure transmitters: 1 for rail unloading, 1 for marine loading

**Why Needed:** Transmitter count not specified; pressure compensation may be required for accuracy (though vegetable oil compressibility is low)

**Impacted WBS/CBS:** PKG-12 / MAT, CD

**Cost Impact:** $6k-12k (2 units @ $3k-6k/unit for process pressure transmitters)

**Confidence:** LOW

**Resolution Path:** Confirm whether pressure compensation is required in DEL-12.02 specification based on accuracy budget in DEL-12.03; pressure compensation may not be needed if Coriolis mass meters used

---

### A-006: Metering Skid Structural Supports

**Statement:** Structural supports for metering skids sized for 6" and 10" meter runs with access platforms

**Why Needed:** Skid size and complexity not detailed; typical metering installations include skid-mounted arrangements

**Impacted WBS/CBS:** PKG-12 / MAT (structural steel for skid), CD (skid fabrication/assembly)

**Cost Impact:** $50k-80k for structural supports and platforms (coordinate with PKG-06)

**Confidence:** LOW

**Resolution Path:** Obtain metering skid GA from DEL-12.01 drawings with structural requirements; coordinate with PKG-06 for structural design

---

### A-007: Meter Run Piping Allowance

**Statement:** Meter run piping includes straight-run sections upstream/downstream of meters (typical 10D upstream, 5D downstream)

**Why Needed:** Straight-run requirements not specified; typical custody transfer meter installation standards

**Basis:**
- Typical straight-run requirements: 10D upstream, 5D downstream for Coriolis meters
- 6" meter: 10D = 60" (1.5m) upstream, 5D = 30" (0.75m) downstream
- 10" meter: 10D = 100" (2.5m) upstream, 5D = 50" (1.25m) downstream

**Impacted WBS/CBS:** PKG-12 / MAT (piping material), CD (piping installation)

**Cost Impact:** $30k-50k for meter run piping (material + installation)

**Confidence:** MED

**Resolution Path:** Confirm straight-run requirements in DEL-12.02 specification and DEL-12.03 calculations based on meter manufacturer requirements

---

### A-008: Proving Equipment (Portable Prover)

**Statement:** One portable prover system sized for both rail and marine meter proving

**Why Needed:** Proving method not selected; portable prover typical for dual-service installations

**Impacted WBS/CBS:** PKG-12 / MAT, COM

**Cost Impact:** $100k-150k for portable prover with traceability and certification

**Range:** In-line provers $150k-250k each (×2 for rail and marine); master meter $50k-80k + periodic calibration costs

**Confidence:** LOW

**Resolution Path:** Confirm proving method in DEL-12.02 specification; if in-line provers specified, increase MAT by ~$200k-350k

---

### A-009: Temperature Compensation Requirement

**Statement:** Temperature compensation is required for custody transfer accuracy; temperature transmitters measure product temperature for volume-to-mass or density correction

**Why Needed:** Compensation method not specified; typical custody transfer practice

**Impacted WBS/CBS:** PKG-12 / MAT (transmitters), E (calculations)

**Cost Impact:** Included in transmitter costs (A-004); affects accuracy budget calculations in DEL-12.03

**Confidence:** HIGH (temperature compensation is standard for custody transfer)

**Resolution Path:** Confirm in DEL-12.02 specification and DEL-12.03 uncertainty calculations

---

### A-010: Density Measurement Method

**Statement:** If Coriolis meters used, density is measured integrally (no separate densitometers); if other technology, density compensation method TBD

**Why Needed:** Density measurement method not specified

**Impacted WBS/CBS:** PKG-12 / MAT

**Cost Impact:** Coriolis meters include integral density (no additional cost); separate densitometers would add ~$30k-60k/unit if required

**Confidence:** MED

**Resolution Path:** Confirm in DEL-12.02 specification based on meter technology and accuracy requirements

---

## Engineering Effort

### A-011: DEL-12.01 Engineering Effort (Drawing Set)

**Statement:** Metering design drawing set estimated at $28,000

**Why Needed:** No project-specific engineering rates or effort estimates available

**Basis:**
- Typical custody transfer metering GA set: 3-6 sheets
- Flow meter installation details: 2-4 sheets
- Proving connection details: 1-2 sheets
- Total 6-12 sheets estimated; ~$2k-4k/sheet for process GA/detail drawings

**Impacted WBS/CBS:** PKG-12 / E

**Cost Impact:** $28,000

**Confidence:** LOW

**Resolution Path:** Provide engineering rate table or effort estimates; progress DEL-12.01 to IN_PROGRESS to define drawing scope

---

### A-012: DEL-12.02 Engineering Effort (Specification)

**Statement:** Metering technical specification estimated at $38,000

**Why Needed:** No project-specific engineering rates or effort estimates available

**Basis:**
- Typical custody transfer metering specification: 30-50 pages (DEL-12.02 Datasheet.md line 24)
- Includes flow meter specification, metering system specification, proving requirements, QA requirements
- Estimated effort: 200-300 engineering hours @ ~$140/hr (process engineer rate typical)

**Impacted WBS/CBS:** PKG-12 / E

**Cost Impact:** $38,000

**Confidence:** LOW

**Resolution Path:** Provide engineering rate table and effort estimates; progress DEL-12.02 to IN_PROGRESS

---

### A-013: DEL-12.03 Engineering Effort (Calculations)

**Statement:** Metering design calculations estimated at $42,000

**Why Needed:** No project-specific engineering rates or effort estimates available

**Basis:**
- Flow meter sizing (2 services), accuracy/uncertainty analysis (uncertainty budget development per API MPMS Chapter 13 or OIML R117), proving calculations
- Estimated effort: 250-350 hours @ ~$140/hr for process/measurement engineer
- Includes sensitivity analysis, vendor coordination, methodology documentation

**Impacted WBS/CBS:** PKG-12 / E

**Cost Impact:** $42,000

**Confidence:** LOW

**Resolution Path:** Provide engineering rate table; progress DEL-12.03 to IN_PROGRESS with defined calculation scope

---

### A-014: DEL-12.04 Engineering Effort (Data Sheets)

**Statement:** Metering data sheet package estimated at $18,000

**Why Needed:** No project-specific engineering rates or effort estimates available

**Basis:**
- Minimum 4 data sheets: flow meters (×2), temperature transmitters, pressure transmitters (DEL-12.04 Datasheet.md line 24)
- Additional data sheets if density transmitters, proving equipment, flow computers
- Estimated effort: 120-150 hours @ ~$140/hr for data sheet development, vendor data incorporation, cross-checks

**Impacted WBS/CBS:** PKG-12 / E

**Cost Impact:** $18,000

**Confidence:** LOW

**Resolution Path:** Provide engineering rate table; confirm data sheet count in DEL-12.04

---

### A-015: DEL-12.05 Engineering Effort (Test Records)

**Statement:** Metering installation & test records estimated at $12,000

**Why Needed:** No project-specific QA/QC rates available

**Basis:**
- QA/QC record compilation, calibration certificate review, proving record development, traceability mapping
- Estimated effort: 80-100 hours @ ~$140/hr for QA engineer
- Includes FAT/SAT coordination, record archiving, regulatory compliance documentation

**Impacted WBS/CBS:** PKG-12 / E

**Cost Impact:** $12,000

**Confidence:** LOW

**Resolution Path:** Provide QA/QC rate table; confirm record scope in DEL-12.05 and ER requirements

---

## Materials and Equipment

### A-016: Custody Transfer Flow Meter Cost (Rail Unloading)

**Statement:** Rail unloading custody transfer flow meter: $180,000 (6" Coriolis mass flowmeter)

**Why Needed:** No vendor quotes available; meter cost estimated from typical custody transfer Coriolis pricing

**Basis:**
- Coriolis mass flowmeter 6" (150mm) for custody transfer service
- Typical cost range: $150k-200k for custody transfer Coriolis with integral density, temperature, HART/Modbus communication, Measurement Canada approval (if required)
- Midpoint estimate: $180k

**Impacted WBS/CBS:** PKG-12 / MAT

**Cost Impact:** $180,000

**Range:** $150k-200k depending on vendor, accuracy class, features, certifications

**Confidence:** LOW

**Resolution Path:** Obtain budgetary quotes from Emerson (Micro Motion), Endress+Hauser (Proline Promass), Krohne (Optimass), or other custody transfer meter suppliers

---

### A-017: Custody Transfer Flow Meter Cost (Marine Loading)

**Statement:** Marine loading custody transfer flow meter: $230,000 (10" Coriolis mass flowmeter)

**Why Needed:** No vendor quotes available; meter cost estimated from typical custody transfer Coriolis pricing

**Basis:**
- Coriolis mass flowmeter 10" (250mm) for custody transfer service
- Typical cost range: $200k-250k for large custody transfer Coriolis
- Midpoint estimate: $230k

**Impacted WBS/CBS:** PKG-12 / MAT

**Cost Impact:** $230,000

**Range:** $200k-250k

**Confidence:** LOW

**Resolution Path:** Obtain budgetary quotes from custody transfer metering suppliers

---

### A-018: Temperature Transmitters (4 Units @ $6k/unit)

**Statement:** Four temperature transmitters @ $6,000/unit = $24,000

**Why Needed:** No vendor quotes; typical RTD Pt100 transmitter pricing

**Basis:**
- RTD Pt100 Class A sensors with 4-20mA + HART output
- Process-grade transmitter with custody transfer accuracy (~±0.1°C)
- Typical cost: $4k-8k/unit installed; midpoint $6k

**Impacted WBS/CBS:** PKG-12 / MAT

**Cost Impact:** $24,000

**Confidence:** MED

**Resolution Path:** Obtain quotes from Emerson (Rosemount), Endress+Hauser, or other transmitter suppliers; confirm transmitter count in DEL-12.04

---

### A-019: Pressure Transmitters (2 Units @ $5k/unit)

**Statement:** Two pressure transmitters @ $5,000/unit = $10,000

**Why Needed:** No vendor quotes; typical process pressure transmitter pricing

**Basis:**
- Process pressure transmitter 0-10 bar range (typical)
- ±0.1% accuracy, 4-20mA + HART output
- Typical cost: $3k-6k/unit; midpoint $5k

**Impacted WBS/CBS:** PKG-12 / MAT

**Cost Impact:** $10,000

**Confidence:** MED

**Resolution Path:** Obtain quotes; confirm whether pressure compensation is required in DEL-12.02 specification and DEL-12.03 accuracy budget

---

### A-020: Portable Prover System

**Statement:** Portable prover system with traceability and Measurement Canada certification: $120,000

**Why Needed:** Proving method not selected; portable prover assumed per D-004

**Basis:**
- Portable prover for custody transfer proving (volumetric or gravimetric)
- Capacity suitable for 6" and 10" meters
- Includes prover, transport cart, connection hoses/fittings, calibration certificate with traceability
- Typical cost: $100k-150k; midpoint $120k

**Impacted WBS/CBS:** PKG-12 / MAT

**Cost Impact:** $120,000

**Range:** Portable prover $100k-150k; in-line prover (×2) $300k-500k; master meter $50k-80k

**Confidence:** LOW

**Resolution Path:** Confirm proving method in DEL-12.02 specification; if in-line provers specified, replace this allowance with in-line prover costs

---

### A-021: Metering Skid Structural Steel

**Statement:** Structural steel for metering skids (rail and marine): $55,000

**Why Needed:** Skid design not detailed; structural requirements estimated

**Basis:**
- Two metering skids: rail unloading skid (6" meter run), marine loading skid (10" meter run)
- Structural steel for meter supports, access platforms, stairs, handrails
- Estimated material: 8-12 tonnes @ $5k-7k/tonne fabricated/delivered
- Midpoint: $55k

**Impacted WBS/CBS:** PKG-12 / MAT (coordinate with PKG-06)

**Cost Impact:** $55,000

**Confidence:** LOW

**Resolution Path:** Obtain metering skid GA from DEL-12.01; coordinate structural design with PKG-06; obtain fabrication quotes

---

### A-022: Meter Run Piping (Material)

**Statement:** Meter run piping (stainless steel) for straight-run sections: $35,000

**Why Needed:** Piping design not detailed; straight-run lengths estimated from typical requirements

**Basis:**
- 6" SS316L piping for rail meter: ~3m straight-run @ $300-400/m
- 10" SS316L piping for marine meter: ~4m straight-run @ $500-700/m
- Includes flanges, gaskets, supports
- Total material: ~$35k

**Impacted WBS/CBS:** PKG-12 / MAT (coordinate with PKG-14 for piping material specs)

**Cost Impact:** $35,000

**Confidence:** MED

**Resolution Path:** Confirm straight-run requirements in DEL-12.03; coordinate with PKG-14 for piping material and installation

---

### A-023: Metering System Installation Consumables

**Statement:** Installation consumables (gaskets, fasteners, welding materials, sealants, calibration fluids): $15,000

**Why Needed:** Consumables not itemized; typical allowance for metering installation

**Impacted WBS/CBS:** PKG-12 / MAT

**Cost Impact:** $15,000

**Confidence:** MED

**Resolution Path:** Refine based on detailed installation scope in Procedure.md and DEL-12.01 drawings

---

### A-031: Flow Computers / Totalizers (2 Units @ $18k/unit)

**Statement:** Two flow computers/totalizers @ $18,000/unit = $36,000

**Why Needed:** Flow computer/totalizer scope not defined; may be dedicated units or integrated in PKG-19 control system

**Basis:**
- Custody transfer totalizing computers (1 for rail, 1 for marine)
- Typical cost: $15k-25k/unit for custody transfer flow computer with totalizing, data logging, communication
- Midpoint: $18k/unit

**Impacted WBS/CBS:** PKG-12 / MAT (may shift to PKG-19 if DCS integration)

**Cost Impact:** $36,000

**Range:** Dedicated flow computers $36k; or scope shifts to PKG-19 DCS totalizing (reduces PKG-12 MAT by $36k)

**Confidence:** LOW

**Resolution Path:** Coordinate with PKG-19 on control system architecture; confirm whether dedicated flow computers (PKG-12) or DCS integration (PKG-19) in DEL-12.02 specification

---

### A-032: Junction Boxes and Marshalling

**Statement:** Junction boxes and instrument marshalling panels for metering system: $12,000

**Why Needed:** Electrical/instrumentation infrastructure not detailed

**Basis:**
- Junction boxes for metering instrumentation
- Marshalling panels if required (coordinate with PKG-20)
- Typical allowance for metering system electrical/instrument infrastructure

**Impacted WBS/CBS:** PKG-12 / MAT (coordinate with PKG-20)

**Cost Impact:** $12,000

**Confidence:** MED

**Resolution Path:** Coordinate with PKG-20 on field instrumentation marshalling; confirm in DEL-12.01 drawings and PKG-20 specification

---

## Construction Labor

### A-024: Metering System Installation Labor

**Statement:** Installation labor for metering systems (meter installation, piping, electrical/instrument connections): 2,400 manhours @ $120/hr all-in = $288,000

**Why Needed:** No project labor rates or installation work breakdown available

**Basis:**
- Flow meter installation (2 units): 200-300 hrs/unit (rigging, alignment, connection, testing)
- Meter run piping installation: 300-400 hrs (welding, NDT, pressure testing)
- Skid assembly and setting: 200-300 hrs
- Electrical/instrument connections: 300-400 hrs (wiring, terminations, junction boxes)
- Transmitter installation: 40-60 hrs/unit × 6 units
- Access platforms/stairs: 150-200 hrs
- Total: ~2,000-2,800 hrs; midpoint 2,400 hrs

**Impacted WBS/CBS:** PKG-12 / CD

**Cost Impact:** $288,000

**Confidence:** LOW

**Resolution Path:** Provide project labor rates; develop detailed installation work breakdown in Procedure.md; coordinate with PKG-14, PKG-17, PKG-19, PKG-20 for interface installation scope

---

### A-025: Survey and Setting Out

**Statement:** Survey and setting out for metering skid installation: 40 manhours @ $120/hr = $5,000

**Why Needed:** Survey scope not detailed; typical allowance for equipment setting

**Impacted WBS/CBS:** PKG-12 / CD

**Cost Impact:** $5,000

**Confidence:** MED

**Resolution Path:** Confirm survey requirements in construction procedures

---

### A-026: Specialist Installation Equipment

**Statement:** Specialty tools and equipment for meter installation (lifting, alignment, torque tools): $18,000

**Why Needed:** Equipment requirements not detailed

**Basis:**
- Crane/hoist for meter handling
- Alignment tools for meter installation
- Torque wrenches for flanges
- Welding equipment (if not in general construction equipment)
- Typical allowance for precision installation equipment

**Impacted WBS/CBS:** PKG-12 / CD

**Cost Impact:** $18,000

**Confidence:** MED

**Resolution Path:** Develop detailed installation equipment list in Procedure.md

---

## Commissioning and Testing

### A-027: Factory Acceptance Test (FAT)

**Statement:** FAT for custody transfer flow meters (2 units): $32,000

**Why Needed:** FAT requirements not specified; typical for custody transfer equipment

**Basis:**
- FAT at vendor facility for 2 flow meters
- FAT includes flow testing at multiple points, accuracy verification, signal testing
- Estimated effort: 80-120 hrs vendor/contractor time @ $200-300/hr (includes vendor FAT engineer + contractor witness)
- Travel/expenses for witness: $8k-12k
- Midpoint: $32k

**Impacted WBS/CBS:** PKG-12 / COM

**Cost Impact:** $32,000

**Confidence:** LOW

**Resolution Path:** Confirm FAT requirements in DEL-12.02 specification and ER Vol 2 Part 2; may not be required if shop calibration certificate sufficient

---

### A-028: Site Acceptance Test (SAT)

**Statement:** SAT for installed metering system (2 services): $28,000

**Why Needed:** SAT requirements not specified; typical for custody transfer systems

**Basis:**
- Functional testing of installed meters
- Signal verification, communication testing, totalizer verification
- Integration testing with control system (PKG-19)
- Estimated effort: 200-250 hrs @ $120/hr (contractor) + specialist support

**Impacted WBS/CBS:** PKG-12 / COM

**Cost Impact:** $28,000

**Confidence:** LOW

**Resolution Path:** Confirm SAT scope and acceptance criteria in DEL-12.02 specification

---

### A-029: Initial Proving (Commissioning)

**Statement:** Initial proving for 2 custody transfer meters: $48,000

**Why Needed:** Proving scope not detailed; initial proving typical for custody transfer commissioning

**Basis:**
- Initial proving to establish baseline meter factor for each meter
- Multiple proving runs per meter (typically 5-10 runs for repeatability verification)
- Proving equipment setup, operation, data collection
- Estimated effort: 300-400 hrs @ $120/hr including proving specialist
- Includes proving equipment mobilization and setup

**Impacted WBS/CBS:** PKG-12 / COM

**Cost Impact:** $48,000

**Confidence:** LOW

**Resolution Path:** Confirm proving methodology and run count in DEL-12.03 calculations; obtain proving service quotes

---

### A-030: Calibration and Documentation

**Statement:** Final calibration verification and record compilation: $12,000

**Why Needed:** QA/QC effort not detailed

**Basis:**
- Calibration certificate review and verification
- Record package compilation per DEL-12.05
- Estimated effort: 80-100 hrs @ $120/hr for QA engineer

**Impacted WBS/CBS:** PKG-12 / COM

**Cost Impact:** $12,000

**Confidence:** MED

**Resolution Path:** Confirm record requirements in DEL-12.05 and ER Vol 2 Part 1 QA requirements

---

## Summary

| Assumption Count | 32 |
|------------------|-----|
| Equipment Quantities | A-001 through A-010 |
| Engineering Effort | A-011 through A-015 |
| Materials/Equipment | A-016 through A-023, A-031, A-032 |
| Construction Labor | A-024 through A-026 |
| Commissioning/Testing | A-027 through A-030 |

### Assumptions by Confidence

| Confidence | Count | % of Total |
|------------|-------|------------|
| LOW | 20 | 62.5% |
| MED | 12 | 37.5% |
| HIGH | 0 | 0% |

### Top Assumptions by Cost Impact

| Rank | Assumption | Cost Impact | Resolution |
|------|------------|-------------|------------|
| 1 | A-016, A-017: Flow meter costs | $410,000 | Obtain vendor quotes for custody transfer Coriolis meters |
| 2 | A-024: Installation labor | $288,000 | Provide labor rates and detailed installation work breakdown |
| 3 | A-008, A-020: Portable prover | $120,000 | Confirm proving method; obtain prover quotes |
| 4 | A-027, A-028, A-029: FAT/SAT/Proving | $108,000 | Define testing scope in DEL-12.02; obtain testing/proving service quotes |
| 5 | A-021: Skid structural steel | $55,000 | Develop skid design in DEL-12.01; coordinate with PKG-06 |

---

*Assumptions log prepared per AGENT_ESTIMATING SPEC requirements. All allowances and uncertainties documented with resolution paths.*
