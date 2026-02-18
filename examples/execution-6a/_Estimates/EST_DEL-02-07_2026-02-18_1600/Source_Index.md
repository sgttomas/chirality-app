# Source Index — EST_DEL-02-07_2026-02-18_1600

## Indexed Price Sources

### 1. Equipment_Pricing.csv

| Field | Value |
|---|---|
| **Path** | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6a/_PriceSources/Equipment_Pricing.csv |
| **Source Type** | Parametric pricing table |
| **Relevant Items** | EQ-04 (Diesel generator system, $120k-$180k, recommended $150k); EQ-05 (ATS, $8k-$15k, recommended $12k — included in EQ-04 for reference) |
| **Parsing Notes** | CSV with 16 items. Generator system EQ-04 is a lump-sum system price including genset, ATS, distribution, fuel tank (72-hr), pad, exhaust, sound attenuation, and commissioning. Confidence is LOW. |
| **Supports** | Line items L-0207-010 (primary pricing source) |
| **Cannot Support** | Vendor quote pricing; detailed component-level breakdown; site-specific installation conditions |

### 2. Electrical_System_Rates.csv

| Field | Value |
|---|---|
| **Path** | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6a/_PriceSources/Electrical_System_Rates.csv |
| **Source Type** | Parametric rate table (per-SF and lump-sum) |
| **Relevant Items** | No direct generator-specific line items. ES-14 (service entrance, $45k) is for DEL-02-06, not DEL-02-07. |
| **Parsing Notes** | CSV with 14 items. Division 26 rates by system type. Generator scope is better covered by EQ-04. |
| **Supports** | Background reference for electrical scope boundary confirmation |
| **Cannot Support** | Generator-specific pricing (covered by Equipment_Pricing.csv) |

### 3. Construction_Labour_Rates.csv

| Field | Value |
|---|---|
| **Path** | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6a/_PriceSources/Construction_Labour_Rates.csv |
| **Source Type** | Market rate table (fully burdened hourly rates) |
| **Relevant Items** | T-07 (Electrician, $80/hr); T-13 (Millwright, $80/hr); T-14 (Crane Operator, $86/hr) |
| **Parsing Notes** | CSV with 15 trades. Alberta prevailing rates with burden multiplier applied. |
| **Supports** | Line item L-0207-040 (installation labour estimate) |
| **Cannot Support** | Subcontractor pricing; generator commissioning specialist rates |

### 4. Professional_Design_Fees.csv

| Field | Value |
|---|---|
| **Path** | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6a/_PriceSources/Professional_Design_Fees.csv |
| **Source Type** | Market fee percentage table |
| **Relevant Items** | DF-05 (Electrical engineering design fees, 2.0%-3.0%, recommended 2.5% of electrical construction cost) |
| **Parsing Notes** | CSV with 8 disciplines. Fee percentages applied to construction cost of respective discipline. |
| **Supports** | Line item L-0207-050 (generator-specific design fees) |
| **Cannot Support** | Fixed-fee consultant proposals; specialist generator consulting |

### 5. Assumed_Project_Parameters.csv

| Field | Value |
|---|---|
| **Path** | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6a/_PriceSources/Assumed_Project_Parameters.csv |
| **Source Type** | Project assumptions and parameters |
| **Relevant Items** | PP-26 (72-hour generator runtime, CONFIRMED/MEDIUM confidence, pending Owner confirmation) |
| **Parsing Notes** | CSV with 29 parameters. PP-26 directly affects fuel tank sizing within EQ-04 system price. |
| **Supports** | Runtime assumption underpinning EQ-04 fuel tank sizing |
| **Cannot Support** | Actual fuel consumption rates; Owner-confirmed runtime requirement |

## Dependency Evidence Source

| Field | Value |
|---|---|
| **Path** | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6a/PKG-002_Main Public Services Building (PSB)/1_Working/DEL-02-07_Emergency Power & Backup Generator/Dependencies.csv |
| **Source Type** | Dependency register (v3.1 schema) |
| **Record Count** | 13 rows (4 anchor, 9 execution dependencies) |
| **Used For** | Blocker identification and readiness assessment (NOT for pricing) |
