# Source Index

## Indexed Price Sources

### 1. Professional_Staff_Rates.csv

| Field | Value |
|---|---|
| Path | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6a/_PriceSources/Professional_Staff_Rates.csv |
| Source Type | Rate table |
| Format | CSV, 31 data rows + header |
| Currency | CAD |
| Confidence | MEDIUM (all rates marked MARKET basis) |
| Relevant Roles | R-20 (Safety Officer, $110/hr); R-24 (Administrative / Document Control, $80/hr) |
| Parsing Notes | Clean CSV; no missing values in relevant rows. R-30 (Surety Broker) has HourlyRate=0 and is marked N/A (commission-based). |
| Supports | Unit rates for all labour line items in DEL-01-03 |
| Cannot Support | Non-labour costs (training materials, PPE, signage supplies) |

### 2. Level_of_Effort.csv

| Field | Value |
|---|---|
| Path | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6a/_PriceSources/Level_of_Effort.csv |
| Source Type | Level of effort / hours allocation table |
| Format | CSV, 18 data rows + header (covering all PKG-001 deliverables in execution 6a) |
| Relevant Rows | DEL-01-03: R-20 Safety Officer = 60h; R-24 Admin/Doc Control = 8h |
| Basis | PARAMETRIC (hours derived from project parameter assumptions) |
| Parsing Notes | Clean CSV. Hours are integer values. Notes column provides derivation rationale (e.g., "H&S plan development (20h) + site safety management (~2.5h/wk x 16wk active)"). |
| Supports | Quantity (hours) for labour line items |
| Cannot Support | Non-labour quantities; unit rates (rates come from Professional_Staff_Rates.csv) |

### 3. Assumed_Project_Parameters.csv

| Field | Value |
|---|---|
| Path | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6a/_PriceSources/Assumed_Project_Parameters.csv |
| Source Type | Project parameters / assumptions table |
| Format | CSV, 29 data rows + header |
| Relevant Parameters | PP-01 (Construction duration = 18 months); PP-02 (Design phase = 4 months) |
| Supports | Context for LoE hour derivations (e.g., construction duration drives Safety Officer site hours) |
| Cannot Support | Direct pricing; no unit rates or cost data for non-labour items |

## Sources NOT Available (Gaps)

| Gap | Impact | CBS Affected |
|---|---|---|
| No training cost source (materials, instructor fees, certification costs) | Cannot price training line item | CBS-TRAINING |
| No PPE/signage supply cost source (unit costs, quantities) | Cannot price supplies line item | CBS-SUPPLIES |
