# Decision Log

## Run: EST_DEL-01-01_2026-02-18_1200

### DEC-EST-001: CBS Mapping Rule

- **Decision:** CBS codes assigned deterministically based on role Category from Professional_Staff_Rates.csv. Management roles -> MGMT; Design roles -> DESIGN; Administrative roles -> ADMIN.
- **Rationale:** No explicit CBSHint provided in decomposition. A deterministic mapping from the rate table Category column provides reproducible CBS assignments.
- **Affected lines:** All (L-001 through L-004).

### DEC-EST-002: Architect (Project) Hours Classified as Management Function

- **Decision:** R-04 Architect (Project) hours (40 hr) in DEL-01-01 are classified under CBS=DESIGN but recognized as a management function (design review/QA-QC), not discipline design production.
- **Rationale:** Per the invoker brief cost ownership rules: "Discipline-specific design hours (architectural, structural, mechanical, electrical, civil) are NOT in PKG-001; they are in PKG-002/003/004 discipline deliverables." The Level_of_Effort.csv notes for this row state "Design review; QA/QC review cycles," confirming this is a coordination/management function. CBS=DESIGN is retained because the role Category in the rate table is "Design," but the Notes column clarifies the management nature.
- **Affected lines:** L-003.

### DEC-EST-003: Rounding Applied

- **Decision:** ROUNDING=DOLLAR applied to all amounts. All computed amounts (rate x hours) are already whole dollar amounts, so no rounding adjustment was needed.
- **Affected lines:** All.

### DEC-EST-004: No Fallback Required

- **Decision:** All 4 line items for DEL-01-01 have complete rate table evidence (rate from Professional_Staff_Rates.csv + hours from Level_of_Effort.csv). FALLBACK_POLICY=STRICT was not triggered.
- **Affected lines:** None (no fallback applied).

### DEC-EST-005: Dependency Evidence Used for Readiness Only

- **Decision:** Dependencies.csv for DEL-01-01 (21 rows) was read and assessed for blockers. No dependency rows were used as pricing evidence. Dependency registers inform readiness/blockers only, per agent invariant.
- **Affected lines:** None (informational).
