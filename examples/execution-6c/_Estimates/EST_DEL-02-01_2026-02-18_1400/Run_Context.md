# Run Context — EST_DEL-02-01_2026-02-18_1400

| Field | Value |
|---|---|
| **RunID** | EST_DEL-02-01_2026-02-18_1400 |
| **AsOf** | 2026-02-18T14:00:00-07:00 |
| **Scope** | DEL-02-01 |
| **ScopeResolvedSummary** | 1 deliverable in scope; 0 excluded; 0 blocked |
| **BASIS_OF_ESTIMATE** | RATE_TABLE |
| **CURRENCY** | CAD |
| **PRICE_SOURCES** | Professional_Staff_Rates.csv, Level_of_Effort.csv, Assumed_Project_Parameters.csv |
| **DECOMPOSITION_PATH** | Penhold_PSB_Project_Decomposition_Final_AddendumIntegrated_v1.md (loaded) |
| **DEPENDENCY_SOURCES** | AUTO (DEL-02-01/Dependencies.csv loaded; 16 rows) |
| **FALLBACK_POLICY** | STRICT |
| **ALLOW_MIXED_METHODS** | FALSE |
| **UPDATE_LATEST_POINTER** | FALSE |
| **Rounding** | DOLLAR |
| **Warnings** | None |

---

## Scope Resolution

| DeliverableID | PackageID | Path | InScope | Notes |
|---|---|---|---|---|
| DEL-02-01 | PKG-04 | PKG-04_Design Proposal (Concept + Design Brief)/1_Working/DEL-02-01_ConceptDesignPackage | TRUE | Concept Design Package; Tier T1 foundational deliverable |

---

## CBS Mapping Rule

CBS codes are assigned deterministically based on role category from Professional_Staff_Rates.csv:

| Role Category | CBS Code | Rule |
|---|---|---|
| Design — Architectural (R-04, R-05) | DESIGN-ARCH | Architectural design hours |
| Production — CAD/BIM (R-06) | PRODUCTION-CAD | Drawing production hours; CAD/BIM software cost embedded in rate |
| Design — Civil (R-07, R-08) | DESIGN-CIVIL | Civil/site engineering hours |
| Design — Structural (R-09, R-10) | DESIGN-STRUCT | Structural engineering hours |
| Design — Mechanical (R-11, R-12) | DESIGN-MECH | Mechanical engineering hours |
| Design — Electrical (R-13, R-14) | DESIGN-ELEC | Electrical engineering hours |
| Management — PM (R-02) | MGMT-COORD | Project management coordination hours |

---

## Price Source Resolution

| Source | Type | Status | Notes |
|---|---|---|---|
| Professional_Staff_Rates.csv | Rate table (hourly rates by role) | Loaded; 30 roles | Provides UnitRate for each line item |
| Level_of_Effort.csv | Rate table (hours by deliverable x role) | Loaded; 12 rows for DEL-02-01 | Provides Qty (hours) for each line item |
| Assumed_Project_Parameters.csv | Parameters | Loaded; 29 params | Context only; no direct pricing for DEL-02-01 |

All line items priced as: Amount = Qty (hours) x UnitRate ($/hr) per RATE_TABLE method.

---

## Exclusions Applied

- `_Estimates/**` — prior estimate snapshots excluded from source ingestion
- `_Aggregation/**` — aggregation outputs excluded
- `_Reconciliation/**` — reconciliation outputs excluded
- `_Archive/**` — archived content excluded
