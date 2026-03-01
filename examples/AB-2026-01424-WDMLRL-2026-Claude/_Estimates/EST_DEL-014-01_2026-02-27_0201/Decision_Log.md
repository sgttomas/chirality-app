# Decision_Log.md — EST_DEL-014-01_2026-02-27_0201

## Defaults Applied

| DecisionID | Decision | Rationale |
|---|---|---|
| DEC-001 | Rounding set to NONE (default) | No rounding parameter provided in brief |
| DEC-002 | UPDATE_LATEST_POINTER = FALSE | Per brief; no pointer file modified |
| DEC-003 | Mixed methods permitted (PARAMETRIC + ALLOWANCE) | ALLOW_MIXED_METHODS = TRUE per brief |
| DEC-004 | FALLBACK_POLICY = ALLOW_PARAMETRIC | Per brief; allows parametric pricing where basis evidence is incomplete |

## Scope Resolution Decisions

| DecisionID | Decision | Rationale |
|---|---|---|
| DEC-010 | Scope resolved to single deliverable DEL-014-01 | SCOPE = DEL-014-01 per brief; confirmed against decomposition (PKG-014, SOW-0041, SOW-0042) |
| DEC-011 | Out-of-scope items excluded per Specification | DEL-014-03 (bulk water fill), DEL-014-02 (septic), DEL-014-04 (floor drains), DEL-014-05 (emergency shower), DEL-015-01 (electrical supply), PKG-006 (plumbing design) all explicitly out of scope |
| DEC-012 | Emergency shower piping excluded from estimate | Per Specification Out of Scope (DEL-014-05); unresolved conflict CONF-014-01-03 noted as warning |

## Pricing Decisions

| DecisionID | Decision | Rationale |
|---|---|---|
| DEC-020 | Cistern vessel priced using UU-05 allowance ($65,000) | Direct match in Underground_Utility_Rates.csv; only available pricing evidence for cistern; confidence LOW |
| DEC-021 | Distribution pump priced at $8,500 parametric | No pump pricing in PRICE_SOURCES; parametric estimate based on industrial centrifugal pump 100 LPM class; FALLBACK_POLICY permits |
| DEC-022 | Distribution piping priced at $12,000 parametric | No interior piping rate table; adapted from UU-01 underground water line rate ($130/m) with reduction factor for interior; estimated ~60m total run |
| DEC-023 | Pipe supports/hangers/valves at $4,500 (35% of piping) | Standard parametric factor for pipe appurtenances; no specific rate table available |
| DEC-024 | Plumber labour estimated at 96 hours total | Parametric: 80 hr installation (2 plumbers x 5 days) + 16 hr testing/commissioning (2 plumbers x 1 day) |
| DEC-025 | Freeze protection at $5,000 parametric allowance | No rate table; parametric estimate for insulation + heat trace on ~40m of vulnerable piping |
| DEC-026 | Permit fee at $1,500 parametric | No Alberta permit fee schedule in PRICE_SOURCES; parametric for industrial plumbing permit |
| DEC-027 | Management LOE priced per PS-STAFF x PS-LOE | 6 roles totaling 38 hours at rates from Professional_Staff_Rates.csv; hours from Level_of_Effort.csv DEL-014-01 rows |

## Fallback Uses

| DecisionID | Line(s) | Fallback Type | Rationale |
|---|---|---|---|
| DEC-030 | DET-001 | ALLOWANCE (from UU-05) | Cistern priced as ALLOWANCE because UU-05 is classified as ALLOWANCE in source; permitted by ALLOW_MIXED_METHODS=TRUE |
| DEC-031 | DET-002 through DET-014 | PARAMETRIC (no direct source) | Multiple items priced parametrically where no direct pricing evidence exists in PRICE_SOURCES; permitted by FALLBACK_POLICY=ALLOW_PARAMETRIC |
