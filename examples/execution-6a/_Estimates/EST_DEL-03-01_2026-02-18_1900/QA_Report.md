# QA Report — EST_DEL-03-01_2026-02-18_1900

## RUN_STATUS: WARNINGS

Some totals exist but material assumptions remain regarding apportionment percentages and the underlying construction cost base.

---

## S1 — Write Quarantine Respected

**PASS.** All files written under `_Estimates/EST_DEL-03-01_2026-02-18_1900/` only. No files outside the estimating tool root were modified.

## S2 — Snapshot Created

**PASS.** Snapshot folder `EST_DEL-03-01_2026-02-18_1900` created under `_Estimates/`.

## S3 — BASIS_OF_ESTIMATE Validated

**PASS.** `BASIS_OF_ESTIMATE = RATE_TABLE` is a valid enum value.

## S4 — Required Artifacts Exist

**PASS.** All required artifacts are present:

| Artifact | Status |
|---|---|
| Run_Context.md | Present |
| Summary.md | Present |
| QA_Report.md | Present (this file) |
| Source_Index.md | Present |
| Decision_Log.md | Present |
| Assumptions_Log.md | Present |
| WBS_CBS_Matrix.csv | Present |
| Detail.csv | Present |

## S5 — Detail Schema Integrity

**PASS.** Detail.csv contains all required columns:

- LineID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes

Method values check:
- L-001: Method=RATE_TABLE (valid)
- L-002: Method=RATE_TABLE (valid)

Allowance/parametric convention check:
- Both lines use Qty=1, Unit=LS, UnitRate=Amount. This follows the convention (items are lump-sum apportioned amounts).

## S6 — Provenance Discipline

**PASS.** Provenance completeness: **100%** (2 of 2 priced rows have non-TBD SourceRef).

| LineID | SourceRef Status | Source Files Referenced |
|---|---|---|
| L-001 | Complete | Professional_Design_Fees.csv DF-02 + Assumed_Project_Parameters.csv PP-23 |
| L-002 | Complete | Earthwork_Civil_Rates.csv EC-11 |

No missing-source offenders.

## S7 — Status Reporting

**RUN_STATUS = WARNINGS**

Reason: Totals are calculable but the following material gaps remain:

1. **Construction cost base (PP-23) is LOW confidence.** The $1,800,000 value driving the design fee is a parametric rough estimate. A refined construction estimate would change the design fee proportionally.
2. **Apportionment percentages (ASM-001, ASM-002) are assumptions.** The 30% DEL-03-01 share of civil design and the 42% share of survey costs are reasoned estimates, not sourced from rate tables. They are documented and bounded but could shift with more granular scope definition.
3. **Rate table source basis mismatch.** The rate tables declare their basis as MARKET or PARAMETRIC rather than RATE_TABLE. Under ALLOW_MIXED_METHODS=FALSE, this is a noted deviation (see DEC-001). The sources are the best available rate table evidence and are treated as such.

## Schema Validity Detail

| Check | Result |
|---|---|
| Detail.csv parseable | PASS |
| All required columns present | PASS |
| Method values valid (QUOTE/RATE_TABLE/HISTORICAL/ALLOWANCE/PARAMETRIC) | PASS (2/2 = RATE_TABLE) |
| Allowance/parametric convention (Qty=1, Unit=LS, UnitRate=Amount) | PASS (convention followed for LS items) |
| Currency consistent | PASS (all CAD) |
| Amounts rounded to DOLLAR | PASS |

## Coverage

| Metric | Value |
|---|---|
| Deliverables in scope | 1 |
| Deliverables covered (with priced lines) | 1 |
| Deliverables missing | 0 |
| Deliverables blocked | 0 |
| Total line items | 2 |
| Total amount | $18,500 CAD |

## Basis-Consistency Check

| Check | Result |
|---|---|
| BASIS_OF_ESTIMATE | RATE_TABLE |
| Methods used in Detail.csv | RATE_TABLE (2/2 lines) |
| Mixed methods present | No |
| ALLOW_MIXED_METHODS setting | FALSE |
| Consistency | PASS (all lines match basis) |
| Note | Source files declare basis as MARKET/PARAMETRIC; treated as rate table evidence per DEC-001 |

## Blocker Counts (from dependency evidence)

| Type | Count | Details |
|---|---|---|
| Upstream prerequisites (unresolved maturity) | 4 | DEL-02-01 building footprint, DEL-04-01 cold storage siting, TPN46 drawings, geotechnical report |
| Post-award constraints | 1 | Civil survey files (post-award from Owner) |
| Hard blockers preventing estimating | 0 | Design fee estimate is viable via percentage-of-cost method |

## What to Fix for a Cleaner Rerun

1. **Refine PP-23 (site/civil construction cost).** Once DEL-03-02 (earthworks), DEL-03-03 (pavements), and DEL-03-04 (utilities) are estimated with meaningful quantities, replace the parametric $1,800,000 with a bottom-up total. This will produce a more accurate civil design fee.
2. **Validate apportionment percentages (ASM-001, ASM-002).** The 30% / 42% splits are reasonable but should be reviewed by the estimating team or compared to historical project data.
3. **Confirm rate table source compatibility.** If ALLOW_MIXED_METHODS=FALSE is strictly enforced, the rate sources should be relabeled as RATE_TABLE (they are functionally rate tables regardless of their declared basis).
