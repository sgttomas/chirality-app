# Procedure: DEL-15.03 Pump Design Calculations

## Purpose

This procedure defines the process for **producing** the **Pump Design Calculations** within **PKG-15 Pumps & Rotating Equipment** for the Canola Oil Transload Facility.

**Deliverable purpose:** Provides the engineering basis and sizing/verification calculations for pumps per ER requirements.

**Source:** `_CONTEXT.md` (description), decomposition DEL-15.03 entry

**Deliverable type:** Calculation (Engineering design calculations)
**Responsible party:** D&B Contractor (Mechanical discipline)

This procedure covers:
1. **Calculation development:** How to size pumps, calculate NPSH, develop system curves
2. **Verification:** How to check calculations for accuracy and completeness
3. **Documentation:** How to format and issue calculation packages

**Source:** Standard engineering calculation process

## Prerequisites

### Dependencies

**Dependency tracking mode:** NOT_TRACKED — Dependencies are coordinated externally by humans (see `execution/_Coordination/_COORDINATION.md`)

**Source:** `_DEPENDENCIES.md`

### Upstream Information Required

| Information | Source | Status |
|------------|--------|--------|
| **Flow rates** | Process design (PKG-10, 11, 12) | **TBD** |
| **Fluid properties** | ER Part 2 or process data | **TBD** |
| **Piping layout** | DEL-14 (piping design) | **TBD** |
| **Pipe sizes** | DEL-14 (piping design) | **TBD** |
| **Equipment pressure drops** | Vendor data or typical values | **TBD** |
| **Elevation data** | Site civil drawings (PKG-04, 05) | **TBD** |
| **Tank levels** | DEL-13 (storage tanks) | **TBD** |

**Source:** Typical pump sizing calculation input requirements

### Reference Materials

- Employer's Requirements Volume 2 Part 2 — **location TBD**: Fluid properties, process requirements
- API 610 — Centrifugal Pumps for Petroleum, Petrochemical and Natural Gas Industries
- Crane Technical Paper No. 410 — Flow of Fluids Through Valves, Fittings, and Pipe
- Cameron Hydraulic Data or Perry's Chemical Engineers' Handbook — Fluid properties

**Source:** Standards and references from Specification.md

### Personnel and Tools

**Personnel:**
- Lead Mechanical Engineer (P.Eng.) — Overall responsibility, approval
- Mechanical Engineer — Calculation development
- Checker (Independent) — Calculation verification

**Tools:**
- Spreadsheet software (Excel or equivalent)
- Calculator or engineering calculation software
- Moody diagram or Colebrook equation solver for friction factor

**Source:** Standard calculation development requirements

## Steps

### Phase 1: Define Pump Duties and Operating Conditions

#### Step 1.1: Identify Pump Services

**Action:**
- List all pump services required for facility (from process design and DEL-15.02)
- For each service, identify:
  - Service description
  - Quantity of pumps (duty, standby, spares)
  - Operating philosophy (continuous, intermittent, duty/standby rotation)

**Verification:**
- Pump services match process requirements and system design

**Records:**
- Pump service list (may be table in calculation or separate summary)

**Source:** Process design, DEL-15.02 specification

---

#### Step 1.2: Collect Fluid Properties

**Action:**
- For each pump service, collect fluid properties at operating temperature:
  - Fluid name (CSD canola oil)
  - Specific gravity (SG) or density (ρ)
  - Kinematic viscosity (ν)
  - Vapor pressure (Pv)
  - Operating temperature range

**Data sources:**
- ER Part 2 (process data)
- Vendor fluid property data
- Engineering handbooks (Cameron, Perry's)

**Verification:**
- Fluid properties are at correct operating temperature
- Units are clearly stated and consistent

**Records:**
- Fluid properties table in calculation

**Source:** ER Part 2, fluid properties references

---

#### Step 1.3: Define Operating Scenarios and Flow Rates

**Action:**
- For each pump service, define operating scenarios:
  - **Normal operation:** Typical flow rate and operating conditions
  - **Maximum flow:** Design maximum (typically 120% of normal)
  - **Minimum flow:** Lowest stable flow (to check minimum continuous flow requirement)
  - **Future expansion:** If applicable per OBJ-8

- Collect flow rate data from process design

**Verification:**
- Flow rates match process requirements and throughput objectives (OBJ-2: 1,000,000 MT/annum)

**Records:**
- Operating scenarios table in calculation

**Source:** Process design (PKG-10, 11, 12), DEL-15.02 specification

---

### Phase 2: Calculate Total Dynamic Head (TDH)

#### Step 2.1: Calculate Static Head

**Action:**
- Identify suction and discharge liquid levels (normal and worst-case)
- Calculate static head: Hs = Elevation(discharge) - Elevation(suction)
- Use surveyed elevations or site drawings

**Verification:**
- Elevations are relative to consistent datum
- Worst-case static head is identified (e.g., minimum suction level, maximum discharge level)

**Records:**
- Static head calculation showing elevations and result

**Source:** Site civil drawings (PKG-04, 05), DEL-15.01 (pump arrangement), DEL-13 (tank levels)

---

#### Step 2.2: Calculate Suction Piping Friction Losses

**Action:**
- From piping layout (DEL-14), identify:
  - Suction pipe length (L)
  - Suction pipe size and internal diameter (D)
  - Fittings and valves (elbows, tees, gate valves, etc.)

- Calculate flow velocity: V = Q / A (where A = π × (D/2)²)

- Calculate Reynolds number: Re = V × D / ν

- Determine friction factor (f) from Moody diagram or Colebrook equation

- Calculate pipe friction: hf_pipe = f × (L/D) × (V²/2g)

- Calculate fitting/valve losses using K-factor method: hf_fittings = ΣK × (V²/2g)
  - K values from Crane TP-410 or equivalent

- **Total suction friction: Hf(suction) = hf_pipe + hf_fittings**

**Verification:**
- Flow is turbulent (Re > 4,000) for typical process pumps; if laminar or transitional, special care required
- Friction factor is reasonable for pipe roughness (ε = 0.046mm typical for commercial steel)
- All significant fittings and valves are included

**Records:**
- Detailed friction loss calculation showing pipe length, velocity, Re, f, K values, and results

**Source:** Crane TP-410, DEL-14 (piping layout), fluid mechanics principles

---

#### Step 2.3: Calculate Discharge Piping Friction Losses

**Action:**
- Same process as Step 2.2, but for discharge piping
- Include control valve pressure drop (if applicable):
  - If Cv (flow coefficient) is known: ΔP = (Q / Cv)² × SG [ΔP in psi, Q in GPM] — convert to head
  - If not known, estimate 50–100 kPa (5–10m) typical for control valve

- **Total discharge friction: Hf(discharge) = hf_pipe + hf_fittings + hf_control_valve + hf_equipment**

**Verification:**
- Control valve pressure drop is reasonable and appropriate for flow control
- Equipment pressure drops (strainers, meters, heat exchangers) are included if applicable

**Records:**
- Detailed friction loss calculation for discharge piping

**Source:** Crane TP-410, DEL-14 (piping layout), vendor data for control valves and equipment

---

#### Step 2.4: Calculate Total Dynamic Head

**Action:**
- Sum all head components:

**TDH = Hs + Hf(suction) + Hf(discharge) + Hp**

Where:
- Hs = Static head
- Hf(suction) = Suction piping friction losses
- Hf(discharge) = Discharge piping friction losses
- Hp = Pressure head (if suction or discharge vessels are pressurized)

- Round to reasonable precision (e.g., nearest 0.1m or 1m depending on magnitude)

**Verification:**
- TDH is reasonable for service type (typical: 20–100m for process pumps)
- Friction losses are significant portion of TDH (if not, check for errors or missing components)

**Records:**
- TDH summary table showing all components and total

**Source:** Fluid mechanics principles, pump sizing methodology

---

### Phase 3: Calculate NPSH Available

#### Step 3.1: Identify Worst-Case Conditions

**Action:**
- Determine worst-case conditions for NPSH:
  - **Minimum suction liquid level** (lowest static head)
  - **Maximum fluid temperature** (highest vapor pressure)
  - **Maximum suction friction losses** (longest piping run, highest flow rate)

**Verification:**
- Worst-case scenario is realistic and conservative

**Records:**
- Worst-case conditions documented in calculation

**Source:** Engineering judgment, API 610 guidance

---

#### Step 3.2: Calculate NPSH Available

**Action:**
- Calculate NPSH available:

**NPSHA = Hatm + Hs(suction) - Hvp - Hf(suction)**

Where:
- Hatm = Atmospheric pressure head (typically 10.3m at sea level; adjust for elevation if needed)
- Hs(suction) = Static head at suction (positive if liquid level above pump centerline, negative if below)
- Hvp = Vapor pressure head at maximum operating temperature (convert vapor pressure to head: Hvp = Pv / (ρ × g))
- Hf(suction) = Suction piping friction losses (from Step 2.2)

**Verification:**
- NPSHA is positive (if negative, pump cannot operate — suction lift too high or NPSH inadequate)
- NPSHA is reasonable for service (typical: 3–15m for process pumps)

**Records:**
- NPSHA calculation showing all components and result

**Source:** API 610 Section 3.8, fluid mechanics principles

---

#### Step 3.3: Determine NPSH Margin Requirement

**Action:**
- Establish required NPSH margin: **NPSHA - NPSHR ≥ 0.5m** (API 610 minimum)
- For critical services or high-energy pumps, larger margin may be specified (1.0–1.5m)
- Document maximum allowable NPSHR for vendor pump selection:

**NPSHR(max) = NPSHA - Margin**

**Verification:**
- NPSH margin requirement is appropriate for service criticality

**Records:**
- NPSH margin requirement and maximum allowable NPSHR documented

**Source:** API 610 Section 3.8, engineering judgment

---

### Phase 4: Calculate Pump Power

#### Step 4.1: Estimate Pump Efficiency

**Action:**
- Estimate pump efficiency based on pump size:
  - Small pumps (< 50 HP): η ~ 60–75%
  - Medium pumps (50–200 HP): η ~ 75–85%
  - Large pumps (> 200 HP): η ~ 85–90%

- Use API 610 typical efficiency curves or vendor historical data if available

**Verification:**
- Efficiency estimate is reasonable for pump size and type

**Records:**
- Efficiency assumption documented with justification

**Source:** API 610 efficiency curves, vendor data

---

#### Step 4.2: Calculate Pump Brake Horsepower

**Action:**
- Calculate pump power:

**SI units:** BHP = (ρ × g × Q × TDH) / (η × 1,000) [result in kW]
- ρ = Fluid density (kg/m³)
- g = 9.81 m/s²
- Q = Flow rate (m³/s)
- TDH = Total dynamic head (m)
- η = Pump efficiency (decimal, e.g., 0.75)

**US units:** BHP = (Q × TDH × SG) / (3,960 × η) [result in HP]
- Q = Flow rate (GPM)
- TDH = Total dynamic head (ft)
- SG = Specific gravity
- η = Pump efficiency (decimal)

**Verification:**
- BHP is reasonable for flow rate and head (rough check: BHP ~ Q × TDH / 360 for Q in m³/hr, TDH in m, η = 75%, result in kW)

**Records:**
- BHP calculation showing inputs, equation, and result

**Source:** Fluid mechanics principles, pump power equations

---

#### Step 4.3: Recommend Motor Size

**Action:**
- Apply motor sizing margin: **Motor power ≥ 1.15 × BHP** (15% margin typical)
- Round up to standard motor size
- Consider VFD if applicable (may require additional margin for harmonics)

**Verification:**
- Motor size is adequate for pump BHP with margin

**Records:**
- Motor sizing recommendation with justification

**Source:** Motor sizing standards, electrical discipline coordination

---

### Phase 5: Develop System Curve

#### Step 5.1: Calculate System Resistance Coefficient

**Action:**
- System curve equation: H(Q) = Hs + K × Q²
- From TDH calculation at rated flow (Qr):

**K = (TDH - Hs) / Qr²**

**Verification:**
- K is positive (if negative, check calculation errors)

**Records:**
- System resistance coefficient calculation

**Source:** Hydraulic system analysis

---

#### Step 5.2: Generate System Curve Data Points

**Action:**
- Calculate system head at multiple flow rates (e.g., 0%, 50%, 75%, 100%, 120% of rated flow):

For each Q: H(Q) = Hs + K × Q²

- Tabulate results and plot if desired (graph showing H vs. Q)

**Verification:**
- System curve passes through calculated operating point (Qr, TDH)

**Records:**
- System curve table and/or plot

**Source:** Hydraulic system analysis

---

### Phase 6: Summarize Results

#### Step 6.1: Prepare Results Summary

**Action:**
- Create summary table for each pump service showing:
  - Flow rate (Q)
  - Total dynamic head (TDH)
  - NPSH available (NPSHA)
  - Maximum allowable NPSHR
  - Pump brake horsepower (BHP)
  - Recommended motor size

**Verification:**
- Summary is clear and complete

**Records:**
- Results summary table

**Source:** Calculation outputs from Steps 2–4

---

#### Step 6.2: Document Recommendations

**Action:**
- Provide recommendations for:
  - Pump type selection (horizontal/vertical, single-stage/multi-stage)
  - Operating point considerations (preferred operating region)
  - NPSH margin verification requirement for vendor proposals
  - Motor sizing requirement
  - Special considerations (heating for viscosity, VFD evaluation, etc.)

**Verification:**
- Recommendations are clear and actionable

**Records:**
- Recommendations section in calculation

**Source:** Engineering judgment, API 610 guidance

---

### Phase 7: Verification and Approval

#### Step 7.1: Self-Check

**Action:**
- Perform self-check of calculations:
  - Verify inputs match source documents
  - Check all equations and unit conversions
  - Verify arithmetic (spot-check key calculations)
  - Ensure assumptions are clearly stated

**Verification:**
- Self-check sign-off

**Records:**
- Self-check documentation

**Source:** Standard calculation quality procedure

---

#### Step 7.2: Independent Check

**Action:**
- Checker performs sample calculations to verify:
  - Methodology is appropriate
  - Key calculations are correct (TDH, NPSHA, BHP)
  - Results are reasonable

- Checker issues check comments if errors found
- Author resolves check comments

**Verification:**
- Checker sign-off obtained

**Records:**
- Check comments and resolutions

**Source:** Standard calculation checking procedure per Specification.md

---

#### Step 7.3: Approval and Issue

**Action:**
- Lead Mechanical Engineer reviews and approves calculation
- Assign revision and issue status
- Transmit to project document control and distribute to:
  - DEL-15.02 (specification author)
  - Procurement (for equipment requisition)
  - Piping discipline (for coordination)
  - Electrical discipline (for motor sizing)

**Verification:**
- All sign-offs obtained
- Calculation is complete and ready for use

**Records:**
- Approved calculation package
- Transmittal documentation

**Source:** Standard calculation approval procedure

---

## Verification

### Verification Summary

| Activity | Verifier | Criteria |
|----------|----------|----------|
| **Input verification** | Author | Inputs match source documents |
| **Calculation check** | Author (self-check) | Equations correct, units consistent, arithmetic correct |
| **Results reasonableness** | Author | Results within expected range for service |
| **Independent check** | Checker | Sample calculations agree, methodology appropriate |
| **Approval** | Lead Engineer | Calculation complete and suitable for use |
| **Vendor verification** | Author | Vendor NPSHR < NPSHA with margin; operating point OK |

**Source:** Standard calculation verification process per Specification.md

## Records

### Documentation Outputs

The following calculation documents shall be produced:

1. **Pump Sizing Calculations** — Flow, head, power for all pump services
2. **NPSH Calculations** — NPSH available for worst-case conditions
3. **System Curves** — System head vs. flow curves

**Source:** `_CONTEXT.md` (anticipated artifacts)

### Calculation Format

- **Cover sheet:** Title, project, author, checker, approver, date, revision
- **Body:** Inputs, assumptions, methodology, calculations, results, recommendations
- **Attachments:** Spreadsheets, reference data, vendor information

**Source:** Standard calculation format per Specification.md

### Record Management

- **Filing location:** `1_Working/DEL-15.03_Pump_Design_Calculations/`
- **Revision control:** Per project procedures — **TBD**
- **Retention:** Per ER requirements — **TBD** — **ASSUMPTION**: 25 years

**Source:** Project document control procedures

---

**Document Status:** ENRICHED (Pass 1)
**Enrichment Date:** 2026-01-28
**Agent:** 4_DOCUMENTS enrichment cycle

**Cross-References:**
- Datasheet.md — Calculation methodology and inputs
- Specification.md — Calculation requirements and acceptance criteria
- Guidance.md — Calculation principles and best practices
- DEL-15.02 — Pump Technical Specification (receives calculation outputs)
- DEL-15.04 — Pump Data Sheet Package (vendor data verification)
- DEL-15.05 — Pump Installation & Test Records (field test comparison)
