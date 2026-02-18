# Run Context — EST_DEL-02-07_2026-02-18_1600

## Run Identity

| Field | Value |
|---|---|
| **RunID** | EST_DEL-02-07_2026-02-18_1600 |
| **AsOf** | 2026-02-18T16:00:00-07:00 |
| **Agent** | ESTIMATING (Type 2 Task Agent) |

## Scope

| Field | Value |
|---|---|
| **Scope (as provided)** | DEL-02-07 only (PKG-002) |
| **ScopeResolvedSummary** | 1 deliverable in scope; 0 blocked; 0 excluded |
| **Deliverables** | DEL-02-07 (Emergency Power & Backup Generator) |
| **Package** | PKG-002 (Main Public Services Building) |

## Configuration

| Parameter | Value |
|---|---|
| **BASIS_OF_ESTIMATE** | QUOTE |
| **CURRENCY** | CAD |
| **FALLBACK_POLICY** | ALLOW_ALLOWANCE |
| **ALLOW_MIXED_METHODS** | TRUE |
| **ROUNDING** | DOLLAR |
| **UPDATE_LATEST_POINTER** | FALSE |
| **OUTPUT_LABEL** | DEL-02-07 |

## Resolved Paths

| Input | Resolved Path |
|---|---|
| **RUN_ROOT** | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6a |
| **ESTIMATES_ROOT** | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6a/_Estimates/ |
| **DECOMPOSITION_PATH** | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6a/_Decomposition/Penhold_PSB_Project_Decomposition_FINAL_v1.0_PHASE7.md |
| **DEPENDENCY_SOURCES** | AUTO (resolved to DEL-02-07 Dependencies.csv) |

## Price Sources (resolved)

| Source File | Type | Relevant Items |
|---|---|---|
| Equipment_Pricing.csv | PARAMETRIC | EQ-04 (generator system); EQ-05 (ATS, reference only — included in EQ-04) |
| Electrical_System_Rates.csv | PARAMETRIC | No direct generator-specific line items; general electrical rates for reference |
| Construction_Labour_Rates.csv | RATE_TABLE | T-07 (Electrician); T-13 (Millwright); T-14 (Crane Operator) |
| Professional_Design_Fees.csv | PARAMETRIC | DF-05 (Electrical engineering design fees) |
| Assumed_Project_Parameters.csv | ASSUMPTION | PP-26 (72-hr runtime); PP-05 (building footprint for reference) |

## CBS Mapping Rule

No explicit `CBSHint` is present in the decomposition for DEL-02-07. CBS codes are assigned using a deterministic discipline-based mapping:

| CBS | Meaning | Applied To |
|---|---|---|
| 26-EMRG-GEN | Emergency Power — Generator Equipment | Genset, ATS, fuel tank, pad, exhaust |
| 26-EMRG-DIST | Emergency Power — Distribution | Distribution from generator to essential loads |
| 26-EMRG-DOOR | Emergency Power — Door Backup Integration | Overhead door backup mechanism integration |
| 26-EMRG-DES | Emergency Power — Design | Generator-specific electrical engineering design |

"26" = CSI Division 26 (Electrical); "EMRG" = Emergency Power sub-classification.

## Basis-of-Estimate Note

The brief specifies `BASIS_OF_ESTIMATE=QUOTE`. However, no vendor quote exists for this deliverable. Per `FALLBACK_POLICY=ALLOW_ALLOWANCE` and `ALLOW_MIXED_METHODS=TRUE`, all line items are priced using the ALLOWANCE method derived from parametric pricing in Equipment_Pricing.csv and Assumed_Project_Parameters.csv. All items are flagged as requiring vendor quote replacement before the estimate is finalized.

## Warnings

- [WARNING] No vendor quote available for generator system. All pricing uses ALLOWANCE fallback from parametric sources.
- [WARNING] PP-26 (72-hour runtime) is an unconfirmed Owner assumption. Fuel tank sizing depends on this. Owner confirmation required.
- [WARNING] AHJ ruling on seismic anchorage (DEP-0207-E009) is PENDING. May affect generator pad and installation costs.
- [WARNING] Multiple upstream prerequisites (DEL-02-04, DEL-02-06, DEL-03-01, DEL-03-04) have TBD satisfaction status.
