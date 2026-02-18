# Run Context

| Field | Value |
|---|---|
| **RunID** | EST_DEL-07-03_2026-02-18_2000 |
| **AsOf** | 2026-02-18T20:00:00-07:00 |
| **Scope** | DEL-07-03 |
| **ScopeResolvedSummary** | 1 deliverable in scope; 0 excluded; 0 blocked |
| **BASIS_OF_ESTIMATE** | RATE_TABLE |
| **CURRENCY** | CAD |
| **PRICE_SOURCES** | Professional_Staff_Rates.csv; Level_of_Effort.csv; Assumed_Project_Parameters.csv |
| **DECOMPOSITION_PATH** | _Decomposition/Penhold_PSB_Project_Decomposition_v2.md (v2.3 FINAL) |
| **DEPENDENCY_SOURCES** | AUTO (resolved: DEL-07-03/Dependencies.csv found; 12 dependency rows loaded) |
| **FALLBACK_POLICY** | STRICT |
| **ALLOW_MIXED_METHODS** | FALSE |
| **UPDATE_LATEST_POINTER** | FALSE |
| **Rounding** | DOLLAR |
| **Warnings** | None |

## Scope Resolution

| DeliverableID | PackageID | Path | InScope | Notes |
|---|---|---|---|---|
| DEL-07-03 | PKG-007 | PKG-007_Construction_Methodology_and_Administration/1_Working/DEL-07-03_SubconsultantApproachNarrative/ | TRUE | Subconsultant Approach Narrative; SOW-0021; OBJ-002, OBJ-006 |

## CBS Mapping Rule

CBS codes are assigned using a deterministic rule based on the rate table `Category` column in `Professional_Staff_Rates.csv`:
- `Management` category roles -> CBS `MGMT`
- `Construction` category roles -> CBS `CONST`
- `Design` category roles -> CBS `DESIGN`
- `Specialty` category roles -> CBS `SPECIALTY`
- For DEL-07-03, only R-02 (Project Manager, Management category) appears in Level_of_Effort.csv, so all hours map to CBS `MGMT`.

## Pricing Method

Cost = SUM(EstimatedHours per role x HourlyRate_CAD per role), sourced from:
- Hours: `Level_of_Effort.csv` (filtered to Execution=6b, DeliverableID=DEL-07-03)
- Rates: `Professional_Staff_Rates.csv` (matched by RoleID)

## Cost Ownership Boundary

Per brief instructions:
- DEL-07-03 covers the subconsultant APPROACH narrative: discipline listing, management/interface approach, geotechnical review protocol (existing 2021 report only per DEC-013).
- DEL-01-09 (Appendix I) is the subtrade LIST form -- that is a separate deliverable and its cost is NOT included here.
- DEL-07-03 is the narrative that explains HOW subconsultants will be managed, not WHO they are.
- DEL-07-01 (Construction Methodology) provides the team accountability context that DEL-07-03 must align with -- interface dependency only, no cost overlap.
