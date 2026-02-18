# Run Context

## Run Identity

| Field | Value |
|---|---|
| **RunID** | EST_DEL-03-05_2026-02-18_2000 |
| **AsOf** | 2026-02-18T20:00:00-07:00 |
| **Agent** | ESTIMATING (Type 2 Task Agent) |

## Scope

| Field | Value |
|---|---|
| **Scope (as provided)** | DEL-03-05 |
| **ScopeResolvedSummary** | 1 deliverable in scope; 0 excluded; 0 blocked |
| **DeliverableID** | DEL-03-05 |
| **DeliverableName** | Environmental Constraints, Flood Hazard & Regulatory Compliance |
| **PackageID** | PKG-003 |
| **PackageName** | Site & Civil Works |

## Configuration

| Parameter | Value |
|---|---|
| **BASIS_OF_ESTIMATE** | RATE_TABLE (validated) |
| **CURRENCY** | CAD |
| **FALLBACK_POLICY** | ALLOW_ALLOWANCE |
| **ALLOW_MIXED_METHODS** | TRUE |
| **UPDATE_LATEST_POINTER** | FALSE |
| **ROUNDING** | DOLLAR |
| **OUTPUT_LABEL** | DEL-03-05 |

## Resolved Paths

| Input | Resolved Path |
|---|---|
| **RUN_ROOT** | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6a |
| **ESTIMATES_ROOT** | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6a/_Estimates/ |
| **DECOMPOSITION_PATH** | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6a/_Decomposition/Penhold_PSB_Project_Decomposition_FINAL_v1.0_PHASE7.md |
| **DEPENDENCY_SOURCES** | AUTO -- read from deliverable folder Dependencies.csv (19 rows; v3.1 schema) |
| **Deliverable Folder** | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6a/PKG-003_Site & Civil Works/1_Working/DEL-03-05_Environmental Constraints, Flood Hazard & Regulatory Compliance/ |

## PRICE_SOURCES (resolved)

| # | Path | Type | Relevance to DEL-03-05 |
|---|---|---|---|
| 1 | _PriceSources/Fees_Permits_Insurance.csv | Rate table / allowance | PRIMARY -- FP-16, FP-17, FP-18 directly applicable (environmental consultant fees, AEPA application, ESC plan) |
| 2 | _PriceSources/Professional_Design_Fees.csv | Rate table (percentage-based) | SECONDARY -- DF-07 cross-references FP-17 for environmental consulting |
| 3 | _PriceSources/Assumed_Project_Parameters.csv | Parameter table | SUPPORTING -- project-level parameters for context |
| 4 | _PriceSources/Earthwork_Civil_Rates.csv | Rate table | NOT APPLICABLE -- earthwork costs belong to DEL-03-02 per cost ownership rules |
| 5 | _PriceSources/Paving_Surfacing_Rates.csv | Rate table | NOT APPLICABLE -- paving costs belong to DEL-03-03 |
| 6 | _PriceSources/Underground_Utility_Rates.csv | Rate table | NOT APPLICABLE -- utility costs belong to DEL-03-04 |
| 7 | _PriceSources/Construction_Labour_Rates.csv | Rate table | NOT APPLICABLE -- physical construction labour belongs to executing deliverables |

## CBS Mapping Rule

CBS codes for DEL-03-05 are assigned using the following deterministic rule:
- **CBS = PROF_SERVICES** for professional consulting fees (environmental consultant, flood hazard assessment, ESC plan preparation)
- **CBS = REGULATORY_FEES** for regulatory application fees (AEPA Water Act application)
- **CBS = REGULATORY_FEES** for regulatory replacement fees (ABWRET-A wetland replacement fee)
- **CBS = ALLOWANCE** for items priced using ALLOWANCE method where fee schedules are uncertain

This mapping is derived from the deliverable substance description in the brief: "Professional Services + Compliance."

## Cost Ownership Rules Applied

Per the brief's cost ownership rules for PKG-003:
- Environmental compliance COSTS (consultant fees, regulatory fees) are priced here in DEL-03-05
- Environmental constraint INTEGRATION into design carries no extra cost (design constraint, not a priced item)
- Stormwater management infrastructure costs belong to DEL-03-02, NOT DEL-03-05
- Clearing, stripping, earthworks costs belong to DEL-03-02, NOT DEL-03-05
- Any physical construction work driven by environmental constraints is priced in the executing deliverable, NOT here

## External Gate

| Gate | Status | Impact |
|---|---|---|
| AEPA Water Act approval | PENDING | Earthwork quantities near waterway carried as conservative assumption + flagged; setback distances are TBD |

## Warnings

- [WARNING] AEPA Water Act approval is PENDING (DEP-3505-E06, DEP-3505-E12). Setback distances remain TBD. This does not block professional services pricing but constrains confidence on scope completeness.
- [WARNING] MIXED_METHODS in use: RATE_TABLE (primary) + ALLOWANCE (fallback for uncertain regulatory fees). Authorized by ALLOW_MIXED_METHODS=TRUE and FALLBACK_POLICY=ALLOW_ALLOWANCE.
