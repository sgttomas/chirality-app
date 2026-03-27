# Run Context

| Field | Value |
|---|---|
| **RunID** | EST_DEL-003-01_2026-03-26_1400 |
| **AsOf** | 2026-03-26T14:00:00-06:00 |
| **Scope** | DEL-003-01 (Preliminary Mechanical Design) |
| **ScopeResolvedSummary** | 1 deliverable, 1 package (PKG-003 Mechanical Design) |
| **BASIS_OF_ESTIMATE** | RATE_TABLE |
| **CURRENCY** | CAD |
| **PRICE_SOURCES** | PriceSources/ (full directory — see Resolved Paths below) |
| **DECOMPOSITION_PATH** | _Decomposition/WDMLRL_Decomposition_Claude.md (R2 — 2026-03-26, post-SCA-001) |
| **DEPENDENCY_SOURCES** | AUTO (DEL-003-01/Dependencies.csv) |
| **FALLBACK_POLICY** | ALLOW_ALLOWANCE |
| **ALLOW_MIXED_METHODS** | TRUE |
| **UPDATE_LATEST_POINTER** | FALSE |
| **Rounding** | NONE |
| **OUTPUT_LABEL** | DEL-003-01 |

## Resolved Paths

| Item | Path |
|---|---|
| RUN_ROOT | /Users/ryan/ai-env/projects/chirality-app/examples/AB-2026-01424-WDMLRL-2026-Claude |
| ESTIMATES_ROOT | {RUN_ROOT}/_Estimates |
| Snapshot | {ESTIMATES_ROOT}/EST_DEL-003-01_2026-03-26_1400 |
| Deliverable Folder | {RUN_ROOT}/PKG-003_Mechanical Design/1_Working/DEL-003-01_Preliminary-Design |
| Price Sources Root | {RUN_ROOT}/_EstimatePrep/EPREP_SCAFFOLD_WDMLRL_2026-02-26_2035/PriceSources/ |
| PS-STAFF | PriceSources/Professional_Staff_Rates.csv |
| PS-LOE | PriceSources/Level_of_Effort.csv |
| PS-PARAMS | PriceSources/Assumed_Project_Parameters.csv |
| PS-DF | PriceSources/Professional_Design_Fees.csv |
| PS-MS | PriceSources/Mechanical_System_Rates.csv |
| PS-CBS | PriceSources/CBS_Taxonomy.csv |
| Decomposition | {RUN_ROOT}/_Decomposition/WDMLRL_Decomposition_Claude.md |
| Dependencies | {RUN_ROOT}/PKG-003_Mechanical Design/1_Working/DEL-003-01_Preliminary-Design/Dependencies.csv |

## Prior Snapshot

| Field | Value |
|---|---|
| Prior RunID | EST_DEL-003-01_2026-02-26_2232 |
| Prior Total | $10,170 CAD |
| Prior Basis | PARAMETRIC |
| Refresh Trigger | SCA-001 (Addenda 2, 3, 4 incorporated into decomposition R2) |

## SCA-001 Impact Assessment (DEL-003-01)

| Change | Source | Impact on DEL-003-01 |
|---|---|---|
| Natural gas supply parameters now defined: 2-inch PVC pipe at 50 PSI constant pressure | Add. 3, Q8 | Resolves prior blocker C-001 (gas availability TBD). Gas supply is now a known parameter for heating system design. Design effort (hours) unchanged -- the Mechanical Engineer still performs the same preliminary design activities. |
| Gas pipeline relocation is County responsibility (not contractor cost) | Add. 3, Q8 | No impact on DEL-003-01. Gas pipeline relocation was always PKG-018 scope (SOW-0080). Confirmation that County bears this cost removes it from contractor estimate but was never in DEL-003-01 (design services deliverable). |

**Net pricing impact:** $0 change. Labour hours and rates unchanged. Total remains $10,170 CAD.

## CBS Mapping Rule

CBS codes assigned using CBS_Taxonomy.csv (PS-CBS). Role Category from Professional_Staff_Rates.csv maps as follows:
- Management category roles (R-01 Project Manager, R-08 Cost Estimator) -> CBS-02 (Professional Services > Project Management)
- Design category roles (R-13 BIM Technician, R-15 Mechanical Engineer) -> CBS-01 (Professional Services > Design & Engineering)

## Warnings

- [INFO] BASIS_OF_ESTIMATE changed from PARAMETRIC (prior run) to RATE_TABLE (this run). The underlying pricing method is the same: LOE hours x staff hourly rates from a rate table. The reclassification reflects the brief's instruction; the rate table (Professional_Staff_Rates.csv) is the primary pricing evidence.
- [INFO] ALLOW_MIXED_METHODS=TRUE but not triggered; all lines use RATE_TABLE method.
- [INFO] FALLBACK_POLICY=ALLOW_ALLOWANCE but not triggered; all items priced from primary rate table sources.
