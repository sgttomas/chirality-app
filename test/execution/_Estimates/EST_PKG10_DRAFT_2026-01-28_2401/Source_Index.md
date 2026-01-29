# Source Index

## Overview

This index lists all pricing and quantity sources discovered and used for the PKG-10 estimate, organized by priority.

---

## 1. Explicit Pricing Sources (Highest Priority)

**Status:** None found

**Search Conducted:**
- Searched `execution/_Estimates/_RateTables/` for rate tables: directory empty
- Searched project workspace for vendor quotes, budgetary proposals, budget sheets: none found for PKG-10 scope
- Searched deliverable folders for pricing references in `_REFERENCES.md` files: no pricing sources listed

**Result:** No explicit pricing sources available. Proceeded to fallback typical model.

**Decision Ref:** D-007

---

## 2. Rate Tables / Cost Libraries

**Status:** None found

**Search Conducted:**
- `execution/_Estimates/_RateTables/`: directory exists but contains no rate table files
- Project workspace search for files matching "rate", "unit cost", "cost library", "pricing": no results for PKG-10 equipment

**Result:** No project rate tables available. All pricing via allowances.

**Decision Ref:** D-007

---

## 3. Quantity Sources

**Status:** Partial (decomposition and deliverable datasheets)

**Sources Used:**

### 3.1 Decomposition (Primary Scope Source)

**Location:** `/Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md`

**Information Extracted:**
- Section 1 Key Parameters: 32 railcar unloading stations (confirmed quantity)
- Section 1 Key Parameters: 1,000,000 MT/annum throughput capacity
- Section 5 PKG-10 Scope: Unloading arms, quick-connects, gravity flow header, spill containment pans, collection system, atmospheric venting, flow indicators
- Section 5 PKG-10 Deliverables: 5 deliverables (DEL-10.01 through DEL-10.05)

**Line Items Supported:**
- L-001 through L-005 (5 deliverables confirmed from decomposition)
- L-006 (32 unloading arms from "32 railcar unloading stations")
- L-007 (32 quick-connects from "32 stations" and "quick-connects" scope element)
- L-011 (32 flow indicators from "32 stations" and "flow indicators" scope element)

**Confidence:** HIGH for deliverable count and 32-station quantity; MEDIUM for equipment configuration

---

### 3.2 DEL-10.01 Datasheet (Scope Detail)

**Location:** `/Users/ryan/ai-env/projects/chirality-app/test/execution/PKG-10_Railcar_Unloading_System/1_Working/DEL-10.01_Railcar_Unloading_Design_Drawing_Set/Datasheet.md`

**Information Extracted:**
- Section "Conditions" — PKG-10 Scope Elements table: confirms 32 unloading arms, 32 quick-connects, gravity flow header (single system with branch connections), 32 spill containment pans, sumps/drains/sump pumps, 32 atmospheric vent connections, 32 flow indicators
- Section "Construction" — Drawing Set Composition: identifies 4 drawing types required (GA, Arm Arrangement, Header Layout, Containment Details)

**Line Items Supported:**
- L-001 (drawing set scope confirmed)
- L-006, L-007, L-009, L-011, L-012 (equipment quantities confirmed: 32 arms, 32 couplers, 32 pans, 32 indicators, 32 vents)
- L-008 (header piping — single system with 32 branches confirmed)

**Confidence:** HIGH for equipment counts (32 confirmed); LOW for equipment sizing/configuration

---

### 3.3 DEL-10.02 Datasheet (Equipment Specification Scope)

**Location:** `/Users/ryan/ai-env/projects/chirality-app/test/execution/PKG-10_Railcar_Unloading_System/1_Working/DEL-10.02_Railcar_Unloading_Technical_Specification/Datasheet.md`

**Information Extracted:**
- Section "Conditions" — PKG-10 Scope Elements table: confirms equipment scope and specification coverage
- Section "Construction" — Specification Document Structure: identifies 3 main specification sections (Unloading Arm Specification, Containment System Specification, Header Pipe Specification)

**Line Items Supported:**
- L-002 (specification scope confirmed)
- Equipment specifications confirmed: arms, couplers, header, containment, pumps

**Confidence:** MEDIUM for specification scope; equipment details TBD

---

### 3.4 DEL-10.04 Datasheet (Equipment Data Sheet Scope)

**Location:** `/Users/ryan/ai-env/projects/chirality-app/test/execution/PKG-10_Railcar_Unloading_System/1_Working/DEL-10.04_Railcar_Unloading_Data_Sheet_Package/Datasheet.md`

**Information Extracted:**
- Section "Attributes": 32 unloading arm data sheets + quick-connect coupler data sheets (32 individual or combined with arm sheets) + sump pump data sheet(s) (quantity TBD)
- Section "Construction" — Equipment Covered table: confirms 32 unloading arms, 32 quick-connect couplers, sump pumps (quantity TBD per containment design)

**Line Items Supported:**
- L-004 (data sheet package scope confirmed: 32+ data sheets)
- L-006, L-007 (32 arms, 32 couplers confirmed)
- L-010 (sump pump quantity TBD; used assumption A-005 for 8 pumps)

**Confidence:** HIGH for arm/coupler count (32 confirmed); LOW for pump count (TBD in source)

---

### 3.5 DEL-10.03 Datasheet (Calculation Scope)

**Location:** `/Users/ryan/ai-env/projects/chirality-app/test/execution/PKG-10_Railcar_Unloading_System/1_Working/DEL-10.03_Railcar_Unloading_Design_Calculations/Datasheet.md`

**Information Extracted:**
- Section "Construction" — Calculation Scope table: header pipe sizing, unloading rate calculations, containment volume calculations
- Section "Conditions" — Design Basis Parameters: throughput (1,000,000 MT/annum), product (canola oil), gravity flow method

**Line Items Supported:**
- L-003 (calculation scope confirmed: 3 major calculation topics)
- Calculation scope informs equipment sizing basis (header diameter, containment volume, throughput verification)

**Confidence:** MEDIUM for calculation scope; quantities TBD pending calculation completion

---

## 4. Fallback Typical Model (Last Resort)

**Status:** Used for all pricing

**Source:** AGENT_ESTIMATING instructions — "Fallback Typical Model (Embedded)" section

**Application:**

### 4.1 Equipment Allowances

Applied fallback typical model for equipment pricing due to absence of vendor quotes:

| Equipment | Typical Range | Selected Value | Assumption Ref |
|-----------|--------------|----------------|----------------|
| Railcar unloading arms | $45k-60k/unit | $50k/unit | A-001 |
| Quick-connect couplers | $2.5k-3.5k/unit | $3k/unit | A-002 |
| Header piping (8-12 inch) | $600-800/lm | $700/lm | A-003 |
| Containment pans (fabricated) | $7k-9k/unit | $8k/unit | A-004 |
| Sump pumps | $5k-7k/unit | $6k/unit | A-005 |
| Flow indicators (local) | $2k-3k/unit | $2.5k/unit | A-011 |

**Confidence:** LOW (industry typical ranges; project-specific variance expected)

**Justification:** Fallback typical model provides runnable placeholder pricing enabling estimate completion. All flagged as Method=ALLOWANCE with Confidence=LOW and traceable to assumption log entries.

---

### 4.2 Labor Allowances

Applied fallback typical model for labor productivity and rates:

| Activity | Typical Productivity | Typical Rate | Assumption Ref |
|----------|---------------------|--------------|----------------|
| Unloading arm installation | 70-80 hrs/unit | $110/hr all-in | A-015 |
| Piping installation (8-12 inch) | 4-5 hrs/lm | $110/hr all-in | A-016 |
| Containment pan installation | 40 hrs/unit | $110/hr all-in | A-017 |
| Sump pump installation | 25 hrs/unit | $110/hr all-in | A-018 |
| Flow indicator installation | 8-10 hrs/unit | $110/hr all-in | A-019 |

**Confidence:** LOW (industry typical; project-specific variance expected)

**Justification:** All-in rate of $110/hr CAD reflects BC lower mainland construction composite rate (fitter + helper + supervision markup). Productivity estimates based on industry typical for similar work.

---

### 4.3 Engineering Allowances

Applied fallback typical model for engineering effort:

| Deliverable | Typical Effort | Basis | Assumption Ref |
|-------------|---------------|-------|----------------|
| Design Drawing Set | 400-500 hrs | GA + 32 arm arrangements + header layout + containment details | A-006 |
| Technical Specification | 130-160 hrs | 3 major specification sections (arms, header, containment) | A-007 |
| Design Calculations | 200-250 hrs | 3 calculation topics (header sizing, throughput, containment) | A-008 |
| Data Sheet Package | 160-200 hrs | 32 arm sheets + coupler sheets + pump sheets | A-009 |
| Installation & Test Records | 90-110 hrs | FAT records + installation records + test records | A-010 |

Engineering rate assumed: $135/hr CAD loaded (engineering labor rate typical for BC)

**Confidence:** LOW (effort estimates vary with design complexity and project standards)

---

### 4.4 Indirects Factors (Fallback Typical Model)

Applied per AGENT_ESTIMATING "Default factors":

| Factor | Rate | Base | Result | Decision Ref |
|--------|------|------|--------|--------------|
| Construction Indirects (CI) | 18% | CD ($717,000) | $129,000 | D-008 |
| Procurement Services (P) | 2% | MAT ($2,555,000) | $51,000 | D-008 |
| EPCM/PM | 6% | CD + CI + MAT ($3,401,000) | $204,000 | D-008 |

**Confidence:** MEDIUM (factors are typical industry averages; project-specific factors may vary ±25%)

**Justification:** Factor-based indirects used due to absence of schedule/duration data for time-based calculation. Factors per embedded fallback typical model.

---

### 4.5 Contingency (Fallback Typical Model)

Applied PCT_BY_BUCKET method with allowance-heavy adjustments per AGENT_ESTIMATING:

**Base contingency by CBS:**
- E, PM, P: 10%
- MAT: 15%
- CD, CI: 20%
- COM: 25%

**Allowance adjustments:**
- E, MAT, CD: +10% (100% allowance share)
- CI, COM: +10% (factor-derived or high allowance)
- PM, P: +5% (factor-derived)

**Final contingency %:**
- E: 20%, MAT: 25%, CD: 30%, CI: 30%, PM: 15%, P: 15%, COM: 30%

**Decision Ref:** D-009

**Confidence:** MEDIUM (contingency method is sound; rates reflect estimate uncertainty)

---

## Source Priority Summary

**Priority 1 (QUOTE):** 0 sources used (0% of estimate)

**Priority 2 (RATE_TABLE):** 0 sources used (0% of estimate)

**Priority 3 (QUANTITY SOURCES):** 5 sources used (deliverable datasheets + decomposition) — quantities for 32 stations confirmed; equipment sizing TBD

**Priority 4 (FALLBACK MODEL):** Applied for all pricing (100% of estimate by value)

**Overall Source Quality:** LOW (no quotes or rate tables; quantities confirmed but equipment sizing/configuration TBD)

**Improvement Path:** Obtain vendor quotes for major equipment (Priority 1 sources) to replace fallback allowances.

---

*Source index compiled per AGENT_ESTIMATING Phase 2.2 (Build Source Index). All sources documented for audit trail and reproducibility.*
