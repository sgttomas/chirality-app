# QA Report — EST_DEL-020-01_2026-02-27_0700

## RUN_STATUS: WARNINGS

Totals are meaningful for the professional staff labour component. Material TBDs remain for third-party costs (crane load testing, Safety Code inspection fees). The labour-only parametric model is complete and internally consistent.

---

## S1 — Write Quarantine Respected

**PASS.** All output files written exclusively under `_Estimates/EST_DEL-020-01_2026-02-27_0700/`. No files outside `_Estimates/` were modified.

## S2 — Snapshot Created

**PASS.** Snapshot folder `EST_DEL-020-01_2026-02-27_0700` created under `_Estimates/`.

## S3 — BASIS_OF_ESTIMATE Validated

**PASS.** `BASIS_OF_ESTIMATE = PARAMETRIC` is a valid enum value.

## S4 — Required Artifacts Exist

**PASS.** All required artifacts present:

| Artifact | Status |
|---|---|
| Run_Context.md | Created |
| Items.csv | Created (18 rows) |
| Summary.md | Created |
| QA_Report.md | Created (this file) |
| Source_Index.md | Created |
| Decision_Log.md | Created |
| Assumptions_Log.md | Created |
| WBS_CBS_Matrix.csv | Created |
| Detail.csv | Created (18 rows) |

## S5 — CSV Schema Integrity

### Items.csv

**PASS.**

| Check | Result |
|---|---|
| Parseable CSV | Yes |
| Required columns present (ItemID, DeliverableID, Description, Qty, Unit, PricingMode, SourceDoc, SourceSection, Notes) | Yes — all 9 columns present |
| All rows trace to source document and section | Yes — all 18 rows have SourceDoc and SourceSection populated |
| PricingMode values valid | Yes — all values are UNIT_RATE or LUMP_SUM |
| Lump-sum convention (Qty=1, Unit=LS) | Yes — all LUMP_SUM rows have Qty=1, Unit=LS |

### Detail.csv

**PASS (with TBD notes).**

| Check | Result |
|---|---|
| Parseable CSV | Yes |
| Required columns present (LineID, ItemID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes) | Yes — all 15 columns present |
| Method values valid | Yes — all values are PARAMETRIC |
| Allowance/parametric convention (Qty=1, Unit=LS, UnitRate=Amount for LS items) | Yes for priced LS items (Amount=0, UnitRate=0); TBD items use Qty=1, Unit=LS, UnitRate=TBD, Amount=TBD |
| All ItemIDs trace back to Items.csv | Yes — all 18 ItemIDs match |

## S6 — Provenance Discipline

| Metric | Value |
|---|---|
| Total rows in Detail.csv | 18 |
| Rows with non-TBD SourceRef | 16 (89%) |
| Rows with `location TBD` SourceRef | 2 (11%) |

**Top missing-source offenders:**

1. **DL-020-01-011** (Crane load testing): `location TBD` — no third-party crane inspection pricing in provided sources.
2. **DL-020-01-018** (Safety Code inspection coordination): `location TBD` — no Safety Code inspection fee schedule in provided sources.

## S7 — Status Reporting

**RUN_STATUS: WARNINGS**

Justification:
- Totals exist and are meaningful for professional staff labour ($11,290 CAD across 80 hours and 8 roles).
- 2 of 18 line items have TBD amounts (crane load testing, Safety Code fees). These represent third-party costs not available in the provided price sources.
- The labour-only model is internally consistent (all 8 roles priced from matched rate + hour sources).
- Non-labour costs (equipment, consumables) are not modelled; assumed negligible but flagged.

## S8 — Operator Acceptance Checklist

| Check | Status | Notes |
|---|---|---|
| RUN_STATUS is OK or WARNINGS with bounded gaps | PASS (WARNINGS) | Gaps limited to 2 third-party cost items; labour model complete |
| Items.csv reviewed for completeness | PASS | 18 items extracted from all 4 documents (Datasheet, Specification, Guidance, Procedure) |
| Basis-consistency checks pass | PASS | All 18 Detail.csv rows use Method=PARAMETRIC, consistent with BASIS_OF_ESTIMATE=PARAMETRIC |
| Provenance completeness reported | PASS | 89% provenance completeness; 2 TBD items identified with reasons |
| Scope coverage explicit | PASS | 1 deliverable (DEL-020-01) in scope; all 4 documents read; 0 missing documents |
| No writes outside _Estimates/ | PASS | Confirmed |

---

## What to Fix for a Cleaner Rerun

1. **Provide crane load testing pricing.** Obtain a quote or parametric rate for third-party crane load testing and inspection in Alberta to resolve DL-020-01-011.
2. **Confirm Safety Code inspection fee structure.** Determine whether Safety Code inspection fees are Owner-borne (per RFP S3.3.1) or Proponent-borne, and if Proponent-borne, provide a fee schedule to resolve DL-020-01-018.
3. **Consider adding non-labour cost allowances.** For a more complete estimate, add parametric allowances for test equipment rental, consumables, O&M manual printing/binding, and training materials.
4. **Validate Commissioning Agent hours.** The 30-hour allocation for the Commissioning Agent should be validated against project complexity once IFC design documents are available. For an industrial facility of ~13,000 sqft with 6+ system categories, 30 hours may be conservative.
