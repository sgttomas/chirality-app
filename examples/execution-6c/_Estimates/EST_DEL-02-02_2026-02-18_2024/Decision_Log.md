# Decision Log — EST_DEL-02-02_2026-02-18_2024

**Snapshot:** EST_DEL-02-02_2026-02-18_2024
**Date:** 2026-02-18

---

## Decisions Applied

### DEC-EST-0202-001: CBS Mapping Rule

**Decision:** CBS codes assigned deterministically from the `Category` column in `Professional_Staff_Rates.csv`:
- `Management` -> `PROF_MGMT`
- `Design` -> `PROF_DESIGN`
- `Specialty` -> `PROF_SPECIALTY`

**Rationale:** No explicit `CBSHint` is present in the decomposition. The rate table's `Category` column provides the most stable, source-backed classification available. This rule is documented in `Run_Context.md` and applied consistently.

**Alternative considered:** Using a single CBS code (e.g., `PROF_SERVICES`) for all lines. Rejected because the rate table provides a natural granularity that supports cost analysis by discipline grouping.

---

### DEC-EST-0202-002: No Fallback Required

**Decision:** No fallback pricing applied. All 8 line items priced directly from RATE_TABLE sources.

**Rationale:** FALLBACK_POLICY = STRICT, but fallback was not triggered because all roles in Level_of_Effort.csv for DEL-02-02 have matching entries in Professional_Staff_Rates.csv. No pricing gaps exist.

---

### DEC-EST-0202-003: Dependency Evidence Used for Readiness Only

**Decision:** Dependencies.csv (19 rows) reviewed for blocker identification. No dependency data used for pricing. Upstream prerequisites (RFP, addenda, geotech report, DEL-02-01) are production sequencing constraints, not estimate-blocking dependencies.

**Rationale:** Per agent instructions: "Dependencies are not pricing evidence." The dependency register confirms that DEL-02-02 can be meaningfully estimated even though production has sequencing constraints.

---

### DEC-EST-0202-004: Assumed_Project_Parameters.csv Used for Context Only

**Decision:** Assumed_Project_Parameters.csv was loaded and reviewed but no line items derive pricing from it. It provides project scope context (building areas, bay counts, etc.) that confirms the design brief subject matter is a $12-20M municipal facility.

**Rationale:** DEL-02-02 is a proposal production cost (professional time to write narrative), not a construction cost. The parameters confirm scope calibration but do not drive unit rates or quantities.

---

### DEC-EST-0202-005: Scope Boundary — Cost Ownership Alignment

**Decision:** All 80 hours from Level_of_Effort.csv for DEL-02-02 are treated as narrative writing and coordination hours per the BOE context. No hours are split to/from DEL-02-01 (concept drawings) or DEL-02-03 (sustainability narrative).

**Rationale:** The BOE context explicitly states:
- Design Brief NARRATIVE belongs to DEL-02-02 (not DEL-02-01)
- Durability/maintenance NARRATIVE belongs to DEL-02-02
- Accessibility NARRATIVE belongs to DEL-02-02
- Adaptability/expansion NARRATIVE belongs to DEL-02-02
- Sustainability/energy strategy goes in DEL-02-03 (not here)

The Level_of_Effort.csv already reflects this boundary (separate allocations exist for DEL-02-01 and DEL-02-03).
