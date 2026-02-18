# Run Context

## Run Identity

| Field | Value |
|---|---|
| **RunID** | EST_DEL-01-01_2026-02-18_2100 |
| **AsOf** | 2026-02-18T21:00:00-07:00 |
| **Agent** | ESTIMATING (Type 2) |

---

## Brief Inputs (as provided)

| Parameter | Value |
|---|---|
| **SCOPE** | DEL-01-01 |
| **RUN_ROOT** | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6c/PKG-01_Compliance & Submission/1_Working/DEL-01-01_ComplianceMatrixAndChecklist |
| **ESTIMATES_ROOT** | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6c/_Estimates/ |
| **BASIS_OF_ESTIMATE** | RATE_TABLE |
| **CURRENCY** | CAD |
| **OUTPUT_LABEL** | DEL-01-01 |
| **UPDATE_LATEST_POINTER** | FALSE |
| **FALLBACK_POLICY** | STRICT |
| **ALLOW_MIXED_METHODS** | FALSE |
| **ROUNDING** | DOLLAR |

---

## Resolved Inputs

| Parameter | Resolved Value |
|---|---|
| **DECOMPOSITION_PATH** | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6c/_Decomposition/Penhold_PSB_Project_Decomposition_Final_AddendumIntegrated_v1.md |
| **DEPENDENCY_SOURCES** | AUTO -- read from DEL-01-01 deliverable folder |
| **Dependencies.csv** | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6c/PKG-01_Compliance & Submission/1_Working/DEL-01-01_ComplianceMatrixAndChecklist/Dependencies.csv |

### PRICE_SOURCES (resolved)

| # | Path | Type | Status |
|---|---|---|---|
| 1 | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6c/_PriceSources/Professional_Staff_Rates.csv | Rate Table | Loaded (30 roles) |
| 2 | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6c/_PriceSources/Level_of_Effort.csv | Rate Table (hours) | Loaded (67 rows; 1 row for DEL-01-01) |
| 3 | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6c/_PriceSources/Assumed_Project_Parameters.csv | Parameters | Loaded (29 params) |

---

## Scope Resolved Summary

| Metric | Value |
|---|---|
| Deliverables in scope | 1 |
| Deliverables estimated | 1 |
| Deliverables blocked | 0 |
| Deliverables excluded | 0 |

---

## CBS Mapping Rule

No explicit `CBSHint` was present in the decomposition for DEL-01-01. CBS is assigned deterministically based on the role category from `Professional_Staff_Rates.csv`:

| Role Category | CBS Code |
|---|---|
| Administrative | ADMIN |
| Management | MGMT |
| Design | DESIGN |
| Production | PROD |
| Construction | CONST |
| Financial | FIN |
| Specialty | SPEC |
| Legal | LEGAL |
| External | EXT |

For DEL-01-01, the sole role (R-22 Proposal Coordinator / Writer) has Category = Administrative, so CBS = `ADMIN`.

---

## Warnings

None.
