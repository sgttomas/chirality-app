# Decision Log -- EST_DEL-02-03_2026-02-18_1500

## Decisions Applied During This Run

### DEC-EST-001: CBS Mapping Rule

- **Decision:** Assign CBS = `PROF_SERVICES` with sub-categories by discipline (`.SPECIALTY`, `.MECH`, `.ELEC`, `.ARCH`)
- **Rationale:** No explicit `CBSHint` found in decomposition for DEL-02-03. Deliverable is purely proposal production (professional staff hours for narrative authoring). Sub-CBS categories align with the discipline of each role for traceability.
- **Alternatives considered:** Single CBS = `PROF_SERVICES` without sub-categories (rejected: less granular traceability).

### DEC-EST-002: No Fallback Applied

- **Decision:** All 4 line items priced using RATE_TABLE method with complete source evidence.
- **Rationale:** FALLBACK_POLICY = STRICT; all hours and rates fully sourced from Level_of_Effort.csv and Professional_Staff_Rates.csv. No fallback needed.

### DEC-EST-003: Rounding Application

- **Decision:** ROUNDING = DOLLAR applied. All line item amounts resolve to whole dollars without fractional rounding needed (all quantities and rates produce integer amounts: 12x165=1980, 8x160=1280, 6x155=930, 4x145=580).
- **Rationale:** Per brief configuration. No rounding adjustment required.

### DEC-EST-004: Dependency Sources Resolved via AUTO

- **Decision:** Read Dependencies.csv from the deliverable folder at the standard path.
- **Rationale:** DEPENDENCY_SOURCES = AUTO. File located at expected path. 11 rows extracted (3 ANCHOR, 8 EXECUTION).

### DEC-EST-005: No PM Hours in LOE -- Accepted

- **Decision:** Accepted the absence of Project Manager (R-02) hours for DEL-02-03 in the Level_of_Effort.csv without adding supplementary hours.
- **Rationale:** STRICT fallback policy does not permit adding hours not in the price sources. The brief BOE context describes DEL-02-03 as T2 (dependent on DEL-02-01 and DEL-02-02), suggesting PM coordination overhead is captured in those upstream deliverables. Noted in Assumptions_Log.md as ASM-003.

### DEC-EST-006: Scope Resolution -- Single Deliverable

- **Decision:** SCOPE = DEL-02-03 resolved to exactly one deliverable under PKG-04.
- **Rationale:** Decomposition Section 8 confirms DEL-02-03_SustainabilityAndEnergyNarrative as a defined deliverable. No scope expansion required.
