# Run Context — EST_DEL-04-02_2026-02-18_1100

## Run Identity

| Field | Value |
|---|---|
| **RunID** | EST_DEL-04-02_2026-02-18_1100 |
| **AsOf** | 2026-02-18T11:00:00-07:00 |
| **AgentType** | ESTIMATING (Type 2) |

## Brief Inputs (Resolved)

| Parameter | Value |
|---|---|
| **Scope** | DEL-04-02 |
| **ScopeResolvedSummary** | 1 deliverable in scope; 0 excluded; 0 blocked |
| **BASIS_OF_ESTIMATE** | RATE_TABLE (validated) |
| **CURRENCY** | CAD |
| **PRICE_SOURCES** | See resolved list below |
| **DECOMPOSITION_PATH** | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6a/_Decomposition/Penhold_PSB_Project_Decomposition_FINAL_v1.0_PHASE7.md |
| **DEPENDENCY_SOURCES** | AUTO (resolved to DEL-04-02/Dependencies.csv) |
| **FALLBACK_POLICY** | STRICT |
| **ALLOW_MIXED_METHODS** | FALSE |
| **UPDATE_LATEST_POINTER** | FALSE |
| **Rounding** | DOLLAR |
| **OUTPUT_LABEL** | DEL-04-02 |

## Resolved PRICE_SOURCES

| # | Path | Type | Status |
|---|---|---|---|
| 1 | _PriceSources/Structural_Concrete_Rates.csv | Rate Table | Loaded; 16 items |
| 2 | _PriceSources/Building_Envelope_Rates.csv | Rate Table | Loaded; 15 items |
| 3 | _PriceSources/Equipment_Pricing.csv | Rate Table | Loaded; 15 items |
| 4 | _PriceSources/Construction_Labour_Rates.csv | Rate Table | Loaded; 15 trades |
| 5 | _PriceSources/Assumed_Project_Parameters.csv | Parameters | Loaded; 29 parameters |

## CBS Mapping Rule

CBS codes are assigned using the following deterministic rule for DEL-04-02:
- **08-Doors** — Overhead doors, person doors, and associated hardware (MasterFormat Division 08)
- **03-Concrete** — Concrete aprons at door openings (MasterFormat Division 03)
- **07-Thermal** — Weatherstripping and sealing at door openings (MasterFormat Division 07)

This mapping is based on CSI MasterFormat divisions as a proxy CBS structure, applied consistently for all line items.

## Deliverable Context

| Field | Value |
|---|---|
| **DeliverableID** | DEL-04-02 |
| **Name** | Cold Storage -- Doors, Openings & Hardware |
| **PackageID** | PKG-004 |
| **Package Name** | Cold Storage Building (Unheated, 60'x100') |
| **Scope Coverage** | SOW-0302 |
| **Objective Support** | OBJ-004 |
| **Tier** | T2 |
| **Substance** | Construction + Equipment |

## Cost Ownership Rules (from brief)

- Doors, openings, hardware --> DEL-04-02 (this estimate)
- Door opener electrical feeds --> DEL-04-04 (NOT this estimate)
- Building shell --> DEL-04-01 (NOT this estimate)

## Warnings

- None.
