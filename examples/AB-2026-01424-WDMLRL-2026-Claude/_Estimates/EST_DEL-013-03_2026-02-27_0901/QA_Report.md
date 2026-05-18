# QA Report — EST_DEL-013-03_2026-02-27_0901

## RUN_STATUS: WARNINGS

**Rationale:** Totals are meaningful as a parametric budget placeholder. Material TBDs remain (MUA airflow rate, equipment selection, ductwork routing) that will require re-estimation once mechanical design is complete. 74% of line items rely on parametric ASSUMPTION without direct price source evidence.

---

## S1 — Write Quarantine Respected

| Check | Result |
|---|---|
| All outputs under _Estimates/ | PASS |
| No deliverable files modified | PASS |
| No lifecycle files modified | PASS |
| No decomposition files modified | PASS |

---

## S2 — Snapshot Created

| Check | Result |
|---|---|
| Snapshot folder exists | PASS — EST_DEL-013-03_2026-02-27_0901/ |

---

## S3 — BASIS_OF_ESTIMATE Validated

| Check | Result |
|---|---|
| BASIS_OF_ESTIMATE provided | PASS — PARAMETRIC |
| Value is valid enum | PASS |

---

## S4 — Required Artifacts Exist

| Artifact | Status |
|---|---|
| Run_Context.md | PRESENT |
| Items.csv | PRESENT |
| Summary.md | PRESENT |
| QA_Report.md | PRESENT (this file) |
| Source_Index.md | PRESENT |
| Detail.csv | PRESENT |
| WBS_CBS_Matrix.csv | PRESENT |
| Decision_Log.md | PRESENT |
| Assumptions_Log.md | PRESENT |

---

## S5 — CSV Schema Integrity

### Items.csv

| Check | Result |
|---|---|
| Parseable CSV | PASS |
| Required columns present (ItemID, DeliverableID, Description, Qty, Unit, PricingMode, SourceDoc, SourceSection, Notes) | PASS |
| All rows trace to source document | PASS — all 25 items reference Datasheet, Specification, or Procedure |
| PricingMode values valid (UNIT_RATE or LUMP_SUM) | PASS |
| No TBD quantities | PASS — all quantities resolved (some are ASSUMPTION-based) |
| Item count | 25 items |

### Detail.csv

| Check | Result |
|---|---|
| Parseable CSV | PASS |
| Required columns present | PASS — all 14 mandatory columns |
| Method values valid | PASS — all PARAMETRIC |
| Allowance/parametric convention | PASS — LS items have Qty=1, Unit=LS, UnitRate=Amount |
| Line count | 31 lines (ITM-022 split into 6 role-based lines) |

---

## S6 — Provenance Discipline

### Provenance Completeness

| Category | Lines | With Source Evidence | With ASSUMPTION Only | Provenance % |
|---|---|---|---|---|
| Rate-table-sourced (MS-02, MS-06) | 2 | 2 | 0 | 100% |
| LOE + Staff Rates | 6 | 6 | 0 | 100% |
| ASSUMPTION-based parametric | 23 | 0 | 23 | 0% |
| **Total** | **31** | **8** | **23** | **26%** |

### Top Missing-Source Offenders

| LineID | Description | Amount (CAD) | Gap |
|---|---|---|---|
| L-003 | Supply ductwork (from MS-06 rate but qty is parametric) | 72,480.00 | Qty derived from floor area parameter; actual ductwork scope TBD |
| L-001 | MUA unit (from MS-02 but sizing TBD) | 45,000.00 | Equipment selection TBD; rate is range midpoint |
| L-007 | Ductwork insulation | 10,870.00 | 15% ratio ASSUMPTION; no direct source |
| L-010 | Controls/BAS integration | 5,500.00 | No direct source; ASSUMPTION only |
| L-011 | Ductwork hangers/supports | 5,400.00 | 7.5% ratio ASSUMPTION; no direct source |

---

## S7 — Basis-Consistency Checks

| Check | Result |
|---|---|
| BASIS_OF_ESTIMATE | PARAMETRIC |
| ALLOW_MIXED_METHODS | TRUE |
| Methods used in Detail.csv | PARAMETRIC only (100%) |
| Basis-consistency | PASS — all methods match PARAMETRIC basis |
| FALLBACK_POLICY | ALLOW_PARAMETRIC — invoked for items without direct rate table evidence |

---

## Quantity Takeoff Coverage

| Metric | Value |
|---|---|
| Deliverables in scope | 1 (DEL-013-03) |
| Documents read | 4 of 4 (Datasheet, Specification, Guidance, Procedure) + _CONTEXT.md |
| Missing documents | 0 |
| Items extracted | 25 |
| Items with TBD quantities | 0 (quantities resolved via parametric methods) |
| Items with ASSUMPTION quantities | 3 (fire dampers qty=4, AHJ inspections qty=2, ductwork area=1208 m2 from PP-10) |

---

## Pricing Coverage

| Metric | Value |
|---|---|
| Total line items in Detail.csv | 31 |
| Lines priced (non-TBD Amount) | 31 (100%) |
| Lines with TBD Amount | 0 |
| Lines with direct price source | 8 (26%) |
| Lines with ASSUMPTION pricing | 23 (74%) |
| Total estimated cost | $186,590.00 CAD |

---

## What to Fix for a Cleaner Rerun

1. **Resolve MUA airflow rate** (BLOCKING TBD from DEL-003-06) -- this drives equipment selection and will change the MUA unit cost and potentially ductwork sizing.
2. **Obtain mechanical design drawings** (DEL-003-02, DEL-003-03) -- enables actual ductwork quantity takeoff instead of parametric per-m2 estimate.
3. **Obtain equipment schedule** (DEL-003-05) -- provides MUA make/model/capacity for quote-based pricing.
4. **Obtain fire separation drawings** -- enables accurate fire/smoke damper count.
5. **Obtain mechanical specification** (DEL-003-07) -- provides insulation, leakage testing, and filtration specifications.
6. **Add trade labour LOE** to Level_of_Effort.csv for HVAC Sheet Metal (T-06) and Gas Fitter to enable separate labour quantification.
7. **Obtain MUA equipment quotes** from suppliers for QUOTE-based pricing to replace parametric allowance.
8. **Obtain TAB contractor quotes** for test-and-balance and duct leakage testing.
9. **Confirm gas-fired vs. indirect MUA type** -- affects gas connection cost and heating integration.
10. **Confirm wash bay inclusion** in MUA distribution scope (Enrichment X-001) -- may affect ductwork quantity.
