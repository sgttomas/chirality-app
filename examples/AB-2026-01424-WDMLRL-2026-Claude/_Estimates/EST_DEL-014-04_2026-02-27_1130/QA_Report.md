# QA Report — EST_DEL-014-04_2026-02-27_1130

## RUN_STATUS: WARNINGS

---

## Schema Validity

### Items.csv
- **Columns:** All 9 required columns present (ItemID, DeliverableID, Description, Qty, Unit, PricingMode, SourceDoc, SourceSection, Notes).
- **Row count:** 27 items.
- **PricingMode values:** UNIT_RATE (25 rows), LUMP_SUM (2 rows) -- all valid.
- **Qty:** All numeric; no TBD quantities. Quantities for pipe runs and labour hours are parametric estimates (not measured from IFC drawings).
- **SourceDoc:** All rows trace to one of the four documents (Datasheet, Specification, Procedure).
- **SourceSection:** All rows populated.
- **PASS**

### Detail.csv
- **Columns:** All 14 required columns present (LineID, ItemID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes).
- **Row count:** 27 lines.
- **Method values:** PARAMETRIC (10 rows), RATE_TABLE (17 rows) -- all valid.
- **Allowance/parametric convention:** L-20 and L-21 are LUMP_SUM items with Qty=1, Unit=LS, UnitRate=Amount -- convention respected.
- **PASS**

---

## Quantity Takeoff Coverage

| Deliverable | Documents Found | Documents Missing | Items Extracted |
|---|---|---|---|
| DEL-014-04 | 5 of 5 (_CONTEXT.md, Datasheet.md, Specification.md, Guidance.md, Procedure.md) | None | 27 |

- All four production documents plus _CONTEXT.md were read and parsed.
- No `[WARNING] MISSING_DOCUMENT` conditions.
- **PASS**

---

## Pricing Coverage

| Metric | Value |
|---|---|
| Total line items | 27 |
| Items priced (non-TBD Amount) | 27 (100%) |
| Items with Amount = TBD | 0 (0%) |
| Items priced via RATE_TABLE | 17 (63.0%) |
| Items priced via PARAMETRIC | 10 (37.0%) |

- **100% pricing coverage** achieved.
- 37% of lines use PARAMETRIC method without rate table support (acceptable under FALLBACK_POLICY=ALLOW_PARAMETRIC and ALLOW_MIXED_METHODS=TRUE).
- **PASS (with caveats)**

---

## Provenance Completeness

| Metric | Value |
|---|---|
| Total Detail.csv rows | 27 |
| Rows with non-TBD SourceRef | 27 (100%) |
| Rows with `location TBD` SourceRef | 0 (0%) |

- All 27 rows have explicit SourceRef values pointing to specific PRICE_SOURCE files/rows or to parametric basis statements.
- **PASS**

### Top Missing-Source Offenders
- None. All lines have SourceRef populated.

---

## Basis-Consistency Checks

| Check | Result |
|---|---|
| BASIS_OF_ESTIMATE | PARAMETRIC (valid enum) |
| ALLOW_MIXED_METHODS | TRUE |
| Method mix | PARAMETRIC: 10 lines (37%), RATE_TABLE: 17 lines (63%) |
| FALLBACK_POLICY | ALLOW_PARAMETRIC |

- Mixed methods are explicitly allowed (ALLOW_MIXED_METHODS=TRUE).
- RATE_TABLE method used where rate tables exist in PRICE_SOURCES (sanitary piping, labour rates, professional staff rates + LOE).
- PARAMETRIC method used where no rate table exists (drain bodies, grates, traps, vent piping, permits, coordination).
- **Consistent with configured policy.**
- **PASS**

---

## Scope Coverage

| Metric | Value |
|---|---|
| Deliverables in scope | 1 (DEL-014-04) |
| Deliverables estimated | 1 (DEL-014-04) |
| Excluded from scope | DEL-018-05 (mud sump civil work), DEL-014-02 (septic system), DEL-006-03 (plumbing design), DEL-014-05 (emergency shower unit), DEL-014-06 (plumbing fixtures), PKG-011 (concrete) |

- Scope boundaries are explicitly stated in Specification (Included/Excluded sections).
- **PASS**

---

## Warnings Summary

| ID | Severity | Description |
|---|---|---|
| W-01 | MEDIUM | 8 TBD material attributes (drain type, body material, grate material, body diameter, outlet size, flow rate, trap type, temperature range) pending IFC plumbing design (DEL-006-03). Material unit rates are parametric estimates. |
| W-02 | LOW | Sump drain quantity assumed minimum 2; final count per IFC design. |
| W-03 | MEDIUM | No dedicated plumbing drain/fixture pricing in PRICE_SOURCES. 10 of 27 lines priced parametrically. |
| W-04 | HIGH | Oil/grease interceptor requirement TBD (REQ-014-04-11). If required, estimated $3,000-$8,000+ not included. |
| W-05 | MEDIUM | Wash bay drain scope boundary with DEL-018-05 TBD. Interior drain and stub included; exterior piping excluded. |
| W-06 | MEDIUM | Pipe run lengths are parametric estimates; actual routing per IFC drawings could vary +/-30%. |
| W-07 | LOW | Plumber labour hours are parametric; no production rate data in PRICE_SOURCES. |

---

## Write Quarantine Verification

- All output files written to: `{RUN_ROOT}/_Estimates/EST_DEL-014-04_2026-02-27_1130/`
- No files modified outside `_Estimates/`.
- **PASS**

---

## What to Fix for a Cleaner Rerun

1. **Add plumbing drain/fixture unit pricing** to PRICE_SOURCES (drain body, grate, trap, and trap primer unit costs from supplier quotes or RS Means).
2. **Resolve oil/grease interceptor requirement** (REQ-014-04-11) -- either include or explicitly exclude with documented determination.
3. **Obtain IFC plumbing drawings** (DEL-006-03) to replace parametric pipe run lengths and drain quantities with actual takeoff measurements.
4. **Confirm sump drain quantity** with Plumbing Engineer; update I-05 quantity if more than 2.
5. **Add above-ground vent piping rate** to Underground_Utility_Rates.csv or a new Mechanical_System_Rates file.
6. **Confirm Alberta Safety Code permit fee** schedule for plumbing permits; replace parametric L-21 with actual fee.
7. **Resolve wash bay drain scope boundary** (CFT-014-04-01) to confirm extent of DEL-014-04 scope vs DEL-018-05.
