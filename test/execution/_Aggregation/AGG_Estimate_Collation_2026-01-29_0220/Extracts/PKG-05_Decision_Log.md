# Decision Log — PKG-05 Concrete Structures Estimate

**Snapshot ID:** EST_PKG05_DRAFT_2026-01-28_2400
**Package Scope:** PKG-05 Concrete Structures
**Date:** 2026-01-28

---

## D-001: Estimate Scope — Package-Level Estimating

**Decision:** Create separate estimates by package rather than single project-wide estimate.

**Trigger:** Project instructions (INIT.md) specify phased work by package: "Progress one deliverable at a time until all deliverables in that package are complete. Only complete one package at a time."

**Evidence:** `/Users/ryan/ai-env/projects/chirality-app/INIT.md`, lines 3-11.

**Impacted WBS/CBS:** All packages (PKG-00 through PKG-35). This estimate covers PKG-05 only.

**Estimate Impact:** This estimate is a subset of the full project. Indirects, project management, and other cross-package costs are allocated proportionally to PKG-05.

**Override Path:** To create full project estimate, modify scope in `_CONFIG.md` to include all packages.

---

## D-002: Currency Selection — CAD

**Decision:** Use Canadian dollars (CAD) as the estimate currency.

**Trigger:** Default currency selection per AGENT_ESTIMATING protocol (Phase 1.3).

**Evidence:** Project location is Fraser Surrey Terminal, 11060 Elevator Road, Surrey, BC (decomposition Section 1, line 10). Canadian location indicates CAD currency.

**Impacted WBS/CBS:** All line items.

**Estimate Impact:** All costs expressed in CAD. No currency conversion required for Canadian vendors/rates.

**Override Path:** Set `currency` parameter in `_CONFIG.md` if different currency required.

---

## D-003: Pricing Date — January 2026

**Decision:** Use January 2026 as the pricing date ("dollars of" month).

**Trigger:** No explicit pricing date found in deliverable documents. Default to current date per AGENT_ESTIMATING protocol.

**Evidence:** Current date is 2026-01-28. No historical pricing dates referenced in deliverable `_REFERENCES.md` files.

**Impacted WBS/CBS:** All line items.

**Estimate Impact:** Costs represent January 2026 pricing. No escalation applied (escalation_mode = NONE per config).

**Override Path:** Set `pricing_date` parameter in `_CONFIG.md` if different pricing basis required.

---

## D-004: Workspace Paths — Default Paths Used

**Decision:** Use default workspace paths specified in AGENT_ESTIMATING instructions.

**Trigger:** Initialization Phase 1.1 — auto-discovery of project paths.

**Evidence:**
- Project workspace: `/Users/ryan/ai-env/projects/chirality-app/test/`
- Execution root: `/Users/ryan/ai-env/projects/chirality-app/test/execution/`
- Decomposition: `/Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md`
- Estimates output: `/Users/ryan/ai-env/projects/chirality-app/test/execution/_Estimates/`

All paths verified as accessible.

**Impacted WBS/CBS:** N/A (infrastructure decision).

**Estimate Impact:** None (path selection does not affect cost values).

**Override Path:** Paths can be overridden via conversation if project structure changes.

---

## D-005: Source Priority — No Project-Specific Pricing Sources Found

**Decision:** Use fallback typical model for pricing due to absence of project-specific quotes, budgets, or rate tables.

**Trigger:** Source discovery (Phase 2.2) found no vendor quotes, budgetary proposals, or project rate tables in deliverable `_REFERENCES.md` files or `_Estimates/_RateTables/` directory.

**Evidence:**
- All PKG-05 deliverable `_REFERENCES.md` files list only the decomposition document
- `_Estimates/_RateTables/` directory is empty
- No pricing documents discovered in PKG-05 deliverable folders

**Impacted WBS/CBS:** All CBS buckets.

**Estimate Impact:** HIGH — All line items will use fallback allowances or parametric models with LOW confidence ratings. Estimate totals will have wide uncertainty ranges.

**Override Path:** To improve estimate accuracy:
1. Add vendor quotes for concrete supply, rebar supply, formwork systems
2. Add rate tables (CSV, XLSX, or MD format) to `_Estimates/_RateTables/` directory
3. Re-run estimate pipeline

---

## D-006: Indirects Model — Factor-Based (No Schedule Data)

**Decision:** Apply indirects using factor-based model rather than time-based model.

**Trigger:** No construction schedule or duration data discovered in deliverable documents.

**Evidence:** Deliverable documents reference project duration assumptions but no detailed schedule or critical path was found.

**Impacted WBS/CBS:** Construction Indirects (CI), Project Management (PM).

**Estimate Impact:** Indirects calculated as factors of Construction Directs (CD) and Materials (MAT) using fallback typical model defaults.

**Override Path:** Provide detailed construction schedule to enable time-based indirects calculation (staffing levels × duration).

---

## D-007: Rounding Policy — Nearest $1,000

**Decision:** Round estimate totals to nearest $1,000 CAD.

**Trigger:** Default rounding policy per AGENT_ESTIMATING protocol and `_CONFIG.md` setting.

**Evidence:** `_CONFIG.md`, rounding = 1000.

**Impacted WBS/CBS:** Summary totals only (detail line items retain calculated precision).

**Estimate Impact:** Minimal — rounding affects presentation only, not line item accuracy.

**Override Path:** Modify `rounding` parameter in `_CONFIG.md` (e.g., 10000 for $10k rounding, 100 for $100 rounding).

---

## D-008: Contingency Method — Percentage by Bucket (PCT_BY_BUCKET)

**Decision:** Apply contingency using percentage-by-CBS-bucket method with allowance-heavy adjustment.

**Trigger:** Default contingency method per AGENT_ESTIMATING protocol and `_CONFIG.md` setting.

**Evidence:** `_CONFIG.md`, contingency_method = PCT_BY_BUCKET. Risk-based three-point estimation not feasible without vendor quotes and project-specific risk data.

**Impacted WBS/CBS:** All CBS buckets — contingency calculated separately for E, PM, P, MAT, CD, CI.

**Estimate Impact:** Contingency will be higher for buckets with high allowance share (due to low confidence in fallback pricing).

**Override Path:**
1. Set `contingency_method = RISK_BASED` in `_CONFIG.md` to enable three-point estimation
2. Provide vendor quotes and project-specific risk data to support risk-based model

---

## D-009: Escalation — Not Applied

**Decision:** Do not apply escalation to this estimate.

**Trigger:** Default escalation mode per AGENT_ESTIMATING protocol and `_CONFIG.md` setting (escalation_mode = NONE).

**Evidence:** No cashflow curve or expenditure schedule discovered. Pricing date (2026-01) represents current pricing; no forward escalation required for draft estimate.

**Impacted WBS/CBS:** All line items (escalation = 0%).

**Estimate Impact:** Estimate represents January 2026 dollars without adjustment for future price changes.

**Override Path:**
1. Set `escalation_mode = EXPLICIT` in `_CONFIG.md`
2. Provide construction schedule with cashflow curve to enable escalation calculation

---

## D-010: Concrete Quantity Basis — Parametric from Tank Parameters

**Decision:** Derive concrete quantities parametrically from known tank and facility parameters.

**Trigger:** No detailed quantity takeoffs available. Deliverables specify 3 × 15,000 MT tanks and 45,000 MT total storage but do not provide foundation/wall dimensions.

**Evidence:**
- Decomposition lines 41-42: Storage Capacity 45,000 MT (3 × 15,000 MT tanks)
- DEL-05.01 Datasheet: Tank foundation layouts, containment walls, equipment pads, thrust blocks
- No dimensioned drawings or QTO available

**Impacted WBS/CBS:** Materials (MAT), Construction Directs (CD) for concrete and rebar.

**Estimate Impact:** Concrete and rebar quantities are parametric estimates based on typical tank foundation/containment proportions. Uncertainty ±40%.

**Override Path:** Provide dimensioned drawings or QTO from DEL-05.01 development.

---

## D-011: Tank Foundation Type — Ring Wall Assumed

**Decision:** Assume ring wall foundations for the 15,000 MT storage tanks (most common for large API 650 tanks).

**Trigger:** Foundation type not specified in deliverables. DEL-05.03 references "Tank foundation calculations" and "Foundation sizing (diameter, thickness)" without specifying type.

**Evidence:** Typical industry practice for 15,000 MT API 650 tanks uses ring wall foundations on properly prepared subgrade. Geotechnical conditions assumed adequate (per PKG-02 earthworks).

**Impacted WBS/CBS:** Materials (MAT), Construction Directs (CD) for tank foundations.

**Estimate Impact:** Ring wall foundation is lower cost than full mat foundation. If mat foundations required (poor soils), costs could increase 50-100%.

**Override Path:** Confirm foundation type from DEL-05.03 design calculations once developed.

---

## Decision Summary Table

| Decision ID | Topic | Selection | Confidence | Impact Level |
|-------------|-------|-----------|------------|--------------|
| D-001 | Scope | PKG-05 only | HIGH | HIGH |
| D-002 | Currency | CAD | HIGH | MED |
| D-003 | Pricing Date | 2026-01 | MED | MED |
| D-004 | Paths | Defaults | HIGH | NONE |
| D-005 | Sources | Fallback model | LOW | HIGH |
| D-006 | Indirects | Factor-based | MED | MED |
| D-007 | Rounding | $1,000 | HIGH | LOW |
| D-008 | Contingency | PCT_BY_BUCKET | MED | MED |
| D-009 | Escalation | NONE | HIGH | LOW |
| D-010 | Quantities | Parametric | LOW | HIGH |
| D-011 | Tank Foundation | Ring wall | MED | MED |

---

**Total Decisions Recorded:** 11
