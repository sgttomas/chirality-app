# Decision Log — PKG-22 Building Interior & MEP

**Snapshot ID:** EST_PKG22_DRAFT_2026-01-28_2358
**Package:** PKG-22 Building Interior & MEP
**Date:** 2026-01-28

---

## Purpose

This document records all decisions made during the estimating process, including defaults, ambiguities, and mapping choices.

---

## Decision Entries

### D-001: Workspace Paths

**Decision:** Use default workspace paths per AGENT_ESTIMATING

**Trigger:** No explicit paths provided in conversation

**Evidence:**
- Execution root: `/Users/ryan/ai-env/projects/chirality-app/test/execution/`
- Decomposition: `/Users/ryan/ai-env/projects/chirality-app/test/Canola_Oil_Transload_Facility_Decomposition_REVISED_v2.md`
- Estimates write zone: `/Users/ryan/ai-env/projects/chirality-app/test/execution/_Estimates/`

**Impacted WBS/CBS:** All

**Estimate Impact:** None (path selection only)

**How to Override:** Provide explicit paths in conversation or update AGENT_ESTIMATING defaults

---

### D-002: Currency Selection

**Decision:** CAD (Canadian dollars)

**Trigger:** Config override in `_CONFIG.md`

**Evidence:**
- `_CONFIG.md` line 9: `currency | CAD | Canadian dollars (project location: Surrey, BC)`
- Project location: Fraser Surrey Terminal, Surrey, BC (Decomposition Section 1)

**Impacted WBS/CBS:** All

**Estimate Impact:** All values in CAD; no currency conversion required

**How to Override:** Update `_CONFIG.md` currency parameter

---

### D-003: Pricing Date

**Decision:** January 2026 (2026-01)

**Trigger:** Config override in `_CONFIG.md`

**Evidence:**
- `_CONFIG.md` line 10: `pricing_date | 2026-01 | January 2026 (current date)`
- Today's date: 2026-01-28

**Impacted WBS/CBS:** All

**Estimate Impact:** Current pricing basis; no historical adjustment; escalation exposure noted in Risk_Register.md

**How to Override:** Update `_CONFIG.md` pricing_date parameter

---

### D-004: Estimate Label

**Decision:** PKG22_DRAFT

**Trigger:** Sequential package estimating approach; update _CONFIG.md for PKG-22

**Evidence:**
- Previous package: PKG20_DRAFT
- Next package per sequence: PKG-22 Building Interior & MEP

**Impacted WBS/CBS:** All (label only)

**Estimate Impact:** None (labeling only)

**How to Override:** Update `_CONFIG.md` estimate_label parameter

---

### D-005: Scope Inclusions/Exclusions

**Decision:** Include E, PM, P, MAT, CD, CI, COM; exclude Owner's costs, land, financing, Employer-obtained permits

**Trigger:** Config override in `_CONFIG.md`

**Evidence:**
- `_CONFIG.md` lines 16-29 (scope settings)
- Decomposition Section 1.2: "This decomposition covers the Contractor's scope of work only"

**Impacted WBS/CBS:** All

**Estimate Impact:** Estimate covers Contractor D&B scope only

**How to Override:** Update `_CONFIG.md` include_scopes/exclude_scopes

---

### D-006: Indirects Model Selection

**Decision:** Factor-based indirects (CI, P, PM, COM calculated as % of directs/materials)

**Trigger:** No construction schedule available; conceptual estimate maturity

**Evidence:**
- No schedule found in workspace
- Deliverables in INITIALIZED state (no execution plan)
- Fallback model supports factor-based indirects (AGENT_ESTIMATING lines 643-652)

**Impacted WBS/CBS:** CI, P, PM, COM

**Estimate Impact:** $391k total indirects/services (19% of MAT+CD base)

**How to Override:** Provide construction schedule and time-based resource loading plan

---

### D-007: Rounding Policy

**Decision:** Nearest $1,000 CAD

**Trigger:** Config override in `_CONFIG.md`

**Evidence:**
- `_CONFIG.md` line 12: `rounding | 1000 | Round to nearest $1,000`

**Impacted WBS/CBS:** Summary totals only (Detail.csv retains calculated precision)

**Estimate Impact:** Minimal (rounding applied to final summary totals only)

**How to Override:** Update `_CONFIG.md` rounding parameter

---

### D-008: Pricing Method (No Quotes/Rates Available)

**Decision:** Use 100% allowance-based pricing for directs and materials; fallback model for indirects

**Trigger:** No vendor quotes or rate tables found (see Source_Index.md)

**Evidence:**
- Source search completed: 0 vendor quotes, 0 rate tables (Source_Index.md Phase 1-2)
- All deliverables in INITIALIZED state with TBD quantities
- Fallback model available per AGENT_ESTIMATING lines 623-691

**Impacted WBS/CBS:** E, MAT, CD (directs); CI, P, PM, COM (parametric factors)

**Estimate Impact:** 100% allowance/parametric pricing; confidence LOW; high contingency required

**How to Override:** Provide vendor quotes, develop rate tables, complete design quantities

---

### D-009: Indirects Factors Applied

**Decision:** Apply fallback typical factors: CI=18%, P=2%, PM=6%, COM=3%

**Trigger:** Factor-based indirects model selected (D-006); no project-specific factors available

**Evidence:**
- Fallback model factors (AGENT_ESTIMATING lines 643-652)
- Factors typical for industrial facility construction in BC Lower Mainland

**Impacted WBS/CBS:** CI, P, PM, COM

**Estimate Impact:**
- CI = 18% × CD ($632k) = $114k
- P = 2% × MAT ($675k) = $14k
- PM = 6% × (CD+CI+MAT) ($1,421k) = $85k
- COM = 3% × (CD+CI+MAT) ($1,421k) = $43k

**How to Override:** Update `_CONFIG.md` with project-specific factors or provide time-based resource plan

---

### D-010: Contingency Method

**Decision:** PCT_BY_BUCKET with allowance-heavy adjustment

**Trigger:** Config override in `_CONFIG.md`; 100% allowance-based pricing

**Evidence:**
- `_CONFIG.md` line 35: `contingency_method | PCT_BY_BUCKET`
- AllowanceShare = 100% for E, MAT, CD buckets
- Fallback model contingency baseline (AGENT_ESTIMATING lines 653-667)

**Impacted WBS/CBS:** All (contingency by CBS bucket)

**Estimate Impact:** Elevated contingency rates (20-30%) due to pricing uncertainty and scope uncertainty

**How to Override:** Update `_CONFIG.md` contingency_method; provide vendor quotes to reduce AllowanceShare

---

### D-011: WBS to CBS Mapping (MEP Deliverables)

**Decision:** Map PKG-22 deliverables to CBS as follows:
- Design deliverables (DEL-22.01 through DEL-22.04, DEL-22.06) → Engineering (E)
- Physical materials (HVAC equipment, plumbing materials, fire suppression components, electrical fixtures, interior finishes) → Materials (MAT)
- Installation work (HVAC installation, plumbing installation, fire sprinkler installation, interior electrical, finishes installation) → Construction Directs (CD)
- QA/QC records (DEL-22.05) → Construction Indirects (CI) / Commissioning (COM)

**Trigger:** Standard WBS→CBS mapping required per estimating protocol

**Evidence:**
- Deliverable types from Decomposition: Drawing, Specification, Calculation, Data Sheet, Record, Drawing Set
- Package discipline: Buildings (MEP specialty)
- Scope keywords: HVAC, plumbing, fire suppression, electrical, finishes

**Impacted WBS/CBS:** E, MAT, CD, CI, COM

**Estimate Impact:** Mapping determines CBS bucket allocation for all line items

**How to Override:** Provide explicit WBS-CBS mapping table or update estimating protocol

---

### D-012: Building Size Assumption

**Decision:** Assume 300 m² (3,230 SF) MCC building as baseline for MEP system sizing

**Trigger:** No building size available from PKG-21 deliverables (INITIALIZED state)

**Evidence:**
- Decomposition project parameters: 1,000,000 MT/a throughput; 32 railcar unloading stations; marine loading controls
- Typical industrial MCC building range: 200-400 m² (2,150-4,300 SF)
- 300 m² is mid-range estimate suitable for conceptual budgeting

**Impacted WBS/CBS:** All MEP line items (HVAC, plumbing, fire suppression, electrical, finishes)

**Estimate Impact:** Significant; building size drives HVAC capacity, plumbing fixture counts, sprinkler head counts, electrical load, finishes quantities

**How to Override:** Complete DEL-21.01 building design drawings or provide building floor area in conversation

**Cross-reference:** A-022 (building size assumption)

---

### D-013: Interior Finishes Scope Interpretation

**Decision:** Include basic industrial interior finishes (flooring, wall finishes, ceilings) in PKG-22 scope

**Trigger:** Decomposition PKG-22 scope states "Interior finishes" but does not detail extent

**Evidence:**
- PKG-22 scope (Decomposition line 525): "Interior finishes, HVAC, plumbing, building electrical distribution, fire suppression"
- Building type: MCC building (industrial occupancy)
- Typical industrial finish levels: sealed concrete floors or epoxy; painted drywall or metal panels; exposed or suspended acoustic ceiling

**Impacted WBS/CBS:** MAT, CD

**Estimate Impact:** $120k allowance for finishes (materials + installation)

**How to Override:** Complete DEL-21.01/DEL-22.01 building design drawings with finish schedules or clarify finish requirements in conversation

**Cross-reference:** A-021 (interior finishes allowance)

---

## Decision Summary

| Decision ID | Topic | Impact Level | Override Path |
|-------------|-------|--------------|---------------|
| D-001 | Workspace paths | Low | Provide explicit paths |
| D-002 | Currency (CAD) | Medium | Update _CONFIG.md |
| D-003 | Pricing date (2026-01) | Medium | Update _CONFIG.md |
| D-004 | Estimate label | Low | Update _CONFIG.md |
| D-005 | Scope inclusions/exclusions | High | Update _CONFIG.md |
| D-006 | Factor-based indirects | High | Provide schedule or override factors |
| D-007 | Rounding ($1,000) | Low | Update _CONFIG.md |
| D-008 | Use allowances (no quotes/rates) | High | Provide vendor quotes or rate tables |
| D-009 | Indirects factors (18/2/6/3%) | High | Update _CONFIG.md or provide resource plan |
| D-010 | PCT_BY_BUCKET contingency | High | Update _CONFIG.md or provide risk model |
| D-011 | WBS-CBS mapping | Medium | Provide explicit mapping table |
| D-012 | Building size (300 m²) | High | Provide PKG-21 building drawings or floor area |
| D-013 | Interior finishes scope | Medium | Clarify finish requirements or provide finish schedule |

---

**Total Decisions:** 13

**Decision Log Prepared By:** Estimating Agent
**Date:** 2026-01-28
**Snapshot:** EST_PKG22_DRAFT_2026-01-28_2358
**Status:** Complete
