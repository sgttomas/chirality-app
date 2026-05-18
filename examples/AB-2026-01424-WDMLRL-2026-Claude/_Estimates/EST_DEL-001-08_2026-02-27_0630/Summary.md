# Summary — EST_DEL-001-08_2026-02-27_0630

## Basis of Estimate

| Field | Value |
|---|---|
| Basis | PARAMETRIC |
| Method | Level of Effort (hours by role) x Professional Staff Rates ($/hr) |
| Currency | CAD |
| Fallback Policy | ALLOW_PARAMETRIC |
| Mixed Methods | Allowed (TRUE) — not exercised; all lines are PARAMETRIC |

## Totals

### By Deliverable

| WBS_DeliverableID | Deliverable Name | Amount (CAD) | Line Count |
|---|---|---|---|
| DEL-001-08 | Finish Schedule | $7,420.00 | 5 |

### By Package

| WBS_PackageID | Package Name | Amount (CAD) | Line Count |
|---|---|---|---|
| PKG-001 | Architectural Design | $7,420.00 | 5 |

### By CBS (Cost Breakdown Structure)

| CBS | Amount (CAD) | Line Count | Description |
|---|---|---|---|
| Design-Management | $1,530.00 | 2 | Project Manager ($990) + Cost Estimator ($540) |
| Design-Production | $5,890.00 | 3 | Senior Architect ($3,240) + Architect ($1,890) + BIM Technician ($760) |
| **TOTAL** | **$7,420.00** | **5** | |

### By Role

| RoleID | Role | Hours | Rate ($/hr) | Amount (CAD) |
|---|---|---|---|---|
| R-01 | Project Manager | 6 | $165.00 | $990.00 |
| R-08 | Cost Estimator | 4 | $135.00 | $540.00 |
| R-11 | Senior Architect | 18 | $180.00 | $3,240.00 |
| R-12 | Architect | 14 | $135.00 | $1,890.00 |
| R-13 | BIM Technician | 8 | $95.00 | $760.00 |
| | **TOTAL** | **50** | | **$7,420.00** |

## Scope Coverage

- **Deliverables in scope:** 1 (DEL-001-08 Finish Schedule)
- **Documents read:** 5 of 5 (_CONTEXT.md, Datasheet.md, Specification.md, Guidance.md, Procedure.md)
- **Missing documents:** None
- **Priceable items identified:** 11 (in Items.csv)
- **Priced line items:** 5 (in Detail.csv) — the 5 labour roles that constitute the design production cost
- **Items not separately priced:** 6 (ITEM-006 through ITEM-011 represent work activities already covered by the labour LOE in ITEM-001 through ITEM-005; they are recorded in Items.csv for scope traceability but do not generate additional cost lines to avoid double-counting)

## Key Observations

1. **DEL-001-08 is a design document** (Finish Schedule). The estimate covers the professional design labour cost to produce the schedule, not the construction cost of installing interior finishes.
2. **Total LOE is 50 hours** across 5 roles, consistent with a "Schedule" type deliverable (comparable to DEL-001-07 Door & Window Schedule which also has 50 hours).
3. **Senior Architect is the dominant cost driver** at 18 hours ($3,240 = 43.7% of total), reflecting the design-lead and code-review responsibility described in the Procedure.
4. **All line items are PARAMETRIC** with MEDIUM confidence, consistent with the parametric LOE model used across this project's design deliverables.

## Warnings

- None. All items priced. 100% provenance coverage. No TBDs in Detail.csv.
