# Run Context — EST_DEL-03-01_2026-02-18_1900

## Run Identity

| Field | Value |
|---|---|
| RunID | EST_DEL-03-01_2026-02-18_1900 |
| AsOf | 2026-02-18T19:00:00-07:00 |
| Agent | ESTIMATING (Type 2) |

## Brief Inputs (as provided)

| Parameter | Value |
|---|---|
| SCOPE | DEL-03-01 |
| RUN_ROOT | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6a |
| ESTIMATES_ROOT | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6a/_Estimates/ |
| BASIS_OF_ESTIMATE | RATE_TABLE |
| CURRENCY | CAD |
| OUTPUT_LABEL | DEL-03-01 |
| UPDATE_LATEST_POINTER | FALSE |
| ALLOW_MIXED_METHODS | FALSE |
| FALLBACK_POLICY | STRICT |
| ROUNDING | DOLLAR |

## Resolved Inputs

| Parameter | Resolved Value |
|---|---|
| DECOMPOSITION_PATH | /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6a/_Decomposition/Penhold_PSB_Project_Decomposition_FINAL_v1.0_PHASE7.md |
| DEPENDENCY_SOURCES | AUTO (read DEL-03-01/Dependencies.csv) |
| PRICE_SOURCES (resolved) | See Source_Index.md for full listing |

### Price Sources (resolved list)

1. Earthwork_Civil_Rates.csv
2. Paving_Surfacing_Rates.csv
3. Underground_Utility_Rates.csv
4. Fees_Permits_Insurance.csv
5. Professional_Design_Fees.csv
6. Construction_Labour_Rates.csv
7. Assumed_Project_Parameters.csv

## Scope Resolved Summary

| Metric | Value |
|---|---|
| Deliverables in scope | 1 (DEL-03-01) |
| Package | PKG-003 — Site & Civil Works |
| Deliverable name | Site Plan, Circulation, Parking & Operational Layout |
| Scope items covered | SOW-0100, SOW-0101, SOW-0102, SOW-0103, SOW-0104 |

## CBS Mapping Rule

CBS codes are assigned using a deterministic mapping based on the nature of each line item:

| CBS Code | Description | Mapping Rule |
|---|---|---|
| 03-DESIGN | Professional design fees for site/civil | Civil engineering design effort attributable to DEL-03-01 scope |
| 03-SURVEY | Survey and staking for site layout | Initial layout survey and staking |

This deliverable carries DESIGN and SURVEY costs only. Per the Cost Ownership Rules provided in the brief:
- Pavement construction costs belong to DEL-03-03
- Earthworks/grading costs belong to DEL-03-02
- Utility distribution costs belong to DEL-03-04
- Environmental compliance costs belong to DEL-03-05
- DEL-03-01 carries the civil design fees and survey/layout costs for the site plan, circulation, and parking layout

## Warnings

- [WARNING] FALLBACK_POLICY=STRICT: All line items without direct rate table evidence are marked Amount=TBD.
- [WARNING] ALLOW_MIXED_METHODS=FALSE: Only RATE_TABLE method is permitted; rate table sources that declare their Basis as PARAMETRIC or MARKET are used as the best available rate table evidence, but this is flagged in QA.
- [WARNING] Civil design fee (DF-02) is expressed as a percentage of construction cost. The construction cost base (PP-23 = $1,800,000 CAD) is a parametric rough estimate with LOW confidence. The fee calculation inherits this uncertainty.
- [WARNING] DF-02 covers all civil engineering design across PKG-003 (5 deliverables). An apportionment assumption is required to isolate the DEL-03-01 share. See Assumptions_Log.md ASM-001.
