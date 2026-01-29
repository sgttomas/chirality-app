# Procedure: DEL-21.03 Building Design Calculations

## Purpose

This procedure defines the process for **producing** **Building Design Calculations** within **PKG-21 Building Structures & Envelope**.

**Deliverable Purpose:** Provides engineering basis and sizing/verification calculations for building.
**Source:** Decomposition line 515

## Prerequisites

### Dependencies

**Dependency Tracking Mode:** NOT_TRACKED — Dependencies coordinated externally
**Source:** `_DEPENDENCIES.md`

**Typical Upstream Inputs:**
1. **Design Criteria** — Loads, materials, performance requirements — **TBD**
2. **Geotechnical Investigation** — Soil bearing, frost depth — **TBD**
3. **Building Layout** — Equipment locations, clearances (coordinate with DEL-21.01)
4. **ER Requirements** — **TBD**: ER Volume 2 Part 3

### Reference Materials

**Codes:** NBC 2020 Part 4, CSA S16, CSA A23.3 (see Specification.md)

### Personnel

1. **Structural Engineer (P.Eng., BC)** — Performs calculations, seals
2. **Independent Checker (P.Eng. or senior engineer)** — Reviews calculations

### Tools

- **Analysis Software** (if used): **TBD** — ETABS, SAP2000, etc.
- **Calculation Software**: MathCAD, Excel, hand calculations

## Steps

### Step 1: Establish Design Criteria

**Activities:**
- Review ER for structural requirements — **TBD**
- Establish loads per NBC 2020 (dead, live, snow, wind, seismic)
- Select materials (steel grades, concrete strengths)
- Document design criteria

**Deliverables:** Design criteria summary

### Step 2: Perform Structural Analysis

**Activities:**
- Develop structural model or calculation scheme
- Calculate member forces, reactions, deflections
- Check load distribution and lateral stability

**Deliverables:** Analysis results

### Step 3: Design Structural Members

**Activities:**
- Design beams (flexure, shear, deflection per CSA S16/A23.3)
- Design columns (axial, bending, buckling)
- Design connections (bolts, welds, base plates)
- Verify all code checks pass

**Deliverables:** Member sizing and connection design

### Step 4: Design Foundations

**Activities:**
- Design footings/piles per geotechnical recommendations
- Check bearing capacity and settlement
- Design reinforcing (if concrete foundations)

**Deliverables:** Foundation sizing and design

### Step 5: Perform Wind/Seismic Analysis

**Activities:**
- Calculate wind pressures per NBC 2020
- Calculate seismic base shear per NBC 2020
- Verify lateral drift limits
- Design lateral load-resisting system

**Deliverables:** Wind/seismic analysis

### Step 6: Document Calculations

**Activities:**
- Compile calculations into organized package
- Include design criteria, analysis, member design, foundation design
- Add sketches/diagrams as needed
- Prepare cover sheet with P.Eng. seal

**Deliverables:** Complete calculation package

### Step 7: Independent Check

**Activities:**
- Independent checker reviews calculations
- Check design criteria, assumptions, code compliance
- Verify spot-checks of critical elements
- Document review comments
- Designer addresses comments

**Deliverables:** Check comments log and resolution

### Step 8: Approval and Issue

**Activities:**
- Lead engineer reviews and approves
- P.Eng. seals calculations
- Issue to project DMS
- Update `_STATUS.md`

**Deliverables:** Issued calculations (PDF with P.Eng. seal)

## Verification

**V1: Independent Check** (Step 7) — Qualified checker reviews
**V2: Peer Review** — Senior engineer reviews approach
**V3: Model Validation** (if software used) — Validate against hand calculations

**Acceptance Criteria:**
- Calculations complete and clear
- All design checks pass
- Independent check complete
- P.Eng. seal and signature

## Records

**Required Outputs:**
1. Building Structural Calculations
2. Foundation Calculations
3. Wind/Seismic Analysis

**Record Management:** `1_Working/` → `2_Checking/` → `3_Issued/` per `_STATUS.md`
**Format:** PDF calculation packages with P.Eng. seal

---

**Procedure Revision History:**

| Date | Revision | Description | Author |
|------|----------|-------------|--------|
| 2026-01-28 | 0 | Initial procedure draft | 4_DOCUMENTS Agent |
