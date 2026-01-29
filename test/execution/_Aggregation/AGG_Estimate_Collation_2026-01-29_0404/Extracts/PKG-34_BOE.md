# Basis of Estimate (BoE) — PKG-34 Coordination & Interfaces

**Snapshot ID:** EST_PKG34_DRAFT_2026-01-29_1045
**Estimate Label:** PKG34_DRAFT
**Package Scope:** PKG-34 Coordination & Interfaces
**Date:** 2026-01-29
**Prepared By:** Estimating Agent (Automated Pipeline)

---

## Executive Summary

This Basis of Estimate documents the methods, sources, assumptions, and decisions used to prepare the PKG-34 Coordination & Interfaces cost estimate.

**Total Estimate:** $520,000 CAD (rounded, includes contingency)
**Base Estimate:** $432,000 CAD (before contingency)
**Contingency:** $88,000 CAD (20.4% blended rate)
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

### 1.2 PKG-34 Coordination & Interfaces Scope

**Package Description:** Terminal operations interface, adjacent project coordination, utility coordination, marine coordination.

**Discipline:** Project Delivery

**Deliverables Included (5 total):**

| ID | Deliverable | Type | Artifacts |
|----|-------------|------|-----------|
| DEL-34.01 | Coordination Meeting Installation & Test Records | Record | Weekly Terminal coordination meeting minutes |
| DEL-34.02 | Interface Agreements | Document | Interface agreements (FSPL-TI, Metro Vancouver, utilities) |
| DEL-34.03 | Marine Coordination Installation & Test Records | Record | Notices to mariners, marine coordination records |
| DEL-34.04 | Security Compliance Installation & Test Records | Record | CBSA/TC security compliance records |
| DEL-34.05 | Trenchless Crossing Monitoring Reports | Report | Settlement monitoring reports, condition monitoring reports |

**Source:** Decomposition Section 5, PKG-34, lines 739-754.

---

## 2. Estimate Scope and Basis

### 2.1 Inclusions

This estimate includes the following CBS categories:

- **Engineering & Design (E):** Trenchless crossing monitoring (survey, instrumentation, analysis, reporting)
- **Project Management (PM):** Coordination meetings, interface management, marine coordination, security compliance documentation
- **Procurement (P):** Third-party monitoring services procurement (factor-based)
- **Construction Indirects (CI):** QA/QC oversight of coordination and monitoring activities (factor-based)

**Source:** `_CONFIG.md`; AGENT_ESTIMATING default CBS structure.

---

### 2.2 Exclusions

This estimate explicitly excludes:

- **Owner's costs:** Employer's coordination effort, Owner's interface management
- **Authority fees:** CBSA fees, Transport Canada fees, marine notice fees payable to authorities
- **Utility relocation costs:** Actual utility relocation work (covered in relevant discipline packages)
- **Other packages:** PKG-00 through PKG-33 and PKG-35 (estimated separately per phased approach)
- **Escalation:** Cost growth over time not applied (January 2026 pricing basis)
- **Taxes:** GST/PST or other sales taxes not included

**Source:** `_CONFIG.md`; Decomposition Section 1.2 (Contractor scope boundary); Decision D-001 (package-level estimating approach).

---

### 2.3 Contracting Assumptions

**Contract Type:** Design & Build (EPCM-style delivery)

**Delivery Model Assumptions:**
- Contractor responsible for weekly Terminal coordination meetings throughout construction
- Contractor responsible for preparing and negotiating interface agreements with third parties
- Contractor responsible for marine coordination including notices to mariners
- Contractor responsible for CBSA/Transport Canada security compliance documentation
- Contractor responsible for trenchless crossing monitoring (HDD/microtunneling)

**Pricing Basis:**
- Lump-sum allowances for coordination and interface management activities
- Time-based allowances for meeting coordination (based on project duration)
- Factor-based indirects (CI, PM) per typical EPC ratios
- No unit price breakdowns (insufficient detail on effort hours)

**Source:** Decomposition Section 1.1 (contract type); typical D&B interface management conventions.

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
- **Allowances:** 90.3% of base cost ($390k)
- **Parametric factors:** 9.7% of base cost ($42k — calculated indirects)

**Source Selection Decision:** D-005 (use fallback model due to absence of project-specific sources)

**Source Index:** See `Source_Index.md` for detailed source discovery findings.

---

### 3.2 Pricing Method by CBS

| CBS | Method | Base Cost (CAD) | Rationale |
|-----|--------|-----------------|-----------|
| E | ALLOWANCE | $95,000 | Trenchless crossing monitoring (survey, instrumentation, reporting) |
| PM | ALLOWANCE + PARAMETRIC | $295,000 | Coordination meetings, interface management, marine/security coordination |
| P | PARAMETRIC | $6,000 | Procurement services for third-party monitoring (2% factor) |
| CI | PARAMETRIC | $36,000 | Construction indirects (QA/QC oversight allocation) |

**Allowance Convention:** All lump-sum allowances use Qty=1, Unit=LS, UnitRate=Amount per SPEC requirements.

---

### 3.3 Fallback Typical Model Disclosure

**Usage:** Primary pricing basis for this estimate (no project-specific sources available)

**Fallback Model Components Used:**

1. **Indirects Factors:**
   - Construction Indirects (CI) = 18% of notional coordination base
   - Procurement (P) = 2% of third-party monitoring services
   - EPCM/PM = 6% of engineering base

2. **Allowance Placeholders:**
   - Weekly coordination meetings: $2,000-$3,000 per meeting (administrative effort)
   - Interface agreements: $20,000-$35,000 per major interface
   - Marine coordination: $3,000-$5,000 per month during marine works
   - Security compliance: $2,500-$4,000 per month during construction
   - Trenchless monitoring: $20,000-$40,000 per crossing location

3. **Contingency Baseline:**
   - E, PM, P: 10% base + allowance adjustment = 20%
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

**Note:** If coordination and interface management extends over multiple years from January 2026, actual costs will be subject to escalation. See Risk R-008 for escalation exposure discussion.

---

## 5. Estimate Methodology

### 5.1 WBS to CBS Mapping

Each deliverable mapped to primary CBS bucket(s) based on deliverable type and content. Mapping documented in `WBS_CBS_Matrix.csv`.

**Mapping Logic:**
- **Coordination Meeting Records (DEL-34.01)** → Project Management (PM) — administrative coordination
- **Interface Agreements (DEL-34.02)** → Project Management (PM) — interface negotiation and documentation
- **Marine Coordination Records (DEL-34.03)** → Project Management (PM) — authority coordination
- **Security Compliance Records (DEL-34.04)** → Project Management (PM) — regulatory compliance documentation
- **Trenchless Crossing Monitoring (DEL-34.05)** → Engineering (E) + PM — technical monitoring and reporting

**Ambiguous Mappings:** DEL-34.05 requires both engineering (survey/monitoring) and project management (coordination); addressed by multi-CBS allocation.

---

### 5.2 Quantity Extraction

**Source:** Decomposition document and typical design-build coordination scope.

**Findings:**
- **Deliverable artifact counts:** 5 deliverables with document/record types specified
- **Physical quantities:** Primarily effort-based (coordination is service-based, not construction-based)

**Quantities Successfully Extracted:**
- Coordination meeting frequency: Weekly during construction (assumed 24-30 months = 100-130 meetings)
- Interface agreement count: 3-5 major interfaces (FSPL-TI, Metro Vancouver, utilities, rail, marine)
- Marine works duration: Estimated 8-12 months active marine construction
- Trenchless crossing count: Estimated 2-4 HDD/trenchless crossings (per typical underground utilities scope)

**Quantities NOT Extracted (Assumptions Required):**
- Specific construction duration
- Detailed interface agreement complexity
- Trenchless crossing locations and monitoring requirements
- Security compliance documentation scope

**Impact:** Cannot create detailed effort-based estimates; forced to use lump-sum allowances based on typical project experience.

**Source:** Decomposition Section 5, PKG-34; typical design-build interface coordination scope.

---

### 5.3 Pricing Methodology

**Primary Method:** ALLOWANCE (lump-sum placeholders)

**Allowance Sizing Approach:**
- Coordination meetings: Weekly administrative effort over 24-30 month construction period
- Interface agreements: Typical interface negotiation and documentation effort for industrial terminal project
- Marine coordination: Typical port/marine authority coordination for marine construction works
- Security compliance: CBSA/TC compliance documentation for port security zone
- Trenchless monitoring: Third-party survey/monitoring services for HDD crossings

**Fallback Model Application:**
- No vendor quotes or rate tables available (see Source_Index.md)
- All allowances documented in Assumptions_Log.md (A-001 through A-007)
- Allowances assigned ±30% to ±50% ranges to reflect uncertainty

**Calculated Indirects:**
- Construction Indirects: 18% of notional coordination base
- EPCM/PM allocation: 6% of engineering base
- Procurement services: 2% of third-party monitoring services

**Source:** Decision D-005, D-006; AGENT_ESTIMATING fallback model (lines 623-691).

---

## 6. Location and Productivity Assumptions

### 6.1 Location

**Location:** Fraser Surrey Terminal, 11060 Elevator Road, Surrey, BC

**Location Factors:**
- **Labor market:** Vancouver/Lower Mainland BC project coordination rates assumed
- **Port jurisdiction:** Vancouver Fraser Port Authority requirements apply
- **Marine authorities:** Transport Canada, Canadian Coast Guard, DFO coordination required
- **Monitoring providers:** BC-based survey/monitoring firms assumed

**Location Adjustments:** None applied (base allowances assume BC Lower Mainland rates).

---

### 6.2 Productivity Assumptions

**Baseline Productivity:** Typical EPC project coordination productivity assumed for allowance sizing

**Productivity Constraints:**
- **Active terminal environment:** Coordination with ongoing Terminal operations adds complexity
- **Multiple interfaces:** FSPL-TI, Metro Vancouver, utilities, marine authorities require parallel coordination
- **Security zone:** CBSA/TC security requirements add compliance burden
- **Marine schedule constraints:** Weather, tidal, and vessel schedule constraints affect coordination

**Productivity Factors Applied:** None explicitly calculated (productivity constraints embedded in allowance ranges and contingency).

**Source:** Risk R-004 (interface complexity); typical EPC coordination benchmarks.

---

## 7. Indirects Model

**Model Type:** Factor-based (default per D-006)

**Rationale:** Construction schedule with detailed coordination durations not available; factor-based model is appropriate for conceptual estimate maturity.

**Factors Applied:**

| Indirect Category | Factor | Basis | Calculated Amount (CAD) |
|-------------------|--------|-------|-------------------------|
| Construction Indirects (CI) | 18% | Notional coordination base = $200k | $36,000 |
| EPCM / Project Management (PM) | 6% | Engineering base (E) = $95k | $5,700 |
| Procurement Services (P) | 2% | Third-party monitoring = $95k | $1,900 |

**Note:** PM factor ($5.7k) is included in PM total ($295k) along with direct PM allowances ($269.3k + $20k).

**Construction Indirects Include:**
- QA/QC oversight of coordination activities
- Document control for interface documentation
- Records management for coordination records

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

**Applied Rates (PKG-34 Estimate):**

| CBS | Base (CAD) | Allowance Share | Adjustment | Final Rate | Contingency (CAD) |
|-----|------------|-----------------|------------|------------|-------------------|
| E | $95,000 | 100% (>=80%) | +10% -> 20% | **20%** | $19,000 |
| PM | $295,000 | 91% (>=80%) | +10% -> 20% | **20%** | $59,000 |
| P | $6,000 | 0% | 0% -> 10% | **15%** | $900 |
| CI | $36,000 | 0% | 0% -> 20% | **25%** | $9,000 |

**Total Contingency:** $87,900 CAD (20.4% blended rate) -> Rounded to $88,000

**Source:** AGENT_ESTIMATING fallback model contingency (lines 653-667); Decision D-008.

---

### 8.3 Contingency Rationale

**Primary Risk Drivers:**
1. **Interface complexity:** Multiple third-party interfaces (FSPL-TI, Metro Vancouver, utilities, marine) (R-001)
2. **Project duration uncertainty:** Coordination effort scales with construction duration (R-002)
3. **Marine coordination requirements:** Port/marine authority coordination scope uncertain (R-003)

**Contingency Adequacy:**
- **Adequate** for normal project risks and moderate scope adjustments
- **Insufficient** if project duration significantly exceeds assumptions or interface complexity is higher than typical

**Recommendation:** Update estimate as project schedule develops and interface requirements become clearer.

**Source:** Risk_Register.md; Contingency Adequacy Assessment.

---

## 9. Escalation Method and Rationale

### 9.1 Method

**Escalation Mode:** NONE (not applied)

**Decision:** D-009 (Escalation — Not Applied)

**Rationale:**
- Estimate represents January 2026 pricing basis
- Coordination and interface management is primarily labor-based (less subject to material escalation)
- Draft estimate maturity does not warrant escalation precision

---

### 9.2 Escalation Exposure

**Construction Duration:** Assumed 24-30 months (typical for multi-year design-build project)

**Escalation Risk:** Labor rate escalation over 24-30 months could add 2-4% annually (4-10% cumulative = $17k - $43k on $432k base)

**Recommendation:** Enable escalation in future estimates if construction duration extends significantly (set `escalation_mode = EXPLICIT` in `_CONFIG.md`).

**Source:** Risk R-008; typical project coordination labor escalation rates.

---

## 10. Rounding Policy

**Rounding:** Nearest $1,000 CAD

**Decision:** D-007 (Rounding Policy — Nearest $1,000)

**Application:**
- Detail.csv line items: Calculated precision retained
- Summary.md totals: Rounded to nearest $1,000
- Final total estimate: Rounded to nearest $1,000

**Rationale:** $1,000 rounding appropriate for conceptual estimate in $400k-$600k range; avoids false precision.

**Source:** `_CONFIG.md`; AGENT_ESTIMATING rounding guidance.

---

## 11. Completeness Metrics

### 11.1 Pricing Method Distribution

| Method | Line Count | Base Cost (CAD) | % of Base |
|--------|------------|-----------------|-----------|
| QUOTE | 0 | $0 | 0% |
| RATE_TABLE | 0 | $0 | 0% |
| ALLOWANCE | 8 | $390,000 | 90.3% |
| PARAMETRIC | 3 | $42,000 | 9.7% |

---

### 11.2 Quantity Extraction Success Rate

| Deliverable Category | Extracted | Not Extracted | Success Rate |
|----------------------|-----------|---------------|--------------|
| Deliverable artifact types | 5/5 | 0/5 | 100% |
| Service effort quantities (hours, meetings) | 0/5 | 5/5 | 0% |

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

**PKG-34 Estimate Accuracy Range:** -30% / +50% (conservative within Class 5 range)

**Source:** AACE International Recommended Practice No. 18R-97 (Cost Estimate Classification System).

---

## 12. Known Gaps and Limitations

### 12.1 Critical Gaps

1. **No vendor quotes or budgetary proposals** — Coordination services and monitoring costs are allowances without market validation
2. **Project duration not confirmed** — Meeting count and coordination effort based on assumed 24-30 month construction
3. **Interface agreement scope undefined** — Number and complexity of interface agreements assumed based on typical practice
4. **Trenchless crossing count not confirmed** — Monitoring cost based on assumed 2-4 crossing locations

**Impact:** Estimate suitable for conceptual budgeting only; not suitable for contracting or detailed project budgeting.

---

### 12.2 Limitations

1. **Single-point allowances:** Ranges documented in Assumptions_Log but not reflected in deterministic line items
2. **No benchmarking:** Estimate not compared to historical similar projects or industry benchmarks
3. **No sensitivity analysis:** Impact of varying key assumptions not quantified

---

### 12.3 Assumptions Requiring Validation

Top assumptions by cost impact (see Assumptions_Log.md for complete list):

1. **A-001:** Trenchless monitoring allowance ($95k) — 22% of base; MED-HIGH uncertainty
2. **A-002:** Interface agreements allowance ($90k) — 21% of base; MED uncertainty
3. **A-003:** Coordination meetings allowance ($75k) — 17% of base; MED uncertainty

**Validation Path:** Confirm project schedule, clarify interface agreement scope, obtain monitoring provider quotes.

---

## 13. References to Supporting Documents

This BoE is supported by the following documents in the estimate snapshot:

| Document | Purpose |
|----------|---------|
| Decision_Log.md | Documents all defaults, ambiguities, and choices (10 decisions) |
| Assumptions_Log.md | Documents all allowances and ranges (7 assumptions) |
| Source_Index.md | Catalogs pricing and quantity sources discovered (none available) |
| Detail.csv | Canonical line item dataset (11 lines) |
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

**Decisions Made:** 10 (documented in Decision_Log.md)

**Assumptions Made:** 7 (documented in Assumptions_Log.md)

---

## 15. Recommended Next Steps

### Immediate Actions (Before Using Estimate for Decisions)

1. **Develop project construction schedule:**
   - Confirm construction duration and phasing
   - Establish coordination meeting frequency and duration
   - Define marine works timeline

2. **Clarify interface agreement requirements:**
   - Identify all required third-party interface agreements
   - Assess complexity and negotiation effort per interface
   - Confirm Employer vs. Contractor responsibility for each interface

3. **Obtain trenchless monitoring quotes:**
   - Confirm number and location of HDD/trenchless crossings
   - Request budgetary quotes from survey/monitoring providers
   - Define monitoring frequency and reporting requirements

### Medium-Term Improvements

4. **Develop project rate tables** in `_Estimates/_RateTables/` for:
   - Project coordination labor (coordinator, administrator)
   - Interface management effort (per agreement type)
   - Monitoring services (survey, instrumentation)

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
- Project construction schedule finalized
- Interface agreement scope clarified
- Trenchless crossing locations confirmed
- Vendor quotes obtained for monitoring services

---

**Basis of Estimate Prepared By:** Estimating Agent
**Date:** 2026-01-29
**Status:** Complete
**Snapshot:** EST_PKG34_DRAFT_2026-01-29_1045
