# Decision Log — PKG-08 Marine Structures Estimate

**Snapshot ID:** EST_PKG08_DRAFT_2026-01-28_2400
**Date:** 2026-01-28

---

## Purpose

This log records all decisions, defaults, and ambiguous interpretations made during the estimating process for PKG-08 Marine Structures. Each decision is assigned a unique ID (D-###) and is referenced from the Basis of Estimate (BOE) and/or line items in `Detail.csv`.

---

## D-801: Currency Selection

**Decision:** Use CAD (Canadian Dollars) as the currency for this estimate.

**Trigger:** Config parameter `currency` not overridden for PKG-08 specifically; default from `_CONFIG.md` applies.

**Evidence:** Project location is Fraser Surrey Terminal, Surrey, BC, Canada. Config file specifies CAD for prior packages (PKG-00 through PKG-04).

**Impacted WBS/CBS:** All line items (PKG-08)

**Estimate Impact:** Currency basis for all pricing; no currency conversion required.

**How to Override:** Edit `_CONFIG.md` or provide PKG-08-specific config override if different currency is required.

---

## D-802: Pricing Date and Escalation

**Decision:** Use January 2026 as pricing date; escalation_mode = NONE.

**Trigger:** No historical pricing sources found; config specifies escalation_mode = NONE.

**Evidence:** Config file `_CONFIG.md` line 10 specifies `pricing_date = 2026-01` and line 36 specifies `escalation_mode = NONE`.

**Impacted WBS/CBS:** All line items (PKG-08)

**Estimate Impact:** Pricing represents "January 2026 dollars"; no escalation applied to future expenditure.

**How to Override:** Update `_CONFIG.md` with `escalation_mode = EXPLICIT` and provide cashflow curve or escalation factors.

---

## D-803: Pricing Sources — No Quotes or Rate Tables

**Decision:** Proceed with 100% Allowance/Parametric pricing using Fallback Typical Model.

**Trigger:** Source discovery (Protocol Phase 2.2) found no vendor quotes, no rate tables in `_RateTables/`, and no historical project data.

**Evidence:**
- `_RateTables/` directory is empty
- No quotes found in deliverable `_REFERENCES.md` files or workspace
- Deliverables at INITIALIZED state with TBD content

**Impacted WBS/CBS:** All line items (PKG-08)

**Estimate Impact:** All pricing is allowance-based or parametric (factor-based). Confidence = LOW for all line items.

**How to Override:**
1. Obtain vendor budgetary quotes for marine piling, structural steel, and marine contractor services
2. Populate `_RateTables/` with unit rates for marine construction
3. Re-run estimating pipeline

---

## D-804: WBS → CBS Mapping

**Decision:** Map PKG-08 deliverables and physical scope to CBS buckets as follows:

| WBS Element | CBS Bucket | Rationale |
|-------------|------------|-----------|
| DEL-08.01 through DEL-08.11 | E (Engineering) | All deliverables are design/engineering outputs (drawings, calcs, specs, reports) |
| Marine piling supply | MAT (Materials) | Equipment/materials supply |
| Structural steel supply | MAT (Materials) | Equipment/materials supply |
| Abutment materials | MAT (Materials) | Concrete, rebar, formwork |
| Marine hardware | MAT (Materials) | Ladders, platforms, anodes |
| Marine logistics | FRT (Freight) | Barge mobilization, marine transport |
| Pile installation | CD (Construction Directs) | Field labor and equipment |
| Steel erection | CD (Construction Directs) | Field labor and equipment |
| Coatings, NDT | CD (Construction Directs) | Field labor and services |
| Supervision, safety, QA/QC | CI (Construction Indirects) | Field overhead and management |
| EPCM allocation | PM (Project Management) | Project-level management and coordination |
| Vendor coordination | P (Procurement) | Procurement services |
| Load testing, proving | COM (Commissioning) | Testing and acceptance |

**Trigger:** No explicit CBS mapping provided in decomposition or ER; agent must infer mapping based on deliverable types and marine scope.

**Evidence:** Standard EPC CBS structure; marine work typically split into MAT (supply), FRT (marine logistics), CD (installation), CI (supervision).

**Impacted WBS/CBS:** All PKG-08 line items

**Estimate Impact:** Determines which CBS bucket each line item rolls up to; affects contingency application and summary reporting.

**How to Override:** Provide explicit WBS-CBS mapping table in `_CONFIG.md` or decomposition.

---

## D-805: Quantity Takeoff Approach — No Explicit Quantities

**Decision:** Proceed with allowance line items (Qty=1, Unit=LS) sized using fallback model and industry-typical assumptions.

**Trigger:** All deliverables at INITIALIZED state; no explicit quantities in Datasheet.md or Specification.md files (all marked TBD).

**Evidence:**
- Reviewed all 11 deliverable folders under `PKG-08_Marine_Structures/1_Working/`
- All `Datasheet.md` files show TBD for quantities, dimensions, materials
- No design drawings or geotechnical reports available to support QTO

**Impacted WBS/CBS:** MAT, CD line items (piling, steel, installation)

**Estimate Impact:** All quantities are placeholders; actual quantities may vary significantly when design matures.

**How to Override:**
1. Complete marine geotechnical investigation (DEL-08.04) to confirm pile type, size, quantity
2. Develop preliminary design drawings (DEL-08.01) with trestle/platform geometry and steel tonnages
3. Re-run estimating pipeline with updated QTO

**Assumptions Created:** A-812 through A-825

---

## D-806: Allowance Sizing Method

**Decision:** Size allowances using:
1. Comparable engineering line items from PKG-01/PKG-02 estimates, scaled for marine complexity
2. Industry-typical unit rates for marine materials (piling, structural steel with marine-grade corrosion protection)
3. Marine construction rates reflecting specialized marine contractor requirements

**Trigger:** No project-specific pricing sources available; must size allowances to produce runnable estimate.

**Evidence:**
- Prior estimates (PKG-00, PKG-01, PKG-02) used allowance-based pricing successfully
- Marine piling: typical CAD $750-$1,100/tonne installed (including supply, delivery, driving)
- Marine structural steel: typical CAD $4,500-$5,500/tonne installed (including supply, delivery, erection, marine-grade coating)
- Engineering deliverables: scaled from prior packages based on complexity and number of deliverables

**Impacted WBS/CBS:** All ALLOWANCE line items (E, MAT, CD)

**Estimate Impact:** Allowance amounts are industry-typical placeholders; may vary ±50% based on actual project-specific conditions.

**How to Override:** Obtain project-specific vendor quotes or populate `_RateTables/` with verified unit rates.

---

## D-807: Indirects, Management, and Commissioning Factors

**Decision:** Apply Fallback Typical Model factors as follows:

| CBS Bucket | Factor | Base | Calculation |
|------------|--------|------|-------------|
| CI (Construction Indirects) | 18% | CD | $1,830k × 0.18 = $329.4k |
| PM (EPCM/Project Mgmt) | 6% | CD + CI + MAT + FRT | ($1,830k + $329.4k + $2,280k + $175k) × 0.06 = $276.9k |
| P (Procurement Services) | 2% | MAT + FRT | ($2,280k + $175k) × 0.02 = $49.1k |
| COM (Commissioning) | 3% | CD + CI + MAT | ($1,830k + $329.4k + $2,280k) × 0.03 = $133.2k |

**Trigger:** No project-specific indirects data or schedule-based models available.

**Evidence:** Fallback Typical Model (AGENT_ESTIMATING.md lines 666-673) provides default factors for marine/EPC work.

**Impacted WBS/CBS:** CI, PM, P, COM line items

**Estimate Impact:** Indirects and management represent 14.3% of base estimate; commissioning represents 2.4%.

**How to Override:**
1. Provide project-specific indirects model (time-based supervision, temporary facilities, HSE costs)
2. Provide schedule/duration data to support time-based indirects calculation
3. Update `_CONFIG.md` with custom factor overrides

**Justification for Marine Work:**
- 18% CI is appropriate for marine construction (enhanced supervision, marine safety, specialized QA/QC for welding/NDT, tide/weather coordination)
- 6% PM reflects marine engineering coordination across disciplines and interfaces
- 3% COM reflects structural load testing, proof testing, as-built survey requirements

---

## D-808: Contingency Method and Percentage

**Decision:** Apply 25% contingency to base estimate using `PCT_BY_BUCKET` method with allowance-heavy adjustment.

**Trigger:** Config specifies `contingency_method = PCT_BY_BUCKET`; estimate is 92.2% ALLOWANCE/PARAMETRIC.

**Evidence:**
- Fallback model (AGENT_ESTIMATING.md lines 677-690) specifies baseline contingency by CBS plus allowance-heavy adjustment
- Pre-conceptual design maturity (< 5%)
- 100% allowance/parametric pricing (no quotes or rate tables)
- Marine construction complexity and uncertainty

**Impacted WBS/CBS:** All CBS buckets

**Estimate Impact:** Contingency = $1,365,750 (25% of rounded base estimate $5,463,000)

**Contingency Breakdown by CBS:**
- E: 20% (baseline 10% + 10% allowance adjustment)
- MAT: 25% (baseline 15% + 10% allowance adjustment)
- FRT: 25% (baseline 15% + 10% allowance adjustment)
- CD: 30% (baseline 20% + 10% allowance adjustment)
- CI: 20% (baseline 20%; no adjustment for parametric)
- PM: 10% (baseline 10%; no adjustment for parametric)
- P: 10% (baseline 10%; no adjustment for parametric)
- COM: 25% (baseline 25%; no adjustment for parametric)

**How to Override:**
1. Switch to `contingency_method = RISK_BASED` in `_CONFIG.md` and provide risk register with quantified impacts
2. Provide explicit contingency % override in `_CONFIG.md`
3. Reduce allowance share by obtaining quotes/rate tables → lower contingency justified

**Rationale:**
- High contingency reflects pre-conceptual maturity and marine construction uncertainty
- Contingency will reduce as design matures and pricing sources improve

---

## Summary

| Decision ID | Topic | Impact |
|-------------|-------|--------|
| D-801 | Currency = CAD | All line items priced in CAD |
| D-802 | Pricing date = 2026-01, no escalation | January 2026 dollars basis |
| D-803 | No quotes/rate tables → 100% allowance/parametric | Low confidence, all pricing |
| D-804 | WBS → CBS mapping | Line item CBS assignment |
| D-805 | No explicit quantities → allowance line items | All quantities are placeholders |
| D-806 | Allowance sizing using industry-typical rates | All allowance amounts |
| D-807 | Indirects/PM/P/COM factors from fallback model | Parametric line items |
| D-808 | 25% contingency (PCT_BY_BUCKET, allowance-heavy) | Contingency amount |

---

**END OF DECISION LOG**
