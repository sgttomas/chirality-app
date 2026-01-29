# Basis of Estimate (BoE) — PKG-05 Concrete Structures

**Snapshot ID:** EST_PKG05_DRAFT_2026-01-28_2400
**Estimate Label:** PKG05_DRAFT
**Package Scope:** PKG-05 Concrete Structures
**Date:** 2026-01-28
**Prepared By:** Estimating Agent (Automated Pipeline)

---

## Executive Summary

This Basis of Estimate documents the methods, sources, assumptions, and decisions used to prepare the PKG-05 Concrete Structures cost estimate.

**Total Estimate:** $2,552,000 CAD (rounded, includes contingency)
**Base Estimate:** $2,101,000 CAD (before contingency)
**Contingency:** $451,000 CAD (21.5% blended rate)
**Currency:** CAD (Canadian dollars)
**Pricing Date:** January 2026
**Confidence:** LOW (86.9% allowance-based; no vendor quotes)
**Maturity:** Class 5 (Conceptual / Order of Magnitude)

---

## 1. Project Overview

### 1.1 Project Description

**Project:** Canola Oil Transload Facility — Phase 1 Design & Build Contract

**Employer:** DP World Fraser Surrey Inc.

**Location:** Fraser Surrey Terminal, 11060 Elevator Road, Surrey, BC

**Key Parameters:**
- Permitted Throughput: 1,000,000 MT per annum
- Storage Capacity: 45,000 MT (3 × 15,000 MT tanks)
- Product: CSD (Crude Super Degummed) canola oil
- Railcar Capacity: 32 unloading stations on 2 tracks
- Contract Type: Design & Build

**Source:** Decomposition document Section 1, `/Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md`

---

### 1.2 PKG-05 Concrete Structures Scope

**Package Description:** Foundations, containment walls, equipment pads, thrust blocks, ground liner system.

**Discipline:** Structural

**Deliverables Included (4 total):**

| ID | Deliverable | Type | Artifacts |
|----|-------------|------|-----------|
| DEL-05.01 | Concrete Structures Design Drawing Set | Drawing | Foundation plans, containment walls, equipment pads, reinforcement drawings |
| DEL-05.02 | Concrete Structures Technical Specification | Specification | Concrete spec, reinforcement spec, formwork spec |
| DEL-05.03 | Concrete Structures Design Calculations | Calculation | Foundation calcs, containment wall calcs, seismic analysis |
| DEL-05.04 | Concrete Structures Installation & Test Records | Record | Pour records, cylinder tests, rebar inspection records |

**Physical Scope Elements:**
- Tank foundations for 3 × 15,000 MT storage tanks (ring wall type assumed)
- Secondary containment walls for tank farm (supports OBJ-7 Environmental Protection)
- Equipment pads for pumps, metering, and railcar unloading equipment
- Thrust blocks for underground piping systems
- Ground liner system interface work

**Source:** Decomposition Section 5, PKG-05, lines 222-236.

---

### 1.3 Objective Mapping

PKG-05 deliverables support the following project objectives:

| Objective | Description | PKG-05 Relevance |
|-----------|-------------|------------------|
| OBJ-3 | Storage Capacity (45,000 MT) | Tank foundations support 3 × 15,000 MT tanks |
| OBJ-7 | Environmental Protection | Containment walls with waterstops prevent spills |

**Source:** Decomposition Section 6, lines 782, 786.

---

## 2. Estimate Scope and Basis

### 2.1 Inclusions

This estimate includes the following CBS categories:

- **Engineering & Design (E):** Design drawings, specifications, design calculations
- **Project Management (PM):** QA/QC documentation, EPCM allocation
- **Procurement (P):** Vendor coordination, expediting services (factor-based)
- **Materials (MAT):** Concrete, reinforcing steel, formwork, waterstops, joint materials
- **Construction Directs (CD):** Concrete placement, rebar installation, formwork erection
- **Construction Indirects (CI):** Concrete testing/QC, field supervision, site overhead

**Source:** `_CONFIG.md`; AGENT_ESTIMATING default CBS structure.

---

### 2.2 Exclusions

This estimate explicitly excludes:

- **Owner's costs:** Employer's project management, Owner's Engineer fees, financing costs
- **Land acquisition:** Site purchase or lease costs (existing terminal)
- **Permits obtained by Employer:** Environmental permits, terminal operating permits procured by DP World
- **Other packages:** PKG-00 through PKG-04 and PKG-06 through PKG-35 (estimated separately)
- **Deep foundations:** Piling if required by geotechnical conditions (would be PKG-05 scope addition)
- **Marine structures concrete:** Covered under PKG-08
- **Building concrete:** Covered under PKG-21/PKG-22
- **Escalation:** Cost growth over time not applied (January 2026 pricing basis)
- **Taxes:** GST/PST or other sales taxes not included

**Source:** `_CONFIG.md`; Decomposition Section 1.2 (Contractor scope boundary); Decision D-001.

---

### 2.3 Contracting Assumptions

**Contract Type:** Design & Build (EPCM-style delivery)

**Delivery Model Assumptions:**
- Contractor responsible for design, procurement, construction of concrete structures
- Concrete supplied by ready-mix from local batching plants (BC Lower Mainland)
- Reinforcing steel fabricated off-site and delivered
- Formwork systems rented or contractor-owned
- Third-party testing services for concrete and rebar inspection

**Pricing Basis:**
- Parametric quantities derived from tank parameters (no detailed QTO)
- Unit rate allowances for concrete, rebar, formwork
- Lump-sum allowances for engineering deliverables
- Factor-based indirects (CI, PM, Procurement) per typical EPC ratios

**Source:** Decomposition Section 1.1 (contract type); typical D&B contracting conventions.

---

## 3. Pricing Sources and Methods

### 3.1 Source Hierarchy

Per AGENT_ESTIMATING protocol, pricing sources are applied in priority order:

1. **Vendor quotes / budgetary proposals** (highest priority)
2. **Project rate tables / cost libraries**
3. **Allowances / parametric models** (fallback)

**For This Estimate:**
- **Quotes:** 0% of base cost (none available)
- **Rate tables:** 0% of base cost (none available)
- **Allowances:** 86.9% of base cost ($1,807,800)
- **Parametric factors:** 13.1% of base cost ($273,607 — calculated indirects)

**Source Selection Decision:** D-005 (use fallback model due to absence of project-specific sources)

**Source Index:** See `Source_Index.md` for detailed source discovery findings.

---

### 3.2 Pricing Method by CBS

| CBS | Method | Base Cost (CAD) | Rationale |
|-----|--------|-----------------|-----------|
| E | ALLOWANCE | $250,000 | No engineering labor rates; allowances based on typical structural design costs |
| PM | ALLOWANCE + PARAMETRIC | $146,871 | QA/QC records allowance + calculated PM factor (6%) |
| P | PARAMETRIC | $17,016 | Procurement services calculated as 2% of materials |
| MAT | ALLOWANCE | $850,800 | No vendor quotes; parametric quantities with typical unit rates |
| CD | ALLOWANCE | $647,000 | No labor rates; parametric quantities with typical installation rates |
| CI | ALLOWANCE + PARAMETRIC | $209,720 | Testing allowance + calculated CI factor (18% of CD) |

**Allowance Convention:** All lump-sum allowances use Qty=1, Unit=LS, UnitRate=Amount per SPEC requirements.

---

### 3.3 Quantity Derivation Methodology

**Approach:** Quantities parametrically derived from known tank parameters.

**Key Parameters Used:**
- Storage capacity: 45,000 MT (3 × 15,000 MT tanks)
- Product specific gravity: 0.92 (typical canola oil)
- Tank volume per tank: ~16,300 m³
- Tank diameter (assumed from volume): ~32m

**Derived Quantities:**

| Element | Quantity | Unit | Derivation Method |
|---------|----------|------|-------------------|
| Tank foundation concrete | 450 | m³ | Ring wall dimensions for 32m tanks |
| Containment wall concrete | 600 | m³ | 110% containment volume, perimeter walls |
| Equipment pad concrete | 200 | m³ | Typical pad sizes for equipment types |
| Thrust block concrete | 80 | m³ | 20 locations × 4 m³ average |
| Reinforcing steel | 180,000 | kg | 100-150 kg/m³ ratio by element |
| Wall formwork | 1,500 | m² | Wall perimeter × height × 2 sides |

**Source:** Decision D-010 (Quantities — Parametric); Assumptions A-005 through A-010.

---

### 3.4 Unit Rate Assumptions

| Item | Unit | Rate (CAD) | Basis |
|------|------|------------|-------|
| Ready-mix concrete (standard) | m³ | $220 | Typical BC Lower Mainland pricing |
| Ready-mix concrete (containment) | m³ | $240 | Premium for low-permeability mix |
| Concrete placement (slab/foundations) | m³ | $180 | Typical installation cost |
| Concrete placement (walls) | m³ | $350 | Complex formwork, waterstops |
| Reinforcing steel (fabricated, delivered) | kg | $2.00 | Typical rebar supply pricing |
| Reinforcing steel (installed) | kg | $1.00 | Typical placement cost |
| Formwork (rental + installation) | m² | $90 | Combined rate for wall forms |

**Source:** Fallback typical model per Decision D-005; BC construction market context.

---

### 3.5 Fallback Typical Model Disclosure

**Usage:** Primary pricing basis for this estimate (no project-specific sources available)

**Fallback Model Components Used:**

1. **Indirects Factors:**
   - Construction Indirects (CI) = 18% of CD
   - Procurement (P) = 2% of MAT
   - EPCM/PM = 6% of (CD + CI + MAT)

2. **Unit Rate Assumptions:**
   - Concrete supply and placement rates per BC market
   - Rebar supply and installation rates per typical pricing
   - Formwork rates for industrial construction

3. **Contingency Baseline:**
   - E, PM, P: 10% base + allowance adjustment
   - MAT: 15% base + allowance adjustment
   - CD, CI: 20% base + allowance adjustment

**Transparency Requirement:** All fallback model uses are labeled as `Method=ALLOWANCE` or `Method=PARAMETRIC`, marked `Confidence=LOW` or `MED`, and traced to Decision D-005, D-006, or D-010.

**Source:** AGENT_ESTIMATING STRUCTURE section (Fallback Typical Model).

---

## 4. Currency and Pricing Date

### 4.1 Currency

**Currency:** CAD (Canadian dollars)

**Decision:** D-002 (Currency Selection — CAD)

**Rationale:** Project location is Fraser Surrey Terminal, Surrey, BC (Canadian location). No mixed currencies in this estimate; all costs expressed in CAD.

**Conversion Assumptions:** None required (all costs assumed to be in CAD).

---

### 4.2 Pricing Date

**Pricing Date:** January 2026 ("dollars of" January 2026)

**Decision:** D-003 (Pricing Date — January 2026)

**Rationale:** No historical pricing dates found in deliverable documents. Defaulted to current date (2026-01-28).

**Escalation:** Not applied in this estimate (escalation_mode = NONE per `_CONFIG.md`).

**Note:** If construction extends over multiple years from January 2026, actual costs will be subject to escalation. See Risk R-008 for escalation exposure discussion.

---

## 5. Estimate Methodology

### 5.1 WBS to CBS Mapping

Each deliverable and scope element mapped to primary CBS bucket(s) based on deliverable type and content. Mapping documented in `WBS_CBS_Matrix.csv`.

**Mapping Logic:**
- **Drawing deliverables** (DEL-05.01) → Engineering (E)
- **Specification deliverables** (DEL-05.02) → Engineering (E)
- **Calculation deliverables** (DEL-05.03) → Engineering (E)
- **Record deliverables** (DEL-05.04) → Project Management (PM)
- **Physical concrete work** → Materials (MAT) + Construction Directs (CD)
- **Testing and QC** → Construction Indirects (CI)

---

### 5.2 Quantity Extraction

**Source:** Deliverable Datasheet.md and Specification.md files in each DEL folder.

**Findings:**
- **Deliverable quantities extracted:** All 4 deliverables have artifact counts
- **Physical quantities:** Derived parametrically from tank parameters (not extracted from design documents)

**Quantities Successfully Derived:**
- Tank foundation concrete: 450 m³ (3 tanks × 150 m³ ring wall each)
- Containment wall concrete: 600 m³ (300m perimeter × 2.5m height × 0.3m avg)
- Equipment pad concrete: 200 m³ (various pads)
- Thrust block concrete: 80 m³ (20 locations)
- Reinforcing steel: 180,000 kg (100-150 kg/m³ ratio)
- Wall formwork: 1,500 m² (containment walls)

**Quantities NOT Extracted (TBD):**
- Exact foundation dimensions (pending design)
- Exact wall heights and thicknesses (pending design)
- Equipment pad sizes (pending interface inputs)
- Thrust block locations (pending piping layout)
- Detailed rebar schedules (pending design)

**Impact:** Quantities carry ±30-45% uncertainty.

**Source:** Exploration findings; parametric derivation per D-010.

---

### 5.3 Pricing Methodology

**Primary Method:** ALLOWANCE (parametric quantities × unit rate allowances)

**Allowance Sizing Approach:**
- Engineering deliverables: Typical EPC cost per drawing/specification/calculation based on complexity
- Physical works: Parametric quantities × typical BC construction unit rates
- Indirects: Factor-based per fallback model

**Fallback Model Application:**
- No vendor quotes or rate tables available (see Source_Index.md)
- All allowances documented in Assumptions_Log.md (A-001 through A-013)
- Quantities assigned ±30-45% ranges to reflect uncertainty

**Source:** Decision D-005, D-006, D-010; AGENT_ESTIMATING fallback model.

---

## 6. Location and Productivity Assumptions

### 6.1 Location

**Location:** Fraser Surrey Terminal, 11060 Elevator Road, Surrey, BC

**Location Factors:**
- **Labor market:** Vancouver/Lower Mainland BC labor rates assumed
- **Concrete supply:** Ready-mix from local batching plants; no premium for distance
- **Access:** Marine terminal with road and rail access
- **Site conditions:** Existing operating terminal; work coordination required

**Location Adjustments:** None applied (base rates assume BC Lower Mainland pricing).

---

### 6.2 Productivity Assumptions

**Baseline Productivity:** Typical EPC project productivity assumed

**Productivity Constraints:**
- **Terminal operational interface:** Work coordination with active terminal operations may affect productivity
- **Containment wall construction:** Complex formwork and waterstop installation requires skilled crews
- **Weather:** BC coastal weather may affect concrete placement schedules

**Productivity Factors Applied:** None explicitly calculated; productivity constraints embedded in contingency.

**Source:** Risk R-010 (Labor availability and productivity).

---

## 7. Indirects Model

**Model Type:** Factor-based (default per D-006)

**Rationale:** Construction schedule with detailed durations not available; factor-based model is appropriate for conceptual estimate maturity.

**Factors Applied:**

| Indirect Category | Factor | Basis | Calculated Amount (CAD) |
|-------------------|--------|-------|-------------------------|
| Construction Indirects (CI) | 18% | Construction Directs (CD) = $647k | $116,460 |
| EPCM / Project Management (PM) | 6% | CD + CI + MAT = $1,864k | $111,871 |
| Procurement Services (P) | 2% | Materials (MAT) = $850.8k | $17,016 |

**Construction Indirects Include:**
- Field supervision and construction management
- Site overhead
- QA/QC and inspection
- HSE and safety management

**Note:** CI includes both calculated factor ($116.5k) and direct testing allowance ($65k from A-013) for total CI = $209.7k.

**Source:** AGENT_ESTIMATING fallback model indirects factors; Decision D-006.

---

## 8. Contingency Method and Rationale

### 8.1 Method

**Contingency Method:** PCT_BY_BUCKET (percentage by CBS bucket)

**Decision:** D-008 (Contingency Method — Percentage by Bucket)

**Rationale:** Risk-based three-point estimation not feasible without vendor quotes and project-specific risk data. Percentage-by-bucket method appropriate for conceptual estimate with high allowance content.

---

### 8.2 Contingency Rates

**Baseline Rates (from fallback model):**
- Engineering, PM, Procurement: 10%
- Materials: 15%
- Construction Directs, Indirects: 20%

**Allowance-Heavy Adjustment:**
- +5% if bucket allowance share ≥ 50%
- +10% if bucket allowance share ≥ 80%

**Applied Rates (PKG-05 Estimate):**

| CBS | Base (CAD) | Allowance Share | Base Rate | Adjustment | Final Rate | Contingency (CAD) |
|-----|------------|-----------------|-----------|------------|------------|-------------------|
| E | $250,000 | 100% | 10% | +5% | **15%** | $37,500 |
| PM | $146,871 | 24% | 10% | 0% | **15%** | $22,031 |
| P | $17,016 | 0% | 10% | 0% | **15%** | $2,552 |
| MAT | $850,800 | 100% | 15% | +5% | **20%** | $170,160 |
| CD | $647,000 | 100% | 20% | +5% | **25%** | $161,750 |
| CI | $209,720 | 31% | 20% | 0% | **25%** | $52,430 |

**Total Contingency:** $446,423 CAD (21.5% blended rate)

**Source:** AGENT_ESTIMATING fallback model contingency; Decision D-008.

---

### 8.3 Contingency Rationale

**Primary Risk Drivers:**
1. **Pricing uncertainty:** No vendor quotes (R-001) — 86.9% of costs are allowances
2. **Quantity gaps:** Parametric quantities (R-002) — ±30-45% uncertainty
3. **Foundation type:** Ring wall assumed (R-003) — could increase if mat required
4. **Geotechnical unknown:** Foundation conditions pending (R-004)

**Contingency Adequacy:**
- **Adequate** for normal project risks and moderate adjustments
- **Marginally adequate** for foundation type change or geotechnical issues
- **Insufficient** if multiple high-impact risks materialize

**Recommendation:** Update estimate as designs and quotes become available; refine contingency based on actual risk profile.

**Source:** Risk_Register.md; Contingency Adequacy Assessment.

---

## 9. Escalation Method and Rationale

### 9.1 Method

**Escalation Mode:** NONE (not applied)

**Decision:** D-009 (Escalation — Not Applied)

**Rationale:**
- Estimate represents January 2026 pricing basis
- Construction schedule with cashflow curve not available
- Draft estimate maturity does not warrant escalation precision

---

### 9.2 Escalation Exposure

**Project Duration:** Assumed 24-30 months (typical for multi-year EPC project)

**Escalation Risk:** Cost escalation over 2-2.5 years could add 3-5% annually

**Cost Exposure:** $90k - $150k on $1.5M physical work base (6-10% cumulative)

**Recommendation:** Enable escalation in future estimates once construction schedule available.

**Source:** Risk R-008; typical escalation rates for industrial construction.

---

## 10. Rounding Policy

**Rounding:** Nearest $1,000 CAD

**Decision:** D-007 (Rounding Policy — Nearest $1,000)

**Application:**
- Detail.csv line items: Calculated precision retained
- Summary.md totals: Rounded to nearest $1,000
- Final total estimate: Rounded to nearest $1,000

**Rationale:** $1,000 rounding appropriate for conceptual estimate in $2-3M range; avoids false precision.

---

## 11. Completeness Metrics

### 11.1 Pricing Method Distribution

| Method | Line Count | Base Cost (CAD) | % of Base |
|--------|------------|-----------------|-----------|
| QUOTE | 0 | $0 | 0% |
| RATE_TABLE | 0 | $0 | 0% |
| ALLOWANCE | 21 | $1,807,800 | 86.9% |
| PARAMETRIC | 3 | $273,607 | 13.1% |

---

### 11.2 Quantity Extraction Success Rate

| Deliverable Category | Extracted | Not Extracted | Success Rate |
|----------------------|-----------|---------------|--------------|
| Deliverable artifact counts | 4/4 | 0/4 | 100% |
| Physical construction quantities | 0/4 | 4/4 | 0% (parametric) |

**Overall Quantity Extraction:** 50% (deliverable counts yes; physical quantities derived parametrically)

---

### 11.3 Estimate Maturity Classification

**Class:** Class 5 (Order of Magnitude / Conceptual)

**Characteristics (per AACE International):**
- End usage: Concept screening, feasibility
- Methodology: Capacity-factored, parametric models, allowances
- Expected accuracy: -20% to -50% (low) / +30% to +100% (high)

**PKG-05 Estimate Accuracy Range:** -30% / +50% (conservative within Class 5 range)

---

## 12. Known Gaps and Limitations

### 12.1 Critical Gaps

1. **No vendor quotes** — All material and installation costs are allowances
2. **Parametric quantities** — Derived from tank parameters, not design documents
3. **Foundation type uncertain** — Ring wall assumed; mat foundation could add 50-100%
4. **Geotechnical parameters unknown** — Foundation design pending PKG-02 inputs
5. **ER requirements not extracted** — Specific concrete/containment requirements TBD

**Impact:** Estimate suitable for conceptual budgeting only; not suitable for contracting or procurement.

---

### 12.2 Limitations

1. **Single-point allowances:** Ranges documented but not reflected in deterministic totals
2. **No sensitivity analysis:** Impact of varying key assumptions not quantified
3. **No benchmarking:** Estimate not compared to historical similar projects

---

## 13. References to Supporting Documents

| Document | Purpose |
|----------|---------|
| Decision_Log.md | Documents all defaults, ambiguities, and choices (11 decisions) |
| Assumptions_Log.md | Documents all allowances and ranges (13 assumptions) |
| Source_Index.md | Catalogs pricing and quantity sources discovered (none available) |
| Detail.csv | Canonical line item dataset (24 lines) |
| WBS_CBS_Matrix.csv | WBS to CBS mapping logic |
| Risk_Register.md | Risk identification and contingency rationale (10 risks) |
| QA_Report.md | Quality checks and completeness scoring (Run Status: WARNINGS) |
| Summary.md | Cost breakdown by CBS and scope element |

---

## 14. Recommended Next Steps

### Immediate Actions

1. **Validate reinforcing steel quantity (A-009: $540k):**
   - 180 tonnes is largest single cost driver (25.9% of base)
   - Develop preliminary rebar schedules or use comparable project data

2. **Obtain vendor budgetary quotes:**
   - Ready-mix concrete (2 suppliers minimum)
   - Fabricated rebar supply
   - Formwork system rental
   - Third-party testing services

3. **Coordinate with PKG-02:**
   - Obtain geotechnical parameters for foundation design
   - Confirm foundation type (ring wall vs. mat)

### Medium-Term Improvements

4. **Extract Employer's Requirements:**
   - Concrete specifications from ER Vol 2 Part 2
   - Containment requirements for OBJ-7

5. **Develop project rate tables:**
   - Engineering labor rates
   - Construction labor rates
   - Equipment rental rates

6. **Re-run estimate** with improved inputs to upgrade maturity from Class 5 to Class 4

---

## 15. Approvals and Limitations

**Prepared By:** Estimating Agent (Automated)
**Reviewed By:** Not yet reviewed
**Approved By:** Not yet approved

**Limitations of Use:**

This estimate is provided for **conceptual budgeting and feasibility assessment purposes only**. It is not:
- A binding quote or commitment
- Suitable for contracting or procurement
- A guaranteed maximum price (GMP)
- A basis for detailed project budgeting
- Suitable for financing decisions without further validation

**Expected Accuracy:** -30% / +50% (Class 5 Order of Magnitude)

**Validity Period:** January 2026 pricing basis; subject to escalation over time

---

**Basis of Estimate Prepared By:** Estimating Agent
**Date:** 2026-01-28
**Status:** Complete
**Snapshot:** EST_PKG05_DRAFT_2026-01-28_2400
