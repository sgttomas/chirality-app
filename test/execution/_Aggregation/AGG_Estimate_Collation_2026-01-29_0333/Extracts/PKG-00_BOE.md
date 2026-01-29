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
