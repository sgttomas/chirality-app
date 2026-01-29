# Procedure: DEL-21.04 Building Data Sheet Package

## Purpose

This procedure defines the process for **producing** **Building Data Sheet Package** within **PKG-21 Building Structures & Envelope**.

**Deliverable Purpose:** Defines and substantiates building in accordance with ER requirements.
**Source:** Decomposition line 516

## Prerequisites

### Dependencies

**Dependency Tracking Mode:** NOT_TRACKED — Dependencies coordinated externally
**Source:** `_DEPENDENCIES.md`

**Typical Upstream Inputs:**
1. **Design Drawings (DEL-21.01)** — Door/window locations and marks
2. **Specifications (DEL-21.02)** — Door/window types and materials
3. **Calculations (DEL-21.03)** — Design loads and parameters
4. **ER Requirements** — **TBD**: Data sheet format requirements

### Personnel

1. **Designer/Engineer** — Prepares data sheets and schedules
2. **Reviewer** — Checks accuracy and coordination

## Steps

### Step 1: Prepare Building System Data Sheet

**Activities:**
- Extract building parameters from drawings, specifications, calculations
- Compile into single-page data sheet format
- Include: dimensions, occupancy, systems, loads, codes
- **TBD** — Format per ER requirements

**Deliverables:** Building system data sheet

### Step 2: Prepare Door Schedule

**Activities:**
- List all doors from all drawing sheets
- Extract door information: type, size, material, fire rating, hardware
- Cross-reference with door specification (DEL-21.02)
- Verify all doors accounted for

**Deliverables:** Complete door schedule

### Step 3: Prepare Window Schedule

**Activities:**
- List all windows from all drawing sheets
- Extract window information: type, size, glazing, frame
- Cross-reference with window specification
- Verify all windows accounted for

**Deliverables:** Complete window schedule

### Step 4: Coordination Review

**Activities:**
- Verify data sheet parameters match calculations
- Verify door/window schedules match drawings
- Verify door/window types match specifications
- Resolve any discrepancies

**Deliverables:** Coordinated data sheets and schedules

### Step 5: Quality Review and Approval

**Activities:**
- Reviewer checks data sheets and schedules for accuracy and completeness
- Designer addresses review comments
- Lead designer approves

**Deliverables:** Approved data sheets and schedules

### Step 6: Issue

**Activities:**
- Issue to project DMS
- Transmit per distribution list
- Update `_STATUS.md`

**Deliverables:** Issued data sheet package

## Verification

**V1: Coordination Check** (Step 4) — Verify data matches drawings, specifications, calculations
**V2: Completeness Check** (Step 4) — Verify all doors/windows included

**Acceptance Criteria:**
- Data sheets complete and accurate
- Schedules complete and coordinated
- **TBD** — Employer approval

## Records

**Required Outputs:**
1. Building System Data Sheet
2. Door Schedule
3. Window Schedule

**Record Management:** `1_Working/` → `2_Checking/` → `3_Issued/` per `_STATUS.md`

---

**Procedure Revision History:**

| Date | Revision | Description | Author |
|------|----------|-------------|--------|
| 2026-01-28 | 0 | Initial procedure draft | 4_DOCUMENTS Agent |
