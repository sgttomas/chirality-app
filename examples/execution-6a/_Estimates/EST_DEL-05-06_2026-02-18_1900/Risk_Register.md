# Risk Register: EST_DEL-05-06_2026-02-18_1900

## RSK-001 -- Stove/Oven Fuel Type May Require Gas Service Connection

- **Risk:** If the stove/oven is gas-fired (rather than electric), a gas service connection to the kitchen area may be required. This connection cost is not included in this estimate.
- **Likelihood:** MEDIUM (fuel type decision TBD per design phase)
- **Impact:** LOW-MEDIUM ($1,500-$5,000 additional for gas line extension from building main to kitchen, depending on routing distance)
- **Source:** Optional_Items_Pricing.csv OPT-14 Notes: "Electric or gas range"; Dependencies.csv run notes mention conditional gas service interface was not extracted under CONSERVATIVE strictness.
- **Mitigation:** Confirm fuel type decision during base building design (DEL-02-05). If gas, add gas connection line item to a future rerun.

## RSK-002 -- Price Volatility on Appliances

- **Risk:** Retail appliance prices may change between estimate date and procurement date. Supply chain disruptions, tariffs, or brand availability could push actual costs toward the upper range.
- **Likelihood:** MEDIUM
- **Impact:** Up to $5,500 (difference between RecommendedPrice total $18,600 and PriceMax total $24,100)
- **Source:** Optional_Items_Pricing.csv min/max range analysis
- **Mitigation:** Obtain actual vendor quotes closer to procurement. Consider specifying "or equivalent" in appliance specifications to allow brand substitution.

## RSK-003 -- Remote Location Premium

- **Risk:** Penhold, AB is a small town. Appliance delivery and installation trades may carry a premium compared to urban centers (Edmonton/Red Deer).
- **Likelihood:** LOW (Red Deer is approximately 20 km away and is a regional service center)
- **Impact:** LOW ($500-$1,500 potential delivery/travel premium)
- **Source:** General knowledge of project location from decomposition (Town of Penhold).
- **Mitigation:** Source appliances and installation services from Red Deer market.
