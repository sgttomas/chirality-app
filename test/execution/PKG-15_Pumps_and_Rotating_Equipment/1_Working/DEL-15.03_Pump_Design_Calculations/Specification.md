# Specification: DEL-15.03 Pump Design Calculations

## Scope

This specification defines the requirements for **Pump Design Calculations** within **PKG-15 Pumps & Rotating Equipment** for the Canola Oil Transload Facility at Fraser Surrey Terminal, Surrey, BC.

**Deliverable scope:** Provides the engineering basis and sizing/verification calculations for pumps per ER requirements.

**Source:** `_CONTEXT.md` (description), decomposition DEL-15.03 entry

### Purpose and Application

The Pump Design Calculations shall:

1. **Determine pump sizing requirements** — Required flow rate, total dynamic head (TDH), and brake horsepower (BHP) for each pump service
2. **Calculate NPSH available** — Net positive suction head available at pump suction for worst-case operating conditions
3. **Develop system curves** — System head vs. flow curves for pump selection and operating point determination
4. **Support equipment specification** — Provide technical basis for DEL-15.02 (Pump Technical Specification)
5. **Enable vendor evaluation** — Provide criteria to evaluate vendor pump proposals against system requirements

**Source:** Standard purpose of pump design calculations in EPC projects

### Calculations Covered

The calculations shall address the following pump services:

| Pump Service | Calculation Required |
|-------------|---------------------|
| **Railcar Unloading Pumps** | Sizing, NPSH, system curve |
| **Marine Loading Pumps** | Sizing, NPSH, system curve |
| **Sump Pumps** | Sizing, NPSH, system curve |
| **Transfer Pumps (if applicable)** | Sizing, NPSH, system curve |

**Source:** `_CONTEXT.md` (anticipated artifacts); pump services from DEL-15.02

### Included

- Fluid properties and operating conditions
- Flow rate determination (from process requirements and throughput objectives)
- Static head calculations (elevation differences)
- Friction loss calculations (piping, fittings, valves per Darcy-Weisbach or Hazen-Williams)
- Equipment pressure drop allowances (strainers, meters, heat exchangers, control valves)
- Total dynamic head (TDH) calculation
- NPSH available (NPSHA) calculation for worst-case conditions
- System resistance curves (head vs. flow)
- Pump power requirements (brake horsepower or kW)
- Pump operating point recommendations

**Source:** Standard pump sizing calculation content

### Excluded

- Pump internal design (vendor responsibility per API 610)
- Motor electrical design (Electrical discipline responsibility)
- Foundation structural design (Structural discipline responsibility per PKG-05)
- Piping detailed stress analysis (Piping discipline responsibility per DEL-14)

**Source:** Decomposition Section 1.2 (Scope Focus: Contractor scope only); typical discipline boundaries

## Requirements

### Functional Requirements

#### FR-1: Support Project Objectives

The pump calculations shall support:

- **OBJ-2 (Throughput Capacity):** Pump sizing to achieve 1,000,000 MT/annum facility throughput
- **OBJ-4 (Operational Flexibility):** Calculate for both tank storage and direct rail-to-ship transfer operating modes
- **OBJ-9 (Lifecycle Cost Optimization):** Size pumps for energy efficiency (operating near best efficiency point)

**Source:** Decomposition Section 2 (Objectives), Section 6 (Objective-Deliverable Mapping for PKG-15)

#### FR-2: Calculate Required Pump Performance

For each pump service, calculations shall determine:

| Parameter | Calculation Method | Output |
|-----------|-------------------|--------|
| **Flow Rate (Q)** | From process requirements and operating scenarios | m³/hr or L/s |
| **Static Head (Hs)** | Elevation difference between suction and discharge liquid levels | m |
| **Friction Losses (Hf)** | Darcy-Weisbach or Hazen-Williams equation for piping; K-factor for fittings/valves | m |
| **Equipment Losses (He)** | Manufacturer data or typical pressure drops for strainers, meters, control valves | m |
| **Total Dynamic Head (TDH)** | TDH = Hs + Hf + He + Hp (pressure head if applicable) | m |
| **NPSH Available** | NPSHA = Hatm + Hs(suction) - Hvp - Hf(suction) | m |
| **Pump Power (BHP)** | BHP = (Q × TDH × SG) / (3,960 × η) [US] or (ρ×g×Q×TDH)/(η×1000) [SI] | kW or HP |

**Source:** Fluid mechanics principles; API 610 Section 3 (hydraulic performance)

#### FR-3: Develop System Curves

Calculations shall produce system head vs. flow curves:

- **System curve equation:** H(Q) = Hs + K × Q²
- **Operating range:** Minimum flow to maximum flow (typically 0–120% of rated flow)
- **Pump operating point:** Intersection of pump curve (vendor) and system curve (calculated)
- **Verification:** Operating point within pump preferred operating region (70–120% of BEP per API 610)

**Source:** Hydraulic system analysis; API 610 Section 3

### Performance Requirements

#### PR-1: Calculation Accuracy

| Parameter | Accuracy Target | Method |
|-----------|----------------|--------|
| **Flow rates** | ±5% of process requirements | Use conservative process design values |
| **Static heads** | ±0.1m | Use surveyed elevations and tank drawings |
| **Friction losses** | ±10% | Use accepted correlations (Darcy-Weisbach, Crane TP-410) with appropriate pipe roughness |
| **NPSHA** | Conservative (worst-case conditions) | Use minimum liquid levels, maximum temperatures, maximum piping lengths |
| **System curve** | Representative of actual system | Include all significant pressure losses; document assumptions |

**Source:** Engineering practice for pump sizing calculations; conservative approach for NPSHA ensures adequate margin

#### PR-2: Design Margins and Safety Factors

| Item | Margin/Factor | Rationale |
|------|--------------|-----------|
| **Flow rate** | **TBD** — Typically 10–20% margin above process requirements | Account for future throughput increase, operational flexibility |
| **NPSH margin** | NPSHA must exceed vendor NPSHR by ≥0.5m (API 610 recommendation) | Prevent cavitation, ensure reliable operation |
| **Motor sizing** | Motor power ≥115% of pump BHP at rated flow (typical) | Provide adequate margin for startup, off-design operation |
| **Pipe roughness** | Use conservative values (e.g., ε = 0.046mm for commercial steel) | Account for fouling and aging |

**Source:** API 610 Section 3 (NPSH margin); industry practice for design margins

### Interface Requirements

#### IF-1: Process Design Interface

Calculations shall receive inputs from process design:

- Flow rates (normal, minimum, maximum) — from PKG-10, 11, 12
- Fluid properties (density, viscosity, vapor pressure) — from ER Part 2
- Operating temperatures — from process design
- Tank levels (normal, minimum) — from DEL-13

**Source:** Typical pump sizing input requirements; coordinate with process packages

#### IF-2: Piping Design Interface

Calculations shall receive inputs from piping design:

- Piping layout (lengths, elevations) — from DEL-14
- Pipe sizes and materials — from DEL-14
- Fittings and valves count and types — from DEL-14
- Equipment pressure drops (strainers, meters, control valves) — from vendor data or DEL-14

**Source:** Friction loss calculations require piping system geometry; coordinate with DEL-14

#### IF-3: Civil/Structural Interface

Calculations shall receive inputs from civil/structural design:

- Site datum and elevations — from PKG-04 (civil)
- Equipment mounting elevations — from DEL-15.01 (arrangement) and PKG-05 (foundations)

**Source:** Static head calculations require accurate elevation data

### Quality Requirements

#### QR-1: Calculation Standards

All calculations shall comply with:

- **Methodology:** Recognized fluid mechanics principles and correlations (Darcy-Weisbach, Hazen-Williams, Crane TP-410)
- **Units:** Consistent unit system (SI preferred; US customary acceptable if consistent)
- **Assumptions:** All assumptions clearly stated and justified
- **References:** All data sources, equations, and correlations properly cited
- **Checking:** Independent check by qualified engineer

**Source:** Engineering calculation standards; project quality requirements

#### QR-2: Calculation Documentation

Each calculation shall include:

1. **Cover sheet:** Project, deliverable ID, calculation title, author, checker, approver, date, revision
2. **Purpose and scope:** What is being calculated and why
3. **Design basis:** Codes, standards, references, design criteria
4. **Inputs:** All input data with sources
5. **Assumptions:** All assumptions clearly stated
6. **Methodology:** Equations, methods, software used
7. **Calculations:** Detailed calculations with intermediate results
8. **Results summary:** Key outputs clearly presented
9. **Conclusions and recommendations:** Operating point, NPSH margin, motor sizing recommendations
10. **Attachments:** Supporting data, software output, vendor data

**Source:** Standard engineering calculation format

#### QR-3: Calculation Software and Tools

- **Spreadsheet calculations:** Excel or equivalent — formulas visible and auditable
- **Specialized software:** **TBD** — Pump sizing software (if used) must be validated and documented
- **Hand calculations:** Acceptable for simple cases; must be legible and organized

**Source:** Engineering calculation practice

## Standards

### Primary Standards and References

- **API 610** — Centrifugal Pumps for Petroleum, Petrochemical and Natural Gas Industries (Section 3: Hydraulic performance, NPSH requirements)
- **Crane Technical Paper No. 410** — Flow of Fluids Through Valves, Fittings, and Pipe (standard reference for friction loss calculations)
- **Hydraulic Institute Standards** — Pump Application Guidelines
- **Cameron Hydraulic Data** — Fluid properties and hydraulic design data
- **Perry's Chemical Engineers' Handbook** — Fluid properties and transport phenomena

**Source:** Industry-standard references for pump hydraulic calculations

### Fluid Mechanics References

- **Darcy-Weisbach equation** — Pipe friction loss: hf = f × (L/D) × (V²/2g)
- **Hazen-Williams equation** — Alternative pipe friction loss method (for water and low-viscosity fluids)
- **Moody diagram** — Friction factor determination based on Reynolds number and relative roughness
- **K-factor method** — Minor losses for fittings and valves: hm = K × (V²/2g)

**Source:** Fluid mechanics textbooks and engineering handbooks

## Verification

### Calculation Verification Methods

| Verification Activity | Method | Acceptance Criteria |
|---------------------|--------|---------------------|
| **Input verification** | Review against source documents | Inputs match process design, piping layout, site data |
| **Methodology verification** | Review equations and correlations | Methods are appropriate and properly applied |
| **Results reasonableness** | Engineering judgment, comparison to similar systems | Results are within expected range for service |
| **Independent check** | Qualified checker performs sample calculations | Spot-check results agree within acceptable tolerance (±5%) |
| **Peer review** | Review by senior engineer not involved in calculations | Technical approach and conclusions are sound |

**Source:** Engineering calculation verification standards

### Vendor Data Comparison

After vendor pump proposals are received:

- Compare vendor NPSHR to calculated NPSHA — verify adequate margin (≥0.5m)
- Compare vendor pump curve to calculated system curve — verify operating point is within preferred region (70–120% of BEP)
- Compare vendor pump power to calculated BHP — verify motor sizing is adequate

**Source:** Standard pump selection verification process; coordinate with DEL-15.04 (vendor data review)

### Field Performance Test Comparison

After installation and commissioning:

- Compare field-measured flow, pressure, power to calculated values
- Investigate discrepancies >10%
- Update calculations if actual system differs significantly from design assumptions

**Source:** Standard commissioning verification; coordinate with DEL-15.05 (performance test records)

## Documentation

### Calculation Document Deliverables

The following calculation documents shall be produced:

1. **Pump Sizing Calculations** — Flow, head, power for all pump services (may be combined document or separate per service)
2. **NPSH Calculations** — NPSH available for worst-case conditions for all pump services
3. **System Curves** — System head vs. flow curves for pump selection (may be included in sizing calculations)

**Source:** `_CONTEXT.md` (anticipated artifacts)

### Calculation Format

Each calculation shall be formatted per project calculation standards:
- **Document:** PDF calculation report with cover sheet, table of contents, body, attachments
- **Attachments:** Excel spreadsheets, software files, vendor data references
- **Revisions:** Revision log showing changes from previous revisions

**Source:** Standard engineering calculation format; project document control standards (TBD)

### Record Management

- **Filing location:** `1_Working/DEL-15.03_Pump_Design_Calculations/` during development; `2_Checking/` during review; `3_Issued/` upon approval
- **Revision control:** Per project document control procedures — **TBD**
- **Retention:** Per ER Part 1 requirements — **TBD** — **ASSUMPTION**: Minimum 25 years (typical for engineering calculations)

**Source:** Project document control procedures (TBD)

---

**Document Status:** ENRICHED (Pass 1)
**Enrichment Date:** 2026-01-28
**Agent:** 4_DOCUMENTS enrichment cycle

**Cross-References:**
- Datasheet.md — Calculation methodology, inputs, outputs
- Guidance.md — Calculation principles, best practices, common issues
- Procedure.md — Step-by-step process for performing calculations
- DEL-15.01 — Pump Design Drawing Set (receives pump arrangement and elevation data)
- DEL-15.02 — Pump Technical Specification (receives calculation outputs: flow, head, NPSH, power)
- DEL-15.04 — Pump Data Sheet Package (vendor data verification against calculations)
- DEL-15.05 — Pump Installation & Test Records (field test comparison to calculations)
