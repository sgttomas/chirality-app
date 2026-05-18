# Decision_Log — EST_DEL-018-03_2026-02-27_0834

## Defaults Applied

| DecisionID | Decision | Rationale |
|------------|----------|-----------|
| DEC-001 | Rounding set to NONE (default) | No rounding policy specified in brief; default applied per protocol |
| DEC-002 | RUN_TIMESTAMP generated at runtime (2026-02-27T08:34:00Z) | Not provided in brief; auto-generated |
| DEC-003 | UPDATE_LATEST_POINTER = FALSE | As specified in brief; no pointer files modified |

## Scope Resolution Decisions

| DecisionID | Decision | Rationale |
|------------|----------|-----------|
| DEC-004 | Scope resolved to single deliverable DEL-018-03 (Gravel Driving Surface) under PKG-018 | SCOPE = DEL-018-03 in brief; confirmed via _CONTEXT.md and Decomposition |
| DEC-005 | Topsoil stripping (ITM-007 / L-007) included in Items.csv at $0 for completeness but EXCLUDED from pricing | Topsoil stripping is DEL-018-01 scope per _DEPENDENCIES.md and SOW-0075; not DEL-018-03 |
| DEC-006 | Aggregate supply (ITM-009 / L-009) included in Items.csv at $0 for completeness but EXCLUDED from pricing | Owner-supplied per SOW-0203, RFP §3.3.1, and Appendix B note; not Contractor scope |
| DEC-007 | Proof-rolling (ITM-014 / L-014) included as conditional allowance | REQ-018-03-11 identifies proof-rolling as subject to civil engineer determination; included per ALLOW_PARAMETRIC fallback policy |

## Fallback Uses

| DecisionID | Decision | Rationale |
|------------|----------|-----------|
| DEC-008 | All 17 priced line items use Method=PARAMETRIC | Consistent with BASIS_OF_ESTIMATE=PARAMETRIC; no fallback to other methods required |
| DEC-009 | ALLOW_MIXED_METHODS not exercised | All lines are PARAMETRIC; no mixed methods needed for this single-deliverable scope |

## Pricing Integration Decisions

| DecisionID | Decision | Rationale |
|------------|----------|-----------|
| DEC-010 | PS-01 rate ($40/m2) applied to gravel placement | PS-01 description "Gravel driving surface (base + place)" directly matches DEL-018-03 scope; rate is RecommendedRate from Paving_Surfacing_Rates.csv |
| DEC-011 | EC-03 rate ($4.00/m2) applied to both subgrade compaction and gravel compaction | EC-03 "Compaction / proof roll allowance" is applicable to both subgrade and placed gravel; applied twice as separate line items |
| DEC-012 | Construction labour (T-07, T-08) hours estimated parametrically | No level-of-effort data for construction trades in Level_of_Effort.csv (which covers professional staff only); hours estimated from area and standard productivity assumptions |
| DEC-013 | Final grading rate set at $5/m2 as parametric estimate | No direct rate in price sources for motor grader finish pass; derived from equipment operator productivity and labour rates as a parametric estimate |
