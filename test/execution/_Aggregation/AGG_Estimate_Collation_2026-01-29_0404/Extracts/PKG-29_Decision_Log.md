# Decision Log — PKG-29 Testing

**Snapshot ID:** EST_PKG29_DRAFT_2026-01-29_0100
**Package:** PKG-29 Testing
**Date:** 2026-01-29

---

## Summary

| Decision ID | Decision | Impact |
|-------------|----------|--------|
| D-001 | Currency = CAD | All pricing in Canadian dollars |
| D-002 | Pricing date = 2026-01 | January 2026 dollars; no escalation |
| D-003 | Estimate label = PKG29_DRAFT | Identifies snapshot version |
| D-004 | Rounding = nearest $1,000 | Applied to summary totals |
| D-005 | Exclusions per _CONFIG.md | Owner costs, financing, taxes excluded |
| D-006 | Indirects model = factor-based | No schedule; use factors |
| D-007 | Escalation mode = NONE | Current pricing; no time-based adjustment |
| D-008 | Contingency method = PCT_BY_BUCKET | Allowance-heavy adjustment applied |
| D-009 | Indirects factors = CI 18%, P 2%, PM 6%, COM 3% | Per fallback typical model |
| D-010 | WBS-CBS mapping per deliverable type | Procedures->E; Records->CD/CI; Equipment->MAT |
| D-011 | Hydrotest water disposal = 50/50 split | 50% discharge permit, 50% haul-off |
| D-012 | FAT scope = major equipment only | 8-12 major FATs; minor equipment excluded |

---

## Decision Details

### D-001: Currency Selection

**Decision:** Use CAD (Canadian dollars) for all pricing

**Trigger:** No currency specified in deliverables; project location is Surrey, BC

**Evidence:** Project location Fraser Surrey Terminal, BC; Employer DP World Fraser Surrey Inc.

**Impacted WBS/CBS:** All line items

**Estimate Impact:** None (baseline currency)

**Override:** Set `currency` in `_CONFIG.md`

---

### D-002: Pricing Date

**Decision:** Use January 2026 as pricing date (2026-01)

**Trigger:** No explicit pricing date in deliverables

**Evidence:** Current date is 2026-01-29; use current month

**Impacted WBS/CBS:** All line items

**Estimate Impact:** None (baseline date)

**Override:** Set `pricing_date` in `_CONFIG.md`

---

### D-003: Estimate Label

**Decision:** Use PKG29_DRAFT as estimate label

**Trigger:** Standard naming convention for package estimates

**Evidence:** Prior estimates use PKG##_DRAFT format

**Impacted WBS/CBS:** Snapshot identification only

**Estimate Impact:** None

**Override:** Set `estimate_label` in `_CONFIG.md`

---

### D-004: Rounding Policy

**Decision:** Round summary totals to nearest $1,000 CAD

**Trigger:** Conceptual estimate precision; standard practice

**Evidence:** `_CONFIG.md` specifies rounding = 1000

**Impacted WBS/CBS:** Summary totals only; Detail.csv retains precision

**Estimate Impact:** Minor rounding adjustments

**Override:** Set `rounding` in `_CONFIG.md`

---

### D-005: Exclusions

**Decision:** Exclude owner's costs, land, financing, taxes, permits obtained by Employer

**Trigger:** Standard D&B contractor estimate scope

**Evidence:** `_CONFIG.md` exclude_scopes; decomposition Section 1.2

**Impacted WBS/CBS:** Entire estimate

**Estimate Impact:** Excluded items not priced

**Override:** Modify `exclude_scopes` in `_CONFIG.md`

---

### D-006: Indirects Model Selection

**Decision:** Use factor-based indirects model (not time-based)

**Trigger:** No construction schedule available

**Evidence:** Deliverables at INITIALIZED status; no schedule data

**Impacted WBS/CBS:** CI, P, PM, COM buckets

**Estimate Impact:** Factor-based may understate indirects for extended testing durations

**Override:** Provide schedule duration; use time-based model

---

### D-007: Escalation Mode

**Decision:** Escalation mode = NONE

**Trigger:** No schedule for escalation calculation

**Evidence:** `_CONFIG.md` escalation_mode = NONE; deliverables INITIALIZED

**Impacted WBS/CBS:** Entire estimate

**Estimate Impact:** Potential 3-6% annual escalation not captured; see Risk R-008

**Override:** Set escalation_mode = EXPLICIT and provide schedule

---

### D-008: Contingency Method

**Decision:** Use PCT_BY_BUCKET contingency with allowance-heavy adjustment

**Trigger:** 100% allowance-based estimate; no vendor quotes

**Evidence:** No pricing sources found; all quantities TBD

**Impacted WBS/CBS:** All CBS buckets

**Estimate Impact:** Elevated contingency rates (20-30% by bucket) due to uncertainty

**Override:** Provide vendor quotes and design quantities; reduce contingency

---

### D-009: Indirects Factors

**Decision:** Apply indirects factors: CI=18%, P=2%, PM=6%, COM=3%

**Trigger:** No project-specific factors available

**Evidence:** AGENT_ESTIMATING fallback typical model (lines 643-652)

**Impacted WBS/CBS:** CI, P, PM, COM buckets (L-019 through L-022)

**Estimate Impact:** $248,000 in factor-based indirects

**Override:** Provide project-specific indirects rates in `_RateTables/`

---

### D-010: WBS to CBS Mapping

**Decision:** Map deliverables to CBS based on deliverable type

**Trigger:** Standard WBS-CBS alignment for T&C package

**Evidence:** Deliverable descriptions in decomposition; WBS_CBS_Matrix.csv

**Impacted WBS/CBS:**
- Procedures (DEL-29.01, 29.02, 29.06) -> Engineering (E)
- Test records (DEL-29.03, 29.04, 29.05, 29.07, 29.08) -> Construction Directs (CD)
- Test equipment -> Materials (MAT)

**Estimate Impact:** Determines CBS bucket allocation

**Override:** Provide project-specific WBS-CBS mapping

---

### D-011: Hydrotest Water Disposal Method

**Decision:** Assume 50% discharge under permit, 50% haul-off disposal

**Trigger:** Discharge permit status unknown; environmental requirements TBD

**Evidence:** Large volume (45,000 m3); Metro Vancouver/VFPA permit uncertain; canola oil residue treatment required

**Impacted WBS/CBS:** CD bucket (L-013 disposal costs)

**Estimate Impact:** $120,000 for haul-off portion; if 100% haul-off required, add ~$120k

**Override:** Confirm discharge permit feasibility; adjust split ratio

---

### D-012: FAT Scope Definition

**Decision:** Include 8-12 major equipment FATs only; exclude minor equipment

**Trigger:** FAT equipment list not available; conceptual scope assumption

**Evidence:** Major equipment typically requiring FAT: storage tanks, pumps, marine loading arm, DCS, switchgear, VFDs

**Impacted WBS/CBS:** CD bucket (L-017 FAT attendance)

**Estimate Impact:** $125,000 for FAT attendance; additional FATs would increase cost

**Override:** Provide FAT equipment list; adjust FAT count and travel

---

**Decision Log Prepared By:** Estimating Agent
**Date:** 2026-01-29
**Total Decisions:** 12
