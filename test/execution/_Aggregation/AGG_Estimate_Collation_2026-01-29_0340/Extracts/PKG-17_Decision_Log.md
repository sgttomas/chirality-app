# Decision Log — PKG-17 Electrical Power Distribution

**Snapshot ID:** EST_PKG17_DRAFT_2026-01-28_0005
**Date:** 2026-01-28

---

This log records all decisions made during the estimating process where the agent had to choose between alternatives or apply defaults due to missing information.

---

## D-1701: Currency Selection

**Decision:** Use CAD (Canadian Dollars) for all pricing

**Trigger:** No explicit currency specified in deliverable documents (deliverable folders do not exist yet)

**Evidence:** Project location is Surrey, BC, Canada (per decomposition). Config file specifies CAD.

**Impacted WBS/CBS:** All packages and CBS buckets

**Estimate Impact:** N/A (all pricing converted to single currency)

**Override Path:** Update `_CONFIG.md` if different currency is required

---

## D-1702: Pricing Date

**Decision:** Use January 2026 as pricing date (current date)

**Trigger:** No historical pricing sources or vendor quotes available

**Evidence:** Config file specifies 2026-01 as pricing date

**Impacted WBS/CBS:** All packages and CBS buckets

**Estimate Impact:** No escalation applied (escalation_mode = NONE)

**Override Path:** Update `_CONFIG.md` to enable escalation if multi-year cash flow is required

---

## D-1703: Pricing Sources

**Decision:** Use 100% Fallback Typical Model (allowance/parametric pricing)

**Trigger:** No vendor quotes, rate tables, or historical data discovered for PKG-17

**Evidence:**
- No deliverable folders exist for PKG-17 (not yet scaffolded)
- No rate tables found in `_RateTables/` for electrical equipment
- No vendor quotes referenced in any available documents

**Impacted WBS/CBS:** All line items

**Estimate Impact:** All pricing is LOW confidence allowance-based

**Override Path:** Provide budgetary quotes for transformers, switchgear, MCCs; populate `_RateTables/electrical_equipment_rates.csv`

---

## D-1704: WBS to CBS Mapping

**Decision:** Map PKG-17 deliverables to CBS buckets as follows:
- DEL-17.01 through DEL-17.05 → E (Engineering)
- Electrical equipment → MAT (Materials)
- Equipment transport → FRT (Freight)
- Installation and testing → CD (Construction Directs)
- Supervision/QA → CI (Construction Indirects, parametric)
- Project management → PM (EPCM, parametric)
- Procurement coordination → P (Procurement, parametric)
- Commissioning support → COM (Commissioning, parametric)

**Trigger:** Standard WBS-to-CBS mapping required per estimating protocol

**Evidence:** Decomposition deliverable types and electrical discipline scope

**Impacted WBS/CBS:** All PKG-17 deliverables

**Estimate Impact:** Determines contingency rates and rollup structure

**Override Path:** Adjust WBS_CBS_Matrix.csv if alternative mapping is required

---

## D-1705: Quantity Takeoff (QTO) Approach

**Decision:** Proceed with allowance line items due to absence of explicit quantities

**Trigger:** No deliverable folders exist for PKG-17; no design drawings or load calculations available

**Evidence:** Decomposition provides only high-level scope description (MV/LV distribution, transformers, switchgear, MCC, panels, grounding, cable installation)

**Impacted WBS/CBS:** All MAT and CD line items

**Estimate Impact:** All material quantities and installation scope are assumptions

**Override Path:** Develop load calculations (DEL-17.03) and preliminary layout (DEL-17.01) to enable quantity-based estimating

---

## D-1706: Allowance Sizing Basis

**Decision:** Size allowances using industry-typical values for industrial electrical installations scaled to facility scope

**Trigger:** No project-specific pricing basis available

**Evidence:**
- Facility scale: 1M MT/annum throughput, 45,000 MT storage, 32 railcar stations
- Electrical loads anticipated from: pumps (PKG-15), storage tanks (PKG-13), railcar unloading (PKG-10), marine loading (PKG-11), building HVAC (PKG-22)
- Comparable industrial facility electrical systems

**Impacted WBS/CBS:** MAT and CD buckets

**Estimate Impact:** Material and labor allowances reflect industrial-scale electrical distribution system

**Override Path:** Obtain vendor budgetary quotes; conduct load study to refine equipment sizing

---

## D-1707: Contingency Method

**Decision:** Use `PCT_BY_BUCKET` method with allowance-based adjustments

**Trigger:** Config file specifies `contingency_method = PCT_BY_BUCKET`

**Evidence:** Config setting; 85.7% of base estimate is allowance/parametric pricing

**Impacted WBS/CBS:** All CBS buckets (contingency applied by bucket)

**Estimate Impact:** Total contingency = 25% average ($896k on $3,554k base)

**Override Path:** Update `_CONFIG.md` to use RISK_BASED method if probabilistic approach is preferred

---

## D-1708: Indirects and Management Factors

**Decision:** Apply default factors from Fallback Typical Model:
- CI (Construction Indirects) = 18% of CD
- PM (EPCM) = 6% of (CD + CI + MAT + FRT)
- P (Procurement) = 2% of (MAT + FRT)
- COM (Commissioning) = 3% of (CD + CI + MAT)

**Trigger:** No project-specific indirects basis or schedule-based estimate available

**Evidence:** Fallback Typical Model defaults per AGENT_ESTIMATING.md lines 666-673

**Impacted WBS/CBS:** CI, PM, P, COM buckets

**Estimate Impact:** Parametric indirects total $509k (14.3% of base estimate)

**Override Path:** Provide project-specific indirects rates or schedule-based resource loading; update `_CONFIG.md` with custom factors

---

**Total Decisions:** 8 (D-1701 through D-1708)

---

**END OF DECISION LOG**
