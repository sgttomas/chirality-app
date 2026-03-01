# Run Context — EST_DEL-007-02_2026-02-27_0600

| Field | Value |
|---|---|
| **RunID** | EST_DEL-007-02_2026-02-27_0600 |
| **AsOf** | 2026-02-27T06:00:00-07:00 |
| **Scope** | DEL-007-02 |
| **ScopeResolvedSummary** | 1 deliverable (DEL-007-02 Landscape Site Plans) under PKG-007 Landscape Architectural Design |
| **BASIS_OF_ESTIMATE** | PARAMETRIC |
| **CURRENCY** | CAD |
| **PRICE_SOURCES** | 1. Professional_Staff_Rates.csv; 2. Level_of_Effort.csv; 3. Assumed_Project_Parameters.csv; 4. Professional_Design_Fees.csv |
| **DECOMPOSITION_PATH** | /Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/_Decomposition/WDMLRL_Decomposition_Claude.md |
| **FALLBACK_POLICY** | ALLOW_PARAMETRIC |
| **ALLOW_MIXED_METHODS** | TRUE |
| **UPDATE_LATEST_POINTER** | FALSE |
| **Rounding** | NONE (default) |
| **OUTPUT_LABEL** | DEL-007-02 |
| **Warnings** | None |

## Resolved Paths

- **ESTIMATES_ROOT**: `_Estimates/`
- **Snapshot Folder**: `_Estimates/EST_DEL-007-02_2026-02-27_0600/`
- **Deliverable Path**: `PKG-007_Landscape Architectural Design/1_Working/DEL-007-02_Landscape-Plans/`

## Documents Read

| Document | Status |
|---|---|
| _CONTEXT.md | Read |
| Datasheet.md | Read |
| Specification.md | Read |
| Guidance.md | Read |
| Procedure.md | Read |
| Decomposition (WDMLRL_Decomposition_Claude.md) | Read — PKG-007 section |

## Price Sources Indexed

| Source | Type | Status |
|---|---|---|
| Professional_Staff_Rates.csv | Rate Table (hourly rates by role) | Indexed — R-19 Landscape Architect at 135 CAD/hr; R-01 PM at 165 CAD/hr; R-08 Cost Estimator at 135 CAD/hr |
| Level_of_Effort.csv | Parametric LOE model (hours by deliverable and role) | Indexed — DEL-007-02 rows: R-01 (6 hr), R-08 (4 hr), R-19 (70 hr) |
| Assumed_Project_Parameters.csv | Parameter set | Indexed — PP-17 Currency = CAD; PP-10 Floor Area approx 13000 sqft |
| Professional_Design_Fees.csv | Fee percentage model | Indexed — Not directly used for this deliverable (LOE model preferred) |
