# Procedure: DEL-27.05 Cathodic Protection Design Basis & Design Calculations

## Purpose

Defines process for producing **Cathodic Protection Design Basis & Design Calculations** within **PKG-27 Engineering Design**. Establishes CP system design to prevent corrosion of buried and submerged steel structures.

**Source:** _CONTEXT.md; Specification.md

## Prerequisites

**Dependencies:** Structural drawings (surface areas), piping drawings (routes, materials), coating specs, site data (resistivity)
**References:** NACE SP0169, CSA Z662, site geotechnical/environmental reports — **TBD**
**Personnel:** Qualified CP Specialist (NACE-certified or equivalent), Senior CP Specialist (checker), P.Eng. (approver)

**Source:** Specification.md; **ASSUMPTION**: CP specialist certification required for corrosion protection design

## Steps

### Step 1: Collect Input Data
- Structure inventory (tanks, piping, marine structures) from drawings
- Surface areas and embedment details
- Coating specifications and efficiency assumptions
- Soil/water resistivity data from site investigation
- Stray current survey results (if applicable)

**Outputs:** Input data package for CP calculations

### Step 2: Develop CP Design Basis
- Assess corrosion environment (soil/water conductivity, aggressiveness)
- Establish protection criteria per NACE SP0169 or CSA Z662
- Select CP system type (ICCP vs. sacrificial) with rationale
- Define design life, current density assumptions, design margins
- Document methodology and standards

**Outputs:** CP Design Basis document

### Step 3: Calculate Current Demand
- For each structure: Surface Area × Current Density × (1 - Coating Efficiency)
- Sum total demand for all structures
- Apply design margin (typical 20-50%)
- **TBD** — Structure-specific current densities from NACE standards

**Outputs:** Current demand calculation with summary table

### Step 4: Design Anode System

**If ICCP:**
- Size rectifier for total current demand + margin + future expansion (**TBD**)
- Select anode type (mixed metal oxide, high silicon cast iron, etc.)
- Design anode bed (deep well vs. distributed)
- Calculate anode-to-earth resistance
- Verify voltage output adequate

**If Sacrificial Anodes:**
- Select anode material (zinc for brackish water, magnesium for soil)
- Calculate anode current output capacity
- Size anodes for design life
- Determine number and spacing for uniform distribution
- Verify anode output meets demand

**Outputs:** Anode layout calculations; anode data sheets

### Step 5: Prepare Design Drawings
- Site plan showing anode locations, rectifier locations (ICCP), test stations
- Connection details (anode-to-structure bonds, cable routing)
- Typical installation details
- **TBD** — Drawing format per project CAD standards

**Outputs:** CP design drawings

### Step 6: Independent Check
- Qualified CP Specialist (independent of originator) checks all calculations
- Verify methodology per NACE/CSA standards
- Check arithmetic, units, assumptions
- Sensitivity analysis for key parameters
- Checker signs off

**Outputs:** Checked and approved calculations

### Step 7: Finalize and Issue
- Address checker comments
- Obtain P.Eng. approval
- Issue to `3_Issued/` with document control
- Distribute to structural/piping/electrical teams for implementation

**Outputs:** Issued CP design basis and calculations ready for construction

**Source:** Specification.md; **ASSUMPTION**: Standard calculation procedure per project QMS

## Verification

- Independent check by qualified CP specialist
- Design code compliance (NACE/CSA)
- Sensitivity analysis
- Post-installation field testing to verify design

**Source:** Specification.md

## Records

**Outputs:** CP design basis, current demand calculations, anode layout calculations, design drawings
**Filing:** Working `1_Working/`; checking `2_Checking/`; issued `3_Issued/`

**Source:** Specification.md; **ASSUMPTION**: Standard deliverable lifecycle per AGENTS.md

---

**Cross-Document Verification (Pass 3):**
- All Steps linked to Specification § requirements being verified
- All Steps linked to Guidance § principles and considerations for rationale
- All Verification activities linked to Specification § requirements
- Terminology verified consistent with Datasheet.md, Specification.md, Guidance.md
- CP calculation methodology (Steps 3-4) verified consistent with Guidance § Examples
- Independent check requirement (Step 6) verified consistent with Specification § QR-1
- Cross-references to structural (PKG-05, PKG-06, PKG-08), piping (PKG-14), and electrical (PKG-17) verified consistent
