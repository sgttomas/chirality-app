# Estimate Summary -- EST_DEL-02-03_2026-02-18_1500

## DEL-02-03: Sustainability & Energy Narrative

**Package:** PKG-04 (Design Proposal -- Concept + Design Brief)
**Basis of Estimate:** RATE_TABLE
**Currency:** CAD
**Rounding:** DOLLAR

---

## BasisOfEstimate_Used

| Field | Value |
|-------|-------|
| **Method** | RATE_TABLE |
| **Rate Source** | Professional_Staff_Rates.csv (Alberta 2024 market rates) |
| **Quantity Source** | Level_of_Effort.csv (parametric planning estimates for 6c execution) |
| **Fallback Policy** | STRICT (no fallback used) |
| **Mixed Methods** | FALSE (all lines = RATE_TABLE) |

---

## Total by Deliverable

| WBS_DeliverableID | Name | Amount (CAD) | Line Count |
|-------------------|------|-------------|------------|
| DEL-02-03 | Sustainability & Energy Narrative | **$4,770** | 4 |

---

## Total by CBS

| CBS | Description | Amount (CAD) | Lines |
|-----|-------------|-------------|-------|
| PROF_SERVICES.SPECIALTY | Building Science Consultant | $1,980 | 1 |
| PROF_SERVICES.MECH | Mechanical Engineering | $1,280 | 1 |
| PROF_SERVICES.ELEC | Electrical Engineering | $930 | 1 |
| PROF_SERVICES.ARCH | Architecture | $580 | 1 |
| **PROF_SERVICES (total)** | **All professional services** | **$4,770** | **4** |

---

## Total by Role

| RoleID | Role | Hours | Rate (CAD/hr) | Amount (CAD) | % of Total |
|--------|------|-------|--------------|-------------|-----------|
| R-27 | Building Science Consultant | 12 | $165 | $1,980 | 41.5% |
| R-11 | Mechanical Engineer (Senior) | 8 | $160 | $1,280 | 26.8% |
| R-13 | Electrical Engineer (Senior) | 6 | $155 | $930 | 19.5% |
| R-04 | Architect (Project) | 4 | $145 | $580 | 12.2% |
| **Total** | | **30** | | **$4,770** | **100.0%** |

---

## Key Observations

1. **DEL-02-03 is a mid-range proposal production deliverable** at $4,770 (30 total hours). This is appropriate for a focused narrative deliverable covering energy efficiency, sustainability strategy, and solar-ready provisions.

2. **Building Science Consultant leads the effort** (41.5% of cost, 40% of hours), consistent with the deliverable scope: energy strategy, envelope performance, and code compliance narrative.

3. **Multi-discipline input is limited but targeted**: Mechanical (HVAC energy efficiency, solar-ready mechanical), Electrical (solar-ready electrical, energy efficiency), and Architecture (envelope coordination) each contribute proportionally to their scope.

4. **No Project Manager hours allocated** for this deliverable in the LOE. Coordination overhead may be captured in the PM hours allocated to DEL-02-01 and DEL-02-02 (upstream dependencies). This is noted but not flagged as a gap since the brief BOE context confirms DEL-02-03 is a Tier 2 deliverable dependent on the concept and design brief.

---

## Warnings and Blockers

### Dependency-Derived Blockers (from Dependencies.csv)

| DependencyID | Target | EstimateImpactClass | Status | Note |
|-------------|--------|-------------------|--------|------|
| DEP-0004 | DEL-02-01 (Concept Design Package) | BLOCKING | TBD | Solar-ready orientation strategy depends on building orientation from concept design |
| DEP-0010 | RFP Appendix A (OSR) | BLOCKING | TBD | Code edition confirmation needed for compliance baseline |
| DEP-0011 | Addendum 03 | BLOCKING | TBD | Mandatory content requirements (solar-ready, exhaust, generator, etc.) |

### Advisory Dependencies

| DependencyID | Target | EstimateImpactClass | Note |
|-------------|--------|-------------------|------|
| DEP-0005 | DEL-02-02 (Design Brief Narrative) | ADVISORY | Scope boundary coordination |
| DEP-0006 | DEL-09-02 (Site Conditions) | ADVISORY | Stormwater/water efficiency alignment |
| DEP-0007 | DEL-06-01 (Commissioning) | ADVISORY | Downstream boundary (high-level vs. detailed commissioning) |

**Note:** These blockers affect the narrative content production, not the cost estimate itself. The estimate is based on pre-determined hours and rates. The blockers indicate that narrative work cannot be finalized until upstream deliverables provide required information.
