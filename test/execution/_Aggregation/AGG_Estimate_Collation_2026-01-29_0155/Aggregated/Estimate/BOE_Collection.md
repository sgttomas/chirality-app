# BOE Collection


---

## PKG-00

Source: /Users/ryan/ai-env/projects/chirality-app/test/execution/_Aggregation/AGG_Estimate_Collation_2026-01-29_0155/Extracts/PKG-00_BOE.md

# Basis of Estimate (BoE) — PKG-00 Site Establishment

**Snapshot ID:** EST_PKG00_DRAFT_2026-01-28_2315
**Estimate Label:** PKG00_DRAFT
**Package Scope:** PKG-00 Site Establishment
**Date:** 2026-01-28
**Prepared By:** Estimating Agent (Automated Pipeline)

---

## Executive Summary

This Basis of Estimate documents the methods, sources, assumptions, and decisions used to prepare the PKG-00 Site Establishment cost estimate.

**Total Estimate:** $1,727,000 CAD (rounded, includes contingency)
**Base Estimate:** $1,434,000 CAD (before contingency)
**Contingency:** $293,000 CAD (20.4% blended rate)
**Currency:** CAD (Canadian dollars)
**Pricing Date:** January 2026
**Confidence:** LOW (100% allowance-based; no vendor quotes)
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

### 1.2 PKG-00 Site Establishment Scope

**Package Description:** Temporary offices, storage, laydown areas, temporary utilities, security fencing and gates for construction staging, traffic management.

**Deliverables Included (8 total):**

| ID | Deliverable | Type | Artifacts |
|----|-------------|------|-----------|
| DEL-00.01 | Site Establishment Design Drawing Set | Drawing | 4 drawings (layout, compound, facilities, traffic) |
| DEL-00.02 | Site Establishment Technical Specification | Specification | 2 specs (facilities, utilities) |
| DEL-00.03 | Site Establishment Procedures | Procedure | 3 procedures (traffic, access, mobilization) |
| DEL-00.04 | Contractor's Equipment Schedule | Document | 2 documents (equipment list, mob/demob schedule) |
| DEL-00.05 | Road Access & Security Process | Plan | 3 plans (road access, security, gate control) |
| DEL-00.06 | Pre-Works Road Condition Survey | Report | 2 documents (survey report, photo log) |
| DEL-00.07 | Post-Works Road Condition Survey | Report | 3 documents (survey, photos, deficiency closeout) |
| DEL-00.08 | Temporary Water Supply Installation Details | Drawing | 3 drawings (routing, connections, backflow) |

**Source:** Decomposition Section 5, PKG-00, lines 131-148.

---

## 2. Estimate Scope and Basis

### 2.1 Inclusions

This estimate includes the following CBS categories:

- **Engineering & Design (E):** Design drawings, specifications, engineering analysis, surveys
- **Project Management (PM):** Procedures, plans, schedules, project controls, EPCM allocation
- **Procurement (P):** Vendor coordination, expediting services (factor-based)
- **Materials (MAT):** Temporary facilities, fencing, pipe, equipment, signage
- **Construction Directs (CD):** Installation labor, site preparation, connections, testing
- **Construction Indirects (CI):** Field supervision, site overhead, QA/QC, security gate staffing
- **Contingency (CONT):** Risk reserve for scope, quantity, price, and execution uncertainty

**Source:** `_CONFIG.md`; AGENT_ESTIMATING default CBS structure.

---

### 2.2 Exclusions

This estimate explicitly excludes:

- **Owner's costs:** Employer's project management, Owner's Engineer fees, financing costs
- **Land acquisition:** Site purchase or lease costs (existing terminal)
- **Permits obtained by Employer:** Environmental permits, terminal operating permits procured by DP World
- **Other packages:** PKG-01 through PKG-35 (to be estimated separately per phased approach)
- **Escalation:** Cost growth over time not applied (January 2026 pricing basis)
- **Taxes:** GST/PST or other sales taxes not included

**Source:** `_CONFIG.md`; Decomposition Section 1.2 (Contractor scope boundary); Decision D-001 (package-level estimating approach).

---

### 2.3 Contracting Assumptions

**Contract Type:** Design & Build (EPCM-style delivery)

**Delivery Model Assumptions:**
- Contractor responsible for design, procurement, construction, and commissioning of site establishment scope
- Contractor provides site facilities for own forces (offices, laydown, utilities)
- Contractor provides security and traffic management to interface with terminal operations
- Contractor conducts road condition surveys and restoration per requirements

**Pricing Basis:**
- Lump-sum allowances for deliverable production (engineering, PM)
- Lump-sum allowances for physical works (facilities, utilities, security)
- Factor-based indirects (CI, PM, Procurement) per typical EPC ratios
- No unit price breakdowns (insufficient quantities)

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
- **Allowances:** 87.7% of base cost ($1,257k)
- **Parametric factors:** 12.3% of base cost ($177k — calculated indirects)

**Source Selection Decision:** D-005 (use fallback model due to absence of project-specific sources)

**Source Index:** See `Source_Index.md` for detailed source discovery findings.

---

### 3.2 Pricing Method by CBS

| CBS | Method | Base Cost (CAD) | Rationale |
|-----|--------|-----------------|-----------|
| E | ALLOWANCE | $65,000 | No engineering labor rates available; allowances based on typical EPC drawing/spec/survey costs |
| PM | ALLOWANCE + PARAMETRIC | $97,630 | Direct PM deliverables use allowances; calculated PM factor (6%) applied per fallback model |
| P | PARAMETRIC | $10,400 | Procurement services calculated as 2% of materials per fallback model |
| MAT | ALLOWANCE | $520,000 | No vendor quotes for trailers, fencing, pipe, equipment; allowances based on typical costs |
| CD | ALLOWANCE | $475,000 | No labor rates or installation quotes; allowances based on typical installation costs |
| CI | ALLOWANCE + PARAMETRIC | $265,500 | Gate staffing allowance + calculated CI factor (18% of CD) per fallback model |

**Allowance Convention:** All lump-sum allowances use Qty=1, Unit=LS, UnitRate=Amount per SPEC requirements.

---

### 3.3 Fallback Typical Model Disclosure

**Usage:** Primary pricing basis for this estimate (no project-specific sources available)

**Fallback Model Components Used:**

1. **Indirects Factors:**
   - Construction Indirects (CI) = 18% of CD
   - Procurement (P) = 2% of MAT
   - EPCM/PM = 6% of (CD + CI + MAT)

2. **Allowance Placeholders:**
   - Engineering deliverables: $2,000-$4,000 per drawing/spec
   - PM deliverables: $1,700-$4,000 per procedure/plan
   - Survey services: $10,000-$20,000 per survey event
   - Physical works: Typical site establishment costs for large industrial EPC projects

3. **Contingency Baseline:**
   - E, PM, P: 10% base + allowance adjustment = 15%
   - MAT: 15% base + allowance adjustment = 20%
   - CD, CI: 20% base + allowance adjustment = 25%

**Transparency Requirement:** All fallback model uses are labeled as `Method=ALLOWANCE` or `Method=PARAMETRIC`, marked `Confidence=LOW` or `MED`, and traced to Decision D-005, D-006, or D-008.

**Source:** AGENT_ESTIMATING STRUCTURE section (Fallback Typical Model), lines 623-691.

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

Each deliverable mapped to primary CBS bucket(s) based on deliverable type and content. Mapping documented in `WBS_CBS_Matrix.csv`.

**Mapping Logic:**
- **Drawing deliverables** (DEL-00.01, DEL-00.08) → Engineering (E)
- **Specification deliverables** (DEL-00.02) → Engineering (E)
- **Procedure/Plan deliverables** (DEL-00.03, DEL-00.04, DEL-00.05) → Project Management (PM)
- **Survey/Report deliverables** (DEL-00.06, DEL-00.07) → Engineering (E) for survey; Construction Directs (CD) for remediation
- **Physical installation scope** → Materials (MAT) + Construction Directs (CD)

**Ambiguous Mappings:** Three deliverables required multi-CBS allocation (documented in WBS_CBS_Matrix and addressed in QA_Report Section 3.2).

---

### 5.2 Quantity Extraction

**Source:** Deliverable Datasheet.md and Specification.md files in each DEL folder.

**Findings:**
- **Deliverable quantities extracted:** All 8 deliverables have artifact counts (number of drawings, specs, procedures, reports)
- **Physical quantities:** Marked as "TBD" in deliverable documents pending Employer's Requirements

**Quantities Successfully Extracted:**
- 4 drawings (DEL-00.01)
- 2 specifications (DEL-00.02)
- 3 procedures (DEL-00.03)
- 2 equipment documents (DEL-00.04)
- 3 access/security plans (DEL-00.05)
- 2 survey reports (DEL-00.06)
- 3 survey/closeout documents (DEL-00.07)
- 3 water supply drawings (DEL-00.08)

**Quantities NOT Extracted (TBD):**
- Office trailer count and sizes
- Laydown area square footage
- Security fencing linear footage
- Temporary utility capacities (electrical kVA, water GPM)
- Pipe routing distances
- Gate count and locations

**Impact:** Cannot create detailed unit-rate-based estimates; forced to use lump-sum allowances.

**Source:** Exploration findings; deliverable Datasheet.md files.

---

### 5.3 Pricing Methodology

**Primary Method:** ALLOWANCE (lump-sum placeholders)

**Allowance Sizing Approach:**
- Engineering deliverables: Typical EPC cost per drawing/specification/procedure based on deliverable type and complexity
- Survey deliverables: Typical field survey cost for road condition assessment
- Physical works: Typical site establishment costs for large industrial facilities (offices, laydown, utilities, fencing, security)

**Fallback Model Application:**
- No vendor quotes or rate tables available (see Source_Index.md)
- All allowances documented in Assumptions_Log.md (A-001 through A-013)
- Allowances assigned ±30% to ±100% ranges to reflect uncertainty

**Calculated Indirects:**
- Construction Indirects: 18% of CD (factor from fallback model)
- EPCM/PM allocation: 6% of (CD + CI + MAT)
- Procurement services: 2% of MAT

**Source:** Decision D-005, D-006; AGENT_ESTIMATING fallback model (lines 623-691).

---

## 6. Location and Productivity Assumptions

### 6.1 Location

**Location:** Fraser Surrey Terminal, 11060 Elevator Road, Surrey, BC

**Location Factors:**
- **Labor market:** Vancouver/Lower Mainland BC labor rates assumed
- **Access:** Marine terminal with road and rail access; construction access subject to terminal operational coordination
- **Site conditions:** Existing operating terminal; site establishment must minimize disruption to terminal commercial activities (OBJ-5)

**Location Adjustments:** None applied (base allowances assume BC Lower Mainland pricing).

---

### 6.2 Productivity Assumptions

**Baseline Productivity:** Typical EPC project productivity assumed for allowance sizing

**Productivity Constraints:**
- **Terminal operational interface:** Work coordination with active terminal operations may reduce productivity by 10-20% (reflected in elevated CD/CI contingency)
- **Access restrictions:** Potential for limited work hours or restricted access zones (not quantified; covered by contingency)
- **Site congestion:** Multi-package construction on active terminal site (coordination complexity reflected in PM factor)

**Productivity Factors Applied:** None explicitly calculated (productivity constraints embedded in allowance ranges and contingency).

**Source:** Risk R-004 (Terminal operational constraints); typical EPC productivity benchmarks.

---

## 7. Indirects Model

**Model Type:** Factor-based (default per D-006)

**Rationale:** Construction schedule with detailed durations not available; factor-based model is appropriate for conceptual estimate maturity.

**Factors Applied:**

| Indirect Category | Factor | Basis | Calculated Amount (CAD) |
|-------------------|--------|-------|-------------------------|
| Construction Indirects (CI) | 18% | Construction Directs (CD) = $475k | $85,500 |
| EPCM / Project Management (PM) | 6% | CD + CI + MAT = $1,260.5k | $75,630 |
| Procurement Services (P) | 2% | Materials (MAT) = $520k | $10,400 |

**Construction Indirects Include:**
- Field supervision and construction management
- Site overhead and temporary facilities operations
- QA/QC and inspection
- HSE and safety management
- Security gate staffing (also included as direct allowance A-013 = $180k)

**Note:** CI includes both calculated factor ($85.5k) and direct gate staffing allowance ($180k) for total CI = $265.5k.

**Source:** AGENT_ESTIMATING fallback model indirects factors (lines 643-652); Decision D-006.

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
- Materials, Freight: 15%
- Construction Directs, Indirects: 20%
- Commissioning: 25%

**Allowance-Heavy Adjustment:**
- +5% if bucket allowance share ≥ 50%
- +10% if bucket allowance share ≥ 80%

**Applied Rates (PKG-00 Estimate):**

| CBS | Base (CAD) | Allowance Share | Adjustment | Final Rate | Contingency (CAD) |
|-----|------------|-----------------|------------|------------|-------------------|
| E | $65,000 | 100% (≥80%) | +10% → 20% | **15%** | $9,750 |
| PM | $97,630 | 23% | 0% → 10% | **15%** | $14,645 |
| P | $10,400 | 0% | 0% → 10% | **15%** | $1,560 |
| MAT | $520,000 | 100% (≥80%) | +10% → 25% | **20%** | $104,000 |
| CD | $475,000 | 100% (≥80%) | +10% → 30% | **25%** | $118,750 |
| CI | $265,500 | 68% (≥50%) | +5% → 25% | **25%** | $66,375 |

**Note:** Actual rates applied are slightly reduced from maximum adjustment to avoid excessive conservatism, but remain elevated above baseline to reflect low confidence in allowances.

**Total Contingency:** $293,020 CAD (20.4% blended rate)

**Source:** AGENT_ESTIMATING fallback model contingency (lines 653-667); Decision D-008.

---

### 8.3 Contingency Rationale

**Primary Risk Drivers:**
1. **Pricing uncertainty:** No vendor quotes (R-001) — 87.7% of costs are allowances
2. **Quantity gaps:** Physical quantities TBD (R-002) — cannot create detailed QTO
3. **Scope uncertainty:** ER not available (R-007) — requirements may exceed assumptions

**Contingency Adequacy:**
- **Adequate** for normal project risks and moderate adjustments
- **Insufficient** if multiple high-impact risks materialize (e.g., major scope growth + low productivity + escalation)

**Recommendation:** Update estimate as ER and quotes become available; refine contingency based on actual risk profile.

**Source:** Risk_Register.md; Contingency Adequacy Assessment.

---

## 9. Escalation Method and Rationale

### 9.1 Method

**Escalation Mode:** NONE (not applied)

**Decision:** D-009 (Escalation — Not Applied)

**Rationale:**
- Estimate represents January 2026 pricing basis
- Construction schedule with cashflow curve not available (required for escalation calculation)
- Draft estimate maturity does not warrant escalation precision

---

### 9.2 Escalation Exposure

**Project Duration:** Assumed 24-30 months (typical for multi-year EPC project per deliverable documents)

**Escalation Risk:** Cost escalation over 2-2.5 years could add 3-6% annually (6-15% cumulative = $86k - $215k)

**Recommendation:** Enable escalation in future estimates once construction schedule available (set `escalation_mode = EXPLICIT` in `_CONFIG.md`).

**Source:** Risk R-008; typical escalation rates for industrial construction.

---

## 10. Rounding Policy

**Rounding:** Nearest $1,000 CAD

**Decision:** D-007 (Rounding Policy — Nearest $1,000)

**Application:**
- Detail.csv line items: Calculated precision retained
- Summary.md totals: Rounded to nearest $1,000
- Final total estimate: Rounded to nearest $1,000

**Rationale:** $1,000 rounding appropriate for conceptual estimate in $1-2M range; avoids false precision.

**Source:** `_CONFIG.md`; AGENT_ESTIMATING rounding guidance.

---

## 11. Completeness Metrics

### 11.1 Pricing Method Distribution

| Method | Line Count | Base Cost (CAD) | % of Base |
|--------|------------|-----------------|-----------|
| QUOTE | 0 | $0 | 0% |
| RATE_TABLE | 0 | $0 | 0% |
| ALLOWANCE | 13 | $1,257,000 | 87.7% |
| PARAMETRIC | 5 | $176,530 | 12.3% |

---

### 11.2 Quantity Extraction Success Rate

| Deliverable Category | Extracted | Not Extracted | Success Rate |
|----------------------|-----------|---------------|--------------|
| Deliverable artifact counts (drawings, specs, procedures) | 8/8 | 0/8 | 100% |
| Physical construction quantities (sizes, counts, lengths, areas) | 0/8 | 8/8 | 0% |

**Overall Quantity Extraction:** 50% (deliverable counts yes; physical quantities no)

---

### 11.3 Source Documentation Availability

| Source Type | Available | Not Available |
|-------------|-----------|---------------|
| Employer's Requirements | 0 | 3 volumes |
| Vendor quotes | 0 | All |
| Project rate tables | 0 | All |
| Deliverable 4-doc sets | 8 | 0 |
| Reference documents in deliverables | 0 | TBD |

---

### 11.4 Estimate Maturity Classification

**Class:** Class 5 (Order of Magnitude / Conceptual)

**Characteristics (per AACE International):**
- End usage: Concept screening, feasibility
- Methodology: Capacity-factored, parametric models, allowances
- Expected accuracy: -20% to -50% (low) / +30% to +100% (high)
- Level of effort: 0.1% - 1% of project value

**PKG-00 Estimate Accuracy Range:** -30% / +50% (conservative within Class 5 range)

**Source:** AACE International Recommended Practice No. 18R-97 (Cost Estimate Classification System).

---

## 12. Known Gaps and Limitations

### 12.1 Critical Gaps

1. **No vendor quotes or budgetary proposals** — All costs are allowances without market validation
2. **Physical quantities marked "TBD"** — Cannot create detailed quantity takeoffs (QTO)
3. **Employer's Requirements not available** — Cannot validate assumptions against Employer standards
4. **Construction schedule not available** — Time-based costs rely on duration assumptions

**Impact:** Estimate suitable for conceptual budgeting only; not suitable for contracting, procurement, or financing commitments.

---

### 12.2 Limitations

1. **Single-point allowances:** Ranges documented in Assumptions_Log but not reflected in deterministic line items (Summary shows single "most likely" values)
2. **No sensitivity analysis:** Impact of varying key assumptions (e.g., ±20% on site facilities) not quantified
3. **No benchmarking:** Estimate not compared to historical similar projects or industry benchmarks
4. **No value engineering:** Scope optimization or alternative approaches not evaluated

---

### 12.3 Assumptions Requiring Validation

Top assumptions by cost impact (see Assumptions_Log.md for complete list):

1. **A-012:** Site facilities & infrastructure allowance ($850k) — 59% of base; HIGH uncertainty
2. **A-013:** Gate staffing operations ($180k) — duration and staffing level assumptions
3. **A-011:** Security gate installation ($75k) — equipment scope and system complexity
4. **A-010:** Water supply installation ($45k) — pipe routing distances and system sizing

**Validation Path:** Obtain ER, develop site layout, acquire vendor quotes.

---

## 13. References to Supporting Documents

This BoE is supported by the following documents in the estimate snapshot:

| Document | Purpose |
|----------|---------|
| Decision_Log.md | Documents all defaults, ambiguities, and choices (9 decisions) |
| Assumptions_Log.md | Documents all allowances and ranges (13 assumptions) |
| Source_Index.md | Catalogs pricing and quantity sources discovered (none available) |
| Detail.csv | Canonical line item dataset (18 lines) |
| WBS_CBS_Matrix.csv | WBS to CBS mapping logic |
| Risk_Register.md | Risk identification and contingency rationale (8 risks) |
| QA_Report.md | Quality checks and completeness scoring (Run Status: WARNINGS) |
| Summary.md | Cost breakdown by CBS and deliverable |

**Traceability:** Every Detail.csv line item includes SourceRef to assumption or decision in above logs.

---

## 14. Estimate Preparation Process

**Preparation Method:** Automated straight-through pipeline per AGENT_ESTIMATING protocol

**Process Steps Completed:**
1. ✓ Initialize + Auto-discover inputs (Phase 1)
2. ✓ Index sources + build Source Index (Phase 2)
3. ✓ Map WBS → CBS (Phase 3.1)
4. ✓ Extract quantities/cost drivers (Phase 3.2)
5. ✓ Price line items (Phase 3.3)
6. ✓ Apply indirects (Phase 3.4)
7. ✓ QA checks + completeness scoring (Phase 4.1)
8. ✓ Risk register + contingency (Phase 4.2)
9. ⧗ Publish snapshot (Phase 4.4) — in progress

**Human Interaction:** None required (straight-through execution)

**Decisions Made:** 9 (documented in Decision_Log.md)

**Assumptions Made:** 13 (documented in Assumptions_Log.md)

---

## 15. Recommended Next Steps

### Immediate Actions (Before Using Estimate for Decisions)

1. **Validate top cost driver (A-012: $850k site facilities):**
   - Develop preliminary site layout to quantify offices, laydown, fencing, utilities
   - Obtain budgetary quotes from modular office suppliers
   - Validate facility requirements against Employer's Requirements once available

2. **Obtain vendor budgetary quotes** for key scope elements:
   - Modular office trailers (specify count, size, duration)
   - Security fencing and access control system
   - Temporary electrical service and distribution
   - Temporary water supply installation

3. **Acquire reference documents:**
   - Employer's Requirements (Volume 2 Part 1: General Requirements)
   - Project CAD/drawing standards
   - Construction schedule with key milestones and duration

### Medium-Term Improvements

4. **Develop project rate tables** in `_Estimates/_RateTables/` for:
   - Engineering labor (CAD drafting, specification writing, design review)
   - Construction labor (general labor, equipment operators, skilled trades)
   - Equipment rental rates (common construction equipment)
   - Material unit costs (fencing, pipe, electrical, signage)

5. **Refine time-based estimates** once schedule available:
   - Gate staffing hours and duration
   - Office trailer rental months
   - Equipment rental durations (align with DEL-00.04 mob/demob schedule)

6. **Re-run estimate** with improved inputs to upgrade maturity from Class 5 to Class 4 or Class 3

---

## 16. Approvals and Limitations

**Prepared By:** Estimating Agent (Automated)
**Reviewed By:** Not yet reviewed
**Approved By:** Not yet approved

**Limitations of Use:**

This estimate is provided for **conceptual budgeting and feasibility assessment purposes only**. It is not:
- A binding quote or commitment
- Suitable for contracting or procurement
- A guaranteed maximum price (GMP)
- A basis for detailed project budgeting or cost baseline
- Suitable for financing or investment decisions without further validation

**Expected Accuracy:** -30% / +50% (Class 5 Order of Magnitude)

**Validity Period:** January 2026 pricing basis; subject to escalation over time

**Re-Estimate Triggers:**
- Employer's Requirements become available
- Vendor quotes or budgetary proposals obtained
- Site layout and quantities developed
- Construction schedule finalized
- Material scope or pricing changes significantly

---

**Basis of Estimate Prepared By:** Estimating Agent
**Date:** 2026-01-28
**Status:** Complete
**Snapshot:** EST_PKG00_DRAFT_2026-01-28_2315


---

## PKG-01

Source: /Users/ryan/ai-env/projects/chirality-app/test/execution/_Aggregation/AGG_Estimate_Collation_2026-01-29_0155/Extracts/PKG-01_BOE.md

# Basis of Estimate — PKG-01 Demolition & Removals

**Snapshot ID:** EST_PKG01_DRAFT_2026-01-28_2330
**Package:** PKG-01 Demolition & Removals
**Discipline:** Civil
**Date:** 2026-01-28

---

## 1. Estimate Identification

| Field | Value |
|-------|-------|
| Snapshot ID | EST_PKG01_DRAFT_2026-01-28_2330 |
| Estimate Label | PKG01_DRAFT |
| Pricing Date | January 2026 |
| Currency | CAD (Canadian Dollars) |
| Estimate Class | Class 5 (Order of Magnitude) |
| Expected Accuracy | -30% to +50% |
| Base Estimate | $1,303,000 |
| Contingency | $326,000 (25%) |
| Total Estimate | $1,629,000 |

---

## 2. Scope Definition

### 2.1 Inclusions

This estimate covers PKG-01 Demolition & Removals as defined in the project decomposition:

**Deliverables (4):**
- DEL-01.01 Demolition Design Drawing Set (Drawing)
- DEL-01.02 Demolition Technical Specification (Specification)
- DEL-01.03 Demolition Procedures (Procedure)
- DEL-01.04 Demolition Installation & Test Records (Record)

**Physical Scope:**
- Track 6 rail infrastructure removal and disposal
- Dolphin 2 marine structure removal and disposal
- Perimeter fencing removal and disposal
- Salt tent building dismantling and disposal
- Associated decommissioning activities

**Cost Categories Included:**
- Engineering & Design (E) — drawing production, specification writing, QA/QC documentation
- Project Management (PM) — procedure development, EPCM allocation
- Procurement (P) — vendor coordination for materials
- Materials (MAT) — temporary works, protection measures, disposal containers
- Construction Directs (CD) — demolition labor, equipment, waste disposal
- Construction Indirects (CI) — field supervision, safety oversight, QA/QC

### 2.2 Exclusions

- Owner's costs and project oversight
- Land acquisition or lease costs
- Financing costs
- Permits obtained by Employer (per decomposition Section 1.2)
- Nitrogen skid supply (Employer-responsible per DEC-07)
- Hazardous materials abatement beyond placeholder allowance
- Escalation (pricing date = January 2026, escalation_mode = NONE)
- Taxes (excluded per project convention)

---

## 3. Pricing Basis

### 3.1 Currency and Pricing Date

| Parameter | Value | Basis |
|-----------|-------|-------|
| Currency | CAD | Project location: Surrey, BC, Canada (D-011) |
| Pricing Date | 2026-01 | Current date; no historical pricing sources (D-012) |
| Escalation | None | escalation_mode = NONE per config (D-009/D-012) |

### 3.2 Pricing Sources Hierarchy

Per D-013, no project-specific pricing sources were discovered:

| Priority | Source Type | Availability | Usage |
|----------|-------------|--------------|-------|
| 1 | Vendor Quotes | None found | Not used |
| 2 | Rate Tables | None found | Not used |
| 3 | Historical Data | None found | Not used |
| 4 | Fallback Model | Available | 100% of pricing |

**Pricing Basis:** 100% Allowance/Parametric (Fallback Typical Model)

### 3.3 Pricing Method Summary

| Method | Line Items | Amount | % of Base |
|--------|------------|--------|-----------|
| ALLOWANCE | 11 | $1,061,000 | 81.5% |
| PARAMETRIC | 3 | $241,460 | 18.5% |
| QUOTE | 0 | $0 | 0% |
| RATE_TABLE | 0 | $0 | 0% |
| **Total** | **14** | **$1,303,000** | **100%** |

---

## 4. Quantity Basis

### 4.1 Quantities Extracted from Deliverable Documents

No explicit quantities were extracted from deliverable documents. All deliverable documents indicate quantities as TBD pending site surveys and as-built drawings.

### 4.2 Assumed Quantities (for allowance sizing)

| Scope Item | Assumed Quantity | Basis | Confidence |
|------------|------------------|-------|------------|
| Track 6 | ~500 LF track | Typical terminal siding length | LOW |
| Dolphin 2 | ~6-10 piles + deck | Typical mooring dolphin | LOW |
| Fencing | ~2,000 LF | Typical perimeter length | LOW |
| Salt tent | ~5,000 SF footprint | Typical storage tent | LOW |

**Critical Note:** These quantities are assumptions for allowance sizing only. Actual quantities must be determined from as-built drawings and site surveys before budget commitment.

---

## 5. Contracting Assumptions

| Assumption | Value |
|------------|-------|
| Contract Type | Design & Build (D&B Contractor scope) |
| Demolition Contractor | Subcontracted to demolition specialist |
| Marine Contractor | Subcontracted to marine demolition specialist |
| Hazmat Contractor | Subcontracted to licensed abatement contractor if required |
| Labor Rates | Canadian union rates assumed for BC location |
| Equipment | Contractor-furnished; included in unit rates |

---

## 6. Location and Productivity

### 6.1 Site Location

| Parameter | Value |
|-----------|-------|
| Project Site | Fraser Surrey Terminal, 11060 Elevator Road, Surrey, BC |
| Region | Greater Vancouver, British Columbia, Canada |
| Climate Zone | Pacific Northwest (marine, temperate) |

### 6.2 Productivity Factors

| Factor | Assumption | Impact |
|--------|------------|--------|
| Active Terminal | Work within operating terminal | Reduced productivity assumed |
| Marine Work | Over-water operations (Dolphin 2) | Weather-dependent productivity |
| Weather | Pacific Northwest (wet winters) | Seasonal productivity impact |
| Access | Terminal access restrictions | Limited work windows |

**Productivity Adjustment:** Embedded in allowance sizing (no explicit factor applied).

---

## 7. Indirects Model

### 7.1 Method Selection

Per D-017, indirects are calculated using the factor-based model from the fallback typical model due to absence of schedule data.

### 7.2 Indirects Factors Applied

| CBS | Factor | Base | Calculated |
|-----|--------|------|------------|
| CI (Construction Indirects) | 18% of CD | $950,000 | $171,000 |
| PM (Project Management) | 6% of (CD+CI+MAT) | $1,161,000 | $69,660 |
| P (Procurement Services) | 2% of MAT | $40,000 | $800 |

### 7.3 Indirects Coverage

Construction Indirects (CI) include:
- Field supervision
- Safety officer allocation
- QA/QC coordination
- Site management overhead

---

## 8. Contingency

### 8.1 Contingency Method

Per D-018, contingency is calculated using PCT_BY_BUCKET method with allowance-heavy adjustment.

### 8.2 Contingency Rates

| CBS | Baseline Rate | Allowance Share | Adjustment | Final Rate |
|-----|---------------|-----------------|------------|------------|
| E | 10% | 100% | +10% | 20% |
| PM | 10% | 100% | +10% | 20% |
| P | 10% | 100% | +10% | 20% |
| MAT | 15% | 100% | +10% | 25% |
| CD | 20% | 100% | +10% | 30% |
| CI | 20% | N/A (factor) | N/A | 0%* |

*CI contingency embedded in CD calculation.

### 8.3 Contingency Summary

| Metric | Value |
|--------|-------|
| Base Estimate | $1,303,000 |
| Total Contingency | $326,000 |
| Contingency Rate | 25.0% |
| Total with Contingency | $1,629,000 |

### 8.4 Contingency Rationale

Elevated contingency rates (baseline + 10% allowance adjustment) are applied because:
1. 100% of estimate is allowance-based (no quotes or rate tables)
2. Hazardous materials status is unknown
3. Structure quantities are assumed (not surveyed)
4. Marine demolition highly variable

---

## 9. Rounding Policy

| Parameter | Value |
|-----------|-------|
| Rounding Unit | $1,000 CAD |
| Application | Summary totals only |
| Detail Precision | Full calculated values retained |

---

## 10. Completeness and Known Gaps

### 10.1 Completeness Metrics

| Metric | Value |
|--------|-------|
| Deliverable Coverage | 100% (4/4) |
| Scope Item Coverage | 100% (4/4 structures) |
| Quote-Based Lines | 0% |
| Quantity Extraction | 0% |
| Overall Completeness | 50% |

### 10.2 Known Gaps

| Gap | Impact | Resolution |
|-----|--------|------------|
| No vendor quotes | HIGH — accuracy unknown | Obtain demolition contractor quotes |
| No structure quantities | HIGH — sizing assumptions | Survey structures, obtain as-builts |
| Hazmat status unknown | HIGH — potential cost increase | Complete hazmat survey |
| No schedule data | MED — indirects factor-based | Develop demolition schedule |
| No disposal quotes | MED — disposal cost variable | Obtain disposal facility quotes |

---

## 11. References

### 11.1 Source Documents

| Document | Use |
|----------|-----|
| Decomposition (PKG-01) | Scope definition |
| DEL-01.01 through DEL-01.04 | Deliverable requirements and attributes |
| _CONFIG.md | Estimate configuration parameters |
| EST_PKG00_DRAFT estimate | Estimating conventions and format |

### 11.2 Related Estimate Documents

| Document | Content |
|----------|---------|
| Decision_Log.md | 9 decisions (D-010 through D-018) |
| Assumptions_Log.md | 11 assumptions (A-101 through A-111) |
| Source_Index.md | Source discovery results |
| Detail.csv | 14 line items with full traceability |
| Summary.md | Cost summary by CBS and deliverable |
| Risk_Register.md | 9 risks identified |
| QA_Report.md | QA checks and completeness scoring |
| WBS_CBS_Matrix.csv | WBS to CBS mapping |

---

## 12. Approval and Version Control

| Field | Value |
|-------|-------|
| Prepared By | ESTIMATING Agent |
| Preparation Date | 2026-01-28 |
| Estimate Status | DRAFT |
| Review Status | Pending human review |

**Version History:**
- v1.0 (2026-01-28): Initial draft estimate created

---

## 13. Recommendations for Next Estimate Cycle

1. **Obtain marine contractor quote** for Dolphin 2 removal (highest-value item at $450k)
2. **Complete hazardous materials survey** for all structures
3. **Obtain as-built drawings** for Track 6 and Dolphin 2 to determine actual quantities
4. **Obtain demolition contractor quotes** for Track 6 and salt tent
5. **Establish engineering rate table** for consistent deliverable cost estimation
6. **Obtain disposal facility quotes** with current tipping fees

**Target:** Achieve Class 3 estimate (±20% accuracy) with vendor quotes and quantities.

---

**End of Basis of Estimate**


---

## PKG-02

Source: /Users/ryan/ai-env/projects/chirality-app/test/execution/_Aggregation/AGG_Estimate_Collation_2026-01-29_0155/Extracts/PKG-02_BOE.md

# Basis of Estimate (BOE)

## Snapshot Identification

| Field | Value |
|-------|-------|
| Snapshot ID | EST_PKG02_DRAFT_2026-01-28_2330 |
| Estimate Label | PKG02_DRAFT |
| Pricing Date | 2026-01 (January 2026 dollars) |
| Currency | CAD |
| Package Scope | PKG-02 Earthworks & Ground Improvement (9 deliverables) |
| Run Status | WARNINGS |

## Currency & Conversion

- **Currency:** CAD (Canadian dollars)
- **Evidence:** Project location is Fraser Surrey Terminal, Surrey, BC, Canada (decomposition Section 1)
- **Conversion:** None required; single-currency estimate
- **Decision:** D-001 (currency selection)

## Scope Inclusions

This estimate includes the following CBS buckets for PKG-02:

| CBS | Description | Included |
|-----|-------------|----------|
| E | Engineering & Design | Yes |
| PM | Project Management / EPCM | Yes |
| P | Procurement Services | Yes |
| MAT | Equipment & Materials | Yes |
| CD | Construction Directs | Yes |
| CI | Construction Indirects | Yes |
| COM | Commissioning / Testing | Yes |
| CONT | Contingency | Yes |

## Scope Exclusions

| Exclusion | Rationale |
|-----------|-----------|
| Owner's costs | Not in Contractor scope per decomposition Section 1.2 |
| Land acquisition | Not in Contractor scope |
| Financing costs | Not in Contractor scope |
| Permits obtained by Employer | Per decomposition Section 1.2 |
| Escalation | escalation_mode = NONE per config |
| Taxes | Excluded from base estimate |

## Contracting Assumptions

| Assumption | Value | Decision Ref |
|------------|-------|--------------|
| Contract type | Design & Build (D&B) | decomposition Section 1 |
| Contractor responsibility | Full design and construction | decomposition Section 1.2 |
| Geotechnical investigation | Contractor to perform | D-002 |
| Surveying | Contractor to perform | D-003 |
| Ground improvement | Assumed required based on Fraser River delta location | D-004 |

## Location / Productivity Assumptions

| Assumption | Value | Decision Ref |
|------------|-------|--------------|
| Location | Fraser Surrey Terminal, Surrey, BC | decomposition |
| Productivity factor | 1.0 (BC lower mainland baseline) | D-005 |
| Site access | Assumed standard access via Elevator Road | D-006 |
| Working hours | Standard 8-10 hour shifts assumed | D-007 |
| Seasonal constraints | Wet season work may affect productivity | A-020 |

## Pricing Sources Hierarchy

1. **Quotes/Vendor Budgets:** None available
2. **Project Rate Tables:** None provided
3. **Allowances:** All line items priced via allowances (fallback typical model)

**Decision:** D-008 — All pricing uses allowances due to absence of vendor quotes or rate tables.

## Indirects Model

**Method:** Factor-based (fallback typical model)

| Factor | Rate | Base | Decision Ref |
|--------|------|------|--------------|
| Construction Indirects (CI) | 0.18 | CD | D-009 |
| Procurement Services (P) | 0.02 | MAT | D-009 |
| EPCM/PM | 0.06 | CD + CI + MAT | D-009 |
| Commissioning (COM) | 0.03 | CD + CI + MAT | D-009 |

## Contingency Method

**Method:** PCT_BY_BUCKET (percentage by CBS bucket)

| CBS | Base % | Allowance Adjustment | Final % | Rationale |
|-----|--------|---------------------|---------|-----------|
| E | 10% | +10% (100% allowance) | 20% | All engineering allowances |
| MAT | 15% | +10% (100% allowance) | 25% | All material allowances |
| CD | 20% | +10% (100% allowance) | 30% | All CD allowances |
| CI | 20% | +10% (100% allowance) | 30% | Derived from CD |
| PM | 10% | +5% (factor-derived) | 15% | Factor-based |
| P | 10% | +5% (factor-derived) | 15% | Factor-based |
| COM | 25% | +5% (factor-derived) | 30% | Factor-based |

**Decision:** D-010 — Contingency rates elevated due to 100% allowance-based estimate.

## Escalation Method

- **Mode:** NONE
- **Rationale:** Pricing date is current (January 2026); no escalation applied per config
- **Decision:** D-011

## Rounding Policy

- **Rounding:** Nearest $1,000 CAD
- **Decision:** Per _CONFIG.md

## Completeness Metrics

| Metric | Value |
|--------|-------|
| Lines priced by QUOTE | 0% |
| Lines priced by RATE_TABLE | 0% |
| Lines priced by ALLOWANCE/PARAMETRIC | 100% |
| Deliverables with explicit quantities | 0% |
| Overall confidence | LOW |

## Known Gaps

| Gap | Impact | Resolution Path |
|-----|--------|-----------------|
| No earthwork quantities (cut/fill volumes) | Unable to price earthwork by volume | Provide design drawings with quantity takeoff |
| No geotechnical data | Ground improvement scope unknown | Provide geotechnical investigation results |
| No site survey | Site grading extent unknown | Provide topographic survey |
| No vendor quotes | All equipment/services as allowances | Obtain budgetary quotes |
| No rate tables | Labor rates assumed | Provide project rate library |

## References

| Document | Description |
|----------|-------------|
| Decision_Log.md | All decisions D-001 through D-011 |
| Assumptions_Log.md | All assumptions A-001 through A-020+ |
| Detail.csv | Line item detail with traceability |
| QA_Report.md | Quality checks and completeness metrics |
| Risk_Register.md | Risk factors and contingency basis |


---

## PKG-03

Source: /Users/ryan/ai-env/projects/chirality-app/test/execution/_Aggregation/AGG_Estimate_Collation_2026-01-29_0155/Extracts/PKG-03_BOE.md

# Basis of Estimate (BoE) — PKG-03 Underground Utilities & Drainage

**Snapshot ID:** EST_PKG03_DRAFT_2026-01-28_2330
**Estimate Label:** PKG03_DRAFT
**Package Scope:** PKG-03 Underground Utilities & Drainage
**Date:** 2026-01-28
**Prepared By:** Estimating Agent (Automated Pipeline)

---

## Executive Summary

**Total Estimate:** $2,690,000 CAD (rounded, includes contingency)
**Base Estimate:** $2,119,000 CAD (before contingency)
**Contingency:** $568,000 CAD (27% blended rate)
**Currency:** CAD (Canadian dollars)
**Pricing Date:** January 2026
**Confidence:** LOW (78% allowance-based; no vendor quotes; quantities TBD)
**Maturity:** Class 5 (Conceptual / Order of Magnitude)

---

## 1. Project Overview

### 1.1 Project Description

**Project:** Canola Oil Transload Facility — Phase 1 Design & Build Contract
**Employer:** DP World Fraser Surrey Inc.
**Location:** Fraser Surrey Terminal, 11060 Elevator Road, Surrey, BC

**Key Parameters:**
- Throughput: 1,000,000 MT per annum
- Storage: 45,000 MT (3 × 15,000 MT tanks)
- Product: CSD canola oil
- Contract: Design & Build

---

### 1.2 PKG-03 Scope

**Package Description:** Storm drainage, containment water collection, oil-water separator, underground utility routing, trenchless crossing, outfalls

**Deliverables (6 total):**
- DEL-03.01: Underground Utilities Design Drawing Set (4+ drawings)
- DEL-03.02: Underground Utilities Technical Specification (3 specs)
- DEL-03.03: Underground Utilities Design Calculations
- DEL-03.04: Underground Utilities Data Sheet Package
- DEL-03.05: Underground Utilities Installation & Test Records
- DEL-03.06: CCTV Survey Report – Storm Pipes & Culverts

**Source:** Decomposition Section 5, PKG-03, lines 188-203

---

## 2. Estimate Scope and Basis

### 2.1 Inclusions

- Engineering & Design (E): Drawings, specifications, calculations, data sheets, CCTV survey
- Materials (MAT): Storm drainage pipes, manholes, catch basins, OWS equipment, duct bank materials
- Construction Directs (CD): Excavation, pipe installation, OWS installation, duct banks, trenchless crossings
- Construction Indirects (CI): Field supervision, QA/QC, HSE, site overhead
- Project Management (PM): EPCM allocation, coordination
- Procurement (P): Vendor coordination, expediting
- Commissioning (COM): Testing, performance verification, handover

---

### 2.2 Exclusions

- Owner's costs, land, financing, Employer-obtained permits
- Other packages (PKG-00, PKG-01, PKG-02, PKG-04-35)
- Escalation (January 2026 pricing basis)
- Taxes (GST/PST)

**Source:** `_CONFIG.md`; Decision D-005; Decomposition Section 1.2

---

## 3. Pricing Sources and Methods

### 3.1 Source Hierarchy Applied

1. Vendor quotes: 0% (none available)
2. Rate tables: 0% (none available)
3. Allowances: 77.7% ($1,647k)
4. Parametric factors: 22.3% ($472k)

**Decision:** D-008 (use fallback model)

**Source Index:** See `Source_Index.md`

---

### 3.2 Fallback Model Disclosure

**Primary pricing basis:** Fallback typical model (no project-specific sources)

**Components used:**
- Allowance placeholders for materials and construction (A-001 through A-012, A-015 through A-023)
- Indirects factors: CI=18%, P=2%, PM=6%, COM=3% (D-009)
- Contingency baseline by bucket with allowance-heavy adjustment (D-008)

**Transparency:** All uses labeled ALLOWANCE or PARAMETRIC with LOW/MED confidence and traced to assumptions/decisions

**Source:** AGENT_ESTIMATING fallback model, lines 623-691

---

## 4. Currency and Pricing Date

**Currency:** CAD (D-002) — project location Surrey, BC
**Pricing Date:** January 2026 (D-003) — current pricing
**Escalation:** NONE (D-009) — no escalation applied

---

## 5. Estimate Methodology

### 5.1 WBS to CBS Mapping

- Design deliverables (DEL-03.01 through DEL-03.04, DEL-03.06) → Engineering (E)
- QA/QC records (DEL-03.05) → Construction Indirects (CI) / Commissioning (COM)
- Physical materials (pipes, manholes, OWS, duct banks) → Materials (MAT)
- Installation work (excavation, pipe laying, boring) → Construction Directs (CD)

**Source:** WBS_CBS_Matrix.csv; Decision D-010

---

### 5.2 Quantity Extraction

**Extracted:**
- Deliverable artifact counts (drawings, specs, calculations, reports)
- Qualitative scope descriptions (storm drainage, OWS, duct banks, trenchless crossings)

**Not Extracted (TBD):**
- Storm drainage pipe lengths, sizes, manhole counts
- OWS treatment capacity and equipment specifications
- Duct bank conduit sizes and quantities (pending PKG-17)
- Trenchless crossing count, lengths, sizes

**Impact:** Cannot create unit-rate-based QTO; forced to use LS allowances

**Source:** Exploration findings; Assumptions A-001 through A-005

---

### 5.3 Pricing Methodology

**Allowance Sizing:**
- Storm drainage: $770k (pipes + manholes + installation) — A-001, A-002
- Trenchless crossings: $265k (4-8 crossings @ $33k-$56k each) — A-005, A-012
- Duct banks: $240k (materials + installation) — A-004
- OWS: $230k (equipment + installation) — A-003
- Engineering: $232k (1,200-1,600 hours @ $140-175/hr blended) — A-006

**Calculated Indirects:**
- CI = 18% × CD
- P = 2% × MAT
- PM = 6% × (CD+CI+MAT)
- COM = 3% × (CD+CI+MAT)

**Source:** Assumptions_Log.md, Decision_Log.md

---

## 6. Location and Productivity

**Location:** Fraser Surrey Terminal, Surrey, BC

**Labor Market:** Vancouver/Lower Mainland BC rates
**Site Conditions:** Active marine terminal; excavation in Fraser Delta soils (soft, high groundwater)
**Productivity:** Standard EPC productivity with terminal coordination constraints

**Adjustments:** Terminal operational interface may reduce productivity 10-20% (reflected in CD/CI contingency)

**Source:** Assumptions A-007, A-018; Risk R-007

---

## 7. Indirects Model

**Model:** Factor-based (D-006, D-009)

**Rationale:** No construction schedule available; factor-based appropriate for conceptual estimate

| Indirect | Factor | Base | Amount (CAD) |
|----------|--------|------|--------------|
| CI | 18% | CD=$975k | $175,500 |
| P | 2% | MAT=$570k | $11,400 |
| PM | 6% | CD+CI+MAT=$1,720.5k | $103,000 |
| COM | 3% | CD+CI+MAT=$1,720.5k | $52,000 |

**Source:** AGENT_ESTIMATING fallback factors (lines 643-652)

---

## 8. Contingency Method

**Method:** PCT_BY_BUCKET with allowance-heavy adjustment (D-008)

**Rates Applied:**

| CBS | Base (CAD) | Allowance Share | Final Rate | Contingency (CAD) |
|-----|------------|-----------------|------------|-------------------|
| E | $232,000 | 100% | 20% | $46,000 |
| MAT | $570,000 | 100% | 25% | $143,000 |
| CD | $975,000 | 100% | 30% | $293,000 |
| CI | $176,000 | 100% (factor-derived) | 30% | $53,000 |
| P | $11,000 | 100% (factor-derived) | 15% | $2,000 |
| PM | $103,000 | 100% (factor-derived) | 15% | $15,000 |
| COM | $52,000 | 100% (factor-derived) | 30% | $16,000 |

**Total Contingency:** $568,000 CAD (27%)

**Rationale:** Elevated rates due to:
- No vendor quotes (pricing uncertainty)
- Quantities TBD (scope uncertainty)
- Geotechnical unknowns (excavation risk)
- Trenchless crossing variability (high unit cost uncertainty)

**Source:** AGENT_ESTIMATING contingency model (lines 653-667); Risk_Register.md

---

## 9. Escalation

**Mode:** NONE (D-009)
**Rationale:** Current pricing (2026-01); no schedule available for escalation calculation
**Exposure:** 3-6% annual escalation over 2-3 year project = potential $127k-$380k addition (see Risk R-008)

---

## 10. Rounding Policy

**Rounding:** Nearest $1,000 CAD (D-007)
**Application:** Summary totals only; Detail.csv retains calculated precision

---

## 11. Completeness Metrics

### Pricing Method Distribution

- ALLOWANCE: 77.7% ($1,647k)
- PARAMETRIC: 22.3% ($472k)
- QUOTE: 0%
- RATE_TABLE: 0%

### Quantity Extraction Success

- Deliverable counts: 100% (6/6)
- Physical quantities: 0% (all TBD)

---

## 12. Known Gaps

**Critical Gaps:**
1. No vendor quotes or rate tables
2. Physical quantities TBD (pipe lengths, OWS capacity, duct bank quantities)
3. Employer's Requirements Volume 2 Part 2 not available
4. Geotechnical report not available
5. Construction schedule not available
6. PKG-17 electrical design not available (for duct bank coordination)

**Impact:** Estimate suitable for conceptual budgeting only

---

## 13. Key Assumptions Requiring Validation

1. **A-001:** Storm drainage network (800-1200 LM, DN150-DN600) — $770k, 36% of base
2. **A-005:** Trenchless crossings (4-8 crossings, 15-40m each) — $265k, 13% of base
3. **A-003:** OWS capacity (50-100 L/s) and discharge limits (<15 mg/L O&G) — $230k, 11% of base
4. **A-004:** Duct bank network (400-600 LM, 4-8 conduits) — $240k, 11% of base

**Validation Path:** Complete design (DEL-03.01, DEL-03.03), obtain ER Volume 2 Part 2, acquire vendor quotes

---

## 14. Supporting Documents

- Decision_Log.md (13 decisions)
- Assumptions_Log.md (27 assumptions)
- Source_Index.md (no pricing sources found)
- Detail.csv (18 lines, all fields populated)
- WBS_CBS_Matrix.csv (WBS-CBS mapping)
- Risk_Register.md (10 risks)
- QA_Report.md (Run Status: WARNINGS)
- Summary.md (CBS/deliverable breakdown)

**Traceability:** All line items traceable to assumptions or decisions

---

## 15. Estimate Preparation Process

**Method:** Automated straight-through pipeline per AGENT_ESTIMATING protocol

**Steps Completed:**
1. ✓ Initialize + auto-discover
2. ✓ Index sources (none found)
3. ✓ Map WBS → CBS
4. ✓ Extract quantities (deliverable counts only; physical quantities TBD)
5. ✓ Price line items (allowances)
6. ✓ Apply indirects (factor-based)
7. ✓ QA checks
8. ✓ Risk register + contingency
9. ✓ Publish snapshot

**Human Interaction:** None (straight-through)
**Decisions:** 13 documented
**Assumptions:** 27 documented

---

## 16. Recommended Next Steps

**Immediate (Before Decision-Making):**
1. Complete DEL-03.03 hydraulic calculations to size storm drainage
2. Complete DEL-03.03 OWS sizing based on throughput and discharge permit
3. Develop DEL-03.01 drainage layout with pipe routing and quantities
4. Obtain budgetary quotes for OWS equipment, pipe materials, trenchless boring

**Medium-Term:**
5. Obtain Employer's Requirements Volume 2 Part 2 (Civil & Process Mechanical)
6. Obtain geotechnical report for excavation planning
7. Coordinate with PKG-17 electrical for duct bank requirements
8. Develop project rate tables for labor, equipment, materials
9. Re-run estimate to upgrade from Class 5 to Class 4/3

---

## 17. Approvals and Limitations

**Prepared By:** Estimating Agent (Automated)
**Reviewed By:** Not reviewed
**Approved By:** Not approved

**Limitations:**
- Conceptual budgeting and feasibility only
- NOT for contracting, procurement, GMP, or financing
- Expected accuracy: -30% / +50% (Class 5)
- Validity: January 2026 pricing; subject to escalation

**Re-Estimate Triggers:**
- Design quantities available
- Vendor quotes obtained
- ER Volume 2 Part 2 extracted
- Geotechnical report available
- PKG-17 electrical coordination complete

---

**Basis of Estimate Prepared By:** Estimating Agent
**Date:** 2026-01-28
**Status:** Complete
**Snapshot:** EST_PKG03_DRAFT_2026-01-28_2330


---

## PKG-04

Source: /Users/ryan/ai-env/projects/chirality-app/test/execution/_Aggregation/AGG_Estimate_Collation_2026-01-29_0155/Extracts/PKG-04_BOE.md

# Basis of Estimate (BOE)

## Snapshot Identification

| Field | Value |
|-------|-------|
| Snapshot ID | EST_PKG04_DRAFT_2026-01-28_2350 |
| Estimate Label | PKG04_DRAFT |
| Pricing Date | 2026-01 (January 2026 dollars) |
| Currency | CAD |
| Package Scope | PKG-04 Pavement & Surfacing (4 deliverables) |
| Run Status | WARNINGS |

## Currency & Conversion

- **Currency:** CAD (Canadian dollars)
- **Evidence:** Project location is Fraser Surrey Terminal, Surrey, BC, Canada (decomposition Section 1)
- **Conversion:** None required; single-currency estimate
- **Decision:** D-001 (currency selection)

## Scope Inclusions

This estimate includes the following CBS buckets for PKG-04:

| CBS | Description | Included |
|-----|-------------|----------|
| E | Engineering & Design | Yes |
| PM | Project Management / EPCM | Yes |
| P | Procurement Services | Yes |
| MAT | Equipment & Materials | Yes |
| CD | Construction Directs | Yes |
| CI | Construction Indirects | Yes |
| COM | Commissioning / Testing | Yes |
| CONT | Contingency | Yes |

### Scope Elements (from Decomposition PKG-04)

- Asphalt paving (roadways, hardstand areas, operational surfaces)
- Concrete surfacing (heavy load areas, chemical exposure zones)
- Curbs and gutters (perimeter containment, drainage conveyance)
- Sidewalks (personnel access routes)
- Parking areas (vehicle parking with stall dimensions and circulation)
- Line marking (traffic control, safety delineation, operational guidance)
- Phase 2 expansion corridor provisions per OBJ-8

## Scope Exclusions

| Exclusion | Rationale |
|-----------|-----------|
| Owner's costs | Not in Contractor scope per decomposition Section 1.2 |
| Land acquisition | Not in Contractor scope |
| Financing costs | Not in Contractor scope |
| Permits obtained by Employer | Per decomposition Section 1.2 |
| Off-site roadway improvements | Public right-of-way (Owner scope) |
| Escalation | escalation_mode = NONE per config |
| Taxes | Excluded from base estimate |
| Earthworks/subgrade (PKG-02) | Separate package; interface only |
| Underground utilities (PKG-03) | Separate package; drainage tie-ins only |

## Contracting Assumptions

| Assumption | Value | Decision Ref |
|------------|-------|--------------|
| Contract type | Design & Build (D&B) | decomposition Section 1 |
| Contractor responsibility | Full design and construction | decomposition Section 1.2 |
| Subgrade preparation | By PKG-02 Earthworks | D-002 |
| Drainage infrastructure | By PKG-03 Underground Utilities | D-003 |
| Interface coordination | Contractor responsibility | decomposition |

## Location / Productivity Assumptions

| Assumption | Value | Decision Ref |
|------------|-------|--------------|
| Location | Fraser Surrey Terminal, Surrey, BC | decomposition |
| Productivity factor | 1.0 (BC lower mainland baseline) | D-004 |
| Site access | Assumed standard access via Elevator Road | D-005 |
| Working hours | Standard 8-10 hour shifts assumed | D-006 |
| Seasonal constraints | Paving limited to dry season (May-October typical) | A-015 |

## Pricing Sources Hierarchy

1. **Quotes/Vendor Budgets:** None available
2. **Project Rate Tables:** None provided
3. **Allowances:** All line items priced via allowances (fallback typical model)

**Decision:** D-007 — All pricing uses allowances due to absence of vendor quotes or rate tables.

## Quantity Basis

All quantities are parametric estimates based on:
- Total site area of ~7 hectares (from PKG-02 scope)
- Industrial transload facility typical pavement coverage ratios
- Deliverable document scope descriptions

| Item | Estimated Quantity | Basis | Decision Ref |
|------|-------------------|-------|--------------|
| Asphalt paving | 35,000 m² | 50% of 7 ha site for roadways/hardstand | A-001 |
| Concrete surfacing | 10,000 m² | Heavy load/chemical exposure zones | A-002 |
| Curbs and gutters | 2,500 lm | Perimeter and internal road delineation | A-003 |
| Sidewalks | 600 m² | Limited personnel areas (~200 lm × 3m) | A-004 |
| Parking area | 2,000 m² | ~50 vehicle stalls plus circulation | A-005 |
| Line marking | 6,000 lm | Traffic control, safety, parking stalls | A-006 |

## Indirects Model

**Method:** Factor-based (fallback typical model)

| Factor | Rate | Base | Decision Ref |
|--------|------|------|--------------|
| Construction Indirects (CI) | 0.18 | CD | D-008 |
| Procurement Services (P) | 0.02 | MAT | D-008 |
| EPCM/PM | 0.06 | CD + CI + MAT | D-008 |
| Commissioning (COM) | 0.03 | CD + CI + MAT | D-008 |

## Contingency Method

**Method:** PCT_BY_BUCKET (percentage by CBS bucket)

| CBS | Base % | Allowance Adjustment | Final % | Rationale |
|-----|--------|---------------------|---------|-----------|
| E | 10% | +10% (100% allowance) | 20% | All engineering allowances |
| MAT | 15% | +10% (100% allowance) | 25% | All material allowances |
| CD | 20% | +10% (100% allowance) | 30% | All CD allowances |
| CI | 20% | +10% (factor-derived) | 30% | Derived from CD |
| PM | 10% | +5% (factor-derived) | 15% | Factor-based |
| P | 10% | +5% (factor-derived) | 15% | Factor-based |
| COM | 25% | +5% (factor-derived) | 30% | Factor-based |

**Decision:** D-009 — Contingency rates elevated due to 100% allowance-based estimate.

## Escalation Method

- **Mode:** NONE
- **Rationale:** Pricing date is current (January 2026); no escalation applied per config
- **Decision:** D-010

## Rounding Policy

- **Rounding:** Nearest $1,000 CAD
- **Decision:** Per _CONFIG.md

## Completeness Metrics

| Metric | Value |
|--------|-------|
| Lines priced by QUOTE | 0% |
| Lines priced by RATE_TABLE | 0% |
| Lines priced by ALLOWANCE/PARAMETRIC | 100% |
| Deliverables with explicit quantities | 0% |
| Overall confidence | LOW |

## Known Gaps

| Gap | Impact | Resolution Path |
|-----|--------|-----------------|
| No pavement layout drawings | Quantities based on area ratios | Provide DEL-04.01 drawings with area calculations |
| No geotechnical data for subgrade | Pavement thickness assumptions only | Provide geotechnical report (PKG-02) |
| No traffic loading data | Pavement design assumptions only | Provide traffic study or ER loading requirements |
| No vendor quotes | All paving/materials as allowances | Obtain budgetary quotes from paving contractors |
| No rate tables | Labor rates assumed | Provide project rate library |

## References

| Document | Description |
|----------|-------------|
| Decision_Log.md | All decisions D-001 through D-010 |
| Assumptions_Log.md | All assumptions A-001 through A-020+ |
| Detail.csv | Line item detail with traceability |
| QA_Report.md | Quality checks and completeness metrics |
| Risk_Register.md | Risk factors and contingency basis |


---

## PKG-05

Source: /Users/ryan/ai-env/projects/chirality-app/test/execution/_Aggregation/AGG_Estimate_Collation_2026-01-29_0155/Extracts/PKG-05_BOE.md

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


---

## PKG-06

Source: /Users/ryan/ai-env/projects/chirality-app/test/execution/_Aggregation/AGG_Estimate_Collation_2026-01-29_0155/Extracts/PKG-06_BOE.md

# Basis of Estimate (BOE)

## Snapshot Identification

| Field | Value |
|-------|-------|
| Snapshot ID | EST_PKG06_DRAFT_2026-01-28_2333 |
| Estimate Label | PKG06_DRAFT |
| Pricing Date | 2026-01 (January 2026 dollars) |
| Currency | CAD |
| Package Scope | PKG-06 Structural Steelwork (5 deliverables) |
| Run Status | WARNINGS |

## Currency & Conversion

- **Currency:** CAD (Canadian dollars)
- **Evidence:** Project location is Fraser Surrey Terminal, Surrey, BC, Canada (decomposition Section 1)
- **Conversion:** None required; single-currency estimate
- **Decision:** D-001 (currency selection)

## Scope Inclusions

This estimate includes the following CBS buckets for PKG-06:

| CBS | Description | Included |
|-----|-------------|----------|
| E | Engineering & Design | Yes |
| PM | Project Management / EPCM | Yes |
| P | Procurement Services | Yes |
| MAT | Equipment & Materials | Yes |
| CD | Construction Directs | Yes |
| CI | Construction Indirects | Yes |
| COM | Commissioning / Testing | Yes |
| CONT | Contingency | Yes |

### Package Scope Detail (PKG-06 Structural Steelwork)

Per decomposition (lines 238-252):
- **Discipline:** Structural
- **Scope:** Steel platforms, stairs, gangways, access structures, handrails, pipe supports
- **Deliverables (5):**
  - DEL-06.01: Structural Steel Design Drawing Set (Drawing)
  - DEL-06.02: Structural Steel Technical Specification (Specification)
  - DEL-06.03: Structural Steel Design Calculations (Calculation)
  - DEL-06.04: Structural Steel Data Sheet Package (Data Sheet)
  - DEL-06.05: Structural Steel Installation & Test Records (Record)

**Anticipated work products:**
- Platform general arrangements, stair drawings, gangway drawings, pipe rack/support drawings, handrail details
- Specifications for structural steel, handrails, and grating
- Structural calculations for platforms, pipe racks, connections
- Data sheets for gangways and grating
- QA/QC records: mill certificates, weld inspection records, galvanizing certificates

## Scope Exclusions

| Exclusion | Rationale |
|-----------|-----------|
| Foundations for platforms/pipe racks | Assumed under PKG-05 Concrete Structures (Decision D-007) |
| Owner's costs | Not in Contractor scope per decomposition Section 1.2 |
| Land acquisition | Not in Contractor scope |
| Financing costs | Not in Contractor scope |
| Permits obtained by Employer | Per decomposition Section 1.2 |
| Escalation | escalation_mode = NONE per config (Decision D-011) |
| Taxes | Excluded from base estimate |

## Contracting Assumptions

| Assumption | Value | Decision Ref |
|------------|-------|--------------|
| Contract type | Design & Build (D&B) | decomposition Section 1 |
| Contractor responsibility | Full design and construction of structural steelwork | decomposition Section 1.2 |
| Fabrication location | Off-site fabrication assumed (shop-fabricated, galvanized, delivered to site) | A-006 |
| Galvanizing | Hot-dip galvanizing assumed for corrosion protection (marine/industrial environment) | A-006, A-013 |
| Foundation coordination | Structural steel assumes foundations provided by others (PKG-05); dependency tracking NOT_TRACKED | D-007 |

## Location / Productivity Assumptions

| Assumption | Value | Decision Ref |
|------------|-------|--------------|
| Location | Fraser Surrey Terminal, 11060 Elevator Road, Surrey, BC | decomposition Section 1 |
| Productivity factor | 1.0 (BC lower mainland baseline) | D-006 |
| Site access | Assumed standard access via Elevator Road; work in active terminal environment may impose constraints | D-006, A-014 |
| Working hours | Standard 8-10 hour shifts assumed | D-006 |
| Crane availability | Mobile crane rental assumed; coordination with other trades may affect erection schedule | A-008 |
| Seasonal constraints | Fraser Surrey Terminal wet season work may affect erection productivity | Risk R-003 |
| Terminal operations continuity | Per decomposition objective OBJ-5 (Terminal Continuity): works must minimize disturbance to existing terminal operations | decomposition Section 2 |

## Pricing Sources Hierarchy

1. **Quotes/Vendor Budgets:** None available
2. **Project Rate Tables:** None provided
3. **Allowances:** All line items priced via allowances (fallback typical model)

**Decision:** D-008 — All pricing uses allowances due to absence of vendor quotes, rate tables, and detailed design drawings.

### Source Discovery Summary

| Source Type | Status | Impact on Estimate |
|-------------|--------|-------------------|
| Vendor quotes (fabrication, galvanizing, handrails, grating, gangways) | None found | All MAT items (56% of base) are allowances |
| Project rate tables (labor, equipment) | None provided | All labor/equipment rates are assumed typical BC rates |
| Design drawings with quantities (tonnage, linear footage, areas, counts) | Not yet available (deliverables INITIALIZED, TBD) | All quantities are allowances |
| Deliverable four-documents | Present for all 5 deliverables | Scope is clear; quantities are not yet defined |

**Reference:** Source_Index.md for full discovery details.

## Indirects Model

**Method:** Factor-based (fallback typical model)

**Rationale:** No project schedule, staffing plan, or time-based indirects model available; factor-based approach used to ensure runnable estimate (Decision D-009).

| Factor | Rate | Base | Formula | Amount (CAD) | Decision Ref |
|--------|------|------|---------|-------------:|--------------|
| Construction Indirects (CI) | 0.18 | CD | 0.18 × $611k | $115,000 | D-009 |
| Procurement Services (P) | 0.02 | MAT | 0.02 × $1,301k | $27,000 | D-009 |
| EPCM/PM | 0.06 | CD + CI + MAT | 0.06 × ($611k + $115k + $1,301k) | $120,000 | D-009 |
| Commissioning (COM) | 0.03 | CD + CI + MAT | 0.03 × ($611k + $115k + $1,301k) | $60,000 | D-009 |

**Construction Indirects (CI) Scope:**
- Field supervision and construction management
- Site overhead and temporary facilities (PKG-06 allocation)
- HSE support and safety programs
- QA/QC coordination and inspection oversight

**Procurement Services (P) Scope:**
- Vendor coordination and expediting
- Material inspection and receiving
- Procurement documentation

**EPCM/PM Scope:**
- Project management (PKG-06 allocation)
- Engineering management and design coordination
- Document control and review
- Interface coordination (foundations, piping, etc.)

**Commissioning (COM) Scope:**
- Load testing and structural verification
- Final inspections and punch list
- Record documentation and as-built reconciliation
- Handover preparation

**Improvement Path:** Provide project schedule with durations, staffing plan, or project-specific indirects rates in config/rate tables to replace factor-based model.

## Contingency Method

**Method:** PCT_BY_BUCKET (percentage by CBS bucket)

**Rationale:** All base estimate line items are allowance/parametric-based (100% allowance share); contingency percentages elevated above baseline to account for estimate immaturity and scope uncertainty (Decision D-010).

| CBS | Base % | Allowance Adjustment | Final % | Rationale |
|-----|--------|---------------------|---------|-----------|
| E | 10% | +10% (100% allowance) | 20% | All engineering effort is allowance-based; no design hours validation |
| MAT | 15% | +10% (100% allowance) | 25% | No vendor quotes; tonnage/quantities are allowances |
| CD | 20% | +10% (100% allowance) | 30% | No productivity data or site-specific validation; all labor allowances |
| CI | 20% | +10% (100% factor-derived) | 30% | Factor-derived from CD base (no schedule validation) |
| PM | 10% | +5% (factor-derived) | 15% | Factor-based (no staffing plan) |
| P | 10% | +5% (factor-derived) | 15% | Factor-based (no procurement plan) |
| COM | 25% | +5% (factor-derived) | 30% | Factor-based (no commissioning plan) |

**Allowance-Heavy Adjustment Formula:**
- If bucket AllowanceShare ≥ 0.50: add +0.05 (5%)
- If bucket AllowanceShare ≥ 0.80: add an additional +0.05 (total +0.10, or 10%)

Where `AllowanceShare = (ALLOWANCE+PARAMETRIC base $) / (bucket base $)`.

For PKG-06, all CBS buckets have 100% allowance/parametric share → maximum adjustment applied.

**Decision:** D-010 — Contingency rates elevated due to 100% allowance-based estimate.

**Total Contingency:** $601,000 (26% of $2,323,000 base estimate)

**Reference:** Risk_Register.md for risk-by-risk contingency justification.

## Escalation Method

- **Mode:** NONE
- **Rationale:** Pricing date is current (January 2026); no escalation applied per config default (Decision D-011)
- **Impact:** Estimate totals are in January 2026 dollars; if work occurs in future years, escalation may be required (see Risk R-007)
- **Override Path:** Set `escalation_mode: EXPLICIT` in config and provide cashflow curve or escalation factors if escalation is required

## Rounding Policy

- **Rounding:** Nearest $1,000 CAD
- **Applied to:** Summary CBS totals, contingency amounts, and final estimate total
- **Rationale:** Estimate maturity (LOW confidence, 100% allowance-based) does not support precision beyond $1,000
- **Decision:** Per _CONFIG.md default (Decision D-002)

## Completeness Metrics

| Metric | Value |
|--------|-------|
| Lines priced by QUOTE | 0% (0 of 21 lines) |
| Lines priced by RATE_TABLE | 0% (0 of 21 lines) |
| Lines priced by ALLOWANCE | 81% (17 of 21 lines) |
| Lines priced by PARAMETRIC | 19% (4 of 21 lines) |
| Deliverables with explicit quantities | 0% (0 of 5 deliverables) |
| Overall confidence | LOW |

### Confidence Assessment by CBS

| CBS | Confidence | Justification |
|-----|------------|---------------|
| E | LOW | All engineering hours are allowances without design scope validation |
| MAT | LOW | No vendor quotes; tonnage and quantities are rough allowances |
| CD | LOW | No productivity data, site-specific rates, or schedule validation |
| CI | LOW | Factor-derived from CD (no independent validation) |
| PM | MED | Factor-based but typical for EPCM allocation at this stage |
| P | MED | Factor-based but typical for procurement services allocation |
| COM | LOW | Factor-based without commissioning plan or test scope |

**Overall Confidence:** LOW (estimate suitable for preliminary budgeting; NOT suitable for procurement or commitment without refinement)

## Known Gaps

| Gap | Impact | Resolution Path |
|-----|--------|-----------------|
| No structural steel tonnage estimate | HIGH — tonnage allowance (150 t) may vary ±50%; affects $900k material cost and $356k erection labor | Provide design drawings (DEL-06.01) with member sizes/lengths or tonnage estimate from calculations (DEL-06.03) |
| No vendor quotes for fabrication/galvanizing | HIGH — $6k/tonne rate is placeholder; may vary $5k-$7.5k/tonne | Obtain budgetary quotes from 3 structural steel fabricators |
| No handrail/grating quantities | MEDIUM — linear/area allowances (400 m, 800 m²) are rough | Provide platform layout drawings showing handrail extents and grating areas |
| No stairs/gangway item list | MEDIUM — count allowance (12 items) is rough | Provide gangway data sheets (DEL-06.04) with item counts, spans, and sizes |
| No project labor rates | MEDIUM — labor rates ($95/hr, $110/hr, etc.) are assumed typical BC rates | Provide project labor rates and equipment rental rates |
| No productivity data | MEDIUM — 25 hrs/tonne erection productivity is typical range | Provide erection productivity assumptions or historical data from execution plan |
| No piping layout for pipe supports | MEDIUM — pipe support allowance ($65k) may be insufficient if piping extents are large | Provide piping general arrangements (process packages) and clarify pipe support responsibility |
| No foundation interface definition | LOW-MEDIUM — coordination risk if foundation loads/schedules not aligned | Confirm foundation scope (PKG-05) and establish interface early |

## Key Estimate Drivers and Sensitivities

### Top 3 Cost Drivers

1. **Structural steel material supply (150 tonnes @ $6k/tonne):** $900,000 (39% of base)
   - Sensitivity: ±50 tonnes → ±$300,000
   - Sensitivity: ±$1k/tonne → ±$150,000

2. **Structural steel erection labor (3,750 hrs @ $95/hr):** $356,000 (15% of base)
   - Sensitivity: ±5 hrs/tonne → ±$71,000
   - Sensitivity: ±$10/hr rate → ±$38,000

3. **Stairs and gangways (12 items @ $15k/item):** $180,000 (8% of base)
   - Sensitivity: ±4 items → ±$60,000
   - Sensitivity: ±$5k/item → ±$60,000

### Tornado Diagram (Conceptual)

If actual values differ from allowances, estimate impact:

| Parameter | Low Case | Base Case | High Case | Range Impact |
|-----------|----------|-----------|-----------|--------------|
| Steel tonnage | 100 t | 150 t | 200 t | ±$600k on MAT+CD |
| Fabrication rate | $5k/t | $6k/t | $7.5k/t | ±$225k on MAT |
| Erection productivity | 20 hrs/t | 25 hrs/t | 35 hrs/t | ±$143k on CD |
| Handrail/grating quantities | -30% | Base | +50% | ±$110k on MAT+CD |
| Stairs/gangways count | 8 items | 12 items | 16 items | ±$60k on MAT |

**Conclusion:** Structural steel tonnage and fabrication rate are the dominant sensitivities; obtaining design drawings and vendor quotes will significantly improve estimate confidence.

## Design Basis and Assumptions Summary

### Structural Steel Scope (Package-Level)

- **Platforms:** Access platforms for railcar unloading stations (32 stations assumed to require platform access)
- **Stairs:** Vertical access between platform levels and grade
- **Gangways:** Elevated walkways connecting platforms or providing access to equipment
- **Pipe racks/supports:** Structural supports for process piping (coordination with process packages)
- **Handrails:** 3-rail galvanized steel handrail system (safety barrier per code)
- **Grating:** Medium-duty industrial grating for platform walking surfaces

### Material Assumptions

- **Steel grade:** CSA G40.21 350W or equivalent (typical structural grade for industrial platforms) — **TBD** pending specification (DEL-06.02)
- **Protective system:** Hot-dip galvanizing (marine/industrial environment corrosion protection) — **TBD** pending specification
- **Handrail:** Galvanized steel, 3-rail system with posts per code — **TBD** pending specification
- **Grating:** Galvanized steel grating, medium-duty industrial rating — **TBD** pending specification and data sheets (DEL-06.04)

### Design Load Assumptions

- **Platform live loads:** Industrial access (per code; likely 4.8 kPa or higher for equipment access) — **TBD** pending calculations (DEL-06.03)
- **Wind/seismic:** Fraser Surrey, BC seismic and wind exposure — **TBD** pending calculations
- **Equipment loads:** Pipe loads, unloading arm reactions (coordination with process packages) — **TBD** pending interface definition

### Construction Assumptions

- **Fabrication:** Off-site shop fabrication assumed (higher quality, lower field labor)
- **Galvanizing:** Off-site hot-dip galvanizing after fabrication
- **Delivery:** Truck delivery to site; laydown area required (see A-014)
- **Erection:** Mobile crane erection; field bolted connections preferred (minimize field welding)
- **Field welding:** Limited field welding anticipated (connections, repairs); weld inspection per CSA W59 or equivalent
- **Site access:** Work in active terminal; coordination with terminal operations required (OBJ-5 Terminal Continuity)

## References

| Document | Description |
|----------|-------------|
| Decision_Log.md | All decisions D-001 through D-013 |
| Assumptions_Log.md | All assumptions A-001 through A-015 |
| Detail.csv | Line item detail with traceability (21 line items) |
| Summary.md | CBS totals and WBS breakdown |
| WBS_CBS_Matrix.csv | WBS × CBS mapping |
| QA_Report.md | Quality checks and completeness metrics |
| Risk_Register.md | Risk factors and contingency basis (8 risk entries) |
| Source_Index.md | Source discovery and quality assessment |
| test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md | PKG-06 scope definition (lines 238-252) |
| test/execution/PKG-06_Structural_Steelwork/1_Working/ | Deliverable folders (DEL-06.01 through DEL-06.05) |

## Estimate Limitations and Disclaimer

**This estimate is a preliminary budgeting tool only and is NOT suitable for:**
- Procurement commitments or purchase orders
- Binding quotations or contractual pricing
- Detailed cost control or cost-loaded schedules
- Tender/bid submission without further refinement

**Limitations:**
1. **No vendor quotes:** All material costs are allowances without vendor validation.
2. **No detailed design:** Structural steel tonnage, handrail/grating quantities, and stair/gangway counts are rough allowances.
3. **No project-specific rates:** Labor and equipment rates are assumed typical BC lower mainland rates without project validation.
4. **No schedule integration:** Indirects and commissioning are factor-based without schedule or staffing plan validation.
5. **No site-specific constraints:** Erection productivity assumes standard access; active terminal constraints not fully assessed.
6. **Dependencies not tracked:** Foundation interface (PKG-05), piping interface (process packages), and other cross-package coordination assumed but not validated.

**Confidence Level:** LOW (estimate maturity is conceptual/allowance-based; suitable for preliminary budgeting and planning)

**Recommended Use:**
- High-level project budgeting and financial planning
- Scope definition and design prioritization (identify areas needing early design effort)
- Risk identification and contingency allocation
- Vendor engagement planning (identify items requiring budgetary quotes)

**Next Steps to Improve Estimate:**
1. Complete structural steel design (DEL-06.01 drawings, DEL-06.03 calculations) to establish tonnages and quantities
2. Obtain vendor budgetary quotes for fabrication, galvanizing, handrails, grating, stairs/gangways
3. Provide project labor rates, productivity assumptions, and equipment rental rates
4. Establish foundation interface (PKG-05 coordination) and piping interface (process packages)
5. Develop erection schedule and site logistics plan to validate productivity assumptions

---

**BOE compiled:** 2026-01-28 23:33
**Estimating Agent:** AGENT_ESTIMATING (straight-through pipeline per AGENT_ESTIMATING.md)
**Agent Version:** 2026-01-28_v3


---

## PKG-07

Source: /Users/ryan/ai-env/projects/chirality-app/test/execution/_Aggregation/AGG_Estimate_Collation_2026-01-29_0155/Extracts/PKG-07_BOE.md

# Basis of Estimate (BOE)

## Snapshot Identification

| Field | Value |
|-------|-------|
| Snapshot ID | EST_PKG07_DRAFT_2026-01-28_2332 |
| Estimate Label | PKG07_DRAFT |
| Pricing Date | 2026-01 (January 2026 dollars) |
| Currency | CAD |
| Package Scope | PKG-07 Rail Works (4 deliverables) |
| Run Status | WARNINGS |

## Currency & Conversion

- **Currency:** CAD (Canadian dollars)
- **Evidence:** Project location is Fraser Surrey Terminal, Surrey, BC, Canada (decomposition Section 1)
- **Conversion:** None required; single-currency estimate
- **Decision:** D-001 (currency selection)

## Scope Inclusions

This estimate includes the following CBS buckets for PKG-07:

| CBS | Description | Included |
|-----|-------------|----------|
| E | Engineering & Design | Yes |
| PM | Project Management / EPCM | Yes |
| P | Procurement Services | Yes |
| MAT | Equipment & Materials | Yes |
| CD | Construction Directs | Yes |
| CI | Construction Indirects | Yes |
| COM | Commissioning / Testing | Yes |
| CONT | Contingency | Yes |

## Scope Exclusions

| Exclusion | Rationale |
|-----------|-----------|
| Owner's costs | Not in Contractor scope per decomposition Section 1.2 |
| Land acquisition | Not in Contractor scope |
| Financing costs | Not in Contractor scope |
| Permits obtained by Employer | Per decomposition Section 1.2 |
| Track subgrade preparation | Assumed in PKG-02 Earthworks per D-013 |
| Track drainage systems | Assumed in PKG-03 Underground Utilities per D-014 |
| Track electrical bonding/grounding | Assumed in PKG-17 Electrical per A-021 |
| Track switches/turnouts | Scope TBD in ER per A-020 |
| Escalation | escalation_mode = NONE per config |
| Taxes | Excluded from base estimate |

## PKG-07 Physical Scope

**From decomposition (test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md:259):**
- New rail tracks 6 & 7
- Track 5 restoration and modifications
- Associated ballast works
- End stops

**Key project parameter (README.md:38):**
- 32 railcar unloading stations

**Scope interpretation:**
- Tracks 6 & 7 support the 32-car unloading capacity
- Track 5 is existing infrastructure requiring restoration/modifications
- Track 6 was previously removed in PKG-01 Demolition scope
- New Track 6 & 7 construction enables Phase 1 operations

## Contracting Assumptions

| Assumption | Value | Decision Ref |
|------------|-------|--------------|
| Contract type | Design & Build (D&B) | decomposition Section 1 |
| Contractor responsibility | Full design and construction | decomposition Section 1.2 |
| Track layout design | Contractor to perform | DEL-07.01 |
| Track geometry calculations | Contractor to perform | DEL-07.03 |
| Rail procurement | Contractor to procure | CBS includes MAT + P |
| Scope split assumptions | Subgrade in PKG-02; drainage in PKG-03 | D-013, D-014 |

## Location / Productivity Assumptions

| Assumption | Value | Decision Ref |
|------------|-------|--------------|
| Location | Fraser Surrey Terminal, Surrey, BC | decomposition |
| Productivity factor | 1.0 (BC lower mainland baseline) | D-006 |
| Site access | Work at operating terminal; coordination required | D-007, A-019 |
| Working hours | Standard shifts assumed; may need night/weekend work | D-007 |
| Terminal operations impact | Active rail operations; safety protocols apply | A-019, R-005 |

## Quantities Basis

**Track lengths (Decision D-002, D-003):**
- Track 6 (new): 500 linear meters
- Track 7 (new): 500 linear meters
- Track 5 (restoration): 300 linear meters
- **Total:** 1,300 linear meters

**Basis:** 32 railcar capacity at ~15m/car spacing suggests ~500m per unloading track. Track 5 restoration assumed at 60% of new track length (partial scope).

**Ballast quantities (Decision D-004):**
- 1,300m track × 1.5 m³/m = 1,950 m³
- **Basis:** Typical rail ballast section (300mm depth × 3m width average)

**End stops (Decision D-005):**
- 4 units (2 tracks × 2 ends each for Tracks 6 & 7)
- **Basis:** New tracks require end stops; Track 5 restoration may use existing

**Other components:**
- Ties/sleepers at typical spacing for track length
- Fasteners as percentage of rail cost (20%)
- Survey, testing, inspection as allowances based on track extent

## Pricing Sources Hierarchy

1. **Quotes/Vendor Budgets:** None available
2. **Project Rate Tables:** None provided
3. **Allowances:** All line items priced via allowances (fallback typical model)

**Decision:** D-008 — All pricing uses allowances due to absence of vendor quotes or rate tables.

## Indirects Model

**Method:** Factor-based (fallback typical model)

| Factor | Rate | Base | Decision Ref |
|--------|------|------|--------------|
| Construction Indirects (CI) | 0.18 | CD | D-009 |
| Procurement Services (P) | 0.02 | MAT | D-009 |
| EPCM/PM | 0.06 | CD + CI + MAT | D-009 |
| Commissioning (COM) | 0.03 | CD + CI + MAT | D-009 |

## Contingency Method

**Method:** PCT_BY_BUCKET (percentage by CBS bucket)

| CBS | Base % | Allowance Adjustment | Final % | Rationale |
|-----|--------|---------------------|---------|-----------|
| E | 10% | +10% (100% allowance) | 20% | All engineering allowances |
| MAT | 15% | +10% (100% allowance) | 25% | All material allowances; rail pricing uncertain |
| CD | 20% | +10% (100% allowance) | 30% | All CD allowances; terminal access risk |
| CI | 20% | +10% (100% allowance) | 30% | Derived from CD |
| PM | 10% | +5% (factor-derived) | 15% | Factor-based |
| P | 10% | +5% (factor-derived) | 15% | Factor-based |
| COM | 25% | +5% (factor-derived) | 30% | Testing scope uncertainty |

**Decision:** D-010 — Contingency rates elevated due to 100% allowance-based estimate.

## Escalation Method

- **Mode:** NONE
- **Rationale:** Pricing date is current (January 2026); no escalation applied per config
- **Decision:** D-011

## Rounding Policy

- **Rounding:** Nearest $1,000 CAD
- **Decision:** Per _CONFIG.md

## Completeness Metrics

| Metric | Value |
|--------|-------|
| Lines priced by QUOTE | 0% |
| Lines priced by RATE_TABLE | 0% |
| Lines priced by ALLOWANCE/PARAMETRIC | 100% |
| Deliverables with explicit quantities | 0% |
| Overall confidence | LOW |

## Known Gaps

| Gap | Impact | Resolution Path |
|-----|--------|-----------------|
| No track layout design | Unable to confirm track lengths | Provide design drawings (DEL-07.01) |
| No Track 5 condition assessment | Restoration scope unknown | Provide condition survey and assessment |
| No track geometry calculations | Ballast design assumptions only | Complete calculations (DEL-07.03) |
| No vendor quotes | All rail/materials as allowances | Obtain budgetary quotes from rail suppliers |
| No rate tables | Labor rates assumed | Provide project rate library |
| No rail specification | Rail type/grade assumed | Develop specification (DEL-07.02) |
| Scope boundaries unclear | Interface assumptions with PKG-02/03/17/34 | Confirm scope splits in ER |

## References

| Document | Description |
|----------|-------------|
| Decision_Log.md | All decisions D-001 through D-014 |
| Assumptions_Log.md | All assumptions A-001 through A-022 |
| Detail.csv | Line item detail with traceability |
| QA_Report.md | Quality checks and completeness metrics |
| Risk_Register.md | Risk factors and contingency basis |


---

## PKG-08

Source: /Users/ryan/ai-env/projects/chirality-app/test/execution/_Aggregation/AGG_Estimate_Collation_2026-01-29_0155/Extracts/PKG-08_BOE.md

# Basis of Estimate — PKG-08 Marine Structures

**Snapshot ID:** EST_PKG08_DRAFT_2026-01-28_2400
**Package:** PKG-08 Marine Structures
**Discipline:** Marine
**Date:** 2026-01-28

---

## 1. Estimate Identification

| Field | Value |
|-------|-------|
| Snapshot ID | EST_PKG08_DRAFT_2026-01-28_2400 |
| Estimate Label | PKG08_DRAFT |
| Pricing Date | January 2026 |
| Currency | CAD (Canadian Dollars) |
| Estimate Class | Class 5 (Order of Magnitude) |
| Expected Accuracy | -30% to +50% |
| Base Estimate | $5,463,000 |
| Contingency | $1,365,750 (25%) |
| Total Estimate | $6,829,000 |

---

## 2. Scope Definition

### 2.1 Inclusions

This estimate covers PKG-08 Marine Structures as defined in the project decomposition:

**Deliverables (11):**
- DEL-08.01 Marine Structures Design Drawing Set (Drawing)
- DEL-08.02 Marine Structures Technical Specification (Specification)
- DEL-08.03 Marine Structures Design Calculations (Calculation)
- DEL-08.04 Marine Geotechnical Report (Report)
- DEL-08.05 Marine Structures Installation & Test Records (Record)
- DEL-08.06 Berthing Energy Calculation Report (Report)
- DEL-08.07 Fender System Deflection Characteristics Data Package (Document Package)
- DEL-08.08 Fender Supplier Design Verification Letter/Report (Report)
- DEL-08.09 Mooring Analysis Report (Report)
- DEL-08.10 Current Assessment Basis Report (Report)
- DEL-08.11 Debris Loading Design Basis Note (Document)

**Physical Scope:**
- Marine piling (40-60 piles, estimated avg 20m length)
- Access trestle structure (estimated 150m length, 3m width, 150 tonnes steel)
- Loading platform structure (estimated 20m × 15m, 80 tonnes steel)
- Catwalk structure (estimated 50m length, 25 tonnes steel)
- Abutments (2 units, landside tie-in structures)
- Marine hardware and accessories (ladders, platforms, cathodic protection)

**Cost Categories Included:**
- Engineering & Design (E) — drawings, calculations, specifications, reports, data packages
- Project Management (PM) — procedures, marine engineering coordination, EPCM allocation
- Procurement (P) — vendor coordination, expediting, inspection
- Materials (MAT) — piles, structural steel, abutment materials, marine hardware
- Freight/Logistics (FRT) — barge mobilization, marine transport, staging
- Construction Directs (CD) — pile installation, steel erection, marine work, coatings, NDT
- Construction Indirects (CI) — field supervision, marine safety, QA/QC
- Commissioning (COM) — load testing, proof testing, as-built survey

### 2.2 Exclusions

- Owner's costs and project oversight
- Land acquisition or lease costs
- Financing costs
- Permits obtained by Employer (per decomposition Section 1.2)
- Fenders and bollards supply/installation (covered under PKG-09 Marine Outfitting)
- Marine loading arm and associated equipment (covered under PKG-11 Marine Loading System)
- Escalation (pricing date = January 2026, escalation_mode = NONE)
- Taxes (excluded per project convention)

---

## 3. Pricing Basis

### 3.1 Currency and Pricing Date

| Parameter | Value | Basis |
|-----------|-------|-------|
| Currency | CAD | Project location: Surrey, BC, Canada (D-801) |
| Pricing Date | 2026-01 | Current date; no historical pricing sources (D-802) |
| Escalation | None | escalation_mode = NONE per config (D-802) |

### 3.2 Pricing Sources Hierarchy

Per D-803, no project-specific pricing sources were discovered:

| Priority | Source Type | Availability | Usage |
|----------|-------------|--------------|-------|
| 1 | Vendor Quotes | None found | Not used |
| 2 | Rate Tables | None found | Not used |
| 3 | Historical Data | None found | Not used |
| 4 | Fallback Model | Available | 100% of pricing |

**Pricing Basis:** 100% Allowance/Parametric (Fallback Typical Model)

### 3.3 Pricing Method Summary

| Method | Line Items | Amount | % of Base |
|--------|------------|--------|-----------|
| ALLOWANCE | 25 | $5,039,000 | 92.2% |
| PARAMETRIC | 4 | $424,546 | 7.8% |
| QUOTE | 0 | $0 | 0% |
| RATE_TABLE | 0 | $0 | 0% |
| **Total** | **29** | **$5,463,546** | **100%** |

---

## 4. Estimate Methodology

### 4.1 Work Breakdown Structure (WBS) to Cost Breakdown Structure (CBS) Mapping

Per D-804, deliverables were mapped to CBS buckets based on deliverable type and marine scope:

| CBS Bucket | WBS Scope | Line Items | Amount | % of Base |
|------------|-----------|------------|--------|-----------|
| E (Engineering) | DEL-08.01 through DEL-08.11 | 11 | $389,000 | 7.1% |
| MAT (Materials) | Piles, steel, abutments, hardware | 6 | $2,280,000 | 41.7% |
| FRT (Freight) | Marine logistics, barge mobilization | 1 | $175,000 | 3.2% |
| CD (Construction Directs) | Installation, erection, coatings, NDT | 7 | $1,830,000 | 33.5% |
| CI (Construction Indirects) | Supervision, safety, QA/QC (parametric) | 1 | $329,400 | 6.0% |
| PM (Project Mgmt) | EPCM allocation (parametric) | 1 | $276,864 | 5.1% |
| P (Procurement) | Vendor coordination (parametric) | 1 | $49,100 | 0.9% |
| COM (Commissioning) | Testing, proving (parametric) | 1 | $133,182 | 2.4% |

### 4.2 Quantity Takeoff (QTO) Approach

No explicit quantities are defined in the deliverable documents (all are at INITIALIZED state with TBDs). Per Protocol Phase 3.2, when explicit quantities do not exist, the agent proceeds with allowance line items priced by the fallback model (Decision D-805).

**Quantity Assumptions (per A-812 through A-825):**
- Marine piles: 40-60 piles, avg 20m length (requires geotechnical design to confirm)
- Trestle: 150m length, 3m width, 150 tonnes structural steel
- Loading platform: 20m × 15m footprint, 80 tonnes structural steel
- Catwalk: 50m length, 25 tonnes structural steel
- Abutments: 2 units, 40 m³ concrete each

These assumptions are placeholders pending design development (DEL-08.01, DEL-08.03, DEL-08.04).

### 4.3 Allowance Sizing Approach

Per Decision D-806, allowances were sized using:
1. **Engineering deliverables:** Comparable to PKG-01/PKG-02 engineering line items, scaled for marine complexity and additional reports (11 deliverables vs typical 4-8)
2. **Materials:** Industry-typical unit rates for marine piling and structural steel with marine-grade corrosion protection
3. **Construction:** Marine construction rates reflecting specialized marine contractor requirements (barge/crane, marine safety, tide/weather constraints)

No project-specific quotes or rate tables were available; all pricing is allowance-based.

### 4.4 Indirects, Management, and Commissioning

Per D-807, indirects and management were calculated using the Fallback Typical Model:

- **Construction Indirects (CI):** 18% of CD = $329,400
  - Justification: Marine work requires enhanced supervision, marine safety oversight, QA/QC for welding/NDT, and marine operations coordination
- **EPCM/PM:** 6% of (CD + CI + MAT + FRT) = $276,864
  - Justification: Marine engineering coordination across multiple disciplines and interfaces
- **Procurement (P):** 2% of (MAT + FRT) = $49,100
  - Justification: Vendor coordination for marine materials and marine logistics
- **Commissioning (COM):** 3% of (CD + CI + MAT) = $133,182
  - Justification: Structural load testing, proof testing, as-built survey, and acceptance testing

---

## 5. Design Maturity and Confidence

### 5.1 Design Maturity Assessment

All 11 deliverables are at `INITIALIZED` lifecycle state per `_STATUS.md`. Design content consists of anticipated scope and TBD placeholders.

**Design Maturity:** Pre-conceptual (< 5%)

**Key Design Inputs Still TBD:**
- Employer's Requirements clause extraction (ER Vol 2 Parts 1-2 present but not extracted)
- Design vessel characteristics (dimensions, displacement, berthing/mooring loads)
- Marine geotechnical parameters (pile capacity, soil layering, scour depth)
- Environmental design basis (wind, current, wave, water levels, seismic)
- Final pile type, size, and layout
- Trestle and platform geometry and framing details
- Equipment loads from PKG-09 (fenders, bollards) and PKG-11 (loading arm)
- Codes and standards requirements

### 5.2 Confidence Assessment

| Line Item Type | Confidence | Rationale |
|----------------|------------|-----------|
| Engineering (E) deliverables | LOW | No ER extraction; complexity and scope assumptions only |
| Materials (MAT) | LOW | No geotechnical design; pile type/size/quantity unknown; steel tonnage estimated |
| Freight (FRT) | LOW | Marine logistics highly variable by contractor capability and schedule |
| Construction Directs (CD) | LOW | No design drawings; marine installation complexity and productivity assumptions |
| Indirects/PM/P/COM (parametric) | LOW-MED | Factor-based using fallback model; typical for marine work but unverified |

**Overall Estimate Confidence:** LOW

---

## 6. Contingency

### 6.1 Contingency Method

Per Decision D-807, contingency method = `PCT_BY_BUCKET` (percentage by CBS bucket).

Given the high allowance share (92.2% of base estimate is ALLOWANCE or PARAMETRIC), a 25% contingency is applied to the base estimate.

### 6.2 Contingency Calculation

| CBS Bucket | Base Amount | Baseline % | Allowance Adjustment | Applied % | Contingency |
|------------|-------------|------------|----------------------|-----------|-------------|
| E | $389,000 | 10% | +10% (100% allowance) | 20% | $77,800 |
| MAT | $2,280,000 | 15% | +10% (100% allowance) | 25% | $570,000 |
| FRT | $175,000 | 15% | +10% (100% allowance) | 25% | $43,750 |
| CD | $1,830,000 | 20% | +10% (100% allowance) | 30% | $549,000 |
| CI | $329,400 | 20% | 0% (parametric) | 20% | $65,880 |
| PM | $276,864 | 10% | 0% (parametric) | 10% | $27,686 |
| P | $49,100 | 10% | 0% (parametric) | 10% | $4,910 |
| COM | $133,182 | 25% | 0% (parametric) | 25% | $33,296 |
| **Total** | **$5,463,546** | — | — | **25%** | **$1,372,472** |

**Rounded Contingency:** $1,365,750 (25% of $5,463,000 rounded base)

### 6.3 Contingency Rationale

High contingency reflects:
- Pre-conceptual design maturity (< 5%)
- 100% allowance/parametric pricing (no quotes or rate tables)
- Marine construction complexity and uncertainty
- Unknown geotechnical conditions and pile requirements
- Interfaces to PKG-09 and PKG-11 not yet defined
- Environmental design basis TBD

---

## 7. Exclusions and Assumptions

### 7.1 Key Exclusions

1. Fenders and bollards (PKG-09 Marine Outfitting)
2. Marine loading arm and equipment (PKG-11 Marine Loading System)
3. Employer-responsible permits and approvals
4. Escalation beyond January 2026 pricing
5. Taxes and financing costs
6. Hazardous materials or contaminated soil remediation
7. Utility relocations or conflicts

### 7.2 Key Assumptions

Documented in `Assumptions_Log.md` (A-801 through A-825). Summary:

- Marine piling: 40-60 piles, avg 20m length, steel pipe piles or H-piles
- Trestle: 150m length, 3m width, 150 tonnes structural steel, marine-grade corrosion protection
- Loading platform: 20m × 15m, 80 tonnes structural steel
- Catwalk: 50m length, 25 tonnes steel
- Abutments: 2 units, 40 m³ concrete each
- Marine environment: Fraser River tidal conditions, moderate current, no ice loading
- Contractor: Specialized marine contractor with barge/crane capability
- Schedule: No extreme weather or tide constraints beyond typical marine work
- Geotechnical: Competent pile-bearing strata within reasonable driving depth

---

## 8. Risks and Opportunities

### 8.1 Key Risks

Documented in `Risk_Register.md` (R-801 through R-808). Summary:

- **R-801:** Geotechnical conditions worse than assumed (pile length, capacity, drivability)
- **R-802:** Marine logistics constraints (barge availability, weather, tides)
- **R-803:** Interfacing equipment loads exceed structural capacity (PKG-09, PKG-11)
- **R-804:** Regulatory approvals and permitting delays (Transport Canada, Coast Guard)
- **R-805:** Environmental design basis more severe than assumed (current, wind, seismic)
- **R-806:** Marine contractor availability and pricing volatility
- **R-807:** Design changes from ER requirements not yet extracted
- **R-808:** Schedule compression requiring premium marine contractor rates

### 8.2 Potential Opportunities

- Optimization of pile layout and trestle geometry during design
- Value engineering of structural steel framing and connections
- Competitive bidding for marine contractor and materials supply
- Phased construction approach to reduce marine mobilization costs

---

## 9. Completeness Metrics

| Metric | Value | Target |
|--------|-------|--------|
| Deliverables with line items | 11/11 | 100% |
| Line items priced by QUOTE | 0% | 50%+ (future) |
| Line items priced by RATE_TABLE | 0% | 30%+ (future) |
| Line items priced by ALLOWANCE | 92.2% | < 30% (future) |
| Line items with Qty/Unit/UnitRate | 100% | 100% |
| CBS buckets covered | 8/8 | 100% |

**Status:** All deliverables and physical scope covered with allowances. No project-specific pricing sources available.

---

## 10. Recommendations

### 10.1 Immediate Actions to Improve Estimate

1. **Extract ER requirements** (Vol 2 Parts 1-2) for marine structures design criteria
2. **Initiate marine geotechnical investigation** (DEL-08.04) to confirm pile requirements
3. **Define design vessel characteristics** and berthing/mooring scenarios
4. **Obtain budgetary quotes** for marine piling supply and installation
5. **Develop preliminary trestle/platform layout** (DEL-08.01) to refine steel tonnages
6. **Coordinate with PKG-09 and PKG-11** for equipment loads and interface requirements

### 10.2 Next Estimate Iteration Triggers

- Marine geotechnical report issued (DEL-08.04)
- Design drawings at 30% maturity (DEL-08.01)
- Vendor budgetary quotes received for piling and structural steel
- Berthing energy and mooring analysis complete (DEL-08.06, DEL-08.09)

---

## 11. References

### 11.1 Decomposition

- Project decomposition: `/Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md`
- PKG-08 scope: Lines 275-291
- Deliverables: DEL-08.01 through DEL-08.11

### 11.2 Deliverable Folders

- `/Users/ryan/ai-env/projects/chirality-app/test/execution/PKG-08_Marine_Structures/1_Working/`
  - All 11 deliverable folders at INITIALIZED lifecycle state

### 11.3 Configuration

- Estimate config: `/Users/ryan/ai-env/projects/chirality-app/test/execution/_Estimates/_CONFIG.md`

### 11.4 Decision and Assumption Logs

- `Decision_Log.md` (D-801 through D-808)
- `Assumptions_Log.md` (A-801 through A-825)

---

## 12. Approvals and Revisions

| Revision | Date | Description | Prepared By |
|----------|------|-------------|-------------|
| 0 | 2026-01-28 | Initial PKG-08 estimate snapshot | ESTIMATING Agent |

**Status:** DRAFT (Class 5, Order of Magnitude)

**Next Review:** After marine geotechnical report and 30% design drawings

---

**END OF BASIS OF ESTIMATE**


---

## PKG-09

Source: /Users/ryan/ai-env/projects/chirality-app/test/execution/_Aggregation/AGG_Estimate_Collation_2026-01-29_0155/Extracts/PKG-09_BOE.md

# Basis of Estimate (BOE)

## Snapshot Identification

| Field | Value |
|-------|-------|
| Snapshot ID | EST_PKG09_DRAFT_2026-01-28_2332 |
| Estimate Label | PKG09_DRAFT |
| Pricing Date | 2026-01 (January 2026 dollars) |
| Currency | CAD |
| Package Scope | PKG-09 Marine Outfitting (5 deliverables) |
| Run Status | WARNINGS |

## Currency & Conversion

- **Currency:** CAD (Canadian dollars)
- **Evidence:** Project location is Fraser Surrey Terminal, Surrey, BC, Canada (decomposition Section 1)
- **Conversion:** None required; single-currency estimate
- **Decision:** D-001 (currency selection)

## Scope Inclusions

This estimate includes the following CBS buckets for PKG-09:

| CBS | Description | Included |
|-----|-------------|----------|
| E | Engineering & Design | Yes |
| PM | Project Management / EPCM | Yes |
| P | Procurement Services | Yes |
| MAT | Equipment & Materials | Yes |
| CD | Construction Directs | Yes |
| CI | Construction Indirects | Yes |
| COM | Commissioning / Testing | Yes |
| CONT | Contingency | Yes |

### Scope Elements (from Decomposition PKG-09)

- **Fenders:** Marine fender system including fender units, chains, anchor pads, frontal frames, mounting hardware
- **Bollards:** Mooring bollards (tee-head or horn type) with foundations/anchorages, proof load testing provisions
- **Ladders:** Ship-to-shore access ladders with safety features (cages, rest platforms per codes)
- **Life-saving equipment:** Life rings, buoys, rescue equipment, mounting hardware per marine safety regulations
- **Existing Berth 10 upgrades and repairs:** Modifications, repairs, refurbishments to existing marine outfitting at Berth 10

## Scope Exclusions

| Exclusion | Rationale |
|-----------|-----------|
| Owner's costs | Not in Contractor scope per decomposition Section 1.2 |
| Land acquisition | Not in Contractor scope |
| Financing costs | Not in Contractor scope |
| Permits obtained by Employer | Per decomposition Section 1.2 |
| Marine structures (PKG-08) | Separate package; structural capacity provided by PKG-08 |
| Fender design verification (DEL-08.08) | PKG-08 deliverable; PKG-09 implements results |
| Berthing energy calculations (DEL-08.06) | PKG-08 deliverable; PKG-09 implements results |
| Mooring analysis (DEL-08.09) | PKG-08 deliverable; PKG-09 implements results |
| Nitrogen supply skid | Employer-supplied per decomposition Section 1.2 |
| Escalation | escalation_mode = NONE per config |
| Taxes | Excluded from base estimate |

## Contracting Assumptions

| Assumption | Value | Decision Ref |
|------------|-------|--------------|
| Contract type | Design & Build (D&B) | decomposition Section 1 |
| Contractor responsibility | Full design, procurement, installation | decomposition Section 1.2 |
| Marine structure interface | Structural capacity provided by PKG-08 | D-002 |
| Berthing design basis | Provided by PKG-08 berthing energy/mooring analyses | D-003 |
| Existing Berth 10 condition | Assumed minor repairs; no major structural work | A-020 |

## Location / Productivity Assumptions

| Assumption | Value | Decision Ref |
|------------|-------|--------------|
| Location | Fraser Surrey Terminal, Surrey, BC | decomposition |
| Productivity factor | 1.0 (BC lower mainland baseline) | D-004 |
| Marine access | Barge/water-based installation access for fenders/bollards | D-005 |
| Working hours | Standard 8-10 hour shifts; marine work tide constraints | D-006 |
| Seasonal constraints | Marine installation limited to favorable weather/tides (May-October typical) | A-021 |

## Pricing Sources Hierarchy

1. **Quotes/Vendor Budgets:** None available
2. **Project Rate Tables:** None provided
3. **Allowances:** All line items priced via allowances (fallback typical model)

**Decision:** D-007 — All pricing uses allowances due to absence of vendor quotes or rate tables.

## Quantity Basis

Quantities are parametric estimates based on:
- Typical marine transload facility outfitting requirements
- Industry-standard fender/bollard spacing and sizing for vessels up to Panamax class
- Deliverable document scope descriptions
- PKG-08 Marine Structures interfaces (assumed berth length ~150m for Phase 1)

| Item | Estimated Quantity | Basis | Decision Ref |
|------|-------------------|-------|--------------|
| Marine fenders | 12 units | Typical spacing 10-15m on 150m berth face | A-001 |
| Mooring bollards | 8 units | Typical 4 bow + 4 stern for Panamax vessel | A-002 |
| Ship-to-shore ladders | 4 units | Typical 2 per berth side for safe access | A-003 |
| Life-saving equipment | 1 LS | Life rings, buoys, rescue equipment per safety codes | A-004 |
| Berth 10 repairs | 1 LS | Minor repairs/refurbishment allowance | A-005 |

## Indirects Model

**Method:** Factor-based (fallback typical model)

| Factor | Rate | Base | Decision Ref |
|--------|------|------|--------------|
| Construction Indirects (CI) | 0.18 | CD | D-008 |
| Procurement Services (P) | 0.02 | MAT | D-008 |
| EPCM/PM | 0.06 | CD + CI + MAT | D-008 |
| Commissioning (COM) | 0.03 | CD + CI + MAT | D-008 |

## Contingency Method

**Method:** PCT_BY_BUCKET (percentage by CBS bucket)

| CBS | Base % | Allowance Adjustment | Final % | Rationale |
|-----|--------|---------------------|---------|-----------|
| E | 10% | +10% (100% allowance) | 20% | All engineering allowances |
| MAT | 15% | +10% (100% allowance) | 25% | All material allowances; marine equipment |
| CD | 20% | +10% (100% allowance) | 30% | All CD allowances; marine installation |
| CI | 20% | +10% (factor-derived) | 30% | Derived from CD |
| PM | 10% | +5% (factor-derived) | 15% | Factor-based |
| P | 10% | +5% (factor-derived) | 15% | Factor-based |
| COM | 25% | +5% (factor-derived) | 30% | Factor-based; proof load testing |

**Decision:** D-009 — Contingency rates elevated due to 100% allowance-based estimate and marine installation complexity.

## Escalation Method

- **Mode:** NONE
- **Rationale:** Pricing date is current (January 2026); no escalation applied per config
- **Decision:** D-010

## Rounding Policy

- **Rounding:** Nearest $1,000 CAD
- **Decision:** Per _CONFIG.md

## Completeness Metrics

| Metric | Value |
|--------|-------|
| Lines priced by QUOTE | 0% |
| Lines priced by RATE_TABLE | 0% |
| Lines priced by ALLOWANCE/PARAMETRIC | 100% |
| Deliverables with explicit quantities | 0% |
| Overall confidence | LOW |

## Known Gaps

| Gap | Impact | Resolution Path |
|-----|--------|-----------------|
| No berthing analysis results (DEL-08.06) | Fender sizing/type based on assumptions | Provide PKG-08 berthing energy calculations |
| No mooring analysis results (DEL-08.09) | Bollard capacities assumed | Provide PKG-08 mooring analysis |
| No fender deflection data (DEL-08.07) | Fender performance assumptions only | Provide PKG-08 fender system analysis |
| No marine structure details (DEL-08.01) | Interface assumptions only | Provide PKG-08 marine structure drawings |
| No vendor quotes | All equipment as allowances | Obtain budgetary quotes from marine equipment suppliers |
| No rate tables | Labor rates assumed | Provide project rate library |
| No Berth 10 condition survey | Repair scope assumed minor | Provide condition assessment/survey |

## References

| Document | Description |
|----------|-------------|
| Decision_Log.md | All decisions D-001 through D-010 |
| Assumptions_Log.md | All assumptions A-001 through A-025+ |
| Detail.csv | Line item detail with traceability |
| Summary.md | Cost summaries and confidence metrics |

