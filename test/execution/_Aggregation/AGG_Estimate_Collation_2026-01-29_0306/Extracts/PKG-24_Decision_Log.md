# Decision Log — PKG-24 Security Systems Estimate

**Snapshot ID:** EST_PKG24_DRAFT_2026-01-28_0030
**Date:** 2026-01-28

This log documents decisions made during the straight-through estimating pipeline for PKG-24 Security Systems.

---

## D-001: Workspace Paths (Auto-Discovery)

**Decision:** Use default workspace paths from AGENT_ESTIMATING configuration
**Trigger:** No explicit paths provided by user in conversation
**Evidence:** Default paths in AGENT_ESTIMATING (lines 12-21)
**Impact:** Low — standard project paths
**Override Method:** Provide explicit paths in conversation or update _CONFIG.md

---

## D-002: Currency Selection

**Decision:** CAD (Canadian dollars)
**Trigger:** Project location Surrey, BC, Canada
**Evidence:**
- Decomposition Section 1 — Location: Fraser Surrey Terminal, Surrey, BC
- `_CONFIG.md` line 9 — currency: CAD
**Impact:** All line items priced in CAD
**Override Method:** Update _CONFIG.md currency parameter

---

## D-003: Pricing Date

**Decision:** 2026-01 (January 2026 dollars)
**Trigger:** Current date for pricing basis
**Evidence:** Current date 2026-01-28; no historical pricing date specified
**Impact:** Pricing reflects current market conditions (January 2026)
**Override Method:** Update _CONFIG.md pricing_date parameter

---

## D-004: Escalation Mode

**Decision:** NONE (no escalation applied)
**Trigger:** No construction schedule available for escalation calculation
**Evidence:**
- `_CONFIG.md` line 36 — escalation_mode: NONE
- No project schedule available in workspace
**Impact:** Estimate is in current (January 2026) dollars; does not reflect future price escalation over project duration
**Impacted WBS:** All
**Exposure:** 3-6% annual escalation over 2-3 year project = potential $50k-$157k addition (see Risk R-008)
**Override Method:** Provide construction schedule and set escalation_mode=EXPLICIT in _CONFIG.md

---

## D-005: Scope Inclusions/Exclusions

**Decision:** Include EPC scope (E, PM, P, MAT, CD, CI, COM); exclude Owner's costs, land, financing, Employer-obtained permits
**Trigger:** Standard D&B contractor scope definition
**Evidence:**
- Decomposition Section 1.2 — Contractor scope only
- `_CONFIG.md` lines 23-29 — include/exclude scopes
**Impact:** Estimate covers contractor-responsible scope only
**Override Method:** Update _CONFIG.md include_scopes and exclude_scopes

---

## D-006: WBS to CBS Mapping

**Decision:** Map PKG-24 deliverables to CBS buckets as follows:
- DEL-24.01, DEL-24.02, DEL-24.03, DEL-24.04 (design/engineering support) → E
- Equipment and materials (cameras, NVR, VMS, access control, network, cabling) → MAT
- Installation work (mounting, cable pulling, configuration, testing) → CD
- Field management and QA/QC → CI
- Vendor coordination and submittals → P
- Project oversight and Terminal coordination → PM
- Integrated testing and handover → COM

**Trigger:** Deliverable types and content analysis
**Evidence:**
- DEL-24.01, DEL-24.02 Specification.md — Drawing and Specification deliverable types
- DEL-24.03 Datasheet.md — Equipment submittals
- DEL-24.04 Datasheet.md — Installation and test records
**Impact:** Determines which CBS bucket each cost element is assigned to
**Impacted WBS:** All DEL-24.XX deliverables
**Override Method:** Manually revise WBS_CBS_Matrix.csv

---

## D-007: Rounding Policy

**Decision:** Round to nearest $1,000 CAD for summary totals
**Trigger:** Standard rounding policy from _CONFIG.md
**Evidence:** `_CONFIG.md` line 12 — rounding: 1000
**Impact:** Summary totals rounded; Detail.csv retains calculated precision
**Override Method:** Update _CONFIG.md rounding parameter

---

## D-008: Pricing Method (Fallback Model)

**Decision:** Use fallback typical model (allowances + parametric factors) for all line items
**Trigger:** No vendor quotes or rate tables found in workspace
**Evidence:**
- Source_Index.md — no pricing sources discovered
- Deliverable documents (DEL-24.01 through DEL-24.04) contain no pricing data
**Impact:** 100% of line items priced using allowances or parametric factors; LOW confidence
**Impacted WBS:** All
**Override Method:** Provide vendor quotes or rate tables in `_RateTables/` folder and re-run estimate

---

## D-009: Indirects Model (Factor-Based)

**Decision:** Use factor-based indirects model with following factors:
- CI = 18% × CD
- P = 2% × MAT
- PM = 6% × (CD + CI + MAT)
- COM = 3% × (CD + CI + MAT)

**Trigger:** No construction schedule or time-based indirects model available
**Evidence:**
- AGENT_ESTIMATING fallback model (lines 643-652)
- No construction schedule in workspace
**Impact:** Indirects calculated as percentage of directs/materials; suitable for conceptual estimate
**Impacted CBS:** CI, P, PM, COM
**Override Method:** Provide construction schedule and duration-based indirects data

---

## D-010: Contingency Method and Rates

**Decision:** PCT_BY_BUCKET method with allowance-heavy adjustments
- E: 20% (10% baseline + 10% allowance adjustment)
- MAT: 25% (15% baseline + 10% allowance adjustment)
- CD: 30% (20% baseline + 10% allowance adjustment)
- CI: 30% (20% baseline + 10% allowance adjustment)
- P: 15% (10% baseline + 5% allowance adjustment)
- PM: 15% (10% baseline + 5% allowance adjustment)
- COM: 30% (25% baseline + 5% allowance adjustment)

**Trigger:** 100% allowance-based pricing requires elevated contingency rates
**Evidence:**
- AGENT_ESTIMATING contingency model (lines 653-667)
- All MAT/CD line items priced by ALLOWANCE method (no quotes)
- All CI/P/PM/COM line items priced by PARAMETRIC method
**Impact:** 26% blended contingency rate ($213k on $833k base)
**Impacted CBS:** All
**Rationale:**
- No vendor quotes (pricing uncertainty)
- Quantities based on engineering judgment (scope uncertainty)
- Terminal integration complexity per DEC-05 (execution risk)
- Coastal marine environment (equipment specification risk)
**Override Method:** Provide vendor quotes and design quantities to reduce allowance percentage; update contingency rates accordingly

---

## D-011: Terminal Integration Scope per DEC-05

**Decision:** Treat CCTV and access control as separate system interfaces with Terminal security network per DEC-05
**Trigger:** Decomposition Section 7, DEC-05 — "Terminal network interfaces treated as multiple distinct systems"
**Evidence:**
- Decomposition DEC-05 (line 805)
- DEL-24.01 Datasheet.md — Integration Points section references DEC-05
- DEL-24.02 Specification.md — Terminal integration requirements per DEC-05
**Impact:**
- VMS software allowance includes Terminal CCTV integration capability
- Access control software allowance includes Terminal access control integration capability
- Network equipment sized for segregated VLANs
- Commissioning includes separate integration testing for CCTV and access control
**Impacted WBS:** DEL-24.01, DEL-24.03, DEL-24.04
**Impacted CBS:** MAT (software), CD (installation), COM (commissioning)
**Override Method:** Obtain Terminal integration specification and adjust software/commissioning allowances

---

**Decision Log Complete**
**Total Decisions:** 11
**Prepared By:** Estimating Agent
**Date:** 2026-01-28
