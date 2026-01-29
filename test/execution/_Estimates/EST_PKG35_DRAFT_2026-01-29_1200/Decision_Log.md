# Decision Log — PKG-35 Training & Handover Estimate

**Snapshot ID:** EST_PKG35_DRAFT_2026-01-29_1200
**Package:** PKG-35 Training & Handover
**Date:** 2026-01-29

---

## Decision Register

| D-ID | Decision | Trigger | Evidence | Impacted WBS/CBS | Estimate Impact | Override Path |
|------|----------|---------|----------|------------------|-----------------|---------------|
| D-001 | Package-level estimating approach (PKG-35 only) | Project phased estimating strategy | `_CONFIG.md`, `_LATEST.md` | All | Enables incremental project estimate | Include additional packages in scope |
| D-002 | Currency = CAD | Project location in Canada | Decomposition Section 1.1 (Surrey, BC) | All | All costs in CAD | Set `currency` in `_CONFIG.md` |
| D-003 | Pricing date = January 2026 | No explicit pricing date in documents | Current date (2026-01-29) | All | Baseline for escalation | Set `pricing_date` in `_CONFIG.md` |
| D-004 | Inclusions/exclusions per standard EPC scope | No explicit scope definition in PKG-35 docs | AGENT_ESTIMATING defaults, Decomposition | All | Standard scope boundaries | Define in `_CONFIG.md` |
| D-005 | Use fallback model for pricing (no quotes/rates available) | Source discovery found no pricing sources | Source_Index.md | All allowances | 85.5% of base priced by allowance | Provide rate tables, vendor quotes |
| D-006 | Factor-based indirects model | No schedule/duration data available | AGENT_ESTIMATING defaults | CI, P, PM factors | $214k in calculated indirects | Provide project schedule, duration |
| D-007 | Rounding = nearest $1,000 | Config default | `_CONFIG.md` | All totals | Display precision | Set `rounding` in `_CONFIG.md` |
| D-008 | Contingency method = PCT_BY_BUCKET | No risk model data available | AGENT_ESTIMATING defaults | All | 25.0% blended contingency | Set `contingency_method` in `_CONFIG.md` |
| D-009 | Escalation = NONE | Draft estimate maturity | `_CONFIG.md` default | All | No escalation applied | Set `escalation_mode = EXPLICIT` |
| D-010 | Defects liability period = 12 months | No contract terms available | Industry typical (D&B contracts) | DEL-35.05, PM | $165k defects liability support | Confirm contract terms |
| D-011 | Training population = 30-50 personnel | No staffing plan available | Industry typical for terminal | DEL-35.01, DEL-35.02, COM | Training delivery scope | Confirm Employer staffing plan |

---

## Decision Details

### D-001: Package-Level Estimating Approach

**Decision:** Estimate PKG-35 Training & Handover as a standalone package estimate, consistent with project phased estimating strategy.

**Trigger:** Project uses incremental package-by-package estimating approach per `_CONFIG.md` and `_LATEST.md`.

**Evidence:**
- `_CONFIG.md` defines phased estimating with packages estimated separately
- `_LATEST.md` shows 24+ packages already estimated

**Impacted WBS/CBS:** All PKG-35 line items

**Estimate Impact:** Enables incremental project estimate development; interfaces with other packages estimated separately.

**Override Path:** Change estimating strategy in `_CONFIG.md` to estimate multiple packages together.

---

### D-002: Currency Selection (CAD)

**Decision:** Use Canadian dollars (CAD) as the estimate currency.

**Trigger:** Currency selection required for estimate.

**Evidence:**
- Project location is Fraser Surrey Terminal, Surrey, BC (Canada)
- Decomposition Section 1.1 confirms Canadian location
- Previous package estimates use CAD

**Impacted WBS/CBS:** All line items

**Estimate Impact:** All costs expressed in CAD; no currency conversion required.

**Override Path:** Set `currency` parameter in `_CONFIG.md` if USD or other currency preferred.

---

### D-003: Pricing Date (January 2026)

**Decision:** Use January 2026 as the pricing date ("dollars of" January 2026).

**Trigger:** No explicit pricing date found in deliverable documents.

**Evidence:**
- No historical pricing references in PKG-35 deliverable documents
- Current date is 2026-01-29
- Consistent with previous package estimates

**Impacted WBS/CBS:** All line items

**Estimate Impact:** Baseline for any future escalation calculations.

**Override Path:** Set `pricing_date` parameter in `_CONFIG.md` if different date required.

---

### D-004: Inclusions/Exclusions Scope

**Decision:** Include standard EPC scope (E, PM, P, CD, CI, COM) and exclude Owner's costs, taxes, and escalation.

**Trigger:** No explicit scope definition in PKG-35 deliverable documents.

**Evidence:**
- AGENT_ESTIMATING default inclusions/exclusions
- Decomposition Section 1.2 (Contractor scope boundary)
- Consistent with previous package estimates

**Impacted WBS/CBS:** All CBS categories

**Estimate Impact:** Standard D&B contractor cost scope; Owner's costs excluded.

**Override Path:** Define specific inclusions/exclusions in `_CONFIG.md`.

---

### D-005: Use Fallback Model for Pricing

**Decision:** Use fallback typical model for all pricing (allowances and parametric factors) due to absence of project-specific pricing sources.

**Trigger:** Source discovery found no vendor quotes, budgetary proposals, or project rate tables.

**Evidence:**
- Source_Index.md documents source discovery findings
- No pricing files found in workspace
- Deliverable documents contain no cost data

**Impacted WBS/CBS:** All allowance line items (85.5% of base)

**Estimate Impact:** All pricing based on typical industry allowances; confidence = LOW.

**Override Path:** Provide vendor quotes for training services, OEM training rates, site reinstatement costs; add rate tables to `_Estimates/_RateTables/`.

---

### D-006: Factor-Based Indirects Model

**Decision:** Use factor-based model for construction indirects, procurement services, and PM allocation.

**Trigger:** No project schedule or duration data available for time-based calculation.

**Evidence:**
- No schedule found in deliverable documents
- AGENT_ESTIMATING defaults for factor-based model
- Consistent with previous package estimates

**Impacted WBS/CBS:** CI ($134k), P ($17k), PM factors

**Estimate Impact:** $214k in calculated indirects (14.5% of base).

**Override Path:** Provide project schedule and duration estimates for time-based calculation.

---

### D-007: Rounding Policy

**Decision:** Round to nearest $1,000 CAD for summary totals.

**Trigger:** Config default.

**Evidence:**
- `_CONFIG.md` specifies `rounding = 1000`
- Appropriate for Class 5 estimate in $1M-$2M range

**Impacted WBS/CBS:** All summary totals

**Estimate Impact:** Display precision for totals.

**Override Path:** Set `rounding` parameter in `_CONFIG.md`.

---

### D-008: Contingency Method (PCT_BY_BUCKET)

**Decision:** Apply contingency using percentage-by-bucket method with allowance-heavy adjustments.

**Trigger:** No risk model data available for risk-based contingency.

**Evidence:**
- No project risk register or risk analysis available
- AGENT_ESTIMATING fallback model contingency method
- Consistent with previous package estimates

**Impacted WBS/CBS:** All CBS categories

**Estimate Impact:** 25.0% blended contingency ($369k).

**Override Path:** Set `contingency_method = RISK_BASED` in `_CONFIG.md` and provide risk data.

---

### D-009: Escalation Not Applied

**Decision:** Do not apply escalation adjustment to estimate.

**Trigger:** Draft estimate maturity; escalation_mode = NONE per config.

**Evidence:**
- `_CONFIG.md` specifies `escalation_mode = NONE`
- Class 5 estimate maturity does not warrant escalation precision
- Consistent with previous package estimates

**Impacted WBS/CBS:** All line items

**Estimate Impact:** No escalation adjustment; estimate represents January 2026 pricing.

**Override Path:** Set `escalation_mode = EXPLICIT` in `_CONFIG.md` and provide escalation factors.

---

### D-010: Defects Liability Period (12 Months)

**Decision:** Assume 12-month defects liability period for costing defects liability support.

**Trigger:** No contract terms available in workspace.

**Evidence:**
- Industry typical for Design & Build contracts (12 months from Taking Over)
- DEL-35.05 Datasheet references "TBD" for defects liability period
- No contract document available

**Impacted WBS/CBS:** DEL-35.05, PM (defects liability management)

**Estimate Impact:** $165k allowance for 12-month defects liability support.

**Override Path:** Confirm contract terms and adjust defects liability support scope.

---

### D-011: Training Population (30-50 Personnel)

**Decision:** Assume training population of 30-50 personnel for costing training delivery.

**Trigger:** No Employer staffing plan available.

**Evidence:**
- Industry typical for terminal operations (console operators, field operators, maintenance, HSE)
- DEL-35.02 Datasheet lists assumed training population categories
- No Employer staffing plan in workspace

**Impacted WBS/CBS:** DEL-35.01, DEL-35.02, COM

**Estimate Impact:** Training delivery scope and duration based on 30-50 trainees.

**Override Path:** Confirm Employer staffing plan and adjust training scope accordingly.

---

## Decision Summary

| Category | Count |
|----------|-------|
| Scope decisions | 2 |
| Pricing basis decisions | 3 |
| Methodology decisions | 4 |
| Assumption-driven decisions | 2 |
| **Total** | **11** |

---

**Decision Log Prepared By:** Estimating Agent
**Date:** 2026-01-29
**Snapshot:** EST_PKG35_DRAFT_2026-01-29_1200
