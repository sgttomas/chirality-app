# Decision Log — PKG-32 Regulatory & Permits

**Snapshot ID:** EST_PKG32_DRAFT_2026-01-29_0016
**Date:** 2026-01-29
**Prepared By:** Estimating Agent (Automated Pipeline)

---

## Decision Summary

This log records all decisions made during the estimating process where ambiguities, missing inputs, or default selections required agent discretion.

**Total Decisions:** 12 (D-3201 through D-3212)

---

## D-3201: Workspace Path Selection

**Decision:** Use default paths per AGENT_ESTIMATING defaults
**Trigger:** No explicit paths provided in conversation
**Evidence:**
- Execution root: `/Users/ryan/ai-env/projects/chirality-app/test/execution/`
- Decomposition: `/Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md`
- Estimates output: `/Users/ryan/ai-env/projects/chirality-app/test/execution/_Estimates/`
**Impacted WBS/CBS:** N/A (process)
**Estimate Impact:** None (process only)
**Override Path:** Provide explicit paths in conversation

---

## D-3202: Currency Selection

**Decision:** CAD (Canadian dollars)
**Trigger:** Default currency selection per config and project location
**Evidence:**
- Project location: Fraser Surrey Terminal, Surrey, BC (Canada)
- `_CONFIG.md` specifies CAD
- Consistent with all prior package estimates
**Impacted WBS/CBS:** All CBS buckets
**Estimate Impact:** Qualitative (currency basis)
**Override Path:** Update `_CONFIG.md` currency parameter

---

## D-3203: Pricing Date

**Decision:** January 2026
**Trigger:** Default to current month per pipeline rules
**Evidence:**
- Current date: 2026-01-29
- `_CONFIG.md` specifies 2026-01
- Consistent with recent package estimates
**Impacted WBS/CBS:** All CBS buckets
**Estimate Impact:** Qualitative (pricing basis date)
**Override Path:** Update `_CONFIG.md` pricing_date parameter

---

## D-3204: Estimate Label

**Decision:** PKG32_DRAFT
**Trigger:** Package-specific estimate label generation
**Evidence:** Consistent with established pattern (PKG00_DRAFT through PKG25_DRAFT)
**Impacted WBS/CBS:** N/A (metadata)
**Estimate Impact:** None (labeling only)
**Override Path:** Update `_CONFIG.md` estimate_label parameter

---

## D-3205: Scope Inclusions/Exclusions

**Decision:** Include Engineering (E), PM, Procurement (P), Materials (MAT), Construction Directs (CD), Construction Indirects (CI), Commissioning (COM); Exclude Owner's costs, land, financing, Employer-obtained permits
**Trigger:** Default scope per `_CONFIG.md` and decomposition boundaries
**Evidence:**
- `_CONFIG.md` include/exclude scopes
- Decomposition Section 1.2 (scope boundaries)
- DEL-32.01 Datasheet Conditions (Contractor-responsible permits only; Employer permits excluded)
**Impacted WBS/CBS:** All CBS buckets
**Estimate Impact:** Qualitative (scope boundary)
**Override Path:** Update `_CONFIG.md` or clarify Employer's Requirements permit responsibility matrix

---

## D-3206: Contingency Method

**Decision:** PCT_BY_BUCKET (percentage by CBS bucket with allowance-heavy adjustment)
**Trigger:** Default method per `_CONFIG.md`
**Evidence:** `_CONFIG.md` contingency_method = PCT_BY_BUCKET
**Impacted WBS/CBS:** Contingency (CONT)
**Estimate Impact:** Contingency allocation methodology
**Override Path:** Update `_CONFIG.md` to RISK_BASED if preferred

---

## D-3207: Escalation Mode

**Decision:** NONE (no escalation applied)
**Trigger:** Default per `_CONFIG.md`
**Evidence:** `_CONFIG.md` escalation_mode = NONE; pricing date = January 2026 (current)
**Impacted WBS/CBS:** N/A (escalation not applied)
**Estimate Impact:** None (escalation excluded)
**Override Path:** Update `_CONFIG.md` escalation_mode to EXPLICIT and provide escalation factors/schedule

---

## D-3208: Fallback Model Use

**Decision:** Use fallback typical model for all pricing (no project-specific quotes or rate tables available)
**Trigger:** No vendor quotes, budgetary quotes, or project rate tables found
**Evidence:**
- Source discovery (Source_Index.md) found no usable pricing sources
- Deliverable folders contain scope/requirements but no cost data
- No rate tables in `_Estimates/_RateTables/`
**Impacted WBS/CBS:** All CBS buckets
**Estimate Impact:** HIGH — 100% of estimate based on allowances and parametric factors (see Assumptions_Log.md)
**Confidence:** LOW
**Override Path:** Provide vendor quotes, budgetary pricing, or populate `_Estimates/_RateTables/` with project-specific rates

---

## D-3209: Indirects Factors

**Decision:** Apply fallback typical model factors:
- Procurement (P) = 2% × (MAT)
- Project Management (PM) = 6% × (E + MAT + CD + CI)
- Commissioning (COM) = 3% × (E + MAT + CD + CI)
**Trigger:** No project-specific indirects model available
**Evidence:** AGENT_ESTIMATING fallback model, lines 662-673
**Impacted WBS/CBS:** P, PM, COM
**Estimate Impact:** Moderate (indirects ~7-11% of directs in typical projects)
**Confidence:** MED (typical industry factors)
**Override Path:** Provide project-specific indirects models, time-phased resource plans, or overhead allocation basis

---

## D-3210: WBS to CBS Mapping

**Decision:** Map PKG-32 deliverables to CBS as follows:
- DEL-32.01 Permit Applications → Engineering (E)
- DEL-32.02 Permits → Project Management (PM)
- DEL-32.03-32.06 Compliance Records → Engineering (E), Construction Indirects (CI)
- DEL-32.07 Correspondence Register → Project Management (PM)
- DEL-32.08 Correspondence Copies → Project Management (PM)
**Trigger:** Deliverable types and descriptions indicate document/administrative work rather than physical construction
**Evidence:**
- Decomposition Section 5 PKG-32 (deliverable types: Document, Permit, Record, Document Package)
- Deliverable Datasheets and Specifications (document preparation, compliance tracking, QA/QC records)
- No physical materials, equipment, or field installation work identified
**Impacted WBS/CBS:** E, PM, CI
**Estimate Impact:** Qualitative (CBS allocation)
**Override Path:** Clarify deliverable CBS assignments in decomposition or provide CBS mapping guidance

---

## D-3211: Permit Fee Allocation

**Decision:** Include placeholder allowance for Contractor-responsible permit fees
**Trigger:** Permit fees likely required but specific fees unknown
**Evidence:**
- DEL-32.01 Specification FR-05 (permit applications submitted with fees)
- DEL-32.02 (permits result from applications)
- Specific permit types TBD (depends on Employer's Requirements and authority requirements)
- Specific fee schedules TBD (authority-dependent)
**Impacted WBS/CBS:** Materials (MAT) — using MAT bucket for fees/non-capital costs
**Estimate Impact:** Moderate (permit fees can range $5k-$50k+ depending on project size/complexity)
**Confidence:** LOW
**Assumption:** A-3208 (permit fees allowance)
**Override Path:** Provide Employer's Requirements permit list, authority fee schedules, or budgetary permit fee estimate

---

## D-3212: Consultant Support Allocation

**Decision:** Include allowance for regulatory/environmental consultant support
**Trigger:** Complex regulatory compliance typically requires specialist support
**Evidence:**
- DEL-32.01 Specification FR-03 (supporting documentation includes environmental assessments, hazard assessments)
- DEL-32.03-32.06 (compliance with VFPA, DFO, Transport Canada, Code requirements)
- Typical EPC projects engage regulatory/environmental consultants for permit applications and compliance
**Impacted WBS/CBS:** Engineering (E)
**Estimate Impact:** Moderate (consultant support typically 10-30% of internal engineering hours for regulatory packages)
**Confidence:** LOW
**Assumption:** A-3207 (consultant support allowance)
**Override Path:** Clarify consultant scope and provide budgetary quotes or engage consultants for preliminary budgets

---

## Decision Impact Summary

| Decision | Impact on Total | Confidence |
|----------|----------------|------------|
| D-3208 (Fallback model use) | HIGH (100% allowance-based) | LOW |
| D-3211 (Permit fees) | Moderate ($25k allowance) | LOW |
| D-3212 (Consultant support) | Moderate ($60k allowance) | LOW |
| D-3209 (Indirects factors) | Moderate (7-11% allocation) | MED |
| Others | Low/Qualitative | N/A |

---

**Prepared By:** Estimating Agent
**Date:** 2026-01-29 00:16
