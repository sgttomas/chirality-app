# Run Context -- EST_DEL-08-01_2026-02-18_1400

## Run Identification

- **RunID:** EST_DEL-08-01_2026-02-18_1400
- **AsOf:** 2026-02-18T14:00:00-07:00
- **Agent:** ESTIMATING (Type 2)

---

## Brief Inputs (as provided)

- **SCOPE:** DEL-08-01
- **RUN_ROOT:** `/Users/ryan/ai-env/projects/chirality-app-test/test/execution-6c/PKG-08_Schedule & Milestones/1_Working/DEL-08-01_DetailedProjectSchedule`
- **ESTIMATES_ROOT:** `/Users/ryan/ai-env/projects/chirality-app-test/test/execution-6c/_Estimates/`
- **BASIS_OF_ESTIMATE:** RATE_TABLE
- **CURRENCY:** CAD
- **DECOMPOSITION_PATH:** `/Users/ryan/ai-env/projects/chirality-app-test/test/execution-6c/_Decomposition/Penhold_PSB_Project_Decomposition_Final_AddendumIntegrated_v1.md`
- **DEPENDENCY_SOURCES:** AUTO
- **PRICE_SOURCES:**
  1. `/Users/ryan/ai-env/projects/chirality-app-test/test/execution-6c/_PriceSources/Professional_Staff_Rates.csv`
  2. `/Users/ryan/ai-env/projects/chirality-app-test/test/execution-6c/_PriceSources/Level_of_Effort.csv`
  3. `/Users/ryan/ai-env/projects/chirality-app-test/test/execution-6c/_PriceSources/Assumed_Project_Parameters.csv`
- **OUTPUT_LABEL:** DEL-08-01
- **UPDATE_LATEST_POINTER:** FALSE
- **FALLBACK_POLICY:** STRICT
- **ALLOW_MIXED_METHODS:** FALSE
- **ROUNDING:** DOLLAR

---

## Resolved Defaults

| Parameter | Resolved Value |
|---|---|
| RunID | EST_DEL-08-01_2026-02-18_1400 |
| AsOf | 2026-02-18T14:00:00-07:00 |
| Scope | DEL-08-01 (single deliverable) |
| ScopeResolvedSummary | 1 deliverable in scope; 0 excluded; 0 blocked |
| BASIS_OF_ESTIMATE | RATE_TABLE (validated) |
| CURRENCY | CAD |
| PRICE_SOURCES | 3 files resolved and readable (see Source_Index.md) |
| DECOMPOSITION_PATH | Located and read successfully |
| DEPENDENCY_SOURCES | AUTO -- Dependencies.csv found at deliverable path |
| FALLBACK_POLICY | STRICT |
| ALLOW_MIXED_METHODS | FALSE |
| UPDATE_LATEST_POINTER | FALSE |
| Rounding | DOLLAR |

---

## Scope Resolution

| DeliverableID | PackageID | Path | InScope | Notes |
|---|---|---|---|---|
| DEL-08-01 | PKG-08 | PKG-08_Schedule & Milestones/1_Working/DEL-08-01_DetailedProjectSchedule | TRUE | Detailed Project Schedule; Tier T2 |

---

## CBS Mapping Rule

CBS codes are assigned deterministically using the following rule:
- `CBS = PROF-SCHED` for professional scheduling services (Gantt production, critical path analysis, schedule narrative)
- `CBS = PROF-PM` for project management coordination hours contributing to DEL-08-01
- `CBS = PROF-CM` for construction management input hours to schedule

This follows the pattern: `PROF-{discipline}` where discipline is derived from the `Category` field in Professional_Staff_Rates.csv.

---

## Warnings

- None.
