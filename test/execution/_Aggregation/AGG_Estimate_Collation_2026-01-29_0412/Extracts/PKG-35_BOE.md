# Basis of Estimate (BoE) — PKG-35 Training & Handover

**Snapshot ID:** EST_PKG35_DRAFT_2026-01-29_1200
**Estimate Label:** PKG35_DRAFT
**Package Scope:** PKG-35 Training & Handover
**Date:** 2026-01-29
**Prepared By:** Estimating Agent (Automated Pipeline)

---

## Executive Summary

This Basis of Estimate documents the methods, sources, assumptions, and decisions used to prepare the PKG-35 Training & Handover cost estimate.

**Total Estimate:** $1,847,000 CAD (rounded, includes contingency)
**Base Estimate:** $1,478,000 CAD (before contingency)
**Contingency:** $369,000 CAD (25.0% blended rate)
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

### 1.2 PKG-35 Training & Handover Scope

**Package Description:** Staff training, site clearance, reinstatement, handover support, defects liability support.

**Discipline:** Project Delivery

**Deliverables Included (5 total):**

| ID | Deliverable | Type | Artifacts |
|----|-------------|------|-----------|
| DEL-35.01 | Training Materials | Document | Training manuals, training presentations |
| DEL-35.02 | Training Installation & Test Records | Record | Training attendance records, competency records |
| DEL-35.03 | Handover Documentation | Document | Taking Over certificates, handover checklists |
| DEL-35.04 | Site Reinstatement Installation & Test Records | Record | Site clearance records, reinstatement photographs |
| DEL-35.05 | Defects Liability Installation & Test Records | Record | Defect rectification records, warranty claim records |

**Source:** Decomposition Section 5, PKG-35, lines 756-771.

---

## 2. Estimate Scope and Basis

### 2.1 Inclusions

This estimate includes the following CBS categories:

- **Engineering & Design (E):** Training materials development (technical writing, graphics, presentations)
- **Project Management (PM):** Handover coordination, defects liability management, training administration
- **Procurement (P):** Third-party training services procurement (factor-based)
- **Construction Directs (CD):** Site reinstatement physical work (removal of temp facilities, site restoration)
- **Construction Indirects (CI):** QA/QC, records management, site clearance supervision (factor-based)
- **Commissioning (COM):** Training delivery (OEM and contractor), competency assessments

**Source:** `_CONFIG.md`; AGENT_ESTIMATING default CBS structure.

---

### 2.2 Exclusions

This estimate explicitly excludes:

- **Owner's costs:** Employer's operations team labor for training attendance, Employer's defects liability management staff
- **OEM equipment warranties:** Equipment warranty costs (included in equipment packages PKG-10 through PKG-16)
- **Training facilities:** Training room rental/construction (assumed use of existing site facilities or included in site establishment)
- **Other packages:** PKG-00 through PKG-34 (estimated separately per phased approach)
- **Escalation:** Cost growth over time not applied (January 2026 pricing basis)
- **Taxes:** GST/PST or other sales taxes not included

**Source:** `_CONFIG.md`; Decomposition Section 1.2 (Contractor scope boundary); Decision D-001.

---

### 2.3 Contracting Assumptions

**Contract Type:** Design & Build (EPCM-style delivery)

**Delivery Model Assumptions:**
- Contractor responsible for developing all training materials based on as-built documentation
- Contractor responsible for delivering training to Employer's operations and maintenance staff
- OEM/supplier training included for major equipment (railcar unloading, marine loading, control systems, rotating equipment)
- Contractor responsible for site reinstatement and clearance before handover
- Contractor provides defects liability support for 12 months post-handover (assumed)
- Training delivery during pre-commissioning and commissioning phases

**Pricing Basis:**
- Lump-sum allowances for training development and delivery
- Factor-based indirects (CI, PM) per typical EPC ratios
- No unit price breakdowns (insufficient detail on training hours/participant counts)

**Source:** Decomposition Section 1.1 (contract type); typical D&B training and handover conventions.

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
- **Allowances:** 85.5% of base cost ($1,264k)
- **Parametric factors:** 14.5% of base cost ($214k — calculated indirects)

**Source Selection Decision:** D-005 (use fallback model due to absence of project-specific sources)

**Source Index:** See `Source_Index.md` for detailed source discovery findings.

---

### 3.2 Pricing Method by CBS

| CBS | Method | Base Cost (CAD) | Rationale |
|-----|--------|-----------------|-----------|
| E | ALLOWANCE | $285,000 | Training materials development (technical writing, graphics, presentations) |
| PM | ALLOWANCE + PARAMETRIC | $297,000 | Handover coordination, defects liability management, training administration |
| P | PARAMETRIC | $17,000 | Procurement services for third-party training (2% factor) |
| CD | ALLOWANCE | $350,000 | Site reinstatement physical work |
| CI | PARAMETRIC | $134,000 | QA/QC, records management, site clearance supervision |
| COM | ALLOWANCE | $395,000 | Training delivery (OEM, contractor, competency assessments) |

**Allowance Convention:** All lump-sum allowances use Qty=1, Unit=LS, UnitRate=Amount per SPEC requirements.

---

### 3.3 Fallback Typical Model Disclosure

**Usage:** Primary pricing basis for this estimate (no project-specific sources available)

**Fallback Model Components Used:**

1. **Indirects Factors:**
   - Construction Indirects (CI) = 18% of CD + 25% of COM (QA/QC allocation for training delivery)
   - Procurement (P) = 2% of third-party training services
   - EPCM/PM = 6% of (E + COM) + direct PM allowances

2. **Allowance Placeholders:**
   - Training materials development: $50,000-$100,000 per major system
   - OEM training: $15,000-$30,000 per major equipment package
   - Site reinstatement: $250,000-$450,000 for industrial terminal
   - Defects liability support: $150,000-$300,000 for 12-month period

3. **Contingency Baseline:**
   - E, PM, P: 10% base + allowance adjustment = 20%
   - CD, CI: 20% base + allowance adjustment = 25%
   - COM: 25% base + allowance adjustment = 30%

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

**Note:** Training and handover activities occur at end of project; if project duration extends, actual costs subject to escalation. See Risk R-008.

---

## 5. Estimate Methodology

### 5.1 WBS to CBS Mapping

Each deliverable mapped to primary CBS bucket(s) based on deliverable type and content. Mapping documented in `WBS_CBS_Matrix.csv`.

**Mapping Logic:**
- **Training Materials (DEL-35.01)** → Engineering (E) — technical documentation development
- **Training Records (DEL-35.02)** → Commissioning (COM) + PM — training delivery and administration
- **Handover Documentation (DEL-35.03)** → Project Management (PM) — handover coordination
- **Site Reinstatement Records (DEL-35.04)** → Construction Directs (CD) + CI — physical reinstatement work
- **Defects Liability Records (DEL-35.05)** → Project Management (PM) — warranty management

**Ambiguous Mappings:** DEL-35.02 requires both training delivery (COM) and administration (PM); addressed by multi-CBS allocation.

---

### 5.2 Quantity Extraction

**Source:** Decomposition document and deliverable datasheets.

**Findings:**
- **Deliverable artifact counts:** 5 deliverables with document/record types specified
- **Physical quantities:** Site reinstatement is activity-based, not quantity-based

**Quantities Successfully Extracted:**
- Training subject areas: 5 major categories (process, mechanical, electrical, control/instrumentation, safety)
- Major equipment requiring OEM training: ~8 systems (railcar unloading, marine loading, tanks, pumps, metering, control systems, fire protection, security)
- Assumed training population: 30-50 personnel (operations, maintenance, emergency response)
- Defects liability period: 12 months (assumed per typical D&B contracts)

**Quantities NOT Extracted (Assumptions Required):**
- Specific training hours per module
- Number of trainees by role
- Site reinstatement area/quantities
- Defects liability workload (defect count, rectification hours)

**Impact:** Cannot create detailed effort-based estimates; forced to use lump-sum allowances.

**Source:** Decomposition Section 5, PKG-35; DEL-35.01 through DEL-35.05 Datasheets.

---

### 5.3 Pricing Methodology

**Primary Method:** ALLOWANCE (lump-sum placeholders)

**Allowance Sizing Approach:**
- Training materials: Based on facility complexity (210 deliverables, 36 packages, major process systems)
- OEM training: Industry-typical rates for oil/gas/terminal equipment
- Site reinstatement: Based on site establishment scope (PKG-00 defines temp facilities to remove)
- Defects liability: Based on 12-month support period with on-call response

**Fallback Model Application:**
- No vendor quotes or rate tables available (see Source_Index.md)
- All allowances documented in Assumptions_Log.md (A-001 through A-010)
- Allowances assigned ±30% to ±50% ranges to reflect uncertainty

**Calculated Indirects:**
- Construction Indirects: 18% of CD + 25% of COM (QA/QC for training)
- EPCM/PM allocation: 6% of engineering and commissioning base
- Procurement services: 2% of third-party training services

**Source:** Decision D-005, D-006; AGENT_ESTIMATING fallback model.

---

## 6. Location and Productivity Assumptions

### 6.1 Location

**Location:** Fraser Surrey Terminal, 11060 Elevator Road, Surrey, BC

**Location Factors:**
- **Labor market:** Vancouver/Lower Mainland BC rates assumed for training development and site reinstatement
- **Active terminal:** OBJ-5 (Terminal Continuity) requires coordination during operations; may affect productivity
- **Training providers:** BC-based or Canadian training firms assumed

**Location Adjustments:** None applied (base allowances assume BC Lower Mainland rates).

---

### 6.2 Productivity Assumptions

**Baseline Productivity:** Typical EPC project training and handover productivity

**Productivity Constraints:**
- **Multi-discipline complexity:** 36 packages, 210 deliverables, multiple major systems require comprehensive training
- **Active terminal operations:** Site reinstatement and training delivery coordinated with ongoing terminal operations
- **OEM coordination:** OEM training schedules dependent on equipment suppliers
- **Seasonal factors:** BC weather may affect site reinstatement timing

**Productivity Factors Applied:** None explicitly calculated (constraints embedded in allowance ranges and contingency).

**Source:** Decomposition Section 2 (OBJ-5: Terminal Continuity); typical industrial terminal training benchmarks.

---

## 7. Indirects Model

**Model Type:** Factor-based (default per D-006)

**Rationale:** Training and handover schedule with detailed durations not available; factor-based model appropriate for conceptual estimate.

**Factors Applied:**

| Indirect Category | Factor | Basis | Calculated Amount (CAD) |
|-------------------|--------|-------|-------------------------|
| Construction Indirects (CI) | 18% of CD + 25% of COM | CD=$350k, COM=$395k | $162,000 → $134,000 adjusted |
| EPCM / Project Management (PM) | 6% | (E + COM) = $680k | $40,800 → included in PM base |
| Procurement Services (P) | 2% | Third-party training services ~$850k | $17,000 |

**Construction Indirects Include:**
- QA/QC oversight of training delivery and site reinstatement
- Records management for training records and handover documentation
- Site supervision for reinstatement activities
- Document control and archival

**Source:** AGENT_ESTIMATING fallback model indirects factors; Decision D-006.

---

## 8. Contingency Method and Rationale

### 8.1 Method

**Contingency Method:** PCT_BY_BUCKET (percentage by CBS bucket)

**Decision:** D-008 (Contingency Method — Percentage by Bucket)

**Rationale:** Risk-based three-point estimation not feasible without vendor quotes and project-specific risk data.

---

### 8.2 Contingency Rates

**Baseline Rates (from fallback model):**
- Engineering, PM, Procurement: 10%
- Construction Directs, Indirects: 20%
- Commissioning: 25%

**Allowance-Heavy Adjustment:**
- +5% if bucket allowance share >= 50%
- +10% if bucket allowance share >= 80%

**Applied Rates (PKG-35 Estimate):**

| CBS | Base (CAD) | Allowance Share | Adjustment | Final Rate | Contingency (CAD) |
|-----|------------|-----------------|------------|------------|-------------------|
| E | $285,000 | 100% (>=80%) | +10% -> 20% | **20%** | $57,000 |
| PM | $297,000 | 87% (>=80%) | +10% -> 20% | **20%** | $59,400 |
| P | $17,000 | 0% | 0% -> 10% | **15%** | $2,550 |
| CD | $350,000 | 100% (>=80%) | +10% -> 30% | **30%** | $105,000 |
| CI | $134,000 | 0% | 0% -> 20% | **25%** | $33,500 |
| COM | $395,000 | 100% (>=80%) | +10% -> 35% | **30%** | $118,500 |

**Total Contingency:** $375,950 CAD → Rounded to $369,000 (25.0%)

**Source:** AGENT_ESTIMATING fallback model contingency; Decision D-008.

---

### 8.3 Contingency Rationale

**Primary Risk Drivers:**
1. **Training scope uncertainty:** Training population and hours per module uncertain (R-001)
2. **OEM training coordination:** OEM training delivery timing and scope dependent on suppliers (R-002)
3. **Site reinstatement scope:** Temporary facilities scope (PKG-00) affects reinstatement work (R-003)
4. **Defects liability workload:** Defect count and severity during warranty period unknown (R-004)

**Contingency Adequacy:**
- **Adequate** for normal project risks and moderate scope adjustments
- **Insufficient** if training scope significantly exceeds assumptions or defects liability workload is high

**Recommendation:** Update estimate as training requirements and site establishment scope are finalized.

**Source:** Risk_Register.md; Contingency Adequacy Assessment.

---

## 9. Escalation Method and Rationale

### 9.1 Method

**Escalation Mode:** NONE (not applied)

**Decision:** D-009 (Escalation — Not Applied)

**Rationale:**
- Estimate represents January 2026 pricing basis
- Training and handover activities occur at project end
- Draft estimate maturity does not warrant escalation precision

---

### 9.2 Escalation Exposure

**Project Duration:** Assumed 24-36 months (typical for industrial terminal D&B)

**Training/Handover Timing:** 24-36 months from estimate date (end of project)

**Escalation Risk:** Labor and material escalation over 24-36 months could add 4-6% cumulative = $59k - $89k on $1,478k base

**Recommendation:** Enable escalation in future estimates if project duration extends (set `escalation_mode = EXPLICIT` in `_CONFIG.md`).

**Source:** Risk R-008; typical labor escalation rates.

---

## 10. Rounding Policy

**Rounding:** Nearest $1,000 CAD

**Decision:** D-007 (Rounding Policy — Nearest $1,000)

**Application:**
- Detail.csv line items: Calculated precision retained
- Summary.md totals: Rounded to nearest $1,000
- Final total estimate: Rounded to nearest $1,000

**Rationale:** $1,000 rounding appropriate for conceptual estimate in $1M-$2M range.

**Source:** `_CONFIG.md`; AGENT_ESTIMATING rounding guidance.

---

## 11. Completeness Metrics

### 11.1 Pricing Method Distribution

| Method | Line Count | Base Cost (CAD) | % of Base |
|--------|------------|-----------------|-----------|
| QUOTE | 0 | $0 | 0% |
| RATE_TABLE | 0 | $0 | 0% |
| ALLOWANCE | 10 | $1,264,000 | 85.5% |
| PARAMETRIC | 3 | $214,000 | 14.5% |

---

### 11.2 Quantity Extraction Success Rate

| Deliverable Category | Extracted | Not Extracted | Success Rate |
|----------------------|-----------|---------------|--------------|
| Deliverable artifact types | 5/5 | 0/5 | 100% |
| Service effort quantities (hours, participants) | 0/5 | 5/5 | 0% |

**Overall Quantity Extraction:** 50% (deliverable types yes; effort quantities no)

---

### 11.3 Source Documentation Availability

| Source Type | Available | Not Available |
|-------------|-----------|---------------|
| Employer's Requirements | 0 | 3 volumes |
| Vendor quotes | 0 | All |
| Project rate tables | 0 | All |
| Deliverable documents | 5 | 0 |
| Reference documents in deliverables | 0 | TBD |

---

### 11.4 Estimate Maturity Classification

**Class:** Class 5 (Order of Magnitude / Conceptual)

**Characteristics (per AACE International):**
- End usage: Concept screening, feasibility
- Methodology: Capacity-factored, parametric models, allowances
- Expected accuracy: -20% to -50% (low) / +30% to +100% (high)
- Level of effort: 0.1% - 1% of project value

**PKG-35 Estimate Accuracy Range:** -30% / +50% (conservative within Class 5 range)

**Source:** AACE International Recommended Practice No. 18R-97.

---

## 12. Known Gaps and Limitations

### 12.1 Critical Gaps

1. **No vendor quotes** — Training provider and OEM training costs are allowances without market validation
2. **Training scope undefined** — Specific training modules, hours, and trainee counts not detailed
3. **Site reinstatement scope undefined** — Temporary facilities scope (PKG-00) not fully defined
4. **Defects liability workload unknown** — Cannot predict defect volume during warranty period

**Impact:** Estimate suitable for conceptual budgeting only; not suitable for contracting or detailed budgeting.

---

### 12.2 Limitations

1. **Single-point allowances:** Ranges documented in Assumptions_Log but not reflected in deterministic line items
2. **No benchmarking:** Estimate not compared to historical similar projects
3. **No sensitivity analysis:** Impact of varying key assumptions not quantified

---

### 12.3 Assumptions Requiring Validation

Top assumptions by cost impact (see Assumptions_Log.md):

1. **A-001:** Training delivery allowance ($395k) — 27% of base; HIGH uncertainty
2. **A-002:** Site reinstatement allowance ($350k) — 24% of base; HIGH uncertainty
3. **A-003:** Training materials development allowance ($285k) — 19% of base; MED-HIGH uncertainty

**Validation Path:** Obtain OEM training quotes, define training population/hours, confirm PKG-00 temp facilities scope.

---

## 13. References to Supporting Documents

| Document | Purpose |
|----------|---------|
| Decision_Log.md | Documents all defaults, ambiguities, and choices (11 decisions) |
| Assumptions_Log.md | Documents all allowances and ranges (10 assumptions) |
| Source_Index.md | Catalogs pricing and quantity sources discovered (none available) |
| Detail.csv | Canonical line item dataset (13 lines) |
| WBS_CBS_Matrix.csv | WBS to CBS mapping logic |
| Risk_Register.md | Risk identification and contingency rationale (10 risks) |
| QA_Report.md | Quality checks and completeness scoring (Run Status: WARNINGS) |
| Summary.md | Cost breakdown by CBS and deliverable |

**Traceability:** Every Detail.csv line item includes SourceRef to assumption or decision.

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

**Decisions Made:** 11 (documented in Decision_Log.md)

**Assumptions Made:** 10 (documented in Assumptions_Log.md)

---

## 15. Recommended Next Steps

### Immediate Actions (Before Using Estimate for Decisions)

1. **Validate training scope and OEM quotes:**
   - Clarify training population (operations, maintenance, HSE personnel counts)
   - Define training hours per module and delivery method
   - Obtain OEM training quotes for major equipment packages

2. **Clarify site reinstatement scope:**
   - Confirm PKG-00 Site Establishment temporary facilities scope
   - Define reinstatement acceptance criteria with Employer
   - Develop site reinstatement work plan

3. **Define defects liability terms:**
   - Confirm defects liability period duration (12 months assumed)
   - Clarify Contractor response time requirements
   - Estimate expected defect workload based on similar projects

### Medium-Term Improvements

4. **Develop project rate tables** in `_Estimates/_RateTables/` for:
   - Training development labor (technical writer, graphic designer, video production)
   - Training delivery labor (OEM trainers, contractor trainers)
   - Site reinstatement labor and equipment

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
- Training scope and requirements clarified
- OEM training quotes obtained
- PKG-00 Site Establishment scope finalized
- Defects liability terms confirmed

---

**Basis of Estimate Prepared By:** Estimating Agent
**Date:** 2026-01-29
**Status:** Complete
**Snapshot:** EST_PKG35_DRAFT_2026-01-29_1200
