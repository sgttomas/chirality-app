# Run Context

| Field | Value |
|---|---|
| **RunID** | EST_DEL-02-05_2026-02-18_2200 |
| **AsOf** | 2026-02-18T22:00:00-07:00 |
| **Scope** | DEL-02-05 |
| **ScopeResolvedSummary** | 1 deliverable in scope; 0 excluded; 0 blocked |
| **BASIS_OF_ESTIMATE** | RATE_TABLE |
| **CURRENCY** | CAD |
| **PRICE_SOURCES** | Professional_Staff_Rates.csv; Level_of_Effort.csv; Assumed_Project_Parameters.csv |
| **DECOMPOSITION_PATH** | `_Decomposition/Penhold_PSB_Project_Decomposition_v2.md` (v2.3 FINAL) |
| **DEPENDENCY_SOURCES** | AUTO (read `DEL-02-05/Dependencies.csv`) |
| **FALLBACK_POLICY** | STRICT |
| **ALLOW_MIXED_METHODS** | FALSE |
| **UPDATE_LATEST_POINTER** | FALSE |
| **Rounding** | DOLLAR |
| **Warnings** | None |

## Resolved Inputs

### Scope

DEL-02-05 -- Electrical/IT Concept Narrative, within PKG-002 (Conceptual Design).

### CBS Mapping Rule

CBS is assigned deterministically as `PROFESSIONAL_SERVICES` for all labour-hour line items on proposal-production deliverables. This is a professional services fee estimate (hours to produce the narrative), not a construction cost estimate.

### Price Sources Detail

1. **Professional_Staff_Rates.csv** -- 30 roles with hourly rates in CAD. Basis: MARKET. Confidence: MEDIUM. Used as the rate table for all line items.
2. **Level_of_Effort.csv** -- 73 rows mapping deliverables to roles and estimated hours. Basis: PARAMETRIC. Used as the quantity source for hours per role per deliverable.
3. **Assumed_Project_Parameters.csv** -- 29 project parameters. Used for context only (no direct pricing from this file for DEL-02-05).

### Dependency Evidence

Dependencies.csv for DEL-02-05 loaded successfully. 15 dependency rows found:
- 4 ANCHOR rows (package, scope, objective traceability)
- 4 UPSTREAM PREREQUISITE/INTERFACE rows (DEL-02-01, DEL-02-02, DEL-02-03, DEL-02-04)
- 3 DOWNSTREAM HANDOVER rows (DEL-03-05, DEL-04-03, DEL-05-04)
- 3 UPSTREAM CONSTRAINT rows (Addendum 03, RFP 7.1.1, Functional Program)
- 1 additional UPSTREAM INTERFACE row (RFP Appendix B)

No blocking dependencies identified for estimating purposes. All upstream dependencies are information prerequisites that affect content, not pricing.
