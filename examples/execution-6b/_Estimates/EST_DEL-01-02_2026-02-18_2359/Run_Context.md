# Run Context

| Field | Value |
|---|---|
| **RunID** | EST_DEL-01-02_2026-02-18_2359 |
| **AsOf** | 2026-02-18T23:59:00-07:00 |
| **Scope** | DEL-01-02 |
| **ScopeResolvedSummary** | 1 deliverable in scope; 0 excluded; 0 blocked |
| **BASIS_OF_ESTIMATE** | RATE_TABLE |
| **CURRENCY** | CAD |
| **PRICE_SOURCES** | Professional_Staff_Rates.csv; Level_of_Effort.csv; Assumed_Project_Parameters.csv |
| **DECOMPOSITION_PATH** | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6b/_Decomposition/Penhold_PSB_Project_Decomposition_v2.md |
| **DEPENDENCY_SOURCES** | AUTO (read DEL-01-02/Dependencies.csv) |
| **FALLBACK_POLICY** | STRICT |
| **ALLOW_MIXED_METHODS** | FALSE |
| **UPDATE_LATEST_POINTER** | FALSE |
| **Rounding** | DOLLAR |
| **OUTPUT_LABEL** | DEL-01-02 |
| **Warnings** | None |

## Scope Resolution

| DeliverableID | PackageID | Path | InScope | Notes |
|---|---|---|---|---|
| DEL-01-02 | PKG-001 | PKG-001_.../DEL-01-02_FormalSubmissionPackage | TRUE | Formal Submission Package (Final PDF Assembly) -- Tier 4, 38th and final deliverable |

## CBS Mapping Rule

CBS codes assigned deterministically based on role category from Professional_Staff_Rates.csv:
- Administrative roles (R-22 Proposal Coordinator/Writer, R-24 Administrative/Document Control) -> CBS = `ADMIN`
- Management roles (R-02 Project Manager) -> CBS = `MGMT`

This rule is consistent across all estimate snapshots in this execution run.

## Price Source Resolution

- **Level_of_Effort.csv**: Provides hours by role for DEL-01-02. Two rows found: R-22 (16h), R-02 (4h).
- **Professional_Staff_Rates.csv**: Provides hourly rates by RoleID. R-22 = $105/hr CAD, R-02 = $175/hr CAD.
- **Assumed_Project_Parameters.csv**: Referenced for context only; no direct pricing impact on DEL-01-02.

## Dependency Context

Dependencies.csv for DEL-01-02 contains 18 EXECUTION-class dependencies (E01-E18). This deliverable depends on ALL other packages (PKG-002 through PKG-010) and all PKG-001 deliverables being complete before PDF assembly can begin. This confirms the Tier 4 (final) status. Dependencies inform sequencing but do not affect pricing.
