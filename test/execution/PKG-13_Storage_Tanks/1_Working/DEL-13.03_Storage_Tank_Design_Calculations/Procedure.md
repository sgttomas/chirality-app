# Procedure: DEL-13.03 Storage Tank Design Calculations

## Purpose

This procedure defines the process for producing **Storage Tank Design Calculations** (API 650 tank design, foundation loading, seismic analysis).

**Deliverable type:** Calculation
**Responsible party:** D&B Contractor

---

## Prerequisites

**Dependencies:** NOT_TRACKED — Coordinated externally (see `_DEPENDENCIES.md`)

**Upstream inputs:**
- Design Basis Memorandum — **TBD**
- DEL-02.04: Geotechnical Reports (bearing capacity, settlement) — **TBD**
- Product specification (SG, temperature) — **TBD**
- ER design criteria (wind, snow, seismic parameters) — **TBD**

**Reference materials:**
- API 650 (including Appendices B, E), NBC 2020
- Project calculation template — **TBD**

**Personnel:**
- Calculation Engineer (P.Eng. or under supervision)
- Independent Checker (P.Eng. or qualified engineer)
- Discipline Lead (P.Eng.)

**Software (if used):**
- **TBD** — Tank design software, spreadsheet tools; validation status required

---

## Steps

### Step 1: Input Data Collection and Review
**Activities:**
1.1. Review ER for design criteria (wind, snow, seismic, temperature)
1.2. Obtain product data (SG, operating temperature range)
1.3. Review geotechnical report (DEL-02.04) for bearing capacity and settlement limits
1.4. Confirm tank capacity requirement (15,000 MT per tank)
1.5. Identify site constraints (footprint, height limits, access)

**Outputs:** Input data register

### Step 2: Trial Geometry Selection
**Activities:**
2.1. Establish trial tank diameter and height based on capacity and constraints
2.2. Typical starting point: D/H ratio ~1.5:1 for large atmospheric tanks
2.3. Calculate liquid volume and verify capacity
2.4. Document trial geometry

**Outputs:** Trial tank geometry (D, H)

### Step 3: Shell Thickness Calculation
**Activities:**
3.1. Calculate hydrostatic pressure at each shell course
3.2. Apply API 650 Equation 5-2 for required thickness
3.3. Check minimum thickness per API 650 Table 5-1a
3.4. Add corrosion allowance if applicable — **TBD**
3.5. Select commercial plate thicknesses
3.6. Calculate shell weight

**Outputs:** Shell course thicknesses

### Step 4: Bottom and Roof Design
**Activities:**
4.1. Design bottom plates per API 650 Sections 5.4 and 5.5 (annular plate if required)
4.2. Design roof per API 650 Section 5.10 (cone, dome, or floating)
4.3. Calculate roof structural members if required
4.4. Check roof loading (dead + live + snow)

**Outputs:** Bottom and roof design

### Step 5: Wind Stability Check
**Activities:**
5.1. Calculate wind loads per NBC 2020
5.2. Check shell stability per API 650 Section 5.9
5.3. Determine if wind girders or stiffeners required
5.4. Design wind girders if needed

**Outputs:** Wind stability verification, wind girder design (if required)

### Step 6: Seismic Analysis
**Activities:**
6.1. Obtain site seismic parameters (PGA, spectral acceleration) from NBC 2020 or site study — **TBD**
6.2. Perform seismic analysis per API 650 Appendix E:
    - Calculate impulsive and convective components
    - Calculate base shear and overturning moment
    - Determine anchorage requirement (anchored vs. unanchored)
6.3. If anchored: Design anchor bolts and anchor chairs; check shell compression
6.4. If unanchored: Check base plate yielding per Appendix E

**Outputs:** Seismic analysis, anchorage design (if required)

### Step 7: Nozzle Reinforcement
**Activities:**
7.1. Review nozzle schedule from process requirements — **TBD**
7.2. Calculate reinforcement area per API 650 Section 5.7
7.3. Design reinforcement pads if required

**Outputs:** Nozzle reinforcement design

### Step 8: Foundation Loading
**Activities:**
8.1. Calculate dead load (empty tank weight)
8.2. Calculate live load (product weight, roof live load)
8.3. Calculate wind and seismic loads (overturning moment, base shear)
8.4. Develop load combinations per NBC 2020
8.5. Calculate bearing pressure distribution
8.6. Check bearing pressure vs. allowable (from DEL-02.04)
8.7. Estimate settlement and check vs. API 650 Appendix B limits

**Outputs:** Foundation loading summary, settlement estimate

### Step 9: Results Summary and Compliance Check
**Activities:**
9.1. Summarize all calculation results in tables
9.2. Verify compliance with API 650 and NBC 2020
9.3. Check utilization ratios for critical elements
9.4. Document conclusions and recommendations

**Outputs:** Results summary, compliance statements

### Step 10: Self-Check
**Activities:**
10.1. Originator reviews calculation for completeness, accuracy, clarity
10.2. Verify input data sources are documented
10.3. Verify assumptions are stated and justified
10.4. Correct errors or omissions

**Outputs:** Self-checked calculation

### Step 11: Independent Check
**Activities:**
11.1. Independent checker reviews calculation:
     - Methodology appropriate and compliant with API 650
     - Input data correct and sourced
     - Spot-check calculations (20% minimum, all critical elements)
     - Results reasonable and supported
11.2. Checker provides comments
11.3. Originator resolves comments
11.4. Checker signs off

**Outputs:** Checked calculation

### Step 12: Design Review (if required)
**Activities:**
12.1. Present key results in design review meeting
12.2. Review geometry, shell thicknesses, seismic anchorage decision, foundation loads
12.3. Document review minutes and action items

**Outputs:** Design review minutes

### Step 13: Approval and Issuance
**Activities:**
13.1. Discipline Lead reviews and approves (sign and stamp)
13.2. Issue for design use: File in `3_Issued/`
13.3. Provide results to DEL-13.01 (drawings) and DEL-13.02 (specification)

**Outputs:** Approved calculations

---

## Verification

Verification per Specification.md Section: Verification (V-01 through V-03)
- Step 10: Self-check
- Step 11: Independent check
- Step 12: Design review (if required)

**Acceptance Criteria:** Per Specification.md AC-01 through AC-05

---

## Records

**Outputs:** API 650 tank design calculations (3), foundation loading calculations, seismic calculations
**Filing:** `2_Checking/` (review) → `3_Issued/` (approved)

**Cross-Document References:**
**See Datasheet.md:** Calculation types, inputs, outputs, load cases
**See Specification.md:** Requirements for calculations (FR, CR, PR series)
**See Guidance.md:** API 650 methodology, seismic principles, trade-offs

---

**Document Status:** Pass 3 (Final) — Enrichment complete. 13-step workflow for API 650 tank design calculations. Cross-document consistency verified. Ready for WORKING_ITEMS refinement.

**Last Updated:** 2026-01-28
