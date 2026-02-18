# Run Context

## Run Identity

- **RunID:** EST_DEL-05-04_2026-02-18_1800
- **AsOf:** 2026-02-18T18:00:00
- **Agent:** ESTIMATING (Type 2)

## Brief Inputs (resolved)

| Field | Value |
|---|---|
| **Scope** | DEL-05-04 only (PKG-005) |
| **ScopeResolvedSummary** | 1 deliverable in scope; 0 excluded; 0 blocked |
| **BASIS_OF_ESTIMATE** | QUOTE (validated; note: no vendor quote exists -- fallback to PARAMETRIC per FALLBACK_POLICY) |
| **CURRENCY** | CAD |
| **RUN_ROOT** | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6a |
| **ESTIMATES_ROOT** | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6a/_Estimates/ |
| **DECOMPOSITION_PATH** | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6a/_Decomposition/Penhold_PSB_Project_Decomposition_FINAL_v1.0_PHASE7.md (loaded successfully) |
| **DEPENDENCY_SOURCES** | AUTO (resolved to: DEL-05-04 Dependencies.csv -- 6 rows loaded) |
| **PRICE_SOURCES** | (1) Optional_Items_Pricing.csv; (2) Assumed_Project_Parameters.csv |
| **FALLBACK_POLICY** | ALLOW_ALLOWANCE |
| **ALLOW_MIXED_METHODS** | TRUE |
| **UPDATE_LATEST_POINTER** | FALSE |
| **Rounding** | DOLLAR |
| **OUTPUT_LABEL** | DEL-05-04 |

## CBS Mapping Rule

No explicit `CBSHint` present in decomposition for DEL-05-04. CBS assignment uses the following deterministic rule:

- Camera system equipment + installation -> `26-SECURITY` (Division 26/28 convention: electronic safety and security)
- Monitoring service (annual operating cost) -> `26-SECURITY-MONITORING`

This is a best-effort mapping. No project-level CBS dictionary was provided.

## Warnings

- [WARNING] BASIS_OF_ESTIMATE is QUOTE but no vendor quote exists. All line items priced using PARAMETRIC method via FALLBACK_POLICY=ALLOW_ALLOWANCE + ALLOW_MIXED_METHODS=TRUE. Every line item is flagged for replacement with actual vendor quote.
- [WARNING] Camera count (16 locations) is an assumption (PP-29, LOW confidence). Actual count depends on DEL-02-01 floor plan (dependency DEP-0504-003).
- [WARNING] All pricing is LOW confidence per source file.

## Cost Ownership Rules (from brief)

| Scope Area | Cost Owner | NOT in |
|---|---|---|
| Camera system (all equipment + wiring + installation) | DEL-05-04 | DEL-02-06 |
| Camera system monitoring service (annual) | DEL-05-04 | All others |

Excluded from this estimate (owned by other deliverables):
- IT network infrastructure that cameras connect TO -> DEL-02-06
- Electrical power circuits to camera locations -> DEL-02-06
- Building-mounted exterior lighting -> DEL-02-06
