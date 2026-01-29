# Decision Log — PKG-33 HSE Management

**Snapshot ID:** EST_PKG33_DRAFT_2026-01-29_1100
**Date:** 2026-01-29
**Package:** PKG-33 HSE Management

---

## Decision Log Purpose

This log documents all defaults, ambiguities, and choices made during the estimating process where human judgment or configuration was required but not explicitly provided.

Per AGENT_ESTIMATING protocol, every decision is recorded with:
- Decision ID (`D-###`)
- Decision statement (what was chosen)
- Trigger (why a choice was required)
- Evidence (file path/section if available) or "no evidence; default"
- Impacted WBS/CBS
- Estimate impact
- How to override in next run

---

## D-001: Package-Level Estimating Approach

**Decision:** Estimate PKG-33 as a standalone package; do not aggregate across all packages in single run.

**Trigger:** AGENT_ESTIMATING can estimate single packages or multiple packages; config must specify scope.

**Evidence:** `_CONFIG.md` note: "This is a phased estimating approach where each package is estimated separately."

**Impacted WBS/CBS:** All (scope definition)

**Estimate Impact:** Enables focused estimate per package; allows iterative refinement; cumulative totals tracked in `_LATEST.md`.

**Override:** To estimate multiple packages in one run, update `_CONFIG.md` with `include_scopes` list of package IDs.

---

## D-002: Currency Selection (CAD)

**Decision:** Use CAD (Canadian dollars) as the single currency for this estimate.

**Trigger:** Must select one currency; project location is Canada; no explicit currency specified in deliverable docs.

**Evidence:**
- Project location: Fraser Surrey Terminal, Surrey, BC (Decomposition Section 1)
- `_CONFIG.md` currency = CAD

**Impacted WBS/CBS:** All

**Estimate Impact:** All costs expressed in CAD; no currency conversion required.

**Override:** N/A (project location is Canadian; CAD is correct).

---

## D-003: Pricing Date (January 2026)

**Decision:** Use January 2026 as the pricing date ("dollars of" January 2026).

**Trigger:** No historical pricing dates found in deliverable documents; must establish pricing basis.

**Evidence:**
- `_CONFIG.md` pricing_date = 2026-01
- Current date: 2026-01-29

**Impacted WBS/CBS:** All

**Estimate Impact:** Costs represent January 2026 pricing; subject to escalation if project extends beyond 2026.

**Override:** If historical pricing data becomes available, update `_CONFIG.md` pricing_date to match source pricing date.

---

## D-004: Estimate Label

**Decision:** Use estimate label `PKG33_DRAFT` for this snapshot.

**Trigger:** Must label estimate for tracking and version control.

**Evidence:**
- `_CONFIG.md` pattern: `PKG##_DRAFT` for draft estimates
- Snapshot ID: EST_PKG33_DRAFT_2026-01-29_1100

**Impacted WBS/CBS:** N/A (labeling only)

**Estimate Impact:** None (metadata for tracking)

**Override:** Update `_CONFIG.md` estimate_label to change label for next run.

---

## D-005: Use Fallback Model (No Project-Specific Sources)

**Decision:** Apply fallback typical model for all pricing due to absence of vendor quotes and project rate tables.

**Trigger:** Source discovery (Phase 2.2) found no vendor quotes, no project rate tables, and no usable pricing data.

**Evidence:**
- Source_Index.md: 0% vendor quotes, 0% rate tables
- Deliverable folders not yet scaffolded
- AGENT_ESTIMATING fallback model (lines 623-691)

**Impacted WBS/CBS:** All (E, PM, P, CI, COM)

**Estimate Impact:**
- Base estimate: 100% allowance/parametric ($775k)
- Confidence: LOW to MED
- Maturity: Class 5 (Order of Magnitude)

**Override:**
- Provide HSE services quotes in workspace
- Create rate tables in `_Estimates/_RateTables/`
- Re-run estimating agent

---

## D-006: Indirects Model (Factor-Based)

**Decision:** Use factor-based indirects model (not time-based).

**Trigger:** No project schedule or detailed duration data available for HSE activities.

**Evidence:**
- No schedule discovered
- `_CONFIG.md` does not specify indirects model
- AGENT_ESTIMATING default: factor-based for conceptual estimates (lines 643-652)

**Impacted WBS/CBS:** PM, P, CI

**Estimate Impact:**
- PM: 6% of E base = $32.7k
- P: 2% of HSE services = $10.9k
- CI: 18% of notional construction allocation = $93.1k

**Override:**
- Provide project schedule with HSE activity durations
- Enable time-based indirects model in config
- Re-run with duration-based calculations

---

## D-007: Rounding Policy (Nearest $1,000)

**Decision:** Round all summary totals and final estimate to nearest $1,000 CAD.

**Trigger:** Must establish rounding policy appropriate for estimate maturity.

**Evidence:** `_CONFIG.md` rounding = 1000

**Impacted WBS/CBS:** All (presentation only; Detail.csv retains calculated precision)

**Estimate Impact:** Avoids false precision for conceptual estimate; $1,000 rounding appropriate for $1M range estimate.

**Override:** Update `_CONFIG.md` rounding parameter (e.g., 10000 for nearest $10k).

---

## D-008: Contingency Method (PCT_BY_BUCKET)

**Decision:** Use percentage-by-bucket contingency method with allowance-heavy adjustment.

**Trigger:** Must select contingency method; risk-based method not feasible without detailed scope and vendor data.

**Evidence:**
- `_CONFIG.md` contingency_method = PCT_BY_BUCKET
- AGENT_ESTIMATING fallback model contingency (lines 653-667)

**Impacted WBS/CBS:** All (contingency calculated per bucket)

**Estimate Impact:**
- Baseline rates: E/PM/P = 10%, CI = 20%, COM = 25%
- Allowance adjustments: +5% if allowance share ≥50%, +10% if ≥80%
- Blended contingency rate: ~24.4%
- Total contingency: $189k

**Override:**
- Set `contingency_method = RISK_BASED` in config
- Provide risk data and three-point estimates
- Re-run with probabilistic contingency

---

## D-009: Escalation (Not Applied)

**Decision:** Do not apply escalation (escalation_mode = NONE).

**Trigger:** Must decide whether to apply cost escalation over project duration.

**Evidence:**
- `_CONFIG.md` escalation_mode = NONE
- No project schedule or cashflow curve available
- HSE services are primarily labor (moderate escalation risk)

**Impacted WBS/CBS:** All (escalation not calculated)

**Estimate Impact:**
- Estimate represents January 2026 pricing
- Actual costs subject to escalation if project extends beyond 2026
- Escalation exposure: ~2-4% annually for labor = $15k-$31k per year on $775k base

**Override:**
- Set `escalation_mode = EXPLICIT` in config
- Provide schedule and escalation factors
- Re-run with escalation applied

---

## D-010: WBS to CBS Mapping (HSE Package)

**Decision:** Map PKG-33 deliverables to CBS buckets as follows:
- Plans (DEL-33.01, DEL-33.07): E + PM
- Assessments/Procedures (DEL-33.02, DEL-33.03, DEL-33.08): E
- Installation & Test Records (DEL-33.04, DEL-33.05, DEL-33.06): CI + COM

**Trigger:** Deliverable types do not map one-to-one to CBS categories; multi-CBS allocation required.

**Evidence:**
- Decomposition deliverable types (Plan, Assessment, Procedure, Record)
- Typical HSE cost breakdown: planning (E+PM), execution (CI), commissioning compliance (COM)

**Impacted WBS/CBS:** All PKG-33 deliverables

**Estimate Impact:** Ensures HSE costs distributed across appropriate CBS buckets for accurate contingency and indirects.

**Override:** If deliverable folders exist with detailed content, refine mapping based on actual scope per deliverable.

**Documented in:** WBS_CBS_Matrix.csv

---

## D-011: Commissioning Allocation (Environmental Compliance During Startup)

**Decision:** Allocate environmental compliance monitoring and CEMP/SPPP records to Commissioning (COM) bucket (25%) and Construction Indirects (CI) bucket (75%).

**Trigger:** Environmental monitoring and waste management span both construction and commissioning phases; must allocate across CBS.

**Evidence:**
- DEL-33.04 (CEMP Compliance), DEL-33.05 (SPPP), DEL-33.06 (Waste Management) described as "Installation & Test Records"
- Typical EPC convention: environmental compliance during construction = CI; during commissioning = COM

**Impacted WBS/CBS:** DEL-33.04, DEL-33.05, DEL-33.06 → CI + COM

**Estimate Impact:**
- CI allocation: $210k (environmental monitoring during construction)
- COM allocation: $70k (environmental compliance during commissioning/startup)

**Override:** If project schedule clarifies construction vs commissioning duration, adjust allocation ratios.

---

## Decision Summary Table

| Decision ID | Topic | Impact Level | Estimate Impact (CAD) |
|-------------|-------|--------------|----------------------|
| D-001 | Estimating approach | Medium | N/A (scope definition) |
| D-002 | Currency (CAD) | Low | N/A (no conversion) |
| D-003 | Pricing date (Jan 2026) | Low | N/A (basis date) |
| D-004 | Estimate label | Low | N/A (metadata) |
| D-005 | Fallback model | **HIGH** | $775k (100% of base) |
| D-006 | Indirects model | Medium | $137k (indirects total) |
| D-007 | Rounding policy | Low | <$1k (rounding) |
| D-008 | Contingency method | **HIGH** | $189k (contingency) |
| D-009 | Escalation (none) | Medium | ~$15-31k/year exposure |
| D-010 | WBS-CBS mapping | Medium | Affects contingency/indirects allocation |
| D-011 | COM allocation | Low-Medium | $70k COM; $210k CI |

**Total Decisions:** 11

---

**Decision Log Prepared By:** Estimating Agent (Phase 1-4)
**Date:** 2026-01-29
**Status:** Complete
