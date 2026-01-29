# Decision Log — PKG-25 Communications & IT

**Snapshot ID:** EST_PKG25_DRAFT_2026-01-29_0004
**Package:** PKG-25 Communications & IT
**Date:** 2026-01-29

---

## Purpose

This log documents decisions made during estimate preparation where ambiguity existed or defaults were applied. Each decision is traceable and includes guidance for overriding in future estimate runs.

---

## D-2501: Workspace Paths

**Decision:** Use default paths from AGENT_ESTIMATING configuration
**Trigger:** No explicit paths provided in conversation
**Evidence:** Project Instance Paths (defaults) section in AGENT_ESTIMATING.md
**Impacted WBS/CBS:** All
**Estimate Impact:** Enables estimate execution
**Override:** Provide explicit paths in conversation or via command-line arguments

**Paths Used:**
- Decomposition: `/Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md`
- Execution root: `/Users/ryan/ai-env/projects/chirality-app/test/execution/`
- Estimates output: `/Users/ryan/ai-env/projects/chirality-app/test/execution/_Estimates/`

---

## D-2502: Currency Selection

**Decision:** CAD (Canadian dollars)
**Trigger:** No explicit currency specified; project location is Surrey, BC
**Evidence:** Project location (Decomposition Section 1.1); _CONFIG.md currency=CAD
**Impacted WBS/CBS:** All (all costs in CAD)
**Estimate Impact:** All line items priced in CAD
**Override:** Update `_CONFIG.md` currency field or provide explicit currency in conversation

**Rationale:** Project location in British Columbia, Canada; Vancouver/Lower Mainland labor market uses CAD pricing

---

## D-2503: Pricing Date

**Decision:** January 2026 (2026-01)
**Trigger:** No explicit pricing date specified
**Evidence:** Current date (2026-01-29); _CONFIG.md pricing_date=2026-01
**Impacted WBS/CBS:** All
**Estimate Impact:** Baseline for escalation calculations (if escalation enabled)
**Override:** Update `_CONFIG.md` pricing_date field

---

## D-2504: Estimate Label

**Decision:** PKG25_DRAFT
**Trigger:** Package-specific estimate
**Evidence:** _CONFIG.md estimate_label updated for PKG-25
**Impacted WBS/CBS:** N/A (metadata only)
**Estimate Impact:** Snapshot folder naming and identification
**Override:** Update `_CONFIG.md` estimate_label field before next run

---

## D-2505: Scope Inclusions/Exclusions

**Decision:** Include E, PM, P, MAT, CD, CI, COM; exclude Owner's costs, land, financing, permits, other packages
**Trigger:** Standard EPC scope for D&B contract
**Evidence:** _CONFIG.md scope settings; Decomposition Section 1.2; DEC-05 (PKG-24 separation)
**Impacted WBS/CBS:** All CBS buckets
**Estimate Impact:** Defines which CBS buckets are populated
**Override:** Update `_CONFIG.md` include_scopes and exclude_scopes lists

**Specific Exclusions for PKG-25:**
- CCTV network (PKG-24 Security Systems per DEC-05)
- Access control network (PKG-24 Security Systems per DEC-05)
- Control system networks/fieldbus (PKG-19 Control Systems) — integration points only
- Cable pathways/trays (PKG-17 Electrical, PKG-21 Buildings) — coordination required

**Source:** DEL-25.01 Specification.md Scope §Exclusions; Decomposition Section 7 DEC-05

---

## D-2506: Indirects Method

**Decision:** Factor-based indirects model
**Trigger:** No construction schedule available
**Evidence:** No schedule file found in workspace; fallback model appropriate for Class 5 estimate
**Impacted WBS/CBS:** CI, P, PM, COM
**Estimate Impact:** Indirects = $83.7k (CI $29k, P $7k, PM $32k, COM $16k)
**Override:** Provide construction schedule for time-based indirects model; or update `_CONFIG.md` with custom factors

**Factors Applied:**
- CI = 18% × CD
- P = 2% × MAT
- PM = 6% × (CD + CI + MAT)
- COM = 3% × (CD + CI + MAT)

**Source:** AGENT_ESTIMATING fallback model lines 643-652

---

## D-2507: Rounding Policy

**Decision:** Round to nearest $1,000 CAD
**Trigger:** Standard rounding for Class 5 estimate
**Evidence:** _CONFIG.md rounding=1000
**Impacted WBS/CBS:** Summary totals only
**Estimate Impact:** Summary totals rounded; Detail.csv retains calculated precision
**Override:** Update `_CONFIG.md` rounding field

---

## D-2508: Contingency Method

**Decision:** PCT_BY_BUCKET with allowance-heavy adjustment
**Trigger:** No risk-based data available; high allowance share
**Evidence:** _CONFIG.md contingency_method=PCT_BY_BUCKET; 82% allowance pricing
**Impacted WBS/CBS:** All (contingency applied to each bucket)
**Estimate Impact:** Total contingency = $169k (30% blended); rounded to $160k
**Override:** Update `_CONFIG.md` contingency_method=RISK_BASED; or provide risk register with quantified impacts

**Baseline Contingency Rates (before adjustment):**
- E: 10% → 20% (+10% for 100% allowance)
- MAT: 15% → 25% (+10% for 100% allowance)
- CD: 20% → 30% (+10% for 100% allowance)
- CI, COM: 25% → 30% (+5% for factor-derived from allowance base)
- P, PM: 10% → 15% (+5% for factor-derived from allowance base)

**Source:** AGENT_ESTIMATING contingency model lines 653-691

---

## D-2509: Escalation Mode

**Decision:** NONE (no escalation applied)
**Trigger:** No project schedule available for escalation curve
**Evidence:** _CONFIG.md escalation_mode=NONE; no schedule file found
**Impacted WBS/CBS:** All (escalation = $0)
**Estimate Impact:** Estimate is in January 2026 dollars; no escalation to mid-point of construction
**Override:** Update `_CONFIG.md` escalation_mode=EXPLICIT and provide project schedule/cash flow curve

**Risk:** Escalation exposure 3-6% annually over 2-3 years = potential $34k-$100k addition (see Risk R-2508)

---

## D-2510: WBS to CBS Mapping

**Decision:** Map deliverables to CBS as follows:
- DEL-25.01, DEL-25.02, DEL-25.03 → E (Engineering)
- DEL-25.04 → CI/COM (QA/QC records)
- Fiber cabling materials → MAT
- Copper cabling materials → MAT
- Network switches, patch panels → MAT
- Cable installation, termination, testing → CD
- Field indirects → CI
- Procurement services → P
- Project management → PM
- Commissioning and integration testing → COM

**Trigger:** Standard CBS structure for telecommunications systems
**Evidence:** Deliverable types and descriptions from Decomposition Table PKG-25
**Impacted WBS/CBS:** All deliverables and CBS buckets
**Estimate Impact:** Determines line item CBS assignments and contingency rates
**Override:** Provide custom WBS-CBS mapping in `_CONFIG.md` or external mapping file

**Source:** WBS_CBS_Matrix.csv; Decomposition Section 5 PKG-25

---

## D-2511: Pricing Source Priority

**Decision:** Use fallback allowance model (no quotes or rate tables available)
**Trigger:** No vendor quotes found; no rate tables in `_RateTables/`
**Evidence:** Source discovery found zero pricing sources
**Impacted WBS/CBS:** All MAT, CD line items (100% allowance/parametric pricing)
**Estimate Impact:** Base estimate = $563k; 82% allowance-based; Confidence = LOW
**Override:** Provide vendor quotes in workspace; populate `_RateTables/` with unit rates; re-run estimate

**Source Hierarchy Attempted:**
1. Vendor quotes → 0 found
2. Rate tables → 0 found
3. Allowances → Applied (A-2501 through A-2518)
4. Parametric factors → Applied (indirects)

**Source:** Source_Index.md; AGENT_ESTIMATING pricing hierarchy (lines 261-291)

---

## D-2512: Network Architecture Assumptions

**Decision:** Assume typical enterprise network architecture in absence of design
**Trigger:** Network architecture not defined; no DEL-25.01 design drawings available
**Evidence:** Deliverables in INITIALIZED status; design quantities TBD per deliverable Datasheets
**Impacted WBS/CBS:** MAT (switches, cabling), CD (installation scope)
**Estimate Impact:** Equipment and cabling allowances sized for typical facility (~4-8 switches, 50-100 data drops)
**Override:** Complete DEL-25.01 network design; define port count matrix; update equipment schedules

**Assumptions:**
- 4-8 network switches (24-48 ports each) — A-2503
- 50-100 workstation/device data drops — implied in A-2502
- Single equipment room (ER) + 2-4 telecommunications rooms (TRs) — A-2515
- Fiber backbone between buildings — A-2501
- Structured copper cabling within buildings — A-2502

**Validation Path:** Complete network architecture study; coordinate with PKG-21 building layouts and PKG-22 equipment room design

---

## Summary

**Total Decisions:** 12
**Decisions with Material Cost Impact:** 6 (D-2506, D-2508, D-2509, D-2510, D-2511, D-2512)
**Decisions Requiring Human Override for Next Run:** 4 (D-2508, D-2509, D-2511, D-2512)

**Recommended Actions:**
1. Obtain vendor quotes for network equipment and cabling (overrides D-2511)
2. Complete network architecture design (resolves D-2512)
3. Provide project schedule for time-based indirects and escalation (overrides D-2506, D-2509)
4. Validate scope exclusions with Employer's Requirements when available (confirms D-2505)

---

**Decision Log Prepared By:** Estimating Agent
**Date:** 2026-01-29
**Status:** Complete
