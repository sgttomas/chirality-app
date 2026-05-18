# Run Context

## Run Identity

| Field | Value |
|---|---|
| RunID | EST_DEL-01-06_2026-02-18_2100 |
| AsOf | 2026-02-18T21:00:00-07:00 |
| PriorRunID | EST_DEL-01-06_2026-02-18_1030 |
| RevisionType | TBD resolution pass (ORCHESTRATOR-directed) |
| AgentType | ESTIMATING (Type 2 Task Agent) — revision by ORCHESTRATOR |

## Scope

| Field | Value |
|---|---|
| Scope (as provided) | DEL-01-06 |
| ScopeResolvedSummary | 1 deliverable in scope; 0 excluded; 0 blocked |
| DeliverableID | DEL-01-06 |
| DeliverableName | Site Supervision, Logistics & Housekeeping |
| PackageID | PKG-001 |

## Configuration

| Parameter | Value |
|---|---|
| BASIS_OF_ESTIMATE | RATE_TABLE |
| CURRENCY | CAD |
| FALLBACK_POLICY | STRICT (overridden to ALLOW_ALLOWANCE for TBD resolution per human authorization) |
| ALLOW_MIXED_METHODS | TRUE (RATE_TABLE + ALLOWANCE; authorized by human for TBD resolution) |
| UPDATE_LATEST_POINTER | FALSE |
| ROUNDING | DOLLAR |
| OUTPUT_LABEL | DEL-01-06 |

## Revision Notes

This snapshot revises EST_DEL-01-06_2026-02-18_1030 to resolve 2 TBD line items. The prior run applied STRICT fallback, leaving L-0106-003 (temp facilities/fencing) and L-0106-004 (site cleaning) at TBD. The human authorized ORCHESTRATOR to resolve TBDs using parametric allowances.

**Changes from prior run:**
- L-0106-003: TBD → $35,000 CAD (ALLOWANCE; parametric estimate for temp facilities/fencing)
- L-0106-004: TBD → $25,000 CAD (ALLOWANCE; parametric estimate for site cleaning)
- ALLOW_MIXED_METHODS changed from FALSE to TRUE
- Total changed from $203,700 → $263,700

## CBS Mapping Rule

Carried forward from prior run. 01-CMGT for labor; 01-SITE for non-labor site costs.
