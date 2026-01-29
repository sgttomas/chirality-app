# Decision Log — PKG-30 Commissioning Estimate

**Snapshot ID:** EST_PKG30_DRAFT_2026-01-29_0014
**Date:** 2026-01-29

This log records all decisions made during the estimating process where choices, defaults, or interpretations were required.

---

## D-001: Currency Selection

**Decision:** Use CAD (Canadian dollars) as the estimate currency

**Trigger:** No explicit currency specified in source documents

**Evidence:**
- Project location: Fraser Surrey Terminal, Surrey, BC (Canada)
- _CONFIG.md specifies CAD for all previous package estimates
- Employer: DP World Fraser Surrey Inc. (Canadian entity)

**Impacted WBS/CBS:** All

**Estimate Impact:** N/A (establishes currency basis)

**How to Override:** Specify alternative currency in _CONFIG.md

**Source:** _CONFIG.md; Decomposition §1.1 (Location)

---

## D-002: Pricing Date

**Decision:** Use January 2026 as pricing date (current date)

**Trigger:** No historical pricing date specified

**Evidence:**
- Current date: 2026-01-29
- No escalation mode enabled (_CONFIG.md: escalation_mode = NONE)
- Represents current market pricing

**Impacted WBS/CBS:** All

**Estimate Impact:** Establishes baseline pricing date; no escalation applied

**How to Override:** Specify pricing_date in _CONFIG.md or enable escalation_mode

**Source:** _CONFIG.md

---

## D-003: Rounding Policy

**Decision:** Round to nearest $1,000 for line items, $10,000 for totals

**Trigger:** Standard rounding policy required

**Evidence:** _CONFIG.md specifies rounding = 1000

**Impacted WBS/CBS:** All

**Estimate Impact:** Minimal (rounding differences < 0.1%)

**How to Override:** Modify rounding parameter in _CONFIG.md

**Source:** _CONFIG.md

---

## D-005: Scope Exclusions

**Decision:** Exclude Owner's costs, Employer-obtained permits, other packages, taxes, escalation

**Trigger:** Standard exclusions per project estimating framework

**Evidence:**
- _CONFIG.md specifies standard exclusions
- Decomposition §1.2 (Scope Focus) defines Contractor vs Employer responsibilities
- Decomposition §7 (Decisions Captured) clarifies responsibility splits

**Impacted WBS/CBS:** All (defines estimate boundary)

**Estimate Impact:** Excludes items not in Contractor scope

**How to Override:** Modify exclude_scopes in _CONFIG.md

**Source:** _CONFIG.md; Decomposition §1.2, §7

---

## D-008: Pricing Method Hierarchy

**Decision:** Apply pricing hierarchy: Vendor quotes (0%) → Rate tables (15%) → Allowances (72%) → Parametric (13%)

**Trigger:** No vendor quotes available; limited rate table data; detailed scope TBD

**Evidence:**
- No vendor quotes for commissioning support available in source files
- Commissioning labor rates available from typical BC market rates
- Commissioning procedures and detailed scope not yet developed (DEL-30.01, DEL-30.02 in INITIALIZED state)
- Consumables quantities TBD

**Impacted WBS/CBS:** All CBS categories; highest impact on CD, MAT, E

**Estimate Impact:** High reliance on allowances (72%) → LOW confidence estimate

**How to Override:** Provide vendor quotes for commissioning support; develop detailed commissioning procedures and plan

**Source:** Source_Index.md; deliverable _STATUS.md files (INITIALIZED state)

---

## D-009: Engineering Scope Pricing Method

**Decision:** Price commissioning procedure and plan development as ALLOWANCE

**Trigger:** Detailed procedure scope not yet defined (DEL-30.01 in INITIALIZED state)

**Evidence:**
- DEL-30.01 Datasheet lists anticipated artifacts but not detailed content
- Typical commissioning procedures: 30-40 hours development per procedure
- ~30 procedures estimated (pre-commissioning, system commissioning, start-up)

**Impacted WBS/CBS:** E (Engineering)

**Estimate Impact:** $385k engineering costs (100% allowance)

**How to Override:** Develop detailed procedure outlines in DEL-30.01; obtain vendor input on procedure requirements

**Source:** DEL-30.01 Datasheet §Construction; typical procedure development effort

---

## D-010: Project Management Allocation

**Decision:** Allocate PM at 6% of (CD + CI + MAT) using parametric method

**Trigger:** No detailed PM scope breakdown available

**Evidence:**
- Fallback typical model: PM = 0.06 × (CD + CI + MAT) for coordination-intensive projects
- Commissioning requires extensive coordination (construction, operations, regulatory, vendors)
- 30-week commissioning duration

**Impacted WBS/CBS:** PM (Project Management)

**Estimate Impact:** $210k PM costs

**How to Override:** Provide detailed PM resource plan; specify PM FTE and rates

**Source:** AGENT_ESTIMATING fallback model; project complexity assessment

---

## D-011: Procurement Services Allocation

**Decision:** Allocate Procurement services at 2% of MAT using parametric method

**Trigger:** No detailed procurement scope breakdown available

**Evidence:**
- Fallback typical model: P = 0.02 × MAT for procurement coordination
- Test equipment and consumables procurement relatively straightforward
- Limited vendor equipment procurement required

**Impacted WBS/CBS:** P (Procurement)

**Estimate Impact:** $52k procurement costs

**How to Override:** Provide detailed procurement resource plan

**Source:** AGENT_ESTIMATING fallback model

---

## D-012: Commissioning Duration Assumptions

**Decision:** Assume 30-week (~7.5 month) total commissioning duration with phased breakdown

**Trigger:** No construction schedule or system handover dates available

**Evidence:**
- Facility scale: 32 railcar stations, 3 tanks, marine loading, extensive I&C systems
- Typical commissioning durations for similar liquid bulk terminals: 6-9 months
- Terminal continuity constraints (OBJ-5) extend duration by ~20%
- Phased approach: Pre-commissioning (8 wks), system commissioning (12 wks), IST (6 wks), start-up (4 wks)

**Impacted WBS/CBS:** CD, CI (commissioning labor duration); PM, P (support duration)

**Estimate Impact:** $2.8M commissioning labor costs; duration is primary cost driver

**How to Override:** Provide integrated construction/commissioning schedule with system handover dates

**Source:** Decomposition §1.1 (facility scale); DEL-30.02 Guidance.md (phased commissioning strategy); typical industry durations

---

## D-014: Commissioning Labor Rates

**Decision:** Use fully burdened commissioning labor rates: Manager $135/hr, Leads $115/hr, Technicians $85/hr

**Trigger:** No project-specific labor rates available

**Evidence:**
- BC industrial labor market rates for 2026
- Fully burdened rates include base wage, benefits, statutory costs, travel, per diem, contractor markup
- Fraser Surrey location (Lower Mainland BC)
- Rates consistent with previous package estimates

**Impacted WBS/CBS:** CD (commissioning labor)

**Estimate Impact:** $1.77M commissioning team labor costs

**How to Override:** Provide project-specific commissioning labor rates or collective agreement rates

**Source:** BC labor market research 2026; previous package estimate rates

---

## D-015: Construction Indirects Allocation

**Decision:** Allocate CI using hybrid approach: field supervision (explicit), other indirects (parametric ~18% of CD)

**Trigger:** No detailed CI scope breakdown available

**Evidence:**
- Field supervision: 1 supervisor for 30 weeks (explicit allocation)
- HSE, QA/QC, site overhead, temp facilities: parametric allocation ~18% of CD
- Fallback typical model: CI = 0.18 × CD for industrial projects with HSE and QA/QC requirements

**Impacted WBS/CBS:** CI (Construction Indirects)

**Estimate Impact:** $505k CI costs

**How to Override:** Provide detailed CI resource plan and site overhead budget

**Source:** AGENT_ESTIMATING fallback model; project HSE and QA/QC requirements

---

## D-018: Contingency Method

**Decision:** Use PCT_BY_BUCKET contingency method with allowance-heavy adjustment

**Trigger:** _CONFIG.md specifies contingency_method = PCT_BY_BUCKET

**Evidence:**
- Baseline contingency by CBS: E (20%), PM (15%), P (15%), MAT (25%), CD (28%), CI (28%), COM (30%)
- Allowance-heavy adjustment: CD, CI, COM buckets >80% allowance → +5% contingency added
- Reflects high scope uncertainty (procedures not developed, durations TBD, vendor support TBD)

**Impacted WBS/CBS:** All CBS categories

**Estimate Impact:** $1.21M total contingency (26% blended rate)

**How to Override:** Specify alternative contingency method in _CONFIG.md or provide detailed risk-based contingency

**Source:** _CONFIG.md; AGENT_ESTIMATING fallback model; allowance share analysis

---

## D-020: Estimate Class Determination

**Decision:** Classify estimate as Class 5 (Conceptual / Order of Magnitude)

**Trigger:** Estimate maturity assessment required

**Evidence:**
- Scope definition level: Decomposition and deliverable datasheets only; detailed procedures TBD
- Pricing sources: 0% vendor quotes, 72% allowances
- Engineering maturity: Deliverables in INITIALIZED state (not yet SEMANTIC_READY or IN_PROGRESS)
- AACE RP 18R-97: Class 5 = 0-2% engineering complete, accuracy -30% to +50%

**Impacted WBS/CBS:** All (estimate classification)

**Estimate Impact:** Defines estimate accuracy range and use limitations

**How to Override:** Develop detailed commissioning procedures and plan; obtain vendor quotes; advance deliverables to IN_PROGRESS state

**Source:** AACE International RP 18R-97 (Cost Estimate Classification System); deliverable _STATUS.md files

---

## D-022: WBS-to-CBS Mapping for Commissioning Deliverables

**Decision:** Map commissioning deliverables to CBS categories based on deliverable type and content

**Trigger:** WBS-CBS mapping required for cost allocation

**Evidence:**
- DEL-30.01 (Procedures), DEL-30.02 (Plan) → E (Engineering / planning activities)
- DEL-30.03, DEL-30.04 (Pre-commissioning, Commissioning records) → CD (field commissioning execution)
- DEL-30.05, DEL-30.06 (IST, Performance testing) → COM (integrated commissioning / testing)
- DEL-30.07 (Punch lists) → CD (defect rectification)
- DEL-30.08 (CP commissioning) → CD (specialized commissioning)

**Impacted WBS/CBS:** E, CD, COM

**Estimate Impact:** Distributes costs appropriately across CBS buckets

**How to Override:** Provide alternative WBS-CBS mapping in _CONFIG.md

**Source:** Decomposition §5 PKG-30 deliverable descriptions; deliverable Datasheets (Type attribute)

---

## D-025: Estimate Use and Limitations

**Decision:** Classify estimate as DRAFT with WARNINGS status; suitable for budgeting only, not for commitments

**Trigger:** QA checks identify high allowance share and scope gaps

**Evidence:**
- 72% allowance/parametric pricing
- Commissioning procedures not yet developed
- System handover schedule unknown
- Vendor commissioning requirements TBD
- Performance test criteria not defined

**Impacted WBS/CBS:** All (estimate use classification)

**Estimate Impact:** Limits estimate use to budgeting and conceptual planning; not suitable for cost control baseline

**How to Override:** Develop detailed scope; obtain vendor quotes; mature estimate to Class 4 or Class 3

**Source:** QA_Report.md; BOE.md §11 (Limitations and Use)

---

**Total Decisions:** 15 (D-001 through D-025; selected key decisions shown)

**Decision Impact Summary:**
- High-impact decisions: D-012 (duration), D-014 (labor rates), D-018 (contingency) — drive 80% of estimate value
- Medium-impact decisions: D-008 (pricing hierarchy), D-020 (estimate class) — affect estimate confidence
- Low-impact decisions: D-001 (currency), D-003 (rounding) — administrative

---

**End of Decision Log**
