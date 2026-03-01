# Run Context — EST_DEL-009-01_2026-02-27_0547

| Field | Value |
|-------|-------|
| **RunID** | EST_DEL-009-01_2026-02-27_0547 |
| **AsOf** | 2026-02-27T05:47Z |
| **Scope** | DEL-009-01 (Development Permit Application & Approval) |
| **ScopeResolvedSummary** | 1 deliverable in PKG-009 (Permitting & Regulatory Compliance) |
| **BASIS_OF_ESTIMATE** | PARAMETRIC |
| **CURRENCY** | CAD |
| **PRICE_SOURCES** | Professional_Staff_Rates.csv, Level_of_Effort.csv, Assumed_Project_Parameters.csv |
| **DECOMPOSITION_PATH** | _Decomposition/WDMLRL_Decomposition_Claude.md |
| **FALLBACK_POLICY** | ALLOW_PARAMETRIC |
| **ALLOW_MIXED_METHODS** | TRUE |
| **UPDATE_LATEST_POINTER** | FALSE |
| **Rounding** | NONE |
| **OUTPUT_LABEL** | DEL-009-01 |

## Resolved Paths

- **RUN_ROOT:** `/Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude`
- **ESTIMATES_ROOT:** `/Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/_Estimates`
- **Deliverable folder:** `PKG-009_Permitting & Regulatory Compliance/1_Working/DEL-009-01_Development-Permit/`
- **Snapshot folder:** `_Estimates/EST_DEL-009-01_2026-02-27_0547/`

## Documents Read

| Document | Status |
|----------|--------|
| _CONTEXT.md | Read |
| Datasheet.md | Read |
| Specification.md | Read |
| Guidance.md | Read |
| Procedure.md | Read |

## Warnings

- Level_of_Effort.csv provides only 2 roles (R-01 Project Manager, R-08 Cost Estimator) totalling 10 hours for DEL-009-01. The four documents describe additional priceable activities (permitting specialist coordination, document control, pre-application consultation) that are not represented in the LoE model. Parametric estimates are applied for these additional items per FALLBACK_POLICY=ALLOW_PARAMETRIC.
- Permit fee is explicitly excluded from Proponent scope (County pays per R-01 §3.3.1 and REQ-009-01-009).
