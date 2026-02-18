# Run Context

## Run Identity

- **RunID:** EST_DEL-02-06_2026-02-18_1500
- **AsOf:** 2026-02-18T15:00:00-07:00
- **Agent:** ESTIMATING (Type 2)

## Brief Inputs (resolved)

- **Scope:** DEL-02-06 only (PKG-002)
- **ScopeResolvedSummary:** 1 deliverable in scope; 0 excluded; 0 blocked
- **BASIS_OF_ESTIMATE:** RATE_TABLE (validated)
- **CURRENCY:** CAD
- **ROUNDING:** DOLLAR
- **FALLBACK_POLICY:** STRICT
- **ALLOW_MIXED_METHODS:** FALSE
- **UPDATE_LATEST_POINTER:** FALSE
- **OUTPUT_LABEL:** DEL-02-06

## Resolved Paths

- **ESTIMATES_ROOT:** /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6a/_Estimates/
- **DECOMPOSITION_PATH:** /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6a/_Decomposition/Penhold_PSB_Project_Decomposition_FINAL_v1.0_PHASE7.md (loaded; v1.0 Phase 7)
- **DEPENDENCY_SOURCES:** AUTO -- loaded Dependencies.csv from DEL-02-06 deliverable folder (19 rows; v3.1)

## Price Sources (resolved)

| # | Path | Type | Status |
|---|------|------|--------|
| 1 | _PriceSources/Electrical_System_Rates.csv | Rate table | Loaded; 15 rows (ES-01 through ES-14) |
| 2 | _PriceSources/Equipment_Pricing.csv | Rate table | Loaded; 15 rows; EQ-11 and EQ-12 relevant to DEL-02-06 |
| 3 | _PriceSources/Construction_Labour_Rates.csv | Rate table | Loaded; 15 rows; T-07 (Electrician) relevant |
| 4 | _PriceSources/Professional_Design_Fees.csv | Rate table | Loaded; 8 rows; DF-05 (Electrical) relevant |
| 5 | _PriceSources/Assumed_Project_Parameters.csv | Parameters | Loaded; 29 rows; PP-05 through PP-08, PP-11, PP-12, PP-27 used |

## Area Breakdown Assumption (CBS mapping rule)

The main PSB (18,000 sf per PP-05) is split into two cost zones for electrical rate application:

- **Institutional/office/shared areas:** 5,200 sf (18,000 sf total - 12,800 sf bay area)
- **Apparatus/shop bay areas:** 12,800 sf (8 bays x ~1,600 sf/bay estimated)

This split is an assumption (ASM-001) documented in Assumptions_Log.md. It drives the allocation between ES-01 (institutional power) / ES-03 (institutional lighting) and ES-02 (bay power) / ES-04 (bay lighting).

## CBS Mapping Rule

No explicit CBSHint was provided in the decomposition for DEL-02-06. CBS codes are assigned deterministically based on the Electrical_System_Rates.csv Category column:

| CBS Code | Description | Mapping Rule |
|----------|------------|--------------|
| 26-00 | Electrical (general) | Default for power distribution, service entrance |
| 26-50 | Lighting | LED lighting systems, emergency lighting |
| 27-00 | IT/Telecom | Data drops, backbone, displays |
| 27-50 | PA/Special Systems | PA system |
| 26-90 | Electrical Design | Professional design fees |
| 26-80 | Electrical Commissioning | System-specific commissioning labor |
| 26-10 | Solar-Ready Provisions | Solar electrical provisions |

This mapping follows CSI MasterFormat Division 26/27 conventions. Documented as decision DEC-RC-01 in Decision_Log.md.

## Warnings

- None critical. Run proceeded with full pricing source coverage for all in-scope line items.
