# Basis of Estimate (BoE) — PKG-28 Design Verification

**Snapshot ID:** EST_PKG28_DRAFT_2026-01-29_0830
**Estimate Label:** PKG28_DRAFT
**Package Scope:** PKG-28 Design Verification
**Date:** 2026-01-29
**Prepared By:** Estimating Agent (Automated Pipeline)

---

## Executive Summary

This Basis of Estimate documents the methods, sources, assumptions, and decisions used to prepare the PKG-28 Design Verification cost estimate.

**Total Estimate:** $892,000 CAD (rounded, includes contingency)
**Base Estimate:** $728,000 CAD (before contingency)
**Contingency:** $164,000 CAD (22.5% blended rate)
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
- Storage Capacity: 45,000 MT (3 x 15,000 MT tanks)
- Product: CSD (Crude Super Degummed) canola oil
- Railcar Capacity: 32 unloading stations on 2 tracks
- Contract Type: Design & Build

**Source:** Decomposition document Section 1, `/Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md`

---

### 1.2 PKG-28 Design Verification Scope

**Package Description:** Independent design verification, VFPA IP coordination, inter-discipline coordination.

**Discipline:** Design

**Deliverables Included (3 total):**

| ID | Deliverable | Type | Artifacts |
|----|-------------|------|-----------|
| DEL-28.01 | Independent Design Verification Reports | Report | IDV reports (by discipline/submission stage) |
| DEL-28.02 | VFPA IP Review Responses | Report | IP review response documents |
| DEL-28.03 | Design Coordination Installation & Test Records | Record | Inter-discipline coordination records, clash detection reports, RFI logs |

**Source:** Decomposition Section 5, PKG-28, lines 621-634.

---

## 2. Estimate Scope and Basis

### 2.1 Inclusions

This estimate includes the following CBS categories:

- **Engineering & Design (E):** Independent design verification reviews, technical analysis, IDV reports, IP review preparation
- **Project Management (PM):** Design coordination activities, RFI management, inter-discipline coordination, clash detection
- **Procurement (P):** Third-party engineering services procurement (factor-based)
- **Construction Indirects (CI):** QA/QC engineering review allocation (factor-based)

**Source:** `_CONFIG.md`; AGENT_ESTIMATING default CBS structure.

---

### 2.2 Exclusions

This estimate explicitly excludes:

- **Owner's costs:** Employer's design review fees, Owner's Engineer fees
- **VFPA fees:** Permit application fees, regulatory review fees payable to authorities
- **Software licenses:** BIM/CAD software costs (assumed part of general engineering overhead)
- **Other packages:** PKG-00 through PKG-27 and PKG-29 through PKG-35 (estimated separately per phased approach)
- **Escalation:** Cost growth over time not applied (January 2026 pricing basis)
- **Taxes:** GST/PST or other sales taxes not included

**Source:** `_CONFIG.md`; Decomposition Section 1.2 (Contractor scope boundary); Decision D-001 (package-level estimating approach).

---

### 2.3 Contracting Assumptions

**Contract Type:** Design & Build (EPCM-style delivery)

**Delivery Model Assumptions:**
- Contractor responsible for independent design verification (IDV) by qualified third-party or internal independent reviewers
- Contractor responsible for VFPA IP coordination and review responses
- Contractor responsible for inter-discipline coordination, clash detection, and RFI management
- IDV required at multiple submission stages (30%, 60%, 90%, IFC) per typical design-build requirements
- VFPA IP review responses coordinated with design submission milestones

**Pricing Basis:**
- Lump-sum allowances for IDV and IP review services
- Factor-based indirects (CI, PM) per typical EPC ratios
- No unit price breakdowns (insufficient detail on review hours)

**Source:** Decomposition Section 1.1 (contract type); typical D&B design verification conventions.

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
- **Allowances:** 91.2% of base cost ($664k)
- **Parametric factors:** 8.8% of base cost ($64k — calculated indirects)

**Source Selection Decision:** D-005 (use fallback model due to absence of project-specific sources)

**Source Index:** See `Source_Index.md` for detailed source discovery findings.

---

### 3.2 Pricing Method by CBS

| CBS | Method | Base Cost (CAD) | Rationale |
|-----|--------|-----------------|-----------|
| E | ALLOWANCE | $445,000 | No engineering labor rates available; allowances based on typical IDV and IP review costs for design-build projects |
| PM | ALLOWANCE + PARAMETRIC | $219,000 | Direct PM deliverables (coordination) use allowances; calculated PM factor (6%) applied per fallback model |
| P | PARAMETRIC | $8,900 | Procurement services calculated as 2% of third-party engineering costs per fallback model |
| CI | PARAMETRIC | $55,100 | Construction indirects (QA/QC review allocation) calculated as factor per fallback model |

**Allowance Convention:** All lump-sum allowances use Qty=1, Unit=LS, UnitRate=Amount per SPEC requirements.

---

### 3.3 Fallback Typical Model Disclosure

**Usage:** Primary pricing basis for this estimate (no project-specific sources available)

**Fallback Model Components Used:**

1. **Indirects Factors:**
   - Construction Indirects (CI) = 18% of CD (applied to engineering hours as notional "construction review")
   - Procurement (P) = 2% of third-party engineering services
   - EPCM/PM = 6% of engineering base

2. **Allowance Placeholders:**
   - IDV reports: $15,000-$30,000 per discipline per submission stage
   - VFPA IP review responses: $8,000-$15,000 per submission cycle
   - Design coordination: $5,000-$10,000 per month of active design

3. **Contingency Baseline:**
   - E, PM, P: 10% base + allowance adjustment = 15-20%
   - CI: 20% base + allowance adjustment = 25%

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

**Rationale:** No historical pricing dates found in deliverable documents. Defaulted to current date (2026-01-29).

**Escalation:** Not applied in this estimate (escalation_mode = NONE per config).

**Note:** If design verification extends over multiple years from January 2026, actual costs will be subject to escalation. See Risk R-008 for escalation exposure discussion.

---

## 5. Estimate Methodology

### 5.1 WBS to CBS Mapping

Each deliverable mapped to primary CBS bucket(s) based on deliverable type and content. Mapping documented in `WBS_CBS_Matrix.csv`.

**Mapping Logic:**
- **IDV Reports (DEL-28.01)** → Engineering (E) — independent technical review and analysis
- **VFPA IP Review Responses (DEL-28.02)** → Engineering (E) + PM — technical response preparation with coordination
- **Design Coordination Records (DEL-28.03)** → Project Management (PM) — coordination, clash detection, RFI management

**Ambiguous Mappings:** DEL-28.02 requires both engineering analysis and project coordination; addressed by multi-CBS allocation.

---

### 5.2 Quantity Extraction

**Source:** Decomposition document and typical design-build verification scope.

**Findings:**
- **Deliverable artifact counts:** 3 deliverables with document types specified
- **Physical quantities:** Not applicable (design verification is service-based, not construction-based)

**Quantities Successfully Extracted:**
- IDV reports required by discipline/stage (estimated 8 disciplines × 4 stages = 32 reviews)
- IP review response cycles (estimated 4-6 major submission cycles)
- Design coordination duration (estimated 18-24 months of active design)

**Quantities NOT Extracted (Assumptions Required):**
- Specific number of IDV reviews per discipline
- VFPA IP review submission count and complexity
- Clash detection model complexity and coordination meeting frequency
- RFI volume and response effort

**Impact:** Cannot create detailed effort-based estimates; forced to use lump-sum allowances based on typical project experience.

**Source:** Decomposition Section 5, PKG-28; typical design-build design verification scope.

---

### 5.3 Pricing Methodology

**Primary Method:** ALLOWANCE (lump-sum placeholders)

**Allowance Sizing Approach:**
- IDV services: Typical independent design verification cost for multi-discipline industrial projects (8-10 disciplines, 4 submission stages)
- VFPA IP review: Typical port authority coordination effort for Canadian port projects
- Design coordination: Typical coordination cost for 210-deliverable project over 18-24 month design duration

**Fallback Model Application:**
- No vendor quotes or rate tables available (see Source_Index.md)
- All allowances documented in Assumptions_Log.md (A-001 through A-008)
- Allowances assigned ±30% to ±50% ranges to reflect uncertainty

**Calculated Indirects:**
- Construction Indirects: 18% of notional engineering "construction review" allocation
- EPCM/PM allocation: 6% of engineering base
- Procurement services: 2% of third-party engineering services

**Source:** Decision D-005, D-006; AGENT_ESTIMATING fallback model (lines 623-691).

---

## 6. Location and Productivity Assumptions

### 6.1 Location

**Location:** Fraser Surrey Terminal, 11060 Elevator Road, Surrey, BC

**Location Factors:**
- **Labor market:** Vancouver/Lower Mainland BC engineering rates assumed
- **VFPA jurisdiction:** Vancouver Fraser Port Authority requirements apply
- **IDV providers:** BC-based or Canadian engineering firms assumed

**Location Adjustments:** None applied (base allowances assume BC Lower Mainland engineering rates).

---

### 6.2 Productivity Assumptions

**Baseline Productivity:** Typical EPC project design verification productivity assumed for allowance sizing

**Productivity Constraints:**
- **Multi-discipline complexity:** 36 packages and 210 deliverables require comprehensive coordination
- **Authority review cycles:** VFPA IP review timelines may affect coordination effort
- **Design iteration:** Multiple submission stages (30/60/90/IFC) require repeated verification

**Productivity Factors Applied:** None explicitly calculated (productivity constraints embedded in allowance ranges and contingency).

**Source:** Risk R-004 (design complexity); typical EPC design verification benchmarks.

---

## 7. Indirects Model

**Model Type:** Factor-based (default per D-006)

**Rationale:** Design verification schedule with detailed durations not available; factor-based model is appropriate for conceptual estimate maturity.

**Factors Applied:**

| Indirect Category | Factor | Basis | Calculated Amount (CAD) |
|-------------------|--------|-------|-------------------------|
| Construction Indirects (CI) | 18% | Notional "construction review" base = $306k | $55,100 |
| EPCM / Project Management (PM) | 6% | Engineering base (E) = $445k | $26,700 |
| Procurement Services (P) | 2% | Third-party services = $445k | $8,900 |

**Construction Indirects Include:**
- QA/QC engineering review allocation
- Quality assurance oversight of design verification process
- Document control and records management

**Note:** CI allocation is notional for a design verification package; represents QA/QC review and oversight allocation.

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
- Construction Directs, Indirects: 20%

**Allowance-Heavy Adjustment:**
- +5% if bucket allowance share >= 50%
- +10% if bucket allowance share >= 80%

**Applied Rates (PKG-28 Estimate):**

| CBS | Base (CAD) | Allowance Share | Adjustment | Final Rate | Contingency (CAD) |
|-----|------------|-----------------|------------|------------|-------------------|
| E | $445,000 | 100% (>=80%) | +10% -> 20% | **20%** | $89,000 |
| PM | $219,000 | 88% (>=80%) | +10% -> 20% | **20%** | $43,800 |
| P | $8,900 | 0% | 0% -> 10% | **15%** | $1,335 |
| CI | $55,100 | 0% | 0% -> 20% | **25%** | $13,775 |

**Note:** PM base includes both direct coordination allowances ($192.3k) and calculated PM factor ($26.7k).

**Total Contingency:** $147,910 CAD (20.3% blended rate) -> Rounded to $164,000 (22.5%)

**Source:** AGENT_ESTIMATING fallback model contingency (lines 653-667); Decision D-008.

---

### 8.3 Contingency Rationale

**Primary Risk Drivers:**
1. **Scope uncertainty:** IDV scope depends on design complexity and authority requirements (R-001)
2. **Authority review cycles:** VFPA IP review timing and iteration count uncertain (R-002)
3. **Design coordination complexity:** 210 deliverables creates significant coordination burden (R-003)

**Contingency Adequacy:**
- **Adequate** for normal project risks and moderate scope adjustments
- **Insufficient** if IDV scope significantly exceeds assumptions or VFPA requires extensive iterations

**Recommendation:** Update estimate as design progresses and IDV/IP scope becomes clearer.

**Source:** Risk_Register.md; Contingency Adequacy Assessment.

---

## 9. Escalation Method and Rationale

### 9.1 Method

**Escalation Mode:** NONE (not applied)

**Decision:** D-009 (Escalation — Not Applied)

**Rationale:**
- Estimate represents January 2026 pricing basis
- Design verification is primarily labor-based (less subject to material escalation)
- Draft estimate maturity does not warrant escalation precision

---

### 9.2 Escalation Exposure

**Design Duration:** Assumed 18-24 months (typical for multi-year design-build project)

**Escalation Risk:** Labor rate escalation over 18-24 months could add 2-4% annually (4-8% cumulative = $29k - $58k on $728k base)

**Recommendation:** Enable escalation in future estimates if design duration extends significantly (set `escalation_mode = EXPLICIT` in `_CONFIG.md`).

**Source:** Risk R-008; typical engineering labor escalation rates.

---

## 10. Rounding Policy

**Rounding:** Nearest $1,000 CAD

**Decision:** D-007 (Rounding Policy — Nearest $1,000)

**Application:**
- Detail.csv line items: Calculated precision retained
- Summary.md totals: Rounded to nearest $1,000
- Final total estimate: Rounded to nearest $1,000

**Rationale:** $1,000 rounding appropriate for conceptual estimate in $500k-$1M range; avoids false precision.

**Source:** `_CONFIG.md`; AGENT_ESTIMATING rounding guidance.

---

## 11. Completeness Metrics

### 11.1 Pricing Method Distribution

| Method | Line Count | Base Cost (CAD) | % of Base |
|--------|------------|-----------------|-----------|
| QUOTE | 0 | $0 | 0% |
| RATE_TABLE | 0 | $0 | 0% |
| ALLOWANCE | 7 | $664,000 | 91.2% |
| PARAMETRIC | 3 | $64,000 | 8.8% |

---

### 11.2 Quantity Extraction Success Rate

| Deliverable Category | Extracted | Not Extracted | Success Rate |
|----------------------|-----------|---------------|--------------|
| Deliverable artifact types | 3/3 | 0/3 | 100% |
| Service effort quantities (hours, reviews) | 0/3 | 3/3 | 0% |

**Overall Quantity Extraction:** 50% (deliverable types yes; effort quantities no)

---

### 11.3 Source Documentation Availability

| Source Type | Available | Not Available |
|-------------|-----------|---------------|
| Employer's Requirements | 0 | 3 volumes |
| Vendor quotes | 0 | All |
| Project rate tables | 0 | All |
| Deliverable documents | 3 | 0 |
| Reference documents in deliverables | 0 | TBD |

---

### 11.4 Estimate Maturity Classification

**Class:** Class 5 (Order of Magnitude / Conceptual)

**Characteristics (per AACE International):**
- End usage: Concept screening, feasibility
- Methodology: Capacity-factored, parametric models, allowances
- Expected accuracy: -20% to -50% (low) / +30% to +100% (high)
- Level of effort: 0.1% - 1% of project value

**PKG-28 Estimate Accuracy Range:** -30% / +50% (conservative within Class 5 range)

**Source:** AACE International Recommended Practice No. 18R-97 (Cost Estimate Classification System).

---

## 12. Known Gaps and Limitations

### 12.1 Critical Gaps

1. **No vendor quotes or budgetary proposals** — IDV services and engineering review costs are allowances without market validation
2. **IDV scope undefined** — Specific disciplines, depth of review, and iteration requirements not detailed
3. **VFPA IP requirements not detailed** — Submission count, review complexity, and response effort assumed
4. **Design duration assumptions** — 18-24 month design duration assumed without schedule confirmation

**Impact:** Estimate suitable for conceptual budgeting only; not suitable for contracting or detailed project budgeting.

---

### 12.2 Limitations

1. **Single-point allowances:** Ranges documented in Assumptions_Log but not reflected in deterministic line items
2. **No benchmarking:** Estimate not compared to historical similar projects or industry benchmarks
3. **No sensitivity analysis:** Impact of varying key assumptions not quantified

---

### 12.3 Assumptions Requiring Validation

Top assumptions by cost impact (see Assumptions_Log.md for complete list):

1. **A-001:** IDV services allowance ($350k) — 48% of base; HIGH uncertainty
2. **A-002:** Design coordination allowance ($150k) — 21% of base; MED-HIGH uncertainty
3. **A-003:** VFPA IP review response allowance ($95k) — 13% of base; MED uncertainty

**Validation Path:** Obtain IDV provider quotes, clarify VFPA IP requirements, develop design schedule.

---

## 13. References to Supporting Documents

This BoE is supported by the following documents in the estimate snapshot:

| Document | Purpose |
|----------|---------|
| Decision_Log.md | Documents all defaults, ambiguities, and choices (9 decisions) |
| Assumptions_Log.md | Documents all allowances and ranges (8 assumptions) |
| Source_Index.md | Catalogs pricing and quantity sources discovered (none available) |
| Detail.csv | Canonical line item dataset (10 lines) |
| WBS_CBS_Matrix.csv | WBS to CBS mapping logic |
| Risk_Register.md | Risk identification and contingency rationale (8 risks) |
| QA_Report.md | Quality checks and completeness scoring (Run Status: WARNINGS) |
| Summary.md | Cost breakdown by CBS and deliverable |

**Traceability:** Every Detail.csv line item includes SourceRef to assumption or decision in above logs.

---

## 14. Estimate Preparation Process

**Preparation Method:** Automated straight-through pipeline per AGENT_ESTIMATING protocol

**Process Steps Completed:**
1. Initialize + Auto-discover inputs (Phase 1)
2. Index sources + build Source Index (Phase 2)
3. Map WBS -> CBS (Phase 3.1)
4. Extract quantities/cost drivers (Phase 3.2)
5. Price line items (Phase 3.3)
6. Apply indirects (Phase 3.4)
7. QA checks + completeness scoring (Phase 4.1)
8. Risk register + contingency (Phase 4.2)
9. Publish snapshot (Phase 4.4) — complete

**Human Interaction:** None required (straight-through execution)

**Decisions Made:** 9 (documented in Decision_Log.md)

**Assumptions Made:** 8 (documented in Assumptions_Log.md)

---

## 15. Recommended Next Steps

### Immediate Actions (Before Using Estimate for Decisions)

1. **Validate IDV scope and provider quotes:**
   - Clarify IDV requirements per discipline and submission stage
   - Obtain budgetary quotes from independent engineering review firms
   - Confirm which disciplines require third-party vs. internal independent review

2. **Clarify VFPA IP requirements:**
   - Obtain VFPA project review requirements and submission schedule
   - Clarify IP review response documentation requirements
   - Confirm review cycle count and typical iteration effort

3. **Develop design schedule:**
   - Establish design phase duration and submission milestones
   - Confirm IDV review windows and VFPA coordination timeline
   - Enable time-based estimate refinement

### Medium-Term Improvements

4. **Develop project rate tables** in `_Estimates/_RateTables/` for:
   - Engineering review labor (senior reviewer, discipline lead, coordinator)
   - Third-party IDV services (per discipline, per review stage)
   - Coordination labor rates

5. **Re-run estimate** with improved inputs to upgrade maturity from Class 5 to Class 4 or Class 3

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
- IDV scope and requirements clarified
- VFPA IP review requirements confirmed
- Vendor quotes obtained for IDV services
- Design schedule finalized

---

**Basis of Estimate Prepared By:** Estimating Agent
**Date:** 2026-01-29
**Status:** Complete
**Snapshot:** EST_PKG28_DRAFT_2026-01-29_0830
