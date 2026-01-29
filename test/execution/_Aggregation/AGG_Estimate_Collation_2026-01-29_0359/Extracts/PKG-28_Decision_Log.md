# Decision Log — PKG-28 Design Verification Estimate

**Snapshot ID:** EST_PKG28_DRAFT_2026-01-29_0830
**Package Scope:** PKG-28 Design Verification
**Date:** 2026-01-29

---

## D-001: Estimate Scope — Package-Level Estimating

**Decision:** Create separate estimates by package rather than single project-wide estimate.

**Trigger:** Project instructions (INIT.md) specify phased work by package: "Progress one deliverable at a time until all deliverables in that package are complete. Only complete one package at a time."

**Evidence:** `/Users/ryan/ai-env/projects/chirality-app/INIT.md`, lines 3-11.

**Impacted WBS/CBS:** All packages (PKG-00 through PKG-35). This estimate covers PKG-28 only.

**Estimate Impact:** This estimate is a subset of the full project. Indirects, project management, and other cross-package costs are allocated proportionally to PKG-28.

**Override Path:** To create full project estimate, modify scope in `_CONFIG.md` to include all packages.

---

## D-002: Currency Selection — CAD

**Decision:** Use Canadian dollars (CAD) as the estimate currency.

**Trigger:** Default currency selection per AGENT_ESTIMATING protocol (Phase 1.3).

**Evidence:** Project location is Fraser Surrey Terminal, 11060 Elevator Road, Surrey, BC (decomposition Section 1, line 10). Canadian location indicates CAD currency.

**Impacted WBS/CBS:** All line items.

**Estimate Impact:** All costs expressed in CAD. No currency conversion required for Canadian engineering service providers.

**Override Path:** Set `currency` parameter in `_CONFIG.md` if different currency required.

---

## D-003: Pricing Date — January 2026

**Decision:** Use January 2026 as the pricing date ("dollars of" month).

**Trigger:** No explicit pricing date found in deliverable documents. Default to current date per AGENT_ESTIMATING protocol.

**Evidence:** Current date is 2026-01-29. No historical pricing dates referenced in deliverable documents.

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

**Trigger:** Source discovery (Phase 2.2) found no vendor quotes, budgetary proposals, or project rate tables for design verification services.

**Evidence:**
- No IDV service provider quotes available
- No VFPA coordination cost data available
- `_Estimates/_RateTables/` directory does not contain design verification rates
- No pricing documents discovered in PKG-28 deliverable folders

**Impacted WBS/CBS:** All CBS buckets.

**Estimate Impact:** HIGH — All line items will use fallback allowances with LOW confidence ratings. Estimate totals will have wide uncertainty ranges.

**Override Path:** To improve estimate accuracy:
1. Obtain budgetary quotes from independent design verification service providers
2. Add engineering review rate tables to `_Estimates/_RateTables/` directory
3. Re-run estimate pipeline

---

## D-006: Indirects Model — Factor-Based (No Schedule Data)

**Decision:** Apply indirects using factor-based model rather than time-based model.

**Trigger:** No design verification schedule or duration data discovered in deliverable documents.

**Evidence:** Decomposition specifies design submission stages (30/60/90/IFC) but does not provide detailed design schedule durations or IDV review windows.

**Impacted WBS/CBS:** Construction Indirects (CI), Project Management (PM), Procurement (P).

**Estimate Impact:** Indirects calculated as factors of Engineering (E) base using fallback typical model defaults.

**Override Path:** Provide detailed design schedule to enable time-based indirects calculation.

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

**Impacted WBS/CBS:** All CBS buckets — contingency calculated separately for E, PM, P, CI.

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
2. Provide design schedule with cashflow curve to enable escalation calculation

---

## D-010: IDV Scope Assumption — 8 Disciplines x 4 Stages

**Decision:** Assume IDV reviews required for 8 major disciplines across 4 submission stages (30%, 60%, 90%, IFC).

**Trigger:** IDV scope not explicitly defined in decomposition; typical design-build practice applied.

**Evidence:**
- Project has 36 packages across 14 disciplines (decomposition Section 8.1)
- Typical IDV focuses on: Civil, Structural, Marine, Process, Mechanical, Electrical, I&C, Specialty
- Standard submission stages: 30%, 60%, 90%, IFC per ER typical requirements

**Impacted WBS/CBS:** Engineering (E) — DEL-28.01

**Estimate Impact:** IDV allowance ($350k) sized based on 32 reviews (8 disciplines x 4 stages) at $10-12k per review average.

**Override Path:** Clarify specific IDV requirements with Employer or independent reviewer; adjust discipline count and review depth as needed.

---

## D-011: VFPA IP Review Scope — 4-6 Submission Cycles

**Decision:** Assume 4-6 major VFPA IP review submission cycles requiring formal responses.

**Trigger:** VFPA IP review requirements not explicitly defined in decomposition; typical port authority review practice applied.

**Evidence:**
- Project is located at Vancouver Fraser Port Authority jurisdiction
- VFPA typically requires project permit review with formal submission/response cycles
- Typical cycles align with design milestones (conceptual, preliminary, detailed, IFC)

**Impacted WBS/CBS:** Engineering (E) + PM — DEL-28.02

**Estimate Impact:** VFPA IP review allowance ($95k technical + $42k coordination) sized based on 4-6 cycles at $15-25k per cycle.

**Override Path:** Clarify VFPA project review requirements and expected submission count; adjust cycle count and complexity as needed.

---

## Decision Summary Table

| Decision ID | Topic | Selection | Confidence | Impact Level |
|-------------|-------|-----------|------------|--------------|
| D-001 | Scope | PKG-28 only | HIGH | HIGH |
| D-002 | Currency | CAD | HIGH | MED |
| D-003 | Pricing Date | 2026-01 | MED | MED |
| D-004 | Paths | Defaults | HIGH | NONE |
| D-005 | Sources | Fallback model | LOW | HIGH |
| D-006 | Indirects | Factor-based | MED | MED |
| D-007 | Rounding | $1,000 | HIGH | LOW |
| D-008 | Contingency | PCT_BY_BUCKET | MED | MED |
| D-009 | Escalation | NONE | HIGH | LOW |
| D-010 | IDV Scope | 8 disciplines x 4 stages | MED | HIGH |
| D-011 | VFPA Scope | 4-6 submission cycles | MED | MED |

---

**Total Decisions Recorded:** 11
