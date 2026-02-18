# Brief — AGG_Estimate_Collation_2026-02-18_2359

## Verbatim Brief

```
PURPOSE: Estimate_Collation
PIPELINE_ID: Proposal_Production_Estimate
EXECUTION_ROOT: /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6b
AGGREGATION_ROOT: /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6b/_Aggregation
CURRENCY: CAD
BASE_YEAR: 2024

SCOPE: All 38 deliverables (DEL-01-01 through DEL-10-02)

WHERE_TO_LOOK: /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6b/_Estimates/

ESTIMATE_SNAPSHOT_PATHS: 40 snapshot directories across 38 deliverables
  (DEL-01-01 through DEL-10-02; see full list in INIT-TASK)
```

## Normalized Brief

| Field | Value |
|-------|-------|
| PURPOSE | Estimate_Collation |
| PIPELINE_ID | Proposal_Production_Estimate |
| EXECUTION_ROOT | test/execution-6b |
| AGGREGATION_ROOT | test/execution-6b/_Aggregation |
| CURRENCY | CAD |
| BASE_YEAR | 2024 |
| SCOPE | 38 deliverables across 10 packages |
| WHERE_TO_LOOK | test/execution-6b/_Estimates/ |
| SNAPSHOT_COUNT | 40 directories (38 unique deliverables; DEL-01-04 and DEL-01-05 have dual-nature lines) |

## Aggregation Strategy

Per BOE Section 7, this collation must produce:
1. Package-level rollups (10 packages + PKG-001 construction pricing + PKG-001 financial allowances as separate categories)
2. Project-level totals (Total Proposal Production Cost, Construction Pricing Content, Financial Allowances, Grand Total)
3. Effort matrix (hours by role x package)
4. Evaluation-weight-adjusted view (cost per evaluation point)
