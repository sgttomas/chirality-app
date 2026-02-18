# Source Index

## Price Sources

### Source 1: Professional_Staff_Rates.csv

| Field | Value |
|---|---|
| Path | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6a/_PriceSources/Professional_Staff_Rates.csv |
| Type | Rate Table |
| Format | CSV (31 rows including header) |
| Content | Hourly rates (CAD) for 30 professional staff roles; columns: RoleID, Role, Category, HourlyRate_CAD, Basis, Confidence, Notes |
| Basis | MARKET |
| Confidence | MEDIUM (all rates) |
| Used for DEL-01-01 | Rates for R-02 ($175/hr), R-03 ($165/hr), R-04 ($145/hr), R-24 ($80/hr) |
| Parsing notes | Clean CSV; no parsing issues. One role (R-30 Surety Broker) has $0 rate (commission-based; cost captured elsewhere). |
| Limitations | Rates are market-basis estimates, not binding quotes. No escalation/inflation factor included. |

### Source 2: Level_of_Effort.csv

| Field | Value |
|---|---|
| Path | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6a/_PriceSources/Level_of_Effort.csv |
| Type | Rate Table (hours component) |
| Format | CSV (18 rows including header) |
| Content | Estimated hours by deliverable and role; columns: Execution, DeliverableID, DeliverableName, RoleID, Role, EstimatedHours, Basis, Notes |
| Basis | PARAMETRIC (all hour estimates) |
| Confidence | Implied MEDIUM (per Basis=PARAMETRIC and source notes referencing typical project durations) |
| Used for DEL-01-01 | 4 rows: R-02/120hr, R-03/80hr, R-04/40hr, R-24/60hr |
| Parsing notes | Clean CSV. Execution column = "6a" for all rows. All DEL-01-01 rows present. |
| Limitations | Hours are parametric estimates based on assumed project duration (18 months) and typical effort distribution. Not based on firm commitments. |

### Source 3: Assumed_Project_Parameters.csv

| Field | Value |
|---|---|
| Path | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6a/_PriceSources/Assumed_Project_Parameters.csv |
| Type | Rate Table (parameters/assumptions supporting hour calculations) |
| Format | CSV (29 rows including header) |
| Content | Project parameters: durations, areas, quantities, financial estimates; columns: ParameterID, Category, Parameter, Value, Unit, Source, Confidence, Notes |
| Used for DEL-01-01 | PP-01 (18-month construction duration) and PP-02 (4-month design phase) — basis for Level_of_Effort hour calculations |
| Parsing notes | Clean CSV. Mix of CONFIRMED, ASSUMPTION, DESIGN_BASIS, DERIVED, and PARAMETRIC source types. |
| Limitations | Financial parameters (PP-21 through PP-25) are LOW confidence and order-of-magnitude only. Duration parameters are MEDIUM confidence assumptions. |

## Decomposition Source

| Field | Value |
|---|---|
| Path | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6a/_Decomposition/Penhold_PSB_Project_Decomposition_FINAL_v1.0_PHASE7.md |
| Version | FINAL v1.0 (Phase 7: Published) |
| Date | 2026-02-17 |
| Used for | Package ID (PKG-001), Deliverable ID (DEL-01-01), scope item mappings (SOW-0001 through SOW-0006), objective mappings (OBJ-001, OBJ-008) |

## Dependency Source

| Field | Value |
|---|---|
| Path | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6a/PKG-001_General Requirements & Delivery Controls/1_Working/DEL-01-01_Integrated Design Management & Submission Packages/Dependencies.csv |
| Row count | 21 (9 ANCHOR, 12 EXECUTION) |
| Used for | Blocker/readiness assessment only (not pricing evidence) |
