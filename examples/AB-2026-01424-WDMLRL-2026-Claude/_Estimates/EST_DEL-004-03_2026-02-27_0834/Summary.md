# Summary — EST_DEL-004-03_2026-02-27_0834

## Basis of Estimate

| Field | Value |
|---|---|
| **BASIS_OF_ESTIMATE** | PARAMETRIC |
| **Method Used** | PARAMETRIC (all lines) |
| **Currency** | CAD |
| **Pricing Model** | Hours (from Level_of_Effort.csv) x Hourly Rates (from Professional_Staff_Rates.csv) |
| **Fallback Policy** | ALLOW_PARAMETRIC |
| **Mixed Methods** | Allowed (TRUE) — not exercised; all lines are PARAMETRIC |

## Scope

- **Deliverable:** DEL-004-03 Power Distribution Plans
- **Package:** PKG-004 Electrical Design
- **Type:** Drawing Set (IFC, P.Eng.-stamped)
- **Discipline:** Electrical Engineering
- **Covers SOW:** SOW-0014 (Complete final electrical design)
- **Supports OBJ:** OBJ-001, OBJ-003, OBJ-005

## Totals by Deliverable

| WBS_DeliverableID | Deliverable Name | Amount (CAD) | Lines |
|---|---|---|---|
| DEL-004-03 | Power Distribution Plans | $18,810.00 | 4 |

## Totals by CBS

| CBS | Amount (CAD) | Lines | % of Total |
|---|---|---|---|
| Design-Electrical | $17,280.00 | 2 | 91.9% |
| Management | $1,530.00 | 2 | 8.1% |
| **TOTAL** | **$18,810.00** | **4** | **100.0%** |

## Totals by Role

| RoleID | Role | Hours | Rate (CAD/hr) | Amount (CAD) | % of Total |
|---|---|---|---|---|---|
| R-16 | Electrical Engineer | 84 | $165.00 | $13,860.00 | 73.7% |
| R-13 | BIM Technician | 36 | $95.00 | $3,420.00 | 18.2% |
| R-01 | Project Manager | 6 | $165.00 | $990.00 | 5.3% |
| R-08 | Cost Estimator | 4 | $135.00 | $540.00 | 2.9% |
| | **TOTAL** | **130** | | **$18,810.00** | **100.0%** |

## Key Observations

1. **Electrical Engineer dominates effort (73.7%):** 84 hours of Electrical Engineer time reflects the complexity of this deliverable — it is the central power distribution drawing set covering all branch circuits for cranes, heavy receptacles, lighting, mechanical equipment, and code compliance. The engineer must perform load calculations, circuit design, code review (CEC Part I), MEP coordination, and apply P.Eng. stamp.

2. **BIM/CAD production is substantial (18.2%):** 36 hours of BIM Technician time covers floor plan setup on architectural underlay, circuit routing graphics, legend/notes sheets, and panel schedule cross-reference sheets. For a ~13,000 sqft industrial shop with multiple load types, this is consistent with standard drawing set production effort.

3. **Management overhead is light (8.1%):** Combined PM and Cost Estimator effort of 10 hours is appropriate for a single Drawing Set deliverable within a larger package.

4. **This is a professional services (design) estimate only.** It covers the cost of producing the Power Distribution Plans drawing set. It does NOT include construction material or installation costs, which would fall under PKG-015 (Electrical & Low-Voltage Installation).

## Warnings

- None. All 4 line items are fully priced with PARAMETRIC method, 100% provenance completeness.

## Coverage Gaps

- Items ITEM-005 through ITEM-008 in Items.csv represent included activities (MEP coordination, utility coordination, County submission, code review) whose effort is embedded within the 4 priced role-hours. They are not separately priced to avoid double-counting.
- Professional_Design_Fees.csv (PS-04) offers an alternative fee-based pricing approach (1.6% of construction value for electrical design). This was not used because LOE-based pricing from Level_of_Effort.csv is more granular and deliverable-specific. The fee-based method would require a construction value estimate that is outside this deliverable scope.
