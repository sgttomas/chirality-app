# Run Context -- EST_DEL-04-04_2026-02-18_1500

| Field | Value |
|---|---|
| **RunID** | EST_DEL-04-04_2026-02-18_1500 |
| **AsOf** | 2026-02-18T15:00:00-07:00 |
| **Scope** | DEL-04-04 (Cold Storage -- Electrical & Ventilation), PKG-004 |
| **ScopeResolvedSummary** | 1 deliverable in scope; 0 excluded; 0 blocked |
| **BASIS_OF_ESTIMATE** | RATE_TABLE |
| **CURRENCY** | CAD |
| **PRICE_SOURCES** | Electrical_System_Rates.csv; Mechanical_System_Rates.csv; Construction_Labour_Rates.csv; Parametric_Building_Rates.csv; Assumed_Project_Parameters.csv |
| **DECOMPOSITION_PATH** | _Decomposition/Penhold_PSB_Project_Decomposition_FINAL_v1.0_PHASE7.md |
| **DEPENDENCY_SOURCES** | AUTO (DEL-04-04/Dependencies.csv loaded; 9 dependency rows found) |
| **FALLBACK_POLICY** | STRICT |
| **ALLOW_MIXED_METHODS** | FALSE |
| **UPDATE_LATEST_POINTER** | FALSE |
| **Rounding** | DOLLAR |
| **Warnings** | None |

## Scope Resolution

| DeliverableID | PackageID | InScope | Path | Notes |
|---|---|---|---|---|
| DEL-04-04 | PKG-004 | TRUE | PKG-004/.../DEL-04-04_Cold Storage - Electrical & Ventilation/ | Cold Storage -- Electrical & Ventilation |

## CBS Mapping Rule

CBS codes were assigned deterministically based on rate table category and discipline:
- `26-ELEC` = Division 26 Electrical (power distribution, lighting, panel, receptacles, door opener feeds)
- `23-VENT` = Division 23 Ventilation (condensation/icing prevention ventilation)

These CBS codes follow CSI MasterFormat division conventions adapted to the rate table categories.

## Rate Table Usage

Primary rates used:
- **ES-12** (Cold storage electrical -- basic power + lighting): $6/sf recommended -- covers panel, receptacles, lighting, door opener feeds. This is used as the comprehensive electrical rate for the cold storage building; ES-05 (lighting-only) is NOT layered on top to avoid double-counting.
- **MS-13** (Cold storage ventilation -- condensation prevention): $3/sf recommended -- covers ridge vents or gable fans, minimal mechanical.

Area parameter: PP-07 = 6,000 sf (60 ft x 100 ft, confirmed, HIGH confidence).

## Cross-Check (informational; not priced)

PB-02 (complete turnkey PEMB) at $48/sf minus PB-01 (shell only) at $32/sf = $16/sf delta for foundation + floor + doors + electrical + ventilation. Our estimate of $9/sf ($54,000 / 6,000 sf) for electrical + ventilation leaves $7/sf for foundation + floor + doors in other deliverables, which is directionally consistent.
