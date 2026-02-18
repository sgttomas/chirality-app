# Run Context

| Field | Value |
|---|---|
| **RunID** | EST_DEL-01-08_2026-02-18_1500 |
| **AsOf** | 2026-02-18T15:00:00-07:00 |
| **Scope** | DEL-01-08 |
| **ScopeResolvedSummary** | 1 deliverable in scope; 0 excluded; 0 blocked |
| **BASIS_OF_ESTIMATE** | RATE_TABLE |
| **CURRENCY** | CAD |
| **PRICE_SOURCES** | Professional_Staff_Rates.csv, Level_of_Effort.csv, Assumed_Project_Parameters.csv |
| **DECOMPOSITION_PATH** | _Decomposition/Penhold_PSB_Project_Decomposition_v2.md (v2.3 FINAL) |
| **DEPENDENCY_SOURCES** | AUTO (read DEL-01-08/Dependencies.csv) |
| **FALLBACK_POLICY** | STRICT |
| **ALLOW_MIXED_METHODS** | FALSE |
| **UPDATE_LATEST_POINTER** | FALSE |
| **Rounding** | DOLLAR |

## Resolved Paths

| Source | Absolute Path |
|---|---|
| Professional_Staff_Rates.csv | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6b/_PriceSources/Professional_Staff_Rates.csv |
| Level_of_Effort.csv | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6b/_PriceSources/Level_of_Effort.csv |
| Assumed_Project_Parameters.csv | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6b/_PriceSources/Assumed_Project_Parameters.csv |
| Decomposition | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6b/_Decomposition/Penhold_PSB_Project_Decomposition_v2.md |
| Dependencies.csv | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6b/PKG-001_Proposal_Compliance_Commercial_and_Team_Qualifications/1_Working/DEL-01-08_KeyTeamMembersAndResumes/Dependencies.csv |

## CBS Mapping Rule

CBS codes are assigned based on role category from Professional_Staff_Rates.csv:
- Administrative roles (R-22, R-24, R-26) -> CBS: PROPOSAL_ADMIN
- No other role categories appear for DEL-01-08.

Since DEL-01-08 is a Tier 0 / Administrative deliverable (resume compilation and formatting), all line items are classified under CBS `PROPOSAL_ADMIN`.

## Pricing Method

Cost = Hours (from Level_of_Effort.csv, filtered to DEL-01-08) x HourlyRate_CAD (from Professional_Staff_Rates.csv, matched by RoleID).

All hours for DEL-01-08 are sourced from Level_of_Effort.csv rows where DeliverableID = DEL-01-08. Rates are sourced from Professional_Staff_Rates.csv matched by RoleID. This constitutes a RATE_TABLE method: externally defined rates applied to externally defined quantities.

## Warnings

None.
