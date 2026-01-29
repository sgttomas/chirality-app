# Guidance: DEL-16.04 Valve Data Sheet Package

## Purpose

This guidance document supports the development of **Valve Data Sheet Package** for **PKG-16 Valves & Specialty Equipment**.

**Deliverable Purpose:** Defines and substantiates individual valve selections per ER requirements for the Canola Oil Transload Facility.

**Source:** `_CONTEXT.md`

**Deliverable Classification:**
- **Type:** Data Sheet
- **Discipline:** Mechanical
- **Responsible Party:** D&B Contractor

**Project Context:**
This deliverable supports **OBJ-1: Safe & Reliable Operation** by providing comprehensive valve data that ensures correct valve selection, procurement, installation, and operation throughout the facility design life.

**Source:** Decomposition document Section 6 (Objective-to-Deliverable Mapping), OBJ-1 includes PKG-16 (DEL-16.01–DEL-16.05)

## Principles

**Engineering Rationale:**

**1. Datasheet Purpose and Function**

Valve datasheets serve as the single-source technical specification for each individual valve, bridging design calculations, procurement specifications, and operational requirements (see also Specification.md — Functional Requirements for datasheet content):

**Key Functions:**
- **Design Documentation:** Consolidates design decisions (valve type, size, materials) in one location
- **Procurement Tool:** Provides vendor with complete technical requirements for quotation and fabrication
- **Installation Reference:** Guides construction personnel on correct valve installation and orientation
- **Operational Reference:** Provides operators with valve performance data (Cv, set pressure, fail-safe mode)
- **Maintenance Reference:** Supports maintenance planning (trim material, actuator type, spare parts)

**Datasheet vs. Specification vs. Calculation:**
- **Specification (DEL-16.02):** General requirements applicable to all valves of a type (e.g., "all control valves shall have stainless steel trim")
- **Calculation (DEL-16.03):** Engineering analysis determining valve size, Cv, set pressure (e.g., "FV-1234 requires Cv = 75.8")
- **Datasheet (DEL-16.04):** Individual valve application of specification and calculation (e.g., "FV-1234: DN 80 globe valve, 316SS body/trim, Cv = 100, pneumatic spring-return actuator")

**Source:** Datasheet function in EPC project lifecycle; relationship to other deliverables

**2. Datasheet Development Philosophy**

Datasheets are developed iteratively as design progresses (see also Procedure.md — Steps for development workflow):

**Design Stage Progression:**

**30% Design (Preliminary):**
- Valve types and approximate sizes based on preliminary process design
- Conservative material selections
- Preliminary actuator types (pneumatic vs. electric)
- **Purpose:** Early identification of long-lead equipment; preliminary cost estimation

**60% Design (Intermediate):**
- Refined valve sizes based on detailed calculations (DEL-16.03)
- Confirmed materials based on service conditions
- Detailed actuator sizing with safety factors
- Preliminary vendor selection (pre-qualified vendors)
- **Purpose:** Basis for vendor inquiry; detailed cost estimation

**90% Design (Advanced):**
- Final valve sizes and specifications
- All TBD items resolved
- Ready for procurement (Issued for Procurement)
- **Purpose:** Final technical basis for vendor bidding

**Post-Procurement (As-Built):**
- Vendor-supplied data incorporated (actual Cv, serial numbers, test results)
- Datasheets updated to reflect actual installed valves
- **Purpose:** As-Built record for operation and maintenance

**Source:** Typical EPC design stage progression; datasheet maturity increases with design maturity

**3. Control Valve Datasheet Principles**

**Valve Type Selection (Globe vs. Ball vs. Butterfly):**

**Globe Valves (Most Common for Control Service):**
- **Advantages:** Excellent control characteristics; high rangeability (50:1 typical); wide variety of trim options (equal percentage, linear, anti-cavitation)
- **Disadvantages:** Higher pressure drop; larger and heavier than ball/butterfly
- **Use for:** Precise flow control; high differential pressure; cavitating service (with anti-cavitation trim)
- **Typical for Canola Oil Facility:** Product transfer flow control; tank level control

**Ball Valves (Segmented Ball for Control):**
- **Advantages:** Compact; lower pressure drop than globe; tight shutoff (Class VI)
- **Disadvantages:** Limited rangeability (30:1 typical); prone to cavitation erosion
- **Use for:** On/off control with some throttling; clean service; fire-safe requirements
- **Typical for Canola Oil Facility:** Isolation service (on/off); some throttling applications

**Butterfly Valves (High-Performance for Control):**
- **Advantages:** Very compact; low pressure drop; economical for large sizes (>NPS 8)
- **Disadvantages:** Limited rangeability (20:1 typical); poor control at high Cv (>90% open)
- **Use for:** Large diameter control; low pressure drop applications
- **Typical for Canola Oil Facility:** Large product lines (NPS 10 and above) where pressure drop is limited

**Source:** Control valve type selection principles; typical applications for liquid service

**Trim Characteristic Selection (Equal Percentage vs. Linear):**

**Equal Percentage (Most Common):**
- Flow change proportional to valve travel at constant ΔP
- Provides near-linear installed characteristic when system pressure drop varies with flow
- **Use for:** Most flow control applications; liquid level control
- **Rangeability:** 50:1 typical

**Linear:**
- Flow change linear with valve travel at constant ΔP
- Provides good control when valve pressure drop is constant (large % of system ΔP)
- **Use for:** Pressure control; applications where valve consumes most of system ΔP
- **Rangeability:** 30:1 typical

**Quick-Opening:**
- Maximum flow change at low travel; minimal change at high travel
- **Use for:** On/off service; safety shutdown valves
- **Rangeability:** 10:1 typical

**Recommendation for Canola Oil Facility:** Use equal percentage trim for most control valves; use linear trim only for pressure control applications where justified by analysis

**Source:** ISA-75.11 flow characteristic selection principles

**4. Relief Valve Datasheet Principles**

**Set Pressure and Overpressure Allowance:**

Per ASME Section VIII and CSA B51, relief valves must be set and sized to prevent overpressure beyond code limits:

**Operating Case (Normal Overpressure Events):**
- Set pressure: ≤ MAWP
- Accumulated pressure during relief: ≤ 1.10× MAWP (10% overpressure)
- **Examples:** Thermal expansion, blocked discharge, control valve failure

**Fire Case (External Fire Scenario):**
- Set pressure: ≤ MAWP
- Accumulated pressure during relief: ≤ 1.21× MAWP (21% overpressure)
- **Example:** Storage tank external fire per API 521

**Set Pressure Tolerance (per API 526):**
- Pressures ≤ 70 psig: ±3 psi
- Pressures > 70 psig: ±2% of set pressure

**Cold Differential Test Pressure (CDTP):**
- Set pressure adjusted for temperature effects during bench testing
- CDTP = Set Pressure × (K_test / K_operating) where K = spring constant at temperature
- Manufacturer provides CDTP for shop testing

**Source:** ASME Section VIII UG-125 through UG-136; API 526/527; CSA B51 Section 4.11

**Orifice Designation (API 526 Standard Orifices):**

API 526 defines standard orifice sizes to promote interchangeability and reduce inventory:

| Orifice | Area (mm²) | Area (in²) | Typical Inlet Size |
|---------|------------|------------|-------------------|
| D | 71 | 0.110 | 3/4" × 1" |
| E | 126 | 0.196 | 1" × 1.5" |
| F | 198 | 0.307 | 1" × 2" |
| G | 314 | 0.503 | 1.5" × 2.5" |
| H | 506 | 0.785 | 2" × 3" |
| J | 804 | 1.287 | 2.5" × 4" |
| K | 1,140 | 1.838 | 3" × 4" |
| L | 1,650 | 2.853 | 3" × 4" |
| M | 2,800 | 4.340 | 4" × 6" |
| N | 4,340 | 6.380 | 4" × 6" |
| P | 6,290 | 11.050 | 6" × 8" |
| Q | 11,100 | 16.000 | 6" × 10" |
| R | 16,800 | 26.000 | 8" × 10" |
| T | 26,000 | — | 10" × 12" |

**Sizing Principle:** Select next larger standard orifice above calculated required area; never downsize below required area

**Source:** API 526 Table 1 (Standard Orifice Designations)

**Applicable Standards Context:**

**ISA Form S20.50 (Control Valve Datasheets):**
- Industry-standard format for control valve datasheets
- Provides consistent structure recognized by vendors worldwide
- Includes process conditions, valve sizing, body/trim specs, actuator specs, accessories
- **Recommendation:** Use ISA S20.50 format (or close adaptation) for all control valve datasheets

**API 526 (Relief Valve Requirements):**
- Defines standard orifice sizes, pressure-temperature ratings, materials
- Specifies set pressure tolerances and testing requirements
- ASME stamping requirements ("UV" for vessels, "V" for piping)
- Mandatory for relief valves in ASME service in North America

**CSA B51 (Canadian Pressure Equipment Code):**
- Mandatory in British Columbia for pressure vessels and pressure piping
- Section 4.11 specifies relief valve requirements (generally aligned with ASME Section VIII)
- Relief valves protecting registered pressure vessels must be registered with Technical Safety BC
- **Note:** CSA B51 registration requirements TBD pending pressure vessel registration strategy

**Source:** Applicable standards for valve datasheets; CSA B51 mandatory in BC jurisdiction

## Considerations

**Factors to consider during development:**

**1. Project-Specific Factors**

- **Package Scope:** PKG-16 Valves & Specialty Equipment — datasheets cover control valves, isolation valves, relief valves, and specialty items (check valves, strainers)
- **Facility Type:** Transload facility (railcar unloading, storage, marine loading) — datasheets must address variable operating conditions (batch operation, seasonal variations)
- **Product:** CSD canola oil (food-grade, high viscosity) — valve materials must be food-grade; valve sizing must account for viscosity effects
- **Location:** Fraser Surrey Terminal, BC — coastal environment (corrosion); CSA B51 jurisdiction

**Source:** Decomposition document Sections 1.1 and 5 (PKG-16 scope)

**2. Deliverable Type Considerations (Data Sheet)**

- **Datasheet Format:** Standardized forms vs. tabular format vs. vendor format (see Specification.md — Functional Requirements for format options)
- **Data Sources:** Datasheets consolidate data from multiple sources (calculations, specifications, P&IDs, vendor data)
- **Revision Control:** Datasheets evolve through design stages (30%, 60%, 90%, IFP, As-Built); revision control critical
- **Vendor Data Incorporation:** Post-procurement update with vendor data (see Procedure.md — Step 4 for vendor data process)

**3. Coordination Requirements**

- **Upstream Deliverables (provide inputs to datasheets):**
  - P&IDs — valve tag numbers, service descriptions, line numbers, fail-safe modes
  - DEL-16.03 calculations — Cv, set pressure, actuator size
  - DEL-16.02 specification — materials, leakage class, testing requirements
  - Piping line list — line sizes, pressure classes
  - Equipment datasheets — protected equipment MAWP (for relief valves)

- **Downstream Deliverables (use datasheet data):**
  - DEL-16.01 drawings — valve arrangement based on datasheet sizes and types
  - DEL-16.05 installation/test records — test acceptance criteria from datasheets
  - Procurement — vendor bidding based on datasheet requirements
  - O&M manuals — operating and maintenance data from datasheets

- **Parallel Deliverables (iterative coordination):**
  - Instrumentation datasheets — control valve positioners, limit switches
  - Electrical datasheets — electric actuator motor specifications
  - HAZOP — fail-safe mode verification against HAZOP recommendations

**Source:** Dependencies inferred from package structure; NOT_TRACKED per `_DEPENDENCIES.md`

**4. Material Selection Considerations**

**Food-Grade Requirements (CSD Canola Oil Service):**
- **Body/Trim Materials:** Stainless steel (316SS or 304SS) preferred for product-contact valves
  - Carbon steel NOT acceptable for product service (corrosion, contamination)
  - Stainless steel provides food-grade cleanliness and corrosion resistance
- **Gasket/Seal Materials:** PTFE, RTFE, or food-grade EPDM
  - No asbestos-containing gaskets
  - No elastomers incompatible with edible oils (NBR may degrade)
- **Surface Finish:** Smooth internal surfaces to minimize product retention and facilitate cleaning
  - Consider electropolished internals for critical product valves
- **Drainability:** Valve design should minimize dead-legs and provide drain connections where required

**Environmental Considerations (Coastal Marine Atmosphere):**
- **External Corrosion:** Stainless steel or coated carbon steel for external components
  - Coastal environment = ISO 12944 corrosion category C4 or C5-M
  - Actuators, limit switches, solenoids require corrosion-resistant enclosures
- **Actuator Enclosures:** Stainless steel or coated aluminum; NEMA 4X or IP66 minimum
- **Bolting:** Stainless steel (ASTM A193 B8/B8M) preferred to reduce maintenance

**Source:** Material selection principles for food-grade service and coastal environment

**5. Fail-Safe Mode Selection**

Control valve and automated isolation valve fail-safe modes must be carefully selected to drive system to safe state on loss of utilities (see also Guidance.md for DEL-16.03 — Principles, Fail-Safe Mode Selection):

**Fail-Closed (FC) — Air-to-Open (ATO):**
- Spring-return actuator closes valve on loss of air supply
- **Use for:** Product isolation valves (prevent spill on power loss); tank inlet valves (prevent overflow)
- **Example:** Marine loading arm isolation valve (close on ESD to contain product)

**Fail-Open (FO) — Air-to-Close (ATC):**
- Spring-return actuator opens valve on loss of air supply
- **Use for:** Pump recirculation valves (prevent pump damage); cooling water valves (prevent overheating)
- **Example:** Pump minimum flow recirculation valve (open on power loss to protect pump)

**Fail-As-Is (FL) or Fail-Last Position (FLP):**
- Double-acting pneumatic or electric actuator; valve remains in last position
- **Use for:** Non-critical isolation valves where neither open nor closed is clearly safer
- **Example:** Manual isolation valve with electric actuator for remote operation convenience

**Decision Basis:**
- HAZOP (DEL-27.02) identifies safety-critical fail-safe modes
- Failure Modes and Effects Analysis (FMEA) evaluates consequences of fail-open vs. fail-closed
- **TBD:** Fail-safe mode approval process (HAZOP, design review, Employer approval)

**Source:** Fail-safe mode selection principles; coordination with HAZOP

**6. Vendor Selection Considerations**

**Pre-Qualified Vendors:**
- **Advantage:** Reduced procurement risk; proven performance; shorter lead time
- **Use for:** Critical valves (control valves, relief valves, large isolation valves)
- **Example Pre-Qualified Vendors (Control Valves):** Fisher (Emerson), Masoneilan (Baker Hughes), Valvitalia, Samson
- **Example Pre-Qualified Vendors (Relief Valves):** Crosby (Emerson), Consolidated, Farris, Leser

**"Or Equal" Provisions:**
- Datasheets may specify performance requirements without mandating specific vendor
- Allows competitive bidding with vendor substitutions subject to approval
- **Requirement:** Vendor must demonstrate equal or better performance (Cv, leakage class, materials, testing)

**Single-Source vs. Multi-Source:**
- **Single-Source (One Vendor for All Valves of Type):** Reduces spare parts inventory; simplifies training
- **Multi-Source (Multiple Vendors):** Lower cost through competition; reduces supply chain risk
- **Trade-off:** Cost savings vs. operational simplicity
- **TBD:** Vendor selection strategy per project procurement plan

**Source:** Vendor selection considerations typical for EPC projects

## Trade-offs

**Competing concerns to evaluate:**

**1. Datasheet Format: Standardized Forms vs. Tabular Database**

| Format | Advantages | Disadvantages | When to Use |
|--------|------------|---------------|-------------|
| **Standardized Forms (ISA S20.50, etc.)** | Familiar to vendors; comprehensive; easy to review | Labor-intensive (one form per valve); difficult to maintain consistency | Small projects (<50 valves); high-mix projects (many valve types) |
| **Tabular Database (Excel, Access, etc.)** | Easy to update; enforces consistency; supports bulk export | Less detail per valve; requires custom formatting for vendor | Large projects (>50 valves); standardized valve population |
| **Hybrid (Database + Forms)** | Best of both worlds; database for consistency, forms for vendor interface | More complex setup; requires data synchronization | Medium to large projects; mix of standard and custom valves |

**Guidance:** Use standardized forms for control valves (ISA S20.50 is industry standard); use tabular database for isolation and relief valves (more repetitive data). For large projects (>100 valves), consider hybrid approach.

**Source:** Datasheet format trade-offs; selection depends on project size and valve population

**2. Material Selection: Stainless Steel vs. Carbon Steel**

| Material | Advantages | Disadvantages | When to Use (Canola Oil Facility) |
|----------|------------|---------------|-----------------------------------|
| **Stainless Steel (316SS)** | Food-grade; corrosion-resistant; low maintenance; acceptable for coastal environment | Higher initial cost (~2–3× carbon steel) | All product-contact valves; valves in corrosive environment |
| **Carbon Steel (A105/A216)** | Lower initial cost; adequate strength | Requires coating/painting; rust potential; NOT food-grade | Utility services only (compressed air, nitrogen); NOT for product service |
| **Duplex Stainless (2205)** | Higher strength than 316SS; better corrosion resistance; lower cost than super-austenitic | Higher cost than 316SS; less common (longer lead time) | Severe corrosive service (if required); generally NOT needed for canola oil |

**Guidance for Canola Oil Facility:**
- **Product Valves:** 316SS body and trim (food-grade requirement, coastal environment)
- **Utility Valves:** Carbon steel acceptable with external coating (cost savings), OR stainless steel for reduced maintenance
- **Recommendation:** Standardize on 316SS for all valves to reduce spare parts inventory and simplify maintenance (trade upfront cost for lifecycle cost reduction)

**Source:** Material selection trade-offs; food-grade and coastal environment drive stainless steel preference

**3. Actuator Type: Pneumatic vs. Electric**

| Actuator Type | Advantages | Disadvantages | Typical Use (Canola Oil Facility) |
|---------------|------------|---------------|-----------------------------------|
| **Pneumatic Spring-Return** | Fast-acting (1–5 sec typical); inherent fail-safe; simple; low cost | Requires compressed air system; limited torque (large valves need large actuators) | Control valves; ESD valves requiring fail-safe |
| **Pneumatic Double-Acting** | Higher torque than spring-return; fast-acting | No inherent fail-safe (requires add-on spring module or accumulator) | Large isolation valves where fail-safe not required |
| **Electric Motor Operator (MOV)** | High torque; precise positioning; no air supply required | Slower (15–60 sec typical); no inherent fail-safe; higher cost | Large gate valves (NPS 10+); infrequent operation |
| **Manual (Handwheel/Gearbox)** | Simple; reliable; no utilities | Requires operator; slow; not suitable for remote/automated operation | Infrequently operated isolation valves; maintenance isolation |

**Guidance for Canola Oil Facility:**
- **Control Valves:** Pneumatic spring-return (fast response, fail-safe capability)
- **ESD Valves:** Pneumatic spring-return (safety-critical fail-safe)
- **Large Isolation Valves (>NPS 10):** Electric MOV (high torque) OR pneumatic double-acting (faster than electric)
- **Infrequent Isolation:** Manual (cost savings; simplicity)

**Typical Distribution (example):** 60% manual, 30% pneumatic, 10% electric — TBD pending P&ID development and automation philosophy

**Source:** Actuator type trade-offs; selection depends on valve function, size, and fail-safe requirements

**4. Leakage Class: Soft-Seated vs. Metal-Seated**

| Leakage Class | Seat Type | Leakage Rate (% of Cv) | When to Use |
|---------------|-----------|------------------------|-------------|
| **Class II** | Metal | 0.5% | High-temperature service (>400°F); fire-safe required |
| **Class IV** | Soft (PTFE) or Metal | 0.01% | Standard for control valves; good shutoff |
| **Class V** | Soft (PTFE) | 0.0005% | Tight shutoff required; moderate temperature (<450°F) |
| **Class VI** | Soft (PTFE, metal-backed) | Air test (no measurable leakage) | Bubble-tight shutoff; fugitive emissions critical |

**Guidance for Canola Oil Facility:**
- **Control Valves:** Class IV adequate for most applications (balance between shutoff and cost)
- **Isolation Valves:** Class VI (ball valves with soft seats) for critical isolation (prevent product cross-contamination)
- **Relief Valves:** Metal seats typical (no leakage class specified; tight shutoff verified by API 527 seat test if required)

**Source:** ANSI/FCI 70-2 leakage class definitions; selection based on shutoff requirements

**5. Relief Valve Type: Conventional vs. Balanced-Bellows vs. Pilot-Operated**

(See also Guidance.md for DEL-16.03 — Trade-offs, Relief Valve Type Selection for detailed comparison)

**Simplified Guidance:**
- **Conventional:** Use for low back pressure applications (<10% set pressure) — most common, lowest cost
- **Balanced-Bellows:** Use for moderate back pressure (10–50% set pressure) — typical for common discharge header
- **Pilot-Operated:** Use for high back pressure (>50% set pressure) OR where very tight shutoff required — highest cost, most complex

**For Canola Oil Facility:**
- **Storage Tank Relief Valves (Atmospheric Discharge):** Conventional (minimal back pressure)
- **Piping Thermal Relief (Discharge to Header):** Balanced-bellows (moderate back pressure from header)
- **High-Pressure Systems (if applicable):** Pilot-operated only if back pressure analysis shows >50%

**Source:** API 520 relief valve type selection guidance

## Examples

**Reference examples and precedents:**

**1. Employer's Requirements**

Refer to Employer's Requirements (Volume 2 Parts 1–3) for project-specific expectations:
- Valve datasheet format and content requirements
- Material specifications and food-grade requirements
- Vendor qualification and approval requirements
- Submittal requirements and review cycles

**Location:** `/Users/ryan/ai-env/projects/chirality-app/test/Volume_2_Part_{1,2,3}_Employers_Requirements.pdf` — **TBD** (not yet available in `_REFERENCES.md`)

**2. Industry Precedents**

**Typical valve datasheets for similar facilities:**

**Control Valve Datasheet Example (Excerpt):**
```
CONTROL VALVE DATA SHEET
Tag: FV-1234
Service: Product Transfer Flow Control (Railcar to Tank)
P&ID: P&ID-001-001, Rev B
Line: 4"-PL-1234-CS-150

PROCESS CONDITIONS:
Fluid: CSD Canola Oil
Flow (Normal/Design/Min): 120 / 150 / 10 m³/h
Inlet Pressure: 8 barg
Outlet Pressure: 3 barg
Differential Pressure: 5 bar
Temperature: 40°C
Density: 920 kg/m³
Viscosity: 35 cSt

VALVE SIZING (per Calc CALC-PKG16-DEL03-001):
Required Kv: 75.8
Selected Valve Size: DN 80 (3")
Valve Type: Globe, through-body
Trim Characteristic: Equal Percentage
Cv Selected: 100 (Kv = 87)
Rangeability: 50:1
Cavitation Index: σ = 1.8 (Acceptable, σ > σc)

VALVE BODY:
Material: ASTM A351 CF8M (316SS)
End Connections: ASME B16.5 Class 150 RF flanges
P-T Rating: Class 150 (285 psig @ 100°F)
Body Style: Through-body globe

TRIM:
Trim Material: 316SS
Seat: Soft-seated PTFE
Plug: Contoured, equal percentage
Stem: 316SS
Packing: Graphite, live-loaded
Leakage Class: ANSI/FCI 70-2 Class IV

ACTUATOR (per Calc CALC-PKG16-DEL03-002):
Type: Pneumatic, spring-return
Action: Air-to-Open (ATO)
Fail-Safe: Fail-Closed (FC)
Required Torque: 85 Nm
Actuator Size: TBD (vendor selection)
Output Torque: ≥128 Nm (safety factor 1.5)
Air Supply: 6 barg
Stroking Time: <5 seconds

ACCESSORIES:
Positioner: Smart digital, 4–20 mA input, HART communication
Limit Switches: Open/closed indication
Air Set: Filter-regulator-gauge (FRG)
Manual Override: Handwheel

CODES & STANDARDS:
Design: IEC 60534 / ISA-75
Flanges: ASME B16.5
Testing: IEC 60534-4
```

**Relief Valve Datasheet Example (Excerpt):**
```
RELIEF VALVE DATA SHEET
Tag: PSV-5001
Protected Equipment: TK-001 (Canola Oil Storage Tank)
P&ID: P&ID-005-001, Rev A

PROTECTED EQUIPMENT:
Type: Atmospheric storage tank (cone roof)
MAWP: 0.35 barg (5 psig)
Design Pressure: 0.21 barg (3 psig)
Design Temperature: 60°C
Volume: 2,500 m³
Diameter: 15 m
Height: 12 m

RELIEF SCENARIO (per Calc CALC-PKG16-DEL03-025):
Governing Scenario: External Fire (API 521 fire case)
Required Relief Capacity: 97,000 kg/h
Relieving Pressure: 0.23 barg (3.3 psig) = 1.1× MAWP
Fluid State: Vapor (canola oil vapor)

VALVE SIZING:
Set Pressure: 0.21 barg (3 psig) = 1.05× design pressure
Set Pressure Tolerance: ±3 psi (per API 526)
Overpressure: 10% (operating case)
Required Orifice Area: 3,250 mm² (5.04 in²)
Selected Orifice: API 526 Orifice N (4,340 mm² / 6.38 in²)
ASME Stamped Capacity: 98,500 kg/h (at 3.3 psig)

VALVE SPECIFICATIONS:
Type: Conventional (low back pressure)
Size: NPS 6 × 8 (6" inlet × 8" outlet)
Body Material: ASTM A216 WCB (carbon steel)
Spring Material: Stainless steel
Trim Material: 316SS
Seat: Metal
Connections: ASME B16.5 Class 150 RF flanges
ASME Stamp: "UV" (pressure vessel service)

DISCHARGE ARRANGEMENT:
Discharge: To atmosphere via vent stack
Discharge Piping: 8" (DN 200) to 15 m high vent
Back Pressure: <5% set pressure (Acceptable for conventional)
Inlet Piping Loss: <3% set pressure

TESTING:
Set Pressure Test: CDTP per API 527
Test Medium: Air or Nitrogen
Capacity Certification: ASME stamped per Section VIII
Seat Tightness: API 527 (if required by specification)

CODES & STANDARDS:
Design: ASME Section VIII Div 1, CSA B51
Sizing: API 520/521
Manufacturing: API 526
Testing: API 527

REGULATORY:
CSA B51 Registration: TBD (if tank is registered pressure vessel)
National Board: TBD
```

**Source:** Typical control valve and relief valve datasheet examples; specific values illustrative only (TBD pending actual design)

**3. Related Deliverables**

- **DEL-16.01 (Valve Design Drawing Set):** Valve arrangement drawings show valves per datasheet tags and sizes
- **DEL-16.02 (Valve Technical Specification):** Procurement specification defines general requirements for valves; datasheets specify individual valve applications
- **DEL-16.03 (Valve Design Calculations):** Sizing calculations provide Cv, set pressure, actuator size data for datasheets
- **DEL-16.05 (Valve Installation & Test Records):** Installation and test records reference datasheets for acceptance criteria (Cv verification, set pressure test)

**Source:** PKG-16 deliverable structure from decomposition Section 5

**4. Datasheet Templates and Standards**

**ISA Form S20.50 (Control Valve Datasheets):**
- Widely recognized industry-standard format
- Available from ISA (International Society of Automation)
- Provides consistent structure for all control valve types (globe, ball, butterfly)
- **Recommendation:** Use ISA S20.50 or close adaptation for control valve datasheets

**Custom Templates (Isolation and Relief Valves):**
- No equivalent industry-standard forms for isolation and relief valves
- Develop project-specific templates based on typical content (see Datasheet.md — Construction section)
- **Recommendation:** Standardize templates across project for consistency

**Vendor Forms:**
- Many valve vendors provide their own datasheet forms
- **Use for:** Vendor quotation and submittal (vendor completes their form)
- **Do NOT use for:** Project design datasheets (maintain project control and consistency)

**Source:** Datasheet format standards and templates

**5. Typical Datasheet Quantities**

**Example for similar facility (1,000,000 MT/annum transload):**
- Control valves: 10–20 (flow control, level control, pressure control)
- Isolation valves (manual): 50–100 (block valves, maintenance isolation)
- Isolation valves (automated): 10–20 (ESD valves, remote-operated)
- Relief valves: 5–15 (tank relief, piping thermal relief, pump blocked discharge)
- Check valves: 10–20 (pump discharge, backflow prevention)
- Strainers: 5–10 (pump suction protection)
- **Total valves: 90–185** (TBD pending P&ID development)

**Source:** Typical valve population for transload facility; actual quantities TBD

**6. Lessons Learned (Typical Issues)**

**Common datasheet issues to avoid:**
- **Inconsistency Between Datasheets and Calculations:** Datasheet shows different Cv than calculation; **Solution:** Automate data transfer from calculation to datasheet (linked spreadsheets)
- **P&ID Tag Mismatch:** Datasheet tag doesn't match P&ID; **Solution:** Maintain master tag register; reconcile P&ID and datasheets regularly
- **Missing Vendor Data:** Post-procurement datasheet not updated with actual valve data; **Solution:** Formal vendor data submittal and review process (see Procedure.md Step 4)
- **Material Specification Ambiguity:** "Stainless steel" without grade specified (304 or 316?); **Solution:** Always specify ASTM grade (e.g., "ASTM A351 CF8M = 316SS")
- **Fail-Safe Mode Error:** Datasheet shows FC but P&ID shows FO; **Solution:** IDC review by control systems discipline to verify fail-safe modes

**Source:** **ASSUMPTION**: Typical datasheet issues from industry experience; project-specific lessons TBD
