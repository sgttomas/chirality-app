# Estimate Summary: DEL-05-06 Option -- Appliances & Laundry

## BasisOfEstimate_Used

- **Basis:** QUOTE
- **Method applied:** Retail appliance pricing from Optional_Items_Pricing.csv treated as quote-equivalent (see DEC-EST-001).
- **Fallback used:** None. All line items priced from primary source.
- **Currency:** CAD
- **Rounding:** DOLLAR

## Estimate Total

| Description | Amount (CAD) |
|---|---|
| Equipment Purchase (CBS-EQP) | $14,100 |
| Installation & Connection (CBS-INST) | $4,500 |
| **DEL-05-06 Total** | **$18,600** |

## Detail by Line Item

| Line | Description | Qty | Unit | Rate | Amount |
|---|---|---|---|---|---|
| L-0506-01 | Refrigerator with freezer | 2 | each | $1,500 | $3,000 |
| L-0506-02 | Microwave (commercial) | 2 | each | $450 | $900 |
| L-0506-03 | Stove/oven with range hood | 1 | each | $3,500 | $3,500 |
| L-0506-04 | Dishwasher | 1 | each | $1,100 | $1,100 |
| L-0506-05 | Laundry set (washer + dryer) | 2 | set | $2,800 | $5,600 |
| L-0506-06 | Installation & connection (all) | 1 | LS | $4,500 | $4,500 |
| | **Total** | | | | **$18,600** |

## Scope Coverage

- **Deliverables in scope:** 1 (DEL-05-06)
- **Deliverables covered:** 1
- **Deliverables blocked:** 0
- **Deliverables excluded:** 0

## Cost Ownership Boundaries (double-count prevention)

| Cost Element | Owner | NOT In |
|---|---|---|
| Appliance equipment purchase + delivery | DEL-05-06 | DEL-05-07 |
| Appliance installation (plumbing/electrical connections) | DEL-05-06 | DEL-02-05, DEL-02-06 |
| Base building kitchen/laundry rough-in (plumbing stubs, circuits) | DEL-02-05 / DEL-02-06 | DEL-05-06 |
| FF&E (loose furniture, fixtures, equipment) | DEL-05-07 | DEL-05-06 |
| $20,000 FF&E allowance items | DEL-05-07 | DEL-05-06 |

## Key Warnings and Notes

1. **Method Classification Decision:** Price source labels appliance items as `PARAMETRIC` basis, but the brief authorizes treating retail appliance pricing as quote-equivalent. Logged as DEC-EST-001.
2. **Range Exposure:** Source provides min/max ranges. Using `RecommendedPrice` (midpoint). Min total = $13,800; Max total = $24,100. See Assumptions_Log.md ASM-002.
3. **Stove/Oven Fuel Type:** Electric or gas range is TBD per design. If gas, a gas service connection may be required (not included in this estimate). See Risk_Register.md RSK-001.
4. **Delivery Costs:** Not separately itemized in source. Assumed included in equipment pricing per ASM-003.
5. **Sales Tax:** Not included. Treatment depends on project tax structure. See ASM-004.
