# Datasheet: DEL-15.03 Pump Design Calculations

## Identification

| Field | Value |
|-------|-------|
| Deliverable ID | DEL-15.03 |
| Name | Pump Design Calculations |
| Package | PKG-15 Pumps & Rotating Equipment |
| Discipline | Mechanical |
| Type | Calculation |
| Responsible | D&B Contractor |
| Status | INITIALIZED |

**Source:** `_CONTEXT.md`, decomposition DEL-15.03

## Attributes

### Calculation Metadata

| Attribute | Value |
|-----------|-------|
| Calculation Number | **TBD** — Per project calculation numbering system |
| Calculation Type | Pump sizing, NPSH, system curves (hydraulic design calculations) |
| Software Used | **TBD** — Excel, MathCAD, specialized pump software, or hand calculations |
| Design Code | API 610 (performance requirements), Fluid mechanics principles, Hydraulic system analysis |
| Load Cases | Operating conditions: normal, minimum flow, maximum flow, startup, shutdown |
| Revision | **ASSUMPTION**: Rev 0 for initial issue |
| Classification | **TBD** — Per project document classification system |
| Format | **ASSUMPTION**: Calculation report (PDF) with Excel/software attachments |

**Source:** Calculation type per deliverable classification; API 610 for pump performance requirements

### Calculation Scope

| Attribute | Value |
|-----------|-------|
| Equipment Covered | Railcar unloading pumps, marine loading pumps, sump pumps, transfer pumps (if applicable) |
| Calculation Purpose | Determine required pump flow, head, NPSH; support equipment specification (DEL-15.02) and selection |
| Design Responsibility | Hydraulic system design by Contractor; pump internal design by vendor per API 610 |
| Service | CSD canola oil transfer and handling |
| Facility Throughput | 1,000,000 MT/annum (OBJ-2) |

**Source:** `_CONTEXT.md` (anticipated artifacts), decomposition Section 2 (OBJ-2)

### Anticipated Calculation Deliverables

The calculations shall address the following:

| Calculation Document | Content |
|---------------------|---------|
| **Pump Sizing Calculations** | Required flow rate, total dynamic head (TDH), brake horsepower (BHP) for each pump service |
| **NPSH Calculations** | Net positive suction head available (NPSHA) at pump suction for worst-case conditions |
| **System Curves** | System head curve (flow vs. head) for each pump system; pump operating point selection |

**Source:** `_CONTEXT.md` (anticipated artifacts)

## Conditions

### Operating Context

**Facility parameters:**
- **Location:** Fraser Surrey Terminal, 11060 Elevator Road, Surrey, BC
- **Service:** CSD canola oil transload facility
- **Throughput:** 1,000,000 MT/annum (OBJ-2)
- **Storage capacity:** 45,000 MT (3 × 15,000 MT tanks) (OBJ-3)
- **Operations:** Tank storage and direct rail-to-ship transfer (OBJ-4)
- **Railcar capacity:** 32 railcar unloading stations

**Source:** Decomposition Section 1 (Project Overview), Section 2 (Objectives)

### Fluid Properties (CSD Canola Oil)

| Property | Value | Notes |
|----------|-------|-------|
| **Product** | Crush Seed Distillate (CSD) canola oil | Refined vegetable oil |
| **Specific Gravity** | **TBD** — Typically 0.91–0.92 @ 15°C | **ASSUMPTION**: Typical for canola oil; confirm from ER Part 2 |
| **Viscosity (kinematic)** | **TBD** — Typically 40–60 mm²/s @ 20°C | Temperature-dependent; affects friction losses |
| **Density** | **TBD** — Calculated from specific gravity (~910–920 kg/m³) | For head and power calculations |
| **Vapor Pressure** | **TBD** — Low (vegetable oil) | For NPSH calculations |
| **Operating Temperature Range** | **TBD** — Per ER Part 2 | **ASSUMPTION**: 10–50°C typical |

**Source:** **ASSUMPTION** — Typical canola oil properties; specific values TBD per ER Part 2 process data

### Design Conditions

| Condition | Value |
|-----------|-------|
| **Flow Rates** | **TBD** — Per process design (PKG-10, 11, 12) for each pump service |
| **Pressures** | **TBD** — Suction and discharge pressures for each pump service |
| **Temperatures** | **TBD** — Operating temperature range |
| **Elevation Data** | **TBD** — Site datum, equipment elevations, static heads |
| **Piping Layout** | **TBD** — Piping lengths, fittings, valves (from DEL-14 piping design) |

**Source:** Process design (PKG-10, 11, 12), piping design (DEL-14), site civil drawings (PKG-04, 05)

## Construction

### Calculation Methodology

#### Pump Sizing Methodology

**Required Flow Rate (Q):**
- Determined from process requirements (throughput, tank filling/emptying time, marine loading rate)
- May include margin for future expansion or operational flexibility
- **TBD** — Per process design and ER Part 2

**Total Dynamic Head (TDH):**
TDH = Static head + Friction losses + Equipment losses + Pressure head

Where:
- **Static head (Hs):** Elevation difference between suction and discharge liquid levels
- **Friction losses (Hf):** Piping friction (Darcy-Weisbach or Hazen-Williams equation), fittings and valves (K-factor method)
- **Equipment losses (He):** Heat exchangers, strainers, flow meters, control valves
- **Pressure head (Hp):** Pressure difference between suction and discharge vessels (if any)

**Brake Horsepower (BHP):**
BHP = (Q × TDH × SG) / (3,960 × η)  [US units: Q in GPM, TDH in ft]
BHP = (ρ × g × Q × TDH) / (η × 1,000)  [SI units: Q in m³/s, TDH in m, result in kW]

Where:
- η = pump efficiency (estimated from API 610 typical curves or vendor data)

**Source:** Fluid mechanics principles; API 610 Section 3 (hydraulic performance)

#### NPSH Calculation Methodology

**NPSH Available (NPSHA):**
NPSHA = Hatm + Hs - Hvp - Hf(suction)

Where:
- **Hatm:** Atmospheric pressure head (typically 10.3m at sea level)
- **Hs:** Static head at pump suction (positive if liquid level above pump centerline, negative if below)
- **Hvp:** Vapor pressure head of fluid at operating temperature
- **Hf(suction):** Friction losses in suction piping

**Worst-case NPSHA:** Calculate for worst-case conditions (lowest liquid level, highest temperature, longest suction piping).

**NPSH Requirement:** NPSHA must exceed vendor NPSHR by adequate margin (typically 0.5m minimum per API 610).

**Source:** API 610 Section 3 (NPSH requirements); fluid mechanics principles

#### System Curve Methodology

**System curve:** Plot of system head (TDH) vs. flow rate (Q)

System head equation:
H(Q) = Hs + K × Q²

Where:
- Hs = static head (constant)
- K = system resistance coefficient (from friction and equipment losses)
- Q = flow rate

**Pump operating point:** Intersection of pump head-flow curve (from vendor) and system curve. Operating point should be within pump preferred operating region (70–120% of best efficiency point).

**Source:** Hydraulic system analysis; API 610 Section 3 (performance requirements)

### Calculation Inputs

Calculation inputs required from other deliverables and sources:

| Input | Source | Status |
|-------|--------|--------|
| **Process flow rates** | PKG-10, 11, 12 (process design) | **TBD** |
| **Fluid properties** | ER Part 2 (process data) | **TBD** |
| **Piping layout and sizes** | DEL-14 (piping design) | **TBD** |
| **Equipment pressure drops** | Vendor data or typical values | **TBD** |
| **Elevation data** | Site civil drawings (PKG-04, 05) | **TBD** |
| **Tank levels** | DEL-13 (storage tanks) | **TBD** |

**Source:** Typical calculation input requirements

### Calculation Outputs

Calculation outputs to support other deliverables:

| Output | Recipient Deliverable | Purpose |
|--------|----------------------|---------|
| **Required flow and head** | DEL-15.02 (specification) | Equipment specification requirements |
| **NPSHA** | DEL-15.02 (specification) | NPSH margin verification |
| **System curves** | DEL-15.02 (specification), vendor selection | Pump operating point selection |
| **Pump power (BHP)** | DEL-15.02 (specification), Electrical discipline | Motor sizing |
| **Foundation loads** | DEL-15.01 (arrangement), PKG-05 (foundations) | Equipment weights and forces |

**Source:** Typical calculation output requirements

## References

### Primary References

- **Decomposition:** `/Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md` (Section 1: Project Overview, Section 2: Objectives, DEL-15.03 entry)
- **Context:** `_CONTEXT.md` (deliverable identity and anticipated artifacts)
- **Reference Index:** `PKG-15/0_References/_REFERENCE_INDEX.md`
- **Employer's Requirements:**
  - Volume 2 Part 1 (General Requirements) — **location TBD**
  - Volume 2 Part 2 (Civil & Process Mechanical Works) — **location TBD**: process requirements, fluid properties

### Applicable Standards and References

- **API 610** — Centrifugal Pumps for Petroleum, Petrochemical and Natural Gas Industries (Section 3: Hydraulic performance)
- **Crane Technical Paper No. 410** — Flow of Fluids Through Valves, Fittings, and Pipe (friction loss calculations)
- **Hydraulic Institute Standards** — Pump sizing and system analysis guidance
- **Cameron Hydraulic Data** — Fluid properties and hydraulic calculations reference
- **Perry's Chemical Engineers' Handbook** — Fluid properties and pump sizing methods

**Source:** Industry-standard references for pump hydraulic calculations

### Cross-References

- **DEL-15.01** — Pump Design Drawing Set (pump arrangement, elevations)
- **DEL-15.02** — Pump Technical Specification (receives calculation outputs: flow, head, NPSH, power)
- **DEL-15.04** — Pump Data Sheet Package (vendor data comparison to calculations)
- **DEL-15.05** — Pump Installation & Test Records (field performance test vs. calculated performance)
- **DEL-10.01–10.05** — Railcar Unloading System (railcar unloading pump requirements)
- **DEL-11.01–11.06** — Marine Loading System (marine loading pump requirements)
- **DEL-12.01–12.05** — Product Transfer & Metering (transfer pump requirements, metering pressure drop)
- **DEL-13.01–13.06** — Storage Tanks (tank levels, static heads)
- **DEL-14.01–14.08** — Process Piping (piping layout, sizes, friction losses)

**Source:** Dependencies inferred from deliverable scope and typical pump sizing workflow

---

**Document Status:** ENRICHED (Pass 1)
**Enrichment Date:** 2026-01-28
**Agent:** 4_DOCUMENTS enrichment cycle
