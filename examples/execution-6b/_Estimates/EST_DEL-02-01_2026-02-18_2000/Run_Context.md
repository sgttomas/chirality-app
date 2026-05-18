# Run Context

| Field | Value |
|---|---|
| **RunID** | EST_DEL-02-01_2026-02-18_2000 |
| **AsOf** | 2026-02-18T20:00:00 |
| **Scope** | DEL-02-01 |
| **ScopeResolvedSummary** | 1 deliverable in scope; 4 line items (by role) |
| **BASIS_OF_ESTIMATE** | RATE_TABLE |
| **CURRENCY** | CAD |
| **PRICE_SOURCES** | Professional_Staff_Rates.csv; Level_of_Effort.csv; Assumed_Project_Parameters.csv |
| **DECOMPOSITION_PATH** | _Decomposition/Penhold_PSB_Project_Decomposition_v2.md (v2.3 FINAL) |
| **DEPENDENCY_SOURCES** | AUTO (read DEL-02-01/Dependencies.csv) |
| **FALLBACK_POLICY** | STRICT |
| **ALLOW_MIXED_METHODS** | FALSE |
| **UPDATE_LATEST_POINTER** | FALSE |
| **Rounding** | DOLLAR |
| **Warnings** | None |

## Resolved Paths

- **ESTIMATES_ROOT:** `test/execution-6b/_Estimates/`
- **Rate Table:** `test/execution-6b/_PriceSources/Professional_Staff_Rates.csv`
- **Level of Effort:** `test/execution-6b/_PriceSources/Level_of_Effort.csv`
- **Project Parameters:** `test/execution-6b/_PriceSources/Assumed_Project_Parameters.csv`
- **Dependencies:** `test/execution-6b/PKG-002_Conceptual_Design/1_Working/DEL-02-01_ArchitecturalConceptPackage/Dependencies.csv`
- **Decomposition:** `test/execution-6b/_Decomposition/Penhold_PSB_Project_Decomposition_v2.md`

## CBS Mapping Rule

CBS codes are assigned as `LABOR-{RoleCategory}` based on the `Category` column in Professional_Staff_Rates.csv. All line items for DEL-02-01 are labor costs (no materials, equipment, or subcontract items).

| RoleCategory | CBS |
|---|---|
| Design | LABOR-DESIGN |
| Production | LABOR-PRODUCTION |
| Management | LABOR-MGMT |

## Cost Ownership (Double-Counting Prevention)

Per the brief, DEL-02-01 carries ONLY:
- Architectural concept DRAWINGS (floor plans, elevations, sections)
- Architectural program integration (room layout, adjacencies, code compliance)
- Cross-discipline COORDINATION hours (architect leading discipline integration)

The following are explicitly NOT in DEL-02-01:
- Civil/site hours (DEL-02-02)
- Structural hours (DEL-02-03)
- Mechanical hours (DEL-02-04)
- Electrical hours (DEL-02-05)

## SOW Multi-Mapping Note

SOW-0009 and SOW-0010 map to all 5 PKG-002 deliverables. This estimate prices ONLY the architectural portion of those scope items, consistent with the cost ownership rules above.
