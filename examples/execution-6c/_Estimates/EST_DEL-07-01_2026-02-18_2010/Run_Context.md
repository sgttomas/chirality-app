# Run Context — EST_DEL-07-01_2026-02-18_2010

## Run Identity

| Field | Value |
|---|---|
| **RunID** | EST_DEL-07-01_2026-02-18_2010 |
| **AsOf** | 2026-02-18T20:10:45Z |
| **AgentType** | ESTIMATING (Type 2) |

---

## Scope

| Field | Value |
|---|---|
| **Scope (as provided)** | DEL-07-01 |
| **ScopeResolvedSummary** | 1 deliverable in scope; 0 excluded; 0 blocked |
| **DeliverableID** | DEL-07-01 |
| **DeliverableName** | DB Firm Experience Profile |
| **PackageID** | PKG-03 |
| **PackageName** | Team Qualifications (Appendix I + resumes) |
| **Tier** | T0 (no upstream production dependencies) |

---

## Configuration

| Parameter | Value |
|---|---|
| **BASIS_OF_ESTIMATE** | RATE_TABLE |
| **CURRENCY** | CAD |
| **FALLBACK_POLICY** | STRICT |
| **ALLOW_MIXED_METHODS** | FALSE |
| **UPDATE_LATEST_POINTER** | FALSE |
| **ROUNDING** | DOLLAR |
| **OUTPUT_LABEL** | DEL-07-01 |

---

## Resolved Paths

| Input | Resolved Path |
|---|---|
| **ESTIMATES_ROOT** | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6c/_Estimates/ |
| **RUN_ROOT** | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6c/PKG-03_Team Qualifications (Appendix I + resumes)/1_Working/DEL-07-01_DesignBuildFirmExperienceProfile |
| **DECOMPOSITION_PATH** | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6c/_Decomposition/Penhold_PSB_Project_Decomposition_Final_AddendumIntegrated_v1.md |
| **DEPENDENCY_SOURCES** | AUTO -- read {RUN_ROOT}/Dependencies.csv |
| **PRICE_SOURCES[0]** | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6c/_PriceSources/Professional_Staff_Rates.csv |
| **PRICE_SOURCES[1]** | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6c/_PriceSources/Level_of_Effort.csv |
| **PRICE_SOURCES[2]** | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6c/_PriceSources/Assumed_Project_Parameters.csv |

---

## CBS Mapping Rule

CBS codes are assigned deterministically based on the role Category from Professional_Staff_Rates.csv:

| Role Category | CBS Code | CBS Label |
|---|---|---|
| Administrative | CBS-ADMIN | Administrative / Proposal Coordination |
| Management | CBS-MGMT | Management / Project Management |

This mapping is documented in Decision_Log.md (DEC-R01).

---

## Warnings

- None. All price sources loaded successfully. Decomposition confirmed. Dependencies loaded (10 ACTIVE rows; no estimate-blocking items).
