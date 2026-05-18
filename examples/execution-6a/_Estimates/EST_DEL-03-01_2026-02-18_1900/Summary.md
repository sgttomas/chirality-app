# Estimate Summary — DEL-03-01: Site Plan, Circulation, Parking & Operational Layout

## Run Identity

| Field | Value |
|---|---|
| Snapshot | EST_DEL-03-01_2026-02-18_1900 |
| Deliverable | DEL-03-01 — Site Plan, Circulation, Parking & Operational Layout |
| Package | PKG-003 — Site & Civil Works |
| Basis of Estimate | RATE_TABLE |
| Currency | CAD |
| Rounding | DOLLAR |
| RUN_STATUS | WARNINGS |

## Basis of Estimate Used

The estimate uses **RATE_TABLE** as the primary method. Two rate table sources provide the pricing basis:

1. **Professional_Design_Fees.csv (DF-02):** Civil engineering design fees at 2.5% of site/civil construction cost. The construction cost base ($1,800,000 CAD) is sourced from Assumed_Project_Parameters.csv (PP-23) and is a parametric rough estimate with LOW confidence.
2. **Earthwork_Civil_Rates.csv (EC-11):** Construction survey and staking at $12,000 lump sum for full site development.

Both line items require apportionment to isolate the DEL-03-01 share from the total civil scope. Apportionment assumptions are documented in Assumptions_Log.md.

## Cost Ownership Context

Per the Cost Ownership Rules provided in the brief, DEL-03-01 carries **design fees and survey/layout costs only**:

| Cost Category | Owner | NOT DEL-03-01 |
|---|---|---|
| Site layout design (civil engineering) | **DEL-03-01** | -- |
| Clearing, stripping, earthworks, grading, drainage | -- | DEL-03-02 |
| Pavement construction (all types) | -- | DEL-03-03 |
| Concrete aprons at overhead doors | -- | DEL-03-03 |
| On-site utility distribution | -- | DEL-03-04 |
| Environmental compliance costs | -- | DEL-03-05 |

Although the brief's cost drivers mention "parking lot construction" and "access road," the cost ownership table explicitly assigns construction costs for pavements to DEL-03-03. DEL-03-01 carries only the design/survey component.

## Totals by CBS

| CBS | Description | Amount (CAD) | Line Count |
|---|---|---|---|
| 03-DESIGN | Civil engineering design fees (DEL-03-01 share) | $13,500 | 1 |
| 03-SURVEY | Construction survey and staking (initial layout) | $5,000 | 1 |
| **TOTAL** | | **$18,500** | **2** |

## Totals by Package/Deliverable

| Package | Deliverable | Amount (CAD) |
|---|---|---|
| PKG-003 | DEL-03-01 | $18,500 |

## Key Warnings

1. **LOW confidence on design fee base:** The $1,800,000 site/civil construction value (PP-23) is parametric with LOW confidence. A refined construction estimate from downstream deliverables (DEL-03-02, DEL-03-03, DEL-03-04) would improve the design fee calculation.
2. **Apportionment assumptions required:** Both line items required apportionment from a larger scope total (total civil design fee across PKG-003; total survey cost across full site development). See ASM-001 and ASM-002 in Assumptions_Log.md.
3. **Method basis mismatch:** The rate table sources declare their basis as MARKET or PARAMETRIC. Under ALLOW_MIXED_METHODS=FALSE, these are used as the best available rate table evidence, but the underlying source confidence is noted. See DEC-001 in Decision_Log.md.

## Blockers

No hard blockers prevent estimating DEL-03-01 at this stage. However, dependency evidence identifies upstream prerequisites (building footprint from DEL-02-01, cold storage siting from DEL-04-01, TPN46 drawings, geotechnical report) whose maturity is unconfirmed. These affect design scope certainty but do not prevent a design fee estimate based on percentage-of-construction-cost. See Blockers.md for detail.
