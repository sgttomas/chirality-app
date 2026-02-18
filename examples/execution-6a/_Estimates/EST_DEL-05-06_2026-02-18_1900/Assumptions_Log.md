# Assumptions Log: EST_DEL-05-06_2026-02-18_1900

## ASM-001 -- Quantities Match OSR S12.6 Minimum

- **Assumption:** Quantities used match the minimum requirements stated in OSR S12.6 and the decomposition (SOW-0505). Specifically:
  - 2 refrigerators with freezers
  - 2 microwaves
  - 1 stove/oven with range hood
  - 1 dishwasher
  - 2 residential laundry sets (washer + dryer per set)
- **Source:** OSR S12.6; Optional_Items_Pricing.csv Notes column (confirms "2 units required per spec" etc.)
- **Risk if wrong:** If Owner requires additional units beyond minimums, estimate will understate.

## ASM-002 -- RecommendedPrice Represents Reasonable Midpoint

- **Assumption:** The `RecommendedPrice` column in Optional_Items_Pricing.csv represents a reasonable midpoint estimate for each appliance.
- **Range exposure:**
  - Minimum total (all PriceMin): $13,800
  - Recommended total: $18,600
  - Maximum total (all PriceMax): $24,100
- **Source:** Optional_Items_Pricing.csv (PriceMin, PriceMax, RecommendedPrice columns)
- **Risk if wrong:** Actual procurement costs may fall anywhere in the min-max range depending on brand selection, procurement timing, and availability.

## ASM-003 -- Delivery Costs Included in Equipment Prices

- **Assumption:** Delivery to site is included in the per-unit equipment prices. No separate delivery line item is included.
- **Source:** Not explicitly stated in Optional_Items_Pricing.csv. Assumed based on typical retail appliance pricing which includes delivery.
- **Risk if wrong:** If delivery is separate, an additional $500-$2,000 may be required depending on supplier location relative to Penhold, AB.

## ASM-004 -- Sales Tax Not Included

- **Assumption:** All amounts in this estimate are pre-tax (exclusive of GST/PST). Sales tax treatment is assumed to be handled at the contract level.
- **Source:** No tax guidance provided in brief or pricing sources.
- **Risk if wrong:** If tax is to be included in the option price, add 5% GST ($930) for a tax-inclusive total of $19,530 (Alberta has no provincial sales tax).

## ASM-005 -- Installation Covers All Appliances in Single Mobilization

- **Assumption:** OPT-17 (appliance installation and connection, $4,500 lump sum) covers installation of all appliances listed in OPT-12 through OPT-16 in a single mobilization.
- **Source:** Optional_Items_Pricing.csv OPT-17 Notes: "Plumbing connections; electrical connections; venting; testing; for all appliances above"
- **Risk if wrong:** If appliance installation requires multiple trades at separate times, installation costs could increase.

## ASM-006 -- Base Building Rough-In Provided by Others

- **Assumption:** All base building rough-in for kitchen and laundry areas (plumbing stubs, dedicated electrical circuits, ventilation connections) is provided under DEL-02-05 (Mechanical) and DEL-02-06 (Electrical) at no cost to DEL-05-06. The DEL-05-06 installation line (L-0506-06) covers only final connections from rough-in points to appliances.
- **Source:** Dependencies.csv DEP-05-06-005 and DEP-05-06-006; Brief cost ownership table.
- **Risk if wrong:** N/A -- this is a confirmed scope boundary, not an assumption about unknowns.
