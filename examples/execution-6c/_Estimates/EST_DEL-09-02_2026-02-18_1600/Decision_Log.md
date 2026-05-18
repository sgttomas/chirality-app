# Decision Log -- EST_DEL-09-02_2026-02-18_1600

## Decisions Applied During This Run

### DEC-EST-001: CBS Mapping Rule

**Decision:** Map CBS codes from Professional_Staff_Rates.csv role categories as follows:
- R-02 (Management) -> PROF-PM
- R-07 (Design / Civil) -> PROF-CIVIL
- R-29 (Specialty / Geotechnical) -> PROF-GEOTECH

**Rationale:** No explicit CBSHint in the decomposition. A deterministic mapping from role Category column to CBS prefix provides traceable, repeatable cost breakdown structure codes. Documented in Run_Context.md.

### DEC-EST-002: Scope Resolution

**Decision:** SCOPE = DEL-09-02 resolves to exactly 1 deliverable under PKG-09.

**Rationale:** Decomposition Section 8 defines DEL-09-02_SiteConditionsAndDueDiligenceSummary. Section 7 confirms it belongs to PKG-09. Scope Ledger (Section 10) maps SOW-024 and SOW-025 to DEL-09-02.

### DEC-EST-003: Dependency Blockers Do Not Block Pricing

**Decision:** The 6 PENDING upstream prerequisite documents (reference reports) and 1 PENDING upstream interface (DEL-04-01) do not block the production cost estimate.

**Rationale:** These dependencies affect the content quality of the deliverable (whether the author can extract actual data from the reports). They do not affect the proposal production cost estimate because the hours and rates to produce DEL-09-02 are defined in Level_of_Effort.csv and Professional_Staff_Rates.csv regardless of report accessibility.

### DEC-EST-004: No Fallback Pricing Required

**Decision:** All 3 line items priced with RATE_TABLE evidence. No fallback to ALLOWANCE or PARAMETRIC needed.

**Rationale:** Both rate table (Professional_Staff_Rates.csv) and hours allocation (Level_of_Effort.csv) provide complete coverage for all roles assigned to DEL-09-02. FALLBACK_POLICY=STRICT, but not triggered.

### DEC-EST-005: Rounding Applied

**Decision:** ROUNDING=DOLLAR applied. All amounts are already whole dollars (no fractional cents in any line item computation).

**Rationale:** 8 x $175 = $1,400; 6 x $155 = $930; 4 x $155 = $620. All products are exact integers. Rounding had no material effect.
