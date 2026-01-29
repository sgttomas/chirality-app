# Decision Log

## EST_PKG09_DRAFT_2026-01-28_2332

All decisions made during the estimating process for PKG-09 Marine Outfitting.

---

### D-001: Currency Selection

**Decision:** Use CAD (Canadian dollars) as the single currency for this estimate.

**Trigger:** Config did not specify currency; auto-discovery required.

**Evidence:** Project location is Fraser Surrey Terminal, 11060 Elevator Road, Surrey, BC, Canada (decomposition Section 1). All work is performed in Canada.

**Impacted WBS/CBS:** All packages and CBS buckets.

**Estimate Impact:** No conversion required; single-currency estimate reduces complexity and eliminates FX risk.

**How to Override:** Set `currency: USD` (or other) in `_CONFIG.md` if required by contract.

---

### D-002: Marine Structure Interface Assumption

**Decision:** Assume PKG-08 Marine Structures provides structural capacity for fender/bollard mounting.

**Trigger:** PKG-08 deliverables (DEL-08.01, DEL-08.03) are not yet available; interface assumptions required.

**Evidence:** Decomposition Section PKG-09 scope states "Fenders, bollards, ladders, life-saving equipment, existing Berth 10 upgrades and repairs." PKG-08 is responsible for "Marine Structures."

**Impacted WBS/CBS:** PKG-09 installation scope (CD lines L-011 through L-015).

**Estimate Impact:** Scope boundary assumed; no structural capacity upgrades included in PKG-09 estimate.

**How to Override:** Coordinate with PKG-08 outputs (DEL-08.01, DEL-08.03) when available to confirm interface scope.

---

### D-003: Berthing Design Basis

**Decision:** Assume berthing energy and mooring loads will be provided by PKG-08 analyses (DEL-08.06, DEL-08.09).

**Trigger:** No berthing energy calculations or mooring analysis results available.

**Evidence:** Decomposition PKG-08 includes DEL-08.06 (Berthing Energy Calculation), DEL-08.07 (Fender System Deflection Characteristics), DEL-08.08 (Fender Supplier Design Verification), and DEL-08.09 (Mooring Analysis).

**Impacted WBS/CBS:** MAT lines L-006 (fenders) and L-007 (bollards); fender/bollard sizing assumptions.

**Estimate Impact:** Fender and bollard sizing/capacity based on parametric assumptions (Panamax vessel class).

**How to Override:** Update fender/bollard specifications when PKG-08 analyses are complete.

---

### D-004: Productivity Factor

**Decision:** Use productivity factor of 1.0 (BC lower mainland baseline).

**Trigger:** No project-specific productivity data available.

**Evidence:** Location is Surrey, BC, Canada (decomposition Section 1). BC lower mainland is a mature construction market with standard labor availability.

**Impacted WBS/CBS:** CD (Construction Directs) labor rates.

**Estimate Impact:** No productivity adjustment applied; labor rates use baseline values.

**How to Override:** Adjust productivity factor in rate tables if site-specific constraints are identified (e.g., access limitations, concurrent operations).

---

### D-005: Marine Access Method

**Decision:** Assume marine installation via crane barge with water-based access for fenders/bollards.

**Trigger:** No installation method specified; marine work requires access assumptions.

**Evidence:** Marine outfitting typically requires crane barge for positioning/installation of heavy fenders and bollards at waterside locations.

**Impacted WBS/CBS:** CD line L-016 (Marine Crane/Barge Mobilization); installation labor lines L-011, L-012.

**Estimate Impact:** Crane barge mobilization cost of $65,000 included; marine labor rates assume barge-based work.

**How to Override:** Confirm installation method with site logistics plan and PKG-08 marine structure access provisions.

---

### D-006: Working Hours and Constraints

**Decision:** Standard 8-10 hour shifts assumed; marine work subject to tide and weather constraints.

**Trigger:** No project schedule or work hour constraints specified.

**Evidence:** Marine construction typically limited by tides, weather, and vessel traffic. Standard shifts assumed for cost estimating.

**Impacted WBS/CBS:** CD (Construction Directs) labor productivity and CI (Construction Indirects) supervision.

**Estimate Impact:** Labor rates assume standard productivity; no shift premiums or overtime included.

**How to Override:** Adjust rates if compressed schedule or shift work is required (update _CONFIG.md or provide project schedule).

---

### D-007: Pricing Sources Hierarchy

**Decision:** All line items priced via allowances (fallback typical model) due to absence of vendor quotes or project rate tables.

**Trigger:** No vendor quotes or rate tables provided; straight-through estimating requires pricing basis.

**Evidence:** No vendor quotes found; no rate tables in `_RateTables/` directory.

**Impacted WBS/CBS:** All CBS buckets; all MAT and CD line items.

**Estimate Impact:** 100% allowance-based estimate; confidence = LOW; contingency elevated per PCT_BY_BUCKET method.

**How to Override:** Provide vendor budgetary quotes for fenders, bollards, ladders, life-saving equipment. Provide project labor/equipment rate tables in `_RateTables/`.

---

### D-008: Indirects and Services Factors

**Decision:** Apply factor-based indirects model using fallback typical model rates.

**Trigger:** No project-specific indirects model or schedule-based data available.

**Evidence:** Fallback typical model (STRUCTURE section of AGENT_ESTIMATING.md).

**Impacted WBS/CBS:**
- CI (Construction Indirects): 18% of CD
- P (Procurement Services): 2% of MAT
- PM (Project Management / EPCM): 6% of (CD + CI + MAT)
- COM (Commissioning): 3% of (CD + CI + MAT)

**Estimate Impact:**
- CI = $64,000 (18% × $355,000)
- P = $31,000 (2% × $1,534,000)
- PM = $114,000 (6% × $1,953,000)
- COM adjusted to reflect proof load testing scope (see lines L-023 through L-025)

**How to Override:** Provide project-specific indirects rates, schedule-based resource loading, or overhead allocation model in _CONFIG.md or rate tables.

---

### D-009: Contingency Method and Rates

**Decision:** Apply PCT_BY_BUCKET contingency with allowance-heavy adjustment (100% allowance estimate).

**Trigger:** Config specified `contingency_method: PCT_BY_BUCKET`; all line items are allowances.

**Evidence:** Fallback typical model contingency rates (STRUCTURE section) plus allowance adjustment (+10% for buckets with 100% allowance share).

**Impacted WBS/CBS:** All CBS buckets.

**Estimate Impact:**
- E: 20% (10% base + 10% allowance adjustment)
- MAT: 25% (15% base + 10% allowance adjustment)
- CD: 30% (20% base + 10% allowance adjustment)
- CI: 30% (20% base + 10% factor-derived adjustment)
- PM: 15% (10% base + 5% factor-derived adjustment)
- P: 15% (10% base + 5% factor-derived adjustment)
- COM: 30% (25% base + 5% factor-derived adjustment)

**Total Contingency:** $568,000 (25.3% of base)

**How to Override:** Provide vendor quotes to reduce allowance share and lower contingency rates. Alternatively, switch to `contingency_method: RISK_BASED` in _CONFIG.md for three-point estimating.

---

### D-010: Escalation Mode

**Decision:** No escalation applied (escalation_mode = NONE).

**Trigger:** Config default; no schedule or cashflow data available.

**Evidence:** Pricing date is January 2026 (current); no future escalation factors defined.

**Impacted WBS/CBS:** All CBS buckets.

**Estimate Impact:** Estimate is in "January 2026 dollars"; no escalation to future expenditure dates.

**How to Override:** Set `escalation_mode: EXPLICIT` in _CONFIG.md and provide schedule/cashflow curve and escalation factors.

---

## Summary

| Decision ID | Topic | Impact |
|-------------|-------|--------|
| D-001 | Currency = CAD | Single-currency estimate |
| D-002 | PKG-08 interface | Scope boundary assumption |
| D-003 | Berthing design basis | Fender/bollard sizing assumptions |
| D-004 | Productivity factor = 1.0 | No productivity adjustment |
| D-005 | Marine access via crane barge | Installation method assumption |
| D-006 | Standard working hours | No shift premiums |
| D-007 | 100% allowance pricing | Low confidence; high contingency |
| D-008 | Factor-based indirects | Default fallback model |
| D-009 | Contingency = 25.3% of base | Elevated for allowance-heavy estimate |
| D-010 | No escalation | January 2026 dollars |

---

*All decisions are traceable to source documents, config defaults, or fallback typical model per AGENT_ESTIMATING.md PROTOCOL.*
