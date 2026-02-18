# Run Context

## Run Identity

| Field | Value |
|---|---|
| **RunID** | EST_DEL-09-01_2026-02-18_1500 |
| **AsOf** | 2026-02-18T15:00:00-07:00 |
| **Agent** | ESTIMATING (Type 2) |

---

## Inputs (as provided)

| Parameter | Value |
|---|---|
| **SCOPE** | DEL-09-01 |
| **RUN_ROOT** | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6c/PKG-09_Due Diligence & Risk Register/1_Working/DEL-09-01_RiskRegisterAndMitigationPlan |
| **ESTIMATES_ROOT** | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6c/_Estimates/ |
| **BASIS_OF_ESTIMATE** | RATE_TABLE |
| **CURRENCY** | CAD |
| **OUTPUT_LABEL** | DEL-09-01 |

---

## Resolved Defaults

| Parameter | Resolved Value |
|---|---|
| **DECOMPOSITION_PATH** | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6c/_Decomposition/Penhold_PSB_Project_Decomposition_Final_AddendumIntegrated_v1.md |
| **DEPENDENCY_SOURCES** | AUTO (resolved to Dependencies.csv at deliverable path) |
| **FALLBACK_POLICY** | STRICT |
| **ALLOW_MIXED_METHODS** | FALSE |
| **UPDATE_LATEST_POINTER** | FALSE |
| **ROUNDING** | DOLLAR |
| **RUN_TIMESTAMP** | 2026-02-18T15:00:00-07:00 |

---

## Scope Resolved Summary

| Metric | Value |
|---|---|
| Deliverables in scope | 1 |
| Deliverables covered (priced) | 1 |
| Deliverables blocked | 0 |
| Deliverables excluded | 0 |

---

## PRICE_SOURCES (resolved)

| # | File | Type | Status |
|---|---|---|---|
| 1 | Professional_Staff_Rates.csv | Rate Table (hourly rates by role) | LOADED — 30 roles |
| 2 | Level_of_Effort.csv | Rate Table (hours per role per deliverable) | LOADED — 3 rows for DEL-09-01 |
| 3 | Assumed_Project_Parameters.csv | Reference parameters | LOADED — 29 parameters (context only) |

---

## CBS Mapping Rule

CBS codes are assigned deterministically based on the `Category` field in Professional_Staff_Rates.csv for each role. The mapping is:

| Role Category | CBS Code | CBS Label |
|---|---|---|
| Management | CBS-MGMT | Management / PM Labour |
| Construction | CBS-CONST | Construction Management Labour |

This is a professional-hours-only deliverable; no construction materials or equipment apply.

---

## Warnings

- None. All inputs loaded successfully. All LOE rows for DEL-09-01 have matching rate table entries. BASIS_OF_ESTIMATE=RATE_TABLE is valid.
