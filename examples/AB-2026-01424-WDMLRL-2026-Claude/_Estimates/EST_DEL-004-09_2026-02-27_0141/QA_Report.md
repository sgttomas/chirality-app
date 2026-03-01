# QA Report — EST_DEL-004-09_2026-02-27_0141

## RUN_STATUS: OK

---

## Schema Validity

### Items.csv

| Check | Result |
|---|---|
| File exists | PASS |
| Parseable CSV | PASS |
| Required columns present (ItemID, DeliverableID, Description, Qty, Unit, PricingMode, SourceDoc, SourceSection, Notes) | PASS |
| All rows have DeliverableID = DEL-004-09 | PASS |
| PricingMode values valid (UNIT_RATE or LUMP_SUM) | PASS |
| Total rows | 36 |
| Rows with Qty = TBD | 0 |
| All rows trace to a SourceDoc (Datasheet, Specification, Procedure) | PASS |
| All rows have SourceSection populated | PASS |

### Detail.csv

| Check | Result |
|---|---|
| File exists | PASS |
| Parseable CSV | PASS |
| Required columns present (LineID, ItemID, CBS, WBS_PackageID, WBS_DeliverableID, Description, Qty, Unit, UnitRate, Amount, Currency, Method, SourceRef, Confidence, Notes) | PASS |
| All ItemIDs trace to Items.csv | PASS (DL-001 to ITEM-001, DL-002 to ITEM-002, DL-003 to ITEM-003, DL-004 to ITEM-004) |
| Method values valid (PARAMETRIC) | PASS |
| Allowance/parametric convention | N/A — all lines are UNIT_RATE with real Qty/Unit (hours) |
| Currency consistent | PASS (all CAD) |
| Total rows | 4 |
| Rows with Amount = TBD | 0 |

---

## Quantity Takeoff Coverage

| Metric | Value |
|---|---|
| Deliverables in scope | 1 (DEL-004-09) |
| Documents read | 4 of 4 (Datasheet, Specification, Guidance, Procedure) |
| Missing documents | 0 |
| Items extracted | 36 |
| Items with labour pricing (UNIT_RATE) | 4 (ITEM-001 through ITEM-004) |
| Items as scope verification lines (LUMP_SUM, cost embedded in labour) | 32 (ITEM-005 through ITEM-036) |

**Note:** Items 5–36 represent the electrical systems, specification requirements, and procedure activities that the Electrical Engineer must address in producing the specification. Their cost is embedded in the labour effort (Items 1–4). They are extracted as separate items for scope verification and traceability, not for separate pricing. This is appropriate for a professional services (design) deliverable where the output is a written specification document, not a constructed asset.

**Specification scope coverage:** The 32 scope verification items cover all 27 requirements (REQ-001 through REQ-027) from the Specification document, plus 5 procedure-level activities (utility coordination, discipline coordination, design calculations, specification drafting, IFC finalization, permit coordination). All major electrical systems from the Datasheet are represented (power supply, lighting across 5 space types, ceiling fans, 5 receptacle circuit types, 5 dedicated equipment circuits, exhaust fans, 2 low-voltage systems, grounding/bonding, emergency lighting, lighting controls, illumination levels, voltage drop, wiring methods, and standards identification).

---

## Pricing Coverage

| Metric | Value |
|---|---|
| Total priced lines in Detail.csv | 4 |
| Lines with Amount = TBD | 0 |
| Pricing coverage | **100%** (4/4) |
| Total estimated amount | **$10,170.00 CAD** |

---

## Provenance Completeness

| Metric | Value |
|---|---|
| Detail.csv rows with non-TBD SourceRef | 4 of 4 |
| Provenance completeness | **100%** |
| Missing-source offenders | None |

All 4 priced lines reference specific rows in Professional_Staff_Rates.csv (for rates) and Level_of_Effort.csv (for hours).

---

## Basis-Consistency Checks

| Check | Result |
|---|---|
| BASIS_OF_ESTIMATE | PARAMETRIC |
| Methods used in Detail.csv | PARAMETRIC (4/4 = 100%) |
| Method mix consistent with basis | **PASS** — all lines use PARAMETRIC method |
| ALLOW_MIXED_METHODS = TRUE | Allowed but not needed; basis is homogeneous |
| FALLBACK_POLICY = ALLOW_PARAMETRIC | No fallback needed; all items priced with primary basis |

---

## Scope Coverage

| Metric | Value |
|---|---|
| Deliverables included | 1 (DEL-004-09) |
| Deliverables excluded | 0 |
| Package | PKG-004 (Electrical Design) |
| SOW coverage | SOW-0014 (Provide electrical design drawings and documentation) |
| Objectives supported | OBJ-003 (Complete P.Eng.-stamped IFC design documentation), OBJ-005 (Electrical/low-voltage systems) |

---

## Write Quarantine Verification

| Check | Result |
|---|---|
| All outputs under _Estimates/ | PASS |
| No files modified outside _Estimates/ | PASS |

---

## Operator Acceptance Checklist

| Criterion | Status |
|---|---|
| RUN_STATUS is OK or WARNINGS with bounded gaps | **OK** |
| Quantity takeoff reviewed for completeness | 36 items extracted from 4 documents; all electrical systems and specification requirements represented |
| Basis-consistency checks pass | PASS — 100% PARAMETRIC |
| Provenance completeness reported | 100% — all lines traced |
| Scope coverage explicit | 1 deliverable, 1 SOW item, 2 objectives |
| No writes outside _Estimates/ | PASS |

---

## What to Fix for a Cleaner Rerun

1. **No action required** — this run is clean with 100% pricing and provenance coverage.
2. **Optional cross-check:** If a construction value estimate becomes available, cross-check the full PKG-004 design fee against the Professional_Design_Fees.csv DF-04 range (1.0%–2.2% of construction value) for reasonableness.
3. **Optional refinement:** If the Electrical Engineer provides a more detailed time breakdown (e.g., hours per procedure step or per specification section), the Items.csv labour lines could be decomposed further for finer-grained tracking.
4. **TBD resolution monitoring:** The specification identifies 7 TBD prerequisite inputs (crane specs, camera system, antenna system, mechanical equipment data, utility confirmation, County approval, code editions). Resolution of these inputs will not change the design labour estimate but will affect deliverable schedule risk.
